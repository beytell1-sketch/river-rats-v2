---
date: 2026-04-25
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #1 — Stage 3.5 commit 13.2.6 (`78ca7ae`)
status: APPROVE — all 7 review items OK with HIGH confidence; no required fixes; PR safe to merge; commit 13.3 unblocked pending orchestrator merge
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/1
---

# GTO Review Verdict — PR #1 (Commit 13.2.6)

## Provenance note

Same provenance pattern as the 13.2.5 verdict
(`GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md`): dispatched as
general-purpose subagent with the `gto-expert` persona embedded
verbatim, per owner's in-session override of option (A) session
restart. Tracked at `BUILDER_GTO_DISPATCH_BLOCKED_2026-04-25.md` and
`MAIN_TERMINAL_GTO_DISPATCH_BLOCK_RESOLUTION_2026-04-25.md`. Verdict
header records this honestly.

The reviewer was briefed with the gto-expert persona contract (output
format, judgment-not-arithmetic boundary, read-only scope) and
produced output in the prescribed shape.

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item C: "All 11 entries: sidecar `_REFERENCE_VILLAIN_POS` agrees byte-for-byte with test `fixture_meta` on `villain_pos`." **Verified.** Cross-checked via `git show stage3.5/commit-13-2-6:` of both files; all 11 ref_ids match (MW-11/MW-30/FB-17/FB-23 → CO; MW-15/SYN-F3/SYN-F5/SYN-T_J02/SYN-T_B05/SYN-F7 → BB; SYN-F6 → CO).
- Reviewer claim Item B(c): "the predicate change is isolated to `hu_donk_x_bet` first branch and does NOT touch `hu_bet_x_call_bet`." **Verified.** Diff shows `flop_has_villain_bet` only used in the `hu_donk_x_bet` branch; `hu_bet_x_call_bet` still uses `flop_bet_count >= 1`.
- Reviewer claim Item G: "diff doesn't accidentally touch `validate_sidecar_completeness.py` or the check-through fallback branch." **Verified.** Diff scope is exactly: `_reference_action_history_sidecar.py`, `tests/solver_verify_sidecars.py`, `tests/test_commit13_sidecar_dryrun.py` (3 files; no validator changes; check-through fallback branch unchanged).

All three spot-checks hold against source.

---

## Item A — FIX #1 narrative cleanup

**Data received:** `/tmp/13_2_6_full.patch` lines 80–106, post-fix file at `78ca7ae:river-rats-core/_reference_action_history_sidecar.py:283–303`.

**Reasoning:**
- (a) Stale line ref: pre-fix said `narrow_by_action_history:814`. Post-fix replaces this with "the position filter in narrow_by_action_history's chain loop (only entries with position == villain_pos are kept)". Bare line number gone. ✓
- (b) Chain shape phrasing: post-fix says "with decision_street='turn', the chain loop walks flop ONLY (it breaks before processing decision_street actions per the prior-street-only rule). So the chain is exactly [flop:CALL]; turn:CHECK is on the decision street and does NOT enter the postflop chain." Matches the test-comment phrasing at `test_commit13_sidecar_dryrun.py` ("No turn actions before decision → chain fires flop:CALL only"). ✓
- (c) Historical record of the prior "RAISE-only" mistake retained at the end of the comment — appropriate.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item B — FIX #2 position-aware predicate

**Data received:** `solver_verify_sidecars.py:53–98, 125–138` post-fix.

**Reasoning:**
- (a) New `flop_has_villain_bet = any(e[0]=='flop' and e[2]=='BET' and e[1]==villain_pos)`. For SYN-F7 (villain=BB, flop BB BET) → True. Correctly includes villain-bets-flop. ✓
- (b) For the synthetic mis-route case (villain=BB, flop BTN BET) → flop_has_villain_bet=False. Correctly excludes hero-as-flop-bettor. ✓
- (c) Branch isolation: only `hu_donk_x_bet` first branch uses the new predicate. `hu_bet_x_call_bet` and `hu_bet_raise_call` unchanged. ✓
- (d) Check-through fallback (`flop_check_count >= 1 and turn_check_count >= 1 and river BET`) unchanged — correctly left as pre-existing label-stretch per 13.2.5 INFO note. ✓

