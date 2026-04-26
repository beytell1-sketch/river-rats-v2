---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Owner · Logic builder · Teaching builder · Game builder · QC stream
re: Pre-pilot owner readiness brief — HIGH-1 decoupled from pilot-dispatch gate via empirical dependency analysis; pilot dispatch can proceed NOW pending owner authorization; teaching HIGH-1 + C5.2 work continues in parallel
status: BRIEF + GATE REVISION — pilot-dispatch gate effectively CLEAR on logic + game sides; teaching HIGH-1 reclassified as teaching-internal; QC Phase 5 sweep can fire immediately on existing master state
---

# Pre-Pilot Owner Readiness Brief

## Headline

**The pilot-dispatch gate is effectively clear.** I had stacked
teaching HIGH-1 on the gate conservatively; honest dependency analysis
shows it doesn't affect pilot correctness. **Owner pilot-dispatch
authorization is the only meaningful remaining gate.**

Owner can authorize pilot dispatch now. Teaching HIGH-1 + C5.2 work
continues in parallel.

## What changed in this analysis

Earlier orchestrator comms (e.g. `309ad35`, `c1a7c0e`) listed
teaching HIGH-1 as a "pilot-dispatch gate item." That was conservative
inheritance from the QC Phase 5 framework + the principle "address all
cross-stream HIGHs before milestone." In response to owner's question
"do we really need to wait for teaching?", I traced what the pilot
dispatch *actually consumes*:

### What HIGH-1 breaks

Teaching renderer's `_per_villain_composition` pass-through doesn't
translate producer keys (`{tp_plus, medium, draw, air}`) to
CONTENT_API documented keys (`{tp_pct, medium_made_pct, draw_pct,
air_pct}`). Surfaces when:
- Teaching's C5.2 fixture swap replaces synthetic sentinel jsonl with
  real production rows → teaching's existing tests FAIL
- Game UI displays renderer output without translation → wrong inner
  keys reach felt

### What HIGH-1 does NOT break (the pilot dispatch path)

| Consumer | Reads from | Bypasses teaching renderer? |
|----------|-----------|------------------------------|
| Pilot labellers (15 = 3 protocols × 5 agents) | Raw oracle features + hand state + action history + board texture | YES — labellers reason from raw data, not rendered content |
| Convergence-checker | Per-labeller output + voting logic | YES — internal aggregation |
| Highlighter (H1/H2) | Consensus action + per-protocol vote tally + anonymised aggregate reasoning | YES — Stage 4 plan §3 explicitly excludes solver output and per-labeller attribution |
| Reviewer | Highlighter output + spec | YES — pure aggregation logic |
| Adjudicator (3 sub-roles) | Reviewer output + Stage 6 hash-locked test set | YES — operates on canonical artifact |
| Stage 6 evaluation | Hash-locked corpus `65cfbf26...` over 47652 bytes | YES — bypasses teaching renderer entirely |
| Stage 5 retrain | Pilot label corpus + commit-14-era multiway training rows | YES — trains on raw producer features |

**Pilot dispatch is downstream of `feature_extractor.py` raw output,
upstream of teaching renderer.** Teaching renderer is in the game UI
path, not in the pilot path.

### Game already handles HIGH-1 forward-compatibility

Phase B integration at game `62d30e6` shipped inner-key shape
tolerance (`_readVillainCompositionPcts()`):

```javascript
// Tolerates either inner-key shape per HIGH-1 caveat
// CONTENT_API form (tp_pct, medium_made_pct, draw_pct, air_pct)
// OR producer form (tp_plus, medium, draw, air)
// Auto-scales fractions (0-1) to percentages
```

Game UI displays correctly regardless of whether teaching's HIGH-1 fix
has landed. **The downstream consumer is decoupled.**

## Revised pilot-dispatch gate

