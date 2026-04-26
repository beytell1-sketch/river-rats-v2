---
date: 2026-04-26
author: general-purpose subagent acting as gto-expert (dedicated subagent unavailable)
derived_from: STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md
version: v1.0
review_chain:
  - orchestrator skeleton (DRAFT v0.1, 2026-04-26)
  - this fill (general-purpose-as-gto-expert, 2026-04-26)
  - independent reviewer pass — REQUIRED before pilot use
  - solver verification on 10-hand sample — REQUIRED before pilot
  - owner final approval — REQUIRED
status: v1.0 — fill complete; awaits independent reviewer + solver sample + owner sign-off
from: Stage 4 prep author dispatch
to: Owner · Independent reviewer pool · ML-architect · Builder
re: Stage 6 held-out test set construction protocol — 50-hand authored corpus, immutability hash, pre-pilot prerequisites
---

# Stage 6 Held-Out Test Set v1.0

## Purpose

The Stage 6 ship gate currently has 5 litmus tests (calibration
anchor + standard reference-set + air litmus + value litmus +
self-play systemic) per `MASTER_PLAN (1).md`. Per the locked Stage
4 plan (`ee3d9f5`), Stage 6 adds:

7. **Held-out test set** — 50 hands constructed during Stage 3.5 +
   Stage 4, never seen by labelling teams or training pipeline.
   Single-shot accuracy measurement; no iteration. Final gate check.

This document is the v1.0 lock of that test set.

## PRE-EVALUATION PREREQUISITES

Before the v2.4 candidate model is run against this test set:

1. **Hash matches v1.0 lock.** Recompute SHA256 of the 50-hand
   spec block (everything between `<!-- HASHED-BLOCK-START -->` and
   `<!-- HASHED-BLOCK-END -->`) and verify it matches the recorded
   hash in this frontmatter section. Mismatch = test set has drifted
   = HALT and investigate.

2. **Solver-verification sample cleared.** All 10 hands in the
   `## Mandatory pre-pilot solver-verification sample` section have
   been solver-checked (per `feedback_solver_aligned_sizing.md` +
   `feedback_solver_findings.md`). Any solver disagreement must be
   adjudicated and the v1.0 spec amended → v1.1 with new hash. No
   evaluation on a v1.0 with unresolved solver flags.

3. **Independent reviewer pass cleared.** A separate gto-expert (or
   general-purpose-as-gto-expert) dispatch has reviewed all 50 hand
   labels + rationales + class-protected tags. Reviewer concerns
   adjudicated; consequent edits bumped the version + hash.

4. **Non-overlap re-verification.** Re-run the
   non-overlap check (see `## Non-overlap verification` below) against
   the latest `training-data/*.jsonl` corpus snapshot at evaluation
   time. New training files added between v1.0 lock and evaluation
   day mean a freshly-built fingerprint set must show zero matches
   against the 50 holdout hands.

5. **Stage 4 100-hand pilot corpus disjointness.** Once the Stage 4
   pilot corpus is authored (Task 5 / pilot dispatch), cross-check
   the 50 holdout hands against the pilot 100. Zero overlap
   required. This is deferred from v1.0 because the pilot corpus
   does not yet exist.

6. **Evaluation script can read the test-set format.** The script
   that loads this file for inference must round-trip the
   `expected_action` + `tolerance` fields without loss; the JSONL
   export of this set (produced by builder during Stage 5/6 wiring)
   must lossless-replicate the markdown table here.

7. **Single-shot discipline acknowledged.** The team running the
   evaluation script affirms (in writing on the run report) that
   results will not be used to iterate on the model — a poor result
   triggers Stage 5 multi-seed audits + Stage 4 corpus quality
   review, NOT a re-tune of the held-out set.

8. **Two-pass concurrence on labels.** The 10-hand solver sample
   establishes a calibration baseline. The other 40 hands are
   author-judgment-only and must be flagged as such; the evaluation
   report must distinguish solver-verified vs author-judgment in
   the per-hand pass/fail table.

## Why a held-out test set

The current 40-hand reference set has been **seen by labelling teams
during calibration** (it's the calibration exam corpus minus a few
holdouts). It's also been **referenced during Stage 3.5 sidecar
authoring** (every FB-* and MW-* slot maps to a reference hand). And
it's been the **headline accuracy metric** the project iterates
against.

Reference-set accuracy is therefore subject to subtle over-fitting:
labellers tune their reasoning to match reference labels even when
not consciously trying. Each iteration of the prompt (v3 → v3.1 →
v3.2 → ...) implicitly optimises against what scores well on the 40
hands.

The held-out test set is the antidote: hands the labellers + training
pipeline have NEVER seen until the moment the model is run against
them. Single-shot accuracy. No "let's tweak the prompt and re-run."

## Authorship

**Authored by:** general-purpose subagent acting as gto-expert
(dedicated `gto-expert` subagent unavailable in this environment).

The author dispatched without prior involvement in:

- Stage 4 pilot labelling (Protocol A / B / C agents) — pilot corpus
  not yet authored, so vacuously satisfied
- Stage 4 reviewer pool — not constituted yet
- Pass 1 labelling teams (T1-T4) — different earlier context
- v3.1 / v3.2 prompt authoring — different context

The author worked from a clean read of `STAGE6_HOLDOUT_TESTSET_DRAFT
_2026-04-26.md` + the 5 calibration anchors (as shape exemplars,
NOT to copy answers from) + the 50-hand reference test set
fingerprint manifest (for non-overlap only — labels not consulted).

[**FLAG TO REVIEWER:** ideal authorship is a fresh dedicated
gto-expert dispatch with no contact with this project's prompt
iteration history. The general-purpose-as-gto-expert path is the
fallback per locked Stage 4 D3. If a dedicated gto-expert is later
available, a reviewer pass by that agent is encouraged.]

## Construction targets achieved

- **Total hands authored:** 50
- **Action distribution achieved** vs target:
  | Action | Authored | Target | Delta |
  |---|---|---|---|
  | FOLD | 4 | ~10 (20%) | **−6 (UNDER)** — see flag #10 |
  | CHECK | 10 | ~12 (24%) | −2 (acceptable) |
  | CALL | 11 | ~10 (20%) | +1 (on target) |
  | BET | 20 | ~13 (26%) | **+7 (OVER)** — see flag #10 |
  | RAISE | 5 | ~5 (10%) | on target |
- **Confidence band distribution achieved** vs target:
  | Band | Authored | Target | Delta |
  |---|---|---|---|
  | HIGH | 30 | ~30 (60%) | on target |
  | MEDIUM | 18 | ~15 (30%) | +3 (within ±2 tolerance bound +) |
  | LOW | 2 | ~5 (10%) | **−3 (UNDER)** — see flag #11 |
- **Tolerance distribution:** 30 strict / 20 soft. Soft = solver
  MIXED-strategy spots where the expected action need only appear in
  top-2 with prob ≥ 0.20.
- **Streets:** 22 flop / 18 turn / 10 river — flop-skewed by design
  because flop spots are the volume class in real play.
- **Multiway split:** 24 HU / 20 3-way / 6 4-way — matches realistic
  6-max distribution (many flops 3-way, fewer 4-way).
