---
date: 2026-05-07
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #281 — Phase 12.5K-C-C-FIX Path 2 (factory FD-suit fixed; MW-47 PASS; MW-17 axis-target shift to RAISE; HALT-escalate) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR281_2026-05-07.md (master `c64d820`)
pr_branch: programmer/phase125k-c-c-fix-redesign-2026-05-07
qc_branch: qc/pr281-125kcc-fix-review-2026-05-07
---

# PR #281 — pre-merge QC verdict: PASS (0/0/0)

35th solo cycle. **Path 2 factory redesign successful at infrastructure level** (FD activation 0%→70%/98%). **Builder's MW-17 axis-target shift diagnosis VERIFIED INDEPENDENTLY**: redesigned hands moved hero from canonical "off-suit + 3-same-suit board" backdoor-class to "suited hero + 2-FD-suit board" real-FD-class — different hand class entirely. Canonical-vs-pipeline mismatch parallel to MW-40-VERIFICATION graduation-fail finding.

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict | ✅ PASS (4 files) |
| 2. Factory FD-suit fix verified (70%/98% activation) | ✅ PASS |
| 3. Path 2 re-design integrity (MW-40 + MW-45 PRESERVED) | ✅ PASS (50/50 signatures identical) |
| 4. Re-pilot label integrity (50 labels) | ✅ PASS |
| 5. Reasoning convergence per axis | ✅ PASS (per-axis distinct rule chain; not mode collapse) |
| 6. **MW-17 axis-target shift diagnosis** [critical] | ✅ **VERIFIED** |
| 7. No solver-as-labels | ✅ PASS |
| 8. TC-X-OWNER-SCOPE-DISCIPLINE | ✅ PASS |
| 9. TC-X-DISPATCH-COMPLIANCE (14th formal exercise) | ✅ PASS |

**Verdict: PASS — clear to merge. Builder's HALT-escalate correct; orchestrator decides Path A (re-tag MW-17 as RAISE) / Path B (redesign for canonical pot-odds match) / Path C (drop MW-17).**

## §2 — Factory FD-suit fix verified

QC independent verification:

| Axis | has_flush_draw=1 / total | Activation rate | Builder claim | Match |
|---|---|---|---|---|
| MW-17 | 35/50 | 70% | 70% | ✅ |
| MW-40 | 0/50 | 0% | preserved (no FD per axis class) | ✅ |
| MW-45 | 0/50 | 0% | preserved (no FD per axis class) | ✅ |
| MW-47 | 49/50 | 98% | 98% | ✅ |

Factory-level fix worked exactly as designed. **PASS.**

## §3 — Path 2 re-design integrity (MW-40 + MW-45 PRESERVED)

Per dispatch §"Do NOT modify MW-40 + MW-45": MW-40 + MW-45 from v1 corpus must be preserved unchanged in v2 corpus.

QC independent verification (signature comparison):

| Axis | v1 count | v2 count | v1↔v2 signatures identical |
|---|---|---|---|
| MW-17 | 50 | 50 | (redesigned per Path 2) |
| MW-40 | 50 | 50 | **50/50 ✓** |
| MW-45 | 50 | 50 | **50/50 ✓** |
| MW-47 | 50 | 50 | (redesigned per Path 2) |

(Signature = `hero_cards`, `board`, `hero_position`, `design_action`, `axis`)

MW-40 + MW-45 fully preserved. **PASS.**

## §4 — Re-pilot label integrity

50 labels = 5 hands × 5 labellers × 2 axes (MW-17 + MW-47). QC verification:

| Axis | Pilot label count | Action distribution |
|---|---|---|
| MW-17 (target CALL) | 25 | 25 RAISE (0 CALL, 0 FOLD) |
| MW-47 (target RAISE) | 25 | 25 RAISE |

Both axes unanimous RAISE. Math: 5×5×2 = 50 ✓. All labels well-formed. **PASS.**

## §5 — Reasoning convergence per axis

Per builder report Phase 3 reasoning samples:

**MW-17 hands** (HU-bet line; num_callers_to_bet=0):
> "v3.2 0.20 threshold governs HU-bet lines. villain_air_pct 0.2786-0.3189 clears 0.20 floor. KB §1.7 nut-FD + Ace blocker RAISE fires."

**MW-47 hands** (bet+call line; num_callers_to_bet=1, villain_aggression_count=1):
> "v3.3 Fix 2.1 suspends the 0.20 threshold for bet+call multiway. All v3.4 clauses (a)-(e) satisfied (nut FD + Ace blocker + OOP + bet+call no-raise + raw_equity ≥ 0.35 + villain_air_pct ≥ 0.05). KB §1.7 RAISE re-applies. MW-47 calibration anchor confirms."

