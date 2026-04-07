# River Rats — GTO Poker Coaching System

## Project Overview

Mobile poker training app with a GTO Oracle that evaluates player
decisions against game-theory-optimal play. Built in Python.

## Current State (6 April 2026)

- **v8 oracle:** 88.1% HU accuracy, 52.5% multiway (40-hand reference set)
- **45-feature pipeline:** shipped, all features live
- **Progressive model chain:** approved — v8→v9-3way→v9-4way→v9-5way
- **Model router:** shipped — selects specialist by opponent count
- **v9-baseline:** trained on 45-feature PokerBench, ready for warm-start
- **Master plan:** docs/MASTER_PLAN (1).md
- **Progressive chain design:** docs/PROGRESSIVE_MODEL_CHAIN.md

## Project Structure

```
river-rats-core/          ← production code (approved files ONLY)
  poker_game.py           ← game state and action handling
  preflop_engine.py       ← preflop decision engine
  range_manager.py        ← range composition and narrowing
  range_narrowing.py      ← street-by-street range updates
  feature_extractor.py    ← 45-feature extraction pipeline
  feature_keys.py         ← feature key definitions
  gto_model.py            ← XGBoost model inference (auto-detect 38/45)
  oracle_router.py        ← model selection by opponent count
  train_model.py          ← model training pipeline
  self_play.py            ← all-oracle self-play runner
  reference_evaluator.py  ← evaluate variants against expert labels
  multiway_adjuster.py    ← multiway pot adjustments
  coaching/               ← teaching pipeline
  models/                 ← trained model files
  tests/                  ← all test files
docs/                     ← specs and design documents
review/                   ← files awaiting review before approval
training-data/            ← CSVs and JSONL for model training
```

## Process Guide

**Read `docs/PROCESS_GUIDE.md` before starting any task.** It defines
team protocols, resource allocation, quality gates, and review
procedures. It also serves as the checklist for independent reviewers.

## Mandatory Protocols

### 1. Plan Before Build — PRESENT FOR REVIEW

**NEVER go straight from spec to building to running.**

The sequence is ALWAYS:
1. Write a plan (what files, what each does, what the open questions are)
2. Present plan for owner review
3. Owner approves (or redirects)
4. Build — one step at a time
5. Present each deliverable in review/ for owner review
6. Owner approves before next step
7. Nothing runs (no pipelines, no generation, no training) until code is reviewed

**Why this exists:** On 6 April 2026, Claude Code built an entire
4-step pipeline (generate → label → export → train), ran it, hit a
yield problem, started improvising fixes, and created a mess — all
without presenting anything for review. The labeller turned out to be
a rule-based heuristic (the exact approach proven not to work) that
nobody caught because it was never reviewed.

Speed without review creates waste. Slow and reviewed creates progress.

### 2. Validate Assumptions Before Building

Before writing code that depends on an assumption, verify it:
- "The self-play runner will produce ~200 3-way decisions from 150 deals"
  → RUN A SMALL TEST FIRST (10 deals) and check the yield
- "The heuristic AI produces realistic opponents"
  → CHECK what the AI actually does before building on it
- "This labelling approach produces GTO-quality labels"
  → QUESTION whether a rule-based heuristic is actually better than
    what we're replacing

**If you can't verify an assumption in 30 seconds, flag it as a
question in the plan.** Don't build on hope.

### 3. Test-First
Write failing tests BEFORE implementation. Tests define the contract.
If tests can't be written, requirements need clarification first.

### 4. Blueprint Before Build
No code changes without an architect agent reading the source first
and producing exact insertion points. Programmer implements from
blueprint only.

### 5. Stop Conditions — NEVER Improvise
If any of these occur, STOP and report BLOCKED:
- File doesn't exist where expected
- Function renamed or moved from blueprint
- Unexplained test failure
- Line numbers don't match
- Output contradicts expected result
- Any situation not covered by the blueprint
- **A pipeline step produces unexpected output (wrong volume, wrong
  distribution, errors)**
- **An assumption the spec relied on turns out to be wrong**

Improvising is worse than stopping. When the yield was 37 instead
of 200, the correct response was STOP and report — not write a
loose-opponent callback hack.

### 6. river-rats-core/ Is Sacred
Only reviewed, approved, passing files enter river-rats-core/.
After every approved change, update river-rats-core/ before starting
the next task. This folder is always deployable.

### 7. Verify Your Own Output
- Code: run full test suite, report pass/fail counts
- Blueprint: verify every file/function exists at specified location
- Poker judgment: provide reasoning for every conclusion
- Pipeline output: check volume, distribution, edge cases BEFORE
  declaring success

"It looks right" is not verification. Show evidence.

### 8. No Dead Code, No Misleading Comments
If an approach fails, remove the failed code. Don't leave dead
functions, wrong comments, or stale docstrings. Every line in a
file should reflect what the file actually does.

### 9. Review Folder Protocol
New files and significant changes go to review/ first with a review
document explaining:
- What was built
- Concerns and known issues
- Open questions that need owner input
- What tests pass/fail

Owner reviews. If approved, files move to river-rats-core/. If not,
they stay in review/ with feedback until fixed.

## Task Decomposition — MANDATORY

Before starting ANY multi-step task, decompose it across specialist
agents. Do NOT do everything yourself in one context.

**The rule:** Every task that involves more than one type of work
MUST be split across agents using subagent delegation.

| Work type | Agent to use |
|-----------|-------------|
| Reading source, finding insertion points, producing blueprints | architect |
| Running code, counting combos, computing equity, pipeline runs | programmer |
| Poker judgment, action evaluation, range decisions | gto-expert |
| ML model design, feature engineering, training config | ml-architect |
| Writing test cases before implementation | tester |
| Reviewing any deliverable before it ships | reviewer |

**Sequencing matters.** When a task needs multiple agents:
1. Design/judgment agent goes first (defines what to build/test)
2. Computation agent goes second (produces data/code)
3. Evaluation agent goes third (judges the output)
4. Reviewer agent goes last (quality gate)

NEVER skip decomposition. A single agent doing design + computation +
evaluation in one pass is the most common failure mode in this project.

## Anti-Patterns (things that have burned us)

- Building before validating → use specs with acceptance criteria
- Building before presenting plan → always plan → review → build
- Running pipelines before reviewing code → review first, run second
- Patching symptoms instead of root causes → find the real bug first
- Improvising when a step fails → STOP, report, get direction
- Agent reading too many documents → one focused brief per agent
- Programmer improvising when blueprint is stale → STOP protocol
- Rubber-stamp reviews → reviewer must produce specific findings
- Files approved but never copied to river-rats-core/ → check after
  every approval
- Assuming data generation will work → test yield with small sample first
- Rule-based heuristics pretending to be expert labels → if the
  labelling approach is threshold-based, it's another adjuster
- Dead code from failed approaches left in files → clean up immediately
- Stale docstrings that contradict the code → update when code changes

## Domain Notes

- Computation (counting combos, equity math) → use the pipeline, don't
  estimate manually
- Poker judgment (is this action GTO-correct?) → requires reasoning
  from computed data, not gut feel
- These are different skills. Never combine them in one agent pass.
- **GTO labelling is poker judgment, not threshold logic.** When the
  spec says "GTO Expert labels," that means per-hand poker reasoning
  about ranges, equity realization, and action implications — not
  if/elif chains on feature values.
