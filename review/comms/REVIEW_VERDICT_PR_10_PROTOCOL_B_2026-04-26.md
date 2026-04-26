---
date: 2026-04-26
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable; persona spec embedded per builder dispatch)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #10 — Stage 4 Protocol B v1.0 fill (`25fc24a`)
status: APPROVE-WITH-NITS — 9 of 10 review items OK with HIGH/MEDIUM confidence; one MEDIUM-severity finding on Example 1 internal consistency (Step 2 narrative contradicts Step 3 conclusion) and one MEDIUM on Anti-pattern #7 vs Example 2 tension; one MEDIUM on verbatim-inlining for pilot build. No blockers for owner review of the v1.0 design artifact. Composition-first reasoning is genuine, schema verification holds, Outcome 4B preserves divergence signal.
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/10
branch: stage4-prep/protocol-b-fill
artifact: prompts/protocol_b_composition_first_v1_0.md (1068 lines)
predecessor: prompts/stage4_drafts/protocol_b_composition_first_v0_1_DRAFT.md (351 lines)
---

# Review Verdict — PR #10 (Stage 4 Protocol B v1.0)

## Provenance note

Read-only review per builder dispatch. Verdict returned via message body; builder writes this comms doc. Reviewer is independent of v1.0 author (different general-purpose subagent dispatch). All file reads from working tree at `25fc24a` HEAD of `stage4-prep/protocol-b-fill`. No solver access used; poker judgment applied per gto-expert persona.

## Builder verification spot-checks (pre-publish)

