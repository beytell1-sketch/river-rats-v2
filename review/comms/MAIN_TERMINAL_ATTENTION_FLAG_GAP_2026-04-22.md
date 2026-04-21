---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: v2.4 attention-flag vocabulary expansion — gap missed in Stage 3.5 plan
status: NEW MUSTs #24-#27 added; cross-cuts Stage 2 + Stage 3 + Stage 4 + Stage 5
---

# v2.4 Attention-Flag Vocabulary Expansion — Missed Gap

Owner audit (2026-04-22): the entire 23-MUST Stage 3.5 plan + v2.4
ship sequence misses the attention-flag mechanism. v2.2 trained on
108 columns (54 raw + 54 binary attention flags from the Exp 3
auxiliary mechanism). `attn_draw_outs` was the #1 feature overall in
v2.2. Labellers tag PRIMARY (drove decision) + CONFIRMED (verified,
supports decision) on each hand; those tags become attention-flag
values that XGBoost trains on alongside the raw vector.

v2.4 adds 4 raw blocker features. **No part of the current plan
extends the attention layer to match.** Result: new features ship
with raw values and zero supervised-attention signal — defeats half
the purpose of adding them.

## Verified evidence

`prompts/gto_labeller_v3.1.md:363-420` — current prompt is explicit on
the **54-feature vector**:

> Tag which features from the 54-feature vector drove this decision.
> Two levels:
>   PRIMARY — Without this feature's value, the action might change.
>   CONFIRMED — Checked this feature, its current value supports the action.

> For BET, RAISE, CALL, and FOLD: you MUST tag all 4 villain
> composition features as PRIMARY or CONFIRMED.

Bucket-specific mandatory-tag table at lines 398-413 includes
`flush_block_pct` for the flush-draw bucket. Does NOT include the
4 new v2.4 blocker features.

`training-data/tag_vocabulary.json` — current schema covers
intentions, street_plan_actions, street_plan_responses; the
attention-flag column set is implicit in the 54 → 108 expansion.

`river-rats-core/run_attention_experiments.py` — Exp 3 ran the
54-flag training; mechanism is shipped but not parameterised on
feature-vector size.

## What this changes

The v2.4 ship sequence implicitly expected:
- Stage 3.5 fixes the chain
- Stage 4 re-labels with v3.2 prompt
- Stage 5 retrains v2.4

But Stage 4 cannot produce a coherent training distribution if
labellers can't tag the new features as PRIMARY. And Stage 5 cannot
train a 116-column model if the training CSV only has 108 columns.

This is a 4-MUST cross-cutting fix that touches Stage 2 (KB §1.9),
Stage 3 (v3.2 prompt), Stage 4 (training CSV writer), Stage 5
(trainer feature count).

## NEW MUSTs

### MUST #24 — CRITICAL — Attention vocabulary expansion (Stage 2)

KB §1.9 update (currently in progress) must include the attention-
tag conventions for the 4 new blocker features alongside their
poker semantics. For each new feature, document:

- When this feature is PRIMARY (without it, action might change)
- When this feature is CONFIRMED (checked, supports action)
- Which buckets it's mandatory-tag for
- Concrete examples of each PRIMARY case + each CONFIRMED case

Also: decide the attention vocabulary structure. Two options:
- (a) **1:1 mapping** — every raw feature gets an `attn_<name>` flag
- (b) **Concept vocabulary** — labellers tag from a curated tag list
  that may aggregate or split features by concept

v2.2 used (b) per pilot history: "Union of all 6 teams' tags." The
current `training-data/tag_vocabulary.json` and the prompt's
mandatory-tag table both suggest (a)-leaning structure. Builder
decides + documents in KB; orchestrator approves.

**Manifest dependency:** Stage 2 cannot complete + commit until
KB §1.9 includes attention-tag conventions for all 4 new features.

### MUST #25 — CRITICAL — v3.2 prompt mandatory-tag rules (Stage 3)

v3.2 prompt (derived from KB §1.9) must:

- Update the leading "Tag which features from the **N-feature
  vector**" line to reflect the new vector size (55 or 59 — verify
  against gto_model.FEATURE_COLUMNS at exposure time)
- Add new entries to the bucket-specific mandatory-tag table at
  the v3.1-equivalent of lines 398-413, covering when each new
  blocker feature is mandatory PRIMARY/CONFIRMED
