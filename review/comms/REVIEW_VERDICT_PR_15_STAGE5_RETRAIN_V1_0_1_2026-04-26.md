---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ML-architect reviewer (dedicated subagent unavailable; persona spec embedded per builder dispatch; reviewer is NOT the v1.0.1 author and NOT the v1.0 reviewer at `463e718`)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #15 — Stage 5 retrain protocol v1.0.1 (`9e6213f`) fix-forward of v1.0
status: APPROVE — All 3 MEDIUM findings (2 MEDIUMs + 1 MEDIUM-NIT) from PR #14 verdict cleanly addressed; bundled NIT applied; no new MEDIUMs introduced; ML core preserved verbatim. Ready for orchestrator merge as canonical v1.0.1.
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/15
branch: stage4-prep/stage5-retrain-fill-3-1
artifact: review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md (914 lines)
predecessor_pr: PR #14 verdict at `463e718` (REQUEST-CHANGES)
predecessor_directive: `9f8457e`
---

# Review Verdict — PR #15 (Stage 5 retrain protocol v1.0.1 fix-forward)

## Provenance note

Independent reviewer dispatch under read-only constraint. Did NOT author v1.0 or v1.0.1; did NOT review v1.0 (different general-purpose subagent at `463e718`). Worked from PR #15 head commit `9e6213f`. Cross-referenced against `gto_model.py:33-62`, `calibration_anchors.json`, `run_v231_anchor_recheck_stage35.py`, `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md`, `BUILDER_V24_P0_LANDED_2026-04-19.md`.

## Builder verification spot-checks

- `git log -p -S "d0182" -- river-rats-core/anchors/calibration_anchors.json` → EMPTY (confirms author claim that d0182 was NEVER in fixture) ✓
- Only commit ever to `calibration_anchors.json` = `570ece2` ✓
- `calibration_anchors.json` contains exactly 5 anchors: `d2410_CO_turn`, `LITMUS_A4d_Qs5s7s_flop`, `LITMUS_T5h_JJ2_flop`, `LITMUS_AA_7h5d2c_flop`, `LITMUS_KQ_KsTs3h_flop` ✓
- d0182/d8411 confirmed only as hard-coded specs in `review/run_v231_anchor_recheck_stage35.py` (lines 74, 97) ✓
- `gto_model.py:33-62` `FEATURE_COLUMNS`, `N_FEATURES = 55` ✓
- d8411 baseline `0.661` (post-Finding B) verified in `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md:88` ✓
- Variance math: `python3 -c "1/sqrt(3)"` → 0.5774 SD ratio = 42.3% SD reduction = 66.7% variance reduction ✓

---

## Item A — MEDIUM #1 — Prereq #2 column count rewrite

**OK / HIGH confidence.** Old "110-column (54+4=58 raw + 58 attn_*)" replaced with "**118-column v2.4 contract (55 raw + 4 v2.4 blocker = 59 raw + 59 attn_*)**" plus parenthetical anchoring v2.3.2 baseline = 55+55=110 against `gto_model.py:33-62` `N_FEATURES=55` and v2.3.2 training report `n_features: 110`. Arithmetic 55+4=59, 59+59=118 ✓. Internally consistent with §Hyperparameters point #4. Added parenthetical also cites `feedback_attention_flags_when_features_change.md` to justify attn_* layer extension 55→59.

## Item B — MEDIUM #2 — Mode D anchor inventory resolution (option (a))

**OK / HIGH confidence.** Author selected option (a) on empirically-verified grounds: `git log -p -S "d0182"` returns EMPTY; `570ece2` is only commit ever to fixture. d0182/d8411 are not "renamed" anchors — they were always β-panel diagnostics in `run_v231_anchor_recheck_stage35.py`, never production fixture entries. v1.0's reference was a documentation error inherited from Stage 3.5 closure docs.

Option (a) correct over (b): re-instantiating d0182/d8411 in `calibration_anchors.json` would import non-fixture diagnostics into production gate without solver verification.

Mode D consistently updated:
- 5-anchor table with Tolerance / Expected / Class-protected columns
- Diagnosis steps reference 5 anchors + d8411 separately
- Rollback decision criteria split into d2410/LITMUS_*/d8411 with d8411 explicitly "Diagnostic, not Gate-3-blocking"

Mode C diagnostic step #3, Gate 3 anchor table, and §Reporting all consistently updated to same 5-anchor + optional-d8411 pattern.

## Item C — MEDIUM-NIT — Variance-reduction math correction

