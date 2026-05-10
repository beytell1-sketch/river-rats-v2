---
date: 2026-05-10
from: Builder stream
to: Main terminal (orchestrator)
re: PR #339 — QC heartbeat staleness observation (silent-signal threshold crossed)
status: OBSERVATION (no action requested; orchestrator decides)
---

# Observation — QC heartbeat stale on PR #339 audit

## Facts

- QC audit-now trigger: PR #340 merged to master `a8aab0c`; comm `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR339_PILOT_2026-05-10.md` landed at 13:58.
- Audit estimate per dispatch: 15-20 min wall-clock.
- Current time: ~14:13. Elapsed since trigger: ~15 min.
- `~/river-rats-qc/.last_seen_master_sha` = `c54eab1` (1 commit behind `a8aab0c`).
- `~/river-rats-qc/findings/` newest is `2026-05-10-pr335-phase15d2-full.md` (13:16). NO `2026-05-10-pr339-*.md` file present.
- No `review/comms/REVIEW_QC_PHASE15D3_PILOT_*` cross-post present.
- No PR #339 review/comment activity per `gh pr view 339`.

## Threshold reference

Per `project_qc_heartbeat_convention.md`: "QC tick MUST write `~/river-rats-qc/.last_seen_master_sha` at end of each tick; stale >2× cadence = real silent signal." Cadence inferred ~5m from prior PR audits → 2× = 10m. Currently ~15m and inside the upper-bound audit estimate window.

## Plausible causes (no judgment)

1. QC audit in progress; first heartbeat update will land at audit completion (no intermediate tick).
2. QC stream offline; standalone session not running.
3. QC tick crashed mid-audit.

I cannot distinguish (1) from (2)/(3) from the builder side.

## Builder posture

- Continuing polling loop at 270s cadence.
- No builder action authored in response to this observation.
- Surfacing per `feedback_check_comms_before_wait.md` + `feedback_queries_to_orchestrator.md` (cross-stream observations route to orchestrator via comm).

Orchestrator decides whether/how to escalate.
