---
date: 2026-04-26
from: River Rats QC stream
to: Main terminal (orchestrator) · Logic builder · Owner (briefed)
re: PR #24 pre-merge QC audit — Task 5 Pilot orchestration v1.0 (FINAL Wave 2 task; gates Stage 4 pilot dispatch); CONVERGED APPROVE-WITH-NITS; 1 MEDIUM (terminology drift) + 11 LOW (pre-dispatch fix-list); recommend merge with pre-dispatch fixes bound to owner approval not merge
status: FLAG (advisory; pre-merge informational; orchestrator's dispatched reviewer makes the merge call)
severity: CONVERGED PASS at gate / 1 MEDIUM (pre-dispatch fix advised) / 11 LOW (advisory tightening) / 2 NIT
multi-expert verdict: CONVERGED APPROVE-WITH-NITS — both agents recommend merge
PR head: 4b6c50aa62b134ac16c3263bb968add1860d5578
full finding: ~/river-rats-qc/findings/2026-04-26-pr24-pre-merge-task5-pilot-orchestration.md
---

# QC Pre-Merge Audit — PR #24 (Task 5 Pilot orchestration v1.0)

## Headline

**APPROVE-WITH-NITS.** Spec fills v0.1 DRAFT (284 lines) → v1.0 (836 lines, 40KB) cleanly. All 5 directive fill-ins + 2 secondary items resolve concretely. All 13 PRE-DISPATCH PREREQUISITES are operator-checkable. 3 UNCERTAIN tags appropriately scoped + mitigated. Cross-references verified.

**Multi-expert CONVERGED APPROVE-WITH-NITS.** Recommend merge. Pre-dispatch fix-list bound to owner pilot-dispatch approval, NOT to Task 5 merge.

## MEDIUM finding (recommend pre-dispatch fix)

### M-1 — Stage 5 contract terminology drift on Highlighter H1 brief

Spec line 591 (highlighter brief substitution context):
> "the 55-feature vector + post-commit-14 multiway promotions = 59 raw features per Stage 5 retrain v1.0.1"

Stage 5 v1.0.1 (`STAGE5_RETRAIN_PROTOCOL_v1_0.md` lines 22, 57, 143, 234, 665) says the +4 features are **v2.4 BLOCKER features** (`nut_flush_block`, `nut_made_block_pct`, etc.), NOT "post-commit-14 multiway promotions." The terminology "post-commit-14 multiway promotions" appears nowhere in Stage 5 or in `prompts/gto_labeller_v3.1.md`.

Arithmetic (55+4=59) correct; semantic label wrong. H1 highlighters reading this brief look for "multiway-promotion features" that don't exist as such.

**Suggested fix:** rewrite line 591 to:
> "the 55-feature vector + 4 v2.4 blocker features = 59 raw features per Stage 5 retrain v1.0.1 §Hyperparameters point #4"

Single-paragraph fix. Recommend pre-dispatch fix.

## LOW pre-dispatch fix-list (5 items recommended; bind to owner approval)

| # | Finding | Suggested fix |
|---|---------|---------------|
| L-1 | Cross-protocol output-path firewall not enforced (Protocol C labellers could path-traverse to read Protocol A/B outputs) | Add labeller tool restriction: Read/Write only within `review/pilot_run_<date>/labels/protocol_<your_protocol>/agent_<your_slot>/` |
| L-8 | Tool restrictions absent from non-orchestrator briefs (Labeller / Highlighter / Reviewer / Adjudicator briefs lack explicit ALLOWED/PROHIBITED lists) | Apply Task 4.5 whitelist-or-raise discipline consistently across all 6 briefs |
| L-11 | API-tier + model-selection are footnotes (drive 5× cost swing + rate-limit risk) | Promote to PRE-DISPATCH PREREQUISITES rows |
| L-12 | Path resolution: `LABELLING_PIPELINE.md` cited without `docs/` prefix in 2 locations | Path correction (`docs/LABELLING_PIPELINE.md`) |

## LOW findings deferred to v1.1 / pilot-runtime (7 items)

- L-2 "Anonymised" reasoning aggregation undefined (style-leakage between protocols)
- L-3 Adjudicator role-separation enforcement is assertion, not mechanical guard
- L-4 No HARD CAP on aggregate cost telemetry (pilot can run past $700 envelope without auto-halt)
- L-5 No aggregate schema-violation DROP halt (Phase D κ on degraded set silently)
- L-6 Labeller resumption mid-batch rule ambiguous
- L-7 Marginal-calibration chain (sequence of 20/24-pass-but-same-hand-missed agents) doesn't trigger HALT
- L-9 Protocol C raise-sizing scope unclear (33%/66% is RAISE-specific; BET sizings street-specific)
- L-10 Inter-batch dispatch gating ("Batch N+1 starts when?") not specified

## NIT findings

- N-1 Phase A 33-way concurrency may also need rate-limit preflight (not just Phase B)
- N-2 Locked plan §4.2 line 146 has stale agent count — pre-existing, not Task 5 scope, flag for plan-level housekeeping

## Multi-expert convergence (TC-15 fifth demonstration)

| Aspect | Agent #1 operator-readability | Agent #2 adversarial |
|--------|--------------------------------|----------------------|
| Merge recommendation | APPROVE-WITH-NITS | APPROVE-WITH-NITS |
| 5 directive fill-ins | ALL PASS | ALL PASS (with deep-probe findings) |
| 13 PRE-DISPATCH PREREQUISITES | All right + verifiable | Mostly verifiable + 2 missing prereqs (L-11) |
| Cross-references | All verified | 1 MEDIUM drift surfaced (M-1) |
| Findings: HIGH | 0 | 0 |
| Findings: MEDIUM | 0 | 1 |
| Findings: LOW | 2 | 11 |

CONVERGED on merge call. DIVERGED at finding depth — adversarial agent's failure-mode + cross-reference probing surfaced gaps operator-readability framing didn't reach. Same protocol-diversity outcome as prior 4 TC-15 demonstrations.

## Author's 4 surfaced concerns

Agent #1 verified each is honestly framed with adequate mitigation:
1. 5-vs-15 parallelism — preflight live tier check + upgrade escape clause. Adequate.
2. Per-call latency ~30-90s — concrete "instrument first 5 calls + halt if >2×" gate. Adequate.
3. Highlighter context-scope independence — middle-path coherent + matches locked plan §3 (NOTE: agent #2 LOW-2 flags "anonymised" needs concrete definition).
4. Adjudicator role independence — covered in brief (LOW-3 recommends mechanical guard at Pilot Orchestrator level).

## Recommendations

### To orchestrator's dispatched reviewer
- **APPROVE merge.** Spec is structurally sound; 13 prereqs are load-bearing safety net.
- M-1 worth flagging for builder to fix-forward OR fold into a Task 5.1 cleanup.

### To owner pre-pilot-dispatch
Bind these 5 fixes (M-1 + L-1 + L-8 + L-11 + L-12) to owner pilot-dispatch approval, NOT to Task 5 merge. ~30 min total fix effort.

### Stage 4 pilot dispatch gate (after Task 5 merges)
- ✅ All 5 prep tasks sealed (Task 5 merge clears)
- ⏳ Phase 2 HIGH-1 teaching renderer translation (pending teaching builder)
- ⏳ HIGH-4 cross-stream coordination — Option B picked at `dfa57e3` (logic adds aggregate derivation)
- ⏳ QC pre-pilot sweep clean (Phase 5 standing roadmap; QC will execute when above clears)
- ⏳ Owner explicit greenlight

After Task 5 merge → **7/9 SEALED**.

## STOP-condition assessment

No STOP triggered. M-1 is documentation-prose drift; spec works mechanically. LOW findings are operator-discipline tightening.

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-pr24-pre-merge-task5-pilot-orchestration.md`
- PR #24: https://github.com/beytell1-sketch/river-rats-v2/pull/24

**Status: QC pre-merge audit COMPLETE. CONVERGED APPROVE-WITH-NITS. Recommend merge per orchestrator's reviewer dispatch. Pre-dispatch fix-list bound to owner approval.**
