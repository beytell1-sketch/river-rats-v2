---
date: 2026-05-10
from: LEAD-PROGRAMMER (builder; architect-hat for trainer adaptation)
to: Main terminal (orchestrator) · Owner (informational)
re: Phase 1.5-D.4 dispatch (PR #364) — surface observation: 30-hand HU reference eval infrastructure gap; orchestrator decision needed on methodology before builder fires smoke
status: OBSERVATION — surface BLOCKED-on-scope-decision per CLAUDE.md §5 + `feedback_orchestrator_decides_not_recommends.md`
---

# Phase 1.5-D.4 — surface 30-hand HU reference eval infrastructure gap

## Observation

Per dispatch §"Smoke gate" the smoke score is "smoke score on 30-hand HU reference vs v8-HU-38 evaluated on same 30 hands". The dispatch presumes:
1. A structured 30-hand HU reference eval data file (analog to MULTIWAY's `BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md` parsed by `reference_evaluator.parse_reference_hands`)
2. An evaluator path that loads model + runs each of 30 hands + compares predicted-vs-expected
3. A v8-HU baseline computable on the same 30 hands

**Found state (verified by source read):**

- `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + `HU_AXIS_{1..6}.md` — design markdown only, prose form; NO structured action-key table
- `data/hu_corpus/pilot_50_v2/consensus.jsonl` (50 rows) — HU-1 LOOKALIKES only (LK-XX format); the 5 HU-1.x ANCHORS themselves not in this file
- `data/hu_corpus/full_HU2_HU6/consensus.jsonl` (696 rows) — HU-2..HU-6 LOOKALIKES only; the 24 anchors HU-2.1..HU-6.4 not in this file
- HU-6.5 anchor — owner-adjudicated CALL per PR #338; not in either consensus.jsonl
- `scripts/hu_anchors_axes_2_6.py` — anchor specifications (24 entries; HU-2.1..HU-6.4); contains hero+board+composition+axis+action_summary but NO `expected_action` field
- HU-1 axis anchors (HU-1.1..HU-1.5) — no Python anchor file found; design markdown only
- `river-rats-core/reference_evaluator.py:parse_reference_hands` — parses MW-XX format only, requires `BATCH2_8_RANGE_ANALYSIS.md`-format GTO action table; no HU equivalent

**Implication:** Builder cannot compute "smoke score on 30-hand HU reference vs v8-HU on same 30 hands" without first building eval infrastructure that:
- Either (A) produces a 30-row HU reference JSONL with structured `expected_action` field per hand
- Or (B) extends `reference_evaluator` to parse HU markdown design files
- Plus (C) wires up evaluator + v8-HU comparison

This is significant scope expansion not explicitly covered by dispatch §"Builder deliverables PR 1 (smoke)".

## Builder recommendations (architect-hat; orchestrator decides)

**Option A: Builder extracts `expected_action` from design markdown narrative + creates minimal eval infra inline (PR1 scope expansion).**

Approach: Each design markdown hand spec has a decision-class narrative implying an expected action (e.g., HU-2.1 "Nut FD + overcards, IP semi-bluff **bet**"). Builder reads all 30 markdown hand-specs + extracts expected_action manually (~30min); creates `data/hu_reference_30_2026-05-10.jsonl` with hero/board/feat_dict-context/expected_action; wires up minimal evaluator script in PR1.

Risk: builder-extracted expected_action lacks owner/architect QA; may differ from what owner intended for the eval gate. CLOSE hands have multiple GTO-acceptable actions; pinning a single expected_action arbitrarily creates ground-truth that may not match the gate spirit.

Wall-clock add to PR1: ~1-2 hr.

**Option B: Surface to architect for separate eval-infra dispatch (1.5-D.0' or 1.5-D.4-prep) BEFORE 1.5-D.4 fires.**

Approach: Architect produces (a) `design/hu_reference_set/HU_30_RANGE_ANALYSIS.md` action-key file (analog to `BATCH2_8_RANGE_ANALYSIS.md`) with owner-confirmed expected action per hand, (b) HU parser extension in `reference_evaluator.py`, (c) HU evaluator wrapper. Then 1.5-D.4 builder fires on solid eval foundation.

Risk: introduces extra round-trip; delays 1.5-D.4 by ~1-2 hr orchestrator+architect time. But establishes durable eval infrastructure usable for 1.5-D.4 + 1.5-E + future HU retrains.

Wall-clock total: ~2-4 hr (orchestrator+architect dispatch + eval infra PR + builder data-layer + 1.5-D.4 PR1).

**Option C: Use proxy eval (held-out subset of 746 corpus) for smoke; defer 30-hand reference eval to PR2.**

Approach: For SMOKE only, evaluate on a held-out 30-hand random sample of the 746 training corpus (or a balanced 30-hand sample of unique anchors). PR2's full ship-gate (≥28/30) still uses the proper 30-hand HU reference set (built via Option A or B by then).

Risk: smoke gate becomes a weaker signal (in-distribution eval rather than reference-set eval); could miss out-of-distribution failures the 30-hand reference would catch. BUT the smoke gate is itself "5pts below baseline" not "absolute pass" so the proxy may still be usable.

Wall-clock add to PR1: ~30min.

**Builder recommendation (architect-hat):** **Option B**. The eval infrastructure is durable + load-bearing for the SHIP-gate (≥28/30 hard-committed per design memo §4.6). Building it via owner-confirmed action key is higher quality than builder-improvised extraction. Per `feedback_quality_default_no_ask.md` slow/quality path. Per `feedback_pilot_first_for_long_jobs.md`: invest in solid pilot infrastructure before scaling.

If orchestrator prefers velocity over-quality: **Option A** with builder-extracted expected_action subject to QC review of the 30-row JSONL before smoke gate is computed.

## What builder will do while orchestrator decides

- WAIT for orchestrator decision (Option A / B / C / Other)
- Per `feedback_named_author_builds_not_polls.md` and `feedback_explicit_action_trigger.md`: builder named in dispatch but the actionable HOW depends on this scope question
- Per `feedback_dont_surface_terminal_liveness_to_owner.md`: this surface goes to orchestrator, NOT owner

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master`: MATCH `a3fb9f3` ✓ (44-arbs adjudication merged)
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.4 dispatch: master `<UNKNOWN — dispatch not yet on master at time of writing>`; comm path `review/comms/MAIN_TERMINAL_PHASE15D4_HU_RETRAIN_DISPATCH_2026-05-10.md`; PR #364
- Architect's design memo §4.5 + §4.6 (ship gate ≥28/30): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- HU 30-hand reference design (markdown only): `design/hu_reference_set/HU_30_HAND_DESIGNS.md`
- Multiway analog: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md`
- Reference parser: `river-rats-core/reference_evaluator.py:parse_reference_hands`
- Anchor data (HU-2..6): `scripts/hu_anchors_axes_2_6.py`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_explicit_action_trigger.md`, `feedback_verify_source_not_plan.md`, `feedback_named_author_builds_not_polls.md`

**Status: BLOCKED-on-scope-decision per CLAUDE.md §5 STOP > improvise. Builder grounded in source (read v9_student trainer pattern + reference_evaluator + HU design markdown + anchor py + corpus jsonl); confirmed 30-hand HU reference eval infrastructure does NOT exist on master. Awaits orchestrator selection of Option A / B / C / Other.**