**OK / HIGH confidence.** Old "30% lower predictive variance (1/√3)" replaced with "~42% lower predictive SD (1/√3 ≈ 0.577 ratio for averaging N=3 independent models; equivalently ~67% lower variance, 1/N for N=3)". Independently verified: 1/√3 = 0.5774; 42.3% SD reduction; 66.7% variance reduction. Both framings present (SD ratio + variance ratio). Companion paragraph also rewritten; no stale "30% lower" in body.

## Item D — Bundled NIT — Prereq #3 orchestrator-action assignment

**OK / HIGH confidence.** New text: "**This step requires orchestrator action pre-Stage-5 (tag baseline model commit on origin); not automatic.** Builder verifies the tag exists before calling the retrain script and HALTs (per CLAUDE.md §5) if absent." Adds HALT condition tied to CLAUDE.md §5 stop conditions — appropriate.

## Item E — No new MEDIUMs introduced

**OK / HIGH confidence.** Mode D ↔ Mode C internally consistent. Mode D 5-anchor table consistent with `calibration_anchors.json` content (tolerance="strict" for all 5; expected actions match d2410=BET, A4d=CHECK, T5h=CHECK, AA=BET, KQ=BET).

**One LOW observation (NOT new MEDIUM, NOT in v1.0.1 scope):** Line 187 §"Inputs from Stage 4" still reads "54 + 4 = 58 binary attn_* flags" — should be 55+4=59 to align with v2.4 attention layer extension. Pre-existing v1.0 statement about Stage 4 input contract (separate axis from training-tensor column count); not flagged in PR #14 verdict; not blocking. Note for v1.1 cleanup.

## Item F — Frontmatter changelog

**OK / HIGH confidence.** All elements verified:
- `version: v1.0.1` ✓
- `status: v1.0.1 (REQUEST-CHANGES fix-forward on v1.0)` ✓
- `review_chain` adds v1.0 reviewer pass at `463e718` and v1.0.1 fix-forward step ✓
- `changelog.v1.0.1` lists 3 fixes + bundled NIT + 6 deferrals + explicit `not_changed` block confirming ML core preservation ✓
- References verdict `463e718` and directive `9f8457e` by SHA ✓

The `not_changed` block is good discipline — explicitly states which v1.0 decisions survived (hyperparameter spec, SHA256 seed scheme, ±2pp + Spearman ≥ 0.8 thresholds, median-seed, 5 rollback modes, all UNCERTAIN tags).

## Item G — Diff scope

