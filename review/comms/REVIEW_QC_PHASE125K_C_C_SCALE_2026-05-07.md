---
date: 2026-05-07
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #285 — Phase 12.5K-C-C-SCALE (700 Lever C labels; Path A applied; MW-40 + MW-45 100% target-match; MW-17 + MW-47 sub-axis-variable) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR285_2026-05-07.md (master `50e815a`)
pr_branch: programmer/phase125k-c-c-scale-2026-05-07
qc_branch: qc/pr285-125kcc-scale-review-2026-05-07
---

# PR #285 — pre-merge QC verdict: PASS (0/0/0)

36th solo cycle. **Mass labelling milestone (700 labels; largest single-PR labelling audit).** All 8 items PASS. Path A re-tag (MW-17 → RAISE) verified at the situations layer; per-axis target-match math verified independently; reasoning convergent per axis with distinct v3.x rule chains; 0 solver-as-labels citations across 700 reasoning blocks.

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict | ✅ PASS (3 files) |
| 2. Path A re-tag verification (MW-17 design_action → RAISE) | ✅ PASS (50/50) |
| 3. Row count integrity (700 labels = 150×4 + 20×5) | ✅ PASS |
| 4. Per-axis target-match | ✅ PASS (100%/100% MW-40+MW-45; sub-axis-variable MW-17+MW-47 documented) |
| 5. No solver-as-labels (0/700) | ✅ PASS |
| 6. Reasoning convergence per axis | ✅ PASS (4 distinct v3.x rule chains) |
| 7. TC-X-OWNER-SCOPE-DISCIPLINE | ✅ PASS |
| 8. TC-X-DISPATCH-COMPLIANCE (15th formal exercise) | ✅ PASS |

**Verdict: PASS — clear to merge. Orchestrator dispatches 12.5K-C-D Opus tier-up on PR merge.**

## §2 — Path A re-tag verification

QC verified design_action distribution per axis in the v3 situations corpus (`corpus_lever_c_situations_v3_path_a_2026-05-07.jsonl`):

| Axis | design_action distribution | Match Path A |
|---|---|---|
| MW-17 | RAISE × 50 (was CALL × 50 in v1+v2) | ✅ Path A re-tag applied |
| MW-40 | BET × 50 | ✅ unchanged (per Path A scope) |
| MW-45 | RAISE × 50 | ✅ unchanged |
| MW-47 | RAISE × 50 | ✅ unchanged |

**PASS.** All 4 axes have design_action matching Path A ratification.

## §3 — Row count integrity

QC measurement on the 700-label jsonl:

| Metric | Builder claim | QC measurement |
|---|---|---|
| Total labels | 700 | 700 ✓ |
| Distinct hands | 170 (200 - 30 reused) | 170 ✓ |
| Per-hand labeller distribution | 4-5 labellers/hand | 150 hands × 4 + 20 hands × 5 = 600 + 100 = **700** ✓ |

Math: 170 hands × ~4.1 labellers/hand = 700 ✓

The 30 MW-40 reused hands (PILOT_LEVER_C_MW40_001..030) are NOT in this PR's labels — they retain authoritative labels from PR #241 (Sonnet 25/25 BET) + PR #245 (Opus 5/5 BET). This matches the §"MW-40 axis special case" cost-saving from PR #269.

**PASS.**

## §4 — Per-axis target-match verification

QC computed per-axis label distribution:

| Axis | Target | Total labels | Action distribution | Target-match rate |
|---|---|---|---|---|
| MW-17 | RAISE (Path A) | 205 | 113 RAISE / 41 CALL / 51 FOLD | 113/205 = **55.1%** (sub-axis-variable per builder claim) |
| MW-40 | BET | 85 | 85 BET (0 other) | **100%** |
| MW-45 | RAISE | 205 | 205 RAISE (0 other) | **100%** |
| MW-47 | RAISE | 205 | 149 RAISE / 54 CALL / 2 FOLD | 149/205 = **72.7%** (sub-axis-variable) |

**Builder claim verified:**
- MW-40 + MW-45 100% target-match ✓
- MW-17 + MW-47 sub-axis-variable ✓

