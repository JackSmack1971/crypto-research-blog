---
name: imn-dual-host-release
description: Qualify an explicitly authorized Independent Market Notes release and verify GitHub Pages and Netlify independently. Use for requested push, release, deployment verification, or diagnosis; excludes article authoring and UX design.
metadata:
  short-description: Verify both publication hosts
---

# Independent Market Notes dual-host release

Use when the user explicitly requests a release-related remote operation or asks to verify/diagnose an existing release. Read-only diagnosis needs no release action; a commit, push, merge, publish, production configuration change, or retry of a failed write requires explicit authorization for that action. This skill does not itself grant that authority.

## Establish the release state

Read current `README.md`, `AGENTS.md`, `.github/workflows/pages.yml`, `netlify.toml`, `site.json`, and Git state. Confirm target commit, branch, and exact authorized operation; for diagnosis, identify the commit being diagnosed. Run the locally required build and Python checks before an authorized push. A local build, GitHub check, push, and host deployment are separate states.

Track the two hosts independently:

| Host | Evidence to read back |
| --- | --- |
| GitHub Pages | Actions run for the exact commit; build and content-check results; deploy job result and deployed URL/commit where available |
| Netlify | Deploy record for the exact commit; build result; published URL and deploy state |

Then verify representative live routes, assets, and canonical/social metadata at each configured origin. GitHub Pages uses a project subpath; Netlify is the canonical origin. Do not infer one host's state from the other's result or from CI alone.

## Recovery and handoff

For interrupted or failed operations, read remote state before retrying to avoid duplicate or conflicting writes. If a host's status is pending or unavailable, report it as pending or unknown, with the evidence checked; do not call it published. Stop if branch, commit, permissions, or remote state contradict the request. Report each host as deployed, failed, pending, unknown, or not requested, and distinguish observed facts from inference.
