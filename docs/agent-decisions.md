# Collaboration Decisions

Only durable, cross-session governance decisions belong here. This document records a proposed collaboration setup packaged for human adoption; its presence does not prove that the live repository has accepted or deployed it.

| ID | Date | Decision | Rationale | Owner / adoption status | Supersedes |
| --- | --- | --- | --- | --- | --- |
| COLLAB-001 | 2026-11-05 | Keep the shared collaboration interface at `docs/agent-collaboration.md` in the Codex repository; distribute the Claude navigator `CLAUDE.md` separately. | Repo-versioned protocol stays with validation contracts, while navigator instructions cannot unintentionally change Codex's implementation role. | Human operator / proposed package, pending repository adoption | None |
| COLLAB-002 | 2026-11-05 | Require an evidence-bearing JSON handoff plus a human-readable summary for navigator reviews; no report grants additional permissions. | Traceable claims and stable finding IDs support independent review without elevating model output to authority. | Human operator / proposed package, pending repository adoption | None |

| COLLAB-003 | 2026-11-05 | Require operator-controlled v1.1 task manifest and independently executed semantic/Git/check gate; old v1.0 handoffs require deliberate migration. | Separates claims from observed technical evidence and prevents contradictory success reports. No agent-supplied report is an approval. | Human operator / proposed package, pending repository adoption | None |
| COLLAB-004 | 2026-11-05 | Introduce lightweight, standard, and enhanced review levels and a minimum tier for sensitive paths. | Match review effort to change risk without silently relaxing validation. | Human operator / proposed package, pending repository adoption | None |
| COLLAB-005 | 2026-11-05 | Collect outcome measures outside the worktree for matched Codex-only vs Claude–Codex tasks. | Determine whether independent review reduces escaped defects rather than merely increasing overhead. | Human operator / proposed package, pending repository adoption | None |
| COLLAB-006 | 2026-11-05 | Align routine publication gates to `build` plus `content-check`, excluding retired Chromium/Playwright and `styling-check` dependencies. | Avoid reintroducing obsolete tooling into publication. Requires revalidation against live CI upon adoption. | Human operator / proposed package, pending repository adoption | None |

For a new decision add: stable ID, date, concise outcome, options considered if material, scope and practical consequences, owner and approval evidence, and a supersession reference if it replaces a previous decision. Don't mark a decision as approved without observed approval.
