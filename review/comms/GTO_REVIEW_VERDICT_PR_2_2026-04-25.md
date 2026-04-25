---
date: 2026-04-25
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #2 — Stage 3.5 commit 13.3.1 (`04a1181`)
status: APPROVE — all 7 review items OK with HIGH confidence; 3 NITs (advisory-only, none required); GTO recommends Option (3) on classifier-promiscuity finding (defer to 14.x); orchestrator can merge with --merge --delete-branch
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/2
---

# GTO Review Verdict — PR #2 (Commit 13.3.1)

## Provenance note

Same provenance pattern as the 13.2.5 / PR #1 verdicts (`GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md` and `GTO_REVIEW_VERDICT_PR_1_2026-04-25.md`): dispatched as general-purpose subagent with the `gto-expert` persona embedded verbatim, per owner's standing in-session authorisation while the dedicated subagent dispatch path is unavailable. Verdict header records this honestly per the standing discipline.

The reviewer was briefed with the gto-expert persona contract (output format, judgment-not-arithmetic boundary, read-only scope) and produced output in the prescribed shape.

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item C: "FB-18/19/20 chain steps produce specifically `flop:CHECK` / `flop:CALL` / `flop:BET` for primary villain CO/BTN/BTN respectively." **Verified.** Ran `narrow_by_action_history` directly on each entry — output matches exactly.
- Reviewer claim Item A on FB-13: "BB has TWO entries on flop (CHECK then FOLD)." **Verified.** Source shows `('flop','BB','CHECK')` followed by `('flop','BB','FOLD')` after `('flop','BTN','BET')`.
- Reviewer claim Item D: "All 12 entries in `folded_mw` post-batch-1 are non-primary-villain folds." **Verified.** Walked each: FB-01/04/06/10/15 (primary CO, BTN folds), FB-02/11/14 (primary BB, CO folds), FB-13 (primary BTN, BB folds), FB-17 (primary CO, BTN folds turn), FB-20 (primary BTN, BB folds flop), FB-23 (primary CO, BTN folds river). 12/12 confirmed non-primary.

All three spot-checks hold against source and runtime behavior.

---

## Item A — Per-fixture action-history correctness (sample audit)

**Sample 1: FB-01** — 3-way CO-open, flop decision, hero=BB, BTN-folded shape. Reviewer walked AH against `action_string="BB check, CO bet 30, BTN fold, BB ???"`. Postflop order BB→CO→BTN respected. Villain_pos `CO` matches `villain_positions[0]`. **OK.**

**Sample 2: FB-12** — 3-way BTN-PFR, flop decision, hero=BB, check-check-bet shape. AH captures the OOP→middle→IP sequence (BB CHECK, CO CHECK, BTN BET) before hero's pending decision. Villain_pos `BTN` matches `villain_positions[0]`. **OK.**

**Sample 3: FB-13** — 3-way BTN-PFR, flop decision, hero=CO, BTN-bet + BB-folded after. The brief flagged the discrepancy between `_FB_ACTION_HISTORY` prose ("BTN bet, BB folded; CO closes HU vs BTN bet-and-call") and JSONL action_string ("BB check, CO check, BTN bet 45, BB fold, CO ???"). Reviewer confirmed the PR builder correctly followed the JSONL `action_string` as canonical ground truth (no "call" between BTN's bet and BB's fold). The "bet-and-call" prose is stale annotation in `reference_evaluator.py:760` — flagged as NIT-3 below for separate cleanup. **OK (PR followed correct ground truth).**

**Sample 4: FB-19** — 3-way BTN-PFR, **turn decision**, prior flop CO bet + BTN call + BB call. AH correctly captures the 4-action flop sequence + the partial turn sequence ending before hero's `???`. Note: prose says CO's flop bet is a "c-bet" but in a BTN-PFR pot CO's lead is technically a probe — semantic nit, not a correctness issue. Chain step for primary villain BTN: `flop:CALL`. **OK.**

**Sample 5: FB-20** — 3-way → 2-way after fold, **turn decision**, prior flop BTN bet + BB fold + CO call. Most intricate entry: preflop kept as 3-way (correct since BB folds postflop, not preflop); flop captures all 5 actions including the BB FOLD and CO CALL closing flop; turn HU sequence ends before hero's decision. Chain step for primary villain BTN: `flop:BET`. **OK.**

