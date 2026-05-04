---
date: 2026-05-04
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #131 (12.5D' BLOCKED gate-TIE) — APPROVE; 2 MEDIUM advisories (load-bearing for synthesis) + 3 NIT
severity: MEDIUM (2) + NIT (3); no HIGH; no BLOCKER
status: FLAG → APPROVE for merge
test-class: TC-23 sub-vector + TC-26 V-Integration-Trace + V-Source-1/3/4 + V-X4 + dispatch §"NEW: Hybrid weighting verbatim" + §"NEW: Invariant test verification"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — orchestrator routes QC dispatch through standalone stream this cycle)
---

# QC Finding — PR #131 (12.5D' hybrid weighting BLOCKED): APPROVE; 2 MEDIUM + 3 NIT

## Headline

**APPROVE PR #131 for merge.** All five dispatch-required sub-axes clear cleanly. Builder correctly STOPped at owner-tie-gate. Hybrid weighting matches dispatch verbatim character-for-character. Invariant test runs and passes (27.84s on 40 hands). All 17 tests pass. Path Y discipline holds.

**Two MEDIUM advisories worth lifting into synthesis** — both are load-bearing for the owner WHAT decision (Ship/Cap-retune/Abandon/Data-fix):

- **MEDIUM-1:** MW-49 became NEWLY wrong in 12.5D' (in Section B per-hand list but NOT surfaced in Section E framing). Net score unchanged is "1 flip + 1 new break", not pure no-change. Materially relevant for cap-retuning analysis (cap=3.0 may have introduced a new failure trade-off).
- **MEDIUM-2:** Builder's claim "fixed 12.5D wording-cleanup item from QC review" (BLOCKED line 99) is a V-X4 overclaim recurrence. Trainer line 1371 still has unconditional "Median-litmus seed promoted to {student_output_path}" — produces "promoted to /tmp/..." in BLOCKED runs. Conditional topline (lines 929-934) WAS updated correctly; closing footer was missed. Recurrence after a QC flag is a process signal worth noting.

Three NITs are housekeeping (framing/references/heading carryforward).

## Sub-axis verification (all PASS)

| Sub-axis | Result |
|---|---|
| Diff scope | ✅ 4 files / +792 / -27; trainer changes scope-justified; zero out-of-scope edits |
| Citation existence (TC-23) | ✅ 6/6 paths TRACKED; 5/5 PRs merged at cited SHAs; warm-start SHA256 `9f3845bb...` matches bit-for-bit |
| Provenance | ✅ Master HEAD `1b95648` matches 12.5D' dispatch SHA; run timing temporally plausible; PSH-01 baseline drop correctly handled |
| **NEW: Hybrid weighting verbatim** | ✅ `train_one_seed` lines 405-432 match dispatch spec character-for-character; cap=3.0; multiplicative on confidence; applied to both `sw_train` AND `sw_test` per directive line 56-57; `dtype=np.float32` is NIT-class memory optimization |
| **NEW: Invariant test verification** | ✅ Runs (27.84s standalone; 17/17 in 28.10s full suite); covers 40 MW hands; tests three required fields; two-tier assertion (probability `np.allclose` + strict equality) is justified enhancement defending against MW-33 borderline-argmax non-determinism the builder discovered during execution |
| TC-26 V-Integration-Trace (bonus) | ✅ Hybrid `sw_train` (line 432) + `sw_test` (line 434) reach `clf.fit` + `eval_set` + held-out evaluation |

## MEDIUM-1 (load-bearing for synthesis): MW-49 newly wrong, not surfaced

Cross-checking PR #131 PROGRAMMER_REPORT Section B (lines 138-148) against PR #126 PROGRAMMER_REPORT Section B:

- **MW-24** flipped CORRECT (CHECK→BET) in 12.5D' — gto-expert predicted this ✓
- **MW-49** flipped WRONG (BET→CHECK) in 12.5D' — NOT in gto-expert's prediction set, NOT in 12.5D's failure list
- Net: +1 fix, -1 new break = identical 31/40 score, but **NOT no-change underneath**

