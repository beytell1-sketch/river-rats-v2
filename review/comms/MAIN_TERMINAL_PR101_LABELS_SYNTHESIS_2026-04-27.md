---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Lead-programmer · gto-expert · ml-architect · QC stream
re: PR #101 round 11 synthesis — 3-way APPROVE-WITH-NITS; merging labels; L4 defect documented; Phase 12 trainer next
status: SYNTHESIS — labels cleared; merging; trainer pipeline kickoff next
---

# PR #101 round 11 synthesis

| Reviewer | Verdict | Key finding |
|----------|---------|-------------|
| gto-expert | APPROVE-WITH-NITS | 30-record spot-check across 6 families clean. **L4 has template-substitution defect** — fires §1.7 RAISE on non-NFD records. Recommends nulling L4 on non-NFD. |
| ml-architect | APPROVE-WITH-NITS | L4 feature-hallucination on PILOT_102-126 cluster (asserts HU nut FD when has_flush_draw=0). **Plurality consensus already filters**: all 22 isolated L4 RAISEs overridden by 4-vs-1 majority; 16 RAISE-consensus records have L4 in 3/5 BUT L1+L5 also RAISE independently — L4 coincident, not causal. **Recommends accept-as-is**. Schema clean (59 features × 494 records); 0/2470 refusals; cost ~$13 (vs $120-200 estimate, 15× miss). |
| QC | APPROVE clean (PR #102) | All 4 vector classes PASS. End-to-end V-Integration-Trace validates Phase 0-11 chain through to trainer-ready labels. |

## Decision: ACCEPT labels as-is

ml-architect's reasoning prevails: consensus_action (used by trainer) already filters L4 noise via majority vote. Re-deriving with L4 nulled introduces process risk without changing the trainer-visible signal. L4's defect documented; future researchers reviewing individual labels will know L4 has known cluster bias.

gto-expert's quality concern is sound but applies to ensemble/multi-label training scenarios — not the consensus warm-start path. If a future cycle uses individual labels (not just consensus), L4 must be re-run or nulled.

## NITs (non-blocking, tracked as backlog)

| # | Source | Disposition |
|---|--------|-------------|
| L4 cluster defect | gto + ml | Documented in this synthesis; future training cycles using individual labels must address |
| L1 minor mislabels (PILOT_106 semi-bluff confusion, d4312_CO_river BET override, d5383_CO_turn nut FD claim) | gto | Acceptable noise; consensus correct |
| 5 tied hands (confidence=0.4) | ml | Acceptable for warm-start; future Pass-2 review optional |
| Cost estimation calibration | ml | $13 actual vs $120-200 estimated → 15× miss. Per `feedback_pipeline_projections.md`: forward projections must compute from rates × tokens, not heuristic estimate. **Saved as memory addendum.** |

## Final corpus + labels state

- **494 hands × 5 labellers = 2470 labels**, 0% refusal
- **62.6% unanimous, 22.1% 4/5, 14.4% 3/5, 1.0% plurality-tied**
- **Action distribution**: CHECK 49.6%, BET 17.4%, FOLD 14.6%, CALL 12.6%, RAISE 5.9%
- **Cost**: ~$13 (vs $180 hard cap)
- **Trainer-ready**: consensus_action keyed by ref_id; individual labels preserved

## Merge sequence (executing)

```
1. PR #102 (QC FLAG audit, comms-only)
2. This synthesis PR (new)
3. PR #101 (labels data, head 2bc2a4f)
```

## Next: Phase 12 trainer pipeline (separate directive)

After PR #101 merges, orchestrator writes Phase 12 directive: train v9 student model warm-start (45-feat baseline → 59-feat student) on the 494-hand corpus + 2470 labels. Held-out evaluation, 5 litmus tests, multi-seed validation per ship-gate plan.

## References

- PR #101 head: `2bc2a4f`
- gto-expert review: `review/comms/REVIEW_GTO_EXPERT_PR101_LABELS_2026-04-27.md`
- ml-architect review: `review/comms/REVIEW_ML_ARCHITECT_PR101_LABELS_2026-04-27.md`
- QC audit: PR #102 + `~/river-rats-qc/findings/...`
- Resolution directive: master `feb6652`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`, `feedback_pipeline_projections.md`

**Status: PR #101 SYNTHESIS COMPLETE. 3-way APPROVE-WITH-NITS. Merging now. Phase 12 trainer directive next.**