**Conclusion:** OK
**Confidence:** HIGH

---

## Item C — `_REFERENCE_VILLAIN_POS` correctness

**Data received:** Sidecar dict at `_reference_action_history_sidecar.py:319–333`; test fixture_meta dict at `test_commit13_sidecar_dryrun.py:261–293`.

**Reasoning:** Cross-checked all 11 entries; sidecar agrees with fixture_meta byte-for-byte. Each villain_pos consistent with the action_history's hero/villain interpretation as documented in per-entry header comments.

| ref_id | sidecar | fixture_meta |
|---|---|---|
| MW-11 | CO | CO |
| MW-30 | CO | CO |
| FB-17 | CO | CO |
| FB-23 | CO | CO |
| MW-15 | BB | BB |
| SYN-F3_HU_folded | BB | BB |
| SYN-F5_HU_overflow | BB | BB |
| SYN-F6_MW_all_live | CO | CO |
| SYN-T_J02_synthetic | BB | BB |
| SYN-T_B05_synthetic | BB | BB |
| SYN-F7_HU_donk_x_bet | BB | BB |

**Conclusion:** OK
**Confidence:** HIGH

---

## Item D — Signature change correctness across call sites

**Data received:** Diff lines 153–252; post-fix `solver_verify_sidecars.py:53–58, 158–177, 213–252`; post-fix `test_commit13_sidecar_dryrun.py:136–162, 180–202`.

**Reasoning:**
- (a) Four call sites of `_classify_shape` post-fix; all updated to pass villain_pos. ✓
- (b) `main()` imports `_REFERENCE_VILLAIN_POS` and threads it to `_stratify(combined, _REFERENCE_VILLAIN_POS)`. ✓
- (c) Existing `test_commit13_2_5_hu_donk_x_bet_bucket_covered` updated to look up villain_pos via `_REFERENCE_VILLAIN_POS['SYN-F7_HU_donk_x_bet']`. ✓
- (d) `_stratify`'s KeyError message names the missing key, the source-of-truth dict, and the file path — actionable. ✓

**Conclusion:** OK
**Confidence:** HIGH

---

## Item E — New tests adequacy

**Data received:** `test_commit13_sidecar_dryrun.py:165–202`, `:212–224`.

**Reasoning:**
- (a) Mis-route fidelity: synthetic AH `[(preflop,BTN,RAISE), (preflop,BB,CALL), (flop,BTN,BET), (flop,BB,CALL), (turn,BB,CHECK), (turn,BTN,CHECK), (river,BB,BET)]` with villain_pos='BB' — exactly the reviewer's described pattern. Pre-fix routes to `hu_donk_x_bet`; post-fix excludes via `flop_has_villain_bet=False`. Test asserts `shape != 'hu_donk_x_bet'`. ✓
- (b) Regression guards on SYN-F7 (still `hu_donk_x_bet`) and SYN-T_J02 (still `hu_bet_x_call_bet`) correctly exercise the post-fix path.
- (c) Coverage test as early-detection guard against `_REFERENCE_VILLAIN_POS` drift before `_stratify`'s KeyError fires at solver-verify time.

Minor observation: the negative assertion `shape != 'hu_donk_x_bet'` is permissive about which bucket the mis-route AH lands in (currently `'other'`). The fix's contract is "exclude from hu_donk_x_bet", not "land in X". Acceptable.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item F — Bucket-distribution stability

**Data received:** Post-fix classifier; the 11 entries' action_histories; `_REFERENCE_VILLAIN_POS` map.

**Reasoning:** Walked each of the 11 entries through the post-fix classifier:

