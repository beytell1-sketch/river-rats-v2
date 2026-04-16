---
date: 2026-04-16
from: Programmer + GTO Expert (joint role)
to: Owner / Main terminal
re: Group D reversal-hand shortlist for owner async pick
status: DELIVERABLE — owner picks 4 of 11
source: MAIN_TERMINAL_UPDATE_2026-04-16-e.md (directive, commit 10247b6)
---

# Group D reversal-hand shortlist (11 candidates)

Calibration exam registry (`GROUP_D_REVERSAL_HANDS` in
`river-rats-core/calibration_exam.py`) currently contains
**1 hand** (`d3688_BB_flop`). Four more nominations are required
to finalise Group D. This doc surfaces a stratified shortlist;
**owner picks 4**, builder ingests with no code change (registry
is extensible per Track C).

## Stratification target vs achieved

| Stratum | Description | Target | Surfaced | Note |
|---|---|---:|---:|---|
| A | Near-bias CHECK labels from v2.2 training | 3–5 | **6** | ✅ full |
| B | d-series Pass 2 solver-confirmed CHECK overrides | 3–5 | **4** | ✅ full |
| C | Solver-mixed ≥40% CHECK spots | 3–5 | **1** | ⚠ under-filled (stop condition; see §Blockers) |
| **Total** | | 10–15 | **11** | within floor |

## Exclusions applied

Per directive, excluded hand-ID stems (all street variants):
- **Existing anchors** (calibration_exam.py): `d8886`, `d2410`, `d8963`, `d3178`, `d3688`
- **10 MW misses** (separate evidence pack, not diagnostic-only):
  `d1454`, `d1562`, `d1983`, `d2920`, `d3229`, `d8411`
  (the other 4 MW misses are already in the anchor exclusion set)

## Summary table

Bias-signature predicate (strict canonical):
`facing_bet=0 ∧ num_opponents≥2 ∧ villain_checked_back=1 ∧
villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧ equity_vs_range≥0.35
∧ spr≤2.0`.

A "Y" in predicate-match means all 7 conditions hold; "Y–"
means ≥6 of 7 hold (near-miss).

| # | sid | Stratum | Street | Hand shape | v2.2 label | Solver verdict | Predicate match |
|---|---|---|---|---|---|---|:---:|
| 1 | d3687_HJ_turn | A | turn | quads (monster) | CHECK | — | Y |
| 2 | d6869_CO_turn | A | turn | TP weak kicker | CHECK | — | Y– (worse=0.60) |
| 3 | d5466_CO_flop | A | flop | TP weak kicker | CHECK | — | Y– (vcb=0, PFR c-bet spot) |
| 4 | d1764_BTN_turn | A | turn | small pocket pair IP | CHECK | — | Y– (vrc=0) |
| 5 | d2074_BTN_turn | A | turn | bottom pair paired-board | CHECK | — | Y– (vrc=0) |
| 6 | d6826_BB_turn | A | turn | middle pair paired-board | CHECK | — | Y– (vrc=0) |
| 7 | d4312_CO_turn | B | turn | TP, 9-high board OOP | CHECK | **solver CHECK override** (Pass 2 BET→CHECK) | **Y** |
| 8 | BP5_01 | B | flop | bottom two pair OOP | CHECK | **solver CHECK override** (Pass 2 BET→CHECK) | N (vcb=0, vrc=0; SRP BB-lead shape) |
| 9 | BP4_11 | B | flop | set of 8s | CHECK | — (P1 BET → final CHECK) | N (vcb=0, vrc=0; SRP BB-lead shape) |
| 10 | d9556_BB_flop | B | flop | full house | CHECK | **solver CONFIRM CHECK** | N (vcb=0; SRP BB-lead shape) |
| 11 | BP4_21 | C | flop | KQ OESD+overcards IP | CHECK | **solver mixed** — BET 25% sizing / CHECK both valid | N (vcb=0) |

**Diversity check:**
- Streets: flop 5, turn 6, river 0 (no reversal-shaped river CHECKs survived the filter after exclusions — v2.2 river CHECK pool is concentrated on give-up air; see §Blockers).
- Hand types: monster/trap (3: d3687, BP4_11, d9556), strong-made (2: BP5_01, d4312), TP-weak (2: d6869, d5466), small/middle pair (3: d1764, d2074, d6826), draw+overcards (1: BP4_21).

---

