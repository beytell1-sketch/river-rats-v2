---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #24 Task 5 Pilot orchestration v1.0 ACK at 4b6c50a — FINAL Wave 2 task; substantial 836-line spec; 5 directive fill-ins + 2 secondary; 3 UNCERTAIN tags documented; 13-prereq PRE-DISPATCH PREREQUISITES; 4 reviewer concerns surfaced; holding merge pending reviewer verdict
status: ACK + HOLD — PR #24 acknowledged; merge awaits reviewer APPROVE; concerns triaged
---

# PR #24 Task 5 Pilot Orchestration v1.0 — ACK

## Headline

PR #24 opened at `4b6c50a` per directive `9093998` (Task 5
greenlight). **FINAL Wave 2 task** of Stage 4 prep — 836 lines
filling the v0.1 DRAFT to v1.0 production spec (40KB).

After PR #24 merges:
- **Stage 4 prep COMPLETE** (5/5 tasks sealed)
- **Pilot dispatch unblocked** pending: Phase 2 HIGH-1 teaching
  fix + HIGH-4 cross-stream + QC pre-pilot sweep + owner greenlight

Substantial milestone. Holding merge pending reviewer verdict per
standing per-batch protocol.

## What's strong about this PR

1. **PRE-DISPATCH PREREQUISITES section near top** with 13 prereqs.
   Mirrors the Stage 5 / Stage 6 / Protocol B/C pattern. Crystal-
   clear what owner needs to confirm before dispatch.

2. **3 UNCERTAIN tags documented:**
   - Anthropic API rate-limit numerical level (no live tier
     dashboard access)
   - Cost ranges $140-$700 (model mix dependent)
   - Per-call latency baseline (no instrumented prior measurements)

   **Each UNCERTAIN tag has a preflight mitigation:** live tier
   check, model selection step, instrumented 5-call validation.
   This is the right way to handle unknowns — surface them
   explicitly + make them testable.

3. **5-way parallelism × 3 sequential batches** (vs 15-way
   concurrent). Reasoning: CCN harness bottleneck + failure
   containment + traceability. ~30-60 min wall-time cost for
   major robustness gain. Cost-aware decision.

4. **Tasks 1-4.5 lessons applied explicitly:**
   - Self-consistency pass
   - Memory + standing-spec alignment (5 specific memory references
     cited)
   - PRE-DISPATCH PREREQUISITES section (parallels prior tasks)
   - Production-grade defensive shielding (whitelist-or-raise
     per Task 4.5 lesson)
   - Numerical/statistical rigour

   This shows the builder is integrating lessons across tasks, not
   treating each as isolated work.

5. **Pilot Orchestrator tool restrictions are whitelist-or-raise**
   per Task 4.5 HIGH-1 lesson. The builder applied the
   `_normalise_street` whitelist-or-raise pattern from Task 4.5 to
   Pilot Orchestrator's tool dispatch. Cross-task discipline
   transfer. Good.

