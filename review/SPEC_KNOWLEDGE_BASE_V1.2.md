# Spec: Knowledge Base Update v1.1 → v1.2

**Date:** 7 April 2026
**Status:** APPROVED — implement before next labelling round
**Source:** Solver findings from GTO Wizard 6-max multiway 100bb

---

## 7 Changes (4 solver rules → specific insertion points)

### 1. Correct DO NOT Rule #2 (line 477-479)

Currently says semi-bluffs require "nut flush draw, combo draws"
but doesn't distinguish RAISE vs CALL. Add carve-out:
- Nut flush draw + blocker (e.g., As) + overcards/outs = RAISE
- Non-nut draws without blockers = check/call as before
- Source: MW-47 solver finding

### 2. Correct DO NOT Rule #6 (line 495-496)

Currently says "blockers matter ~40% less 3-way." Solver shows
blockers swing raise frequency by 40pp for the same hand. Amend:
- Blockers for bluff selection (which bluffs to choose) — less
  important 3-way
- Blockers for action selection (raise vs call with made hand /
  strong draw) — still critical

### 3. Add new reference data subsection (after Section 1.6)

**1.7 Semi-Bluff Conditions (Solver-Verified)**
- Table: conditions that make 3-way semi-bluff raising profitable
- Nut draw + blocker + side equity = raise
- Non-nut draw or no blocker = call/check
- Non-set made hands at mixed SPR = default CALL (can't express
  mixed strategies)

### 4. Add Worked Example 9 (after Example 8)

MW-47 pattern: AsQs on Ks Jd 5s, SB facing bet. Nut flush draw
+ As blocker + overcards + gutshot = RAISE. Walk through the
5-factor framework showing why this overrides the "don't semi-bluff
3-way" default.

### 5. Correct Example 3 (line 269-295)

This is the MW-30 pattern — currently recommends FOLD. Solver says
CALL. Add a footnote/correction noting that solver verification
showed KT top pair with 40% equity facing bet+call is a CALL, and
that the "action narrows ranges" reasoning was over-applied here.
Keep the example as a teaching tool but mark the action as CALL
with the corrected reasoning.

### 6. Update Factor 5 (Action History) (line 164-175)

Add qualifier to the bet-and-call signal: it narrows ranges but
does NOT automatically mean fold. Equity well above pot odds +
made hand = still CALL. The fold applies when hero's specific
holding is dominated by the narrowed range AND equity is close
to break-even.

### 7. Version bump to v1.2 with changelog entry.

---

## What Does NOT Change

- Sections 1.1-1.6 (reference data) — still correct
- Preflop construction (Section 3) — unchanged
- Examples 1, 2, 4, 5, 6, 7, 8 — unchanged
- DO NOT rules 1, 3, 4, 5, 7, 8 — unchanged

## Open Question

Should Example 3 (MW-30) be fully rewritten as a CALL example,
or kept as-is with a correction note? Rewriting is cleaner but
loses the teaching value of showing the over-fold trap.

**Owner decision needed before implementation.**

## After Implementation

- Re-generate agent_context.txt (prompt + updated knowledge base)
- Update checksums in docs/LABELLING_PIPELINE.md
- Re-run calibration exam to verify no regression
- Proceed with next labelling round
