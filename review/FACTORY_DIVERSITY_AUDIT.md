# Factory Diversity Audit
**Date:** 9 April 2026
**Scope:** Batch 1 (generate_factory_situations.py, 151 situations) + Batch 2 (generate_factory_batch2.py, 261 situations)
**Purpose:** Establish current-state diversity baseline; derive concrete requirements for the new 151-situation RAISE batch.

---

## 1. Current State Audit

### 1.1 Board inventory

**Batch 1 — 16 unique boards across 151 situations**

| Board ID | Cards | Texture | Street | Hero pos | Hands |
|----------|-------|---------|--------|----------|-------|
| PA_Board1 | Ac 8d 3s | Rainbow, dry, A-high | Flop | BB (OOP) | 10 |
| PA_Board2 | 9d 6c 2h | Rainbow, low, connected | Flop | SB (OOP) | 10 |
| PA_Board3 | Jh 8h 4h | Monotone, wet | Flop | BB (OOP) | 10 |
| PA_Board4 | Qc Qd 7s | Paired, rainbow, dry | Flop | BB (OOP) | 10 |
| PA_Board5 | Ts 9d 5c 7h | Connected, rainbow | Turn | BB (OOP) | 10 |
| PA_Board6 | Ad 9d 4c | Two-tone, A-high | Flop | BB (OOP) | 10 |
| PA_Board7 | Jc 8c 5d 2h | Two-tone | Turn | SB (OOP) | 9 |
| PA_Board8 | Qc 8d 3s 6h 2c | Rainbow, dry | River | BB (OOP) | 10 |
| CALL_Board1 | Jd 8d 4c | Two-tone, medium | Flop | BB (OOP) | 9 |
| CALL_Board2 | Ks 9h 5d | Rainbow, dry | Flop | BTN (IP) | 9 |
| CALL_Board3 | Qh 7c 2s 5d | Rainbow, dry | Turn | BTN (IP) | 9 |
| CALL_Board4 | Ah 9c 3s 6d Tc | Rainbow, dry | River | BB (OOP) | 9 |
| CALL_Board5 | Kd Jc 6s | Rainbow, dry, high | Flop | BB (OOP) | 9 |
| CALL_Board6 | Ts 8h 3s | Two-tone, medium | Flop | BB (OOP) | 9 |
| CALL_Board7 | As Qd 5h | Rainbow, A-high | Flop | BTN (IP) | 9 |
| CALL_Board8 | 7h 7d 5s 9c Js | Paired, river | River | BTN (IP) | 9 |

**Batch 2 — 30 unique boards across 261 situations**

| Board group | Boards | Cards (abbreviated) | Texture | Street(s) |
|-------------|--------|---------------------|---------|-----------|
| SB (8 boards) | SB_B1 | Ks Jd 5s | Two-tone | Flop |
| | SB_B2 | Qh 8d 3h | Two-tone | Flop |
| | SB_B3 | Td 7d 2c | Two-tone | Flop |
| | SB_B4 | Jc 8s 4c 9c | Two-tone (monotone turn) | Turn |
| | SB_B5 | 7s 6s 5d | Two-tone, connected | Flop |
| | SB_B6 | 9h 6h 2d Kd | Two-tone turn | Turn |
| | SB_B7 | Ah 9c 4h Th | SPR-collapsed HU turn | Turn |
| | SB_B8 | Qs 8s 3d 5c Jh | Two-tone (bricked), river | River |
| FB (5 boards) | FB_B1 | Jh 7h 2c | Two-tone | Flop |
| | FB_B2 | Kc 9c 5d 3c | Monotone turn | Turn |
| | FB_B3 | Td 6d 2s 8h | Two-tone turn | Turn |
| | FB_B4 | As 7s 3c Ks 9d | Monotone turn, river | River |
| | FB_B5 | 8h 5h 2d Qh Jc | Monotone turn, river | River |
| OC (4 boards) | OC_B1 | 9c 6h 3d | Rainbow, low | Flop |
| | OC_B2 | 8d 5c 2h Jh | Two-tone turn | Turn |
| | OC_B3 | 7c 4d 2s 9h Tc | Rainbow, river | River |
| | OC_B4 | 6s 3h 2c Ts | Two-tone (minor) turn | Turn |
| TV (4 boards) | TV_B1 | Qc 8d 4s 2h | Rainbow | Turn |
| | TV_B2 | Jd 7c 3s Ah | Rainbow, scare card | Turn |
| | TV_B3 | Kd 9s 5h 2c Qh | Rainbow, river | River |
| | TV_B4 | Tc 7d 4c 8s | Two-tone | Turn |
| BD (9 boards) | BD_B1 | Ac Kd 7h | Rainbow, A-high | Flop |
| | BD_B2 | 5d 5c 9h Jd | Paired, turn | Turn |
| | BD_B3 | Td 8c 3h 6s | Connected, rainbow | Turn |
| | BD_B4 | Kh 9d 4c 2s Jc | Rainbow, river | River |
| | BD_B5 | 7h 4d 2c Qd 9s | Two-tone, river | River |
| | BD_B6 | 9c 7c 2d Kh | Two-tone turn | Turn |
| | BD_B7 | Jh 8d 5c Qc 4h | Two-tone, river | River |
| | BD_B8 | 6h 3d 2h 9c Ks | Two-tone, river | River |
| | BD_B9 | Qh 9h 4d Th | Monotone turn | Turn |

