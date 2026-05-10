---
date: 2026-05-10
from: Main terminal (orchestrator; owner-adjudication relay + 1.5-D.3 dispatch)
to: LEAD-PROGRAMMER (architect-hat lead for 1.5-D.3) · QC stream · Owner (ratification record)
re: (a) HU-6.5 owner adjudication = CALL with solver-verification flag pending; (b) Phase 1.5-D.3 (HU corpus assembly) dispatch
status: ADJUDICATION + DIRECTIVE — fire LEAD-PROGRAMMER on 1.5-D.3 — fire now
---

# (a) HU-6.5 owner adjudication

## Spot

Phase 1.5-D.2 FULL (PR #335 merged at master `6f08432`) routed HU-6.5 to owner-arbitration:
- **Sonnet 5-labeller majority (3-2): CALL**
- **Opus tier-up: FOLD**

Per dispatch consensus rule (`MAIN_TERMINAL_PHASE15D2_HU_LABELLING_PIPELINE_DISPATCH_2026-05-10.md` §"Consensus rule"): 3-2 with research (Opus) contradicting majority → owner-arbitration.

## Spot detail (full hand)

- **Hero**: Qd9h (BTN, 100bb effective)
- **Board**: 7h 6c 5s 2d 8d (river)
- **Action**: BTN opens 2.5bb → BB calls. Flop 7h6c5s: BB checks → BTN bets 1.4bb (25%) → BB calls. Turn 2d: BB checks → BTN bets 2.7bb (33%) → BB calls. River 8d: **BB leads 20.6bb (150% pot overbet)**. Hero faces decision.
- **Pot odds**: 37.5% required to call
- **Hero's hand**: nut straight 5-6-7-8-9 (9-high) on flush-completing runout (board has 2d/8d). Qd is a weak diamond blocker.

## Owner decision

**Final label: CALL.** Reason (per owner): "probably a very close call. but still a call."

Solver verification flag: solver currently offline; **flag this spot for solver review when available** to validate the call vs the Opus FOLD recommendation.

## Effect on consensus.jsonl

The data already records consensus = CALL (per Sonnet majority); this comm ratifies that consensus per owner judgment with a SOLVER-VERIFICATION-PENDING annotation. No re-write of consensus.jsonl needed; the annotation lives here in the orchestrator-record + propagates into 1.5-D.3 corpus assembly with a flag for the spot.

## Solver-verification queue (recurring annotation pattern)

Spots flagged for solver verification when solver is back online:
- **HU-6.5 (this comm)**: nut-straight-on-flush-completing-river facing 150% lead-overbet; bluff-catch threshold; owner CALL adjudication; verify against solver overbet-response equilibrium.

Future owner-adjudicated spots should append to this section as the workstream proceeds.

---

# (b) Phase 1.5-D.3 dispatch — HU corpus assembly

## Context (state at this dispatch)

Phase 1.5-D.2 fully merged at master `6f08432`:
- PR #332 PILOT (HU-1 5/5 unanimous) → master `bed7368`
- PR #334 QC PASS · 0/0/0 → master `1a644ea`
- PR #335 FULL (HU-2..HU-6 24 consensus + 1 owner-arbitrated) → master (just merged)
- PR #337 QC PASS · 0/0/0 → master `6f08432` (just merged)
- HU-6.5 owner adjudication = CALL (this comm)

This dispatch fires Phase 1.5-D.3 as the THIRD sub-sub-phase of Phase 1.5-D (HU re-train cascade): assemble HU corpus per architect's design memo §4.4.

## LEAD-PROGRAMMER (architect-hat lead) — fire now

You are authorized to fire Phase 1.5-D.3 per design memo §4.4 (in master). Architect-hat designs the lookalike-generation pipeline; programmer-hat implements `scripts/generate_hu_situations.py`; ml-architect-hat consults on similarity-band feature-distance threshold.

### Single committed scope: design memo §4.4 in master

The architect's §4.4 IS the binding spec. Do not re-design; execute.

- **Target corpus size**: 750 HU labelled situations (architect commits per §4.4; 30 reference-spot lookalikes × 25 = 750)
- **Reference spots**: 30 hands × 6 axes from `design/hu_reference_set/` (in master since 1.5-D.1)
- **Generation pipeline** (mirror 12.5K Lever C → assembly pattern):
  - New file: `scripts/generate_hu_situations.py` — draws from the 30 reference spots, varies (board run-out / position / SPR / villain action sequence) to produce ~3000 HU situations
  - Filter to ~750 via similarity-band selection: each reference spot anchors ~25 situations within feature-space distance threshold
  - Architect commits to exact distance threshold based on close-hand-selection analysis on **v9-3way-on-59 model uncertainty surface** (β anchor per α/β resolution)
  - Label all 750 through the §4.3 pipeline (5-labeller consensus + Opus tier-up)
  - Assemble into `data/corpus_hu_750_2026-05-10.jsonl` + matching labels file

### Pilot+full split per STANDING RULE (`feedback_pilot_first_for_long_jobs.md`)

- **Pilot batch**: 50 HU situations from the HU-1 pilot batch axis. Run through generation → labelling → consensus → solver verification on disagreements (when solver returns online).
- **Gate**: 50-hand pilot produces ≥ 80% labeller-consensus rate AND solver-verified consensus matches majority on ≥ 90% of solver-checked spots (solver-check held until solver returns; until then, gate is "≥ 80% labeller-consensus rate" only — flag solver-pending hands).
- **Full 700 fires only after pilot clears the gate.**

### Output (in PR diff — pilot first, then full after gate)

Pilot batch (1.5-D.3-pilot PR):
1. `scripts/generate_hu_situations.py` — generation script
2. `data/hu_corpus/pilot_50/situations.jsonl` — 50 generated situations
3. `data/hu_corpus/pilot_50/raw_labels.jsonl` — 5 labellers × 50 = 250 outputs
4. `data/hu_corpus/pilot_50/consensus.jsonl` — 50 hands × consensus
5. `data/hu_corpus/pilot_50/calibration_results.jsonl` — 5 labellers × calibration
6. `data/hu_corpus/pilot_50/opus_tier_up.jsonl` — Opus tier-up on non-unanimous
7. `data/hu_corpus/pilot_50/similarity_distance_audit.jsonl` — per-spot similarity-band assignment evidence
8. `review/comms/BUILDER_REPORT_PHASE15D3_PILOT_2026-05-10.md` — execution log + gate result + similarity-threshold rationale

Full batch (1.5-D.3-full PR; ONLY after pilot gate clears):
9. `data/hu_corpus/full_700/situations.jsonl` — 700 generated situations (or sized per pool-filter result, target ~700)
10. `data/hu_corpus/full_700/raw_labels.jsonl` — 5 labellers × 700 = 3500 outputs
11. `data/hu_corpus/full_700/consensus.jsonl` — 700 hands × consensus + confidence
12. `data/hu_corpus/full_700/calibration_results.jsonl` — re-validated calibration
13. `data/hu_corpus/full_700/opus_tier_up.jsonl` — Opus tier-up on non-unanimous
14. `data/corpus_hu_750_2026-05-10.jsonl` — assembled final corpus (pilot 50 + full 700 = 750)
15. `data/corpus_hu_750_2026-05-10_labels.jsonl` — matching labels file
16. `review/comms/BUILDER_REPORT_PHASE15D3_FULL_2026-05-10.md` — execution log + final corpus stats

### Methodology constraints (binding)

- **Single committed path** per `feedback_quality_default_no_ask.md`: no menus
- **Pilot-first** per `feedback_pilot_first_for_long_jobs.md`: ENFORCED via gate
- **No deadlines** per `feedback_no_deadlines.md`
- **HU-6.5 owner adjudication propagates**: consensus.jsonl entries that include HU-6.5 lookalike spots must apply the CALL adjudication + carry the solver-verification-pending flag forward
- **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: solver outputs (when available) → research findings only; NEVER training labels
- **Bucket-first** per `feedback_bucket_first_labelling.md`: NO equity thresholds in labelling prompt
- **Calibration mandatory** per `docs/PROCESS_GUIDE.md` §2.1
- **STOP conditions** per CLAUDE.md §5: lookalike pool < 3000 (insufficient diversity) / similarity-band assignment fails for any reference spot / labeller failure-mode → STOP and report. Do NOT improvise.

### What this PR does NOT do (mandatory negative scope)

- ❌ Does NOT execute 1.5-D.4 retrain (separate sub-sub-phase)
- ❌ Does NOT modify any source files outside `scripts/generate_hu_situations.py` + `data/hu_corpus/`
- ❌ Does NOT use solver output as training label
- ❌ Does NOT relax pilot gate
- ❌ Does NOT improvise on STOP conditions

## QC stream — what you audit (post-PR; standalone, ~15-20 min per PR)

Routing per `feedback_qc_routing_when_standalone_active.md`. Pre-merge QC required per `feedback_qc_required_before_approval.md`.

10-item audit (per pilot PR + per full PR):

1. **Diff scope strict** (TC-23): files in `scripts/` + `data/hu_corpus/` + `review/comms/` only. NO unauthorized source/prompt/model edits.
2. **Generation script quality**: `generate_hu_situations.py` reads from `design/hu_reference_set/` + outputs valid jsonl with all required fields per HU spot spec.
3. **Pool size**: ~3000 generated; final filtered to ~750 (pilot 50 + full 700).
4. **Similarity-band threshold compliance**: similarity_distance_audit.jsonl shows per-spot assignment within architect-committed threshold; threshold rationale documented in builder report.
5. **5 labellers per spot + calibration compliance**: per-spot 5 labeller IDs; calibration results show ≥ 20/24 + 3 GTO-reversal correct.
6. **Bucket-first compliance** + solver-vs-labels separation as per 1.5-D.2 audit pattern.
7. **Consensus rule applied**: per-spot consensus rule per design memo §4.3.
8. **Pilot gate verification** (pilot PR): ≥ 80% labeller-consensus rate.
9. **HU-6.5 owner-adjudication propagation**: lookalike spots derived from HU-6.5 carry the CALL consensus + solver-verification-pending flag forward.
10. **TC-X-DISPATCH-COMPLIANCE**: §4.4 spec + pilot+full split + solver-pending gating + negative scope items honored.

QC writes per PR + heartbeat sync.

## Owner — informational

- Standing directive: orchestrator merges this dispatch + builder PRs (pilot then full) + QC verdicts autonomously
- Owner-adjudicated splits surface to owner gate via builder report; orchestrator HOLDs corpus-finalisation if owner-judgment is required
- After 1.5-D.3 full + verdict merge → orchestrator dispatches Phase 1.5-D.4 (HU model retrain on 59-surface; from-scratch per §4.5)

## Loop status

Loop CONTINUES through 1.5-D.3 pilot → gate → full → QC → 1.5-D.4 dispatch → 1.5-E (router/coaching) → Phase 2 D5 deferred per blueprint.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `6f08432` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 1.5-D.2 fully merged: master `6f08432` (PR #332 + #334 + #335 + #337)
- HU reference set: `design/hu_reference_set/`
- HU-6.5 spec: `design/hu_reference_set/HU_AXIS_6_RIVER_PRECISION.md`
- HU-6.5 raw labels + consensus: `data/hu_labelling/full_HU2_HU6/`
- Architect's design memo §4.4: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- 12.5K Lever C precedent: `scripts/generate_lever_c_situations.py`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: HU-6.5 adjudicated CALL with solver-verification flag pending. LEAD-PROGRAMMER fires Phase 1.5-D.3 (HU corpus assembly; pilot 50 → full 700 via lookalike-generation pipeline) on this comm merge. STOP > improvise. Orchestrator merges PRs + QC verdicts autonomously per standing directive on PASS. Loop CONTINUES to 1.5-D.4 post-full-merge.**
