---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder · Teaching terminal · Game builder
re: Continue both streams; owner's playtest-logging plan gates the game session only
status: DIRECTIVE
---

# Gating Map — Owner's Playtest Logging Plan

Owner is building a playtest feedback-logging plan in parallel.
Question: should teaching and builder pause?

**Answer: no. Keep going.** The logging plan gates the actual
playtest session, not the upstream prep.

## What does and doesn't depend on the logging plan

| Work item | Depends on logging? | Status |
|---|---|---|
| Builder: self-play diagnostic | No — synthetic, internal stats | PROCEED |
| Teaching: Path B plan doc | No — design work | PROCEED |
| Teaching: expert-review the plan | No — design review | PROCEED |
| Teaching: Path B implementation | No — code work | PROCEED |
| Teaching: L3 hardening re-pass | No — unit/integration tests | PROCEED |
| Teaching: false-draw guard | No — already cleared to ship | PROCEED |
| Game: coordinated adapter swap | **Yes** — produces output captured during playtest | HOLD |
| Human playtest sessions | **Yes** — logging plan IS the instrument | HOLD |

## Why this is the right gating

- The upstream work (self-play, Path B, hardening) all has to
  happen regardless. Pausing it wastes calendar time and
  doesn't help the logging plan.
- Quality-focused: build the measurement instrument (owner's
  logging plan) before measuring — correct. But upstream
  readiness builds in parallel so the measured subject exists
  when the instrument lands.
- Three streams independent: owner's logging is effectively a
  fourth parallel stream. All four converge at the game swap
  + first playtest session.

## What each terminal should do

**Builder:** run self-play now per directive-k. Report results.
After that, stand by for playtest-surface bugs routed from the
logging plan.

**Teaching:** start the Path B plan doc. Expert-review before
deletion. Small commits. L3 hardening re-pass. By the time
teaching converges, owner's logging plan should also be ready
— natural handoff.

**Game:** continue to hold on the coordinated swap. When teaching
and logic both report ready AND owner signals logging plan is
ready, execute the swap and start playtest.

## If owner wants help with the logging plan

Not implying you do. But if at any point you want help on:
- Schema for findings capture (what fields, what granularity)
- Integration points with the game prototype
- Categorization scheme (oracle-surface vs teaching-surface vs
  UX vs poker-judgment)
- Replay/reproduction format so a logged finding can re-run
  through the pipeline

I can spawn a subagent to draft an option for your review. Say
the word. No intrusion otherwise.

## Summary in one line

Upstream prep continues; game swap + playtest waits for your
logging plan. All four streams land together.
