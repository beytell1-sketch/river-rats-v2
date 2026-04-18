---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Blocker description is directionally biased — fold into Path B
status: DIRECTIVE — include in Path B scope
---

# Blocker Description — Directional Bug

Owner surfaced a real teaching bug in the same class as the
false-draw one.

## The bug

`interface/l3_renderer_enriched.py:541`:

```python
def _blocker_desc(fv: Dict[str, Any]) -> str:
    flush_block = fv.get("flush_block_pct", 0.0)
    flush_danger = fv.get("flush_danger", 0.0)
    if flush_block > 0.05 and flush_danger > 0.20:
        return f"Hero's cards block {flush_block * 100:.0f}% of villain's flush combos."
    return ""
```

## What's wrong

1. **Directionally biased wording.** "Blocks" in poker parlance
   connotes "you're helping yourself" — which is only true when
   hero is the aggressor. For bluff-catchers, the same blocker
   is negative (reduces villain's bluff combos, making the
   remainder value-heavy).

2. **Fires direction-blind.** Same sentence regardless of hero's
   action, oracle recommendation, or whether hero is facing a
   bet.

3. **Low thresholds.** 5% block + 20% board danger triggers on
   almost every two-tone board where hero holds a card of the
   dominant suit. Fires constantly.

## Owner's example (canonical bluff-catch miss)

Hero holds Jack of spades with middle pair on a two-spade board,
facing a bet from CO. Current pipeline says "hero blocks X% of
villain flush combos" — implies positive. Reality: villain's
betting range contains some semi-bluff flush draws; blocking
those REMOVES bluffs from villain's range, making the remaining
range more value-weighted. Hero's bluff-catch is WORSE, not
better.

## Fix — fold into Path B

This is the same V3 violation as the intention templates. The
sentence is not explaining WHY explicitly, but the word "block"
smuggles a directional interpretation. V3 compliance requires
directional neutrality.

**Option A (observation-neutral rewrite):**

```
"X% of villain's flush combos contain a card in hero's hand."
```

Factual, directionally neutral, student constructs the
interpretation.

**Option B (delete entirely):**

Flush-blocker awareness is arguably L4+ material. L3 student
already has the raw data:
- Hero's cards visible
- Board cards visible
- Villain range composition shown as percentages
Student can derive "I hold a spade, two spades on board, so
villain's flush combos are reduced." No need for system prose.

**Recommend B.** Same reasoning as the `action_signal_lines`
delete: any prose that labels a feature as noteworthy for the
current decision is adjacent to WHY. Under strict V3 compliance
(directive-n), pre-hint should be raw observations; this
sentence is a system-opinion dressed as observation.

If you go A instead, run it through the GTO + V3 reviewer
subagents before landing — the word "remove" / "reduce" might
still smuggle direction depending on phrasing. B is the safer
quality-focused answer.

## Scope

- Add to the Path B plan as §1.6 or similar (after §1.5
  pre-hint sentence scrub)
- Same commit discipline: small, reviewable, expert-reviewed
  before landing
- L3 hardening re-pass covers this change alongside the rest
- Search the codebase for any other "block" / "blocker" prose
  emissions with the same directional bias

Related: `l3_renderer.py:374 _blocker_sentence` — check the
legacy renderer has the same pattern; fold into Path B cleanup
if yes.

## Note on feature itself

`flush_block_pct` and `flush_danger` are useful NUMERIC
features for the oracle and for observation-only pre-hint
display (e.g., as a raw percentage in the range panel).
Keeping the data, changing the prose.

No static override, no causal explanation — just remove the
directionally-biased sentence.