**Total across both batches: 46 unique boards, 412 situations.**

### 1.2 Situations per board

- Batch 1: 8–10 situations per board. Maximum concentration: 10 situations on PA_Board1–3 through PA_Board6, PA_Board8. All boards in Batch 1 are at or near the cap of 10.
- Batch 2: 8–9 situations per board. Maximum concentration: 9 situations per board (standard across SB, FB, OC, TV, BD groups).
- Combined maximum on any single board: 10 (multiple Batch 1 boards). No board appears in both batches (verified by checking card strings).

### 1.3 Board texture counts (both batches combined, 46 boards)

| Texture | Count | % of boards |
|---------|-------|-------------|
| Rainbow | 14 | 30% |
| Two-tone (flop) | 16 | 35% |
| Monotone (flop) | 1 | 2% |
| Monotone (achieved by turn) | 4 | 9% |
| Paired | 3 | 7% |
| Connected / high-straight-danger | 4 | 9% |
| River runouts (5-card) | 4 | 9% |

Methodology: boards were classified by the most aggressive texture feature at the decision point. A turn board that has three clubs is classified as monotone-by-turn, not two-tone-by-flop, because the feature extractor sees the full board at decision time.

**Monotone total: 5 boards out of 46 = 11% of the board pool.**
At 8–10 situations per board, monotone boards represent roughly 11% of all situations (45–50 situations from monotone boards out of 412 total). This is already above the real-world 3-way flop monotone rate (~5%) but within a defensible oversampling range given the training purpose.

**Two-tone total: 20 boards (43%). Rainbow total: 14 boards (30%).**

### 1.4 Position distribution (both batches)

| Hero position | Boards | % |
|--------------|--------|---|
| BB (OOP) | 22 | 48% |
| SB (OOP) | 8 | 17% |
| BTN (IP) | 12 | 26% |
| CO (IP) | 4 | 9% |

OOP situations: 65% of boards. IP situations: 35%.

Note: this OOP concentration is partly intentional (OOP decisions are harder and more training-relevant) but 65% is high enough to risk teaching a position-correlated bias — the model may associate certain feature values with OOP position and generalize incorrectly.

### 1.5 Street distribution (both batches)

| Street | Boards | % |
|--------|--------|---|
| Flop | 19 | 41% |
| Turn | 18 | 39% |
| River | 9 | 20% |

River is underrepresented relative to a balanced distribution (expected ~33%). Flop and turn are roughly balanced against each other.

### 1.6 SPR analysis

The JSONL confirms that all Batch 1 boards use effective_stack=100.0 with pot=90.0 at the decision point, producing SPR = 1.11 at every flop decision. This is a significant uniformity issue: almost all Batch 1 situations share the same SPR.

Batch 2 is more varied:
- SB_B7 (Ah 9c 4h Th): effective_stack=180, pot=350, to_call=140 — SPR approximately 0.5, representing a stack-off scenario
- FB_B4 (river): pot=300, to_call=100 — different structure
- Most Batch 2 boards still use effective_stack=100.0

The SPR=1.11 uniformity in Batch 1 is a known structural issue: 10 hands on the same board with the same SPR produce feature vectors that differ only in hero_cards and derived hand-strength features. The model sees 10 points on a line, not 10 distinct situations.

### 1.7 Facing-bet vs not-facing-bet distribution

