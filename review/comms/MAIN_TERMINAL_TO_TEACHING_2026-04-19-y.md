---
date: 2026-04-19
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Teaching team instructions — begin plan v2 execution
status: DIRECTIVE — recentering LOCKED (directive-v, 80c8db4), write plan v2 now
---

# Teaching Team — Current Instructions

## Context

Owner approved the recentering in full. Directive-v at 80c8db4
locks:

- Primary window: range-first (range composition → numeric
  dashboard → decision + tightness)
- Flag window: 7 active flags + blocker placeholder
- L3 prose cuts: hand_bucket, hero_position, draw_type_desc,
  showdown_value_desc, position_desc, forward_plan_desc
- Schema: new `FlagEntry` dataclass, `flags: List[FlagEntry]`
  field, CONTENT_API v4.0

You're unblocked. Begin plan v2 execution per directive-v §Plan v2.

## Do now — write plan v2 doc

Location: `~/river-rats-teaching/review/comms/TEACHING_PLAN_V2_2026-04-19.md`

### Required contents

1. **Field-by-field diff table.** For every field in
   `EnrichedTeachingOutput`, show:
   - Current state (exists? content pattern?)
   - New state (keep / remove / relocate)
   - Render path (primary window / flag window / dashboard /
     audit-only / deleted)
   - Line references in `interface/l3_renderer_enriched.py`

2. **`FlagEntry` dataclass spec.** Fields, types, defaults,
   serialization, how the render pipeline decides when to emit
   each flag.

3. **Flag trigger table.** For the 7 active flags (commitment,
   deep-stack, danger, monotone, paired, connected,
   board-favour-hostile), specify:
   - Feature source and threshold
   - Neutral observation text template
   - Threshold constants (locked values)
   - Blocker flag: placeholder only — note gated on v2.4 logic
     features

4. **L3 removal list with call-site scan.** Each removed field
   needs every downstream reader/consumer identified:
   - Game adapter references
   - Scan_guard_leaks.py references
   - Any tests that expect the field
   - Any downstream tooling (`interface/generate_*.py` etc.)

5. **CONTENT_API v4.0 schema diff.** Before/after snippet,
   migration notes for consumers.

6. **New guard-leak category.** `directional_framing_words`:
   `[block, blocks, blocker, protect, protects, charge, charges,
   extract, extracts, deny, denies]`. Add to
   `scan_guard_leaks.py`. Any match in non-audit prose = leak.

7. **Game adapter migration path.** What fields the adapter
   needs to handle (new `flags` list, removed L3 prose fields,
   unchanged villain_*_pct fields for the range bar).

8. **Rollback plan.** Per-commit revert order if anything
   breaks.

9. **Test/hardening plan.** L3 hardening tier re-pass on new
   structure:
   - Guard-leak scan (pass on all categories including new
     directional-framing)
   - 10-hand manual sample across CLEAR / STANDARD / BOUNDARY
     difficulty
   - Adversarial suite for new flag-rendering code
   - Sample check for residual causal prose — 10 hands, zero
     directional-framing hits, zero WHY verbs

## Do next — expert review

Before ANY code change, spawn BOTH:
- **GTO reviewer subagent** — plan poker-accurate? flag
  thresholds defensible? observation texts factually correct?
- **V3 compliance reviewer subagent** — plan observation-only?
  flag texts pure? no causal smuggling?

Both must PASS. If either FLAGs or FAILs, revise plan and
re-review.

## Implementation discipline

Same as Path B:

- **Small reviewable commits.** Not one monolithic rewrite.
  Logical boundaries: dataclass change, flag registry, primary
  window reorder, each prose removal, new guard-leak category,
  CONTENT_API update.
- **Register the new guard-leak category early** (before
  deletions) so the hardening scan validates each increment.
- **Pre-existing backlog** (river-outs-parenthetical, plan-tag
  dedupe) stays backlog — don't absorb them into this pass.
- **Hold commit i alignment.** Blocker stays deleted; flag
  entry is a placeholder only. No code for blocker flag this
  pass.

## Do NOT do

- Do NOT design the blocker flag. Deferred to v2.4 logic
  features (nut_flush_block / draw_block_pct /
  nut_made_block_pct). Builder owns scoping those; you
  integrate after they land.
- Do NOT touch `range_position_desc` phrasing. It's locked
  primary teaching — stays as-is from Path B hardening.
- Do NOT re-introduce any intention prose or causal verbs,
  even under a different field name.
- Do NOT ship before L3 hardening passes.

## Cross-stream awareness

- **Game:** building range-bar UI on v2.2 that reads your
  `villain_*_pct` fields. Those fields stay unchanged; game's
  UI ships independent of your CONTENT_API v4.0 release.
- **Logic:** building pre-flight gate + scoping blocker
  features. Their v2.4 feature work informs your blocker flag
  design, but doesn't gate your plan v2 (blocker stays
  placeholder for now).
- **Playtest:** owner's hand-log system now captures teaching
  schema version (817b646). Logs from the v4.0 schema will tag
  distinctly; pre-v4.0 and post-v4.0 logs will be
  distinguishable.

## Timeline

- Plan v2 doc: 3-4 hours (comprehensive diff + scans + test
  plan)
- Expert review: 30-60 min (two subagents in parallel)
- Implementation: 1-2 days (small commits, hardening re-pass,
  sample check)

Total: ~2 days at owner's slow/quality pace.

## Ping cadence

- After plan v2 doc pushed: ping for reviewer verification
- After expert reviews pass: ping for green-light to start
  deletions
- After each non-trivial commit: push and note progress
- After full hardening passes: final ship report

Go.
