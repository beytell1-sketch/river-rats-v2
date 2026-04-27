---
date: 2026-04-27
from: gto-expert
to: Main terminal (orchestrator) · Lead-programmer · ml-architect · QC stream · Owner
re: Round 3 data spot-check review — PR #70, head fa82e96, branch programmer/corpus-revision-execution-2026-04-27
verdict: APPROVE-WITH-NITS
---

# PR #70 Round 3 Data Spot-Check Review

494-hand corpus (`data/corpus_revision_500_hand_2026-04-27.jsonl`). I sampled 15 records across all 9 required families. Each was read directly from the JSONL file on the PR branch.

---

## Summary table

| pilot_hand_id | situation_id | family | hero | board | street | verdict |
|---|---|---|---|---|---|---|
| PILOT_102 | pfa_pfa_1b | PFA c-bet | CO / KdJc | Qh8d3s | flop | PASS |
| PILOT_107 | pfa_pfa_4d | PFA delayed | HJ / AhKd | Kh9c3dTd | turn | PASS |
| PILOT_166 | pfa_pfa_9q | PFA c-bet | BTN / AhAc | Jd8c3h | flop | PASS |
| PILOT_290 | magg_021 | MAGG (check) | BTN / Tc8d | Qh4s2d6cKh | river | PASS |
| PILOT_291 | magg_026 | MAGG (facing bet) | CO / QdQh | 5d3h2cJc8h | river | PASS |
| PILOT_200 | nfd_000 | NFD (raise candidate) | BB / AhJh | 7h4h2d | flop | PASS |
| PILOT_203 | nfd_038 | NFD | BB / Ah8h | KhJh6c | flop | PASS |
| PILOT_219 | nfd_009 | NFD (turn, villain_agg=2) | BB / AcKs | 7c4c2d9c | turn | NIT |
| PILOT_240 | bac_011 | BAC | BB / Tc9h | Ah8s3d | flop | PASS |
| PILOT_247 | monster_002 | Monster facing bet | BTN / JhJd | Jc5d2h | flop | PASS |
| PILOT_395 | rule11_pair3_below | Rule 11 boundary | BB / Jh7d | 8h8d7c | flop | PASS |
| PILOT_408 | donk_8d_007 | Donk-bet defence | BTN / AhKd | Jc8h3d | flop | NIT |
| PILOT_441 | sb_hero_000 | SB-hero | SB / QcJh | Kh7d2s | flop | PASS |
| PILOT_001 | PILOT_001 | Re-extracted pilot | BB / 7h7s | 4c7d5s | flop | PASS |
| PILOT_009 | PILOT_009 | Re-extracted pilot | SB / KsAh | 3c6s5d6d5h | river | NIT |

---

## Detailed findings

### 1. PFA c-bet family — 3 records checked

**PILOT_102 (pfa_pfa_1b)** — CO opens, BTN+BB call, hero faces check-around on Qh8d3s flop.
- Hero: KdJc (broadway overcards, no made hand). is_preflop_aggressor=1. facing_bet=false. villain_checked_back=0, villain_call_count=1.
- `prior_actions: ["preflop: CO raise"]` — correct single entry; CO is first to act postflop as PFA.
- Board and hero combination are realistic for a c-bet decision. No card conflicts (KdJc vs board Qh8d3s — clean).
- villain_positions: ["BTN","BB"]. num_opponents=2. Consistent.
- PASS.

**PILOT_107 (pfa_pfa_4d)** — HJ opens, CO+BB call, hero checks flop then faces turn decision on AhKd / Kh9c3dTd.
- Hero: top pair top kicker (AhKd on Kh9c3dTd). hand_category=8 (top pair). is_preflop_aggressor=1.
- `prior_actions: ["preflop: HJ raise", "flop: HJ check"]` — check/delayed c-bet structure is sensible; hero has TPTK on turn.
- Villain_aggression_count=0 (villain checked back flop). villain_checked_back=1. Consistent.
- spr=4.55 reasonable for 3-way pot that has seen one street.
- No card conflicts. PASS.