- Batch 1, PA boards (8 boards): split approximately 50/50 — first 5 boards use to_call=0 (lead decision), boards 6–8 use to_call > 0 (facing bet)
- Batch 1, CALL boards (8 boards): all facing bet
- Batch 2: varied across groups — SB boards almost all facing bet, TV and BD boards mixed

---

## 2. Frequency Realism Assessment

### 2.1 Monotone boards

Real-world 3-way flops are monotone approximately 5% of the time. Both batches combined have 5 monotone-or-monotone-by-turn boards out of 46 = 11% of boards. At roughly 8–9 situations per board, this produces approximately 40–45 monotone situations from 412 total, or about 10–11% of the training set.

**Assessment:** Oversampled by approximately 2x relative to real frequency. This is a defensible oversampling for training purposes — flush draws and blocking are important concepts that need exposure. However, 10% monotone in the RAISE-focused new batch would be appropriate; going higher would distort the model's sense of how often flush dynamics arise.

### 2.2 SPR <= 1.5 situations

All 8 PA flop boards in Batch 1 use pot=90, effective_stack=100, producing SPR=1.11. That is 80 situations (8 boards × 10 hands) all at SPR=1.11. Of 151 Batch 1 situations, 80 have SPR <= 1.5. That is 53% of Batch 1.

Real-world 3-way pots with SPR <= 1.5 on the flop: rare. Standard 3bb open + 2 callers creates ~9bb pot with ~97bb effective stacks, giving SPR ~10.8 at flop. SPR <= 1.5 requires either a heavily raised preflop pot, a small effective stack, or a turn/river street where previous bets have shrunk the stack. SPR=1.11 at the flop in a standard call-call-call structure is nearly impossible in real games at 100bb effective.

**Assessment:** This is a significant frequency realism problem in Batch 1. Over half the situations use a SPR that almost never occurs in real 3-way flop spots at 100bb. The feature extractor will have seen spr=1.11 as a near-constant in Batch 1 training data, potentially learning it as a contextual anchor rather than a variable.

**Mechanism:** The PA boards set effective_stack=100 and pot=90, which means the feature extractor computes SPR as effective_stack / pot = 100/90 = 1.11. A realistic 3-way flop at 100bb should have pot ~9bb and effective stack ~97bb, giving SPR ~10.8. The factory boards are using pot=90 to represent 90 chips in an implicitly 100-chip stack game — but this creates a collapsed SPR that does not represent typical preflop-to-flop stack depth.

The Batch 2 boards inherited the same structure for most situations (pot=90, effective_stack=100) and have the same problem on flop boards. Turn boards (pot=180 or 200, effective_stack=100) produce SPR around 0.5–0.56, which is realistic for turn/river spots after multiple streets of betting, but again all cluster near the same value.

### 2.3 Sub-pattern frequency concerns

The PA boards in Batch 1 are designed as position-and-action sweeps (same board, 10 different hands). Every hand on a PA board produces nearly identical villain-facing features: same board_favour, same flush_danger, same straight_danger, same villain_top_pair_plus_pct, same villain_fold_equity_estimate. Only hero-side features vary. This means the model is seeing board-contextual features as constants within a board group, which is appropriate for within-group discrimination but provides no variation in the board-level feature dimensions across hands on the same board.

The concern is not that this approach is wrong (it deliberately tests hand-strength discrimination) but that the RAISE-focused new batch must avoid the same pattern. A RAISE batch where all 28 SP5 situations happen to share the same flush_danger and board_favour values will teach the model that SP5 = fixed context + varying hand strength, rather than teaching it that SP5 applies across a range of board contexts.

---

## 3. Concrete Diversity Requirements for the New 151-Situation Batch

All requirements are measurable by automated check or manual count at review time.

### R1. Board uniqueness

- Minimum 25 unique boards across the 151 situations.
- Maximum 8 situations per board (hard cap; prefer 6).
- No board from Batch 1 or Batch 2 may be reused. The existing 46 boards are excluded.
- Consequence of R1: with 25 boards and an average of 6 situations per board, the batch reaches 150 situations naturally. This also prevents the 10-hand-sweep structure that created the SPR=1.11 uniformity problem.

### R2. Board texture distribution

