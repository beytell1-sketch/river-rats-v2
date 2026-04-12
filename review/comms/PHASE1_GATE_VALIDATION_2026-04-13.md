# Phase 1 Gate Validation — Facing-Bet Test Set
**Date:** 2026-04-13
**Author:** Lead Programmer
**Task:** Validate all 40 action sequences through hand_sequence_validator.py before GTO Expert labelling round
**Result: PASS — 40 / 40 VALID**

---

## Validation Results

| FB | Source | Positions | Street | Hero | Validator result |
|---|---|---|---|---|---|
| FB-01 | REDESIGN_12 | BB,CO,BTN | flop | BB | VALID |
| FB-02 | ORIGINAL | BB,CO,BTN | flop | BTN | VALID |
| FB-03 | ORIGINAL | BB,CO,BTN | flop | BB | VALID |
| FB-04 | REDESIGN_12 | BB,CO,BTN | flop | BB | VALID |
| FB-05 | ORIGINAL | BB,CO,BTN | flop | BTN | VALID |
| FB-06 | REDESIGN_12 | BB,CO,BTN | flop | BB | VALID |
| FB-07 | ORIGINAL | BB,CO,BTN | flop | CO | VALID |
| FB-08 | ORIGINAL | BB,CO,BTN | flop | CO | VALID |
| FB-09 | ORIGINAL | BB,CO,BTN | flop | BTN | VALID |
| FB-10 | REDESIGN_12 | BB,CO,BTN | flop | BB | VALID |
| FB-11 | ORIGINAL | BB,CO,BTN | flop | BTN | VALID |
| FB-12 | ORIGINAL | BB,CO,BTN | flop | BB | VALID |
| FB-13 | REDESIGN_12 | BB,CO,BTN | flop | CO | VALID |
| FB-14 | ORIGINAL | BB,CO,BTN | flop | BTN | VALID |
| FB-15 | REDESIGN_12 | BB,CO,BTN | flop | BB | VALID |
| FB-16 | ORIGINAL | BB,CO,BTN | flop | BB | VALID |
| FB-17 | REDESIGN_12 | BB,CO,BTN | turn | BB | VALID |
| FB-18 | ORIGINAL | BB,CO,BTN | turn | BTN | VALID |
| FB-19 | REDESIGN_12 | BB,CO,BTN | turn | BB | VALID |
| FB-20 | ORIGINAL | CO,BTN | turn | CO | VALID |
| FB-21 | REDESIGN_12 | BB,CO,BTN | turn | BB | VALID |
| FB-22 | ORIGINAL | BB,CO,BTN | flop | CO | VALID |
| FB-23 | REDESIGN_5 | BB,CO,BTN | river | BB | VALID |
| FB-24 | ORIGINAL | BB,CO,BTN | river | BTN | VALID |
| FB-25 | ORIGINAL | BB,CO | river | BB | VALID |
| FB-26 | ORIGINAL | BB,CO,BTN | river | BTN | VALID |
| FB-27 | REDESIGN_12 | BB,CO,BTN | flop | BB | VALID |
| FB-28 | ORIGINAL | BB,CO,BTN | flop | BB | VALID |
| FB-29 | ORIGINAL | BB,CO,BTN | flop | CO | VALID |
| FB-30 | ORIGINAL | BB,CO,BTN | flop | BTN | VALID |
| FB-31 | ORIGINAL | BB,CO,BTN | flop | BTN | VALID |
| FB-32 | REDESIGN_5 | BB,CO,BTN | flop | BB | VALID |
| FB-33 | REDESIGN_5 | BB,CO,BTN | flop | CO | VALID |
| FB-34 | REDESIGN_5 | BB,CO,BTN | flop | CO | VALID |
| FB-35 | REDESIGN_12 | BB,CO,BTN | turn | CO | VALID |
| FB-36 | ORIGINAL | CO,BTN | turn | CO | VALID |
| FB-37 | REDESIGN_5 | BB,CO,BTN | turn | CO | VALID |
| FB-38 | ORIGINAL | BB,CO,BTN | river | CO | VALID |
| FB-39 | REDESIGN_12 | BB,CO,BTN | river | BB | VALID |
| FB-40 | ORIGINAL | BB,CO,BTN | flop | BB | VALID |

---

## Summary

- **PASS: 40 / 40**
- **FAIL: 0 / 40**

**Gate criterion MET. Phase 2 (GTO Expert labelling) is UNBLOCKED.**

---

## Corrections Applied During Validation

Six situations required their action strings to be corrected before passing. These are spec description errors (wrong "closes action" label) in situations that were NOT redesigned — the underlying game state is valid but the written narrative misidentified which player acts last.