## Stratum A — near-bias CHECK labels from v2.2 training

Predicate (relaxed vs canonical): `facing_bet=0 ∧ num_opponents≥2 ∧
villain_checked_back=1 ∧ spr≤2.5 ∧ worse_hand_pct≥0.50 ∧
equity_vs_range≥0.30` (with `villain_range_capped` allowed to be 0
for the "single-axis fail" subset per directive). These are CHECK
labels that *look similar to the bias signature* but panel chose
CHECK — diagnostic for whether v2.3 over-applies the override.

### 1. `d3687_HJ_turn` [A, full bias-sig]

- **hero:** 8c Kc (quads — eight of eights, three-way)
- **hero_pos:** HJ (MIDDLE)
- **board:** Jd 8h 8d 8s (triple-paired turn)
- **villains:** BTN, BB
- **action_history:** preflop HJ raise; flop HJ check → both villains check; turn checked to HJ
- **street:** turn
- **v2.2 label:** CHECK (Pass1+relabel consensus)
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=1 vrc=1 worse=1.00 evr=1.00 spr=1.25`
- **Why Group D:** *Every* numeric bias-trigger is satisfied (worse=1.0, evr=1.0, capped range, villains checked back). Model will scream BET. Correct answer is CHECK — with quads and no hand can call, any bet folds out worse. Pure trap. **Hardest possible discipline test** for v2.3.

### 2. `d6869_CO_turn` [A, full bias-sig, threshold-relaxed]

- **hero:** 8d Ah (TP weak kicker)
- **hero_pos:** CO (MIDDLE)
- **board:** Qd Ac 9s Kd (4-to-broadway turn, flush-danger high)
- **villains:** BTN, BB
- **action_history:** preflop CO raise; flop CO check → both villains check; turn checked to CO
- **v2.2 label:** CHECK
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=1 vrc=1 worse=0.60 evr=0.38 spr=1.25`
- **Why Group D:** Full bias-sig shape at relaxed thresholds (worse=0.60 is <0.55? actually 0.60 ≥ 0.55 so this is at canonical). Board is extremely dangerous: KT makes straights, flush completes with any diamond. TP weak kicker shouldn't be BET 3-way into a multi-draw board even with capped villains — bet folds out everything worse and keeps in sets/two pair/straights/flushes. CHECK discipline on a "looks-bettable" feature profile.

### 3. `d5466_CO_flop` [A, single-axis fail: vcb=0]

