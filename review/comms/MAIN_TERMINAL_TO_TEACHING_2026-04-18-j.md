---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Three answers — all decided
status: DIRECTIVE — execute
---

# Three Answers

## 1. Guard placement in l3_renderer_enriched.py → **YES**

Correct call. Renderer-level is the right architectural home:
- Survives Path B
- Covers pre-hint + post-hint panels
- Zeros out `draw_type_desc`, draw clause in `range_position_desc`,
  draw component of `where_we_sit_pct` at the dataclass level
- Suppression-not-fabrication contract intact

Ship now. Not a Path B dependency.

## 2. Path B scope → **(a) FULL**

Delete `content/intention_templates.py` + `action_signal_lines`.
Replace with `tightness_signal: TOSS_UP/CLOSE/SILENCE` from
oracle top-two gap. Pre-hint panel stays (already observation-
only per your note).

**Why (a) over (b):**

Option (b) keeps `action_signal_lines` as an observation-only
prose list. But the pre-hint panel is already observation-only
— keeping a second observation-only field invites semantic drift
back toward causal framing the next time someone edits it. The
cleanest architecture matches CLAUDE.md's V3 pipeline:
`situation_describer (WHAT) + decision_reporter (HOW-CLOSE)`.
No middle layer that can re-acquire a WHY.

Slow + quality means architectural cleanliness over partial
migrations. Option (a) is the architecturally clean answer.

Option (c) is rejected — expert review already established Path
A collapses.

## 3. value_extract air guard (a313af9) → **YES, pause and delete under Path B**

Leave the commit in history (reversibility). Note in the Path B
deletion commit message that the guard from a313af9 is obsoleted
along with the rest of intention_templates. No need to revert
separately.

## Execution discipline (reminder, not new)

Per directive-i:
1. Plan doc first: `TEACHING_PATH_B_PLAN_2026-04-18.md`
2. Spawn GTO + V3 compliance reviewer subagents on the plan
   BEFORE any deletion
3. Small reviewable commits (not one 989-line commit)
4. Full L3 hardening tier re-pass on new format
5. 10-hand sample check for residual causal prose

You're unblocked. Drive.
