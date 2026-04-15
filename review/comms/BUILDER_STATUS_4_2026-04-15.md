---
date: 2026-04-15
from: Builder
to: Main terminal / Owner
re: Round 4 status — directive-f executed, all tracks closed except v2.3 hand generation
status: ALL DIRECTIVE-F TRACKS COMPLETE
---

# Builder Status #4

5 commits this round.

| Commit | Item | Result |
|---|---|---|
| `ee9b69d` | Track 2 closure | ✅ done — 84% canonical adopted |
| `553c730` | Track 6 amendments (initial) | ✅ done — 5 amendments applied |
| `11f4c85` | Stream C training-bucket spot-check | ✅ done — verdict 400 hands |
| `c78ee17` | Forensic verification | ✅ done — 80% reproduces, d4534-OUT confirmed |
| `166d393` | Track 6 sizing follow-up | ✅ done — placeholder filled with 400 |

## Track 2 — CLOSED

Per directive-f §1: 84.0% (42/50) MW-50 adopted as canonical for the
live `v2_2_model.json`. 80% reclassified as recovered shadow-model
measurement. `V22_TRAINER_PORT_2026-04-15.md` updated.

## Track 6 — COMPLETE (initial + sizing follow-up)

### PLAN_V23_SCOPE amendments
1. **BET delta** — Architect chose **additive interpretation**:
   allocation-table BET rows sum to 186 (not 166); RAISE rows = 20;
   total 206. Rebalance updated from "+166 BET" to "+186 BET" → v2.3
   BET = 285 (48.2%). ~31 Protection BET row reframed as a subset of
   the 186. Rationale documented in a new "BET delta accounting"
   paragraph.
2. **Section 2 bias signature** — Replaced "Bucket-First CHECK Bias"
   with "Defensive Multiway-Checked-Through CHECK Bias" (verbatim
   directive-f wording). Predicate rendered as formal feature
   conjunction. Pass 1 prompt override clause inserted verbatim.
3. **Calibration gate** — New "Explicit Calibration Gate"
   subsection: 23/28 + reversals correct, failure → panel redesign.
4. **Supplement sizing** — Initially placeholder, **now resolved
   to 400 hands** per Stream C verdict (commit `166d393`). Caveat
   recorded: bucket size 24 is near sparsity floor, 400 is both
   the label-signal-healthy answer and the safe near-sparsity
   answer.

### PLAN_V23_DIAGNOSTIC_TEST_SET amendments
5. **Absolute accuracy floor** — Groups A+B now require BOTH +5pp
   delta over v2.2 AND 70% absolute floor.
6. **Group D regression fallback** — >1 hand regression on reversal
   accuracy = STOP before ship.

## Stream C — verdict 400

- Bucket size: 24 rows (6.2% of 385)
- Distribution: BET 79.2% / CHECK 20.8% / 0% FOLD/CALL/RAISE
- 2 solver-reversal overrides (both BET→CHECK)
- Bucket medians (deep inside precondition shape, not edge-
  clustered): HRP 0.884, equity_vs_range 0.875, worse_hand_pct
  0.946, SPR 1.250
- Verdict: ≤30% CHECK → label signal healthy → 400 hands
- Caveat: sparsity-floor proximity → 400 also resolves
  representation risk

## Forensic verification — PASS

Recovered `eval_MW_with_legal_action_masking.py` ran as-is →
**80.00% (40/50)** on MW-50, d2920-IN / d4534-OUT confirmed. FB-40
side effect = 72.5%. Shadow-model finding from Stream A.3 closes
cleanly. Confirmation appended to `V22_TRAINER_PORT_2026-04-15.md`
§7.

## Updated track grid

| Track | Status |
|---|---|
| 1 Harness hardening | ✅ done |
| 2 FB/MW re-eval | ✅ CLOSED |
| 3 Training audit | ✅ done |
| 3.5 ANOMALY-A | ✅ resolved (path 3) |
| 4 MW bias deep-dive | ✅ done (B.1+B.2) |
| 5 BP generator fix | ✅ done |
| 6 Scope corrections | ✅ done (incl. sizing) |
| Stream A | ✅ shipped (port + CLAUDE.md addendum) |
| Stream C | ✅ done — 400 hands |
| Forensic verification | ✅ done |

## What's left (per consolidated plan §6)

| Item | Owner? | State |
|---|---|---|
| Solver on 10 MW misses | yes | deferred |
| Gate 7 ship/iterate | yes | owner call |
| v2.3 scope final approval | yes | scope now amended; ready for owner sign-off |
| v2.3 hand generation | builder, post-approval | gated on owner approval of amended scope |
| Clean-CSV retrain (deferred) | builder, on directive | not on critical path |
| v3.0 action distributions | backlog | post-v2.2 |

Nothing actionable for builder until owner approves the amended
v2.3 scope OR issues a new directive. Standing by.