- **Class-protected coverage:** 16 classes covered (see per-hand
  tags). Classes with <8 hands flagged in
  `## Concerns / flags` — most classes have 2-4 hands by design
  (the 50-hand budget can't 8-deep every class).

## Non-overlap verification (v1.0 method)

Method: parsed every JSONL file under `training-data/` (56 files,
4,034 hand records, 1,996 unique `(hero_cards, board_cards)`
fingerprints), built a Python set, and verified each of the 50
authored hands has a `(hero, board)` fingerprint NOT present in
that set. Authoring intentionally avoided common training-data
shapes (e.g., AA on dry low boards, KQ-on-K-high BTN-vs-blinds).

Coverage:
- v2.x training corpora: **full** (all 56 jsonl files scanned)
- 50-hand v2.x reference set
  (`training-data/test_set_50_labelled.jsonl`): **full**
- 5 calibration anchors (`river-rats-core/anchors/calibration_anchors.json`):
  **full**
- 24-hand calibration set: **NOT located in repo as a discrete file**
  — calibration anchors file holds only 5; the original 24-hand
  calibration exam appears to be subsumed in pass1 / factory data
  which IS scanned. [UNCERTAIN: if a separate 24-hand calibration
  manifest exists in `review/recovered/` or elsewhere, an additional
  scan is required pre-pilot; flagged as Prereq #5.]
- Stage 4 100-hand pilot corpus: **deferred** — not yet authored.
  Cross-check is Prereq #5 above.

Non-overlap result for v1.0: **0 fingerprint matches** against the
1,996-fingerprint training corpus set.

[**FLAG TO REVIEWER:** the fingerprint key is `(sorted(hero_cards),
sorted(board_cards))`. This catches identical-shape hands but
NOT near-duplicates (e.g., Ah4h vs Ad4d on the same board is
strategically equivalent but distinct under this key). For v1.0
this is acceptable — the held-out set should be strategically
distinct anyway. v1.1 could add a card-class equivalence pass.]

## Hash + lock

The 50-hand spec block is bracketed by HTML comments below.
Compute SHA256 over the bracketed bytes (inclusive of the start
comment line through and including the end comment line).

Recommended one-liner:
```
python3 -c "
import hashlib, re
src = open('review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md').read()
m = re.search(r'<!-- HASHED-BLOCK-START -->.*?<!-- HASHED-BLOCK-END -->', src, re.S)
print(hashlib.sha256(m.group(0).encode()).hexdigest())
"
```

**v1.0 SHA256 (50-hand spec block):**
`8b553de0745bb50f5867a330d507eb106c04b9bc09f385e16966eec925b3b74b`

Block bounds at v1.0 lock: 1,005 lines, 40,404 bytes between the
two HTML comment markers. Locate via `grep -n HASHED-BLOCK file.md`
since absolute line numbers may shift if non-spec sections
(frontmatter, prerequisites, flags) are amended; the byte content
of the bracketed block is the lock — those non-spec amendments do
not break the lock and do not require version bump. Any edit to a
hand spec inside the bracketed block changes the hash and forces
v1.1 with re-verification.

## Mandatory pre-pilot solver-verification sample (10 hands)

These 10 hands MUST be solver-checked before this test set is used
in evaluation. Selected to span all confidence bands + all action
classes + the highest-stakes / most-disagreement-likely spots.

| Anchor ID | Conf | Action | Why selected |
|---|---|---|---|
| HOLDOUT_002_KJo_3way_T_paired | MEDIUM | BET_33 | TPGK on paired turn — known model-disagreement class (mirror d2410 risk surface). |
| HOLDOUT_007_AKo_4way_flop_air_double_paired | HIGH | CHECK | Air on double-paired flop in 4-way — multiway range collisions. |
| HOLDOUT_013_QQ_3bet_pot_J_high | HIGH | BET_66 | Overpair in 3-bet pot vs single villain — sizing class. |
| HOLDOUT_019_T9s_OESD_turn_face_bet | MEDIUM | CALL | Drawing-hand pot-odds vs implied — boundary CALL/FOLD. |
| HOLDOUT_024_AhKh_FD_NFD_river_brick | LOW | CHECK | Missed nut-flush draw on river paired board — bluff-or-give-up. |
| HOLDOUT_028_88_set_river_2flush_complete | HIGH | CHECK | Set on river when flush completes — value-vs-protect tension. |
| HOLDOUT_032_AQo_4way_open_face_3bet | HIGH | CALL | Preflop-equivalent geometry transferred to flop — vs 3bet from blinds. |
| HOLDOUT_037_J9s_BB_defend_K_high_flop | MEDIUM | CALL | BB defend texture, mid-strength + BDFD on K-high — soft tolerance. |
| HOLDOUT_043_22_set_3way_river_overcards | MEDIUM | BET_33 | Bottom set on river 3-way overcard runout — thin value vs check. |
| HOLDOUT_049_AhJh_river_NF_paired_check_back | HIGH | RAISE_66 | Nut flush facing turn donk → call → river bet on paired — RAISE for value not protected by pair. |

## UNCERTAIN tag census

- 4× `[UNCERTAIN-SOLVER: ...]` — spots flagged for explicit solver
  pre-pilot adjudication beyond the 10-hand mandatory sample
  (HOLDOUT_009, HOLDOUT_022, HOLDOUT_036, HOLDOUT_045)
- 2× `[UNCERTAIN: ...]` — non-solver uncertainties (24-hand
  calibration manifest location; near-duplicate equivalence in
  fingerprint check)

## 50-hand specification

Sizing convention (per `feedback_solver_aligned_sizing.md`,
pot-relative, NOT facing-bet-multiples):
- BET_25, BET_33, BET_66, BET_75, BET_150 (street-appropriate)
- RAISE_33, RAISE_66 (when raising an existing bet)
- All preflop opens are stack-100bb 6-max defaults: 2.5bb open from
  any opener position; 3-bets to 9bb IP / 11bb OOP; 4-bets to 21bb.
- All hands assume 100bb effective unless otherwise noted.
- Position abbreviations: UTG, HJ, CO, BTN, SB, BB.
- Action history convention follows MUST #11/#12 (same-street-collapsed
  with explicit bet sizes shown as fraction-of-pot-at-time-of-action).

<!-- HASHED-BLOCK-START -->

### HOLDOUT_001_KTs_BTN_flop_TP_dry — HU flop value bet

- Hero: `Ks Ts`
- Board (flop): `Tc 6h 2d`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5; flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPGK on dry low board, HU IP, c-bet for thin value
- Rationale: TPGK with backdoor flush, vs full BB calling range that
  is pair-light on this disconnected board. Standard small c-bet for
  thin value + denial vs unders/gutters. RAISE not in scope (no bet
  to raise); CHECK is the only credible alternative and gives up too
  much equity vs unders that fold to small bets.

### HOLDOUT_002_KJo_3way_T_paired — TT-on-turn checked-to-hero

- Hero: `Kh Jc`
- Board (turn): `Td 8s 4h Th`
- Position / stack: HJ / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, CO call, BB call;
  turn: BB check`
- Pot at decision: 16.6bb; SPR ≈ 5.85
- **Expected action:** BET_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: King-high overcards + BDFD on paired turn, 3-way,
  range-advantage continuation
- Rationale: HJ open range retains range advantage on T-paired turn
  vs CO call + BB call. Hero's actual hand is a marginal blocker
  bluff/equity hand (overcards to T, blocks KJ/KT/JT). Small bet
  pressures Tx-light caller ranges. [UNCERTAIN-SOLVER: 3-way
  trips-board node frequencies are sensitive to range model; flag
  for explicit solver verification.]

### HOLDOUT_003_77_UTG_flop_3way_overpair_dry — overpair multiway dry

- Hero: `7h 7d`
- Board (flop): `5c 4h 2s`
- Position / stack: UTG / 100bb eff
- Villains: 2 (BTN, BB)
- Action history: `preflop: UTG open 2.5, BTN call 2.5, BB call 2.5`
- Pot at decision: 7.5bb; SPR ≈ 13
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Small overpair on low connected flop, 3-way OOP
- Rationale: Overpair to 5-high board with backdoor straight blocker
  effects against capped multiway calling ranges. Small bet because
  draws (3x, 6x, 8s7s, 6c3c) and overcards have meaningful equity
  vs 77 — small bet denies cheaply, builds pot for strong-but-vulnerable
  value.

### HOLDOUT_004_AQo_CO_flop_air_3way_high — A-high air on Q-high 3-way

- Hero: `Ad Qc`
- Board (flop): `Qh 9s 5c`
- Position / stack: CO / 100bb eff
- Villains: 2 (BTN, SB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, SB call 2.5;
  flop: SB check`
- Pot at decision: 8bb; SPR ≈ 12.2
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPTK on dynamic flop, 3-way IP one caller
  remaining behind
- Rationale: TPTK (top pair top kicker) on Q95 vs BTN+SB. Standard
  c-bet for value vs Qx-weaker / mid-pairs / drawing hands; small
  size sufficient because deep enough to play turn/river streets.
  CHECK gives up equity realisation against BTN's float-heavy range.

### HOLDOUT_005_KQs_BTN_flop_HU_FD_BDSD — HU flush draw on K-high

- Hero: `Kc Qc`
- Board (flop): `5c 4c 2h`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5; flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Big draw + 2 overcards, HU IP, semi-bluff
- Rationale: ~16 outs (9 flush + 6 over + 3 BDSD overlap) ≈ 50%
  equity vs BB's range. Small c-bet for fold equity + builds pot
  for hits. CHECK acceptable but BET_33 is the higher-EV line
  given range advantage on low-card BB-call texture.

### HOLDOUT_006_QQ_HJ_turn_overpair_3way_brick — overpair turn brick

- Hero: `Qs Qd`
- Board (turn): `8h 5s 2c 7d`
- Position / stack: HJ / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, CO call, BB call;
  turn: BB check`
- Pot at decision: 15.6bb; SPR ≈ 6.23
- **Expected action:** BET_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Overpair vs sticky multiway range, turn
  protection-bet for size
- Rationale: Two callers on flop = pair-heavy + draw-heavy. 7d
  brings new draws (gutters, 7-pairs). QQ value-bets bigger on turn
  to protect equity + extract from 8x/5x/draws/lower overpairs that
  refuse to fold to small. Small overpair (TT/JJ) less clear; QQ
  clear.

### HOLDOUT_007_AKo_4way_flop_air_double_paired — A-high 4-way paired

- Hero: `Ah Kc`
- Board (flop): `Jc Js 4d 4h` *(NOTE: 4-card depiction is wrong;
  flop is 3 cards.)*
- Board (flop): `Jc Js 4d`
- Position / stack: BTN / 100bb eff
- Villains: 3 (UTG, HJ, BB)
- Action history: `preflop: UTG open 2.5, HJ call 2.5, BTN call 2.5,
  BB call 2.5; flop: BB check, UTG check, HJ check`
- Pot at decision: 10.5bb; SPR ≈ 9.3
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: A-high air on paired board, 4-way, position behind
  3 checkers
- Rationale: 4-way + double-paired board = checked-around ranges
  contain Jx + 4x at non-trivial frequency; UTG check after open is
  range-condensed. AK as pure air with 6 outs (3 A + 3 K) cannot
  bet for value or fold-equity 4-way. Take free card, play river-or-
  turn-bet-when-checked. CHECK strictly correct.

### HOLDOUT_008_T9s_BB_flop_OESD_face_cbet — BB defend OESD face cbet

- Hero: `Tc 9c`
- Board (flop): `8d 7h 2s`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65`
- Pot at decision: 6.6bb after BTN bet; to-call 1.65; pot odds 25%
- **Expected action:** RAISE_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Big draw OOP face flop c-bet, raise-as-semibluff
- Rationale: 8 OESD outs + 6 over outs (with caveat T9 vs 8x) ≈
  ~35-40% equity vs BTN c-bet range. Raising wins fold equity vs
  BTN's air + builds pot for hits. CALL is also defensible (the
  soft tolerance acknowledges this); RAISE chosen because it
  realises equity better OOP and protects against BTN barrel
  patterns that would charge the draw on bad turns.

