---
date: 2026-04-26
from: Main terminal (orchestrator) per owner revert direction at ~21:05 SAST
to: Logic builder · Pilot Orchestrator · Owner (briefed) · QC stream
re: Owner-reverted "upgrade to Opus" direction acknowledged; Path A directive at 24494eb revised — A.4 v3.2 retry runs PARALLEL Sonnet+Opus (Option C+ on revised protocol) instead of Opus-only; F-S5 patch bundled in v3.2 proceeds (Pilot Orchestrator releases the hold); cost envelope back to original $140-$700 spec
status: REVISION — Path A v3.2 protocol revision STILL ACTIVE; A.4 retry mode = parallel Sonnet+Opus per Option C pattern; F-S5 patch in v3.2 (bundle) confirmed go; cost envelope restored to spec; Phase B model lock decided empirically post-A.4-retry per owner's preference (Sonnet preferred per revert)
---

# Path A revision per Opus revert

## Owner revert direction

Per Pilot Orchestrator comm at master `1fe57a2`
(`PILOT_PHASE_A_OWNER_DIRECTION_OPUS_LABELLER_LOCK_REVERTED_2026-04-26.md`):

> 1. "upgrade lablelers to opus 4.7" (~21:00 SAST, initial)
> 2. "undo upgrade to opus 4.7 request" (~21:05 SAST, revert)

Pilot Orchestrator correctly reverted A.2 model lock (Sonnet 4.6
labeller; Opus 4.7 high-stakes). Cost envelope returns to original
$140-$700 spec.

**Race condition note:** my Path A directive (`24494eb`, ~20:55 SAST)
was written before I saw the revert. It says "re-run A.4 with Opus
only per owner direction" — that direction has since been withdrawn.
This revision corrects.

## Path A — REVISED retry mode

| Element | Original Path A | Revised |
|---------|-----------------|---------|
| v3.2 protocol revision (Fix 1 + 2 + 3 bundled) | ✅ ACTIVE | ✅ ACTIVE (unchanged) |
| F-S5 patch (Fix 3 bundled into v3.2) | ✅ ACTIVE | ✅ ACTIVE (Pilot Orch releases hold per this revision) |
| A.4 retry mode | Opus only ($2.63) | **Parallel Sonnet+Opus ($3.04)** — Option C+ on v3.2 |
| Phase B model lock | Opus 4.7 (per owner) | **Empirical winner** (Sonnet preferred per owner revert; default to Sonnet if both PASS) |
| Phase B cost projection | $375-1875 (Opus) | $75-375 (Sonnet) — back in $700 envelope |

## Why parallel retry, not Sonnet-only

Three reasons to keep parallel testing on v3.2:

1. **Same incremental cost.** Original A.4 Option C ran $3.03; v3.2
   retry parallel is $3.04. The Opus lane gives us empirical
   confirmation that v3.2 fixes universally apply (not just to one
   model).

2. **Risk mitigation if Sonnet fails again.** If v3.2 Sonnet fails
   on the same hands, we have Opus data to know whether it's a
   protocol gap (both fail) or model-capability gap (only Sonnet
   fails). Saves a separate dispatch later.

3. **Per `feedback_quality_default_no_ask.md`:** slow/clean — get the
   full empirical picture before making the Phase B model decision.

**Decision tree post-A.4 v3.2 retry:**

| Sonnet | Opus | Phase B disposition |
|--------|------|---------------------|
| PASS | PASS | Ship **Sonnet** (cheaper; spec adequacy met; matches owner revert; cost in $140-$700 envelope) |
| PASS | FAIL | Ship Sonnet (cheaper; meets gate; Opus fail flagged for v3.x diagnosis post-pilot) |
| FAIL | PASS | Escalate to owner — Opus is the only path; cost projection $375-1875 against $700 envelope; owner decides |
| FAIL | FAIL | HARD HALT — Path D (try Protocol B/C reasoning instead of v3.x); larger discussion required |

**Default disposition under owner's reverted direction: Sonnet preferred when adequate.**

## F-S5 patch — RELEASE hold

Pilot Orchestrator's revert comm at `1fe57a2` was holding F-S5 patch
start "pending owner confirmation given active back-and-forth
(pause → resume → Opus upgrade → undo)." Per this revision +
`feedback_listen_to_orchestrator_always.md`:

**F-S5 patch (bundled in v3.2) PROCEEDS.** F-S5 is independent of
model selection — the phantom feature affects ALL labellers
regardless of Sonnet vs Opus. The patch is needed for Phase B
regardless of model lock. Pilot Orch / logic builder may release the
hold and proceed with v3.2 authoring.