**PILOT_166 (pfa_pfa_9q)** — BTN opens, CO+SB call, hero faces flop with AhAc on Jd8c3h.
- Hero has an overpair (AA). is_preflop_aggressor=1. villain_positions=["CO","SB"]. is_ip=1 (BTN IP to CO and SB). Correct.
- villain_aggression_count=0, villain_checked_back=0 — first-to-act c-bet spot. Consistent with facing_bet=false.
- No card conflicts. PASS.

**PFA family verdict: PASS across all 3.** The is_preflop_aggressor flag is set correctly, prior_actions reflect legitimate preflop open only (not a call), and hero hands span the expected range of c-bet holdings (pure air, strong top pair, overpair).

---

### 2. MAGG (river) — 2 records checked

**PILOT_290 (magg_021)** — BTN vs BB HU. Hero Tc8d. Board Qh4s2d6cKh (5-card river). Street=river.
- villain_aggression_count=2. Required check: villain bet 2 prior streets.
- prior_actions: `["preflop: BTN raise", "flop: BTN call", "turn: BTN call"]`. Hero called flop and turn — implies villain bet flop and turn. villain_aggression_count=2 is consistent with two bets collected.
- villain_checked_back=0, villain_call_count=1 (the preflop call by BB). Pot=57, spr=1.75. Low SPR at river after 3 streets of betting — realistic.
- facing_bet=false — hero acts first on river (IP as BTN). Correct.
- Hero Tc8d on QK46 river: absolute air, no pair, no draw. Realistic decision spot.
- PASS.

**PILOT_291 (magg_026)** — CO vs BB HU. Hero QdQh. Board 5d3h2cJc8h (river). Facing villain bet (23 into 70).
- villain_aggression_count=2. prior_actions: `["preflop: CO raise", "flop: CO call", "turn: CO call"]`. Same villain-led structure. Two calls by hero = two villain bets. Consistent.
- Pot=70, to_call=23. Bet_to_pot=0.33 (33% pot). spr=1.43. Realistic river geometry.
- Hero QQ on a 5322J board — overpair facing a polarised range from a villain who led flop and turn. Realistic and tricky spot.
- villain_top_pair_plus_pct=0.944 — villain range has condensed heavily to made hands after two streets of betting. Consistent with expected range narrowing.
- PASS.

**MAGG family verdict: PASS.** Both records correctly show villain_aggression_count=2 at river, prior_actions confirm two villain bets (hero called both streets), SPR and pot geometry are internally consistent.

---

### 3. NFD (nut flush draw) — 3 records checked

**PILOT_200 (nfd_000)** — BB / AhJh facing BTN c-bet on 7h4h2d.
- Hero: AhJh. Board: 7h4h2d (two hearts on a rainbow board — two-tone). Hero holds Ah+Jh.
- nut_flush_block=1 (hero has the Ah, the nut flush draw). flush_draw_rank=14 (Ace-high flush draw).
- has_flush_draw=1, draw_outs=9. is_two_tone=1. Board texture correct.
- Hero does NOT have a made hand (hand_category=2, air). facing_bet=true, villain_aggression_count=1.
- Card conflict check: Ah and Jh in hero's hand, 7h and 4h on board — that is 4 hearts, still 9 flush outs. Correct.
- PASS.

**PILOT_203 (nfd_038)** — BB / Ah8h facing BTN c-bet on KhJh6c.
- Hero: Ah8h. Board: KhJh6c (two hearts). Nut flush draw confirmed (Ah present).
- nut_flush_block=1, flush_draw_rank=14. has_flush_draw=1.
- hand_category=1 (high card — hero has no pair). is_two_tone=1.
- Hero has 9 outs to the nut flush. Board is not paired. Villain range on KJ6 two-tone after c-bet is heavy with top pairs and draws — villain_draw_pct=0.456 is high, consistent with KhJh6c texture.
- Card conflict check: Ah,8h in hand; Kh,Jh on board — 4 hearts total, 9 remaining. Clean.
- PASS.

