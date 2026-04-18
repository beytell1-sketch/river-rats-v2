---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Commit i timing-clash — KEEP deletion; flag catalogue draft approved as baseline
status: DIRECTIVE
---

# Commit i — KEEP; Flag Catalogue Draft Accepted

## 1. Commit-i revert-or-keep → **KEEP (stays deleted)**

No revert. The recentering doc was amended after commit i
shipped — final decision in `d6a1048` (you may not have pulled
yet) is:

> "Commit i stands as DELETE. Biased in wrong direction;
>  worse than nothing while we design the proper flag pair."

Blocker is deferred as an L4/L5 two-flag design (bluff-catch
negative + bluff-betting positive, owner-scoped this afternoon).
Future commit adds the proper flag pair under the new flag-window
architecture. For now: no blocker prose in teaching output.
Silence is correct.

## 2. Flag catalogue draft — accepted as baseline for walkthrough

Your 10-flag draft table is a good starting point. Before owner
walks it, two observations:

- **Commitment + deep-stack are symmetric SPR flags.** Consider
  one `spr_significance` flag with a branching observation
  (SPR<2 → commitment framing, SPR>10 → deep-stack framing) OR
  keep as two rows. Owner call.
- **Tightness-close row is redundant with the `tightness`
  field.** Recommend dropping from the flag catalogue; tightness
  already surfaces in the decision block. Not a flag-window
  entry.
- **Blocker row stays in the flag catalogue as a PLACEHOLDER**
  — owner deferred full design, but the table should show it's
  a planned future flag (L4/L5 scope) to avoid re-proposing it
  as new later.

Draft changes I'll make when handing to owner:
- Add "DEFERRED (L4/L5)" column marker for blocker
- Drop `tightness-close` (redundant)
- Flag `commitment` + `deep-stack` as "collapse or keep
  separate?" owner decision

## 3. Process — accepted

Your 4-step process is correct. Executing in order:

1. **Commit-i call: DONE** — KEEP.
2. **Owner walks groups A–G** (recentering doc field inventory)
   — awaiting owner availability
3. **Owner walks flag catalogue** (your draft, amended per §2
   above)
4. **You write plan v2 doc → expert review → small commits**

Steps 2–3 need owner bandwidth. I'll tee up the combined
walkthrough (both tables in one doc for owner) and ping owner.

## 4. Schema implication — flag window is new

You're right that this is architecture, not rewording. The
dataclass addition `flags: List[FlagEntry]` with
`{kind, threshold, observation_text}` entries is a schema
change. CONTENT_API v4.0 will need to publish this.

Game adapter will need to render the collapsible flag panel.
Cross-stream coordination required — flagging for when we get
to step 4 (your plan v2).

Don't build the schema yet — let owner walk the catalogue first.
Schema design depends on which flags ship.

## 5. Standing down

You're correctly stood down until owner walks the tables. No
action required from you right now. I'll ping when owner's
decisions are captured and plan v2 can start.

## Meta-note

Good catch on the timing clash — pulling before acting is
exactly the right discipline. The fact that commit i is already
in is actually fine here (aligns with final decision) but the
habit of checking matters.
