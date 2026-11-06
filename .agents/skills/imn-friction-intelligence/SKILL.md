---
name: imn-friction-intelligence
description: Record and analyze recurring local Codex shell, tooling, environment, and development workflow friction; use when avoidable retries recur or when reviewing local friction evidence. Does not automatically edit policy.
metadata:
  short-description: Local friction evidence and remediation
---

# Local friction intelligence (opt-in)

Read `docs/friction-intelligence.md` before using the collector. This Skill describes a procedure; it does not authorize file, environment, or policy changes.

1. Distinguish actual operational friction from expected failing tests, exploratory commands, product defects, and denied operations. Never treat a denial as a signal to bypass authorization.
2. For material avoidable friction, record a **sanitized, non-secret, single-line summary** using `python3 tools/friction.py record` with category, stable fingerprint, platform, tool, and synopsis. Optional `--recovery` is allowed only when verified. Do not input raw logs, full commands with arguments, prompts, environment dumps, user content, or credentials.
3. The database defaults to the user's home directory under `.codex/friction-intelligence/`, outside the repository. If unavailable, continue the primary task; disclose the logging gap rather than writing an unapproved fallback inside the repository.
4. Review `python3 tools/friction.py clusters --min-count 2` for recurring patterns. A count is not causal proof; sessions with unknown identity are not evidence of distinct tasks. Investigate reproducibility and platform/tool version drift before claiming a root cause.
5. Propose the smallest remedy in this order when applicable: environment repair; executable script/validator; narrowly scoped Skill; finally concise `AGENTS.md` guidance. For machine-specific issues keep local notes rather than altering portable repo policy.
6. Record the proposed change, reproducer, expected result, regression risks, and rollback in the task handoff. Require independent verification and operator authorization before modifying AGENTS.md, Skills, runtime config, security settings, or shared scripts.
7. Evaluate comparable tasks before and after adoption. Report failed attempts per task, repeated clusters, collector coverage, and false-positive rate; separate environment/model/version changes. Do not equate fewer errors with causal improvement without a controlled comparison.

**No automatic hooks, global interception, or instruction self-modification are installed by this Skill.** A collector records only incidents explicitly submitted by authorized agents/operators; missing records do not mean no failures occurred.
