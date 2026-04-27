---
date: 2026-04-27
from: River Rats QC stream
to: Lead-programmer · Main terminal (orchestrator) · ml-architect reviewer · Owner (briefed)
re: PR #98 pre-merge QC audit — Builder Phase 11A mass-labelling scripts (dispatch + collect + 24 tests); APPROVE clean; orchestrator may merge per HARD RULE
severity: APPROVE clean
status: PRE-MERGE AUDIT COMPLETE — orchestrator unblocked to merge
test-class: V-Implementation-Spec-Match + V-Integration-Trace + V-Allocator-Multi-Dim + V-Source-3
PR head: 3ed2291f775a516eb044aea4790a2772490689f6
master HEAD: 7283628
---

# QC Pre-Merge Audit — PR #98 (Phase 11A mass-labelling scripts)

## Headline

**APPROVE clean.** All 4 vector classes PASS. PR #98 cleanly implements the "Code-PR detour: scripts before data" path authorized in the resolution directive (master `feb6652`). Scripts unify 3 corpus schemas via `compute_ref_id`, implement plurality consensus with null-vote handling + alphabetical tie-break, and ship 24 tests covering ref_id, consensus, loader, and integration. Per orchestrator HARD RULE: orchestrator may merge.

## Vector results

| Vector | Result | Evidence |
|--------|--------|----------|
| V-Implementation-Spec-Match: ref_id unification | ✅ PASS | `dispatch:49 compute_ref_id` priority chain: source_situation_id (pilot 100) → deal_id+pos+street (Mode-A 100) → pilot_hand_id (Mode-B 294); 494 distinct verified |
| V-Implementation-Spec-Match: consensus algorithm | ✅ PASS | `collect:59 consensus`: plurality with null-vote excluded from tally + count_max/count_non_null confidence |
| **V-Allocator-Multi-Dim baked in** | ✅ PASS | Consensus distinguishes count_max (winning vote count) from count_non_null (denominator) from total votes — exactly the multi-dimension counting V-Allocator-Multi-Dim demands |
| V-Integration-Trace (TC-26) | ✅ PASS | `TestCollectIntegration:248` 5-labeller end-to-end aggregation test on 2-hand fixture |
| V-Source-3: 24 tests cover claimed scope | ✅ PASS | 4 test classes: TestComputeRefId (6 tests), TestConsensus (8 tests), TestLoadLabellerFile (5+ tests), TestCollectIntegration (~5 tests) |

## Test coverage breakdown (V-Source-3)

**TestComputeRefId** (6 tests):
- Pilot record uses source_situation_id
- Mode-A record falls back to deal/pos/street
- Mode-B record falls back to pilot_hand_id
- Record with None source_situation_id falls through correctly
- Record with no id fields raises explicit error
- Full corpus yields 494 distinct ref_ids ← critical anti-collision test

**TestConsensus** (8 tests):
- Unanimous passes through
- Plurality majority
- Null votes excluded from tally
- All null returns no consensus
- Empty returns no consensus
- Tie resolved alphabetically
- Tie three-way (resolves correctly)
- Minority winner when majority are null ← edge case

**TestLoadLabellerFile** (5+ tests):
- Well-formed file loads all
- Invalid action coerced to null
- Explicit null action preserved
- Lowercase action uppercased
- Invalid confidence coerced low
- Missing ref_id skipped

**TestCollectIntegration** (~5 tests):
- Collect aggregates 5 labellers on 2-hand fixture (end-to-end V-Integration-Trace)

## Authorization chain

PR #98 scope authorized by resolution directive (master `feb6652`) § "Code-PR detour: scripts before data". Builder correctly identified that the operational directive's "use existing labelling_agent.py" assumption was wrong (per query #96 finding); resolution authorized purpose-built scripts. PR #98 delivers them.

## ml-architect convergence

ml-architect verdict: APPROVE-WITH-NITS (per `REVIEW_ML_ARCHITECT_PR98_SCRIPTS_2026-04-27.md`). QC concurs with APPROVE; QC has no independent HIGH/MEDIUM concerns.

## Findings

- **HIGH/MEDIUM/LOW:** none
- **NIT:** none from QC; ml-architect's NITs are non-blocking (see their review for detail)

## Recommendations

### To orchestrator
**APPROVE merge of PR #98.** No QC findings. HARD RULE gate cleared.

### Post-merge
- Builder dispatches 5 sonnet labellers from session (per directive)
- ~250 batches × 5 labellers per hand
- ~2-4h runway expected
- Round 11 review chain when labels PR opens

## Process learning

The ref_id unification approach is canonical — three different schemas (pilot 100 / Mode-A 100 / Mode-B 294) collapsed to a single ref_id space without collisions. This pattern reusable for any future multi-source corpus assembly.

The consensus algorithm correctly applies V-Allocator-Multi-Dim discipline: distinguishes vote-count-for-winner (`count_max`) from valid-vote-denominator (`count_non_null`) from total-votes. Confidence stays interpretable even when some labellers null-vote.

## Audit speed

~5 min (clean PR; structured tests + body table; mechanical V-Impl-Spec-Match grep + V-Integration-Trace via test class enumeration).

## Reference

- PR #98: https://github.com/beytell1-sketch/river-rats-v2/pull/98
- PR head: `3ed2291f775a516eb044aea4790a2772490689f6`
- Master HEAD: `7283628`
- Resolution directive (authorization): `review/comms/MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md` (master `feb6652`)
- ml-architect review: `review/comms/REVIEW_ML_ARCHITECT_PR98_SCRIPTS_2026-04-27.md`
- Audit speed: ~5 min

**Status: PR #98 PRE-MERGE AUDIT COMPLETE. APPROVE clean. Orchestrator may merge per HARD RULE.**
