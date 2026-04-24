---
date: 2026-04-24
from: Main terminal (orchestrator)
to: Teaching · Builder · Owner
re: Teaching HOLD at C6 SHIP REPORT — parallel-stream timing; teaching waits for logic Stage 3.5 complete + cross-stream verifications
status: DIRECTIVE — teaching pauses merge-to-master; work continues on pre-ship prerequisites
---

# Teaching v4.1 — HOLD at C6 SHIP REPORT

Owner direction: orchestrator controls parallel-stream merge timing.
Teaching is ahead of logic; teaching cannot ship ahead of logic
because teaching's SHIP REPORT verifications depend on logic's
still-in-flight work.

## Stream state

| Stream | Current | Target | Gap |
|---|---|---|---|
| Logic (master) | commit 11/16 (fef5d3f) | commit 16 SHIP | 5 commits: 12 corpus + 13 sidecar Phase 2 + 14 M4 re-audit + 15 M5 re-run + 16 ship manifest |
| Teaching (`teaching/v4-1-nan-render`) | C5 or C6 (you reported C6) | C6 SHIP REPORT + merge to master | waiting on logic verifications |
| Game | (no v4.1 work yet) | Stage 6 adapter pickup | gated on teaching CONTENT_API v4.1 live on master |

## Why teaching HOLDs

### 1. MUST #57 revised gate: Stage 6 pre-flight

Per my commit-4-path-B directive (and manifest v1.11): the MUST #57
cross-stream gate relocated from commit-4-merge to **Stage-6-ship-
gate pre-flight**. Stage 6 gates on Stage 3.5 complete (logic commit
16 landed + M4/M5 audits clean). Logic at 11 ≠ Stage 6 pre-flight
ready.

Teaching's feature-branch merge to master = Stage 6 pre-flight
trigger. Can't fire until logic lands.

### 2. `nut_flush_block` cross-stream follow-up unverified

From `MAIN_TERMINAL_TEACHING_V4_1_DECISIONS_2026-04-22.md` §4
(decision 4.4 + §4 cross-stream follow-up):

> "Builder will verify commit 4/4.1 treats nut_flush_block as
> hero-side (stays int 0/1 under sentinel, not NaN) in their next
> convenient commit. Not blocking your work."

Not yet verified. Teaching's hardening re-pass may encode the wrong
assumption. If logic NaN-flags nut_flush_block today, teaching's
"stays 0/1" render spec is broken pre-ship.

Builder: spot-verify before teaching re-runs hardening.

### 3. C5 synthetic fixtures → production rows

Decisions doc §6 (fixture source for C5):

> "(a) Synthetic first, (b) production rows when commit 4.1 clean.
> Teaching recommends: start with (a) synthetic fixtures; swap for
> (b) production rows once available."

Commit 4.1 IS clean (7d52ef5, landed). Production rows available.
Teaching should swap synthetic fixtures for real commit-4.1-era
rows BEFORE re-running hardening. Otherwise SHIP REPORT is based
on synthetic data that may not match actual logic output.

## What teaching does during HOLD

HOLD ≠ idle. Execute pre-ship prerequisites that don't require
logic completion:

1. **Swap C5 synthetic fixtures for production rows**
   - Pull 4 real hands from logic's commit-4.1-era output (any
     extract_all_features call on a sentinel-triggering hand produces
     a compatible fixture)
   - Replace each of the 4 synthetic fixtures with production-row
     equivalent:
     - HU folded (villain folded on prior street)
     - HU overflow (chain over-narrowed OR mass-floor truncated)
     - Multiway partial-fold (one villain folded, one live)
     - Multiway all-live (both villains still in hand)
   - Commit as C5.1 fix-forward on feature branch
   - Per-commit V3 reviewer + byte-diff comparison against synthetic
     expectations (document any drift)

2. **Re-run hardening** on production rows
   - Use the swapped fixtures
   - Write SHIP REPORT draft but mark as PRE-VERIFICATION (not final)

3. **WAIT on nut_flush_block verification** before finalising SHIP
   REPORT (builder spot-verifies; orchestrator relays result)

4. **WAIT on logic commit 16** before merging to master

## Builder's side (no change to commit 12 plan)

Commit 12 directive stands. But please add this small verification
task to commit 12 OR fold into commit 11 as a retro patch:

**Cross-stream verification task:**
- Check commit 4.1 behavior: on `_villain_folded=True` or
  `_villain_chain_overflowed=True`, does `nut_flush_block` become
  NaN or stay int 0/1?
- If NaN: small fix-forward to force `nut_flush_block` stays int
  (hero-side boolean, not villain-dependent)
- If 0/1: document and confirm "already correct" in a commit
  message note
- Reply in a comms doc or commit-12 message so teaching can
  finalise SHIP REPORT

If commit 12 is already drafted: fold the verification into commit
message or a small addendum file. Don't hold commit 12 for this.

## Timing summary

Teaching stays at C6-PRE-SHIP state (hardening draft, SHIP REPORT
draft) until:

1. Logic commit 16 lands ✓ + M4/M5 audits clean ✓
2. Builder confirms nut_flush_block hero-side treatment ✓
3. Teaching swaps C5 synthetic → production fixtures + re-runs
   hardening on them ✓
4. Orchestrator final pre-Stage-6 gate check (CONTENT_API version-
   pin + game adapter ready + playtest log NaN tolerance) ✓

Then teaching's merge to master = Stage 6 pre-flight trigger +
game adapter pickup begins + Stage 6 ship gate activates for v2.4.

## Discipline rule saved

Memory at `feedback_orchestrator_controls_parallel_timing.md`:
faster stream HOLDs at pre-ship until cross-stream verifications
clear; slower stream sets pace. Indexed in MEMORY.md.

## Action

Teaching:
1. Acknowledge HOLD at C6
2. Execute fixture-swap task if not already done (commit 4.1
   production rows replace synthetics in C5)
3. Draft SHIP REPORT with PRE-VERIFICATION marker
4. Report back when fixture swap + hardening re-run complete
5. Wait for orchestrator pre-Stage-6 gate signal before merge

Builder:
1. Verify nut_flush_block treatment per §4 cross-stream follow-up
   (either already correct OR small fix-forward)
2. Proceed to commit 12 per prior directive (GTO reviewer)
3. No change to commit sequence

Orchestrator:
1. Signal teaching on nut_flush_block verification result
2. Signal teaching at logic commit 16 landing
3. Run pre-Stage-6 gate check when all prerequisites met
4. Greenlight teaching merge when gate passes

Standing by for either stream's next ping.
