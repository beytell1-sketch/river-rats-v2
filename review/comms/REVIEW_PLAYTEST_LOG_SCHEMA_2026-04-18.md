---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Game builder
re: Playtest log schema review — core solid, three gaps to close
status: DIRECTIVE — close 3 gaps before handing real logs to logic team
---

# Playtest Log Review — Verdict

Logs reviewed: both files in `~/river-rats-game/playtest-logs/`.
One real-backend log (e635f992, oracle v2_3_model_shipped.json,
1 logged entry with logic feedback), one mock-backend log
(4dc31ce7, oracle mock).

## What works — core is solid

All six essentials from directive-m are hit. Owner can keep
logging with the current schema; structure is correct.

- **Reproducibility payload:** villain hole cards (all 5), full
  5-card board runout, seed, final pot, winner, showdown_reached
  all captured in `ground_truth.ground_truth`. ✅
- **Visible vs ground-truth split:** clean parallel `player_visible_
  state` and `ground_truth_state`. Hero's river decision visible
  as null (abandoned); ground_truth terminal shows full showdown
  with villain cards. ✅
- **Terminal / showdown data:** villain hole cards per position,
  winner field, final pot. ✅
- **Session metadata:** session_id persists across reloads,
  start/end/hands_in_bundle/hands_logged, seeds + preflop scenarios
  in bundle_config. ✅
- **User vs oracle actions:** `user_actions[].matched_oracle`
  flag diagnoses whether feedback is about oracle judgment or
  hero deviation. ✅
- **Explicit feedback booleans:** `has_teacher_feedback` /
  `has_logic_feedback` + per-team counts in top-level `counts`
  block. ✅
- **Feature vector:** 55/55 FEATURE_COLUMNS populated in
  `oracle_output.features` (including board_adjusted_hrp). ✅
- **Model provenance partial:** `oracle_model_filename` +
  `oracle_model_sha256` populated for real-backend runs. ✅

## Three gaps — close before next playtest hand-off

### Gap 1 — SHAP attributions always empty

`oracle_output.feature_attention = {}` in every entry. This is
the key debug signal for logic team ("which features pushed the
oracle toward this action?"). Without SHAP, they can re-run the
pipeline but can't see the attribution ordering.

**Fix:** wire `shap_explainer` into the real_oracle adapter.
Populate `feature_attention` with the per-feature SHAP values
for the predicted action class. Non-blocking for current
logging but required before serious logic-team review.

### Gap 2 — Repo commit provenance null

```
"oracle_repo_commit": null,
"teaching_repo_commit": null,
```

Only `game_build_commit` is populated. When a log comes back in
a week, reproducing the exact upstream state needs to know which
v2-core and teaching commits were live at the time. Model sha256
helps (good), but repo commits are the full chain.

**Fix:** in the real-backend adapters, capture `git rev-parse
HEAD` from `~/river-rats-v2` and `~/river-rats-teaching` at
session start (or per-log). Populate both fields. Cheap.

### Gap 3 — `teaching_schema_version` null

Currently always null. Becomes critical once Path B lands — we
need to know whether a logged entry was generated pre-Path-B
(with `action_signal_lines` and `intention_templates`) or
post-Path-B (with `tightness_signal`, no intention prose).

**Fix:** teaching side publishes a schema version string (e.g.,
`"path_b_v1"` vs current `"phase_2_tier_a"`). Game adapter
reads it and populates the field. Coordinate with teaching
terminal.

## Minor observation — mock vs real

The 14:36 log is mock backends. For any log intended to inform
the builder, confirm the server's `[saved]` line and verify the
saved file has:

```json
"oracle_backend": "real"
"teaching_backend": "real"
"oracle_model_filename": "<non-null>"
```

If those are null or "mock," the log is against the mock
backends and the feedback doesn't reflect real v2.3.1/v2.3.2
behavior. Quick sanity check worth automating — if any logged
hand has `oracle_backend != "real"`, show a warning banner at
the top of the exported JSON.

## Priority

- Gap 1 (SHAP): highest — logic team needs it to debug
  findings efficiently
- Gap 2 (repo commits): high — cheap to fix, high reproducibility
  payoff
- Gap 3 (teaching schema version): coordinate with teaching
  Path B landing; ship together
- Minor (mock warning): nice-to-have; prevents silent mock logs

## Owner can keep logging

Current schema is enough for builder to read and act on specific
findings. The gaps above are about making future logs more
self-contained and diagnostically richer — not blockers on today's
logging.

When owner hands a log to the logic team, include the entry's
`reproducibility.oracle_model_sha256` so the team runs against
the matching model.
