---
date: 2026-04-25
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Post-merge GTO audit verdict on Stage 3.5 commit 13.2.5 (`bf4b24e`)
status: APPROVE_WITH_FIXES — 1 required narrative-cleanup fix + 1 pre-13.3 defensive classifier tightening; commit is structurally sound; orchestrator can greenlight 13.3 contingent on the fix-forward (13.2.6) landing
---

# GTO Review Verdict — Commit 13.2.5

## Provenance note

The dedicated `gto-expert` subagent at `~/river-rats-v2/.claude/agents/gto-expert.md` is not registered in the current builder session (subagent availability is set at session-launch cwd, not by file presence). Per `BUILDER_GTO_DISPATCH_BLOCKED_2026-04-25.md` and the resolution at `MAIN_TERMINAL_GTO_DISPATCH_BLOCK_RESOLUTION_2026-04-25.md` (`15f7b07`), the orchestrator's standing recommendation was option (A) — restart from v2 cwd. Owner overrode in-session with "no session restart, continue here," which authorises option (B) — general-purpose dispatch with the gto-expert persona embedded verbatim. Provenance recorded honestly per `BUILDER_GTO_DISPATCH_BLOCKED_2026-04-25.md` §"Resolution paths."

The reviewer was briefed with the gto-expert persona contract (output format, judgment-not-arithmetic boundary, read-only scope) and produced output in the prescribed shape. Verification spot-checks below confirm the reviewer's two specific line-reference claims were correct (per `feedback_verify_source_not_plan.md`).

## Builder verification spot-checks (pre-publish)

- Reviewer claim: "Line 306 of `_reference_action_history_sidecar.py` references `narrow_by_action_history:814`, but the actual position filter is at line 947." **Verified.** `grep -n "narrow_by_action_history\|814" _reference_action_history_sidecar.py` shows the comment at line 306; `grep -n "position.*villain_pos" range_narrowing.py` shows the position filter at line 947.
- Reviewer claim: "Lines 309–310 contain an ambiguous parenthetical implying turn:CHECK enters the chain when decision_street='turn'." **Verified.** Source reads: `# Chain for villain BB is flop:CALL + (turn-CHECK is decision-/ # street chain step on turn if decision_street=='turn').` Per code at `range_narrowing.py:937–941`, the chain loop breaks BEFORE the decision_street, so turn:CHECK does NOT enter the postflop chain when decision_street='turn'.

Both findings hold up to source-file scrutiny.

---

## Item 1 — FIX #1 (SYN-T_B05 header comment — BET-RAISE-CALL collapses to CALL)

**Data received:**
- Diff lines 178–187 of `/tmp/bf4b24e_full.patch`
- Sidecar header at `_reference_action_history_sidecar.py:299–320`
- `_collapse_same_street_sequence` at `range_narrowing.py:772–837`
- `narrow_by_action_history` chain loop with position filter at `range_narrowing.py:937–956`
- Test fixture meta `'SYN-T_B05_synthetic': (['Kh','7d','2c','9s'], 'BB', 'turn', True)` at `tests/test_commit13_sidecar_dryrun.py:218`

**Reasoning:**
1. Walk the chain logic with villain_pos='BB', decision_street='turn':
   - Loop iterates flop only (turn = decision_street → break).
   - flop position filter (line 947) keeps only entries with `position == 'BB'` → `[('flop','BB','BET'), ('flop','BB','CALL')]`. BTN's RAISE is filtered out. Narrative claim is mechanically correct.
2. `_collapse_same_street_sequence` walks BB's sequence `[BET, CALL]`:
   - BET classified as 'bet' → decisive, `last_decisive_idx=0`.
   - CALL classified as 'call' → decisive, `last_decisive_idx=1`.
   - Returns `[actions[1]]` = `[CALL]`. Confirms `[BET, CALL]` collapses to CALL, not RAISE.
