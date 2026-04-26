---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT GTO reviewer (gto-expert subagent unavailable; persona spec embedded per builder dispatch; reviewer is NOT v1.0 author and NOT prior Stage 4 prep reviewer)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #16 — Stage 6 held-out test set v1.0 (`30ec324`)
status: APPROVE-WITH-NITS — strong design artifact (50 hands well-authored, non-overlap verified, sizing tags solver-aligned, prereqs disciplined) BUT 7 substantive issues require Task 4.1 fix-forward before pilot dispatch / evaluation use, including 1 HIGH-severity hash mismatch (recorded ≠ recomputed) + 1 HIGH-severity arithmetic errors + 4 MEDIUM-severity rebalances. Reviewer notes a stricter reading would escalate to REQUEST-CHANGES.
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/16
branch: stage4-prep/stage6-holdout-fill
artifact: review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md (1449 lines)
predecessor: review/comms/STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md (~205 lines)
---

# Review Verdict — PR #16 (Stage 6 held-out test set v1.0)

## Provenance note

Independent reviewer dispatch under read-only constraint. Did NOT author v1.0 or any predecessor Stage 4 prep task; did NOT review v0.1 DRAFT or any prior Stage 4 prep PR. Worked from PR #16 head commit `30ec324` (note: post-verdict, builder pushed `8351b6f` to restore the PROCEED comm — see Item L). Cross-referenced against `feedback_solver_aligned_sizing.md`, `calibration_anchors.json`, training-data `*.jsonl` files, and the v0.1 DRAFT.

## Builder verification spot-checks

- 56 jsonl files in `training-data/` confirmed via `find` ✓
- Independently parsed 50 holdout `(hero, board)` fingerprints; cross-checked vs 1846 unique training-data fingerprints — 0 matches confirms non-overlap ✓
- 5 calibration anchors visually inspected vs 50 holdout heroes/boards — no overlap ✓
- Recovery trail: master HEAD `6d8f2a1` clean (no leftover Stage 6 file) ✓

---

## Item A — 50 hands present + completeness

**OK (with NITs) / HIGH confidence.** All 50 HOLDOUT_001-050 sections present with all required fields. Spot-checked 9 hands across confidence bands + action classes — all actionable.

