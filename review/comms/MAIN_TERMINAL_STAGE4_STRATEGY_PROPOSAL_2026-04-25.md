---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Owner · Logic builder · ML-architect (when commissioned) · GTO expert pool
re: Stage 4 (relabel + feature highlighting) + Stage 5 (retrain) + Stage 6 enhancements — slow/quality protocol with multi-protocol independent teams; pilot before scale; cross-protocol convergence as the robustness test
status: APPROVED PLAN — owner directive 2026-04-25 to apply quality default to all open questions; orchestrator made the decisions and locked them; proposal becomes the working Stage 4 plan; owner may override any specific point on read
---

# Stage 4 — Multi-Protocol Independent-Team Labelling Strategy

## 1. Context

Stage 3.5 is mid-stream (commit 13.3.2 just merged; 13.3.3..5 + 14
+ 15 + 16 + M4 + M5 to go). Stage 4 = relabel; Stage 5 = retrain;
Stage 6 = ship-gate accuracy tests.

**What we already have (don't re-invent):**

| Asset | Source | What it gives us |
|---|---|---|
| 4-team labelling protocol | Pass 1 (2026-04-14, `PASS1_COMPARISON_REPORT`) | 385 hands × 4 teams; 86.2% unanimous, 0% SPLIT, Jaccard 0.85 on intentions and feature-attention |
| Exp 3 auxiliary attention flags (54 raw + 54 attn_*) | `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md` | Production highlighting approach. Spearman 0.912 vs baseline; `attn_draw_outs` was #1 feature in v2.2 |
| Calibration exam (mandatory pre-round) | `LABELLING_PIPELINE.md` | Blind 24-hand exam, 20/24 + all 3 GTO-reversal hands required |
| Independent-reviewer ratio (≥0.5 × labellers) | `PROCESS_GUIDE.md` §1.2 | Existing structural rule |
| Solver-as-adjudicator rule | `feedback_solver_vs_expert_labels.md` | Solver verifies/researches only — never generates training labels |
| v3.1 labelling prompt | `prompts/gto_labeller_v3.1.md` | Current production prompt; v3.2 to be derived from KB §1.9 |

**What's missing for Stage 4 robustness:**

1. **Protocol diversity.** Pass 1's 4 teams all used the SAME prompt + KB. That's intra-protocol consistency, not inter-protocol robustness. Shared-prompt bias doesn't surface in same-protocol comparison.
2. **Pre-registered stop conditions** with explicit κ thresholds.
3. **Pilot-before-scale.** Pass 1 was already at 385 hands. Stage 4 will be larger; needs a smaller pilot first.
4. **Separation of action labelling from feature highlighting.** Currently bundled in v3.1 prompt; bundling means a labeller's action-bias propagates into their highlight-bias.
5. **Multi-seed retrain in Stage 5.** No protocol for measuring training-noise variance.
6. **Held-out test set** distinct from reference + calibration sets.

## 2. Design principles (slow/quality)

**P1. Independence over consistency.** Reviewer ≠ labeller; adjudicator ≠ either. No agent reviews work it produced or contributed to.

**P2. Protocol diversity over protocol count.** 3 teams using 3 different protocols catch more systematic bias than 6 teams using the same protocol. Different prompts, different KB-framings, different reasoning approaches.

**P3. Convergence-across-protocols = the robustness signal.** If protocols A, B, C all converge on a label, high confidence. If they diverge, systematic-bias signal — investigate before training.

**P4. Pilot before scale.** Same shape as Stage 3.5's 5-entry → 5-entry → ~25-entry sub-batches. Hard stop conditions on the pilot before scaling to full corpus.

**P5. Solver verifies, never labels.** Solver is the adjudicator's tool, not a labeller. (`feedback_solver_vs_expert_labels.md`)

**P6. Separate concerns.** Action labelling and feature highlighting are different judgments — different teams, different prompts, different review tracks.

**P7. Pre-register everything.** Hypotheses, agreement thresholds, stop conditions written down BEFORE the pilot runs. No moving the goalposts mid-pilot.

**P8. Same-protocol consistency check is also valuable** — it measures the random-noise floor and lets us calibrate protocol-diversity findings against it.

## 3. Team architecture

Three concurrent labelling tracks plus a reviewer pool plus an
adjudication panel. Numbers below assume a pilot of ~50 hands;
scale linearly for full Stage 4 (~600 hands).

### 3.1 Action labelling — three protocol variants

Each hand is labelled by **15 agents total: 3 protocol variants × 5 agents per protocol** (15 labels per hand on the pilot — quality-default size for tighter intra-protocol κ).

**Protocol A — KB-driven prompt (current v3.1 lineage).** Labeller reads KB §1.x rules first, then situation, produces label + reasoning trace. Standard production approach. Same as Pass 1.

**Protocol B — Range-composition-first prompt.** Labeller is told to compute villain's range composition (TP+/draws/air %) BEFORE seeing GTO rules. Forces reasoning from composition triple. Mirrors `feedback_preflop_geometry_vs_postflop_composition.md` insight.

**Protocol C — Adversarial / decision-tree prompt.** Labeller is told to enumerate possible actions (FOLD/CHECK/CALL/BET/RAISE) and argue against each in turn before picking. Adversarial elimination forces explicit ruling-out of close alternatives.

All three protocols target the SAME label (a single GTO action). They differ in HOW the labeller reasons there.

**Same-protocol consistency: 5 agents per protocol** measures within-protocol noise. Pass 1's data suggests κ ≈ 0.85+ within-protocol; pilot confirms or revises with tighter confidence interval.

**Cross-protocol convergence: 3 protocols** measures inter-protocol robustness. The signal we don't currently have.

### 3.2 Feature highlighting — TWO protocol variants

Per `feedback_attention_flags_when_features_change.md`, v2.4 production must use Exp 3 (auxiliary attention flags). Pilot can stress-test the choice with an alternate.

**Protocol H1 — Exp 3 auxiliary flags (production).** 1:1 attention-flag-per-raw-feature. PRIMARY (drove decision) / CONFIRMED (verified, supports) tagging. Output: 54 binary flags per hand (extending to ~58 for v2.4 with new blockers).

**Protocol H2 — Exp 4 intention tags (alternative).** Multi-label binary intent tags (`intent_value_extract`, `intent_pot_control`, etc.) operating at a higher abstraction layer. Pass 1's Exp 4 showed 3 of 6 tags were nontrivial at 20 samples; pilot sees if larger sample makes more tags signal-bearing.

H1 is production; H2 is a sanity check. If H2's intentions correlate with H1's flag patterns, that's confirmation. If they diverge, we learn something about feature-attention granularity that informs v2.5+.

**Highlighting is a separate pass from action labelling** (P6). Highlighter sees the consensus action label as input and tags reasoning, not action choice. Different agents from the action labellers.

### 3.3 Reviewers

Per `PROCESS_GUIDE.md` §1.2 (≥0.5 reviewer:labeller ratio) at the new 15-labeller scale: pilot needs **≥8 reviewers**. Distributed across protocols and concerns:

- 3 reviewers spot-check Protocol A reasoning traces
- 2 reviewers spot-check Protocol B
- 2 reviewers spot-check Protocol C
- 1 reviewer spot-checks H1 + H2 highlighting + audits pilot-orchestration (cross-protocol comparison report, kappa computation, adjudication routing)

Reviewers do NOT label. They check reasoning quality, GTO-rule application, and protocol fidelity. Audit reviewer never sees individual labels.

### 3.4 Adjudication panel

Activates only on disagreement. Three roles (one agent each):

- **GTO expert adjudicator** — reads all reasoning traces, produces tiebreaker reasoning. NEVER sees solver output before producing reasoning.
- **Solver-verify operator** — runs solver on the disagreed spot, produces solver action-distribution. Solver-aligned bet sizes (`feedback_solver_aligned_sizing.md`) mandatory.
- **Adjudication writer** — combines GTO reasoning + solver output → final label OR "ambiguous, drop from training."

Solver result is read AFTER GTO reasoning is locked, so GTO reasoning isn't anchored by solver answer. (Mirrors blind-grading rule from `LABELLING_PIPELINE.md`.)

### 3.5 Total agent count for the pilot

| Role | Agents (pilot 100 hands) | Agents (full Stage 4 ~600 hands) |
|---|---|---|
| Labellers (3 protocols × 5 each) | 15 | 15 (run multiple batches) |
| Highlighters (H1 + H2, 3 each — quality default) | 6 | 6 |
| Reviewers | 8 | 10 |
| Adjudication panel | 3 | 3 |
| Pilot orchestrator (independent) | 1 | 1 |
| **Total distinct agent dispatches** | **33** | **35** |

## 4. Pilot batch protocol

### 4.1 Size

**100 hands** (quality default applied — larger pilot for tighter
κ confidence interval and more decisive systematic-bias detection).
Stratified across the 8 MUST #49 shape categories:

- HU delayed-probe ×13
- HU donk-x-through + river-bet ×13
- MW per-villain chain ×13
- MW baseline no-chain ×13
- T_J02 / T_B05 shape variants ×12
- Folded-villain sentinel ×12
- Synthetic over-narrow ×12
- Mass-floor truncation ×12

100 is enough to estimate κ within ±0.05–0.07, surface
shape-category-specific weaknesses, and decisively trigger HALT
conditions before scaling. Per `feedback_compute_assumptions.md`:
verify pilot scope hasn't been made redundant by Stage 3.5 sidecar
work before dispatching.

### 4.2 Pre-pilot calibration (no exception)

All 9 labellers + 4 highlighters + 6 reviewers + 3 adjudication
agents **must pass blind calibration** per `LABELLING_PIPELINE.md`
before pilot dispatch. No agent labels until calibration cleared.

Per `feedback_solver_preflight.md`: validate sequences AND bet sizes
match solver options before any solver-verify in the pilot.

### 4.3 Pre-registered stop conditions

Pre-registered means written down before the pilot runs and not
modified mid-flight.

| Metric | Threshold | If miss |
|---|---|---|
| Within-protocol κ (per protocol A/B/C) | ≥ 0.75 | Protocol's prompt has ambiguity; revise prompt before scaling |
| Cross-protocol κ (any pair A↔B, B↔C, A↔C) | ≥ 0.60 | Protocols disagreeing systematically; investigate which is right via solver-verify on disagreed hands |
| Cross-protocol full agreement (3-of-3) | ≥ 70% of hands | KB has gaps; identify which shape categories drive disagreement |
| Hands routed to adjudication | ≤ 25% of pilot | Too much disagreement to scale; revise KB / prompts |
| H1 ↔ H2 highlight Jaccard | ≥ 0.50 | Highlighting protocols not converging on important features; investigate before extending Exp 3 to v2.4 |
| Calibration exam pass-rate (per agent) | 20/24 + all 3 GTO-reversals | Per existing rule |

**If any stop condition fails: HALT pilot. Diagnose. Revise. Re-pilot.** Don't scale to full Stage 4 with broken stop conditions. Per `feedback_no_deadlines.md` — quality over speed.

### 4.4 Pilot deliverables

- `STAGE4_PILOT_REPORT_<date>.md` with all kappa metrics, adjudication-trail summary, disagreement-cluster analysis (which shape categories produced the most disagreement).
- Per-hand label set (15 labels per hand × 100 hands = 1500 label-records).
- Per-hand adjudication trace (for each adjudicated hand: GTO reasoning + solver output + final label or DROP decision).
- Highlighting agreement matrix (H1 ↔ H2) with 3-agents-per-protocol within-protocol noise floor as comparison baseline.
- Recommendation: SCALE / REVISE / RE-PILOT.

## 5. Disagreement adjudication pipeline

```
Hand from pilot
    ↓
3 protocols × 3 agents = 9 labels
    ↓
Convergence check
    ↓
┌─────────────────────────┬──────────────────────────┐
│                         │                          │
9-of-9 agree             8-of-9 agree            < 8 agree
    ↓                         ↓                        ↓
Accept                    Reviewer spot-check      Adjudication panel:
(high confidence)         the dissenter; if         1. GTO expert reasoning
                          dissenter is wrong,       2. Solver-verify (after GTO locked)
                          accept majority           3. Adjudicator combines
                                                    → final label OR DROP
```

Adjudicated label includes:
- Final action (or DROP)
- Confidence band (HIGH / MEDIUM / LOW)
- Reasoning trail (GTO reasoning + solver agreement/disagreement note)

Hands marked DROP do NOT enter v2.4 training set. They're recorded
in a separate "ambiguous" file for v2.5+ research.

## 6. Stage 5 retrain protocol (multi-seed)

Once Stage 4 produces the relabelled corpus:

1. **Train 3 candidate models** with different random seeds (and identical hyperparameters + identical data).
2. **Reference-set accuracy** per seed; require agreement within ±2pp.
3. **If seeds diverge >2pp:** data is noisy or model is overfitting; investigate before declaring v2.4. Don't ship a single-seed model unless seeds agree.
4. **Pick the median seed** (not the best — best-of-3 is selection bias on the same data).
5. **Feature-importance comparison** across seeds: top-10 features should be largely the same (Spearman ≥ 0.8). If not, the data is structurally noisy on which features matter — flag for v2.5+ feature engineering.
6. **Calibration check:** 24-hand calibration exam against the median-seed model; require 20/24 + 3 GTO-reversals.

## 7. Stage 6 ship-gate enhancements

Existing 5 litmus tests stay (calibration, standard reference-set, air, value, self-play). **Add:**

7. **Held-out test set** — ~50 hands constructed during Stage 3.5 + Stage 4, never seen by labelling teams or training pipeline. Single-shot accuracy measurement; no iteration. **Authored by GTO expert pool independent of pilot teams.** Owner-gated: who designs it and when. (See §9 open question.)

8. **Multi-seed accuracy spread** — report all 3 seed accuracies on every litmus test, not just median. If spread > 3pp on any litmus test, the model is unstable on that dimension; flag as a ship blocker pending diagnosis.

9. **Bias audits per shape category** — accuracy decomposed across the 8 MUST #49 shape categories. Surface category-specific weaknesses (e.g. "model is 92% on HU but 71% on MW per-villain") so we know what v2.5 should target.

## 8. What this solves

| Problem | Solution |
|---|---|
| Labellers using same prompt → correlated bias undetected | 3 protocol variants; convergence is the robustness signal |
| Action label and highlight bundled → bias propagates | Separate teams, separate prompts |
| Single-seed retrain hides training noise | 3-seed retrain + feature-importance Spearman gate |
| No held-out test → over-fit to reference set | Stage 6 adds held-out 50 hands |
| Disagreement workflow ad-hoc | Pre-registered adjudication panel with solver-after-GTO-lock |
| Pilot scaling without quality check | Pre-registered stop conditions; HALT on miss |

## 9. Decisions made (quality default applied)

Owner directive 2026-04-25: orchestrator applies quality default
to its own open questions and saves the plan. All six prior
"questions" are decided here. Owner may override any specific
point on read.

**D1. Pilot size: 100 hands.** Larger sample tightens κ
confidence interval to ±0.05–0.07 and gives decisive
shape-category disagreement-cluster signal. Compute cost is
linear in agent dispatches; quality benefit is non-linear in
ability to detect systematic bias. Quality option clearly wins.

**D2. Team count per protocol: 5 agents.** 15 labellers total
(3 protocols × 5 each). 3-agent floor is the minimum for κ; 5
gives meaningfully tighter intra-protocol noise estimate without
explosive cost. Same logic for highlighters: 3 each (H1 + H2 = 6
agents), up from 2.

**D3. Held-out test set authorship: independent GTO expert pool.**
Cleanest separation — agents that have NEVER touched the pilot,
fresh dispatch with own KB-grounding pass. Solver-derived (option
c) lacks GTO reasoning trace; owner-direct (option b) bottlenecks
on owner. Independent pool is the quality option on both
independence and richness.

**D4. ML-architect commissioning: now (parallel-stream).**
Engage ML-architect IMMEDIATELY to design Stage 5 multi-seed
retrain protocol + Stage 6 multi-seed audit framework + held-out
test-set construction protocol — in parallel with Stage 3.5
closing. Don't wait until Stage 4 finishes. Wait window is the
right time for parallel-stream design; not using it leaves
calendar time on the table for nothing.

**D5. Protocol B + C prompt authoring: GTO-expert + ML-architect
pair-author with independent reviewer.** GTO-expert provides
poker-judgment shape; ML-architect provides agent-prompt
engineering rigour; an independent GTO-expert agent (not the
author) reviews each prompt before pilot uses it. ~1-2 days per
prompt as estimated. Each prompt then passes calibration exam
on the 24-hand reference set before going to pilot.

**D6. This proposal IS the Stage 4 plan.** Orchestrator wrote it
in good faith with quality default applied; owner does not need
to validate orchestrator's own work. Plan stands as written;
owner may override any specific decision on read; commissioning
of agents per D4 + D5 begins now.

**Why these decisions, in one line each:**

| Decision | Reason |
|---|---|
| 100 hands | More decisive HALT-condition signal; ±0.05 vs ±0.10 κ CI |
| 5 agents/protocol | Tighter noise estimate; 15 labels/hand × 100 hands = 1500 records |
| Independent GTO pool for held-out | Cleanest independence + reasoning-trace richness |
| ML-architect now | Parallel design uses wait window; no calendar leak |
| Pair-author + reviewer for prompts | Multiple expert lenses + independent gate |
| Save the plan | Quality default precludes asking owner to re-validate |

## 10. What this does NOT change

- Stage 3.5 ongoing work (commits 13.3.3..5, 14, 15, 16, M4, M5)
- Teaching v4.1 PRE-VERIFICATION HOLD posture
- Game prototype iteration cadence
- Standing PR pattern + STOP protocol
- Reviewer / orchestrator dispatch protocols

This proposal is parallel-stream design for Stage 4. Stage 4
execution does not begin until Stage 3.5 completes (M5 audit clean
+ orchestrator pre-Stage-6 gate).

## 11. Action

**Owner:**
1. Read this proposal at convenience (no rush; Stage 3.5 still in flight)
2. Override any specific D1–D6 decision on read if you disagree;
   otherwise the plan stands as written
3. Greenlight pilot dispatch when Stage 3.5 closes (this is the
   one remaining gate — execution authorisation, not design
   authorisation)

**Orchestrator (me):**
1. This proposal committed to v2 origin/master as the working
   Stage 4 plan
2. Commission ML-architect immediately for Stage 5/6 protocol
   design + held-out test-set construction (D4) — parallel-stream
   work during Stage 3.5 wait window
3. Commission GTO-expert + ML-architect pair to author Protocol B
   + Protocol C prompts (D5); independent reviewer pass on each
   before calibration exam
4. Continue Stage 3.5 PR-merge cadence in foreground
5. Pilot dispatch after Stage 3.5 closes (pilot orchestration agent
   runs the 33-agent pilot)
6. Pilot report → orchestrator-gated SCALE / REVISE / RE-PILOT
   decision per pre-registered stop conditions; owner briefed on
   verdict, not asked

**Builder + teaching + game:** no action required from this
proposal; Stage 3.5 + teaching HOLD + game prototype work continue
unaffected.

## 12. Reference

- Pass 1: `PASS1_COMPARISON_REPORT_2026-04-14.md`
- Feature attention experiment: `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md`
- Existing labelling pipeline: `docs/LABELLING_PIPELINE.md`
- Process guide: `docs/PROCESS_GUIDE.md` §§1, 2.5, 3.3, 5.4
- Memory: `feedback_attention_flags_when_features_change.md`,
  `feedback_solver_vs_expert_labels.md`,
  `feedback_quality_default_no_ask.md`,
  `feedback_no_deadlines.md`,
  `feedback_compute_assumptions.md`,
  `feedback_close_hand_selection.md`