### HOLDOUT_009_88_BB_flop_set_face_cbet_3way_LP — set on flop face HJ cbet

- Hero: `8h 8d`
- Board (flop): `8c 6s 3d`
- Position / stack: BB / 100bb eff
- Villains: 2 (HJ as opener, BTN as caller)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, BTN call`
- Pot at decision: 13.2bb; to-call 2.7; pot odds ≈ 17%
- **Expected action:** RAISE_66
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Top set OOP 3-way face c-bet + caller, raise to
  isolate + build
- Rationale: Top set 3-way after caller = need to deny equity to
  draws (54s, 75s, 97s, etc.) AND get value from HJ overpairs/Tx
  pair-plus. Calling lets BTN tag along with bad equity for hero.
  Raising isolates HJ's strong range (folds out BTN), charges
  draws, builds for stacks-in by river. Could mix CALL on certain
  textures. [UNCERTAIN-SOLVER: 3-way OOP raise frequencies vary
  by solver model — flag for verification.]

### HOLDOUT_010_AJo_HJ_flop_TP_face_donk — TP face BB donk

- Hero: `Ah Js`
- Board (flop): `Ac 9d 4s`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB, after preflop call)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB bet_33 1.65`
- Pot at decision: 6.6bb; to-call 1.65; pot odds 25%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK face BB donk OOP-from-OOP, call to bluff-catch
- Rationale: BB donk on A-high typically polarised into Ax-strong /
  draws+air. TPGK has good showdown value but is dominated by AQ+
  in BB donk-into-PFR range. CALL keeps villain's bluffs in,
  avoids being raised off equity. RAISE folds out worse + only
  gets called by better. CALL is the textbook line.

### HOLDOUT_011_55_CO_flop_underpair_3way_high_card — underpair high-card flop

- Hero: `5c 5h`
- Board (flop): `Kd 9s 4h`
- Position / stack: CO / 100bb eff
- Villains: 2 (BTN, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check`
- Pot at decision: 8bb; SPR ≈ 12.2
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Small underpair on high-card multiway flop, OOP-to-IP-after
- Rationale: 55 has ~20% equity 3-way on K94. Betting gets
  raised by Kx, called by 9x + draws + better underpairs. Check
  to realise equity, fold to bet, take free turn if checked. Pure
  CHECK in solvers for small underpairs vs ≥1 high card.

### HOLDOUT_012_QJs_BTN_turn_2pair_brick — QJ turn 2-pair brick

- Hero: `Qd Jd`
- Board (turn): `Qh Jc 7s 3h`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check`
- Pot at decision: 8.8bb; SPR ≈ 10.6
- **Expected action:** BET_75
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Strong 2-pair turn IP, big bet for value+protection
- Rationale: Two-pair vs BB call-call range that contains Qx, Jx,
  draws, overcards. Bet big to charge straight draws (T9, 98, KT)
  + build pot for stacks vs Qx. 33% leaves money behind vs polarised
  ranges; 75% extracts from full pair-plus + denies draws. Pure
  big-bet class.

### HOLDOUT_013_QQ_3bet_pot_J_high — QQ in 3bet pot J-high flop

- Hero: `Qh Qd`
- Board (flop): `Jh 7c 3s`
- Position / stack: BTN / 100bb eff (in 3-bet pot)
- Villains: 1 (BB after 3-bet)
- Action history: `preflop: BTN open 2.5, BB 3bet 11, BTN call 11;
  flop: BB check`
- Pot at decision: 22.5bb; SPR ≈ 3.96
- **Expected action:** BET_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Overpair in 3bet pot, BB checks-to-PFR-caller, value bet
- Rationale: 3-bet pot, BB's 3-bet range condensed (TT-AA, AK, some
  bluffs). BB checks J-high → range is condensed lower (KK/AA/AK
  plus give-ups). QQ has clear value vs missed AK, lower pairs,
  some Jx in BB's range. 66% builds pot for stacks-by-river vs
  KK/AA reverse-implied, denies AK + 7x equity. SPR low → bigger
  sizing.

### HOLDOUT_014_AJo_SB_river_TP_face_2bbl — TP river face 2 barrels

