---
date: 2026-04-13
from: Main terminal (orchestrator)
to: Owner (Rupert)
re: Plan — complete the facing-bet test set (task #4 final phase)
status: FOR REVIEW — awaiting approval before execution
---

## Why we are doing this

The v9-3way oracle has a measured **63% passive bias** on 3-way
check-to-hero spots. The 5 true remaining reference-set failures
(MW-17 under-calling, MW-25/40 passive BET→CHECK, MW-45
under-raising, MW-47 shared blind spot) are all manifestations of
this bias. Before we retrain v2.2 to fix it, we need a **second
evaluation axis** that measures the model's facing-bet behaviour
independently of the existing 40-hand reference set.

Without this test set, we would retrain v2.2 and have no way to
know if the model improved on facing-bet decisions — the reference
set only covers check-to-hero and BET/CHECK spots. We would be
flying blind on half the decision space.

The facing-bet test set was designed (40 situations), labelled by
4 GTO Expert agents, reviewed, and partially solver-verified. But
**structural errors in action sequencing** (wrong postflop order,
impossible bet-and-call sequences, fold-without-bet) contaminated
12 situations across 3 audit rounds. 5 situations still need
redesign. The root cause was hand-written action sequences without
machine validation.

This plan completes the test set with two systemic fixes:
1. **All action sequences validated by code** before any human sees
   them (hand_sequence_validator.py)
2. **All bet sizes aligned to GTO Wizard solver options** so solver
   verification is exact-match with zero sizing warnings

## What needs to happen

### Phase 1 — Redesign 5 failed situations (architecture)

**Situations:** FB-23, FB-32, FB-33, FB-34, FB-37

**Errors:**
- FB-23: Illegal fold without a bet (turn)
- FB-32: Impossible bet-and-call (BTN hero, CO bets → BTN acts
  before BB, can't see BB call)
- FB-33: Impossible bet-and-call (BB hero, BTN bets → BB acts
  before CO, can't see CO call)
- FB-34: Impossible bet-and-call (same as FB-33)
- FB-37: Missing player checks in action sequence (CO skipped)

**Requirements for each redesigned situation:**
- Use existing boards only (13 boards passed overlap checks)
- Use solver-aligned sizing ONLY:
  - Flop bets: 25% or 66% pot
  - Turn/river bets: 33% or 75% pot
  - Raises: 33% or 66% pot
- Action sequence must pass `hand_sequence_validator.py`
- Must maintain facing_bet=True
- Preserve the original axis coverage intent where possible

### Phase 2 — Fresh GTO Expert labels (40 situations)

This is the big resource commitment. ALL 40 situations get fresh
labels — not just the 5 redesigns. Here's why:

**Why relabel all 40, not just the 5 redesigns:**

1. **Sizing changed.** The solver-aligned sizing (25%/66% flop,
   33%/75% turn+river) produces different pot odds than the
   original sizing (33%/50%/67%). Different pot odds → different
   GTO-correct actions on borderline hands. Every CALL/FOLD
   decision near the pot-odds threshold needs re-evaluation.

2. **12 situations had positional corrections.** The earlier
   redesign round changed 12 situations from sandwich→closing or
   vice versa. 10 labels "survived" but the reasoning was built
   on the wrong positional assumption. Fresh labels with correct
   positions produce cleaner reasoning chains.

3. **Pot odds formula was inconsistent.** Agent 3 used a different
   formula from Agents 1/2/4. Standardising to call/(pot+bet+call)
   means all 40 labels use the same math.

4. **Solver verification showed 4 mixed spots and 2 label flips.**
   FB-15 was relabelled FOLD→CALL (wrong — solver says FOLD),
   FB-17 was RAISE→CALL. The expert labels were wrong on spots
   the solver clarified. Fresh labels with solver-verified sizing
   will be more accurate from the start.

5. **Trust.** After 4 audit rounds finding errors, the owner (and
   future reviewers) need to trust this test set completely. "We
   relabelled everything fresh with correct sequences and sizes"
   is a stronger foundation than "we patched 12, relabelled 2,
   kept 28 from the original round."

### Phase 3 — Machine validation gate

Before any GTO Expert sees a situation, every action sequence runs
through `hand_sequence_validator.py`. Any error = rejected, sent
back to the architect for correction. Zero human-written sequences
reach the labelling round without machine validation.

### Phase 4 — Independent reviewer

Reviewer checks all 40 situations post-labelling:
- Card conflicts
- Action consistency (machine-validated, but double-check)
- Axis coverage
- Label quality (reasoning cites equity vs pot odds, uses
  composition triple, considers position)
- No batch 4 / reference set overlap
- Pot odds formula consistency (all use call/(pot+bet+call))

### Phase 5 — Solver verification (19 flagged situations)

All RAISE labels, MEDIUM-confidence CALLs, and high-equity FOLDs
go through GTO Wizard. With solver-aligned sizing, every hand can
be entered exactly — no mapping, no red flags, no approximation.

### Phase 6 — Production test set file

Convert the 40 verified situations into a machine-readable format
(JSONL or CSV) with extracted features, ready for
`reference_evaluator.py` to score against the oracle.

---

## Team design

### Agent 1 — Architect (Phase 1)
**Role:** Redesign the 5 failed situations with correct action
sequences and solver-aligned sizing.
**Type:** architecture-expert
**Input:** The 5 failure descriptions from the definitive audit +
the 13 existing board specs + solver-aligned sizing table.
**Output:** 5 redesigned situation specs.
**Gate:** Every action sequence passes `hand_sequence_validator.py`
(the architect must run the validator and include the output).

### Agent 2 — Validator (Phase 1 gate)
**Role:** Run `hand_sequence_validator.py` on ALL 40 situations
(the 5 redesigned + the 35 unchanged) and confirm every one passes.
**Type:** lead-programmer
**Input:** The 40 situation specs (5 redesigned + 35 from original).
**Output:** Validation report — 40/40 pass or list of failures.
**Gate:** 40/40 pass required before Phase 2 starts.

### Agents 3-7 — GTO Expert labellers (Phase 2)
**Role:** Design hero cards and label GTO-correct actions with full
poker reasoning for all 40 situations.
**Type:** general-purpose (with detailed poker brief)
**Allocation:** 5 agents × 8 situations each = 40 total
(Process Guide Section 1.1: ≤10 hands per GTO agent)
**Input:** The validated situation specs + `knowledge/three_way_gto.md`
+ solver-aligned sizing table.
**Output:** 40 labelled situations with per-hand reasoning.
**Constraint:** Must use call/(pot+bet+call) for pot odds. Must
cite the composition triple framework. Must flag RAISE, MEDIUM-
confidence CALL, and high-equity FOLD for solver verification.

**Why 5 agents, not 4:**
The original round used 4 agents × 10 hands. That produced
situations where agents labelled the same board differently
(FB-17/FB-37 nut-straight contradiction). With 5 agents × 8 hands,
each agent handles fewer boards and cross-board consistency is
easier to enforce. Also, the solver verification showed 4 mixed
spots where the expert was wrong — more agents = more independent
judgment = higher chance of catching errors.

**Brief structure per agent:**
- Situations assigned by BOARD, not by number — each agent gets
  2-3 boards and all situations on those boards. This prevents
  cross-agent inconsistency on the same board.
- Each agent gets the solver-aligned sizing table and the
  instruction: "pot odds = call / (pot + bet + call). This is the
  equity-needed-to-call formula."
- Each agent is told which position hero is in and what the
  classification is (sandwich/closing/OOP-first) — no room for
  misinterpretation.

### Agent 8 — Independent reviewer (Phase 4)
**Role:** Audit all 40 labelled situations against the checklist.
**Type:** general-purpose (independent — has not seen Phase 1-2)
**Input:** The 40 labelled situations + checklist.
**Output:** Review report with APPROVED / APPROVED WITH FIXES /
BLOCKED verdict.
**Constraint:** Must be a FRESH agent that did not participate in
Phases 1-2. No self-reviewing.

### Agent 9 — Solver verification compiler (Phase 5)
**Role:** Generate the solver verification HTML with all 19 flagged
situations, using solver-aligned sizing (exact match, no mapping).
**Type:** lead-programmer
**Input:** The 40 labelled situations + solver sizing table.
**Output:** `review/SOLVER_VERIFY_ALL_19_V3.html`
**Constraint:** Every action sequence in the HTML must pass
`hand_sequence_validator.py`.

### Human — Owner (Phase 5)
**Role:** GTO Wizard solver verification of the 19 flagged hands.
**Input:** The solver verification HTML.
**Output:** Solver results per hand (action, frequency, notes).
**Gate:** Label confirmed, flipped, or marked as mixed.

### Agent 10 — Production file builder (Phase 6)
**Role:** Convert the final 40 verified situations into JSONL/CSV
with extracted features.
**Type:** lead-programmer
**Input:** The 40 verified and solver-confirmed situations.
**Output:** `training-data/facing_bet_test_set_40.jsonl` + 
evaluation script integration into `reference_evaluator.py`.

---

## Sequencing

```
Phase 1 (Architect)
  ↓
Phase 1 gate (Validator — 40/40 pass)
  ↓
Phase 2 (5 GTO Experts, parallel)  ← biggest resource commitment
  ↓
Phase 4 (Reviewer — independent)
  ↓
Phase 5a (HTML compiler)
  ↓
Phase 5b (Owner — GTO Wizard)     ← human in the loop
  ↓
Phase 6 (Production file builder)
  ↓
Task #4 COMPLETE → unblocks task #6 (v2.2 retrain)
```

Phases 1-2 can run in ~1 session. Phase 5b (solver verification)
depends on owner availability.

---

## Resource summary

| Phase | Agents | Type | Parallel? |
|---|---|---|---|
| 1 — Redesign | 1 | architecture-expert | — |
| 1 gate — Validate | 1 | lead-programmer | — |
| 2 — Label | 5 | general-purpose | YES (all 5 parallel) |
| 4 — Review | 1 | general-purpose | — |
| 5a — HTML | 1 | lead-programmer | — |
| 5b — Solver | human | — | — |
| 6 — Production | 1 | lead-programmer | — |
| **Total** | **10 agents + human** | | |

---

## Success criteria

The facing-bet test set is COMPLETE when:

1. 40 situations, all with facing_bet=True
2. Every action sequence passes `hand_sequence_validator.py`
3. All bet sizes are solver-aligned (25%/66% flop, 33%/75% turn+river)
4. 40 GTO Expert labels with per-hand reasoning
5. Independent reviewer approved
6. 19 flagged situations solver-verified via GTO Wizard
7. Production JSONL/CSV generated with extracted features
8. Integrated into `reference_evaluator.py` as second evaluation axis

---

## Risk register

| Risk | Mitigation |
|---|---|
| GTO Expert agents make new errors | 5 agents × 8 hands (not 4×10). Board-based assignment prevents cross-agent inconsistency. Machine-validated sequences. |
| Solver verification finds more label flips | Expected. The 4 mixed spots from round 1 suggest ~20% of labels are solver-sensitive. Budget for 4-8 flips in 19 verified hands. |
| Action sequences still wrong after machine validation | Validator catches all known error patterns (fold-without-bet, wrong response order, skipped players, impossible bet-and-call). If a new pattern appears, add it to the validator. |
| Sizing mismatch with solver | Eliminated. All sizes match GTO Wizard exactly. |
| Axis coverage shifts from redesigns | 5 redesigns on existing boards. Axis distribution monitored in Phase 4 review. |

---

## What this plan does NOT cover

- **FB-20 solver verification** — still outstanding from round 1.
  Include in Phase 5b alongside the 19 flagged from the fresh round.
- **Notation fixes for FB-05, FB-09, FB-18, FB-30** — these had
  "fold at start of street" notation issues. The full relabelling
  in Phase 2 supersedes these fixes (all sequences rewritten from
  scratch with machine validation).
- **v2.2 retrain** — task #6, gated on this test set completing.

---

**Awaiting approval. On "go" I execute Phase 1 immediately.**
