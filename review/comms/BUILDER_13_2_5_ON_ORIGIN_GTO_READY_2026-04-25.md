---
date: 2026-04-25
from: Logic builder
to: Main terminal (orchestrator) · GTO reviewer · Owner
re: Stage 3.5 commit 13.2.5/16 is on origin/master — ready for post-merge GTO re-review verdict
status: NOTIFICATION — passive push of bf4b24e + c4ab27e succeeded per orchestrator addendum 0bb91ef; standing by on 13.3 authoring pending GTO verdict + orchestrator greenlight; PR pattern acknowledged for 13.3 onward
---

# Builder — 13.2.5 on Origin, GTO Re-Review Ready

## State confirmation

Per `MAIN_TERMINAL_PUSH_POLICY_ADDENDUM_2026-04-25.md`, `bf4b24e` and
`c4ab27e` landed on origin/master passively when orchestrator pushed
`b6c1ade`. Verified locally:

```
$ git log --oneline origin/master -5
0bb91ef Push-policy decision addendum — push succeeded; PR pattern still standing
b6c1ade Push-policy decision — Option B (feature-branch + PR) for Stage 3.5
c4ab27e Builder comms — commit 13.2.5 landed locally, push blocked
bf4b24e Stage 3.5 commit 13.2.5/16: GTO fix-forward on 2nd dry-run batch
329ecf7 Stage 3.5 commit 13.2/16: 2nd dry-run — 5 synthetic deferred-shape entries
```

Local working tree clean, in sync with origin/master at `0bb91ef`.

The 13.2.5 fix-forward is now on the audit trail. No retroactive PR
required (addendum §"Revised concrete action for 13.2.5"). This note
is the audit-trail handoff to GTO reviewer.

## What the GTO reviewer is verifying

Commit `bf4b24e` (`Stage 3.5 commit 13.2.5/16: GTO fix-forward on
2nd dry-run batch`) addresses the GTO reviewer's APPROVE_WITH_FIXES
verdict on commit `329ecf7` (commit 13.2 — 2nd dry-run batch). Five
fix items implemented as FIX #1–#5:

| # | Fix | Source | File |
|---|-----|--------|------|
| 1 | SYN-T_B05 header comment — BTN RAISE is hero-side and position-filtered; villain `[BET, CALL]` collapses to CALL via MUST #11/#12 last-decision-bearing rule | ACTION ITEM #1 from 13.2 GTO verdict | `_reference_action_history_sidecar.py` |
| 2 | SYN-F5 chain comment — chain is 2 steps (flop:CALL + turn:CALL); river is decision-street, excluded from narrowing chain per prior-street-only rule | ACTION ITEM #2 | `_reference_action_history_sidecar.py` |
| 3 | SYN-F7_HU_donk_x_bet authored — OOP-aggressor donk-flop → turn-check → river-bet shape (flop BET / turn CHECK / river facing_bet) per MUST #49 8-bucket coverage requirement | ACTION ITEM #3 | `_reference_action_history_sidecar.py` |
| 4 | Authoring-spec clarification in sidecar docstring — fixture_meta boards must be `List[str]` (`'Kh','7d','2c'`), NOT concatenated `'Kh7d2c'` | CLARIFICATION | `_reference_action_history_sidecar.py` docstring |
| 5 | `validate_fixture_meta_boards()` — AST-based CI validator catches board-format drift at lint time | INFO | `validate_sidecar_completeness.py` |

Plus a classifier correctness fix in `solver_verify_sidecars.py`:
`hu_bet_x_call_bet` vs `hu_donk_x_bet` disambiguated via the
`turn_has_call` predicate. SYN-F7 lands in `hu_donk_x_bet` after
the fix.

## Files touched

```
river-rats-core/_reference_action_history_sidecar.py    (+85 lines)
river-rats-core/tests/solver_verify_sidecars.py         (+19 lines)
river-rats-core/tests/test_commit13_sidecar_dryrun.py   (+33 lines)
river-rats-core/tests/validate_sidecar_completeness.py  (+86 lines)

4 files changed, 209 insertions(+), 14 deletions(-)
```

No production-feature-extraction code touched; sidecar fixtures +
validator + tests only. Scope is fix-forward on 13.2 authoring,
not new feature work.

## Test results at push time

- MUST #35 structural validator: PASS (11 reference + 3 calibration entries + fixture_meta AST check)
- MUST #54 solver-verify stub: PASS (7 buckets, 7-entry stratified sample)
- `test_commit13_sidecar_dryrun.py`: **11/11 PASS** (was 9/9 pre-13.2.5)
- Broader suite: **1332 passed, 11 failed, 55 skipped** (~83s)
- All 11 broader-suite failures are pre-existing (feature count 55→59 v2.4 held-back blockers; v2.2 CSV encoding). NONE are 13.2.5 regressions.

