---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Vocab gap flagged during air-CHECK labelling — `check_give_up` concept
status: FYI — not a v2.3.1 blocker; for vocab-registry review
---

# Vocab Gap — "Check to Realize Equity Cheaply"

## What happened

During v2.3.1 Layer 2 labelling (air-CHECK counter-examples),
panel 01 flagged a missing street-plan vocab term:

> Proposed tag: `check_give_up`
> Meaning: "check air intending to realize equity cheaply on
> river"

Builder used `check_pot_control` as closest approved fit.

## Why the gap is genuine

Current approved street-plan vocab has:
- `check_pot_control` — "I have something to protect; keep pot
  small; avoid bloating with a medium hand"

This doesn't semantically cover:
- `check_give_up` / `check_realize_equity` — "I have nothing;
  check to see showdown cheaply and realize whatever equity
  remains without investing more"

Different hand states, different student framing:
- pot_control: hero has value, signal is "don't get bloated"
- give_up/realize_equity: hero has air, signal is "cheap river,
  maybe improve, maybe fold to bet"

## Not a v2.3.1 blocker

- Builder used closest approved vocab; oracle labels are
  unaffected (labels are action, not tag)
- Teaching output can derive the correct framing from hand
  state (is_made=0, has_showdown_value=0) without the tag
- Layer 3 value_extract air guard you're working on may
  naturally surface the same gap — worth watching

## What I'd like

Review this during your vocab-registry work. If the `check_give_up`
or equivalent concept belongs in approved vocab:
- Add it to the registry
- Consider whether it's L3 or belongs in Phase 3 L2/L1
- Ping back if you want builder to relabel any hands with the
  new tag (most likely no; it's a street-plan tag, not action)

No timeline pressure. Just flagging.
