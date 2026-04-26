---
date: 2026-04-26
from: Logic builder (Build D author)
to: Main terminal (orchestrator) · Owner · Independent reviewer · QC stream
re: PR #43 OPEN — Build D: 5-hand synthetic partial-fold MW fixtures for Phase A.5 (closes V-X2); per orchestrator directives MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md (fa280d6) + MAIN_TERMINAL_PR41_MERGE_ACK_BUILD_D_KICKOFF_2026-04-26.md
status: BUILD COMPLETE → REVIEWER PENDING
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/43
branch: stage4-pre-dispatch/phase-a5-partial-fold-fixtures
feature_commit: 70bb66f
qc_audit_offer: V-D1...V-D3 vectors expected; TC-15 multi-expert per QC standing offer
---

# PR #43 Opened — Build D (Phase A.5 partial-fold MW fixtures)

## Summary

5 synthetic fixtures + generator + sidecar; SHA256 `c196fb82cf78b6c02660dca72051df36938ebfeca87ebd23e935ec96b510f513`; 10,761 bytes. Closes V-X2.

After PR #43 merges: V-X2 closed; orchestrator's Phase A.5 spec edit lands; pilot dispatch resumes. **Final pre-pilot blocker.**

## Diversity coverage

- Streets: flop=2, turn=2, river=1
- Folded positions: BB, SB, CO, BTN, HJ, UTG (all 6 unique)
- Live villain counts: 1 (PF_003), 2 (PF_002 + PF_005), 3 (PF_001 + PF_004)

## Validator-caught + fixed pre-commit

PF_002 + PF_005 originally listed BB in `villain_positions` despite BB folding flop. The script's structural validator (`villain_positions excludes folded positions`) caught both before commit; fixtures rewritten with progressive-fold scenarios (live set evolves across streets). Net positive — better diversity coverage.

## Reviewer dispatch context

Cross-checks REQUIRED:
1. Reproducibility: re-run script, verify SHA matches
2. Per-fixture validity: each has fold + live set excludes folds + num_opponents matches
3. Diversity: streets / folded positions / live villain counts adequately covered
4. Disjointness: 0 overlaps with all 4 forbidden sets (49+21+9+100=179 dedup)
5. 59-feature `feat_dict` per fixture
6. Source design artifacts UNTOUCHED

## Next builder actions

1. Dispatch independent reviewer
2. On reviewer return: write verdict + commit + push to master + PR comment
3. Stand by for orchestrator merge
4. After PR #43 merges → compose `BUILDER_BUILDS_ABCD_COMPLETE_2026-04-26.md` (final builder signal before pilot dispatch)

## References

- PR #43: https://github.com/beytell1-sketch/river-rats-v2/pull/43
- Build D directive: `MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md`
- V-X2 origin: `QC_PRE_MERGE_AUDIT_PR39_2026-04-26.md`
- Build C v1.0.1 (hash predecessor): `c93a41c4...`

**Status: PR #43 OPEN. Build D complete. Final pre-pilot build.**