The 25+ boards must include:
- Rainbow: 6–8 boards (24–32%)
- Two-tone: 11–13 boards (44–52%)
- Monotone (flop): 1–2 boards (4–8%) — maximum 2; do not exceed 16 situations from monotone flop boards
- Paired: 2–3 boards (8–12%)
- Connected (straight_danger >= 0.40 at decision point): 3–4 boards (12–16%)
- River runouts contributing flush completion: 2–3 boards

Allowable deviation: +/- 1 board per category. If monotone exceeds 2 boards, the reviewer must document the training justification.

### R3. SPR distribution

No more than 20% of situations may share the same SPR value (within +/- 0.15 tolerance). The new batch must include situations across at least 4 distinct SPR tiers:
- SPR 1.0–2.0: at most 25% of situations (these are low-SPR commit spots; realistic for turns/rivers but not flops at standard stack depth)
- SPR 2.0–4.0: at least 30% of situations
- SPR 4.0–8.0: at least 25% of situations
- SPR 8.0+: at least 15% of situations

Implementation note: to achieve realistic flop SPRs, use effective_stack values proportional to the pot. A pot=90 flop with effective_stack=900 gives SPR=10. The factory can set effective_stack independently to model any realistic stack depth.

### R4. Street distribution

Across the 151 situations:
- Flop: 40–55 situations (27–36%)
- Turn: 50–65 situations (33–43%)
- River: 35–50 situations (23–33%)

River is deliberately increased relative to existing batches because SP8 (bluff raise) requires street=2 and contributes 16 situations. The new batch should also include river CALL counterexamples at higher rates than previous batches.

### R5. Position distribution

- OOP (BB, SB): 55–70 situations (36–46%)
- IP (BTN, CO, HJ): 80–95 situations (53–63%)

This reverses the OOP-heavy bias in existing batches. The new batch is RAISE-focused; most value raises and bluff raises are IP or in OOP check-raise scenarios. IP must be adequately represented.

### R6. Situations per sub-pattern per board

For each RAISE sub-pattern (SP1, SP2, SP3, SP5, SP7, SP8):
- Minimum 4 unique boards per sub-pattern
- Maximum 3 situations per board within a sub-pattern

This prevents a sub-pattern from concentrating in 2 boards with 10 situations each. SP5 (28 RAISE situations) should span at least 7 boards. SP7 (25 situations) should span at least 7 boards. SP8 (16 situations) should span at least 5 boards.

### R7. Villain-side feature variance within sub-patterns

For every sub-pattern of size N >= 8, the following villain-facing features must each vary by at least the specified range across situations in that sub-pattern:
- villain_fold_equity_estimate: range >= 0.20 (e.g., not all situations at 0.45–0.50)
- villain_top_pair_plus_pct: range >= 0.10
- board_favour: range >= 0.15 (values spanning both positive and negative if sub-pattern is intended to fire regardless of board-favour direction)
- flush_danger: range >= 0.10 for sub-patterns where flush is relevant; at least 2 distinct values

These ranges are measured as (max - min) across all situations in the sub-pattern.

---

## 4. Per-Sub-Pattern Variation Requirements

### SP1: Monster + wet board + low SPR (18 RAISE examples)

SP1 fires on flush_danger >= 0.40, SPR <= 2.5, hand_category >= 10. The risk is that all 18 situations end up on 2 or 3 boards with similar flush_danger values (~0.40–0.45) and near-identical SPR (~2.0). The model then learns "flush_danger=0.42, SPR=2.1 → RAISE" rather than learning the boundary.

Required variation within SP1:
- flush_danger must span at least 0.40–0.75 (include both moderate-flush and heavy-flush boards)
- SPR must span 1.0–2.5 (do not cluster at 2.0–2.2; include at least 3 situations at SPR <= 1.5 and at least 3 at SPR 2.0–2.5)
- hand_category: include both two_pair (value >= 10 but lower end) and set (higher end) — the model should learn both qualify
- Street: mix of flop and turn (SP1 should not be exclusively flop)
- Minimum 6 unique boards

### SP2: Monster + dry board + low SPR commit (10 RAISE examples)

SP2 fires on flush_danger <= 0.20, straight_danger <= 0.20, SPR <= 1.5, hero_range_percentile >= 0.90. With only 10 situations, clustering risk is high.

