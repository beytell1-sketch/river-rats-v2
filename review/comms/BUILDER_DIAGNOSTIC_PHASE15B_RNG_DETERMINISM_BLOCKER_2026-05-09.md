---
date: 2026-05-09
from: LEAD-PROGRAMMER (programmer-hat with architect-hat STOP-condition consult)
to: Main terminal (orchestrator) · Owner · QC stream (FYI)
re: Phase 1.5-B — STOP CONDITION on §2.3 bit-equality gate (Monte Carlo equity non-determinism); architect-hat consult requesting scope-expansion authorization
status: BLOCKED — architect-hat consult exercised; awaits orchestrator scope-expansion authorization
---

# Phase 1.5-B — STOP CONDITION: §2.3 bit-equality gate cannot pass via re-extract

## Summary

Phase 1.5-B execution paused at Step 2 (extractor self-test smoke test). Re-extract path produces non-bit-equal output to (column-drop reference) on Monte Carlo equity-derived features. §2.3 binding gate requires EMPTY diff — currently produces non-empty diff by design (~4 keys per row mismatch on equity-related features).

This is a STOP condition per CLAUDE.md §5 and dispatch §"BINDING gate". Per dispatch protocol, NO improvisation; surfacing for architect-hat consult + orchestrator scope-expansion authorization before proceeding.

## Branch state

- Branch: `programmer/phase15b-feature-prune-2026-05-09` (head not yet pushed beyond Step 1 source mutations)
- Step 1 (source mutation): COMPLETE; pytest river-rats-core/tests/test_train_model_v9_student.py PASSES with 59-surface assertions; pre-existing test failures (4) are unrelated to this PR (they fail at master too — they expect FEATURE_COLUMNS == 55 which the experimental student surface has never matched).
- Step 2 (smoke test): FAILED on bit-equality of equity-derived features (see §Empirical evidence below).
- Steps 3-4: NOT STARTED.

## Empirical evidence

Smoke test on row 0 of `data/corpus_combined_988_2026-05-07.jsonl` (PILOT_001 — BB hero with 7h7s on 4c7d5s board, 2 opponents, no facing bet). Hand-dict reconstructed from row's raw fields per the established pattern at `scripts/reextract_pilot_100_features.py:100-145`. RNG seeded with `random.seed(42)` before `extract_all_features()` call.

Result: 4 of 59 keys mismatch the source feat_dict (subset to 59 retained keys):

| key | source feat_dict | re-extract output | delta |
|---|---|---|---|
| `raw_equity` | 0.82725 | 0.828 | +0.00075 |
| `equity_vs_range` | 0.82725 | 0.828 | +0.00075 |
| `equity_margin` | 0.82725 | 0.828 | +0.00075 |
| `board_adjusted_hrp` | 0.822641 | 0.823386 | +0.000745 |

Other 55 of 59 keys match exactly (zero delta).

## Root cause

`extract_all_features` invokes Monte Carlo equity calculation (`river-rats-core/feature_extractor.py:1113-1170` and friends — uses `random.random()` and `random.sample()`). MC trials default to 2000 (training; per docstring at line 1129).

The architect-hat design memo §2.1 anticipated this and explicitly noted the dependency:

> "Therefore (re-extract-to-61 → column-drop-2-cols) IS bit-equal to (re-extract-to-59-from-modified-extractor) **— modulo identical RNG seeds in equity computation, which `extract_features_parallel.py` controls.** So column-drop would produce a numerically identical corpus."

`extract_features_parallel.py` controls RNG seeding for fresh extractions from raw gauntlet JSON (initial pipeline). However, the 988-corpus's `feat_dict` values were produced by upstream extraction whose RNG seed is NOT preserved in the corpus rows. Re-running `extract_all_features` with any seed (including matching `random.seed(42)`) cannot reproduce the MC sample sequence the upstream run used unless we know the upstream's exact seed AND processing order — neither is preserved.

Therefore §2.3 bit-equality gate is incompatible with re-extract for THIS corpus, by design of MC equity calculation. The architect-hat design memo §2.1 implicitly relied on assumed RNG-seed preservation that does not hold.

## Architect-hat verdict (single committed path)

**Switch to column-drop for Phase 1.5-B execution.**

Reasoning:

