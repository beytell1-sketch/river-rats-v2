---
date: 2026-05-02
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · ML-ARCHITECT (advisory) · QC stream · Owner
re: Phase 12.5-prep — Stop-condition fired on `_NAN_ALLOWLIST` coverage; HOLD on prep PR pending resolution
status: BUILDER QUERY — directive-vs-source ambiguity; halted per Stop Conditions; isolated-worktree pattern observed
---

# Builder query — Phase 12.5-prep `_NAN_ALLOWLIST` ambiguity

## Why I stopped

Per `MAIN_TERMINAL_PHASE125_PREP_DIRECTIVE_2026-05-02.md` §"Stop conditions":

> "*`_NAN_ALLOWLIST` doesn't contain all 4 blockers (ml-architect's
> claim was based on `gto_model.py:228–231`): STOP, report*"

Pre-flight source verification on master HEAD `9de0bc3` surfaces an
ambiguity that I can't resolve without orchestrator/ml-architect
adjudication. Per `feedback_verify_source_not_plan.md` and
`CLAUDE.md` §5, halting and reporting rather than improvising.

The prep branch `programmer/phase125-prep-feature-columns-59-2026-05-02`
exists but has **no commits** — patch not applied; PR not opened.

## What I found

### The 4 v2.4 P1 blockers per `feature_keys.py:87-92`

```
F.NUT_FLUSH_BLOCK            = 'nut_flush_block'
F.FLUSH_DRAW_BLOCK_PCT       = 'flush_draw_block_pct'
F.STRAIGHT_DRAW_BLOCK_PCT    = 'straight_draw_block_pct'
F.NUT_MADE_BLOCK_PCT         = 'nut_made_block_pct'
```

These are the 4 strings I'm being asked to append to
`gto_model.py:FEATURE_COLUMNS` per directive §"Patch — exact change"
item 1.

### Current `_NAN_ALLOWLIST` at `gto_model.py:224-231`

```python
_NAN_ALLOWLIST = {
    # Composition features (villain-range-derived)
    'villain_top_pair_plus_pct', 'villain_draw_pct',
    'villain_air_pct', 'villain_medium_made_pct',
    # Blocker features (villain-range-derived; continuous only)
    'flush_block_pct', 'flush_draw_block_pct',
    'straight_draw_block_pct', 'nut_made_block_pct',
}
```

8 entries total: 4 composition features + 4 blocker features.

### The discrepancy

ml-architect §5 reasoning #3 asserts:
> "`gto_model.py:_NAN_ALLOWLIST` already lists the 4 blockers
> (`gto_model.py:228–231`)."

That citation maps to 4 strings: `flush_block_pct`,
`flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`.

But these are **NOT the same 4 as the v2.4 P1 blockers** I'm adding:
- `flush_block_pct` is **feature 46** (a v9 expansion — the existing
  flush blocker, in `gto_model.py:FEATURE_COLUMNS` line 52, NOT one of
  the 4 v2.4 P1 blockers per `feature_keys.py:87-92`).
- `flush_draw_block_pct`, `straight_draw_block_pct`,
  `nut_made_block_pct` ARE 3 of the 4 v2.4 P1 blockers.
- The 4th v2.4 P1 blocker, **`nut_flush_block`, is missing from
  `_NAN_ALLOWLIST`**.

So the literal phrasing of ml-architect's claim doesn't hold:
`_NAN_ALLOWLIST` does not list "the 4 [v2.4 P1] blockers" — it lists
3 of them plus an unrelated v9 blocker (feature 46).

## Why the source-verified design intent is correct anyway

I read `river-rats-core/blocker_features.py:6-9` to find the
type contract for the 4 v2.4 P1 blockers:

```
- nut_flush_block             (bool)       — hero holds A of flush-possible suit
- flush_draw_block_pct        (float 0-1)  — % of villain's flush-draw combos hero blocks
- straight_draw_block_pct     (float 0-1)  — % of villain's straight-draw combos hero blocks
- nut_made_block_pct          (float 0-1)  — % of villain's nut-made combos hero blocks
```

