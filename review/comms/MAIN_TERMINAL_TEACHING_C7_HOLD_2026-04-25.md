---
date: 2026-04-25
from: Main terminal (orchestrator)
to: Teaching · Owner
re: C7 (hero_range_percentile wording cleanup) — HOLD until after C5.2 fixture swap; teaching stays strictly held
status: DIRECTIVE — defer C7 to post-C5.2; no new teaching commits during HOLD window; plan author's "land C7 last" recommendation applies as-is
---

# Teaching C7 — Hold Until After C5.2 Fixture Swap

## Decision

**Hold C7.** Do not start the wording cleanup now. Land it after the
C5.2 real-row fixture swap (which itself happens after builder
commit 14 lands the multiway field promotion).

Sequencing:

```
[builder commit 14 lands]
  → C5.2 (real-row F3/F4 swap, data-only on the C5.2-pre-prep plumbing)
  → V3 per-commit review on C5.2
  → C7 (hero_range_percentile wording cleanup, doc-only)
  → V3 per-commit review on C7
  → SHIP REPORT promotes from PRE-VERIFICATION to FULL VERIFICATION
  → Orchestrator pre-Stage-6 gate (HOLD #4)
  → Merge greenlight
```

## Why hold C7 now (not "use the wait window")

Three reasons.

**1. The plan author already decided this.** From
`TEACHING_V4_1_NAN_RENDER_PLAN_2026-04-22.md` §C7:

> "Teaching may land C7 at any point in the sequence where it's
> lightest — early if it's simplest, or last as the ship-cleanup
> commit. **Recommend landing C7 last to keep NaN-render scope clean
> in the SHIP REPORT.**"

The plan is permissive on timing but recommends *last*. "Last" here
means after the NaN-render scope work is closed out — and C5.2
real-row swap is itself NaN-render scope work (it's the production-
row verification of the same render paths). Therefore "C7 last"
means after C5.2.

We don't override the plan author's explicit recommendation without
a strong reason. There isn't one.

**2. Strict held-stream discipline (parallel-stream pacing).**
Per `feedback_orchestrator_controls_parallel_timing.md`: faster
stream HOLDs at pre-ship until cross-stream verifications clear;
slower stream sets pace; orchestrator gates merges. Teaching is the
faster stream. Logic is gating. Teaching adding commits during the
HOLD window — even doc-only — softens the held-state semantics and
risks the SHIP REPORT scope drifting commit-by-commit.

Better: teaching is *truly* held, then unholds in a clean burst
(C5.2 swap → C7 cleanup → SHIP REPORT update → merge greenlight)
once the upstream signal arrives.

**3. SHIP REPORT update cadence.** Currently PRE-VERIFICATION HOLD.
If C7 lands now: SHIP REPORT updates twice (once for C7's V3 review
artefact, once when C5.2 lands and removes PRE-VERIFICATION marker).
If C7 lands after C5.2: SHIP REPORT updates once, in a single
post-commit-14 burst, listing both the C5.2 real-row evidence and
the C7 wording verification under one full-verification revision.
Single coherent update beats two interleaved updates.

## What teaching should do during the HOLD window

Nothing on `teaching/v4-1-nan-render`. Strict hold.

Useful waiting-window activities (none of these add commits to the
held branch):

- **Monitor**: watch `~/river-rats-v2/origin/master` for commit 14
  (Finding B fold-in). Recognisable by:
  - Commit message citing Finding B
  - Diff in `feature_extractor.py`'s `extract_range_composition`
    promoting `_per_villain_folded` / `_per_villain_composition` /
    `_per_villain_overflowed` from `chain_meta`
  - 4 new tests (`test_must46_per_villain_*_promoted_in_multiway`
    + HU-empty-dict regression)
- **Pre-stage** the C5.2 swap mechanics in your own head (or in a
  scratch note, NOT in the repo): which 3-way hands feed F3 (partial-
  fold) and F4 (all-live), what the expected
  `_per_villain_composition` payload shape will look like, what the
  hardening re-pass commands are
- **Pre-draft** the C5.2 commit message and the SHIP REPORT update
  text in scratch (not committed) so post-commit-14 execution is
  data-only + paperwork
- **Re-read** `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` +
  the addendum: when teaching unholds, the merge to teaching's own
  branch / master will follow the same PR pattern logic adopted

If a question surfaces during the wait: route via a comms doc per
`feedback_queries_to_orchestrator.md`, not AskUserQuestion.

## Cross-stream signal teaching is waiting for

| Trigger | Source | Teaching action |
|---|---|---|
| Commit 14 on origin/master | `git log origin/master` shows commit 14 SHA | Begin C5.2 fixture swap |
| Commit 16 + M4/M5 clean | Builder ping in v2 comms | None (orchestrator handles HOLD #1 → #4) |
| Pre-Stage-6 gate signal | Orchestrator comms doc | Drop PRE-VERIFICATION marker on SHIP REPORT |
| Merge greenlight | Orchestrator comms doc | Open PR `teaching/v4-1-nan-render` → master |

## C7 plan when it activates (reference, do not execute now)

When C7 finally runs (post-C5.2):

- One commit, doc-only
- `interface/l3_renderer_enriched.py:129` — update docstring per plan
  §C7 wording
- `interface/CONTENT_API.md` — schema-table entry gains description:
  *"Relative rank of hero's hand within the preflop opening range on
  this board (0-100%, preflop only)."*
- Note in CONTENT_API.md flagging cross-stream coordination item for
  game-team UI label update
- No renderer code change; the number produced is unchanged
- V3 compliance reviewer pass on wording (no directional framing,
  no WHY leak)
- No code run needed
- PR pattern (per push-policy decision): branch
  `teaching/v4-1-c7-wording`, PR to `teaching/v4-1-nan-render`,
  per-commit V3 review on the PR thread, `--merge` on approve,
  `--delete-branch`

## Risk note

The only scenario in which deferring C7 hurts: commit 14 lands with
unexpected complications (e.g. Finding B resolution doesn't match
the spec, requires fix-forward) and the teaching wait window
stretches significantly. Even then, doing C7 now wouldn't
*accelerate* the ship — it would just produce a held commit
sitting on a still-held branch. Same calendar, more complexity.

If commit 14 stalls > 3 days from today (2026-04-25), reassess. Not
an issue at current pacing.

## Reference

- `TEACHING_V4_1_NAN_RENDER_PLAN_2026-04-22.md` §C7 — the source
  recommendation
- `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md` —
  Finding B resolution / commit 14 spec
- `MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` + addendum —
  PR pattern teaching will inherit when it unholds
- `feedback_orchestrator_controls_parallel_timing.md` — held-stream
  discipline
- `feedback_quality_default_no_ask.md` — quality option chosen
  without re-asking owner

## Action

**Teaching:**

1. Hold C7. Don't start the wording-cleanup commit.
2. Stay on `teaching/v4-1-nan-render` HEAD = `0b6d4d3` with no new
   commits during the wait window
3. Monitor v2 origin/master for commit 14 landing
4. When commit 14 lands: execute C5.2 fixture swap → V3 review →
   then C7 → V3 review → SHIP REPORT update
5. If a cross-stream question surfaces: route via a teaching-comms
   doc, not AskUser

**Orchestrator (me):**

1. Track logic stream: GTO post-merge verdict on 13.2.5, then
   greenlight 13.3, then 14
2. When commit 14 lands: notify teaching via comms doc to begin C5.2
3. Run pre-Stage-6 gate when HOLD #1 / #3 / #5 all clear
4. Issue merge greenlight for teaching when gate passes

**Owner:** no action; briefed via this doc.
