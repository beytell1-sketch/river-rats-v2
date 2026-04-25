---
date: 2026-04-26
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #6 — Stage 3.5 commit 13.3.5 (`2e89479`); FINAL 13.3 sub-batch (wrap-up + 6 NITs)
status: APPROVE — all 7 review items OK with HIGH confidence; no required fixes; one cosmetic observation (test docstring); 13.3 corpus sufficiently sealed for Stage 3.5 → commit 14 transition; orchestrator can merge with --merge --delete-branch
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/6
---

# GTO Review Verdict — PR #6 (Commit 13.3.5, FINAL 13.3 Wrap-Up)

## Provenance note

Same provenance pattern as the 13.2.5 / PR #1-5 verdicts: dispatched as general-purpose subagent with the `gto-expert` persona embedded verbatim, per owner's standing in-session authorisation while the dedicated subagent dispatch path is unavailable.

**Process tightenings applied:** read-only brief explicit (Read/Grep/Glob/Bash only; no Write/Edit; return verdict via message body). Agent correctly returned verdict via message — no file writes. Verdict authored on master per `git checkout master BEFORE` recipe.

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item A: 5 chain-step spot-checks (MW-46, MW-50, SYN-F3_HU_folded, FB-25, MW-49) all derive correctly from `_action_to_narrow` + `_collapse_same_street_sequence` semantics. **Verified by reviewer's reading of `range_narrowing.py:739-758` (class normalisation) and `:772-837` (collapse rule).** Builder cross-checked MW-46 chain steps against runtime in 13.3.4 review (matches).
- Reviewer claim Item G: "NIT-1 baseline is pure-function-of-inputs and orthogonal to commit 14's downstream `_per_villain_*` field promotion." **Verified.** `narrow_by_action_history` is at `range_narrowing.py:863-1071`; commit 14 modifies `extract_range_composition` (`feature_extractor.py:1539+`) which CONSUMES the chain output but doesn't feed back into chain computation. NIT-1 assertions stable through commit 14.
- Test suite 14/14 PASS confirmed independently before pre-publish.

All three spot-checks hold against source.

---

## Item A — NIT-1 chain-step content assertions (5 spot-checks)

Reviewer spot-checked 5 representative chain shapes:

**MW-46** (river decision, multi-street collapse): expected `['flop:BET', 'turn:CALL']`. Verified: CO flop=`[BET]` trivial collapse; CO turn=`[CHECK, CALL]` collapses to `[CALL]` via MUST #11 (last-decision-bearing); river excluded. **OK.**

**MW-50** (turn decision, prior-street RAISE): expected `['flop:BET']`. Verified: BTN single-action `RAISE` → `_action_to_narrow('RAISE')` returns `'bet'` per line 750. **OK.** Confirms RAISE→BET class normalisation behaviour.

**SYN-F3_HU_folded** (BB folds flop, prior to turn decision): expected `['flop:FOLD']`. Verified: FOLD path at lines 962-968 returns chain_steps with `'flop:FOLD'`. **OK.**

**FB-25** (CO triple-barrel, prior chain through turn): expected `['flop:BET', 'turn:BET']`. Verified: each street has single CO BET → trivial collapse → `BET` class label. **OK.**

**MW-49** (BB CHECK→CALL collapse on flop): expected `['flop:CALL']`. Verified: collapse drops CHECK (sandbag), keeps CALL (last decisive) → `CALL` class. **OK.**

**Coverage cross-check:** 30 fixture_meta `expects_fire=True` entries == 30 `expected_chain_steps` keys, set-equal. Test 14/14 PASS with new asserts firing.

**Item A overall:** OK
**Confidence:** HIGH

---

## Item B — FB-13 / FB-35 stale prose updates

Both new comments accurately reflect their JSONL `action_string` ground truth:

**FB-13:** `'BB check, CO check, BTN bet 45, BB fold, CO ???'` — new comment "Check-check-bet (BTN c-bet), BB folded; CO closes HU vs BTN bet (BB fold, no call)" matches exactly. Old "bet-and-call" was the bug; corrected.

**FB-35:** `'BB check, CO check, BTN bet 90, BB fold, CO ???'` (turn) — new comment correctly identifies decision is on Turn, BB folded turn (not flop), and that flop must have been check-check-bet-call-call to reach 3-way turn. Match exact.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item C — MW-29 "35 into 155" parenthetical clarification

New form: `Pot odds 22.6% = 35 / (120 preflop pot + 35 CO bet) confirms BTN folded with no caller (post-bet pot 155 is the call denominator)`.

