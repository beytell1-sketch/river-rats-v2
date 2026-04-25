---
date: 2026-04-26
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner · Teaching builder · Game builder
re: Per-batch GTO review on PR #7 — Stage 3.5 commit 14 (`134be52`); Finding B fold-in — multiway per-villain field promotion
status: APPROVE — all 7 review items OK with HIGH confidence; no required fixes; cross-stream contract READY for teaching HOLD #5 + game per-villain range bars; orchestrator can merge with --merge --delete-branch
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/7
---

# GTO Review Verdict — PR #7 (Commit 14, Finding B Fold-In)

## Provenance note

Same provenance pattern as the 13.2.5 / PR #1-6 verdicts: dispatched as general-purpose subagent with the `gto-expert` persona embedded verbatim, per owner's standing in-session authorisation while the dedicated subagent dispatch path is unavailable.

**Process tightenings applied:** read-only brief (Read/Grep/Glob/Bash only; no Write/Edit; verdict via message). Agent correctly returned via message body — no file writes. Verdict authored on master per `git checkout master BEFORE` recipe.

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item D: "diff is purely additive (237 added, 0 deleted)." **Verified.** `git show --stat 134be52` shows `2 files changed, 233 insertions(+)` (commit message slightly overstated +237; actual is +233; both confirm zero deletions). HU loop in `extract_range_composition` lines 1780-1835 untouched.
- Reviewer claim Item A: "Partition logic mirrors HU loop exactly." **Verified.** Both loops use `_TOP_PAIR_PLUS / _DRAW_CATEGORIES / _AIR_CATEGORIES / _MEDIUM_MADE_CATEGORIES` constants from feature_extractor.py:1528-1536; same river-reclass; same `round(_, 4)`. Comment in MW path explicitly cites parity with HU.
- Reviewer claim Item E: "Pre-existing TestFeatureContract failures are FEATURE_COLUMNS count drift, not Finding B." **Verified.** Builder ran `git stash && pytest TestFeatureContract -v && git stash pop` — same 3 failures at master HEAD (without commit 14 changes). Failures explicitly mention `'nut_flush_block'` (v2.4 held-back blocker), not per_villain_*.
- Test 4/4 PASS confirmed.

All four spot-checks hold against source.

---

## Item A — Per-villain composition derivation correctness

**OK / HIGH confidence.** New ~40-line block in `_get_chain_narrowed_villain_range` MW path is a faithful, line-for-line mirror of the HU loop's partition-by-shape logic with one intentional spec-driven divergence:
- Same constants (`_TOP_PAIR_PLUS / _DRAW_CATEGORIES / _AIR_CATEGORIES / _MEDIUM_MADE_CATEGORIES`)
- Same river-reclassification (`if street_name == 'river' and cat == 'draw': cat = 'air'`)
- Same `round(_, 4)`, same `freq <= 0` skip, same try/except around `classify_hand`
- **Intentional divergence:** folded/overflowed/empty cases get zero-default composition (NOT NaN-flag like HU). Required by teaching/game's "renderable value" contract; no NoneType-error path.
- **No category leaks:** `classify_hand` enumerates exactly 8 categories `{nuts, strong_value, good_value, draw, medium_made, weak_made, bluff, air}`; the 4 buckets partition exhaustively (3+1+2+2=8). Sum-to-1.0 contract holds.

## Item B — Step 10b promotion in `extract_all_features`

**OK / HIGH confidence.** Verified:
1. HU empty-dict default set BEFORE the MW gate (lines 2272-2274 unconditional), then MW gate overwrites at 2285. HU and unknown cases keep `{}`.
2. MW gate `if _num_opp >= 2 and _opp_positions:` matches the chain helper's own MW gate at line 740.
3. `assign_opponent_positions` fallback identical to equity/partition path at line 1430 — cache key tuple aligns, cache hit confirmed.
4. Cache reuse via `hand=hand` argument; new `per_villain_composition` key populated INSIDE the helper before meta is cached, so any cache entry written by this commit's helper carries the key. Pre-commit-14 cached entries (long-running deploy window) lack the key but `.get('per_villain_composition', {})` fallback returns `{}` — survivable.

## Item C — Test coverage adequacy

**OK / HIGH confidence.** All 4 MUST #46 tests PASS. Test 2 (composition) is the key regression guard for the cross-stream contract: if a future commit silently drops or renames any of the 3 promoted keys, the assertion fires loudly. Test 4 covers both explicit-HU and default-no-key cases.

Non-blocking gap (out of scope): no test exercises `_action_history` to drive an actual fold, so tests 1+3's "no folded" branch is the only tested branch. Coverage breadth, not contract correctness.