## Cost envelope restored

Phase A so far: $3.03 (well under $200 cap).

Path A revised budget:
- v3.2 builder cycle: ~$0 (text edits + dispatched reviews ~$5)
- A.4 retry parallel Sonnet+Opus: ~$3.04
- A.8 trace audit + coverage audit: ~$5
- A.8 final synthesis: ~$3
- **Path A revised subtotal:** ~$16

Total Phase A projected: ~$19 of $200 cap (10%).

Phase B projected (Sonnet labeller per owner revert):
- $75-$375 against $700 envelope — within original spec
- Total pilot run target: $140-$700 unchanged

**Net cost impact of revert:** saves ~$300-1500 in Phase B vs Opus
labeller. Owner's revert is fiscally sound given Sonnet's adequacy
will be retested empirically on v3.2.

## Wall-time impact

Unchanged from original Path A:
- v3.2 builder cycle: ~30-60 min
- v3.2 PR review: ~30-45 min
- A.4 retry parallel: ~5-10 min (parallel = single wall-time)
- Trace audit + coverage audit + A.8 synthesis: ~30-45 min
- **Path A revised wall-time:** ~95-160 min from now (same)

Phase B dispatch decision still ETA ~22:00-23:30 SAST.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 49 | v3.2 protocol revision (Fix 1 + 2 + 3 bundled) | 🔥 ACTIVE — F-S5 hold RELEASED | Logic builder |
| 50 | A.4 v3.2 retry — parallel Sonnet+Opus (Option C+ on v3.2) | ⏳ QUEUED post-v3.2 merge | Pilot Orchestrator |
| 51 | Phase B revised cost projection (post-A.4 retry results) | ⏳ POST-A.4-RETRY | Pilot Orchestrator |
| 52 | A.8 synthesis (post-A.4 retry + trace audit + coverage audit) | ⏳ QUEUED | Orchestrator |

## Action items

**Logic builder (transient builder persona):**
1. Take Path A directive at `24494eb` AS REVISED HERE
2. Branch `stage4-pre-dispatch/v3-2-protocol-revision` (unchanged)
3. Apply Fix 1 + Fix 2 + Fix 3 per `24494eb` scope
4. F-S5 patch hold RELEASED — proceed with v3.2 authoring
5. PR + triple-pipeline review + merge (unchanged)

**Pilot Orchestrator:**
1. Continue holding (no Phase B dispatch); A.7 HALT in effect
2. After v3.2 merges: re-run A.4 with **parallel Sonnet+Opus on v3.2**
   (Option C+ on revised protocol — same model setup as original
   Option C, but now on v3.2 instead of v3.1)
3. Surface A.4 v3.2 retry results
4. Apply revised decision tree above to recommend Phase B disposition

**Orchestrator (me):**
1. This revision ack shipped (atomic flow next)
2. Watch for v3.2 PR drop
3. Dispatch gto-expert reviewer at v3.2 PR open
4. Post-A.4 retry: dispatch trace audit + run coverage audit
5. Compose A.8 final synthesis
6. Phase B dispatch decision per revised decision tree

**QC stream:**
- Layer 3 watch continues
- V-A4-1 ("v3.1 fails Group-D BB-flop CHECK reversals") in test corpus
- v3.2 PR will need pre-merge audit (same Path B pattern)

**Owner:**
- Revert noted; A.2 lock back to Sonnet labeller per spec
- Path A revised retry mode: parallel Sonnet+Opus on v3.2 (same cost ~$3)
- F-S5 patch (phantom feature) bundled into v3.2 — proceeds
- Default Phase B model: Sonnet preferred when v3.2 calibration adequate (matches your revert)
- Cost envelope restored to original $140-$700 spec
- ETA Phase B dispatch decision ~22:00-23:30 SAST (unchanged from original Path A)

## References

- Path A directive (this revision modifies retry mode only): `24494eb`
- Owner revert comm: `1fe57a2`
- A.7 HALT: `b2de857`
- A.8 partial synthesis (F-S5 directive — superseded by v3.2 bundle): `947f176`
- A.4 v3.1 calibration results: `review/pilot_run_2026-04-26/calibration_results_*.json`
- Memory: `feedback_quality_default_no_ask.md` (parallel retry preserves slow/clean), `feedback_listen_to_orchestrator_always.md` (owner revert direction sufficient), `feedback_no_deadlines.md` (quality > speed)

**Status: PATH A REVISED. v3.2 PROTOCOL REVISION ACTIVE WITH F-S5 BUNDLE.
A.4 v3.2 RETRY = PARALLEL SONNET+OPUS. Phase B HELD. Cost envelope
back to spec.**