```
✅ Phase 2 HIGH-2 (game adapter passlist):           SEALED
✅ Phase 3 HIGH-1/2/3 + Phase 1 HIGH (Task 4.5):     SEALED
✅ Task 4.3 v1.0.3 NITs:                             SEALED
✅ Task 5 (Pilot orchestration v1.0):                SEALED
✅ HIGH-4 (cross-stream aggregate semantics):        SEALED
✅ Task 5 v1.0.1 + v1.0.2 pre-dispatch fixes:        SEALED
✅ Stage 6 held-out test set hash-locked at 65cfbf26...: SEALED v1.0.3
✅ Game forward-compat (HIGH-1 tolerance via Phase B): SEALED at game 62d30e6

⏳ QC Phase 5 pre-pilot sweep — CAN FIRE NOW on existing master state
   (HIGH-1 decoupled from pilot-dispatch correctness)

⏳ Owner pilot-dispatch authorization — final gate
```

## Reclassified items (still active, but NOT blocking pilot)

These are real work items but on different critical paths:

| # | Item | Critical path | Status |
|---|------|---------------|--------|
| 10 | Teaching HIGH-1 (renderer translation) | Teaching C5.2 fixture swap; v4.1 ship | ACTIVE on teaching's branch; ~30-60 min author work; nudge issued at `4865d33` |
| 21 | FEATURE_COLUMNS contract drift | Logic v1.1 housekeeping | QUEUED post-pilot |
| 22 | RERUN_ gitignore | Logic v1.1 housekeeping | QUEUED post-pilot |
| 23 | Cache-key docstring | Logic v1.1 housekeeping | QUEUED post-pilot |
| 24 | HIGH-2 indirect propagation | Logic v1.1 hardening | QUEUED post-pilot |
| 27 | HIGH-4 monotone-True doc | Logic v1.1 housekeeping | QUEUED post-pilot |

**None of these affect pilot correctness.** Pilot can dispatch with
all of them open; they're real but separate work.

## QC Phase 5 sweep — fire now

QC's published Phase 5 framework (`14fc0ad`) gated on "HIGH-1 lands +
v1.0.x lands." Both gates were precautionary, not load-bearing on
pilot correctness. **QC can fire Phase 5 sweep on the current master
state (`3871799`).** I'll send a cross-stream comm to QC clarifying
the gate-decoupling.

If QC Phase 5 sweep produces a finding affecting pilot correctness,
that's a real signal. If it produces only HIGH-1-related findings
(teaching renderer surface), those don't block pilot dispatch.

## Recommended sequence

### Option A — Dispatch pilot in parallel (RECOMMENDED)

1. **NOW:** Owner authorizes pilot dispatch
2. **NOW (parallel):** QC fires Phase 5 sweep on existing master
3. **NOW (parallel):** Teaching continues HIGH-1 fix per directive
   `e29aec1` + nudge `4865d33`
4. Pilot Orchestrator dispatches per Task 5 v1.0.2 spec
5. Phase A (33-way preflight + tier check + 5-call latency probe)
   verifies operational assumptions before Phase B (heavy labelling)
   commits

**Cost:** ~30-60 min faster pilot start. **Risk:** zero load-bearing
on pilot correctness; any HIGH-1-related issues surface in
teaching/game streams (forward-compat already shipped on game side).

### Option B — Wait for teaching HIGH-1 (CONSERVATIVE)

1. Wait ~30-60 min for teaching HIGH-1 PR
2. Merge teaching HIGH-1
3. QC Phase 5 sweep fires
4. Owner authorizes pilot dispatch
5. Pilot dispatches

**Cost:** ~30-60 min added wall-time. **Benefit:** marginal — no
correctness gain on pilot; cleanest cross-stream state at dispatch
time.

### Option C — Hybrid (defer authorization until QC Phase 5 sweep clean)

1. **NOW:** QC fires Phase 5 sweep on current master
2. If QC sweep clean (no pilot-affecting findings): owner authorizes
3. Teaching HIGH-1 continues in parallel (post-authorization)

**Recommended:** Option C. Honors QC's pre-pilot adversarial
test-case principle (their TC-13 framework is real signal) without
waiting on teaching. The QC sweep itself is ~10-30 min on current
master; faster than waiting on teaching HIGH-1.

## Why I'm correcting the gate now

Per memory `feedback_quality_default_no_ask.md`: "Don't ask between
fast/loose vs slow/clean — pick clean and proceed." I had been
operating with "wait for teaching" = clean. But that was wrong: clean
is "address all *load-bearing* dependencies"; teaching HIGH-1 is not
load-bearing for pilot.

