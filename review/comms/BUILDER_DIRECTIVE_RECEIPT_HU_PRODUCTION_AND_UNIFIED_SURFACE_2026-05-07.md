---
date: 2026-05-07
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner (FYI) · QC stream (FYI)
re: Owner directive received during 12.5L owner-gate hold — HU production-readiness + unified feature surface across the chain + drop the 2 J-B features
status: DIRECTIVE-RECEIPT — surfaces owner-scope decision to orchestrator for sequencing; builder HOLDS execution pending orchestrator MAIN_TERMINAL_* dispatch
---

# Owner directive — HU production + unified feature surface

## §1 What the owner said

Owner (verbatim, with my parsed reading in brackets):

> "we ne[e]d[s] [HU] ready, am[d] it needs to run off the same feature sets. minus 2 new features that should be cu[t]e [→ "cut"]. this will allow consist[ent] teaching through[]put that pulls from features."

## §2 Builder's parsed reading

The owner-scope decision (per `feedback_orchestrator_decides_not_recommends.md`: owner decides WHAT/WHETHER):

1. **HU must reach production-readiness on equal evidentiary footing with the multiway model.** Today: v8 HU is FROZEN at 38-feature surface; 88.1% PokerBench aggregate accuracy; only 4 of 40 reference hands are HU; no HU-specific solver-corrected reference set exists. Owner directive: HU must be brought to the same evidentiary state as v9-3way-v2.2 (per-hand solver-corrected reference set + per-hand stay-wrong tracking).
2. **Unified feature surface across the progressive chain.** Today: v8 HU 38-feat / v9-3way-v2.2 45-feat / 12.5K experimental 61-feat — three different surfaces. Owner directive: ONE surface, used by all (HU, 3-way, 4-way, 5-way).
3. **Drop the 2 J-B features** added in 12.5J-B (PR #198 area):
   - `nut_blocker_overcard_count` — designed for MW-17 axis; chosen-seed importance 0.0091 (below 1% drop threshold)
   - `bet_call_multiway_oop_raise_pressure_index` — designed for MW-47 axis; chosen-seed importance 0.0076 (below 1% drop threshold)
   Both targeted axes (MW-17, MW-47) remained on the stay-wrong list through 12.5K. They cost surface complexity for no measurable lift.
4. **Reason / why**: coaching pipeline pulls feature-level explanations downstream as part of the teaching loop. If HU's feature set differs from multiway's, the coach narrative fragments per opponent count. A unified surface enables consistent feature-grounded coaching regardless of HU/3-way/4-way context.

**Net target surface**: 59 features = 61-current-experimental MINUS 2 J-B features. Then unified across HU + 3-way + (future) 4-way + 5-way.

## §3 Implications — what touches what

This is a multi-week scope with branched dependencies. Surfacing for orchestrator sequencing — NOT prescribing one:

| Workstream | Dependency | Approximate scope |
|---|---|---|
| HU reference set | independent | Design ~30-40 HU postflop spots; 5-labeller v3.4 consensus; canonical actions; mirror MW-11–50 design pattern |
| Feature-prune (drop 2 J-B) | independent | `feature_extractor.py` + `feature_keys.py`: remove 2 functions + columns; 61 → 59; trainer surface bump 61 → 59; invariant tests re-baseline; corpus re-extraction (mechanical via composite removal) |
| HU reference evaluation | needs HU ref set | Run v8 HU (38-feat) against new HU ref set; identify HU stay-wrong hands; assess the ~88.1% claim against per-hand canonical |
| HU model retrain on 59-surface | needs feature-prune + HU corpus | New v8-or-vNext-HU model; warm-start strategy needs decision (warm-start from where if surface changes 38 → 59?); HU corpus needs assembly (analogous to 988-corpus for 3-way; today HU side has only PokerBench rows, not labelling-pipeline labels) |
| Re-baseline 3-way on 59-surface | needs feature-prune | Re-train v9-3way analog on 59-surface; verify no regression vs current 988-corpus 33.00/40 ± 0.00 ceiling at the new surface size |
| Coaching pipeline alignment | needs unified 59 + HU model | Downstream consumer; depends on the chain stabilizing on 59-surface across all opponent counts |
| Progressive chain extension (v9-4way, v9-5way) | needs all of above | Stalls until HU + 3-way are on 59-surface; this is exactly what Option C of the 12.5L synthesis would have advanced |

## §4 Sequencing options for orchestrator (NOT decisions — surfacing)

Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator decides sequencing. Three plausible orderings I see, surfaced for orchestrator weighing:

- **Order 1 — HU-reference-set-first**: HU ref set → drop 2 features → re-baseline 3-way on 59 → HU corpus (if needed) → HU retrain on 59 → progressive chain extension. Risk: HU labelling work is the longest-lead and not yet started; pushes HU production-ready longest.
- **Order 2 — Feature-prune-first**: Drop 2 features + re-baseline 3-way on 59 (verify no regression) → HU ref set → HU corpus → HU retrain on 59. Risk: re-baselines 3-way before HU work begins; smaller scope items first.
- **Order 3 — Parallel HU-ref-set + feature-prune**: HU ref set design + feature-prune kick off in parallel; converge at HU retrain. Risk: orchestrator must coordinate two streams; current team structure is single-builder so parallel = sequential anyway.

I do NOT recommend a sequencing here — that's orchestrator-scope. I'm surfacing the dependency graph so orchestrator has the data to decide.

## §5 What I am NOT doing (per `feedback_optional_is_not_authorized.md` + `feedback_explicit_action_trigger.md`)

- ❌ NOT executing any of the workstreams in §3 — there is no fire-now dispatch from orchestrator naming me on a specific PR/commit for HU/feature-prune/etc.
- ❌ NOT picking a sequencing order — orchestrator-scope.
- ❌ NOT re-opening the 12.5L synthesis (it stands; this directive is a NEW phase that supersedes the 12.5L Option-A SHIP-as-is sketch and effectively chooses something between 12.5L Option B and Option C).
- ❌ NOT shipping anything from this branch beyond this directive-receipt comm.

## §6 What I AM doing

- Authoring this directive-receipt comm so orchestrator has clear visibility into the owner's decision.
- Committing + pushing + opening PR for orchestrator to ratify or amend.
- Holding loop ticks at "no fire-now dispatch" posture until orchestrator dispatches a phase plan.

## §7 Files in PR diff

- `review/comms/BUILDER_DIRECTIVE_RECEIPT_HU_PRODUCTION_AND_UNIFIED_SURFACE_2026-05-07.md` (this comm)

Single-file directive-receipt; no code/data changes.

## §8 Relationship to 12.5L synthesis

This directive supersedes the 12.5L Option-A SHIP recommendation. The owner has effectively decided:
- NOT Option A pure (because Option A locks v9-3way-v2.2 + 988-corpus + 61-surface as production; this directive requires changes to the surface and an unbuilt HU artefact).
- Closer to Option B (different stack work) + Option C (progressive chain extension) hybrid: drop 2 features + bring HU online + re-baseline + extend chain.
- The 3-lever ceiling claim in 12.5L synthesis remains valid for the 61-surface — it does NOT preclude this owner-directed 59-surface unification.

The 12.5L synthesis comm + 988-corpus + chosen-median-seed model artefact remain in master as the empirical record of the 12.5K experiment. They do not need to be reverted.

## §9 References

- 12.5L synthesis: `review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` (master `ad84d78`, PR #297)
- 12.5J-B 2-feature implementation: `review/comms/BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md`
- Feature importance (chosen Seed 2 of 988-corpus): `review/comms/BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` §"Section C — Gate 2.3 feature importance"
- v8 HU model: `river-rats-core/models/gto_model_v8_hu.json` (FROZEN; 38-feature)
- Oracle router: `river-rats-core/oracle_router.py`
- Reference set: `river-rats-core/reference_evaluator.py` (40 hands; 4 HU + 24 3-way + 12 4-way; designed in `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`)
- Master plan progressive chain: `docs/PROGRESSIVE_MODEL_CHAIN.md`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_queries_to_orchestrator.md`, `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`

---

**Status: Owner directive received during 12.5L owner-gate hold. Surfaced to orchestrator for sequencing. Builder HOLDS at "no fire-now dispatch" posture per `feedback_explicit_action_trigger.md` until orchestrator MAIN_TERMINAL_* dispatch names a specific phase + PR/commit.**