3. Two narrative roughnesses in the corrected comment:
   - Line 306 references `narrow_by_action_history:814`; actual line is `:947`. Stale line number — drifted post-write.
   - Lines 309–311 say "Chain for villain BB is flop:CALL + (turn-CHECK is decision-street chain step on turn if decision_street=='turn')." Reads ambiguously as if turn:CHECK enters the chain. Per code (line 938–941) the loop breaks before turn when decision_street='turn', so turn:CHECK does NOT enter the postflop chain. Test comment at lines 215–218 phrases it correctly: "No turn actions before decision → chain fires flop:CALL only."

**Conclusion:** FIX-NEEDED (cosmetic — narrative roughness; not a code/semantic bug)
**Confidence:** HIGH

---

## Item 2 — FIX #2 (SYN-F5 chain comment — 2 steps, river is decision-street)

**Data received:**
- Diff lines 110–131 of patch
- Sidecar header at `_reference_action_history_sidecar.py:213–240`
- Chain-loop break-on-decision at `range_narrowing.py:937–941`
- Test fixture `'SYN-F5_HU_overflow': (['Kh','7d','2c','9s','5h'], 'BB', 'river', True)`

**Reasoning:**
1. With decision_street='river', chain walks flop → turn → break at river. Actions on river are NOT chained.
2. flop villain BB actions = [CHECK, CALL] → collapse to [CALL] → chain: flop:CALL.
3. turn villain BB actions = [CHECK, CALL] → collapse to [CALL] → chain: turn:CALL.
4. Chain length = 2. Header now reads "chain is 2 steps (flop:CALL + turn:CALL), not 3."
5. Prior `# chain step 3: river:BET narrows to polarized` was the bug; new tag `# DECISION-STREET (excluded from chain per gate; enters via facing_bet)` is consistent with code.
6. The "prior-street-only" framing matches `narrow_by_action_history`'s docstring: "Walks streets flop → turn → river up to (but NOT including) actions on `decision_street`."

**Conclusion:** OK
**Confidence:** HIGH

---

## Item 3 — FIX #3 (SYN-F7_HU_donk_x_bet entry authored)

**Data received:**
- Diff lines 134–159 of patch
- Entry at `_reference_action_history_sidecar.py:276–297`
- Bucket label at `solver_verify_sidecars.py:40` — "HU donk-flop + turn-check-through + river-bet"
- Classifier at `solver_verify_sidecars.py:113–120`
- New test `test_commit13_2_5_hu_donk_x_bet_bucket_covered` at `tests/test_commit13_sidecar_dryrun.py:145–155`

**Reasoning:**
1. **Shape vs MUST #49 bucket:** bucket label is "HU donk-flop + turn-check-through + river-bet". Entry: BB BET flop, BTN CALL, both CHECK turn, BB BET river. That is exactly donk-flop + turn-check-through + river-bet from villain-BB POV with hero=BTN.
2. **Chain encoding under prior-street-only rule:** decision_street='river'. Chain walks flop, turn:
   - flop villain BB = [BET] → trivial collapse → [BET]. Chain: flop:BET.
   - turn villain BB = [CHECK]. Collapse: only CHECK → keep last (line 833 `actions[-1]`). Chain: turn:CHECK.
   - river: break.
3. Comment "Chain: flop:BET + turn:CHECK (2 prior-street BB actions narrow against the range); river-BET enters via facing_bet gate." is correct.
4. **Classifier routing:** flop_bet_count=1 (BB BET), turn_check_count=2 (BB+BTN CHECK), turn_has_call=False, river BET present → routes to `hu_donk_x_bet` per new branch at lines 116–120.
5. **GTO realism:** donk-flop → turn-check → river-bet is a recognised range-bearing pattern. BB has range advantage on certain low/middling boards (e.g., 86x rainbow vs BTN open) and develops a donk frequency in solver outputs. After donk-call, BB's range is somewhat capped on the turn (no nut over-pairs); the natural play is to check turn, then either give up or value-bet/bluff river depending on the runout. The shape exists and is bucket-distinct from `hu_bet_x_call_bet` (4-class chain) and `delayed_probe` (turn-bet-after-flop-check). PASS.
6. Note: `flop_bet_count >= 1` is position-agnostic in the classifier — see Item 6 for the residual concern about classifier promiscuity.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item 4 — FIX #4 (Authoring-spec docstring update)

