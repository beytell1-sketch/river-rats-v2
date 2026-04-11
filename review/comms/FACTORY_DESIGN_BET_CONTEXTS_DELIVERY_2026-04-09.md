---
date: 2026-04-09
from: GTO Expert
to: Reviewer / Owner
re: Factory design brief — BET context situations (batch 4)
status: DELIVERED — awaiting reviewer then owner approval
---

## Deliverable

`review/FACTORY_DESIGN_BET_CONTEXTS.md`

Factory design brief for 100 BET-context situations across 6 sub-patterns.

---

## What was produced

A structured factory design brief using the FACTORY_DESIGN_RAISE_CONTEXTS_V2.md
format, adapted for BET/CHECK decisions and the specific gaps identified by the
recalibration run.

Sub-patterns and counts:

| Code | Description | Count | Target step |
|------|-------------|-------|-------------|
| BP1 | IP PFA value c-bet | 30 | 3A |
| BP2 | OOP PFA value c-bet | 15 | 3B |
| BP3 | PFA semi-bluff c-bet | 20 | 4A-D |
| BP4 | IP thin value non-PFA | 15 | 5 |
| BP5 | OOP value exception | 10 | 6 |
| BP6 | CHECK counterexamples | 10 | Default/suppressors |
| Total | | 100 | |

---

## Key design decisions made

**On villain_air_pct:** The brief documents exactly why current factory
situations produce degenerate air_pct (0.162-0.297) and how to construct
situations that reach 0.40-0.55. The core fix is using cold-callers (BTN/CO)
as villains on A/K-high dry boards, not BB defenders. Cold-callers have tighter
preflop ranges that miss high boards much harder. This was the primary blocker
for Steps 3B and 6.

**On villain_aggression_count = 0:** The brief explicitly requires this for
BP2 and BP5 (Steps 3B and 6), explains the action sequences that produce it
(villain called preflop, checked postflop — no bets), and flags it as a
structural constraint rather than a variation parameter.

**On SPR realism:** The brief directly addresses the SPR=1.11 Batch 1 artifact.
Flop SRP situations must use effective_stack proportional to pot (e.g.,
pot=90, effective_stack=900 gives SPR=10). The brief gives this calculation
explicitly in R3. All BP1 and BP2 flop situations should use SPR 8-12.

**On IP/OOP balance:** BP1 (30 IP) + BP3 IP portion (17 IP) + BP4 (15 IP) = 62 IP
situations. BP2 (15 OOP) + BP3 OOP portion (3) + BP5 (10 OOP) = 28 OOP.
Plus BP6 mixed. Final IP: ~67, OOP: ~33. This directly corrects the 95% OOP
concentration that blocked Steps 3A, 4B-D, and 5.

**On BP3 sub-condition allocation:** The four sub-conditions of Step 4 are
explicitly allocated (4A: 8 situations, 4B: 6, 4C: 3, 4D: 3) rather than
leaving it to the factory agent to decide. This prevents all 20 semi-bluff
situations landing on sub-condition 4A (combo draw only) and ignoring the
blocker-based sub-conditions.

**On BP6 CHECK counterexamples:** Each of the 7 failure modes maps to a
specific suppressor or unmet gate in the BET tree. One situation per mode
explicitly shows the single failing feature. The BP6-E situation (villain_air_pct
= 0.32 on an otherwise valid Step 3B setup) is the most instructive — it pairs
directly with a BP2 situation on a near-identical board, showing the model
exactly where the 0.40 gate sits.

---

## What the reviewer should check

1. Feature conditions in each sub-pattern match the recalibrated BET tree
   exactly (see Tree Version Alignment Check table at end of brief).

2. The BP3 sub-condition 4C references board_favour >= 0.30. The tree demotes
   board_favour from primary gate but retains it as a feature. 4C is the one
   place board_favour is still used as a design constraint. Confirm this is
   consistent with the tree as written.

3. BP5 (Step 6) requires connectivity_score <= 3. The brief specifies low
   boards (7-high, 8-high) for hero to achieve high villain_air_pct. Confirm
   that 7-6-2 type boards (which have connectivity concerns) are filtered out
   by the connectivity_score <= 3 gate, and that the board examples in the brief
   satisfy this.

4. BP6-D uses a connected board (Tc-9d-8c) as a Tier 4 example where Step 3A
   exits without firing. Confirm that straight_danger on Tc-9d-8c is >= 0.50,
   which would also trigger S1 if hero has no made hand and draw_outs < 12.
   If S1 fires, the CHECK label is correct and the failure mode is S1, not
   just Tier 4. The brief may need to clarify whether BP6-D situations are
   S1-suppressed or simply Tier 4 non-firings. Both produce CHECK; the distinction
   matters for the model's feature attribution.

5. The reviewer checklist has 18 items. Confirm all 18 are auditable from the
   situation data without requiring re-running the labeller.

---

## What this brief does NOT cover

- Board-level feature computation (villain_air_pct calculation by board/range
  combination) — that is an architecture task.
- Hero card enumeration within each sub-pattern — that is a factory generation task.
- The actual situation JSONL format — reuse the Batch 3 format unchanged.
- Action sequence validation — the existing validator covers this.

---

## Next steps (for owner to direct)

1. Owner approves or redirects this brief.
2. Architecture agent reads the brief and produces a board allocation plan
   (which new boards to use, SPR values, action sequences).
3. Factory generation agents (2-3) build the JSONL situations from the brief.
4. Deterministic labeller runs on the new 100 situations (sanity check only —
   not the final label source).
5. GTO expert labels all 100 situations in full context.
6. Combine all batches (~663 total) and proceed to dual labelling.

---

*Written to: review/comms/FACTORY_DESIGN_BET_CONTEXTS_DELIVERY_2026-04-09.md*
