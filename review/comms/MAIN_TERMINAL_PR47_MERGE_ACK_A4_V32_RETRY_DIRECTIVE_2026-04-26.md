---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Pilot Orchestrator (logic builder reactivates Pilot Orchestrator persona post-merge) · Owner (briefed) · QC stream
re: PR #47 (v3.2 protocol revision: Fix 1 + 2 + 3 bundled) MERGING after triple-reviewer convergent APPROVE; A.4 v3.2 retry directive issued — parallel Sonnet+Opus on revised protocol per Path A revision
status: MERGE ACK + A.4 RETRY DIRECTIVE — v3.2 ships clean; Pilot Orchestrator re-runs A.4 with parallel Sonnet+Opus on v3.2 (Option C+ pattern); per revised decision tree default Phase B = Sonnet if PASS
---

# PR #47 Merge ACK + A.4 v3.2 Retry Directive

## Triple-reviewer convergence — APPROVE clean

| Pipeline | Verdict | Findings |
|----------|---------|----------|
| Builder reviewer (5972035) | APPROVE post-fix-forward | HIGH (Rule 11 predicate too narrow) + MED (`nut_flush_block` not real feature) + 2 NITs all resolved at PR commit `5188299`; Rule 11 broadened to `is_made_hand=1` covering TPWK; BET exception (a) tightened to require BOTH `villain_TP+>=0.40` AND (`is_strong_made=1` OR `is_monster=1`) so TPWK can't escape; self-test confirms all 4 anchors (d3688/d9556/d3178/MW-39) route correctly |
| QC pre-merge audit (PR #48) | APPROVE clean | 14th successive QC audit clean across the day's pre-pilot work |
| Orchestrator gto-expert reviewer | APPROVE-WITH-NITS | All 5 sub-checks per Fix PASS; 2 LOW nits (2-tone-flush state-space could enumerate flush-completing turn/river more explicitly; MW-39 self-flagged for future addition to `calibration_exam.py` constants); merge as-is recommended |

**Convergent verdict — all three pipelines independently confirm:**
- **Fix 1 (Rule 11):** GTO-sound paired-board CHECK exception (caps villain to bluff-catchers; CHECK extracts via induced bluff-catches vs BET-protect which has nothing to protect against on capped paired boards). 2 EXCEPT clauses + 5 carve-outs (HU/IP/dry/river-checked-to/drawing) preserve d3178 AA-checked-to-river BET via the river-checked-to carve-out
- **Fix 2 (KB §1.7 OVERRIDE):** `villain_air_pct >= 0.20` threshold sound; CALL below; MW-30 anchor citation correct (villain_air=0.15 insufficient); supplements rather than edits standalone KB
- **Fix 3 (F-S5 phantom feature):** Phantom `hero_top_pair_plus_pct` removed from substantive guidance; replacement uses bucket + `prior_actions` (existing features); pilot + design byte-equivalent; 3-axis Step 2 structure preserved
- **No breaking changes:** all 7 calibration anchors preserved via carve-outs; cross-protocol consistency preserved (no Protocol C edits)

## Merge decision

**MERGE PR #47 AS-IS.** Triple-pipeline APPROVE clean with empirical anchors verified (4/4 route correctly post-fix-forward). 2 LOW nits deferred to v1.0.x housekeeping. No HIGH/MEDIUM blockers.

## A.4 v3.2 RETRY DIRECTIVE

Per Path A revised decision tree at master `5cc7ba1`:

**Pilot Orchestrator (reactivates persona post-PR-#47 merge):**

1. **Re-run A.4 calibration on v3.2 with parallel Sonnet+Opus (Option C+ pattern):**
   - Same 38-hand exam (28 standard + 10 reversal) per `calibration_exam.py` v2.3 constants
   - Same answer key (Pilot Orchestrator-private; not visible to labeller agents)
   - Both Sonnet 4.6 + Opus 4.7 lanes in parallel
   - Use v3.2 protocol (NEW `prompts/gto_labeller_v3.2.md` at master post-merge)
   - Cost target ~$3.04 (matches original A.4 Option C run; Sonnet ~$0.41 + Opus ~$2.63)
   - Wall-time target ~5-10 min (parallel = single wall-time)

2. **Halt thresholds (preserved from original Option C):**
   - Sonnet > $80 → HALT
   - Opus > $200 → HALT
   - Total > $200 → HALT
   - Both calibration FAIL → HARD HALT, escalate

3. **Decision tree post-A.4 v3.2 retry:**

| Sonnet | Opus | Phase B disposition |
|--------|------|---------------------|
| PASS | PASS | Ship **Sonnet** (cheaper; spec adequacy met; matches owner revert; Phase B cost ~$75-375 in $700 envelope) |
| PASS | FAIL | Ship Sonnet (cheaper; meets gate; Opus fail flagged for v3.x diagnosis post-pilot) |
| FAIL | PASS | Escalate to owner — Opus only path; cost projection $375-1875 against $700 envelope; owner decides |
| FAIL | FAIL | HARD HALT — Path D (try Protocol B/C reasoning instead of v3.x); larger discussion required |

4. **Surface A.7 v3.2 summary** with empirical results + per-hand comparison vs A.4 v3.1 results (specifically: do d3688/d9556/MW-39 now route correctly?)

5. **Phase B remains HELD** until orchestrator confirms A.7 v3.2 GO + (if needed) owner envelope decision.

## What v3.2 expected to fix empirically

The 3 v3.1 failures should now route correctly:

| Hand | v3.1 result | v3.2 expected | Why |
|------|-------------|--------------|-----|
| d3688_BB_flop (8cKc TPWK on KdTd4s 2-tone-flush) | Sonnet+Opus BET; expert CHECK | CHECK | Rule 11 EXCEPT (b) 2-tone-flush OOP + multi-villain; predicate now covers TPWK via `is_made_hand=1` |
| d9556_BB_flop (5h5d full house on 5s6d6h paired) | Sonnet+Opus BET; expert CHECK | CHECK | Rule 11 EXCEPT (a) paired-board capped villain; predicate covers monster via `is_made_hand=1`; BET exception (a) NOT triggered (villain_TP+ on paired 5s6d6h is low) |
| MW-39 (AhJh nut FD on Kh8h3d) | Sonnet+Opus RAISE; expert CALL | CALL | KB §1.7 OVERRIDE: `villain_air_pct = 0.05 < 0.20` → CALL preferred |

**If d3178 AA-checked-to-river spot also tested:** must still BET (via river-checked-to carve-out).

## QC PR #48 — Path B bundle

QC's audit comm (`QC_PRE_MERGE_AUDIT_PR47_2026-04-26.md`) bundled into orch commit per Path B. Closing PR #48 as no-op after this commit lands.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 49 | v3.2 protocol revision (PR #47) | ✅ SEALING — this commit | Logic builder |
| 50 | A.4 v3.2 retry — parallel Sonnet+Opus | 🔥 ACTIVE — this directive | Pilot Orchestrator |
| 51 | Phase B revised cost projection (post-A.4 retry) | ⏳ POST-A.4-RETRY | Pilot Orchestrator |
| 52 | A.8 final synthesis (post-A.4 retry + trace audit + coverage audit) | ⏳ QUEUED | Orchestrator |
| 53 | F-PR47-N1 NIT (2-tone-flush state-space enumeration) | ⏳ DEFERRED v1.0.x housekeeping | Logic builder |
| 54 | F-PR47-N2 NIT (MW-39 add to calibration_exam.py constants) | ⏳ DEFERRED v1.0.x housekeeping | Logic builder |

## Action

**Pilot Orchestrator (logic builder reactivates Pilot Orchestrator persona):**
1. Build persona pauses post-PR-#47 merge (this commit triggers it)
2. Reactivate Pilot Orchestrator persona
3. Re-run A.4 calibration with parallel Sonnet+Opus on v3.2 protocol
4. Surface A.7 v3.2 summary with per-hand comparison vs v3.1 (especially d3688/d9556/MW-39 routing)
5. If GO + Sonnet PASS → standby for orchestrator Phase B confirmation
6. If GO + only Opus PASS → escalate envelope decision via comm
7. If NO-GO → HALT, escalate Path D

**Orchestrator (me):**
1. PR #47 merge + close PR #48 + this ack + A.4 directive shipped (this commit)
2. Watch for A.7 v3.2 summary (~5-10 min ETA)
3. On GO: confirm Phase B dispatch (Sonnet default per owner revert)
4. On NO-GO: surface to owner; coordinate Path D
5. /loop continues at 10-min cadence during A.4 v3.2 retry

**QC stream:**
- Continue Layer 3 watch
- A.4 v3.2 retry is high-value monitoring point (V-A4-1 vector specifically tests this)
- Same Path B bundle pattern for any pre-merge audits

**Owner:**
- v3.2 PR shipped clean (triple-reviewer convergent APPROVE)
- Builder caught + fixed Rule 11 predicate gap (TPWK not covered) before reviewer dispatch — strong builder-side QC
- A.4 v3.2 retry begins NOW (~5-10 min wall-time)
- Default Phase B disposition: Sonnet labeller per your revert; cost in $700 envelope
- A.7 v3.2 summary expected ~21:35-21:45 SAST

## References

- PR #47: `https://github.com/beytell1-sketch/river-rats-v2/pull/47`
- PR #48 (QC audit, Path B bundled): `review/comms/QC_PRE_MERGE_AUDIT_PR47_2026-04-26.md`
- gto-expert verdict: `review/comms/REVIEWER_GTO_EXPERT_PR47_2026-04-26.md`
- Builder reviewer: master `5972035`
- Builder fix-forward: PR #47 commit `5188299`
- Path A directive: `24494eb`; revision: `5cc7ba1`
- A.4 v3.1 HALT (empirical motivation): `b2de857`
- v3.2 protocol: `prompts/gto_labeller_v3.2.md` (post-merge master HEAD)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_solver_findings.md`, `feedback_listen_to_orchestrator_always.md`

**Status: PR #47 MERGING. v3.2 PROTOCOL SEALED. A.4 v3.2 RETRY DIRECTIVE
ACTIVE. Pilot Orchestrator re-runs calibration with parallel Sonnet+Opus
on revised protocol. ETA A.7 v3.2 summary ~21:35-21:45 SAST.**