**Data received:**
- Diff lines 76–103 of patch
- Sidecar docstring at `_reference_action_history_sidecar.py:40–66`
- Real-fixture board parse at `feature_extractor.py:153–163` (`board_str[i:i+2]` parser → `List[str]` of 2-char cards)
- Synthetic-fixture board form in test_commit13: `['Kh','7d','2c']` etc. at `tests/test_commit13_sidecar_dryrun.py:195–222`
- `_street_board(full_board: List[str], street)` at `range_narrowing.py:761–769` — relies on `[:3]/[:4]/[:5]` slicing, so `List[str]` (3/4/5 elements) is required

**Reasoning:**
1. Docstring claim "fixture_meta board must be List[str]" matches reality: `_street_board` slices a list (passing `'Kh7d2c'` would yield `'Kh7'` — 3 characters not 3 cards — and break narrowing).
2. Docstring also correctly notes that real fixture JSONL stores `board` as a concatenated string with parse upstream — matches `feature_extractor.py:153–163` (`_parse_board_string`).
3. Spec is clear, well-located, and matches the rest of the codebase.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item 5 — FIX #5 (`validate_fixture_meta_boards()` AST validator)

**Data received:**
- Diff lines 296–367 of patch
- Validator function at `validate_sidecar_completeness.py:100–171`
- Current fixture_meta at `tests/test_commit13_sidecar_dryrun.py:192–223` (all 11 entries use `List[str]` format)
- Test `test_commit13_2_5_fixture_meta_boards_list_of_strings` at `tests/test_commit13_sidecar_dryrun.py:158–169`

**Reasoning (mental execution against test cases):**
1. Concatenated string `'Kh7d2c'`: `ast.Constant(value='Kh7d2c')` not `ast.List` → flagged. ✓
2. List of strings `['Kh','7d','2c']`: `ast.List` with three `ast.Constant` value=str length=2 → passes. ✓
3. Tuple `('Kh','7d','2c')`: `ast.Tuple` not `ast.List` → flagged. ✓
4. Set `{'Kh','7d','2c'}`: `ast.Set` → flagged. ✓
5. Variable reference `MY_BOARD`: `ast.Name` → flagged. ✓
6. List comprehension `[c for c in cards]`: `ast.ListComp` → flagged. ✓
7. `['Kh', 7, '2c']` (non-string element): `isinstance(card.value, str)` False → flagged. ✓
8. `['K', '7d', '2c']` (1-char card): `len(card.value) != 2` → flagged. ✓
9. `[f'K{x}', '7d', '2c']` (f-string element): `ast.JoinedStr` → flagged. ✓

**Blind spots (minor, non-blocking):**
- Empty list `[]`: passes List type check; no per-card violations fire. Real-world impact nil (other tests would fail), but validator is silent.
- Dynamically-extended dict (`fixture_meta['NEW'] = ...` post-assignment): walker only inspects dict literal at the `=` site; post-hoc additions slip through. Not a current concern.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item 6 — Classifier disambiguation (`turn_has_call` predicate)

**Data received:**
- Diff lines 193–229 of patch
- Classifier `_classify_shape` at `solver_verify_sidecars.py:53–132`
- All 11 sidecar entries' action histories in `_reference_action_history_sidecar.py`