- Hero: `Ad Js`
- Board (river): `Ac 9h 4d Tc 5s`
- Position / stack: SB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, SB 3bet 11, BTN call 11;
  flop: SB bet_33 7.4, BTN call;
  turn: SB bet_75 22, BTN call;
  river: SB check, BTN bet_75 65`
- Pot at decision: 173bb; to-call 65; pot odds ≈ 27%
- **Expected action:** FOLD
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK river facing big bet after barrel-call, OOP, fold
- Rationale: SB 3-bet → barrel flop+turn → river check → BTN 75% pot.
  BTN's call-call-bet line on river is heavily polarised to
  straights (87s/JT/65s rare but possible), Ax-better (AQ/AK rare
  given BTN call vs 3bet), and bluffs (missed BD draws). At 27%
  pot odds, AJ unblocks bluffs (no spades/hearts blockers), but
  BTN range is value-heavy here. FOLD is the higher-EV play; CALL
  is defensible vs an aggressive opp pool (soft tolerance).

### HOLDOUT_015_AdKd_flop_NFD_HU_IP_paired — NFD on paired board HU IP

- Hero: `Ad Kd`
- Board (flop): `Td 8d 8s`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Nut flush draw + 2 overs on paired board, HU IP
- Rationale: NFD + AK overcards ≈ 47% equity vs BB. Small c-bet for
  fold equity vs unders + denies free turn. Not overplayed
  because paired board reduces villain draw frequency; small size
  keeps bluffs and weak Tx in the pot.

### HOLDOUT_016_KQs_HJ_turn_FD_brick_3way — KQ FD turn brick 3-way

- Hero: `Ks Qs`
- Board (turn): `9s 7s 4h 2d`
- Position / stack: HJ / 100bb eff
- Villains: 2 (BTN, BB)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, BTN call, BB fold;
  turn: HJ bet_33 5.5` *(intent: hero already bet — re-frame: this
  is HJ's decision after BB fold and BTN call)*
- Re-frame action history: `preflop: HJ open 2.5, BTN call 2.5,
  BB call 2.5; flop: BB check, HJ bet_33 2.7, BTN call, BB fold;
  turn: (HJ to act first vs BTN HU)`
- Pot at decision: 11.4bb; SPR ≈ 8.5
- **Expected action:** BET_75
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: NFD + 2 overs + BDSD turn vs single caller, polarised barrel
- Rationale: 9 flush outs + 6 overs ≈ ~38% equity vs BTN's flop-call
  range. Big barrel size on turn extracts from 9x/draws and gets
  folds from medium pairs that float flop. Half/threequarter pot
  is the polar-bet class — mixed with smaller barrels in solver.
  CHECK to realise equity also ok.

### HOLDOUT_017_44_BTN_flop_underpair_HU_dry_low — small underpair HU low flop

- Hero: `4c 4d`
- Board (flop): `8h 6c 2s`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Small underpair HU IP on low dry flop, mixed bet/check
- Rationale: 44 has decent showdown value but is dominated by 5x+,
  vulnerable to overcards. Small c-bet realises equity vs BB
  give-ups + protects vs 7s/9s/Tx that float flop. CHECK is also
  fine — solver mixes near 50/50 in this exact spot. BET chosen
  because hero blocks 4x straight outs of villain.

### HOLDOUT_018_AhTh_BB_flop_air_3way_3spades — air on monotone 3-way BB

- Hero: `Ah Th`
- Board (flop): `Qs 7s 3s`
- Position / stack: BB / 100bb eff
- Villains: 2 (CO, BTN)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO bet_33 2.7, BTN call`
- Pot at decision: 13.2bb; to-call 2.7; pot odds ≈ 17%
- **Expected action:** FOLD
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Air on monotone face cbet + caller 3-way OOP
- Rationale: No spade in hand, no pair, no draw. 3-way pot, two
  villains showing strength on a monotone flop. Pot odds favourable
  (17%) but realisation OOP 3-way is terrible. CALL bleeds chips;
  RAISE folds out only worse. Pure FOLD class. Mirrors the LITMUS_
  A4d_Qs5s7s air-on-monotone shape but as caller not bettor.

### HOLDOUT_019_T9s_OESD_turn_face_bet — T9 OESD turn face barrel

- Hero: `Tc 9c`
- Board (turn): `8d 7h Ks 2c` *(turn=2c, so order Kc-on-flop-then?)*
- Re-spec board: flop `Kc 8d 7h`, turn `2c` → board cards at decision:
  `Kc 8d 7h 2c`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6`
- Pot at decision: 15.4bb; to-call 6.6; pot odds ≈ 30%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: OESD facing turn barrel with no overcards, pot
  odds vs equity calc
- Rationale: 8 outs ≈ 18% direct + ~3-5% implied → ~21-23% equity.
  Pot odds 30% → not a price call by direct equity, but implied
  odds vs BTN's Kx + AK justify CALL on most tables. RAISE folds
  out bluffs (BTN range here is ~50% Kx+, ~30% bluffs). FOLD too
  tight given pot odds + clean draw. Soft tolerance: solver mixes
  CALL/FOLD.

### HOLDOUT_020_AKo_4way_flop_3spades_air — A-high air on monotone 4way

- Hero: `Ah Kc`
- Board (flop): `Qs 8s 5s`
- Position / stack: CO / 100bb eff
- Villains: 3 (BTN, SB, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, SB call 2.5,
  BB call 2.5; flop: SB check, BB check`
- Pot at decision: 10bb; SPR ≈ 9.75
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Air on monotone 4-way, no spade, position with one IP behind
- Rationale: 4-way monotone flop = at least one player likely has a
  spade. No spade in AK = no flush draw, can't bluff effectively,
  can't value. BTN behind likely floats with any pair or spade.
  Pure CHECK class (mirrors LITMUS_A4d).

### HOLDOUT_021_JJ_HJ_turn_overpair_face_x_donk — overpair face turn donk

- Hero: `Jh Jc`
- Board (turn): `8h 5d 2s 9c`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB bet_33 2.7`
- Pot at decision: 10.6bb; to-call 2.7; pot odds 25%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Overpair face turn donk small-size, call-not-raise
- Rationale: BB donk-leads on 9c turn = polarised to T7/76 / 9x /
  bluffs. JJ is a clear bluffcatcher: ahead of bluffs + 8x/5x,
  behind 9x/sets/straights. RAISE folds out bluffs and only gets
  called by better. CALL realises equity, plays river vs continued
  barrel.

### HOLDOUT_022_AcQc_BTN_river_FD_missed_2tone_paired — missed FD river paired

- Hero: `Ac Qc`
- Board (river): `Kc 7c 4h 2s 7d`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6, BB call;
  river: BB check`
- Pot at decision: 28.6bb; SPR ≈ 3.1
- **Expected action:** BET_75
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Missed NFD on paired river IP, polar bluff vs check
- Rationale: A-high checks behind for showdown value vs BB's
  call-call range (Kx that didn't raise, 7x slowplay, weaker
  flush draws). But hero blocks Acxc / AcKc nut combos. Polar
  bluff line: rep flush + Kx-better + 7x. Frequency-matched: solver
  mixes ~50/50 BET_75 vs CHECK. Tolerated as BET_75 strict-mode
  for evaluation; CHECK in soft. [UNCERTAIN-SOLVER: river-bluff
  frequency on paired NFD-miss highly opp-dependent.]

### HOLDOUT_023_KK_CO_flop_overpair_3bet_pot_dry — KK 3bet pot dry

- Hero: `Kh Kd`
- Board (flop): `7c 5h 2s`
- Position / stack: CO / 100bb eff
- Villains: 1 (BB after 3-bet)
- Action history: `preflop: CO open 2.5, BB 3bet 11, CO call 11;
  flop: BB bet_33 7.4`
- Pot at decision: 29.4bb; to-call 7.4; pot odds ≈ 25%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: KK 3bet pot face flop c-bet from 3-bettor, slowplay vs raise
- Rationale: KK on dry low flop in 3bet pot. Raising folds out bluffs
  + reps only AA. CALL keeps BB's range wide (continues bluffs to
  turn, lets QQ/JJ/AK barrel), maximises EV. Vs 4bet AA-only line
  KK is in clean shape to call-down. Solver pure CALL.

### HOLDOUT_024_AhKh_FD_NFD_river_brick — NFD missed river paired 2

- Hero: `Ah Kh`
- Board (river): `Th 8h 4c 2s 4d`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ check;
  river: BB check`
- Pot at decision: 8.3bb; SPR ≈ 11.5
- **Expected action:** CHECK
- Confidence: LOW
- Tolerance: soft
- Class-protected: Missed NFD river on paired board, IP, prior turn-check-back
- Rationale: Hero gave up turn (checked back), paired river. BB's
  range is condensed to Tx + air. Hero has A-high SDV but blocks
  a lot of Tx top-pair. Bluff line is plausible (rep AA/Tx better)
  but turn-check-back caps hero. Pure CHECK to take SDV. LOW
  confidence because turn-check-back-then-river-bluff is opp-pool
  dependent; against fold-heavy pools BET_66 also reasonable.

### HOLDOUT_025_AhJh_3way_river_TP_face_xraise — TP river face check-raise

- Hero: `Ah Jh`
- Board (river): `Ad 9c 4s Th 2c`
- Position / stack: BTN / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO bet_33 2.7, BTN call, BB fold;
  turn: CO check, BTN bet_75 9.6, CO call;
  river: CO check, BTN bet_33 13, CO raise to 50`
- Pot at decision: 89bb; to-call 37; pot odds ≈ 29%
- **Expected action:** FOLD
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPGK face river check-raise from preflop opener
  on flushless static runout
- Rationale: CO check-raised river on a board where the only credible
  value is 2-pair+, sets, straights (T9/A9/AT/44/99/AA). AJ is
  crushed. Pot odds 29% but value-only-villain range = call needs
  ≥30% bluffs which is unrealistic for the unprovoked check-raise
  line on a static board. Pure FOLD.

### HOLDOUT_026_TT_BB_flop_overpair_3way_xc_lim — TT overpair multiway low

- Hero: `Tc Th`
- Board (flop): `6h 5c 3d`
- Position / stack: BB / 100bb eff
- Villains: 2 (HJ, BTN)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, BTN call`
- Pot at decision: 13.2bb; to-call 2.7; pot odds ≈ 17%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Mid overpair 3-way OOP face cbet + caller, call-not-raise
- Rationale: TT is solid bluffcatcher 3-way: ahead of HJ's pair-light
  bluff frequency + BTN floats. Behind sets/two-pair/straights but
  those are minority. RAISE bloats pot vs uncapped HJ. CALL keeps
  range wide, plays turn vs likely double-barrel. Pure CALL class
  for mid overpair.

### HOLDOUT_027_AKs_BTN_flop_TPTK_3way_two_tone — TPTK 3-way two-tone

- Hero: `Ad Ks`
- Board (flop): `Ah 8h 3s`
- Position / stack: BTN / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO check`
- Pot at decision: 8bb; SPR ≈ 12.2
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPTK 3-way IP on two-tone, range-advantage value bet
- Rationale: BTN call has uncapped range incl. AK/AQ; CO+BB checked.
  Standard small bet for value vs Ax-weaker / heart draws / underpairs;
  builds pot for stacks-by-river vs 8x/3x calls. CHECK loses too
  much equity vs heart-draw realisation.

### HOLDOUT_028_88_set_river_2flush_complete — set river flush completes

- Hero: `8h 8d`
- Board (river): `8c 6h 3s 2h Kh`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ bet_75 6.6, BB call;
  river: BB check`
- Pot at decision: 28.6bb; SPR ≈ 3.1
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Set on river when flush completes, value-vs-protect
  trap, OOP-checked-to
- Rationale: BB's call-call range on this runout is heavy with hearts
  (flush draws), Kx (paired turn now top pair), and slowplays. River
  Kh completes hearts AND adds Kx top pair. Betting gets called by
  flushes (hero loses) + folded by Kx-no-heart that won't pay. CHECK
  realises showdown vs Kx + bluffs vs missed straight draws. Could
  reasonably mix BET_33 vs aggressive BB rivers but CHECK is
  modal-EV.

### HOLDOUT_029_QJo_HJ_flop_air_4way_low_flop — QJo air 4-way low

- Hero: `Qs Jc`
- Board (flop): `7d 4h 2c`
- Position / stack: HJ / 100bb eff
- Villains: 3 (CO, BTN, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BTN call 2.5,
  BB call 2.5`
- Pot at decision: 10bb; SPR ≈ 9.75
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: PFR-air on low flop 4-way, give up
- Rationale: 4-way pot on 742 = at least one player has 7x/4x/2x or
  pair frequency very high. QJ has 6 outs (3 Q + 3 J), no draw, no
  blocker effects. Bet folds out only worse, gets called/raised by
  better. CHECK pure. Realise equity, take free card.

### HOLDOUT_030_99_BTN_flop_overpair_HU_K_high — 99 underpair HU K-high

- Hero: `9c 9h`
- Board (flop): `Ks 7d 3c`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Mid pair on K-high HU IP, c-bet for SDV+denial
- Rationale: 99 on K73 vs BB call range = ahead of pair-low + air,
  behind Kx. Small c-bet folds out 5x/6x/8x/JTo and gets called
  by 7x. Cheap denial vs BB's float range. Standard small c-bet
  HU IP on K-high.

### HOLDOUT_031_AhAd_HJ_river_overpair_face_xraise_river — AA face river check-raise

- Hero: `Ah Ad`
- Board (river): `9c 7h 4s 2d 2h`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ bet_75 6.6, BB call;
  river: BB check, HJ bet_33 9.5, BB raise to 35`
- Pot at decision: 73bb; to-call 25.5; pot odds ≈ 26%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: AA face river check-raise on paired runout, call-down
- Rationale: BB check-raises river on paired board. Value range:
  22 (full house), 99/77 (full house), some 4x trips. Bluffs:
  missed flush draws + busted straight draws (8h6h, JhTh, 65s).
  Pot odds 26% requires ~26% bluff frequency in BB's range. AA
  has SDV vs all bluffs + loses to all value. Solver-typical
  CALL frequency ~50-70%. CALL chosen; FOLD also defensible.

### HOLDOUT_032_AQo_4way_open_face_3bet — AQo open face 3bet 4way limp scenario

- Hero: `Ad Qh`
- Board: preflop decision (so this is 4-way preflop)
- Position / stack: HJ / 100bb eff
- Villains: 3 (CO calls, BTN calls, BB 3bets)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BTN call 2.5,
  BB 3bet to 14`
- Pot at decision: 21.5bb; to-call 11.5; pot odds ≈ 35%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Preflop AQo face squeeze with 2 cold-callers behind
- Rationale: Squeeze size 14bb (5.6x) is suppressed by callers'
  presence. AQo behind a 3-bettor BB sees CO+BTN cold-callers
  also have to act. With BTN/CO unlikely to 4-bet thin (likely
  fold or call), HJ closes vs BB's squeeze range (TT+, AQ+,
  some bluffs). AQo has decent equity + position vs the squeeze
  cold-caller multiway. 4bet too thin (folds bluffs); CALL with
  position is standard. FOLD is over-tight.

### HOLDOUT_033_KQs_CO_flop_TPGK_HU_face_donk_K_high — KQ TPGK face BB donk

- Hero: `Kc Qd`
- Board (flop): `Kh 9s 4c`
- Position / stack: CO / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: CO open 2.5, BB call 2.5;
  flop: BB bet_33 1.65`
- Pot at decision: 6.6bb; to-call 1.65; pot odds 25%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK face BB donk-lead, call vs raise
- Rationale: BB donks ~33% on K-high → polarised to slowplay (KQ/KJ/KT/
  KK rare, 99) + draws (T8s, J8s) + air. KQ has TPGK (Q kicker
  decent vs BB donk range). RAISE folds out bluffs and gets called
  by better Kx (KQ/KJ/KT). CALL keeps BB's range wide for turn.

### HOLDOUT_034_22_SB_flop_underpair_air_3way_high_card — 22 air 3way high card

- Hero: `2c 2h`
- Board (flop): `Ad Th 6c`
- Position / stack: SB / 100bb eff
- Villains: 2 (HJ, BTN)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, SB call 2.5,
  BB fold; flop: SB check, HJ check`
- Pot at decision: 8bb; SPR ≈ 12.2
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Tiny underpair 3-way on AT-high after both villains check
  to BTN
- Rationale: 22 has ~6% equity 3-way on AT6. Both checked to BTN —
  hero (SB) acts first on turn. Pure CHECK class for tiny pair on
  high-card multiway flop. Bet gets raised by Ax + called by Tx.

### HOLDOUT_035_8d8h_BTN_turn_set_2flush_complete — set turn flush complete

- Hero: `8d 8h`
- Board (turn): `8c 6c 3c 2d`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check`
- Pot at decision: 8.8bb; SPR ≈ 10.6
- **Expected action:** BET_75
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Top set when flush completed on turn, IP, value+protect
- Rationale: Top set vs BB call range (lots of clubs, mid-pair). 2d
  turn is brick. Big bet for value vs Tx-pair / underpairs / clubs
  refusing to fold + protects vs straight draws (54, 75, 97). 75%
  near-pot is solver-modal; could mix POT (BET_100 not in standard
  sizing tags so capped at 75%).

### HOLDOUT_036_AhKh_HJ_flop_TPTK_4way_dry — TPTK 4-way dry

- Hero: `Ah Kh`
- Board (flop): `Ad 7c 2s`
- Position / stack: HJ / 100bb eff
- Villains: 3 (CO, BTN, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BTN call 2.5,
  BB call 2.5`
- Pot at decision: 10bb; SPR ≈ 9.75
- **Expected action:** BET_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPTK 4-way OOP, range-narrow value bet
- Rationale: TPTK 4-way on dry A72. HJ retains range advantage on Ax.
  Small bet vs sticky multiway range (Ax-weaker + 7x). Some merit to
  CHECK 4-way to control pot, but TPTK is too strong to give up
  street. [UNCERTAIN-SOLVER: 4-way OOP cbet frequency on Axx-dry
  is a known disagreement spot — flag for explicit verification.]

### HOLDOUT_037_J9s_BB_defend_K_high_flop — BB defend K-high BD draws

- Hero: `Jh 9h`
- Board (flop): `Kh 8s 5d`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65`
- Pot at decision: 6.6bb; to-call 1.65; pot odds 25%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: BB defend texture with BDFD + BDSD + overcards, call vs fold
- Rationale: J9hh on K85 = BDFD (hearts) + BDSD (T7/QT runouts) + 2
  cards under K. ~28-32% equity vs BTN cbet range. Pot odds 25% =
  good price + implied odds on T/Q turns. RAISE thin; CALL preferred.
  FOLD over-tight given price + multi-way runout potential.

### HOLDOUT_038_QQ_BTN_flop_overpair_HU_low_dry — QQ on low dry flop HU

- Hero: `Qh Qd`
- Board (flop): `7c 4s 2h`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Strong overpair HU IP low dry, small c-bet for value
- Rationale: Standard small c-bet HU IP. QQ ahead of full BB call
  range minus 22/44/77 sets. Small size keeps bluffs in (BB float
  with Ax-K-high, gutters), denies overcards' equity realisation.

### HOLDOUT_039_AcQs_HJ_river_TP_face_x_lead_river — TPGK face river donk

- Hero: `Ac Qs`
- Board (river): `Ah 9d 4c 7h 5s`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ check;
  river: BB bet_75 7.5`
- Pot at decision: 17.5bb; to-call 7.5; pot odds ≈ 30%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK face river donk after turn check-back, OOP-from-PFR
- Rationale: Hero turn check-back caps; BB's river donk-lead 75% is
  polarised to 6x (straights), 5x rivered 2pair, A-better, plus
  bluffs (busted hearts JT/QJ/T8). AQ has SDV. Pot odds 30% requires
  ~30% bluffs which is realistic for donk-river polar lines. CALL
  modal; FOLD vs nit pool ok.

### HOLDOUT_040_77_HJ_flop_underpair_3way_K_high — 77 underpair K-high 3-way

- Hero: `7h 7d`
- Board (flop): `Kc 9d 5s`
- Position / stack: HJ / 100bb eff
- Villains: 2 (BTN, BB)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5`
- Pot at decision: 7.5bb; SPR ≈ 13
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Small-mid underpair K-high 3-way OOP from PFR
- Rationale: 77 face 2 callers on K95 = ~15% equity 3-way. Bet gets
  raised by Kx + sets, called by 9x + draws (BTN with TJ/T9 etc).
  CHECK to realise equity, fold to bet, take free turn if checked.

### HOLDOUT_041_KsTs_CO_flop_TP_HU_2tone_K_high — KT on KsTs flop TPTK

- Hero: `Kh Tc`
- Board (flop): `Ks 9s 4d`
- Position / stack: CO / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: CO open 2.5, BB call 2.5; flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPGK on draw-heavy flop HU IP, bigger bet for protection
- Rationale: KT on K9s4d (two-tone spades) = TPGK on draw-heavy
  texture. Vs BB call range, hero ahead of K-weaker, behind KQ/AK.
  BET_66 (vs BET_33) chosen for protection vs flush draws + straight
  draws (Q-high, JTs, 87s). Solver mixes BET_33/BET_66 — BET_66 is
  the protect-equity choice for TPGK on draw-heavy.

### HOLDOUT_042_4c4d_HJ_flop_underpair_HU_2overs_low — small underpair on midflop

- Hero: `4c 4d`
- Board (flop): `Th 7d 5c`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5; flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** CHECK
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Small underpair on dynamic mid-flop HU IP, mixed bet/check
- Rationale: 44 on T75 = ~30% equity vs BB range. Wet board = 8/9/6
  draws, Tx top pair. Small c-bet ok for SDV, but solver mixes ~50/50
  with CHECK. CHECK chosen because realisation is decent IP (closed
  action on flop), avoids being raised by 8x/9x draws.

### HOLDOUT_043_22_set_3way_river_overcards — bottom set 3-way river over

- Hero: `2c 2h`
- Board (river): `9d 6h 2d Kh Qs`
- Position / stack: BTN / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO bet_33 2.7, BTN call, BB fold;
  turn: CO check, BTN check;
  river: CO check`
- Pot at decision: 13.4bb; SPR ≈ 6.7
- **Expected action:** BET_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Bottom set on river with overcard runout (K, Q),
  thin value 3-way-down-to-HU
- Rationale: Bottom set faded straight draws and didn't get called by
  worse on flop bet only. Turn checked through. River K + Q runout
  scary but CO checks river → likely AT-pair-or-worse / Kx-rare
  (CO would bet Kx). Small bet for thin value vs CO's missed-draw
  call-frequency + 9x. Big bet folds out everything; check loses
  thin value vs Tx/Jx that call small. Mixed in solver — small bet
  is the modal value-extract.

### HOLDOUT_044_AdQh_HJ_flop_air_4way_low — AQ air 4-way low flop

- Hero: `Ad Qh`
- Board (flop): `9s 6c 3d`
- Position / stack: HJ / 100bb eff
- Villains: 3 (CO, BTN, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BTN call 2.5,
  BB call 2.5`
- Pot at decision: 10bb; SPR ≈ 9.75
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: PFR-air on low flop 4-way with backdoor potential
- Rationale: 4-way 963 = high pair frequency in callers' ranges. AQ
  air with BD diamonds + 6 over outs, but bet folds out only worse
  4-way. CHECK to realise equity, take free turn, see if any A/Q/3rd
  diamond comes.

### HOLDOUT_045_KhQh_BB_flop_TP_3bet_pot_face_cbet — KQ TP face cbet 3bet pot

- Hero: `Kh Qh`
- Board (flop): `Kc 7d 2c`
- Position / stack: BB / 100bb eff (in 3-bet pot)
- Villains: 1 (BTN after 3-bet)
- Action history: `preflop: BTN open 2.5, BB 3bet 11, BTN call 11;
  flop: BB bet_33 7.4`
- Pot at decision: 29.4bb after BB bet (pot 22 → 22+7.4=29.4)
- *(re-frame: this is BB-as-aggressor cbetting 3-bet pot;
  decision-on-hero is BB cbet → action complete; reframe needed)*
- Re-frame: `preflop: BTN open 2.5, BB 3bet 11, BTN call 11;
  flop: BB check, BTN bet_33 7.4`
- Pot at decision: 29.4bb; to-call 7.4; pot odds ≈ 25%
- **Expected action:** RAISE_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK in 3bet pot OOP face IP cbet, check-raise for value
- Rationale: BB 3bet then check-call is normal; check-raise on K-high
  is a strong-hand line mixed with bluffs (AhXh, QhJh). KQ TPGK has
  enough equity to check-raise vs BTN's small cbet range (mostly
  wide bluffs given pot is bloated). Solver mixes CALL/RAISE_33;
  raise builds pot for stack-by-river vs Kx-weaker / draws. CALL
  also fine. [UNCERTAIN-SOLVER: 3-bet-pot OOP check-raise frequencies
  swing materially with stack depth — flag for explicit verification.]

### HOLDOUT_046_99_HJ_turn_overpair_face_xraise_HU — 99 turn face cr HU

- Hero: `9h 9d`
- Board (turn): `8c 6h 4s 2d`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ bet_75 6.6, BB raise to 22`
- Pot at decision: 36.85bb; to-call 15.4; pot odds ≈ 29.5%
- **Expected action:** FOLD
- Confidence: LOW
- Tolerance: soft
- Class-protected: Mid overpair face turn check-raise from BB caller, fold
- Rationale: BB check-raises turn after call-call on 8642 = polarised
  to 75/53 straights, sets (88/66/44), 8x two-pair (84/86), and
  rare bluffs. 99 has SDV vs bluffs but loses to all value classes.
  At 29.5% pot odds, requires ~30% bluffs which is generous for
  a turn check-raise OOP (typical solver bluff-freq ~15-20%). FOLD
  modal. CALL defensible vs aggressive opponents (LOW band reflects
  this disagreement).

### HOLDOUT_047_AcKs_HJ_flop_TPTK_3bet_pot_HU_dynamic — TPTK 3bet pot dynamic

- Hero: `Ac Ks`
- Board (flop): `Kh 9h 8s`
- Position / stack: HJ / 100bb eff (in 3-bet pot)
- Villains: 1 (BTN after BTN 3bet HJ open and HJ called)
- Action history: `preflop: HJ open 2.5, BTN 3bet 9, HJ call 9;
  flop: HJ check`
- *(re-frame: this is HJ checking → BTN to act → if BTN cbets, HJ's
  decision)*
- Re-frame: `preflop: HJ open 2.5, BTN 3bet 9, HJ call 9;
  flop: HJ check, BTN bet_33 6`
- Pot at decision: 24bb; to-call 6; pot odds 25%
- **Expected action:** RAISE_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPTK 3bet pot OOP face IP cbet on dynamic, check-raise
- Rationale: K98 two-tone is dynamic; TPTK with NO-flush-block (no
  hearts) is a strong check-raise candidate vs BTN's small cbet
  range. BTN's range is wide bluffs + AA/KK condensed. Check-raise
  builds pot for stacks vs KK/AK-suited blockers, charges JT/QJ/T7
  draws, denies hearts. Solver-typical RAISE in this class.

### HOLDOUT_048_Td9d_BTN_river_FD_missed_paired — Tdiamond missed FD paired river

- Hero: `Td 9d`
- Board (river): `Ad 8d 4c 2s 4h`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6, BB call;
  river: BB check`
- Pot at decision: 28.6bb; SPR ≈ 3.1
- **Expected action:** BET_150
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Missed FD (non-nut) paired river IP, polar bluff with no SDV
- Rationale: T-high after barrel-barrel on Ad8d → checked-river. BB's
  range is condensed to Ax (limp-checked twice) + 8x + busted draws.
  T9 has zero SDV. Polar bluff overbet (BET_150) reps 4x trips +
  flushes, gets folds from Ax-weaker that gave up. Solver pure
  bluff line for missed-FD-with-no-SDV.

### HOLDOUT_049_AhJh_river_NF_paired_check_back — nut flush face river bet on paired

- Hero: `Ah Jh`
- Board (river): `Kh 9h 4c 2h Kc`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN check;
  river: BB bet_33 2.8`
- Pot at decision: 11.1bb; to-call 2.8; pot odds ≈ 25%
- **Expected action:** RAISE_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Nut flush facing small river donk on paired board, raise for value
- Rationale: BTN turn-check-back caps own range; BB river donk on
  paired board = polarised to Kx (trips/full house), some bluffs.
  Hero has nut flush. Just-call gets ~3bb extra; raise gets value
  from Kx (BB will pay-call most of the time given pot odds and
  BB's polarised donk). Raise-66 chosen because bigger raise risks
  folding out non-trip Kx; small raise extracts thin value.

### HOLDOUT_050_AsKs_CO_flop_NFD_TPTK_3bet_pot — NFD+TPTK 3bet pot CO

- Hero: `As Ks`
- Board (flop): `Kd 7s 4s`
- Position / stack: CO / 100bb eff (in 3-bet pot)
- Villains: 1 (BB after 3-bet)
- Action history: `preflop: CO open 2.5, BB 3bet 11, CO call 11;
  flop: BB bet_33 7.4`
- Pot at decision: 29.4bb; to-call 7.4; pot odds ≈ 25%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: NFD + TPTK in 3bet pot face cbet, slowplay vs raise
- Rationale: NFD + TPTK = ~70% equity vs BB cbet range. Raise folds
  out bluffs (AQ/JJ/QQ no-spade) and reps only AA. CALL keeps BB's
  range wide for turn barrel + lets hero hit flush card cheaply.
  Solver pure CALL in 3bet pot for nut combo draws.

<!-- HASHED-BLOCK-END -->

## Per-class coverage breakdown

| Class-protected tag | Hands | Notes |
|---|---|---|
| TPGK / TPTK on dry / two-tone (HU IP) | 7 | well-covered |
| TPGK / TPTK on multi-way + 3-bet-pot textures | 6 | well-covered |
| Overpair (low/mid/high) value classes | 7 | well-covered |
| Air on monotone / paired / 4-way (give-up class) | 6 | well-covered |
| Mid/small underpair multiway / HU | 5 | adequate |
| Big draws (FD/NFD/OESD) — semibluff/call/check | 7 | well-covered |
| Set / two-pair (value+protect) | 4 | adequate (4 hands) |
| Bluff-catch face-bet / face-raise | 5 | adequate |
| Polar-bluff missed FD river | 3 | adequate |
| Preflop face-3bet cold-caller behind | 1 | flagged below |

## Concerns / flags worth surfacing to reviewer

1. **Preflop class is thin.** Only HOLDOUT_032 is a preflop spot. The
   held-out test set is overwhelmingly postflop. If the v2.4 model
   is also evaluated on preflop accuracy, supplement is needed.
   [Per the locked Stage 4 plan, postflop is the ship-gate scope, so
   this is consistent — but flag to reviewer.]

2. **River class is 10 hands (20%).** Adequate but lighter than
   flop+turn. River decisions are higher-stakes (last-street-pot-
   commit) and the model's weakest stage historically. Reviewer
   may want to raise river share to ~30% in v1.1.

3. **No 5-way+ hands.** Test set is HU/3-way/4-way only. v2.4 is the
   3-way specialist; 5-way+ is out-of-scope. Confirmed consistent
   with progressive-model-chain.

4. **Soft-tolerance count (15 hands) is high.** The DRAFT did not
   set a soft-vs-strict target. Reviewer may want to push more
   spots to strict-tolerance to make the test set harsher; current
   choice is calibrated to MIXED-strategy reality.

5. **Authoring is general-purpose-as-gto-expert, not a dedicated
   gto-expert dispatch.** Per locked Stage 4 D3 the dedicated
   author is preferred but the general-purpose fallback is
   authorised. A dedicated agent's reviewer pass is strongly
   recommended.

6. **Non-overlap is fingerprint-based** `(sorted(hero), sorted(board))`.
   Does not catch suit-isomorphic near-duplicates. v1.1 could add
   card-class equivalence; for v1.0 the held-out hands are
   strategically distinct anyway.

7. **24-hand calibration manifest** location not located as a discrete
   file in repo. Cross-check is currently subsumed in the
   pass1/factory full-corpus scan. If a separate manifest exists in
   `review/recovered/` or off-tree, a directed pre-pilot scan is
   needed.

8. **Two hands have shape ambiguity in the action history**
   (HOLDOUT_007 had a 4-card flop typo corrected inline; HOLDOUT_016,
   HOLDOUT_019, HOLDOUT_045, HOLDOUT_047 have re-frame notes
   embedded). These inline corrections should be flattened in v1.1
   for cleaner JSONL export.

9. **One hand uses BET_150 (HOLDOUT_048 overbet).** Confirm with
   reviewer that BET_150 (1.5×pot) is supported by the action-class
   vocabulary in `gto_model.py` — the model currently emits a
   5-class action `(FOLD, CHECK, CALL, BET, RAISE)` without
   distinguishing sizes at output. Sizes here are documentation
   for the labeller / solver; the evaluator must be configured to
   coalesce all BET_* into BET when scoring.

10. **Action distribution skews BET-heavy and FOLD-light.** Achieved:
    20 BET (40% vs 26% target, +7 over) / 4 FOLD (8% vs 20% target,
    −6 under). Underlying cause: the post-flop checked-to-hero
    decision class is dominantly BET in solver-correct play (small
    c-bet for thin value/denial), and FOLD spots are rare in
    PFR-aggressor scenarios. To rebalance to target, v1.1 would need
    ~6 hands re-authored as face-bet → FOLD spots (e.g., dominated
    bluffcatchers, draws short of pot odds). Flagging for reviewer to
    decide: accept v1.0 as-is (reflecting solver-realistic
    distribution) vs require v1.1 rebalance pre-pilot. **Per-class
    breakdowns** in the evaluation report can normalise for this if
    the v1.0 distribution is accepted.

11. **LOW-confidence band is under target (2 vs 5).** Only HOLDOUT_024
    and HOLDOUT_046 carry LOW. To match the 10% target, 3 more
    boundary spots would need re-authoring. Acceptable for v1.0 if
    reviewer agrees the test set is intentionally biased toward
    solver-defensible spots (LOW = author admits the call is opinion-
    divided, which is a small fraction of real spots).

12. **No FOLD in 10-hand solver-verification sample.** Initial author
    pick was driven by class-protected diversity; FOLD spots are the
    easiest-to-solver-verify so they were deprioritised. Reviewer
    should consider swapping in HOLDOUT_046 (FOLD, LOW) for one of
    the current 10 if FOLD coverage in the solver sample matters.

## Usage protocol

### Single-shot evaluation

When v2.4 candidate model is ready (post-Stage 5):

1. Load held-out test set (this file + JSONL companion produced by
   builder).
2. Run model inference on all 50 hands (no human in the loop;
   automated).
3. Score against held-out labels (treating BET_* as BET, RAISE_* as
   RAISE for the 5-class model output; per-hand soft-tolerance
   scoring per `tolerance_rules` in `calibration_anchors.json`).
4. Report accuracy + per-class-protected breakdown + per-confidence-
   band breakdown + per-street breakdown + per-num-opponents
   breakdown.

**No iteration.** If v2.4 candidate scores poorly on held-out: the
candidate is rejected, NOT the held-out set. Investigate via Stage
5 multi-seed audits + Stage 4 corpus quality checks. Don't tweak
the held-out set "to make v2.4 look good."

### Held-out hand exposure

After single-shot evaluation, the held-out hands MAY be added to the
labelling corpus for v2.5+ (test value is exhausted). For v2.4
specifically, the held-out set is **single-use**.

## Disposition for v2.5+

For v2.5 ship, a NEW held-out test set is constructed. The v2.4
held-out hands move into the training corpus (if owner approves) or
get archived. The new held-out set is constructed with the same
authorship + non-overlap protocol against v2.5-era corpora.

## Self-consistency closure

Self-consistency pass run after authoring:

1. **All 50 hands have all required fields.** Verified — Anchor ID,
   hero hand, board, position+stack, action history (with re-frame
   notes where original draft was ambiguous), villain count,
   expected action, confidence band, tolerance, rationale, class-
   protected. PASS.

2. **Action sizing tags use solver-aligned conventions.** Verified
   per `feedback_solver_aligned_sizing.md` — flop 25%/66%, turn
   33%/75%, river 33%/75%/150%, RAISE 33%/66% pot-relative. PASS.

3. **Pot/SPR arithmetic spot-check.** Verified for HOLDOUT_001
   (5.5bb pot at flop after open-call: 2.5 + 2.5 + 0.5 SB + (was
   1bb BB folded to call, so 1.5bb of dead money + 5bb action) =
   5.5bb correct; 100bb − 2.5bb = 97.5bb stack; SPR 97.5/5.5 =
   17.7), HOLDOUT_013 (open 2.5 + 3bet 11 + call 11 + 0.5 SB dead
   = ~25bb pre-pot; pot pre-flop = 22.5bb after blinds returned;
   SPR (100−11)/22.5 = 3.96 ≈ 89/22.5). Spot-check sample passes;
   full audit in reviewer pass.

4. **Confidence band distribution.** 30 HIGH / 18 MEDIUM / 2 LOW.
   HIGH on target, MEDIUM +3, LOW −3. PARTIAL — see flag #11.

5. **Action distribution.** 4 FOLD / 10 CHECK / 11 CALL / 20 BET /
   5 RAISE. RAISE on target, CHECK/CALL within ±2, BET +7, FOLD
   −6. PARTIAL — see flag #10 for explanation + reviewer
   recommendation.

6. **10-hand solver sample spans bands + classes.** 4 HIGH / 5
   MEDIUM / 1 LOW; actions: 0 FOLD / 2 CHECK / 3 CALL / 4 BET /
   1 RAISE. PARTIAL — FOLD class missing — see flag #12 for
   reviewer decision (swap HOLDOUT_046 into the 10-sample).

7. **Non-overlap verification (programmatic).** Built fingerprint
   set from 56 jsonl files in `training-data/` (1,996 unique
   `(sorted(hero), sorted(board))` keys covering 4,034 records).
   Cross-checked all 50 holdout fingerprints. **Result: 0 matches.**
   PASS.

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` — Stage 4
  plan §7 specifies the held-out set as a Stage 6 addition
- `MASTER_PLAN (1).md` — existing Stage 6 ship gate (5 litmus tests)
- `LABELLING_PIPELINE.md` — calibration exam construction (similar
  authoring discipline)
- `feedback_solver_findings.md` — solver verification protocol
- `feedback_solver_aligned_sizing.md` — bet sizes for solver
  verification
- `STAGE5_RETRAIN_PROTOCOL_v1_0.md` — model that this set tests
- `STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md` — origin draft