**Item A overall: OK. Confidence: HIGH.**

---

## Item B — Position-aware classifier compatibility

`_REFERENCE_VILLAIN_POS` extended with 19 new entries; cross-checked all against `villain_positions[0]` from JSONL — zero mismatches. All 19 present (test `test_commit13_2_6_villain_pos_map_covers_all_reference_entries` passes). The position-aware `flop_has_villain_bet` predicate is in scope; the `_stratify` KeyError guard won't trip. Prior shipped synthetic + real fixture classifications unaffected.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item C — `expects_chain_fire` correctness

Simulated chain narrowing for all 19 entries against the `narrow_by_action_history` semantics:
- FB-01..16 (`decision_street='flop'`) → chain breaks immediately, no postflop streets walked → `expects_chain_fire=False` ✓ (16/16).
- FB-18 (turn, villain=CO): chain step `flop:CHECK` → fires ✓.
- FB-19 (turn, villain=BTN): chain step `flop:CALL` → fires ✓.
- FB-20 (turn, villain=BTN): chain step `flop:BET` → fires ✓.

Test `test_dryrun_entries_exercise_chain_narrowing` asserts `meta['chain_steps']` non-empty for `expects_fire=True`; all 13 tests pass.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item D — Bucket distribution / classifier promiscuity

**Finding:** 10 of 12 entries in `folded_mw` post-batch-1 are FB-* with non-primary-villain folds (e.g. FB-01: BTN folds, primary villain CO is still live). The classifier rule `if has_fold and is_mw: return 'folded_mw'` doesn't distinguish "primary villain folded" (true sentinel territory) from "non-primary villain folded" (HU-after-fold).

**Reviewer assessment:**
- (a) **Finding correct as described** — all 12 `folded_mw` entries verified to be non-primary-villain folds.
- (b) **Functionally non-blocking** — the chain-narrowing code at `range_narrowing.py:947-948` filters by `villain_pos` BEFORE checking action class, so non-primary folds are correctly skipped from chain logic. Promiscuity affects only stratification labels in `solver_verify_sidecars.py` (used for sampling distribution in solver-verify stub), not chain code or feature extraction.
- (c) **Recommendation: Option (3) — defer to 14.x cleanup.** Rationale:
  - Bug is pre-existing classifier issue surfaced (not introduced) by batch 1's volume.
  - Doesn't affect chain-narrowing correctness, feature extraction, or model training — only stratified-sampling labels in a stub solver-verify.
  - Fix-spec is clear (split `folded_mw` into `folded_mw_primary` vs `folded_mw_offvillain` based on whether `villain_pos in fold_positions`).
  - Carries through batches 13.3.2..5 unchanged because FB-* shape distribution will stay similar.

**Conclusion:** OK (finding accurate, non-blocking; defer to 14.x with explicit tracking)
**Confidence:** HIGH

---

## Item E — 3-way BTN-PFR preflop encoding

PR uses simplified `BTN RAISE + CO CALL + BB CALL` for FB-12/13/19 (real preflop has CO acting before BTN). Reviewer verified:
- `narrow_by_action_history` doesn't walk preflop (`STREET_ORDER = ['flop', 'turn', 'river']`).
- `feature_extractor.py:632-669` `get_villain_range()` uses `opener_pos` from `_FB_OPENER_POSITION` — preflop AH never consulted for range construction.
- `_FB_ACTION_HISTORY` tuple in `reference_evaluator.py:746` provides separate preflop-derived feature signals (villain_aggression_count etc.) — also doesn't read AH preflop entries.
- No tests assert on preflop AH ordering.

Convention is documented inline in the sidecar (`# Convention recap:` block) and in the commit message.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item F — Test coverage adequacy

`test_dryrun_entries_exercise_chain_narrowing` runs `narrow_by_action_history` on each entry and asserts `chain_steps` non-empty for `expects_fire=True`. Structural contract fields (`chain_steps`, `surviving_weight`) asserted present for all entries. 13/13 pass.

