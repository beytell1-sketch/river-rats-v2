# Restart Prompt — Pass 2 Targeted Review

## Status at pause (2026-04-14)

Pass 1 labelling: COMPLETE (156 agents, 385 hands, comparison report approved)
Pass 1 gate: PASSED by owner
T5-T6 discovery: COMPLETE (78 agents, union report approved)
Pass 2: BLOCKED — all 13 reviewer agents failed due to Anthropic usage quota exhaustion (error "You're out of extra usage · resets 10pm Africa/Johannesburg"). Retry after quota reset.

## Triage (already computed)

68 hands flagged for Pass 2, deduplicated into 5 tiers:

| Tier | Category | Count | Treatment | Agents |
|------|----------|-------|-----------|--------|
| 1 | CONFIDENT_SPLIT | 1 | Panel of 3 + solver mandatory | 3 |
| 2 | MAJORITY split | 13 | Panel of 3 + solver | 3 |
| 3 | HARD/CONTESTED difficulty | 20 | Panel of 3 | 3 |
| 4 | STRONG (3/4) | 25 | 1 expert reviewer per batch of 9 | 3 |
| 5 | CHECK->BET transitions (UNANIMOUS+STANDARD) | 9 | 1 challenger | 1 |
| **Total** | | **68 hands** | | **13 agents** |

## Artefacts ready for re-launch

- Triage list: `/tmp/pass2_triage.json` (68 hands, tier-sorted)
- Review packets (one per reviewer, with situation text + 4 team labels + discovery union):
  - `/tmp/pass2_packets/tier1_reviewer{1,2,3}.json`
  - `/tmp/pass2_packets/tier2_reviewer{1,2,3}.json`
  - `/tmp/pass2_packets/tier3_reviewer{1,2,3}.json`
  - `/tmp/pass2_packets/tier4_batch{0,1,2}.json`
  - `/tmp/pass2_packets/tier5_challenger.json`
- Output dir: `/tmp/pass2_results/` (empty — retry writes here)

## Re-launch

Re-issue the 13 agent calls with the same prompts used in the previous session (see commit `aa54ef4` and subsequent message history). Each reviewer reads their packet + the KB + the labelling prompt, judges each hand independently, and writes JSON results.

Output schema per hand (panel tiers 1-3):
```
{situation_id, my_action, my_confidence, my_reasoning, team_agreement:{T1,T2,T3,T4}, decisive_features, solver_recommended, solver_spot}
```

Tier 4 schema: adds `dissenter_valid: bool`.
Tier 5 schema: `{situation_id, my_action, my_confidence, my_reasoning, old_check_defensible, new_bet_defensible, solver_recommended}`.

## After Pass 2 reviewers complete

1. Aggregate panel votes (per-hand majority across 3 panelists)
2. Cross-reference reviewer actions vs Pass 1 team consensus
3. Build consolidated report at `review/comms/PASS2_REVIEW_REPORT_2026-04-14.md`
4. List hands flagged for solver (expected 14 mandatory + panelist additions)
5. Report: (a) how many Pass 1 labels stand, (b) how many change, (c) CHECK->BET transitions validated vs flagged for over-aggression
6. Present for Pass 2 gate

## Pass 1 final stats (for context)

- 86.2% UNANIMOUS (332/385), 10.4% STRONG (40), 3.4% MAJORITY (13)
- Intention Jaccard 0.850, feature Jaccard 0.846
- 0 SPLIT hands, 1 CONFIDENT_SPLIT
- Recon 200: 41.5% old-vs-new agree; 0 CALL↔RAISE swaps, 0 CALL→FOLD high-equity cases
- T5-T6 union adds avg 8.5 features/hand on top of T1-T4's 14.1 (total avg 22.6/46 non-excluded)

## Files already committed

- `training-data/pass1_T{1-4}_labels.jsonl`
- `training-data/pass1_comparison.jsonl`
- `training-data/pass1_recon_comparison.jsonl`
- `training-data/pass1_discovery_union.jsonl`
- `review/comms/PASS1_COMPARISON_REPORT_2026-04-14.md`
- `review/comms/PASS1_DISCOVERY_REPORT_2026-04-14.md`
- Pass 1 gate approval (from owner) and discovery gate approval (from owner) in session history
