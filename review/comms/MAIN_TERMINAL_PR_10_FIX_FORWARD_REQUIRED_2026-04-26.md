---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #10 (Task 1 Protocol B v1.0) — APPROVE-WITH-NITS verdict; fix-forward to v1.0.1 required per quality-default discipline before merge
status: DIRECTIVE — 3 MEDIUM-severity findings to address; standing pattern from PR #1 (13.2.5 → 13.2.6) applies; fix-forward branch stage4-prep/protocol-b-fill-1-1
---

# PR #10 Fix-Forward Required — Protocol B v1.0.1

## Reviewer verdict summary

PR #10 verdict at `aa1c2f7`: **APPROVE-WITH-NITS** with 3 MEDIUM-severity findings. Reviewer's literal phrasing: "No blockers for owner review of the v1.0 design artifact."

However, per memory `feedback_quality_default_no_ask.md`:

> "Reviewer flag as MEDIUM / non-blocking → still address it;
> don't defer without reason"

The owner's standing instruction is to address MEDIUM findings before
proceeding. PR #10 is held pending fix-forward to v1.0.1.

## The 3 MEDIUM findings

### MEDIUM #1 — Example 1 internal consistency (Item D)

The pot/SPR math doesn't match the described action sequence. With
"CO opens, BTN call, BB call → flop checks through" at 100bb stacks,
preflop pot is ~9-12bb and flop pot stays unchanged through checks
→ turn pot ~9-12bb, NOT 80. "Pot 80, SPR 1.25" implies stacks ~100bb
behind, only consistent with ~180bb effective.

Step 2 also contains unfinished editorial drift: *"wait, hero is
TPGK against a turned flush; actually..."* — reads as draft
mid-revision.

**Fix-forward action:** either (a) recompute the situation: change
preflop action / stack depth to make pot 80 + SPR 1.25 self-
consistent, OR (b) re-author Example 1 with consistent pot/stack
math. Strip all "wait... actually" editorial fragments. Lock the
final example as a completed worked-trace.

### MEDIUM #2 — Anti-pattern #7 vs Example 2 tension (Item F)

Example 2 uses pot-odds math in Step 3 (CALL profitable: surplus
0.15 / 0.22 etc.) to derive surplus. Anti-pattern #7 explicitly
forbids equity-vs-pot-odds conflation in Steps 1-3. Either:

(a) Add a carve-out to Anti-pattern #7: "equity-derived-from-
   composition pot-odds math IS allowed in Step 3 for MW-30-style
   anchor cases where the math is composition-grounded, not
   precomputed equity-from-tracker"
   
(b) Defer Example 2's pot-odds math to Step 4 (post bucket
   cross-check) so the example's own trace doesn't fail
   Anti-pattern #7

Reviewer's note (Item F): "As written, Example 2's own trace would
FAIL grade against #7."

**Fix-forward action:** pick (a) or (b). (a) is shorter; (b) is
purer composition-first. Builder discretion on which preserves
protocol intent better.

Also fix Example 2 arithmetic: pot odds 30/(30+90) = **0.25** not
0.18; surplus then 0.15 not 0.22. Direction of conclusion (CALL
profitable) holds via MW-30 anchor; arithmetic does not.

### MEDIUM #3 — Verbatim-inlining for pilot build

[**This finding wasn't in the excerpts I read; please surface from
the verdict's full text and address per same fix-forward pattern.**]

Likely concern: the v1.0 prompt references shared resources (KB
sections, MUST citations, threshold values) verbatim — pilot build
needs these inlined OR resolved at dispatch time. Build pipeline
sanity check needed.

## NITs that can defer (NOT fix-forward blockers)

Reviewer also flagged NIT-level items per Item F:

- Possible missing Anti-pattern #11: "Don't mix per-villain and
  merged composition in the same trace without naming which you're
  using." MUST #46 folded-villain handling mentioned in Step 1 but
  not its own anti-pattern.
- Item C NIT: 4B rate floor not constrained or estimated; if pilot
  data has <5% 4B hands the cross-protocol signal becomes
  statistically thin. Suggest 4B-rate floor as a pilot design
  parameter (Task 5 scope, NOT Task 1).

These can fold into a wrap-up commit at end of Tasks 1-5 OR into
Task 5's pilot-orchestration-fill scope (4B-rate-floor finding
naturally belongs there). Builder discretion.

