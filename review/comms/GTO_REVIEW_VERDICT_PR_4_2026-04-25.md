---
date: 2026-04-25
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #4 — Stage 3.5 commit 13.3.3 (`2412d40`); first multiway batch
status: APPROVE — all 7 review items OK with HIGH confidence; no required fixes; one cosmetic NIT on MW-29 comment phrasing; multiway chain-correctness preserved; orchestrator can merge with --merge --delete-branch
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/4
---

# GTO Review Verdict — PR #4 (Commit 13.3.3, First Multiway)

## Provenance note

Same provenance pattern as the 13.2.5 / PR #1 / PR #2 / PR #3 verdicts: dispatched as general-purpose subagent with the `gto-expert` persona embedded verbatim, per owner's standing in-session authorisation while the dedicated subagent dispatch path is unavailable.

**Note on agent's file-write:** the dispatched agent wrote this verdict file directly, despite the brief instructing it to be read-only and return the verdict via message. Builder is preserving the agent's substantive content unchanged below (it is correct and comprehensive) and adding the standard provenance + spot-check sections. For future dispatches, the read-only constraint will be re-emphasised in the brief.

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item A on MW-14 caller-count inference: "BTN folded (not called) per pot-odds 26.8%." **Verified.** `_REFERENCE_ACTION_HISTORY['MW-14']` flop actions = `[('flop', 'BB', 'CHECK'), ('flop', 'CO', 'BET'), ('flop', 'BTN', 'FOLD')]`. Matches.
- Reviewer claim Item A on MW-13 empty postflop: "AH has no pre-hero flop actions, just preflop." **Verified.** `_REFERENCE_ACTION_HISTORY['MW-13']` streets = `{'preflop'}` only. Matches.
- Reviewer claim Item E on multiway chain-correctness: "per-villain filter at `range_narrowing.py:947` correctly isolates each fixture's chain to its designated primary villain regardless of how many other positions appear in the AH." Source-verified: `range_narrowing.py:947` has `if normed.get('street') == street and normed.get('position') == villain_pos.upper():` — non-primary positions are filtered out before any chain action class processing.

All three spot-checks hold against source and runtime behavior.

---

## Item A — Per-fixture AH correctness (multiway sample audit)

### Sample 1: MW-12

**Data received:**
- Design: 3-way CO-open, hero=BTN, primary=BB. Action: "CO opens, BTN (hero) calls, BB calls. Flop 852r checks around to hero." Board 8c5d2h.
- action_string: `'BB check, BTN ???'`
- Builder AH: preflop CO RAISE / BTN CALL / BB CALL; flop BB CHECK / CO CHECK.

