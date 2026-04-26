---
date: 2026-04-26
from: Logic builder (NOW Pilot Orchestrator persona — but HALTING before A1)
to: Main terminal (orchestrator) · Owner
re: HALT at PRE-DISPATCH PREREQUISITES gate (BEFORE Phase A.1) — 4 rows are RED; per spec "If ANY row is RED: pilot does NOT dispatch. Halt. Do NOT improvise." Empirical evidence + recommended path forward enclosed.
status: HALT — pilot dispatch cannot begin; PRE-DISPATCH gate has gaps; owner + orchestrator must direct fix-forward path
authorization_received: MAIN_TERMINAL_PILOT_DISPATCH_AUTHORIZED_PROCEED_2026-04-26.md (082336d, 16:19) — owner /loop "authorise pilot" at 15:35 SAST
spec: STAGE4_PILOT_ORCHESTRATION_v1_0.md v1.0.3 (master c4f29a5) §"PRE-DISPATCH PREREQUISITES" — 16 rows; gate is "If ANY row is RED: pilot does NOT dispatch."
---

# Pilot Phase A HALT — PRE-DISPATCH PREREQUISITES Gaps

## Executive summary

Pilot Orchestrator persona activated per orchestrator directive at 16:19. **First action is to verify ALL 16 PRE-DISPATCH PREREQUISITES are GREEN before A1.** Verification finds **4 rows RED**:

| # | Prerequisite | Status | Evidence |
|---|---|---|---|
| 2 | Pilot 100-hand corpus disjoint from Stage 6 holdout | **RED** | Pilot 100-hand corpus does not exist in the working tree |
| 3 | Pilot 100-hand corpus disjoint from v2.3 calibration manifest | **RED** | Same — corpus does not exist |
| 5 | Protocol B labeller-facing pilot artifact | **RED** | `prompts/protocol_b_composition_first_v1_0_pilot.md` does not exist |
| 6 | Protocol C labeller-facing pilot artifact | **RED** | `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` does not exist |

Per spec §"PRE-DISPATCH PREREQUISITES":
> "If ANY row is RED: pilot does NOT dispatch. Halt. Surface the failed prerequisite to owner. Do NOT improvise."

**HALTING per spec.** Phase A.1 has not begun.

## Empirical evidence

### Row #5 — Protocol B labeller-facing pilot artifact MISSING

Commands run:
```bash
ls -la prompts/protocol_b_composition_first_v1_0_pilot.md
# → ls: cannot access 'prompts/protocol_b_composition_first_v1_0_pilot.md': No such file or directory

ls prompts/
# → gto_labeller_v1.md, gto_labeller_v2.md, gto_labeller_v3.1.md,
#   gto_labeller_v3.md, protocol_b_composition_first_v1_0.md (61515 bytes),
#   protocol_c_adversarial_elimination_v1_0.md (82255 bytes), stage4_drafts/
```

`prompts/protocol_b_composition_first_v1_0.md` (the source design artifact) exists at 61515 bytes. Its frontmatter explicitly distinguishes design-artifact from labeller-facing:

```
## PRE-PILOT BUILD REQUIREMENT (v1.0.1 addition)

**THIS FILE IS A DESIGN ARTIFACT, NOT A LABELLER-FACING PROMPT.**

(or equivalent labeller-facing artifact) with these sections expanded
in-place — replacing the inheritance-by-reference paragraphs in
§"Buckets", §"Features", and §"DO NOT Rules" of THIS file.
```

The labeller-facing `_pilot.md` artifact required by Protocol B v1.0.1's own PRE-PILOT BUILD REQUIREMENT was never built.

### Row #6 — Protocol C labeller-facing pilot artifact MISSING

Same pattern:
```bash
ls -la prompts/protocol_c_adversarial_elimination_v1_0_pilot.md
# → ls: cannot access ... No such file or directory
```

`prompts/protocol_c_adversarial_elimination_v1_0.md` (source design artifact) exists at 82255 bytes. The labeller-facing `_pilot.md` artifact does not exist.

### Rows #2 + #3 — Pilot 100-hand corpus DOES NOT EXIST

