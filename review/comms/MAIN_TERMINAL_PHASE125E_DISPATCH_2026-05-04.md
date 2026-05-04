---
date: 2026-05-04
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · ML-ARCHITECT (advisory) · GTO-EXPERT (review of 14 manual canonicals)
re: Phase 12.5E — corpus expansion per Direction Data-fix; ml-architect design adopted; 12.5E-B situation generation dispatched
status: DIRECTIVE — owner picked Data-fix; design + dispatch landing together
---

# Phase 12.5E — corpus expansion (Data-fix)

Owner picked Data-fix at the 12.5D' synthesis owner gate. Slow-quality path per standing instruction (`feedback_quality_default_no_ask.md`, reinforced 2026-05-04).

ml-architect's 12.5E-A design comm is `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` — landing in this PR alongside this dispatch directive. Design is **adopted in full**. Highlights (per ml-architect's quality-default in-design decisions):

- **110 new hands**, not 100 (extra 10 distributed across T5 NFD+gutshot RAISE OOP and T4 slowplay-set-turn-lead — H-FEAT primary tests)
- **5 expert labellers per hand**, not 3 (multi-expert convergence pattern; tighter consensus)
- **14 manual canonical hands** + 96 situation-factory parametric hands (two-track sourcing)
- **4 QC gates** (G1 join-cardinality, G2 distribution sanity, G3 dedup vs 494, G4 labeller drift on T8 controls)
- **8 templates** covering MW-25/40/42/45/47/17 failure families + monster-delayed-aggression reinforcement + control hands
- Post-12.5E corpus = 604 hands; **RAISE class doubles 5.9% → 10.1%** (the single most important distributional shift)
- Predicted outcome: blocker importance 0.0000 → ≥0.02; median seed solver-corrected 35-37 (range, not point estimate)

This dispatch authorizes 12.5E-B (situation generation) immediately. 12.5E-C/D/E/F sequence as design specifies, each gated on the prior phase landing on master.

## Why this skips a separate "owner gate on the design"

Per `feedback_quality_default_no_ask.md` (reinforced 2026-05-04 owner statement: *"i have time, slow quality approach. please remember this, this is always the direction. please stop asking and always recommend the slow quality approach"*): orchestrator does NOT bring quality-default design decisions to owner for confirmation. The design is the slow-quality path; orchestrator approves and dispatches; owner sees merged on master and can redirect on read.

If owner has any redirect on the design or this dispatch, post a comm and orchestrator amends.

## 12.5E-B — LEAD-PROGRAMMER (situation generation)

Branch: `programmer/phase125e-b-situation-generation-2026-05-XX` (XX = your start date)

### Authority chain (highest to lowest precedence)

1. This dispatch directive (operational scope, sequencing, stop conditions)
2. ml-architect 12.5E-A design comm (`PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md`) — verbatim implementation target for §3 templates + §5 sourcing + §6.4 join-cardinality gate + §7 QC gates
3. Existing corpus-generation pipeline (`scripts/build_corpus_revision_500_hand.py` per `BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md` if exists; verify on pre-flight)
4. Existing labeller pipeline (`dispatch_mass_labelling.py`, `collect_mass_labels.py`) — reused unchanged for 12.5E-C
5. CLAUDE.md §6 (sacred core) + §6 addendum

### Deliverable for 12.5E-B (this phase)

Three new files + 1 NEW comm:

1. **`scripts/build_corpus_revision_125e_situations.py`** — situation generator implementing §3 templates T1-T8 + §5 two-track sourcing
2. **`data/corpus_revision_125e_situations_2026-05-XX.jsonl`** — 96 parametric situations (T1-T7 factory output) at design-spec count (12+10+10+12+12+8+10+22 minus 14 manuals = effectively the parametric-track output)
3. **`data/corpus_revision_125e_manual_canonicals_2026-05-XX.jsonl`** — 14 manual canonical hand designs (per §5.1 Track B); these go to GTO-EXPERT review before labelling
4. **`review/comms/BUILDER_REPORT_PHASE125E_B_SITUATION_GENERATION_2026-05-XX.md`** — report with G1-G3 self-checks (no labels yet; G4 fires at 12.5E-D)

### NOT included in 12.5E-B (later phases)

