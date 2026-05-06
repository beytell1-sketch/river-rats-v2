---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5I-C pilot HALT — T8'-redesigned uniformly CHECK-labelled (5/5 hands including 2 manual canonicals); 12.5I-A §9 open question now operationalized
status: HALT — pilot complete, full phase NOT triggered, awaiting orchestrator direction
branch: programmer/phase125i-c-labelling-2026-05-06
base: master `a635bcb`
pilot brief: /tmp/mass_labelling_125i_pilot/labeller_1_brief.md (transient)
pilot output: /tmp/mass_labelling_125i_pilot/labels_v3_4_labeller_1.json (transient)
---

# 12.5I-C pilot HALT — T8'-redesigned protocol-vs-reference disagreement

## Per-dispatch stop condition triggered

> **From dispatch §"Stop conditions":** *"Manual canonical pilot >1 divergence from prediction → STOP, route to orchestrator (per 12.5H-C precedent)."*

**2 of 4 manual canonicals diverged** from prediction (PILOT_785 + PILOT_786, both T8'-redesigned). Per dispatch literal STOP rule, full Sonnet × 5 × 94 phase NOT triggered.

**Substantive finding:** the entire T8'-redesigned template (5/5 pilot hands including BOTH manual canonicals) routes to **CHECK** uniformly under v3.4. The 12.5I-A §9 open question on MW-25 reference re-evaluation is now operationalized — corpus + protocol + model all align on CHECK; BATCH2 reference (BET) is the outlier.

T9'-expanded (3/3) + T10'-redesigned (5/5) are CLEAN.

## Pilot scope

1 Sonnet × 13 hands across 3 templates + 4 manual canonicals.
- Cost: ~$0.30 (well below budget)
- Total labels: 13/13, refusals: 0
- Schema: valid; reasoning traces cite v3.4 clauses correctly
- v3.4 routing: confirmed (KB §1.7, DO NOT Rule 2 fired correctly)

## Pilot results table

| pilot_hand_id | template | predicted | labeller_1 | match | confidence |
|---|---|---|---|:---:|---|
| PILOT_695 | T8'-redesigned (parametric #1) | BET | **CHECK** | ✗ | (varies) |
| PILOT_710 | T8'-redesigned (parametric #16) | BET | **CHECK** | ✗ | |
| PILOT_722 | T8'-redesigned (parametric #28) | BET | **CHECK** | ✗ | |
| PILOT_727 | T9'-expanded (parametric) | BET | BET | ✓ | |
| PILOT_745 | T9'-expanded (parametric) | BET | BET | ✓ | |
| PILOT_756 | T10'-redesigned (parametric) | RAISE | RAISE | ✓ | |
| PILOT_757 | T10'-redesigned (parametric) | RAISE | RAISE | ✓ | |
| PILOT_770 | T10'-redesigned (parametric) | RAISE | RAISE | ✓ | |
| PILOT_784 | T10'-redesigned (parametric) | RAISE | RAISE | ✓ | |
| PILOT_785 | **T8' canonical 01 (MW-25 EXACT REPLICA: Ks7s on As9s5d)** | BET | **CHECK** | ✗ | |
| PILOT_786 | **T8' canonical 02 (non-nut FD: Tc9c on Qh5c3c)** | BET | **CHECK** | ✗ | |
| PILOT_787 | T9' canonical (MW-40 exact: AhTs on AdJc5h rainbow) | BET | BET | ✓ | |
| PILOT_788 | T10' canonical (MW-45 adjacent: 6d6s on AsKh6cQd) | RAISE | RAISE | ✓ | |

**Match rate: 8/13 (62%).** **All 5 T8'-redesigned hands FAIL prediction (uniform CHECK).** **All 8 T9'-e + T10'-r hands MATCH prediction (100%).**

## Diagnosis: T8'-redesigned protocol-vs-reference disagreement (operationalized)

### Labeller reasoning on PILOT_785 (MW-25 EXACT REPLICA)

> *"This is a drawing hand (flush draw, 9 outs, spades — Ks7s on As9s5d). The board Ace of spades (As) is ON THE BOARD, not in hero's hand; hero holds Ks7s — a King-high (second-nut) spade flush draw. Since hero cannot hold the As (it is on the board), hero cannot possess the nut FD blocker required by KB §1.7 (nut_flush_block=0 confirms this). **KB §1.7 semi-bluff RAISE carve-out therefore does NOT trigger despite villain_air=0.34 > 0.20.** Hero is NOT the preflop aggressor (is_preflop_aggressor=0), so no c-bet role. **DO NOT Rule 2 applies: non-nut FD 3-way — CHECK to realise equity for free IP.**"*

### Labeller reasoning on PILOT_786 (non-nut FD contrast variant)

> *"Hero holds Tc, not Ac — not the nut FD (nut_flush_block=0); KB §1.7 semi-bluff RAISE requires the canonical Ace-of-the-flush-suit blocker, which is absent. villain_air=0.549 is very high, but **the absence of the nut blocker means DO NOT Rule 2 governs**: betting a non-nut flush draw into 3 opponents 3-way is -EV regardless of air fraction because fold equity requires simultaneous folds from multiple opponents."*

### The structural problem

v3.4 protocol routes T8'-family hands to CHECK uniformly when:
- Hero has FD WITHOUT nut blocker (DO NOT Rule 2 fires)
- AND hero is NOT the PFA (no c-bet role)
- AND no facing bet (KB §1.7 RAISE carve-out cannot fire)

ANY T8' configuration satisfying these 3 conditions → CHECK regardless of:
- villain_air (even at 0.55 doesn't help)
- Hero's specific composition (K-high FD vs non-nut FD vs anything else)
- Board texture (monotone vs two-tone)
- Number of opponents (Rule 2 fires for 3-way+)

The 12.5I-A T8'-redesign **could not** rescue this because the deeper protocol-vs-reference disagreement is between:
- **v3.4** (corpus + model + protocol): CHECK on non-PFA-non-facing-bet draws in 3-way+
- **BATCH2 MW-25 reference**: BET (denial + thin value via fold equity from three checks)

This validates 12.5I-pre diagnostic §"Cross-hand patterns" Pattern 1 + 12.5I-A §9 open question: **MW-25 BET expert may itself be GTO-incorrect** OR v3.4 protocol may need a BET-after-checked-through-multiway clause.

## What's CLEAN

- **T9'-expanded**: 3/3 BET match (PILOT_727, 745, 787 — including MW-40 exact replica). Protocol routing solid.
- **T10'-redesigned**: 5/5 RAISE match (PILOT_756, 757, 770, 784, 788 — including MW-45 adjacent canonical with broadway-completed turn). Protocol routing solid.
- **64 hands (32 T9'-e + 30 T10'-r + 1 T9' canonical + 1 T10' canonical)** are ready for full Sonnet × 5 × 64 labelling if orchestrator approves T8' deferral.

## Recommendations to orchestrator (3 options)

### Option A: gto-expert reference re-evaluation on BATCH2 MW-25 (RECOMMENDED)

Commission gto-expert-hat (or external GTO authority) review of MW-25 spec. Specific question: is BET on Ks7s on As9s5d (4-way checked through, BTN IP, hero K-high FD with As public on board) GTO-correct?

If YES: v3.4 protocol genuinely has a gap; need protocol amendment (Option B fallback).
If NO: MW-25 expert action should be CHECK; MW-25 graduates from the stay-wrong list at zero corpus cost; T8'-redesigned 30 hands ship as additional CHECK-bucket training (no harm, no MW-25 leverage).

**Cost:** 1-2 hours gto-expert review. **Saves:** ~$2-3 labelling cost on T8' hands + addresses the structural disagreement.

### Option B: v3.4 protocol amendment for non-PFA-non-facing-bet-multiway BET reasoning

Add a clause that allows BET on non-nut-FD-checked-through-multiway when villain_air ≥ 0.40 (or similar threshold). Risky per `feedback_bucket_first_labelling.md` (no equity thresholds in labelling) — but the existing v3.2 KB §1.7 OVERRIDE already uses villain_air thresholds, so precedent exists.

**Cost:** orchestrator + ml-architect + gto-expert design pass; ~3-5 days. **Risk:** thresholds may over-fit MW-25 specifically without generalizing.

### Option C: drop T8'-redesigned from 12.5I-C; proceed with T9'-e + T10'-r only (64 hands)

Skip T8' labelling entirely for 12.5I-C. Ship full Sonnet × 5 × 64 labels for T9'-e + T10'-r only. The 30 T8' hands stay as situations without labels (or get CHECK labels via separate cheap pass since outcome is known).

12.5K combined re-train then trains on:
- 694 (12.5H combined) + 64 (12.5I-C) + 12.5J features = 758 hands × 61 features
- MW-25 stays wrong; MW-40 + MW-45 + MW-17 + MW-47 addressed via T9'/T10'/12.5J

**Cost:** zero additional. **Trade-off:** MW-25 stays wrong; gate score gain reduced from theoretical "MW-25 + MW-40 + MW-45 flips" (3 hands) to "MW-40 + MW-45" (2 hands).

### My recommendation

**Option A first** (gto-expert reference re-evaluation). If gto-expert confirms BET, escalate to Option B. If gto-expert confirms CHECK, proceed with Option C while removing MW-25 from stay-wrong list (graduation at zero cost).

This preserves the slow-quality default per `feedback_quality_default_no_ask.md` — fix the underlying reference question before committing to expensive corpus or protocol changes.

## What's NOT a blocker

- **T9'-expanded + T10'-redesigned (64 hands)** are ready for full labelling on orchestrator approval (Option C path)
- **12.5J-B (PR #205)** is independent of this 12.5I-C halt; feature implementation proceeds in parallel
- **12.5K combined re-train** can still target gate ≥33 via T9'-e + T10'-r + 12.5J features alone (per 12.5I-pre diagnostic estimates: T9' 70-80% MW-40 fix + T10' 50-60% MW-45 fix + 12.5J ~40-50% MW-17/47 fix → ~1.7 expected hand flips → median 33-34)

## What's blocked / what's queued

**Blocked:**
- 12.5I-C full phase → on orchestrator direction (Option A / B / C)
- 12.5I-D / 12.5I-E / 12.5I-F → all downstream of 12.5I-C
- 12.5K combined re-train → on both 12.5I-E and 12.5J-E ship

**Parallel (independent of 12.5I):**
- 12.5J-B PR #205 (feature implementation) — QC trigger pending; not affected by 12.5I-C halt

**NEW orchestrator queue:**
- BATCH2 MW-25 reference re-evaluation (Option A)
- TC-X-DISPATCH-PREDICTION-VERIFICATION third-instance reminder: predictions on T8'-redesigned were inherited from 12.5I-A design which itself flagged uncertainty in §3 + §9. Pilot operationalized the uncertainty per the formalized test class. No further formalization needed.

## References

- 12.5I-C dispatch: master `a635bcb` (PR #206)
- 12.5I-B merged: master `5df39f7` (PR #202)
- 12.5I-A merged: master `d045b03` (PR #197)
- 12.5I-pre diagnostic §"Cross-hand patterns" pattern 1: `review/comms/BUILDER_REPORT_PHASE125I_PRE_DIAGNOSTIC_2026-05-06.md`
- 12.5J-B parallel: master `41a40b9` (PR #205) — independent of this halt
- v3.4 protocol: `prompts/gto_labeller_v3.4.md`
- BATCH2 MW-25 reference: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`
- Memory: `feedback_pilot_first_for_long_jobs.md` (pilot caught the T8' issue cheaply), `feedback_quality_default_no_ask.md` (Option A is slow-quality default), `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5I-C HALT (literal dispatch STOP rule, 2 manual divergences). Recommend Option A (gto-expert MW-25 reference re-evaluation) as slow-quality path. T9'-e + T10'-r CLEAN; ready for full labelling on orchestrator direction. Awaiting orchestrator decision.**