Required variation within SP2:
- At least 4 unique boards (2 flop, 2 turn — dry boards appear on both streets)
- hero_range_percentile must span 0.90–0.98 (do not use 0.90 for all 10; vary it to teach the boundary at 0.90, not the interior)
- SPR must span 0.8–1.5 (include stack-off scenarios near SPR=1.0 AND near-commit at 1.4)
- hand_category: at least 3 situations using two_pair (category 10–11) and at least 5 using set (12+) to show both qualify
- villain_fold_equity_estimate must vary — SP2 does not depend on fold equity, but varying it teaches the model that SP2 RAISE does not require fold equity

### SP3: Monster + OOP check-raise (12 RAISE examples)

SP3 fires OOP (is_ip == 0), villain_aggression_count <= 1, moderate SPR (2.0–3.5), no suppressors.

Required variation within SP3:
- At least 5 unique boards
- SPR must span 2.0–3.5 with at least 3 distinct SPR values
- Street: mix flop and turn (OOP check-raises occur on both)
- Board texture: include at least 2 rainbow, 2 two-tone, 1 paired board to show that SP3 fires across textures (flush_danger and straight_danger are not suppressors here — the monster is strong enough)
- hero_range_percentile must vary across 0.90–0.99 (monsters vary in absolute strength)

### SP5: Semi-bluff raises (28 RAISE examples)

SP5 is the highest-volume and most error-prone sub-pattern. The model sees 28 situations that must all have flush_draw_rank >= 12 AND flush_block_pct > 0. The risk: all 28 situations may cluster around similar flush_danger, flush_block_pct, and villain_fold_equity_estimate values, teaching the model a point rather than a boundary.

Required variation within SP5:
- Minimum 7 unique boards
- flush_danger must span at least 0.20–0.60 (nut flush draws appear on low-flush-danger boards too)
- flush_draw_rank must vary: at least 8 situations at rank 14 (Ace), at least 8 at rank 13 (King), at least 6 at rank 12 (Queen), at most 4 below rank 12 (v2 gate requires >= 12, but situations near the boundary at rank 12 teach the threshold)
- flush_block_pct must vary across 0.05–0.35 (partial blocking has a spectrum; do not cluster at 0.15–0.20)
- villain_fold_equity_estimate must span 0.45–0.70 (v2 gate requires >= 0.45; include situations at 0.45–0.50 to teach the boundary AND situations at 0.65–0.70 to show strong fold equity)
- villain_aggression_count must include both 0 and 1 across situations (the suppressor fires at >= 2; include both valid values)
- is_paired: all 28 must have is_paired == 0 per the gate — but board texture beyond paired/non-paired should vary (low-connectivity vs high-connectivity non-paired boards)
- Street: at least 10 situations on turn, at least 14 on flop (semi-bluff raises are more common on flop; turn semi-bluffs are fewer but important)
- Position: at least 10 OOP and 10 IP situations

### SP6: Semi-bluff suppressed CALL (13 CALL examples)

SP6 counterexamples must teach the model all failure modes of the SP5 gate. Current brief defines 4 failure classes:
1. fold_equity < 0.45 (fold-equity suppressor)
2. villain_aggression_count >= 2 (aggression suppressor)
3. is_paired == 1 (paired board)
4. draw_outs < 9 (gutshot only)
5. flush_draw_rank < 12 (non-nut draw, from Item 13)
6. flush_block_pct == 0 (no blocker, from Item 9 and Item 13)

Required variation within SP6:
- All 6 failure modes must appear (at least 2 situations per mode for modes 1–4; 3 situations for modes 5 and 6 combined, as these are the new v2 additions)
- Do not put all fold-equity-suppressed situations on the same board — use at least 3 unique boards for that failure mode
- The 13 situations must have distinct hero hand profiles: do not reuse the same hero_cards on different boards within SP6

### SP7: OOP thin value check-raise (25 RAISE examples)

SP7 fires on hero_range_percentile >= 0.75, is_ip == 0, villain_fold_equity_estimate >= 0.40, villain_aggression_count <= 1, flush_danger <= 0.35, straight_danger <= 0.35, num_callers_to_bet == 0. The risks: (a) all 25 situations may cluster at hero_range_percentile 0.75–0.80 (near the boundary), teaching a point at 0.75 rather than the interior; (b) all situations may use fold_equity near 0.40, again anchoring at the boundary.

