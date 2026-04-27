---
date: 2026-04-27
from: Lead-programmer (named author)
to: Main terminal (orchestrator) · Owner
re: Mass labelling operational directive — 5 grounding gaps before dispatch can begin; HOLD on 250-subagent dispatch
status: BUILDER_QUERY — directive-vs-source drift; clarification needed
---

# Builder query — mass labelling operational directive grounding

Per `feedback_builder_grounds_before_executing.md` + `feedback_queries_to_orchestrator.md` + CLAUDE.md "Stop Conditions — NEVER Improvise": grounding revealed material drift between
`MAIN_TERMINAL_MASS_LABELLING_OPERATIONAL_2026-04-27.md` (master `2b1d4cb`)
and the actual `river-rats-core/labelling_agent.py` + corpus schema +
the prior Phase B Protocol A label artefacts on master `4bce49f`.

I HOLD on the 250-subagent dispatch until the orchestrator clarifies — the
risk of charging ~$200-700 of subagent calls against a broken plan is
material per `feedback_quality_default_no_ask.md`.

## Drift findings (verified by dry-run)

### 1. CLI args don't match the script (EXISTENCE drift, per feedback_spec_vs_infrastructure_code_drift.md)

Directive § Step 1 issues:
```
python3 river-rats-core/labelling_agent.py prepare \
  --input data/corpus_revision_500_hand_2026-04-27.jsonl \
  --batch-size 10 \
  --num-labellers 5 \
  --protocol prompts/gto_labeller_v3.2.md \
  --output-dir review/labelling_batches/
```

Dry-run on master `2b1d4cb`:
```
labelling_agent.py: error: unrecognized arguments:
  --num-labellers 5 --protocol prompts/gto_labeller_v3.2.md
  --output-dir review/labelling_batches/
```

Three flags don't exist. Script's actual argparse (`labelling_agent.py:314-321`):
- `--input`, `--batch-size`, `--prompt` (NOT `--protocol`),
  `--batch-dir` (NOT `--output-dir`).
- `--num-labellers`: **does not exist as a script concept**.
  Each batch is dispatched ONCE to one subagent.
  The script has no notion of "5 labellers per hand".

### 2. Corpus schema mismatch (CONTENT drift)

Even with the CLI flags corrected, `prepare_batches` crashes on the corpus:

```
$ python3 river-rats-core/labelling_agent.py prepare \
    --input data/corpus_revision_500_hand_2026-04-27.jsonl \
    --batch-size 10 --prompt prompts/gto_labeller_v3.2.md \
    --batch-dir review/labelling_batches/
Loaded 494 situations
KeyError: 'situation_id'           # labelling_agent.py:116
```

Corpus record top-level keys (verified):
```
['board', 'deal_id', 'facing_bet', 'feat_dict', 'hero_cards',
 'hero_position', 'num_opponents', 'pilot_hand_id', 'pot',
 'prior_actions', 'source_situation_id', 'street', 'to_call',
 'villain_positions']
```

The script (`labelling_agent.py:116, 120, 156`) reads `sit['situation_id']`.
The corpus has `pilot_hand_id` and `source_situation_id` — NOT `situation_id`.

### 3. Past pattern (PR #50, master 4bce49f) used a different format

Phase B Protocol A labels (the only prior 5-labeller artefact):
- File layout: `review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_{1..5}.json`
- ONE JSON file per labeller, NOT batch files
- Each file: `{lane, model, protocol_version, protocol, total_labels, labels: [...]}`
- Each label keyed by `ref_id` (e.g. `"d6066_BB_flop"`) — derived from
  `deal_id + hero_position + street`, NOT `situation_id` or `pilot_hand_id`.

So the prior dispatch model was **5 subagent runs, each labelling all 100
hands in one go, each producing one labeller_N.json**. Not 50×10×5 batches.

### 4. Dispatch model ambiguity

The directive's cost estimate ($120-200) and wall-time (2-4 h) are
consistent with **5 subagent runs × 494 hands each** (Phase B style),
NOT with **250 batched subagent dispatches** (labelling_agent.py style).

At sonnet rates with a 100K+ char protocol context per dispatch:
- 5 × 494-hand dispatches: ~$75-150 (consistent with estimate)
- 250 × 10-hand dispatches: ~$250-750 (well above estimate)

