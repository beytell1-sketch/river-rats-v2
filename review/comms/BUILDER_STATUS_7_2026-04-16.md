---
date: 2026-04-16
from: Builder
to: Main terminal / Owner
re: Round 7 — Group D ingested, Phase 1.4 resolved, Phase 3 PASS, Phase 3.5 PASS
status: Phase 4 UNBLOCKED pending owner 3–5-hand spot-check
---

# Builder Status #7

**6 commits this round.** Every v2.3 gate between Phase 1 and Phase 4 has cleared on iteration 1.

| Commit | Item | Result |
|---|---|---|
| `1a9c386` | Group D owner picks ingested | ✅ 5 reversals, 10/10 tests pass |
| `84eaae0` | Phase 1.4 curated — 3 staged | ✅ PA_Board3 dropped per owner |
| `84c65d5` | Phase 3 calibration | ✅ **PASS iter 1**: 28/28 + 10/10 |
| `f9cde81` | Phase 3.5.1 pilot sample | ✅ 16 hands stratified |
| `d7ac0a1` | Phase 3.5.2 pilot labelled | ✅ 16 × 4 Pass 1 + 4 Pass 2 |
| `ec2d94b` | Phase 3.5.3 pilot review | ✅ **PASS iter 1**: 5/5 criteria |

## Group D — ingested (commit `1a9c386`)

Owner picks: `d4312_CO_turn`, `d9556_BB_flop`, `d2074_BTN_turn`, `d5466_CO_flop` + existing `d3688_BB_flop` = **5 reversals total**. Registry extended as a one-line set addition; no code change needed. Tests 10/10 still pass. Extensibility property holds.

## Phase 1.4 — curated resolved (commit `84eaae0`)

3 nut-blocker hands staged per owner directive:
- `d1983_BTN_turn` (turn, row 7) — Ad4d nut FD
- `BP7_06` (turn, row 7) — AhJh nut FD
- `d5620_BTN_flop` (flop, row 6) — AdQs nut SD + A-blocker

PA_Board3 dropped (pool-defect cleanup ticket `TICKET_PA_BOARD_POOL_DEFECT_2026-04-16.md` opened for post-ship backlog). **Final supplement total: 398.** UMBRELLA 268 absorbs predicate-shape coverage.

## Phase 3 calibration — PASS iter 1 (commit `84c65d5`)

- **Standard: 28/28** (100%)
- **Reversals: 10/10** (includes all 5 Group D + original anchors)
- Iteration count: 1
- No prompt revision or KB edit needed

Override-clause behaviour in single-panel exam:
- Predicate-matching hands: **4/4 fired + cited** (d2410, d8963, d3178, d4312)
- Negative-control guards: **4/4 correctly did NOT fire** (d2074, d3688, d5466, d9556)

Edge case carryforward: MW-27 — action history shows both villains checked this street but `villain_checked_back=0` in feat_dict (feature counts only prior-street check-backs). Override fired "conceptually" and produced the correct answer. Flagged for Phase 3.5 watch — did NOT recur at turn-level in the pilot.

## Phase 3.5 pilot — PASS iter 1 (commits `f9cde81`, `d7ac0a1`, `ec2d94b`)

**16 hands** sampled, stratified:
- A — predicate-matching: 7 (UMBRELLA × 5, MM_IP_TURN × 2)
- B — non-predicate negative controls: 4 (RAISE_VALUE × 2, PROT_DANGER × 1, PFR_CONT × 1)
- C — §3 additions: 2 (BP7_06 → §3.A/§3.C, MM_OOP_TURN_001 → §3.D)
- D — reversal-shaped boundary: 3 (MM_IP_TURN_003/030/033 at evr≈0.36–0.40)

Zero overlap with Phase 3 exam (33 hands).

**64 Pass 1 traces (16 × 4) + 4 Pass 2 review traces** on the 4 hands with 3/4 majorities. All traces preserved verbatim in `training-data/v23_pilot_labelled.jsonl` (not merged into production CSV).

### Per-criterion verdict

| # | Criterion | Target | Actual | Verdict |
|---|---|---|---|---|
| 1a | Override citation on predicate | ≥80% | **100% hand / 95% panel** | PASS |
| 1b | Negative-control non-leak | 100% | **0/24 fired** | PASS |
| 2 | §3 engagement on targeted | ≥80% | **4/4 on both targeted hands** | PASS |
| 3 | 4/4 agreement on predicate | ≥70% | **80% (8/10)** | PASS |
| 4 | Pass 2 v3 citations | 100% | **4/4** | PASS |
| 5 | Reasoning quality | "no regression" | clean; 70% non-trivial conflicts; 89% substantive alternatives; no templating | PASS |

**Overall: PASS on iteration 1.** No prompt revision needed.

### Noteworthy informational findings (non-blocking)

- **MW-27 carryforward resolved favourably.** Both flop-level `villain_checked_back=0` hands (PROT_DANGER_011, PFR_CONT_025) correctly kept `override_clause_fired=false` across all 8 panels — improvement over the Phase 3 MW-27 ambiguity. Turn-level MW-27 shape did not recur in the pilot. Noted for future v3 tightening; not blocking.
- **Composition-quad split pattern.** The two Stratum D 3/1 splits (MM_IP_TURN_003/033) share 4% villain_air_pct + 33-37% villain_draw_pct. Pass 2 affirmed the mechanical override and enqueued both for solver. If solver agrees with the dissenters (CHECK), a future v3 could add a composition-quad guard to the override-the-override criteria. This is learning from edge cases for v3.x, not a Phase 3.5 FAIL.
- **§3.B unreachable** from factory records (zero HRP=0.00 cases). §3.B is a guard against a historical test-harness artifact (HRP=0.00) that no longer arises in the post-Fix-1 pipeline. Correct by design — no action needed.

## Phase grid

| Phase | Status |
|---|---|
| 0 Pre-flight | ✅ GO |
| 1 Generation | ✅ 483 factory + 3 curated = 486 records |
| 1.4 Curated | ✅ resolved (3 staged) |
| 1.5 Solver-sourced | 🟡 owner-led, async |
| 2 Assembly QA | ✅ PASS factory (curated re-QA still light-touch pending) |
| 3 Calibration | ✅ **PASS iter 1** |
| **3.5 Pilot review** | ✅ **PASS iter 1** |
| 4 Production labelling | 🟢 **UNBLOCKED** pending owner spot-check |
| 5 Assembly | ⏸️ gated on Phase 4 |
| 6 Training | ⏸️ gated on Phase 5 |
| 7 Validation | ⏸️ gated on Phase 6 (solver on 8 MW misses at ship gate) |

## Owner touchpoint needed

**Phase 3.5 spot-check (~30 min).** Read `review/comms/PHASE_3_5_PILOT_REVIEW_2026-04-16.md`. Spot-read reasoning traces for 3–5 pilot hands (suggested set is flagged in the review doc). Confirm or flag anything the builder missed.

- **CONFIRM →** Phase 4 launches (400-hand production labelling, same 4+2 panel structure)
- **FLAG →** prompt redesign + new pilot set + re-run Phase 3 + Phase 3.5

## Builder holding

Nothing actionable without owner spot-check result. When confirmed, Phase 4 proceeds — estimated 168 Pass 1 calls + ~30 Pass 2 calls (2-3 hours with parallel panels).

Cleanup backlog (post-ship, non-blocking):
- PA_Board pool defect ticket
- v2.3 factory position concentration (BTN/SB only — may want CO/HJ pass in future iteration)

Standing by.
