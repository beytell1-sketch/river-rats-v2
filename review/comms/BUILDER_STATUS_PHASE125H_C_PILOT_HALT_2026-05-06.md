---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5H-C — pilot HALT; 3 of 6 manual canonicals diverge from predicted v3.4 output; route to architect hat per dispatch stop condition
status: HALT — pilot complete, full phase NOT triggered, awaiting orchestrator direction
branch: programmer/phase125h-c-labelling-2026-05-06
base: master `fb6983b` (12.5H-C dispatch HEAD)
pilot brief: /tmp/mass_labelling_125h_pilot/labeller_1_brief.md (transient)
pilot output: /tmp/mass_labelling_125h_pilot/labels_v3_4_labeller_1.json (transient; reproducible)
---

# 12.5H-C pilot HALT — manual canonical divergence

## Per-dispatch stop condition triggered

> **From dispatch §"Stop conditions on pilot":** *"Manual canonical pilot hand consensus disagrees with predicted v3.4 output → STOP, route back to architect hat (situation construction or v3.4 wording may have a gap; earlier the better)."*

**3 of 6 manual canonicals diverged from prediction.** No further labellers dispatched. Full Sonnet × 5 × 90 phase NOT triggered. Awaiting orchestrator direction (architect-hat amendment OR v3.4 prompt amendment OR canonical re-prediction).

## Pilot scope

1 Sonnet × 20 hands (6 manuals + 14 parametric across 6 templates including all 5 design_action buckets in T-CONTROL).
- Cost: ~$0.50 (well below budget)
- Total labels: 20/20, refusals: 0
- Schema: valid; all reasoning traces cite v3.4 clauses correctly
- Per-call cost matches Sonnet 4.6 estimate ✓
- v3.4 routing: confirmed (PILOT_658 + PILOT_694 both fire Fix 2.1.1 clause-e correctly → RAISE)

## Pilot results table

| pilot_hand_id | template | predicted | labeller_1 | match | confidence |
|---|---|---|---|:---:|---|
| PILOT_605 | T8' parametric | (none — exploratory) | CHECK | — | MEDIUM |
| PILOT_620 | T8' parametric | (none) | CHECK | — | MEDIUM |
| PILOT_621 | T9' parametric | (none) | BET | — | MEDIUM |
| PILOT_633 | T9' parametric | (none) | BET | — | MEDIUM |
| PILOT_634 | T10' parametric | (none) | RAISE | — | HIGH |
| PILOT_646 | T10' parametric | (none) | RAISE | — | HIGH |
| PILOT_647 | T7-ext parametric | (none) | **FOLD** | — | HIGH |
| PILOT_658 | T-RAISE-stabilize parametric | (none) | RAISE | — | HIGH |
| PILOT_669 | T-CONTROL CHECK | CHECK | CHECK | ✓ | HIGH |
| PILOT_675 | T-CONTROL BET | BET | BET | ✓ | HIGH |
| PILOT_678 | T-CONTROL BET | BET | BET | ✓ | HIGH |
| PILOT_680 | T-CONTROL FOLD | FOLD | FOLD | ✓ | HIGH |
| PILOT_684 | T-CONTROL CALL | CALL | CALL | ✓ | MEDIUM |
| PILOT_687 | T-CONTROL RAISE | RAISE | RAISE | ✓ | HIGH |
| PILOT_689 | T8' manual canonical | BET | **CHECK** | ✗ | HIGH |
| PILOT_690 | T8' manual canonical | BET | BET | ✓ | MEDIUM |
| PILOT_691 | T9' manual canonical (MW-40 exact) | BET | BET | ✓ | MEDIUM |
| PILOT_692 | T10' manual canonical (MW-45 exact) | RAISE | **CALL** | ✗ | MEDIUM |
| PILOT_693 | T7-ext manual canonical (MW-17 exact) | CALL | **FOLD** | ✗ | HIGH |
| PILOT_694 | T-RAISE-stab manual canonical (MW-47-style) | RAISE | RAISE | ✓ | HIGH |

**Manual canonical match rate: 3/6 (50%).** **T-CONTROL design_action match rate: 6/6 (100%).**

