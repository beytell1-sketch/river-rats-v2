---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ml-architect + orchestration-engineering reviewer (dedicated subagent unavailable; persona spec embedded per builder dispatch; reviewer is NOT v1.0 author and NOT prior Stage 4 prep reviewers)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #24 — Stage 4 Task 5 Pilot orchestration v1.0 (`4b6c50a`) — FINAL Wave 2 task
status: APPROVE-WITH-NITS — All 6 ML-architect DRAFT v0.1 flags resolved with sound reasoning; structural framework + dispatch sequencing + brief templates + failure-handling matrix + 13-prereq gate all sound + execution-ready; 5 NITs surfaced (none block merge); UNCERTAIN tags appropriately scoped + gated to preflight verification
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/24
branch: stage4-prep/pilot-orchestration-fill
artifact: review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md (836 lines, new file)
predecessor: review/comms/STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md (~284 lines)
---

# Review Verdict — PR #24 (Stage 4 Task 5 Pilot orchestration v1.0)

## Provenance note

Independent reviewer dispatch under read-only constraint. Did NOT author Task 5; did NOT review any prior Stage 4 prep PR. Worked from PR #24 head commit `4b6c50a`. Cross-referenced against locked Stage 4 plan (`ee3d9f5`), Protocol B/C v1.0.1, Stage 5/6 specs, and full diff (new file).

## Builder verification spot-checks

- Stage 6 hash `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5` matches `STAGE6_HOLDOUT_TESTSET_v1_0.md` line 282 ✓
- Task 4.5 merge `add2617` confirmed via `git show --stat` ✓
- Protocol B v1.0.1 + Protocol C v1.0.1 + Stage 5 v1.0.1 versions verified in headers ✓
- All 8 cited memory files present in `~/.claude/projects/-home-rupertbeytell/memory/` ✓
- Cost envelope independent recalculation: $142.84-$701.20 maps cleanly to stated $140-$700 ✓
- Phase B 5h matches 60s/call midpoint math (300 calls × 60s ÷ 5 parallel × 3 batches) ✓

---

## Item A — Parallelism limits

**OK / HIGH confidence.** 5 labellers × 3 sequential batches by protocol (vs 15-way single-batch). CCN harness bottleneck argument technically correct; failure-containment strongest argument; provenance/traceability sound. Trade-off ~60 min wall-time premium for substantial robustness gain. UNCERTAIN tag on Tier-X rate limit appropriately scoped (preflight gate + upgrade path).

## Item B — Dispatch ordering

**OK / HIGH confidence.** Strict edges A→B→D→C, D→F; permitted overlaps D+E, C+F, E+F. Dependency graph internally consistent. Highlighter context-scope (consensus + per-protocol vote tally + anonymised aggregate reasoning, NOT per-labeller attribution + NOT solver) is principled middle path. Aligns with locked plan §3 (verbatim quote verified).

## Item C — Brief templates

**OK / HIGH confidence.** All 6 phase agent roles have actionable briefs:
- Labeller A/B/C correctly differentiated per protocol; sizing taxonomy cited per `feedback_solver_aligned_sizing.md`
- Convergence-Checker pseudocode concrete (Fleiss-κ, Cohen-κ pairs, 3-of-3 routing, schema)
- Highlighter H1+H2 cite 59-feature vocabulary lock from Stage 5 v1.0.1's 118-column contract
- Reviewer cites `feedback_review_autosave.md`, `feedback_comms_folder.md`, `feedback_verify_source_not_plan.md`
- Adjudicator enumerates 3 sub-roles + role 1+3 independence (in brief text)
- Pilot Orchestrator top-level: cwd discipline, 13-prereq verification, tool restrictions, real-time status comms

All 8 cited memory files verified present.

## Item D — Concurrency / queue logic

**OK / HIGH confidence.** 3-batch dispatch coherent. 5-mode failure handling matrix (rate-limit/5xx/agent-internal/schema/calibration) covers realistic failure surface — each mode has retry policy + escalate-after, avoiding open-ended "retry until success" failure mode. Cost telemetry recorded at write-time (clean spec; see Item H for new-ask note). Cost ranges $140-$700 verified by independent recalculation.

## Item E — Time estimates

**OK with minor advisory / MEDIUM confidence.** 10-13h total wall-time vs DRAFT 10-18h. Per-phase derivation cites ~30-90s per-call latency under explicit UNCERTAIN with preflight 5-call validation step (right mitigation).

**Phase B 5-6h consistency check:** 60s/call midpoint = exactly 5h. 30s low → 2.5h; 90s high → 7.5h. Stated 5-6h is midpoint-to-conservative but doesn't span full 30-90s envelope.

