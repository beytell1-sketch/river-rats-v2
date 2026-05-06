---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #245 + PR #247 merged (QC PASS 0/0/0; 26th solo cycle; CONVERGENT + INDEPENDENT corroboration); MW-40 graduation-fail CONFIRMED via 4-source pattern symmetric to MW-25; dispatch 12.5I-MW40-VERIFICATION-E memo-only PR
status: DIRECTIVE — merges PR #245 + PR #247; fires LEAD-PROGRAMMER on -E memo-only PR (graduation-fail) — fire now
---

# PR #245 + PR #247 merge + 12.5I-MW40-VERIFICATION-E memo-only dispatch

QC verdict on PR #245 (`REVIEW_QC_PHASE125I_MW40_VERIFICATION_D_OPUS_TIERUP_2026-05-06.md` on `qc/pr245-mw40-verification-d-review-2026-05-06`, PR #247): **PASS — 0 BLOCKER, 0 SHOULD_FIX, 0 NIT (26th solo cycle).** Verdict tag: "CONVERGENT + INDEPENDENT corroboration." Opus 4.7 reasoning corroborates Sonnet's BET conclusion through BOTH the same protocol-rule chain (DO NOT Rule 11 OOP-only exemption + composition quad) AND independent v3.4 routing paths. **Strongest possible empirical signal short of solver-aligned ground truth.**

## MW-40 graduation-fail — 4-source pattern symmetric to MW-25

| Source | Result | Reference |
|---|---|---|
| 1. v3.4 production-prompt Sonnet pilot (5 hands × 5 labellers) | 25/25 BET at 1.00 confidence; CONVERGENT reasoning | PR #241 (master `d411cb8`) |
| 2. Opus 4.7 tier-up on the same 5 pilot hands | 5/5 BET; CONVERGENT + INDEPENDENT reasoning | PR #245 (this resolution) |
| 3. v3.4 protocol-rule chain (DO NOT Rule 11 OOP-only exemption + villain_checked_back weakness + composition quad villain_air_pct + danger_score=0 → value/protection BET routing) | Production-prompt deterministic routing | `prompts/gto_labeller_v3.4.md` |
| 4. PR #209 Opus 4.7 HIGH on PILOT_787 (the original CHECK signal) | Anomalous to broader pattern at parametric scale | `077c168` |

The 4-source convergence is unambiguous in the BET direction at the labelling-pipeline layer. PILOT_787's original CHECK was a **single-hand anomaly** that did NOT generalize to the broader J-on-board TPMK T-kicker 4-way checked-through IP non-PFA pattern. The structural argument ("J-on-board flips composition triple toward CHECK") is empirically TOO NARROW under the v3.4 production-prompt protocol routing.

## Decision 3β outcome — graduation-fail confirmed