Required variation within SP7:
- Minimum 7 unique boards
- hero_range_percentile must span 0.75–0.92, with at least 6 situations in each of these bands: 0.75–0.80 (boundary), 0.80–0.86 (interior), 0.86–0.92 (strong non-monster)
- villain_fold_equity_estimate must span 0.40–0.65, with at least 5 situations at 0.40–0.50 (boundary) and at least 5 at 0.55–0.65 (clear interior)
- flush_danger must vary 0.05–0.35 (the suppressor fires at > 0.35; situations across this range teach the boundary)
- straight_danger must vary 0.05–0.35 (same reason)
- SPR must span 2.0–3.5 (moderate SPR is required; vary it)
- Street: mix of flop and turn — thin value check-raises occur more on turns but flop examples are needed too; target 10 flop, 15 turn
- villain_aggression_count must include both 0 and 1 (not all situations at count=0)

SP7 CALL counterexamples needed in other sub-patterns: the brief places IP thin value in CALL territory (is_ip == 1, hero_range_percentile 0.75–0.92). At least 3 of the SP10 situations should use this configuration as CALL, so the model sees the IP vs OOP distinction explicitly.

### SP8: Bottom of range bluff raise (16 RAISE examples)

SP8 requires street == 2 (river), hero_range_percentile <= 0.20, villain_fold_equity_estimate >= 0.50, villain_top_pair_plus_pct <= 0.35, num_callers_to_bet == 0, villain_aggression_count == 0.

Required variation within SP8:
- Minimum 5 unique river boards — do not use the same river runout for more than 3 situations
- hero_range_percentile must span 0.02–0.20, with at least 4 situations at 0.02–0.08 (true air) and at least 4 at 0.12–0.20 (bricked draws with minimal showdown value)
- villain_fold_equity_estimate must span 0.50–0.72 (boundary and interior)
- villain_top_pair_plus_pct must span 0.10–0.35 (the suppressor fires at > 0.35; include boundary values)
- Hero hand types must vary: at least 4 situations using bricked flush draw (has_flush_draw was 1 on earlier street), at least 4 using bricked straight draw, at least 4 using complete air (no draw ever existed). Do not build all 16 situations around the same hand type.
- Board texture: at least 2 monotone-or-two-tone runouts (where flush draws were plausible), at least 2 rainbow runouts (where the bluff raise is pure position/fold-equity based)
- villain_aggression_count == 0 is required for all 16 — this is a structural constraint, not a variation opportunity

### SP9: Flat spots CALL (10 CALL examples)

SP9 fires when num_callers_to_bet >= 1 (sandwiched), or board_favour <= -0.30 with villain_range_capped == 0, or villain_aggression_count >= 2.

Required variation:
- All three SP9 triggers must appear (at least 3 situations per trigger)
- board_favour must span -0.30 to -0.60 for the board-favour trigger (not all at exactly -0.30)
- villain_aggression_count: use 2 and 3 for the aggression trigger (not all at count=2)

### SP4: Monster suppressors CALL (6 CALL examples)

SP4 fires when is_monster == 1 but a Step 2 suppressor fires. Brief defines 4 suppressors: S2 (paired board + flush danger), S3 (multi-street aggressor), S4 (high SPR IP, spr >= 6.0), S5 (callers-to-bet + percentile < 0.92).

Required variation:
- All 4 suppressors must appear at least once
- The S4 suppressor must use spr >= 6.0 (not 4.0) — this was a v2 correction; verify all S4 situations
- Recommend 2 situations for S3 and S4 (the most common suppressors in real games) and 1 each for S2 and S5

### SP10: Middle range CALL fill (13 CALL examples)

SP10 must teach the model that hero_range_percentile 0.40–0.80 with limited draw equity = CALL, not RAISE. The Item 10 additions (5 new situations) specifically target 0.70–0.80 with draw_outs 6–8.

Required variation:
- hero_range_percentile must span 0.40–0.80 in at least 4 distinct bands: 0.40–0.55, 0.55–0.65, 0.65–0.75, 0.75–0.80 (at least 3 situations per band across the 13 total)
- draw_outs must span 0–8 (include situations with draw_outs == 0, 4–6, and 6–8)
- At least 3 situations where is_ip == 1 and hero_range_percentile >= 0.75 — these explicitly teach the IP vs OOP distinction that SP7 depends on
- Board texture must vary: at least 3 boards with flush_danger 0.20–0.50 (to show that moderate danger does not automatically produce a RAISE)

---

## 5. Concerns About Existing Batches