- Add new default-PRIMARY entries to the action-default tables at
  the v3.1-equivalent of lines 415-420
- Provide concrete tagging examples for the new features (one
  PRIMARY example, one CONFIRMED example per feature)

**Manifest dependency:** Stage 3 cannot complete + commit until
v3.2 prompt instructs labellers on tagging all 4 new features.

### MUST #26 — CRITICAL — Training pipeline writes expanded attention columns (Stage 4 prereq)

Whatever produces `v2_4_training.csv` (factory pipeline +
labelling assembly — `assemble_pilot_data.py` v2.2 era; verify
the v2.4 equivalent path during blueprint v2 research) must:

- Capture the new attention-flag columns from labellers' output
- Write them to CSV alongside the existing 54 attention columns
- Document the new column schema (header order, naming convention)
- Audit column for `_attention_vocabulary_version` (v2.2 = "exp3_54flag",
  v2.4 = "v2.4_<NN>flag" or whatever the chosen versioning is)

**Manifest dependency:** Stage 4 re-label cannot start until the
training-CSV writer is verified to capture the expanded attention
set. If the writer drops new flags silently (per the CRITICAL #2
silent-fallback class of risk), the v2.4 training distribution
will be missing the new attention signal entirely — same failure
class as v2.3.2 mixture, different layer.

### MUST #27 — CRITICAL — Trainer consumes expanded vocabulary (Stage 5)

`train_v2_4.py` (or whatever trainer name lands) must:

- Read the new feature count + attention count from the training
  CSV header, not hardcode 108
- Document the v2.4 total: 54 + 4 raw + (existing attention flags)
  + (new attention flags) = projected 116 if 1:1, projected
  variable if (b) concept vocabulary
- The Exp 3 attention-mechanism wiring at
  `river-rats-core/run_attention_experiments.py` must be reviewed
  for v2.4 — the 54-flag count is hardcoded in places per project
  history; new flag count needs end-to-end consistency

**Manifest dependency:** Stage 5 retrain cannot complete + sign off
until trainer is confirmed to consume the expanded vocabulary
without silent column drops.

## Decision the builder owns (decide + document, don't ask)

Per quality default + DECIDE and EXECUTE:

- **Vocabulary structure (a) vs (b)**: builder picks based on what
  the v2.2 implementation actually did + what fits the new blockers.
  Document choice + reasoning in MUST #24's KB §1.9 entry. If (b)
  concept vocabulary: list the new concepts, their fingerprint to
  raw features, the rationale.
- **Numbering convention**: `attn_nut_flush_block` vs
  `attn_blocker_nut_flush` vs whatever — pick consistent with v2.2
  precedent.
- **Backward compat at trainer**: should v2.4 trainer be able to
  load a v2.2 CSV (54 + 54) and zero-pad the new attention columns
  for warm-start? Or does retraining from scratch on the new schema
  forbid backward load? Architecture decision; document.

## Why this surfaces now and not earlier

The Stage 3.5 reconciliation focused on FEATURE-PIPELINE consistency
— labellers seeing chain-correct values. It missed the meta-question
of WHAT labellers tag, only addressing what they see.

Reviewer panel (architecture, GTO, red-team, practical, research) —
none surfaced the attention-flag gap because none of their prompts
framed the labelling pipeline's training-attention output. My
prompts to them said "training distribution" and "model decisions"
and "teaching display"; none said "labellers ALSO produce attention
training labels via tagging."

Memory at `feedback_attention_flags_when_features_change.md` records
the rule for future audits.

## Action

- Builder: incorporate MUSTs #24-#27 into blueprint v2 alongside
  the existing 23 MUSTs. They cross-cut Stage 2/3/4/5 — document
  per-stage dependency in v2's manifest-update section.
- Orchestrator: bumping manifest v1.8 → v1.9 with the new
  per-stage prerequisites.
- No code edits, no Stage 2 commits, no Stage 4 work until
  MUSTs #24-#27 are in scope and reviewed.

## Reference

- `prompts/gto_labeller_v3.1.md:363-420` — current attention spec
- `training-data/tag_vocabulary.json` — current vocabulary schema
- `river-rats-core/run_attention_experiments.py` — Exp 3 mechanism
- `project_river_rats_v2.md` memory — v2.2 history (108 features,
  attn_draw_outs #1 feature, "Union of all 6 teams' tags")
- `feedback_attention_flags_when_features_change.md` — audit rule
