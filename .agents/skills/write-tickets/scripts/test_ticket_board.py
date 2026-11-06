"""Offline invariants for ticket_board. Run: python -m unittest discover -s scripts -p 'test_*.py'."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import ticket_board as tb


def make_entry(ticket_id, **overrides):
    entry = {
        "id": ticket_id,
        "title": ticket_id.replace('-', ' ').title(),
        "status": "draft",
        "depends_on": [],
        "resources": [],
        "parallel_safe": False,
        "blocker": None,
        "open_decisions": [],
        "approval": None,
    }
    entry.update(overrides)
    return entry


class BoardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "tickets"
        self.root.mkdir()
        self.entries = [make_entry("001-login")]
        self.save()

    def save(self):
        for entry in self.entries:
            ticket = self.root / entry["id"]
            ticket.mkdir(exist_ok=True)
            rd = ticket / "rd.md"
            ev = ticket / "eval.md"
            if not rd.exists():
                rd.write_text(f"# Login\n\n**Ticket:** {entry['id']}\n\n- **R-01**: Login returns a session.\n", encoding="utf-8")
            if not ev.exists():
                ev.write_text(f"# Eval\n\n**Ticket:** {entry['id']}\n\n| Requirement | Setup | Action | Expected |\n|---|---|---|---|\n| R-01 | New user | Sign in | Session visible |\n", encoding="utf-8")
        (self.root / "board.json").write_text(json.dumps({"schema_version": 1, "tickets": self.entries}, indent=2), encoding="utf-8")

    def errors(self):
        return tb.check(self.root, tb.read_manifest(self.root))

    def approve(self, entry):
        entry["status"] = "ready"
        entry["approval"] = {"ref": "user approved reviewed ticket contents", "fingerprint": tb.fingerprint(entry, tb.get_documents(self.root, entry["id"]))}
        self.save()

    def test_draft_valid(self):
        self.assertEqual(self.errors(), [])

    def test_ready_with_matching_approval(self):
        self.approve(self.entries[0])
        self.assertEqual(self.errors(), [])

    def test_ready_without_approval_rejected(self):
        self.entries[0]["status"] = "ready"
        self.save()
        self.assertIn("requires approval", " ".join(self.errors()))

    def test_draft_cannot_keep_approval(self):
        self.entries[0]["approval"] = {"ref": "x", "fingerprint": "0" * 64}
        self.save()
        self.assertIn("draft must have approval null", " ".join(self.errors()))

    def test_missing_requirement_evaluation(self):
        (self.root / "001-login" / "rd.md").write_text("**Ticket:** 001-login\n- **R-01**: A\n- **R-02**: B\n", encoding="utf-8")
        self.assertIn("no eval.md row for R-02", " ".join(self.errors()))

    def test_duplicate_eval_row(self):
        path = self.root / "001-login" / "eval.md"
        path.write_text(path.read_text(encoding="utf-8") + "| R-01 | X | Y | Z |\n", encoding="utf-8")
        self.assertIn("duplicate requirement IDs in eval.md", " ".join(self.errors()))

    def test_invalid_eval_column_count(self):
        path = self.root / "001-login" / "eval.md"
        path.write_text("**Ticket:** 001-login\n| R-01 | setup | action |\n", encoding="utf-8")
        self.assertIn("four nonempty cells", " ".join(self.errors()))

    def test_missing_dependency(self):
        self.entries[0]["depends_on"] = ["999-missing"]
        self.save()
        self.assertIn("missing dependency", " ".join(self.errors()))

    def test_cycle(self):
        self.entries[0]["depends_on"] = ["002-dashboard"]
        self.entries.append(make_entry("002-dashboard", depends_on=["001-login"]))
        self.save()
        self.assertIn("Dependency cycle", " ".join(self.errors()))

    def test_stale_document_approval(self):
        self.approve(self.entries[0])
        with (self.root / "001-login" / "rd.md").open("a", encoding="utf-8") as handle:
            handle.write("\nExtra behavior.\n")
        self.assertIn("approval fingerprint stale", " ".join(self.errors()))

    def test_stale_metadata_approval(self):
        self.approve(self.entries[0])
        self.entries[0]["title"] = "Changed title"
        self.save()
        self.assertIn("approval fingerprint stale", " ".join(self.errors()))

    def test_unresolved_decisions_block_ready(self):
        self.entries[0]["open_decisions"] = ["Choose data retention rule"]
        self.save()
        self.approve(self.entries[0])
        self.assertIn("unresolved open_decisions", " ".join(self.errors()))

    def test_parallel_group_disjoint_and_serial(self):
        a = make_entry("001-one", status="ready", parallel_safe=True, resources=["feature-a"])
        b = make_entry("002-two", status="ready", parallel_safe=True, resources=["feature-b"])
        c = make_entry("003-three", status="ready", parallel_safe=False, resources=[])
        d = make_entry("004-four", status="ready", parallel_safe=True, resources=["feature-a"])
        batches = tb.candidate_batches([a, b, c, d])
        self.assertEqual([[e["id"] for e in group] for group in batches], [["001-one", "002-two"], ["003-three"], ["004-four"]])

    def test_shared_resources_force_separate_batches(self):
        a = make_entry("001-one", parallel_safe=True, resources=["db"])
        b = make_entry("002-two", parallel_safe=True, resources=["db"])
        self.assertEqual(len(tb.candidate_batches([a, b])), 2)

    def test_concurrent_path_overlap_and_casefold(self):
        a = make_entry("001-one", parallel_safe=True, resources=["src/Components"])
        b = make_entry("002-two", parallel_safe=True, resources=["src/components/Nav.tsx"])
        self.assertEqual(len(tb.candidate_batches([a, b])), 2)

    def test_dependency_waiting_even_with_approval(self):
        second = make_entry("002-dashboard", depends_on=["001-login"])
        self.entries.append(second)
        self.save()
        self.approve(second)
        self.approve(self.entries[0])
        body = tb.render_body({"schema_version": 1, "tickets": self.entries})
        self.assertIn("unfinished dependencies: 001-login", body)
        self.assertIn("Layer 2: `002-dashboard`", body)

    def test_board_generate_verify_and_reject_tampering(self):
        data = tb.read_manifest(self.root)
        board = tb.rendered_board(data)
        tb.write_board(self.root, board)
        self.assertTrue(tb.is_intact_generated_board((self.root / "BOARD.md").read_text(encoding="utf-8")))
        self.assertEqual((self.root / "BOARD.md").read_text(encoding="utf-8"), board)
        path = self.root / "BOARD.md"
        path.write_text(path.read_text(encoding="utf-8") + "manual addition", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "modified"):
            tb.write_board(self.root, board)

    def test_refuse_overwrite_custom_board(self):
        path = self.root / "BOARD.md"
        path.write_text("# My own board\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unrecognized"):
            tb.write_board(self.root, tb.rendered_board(tb.read_manifest(self.root)))
        self.assertEqual(path.read_text(), "# My own board\n")

    def test_orphan_ticket_directory(self):
        (self.root / "002-orphan").mkdir()
        self.assertIn("Unlisted ticket directory", " ".join(self.errors()))

    def test_reject_mismatched_ticket_marker(self):
        path = self.root / "001-login" / "eval.md"
        path.write_text(path.read_text(encoding="utf-8").replace("001-login", "002-other"), encoding="utf-8")
        self.assertIn("must contain exactly one", " ".join(self.errors()))

    def test_duplicate_numeric_id(self):
        self.entries.append(make_entry("001-other"))
        self.save()
        self.assertIn("numeric prefix already used", " ".join(self.errors()))

    def test_parallel_flag_rejects_unassessed_resources(self):
        self.entries[0]["parallel_safe"] = True
        self.entries[0]["resources"] = ["unassessed"]
        self.save()
        self.assertIn("unresolved placeholders", " ".join(self.errors()))

    def test_parallel_flag_requires_resources(self):
        self.entries[0]["parallel_safe"] = True
        self.save()
        self.assertIn("nonempty shared-resource inventory", " ".join(self.errors()))

    def test_reject_symlink_document(self):
        doc = self.root / "001-login" / "rd.md"
        other = self.root / "other.txt"
        other.write_text("test", encoding="utf-8")
        doc.unlink()
        try:
            doc.symlink_to(other)
        except (OSError, NotImplementedError):
            self.skipTest("symlink support unavailable")
        self.assertIn("unsafe symlink", " ".join(self.errors()))

    def test_cli_validation_and_render_roundtrip(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tb.main(["validate", "--root", str(self.root)]), 0)
            self.assertEqual(tb.main(["render", "--root", str(self.root), "--write"]), 0)
            self.assertEqual(tb.main(["validate", "--root", str(self.root), "--check-rendered"]), 0)
        self.entries.append(make_entry("002-dashboard"))
        self.save()
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(tb.main(["validate", "--root", str(self.root), "--check-rendered"]), 1)


if __name__ == "__main__":
    unittest.main()