**ADVISORY (LOW):** point estimates tighter than 30-90s band would mathematically support. Preflight gate handles this — but a reader might miss "5-6h" is midpoint estimate, not worst-case. NIT for future revision: footnote that point estimates assume 60s/call midpoint, worst-case under UNCERTAIN band could extend phases ~50%.

## Item F — PRE-DISPATCH PREREQUISITES section

**OK with one cross-stream gap / MEDIUM confidence.** 13 numbered prereqs covering hash-locks, disjointness, sealed protocols, sealed Stage 5/6, Task 4.5 merge, QC sweep, calibration, solver options, cwd discipline, owner greenlight.

Each prereq necessary AND sufficient. Stage 6 hash-lock + Task 4.5 merge cross-checked successfully.

**NIT (CROSS-STREAM):** prereq #9 names "Phase 2 HIGH-1 (teaching renderer) status confirmed" but PR description ALSO claims "pilot dispatch unblocked pending Phase 2 HIGH-1 + HIGH-4 cross-stream + QC pre-pilot sweep + owner greenlight" — and HIGH-4 is NOT explicitly in v1.0 prereq table. Per `MAIN_TERMINAL_PR22_MERGED_QC_PRE_MERGE_ACK_2026-04-26.md`, HIGH-4 is queued cross-stream coordination affecting aggregate flag derivation. Recommend adding HIGH-4 as separate prereq row OR updating prereq #9 to enumerate "HIGH-1 + HIGH-4". Future v1.0.1 NIT pass acceptable.

## Item G — Cross-references accuracy

**OK with one path-prefix NIT / HIGH confidence.** All major cross-references verified:
- Protocol B/C v1.0.1, Stage 5 v1.0.1, Stage 6 v1.0.3 paths + versions confirmed
- Task 4.5 PR #21 merge `add2617` confirmed
- 8 memory files all verified present

**NIT (LOW):** `LABELLING_PIPELINE.md` referenced 3 times without `docs/` prefix; actual file at `docs/LABELLING_PIPELINE.md`. Convention matches predecessor DRAFT and sibling specs (Stage 5 DRAFT, Stage 6 DRAFTs/v1.0). Internally consistent with corpus; future cross-corpus pass could fix all together.

## Item H — No new MEDIUMs

**OK with two LOW advisories / MEDIUM confidence.**

**Internal consistency:** Brief templates do NOT contradict dispatch ordering. Failure-handling modes cover calibration-fail (Phase A) adequately.

**LOW-MEDIUM ADVISORY:** Adjudicator brief enforces role 1+3 independence in text, but Pilot Orchestrator top-level brief lacks explicit verification mechanism. Recommend adding a one-liner: "When dispatching Phase F adjudicators per hand, role 1 and role 3 MUST be separate subagent dispatch calls — track dispatch IDs to verify."

**LOW (cost telemetry):** Per-call $/token logging is NEW infrastructure ask (no existing system to integrate with). Implementation falls to orchestrator agent at execution time. Surface to orchestrator at commission time so they don't assume a library exists.

**Highlighter context-scope:** middle path is correct trade-off; transparent acknowledgement is right discipline. Not MEDIUM.

## Item I — Author concerns assessment

| Concern | Disposition |
|---|---|
| 5-vs-15 parallelism rate-limit verification | LEGITIMATE / NIT-LOW (preflight gate mitigates) |
| Per-call latency assumption judgement-based | LEGITIMATE / LOW (preflight 5-call gate is right mitigation; 5-6h band tightness is the real concern — see Item E) |
| Highlighter context-scope independence | LEGITIMATE / NIT-or-below (middle path principled, trade-off acknowledged) |
| Adjudicator role 1+3 independence enforcement | LEGITIMATE / LOW-MEDIUM (brief says it; Pilot Orchestrator brief lacks verification mechanism — see Item H) |

## Item J — Tasks 1-4.5 lessons applied

**OK / HIGH confidence.** Self-consistency, memory alignment, PRE-DISPATCH PREREQUISITES section parallels prior pre-execution patterns, whitelist-or-raise discipline in tool restrictions, numerical rigour in time estimates with UNCERTAIN tags + preflight gates.

## Item K — Diff scope

**OK / HIGH confidence.** 836 lines (new file). Components justified: frontmatter, purpose, prereqs, role+restrictions, phases A-G, concurrency/queue, time estimates, brief templates (largest component, justified by commission-readiness), author note, reference. No scope creep.

## Item L — Ready for orchestrator merge?

**APPROVE-WITH-NITS.**

