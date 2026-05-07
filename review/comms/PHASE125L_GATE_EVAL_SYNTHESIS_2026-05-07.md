---
date: 2026-05-07
from: LEAD-PROGRAMMER (architect-hat)
to: Owner (DECISION-PENDING) · Main terminal (orchestrator) · QC stream
re: Phase 12.5L gate evaluation — synthesis of 12.5K 3-lever exhaustion + owner-decision proposal (Options A / B / C); architect-hat recommendation
status: SYNTHESIS — owner-gate (HARD) at PR merge; no execution this PR
---

# Phase 12.5L gate-eval — synthesis comm

## §1 Purpose

Closing synthesis for the 12.5I/J/K workstream. Per dispatch `MAIN_TERMINAL_PR293_RESOLUTION_AND_125L_DISPATCH_2026-05-07.md` (master `b59a0d0`, PR #296):

- Document the 3-lever ceiling experiment in full
- Surface the empirical ceiling claim with per-lever evidence
- Present 3 owner-decision options with cost/time/risks
- Provide a single architect-hat recommendation
- Document stay-wrong list final state for project memory

This comm contains NO execution. The owner-gate at -L QC PASS is HARD per dispatch §"Sequencing"; orchestrator HOLDS LOOP at -L QC PASS pending owner decision.

---

## §2 Full 12.5K experiment record

### §2.1 Background — what brought us to 12.5K

12.5I (MW-40 verification mini-pipeline A→B→C→D→E, master through PR #245) attempted to graduate MW-40 from the stay-wrong list via targeted labelling. **Result: graduation-fail.** The redesigned MW-40 hands routed BET via the labelling pipeline — empirically faithful per the v3.4 protocol, but divergent from the canonical CALL action on the reference set. Project-memory finding: MW-40 is a labelling-pipeline-canonical mismatch.

12.5J (small-sample retrain with feature-set adjustment, PR #126→`B_FEATURE_IMPLEMENTATION`→`E_SMALL_SAMPLE_RETRAIN`) ran a 5-seed re-train on the 788-corpus. **Result: median 33/40 solver-corrected; model NOT promoted** (below v9-3way-v2.2 baseline 34/40).

These two failures motivated the 3-lever 12.5K diagnosis: identify whether the gap was variance / hyperparameter / data-bound.

### §2.2 12.5K — three levers

| Lever | Hypothesis | Method | n | Result | Verdict |
|---|---|---|---|---|---|
| **A — More seeds (variance)** | 5-seed sample too small; baseline gap is sample-variance noise | 20 seeds (0-19) on 788-corpus same hypers | 20 | mean **33.10/40 ± 0.30** (1-σ upper 33.40) | **Variance hypothesis ruled out** |
| **B — Hyperparameters** | 59-surface hypers wrong for 61-surface architecture | 3-config × 5-seed pilot (default / deeper_fewer / more_lower_lr) on 788-corpus | 15 | best **33.20 ± 0.40**; spread 0.20 hands across configs | **Hyperparameter hypothesis ruled out (early-stop on weak signal)** |
| **C — Augmented data** | 788-corpus undersized; stay-wrong axes need more training data | 200-hand 4-axis labelling pipeline (PR #269/#273/#281/#285/#289/#293); 988-corpus 5-seed retrain | 5 | mean **33.00/40 ± 0.00** | **Augmented-data hypothesis ruled out (NULL within Lever A noise)** |

All three levers produced means in **33.0 — 33.2 / 40 solver-corrected**. None produced a mean within Lever A's 1-σ upper bound of 33.40 even when generously interpreted, and none reached the baseline 34/40.

### §2.3 Per-lever detail

#### §2.3.1 Lever A — variance characterization (PR #253 + PR #261)

- **Plan**: 20-seed run on 788-corpus to characterize the natural sample variance.
- **Pilot**: Seeds 5+6 (PILOT_REPORT_PHASE125K_A_2026-05-06.md): both 33/40; pilot gate CLEAR.
- **Full run**: Seeds 7-19 added (13 more) on top of PR #253's 5 + 2 pilot = **20 seeds total**.
- **Result distribution**: 2 of 20 seeds at 34/40 (10%; Seeds 1, 17); 18 of 20 at 33/40 (90%). Mean **33.10/40**; std **0.30**; 1-σ upper bound **33.40**.
- **Per stay-wrong** (MW-17/40/45/47): 4/4 stay-wrong continue to diverge across all 20 seeds at chosen-seed inference.
- **Cost**: ~$0; ~2-3h wall clock (5 seeds × ~36s × 4 batches).
- **Verdict**: Sample variance is NOT what's causing the baseline gap. The 1-σ upper bound 33.40 is below 34.0; the model is genuinely below baseline at the 20-seed scale.

#### §2.3.2 Lever B — hyperparameter sweep (PR #265)

- **Plan**: 3-config × 5-seed pilot on 788-corpus; gate-out before full sweep (~50-100 configs) if signal weak.
- **Configs tested**: `default` (existing v9-3way-v2.2 hypers), `deeper_fewer` (max_depth+1, n_estimators-200), `more_lower_lr` (n_estimators+200, lr×0.7).
- **Per-config 5-seed means**: default **33.20/40 ± 0.40**; deeper_fewer **33.00/40 ± 0.00**; more_lower_lr **33.20/40 ± 0.40**.
- **Per-config spread**: 0.20 hands (33.00 → 33.20).
- **Per stay-wrong**: 4/4 stay-wrong continue to diverge across all 3 configs at chosen seed.
- **Cost**: ~$0; ~3 min × 3 configs = ~10 min wall clock (much faster than estimated).
- **Verdict**: Pilot signal decisive. Best-config mean (33.20) is within Lever A's 1-σ upper bound (33.40); no hyperparameter direction in the pilot points to a +0.5+ lift. Early-stop on weak signal per `feedback_quality_default_no_ask.md`. Even a hypothetical +1-hand best config in the wider grid would not justify 50-100h wall clock vs cheaper Lever C.

#### §2.3.3 Lever C — augmented data (PR #269 → PR #273 → PR #281 → PR #285 → PR #289 → PR #293)

5-phase pipeline:

| Sub-phase | PR | Scope | Result |
|---|---|---|---|
| -A (plan) | merged | Plan + design | Plan ratified; 4 axes targeting MW-17/40/45/47 |
| -B (situation gen) | #269 | 200 hands × 4 axes | Pilot routing PASS for MW-40/45 axes; MW-17/47 routed FOLD due to 1-FD-suit board factory bug |
| -C-PILOT (label) | #273/#277/#281 | 50-hand pilot labelling | Path 2 fix (suited hero + 2-FD-suit boards); Path A re-tag MW-17 (axis-target shift to RAISE) |
| -C-SCALE (label) | #285 | 200-hand × 5-labeller × 4-axis full labelling | 1050 labels; consensus produced |
| -D (Opus tier-up) | #289 | 20 Opus calls (5 canonical × 4 axes) | **20/20 Sonnet-Opus match (100%)** across all 4 axes |
| -E (integration + retrain) | #293 | 988-corpus assemble + 5-seed retrain | mean **33.00/40 ± 0.00** |

- **Per-action distribution shift**: BET +30%, RAISE +88%, CHECK unchanged (Lever C concentrated on under-represented postflop classes).
- **Confidence distribution** (988-corpus labels): 1.0 = 675 (68%), 0.8 = 182 (18%), 0.6 = 125 (13%), 0.4 = 6 (1%).
- **Per stay-wrong** (chosen Seed 2): 4/4 stay-wrong continue to diverge. Lever C did NOT graduate any stay-wrong hand.
- **Cost**: ~$45-50 LLM (Sonnet labelling SCALE) + ~$15-20 (Opus tier-up); ~6-8h wall clock total across the 6 PRs.
- **Verdict**: Augmented data ruled out as the cause. The model trained on the pipeline-labelled augmented corpus learns the pipeline's view, which diverges from canonical for MW-17 + MW-40 (graduation-fail-by-construction). MW-45/47 are pipeline-aligned but model still doesn't graduate them — the model layer can't extract the discriminating signal at 988-corpus 61-surface scale.

### §2.4 Composite cost

12.5K total (all 3 levers + Lever C 5-phase pipeline): ~$60-70 LLM; ~12-15h wall clock; ~30 PRs through the chain (PR #228 → PR #295). **Empirically thorough; no remaining lever-class to test within the existing trainer/feature/architecture stack.**

---

## §3 Empirical ceiling claim

### §3.1 The claim

**v9-3way-v2.2 at 34/40 solver-corrected IS the ceiling for the current trainer/feature/architecture stack on the available 988-corpus 61-feature configuration.**

### §3.2 Per-lever evidence supporting the claim

1. **Lever A rules out variance**: 20 seeds; mean 33.10 ± 0.30; 1-σ upper 33.40 < 34.0. The 34/40 baseline is at the high end of natural variance, not the central tendency.
2. **Lever B rules out hyperparameters**: 3 configs span 0.20 hands. No direction in the explored hyperparameter neighborhood lifts mean by ≥0.5. Best config (33.20) at Lever A's upper-noise edge.
3. **Lever C rules out training-data scale**: 988-corpus mean 33.00 ± 0.00 within Lever A noise (33.10 ± 0.30). Adding 200 high-quality (20/20 Opus-validated) hands targeting under-represented classes did NOT lift mean.
4. **Stay-wrong consistency**: All 4 stay-wrong hands diverge across all 3 levers at chosen-seed inference. The model's wrongness is structural, not sampling.
5. **Convergent diagnostic finding**: 12.5I MW-40 graduation-fail (PR #245) + 12.5K-C-C-PILOT MW-17 axis-target shift (PR #281) confirm 2 of 4 stay-wrong are labelling-pipeline-canonical mismatches; augmented training via the labelling pipeline architecturally cannot teach canonical action on those axes.

### §3.3 What the ceiling claim does NOT exclude

- Different feature surface (e.g., 75+ features with new geometric or composition features)
- Different model architecture (e.g., transformer-based, teacher-student distillation from oracle)
- Different labelling source (e.g., human-expert labelling, oracle-direct labelling — both outside the existing v3.x labelling pipeline)
- Substantially different corpus scale (~5000+ hands) with broader axis coverage

These are categorically different from variance / hyperparameter / data-scale-within-pipeline. They are the substance of Option B below.

---

## §4 Owner-decision proposal — 3 options

### §4.1 Option A — SHIP and accept v9-3way-v2.2 as the empirical ceiling

**What it does:**
- Lock v9-3way-v2.2 (34/40 solver-corrected) as the production model for HU+3way scope.
- Lock the 988-corpus + 61-feature surface + existing trainer + warm-start anchor as the production training stack.
- Document the 3-lever exhaustion as the empirical case for ceiling acceptance.
- Project memory: "v9-3way-v2.2 IS the ceiling for current stack on 988-corpus" (project_*) + "MW-17 + MW-40 are labelling-pipeline-canonical mismatches" (project_*).
- Move project to next deliverable per CLAUDE.md progressive chain (multiway 4-way OR HU model expansion OR coaching pipeline OR mobile app integration).

**Cost**: ~$0 LLM; ~30-60 min builder synthesis to memorialize.
**Wall clock**: ~1 day.
**Risks**:
- **Risk-A1 (medium)**: 34/40 solver-corrected is below the 88.1% HU accuracy target if the 40-hand reference set is tightened (e.g., 50-hand or 60-hand reference with rebalanced multiway).
- **Risk-A2 (low)**: If a future rebuild of the labelling pipeline produces canonical-aligned labels for MW-17 + MW-40, the ceiling may shift; closing the 12.5K experiment now means re-opening it later if pipeline rebuild happens.
- **Risk-A3 (low)**: Project pivots away from the 3-way model with 6/40 solver-corrected hands as known unreliable; coaching pipeline must surface this to users.

### §4.2 Option B — PURSUE Lever D (different architecture/approach)

**What it does:**
- Architect-hat exploration phase (analogous to 12.5L synthesis but for "what radically different approach could break the ceiling?").
- Candidate Lever D directions:
  - **D1**: Teacher-student distillation from a stronger oracle (e.g., GTO solver direct-labelling on 5000+ hand corpus).
  - **D2**: Transformer / sequence-model architecture vs the current XGBoost; range-as-sequence + board-as-token representation.
  - **D3**: Meta-learning with task-conditioned heads (one head per multiway-vs-HU; one per stack-depth bucket).
  - **D4**: Substantial corpus expansion (5000+ hands) via untested labelling sources (oracle-direct or human-expert).
  - **D5**: Feature surface expansion (75+) via composition-quad redesign + new geometric features.
- Each candidate gets a small pilot (1-2 weeks) before commitment.

**Cost**: ~$undefined LLM (architecture-dependent); ~2-6 weeks per candidate D-direction; ~3-4 candidates plausibly worth piloting.
**Wall clock**: 2-6 months for full Lever D exploration.
**Risks**:
- **Risk-B1 (high)**: No guarantee any Lever D direction breaks the ceiling. The ceiling claim covers the existing stack; Lever D is a bet on a fundamentally different stack producing better numbers, with no pre-experiment evidence.
- **Risk-B2 (medium)**: Sunk cost. Each candidate that fails consumes weeks of wall clock vs Option A's pivot to other deliverables.
- **Risk-B3 (medium)**: Distracts from the production-readiness deliverables (coaching pipeline, mobile integration) that the project needs to ship before model-quality lift becomes user-visible.
- **Risk-B4 (low)**: Architectural drift — multiple Lever D candidates may produce mutually incompatible artifacts that complicate eventual production deployment.

### §4.3 Option C — ACCEPT CEILING and advance progressive chain to v9-4way

**What it does:**
- Same lock-in as Option A (production model = v9-3way-v2.2).
- Specifically advances the project to v9-4way per CLAUDE.md "Progressive model chain: v8→v9-3way→v9-4way→v9-5way".
- Treats the 988-corpus + 61-feature stack as the **production scaffold**, not the ceiling target. The next phase trains v9-4way on the same stack and the team learns whether the ceiling-class problem replicates at 4-way.
- Project memory: same as Option A.

**Cost**: v9-4way training (~similar to v9-3way training cycles): ~$50-100 LLM (labelling at 4-way scale); ~4-8 weeks wall clock for full v9-4way development.
**Wall clock**: 1-2 months.
**Risks**:
- **Risk-C1 (medium)**: v9-4way may hit a similar 34/40-class ceiling for analogous structural reasons (same trainer + similar feature surface + same labelling pipeline).
- **Risk-C2 (low)**: Reusing the labelling pipeline that has known canonical mismatches (MW-17, MW-40) at 3-way may produce analogous mismatches at 4-way, costing future mini-pipeline cycles like 12.5I MW-40 verification.
- **Risk-C3 (medium)**: Progressive chain commitment locks the project to model expansion before it has shipped the coaching-pipeline / mobile-app deliverables that user-facing value depends on.

### §4.4 Comparison matrix

| Dimension | Option A (SHIP) | Option B (Lever D) | Option C (Advance chain) |
|---|---|---|---|
| Cost | ~$0 | ~$undefined | ~$50-100 |
| Wall clock | ~1 day | 2-6 months | 1-2 months |
| Ceiling-break probability | n/a (accepts) | uncertain (no pre-evidence) | n/a (accepts; tests at 4-way) |
| Production-readiness impact | Frees team for coaching/mobile | Distracts from production | Continues model expansion |
| Sunk-cost risk | Minimal | High | Medium |
| Memorializes 12.5K | Yes | Yes | Yes |

---

## §5 Architect-hat recommendation

### §5.1 Recommendation: **Option A — SHIP and accept v9-3way-v2.2 as the empirical ceiling**.

### §5.2 Reasoning

Per memory `feedback_orchestrator_decides_not_recommends.md` + `feedback_quality_default_no_ask.md`: architect commits to a single recommendation with reasoning, owner decides.

**Three reasons Option A is the architect-hat recommendation:**

1. **Empirical case is decisive.** The 3-lever ceiling claim is supported by 35+ training runs across 3 fundamentally different intervention dimensions (variance / hyperparameters / data scale). The probability of a 4th lever WITHIN the existing stack producing a +1-hand lift is indistinguishable from zero given the convergent evidence. The remaining unexplored lift directions (Option B candidates D1-D5) are categorically different from the existing stack — they are not "more tuning" but "different stack." That's a separate project, not a continuation of 12.5K.

2. **Production-readiness ROI is unfavorable for Option B.** The user-facing value of the project depends on the coaching pipeline + mobile app shipping. A 1-2-month delay shipping production for a 0-1 hand lift on the 40-hand reference set produces minimal user-facing improvement vs the same 1-2 months invested in coaching-pipeline UX or multi-stack-depth coverage. Option B is the academically interesting path, but the project's stated user-value chain (CLAUDE.md "Mobile poker training app with a GTO Oracle") depends on shipped product, not benchmark optimization.

3. **Option C's incremental cost is largely orthogonal to the ceiling decision.** Whether v9-4way is built on the existing stack (Option C) or a Lever D stack (Option B continuation) is a SEPARATE decision from "is v9-3way-v2.2 the ceiling for the existing stack?" Option A says YES to the latter without committing to either v9-4way path; the v9-4way decision can happen after Option A locks v9-3way and after the coaching/mobile deliverables progress. **Sequencing**: lock the ceiling NOW, decide the chain-extension cadence LATER.

### §5.3 What Option A leaves on the table for owner consideration

- **The 4 stay-wrong hands** (MW-17, MW-40, MW-45, MW-47) remain known model-layer mismatches. Coaching-pipeline UX should surface low-confidence predictions to users so the model's known weak-spots are not presented as authoritative.
- **The labelling pipeline's canonical mismatch** on MW-17 + MW-40 is a standing limitation; if a future rebuild of the v3.x labelling protocol resolves it, the ceiling claim can be revisited.
- **Lever D exploration** is parked, not refused. A future architect-hat phase can re-open it after coaching/mobile ship.

### §5.4 Summary

**Architect-hat recommends Option A.** The 12.5K experiment is empirically conclusive; Option B's expected value is low for the project's user-value chain at this stage; Option C's chain-advancement is a separate decision that can wait. Lock v9-3way-v2.2 as production for HU+3way; pivot to coaching/mobile/UX deliverables; revisit Lever D as a future project phase if and when production-readiness is past the user-value threshold.

---

## §6 Stay-wrong list — final state for project memory

### §6.1 Final stay-wrong list (4 hands; 12.5K experiment closure)

| Hand | Type | Pipeline label | Canonical label | Cause | 12.5K outcome |
|---|---|---|---|---|---|
| **MW-17** | labelling-pipeline canonical mismatch | RAISE (per Path A re-tag; suited nut FD on 2-FD-suit board) | CALL | Pipeline routes "suited nut FD on 2-FD-suit board → RAISE" via KB §1.7; canonical is CALL with low pot odds | NO graduation; pipeline-canonical mismatch is structural |
| **MW-40** | labelling-pipeline canonical mismatch | BET (per PR #245 graduation-fail) | CALL | Pipeline routes redesigned MW-40 to BET via composition-quad; canonical is CALL | NO graduation; pipeline-canonical mismatch is structural |
| **MW-45** | model-layer-stuck (pipeline-aligned) | RAISE | RAISE | Pipeline correctly labels RAISE; 988-corpus 5-seed model still mispredicts | NO graduation; model layer can't extract signal at current corpus/feature scale |
| **MW-47** | model-layer-stuck (pipeline-aligned) | RAISE | RAISE | Pipeline correctly labels RAISE; 988-corpus 5-seed model still mispredicts | NO graduation; same as MW-45 |

### §6.2 Memory candidates (orchestrator surface for owner ratification)

1. **Project memory**: "v9-3way-v2.2 IS the ceiling for the current trainer/feature/architecture stack on 988-corpus 61-surface configuration. 3-lever exhaustion verified via Levers A/B/C in 12.5K. Future lift requires Lever D class (different architecture/approach), not within-stack tuning."
2. **Project memory**: "MW-17 + MW-40 are labelling-pipeline-canonical mismatches. Augmented training data via the v3.x labelling pipeline architecturally cannot teach canonical action on these axes; future verification rounds should pre-test labelling-pipeline-canonical alignment BEFORE designing data."
3. **Project memory**: "MW-45 + MW-47 are model-layer-stuck (pipeline-aligned). Either feature surface or model architecture limits the current stack from extracting the discriminating signal at 988-corpus scale. Lever D candidates D1/D2/D5 are the most plausible directions to break this."
4. **Memory note refresh** (per dispatch §"Owner-scope items pending"): "composition quad" vs "composition triple" terminology; pre-flight 4-check does NOT catch domain-specific feature semantics; structural arguments must cross-check against v3.4 DO NOT rules.

---

## §7 What this PR does NOT do (per dispatch §"What you do NOT do")

- ❌ Does NOT execute Option A, B, or C (synthesis only)
- ❌ Does NOT modify v3.x prompts
- ❌ Does NOT modify river-rats-core/ source
- ❌ Does NOT modify BATCH2 reference
- ❌ Does NOT modify any data file
- ❌ Does NOT make the ship-or-defer decision (owner-scope per dispatch §"Sequencing — HARD OWNER-GATE on -L merge")

---

## §8 Files in PR diff

- `review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` (this comm)

That is the entire diff. Single-file synthesis comm; no code/data changes.

---

## §9 References

- 12.5K master plan: `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- Lever A: `BUILDER_REPORT_PHASE125K_A_MORE_SEEDS_2026-05-06.md` (PR #261; master `edf04a6`)
- Lever B: `BUILDER_REPORT_PHASE125K_B_HYPERPARAMETER_SWEEP_2026-05-06.md` (PR #265; master `d45575b`)
- Lever C plan: `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`
- Lever C 5-phase: PR #269 / PR #273 / PR #281 / PR #285 / PR #289 / PR #293
- 12.5K-C-E builder report: `BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (PR #293; master `62814a3`)
- 12.5K-C-E QC verdict: `REVIEW_QC_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (PR #295; master `50e7e15`)
- 12.5L dispatch: `MAIN_TERMINAL_PR293_RESOLUTION_AND_125L_DISPATCH_2026-05-07.md` (master `b59a0d0`; PR #296)
- 12.5I MW-40 graduation-fail: `BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md` (PR #245)
- 12.5K-C-C MW-17 axis-target shift: `BUILDER_REPORT_PHASE125K_C_C_FIX_2026-05-07.md` (PR #281)
- v9-3way-v2.2 baseline: 34/40 solver-corrected (CLAUDE.md project state; reference set 40-hand)
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, loop directive

---

**Status: 12.5L gate-eval synthesis COMPLETE. 3-lever ceiling claim documented; 3 owner-decision options analyzed (A SHIP / B Lever D / C advance chain); architect-hat recommendation = Option A. Awaiting QC pre-merge audit + ORCHESTRATOR LOOP HOLD at -L QC PASS pending owner decision per dispatch §"Sequencing — HARD OWNER-GATE on -L merge".**