Sidecar state after 13.2.5:

- 11 reference entries (was 10 pre-13.2.5; FIX #3 adds SYN-F7_HU_donk_x_bet)
- 3 calibration entries (unchanged)
- 7 shape buckets populated (was 6; `hu_donk_x_bet` added by FIX #3)

## Suggested GTO reviewer focus

For the post-merge audit-trail verdict:

1. **FIX #1 + #2 narrative correctness** — the header/chain comments now explain *why* the collapse / chain length is what it is. Verify the explanations match MUST #11/#12 (last-decision-bearing collapse) and the prior-street-only chain rule respectively.
2. **FIX #3 SYN-F7 entry** — verify the donk-flop → turn-check → river-bet shape is faithful to MUST #49's `hu_donk_x_bet` bucket definition and that the chain steps + facing_bet gating are GTO-correct on this shape. This is the only new authored entry; the others are comment / spec clarifications.
3. **Classifier fix** — `turn_has_call` predicate disambiguates `hu_bet_x_call_bet` vs `hu_donk_x_bet`. Confirm the predicate is sufficient (no boundary case where turn has BOTH a call and a non-call action that would mis-route).
4. **AST validator (FIX #5)** — confirms board format at lint time. Ground rule: validator should fire on `'Kh7d2c'` and pass on `['Kh', '7d', '2c']`. Optional spot-check.

ACTION ITEMS #1–#3 were the binding fixes from 13.2's verdict.
CLARIFICATION (#4) and INFO (#5) were addressed in scope as well per
quality default — none required, all delivered.

## What is NOT in 13.2.5

- No new fixture entries beyond SYN-F7 (FIX #3 only)
- No multiway-field promotion (that's commit 14's Finding-B fold-in scope)
- No range-narrowing logic changes (sidecar fixtures only)
- No KB / labeller / model changes

## Standing posture

Per orchestrator addendum §"Revised concrete action for 13.2.5":

1. ✅ Push state confirmed (`bf4b24e` + `c4ab27e` on origin)
2. ✅ This notification published (audit trail)
3. ⏸ HOLD on commit 13.3 authoring — awaits GTO verdict + orchestrator greenlight
4. 🆕 PR pattern adopted from commit 13.3 onward per parent directive `b6c1ade`:
   - Branch naming `stage3.5/commit-13-3` (and per-batch sub-branches if 13.3 splits into ~25-entry slices)
   - One PR per logical batch, `--merge` (not `--squash`) on approval
   - Per-batch GTO review on the PR thread, not in `review/comms/`
   - Same shape continues for commits 14 / 15 / 16 / M4 / M5

If GTO surfaces APPROVE_WITH_FIXES or REWORK on 13.2.5: builder
fix-forwards as 13.2.6 on a feature branch (PR pattern now applies)
before commit 13.3 begins.

If GTO APPROVE: builder waits for orchestrator to greenlight 13.3,
then opens `stage3.5/commit-13-3` and starts authoring the ~130-entry
full lift per `MAIN_TERMINAL_COMMIT13_DECISION_2ND_DRYRUN_2026-04-24.md`
§"Then (C.2) full lift" with per-batch GTO review.

## Cross-stream impact

| Stream | Effect |
|---|---|
| Logic | 13.2.5 audit trail closes on GTO verdict; 13.3 authoring unblocked on APPROVE |
| Teaching HOLD #1 | Unchanged — still waits on commit 16 + M4/M5 |
| Teaching HOLD #3 / #5 | Unchanged — still waits on commit 14 (Finding B fold-in) |
| Teaching HOLD #4 | Unchanged — waits on #1 + #3 + #5 |

No teaching-side action triggered by 13.2.5 alone. Teaching stays
at PRE-VERIFICATION HOLD on its v4.1 SHIP REPORT.

## Reference

- `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md` — original local-landed report (push was blocked at the time)
- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` (`b6c1ade`) — parent directive: Option B PR pattern as standing
- `MAIN_TERMINAL_PUSH_POLICY_ADDENDUM_2026-04-25.md` (`0bb91ef`) — passive-push addendum; 13.2.5 retroactive-PR moot
- `MAIN_TERMINAL_COMMIT13_DECISION_2ND_DRYRUN_2026-04-24.md` (`cb45c15`) — quality-default precedent for the 2nd dry-run batch path
- `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md` — commit 14 Finding-B spec for upcoming work
- `feedback_quality_default_no_ask.md`
- `feedback_github_is_state_not_local.md`

Standing by for GTO verdict.
