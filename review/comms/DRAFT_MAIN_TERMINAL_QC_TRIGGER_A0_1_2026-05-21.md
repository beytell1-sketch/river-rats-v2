# MAIN_TERMINAL — QC Trigger: PR A0.1 sizing_schema_normalizer

**DATE:** 2026-05-21
**AUTHOR:** Orchestrator
**STATUS:** STANDBY — fires when Builder ships PR A0.1
**TARGET PR:** river-rats-v2#460 (A0.1 normalizer implementation; SHA fea2123)
**TYPE:** MILESTONE — pre-merge QC required per `feedback_qc_required_before_approval.md`

---

## Trigger condition

This directive fires the moment Builder pushes branch `builder/a0.1-normalizer-2026-05-21` and opens a PR. Orchestrator commits this directive (with PR # filled in) and notifies QC.

---

## MAIN_TERMINAL — QC: fire now A0.1 audit

QC audits the Builder PR for A0.1 (sizing_schema_normalizer implementation). FLAG-only, audit-and-recommend, do not modify code.

---

## Audit scope

### Code correctness (against blueprint)

1. **Module structure** — verify `river-rats-core/sizing_schema_normalizer.py` exists, has provenance docstring (per `river-rats-v2/CLAUDE.md:111-122`), uses stdlib-only deps
2. **Constants** — CANONICAL_BB, CANONICAL_PCT, CANONICAL_MULT exactly match blueprint §3.2
3. **Algorithm** — RAISE normalization matches blueprint §3.2 (3 candidates, legality filter, canonical-set tie-break) byte-for-byte at the logical level
4. **API surface** — public functions `normalize_label`, `normalize_batch`, CLI entrypoint all present
5. **Validation rules** — §1.4 enforced (action/field combo legality)

### Test coverage

6. **All 12 tests from blueprint §3.5 present** — verify each test name + corresponding assertion
7. **Test pass rate** — re-run test suite and confirm 12/12 passing
8. **Edge cases** — any tests added beyond the 12 specified? Are they sound?

### TC-23 EXISTENCE + CONTENT drift audit

9. **EXISTENCE** — `git ls-files river-rats-core/sizing_schema_normalizer.py` returns non-empty (per `feedback_tc23_existence_must_be_git_tracked.md`)
10. **EXISTENCE** — `git ls-files river-rats-core/tests/test_sizing_schema_normalizer.py` returns non-empty
11. **CONTENT** — code is internally consistent (function called in __main__ exists and signature matches)
12. **CONTENT** — no `predicted_sizing_pct` writes anywhere (single field is read-only legacy from input; outputs are split)

### Brief unchanged (orchestrator override verification)

13. **Brief integrity** — `data/4way_labeller_brief.md` is UNCHANGED in this PR (per RATIFICATION orchestrator override; brief patch moves to A0.3)
14. **No corpus mutation** — no files under `data/4way_corpus/full_700/` are modified

### Dry-run sanity

15. **Dry-run on batch_001_l1** — Builder reports `{clean, ambiguous_resolved, malformed_rejected}` in commit message. Re-run and verify the counts match Builder's report (reproducibility check).
16. **Sanity proportions** — clean+ambiguous_resolved ≥ 90% (per blueprint §7.5 prediction of ~98%); malformed_rejected ≤ 10% (per blueprint decision boundary).

### Cross-stream sanity

17. **Branch base** — Builder branch rooted at origin/master (per `feedback_orchestrator_branch_base_verification.md`)
18. **Single-file payload** — only 2 files in diff: normalizer + tests
19. **No drift from blueprint PR #459** — if QC blueprint-prereview (`findings/2026-05-21-pr459-a0-blueprint-prereview.md`) raised any BLOCKERs, verify Builder addressed them

---

## Verdict format

QC writes verdict to `findings/2026-05-21-pr{XXX}-a0-1-normalizer.md`:

```
---
date: 2026-05-21
target_pr: river-rats-v2#XXX
phase: A0.1 sizing_schema_normalizer implementation
verdict: PASS / ISSUES FOUND / FAIL
severity_summary: X BLOCKER · Y SHOULD_FIX · Z NIT
audit_type: pre-merge milestone
qc_branch: qc/pr{XXX}-a0-1-normalizer-review-2026-05-21
master_at_audit: <SHA>
---

# PR #XXX — A0.1 normalizer pre-merge audit
[findings]
```

---

## Decision routing

- **PASS** → orchestrator merges A0.1; dispatches A0.2 (backfill 001-007) and updates `.last_seen_master_sha`
- **ISSUES FOUND** with SHOULD_FIX only → orchestrator decides per-issue: ship with NITs deferred, or block-and-fix
- **FAIL** or BLOCKER ≥ 1 → orchestrator blocks merge; Builder revises and re-pushes

---

## Out of scope

- Brief audit (brief unchanged in A0.1 per orchestrator override)
- Backfill audit (that's A0.2 / G0.2)
- Batch-008 audit (that's A0.3 / G0.3)
- A2/A3/B-series audits (separate Phase 2-F directives)