Per-axis convergent reasoning with **distinct rule chains** (HU-bet line uses v3.2 0.20 threshold; bet+call line uses v3.3 Fix 2.1). Both axes converge on RAISE via KB §1.7 nut-FD carve-out, but through different pipeline-routing clauses. NOT mode collapse — labellers correctly applied per-axis-specific protocol clauses.

**PASS.**

## §6 — MW-17 axis-target shift diagnosis (CRITICAL)

Builder's claim per §"Why MW-17 failed: structural-target / structural-fix mismatch":

> Canonical MW-17 (BATCH2): AdKs (off-suit) on Jd8d4c (2 diamonds + 1 club). Hero has 1 diamond, board has 2 diamonds = 3 total → has_flush_draw=0 per pipeline (requires ≥4). Equity 0.251 (low; backdoor + nut blocker at pot-odds boundary). Action target CALL HIGH.
>
> Path 2 redesign MW-17: AsKs (suited spades) on board with 2 spades = 4 spades total → has_flush_draw=1 per pipeline. Real FD with 9 outs + nut blocker. Different hand class entirely.

QC independent verification of canonical structure:
- Per memory `feedback_solver_findings.md` finding 5: "MW-17: AdKs on Jd8d4c → CALL low equity" — canonical MW-17 reference confirmed
- Pipeline `has_flush_draw` activation logic: requires ≥4 same-suit cards (hero 2 + board 2). Canonical MW-17 has hero off-suit (1 diamond max from hero, since hero is AdKs which has 1 diamond), board has 2 diamonds = max 3 same-suit total → has_flush_draw=0
- Path 2 redesign added hero AsKs (suited spades = 2 hero spades) on 2-FD-suit board (Js9s5d-class with 2 spades) = 4 spades total → has_flush_draw=1 → KB §1.7 nut-FD carve-out triggers RAISE

**Builder's diagnosis is mathematically verified.** The redesigned MW-17 hands test a DIFFERENT axis class than canonical MW-17 reference:

- Canonical MW-17 = "low-equity backdoor-FD-with-nut-blocker at pot-odds boundary" → CALL
- Redesigned MW-17 = "high-equity real-FD-with-nut-blocker" → RAISE per KB §1.7

The "fix" should have been to LOWER pot odds (e.g., CO bet 27% pot rather than 50% pot to match canonical) rather than ADD real FD (which fundamentally changed the hand class).

This is **a labelling-pipeline-canonical mismatch parallel to MW-40-VERIFICATION graduation-fail**:
- MW-40: pipeline produces BET on parametric variants; canonical CHECK was structural-prediction-based; verification confirmed pipeline answer (BET) at scale
- MW-17: pipeline produces RAISE on real-FD redesigned variants; canonical CALL was backdoor-FD-class; redesign moved the test out of the canonical's hand class

**Implication for orchestrator path selection** (per dispatch §"Per-axis off-ramp decision matrix"):

| Path | Description | Trade-off |
|---|---|---|
| A | Re-tag MW-17 axis as RAISE (accept empirical finding; pipeline-faithful) | Acknowledges that "under-calling" axis = real-FD-RAISE not backdoor-CALL; updates BATCH2 if owner ratifies |
| B | Redesign MW-17 to LOWER pot odds (CO bet ~27% pot); test backdoor-FD CALL hand class | Re-tests canonical MW-17 axis class faithfully; may or may not produce CALL consensus |
| C | Drop MW-17 from Lever C entirely; ship MW-40 + MW-45 + MW-47 | Lever C corpus 150 hands instead of 200; preserves 12.5K-K combined re-train scope |

QC has no preference. Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator decides.

**PASS** (diagnosis verified; off-ramp paths surfaced).

## §1, §7-§9 — other items

**§1 Diff scope:** 4 files (50-row pilot labels jsonl + 200-row v2 situations jsonl + 138L builder report + 314L factory script). Verified NOT touched: v3.x prompts, BATCH2, river-rats-core/, training-data, plan-comm, memory.

**§7 No solver-as-labels:** reasoning samples cite v3.2/v3.3/v3.4 protocol clauses + KB §1.7 + MW-47 calibration anchor. 0 solver citations as label authority.

**§8 TC-X-OWNER-SCOPE-DISCIPLINE:** owner-scope perimeter held; v3.x prompts unchanged; BATCH2 references unchanged; reference set unchanged.

**§9 TC-X-DISPATCH-COMPLIANCE (14th formal exercise):**

| Compliance check | Match |
|---|---|
| Path 2 phases 1+2+3 executed | ✅ Phase 1 redesign + Phase 2 re-emit + Phase 3 re-pilot |
| HALT-and-escalate on EITHER pilot FAIL | ✅ MW-17 FAIL → HALT triggered; full-scale run NOT FIRED |
| Orchestrator-scope decision route preserved | ✅ Path A/B/C surfaced; no auto-selection |
| MW-40 + MW-45 preserved unchanged | ✅ 50/50 signatures identical |
| Re-pilot scoped exactly per dispatch | ✅ 5 hands × 5 labellers × 2 axes = 50 labels |

