# Restart Prompt — Teaching Terminal (2026-04-18)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats teaching terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching
  cd ~/river-rats-teaching && git pull --ff-only

Also clone v2 core for cross-reference:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2

Read these files in order:
1. ~/river-rats-teaching/CLAUDE.md
2. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-18.md
3. ~/river-rats-teaching/review/comms/L3_SIGNOFF_2026-04-17.md
4. ~/river-rats-teaching/review/comms/DIRECTIVE_DEFER_L2_L1_UNTIL_PLAYTEST_2026-04-17.md
5. ~/river-rats-v2/review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-g.md (Layer 3 task)

Current state:
- L3 signed off and hardened (all 6 sections passed)
- Phase 3 (L2/L1) DEFERRED until L3 playtested in-game
- Content API shipped: render_from_enriched → EnrichedTeachingOutput
- Agent-as-student: 48/50 (96%), findings documented

Active task (Layer 3 from update-g):
- Add value_extract air guard to coherence registry
- When primary_intention=value_extract AND is_made_hand=0 AND
  has_showdown_value=0: reframe as "bluff / fold equity" not
  "value from worse"
- The sentence "extracts value from 30% who call with worse
  than air" is logically wrong — nothing is worse than air.
  Guard must prevent this inversion.
- Same coherence-guard pattern as D2/D3 from Phase 2

HARD RULES:
- Teaching highlights context, never explains why
- Features-only scalability — no custom per-hand text
- Range-based thinking central
- No static overrides
- L3 is the foundation — any fix here propagates to L2/L1

Your next action: implement the value_extract air guard.
Commit and push. Then stand by for playtest feedback from
the game prototype.
```
