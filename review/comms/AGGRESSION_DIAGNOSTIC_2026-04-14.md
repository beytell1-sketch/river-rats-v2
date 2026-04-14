---
date: 2026-04-14
from: Builder
to: Owner
re: Aggression-feature diagnostic — current v2.2 dataset vs realistic 3-way postflop distribution
---

# Aggression Feature Diagnostic — 385 Hand Dataset vs Realistic 3-way Postflop

## TL;DR

- **`num_callers_to_bet` is DEAD**: 100% of 385 hands have value=0. The oracle cannot learn to read range-narrowing from callers.
- **`villain_aggression_count` has variance** but skewed: 51% / 44% / 5% for values 0/1/2. Cumulative multi-street aggression (agg≥2) only appears on river.
- **Archetype coverage is heavily skewed toward passive-line hands**: 94 flop-check-to-hero spots (target 35), 77 turn-after-checked-flop spots (target 25). These are over-represented by a combined ~110 hands.
- **Critical archetypes have ZERO support**: bet-and-call flop (sandwich/closing), turn second-barrel cumulative agg=2, turn bet-and-call, flop donk bet, river check-around, river bet-and-call.
- **Proposed fix**: supplement ~206 new hands targeting missing archetypes. Total after supplement: 591 hands.

## Current distribution vs realistic 3-way postflop target

| Archetype | Current | Target | Gap |
|---|---:|---:|---:|
| flop: facing single bet (no callers yet) | 55 | 70 | +15 |
| flop: facing bet-and-call — sandwich/closing (agg=1, ncb=1) | 0 | 40 | **+40** |
| flop: facing bet-and-raise (agg=2) | 4 | 12 | +8 |
| flop: checked to hero, zero aggression | 94 | 35 | **−59** (over) |
| flop: donk-bet facing hero as PFA | 0 | 15 | **+15** |
| turn: facing single bet (cumulative agg=1) | 18 | 30 | +12 |
| turn: facing single bet (cumulative agg=2) | 0 | 35 | **+35** |
| turn: facing bet-and-raise | 8 | 10 | +2 |
| turn: facing bet-and-call | 0 | 20 | **+20** |
| turn: checked back, hero leads/checks | 77 | 25 | **−52** (over) |
| river: facing single bet after agg=2 (triple barrel) | 15 | 30 | +15 |
| river: facing bet-and-raise | 15 | 15 | ✓ 0 |
| river: facing bet-and-call | 0 | 10 | **+10** |
| river: checked to hero, zero aggression | 0 | 20 | **+20** |
| river: checked to hero after agg=2 earlier | 4 | 18 | +14 |

## Why the distribution is wrong

The reconstructed 200 hands came from heuristic self-play where the AI rarely produced sandwich/closing scenarios (bet-and-call before hero acts) because the action generator favoured one-villain-at-a-time decisions. The 185 BP-series factory hands were designed for specific spots but also never generated multi-caller action.

As a result, every training hand has `num_callers_to_bet=0`. The model is told 'this feature exists' but shown exactly one value — it's a dead column.

Similarly, cumulative turn aggression (agg=2) never appears, so the model cannot learn that a second barrel narrows range more than a first barrel.

## Expected realistic 3-way postflop distribution (poker first principles)

In a 3-way single-raised pot, postflop decisions break down roughly:

| Pattern family | Rough frequency | Why |
|---|---|---|
| Flop: PFA c-bets, first defender decides | ~18% | Standard c-bet spot |
| Flop: bet-and-call, closer decides | ~10% | Classic sandwich/closing — range-narrowing peak |
| Flop: checked to hero | ~9% | Mostly OOP or non-PFA IP |
| Flop: donk-bet faced by PFA | ~4% | Rare but meaningful (BB leads) |
| Flop: bet-and-raise | ~3% | Check-raises and bet-raises |
| Turn: second barrel (agg cumulative = 2) | ~9% | Canonical barrel-or-give-up spot |
| Turn: first aggression after checked flop | ~8% | Delayed stab |
| Turn: checked to hero (flop checked through) | ~6% | OOP BB/SB leads or checks |
| Turn: bet-and-call, closer decides | ~5% | Turn sandwich |
| Turn: bet-and-raise / check-raise | ~3% | Rare but heavy |
| River: check-through line, hero decides | ~10% | After capped action |
| River: facing bet after agg=2 line | ~8% | Triple-barrel resistance |
| River: bet-and-raise | ~4% | Near-nuts signal |
| River: bet-and-call | ~3% | Sandwich/closing river |

## Proposal: supplement 206 targeted hands

Rather than relabel the existing 385 (expensive — we already ran 6 teams through them), supplement with ~206 new hands generated specifically to fill missing archetypes.

**Supplement composition:**

| Archetype | Hands needed |
|---|---:|
| Flop bet-and-call (sandwich/closing) | 40 |
| Turn facing bet cumulative agg=2 | 35 |
| Turn bet-and-call | 20 |
| River checked to hero zero agg | 20 |
| Flop donk-bet facing PFA | 15 |
| River facing single bet after agg=2 | 15 |
| Flop facing single bet (more support) | 15 |
| River checked after agg=2 earlier | 14 |
| Turn facing single bet agg=1 | 12 |
| River bet-and-call | 10 |
| Flop bet-and-raise | 8 |
| Turn bet-and-raise | 2 |
| **Total** | **206** |

## Pipeline implications

1. **Generator must be upgraded** to produce multi-caller action. Current self-play pipeline decides hands in a one-villain-at-a-time sequence that collapses `num_callers_to_bet` to 0. Fix: on each street, iterate through all active villains before asking hero.

2. **Cumulative aggression_count must be tracked across streets**. Currently feature may reset per street — verify in the extractor. If it resets, change to cumulative so turn agg=2 means 'PFA c-bet flop, called, PFA barrels turn'.

3. **`num_callers_to_bet` may need feature audit** — even if we add sandwich hands, if the extractor still writes 0 the pipeline is broken, not just the data.

4. **Labelling budget for supplement**: 206 hands × 4 teams × ~10 per batch = ~83 labelling agent-calls. Plus T5-T6 discovery (21 agents × 2 = 42). Plus Pass 2 review on splits (~8 reviewers). **Total ~133 agents** for the supplement.

## Recommendation

Log this as v2.3 prerequisite work. v2.2 can ship with the current 385 and the attn_* flags; the oracle will have limited signal on num_callers_to_bet (essentially a noop column), and weaker signal on cumulative aggression. The supplement is not blocking v2.2 but is **mandatory before v2.3** if we want the model to learn range-narrowing from caller count.

**Alternative**: if v2.2 production performance is weak on bet-and-call sandwich spots, pull those ~75 hands forward as a v2.2.1 supplement instead of waiting for v2.3.
