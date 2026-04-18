# Restart Prompt — Game Builder (2026-04-18)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats game builder terminal.

Working directory: ~/river-rats-game
(not a git repo yet — local only)

Also clone/pull sibling repos for reference:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching

Read these files in order:
1. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-18.md
2. ~/river-rats-game/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-18-b.md (adapter guidance)
3. ~/river-rats-game/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-17-c.md (role clarification)
4. ~/river-rats-game/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-17-d.md (3-source architecture)
5. ~/river-rats-game/review/lessons.md

Current state:
- Engine shipped: cards.py, game_state.py, dealer.py,
  session.py, mocks.py (81/81 tests passing)
- Prototype: table_and_teaching_v1.html with card visuals
- Contract v2: three-source architecture
  (game_state, oracle_output, teaching_output)
- All integration questions answered in update-b

Active task (F.4):
- Build real oracle + teaching adapters
- Oracle: v2.2 model (v2.3 reverted, v2.3.1 in progress)
  Model path: ~/river-rats-v2/river-rats-core/models/v2_2_model.json
  NOTE: feature vector is changing (108 → 110 for v2.3.1).
  Build adapter against 108 for now; flag for update when
  v2.3.1 ships.
- Teaching: render_from_enriched is stable
  Docs: ~/river-rats-teaching/interface/CONTENT_API.md
- Heuristic sources for hand_bucket, difficulty, intentions,
  primary_intention documented in update-b §teaching answers

YOUR ROLE:
- You own GAME STATE and the LOOP
- Oracle and teaching are BLACK BOXES you call via adapters
- You do NOT read oracle/teaching internals
- Three data sources: game_state (you), oracle_output (you
  call oracle), teaching_output (you call teaching)
- render(game_state, oracle_output, teaching_output)

HARD RULES:
- No static overrides at any layer
- Game does NOT correct or override oracle output
- Game does NOT generate teaching text
- Scope: simulation + display + user input + session mgmt

Your next action: build the two adapter modules per update-b,
wire into generate_session_dump.py with --oracle=real
--teaching=real flags, generate playtest bundle on v2.2.

When v2.3.1 ships: swap model path (one line), update feature
count in adapter (108→110). Everything else unchanged.
```
