---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder (NOW Builder persona for Build B) · Owner (briefed) · QC stream · Game/Teaching builders (informational)
re: PR #35 (Build A) merging after dual-pipeline APPROVE-WITH-NITS verdict (QC + V3-compliance both clean); PRE-DISPATCH row #5 transitions RED → GREEN; Build B kickoff directive issued
status: MERGE ACK + BUILD B DIRECTIVE — Build A artifact ships clean; PRE-DISPATCH gate one row down (3 RED remaining); Build B begins now per directive 3f9564e serial sequence
---

# PR #35 Merge ACK + Build B Kickoff

## Dual-pipeline verdict — APPROVE clean

| Pipeline | Verdict | Findings |
|----------|---------|----------|
| QC pre-merge audit (PR #36) | APPROVE-WITH-NITS | 8 V-A vectors PASS; 2 frontmatter NITs (line-range + rule-count shorthand) |
| V3-compliance content reviewer (orchestrator-dispatched) | APPROVE-WITH-NITS | Byte-perfect verbatim diff on §Buckets/§Features/§DO NOT Rules; feature names match `feature_extractor.py` at master HEAD; 59-feature contract verified |

**Convergent verdict.** Both pipelines independently confirm:
- Verbatim-inlined content is byte-perfect against v3.1 source line ranges
- Feature contract (59 raw) matches Stage 5 retrain v1.0.1 §Hyperparameters
- No spec-vs-code drift (the existence-drift class that fired twice
  earlier today on calibration_exam.py + missing pilot artifacts)
- NITs are frontmatter shorthand explained inline at artifact lines
  605-609 — not actually drift

## Merge decision

**MERGE PR #35 AS-IS.** NITs are not gating per:
- `feedback_quality_default_no_ask.md` — quality default doesn't mean
  fix every cosmetic issue; it means pick the clean path. The clean
  path here is merge + queue NIT housekeeping (if anyone cares) for
  v1.1 sweep
- Both reviewers explicitly recommend merge
- NITs are explained inline in the artifact body (not silent drift)

**Post-merge state:**
- Master advances 56a738a → <merge SHA>
- PRE-DISPATCH PREREQUISITES gate: row #5 transitions RED → GREEN
- Remaining RED rows: #2/#3 (corpus) + #6 (Protocol C `_pilot.md`)
- 3 RED rows remain; ~1.5-3h to clear

## Build B kickoff (immediate, per serial directive)

Per directive `3f9564e` serial sequence (A → B → C):

**Logic builder → pick up Build B per existing directive.** Same
pattern as Build A:

- **Source:** `prompts/protocol_c_adversarial_elimination_v1_0.md`
  (82255 bytes; design artifact at master HEAD)
- **Target:** `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`
- **Branch:** `stage4-pre-dispatch/protocol-c-pilot-build`
- **Method:** verbatim-inline §Buckets (v3.1 lines 170-204) + §Features
  (v3.1 lines 439-496 + 4 v2.4 P1 blockers + board_adjusted_hrp = 59
  raw) + §DO NOT Rules (v3.1 lines 590-647) — same recipe as Build A
- **Frontmatter:** version `v1.0.x` → `v1.0.x-pilot`;
  `artifact_class: PILOT-RUNTIME`; `build_provenance` block
- **Self-test before PR:** zero "see source artifact" / "see canonical"
  / "copy verbatim" / "design artifact" / "(or equivalent labeller-
  facing artifact)" markers in the build-output document

**Workflow:** PR + reviewer cycle. Same dual-pipeline pattern:
- QC will dispatch their pre-merge audit (TC-23 + V-A vectors); they
  have V-B1...V-B3 pre-emptive scoping ready per their tick 30+
  publication
- I'll dispatch V3-compliance reviewer in parallel
- Merge after both clear

**Estimated effort:** ~30-45 min (Build A took ~30 min from
directive); pattern is now established, second pass should be slightly
faster.

## Frontmatter NIT cleanup (optional housekeeping)

If you want to fold the 2 NITs into the next build (Build B same
pattern would inherit them otherwise), edit your Build B frontmatter
to:
- Use consistent line range (590-647 OR 595-647 — pick one)
- Use rule count format `(Rules 1-10; v1.0.1 design summary 11
  subsumed into Rule 10 verbatim)` — explicit not abbreviated

This avoids NIT carryover in Build B. But it's optional; the Build B
review will flag the same NITs if they recur, and you can address
them in the same v1.1 housekeeping sweep.

## Cross-stream

- **QC stream:** Continuing Layer 1+2 audit mode for Build B PR drop;
  V-B1...V-B3 vectors pre-scoped; standing by
- **Teaching builder:** C5.2 fixture swap continues independently
- **Game builder:** multiway playtest continues per your timing

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 35 | Build A — Protocol B labeller-facing pilot artifact | ✅ SEALED — PR #35 merging | Logic builder |
| 36 | Build B — Protocol C labeller-facing pilot artifact | 🔥 ACTIVE — directive issued | Logic builder |
| 37 | Build C — Pilot 100-hand stratified corpus | 🔥 QUEUED — after Build B | Logic builder |
| 39 | NIT cleanup carry-forward (Build B pre-empt OR v1.1 sweep) | ⏳ DEFERRED — NIT-class | TBD |

## References

- PR #35: `https://github.com/beytell1-sketch/river-rats-v2/pull/35`
- QC PR #36 audit (Path B bundled in this commit):
  `review/comms/QC_PRE_MERGE_AUDIT_PR35_2026-04-26.md`
- V3-compliance reviewer verdict:
  `review/comms/REVIEWER_V3_COMPLIANCE_PR35_2026-04-26.md`
- Builds A/B/C directive: `3f9564e`
  (`MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md`)
- Pilot orchestration spec v1.0.3: `c4f29a5`
  (`STAGE4_PILOT_ORCHESTRATION_v1_0.md`)
- Source design artifacts at master HEAD `c4f29a5`:
  - `prompts/gto_labeller_v3.1.md` (canonical Buckets/Features/DO NOT Rules)
  - `prompts/protocol_c_adversarial_elimination_v1_0.md` (Build B source)
- Feature contract source: `river-rats-core/feature_extractor.py` at
  `c4f29a5`; `FEATURE_COLUMNS` length 59

## Action

**Logic builder:**
1. Build A SEALED — proceed to Build B per directive `3f9564e`
2. Same recipe as Build A (verbatim-inline same 3 sections + frontmatter pattern)
3. Branch: `stage4-pre-dispatch/protocol-c-pilot-build`
4. PR + dual-pipeline review + merge
5. After Build B sealed → Build C (corpus stratification)

**Orchestrator (me):**
1. PR #35 merge + close PR #36 + this ack shipped (this commit)
2. Watch for Build B PR drop (~30-45 min ETA)
3. Dispatch V3-compliance reviewer when Build B PR opens
4. /loop continues at 10-min cadence during active build phase

**QC stream:**
- Continue Layer 1+2 audit mode for Build B PR
- V-B1...V-B3 vectors pre-scoped; deploy at PR drop
- Same Path B bundle pattern after audit ships

**Owner:**
- Build A SHIPPED clean (dual-reviewer convergent APPROVE)
- 3 of 4 RED rows remain; ~1.5-3h to clear PRE-DISPATCH gate
- After all 3 builds seal: pilot dispatch resumes (Phase A.1-A7)

**Status: PR #35 MERGING. PRE-DISPATCH row #5 GREEN. Build B begins
NOW per serial directive. Build A→B→C cleanup pace healthy.**
