"""Focused safety regression tests for the collaboration verification gate."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import collaboration as c


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"
        self.repo.mkdir()
        def git(*args):
            return subprocess.run(["git", "-C", str(self.repo), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode().strip()
        self.git = git
        git("init", "-q", "-b", "main")
        (self.repo / "README.md").write_text("Initial\n")
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts" / "verify.py").write_text("print('Ran 3 tests in 0.1s')\n")
        git("add", "README.md", "scripts/verify.py")
        git("-c", "user.name=Test", "-c", "user.email=test@example.test", "commit", "-qm", "init")
        base = git("rev-parse", "HEAD")
        self.manifest = {
            "protocol_version": "1.1", "task_id": "TASK-1", "review_tier": "lightweight",
            "base_commit": base, "authorized": ["README.md"], "protected": ["tests/fixtures/**"],
            "checks": [{"id": "diff", "argv": [sys.executable, "-c", "print('okay')"], "kind": "review", "timeout_seconds": 10}],
            "authorized_external_actions": []
        }
        (self.repo / "README.md").write_text("Changed\n")
        self.h = c.prepare(self.manifest, self.repo)
        self.pass_handoff()

    def pass_handoff(self):
        self.h.update({"phase": "verification", "status": "passed", "verification": [
            {"check_id": ch["id"], "command": c.shlex.join(ch["argv"]), "kind": ch["kind"],
             "exit_code": 0, "tests_executed": 3 if ch["kind"] == "tests" else None,
             "status": "passed", "environment": "local_linux" if sys.platform != "win32" else "local_windows",
             "evidence": "local log (operator should retain original)"} for ch in self.manifest["checks"]]})

    def test_valid_passes_semantic_and_independent_gate(self):
        self.assertEqual(c.validate(self.h, self.manifest), [])
        self.assertEqual(c.verify_repo(self.h, self.manifest, self.repo), [])
        errors, receipts = c.run_checks(self.repo, self.h, self.manifest)
        self.assertEqual(errors, [])
        self.assertEqual(len(receipts), 1)

    def test_pass_without_checks_rejected(self):
        self.h["verification"] = []
        self.assertIn("passed handoff has no checks", c.validate(self.h, self.manifest))

    def test_unknown_git_state_rejected(self):
        self.h["repository"]["working_tree"] = "unknown"
        self.assertTrue(c.validate(self.h, self.manifest))

    def test_modified_protected_path_rejected(self):
        self.h["scope"]["changed"].append("tests/fixtures/metadata.json")
        self.assertTrue(any("protected path" in e for e in c.validate(self.h, self.manifest)))

    def test_unauthorized_path_rejected(self):
        self.h["scope"]["changed"].append("assets/secret.css")
        self.assertTrue(any("unauthorized" in e for e in c.validate(self.h, self.manifest)))

    def test_actual_extra_untracked_file_rejected_even_if_reported_clean(self):
        (self.repo / "surprise.txt").write_text("untracked")
        self.assertTrue(c.verify_repo(self.h, self.manifest, self.repo))

    def test_stale_head_rejected(self):
        self.h["repository"]["head_commit"] = "f" * 40
        self.assertTrue(c.verify_repo(self.h, self.manifest, self.repo))

    def test_zero_tests_rejected_by_schema_and_semantics(self):
        self.manifest["review_tier"] = self.h["review_tier"] = "standard"
        self.manifest["checks"][0]["kind"] = self.h["verification"][0]["kind"] = "tests"
        self.h["verification"][0]["tests_executed"] = 0
        self.assertTrue(c.validate(self.h, self.manifest))

    def test_independently_detects_fake_test_count(self):
        self.manifest["review_tier"] = self.h["review_tier"] = "standard"
        self.manifest["checks"][0]["kind"] = self.h["verification"][0]["kind"] = "tests"
        self.manifest["checks"][0]["argv"] = [sys.executable, "scripts/verify.py"]
        self.h["verification"][0]["command"] = c.shlex.join(self.manifest["checks"][0]["argv"])
        self.h["verification"][0]["tests_executed"] = 100
        self.assertFalse(c.validate(self.h, self.manifest))
        errors, receipts = c.run_checks(self.repo, self.h, self.manifest)
        self.assertTrue(any("reported result differs" in x for x in errors))
        self.assertEqual(receipts[0]["tests_executed"], 3)

    def test_not_run_can_be_prepared_but_not_successful(self):
        unverified = c.prepare(self.manifest, self.repo)
        self.assertEqual(c.validate(unverified, self.manifest), [])
        self.assertNotEqual(unverified["status"], "passed")

    def test_silent_finding_drop_rejected(self):
        old = copy.deepcopy(self.h)
        old["findings"] = [{"id": "TASK-1-F01", "state": "open", "severity": "major", "evidence": "issue", "acceptance": "fixed"}]
        self.assertTrue(any("silently dropped" in x for x in c.validate(self.h, self.manifest, old)))

    def test_resolved_finding_requires_evidence(self):
        self.h["findings"] = [{"id": "F1", "state": "resolved", "severity": "blocking", "evidence": None, "acceptance": "fixed"}]
        self.assertTrue(any("lacks evidence" in x for x in c.validate(self.h, self.manifest)))

    def test_external_action_requires_operator_manifest_authorization(self):
        self.h["external_actions"] = [{"action": "push", "target": "main", "approval_ref": "claim", "evidence": "URL"}]
        self.assertTrue(any("not listed" in x for x in c.validate(self.h, self.manifest)))

    def test_downgrade_critical_tier_blocked(self):
        self.h["scope"]["changed"] = [".github/workflows/pages.yml"]
        self.manifest["authorized"] = self.h["scope"]["authorized"] = [".github/workflows/**"]
        self.assertTrue(any("review tier too low" in x for x in c.validate(self.h, self.manifest)))

    def test_schema_protocol_incompatibility_rejected(self):
        self.h["schema_version"] = "1.0"
        self.assertTrue(c.validate(self.h, self.manifest))

    def test_unresolved_decision_blocks_pass(self):
        self.h["decisions_required"] = ["Approve baseline"]
        self.assertTrue(c.validate(self.h, self.manifest))

    def test_missing_tests_does_not_count_as_passing(self):
        self.manifest["review_tier"] = self.h["review_tier"] = "standard"
        self.assertTrue(any("must contain a test" in x for x in c.validate(self.h, self.manifest)))

    def test_manifest_check_command_mismatch(self):
        self.h["verification"][0]["command"] = "echo passed"
        self.assertTrue(any("diverges" in x for x in c.validate(self.h, self.manifest)))

    def test_protected_worktree_file_independently_detected(self):
        (self.repo / "tests/fixtures").mkdir(parents=True)
        (self.repo / "tests/fixtures/metadata.json").write_text("{}")
        self.assertTrue(any("protected" in x for x in c.verify_repo(self.h, self.manifest, self.repo)))

    def test_path_glob_does_not_match_sibling(self):
        self.assertTrue(c.includes(["docs/**"], "docs/a.txt"))
        self.assertFalse(c.includes(["docs/**"], "docs2/a.txt"))
        self.assertFalse(c.valid_path("../tests/fixtures/**"))

    def test_end_to_end_cli_prepare_validate_and_gate(self):
        base = Path(self.tmp.name)
        manifest_path = base / "manifest.json"
        handoff_path = base / "handoff.json"
        receipt_path = base / "receipt.json"
        c.save_json(manifest_path, self.manifest)
        command = [sys.executable, str(Path(c.__file__).resolve())]
        prep = subprocess.run(command + ["prepare", "--repo", str(self.repo), "--manifest", str(manifest_path), "--out", str(handoff_path)], capture_output=True, text=True)
        self.assertEqual(prep.returncode, 0, prep.stdout + prep.stderr)
        prepared = c.read_json(handoff_path)
        self.assertEqual(prepared["status"], "not_run")
        self.assertEqual(len(prepared["verification"]), 1)
        prepared.update({"phase": "verification", "status": "passed"})
        prepared["verification"][0].update({"status": "passed", "exit_code": 0, "evidence": "retained log", "tests_executed": None})
        c.save_json(handoff_path, prepared)
        val = subprocess.run(command + ["validate", "--manifest", str(manifest_path), "--handoff", str(handoff_path)], capture_output=True, text=True)
        self.assertEqual(val.returncode, 0, val.stdout)
        self.assertEqual(json.loads(val.stdout)["result"], "SEMANTICALLY_VALID_UNVERIFIED")
        gate = subprocess.run(command + ["gate", "--repo", str(self.repo), "--manifest", str(manifest_path), "--handoff", str(handoff_path), "--out", str(receipt_path)], capture_output=True, text=True)
        self.assertEqual(gate.returncode, 0, gate.stdout + gate.stderr)
        self.assertEqual(c.read_json(receipt_path)["result"], "TECHNICALLY_VERIFIED")
        self.assertFalse((self.repo / "receipt.json").exists())

    def test_cli_blocks_manifest_inside_repository(self):
        manifest_path = self.repo / "manifest.json"
        c.save_json(manifest_path, self.manifest)
        out = Path(self.tmp.name) / "handoff.json"
        run = subprocess.run([sys.executable, str(Path(c.__file__).resolve()), "prepare", "--repo", str(self.repo), "--manifest", str(manifest_path), "--out", str(out)], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("outside", run.stdout)

    def test_multiple_test_summaries_with_zero_fail_closed(self):
        self.assertEqual(c.parse_test_count("Ran 0 tests in 0.01s\nRan 42 tests in 0.2s"), 0)

    def test_disallowed_git_push_never_runs(self):
        self.manifest["checks"][0]["argv"] = ["git", "push", "origin", "main"]
        errors, receipts = c.run_checks(self.repo, self.h, self.manifest)
        self.assertTrue(any("forbidden" in x for x in errors))
        self.assertEqual(receipts[0]["error"], "command forbidden")

    def test_disallowed_shell_wrapper_never_runs(self):
        self.manifest["checks"][0]["argv"] = ["bash", "-c", "echo okay"]
        errors, _ = c.run_checks(self.repo, self.h, self.manifest)
        self.assertTrue(any("forbidden" in x for x in errors))

    def test_check_runner_rejects_zero_test_output(self):
        self.manifest["review_tier"] = self.h["review_tier"] = "standard"
        self.manifest["checks"][0]["kind"] = self.h["verification"][0]["kind"] = "tests"
        self.manifest["checks"][0]["argv"] = [sys.executable, "-c", "print('Ran 0 tests in 0.01s')"]
        self.h["verification"][0]["command"] = c.shlex.join(self.manifest["checks"][0]["argv"])
        self.h["verification"][0]["tests_executed"] = 1
        errors, _ = c.run_checks(self.repo, self.h, self.manifest)
        self.assertTrue(any("nonzero test count" in x for x in errors))


class SchemaCompatibilityTests(unittest.TestCase):
    def test_schemas_valid_2020_12(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("optional jsonschema metavalidation is unavailable")
        for path in (c.REQUIRED_HANDOFF, c.REQUIRED_MANIFEST):
            Draft202012Validator.check_schema(c.read_json(path))

    def test_validator_matches_jsonschema_for_valid_and_invalid(self):
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("optional jsonschema parity test unavailable")
        for path in (c.REQUIRED_HANDOFF, c.REQUIRED_MANIFEST):
            schema = c.read_json(path)
            for value in ({}, [], {"protocol_version": "1.0"}):
                self.assertEqual(bool(c.shape_validate(value, schema)), not Draft202012Validator(schema).is_valid(value))

    def test_metrics_record_and_summary(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "metrics.jsonl"
            event = {"task_id": "T1", "workflow": "claude_codex", "elapsed_minutes": 35, "review_rounds": 2,
                     "confirmed_findings": 3, "false_alarms": 1, "independent_defects": 2, "escaped_defects": 0, "recurrences": 0}
            c.metrics_record(ledger, event)
            report = c.metrics_summary(ledger)["claude_codex"]
            self.assertEqual(report["review_precision"], 0.75)
            self.assertEqual(report["mean_elapsed_minutes"], 35)


if __name__ == "__main__":
    unittest.main()