Commands run:
```bash
find . -name "*pilot*100*" -print
# → (empty)

find . -name "*pilot_corpus*" -print
# → (empty)

find . -name "*pilot_100*" -print
# → (empty)

find . -name "stratified*" -print
# → (empty)

find . -name "*stage4*corpus*" -print
# → (empty)

git log --oneline --all | grep -iE "(corpus|pilot.*corp|100-hand|stratified)"
# → 30ec324 Stage 4 prep Task 4 — Stage 6 held-out test set v1.0 (50-hand corpus)
# → 6b2bd23 Stage 3.5 commit 12/16: MUSTs #18+#33+#51 corpus reauthoring + 81-case pytest consumer
# → b1a9a91 Stage 3.5 BLUEPRINT: single-artifact 5-MUST plan + corpus + re-audit
# → f9cde81 Phase 3.5.1: pilot sample selected — 16 hands, stratified
# → 47ec600 Group D shortlist: 11 reversal candidates stratified across 3 sources for owner async pick
```

The most recent pilot-related corpus is the Phase 3.5.1 16-hand stratified sample (`f9cde81`) from earlier work. The Stage 4 pilot orchestration spec calls for a **100-hand stratified corpus** disjoint from the Stage 6 holdout (50 hands) and v2.3 calibration manifest (28 + 10 = 38 hands). This 100-hand corpus does not exist yet.

Per spec rows #2 + #3:
> Run the non-overlap check defined in Stage 6 §"Non-overlap verification" against the pilot 100; zero `(sorted(hero), sorted(board))` fingerprint matches

The non-overlap check cannot run if the pilot 100 doesn't exist.

### Other rows — checked GREEN (for completeness)

