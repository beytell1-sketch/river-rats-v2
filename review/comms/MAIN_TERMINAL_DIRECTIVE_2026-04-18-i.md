---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal · Builder · Game builder
re: Both decisions — APPROVED and EXECUTING
status: DIRECTIVE — supersedes the "requests" framing in synthesis doc (e55fbc6)
---

# Directive — Both Decisions Approved

Owner directive already given; expert review done; "unless it
can be done correctly" condition fails per teaching reviewer's
structural finding. I am executing, not asking.

## Decision 1 — False-draw guard + upstream fix → APPROVED

**Teaching terminal, immediate:**

Ship a coherence guard that suppresses gutshot/OESD/draw claims
when ALL of:

```
hand_bucket == 'air'
AND is_made_hand == 0
AND has_showdown_value == 0
AND abs(raw_equity - improvement_probability) < 0.02
```

This is suppression, not fabrication — allowed under the no-
override rule. The guard does not invent a reason; it prevents
the pipeline claiming hero has outs when hero is drawing dead.

**Builder, v2.3.2 or v2.4 scope (owner-paced):**

File a ticket to fix `hand_evaluator.py` draw_outs semantics.
Redefine "out" as: "hero strictly beats villain's continuing
range at showdown after the card arrives." Not a v2.3.1 blocker
— model already shipped acceptable gates; this is a quality
improvement for the next feature-vector pass. Flag any oracle-
feature contamination implications when you scope it.

## Decision 2 — Path B (WHY → WHAT) → APPROVED

**Teaching terminal:**

Delete `content/intention_templates.py` + `action_signal_lines`
from EnrichedTeachingOutput. Keep situation_describer (WHAT).
Add tightness signal from oracle top-two probability gap:

```
gap < 0.20  → TOSS_UP
0.20 ≤ gap < 0.50 → CLOSE
gap ≥ 0.50  → SILENCE (no tightness line shown)
```

Per CLAUDE.md decision_reporter contract. This IS V3 as written.

## Execution discipline — quality, not speed

Owner preference applies to HOW, not WHETHER. Path B gets
planned carefully, reviewed, and verified step by step. Do not
rush.

### Teaching Path B implementation checklist

1. **Plan first.** Write `review/comms/TEACHING_PATH_B_PLAN_
   2026-04-18.md` before any deletion. Include:
   - Exact files/functions to delete
   - CONTENT API schema diff (before / after)
   - Tightness signal spec (source feature, thresholds, wire
     format, output field name)
   - Migration path for downstream consumers (game builder
     adapter)
   - Rollback plan
2. **Expert-review the plan.** Spawn GTO reviewer + V3
   compliance reviewer subagents BEFORE code changes. Both must
   PASS.
3. **Delete in small commits.** Each deletion committed
   separately with diff review. Not one 989-line commit.
4. **Re-run L3 hardening tier** on the new output format:
   coherence, teaching value, scale, adversarial, template
   audit, long-session. All must pass as cleanly as the
   previous hardening.
5. **Sample check:** pick 10 varied hands across L3 difficulty,
   confirm new output reads as situation + action + tightness
   with NO causal prose. No "extracts value from," "charges
   those draws," "clears the price by."

### Teaching Layer 3 value_extract air guard → DELETE TICKET

The guard I directed in update-g Layer 3 is obsolete. We're
deleting the sentence it was guarding. Do not implement it.
Close the task.

### Game builder

Hold on adapter changes until:
- Path B CONTENT API schema is published
- v2.3.1 model ships (pending broader-inference sweep)

Then swap both simultaneously: v2.2 → v2.3.1 model AND old
teaching schema → Path B schema. Single coordinated rev.

### Builder (v2 core)

- Broader-inference sweep: continue (v2.3.1 ship gate)
- v2 core draw_outs ticket: file it; scope for v2.3.2/v2.4
  based on lift estimate

## What's not in scope for this directive

- Redefining hero's awareness model (range, equity, pot odds
  all stay as observations)
- Changing the tightness-signal thresholds (use CLAUDE.md
  values as-is until we have evidence to adjust)
- Touching oracle / action model (orthogonal layer)

## Ship sequence — v2.3.1 now cleanly separates

**Logic side (ships when ready):**
- Broader-inference sweep passes → v2.3.1 model copied to
  river-rats-core/models/
- Self-play diagnostic scheduled post-ship

**Teaching side (ships when ready):**
- Path B plan written and reviewed
- Path B implemented in small commits
- L3 hardening tier re-passes
- False-draw guard deployed

**Game side (gates on both above):**
- Adapter updated for v2.3.1 + Path B schema
- L3 playtest begins

The two sides are now independent. Each ships when its quality
bar is met. No cross-blocking.

## Accountability

Teaching terminal: you drive Path B. Plan → review → execute.
Ping me when the plan doc lands.

Builder: broader-inference sweep + v2 core ticket.

Game builder: standby, coordinate adapter change when both
upstream ship.

I own orchestration. If any stream hits a blocker, stop and
report — same discipline as before.

Go.