**Reasoning (boundary-case enumeration):**
1. **SYN-F7 routing under new rule:** flop_bet_count=1, turn_check_count=2, turn_has_call=False, river BET → falls through `hu_bet_x_call_bet` (which now requires turn_has_call) → matches `hu_donk_x_bet` (lines 116–120). Correct.
2. **SYN-T_J02 routing (regression check):** flop:BB BET, turn:BB CHECK + BB CALL (turn_has_call=True), river BET → matches `hu_bet_x_call_bet` (now requires turn_has_call). Unchanged.
3. **Boundary case — turn has BOTH CALL and BET (e.g., flop BET / turn CHECK / turn BET / turn CALL / river BET):** turn_check_count≥1, turn_has_call=True → `hu_bet_x_call_bet`. Shape is a 4-class chain matching the canonical bucket. Correct.
4. **Position-agnostic flop_bet_count promiscuity (residual concern):** `flop_bet_count >= 1` matches whether VILLAIN bet flop or HERO did. For SYN-F7 (BB-bet on flop) it's correct, but during the upcoming 130-entry full lift, real fixtures with hero-as-flop-bettor + villain-river-stab after turn-check-through would mis-route to `hu_donk_x_bet` despite NOT being a donk shape. Recommend tightening with a `villain_donked_flop` predicate (check `e[1] == villain_pos` on the flop BET).
5. **6-bucket collision check vs MUST #49:**
   - `folded_*`: PRIORITY 1 — fires before structural shapes if FOLD postflop. Disjoint from `hu_donk_x_bet`.
   - `hu_bet_raise_call`: requires `flop_has_raise=True`. Disjoint.
   - `delayed_probe`: requires `flop_check_count >= 1` AND turn BET. SYN-F7 has flop_check_count=0. Disjoint.
   - `mw_per_villain`: requires is_mw (3+ positions). HU disjoint.
   - `over_narrow` / `mass_truncation`: runtime sentinels, not authoring shapes.

**Note on check-through fall-through (lines 121–123):** OLD rule `flop_check_count ≥ 1 + turn_check_count ≥ 1 + river BET → hu_donk_x_bet` is retained as fallback for "river-stab-after-double-check-through" — labeling it as `hu_donk_x_bet` is a misnomer. Pre-existing, not introduced by 13.2.5; flag for cleanup in a future commit, not blocker.

**Conclusion:** OK (for SYN-F7 routing); FIX-NEEDED for classifier robustness pre-13.3 (position-agnostic `flop_bet_count` would mis-route hero-bet-flop hands).
**Confidence:** HIGH (on SYN-F7 routing); MEDIUM on full-lift robustness.
**To raise confidence:** confirm no upcoming 13.3 fixture has hero-as-flop-bettor with villain-led river-bet, OR tighten predicate to position-aware `flop_has_villain_bet` before 13.3 lift.

---

## VERDICT

**APPROVE_WITH_FIXES**

