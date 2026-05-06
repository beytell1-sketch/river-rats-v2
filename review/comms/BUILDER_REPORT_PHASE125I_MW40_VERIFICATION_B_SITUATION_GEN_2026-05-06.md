---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5I-MW40-VERIFICATION-B (Path γ' amended scope) — 30 J-on-board variants emitted; Hybrid pilot-first 4-check PASS on first 5; stop conditions clear
status: complete; PR opens for QC audit
branch: programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06
base: master `42460ae` (post-PR #237 Path γ' resolution merge)
---

# Phase 12.5I-MW40-VERIFICATION-B — situation generation (Path γ' amended)

## Headline

| Step | Result |
|---|---|
| Path γ' compliance | ✅ 15/0/15 sub-axis split (A: 15, B: dropped, C: 15); hero TJ off-suit uniform; blocker_variant uniform `with_J_blocker` |
| Hybrid pilot-first 4-check on first 5 | ✅ PASS (all 4 checks); see §"Pre-flight 4-check on first 5" below |
| Total emitted | ✅ 30/30 |
| Sub-axis distribution | ✅ A:15 / C:15 (B dropped per Path γ') |
| Hero-hand class | ✅ TJ off-suit uniform (29 TPMK + 1 trips on the JcJh4s paired-J boundary explicitly sanctioned by plan §4) |
| ref_id namespace | ✅ `PILOT_MW40_VERIF_001..030` exact; 0 collisions vs 1476 existing ref_ids (788-corpus + prior 125i) |
| Schema integrity | ✅ 30/30 rows × 61 keys; **0 NaN / 0 Inf** across 1830 feat_dict values |
| Step-18 activation rates | ✅ 0/30 for both (`nut_blocker_overcard_count` + `bet_call_multiway_oop_raise_pressure_index`); matches plan §5 prediction (≈0) |
| design_action discipline | ✅ CHECK uniform across all 30 |
| Stop conditions | ✅ none triggered; full record §"Stop conditions" |

**Cost:** ~$0 (deterministic factory; no LLM calls). **Time:** ~22 min builder including HALT-resolution branch reuse + 5-board selection per sub-axis.

## §"Pre-flight 4-check on first 5" (Hybrid pilot-first per PR #228 SHOULD_FIX-1 Path 3)

Pre-flight ran on situations PILOT_MW40_VERIF_001..005 BEFORE emitting the remaining 25. Result per check:

```
=== Hybrid pilot-first 4-check pre-flight on first 5 emitted ===
  Check 1 PASS: 5 rows × 61 keys; 0 NaN/Inf
  Check 2 REPORT: Step-18 activations on first 5 — 
    nut_blocker_overcard_count=0/5,
    bet_call_multiway_oop_raise_pressure_index=0/5
    (plan §5 predicted ≈0 for both)
  Check 3 PASS: 5 ref_ids in PILOT_MW40_VERIF_* namespace; 0 collisions
  Check 4 PASS: 5 rows × 5 structural fields all match plan §3
=== Pre-flight PASS — proceeding with remaining 25 situations ===
```

| Check | Spec | Result |
|---|---|---|
| 1 — Schema parity | 61-surface uniform; 0 NaN/Inf | ✅ PASS (5 × 61 = 305 values; 0 NaN/Inf) |
| 2 — Step-18 plausibility | Both features ≈ 0 across J-on-board variants | ✅ REPORT (0/5 for both; matches prediction; per amended dispatch §"Stop conditions" Step-18 is REPORT not STOP) |
| 3 — ref_id namespace | All 5 in `PILOT_MW40_VERIF_001..005`; no collisions | ✅ PASS (0 collisions vs 1476 existing ref_ids) |
| 4 — Top-level structural fields | All 5 match plan §3 (hero_position=BTN, street=flop, num_opponents=3, facing_bet=False, to_call=0.0) | ✅ PASS (5 × 5 = 25 field-checks all match) |

## §"Sub-axis distribution" (Path γ' 15/0/15)

| Sub-axis | Count | Boards |
|---|---|---|
| **A — J-high flop, TPMK on top of J-high** | **15** | Js9c5h, Js7d3c, Js8h4d, Js9d2c, Js8c4h, Js7h2d, Js9h3c, Js6d4s, Js9c3d, Js7c5d (10 from plan §4) + **Js8d3h, Js9c4d, Js7c4d, Js9h6c, Js8d2c (5 fresh per dispatch §"Sub-axis B board-list expansion")** |
| **B — DROPPED** | **0** | (per Path γ' resolution; future-J-expectation stress-test deferred to follow-up phase) |
| **C — J-medium flop / set-of-Js boundary** | **15** | Jh5c2d, Jc8h3s, Jd9c4h, Jh6s3c, Jc7d2s, Jd8c5h, Jh4c2s, Jc9h6d, Jd7h3c, JcJh4s (10 from plan §4 — JcJh4s is the 1 J-paired boundary) + **Jh7s3d, Jc8d4h, Jh6d2c, Jd5h3c, Jc7h4d (5 fresh per dispatch §"Sub-axis B board-list expansion"; all single-J non-paired; ≤2 paired-J variants total in C ≤ requirement satisfied — only 1 paired)** |

### Builder-selected 5 fresh per sub-axis — design rationale

**Sub-axis A (J-high; rainbow; 7-9 secondary):**

| ref_id | Hero | Board | Secondary | Rationale |
|---|---|---|---|---|
| PILOT_MW40_VERIF_011 | TcJd | Js8d3h | 8 | rainbow, sec=8, low=3; matches plan §3 constraint table; not in plan §4 list |
| PILOT_MW40_VERIF_012 | ThJc | Js9c4d | 9 | rainbow, sec=9, low=4 |
| PILOT_MW40_VERIF_013 | ThJc | Js7c4d | 7 | rainbow, sec=7, low=4 |
| PILOT_MW40_VERIF_014 | TdJc | Js9h6c | 9 | rainbow, sec=9, low=6 |
| PILOT_MW40_VERIF_015 | ThJc | Js8d2c | 8 | rainbow, sec=8, low=2 |

**Sub-axis C (J-medium; rainbow; non-paired; bottom ≥ 2):**

| ref_id | Hero | Board | Rationale |
|---|---|---|---|
| PILOT_MW40_VERIF_026 | TcJd | Jh7s3d | rainbow, J-high, non-paired |
| PILOT_MW40_VERIF_027 | TsJh | Jc8d4h | rainbow, J-high, non-paired |
| PILOT_MW40_VERIF_028 | TsJd | Jh6d2c | rainbow, J-high, non-paired |
| PILOT_MW40_VERIF_029 | TsJh | Jd5h3c | rainbow, J-high, non-paired |
| PILOT_MW40_VERIF_030 | TsJd | Jc7h4d | rainbow, J-high, non-paired |

T-kicker pinned (TJ uniform); no adjacent-kicker control variants per dispatch §"Sub-axis B board-list expansion guidelines" point 5.

## §"Blocker distribution" (Path γ' uniform)

All 30 variants: hero TJ off-suit → hero holds 1 J → uniform `with_J_blocker = 1`.

- `with_J_blocker`: 30/30
- `no_J_blocker`: 0/30

Per amended dispatch §"Stop conditions": "Blocker split = 30/0 (uniform with-J-blocker) is the expected outcome; no STOP on this condition; report to confirm." ✅ Confirmed.

Blocker-effect-sensitivity test (`feedback_solver_findings.md` finding 2) is deferred to a follow-up phase per Path γ' decision rationale.

## §"Step-18 activation prediction" (vs observed)

| Step-18 feature | Plan §5 predicted | Observed (full 30) | Observed (first 5) |
|---|---|---|---|
| `nut_blocker_overcard_count` | ≈ 0 (hero IP, no nut-FD blocker semantics on J-on-board) | 0 / 30 (= 0%) | 0 / 5 |
| `bet_call_multiway_oop_raise_pressure_index` | ≈ 0 (hero IP not OOP) | 0 / 30 (= 0%) | 0 / 5 |

Both Step-18 features show exactly the predicted activation pattern (0/30 active across all variants). No attention flag triggered per `feedback_attention_flags_when_features_change.md`. Pre-flight Check 2 REPORT confirmed this on first 5 before remaining 25 emitted.

## §"Schema integrity"

```
30 / 30 rows × 61 feat_dict keys = 1830 values
NaN count:  0
Inf count:  0
NaN+Inf rate: 0.0000% (well below 1% STOP threshold)
```

61-surface uniform across all 30 rows (post-PR #205 surface). `feat_dict` constructed via canonical `feature_extractor.extract_all_features` (read-only import; no `river-rats-core/` modifications).

### Hand-class distribution observation (per amended dispatch — REPORT, not STOP)

| `hand_category` | Count | Rows | Note |
|---|---|---|---|
| 6 (TP medium kicker) | 29 / 30 | All sub-axis A + sub-axis C single-J variants | Plan §3 expected; mirrors MW-40 reference (AhTs on AJ5r → pair-of-A T-kicker → TPMK) but with pair-of-J T-kicker on J-on-board |
| 11 | 1 / 30 | PILOT_MW40_VERIF_025 (board JcJh4s, hero ThJd) — three Js (trips) | Plan §4 sub-axis C explicit: "JcJh4s (last is J-paired flop — extreme test case where set-of-Js composition spikes; included as 1 boundary variant)". Hero TJ + 2 board Js = trips. Not TPMK; expected boundary deviation |

**Why this is not a STOP:** the amended dispatch's stop conditions do not include "hand_category=6 uniform". The plan §4 explicitly sanctioned the JcJh4s boundary variant as "extreme test case where set-of-Js composition spikes". Hero TJ on a paired-J board necessarily produces trips (not TPMK); this is the design's deliberate choice to test composition behaviour at the boundary. design_action remains CHECK (slowplay-trips on paired-board commonly checks too) and Step-18 features remain 0/0 on this row.

## §"ref_id namespace"

```
ref_id range: PILOT_MW40_VERIF_001 ... PILOT_MW40_VERIF_030
All 30 in PILOT_MW40_VERIF_* namespace: ✓
Within-set duplicates: 0
Collisions vs 788-corpus + prior 125i (1476 existing ref_ids): 0
```

Disjoint namespace by construction (`PILOT_MW40_VERIF_*` is a fresh prefix; existing ref_ids use `PILOT_NNN`, `t8primeR_*`, `t9primeE_*`, `t10primeR_*`, etc.).

## §"Stop conditions" (full record)

Per amended dispatch (PR #237 resolution):

| Condition | Triggered? | Evidence |
|---|---|---|
| Pre-flight fails ANY of the 4 checks on first 5 emitted | NO | All 4 checks PASS (Check 2 = REPORT, not FAIL) |
| ref_id collision with 788-corpus or prior 125i ref_ids on full 30 | NO | 0 collisions vs 1476 existing |
| ≥1% NaN/Inf across 30 × 61 = 1830 feat_dict values | NO | 0 NaN, 0 Inf |
| **Sub-axis split not exactly 15/0/15** (amended) | NO | 15/0/15 exact |
| **Blocker split = 30/0 expected** (amended; REPORT not STOP) | n/a | 30/0 uniform; matches Path γ' expectation |
| Step-18 features non-zero pattern that contradicts plan §5 | NO | 0/30 for both; matches prediction exactly |
| design_action ≠ CHECK on any emitted situation | NO | CHECK uniform across all 30 |

## §"Files in PR diff"

3 files in PR diff:

1. `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (30 rows; 61-surface; full schema per `emit_row` precedent + Path γ' metadata fields)
2. `scripts/build_corpus_revision_125i_mw40_verif_situations.py` (factory script; mirrors `build_corpus_revision_125i_situations.py` precedent; includes inline pre-flight 4-check)
3. `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md` (this report)

## §"What I did NOT do" (per dispatch §"What you do NOT do")

- ❌ Did NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md` untouched)
- ❌ Did NOT modify `river-rats-core/` source (read-only import of `feature_extractor.extract_all_features` only)
- ❌ Did NOT modify BATCH2 reference (orchestrator-scope; locked until -E)
- ❌ Did NOT touch existing 788-corpus or any prior-phase corpus files
- ❌ Did NOT label any hands (12.5I-MW40-VERIFICATION-C scope)
- ❌ Did NOT run any LLM inference (deterministic factory; LLM is at -C)
- ❌ Did NOT skip the 4-check pre-flight (Hybrid pilot-first binding per PR #228 SHOULD_FIX-1 Path 3 resolution; ran in `_preflight_4check` before emitting beyond 5)
- ❌ Did NOT auto-fix NIT-1 (terminology drift) or NIT-2 (5th stop condition placement) from PR #228 audit (carry-forward to -E per orchestrator)
- ❌ Did NOT add adjacent-kicker control variants (T-kicker pinned uniformly per dispatch §"Sub-axis B board-list expansion guidelines" point 5)
- ❌ Did NOT exceed ≤2 paired-J variants in sub-axis C (only 1 — JcJh4s; the 5 fresh additions are all single-J non-paired)
- ❌ Did NOT modify the merged plan PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md (orchestrator-scope; PR #237 resolution amends the dispatch, not the plan)

## What's blocked / what's queued

**Cleared by this PR (after merge):**
- 12.5I-MW40-VERIFICATION-C labelling round dispatch (5 Sonnet × 30 hands; pilot-first 5-hand × 5-Sonnet gate per `feedback_pilot_first_for_long_jobs.md` for LLM-uncertainty mitigation)
- 12.5J-C trainer integration test on 61-surface (parallel queue; orchestrator decides interleave order)

**Awaiting orchestrator dispatch:**
- Decision on which fires first after this merge: -C labelling round OR 12.5J-C trainer integration test

## References

- Resolution comm (Path γ' selection): `MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md` (master `42460ae`, PR #237)
- Original -B dispatch: `MAIN_TERMINAL_PR232_MERGE_AND_MW40B_DISPATCH_2026-05-06.md` (master `d584023`, PR #235)
- HALT query (this PR's prior commit): `BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md` (commit `bfdda9f` on this branch)
- Plan (authoritative; merged at PR #228): `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (master `e0e0304`)
- 12.5I-B factory precedent: `scripts/build_corpus_revision_125i_situations.py` (master `994ae67`)
- 12.5E-B factory primitives: `scripts/build_corpus_revision_125e_situations.py` (`emit_row`, `build_hand_dict`)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md` (Path γ' selected by orchestrator after builder offered α/β/γ), `feedback_pilot_first_for_long_jobs.md` (Hybrid 4-check working as intended both at HALT-detection and at code-level pre-flight), `feedback_attention_flags_when_features_change.md` (Step-18 0/30 matches prediction exactly), `feedback_explicit_action_trigger.md` + `feedback_optional_is_not_authorized.md` (HALT was correct posture; resumed only on PR #237 fire-now), `feedback_named_author_builds_not_polls.md` (named-author execution per amended dispatch), `feedback_shared_tree_commit_hygiene.md` (pre-flight git status before commit)

**Status: 12.5I-MW40-VERIFICATION-B (Path γ' amended scope) complete. 30 J-on-board variants emitted; Hybrid pilot-first 4-check PASS; all stop conditions clear. PR opens for QC audit per amended dispatch §"QC stream — what you audit". Builder ready for orchestrator's next dispatch (12.5I-MW40-VERIFICATION-C labelling round OR 12.5J-C trainer integration test) on this PR's merge.**
