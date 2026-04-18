---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Game builder
re: Hand-log feedback system — design review + essentials for v1
status: DIRECTIVE — implement essentials before ship
---

# Hand-Log System — Design Review

Design is on the right track. The two-textarea / localStorage /
JSON export shape matches owner's spec. Six additions required
before v1 ships — all tied to owner's "exact way it played out,
not just what's on screen" requirement. These are essentials,
not nice-to-haves.

## ESSENTIAL additions (must be in v1)

### 1. Full reproducibility payload

A logged hand must be re-runnable through the pipeline from the
payload alone. Current snapshot is close — add:

- **All hole cards** including every villain's cards, not just
  what the UI revealed at each street
- **Pre-baked RNG seed** if hands are generated with one; or
  explicit card-order list so the deal is deterministic
- **Per-decision feature vector** (the 110-feature array that
  went into the oracle at each decision point)
- **Per-decision oracle output**: full action probability
  distribution (BET/CHECK/CALL/RAISE/FOLD), top-two gap
  (tightness signal), size bucket if applicable
- **Per-decision SHAP attributions** if available (for the
  logic team to debug "why did oracle say X here")
- **Board runout** including future streets even if hand ended
  early (fold on flop → still log what turn/river would have
  been)

Rule of thumb: if a logic-team engineer can't reproduce the
oracle's decision by running the payload through the pipeline,
the payload is incomplete.

### 2. Schema + version tagging at payload root

Every entry gets:

```json
{
  "log_schema_version": "1.0",
  "oracle_model": "v2_3_1_model.json",
  "oracle_model_sha256": "<hash>",
  "teaching_schema_version": "path_b_v1",     // or current pre-Path-B
  "game_build_commit": "<git sha of the prototype>",
  ...
}
```

Without this, a log returned a week from now is ambiguous
about which model/teaching generated the finding.

### 3. User-visible vs ground-truth separation

Split the snapshot into two parallel views:

```json
"player_visible_state": { /* what the UI showed at log time */ },
"ground_truth_state":   { /* all cards, all oracle internals */ }
```

Owner's requirement: "not just what can be seen on screen."
Both views in the log; teams can analyze either.

### 4. Terminal / showdown data

When the hand concludes (before or after logging):
- Villain hole cards revealed
- Final board
- Winner + pot size
- Showdown equity vs actual result

If the user logs mid-hand and abandons, capture `hand_status:
"abandoned_at_street_X"` instead of terminal data.

### 5. Session metadata

Single header block at top of exported log:

```json
{
  "session_id": "<uuid>",
  "session_start": "<iso>",
  "session_end": "<iso>",
  "hands_played": N,
  "hands_logged": M,
  "oracle_model": ...,
  "teaching_schema_version": ...,
  "game_build_commit": ...,
  "entries": [ ... ]
}
```

Teams process the header once, then iterate entries. Avoids
per-entry metadata duplication on the consumer side.

### 6. Empty-feedback flag in export

Owner's spec: empty feedback box → team ignores that hand.
Make this explicit in the JSON:

```json
"feedback_to_teacher": "",
"feedback_to_logic":   "Oracle says call, but ...",
"has_teacher_feedback": false,
"has_logic_feedback":   true
```

Each team's consumer can filter on `has_<team>_feedback` without
string-length checks. Small, obvious, avoids "whitespace counts
as empty?" ambiguity.

## NICE-TO-HAVE (defer to v1.1 unless easy)

- Quick-tag buttons alongside free-text (false-draw, wrong-
  action, WHY-language, teaching-too-terse, etc.)
- Per-decision marker — user clicks "this street's decision
  is the issue" to pinpoint which decision inside the hand
- Replay tool (`scripts/replay_log.py <log.json>`) that takes
  a logged hand and runs it back through the pipeline

These add polish but don't block v1. Ship essentials first.

## Git hygiene

Session logs go to a dedicated folder:
- Suggest `~/river-rats-game/playtest-logs/` locally
- Add to `.gitignore` — raw playtest data shouldn't auto-commit
- Teams pull specific logs by hand when reviewing findings

## Verification before ship

Before owner's first playtest session:

1. Log one real hand, export, confirm every field populated
2. Hand the JSON to builder: can they re-run the oracle
   decision from the payload? If yes, payload is complete.
3. Hand the JSON to teaching: can they see the teaching output
   + context for any feedback-to-teacher entry? If yes, good.
4. Reload the page mid-session, confirm localStorage persistence
   works across refresh

If any of those fail, fix before playtest.

## Why this scope

Owner's explicit constraint: "exact way it played out, not just
what's on screen." That's what drives items 1, 3, 4. Without
those, logged findings lose fidelity and teams can't reproduce.

Items 2 and 5 are so the log remains interpretable over time
— logs opened a week later need to say which model/schema
generated them.

Item 6 is the minimal surface to match owner's "empty → ignore"
spec unambiguously.

Go.
