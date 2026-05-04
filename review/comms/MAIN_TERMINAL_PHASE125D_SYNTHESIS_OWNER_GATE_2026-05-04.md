---
date: 2026-05-04
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream · GTO-EXPERT · ML-ARCHITECT
re: Phase 12.5D gate FAIL — three expert findings synthesized; owner WHAT decision (A/B/C/C') ready
status: SYNTHESIS — owner gate
---

# Phase 12.5D — three-expert synthesis for owner WHAT decision

QC, gto-expert, and ml-architect findings landed. Strong convergence on root cause and mitigation. Owner gate is now informed.

## Convergence headline

Both gto-expert and ml-architect independently identified the **same root cause** for 7 of 9 student misses on the reference set: **class-prior collapse from confidence-only weighting** on a corpus skewed toward CHECK (245/494 rows = 50%). gto-expert calls it "class-prior collapse on aggressive labels {BET, RAISE}"; ml-architect quantifies it as "3.9× passive bias under pure confidence weighting" (passive {CHECK+CALL+FOLD} ≈ 342 gradient mass vs aggressive {BET+RAISE} ≈ 88).

The held-out confusion matrix confirms one-way collapse: **3 BET→CHECK, 3 RAISE→CALL, zero in the opposite direction**. RAISE is the most visibly collapsed because its support is smallest (29 rows), but BET is also under-firing.

This means **a RAISE-only mitigation (Direction C as originally framed = ml-architect §11 R-2 option C in isolation) leaves 4-5 of 7 in-family failures on the table.** The mitigation must address the broader passive→aggressive collapse, not just RAISE.

## Three findings — full

### Finding 1 — Schema discoveries (handled in-module per Path Y)

**1a — Blueprint join-key defect.** Blueprint §6 cited `corpus.source_situation_id == labels.ref_id`; verified on row 1 only. Empirical join cardinality on 494 rows = **100/494**. Cohort 2 (rows 100-493) uses corpus `situation_id` like `monster_003`/`nfd_028`/`magg_006` while labels carry `ref_id=PILOT_###` — zero overlap on the original key. Builder's switch to `pilot_hand_id == pilot_hand_id` recovers 494/494.

ml-architect root cause (Q1): **bad spec inheritance from PR #110**. ml-architect §12 verified row 1 only; PR #122 §6 inherited and re-cited row 1; both pre-flight passes were defeated by N=1.

**Protocol amendment proposed by ml-architect:** any blueprint citing a join key must (a) verify on at least 5 sample rows spanning the file, AND (b) compute and report empirical join cardinality before approval. If ratio < 0.99 → STOP-class question, not a verified premise.

**1b — In-module `_StudentInference` mirror.** Builder added `_StudentInference` + `_evaluate_student_one_hand` inside the trainer module to handle 59-feature inference (Path Y forbids extending `gto_model.FEATURE_COLUMNS`).

ml-architect verdict (Q2): **methodologically sound for the 12.5D one-shot, but creates permanent silent-drift risk** if `reference_evaluator._evaluate_one_hand` is updated and the mirror isn't. No import dependency to remind future editors.

**Mitigation proposed by ml-architect (Option α invariant test):** build a `_StudentInferenceLike45` shim, run all 40 MW hands through both the canonical `_evaluate_one_hand(GtoOracle(baseline_45))` and `_evaluate_student_one_hand(_StudentInferenceLike45(baseline))` with `STUDENT_FEATURE_COLUMNS_V9[:45]`, assert identical `(adjusted_action, correct, was_adjusted)`. Any drift flips at least one hand. ~1 test, low surface.

### Finding 2 — Mixed-direction miscalibration (NOT just RAISE collapse)

gto-expert per-hand verdict (Q1): **ONE shared root cause for 7/9 failures + 1 distinct cause for 2/9**.

| ref_id | failure | cause |
|---|---|---|
| MW-17 | CALL→FOLD | shared (passive collapse, same family) |
| MW-24, 25, 40, 42 | BET→CHECK ×4 | shared (passive collapse) |
| MW-45, 47 | RAISE→CALL ×2 | shared (passive collapse) |
| MW-31 | FOLD→CALL | distinct (no feature for villain check-raise credibility in MW pot) |
| MW-46 | CALL→RAISE | distinct (no feature for villain check-raise river-action credibility) |

The 7 shared failures are addressable by class-balanced weighting. The 2 distinct failures (MW-31, MW-46) are a feature-surface gap — the trainer/migration was never going to fix them. Acknowledging this is important: even a perfect mitigation closes ~7 of the 31→33 gap, not all of it.

### Finding 3 — P1 blockers H2 confirmed (features not load-bearing on this corpus)

gto-expert verdict (Q2): **H2** (features are real poker concepts but reference set's RAISE/bluff hands are decided by composition-level features, not blockers).

Decisive analysis on the two RAISE collapses where blockers were the migration's premise:

- **MW-45:** board AcKd6h-Qs is **rainbow** — `nut_flush_block` is **structurally inert** on this row (zero flush dimension exists). The correct RAISE comes from `is_set` + `worse_hand_pct=0.91` + composition signals already in the 55-feature surface. Correctly weighting `nut_flush_block` changes nothing.
- **MW-47:** hero IS the canonical nut-flush-blocker case (AsQs on KsJd5s two-tone). But the GTO-correct RAISE is justified by `{nut draw outs} + {gutshot} + {fold equity vs bet+call}`, **not by the blocker bit per se**. A perfectly-weighted blocker would not flip the prediction; the missing signal is "draws are RAISE-eligible with fold equity."

Empirical importances confirm: `nut_flush_block`=0.0000 (literally never split on), `straight_draw_block_pct`=0.0071, `nut_made_block_pct`=0.0056. The booster recognized these features have low discriminative power on the actual training distribution and ignored them.

**Implication:** the contract migration premise (55→59 features for blocker discrimination) does not deliver value on this reference set + corpus. Either the corpus needs more blocker-decisive situations (gto-expert H1, alternative — but gto-expert ruled this out via per-hand analysis), or the 4 P1 blocker features are not load-bearing for the canonical RAISE/bluff spots they were designed to capture (H2, what gto-expert concludes).

### QC verdict on PR #126: APPROVE

Three audits all pass:
1. **Diff scope** — exactly 4 files; zero edits to existing source surfaces; no model artifact (correctly absent per stop condition #3); Path Y discipline verified genuine
2. **Citation existence (TC-23)** — zero drift at current master HEAD; all citations verified live; `feature_extractor.FEATURE_COLUMNS` length=59, `gto_model.FEATURE_COLUMNS` length=55, blocker tail correct
3. **Provenance** — trainer docstring + report Section D match reality; warm-start anchor SHA256 `9f3845bb...c366900` matches live `sha256sum`; xgboost 3.2.0, numpy 2.4.3, python 3.12.3 all match; CLAUDE.md §6 addendum satisfied

**One non-blocking wording cleanup:** trainer report line 261 says "Median-litmus seed promoted to /tmp/builder-12.5D-wt/..." which conflicts with Section D "no model promoted" — wording cleanup, technical state correct. Can ride along on 12.5D' or be amended in a follow-up cleanup PR; does not gate APPROVE.

QC: APPROVE. Orchestrator merges PR #126 immediately as a re-runnable BLOCKED baseline.

## Owner WHAT decision space (A/B/C/C')

Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator presents options; owner decides. The four directions are now sharper given expert findings:

### Direction A — accept gate fail; close 12.5D as ran-cleanly-fell-short
- **Pros:** cleanest paper trail; lowest immediate cost
- **Cons:** discards the actionable class-prior collapse finding; the trainer (now on master after merge) sits as a baseline future iterations build from but no concrete next step is queued; forces a future "we should have run 12.5D' when we had the diagnosis" reckoning
- **What ships:** PR #126 merged as baseline; v9-3way-v2.2 stays canonical for the 31/40 region; v9-student is a "tried, didn't beat baseline" data point in the project log

### Direction B — re-evaluate gate threshold; potentially ship 31/40
- **Pros:** acknowledges the migration premise (Finding 3 H2) didn't hold; ships v9-student despite being below baseline if a structural-shortfall argument is made
- **Cons:** the chosen seed scores **strictly worse** than baseline on the same overlay (31 vs 33). Shipping a regression to ship the migration is worse than not shipping. gto-expert + ml-architect both implicitly reject this.
- **Verdict from experts:** B is structurally weak. gto-expert: "do NOT recommend Option A — closing silently regresses the litmus." ml-architect: "the empirical 31 vs 33 disproves 'confidence alone is sufficient'."

### Direction C (as originally framed) — 12.5D' with R-2 option C (hybrid weighting on RAISE only)
- **Pros:** localized; ml-architect §11 R-2 sanctioned
- **Cons:** **insufficient given finding 2.** RAISE-only mitigation addresses 2 of 7 in-family failures (MW-45/47); leaves the 5 BET/CALL collapses on the table (MW-17/24/25/40/42)
- **Verdict:** orchestrator does NOT recommend C as originally framed; it would not close the 31→33 gap

### Direction C' (NEW — emerged from synthesis) — 12.5D' with broader hybrid weighting + invariant test
- **Implementation surface:** ~5 lines at `train_model.py:252-257` shape: `sample_weight = confidence × min(3.0, mean_class_count / class_count)` (ml-architect Q3) + 1 invariant test (`_StudentInferenceLike45` shim per ml-architect Option α) + the blueprint pre-flight protocol amendment (ml-architect Q1)
- **Expected effect:** addresses 7 of 7 in-family failures (gto-expert shared root cause). MW-31/MW-46 remain residual — feature-surface gap, separate fix not in scope. Plausible 12.5D' outcome: **31 → 36-38 of 40** (closing the gap and exceeding baseline by 3-5)
- **Risks:** (a) hybrid weighting may overshoot — turn the under-aggression into over-aggression; (b) the 3.0 cap is hyperparameter; ml-architect picked from train_model.py:252-257 prior art, but tuning may be needed; (c) MW-31/46 stay broken regardless
- **Path Y discipline:** preserved. New surface = trainer-internal + tests-internal. No edits to gto_model.py / coaching/gto_model.py / sizing_oracle.py / train_model.py / train_sizing_model.py / feature_extractor.py.

### Recommendation framing (per `feedback_orchestrator_decides_not_recommends.md`)

**Orchestrator does NOT recommend between A/B/C/C'.** That's owner-scope. Orchestrator's structural observation:

- **A** is technically valid but discards the diagnostic. If chosen, queue the gto-expert+ml-architect findings as project-state knowledge for future cycles.
- **B** is structurally weak. Both experts implicitly reject.
- **C** as originally framed is structurally insufficient. Orchestrator notes this.
- **C'** is the structurally-supported 12.5D' path if owner wants another shot at the gate.

If owner has no preference, the **default cleanest path** would be C' — but owner's call.

## What happens after owner decision

| Owner picks | Next orchestrator action |
|---|---|
| A | Author "12.5D close-out" comm; queue Findings 1-3 in project state for future cycles; phase advances to whatever ml-architect/owner queues next (no v9-student ship) |
| B | Author "12.5D ship at 31/40" directive (with strong caveats); dispatch builder to write the model artifact; QC + ml-architect re-review the ship-a-regression decision |
| C (original framing — RAISE-only mitigation) | Author "12.5D' RAISE-only" directive; orchestrator notes structural insufficiency in the directive |
| C' (broader hybrid + invariant test) | Author "12.5D' hybrid weighting + invariant test + protocol amendment" directive per ml-architect Q3 spec; LEAD-PROGRAMMER named author |
| Other | Owner-defined; orchestrator authors the matching directive |

## What does NOT happen at this gate

- No 12.5+1 dispatch until owner picks
- No source-surface edits under any direction (Path Y still binds)
- No model promotion under any direction without passing reference-evaluator gate

## References

- BLOCKED PR #126 (open at synthesis time; orchestrator merges per QC APPROVE immediately after this comm)
- Decision comm PR #127 (master `3d637c7`)
- Dispatch directive PR #125 (master `e3c0dfc`)
- Approved blueprint PR #122 (master `1e4e47e`)
- Pivot directive PR #119 (master `770b897`)
- ml-architect spec PR #110 (master `291af80`) — §11 R-2 risk register
- Findings (raw, in /tmp on orchestrator host):
  - `/tmp/qc_125d_findings.md`
  - `/tmp/gto_expert_125d_findings.md`
  - `/tmp/ml_architect_125d_findings.md`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_quality_default_no_ask.md`

**Status: SYNTHESIS COMPLETE. PR #126 merging now per QC APPROVE. Owner gate ready: A/B/C/C'. Default cleanest path = C', but owner's call.**
