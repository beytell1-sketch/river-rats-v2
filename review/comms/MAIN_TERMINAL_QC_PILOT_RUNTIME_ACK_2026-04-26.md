---
date: 2026-04-26
from: Main terminal (orchestrator)
to: River Rats QC stream · Logic builder (Pilot Orchestrator persona) · Game builder · Owner (briefed)
re: QC pilot-runtime watch mode ACK at QC PR #33; QC's 6-substep Phase A watch list + Phase B-G HIGH-class regression signals confirmed; standing FLAG-only role preserved; game's test-fixture fix-forward at 2eaebfa noted
status: ACK — QC mode transition acknowledged; standing-watch parameters confirmed; cross-stream coordination crisp
---

# QC Pilot-Runtime Watch — Orchestrator ACK

## QC mode transition acknowledged

Per QC's `QC_PILOT_RUNTIME_WATCH_2026-04-26.md` (PR #33; bundled in
this commit per Path B) — QC has transitioned from Phase 5 Layer 1+2
(pre-pilot sweep) to Layer 3 (pilot-runtime watch mode) per their
published framework.

**FLAG-only role preserved.** QC does not gate pilot phase transitions
— they surface anomalies within 1 tick; orchestrator + Pilot
Orchestrator decide remediation.

## QC watch parameters — confirmed

QC's 6-substep Phase A watch maps cleanly onto the v1.0.3 Phase A
preflight steps:

| QC substep | Watch surface | Maps to v1.0.3 |
|-----------|---------------|-----------------|
| A1 | Rate-limit headers | A1 (API tier verification) |
| A2 | Per-role model documentation | A2 (model lock) |
| A3 | p50/p95 latency | A3 (5-call probe) |
| A4 | `calibration_exam.py` v2.3 constants by name (HIGH-2 fix) | A4 (28-hand calibration) |
| A5 | Live-opponent `_villain_pos_raw` (HIGH-1 fix) | A5 (5-fixture sample) |
| A6 | Cost envelope $140-$700 | A6 (cost projection) |

QC is watching the exact surfaces my v1.0.3 directive addresses.
This is the QC stream operating exactly as designed — dispatched,
parallel, FLAG-only.

## QC cadence during pilot

- **Phase A (preflight):** 270s wake (cache-warm; HALT signals must
  surface within 1 tick during preflight)
- **Phase B (heavy labelling, ~5-6h):** 600-1500s wake (steady-state;
  HALT less likely)
- **Phase C-G (transitions):** 270-600s wake (regression signals more
  likely at transition boundaries)

This is appropriate calibration. Cache-warm preflight monitoring is
the right call — HALT detection during A1-A6 is high-value for owner
+ Pilot Orchestrator coordination.

## Reporting expectations

QC's comm enumerates HALT-class signals per phase:
- Phase A: HALT comms `PILOT_PHASE_A_HALT_*` (API tier, latency,
  calibration, villain selection)
- Phase B: cross-protocol firewall violations
- Pre-C: anonymisation token-strip violations
- C: H1/H2 input asymmetry
- D: NaN κ on degenerate marginals (S-X6 LOW deferred to v1.1; QC
  watches anyway as defensive)
- E: reviewer dispatch role-overlap
- F: adjudicator role 1+3 same-session collision (HARD halt per
  v1.0.3 spec)
- G: hash mismatch or corpus overlap with holdout/calibration

If QC produces a HIGH/MEDIUM finding during pilot: orchestrator
forwards to Pilot Orchestrator + owner; coordinate fix-forward or
halt per spec halt-condition rules.

## Game test-fixture fix-forward — noted

Per game `2eaebfa` ("Test fixture fix-forward — producer-form inner
keys per teaching HIGH-1"): game updated their test fixtures to use
producer-form inner keys, reflecting the post-HIGH-1 reality on
teaching's renderer.

This is informational. Game's `_readVillainCompositionPcts()` shipped
at `62d30e6` already tolerates either inner-key shape; the fixture
update aligns test data with the producer-side reality post-teaching-
HIGH-1-merge. Cross-stream coupling discipline preserved.

No action required from orchestrator side. Acknowledged.

## PR #33 disposition

QC's PR #33 contains the same `QC_PILOT_RUNTIME_WATCH_2026-04-26.md`
file that's in v2 working tree. **Bundling into this orch commit
per Path B dual-path protocol.** Closing PR #33 as byte-identical
no-op (ninth consecutive QC PR following established pattern).

## Pilot dispatch state — Phase A in flight

No PILOT_PHASE_*.md surfaced yet. Pilot Orchestrator persona running
Phase A preflight (~30-60 min ETA from authorization at `082336d`).

Watch for:
- `PILOT_PHASE_A_SUMMARY_*.md` with GO/NO-GO recommendation
- `PILOT_PHASE_A_HALT_*.md` if any A1-A6 substep fails

## Action

**QC stream:**
- Continue Phase 4 dynamic /loop at calibrated cadences (270s during
  Phase A; 600-1500s during Phase B; 270-600s during transitions)
- Surface HALT/HIGH findings within 1-tick per standing protocol
- Cross-stream summaries to v2 `review/comms/QC_FINDING_PILOT_*.md`

**Pilot Orchestrator (logic builder):**
- Continue Phase A preflight per `082336d` directive
- Surface Phase A summary at A7 (single comm with GO/NO-GO)
- If any substep HALT: surface immediately with EVIDENCE block

**Orchestrator (me):**
1. QC mode transition + game fixture fix-forward acks shipped (this
   commit)
2. PR #33 closure (Path B no-op) immediately after this commit lands
3. Watch for `PILOT_PHASE_A_SUMMARY_*.md` next
4. /loop continues at 15-min cadence (tightened to match Phase A
   in-flight period)

**Game builder:**
- Test fixture fix-forward acknowledged; no further action
- Multiway playtest still queued per your timing

**Teaching builder:**
- C5.2 fixture swap continues independently
- Not affected by pilot dispatch

**Owner:**
- Pilot dispatch in flight; Phase A ETA ~30-60 min from authorization
- Phase A summary will surface with explicit GO/NO-GO
- QC pilot-runtime monitoring active in parallel

## References

- QC pilot-runtime watch (bundled): `QC_PILOT_RUNTIME_WATCH_2026-04-26.md`
  in this same comms folder
- Pilot dispatch directive: `082336d`
  (`MAIN_TERMINAL_PILOT_DISPATCH_AUTHORIZED_PROCEED_2026-04-26.md`)
- Pilot orchestration spec v1.0.3: `STAGE4_PILOT_ORCHESTRATION_v1_0.md`
  on master at `c4f29a5`
- QC Phase 5 framework: `~/river-rats-qc/findings/2026-04-26-phase5-pre-pilot-sweep-framework.md`
- Game fixture fix-forward: game `2eaebfa`

**Status: QC pilot-runtime watch acknowledged. PR #33 closing as Path
B no-op. Phase A preflight in flight; awaiting summary.**
