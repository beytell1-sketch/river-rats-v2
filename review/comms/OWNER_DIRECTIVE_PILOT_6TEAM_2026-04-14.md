---
date: 2026-04-14
from: Owner (Rupert)
to: Builder team
re: Amended pilot — merge 6-team structure test with feature attention pilot
status: DIRECTIVE — replaces the pilot section of PLAN_PHASE3_FINAL
---

# Amended Pilot: 6-Team Structure + Feature Attention

## What changed

The original pilot ran 3 approaches × 2 agents = 6 labellers +
3 challengers = 9 agents on 20 hands. It tested feature attention
approaches only.

The amended pilot runs 6 teams × 20 hands, with 2 teams per
feature attention approach. It tests both the feature attention
approaches AND the full 6-team production structure.

## Structure

| Team | Feature attention approach | Agents | Hands |
|------|--------------------------|--------|-------|
| T1 | A (auto-tag Tier 1, agent removes) | 2 (10 hands each) | 20 |
| T2 | A | 2 | 20 |
| T3 | B (blank slate + automated check) | 2 | 20 |
| T4 | B | 2 | 20 |
| T5 | C (action-dependent auto-tags) | 2 | 20 |
| T6 | C | 2 | 20 |

**Total: 12 labelling agents + 1 comparison programmer = 13**

Each team receives the 20 hands in a different random order
(6 seeds), per the production plan's team differentiation rule.

No team sees another team's output.

## What this tests

### Feature attention (original pilot question)

- **Within-approach agreement:** T1 vs T2 (both Approach A),
  T3 vs T4 (both B), T5 vs T6 (both C). Which approach
  produces consistent feature tags between independent agents
  using the same method?
- **Cross-approach comparison:** Which approach produces the
  most accurate and useful feature attention data overall?
- **All original pilot metrics still apply:** inter-rater
  agreement, false positive/negative rates, removal burden
  (A only), flag response quality (B only), intention
  consistency, vocabulary proposals.

### 6-team production structure (new question)

- **Action consensus:** Do 6 teams agree on the 20 hands?
  How many are UNANIMOUS (6/6), STRONG (5/6), MAJORITY (4/6),
  SPLIT, or FRAGMENTED?
- **Difficulty consensus:** Do teams agree on difficulty? Are
  there CONTESTED hands? Any CONFIDENT_SPLIT (D1 majority +
  action split)?
- **Comparison report format:** Does the automated comparison
  report produce useful, readable output? Can the owner make
  decisions from it?
- **Pass 2 dry run:** If any hands are non-unanimous, run the
  Pass 2 treatment (challenger for UNANIMOUS+STANDARD, expert
  reviewer for STRONG, full panel for MAJORITY or worse). Test
  the escalation process end-to-end on real data.

### Calibration cross-check (bonus)

4 of the 20 pilot hands can be selected from the calibration
failures (MW-12, MW-15, MW-17, MW-28) or similar edge cases.
Does the 6-team structure catch the patterns that the single
calibration agent missed? If 4/6 teams get MW-17 right and
2/6 get it wrong, the consensus process works. If all 6 miss
it, there's a systemic prompt issue.

## Hand selection (20 hands)

Same stratification as the original pilot, but include at least
2-3 hands similar to the calibration failure patterns:

| Criterion | Count | Notes |
|-----------|-------|-------|
| Facing bet — CALL expected | 4 | Include 1 AK-overcard-equity type (MW-17 pattern) |
| Facing bet — FOLD expected | 3 | |
| Facing bet — RAISE expected | 3 | Non-monster semi-bluff |
| Not facing — BET expected | 4 | Include 1 OOP-value-bet type (MW-28 pattern) |
| Not facing — CHECK expected | 3 | Include 1 river-air-3way type (MW-12/15 pattern) |
| Difficulty 3 expected | 3 | Boundary spots |
| **Total** | **20** | 10 reconstructed + 10 new factory |

## Pilot evaluation

After all 6 teams finish, produce:

### Report 1: Feature attention comparison (original pilot)

Per approach (A, B, C):
- Within-approach Jaccard similarity on feature tags
- False positive/negative rates vs reviewer assessment
- Removal burden (A) / flag response quality (B)
- Recommendation: which approach for production

### Report 2: 6-team consensus (new)

Per hand:
- Full comparison report row (same format as production)
- Action consensus classification
- Difficulty consensus classification
- CONFIDENT_SPLIT flags
- Intention Jaccard across all 6 teams
- Feature Jaccard across all 6 teams

Summary statistics:
- % UNANIMOUS, % STRONG, % MAJORITY, % SPLIT
- % CLEAR difficulty, % CONTESTED
- Number of CONFIDENT_SPLIT hands
- Average intention Jaccard
- Average feature Jaccard

### Report 3: Pass 2 dry run (if applicable)

For any non-unanimous hands:
- Run the appropriate Pass 2 treatment
- Document: did the escalation process produce a clear
  resolution?
- Document: was the final label better than simple majority
  vote?

## Pilot gate

Owner reviews all 3 reports. Decisions:

1. Which feature attention approach (A, B, or C) for production
2. Does the 6-team consensus structure work? Produces useful
   disagreements, not noise?
3. Does the comparison report format work? Readable, actionable?
4. Does Pass 2 escalation work? Adds value, not just process?
5. Any adjustments needed before scaling to 385 hands?

If the 6-team structure doesn't surface useful disagreements
on 20 hands (e.g., 20/20 are UNANIMOUS with zero interesting
difficulty splits), consider whether 6 teams is justified at
scale or whether 4 teams would suffice.

## What this does NOT change

- Production plan structure (Pass 1 → Pass 2 → Assembly)
- 385 total training hands
- Enriched output schema
- Seed vocabulary
- Solver verification triggers
- Phase 4 training plan

---

**Builder: run this amended pilot. 12 labelling agents + 1
comparison programmer. Produce all 3 reports. Send for pilot
gate review.**
