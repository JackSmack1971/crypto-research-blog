#!/usr/bin/env python3
"""Validate and render write-tickets boards. Stdlib only; no remote actions.

Usage:
  python ticket_board.py validate --root tickets [--check-rendered]
  python ticket_board.py render --root tickets [--write]
  python ticket_board.py fingerprint --root tickets --id 001-feature-name

Exit 0 for verified success; 1 for invalid data, unsafe output, or I/O failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ID_PATTERN = re.compile(r"^[0-9]{3,}-[a-z0-9]+(?:-[a-z0-9]+)*$")
REQ_PATTERN = re.compile(r"^\s*-\s+\*\*(R-[0-9]{2,})\*\*:\s+(.\S.*|\S)\s*$")
EVAL_PATTERN = re.compile(r"^\s*\|\s*(R-[0-9]{2,})\s*\|")
TICKET_MARKER_PATTERN = re.compile(r"^\*\*Ticket:\*\*\s+(\S+)\s*$", re.M)
RESOURCE_PLACEHOLDERS = {"unknown", "unassessed", "none", "todo", "tbd", "?"}
HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
HEADER_PATTERN = re.compile(r"^<!-- write-tickets-board:v1 body-sha256:([0-9a-f]{64}) -->\n")
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD)\b|<Feature title>|<NNN-feature-slug>|\bdecision required\b", re.I)
VALID_STATUSES = {"draft", "ready", "in_progress", "done"}
ENTRY_FIELDS = {"id", "title", "status", "depends_on", "resources", "parallel_safe", "blocker", "open_decisions", "approval"}
FINGERPRINT_FIELDS = ("id", "title", "depends_on", "resources", "parallel_safe", "open_decisions")


def sort_key(ticket_id: str) -> tuple[int, str]:
    return int(ticket_id.split("-", 1)[0]), ticket_id


def is_nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def root_path(root: str | Path) -> Path:
    path = Path(root)
    if path.is_symlink():
        raise ValueError(f"Refusing symlink ticket root: {path}")
    if not path.is_dir():
        raise ValueError(f"Ticket root does not exist or is not a directory: {path}")
    return path


def read_manifest(root: Path) -> dict:
    path = root / "board.json"
    if path.is_symlink():
        raise ValueError(f"Refusing symlink manifest: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read valid board.json: {exc}") from exc
    if not isinstance(data, dict) or set(data) != {"schema_version", "tickets"}:
        raise ValueError("board.json must contain exactly schema_version and tickets")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("board.json schema_version must be integer 1")
    if not isinstance(data["tickets"], list) or not data["tickets"]:
        raise ValueError("board.json tickets must be a nonempty array")
    return data


def get_documents(root: Path, ticket_id: str) -> tuple[bytes, bytes]:
    if not ID_PATTERN.fullmatch(ticket_id):
        raise ValueError(f"Invalid ticket ID: {ticket_id!r}")
    directory = root / ticket_id
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Missing ticket directory or unsafe symlink: {directory}")
    docs: list[bytes] = []
    for filename in ("rd.md", "eval.md"):
        path = directory / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing ticket document or unsafe symlink: {path}")
        docs.append(path.read_bytes())
    return docs[0], docs[1]


def fingerprint(entry: dict, docs: tuple[bytes, bytes]) -> str:
    """Bind approval to contents and decision-changing board metadata."""
    h = hashlib.sha256()
    h.update(b"write-tickets-approval:v1\x00")
    metadata = {key: entry[key] for key in FINGERPRINT_FIELDS}
    h.update(json.dumps(metadata, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    for name, content in zip(("rd.md", "eval.md"), docs):
        h.update(name.encode("ascii") + b"\x00")
        h.update(len(content).to_bytes(8, byteorder="big"))
        h.update(content)
    return h.hexdigest()


def requirement_ids(rd: str, ev: str, ticket_id: str) -> list[str]:
    errors: list[str] = []
    r_ids: list[str] = []
    for line in rd.splitlines():
        match = REQ_PATTERN.match(line)
        if match:
            r_ids.append(match.group(1))
    if not r_ids:
        errors.append(f"{ticket_id}: rd.md has no '- **R-01**: ...' requirements")
    elif len(r_ids) != len(set(r_ids)):
        errors.append(f"{ticket_id}: duplicate requirement IDs in rd.md")
    e_ids: list[str] = []
    for line in ev.splitlines():
        match = EVAL_PATTERN.match(line)
        if not match:
            continue
        e_ids.append(match.group(1))
        cells = [part.strip() for part in re.split(r"(?<!\\)\|", line.strip().strip("|"))]
        if len(cells) != 4 or any(not cell for cell in cells):
            errors.append(f"{ticket_id}: eval row {match.group(1)} must have four nonempty cells")
    if len(e_ids) != len(set(e_ids)):
        errors.append(f"{ticket_id}: duplicate requirement IDs in eval.md")
    for missing in sorted(set(r_ids) - set(e_ids)):
        errors.append(f"{ticket_id}: no eval.md row for {missing}")
    for extra in sorted(set(e_ids) - set(r_ids)):
        errors.append(f"{ticket_id}: eval.md row {extra} has no rd.md requirement")
    return errors


def graph_layers(by_id: dict[str, dict]) -> list[list[str]]:
    remaining = set(by_id)
    layers: list[list[str]] = []
    done: set[str] = set()
    while remaining:
        current = sorted(
            (t for t in remaining if set(by_id[t]["depends_on"]).issubset(done)),
            key=sort_key,
        )
        if not current:
            raise ValueError("Dependency cycle detected: " + ", ".join(sorted(remaining)))
        layers.append(current)
        done.update(current)
        remaining.difference_update(current)
    return layers


def check(root: Path, data: dict) -> list[str]:
    errors: list[str] = []
    ids: set[str] = set()
    by_id: dict[str, dict] = {}
    used_numbers: dict[int, str] = {}
    for n, entry in enumerate(data["tickets"], 1):
        loc = f"entry #{n}"
        if not isinstance(entry, dict):
            errors.append(f"{loc}: must be an object")
            continue
        if set(entry) != ENTRY_FIELDS:
            errors.append(f"{loc}: expected fields {', '.join(sorted(ENTRY_FIELDS))}; actual {', '.join(sorted(entry))}")
            continue
        name = entry["id"]
        if not isinstance(name, str) or not ID_PATTERN.fullmatch(name):
            errors.append(f"{loc}: invalid ticket id {name!r}")
            continue
        if name in ids:
            errors.append(f"{loc}: duplicate ticket id {name}")
            continue
        ids.add(name)
        number = int(name.split("-", 1)[0])
        if number in used_numbers:
            errors.append(f"{name}: numeric prefix already used by {used_numbers[number]}")
        else:
            used_numbers[number] = name
        by_id[name] = entry
        if not is_nonblank(entry["title"]):
            errors.append(f"{name}: title must be nonblank")
        if entry["status"] not in VALID_STATUSES:
            errors.append(f"{name}: invalid status {entry['status']!r}")
        for field in ("depends_on", "resources", "open_decisions"):
            values = entry[field]
            if not isinstance(values, list) or any(not is_nonblank(v) for v in values):
                errors.append(f"{name}: {field} must be an array of nonblank strings")
            elif len(values) != len(set(values)):
                errors.append(f"{name}: {field} contains duplicate values")
        if type(entry["parallel_safe"]) is not bool:
            errors.append(f"{name}: parallel_safe must be boolean")
        elif entry["parallel_safe"]:
            if not isinstance(entry["resources"], list) or not entry["resources"]:
                errors.append(f"{name}: parallel_safe requires nonempty shared-resource inventory")
            elif any(isinstance(resource, str) and resource.strip().lower() in RESOURCE_PLACEHOLDERS for resource in entry["resources"]):
                errors.append(f"{name}: parallel_safe resources contain unresolved placeholders")
        if entry["blocker"] is not None and not is_nonblank(entry["blocker"]):
            errors.append(f"{name}: blocker must be null or a nonblank string")
        approval = entry["approval"]
        if entry["status"] == "draft":
            if approval is not None:
                errors.append(f"{name}: draft must have approval null")
        else:
            if not isinstance(approval, dict) or set(approval) != {"ref", "fingerprint"}:
                errors.append(f"{name}: {entry['status']} requires approval ref and fingerprint")
            elif not is_nonblank(approval["ref"]) or not isinstance(approval["fingerprint"], str) or not HASH_PATTERN.fullmatch(approval["fingerprint"]):
                errors.append(f"{name}: approval ref must be nonblank and fingerprint 64 hex characters")
            if isinstance(entry["open_decisions"], list) and entry["open_decisions"]:
                errors.append(f"{name}: approved ticket has unresolved open_decisions")
        try:
            rd_bytes, ev_bytes = get_documents(root, name)
            rd = rd_bytes.decode("utf-8")
            ev = ev_bytes.decode("utf-8")
            if not rd.strip() or not ev.strip():
                errors.append(f"{name}: empty requirements or evaluation document")
            for filename, content in (("rd.md", rd), ("eval.md", ev)):
                markers = TICKET_MARKER_PATTERN.findall(content)
                if markers != [name]:
                    errors.append(f"{name}: {filename} must contain exactly one '**Ticket:** {name}' marker")
            errors.extend(requirement_ids(rd, ev, name))
            if entry["status"] != "draft":
                if PLACEHOLDER_PATTERN.search(rd) or PLACEHOLDER_PATTERN.search(ev):
                    errors.append(f"{name}: approved ticket contains TODO/TBD/decision-required/template placeholder")
                if isinstance(approval, dict) and isinstance(approval.get("fingerprint"), str):
                    if fingerprint(entry, (rd_bytes, ev_bytes)) != approval["fingerprint"]:
                        errors.append(f"{name}: approval fingerprint stale; revert to draft and request reapproval")
        except (UnicodeDecodeError, ValueError, OSError) as exc:
            errors.append(f"{name}: {exc}")
    for name, entry in by_id.items():
        if not isinstance(entry.get("depends_on"), list) or not all(isinstance(v, str) for v in entry["depends_on"]):
            continue
        for dep in entry["depends_on"]:
            if dep == name:
                errors.append(f"{name}: cannot depend on itself")
            elif dep not in ids:
                errors.append(f"{name}: missing dependency {dep}")
    if not errors:
        try:
            graph_layers(by_id)
        except ValueError as exc:
            errors.append(str(exc))
    for child in root.iterdir():
        if re.fullmatch(r"[0-9]{3,}-.*", child.name) and child.name not in ids:
            if child.is_dir() or child.is_symlink():
                errors.append(f"Unlisted ticket directory: {child.name}")
    return errors


def normalized_resource(resource: str) -> str:
    return resource.strip().replace("\\", "/").rstrip("/").casefold()


def resources_conflict(first: set[str], second: set[str]) -> bool:
    """Conservatively treat identical resources and nested paths as shared."""
    for a in first:
        for b in second:
            if a == b or a.startswith(b + "/") or b.startswith(a + "/"):
                return True
    return False


def candidate_batches(eligible: list[dict]) -> list[list[dict]]:
    batches: list[list[dict]] = []
    current: list[dict] = []
    occupied: set[str] = set()
    for entry in sorted(eligible, key=lambda e: sort_key(e["id"])):
        resources = {normalized_resource(resource) for resource in entry["resources"]}
        if not entry["parallel_safe"]:
            if current:
                batches.append(current)
            batches.append([entry])
            current = []
            occupied = set()
            continue
        if current and resources_conflict(resources, occupied):
            batches.append(current)
            current = []
            occupied = set()
        current.append(entry)
        occupied.update(resources)
    if current:
        batches.append(current)
    return batches


def render_body(data: dict) -> str:
    by_id = {e["id"]: e for e in data["tickets"]}
    entries = sorted(data["tickets"], key=lambda e: sort_key(e["id"]))
    eligible: list[dict] = []
    waiting: list[tuple[dict, str]] = []
    drafts: list[dict] = []
    active: list[dict] = []
    done: list[dict] = []
    for entry in entries:
        status = entry["status"]
        if status == "draft":
            drafts.append(entry)
        elif status == "ready":
            pending = [dep for dep in entry["depends_on"] if by_id[dep]["status"] != "done"]
            reasons: list[str] = []
            if pending:
                reasons.append("unfinished dependencies: " + ", ".join(pending))
            if entry["blocker"]:
                reasons.append("blocker: " + entry["blocker"])
            if reasons:
                waiting.append((entry, "; ".join(reasons)))
            else:
                eligible.append(entry)
        elif status == "in_progress":
            active.append(entry)
        else:
            done.append(entry)

    lines = [
        "# Ticket board", "",
        "> Generated from `board.json`. Do not edit this file directly. `ready` requires explicit user approval; candidate batches are **not** authorization to implement or run agents in parallel.",
        "", f"**Totals:** {len(entries)} tickets · {len(drafts)} draft · {len(eligible) + len(waiting)} ready · {len(active)} in progress · {len(done)} done", "",
        "## Eligible now (approved and dependencies done)", "",
    ]
    if eligible:
        lines.extend(["| Ticket | Parallel assessed? | Shared resources |", "|---|---|---|"])
        for entry in eligible:
            lines.append(f"| [{entry['id']}]({entry['id']}/rd.md) | {'Candidate' if entry['parallel_safe'] else 'No; serialize'} | {', '.join(entry['resources']) or 'unassessed'} |")
    else:
        lines.append("None.")
    lines.extend(["", "## Conservative candidate dispatch batches", ""])
    batches = candidate_batches(eligible)
    if batches:
        for i, batch in enumerate(batches, 1):
            names = ", ".join(f"`{entry['id']}`" for entry in batch)
            annotation = "candidate concurrently, subject to independent isolation check" if len(batch) > 1 else "one ticket at a time"
            lines.append(f"- Batch {i}: {names} — {annotation}")
        lines.append("")
        lines.append("Do not launch separate batches simultaneously. Reassess real files, worktrees, shared state, permissions and integration ownership before dispatch; conservative grouping does not prove isolation.")
    else:
        lines.append("No dispatch candidates until an approved ticket is unblocked.")
    lines.extend(["", "## Ready but waiting", ""])
    if waiting:
        for entry, reason in waiting:
            lines.append(f"- `{entry['id']}` — {reason}")
    else:
        lines.append("None.")
    lines.extend(["", "## Draft — approval required", ""])
    if drafts:
        for entry in drafts:
            decisions = "; ".join(entry["open_decisions"])
            lines.append(f"- `{entry['id']}` — {entry['title']}" + (f"; decisions: {decisions}" if decisions else ""))
    else:
        lines.append("None.")
    lines.extend(["", "## In progress", ""])
    lines.extend([f"- `{e['id']}` — {e['title']}" for e in active] or ["None."])
    lines.extend(["", "## Done", ""])
    lines.extend([f"- `{e['id']}` — {e['title']}" for e in done] or ["None."])
    lines.extend(["", "## Dependency layers (planning only; ignore statuses)", ""])
    for i, layer in enumerate(graph_layers(by_id), 1):
        lines.append(f"- Layer {i}: " + ", ".join(f"`{ticket}`" for ticket in layer))
    lines.extend(["", "Layers express dependency order only. They do not establish approval, safe parallelism, or implementation progress.", ""])
    return "\n".join(lines)


def rendered_board(data: dict) -> str:
    body = render_body(data)
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return f"<!-- write-tickets-board:v1 body-sha256:{digest} -->\n" + body


def is_intact_generated_board(content: str) -> bool:
    match = HEADER_PATTERN.match(content)
    if not match:
        return False
    actual = hashlib.sha256(content[match.end():].encode("utf-8")).hexdigest()
    return actual == match.group(1)


def write_board(root: Path, content: str) -> None:
    target = root / "BOARD.md"
    if target.is_symlink():
        raise ValueError("Refusing to overwrite symlink BOARD.md")
    if target.exists():
        old = target.read_text(encoding="utf-8")
        if not is_intact_generated_board(old):
            raise ValueError("Refusing to overwrite unrecognized or manually modified BOARD.md")
        if old == content:
            return
    tmp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", prefix=".write-tickets-", suffix=".tmp", dir=root, delete=False) as tmp:
            tmp.write(content)
            tmp_name = tmp.name
        os.replace(tmp_name, target)
    finally:
        if tmp_name and os.path.exists(tmp_name):
            os.unlink(tmp_name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="Validate schema, traceability, graph, approval fingerprints")
    validate.add_argument("--root", default="tickets")
    validate.add_argument("--check-rendered", action="store_true")
    render = sub.add_parser("render", help="Print or safely write a generated BOARD.md")
    render.add_argument("--root", default="tickets")
    render.add_argument("--write", action="store_true")
    fp = sub.add_parser("fingerprint", help="Compute a ticket-version hash; not user approval")
    fp.add_argument("--root", default="tickets")
    fp.add_argument("--id", required=True)
    args = parser.parse_args(argv)
    try:
        root = root_path(args.root)
        data = read_manifest(root)
        if args.command == "fingerprint":
            entries = [e for e in data["tickets"] if isinstance(e, dict) and e.get("id") == args.id]
            if len(entries) != 1 or not all(k in entries[0] for k in FINGERPRINT_FIELDS):
                raise ValueError("Unknown or invalid ticket ID in manifest")
            print(fingerprint(entries[0], get_documents(root, args.id)))
            return 0
        errors = check(root, data)
        if errors:
            for error in errors:
                print("ERROR: " + error, file=sys.stderr)
            return 1
        proposed = rendered_board(data)
        if args.command == "render":
            if args.write:
                write_board(root, proposed)
                print(f"WROTE: {root / 'BOARD.md'}")
            else:
                sys.stdout.write(proposed)
        else:
            if args.check_rendered:
                path = root / "BOARD.md"
                if path.is_symlink() or not path.is_file() or path.read_text(encoding="utf-8") != proposed:
                    raise ValueError("BOARD.md absent, stale, or modified; render after reconciling edits")
            print(f"PASS: {len(data['tickets'])} ticket(s), requirement mapping, dependency graph, approvals" + (", generated board" if args.check_rendered else ""))
        return 0
    except (ValueError, OSError, UnicodeError, TypeError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
