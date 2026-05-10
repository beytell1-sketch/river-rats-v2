---
date: 2026-05-10
from: Main terminal (orchestrator; owner-delegated adjudication per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`)
to: LEAD-PROGRAMMER (builder; data-layer applicator) · QC stream (post-adjudication audit)
re: (a) 44 owner-arbs adjudicated by orchestrator per owner-delegated quality picks + (b) builder applies adjudications to consensus.jsonl + (c) solver-verification queue updated to 48 spots; HOLD-with-accepted-risk per owner; verification + retrain-if-needed is recovery + (d) post-data-layer-fix authorize 1.5-D.4 design/prep
status: DISPATCH — fire now
---

# (a) 44 owner-arbs adjudication — orchestrator picks per owner delegation

Owner direction (verbatim, 2026-05-10 21:13 SAST): "its too difficult, flag for solver verification. my solver is offline, pick best option, we can verify with sovler later and retrain if necesary"

Per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` (NEW memory): orchestrator picks each spot per quality/GTO theory; ALL spots enter solver-verification queue; retrain-if-needed is the accepted recovery path.

## Per-anchor adjudications (11 unique decisions covering 44 spots)

### 1. HU-5.4 GROUP (22 spots: HU-5.4-LK-01 .. HU-5.4-LK-22; 21 IDENTICAL Sonnet 3-CHECK / 2-BET; Opus BET on 21 of 22)

**Spot:** Th8h. Eff 100bb. BTN opens 2.5bb, BB (hero) calls. Pot 5.5bb. FLOP 9h7c{xh} two-tone hearts (variations of 3rd card). BB OOP, no bet to face (donk-lead vs check). Hero combo-draw FD + open-ender (~13-15 outs).

**Adjudication: CHECK.** Reasoning: Standard pot-control OOP without information advantage. Sonnet majority CHECK; Opus BET likely overestimates donk-lead frequency in HU OOP. GTO mixes here, but check-based strategy is the lower-variance + theory-aligned baseline. Solver verification will refine frequency mix.

**All 22 spots → consensus_action = CHECK.**

### 2. HU-2.4 GROUP (7 spots: HU-2.4-LK-04..05, LK-07..08, LK-22..24, LK-26; 5 are 2-2-1 RAISE/CALL/FOLD; 2 are 3-2 with Opus disagree)

**Spot:** 6c5c. Eff 60bb. BTN (hero) opens 2.5bb, SB folds, BB calls. Pot 5bb. FLOP 8c7d7h (anchor) or {board variations}. BB checks, BTN bets 3.63bb (66%). BB CHECK-RAISES to 9.9bb. Pot 14.85bb, hero faces 6.27bb to call. SPR ~3. Hero straight draw + backdoor FD ~30-35% equity vs BB c-r range.

**Adjudication: CALL.** Reasoning: At compressed SPR with 30-35% equity + ~30% pot odds, CALL captures equity at fair price + preserves implied odds when straight comes. Jam adds variance without clear EV gain (FE on weak overpairs balanced by reverse-implied-odds on sets). FOLD is over-conservative.

**All 7 spots → consensus_action = CALL.**

### 3. HU-3.3 GROUP (7 spots: HU-3.3-LK-03, 05, 07, ...; delayed-stab vs check)

**Spot:** KsQs. Eff 100bb. BTN (hero) opens 2.5bb, SB folds, BB calls. Pot 5.5bb. FLOP 8h6h5c two-tone hearts. BB checks, BTN checks back (delayed-stab line). TURN: 8h6h5c{4c, 7c, etc.}. BB checks. Hero acts; no bet to face. Hero 2 overs + backdoor straight (KQ-J-T-9 path) ~6-7 outs.

**Adjudication: CHECK.** Reasoning: Pot-control with showdown value on connected wet board. 2 overcards have implicit equity but board threatens river straights/flushes — checking reduces pot bloat on bad rivers. BET is GTO-mixed but CHECK is higher-quality default for a delayed-stab line where villain has shown weakness twice.

**All 7 spots → consensus_action = CHECK.**

### 4. HU-2.3-LK-23 (1 spot)

**Spot:** Js9s. Eff 100bb. BTN opens 2.5bb, BB (hero) calls. FLOP Qs7s3d two-tone spades. BB checks, BTN bets 25% (1.4bb). BB calls. TURN 2c brick. BB checks, BTN bets 75% (×1.1 = 9.1bb). Pot ~20.6bb, hero faces 9.1bb. Hero nut FD + gutshot ~12 outs ~28-30% equity. Pot odds 31%.

**Adjudication: CALL.** Reasoning: Pot odds (31%) ≈ FD equity. Standard CALL captures equity + showdown on river. Js spade blocker reduces villain's KsJs/QsJs. RAISE is solver-mix option but adds variance; CALL is lower-variance quality choice.

**Spot → consensus_action = CALL.**

### 5. HU-2.5 GROUP (2 spots: HU-2.5-LK-02, HU-2.5-LK-03)

**Spot:** Ad5d. Eff 100bb. BTN (hero) opens 2.5bb, SB folds, BB calls. FLOP Jh8d3c. BB checks, BTN checks back. TURN 4c (LK-02) or 5c (LK-03). BB checks. Hero acts; no bet to face. Hero has A-high + gutshot (5 outs to wheel) + A-blocker; **NO FLUSH DRAW** (turn brick is club, not diamond — variation_param explicitly replaced 2d with 4c/5c).

**Adjudication: CHECK.** Reasoning: Without FD, hero is A-high + gutshot only. BET would be thin without equity backup; villain can call wider with showdown value. CHECK realizes equity at no cost + retains A-blocker bluff-catch on river. Original FD-spec adjudication (BET) does NOT apply when board mutated away from FD-completing turn.

**Both spots → consensus_action = CHECK.**

### 6. HU-3.4-LK-25 (1 spot)

**Spot:** Ts8h. Eff 100bb. BTN opens 2.5bb, BB (hero) calls. FLOP 7d7c3h paired-rainbow. BB checks, BTN bets 25% (anchor 1.4bb; ×1.5 variation = 2.1bb = 38% pot). Hero air with backdoor straight (7-8-9-T-J needs 6+9 or 9+x).

**Adjudication: FOLD (CHECK-FOLD).** Reasoning: Air hand on paired rainbow board OOP. Backdoor draws too thin to call. CHECK-RAISE bluff with no equity is high-variance. FOLD captures min-loss; standard line.

**Spot → consensus_action = FOLD.**

### 7. HU-3.5-LK-03 (1 spot)

**Spot:** Ac4c. Eff 100bb. BTN (hero) opens 2.5bb, SB folds, BB calls. FLOP Kh9d6s. BB checks, BTN bets 25% (1.4bb), BB calls. TURN 5h. BB checks, BTN checks back. RIVER 6c (variation: replaced 2c with 6c → board pairs the 6). BB leads 4bb (33% pot, pot 12bb). Hero has busted-air + A-blocker + 4-blocker (slight).

**Adjudication: CALL.** Reasoning: Pot odds 4 / (12 + 4 + 4) = 20%. A-blocker reduces villain's bluff-catch-this-folds-too-much value combos (Ax). Block-lead 33% on paired river is often weak/bluff range. CALL captures bluff-catch EV with blocker support. FOLD over-folds to thin sizing.

**Spot → consensus_action = CALL.**

### 8. HU-5.1 GROUP (2 spots: HU-5.1-LK-28 sizing 2.5x, HU-5.1-LK-29 sizing 3.0x)

**Spot:** 7d7s set. Eff 100bb. BTN opens 2.5bb, BB (hero) calls. FLOP Th7c4h two-tone hearts. BB checks, BTN bets 4.6bb (anchor 66%). VARIATION: ×2.5 = 11.5bb (~164% overbet) for LK-28; ×3.0 = 13.8bb (~197% overbet) for LK-29. Hero set-of-7s on wet two-tone.

**Adjudication: RAISE (CHECK-RAISE).** Reasoning: Set on wet two-tone facing massive overbet is a clear CHECK-RAISE / JAM spot. Charge FDs + protect against turn cards (8-9-J-Q-A overcards). Slowplay loses too much value on safe rivers + concedes equity to draws. Standard solver-aligned line.

**Both spots → consensus_action = RAISE.**

### 9. HU-6.4-LK-24 (1 spot)

**Spot:** AcQh. Eff 100bb. BTN opens 2.5bb, BB (hero) calls. FLOP Qs9c4s two-tone spades. BB checks, BTN bets 25% (1.4bb), BB calls. TURN 7c. BB checks, BTN bets 75% (6.2bb), BB calls. RIVER 2h brick (FD busted). BTN bets 75% (anchor 15.5bb). VARIATION: ×1.25 = 19.4bb. Pot 20.7bb, hero faces 19.4bb. Hero TPTK (Qs paired with hero Qh + A kicker).

**Adjudication: CALL.** Reasoning: Top-pair-top-kicker is the canonical bluff-catch hand on busted-FD river facing polarized triple-barrel. Folding TPTK overcompensates to value-heavy assumption; standard solver consensus is CALL with blocker support. Pot odds 19.4 / (20.7+19.4+19.4) = 33%; need 33% equity to call; TPTK has plenty.

**Spot → consensus_action = CALL.**

## Adjudication summary (44 spots → 6 distinct actions)

| Action | Spot count |
|---|---|
| CHECK | 22 (HU-5.4) + 7 (HU-3.3) + 2 (HU-2.5) = **31** |
| CALL | 7 (HU-2.4) + 1 (HU-2.3-LK-23) + 1 (HU-3.5-LK-03) + 1 (HU-6.4-LK-24) = **10** |
| RAISE | 2 (HU-5.1) = **2** |
| FOLD | 1 (HU-3.4-LK-25) = **1** |
| **Total** | **44** ✓ |

---

# (b) Builder data-layer application

**Action for builder:** Update `data/hu_corpus/full_HU2_HU6/consensus.jsonl` for all 44 owner-arb rows. For each row, set:
- `consensus_action` = the per-spot adjudication from §(a) above
- `notes` field updated to: `"owner-delegated orchestrator-adjudicated <ACTION> per MAIN_TERMINAL_FULL_44_ARBS_ADJUDICATION_AND_PRE_D4_DISPATCH_2026-05-10.md §(a); owner-arb=true preserved; solver-verification-pending"`
- `owner_arb` field remains `true` (preserves provenance signal)

Output: separate small-PR (per PR #349 precedent), title format: `Builder: apply 44 owner-delegated orchestrator-adjudications to full_HU2_HU6/consensus.jsonl`

QC for the data-layer PR is routine (1 file diff verification; not milestone-class). Orchestrator merges autonomously on diff verification.

---

# (c) Solver-verification queue (updated)

Per `feedback_solver_verification_queue.md` + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`: ALL 44 newly-adjudicated spots enter the solver-verification queue alongside the 4 prior owner-adjudications. Total queue: **48 spots**.

**Owner explicit on 1.5-D.4 readiness:** "we can verify with solver later and retrain if necessary" → 1.5-D.4 dispatch proceeds with HOLD-with-accepted-risk on solver verification. Verification becomes post-train; if solver disagrees on N spots, retrain delta is the recovery path (re-label N spots, update corpus, re-train).

## Updated queue (48 spots)

**Prior (4 spots; from earlier dispatches):**
| spot_id | hero/board | adjudication | source |
|---|---|---|---|
| HU-6.5 | Qd9h on 7h6c5s2d8d; BB 150% overbet | CALL | PR #338 |
| HU-1.5-LK-10 | Qd9h on 7h6c5s2d8d; BB ~112% overbet | CALL | PR #343 |
| HU-1.4-LK-04 | TsTd on 8h5c2d6c; BB 33% probe | CALL | PR #348 |
| HU-1.4-LK-05 | TsTd on 8h5c2d7c; BB 33% probe | CALL | PR #348 |

**New (44 spots; this dispatch):**
| anchor | spot count | spot_ids | adjudication |
|---|---|---|---|
| HU-2.3 | 1 | HU-2.3-LK-23 | CALL |
| HU-2.4 | 7 | HU-2.4-LK-04, -05, -07, -08, -22, -23, -24 (sample; full list in consensus.jsonl) | CALL |
| HU-2.5 | 2 | HU-2.5-LK-02, -03 | CHECK |
| HU-3.3 | 7 | HU-3.3-LK-03, -05, -07, etc. (full list in consensus.jsonl) | CHECK |
| HU-3.4 | 1 | HU-3.4-LK-25 | FOLD |
| HU-3.5 | 1 | HU-3.5-LK-03 | CALL |
| HU-5.1 | 2 | HU-5.1-LK-28, -29 | RAISE |
| HU-5.4 | 22 | HU-5.4-LK-01..LK-22 (or -01..-22 cluster) | CHECK |
| HU-6.4 | 1 | HU-6.4-LK-24 | CALL |

**Drain protocol** (when solver returns online; per memory rule):
1. Run all 48 spots through solver
2. Document agree/disagree per spot
3. If solver disagrees on any spots: queue retrain-delta dispatch (re-label disagreeing spots; update consensus.jsonl + raw_labels; re-train HU model on updated corpus)
4. Document outcome in `SOLVER_VERIFICATION_QUEUE_DRAINED_<date>.md` comm

This rule persists across orchestrator sessions via memory file `feedback_solver_verification_queue.md` + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`.

---

# (d) Post-data-layer-fix: authorize Phase 1.5-D.4 design/prep

After builder data-layer PR + orchestrator merge: Phase 1.5-D.4 (HU model retrain on 59-surface, from-scratch per design memo §4.5) is AUTHORIZED to proceed.

## 1.5-D.4 scope reminder (per design memo §4.5)

- **Trainer:** `river-rats-core/train_model_vNext_hu.py` (HU-specific variant of `train_model_v9_student.py`)
- **Warm-start strategy:** from-scratch (architect-committed; multi-class transition + corpus-origin difference necessitate re-init)
- **Surface:** 59-feature (matches v9-3way-on-59 production)
- **Corpus inputs:**
  - `data/hu_corpus/pilot_50_v2/consensus.jsonl` (50 hands from HU-1 axis)
  - `data/hu_corpus/full_HU2_HU6/consensus.jsonl` (696 hands from HU-2..HU-6 axes; will include 44 newly-adjudicated rows post-data-layer-fix)
  - **Total:** 746 HU-labelled situations (architect committed ~750)
- **Target:** vNext-HU-59 model artifact with provenance docstring linking commit → model
- **Gate:** TBD per architect dispatch (likely ≥88.1% HU accuracy reference + ≥ HU baseline on close-hand subset)

Builder dispatches Phase 1.5-D.4 per design memo §4.5 in a separate dedicated dispatch comm after data-layer PR merges.

---

# Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT modify FULL labelling raw_labels.jsonl or opus_tier_up.jsonl (only consensus.jsonl rows for owner-arb spots)
- ❌ Does NOT modify pilot_50_v2/consensus.jsonl (already adjudicated in PR #349)
- ❌ Does NOT change §4.3 consensus rule or §4.4 corpus-assembly architecture
- ❌ Does NOT use solver output as training label (solver is OFFLINE; verification is post-train)
- ❌ Does NOT block 1.5-D.4 on solver-queue-drain (owner explicitly accepted HOLD-with-risk)

---

# QC stream — what you audit

For builder data-layer PR (post-this-dispatch):
1. Diff scope strict: 1 file (`data/hu_corpus/full_HU2_HU6/consensus.jsonl`); 44 row updates
2. Per-row verification: each owner-arb row updated to match §(a) per-spot adjudication
3. Notes field cites this dispatch comm + "solver-verification-pending"
4. owner_arb=true preserved
5. No other rows modified (only owner_arb=true spots)

Routine audit (~10 min). Cross-post + heartbeat per protocol.

---

# Owner — informational

- 11 unique decisions covering 44 spots: 31 CHECK + 10 CALL + 2 RAISE + 1 FOLD
- All 44 added to solver-verification queue (now 48 total queue)
- 1.5-D.4 retrain proceeds with accepted-risk per your direction; solver-verify + retrain-if-needed is recovery
- Saved memory `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` for future-session reference

---

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `3034092` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- QC verdict PR #361 head: `c930acd` (PASS · 0/0/0; 4 deviations ACCEPT)
- Builder PR #359 head: `48b695b`
- AMENDMENT dispatch: master `bdd1960` (PR #357)
- Phase 0 outcome (FL6 evidence): master `c591570` (PR #356)
- 1.5-D.3 FULL INFRA-PREP merged: master `6274fce` (PR #350 + QC PR #352 PASS)
- HU-1.4 data-layer-fix precedent: master `e58ed94` (PR #349) — pattern reference for builder
- Architect's design memo §4.3 + §4.4 + §4.5: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` (NEW), `feedback_solver_verification_queue.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`

**Status: 44 owner-arbs adjudicated by orchestrator per owner-delegated quality picks (31 CHECK + 10 CALL + 2 RAISE + 1 FOLD). Builder fires data-layer PR to apply to consensus.jsonl. Solver-verification queue updated to 48 spots; HOLD-with-accepted-risk per owner. After data-layer PR merge → orchestrator authorizes Phase 1.5-D.4 (HU retrain) per design memo §4.5.**
