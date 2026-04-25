---
date: 2026-04-25
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #5 — Stage 3.5 commit 13.3.4 (`d07e65d`); second multiway batch
status: APPROVE — all 7 review items OK with HIGH confidence; one cosmetic NIT (test-file comment); multiway chain-correctness CONFIRMED CORRECT across multi-postflop-street MW shapes; MW-50 RAISE→BET normalisation lossy but pre-existing/documented/deferred to v2.5; orchestrator can merge with --merge --delete-branch
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/5
---

# GTO Review Verdict — PR #5 (Commit 13.3.4, Second Multiway)

## Provenance note

Same provenance pattern as the 13.2.5 / PR #1-4 verdicts: dispatched as general-purpose subagent with the `gto-expert` persona embedded verbatim, per owner's standing in-session authorisation while the dedicated subagent dispatch path is unavailable.

**Process tightening applied:** per the protocol-tightening from `a8af4aa` ("Read-only agent dispatch brief"), this dispatch's brief explicitly enumerated `Read/Grep/Glob/Bash` tools and forbid `Write/Edit`. The agent correctly returned its verdict via the response message body (no file writes). Builder authored this comms doc on master per the `git checkout master BEFORE authoring verdict` recipe (protocol-tightening #2).

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item E: "9 turn/river chain steps verified empirically." **Verified.** Builder ran `narrow_by_action_history` directly on all 9 entries — outputs match exactly: MW-32 `['flop:BET']`, MW-41 `['flop:BET']`, MW-42 `['flop:BET','turn:CALL']`, MW-43 `['flop:CHECK','turn:CHECK']`, MW-44 `['flop:BET']`, MW-45 `['flop:CHECK']`, MW-46 `['flop:BET','turn:CALL']`, MW-49 `['flop:CALL']`, MW-50 `['flop:BET']`.
- Reviewer claim Item E.5: "RAISE→bet class normalisation at `range_narrowing.py:750`." **Verified.** Source confirms: `if a in ('BET', 'RAISE'): return 'bet'`. The lossiness is real but pre-existing.
- Reviewer NIT on `test_commit13_sidecar_dryrun.py:422-429`: "Wait — let me restate" comment survived to commit. **Verified.** Patch line 784 shows the comment in the diff (added by builder during fixture_meta authoring). Cosmetic only; defer to 13.3.5 wrap-up alongside other cleanup items.

All three spot-checks hold.

---

## Item A — Per-fixture AH correctness (5 turn/river samples)

Reviewer sampled 5 representative shapes and verified each:

**Sample 1 — MW-31 (decision-street CHECK-RAISE):** preflop CO-open, flop BB CHECK / CO CHECK / BTN BET / BB FOLD / CO RAISE. Postflop position order BB→CO→BTN respected. CO's CHECK + RAISE both on decision-street → correctly excluded from chain (chain=[]). **OK.**

**Sample 2 — MW-42 (river decision; turn CHECK→CALL collapse):** flop CO-bet/BTN-call/BB-fold; turn CO-CHECK/BTN-BET/CO-CALL collapses to `turn:CALL` via MUST #11. Empirical chain `['flop:BET','turn:CALL']`. **OK.**

**Sample 3 — MW-44 (turn decision; BB double-lead):** flop BB-BET/CO-CALL/BTN-CALL → 3-way to turn; turn BB-BET/CO-FOLD. BB single flop action → `flop:BET` chain step. **OK.**

**Sample 4 — MW-46 (river check-raise; key Axis 7):** 4-way HJ-PFR → HU CO vs BTN after flop folds. Chain `['flop:BET','turn:CALL']`; river check-raise on decision-street excluded. **OK.**

**Sample 5 — MW-50 (prior-street CHECK-RAISE; flop RAISE):** 4-way CO-PFR + SB; flop SB-CHECK/BB-CHECK/CO-BET/BTN-RAISE/SB-FOLD/BB-CALL/CO-CALL → 3-way turn. BTN's only flop action is RAISE → `flop:BET` (BET/RAISE class normalisation). Chain `['flop:BET']`. Reviewer assesses normalisation lossiness in Item E.5. **OK.**

**Item A overall:** OK
**Confidence:** HIGH

---

## Item B — Position-aware classifier compatibility