Math: 35 / (120 + 35) = 22.6% ✓. Numerator + denominator components both stated explicitly; trailing parenthetical removes the prior ambiguity of "(35 into 155)".

**Conclusion:** OK
**Confidence:** HIGH

---

## Item D — PR-5 test-comment cleanup

"Wait — let me restate" remark removed; corrected counts (Flop 11 / Turn 6 / River 3 = 20) verified against fixture_meta entry list. Math checks; clean removal.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item E — New test `test_commit13_3_5_villain_pos_map_covers_calibration_entries`

Asserts `set(_CALIBRATION_ACTION_HISTORY) - set(_REFERENCE_VILLAIN_POS) == set()`. Test PASSes against current state (40 calibration ref_ids all in `_REFERENCE_VILLAIN_POS`).

**Cosmetic observation (non-blocking):** docstring says "every MW-* entry" but assertion is broader (all calibration keys). Currently equivalent (all 40 calibration keys are MW-prefixed). If a non-MW prefix ever lands in calibration, either tighten the assertion to MW-prefixed only, or update the docstring. Not a fix-required item.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item F — Scope / no-creep

`git show --stat 2e89479` reports exactly 3 files modified (sidecar + reference_evaluator + test). +76/-10. No drift into renderer/classifier/validator/range_narrowing/feature_extractor.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item G — Sufficiency of NIT-1 baseline capture

Reviewer's analysis: `narrow_by_action_history` is a pure function of `(full_range, board, action_history, villain_pos, decision_street)`. Commit 14 modifies `extract_range_composition` which CONSUMES the chain output downstream — doesn't feed back into chain computation. NIT-1 assertions are stable through commit 14.

If commit 14 modifies `_action_to_narrow`, `_collapse_same_street_sequence`, or street ordering, assertions would fire. But Finding B scope is composition-side field promotion, not narrowing-class semantics.

**Conclusion:** OK
**Confidence:** HIGH

---

## VERDICT

**APPROVE**

**Rationale:** All 7 items pass with HIGH confidence. The 5 spot-checked chain-step assertions correctly derive from documented `_action_to_narrow` + `_collapse_same_street_sequence` semantics. Coverage exact (30 fire-true entries == 30 expected_chain_steps keys). The 4 stale-prose cleanups (FB-13, FB-35, MW-29, test comment) accurately reflect ground truth. New calibration-side villain_pos coverage test PASSes and closes the dual-sidecar gap. Scope clean; NIT-1 baseline forward-stable through commit 14.

**Required fixes:** None.

**Blockers:** None.

**13.3 wrap completeness assessment:** **Corpus sufficiently sealed for Stage 3.5 → commit 14 transition.** Counts lock at 86 reference + 40 calibration; 7 shape buckets; 30 chain-fire entries. NIT-1 is the right regression guard for `narrow_by_action_history` semantics — pure-function-of-inputs, orthogonal to commit 14's downstream field promotion. Carry-forward items (folded_mw classifier promiscuity, mw_per_villain distribution growth, MW-50 RAISE→BET lossiness, delayed_probe MW-41 mis-routing) all correctly deferred to 14.x or v2.5 with documented pointers.

**Cosmetic observation (non-blocking):** new calibration-coverage test docstring says "MW-* entry" but assertion is broader. If non-MW prefix ever lands in calibration, tighten or update docstring. Acceptable for ship.

**Greenlight commit 14:** Yes, conditional on orchestrator merge of PR #6.

---

## Action

**Builder:**
1. Post comment on PR #6 referencing this verdict.
2. Run checkpoint #3 (post-verdict-comment) — UNKNOWN settle to CLEAN per protocol clarification.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check (PR state, branch naming, --merge not --squash, verdict provenance line present).
3. Merge PR #6 with `gh pr merge 6 --merge --delete-branch`.
4. After merge: 13.3 sequence COMPLETE. Issue commit-14 greenlight on `stage3.5/commit-14`. Per the merge directive: PR title MUST cite Finding B; PR body MUST include "unblocks teaching HOLD #5" and "unblocks game per-villain range bars".

**Owner:** sleep. Wake to a sealed 13.3 corpus + commit-14-ready state.

## Reference

- PR #6: https://github.com/beytell1-sketch/river-rats-v2/pull/6
- Greenlight directive: `review/comms/MAIN_TERMINAL_PR_5_MERGED_2026-04-26.md` (`8480b56`)
- Inheritance baseline (PR #5 verdict): `review/comms/GTO_REVIEW_VERDICT_PR_5_2026-04-25.md`
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
- Restart protocol: `review/comms/BUILDER_RESTART_PROTOCOL_2026-04-25.md`