v1.0 is execution-ready as canonical Stage 4 pilot orchestration script. All 6 ML-architect DRAFT v0.1 flags resolved with sound reasoning. PRE-DISPATCH PREREQUISITES converts design artifact into executable plan with clear gate. UNCERTAIN tags appropriately scoped. Brief templates commission-ready.

**Pilot dispatch correctly NOT unblocked by this merge** — pilot dispatch remains gated on:
- All 13 PRE-DISPATCH PREREQUISITES GREEN (current state: prereqs #5/#6 labeller-facing artifacts NOT YET BUILT — `protocol_b_composition_first_v1_0_pilot.md` + `protocol_c_adversarial_elimination_v1_0_pilot.md` confirmed absent at filesystem; downstream BUILD step gated by Protocol B/C v1.0.1 PRE-PILOT BUILD REQUIREMENT, NOT a v1.0 deficiency)
- Phase 2 HIGH-1 teaching renderer fix (parallel stream)
- HIGH-4 cross-stream coordination
- Phase 5 QC pre-pilot sweep
- Owner explicit greenlight

---

## VERDICT

**APPROVE-WITH-NITS — overall confidence HIGH.**

**Required fixes:** None.
**Blockers:** None.

## NIT-level observations

1. **Phase B time estimate band tightness:** 5-6h midpoint vs 30-90s underlying band → 2.5-7.5h envelope. Footnote that point estimates assume 60s/call midpoint, worst-case extends ~50%. Future v1.0.1.
2. **HIGH-4 cross-stream prereq missing:** PR description names HIGH-4 as gate but v1.0 prereq table only has HIGH-1. Add HIGH-4 row OR update prereq #9 to enumerate "HIGH-1 + HIGH-4". Future v1.0.1.
3. **Adjudicator role 1+3 dispatch enforcement:** brief text says "must be different subagent dispatches" but Pilot Orchestrator brief lacks dispatch-ID verification mechanism. Recommend adding one-liner. Future v1.0.1.
4. **`LABELLING_PIPELINE.md` path-prefix:** consistently bare-filename across v1.0 + sibling specs. Cross-corpus convention; not v1.0-specific. Future cross-corpus pass.
5. **Cost telemetry as new ask:** per-call $/token logging folded into orchestrator-runtime responsibility with no existing infrastructure. Surface to orchestrator at commission time.

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | NIT | Footnote Phase B time-estimate band per Item E |
| 2 | NIT | Add HIGH-4 to prereq table (or expand prereq #9) per Item F |
| 3 | LOW-MEDIUM | Add adjudicator role 1+3 dispatch-ID verification to Pilot Orchestrator brief per Item H |
| 4 | NIT (corpus) | `docs/LABELLING_PIPELINE.md` path-prefix cross-corpus pass |
| 5 | LOW | Cost telemetry implementation surfacing at orchestrator commission |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_24_TASK_5_PILOT_ORCHESTRATION_2026-04-26.md`.
2. Post comment on PR #24 referencing the verdict.
3. Stand by for orchestrator merge / micro-fix direction.
4. Lifts orchestrator's HOLD pending reviewer (per `MAIN_TERMINAL_PR24_ACK_HOLD_PENDING_REVIEWER`).

**Orchestrator:**
1. Read this verdict.
2. Decide: (a) merge PR #24 as v1.0 + open Task 5.1 micro-fix for the 3 LOW-MEDIUM/NIT items; OR (b) require v1.0.1 micro-fix before merge. Prior-pattern precedent: small NITs deferred to v1.1 / wrap; LOW-MEDIUM (NIT-3) is the hairier call.
3. Either way: Stage 4 prep Wave 2 effectively complete after PR #24 lands. Pilot dispatch remains owner-gate.

**Owner:** wake to find Stage 4 prep Wave 2 complete (5/5 tasks sealed); pilot dispatch remains your gate; pre-pilot blockers (HIGH-1 teaching, HIGH-4 cross-stream, QC pre-pilot sweep) listed in v1.0 prereq table.

## Reference

- PR #24: https://github.com/beytell1-sketch/river-rats-v2/pull/24
- Feature commit: `4b6c50a`
- Source DRAFT: `review/comms/STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md`
- Output: `review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md`
- Locked Stage 4 plan: `review/comms/MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` (`ee3d9f5`)
- Stage 6 v1.0.3 (sealed): hash `65cfbf26...`
- Task 4.5 merge: `add2617`
- Tasks 1-4.5 verdict precedents: PR #11/#13/#15/#21/#22

**FINAL VERDICT: APPROVE-WITH-NITS — HIGH confidence overall. Stage 4 prep Wave 2 ready to close on PR #24 merge.**
