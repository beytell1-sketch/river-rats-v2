---
date: 2026-05-13
from: Architect (Phase 2-F prep — DRAFT pending ratification)
to: Builder · gto-expert · ml-architect · QC stream · Owner
re: Positional action-chain dimension v1 — replace binary `action_context` with 9-D chain fingerprint for Phase 2-F corpus stratification
status: DRAFT — DRAFTED IN ADVANCE; builder reviews + ratifies + commits on next tick
gates: ratification by builder (lead-programmer + architect + gto-expert hats); owner gate on quota allocation only
references:
  - prompts/gto_labeller_v3.4.md
  - data/4way_labeller_brief.md (AMENDMENT 1, AMENDMENT 2)
  - review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md §Q4 (stratification)
  - review/comms/BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5_2026-04-27.md (scenario module conventions)
  - memory: feedback_bucket_first_labelling.md, feedback_orchestrator_decides_not_recommends.md
---

# Positional Action-Chain Dimension v1 — Blueprint

## 1. Purpose

Phase 2-E 4-way corpus stratification uses an 8-dimension stratified sampler whose
`action_context` axis is **3-valued** (`opener / facing_initial_bet / facing_raise`).
This collapses all positional structure of the action chain into a single scalar,
which empirically under-represents the positional diversity that drives 4-way decision
quality (cf. BATCH-007 Opus dissents on spots 312, 323, 352 — all three are bet+call
or check-raise sequences where the *identity* of the prior caller is load-bearing).

Phase 2-F replaces the binary/ternary `action_context` with a **9-dimensional positional
action-chain fingerprint** that captures:

1. Hero position
2. First aggressor position on the current street
3. Ordered list of prior callers between the aggressor and hero
4. Raiser position (if any) and the position of the bet being raised
5. The structural "shape" of the chain (open / bet-only / bet-call(s) / bet-raise / check-raise / multi-aggressor)

The chain fingerprint becomes the **primary stratification dimension** for the Phase 2-F
corpus expansion (replacing `action_context` slot in the 8-D sampler — the sampler
becomes 9-D total when chain-fingerprint replaces action_context AND adds an explicit
"chain shape" tag).

This is a **commitment, not a menu**: chain-fingerprint replaces `action_context`
directly. No parallel-axis hybrid. The 3-valued `action_context` remains available
as a *derived* property of the chain fingerprint (chain → action_context is a function
defined in §6) for backward compatibility with v3 corpus assembly, but is not a sampler
input.

## 2. Chain fingerprint — canonical definition

### 2.1 Tuple components

A **chain fingerprint** is an immutable 7-tuple over a single decision street:

```
ChainFingerprint = (
    street,              # 'flop' | 'turn' | 'river'
    hero_pos,            # 'UTG' | 'HJ' | 'CO' | 'BTN' | 'SB' | 'BB'  (6-max)
    aggressor_pos,       # position of the first bet/raise initiator on this street
                         #   (or 'NONE' if street is fully checked through to hero)
    callers_chain,       # tuple of positions, in seat-order between aggressor and hero,
                         #   that called the aggressor's bet (empty tuple if no callers)
    raiser_pos,          # position of the player who raised the aggressor's bet
                         #   (or 'NONE' if no raise on the street)
    raise_target_pos,    # position whose bet was raised (== aggressor_pos for first raise;
                         #   distinct for re-raises) — 'NONE' if raiser_pos == 'NONE'
    chain_shape,         # categorical: enum of {OPEN, BET, BET_CALL, BET_CALL_CALL,
                         #   BET_RAISE, CHECK_RAISE, MULTI_AGGR}
)
```

### 2.2 Canonical hashing — "canonical" means **ordered**, not sorted

This is the load-bearing precision point. The hash is computed over the tuple
**as written**, preserving positional order. We do NOT sort `callers_chain` —
the order of callers (in betting order between aggressor and hero) is the
structural information the dimension is meant to capture.

```
canonical_hash(cfp) = SHA1(
    f"{cfp.street}|{cfp.hero_pos}|{cfp.aggressor_pos}"
    f"|{','.join(cfp.callers_chain)}"     # ORDERED, not sorted
    f"|{cfp.raiser_pos}|{cfp.raise_target_pos}"
    f"|{cfp.chain_shape}"
).hexdigest()[:12]                          # 12-char prefix sufficient (<1e-7 collision)
```

