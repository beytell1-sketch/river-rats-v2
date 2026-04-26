---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT V3-compliance + verbatim-inlining reviewer (different dispatch from Build A reviewer and Build B author)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #37 — Build B: Protocol C labeller-facing pilot artifact (`2a597b4`)
status: APPROVE-WITH-NITS — verbatim inlining is byte-exact across all 3 sections; cross-stream contracts intact; one minor body-text staleness remains (Anti-patterns intro "Rules 1-11" — same locus as Build A NIT-2 body occurrence)
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/37
branch: stage4-pre-dispatch/protocol-c-pilot-build
artifact: prompts/protocol_c_adversarial_elimination_v1_0_pilot.md (commit 2a597b4; +1964 lines new file)
predecessor: 2ea67d0 (master / PR #35 Build A merged)
predecessor_directive: 3f9564e (Builds A/B/C directive) + PR35_MERGE_ACK_BUILD_B_KICKOFF
qc_audit: TC-23 (PRE-DISPATCH PREREQUISITES row #6)
---

# Review Verdict — PR #37 (Build B: Protocol C labeller-facing pilot artifact)

## Provenance note
Independent fresh-dispatch review. Did not author the v1.0/v1.0.1 design artifact, the orchestrator directive, the Build A pilot or its review, or the Build B pilot. Read-only run; no edits, no PR comments, no pushes.

## Per-section verbatim verification

### §Buckets — verbatim from v3.1 lines 170-204
**PASS — HIGH confidence.** Byte-for-byte diff of pilot lines 640-674 (after stripping `> ` blockquote prefix) against v3.1 lines 170-204 is empty (1,433 chars both sides). All six bucket definitions present in original order with original example hands; "State the bucket explicitly:" closer preserved.

### §Features — verbatim from v3.1 lines 439-496 + v2.4 P1 blockers + board_adjusted_hrp note
**PASS — HIGH confidence.** Byte-for-byte diff of pilot lines 691-748 (unquoted) against v3.1 lines 439-496 is empty (3,374 chars both sides). Full 54-row table preserved, no field reordering. Feature 55 (`board_adjusted_hrp`) documented separately at pilot lines 752-757 with correct provenance pointer (Stage 5 un-hold per MUST #48); cross-checked against `river-rats-core/gto_model.py` `FEATURE_COLUMNS` — Python `len(FEATURE_COLUMNS)` returns exactly 55 with `board_adjusted_hrp` at index 54 (last position, position #55). Features 56-59 (`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`) present at pilot lines 763-768 as a separate table with correct numbering. **Total raw feature contract = 59** asserted at pilot lines 770-774 and matches `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4 ("55 raw + 4 v2.4 blocker = 59 raw") — phrased identically (line 234 + 264 of retrain protocol).

### §DO NOT Rules — verbatim from v3.1 lines 590-647
**PASS — HIGH confidence.** Byte-for-byte diff of pilot lines 784-841 (unquoted) against v3.1 lines 590-647 is empty (2,762 chars both sides). All 10 numbered rules present in order. The footnote at pilot lines 843-847 explicitly explains the design-artifact "11" referred to v3 §3.B HRP test-harness warning being subsumed into Rule 10 — verified accurate: Rule 10 carries the `[v3 addition §3.B]` marker and covers `HRP_INVESTIGATION_2026-04-15.md` directly.

### §Output schema — v3.1 example fields verbatim + Protocol-C additions
**PASS — HIGH confidence.** Pilot lines 882-950 contain a fully-populated JSON example with every v3.1 field (situation_id, hand_bucket, action, confidence, difficulty, reasoning, intentions_raw, intentions, street_plan_raw, street_plan_tags, feature_attention, tier1_removals, proposed_tags, alternatives_considered) plus Protocol-C additions (protocol, candidate_actions, case_against, elimination_trail, final_action, case_against_strawman_count / _strong_count / _moderate_count / _weak_count, mixed_action_pair, mixed_confidence_band, mixed_strategy_acknowledged, primary_action, escalate_to_adjudicator). The design-artifact `... (all v3.1 fields verbatim) ...` placeholder is replaced with a complete worked-example body. Per-field semantics for Protocol-C additions documented at lines 958-983. (A separate MIXED-handling demo at lines 565-598 uses `"argument": "..."` ellipses inside string values as illustrative shorthand — these are not unfilled placeholder markers.)

## Other items

### Frontmatter v1.0.1-pilot + build_provenance
**PASS.** `version: v1.0.1-pilot`; `artifact_class: PILOT-RUNTIME (labeller-facing; self-contained)`; `derived_from` correctly names `prompts/protocol_c_adversarial_elimination_v1_0.md @ master c4f29a5`; `build_provenance` block names source design artifact + master commit, `inlined_from` points at v3.1, lists all four inlined sections with line ranges, references the directive `MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md (commit 3f9564e)`, names `pattern_predecessor: Build A`, and explicitly documents the NIT carry-forward pre-emption (lines 28-30).

### Build A NIT pre-emptions (per orchestrator's NIT-cleanup suggestion)
**PARTIAL PASS — one residual body occurrence.**
- **NIT-1 (line range)** — fully pre-empted. Pilot uses `590-647` consistently across frontmatter (lines 14, 24), pilot-build-provenance section header (line 90), and §DO NOT Rules section header (line 778). No `595-647` stragglers anywhere except inside provenance text documenting the pre-emption itself (lines 29, 121).
- **NIT-2 (rule-count format)** — frontmatter pre-empted, body residual. The frontmatter `build_provenance.inlined_sections` (line 24) uses the explicit form `"Rules 1-10; v1.0.1 design summary item 11 subsumed into Rule 10 verbatim"`. However, **§Anti-patterns intro at line 1563 still reads `"In addition to v3.1's anti-patterns (DO NOT Rules 1-11 + v3.1 §"Anti-patterns")"`** — same shorthand carried verbatim from source design artifact line 1299, which mirrors Build A NIT-2 body occurrence (Build A pilot line 1165). The orchestrator directive's NIT-cleanup bullets specifically targeted *frontmatter* edits ("edit your Build B frontmatter to:"), so Build B did exactly what the directive asked literally; build_provenance line 30 nonetheless overclaims by stating it "closes Build A reviewer + QC NIT-2 'Rules 1-11' shorthand" — a body occurrence is not closed.

### No remaining inheritance-by-reference markers (labeller-workflow scope)
**PASS.** Greps for `see source artifact`, `(or equivalent labeller-facing artifact)`, `... (all v3.1 fields)`, `Reference: v3.1 §`, `inherited from v3.1` over §Reasoning Order through §Anti-patterns (lines 179-1727) return only descriptive section headers ("§Output schema (inherited from v3.1, with Protocol-C additions)" at line 851) whose body IS verbatim-inlined immediately below. Same NIT-3 status as Build A — accepted as descriptive provenance, no labeller-time external lookup directed. Two §Buckets/§Features/§DO NOT Rules headers (lines 631, 680, 778) carry "verbatim-inlined from v3.1" qualifiers that are accurate descriptions of the inlined block beneath them. Build B executed the inheritance-replacement task correctly.

### Source design artifact UNTOUCHED
**PASS.** `git diff master..stage4-pre-dispatch/protocol-c-pilot-build -- prompts/protocol_c_adversarial_elimination_v1_0.md` returns zero lines.

### TC-23 closure — PRE-DISPATCH row #6 RED → GREEN candidate
**PASS.** Per `PILOT_PHASE_A_HALT_PREREQ_GAPS_2026-04-26.md` row #6: "`prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` does not exist". After PR #37 merge, the artifact will exist at master HEAD, satisfying the TC-23 "verify each referenced path exists" audit and flipping row #6 to GREEN.

### Diff scope (+1964 new file only)
**PASS.** `git diff --stat master..stage4-pre-dispatch/protocol-c-pilot-build` shows: +1964 new pilot file; -113 on `review/comms/PR37_BUILD_B_PROTOCOL_C_PILOT_OPENED_2026-04-26.md`. The "deletion" is a branch-divergence artefact — that comm was added to master in commit `6e90a40` AFTER feature branch diverged from `2ea67d0`; merge will preserve it. Not a regression. No code/contract files touched. Same pattern Build A reviewer noted.

### Branch verification
**PASS.** Single commit `2a597b4` on `stage4-pre-dispatch/protocol-c-pilot-build` ahead of merge-base `2ea67d0`. Not present on master; PR #37 OPEN.

### Pattern parallel with Build A
**PASS.** Build B frontmatter / build_provenance / inlined-block style mirrors Build A. Same `PILOT-RUNTIME` artifact_class, same `derived_from @ master c4f29a5` pattern, same blockquote-prefixed verbatim blocks with `(End verbatim block.)` closers, same FEATURE_COLUMNS-aware feature-55 footnote, same Protocol-additions documented after the canonical schema example, same `## Pilot artifact build provenance` section. Build B extends with `nit_carryforward_from_build_a` provenance subsection — net positive over Build A.

## Findings summary

1. **NIT-1 (overclaim in build_provenance):** Pilot frontmatter line 30 claims the rule-count format pre-emption "closes Build A reviewer + QC NIT-2 'Rules 1-11' shorthand". The frontmatter occurrence is closed; the §Anti-patterns intro body line 1563 still reads `"DO NOT Rules 1-11"` (carried verbatim from source design artifact line 1299). Recommend either (a) softening the build_provenance claim to "closes Build A NIT-2 frontmatter occurrence; body Anti-patterns intro line 1563 retains the same shorthand pending v1.1 sweep", or (b) editing line 1563 to the explicit form. The orchestrator's directive only literally asked for frontmatter cleanup, so option (a) is closer to directive scope.
2. **NIT-2 (§Output schema header staleness — same as Build A NIT-3):** Line 851 `## Output schema (inherited from v3.1, with Protocol-C additions)` is mildly inheritance-by-reference flavoured but body IS self-contained verbatim-inline. Acceptable as descriptive provenance, no labeller-time lookup directed. Inherited from design artifact wording.
3. **OBSERVATION (out-of-scope):** Same scope-edge as Build A — the §Anti-patterns intro references v3.1 §"Anti-patterns" which is NOT verbatim-inlined. Per directive only Buckets / Features / DO NOT Rules were in inlining scope, so this is correct, but if pilot reveals a labelling failure mode tied to v3.1's §Anti-patterns, an inlining extension may be needed (parallel observation to Build A verdict item 4).

No HIGH or MEDIUM findings.

## VERDICT
**APPROVE-WITH-NITS — overall confidence HIGH.**

Build B executes the orchestrator directive cleanly. All three required v3.1 sections are byte-exact verbatim inlines (Python char-comparison: 1,433 + 3,374 + 2,762 chars all match exactly — identical to Build A inlining counts since the same v3.1 master HEAD line ranges were targeted). The 4 v2.4 P1 blocker features are correctly numbered 56-59. The 59-raw-feature contract is internally consistent and matches `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4 + `gto_model.py` `FEATURE_COLUMNS` length 55 + 4 blockers. Output schema fully expanded — `... (all v3.1 fields verbatim) ...` placeholder replaced with full v3.1 fields plus the 11 Protocol-C addition fields. Frontmatter and build_provenance accurately capture the build, and explicitly document the Build A NIT carry-forward pre-emption. NIT-1 (frontmatter line range) cleanly pre-empted. NIT-2 (rule-count format) pre-empted in frontmatter; one body occurrence (line 1563 §Anti-patterns intro) remains because the directive scoped the cleanup to frontmatter only. Build_provenance line 30 overclaims slightly. Source design artifact untouched. TC-23 / PRE-DISPATCH row #6 cleared on merge.

The 2 NITs are descriptive-text staleness; the labeller is not misled at runtime (Rules 1-10 verbatim block at lines 784-841 is the source of truth the labeller reads). Recommend fix-forward in a follow-up cleanup commit or v1.1 sweep, not a blocker on Build B merge or Phase A.1 kickoff.

**Required fixes:** None.
**Blockers:** None.

## Action

**Builder:** stand by for orchestrator merge. Optional: a one-line follow-up commit to soften build_provenance line 30 wording or fix line 1563 ("Rules 1-11" → explicit form) if orchestrator wants Build C / Build D to inherit a clean baseline.

**Orchestrator:** APPROVE-WITH-NITS clean (2 NITs cosmetic, non-labeller-blocking). Merging PR #37 closes PRE-DISPATCH PREREQUISITES row #6 (Protocol C pilot artifact RED → GREEN). After merge: Builds A + B SEALED; Build C (pilot 100-hand corpus) is the remaining PRE-DISPATCH gate.

**Owner:** wake to find Build B complete; Build C remaining to clear PRE-DISPATCH gate.

## Reference

- PR #37: https://github.com/beytell1-sketch/river-rats-v2/pull/37
- Feature commit: `2a597b4` on `stage4-pre-dispatch/protocol-c-pilot-build`
- Directive: `3f9564e` (Builds A/B/C) + `MAIN_TERMINAL_PR35_MERGE_ACK_BUILD_B_KICKOFF_2026-04-26.md`
- HALT comm: `1fb5f04`
- QC follow-up (TC-23): `782b964`
- Source design artifact: `prompts/protocol_c_adversarial_elimination_v1_0.md` at master `c4f29a5`
- v3.1 source: `prompts/gto_labeller_v3.1.md` at master HEAD
- Stage 5 retrain v1.0.1: §Hyperparameters point #4 (59 raw features contract)
- Build A predecessor verdict: `review/comms/REVIEW_VERDICT_PR_35_BUILD_A_2026-04-26.md`

**FINAL VERDICT: APPROVE-WITH-NITS — HIGH confidence overall. Cleared for orchestrator merge. Build C (pilot 100-hand corpus) is the remaining PRE-DISPATCH gate.**
