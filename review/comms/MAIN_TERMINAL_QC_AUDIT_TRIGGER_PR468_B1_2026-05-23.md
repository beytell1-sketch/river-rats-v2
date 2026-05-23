---
date: 2026-05-23
from: Orchestrator (Main Terminal)
to: QC (river-rats-qc/ terminal)
re: Pre-merge audit dispatch for PR #468 — Phase 2-F1 B1 (positional_action_chain_scenarios.py)
status: FIRE NOW
type: MILESTONE pre-merge audit per feedback_qc_required_before_approval
target_pr: river-rats-v2#468
target_branch: builder-phase2-f1-b1-2026-05-22
target_base: master (220ac0d)
authorization: this is the explicit MAIN_TERMINAL_* trigger per feedback_explicit_action_trigger
---

# MAIN_TERMINAL — QC: fire now A1/B1 audit on PR #468

QC, you are the named auditor of PR #468 (Builder B1 implementation —
`positional_action_chain_scenarios.py`). FLAG-only audit per
`project_river_rats_qc`.

## Builder report headline numbers (to verify, not assume)

- 5 files / +1793 lines (single-scope payload per `feedback_shared_tree_commit_hygiene`)
- 20/20 unit tests PASS (CFP-1..6 + QUOTA-1..6 + VALIDATION-1..2 + ordering)
- All 5 A1 quota floors PASS on 24-spec output:
  - facing-raise 10/24
  - river 5/24
  - position-balance 6/6 classes ≥1
  - top-12 12/12
  - sandwich 5/24
- 0 prompt/brief/KB changes
- RNG-deterministic; <1ms generation time
- 8/9 RATIFICATION_A1 acceptance criteria satisfied (criterion #9 = this audit)
- Branch base = master 220ac0d (single-commit ahead)

## Required audit dimensions

### Code correctness vs RATIFICATION_A1

1. Verify `river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py` exists (per RATIFICATION_A1 file-path spec)
2. Module-level function signatures match RATIFICATION_A1 spec (`generate_chain_scenarios`, `enumerate_top_12_chains`, `generate_phase_2f_chain_quota`, `validate_chain_fingerprint`)
3. 7-tuple chain fingerprint implementation matches v1 blueprint §3 (ordered, not sorted; chain_shape enum included)
4. 274 enumerated chain fingerprints producible (108 flop + 94 turn + 72 river)
5. Top-12 anchor selection algorithm matches v1 §5.1 (re-derived from `batch_00{1..8}_consensus_v2.jsonl` with escalation gate if any rank shifts >2 positions per RATIFICATION_A1 commitment #3)

### Quota arithmetic verification

6. Independently re-run the yield test (or the 24-spec generator) and verify Builder's claimed floors:
   - facing-raise ≥10/24 (target ≥10 per 50-hand batch; 24 enumerated slots only — confirm extrapolation rationale to 50-hand batch)
   - river ≥5/24
   - position-balance: each of {UTG, MP, CO, BTN, SB, BB} appears ≥1 in enumerated slots (collapse rule {EP, HJ} → MP per orchestrator addendum)
   - top-12 12/12 (all 12 anchors covered exactly once)
   - sandwich ≥4/24 (Builder reports 5/24; verify the +1 isn't a quota-miscount)

### Test coverage

7. Re-run `pytest` on the test file; verify 20/20 PASS independently of Builder's claim
8. Verify all 6 CFP (canonical-form preservation) tests present per v1 blueprint
9. Verify all 6 QUOTA tests present (one per floor + 1 extrapolation/sandwich edge case)
10. Verify the 2 VALIDATION tests cover invalid chain rejection per `validate_chain_fingerprint`
11. Verify ordering test — fingerprints are ordered-tuple-stable (per v1 blueprint commitment that order matters)

### TC-23 EXISTENCE + CONTENT (per `feedback_tc23_existence_must_be_git_tracked`)

12. `git ls-files river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py` returns non-empty
13. `git ls-files river-rats-core/tests/test_positional_action_chain_scenarios.py` returns non-empty (or matching test file location)
14. CONTENT: chain_shape enum referenced by both module and tests; no orphan enum values
15. CONTENT: no `predicted_sizing_pct` writes (only reads from input contexts; output uses split schema)

### Brief/corpus/source integrity

16. `git diff origin/master -- data/4way_labeller_brief.md` returns empty (brief v2 unchanged per Phase 2-F1 STAGED scope)
17. `git diff origin/master -- data/4way_corpus/full_700/` returns empty (batches 001-008 frozen per RATIFICATION_A1)
18. `git diff origin/master -- river-rats-core/sizing_schema_normalizer.py` returns empty (A0.1.x frozen)
19. `git diff origin/master -- knowledge/three_way_gto.md` returns empty (Phase 2-F2 scope, not F1)
20. `git diff origin/master -- prompts/gto_labeller_v3.4.md` returns empty (Phase 2-F2 scope, not F1)

### Branch hygiene

21. `git merge-base origin/builder-phase2-f1-b1-2026-05-22 origin/master` equals master HEAD (220ac0d)
22. `git diff --name-only origin/master..origin/builder-phase2-f1-b1-2026-05-22` lists EXACTLY the 5 expected files
23. The 5 untracked `mass_labelling_*` directories Builder mentioned are NOT in the PR diff (orphan artifacts excluded per single-scope payload)

### Cross-stream sanity

24. CFP-1..6 bug checklist: verify each bug case from v1 blueprint §5.1's CFP list has corresponding regression-test coverage
25. RNG-determinism: re-run yield test with declared seed; verify bit-identical output to Builder's claim
26. Re-run anchor frequency audit (RATIFICATION_A1 commitment #3 escalation gate): re-derive top-12 chains from `batch_00{1..8}_consensus_v2.jsonl` and confirm rank stability (no rank shifts >2 positions vs v1 §5.1 anchor predictions)

## Bonus (optional, defer if blocked)

If you have bandwidth after the milestone audit, also produce a routine TC-25 batch finding covering:
- PR #465 (§3.6 ratification, docs-only)
- PR #458 (Phase 2-F drafts bundle, REVIEW-ONLY)
- PR #466 (A1 ratification + B1 fire-now)

These were marked routine-TC-25 batchable in QC's session-start report. Single batched findings file is acceptable.

## Verdict deliverable

Write to `~/river-rats-qc/findings/2026-05-23-pr468-b1-positional-chain-scenarios.md` per QC restart protocol format. Commit + push to QC `origin/main`. Bump `.last_seen_master_sha` to current v2 origin/master.

## Decision routing

- **PASS** → orchestrator merges PR #468; immediately dispatches Builder for batch_009 generation (pilot for the new scenarios per `feedback_pilot_first_for_long_jobs` — single batch first, then 010-014 conditional on quota materialization)
- **ISSUES FOUND** with SHOULD_FIX only → orchestrator decides per-issue; routine items deferred to follow-up, blocker items kick back to Builder
- **FAIL** or BLOCKER ≥ 1 → orchestrator blocks merge; Builder revises; re-audit cycle

## Cross-stream coordination

Builder terminal is idle (waiting your verdict). 5-way reference workstream (PR #467) is in parallel and does not affect this audit.

Heartbeat at end of tick: bump `.last_seen_master_sha` to whatever `origin/master` shows when you commit your findings (will still be 220ac0d if PR #468 hasn't merged yet; orchestrator handles bumping post-merge).

---

**Authorization** per `feedback_listen_to_orchestrator_always`: this directive addressed to QC by name with named PR target = sufficient authorization. No further owner approval needed before audit fires.