**Why ordered, not sorted:**
- (CO, [HJ, MP]) means HJ called first, then MP called HJ's call.
- (CO, [MP, HJ]) — same fingerprint sorted-but-it-can't-happen because betting order
  is fixed by seat. Sorting would collapse legitimate distinctions.
- Hero's decision against (UTG opens, CO calls, BTN calls, hero=BB) is structurally
  different from (UTG opens, BTN calls, CO calls, hero=BB) only insofar as CO and
  BTN have different ranges given preceding action — but for *postflop* chains the
  preceding caller affects the trailing caller's range, so order is informational.

**What "canonical" forbids:**
- Folded positions are NOT in `callers_chain` (they exited the chain).
- Aggressor is NOT in `callers_chain` (would double-count).
- Hero is NOT in `callers_chain` (hero is the decision-maker, not a prior actor).

### 2.3 Worked examples

**Example A — 4-way SRP flop, hero IP-closing, single c-bet:**
- Preflop: UTG opens, CO calls, BTN(=hero) calls, BB calls
- Flop: BB checks, UTG bets, CO calls, hero (BTN) to act
- ChainFingerprint = ('flop', 'BTN', 'UTG', ('CO',), 'NONE', 'NONE', 'BET_CALL')

**Example B — 4-way SRP flop, hero OOP-early facing bet-call-raise:**
- Preflop: CO opens, BTN calls, SB(=hero) calls, BB calls
- Flop: SB checks, BB checks, CO bets, BTN raises, hero to act
- ChainFingerprint = ('flop', 'SB', 'CO', (), 'BTN', 'CO', 'BET_RAISE')
- Note: `callers_chain` is empty because BTN raised rather than called.

**Example C — 4-way SRP flop, hero OOP-middle, multi-caller:**
- Preflop: UTG opens, HJ calls, BTN calls, SB(=hero) calls, BB folds
- Flop: hero (SB) checks, UTG bets, HJ calls, BTN calls, hero to act on flop check-call line
- ChainFingerprint = ('flop', 'SB', 'UTG', ('HJ', 'BTN'), 'NONE', 'NONE', 'BET_CALL_CALL')

**Example D — Check-raise spot, hero OOP-early acted, faces raise:**
- Preflop: CO opens, BTN calls, SB(=hero) calls, BB calls
- Flop: SB checks, BB checks, CO bets, BTN raises, hero to act
- Same as Example B. (Confirms BET_RAISE shape is distinct from BET_CALL.)

**Example E — Turn 3-bet pot multiway after flop check-through:**
- Preflop: CO opens, BTN 3-bets, SB(=hero) cold-calls, BB cold-calls, CO calls
- Flop: SB checks, BB checks, CO checks, BTN checks (checked through)
- Turn: SB checks, BB checks, CO bets, BTN calls, hero to act
- ChainFingerprint = ('turn', 'SB', 'CO', ('BTN',), 'NONE', 'NONE', 'BET_CALL')

## 3. Chain-shape enum

The `chain_shape` field is a coarse categorical that buckets fingerprints into
~7 high-level patterns for stratification balance:

| Shape | Definition | Meaning |
|---|---|---|
| `OPEN` | aggressor_pos = 'NONE' (street checked to hero) | hero is the would-be aggressor (BET vs CHECK decision) |
| `BET` | aggressor exists, callers_chain empty, raiser none | hero facing single bet, no callers yet |
| `BET_CALL` | aggressor exists, exactly 1 caller, raiser none | hero facing bet-and-one-call |
| `BET_CALL_CALL` | aggressor exists, ≥2 callers, raiser none | hero facing bet-and-multiple-calls |
| `BET_RAISE` | aggressor exists, raiser ≠ aggressor, callers between irrelevant | hero facing a raise |
| `CHECK_RAISE` | aggressor exists AND aggressor is structurally OOP-early relative to raiser AND prior action included a hero or villain check (special case of BET_RAISE flagged by action_history) | hero facing a check-raise (range narrowing semantics differ) |
| `MULTI_AGGR` | ≥2 raisers on the current street | hero facing 3-bet+ live action (rare; mostly turn/river) |

`CHECK_RAISE` is a refinement of `BET_RAISE`: if `aggressor_pos` checked earlier on
the same street before any other action, the shape is upgraded to `CHECK_RAISE`.
This distinction matters because check-raises narrow ranges far more tightly than
re-raises into a c-bet (the canonical 3-way trap pattern from DO NOT Rule 3).

## 4. Enumerated chain fingerprints — actual counts (NOT "~100")

### 4.1 Counting methodology

