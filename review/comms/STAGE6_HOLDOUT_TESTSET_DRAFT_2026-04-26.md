---
date: 2026-04-26
from: Main terminal (orchestrator) — DRAFT
to: Owner · Independent GTO expert pool · ML-architect
re: Stage 6 held-out test set construction protocol — independent authoring with non-overlap guarantees vs reference / calibration / pilot
status: DRAFT v0.1 — orchestrator structural framework; awaits independent GTO pool + ML-architect + owner review
---

# Stage 6 Held-Out Test Set Construction — DRAFT v0.1

## Purpose

The Stage 6 ship gate currently has 5 litmus tests (calibration
anchor + standard reference-set + air litmus + value litmus +
self-play systemic) per `MASTER_PLAN (1).md`. Per the locked Stage
4 plan (`ee3d9f5`), Stage 6 adds:

7. **Held-out test set** — ~50 hands constructed during Stage 3.5 +
   Stage 4, never seen by labelling teams or training pipeline.
   Single-shot accuracy measurement; no iteration. Final gate check.

This draft specifies the construction protocol.

## Why a held-out test set

The current 40-hand reference set has been **seen by labelling teams
during calibration** (it's the calibration exam corpus minus a few
holdouts). It's also been **referenced during Stage 3.5 sidecar
authoring** (every FB-* and MW-* slot maps to a reference hand). And
it's been the **headline accuracy metric** the project iterates
against.

Reference-set accuracy is therefore subject to subtle over-fitting:
labellers tune their reasoning to match reference labels even when
not consciously trying. Each iteration of the prompt (v3 → v3.1 →
v3.2 → ...) implicitly optimises against what scores well on the 40
hands.

The held-out test set is the antidote: hands the labellers + training
pipeline have NEVER seen until the moment the model is run against
them. Single-shot accuracy. No "let's tweak the prompt and re-run."

## Authorship

**Authored by: Independent GTO expert pool.** Per locked Stage 4 D3:
"Held-out test set authorship: independent GTO expert pool. Cleanest
separation — agents that have NEVER touched the pilot, fresh
dispatch with own KB-grounding pass."

Specifically: a fresh dispatch of gto-expert (or general-purpose-with-
persona-fallback) on a session-launch that has NOT participated in:

- Stage 4 pilot labelling (Protocol A / B / C agents)
- Stage 4 reviewer pool
- Stage 4 adjudication panel
- Pass 1 labelling teams (T1-T4)
- v3.1 / v3.2 prompt authoring

The independent author dispatches work from a clean slate KB-read
on `knowledge/three_way_gto.md` + the existing reference set as a
shape exemplar (NOT to copy answers from). They author NEW hands
with NEW situations.

## Authorship constraints

### Construction targets

- **Total hands:** 50
- **Stratification across the 8 MUST #49 shape categories:** 6-7 per
  category
- **Action distribution targets** (rough; not strict):
  - FOLD: ~8-10 hands
  - CHECK: ~10-12 hands
  - CALL: ~8-10 hands
  - BET (small + medium + large): ~12-15 hands
  - RAISE: ~6-8 hands
- **Confidence band distribution:** target ~60% HIGH, ~30% MEDIUM,
  ~10% LOW. The held-out test set should INCLUDE close spots so
  it tests model performance on hard hands, not just easy ones.

### Non-overlap guarantees

The constructed hands MUST NOT overlap with:

1. **Reference set (40 hands):** existing reference-set hand IDs are
   tracked. Author cross-checks every constructed hand against the
   reference set — same hero hole cards + same board + same action
   history = duplicate. Reject and re-construct.

2. **Calibration set (24 hands):** same check.

3. **Stage 4 pilot corpus (100 hands):** same check.

4. **Stage 4 full corpus (~600 hands minus DROPs):** same check.

5. **v2.x training corpora:** same check.

[**INDEPENDENT POOL REVIEW NEEDED:** the cross-check needs a tool —
something that hashes (hero cards, board, action history) and
detects collision. Independent pool to author the de-dup tool or
verify against a manifest of all prior hands.]

