---
date: 2026-05-06
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #236 — Phase 12.5I-MW40-VERIFICATION-B (Path γ' amended; 30 J-on-board variants; pre-flight 4-check PASS) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 1 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR236_2026-05-06.md (master `c028fdb`, PR #238)
amended_dispatch: MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md (master `42460ae`, PR #237)
pr_branch: programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06 (head `58ac0d6`)
qc_branch: qc/pr236-mw40-verification-b-review-2026-05-06
---

# PR #236 — pre-merge QC verdict: PASS (0 / 1 SHOULD_FIX / 0 NIT)

24th solo cycle. Path γ' amended situation-generation milestone. All 8 trigger items verified. Builder's Hybrid pilot-first 4-check PASS confirmed by data + script audit; ref_id namespace disjoint by construction; Step-18 prediction matches observed (0/30 each). **One SHOULD_FIX surfaced**: amended dispatch's sub-axis C spec is internally contradictory ("J as middle card" vs the inherited 10 plan §4 boards which are all J-as-highest). Builder followed the plan-inheritance half correctly; orchestrator-scope to resolve.

This is the **first informal activation of TC-X-INTRA-PLAN-CONSISTENCY** (curative entry #13 added 2026-05-06 ~22:11 SAST, 1 tick before this audit fired). The class delivered value on first run — surfaced a real dispatch-internal contradiction that the 7-item baseline audit would not have caught.

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. Pre-flight 4-check correctness (Hybrid pilot-first) | ✅ PASS |
| 3. Row count integrity (30 / no dups / namespace disjoint) | ✅ PASS |
| 4. Sub-axis distribution (Path γ' 15/0/15) | ✅ PASS |
| 5. Schema integrity (61-surface uniform; 0 NaN/Inf) | ✅ PASS |
| 6. Step-18 activation (≈ 0 across 30) | ✅ PASS |
| 7. TC-X-DISPATCH-COMPLIANCE (3rd formal exercise) | ✅ PASS |
| 8. Path γ' compliance (5 additional per A and C; T-kicker; ≤2 paired-J) | ⚠️ SHOULD_FIX-1 (sub-axis C "J as middle card" contradiction) |
| TC-X-INTRA-PLAN-CONSISTENCY (informal; curative entry #13) | ⚠️ ACTIVATED — same SHOULD_FIX-1 |

**Verdict: PASS — 0 BLOCKER. Orchestrator should resolve SHOULD_FIX-1 (dispatch-internal contradiction) before -C labelling fires** so labellers are evaluating the intended structural pattern.

## §1 — Diff scope strict

`git diff --stat master...origin/programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06` (three-dot):

```
 data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl |  30 ++
 review/comms/BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md | 125 +++
 review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md | 191 ++++++
 scripts/build_corpus_revision_125i_mw40_verif_situations.py | 426 ++++++++++++++++
 4 files changed, 772 insertions(+)
```

All 4 files match the trigger's expected list (jsonl + factory script + builder report + HALT query carry-forward). 0 deletions, 0 modifications. **PASS** for diff scope.

Verified NOT touched (perimeter sweep):
- `prompts/` (v3.x) — 0 changes
- `design/multiway_reference_set/BATCH2_*` — 0 changes
- `river-rats-core/` — 0 changes
- `data/corpus_combined_*` (existing 788-corpus) — 0 changes
- `data/corpus_revision_125i_situations_*` (94 prior 12.5I-C revisions) — 0 changes
- `training-data/`, model files, memory files — 0 changes
- `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_*` (the merged plan) — 0 changes (TC-X-DISPATCH-COMPLIANCE: builder did NOT auto-fix the plan)

Owner-scope perimeter held. **PASS.**

## §2 — Pre-flight 4-check correctness

Builder report §"Pre-flight 4-check on first 5" reports the Hybrid pilot-first ran on `PILOT_MW40_VERIF_001..005` BEFORE emitting the remaining 25:

| Check | Trigger spec | Builder result |
|---|---|---|
| 1 — Schema parity | 61-surface; 0 NaN/Inf/missing | ✅ PASS (5 × 61 = 305 values; 0 NaN/Inf) |
| 2 — Step-18 plausibility | Both ≈ 0 across J-on-board | ✅ REPORT (0/5 for both; matches plan §5 prediction; per amended dispatch this is REPORT not STOP) |
| 3 — ref_id namespace | All in `PILOT_MW40_VERIF_001..005`; disjoint | ✅ PASS (0 collisions vs 1476 existing ref_ids: 788-corpus + 94-revision corpus + prior 12.5I) |
| 4 — Top-level structural fields | Match plan §3 constraint table | ✅ PASS (per builder report §"Pre-flight 4-check"; spot-verified in QC data audit, see §3-§4 below) |

QC independently re-verified Check 1 + Check 2 + Check 3 on the FULL 30 emitted corpus (not just first 5):
- Schema parity: 30/30 rows have feat_dict size 61; 0 NaN/Inf in 30 × 61 = 1830 values
- Step-18 plausibility: 0/30 for both `nut_blocker_overcard_count` and `bet_call_multiway_oop_raise_pressure_index` — matches plan §5 prediction exactly
- ref_id namespace: `PILOT_MW40_VERIF_001..030` complete (no gaps); 0 collisions vs 788-corpus + prior 125i

**PASS.** Pre-flight discipline applied as Path 3 Hybrid resolution intends.

## §3 — Row count integrity

| Metric | Builder claim | QC measurement | Match |
|---|---|---|---|
| Total rows | 30 | 30 | ✅ |
| Distinct ref_ids | 30 | 30 (via `pilot_hand_id` field) | ✅ |
| Namespace | `PILOT_MW40_VERIF_001..030` exact | 001..030, no gaps | ✅ |
| Cross-source ref_id collision (vs 788) | 0 | 0 | ✅ |
| Cross-source ref_id collision (vs 94-revision 125i) | 0 | 0 | ✅ |

**PASS.**

## §4 — Sub-axis distribution (Path γ' 15/0/15)

| Sub-axis | Path γ' target | Builder emission | Match |
|---|---|---|---|
| A (J-high flop) | 15 | 15 | ✅ |
| B (dropped) | 0 | 0 | ✅ |
| C (J-medium per spec; J-as-highest per inherited boards — see SHOULD_FIX-1) | 15 | 15 | ✅ on count |

**PASS** for distribution count; SHOULD_FIX-1 on board character (see §"SHOULD_FIX-1" below).

## §5 — Schema integrity (61-surface uniform)

QC measurement on full 30 rows:
- All 30 rows have `feat_dict` size = 61 (single key set across all 30; perfect uniformity)
- 0 rows with NaN/Inf in any feat_dict value (1830 values total)
- All 30 rows have identical top-level key set (`blocker_variant`, `board`, `design_action`, `facing_bet`, `feat_dict`, `generation_source`, `hero_cards`, `hero_position`, `num_opponents`, `opener_position`, `pilot_hand_id`, `pot`, `prior_actions`, `situation_id`, `street`, `sub_axis`, `template_id`, `to_call`, `villain_positions`)

Constraint table verification (uniform across all 30):

| Constraint | Plan §3 spec | QC observed | Match |
|---|---|---|---|
| `hero_position` | BTN | BTN (30/30) | ✅ |
| `num_opponents` | 3 | 3 (30/30) | ✅ |
| `street` | flop | flop (30/30) | ✅ |
| `facing_bet` | False | False (30/30) | ✅ |
| `to_call` | 0.0 | 0.0 (30/30) | ✅ |
| `hero_cards` (TJ uniform) | TJ off-suit | All 30 are TJ (9 suit-permutations) | ✅ |
| `template_id` | T11_MW40V | T11_MW40V (30/30) | ✅ |
| `design_action` | CHECK | CHECK (30/30) | ✅ |
| `blocker_variant` | with_J_blocker uniform | with_J_blocker (30/30) | ✅ |

**PASS.** No TT or T9 leakage from dropped sub-axis B.

## §6 — Step-18 activation pattern

| Feature | Plan §5 prediction | Observed (full 30) | Match |
|---|---|---|---|
| `nut_blocker_overcard_count` | ≈ 0 across J-on-board variants | 0/30 active | ✅ exact |
| `bet_call_multiway_oop_raise_pressure_index` | ≈ 0 across J-on-board variants | 0/30 active | ✅ exact |

Both Step-18 features show exactly the predicted activation pattern. Per `feedback_attention_flags_when_features_change.md` capture discipline: feature changes match the plan's anticipated pattern; no attention-vocab flag triggered. **PASS.**

## §7 — TC-X-DISPATCH-COMPLIANCE (3rd formal exercise)

Cross-check builder's implementation against amended dispatch (`MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md`):

| Compliance check | Spec | Observation | Match |
|---|---|---|---|
| 4-check pre-flight on first 5 | Hybrid Path 3 binding | builder ran via `_preflight_4check` before emitting beyond 5 | ✅ |
| Sub-axis split 15/0/15 | Path γ' resolution | A=15 / B=0 / C=15 emitted | ✅ |
| No auto-fix to merged plan | builder must not modify plan | `PLAN_PHASE125I_MW40_VERIFICATION_*` 0 changes in PR diff | ✅ |
| T-kicker pinned | resolution §"sub-axis B board-list expansion guidelines" point 5 | All 30 hero hands are TJ (no adjacent-kicker variants) | ✅ |
| No NIT-1/NIT-2 auto-fix from PR #228 | builder must not modify plan | plan unchanged; NITs carry-forward to -E | ✅ |
| Hero TJ off-suit uniform | resolution §"Path γ' table" col "Hand classes" | TJ across all 30; off-suit confirmed (9 suit-permutations of T+J) | ✅ |

Per `feedback_listen_to_orchestrator_always.md`: builder followed orchestrator-named-author execution path. No unilateral deviation in builder behavior.

**PASS for builder's compliance** (the SHOULD_FIX surfaced below is a contradiction WITHIN the dispatch, not a builder deviation from it).

## §8 — Path γ' compliance + SHOULD_FIX-1

### Path γ' headline compliance

| Requirement | Spec | Builder | Match |
|---|---|---|---|
| 15 boards in sub-axis A (10 inherited + 5 additional) | resolution comm §"Path γ' table" sub-axis A | 15 boards (Js9c5h ... + 5 additional Js-prefix) | ✅ |
| 15 boards in sub-axis C (10 inherited + 5 additional) | resolution comm §"Path γ' table" sub-axis C | 15 boards (Jh5c2d ... + 5 additional J-prefix) | ✅ on count |
| ≤2 paired-J variants total in C | resolution §"sub-axis B board-list expansion guidelines" point 3 | 1 paired-J variant (`JcJh4s` from plan; no additional paired-J) | ✅ |
| All 30 boards match plan §3 constraint table | resolution + plan §3 | confirmed via §5 above | ✅ |
| Hero TJ uniform across all 30 | resolution + plan §3 | 30/30 TJ | ✅ |

### SHOULD_FIX-1: Sub-axis C "J as middle card" vs inherited boards (J-as-highest)

**Dispatch text (binding spec):**

`MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md` line 66 sub-axis C:

> The 10 boards from plan §4: `Jh5c2d, Jc8h3s, Jd9c4h, Jh6s3c, Jc7d2s, Jd8c5h, Jh4c2s, Jc9h6d, Jd7h3c, JcJh4s`. **Builder selects 5 additional J-medium parametric flops** matching plan §3 constraint table (**J as the middle card on flop**; non-paired except for the one boundary paired-J variant from plan; rainbow).

And line 95 §"Sub-axis B board-list expansion guidelines" point 3:

> For sub-axis C: **J as middle card on flop**; rainbow; bottom of flop ≥ 2; ≤2 paired-J variants total in C

**Internal contradiction:**

QC inspected each of the 10 inherited plan §4 boards by rank:

| Board | J rank | Other ranks | J position by rank |
|---|---|---|---|
| Jh5c2d | 11 | 5, 2 | **Highest** |
| Jc8h3s | 11 | 8, 3 | **Highest** |
| Jd9c4h | 11 | 9, 4 | **Highest** |
| Jh6s3c | 11 | 6, 3 | **Highest** |
| Jc7d2s | 11 | 7, 2 | **Highest** |
| Jd8c5h | 11 | 8, 5 | **Highest** |
| Jh4c2s | 11 | 4, 2 | **Highest** |
| Jc9h6d | 11 | 9, 6 | **Highest** |
| Jd7h3c | 11 | 7, 3 | **Highest** |
| JcJh4s | 11/11 | 4 | **Highest (paired)** |

**0 of 10 inherited plan §4 boards satisfy "J as middle card on flop."** All 10 have J as the highest rank on the flop. The plan §4's terminology "J-medium flop" did not literally mean "J as middle card" — it appears to have been a loose label for "J-on-board, board has J + low cards" (which is structurally J-high with low secondaries).

QC inspected the builder's 5 additional sub-axis C boards: same J-as-highest pattern (matching the inherited 10's character, not the dispatch's literal "J as middle card" text).

**Net:** 0 of 15 sub-axis C boards satisfy the dispatch's literal "J as middle card" specification. Builder faithfully followed the plan-inheritance half of the dispatch + 5 mirroring; the dispatch's literal text for the additional 5 was unsatisfiable given the inherited 10's character.

### Why this is a real finding (not a re-litigation)

The MW-40 canonical reference is hero `AhTs` on `AJ5r` — `A(14)-J(11)-5(5)`. Here J **is** the middle card (with A as overcard). The dispatch's "J as middle card" specification is the structurally precise restatement of MW-40's canonical board pattern. Sub-axis C's actual boards (J-as-highest, no overcard) do not mirror MW-40's overcard-J-low structure.

Whether this affects the verification's empirical signal at -C labelling is a GTO judgment beyond QC's audit scope (per trigger §"What you do NOT do": "Do NOT make GTO judgments..."). But the literal dispatch-spec compliance is what TC-X-DISPATCH-COMPLIANCE checks, and the answer is: builder followed the plan-inheritance half; the literal "J as middle card" text is unsatisfied.

### Why this is not a BLOCKER

The verification still tests "J-on-board TPMK 4-way checked-through" structurally. Sub-axis A explicitly tests "J-as-highest" (per resolution §"Path γ' table" line 64); sub-axis C with J-as-highest is structurally similar to A but with broader board-character variation (lower secondaries vs higher ones in A). The verification round's primary structural target (J-on-board flips composition) is exercised by all 30 boards regardless of J-as-highest vs J-as-middle distinction.

Treating this as SHOULD_FIX (not BLOCKER) per the audit norm "MILESTONE PR pre-merge audit; surface for orchestrator decision; do not block when verification target is still meaningfully tested."

### Recommended resolution paths (orchestrator decides; QC has no preference)

1. **Ratify** plan/builder interpretation: orchestrator amends `MAIN_TERMINAL_*_RATIFY_*` confirming "J-medium" in plan §4 + resolution comm = "J-on-board, board has J + low secondaries" (informal terminology); proceed to -C labelling on the existing 30. Plan §10 R3 already flagged terminology drift; this would be a similar ratification.
2. **Amend** plan: builder dispatched via `MAIN_TERMINAL_*` to author -B2 PR replacing the 10+5 sub-axis C boards with J-as-middle-card boards (e.g., `AhJc5d`, `KhJc6s`, `AdJh4c`, etc.); -C labelling fires on -B2 merge.
3. **Hybrid**: keep the 10 inherited plan §4 boards (acknowledging plan-inheritance binding); replace only the 5 additional with J-as-middle-card boards (`AhJc5d`-class). 5 of 15 sub-axis C boards then satisfy "J as middle card" literally. Sub-axis becomes character-mixed (10 J-as-highest + 5 J-as-middle).

QC has no preference. Per `feedback_orchestrator_decides_not_recommends.md`, orchestrator selects.

### TC-X-INTRA-PLAN-CONSISTENCY first-activation note

This finding is the **first informal activation of TC-X-INTRA-PLAN-CONSISTENCY** (curative log entry #13, added 2026-05-06 ~22:11 SAST after PR #228 audit gap surfaced via PR #236 builder HALT). The class delivered value on first run:

- The 7-item baseline audit (PASS items 1-7) would have not surfaced this issue — items individually PASS on count + character + integrity.
- TC-X-INTRA-PLAN-CONSISTENCY ("rules R1 ∧ R2 ∧ … simultaneously satisfiable in joint domain") fires on the joint constraint of "inherit 10 plan §4 boards" ∧ "J as middle card" → unsatisfiable since the 10 inherited boards are J-as-highest.
- This same gap was previously expressed in the plan §4 sub-axis B contradiction that surfaced at PR #236 builder HALT; the new class catches the analogous pattern in the dispatch's resolution.

QC continues to apply the class informally; pending owner ratification per `project_river_rats_qc.md` "owner-curated coverage" principle.

## §"Stop conditions" — design-phase

Per amended dispatch §"Stop conditions" (in resolution comm) + plan §"Stop conditions":

- ❌ Pre-flight fails ANY of the 4 checks on first 5 emitted → All 4 PASS (Check 2 = REPORT not FAIL)
- ❌ ref_id collision with 788-corpus or prior 125i → 0 collisions
- ❌ 30-row count not exact → 30/30 emitted
- ❌ Step-18 features non-zero pattern that contradicts plan §5 → 0/30 for both, matches prediction
- ❌ Blocker split = 30/0 expected (REPORT not STOP) → 30/0 uniform; matches Path γ' expectation

## Test classes exercised

- TC-23 spec/infrastructure drift (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (5th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (3rd formal exercise; PASS for builder behavior)** — class continues to validate as durable
- **TC-X-INTRA-PLAN-CONSISTENCY (1st informal activation; SURFACED SHOULD_FIX-1)** — first-run value confirmed
- TC-X-METHODOLOGY-RULE-CROSSCHECK (sub-class; 4-check pre-flight cell-by-cell against Hybrid Path 3 spec)

## Smarter-over-time observation

Curative entry #13 (TC-X-INTRA-PLAN-CONSISTENCY) was added to `~/river-rats-qc/learning/curative_additions_log.md` 1 tick before this audit fired. The class's first activation surfaced a real dispatch-internal contradiction. This is a fast positive validation of the class — closing the loop within the same session that the gap was detected (PR #236 HALT → curative log entry → class activation on next audit).

Both TC-X-DISPATCH-COMPLIANCE and TC-X-INTRA-PLAN-CONSISTENCY remain informal pending owner directive ratification per `project_river_rats_qc.md` operating principle.

## Audit cost / time

- Wall clock: ~14 min (data inspection + script audit + builder report cross-check + dispatch cell-by-cell verification + verdict authoring). Within dispatch estimate (~10-15 min).
- LLM cost: $0 (mechanical Python + git operations).

## Gates

PR #236 cleared from QC side conditional on orchestrator resolving SHOULD_FIX-1. Per amended dispatch §"What gates on this audit":

- 12.5I-MW40-VERIFICATION-C labelling round dispatch — gates on PR #236 merge AND SHOULD_FIX-1 resolution path being clear (otherwise -C labellers evaluate boards that don't match the literal dispatch spec)
- 12.5J-C trainer integration test on 61-surface — parallel queue with -C in builder serial; gates on PR #236 merge

If orchestrator chooses Path 1 (ratify), merge can proceed immediately and -C fires on the 30 J-as-highest boards as committed. If Path 2 or 3, -C waits on -B2 amendment.

## References

- 12.5I-MW40-VERIFICATION-B amended dispatch (Path γ'): `MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md` (master `42460ae`, PR #237)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR236_2026-05-06.md` (master `c028fdb`, PR #238)
- Original -B dispatch (superseded): `MAIN_TERMINAL_PR232_MERGE_AND_MW40B_DISPATCH_2026-05-06.md` (master `d584023`, PR #235)
- Plan source: `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (master `e0e0304`, PR #228) §4 sub-axis C
- HALT query (PR #236 audit-trail): `BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md` (PR #236 first commit `bfdda9f`)
- MW-40 canonical reference: `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md` MW-40 row (J as middle card on `AJ5r`)
- Curative log: `~/river-rats-qc/learning/curative_additions_log.md` entry #13 (TC-X-INTRA-PLAN-CONSISTENCY, added 2026-05-06 ~22:11)
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `project_river_rats_qc.md` (owner-curated coverage)

**Status: VERDICT = PASS. PR #236 cleared for merge from QC side, conditional on orchestrator resolving SHOULD_FIX-1 (sub-axis C dispatch-internal contradiction). 24th solo QC cycle. TC-X-INTRA-PLAN-CONSISTENCY first informal activation — class delivered first-run value.**
