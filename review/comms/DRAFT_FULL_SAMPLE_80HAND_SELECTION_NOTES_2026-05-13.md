# Full Sample Selection Notes — 80 Hand Re-Label Consistency Audit (2026-05-13)

## Purpose

Construct the 80-hand full stratified sample for the Phase 2-F re-label
consistency audit (`DRAFT_SPEC_RELABEL_CONSISTENCY_AUDIT_v1_2026-05-13.md`).
The sample re-labels under v3.5 prompt + AMENDMENT 3 and measures drift
vs the current 4-way consensus from batches 001-007.

## Source

Same as pilot: `data/4way_corpus/full_700/batch_001..007` —
- 350 input hands across 7 batches (`batch_NNN_50hand.jsonl`)
- 337 consensus rows (`batch_NNN_consensus.jsonl`) after owner-arb removal
- 265 postflop in-consensus rows form the sampling universe
  (preflop rows and rows without a consensus_action excluded)

## Seed and reproducibility

`SEED = 20260513` (identical to pilot agent — today's date as int).
All ranking uses lexicographic tuple ordering with `spot_id` ascending
as the final tie-break, so the algorithm is deterministic without
invoking any RNG (the pilot agent's SELECTION_NOTES describes a
`random.Random(SEED)` for shuffles, but the Stage B free-pick logic in
practice converges to the spot_id tie-break once the four coverage axes
saturate — making the residual picks RNG-independent given the SEED).

Re-running `python3 /tmp/build_full_sample.py` against the same corpus
snapshot yields byte-identical output. The script lives in `/tmp/` per
the orchestrator's instruction; only `review/comms/` artifacts ship.

## Schema handling — batch_001 vs batch_002..007

`batch_001_consensus.jsonl` uses key `consensus_state`; batches 002..007
use `state`. The loader resolves either form via
`rec.get('consensus_state') or rec.get('state')`, then derives agreement
from `sonnet_votes` directly (state-key independent).

## Algorithm — pilot-pinned anchor + least-represented-first extension

To guarantee the strict-subset property (pilot ⊂ full) by construction,
we **pin** the 20 pilot spot_ids (loaded from the committed
`DRAFT_PILOT_SAMPLE_20HAND_2026-05-13.jsonl`) as the first 20 picks of
the 80-hand sequence, then deterministically pick 60 more by
least-represented-first scoring.

**Coverage counter initialization (from the 20 pilot picks):**
- `batch_count`: per-batch pick count after the 20 pilot picks
- `position_count`: per-position pick count after the 20 pilot picks
- `context_count`: per-action_context count after the 20 pilot picks
- `texture_count`: per-board_texture count after the 20 pilot picks
- `street_count`: per-street count after the 20 pilot picks

**Stage B scoring (per remaining pick):**
Each iteration, sort each remaining (universe minus picked) hand by
the lexicographic tuple:
```
(batch_count[h.batch], position_count[h.pos], context_count[h.ctx],
 texture_count[h.tex], street_count[h.street], -is_split, h.spot_id)
```
Pick the lowest-ranked hand (least-represented batch, then least-
represented position, etc.). Counters update after every pick.
`is_split` flipped to negative biases ties toward split (drift-likely)
hands per audit spec §3. `spot_id` ascending breaks all final ties.

**Why least-represented-first.** The pilot agent's algorithm was a
two-stage stratified round-robin (Stage A: 2-picks-per-batch quota with
split/unanimous pairing; Stage B: free picks scored by new-axis flags).
That two-stage form is brittle when extending: re-running Stage A with
an 80-hand quota (≈11/batch) would not preserve the pilot's exact picks;
continuing only Stage B free-pick logic past saturation degenerates to
spot_id ascending order (pulling everything from batch_001/002).

Least-represented-first generalizes the pilot's intent to any sample size
with one consistent rule:
  1. Guarantees pilot ⊂ full by construction (pilot picks are pinned;
     extension only adds new picks).
  2. Maintains per-batch balance (~10-12 picks/batch at 80) and per-axis
     balance simultaneously, instead of saturating-then-degenerating.
  3. Reproduces byte-identical output across re-runs (deterministic
     given the spot_id tie-break; no RNG dependence past coverage init).
  4. Preserves the audit spec §3 chi-square gate intent, verified post-
     hoc below.

**Note on deterministic-without-RNG.** The pilot SELECTION_NOTES
describes a `random.Random(SEED)` for shuffles, but in practice the
Stage B logic resolves all ties via `spot_id` ascending — the RNG never
changes the output. The 80-hand extension uses the same deterministic
tuple sort; `SEED=20260513` is retained as a documentation constant.

## Strict-subset verification (pilot ⊂ full)

All 20 pilot spot_ids (from `DRAFT_PILOT_SAMPLE_20HAND_2026-05-13.jsonl`)
appear in the 80-hand full sample. The script asserts this
set-equality at build time:

```
assert set(pilot_ids_list).issubset(full_ids), 'pilot ⊂ full FAILED'
```

Result: **PASS** (this run).

## Chi-square stratification preservation proof

Audit spec §3.2 requires that the 20-hand pilot's 4-D (position × context
× street × texture) cell distribution be statistically indistinguishable
from a quarter-scale draw from the 80-hand full sample (chi-square
goodness-of-fit, p > 0.05).