### FB-35 (REDESIGN_12) — Missing initiative check
The REDESIGN_12 document specifies "BB checks, BTN bets" on the turn. In a BB/CO/BTN pot, initiative order is BB → CO → BTN. CO must check before BTN can bet.

**Corrected action string:**
`BB check, CO check, BTN bet 90, BB fold, CO ???`
(CO's initiative check added before BTN's bet)

### FB-05, FB-09, FB-18, FB-30 (ORIGINAL) — BTN wrongly labelled "closing action" in CO-opens pot

These four situations all follow the pattern: CO opens, BTN calls, BB calls. On the action street, CO bets. After CO bets, clockwise-from-CO response order is BTN (seat 5, higher than CO's seat 4) first, then BB (seat 1, wrapping). BTN is the **first responder**, not the last. BB responds after BTN.

The spec descriptions say "BB folds, CO bets, BTN closes action" but this is structurally impossible: BB cannot fold in response to CO's bet before BTN has responded, because BTN is clockwise-from-CO before BB.

The correct sequences remove the premature BB fold and present BTN as first responder:

| FB | Corrected action string |
|---|---|
| FB-05 | `BB check, CO bet 60, BTN ???` |
| FB-09 | `BB check, CO bet 90, BTN ???` |
| FB-18 | `BB check, CO bet 60, BTN ???` |
| FB-30 | `BB check, CO bet 60, BTN ???` |

**Hero classification impact:** These four heroes (BTN) are the **first responder** to CO's bet, not the last. BB still acts after hero in each case. The spec's "hero closes action" label for these four situations is incorrect. GTO Expert agents should be aware that BB has a live decision after hero acts.

### FB-12 (ORIGINAL) — BB wrongly labelled "closing action" in BTN-opens pot

BTN opens, CO calls, BB calls. BTN bets. After BTN bets (seat 5), clockwise order is: BB (seat 1, wrapping) first, then CO (seat 4). BB is the **first responder**. CO is last.

The spec says "CO folds, hero BB closes action" but CO cannot fold before BB has responded to BTN's bet.

**Corrected action string:**
`BB check, CO check, BTN bet 45, BB ???`
(CO's premature fold removed; BB is first responder, CO still to act)

**Hero classification impact:** BB is the first responder to BTN's bet. CO still has a live decision after hero acts. The spec's "hero closes action" label is incorrect.

---

## Bet Sizing Flags

Approved sizings per spec: flop 25% or 66% pot | turn 33% or 75% pot | river 33% or 75% pot

10 of 40 situations use approved solver-aligned sizing. 30 of 40 use old sizing (Option B — original data keeps original sizing). GTO Expert agents should note which sizing applies.

**Situations using approved solver-aligned sizing (10):**

| FB | Source | Street | Sizing |
|---|---|---|---|
| FB-05 | ORIGINAL | flop | 66% (60 into 90) |
| FB-20 | ORIGINAL | turn | 75% (90 into 120) |
| FB-23 | REDESIGN_5 | river | 75% (90 into 120) |
| FB-24 | ORIGINAL | river | 75% (90 into 120) |
| FB-30 | ORIGINAL | flop | 66% (60 into 90) |
| FB-31 | ORIGINAL | flop | 66% (60 into 90) |
| FB-32 | REDESIGN_5 | flop | 66% (60 into 90) |
| FB-33 | REDESIGN_5 | flop | 66% (60 into 90) |
| FB-34 | REDESIGN_5 | flop | 25% (22 into 90) |
| FB-37 | REDESIGN_5 | turn | 75% (68 into 90) |

**Situations using non-approved (old) sizing (30):**

All 30 are expected per Option B — original data retains original sizing. Notable outliers for GTO Expert awareness:

- FB-09 (ORIGINAL): flop 100% pot (90 into 90) — pot-sized overbet
- FB-38 (ORIGINAL): river 100% pot (90 into 90) — pot-sized overbet
- FB-09 and FB-38 use pot-sized bets which fall outside the standard sizing matrix; GTO Expert should treat these as "large polarising bets" and reason accordingly.

---

## Action Strings for GTO Expert Agents

These are the validated action strings for each situation. Use these verbatim in labelling briefs.

### REDESIGN_12 situations

| FB | Positions | Street | Validated action string | Hero |
|---|---|---|---|---|
| FB-01 | BB,CO,BTN | flop | `BB check, CO bet 30, BTN fold, BB ???` | BB |
| FB-04 | BB,CO,BTN | flop | `BB check, CO bet 45, BTN fold, BB ???` | BB |
| FB-06 | BB,CO,BTN | flop | `BB check, CO bet 30, BTN fold, BB ???` | BB |
| FB-10 | BB,CO,BTN | flop | `BB check, CO bet 30, BTN fold, BB ???` | BB |
| FB-13 | BB,CO,BTN | flop | `BB check, CO check, BTN bet 45, BB fold, CO ???` | CO |
| FB-15 | BB,CO,BTN | flop | `BB check, CO bet 45, BTN fold, BB ???` | BB |
| FB-17 | BB,CO,BTN | turn | `BB check, CO bet 60, BTN fold, BB ???` | BB |
| FB-19 | BB,CO,BTN | turn | `BB check, CO check, BTN bet 90, BB ???` | BB |
| FB-21 | BB,CO,BTN | turn | `BB check, CO bet 45, BTN fold, BB ???` | BB |
| FB-27 | BB,CO,BTN | flop | `BB check, CO bet 30, BTN fold, BB ???` | BB |
| FB-35 | BB,CO,BTN | turn | `BB check, CO check, BTN bet 90, BB fold, CO ???` | CO |
| FB-39 | BB,CO,BTN | river | `BB check, CO check, BTN bet 90, BB ???` | BB |

### REDESIGN_5 situations

| FB | Positions | Street | Validated action string | Hero |
|---|---|---|---|---|
| FB-23 | BB,CO,BTN | river | `BB check, CO bet 90, BTN fold, BB ???` | BB |
| FB-32 | BB,CO,BTN | flop | `BB check, CO bet 60, BTN call 60, BB ???` | BB |
| FB-33 | BB,CO,BTN | flop | `BB check, CO check, BTN bet 60, BB call 60, CO ???` | CO |
| FB-34 | BB,CO,BTN | flop | `BB check, CO check, BTN bet 22, BB call 22, CO ???` | CO |
| FB-37 | BB,CO,BTN | turn | `BB check, CO check, BTN bet 68, BB fold, CO ???` | CO |

### ORIGINAL situations (23)

| FB | Positions | Street | Validated action string | Hero | Notes |
|---|---|---|---|---|---|
| FB-02 | BB,CO,BTN | flop | `BB bet 30, CO fold, BTN ???` | BTN | |
| FB-03 | BB,CO,BTN | flop | `BB check, CO bet 30, BTN call 30, BB ???` | BB | |
| FB-05 | BB,CO,BTN | flop | `BB check, CO bet 60, BTN ???` | BTN | BTN first responder; BB acts after |
| FB-07 | BB,CO,BTN | flop | `BB bet 45, CO ???` | CO | CO sandwiched; BTN behind |
| FB-08 | BB,CO,BTN | flop | `BB bet 45, CO ???` | CO | CO sandwiched; BTN behind |
| FB-09 | BB,CO,BTN | flop | `BB check, CO bet 90, BTN ???` | BTN | BTN first responder; BB acts after |
| FB-11 | BB,CO,BTN | flop | `BB bet 45, CO fold, BTN ???` | BTN | |
| FB-12 | BB,CO,BTN | flop | `BB check, CO check, BTN bet 45, BB ???` | BB | BB first responder; CO acts after |
| FB-14 | BB,CO,BTN | flop | `BB bet 30, CO fold, BTN ???` | BTN | |
| FB-16 | BB,CO,BTN | flop | `BB check, CO bet 45, BTN call 45, BB ???` | BB | |
| FB-18 | BB,CO,BTN | turn | `BB check, CO bet 60, BTN ???` | BTN | BTN first responder; BB acts after |
| FB-20 | CO,BTN | turn | `CO check, BTN bet 90, CO ???` | CO | 2-way; BB folded earlier |
| FB-22 | BB,CO,BTN | flop | `BB check, CO check, BTN bet 30, BB call 30, CO ???` | CO | |
| FB-24 | BB,CO,BTN | river | `BB bet 90, CO fold, BTN ???` | BTN | |
| FB-25 | BB,CO | river | `BB check, CO bet 90, BB ???` | BB | 2-way; BTN folded earlier |
| FB-26 | BB,CO,BTN | river | `BB bet 90, CO fold, BTN ???` | BTN | |
| FB-28 | BB,CO,BTN | flop | `BB check, CO bet 30, BTN call 30, BB ???` | BB | |
| FB-29 | BB,CO,BTN | flop | `BB bet 45, CO ???` | CO | CO sandwiched; BTN behind |
| FB-30 | BB,CO,BTN | flop | `BB check, CO bet 60, BTN ???` | BTN | BTN first responder; BB acts after |
| FB-31 | BB,CO,BTN | flop | `BB bet 60, CO fold, BTN ???` | BTN | |
| FB-36 | CO,BTN | turn | `CO check, BTN bet 60, CO ???` | CO | 2-way; BB folded earlier |
| FB-38 | BB,CO,BTN | river | `BB bet 90, CO ???` | CO | CO sandwiched; BTN behind |
| FB-40 | BB,CO,BTN | flop | `BB check, CO check, BTN bet 30, BB ???` | BB | BB sandwiched; CO behind |
