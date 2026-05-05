---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-A — corpus expansion design (B-then-C step 2); architect hat authors design comm with empirical evidence baked in
status: TRIGGER — fire now
---

# Phase 12.5H-A — corpus expansion design

12.5H-pre merged at master `edd5556`. H-FEAT empirical state crystal:
- **Validated at cross-seed median:** `nut_flush_block` median = 0.0268 (above ml-architect Q4 ≥0.02 floor)
- **Volatile:** per-seed range [0.0000, 0.1406]; 40% of seeds below 0.02 floor; bimodal 60/40 distribution
- **cap-non-binding cross-validated:** cap=3.0 vs cap=4.0 byte-identical at trainer time (orthogonal confirmation of 12.5G's predict-time finding)

Orchestrator decision per `feedback_quality_default_no_ask.md` standing rule + the cross-seed median validation: 12.5H-A scope = E-DIST corpus expansion focus, with seed-volatility caveat documented. Migration's premise stands at median; 12.5H aims to push median + tighten variance.

## LEAD-PROGRAMMER (architect hat) — what you do

Branch: `programmer/phase125h-a-design-2026-05-XX` (XX = your start date)

### Author `review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-XX.md`

This is a design comm. **No code changes; no corpus generation; no labelling.** Just the design document.

The 12.5E-A design (`PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md`, master `bad1396`) is the structural template. 12.5H-A reuses the §-structure and updates per empirical evidence from 12.5C/D/D'/E/G/H-pre.

### Required content

#### §1 — Authority chain (12.5C through 12.5H-pre empirical evidence)

Cite the active authority chain. Reference 12.5E-F synthesis (PR #155) + 12.5G cap-non-binding refutation (PR #157) + 12.5H-pre cross-seed analysis (PR #161). Document that B-then-C compound is the active path; 12.5G was step 1 (cap retune null result); 12.5H is step 2 (corpus expansion).

#### §2 — Empirical diagnosis (refined per 12.5H-pre + 12.5G)

Update the diagnosis section from 12.5E-A with new empirical evidence:

- **H-FEAT validated at cross-seed median (0.0268)**, but volatile (bimodal 60/40; per-seed range [0.0000, 0.1406])
- **cap-non-binding** (cap=3.0 max natural boost is 1.776×; cap=4.0 byte-identical to cap=3.0 in 5/5 seeds). Cap is NOT a lever on this corpus.
- **5 stay-wrong hands** per Opus second-tier evaluation (12.5E-F):
  - 3 pure E-DIST: MW-25 (FD-checked-through 4-way monotone), MW-40 (TP-T-kicker 4-way after PFR check), MW-45 (slowplay-set turn lead 4-way)
  - 1 E-FEATURE primary: MW-17 (NFD+overcards under pot odds + implied/blocker reasoning outside 59-feature surface)
  - 1 compound: MW-47 (NFD+gutshot RAISE OOP)
- **MW-20 newly broken at 12.5E-E**: over-aggression downstream of corpus RAISE-class shift; held-out CHECK recall regressed
- **Seed-volatility hypothesis** (NEW from 12.5H-pre 60/40 bimodal): `nut_flush_block` activation depends on train/test split sensitivity OR warm-start anchor interaction OR booster initialization. Investigate as part of design.

#### §3 — Target situations to add (failure templates, refined per 12.5E empirical)

Per Opus 12.5E-F evaluation specific template families:

- **T8' — monotone-multiway-checked-through (MW-25 family expansion)** — N hands targeting the corpus gap that left MW-25 stay-wrong
- **T9' — PFR-checks-back-Ax-multiway (MW-40 family)** — N hands targeting the MW-40 gap
- **T10' — slowplay-set-turn-lead expansion (MW-45 family)** — adds variation beyond 12.5E T4
- **T7-extension — NFD-CALL implied-odds (MW-17 family)** — addresses E-FEATURE primary residual; may need composition triple variation
- **T-RAISE-stabilize — additional bet+call multiway with villain_air ≥ 0.05** — to tighten the 60/40 bimodal `nut_flush_block` activation; provide more redundant exemplars per pattern so all seeds activate the feature

For each template:
- Composition triple (TP+ / draws / air)
- Board texture family
- Action history canonical
- Hand count (per-template; quality-default sizing per `feedback_quality_default_no_ask.md` — bigger samples preferred)
- Source (situation factory parametric vs manual canonical)
- Predicted v3.4 protocol output (RAISE/CALL/BET/CHECK/FOLD per labelling rule)

#### §4 — Quantity and class distribution

Per Opus second-tier eval recommendation: 50-90 new hands. Slow-quality default = upper bound (90), distributed across templates per E-DIST diagnosis weight.

Specifically:
- T8' (MW-25 family): N hands; MW-25 was 12.5E miss → high priority
- T9' (MW-40 family): N hands
- T10' (MW-45 family): N hands
- T7-ext (MW-17 family): N hands; may also need feature-engineering follow-up
- T-RAISE-stabilize: N hands; aimed at tightening bimodal H-FEAT activation
- Controls: ~20% to detect labeller drift

Class distribution post-merge: 604 + N hands. Predict shifts based on per-template predicted labels.

#### §5 — Sourcing strategy

Two-track per 12.5E-A pattern:
- Track A: situation factory (parametric); reuse `scripts/build_corpus_revision_125e_situations.py` extended for new templates
- Track B: manual canonicals for H-FEAT primary tests (e.g., MW-25 family canonical hand × 1-2; MW-40 family × 1-2)
- NEVER use solver as labels (per `feedback_solver_vs_expert_labels.md`)

#### §6 — Labeller pipeline reuse

Same pipeline as 12.5E-C with:
- v3.4 prompt (`prompts/gto_labeller_v3.4.md`) — locked at master `a598f0a`
- 5 labellers per hand (Sonnet × 5; matches existing 604-corpus methodology)
- Pilot-first per `feedback_pilot_first_for_long_jobs.md`: dispatch labelling round as pilot (manual canonicals + small parametric sample) → gate → full
- Tier-up verification per same memory: orchestrator-side Opus cross-check on contested hands before "labels final"
- Hero-only convention in `prior_actions` (per 12.5E-B amendment)
- Pre-flight join-cardinality gate ≥0.99 (per 12.5D' protocol amendment)

#### §7 — QC gates

G1-G4 per 12.5E design §7 — same gates fire on 12.5H-D corpus QC phase.

Plus NEW G5 (per QC's TC-X-CAP-BINDING-PRE-CHECK): pre-flight check that any cap parameter is binding on the new combined corpus before any future cap-tuning workstream. (12.5H itself doesn't tune cap; this is forward-looking.)

#### §8 — 12.5H workstream phases

- 12.5H-A: design comm (this dispatch's deliverable)
- 12.5H-B: situation generation (LEAD-PROGRAMMER, default hat)
- 12.5H-C: labelling round with pilot+full + Opus tier-up cross-check (per slow-quality)
- 12.5H-D: QC the new corpus (4 gates G1-G4 + new G5 cap-binding pre-flight)
- 12.5H-E: re-train using existing trainer module + cross-seed importance reporting
- 12.5H-F: gate evaluation (median ≥33 to PROMOTE)

Each phase fires on prior phase merge + explicit MAIN_TERMINAL_*_TRIGGER comm (per `feedback_explicit_action_trigger.md`).

#### §9 — Predicted outcome

- Median: 12.5E was 32; predicted 12.5H = 33-35 conservative range (per Opus 50-60% gap-close estimate, revised down from gto-expert's 50-70% by ~10pp due to 12.5E lower-than-predicted marginal yield)
- Cross-seed `nut_flush_block` importance: predict median 0.04-0.06 (above 0.02 floor); 80%+ of seeds above floor (vs current 60%)
- MW-31 / MW-46 distinct-cause hands stay wrong (feature-surface gap; out of Path Y scope)
- T-RAISE-stabilize hands aim to push the 40%-sub-floor seeds above the floor

#### §10 — Methodology lessons baked in

From 12.5E/G/H-pre cycle, these methodology rules are now active and apply to all future trainer + corpus dispatches:
- **Cross-seed importance reporting** (TC-X-CROSS-SEED-IMPORTANCE): report median + std + min/max + % above-floor for any feature-importance claim
- **Cap-binding pre-flight** (TC-X-CAP-BINDING-PRE-CHECK): before cap-tuning, compute mean/min(class_count) vs cap; STOP if cap is non-binding
- **Tier-up verification** on training-data outputs: orchestrator-side Opus cross-check before "labels final"
- **Pilot-first** on all long batches
- **Hero-only convention** in `prior_actions` (matches existing 494 corpus)
- **Pre-flight join-cardinality** ≥0.99 (per 12.5D' amendment)

#### §11 — References

Cite all relevant authority sources at master HEAD.

### Stop conditions

- Design comm grows >700 lines without addressing all 11 sections → STOP, route back
- Any §3 template lacks predicted v3.4 protocol output → STOP, fill in
- Any §4 hand count cited without empirical justification → STOP, justify per slow-quality
- Solver-as-labels appears anywhere in design → STOP per `feedback_solver_vs_expert_labels.md`

### What you do NOT do

- No code changes
- No corpus generation
- No labelling
- No trainer modifications
- No promotion of any model
- DO NOT include feature-engineering scope (out of Path Y; out of 12.5H scope; would be 12.5I or beyond)

## QC stream — what you audit

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when the 12.5H-A design PR opens.

When triggered (3 audits — design-only):

1. **Diff scope** — exactly 1 file (the design comm); analysis-only; no code/corpus/labels/prompt edits
2. **Citation existence** — every file:line in design exists at master HEAD
3. **Methodology incorporation** — verify all six methodology rules from §10 are reflected in the design (cross-seed reporting + cap-binding check + tier-up verification + pilot-first + hero-only + pre-flight join-cardinality)

Post `REVIEW_QC_PHASE125H_A_DESIGN_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER architect hat authors design comm (~500-700 lines)
2. PR opens
3. Orchestrator posts QC audit-now trigger
4. Standalone QC audit
5. On QC APPROVE: orchestrator merges; dispatches 12.5H-B (situation generation)

## What's blocked / what's queued

**Blocked:**
- 12.5H-A PR opens → on builder design comm
- 12.5H-A QC trigger → on PR open
- 12.5H-A merge → on QC APPROVE
- 12.5H-B/C/D/E/F → all downstream of 12.5H-A merge

**Queued:**
- All NIT cleanup items still on the queue
- T1 outcome assessment per PR #144 deferral (MW-25 still wrong; 12.5H targets via T8' family)
- T8 schema gap (encode `design_action` per T8 hand) — incorporate in 12.5H-B factory if convenient
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations) → builder formalizes in `docs/PROCESS_GUIDE.md` opportunistically

## References

- 12.5H-pre merged: master `edd5556` (PR #161)
- 12.5H-pre QC verdict: master `d4e4d77` (PR #163)
- 12.5G refuted cap: master `2135fc8` (PR #157)
- 12.5E-F synthesis: master `16351e1` (PR #155)
- 12.5E-A design (structural template): master `bad1396` (PR #133)
- Opus second-tier evaluation: `review/comms/ORCH_OPUS_125E_F_EVALUATION_2026-05-05.md` (master `16351e1`)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_river_rats_team_structure.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_output_structure_per_party.md`

**Status: 12.5H-A TRIGGER posted. LEAD-PROGRAMMER architect hat authors design comm. After QC APPROVE: 12.5H-B situation generation dispatched.**
