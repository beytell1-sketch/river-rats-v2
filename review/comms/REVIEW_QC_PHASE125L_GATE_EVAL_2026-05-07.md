---
date: 2026-05-07
from: River Rats QC (standalone stream)
to: Main terminal (orchestrator) · Owner · LEAD-PROGRAMMER (architect-hat)
re: PR #297 — 12.5L gate-eval synthesis (3-lever ceiling; architect-hat recommends Option A SHIP) — pre-merge audit
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 1 NIT
audit_type: pre-merge synthesis (FINAL pre-owner-gate phase)
qc_branch: qc/pr297-125l-gate-eval-review-2026-05-07
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR297_2026-05-07.md (master `d57fa37`)
target_pr_head: d9d013cf1cafa2d64e6e6d38ef507f254ff111b8
---

# QC pre-merge audit — PR #297 (12.5L gate-eval synthesis)

## Result

**PASS** (0 BLOCKER, 0 SHOULD_FIX, **1 NIT**). 39th solo cycle. Synthesis is comprehensive, internally consistent on the substantive ceiling claim, and architecturally compliant with the dispatch's 7 audit items. The single NIT is a minor labels-count discrepancy in §2.3.3 prose that does not affect any conclusion or owner-decision input.

## Audit-item walkthrough (7 items per trigger)

### 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)

PR diff: 1 file (`review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md`, 268 additions, 0 deletions). No code, data, prompts, BATCH2, river-rats-core/, training-data/, or memory edits. **Owner-scope perimeter held.** Matches dispatch §"What you do NOT do" exactly.

### 2. All 3 levers documented with empirical findings + costs

§2.2 summary table covers all three levers. §2.3 per-lever detail:

- **§2.3.1 Lever A** (variance, PR #253 + #261): 20 seeds; mean 33.10 ± 0.30; 1-σ upper 33.40; ~$0; ~2-3h. Consistent with prior QC audit of PR #261.
- **§2.3.2 Lever B** (hyperparameters, PR #265): 3 configs × 5 seeds; per-config 33.00-33.20; spread 0.20; ~$0; ~10 min wall clock. Consistent with prior QC audit of PR #265.
- **§2.3.3 Lever C** (augmented data, PR #269 → #293): 5-phase pipeline; 988-corpus 5-seed mean 33.00 ± 0.00; ~$60-70 LLM total; ~6-8h. Consistent with my just-completed PR #293 audit.

§2.4 composite cost: ~$60-70 LLM, ~12-15h wall clock, ~30 PRs (PR #228 → #295). All cost/time figures are reasonable bounds against the audit-trail record. ✓

### 3. 3 options analyzed with cost/time/risks (material parity)

§4.1-4.3:

| Option | Cost | Wall clock | # risks |
|---|---|---|---|
| A SHIP | ~$0 | ~1 day | 3 (A1 medium / A2 low / A3 low) |
| B Lever D | ~$undefined | 2-6 months | 4 (B1 high / B2 medium / B3 medium / B4 low) |
| C Advance chain | ~$50-100 | 1-2 months | 3 (C1 medium / C2 low / C3 medium) |

Each option specifies what-it-does, cost, wall clock, and ranked risks with severity. **Material parity satisfied** for owner decision-making. §4.4 comparison matrix consolidates across 6 dimensions (cost, wall clock, ceiling-break probability, production-readiness impact, sunk-cost risk, memorialization). ✓

### 4. Architect-hat recommendation present (single committed position)

§5.1: **"Recommendation: Option A — SHIP and accept v9-3way-v2.2 as the empirical ceiling."** Single committed position. §5.2 provides three-reason justification (empirical case decisive / ROI unfavorable for Option B / Option C orthogonal to ceiling decision). §5.3 explicitly notes what Option A leaves on the table for owner consideration (4 stay-wrong as low-confidence; pipeline mismatch as standing limitation; Lever D parked-not-refused).

**Compliant with `feedback_orchestrator_decides_not_recommends.md`**: architect commits to a HOW recommendation, owner retains WHAT/WHETHER decision. No menu; no hedging across multiple options. ✓

### 5. TC-X-OWNER-SCOPE-DISCIPLINE (19th formal use)

§7 explicit "What this PR does NOT do" with 6 negatives (no execution / no v3.x / no river-rats-core / no BATCH2 / no data / no decision). PR diff verified to satisfy all six. **Perimeter held.**

### 6. TC-X-DISPATCH-COMPLIANCE (18th formal exercise; durable)

Dispatch §"Scope — synthesis comm + owner-decision proposal" required 5 deliverables:

- (a) Full 12.5K experiment record → §2 ✓
- (b) Empirical ceiling claim → §3 ✓
- (c) Owner-decision proposal — 3 options minimum → §4 (3 options A/B/C) ✓
- (d) Cost/time estimates per option → §4 each option ✓
- (e) Risks per option → §4 each option (3-4 risks each) ✓

Plus dispatch §"Output" expected single-file synthesis comm at the named path. ✓ Plus dispatch §"What you do NOT do" five negatives all confirmed. ✓

### 7. Stay-wrong list final state cited; owner-scope decision data complete

§6.1 final stay-wrong table with 4 rows:

- MW-17: labelling-pipeline canonical mismatch (Path A re-tag RAISE vs canonical CALL); NO graduation.
- MW-40: labelling-pipeline canonical mismatch (BET vs canonical CALL); NO graduation.
- MW-45: model-layer-stuck (pipeline-aligned); NO graduation.
- MW-47: model-layer-stuck (pipeline-aligned); NO graduation.

Type / pipeline label / canonical label / cause / 12.5K outcome populated for each. Consistent with prior QC findings on PR #245 (MW-40), PR #281 (MW-17 axis-target shift), and PR #293 (Section E stay-wrong continues to diverge under Lever C 988-corpus retrain). ✓

§6.2 four memory candidates surfaced for owner ratification (3-lever ceiling; pipeline-canonical mismatch on MW-17 + MW-40; model-layer-stuck on MW-45 + MW-47; composition-quad terminology refresh). Routed correctly to owner per `feedback_orchestrator_decides_not_recommends.md`. ✓

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (19th formal use)
- TC-X-DISPATCH-COMPLIANCE (18th formal exercise; durable)
- TC-X-INTRA-PLAN-CONSISTENCY (informal — 12.5L synthesis cross-checked against PR #261/#265/#285/#289/#293 audit-trail)
- TC-X-METHODOLOGY-RULE-CROSSCHECK (informal — architect-hat single-recommendation rule per `feedback_orchestrator_decides_not_recommends.md`)

No new class additions; all hits durable.

## NIT-1 — §2.3.3 Lever C SCALE labels count

**Severity: NIT (informational; does NOT affect ceiling claim or any owner-decision data).**

§2.3.3 table row "-C-SCALE" claims "1050 labels". The actual SCALE phase (PR #285) audit-trail record is **700 labels** (150 hands × 4 labellers + 20 hands × 5 labellers = 600 + 100 = 700; verified in QC finding `2026-05-07-pr285-125kcc-scale-mass-labelling.md`). Sum of all Lever C labelling phases (PILOT 100 + PILOT-FIX 50 + SCALE 700 + Opus tier-up 120) = 970, also not 1050.

Likely cause: synthesis prose may be using a budget-or-allocated figure rather than the audit-confirmed produced count. The discrepancy does not affect the cost figure (~$60-70 LLM remains correct against the actual labelling output) and does not affect the substantive 3-lever ceiling claim or any of the 3 owner-decision options.

**Remediation (optional, builder-discretion)**: §2.3.3 row "-C-SCALE" change "1050 labels" → "700 labels" to align with audit-trail record. Or add a footnote distinguishing budget-vs-produced if intended. Not blocking; orchestrator can merge as-is and append a one-line correction note in the merge resolution comm if desired.

## Smarter-over-time

This is a **synthesis** PR rather than data/code execution; the audit reduces to consistency checking against the prior PR audit-trail (PR #261 / #265 / #285 / #289 / #293 verdicts) plus dispatch-compliance verification. The class system (#11-#14) carries through cleanly; the 7-item synthesis-audit format is durable for future "closing-phase" PRs of this kind.

The 12.5K closing pattern (5-phase Lever C + 3-lever ceiling claim + architect-hat recommendation + owner-gate hand-off) is the second clean instance of this template — first was the v8 → v9-3way migration ship-gate. Worth noting as a reusable pattern.

## Gates

PR #297 cleared from QC side. **0 BLOCKER, 0 SHOULD_FIX, 1 NIT (non-blocking).**

**HARD OWNER-GATE activates after PR #297 + this verdict merge** per dispatch §"What gates" + per loop directive (stop-loop conditions: explicit owner say-so OR hard owner-gate). Orchestrator HOLDS LOOP at -L QC PASS pending owner ship-vs-defer decision. QC has no further pre-merge work queued; loop continues with idle-tick heartbeat refresh until owner directs.

## Cycle stats

- 39th solo QC cycle.
- Wall clock: ~14 min.
- LLM cost: $0.

---

**Verdict: PASS · 0/0/1 NIT · synthesis cleared from QC side · HARD OWNER-GATE next.**