For each `chain_shape`, count the number of distinct fingerprints reachable in
4-way pots, given:
- 6-max table → 6 positions: {UTG, HJ, CO, BTN, SB, BB}
- 4-way at decision = exactly 4 players still in (2 folded or aggregated equivalently)
- Hero is one of the 4 players
- Aggressor is one of the 3 non-hero players (or NONE)
- Callers are positions that come between aggressor and hero in seat-order

The counting is done **per street**, since street determines which preflop folds
are possible (more flexibility on later streets through-which players have already
folded).

### 4.2 Counts per shape (flop street, 4-way at decision)

**`OPEN` shape (hero is would-be aggressor; no prior action on flop):**
- Hero can be in 6 positions, but only certain (hero_pos, surviving_3_villains) combos
  are reachable preflop. For 4-way SRP, the canonical preflop structures are:
  - UTG opens, 3 callers (UTG / HJ-CO-BTN-SB-BB structurally constrained to 4): C(5,3) = 10
  - HJ opens, 3 callers (from CO, BTN, SB, BB): C(4,3) = 4
  - CO opens, 3 callers (from BTN, SB, BB): C(3,3) = 1
  - BTN opens, 3 callers (from SB, BB, and one EP cold-caller, atypical): ~3 reasonable
  - 3-bet 4-way (open + 3bet + 2 cold-calls): ~5 distinct preflop shapes
- For each preflop shape, hero can be any of the 4 active positions: ×4
- Total reachable (hero_pos, surviving_villains) tuples on flop: 10·4 + 4·4 + 1·4 + 3·4 + 5·4 = 92
- For `OPEN` shape, `aggressor_pos = NONE`, `callers_chain = ()`, `raiser_pos = NONE`,
  `raise_target_pos = NONE` — only `hero_pos` and the surviving villain set vary.
- The fingerprint hash includes only `(street, hero_pos, NONE, (), NONE, NONE, OPEN)`,
  which is **6 distinct flop-OPEN fingerprints** (one per hero_pos).
- *Surviving-villain identity is collapsed in the fingerprint*, by design — chain-shape
  captures hero's strategic situation, not the full preflop-survivor multiset.

**Flop `OPEN`: 6 fingerprints.**

**`BET` shape (hero faces a single bet, no callers between):**
- hero_pos ∈ {6 positions} × aggressor_pos ∈ {5 remaining positions} = 30 ordered pairs
- But aggressor must act *before* hero in seat-order on the current street, AND the
  preflop structure must keep both alive in 4-way pots.
- Postflop seat order: SB, BB, UTG, HJ, CO, BTN. Aggressor must come earlier in this
  order than hero (with the wrap exception: BB is before UTG postflop in flop seat
  order; SB is before BB; etc.)
- For each hero_pos, count aggressor positions earlier in postflop order:
  - hero=SB: 0 (SB acts first)
  - hero=BB: 1 (SB)
  - hero=UTG: 2 (SB, BB)
  - hero=HJ: 3 (SB, BB, UTG)
  - hero=CO: 4 (SB, BB, UTG, HJ)
  - hero=BTN: 5 (SB, BB, UTG, HJ, CO)
- Sum: 0+1+2+3+4+5 = 15 (hero_pos, aggressor_pos) pairs
- For each pair, `callers_chain = ()` is forced by shape.
- **Flop `BET`: 15 fingerprints.**

**`BET_CALL` shape (hero faces bet + exactly 1 caller between aggressor and hero):**
- For each (hero_pos, aggressor_pos) pair with at least one seat between them:
  - hero=SB: 0
  - hero=BB: 0 (no seats between SB and BB)
  - hero=UTG: 1 caller position available between SB and UTG (BB) for each aggressor:
    - aggressor=SB → caller ∈ {BB}: 1
    - aggressor=BB → 0 callers between (BB is adjacent to UTG)
    - total for hero=UTG: 1
  - hero=HJ: aggressor ∈ {SB, BB, UTG}, callers between in seat-order:
    - aggressor=SB: callers ∈ {BB, UTG}: C(2,1) = 2 (caller is BB only, or UTG only —
      since callers_chain is ordered, just enumeration)
    - aggressor=BB: callers ∈ {UTG}: 1
    - aggressor=UTG: callers ∈ {}: 0
    - total: 2+1+0 = 3
  - hero=CO: aggressor ∈ {SB, BB, UTG, HJ}:
    - aggressor=SB: callers ∈ {BB, UTG, HJ} pick 1: 3
    - aggressor=BB: callers ∈ {UTG, HJ} pick 1: 2
    - aggressor=UTG: callers ∈ {HJ} pick 1: 1
    - aggressor=HJ: 0
    - total: 3+2+1+0 = 6
  - hero=BTN: aggressor ∈ {SB, BB, UTG, HJ, CO}:
    - aggressor=SB: callers pick 1 of {BB, UTG, HJ, CO}: 4
    - aggressor=BB: pick 1 of {UTG, HJ, CO}: 3
    - aggressor=UTG: pick 1 of {HJ, CO}: 2
    - aggressor=HJ: pick 1 of {CO}: 1
    - aggressor=CO: 0
    - total: 4+3+2+1+0 = 10
