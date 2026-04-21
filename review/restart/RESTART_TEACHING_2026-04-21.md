# Restart Prompt — Teaching Terminal (2026-04-21)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats teaching terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching

Also pull orchestrator repo for cross-stream state:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2

Working directory: ~/river-rats-teaching
Repo HEAD at handoff: 42d7f76
Role: teaching layer — L3 rendering, flag window, CONTENT_API, observation-only discipline

Read these files in order before doing anything else:
1. ~/river-rats-teaching/CLAUDE.md (teaching-specific rules)
2. ~/river-rats-v2/CLAUDE.md (project-level)
3. ~/river-rats-v2/RELEASE_MANIFEST.yaml (integrated approved state)
4. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md (shared snapshot)
5. ~/river-rats-teaching/review/comms/TEACHING_STATUS_UPDATE_2026-04-21.md (your current state)
6. ~/river-rats-v2/review/comms/MAIN_TERMINAL_DIRECTIVE_2026-04-18-v.md (locked recentering)
7. ~/.claude/projects/-home-rupert-river-rats-v2/memory/MEMORY.md (memory index — teaching uses same memory)

Current status: plan v2.1 SHIPPED across 11 commits. Path B complete + recentering complete.

Architecture shipped:
- Primary window: range-first (range composition, villain_*_pct
  fields, board_favour)
- Flag window: 7 active flags + blocker placeholder (deferred)
- L3 prose cuts: hand_bucket, hero_position, draw_type_desc,
  showdown_value_desc, position_desc, forward_plan_desc
  (removed; will restore for L1/L2 when those build)
- New FlagEntry dataclass with kind/trigger_value/observation_text
- CONTENT_API v3.0 published
- Guard-leak scanner expanded with directional-framing words
  (block/protect/charge/extract/deny + force/punish/drive/
  dominate) and WHY smugglers (make correct, safe to, justify,
  defensible)

End-state hardening metrics:
- 0 V3 leaks across 3,080 sentences × 8 fields
- 31 output fields
- 2.16 mean flags/hand
- Commitment flag 100%-firing waivered as dataset artifact
  (revisit post-playtest)

Deferred / standing by on:

1. Blocker flag 2-flag design (L4/L5)
   Gated on: v2.4 oracle features shipping (nut_flush_block,
   flush_draw_block_pct, straight_draw_block_pct,
   nut_made_block_pct). Scope spec is in
   ~/river-rats-v2/RELEASE_MANIFEST.yaml under
   queued.teaching_blocker_flag_design with owner's 2-flag
   phrasing inline. Requires GTO + V3 reviewer pass.

2. L1/L2 build
   Gated on: L3 playtest findings. Owner-paced. See
   feedback_playtest_before_lower_levels.md.

3. river-outs-parenthetical backlog + plan-tag dedupe
   Cosmetic; not in this cycle.

4. Any playtest findings flagged to teaching via hand-log system
   (owner clicks "Log Hand" in game, writes feedback to teacher)

Teaching contract rules (apply always):
- Observation-only at L3. No WHY prose. No directional framing
  words (block/protect/charge/extract/deny).
- Range-based thinking is central.
- Feature data pipes THROUGH teaching; teaching doesn't fabricate.
- Coherence guards OK (suppression); override guards NOT OK
  (fabrication).
- Expand the guard-leak scanner when new violation categories
  surface, don't patch individual templates.
- Plan → expert review (GTO + V3 reviewer subagents) → small
  commits → hardening re-pass. Default discipline.
- Multi-agent review for load-bearing changes — don't ask.

Cross-stream awareness:
- Logic v2.4 Stage 3.5 in progress (5 MUSTs). Feature values
  you consume will shift when v2.4 ships; most teaching output
  inherits automatically via classify_villain_range, but SHAP
  attribution values will also shift. Hardening re-pass
  recommended post-v2.4 ship.
- Game prototype running on Path B output cleanly. If you change
  CONTENT_API, coordinate with game terminal.

Orchestrator (main terminal) is the cross-stream coordinator.
Your work is stable; no active blockers.

Ping orchestrator when:
- Owner signals blocker flag design should start (v2.4 shipped)
- Playtest findings arrive via hand-log with has_teacher_feedback=True
- You surface a new hardening gap or violation category
- CONTENT_API version bump needed

Standing by.
```
