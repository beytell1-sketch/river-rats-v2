---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #222 + PR #224 merged (QC PASS 0/0/0); dispatch 12.5I-MW40-VERIFICATION-A design (Decision 3β); queue 12.5J-D-pre after MW-40-A merge
status: DIRECTIVE — merges done; fires LEAD-PROGRAMMER on MW-40-VERIFICATION-A design (architect hat) — fire now
---

# PR #222 cleared + 12.5I-MW40-VERIFICATION-A design dispatch

QC verdict on PR #222 (`REVIEW_QC_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md` on `qc/pr222-corpus-assemble-review-2026-05-06`, PR #224): **PASS — 0 BLOCKER, 0 SHOULD_FIX, 0 NIT (21st solo cycle).** Independent recomputation of Step-18 features via canonical extractor, activation rates exact match, owner-scope perimeter held. No fix-forward.

Per loop directive: data PR with QC PASS clean → merge after re-checking findings. PR #224 merged at master `4d8fcf8`; PR #222 merged at master `48084c3`. 788-row 61-surface combined corpus is now the canonical training input for 12.5K.

## LEAD-PROGRAMMER — Step 5: 12.5I-MW40-VERIFICATION-A design (fire on this comm merge)

Per `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` § "Decision 3β" + dispatch sequencing table row 5. Architect-hat task; design only — no situation generation, no labelling.

Branch: `programmer/phase125i-mw40-verification-a-design-2026-05-06`. Base: master post-this-comm-merge (`48084c3` + this comm).

### Mini-phase context

MW-40 is 1 of 4 stay-wrong remaining (post-MW-25 graduation). PILOT_787 in 12.5I-C produced Sonnet 3-2 + Opus HIGH CHECK + structural composition argument: J-on-board 4-way checked-through TPMK (T-kicker, IP non-PFA) flips composition from "BET-thin-value-defensible" (no J on board) to "CHECK-mandatory" (J on board → set-of-Js + JJ slowplay + suited-J broadways dominate). Per Decision 3β: 3 sources is meaningful but does not yet meet the slow-quality bar set by MW-25's 4-source + 30-hand parametric pattern. Verification round tests the structural prediction empirically before committing the BATCH2 reference update.

### Design scope — `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (in review/comms/)

Use `PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md` (master `54e2943`+) as structural template. This is a focused mini-phase, not a full T-template family expansion, so the design comm can be ~half the length.

**Per-template scope (single template; ~30 hands):**