## Three divergences with diagnosis

### Divergence 1: PILOT_689 (T8' monotone canonical) — CHECK not BET (LP-side prediction error)

**Hero:** Ks7h on As9s5s monotone (4-way checked through, BTN IP)

**Labeller reasoning (HIGH confidence):**
> *"Critically: board As9s5s is monotone with As ON the board — any villain holding a single spade already has a made flush. better_hand_pct=0.831 means 83.1% of villain range currently beats hero (made flushes). Hero's Ks 'draw' on an all-spades board does not actually draw to a better hand since the board already has the As; hero needs a spade in hand AND would only make a King-high flush."*

**Diagnosis:** This is an **LP-side prediction error**, not a labeller or protocol issue. The labeller is correct. On monotone-spades boards with the As public, the K-high FD discriminative axis collapses to "non-nut draw vs flush-heavy continuing range" → CHECK is GTO. The 12.5E-B `t1_monotone_fd_checked_through_4way` hands (PILOT_495-506) are *all* labelled CHECK in 12.5E-C for the same reason (verified by inspection of `data/corpus_revision_125e_labels_2026-05-05.jsonl`).

The orchestrator-side prediction "BET for T8'/T9'/T10' hands" in dispatch §"Pilot gate criteria" is therefore wrong for T8' monotone-flop family. The T8' template *itself* is well-formed; just my BET prediction was incorrect.

**Recommendation:** Update predicted action for T8' family to CHECK (matching existing 604 corpus pattern). T8' parametric also labelled CHECK uniformly (PILOT_605, PILOT_620). This is consistent with template family + existing labelled corpus. **No template or protocol change needed.**

### Divergence 2: PILOT_692 (T10' MW-45 canonical) — CALL not RAISE (texture-specific; defensible both ways)

**Hero:** 6d6c (set) on AcKd6hQs turn (4-way: hero BB OOP facing CO turn lead 12bb + BTN call)

**Labeller reasoning (MEDIUM confidence):**
> *"better_hand_pct=0.103 (10.3% of range beats hero — JT makes broadway straight on AKQx board). danger_score=0.880 (very high — AcKdQs+6h completes JT straight). ... RAISE risks committing stacks when 10.3% of villain range has a straight (JT on AKQx), and villain_top_pair_plus=0.485 means the continuing range is value-heavy. CALL is preferred over RAISE here: the danger_score=0.88 and villain_air=0.066 (almost no fold equity to a raise) means RAISE has no fold-equity component and risks committing against the straight-heavy portion."*

**Diagnosis:** GTO is genuinely close on this texture. AKQ-broadway-completed turn with 4-way action turns set-of-6s into a vulnerable middle-bucket monster, not a clean RAISE-for-value-and-protection hand. Both CALL (preserve implied odds at compressed SPR; pot-control vs straight-heavy continuing range) and RAISE (extract value before river-card threat; protection vs draws) are GTO-defensible. The labeller's CALL reasoning is sound.

T10' parametric hands (PILOT_634, PILOT_646) all labelled RAISE — those have NON-broadway turn cards (Td, Tc) that don't bring danger_score this high. So T10' template is well-formed; only the MW-45 canonical's specific board texture is ambiguous.

**Recommendation:** Two paths:
- (a) **Accept the labeller's CALL** as the v3.4 prediction for MW-45-style hands and update prediction to CALL. The MW-45 reference set hand's GTO answer may itself warrant re-validation against this finding.
- (b) **Change manual canonical board** to less broadway-saturated texture (e.g., 6d6c on AcKd6h7s — set on rainbow A-K-6 + 7 turn, no broadway/straight danger) where RAISE is unambiguously correct.

Path (a) is cheaper and informative; path (b) requires architect-hat amendment. Recommend (a).

### Divergence 3: PILOT_693 (T7-ext / literal MW-17 spec) — FOLD not CALL (CRITICAL — protocol-vs-reference gap)

**Hero:** AdKs on Jd8d4c (BB OOP facing CO bet 5bb after BTN folded; 3-way reduced to HU on flop)

