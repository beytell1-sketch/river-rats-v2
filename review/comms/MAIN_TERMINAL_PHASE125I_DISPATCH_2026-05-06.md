---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5I — corpus expansion for MW-25/40/45 (E-DIST underpowered + isomorph-mismatch); parallel with 12.5J (separate dispatch)
status: TRIGGER — fire now
---

# Phase 12.5I — corpus expansion (D path; addresses 3 of 5 stay-wrong)

12.5I-pre diagnostic merged at master `54e2943`. Per-hand verdicts assigned 3 hands to 12.5I (corpus path D):

- **MW-25** (E-DIST underpowered + E-FEATURE secondary): T8' redesign — BET-after-checked-through-multiway hands with `hero-doesnt-have-As-public`; ablating `better_hand_pct` shifts +0.147 toward BET (corpus has near-zero precedent for this pattern)
- **MW-40** (E-DIST underpowered, **closest to flipping** at BET prob 0.305): T9' expansion — 30-40 hands from current 12; the most tractable target
- **MW-45** (isomorph-mismatch + E-DIST secondary): T10' redesign — AKQx-broadway-completed-turn variants specifically; current T10' parametric texture didn't match MW-45's specific board

12.5I runs in **parallel with 12.5J** (feature engineering for MW-17/47; separate dispatch comm `MAIN_TERMINAL_PHASE125J_DISPATCH_2026-05-06.md`). Non-overlapping targets; no coordination overhead.

## LEAD-PROGRAMMER — what you do

This is a multi-phase workstream parallel to 12.5H structure. 12.5I-A through 12.5I-F mirror 12.5H-A through 12.5H-F.

### 12.5I-A — Corpus expansion design (architect hat)

Author `review/comms/PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-XX.md`. Use 12.5H-A (`PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md`) as structural template. Per-template scope:

- **T8'-redesigned** (MW-25 family): 30-40 hands. Constraint: hero NOT holding the on-board top card (avoid the As-public discriminative-axis collapse that broke 12.5H T8'). Heroes draw to non-nut FD on monotone boards. Predicted v3.4 output: BET (per diagnostic — corpus needs to teach BET-after-checked-through-multiway for non-nut-blocker hero spots).
- **T9'-expanded** (MW-40 family): 30-40 hands (up from 12). TP-medium-kicker IP 4-way after PFR check. Same template; just more diverse parametric variants (different boards, different villain ranges, different opener positions).
- **T10'-redesigned** (MW-45 family): 30-40 hands. Constraint: AKQx-broadway-completed turn texture specifically (or equivalent broadway-rich textures where slowplayed set on flop becomes vulnerable on turn). Match MW-45's specific isomorph.

**Total target: 90-120 new hands** (3 templates × 30-40 each). Combined corpus post-12.5I: 694 + 90-120 = 784-814 hands.

Per design §10 methodology rules from 12.5H-A apply standing (cross-seed importance reporting, cap-binding pre-flight, tier-up verification, pilot-first, hero-only convention, pre-flight join-cardinality, design_action per T-CONTROL).

### 12.5I-B/C/D/E/F — same structure as 12.5H-B through 12.5H-F

After 12.5I-A design merges:
- 12.5I-B: situation generation (factory + manual canonicals)
- 12.5I-C: labelling round (Sonnet × 5; pilot-first; orchestrator-side Opus tier-up post-QC)
- 12.5I-D: corpus QC sweep
- 12.5I-E: re-train on combined ~800-hand corpus (parallel with 12.5J-E if 12.5J ships first)
- 12.5I-F: gate evaluation

Each phase fires on prior phase merge + explicit MAIN_TERMINAL_*_TRIGGER comm (per `feedback_explicit_action_trigger.md`).

### Scope discipline

- Path Y still binds — no source surface edits beyond trainer module + tests
- v3.4 prompt unchanged
- 12.5H corpus + labels + manual canonicals locked
- 12.5I corpus is ADDITIVE only (combined corpus = 12.5H + 12.5I)
- 12.5J's feature engineering work (out of Path Y per design) does NOT block 12.5I; both proceed independently until 12.5K combined re-train

### Stop conditions

- Design diverges from per-hand diagnostic spec → STOP, route to orchestrator
- Per-template count below 30 hands → STOP (12.5H demonstrated 12-15 was underpowered)
- Solver-as-labels appears → STOP per `feedback_solver_vs_expert_labels.md`
- Cross-coordination conflict with 12.5J → route to orchestrator (avoid premature integration; 12.5K is the integration phase)

### What you do NOT do

- Do NOT touch existing corpus (12.5H locked)
- Do NOT modify v3.x prompts
- Do NOT modify trainer module
- Do NOT design features (12.5J scope)

## QC stream — what you audit (per phase)

Same audit pattern as 12.5H. Each 12.5I-X PR fires its own QC trigger when builder force-pushes.

## Sequencing

1. LEAD-PROGRAMMER (architect hat) authors 12.5I-A design comm based on diagnostic verdicts
2. 12.5I-A PR opens
3. Orchestrator posts QC audit-now trigger
4. Standalone QC audit
5. On QC APPROVE: 12.5I-B (situation generation) dispatched; 12.5I-C/D/E/F follow

## What's blocked / what's queued

**Blocked:**
- 12.5I-A PR opens → on builder design comm
- Each subsequent 12.5I-X → on prior phase merge

**Parallel (independent of 12.5I):**
- 12.5J workstream (feature engineering for MW-17/47) — separate dispatch comm
- 12.5K combined re-train — fires AFTER both 12.5I-E and 12.5J-E ship

## References

- 12.5I-pre diagnostic: master `54e2943` (PR #193)
- 12.5H-A design (structural template): master `858b032` (PR #165)
- 12.5J dispatch (parallel): `MAIN_TERMINAL_PHASE125J_DISPATCH_2026-05-06.md` (in this PR cycle)
- Memory: `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_river_rats_team_structure.md`, `feedback_solver_vs_expert_labels.md`

**Status: 12.5I TRIGGER posted. LEAD-PROGRAMMER (architect hat) authors 12.5I-A design comm. Parallel with 12.5J. Combined re-train at 12.5K.**