- Labels (12.5E-C produces these via existing labeller pipeline)
- QC gate on labels (12.5E-D)
- Re-train (12.5E-E reuses 12.5C trainer module on master; no code changes expected)
- Reference-set gate (12.5E-F)

### Sequencing for 12.5E-B (slow-quality path explicit)

Per design §8.B and `feedback_quality_default_no_ask.md`:

1. **Pre-flight grounding (mandatory before code).** Read design §3 (all 8 templates). Read existing corpus pipeline scripts. Read corpus_revision_500_hand_2026-04-27.jsonl row 1 + 100 + 200 + 400 + 493 to internalize schema. Identify any drift between design's cited file:lines and current master HEAD. STOP if drift >0.99 cardinality on any cited reference (per protocol amendment).
2. **Implement situation generator** — one template at a time, with intermediate verification (each template emits 12-12-10-12-12-8-10 = 76 parametric situations + 36 controls = 112 candidates pre-dedup; design target after T8 = 96 parametric + 14 manual = 110 total). After each template, run a small dry-run (5 situations) and verify shape against design §3 spec.
3. **Author 14 manual canonical hands** — design §5.1 Track B specifies these are GTO-correctness-load-bearing for the H-FEAT primary test (T5 NFD+gutshot RAISE OOP, T4 slowplay-set, T7 NFD+overcards-with-blocker). Manual designs go to a separate JSONL for GTO-EXPERT review. Do NOT skip the manual track to save time.
4. **G1-G3 self-checks** per design §7:
   - G1 (join-cardinality): empirically verify `pilot_hand_id` cardinality on the new 110 rows (must be 110/110 unique, no collisions with the 494 existing rows)
   - G2 (distribution): verify class targets 12+10+10+12+12+8+10+22 hold within ±1 hand per template
   - G3 (duplicate detection): verify zero exact-board+hero-hand+action-history duplicates vs the 494 existing rows
5. **Author the 12.5E-B builder report** documenting the generation run + G1-G3 results
6. **Open 12.5E-B PR** with the 4 files (3 data + 1 comm); PR title `Builder Phase 12.5E-B: situation generation (110 hands across 8 templates)`; PR body ≤15 lines linking design comm + this dispatch

### Stop conditions for 12.5E-B

