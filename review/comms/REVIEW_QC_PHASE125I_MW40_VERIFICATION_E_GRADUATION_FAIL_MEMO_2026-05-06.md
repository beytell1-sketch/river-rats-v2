---
date: 2026-05-06
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #249 — Phase 12.5I-MW40-VERIFICATION-E graduation-fail memo (4-source pattern; stay-wrong 4→4 unchanged) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR249_2026-05-06.md (master `4b309b7`, PR #250)
pr_branch: programmer/phase125i-mw40-verification-e-memo-2026-05-06 (head `e824829`)
qc_branch: qc/pr249-mw40-verification-e-review-2026-05-06
---

# PR #249 — pre-merge QC verdict: PASS (0/0/0)

27th solo cycle. **MW-40 verification round closure milestone.** Documentation-only milestone — no new labels, no factory output, no model inference (~$0). All 7 trigger items verified clean. NIT-1 / NIT-2 / NIT-3 carry-forward fully folded in. 4-source convergence table mirrors MW-25 graduation pattern symmetrically on the failing direction. BATCH2 BET MEDIUM stands; stay-wrong list 4 → 4 unchanged.

This audit closes the MW-40 verification round (5 phases A → B → C → D → E). Cumulative QC cycles 21–27 covered: PR #222 (788-corpus assemble) → PR #228 (plan) → PR #232 (test-guard deflake) → PR #236 (-B situation gen) → PR #241 (-C pilot HALT) → PR #245 (-D Opus tier-up) → PR #249 (-E memo). 5 PASS verdicts + 2 SHOULD_FIX (1 ratified Path 3 Hybrid, 1 ratified Path 1 J-medium-as-J-low-secondaries).

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. Stay-wrong list integrity (4 unchanged; MW-40 row updated) | ✅ PASS |
| 3. BATCH2 reference label unchanged (BET MEDIUM stands) | ✅ PASS |
| 4. Memory file integrity (Verified Negative Result entry) | ✅ PASS |
| 5. NIT-1 / NIT-2 / NIT-3 carry-forward fold-in | ✅ PASS |
| 6. TC-X-OWNER-SCOPE-DISCIPLINE | ✅ PASS |
| 7. TC-X-DISPATCH-COMPLIANCE (6th formal exercise) | ✅ PASS |

**Verdict: PASS — clear to merge. MW-40 verification round closed cleanly.** No QC-side blocker.

## §1 — Diff scope strict

`git diff --stat master...origin/programmer/phase125i-mw40-verification-e-memo-2026-05-06` (three-dot):

```
 design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md | 2 +
 review/RESTART_PROMPT_V9_3WAY.md | 2 +- (1 line replaced)
 review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md | 161 +++++++++++++++++++++
 3 files changed, 164 insertions(+), 1 deletion(-)
```

Memory file edit (`~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`) lives outside the v2 repo (per design — memory is per-user system state, not v2-tracked); verified via direct read in §4 below.

Verified NOT touched (perimeter sweep):
- `prompts/gto_labeller_v3.4.md` (locked) — 0 changes
- `river-rats-core/` — 0 changes
- `data/corpus_*.jsonl` (788-corpus + prior 12.5I corpora + MW40-VERIF corpora) — 0 changes
- `training-data/`, model files — 0 changes
- `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_*` (merged plan; -E does not amend it) — 0 changes
- Other memory files (only `reference_corrections.md` is in scope per dispatch) — 0 changes

Owner-scope perimeter held. **PASS.**

## §2 — Stay-wrong list integrity

Inspected `review/RESTART_PROMPT_V9_3WAY.md` change (line 97):

| Field | Pre-edit | Post-edit | Spec |
|---|---|---|---|
| Header | "## 4 True Remaining Failures (solver-corrected + 2026-05-06 graduation update)" | unchanged | ✅ count stays 4 |
| MW-17 row | "Under-calling (low equity draw)" | unchanged | ✅ |
| MW-40 row | "graduation candidate; Opus CHECK HIGH on PILOT_787 (PR #213); 12.5I-MW40-VERIFICATION queued" | "BATCH2 BET MEDIUM stands. Verification round complete 2026-05-06 (PR #228 plan / PR #236 corpus / PR #241 Sonnet pilot 25/25 BET / PR #245 Opus 4.7 tier-up 5/5 BET): graduation-fail confirmed via 4-source convergence symmetric to MW-25 graduation pattern. PILOT_787's CHECK is a single-hand anomaly relative to the broader J-on-board TPMK T-kicker 4-way checked-through IP non-PFA pattern. v3.4 DO NOT Rule 11 OOP-only exemption + composition quad routing dominates." | ✅ annotation cites all 4 PRs |
| MW-45 row | "Under-raising" | unchanged | ✅ |
| MW-47 row | "Shared blind spot (nut draw should raise)" | unchanged | ✅ |

