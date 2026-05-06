---
date: 2026-05-06
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #228 — Phase 12.5I-MW40-VERIFICATION-A design (T11'-MW40V; 30 variants; flop SoD; CHECK predicted) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 1 SHOULD_FIX, 2 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR228_2026-05-06.md (master `cec36b4`)
pr_branch: programmer/phase125i-mw40-verification-a-design-2026-05-06 (head `988e39e`)
qc_branch: qc/pr228-mw40-verification-a-review-2026-05-06
---

# PR #228 — pre-merge QC verdict: PASS (0 / 1 SHOULD_FIX / 2 NIT)

22nd solo cycle. Design-only mini-phase milestone (no labelling outputs, no Opus tier-up needed per dispatch §"Why no Opus tier-up"). All 7 trigger items reviewed; 1 methodology-rule divergence flagged for orchestrator ratification, 2 NIT (terminology + stop-condition listing).

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. Per-template count target (≥30 hands) | ✅ PASS |
| 3. Scope discipline (MW-40-only; J-on-board family) | ✅ PASS |
| 4. Methodology rules present (all 7 standing rules) | ⚠️ SHOULD_FIX (rule #4 inverted vs dispatch) |
| 5. design_action prediction = CHECK with structural reasoning | ✅ PASS (NIT-1: terminology) |
| 6. Sub-axes coverage (J-high / J-low+turn / paired-J / blocker) | ✅ PASS |
| 7. Stop conditions present | ✅ PASS (NIT-2: 1 of 5 not in §8 list) |

**Verdict: PASS — no BLOCKER. Orchestrator should ratify or amend SHOULD_FIX before -B fires.** Builder may not auto-fix per `feedback_explicit_action_trigger.md`; orchestrator decides.

## §1 — Diff scope strict

`git diff --stat master...programmer/phase125i-mw40-verification-a-design-2026-05-06`:

```
 review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md | 211 +++++++++++++++++++++
 1 file changed, 211 insertions(+)
```

Exactly 1 file added, 0 deletions, 0 modifications. Scope is even tighter than the trigger's allowance ("expected 1 file (+ optional supporting analysis files)") — single deliverable. **PASS.**

## §7 — Owner-scope discipline (audit item 7 sweep)

Verified PR diff does NOT touch:
- `prompts/` (v3.x prompt files; including `prompts/gto_labeller_v3.4.md`) — 0 changes
- `design/multiway_reference_set/BATCH2_*` (BATCH2 reference) — 0 changes
- `river-rats-core/` (production source) — 0 changes
- `data/` (existing 788-corpus + any prior-phase corpus) — 0 changes
- `training-data/` — 0 changes
- Memory files / `reference_corrections.md` — 0 changes

Owner-scope perimeter held. **PASS.**

## §2 — Per-template count target

Plan §3 + §4 specify exactly **30 parametric variants** (10/10/10 across sub-axes A/B/C) — meets dispatch's "30-hand bar matching MW-25 graduation pattern." Above the BLOCKER threshold. **PASS.**

## §3 — Scope discipline (MW-40-only; J-on-board family)

Plan §3 constraint table locked across all 30 variants:

| Constraint | Plan value | MW-40 reference | Match |
|---|---|---|---|
| `hero_seat` | BTN | BTN | ✅ |
| `hero_position` | IP, closes action | IP closes | ✅ |
| `hero_role` | non-PFA (caller) | non-PFA | ✅ |
| `num_opponents` | 3 (4-way SRP) | 4-way SRP | ✅ |
| `street_of_decision` | FLOP | FLOP | ✅ |
| `villain_check_through_count` | 3 (PFR + 2 callers all check) | matches MW-40 | ✅ |
| `effective_stack` | 200bb | matches MW-40 SPR profile | ✅ |
| `hand_category` | 6 (TP medium kicker) | 6 (per BATCH2_8) | ✅ |
| `kicker_class` | T-kicker pinned (TJ) | matches dispatch trigger §3 | ✅ |
| `is_rainbow` | 1 on flop | matches AJ5r baseline | ✅ |
| `pot_odds` | 0.0 (no bet to call) | matches MW-40 (action sequence is the discriminator) | ✅ |

J-on-board family enforced across all 3 sub-axes (sub-axis A J-high, sub-axis B J-on-turn, sub-axis C J-medium / paired-J). Plan §2 + §9 explicitly fence out: v3.x prompts, BATCH2 reference, `river-rats-core/`, 788-corpus, training-data. **PASS.**

**Informational (not a finding):** Sub-axis B uses hero `TT` or `T9` (TPMK on J-low flop with turn-J) rather than `TJ` (sub-axes A/C). The plan §4 sub-axis B self-explains: "TJ is just T-high or J-high on a J-low flop, not TPMK on flop." This is a logical resolution of the inherent tension in the trigger (which both pinned `TJ` AND specified J-low flop as a sub-axis). Plan §10 R1 offers the orchestrator override (drop sub-axis B → 15/0/15 split) if pure board-J-at-decision-time test is preferred. Acceptable as committed default.

## §4 — Methodology rules present

Trigger §"Audit scope" item 4 enumerates 7 standing methodology rules from 12.5I-A. Cross-checked against dispatch source `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` lines 47-53 to confirm authoritative wording.

| Trigger rule | Dispatch authoritative wording | Plan §6 row | Match |
|---|---|---|---|
| Cross-seed importance reporting | "Cross-seed importance reporting (Step-18 features activation prediction on new template)" | row 7 | ✅ |
| Cap-binding pre-flight | "Cap-binding pre-flight (verify factory parametric variants don't collide with existing 788-corpus ref_ids; new ref_id namespace `PILOT_MW40_VERIF_001..030`)" | post-table paragraph | ✅ |
| Tier-up verification | "Tier-up verification (Sonnet pilot first per `feedback_pilot_first_for_long_jobs.md`; Opus tier-up on canonical hands during -C)" | row 5 | ✅ |
| **Pilot-first** | **"Pilot-first (5-hand pilot before full 30-hand factory run during 12.5I-MW40-VERIFICATION-B)"** | **row 4** | **❌ INVERTED** |
| Hero-only convention | "Hero-only convention (only hero hand observed; villain ranges narrowed via PFR-check action sequence)" | row 1 | ✅ |
| Pre-flight join-cardinality | "Pre-flight join-cardinality (factory-generated count = exactly the planned count; no over-generation, no under-generation)" | row 2 | ✅ |
| design_action per T-CONTROL | "design_action per T-CONTROL (CHECK predicted; document structural reasoning)" | row 3 | ✅ |

### SHOULD_FIX-1: Pilot-first rule inverted vs dispatch (audit item 4)

**Plan §6 row 4** states:

> Pilot-first does NOT apply at 12.5I-B (situation generation is deterministic factory output) → Inherited: 12.5I-MW40-VERIFICATION-B is also deterministic factory; no pilot-first needed at -B

**Dispatch line 50** states (authoritative):

> Pilot-first (5-hand pilot before full 30-hand factory run during 12.5I-MW40-VERIFICATION-B)

**Conflict:** the plan unilaterally inverts the dispatch's methodology rule for -B. Plan rationale ("factory is deterministic — either it works or it doesn't") is defensible poker-pipeline theory but it requires orchestrator ratification per `feedback_explicit_action_trigger.md` and `feedback_orchestrator_decides_not_recommends.md` (orchestrator decides WHAT/WHETHER; expert recommends HOW within the dispatch).

**Why this matters:** without a 5-hand factory pilot at -B, schema mismatches / Step-18 feature regressions / ref_id collisions surface only after all 30 variants are emitted. With a 5-hand pilot, the same checks fire at 1/6 the cost. The dispatch's rule is process-preventative; the plan's inversion accepts the cost-savings tradeoff. Both are reasonable; only orchestrator can ratify the tradeoff.

**Recommended resolution paths (orchestrator decides):**
1. **Ratify** plan's interpretation: orchestrator writes `MAIN_TERMINAL_PR228_AMENDMENT_*` confirming "deterministic factory exempts pilot-first at -B; tier-up + pilot-first remain at -C as planned." Plan stands; PR #228 merges as-is.
2. **Amend** plan: builder dispatched via `MAIN_TERMINAL_*` to author -A2 fix-forward PR adding 5-hand pilot factory pass to plan §6 row 4 + §5 pre-flight checklist before merging -A.
3. **Hybrid**: orchestrator ratifies "no pilot at -B" but adds a `MAIN_TERMINAL_*` standing rule that schema-validation + Step-18 NaN/Inf check fires on first 5 emitted situations during -B as a quasi-pilot; full factory continues only on those 5 passing.

QC has no preference between these — all three resolve the divergence cleanly. Per `feedback_explicit_action_trigger.md`, builder MUST NOT auto-fix; QC has surfaced; orchestrator's next tick decides.

## §5 — design_action prediction = CHECK + structural reasoning

Plan §3 specifies `design_action = CHECK` uniform across all 30 variants. Structural reasoning includes:

- ✅ PILOT_787 evidence chain (Sonnet 3-2 + Opus HIGH per PR #209 + PR #213) — cited explicitly with PR refs
- ✅ Composition flip on J-on-board (set-of-Js + JJ slowplay + suited-J broadways dominate; villain `top_pair_plus_pct` rises) — argued in detail with the four-component composition reasoning
- ✅ 4-way checked-through composition implications — addressed via villain check-through range narrowing argument
- ✅ Solver-as-labels prohibition — explicit anti-pattern note (plan §3 last paragraph)

**PASS** with NIT-1 below.

### NIT-1: terminology — "composition quad" vs "composition triple"

Plan uses "composition quad" (matching v3.4 prompt surface: 4 components — `villain_top_pair_plus_pct`, `villain_medium_made_pct`, `villain_draw_pct`, `villain_air_pct`). Trigger §"Audit scope" item 5 references "composition triple flip." Memory file `feedback_preflop_geometry_vs_postflop_composition.md` describes "TP+/draws/air composition triple."

The discrepancy is between the v3.4 prompt's 4-component model (TP+ / medium_made / draws / air) and the memory note's 3-component model (TP+ / draws / air, collapsing medium_made into the air or TP+ class). Plan §10 R3 self-flags this terminology drift to orchestrator and chooses "composition quad" to match the prompt surface (the actual labelling input).

**Recommended action:** orchestrator considers refreshing memory file `feedback_preflop_geometry_vs_postflop_composition.md` to align with v3.4 prompt's 4-component model OR confirms the 3-component model is the correct frame and the v3.4 prompt should be revisited. Either way, this is a memory-file edit that is owner-scope; QC flags + defers.

Severity: NIT (terminology consistency, not structural). Does not block merge.

## §6 — Sub-axes coverage

Trigger §"Audit scope" item 6 specifies 4 sub-axes:

| Sub-axis | Trigger spec | Plan §4 spec | Count | Match |
|---|---|---|---|---|
| J-high flop (Js9c5h-class) | ~10 | sub-axis A: 10 boards (Js9c5h, Js7d3c, Js8h4d, Js9d2c, Js8c4h, Js7h2d, Js9h3c, Js6d4s, Js9c3d, Js7c5d) | 10 | ✅ |
| J-low flop with J-on-turn (9c5d3h → Js-class) | ~10 | sub-axis B: 10 flops + uniform turn=Js | 10 | ✅ |
| Paired-J or set-of-Js in range (Jh5c2d-class) | ~10 | sub-axis C: 10 boards including JcJh4s as boundary paired-J | 10 | ✅ |
| Blocker-effect variation | with-J-blocker AND without-J-blocker | 5 with / 5 without per sub-axis = 15/15 split across 30 | 15/15 | ✅ |

All 4 sub-axes present. The 1 paired-J variant in sub-axis C (JcJh4s) is the boundary case as the trigger's "Paired-J" label requires. **PASS.**

## §7 — Stop conditions present

Trigger §"Audit scope" item 7 lists 5 expected STOP conditions. Plan §8 lists 5 STOP conditions (4 of which match the trigger's; the 5th differs).

| Trigger stop condition | Plan §8 stop condition | Match |
|---|---|---|
| Per-template count < 30 → STOP | "Per-template count below 30 hands → STOP" | ✅ |
| Solver-as-labels → STOP | "Solver-as-labels appears in the design comm → STOP" | ✅ |
| Non-J-on-board boards → STOP | "Factory parametric ranges introduce non-J-on-board boards → STOP unless documented exception" | ✅ |
| `design_action ≠ CHECK` without explicit reasoning → STOP | "`design_action` prediction differs from CHECK without explicit structural reasoning per §3 → STOP" | ✅ |
| **<27/30 graduation threshold (failure mode that would keep MW-40 in stay-wrong)** | **Not in §8 STOP list — referenced in §10 R4 as downstream consideration** | **⚠️ NIT-2** |

Plus an additional "Design-phase additional stop" in plan §8: "if QC flags sub-axis B as scope-violation … apply the §4 fallback." Net: plan §8 has 5 stop conditions, but the 5th differs from the trigger's 5th.

### NIT-2: 5th stop condition referenced but not in STOP list

Trigger §7 expected the design comm to "explicitly list" all 5 stop conditions. Plan moves the 5th (<27/30 graduation threshold) into §10 R4 as a "risk + open question for orchestrator" rather than a §8 STOP condition.

This is defensible — the threshold is a downstream-phase (-C/-D) gating decision, not a current-phase (-A) STOP. But the trigger's spec asked for explicit listing in the design comm.

Severity: NIT (one stop condition in §10 instead of §8; semantic content present). Does not block merge. Builder may add to §8 in a future amendment if convenient (low-priority fix-forward).

## §"Stop conditions" — design-phase

Per dispatch §"Stop conditions" + plan §8 → all design-phase stops not triggered:
- ❌ Design diverges from MW-40 scope → plan §3 + §9 keep MW-40-only (PASS via §3 above)
- ❌ Per-template count < 30 → 30 exactly (PASS via §2)
- ❌ Solver-as-labels in design comm → explicit prohibition (PASS via §5)
- ❌ Non-J-on-board boards → all 30 are J-on-board family (PASS via §6)
- ❌ design_action ≠ CHECK without reasoning → CHECK uniform with structural argument (PASS via §5)

## Test classes exercised

- TC-23 spec/infrastructure drift (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (3rd formal use after PR #218 + PR #222)
- TC-X-DISPATCH-COMPLIANCE (new informal class — verify plan matches dispatch authoritative wording on methodology rules; this audit's pilot-first finding is the first formal exercise)
- TC-X-METHODOLOGY-RULE-CROSSCHECK (verify plan's methodology table cell-by-cell against dispatch source)

## Smarter-over-time artefact updates

**New incident pattern (proposed, owner-scope to ratify):** "Plan inverts dispatch methodology rule with rationale" → root cause: builder applied poker-pipeline theory ("deterministic factory exempts pilot") to override dispatch text; not a pure execution error. **Test class:** TC-X-DISPATCH-COMPLIANCE — for every design-phase plan, run a dispatch-vs-plan methodology-rule diff before per-item audit. **Curative addition:** if owner ratifies, log to `learning/curative_additions_log.md` and add to `learning/test_class_registry.md`.

QC will hold the curative addition pending owner directive (per project_river_rats_qc.md operating principle: "owner-curated coverage — when QC misses an incident, owner writes one-line directive").

## Audit cost / time

- Wall clock: ~13 min (plan read + dispatch cross-check + memory cross-reference + verdict authoring). Within dispatch estimate (~10-15 min).
- LLM cost: $0 (pure document review + git operations).

## Gates

- **PR #228 merge:** clear from QC side as PASS — but orchestrator should resolve SHOULD_FIX-1 (pilot-first divergence) before -B fires (one of the 3 resolution paths in §4 above). If orchestrator chooses path 1 (ratify plan), merge can proceed immediately.
- **12.5J-D-pre dispatch:** gates on PR #228 merge (no QC-side blocker)
- **12.5I-MW40-VERIFICATION-B situation generation:** gates on 12.5J-D-pre merge AND the SHOULD_FIX-1 resolution path being clear (otherwise -B inherits the methodology divergence)

## References

- 12.5I-MW40-VERIFICATION-A dispatch: `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` (master `f52a93d`, PR #226), authoritative line 50 for pilot-first rule
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR228_2026-05-06.md` (master `cec36b4`)
- Plan under review: `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (PR #228 head `988e39e`)
- Decision 3β source: `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217)
- PILOT_787 evidence: `BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md` (master `994ae67`, PR #213) + Opus tier-up record at PR #209
- BATCH2 MW-40 reference (current state, awaiting verification): `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`
- Memory: `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_preflop_geometry_vs_postflop_composition.md` (terminology drift), `feedback_solver_vs_expert_labels.md`, `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `project_river_rats_qc.md` (owner-curated coverage)

**Status: VERDICT = PASS. PR #228 cleared for merge from QC side, conditional on orchestrator resolving SHOULD_FIX-1 (pilot-first methodology divergence). Two NITs (terminology drift; stop-condition listing) are advisory, do not block. 22nd solo QC cycle.**
