---
date: 2026-05-06
from: LEAD-PROGRAMMER (Builder, architect hat)
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: 12.5I-MW40-VERIFICATION-A design — single template T11'-MW40V (~30 J-on-board parametric variants); Decision 3β verification round; structural prediction CHECK
status: design-only deliverable; situation generation gates on this PR's merge + 12.5J-D-pre clearance per dispatch sequencing
---

# PLAN: 12.5I-MW40-VERIFICATION-A — single-template design (T11'-MW40V; ~30 hands)

## §1 Authority chain

- Owner directive: Decision 3β (defer MW-40 BATCH2 reference update; queue parametric verification round with ≥27/30 CHECK graduation bar) — `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217).
- Orchestrator dispatch: `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` (master `f52a93d`, PR #226). Fire-on-merge condition met (PR #226 merged at master `f52a93d`).
- Builder named: LEAD-PROGRAMMER (architect hat). Active fire-now directive — AUTHOR per `feedback_named_author_builds_not_polls.md`.
- Source for verification target: PILOT_787 in `BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md` (master `994ae67`, PR #213) — Sonnet 3-2 CHECK + Opus HIGH CHECK + structural composition argument vs BATCH2 reference BET MEDIUM.

## §2 Scope

**Single template, single mini-phase deliverable.** Design ~30 J-on-board parametric variants of the MW-40 canonical situation (`AhTs` on `AJ5r` BTN IP non-PFA 4-way SRP all-checked-through, flop street-of-decision) to test whether the structural argument ("J-on-board flips composition quad → CHECK") generalises. If ≥27/30 CHECK consensus at 12.5I-MW40-VERIFICATION-C → MW-40 graduates with 4-source pattern matching MW-25 (PILOT_787 + ≥27 parametric variants + Opus tier-up + structural argument). If <27/30 → structural argument is too narrow; PILOT_787 stays as anomaly; BATCH2 MW-40 reference stays BET MEDIUM.

**Out of scope for this PR:** situation generation (12.5I-MW40-VERIFICATION-B), labelling (-C), Opus tier-up (-D), graduation decision + BATCH2 reference update (-E). All gated downstream of this PR + 12.5J-D-pre.

**Out of scope, full stop:** v3.x prompts, river-rats-core/ source, BATCH2 reference, existing 788-corpus, training-data, model files. Read-only reference to all of these.

## §3 Per-template specification — T11'-MW40V (J-on-board TPMK 4-way checked-through, flop)

### Constraints (locked across all 30 variants)

| Field | Value | Source authority |
|---|---|---|
| `hero_seat` | BTN | mirrors MW-40 reference (`BATCH2_8_RANGE_ANALYSIS.md`) |
| `hero_position` | IP, closes action | mirrors MW-40 |
| `hero_role` | non-PFA (caller, not opener) | mirrors MW-40 |
| `num_opponents` | 3 (4-way SRP preflop) | mirrors MW-40 |
| `street_of_decision` | FLOP | mirrors MW-40 (committed; rejected alternative: turn-of-decision — would dilute the verification signal because PILOT_787 / MW-40 both decide on flop) |
| `prior_actions` (hero-only convention per methodology rule 1) | preflop: caller post-open; flop: action checks to BTN | hero-only convention per `feedback_attention_flags_when_features_change.md` capture discipline |
| `villain_check_through_count` | 3 (PFR + 2 callers all check before hero) | mirrors MW-40 — this is the action-sequence signal that drives the "checked-through 4-way" composition prediction |
| `effective_stack` | 200bb (deep) | mirrors MW-40 SPR profile |
| `hand_category` | 6 (TP medium kicker) | mirrors MW-40 (`is_made_hand=1`, `hand_category=6`) |
| `kicker_class` | T-kicker pinned (TJ) | committed; rejected alternative: include 9-kicker / Q-kicker control variants — would test broader medium-kicker pattern but dilutes the MW-40-specific verification (the prediction is about T-kicker on J-paired board, not all medium-kicker patterns); kept as a follow-up question for orchestrator if -C consensus is borderline |
| `is_rainbow` | 1 on flop (or 1 across flop+turn for J-on-turn variants) | mirrors MW-40 (AJ5r) and isolates the J-blocker / set-of-Js composition effect from FD geometry |
| `pot_odds` | 0.0 (no bet to call) | mirrors MW-40 — the action-sequence signal IS the discriminator |

### Predicted v3.4 output per T-CONTROL (methodology rule 3)

`design_action = CHECK` (uniform across all 30 variants).

**Structural reasoning (prediction to be tested empirically):**

The v3.4 prompt's "composition quad" (`villain_top_pair_plus_pct`, `villain_medium_made_pct`, `villain_draw_pct`, `villain_air_pct`) flips on J-on-board hands relative to non-J-on-board TPMK 4-way checked-through. On `AJ5r`-class boards versus a 4-way SRP checked-through villain range:

- `villain_top_pair_plus_pct` is materially elevated by **set-of-Js** (JJ slowplay + AJ + KJ + QJ + Tx-suited that backed in to TP) compared to a non-paired non-J board where check-through composition is dominated by `medium_made` + `air`
- `villain_medium_made_pct` (worse pairs) shrinks because Jx-broadway holdings are routed into TP+ rather than medium_made
- Net composition: TP+ ↑, medium_made ↓, draws ≈ flat, air ≈ flat → `better_hand_pct` rises above the threshold where thin-value BET on TPMK-T-kicker remains +EV

This is the empirical claim. If 30 J-on-board variants produce ≥27 CHECK consensus from 5 Sonnet labellers each, the prediction holds and MW-40 graduates. If <27, the structural argument generalises poorly and the BATCH2 BET MEDIUM reference stands.

**Solver-as-labels prohibition** (`feedback_solver_vs_expert_labels.md`): the prediction is NOT a solver claim. It is a hypothesis about what the v3.4 labelling pipeline will produce given its current "composition quad" reasoning protocol (`prompts/gto_labeller_v3.4.md` §"composition quad" + Mandatory composition section). The verification tests the labelling pipeline's output, not solver alignment.

## §4 Quantity and class distribution (sub-axes; 10/10/10 split)

Total: **30 parametric variants**, single template, three sub-axes of ~10 each.

### Sub-axis A — J-high flop, hero TPMK on top of J-high (10 variants)

Boards with J as the highest card on flop. Hero `TJ` or `JT`-suited variants where hero pair = pair-of-Js (top pair) with T (or adjacent control) kicker. (Note: this differs slightly from MW-40 canonical where hero is `AhTs` and TPMK = pair-of-Aces; on J-high flops the parallel TPMK = pair-of-Js. The verification is testing the "J-on-board" structural axis, not the "TPMK on top of any board" axis. Sub-axis A pins TPMK = pair-of-Js to keep the J-on-board signal pure.)

- Js9c5h, Js7d3c, Js8h4d, Js9d2c, Js8c4h, Js7h2d, Js9h3c, Js6d4s, Js9c3d, Js7c5d
- Hero hand: TJ (T-kicker pinned)
- Suit variation: hero may or may not hold J-blocker; covered in §"blocker variation" below

### Sub-axis B — J-low flop with J-on-turn (10 variants)

Flop is J-low (no J), turn brings J. Decision is on the **flop** in the 4-way checked-through state — but the structural prediction is that the J-on-turn (when it arrives in -C labelling output) flips the composition quad. **Important ambiguity resolved:** the dispatch text says "J-low flop with J-on-turn" but the 12.5I-MW40-VERIFICATION verification target is the **flop street-of-decision** behaviour (mirroring MW-40). Sub-axis B keeps the decision on the flop with hero TPMK on the flop (T as top pair on the flop) and tests whether the future turn-J expectation already shows up in `villain_top_pair_plus_pct` or `villain_medium_made_pct` for the labelling output. **This sub-axis is a stress-test, not a direct test of the J-on-board prediction;** it tests whether labelling correctly handles "J-on-turn-arriving" forecast composition. If sub-axis B labels behave inconsistently with sub-axes A and C, that tells us the structural argument is actually about board-J-presence at decision time, not about board-J-incidence over the hand.

- 9c5d3h, 7c4d2s, 8h6c2d, 9h6c3s, 8c5d2h, 7d4s2c, 9s6h4d, 8d5c3s, 7s5h2d, 9d6s4c (all flops); turn = `Js` for each
- Hero hand: hero TT or T9 (TPMK on flop with T as top pair); turn-J reveals AhTs-equivalent runout
- **Open question for orchestrator (committed default if no override):** sub-axis B may be cut to ~5 hands and sub-axis C bumped to ~15 if QC flags scope-discipline concern about the "turn-J forecast" axis blending into MW-40-specific prediction. **Default committed: 10/10/10 split.** If orchestrator overrides → sub-axis B → 5, sub-axis C → 15.

### Sub-axis C — J-medium flop with paired-J or set-of-Js in range (10 variants)

Boards where J is the middle card or J-pair is on flop. Tests the elevated-set-of-Js composition argument directly (the boards where villain set-of-Js combos are densest in their 4-way SRP checked-through range).

- Jh5c2d, Jc8h3s, Jd9c4h, Jh6s3c, Jc7d2s, Jd8c5h, Jh4c2s, Jc9h6d, Jd7h3c, JcJh4s (last is J-paired flop — extreme test case where set-of-Js composition spikes; included as 1 boundary variant; remaining 9 are J-medium)
- Hero hand: TJ (T-kicker pinned, pair-of-Js top pair)

### Blocker variation (per `feedback_solver_findings.md` finding 2 — blocker-effect sensitivity)

Within each sub-axis, **5 of 10 variants** include hero J-blocker (e.g., hero holds the off-suit J as kicker on a board with another J), **5 of 10 do not**. This isolates the blocker-effect sensitivity: if J-blocker variants flip back to BET while non-J-blocker variants stay CHECK, the structural argument is dominated by set-of-Js combo density and the labelling pipeline correctly responds to blocker effects. Total: 15 with-J-blocker / 15 without across the 30 variants.

### Manual canonical authoring (Track B equivalent)

**Not used.** Single template, factory-driven from parametric specification (Track A only). All 30 variants emit from the same factory pass with the constraint table above + sub-axis sub-tables. Mirror of T9'-expanded factory pattern from 12.5H-A.

## §5 Track A — situation factory specification

**Output target (12.5I-MW40-VERIFICATION-B scope; not this PR):** 30 situations with ref_ids `PILOT_MW40_VERIF_001..030` (clean disjoint namespace per dispatch §"Cap-binding pre-flight"; no collision with the 788-corpus PILOT_695..PILOT_788 range nor with any 12.5I-A/B/C ref_ids).

**Factory inputs:**
- Constraint table (§3 above)
- Sub-axis tables (§4 above; 10 boards × 3 sub-axes)
- Hero hand spec per sub-axis (TJ or TT/T9)
- Suit-permutation table for blocker variation (5 with-J-blocker / 5 without per sub-axis)

**Factory output structure (per situation):**
- `ref_id`: `PILOT_MW40_VERIF_NNN` (zero-padded 3-digit)
- `feat_dict`: 61-surface (post-PR #205); all 61 keys populated by `feature_extractor.extract_features` over the synthesized hand state
- `hero_cards`: top-level field (matches 788-corpus pattern; required for label-file feat_dict backfill if any future re-extraction is needed)
- `prior_actions`: hero-only convention (no villain action records beyond preflop opener position + check-through count)
- `design_action`: `CHECK` per §3 prediction
- Standard metadata (template_id = `T11_MW40V`, sub_axis = `A`/`B`/`C`, blocker_variant = `with_J_blocker`/`no_J_blocker`)

**Pre-flight checks (12.5I-MW40-VERIFICATION-B scope):**
- ref_id namespace disjoint from 788-corpus + all prior 125i ref_ids → STOP if collision
- All 30 situations produce non-NaN/non-Inf feat_dict on all 61 keys → STOP if ≥1% NaN/Inf
- Step-18 features (`nut_blocker_overcard_count`, `bet_call_multiway_oop_raise_pressure_index`) compute as predicted: both expected ≈ 0 across all 30 variants (hero is IP not OOP, no nut-FD blocker semantics on J-on-board). Flag any non-zero activations explicitly per `feedback_attention_flags_when_features_change.md`.
- Distribution sanity: `is_made_hand=1` for 30/30, `hand_category=6` for 30/30, `is_ip=1` for 30/30, `num_opponents=3` for 30/30
- Cross-axis sanity: 10 / 10 / 10 split exact across sub-axes A/B/C

## §6 Methodology rules (7 standing per 12.5I-A precedent)

| # | Rule | Application to MW-40-VERIFICATION |
|---|---|---|
| 1 | Hero-only convention in `prior_actions` | Yes — uniform across all 30 variants per §5 factory spec |
| 2 | Pre-flight join-cardinality ≥0.99 vs existing 788-corpus | Yes — but MW-40-VERIFICATION corpus is a NEW namespace (`PILOT_MW40_VERIF_*`), so join-cardinality = 30/30 = 1.00 by construction; cardinality check applies at 12.5K combined re-train if these 30 are added to the corpus (gated on -E graduation outcome) |
| 3 | `design_action` field per hand for T-CONTROL-like rows | Yes — `CHECK` uniform per §3 prediction |
| 4 | Pilot-first does NOT apply at 12.5I-B (situation generation is deterministic factory output) | Inherited: 12.5I-MW40-VERIFICATION-B is also deterministic factory; no pilot-first needed at -B |
| 5 | Pilot-first DOES apply at 12.5I-C (labelling round; Sonnet × 5 × ~30 hands) | Yes — at -C: 5-hand Sonnet pilot before full 30-hand × 5-labeller run, gate on coherent CHECK majority in pilot before scaling, halt if pilot diverges from prediction with sub-axis-specific patterns. Per `feedback_pilot_first_for_long_jobs.md`: tier-up verification (Sonnet → Opus cross-check on canonical hands) at -D |
| 6 | Solver-as-labels prohibited per `feedback_solver_vs_expert_labels.md` | Yes — solver may be consulted to verify the "elevated set-of-Js composition" prediction at -D Opus tier-up audit, but never as labels for the 30 variants |
| 7 | Cross-seed importance reporting at 12.5I-E | Yes — IF -E graduates and these 30 variants merge into corpus 818, the 12.5K trainer report verifies Step-18 feature activations on the 30 (predicted ≈ 0 for both); flag any deviation from the §5 prediction |

**Cap-binding pre-flight** (additional rule per dispatch): ref_id namespace `PILOT_MW40_VERIF_001..030` verified disjoint vs 788-corpus + all prior 12.5I ref_ids before -B emits situations.

## §7 Sequencing — multi-phase 12.5I-MW40-VERIFICATION workstream

| Phase | Scope | Gate | Owner |
|---|---|---|---|
| **A (this PR)** | Design + plan | this PR opens; QC audit pre-merge | LEAD-PROGRAMMER (architect hat) |
| Pause: 12.5J-D-pre | Test-guard deflake (engineering scope; Option b tier-2 Δ-tolerance) | A merge | LEAD-PROGRAMMER (programmer hat); separate dispatch |
| **B** | Situation generation (30 variants; factory pass) | 12.5J-D-pre merge | LEAD-PROGRAMMER (programmer hat); separate dispatch |
| **C** | Labelling round (5 Sonnet × 30 hands; pilot-first 5-hand gate) | B merge | LEAD-PROGRAMMER (programmer hat); separate dispatch; ~$5-10 LLM cost |
| **D** | Opus tier-up cross-check on canonical hands + verification verdict | C QC PASS | LEAD-PROGRAMMER + Opus tier-up subprocess; ~$3-5 LLM cost |
| **E** | BATCH2 reference update PR (graduation-pass case) OR memo-only PR (graduation-fail case) | D verdict | LEAD-PROGRAMMER (BATCH2 update authored by builder; orchestrator-scope decision to dispatch) |

Builder remains single-stream serial. Slower stream sets pace per `feedback_orchestrator_controls_parallel_timing.md`. Orchestrator gates each transition with a `MAIN_TERMINAL_*_DISPATCH` comm naming LEAD-PROGRAMMER per `feedback_explicit_action_trigger.md`.

## §8 Stop conditions (this PR — design phase)

Per dispatch §"Stop conditions" + design-phase amendments:

- Design diverges from per-hand Decision 3β scope (MW-40-specific J-on-board only; do not blend in MW-17/45/47 axes) → STOP
- Per-template count below 30 hands → STOP
- Solver-as-labels appears in the design comm → STOP
- Factory parametric ranges introduce non-J-on-board boards (sub-axis B's J-low flop / J-on-turn is the exception by construction; documented in §4) → STOP unless documented exception
- `design_action` prediction differs from CHECK without explicit structural reasoning per §3 → STOP

**Design-phase additional stop:** if QC flags sub-axis B as scope-violation (turn-J forecast not in MW-40 prediction surface), apply the §4 fallback (sub-axis B → 5; sub-axis C → 15) on a fix-forward PR; do NOT auto-fix without orchestrator directive per `feedback_explicit_action_trigger.md`.

## §9 What this PR does NOT do (per dispatch)

- Does NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Does NOT modify river-rats-core/ source (read-only reference)
- Does NOT modify BATCH2 reference (orchestrator-scope; locked until -E)
- Does NOT touch existing 788-corpus or any prior-phase corpus files
- Does NOT generate situations (12.5I-MW40-VERIFICATION-B scope)
- Does NOT label hands (12.5I-MW40-VERIFICATION-C scope)
- Does NOT run Opus tier-up (12.5I-MW40-VERIFICATION-D scope)

## §10 Risks + open questions for orchestrator

Per `feedback_orchestrator_decides_not_recommends.md`: experts (this builder, architect hat) recommend HOW; orchestrator decides WHAT/WHETHER. Where I have committed to a position, no question is raised. Where scope is ambiguous, I flag it.

| # | Risk / question | Builder default (committed) | When orchestrator must override |
|---|---|---|---|
| R1 | Sub-axis B (J-low flop with J-on-turn) is a stress-test of "future-J expectation in composition quad" rather than a direct test of board-J-at-decision-time. Mixing it with sub-axes A and C may add noise. | 10/10/10 split kept; sub-axis B's signal will be assessed at -C via per-axis CHECK consensus | If orchestrator wants pure "J-at-decision-time" test → drop sub-axis B → 15/0/15 |
| R2 | Adjacent-kicker control variants (9-kicker, Q-kicker) are out of scope. The verification only tests T-kicker on J-paired boards. If -C consensus is borderline (24-26/30), the design cannot disentangle "T-kicker-specific" from "all-medium-kicker" patterns. | T-kicker pinned for the 30 variants; adjacent-kicker investigation is a follow-up phase if -C is borderline | If orchestrator wants pre-emptive disentanglement → expand to 15 T-kicker / 15 adjacent — but raises -C cost to 75-150 hands |
| R3 | The "composition quad" terminology in v3.4 prompt differs from the "composition triple" memory note (`feedback_preflop_geometry_vs_postflop_composition.md`). Plan uses "composition quad" to match the prompt surface; flagging the memory drift for orchestrator review. | Plan uses "composition quad" throughout; no memory edit proposed (memory edit is owner-scope) | If orchestrator wants memory note refreshed → owner directive needed |
| R4 | If -C produces 27/30 CHECK exactly (the threshold floor), graduation is ambiguous (statistical noise within 5-labeller × 30-hand sampling). | At threshold, recommend orchestrator either accept graduation (matching MW-25 4-source pattern) or commission a 30-hand re-run with 7 Sonnet labellers for tighter consensus measurement | Orchestrator decides which side of the threshold floor to land on if -C arrives there |
| R5 | The PILOT_787 source report did not include the Opus tier-up verdict text (per Explore brief §3). The 4-source bar for graduation depends on Opus HIGH CHECK at -D being independently re-confirmed on canonical hands. | Plan assumes Opus tier-up at -D will reproduce the original PILOT_787 Opus HIGH CHECK; if Opus diverges at -D, graduation halts regardless of Sonnet 27/30. | Orchestrator decides whether divergent Opus output is a halt-and-redesign event or a memo-only graduation-fail event |

## §11 Cost / time

**This PR (design phase):** ~$0 (no LLM calls; document authoring; one Explore agent burst for grounding ≈ pennies). ~30-45 min builder wall clock; this comm at ~3000 words.

**Downstream phases (informational):**
- B (situation gen): ~$0 (factory script); ~15-20 min
- C (labelling): ~$5-10 (5 Sonnet × 30 hands × ~$0.05/hand); ~30-45 min
- D (Opus tier-up): ~$3-5 (Opus on ~5-10 canonical hands); ~15-20 min
- E (BATCH2 update or memo): ~$0; ~15-30 min depending on graduation-pass vs graduation-fail authoring

**Total verification round (B+C+D+E):** ~$8-15 + ~75-115 min wall clock — well within the Decision 3β budget ("~$10-15 + 1-2 hours wall clock").

## §12 Deliverable scope (this PR)

1 file in PR diff: `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (this comm).