### Construction process per hand

1. **Sample a shape category** from the 8 MUST #49 categories,
   weighted to hit the stratification target.
2. **Generate a NEW situation** that matches the shape: hero hole
   cards + board + action history that produces the chain-narrowing
   path for that shape.
3. **Cross-check non-overlap** against all 5 corpora above.
4. **Compute features** via `extract_all_features()` to verify the
   feature vector is well-formed (no NaN unless a sentinel triggers,
   composition triple sums to ≈1.0, etc.).
5. **Author label** via the gto-expert's poker reasoning — NOT
   copying from reference / calibration / pilot answers (which the
   independent pool hasn't seen anyway).
6. **Author confidence band** based on how close the spot is.
7. **Author reasoning trace** in the same format as Stage 4
   labelling output.

[**INDEPENDENT POOL REVIEW NEEDED:** automation level — full agent
authoring vs human-in-the-loop check on each hand. Higher automation
= faster but riskier on quality. Owner / independent pool to decide
trade-off.]

### Verification before locking the held-out set

Before the held-out set is locked (NEVER to be modified after):

1. **Solver verification on a sample.** Run solver on 10 randomly-
   sampled hands per `feedback_solver_findings.md` + `feedback_solver_aligned_sizing.md`.
   Flag any sample where solver disagrees with author's label (>20%
   action distribution gap = mismatch). Adjudicate per Stage 4
   adjudication panel.

2. **Independent reviewer pass.** Different gto-expert dispatch
   reviews all 50 hands' labels + reasoning traces. Flag concerns;
   adjudicate.

3. **Distribution check.** Verify the 50 hands hit the stratification
   target + action distribution + confidence band targets within
   tolerance (±2 hands per stratum).

4. **Hash + lock.** Compute SHA256 of the held-out test set JSONL.
   Commit to repo with frontmatter recording the hash. ANY future
   modification to the held-out set bumps the hash and is treated as
   a NEW test set (not a "fix" to the existing one).

## Usage protocol

### Single-shot evaluation

When v2.4 candidate model is ready (post-Stage 5):

1. Load held-out test set
2. Run model inference on all 50 hands (no human in the loop;
   automated)
3. Score against held-out labels
4. Report accuracy + per-shape-category breakdown + per-confidence-
   band breakdown

**No iteration.** If v2.4 candidate scores poorly on held-out: the
candidate is rejected, NOT the held-out set. Investigate via Stage
5 multi-seed audits + Stage 4 corpus quality checks. Don't tweak
the held-out set "to make v2.4 look good."

### Held-out hand exposure

After the single-shot evaluation, the held-out hands MAY be added to
the labelling corpus for v2.5+ (since the test value is exhausted —
once a hand has been measured against, it can't be a held-out test
again).

For v2.4 specifically, the held-out set is **single-use**.

## Disposition for v2.5+

For v2.5 ship, a NEW held-out test set is constructed. The v2.4
held-out hands move into the training corpus (if owner approves)
or get archived. The new held-out set is constructed with the same
authorship + non-overlap protocol against the v2.5-era corpora.

[**OWNER REVIEW NEEDED:** disposition policy for spent held-out
hands. Owner to confirm move-to-training vs archive.]

## Author note

DRAFT v0.1. Structural framework + non-overlap rules + verification
discipline locked in. Poker-judgment specifics (action distribution
targets, confidence band targets, automation level, sample size for
solver verification) flagged for independent pool + owner review.

Production path: `STAGE6_HOLDOUT_TESTSET_v1.0.md` after fill-in and
review chain.

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` — Stage 4
  plan §7 specifies the held-out set as a Stage 6 addition
- `MASTER_PLAN (1).md` — existing Stage 6 ship gate (5 litmus tests)
- `LABELLING_PIPELINE.md` — calibration exam construction (similar
  authoring discipline)
- `feedback_solver_findings.md` — solver verification protocol
- `feedback_solver_aligned_sizing.md` — bet sizes for solver
  verification