Applied test: chi-square goodness-of-fit with observed = pilot per-cell
counts; expected = (pilot_n / full_n) × full_count = full_count / 4.
Standard practice: cells with expected count < 1 are pooled into a
single 'rare' bucket to avoid divisor inflation.

- chi² statistic = **5.550**
- effective degrees of freedom = 7
  (8 effective buckets from 32 populated cells)
- minimum expected per-cell count (pre-pool) = 0.250
- chi² critical value (p=0.05, dof=7) = 14.067
- chi² < critical: TRUE
- decision: **STRATIFICATION PRESERVED (p > 0.05)**

The audit spec §3.2 preservation gate is satisfied: the pilot is a
stratification-representative quarter-scale draw from the full sample.

## Per-cell distribution (full vs pilot)

| cell (pos / ctx / street / texture) | full | pilot | expected (full/4) |
|---|---|---|---|
| BB / facing-bet / turn / monotone | 5 | 1 | 1.25 |
| BB / facing-bet / turn / paired | 3 | 0 | 0.75 |
| BB / facing-bet / turn / two_tone | 2 | 1 | 0.50 |
| BTN / facing-bet / flop / monotone | 1 | 0 | 0.25 |
| BTN / facing-bet / flop / paired | 1 | 0 | 0.25 |
| BTN / facing-bet / flop / rainbow_dry | 1 | 0 | 0.25 |
| BTN / facing-bet / flop / two_tone | 4 | 0 | 1.00 |
| BTN / opener / flop / paired | 2 | 0 | 0.50 |
| BTN / opener / flop / rainbow_dry | 1 | 1 | 0.25 |
| CO / facing-bet / flop / paired | 1 | 0 | 0.25 |
| CO / facing-bet / flop / rainbow_dry | 4 | 2 | 1.00 |
| CO / opener / flop / paired | 3 | 2 | 0.75 |
| CO / opener / flop / rainbow_dry | 2 | 2 | 0.50 |
| EP / opener / flop / rainbow_dry | 1 | 0 | 0.25 |
| EP / opener / flop / two_tone | 7 | 0 | 1.75 |
| EP / opener / turn / rainbow_dry | 2 | 1 | 0.50 |
| HJ / facing-bet / flop / rainbow_dry | 4 | 0 | 1.00 |
| HJ / opener / flop / rainbow_dry | 3 | 2 | 0.75 |
| HJ / opener / flop / two_tone | 3 | 0 | 0.75 |
| MP / facing-bet / flop / paired | 1 | 1 | 0.25 |
| MP / facing-bet / flop / rainbow_dry | 2 | 1 | 0.50 |
| MP / facing-bet / flop / two_tone | 2 | 1 | 0.50 |
| MP / opener / flop / paired | 2 | 0 | 0.50 |
| MP / opener / flop / rainbow_dry | 1 | 0 | 0.25 |
| MP / opener / flop / two_tone | 2 | 1 | 0.50 |
| SB / facing-bet / flop / rainbow_dry | 4 | 1 | 1.00 |
| SB / facing-bet / flop / two_tone | 3 | 1 | 0.75 |
| SB / opener / flop / paired | 3 | 1 | 0.75 |
| UTG / opener / flop / two_tone | 4 | 1 | 1.00 |
| UTG / opener / turn / paired | 3 | 0 | 0.75 |
| UTG / opener / turn / rainbow_dry | 2 | 0 | 0.50 |
| UTG / opener / turn / two_tone | 1 | 0 | 0.25 |

## Caveats (carried over from pilot SELECTION_NOTES)

Properties of the 4-way corpus itself, NOT sampler bugs:

1. **No river hands.** Corpus contains flop + turn only; river generation
   is gated behind D5 per the blueprint memo. Spec §2.1's third street
   value cannot be exercised by this audit.
2. **No facing-raise hands.** All postflop `facing_bet=1` rows price at
   ≤45% pot-before-call. Spec §2.1's third action_context value is
   structurally empty in the source corpus.
3. **Position/texture skew** inherited from source: CO-heavy positions,
   rainbow_dry-heavy textures, monotone rare.

These caveats reduce the effective stratification space from the
spec's 6×3×3×4=216 cells to 32 populated cells (~14%).

## Files emitted

- `DRAFT_FULL_SAMPLE_80HAND_2026-05-13.jsonl` — 80 input records, sorted by spot_id
- `DRAFT_FULL_SAMPLE_80HAND_INDEX_2026-05-13.md` — markdown table + coverage + chi² summary
- `DRAFT_FULL_SAMPLE_80HAND_SELECTION_NOTES_2026-05-13.md` — this file

## Reproducibility statement

Produced by `/tmp/build_full_sample.py` with `SEED=20260513` against
the corpus snapshot at the working-tree HEAD of
`builder-phase2-e-full-batch8-2026-05-12` (commit-equivalent state with
`orch/phase2f-drafts-2026-05-13` for the pilot input). The 20-hand pilot
is verified as a strict subset by spot_id set equality (assertion in
the script).
