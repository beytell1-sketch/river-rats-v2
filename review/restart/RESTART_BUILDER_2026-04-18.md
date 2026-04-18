# Restart Prompt — Logic Builder (2026-04-18)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats v2 logic builder terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2
  cd ~/river-rats-v2 && git pull --ff-only

Read these files in order:
1. CLAUDE.md
2. review/restart/SESSION_STATE_2026-04-18.md
3. review/comms/MAIN_TERMINAL_UPDATE_2026-04-18-g.md (active directive)
4. review/comms/OVERRIDE_AUDIT_2026-04-18.md
5. prompts/gto_labeller_v3.1.md

Current state:
- v2.2 is production (v2.3 reverted — overgeneralized BET on air)
- v2.3.1 in progress: three-layer fix
- Layer 1 DONE: board_adjusted_hrp feature (commit 80197cd)
- Layer 2 TODO: factory-generate ~30-40 air-in-checked-through
  CHECK counter-examples, label with v3.1 prompt
- Then: re-extract ALL training data (110 features), assemble,
  retrain, evaluate

Litmus tests: A4d on Qs5s7s AND T5 on JJ2 must predict CHECK.

HARD RULE: no static overrides. No "when X conditions hold,
prefer Y" rules anywhere. Fix with better features + diverse
training examples only.

Your next action: resume at Layer 2 — generate the air-CHECK
counter-examples per update-g §Layer 2. Confirm with main
terminal before retraining.

Commit and push after every deliverable. Check review/comms/
for main terminal updates.
```