**Rationale:** All five fixes (FIX #1–#5) plus the classifier disambiguation are mechanically correct and consistent with the underlying chain code, the prior-street-only rule, MUST #11/#12 collapse semantics, and MUST #49 bucket definitions. SYN-F7 is a faithful donk-x-bet shape; FIX #2 chain-comment is right; FIX #4 docstring matches reality; FIX #5 AST validator covers the stated scope. The two FIX-NEEDED items are: (a) two narrative roughnesses in FIX #1's header comment (stale line-number reference `:814` and an ambiguous parenthetical implying turn:CHECK enters the chain), and (b) a position-agnostic predicate in the classifier that doesn't matter for the current 11 entries but should be tightened before the 130-entry lift. None are blockers; commit 13.2.5 is structurally sound and the orchestrator can greenlight 13.3 contingent on the fix-forward (13.2.6) landing.

**Required fixes (to land as 13.2.6 on `stage3.5/commit-13-2-6` PR per parent push-policy directive):**

1. **FIX #1 narrative cleanup** in `_reference_action_history_sidecar.py:299–320` (SYN-T_B05_synthetic header):
   - Update stale line reference `narrow_by_action_history:814` → `:947` (or remove the bare line number entirely; reference "the position filter in the chain loop" to avoid future drift).
   - Rephrase the ambiguous parenthetical at lines 309–311. Under the actual code, when `decision_street='turn'` the loop breaks BEFORE processing turn, so turn:CHECK does NOT enter the postflop chain. Mirror the test-comment phrasing at `tests/test_commit13_sidecar_dryrun.py:215–218`: "No turn actions before decision → chain fires flop:CALL only."

2. **Classifier predicate tightening** in `solver_verify_sidecars.py:_classify_shape` lines 116–120:
   - The `hu_donk_x_bet` flop-bet branch uses `flop_bet_count >= 1`, which is position-agnostic. For the 13.3 130-entry lift, tighten to a `flop_has_villain_bet` predicate (check `e[1] == villain_pos` on the flop BET). Requires threading villain_pos into the classifier; small change.
   - Alternative path: audit 13.3's authoring list to confirm no fixture has hero-as-flop-bettor with villain-led river-bet pattern. Either approach is acceptable; recommend the predicate fix because it's defensive against future drift.
   - **Note on bundling:** the agent's verdict text is internally ambiguous on whether this is "required for 13.2.5 sign-off" or "required pre-13.3." Builder reading: bundle into 13.2.6 since cost is small and quality default applies; the orchestrator can override if it prefers to defer to a separate `stage3.5/commit-13-2-7` or fold into `stage3.5/commit-13-3` setup.

**Optional cleanup (INFO, not required):**

- The `hu_donk_x_bet` "check-through variant" branch (lines 121–123) labels "flop-check-through + turn-check-through + river-bet" as `hu_donk_x_bet`, a misnomer (no donk involved). Pre-dates 13.2.5; consider renaming to a separate `river_stab_after_check_through` bucket in a future commit.
- AST validator blind spots (empty list, dynamically-extended dicts). Neither affects current state.

---

## Action

**Builder:**
1. Open `stage3.5/commit-13-2-6` per the standing PR pattern from `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md`.
2. Land the two required fixes (FIX #1 narrative cleanup + classifier predicate tightening) on that branch.
3. Open PR to master with title `Stage 3.5 commit 13.2.6/16: APPROVE_WITH_FIXES on 13.2.5 — narrative cleanup + classifier tightening` and body referencing this verdict doc.
4. Per directive: per-batch GTO review on the PR thread (dispatch gto-expert when its dispatch path is back; until then, owner authorises general-purpose-with-persona — same provenance pattern as this verdict).
5. On orchestrator + reviewer APPROVE: `gh pr merge --merge --delete-branch` per push-policy parent directive.

**Orchestrator:**
1. Read this verdict.
2. On 13.2.6 PR opening: standard PR review + greenlight cycle.
3. On 13.2.6 merge: greenlight commit 13.3 authoring per the existing decision tree.
4. Continue tracking the gto-expert dispatch-path resolution (separate from 13.2.5 / 13.2.6 critical path; the option-A session restart can happen at any point and will benefit all future Stage 3.5 reviews).

**Owner:** no action; briefed via this doc and the override message.

## Reference

- `BUILDER_V24_STAGE35_COMMIT_13_2_5_LANDED_2026-04-21.md` — fix list source
- `BUILDER_13_2_5_ON_ORIGIN_GTO_READY_2026-04-25.md` (`7bca96a`) — builder GTO-ready notification
- `BUILDER_GTO_DISPATCH_BLOCKED_2026-04-25.md` (`2a8bc17`) — original BLOCKED comms
- `MAIN_TERMINAL_GTO_DISPATCH_BLOCK_RESOLUTION_2026-04-25.md` (`15f7b07`) — option-A resolution (overridden in-session by owner)
- `MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`) — dispatch authority
- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` + addendum — PR pattern for 13.2.6 onward
- `feedback_quality_default_no_ask.md`
- `feedback_verify_source_not_plan.md` (used in builder spot-checks above)
- `~/river-rats-v2/.claude/agents/gto-expert.md` — persona embedded in the dispatch