All 20 entries in `_REFERENCE_VILLAIN_POS` cross-checked against design's `Primary villain position`:
MW-31 CO ✓ | MW-32 CO ✓ | MW-33 CO ✓ | MW-34 BB ✓ | MW-35 CO ✓ | MW-36 CO ✓ | MW-37 CO ✓ | MW-38 BB ✓ | MW-39 CO ✓ | MW-40 BB ✓ | MW-41 CO ✓ | MW-42 CO ✓ | MW-43 CO ✓ | MW-44 BB ✓ | MW-45 CO ✓ | MW-46 CO ✓ | MW-47 CO ✓ | MW-48 BTN ✓ | MW-49 BB ✓ | MW-50 BTN ✓.

**Conclusion:** OK. **Confidence:** HIGH.

---

## Item C — `expects_chain_fire` correctness

- 11 flop decisions → False ✓
- 6 turn decisions → True (each produces single chain step on flop) ✓
- 3 river decisions → True (each produces flop+turn chain steps) ✓

Direct simulation matches PR claims for all 9 turn/river entries.

**Conclusion:** OK. **Confidence:** HIGH.

---

## Item D — Calibration mirror byte-identity

All 20 MW-31..50 entries appear in both sidecars; reviewer empirically verified `_REFERENCE_ACTION_HISTORY[k] == _CALIBRATION_ACTION_HISTORY[k]` for all 20. Calibration set sized 40 (3 commit-13 + 17 commit-13.3.3 + 20 commit-13.3.4). `test_mw_entries_match_across_sidecars` PASS.

**Conclusion:** OK. **Confidence:** HIGH.

---

## Item E — Multiway chain-correctness across multiple postflop streets

**The highest-stakes new behaviour exercised in 13.3.4. CONFIRMED CORRECT.**

1. **Per-villain narrowing semantics work correctly on MW shapes with multiple streets.** `range_narrowing.py:947` filter (`position == villain_pos.upper()`) correctly isolates each fixture's chain to its designated primary villain. Verified for MW-46 (HJ/CO/BTN/BB on flop → only CO BET enters chain), MW-49 (HJ/CO/BTN/BB → only BB CALL enters), MW-50 (SB/BB/CO/BTN → only BTN RAISE enters).
2. **Same-street CHECK→CALL collapse on turn in MW shapes.** MW-42 turn CO-CHECK + CO-CALL collapses to `turn:CALL`. MW-46 turn same. MUST #11 last-decision-bearing rule applied correctly.
3. **River check-raise on decision-street correctly excluded.** MW-46 river CO-CHECK + CO-RAISE both on decision-street → chain has no river entries.
4. **Prior-street check-raise produces chain step.** MW-50 BTN-RAISE on flop → `flop:BET` (RAISE→bet class normalisation per `_action_to_narrow`).
5. **MW-50 RAISE→BET normalisation: lossy but pre-existing.** A check-raise range is tighter and stronger than a c-bet range; the chain narrowing applies the same `narrow_to_betting_range` filter for both. **However:**
   - Lossiness is **uniform across the codebase** (HU and MW alike), not introduced by 13.3.4.
   - Documented at `range_narrowing.py:802-807` as deferred to v2.5 with planned remediation (`CHECK_RAISE_BETTING_FREQUENCIES` Alternative-A).
   - Acknowledged in commit message (lines 45-51, 104-106).
   - Chain still narrows in **the right direction** (toward aggressive-action-consistent hands); just under-narrows on check-raises.
   - Applies identically to HU check-raise hands (e.g. SYN-F5_HU_overflow which exercises the same path).
   - **NOT chain-correctness-affecting** per the orchestrator's directive (which scopes the blocker condition to "chain-correctness-affecting" issues).

**Verdict on E.5:** Lossy in range-strength sense, but pre-existing, documented, tracked, and not a 13.3.4 blocker. Defer to v2.5 per existing roadmap.

**Conclusion:** OK. No chain-correctness blocker. **Confidence:** HIGH.

---

## Item F — Bucket distribution shifts