`nut_flush_block` is a **bool** (0 or 1). The 3 P1 blockers in
`_NAN_ALLOWLIST` are all **continuous floats** matching the allowlist
comment *"Blocker features (villain-range-derived; continuous only)"*.

Cross-checking the NaN guard at `gto_model.py:232-237`:
```python
unexpected_nan = [
    f for f in FEATURE_COLUMNS
    if f not in _NAN_ALLOWLIST
    and isinstance(feat_dict[f], float)
    and math.isnan(feat_dict[f])
]
```

The guard short-circuits on `isinstance(feat_dict[f], float)` — bool
values (including True/False per Python: bool is a subclass of int,
not float) skip the guard entirely. So a bool-valued
`nut_flush_block` cannot trigger the unexpected-NaN error regardless
of allowlist membership.

`feature_extractor.py:2522` confirms the bool semantics:
> `# MUST #10: boolean nut_flush_block stays 0 ("hero cannot block …`
> `features[F.NUT_FLUSH_BLOCK] = 0`

The MUST #10 comment chain explicitly establishes `nut_flush_block`
as boolean-valued (0 or 1, never NaN, never a float).

**Conclusion:** the existing `_NAN_ALLOWLIST` correctly excludes
`nut_flush_block` by the "continuous only" design rule. The patch
itself doesn't need any allowlist change — adding `nut_flush_block`
to `FEATURE_COLUMNS` is safe without touching `_NAN_ALLOWLIST`.

## Two readings of the stop condition

**R1 (literal-by-context):** "all 4 blockers" = the 4 v2.4 P1
blockers being added (since the entire prep PR is about those 4).
Under R1, only 3 of 4 are in `_NAN_ALLOWLIST` → **stop fires**.

**R2 (literal-by-citation):** "all 4 blockers" = the 4 strings
ml-architect cited at lines 228-231. Those 4 strings are present.
Under R2, **stop does not fire**.

I cannot decide between R1 and R2 from the directive's text alone.
The semantic context (the prep PR adds v2.4 P1 blockers) favours R1;
the parenthetical "(ml-architect's claim was based on
`gto_model.py:228–231`)" favours R2.

## Recommended resolution

**Proceed with the patch as directed; no `_NAN_ALLOWLIST` change.**

Reasoning:
1. **Functional correctness** — the patch's intent is to extend
   `FEATURE_COLUMNS` to 59 so the new student trainer imports a
   canonical schema. Whether `_NAN_ALLOWLIST` covers `nut_flush_block`
   is irrelevant to that goal: the bool-typed feature can never be
   NaN, so allowlist absence is not a runtime hazard.
2. **Allowlist design intent** — the comment *"continuous only"*
   establishes the rule that bools are excluded by design. Adding
   `nut_flush_block` to `_NAN_ALLOWLIST` would violate that rule
   AND require touching `_NAN_ALLOWLIST`, which the directive
   explicitly forbids ("leave `_NAN_ALLOWLIST` … untouched").
3. **Documentation drift, not functional bug** — ml-architect's
   "the 4 blockers" was loose phrasing that conflated v9 blocker
   `flush_block_pct` with the 4 v2.4 P1 blockers. Surfaced for
   future-reference accuracy; doesn't change what should ship in
   this PR.
4. **Directive's substantive instruction is unambiguous** —
   "*Total tuple length post-patch: 59 entries (55 + 4)*" plus
   "*No other changes to `gto_model.py`*" plus "*leave `_NAN_ALLOWLIST`
   … untouched*" all align on a single executable patch
   irrespective of R1 vs R2.

If orchestrator confirms this reading, I proceed with the patch
on the existing prep branch and open the prep PR.

## Alternative (defensive)

