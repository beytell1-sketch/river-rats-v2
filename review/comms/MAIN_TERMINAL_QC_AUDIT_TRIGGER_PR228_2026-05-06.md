---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #228 — 12.5I-MW40-VERIFICATION-A design (architect-hat; T11'-MW40V; 30 variants; flop SoD; CHECK predicted) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #228

PR #228: `programmer/phase125i-mw40-verification-a-design-2026-05-06`. Design comm: `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` (master `f52a93d`, PR #226).

Mini-phase scope: design only — no situation generation, no labelling. Tests Decision 3β structural prediction (J-on-board 4-way checked-through TPMK T-kicker → CHECK) before committing the BATCH2 MW-40 reference update.

## Audit scope (7 items per dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected 1 file (+ optional supporting analysis files in `review/comms/` if structural argument benefits from a separate composition-triple breakdown):
   - `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`
   
   Verify NOT touched: v3.x prompts (`prompts/gto_labeller_v3.4.md`), BATCH2 reference (`design/multiway_reference_set/BATCH2_*`), `river-rats-core/` source, training-data, existing 788-corpus or any prior-phase corpus files, memory files / `reference_corrections.md`.

2. **Per-template count target** — 30 hands planned (matches Decision 3β explicit 30-hand bar matching MW-25 graduation pattern). Below 30 → BLOCKER.

3. **Scope discipline (MW-40-only)** — design must NOT blend MW-17/45/47 axes; J-on-board family only. Hero seat = BTN IP non-PFA (matches MW-40 reference). Action sequence = 4-way SRP, PFR check, all 3 OOP players check to BTN on flop → 4-way checked-through. Hand class = TPMK with T-kicker (TJ).

4. **Methodology rules present** — all 7 standing rules from 12.5I-A:
   - Cross-seed importance reporting (Step-18 features activation prediction on new template)
   - Cap-binding pre-flight (factory parametric variants don't collide with existing 788-corpus ref_ids; new disjoint ref_id namespace)
   - Tier-up verification plan (Sonnet pilot first; Opus tier-up on canonicals during 12.5I-MW40-VERIFICATION-C)
   - Pilot-first plan (5-hand pilot before full 30-hand factory run during 12.5I-MW40-VERIFICATION-B)
   - Hero-only convention (only hero hand observed)
   - Pre-flight join-cardinality (factory-generated count = exactly 30; no over/under-generation)
   - design_action per T-CONTROL (CHECK predicted; document structural reasoning)

5. **design_action prediction = CHECK** — with explicit structural reasoning citing:
   - PILOT_787 evidence chain (Sonnet 3-2 + Opus HIGH per PR #209 + PR #213)
   - Composition-triple flip on J-on-board (set-of-Js + JJ slowplay + suited-J broadways dominate)
   - 4-way checked-through composition implications (vs HU)

6. **Sub-axes coverage** — design includes (per dispatch §"Per-template scope"):
   - J-high flop variants (Js9c5h-class) — ~10
   - J-low flop with J-on-turn variants (9c5d3h → Js-class) — ~10
   - Paired-J or set-of-Js in range variants (Jh5c2d-class) — ~10
   - Blocker-effect variation (with-J-blocker AND without-J-blocker per `feedback_solver_findings.md` finding 2)

7. **Stop conditions present** — design comm explicitly lists:
   - Per-template count < 30 → STOP
   - Solver-as-labels → STOP
   - Non-J-on-board boards → STOP
   - design_action ≠ CHECK without explicit structural reasoning → STOP
   - <27/30 graduation threshold (failure mode that would keep MW-40 in stay-wrong)

## QC routing

Standalone stream (`~/river-rats-qc/`) per `feedback_qc_routing_when_standalone_active.md`. Pre-merge audit (mini-phase design milestone). Expected duration: ~10-15 min (single-file design comm; medium scope).

## Output

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_A_DESIGN_2026-05-06.md` on `qc/pr228-mw40-verification-a-review-2026-05-06`. PR opens. Verdict: PASS / ISSUES FOUND / FAIL.

## What gates on this audit

- PR #228 merge → on QC PASS (no Opus tier-up needed; design phase — no labelling outputs per `feedback_pilot_first_for_long_jobs.md` sub-rule)
- 12.5J-D-pre test-guard deflake dispatch → on PR #228 merge (next builder serial step)
- 12.5I-MW40-VERIFICATION-B situation generation dispatch → on 12.5J-D-pre merge
- 12.5I-MW40-VERIFICATION-C labelling round → on B merge
- 12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision → on C QC PASS
- 12.5I-MW40-VERIFICATION-E BATCH2 reference update OR memo PR → on D outcome

## What you do NOT do

- Do NOT make GTO judgments on whether CHECK is the right design_action (that is the verification target; QC verifies the *design integrity*, not the GTO truth — solver and Sonnet+Opus consensus during 12.5I-MW40-VERIFICATION-C/D will produce the empirical answer)
- Do NOT modify any file (review-only)
- Do NOT recommend further design changes outside the 7-item audit scope (orchestrator-scope; surface to orchestrator if design has structural integrity issues outside the audit checklist)
- Do NOT run training or inference

## References

- 12.5I-MW40-VERIFICATION-A dispatch: `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` (master `f52a93d`, PR #226)
- Decision 3β source: `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217)
- PILOT_787 evidence chain: PR #209 (Opus 4.7 MW-40 HIGH; master `077c168`) + PR #213 (Sonnet 3-2; master `994ae67`)
- 12.5I-A design precedent: `review/comms/PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md`
- BATCH2 MW-40 (current reference, awaiting verification): `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `feedback_solver_findings.md` finding 2 (blocker-effect sensitivity)

**Status: QC stream — fire now on PR #228. Standalone audit, pre-merge, 7-item scope. ~10-15 min.**