Class durable on 14th formal exercise.

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (16th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (14th formal exercise; durable)**
- **TC-X-DISPATCH-PREDICTION-VERIFICATION (entry #11; 5th formal exercise)** — class catches axis-target shifts as factory-vs-canonical structural mismatches; distinguishes from labelling-pipeline-divergence
- **TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE (entry #14; 4th informal exercise)** — class detects per-axis distinct rule chains (v3.2 vs v3.3 vs v3.4 + KB §1.7) as convergent (not mode collapse)
- TC-X-INTRA-PLAN-CONSISTENCY (informal continuation)

## Smarter-over-time observations

**Canonical-vs-pipeline mismatch family pattern:**

PR #281 surfaces a **second instance** of the canonical-vs-pipeline mismatch class first identified at MW-40-VERIFICATION (PR #228-249 cycle):
- MW-40: pipeline BET; canonical CHECK was structural-prediction-based; verification confirmed pipeline (BET)
- MW-17: pipeline RAISE on real-FD redesign; canonical CALL was backdoor-FD-class (hand-class shifted, not just prediction)

The pattern: BATCH2 canonical references include hands where the labelling pipeline's empirical answer differs from the canonical, and the difference is structural (different hand class) rather than just-noise.

**Worth noting for future verification rounds:** when a canonical reference says "low-equity backdoor + nut-blocker → CALL", the parametric expansion should preserve the backdoor-FD-only structure (hero off-suit, ≤3 same-suit total), NOT add real FD. This is **a learning candidate for owner ratification as a curative class:**

- TC-X-CANONICAL-HAND-CLASS-PRESERVATION: when expanding a canonical reference to parametric variants, verify hero+board same-suit-count distribution preserves the canonical's hand class. If canonical has has_flush_draw=0, parametric variants should preserve has_flush_draw≈0; if canonical has has_flush_draw=1, preserve has_flush_draw≈1.

(Logging informally to `~/river-rats-qc/learning/incident_pattern_library.md` as watch-list pattern; awaiting 2-3 instances or owner directive for class formalization.)

## Audit cost / time

- Wall clock: ~14 min (canonical structure verification + signature comparison + per-axis label distribution + critical diagnosis verification + verdict authoring). Within 10-15 min estimate.
- LLM cost: $0.

## Gates

PR #281 cleared from QC side. Per dispatch §"What gates":
- PR #281 merge: clear from QC; HALT-escalate correctly executed
- Path A/B/C selection: orchestrator decides on PR merge
- Subsequent execution: orchestrator dispatches per chosen path

## References

- 12.5K-C-C-FIX dispatch (Path 2 redesign): `MAIN_TERMINAL_PR277_RESOLUTION_AND_125KCC_REDESIGN_DISPATCH_2026-05-07.md` (master `748f3a3`, PR #280)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR281_2026-05-07.md` (master `c64d820`)
- Builder report: `BUILDER_REPORT_PHASE125K_C_C_FIX_2026-05-07.md` (in PR #281; 138L)
- v1 situations corpus (PR #273; baseline for MW-40 + MW-45 preservation comparison): `data/corpus_lever_c_situations_2026-05-07.jsonl`
- v2 situations corpus (this PR): `data/corpus_lever_c_situations_v2_2026-05-07.jsonl`
- Pilot labels: `data/corpus_lever_c_fix_pilot_labels_raw_2026-05-07.jsonl` (50 labels)
- v3.4 KB §1.7 (nut-FD carve-out): `prompts/gto_labeller_v3.4.md`
- BATCH2 MW-17 reference: `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`
- Memory: `feedback_solver_findings.md` finding 5 (canonical MW-17 = AdKs on Jd8d4c CALL low equity; QC's diagnosis verification source)
- Curative log: `~/river-rats-qc/learning/curative_additions_log.md` entries #11-#14

**Status: VERDICT = PASS. PR #281 cleared for merge from QC side. Factory FD-suit fix verified (70%/98% activation); MW-40+MW-45 preserved; MW-17 axis-target shift diagnosis VERIFIED (canonical-vs-pipeline mismatch parallel to MW-40-VERIFICATION); orchestrator decides Path A/B/C. 35th solo QC cycle. TC-X-DISPATCH-COMPLIANCE 14th formal exercise; TC-X-DISPATCH-PREDICTION-VERIFICATION 5th formal exercise; TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE 4th informal exercise; all classes durable. New watch-list pattern: TC-X-CANONICAL-HAND-CLASS-PRESERVATION.**