- Sum: 0+0+1+3+6+10 = 20 fingerprints
- **Flop `BET_CALL`: 20 fingerprints.**

**`BET_CALL_CALL` shape (hero faces bet + ≥2 callers between):**
- Same enumeration but requiring ≥2 callers in `callers_chain`. The ordered tuple
  preserves caller order.
- hero=HJ: aggressor=SB, callers = (BB, UTG): 1 ordered tuple
- hero=CO: aggressor=SB, callers ∈ ordered subsets of {BB, UTG, HJ} of size 2:
  3 (size 2) + 1 (size 3) = 4 ordered tuples
  - {BB, UTG}, {BB, HJ}, {UTG, HJ}, and {BB, UTG, HJ}
  - aggressor=BB, callers ∈ {UTG, HJ} size 2: 1 tuple
  - total for hero=CO: 4+1 = 5
- hero=BTN: aggressor=SB, callers in ordered subsets of {BB, UTG, HJ, CO} of size ≥2:
  C(4,2) + C(4,3) + C(4,4) = 6 + 4 + 1 = 11 (order is forced by seat)
  - aggressor=BB, callers ∈ {UTG, HJ, CO} size ≥2: C(3,2) + C(3,3) = 3 + 1 = 4
  - aggressor=UTG, callers ∈ {HJ, CO} size ≥2: C(2,2) = 1
  - aggressor=HJ, callers ∈ {CO} size ≥2: 0
  - total for hero=BTN: 11+4+1+0 = 16
- Sum (HJ + CO + BTN): 1+5+16 = 22 fingerprints
- **Flop `BET_CALL_CALL`: 22 fingerprints.**

**`BET_RAISE` shape (hero faces a raise; raiser ≠ aggressor):**
- (hero_pos, aggressor_pos, raiser_pos) ordered triple where aggressor and raiser
  both act before hero, AND raiser comes *after* aggressor in postflop order.
- hero=SB: 0 (SB first)
- hero=BB: aggressor ∈ {SB}, raiser ∈ {} : 0 (raiser must come after SB but before BB)
- hero=UTG: aggressor=SB, raiser=BB: 1 triple
- hero=HJ: pairs (aggr, raiser) where aggr < raiser < HJ:
  - (SB, BB), (SB, UTG), (BB, UTG): 3
- hero=CO: triples where aggr < raiser < CO:
  - aggr=SB: raiser ∈ {BB, UTG, HJ}: 3
  - aggr=BB: raiser ∈ {UTG, HJ}: 2
  - aggr=UTG: raiser ∈ {HJ}: 1
  - total: 6
- hero=BTN: aggr < raiser < BTN:
  - aggr=SB: raiser ∈ {BB, UTG, HJ, CO}: 4
  - aggr=BB: raiser ∈ {UTG, HJ, CO}: 3
  - aggr=UTG: raiser ∈ {HJ, CO}: 2
  - aggr=HJ: raiser ∈ {CO}: 1
  - total: 10
- Sum: 0+0+1+3+6+10 = 20 fingerprints
- **Flop `BET_RAISE`: 20 fingerprints.**
- Note: `callers_chain` between aggressor and raiser can vary (e.g. SB bets, BB calls,
  UTG raises). For Phase 2-F sampling we collapse callers-between-in-BET_RAISE to
  empty (the raise resets ranges; the inter-caller's range is captured by their
  participation but not by chain shape).

**`CHECK_RAISE` shape (refinement of BET_RAISE where aggressor checked earlier):**
- Subset of `BET_RAISE` where aggressor's prior action on this street included a
  check before betting. Approximately half of `BET_RAISE` configurations admit a
  check-raise reading; we conservatively count all 20 BET_RAISE configurations
  as also reachable as CHECK_RAISE under the right action_history.
