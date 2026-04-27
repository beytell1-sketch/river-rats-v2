---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author for dispatch) · gto-expert · ml-architect · QC stream · Owner
re: Mass labelling operational directive — owner approved defaults; builder terminal dispatches via labelling_agent.py
status: DIRECTIVE — owner sign-off received "proceed with the labelling defaults"; dispatch from builder terminal (not orchestrator)
---

# Mass labelling operational directive

## Authorization

Owner sign-off 2026-04-27 ~18:50 SAST: "proceed with the labelling defaults". All defaults from kickoff proposal locked in:
- 5 sonnet labellers per hand
- 494 hands × 5 = 2470 labels
- Skip PILOT_009 manual spot-check (QC pre-merge gate cleared)
- Tier 1 manifest 33→45 runs in parallel (separate workstream)

## Why builder terminal dispatches, not orchestrator

Mass labelling = 1235+ Agent dispatches (247 batches × 5 labellers if batch_size=10). Orchestrator session would crash context. Per memory `feedback_orchestration_efficiency_rules.md` + existing pattern in `river-rats-core/labelling_agent.py` ("done in Claude Code conversation"), the **builder terminal** is the natural home for the dispatch loop.

Per `feedback_listen_to_orchestrator_always.md` + `feedback_named_author_builds_not_polls.md`: this directive names the lead-programmer as author. Authoring mode on next /loop tick.

## Operational sequence

### Step 1 — Prepare batches

```
cd ~/river-rats-v2
git pull --ff-only origin master
python3 river-rats-core/labelling_agent.py prepare \
  --input data/corpus_revision_500_hand_2026-04-27.jsonl \
  --batch-size 10 \
  --num-labellers 5 \
  --protocol prompts/gto_labeller_v3.2.md \
  --output-dir review/labelling_batches/
```

(Verify exact arg names against the script's argparse; adjust as needed.)

Expected: ~50 batches × 5 labellers = ~250 batch files in `review/labelling_batches/`.

### Step 2 — Dispatch labellers (Claude Code subagents in builder terminal)

For each batch file: dispatch a sonnet subagent via the Agent tool:
- Subagent type: general-purpose (or specific labelling persona if defined)
- Brief: "You are a v3.2 GTO labeller. Read prompts/gto_labeller_v3.2.md. Label each hand in the batch file <path>. Output labels to <path>.labelled. Use the protocol verbatim — no improvisation."
- Run in parallel where context allows (batch dispatch in tight loops)

Track completion: log each batch's status (pending / running / complete / failed).

### Step 3 — Collect results

```
python3 river-rats-core/labelling_agent.py collect \
  --batch-dir review/labelling_batches/ \
  --output data/corpus_revision_500_hand_labels_2026-04-27.jsonl
```

Verify:
- 2470 labels in output (494 × 5)
- No labeller refusals beyond ~5% (acceptable refusal rate)
- All hands have ≥3 of 5 labels (some refusals tolerable)

### Step 4 — Open labels PR (milestone)

- Branch: `programmer/labels-mass-2026-04-27`
- Files: `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` + final report at `review/comms/PROGRAMMER_REPORT_MASS_LABELLING_2026-04-27.md`
- Title: `Builder: 494-hand mass labels (2470 labels, v3.2 protocol)`
- Body: distribution stats (RAISE/CALL/CHECK/BET/FOLD per category), refusal rate, wall-time, cost.

## Round 11 review chain (when labels PR opens — milestone gate per QC scope rule)

- **gto-expert**: spot-check 30 random labels for v3.2 protocol correctness
- **ml-architect**: label distribution checks (refusal rate, action mix per category, no NaN/parsing errors)
- **QC**: paired V-Implementation-Spec-Match (label format matches contract — same schema as Phase A 500 labels at master `4bce49f`) + V-Integration-Trace (sample label loads cleanly into trainer)

Per memory `feedback_qc_required_before_approval.md`: this is a milestone PR. QC pre-merge gate REQUIRED.

## Failure handling

- Individual batch dispatch failure: re-dispatch that batch only; don't restart the whole pipeline
- Labeller refusal: acceptable up to ~5%; if higher, surface to orchestrator for protocol audit
- Parsing failure on label collection: builder reports BLOCKED; orchestrator dispatches mini-fix cycle

## What this directive does NOT cover

- Trainer pipeline (separate Phase 12 directive after labels merge)
- Tier 1 manifest expansion (parallel workstream; separate PR)
- Held-out evaluation (Phase 12+)

## Cost tracking

Per kickoff proposal: ~$120-200 expected. Builder reports actual cost in final report (Step 4).

## References

- Master HEAD: `38f7c1f`
- Corpus: `data/corpus_revision_500_hand_2026-04-27.jsonl` (494 records, FINAL)
- Protocol: `prompts/gto_labeller_v3.2.md`
- Labelling agent: `river-rats-core/labelling_agent.py`
- Past pattern: Phase A 500 labels at master `4bce49f`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`

**Status: MASS LABELLING OPERATIONAL DIRECTIVE OPEN. Builder runs prepare → dispatch → collect → opens labels PR. Round 11 review chain dispatches when PR opens.**
