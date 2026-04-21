# Restart Prompt — Game Builder (2026-04-21)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats game builder terminal.

Working directory: ~/river-rats-game (local; NOT on GitHub yet — do
not attempt to clone)

Also pull orchestrator repo for cross-stream state:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2

Also ensure teaching repo is available (adapter imports from it):
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching

Repo HEAD at handoff: 4fe1d41
Role: game prototype, real_oracle/real_teaching adapters, playtest
logging, UI

Read these files in order before doing anything else:
1. ~/river-rats-game/README.md (if exists; game-specific)
2. ~/river-rats-v2/CLAUDE.md (project-level)
3. ~/river-rats-v2/RELEASE_MANIFEST.yaml (integrated approved state)
4. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md (shared snapshot)
5. ~/river-rats-game/review/comms/GAME_TO_MAIN_TERMINAL_2026-04-21.md (your current state)
6. ~/river-rats-v2/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-18-m.md (playtest log 6 essentials)
7. ~/river-rats-v2/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-19-w.md (UI first cut directive)
8. ~/river-rats-game/playtest-logs/README.md (playtest workflow)

Current status: shipped and stable.

What's live in the prototype:
- Three-zone frame (table / coaching / hero controls)
- V1 range bar (horizontal stacked, 60×6px under each villain chip,
  min-segment-width clamped for visibility)
- Badge A action-order inline prefix ("① CHECK ② CALL ③ RAISE")
- Hand vs range panel split (commit 143993a)
- real_oracle adapter with SHAP (gated on for_position == hero to
  control cost)
- real_teaching adapter — Path-B-resilient (handles CONTENT_API v3.0
  output shape: range_position_desc, villain_*_pct, flags list,
  tightness signal)
- Playtest log schema v2 with full reproducibility payload:
  oracle_model_sha256, oracle_repo_commit, teaching_repo_commit,
  teaching_schema_version, game_build_commit, full_feature_vector_
  per_decision, shap_attributions_per_decision, ground_truth_vs_
  player_visible_split, is_real_backend banner
- Hand-log system with Log button, teacher/logic feedback boxes,
  Save + Export, localStorage persistence across reloads
- Mock-backend warning banner (red band when either oracle_backend
  or teaching_backend is "mock")
- 91/91 tests pass
- Real bundle generates clean (15 hands / 36 decisions in recent
  run)
- Prototype renders cleanly in both HU and 3-way

Running against:
- Oracle: v2.2 (~/river-rats-v2/river-rats-core/models/v2_2_model_shipped.json)
- Teaching: l3_enriched_v3.0 schema (plan v2.1 shipped at 42d7f76)

Deferred (not started — owner-paced):
- Second cut: pot-odds chip on felt (mockup not yet written)
- Third cut: per-seat stack visualization, street timeline at bottom of felt
- Per-villain range bars in multiway (teaching-side scope; await
  teaching CONTENT_API update if it happens)

Standing by for:
- Owner playtest session + hand-log findings to triage
- Orchestrator direction on next UI cut (second = pot-odds chip)
- v2.4 model ship signal (adapter swap from v2.2 to v2.4 once
  v2.4 passes ship gate; logic team currently blocked on Stage 3.5
  MUSTs)
- Any teaching CONTENT_API version bump requiring adapter update
  (teaching is stable currently)

Game contract rules (apply always):
- Game OWNS the felt: seat positions, chip visuals, action tags,
  range bars, action-order badges, pot display, board, hero controls
- Game DOES NOT own panel prose — that's teaching's domain. Game
  renders teaching output; game doesn't invent teaching content
- All villain_*_pct data reads come from teaching_output. Do NOT
  recompute at UI layer (single source of truth discipline)
- Playtest logs go to ~/river-rats-game/playtest-logs/ (gitignored);
  schema bump = version up the log_schema_version field
- Any UI change that affects "what the student sees" coordinates
  with teaching philosophy (no WHY in visuals any more than in prose)
- Multi-agent review for load-bearing changes — don't ask, escalate
- Slow/quality, no rush

Orchestrator (main terminal) is the cross-stream coordinator. Your
work is stable; no cross-stream blockers.

Ping orchestrator when:
- Owner flags a playtest finding (show summary + affected log file)
- You need direction on second cut
- Any adapter issue when v2.4 ships
- Any teaching schema mismatch surfaces

Standing by.
```
