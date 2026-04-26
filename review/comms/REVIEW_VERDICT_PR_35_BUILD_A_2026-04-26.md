---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT V3-compliance + verbatim-inlining reviewer (different dispatch from Build A author)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #35 — Build A: Protocol B labeller-facing pilot artifact (`f95cdab`)
status: APPROVE-WITH-NITS — verbatim inlining is byte-exact across all 3 sections; cross-stream contracts intact; minor numbering staleness ("Rules 1-11" lingers from design artifact)
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/35
branch: stage4-pre-dispatch/protocol-b-pilot-build
artifact: prompts/protocol_b_composition_first_v1_0_pilot.md (commit f95cdab; +1458 lines new file)
predecessor: 782b964 (master / QC follow-up bundled; PR #34 closed)
predecessor_directive: 3f9564e (Build A directive)
qc_audit: TC-23 (per QC_HALT_PHASE_A_PREREQ_GAPS_FOLLOWUP_2026-04-26.md)
---

# Review Verdict — PR #35 (Build A: Protocol B labeller-facing pilot artifact)

## Provenance note
Independent review by a fresh dispatch general-purpose subagent — did not author or co-author the v1.0/v1.0.1 design artifact, the orchestrator directive, or the Build A pilot artifact. Read-only run; no edits, no PR comments, no pushes.

## Per-section verbatim verification

### §Buckets — verbatim from v3.1 lines 170-204
**PASS — HIGH confidence.** Python byte-comparison: pilot artifact lines 404-438 (after stripping `> ` blockquote prefix) equal v3.1 lines 170-204 char-for-char (1,433 chars both sides). All six bucket definitions present in original order with original example hands; "State the bucket explicitly" closer preserved.

### §Features — verbatim from v3.1 lines 439-496 + v2.4 blockers + board_adjusted_hrp
**PASS — HIGH confidence.** Python byte-comparison: pilot lines 453-510 (unquoted) equal v3.1 lines 439-496 char-for-char (3,374 chars both sides). Full 54-row table preserved, no field reordering. Feature 55 `board_adjusted_hrp` documented separately with correct provenance pointer (Stage 5 un-hold per MUST #48); cross-checked against `river-rats-core/gto_model.py` `FEATURE_COLUMNS` — length is exactly 55 with `board_adjusted_hrp` at index 55 (last position). Features 56-59 (nut_flush_block, flush_draw_block_pct, straight_draw_block_pct, nut_made_block_pct) present as a separate table with correct numbering; all four exist in `river-rats-core/feature_keys.py`. **Total raw feature contract = 59** asserted in pilot (line 532-536) and matches `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters phrasing "55 raw + 4 v2.4 blocker = 59 raw" (line 57, 143).

### §DO NOT Rules — verbatim from v3.1 lines 590-647
**PASS — HIGH confidence.** Python byte-comparison: pilot lines 546-603 (unquoted) equal v3.1 lines 590-647 char-for-char (2,762 chars both sides). All 10 numbered rules present in order. The footnote at lines 605-609 explicitly explains the design-artifact "11" referred to v3 §3.B HRP test-harness warning being subsumed into Rule 10 — verified accurate: Rule 10 carries the `[v3 addition §3.B]` marker and covers `HRP_INVESTIGATION_2026-04-15.md` directly.

### §Output schema — v3.1 example fields + Protocol-B additions
**PASS — HIGH confidence.** Pilot lines 624-686 contain a fully-populated JSON example with every v3.1 field (situation_id, hand_bucket, action, confidence, difficulty, reasoning, intentions_raw, intentions, street_plan_raw, street_plan_tags, feature_attention, tier1_removals, proposed_tags, alternatives_considered) plus Protocol-B additions (protocol, composition_derived_candidates, bucket_aligned_action, outcome_4a_or_4b, composition_rule_conflict, composition_reasoning_trace, override_kb_justification, escalate_to_adjudicator). The design-artifact `... (all v3.1 fields verbatim) ...` placeholder (design line 452) has been replaced with a complete worked-example body. Per-field semantics for the Protocol-B additions documented at lines 695-716.

## Other items

### Frontmatter v1.0.1-pilot + build_provenance
**PASS.** `version: v1.0.1-pilot`; `artifact_class: PILOT-RUNTIME (labeller-facing; self-contained)`; `derived_from` correctly names `prompts/protocol_b_composition_first_v1_0.md @ master c4f29a5`; `build_provenance` block names source design artifact + master commit, `inlined_from` points at v3.1, lists all three inlined sections with line ranges, and references the directive `MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md (commit 3f9564e)`. **NIT:** the build_provenance entry for §DO NOT Rules says "Rules 1-11" — pilot's own inlined block has 10 rules, which the in-body footnote acknowledges; frontmatter wording is mildly stale.

### No remaining inheritance-by-reference markers (labeller-workflow scope)
**PASS.** Greps for `see source artifact`, `(or equivalent labeller-facing artifact)`, `... (all v3.1 fields)`, `Reference: v3.1 §`, `inherited from v3.1` over §Reasoning Order through §Anti-patterns (lines 179-1331) return **0 hits**. Three matches outside scope are descriptive provenance only: line 161 §Role heading qualifier (body itself is self-contained role text, no labeller lookup directed); line 721 closing note in §Output schema (post-inlined-JSON descriptive footer); line 1453 §Reference (out-of-labeller-scope per artifact's own §"Out of labeller scope" declaration at line 130-133). Design artifact had 8 such markers in scope; pilot reduces to 0 in scope. Build A executed the inheritance-replacement task correctly.

### Source design artifact UNTOUCHED
**PASS.** `git diff master..stage4-pre-dispatch/protocol-b-pilot-build -- prompts/protocol_b_composition_first_v1_0.md` returns empty. Only `prompts/protocol_b_composition_first_v1_0_pilot.md` appears in the prompts/ diff (+1458 lines, new file).

### TC-23 closure — PRE-DISPATCH row #5 RED → GREEN candidate
**PASS.** Per HALT comm row #5: "`prompts/protocol_b_composition_first_v1_0_pilot.md` does not exist". After PR #35 merge, the artifact will exist at master HEAD, satisfying the TC-23 "verify each referenced path exists" audit and flipping row #5 to GREEN.

### Diff scope (+1458 new file only)
**PASS.** `git diff --stat master..feature-branch` shows: +1458 new pilot file; -114 on `review/comms/PR35_BUILD_A_PROTOCOL_B_PILOT_OPENED_2026-04-26.md`. The "deletion" is an artefact of branch divergence — that comm was added to master in commit `56a738a` AFTER feature branch diverged from `782b964`; merge will preserve it. Not a regression. No code/contract files touched.

### Branch verification
**PASS.** `git log f95cdab..master` empty in reverse direction; single commit `f95cdab` on `stage4-pre-dispatch/protocol-b-pilot-build` ahead of merge-base `782b964`. Not present on master.

## Findings summary

1. **NIT-1 (frontmatter staleness):** `build_provenance.inlined_sections` line 24 reads `"§DO NOT Rules: v3.1 lines 590-647 (Rules 1-11)"` — the inlined block contains 10 rules; pilot's own footnote (lines 605-609) explains why "11" appears in the v1.0.1 design summary. Frontmatter would be more accurate as "Rules 1-10 (with the design-summary item 11 subsumed into Rule 10)". Inherited from design artifact wording.
2. **NIT-2 (Anti-patterns intro staleness):** Line 1165 reads `"In addition to v3.1's anti-patterns (DO NOT Rules 1-11 + …)"` — same staleness as NIT-1; "Rules 1-10" would be consistent with the inlined block. Inherited from design artifact.
3. **NIT-3 (§Role heading qualifier):** "Role (inherited from v3.1)" is mildly inheritance-by-reference flavoured but the body IS self-contained — no labeller-time lookup directed; acceptable as descriptive provenance.
4. **OBSERVATION (out-of-scope but worth noting for next builder):** Pilot's §Anti-patterns intro at line 1166 references "v3.1 §Anti-patterns" — that section is NOT verbatim-inlined here. Per the directive only Buckets / Features / DO NOT Rules were in scope, so this is correct, but if Build B/C reveal a labelling failure mode tied to v3.1's §Anti-patterns, an inlining extension may be needed.

No HIGH or MEDIUM findings.

## VERDICT
**APPROVE-WITH-NITS — overall confidence HIGH.**

Build A executes the orchestrator directive cleanly. All three required v3.1 sections are byte-exact verbatim inlines (Python char-comparison: 1,433 + 3,374 + 2,762 chars all match exactly). The 4 v2.4 P1 blocker features are correctly numbered 56-59 and exist in `feature_keys.py`. The 59-raw-feature contract is internally consistent and matches `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4 + `gto_model.py` FEATURE_COLUMNS length 55 + 4 blockers. Output schema fully expanded — `... (all v3.1 fields verbatim) ...` placeholder gone. Frontmatter and build_provenance accurately capture the build. Zero inheritance-by-reference markers remain in labeller-workflow scope. Source design artifact untouched. TC-23 / PRE-DISPATCH row #5 cleared on merge.

The 3 NITs are all descriptive-text staleness around the "Rules 1-11" / "Rules 1-10" boundary; the in-body footnote already documents why "11" appears, so the labeller is not misled at runtime. Recommend fix-forward in Build B or a follow-up cleanup commit, not a blocker on Build A merge or Phase A.1 kickoff.

**Required fixes:** None.
**Blockers:** None.

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_35_BUILD_A_2026-04-26.md` ✓
2. Commit + push verdict to master with branch verification
3. Post PR comment on PR #35
4. Stand by for orchestrator merge
5. After merge: begin Build B (Protocol C labeller-facing pilot artifact, same pattern); fold Build A NITs into Build B's design-artifact-text consistency pass

**Orchestrator:**
1. Read this verdict
2. Merge PR #35 — APPROVE-WITH-NITS clean (3 NITs all cosmetic / non-labeller-blocking)
3. After merge: Build A SEALED; PRE-DISPATCH row #5 RED → GREEN; Build B can begin

**Owner:** wake to find Build A complete; Builds B + C remaining (~1.5-3h to clear PRE-DISPATCH gate fully).

## Reference

- PR #35: https://github.com/beytell1-sketch/river-rats-v2/pull/35
- Feature commit: `f95cdab`
- Directive: `3f9564e` (Build A directive)
- HALT comm: `1fb5f04`
- QC follow-up: `782b964`
- Source design artifact: `prompts/protocol_b_composition_first_v1_0.md` at master `c4f29a5`
- v3.1 source: `prompts/gto_labeller_v3.1.md` at master HEAD
- Stage 5 retrain v1.0.1: §Hyperparameters point #4 (59 raw features contract)

**FINAL VERDICT: APPROVE-WITH-NITS — HIGH confidence overall. Cleared for orchestrator merge. Build B is next.**
