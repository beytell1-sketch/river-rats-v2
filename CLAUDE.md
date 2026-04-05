# River Rats — GTO Poker Coaching System

## Project Overview

Mobile poker training app with a GTO Oracle that evaluates player
decisions against game-theory-optimal play. Built in Python.

## Project Structure

```
river-rats-core/          ← production code (approved files ONLY)
  poker_game.py           ← game state and action handling
  preflop_engine.py       ← preflop decision engine
  range_manager.py        ← range composition and narrowing
  range_narrowing.py      ← street-by-street range updates
  feature_extractor.py    ← 38-feature extraction pipeline
  feature_keys.py         ← feature key definitions
  gto_model.py            ← XGBoost model inference
  train_model.py          ← model training pipeline
  hand_evaluator.py       ← hand strength evaluation
  hand_categories.py      ← hand classification
  multiway_adjuster.py    ← multiway pot adjustments
  coaching/               ← teaching pipeline
  models/                 ← trained model files
  tests/                  ← all test files
docs/                     ← specs and design documents
independent-review/       ← audit trail and review history
```

## Mandatory Protocols

### 1. Test-First
Write failing tests BEFORE implementation. Tests define the contract.
If tests can't be written, requirements need clarification first.

### 2. Blueprint Before Build
No code changes without an architect agent reading the source first
and producing exact insertion points. Programmer implements from
blueprint only.

### 3. Stop Conditions — NEVER Improvise
If any of these occur, STOP and report BLOCKED:
- File doesn't exist where expected
- Function renamed or moved from blueprint
- Unexplained test failure
- Line numbers don't match
- Output contradicts expected result
- Any situation not covered by the blueprint

Improvising is worse than stopping.

### 4. river-rats-core/ Is Sacred
Only reviewed, approved, passing files enter river-rats-core/.
After every approved change, update river-rats-core/ before starting
the next task. This folder is always deployable.

### 5. Verify Your Own Output
- Code: run full test suite, report pass/fail counts
- Blueprint: verify every file/function exists at specified location
- Poker judgment: provide reasoning for every conclusion

"It looks right" is not verification. Show evidence.

## Domain Notes

- Computation (counting combos, equity math) → use the pipeline, don't
  estimate manually
- Poker judgment (is this action GTO-correct?) → requires reasoning
  from computed data, not gut feel
- These are different skills. Don't combine them in one agent pass.

## Anti-Patterns (things that have burned us)

- Building before validating → use specs with acceptance criteria
- Patching symptoms instead of root causes → find the real bug first
- Agent reading too many documents → one focused brief per agent
- Programmer improvising when blueprint is stale → STOP protocol
- Rubber-stamp reviews → reviewer must produce specific findings
- Files approved but never copied to river-rats-core/ → check after
  every approval