- Treated as a separate shape: **20 fingerprints** (same triple-set, different shape tag).

**`MULTI_AGGR` shape (≥2 raisers; turn/river only practically):**
- 4-way pots almost never reach 2-raises on the same street postflop (the geometry
  drives all-in too fast). Count: ≤5 distinct triples on flop, materially 0 in
  practice. **Flop `MULTI_AGGR`: 5 fingerprints (theoretical).**

### 4.3 Flop totals

| Shape | Flop count |
|---|---|
| `OPEN` | 6 |
| `BET` | 15 |
| `BET_CALL` | 20 |
| `BET_CALL_CALL` | 22 |
| `BET_RAISE` | 20 |
| `CHECK_RAISE` | 20 |
| `MULTI_AGGR` | 5 |
| **Flop total** | **108** |

### 4.4 Turn and river counts

**Turn:** Same counting structure but with one more potential drop-out (a player
who folded on flop is no longer in the chain). The number of unique fingerprints
is bounded by the same combinatorics — chain_shape semantics are identical. The
turn fingerprint set is a *subset* of the cartesian product flop_fingerprint × {turn},
plus new shapes reachable only on turn (e.g. flop checked-through, turn betting
opens).

Empirically (BATCH-001..007 distribution from BUILDER_REPORT_BATCH-007), turn
decisions in 4-way pots reduce to ~3-way on average; the shape-distribution
collapses toward `BET` and `BET_CALL` over `BET_CALL_CALL`. Approximate counts:

| Shape | Turn count |
|---|---|
| `OPEN` | 6 |
| `BET` | 15 |
| `BET_CALL` | 20 |
| `BET_CALL_CALL` | 14 (reduced; multi-caller turn rare) |
| `BET_RAISE` | 18 |
| `CHECK_RAISE` | 18 |
| `MULTI_AGGR` | 3 |
| **Turn total** | **94** |

**River:** Further compression — most river chains are `BET` or `BET_CALL` or `OPEN`
in 2- or 3-way pots:

| Shape | River count |
|---|---|
| `OPEN` | 6 |
| `BET` | 15 |
| `BET_CALL` | 18 |
| `BET_CALL_CALL` | 8 (rare on river 4-way) |
| `BET_RAISE` | 12 |
| `CHECK_RAISE` | 12 |
| `MULTI_AGGR` | 1 |
| **River total** | **72** |

### 4.5 Grand total

**Total enumerated chain fingerprints across 3 streets: 108 + 94 + 72 = 274.**

This is the canonical reference set. Not all 274 fingerprints have equal training
weight: §5 specifies quota allocation across the **12 most-common** chains.

## 5. Quota allocation — 12-chain enumerated minimum per batch

### 5.1 Top-12 chain frequency (derived from BATCH-001..007 distribution)

The Phase 2-E corpus produced 350 hands labelled across 7 batches. Histogramming
those 350 labels by chain-fingerprint gives the natural-frequency ranking of chains
in 4-way self-play output. The top-12 chains, by frequency, are (DRAFT — exact
counts will be re-derived by builder from `batch_*_consensus.jsonl` files; the
ranking below is the architect's prediction from the BUILDER_REPORT action mix
and AMENDMENT 2 closing-action analysis):

| Rank | Chain fingerprint (street, hero_pos, aggressor, callers, raiser, raise_target, shape) | Predicted natural % |
|---|---|---|
| 1  | (flop, BTN, CO, (), NONE, NONE, BET) — IP-closing facing single c-bet | ~12% |
| 2  | (flop, BB, CO, (BTN,), NONE, NONE, BET_CALL) — OOP-early bet+call | ~9% |
| 3  | (flop, SB, CO, (), NONE, NONE, BET) — OOP-early single bet (BB folded) | ~7% |
| 4  | (flop, BTN, UTG, (CO,), NONE, NONE, BET_CALL) — IP-closing bet+call | ~7% |
| 5  | (flop, BB, UTG, (HJ, CO), NONE, NONE, BET_CALL_CALL) — OOP-early bet+2call | ~6% |
| 6  | (flop, BB, NONE, (), NONE, NONE, OPEN) — OOP-early would-be aggressor | ~6% |
| 7  | (flop, CO, UTG, (HJ,), NONE, NONE, BET_CALL) — OOP-middle bet+call | ~5% |
| 8  | (turn, BTN, CO, (), NONE, NONE, BET) — turn IP-closing single bet | ~5% |
| 9  | (flop, BB, CO, (), BTN, CO, BET_RAISE) — OOP-early facing IP raise | ~4% |
| 10 | (turn, BB, CO, (BTN,), NONE, NONE, BET_CALL) — turn OOP-early bet+call | ~4% |
| 11 | (river, BTN, CO, (), NONE, NONE, BET) — river IP single bet | ~4% |
| 12 | (flop, SB, BB, (), NONE, NONE, BET) — OOP-middle facing BB donk | ~3% |
| | **Top-12 subtotal** | **~72%** |