- **T11'-MW40-VERIFICATION**: J-on-board 4-way checked-through TPMK on a J-high or J-on-turn board family. ~30 parametric variants. Constraints:
  - **Hero seat / position**: BTN IP non-PFA (matches MW-40 reference)
  - **Action sequence**: 4-way SRP, PFR (UTG/HJ/CO) checks, all 3 OOP players check to BTN on flop → 4-way checked-through to turn (or river — design choice; mirror MW-40's exact street-of-decision)
  - **Hero hand class**: TPMK with T-kicker (J-high or J-turn boards) — pair-of-Js + Tx kicker
  - **Board class**: J-on-board (flop OR turn). Sub-axes:
    - J-high flop (e.g., Js9c5h, Js7d3c, Js8h4d) — ~10 variants
    - J-low flop with J-on-turn (e.g., 9c5d3h → Js, 7c4d2s → Js, 8h6c2d → Js) — ~10 variants
    - J-medium flop with paired-J or set-of-Js in range (e.g., Jh5c2d, Jc8h3s) — ~10 variants
  - **Kicker variation**: T-kicker pinned (TJ); MAY include adjacent-kicker control variants (9-kicker, Q-kicker) IF the design needs to discriminate the T-kicker-specific composition prediction from broader medium-kicker patterns — flag explicitly in design if so
  - **Suit / blocker variation**: vary suits to avoid backdoor-FD bias; vary whether hero holds J-blocker (e.g., Jh as kicker on Jc-board reduces villain JJ combos — design should include both with-blocker and without-blocker variants to test blocker-effect sensitivity per `feedback_solver_findings.md` finding 2)
  - **Predicted v3.4 output (design_action per T-CONTROL)**: CHECK (matches PILOT_787, Opus HIGH, structural prediction). If actual labelling produces ≥27/30 CHECK consensus → MW-40 graduates with 4-source pattern matching MW-25. If <27/30 → structural argument is too narrow; PILOT_787 stays as anomaly; MW-40 stays in stay-wrong.

**Total target: ~30 hands (single template).** Combined corpus post-12.5I-MW40-VERIFICATION (if it ships into corpus): 788 + 30 = 818 hands. **Note:** corpus addition gates on the verification round outcome AND on Decision 3β follow-up (whether to lock the BATCH2 reference); design phase is decoupled from that decision.

### Methodology rules (standing per 12.5H-A / 12.5I-A)

- Cross-seed importance reporting (verify Step-18 features activate as predicted on the new template — both `nut_blocker_overcard_count` (likely 0 for J-on-board since hero K is not the nut blocker on J-high) and `bet_call_multiway_oop_raise_pressure_index` (mostly 0 since hero is IP not OOP); flag any unexpected activations)
- Cap-binding pre-flight (verify factory parametric variants don't collide with existing 788-corpus ref_ids; new ref_id namespace `PILOT_MW40_VERIF_001..030` or similar — pick a clean disjoint range)
- Tier-up verification (Sonnet pilot first per `feedback_pilot_first_for_long_jobs.md`; Opus tier-up on canonical hands during 12.5I-MW40-VERIFICATION-C labelling)
- Pilot-first (5-hand pilot before full 30-hand factory run during 12.5I-MW40-VERIFICATION-B)
- Hero-only convention (only hero hand observed; villain ranges narrowed via PFR-check action sequence)
- Pre-flight join-cardinality (factory-generated count = exactly the planned count; no over-generation, no under-generation)
- design_action per T-CONTROL (CHECK predicted; document the structural reasoning per the PILOT_787 evidence chain)

### Stop conditions

- Design diverges from per-hand Decision 3β scope (MW-40-specific J-on-board only; do not blend in MW-17/45/47 axes) → STOP, route to orchestrator
- Per-template count below 30 hands → STOP (Decision 3β explicitly set 30-hand bar matching MW-25 graduation pattern)
- Solver-as-labels appears → STOP per `feedback_solver_vs_expert_labels.md`
- Factory parametric ranges introduce non-J-on-board boards → STOP (scope discipline)
- design_action prediction differs from CHECK without explicit structural reasoning → STOP (the prediction *is* the verification target)

### What you do NOT do

- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source (read-only reference)
- Do NOT modify BATCH2 reference (orchestrator-scope; locked until verification round completes)
- Do NOT touch existing 788-corpus or any prior-phase corpus files
- Do NOT generate situations (12.5I-MW40-VERIFICATION-B scope; separate dispatch)
- Do NOT label hands (12.5I-MW40-VERIFICATION-C scope; separate dispatch)
- Do NOT run Opus tier-up (12.5I-MW40-VERIFICATION-D scope; separate dispatch)

### Cost / time

~$0 (design only; no LLM calls; document authoring). ~30-45 min builder time including the design comm.

### Deliverable scope

1 file in PR diff: `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`

(Optional supporting analysis files in `review/comms/` if the structural argument benefits from a separate composition-triple breakdown table; keep minimal.)

## QC stream — what you audit (when 12.5I-MW40-VERIFICATION-A PR opens)

Standalone audit pattern, similar to 12.5I-A but adapted for mini-phase scope:

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly 1 file (+ optional analysis files); no drift outside review/comms/. Verify NOT touched: v3.x prompts, BATCH2 reference, river-rats-core/, training-data, existing corpus files.
2. **Per-template count target** — 30 hands planned (matches Decision 3β).
3. **Scope discipline (MW-40-only)** — design does NOT blend MW-17/45/47 axes; J-on-board family only.
4. **Methodology rules present** — all 7 standing rules from 12.5I-A (cross-seed importance, cap-binding pre-flight, tier-up verification plan, pilot-first plan, hero-only convention, pre-flight join-cardinality, design_action per T-CONTROL).
5. **design_action prediction = CHECK** — with structural reasoning citing PILOT_787 + Opus HIGH + composition triple flip.
6. **Sub-axes coverage** — design includes J-high flop / J-low flop with J-turn / paired-J variants (~10 each); blocker-effect variation present.
7. **Stop conditions present** — design comm explicitly lists stop conditions including the <27/30 graduation threshold.

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_A_DESIGN_2026-05-06.md` on `qc/pr<N>-mw40-verification-a-review-2026-05-06`. ~10-15 min audit.

## Why no Opus tier-up on 12.5I-MW40-VERIFICATION-A

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs (Sonnet judgments on poker hands). 12.5I-MW40-VERIFICATION-A is design / planning — no new poker judgments produced (the design predicts CHECK; that's a hypothesis to test, not a labelled output). Standard QC PASS suffices. Opus tier-up will run during 12.5I-MW40-VERIFICATION-D.

## Sequencing — what fires after 12.5I-MW40-VERIFICATION-A merges

Per Decision 3β + `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md` queue:

1. **12.5J-D-pre test-guard deflake dispatch** (Option b: tier-2 Δ-tolerance per `MAIN_TERMINAL_PR205_MW33_RESOLUTION_2026-05-06.md`) — fires on MW-40-A merge (separate dispatch comm). Builder serial; 12.5J-D-pre is engineering scope (test guard), runs cleanly between MW-40-A and MW-40-B without poker-judgment overlap.
2. **12.5I-MW40-VERIFICATION-B situation generation dispatch** — fires on 12.5J-D-pre merge.
3. **12.5I-MW40-VERIFICATION-C labelling round** (5 Sonnet × 30 hands; pilot-first) — fires on B merge.
4. **12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision** — fires on C QC PASS.
5. **12.5I-MW40-VERIFICATION-E**: BATCH2 reference update PR (mirrors MW-25 pattern) IF graduation passes; OR memo-only PR documenting failed verification IF graduation does not pass.

Builder remains single-stream serial. Slower stream sets pace per `feedback_orchestrator_controls_parallel_timing.md`; orchestrator gates each transition.

## What's blocked / what's queued

**Cleared by this comm:**
- PR #222 merge confirmation (788-row corpus locked)
- PR #224 merge confirmation (QC verdict record)
- 12.5I-MW40-VERIFICATION-A design dispatch fires

**Newly queued (after MW-40-A merges):**
- 12.5J-D-pre test-guard deflake dispatch
- 12.5I-MW40-VERIFICATION-B/C/D/E (sequenced)

**Still queued (later):**
- 12.5J-C trainer integration test on 61-surface (pending 12.5J-D-pre)
- 12.5K combined re-train (gates on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship)
- 12.5L gate eval (gates on 12.5K)

## References

- PR #222 (12.5I-D corpus assemble merged): master `48084c3`
- PR #224 (QC PASS 0/0/0 verdict merged): master `4d8fcf8`
- PR #223 (QC trigger that fired this audit): master `6f5e32a`
- PR #221 (orchestrator: PR #218 merge + 12.5I-D dispatch): master `680f51d`
- PR #217 (orchestrator: PR #213 quality-default decisions; Decision 3β source): master `d6912ad`
- PR #213 (12.5I-C labelling, PILOT_787 Sonnet 3-2 source): master `994ae67`
- PR #209 (Opus 4.7 MW-25 re-eval; precedent for Decision 3β verification pattern): master `077c168`
- 12.5I-A design precedent: `review/comms/PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md`
- 12.5I-B/C precedents: `MAIN_TERMINAL_PHASE125I_B_DISPATCH` / `MAIN_TERMINAL_PHASE125I_C_DISPATCH`
- Memory: `feedback_quality_default_no_ask.md` (4-source bar matching MW-25), `feedback_pilot_first_for_long_jobs.md` (Sonnet pilot + Opus tier-up plan), `feedback_orchestrator_decides_not_recommends.md` (orchestrator-scoped sequencing), `feedback_solver_findings.md` finding 2 (blocker-effect sensitivity)

**Status: PR #222 + PR #224 merged. LEAD-PROGRAMMER fires 12.5I-MW40-VERIFICATION-A design (architect hat) on this comm merge. ~30-45 min wall clock to PR open.**
