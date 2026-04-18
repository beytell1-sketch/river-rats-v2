---
date: 2026-04-18
from: Main terminal (outgoing orchestrator)
to: All restarting terminals
re: Current state snapshot for 4-terminal restart
---

# Session State — 2026-04-18

## v2 Core (Logic Builder)

### Shipped
- v2.2 model: production (reverted to for playtest)
- v2.3 model: shipped at 447254d but REVERTED — overgeneralizes
  BET on air hands due to override-contaminated training approach
- Feature extractor: 55 raw features (board_adjusted_hrp added
  at 80197cd)
- v3.1 labelling prompt: created at 4a2d28c (override stripped)
- Override audit: 349/486 hands fired, ALL CLEAN (0 SUSPECT)
- Harness hardening, dtype guards, pre-flight schema gate: all
  shipped

### In Progress — v2.3.1
Three-layer fix per MAIN_TERMINAL_UPDATE_2026-04-18-g.md:
1. board_adjusted_hrp feature (DONE — 80197cd)
2. ~30-40 air-in-checked-through CHECK counter-examples (TODO —
   factory-generate, label with v3.1 prompt)
3. Re-extract all training data with 110-feature vector, assemble,
   retrain, evaluate

Litmus tests: A4d on Qs5s7s AND T5 on JJ2 must predict CHECK.

### Pending
- Self-play diagnostic with v2.3 (logged in memory, run after
  v2.3.1 ships)
- Solver on 8 MW misses (owner-paced, post-ship)
- 28 solver-enqueued hands from Phase 4 (owner-paced)

### Key files
- review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-g.md — active
  directive for v2.3.1
- review/comms/OVERRIDE_AUDIT_2026-04-18.md — audit results
- prompts/gto_labeller_v3.1.md — clean prompt (no override)
- review/comms/PLAN_CONSOLIDATED_2026-04-15.md — original plan

## Teaching

### Shipped
- L3 renderer: signed off after hardening (coherence, teaching
  value, scale, adversarial, template audit, long-session)
- Content API: render_from_enriched → EnrichedTeachingOutput
  with .to_dict(), documented at interface/CONTENT_API.md
- Phase 2 Tier A: shipped
- Draw-type specificity, showdown-value indicator, HRP
  contradiction guard, board-relative range framing: all landed

### In Progress
- value_extract air guard (per MAIN_TERMINAL_UPDATE_2026-04-18-g
  Layer 3) — don't say "value extract" when hero has air
- Agent-as-student: 48/50 (96%), 2 misses diagnosed

### Deferred
- Phase 3 (L2/L1): deferred until L3 playtested in-game
- L3 playtest findings feed back into L3 adjustments first

### Key files
- review/comms/L3_SIGNOFF_2026-04-17.md
- review/comms/DIRECTIVE_DEFER_L2_L1_UNTIL_PLAYTEST_2026-04-17.md
- review/comms/DIRECTIVE_L3_TEACHING_VALUE_FIXES_2026-04-17.md

## Game Builder

### Shipped
- Engine: cards.py, game_state.py, dealer.py, session.py,
  mocks.py — all tested (81/81)
- Prototype: table_and_teaching_v1.html with card visuals,
  pre-hint/post-hint split, Oracle's Read panels
- Contract v2: three-source architecture (game_state,
  oracle_output, teaching_output)
- Session dump: generate_session_dump.py with --oracle/--teaching
  flags

### In Progress
- Real oracle + teaching integration adapters (F.4)
- All integration questions answered in
  MAIN_TERMINAL_TO_GAME_2026-04-18-b.md
- Currently on v2.2 model (reverted from v2.3)

### Key files
- review/comms/MAIN_TERMINAL_TO_GAME_2026-04-18-b.md — adapter
  guidance
- engine/ — full game engine
- review/prototype/ — HTML playtest

## Hard Rules (from memory)

1. No static overrides anywhere in the pipeline
2. Fix with better features + diverse training examples
3. L3 must be playtested in-game before L2/L1
4. Teaching highlights context, never explains why
5. Features-only scalability — no custom per-hand text
6. Range-based thinking central at all levels
7. Slow/quality — no rush, rushing causes trouble later
8. Recommend, don't defer decisions to owner

## Repos

- v2 core: github.com/beytell1-sketch/river-rats-v2
- Teaching: github.com/beytell1-sketch/river-rats-teaching
- Game: ~/river-rats-game (local, not on GitHub yet)