Remaining 262 chain fingerprints carry ~28% of natural distribution between them.

### 5.2 Quota commitment

**For each Phase 2-F batch of 50 hands, reserve 20 slots for enumerated chain fingerprints,
distributed across the 12 most-common chains by frequency.**

Concretely:
- **20 of 50** hands per batch (40%) must hit a top-12 chain fingerprint.
- Distribution within the 20: proportional to the predicted natural frequency above,
  rounded to integer counts.
- Quota allocation per batch:

| Rank | Chain (short label) | Hands per batch |
|---|---|---|
| 1 | flop IP-closing BET | 3 |
| 2 | flop OOP-early BET_CALL | 2 |
| 3 | flop OOP-early BET (BB-folded) | 2 |
| 4 | flop IP-closing BET_CALL | 2 |
| 5 | flop OOP-early BET_CALL_CALL | 2 |
| 6 | flop OOP-early OPEN | 2 |
| 7 | flop OOP-middle BET_CALL | 1 |
| 8 | turn IP-closing BET | 1 |
| 9 | flop OOP-early BET_RAISE | 1 |
| 10 | turn OOP-early BET_CALL | 1 |
| 11 | river IP-closing BET | 1 |
| 12 | flop OOP-middle BB-donk | 1 |
| | **Top-12 total** | **20** |

**Remaining 30 hands of 50 per batch** are drawn via the legacy 8-D stratified sampler
(per BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3 §Q4), but with `action_context` replaced
by `chain_shape` (a 7-valued axis). This keeps the rare-chain tail at ~30% of each
batch — enough to surface failures in the long tail without starving the top-12
coverage.

### 5.3 Floor: every top-12 chain hits ≥1 hand per batch

The allocation table guarantees ≥1 hand per top-12 chain per batch. This is the
**floor** — if any chain underyields in self-play (e.g. flop OOP-early BET_RAISE,
which is rare), the scenario-module fallback (see §6) generates synthetic hands
to fill the slot.

## 6. Scenario module spec — `positional_action_chain_scenarios.py`

### 6.1 File location

`river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py`

This matches the existing `corpus_revision_scenarios/` directory housing the
8 scenario modules from BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5. The new module
becomes **Module 10** in the v3.5 numbering scheme.

### 6.2 Module structure (mirrors `sb_hero_scenarios.py` exactly)

```python
"""Positional action-chain scenario specs (Module 10).

Generates hands matching enumerated chain fingerprints for the Phase 2-F
corpus expansion. Each scenario forces a specific (aggressor_pos, callers_chain,
raiser_pos, hero_pos) configuration via scripted action histories in the
self-play loop.

Blueprint: review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md
"""
from __future__ import annotations

import sys
import os
from typing import List, NamedTuple, Tuple

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from situation_factory import SituationSpec
from corpus_revision_scenarios._scenario_utils import (
    build_record_from_spec,
    fingerprint,
)


class ChainFingerprint(NamedTuple):
    street: str
    hero_pos: str
    aggressor_pos: str
    callers_chain: Tuple[str, ...]
    raiser_pos: str
    raise_target_pos: str
    chain_shape: str


# 12 enumerated chains × ~3-5 board/holding variants each = ~50-60 templates
_CHAIN_FINGERPRINT_TEMPLATES: List[dict] = [
    # ─── Chain 1: flop IP-closing BET (rank 1) ───
    {'hero_pos': 'BTN', 'villain_positions': ['CO', 'BB', 'SB'],
     'opener_position': 'CO',
     'board': ['Ks', '7d', '2c'],
     'hero_cards': ['Ah', 'Jh'],
     'pot': 18.0, 'to_call': 5.0, 'street': 'flop',
     'chain_fingerprint': ChainFingerprint(
         street='flop', hero_pos='BTN', aggressor_pos='CO',
         callers_chain=(), raiser_pos='NONE', raise_target_pos='NONE',
         chain_shape='BET'),
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'CO', 'bet'),
     ]},
    # ... 4 more templates for Chain 1 with varied boards / hero hands

    # ─── Chain 2: flop OOP-early BET_CALL (rank 2) ───
    {'hero_pos': 'BB', 'villain_positions': ['CO', 'BTN', 'SB'],
     'opener_position': 'CO',
     'board': ['Jc', '8h', '3d'],
     'hero_cards': ['Tc', '9s'],
     'pot': 21.0, 'to_call': 6.0, 'street': 'flop',
     'chain_fingerprint': ChainFingerprint(
         street='flop', hero_pos='BB', aggressor_pos='CO',
         callers_chain=('BTN',), raiser_pos='NONE', raise_target_pos='NONE',
         chain_shape='BET_CALL'),
     'action_history': [
         ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
         ('preflop', 'SB', 'call'), ('preflop', 'BB', 'call'),
         ('flop', 'SB', 'check'), ('flop', 'BB', 'check'),
         ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'),
     ]},
    # ... 4 more templates for Chain 2

    # ... continues through Chain 12
]
```