Per `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217) Decision 3β:

> "If 30/30 (or ≥27/30) CHECK consensus → MW-40 graduates with the same evidence pattern as MW-25. If <27/30 → structural argument is too narrow; MW-40 stays wrong; PILOT_787 stays as a single anomaly."

**Outcome: 0/30 effective CHECK consensus** (5/30 sampled at pilot, all BET; remaining 25/30 not labelled because pilot HALT correctly fired). MW-40 stays in BATCH2 reference as **BET MEDIUM** (the original expert label; no graduation update). Stay-wrong list count remains 4 → 4: MW-17, MW-40, MW-45, MW-47.

## LEAD-PROGRAMMER — Step: 12.5I-MW40-VERIFICATION-E memo-only PR (fire on this comm merge)

Per dispatch `MAIN_TERMINAL_PR241_RESOLUTION_AND_MW40D_DISPATCH_2026-05-06.md` (master `966fcbd`, PR #244) §"Sequencing — what fires after -D merges" item 1 (default outcome path).

Branch: `programmer/phase125i-mw40-verification-e-memo-2026-05-06`. Base: master post-this-comm-merge.

### Scope — memo-only PR (graduation-fail documentation; NIT carry-forward)

Documentation PR. NO factory generation, NO labelling, NO model inference, NO model training. Updates 1 doc file + 1 memory file + (optionally) the BATCH2 RANGE_ANALYSIS.md for the documented-anomaly footnote on MW-40.

### Files to edit (3-4 expected)

1. **`review/RESTART_PROMPT_V9_3WAY.md`** (stay-wrong list update; mirror PR #218 BATCH2 graduation pattern but on the failing direction):
   - MW-40 entry remains in stay-wrong (no graduation).
   - Add annotation in MW-40's row: "Verification round complete 2026-05-06: PR #241 Sonnet pilot 25/25 BET + PR #245 Opus 4.7 tier-up 5/5 BET = graduation-fail. PILOT_787's CHECK is a single-hand anomaly relative to the broader J-on-board TPMK T-kicker 4-way checked-through IP non-PFA pattern. v3.4 DO NOT Rule 11 OOP-only exemption + composition quad routing dominates."
   - No other stay-wrong entries modified.

2. **`/home/rupertbeytell/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`** (memory file edit; mirrors PR #218 pattern but adds a "Verified Negative Result" section if no such structure exists):
   - Add new section "Verified Negative Reference Verifications" (if not present) or append to existing structure
   - Add MW-40 entry: "Verified 2026-05-06 via 12.5I-MW40-VERIFICATION (Decision 3β round): Original BATCH2 expert action BET MEDIUM stands. PILOT_787 (PR #213) suggested CHECK; broader 30-hand parametric verification pilot HALTed at 25/25 Sonnet BET (PR #241) + 5/5 Opus 4.7 BET (PR #245); graduation-fail confirmed via 4-source convergence symmetric to MW-25 graduation pattern. PILOT_787 is a single-hand anomaly. Stay-wrong list unchanged: 4 hands (MW-17, MW-40, MW-45, MW-47)."

3. **`design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`** (OPTIONAL — only if MW-40's RANGE_ANALYSIS section benefits from a documented-anomaly footnote referencing PR #241/#245). If the existing MW-40 commentary doesn't reference PILOT_787 or this verification round, ADD a brief footnote citing PR #209 + PR #213 + PR #241 + PR #245 with the conclusion "graduation-fail confirmed; BET MEDIUM stands." If the existing commentary already covers this adequately, SKIP.
   - Builder discretion: skip if not informative; orchestrator-scope to dispatch larger BATCH2 edits separately if needed.

### NIT carry-forward fold-in (per PR #237 + PR #240 carry-forward)

The -E PR is the next design-comm touch. Per `MAIN_TERMINAL_PR228_RESOLUTION_AND_JDPRE_DISPATCH_2026-05-06.md` + `MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md` carry-forward:

- **NIT-1 (terminology drift "composition quad" vs memory "composition triple")**: in -E memo, when documenting the v3.4 DO NOT Rule 11 + composition quad finding, use the canonical project terminology "composition quad" (matches v3.4 prompt surface). Footnote-cite the memory note's "composition triple" as legacy terminology that should be refreshed (memory edit is owner-scope; surface in -E for owner read).

- **NIT-2 (5th stop condition placement: <27/30 graduation threshold not in §8 STOP list of plan)**: -E memo explicitly cites the threshold (≥27/30 for graduation; observed 0/30 effective) as the Decision 3β graduation criterion. This is the threshold's first formal application; NIT-2 carry-forward is now satisfied (the threshold lived in plan §10 R4 only; in -E memo it's elevated to the top-level outcome reference).

- **NIT-3 (plan-internal-consistency cross-check, surfaced via PR #236 + PR #240)**: -E memo's "lessons learned" section documents the plan §4 contradictions (PR #236 HALT on sub-axis B blocker; PR #240 amendment "J as middle card" terminology drift). Promote to project process-improvement candidate: "future verification-round plans should run a contradiction-cross-check between hand-class spec and intra-sub-axis distribution rules + literal vs informal terminology before merge." Routes to TC-X-INTRA-PLAN-CONSISTENCY (informal class) and TC-X-DISPATCH-COMPLIANCE (informal class) as their motivating evidence; owner-scope to ratify the classes formally.

### Builder report

`review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md`:

- §"Verification round summary" — A→B→C→D→E pipeline summary; PR refs; final outcome
- §"4-source convergence table" — Sonnet pilot + Opus tier-up + protocol-rule chain + PILOT_787 anomaly; mirror format of MW-25 4-source graduation table
- §"Files edited" — exact diff scope
- §"NIT-1 / NIT-2 / NIT-3 carry-forward fold-in" — record of how each was applied in this PR
- §"Lessons learned" — structural argument was empirically too narrow; v3.4 DO NOT Rule 11 OOP-only exemption is the dominant routing for IP non-PFA TPMK T-kicker 4-way checked-through; PILOT_787's CHECK requires further single-hand investigation if revisited
- §"Stay-wrong list state" — 4 → 4 (unchanged); MW-17, MW-40, MW-45, MW-47
- §"What's blocked / what's queued" — 12.5J-C trainer integration test (parallel); 12.5K combined re-train (gates on -E + 12.5J-E)
- §"References" — PR #209, PR #213, PR #217, PR #228, PR #236, PR #237, PR #240, PR #241, PR #243, PR #244, PR #245, PR #247

### What you do NOT do

- Do NOT label hands (verification round complete)
- Do NOT modify the -B corpus or -C/-D label files (immutable empirical record)
- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source
- Do NOT modify BATCH2 reference labels (MW-40 stays BET MEDIUM; only optional footnote addition allowed)
- Do NOT update the stay-wrong list COUNT (still 4 — no graduation occurred)
- Do NOT promote informal classes to formal classes (owner-scope; surface for read only)

### Cost / time

~$0 (documentation only; no LLM, no inference). ~20-30 min builder wall clock for the 3-4 file edits + report.

### Deliverable scope

3-4 files in PR diff:
1. `review/RESTART_PROMPT_V9_3WAY.md` (annotation in MW-40 row)
2. `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (Verified Negative Result section + MW-40 entry; edited via filesystem outside the v2 repo)
3. `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md` (OPTIONAL footnote)
4. `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md`