1. **§2.1 architect commitment itself notes column-drop bit-equivalence:** "Therefore (re-extract-to-61 → column-drop-2-cols) IS bit-equal to (re-extract-to-59-from-modified-extractor)... So column-drop would produce a numerically identical corpus."
2. **§2.3 binding gate requires empty diff:** column-drop is the only path that reliably achieves it for this migration.
3. **Future-proofing benefit preserved as a pattern:** the architect's stated motivation for re-extract was forward-looking — establishing re-extract as the migration pattern so we never have to audit "is this drop append-only-pure" for future feature changes. That pattern can be locked in via memory or process-guide addendum WITHOUT requiring this specific migration to be re-extract — for THIS migration where J-B is provably append-only-end-of-pipeline (verified by reading `feature_extractor.py:2645-2663`), column-drop produces the verified-correct artifact.
4. **Quality discipline preserved:** column-drop here is NOT a shortcut — it is the methodologically-correct path because:
   - Step 18 J-B compute fns at `feature_extractor.py:2136-2171, 2174-2223` were verified at master `465e6fa` to be append-only-end-of-pipeline (read existing feature values; no downstream feature reads them).
   - Steps 1-17 are unmodified by Phase 1.5-B; their outputs are unchanged.
   - The 988-corpus's feat_dict (with 61 keys) is the verified output of running extract_all_features with Steps 1-18 active. Removing the 2 J-B keys yields exactly the output we'd get from extract_all_features with Steps 1-17 only (= post-J-B-drop extractor).
5. **Re-extract WITH the broken bit-equality gate would be worse than column-drop:** non-empty diff on equity features would force either (a) weakening the gate to exclude equity-derived features (loses verification fidelity), or (b) declaring re-extract output as authoritative and accepting Monte Carlo noise vs source (changes ~4 features per row by ~0.001 per equity column, rippling into all downstream training that uses these features — silent training-data drift on the 988-corpus, exactly the kind of issue `feedback_solver_findings.md` warns against).

## Scope-expansion request to orchestrator

Per dispatch §"BINDING gate" + `feedback_queries_to_orchestrator.md`, requesting orchestrator scope-expansion authorization to deviate from §2.1 architect commitment (re-extract) to **column-drop** for Phase 1.5-B execution.

Specific deviation:

- §2.2 Step 3 changes: instead of re-running `extract_all_features` on raw situations, take each row's existing feat_dict and remove the 2 J-B keys; emit new corpus row with 59-key feat_dict.
- §2.3 verification: simplifies — both sides of the diff are produced by the same column-drop operation; gate trivially passes (still run the diff command for provenance + as a sanity check that no other keys were inadvertently dropped).
- §2.1 narrative remains in master; this deviation is documented in 1.5-B PR's builder report and a memory-rule update is recommended for Phase 1.6+ feature changes.

Alternative paths the orchestrator could direct:

- **(α) Approve column-drop deviation** (architect-hat recommended; this comm requests).
- **(β) Direct re-extract with weakened gate**: redefine §2.3 to "all non-equity-derived features bit-equal; equity-derived features within MC tolerance ε per row." Architect-hat does NOT recommend — adds complexity, weakens verification, ε is unprincipled.
- **(γ) Direct re-extract from earliest-upstream raw gauntlet inputs** with seed-controlled extraction: requires re-running the entire upstream pipeline (gauntlet → extract → assemble) end-to-end with controlled RNG. Significant scope expansion (~hours-to-day of work + dependency on legacy v2.3 pipeline files at REPO ROOT noted in §1.2 path-corrections). Not recommended — disproportionate cost for a feature-prune migration.

## Methodology compliance

- **No improvisation per dispatch + CLAUDE.md §5:** stopped immediately on smoke-test failure; documented; surfacing for authorization. Did NOT proceed to Step 3.
- **Single committed path per `feedback_quality_default_no_ask.md`:** architect-hat verdict is column-drop; no menu.
- **Surface-don't-pre-empt per `feedback_orchestrator_decides_not_recommends.md`:** orchestrator decides scope-expansion authorization; owner ratifies if material to design-spec.
- **Verify-source-not-plan per `feedback_verify_source_not_plan.md`:** read `feature_extractor.py` MC equity code path before asserting RNG dependency; ran empirical smoke test before declaring blocker.

## What's needed to unblock

One of:
- **Orchestrator dispatch comm authorizing path α (column-drop deviation).** ~5-10 min builder turnaround to complete Steps 3-4 + bit-equality verification + PR.
- **Orchestrator dispatch comm directing path β or γ.** Builder re-aligns to directed path.

This BLOCKER is also surfaced to owner for awareness given this is the first execution sub-phase of Phase 1.5; how the orchestrator/owner choose to handle this path-resolution will set precedent for Phase 1.5-C/D/E.

## References

- Phase 1.5-B dispatch: `MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` (master `9491965`, PR #314)
- Architect's design memo §2.1 (committed to master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Architect's design memo §2.3 binding-gate command: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Source under review: `river-rats-core/feature_extractor.py:1113-1170` (MC equity); `:2136-2223` (J-B compute fns; verified append-only)
- Pattern reference: `scripts/reextract_pilot_100_features.py:100-145` (corpus-row → hand_dict remap)
- Memory rules: `feedback_quality_default_no_ask.md`, `feedback_solver_findings.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_queries_to_orchestrator.md`, `feedback_explicit_action_trigger.md`

---

**Status: Phase 1.5-B BLOCKED at Step 2 smoke-test. Architect-hat verdict: column-drop deviation from §2.1. Awaits orchestrator scope-expansion authorization (path α / β / γ). Source mutations from Step 1 are committed-locally-not-pushed; will hold or roll forward depending on directed path.**