- Pre-flight finds drift in cited file:lines → STOP, report
- Any template's situation generator produces fewer than the design's 12-10-10-12-12-8-10-22 spec count → STOP, report (don't backfill from a different template)
- G1 cardinality check fails (any pilot_hand_id collision with existing 494) → STOP, regenerate with new IDs
- G2 distribution check fails (any class >±1 hand off target) → STOP, fix the generator
- G3 duplicate detection finds any exact-board+hero+action-history match against existing 494 → STOP, replace the duplicate with a fresh parametric variant
- Any solver call that would produce a label → STOP (design §5.2 forbids; solver is verify-after only)
- 14 manual canonicals drift from design §3 specifics → STOP, route to GTO-EXPERT for re-spec

### What you do NOT do in 12.5E-B

- Do NOT label any situations (12.5E-C is the labelling phase)
- Do NOT run the existing labeller pipeline (kept unchanged for 12.5E-C)
- Do NOT touch the 494 existing corpus rows (they're locked; expansion is additive only)
- Do NOT touch trainer module on master (12.5E-E reuses unchanged)
- Do NOT mutate `BATCH2_8_HAND_DESIGNS.md` reference set (kept canonical)

## QC stream

**QC pre-merge audit FIRES on the 12.5E-B PR.** Per dispatch protocol amendment + `feedback_qc_routing_when_standalone_active.md`: standalone QC stream is the primary channel. Orchestrator will NOT spawn parallel general-purpose subagent for the same audit.

12.5E-B QC checks (4 audits, NEW vs prior phases):

1. **Diff scope** — exactly 4 new files; no edits to existing source surfaces or existing data files
2. **Citation existence** — every file:line citation in the situation generator + builder report exists at master HEAD at audit time
3. **Distribution sanity** — verify 110 hands match design §3 template counts (12+10+10+12+12+8+10+22) within ±1 hand per template
4. **NEW: Join-cardinality** — `pilot_hand_id` count on 110 new rows = 110 (no collisions); zero overlap with existing 494 rows' `pilot_hand_id` set

QC stream additionally lands a **TC-15-corpus-expansion sub-vector** observation on the audit (this is a new audit pattern; record it for future corpus-expansion rounds).

Post `REVIEW_QC_PHASE125E_B_SITUATION_GENERATION_*.md`. APPROVE or HOLD.

## ML-ARCHITECT (advisory)

The 12.5E-B PR will surface:
- Actual situation distribution per template (vs design target)
- Generator dry-run logs
- Any deviations from design §3 specifics

If situation generator produces parametric situations that don't match the H-FEAT primary test design (e.g., T5 NFD+gutshot RAISE OOP situations all happen to have flush-blocker draws so the booster can't discriminate), recommend a template-specific spec amendment for 12.5E-B' (re-do the affected template).

No gate vote required at 12.5E-B PR. 12.5E-D QC + 12.5E-F gate are your subsequent decision points.

## GTO-EXPERT (review of 14 manual canonicals)

The 14 manual canonical hands (design §5.1 Track B) go to GTO-EXPERT review **before** the labelling round (12.5E-C). For each manual hand, verify:

1. Composition triple (TP+/draws/air) matches the design spec for the template family
2. Board texture is canonical for the failure pattern (e.g., MW-47 family hands have a two-tone board with a nut-flush-draw being the load-bearing feature)
3. Action history is plausible (no "this would never happen at the table" sequences)
4. Position and SPR are consistent with the GTO RAISE/BET reasoning the hand is meant to capture

Post `REVIEW_GTO_EXPERT_PHASE125E_B_MANUAL_CANONICALS_*.md`. If any of the 14 hands needs revision, builder amends in the same PR before the labelling round.

This review fires AFTER builder posts the 14-hand JSONL but BEFORE 12.5E-C dispatch. Builder waits on GTO-EXPERT before requesting 12.5E-C dispatch.

## After 12.5E-B PR opens

1. Standalone QC pre-merge audit fires
2. ML-ARCHITECT advisory read (no gate vote)
3. GTO-EXPERT reviews the 14 manual canonicals
4. On all clear: orchestrator merges 12.5E-B PR; dispatches 12.5E-C (labelling round) per design §8.C — branch `programmer/phase125e-c-labelling-2026-05-XX`, reuse existing `dispatch_mass_labelling.py`, 5 sonnet labellers per hand, $120 hard cap

## Methodology lesson now active

Per design §10.1 + 12.5D' synthesis: held-out gates ≠ reference-set gates on this corpus. 12.5E re-train (12.5E-E) will evaluate BOTH held-out and reference-set; **reference-set is ship-primary**. Trainer report Section E will be expanded with a new "held-out vs reference-set transfer-correlation" diagnostic (per design §10.2). Builder includes that section in the 12.5E-E report.

## What this directive supersedes

Nothing. Pivot directive PR #119 + nudge PR #121 + blueprint PR #122 + dispatch PR #125 + synthesis PR #128 + 12.5D' dispatch PR #130 + 12.5D' synthesis PR #132 + this dispatch are the active authority chain for 12.5E.

## References

- 12.5D' synthesis: `review/comms/MAIN_TERMINAL_PHASE125D_PRIME_SYNTHESIS_OWNER_GATE_2026-05-04.md` (master `5ca1e74`, PR #132)
- 12.5E-A design: `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (this PR)
- 12.5D' dispatch: PR #130 (master `1b95648`)
- 12.5D synthesis: PR #128 (master `d6dd36d`)
- 12.5C blueprint: PR #122 (master `1e4e47e`)
- ml-architect spec: PR #110 (master `291af80`); §11 R-2 risk register reversed by 12.5D' empirical refutation
- ml-architect 12.5D' findings: `/tmp/ml_architect_125d_prime_findings.md` (raw, on orchestrator host)
- gto-expert 12.5D' findings: `/tmp/gto_expert_125d_prime_findings.md` (raw, on orchestrator host)
- Memory: `feedback_quality_default_no_ask.md` (reinforced 2026-05-04), `feedback_qc_routing_when_standalone_active.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_listen_to_orchestrator_always.md`

**Status: 12.5E DISPATCHED. Design adopted in full per slow-quality path. LEAD-PROGRAMMER named author for 12.5E-B (situation generation). Branch `programmer/phase125e-b-situation-generation-2026-05-XX`. 4-file deliverable. 12.5E-C/D/E/F sequence per design §8.**