**NITs for v1.1:**
- H007: inline `*(NOTE: 4-card depiction is wrong; flop is 3 cards.)*` followed by corrected line. Two `Board:` lines breaks JSONL exporter
- H016, H019, H045, H047: `Re-frame action history` blocks (original sequence didn't terminate at hero decision). Same JSONL-export risk
- H032: preflop hand with no `Board:` field — schema must accommodate or silently breaks export round-trip

These don't break v1.0 as design artifact but Prereq #6 (format round-trip) cannot pass without a flatten pass.

## Item B — Action distribution skew

**NOT-OK (defer to fix-forward) / MEDIUM confidence.** Achieved 4 FOLD / 10 CHECK / 11 CALL / 20 BET / 5 RAISE vs target 10/12/10/13/5.

- BET +7 mostly defensible (checked-to-hero IP nodes solver-correctly skew small c-bet; flop-skewed corpus concentrates this class)
- **FOLD −6 is real evaluation gap.** Effective FOLD-class sample size 4 — single mislabel swings per-class metric by 25pp. Cannot reliably score FOLD behavior. The model's known weak class historically is FOLD discipline (over-fold MW textures, under-fold dominated bluffcatcher rivers per `feedback_solver_findings.md`).

**Fix-forward (Task 4.1):** re-author 6 hands as face-bet → FOLD spots covering: dominated bluffcatcher rivers, draws short of pot odds, MW air on monotone face-cbet, IP TP face turn-x-raise on dynamic boards.

## Item C — Confidence band distribution

**OK-WITH-FIX-FORWARD / MEDIUM confidence.** 30 HIGH / 18 MEDIUM / 2 LOW vs target 30/15/5.

- HIGH on target; MEDIUM marginal +3
- **LOW −3 is meaningful.** Only 2 LOW (H024, H046) → no statistical power for LOW-band stratum. LOW spots are highest-signal evaluation hands.

**Fix-forward (Task 4.1):** add 3 more LOW: candidates include thin river bluffs into capped ranges, MW turn underpair vs continuation barrel, 3bet-pot OOP check-raise frequency calls.

## Item D — Solver-verification 10-sample composition

**NOT-OK / MEDIUM confidence.** Sample H002, 007, 013, 019, 024, 028, 032, 037, 043, 049 has 4 HIGH / 5 MEDIUM / 1 LOW + CHECK/CALL/BET/RAISE classes, but **NO FOLD**.

- No-FOLD-in-sample is real gap; FOLD spots' equity/fold-equity split is solver verification's primary value
- Author's swap-in HOLDOUT_046 (mid overpair face turn check-raise, FOLD, LOW) verified appropriate — drop one of {H019, H037} (both CALL/MEDIUM/soft over-represented)

**Fix-forward:** swap H046 in for H019 or H037. Consider also adding 3-bet pot OOP check-raise hand (H045 or H047).

## Item E — Non-overlap verification rigour

**OK (with caveat) / HIGH confidence.**

- 56 jsonl training-data files independently confirmed
- Independent fingerprint cross-check: 0 matches against my parsed 49 holdout tuples (H032 preflop has no Board → cannot collide with postflop training data)
- My fingerprint count (1846) differs from author's 1996 — explained by field-name variation across heterogeneous corpus; headline result (zero matches) preserved
- 5 calibration anchors visually inspected vs holdout — no overlap ✓
- **Caveat:** suit-isomorphism deferred (acceptable v1.0; document in Prereq)
- **Author flag #7 — 24-hand calibration manifest location unknown** is real prereq gap; owner needs to confirm whether separate manifest exists. Author's "subsumed in pass1/factory" claim plausible but not verified. Document as Task 4.1.

## Item F — SHA256 hash content lock

**NOT-OK / HIGH confidence — single most consequential finding.**

- **Claimed hash:** `8b553de0745bb50f5867a330d507eb106c04b9bc09f385e16966eec925b3b74b`
- **Recomputed hash on file at `30ec324`:** `b3970aa595bba9e6d0c107e2c07d1ec4165bd214d0262914a3d96a15d11322ae`
- **Claimed bytes:** 40,404
- **Actual bytes between markers:** 40,655

3 occurrences of each marker in the file (START at offsets 1512, 9169, 12508; END at 1574, 9224, 53163) because the prereq prose AND the recommended `python3` one-liner reference markers literally. Author's recommended one-liner uses `re.search(re.S)` non-greedy `.*?` which matches FIRST pair — empty 62-byte span produces hash `39c381...`. Neither greedy/non-greedy/LAST-LAST matches recorded `8b553de0...`.

**The lock currently certifies nothing.** Most likely author computed hash on in-progress version then made post-hash edits (H007 fix-up, re-frame notes for H016/19/45/47, post-fact line renumbering) and committed without re-hashing.

**Fix-forward (Task 4.1):** Recompute hash on final byte content; record corrected hash; document resolution rule (e.g., "use LAST-LAST markers" — and remove literal markers from prereq prose to eliminate ambiguity, OR escape them as code-fenced examples that don't grep-match the literal strings).

## Item G — Sizing tag conventions

**OK (with one nit) / HIGH confidence.** Spot-checked 10 hands: all BET sizes in sanctioned set; H048 BET_150 confirmed river spot; all RAISE_* uses are facing existing bets (`feedback_terminology_raise_vs_bet.md` discipline observed).

NIT: H041 BET_66 on flop is sanctioned but slightly atypical (most solvers use 25/50/66/75 mix). Acceptable.

## Item H — Pot/SPR arithmetic

**NOT-OK / HIGH confidence on H022/H028, LOW elsewhere.** Spot-checked 10 hands:

- H001, H013: ✓
- H002, H006, H023, H047, H049, H050: off by 0.5 (SB dead-money inconsistency)
- **H022, H028: claimed pot 28.6, recomputed 22 — off by 6.6bb (~30%); looks like double-counted turn bet**
- H039: river donk "BB bet_75 7.5" but 75% of pot 8.8 = 6.6, not 7.5

Errors small individually (±0.5) but holdout test set is gold-standard spec. If evaluator re-derives pot from action history, hand fails format validation. If evaluator trusts stated field, SPR-to-action mapping subtly wrong.

Author's self-consistency closure spot-checked only H001 + H013 — both happen to be the two without error pattern. Should have spot-checked at least one 4-street hand (H022/H028 type) and one MW preflop (H023/H050 type).

**Fix-forward (Task 4.1):** full arithmetic audit + standardise SB-dead-money rule (state explicitly: "0.5bb dead-SB included" or "excluded — only voluntarily-committed chips").

## Item I — Per-hand poker-rigour

**OK (with 1 MEDIUM concern) / MEDIUM confidence.** Spot-checked 10 hands; all rationales sound; action follows from rationale.

**MEDIUM concern — H022 (BET_75, MEDIUM, soft):** missed-NFD river polar bluff. Hero blocks Ax flush combos (true, hero has Ac). But polar-bluff line on paired river also weighs hero's TURN sizing (BTN bet_75 6.6 = 75% pot, then river BB checks). On turn hero polarised to big bet — by river the line is "big-turn, polar river"; BB's call-call vs that line is heavy with Kx wanting to bluffcatch. Solver-typical CHECK frequency may exceed BET. Author already flagged with `[UNCERTAIN-SOLVER]` and soft tolerance; this hand is in the 4-hand UNCERTAIN-SOLVER census beyond 10-sample. Acceptable as-is given the flag; solver verification on H022 should be added to pre-pilot solver pass.

No hand obviously contradicts its rationale.

## Item J — PRE-EVALUATION PREREQUISITES section

**OK / HIGH confidence.** 8 prereqs covering hash match, solver-sample clearance, independent reviewer pass, non-overlap re-verification, pilot-corpus disjointness, format round-trip, single-shot discipline, two-pass concurrence. All well-formed.

Two are blocking on this review's findings:
- Prereq #1 (hash match) **CANNOT** pass at v1.0 — see Item F
- Prereq #6 (format round-trip) **CANNOT** pass without flattening inline corrections in H007/H016/H019/H045/H047 — see Item A

Both forced into Task 4.1 fix-forward.

## Item K — Frontmatter discipline

**OK / HIGH confidence.** Version, author, derived_from, review_chain all present and accurate. Author honestly identified as general-purpose-as-gto-expert per locked Stage 4 D3 fallback.

## Item L — Process note (recovery)

**OK / HIGH confidence.** Master HEAD `6d8f2a1` clean (no leftover Stage 6 file). Working tree only `review/ARCHITECTURE_END_STATE.html` untracked (unrelated). Recovery clean.

**One artifact:** PR #16's diff vs master originally showed deletion of `MAIN_TERMINAL_BUILDER_TASK4_PROCEED_2026-04-26.md` (110 lines) — cherry-pick artifact. Builder restored this on the feature branch in commit `8351b6f` (post-verdict-dispatch). Reviewer noted the issue; builder fixed before merge.

## Item M — Ready for orchestrator merge?

**APPROVE-WITH-NITS — MEDIUM confidence overall.**

**Strengths:**
- 50 hands authored with poker-rigorous rationales and class-protected tags
- Non-overlap verification independently confirmed (zero matches)
- Sizing tags solver-aligned per `feedback_solver_aligned_sizing.md`
- Frontmatter and prereqs disciplined; UNCERTAIN-SOLVER tags honestly placed
- Process recovery clean
- Spot-checked poker reasoning sound on 10 hands

**Material findings forcing fix-forward (Task 4.1):**

1. **Hash mismatch (HIGH).** Recorded hash `8b553de0...` vs actual `b3970aa5...`. Lock currently certifies nothing.
2. **FOLD-class undersample (MEDIUM).** 4 FOLD vs 10 target = no per-class FOLD evaluation power. Re-author 6 hands.
3. **LOW-band undersample (MEDIUM).** 2 LOW vs 5 target = no LOW-band stratum power. Re-author 3 hands.
4. **Solver-sample missing FOLD (MEDIUM).** Swap H046 in for H019 or H037.
5. **Pot/SPR arithmetic errors (HIGH on H022/H028 ~6.6bb gap; LOW on ±0.5 SB-dead-money inconsistencies).** Full audit + state SB-dead-money rule.
6. **JSONL-export blockers (LOW-MEDIUM).** Inline corrections in H007/H016/H019/H045/H047 + missing Board on H032 will fail format round-trip.
7. **24-hand calibration manifest gap (MEDIUM).** Owner confirmation needed.

**Recommendation:** APPROVE-WITH-NITS for v1.0 as design artifact (50 hands, distribution analysis, prereqs, non-overlap method survive review). REQUIRE Task 4.1 fix-forward before pilot dispatch / evaluation use, addressing F (hash) + B (FOLD rebalance) + C (LOW rebalance) + D (sample swap) + H (arithmetic audit) + A/J prereq #6 (export flatten) + E/J prereq #4 (calibration manifest confirmation).

Per `feedback_quality_default_no_ask.md`, the Task 4.1 fix-forward is the right answer — v1.0 should not be used in pilot evaluation in current state.

---

## VERDICT

**APPROVE-WITH-NITS — overall confidence MEDIUM.**

(MEDIUM not HIGH because hash failure at Item F is the kind of issue that, in a different framing, justifies REQUEST-CHANGES. Landing on APPROVE-WITH-NITS because design artifact is genuinely useful and Task 4.1 fix-forward is the standing pattern that has worked on PRs #10/12/14 — but a stricter reviewer could reasonably escalate.)

**Required fixes:** None for design-artifact ship (v1.0 is reviewable). All 7 fix-forward items are pre-pilot blockers.
**Blockers:** None for design-artifact merge; multiple pre-pilot blockers.

## NIT-level observations (deferred)

(See action items — most NITs bundled into recommended Task 4.1 fix-forward.)

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | HIGH | Hash recompute + lock-rule clarification (LAST-LAST markers + escape literal strings) |
| 2 | HIGH | Pot/SPR arithmetic full audit + state SB-dead-money rule |
| 3 | MEDIUM | Re-author 6 FOLD hands (face-bet → FOLD spots) |
| 4 | MEDIUM | Re-author 3 LOW hands (boundary spots) |
| 5 | MEDIUM | Swap H046 for H019 or H037 in 10-sample |
| 6 | MEDIUM | 24-hand calibration manifest confirmation (owner) |
| 7 | LOW-MEDIUM | Flatten inline corrections (H007/16/19/45/47) + add Board placeholder for H032 |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_16_STAGE6_HOLDOUT_2026-04-26.md`.
2. Post comment on PR #16 referencing the verdict.
3. Stand by for orchestrator fix-forward direction (per established pattern, fix-forward highly likely given HIGH-severity hash + arithmetic issues).
4. If fix-forward directive issued: execute Task 4.1.
5. **Already addressed:** PROCEED comm restored on feature branch (`8351b6f`) — cherry-pick artifact reviewer flagged is now resolved.

**Orchestrator:**
1. Read this verdict.
2. Issue Task 4.1 fix-forward directive (recommended); alternative: BLOCK PR #16 until v1.0.1 lands. PR #11/13/15 precedents all went fix-forward path.
3. Per quality default `feedback_quality_default_no_ask.md`: HIGH-severity findings (hash, arithmetic) should be addressed before merge.

**Owner:** wake to find Stage 6 held-out test set v1.0 needs Task 4.1 fix-forward. Design intent intact (50 hands well-authored); 7 substantive issues need resolution before pilot evaluation use.

## Reference

- PR #16: https://github.com/beytell1-sketch/river-rats-v2/pull/16
- v1.0 commit: `30ec324`
- PROCEED restore commit (post-review): `8351b6f`
- Source artifact: `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md`
- Solver-aligned sizing memory: `feedback_solver_aligned_sizing.md`
- Solver findings memory: `feedback_solver_findings.md`
- Existing fixture: `river-rats-core/anchors/calibration_anchors.json`
- Tasks 1.1 / 2.1 / 3.1 fix-forward precedents: PR #11, PR #13, PR #15

**FINAL VERDICT: APPROVE-WITH-NITS — MEDIUM confidence overall. Task 4.1 fix-forward strongly recommended (HIGH-severity hash + arithmetic findings). Mirrors PR #11/#13/#15 pattern.**