6. **Time estimates narrowed to 10-13h** (from DRAFT's 10-18h)
   with per-phase breakdown. Concrete + falsifiable.

7. **HARD branch check verified pre-commit.** Task 4 incident
   lesson honored.

## 4 Reviewer Concerns Triage

### Concern 1 — 5-vs-15 parallelism Tier-X rate-limit unverified

Reviewer should confirm orchestrator's preflight live-tier check is
operationally adequate.

**Orchestrator triage:** ACCEPTED. The preflight live-tier check is
the right mitigation; reviewer should verify the check actually
runs as the first dispatch step (and is observable in the
orchestrator log). If the check doesn't run, the 5-way parallelism
becomes load-bearing on an unverified assumption.

### Concern 2 — Per-call latency assumption judgement-based

5-call validation preflight gate added but doesn't eliminate Phase
B blow-past risk.

**Orchestrator triage:** ACCEPTED. Mitigation has a tail risk: if
the 5-call sample shows significantly higher latency than ~30-90s,
Phase B's 5-6h estimate balloons. The fix-forward path is
documented (preflight validation gates dispatch); reviewer should
confirm the gate criteria are explicit (e.g. "if 5-call median >
X seconds, halt and recompute estimates").

Suggestion to builder for v1.0.1 if reviewer flags this: add an
explicit gate threshold (e.g. "if 5-call median p95 > 120s, halt
+ recompute"). Otherwise the gate is "soft" and may not actually
block in practice.

### Concern 3 — Highlighter context-scope independence

Feeding aggregate reasoning text gives H1/H2 better signal but
slightly weakens "highlighter independent from labeller reasoning."

**Orchestrator triage:** ACCEPTED but I'd press the builder
slightly here. The locked Stage 4 plan §3 intent was strict
independence between labeller and highlighter framings. Aggregate
reasoning text is *not* per-labeller attribution, so the
independence at the labeller level is preserved — but if the
aggregate reasoning is informative enough to predict the
consensus action, the highlighter is no longer reasoning
independently.

Reviewer should confirm: does the aggregate reasoning provided to
the highlighter let the highlighter "see through" to the consensus
action? If so, the independence claim is weakened. If the
aggregate reasoning is sufficiently abstracted (e.g. composition
buckets, board texture features) that the highlighter still has
to do real reasoning to arrive at the highlight, independence is
preserved.

This is a judgment call; reviewer's framing is the right one.

### Concern 4 — Adjudicator role 1 + role 3 must be DIFFERENT subagents

Reviewer should verify orchestrator's dispatch logic actually
enforces independence.

**Orchestrator triage:** ACCEPTED. This is a load-bearing
correctness property — same-subagent for both roles compromises
the independent-arbitration intent. Reviewer should:
- Read Pilot Orchestrator's dispatch logic for adjudicator
  roles 1 + 3
- Verify the dispatch creates two distinct subagent instances
- Verify there's no shared-context leak (e.g. role 1's reasoning
  reaching role 3's brief)

If the dispatch logic relies on agent IDs or session boundaries,
that's a strong guarantee. If it relies on prompt-only
differentiation, that's weaker (less convergence-prone, but not
immune to context bleed in long-running orchestrators).

## What's pending

1. **Independent reviewer dispatch by builder.** Recommended
   flavour: ml-architect-flavour or general-purpose-with-pilot-
   orchestration-persona. The 4 concerns above need empirical
   verification (especially Concern 4 — dispatch independence).

2. **Reviewer verdict on master** (verdict commit precedes merge).

3. **Orchestrator merge on APPROVE** via atomic bash flow with
   rollback tag.

4. **If APPROVE-WITH-NITS / REQUEST-CHANGES:** fix-forward via
   v1.0.1 of Task 5 per quality default.

## Stage 4 prep progress

```
Task 1 (Protocol B v1.0.1)         ✅ sealed dc6fa1f
Task 2 (Protocol C v1.0.1)         ✅ sealed 435757f
Task 3 (Stage 5 retrain v1.0.1)    ✅ sealed b639776
Task 4 (Stage 6 held-out v1.0.1)   ✅ sealed afc815c
Task 4.2 (v1.0.2 micro-correction) 🟡 APPROVE-WITH-NITS at f43cd49
Task 4.3 (v1.0.3 NIT pass)         ✅ sealed 970017e
Task 4.5 (Logic hardening bundle)  ✅ sealed add2617
Task 5 (Pilot orchestration v1.0)  🟡 ON PR #24 — pending reviewer
HIGH-4 (cross-stream aggregate)    🆕 directive issued at dfa57e3
```

After PR #24 sealed: Stage 4 prep complete; pilot-dispatch gate
remaining items are cross-stream + QC + owner.

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 25 | Task 5 reviewer verdict + sealing | 🔥 ACTIVE — PR #24 pending reviewer | Orchestrator → builder |

(All other HOLDs unchanged.)

## Pilot-dispatch gate progress (after PR #24 sealed will be 7/9)

```
✅ Phase 2 HIGH-2 (game adapter passlist):           SEALED at b944621
✅ Phase 3 HIGH-1/2/3 + Phase 1 HIGH (Task 4.5):     SEALED via PR #21
✅ Task 4.3 v1.0.3 NITs:                             SEALED via PR #22
🟡 Task 5 (Pilot orchestration v1.0):                ON PR #24 (pending reviewer)
⏳ Phase 2 HIGH-1 (teaching renderer translation):    pending teaching
⏳ HIGH-4 (cross-stream aggregate semantics):         awaits builder pickup
⏳ HOLD #21 FEATURE_COLUMNS contract drift:           post-Task-4.5 investigation
⏳ HOLD #24 HIGH-2 indirect propagation:              v1.1 post-pilot
⏳ QC pre-pilot sweep clean (Phase 5):                QC standing roadmap
```

After PR #24 merges: pilot-dispatch gate at 7/9 SEALED. Remaining
critical-path: teaching HIGH-1 + HIGH-4 + QC pre-pilot sweep +
owner greenlight.

## Cross-stream context

- **Teaching at `b75d867`** — held; HIGH-1 directive shipped;
  awaiting builder's renderer translation fix
- **Game at `62fee00`** — Phase B mockup approved; integration
  greenlit; not yet shipped
- **QC stream Phase 4 active** — dynamic /loop; standing re-audits
  queued

## Action

**Builder:**
1. Dispatch reviewer on PR #24 per standing pattern (ml-architect
   or pilot-orchestration persona; verify the 4 concerns)
2. Surface verdict in `review/comms/` when it lands
3. **After PR #24 sealed:** consider HIGH-4 fix (Option B; ~30-60
   min) before pivoting to other queued items (HOLD #21
   FEATURE_COLUMNS investigation can wait)
4. Stage 4 prep wraps after Task 5 + HIGH-4 lands

**Orchestrator (me):**
1. PR #24 ACK shipped (this commit)
2. Hold PR #24 merge pending reviewer verdict
3. On reviewer APPROVE → tag rollback + merge via atomic bash
   flow
4. Loop continues at 15-min cadence
5. Watch for incoming teaching HIGH-1 fix + game Phase B integration

**Owner:**
- FINAL Wave 2 task in flight
- After PR #24 merges + HIGH-4 fix lands + teaching HIGH-1 fix
  lands + QC pre-pilot sweep clean → pilot dispatch gate at owner
- Stage 4 prep ~95% complete (4 sealed + 1 PR-pending of 5 main
  tasks; HIGH-4 is post-Task-5)

## References

- Task 5 directive: `9093998`
  (`MAIN_TERMINAL_PR21_MERGED_TASK5_GREENLIGHT_2026-04-26.md`)
- Pilot orchestration draft: `STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md`
- PR #24 commit: `4b6c50a`
- Stage 4 plan: `ee3d9f5`
  (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`)
- HIGH-4 coordination: `dfa57e3`
  (`MAIN_TERMINAL_HIGH_4_CROSS_STREAM_COORDINATION_2026-04-26.md`)

**Status: PR #24 ACK'd; FINAL Wave 2 task; held pending reviewer
verdict; 4 concerns triaged; standing per-batch protocol.**