## Fix-forward workflow (mirror PR #1 → 13.2.6 pattern)

1. **New branch:** `stage4-prep/protocol-b-fill-1-1`
2. **Author dispatch:** address MEDIUM #1 (Example 1 self-
   consistency), MEDIUM #2 ((a) or (b)), MEDIUM #3 (verbatim-inlining
   per verdict's full text)
3. **Reviewer dispatch (different agent):** verify all 3 MEDIUMs
   addressed; flag any new issues; verify no new MEDIUM-severity
   issues introduced
4. **Open PR #11** with title "Stage 4 prep Task 1.1: Protocol B
   v1.0.1 (APPROVE-WITH-NITS fix-forward)"
5. **Standing PR pattern:** 4-checkpoint state protocol, verdict
   on PR thread, builder writes verdict comms, orchestrator merges
   on APPROVE
6. **PR #10 disposition:** orchestrator will merge PR #10 first
   (after fix-forward verdict is APPROVE), since the v1.0 is the
   baseline that v1.0.1 patches. ALTERNATIVELY: close PR #10 +
   merge only the v1.0.1 (cleaner history). Builder discretion.

[**ALTERNATIVE PATH (faster, less clean): merge PR #10 as-is now
+ fix-forward via v1.0.1 commit on top of merged v1.0.** This
preserves PR #10 as a milestone but means master has a transient
v1.0 with known issues. Quality default disfavours this.]

## Recommendation

Take the slow/quality path: **PR #10 stays open until v1.0.1
fix-forward lands**. Address the 3 MEDIUMs, push v1.0.1 as PR #11,
get APPROVE verdict, then orchestrator merges both (v1.0 first,
v1.0.1 second; OR closes #10 and merges #11 as the canonical v1.0).

Owner can override on read.

## Estimated fix-forward effort

~30-45 min for the 3 MEDIUMs (re-authoring Example 1 + restructuring
Example 2 / Anti-pattern #7 + verbatim-inlining check). Plus
reviewer dispatch ~15-30 min. Total ~1 hour.

## Cross-stream — unchanged

Tasks 2-5 sequencing unchanged. Builder can begin Task 2 (Protocol
C author dispatch) IN PARALLEL with the Task 1 fix-forward, OR stay
sequential (builder choice per their plan).

## Action

**Builder:**

1. Pick path: stay sequential (Task 1.1 first, then Task 2) OR
   parallel (Task 1.1 + Task 2 author dispatches concurrent)
2. Author dispatch on `stage4-prep/protocol-b-fill-1-1`
3. Reviewer dispatch (independent)
4. PR #11 per standing pattern
5. After PR #11 APPROVE: orchestrator merges (decides #10/#11 disposition then)

**Orchestrator (me):**

1. PR #10 held pending fix-forward
2. PR #11 (Task 1.1) merge per standing pattern after APPROVE
3. PR #10 disposition decided at v1.0.1 APPROVE moment
4. Loop continues at 15-min cadence; will catch fix-forward + Task 2 PR + further

## Reference

- `MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md` (`6201554`)
  — Stage 4 prep tasks directive
- `BUILDER_STAGE4_PREP_SCOPE_2026-04-26.md` (`1c63d93`) — builder's
  execution plan
- `aa1c2f7` — PR #10 reviewer verdict (APPROVE-WITH-NITS)
- `feedback_quality_default_no_ask.md` — "MEDIUM/non-blocking →
  still address; don't defer"
- PR #1 (13.2.5 → 13.2.6) — prior fix-forward precedent
