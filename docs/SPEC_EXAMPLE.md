# SPEC: Example — Fix CALL→RAISE Error in Legacy Rules

## Objective

Eliminate false RAISE recommendations when the correct GTO action is
CALL, caused by `is_pure_value_raise()` in `legacy_rules.py`.

## Context

The oracle occasionally recommends RAISE when CALL is GTO-correct.
Root cause traced to `is_pure_value_raise()` which doesn't account
for pot control situations where equity is high but raising inflates
the pot against a capped range.

## Requirements

- `is_pure_value_raise()` must return False when pot control is
  indicated (equity > threshold but opponent range is uncapped)
- RaiseSignal system must gate all raise recommendations through
  the NONE/POSSIBLE/PREFERRED tiers
- No raise recommendation without passing through the global
  arbitration layer

## Constraints

- Do not modify `poker_game.py` — only `legacy_rules.py` and
  `raise_signal.py`
- All existing oracle tests must continue to pass
- Pot control threshold values must be configurable, not hardcoded

## Acceptance Criteria

- [ ] 5 known CALL→RAISE error hands now produce CALL
- [ ] `is_pure_value_raise()` returns False for pot-control scenarios
- [ ] RaiseSignal arbitration layer is invoked for every raise path
- [ ] All existing tests pass (zero regressions)
- [ ] 3 new test cases cover the pot-control gate

## Risks

- Threshold tuning may over-correct (suppress valid raises)
- Other callers of `is_pure_value_raise()` may depend on current
  behavior — architect must trace all call sites

## Notes

- GTO Expert should validate the pot-control threshold values after
  the programmer implements them. Computation first, judgment second.