MW-40 row preserved (NOT removed; this is graduation-fail not graduation). Annotation cites the full PR chain (#228 / #236 / #241 / #245). MW-17, MW-45, MW-47 untouched. Stay-wrong count 4 → 4 unchanged. **PASS.**

## §3 — BATCH2 reference label unchanged

Inspected `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md` line 42 (the canonical action+confidence table):

```
| MW-40 | spr_interactio | 0.206 | 0.000 | BET | MEDIUM |
```

This is the canonical table row that `reference_evaluator.py` reads. **UNCHANGED** in PR diff. ✅ BET MEDIUM stands.

Inspected `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` MW-40 entry (line 629 region): no changes in PR diff.

Optional BATCH2 footnote was added at lines 729-731 of `BATCH2_8_RANGE_ANALYSIS.md` (commentary section, not the canonical label table):

```markdown
**Verification round footnote (12.5I-MW40-VERIFICATION; 2026-05-06):** PILOT_787 (PR #213) showed Sonnet 3-2 CHECK + Opus HIGH CHECK on this exact reference, suggesting a possible BET → CHECK graduation. A 30-hand parametric verification round (Decision 3β) was run to test whether the J-on-board structural argument generalizes. Result: Sonnet pilot 25/25 BET (PR #241) + Opus 4.7 tier-up 5/5 BET (PR #245) = full multi-source consensus 30/30 BET. **BATCH2 BET MEDIUM stands; graduation-fail confirmed via 4-source convergence symmetric to MW-25 graduation pattern.** PILOT_787 is a single-hand anomaly relative to the broader J-on-board TPMK T-kicker 4-way checked-through IP non-PFA pattern. v3.4 routes via DO NOT Rule 11 OOP-only exemption + composition quad villain_air_pct + villain_checked_back weakness + danger_score=0 → value/protection BET.
```

Footnote is COMMENTARY only; the canonical label table row at line 42 is unchanged. **PASS.**

## §4 — Memory file integrity (direct read)

Inspected `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` directly:

| Check | Result |
|---|---|
| New "Verified Negative Result" entry exists for MW-40 | ✅ Present in dedicated section format |
| 4-source convergence cited (PR #241 Sonnet + PR #245 Opus + protocol-rule chain + PR #209 PILOT_787 reclassified) | ✅ All 4 sources explicitly enumerated |
| Multi-source aggregate 30/30 BET cited | ✅ Stated verbatim |
| Stay-wrong 4 → 4 (UNCHANGED) annotated | ✅ Listed in MW-40 details bullets |
| Decision 3β graduation threshold cited (NIT-2 fold-in) | ✅ "≥27/30 CHECK consensus; observed 0/30 effective" |
| Existing MW-25 entry (graduated CHECK HIGH per PR #218) | ✅ untouched (separate section above; not modified by -E) |
| Existing solver-corrected section | ✅ untouched |
| File integrity (no duplicate entries, no orphan sections) | ✅ Clean structure |

The memory addition takes a "Verified Negative Result" framing that complements the existing "Solver-Corrected Reference Labels" section + "Unverified But Likely Corrections" section + "Impact on Scoring" + "How to Apply" sections. Sectioning is coherent.

**PASS.**

## §5 — NIT-1 / NIT-2 / NIT-3 carry-forward fold-in

Builder report §"NIT-1 / NIT-2 / NIT-3 carry-forward fold-in" (lines 60-78) addresses each NIT explicitly:

### NIT-1 (terminology drift)

> The v3.4 prompt surface uses "composition quad" (4 features...). The memory note `feedback_preflop_geometry_vs_postflop_composition.md` uses "composition triple"... Throughout this -E memo and the appended `reference_corrections.md` entry, **"composition quad"** is used as the canonical project terminology (matches the v3.4 prompt surface, which is the protocol the labellers actually apply).

Builder report §"What I did NOT do" line 124 explicitly notes: "Did NOT refresh the memory note `feedback_preflop_geometry_vs_postflop_composition.md` for NIT-1 (owner-scope)". Correct disposition — memory note refresh stays owner-scope per `feedback_orchestrator_decides_not_recommends.md`. **PASS.**

### NIT-2 (5th stop condition placement)

> The plan §10 R4 placed the threshold (≥27/30 CHECK consensus → MW-40 graduates; <27/30 → graduation-fail) as an "open question for orchestrator" rather than a §8 STOP condition. In this -E memo, the threshold is **elevated to the top-level outcome reference**...

Threshold cited in 3 places (§"Decision 3β outcome" of orchestrator's PR #248 + this memo's §"4-source convergence table" + `reference_corrections.md` entry). NIT-2 is operationally satisfied: the threshold has its first formal application as the outcome criterion. **PASS.**

### NIT-3 (plan-internal-consistency cross-check)

> Future verification-round design comms should run a contradiction-cross-check between (a) hand-class spec, (b) intra-sub-axis distribution rules, and (c) literal vs informal terminology BEFORE merge. This is the motivating evidence for both `TC-X-INTRA-PLAN-CONSISTENCY` (informal class; curative entry #13; QC stream) and `TC-X-DISPATCH-COMPLIANCE` (informal class; 5 successful exercises now: PR #228 + PR #232 + PR #236 + PR #241 + PR #245).

Builder report explicitly attributes the QC curative classes (entries #13 and #12 from `~/river-rats-qc/learning/curative_additions_log.md`) and lists their motivating evidence + 5 successful exercises. Owner-ratification surfaced as queued action. **PASS.**

## §6 — TC-X-OWNER-SCOPE-DISCIPLINE

(Verified in §1 above; restating for completeness.)

- 0 v3.x prompt edits
- 0 `river-rats-core/` source edits
- 0 corpus / training-data edits
- 0 plan-comm edits (PR #228 plan unchanged)
- Memory edit IS in scope per dispatch (mirrors PR #218 graduation pattern symmetrically)
- BATCH2 footnote IS in scope per dispatch §"Files to edit" item 3 (commentary, not canonical label change)

**PASS.**

## §7 — TC-X-DISPATCH-COMPLIANCE (6th formal exercise)

| Compliance check | Spec | Observation | Match |
|---|---|---|---|
| Memo-only; no new labels | dispatch §"Memo-only PR" | 0 new label rows added; only commentary | ✅ |
| No factory output | dispatch §"What you do NOT do" | No new corpus rows | ✅ |
| No model inference | dispatch §"Cost / time" ($0) | 0 LLM calls | ✅ |
| 4-source convergence table format mirrors MW-25 graduation symmetrically | dispatch §"4-source convergence table" | builder report §"4-source convergence table" lines 26-32 mirror PR #218 + memory `reference_corrections.md` MW-25 graduation pattern in symmetric direction | ✅ |
| Stay-wrong COUNT unchanged (4) | dispatch + plan | header still "4 True Remaining Failures" | ✅ |
| BATCH2 canonical label unchanged | dispatch | line 42 "BET MEDIUM" stands | ✅ |
| References cite full PR chain | dispatch §"References" | builder report cites PR #209 / #213 / #217 / #228 / #236 / #237 / #240 / #241 / #243 / #244 / #245 / #247 / #248 | ✅ |

Per `feedback_listen_to_orchestrator_always.md` + `feedback_explicit_action_trigger.md`: builder discipline matches dispatch authoritative wording. **PASS.**

TC-X-DISPATCH-COMPLIANCE class continues to validate as durable on 6th formal exercise. The class has now passed 5 clean exercises (PR #232 / #236 / #241 / #245 / #249) plus 1 surfacing exercise (PR #228 SHOULD_FIX-1 that originated the class).

## Test classes exercised

- TC-23 spec/infrastructure drift (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (8th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (6th formal exercise; clean PASS — class is highly durable)**
- TC-X-INTRA-PLAN-CONSISTENCY (informal continuation; explicitly attributed in builder report §"NIT-3")
- TC-X-DISPATCH-PREDICTION-VERIFICATION (entry #11; this PR closes the verification arc the class was designed to close — "did the dispatch prediction hold? — empirically falsified, multi-source confirmed")

## Smarter-over-time observations

**Verification round closure summary** — this audit closes a 7-PR / 5-phase arc (A → B → C → D → E) that exercised the curative class system extensively:

| PR | Phase | Audit verdict | Class activations |
|---|---|---|---|
| PR #228 | -A design plan | PASS+1 SHOULD_FIX+2 NIT | Originated TC-X-DISPATCH-COMPLIANCE (entry #12) via SHOULD_FIX-1 surfacing |
| PR #232 | 12.5J-D-pre (test-guard deflake; parallel to verification round) | PASS 0/0/0 | TC-X-DISPATCH-COMPLIANCE 1st clean validation |
| PR #236 | -B situation gen (Path γ' amended) | PASS+1 SHOULD_FIX+0 NIT | TC-X-INTRA-PLAN-CONSISTENCY (entry #13) 1st informal activation surfaced SHOULD_FIX-1 |
| PR #241 | -C pilot HALT | PASS 0/0/0 | TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE (entry #14) 1st informal activation; TC-X-DISPATCH-PREDICTION-VERIFICATION 2nd exercise |
| PR #245 | -D Opus tier-up | PASS 0/0/0 | TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE 2nd exercise (Opus side; class durable across model classes); TC-X-DISPATCH-PREDICTION-VERIFICATION 3rd exercise |
| PR #249 | -E memo (this PR) | PASS 0/0/0 | TC-X-DISPATCH-COMPLIANCE 6th formal exercise; closes verification arc |

3 informal classes accumulated through this single feature cycle (#12, #13, #14) all validated through repeated activation. The MW-40 verification cycle has been a particularly fertile test bed for the curative class system; the class family is robust enough to formalize at owner discretion.

**The QC → orchestrator → builder feedback loop has consistently closed within 1-2 PR cycles throughout this arc.** Builder citations of QC curative classes (entries #12, #13 explicitly in PR #249 builder report §"NIT-3") demonstrate the class system is influencing builder design discipline, not just QC audit verdicts.

## Audit cost / time

- Wall clock: ~12 min (memory file direct read + diff inspection + builder report cross-check + 7-item verification + verdict authoring). Within 10-15 min estimate.
- LLM cost: $0 (mechanical inspection + git operations).

## Gates

PR #249 cleared from QC side. Per dispatch §"What gates on this audit":

- **MW-40 verification round closed** with this PR's merge.
- 12.5J-C trainer integration test on 61-surface dispatch — gates on PR #249 merge (next builder serial step; engineering scope; routine code/spec PR per `feedback_qc_required_before_approval.md` SCOPED RULE → post-merge TC-25 only)
- 12.5K combined re-train design — gates on -E + 12.5J-E ship

No QC-side blocker.

## References

- 12.5I-MW40-VERIFICATION-E dispatch: `MAIN_TERMINAL_PR245_RESOLUTION_AND_MW40E_DISPATCH_2026-05-06.md` (master `92e2d85`, PR #248)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR249_2026-05-06.md` (master `4b309b7`, PR #250)
- Builder report: `BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md` (in PR #249)
- PR #218 (BATCH2 MW-25 graduation update; precedent for -E pattern, opposite direction): master `e01b296`
- PR #245 (Builder -D Opus tier-up; 5/5 BET): master `877555a`
- PR #241 (Builder -C pilot HALT 25/25 BET): master `d411cb8`
- PR #236 (Builder -B situation gen Path γ'): master `a20b495`
- PR #228 (-A plan): master `e0e0304`
- PR #213 (PILOT_787 Sonnet 3-2 CHECK; the source anomaly): master `994ae67`
- PR #209 (Opus 4.7 PILOT_787 HIGH CHECK; the precedent for tier-up + the anomaly): master `077c168`
- Memory: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (Verified Negative Result MW-40 entry; direct read confirms)
- Curative log: `~/river-rats-qc/learning/curative_additions_log.md` entries #11 / #12 / #13 / #14 (cited by builder report §"NIT-3" for class attribution)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `feedback_listen_to_orchestrator_always.md`

**Status: VERDICT = PASS. PR #249 cleared for merge from QC side. MW-40 verification round (5 phases A→B→C→D→E) closes cleanly. 27th solo QC cycle. 3 informal curative classes (#12, #13, #14) validated through the full arc; 6th TC-X-DISPATCH-COMPLIANCE clean exercise here.**
