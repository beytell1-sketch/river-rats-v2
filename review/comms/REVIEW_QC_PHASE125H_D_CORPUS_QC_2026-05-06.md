---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (for 12.5H-E builder cleanup window)
re: Phase 12.5H-D — corpus QC sweep on 694-hand combined corpus — APPROVE; 0 NIT new (3 prior NITs ride along)
severity: clean approval; no findings
status: FLAG → APPROVE; 12.5H-E re-train unblocked
test-class: design §7 G1-G4 + NEW G5 cap-binding pre-flight (TC-X-CAP-BINDING-PRE-CHECK first-corpus-scope activation) + design_action verification (TC-X T8 schema gap fix first measurable activation)
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 13th successive cycle solo-routed)
---

# QC Review — 12.5H-D corpus QC sweep (694-hand combined corpus): APPROVE

## Verdict

**APPROVE 12.5H-D corpus state.** All 5 gates PASS — cleanest corpus QC verdict in the 12.5H cycle.

**Two QC institutional curative validations achieved this audit:**
1. **TC-X T8 schema gap fix (from PR #150 NIT) — first empirical activation: 20/20 = 100% T-CONTROL design_action match.** The schema-level fix produces perfect drift-detection on first measurable run.
2. **TC-X-CAP-BINDING-PRE-CHECK — first corpus-scope activation.** Computed pre-flight confirms 694-hand corpus remains cap-non-binding (max boost 1.757× < cap=3.0). Forward-active for any future cap-tuning consideration.

3 prior-cycle NITs documented for 12.5H-E builder cleanup window per dispatch §"Cleanup items".

**12.5H-E re-train unblocked.** Orchestrator dispatches per sequencing line 56.

QC FLAG-only role per CLAUDE.md.

## Gate G1 — join-cardinality ✅ CLEAN

| Quantity | Observed | Expected |
|---|---|---|
| Old 604 unique `pilot_hand_id` | 604 | 604 ✓ |
| New parametric (12.5H-B') unique | 84 | 84 ✓ |
| New manual canonicals (12.5H-B') unique | 6 | 6 ✓ |
| Combined situations unique | **694** | 694 ✓ |
| Old ∩ new collisions | **0** | 0 ✓ |
| Combined labels unique | **694** | 694 ✓ |
| Situations ∩ labels | 694 | 694 ✓ (perfect join) |
| Situations \\ labels | 0 | 0 ✓ |
| Labels \\ situations | 0 | 0 ✓ |

**G1 CLEAN.**

## Gate G2 — distribution sanity ✅ CLEAN

### Combined 694-hand consensus_action distribution

| class | count | % | flag |
|---|---|---|---|
| FOLD | 79 | 11.4% | ✓ |
| CHECK | 295 | 42.5% | ✓ |
| CALL | 79 | 11.4% | ✓ |
| BET | 137 | 19.7% | ✓ |
| **RAISE** | **104** | **15.0%** | ✓ (design §4 prediction = 13.5%; achieved + slightly exceeded) |

All 5 classes >5% ✓. **RAISE class shifts 11.3% (12.5E baseline) → 15.0% (post-12.5H) = +3.7pp.** Design §4 predicted +2.2pp; achieved +3.7pp (RAISE-density slightly higher than predicted, consistent with T10' + T-RAISE-stabilize + T7-ext SUITED-NFD-with-air design intent).

### Median consensus_confidence (cohort comparison)

| Cohort | Median |
|---|---|
| Old 604 | 1.00 |
| New 90 | 1.00 |

Median preserved across cohorts ✓. No degradation; design-intent improvement on labeller agreement (template specificity).

**G2 CLEAN.**

## Gate G3 — cross-cohort dedup ✅ CLEAN

Strict fingerprint (board + hero_cards + prior_actions + hero_position + street): **0 collisions** between old 604 + new 90. Builder PR #169/#175 self-checked + QC re-verifies at corpus scope.

**G3 CLEAN.**

## Gate G4 — labeller-drift detection ✅ CLEAN — TC-X T8 schema gap fix achieves 100% match

### T-CONTROL design_action verification (NEW G4 implementation)

Per dispatch line 35 (per TC-X T8 schema gap fix from PR #150): T-CONTROL hands now encode `design_action` per row; same-action match threshold ≥70%.

| Quantity | Observed | Expected | Match |
|---|---|---|---|
| T-CONTROL hands in 12.5H corpus | 20 | 20 | ✓ |
| T-CONTROL hands with `design_action` field | **20/20** | 20/20 | ✓ all encoded |
| **T-CONTROL same-action match** | **20/20 = 100.0%** | ≥70% | ✅ **PERFECT** |
| Mismatches | 0 | (any documented) | ✓ none |

**This is the first empirical activation of the TC-X T8 schema gap fix from PR #150 NIT.** The schema fix produces perfect drift-detection on first measurable run. The same audit class would have been INDETERMINATE (as it was at 12.5E-D) without the design_action field. Curative confirmed working at first measurement.

### Per-class confidence-Δ (G4 secondary check)

| class | old mean | new mean | Δ | within ±0.15? |
|---|---|---|---|---|
| BET | 0.885 | 0.989 | +0.105 | ✓ |
| CALL | 0.900 | 1.000 | +0.100 | ✓ |
| CHECK | 0.918 | 0.883 | -0.035 | ✓ |
| FOLD | 0.955 | 1.000 | +0.045 | ✓ |
| **RAISE** | 0.788 | 0.928 | **+0.140** | ✓ (just under 0.15 threshold) |

All 5 classes within ±0.15 threshold ✓. RAISE shift (+0.140) is the largest signal — design-intended drift from template specificity (T10' MW-45 monsters + T-RAISE-stabilize MW-47 + T7-ext SUITED-NFD with air ≥ 0.20 produce dense pattern-locked RAISE situations with high labeller agreement).

This is a substantially tighter result than 12.5E-D's RAISE +0.292 because:
- 12.5H corpus is more pattern-locked than 12.5E-B (T10' / T-RAISE-stabilize / T7-ext have explicit MW-XX targeting; 12.5E was T1-T7 with mixed-bucket patterns)
- v3.4 protocol (with Fix 2.1.1 clause-e floor) gives labellers a clearer discriminator than v3.3
- Combined effect: tighter consensus, narrower confidence shift

**G4 CLEAN.** Drift documented + below threshold; T-CONTROL design_action match perfect.

## Gate G5 (NEW) — cap-binding pre-flight ✅ CLEAN — TC-X-CAP-BINDING-PRE-CHECK first corpus-scope activation

Per dispatch line 38 + per QC's TC-X-CAP-BINDING-PRE-CHECK class (queued 2026-05-05; promoted to design gate in 12.5H-A; first corpus-scope activation here).

| Quantity | Value |
|---|---|
| Class counts | FOLD 79 / CHECK 295 / CALL 79 / BET 137 / RAISE 104 |
| Mean class count | 138.8 |
| Min class count (FOLD or CALL — tied at 79) | 79 |
| Max natural per-class boost | **1.757×** |
| vs cap=3.0 | **NON-BINDING** (cap > 1.757; sweep would be no-op) |

This confirms — at 694-hand corpus level — that any future cap-sweep consideration (e.g. 12.5G-equivalent post-12.5H-F) would still produce identical models at cap=3.0 vs cap=4.0. Cap-as-lever remains empirically refuted.

**Forward-actionable:** at 12.5H-E re-train + 12.5H-F gate evaluation + any post-evaluation 12.5I+ planning, this pre-flight result is the canonical reference for "is cap-tuning a viable lever?" Answer: no, until corpus class distribution changes substantially.

**G5 CLEAN.**

## Cleanup items documented (3 prior-cycle NITs ride along to 12.5H-E)

Per dispatch §"Cleanup items":

1. **PR #139 NIT-1**: PLAN §3.T8 wording reconciliation. Now superseded by 12.5H-A's design (90 hands across 6 templates ≠ 12.5E §3 T8 enumeration); the 12.5E PLAN §3.T8 NIT is mostly obsolete but the wording cleanup ride-along still applies.
2. **PILOT_595 design_note cosmetic** (TPTK→top-two-pair): 12.5E-C era artefact; ride-along at 12.5H-E.
3. **PR #148 NIT-1** (BUILDER_REPORT preserved-original stale filename): ride-along at 12.5H-E.

Plus newer NITs accumulated this cycle:
- **PR #169 NIT-1** (12.5H-A design §3/§4/§8 T-CONTROL count inconsistency): part of TC-X-DISPATCH-PREDICTION-VERIFICATION 3-instance pattern; formalized as test class. Could be cleaned at 12.5H-E if scope permits.
- **PR #175 MEDIUM-1** (PILOT_693 dispatch CALL-vs-RAISE prediction error): orchestrator post-merge updated 12.5H-C re-pilot predictions per PR #178 — closed.
- **PR #181 MEDIUM-1** (PILOT_692 dispatch CALL-vs-RAISE prediction error): same family; orchestrator-side update suggested at 12.5H-E synthesis or beyond.

## QC institutional curative validations achieved this audit

This 12.5H-D sweep is significant for QC's institutional memory — **two of three formalized test classes from this cycle achieve their first measurable activation here:**

### TC-X T8 schema gap fix (from PR #150 NIT, queued in `curative_additions_log.md`) — FIRST MEASURABLE ACTIVATION
- 12.5E-D had this audit as INDETERMINATE (no design_action field; aggregate-class best-case 68.2% < 70%)
- 12.5H-D has this audit as **PERFECT 100% match** (20/20 T-CONTROL hands)
- Schema fix works as designed; drift-detection now precise

### TC-X-CAP-BINDING-PRE-CHECK (queued 2026-05-05 from 12.5G empirical refutation) — FIRST CORPUS-SCOPE ACTIVATION
- Pre-flight computation produces 1.757× < cap=3.0 → cap-non-binding confirmed at 694-hand scale
- Forward-active for any future cap-tuning workstream consideration

(Note: TC-X-CROSS-SEED-IMPORTANCE will activate next at 12.5H-E re-train when cross-seed importance reporting is required by trainer report contract.)

## What QC did NOT audit (scope partition)

- **Per-hand label correctness review** — orchestrator's PR #184 Opus tier-up cross-check did this (LABELS FINAL 20/20 agreement)
- **12.5H-E trainer module readiness** — out of 12.5H-D scope
- **12.5H-F gate evaluation forecasting** — orchestrator/owner scope at 12.5H-F synthesis

## Test class implication

- **TC-X T8 schema gap fix curative VALIDATED** — perfect first-activation result (100% match). Pattern reproducible: schema-level-curative-from-NIT → operationalize-in-design → measure-on-first-corpus → confirm-curative-works.
- **TC-X-CAP-BINDING-PRE-CHECK first corpus-scope activation** — confirms cap-non-binding at 694-hand scale; forward-active.
- **G4 drift-classification pattern continues** — distinguish design-intended distributional shift (RAISE +0.140) from labeller-drift regression. Pattern stable.
- **Cleanest corpus QC verdict so far in 12.5H cycle** — 0 new NITs; all gates clean; 2 institutional curatives validated. Process is working.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **13th successive cycle solo-routed**. Loop heartbeat detected dispatch within ~1-2 min of master push (loop fired immediately on `/loop` invocation). Dynamic /loop self-pacing continues working as designed.

## References

- Dispatch: `MAIN_TERMINAL_PHASE125H_D_DISPATCH_2026-05-06.md` (master `026adf8`, PR #185)
- 12.5H-C LABELS FINAL: master `690ca8f` (PR #184)
- 12.5H-C labelling round merged: master `90e17dc` (PR #181)
- 12.5H-C QC verdict (TC-X formalization): master `14ac162` (PR #183)
- 12.5H-A design: master `858b032` (PR #165)
- 12.5E-D precedent: master `4070a11` (PR #150) — original T8 schema gap NIT
- TC-X T8 schema gap fix curative: `~/river-rats-qc/learning/curative_additions_log.md` (originating NIT in PR #150 finding)
- TC-X-CAP-BINDING-PRE-CHECK class: `~/river-rats-qc/learning/test_class_registry.md` (queued 2026-05-05)
- TC-X-DISPATCH-PREDICTION-VERIFICATION class (formalized 2026-05-06): same registry
- Memory: `feedback_qc_routing_when_standalone_active.md` (13th cycle), `feedback_explicit_action_trigger.md`, `feedback_qc_required_before_approval.md`

## Status

**APPROVE 12.5H-D corpus state.** All 5 gates clean; 0 new NITs; 3 prior NITs ride along; 2 QC institutional curatives validated this audit (TC-X T8 schema gap fix → 100% match; TC-X-CAP-BINDING-PRE-CHECK → cap-non-binding confirmed at 694-hand scale).

**12.5H-E re-train unblocked.** Orchestrator dispatches per sequencing line 56.