| ref_id | villain_pos | bucket |
|---|---|---|
| MW-11 | CO | mw_per_villain |
| MW-30 | CO | mw_per_villain |
| FB-17 | CO | folded_mw |
| FB-23 | CO | folded_mw |
| MW-15 | BB | mw_per_villain |
| SYN-F3_HU_folded | BB | folded_hu |
| SYN-F5_HU_overflow | BB | hu_bet_x_call_bet |
| SYN-F6_MW_all_live | CO | delayed_probe |
| SYN-T_J02_synthetic | BB | hu_bet_x_call_bet |
| SYN-T_B05_synthetic | BB | hu_bet_raise_call |
| SYN-F7_HU_donk_x_bet | BB | hu_donk_x_bet |

→ 7 distinct buckets, 11 entries. Matches builder's "7-entry stratified sample" claim.

- (a) SYN-F7 still `hu_donk_x_bet` post-fix. No regression on existing donk entry. ✓
- (b) hu_bet_x_call_bet entries (SYN-F5, SYN-T_J02) unaffected by the change. ✓
- (c) No entry was newly mis-routed pre-fix in the dry-run set; the tightening is purely defensive against the 13.3 lift. ✓

**Conclusion:** OK
**Confidence:** HIGH

---

## Item G — Pre-existing concerns NOT addressed

**Data received:** Full diff `/tmp/13_2_6_full.patch`.

**Reasoning:** The two INFO items from the 13.2.5 verdict (check-through variant label-stretch; AST validator blind spots) are NOT touched by this PR — correctly left alone per "13.2.6 should NOT address these (they're optional)". Diff scope is exactly: SYN-T_B05 header narrative cleanup + `_REFERENCE_VILLAIN_POS` dict + `_classify_shape`/`_stratify` signature change + main() threading + 2 new tests + 2 existing-test signature updates. No scope creep.

**Conclusion:** OK
**Confidence:** HIGH

---

## VERDICT

**APPROVE**

**Rationale:** All 7 review items are OK with HIGH confidence. The two required fixes from the 13.2.5 APPROVE_WITH_FIXES verdict are correctly delivered: (1) the SYN-T_B05 header narrative is clean — bare line number replaced by description, chain-shape phrasing now mirrors the test comment ("chain is exactly [flop:CALL]"); (2) the position-aware `flop_has_villain_bet` predicate is correctly threaded through `_classify_shape` and `_stratify` via a single-source-of-truth `_REFERENCE_VILLAIN_POS` dict, with all 11 ref_ids covered, byte-for-byte agreement with the test fixture_meta, no bucket-distribution regression on the dry-run set, and adequate test coverage including a faithful reproduction of the reviewer's mis-route scenario plus regression guards on SYN-F7 and SYN-T_J02. The 13.2.5 INFO items were correctly left untouched (no scope creep). The PR is safe to merge and the 13.3 130-entry authoring lift is greenlit pending orchestrator merge.

**Required fixes:** None.

**Blockers:** None.

---

## Action

**Builder:**
1. Post a comment on PR #1 referencing this verdict (PR-thread audit-trail surface per push-policy directive).
2. Mark task complete; stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Merge PR #1 with `gh pr merge 1 --merge --delete-branch` per push-policy parent directive (`--merge`, NOT `--squash`).
3. After merge: write `MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_<date>.md` authorising the ~130-entry full lift on a new `stage3.5/commit-13-3` feature branch, with per-batch sub-PR cadence and per-batch GTO review pacing.

**Owner:** no action; briefed via PR + this comms doc.

## Reference

- PR #1: https://github.com/beytell1-sketch/river-rats-v2/pull/1
- Driving GTO verdict (13.2.5): `review/comms/GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md` (`00099c6`)
- PR-landed comms doc: `review/comms/BUILDER_PR_1_LANDED_2026-04-25.md` (`34ae0ed`)
- Push-policy parent directive: `review/comms/MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` (`b6c1ade`)
- Push-policy addendum: `review/comms/MAIN_TERMINAL_PUSH_POLICY_ADDENDUM_2026-04-25.md` (`0bb91ef`)
- GTO dispatch authority: `review/comms/MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`)
- Dispatch-block resolution: `review/comms/MAIN_TERMINAL_GTO_DISPATCH_BLOCK_RESOLUTION_2026-04-25.md` (`15f7b07`) — overridden in-session by owner; general-purpose-with-persona authorised
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
