---
date: 2026-04-26
from: Logic builder (Build A author)
to: Main terminal (orchestrator) · Owner · Independent reviewer (when dispatched) · QC stream (TC-23 audit candidate)
re: PR #35 OPEN — Build A: Protocol B labeller-facing pilot artifact (v1.0.1-pilot); per orchestrator directive 3f9564e; closes PRE-DISPATCH PREREQUISITES row #5; reviewer dispatch next builder action
status: BUILD COMPLETE → REVIEWER PENDING
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/35
branch: stage4-pre-dispatch/protocol-b-pilot-build
feature_commit: f95cdab
directive_source: MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md (3f9564e)
qc_audit_offer: QC_HALT_PHASE_A_PREREQ_GAPS_FOLLOWUP_2026-04-26.md (TC-23 standing offer)
---

# PR #35 Opened — Build A (Protocol B pilot artifact)

## Summary

New file: `prompts/protocol_b_composition_first_v1_0_pilot.md`
(1,458 lines). Self-contained labeller-facing artifact derived from
the design artifact `prompts/protocol_b_composition_first_v1_0.md`
at master `c4f29a5`.

## Verbatim-inlined sections

Per Protocol B v1.0.1 PRE-PILOT BUILD REQUIREMENT + orchestrator
Build A directive at `3f9564e`:

| Section | Source | Lines |
|---------|--------|-------|
| §Buckets | `prompts/gto_labeller_v3.1.md` | 170-204 (Step 1: CLASSIFY THE HAND) |
| §Features | `prompts/gto_labeller_v3.1.md` | 439-496 (54-feature vector) + v2.4 P1 blockers (56-59) + board_adjusted_hrp (55) note |
| §DO NOT Rules | `prompts/gto_labeller_v3.1.md` | 590-647 (Rules 1-10) |
| §Output schema | `prompts/gto_labeller_v3.1.md` | §Output Format example fields + Protocol-B additions |

The §Output schema inlining is a within-spirit scope expansion: the
v1.0.1 design artifact had `... (all v3.1 fields verbatim) ...` as a
placeholder; for the pilot artifact to be self-contained per
labeller workflow, the actual fields are inlined.

## Frontmatter changes

- `version: v1.0.1` → `v1.0.1-pilot`
- `artifact_class: PILOT-RUNTIME` added (labeller-facing)
- `derived_from` updated to point at design artifact at master `c4f29a5`
- `review_chain` extended with Build A pass + reviewer-required gate
- `build_provenance` block records source + commit + inlined sections + directive ref

PRE-PILOT BUILD REQUIREMENT section replaced with §"Pilot artifact
build provenance (Build A output)" — describes artifact as build
output rather than a future build requirement.

## Diff scope

```
prompts/protocol_b_composition_first_v1_0_pilot.md | 1458 ++++++++++++++++++++
1 file changed, 1458 insertions(+)
```

Single feature commit `f95cdab` on
`stage4-pre-dispatch/protocol-b-pilot-build`. Source design artifact
(`prompts/protocol_b_composition_first_v1_0.md`) NOT modified by
this PR.

## Builder verification spot-checks

- [x] HARD branch check pre-commit (`stage4-pre-dispatch/protocol-b-pilot-build`) — Tasks 4 / 4.2 incident lessons
- [x] Self-test grep for inheritance-by-reference markers in build-output document returns ZERO matches:
  - `see source artifact` (no hits)
  - `copy verbatim into this section at finalisation` (no hits)
  - `(or equivalent labeller-facing artifact)` (no hits)
  - `... (all v3.1 fields)` (no hits)
- [x] §Buckets verbatim block contains all 6 buckets (monster, strong_made, medium_made, weak_made, drawing, air) with examples + classification questions matching v3.1 lines 170-204
- [x] §Features verbatim block contains 54 v3.1 rows + board_adjusted_hrp note + 4 v2.4 P1 blockers (nut_flush_block, flush_draw_block_pct, straight_draw_block_pct, nut_made_block_pct) = 59 total raw features
- [x] Total raw feature count cross-checked against `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4 ("55-feature vector + 4 v2.4 blocker features = 59 raw features") — match
- [x] §DO NOT Rules verbatim block contains Rules 1-10 from v3.1 lines 590-647
- [x] §Output schema example contains all v3.1 fields (situation_id, hand_bucket, action, confidence, difficulty, reasoning, intentions_raw, intentions, street_plan_raw, street_plan_tags, feature_attention, tier1_removals, proposed_tags, alternatives_considered) + Protocol-B addition fields (protocol, composition_derived_candidates, bucket_aligned_action, outcome_4a_or_4b, composition_rule_conflict, composition_reasoning_trace, override_kb_justification, escalate_to_adjudicator)

## Reviewer dispatch context (next builder action)

Required reviewer characteristics:
- Independent dispatch (general-purpose subagent, V3-compliance / verbatim-inlining persona)
- Read-only constraint
- Cross-checks REQUIRED:
  1. Verbatim-inlining correctness: spot-check §Buckets / §Features / §DO NOT Rules / §Output schema against `prompts/gto_labeller_v3.1.md` source content (no paraphrasing or summarisation; verbatim must mean verbatim)
  2. v2.4 blocker features (56-59) match `feedback_attention_flags_when_features_change.md` + `BUILDER_V24_P1_SPEC_LOCKED_2026-04-19.md` naming
  3. Total raw feature count = 59 cross-references against Stage 5 retrain v1.0.1 §Hyperparameters point #4
  4. Frontmatter v1.0.1-pilot + build_provenance accurate vs actual diff
  5. No remaining inheritance-by-reference markers in labeller-workflow scope (§"Reasoning Order" through §"Anti-patterns")
  6. Source design artifact `prompts/protocol_b_composition_first_v1_0.md` at master HEAD UNTOUCHED by this PR
  7. TC-23 (per QC follow-up): verify that PRE-DISPATCH PREREQUISITES row #5 is now closeable — the labeller-facing artifact EXISTS at master HEAD after merge

QC has standing offer for pre-merge audit using TC-23 + standard pattern.

## Next builder actions

1. Dispatch independent reviewer (general-purpose + V3-compliance persona); read-only
2. On reviewer return: write verdict to `review/comms/REVIEW_VERDICT_PR_35_BUILD_A_2026-04-26.md`; commit + push to master; PR comment
3. Stand by for orchestrator merge
4. After Build A merged → Build B (Protocol C labeller-facing pilot artifact, same pattern)
5. After Build B merged → Build C (pilot 100-hand stratified corpus)
6. After all 3 sealed → re-issue Pilot Orchestrator dispatch directive

## References

- PR #35: https://github.com/beytell1-sketch/river-rats-v2/pull/35
- Feature commit: `f95cdab`
- Directive: `3f9564e` (`MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md`)
- HALT comm: `1fb5f04` (`PILOT_PHASE_A_HALT_PREREQ_GAPS_2026-04-26.md`)
- QC follow-up + TC-23: `782b964` (`QC_HALT_PHASE_A_PREREQ_GAPS_FOLLOWUP_2026-04-26.md`)
- Source design artifact: `prompts/protocol_b_composition_first_v1_0.md` at master `c4f29a5`
- v3.1 source: `prompts/gto_labeller_v3.1.md` at master HEAD
- Stage 5 retrain v1.0.1 (downstream contract): `STAGE5_RETRAIN_PROTOCOL_v1_0.md`

**Status: PR #35 OPEN. Build A complete. Reviewer dispatch is next builder action. After Build A seals: Build B → Build C → Pilot Orchestrator re-activation.**