### Concern 1: SPR uniformity in Batch 1 (high severity)

As documented in Section 1.6, 80 of 151 Batch 1 situations have SPR=1.11 (all PA flop boards). This is both unrealistic (SPR=1.11 at 100bb depth almost never occurs in real 3-way flop spots) and structurally problematic (the model cannot learn SPR as a discriminating feature from Batch 1 data). Batch 2 is somewhat better but still clusters around SPR=0.5 (turn boards) and SPR=1.11 (flop boards).

Recommended action: when the training set is assembled, apply class-weight correction or feature-range normalization to prevent SPR being treated as a near-constant. This does not require regenerating existing situations, but the new batch must actively counter the uniformity by spanning the full 1.0–10.0 range.

### Concern 2: OOP concentration (medium severity)

65% of existing boards have OOP heroes. This means the model has seen OOP as the dominant context for training. For a RAISE model, this matters because raise decisions look different OOP (check-raise) vs IP (value-raise after betting). If SP5 semi-bluff situations are also predominantly OOP, the model may associate semi-bluff raises specifically with OOP context.

The new batch should run at least 55% IP (see R5). Within SP5, specifically target 10–12 IP situations and 16–18 OOP situations to avoid the OOP anchor.

### Concern 3: Villain-facing feature constants within board groups (medium severity)

All 10 hands on PA_Board1 share identical villain_fold_equity_estimate (0.703), identical board_favour (0.1387), identical villain_top_pair_plus_pct (0.1613). These are board-level features; they cannot vary within the same board configuration. This is architecturally unavoidable but means the model learns hero-hand discrimination within a fixed board context rather than discriminating across board contexts.

Within a sub-pattern like SP5 (28 situations), if the designer uses only 3–4 boards, villain-facing features will only take 3–4 distinct values across 28 situations. The per-sub-pattern board minimum in R6 (minimum 7 boards for SP5) directly addresses this.

### Concern 4: Batch 2 SB group — HU board included (low-to-medium severity)

SB_Board7 (Ah 9c 4h Th) is a HU board with villain_positions=['CO'] (single opponent). This creates a structural discontinuity: all other SB boards are 3-way. The feature extractor produces different num_opponents, villain range estimates, and equity computations for HU vs 3-way. Including this board in training creates implicit context variance that may be confounded with the semi-bluff decisions being trained. Not a reason to remove it — HU turn semi-bluff decisions are real — but the new batch should be aware that mixing HU and 3-way boards introduces a context variable. If the new batch includes HU boards, label them clearly in the design document.

### Concern 5: Paired boards underrepresented (low severity)

Only 3 of 46 boards (6.5%) are paired. Real 3-way flops include a paired board (one rank appears twice on the 3-card flop) approximately 17% of the time. The existing factory undersamples paired boards by roughly 2.5x. This matters because paired boards suppress SP5 (is_paired == 1 → CALL) and affect SP1 differently than unpaired boards. The new batch should target 3–4 paired boards (12–16% of the 25+ required boards), both to improve realism and to supply more SP4 and SP6 suppressor examples.

---

## Reviewer Checklist (for the new 151-situation batch)

The following checks must be documented in the review before the batch can be approved:

1. Count unique boards. Must be >= 25. None may appear in the existing 46-board list.
2. Count situations per board. No board may have > 8 situations.
3. Count monotone boards (flop-level). Must be <= 2.
4. Compute SPR distribution. At least 4 distinct tiers must be populated; no tier above 25% of total situations.
5. Count OOP vs IP heroes. OOP must be <= 70 situations.
6. Count street distribution. River must be >= 35 situations.
7. For SP5: count unique boards. Must be >= 7.
8. For SP5: compute range of flush_draw_rank, flush_block_pct, villain_fold_equity_estimate. Each must meet minimums in Section 4.
9. For SP7: compute range of hero_range_percentile, villain_fold_equity_estimate. Each must meet minimums in Section 4.
10. For SP8: count unique river boards. Must be >= 5. Count situations at street != 2 — must be 0.
11. For SP4: verify all S4 situations have spr >= 6.0.
12. For SP10: count situations with is_ip == 1 and hero_range_percentile >= 0.75. Must be >= 3.
13. For every sub-pattern of size >= 8: compute villain_fold_equity_estimate range. Must be >= 0.20.
14. Confirm no hero_cards duplicate within a sub-pattern on the same board.
