#!/usr/bin/env python3
"""Local-only, opt-in operational-friction ledger. No Codex private API required.

Never accepts raw stderr, stdout, prompts, environment dumps, or shell arguments.
The human/agent supplies a short non-sensitive synopsis instead.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import sys

CATEGORIES = ('shell', 'syntax', 'environment', 'dependency', 'testing', 'tool-discovery', 'git', 'orchestration', 'workflow')
STATES = ('observed', 'reproduced', 'resolved')
SCHEMA = '''
CREATE TABLE IF NOT EXISTS incidents (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 created_utc TEXT NOT NULL,
 category TEXT NOT NULL,
 fingerprint TEXT NOT NULL,
 platform TEXT NOT NULL,
 tool TEXT NOT NULL,
 synopsis TEXT NOT NULL,
 recovery TEXT NOT NULL,
 evidence_kind TEXT NOT NULL,
 state TEXT NOT NULL,
 session_ref TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS incidents_fingerprint ON incidents(fingerprint);
'''
# This is a defense-in-depth check, not a guarantee that supplied text contains no secrets.
SUSPECT = re.compile(r'(?i)(sk-[a-z0-9_-]{12,}|gh[pousr]_[a-z0-9_]{12,}|-----BEGIN [A-Z ]*PRIVATE KEY|(?:password|secret|token|api[_-]?key)\s*[:=]\s*\S+|https?://[^\s/@]+:[^\s/@]+@)')
SAFE_ID = re.compile(r'^[a-zA-Z0-9_.-]{1,64}$')


def short_text(value, field, maxlen=240):
    if not isinstance(value, str) or not value.strip() or len(value) > maxlen or '\n' in value or '\r' in value or '\x00' in value:
        raise ValueError(f'{field} must be a nonempty single line (at most {maxlen} characters)')
    if SUSPECT.search(value):
        raise ValueError(f'{field} resembles sensitive material; use a sanitized summary')
    return value.strip()


def db_path(raw):
    if raw:
        candidate = Path(raw).expanduser().resolve()
    else:
        candidate = (Path.home() / '.codex' / 'friction-intelligence' / 'incidents.sqlite3').resolve()
    # Prevent accidentally writing to repository by default; explicit override is intentional.
    return candidate


def connect(path):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not path.exists():
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(fd)
    db = sqlite3.connect(path, timeout=10)
    try:
        db.execute('PRAGMA busy_timeout=10000')
        db.execute('PRAGMA journal_mode=WAL')
        db.executescript(SCHEMA)
    except BaseException:
        db.close()
        raise
    return db


def record(db, args):
    category = args.category
    tool = short_text(args.tool, 'tool', 64)
    platform = short_text(args.platform, 'platform', 64)
    fingerprint = short_text(args.fingerprint, 'fingerprint', 100).lower()
    if not re.fullmatch(r'[a-z0-9][a-z0-9._-]*', fingerprint):
        raise ValueError('fingerprint must be a stable non-sensitive slug')
    synopsis = short_text(args.synopsis, 'synopsis')
    recovery = short_text(args.recovery, 'recovery') if args.recovery else ''
    session = args.session or 'unknown'
    if not SAFE_ID.fullmatch(session):
        raise ValueError('session must be a non-sensitive opaque identifier')
    with db:
        cursor = db.execute('''INSERT INTO incidents
        (created_utc,category,fingerprint,platform,tool,synopsis,recovery,evidence_kind,state,session_ref)
        VALUES (?,?,?,?,?,?,?,?,?,?)''', (datetime.now(timezone.utc).isoformat(), category, fingerprint, platform, tool, synopsis,
            recovery, args.evidence, args.state, session))
    return {'id': cursor.lastrowid, 'status': 'recorded'}


def clusters(db, minimum):
    rows = db.execute('''SELECT category,fingerprint,platform,tool,COUNT(*) AS count,
    COUNT(DISTINCT session_ref) AS sessions,MAX(created_utc) AS latest,
    SUM(CASE WHEN state='reproduced' THEN 1 ELSE 0 END) AS reproduced
    FROM incidents GROUP BY category,fingerprint,platform,tool
    HAVING COUNT(*)>=? ORDER BY count DESC,latest DESC''', (minimum,)).fetchall()
    return [{'category':r[0], 'fingerprint':r[1], 'platform':r[2], 'tool':r[3],
             'count':r[4], 'distinct_session_refs':r[5], 'last_seen_utc':r[6], 'reproduced_count':r[7],
             'review_status':'candidate_only'} for r in rows]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--db', help='Explicit local SQLite path (default: ~/.codex/friction-intelligence/incidents.sqlite3)')
    sub = parser.add_subparsers(dest='command', required=True)
    r = sub.add_parser('record', help='Manually record sanitized evidence; no shell history scraping')
    r.add_argument('--category', choices=CATEGORIES, required=True)
    r.add_argument('--fingerprint', required=True, help='Stable normalized error identifier, not raw error output')
    r.add_argument('--platform', required=True, help='Example: windows-powershell, linux-bash')
    r.add_argument('--tool', required=True, help='Example: git, python, pwsh')
    r.add_argument('--synopsis', required=True, help='Short sanitized observation')
    r.add_argument('--recovery', default='', help='Verified recovery, if any')
    r.add_argument('--evidence', choices=('observed-tool-result', 'manual-report', 'reproduction'), default='manual-report')
    r.add_argument('--state', choices=STATES, default='observed')
    r.add_argument('--session', default='unknown', help='Opaque non-sensitive session reference')
    c = sub.add_parser('clusters', help='Return deduplicated incident counts; not root-cause proof')
    c.add_argument('--min-count', type=int, default=2)
    l = sub.add_parser('list', help='List recent sanitized incident records')
    l.add_argument('--limit', type=int, default=20)
    args = parser.parse_args(argv)
    if args.command == 'clusters' and not 1 <= args.min_count <= 100000:
        parser.error('--min-count must be between 1 and 100000')
    if args.command == 'list' and not 1 <= args.limit <= 200:
        parser.error('--limit must be between 1 and 200')
    try:
        db = connect(db_path(args.db))
        try:
            with db:
                if args.command == 'record': result = record(db,args)
                elif args.command == 'clusters': result = clusters(db,args.min_count)
                else:
                    db.row_factory = sqlite3.Row
                    result = [dict(row) for row in db.execute('SELECT * FROM incidents ORDER BY id DESC LIMIT ?', (args.limit,))]
        finally:
            db.close()
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, sqlite3.Error, ValueError) as exc:
        print(f'friction collector: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
