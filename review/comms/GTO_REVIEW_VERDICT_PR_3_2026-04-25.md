---
date: 2026-04-25
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #3 — Stage 3.5 commit 13.3.2 (`a0cdac9`)
status: APPROVE — all 7 review items OK with HIGH confidence; FB-25 GTO judgment call CONFIRMED; classifier-promiscuity findings deferred to 14.x; orchestrator can merge with --merge --delete-branch
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/3
---

# GTO Review Verdict — PR #3 (Commit 13.3.2)

## Provenance note

Same provenance pattern as the 13.2.5 / PR #1 / PR #2 verdicts: dispatched as general-purpose subagent with the `gto-expert` persona embedded verbatim, per owner's standing in-session authorisation while the dedicated subagent dispatch path is unavailable.

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item A on FB-25 chain steps: "for primary villain CO, both candidate encodings produce identical chain steps `flop:BET + turn:BET`." **Verified.** Ran `narrow_by_action_history` directly: `chain_steps=['flop:BET', 'turn:BET']` confirmed.
- Reviewer claim Item D: "FB-38 and FB-39 routing to `hu_donk_x_bet` is via the check-through variant branch (lines 138-140), NOT the donk branch." **Verified.** Ran `_classify_shape` directly on both: bucket=`hu_donk_x_bet` for both. Source inspection of `solver_verify_sidecars.py:138-140` confirms it's the check-through variant.
- Reviewer claim Item B: "All 19 villain_pos entries match `villain_positions[0]` from JSONL." **Verified.** Reviewer enumerated all 19 in a table; cross-checked spot samples.

All three spot-checks hold against source and runtime behavior.

---

## Item A — Per-fixture action-history correctness

Sampled 5 representative shapes including the FB-25 GTO judgment call:

**Sample 1 — FB-21 (turn, flop check-through, regression vs FB-17/18):** AH matches `action_string="BB check, CO bet 45, BTN fold, BB ???"`; flop check-through correctly reconstructed. Same shape as FB-17/FB-18; regression check passes. **OK.**

**Sample 2 — FB-22 (3-way BTN-PFR, flop, hero=CO, check-check-bet-call):** AH matches `action_string="BB check, CO check, BTN bet 30, BB call 30, CO ???"`. Postflop order BB→CO→BTN respected. Hero terminates flop block before acting. **OK.**

**Sample 3 — FB-25 ⚠️ GTO JUDGMENT CALL — CONFIRMED:** Builder encoded BTN folding to flop c-bet (most natural reading of "BTN folded earlier"). Reviewer assessed both candidate encodings and confirmed:
1. "BTN folded earlier" most naturally points to the FIRST opportunity to fold — the c-bet.
2. JSONL `positions=[BB, CO]` lists only 2 active positions on river street, consistent with BTN gone before turn play.
3. **For primary villain CO, both candidate encodings produce identical chain steps `flop:BET + turn:BET`** — the chain narrows on CO's actions only (per `range_narrowing.py:947` filter). The choice is non-load-bearing for what this PR's plumbing exercises.
4. Alternative ("BTN cold-calls c-bet OOP-to-PFR then folds to turn 2nd barrel") is a much rarer line.

Builder's interpretation **CONFIRMED. Ship as encoded. OK.**

**Sample 4 — FB-35 ⚠️ STALE PROSE CASE:** Prose at `_FB_ACTION_HISTORY:782` says "BB folded" on flop, but JSONL action_string ("BB check, CO check, BTN bet 90, BB fold, CO ???") shows BB folding on TURN. Builder followed action_string per established convention (continues FB-13 pattern). For BB to be checking turn, BB must have CALLED flop — only consistent reconstruction. Prose genuinely stale; tracked for batch 13.3 prose-cleanup commit. **OK — encoding correct.**

**Sample 5 — FB-39 (3-way BTN-PFR, river, all checked flop+turn, BTN bets river, hero=BB sandwich):** AH matches action_string. Prior streets correctly reconstruct double-check-through (only consistent way to reach 3-way river). Primary villain BTN chain step: flop:CHECK + turn:CHECK. **OK.**

**Item A overall: OK. Confidence: HIGH.**

---

## Item B — Position-aware classifier compatibility

Reviewer enumerated all 19 new entries against `villain_positions[0]` from JSONL — 19/19 match. `_REFERENCE_VILLAIN_POS` extension is byte-for-byte correct.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item C — `expects_chain_fire` correctness

Walked all 19 entries against `narrow_by_action_history` semantics:
- Flop decisions (10): `expects_chain_fire=False` ✓
- Turn decisions (4): FB-21 (`flop:CHECK`), FB-35 (`flop:BET`), FB-36 (`flop:BET`), FB-37 (`flop:CHECK`) — all True ✓
- River decisions (5): FB-24/26/38/39 (`flop:CHECK + turn:CHECK`), FB-25 (`flop:BET + turn:BET`) — all True ✓

