# Restart Prompt — Main Terminal / Orchestrator (2026-04-21)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats v2 main reviewer/orchestrator terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching

Also confirm ~/river-rats-game/ is present (local only, not on GitHub).

Working directory: ~/river-rats-v2
Role: orchestrator — cross-stream coordination, manifest owner,
directive writer, multi-agent review escalation, approval gates

Read these files in order before doing anything else:
1. ~/river-rats-v2/CLAUDE.md
2. ~/river-rats-v2/RELEASE_MANIFEST.yaml (integrated approved state; v1.6 — YOU OWN THIS)
3. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md (shared snapshot)
4. ~/river-rats-v2/review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md (current v2.4 gate)
5. ~/.claude/projects/-home-rupert-river-rats-v2/memory/MEMORY.md (memory index — READ EVERY REFERENCED FILE)

Key memories (priority order):
- feedback_recommend_dont_defer.md — DECIDE and EXECUTE; bar for
  asking owner is ABSOLUTELY NECESSARY; default recommendation is
  quality-focused slow-moving
- feedback_multi_agent_review_for_load_bearing.md — 4-6 parallel
  reviewers default for load-bearing/cross-component changes;
  don't ask, escalate
- user_owner_style.md — slow/quality, no rush; key judgments in
  chat, not long reports
- feedback_no_manual_overrides_in_labelling.md — HARD RULE; no
  static overrides anywhere
- feedback_counter_example_balance.md — single-class injection
  shifts surface systemically
- feedback_concentration_effect.md — narrow-texture clustering
  amplifies bias even with panel-correct labels
- feedback_class_balance_needs_both_classes.md — pruning/
  reweighting can't teach boundaries
- user_teaching_philosophy.md — range-based thinking central;
  teaching highlights WHAT not WHY
- project_board_adjusted_hrp.md, project_self_play_retest_v23.md —
  project context tickets

Current cross-stream state (per manifest v1.6):

Deployed:
- Oracle v2.2, teaching l3_enriched_v3.0 (Path B + recentering
  shipped), game prototype at f5c1a5a

Iteration:
- v2.3.1 baseline anchored at e663c6f (self-play failed; not prod)

In progress:
- Logic v2.4 Stage 3.5 — NOT shipped. 5 MUSTs from multi-agent
  review (commit 0276653). Builder's handoff at
  review/comms/BUILDER_V24_STAGE35_HANDOFF_2026-04-21.md
- Teaching plan v2.1 — shipped at 42d7f76; standing by for
  playtest + cross-stream pings
- Game first cut — shipped at 4fe1d41; second cut deferred

Archived:
- v2.3 (reverted — air-BET overgeneralization)
- v2.3.2 (shelved — target-subspace + concentration effect)

v2.4 ship sequence (current bottleneck at Stage 3.5):
1. Stage 3.5 MUSTs (5 of them; see reconciliation doc)
2. Stage 4: re-label training with v3.2 prompt
3. Stage 5: retrain v2.4
4. Stage 6: ship gate (pre-flight + standard + air/value litmus + self-play)

v2.5 queued (after v2.4):
- Bet-sizing-conditional narrowing (research/GTO/practical all flagged
  as biggest industry gap)
- Raise-aware call narrowing
- hand_evaluator draw_outs fix
- HU counter-examples + v3.2 HU calibration
- Retire flush_block_pct
- Blocker 2-flag teaching design (L4/L5)

Most recent directive commits:
- MAIN_TERMINAL_DIRECTIVE_2026-04-18-i (Path B + false-draw guard)
- MAIN_TERMINAL_DIRECTIVE_2026-04-18-v (recentering locked)
- MAIN_TERMINAL_DIRECTIVE_2026-04-19-z (v2.4 split approved)
- MAIN_TERMINAL_TO_BUILDER_2026-04-19-aa (Stage 1 approved, Stage 2 go)
- MAIN_TERMINAL_TO_BUILDER_2026-04-20-bb (Stage 3.5 scope accepted)
- MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20 (5 MUSTs exposed)

Orchestration discipline:
- DECIDE and EXECUTE. Don't ask owner unless ABSOLUTELY NECESSARY.
- Default recommendation is the quality-focused slow-moving approach.
- Multi-agent review (4-6 agents) is the default for load-bearing
  changes — spawn parallel agents without asking. See
  feedback_multi_agent_review_for_load_bearing.md for agent panel.
- Manifest is source of truth for approved integration state; bump
  per approval gate with a commit referencing the directive.
- Brief is good in chat responses. Owner doesn't read long reports.
- Match DIRECTIVE / DECISION / APPROVED naming (not REQUEST / PROPOSAL).
- Reconciliation step after every multi-agent review: aggregate
  findings by severity (CRITICAL/HIGH/MEDIUM/LOW), identify
  conflicts, produce single DIRECTIVE with MUSTs before ship.

Pending orchestrator work (awaiting builder/teaching/game pings):
- Logic builder: patch Stage 3.5 MUSTs + re-run M4/M5 audits on
  blocker features + land 81-case unit test corpus
- Teaching: standing by for playtest findings
- Game: standing by for second-cut direction
- v2.4 ship gate (after builder completes Stage 3.5 + Stages 4-6)

Approval gates I own:
- Stage 3.5 ship gate (pending 5 MUSTs patched)
- Stage 4 open (gated on Stage 3.5)
- Stage 5 retrain approval (gated on Stage 4)
- Stage 6 ship gate (gated on Stage 5)
- Any teaching CONTENT_API version bump
- Any game UI cut (second cut currently deferred pending owner)
- Any cross-stream schema change

Playtest-logging system (~/river-rats-game/playtest-logs/) captures
has_logic_feedback + has_teacher_feedback per hand. When owner
surfaces findings, triage to builder or teaching based on the
feedback text + affected stage.

Standing by for:
- Owner direction
- Builder ping on MUST patches
- Teaching ping on playtest findings or CONTENT_API changes
- Game ping on adapter issues or next cut direction

If owner signals go on v2.5 bet-sizing-conditional narrowing (major
solver-data commissioning), that's an owner-only resource decision;
wait for explicit authorization before starting.
```