**OK / HIGH confidence.** Diff: 197 ins / 50 del (net +147 lines, total 247 diff lines). Component breakdown justifiable per fix:
- ~70 lines: changelog v1.0.1 frontmatter (mandatory traceability)
- ~50 lines: Mode D rewrite (5-anchor table + diagnosis/decision restructure required to make Mode D mechanically executable per MEDIUM #2)
- ~30 lines: Mode C / Gate 3 / §Reporting cross-reference rewrites (consistency requirement)
- ~20 lines: Prereq #2 + Prereq #3 NIT
- ~10 lines: variance-reduction math
- ~17 lines: author-note v1.0.1 paragraph

No scope creep into LOW/NIT territory beyond the explicitly bundled Prereq #3 NIT. The 6 deferrals enumerated show the author held the line.

## Item H — Self-consistency pass

**OK / HIGH confidence.** Re-ran author's grep checks:
- `grep "110-column|108-column|116-column|54 raw|58 raw|58 attn"` → only intentional context (changelog history + §Hyperparameters historical 54+54=108 v2.2 / 55+55=110 v2.3.2)
- `grep "d0182|d8411|LITMUS_"` → all current-tense uses actual fixture IDs; d0182 only in changelog; d8411 only in changelog OR explicit "Stage 3.5 audit-script diagnostic"
- `grep "30% lower|1/√3|1/sqrt(3)"` → "30% lower" only in changelog; "1/√3" with correct 42% SD / 67% variance framing

## Item I — Mode D anchor table content

**OK / HIGH confidence.** All 5 anchors correctly specified vs `calibration_anchors.json`:
- d2410_CO_turn: strict / BET / TPGK turn after flop check ✓
- LITMUS_A4d_Qs5s7s_flop: strict / CHECK / Air on monotone ✓
- LITMUS_T5h_JJ2_flop: strict / CHECK / Air on paired board ✓
- LITMUS_AA_7h5d2c_flop: strict / BET / Overpair dry ✓
- LITMUS_KQ_KsTs3h_flop: strict / BET / TPGK two-tone ✓

All tolerances correctly read as `strict`. Class-protected descriptions reasonable paraphrases of fixture's `rationale` field.

## Item J — d8411 as "optional audit diagnostic" semantic check

**OK / HIGH confidence.** Semantic split correct:
- d8411 IS in `run_v231_anchor_recheck_stage35.py:97` (β-panel anchor)
- Stage 3.5 closure confirms d8411 STRENGTHENED 0.589 → 0.661 from Finding B
- d8411 is NOT in `calibration_anchors.json` (verified empirically)

Audit-script-optional Stage 3.5 diagnostic with named 0.661 baseline is right semantic split. Promoting d8411 to fixture would either bypass solver-verification discipline (bad) or require running solver now (out of scope). Current path is correct middle.

## Item K — Ready for orchestrator merge?

**APPROVE.** All PR #14 MEDIUMs cleanly addressed with verified arithmetic and verified anchor inventory. Bundled Prereq #3 NIT applied. No new MEDIUMs. 6 deferrals are sensible scope-control. Frontmatter changelog discipline strong (explicit `not_changed` block + SHA references). ML core preserved verbatim.

Ready for orchestrator merge as canonical v1.0.1.

---

## VERDICT

**APPROVE — overall confidence HIGH.**

All 3 fix-forward items (2 MEDIUMs + 1 MEDIUM-NIT) cleanly addressed with empirical verification (anchor history via `git log -S`, column counts vs `gto_model.py`, variance math independently re-derived). Bundled NIT (Prereq #3) applied. 6 LOW/NIT items appropriately deferred to v1.1 / Task 5 wrap-up with explicit changelog enumeration.

No new MEDIUM-severity issues introduced. Mode D + Mode C + Gate 3 + §Reporting all internally consistent. Diff scope (247 lines) accountable per fix.

**Required fixes:** None. **Blockers:** None.

**Recommendation:** Merge PR #15 as canonical v1.0.1, then close PR #14 (predecessor superseded). Mirrors PR #11/#13 auto-resolution pattern.

## NIT-level observations (non-blocking)

1. (LOW, NEW for v1.1) Line 187 §"Inputs from Stage 4" reads "54 + 4 = 58 binary attn_* flags" — should be 55+4=59 to align with v2.4 attention layer extension per `feedback_attention_flags_when_features_change.md`. Pre-existing v1.0 statement; separate axis from training-tensor column count; not in PR #14 verdict scope; not blocking.
2. (Inherited from PR #14 verdict, deferred per directive) 6 LOWs/NITs in changelog `deferred_to_v1_1_or_task_5_wrapup` — all owner / orchestrator awareness, non-blocking.

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | LOW (v1.1) | §Inputs from Stage 4 line 187 attn_* count: 58 → 59 (alignment with v2.4 attention layer) |
| 2 | (deferred) | 6 deferrals from changelog enumerated for v1.1 / Task 5 wrap-up |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_15_STAGE5_RETRAIN_V1_0_1_2026-04-26.md`.
2. Post comment on PR #15 referencing the verdict.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Merge PR #15 — APPROVE clean. Auto-resolves PR #14 (ancestor). Mirrors PR #11/#13 patterns.
3. Greenlight Task 4 (Stage 6 held-out test set) per Stage 4 prep plan.

**Owner:** wake to find Stage 5 retrain protocol v1.0.1 ready for retrain dispatch — all MEDIUMs resolved, ML core preserved, fix-forward addressed real bugs (Mode D anchor mismatch was a documentation error v1.0 inherited from Stage 3.5 closure docs).

## Reference

- PR #15: https://github.com/beytell1-sketch/river-rats-v2/pull/15
- v1.0.1 commit: `9e6213f`
- v1.0 commit: `a7a62fa`
- v1.0 verdict: `463e718` (REQUEST-CHANGES)
- Orchestrator directive: `9f8457e`
- Source artifact: `review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md`
- Fixture: `river-rats-core/anchors/calibration_anchors.json`
- Trainer: `river-rats-core/train_v2_3_2.py`
- v2.4 features: `river-rats-core/gto_model.py:33-62`
- Stage 3.5 closure: `review/comms/BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md`
- Tasks 1.1 + 2.1 verdict precedents: PR #11 + PR #13 verdicts

**FINAL VERDICT: APPROVE — HIGH confidence overall. Ready for orchestrator merge as canonical Stage 5 retrain v1.0.1; Task 4 (Stage 6 held-out) next.**