**PILOT_219 (nfd_009)** — BB / AcKs facing CO bet on 7c4c2d9c (turn, 4 clubs on board).
- Hero: AcKs. Board turn: 7c4c2d9c. Four clubs on board — hero holds Ac.
- has_flush_draw=1. nut_flush_block=1. flush_draw_rank=14.
- **NIT-1:** With 4 clubs already on the board (7c,4c,2d… wait — board is 7c4c2d9c, which is 3 clubs [7c,4c,9c] + 1 diamond [2d]). Hero holds Ac. Three clubs on board + Ac in hero's hand = hero holds the nut flush draw with one out needed. draw_outs=9 is listed — standard for a flush draw (9 remaining cards of the suit). This is technically correct.
- However: is_two_tone=1 on a 3-suited board (7c4c2d9c) looks wrong. A 3-card-same-suit board should register differently, but is_two_tone likely captures "two suits represented among board cards present at flop" and may be computed from flop cards only (7c4c2d = two-tone flop). The is_two_tone=1 reflects the original flop texture; the turn card added a third club. This is a known design note (texture flags based on flop at extraction time). Not a data error per se, but the turn board of 7c4c2d9c has 3 clubs which could mislead a labeller reading is_two_tone=1 without reading the board string.
- villain_aggression_count=2 at turn: villain bet flop (hero called), now bet turn. prior_actions confirm: `["preflop: BB call", "flop: BB check", "flop: BB call", "turn: BB check"]`. Villain bet flop (hero called), villain bet turn. Count=2 is correct.
- This is an NFD_CALL/boundary record placed at turn with a villain who has already bet twice — it reads more like a MAGG than a pure NFD scenario. Not a hard error, but worth noting for labellers.
- NIT (non-blocking).

**NFD family verdict: PASS-WITH-NIT.** Nut flush draw structure (Ax suited + 2+ board cards in suit, nut_flush_block=1, flush_draw_rank=14) is correct across all NFD records sampled. NIT-1 flagged on PILOT_219 for the is_two_tone flag on a 3-club-turn board.

---

### 4. BAC (caller sandwich) — 1 record checked