No supporting analysis files this round; the structural argument is fully expressed in §3-4. If QC at audit flags that a separate composition-quad breakdown table would help, that fix-forward goes to a -A2 amendment PR per `feedback_explicit_action_trigger.md` — not silently to this PR.

## §13 References

- Dispatch (fire trigger): `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` (master `f52a93d`, PR #226)
- Decision 3β source: `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217)
- PILOT_787 labelling source: `BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md` (master `994ae67`, PR #213)
- BATCH2 MW-40 reference (current state): `BATCH2_8_RANGE_ANALYSIS.md` (research path)
- Template precedent: `PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md` (master `54e2943`)
- 788-corpus baseline: master `48084c3` (PR #222)
- v3.4 labelling prompt: `prompts/gto_labeller_v3.4.md` (composition quad surface)
- Memory: `feedback_quality_default_no_ask.md` (4-source bar matching MW-25), `feedback_pilot_first_for_long_jobs.md` (Sonnet pilot + Opus tier-up at -C/-D), `feedback_orchestrator_decides_not_recommends.md` (expert HOW / orchestrator WHAT), `feedback_solver_findings.md` finding 2 (blocker-effect sensitivity), `feedback_solver_vs_expert_labels.md` (solver-as-labels prohibited), `feedback_attention_flags_when_features_change.md` (Step-18 capture discipline), `feedback_named_author_builds_not_polls.md` (named-author AUTHOR), `feedback_explicit_action_trigger.md` (no auto-fix; fix-forward via dispatch)

**Status: 12.5I-MW40-VERIFICATION-A design complete (single template T11'-MW40V; 30 variants; 10/10/10 sub-axis split with blocker variation; design_action = CHECK uniform; structural prediction documented per §3). PR opens for QC audit. Builder ready for 12.5J-D-pre dispatch on this PR's merge per dispatch sequencing.**