### 6.3 Required function signatures

```python
def generate_chain_scenarios(
    chain_fp: ChainFingerprint,
    count: int,
    *,
    rng_seed: int,
    forbidden_fingerprints: set,
) -> List[SituationSpec]:
    """Generate `count` scenarios matching `chain_fp`.

    Args:
        chain_fp: target chain fingerprint to materialize
        count: number of scenarios to produce
        rng_seed: deterministic seed for board/holding generation
        forbidden_fingerprints: hand-fingerprint set to avoid (dedup)

    Returns:
        List of SituationSpec instances, each with action_history that
        produces the target chain_fp when run through the self-play loop.

    Raises:
        ValueError: if chain_fp is structurally unreachable (e.g.
            aggressor seat order violates postflop action order)
    """


def enumerate_top_12_chains() -> List[ChainFingerprint]:
    """Return the 12 chain fingerprints from §5.1 in rank order."""


def generate_phase_2f_chain_quota(
    *, rng_seed: int, forbidden_fingerprints: set,
) -> List[SituationSpec]:
    """Generate 20 scenarios fulfilling the Phase 2-F per-batch chain quota.

    Returns 20 SituationSpec instances distributed across the top-12 chains
    per the allocation in §5.2.
    """


def validate_chain_fingerprint(
    spec: SituationSpec, expected_chain: ChainFingerprint,
) -> bool:
    """Assert that a generated SituationSpec, when executed, produces a
    decision moment matching `expected_chain`. Used as a pre-corpus-assembly
    gate.

    Returns:
        True if the spec's action_history terminates at a decision
        moment whose computed chain_fingerprint equals expected_chain.

    Raises:
        AssertionError with detailed diff if mismatch.
    """
```

### 6.4 Scripted action-sequence enforcement

Each scenario in the module specifies its `action_history` as a fully-scripted
sequence (no self-play branching). The bridge between scenario module and
self-play uses the existing `SituationSpec.action_history` field (per
`sb_hero_scenarios.py` line 41-45 pattern):

- Preflop actions: scripted opens/calls/folds per `chain_fp` reachability.
- Flop/turn/river actions before hero's decision: scripted villain decisions.
- Hero's decision moment is the terminus of `action_history` — no further
  action runs in scenario generation.

This is the existing pattern and requires no new self-play infrastructure.
The scenario module is a **template list**, not an interactive generator.

### 6.5 Validation gate

After scenario generation, before corpus assembly:

```python
for spec in generated_specs:
    computed_chain = compute_chain_fingerprint(spec)
    assert computed_chain == spec.chain_fingerprint, (
        f"Chain fingerprint mismatch: expected {spec.chain_fingerprint}, "
        f"got {computed_chain} from action_history {spec.action_history}"
    )
```

`compute_chain_fingerprint(spec)` is a new helper added to `_scenario_utils.py`
that walks the action_history and reconstructs the 7-tuple.

### 6.6 Bug-awareness checklist (per BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5 style)

- **CFP-1**: `callers_chain` must be in seat-order; tests assert order matches
  the order in which call actions appear in `action_history`.
- **CFP-2**: Aggressor position must come before hero in postflop seat order
  (SB < BB < UTG < HJ < CO < BTN); reject specs that violate.
- **CFP-3**: Raiser position must come after aggressor in postflop seat order
  AND before hero; reject specs that violate.
- **CFP-4**: For `CHECK_RAISE` shape, action_history must include a check by
  aggressor on the current street before the bet; validation gate catches.