**Conclusion:** OK
**Confidence:** HIGH

---

## Item D — Bucket distribution shifts

**Finding 1 — `folded_mw` 12 → 21 (+9):** Reviewer enumerated all 9 new non-primary-fold entries (FB-21/24/25/26/27/31/35/36/37); all 9 verified to be non-primary folds. Same pre-existing promiscuity from PR #2 Item D.

**Finding 2 — `hu_donk_x_bet` 1 → 3 (+2 from FB-38/FB-39):** Reviewer confirmed via direct simulation (`_classify_shape`) and source inspection that both route via the **pre-existing "check-through variant" branch** at `solver_verify_sidecars.py:138-140`, NOT the actual flop-donk branch. Pre-existing label-stretch flagged as INFO in PR #1's verdict; first time real entries exercise this path.

**Recommendation: defer both to 14.x cleanup.** Continues orchestrator's stated deferral from `cc52d76`. Folding into 13.3.x would expand scope into the bucket classifier and violate per-PR discipline.

**Conclusion:** OK (telemetry shifts explained; pre-existing).
**Confidence:** HIGH

---

## Item E — Convention-respect

3-way preflop encoding (CO-open vs BTN-PFR), postflop position order (BB→CO→BTN), hero-per-`???` marker — all 19 entries follow consistently. `_FB_OPENER_POSITION` cross-check 19/19. Same conventions as PR #2.

**Conclusion:** OK
**Confidence:** HIGH

---

## Item F — Test coverage

`_EXPECTED_COMMIT13_3_2_REFIDS` defined; `_EXPECTED_REFERENCE_REFIDS` extended via union. `test_dryrun_entries_exercise_chain_narrowing` now iterates 49 entries (30 + 19). Boards in fixture_meta are `List[str]` format matching JSONL.

**PR #2 NIT-1 (chain-step content assertions) — recommendation:** continue deferring through 13.3.3/4. Fold into 13.3.5 wrap-up commit alongside the stale-prose cleanup. Doing it mid-batch risks scope creep.

**Conclusion:** OK (test coverage adequate; advisory deferred).
**Confidence:** HIGH

---

## Item G — Scope / no-creep

`git show --stat a0cdac9` reports exactly 2 files changed (sidecar + dryrun test). No creep into renderer/classifier/validator/range_narrowing/feature_extractor.

**Conclusion:** OK
**Confidence:** HIGH

---

## VERDICT

**APPROVE**

**Rationale:** All 19 new FB-21..40 reference entries (minus FB-23) encode correctly per JSONL action_string canonical ground truth. The FB-25 GTO judgment call is **CONFIRMED** — most natural narrative reading, consistent with JSONL `positions=[BB, CO]` river-street roster, and chain-fire-invariant to the tie-breaker. The FB-35 stale-prose case correctly follows action_string per established convention. Item D's `folded_mw` and `hu_donk_x_bet` shifts are pre-existing classifier label-stretch (PR #1/PR #2 INFO), correctly deferred. Test coverage and scope are clean.

**Required fixes:** None.

**Blockers:** None.

**Special verdict on FB-25 judgment call:** CONFIRM builder's interpretation. Encoding "BTN folds to flop c-bet" is correct. For primary villain CO, both candidate encodings produce identical chain steps `flop:BET + turn:BET` (verified via direct simulation), so the choice is non-load-bearing for chain-narrowing. The encoding is the most natural narrative reading of "BTN folded earlier" in a triple-barrel line. Ship as encoded.

**Recommendation on Item D telemetry findings:** Defer both `folded_mw` (+9) and `hu_donk_x_bet` (+2) to 14.x cleanup. Continues orchestrator's stated deferral from `cc52d76`. Address all three label issues (donk-stretch, folded_mw promiscuity, plus any new ones from 13.3.3/4/5) in one consolidated 14.x commit.

**Greenlight 13.3.3 batch authoring:** Yes, conditional on orchestrator's merge of PR #3.

---

## Action

**Builder:**
1. Post comment on PR #3 referencing this verdict.
2. Run checkpoint #3 (post-verdict-comment) per the orchestrator's STOP-extension directive.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check (PR state, branch naming, --merge not --squash, verdict provenance line present).
3. Merge PR #3 with `gh pr merge 3 --merge --delete-branch`.
4. After merge: builder is unblocked to start batch 13.3.3 on `stage3.5/commit-13-3-3`.

**Owner:** no action; briefed via PR + this comms doc.

## Reference

- PR #3: https://github.com/beytell1-sketch/river-rats-v2/pull/3
- 13.3 greenlight directive: `review/comms/MAIN_TERMINAL_COMMIT13_3_GREENLIGHT_2026-04-25.md` (`e87f371`)
- PR #2 merge greenlight: `cc52d76`
- Inheritance baseline (PR #2 verdict): `review/comms/GTO_REVIEW_VERDICT_PR_2_2026-04-25.md`
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