**Labeller reasoning (HIGH confidence):**
> *"This is an air hand (AdKs on Jd8d4c — no made hand, no flush draw, no straight draw, draw_outs=0, hand_category=2, is_made_hand=0). Step 1: air bucket — overcards only. better_hand_pct=0.597, equity_vs_range=0.245. Step 2: OOP (BB), HU facing a single bet, villain_air=0.312, villain_top_pair_plus=0.386. pot_odds=0.278. equity_vs_range=0.245 < pot_odds=0.278 (negative equity margin). ... Hero has Ad on Jd8d4c (two-diamond board) — nut flush BLOCKER but NOT a flush draw (Ks is not a diamond). draw_outs=0 confirms no draw path. ... DO NOT Rule 6 warns blockers matter less 3-way, and here this is effectively HU (2 opponents). The nut flush block does not convert air into a calling hand; hero needs to call with equity, not blockers."*

**Diagnosis:** This is a **fundamental protocol-vs-reference gap**.

- **MW-17 reference set spec** (`design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`): hero AdKs on Jd8d4c facing CO bet 3-way; reference action **CALL** with reasoning citing pot odds 26.8% required + nut flush blocker (Ad) + 2 overcards + implied odds via backdoor improvements.
- **v3.4 protocol bucket-first reasoning**: equity_vs_range (0.245) < pot_odds (0.278); draw_outs=0; nut blocker doesn't convert air to call; pure equity-vs-pot-odds → **FOLD**. Per `feedback_bucket_first_labelling.md`, the labeller is forbidden from using equity-threshold reasoning AS the bucket — but it correctly *describes* why the bucket-classified-as-air-hand has insufficient continuing equity.
- **T7-ext parametric PILOT_647** (AcKd on Jc8c4d, same template): also labelled FOLD with HIGH confidence — confirming this is **systemic** to the T7-ext template, not a one-off.

The implication: if we proceed to full Sonnet × 5 × 90 with T7-ext as currently designed, all 12 T7-ext hands (11 parametric + 1 MW-17 canonical) will be labelled FOLD by majority — generating training data that **reinforces** the model's existing FOLD-on-MW-17 misclassification rather than correcting it.

