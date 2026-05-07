---
date: 2026-05-07
from: LEAD-PROGRAMMER (Builder, architect hat)
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: Phase 12.5K-C-A Lever C design — 4-axis augmented data labelling round (MW-17 / MW-40 / MW-45 / MW-47); 5-phase mini-pipeline; per-axis pilot-first gates; per-axis off-ramps
status: design-only deliverable; execution gates on lever-specific dispatches per orchestrator
---

# PLAN: 12.5K-C Lever C augmented training data (architect-hat design)

## §1 Authority chain

- 12.5K design plan (parent): `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` (master `9798007`, PR #257) §5 "Lever C — augmented training data"
- Empirical convergence (2026-05-06):
  - Lever A (variance): RULED OUT — 20-seed mean 33.10 ± 0.30 (PR #261; QC PASS PR #263)
  - Lever B (hyperparameters): RULED OUT — 3-config pilot spread 0.20 hands (PR #265; QC PASS PR #267)
  - **Lever C (augmented data) is the remaining lever**
- Dispatch (fire trigger): `MAIN_TERMINAL_PR265_RESOLUTION_AND_125KCA_DISPATCH_2026-05-07.md` (master `1292233`, PR #268)
- Builder named: LEAD-PROGRAMMER (architect hat). Active fire-now directive — AUTHOR per `feedback_named_author_builds_not_polls.md`.

## §2 Scope — 4-axis augmented data labelling round (5-phase mini-pipeline)

The model is at-or-near hyperparameter-optimal at the 788-corpus 61-surface scale. Lever C tests the hypothesis that **the existing corpus is undersized for the 5-class 61-feature problem, especially on the under-represented stay-wrong classes (CALL/RAISE/BET-on-facing-bet patterns)**. Adding ~200 targeted training examples on the 4 stay-wrong axes (50 each × 4 axes) tests whether the model's decision boundary moves with more data.

Mirror the 12.5I-MW40-VERIFICATION 5-phase pattern:

| Phase | Scope | Cost | Wall clock |
|---|---|---|---|
| **A — Design** (this PR) | Architect-hat design plan; per-axis structural prediction; pilot-first per-axis gate; off-ramps | ~$0 | ~30-45 min |
| **B — Situation generation** | 4 axes × 50 parametric variants = 200 situations; factory pass; pre-flight schema/feature/ref_id integrity | ~$0 | ~15-20 min |
| **C — Labelling round** | 4 axes × 5 Sonnet labellers × 50 hands = 1000 individual labels; per-axis pilot-first 5-hand gate; per-axis off-ramp on pilot fail | ~$50-80 LLM | ~2-3 hours |
| **D — Opus tier-up** | 4 axes × 5 canonical hands × 1 Opus call = 20 Opus calls | ~$15-20 LLM | ~30 min |
| **E — Corpus integration + re-train** | Augment 788 → 988 (or partial if axes dropped); 5-seed re-train; reference set spot-check vs Lever A 20-seed baseline | ~$0 | ~1-2 hours |

**Total Lever C budget**: ~$65-100 LLM; ~4-6 hours wall clock. Within ~$300/30h auto-approval cap.

## §3 Per-axis structural specifications

### Axis MW-17 — Under-calling on low-equity nut FD facing CO bet 3-way

**Reference state (BATCH2):**
- Hand: AdKs (nut flush draw + 2 overcards) on Jd8d4c
- Position: BTN (caller); CO opens, hero calls, BB calls; flop CO bets
- Canonical action: **CALL** HIGH (raw equity 0.251, pot odds 0.268, equity-just-meets pot-odds; nut blocker)
- Model stay-wrong: predicts FOLD (chosen seed 12 PR #253)

**Structural prediction**: at 50 parametric variants of (nut FD + facing-bet + 3-way), labelling pipeline produces **CALL consensus** because:
1. Nut blocker present (`nut_flush_block ≥ 0.5`) — solver-aligned per `feedback_solver_findings.md` finding 4
2. Pot odds + equity meet break-even (raw_equity ≥ 0.22 vs pot_odds 0.25-0.30)
3. Multiway non-PFA in position with realizable equity

**Variants (50)**:
- Sub-axis A1 (Jx-high two-tone with nut FD; ~20 variants): hero AKs/AQs/AJs/A♠ x with on-board flush suit; board has J or Q or T high + low cards; CO bet 33-50% pot; rainbow/2-tone variations
- Sub-axis A2 (Tx-high or 9x-high two-tone with nut FD; ~15 variants): same hero class; lower top card; tests sensitivity to top-card rank
- Sub-axis A3 (paired-board two-tone with nut FD; ~10 variants): tests blocker-effect on paired boards
- Sub-axis A4 (rainbow with backdoor nut FD; ~5 variants): control — should produce more FOLD-leaning consensus (lower equity); validates labelling discriminates FD-strength

**Pilot 5 hands**: 2 from A1 + 2 from A2 + 1 from A3.

### Axis MW-40 — Residual passive (BET MEDIUM thin value 4-way checked-through)

**Reference state (BATCH2):**
- Hand: AhTs (TPMK T-kicker) on AJ5r
- Position: BTN (closing IP non-PFA); 4-way SRP, all check
- Canonical action: **BET MEDIUM** (raw equity 0.206, but 4-way checks cap villain ranges; thin-value bet appropriate)
- Model stay-wrong: predicts CHECK (chosen seed 12 PR #253)
- Verification round: graduation-fail confirmed (PR #241/#245 25/25 + 5/5 BET pilot consensus)

**Structural prediction**: at 50 parametric variants of (TPMK T-kicker + 4-way checked-through + IP non-PFA), labelling pipeline produces **BET consensus** because:
1. DO NOT Rule 11 OOP-only exemption — hero is IP, Rule 11 inactive
2. Composition quad: villain_air_pct elevated (0.4-0.6); villain_top_pair_plus_pct moderate; danger_score=0 on rainbow
3. villain_checked_back=1 caps villain ranges; thin-value-bet routing

**Variants (50)**: mirrors MW-40-VERIFICATION's existing 30-hand corpus (`data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl`) + 20 fresh parametric variants.

**Important consideration (architect-hat note for orchestrator)**: the MW-40-VERIFICATION-B 30-hand corpus already exists with consensus BET labels (5/5 Sonnet + Opus pilot 5/5 BET). **Recommend re-using those 30 hands as part of Lever C MW-40 axis** rather than re-labelling. New work: 20 fresh variants (already-labelled 30 + 20 fresh = 50 total). Saves ~$30 LLM + ~30 min on this axis.

**Pilot 5 hands**: 5 from the 30 already-labelled MW-40-VERIFICATION corpus (treat as smoke-test that consensus reproduces; expected 5/5 BET).

### Axis MW-45 — Under-raising slowplay-set on broadway-completed turn

**Reference state (BATCH2):**
- Hand: 5c5d (bottom set) on Ac8h5s flop, then turn Jc (broadway-completed)
- Position: CO leads turn; hero raise spot
- Canonical action: **RAISE** HIGH (set-of-5s; broadway-completed flush+straight texture; villain Ax ranges + draws comprise composition)
- Model stay-wrong: predicts CALL (chosen seed 12 PR #253)

**Structural prediction**: at 50 parametric variants of (slowplay-set + broadway-completed turn + facing-lead), labelling pipeline produces **RAISE consensus** because:
1. is_monster=1 (set is rare-strong)
2. Broadway turn completes draws → villain's bet range is polarized; raising for value extracts max
3. Composition quad: villain_top_pair_plus_pct moderate but villain_draw_pct elevated → RAISE for protection-and-value

**Variants (50)**:
- Sub-axis MW45-1 (bottom-set + broadway-Q turn; ~20): variations of A-K-x flop with Q turn
- Sub-axis MW45-2 (bottom-set + broadway-J turn; ~15): variations of A-K-x flop with J turn
- Sub-axis MW45-3 (middle-set + broadway turn; ~10): tests middle-set vs bottom-set sensitivity
- Sub-axis MW45-4 (top-set + broadway turn; ~5): control — should produce stronger RAISE consensus

**Pilot 5 hands**: 2 from MW45-1 + 2 from MW45-2 + 1 from MW45-3.

### Axis MW-47 — Shared blind spot (nut FD+OESD facing bet+call should RAISE)

**Reference state (BATCH2 + solver-corrected):**
- Hand: AsQs (nut FD + 2 overcards + gutshot) on KsJ5 two-spade flop
- Position: BB; CO opens, hero calls, BTN calls; CO bets, BTN calls; hero spot
- Canonical action: **RAISE** (solver-corrected per `reference_corrections.md`; original expert was CALL)
- Model stay-wrong: predicts CALL (chosen seed 12 PR #253)

**Structural prediction**: at 50 parametric variants of (nut FD + multiway + facing bet+call), labelling pipeline produces **RAISE consensus** because:
1. Nut blocker (`nut_flush_block ≥ 0.5`) — solver-aligned per `feedback_solver_findings.md` finding 4
2. is_combined_nut_potential composite signal
3. Equity vs the bet-call composition is high; RAISE extracts fold equity from BTN's drawing range

**Variants (50)**:
- Sub-axis MW47-1 (nut FD + overcards + gutshot; ~20): variations on KsJx-spade flops
- Sub-axis MW47-2 (nut FD + 2 overcards no gutshot; ~15): tests gutshot-contribution sensitivity
- Sub-axis MW47-3 (nut FD + 1 overcard + gutshot; ~10): tests overcard-contribution sensitivity
- Sub-axis MW47-4 (non-nut FD + overcards + gutshot; ~5): control — should produce LESS-clear RAISE consensus (the nut-blocker is what tips it)

**Pilot 5 hands**: 2 from MW47-1 + 2 from MW47-2 + 1 from MW47-3.

## §4 Per-axis pilot-first gates (binding per `feedback_pilot_first_for_long_jobs.md`)

Per dispatch §"Per-axis pilot-first 5-hand gate":

| Pilot gate criterion | Continue if... | Off-ramp (per axis) if... |
|---|---|---|
| Pilot consensus aligns with structural prediction | ≥4/5 hands consensus on the predicted action | <4/5 → REPORT to orchestrator (mirror MW-40-VERIFICATION-C HALT pattern); orchestrator decides per axis |
| Sonnet API errors | <5% on 5-hand × 5-labeller pilot (= 25 calls) | >5% → STOP infrastructure |
| Reasoning convergence | Convergent reasoning citing v3.4 KB sections | Mode-collapse-style identical text → STOP |

**Per-axis off-ramp**: if axis fails pilot, that axis is dropped from Lever C; remaining axes proceed with partial scale. Mirrors the partial-scale pattern in 12.5K parent plan §5 outcome matrix row 2.

**Pre-emptive note (R3 in §10 below)**: the labelling pipeline can diverge from structural arguments (proven at MW-40-VERIFICATION). Building this off-ramp into the design lets the round gracefully handle 1-N axis fails without polluting the corpus. Even in the worst case (all 4 axes fail pilot), the discovery has informational value — it tells us the labelling pipeline disagrees with the canonical labels on these axes (similar to MW-40 finding).

## §5 Factory specifications per axis

For each axis, the factory script emits per-variant rows with:

- `ref_id` per axis: `PILOT_LEVER_C_MW17_001..050`, `PILOT_LEVER_C_MW40_001..050`, `PILOT_LEVER_C_MW45_001..050`, `PILOT_LEVER_C_MW47_001..050`
- Disjoint vs 788-corpus (PILOT_001..PILOT_788) and prior 12.5I namespaces (PILOT_695..PILOT_788; PILOT_MW40_VERIF_001..030)
- Cap-binding pre-flight: factory verifies disjointness before emit

**Standard fields per row** (mirror existing 12.5I-B factory output structure):
- `feat_dict`: 61-surface (post-PR #205); all 61 keys populated by `feature_extractor.extract_all_features` (read-only import)
- `hero_cards`: top-level
- `prior_actions`: hero-only convention
- `design_action` per T-CONTROL: per-axis structural prediction
- Standard metadata: `template_id`, `axis`, `sub_axis`, `lever_c_round=2026-05-07`

**Pre-flight 4-check on first 5 emitted situations per axis (Hybrid pilot-first per PR #228 SHOULD_FIX-1 Path 3 precedent)**:
1. Schema parity (61-surface; 0 NaN/Inf)
2. Step-18 feature plausibility per axis (axis-specific expected ranges)
3. ref_id namespace integrity (axis-namespace; no cross-axis collision; no collision with existing corpora)
4. Top-level structural fields match per-axis constraint table

Pre-flight failure → STOP; do NOT emit beyond 5.

### MW-40 axis special case

Per §3 architect-hat note: re-use the 30 already-labelled MW-40-VERIFICATION-B hands (`data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` PILOT_MW40_VERIF_001..030); add 20 fresh variants `PILOT_LEVER_C_MW40_031..050`. Total 50 hands for MW-40 axis. **Saves ~$30 LLM + ~30 min on this axis** (the existing 30 are already labelled BET 25/25 Sonnet + 5/5 Opus; no need to re-label).

## §6 Methodology rules (7 standing per 12.5I-A)

| # | Rule | Application |
|---|---|---|
| 1 | Hero-only convention in `prior_actions` | Yes — per-axis factory spec |
| 2 | Pre-flight join-cardinality (factory output count = exactly the planned count) | Yes — per-axis 50-hand exact count; 0 over/under |
| 3 | `design_action` field per hand for T-CONTROL-like rows | Yes — per-axis prediction (CALL / BET / RAISE / RAISE) |
| 4 | Pilot-first does NOT apply at -B (situation generation is deterministic factory) | Inherited; Hybrid pre-flight on first 5 per axis |
| 5 | Pilot-first DOES apply at -C (labelling round; binding) | Per-axis 5-hand × 5-labeller pilot; per-axis off-ramp on pilot fail |
| 6 | Solver-as-labels prohibited | Solver may verify per-axis predictions OR canonical references at -D Opus tier-up; never as labels |
| 7 | Cross-seed importance reporting at -E re-train | Yes — verify Step-18 + per-axis features activate as predicted on the 988-corpus re-train |

**Cap-binding pre-flight** (per dispatch + plan §5): ref_id namespace disjoint vs 788-corpus + prior 12.5I namespaces (PILOT_695..PILOT_788, PILOT_MW40_VERIF_001..030). Verified at -B emit time + at -E corpus integration.

## §7 Sequencing (multi-phase 12.5K-C workstream)

| Phase | Scope | Gate | Owner |
|---|---|---|---|
| **A (this PR)** | Design + plan | this PR opens; QC audit pre-merge | LEAD-PROGRAMMER (architect hat) |
| **B** | Situation generation (4 axes × 50 = 200 hands; factory pass; Hybrid pre-flight 4-check on first 5 per axis; MW-40 special case = re-use 30 + 20 fresh) | A merge | LEAD-PROGRAMMER (programmer hat); separate dispatch |
| **C** | Labelling round (4 axes × 5 Sonnet × 50 hands = 1000 labels; per-axis 5-hand pilot first; per-axis off-ramp) | B merge | LEAD-PROGRAMMER (programmer hat); separate dispatch; ~$50-80 LLM cost |
| **D** | Opus tier-up cross-check on 5 canonical hands × 4 axes = 20 Opus calls | C QC PASS | LEAD-PROGRAMMER (programmer hat); separate dispatch; ~$15-20 LLM cost |
| **E** | Corpus integration (788+200=988 OR partial if axes dropped) + 5-seed re-train + reference-set spot-check | D verdict | LEAD-PROGRAMMER (programmer hat); separate dispatch |

Builder remains single-stream serial. Slower stream sets pace per `feedback_orchestrator_controls_parallel_timing.md`. Orchestrator gates each transition with a `MAIN_TERMINAL_*_DISPATCH` comm naming LEAD-PROGRAMMER per `feedback_explicit_action_trigger.md`.

## §8 Stop conditions (this PR — design phase)

Per dispatch §"Stop conditions (12.5K-C-A design)":

- Plan does NOT include all 4 stay-wrong axes (MW-17 + MW-40 + MW-45 + MW-47) → ✅ Plan covers all 4 axes (§3)
- Plan does NOT specify pilot-first 5-hand gate per axis → ✅ Per-axis pilot-first gate documented in §4
- Plan recommends solver-as-labels for any axis → ✅ §6 rule 6 explicit prohibition; D-phase Opus tier-up uses Sonnet+Opus, never solver-as-labels
- Plan total cost > ~$300 LLM OR > ~30h wall clock → ✅ ~$65-100 / ~4-6h (well under cap)
- Plan does NOT specify per-axis ref_id namespace → ✅ §5 explicit `PILOT_LEVER_C_<AXIS>_001..050` per axis
- Plan recommends labels NOT independently verified by Sonnet+Opus tier-up → ✅ §7 D-phase Opus tier-up on canonical hands per axis

No stop conditions triggered.

**Design-phase additional consideration**: if QC at audit flags the MW-40 axis re-use as scope-creep (adding 20 fresh + re-using 30 already-labelled creates a cleanliness question about the 30-hand corpus's existing labels feeding into Lever C training), apply orchestrator-decision-routed fallback (drop MW-40 special case; do all 50 fresh hands). NOT triggered in design; surfaced for QC consideration.

## §9 What this PR does NOT do (per dispatch)

- ❌ Does NOT execute any labelling (this is design only)
- ❌ Does NOT modify v3.x prompts
- ❌ Does NOT modify `river-rats-core/` source
- ❌ Does NOT modify BATCH2 reference
- ❌ Does NOT touch existing 788-corpus or labels
- ❌ Does NOT touch the existing 12.5I-MW40-VERIFICATION corpus (read-only reference for the MW-40 axis re-use plan)
- ❌ Does NOT auto-fix Lever B's report (orchestrator-scope)
- ❌ Does NOT recommend skipping pilot-first per axis (binding; included in §4)
- ❌ Does NOT recommend solver-as-labels (§6 rule 6 explicit prohibition)
- ❌ Does NOT recommend BATCH2 reference update at -E (graduation decisions are orchestrator-scope)

## §10 Risks + open questions for orchestrator

Per `feedback_orchestrator_decides_not_recommends.md`: experts (this builder, architect hat) recommend HOW; orchestrator decides WHAT/WHETHER.

| # | Risk / question | Builder default (committed) | When orchestrator must override |
|---|---|---|---|
| R1 | MW-40 axis special-case (re-use 30 already-labelled + add 20 fresh) — design optimization saves ~$30 LLM + ~30 min but introduces a cleanliness concern (30 of the 50 MW-40-axis training rows come from a verification round dataset with confirmed BET labels; the labels are CORRECT but the data origin differs from the other axes' fresh 50). | Re-use the 30; document the dual-source clearly in -B/-C reports | If orchestrator wants axis-uniformity → drop MW-40 special case; do all 50 fresh hands (cost +$30 LLM + ~30 min) |
| R2 | Per-axis off-ramp risk: if 2+ axes fail pilot, the augmented-data round produces a small partial expansion (e.g., 50-100 fresh rows from 1-2 axes only). May be insufficient to move the model's decision boundary. | Per-axis off-ramp with documented fail-discovery; orchestrator decides at -C completion whether partial scale warrants -E retrain or whether to off-ramp Lever C entirely | If orchestrator wants axis-fail HALT (treat 1+ axis fail as Lever C failure) → off-ramp to direct re-design |
| R3 | The MW-40-VERIFICATION-C HALT pattern (Sonnet 25/25 BET + Opus 5/5 BET; predicted CHECK) showed that the labelling pipeline can disagree with structural arguments. The per-axis pilot-first gate explicitly handles this, but if MW-17/45/47 also reveal pipeline disagreement with their canonical labels, that's an MW-40-style "structural argument empirically too narrow" for those axes — and would invalidate the entire Lever C augmented-data hypothesis (the model can't be taught CALL on MW-17 if the labelling pipeline says FOLD on those hands). | Per-axis pilot reveals this cleanly; orchestrator decides per-axis go/no-go after pilot | None — design supports |
| R4 | The 788 → 988 corpus expansion at -E is +25% in size; but the new 200 rows are concentrated on 4 axes that comprise ~20% of the reference set (4 stay-wrong / 40 reference). The class-imbalance axis remains: FOLD/CALL stay at 10-15% of corpus even after expansion. | Document class ratios at -E; observe whether expansion helps; cap Lever C scope at 200 unless orchestrator approves more | Future phase 12.5M may need explicit class re-weighting OR larger expansion if class imbalance remains the bottleneck (design plan §10 R6 from PR #257 carry) |
| R5 | The 30 already-labelled MW-40-axis hands have consensus BET 1.00 confidence per labeller (PR #241/#245). Their labels are stronger than typical 5-Sonnet consensus (often 0.6-0.8 confidence). When integrated into 988-corpus, these 30 rows will be heavily weighted by `consensus_confidence=1.0`. May dominate over the new fresh rows. | Document the confidence-weighting interaction in -E trainer report; orchestrator decides whether to down-weight the re-used 30 | If orchestrator wants uniform-weighting → manually set the 30 re-used rows to 0.8 confidence; loss of signal but more uniform representation |
| R6 | If any axis's pilot reveals the labelling pipeline routes via a v3.4 DO NOT rule that contradicts the canonical (mirroring MW-40's DO NOT Rule 11 OOP-only finding), that axis needs re-design BEFORE further labelling. The 5-hand pilot is fast; this risk is bounded. | Surface to orchestrator on pilot HALT; per-axis design tweak is a -A2 dispatch if needed | Orchestrator decides per-axis re-design vs drop |

## §11 Cost / time budget (Lever C end-to-end, informational; this PR is design-only ~$0)

| Phase | Cost | Wall clock |
|---|---|---|
| -A (this PR) | ~$0 | ~30-45 min |
| -B (situation gen) | ~$0 | ~15-20 min |
| -C (labelling round) | ~$50-80 LLM (5 Sonnet × ~170 hands × ~$0.05) — assumes MW-40 special case re-uses 30 already-labelled; if all 200 are fresh: ~$50 | ~2-3 hours |
| -D (Opus tier-up) | ~$15-20 LLM (20 Opus × $0.75-1) | ~30 min |
| -E (corpus + re-train) | ~$0 | ~1-2 hours |
| **Total** | **~$65-100 LLM** | **~4-6 hours** |

Within ~$300/30h auto-approval cap. If MW-40 special case is rejected (R1 override): cost +$30 LLM, +~30 min.

## §12 Deliverable scope (this PR)

1 file in PR diff: `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` (this comm).

No supporting analysis files this round; the per-axis structural arguments are fully expressed in §3-4. If QC at audit flags that a separate per-axis composition-quad breakdown table would help, that fix-forward goes to a -A2 amendment PR per `feedback_explicit_action_trigger.md`.

## §13 References

- Dispatch (fire trigger): `MAIN_TERMINAL_PR265_RESOLUTION_AND_125KCA_DISPATCH_2026-05-07.md` (master `1292233`, PR #268)
- 12.5K design plan §5 (Lever C spec): `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` (master `9798007`, PR #257)
- 12.5K-A Lever A (variance ruled out): PR #261 master `edf04a6`
- 12.5K-B Lever B (hyperparameter ruled out): PR #265 master `d45575b`
- 12.5I-MW40-VERIFICATION-A design (5-phase mini-pipeline pattern + Hybrid pilot-first 4-check precedent): PR #228 master `e0e0304`
- 12.5I-MW40-VERIFICATION-B corpus (30 hands; reusable for MW-40 axis per §3): PR #236 master `a20b495`
- 12.5I-MW40-VERIFICATION-C/D (BET 25/25 + 5/5 consensus on the 5 pilot hands; MW-40 axis labelling-pipeline output is BET): PR #241/#245
- 788-corpus baseline: master `48084c3` (PR #222)
- v3.4 protocol prompt: `prompts/gto_labeller_v3.4.md`
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (MW-30/46/47)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md` (per-axis pilot + Opus tier-up at -D), `feedback_orchestrator_decides_not_recommends.md`, `feedback_solver_findings.md` (finding 4: nut blocker effect), `feedback_solver_vs_expert_labels.md`, `feedback_attention_flags_when_features_change.md` (61-surface per-axis activation reporting at -E)

**Status: 12.5K-C-A Lever C design complete. 4 stay-wrong axes (MW-17 / MW-40 / MW-45 / MW-47) at 50 parametric variants each = 200 total. Per-axis pilot-first 5-hand gate + per-axis off-ramp. MW-40 axis special case (re-use 30 already-labelled + 20 fresh) noted as orchestrator-decision item R1. Total Lever C budget ~$65-100 LLM / ~4-6 hours. PR opens for QC audit. Builder ready for 12.5K-C-B (situation generation) on this PR's merge.**