Per memory `feedback_compute_assumptions.md`: "Before long jobs,
verify prior changes haven't made steps redundant (e.g. all-player
logging makes hero rotation pointless)." The HIGH-1 wait was
predicated on a dependency that doesn't exist. Game's HIGH-1
forward-compat tolerance shipped before pilot would dispatch — that
made the HIGH-1 wait redundant for pilot purposes.

## Cross-stream notifications

After owner reviews this brief:

1. **QC**: cross-stream comm (`MAIN_TERMINAL_TO_QC_PHASE5_GATE_DECOUPLED_2026-04-26.md`)
   noting HIGH-1 is decoupled; Phase 5 sweep can fire now
2. **Teaching**: cross-stream comm noting HIGH-1 reclassified as
   teaching-internal (still needed for C5.2 + v4.1, no longer
   blocking pilot)
3. **Logic builder**: standby; pilot dispatch is owner-gated; logic
   builder's next directive depends on owner's authorization decision

## Pilot dispatch — what will happen

Per `STAGE4_PILOT_ORCHESTRATION_v1_0.md` (sealed at `3fa8e93`):

- 7-phase orchestration (A: preflight; B: 15-labeller × 100-hand
  dispatch; C: convergence checking; D: highlighter pass; E:
  reviewer pass; F: adjudicator pass; G: corpus seal)
- 10-13h wall-time estimate (Phase B is the heavy lift)
- $140-$700 cost envelope (model-mix dependent; preflight selection)
- 13+2 PRE-DISPATCH PREREQUISITES (live API tier check, model
  selection, etc. — all operator-checkable, owner verifies before
  dispatch)
- Standing protocol-diversity principle (3 protocols × 5 agents = 15
  labellers; CONVERGED labels treated as high-confidence)

## Action

**Owner:**
- Decide: Option A (dispatch now) / B (wait teaching) / C (wait QC
  Phase 5 only)
- If A or C: review the 15 PRE-DISPATCH PREREQUISITES in
  `STAGE4_PILOT_ORCHESTRATION_v1_0.md` before authorization
- Authorization is a discrete decision; can be a comms doc
  `OWNER_PILOT_DISPATCH_AUTHORIZATION_<date>.md` or a /loop
  instruction to logic builder + Pilot Orchestrator persona

**Orchestrator (me):**
- This brief shipped (after commit + push)
- Cross-stream comms to QC + teaching to clarify gate-decoupling
- /loop continues at 15-min cadence
- On owner authorization: orchestrator dispatches Pilot Orchestrator
  per spec; loop monitoring shifts to phase-by-phase progress
  tracking

**QC stream:**
- Phase 5 pre-pilot sweep can fire on current master `3871799`
- Cross-stream comm follows

**Teaching builder:**
- HIGH-1 fix continues per `e29aec1` directive + `4865d33` nudge
- Reclassified as teaching-internal (gates C5.2 + v4.1, not pilot)
- Still important; just different critical path

**Logic builder:**
- Standby; awaiting owner pilot-dispatch authorization
- On authorization: become Pilot Orchestrator persona per Task 5
  spec
- Post-pilot: HOLD #21 / #22 / #23 / #24 / #27 housekeeping cycle

## References

- Stage 4 plan: `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`
  (`ee3d9f5`)
- Pilot orchestration spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md`
  (sealed via PR #29 at `b2fbf02`; canonical at master)
- Stage 6 held-out hash-lock: `STAGE6_HOLDOUT_TESTSET_v1_0.md`
  (v1.0.3; SHA256 `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`)
- HIGH-1 directive (still active for teaching): `e29aec1`
  (`MAIN_TERMINAL_TO_TEACHING_QC_HIGH_1_2026-04-26.md`)
- HIGH-1 nudge: `4865d33`
  (`MAIN_TERMINAL_TO_TEACHING_HIGH_1_NUDGE_2026-04-26.md`)
- Game HIGH-1 forward-compat: `62d30e6` (game `_readVillainCompositionPcts()`)

**Status: pre-pilot owner readiness brief shipped. Pilot-dispatch gate
effectively CLEAR. Owner authorization is the only meaningful gate.
Recommended: Option C (QC Phase 5 sweep on current master, then
authorize). Teaching HIGH-1 + C5.2 work continues in parallel.**