Per `feedback_orchestrator_decides_not_recommends.md`: the memory file edit is part of this PR even though it lives outside v2. Builder edits the memory file directly (per PR #218 precedent); QC verifies via direct read.

### Stop conditions

- Stay-wrong list count modified (should remain 4) → STOP
- BATCH2 reference label changed (MW-40 BET MEDIUM stands) → STOP
- New labels added to corpus → STOP (verification round is complete; no new labels)
- v3.x prompts touched → STOP
- river-rats-core/ touched → STOP

### Builder report sections (mandatory)

(Listed above in §"Builder report" section.)

## QC stream — what you audit (when -E PR opens)

Standalone audit, ~10-15 min, 7-item scope:

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly the 3-4 files (memory file via direct read; v2-repo files via PR diff). NO touch to v3.x prompts, river-rats-core/, training-data, existing corpora, plan files (the merged plan stays as-is; -E doesn't amend it).

2. **Stay-wrong list integrity** — header still "4 True Remaining Failures"; MW-40 still listed; only annotation added; no other entries modified.

3. **BATCH2 reference label unchanged** — MW-40 BET MEDIUM stands in `BATCH2_8_HAND_DESIGNS.md` AND `BATCH2_8_RANGE_ANALYSIS.md` (if optional footnote added, only the COMMENTARY changes; the canonical label table row stays BET MEDIUM).

4. **Memory file integrity** — `reference_corrections.md` has the new "Verified Negative Result" entry (or appended structure); existing MW-25 entry unchanged; existing solver-corrected section unchanged.

5. **NIT-1 / NIT-2 / NIT-3 carry-forward fold-in** — verify -E memo addresses all 3 NITs explicitly per the dispatch §"NIT carry-forward fold-in" guidance.

6. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x / river-rats-core / training-data / corpus edits beyond scope.

7. **TC-X-DISPATCH-COMPLIANCE (6th formal exercise)** — verify -E was authored per dispatch (memo-only; no labels added; no factory; no inference); 4-source convergence table format matches MW-25 graduation pattern symmetrically (failing direction); references all 12+ PRs in the chain.

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md` on `qc/pr<N>-mw40-verification-e-review-2026-05-06`.

## Why no Opus tier-up on -E

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs. -E is a documentation memo with NO new labelling outputs. The empirical answer is the merged record from -C (PR #241) + -D (PR #245). -E codifies that record into project state. Standard QC PASS suffices.

## Sequencing — what fires after -E merges

Per dispatch queue:

1. **12.5J-C trainer integration test on 61-surface** — fires on -E merge. This is the engineering work that was queued earlier; non-blocking on MW-40 verification round outcome.
2. **12.5K combined re-train design** — gates on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship. Architect-hat phase.
3. **12.5L gate eval** — gates on 12.5K.

Per `feedback_orchestrator_controls_parallel_timing.md`: builder serial; orchestrator gates each transition.

## What's blocked / what's queued

**Cleared by this comm:**
- PR #245 merge (Builder -D Opus tier-up)
- PR #247 merge (QC verdict record)
- 12.5I-MW40-VERIFICATION-E memo-only PR dispatch fires
- MW-40 verification round complete (5 phases A→B→C→D→E)
- 4-source pattern fully documented

**Newly queued (after -E merges):**
- 12.5J-C trainer integration test on 61-surface
- 12.5K combined re-train design (gates on -E + 12.5J-E ship)

**Still queued (later):**
- 12.5J-D / 12.5J-E (post-12.5J-C)
- 12.5K combined re-train + 12.5L gate eval

**Owner-scope items pending (informational, non-blocking):**
- TC-X-INTRA-PLAN-CONSISTENCY ratification (curative entry #13; 1 surfaced finding via PR #236; class continues to deliver value)
- TC-X-DISPATCH-COMPLIANCE ratification (5 exercises now: PR #228 surfaced + PR #232 PASS + PR #236 PASS + PR #241 PASS + PR #245 PASS)
- Memory note refresh for "composition quad" vs "composition triple" terminology (NIT-1 surfaced in -E memo)
- Process-improvement candidate from PR #241 finding: "structural arguments must cross-check against v3.4 DO NOT rules before submission to verification rounds" — owner-scope to ratify as standing rule

## References

- PR #245 (Builder -D Opus tier-up; 5/5 BET): branch `programmer/phase125i-mw40-verification-d-opus-tierup-2026-05-06`
- PR #247 (QC PASS 0/0/0; CONVERGENT + INDEPENDENT corroboration): branch `qc/pr245-mw40-verification-d-review-2026-05-06`
- PR #246 (QC trigger): master `9925163`
- PR #244 (orchestrator: -D Path 3 Hybrid Opus dispatch): master `966fcbd`
- PR #243 (QC verdict on -C pilot HALT): master `f5aebe2`
- PR #241 (Builder -C pilot HALT 25/25 BET; -D's input): master `d411cb8`
- PR #228 (Plan; J-on-board structural prediction): master `e0e0304`
- PR #217 (Decision 3β source; graduation threshold ≥27/30): master `d6912ad`
- PR #213 (PILOT_787 Sonnet 3-2 source; the original CHECK signal): master `994ae67`
- PR #209 (Opus 4.7 MW-25 tier-up; precedent for -D pattern AND original PILOT_787 Opus HIGH source): master `077c168`
- v3.4 prompt protocol (DO NOT Rule 11 OOP-only exemption; the dominant routing rule): `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_orchestrator_decides_not_recommends.md` (orchestrator dispatches -E), `feedback_orchestration_efficiency_rules.md` (single comm: merge + dispatch), `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`

**Status: PR #245 + PR #247 cleared for merge. MW-40 graduation-fail confirmed via 4-source pattern symmetric to MW-25. LEAD-PROGRAMMER fires 12.5I-MW40-VERIFICATION-E memo-only PR on this comm merge. ~20-30 min wall clock to PR open.**
