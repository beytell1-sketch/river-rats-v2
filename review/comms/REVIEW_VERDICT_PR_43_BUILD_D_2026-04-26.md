---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ml-architect + gto-expert reviewer (different dispatch from Build A/B/C/C-v1.0.1 reviewers; not Build D author)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #43 — Build D: 5-hand synthetic partial-fold MW fixtures for Phase A.5 (`70bb66f`)
status: APPROVE — 1 MEDIUM (non-blocking hash-lock determinism nit), 2 NITs; all 5 fixtures valid + diverse + disjoint + Phase A.5 usable
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/43
branch: stage4-pre-dispatch/phase-a5-partial-fold-fixtures
artifact: data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl (10,761 bytes; SHA256 c196fb82cf78b6c02660dca72051df36938ebfeca87ebd23e935ec96b510f513)
predecessor: 2a64e11 (master / PR #41 Build C v1.0.1 merged)
predecessor_directive: MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md (fa280d6) + MAIN_TERMINAL_PR41_MERGE_ACK_BUILD_D_KICKOFF_2026-04-26.md
qc_audit_origin: V-X2 from PR #40 audit on PR #39
---

# Review Verdict — PR #43 (Build D: Phase A.5 partial-fold MW fixtures)

## Provenance note
Independent ml-architect + gto-expert reviewer dispatch. Did not author Build D and was not the reviewer on Builds A/B/C/C-v1.0.1. Used Read on script + lock + Phase A.5 spec + V-X2 lookup + Stage 6 holdout + v2.3 calibration + pilot 100 corpus; ran the one allowed reproduction `python3 scripts/build_phase_a5_partial_fold_fixtures.py`; wrote inline python3 -c verification scripts for hash check, per-fixture validity, diversity coverage, disjointness re-derivation against all 4 forbidden sets, and Phase A.5 contract adherence.

## Verdict
**APPROVE — overall confidence HIGH on fixture quality; MEDIUM on hash-lock determinism (non-blocking).**

Build D ships a structurally clean, design-correct 5-hand synthetic fixture set for Phase A.5 `_villain_pos_raw` live-vs-folded discrimination. All 7 acceptance criteria except (#6 hash-lock determinism) cleanly pass. The hash-lock issue is a script-side seed omission — the **artifact bytes themselves are valid and self-consistent with the lock sidecar**; the script just won't reproduce them on a re-run. Non-blocking for pilot dispatch (the artifact is what matters, not a re-derivation), but worth surfacing for future builders.

## Per-criterion results

### 1. Reproducibility / determinism — **MEDIUM finding**
- Committed JSONL SHA256 = `c196fb82cf78b6c02660dca72051df36938ebfeca87ebd23e935ec96b510f513` ✓ matches lock sidecar attestation
- Re-running `python3 scripts/build_phase_a5_partial_fold_fixtures.py` produces a **DIFFERENT** SHA each run (observed `86d4805f...`, then `e8fd981d...`) at the SAME byte_size 10761
- **Root cause:** `feature_extractor._true_multiway_equity_mc()` uses unseeded `random.sample()` + `random.random()` for 2000-trial Monte Carlo equity estimation. Non-determinism manifests in `equity_vs_range`, `raw_equity`, `equity_margin`, `board_adjusted_hrp` (downstream of equity).
- **Why Build C v1.0.1 was reproducible and Build D isn't:** `scripts/build_pilot_corpus_100_hand.py` line 70 calls `random.seed(SEED)` at module load. Build D's docstring (line 35) explicitly says "SEED not needed for selection" — true for selection, but the SEED is also needed downstream for MC equity sampling inside `feature_extractor`. Build D omitted it.
- **Severity:** MEDIUM. The committed artifact is internally consistent (sidecar SHA matches the file bytes). Phase A.5 loads the JSONL as-is; orchestrator never re-runs the script. But: any future re-derivation (e.g. if QC wants to confirm bit-identity from source) will fail. Recommend `random.seed(20260426)` carry-forward in a follow-up nit.

### 2. Per-fixture validity — **PASS**
All 5 fixtures (`phase_a5_pf_001`–`005`) verified independently:
- Hero (2 cards) + board (3/4/5 for flop/turn/river) all from valid 52-card deck, no within-hand duplicates
- 59-key `feat_dict` exactly matches `FEATURE_COLUMNS (55) + V24_P1_BLOCKER_FEATURES (4)` per Stage 5 v1.0.1 contract
- `num_opponents` exactly equals `len(villain_positions)` for every fixture (3/2/1/3/2)
- Each has ≥1 non-hero villain `fold` token in `prior_actions`
- `villain_positions` strictly excludes all positions appearing as folded in `prior_actions` (independently verified set difference)

### 3. Diversity coverage — **PASS** (better than directive)

| Dimension | Directive recommendation | Build D delivered |
|---|---|---|
| Streets | flop=2, turn=2, river=1 | flop=2, turn=2, river=1 ✓ |
| Folded positions | spread BTN/CO/HJ/SB/UTG | All 6 covered: BB, BTN, CO, HJ, SB, UTG |
| Live villain count | mix 1/2/3 | 1-live=1, 2-live=2, 3-live=2 ✓ |
| Composition mix | EP-live/late-fold + late-live/EP-fold + multi-vill | All cases represented; PF_002/PF_005 add bonus "live set evolves across streets" coverage |

### 4. Disjointness — **PASS (0/0/0/0)**

| Forbidden source | Fingerprint count | Lock attestation | Overlap with Build D |
|---|---|---|---|
| Stage 6 holdout | 49 | 49 ✓ | **0** |
| v2.3 calibration legacy | 21 | 21 ✓ | **0** |
| v2.3 anchor extension | 9 | 9 ✓ | **0** |
| Pilot 100 corpus (Build C v1.0.1, SHA `c93a41c4...` re-verified ✓) | 100 | 100 ✓ | **0** |
| **Total deduplicated forbidden** | **179** | **179 ✓** | **0** |

### 5. Within-fixture uniqueness — **PASS** (5 unique fingerprints)

### 6. Phase A.5 contract adherence — **PASS**
Each `partial_fold_scenario` text accurately narrates: opening width → fold(s) → live set composition. The fixture's `villain_positions[0]` (used as `vp` → `_villain_pos_raw` per script line 365) is always a live opponent. PF_003 is the strictest test (sole live villain CO; if rule fails, no fallback). PF_005 tests cross-street evolved live-set on a river decision — the highest-value Phase A.5 trap for any future implementation regression.

### 7. Source design artifacts UNTOUCHED — **PASS**
Only the 3 expected files appear in the diff. No touches to `river-rats-core/`, `training-data/`, or any orchestration/spec doc.

### 8. Lock sidecar attestations — **PASS**
SHA256, byte_size, all 4 disjointness counts, all 0/0/0/0 overlap counts, street distribution, folded positions list, live villain count distribution all match independently-recomputed values.

### 9. Pre-commit validator rigor — **PASS**
Validator at lines 458–497 enforces (a) no fingerprint overlap with forbidden set, (b) no within-fixture fingerprint dup, (c) ≥1 non-hero fold in `prior_actions`, (d) `villain_positions` ∩ folded positions = ∅, (e) `num_opponents == len(villain_positions)`. Builder claim that PF_002 + PF_005 originally listed BB in `villain_positions` despite BB folding flop is exactly the kind of bug check (d) catches.

### 10. Branch verification — **PASS**
Single feature commit `70bb66f` on `stage4-pre-dispatch/phase-a5-partial-fold-fixtures`; not on master.

## Findings summary

| Severity | Finding | Disposition |
|---|---|---|
| **MEDIUM-1** | `random` not seeded before `extract_all_features` MC equity calls → script is non-reproducible across runs (committed bytes are still self-consistent with lock; only re-derivation breaks). | Non-blocking. Recommend `random.seed(20260426)` carry-forward nit for any post-pilot follow-up. Doesn't block merge — Phase A.5 consumes the JSONL artifact, not a re-derivation. |
| NIT-1 | Stage 6 spec hash drift (lock references historical `65cfbf26...`, current is `eb4d3bd3...`). Counts still match (49); spec-side cosmetic touch since Build C. | Carry-forward; not Build D's domain. |
| NIT-2 | `_count_villain_aggression`/`_calls` substring-match for hero exclusion is fragile against future overlapping position names. Currently correct for all 5 fixtures. | Defensive parse: split-then-token-compare on `[a.split(':',1)[1].strip().split()[0]]` would be robust. |

## Decision request (similar to PR #39 V-C13 pattern)

**Builder recommendation:** fix-forward Build D v1.0.1 with `random.seed(20260426)` (1-line addition; ~5 min) — same Build C v1.0.1 pattern. Quality-default per `feedback_quality_default_no_ask.md`. Estimated total: ~10-15 min build + ~15-30 min reviewer cycle.

**Alternative:** merge as-is per reviewer's "non-blocking" assessment; queue determinism fix as v1.1 housekeeping (the artifact is byte-stable on disk; pilot dispatch loads JSONL not script).

**Builder leans Option A (fix-forward).** Phase A.5 is a single-shot consumer; determinism doesn't matter at runtime. But future audit / reproducibility / compliance care about it. Cheap to fix.

## Verdict (formal)
**APPROVE for merge** per reviewer's stated "non-blocking" assessment. Decision-request to orchestrator on whether to fix-forward Build D v1.0.1 (recommended) OR merge as-is + defer determinism fix.

**Required fixes:** None.
**Blockers:** None.

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_43_BUILD_D_2026-04-26.md` ✓
2. Commit + push verdict to master with HARD branch + git status check
3. Post PR comment on PR #43 referencing verdict + decision-request on fix-forward
4. Stand by for orchestrator option call (fix-forward Build D v1.0.1 OR merge as-is + queue v1.1)

**Orchestrator:**
1. Read this verdict
2. Decide: Option A (builder fix-forward Build D v1.0.1, ~10-15 min) OR Option B (merge as-is + v1.1 queue)
3. After resolution: PR #43 (or v1.0.1 successor) merges; V-X2 closed; Phase A.5 spec edit lands; pilot dispatch resumes

**Owner:** wake to find Build D complete; one MED (non-blocking, builder recommends fix-forward) awaiting orchestrator option call.

## Reference

- PR #43: https://github.com/beytell1-sketch/river-rats-v2/pull/43
- Feature commit: `70bb66f`
- Build D directive: `MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md`
- Build D kickoff: `MAIN_TERMINAL_PR41_MERGE_ACK_BUILD_D_KICKOFF_2026-04-26.md`
- V-X2 origin: `QC_PRE_MERGE_AUDIT_PR39_2026-04-26.md`
- Build C v1.0.1 (pattern + hash predecessor): `c93a41c4...`
- Phase A.5 spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 §"Phase A.5"
- Stage 5 retrain v1.0.1 contract: §Hyperparameters point #4 (59 features)

**FINAL VERDICT: APPROVE — HIGH confidence on fixture quality; MEDIUM on hash-lock determinism (non-blocking). Decision-request to orchestrator on fix-forward path.**