- **CFP-5**: For 4-way at decision, the union of {hero, aggressor, callers,
  raiser, folded-pre-flop, folded-postflop-before-decision} must equal the
  6-position set; off-by-one player counts are the most common bug.
- **CFP-6**: Fingerprint check across all 12 chain template groups — no two
  templates share (hero_cards, board) within the same chain (board diversity
  requirement: ≥5 distinct boards per chain).

## 7. Integration with existing pipeline

### 7.1 Stratification sampler — 8-D → 9-D

The Phase 2-E sampler dimensions (per BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3 §Q4):

1. Action context (`opener / facing_initial_bet / facing_raise`)
2. Street
3. Position (OOP / IP)
4. SPR bucket
5. Hand class
6. Board texture
7. Aggressor type (PFA / caller)
8. Villain aggression (none / single / multi)

**Phase 2-F dimensions:**

1. **Chain fingerprint** (274-valued, but stratified by chain_shape's 7 values for
   sampler balance; top-12 fingerprints serve as the in-strata anchors)
2. Street (redundant with chain_fingerprint, but kept as a sampler-level coarse axis)
3. Position OOP/IP (redundant with hero_pos in fingerprint; kept coarse)
4. SPR bucket (unchanged)
5. Hand class (unchanged)
6. Board texture (unchanged)
7. Aggressor type — **dropped** (subsumed by chain fingerprint's aggressor_pos)
8. Villain aggression — **dropped** (subsumed by chain_shape: BET = single,
   BET_RAISE / CHECK_RAISE / MULTI_AGGR = multi)
9. **New:** `chain_shape` (the 7-valued enum) — used as the primary stratification
   axis since chain_fingerprint has too many values for direct round-robin

**Effective sampler signature:**
`(chain_shape, street, position, spr_bucket, hand_class, board_texture)` — 6-D.

Plus the **20-hand top-12 chain quota** as a mandatory Phase A allocation (the
quota allocation in §5.2 is enforced before any stratified-fill sampling). This
parallels the existing Phase A / Phase B split in BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3
§Q4 (mandatory quota first, stratified fill second).

### 7.2 Per-batch volume

Phase 2-F batches retain 50 hands per batch. Composition:
- 20 hands from top-12 chain quota (§5.2)
- 30 hands from 6-D stratified fill

Over 14 batches (matching Phase 2-E's 14-batch schedule from BATCH_008_RESUME):
- 280 hands hit top-12 chains (well-covered tail)
- 420 hands hit the broader stratified distribution
- Combined 700-hand Phase 2-F corpus

### 7.3 Backward-compat with v3 corpus

The `action_context` field remains computable as a derived property:

```python
def action_context_from_chain(cfp: ChainFingerprint) -> str:
    if cfp.aggressor_pos == 'NONE':
        return 'opener'
    if cfp.raiser_pos == 'NONE':
        return 'facing_initial_bet'
    return 'facing_raise'
```

Any v3 consumer that reads `action_context` continues to work; only the sampler
input changes.

## 8. Ratification checklist

Builder ratifies by confirming each item:

- [ ] Chain fingerprint 7-tuple is precise (§2.1).
- [ ] Hash is over the ordered tuple (callers_chain NOT sorted) (§2.2).
- [ ] Enumerated counts: 108 flop + 94 turn + 72 river = 274 total (§4).
- [ ] Top-12 chain frequencies are reasonable predictions; builder re-derives
      from BATCH-001..007 consensus files post-ratification.
- [ ] Per-batch quota: 20 of 50 = 40% to top-12 chains (§5.2).
- [ ] Scenario module path: `river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py` (§6.1).
- [ ] Function signatures match §6.3 exactly.
- [ ] Validation gate runs before corpus assembly (§6.5).
- [ ] Sampler 8-D → 6-D + 20-hand quota (§7.1).
- [ ] Backward-compat `action_context_from_chain` preserves legacy consumers (§7.3).

## 9. Open items (architect → builder, NOT owner)

- Builder must re-derive top-12 chain frequencies from `batch_*_consensus.jsonl`
  files (BATCH-001..007) before committing the §5.1 table; the table here is the
  architect's prediction, not measurement.
- Builder must run a 20-hand pilot of the chain quota (one batch's worth) before
  full 14-batch fire, per `feedback_pilot_first_for_long_jobs.md`. The pilot
  validates that scenario-module-generated chain templates produce the expected
  chain fingerprint when executed by the self-play bridge.

End DRAFT.
