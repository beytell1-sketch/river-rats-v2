---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Path B completion review — CONDITIONAL APPROVAL, one missing commit
status: DIRECTIVE — add commit i (blocker-desc delete) before ship
---

# Path B Completion Review

## Strong work overall

All 8 planned commits landed per plan-v2. Expert review before
deletion. Small reviewable commits. Hardening re-pass
comprehensive. Quantified V3 compliance:

- 0 WHY-verb hits / 3,080 sentences × 8 fields
- 0 guard-leak hits across all categorized checks
- 36/241 adversarial hands correctly suppressed by false-draw
  guard
- 10-hand manual sample observation-only across difficulty bands
- ~3,100 lines of causal prose net removed

This is exactly the quality-focused execution the directive
asked for. Documentation refresh (CONTENT API v3.0) ships
alongside.

## One gap — `_blocker_desc` untouched

My directive `TO_TEACHING_BLOCKER_DIRECTIONAL_BUG_2026-04-18`
(commit 28328bc) asked for blocker-desc to be folded into Path
B as §1.6. It was filed after your plan was drafted, and it
looks like it slipped through implementation.

Current state, `interface/l3_renderer_enriched.py:541`:

```python
def _blocker_desc(fv: Dict[str, Any]) -> str:
    flush_block = fv.get("flush_block_pct", 0.0)
    flush_danger = fv.get("flush_danger", 0.0)
    if flush_block > _FLUSH_BLOCK_THRESHOLD and flush_danger > _FLUSH_DANGER_THRESHOLD:
        return f"Hero's cards block {flush_block * 100:.0f}% of villain's flush combos."
    return ""
```

Why this matters:
- The word "block" smuggles directional connotation (positive-
  for-hero) that's only true when hero is the aggressor
- For bluff-catchers, blocker actually hurts (removes villain's
  bluffs, makes remaining betting range value-heavy)
- Not caught by WHY-verb scan because "block" isn't a causal
  verb — it's a framing bias
- Not caught by guard-leak category list because blocker-
  direction wasn't registered as a category

Your guard-leak scan passing is honest — it's just scanning a
finite category list. The blocker directive added a new
category of violation after the plan locked.

## Required: Commit i — delete `_blocker_desc`

**Option B from my original directive** (delete entirely).
Student already has:
- Hero's two cards visible
- Board visible
- Villain range composition as percentages (via existing
  panels)

Student can derive "I hold a spade, two spades on board → I
block some villain flush combos" on their own — including the
correct directional interpretation for their specific action.
No system prose needed.

**Scope of commit i:**

1. Delete `_blocker_desc` function (lines 541-546)
2. Delete `blocker_desc` field from `EnrichedTeachingOutput`
   dataclass (line 126)
3. Delete `blocker_desc=blocker` assignment in `render_from_enriched`
   (line 725) and the helper call (line 662)
4. Update CONTENT_API.md: remove `blocker_desc` from the
   schema v3.0 doc; regenerate examples
5. Check `interface/l3_renderer.py:374 _blocker_sentence`
   (legacy renderer) — delete if it has the same pattern
6. Update `interface/scan_guard_leaks.py:171` — remove
   `out.blocker_desc` reference
7. Search for any downstream test expecting `blocker_desc` to
   exist; update or delete

**After deletion:**

- Re-run guard-leak scan (should still be 0/0/0 on all
  registered categories)
- Re-run the 10-hand sample check — confirm no output still
  emits blocker prose
- Update hardening report with a one-line addendum

**Expected outcome:** pure observation-only output surface
with ZERO causal-adjacent prose remaining.

## Also register a new guard-leak category

Add to `scan_guard_leaks.py` a check for directional framing
words in pre-hint prose:

```
DIRECTIONAL_FRAMING_WORDS = [
    "block", "blocks", "blocker",  # directional
    "protect", "protects",         # directional
    "charge", "charges",           # directional
    "extract", "extracts",         # directional
    "deny", "denies",              # directional
]
```

These words imply hero-benefit or hero-action interpretation.
Under strict V3, they shouldn't appear in observation-only
prose (they can appear in decision_reporter tightness signal
prose if that ever warrants it — but not in pre-hint
observations).

This future-proofs against the next directionally-biased
addition slipping through.

## Timeline

Commit i should be small — 1-2 hours including hardening
verification. Path B otherwise ready to ship at 8ed2396; just
add i and this is done.

## Cross-stream update — teaching needs to know

Your report says "v2.3.1 model: ships independently (Builder
gates on broader-inference sweep)." That's stale. Actual status:

- v2.3.1 self-play FAILED (systemic regression caught)
- v2.3.2 trained with balancing value-BET counter-examples
- v2.3.2 passed litmus (both air + value 95-99%) but FAILED
  Tier 1 holdout gates (FB-40 70%, MW-50 78%)
- Currently in α+β triage: self-play + per-hand panel re-audit
- Ship/revisit decision pending joint report

So game adapter gates on BOTH:
- Logic side: v2.3.2 ship decision from triage (TBD)
- Teaching side: Path B ready at 8ed2396 + commit i

No cross-stream blocking; just keeping you in the loop.

## Not in scope for commit i

- River-outs-parenthetical pre-existing issue (backlog, agreed)
- Plan-tag dedupe (backlog, agreed)
- Adding new observation-only features
- Re-running full adversarial suite (only blocker paths changed;
  targeted re-run sufficient)

Go on commit i. Ping when hardening addendum confirms clean.