## Item D — HU regression contract

**OK / HIGH confidence.** Diff is purely additive (237 inserted, 0 deleted; 2 files only). HU loop in `extract_range_composition` untouched. Existing scalar fields (`villain_top_pair_plus_pct` etc.) unchanged on HU rows. HU regression structurally impossible.

## Item E — Pre-existing test failures attribution

**OK / HIGH confidence.** 3 failures in `tests/test_multiway_features.py::TestFeatureContract` are about FEATURE_COLUMNS count drift (55 vs 59 from v2.4 held-back blockers — `nut_flush_block` etc.), NOT about per_villain_*. Empirically verified by `git stash` test on master HEAD (same 3 failures without commit 14 changes). PR description's attribution is correct.

## Item F — Cross-stream contract verification

**OK / HIGH confidence.** Cross-stream contract from `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md` exactly matches shipped:

| Spec | Shipped |
|---|---|
| `_per_villain_folded: Dict[str, bool]` | ✓ |
| `_per_villain_composition: Dict[str, Dict[str, float]]` with triple keys `tp_plus / medium / draw / air` | ✓ |
| `_per_villain_overflowed: Dict[str, bool]` | ✓ |
| Empty-dict-on-HU (no NoneType) | ✓ |
| Composition triple sums to ≈1.0 per opponent | ✓ |

**Both downstream consumers' contracts are met:**
- **Teaching (HOLD #5 unblock — C5.2 fixture swap):** can read `features['_per_villain_folded']` and `features['_per_villain_composition']` directly from `extract_all_features` output. F3/F4 multiway sentinels can swap to production rows. HU rows produce empty dicts so renderer's `len()` / iterate paths don't NoneType-error.
- **Game per-villain range bars:** UI can iterate `features['_per_villain_composition'].items()` for per-opponent rendering. The 4-key triple sums to ≈1.0 so bars stack correctly without renormalization.

## Item G — Scope / no-creep

**OK / HIGH confidence.** Exactly 2 files modified (feature_extractor.py + new test file). No drift into renderer / classifier / validator / range_narrowing / oracle_router / gto_model / train_model / teaching consumer / game consumer. Pure feature-extractor + new test.

---

## VERDICT

**APPROVE**

**Rationale:** All 7 items OK with HIGH confidence. The MW per-villain composition derivation is a faithful, line-for-line mirror of the HU loop's partition-by-shape logic with one intentional spec-driven divergence (zero-default instead of NaN-flag for folded/overflowed/empty cases — required by teaching/game's "renderable value" contract). Step 10b promotion correctly handles HU (empty-dict defaults BEFORE the MW gate), MW gate (consistent with existing equity/partition fallback), and cache reuse (passes `hand=hand`). The 4 new MUST #46 tests cover the cross-stream contract with adequate regression-guard strength. Pre-existing TestFeatureContract failures empirically verified as v2.4 held-back-blocker FEATURE_COLUMNS count drift, unrelated to commit 14. Pure additive diff (zero deletions, 2 files, 233 lines) — no scope creep, no HU regression possible.

**Required fixes:** None.

**Blockers:** None.

**Cross-stream readiness assessment:** **READY.** The promoted-field contract is complete and correct for both downstream consumers (teaching HOLD #5 + game per-villain range bars). Merge is safe.

---

## Action

**Builder:**
1. Post comment on PR #7 referencing this verdict.
2. Run checkpoint #3 (post-verdict-comment) per the orchestrator's STOP-extension directive — UNKNOWN settle to CLEAN per protocol clarification.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check (PR state, branch naming, --merge not --squash, verdict provenance line present).
3. Merge PR #7 with `gh pr merge 7 --merge --delete-branch`.
4. **CRITICAL post-merge**: write the cross-stream notification comms:
   - `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_<date>.md` — triggers teaching's C5.2 fixture swap process
   - `MAIN_TERMINAL_TO_GAME_<date>-<letter>.md` — triggers game's per-villain range bars + range_position_desc rename consideration
5. Continue Stage 3.5 → commit 15 greenlight.

**Owner:** Wake to a merged commit 14 + cross-stream unblocks transmitted + commit 15 ready.

## Reference

- PR #7: https://github.com/beytell1-sketch/river-rats-v2/pull/7
- Greenlight directive: `review/comms/MAIN_TERMINAL_PR_6_MERGED_COMMIT14_GREENLIGHT_2026-04-26.md`
- Cross-stream finding origin: `review/comms/MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md`
- Rollback tag: `stage3.5-pre-commit-14` at master HEAD before commit 14 was authored
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
- Restart protocol: `review/comms/BUILDER_RESTART_PROTOCOL_2026-04-25.md`
