#!/usr/bin/env python3
"""Local, dependency-free Claude/Codex handoff checks. No network or git writes.

The independent gate is an operator-run process. Agent-supplied JSON/receipts are
claims, not trusted attestations. The gate observes Git and executes checks again.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess
import sys
from typing import Any

VERSION = "1.1"
ROOT = Path(__file__).resolve().parents[1]
TIERS = {"lightweight": 0, "standard": 1, "enhanced": 2}
REQUIRED_HANDOFF = ROOT / "docs" / "agent-handoff.schema.json"
REQUIRED_MANIFEST = ROOT / "docs" / "agent-task.schema.json"


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str | Path, data: Any) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def shape_validate(value: Any, schema: dict, root: dict | None = None, where: str = "$") -> list[str]:
    """Validate the JSON Schema keywords used by the bundled Draft 2020-12 schemas.

    This intentionally fails on any new keyword, rather than silently ignoring
    future schema edits. Also checked against jsonschema in the package tests.
    """
    root = schema if root is None else root
    errors: list[str] = []
    allowed = {"$schema", "$id", "title", "type", "additionalProperties", "required", "properties",
               "const", "enum", "minLength", "pattern", "items", "minItems", "uniqueItems",
               "minimum", "maximum", "$defs", "$ref", "allOf", "if", "then"}
    unknown = set(schema) - allowed
    if unknown:
        return [f"{where}: unsupported schema keywords: {sorted(unknown)}"]
    if "$ref" in schema:
        ref = schema["$ref"]
        if not isinstance(ref, str) or not ref.startswith("#/"):
            return [f"{where}: unsupported schema reference {ref!r}"]
        target = root
        for part in ref[2:].split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        return shape_validate(value, target, root, where)
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append(f"{where}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{where}: not an accepted value")
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        match = {"object": lambda x: isinstance(x, dict), "array": lambda x: isinstance(x, list),
                 "string": lambda x: isinstance(x, str), "integer": lambda x: type(x) is int,
                 "null": lambda x: x is None}
        if not any(match[t](value) for t in types):
            return errors + [f"{where}: expected {types}, got {type(value).__name__}"]
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{where}.{key}: missing required field")
        if schema.get("additionalProperties") is False:
            for key in value.keys() - schema.get("properties", {}).keys():
                errors.append(f"{where}.{key}: unexpected field")
        for key, child in schema.get("properties", {}).items():
            if key in value:
                errors += shape_validate(value[key], child, root, f"{where}.{key}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{where}: too few items")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
            errors.append(f"{where}: contains duplicates")
        if "items" in schema:
            for i, child in enumerate(value):
                errors += shape_validate(child, schema["items"], root, f"{where}[{i}]")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{where}: cannot be empty")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{where}: does not match expected pattern")
    if type(value) is int:
        if value < schema.get("minimum", value) or value > schema.get("maximum", value):
            errors.append(f"{where}: outside accepted numeric range")
    for s in schema.get("allOf", []):
        errors += shape_validate(value, s, root, where)
    if "if" in schema and not shape_validate(value, schema["if"], root, where):
        errors += shape_validate(value, schema["then"], root, where)
    return errors


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=False, timeout=30)
    if result.returncode:
        raise ValueError(f"git {args[0]} failed: {result.stderr.decode(errors='replace').strip()[:240]}")
    return result.stdout


def git_state(repo: Path, base: str) -> dict:
    # `git diff base` includes staged, unstaged, and committed changes; untracked files
    # are collected separately. No checkout, reset, clean, fetch or mutation.
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    branch = git(repo, "symbolic-ref", "--quiet", "--short", "HEAD").decode().strip() if not git_detached(repo) else None
    git(repo, "cat-file", "-e", f"{base}^{{commit}}")
    ancestor = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", base, head], capture_output=True)
    if ancestor.returncode:
        raise ValueError("manifest base_commit is not an ancestor of current HEAD")
    tracked = git(repo, "diff", "--name-only", "--no-renames", "-z", base).split(b"\0")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0")
    names = sorted({p.decode("utf-8", errors="surrogateescape").replace("\\", "/") for p in tracked + untracked if p})
    dirty = bool(git(repo, "status", "--porcelain=v1", "-z"))
    return {"base_commit": base, "head_commit": head, "branch": branch,
            "working_tree": "modified" if dirty else "clean", "changed": names}


def git_detached(repo: Path) -> bool:
    return subprocess.run(["git", "-C", str(repo), "symbolic-ref", "--quiet", "HEAD"], capture_output=True).returncode != 0


def valid_path(path: str) -> bool:
    if not isinstance(path, str) or not path or "\\" in path or "\x00" in path:
        return False
    if path.startswith("/") or path.startswith("./") or path.endswith("/") or ":" in path:
        return False
    if path.endswith("/**"):
        path = path[:-3]
    parts = PurePosixPath(path).parts
    return bool(parts) and not any(p in (".", "..", "*") or "*" in p or "?" in p or "[" in p for p in parts)


def includes(patterns: list[str], path: str) -> bool:
    return any(path == rule or (rule.endswith("/**") and path.startswith(rule[:-2])) for rule in patterns)


def minimum_tier(paths: list[str]) -> str:
    if not paths:
        return "lightweight"
    # All active CI/deployment/security/fixture contracts require enhanced review.
    critical = (".github/workflows/", "tests/fixtures/", "docs/agent-", "tools/collaboration.py")
    if any(p.startswith(critical) or p in {"AGENTS.md", "netlify.toml", "scripts/refresh_fixtures.py"} for p in paths):
        return "enhanced"
    if paths and all(p.endswith((".md", ".txt", ".rst")) for p in paths):
        return "lightweight"
    return "standard"


def semantic_errors(h: dict, m: dict, previous: dict | None = None) -> list[str]:
    errors: list[str] = []
    if h["protocol_version"] != m["protocol_version"] or h["schema_version"] != VERSION:
        errors.append("protocol/schema mismatch; migrate explicitly, do not auto-upgrade")
    if h["task_id"] != m["task_id"] or h["review_tier"] != m["review_tier"]:
        errors.append("handoff task ID or tier differs from operator manifest")
    for field in ("authorized", "protected"):
        if set(h["scope"][field]) != set(m[field]):
            errors.append(f"scope.{field} differs from operator manifest")
    all_paths = [*m["authorized"], *m["protected"], *h["scope"]["changed"]]
    if any(not valid_path(x) for x in all_paths):
        errors.append("paths must be safe relative POSIX paths or directory/** patterns")
    if len(set(h["scope"]["changed"])) != len(h["scope"]["changed"]):
        errors.append("changed files are duplicated")
    for p in h["scope"]["changed"]:
        if not includes(m["authorized"], p):
            errors.append(f"unauthorized changed path: {p}")
        if includes(m["protected"], p):
            errors.append(f"protected path changed: {p}")
    if TIERS[h["review_tier"]] < TIERS[minimum_tier(h["scope"]["changed"])]:
        errors.append(f"review tier too low for changed paths; minimum {minimum_tier(h['scope']['changed'])}")
    if len({c["id"] for c in m["checks"]}) != len(m["checks"]):
        errors.append("duplicate manifest check IDs")
    if len({v["check_id"] for v in h["verification"]}) != len(h["verification"]):
        errors.append("duplicate handoff check IDs")
    if m["review_tier"] in ("standard", "enhanced") and not any(c["kind"] == "tests" for c in m["checks"]):
        errors.append("standard/enhanced review must contain a test check")
    if m["review_tier"] == "enhanced" and len(m["checks"]) < 2:
        errors.append("enhanced review requires at least two independent check commands")
    if h["status"] == "passed":
        if not h["verification"]:
            errors.append("passed handoff has no checks")
        if h["repository"]["working_tree"] == "unknown" or not h["repository"]["head_commit"] or not h["repository"]["base_commit"]:
            errors.append("passed handoff has unknown Git state or commit")
        if h["repository"]["branch"] is None:
            errors.append("passed handoff has unknown/detached branch")
        if h["decisions_required"]:
            errors.append("passed handoff has unresolved human decisions")
        if any(f["state"] != "resolved" and f["severity"] in ("blocking", "major") for f in h["findings"]):
            errors.append("passed handoff has unresolved material findings")
        checks = {c["id"]: c for c in m["checks"]}
        verifications = {v["check_id"]: v for v in h["verification"]}
        if checks.keys() != verifications.keys():
            errors.append("handoff checks do not equal required operator checks")
        for cid, v in verifications.items():
            if cid not in checks:
                continue
            c = checks[cid]
            if v["command"] != shlex.join(c["argv"]) or v["kind"] != c["kind"]:
                errors.append(f"{cid}: command or kind diverges from manifest")
            if v["status"] != "passed" or v["exit_code"] != 0 or not v["evidence"]:
                errors.append(f"{cid}: missing successful result or evidence reference")
            if c["kind"] == "tests" and (v["tests_executed"] is None or v["tests_executed"] < 1):
                errors.append(f"{cid}: no positive test count")
            if c["kind"] != "tests" and v["tests_executed"] is not None:
                errors.append(f"{cid}: non-test check must have null test count")
    if len({f["id"] for f in h["findings"]}) != len(h["findings"]):
        errors.append("duplicate finding IDs")
    for f in h["findings"]:
        if f["state"] == "resolved" and not f["evidence"]:
            errors.append(f"{f['id']}: resolved finding lacks evidence")
    if previous is not None:
        if previous["task_id"] != h["task_id"]:
            errors.append("previous handoff belongs to a different task")
        for prior in previous["findings"]:
            if prior["id"] not in {x["id"] for x in h["findings"]}:
                errors.append(f"prior finding silently dropped: {prior['id']}")
    approved = {(x["action"], x["target"], x["approval_ref"]) for x in m["authorized_external_actions"]}
    for act in h["external_actions"]:
        if not act["approval_ref"] or not act["evidence"]:
            errors.append(f"external action {act['action']}: missing approval reference or evidence")
        if (act["action"], act["target"], act["approval_ref"]) not in approved:
            errors.append(f"external action {act['action']}: not listed in operator authorization manifest")
    return errors


def validate(h: dict, m: dict, previous: dict | None = None) -> list[str]:
    errors = shape_validate(m, read_json(REQUIRED_MANIFEST)) + shape_validate(h, read_json(REQUIRED_HANDOFF))
    if previous is not None:
        errors += shape_validate(previous, read_json(REQUIRED_HANDOFF))
    if errors:
        return errors
    return semantic_errors(h, m, previous)


def verify_repo(h: dict, m: dict, repo: Path) -> list[str]:
    state = git_state(repo, m["base_commit"])
    errors = []
    if h["repository"] != {k: state[k] for k in ("base_commit", "head_commit", "branch", "working_tree")}:
        errors.append("handoff Git state differs from independently observed repository state")
    if set(state["changed"]) != set(h["scope"]["changed"]):
        errors.append(f"observed changed paths differ: observed={state['changed']}")
    for p in state["changed"]:
        if not includes(m["authorized"], p):
            errors.append(f"observed unauthorized path: {p}")
        if includes(m["protected"], p):
            errors.append(f"observed protected path modification: {p}")
    if TIERS[m["review_tier"]] < TIERS[minimum_tier(state["changed"])]:
        errors.append("observed changes demand a higher review tier")
    return errors


def parse_test_count(output: str) -> int | None:
    if re.search(r"\bRan\s+0\s+tests?\b|\bno tests ran\b|\b0 passed\b", output, re.I):
        return 0
    matches = re.findall(r"\bRan\s+(\d+)\s+tests?\b", output)
    if not matches:
        matches = re.findall(r"\b(\d+)\s+passed(?:\s+in\s+|\s*,|\s*$)", output, re.M)
    return int(matches[-1]) if matches else None


def prohibited_check_command(argv: list[str]) -> bool:
    """Block obvious external/destructive commands; not a sandbox for arbitrary code."""
    executable = Path(argv[0].replace("\\", "/")).name.lower()
    if executable.endswith(".exe"):
        executable = executable[:-4]
    if executable in {"gh", "curl", "wget", "ssh", "scp", "rm", "rmdir", "del", "pwsh", "powershell", "bash", "sh", "cmd"}:
        return True
    if executable == "git":
        # Read-only Git commands are sufficient for gate checks; disallow writes/network.
        arguments = argv[1:]
        while arguments and arguments[0] in ("-C", "--git-dir", "--work-tree"):
            arguments = arguments[2:]
        return not arguments or arguments[0] not in {"diff", "status", "show", "log", "rev-parse", "ls-files"}
    return False


def run_checks(repo: Path, h: dict, m: dict) -> tuple[list[str], list[dict]]:
    errors, receipts = [], []
    claims = {v["check_id"]: v for v in h["verification"]}
    observed_environment = "local_windows" if sys.platform == "win32" else "local_linux"
    for check in m["checks"]:
        cid = check["id"]
        claim = claims[cid]
        if prohibited_check_command(check["argv"]):
            errors.append(f"{cid}: potentially destructive/network check command is forbidden")
            receipts.append({"check_id": cid, "error": "command forbidden"})
            continue
        try:
            # argv list and shell=False. No command execution from handoff prose.
            process = subprocess.run(check["argv"], cwd=repo, capture_output=True, timeout=check["timeout_seconds"], check=False)
            raw_output = process.stdout + b"\n" + process.stderr
            log = raw_output.decode("utf-8", errors="replace")
            count = parse_test_count(log) if check["kind"] == "tests" else None
            receipt = {"check_id": cid, "argv": check["argv"], "exit_code": process.returncode,
                       "tests_executed": count, "sha256_of_output": hashlib.sha256(raw_output).hexdigest(),
                       "environment": observed_environment, "output_tail": log[-4000:]}
            receipts.append(receipt)
            if process.returncode or (check["kind"] == "tests" and (count is None or count < 1)):
                errors.append(f"{cid}: independent check failed or nonzero test count unavailable (exit={process.returncode}, tests={count})")
            if claim["exit_code"] != process.returncode or claim["tests_executed"] != count:
                errors.append(f"{cid}: reported result differs from independent execution")
            if claim["environment"] != observed_environment:
                errors.append(f"{cid}: reported environment differs from independent execution")
        except (OSError, subprocess.TimeoutExpired) as exc:
            errors.append(f"{cid}: independent check could not complete: {type(exc).__name__}")
            receipts.append({"check_id": cid, "error": type(exc).__name__})
    return errors, receipts


def prepare(m: dict, repo: Path) -> dict:
    state = git_state(repo, m["base_commit"])
    return {"schema_version": VERSION, "protocol_version": VERSION, "task_id": m["task_id"],
            "phase": "implementation", "review_tier": m["review_tier"], "status": "not_run",
            "scope": {"authorized": m["authorized"], "changed": state["changed"], "protected": m["protected"]},
            "repository": {k: state[k] for k in ("base_commit", "head_commit", "branch", "working_tree")},
            "verification": [{"check_id": ch["id"], "command": shlex.join(ch["argv"]), "kind": ch["kind"],
                              "exit_code": None, "tests_executed": None, "status": "not_run",
                              "environment": "local_windows" if sys.platform == "win32" else "local_linux",
                              "evidence": None} for ch in m["checks"]],
            "findings": [], "decisions_required": [], "external_actions": [],
            "next_recommended_action": "Run actual checks; populate exact observations; request independent gate."}


def metrics_record(path: Path, event: dict) -> None:
    allowed = {"task_id", "workflow", "elapsed_minutes", "review_rounds", "confirmed_findings", "false_alarms",
               "independent_defects", "escaped_defects", "recurrences"}
    if set(event) != allowed or not isinstance(event["task_id"], str) or not event["task_id"]:
        raise ValueError("invalid metrics event fields")
    if event["workflow"] not in ("codex_only", "claude_codex"):
        raise ValueError("workflow must be codex_only or claude_codex")
    if any(type(event[k]) is not int or event[k] < 0 for k in allowed - {"task_id", "workflow"}):
        raise ValueError("metric counts/minutes must be nonnegative integers")
    if event["independent_defects"] > event["confirmed_findings"]:
        raise ValueError("independently detected defects cannot exceed confirmed findings")
    record = {**event, "recorded_at_utc": datetime.now(timezone.utc).isoformat()}
    with path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(record, ensure_ascii=False) + "\n")


def metrics_summary(path: Path) -> dict:
    groups: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        v = json.loads(line)
        name = v["workflow"]
        out = groups.setdefault(name, {"tasks": 0, "elapsed_minutes": 0, "review_rounds": 0,
                                       "confirmed_findings": 0, "false_alarms": 0, "independent_defects": 0,
                                       "escaped_defects": 0, "recurrences": 0})
        out["tasks"] += 1
        for k in out.keys() - {"tasks"}:
            out[k] += v[k]
    for v in groups.values():
        v["mean_elapsed_minutes"] = round(v["elapsed_minutes"] / v["tasks"], 2)
        denom = v["confirmed_findings"] + v["false_alarms"]
        v["review_precision"] = round(v["confirmed_findings"] / denom, 3) if denom else None
        v["escape_rate_per_task"] = round(v["escaped_defects"] / v["tasks"], 3)
    return groups


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "validate", "gate"):
        p = sub.add_parser(name)
        p.add_argument("--manifest", required=True)
        if name != "prepare":
            p.add_argument("--handoff", required=True)
            p.add_argument("--previous")
        if name != "validate":
            p.add_argument("--repo", required=True)
        if name == "prepare":
            p.add_argument("--out", required=True)
        if name == "gate":
            p.add_argument("--out", help="Optional independent receipt JSON; use a path OUTSIDE the working repo")
    rec = sub.add_parser("record-outcome")
    rec.add_argument("--ledger", required=True)
    rec.add_argument("--event", required=True, help="JSON file of confirmed outcome measurements")
    summ = sub.add_parser("summarize")
    summ.add_argument("--ledger", required=True)
    args = parser.parse_args()
    try:
        if args.command == "record-outcome":
            metrics_record(Path(args.ledger), read_json(args.event))
            print("Recorded operator-supplied measurements; not independently audited")
            return 0
        if args.command == "summarize":
            print(json.dumps(metrics_summary(Path(args.ledger)), indent=2))
            return 0
        m = read_json(args.manifest)
        if args.command in ("prepare", "gate") and Path(args.manifest).resolve().is_relative_to(Path(args.repo).resolve()):
            raise ValueError("operator manifest must reside outside the working repository")
        me = shape_validate(m, read_json(REQUIRED_MANIFEST))
        if me:
            raise ValueError("; ".join(me))
        if any(not valid_path(p) for p in m["authorized"] + m["protected"]):
            raise ValueError("manifest contains invalid path patterns")
        if args.command == "prepare":
            out = Path(args.out).resolve()
            if out.is_relative_to(Path(args.repo).resolve()):
                raise ValueError("handoff output must be outside repository")
            h = prepare(m, Path(args.repo).resolve())
            save_json(out, h)
            print(f"Prepared unverified handoff: {out}")
            return 0
        h = read_json(args.handoff)
        previous = read_json(args.previous) if args.previous else None
        errors = validate(h, m, previous)
        receipts = []
        if args.command == "gate" and not errors:
            repo = Path(args.repo).resolve()
            if args.out and Path(args.out).resolve().is_relative_to(repo):
                errors.append("gate receipt must be outside repository")
            elif h["status"] != "passed":
                errors.append("only passed handoffs are eligible for independent gate")
            else:
                errors += verify_repo(h, m, repo)
                if not errors:
                    recheck_errors, receipts = run_checks(repo, h, m)
                    errors += recheck_errors
                    # Checks may mutate the working tree; never trust the pre-check observation alone.
                    errors += verify_repo(h, m, repo)
        report = {"result": "BLOCK" if errors else ("TECHNICALLY_VERIFIED" if args.command == "gate" else "SEMANTICALLY_VALID_UNVERIFIED"),
                  "errors": errors, "independent_receipts": receipts,
                  "human_authorization_still_required": True}
        if args.command == "gate" and args.out:
            save_json(args.out, report)
        print(json.dumps(report, indent=2))
        return 1 if errors else 0
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"result": "BLOCK", "errors": [str(exc)], "human_authorization_still_required": True}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