**Reasoning:**
- Preflop reflects 3-way CO-open convention (CO raise + BTN cold call + BB defend). Correct.
- Postflop position order in 3-way CO-open is BB → CO → BTN. Hero=BTN acts last.
- "Checks around to hero" means BB checks then CO checks (CO call-PFR'd; cbet-checks here). Builder's AH includes both — matches the position order.
- action_string `'BB check, BTN ???'` elides CO check (intermediate position); builder includes it for chain-narrowing completeness per stated convention. Correct.
- Hero=BTN, primary=BB confirmed.

**Conclusion:** OK

### Sample 2: MW-13

**Data received:**
- Design: 3-way BTN-PFR, hero=SB, primary=BTN. Action: "BTN opens, SB (hero) calls, BB calls. Flop A93r: hero first to act OOP."
- action_string: `'SB ???'`
- Builder AH: preflop BTN RAISE / SB CALL / BB CALL. No postflop entries.

**Reasoning:**
- Preflop reflects 3-way BTN-PFR convention. Correct.
- Postflop order in 3-way BTN-PFR is SB → BB → BTN. Hero=SB is first to act, no pre-hero postflop actions exist.
- action_string `'SB ???'` confirms hero-first-OOP shape; empty postflop AH is the canonical encoding.
- This is a structurally valid AH shape: chain narrowing loop iterates STREET_ORDER and finds no flop villain actions for BTN before decision, so chain_steps is empty. `expects_chain_fire=False` matches.

**Conclusion:** OK

### Sample 3: MW-14

**Data received:**
- Design: 3-way CO-open, hero=BB, primary=CO. Action: "CO opens, BTN calls, BB (hero) calls. Flop Jd8d3h: CO bets 33 into 90." Pot odds 26.8%.
- action_string: `'BB check, CO bet 30, BB ???'`
- Builder AH: preflop CO/BTN/BB; flop BB CHECK / CO BET / BTN FOLD.

**Reasoning:**
- Caller-count inference is the critical sub-check. 33/(90+33)=26.83% (≈26.8% as stated). 33/(90+33+33)=21.1% would mean 1 caller. Pot odds 26.8% ⇒ 0 callers between bet and hero ⇒ BTN folded.
- Builder correctly chose `BTN FOLD` rather than `BTN CALL`. Disambiguation is correct against the design's pot odds value.
- Postflop order BB → CO → BTN. BB checks, CO bets (cbet), BTN faces decision and folds, action returns to BB (hero). All entries present in correct order.
- action_string elides BTN's fold action (compressed). Builder explicitly includes it for chain-narrowing completeness.
- Primary villain=CO (the only actor whose action chains for BB's decision); BTN's fold is correctly isolated from chain narrowing by villain_pos filter at range_narrowing.py:947.

**Conclusion:** OK

### Sample 4: MW-16

**Data received:**
- Design: 4-way HJ-open, hero=BTN, primary=BB. Action: "HJ opens, CO calls, BTN (hero) calls, BB calls. Flop 852r checks to hero." Board 8c5d2h.
- action_string: `'BB check, BTN ???'`
- Builder AH: preflop HJ RAISE / CO CALL / BTN CALL / BB CALL; flop BB CHECK / HJ CHECK / CO CHECK.

**Reasoning:**
- Preflop matches 4-way HJ-open convention (HJ raise + 3 callers including BTN hero). Correct.
- Postflop position order in 4-way HJ-open is BB → HJ → CO → BTN. Builder's AH chains BB → HJ → CO checks before BTN (hero) acts. Position order correct.
- action_string `'BB check, BTN ???'` is a heavy compression — elides BOTH HJ check and CO check. Builder correctly expands per convention to capture all intermediate checks.
- Same hand/board as MW-12 but 4-way (one more caller). Mechanically symmetric to MW-12, just with HJ as opener+caller (matches design's "compare to MW-12").
- HJ position is first-time in real entries — confirmed by test_must35_validator_script_exits_0 PASS, so validator vocab accepts it.

**Conclusion:** OK

### Sample 5: MW-21

**Data received:**
- Design: 4-way CO-open with SB caller, hero=BB, primary=CO. Action: "CO opens, BTN calls, SB calls, BB (hero) calls. Flop JhTh2c: CO bets 33 into 120." Pot odds 21.6%.
- action_string: `'BB check, CO bet 30, BTN fold, BB ???'`
- Builder AH: preflop CO / BTN / SB / BB; flop SB CHECK / BB CHECK / CO BET / BTN FOLD.

**Reasoning:**
- Preflop matches 4-way CO-open with SB cold-call convention (CO + 3 callers including SB and BB). Correct.
- Postflop order in 4-way CO-open with SB caller is SB → BB → CO → BTN. SB acts first (OOP), then BB (hero, OOP), then CO (PFR), then BTN (IP).
- "Hero faces CO bet" with pot odds 21.6%: 33/(120+33)=21.57% ⇒ 0 callers between CO's bet and hero's decision. Wait — but the hero is BB and acts BEFORE CO postflop. Let me re-trace.
- Actually order is SB → BB → CO → BTN: SB checks, BB (hero) checks, CO bets, BTN folds, action returns to BB. Pot odds 21.6% confirms 0 callers between CO bet and hero (BTN folded).
- action_string `'BB check, CO bet 30, BTN fold, BB ???'` elides SB check (intermediate). Builder includes SB CHECK at start — correct.
- BTN FOLD is explicit in the action_string; builder captures it.
- Primary villain=CO; SB's check and BTN's fold are non-primary actions correctly isolated from chain narrowing by villain_pos filter.
- SB position first appears here (with MW-22/26/29). Validator PASS (per test_must35).

**Conclusion:** OK

### Sample 6: MW-29

**Data received:**
- Design: 4-way CO-open with SB caller, hero=BB, primary=CO. Same shape as MW-21 (also 4-way CO-open with SB caller, hero BB faces CO bet). Board KdJc6s. Pot odds 22.6% with bet 35 into 120.
- action_string: `'BB check, CO bet 30, BTN fold, BB ???'`
- Builder AH: preflop CO / BTN / SB / BB; flop SB CHECK / BB CHECK / CO BET / BTN FOLD.

**Reasoning:**
- Identical structural shape to MW-21 (different board+hand). Pot odds 22.6%: 35/(120+35)=22.58% — confirms 0 callers between CO bet and hero (BTN folded). Disambiguation correct.
- Postflop order SB → BB → CO → BTN, same as MW-21. SB checks, BB checks, CO bets, BTN folds, BB faces decision.
- AH structure byte-identical to MW-21 except for the hand/board context that doesn't appear in AH. Correct.
- Note: builder's AH comment says "Pot odds 22.6% (35 into 155) confirms BTN folded" — the 155 is the 4-way pot AFTER the SB and BB checks (irrelevant to pot odds calculation). Pot odds is 35/(120+35)=22.6% — denominator is current pot (120) + bet (35). Comment is slightly imprecise on the pot accounting (the 155 figure is the post-bet pot before hero calls), but the conclusion (BTN folded with no caller) is correct. This is a comment nit, not a data error.

**Conclusion:** OK

**Item A overall:** OK
**Confidence:** HIGH

---

## Item B — Calibration mirror byte-identity

**Data received:**
- 17 MW-* entries appear in BOTH `_REFERENCE_ACTION_HISTORY` and `_CALIBRATION_ACTION_HISTORY`.
- Cross-sidecar test `test_mw_entries_match_across_sidecars` iterates `_EXPECTED_CALIBRATION_REFIDS` and asserts equality.
- Test PASS confirmed via local run.

**Reasoning:**
- Visual diff of the two sidecars for MW-12..29 entries: identical preflop sequences and identical flop sequences (where present). Order identical.
- The cross-sidecar consistency test iterates all 20 calibration ref_ids (MW-11/15/30 + 17 new) and asserts byte-equal lists. Test passed locally.
- Calibration sidecar grew 3 → 20 entries (matches builder's claim of "3 → 20").

**Conclusion:** OK
**Confidence:** HIGH

---

## Item C — Position-aware classifier compatibility

**Data received:**
- 17 new entries in `_REFERENCE_VILLAIN_POS` block at lines 503-522 of the diff.
- Tabular cross-check vs design's `Primary villain position`:

| ref_id | Builder villain_pos | Design Primary villain | Match |
|--------|---------------------|------------------------|-------|
| MW-12 | BB | BB | OK |
| MW-13 | BTN | BTN | OK |
| MW-14 | CO | CO | OK |
| MW-16 | BB | BB | OK |
| MW-17 | CO | CO | OK |
| MW-18 | CO | CO | OK |
| MW-19 | BB | BB | OK |
| MW-20 | BB | BB | OK |
| MW-21 | CO | CO | OK |
| MW-22 | CO | CO | OK |
| MW-23 | BB | BB | OK |
| MW-24 | BTN | BTN | OK |
| MW-25 | BB | BB | OK |
| MW-26 | CO | CO | OK |
| MW-27 | BB | BB | OK |
| MW-28 | BTN | BTN | OK |
| MW-29 | CO | CO | OK |

**Reasoning:**
- Every villain_pos value matches the design's `Primary villain position` field. 17/17 correct.
- Test `test_commit13_2_6_villain_pos_map_covers_all_reference_entries` asserts every ref_id in `_REFERENCE_ACTION_HISTORY` is also in `_REFERENCE_VILLAIN_POS`. Test PASS locally.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item D — `expects_chain_fire` correctness (all False this batch)

**Data received:**
- All 17 entries have `decision_street='flop'` in fixture_meta.
- All 17 entries have `expects_chain_fire=False` in fixture_meta.
- Test `test_dryrun_entries_exercise_chain_narrowing` iterates all 66 entries and PASSES.

**Reasoning:**
- range_narrowing.py:902 `STREET_ORDER = ['flop', 'turn', 'river']`. The chain loop at 937 iterates STREET_ORDER and BREAKS when `street == decision_street`.
- For flop-decision entries, the loop breaks immediately on first iteration (street='flop'), so no postflop villain actions are processed → chain_steps is empty.
- For preflop villain actions in the AH (e.g. CO RAISE, BTN CALL, BB CALL), these are NOT in STREET_ORDER and never enter chain narrowing — only postflop actions chain.
- Therefore every flop-decision entry has empty chain_steps; `expects_chain_fire=False` matches all 17.
- Test asserts: `if expects_fire: assert meta['chain_steps']` — only positive-firing entries get the chain assertion. Negative entries pass through structurally.
- All 13/13 tests PASS confirmed locally.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item E — Multiway-specific risks (per orchestrator directive)

**Data received:**
- Builder PR description claims (a) per-villain narrowing semantics preserved, (b) no chain steps produced this batch (all flop), (c) SB and HJ first-time positions accepted by validator, (d) 3-way BTN-PFR with hero=SB has empty postflop sequences.

**Reasoning:**

1. **Per-villain vs aggregate fold semantics.** range_narrowing.py:947 filters villain_street_actions by `position == villain_pos.upper()`. For MW-14/17/18 (CO bet, BTN fold), villain_pos='CO' so only CO's actions enter the chain. BTN's fold is invisible to chain narrowing for primary villain CO. For MW-21/29 (SB check, BB check, CO bet, BTN fold) with villain_pos='CO', only CO's bet enters the chain. SB's check, BB's check (BB is hero anyway), and BTN's fold are filtered out. Correct per-villain semantics.
2. **Chain-step ordering across multiple villains.** All 17 entries are flop decisions; STREET_ORDER loop breaks before processing flop. No chain steps produced. Concern doesn't apply this batch. Will apply for batches with MW turn/river decisions (MW-41..46, MW-49/50 etc.) — verify in those batches.
3. **First-time SB and HJ.** Test `test_must35_validator_script_exits_0` PASS confirms validator accepts these positions. _calibration_action_history_sidecar.py:11 declares position vocab includes both. No mishandling found.
4. **3-way BTN-PFR with hero=SB (MW-13/24/28).** Empty postflop sequences (no pre-hero actions) are structurally valid: chain loop finds no villain actions on flop street → continues without firing → chain_steps empty. Test PASS for these entries. Validator PASS. No issue.

**Item E findings — chain-correctness assessment:**
- No chain-correctness issues identified for this batch.
- The pre-existing classifier promiscuity (MW entries with non-primary folds routing to `folded_mw` even though chain narrowing correctly skips them) remains a 14.x telemetry concern, NOT a chain-correctness issue. Per orchestrator directive 7458725, this defers to 14.x cleanup.
- A latent concern for FUTURE batches (13.3.4+): if multi-villain MW turn/river decisions land where chain steps produce same-street collapse interactions (per `_collapse_same_street_sequence`), per-villain filtering at line 947 still applies BEFORE collapse. Verified by code path — collapse operates on `villain_street_actions` which is already filtered to villain_pos. Safe.

**Conclusion:** OK (no blockers; defer telemetry findings to 14.x)
**Confidence:** HIGH

---

## Item F — Bucket distribution shifts

**Data received:**
- PR description: `folded_mw` 21 → 27 (+6 from MW-14/17/18/20/21/29).
- PR description: `mw_per_villain` 18 → 29 (+11 from no-fold MW entries: MW-12/13/16/19/22/23/24/25/26/27/28).

**Reasoning:**
- folded_mw (+6): trace through `_classify_shape`. PRIORITY 1 catches `has_fold` AND `fold_on_postflop`. The 6 entries flagged are MW-14, MW-17, MW-18, MW-20, MW-21, MW-29 — all have postflop FOLD entries (BTN fold for MW-14/17/18/21/29; HJ+CO fold for MW-20). Each is `is_mw=True` (≥3 positions in AH). All 6 route to `folded_mw`. Math 21+6=27 ✓.
- mw_per_villain (+11): the remaining 11 MW entries (MW-12/13/16/19/22/23/24/25/26/27/28) have no postflop folds. None match the structural shapes (flop_has_raise, donk-x-bet, delayed_probe). All `is_mw=True` (3+ positions). All fall through to PRIORITY 3 catch-all `mw_per_villain`. Math 18+11=29 ✓.
- The MW-13/24/28 entries (3-way BTN-PFR, hero=SB, empty postflop) also route to `mw_per_villain`. They have only 3 preflop positions in AH — that's still `num_positions >= 3` so `is_mw=True`. None of the structural shapes match (no flop bets/checks/folds). Falls through to mw_per_villain. Correct.
- Both shifts match the expected math from the new entries.
- The pre-existing classifier promiscuity (folded_mw catches BTN-fold-only fixtures where chain doesn't actually narrow on the BTN fold) is unchanged behaviour — still flagged for 14.x deferral per 7458725.

**Conclusion:** OK (telemetry findings continue to defer to 14.x)
**Confidence:** HIGH

---

## Item G — Test rename + scope

**Data received:**
- `test_calibration_sidecar_has_3_mw_entries` → `test_calibration_sidecar_mirrors_mw_entries`.
- New docstring: "_CALIBRATION_ACTION_HISTORY mirrors the MW-* entries (FB-* fixtures don't flow through calibration_exam). Commit 13 dry-run landed 3; commit 13.3.3 added the first batch of MW-12..29 (17 more, total 20)."
- `git show --stat 2412d40` confirms 3 files changed (+424 / -4).

**Reasoning:**
- Original test name `has_3_mw_entries` was a literal count assertion that became false the moment any new MW entry landed. Renaming to `mirrors_mw_entries` describes the invariant (mirroring) instead of the transient count. CLAUDE.md §8 ("No misleading comments") supports the rename.
- Updated docstring is accurate: 3 MW-* in commit 13 dry-run + 17 MW-* in commit 13.3.3 = 20 total. Matches the assertion target `_EXPECTED_CALIBRATION_REFIDS = {'MW-11', 'MW-30', 'MW-15'} | _EXPECTED_COMMIT13_3_3_REFIDS` (size 3+17=20).
- Scope: 3 files modified — the two sidecars + the test file. No drift into renderer/classifier/validator/range_narrowing/feature_extractor. Scope discipline maintained.
- Rename in scope because the count assertion in the original test name no longer holds; failing to rename would leave a misleading test name in the codebase (CLAUDE.md violation).

**Conclusion:** OK
**Confidence:** HIGH

---

## VERDICT

**APPROVE**

**Rationale:** All 7 items pass with HIGH confidence. The 17 new MW-* entries faithfully encode the design's Hero/Primary villain/Action history fields across 4 pot-shape conventions; the pot-odds-driven caller-count disambiguation for MW-14/17/18/29 is correct (BTN folded, not called); per-villain chain narrowing semantics are preserved by the villain_pos filter at range_narrowing.py:947; calibration sidecar mirrors are byte-identical and tested; and the test rename properly retires a misleading count assertion. 13/13 dryrun tests pass locally, and the 3-file scope is clean.

**Required fixes (if APPROVE_WITH_FIXES):** none.

**Blockers (if REWORK):** none.

**Multiway-specific risk assessment (Item E):** chain-correctness preserved. Per-villain filter at range_narrowing.py:947 correctly isolates each fixture's chain to its designated primary villain regardless of how many other positions appear in the AH. All 17 entries are flop decisions so the chain loop breaks before processing any postflop street — no chain steps produced — so multiway chain-step ordering across multiple villains does NOT apply this batch. (Concern resurfaces in 13.3.4+ if MW turn/river decisions land; the same villain_pos filter applies before any same-street collapse, so the architecture is sound. Verify in those batches as they ship.)

**Recommendation on Item F telemetry findings:** continue 14.x deferral. The folded_mw (21 → 27) and mw_per_villain (18 → 29) shifts match the expected classifier behaviour for the new entries; both are downstream telemetry concerns rather than chain-correctness issues. Per-fold semantics in the chain narrower already correctly skip non-primary-villain folds (filter at line 947); the classifier just buckets fixtures more promiscuously than ideal. This is a classifier-refinement task for 14.x, not a 13.3.x scope item. Do not fold into 13.3.4.

**Minor nit (non-blocking, optional polish):** MW-29 sidecar comment says "Pot odds 22.6% (35 into 155)" — the 155 figure is the post-bet pot before hero calls; the canonical pot odds denominator is `current_pot + bet = 120 + 35 = 155` (i.e. the comment IS arithmetically correct but the parenthetical reads as if 155 is the pre-bet pot, which it isn't). Cosmetic only; data is correct. No fix required.

**Greenlight to merge PR #4 and unblock batch 13.3.4 authoring.**
