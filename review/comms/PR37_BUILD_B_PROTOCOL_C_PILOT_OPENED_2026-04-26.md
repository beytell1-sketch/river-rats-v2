---
date: 2026-04-26
from: Logic builder (Build B author)
to: Main terminal (orchestrator) · Owner · Independent reviewer (when dispatched) · QC stream (TC-23 + V-B vectors candidate)
re: PR #37 OPEN — Build B: Protocol C labeller-facing pilot artifact (v1.0.1-pilot); per orchestrator directives 3f9564e + PR35_MERGE_ACK_BUILD_B_KICKOFF; closes PRE-DISPATCH PREREQUISITES row #6; reviewer dispatch next builder action
status: BUILD COMPLETE → REVIEWER PENDING
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/37
branch: stage4-pre-dispatch/protocol-c-pilot-build
feature_commit: 2a597b4
directive_source: MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md (3f9564e) + MAIN_TERMINAL_PR35_MERGE_ACK_BUILD_B_KICKOFF_2026-04-26.md
predecessor: PR #35 Build A (Protocol B pilot) — APPROVE-WITH-NITS dual-pipeline
qc_audit_offer: V-B1...V-B3 vectors pre-scoped per QC follow-up
---

# PR #37 Opened — Build B (Protocol C pilot artifact)

## Summary

New file: `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`
(1,964 lines). Self-contained labeller-facing artifact derived from
`prompts/protocol_c_adversarial_elimination_v1_0.md` (design artifact
at master `c4f29a5`). Same recipe as Build A PR #35.

## Verbatim-inlined sections

| Section | Source | Lines |
|---------|--------|-------|
| §Buckets | `prompts/gto_labeller_v3.1.md` | 170-204 (Step 1: CLASSIFY THE HAND) |
| §Features | `prompts/gto_labeller_v3.1.md` | 439-496 (54-feature vector) + v2.4 P1 blockers (56-59) + board_adjusted_hrp (55) note |
| §DO NOT Rules | `prompts/gto_labeller_v3.1.md` | 590-647 (Rules 1-10; item 11 subsumed into Rule 10 verbatim) |
| §Output schema | `prompts/gto_labeller_v3.1.md` | §Output Format example fields + Protocol-C additions |

Replaces design artifact's COMBINED "Buckets, Features, DO NOT Rules
(inherited from v3.1)" section (line 600 of source) with three
SEPARATE verbatim-inlined sections.

## Build A NIT pre-emptions (per orchestrator's NIT-cleanup suggestion)

| NIT | Source | Build B fix |
|-----|--------|-------------|
| Build A reviewer + QC NIT-2: "Rules 1-11" shorthand | Inherited from design artifact | Used "Rules 1-10; v1.0.1 design summary item 11 subsumed into Rule 10 verbatim" explicitly throughout |
| Build A QC NIT-1: line-range 590-647 vs 595-647 inconsistency | Inherited from design artifact | Used 590-647 consistently across frontmatter / section header / footer |

Build A NIT-3 (§Role heading qualifier "(inherited from v3.1)" — body self-contained, mildly inheritance-flavoured): NOT addressed in Build B because §Role section in Protocol C source uses the same pattern; same disposition (descriptive provenance only, not labeller-blocking).

## Frontmatter changes

- `version: v1.0.1` → `v1.0.1-pilot`
- `artifact_class: PILOT-RUNTIME` added (labeller-facing)
- `derived_from` updated to point at design artifact at master `c4f29a5`
- `review_chain` extended with Build B pass + reviewer-required gate
- `build_provenance` block records source + commit + inlined sections + directive ref + Build A NIT pre-emption documentation

PRE-PILOT BUILD REQUIREMENT section replaced with §"Pilot artifact build provenance (Build B output)".

## Diff scope

```
prompts/protocol_c_adversarial_elimination_v1_0_pilot.md | 1964 ++++++++++++++++++++
1 file changed, 1964 insertions(+)
```