**Recommendation:** This blocks 12.5H-C until resolved. Three orchestrator-level options (LP can't decide):
- (a) **v3.4 protocol amendment** — add an implied-odds + nut-blocker + 2-overcards clause that overrides bucket-first equity reasoning for hands with `nut_flush_block=1 AND overcard_outs >= 2 AND num_opponents <= 2 AND pot_odds <= 0.30`. Targets: MW-17-family hands. Risk: feature-threshold-encoded protocol contradicts `feedback_bucket_first_labelling.md`.
- (b) **MW-17 reference set re-validation** — orchestrator-side Opus + GTO-EXPERT review of MW-17. If FOLD is the GTO-correct answer, MW-17 reference itself should be amended (this is a reference-set-amendment per `BATCH2_8_HAND_DESIGNS.md` "Do NOT mutate" — escalation required). Risk: erodes reference set authority; likely incorrect (BATCH2 was solver-vetted).
- (c) **T7-ext template redesign** — replace nut-blocker+overcards configuration with TRUE NFD (suited hero hand giving has_flush_draw=1) + overcards configuration. This makes T7-ext mirror existing 604 corpus's T7 family (PILOT_553-568, all SUITED) but on different boards. Trade-off: MW-17 *exact* literal-replica canonical no longer fits the template; would need architect-hat amendment to manual canonical PILOT_693 to make it suited (e.g., AdKd on Jd8d4c — adds the 4th diamond → has_flush_draw=1 AND nut blocker).

Recommend **path (c) + targeted v3.4 supplement**: T7-ext template carries SUITED-hand variants that have has_flush_draw=1 + nut blocker discriminative axis; manual canonical PILOT_693 changes from AdKs (literal MW-17) to AdKd-style with one extra diamond on the board (makes it true NFD + nut blocker). This generates training data that activates the existing nut-FD-bucket reasoning chain (which v3.4 + the corpus already supports — labellers correctly handle PILOT_658/694 in T-RAISE-stabilize via the same nut-FD axis).

The literal MW-17 hand (AdKs unsuited on Jd8d4c) becomes a *reference set evaluation hand*, not a *training set hand* — it's used at evaluation time to test whether the trained model handles the MW-17 stay-wrong pattern, NOT used as a training label. This separates training discriminative axis (nut-FD bucket) from evaluation target (MW-17 spec hand).

## Summary of recommendations to orchestrator

1. **PILOT_689 (T8' monotone) — accept labeller CHECK as the prediction.** Update orchestrator-side prediction; no template/protocol/canonical change. T8' template generates valid CHECK training labels for monotone-flop FD-checked-through 4-way bucket reasoning (matching existing 604 corpus). **No blocker.**

2. **PILOT_692 (T10' MW-45 canonical) — recommend accepting labeller CALL as the prediction** (path a). T10' template generates valid mixed-RAISE-or-CALL training labels (RAISE when texture has no straight danger; CALL when broadway-completed). **No blocker, but needs orchestrator decision on MW-45 reference re-validation.**

3. **PILOT_693 (T7-ext / MW-17) — RECOMMEND path (c): redesign T7-ext to carry SUITED-NFD-with-nut-blocker hands; demote literal MW-17 canonical from training canonical to evaluation-only reference.** **THIS IS A BLOCKER for full 12.5H-C.** Architect-hat amendment required to T7-ext factory + manual canonical before relaunching pilot.

If orchestrator concurs with path (c), expected change scope: edit `scripts/build_corpus_revision_125h_situations.py` T7-ext template's parametric configs (use SUITED hero like AhKh on Jh8h3c, AdKd on Jd8d3c, etc.) + edit `_MANUALS` PILOT_693 entry (use SUITED variant like AdKd on Jd8d4c with has_flush_draw=1). Re-run factory with G1-G3 self-checks. Reopen 12.5H-B PR or add an addendum PR before 12.5H-C re-pilot.

## What's NOT a blocker

- **All 14 non-T7-ext parametric hands**: labelled with valid v3.4 reasoning, schema correct, ready for full phase
- **T-CONTROL design_action 6/6 match**: validates the entire T-CONTROL bucket + design_action mechanism for G4 drift detection at 12.5H-D
- **PILOT_658/694 (T-RAISE-stabilize)**: both correctly fire v3.4 Fix 2.1.1 clause-e → RAISE, validating the 60/40 bimodal seed-volatility fix for the H-FEAT primary corpus expansion
- **Cost / schema / refusals**: all clean; full phase fully feasible at $120 budget
- **PILOT_690 (T8' NFD canonical)**: BET as predicted ✓ — confirms T8' family is mixed CHECK-or-BET depending on whether hero card competes with on-board As

## What's blocked / what's queued

**Blocked:**
- 12.5H-C full phase (5 Sonnet × 90) → on orchestrator direction for divergence 3 (T7-ext / MW-17)
- 12.5H-C PR opens → on full phase complete
- 12.5H-C labels-final gate, merge, 12.5H-D dispatch → all downstream

**Queued:** all items per PR #169 §"What's blocked / queued"

## References

- 12.5H-C dispatch: master `fb6983b` (PR #172)
- 12.5H-B situations + manuals merged: master `094cfc2` (PR #169)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `fb6983b`)
- MW-17 reference: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`
- 12.5H-A design: `review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md` (master `858b032`)
- Existing 604 labels (for T8' CHECK confirmation): `data/corpus_revision_125e_labels_2026-05-05.jsonl` (master `0eaac06`)
- Memory: `feedback_pilot_first_for_long_jobs.md` (pilot-first STANDING RULE caught the issue), `feedback_bucket_first_labelling.md` (no equity thresholds in labelling), `feedback_solver_vs_expert_labels.md`, `feedback_queries_to_orchestrator.md` (this comm routes per the rule)

**Status: 12.5H-C HALT. LP awaits orchestrator decision on path (a)/(b)/(c) for T7-ext divergence. Will re-pilot on direction.**