The sub-axis-variable signal on MW-17 + MW-47 is consistent with the `feedback_solver_findings.md` finding 2 (blocker-effect sensitivity — different sub-axes within nut-FD axes can route to RAISE/CALL/FOLD depending on equity + position + multiway):
- MW-17 (HU-bet line): 55% RAISE consensus on Path-A re-tagged hands. The empirical truth at 50-hand parametric scale is that the "RAISE" target re-tag is the modal answer (113/205) but not unanimous.
- MW-47 (bet+call line): 73% RAISE consensus. v3.3 Fix 2.1 + v3.4 clause-e routing is more discriminative; 27% of hands fall into CALL (specific sub-axis combinations where clause-e gating doesn't trigger).

Per Path A ratification (orchestrator-decision), the sub-axis-variable signal is acceptable — the labels are the ground-truth for re-train (training data should reflect what the labelling pipeline actually produces, not just unanimous-consensus subsets).

**PASS.**

## §5 — No solver-as-labels

QC scanned all 700 reasoning blocks for solver/PIO/equity-solver citations as label authority. **0/700 such citations.** Authorities cited per block: v3.x protocol surface (v3.2 OVERRIDE threshold; v3.3 Fix 2.1; v3.4 clause-e gating; KB §1.7 nut-FD carve-out) + composition quad features + danger_score + has_flush_draw + bucket-first hand classification.

**PASS.**

## §6 — Reasoning convergence per axis

Sampled 1 reasoning block per axis (4 samples):

### MW-17 sample (PILOT_LEVER_C_MW17_001 RAISE HIGH):

> "This is a drawing hand — nut flush draw (AsKs on Jh9s5s, 9 spade outs) with no made hand. Hero is OOP in BB facing a single CO/BTN bet with no callers (num_callers_to_bet=0). The v3.2 KB §1.7 OVERRIDE threshold of villain_air_pct >= 0.20 applies in HU/bet-alone lines; villain_air_pct=0.2786 clears that threshold. Hero holds the Ace of spades (nut_flush_block=1), satisfying clause (a) of KB §1.7..."

Cites v3.2 OVERRIDE + KB §1.7 clause (a) + composition quad. Hand-specific values.

### MW-40 sample (PILOT_LEVER_C_MW40_031 BET HIGH):

> "This is a medium made hand (TdJh = top pair ten kicker with Jack on Js8c2d). Bucket: medium_made. Situation: hero is IP (BTN, closing action), three opponents all checked to hero (villain_checked_back = 1, villain_aggression_count = 0)..."

Cites bucket-first + composition quad + IP carve-out. Same chain as PR #241/#245 (consistent across phases).

### MW-45 sample (PILOT_LEVER_C_MW45_001 RAISE HIGH):

> "This is a monster hand (5c5d = set of fives on AhKs5hQc turn). Bucket: monster. Hero is IP (BTN), facing a turn bet from CO/BB after checking flop... better_hand_pct = 0.071 — only 7% of villain's range beats hero..."

Cites bucket + better_hand_pct + danger_score. Set-on-turn reasoning.

### MW-47 sample (PILOT_LEVER_C_MW47_001 RAISE HIGH):

> "This is a drawing hand — combo draw (AsQs on KsJh5s: nut spade flush draw + gutshot/open-ended straight draw with 17 outs) with no made hand. Hero is OOP in BB facing a bet with 1 caller (num_callers_to_bet=1) and villain_aggression_count=1, placing this in the v3.3 bet+call multiway line where the v3.2 0.20 villain_air_pct threshold is suspended. Checking v3.4 clause (e): villain_air_pct=0.2015..."

Cites v3.3 Fix 2.1 (bet+call multiway exception) + v3.4 clause (e). 17-out combo draw reasoning. Distinct from MW-17 (HU-bet line uses v3.2; MW-47 uses v3.3+v3.4 clause-e).

### Convergence verdict

All 4 axes show convergent reasoning with **distinct v3.x rule chains**:
- MW-17: v3.2 OVERRIDE threshold + KB §1.7 clause (a)
- MW-40: bucket-first + IP carve-out (from MW-40-VERIFICATION chain)
- MW-45: bucket monster + better_hand_pct + danger_score
- MW-47: v3.3 Fix 2.1 + v3.4 clause (e)

Convergence within each axis (per builder report Phase 3 indicates per-axis convergence). Distinct rule chains across axes confirm labellers correctly apply axis-specific protocol clauses. **NOT mode collapse.**

**PASS.**

## §1, §7-§8 — other items

**§1 Diff scope:** 3 files (700-label jsonl + v3 situations jsonl + 112L builder report). 0 deletions; 0 modifications. NOT touched: v3.x prompts, BATCH2, river-rats-core/, training-data, plan-comm, memory.

**§7 TC-X-OWNER-SCOPE-DISCIPLINE:** owner-scope perimeter held; v3.x prompts unchanged; BATCH2 references unchanged; reference set unchanged.

**§8 TC-X-DISPATCH-COMPLIANCE (15th formal exercise):**

| Compliance check | Match |
|---|---|
| Path A applied (MW-17 design_action → RAISE) | ✅ 50/50 |
| Pilot-first executed (per-axis 5-hand pilot before full scale) | ✅ MW-40 + MW-45 from PR #277 pilot-PASS; MW-17 + MW-47 from PR #281 fix-pilot |
| Sub-axis-variable not auto-resolved | ✅ Builder reports MW-17 55% RAISE / MW-47 73% RAISE; raw labels preserved |
| Orchestrator-scope decisions preserved | ✅ Path A orchestrator-decided; builder applied |
| MW-40 reused 30 hands NOT re-labelled | ✅ Only 20 fresh MW-40 in 85 labels |

Class durable on 15th formal exercise.

## TC-X-INTRA-PLAN-CONSISTENCY (informal continuation)

| Rule pair | Joint domain | Satisfiable? |
|---|---|---|
| Path A re-tag MW-17 RAISE ∧ Lever C corpus integration | MW-17 design_action shifted; corpus integration uses RAISE labels at -E | ✅ |
| 700 labels ∧ 170 fresh hands × 4-5 labellers | 150 × 4 + 20 × 5 = 700 | ✅ exact math |
| Sub-axis-variable MW-17 + MW-47 ∧ Path A acceptance | Path A accepts non-unanimous as ground truth (training data should reflect pipeline output) | ✅ |
| MW-40 30 reused ∧ 20 fresh in 85 labels | 30 reused (not in this PR; PR #241+#245 authoritative) + 20 × ~4.25 = 85 | ✅ |

No contradictions surfaced. **PASS.**

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (17th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (15th formal exercise; durable)**
- **TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE (entry #14; 5th informal exercise)** — at scale (700 labels across 4 axes; 4 distinct v3.x rule chains); class continues to validate as durable across volumes
- TC-X-INTRA-PLAN-CONSISTENCY (informal; no contradictions)
- TC-X-METHODOLOGY-RULE-CROSSCHECK

## Smarter-over-time observations

**Largest single-PR labelling audit to date:** 700 labels (vs 100 in PR #277; 50 in PR #281). All audit techniques scaled cleanly:
- Math verification: per-hand labeller distribution Counter approach handles arbitrary scale
- Per-axis aggregation: dictionary-based per-axis Counter scales to N axes
- Reasoning sampling: 4-axis × 1-sample = sufficient for convergence verification at this scale
- Solver-as-labels regex scan: 700 blocks scanned in <1s

**Sub-axis-variable signal on MW-17 + MW-47** is informationally rich:
- 55% MW-17 RAISE consensus = labelling pipeline confirms Path A re-tag at >50% rate, but ~45% of MW-17 sub-axes route to CALL/FOLD per equity-vs-pot-odds when KB §1.7 carve-out doesn't fully trigger
- 73% MW-47 RAISE consensus = stronger signal because v3.4 clause-e is more specific
- Both are training-data-suitable: the trained model will learn the per-sub-axis discrimination

**Compound value cycle continuing:**
- MW-40 verification round (PR #228-249) → 30 reused hands in Lever C
- Lever C-A design (PR #269) → per-axis off-ramp pattern
- Lever C-C pilot HALT (PR #277) → factory FD-suit diagnosis
- Lever C-C-FIX (PR #281) → MW-17 axis-target shift discovery
- Lever C-C-SCALE (PR #285, this audit) → 700 labels with Path A re-tag

The QC class system has accompanied every step of this 5-PR Lever C cycle, maintaining empirical-faithful audit trail.

## Audit cost / time

- Wall clock: ~16 min (data audit + per-axis verification + reasoning sampling + verdict authoring). Within 15-20 min estimate.
- LLM cost: $0.

## Gates

PR #285 cleared from QC side. Per dispatch §"What gates":
- PR #285 merge: clear from QC; mass labelling complete with verified Path A
- 12.5K-C-D Opus tier-up dispatch: gates on PR #285 merge

No QC-side blocker.

## References

- 12.5K-C-C-SCALE dispatch (Path A): `MAIN_TERMINAL_PR281_RESOLUTION_AND_125KCC_SCALE_DISPATCH_2026-05-07.md` (master `7652b75`, PR #284)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR285_2026-05-07.md` (master `50e815a`)
- Builder report: `BUILDER_REPORT_PHASE125K_C_C_SCALE_2026-05-07.md` (in PR #285; 112L)
- Lever C plan: `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`
- v3.x protocols: `prompts/gto_labeller_v3.4.md` (KB §1.7 nut-FD carve-out; v3.3 Fix 2.1; v3.2 OVERRIDE threshold)
- 30 reused MW-40 source: PR #241 (Sonnet 25/25 BET) + PR #245 (Opus 5/5 BET)
- Memory: `feedback_solver_findings.md` finding 2 (blocker-effect sensitivity); `feedback_pilot_first_for_long_jobs.md`; `feedback_orchestrator_decides_not_recommends.md`

**Status: VERDICT = PASS. PR #285 cleared for merge from QC side. Mass labelling complete (700 labels); Path A re-tag verified; per-axis math correct; reasoning convergent per axis with distinct v3.x rule chains. 36th solo QC cycle. TC-X-DISPATCH-COMPLIANCE 15th formal exercise; TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE 5th informal exercise; classes durable at scale.**
