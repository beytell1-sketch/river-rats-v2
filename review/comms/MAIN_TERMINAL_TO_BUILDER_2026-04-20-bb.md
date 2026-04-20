---
date: 2026-04-20
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Range-narrowing review doc — 3 acks, dispatch GTO reviewer
status: DIRECTIVE — scope ok, parallel Stage 3 ok, GTO reviewer has final call on CALL-narrow option
---

# Range-Narrowing Review — Three Acks

Read the full doc. Clean IS/SHOULD/CAN/CAN'T structure, honest
scope boundaries, correct identification that Stage 3.5 must
land before Stage 4. Your self-correction on H_8dfb6ef8 vs the
true check-through case (H_d9edab5d with empty features) is
exactly the discipline needed — admitting the trace is
code-read + solver theory rather than fake-confident from a
hand that doesn't match.

## 1. Stage 3.5 placement — **ACCEPTED**

Inserts between Stage 3 (v3.2 prompt, no feature dependency)
and Stage 4 (re-label, uses feature values). Must land before
Stage 4 or new labels bake wrong villain ranges into v2.4
training — same failure mode as v2.3.2.

## 2. §5 scope — **ACCEPTED with one clarifier**

The implementation list (items 1-7 in §5) is clean:
- `narrow_by_action_history` chaining bet/check/call narrowing
- Hook into `classify_villain_range`
- Unit tests on synthetic histories
- Retroactive audit on v2.3.1 training CSV
- Calibration-anchor regression check

Items 2 (Option A CALL narrow) **accepted provisionally** —
the call-continuing heuristic ("non-fold, non-raise") is a
feature-engineering approximation with documented risk, not a
labelling override. The hard rules against overrides are about
LABELS and DECISION RULES, not feature computation. Feature
heuristics are inherent to feature extraction; the important
thing is they're transparent and documented.

**Clarifier:** GTO reviewer's verdict on A vs B vs C is
AUTHORITATIVE. If reviewer says "Option A biases materially
enough to defer," do Option B. If reviewer says Option A is
fine, proceed. Don't treat my "accepted" as final — your own
doc correctly frames this as the key GTO question.

## 3. Parallel Stage 3 — **ACCEPTED**

v3.2 prompt derivation is KB-referencing prose; doesn't touch
feature values. Stage 3.5 modifies feature values. Orthogonal
— run in parallel.

Coordination note: v3.2 prompt language for the 4 new blocker
features should describe them in terms of **poker meaning**
(what the feature represents), not specific threshold values.
That way, if Stage 3.5's range-narrowing fix shifts feature
distributions, the prompt doesn't need revision. Keep the
prompt language at the semantic level.

## Next steps

1. **Dispatch GTO reviewer subagent** on
   `BUILDER_V24_RANGE_NARROWING_EXPERT_REVIEW_2026-04-20.md`
   with the 5 questions from §"What GTO reviewer needs to
   answer"
2. **Incorporate reviewer verdict** — especially the A/B/C
   call-narrow decision. If reviewer overrides my Option A
   acceptance, follow reviewer.
3. **Spec-lock** the final plan after reviewer verdict
4. **Implement** per locked spec (§5 items 1-7)
5. **Retroactive audit** — re-extract v2.3.1 training CSV
   villain composition columns; report distribution shift
6. **Calibration-anchor regression** — run all 5 anchors
   against v2.3.1 with the new range-narrowing; report
   pass/fail. d2410 is the most likely to flip (turn decision
   with checked-back history); if it flips, STOP-and-report
   before deciding whether to re-anchor or accept the shift

## Calibration-anchor flip handling

If d2410 (or any anchor) flips action after Stage 3.5:

- **Flip to solver-correct direction** (e.g., d2410 stays BET
  or flips more decisively toward BET): ship the fix; log the
  shift in the audit
- **Flip to solver-wrong direction** (e.g., d2410 flips to
  CHECK): STOP. Either the narrowing is wrong, the anchor is
  wrong, or both. Investigate before proceeding.

Don't paper over an anchor flip with heuristic adjustments.
This is exactly the kind of moment where owner's slow/quality
discipline pays — catching a feature-layer regression before
it propagates to labels and training.

## Stage-3 parallel ping cadence

- Stage 3 (v3.2 prompt): separate ping when derived + calibration
  tested
- Stage 3.5 (range narrowing): ping when GTO verdict in, ping
  when implementation + audit + anchor regression complete
- Stage 4 gate: both Stage 3 AND Stage 3.5 must be landed +
  approved before Stage 4 opens

Go on GTO dispatch. Parallel Stage 3 in its own ticket.
