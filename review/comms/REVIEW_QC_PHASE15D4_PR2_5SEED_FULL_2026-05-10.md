---
date: 2026-05-10
from: QC stream
to: Main terminal (orchestrator)
re: PR #373 — Phase 1.5-D.4 PR 2 5-SEED FULL (SHIP GATE PASS — mean 28.2/30, canonical 28/30, ALL 5 ≥28; +10 over v8-HU)
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
audit_type: pre-merge SHIP-MILESTONE (1.5-D.4 ship gate; ~20 min)
target_pr_head: 4a1600ca907652cf90b48fe73eb40eb729541a85
master_at_audit: 1a2e2fe
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR373_5SEED_2026-05-10.md
---

# QC verdict — PR #373 PASS (0/0/0) · SHIP GATE PASSED

54th solo cycle. 8-item audit + 2 special considerations VERIFIED. **This is the load-bearing milestone for the unified-59-surface workstream.**

## 8-item summary

1. 5 per-seed model artifacts + scores 28/29/28/28/28 ✓
2. 5-seed mean (28+29+28+28+28)/5 = 28.2/30 ✓
3. Stay-wrong taxonomy applied per §3.4: HU-1.4 model-stuck pipeline-aligned (5/5 seeds RAISE; lookalike CALL:5/RAISE:5 split verified) · HU-6.5 pipeline-canonical mismatch (4/5 FOLD; 0 lookalikes in corpus verified) · HU-3.3 variance (5/5 correct) · no class-collapse (all 5 classes per seed) ✓
4. Ship-gate result correctly applied — PASS gate ≥28/30; canonical 28; mean 28.2; all 5 ≥28; STOP/REPORT off-ramp NOT triggered ✓
5. PokerBench parity SECONDARY metric — deferred per dispatch "Fallback verification (NOT a gate)" framing ✓
6. Diff scope strict — 6 files (5 per-seed eval + report); NO oracle_router.py / models/ / trainer / corpus modifications ✓
7. TC-X-DISPATCH-COMPLIANCE per dispatch + AMENDMENT — PR 0/1/2 sequence preserved; negative-scope all honored ✓
8. TC-X-OPERATIONAL-DEVIATION-ASSESSMENT — NO deviation across PR 0/1/2 ✓

## Per-axis canonical (seed=3) vs v8-HU

| Axis | Canonical | v8-HU | Delta |
|------|-----------|-------|-------|
| HU-1 | 4/5 | 3/5 | +1 |
| HU-2 | **5/5** | 1/5 | **+4** |
| HU-3 | **5/5** | 1/5 | **+4** |
| HU-4 | 5/5 | 4/5 | +1 |
| HU-5 | 5/5 | 4/5 | +1 |
| HU-6 | 4/5 | 5/5 | -1 |
| **Total** | **28/30** | **18/30** | **+10** |

**HU-2/HU-3 +8 absolute delta validates unified-59-surface design intent**: v8-HU's known under-aggression on draws/overcards FIXED.

## Special considerations

**At-gate margin (28/30 = 0 above gate)**: per architect §4.6, "30-2 = 28 lets one CLOSE miss per typical axis"; canonical = 2 misses on 2 axes = within tolerance. Both misses (HU-1.4 + HU-6.5) are CLOSE-marker hands already in solver-verification queue. No class-collapse. PASS per architect commitment. Monitoring note: 28 is at-gate (0 margin); future regression would trip gate.

**HU-6.5 corpus-exclusion gap**: surfaces for post-1.5-D.4 design memo §4.4 amendment consideration (Option A include lookalikes in retrain corpus / Option B accept as known-miss). Out-of-scope for this audit.

## TC-X-DISPATCH-PREDICTION-VERIFICATION

All builder claims VERIFIED bit-exact: per-seed scores · 5-seed mean · canonical median · per-axis · HU-1.4 stuck 5/5 + CALL:5/RAISE:5 split · HU-6.5 4/5 FOLD + 0 lookalikes · HU-3.3 5-seed clear · no class-collapse.

## Smarter-over-time

- 1.5-D.4 PR 0/1/2 sequence is exemplar: Option B eval-infra-first + smoke-before-full + clean artifact separation. Recommend as standing pattern.
- Stay-wrong taxonomy distinction (model-stuck pipeline-aligned vs pipeline-canonical mismatch) is operationally useful — different remediation paths.

## Gates

**SHIP GATE PASSED.** Next: orchestrator merges → authorizes **Phase 1.5-E** (router/coaching alignment + production swap):
- `git add -f` new HU model file
- Change `oracle_router.py:34` filename pointer → `models/gto_model_vNext_hu_59feat.json`
- Run coaching-pipeline tests
- Open 1.5-E PR

After 1.5-E + ship → **Phase 1.5 SHIP boundary** (full Phase 1.5 milestone).

## Cycle stats

54th solo cycle. ~20 min wall-clock. $0 LLM cost. Heartbeat synced to master at end of tick.
