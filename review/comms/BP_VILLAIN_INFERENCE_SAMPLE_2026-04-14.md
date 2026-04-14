# Phase 3.5A — Villain Inference Sample for Review
**Date:** 2026-04-14

## Summary

- **185 BP-series hands total**
- **9 clean** (no missing villain declared)
- **148 HIGH-confidence** — missing seat is named in the action_history string (pipeline bug was only in the header field)
- **28 LOW-confidence** — action history doesn't name the seat, structural inference required

## Key finding

The BP-series generator DID track the missing villain in action_history (e.g. `SB check, BB bet, BTN ???`) but the `Villain positions` header only listed one seat. The data isn't truly missing — it was just dropped from one field. High-confidence inference recovers the seat directly from the action string.

## Sample — 15 HIGH-confidence inferences (distinct patterns)

| ID | Hero | Declared | Inferred | All villains | Action history (first 70ch) |
|---|---|---|---|---|---|
| BP1_01 | BTN | ['BB'] | ['SB'] | ['BB', 'SB'] | `SB check, BB bet, BTN ???` |
| BP1_03 | BB | ['BTN'] | ['HJ'] | ['BTN', 'HJ'] | `BB check, HJ check, BTN bet, BB ???` |
| BP1_05 | CO | ['BB'] | ['SB'] | ['BB', 'SB'] | `SB check, BB bet, CO ???` |
| BP1_07 | BB | ['BTN'] | ['CO'] | ['BTN', 'CO'] | `BB check, CO check, BTN bet, BB ???` |
| BP1_12 | SB | ['BTN'] | ['HJ'] | ['BTN', 'HJ'] | `SB check, HJ check, BTN bet, SB ???` |
| BP1_27 | SB | ['BTN'] | ['CO'] | ['BTN', 'CO'] | `SB check, CO check, BTN bet, SB ???` |
| BP4_01 | BTN | ['SB'] | ['BB'] | ['SB', 'BB'] | `SB check, BB check, BTN ???` |

## Sample — 5 LOW-confidence inferences (need owner call)

| ID | Hero | Declared | Best guess | Reasoning | Action history |
|---|---|---|---|---|---|
| BP4_07 | CO | ['BB'] | ['BTN'] | action history gave nothing; structural inference adds ['BTN'] (standard 3-way SRP blind defender) | `BB check, CO ???` |
| BP4_08 | CO | ['BB'] | ['BTN'] | action history gave nothing; structural inference adds ['BTN'] (standard 3-way SRP blind defender) | `BB check, CO ???` |
| BP4_11 | BB | ['CO'] | ['BTN'] | action history gave nothing; structural inference adds ['BTN'] (standard 3-way SRP blind defender) | `BB check, BB ???` |
| BP4_12 | BB | ['CO'] | ['BTN'] | action history gave nothing; structural inference adds ['BTN'] (standard 3-way SRP blind defender) | `BB check, BB ???` |
| BP4_13 | BB | ['CO'] | ['BTN'] | action history gave nothing; structural inference adds ['BTN'] (standard 3-way SRP blind defender) | `BB check, BB ???` |

For LOW-confidence: recommendation is to infer **BB** as the missing blind defender by default, or to review each individually. Owner to decide.

## Next step

If sample looks good, roll inference to all 185 BP hands and re-generate situation_texts with complete villain lists. Then re-run Pass 1 on the 185 corrected hands with fresh 4-team labelling.