**NIT (advisory):** test does NOT assert chain step **content** (e.g., FB-18 should produce specifically `flop:CHECK`, not just non-empty). For batch 1 with 3 turn entries this is low-risk; for batches 13.3.2..5 with more complex chains, recommend adding an explicit chain-step content assertion. Optional addition for 13.3.5 wrap-up.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item G — Scope / no-creep

`git show --stat 04a1181` reports exactly 2 files changed: `_reference_action_history_sidecar.py` (+265 / -0) and `tests/test_commit13_sidecar_dryrun.py` (+41 / -1). No renderer / classifier code / validator / range_narrowing / feature_extractor or other file modified. Classifier-promiscuity finding (Item D) explicitly NOT auto-fixed — appropriate scope discipline.

**Conclusion:** OK
**Confidence:** HIGH

---

## VERDICT

**APPROVE**

**Rationale:** All 19 new entries faithfully encode the JSONL `action_string` ground truth with correct postflop position ordering (BB→CO→BTN), correct hero identification via the `???` marker, and correct primary-villain assignment matching `villain_positions[0]`. Chain narrowing semantics are correctly anticipated (`expects_chain_fire` matches the `decision_street`-prior + `villain_pos`-filter rule for all 19; verified by direct simulation producing `flop:CHECK` / `flop:CALL` / `flop:BET` for FB-18/19/20). The position-aware classifier compatibility is fully preserved; the BTN-PFR preflop simplification is downstream-safe (chain doesn't walk preflop, opener metadata lives in `_FB_OPENER_POSITION` separately). Scope is clean (2 files only). 13/13 dryrun + 32/32 adjacent tests pass.

**Required fixes:** None.

**Advisory NITs (not required for merge, optional follow-up):**

1. **NIT-1:** Future batches 13.3.2+ would benefit from explicit chain-step content assertions in the dryrun test, not just `chain_steps` non-empty (Item F gap). Could be a 13.3.5 wrap-up addition.
2. **NIT-2:** Add one sentence to the inline convention comment in `_reference_action_history_sidecar.py` clarifying that the preflop simplification is safe because the chain doesn't walk preflop (Item E). Already in commit message; mirroring inline would help future authors.
3. **NIT-3 (out of PR scope, separate cleanup):** The `_FB_ACTION_HISTORY` prose comment for FB-13 at `reference_evaluator.py:760` says "bet-and-call" but action_string shows BB folded directly (no call before fold). Stale annotation. Should be cleaned up in a separate prose-fix commit; the metadata field index 3 (`num_callers_to_bet=1`) may also warrant review for FB-13. **Not in PR #2 scope.** PR builder correctly used JSONL action_string as the canonical ground truth.

**Recommendation on Item D classifier-promiscuity finding:** **Option (3) — defer to 14.x cleanup.** The bug doesn't affect chain code, feature extraction, or training — only solver-verify stratification labels. Track as known issue with explicit fix spec for 14.x.

**Greenlight 13.3.2 batch authoring:** Yes, conditional on orchestrator's merge of PR #2.

---

## Action

**Builder:**
1. Post comment on PR #2 referencing this verdict.
2. Run checkpoint #3 (post-verdict-comment) and #4 (pre-merge) per the orchestrator's STOP-extension directive.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check (PR state, branch naming, --merge not --squash, verdict provenance line present).
3. Merge PR #2 with `gh pr merge 2 --merge --delete-branch`.
4. After merge: builder is unblocked to start batch 13.3.2 on `stage3.5/commit-13-3-2`.

**Owner:** no action; briefed via PR + this comms doc.

## Reference

- PR #2: https://github.com/beytell1-sketch/river-rats-v2/pull/2
- 13.3 greenlight directive: `review/comms/MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md` (`e87f371`)
- Inheritance baseline (PR #1 verdict): `review/comms/GTO_REVIEW_VERDICT_PR_1_2026-04-25.md` (`2fc545c`)
- Push-policy parent: `review/comms/MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` (`b6c1ade`)
- GTO dispatch authority: `review/comms/MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`)
- Dispatch-block resolution: `review/comms/MAIN_TERMINAL_GTO_DISPATCH_BLOCK_RESOLUTION_2026-04-25.md` (`15f7b07`)
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
