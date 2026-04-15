---
date: 2026-04-14
from: Owner (Rupert)
to: Builder team
re: BP-series villain defect — full relabel, solver budget constraints
status: DIRECTIVE — blocks final assembly and Phase 4 training
discovered: Pass 2 solver verification preparation
---

# Phase 3.5: BP Villain Reconstruction + Full Relabel

## The defect

185 BP-series factory hands declare `num_opponents=2` (3-way
pot) but only record 1 villain position. The second villain
seat was dropped by the generator.

Pass 1 labelling teams saw incomplete villain information on
half the dataset. They labelled these hands with either (a) a
guessed second villain or (b) heads-up reasoning against the
one declared villain. Either way, the labels carry structural
noise.

Inter-team agreement (Pass 1 UNANIMOUS = 86%) does not prove
correctness when all teams had the same missing input. They
agreed on the wrong mental model.

## Decisions

### 1. Relabel ALL 185 BP-series hands

Not just the close ones. Unanimous agreement on wrong input
isn't correctness — it's shared blindness. Relabel all 185
with the full villain list.

### 2. Solver budget is the hard constraint

Owner runs solver verification on flagged hands only — not
200 d-series, not all BP relabels. Build the solver list by
filtering to:

- All Pass 2 MAJORITY-split hands (13 from d-series + new BP splits)
- All CONFIDENT_SPLIT hands
- Hands where old-vs-new BP label flips are in the CALL↔RAISE
  or CALL↔FOLD (equity > 0.30) category
- A small sample (~5-10) of the highest-disagreement hands
  from the BP old-vs-new comparison

Target solver budget: ~30 hands maximum. Owner triages
further if the filter yields more.

### 3. d-series solver verification proceeds now in parallel

The 200 d-series hands have complete villain information.
Solver verification on flagged d-series hands is not blocked.

## Execution plan

### Phase 3.5A: Build villain inference script

Write a script that for each BP hand:
1. Reads `action_string` and declared positions
2. Infers the 2nd villain from preflop structure (hero position +
   declared villain + pot shape + action sequence)
3. Produces the complete villain list

Human-review a sample of 20 BP hands to verify inference
correctness before batch-running on all 185.

**Gate 5.5A:** Owner reviews 20-hand inference sample. Approve
before batch run.

### Phase 3.5B: Batch-run inference on all 185 BP hands

Produces updated situation records with complete villain lists.
Verify: zero hands with `num_opponents=2` and only 1 declared
villain remaining.

### Phase 3.5C: Re-run Pass 1 on 185 BP hands

4 labelling teams, Approach C amended (same protocol as
original Pass 1). Critical:

- **Fresh agents.** Do NOT reuse Pass 1 BP agents — they have
  prior labels and will anchor. Fresh agents only.
- **Different random order per team** (4 new seeds).
- **Same prompt** (gto_labeller_v2.md).
- **~75 agent-calls total** (4 teams × ~19 batches of 10).

Each agent sees the updated situation with the complete villain
list. The composition quad features (TP+/medium/draw/air) remain
as computed — they were blended across all villains even in the
original data, so the feature values don't change. What changes
is the agent's mental model of the spot.

### Phase 3.5D: T5-T6 discovery on 185 BP hands

Bottom-up feature scan per the original discovery protocol. 2
teams, ~38 agent-calls total.

Includes discovery of any newly-relevant features now that both
villains are visible (e.g., sandwich position features, second
villain position-specific reads).

### Phase 3.5E: BP comparison report

For each of 185 BP hands:
- Old Pass 1 consensus action
- New Pass 1 consensus action
- Action agreement (yes/no)
- Difficulty comparison
- Feature attention union change

Summary statistics:
- % of BP hands where labels flipped
- Distribution of flip types (CHECK→BET, FOLD→CALL, etc.)
- Correlation between flip rate and hand bucket

Quantifies the damage from the original defect.

### Phase 3.5F: Pass 2 on BP splits

Same structure as the original Pass 2 — challengers for
unanimous, expert reviewers for STRONG, full panel for
MAJORITY. Estimated 5-10 agents depending on how many hands
split in the new labelling.

### Phase 3.5G: Solver list construction

Filter d-series + BP relabel to the solver verification list.
Target ~30 hands. Owner runs in GTO Wizard with:
- Complete villain information
- Sequences validated
- Bet sizes matching solver options exactly (25%/66% flop,
  33%/75% turn/river)

### Phase 3.5H: Final assembly

Only after solver verification completes:
- Apply d-series Pass 2 overrides (10 hands from earlier report)
- Apply BP relabel results (replaces all 185 BP Pass 1 labels)
- Apply any solver-driven label corrections
- Union feature attention across T1-T6 (for all 385 hands)
- Build 108-column training CSV (54 features + 54 attn flags)
- Vocabulary review (merge proposed_tags synonyms)

## Gate structure

| Gate | What | When |
|---|---|---|
| 5.5A | Owner reviews 20-hand inference sample | After Phase 3.5A |
| 5.5B | Owner reviews Pass 1 + Pass 2 BP relabel report | After Phase 3.5F |
| Solver gate | Owner runs ~30-hand solver batch | After 5.5B |
| 6 | Owner approves final label set for training | After Phase 3.5H |

## Agent budget

| Phase | Agent-calls |
|---|---|
| 3.5A script + sample review | 1 programmer |
| 3.5B batch inference | 0 (script run) |
| 3.5C BP Pass 1 relabel | ~75 |
| 3.5D BP T5-T6 discovery | ~38 |
| 3.5E comparison report | 1 programmer |
| 3.5F BP Pass 2 | ~5-10 |
| 3.5G solver list + owner verification | ~1 + owner |
| 3.5H final assembly | 1 programmer |
| **Total** | **~125 agents + owner solver session** |

Plus the original Pass 2 override application and vocabulary
review already queued.

## v2.3 backlog addition (MANDATORY)

Log as a v2.3 blocker: **the feature extractor and situation
factory must always record ALL villain seats.** The BP-series
generator's bug (recording only one villain for 3-way hands)
cannot recur. This is a data-pipeline contract, not a
labelling choice.

Add a validator to `situation_factory.py`:
- If `num_opponents >= 2`, `villain_positions` must have at
  least `num_opponents` entries
- Fail at generation time, not at labelling time

## What does NOT change

- d-series (200 hands) labels stand as-is. Pass 2 overrides
  apply. Solver verification on d-series flagged hands proceeds.
- gto_labeller_v2.md prompt — no changes
- Tag vocabulary — no changes
- Calibration — no changes (already passed 20/24)
- Feature attention training mechanism (Exp 3 auxiliary flags)
- Phase 4 training plan

## What blocks v2.2 training

Phase 3.5 must complete before final assembly (Phase 3.5H)
and Phase 4 training. No training on incomplete data.

## d-series work proceeds in parallel

- Apply the 10 d-series Pass 2 label overrides now
- Build the solver verification list for d-series flagged hands
  (from the 14 mandatory + challenger flag)
- Owner runs d-series solver verification while Phase 3.5 BP
  relabelling executes
- By the time BP relabel completes, d-series is fully verified

---

**Builder: start Phase 3.5A — build the villain inference
script and human-review a 20-hand sample. Nothing else
proceeds until inference is validated.**