- v0.1 → v1.0 diff: confirmed all 5 placeholder blocks in v0.1 (`GTO-EXPERT REVIEW NEEDED` ×4, `TODO` ×1) are addressed in v1.0; no leftover placeholders. **Verified by `wc -l` and grep on v1.0**.
- `gto_model.py:33-62` — `FEATURE_COLUMNS` is 55-tuple ending at `board_adjusted_hrp`. Author's "Protocol B does NOT add" claim verified.
- `assemble_pilot_data.py:929-940` — `write_attention_csv` builds `FEATURE_COLUMNS + attn_{...} + label`; no protocol/composition columns. Verified.
- `train_v2_3_2.py:91` — `split_feature_columns(list(rows[0].keys()))` consumes only raw + attn; Protocol B metadata invisible.
- `range_narrowing.py:115` — `RIVER_BETTING_FREQUENCIES['medium_made'] = 0.15` (MUST #50). Threshold-D citation accurate.

All spot-checks hold.

---

## Item A — Composition-first reasoning vs disguised rule-first

**OK / HIGH confidence.** Examples 1, 3, 5 cleanly derive action FROM composition before invoking buckets. Examples 2 and 4 (Outcome 4B cases) keep composition primary in Steps 1-3 with the bucket arriving in Step 4. Anti-pattern #1 explicitly forbids the rule-first-in-disguise failure mode and none of the examples produce it.

**Caveat:** Example 2 cites pot-odds math in Step 3, which Anti-pattern #7 ("equity-vs-pot-odds conflation with composition") explicitly forbids in Steps 1-3. Internal tension between worked example and anti-pattern. Flagged as MEDIUM under Item F.

## Item B — Threshold values vs solver-grounded analysis

**OK-with-caveats / MEDIUM confidence.**

| Threshold | Verdict | Reasoning |
|---|---|---|
| 0.55 air | OK / MEDIUM | Sound for 3-way joint-fold barrier; slightly conservative |
| 0.40 draws | OK / HIGH | Anchored to KB §"Bluff-to-Value Ratio" + KB §1.7 + 3-way two-tone-flop empirics |
| 0.35 TP+ | OK-with-caveat / MEDIUM | Author's own UNCERTAIN flag valid — the 0.34/0.35 boundary risks mis-classifying CHECK-leaning shapes as MIXED |
| 0.40 medium | OK-with-caveat / MEDIUM | Direction right; "pot-controlling sizing typically dominates" overstates implication when hero is strong-made (Example 1 itself shows thin-value-bet works) |

No threshold would mis-classify a clear BET as a CHECK. The MIXED shape is explicitly valid (Anti-pattern #4). Reviewer agrees with author's UNCERTAIN flags — pre-pilot solver verification on d-series spots is warranted.

## Item C — Cross-protocol divergence detection preserved

**OK / HIGH confidence.** Outcome 4B preserves divergence in TWO ways even when action defaults to bucket-aligned:
1. `composition_derived_candidates` always carries the composition-derived action (v1.0 lines 246-247).
2. `composition_rule_conflict = true` flag fires on every 4B outcome (v1.0 line 233 + Anti-pattern #3 + line 381-383).

Stage 4's pilot can adjudicate two distinct signals: (a) `action` agreement A vs B, and (b) `composition_derived_candidates[0]` vs A's-bucket-action. Signal (b) is the inter-protocol-divergence diagnostic. Three exception paths (kb_cited / anchor_match / escalate) further allow composition-derived action to win the `action` field when justified — protocol is not a rubber-stamp.

NIT: 4B rate is not constrained or estimated; if pilot data has <5% 4B hands the cross-protocol signal becomes statistically thin. Suggest 4B-rate floor as a pilot design parameter (Task 5 scope).

## Item D — Worked examples poker-rigour

**Mixed: 4/5 OK, Example 1 has MEDIUM internal-consistency issues.**

- **Example 1 (MEDIUM):** "Pot 80, SPR ~1.25" on turn doesn't match the action sequence "CO opens, BTN call, BB call → flop checks through" at 100bb stacks (preflop pot ~9-12bb, flop pot unchanged → turn pot ~9-12bb, not 80). Pot 80 + SPR 1.25 implies stacks ~100 behind, only consistent with ~180bb effective. Step 2 also contains unfinished editorial drift ("wait, hero is TPGK against a turned flush; actually..."). Reads as draft mid-revision.
- **Example 2 (NIT on arithmetic):** Pot odds 30/(30+90) = **0.25** not 0.18; surplus then 0.15 not 0.22. Direction of conclusion (CALL profitable) holds via MW-30 anchor; arithmetic does not.
- **Example 3 (OK / HIGH):** KQ on Ks Ts 3h 3-way checked-to-BTN. Composition pcts and equity ~0.62 plausible; BET 66% is solver-aligned (per `feedback_solver_aligned_sizing.md` flop sizes).
- **Example 4 (OK / MEDIUM):** Constructed (not corpus). Qualitative reasoning realistic for d8886-class mixed 50/50 spot.
- **Example 5 (OK / HIGH):** Per-villain post-fold MW with nut-flush blocker. Reasoning chain rigorous; chain-narrowed pcts and worse_hand_pct ~0.66 plausible; BET 33% follows.

## Item E — Calibration grading rubric workability

**OK / MEDIUM-HIGH confidence.** 4-tier rubric (STRONG / OK / WEAK / FAIL) with mostly disjoint signals. Mental grading of all 5 worked examples lands STRONG. Boundary risks where two graders might disagree: STRONG vs OK on "first 1-2 sentences cite ≥3 pcts" (count of sentences is interpretable); WEAK vs FAIL on "primary justification" judgment-dependence. The κ ≥ 0.65 target is author-flagged UNCERTAIN with appropriate caveat. Two graders would land same tier ~75-85% on most traces — close to ≥80% target; borderline cases use third-grader resolution. Pass criterion (≥3 STRONG, 0 FAIL on 5 trace-graded hands) is sensible.

## Item F — Anti-pattern list completeness

**OK with one MEDIUM tension / MEDIUM-HIGH confidence.** All 10 anti-patterns cover major failure modes. **Anti-pattern #7 (equity-vs-pot-odds conflation in Step 1-3) has internal tension with Example 2** which uses pot-odds math in Step 3 to derive surplus. Either #7 needs a carve-out for "equity-derived-from-composition pot-odds math is allowed in Step 3 for MW-30-style anchor cases" OR Example 2 should defer math to Step 4. As written, Example 2's own trace would FAIL grade against #7.

**Possible missing #11:** "Don't mix per-villain and merged composition in the same trace without naming which you're using." MUST #46 folded-villain handling is mentioned in Step 1 but not its own anti-pattern. NIT-level.

No false-positive anti-patterns in the list itself.

## Item G — Schema/CSV compatibility verification

**OK / HIGH confidence.** Author's "zero trainer-side changes" claim verified end-to-end:
- `gto_model.py:33-62` FEATURE_COLUMNS unchanged
- `assemble_pilot_data.py:929-940` write_attention_csv excludes Protocol B metadata
- `export_3way_training.py:64` fieldnames excludes Protocol B metadata
- `train_v2_3_2.py:91` reads only raw + attn columns

Author's UNCERTAIN flag about `train_v2_4.py` not existing (verified — only `train_v2_3_1.py` and `train_v2_3_2.py` on disk) is correctly conservative. Compatibility argument extends to v2.4 IF v2.4 follows same FEATURE_COLUMNS + attn_* contract (design intent per Stage 5 plan, not yet code-verified). Honest flag.

## Item H — UNCERTAIN tag rigor

**OK / HIGH confidence.** All 5 UNCERTAIN tags are legitimate. Reviewer found no under-tagging or over-tagging. 5 UNCERTAINs in 1068 lines is right-sized.

## Item I — Inheritance-by-reference vs verbatim copy

**MEDIUM concern / MEDIUM confidence.** v1.0 §"Buckets" / §"Features" / §"DO NOT Rules" reference v3.1 line ranges rather than inlining verbatim. Risk: drift if v3.x evolves. Mitigation: line-pinned references make drift detectable at finalisation.

For a v1.0 design artifact this is acceptable. **For pilot dispatch, recommend producing `v1.0-pilot.md` with v3.1 §"Bucket taxonomy" lines 170-204, §"Features" lines 439-496, §"DO NOT Rules" lines 595-647 inlined verbatim** — separates design artifact (v1.0, references) from labeller-facing artifact (v1.0-pilot, fully inlined). Otherwise labellers chase references during a labelling session.

## Item J — Ready for owner review on pilot dispatch?

**APPROVE for design-artifact review / NOT YET ready for pilot dispatch.**

For owner review of v1.0 as design artifact: yes. For pilot dispatch (when owner authorises Stage 4): three things must be addressed:
1. **Example 1 cleanup** (arithmetic + drift) — labellers will read this as template
2. **Verbatim inlining** (v1.0-pilot.md build step)
3. **Anti-pattern #7 vs Example 2 reconciliation**

Remaining items (threshold solver-verification, κ tuning, calibration exam construction) are owner-acknowledged next steps in the review chain.

---

## VERDICT

**APPROVE-WITH-NITS — overall confidence HIGH.**

**Rationale:** The v1.0 fill is substantive, mostly-rigorous expansion of the v0.1 skeleton. Composition-first reasoning is genuine, schema verification holds end-to-end against the v2.3.2 trainer, Outcome 4B preserves cross-protocol signal, calibration rubric is workable, anti-pattern list covers major failure modes.

**Required fixes for design-artifact ship:** None.

**Required fixes for pilot dispatch:** 3 MEDIUM items (Example 1 cleanup, Anti-pattern #7/Example 2 tension, verbatim inlining). All addressable in v1.1 or pilot-build pass; none blockers for owner v1.0 review.

**Blockers:** None.

**Stale-tree recovery:** N/A (single new file, no production paths touched).

## NIT-level observations (non-blocking)

1. Example 2 pot-odds arithmetic: 30/(30+90) = 0.25, not 0.18. Surplus then 0.15, not 0.22.
2. Example 1 narrative parenthetical reads as draft text.
3. v1.0 line 551 typo: "per village" → "per villain".
4. Threshold "≥0.40 medium → pot-controlling typically dominates" overstates action implication.
5. Anti-pattern #7 too strict given Example 2.
6. §"Buckets/Features/DO NOT" use deferred verbatim-copy.
7. Suggest 4B-rate floor as pilot design parameter (Task 5 scope).
8. Suggest action-history-blindness anti-pattern (#11) for v1.1.

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | MEDIUM | Fix Example 1 pot/SPR arithmetic + remove mid-thought drift (pre-pilot edit on v1.0 or v1.1) |
| 2 | MEDIUM | Resolve Anti-pattern #7 vs Example 2 tension |
| 3 | MEDIUM | Produce v1.0-pilot.md with v3.1 buckets/features/DO-NOT-rules inlined verbatim (pre-pilot build step) |
| 4 | LOW (author-flagged) | Solver-verify thresholds 0.35 TP+ and 0.40 medium against d-series anchors before pilot |
| 5 | NIT | Fix Example 2 pot-odds arithmetic (0.25 not 0.18) |
| 6 | NIT | Fix typo line 551 "per village" → "per villain" |
| 7 | NIT | Consider adding action-history-blindness anti-pattern (#11) |
| 8 | NIT | Add 4B-rate floor as pilot design parameter (Task 5 scope) |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_10_PROTOCOL_B_2026-04-26.md`.
2. Post comment on PR #10 referencing the verdict.
3. Stand by for orchestrator merge.
4. Action items 1-3 (MEDIUM) recommended for follow-up commit before pilot dispatch — owner gate.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check.
3. Merge PR #10 with `gh pr merge 10 --merge --delete-branch` if APPROVE-WITH-NITS is acceptable for design-artifact ship (NITS are pre-pilot fixes, not pre-merge fixes).
4. After merge: builder may proceed to Task 2 (Protocol C).

**Owner:** wake to find Protocol B v1.0 design artifact landed with reviewer-flagged action items for pre-pilot fixes. v1.0 is suitable for design review; pre-pilot polish required before first labeller use.

## Reference

- PR #10: https://github.com/beytell1-sketch/river-rats-v2/pull/10
- Feature commit: `25fc24a`
- Source DRAFT: `prompts/stage4_drafts/protocol_b_composition_first_v0_1_DRAFT.md`
- Output: `prompts/protocol_b_composition_first_v1_0.md`
- Directive: `review/comms/MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md`
- Builder scope: `review/comms/BUILDER_STAGE4_PREP_SCOPE_2026-04-26.md` (`1c63d93`)
- gto-expert persona: `~/river-rats-v2/.claude/agents/gto-expert.md`

**FINAL VERDICT: APPROVE-WITH-NITS — HIGH confidence overall. v1.0 design-artifact ship-ready; v1.1/pilot-build pass needed before pilot dispatch.**