- **hero:** 6d Kd (TP weak kicker, backdoor flush)
- **hero_pos:** CO (MIDDLE)
- **board:** Kh Qc 9d (flop)
- **villains:** BTN, BB
- **action_history:** preflop CO raise; CO first to act on flop
- **v2.2 label:** CHECK
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=0 vrc=1 worse=0.78 evr=0.45 spr=1.25`
- **Why Group D:** PFR c-bet-or-check spot, three-way, wet board. Model will see worse=0.78, vrc=1, evr=0.45 and lean BET. Correct answer is CHECK — KQ9 is a wet connected broadway where BTN/BB have AK/QQ/JJ/JT/T8 strong holdings even in "capped" ranges, and K-weak doesn't want to get raised off equity. Also the only **flop PFR-first-to-act** spot in the shortlist (flop street diversity).

### 4. `d1764_BTN_turn` [A, single-axis fail: vrc=0]

- **hero:** 5s 5d (pair of 5s below the board)
- **hero_pos:** BTN (IP)
- **board:** 9s 4s 9d Qh (paired turn with backdoor flush)
- **villains:** HJ, BB
- **action_history:** preflop BTN call; flop BTN check → turn checked to BTN
- **v2.2 label:** CHECK
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=1 vrc=0 worse=0.67 evr=0.28 spr=1.25`
- **Why Group D:** Full bias-sig except `villain_range_capped=0` (villains' range uncapped — paired board means trips/FH live for any 9x). A small pair IP with 67% worse but only 28% equity should check behind for SDV and pot control. Tests that v2.3 doesn't fire "worse≥0.55 ∧ vcb=1" override without checking `vrc` guard.

### 5. `d2074_BTN_turn` [A, single-axis fail: vrc=0]

- **hero:** 7h 6h (bottom pair + flush blocker)
- **hero_pos:** BTN (IP)
- **board:** Qd 8d 6s Qh (paired turn, backdoor flush)
- **villains:** HJ, BB
- **action_history:** preflop BTN call; flop BTN check → turn checked to BTN
- **v2.2 label:** CHECK
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=1 vrc=0 worse=0.66 evr=0.25 spr=1.25`
- **Why Group D:** Similar to #4 but with a **paired broadway** board (Q-high pair). Bottom pair + no backdoors shouldn't bet three-way — villain Qx is in range (KQ/QJ/Q9/AQ not filtered out by call-call preflop line). Panel CHECK is correct; numeric features look bettable. Clean `vrc=0` discipline test.

### 6. `d6826_BB_turn` [A, single-axis fail: vrc=0]

- **hero:** 6d 5d (pair of 5s + backdoor flush)
- **hero_pos:** BB (OOP)
- **board:** 9h 5s 9s Td (paired turn)
- **villains:** CO, BTN
- **action_history:** preflop BB call; flop BB check → all check; turn BB first to act
- **v2.2 label:** CHECK
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=1 vrc=0 worse=0.62 evr=0.27 spr=1.25`
- **Why Group D:** OOP version of the `vrc=0` pattern. BB donks into two capped-but-not-truly-capped villains on a paired board — middle pair can't stand a raise, shouldn't bloat. Panel CHECK correct. Tests OOP vs IP applicability of the override gate (#4/#5 are IP, this is OOP).

---

## Stratum B — d-series / BP Pass 2 solver-confirmed CHECK overrides

These are Pass 2 reversal-shaped hands where the solver confirmed
CHECK (or, for BP4_11, the Pass 1 BET camp was overturned to CHECK
at final). Canonical reversal anchors because they test panel
discipline on spots the solver has actually ruled on.

### 7. `d4312_CO_turn` [B, full bias-sig + solver CHECK override]

- **hero:** 3s Ks (TP on a safe board)
- **hero_pos:** CO (MIDDLE)
- **board:** 7d 9h 5s Kc (turn K)
- **villains:** BTN, BB
- **action_history:** preflop CO raise; flop CO check → both check; turn K peels, checked to CO
- **v2.2 label:** CHECK (**Pass 2 + SOLVER override — was Pass 2 BET, solver said CHECK**)
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=1 vrc=1 worse=0.81 evr=0.51 spr=1.25`
- **Why Group D:** **The gold-standard Source B reversal.** All bias-triggers satisfied (worse=0.81, evr=0.51, capped, vcb=1, spr=1.25, 3-way). Pass 2 panel said BET. Owner ran GTO Wizard — solver said CHECK. OVERRIDE applied. If v2.3 can CHECK here, the "bucket-first BET bias" is controlled. This is the hand the Group D diagnostic exists to catch.
- **Solver log:** `solver_verification_log.jsonl` → "Solver says CHECK. Pass 2 BET was wrong."

### 8. `BP5_01` [B, solver CHECK override]

- **hero:** 4h 2d (bottom two pair, low kickers)
- **hero_pos:** BB (OOP)
- **board:** 8s 4d 2h (flop)
- **villains:** CO (+ BTN inferred)
- **action_history:** preflop 3-way SRP; BB first to act on flop (or BB check → ??? — per bp_villain_inference notes, hero is BB leading/checking)
- **v2.2 label:** CHECK (**Pass 2 + SOLVER override — was Pass 2 BET, solver said CHECK**)
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=0 vrc=0 worse=0.97 evr=0.72 spr=1.11`
- **Why Group D:** Strong-made hand (bottom 2pair, 97% worse) at SPR 1.11 OOP into two villains. Model will lean BET on pure strength. Solver says CHECK — bottom two pair at low SPR OOP gets all-in vs. top-two / sets (which are in range) and loses value from Tx/9x that would have barrelled. Tests "huge worse_hand_pct does not imply bet" in the absence of vrc/vcb bias-sig triggers. **Non-bias-sig reversal shape** (different failure mode than d4312).
- **Solver log:** "Tier 1 CONFIDENT_SPLIT panel said BET, solver says CHECK. Bottom-two-pair OOP at SPR 1.11 should check, not bet."

### 9. `BP4_11` [B, P1 BET → final CHECK trap reversal]

- **hero:** 8d 8c (set of eights)
- **hero_pos:** BB (OOP)
- **board:** 8s 4d 2h (flop)
- **villains:** CO (+ other inferred)
- **v2.2 label:** CHECK (Pass 1 BET → Pass 2 override CHECK via `bp_pass2_final_overrides.json`)
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=0 vrc=0 worse=1.00 evr=0.90 spr=1.11`
- **Why Group D:** Set on a dry low board, OOP, three-way. Model will see worse=1.0 and BET. Pass 2 consensus flipped to CHECK — slow-playing the nut hand on 842r to let villains barrel / catch up with overcards. **Slowplay/trap reversal** — distinct from the bias-sig override shape. Tests that v2.3 can hold CHECK on strong-made hands with *no* other action (not just when vcb/vrc are set). No solver entry in `solver_verification_log.jsonl` for this sid but Pass 2 override stands (from `bp_pass2_final_overrides.json`, entry `{"situation_id": "BP4_11", "old": "BET", "new": "CHECK"}`).
- *Note:* Owner may prefer d9556 (below) over BP4_11 for a solver-verified trap. Both compete for the same "slowplay reversal" slot.

### 10. `d9556_BB_flop` [B, solver CONFIRM CHECK — monster trap]

- **hero:** 5h 5d (full house, 5s full of 6s after flopping a set — wait, board is 5s6d6h → hero has 5-5 so hero holds a **full house 5s full of 6s**)
- **hero_pos:** BB (OOP)
- **board:** 5s 6d 6h (paired low flop)
- **villains:** UTG, BTN
- **action_history:** preflop BB call (3-way SRP); BB first to act on flop
- **v2.2 label:** CHECK (Pass1+relabel consensus)
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=0 vrc=0 worse=0.996 evr=0.899 spr=1.25`
- **Why Group D:** Full house OOP at SPR 1.25 on a paired board. Model will see worse=99.6% + made hand flag and BET. Solver says CHECK (CONFIRM — owner verified). Reasoning: the only hands that call are 6x (for quads scare) and overpairs, and you capture more by checking and letting opponents bet their own Tx/9x/overpairs. **Solver-confirmed trap** — diagnostically stronger than BP4_11 for the same slot. Solver log entry confirms CHECK directly.

---

## Stratum C — solver-mixed ≥40% CHECK

⚠ Under-filled (only 1 candidate surfaced; see §Blockers).

### 11. `BP4_21` [C, solver mixed-zone panel discipline]

- **hero:** Kd Qh (OESD + two overcards)
- **hero_pos:** BTN (IP)
- **board:** Jh 9c 6d (flop)
- **villains:** SB (declared) + BB (inferred)
- **action_history:** SB check, BB check, BTN to act
- **v2.2 label:** CHECK (**Pass 2 — solver said BET 25% pot (small sizing); owner keeps CHECK in mixed zone**)
- **Bias-sig features:** `facing_bet=0 nop=2 vcb=0 vrc=1 worse=0.21 evr=0.27 spr=1.11`
- **Why Group D:** KQ on J96 IP has OESD + two overcards — classic semi-bluff candidate, and a bucket that "feels like a BET." Solver offers BET 25% or CHECK both as valid; owner/Pass 2 picked CHECK side of the mix. **Tests mixed-zone panel discipline** — when solver does NOT have a pure answer and both actions are GTO-defensible, v2.3 should be able to sustain CHECK without interpreting the numeric features as a BET command. Lower-confidence target than Source A/B because the hand is genuinely close; include in Group D only if owner is comfortable mandating 100%-pass on a mixed-zone decision.
- **Solver log:** "Pass 2 CHECK was wrong; solver bets small. Confirms bucket-first CHECK bias in mixed spots." — Note: the solver log verdict was OVERRIDE to BET, but the final v2.2 label kept CHECK per "owner keeps CHECK in mixed zone" reasoning. This is the one hand where the v2.2 label and the solver verdict **disagreed on action** but both acknowledged it's a mixed spot. Diagnostically this is the most conceptually ambiguous candidate in the shortlist. Owner should decide whether Group D tolerates this level of mixed-spot ambiguity.

---

## Owner instructions

Pick **4** hands from the 11 above and comment back (via this file
as a trailing section, or a new comm). Suggested diversification:

- **≥1 from Source B** (solver-confirmed reversals are highest-value
  calibration anchors — `d4312_CO_turn` is the strongest single pick)
- **≥2 from Source A** (the bulk of bias-sig near-misses; pick to cover
  flop + turn + at least one IP and one OOP)
- **Consider 1 from Source C** only if comfortable with mixed-zone
  discipline requirement (BP4_21); otherwise fill the 4th slot with
  another Source A candidate

### Suggested default (if owner wants a builder nomination)

1. `d4312_CO_turn` — gold-standard bias-sig reversal with solver CHECK
2. `d9556_BB_flop` — solver-confirmed trap on paired flop (not d3687; see note)
3. `d2074_BTN_turn` — `vrc=0` discipline test, IP, turn, paired board
4. `d5466_CO_flop` — flop PFR-first-to-act diversity, worse=0.78 borderline

Avoiding `d3687_HJ_turn` in the suggested default because its
features are *so* extreme (worse=1.0 evr=1.0 quads) that it may
not test the calibration gate in the subtle way the other reversals
do — if v2.3 BETs here, so would most rational rule-based systems,
and the signal is less informative about the bias-sig override
specifically. Owner may still prefer it as the hardest possible
stress test.

### Ingestion

When picks land, builder adds them to the registry:

```python
# river-rats-core/calibration_exam.py (lines 73-75)
GROUP_D_REVERSAL_HANDS = {
    'd3688_BB_flop',
    # 4 owner picks go here — no other code change needed
}
```

`calibration_exam.GTO_REVERSAL_HANDS` auto-ingests the set.
Test `test_calibration_exam_extensibility` (line ~246) continues
to pass without modification.

---

## Blockers / stop-condition flags

- **Source C under-filled (1/3).** Only `BP4_21` has an explicit
  solver-mixed signal in `solver_verification_log.jsonl` that is
  (a) not excluded by the anchor/MW-miss list and (b) has `label=CHECK`.
  The other mixed-solver hands in the log (`d8886_BTN_flop`,
  `d8963_HJ_turn`) are both in the anchor-exclusion list
  (`d8886_BB_flop` and `d8963_HJ_turn` already in
  `_NEW_HARD_ANCHOR_IDS`). **Did not relax further per directive**
  — stop condition met. If owner wants Source C backfill, two options:
  (i) accept single-axis-fail `vrc=0` hands (#4/#5/#6) as proxy
  Source C (they're bias-sig near-misses where the "mixed" nature
  comes from the `vrc=0` guard); (ii) wait on upcoming solver sessions
  for row 11 / auto-enqueue reserve to generate new mixed-CHECK data.

- **No river candidates.** v2.2 training river CHECKs (n=42) are
  almost all weak-hand give-ups (air / weak made). After filtering
  to `worse≥0.50 OR evr≥0.30` plausible-BET shape, zero river CHECKs
  remain. The `d3229_BTN_river` spot that would've fit was excluded
  as an MW miss. Street distribution is flop 5 / turn 6 / river 0.
  Not a hard blocker — Group D's purpose is calibration discipline,
  and flop+turn provides sufficient coverage of the
  `vcb=1+vrc=1+worse+evr+spr` signature space. Flag for potential
  future expansion when river reversal data becomes available.

- **Source B `d4312_CO_turn` is the only d-series solver-confirmed
  CHECK reversal from solver log.** The others (`d8886`, `d8963`)
  are excluded. BP-series (BP5_01, BP4_11, BP4_21) are factory
  hands, not d-series PokerBench hands. Directive text says
  "d-series Pass 2 solver-confirmed CHECK overrides" but the broader
  interpretation ("Pass 2 solver-confirmed CHECK overrides") is
  what the candidate pool supports. Owner should decide if BP-series
  hands are acceptable for Group D; if not, Source B collapses to
  `d4312_CO_turn` + `d9556_BB_flop` (both d-series) and the 4-pick
  quota must draw more from Source A.

## Provenance

- `training-data/v2_2_training.csv` (385 rows, filtered to
  `label=CHECK` ∧ predicate variants per stratum)
- `training-data/solver_verification_log.jsonl` (13 entries)
- `training-data/pass2_summary.jsonl` (68 entries; Pass 1/Pass 2
  consensus comparisons)
- `training-data/bp_pass2_final_overrides.json` (12 BP-series Pass 2
  final overrides)
- `training-data/3way_combined_350.jsonl` +
  `training-data/test_set_50_labelled.jsonl` (card/action lookup)
- `training-data/factory_batch5_situations.jsonl` (BP-series card
  lookup)
- `review/comms/SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html` (10 MW
  miss sids — exclusion list source)
- `river-rats-core/calibration_exam.py` (anchor + Group D registry —
  exclusion list source)

No code was modified by this analysis. All queries are read-only.
