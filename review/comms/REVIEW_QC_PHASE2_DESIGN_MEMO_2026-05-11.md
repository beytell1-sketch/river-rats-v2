---
date: 2026-05-11
from: QC stream
to: Main terminal (orchestrator)
re: PR #388 — Phase 2-A unified surface design memo (D5 refresh + 4-way feature gap + AMENDMENTS 1+2+3 folded; design-only; 21 candidates → 74-80 surface; 9 owner-scope items)
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT (1 cosmetic ordering self-flagged by builder; acceptable)
audit_type: pre-merge milestone (Phase 2-A design memo; ~25 min)
target_pr_head: ee1da68cf
master_at_audit: 4311f02
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR388_PHASE2_DESIGN_2026-05-11.md
---

# QC verdict — PR #388 PASS (0/0/0)

57th solo cycle. 17-item audit covering base memo (§1-§7) + AMENDMENTS 1+2+3 (§3.X + §3.Y + §X + §Y + §6.8 + §6.9) VERIFIED.

## 17-item summary

### Part A — Base memo
1. §1 current state attestation (1.1-1.7) ✓
2. §2 D5 blueprint refresh (2.1-2.4) ✓
3. §3 4-way feature gap (3.1-3.3) ✓
4. §3.X street distribution AMENDMENT 1 (3.X.1-3.X.6, 6 sub-items) ✓
5. §3.Y re-raise × players-left AMENDMENT 2 (3.Y.1-3.Y.7, 7 sub-items; 6 candidate features named; 4 net after collinearity) ✓
6. §4 surface lock — 21 candidates (11 D5 + 6 4-way + 4 re-raise) → 74-80 surface ✓ matches builder claim
7. §5 sub-phase decomposition 2-A through 2-H (with 2-E.0 NEW insertion before 2-E) ✓
8. §6 owner-scope items 9 total (6.1-6.9) ✓
9. §7 negative scope — NO build/train/corpus confirmed ✓

### Part B — AMENDMENT 3 fold
10. §X labeller readiness (X.1-X.6) — HU brief survey + 4-way brief design (multiway range-chain + squeeze-pressure + closing-action + anti-rule + bucket-first) + 29-hand calibration (vs HU 28; +1 axis breadth) + 5-hand pilot NEW sub-phase 2-E.0 + FL4-incident cost-of-failure ✓
11. §Y 5-way scope (Y.1-Y.5) — state assessment + **5-way file MISSING INDEPENDENTLY VERIFIED** (git ls-files empty; ls No such file; router `_get_oracle` graceful fallback to nearest available descending = design observation NOT routing bug) + surface/corpus implications + Architect Option B (defer to Phase 3) per quality default ✓
12. §6.8 + §6.9 new owner-scope items present; total = 9 ✓

### Part C — Process discipline
13. TC-23 EXISTENCE + CONTENT — git-tracked + content matches all 4 dispatches; 724 lines (≈720 estimate) ✓
14. Design-only scope strictly preserved — 6/6 negative-scope items honored (NO source / data / corpus / training / models / build) ✓
15. TC-X-DISPATCH-COMPLIANCE per PR #385 + #386 + #387 + #389 — all 4 dispatches addressed; architect/ml-architect/gto-expert hats evident; counts consistent ✓
16. Self-flagged cosmetic — §3.4/§3.5 ordering after §X §Y due to amendment-fold sequencing. QC categorization: cosmetic-only; substantive coverage complete. ACCEPT.

### Part D — Architect-flagged gap
17. §1.6 "multiway-specialist-gap" — acknowledged as known design constraint; §6.9 owner-decides remediation ✓

## 5-way file-missing finding (architect-flagged, QC-verified)

**Verdict: design observation, NOT routing bug.**

Evidence:
- `git ls-files river-rats-core/models/gto_model_v9_5way.json` → empty (not git-tracked)
- `ls river-rats-core/models/gto_model_v9_5way.json` → "No such file"
- Router `_get_oracle()` at `oracle_router.py:94-109`: graceful descending-key fallback; 5+ opponents clamp to key=4 → cascades to 3 → 2 → 1 (vNext-HU-59); no crash
- Production behavior: 5+-opponent calls receive HU-trained predictions (model-quality degradation; not failure)
- §6.9 owner-scope item covers this: Option A (build 5-way) vs Option B (defer to Phase 3)

Architect's Option B default per quality + scope discipline ACCEPT.

## TC-X-DISPATCH-PREDICTION-VERIFICATION

All builder claims VERIFIED: 2 commits / 1 file / 724 lines ✓; 21 candidates (11+6+4) ✓; 74-80 surface ✓; 9 owner-scope items ✓; 5-way file MISSING (design observation) ✓; design-only scope preserved ✓; §3.4/§3.5 cosmetic ordering self-flagged ✓.

## TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (10th application)

NO deviation. Builder Path-A-amended via 2-commit sequence to fold AMENDMENT 3 cleanly. All 4 dispatches addressed in single combined memo.

## Smarter-over-time

- 5-way graceful fallback pattern = robust missing-model safety net (`oracle_router._get_oracle` descending-key cascade); useful precedent for future surface expansions
- 9-owner-scope-item pattern = highly orchestrator-friendly for AskUserQuestion surfacing; recommend as standing pattern for design memos
- AMENDMENT-fold-via-2-commit pattern = clean git history + amendment provenance
- Sub-phase 2-E.0 pilot = exemplar `feedback_pilot_first_for_long_jobs.md` application; FL4-incident-driven cost-of-failure prevention

## Gates

PR #388 cleared. Next: orchestrator merges → surfaces 9 owner-scope items (6.1-6.9) for owner ratification via AskUserQuestion → after owner ratifies → Phase 2-B pilot dispatch (3-candidate pilot per architect's design).

## Cycle stats

57th solo cycle. ~25 min wall-clock. $0 LLM cost. Heartbeat synced to master at end of tick.
