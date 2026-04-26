---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Teaching builder · Game builder · Owner (briefed)
re: QC stream now active at ~/river-rats-qc/ + github.com/beytell1-sketch/river-rats-qc; advisory FLAG-only role; not in merge gate; ingests comms history first; multi-expert testing principle
status: ANNOUNCEMENT — fourth independent voice added per owner directive 2026-04-26; standing protocols for builders unchanged; QC findings produce fix-forward work, never block merges
---

# QC Stream Live — Independent Quality Control

## What changed

Project structure expanded from 4 streams to 5:

1. **Orchestrator** at `~/` — coordinates, gates merges (unchanged)
2. **Logic builder** at `~/river-rats-v2/` (unchanged)
3. **Teaching builder** at `~/river-rats-teaching/` (unchanged)
4. **Game builder** at `~/river-rats-game/` (unchanged)
5. **🆕 QC stream** at `~/river-rats-qc/` — independent quality control

QC repo: https://github.com/beytell1-sketch/river-rats-qc (private,
owner-only access).

Owner authorised 2026-04-26 per the multi-team / independent-review
discipline locked in the Stage 4 plan.

## What QC is

Independent fourth voice — separate from author, reviewer,
orchestrator. Catches what same-pipeline review chains miss.

**Five workstreams:**

1. **Audit-trail integrity** — verify reviewer-verdict claims match
   master content (e.g. "0 regressions" → really? "telemetry-only" →
   really?)
2. **Cross-stream contract drift** — does game's adapter actually
   match teaching's emitted CONTENT_API? Does v2's
   `extract_all_features` output what teaching/game consume?
3. **Architecture stress** — malformed inputs, edge cases, failure
   modes, perf, concurrency
4. **Process compliance audits** — random spot-checks of past PRs
   against PROCESS_GUIDE "Reviewer check" blocks
5. **Pre-milestone adversarial test cases** — generate stress
   fixtures BEFORE owner-gated transitions (Stage 4 pilot, Stage 5
   retrain, Stage 6 ship)

## What QC is NOT

- NOT a code author
- NOT a reviewer in the merge gate (different role from gto-expert /
  V3 / ml-architect)
- NOT a merger of PRs
- NOT a strategist (owner makes scope decisions)
- NOT a bottleneck on builder velocity
- NOT in the merge gate path

**Merge gate stays: orchestrator pre-merge check + dispatched
reviewer APPROVE + owner gate (high-stakes only).** QC findings are
ADVISORY → produce fix-forward work, never block merges.

## How QC operates

**Comms-history-first learning:** QC ingests project comms history
on activation. Reads incident patterns from past comms (misplaced
commits, push-block recoveries, dispatch path issues, fix-forward
triggers, audit-trail integrity questions). Uses these as training
data to inform what test classes matter.

**Multi-expert independent testing:** for high-stakes audits, QC
dispatches multiple expert agents independently on the same
target. Same multi-protocol robustness principle from Stage 4
plan. CONVERGED = high confidence, DIVERGED = investigate.

**Smarter over time:** QC maintains 4 evolving artefacts:
- `incident_pattern_library.md` — what incidents this project has
  had + root causes (training set)
- `test_class_registry.md` — what tests run, when, past findings
- `coverage_map.md` — project module × test class grid
- `curative_additions_log.md` — missed-class incidents → owner
  directives → new test classes added (institutional memory)

**Cadence:** own /loop, hourly continuous monitoring; accelerated
near milestones.

## How findings flow to your stream

If QC produces a finding affecting v2 / teaching / game:

1. Full finding lives at `~/river-rats-qc/findings/<date>-<topic>.md`
2. Cross-stream summary committed to your repo's
   `review/comms/QC_FINDING_<date>_<topic>.md`
3. Severity dictates response time:
   - **HIGH** — within 1 tick (15 min); orchestrator + owner notified
   - **MEDIUM** — noted at next routine sweep
   - **LOW / NIT** — batched in weekly digest
4. Status: FLAG (advisory) — orchestrator/builder decides whether
   to fix-forward or defer

## What you (each builder) need to do

**Nothing changes about your existing workflow.**

- Continue per-batch GTO / V3 / ml-architect reviews per standing
  pattern
- Continue PR cycle + standing per-batch protocol
- Continue dispatch-brief tool-list discipline
- Continue HARD pre-commit branch check
- Continue verdict-on-master mechanic

QC operates IN PARALLEL with you, not BEFORE or AFTER. If QC
produces a finding for your stream, treat it like any other
fix-forward signal (per `feedback_quality_default_no_ask.md` —
MEDIUM/non-blocking → still address).

## What's queued for QC's first run

Per `~/river-rats-qc/INITIAL_PRIORITIES_2026-04-26.md`:

**Phase 0** (mandatory): comms-history ingestion (~30-60 min)

**Phase 1** (first-run priority): audit-trail integrity sweep on
overnight Stage 3.5 PRs #5–#9. For each:
- Verify "0 regressions" claim (re-run canonical test suite)
- Verify diff scope claims (`git show --stat` classification)
- Verify specific numerical claims (e.g. M5 d8411 +0.072 p(BET))
- Verify M4 audit reproducibility (0/124 isolation violations)

If FAIL on any: HIGH-severity finding within 1 tick.

**Phase 2:** cross-stream contract drift on commit 14 multiway
field promotion (game ↔ teaching ↔ logic).

**Phase 3:** architecture stress on commit 14 (4-way hands,
all-villain-folded, NaN composition, heavy-collision boards).

**Phase 4+:** continuous monitoring + pre-milestone gates.

## Activation

QC terminal needs to be launched from `~/river-rats-qc/` cwd so:
- QC-local subagents in `.claude/agents/` are registered
- Project-scoped memory is correct
- Comms folder defaults align

Owner launches the QC session when ready. QC's `INITIAL_PRIORITIES_2026-04-26.md`
walks the first session through Phase 0 → 1.

## Cross-stream HOLD register update

Adding a row:

| # | Item | Status | Owner |
|---|---|---|---|
| 7 | QC stream activation + first-run audit-trail sweep | ⏳ pending — awaiting owner to launch QC terminal | Owner |

This isn't a blocker on Stage 4 prep work — Tasks 3-5 continue per
existing plan. QC adds a parallel audit voice.

## Reference

- `~/river-rats-qc/CLAUDE.md` — QC role definition
- `~/river-rats-qc/learning/incident_pattern_library.md` — 10 seeded
  incidents (training set)
- `~/river-rats-qc/learning/test_class_registry.md` — 10 active test
  classes
- `~/river-rats-qc/INITIAL_PRIORITIES_2026-04-26.md` — bootstrap
  directive
- https://github.com/beytell1-sketch/river-rats-qc — repo
- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` (`ee3d9f5`)
  — multi-team / independent-review principle that QC extends
