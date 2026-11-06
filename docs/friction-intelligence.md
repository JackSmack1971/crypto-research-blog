# Local friction intelligence — operating contract

This is an **opt-in, local-only** development learning subsystem. The Python stdlib collector `tools/friction.py` stores sanitized incidents in `~/.codex/friction-intelligence/incidents.sqlite3` by default (Windows: the current user's home directory). It has no shell interception, telemetry subscriptions, background service, or model-initiated automatic writes to `AGENTS.md`. It makes no claim that Codex emits all shell/tool events or dynamically reloads changed instructions. Validate any future hook integration against the installed CLI, environment, and hook failure behavior.

## Commands

Run from repo root, with `python` in place of `python3` where that is the active verified interpreter:

```sh
python3 tools/friction.py record --category shell --fingerprint powershell-unix-ls --platform windows-powershell --tool pwsh --synopsis "Unix listing flags were rejected by the active shell" --recovery "Get-ChildItem -Force succeeded" --evidence observed-tool-result --state resolved --session task-opaque-001
python3 tools/friction.py clusters --min-count 2
python3 tools/friction.py list --limit 20
```

For isolated testing, supply `--db /path/to/temporary.sqlite3` **before** the subcommand. This is an explicit override; the default is not inside the repository. Use separate database files for separate machines if desired. Do not commit, export or sync incident data without an explicit additional decision.

## Event semantics

Each event has a timestamp, controlled category, stable human-selected fingerprint, platform, tool, sanitized synopsis, optional verified recovery, evidence source, observed/reproduced/resolved state, and optional opaque session reference. Cluster grouping is based on category + fingerprint + platform + tool; counts and session references support triage, **not automatic root-cause identification**. Do not manufacture session IDs or treat `unknown` as a distinct-session guarantee.

The tool rejects some obvious secret formats, line breaks, and overlong strings. **This is not a comprehensive DLP control.** Never supply raw stderr/stdout, shell arguments, file contents, paths with personal details, URLs containing credentials, prompts, tokens or secrets. Inspect sanitized submissions before recording. Host filesystem ACLs and backups remain the operator's responsibility. SQLite creates companion `-wal`/`-shm` files as needed. Local records are user-modifiable and are not authoritative independent audit evidence. Purging/retention and portability should be established by the operator before using this for sensitive workflows.

## Promotion gate

A durable change follows: observed → grouped → reproduced → remedy proposed → targeted regression tested → independent review → operator-approved change → measured follow-up or rollback. Unverified diagnoses stay in local evidence; do not turn them into global rules. Prefer mechanical/environment fixes over instruction accretion. Retain original instruction text and report the exact diff when proposing edits. Never weaken execution approval, sandbox, Git restrictions, CI, or protected publishing boundaries as a friction workaround.

Recording must be best-effort and must not delay a time-critical primary task. The collector's output is ordinary JSON and has no authorization status. `AGENTS.md`, skills, tools, and observed logging do not grant access to new systems or allow bypassing denied operations.

## Boundaries and limitations

- This document and tools/friction.py are a local, opt-in control-plane subset; they are not part of the site build, and nothing in build.py, CI or deployment depends on them.
- Existing CI/publishing remains unchanged. Nothing is wired into GitHub Actions or Netlify.
- A user can inspect the local ledger; other agents read it only by intentionally invoking the tool in an authorized environment.
- There is no automatic suggestion writer, remediation executor, host-wide collector, policy compiler, or reliable live-refresh contract.
- Future automation should add source/version-pinned conformance tests, complete capture-coverage reporting, bounded retention, access controls, redaction validation, and a separate review gate before enabling collection hooks.