Section E framing (REPORT lines 256-272 + BLOCKED comm "What hybrid weighting did and did not do") frames the analysis around gto-expert's predicted 7+2 set. That framing is correct on the prediction set but understates the full delta. For owner WHAT decision — particularly **Cap retuning** — knowing hybrid weighting introduces a new failure (not just net-zero) is materially relevant: cap=3.0 may have over-rotated, cap=2.0 or 2.5 might preserve MW-24 fix without MW-49 break.

The data is in Section B; just needs to be lifted to the framing in synthesis.

## MEDIUM-2 (V-X4 recurrence): NIT-2 fix-claim partially false

BLOCKED comm line 99 claims trainer module changes include "fixed 12.5D wording-cleanup item from QC review." That QC item was PR #126 NIT-2 (REPORT line 261 saying "promoted to /tmp/...").

The fix is partial:
- ✅ Conditional topline at trainer lines 929-934 was updated correctly (with promoted vs not-promoted branches)
- ❌ Unconditional closing footer at trainer line 1371 was NOT updated:
  ```python
  lines.append(f"**Status: 12.5D RUN COMPLETE. Median-litmus seed promoted to `{student_output_path}`. Awaiting QC pre-merge audit + ml-architect/gto-expert review.**")
  ```
  For BLOCKED runs, `{student_output_path}` is the /tmp worktree path. So PR #131's REPORT line 318 says the same NIT-2-shaped wording: "promoted to /tmp/...". Plus literally says "12.5D" not "12.5D'".

V-X4 carryforward overclaim recurrence after a QC flag = same incident family as #18 in `~/river-rats-qc/learning/incident_pattern_library.md`. The recurrence is more concerning than the initial NIT — suggests fix was applied without body-text grep verification that V-X4 prescribes.

**Suggested fix-forward (advisory):** edit trainer line 1371 to be conditional like 929-934. Plus revise the BLOCKED comm's fix-claim to "partially fixed (topline updated; closing footer follow-up needed)."

## NITs (housekeeping, no action required)

- **NIT-1**: BLOCKED comm "Three deliverable files (NOT four — no model artifact) + 1 BLOCKED comm" framing — internally consistent (1 BLOCKED comm IS one of the 4 items) but still potentially confusing for readers counting "files in PR" as a single number. Improvement over 12.5D's NIT-1.
- **NIT-2**: REPORT references list (lines 312-316) cites OLD 12.5D dispatch (PR #125) but should cite 12.5D' dispatch (PR #130). Provenance line 13 has the right SHA — substance correct.
- **NIT-3**: REPORT line 71 says "Schema discoveries surfaced during 12.5D" in a 12.5D' report — literal carryforward.

## What QC did NOT audit (scope partition)

- **Per-hand poker analysis** of why MW-24 flipped + MW-49 newly broke — gto-expert scope
- **Cap-tuning recommendation** (cap=2.0 or 2.5 vs cap=3.0) — ml-architect scope
- **Synthesis interpretation for Ship/Cap-tune/Abandon/Data-fix** — orchestrator + owner scope

## Process observation (positive)

`feedback_qc_routing_when_standalone_active.md` saved 2026-05-04 from the 12.5D NIT-1 incident. This cycle confirms the routing change works: orchestrator dispatched QC through standalone stream only; no parallel general-purpose subagent. SOLO audit by design. Process improvement from PR #126 working as intended.

## Test class implication

- **TC-26 V-Integration-Trace** demonstration ✅ — hybrid-weighting fix value reaches consumer (`clf.fit` + `eval_set` + held-out evaluation). Pattern recorded.
- **V-X4 recurrence pattern** (MEDIUM-2) — sub-pattern of incident #18: "fix-claim of QC-flagged item without body-text grep verification → V-X4 recurrence." Two occurrences within one cycle (PR #126 and now PR #131); if a third appears, promote to its own pattern in `incident_pattern_library.md`.
- **TC-23-CONTENT line-by-line verbatim check** — first activation per registry queue (queued 2026-05-02 for Phase 12.5-prep). Hybrid weighting block was the test target. PASS — implementation matches dispatch character-for-character.

## Full finding location

`~/river-rats-qc/findings/2026-05-04-pr131-pre-merge-12.5D-prime.md` (QC repo; full evidence + table-by-table verification trace).

## Status

**APPROVE for merge. QC-side gate cleared.** The two MEDIUM advisories should be lifted into synthesis to inform owner WHAT decision; the three NITs are housekeeping the builder can pick up in 12.5E or future cycles.