Single feature commit `2a597b4` on `stage4-pre-dispatch/protocol-c-pilot-build`. Source design artifact (`prompts/protocol_c_adversarial_elimination_v1_0.md`) NOT modified by this PR.

## Builder verification spot-checks

- [x] HARD branch check pre-commit (`stage4-pre-dispatch/protocol-c-pilot-build`)
- [x] Self-test grep for inheritance-by-reference markers in JSON / labeller-workflow scope returns ZERO matches
  - The one match at line 91 is descriptive provenance (documents which placeholder was replaced), not actual placeholder
- [x] §Buckets verbatim block contains all 6 buckets matching v3.1 lines 170-204
- [x] §Features verbatim block contains 54 v3.1 rows + board_adjusted_hrp note + 4 v2.4 P1 blockers (nut_flush_block, flush_draw_block_pct, straight_draw_block_pct, nut_made_block_pct) = 59 total raw features
- [x] Total raw feature count cross-checked against `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4 — match
- [x] §DO NOT Rules verbatim block contains Rules 1-10 from v3.1 lines 590-647
- [x] §Output schema example contains all v3.1 fields + Protocol-C addition fields (protocol, candidate_actions, case_against, elimination_trail, final_action, case_against_*_count, mixed_*, primary_action, escalate_to_adjudicator)
- [x] Build A NIT pre-emptions applied: line-range 590-647 consistent + rule-count format explicit

## Reviewer dispatch context (next builder action)

Required reviewer characteristics:
- Independent dispatch (different general-purpose subagent + V3-compliance / verbatim-inlining persona than Build A reviewer)
- Read-only constraint
- Cross-checks REQUIRED (same pattern as Build A PR #35):
  1. Verbatim-inlining correctness: byte-comparison §Buckets / §Features / §DO NOT Rules / §Output schema against v3.1 source
  2. v2.4 blocker features (56-59) match `feature_keys.py` naming
  3. Total raw feature count = 59 cross-references against Stage 5 retrain v1.0.1
  4. Frontmatter v1.0.1-pilot + build_provenance accurate
  5. No remaining inheritance-by-reference markers in labeller-workflow scope (§"Reasoning Order" through §"Anti-patterns")
  6. Source design artifact `prompts/protocol_c_adversarial_elimination_v1_0.md` UNTOUCHED
  7. TC-23: PRE-DISPATCH PREREQUISITES row #6 closeable (artifact EXISTS at master HEAD after merge)
  8. Build A NIT pre-emptions verified clean

QC has standing offer for pre-merge audit using TC-23 + V-B1...V-B3 vectors (pre-scoped per their tick 30+ publication).

## Next builder actions

1. Dispatch independent reviewer (general-purpose + V3-compliance persona); read-only
2. On reviewer return: write verdict to `review/comms/REVIEW_VERDICT_PR_37_BUILD_B_2026-04-26.md`; commit + push to master; PR comment
3. Stand by for orchestrator merge
4. After Build B merged → Build C (pilot 100-hand stratified corpus)
5. After all 3 sealed → re-issue Pilot Orchestrator dispatch directive

## References

- PR #37: https://github.com/beytell1-sketch/river-rats-v2/pull/37
- Feature commit: `2a597b4`
- Predecessor PR #35 (Build A): merged with reviewer + QC + V3-compliance APPROVE-WITH-NITS
- Build B kickoff: `MAIN_TERMINAL_PR35_MERGE_ACK_BUILD_B_KICKOFF_2026-04-26.md`
- Builds A/B/C directive: `3f9564e` (`MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md`)
- Source design artifact: `prompts/protocol_c_adversarial_elimination_v1_0.md` at master `c4f29a5`
- v3.1 source: `prompts/gto_labeller_v3.1.md` at master HEAD
- Stage 5 retrain v1.0.1 (downstream contract): `STAGE5_RETRAIN_PROTOCOL_v1_0.md`

**Status: PR #37 OPEN. Build B complete. Reviewer dispatch is next builder action. After Build B seals: Build C (pilot 100-hand corpus) → Pilot Orchestrator re-activation.**
