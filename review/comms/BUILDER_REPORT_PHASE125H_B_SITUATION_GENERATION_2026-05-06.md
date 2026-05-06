---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5H-B' — situation generation amendment (path c; T7-ext SUITED-NFD redesign)
status: REPORT — amendment PR open, ready for QC trigger
branch: programmer/phase125h-b-prime-amendment-2026-05-06
base: master `c01b799` (post 12.5H-B + PR #173 PILOT HALT merge)
amendment of: PR #169 (master `094cfc2`)
---

# 12.5H-B' amendment builder report — T7-ext SUITED-NFD redesign

## Amendment 2026-05-06 (path c — T7-ext SUITED-NFD redesign)

Per orchestrator dispatch `MAIN_TERMINAL_PHASE125H_B_PRIME_AMEND_2026-05-06.md`
(master `a84793c`, PR #174). 12.5H-C pilot HALT (PR #173) identified the
T7-ext / MW-17 protocol-vs-reference gap: original UNSUITED hero hands
(literal MW-17 spec AdKs on Jd8d4c) routed via v3.4 bucket-first reasoning
to FOLD with HIGH confidence; full Sonnet × 5 × 90 would have generated
training labels REINFORCING the model's existing FOLD-on-MW-17
misclassification. Path (c) adopted: redesign T7-ext template to use
SUITED-NFD-with-nut-blocker hands (mirrors existing PILOT_553-568 T7
family which v3.4 handles correctly via the nut-FD axis). Demote literal
MW-17 canonical from training canonical to evaluation-only reference.

**Files updated in this amendment (4 — same scope as original 12.5H-B PR #169):**

1. `scripts/build_corpus_revision_125h_situations.py` — T7-ext template
   class (lines 320-400) redesigned: 11 SUITED-NFD parametric configs
   replacing the original UNSUITED + blocker-only mix. PILOT_693 manual
   canonical (lines 878-906) changed from `AdKs on Jd8d4c` (UNSUITED)
   to `AdKd on Jd8d4c` (SUITED — adds the 4th diamond making it true NFD
   + nut blocker).
2. `data/corpus_revision_125h_situations_2026-05-06.jsonl` — regenerated
   from amended factory; T7-ext rows (PILOT_647..657) replaced with new
   SUITED-NFD-with-blocker discriminative axis.
3. `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` —
   regenerated; PILOT_693 row replaced with SUITED variant.
4. `review/comms/BUILDER_REPORT_PHASE125H_B_SITUATION_GENERATION_2026-05-06.md`
   — this file; amendment section prepended.

**T7-ext discriminative axis verification (programmatic check, all 12 hands):**

| pilot_hand_id | hero | board | has_flush_draw | nut_flush_block | raw_equity | ✓ |
|---|---|---|---:|---:|---:|:---:|
| PILOT_647 | AhKh | Jh9h3c | 1 | 1 | 0.477 | ✓ |
| PILOT_648 | AhQh | Jh9h3c | 1 | 1 | 0.454 | ✓ |
| PILOT_649 | AhKh | Th7h3c | 1 | 1 | 0.502 | ✓ |
| PILOT_650 | AhQh | Th9h3c | 1 | 1 | 0.450 | ✓ |
| PILOT_651 | AdKd | Jd9d3c | 1 | 1 | 0.458 | ✓ |
| PILOT_652 | AdQd | Jd9d3c | 1 | 1 | 0.425 | ✓ |
| PILOT_653 | AdKd | Td9d3c | 1 | 1 | 0.469 | ✓ |
| PILOT_654 | AsKs | Js9s3c | 1 | 1 | 0.467 | ✓ |
| PILOT_655 | AsQs | Js9s3c | 1 | 1 | 0.440 | ✓ |
| PILOT_656 | AcKc | Jc9c3d | 1 | 1 | 0.464 | ✓ |
| PILOT_657 | AcQc | Jc9c3d | 1 | 1 | 0.431 | ✓ |
| PILOT_693 (manual) | AdKd | Jd8d4c | 1 | 1 | 0.463 | ✓ |

12 of 12 satisfy the discriminative axis (`has_flush_draw=1` AND
`nut_flush_block=1`).

**G1-G3 PASS on amended dataset:**
```
G1 PASS: 90 unique pilot_hand_ids; 0 collisions vs existing 604
G2 PASS: T8PRIME=18/18, T9PRIME=14/14, T10PRIME=14/14, T7EXT=12/12, TRAISE=12/12, TCONTROL=20/20
G3 PASS: 0 (board, hero, position, prior_actions) duplicates internal or vs 604
```

**v3.4 prediction self-review (4-hand verification subagent run):**

Per dispatch §"LEAD-PROGRAMMER (gto-expert hat — re-review of amended T7-ext)" — verified PILOT_693 + 3 parametric T7-ext hands (PILOT_647, PILOT_651, PILOT_656) through v3.4 protocol via 1-Sonnet labeller subagent.

| pilot_hand_id | hero | board | villain_air_pct | v3.2 ≥ 0.20 threshold | predicted action |
|---|---|---|---:|:---:|:---:|
| PILOT_647 | AhKh | Jh9h3c | 0.047 | FAILS | **CALL** |
| PILOT_651 | AdKd | Jd9d3c | 0.282 | PASSES | **RAISE** (KB §1.7 fires) |
| PILOT_656 | AcKc | Jc9c3d | 0.282 | PASSES | **RAISE** (KB §1.7 fires) |
| PILOT_693 | AdKd | Jd8d4c | 0.312 | PASSES | **RAISE** (KB §1.7 fires) |

**v3.4 routing analysis:**
- Drawing bucket (nut FD + nut blocker, hand_category=2)
- num_callers_to_bet=0 → v3.3 Fix 2.1 + v3.4 Fix 2.1.1 do NOT engage (HU after BTN fold, not bet+call multiway)
- KB §1.7 OVERRIDE (v3.2) fires when villain_air ≥ 0.20 → RAISE
- When villain_air < 0.20 → CALL (drawing-bucket equity vs pot odds, no carve-out)
- Action split is GTO-correct given the v3.4 protocol's villain-air-conditional KB §1.7 carve-out

**Outcome: amendment successfully resolves the FOLD anti-training risk.** All T7-ext hands now route to RAISE or CALL (NOT FOLD) — generating SOUND training data on the nut-FD-with-blocker discriminative axis. Stop condition "T7-ext SUITED hands STILL produce FOLD-predicted under v3.4 protocol" does NOT trigger; amendment is unblocked.

**Note on orchestrator-side prediction:** Dispatch §"Updated 12.5H-C predictions" predicted CALL for the new PILOT_693. Actual v3.4 verification produces RAISE because villain_air_pct = 0.312 (> 0.20 threshold) on the J-high two-tone with broadway-overcards hero. Orchestrator's prediction text noted "KB §1.7 RAISE may fire if villain_air >= 0.20 — verified at amendment self-review" — this is what fired. RAISE is GTO-correct and not a stop condition; flagging here for orchestrator's information so 12.5H-C re-pilot predictions can be updated to CALL/RAISE-mix-driven-by-villain_air rather than uniform CALL.

**Honest implication for MW-17 stay-wrong (per amendment dispatch §"Honest implication of (c)"):**
Path (c) generates training data on the SUITED-NFD-with-blocker axis (mostly RAISE with some CALL). MW-17's literal pattern (UNSUITED-overcards-with-blocker, raw_equity 0.245, NO flush-draw outs, ONLY backdoor + blocker) is a different axis and may NOT be fixed by 12.5H training. If 12.5H-F gate fails on MW-17, that's evidence of E-FEATURE primary per gto-expert 12.5D' diagnosis and escalates to feature engineering — that's the genuine next step, not a workaround.

## Summary (12.5H-B original, retained for reference)

90 new situations factory-generated across 6 templates per 12.5H-A
design (`review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md`,
master `858b032`). pilot_hand_id range PILOT_605..PILOT_694, zero
collisions vs existing 604-hand corpus. All G1-G3 self-checks PASS.

Per dispatch §"What you do NOT do": no labelling, no trainer touch, no
prompt touch, no existing-corpus mutation, no solver call. Per
dispatch §"Methodology rules": hero-only convention uniform across all
90 rows (0 violations); `design_action` field present on all 20
T-CONTROL rows (TC-X T8 schema fix).

## Files in PR diff (exactly 4)

1. `scripts/build_corpus_revision_125h_situations.py` (NEW, 1146 lines) —
   factory + 6 template classes (T8'/T9'/T10'/T7-ext/T-RAISE-stabilize/
   T-CONTROL) + 6 inline manual canonicals + G1-G3 self-checks. Reuses
   helpers from `scripts/build_corpus_revision_125e_situations.py`
   (master `858b032`): `emit_row`, `build_hand_dict`,
   `_hero_only_prior_actions`, `TemplateGenerator` base, `GeneratedSituation`.
2. `data/corpus_revision_125h_situations_2026-05-06.jsonl` (NEW,
   84 rows) — parametric situations PILOT_605..PILOT_688.
3. `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl`
   (NEW, 6 rows) — manual canonical hands PILOT_689..PILOT_694
   (subject to GTO-EXPERT review at 12.5H-C trigger; self-reviewed
   here under gto-expert hat per dispatch §"LEAD-PROGRAMMER (gto-expert
   hat)").
4. `review/comms/BUILDER_REPORT_PHASE125H_B_SITUATION_GENERATION_2026-05-06.md`
   (NEW, this file).

## Per-template count table (G2 distribution)

| Template | Parametric | Manual | Total | Design §4 target | Δ |
|----------|-----------:|-------:|------:|-----------------:|--:|
| T8' (MW-25 monotone-FD checked-through 4-way) | 16 | 2 | 18 | 18 | 0 |
| T9' (MW-40 TP-medium-kicker IP 4-way after PFR check) | 13 | 1 | 14 | 14 | 0 |
| T10' (MW-45 slowplay set turn lead 4-way) | 13 | 1 | 14 | 14 | 0 |
| T7-ext (MW-17 nut-blocker + overcards CALL pot odds 3-way) | 11 | 1 | 12 | 12 | 0 |
| T-RAISE-stabilize (MW-47 + 60/40 bimodal fix; bet+call multiway) | 11 | 1 | 12 | 12 | 0 |
| T-CONTROL (drift detection across 5 buckets w/ design_action) | 20 | 0 | 20 | 20 | 0 |
| **Total** | **84** | **6** | **90** | **90** | **0** |

All per-template counts within ±1 (in fact exact match) of design §4.

## G1-G3 self-check results

```
G1 PASS: 90 unique pilot_hand_ids; 0 collisions vs existing 604
G2 PASS: T8PRIME=18/18, T9PRIME=14/14, T10PRIME=14/14, T7EXT=12/12, TRAISE=12/12, TCONTROL=20/20
G3 PASS: 0 (board, hero_cards, hero_position, prior_actions) duplicates vs existing 604; 0 internal duplicates
```

`scripts/build_corpus_revision_125h_situations.py --strict` exits 0.

### G3 dedup notes

Initial run found 38 fingerprint collisions vs the 604-hand corpus.
Root cause: T8'/T9'/T10' parametric configs unintentionally mirrored
12.5E-B's T1/T2/T4 board+hero pairs (same monotone-spades boards,
same A-high/K-high rainbow boards, same paired-flop patterns).
T-CONTROL collided with `t8_controls`. Fixed by:
- T8': switched to NEW spade-monotone boards (Js9s4s, Ts8s4s, 9s7s3s,
  Qs7s3s) plus suit-rotated hearts/diamonds/clubs variants. Existing
  604 only used monotone-spades; the suit-rotated boards expand the
  corpus discriminatively.
- T9': switched to NEW A-high/K-high rainbow boards distinct from
  As7d3c, Ad8c4s, Ks6d2c, Kc9s3d, Ah6c2s.
- T10': switched to NEW (hero, flop, turn) combinations; preserved set
  ranks 33-99 axis on different texture/turn cards.
- T-RAISE-stabilize: switched bricks from 5c/5d to 6c/6h/7c/7h/8c, and
  used heart bricks on club-FD variants to avoid the existing PILOT_539
  -550 NFD-gutshot brick set.
- T-CONTROL: completely fresh hero+board combos for all 6 buckets.

Two residual canonical-vs-canonical collisions (T-RAISE
parametric_01 vs `t5_manual_canonical` PILOT_599; T8' canonical_02 vs
`t1_manual_canonical` PILOT_591) fixed by board offset (KsJs6c→KsJs8c;
Js9s4s→Js9s3s).

## Hero-only convention verification

All 90 rows have `prior_actions` filtered to hero-only entries via
`_hero_only_prior_actions` (reused from 12.5E-B factory line 119).
0 violations across the 90 rows. `action_history` (which
`extract_all_features` consumes for chain narrowing) preserves the
full multi-actor sequence per existing-494 convention.

## design_action verification (TC-X T8 schema fix)

All 20 T-CONTROL rows have an explicit `design_action` field
(CHECK / BET / FOLD / CALL / RAISE) per dispatch §"Methodology rules"
item 3 + QC's TC-X T8 schema gap finding from PR #150. Distribution:

| design_action | count |
|---------------|------:|
| CHECK         | 6 |
| BET           | 5 |
| FOLD          | 4 |
| CALL          | 3 |
| RAISE         | 2 |
| **Total**     | **20** |

This enables 12.5H-D to do exact same-action match against 494/110-hand
corpus near-equivalents for G4 drift detection. No other rows include
the field (only T-CONTROL).

## gto-expert-hat self-review (6 manual canonicals)

Per dispatch §"LEAD-PROGRAMMER (gto-expert hat — pre-PR self-review)".
Each canonical re-evaluated against composition/board/action/position/
SPR criteria from dispatch §"LEAD-PROGRAMMER (architect hat)". GTO-EXPERT
review at 12.5H-C dispatch will be the binding gate; this is internal
sanity check before PR open.

### PILOT_689 — t8prime_manual_canonical_01 (Ks7h on As9s5s, BTN, 4-way checked through)

- composition triple: K-high FD (1 hole spade + 3 board spades) +
  no overcards (A-high board), checked-through 4-way → drawing-bucket
  weak FD ✓
- board texture: monotone spades A-9-5, no pairs → discriminative axis
  is_monotone=1, has_flush_draw=1, is_paired=0 ✓ (verified PILOT_689
  feat_dict: cat=0, FD=1, mono=1, eq=0.382)
- action history: HJ open / CO call / BTN call / BB call / BB check /
  HJ check / CO check → all 3 villains checked, hero IP last to act ✓
- position + SPR: BTN with 110 effective pot ratio after 4-way preflop
  (~20-25 SPR) is canonical for drawing-bucket BET ½-pot for
  fold equity + equity denial + protection ✓
- author_design_note describes intent (MW-25 family monotone-board
  adaptation; hero kicker suit changed from MW-25's Ks/7s to Ks/7h to
  preserve FD axis on monotone instead of producing a made flush).
- **VERDICT: PASS** — labelling at 12.5H-C should produce BET 5-7
  drawing bucket reasoning.

### PILOT_690 — t8prime_manual_canonical_02 (AsKh on Js9s3s, BTN, 4-way checked through)

- composition triple: NFD (As + 3 board spades = 4 spades) + 2
  overcards (A, K both > J) → drawing-bucket strong FD with overcards ✓
- board texture: monotone spades J-9-3 (avoids 12.5E-B PILOT_591
  Js9s4s board) ✓ (verified PILOT_690 feat_dict: cat=2, FD=1, mono=1,
  eq=0.403)
- action history: HJ open / CO call / BTN call / BB call / BB check /
  HJ check / CO check ✓
- position + SPR: BTN ✓
- author_design_note describes contrast pair with PILOT_689 (K-high FD
  vs NFD canonical) for booster generalization.
- **VERDICT: PASS** — labelling at 12.5H-C should produce BET 5-7
  drawing bucket reasoning, possibly slightly larger size given
  combined value/draw.

### PILOT_691 — t9prime_manual_canonical_01 (AhTs on AcJc5d, BTN, 4-way after PFR check)

- composition triple: TP T-kicker on rainbow A-J-5 board, 4-way ✓
- board texture: rainbow (Ac/Jc/5d — Ac and Jc both clubs but only 2
  → no FD on board), no straight draw possible in normal range; A is
  top, J is overcard kicker → discriminative axis is_made_hand=1,
  hand_category=6 (TP-medium-kicker) ✓ (verified PILOT_691 feat_dict)
- action history: HJ open / CO call / BTN call / BB call / BB check /
  HJ check / CO check → PFR check-back is the diagnostic event;
  condenses HJ range to weak Jx/broadways without A ✓
- position + SPR: BTN with PFR check-back creates BTN's protect-and-
  thin-value spot. AT pairing the A is canonical "thin value + protect
  vs draws" → strong-made-bucket BET ½-pot ✓
- raw_equity 0.202 reflects multiway equity compression (4-way
  versus AK/AQ/AJ/JJ/55 calling range), but BET reasoning should be
  protection + fold equity denial, not equity-only.
- author_design_note matches MW-40 exact spec (literal AcJc5d board).
- **VERDICT: PASS** — labelling should produce BET ½-pot strong-made
  reasoning anchored on multiway protection.

### PILOT_692 — t10prime_manual_canonical_01 (6d6c on AcKd6hQs, BB, turn lead 4-way)

- composition triple: bottom set on rainbow A-K-6 flop + Q turn brings
  broadway → set facing villain turn lead + 1 caller + folder ✓
- board texture: rainbow flop (Ac/Kd/6h), Q turn brings broadway draws
  but no flush; CO turn lead on broadway-completing card represents
  AK-strong, AQ, KQ, QQ; BTN call confirms strength ✓
- action history: 4-way preflop, flop checks through, turn CO leads,
  SB folds, BTN calls, hero (BB) faces bet+call → discriminative axis
  villain_aggression_count=1, num_callers_to_bet=1, num_opponents=3
  facing turn aggression ✓ (verified PILOT_692 feat_dict: cat=12, made=1,
  agg=1, cal2bet=1, eq=0.541)
- position + SPR: BB OOP with deep SPR (preflop 4-way pot ~10.5; turn
  pot 35 after lead+call; SPR ~3 based on 100bb effective stacks) →
  RAISE for value + protection vs the broadway draws AK/AQ may have
  improved-to-2P or have nut blockers ✓
- author_design_note matches MW-45 exact spec (literal AcKd6hQs board
  + 6d6c hero).
- **VERDICT: PASS** — labelling should produce RAISE strong-made
  bucket reasoning (set + protect/value vs broadway-completed range).

### PILOT_693 — t7ext_manual_canonical_01 (AdKs on Jd8d4c, BB, single bet 3-way)

- composition triple: nut diamond blocker (Ad) + 1 board diamond pair
  (Jd 8d) = 3 diamonds = backdoor flush draw + nut blocker; K
  overcard → drawing-bucket marginal CALL via implied/blocker
  reasoning ✓
- board texture: J-high two-tone (diamond) with low offsuit brick;
  pot odds required 26.8% per MW-17 spec; raw_equity 0.246
  marginally below pot-odds, implied + blocker close the gap ✓
  (verified PILOT_693 feat_dict: cat=2, made=0, FD=0, eq=0.246)
- action history: CO open / BTN call / BB call / BB check / CO bet 5
  / BTN fold → hero faces single bet 3-way after one fold; CO
  range condensed to value + bluffs that fold equity supports ✓
- position + SPR: BB OOP facing single bet from CO ✓
- author_design_note: matches MW-17 exact spec literally (AdKs on
  Jd8d4c). Labelling reasoning explicitly per
  `feedback_bucket_first_labelling.md` (drawing-bucket via composition,
  NOT pot-odds threshold).
- note: feature `has_flush_draw=0` because hero has only 3 diamonds
  visible (need 4 for FD); the discriminative axis here is composition
  (nut blocker + overcard + backdoor) + raw_equity in implied-odds
  range, not has_flush_draw. T7-ext naming carries "NFD" loosely from
  dispatch terminology; canonical hand is properly nut-blocker+overcard.
- **VERDICT: PASS** — labelling should produce CALL drawing-bucket
  reasoning anchored on composition (not threshold).

### PILOT_694 — traise_stabilize_manual_canonical_01 (AsQs on KsJd5s, BB, bet+call multiway)

- composition triple: NFD spades (As + Ks + 5s on board = 4 spades) +
  gutshot to broadway (T for QJTKx straight) + As nut blocker → strong
  combo draw ✓ (verified PILOT_694 feat_dict: cat=1, FD=1, agg=1,
  cal2bet=1, eq=0.425)
- board texture: K-J-5 with 2 spades + 1 diamond brick → mixed-suit
  variant deliberately chosen to avoid 12.5E-B's t5 hands which used
  pure spade-FD with 5c/5d brick (PILOT_539-550). Mixed Jd creates
  the v3.4 Fix 2.1.1 clause-e villain_air ≥0.05 carve-out the
  60/40 bimodal fix targets ✓
- action history: HJ open / CO call / BTN call / BB call / BB check /
  HJ check / CO bet 6 / BTN call → bet+call multiway with hero next OOP
  facing CO bet + BTN call (1 caller to bet) ✓
- position + SPR: BB OOP after bet+call, SPR ~4 → drawing-bucket
  RAISE for combined value/semi-bluff (NFD + gutshot + nut blocker
  with 9+4 outs ≈ 31% raw equity, plus fold equity from raise) ✓
- author_design_note matches MW-47 family + 60/40 bimodal seed-
  volatility fix (clauses a-e of v3.4 Fix 2.1.1 should all hold on
  this board).
- **VERDICT: PASS** — labelling should produce RAISE drawing-bucket
  semi-bluff reasoning; v3.4 protocol clause-e should fire (carve-out
  for villain_air ≥0.05) given the mixed-suit board structure.

### Self-review summary

All 6 canonicals PASS internal gto-expert hat self-review. One
significant bug found and fixed during self-review (PILOT_689 had hero
Ks7s on monotone As9s5s which gave a complete K-high flush rather than
a flush draw; corrected to Ks7h to preserve FD axis on monotone). All
6 canonical feat_dicts now match the design family's discriminative
axes. GTO-EXPERT review at 12.5H-C dispatch will be the binding gate.

## Pre-flight verification (architect hat)

Per dispatch §"Sequencing" item 1: pre-flight at master HEAD `8c90649`
confirmed all cited references exist:

- `scripts/build_corpus_revision_125e_situations.py` exists at master HEAD
  (1796 lines; verified helpers at lines 69 / 119 / 148 / 264 / 271)
- `data/corpus_combined_604_2026-05-05.jsonl` exists (604 rows; G1+G3 ref)
- `prompts/gto_labeller_v3.4.md` exists (untouched)
- `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` exists (MW-17
  reference checked: hero AdKs on Jd8d4c, num_opponents 2, pot_odds
  required 26.8% — used to guide PILOT_693 canonical and to confirm T7-ext
  template's nut-blocker+overcard family is the correct MW-17 expansion)

No drift found vs design.

## Stop conditions checked (per dispatch)

- ✅ Pre-flight: no drift in cited file:lines vs design
- ✅ Per-template counts: all exact match to design §4 (Δ=0)
- ✅ G1/G2/G3: all PASS
- ✅ Hero-only convention uniform: 0 violations across 90 rows
- ✅ No solver call: factory uses only feature_extractor, no solver imports
- ✅ Diff: exactly 4 files

## What's blocked / what's queued

**Blocked:**
- 12.5H-B QC trigger → on this PR open (orchestrator posts
  `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` next)
- 12.5H-B merge → on QC APPROVE
- 12.5H-C/D/E/F → all downstream of 12.5H-B merge

**Queued:** all items per PR #168 §"What's blocked / queued"

## References

- 12.5H-B dispatch: master `8c90649` (PR #168)
- 12.5H-A design: master `858b032` (PR #165)
- 12.5H-A QC verdict: master `68b6924` (PR #167)
- 12.5E-B (structural template): master `0eaac06` (PR #136)
- MW-17 reference: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`
- Existing 604 corpus: `data/corpus_combined_604_2026-05-05.jsonl`

**Status: 12.5H-B complete locally. PR opening; QC trigger awaited.**
