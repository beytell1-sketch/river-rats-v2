---
date: 2026-05-06
from: LEAD-PROGRAMMER (architect hat)
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5I-A — corpus expansion design (90-120 new hands across T8'-redesigned, T9'-expanded, T10'-redesigned; MW-25/40/45 targets); per-hand diagnostic-driven scope
status: DESIGN — PR open, ready for QC trigger
branch: programmer/phase125i-a-design-2026-05-06
base: master `c536c30`
---

# 12.5I-A — corpus expansion design (D path)

## §1 Authority chain

- 12.5H-F synthesis owner gate (PR #191): owner picked **E** → **C+D parallel** compound
- 12.5I-pre diagnostic (PR #193) per-hand verdicts assigned 3 hands to D path:
  - **MW-25**: E-DIST underpowered + E-FEATURE secondary; ablation moves expert by +0.147 (corpus-tractable)
  - **MW-40**: E-DIST underpowered (closest to flipping at margin +0.267, BET prob 0.305)
  - **MW-45**: isomorph-mismatch + E-DIST secondary (model has features; needs specific texture in corpus)
- 12.5I dispatch (PR #196): per-template scope 30-40 hands (12.5H demonstrated 12-15 was underpowered)

## §2 Scope

90-120 new hands across 3 templates targeting 3 stay-wrong reference hands. Combined corpus post-12.5I: 694 + 90-120 = 784-814 hands. Additive only (12.5H locked). Path Y still binds at corpus level (no source-surface edits beyond trainer module + tests).

12.5I runs **parallel with 12.5J** (feature engineering for MW-17/47; PR #196 separate dispatch). Non-overlapping targets; integration at 12.5K.

## §3 Per-template specification

### Template T8'-redesigned (MW-25 family — BET-after-checked-through-multiway with non-nut-blocker hero)

**Target reference hand:** MW-25 (Ks7s on As9s5d, BTN IP 4-way checked through; expert BET HIGH)

**12.5H T8' failure mode (per 12.5I-pre diagnostic):** original T8' template put the As ON the monotone board, which made hero's K-spade dominated by every villain holding any spade (better_hand_pct=0.831). All 18 T8' hands labelled CHECK uniformly — corpus produced labels matching the model's "wrong" CHECK prediction, NOT the BET reference action.

**Redesign constraint:** hero must NOT hold the on-board top card. This avoids the As-public discriminative-axis collapse. The critical insight: MW-25 reference hand HAS hero with K-high FD (Ks7s) ON a board where As IS public — meaning the BATCH2 reference's BET reasoning is itself questionable (or relies on non-equity factors like fold-equity-from-three-checks-implies-weakness). The redesign proceeds AS IF the BET expert is correct (per dispatch); QC may flag if a deeper protocol issue surfaces during labelling round.

**Discriminative axis:**
- `is_monotone=1` (or `is_two_tone=1` with hero having FD)
- `has_flush_draw=1`
- `nut_flush_block=0` (hero does NOT hold the nut blocker — distinguishes from T8' canonical)
- `villain_checked_back=1` (4-way preflop, all check on flop, hero last to act)
- `num_opponents>=3`
- `is_paired=0`
- Hero in IP position (BTN or CO last to act)

**Spec variants (target ~30-35 hands):**
- TWO-TONE flop with hero holding 1 same-suit card: e.g., 9c8c on Kh4c2c (hero has K overcard absent; only kicker info). Hero IS on a real flush draw but not nut FD. Predicted: BET on the IP-after-check-through axis (denial + thin value).
- Variants across board high (J/T/Q-high; avoiding A-high to escape v3.4's "non-nut FD on nut-board is dominated" reasoning).
- Hero card variants: T9 / 87 / 76 connectors + suit; or non-suited paired-mid with backdoor draws.
- ~10 hands per board family (J-high / T-high / Q-high).

**Predicted v3.4 protocol output:** BET (target). However, given 12.5H T8' all routed to CHECK, this prediction is uncertain — pilot phase will verify. If pilot routes to CHECK uniformly (similar to 12.5H T8'), STOP and route to orchestrator with v3.4 protocol amendment question.

**Sub-template T8'-redesign-MW25-canonical** (manual canonical x2): explicit "hero=Ks7s on As9s5d" exact replica + 1 contrast variant on different texture. These are the HARDEST hands to predict; pilot phase may reveal protocol-vs-reference disagreement specifically here.

### Template T9'-expanded (MW-40 family — TP-medium-kicker IP 4-way after PFR check)

**Target reference hand:** MW-40 (AhTs on AdJc5h, BTN IP 4-way checked through; expert BET MEDIUM)

**12.5H T9' status:** 14 hands (13 parametric + 1 manual) all labelled BET 14/14 unanimous. v3.4 routing correct. Model fails to transfer with margin only +0.267 (closest to flipping). T9'-expanded is a STRAIGHTFORWARD scale-up; same template structure; just more diverse parametric variants.

**Discriminative axis (unchanged from 12.5H T9'):**
- `is_made_hand=1` with `hand_category=6` (top pair medium kicker)
- `is_rainbow=1` (no FD on board)
- `villain_checked_back=1`
- `num_opponents>=3` (4-way preflop)
- Hero IP

**Spec variants (target ~32 hands; expansion factor ~2.3× from 14):**
- A-high boards with kicker T or J:
  - AT-rainbow + low cards (5/6/7) — 8 hands across A6 / A7 / A5 / Ac9 mids
  - AJ-rainbow + low cards — 8 hands
- K-high boards with kicker T or J:
  - KT-rainbow — 8 hands
  - KJ-rainbow — 8 hands

Vary preflop opener position (HJ / CO / UTG) and 4-way structure to add variation without changing the core axis. Re-use existing T9' parametric hands' structural pattern; just add more configurations.

**Predicted v3.4 protocol output:** BET unanimous (per existing T9' precedent + reference set). Pilot phase verification: should be routine.

**Sub-template T9'-expanded-MW40-canonical** (manual canonical x1): MW-40 exact replica AhTs on AdJc5h. Same as 12.5H PILOT_691 — not changed.

### Template T10'-redesigned (MW-45 family — slowplay set + AKQx-broadway-completed turn)

**Target reference hand:** MW-45 (6d6c on AcKd6hQs turn, BB OOP facing CO turn lead 4-way + BTN call; expert RAISE HIGH)

**12.5H T10' failure mode (per 12.5I-pre diagnostic):** original T10' parametric used non-broadway-completed turn cards (Td/Tc/Js/Jd/Qc) — they don't match MW-45's specific AKQx broadway-completed pattern. T10' canonical PILOT_692 IS the MW-45 exact replica and DID label as RAISE 5/5 in full phase. But the 13 different-texture parametric hands didn't transfer to the AKQx texture in model inference. **Isomorph-mismatch primary.**

**Redesign constraint:** include broadway-completed turn cards (AKQ-x, AKJ-x, KQJ-x patterns) in parametric configs. The flop must have at least 2 broadway cards + low pair card; the turn must complete a broadway straight.

**Discriminative axis:**
- `hand_category=12` (set; flopped; bottom or middle set)
- `is_monster=1`
- Street=turn
- `villain_aggression_count=1` (CO bet turn)
- `num_callers_to_bet>=1` (one villain called turn lead before hero's action)
- `num_opponents>=2` (4-way preflop, at least 2 alive on turn)
- Turn card BROADWAY-COMPLETING (Q on AK6 flop; J on AKQ/AK6 flop; etc.)

**Spec variants (target ~28-32 hands):**
- Bottom-set on AK6-Q turn: 6c6d / 6h6c / 6d6h on AcKd6hQs / AcKh6dQs / AsKd6cQh — 8 hands
- Bottom-set on AKJ-Q turn: 5h5c on AcKd5sQh - etc. — 6 hands
- Bottom-set on KQ6-J turn: 6h6c on KsQd6sJc - etc. — 6 hands
- Middle-set on AKx-broadway: 7d7c on AcKd7hQs etc. — 6 hands
- Top-set sub-family: AcAd on KQJ-x rainbow + broadway turn — 4 hands (less common but isomorphic axis)

For each: 4-way preflop, slowplay flop (all check), CO turn lead, BTN calls, hero (BB or SB) faces bet+call OOP.

**Predicted v3.4 protocol output:** RAISE (per MW-33 anchor: set must RAISE vs bet+call at compressed SPR). Some borderline texture variants may produce CALL (the 12.5H PILOT_692 original-pilot-CALL pattern). Pilot phase will verify.

**Sub-template T10'-redesigned-MW45-canonical** (manual canonical x1): MW-45 exact replica 6d6c on AcKd6hQs. Same as 12.5H PILOT_692.

## §4 Quantity and class distribution

**Total target: 90-120 new hands** (3 templates × 30-40 each).

| Template | Parametric | Manual canonicals | Total |
|---|---:|---:|---:|
| T8'-redesigned (MW-25) | 30-35 | 2 | 32-37 |
| T9'-expanded (MW-40) | 32 | 1 | 33 |
| T10'-redesigned (MW-45) | 28-32 | 1 | 29-33 |
| **Total** | **90-99** | **4** | **94-103** |

Aim for 100 ± 5 hands. Combined corpus post-12.5I = 694 + 100 = 794 hands.

### Class distribution after 12.5I merge

Predicted label class additions (assumes pilot APPROVE confirms predictions):

| Class | 12.5H corpus (694) | +12.5I predicted | Post-12.5I (~794) | Pre/post % |
|---|---:|---:|---:|---:|
| FOLD | 79 | 0 | 79 | 11.4% → 9.9% |
| CHECK | 295 | 0 | 295 | 42.5% → 37.2% |
| CALL | 79 | 0 | 79 | 11.4% → 9.9% |
| BET | 137 | ~67 (T8'-r 32 + T9'-e 33 + 2 manual) | ~204 | 19.7% → 25.7% |
| RAISE | 104 | ~33 (T10'-r 33) | ~137 | 15.0% → 17.3% |

**BET class shifts +6.0pp; RAISE class shifts +2.3pp.** Per 12.5H precedent (RAISE +2.2pp at 12.5H), shift is conservative. BET increase is intentional given MW-25 + MW-40 + MW-40 family expansion.

If pilot reveals T8' produces CHECK uniformly (the 12.5H T8' mode), the BET predictions for T8'-redesigned collapse to CHECK and the class distribution rebalances toward CHECK + the corpus delivers no MW-25 leverage. Pilot gate STOP would surface this.

## §5 Manual canonical authoring (Track B — gto-expert-load-bearing)

4 manual canonical hands:

1. **T8'-redesigned canonical 01** (MW-25 exact replica): hero Ks7s on As9s5d, BTN IP, 4-way checked through. Author note: this is the literal MW-25 reference hand. Predicted action: BET per BATCH2 reference; CHECK per v3.4 + 12.5H corpus precedent. **Pilot phase MUST verify which prediction wins; route to orchestrator on disagreement.**

2. **T8'-redesigned canonical 02** (contrast variant): hero 9c8c on Kh4c2c, BTN IP, 4-way checked through. K-high two-tone flop with hero as connector + FD (no nut blocker, no on-board overcards). Predicted: BET (denial + thin value).

3. **T9'-expanded canonical** (MW-40 exact replica): hero AhTs on AdJc5h, BTN IP, 4-way checked through 200bb deep. Same as 12.5H PILOT_691. Predicted: BET (per existing 12.5H label).

4. **T10'-redesigned canonical** (MW-45 exact replica): hero 6d6c on AcKd6hQs turn, BB OOP facing CO bet 75 + BTN call. Same as 12.5H PILOT_692. Predicted: RAISE (per full-phase label; supersedes original 1-labeller-pilot CALL).

Per dispatch §"Manual canonical authoring": GTO-EXPERT review (gto-expert hat) required BEFORE labelling round. Author notes per `feedback_bucket_first_labelling.md` — bucket-first reasoning, no equity thresholds.

## §6 Track A — situation factory

Reuse `scripts/build_corpus_revision_125e_situations.py` + `scripts/build_corpus_revision_125h_situations.py` as structural template. Author NEW factory `scripts/build_corpus_revision_125i_situations.py` with 3 new template classes (T8PrimeRedesigned, T9PrimeExpanded, T10PrimeRedesigned) + inline manual canonicals in `_MANUALS` list (same pattern as 12.5H factory).

`pilot_hand_id` range: PILOT_695..PILOT_794 (or per-design exact range; ~100 hands).

G1-G3 self-checks per 12.5H precedent:
- G1 (join-cardinality): 100 unique pilot_hand_id; 0 collisions vs existing 694
- G2 (distribution): per-template counts within ±2 of design §4
- G3 (duplicate detection): zero exact-match duplicates vs existing 694 on (board, hero_cards, action_history, hero_position)

## §7 Methodology rules (per 12.5H-A §10 — all standing)

1. **Hero-only convention** in `prior_actions` (matches existing 794-hand corpus uniformly post-12.5I)
2. **Pre-flight join-cardinality** ≥0.99 vs existing 694 (per 12.5D' protocol amendment)
3. **`design_action` field per hand** for any T-CONTROL-like rows added (12.5I doesn't add T-CONTROL by default — design_action not required for T8'-r/T9'-e/T10'-r)
4. **Pilot-first does NOT apply at 12.5I-B** (situation generation is deterministic factory output)
5. **Pilot-first DOES apply at 12.5I-C** (labelling round; Sonnet × 5 × ~100 hands; same pattern as 12.5H-C)
6. **Solver-as-labels prohibited** per `feedback_solver_vs_expert_labels.md`
7. **Cross-seed importance reporting** at 12.5I-E trainer report (TC-X-CROSS-SEED-IMPORTANCE)
8. **Cap-binding pre-flight** at 12.5I-E (TC-X-CAP-BINDING-PRE-CHECK; informational)
9. **Tier-up verification** orchestrator-side at 12.5I-C (Opus single-pass on contested hands; same as 12.5H-C pattern)
10. **TC-X-DISPATCH-PREDICTION-VERIFICATION** (newly-formalized at 12.5H-C): predictions in this design comm are LP-side; orchestrator may amend at trigger time; pilot phase is the truth signal

## §8 Sequencing — multi-phase 12.5I workstream

Per 12.5H-A precedent, 12.5I workstream phases:

| Phase | Comm pattern | Deliverable | Gate |
|---|---|---|---|
| 12.5I-A (this comm) | PLAN_PHASE125I_CORPUS_EXPANSION | design (1 file) | QC APPROVE |
| 12.5I-B | BUILDER_REPORT_PHASE125I_B | factory + ~100 situations + manuals + report (4 files) | QC APPROVE |
| 12.5I-C | BUILDER_REPORT_PHASE125I_C | labels raw + consensus + report (3 files); pilot-first | QC APPROVE + Opus tier-up |
| 12.5I-D | REVIEW_QC_PHASE125I_D | corpus QC sweep on combined ~794 corpus | QC APPROVE |
| 12.5I-E | PROGRAMMER_REPORT_PHASE125I_E | re-train on 794-hand corpus (parallel with 12.5J-E if 12.5J ships first) | QC APPROVE; gate ≥33 = PROMOTE |
| 12.5I-F | MAIN_TERMINAL_PHASE125I_F_SYNTHESIS | gate evaluation + owner gate | owner WHAT |

12.5K = combined re-train integrating 12.5I + 12.5J results. Fires AFTER both 12.5I-E and 12.5J-E ship (per dispatch §"What's blocked / queued").

### 12.5I-A exit gate

- Manual canonicals listed and design notes drafted for gto-expert review
- Per-template counts + class distribution table populated
- Discriminative axes specified per template
- Cross-references to 12.5I-pre diagnostic per-hand verdicts present
- Predicted v3.4 outputs per template + acknowledgment of T8'-redesign uncertainty

## §9 Risks + open questions for orchestrator

### Risk 1: T8'-redesign protocol disconnect

12.5I-pre diagnostic surfaced that v3.4 protocol applied to MW-25-exact replicas produces CHECK uniformly (not the reference's BET). T8'-redesigned attempts to construct hands where v3.4 routes to BET, but this is a NEW pattern not previously tested. Risk: pilot phase reveals all T8'-redesigned hands ALSO route to CHECK → corpus delivers no MW-25 leverage → STOP and route to orchestrator with v3.4 protocol amendment proposal OR BATCH2 MW-25 reference re-evaluation question.

**Mitigation:** pilot 1-Sonnet × ~20 T8'-redesigned hands before full Sonnet × 5 × all-100; STOP on uniform CHECK consensus.

### Risk 2: T9'-expansion may be insufficient

Margin to flip MW-40 is +0.267 — small but not zero. 32 hands (2.3× from 14) may not be enough booster signal. Backup: T9' to 50 hands at 12.5I-A amendment if 12.5I-E re-train doesn't flip MW-40.

### Risk 3: T10'-redesign isomorph-mismatch may persist

Even with broadway-completed turn variants, the booster may not transfer to MW-45's specific 4-card AKQ-rainbow texture. Backup: T10' to MORE-specific board textures (AKQ-rainbow only, not AKJ or KQJ) at 12.5I-A amendment if 12.5I-E doesn't flip MW-45.

### Open question to orchestrator

Per 12.5I-pre diagnostic §"Cross-hand patterns": **MW-25 BET expert may itself be GTO-incorrect.** v3.4 + 12.5H corpus + model all align on CHECK. Should orchestrator request gto-expert-hat reference re-evaluation BEFORE 12.5I-B factory work? If MW-25 should be CHECK, T8'-redesigned can be deprecated entirely (MW-25 graduates from stay-wrong list at zero corpus cost).

## §10 References

- 12.5I dispatch: master `c536c30` (PR #196)
- 12.5I-pre diagnostic: master `54e2943` (PR #193)
- 12.5H-A design (structural template): master `858b032` (PR #165)
- 12.5H-B factory (structural template): master `094cfc2` (PR #169)
- 12.5H-C labelling (structural template): master `90e17dc` (PR #181)
- 12.5H-E re-train (structural template): master `283af91` (PR #188)
- 12.5J-A dispatch (parallel): master `c536c30` (PR #196)
- BATCH2 reference set: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md`
- v3.4 protocol: `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_explicit_action_trigger.md`, `feedback_river_rats_team_structure.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_attention_flags_when_features_change.md`

**Status: 12.5I-A DESIGN COMPLETE. PR opening; awaiting QC trigger. After QC APPROVE: 12.5I-B (situation generation factory) dispatches. Open question to orchestrator on MW-25 reference re-evaluation surfaced in §9.**
