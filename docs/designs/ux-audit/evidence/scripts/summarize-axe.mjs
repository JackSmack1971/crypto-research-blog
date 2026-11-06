import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
const dir = path.resolve("docs/designs/ux-audit/evidence/axe");
const files = readdirSync(dir).filter((name) => name.endsWith(".json") && name !== "_run-index.json");
const data = files.map((file) => ({ file, json: JSON.parse(readFileSync(path.join(dir, file), "utf8")) }));
const impacts = ["critical", "serious", "moderate", "minor", "unknown"];
const counts = Object.fromEntries(impacts.map((impact) => [impact, 0]));
const lines = [
  "# Axe accessibility results",
  "",
  "Axe ran with WCAG 2.0/2.1 A and AA tags using the installed `@axe-core/playwright`, against local `dist/` served at `127.0.0.1:4173`. Each JSON file contains the raw axe result for that scenario and viewport.",
  "",
  "## Violation summary by impact",
  "",
  "| Impact | Rule occurrences |",
  "| --- | ---: |",
];
for (const impact of impacts) {
  const count = data.reduce((sum, { json }) => sum + json.violations.filter((v) => (v.impact ?? "unknown") === impact).length, 0);
  counts[impact] = count;
  lines.push(`| ${impact} | ${count} |`);
}
lines.push("", "## All violations", "", "| Scenario | Viewport | Impact | Rule | Affected nodes | Help |", "| --- | ---: | --- | --- | ---: | --- |");
let found = 0;
for (const { file, json } of data) {
  for (const violation of json.violations) {
    found += 1;
    lines.push(`| ${json.scenario} | ${json.viewport.width}px | ${violation.impact ?? "unknown"} | ${violation.id} | ${violation.nodes.length} | ${violation.help.replaceAll("|", "\\|")} ([raw](axe/${file})) |`);
  }
}
if (!found) lines.push("| None | — | — | — | — | No violations detected. |", "| — | — | critical | 0 | — | — |", "| — | — | serious | 0 | — | — |", "| — | — | moderate | 0 | — | — |", "| — | — | minor | 0 | — | — |");
lines.push("", `Scenarios scanned: ${data.length}. This is an automated WCAG rule scan, not a full accessibility conformance assessment.`, "");
writeFileSync(path.resolve("docs/designs/ux-audit/evidence/axe-summary.md"), lines.join("\n"));
console.log(JSON.stringify({ files: data.length, counts, violations: found }));