Per `feedback_pipeline_projections.md`: static yield math must read
the runner code, not just the proposal. The estimate matches model A,
the script enforces model B, and the directive references both.

### 5. v3.2 protocol path

Verified exists: `prompts/gto_labeller_v3.2.md` (40,615 bytes). OK.
But `labelling_agent.py:106` defaults to `gto_labeller_v3.md`. Past
artefacts say `protocol_version: v3.2`, so the prompt path is correct
in the directive — just need to thread it through `--prompt` not `--protocol`.

## Specific clarifications needed

1. **Dispatch model**: Past-pattern (5 × full corpus per labeller, each
   labeller produces one JSON) OR new batched (50 batches × 5 dispatches
   each = 250 dispatches)? Builder recommends past-pattern: simpler,
   matches cost estimate, prior reviewer chain knows the format,
   `ref_id` keying matches `reference_evaluator.py:95`.

2. **Output schema**: Directive § Step 4 says
   `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` — flat JSONL.
   Past pattern was 5 JSON files keyed by `ref_id`. Should builder:
   (a) use past pattern, then convert at collect time?
   (b) flatten directly to JSONL with one row per (hand × labeller)?
   (c) flatten with consensus aggregation across 5 labellers?

3. **ID field**: corpus has `pilot_hand_id` for the original 100 pilot
   records and `source_situation_id` (deal-position-street style) for
   newer records. Past `ref_id` was deal-position-street. Should builder
   compute a unified `ref_id` per record at prepare time?

4. **Prepare-script fix scope**: do I patch `labelling_agent.py` to read
   `pilot_hand_id` (or new computed `ref_id`) AND add `--num-labellers`
   flag, OR do I bypass it and replicate the past Phase B per-labeller
   dispatch pattern via a thin wrapper script?

5. **Authorization to spend**: even after model is chosen, the dispatch
   loop is the largest single cost in this project to date. Confirm
   ~$120-200 ceiling is actually the spend cap, OR adjust ceiling
   given dispatch model decision.

## What I have NOT done

- NOT dispatched any subagents.
- NOT modified `labelling_agent.py`.
- Cleaned up the partial `review/labelling_batches/` directory created
  during the dry-run.

## What I am ready to do once unblocked

If orchestrator's verdict is **past-pattern** (5 × full corpus):
1. Write `scripts/dispatch_mass_labelling.py` — generates 5 sonnet
   subagents in sequence (or staggered parallel), each producing
   `review/mass_labelling_2026-04-27/labels_v3_2_labeller_{1..5}.json`.
2. Write `scripts/collect_mass_labels.py` — aggregates the 5 files into
   `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` per directive
   schema (1 row per (hand × labeller) or 1 row per hand with 5-vote field —
   depends on clarification 2).
3. Open labels PR per directive § Step 4.

If orchestrator's verdict is **labelling_agent.py with patches**:
1. Add `--num-labellers`, `--protocol` (or rename instructions to use
   `--prompt`), `--output-dir` (or rename to `--batch-dir`) flags.
2. Add `pilot_hand_id`/`source_situation_id` → `situation_id` adapter
   in `prepare_batches`.
3. Dispatch 250 subagents with retry/skip logic.
4. Open labels PR per directive § Step 4.

## References

- Directive (master `2b1d4cb`):
  `MAIN_TERMINAL_MASS_LABELLING_OPERATIONAL_2026-04-27.md`
- Script (master `4bce49f` and unchanged on `2b1d4cb`):
  `river-rats-core/labelling_agent.py`
- Corpus (master `9c8639a`):
  `data/corpus_revision_500_hand_2026-04-27.jsonl` (494 records)
- Past pattern (master `4bce49f`):
  `review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_{1..5}.json`
- Memory: `feedback_listen_to_orchestrator_always.md`,
  `feedback_named_author_builds_not_polls.md`,
  `feedback_builder_grounds_before_executing.md`,
  `feedback_queries_to_orchestrator.md`,
  `feedback_spec_vs_infrastructure_code_drift.md`,
  `feedback_quality_default_no_ask.md`,
  `feedback_pipeline_projections.md`

**Status: BUILDER QUERY OPEN. Pilot Orch HOLD on 250-subagent dispatch
until orchestrator clarifies dispatch model + output schema + script-
patching scope. Once clarified, builder authors per directive within one
tick.**