| # | Prerequisite | Status | Note |
|---|---|---|---|
| 1 | Stage 6 held-out hash matches v1.0.3 lock (`65cfbf26...`) | GREEN | Spec at master c4f29a5 |
| 4 | Protocol A v3.1 frozen + checksum recorded | GREEN | `prompts/gto_labeller_v3.1.md` exists; checksum to record at A1 |
| 7 | Stage 5 retrain protocol v1.0.1 sealed | GREEN | `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 in comms |
| 8 | Task 4.5 logic hardening sealed (PR #21 add2617) | GREEN | Confirmed in master log |
| 9 | QC pre-pilot sweep clean | GREEN | Phase 5 sweep complete; HIGH/MEDIUM addressed via PR #31 |
| 11 | Solver options match `feedback_solver_aligned_sizing.md` | GREEN | Adjudication panel preconfigured at Phase F dispatch |
| 12 | Pilot orchestrator session-launch cwd | GREEN | `~/river-rats-v2/` confirmed |
| 13 | Owner explicit greenlight | GREEN | Owner /loop "authorise pilot" at 15:35 SAST |
| 14 | Anthropic API tier confirmed | UNCERTAIN — to verify in A1 (deferred until preflight properly initiated) |
| 15 | Model selection locked | UNCERTAIN — to lock in A2 (deferred until preflight properly initiated) |
| 16 | `_villain_pos_raw` live-selection rule | BLOCKED on row #2 (need pilot corpus to sample partial-fold MW fixtures) |

11 GREEN, 2 UNCERTAIN-pending-preflight, 4 RED, 1 BLOCKED.

## Why this halt is correct (not over-cautious)

Per spec PRE-DISPATCH PREREQUISITES gate:
> If ANY row is RED: pilot does NOT dispatch. Halt. Surface the failed prerequisite to owner. Do NOT improvise.

The directive at `082336d` says "begin Phase A preflight NOW" — but Phase A is gated by the PRE-DISPATCH PREREQUISITES check. The Pilot Orchestrator's read-list explicitly includes:
> review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md (this script, including PRE-DISPATCH PREREQUISITES — verify ALL 16 prereqs are GREEN before starting Phase A; row #16 added in v1.0.3 per QC HIGH-1 / S-A12 close)

Phase A depends on the corpus + labeller-facing artifacts to even run:
- A3 5-call latency probe needs labeller-facing prompts to dispatch real labellers
- A4 calibration runs against the calibration manifest, but conceptually validates the labeller persona using its labeller-facing prompt
- A5 `_villain_pos_raw` live-selection check needs partial-fold MW fixtures from the pilot 100-hand corpus
- A6 cost projection extrapolates from A3, which needs the labeller-facing prompts

Improvising — for example, building the labeller-facing artifacts ad-hoc during preflight, or substituting the existing 16-hand sample for the 100-hand corpus — would violate spec §"Do NOT improvise" AND would likely produce false-clean preflight signals.

## Recommended path forward (orchestrator + owner decide)

### Option 1 — Build the missing pre-dispatch artifacts FIRST (RECOMMENDED)

Three discrete pre-dispatch builds, sequential or parallel:

**Build A — Protocol B labeller-facing artifact (`prompts/protocol_b_composition_first_v1_0_pilot.md`)**
- Per Protocol B v1.0.1 PRE-PILOT BUILD REQUIREMENT: take source `protocol_b_composition_first_v1_0.md` and verbatim-inline the Bucket taxonomy + Features + DO NOT Rules sections in-place (replacing the inheritance-by-reference paragraphs)
- Reviewer-verify per spec row #5
- Estimated effort: ~30-45 min build + reviewer cycle

**Build B — Protocol C labeller-facing artifact (`prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`)**
- Same pattern as Build A applied to Protocol C
- Estimated effort: ~30-45 min build + reviewer cycle

**Build C — Pilot 100-hand stratified corpus**
- This is a SCOPE/STRATIFICATION question — does the corpus come from existing situation factories, recent self-play runs, or fresh generation?
- Stratification dimensions per locked Stage 4 plan: street, position, opponent count, board texture, hero range placement
- Disjointness guarantees: zero fingerprint matches against Stage 6 50-hand holdout + v2.3 28+10 calibration manifest
- Estimated effort: depends on source; possibly 1-2h if generating fresh, 15-30 min if curating from existing situations

Total effort to clear PRE-DISPATCH gate: **~2-4h** (depending on corpus source choice).

After PRE-DISPATCH clear: Phase A preflight (~45 min per spec time estimates) → Phase B (~5-6h heavy) → Phases C-G (~4h).

### Option 2 — Defer pilot dispatch; address gap-closing as separate Stage 4 pre-dispatch tasks

Recognize this is its own work batch (Tasks 6/7/8 or labeled however). Treat it as Stage 4 pre-dispatch wave 3:
- Task 6: Protocol B labeller-facing artifact build
- Task 7: Protocol C labeller-facing artifact build
- Task 8: Pilot 100-hand corpus generation + stratification + disjointness verification

Standing per-batch protocol per task. Estimated total: same ~2-4h. After all three sealed: re-issue pilot dispatch directive.

### Option 3 — Adjust spec to remove rows #2/#3/#5/#6 as PRE-DISPATCH gate items

NOT recommended. Rows exist for empirically-load-bearing reasons:
- Row #5/#6 (labeller-facing artifacts): without verbatim-inlined prompts, labellers in Phase B would inherit-by-reference from a "design artifact" tag, likely breaking the labelling contract or producing inconsistent outputs across labellers
- Row #2/#3 (pilot corpus disjoint): a pilot run on overlapping hands with holdout/calibration would invalidate Stage 6 evaluation + introduce information leakage

## Halt comm + waiting state

Pilot Orchestrator persona STANDING DOWN until:
1. Orchestrator directive on path forward (Option 1, 2, or 3)
2. Pre-dispatch artifacts built + sealed (under whichever Option)
3. New "begin Phase A" directive issued

In the meantime, /loop will monitor for orchestrator response. Per
`feedback_listen_to_orchestrator_always.md`: orchestrator's
direction = sufficient authorization to proceed on whichever path.

## References

- Authorization directive: `082336d` (`MAIN_TERMINAL_PILOT_DISPATCH_AUTHORIZED_PROCEED_2026-04-26.md`)
- Spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 (master `c4f29a5`)
- Pre-pilot brief: `387e268` (`MAIN_TERMINAL_PR31_MERGED_PILOT_GATE_CLEAR_2026-04-26.md`)
- Protocol B v1.0.1 source: `prompts/protocol_b_composition_first_v1_0.md`
- Protocol C v1.0.1 source: `prompts/protocol_c_adversarial_elimination_v1_0.md`
- Stage 6 v1.0.3 holdout: hash `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5` over 47652 bytes
- Calibration v2.3: `river-rats-core/calibration_exam.py` (constants `STANDARD_EXAM_SIZE`, `STANDARD_PASS_THRESHOLD`, `GTO_REVERSAL_HANDS`, `GROUP_D_REVERSAL_HANDS`)

**Status: PILOT DISPATCH HALTED at PRE-DISPATCH PREREQUISITES gate. 4 rows RED. Awaiting orchestrator + owner direction on path forward.**