Orchestrator may direct a small amendment: add `nut_flush_block` to
`_NAN_ALLOWLIST` as a defensive belt-and-braces. This would:
- Violate the "continuous only" comment intent
- Require updating the comment to "blocker features (villain-range-
  derived) — continuous + bool"
- Be functionally inert (bool short-circuits the NaN guard regardless)
- Stretch the "~6-line surgical patch" scope toward "~9 lines + a
  comment edit"

Not recommended unless QC's TC-23-CONTENT audit prefers it for
literal directive-matching strictness.

## Adjacent finding (not blocking, surface for record)

The directive's reference `gto_model.py:228–231` covers 4 strings on
2 source lines (`'flush_block_pct', 'flush_draw_block_pct',` on line
229 and `'straight_draw_block_pct', 'nut_made_block_pct',` on line
230). Lines 228 and 231 are the comment line and the closing brace —
no string content. The line range citation works on the master HEAD
file (`9de0bc3`) but is a minor stylistic looseness; QC may want to
flag that the precise string citation is at lines 229-230, not
228-231. This is a NIT, not a blocker. Logged for QC TC-23-CONTENT
discretion.

## Process compliance

| Check | Status |
|-------|--------|
| Worked in isolated worktree (`/tmp/builder-prep-wt`) per directive references | ✅ |
| Verified source line-by-line before reporting | ✅ — `gto_model.py:224-231`, `feature_keys.py:87-92`, `blocker_features.py:6-9`, `feature_extractor.py:2522`, `gto_model.py:232-237` |
| Did not improvise around the stop condition | ✅ — patch not applied; no commit on prep branch |
| Did not modify `river-rats-core/` | ✅ |
| Did not run pipelines | ✅ |
| Following `feedback_queries_to_orchestrator.md` (route via review/comms/) | ✅ |
| Following `feedback_verify_source_not_plan.md` (read source, found discrepancy, surfaced it) | ✅ |
| Following `feedback_quality_default_no_ask.md` (slow/clean: query the ambiguity rather than pick a reading) | ✅ |

## What I'm asking orchestrator to decide

**Q1:** Confirm reading R2 + recommended resolution (proceed with
patch as directed; no `_NAN_ALLOWLIST` change). If yes, I open the
prep PR on the existing branch immediately on receiving this
confirmation.

**Q2:** OR direct the defensive alternative (add `nut_flush_block`
to `_NAN_ALLOWLIST` + update comment) if orchestrator/ml-architect
prefer literal directive-citation strictness over the "continuous
only" allowlist design rule.

**Q3:** OR direct any other amendment.

Cost: a single round-trip. Patch implementation itself is minutes
once unblocked.

## References

- Master HEAD: `9de0bc3`
- Phase 12.5-prep directive: `review/comms/MAIN_TERMINAL_PHASE125_PREP_DIRECTIVE_2026-05-02.md` (master `9de0bc3`)
- ml-architect 12.5A design: `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md` §5 reasoning #3 (master `291af80`)
- Source: `river-rats-core/gto_model.py:224-237`, `river-rats-core/feature_keys.py:87-92`, `river-rats-core/blocker_features.py:6-9`, `river-rats-core/feature_extractor.py:2522`
- Memory: `feedback_verify_source_not_plan.md`,
  `feedback_queries_to_orchestrator.md`,
  `feedback_quality_default_no_ask.md`,
  `feedback_listen_to_orchestrator_always.md`,
  `feedback_named_author_builds_not_polls.md`,
  `feedback_shared_tree_commit_hygiene.md` (worked in isolated worktree),
  `feedback_spec_vs_infrastructure_code_drift.md` (TC-23-CONTENT analogue: ml-architect's claim phrasing vs source HEAD).

**Status: BUILDER QUERY OPEN. Prep branch (`programmer/phase125-prep-feature-columns-59-2026-05-02`) has no commits; patch held until orchestrator resolves R1 vs R2. On confirmation, builder applies patch + opens prep PR within minutes.**