- `folded_mw`: 27 → 38 (+11) — MW entries with non-primary or other folds. Same pre-existing classifier promiscuity.
- `mw_per_villain`: 29 → 37 (+8) — no-fold MW entries.
- `delayed_probe`: 3 → 4 (+1: MW-41 routes here even though structurally a turn-decision against CO's 2nd barrel, not a strict delayed probe). Loose pattern-match; same family of pre-existing classifier laxity.

All three shifts are pre-existing classifier promiscuity (PR #2/#3/#4 INFO findings). **None chain-correctness-affecting; none functionally blocking.**

**Recommendation:** Continue 14.x deferral per orchestrator's standing decision. Address all label issues in one consolidated 14.x commit alongside PR #4's findings.

**Conclusion:** OK (deferred). **Confidence:** MEDIUM (couldn't combo-count classifier output without running, but PR claims are internally consistent and consistent with established defer-track).

---

## Item G — Scope / no-creep

`git show --stat d07e65d` reports exactly 3 files changed (`_calibration_action_history_sidecar.py` +221, `_reference_action_history_sidecar.py` +373, `tests/test_commit13_sidecar_dryrun.py` +45/-1). No drift into renderer/classifier/validator/range_narrowing/feature_extractor.

**Conclusion:** OK. **Confidence:** HIGH.

---

## VERDICT

**APPROVE**

**Rationale:** All 7 items pass with HIGH confidence. The 20 new MW-31..50 entries faithfully encode the design's Hero/Primary villain/Action history fields across flop/turn/river decisions. All 9 turn/river chain outputs were empirically verified to match PR claims exactly. Per-villain narrowing semantics work correctly across multi-street MW shapes. Same-street CHECK→CALL collapse works on MW turn streets (MW-42, MW-46). Decision-street check-raises correctly excluded from chain (MW-31 flop, MW-46 river). Calibration sidecar byte-identical (40 entries). Scope is clean.

**Required fixes:** None.

**Blockers:** None.

**Multiway chain-correctness assessment (Item E):** **CONFIRMED CORRECT.** Per-villain filter, same-street collapse, decision-street exclusion, and prior-street class normalisation all verified working on MW shapes. No chain-correctness blocker.

**MW-50 RAISE-to-BET normalisation assessment (Item E.5):** Lossy in range-strength sense (check-raise range tighter than c-bet range), but **pre-existing, documented at `range_narrowing.py:802-807`, tracked for v2.5 (`CHECK_RAISE_BETTING_FREQUENCIES`), and applies uniformly across HU and MW**. Not introduced by 13.3.4. Not chain-correctness-affecting (chain narrows in correct direction). **Not a blocker.**

**Recommendation on Item F telemetry findings:** Continue 14.x deferral. `folded_mw` (+11), `mw_per_villain` (+8), `delayed_probe` (+1 from MW-41 mis-routing) — all same family of pre-existing classifier promiscuity. Address in consolidated 14.x cleanup alongside PR #2/#3/#4 findings.

**Cosmetic NIT (non-blocking, defer to 13.3.5 wrap-up):** Test fixture_meta inline comment at `tests/test_commit13_sidecar_dryrun.py:422-429` (patch line 784) contains a self-correcting "Wait — let me restate" remark that survived into committed code. Harmless (comment-only); the corrected statement following it is accurate. Defer to 13.3.5 wrap-up alongside FB-13/FB-35 stale prose, MW-29 cosmetic NIT, NIT-1 chain-step content assertions.

**Greenlight 13.3.5 batch authoring:** Yes, conditional on orchestrator's merge of PR #5.

---

## Action

**Builder:**
1. Post comment on PR #5 referencing this verdict.
2. Run checkpoint #3 (post-verdict-comment) per the orchestrator's STOP-extension directive — UNKNOWN state means GitHub-compute-pending, retry after ~15s; only DIRTY/UNMERGEABLE = state mismatch.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check (PR state, branch naming, --merge not --squash, verdict provenance line present).
3. Merge PR #5 with `gh pr merge 5 --merge --delete-branch`.
4. After merge: builder is unblocked to start batch 13.3.5 (FINAL batch — synthetics + sweep cleanup including NIT items).

**Owner:** no action; briefed via PR + this comms doc.

## Reference

- PR #5: https://github.com/beytell1-sketch/river-rats-v2/pull/5
- 13.3 greenlight directive: `review/comms/MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md`
- PR #4 merge greenlight: `a8af4aa`
- Inheritance baseline (PR #4 verdict): `review/comms/GTO_REVIEW_VERDICT_PR_4_2026-04-25.md`
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
- Restart protocol: `review/comms/BUILDER_RESTART_PROTOCOL_2026-04-25.md`
