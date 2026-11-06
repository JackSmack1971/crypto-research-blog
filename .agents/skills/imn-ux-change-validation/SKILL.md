---
name: imn-ux-change-validation
description: Implement and validate an approved Independent Market Notes UX or accessibility slice while preserving article composition and site behavior. Use after design approval; excludes unapproved redesign decisions and general regression ownership.
metadata:
  short-description: Validate approved UX slices
---

# Independent Market Notes UX change validation

Use for one bounded UX or accessibility slice whose intended outcome and approval state are established. Approval may be explicit in the user's request or recorded in an applicable design/EGM artifact; verify the source of approval and translate it into observable acceptance criteria before implementation. Read applicable instructions, `README.md`, relevant artifacts, and actual source. If a material product or editorial decision is unresolved, continue independent investigation but do not make that decision through implementation.

## Preserve design and editorial intent

- Treat approved contrast, interaction, and content-composition decisions as constraints; verify the relevant decision artifact instead of relying on a summary.
- Preserve each essay's individual typography, charts, tables, and layout. Shared tokens or wrappers may be changed only within the approved slice.
- Keep article links available in initial HTML if JavaScript is unavailable. Preserve keyboard access, visible focus, semantic structure, and responsive behavior.
- Do not select or ship a related-note ranking policy based on implementation convenience. For that work, use the content-discovery dry-run and wait for review of its candidate results and policy.

## Validate the slice

Define observable acceptance checks from the approved design and record the relevant route, interaction, or article structure for each check. Inspect affected routes at relevant viewports and representative article structures. Run required Python checks for touched surfaces. When browser tooling is already available and the task includes visual/accessibility review, inspect functional behavior, keyboard flow, overflow, accessibility output, and expected/actual/diff screenshots. Playwright is optional local evidence in this repository, not publication CI; do not install or repair it for routine validation.

Classify failures as behavioral, accessibility, intended visual change, accidental visual regression, or environment-specific rendering only when evidence supports that classification. Refresh only reviewed screenshot targets after confirming intended differences; never weaken thresholds or hide findings with exceptions. Report checks and any human review still needed. This skill does not authorize deployment.
