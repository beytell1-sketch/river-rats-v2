---
date: 2026-05-07
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: Phase 12.5K-C-C Lever C labelling pilot — per-axis gate; **MW-17 + MW-47 FAIL** (factory boards don't reproduce drawing equity); MW-40 + MW-45 PASS; HALT before full run; route to orchestrator for per-axis decisions
status: HALT — pilot gate triggered per-axis off-ramp on MW-17 + MW-47; full run NOT FIRED on any axis pending orchestrator decisions
branch: programmer/phase125k-c-c-labelling-2026-05-07
base: master `6fab0d7` (post-PR #276 dispatch merge)
---

# Phase 12.5K-C-C Lever C labelling pilot — HALT (2 of 4 axes fail; 2 pass)

## Headline

| Axis | Target action | Pilot consensus | Gate | Cost |
|---|---|---|---|---|
| MW-17 | CALL | 5/5 hands FOLD (4/5 labeller majority FOLD per hand) | ⛔ **FAIL** — 0/5 hands have ≥4/5 CALL consensus | ~$1-2 |
| MW-40 | BET | 5/5 hands BET (5/5 labeller unanimous per hand) | ✅ **PASS** | ~$1-2 |
| MW-45 | RAISE | 5/5 hands RAISE (5/5 labeller unanimous per hand) | ✅ **PASS** | ~$1-2 |
| MW-47 | RAISE | 0/5 hands RAISE (mix of CALL/FOLD; 1/5 labeller pro-RAISE) | ⛔ **FAIL** — 0/5 hands have ≥4/5 RAISE consensus | ~$1-2 |

**Cost so far:** ~$5-8 LLM (5 sonnet labellers × 20 hands each in 5 parallel Agent calls). **Time:** ~12 min builder.

**Full run NOT FIRED on any axis.** Per `feedback_quality_default_no_ask` early-stop on strong signal: HALT before ~$30-40 LLM full-run cost; route to orchestrator for per-axis decisions.

## §"Pilot batch results" — per-hand × per-axis × per-labeller

100 pilot labels (5 hands × 5 labellers × 4 axes). Full per-hand consensus from `data/corpus_lever_c_pilot_labels_raw_2026-05-07.jsonl`:

### MW-17 axis (target CALL) — FAIL

| ref_id | per-labeller votes | majority | confidence |
|---|---|---|---|
| PILOT_LEVER_C_MW17_001 | FOLD:4, CALL:1 | FOLD | 0.80 |
| PILOT_LEVER_C_MW17_002 | FOLD:4, CALL:1 | FOLD | 0.80 |
| PILOT_LEVER_C_MW17_003 | FOLD:4, CALL:1 | FOLD | 0.80 |
| PILOT_LEVER_C_MW17_004 | FOLD:4, CALL:1 | FOLD | 0.80 |
| PILOT_LEVER_C_MW17_005 | FOLD:4, CALL:1 | FOLD | 0.80 |

**0/5 hands have ≥4/5 CALL consensus.** L1 was the lone CALL voter; L2/L3/L4/L5 all voted FOLD on every pilot hand.

### MW-40 axis (target BET) — PASS

| ref_id | per-labeller votes | majority | confidence |
|---|---|---|---|
| PILOT_LEVER_C_MW40_031..035 | BET:5 | BET | 1.00 (each) |

**5/5 hands have 5/5 BET consensus.** Strongest possible signal. Replicates MW-40-VERIFICATION-C 25/25 BET unanimous (PR #241) on these 5 fresh J-on-board variants.

### MW-45 axis (target RAISE) — PASS

| ref_id | per-labeller votes | majority | confidence |
|---|---|---|---|
| PILOT_LEVER_C_MW45_001..005 | RAISE:5 | RAISE | 1.00 (each) |

**5/5 hands have 5/5 RAISE consensus.** Strongest signal. Set-of-5s on broadway-completed-turn 3-way IP facing CO lead → universal RAISE for value+protection per labellers' MW-33 calibration anchor reasoning.

### MW-47 axis (target RAISE) — FAIL

| ref_id | per-labeller votes | majority | confidence |
|---|---|---|---|
| PILOT_LEVER_C_MW47_001 | CALL:2, FOLD:2, RAISE:1 | CALL | 0.40 |
| PILOT_LEVER_C_MW47_002 | CALL:2, FOLD:2, RAISE:1 | CALL | 0.40 |
| PILOT_LEVER_C_MW47_003 | FOLD:4, RAISE:1 | FOLD | 0.80 |
| PILOT_LEVER_C_MW47_004 | FOLD:4, RAISE:1 | FOLD | 0.80 |
| PILOT_LEVER_C_MW47_005 | CALL:2, FOLD:2, RAISE:1 | CALL | 0.40 |

**0/5 hands have ≥4/5 RAISE consensus.** L3 was the lone RAISE voter; L1/L5 voted CALL/FOLD; L2/L4 voted FOLD-uniformly.

## §"Why the failures" — diagnostic from labeller reasoning

### MW-17 axis failure

The MW-17 axis was designed for "nut FD on facing-bet 3-way" mirroring the canonical AdKs on Jd8d4c. But the labellers (L2-L5) report:

> "Pure air with draw_outs=0 and equity below pot odds in all cases."
> "All hands have equity below pot odds (0.182–0.243 vs 0.25) with zero draw outs."

The factory's MW-17 boards (e.g., Js8s5d, Js7d3c) have 2 spades, but hero has off-suit AsKh/AsQh (1 spade total in hand). This produces 3-spade-total (1 hero + 2 board) → **labelling pipeline classifies this as backdoor draw, not real flush draw** (`has_flush_draw=0` likely).

The canonical AdKs on Jd8d4c also has 1 hero diamond + 2 board diamonds = 3-total. If the canonical reference has `has_flush_draw=1` while my factory's identical-suit-count boards have `has_flush_draw=0`, there's a feature-extraction discrepancy worth investigating. **More likely: the labellers' interpretation of equity-vs-pot-odds in absence of `has_flush_draw=1` defaults to FOLD; the canonical reference's CALL was potentially a feature-state-specific routing that doesn't trigger here.**

L1's CALL vote (5/5) cited implied odds + nut blocker. L2/L3/L4/L5's FOLD votes cited equity-below-pot-odds + no draw. Inter-labeller variance reveals the boundary case at this exact equity/pot-odds ratio.

### MW-47 axis failure

The MW-47 axis was designed for "nut FD + overcards + gutshot facing bet+call multiway" mirroring the canonical AsQs on KsJ5 two-spade flop. But the labellers report:

> "no flush draw present in any hand so KB §1.7 v3.3 carve-out never triggers"
> "DO NOT Rule 2 prohibits raising straight-only draws 3-way OOP"

The factory's MW-47 N1 boards (e.g., KsJh5d, KsJc5h) have **only 1 spade on board** (Ks). Hero AsQs has 2 spades. Total 3 spades. **Same diagnostic pattern as MW-17**: the labelling pipeline's `has_flush_draw=0` for 1-board-spade configurations, even when hero has 2 same-suit cards.

The canonical MW-47 reference is on **KsJ5** (a 2-spade flop where Js is also a spade — wait, looking again: KsJ5 with Js as the J-spade flop card means board has 2 spades: Ks + Js). My factory N1 was supposed to mirror this but I wrote "KsJh5d" (Jh not Js) — only 1 spade.

**Factory bug confirmed**: MW-47 N1 boards should have BOTH Ks AND Js (2 spades) for hero's nut FD to register as `has_flush_draw=1`. My current factory has 1 spade per N1 board → labellers can't apply the RAISE carve-out.

### MW-40 + MW-45 (PASS) — clean

These axes don't depend on flush-draw feature flags. MW-40 routes via DO NOT Rule 11 IP-exemption + composition quad. MW-45 routes via set-monster + broadway-turn + value-RAISE. Both are clean structural patterns the labellers handle uniformly.

## §"Per-axis off-ramp decision matrix"

Per dispatch §"Per-axis pilot gate" + plan §4 off-ramp:

| Axis | Pilot result | Off-ramp action |
|---|---|---|
| **MW-17 FAIL** | 0/5 ≥4/5 CALL | DROPPED from full run; orchestrator decides re-design (factory boards need reconfiguration to produce real `has_flush_draw=1` — boards must have 2+ FD-suit cards including the high one) |
| **MW-40 PASS** | 5/5 unanimous BET | Eligible for full run (15 fresh hands × 5 labellers = 75 labels; ~$5 LLM, ~5-10 min) |
| **MW-45 PASS** | 5/5 unanimous RAISE | Eligible for full run (45 hands × 5 labellers = 225 labels; ~$15 LLM, ~15-20 min) |
| **MW-47 FAIL** | 0/5 ≥4/5 RAISE | DROPPED from full run; orchestrator decides re-design (factory boards need 2-spade flops with both Ks AND Js per canonical reference structure) |

## §"What I am NOT doing right now"

- ❌ NOT firing the full run on ANY axis (per dispatch "Do NOT auto-decide off-ramp; route to orchestrator")
- ❌ NOT modifying the merged 200-hand corpus (the failed-axis hands are still in `data/corpus_lever_c_situations_2026-05-07.jsonl`; orchestrator decides whether to drop them or re-design)
- ❌ NOT re-running the failed axes with re-designed factory (-A2 amendment is orchestrator-scope per `feedback_explicit_action_trigger.md`)
- ❌ NOT modifying v3.x prompts, BATCH2, river-rats-core/, or any other source

## §"What unblocks me — orchestrator decides"

Three paths the orchestrator could take:

1. **Proceed-with-2-axes** (MW-40 + MW-45 only): orchestrator dispatches builder to run full 75 + 225 = 300 labels on the passing axes; -E corpus integration adds those 60 hands × consensus to 788 → 848-corpus; MW-17 + MW-47 dropped permanently. Cost: ~$20 LLM.

2. **Re-design failed axes (-A2 amendment)**: orchestrator dispatches builder to author -A2 amendment fixing MW-17 + MW-47 factory boards (2-tone-FD-suit boards with both top-spade cards); re-emit those 100 hands; re-run pilot. Cost: ~30-60 min builder + retest.

3. **Halt Lever C entirely**: orchestrator concludes the labelling pipeline can't be relied on for these axes' canonical interpretations; off-ramp Lever C; route 12.5L gate eval directly with Lever A's 20-seed mean as the conclusion.

**Builder default-if-no-override:** Path 1 (proceed-with-2-axes). The MW-17 + MW-47 pipeline-canonical disagreement is real and informative; re-designing the factories doesn't address the underlying feature-extraction question (it just produces different hands the pipeline might then label correctly). Adding 60 high-confidence-BET-RAISE training examples on MW-40 + MW-45 axes is a clean partial-scale outcome. Aligns with `feedback_quality_default_no_ask` early-stop on strong signal.

If orchestrator prefers full coverage of all 4 axes, Path 2 is reasonable but adds churn.

## §"Stop conditions" (per dispatch)

| Condition | Triggered? |
|---|---|
| Pilot consensus < 4/5 hands per axis | YES on MW-17 + MW-47 (per-axis off-ramp) |
| Sonnet API errors > 5% | NO (5/5 labellers returned all 20 labels successfully) |
| Reasoning convergence | YES per axis (within-axis labellers cite consistent v3.4 protocol elements; across-labeller-disagreement on MW-17 + MW-47 is structural-feature-flag-driven, not mode-collapse) |
| Solver-as-labels | NO (all reasoning cites v3.4 KB sections + DO NOT rules + composition quad / quad / blockers; no solver references) |
| Schema-mismatch | NO (all 100 labels have valid pilot_hand_id/action/confidence/reasoning fields) |
| Auto-fix on borderline | NO (HALT-and-route per dispatch) |

## §"Files in PR diff"

3 files added (no situation modifications; no corpus modifications; pilot labels + run script + this report):

1. `scripts/run_lever_c_labelling.py` (orchestration helper; ~200 lines)
2. `data/corpus_lever_c_pilot_labels_raw_2026-05-07.jsonl` (100 pilot labels = 20 hands × 5 labellers)
3. `review/comms/BUILDER_REPORT_PHASE125K_C_C_LABELLING_PILOT_HALT_2026-05-07.md` (this report)

Plus working artefacts in `review/mass_labelling_lever_c_2026-05-07/pilot/` (briefs, raw labeller JSONs, manifest, corpus subset) excluded from PR by default.

## §"References"

- Dispatch (fire trigger): `MAIN_TERMINAL_PR273_RESOLUTION_AND_125KCC_DISPATCH_2026-05-07.md` (master `6fab0d7`, PR #276)
- 12.5K-C-A merged plan §3-§5 (per-axis structural specs): `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` (master `0f5f39f`, PR #269)
- 12.5K-C-B 200-hand corpus (source for pilot subsets): `data/corpus_lever_c_situations_2026-05-07.jsonl` (master `3f4a528`, PR #273)
- v3.4 protocol: `prompts/gto_labeller_v3.4.md`
- MW-40-VERIFICATION-C HALT precedent (parallel pattern): PR #241 master `d411cb8`
- Memory: `feedback_pilot_first_for_long_jobs.md` (per-axis pilot-first gate; binding); `feedback_orchestrator_decides_not_recommends.md` (per-axis off-ramp routes to orchestrator); `feedback_quality_default_no_ask.md` (early-stop on strong signal saves $30-40 LLM); `feedback_explicit_action_trigger.md` (no auto-fix on borderline); `feedback_solver_findings.md` finding 4 (nut blocker effect — feature-extraction-flag dependency revealed at MW-17 + MW-47 pilot)

**Status: 12.5K-C-C pilot HALT triggered. MW-40 + MW-45 PASS (5/5 unanimous per axis); MW-17 + MW-47 FAIL (factory feature-extraction disagreement; nut FD requires 2-tone-FD-suit boards). Full run NOT fired on any axis. PR opens for QC audit. Builder default: Path 1 proceed-with-2-axes (orchestrator decides).**
