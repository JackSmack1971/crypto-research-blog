"""Isolated stdlib-only checks for the optional local friction collector."""
import importlib.util
import io
import json
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
import tempfile
import unittest
from unittest import mock

MODULE = Path(__file__).resolve().parents[1] / 'tools' / 'friction.py'
spec = importlib.util.spec_from_file_location('friction', MODULE)
friction = importlib.util.module_from_spec(spec)
spec.loader.exec_module(friction)


class FrictionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = str(Path(self.temp.name) / 'private' / 'friction.sqlite3')

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                status = friction.main(['--db', self.db, *args])
            except SystemExit as exc:
                status = int(exc.code)
        return status, json.loads(out.getvalue()) if out.getvalue() else None, err.getvalue()

    def record(self, session='s1', fingerprint='shell-mismatch'):
        return self.run_cli('record', '--category', 'shell', '--fingerprint', fingerprint,
                            '--platform', 'windows-powershell', '--tool', 'pwsh',
                            '--synopsis', 'Unix-only argument rejected', '--recovery',
                            'PowerShell equivalent verified', '--session', session)

    def test_persist_cluster_and_list(self):
        self.assertEqual(self.record('s1')[0], 0)
        self.assertEqual(self.record('s2')[0], 0)
        code, rows, _ = self.run_cli('clusters', '--min-count', '2')
        self.assertEqual(code, 0)
        self.assertEqual(rows[0]['count'], 2)
        self.assertEqual(rows[0]['distinct_session_refs'], 2)
        self.assertEqual(rows[0]['review_status'], 'candidate_only')
        self.assertEqual(self.run_cli('list', '--limit', '1')[1][0]['id'], 2)

    def test_no_leakage_of_raw_or_multiline_or_secret(self):
        for value in ('abc\nInjected', 'token=not-for-storage', 'sk-' + 'z'*25):
            code, _, _ = self.run_cli('record', '--category', 'syntax', '--fingerprint', 'safe-id',
                    '--platform', 'win', '--tool', 'git', '--synopsis', value)
            self.assertEqual(code, 2)
        self.assertEqual(self.run_cli('list')[1], [])

    def test_distinct_platform_and_fingerprint(self):
        self.record('s1')
        self.record('s1', 'other-syntax')
        self.assertEqual(len(self.run_cli('clusters', '--min-count', '2')[1]), 0)
        rows = self.run_cli('clusters', '--min-count', '1')[1]
        self.assertEqual(len(rows), 2)

    def test_reject_unbounded_query(self):
        self.assertEqual(self.run_cli('list', '--limit', '201')[0], 2)
        self.assertEqual(self.run_cli('clusters', '--min-count', '0')[0], 2)

    def test_db_outside_repository_when_no_override(self):
        with mock.patch.object(friction.Path, 'home', return_value=Path(self.temp.name)):
            p = friction.db_path(None)
        self.assertEqual(p, Path(self.temp.name, '.codex', 'friction-intelligence', 'incidents.sqlite3'))


if __name__ == '__main__':
    unittest.main()