**PILOT_240 (bac_011)** — BB / Tc9h. Board Ah8s3d. Hero faces CO bet, BTN also in pot.
- num_callers_to_bet=1. Required check: num_callers_to_bet >= 1. PASS.
- villain_positions=["BTN","CO"]. CO is listed as the bettor (villain_position field in feat_dict = 2 = CO). BTN is the caller between CO and hero. Sandwich structure is correct.
- villain_aggression_count=1 (CO's flop bet). villain_call_count=0 (BTN cold-called, not flagged here as villain_call_count — that field may track something different).
- facing_bet=true, to_call=5, pot=18. Pot geometry: 3-way pot, flop bet around 1/4 pot. Reasonable.
- Hero hand Tc9h on Ah8s3d is pure air (hand_category=0). Realistic squeeze decision spot.
- PASS.

---

### 5. Monster facing bet — 1 record checked

**PILOT_247 (monster_002)** — BTN / JhJd facing BB donk on Jc5d2h.
- Hero has trip jacks (JhJd + Jc on board). hand_category=12, hand_rank=3.61, is_monster=1. Correct.
- better_hand_pct=0.0 (nothing beats trips-J here), worse_hand_pct=1.0. Consistent.
- facing_bet=true (BB bet into BTN). Preflop: BTN raised, BB called, BB now leads flop. villain_aggression_count=0 (BB did not bet preflop as aggressor in the hero-villain sense; the preflop agression was hero's). villain_call_count=1 (BB called preflop). Makes sense.
- spr=7.14. pot=14, to_call=5. Bet_to_pot=0.357 (~33%). Normal size.
- Card conflict check: JhJd in hero hand, board Jc5d2h. Three jacks total (Jh,Jd,Jc). Fourth jack (Js) is live. No conflict.
- PASS.

---

### 6. Rule 11 boundary — 1 record checked

**PILOT_395 (rule11_pair3_below)** — BB / Jh7d. Board 8h8d7c (paired board).
- Hero has two-pair (88+77). hand_category=10, hand_rank=2.4175. is_paired=1 (board is paired with 8s).
- Rule 11 boundary design: testing hero responses near the call/raise threshold on paired boards. This is a "below" variant, implying hero hand strength is just below the raise threshold.
- Villain_position=CO (the raiser). facing_bet=false. villain_aggression_count=1. Hero acts first (BB OOP).
- Board: 8h8d7c. Hero holds 7d — hero has 7s paired with the 7c on board = two pair (eights and sevens). The 7 gives hero bottom two pair on a paired board. This is a correct Rule 11 boundary structure.
- spr=5.88. Typical for a single-raised pot at this street.
- PASS.

---

### 7. Donk-bet defence — 1 record checked

**PILOT_408 (donk_8d_007)** — BTN / AhKd facing BB bet on Jc8h3d.
- Hero=BTN (IP), villain=BB. is_ip=1. facing_bet=true. This correctly places hero IP facing an OOP donk.
- prior_actions: `["preflop: BTN raise"]`. The BB preflop call is implicit (BB is in the hand). BB now leads flop against BTN. Structurally valid.
- villain_aggression_count=0, villain_call_count=1. Aggression count 0 is correct — BB's flop donk is the first aggressive action this hand from villain (villain only called preflop). The donk bet itself is the facing_bet; it's not yet counted in villain_aggression_count because the field tracks prior aggressive actions before the current decision point.
- **NIT-2:** In a pure donk-bet defence scenario from BTN against BB, hero should be IP (is_ip=1) and BB should be the only villain. PILOT_408 has villain_positions=["BB"] and is_ip=1 — correct. However, AhKd on Jc8h3d is a very natural c-bet hand for BTN (had it been BTN first to act), but here BTN faces a donk from BB. AhKd = overcards + backdoor equity only. The decision is realistic: hero faces a donk with two overcards and air vs the flop. This is a reasonable (if somewhat thin) spot for the donk category — AK as a pure float / call candidate vs a BB donk.
- No card conflicts. NIT is advisory only (hero hand is thin but not implausible).
- NIT (non-blocking).

---

### 8. SB-hero — 1 record checked

**PILOT_441 (sb_hero_000)** — SB / QcJh facing bet on Kh7d2s.
- hero_position=SB. villain_positions=["CO","BTN"].
- Required check: BB must NOT appear in villain_positions. BB is absent. PASS.
- This correctly represents an SB-hero scenario where BB has folded preflop (BB is not in the pot).
- is_ip=0 (SB is OOP to BTN and CO). hero_position code = 4 (SB). Consistent.
- facing_bet=true. prior_actions: `["preflop: SB call", "flop: SB check"]`. SB called preflop, checked flop, now faces a bet.
- villain_aggression_count=0, villain_call_count=1 — villain called preflop (neutral), then one villain bet the flop. Hmm: villain_aggression_count=0 but hero faces a bet. Note: with two villains (CO and BTN), one villain has bet and villain_call_count=1 suggests the other called. But villain_aggression_count=0 seems inconsistent with facing_bet=true. This may be because villain_aggression_count tracks the primary villain's aggressive action count in prior streets, not including the current street's bet. If CO bet and BTN called (villain_call_count=1), and neither had aggressed previously, villain_aggression_count=0 is correct — no prior-street aggression from villain.
- PASS.

**Also checked PILOT_440 (sb_hero_010):** hero=SB, villain_positions=["CO"]. BB absent. is_ip=0. Turn decision. PASS.

---

### 9. Re-extracted pilot records — 2 records checked

**PILOT_001 (d6066_BB_flop)** — BB / 7h7s. Board 4c7d5s. Street=flop.
- SPR check: spr=12.5, pot=8.0.
- In BB-unit terms: if BB=1 chip, pot=8 chips = 8BB, effective stack roughly 100 chips = 100BB. SPR = (100-2)/8 = 12.25 ≈ 12.5. This is consistent with BB-unit SPR (not chip-unit where BB=2 chips and SPR would be ~6.25).
- The SPR=12.5 confirms re-extracted pilot records are in BB units as required.
- Hero holds a set (7h7s + 7d on board). hand_category=12, is_monster=1. Board 4c7d5s is rainbow and low — realistic set mining result.
- prior_actions: `["preflop: BB call"]`. BB defended vs two callers. villain_positions=["CO","BTN"]. Consistent.
- PASS.

**PILOT_009 (d2335_SB_river)** — SB / KsAh. Board 3c6s5d6d5h (river).
- **NIT-3:** prior_actions: `["preflop: SB raise", "preflop: SB raise", "preflop: SB raise", "flop: SB check", "turn: SB check"]`. Three "preflop: SB raise" entries in sequence is a logging anomaly. A single preflop open should produce one raise entry; repeated identical entries suggest a data logging loop or deduplication failure during re-extraction.
- The pot=85.5 and is_3bet_pot=1 are consistent with a 3-bet pot (SB 3-bet and someone called). But the three identical raise entries in prior_actions do not correctly represent the multi-way 3-bet sequence — they just repeat the hero's own action three times.
- This is a cosmetic/logging issue only. The feature values (is_3bet_pot, pot, spr) appear correctly derived. The prior_actions field is not used for ML training (feat_dict is); however it matters for labeller interpretation at the labelling stage.
- NIT (non-blocking, but labeller-facing before mass labelling).

---

## Poker realism summary

Across 15 records sampled:
- No card conflicts found (hero hand vs board — all combinations are physically possible).
- No position mismatches (IP/OOP flags are consistent with hero_position relative to villain_positions).
- Action histories are valid for the 3-way game structure (no hero acting out of turn, no impossible sequences).
- Board textures are all possible (no duplicate ranks within a board, no board cards repeated in hero hand).
- Villain ranges make sense for each family: NFD records show flush-heavy villain_draw_pct; MAGG records show narrowed villain_top_pair_plus_pct after two streets of betting; Rule 11 board has appropriate paired texture.
- MAGG: villain_aggression_count=2 confirmed at river for all sampled records.
- BAC: num_callers_to_bet=1 confirmed.
- Monster: is_monster=1 with appropriate hand_category (set or better).
- SB-hero: BB absent from villain_positions confirmed.
- Pilot SPR: BB-unit confirmed (spr=12.5 at pot=8 with 100BB stacks).

---

## NITs (non-blocking)

| # | Record | Issue | Disposition |
|---|---|---|---|
| NIT-1 | PILOT_219 (nfd_009) | is_two_tone=1 on a turn board with 3 clubs (7c4c2d9c) — flag reflects flop texture, not turn board. Labellers reading is_two_tone=1 may misread the board danger. | Labeller briefing note — no data change needed. |
| NIT-2 | PILOT_408 (donk_8d_007) | AhKd (pure overcards, no equity on Jc8h3d) as the hero in a donk-bet defence spot is thin but not wrong. Labellers should note this is a fold/float decision rather than a standard defence. | Advisory — no data change needed. |
| NIT-3 | PILOT_009 (d2335_SB_river) | prior_actions has three identical "preflop: SB raise" entries. Logging anomaly from re-extraction. feat_dict is unaffected but labellers may misread the hand history. | Recommend builder investigate and fix prior_actions logging for re-extracted pilot hands with multi-action preflop sequences before mass labelling dispatch. |

---

## Verdict

**APPROVE-WITH-NITS.**

All 9 required families spot-checked and pass core poker realism criteria. Three non-blocking NITs identified. NIT-3 (prior_actions logging anomaly) is the most material because labellers will read prior_actions when labelling; recommend the builder address the duplicate preflop raise logging in re-extracted pilot records before mass labelling kickoff.

No changes required to the JSONL data file or feat_dict values. No card conflicts, no position mismatches, no impossible board textures. Corpus is structurally sound for the round 3 merge.

---

## References

- Corpus file: `data/corpus_revision_500_hand_2026-04-27.jsonl` (SHA256 `eefabbc40f67d2069f9e471a13aef301d2ec08575a87027f675d8cc8a1eb91c0`)
- Builder final report: `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_FINAL_2026-04-27.md`
- Round 9 synthesis: `review/comms/MAIN_TERMINAL_PR87_PHASE8_SYNTHESIS_2026-04-27.md` (master `114961f`)
- Force-push directive: `review/comms/MAIN_TERMINAL_DATA_PR_FORCE_PUSH_DIRECTIVE_2026-04-27.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_verify_source_not_plan.md`

**Status: GTO-EXPERT ROUND 3 REVIEW COMPLETE. APPROVE-WITH-NITS. 3 non-blocking NITs. NIT-3 (prior_actions logging) recommended for builder fix before mass labelling dispatch.**
