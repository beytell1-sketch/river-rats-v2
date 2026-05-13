# Pilot Sample Selection Notes — 2026-05-13

## Purpose
Construct a 20-hand stratified pilot for the Phase 2-F re-label consistency
audit. We will re-label these 20 hands with the v3.5 prompt amendment and
measure drift vs the current 4-way consensus.

## Source
`data/4way_corpus/full_700/batch_001..007` — 7 batches, 350 input hands.
Consensus files contain 337 rows total (13 hands removed via owner-arb queue).
After dropping `street=preflop` and any input rows without a consensus row,
the postflop universe sampler operates on is **265 hands**.

## Seed
`SEED = 20260513` (today's date as integer).
All shuffles use `random.Random(SEED)`. Tie-breaks fall back to ascending
`spot_id` to guarantee bit-identical reproducibility across re-runs.

## Stratification axes
| axis           | values used in corpus                                         |
|----------------|---------------------------------------------------------------|
| batch_id       | batch_001..batch_007 (7 values)                               |
| hero_position  | BTN, CO, HJ, MP, UTG, EP, SB, BB (8 values)                   |
| action_context | opener, facing-bet, facing-raise (derived; see below)         |
| street         | flop, turn, river (river EMPTY in this corpus)                |
| board_texture  | rainbow_dry, two_tone, paired, monotone (derived from flop)   |
| agreement      | 5/5 (unanimous) vs 4/1 / 3/2 / 2-2-1 (split)                  |

## Derivation logic

**`board_texture`** computed from the first 3 board cards (flop). Turn-street
hands inherit their flop's texture. Rules: monotone if all 3 suits identical,
paired if any rank repeats, two_tone if exactly 2 suits match, else rainbow_dry.

**`action_context`** derived from `facing_bet` and the to_call / pot-before-call
ratio:
  - `facing_bet=0` postflop => `opener` (hero first-to-act)
  - `facing_bet=1`, to_call <= 45% of pot-before-call => `facing-bet`
  - `facing_bet=1`, to_call >  45% of pot-before-call => `facing-raise`

**`agreement`** computed from `sonnet_votes` (5-vote list). 5/5 = unanimous;
4/1 and 3/2 = split (more likely to drift on re-label, per task brief).

## Algorithm

Two-stage stratified round-robin with deterministic tie-breaks:

**Stage A — per-batch quota (14 picks).** For each of the 7 batches, pick 2
hands. Within a batch, candidates are ranked by (unseen-position, unseen-
context, unseen-texture, spot_id), then if the first pick was unanimous we
try to make the second pick a split hand (and vice versa). This guarantees
the >= 2-per-batch requirement and seeds initial position/context/texture
diversity.

**Stage B — 6 free picks.** Score each remaining hand by:
  `(new_position, new_context, new_street, new_texture, is_split)`
Pick the max-scoring hand each iteration, with `spot_id` as the final
tie-break. Coverage sets update after every pick so later picks fill
gaps the earlier ones missed.

## Caveats — populated-stratum gaps

These are properties of the 4-way corpus itself, NOT sampler bugs:

1. **No river hands.** Corpus contains 248 flop + 28 turn + 0 river hands.
   The "river" stratum is empty. The 1.5-D.4 v9-3way pipeline only labels
   flop+turn spots in the current curriculum; river generation is gated
   behind D5 (deferred per blueprint memo).

2. **No facing-raise hands.** All 102 postflop facing-bet rows price at
   ~23-35% of pot-before-call (a single oracle-aligned flop or turn bet).
   No `bet+raise` sequences exist in the corpus, so the "facing-raise"
   stratum is also empty. Sample is therefore drawn from the opener +
   facing-bet contexts only.

3. **Position skew.** Postflop counts: CO=75, BTN=45, MP=42, SB=39, UTG=27,
   HJ=21, BB=14, EP=13. Sampler covers as many positions as 20 picks allow
   but cannot guarantee all 8 with only ~2.5 slots free per position after
   the batch quota.

4. **Texture skew.** Postflop counts: rainbow_dry=139, two_tone=107,
   paired=23, monotone=7. Monotone may receive 0 picks in some seeds.

5. **Some `state` field is named `state`, not `consensus_state`.** Only
   batch_001 uses the new key; batches 002-007 use the legacy `state`.
   Sampler treats them as identical (loader reads `sonnet_votes` directly
   rather than relying on the rolled-up state label).

## Reproducibility
Re-running `python3 /tmp/build_pilot_sample.py` with the same corpus snapshot
and `SEED=20260513` will emit byte-identical artifacts (verified: spot_ids are
sorted in the final JSONL/MD).

## Coverage proof
See `DRAFT_PILOT_SAMPLE_20HAND_INDEX_2026-05-13.md` "Coverage summary" section.
Populated-stratum coverage is enumerated there.
