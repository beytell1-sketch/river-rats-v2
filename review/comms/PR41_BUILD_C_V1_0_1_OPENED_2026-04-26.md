---
date: 2026-04-26
from: Logic builder (Build C v1.0.1 author)
to: Main terminal (orchestrator) · Owner · Independent reviewer (when dispatched) · QC stream
re: PR #41 OPEN — Build C v1.0.1 fix-forward addressing QC V-C13 (59-feature embedding); per orchestrator directive MAIN_TERMINAL_PR39_DECISION_FIX_FORWARD_VC13_2026-04-26.md (Option 2); supersedes PR #39
status: BUILD COMPLETE → REVIEWER PENDING
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/41
branch: stage4-pre-dispatch/pilot-corpus-100-hand-v1-0-1
feature_commit: 5889a2a
directive_source: MAIN_TERMINAL_PR39_DECISION_FIX_FORWARD_VC13_2026-04-26.md (Option 2)
predecessor: PR #39 (Build C v1.0; will close as superseded)
qc_audit_offer: V-C13 closure verification expected
---

# PR #41 Opened — Build C v1.0.1 (V-C13 fix-forward)

## Summary

Three changed files; same SEED=20260426 → identical 100-hand selection; only `feat_dict` content changes (45→59 features per Stage 5 retrain v1.0.1 contract).

## Hash transition

| | v1.0 (PR #39) | v1.0.1 (this PR) |
|---|---|---|
| SHA256 | `492154...ef4b` | `c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40` |
| Bytes | 131,835 | 173,079 (+41,244 from richer feat_dict) |
| feat_dict feature count | 45 (legacy) | 59 (Stage 5 v1.0.1 contract) |

## What changed

- `scripts/build_pilot_corpus_100_hand.py` — adds `extract_all_features` re-extraction loop per record at corpus-build time; filters to `EXPECTED_FEAT_DICT_KEYS = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)`; asserts 59-contract at module load + per-record
- `data/pilot_corpus_100_hand_2026-04-26.jsonl` — regenerated with 59-feature feat_dict per record
- `data/pilot_corpus_100_hand_2026-04-26.lock.json` — sidecar adds `pilot_corpus_version=v1.0.1`, `feat_dict_feature_count=59`, `feat_dict_contract_source`, `v1_0_to_v1_0_1_change`, `v1_0_sha256_predecessor`

## V-X2 NOT in scope

Per orchestrator directive: V-X2 (Phase A.5 partial-fold MW fixture source) owned by orchestrator separately.

## Reviewer dispatch context (next builder action)

Required cross-checks (different reviewer than PR #39 reviewer):
1. Reproducibility: re-run `python3 scripts/build_pilot_corpus_100_hand.py`; verify SHA256 matches `c93a41c4...5e40`
2. 59-feature contract: every record has exactly 59 keys in feat_dict; all 55 FEATURE_COLUMNS + 4 v2.4 P1 blockers present
3. Disjointness: same 0-overlap verification as PR #39 (selection didn't change)
4. Within-pilot uniqueness: 100 unique fingerprints
5. Determinism preserved: same SEED → same selection (only feat_dict differs from v1.0)
6. Lock sidecar attestations accurate
7. Source design artifacts UNTOUCHED

## Next builder actions

1. Dispatch independent reviewer (general-purpose + ml-architect/gto-expert persona); read-only
2. On reviewer return: write verdict to `review/comms/REVIEW_VERDICT_PR_41_BUILD_C_V1_0_1_2026-04-26.md`; commit + push to master with HARD branch + git status check; PR comment
3. Stand by for orchestrator merge
4. After PR #41 merged → surface `BUILDER_BUILDS_ABC_COMPLETE_2026-04-26.md` (modulo V-X2 spec edit owned by orchestrator)
5. PR #39 closes as superseded

## References

- PR #41: https://github.com/beytell1-sketch/river-rats-v2/pull/41
- PR #39 (superseded): https://github.com/beytell1-sketch/river-rats-v2/pull/39
- Orchestrator decision: `MAIN_TERMINAL_PR39_DECISION_FIX_FORWARD_VC13_2026-04-26.md`
- QC PR #40 finding: V-C13
- Stage 5 retrain v1.0.1 contract: §Hyperparameters point #4
- Feature extractor: `river-rats-core/feature_extractor.py`

**Status: PR #41 OPEN. Build C v1.0.1 complete. Reviewer dispatch is next builder action.**
