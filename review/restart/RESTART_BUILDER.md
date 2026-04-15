# Restart Prompt — Builder Terminal

Copy the block below into a fresh Claude Code session as your
first message.

---

```
I'm restarting the River Rats v2 project. You are the BUILDER
terminal — you coordinate architecture, programmer, ML architect,
GTO expert, and tester agents.

Please start by reading these files from the repo at
/home/rupertbeytell/river-rats-v2/ in order:

1. CLAUDE.md — project conventions (MUST follow Plan-Build-Review,
   test-first, blueprint-before-build, stop conditions, sacred
   river-rats-core/)
2. review/comms/SESSION_STATE_2026-04-15.md — where we are
3. review/comms/HRP_INVESTIGATION_2026-04-15.md — test harness
   bug finding (THIS CHANGES TRACK A SCOPE)
4. review/comms/DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md
   — your active directive
5. review/comms/REVIEW_PARALLEL_TRACKS_2026-04-15.md — amendments
   you owe

Also read:
- docs/PROCESS_GUIDE.md if it exists
- review/comms/PLAN_V2.2_FINAL_COMBINED_2026-04-13.md (overall)
- review/comms/PLAN_PHASE3_FINAL_2026-04-13.md (Phase 3)

Current state:
- v2.2 model trained, saved at river-rats-core/models/v2_2_model.json
- Gate 7 PENDING on owner solver verification of 10 MW misses
- You were executing 6 parallel tracks and stopped responding
- Restart should resume Tier 1 tracks

Tier 1 tracks to launch (in parallel, no dependencies):
- Track 1: Harness hardening (Programmer, test-first)
- Track 3: Training data completeness audit (Programmer + ML Architect)
- Track 4: MW miss bias deep-dive (GTO Expert + Programmer)
- Track 5: BP generator fix implementation (Programmer, test-first
  per BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md blueprint)

Tier 2 (after Tier 1):
- Track 2: FB-40 re-eval with hardened harness (after Track 1)
- Track 6: Track A scope corrections (after Track 4)

Constraints you MUST follow:
- Plan → Review → Build → Review (never skip)
- Test-first before implementation
- Blueprint before build — architect reads source, writes
  exact insertion points
- Stop conditions: if source differs from blueprint, STOP and
  report BLOCKED, do not improvise
- Commit autonomously with descriptive messages
- Do NOT re-run BP labelling
- Do NOT ship v2.2 — Gate 7 is owner's decision
- Do NOT generate v2.3 hands yet — waiting on Track B fix and
  Track A amendments

Report status and confirm you've read the files. Launch Tier 1
tracks if owner approves the restart, or await direction.
```

---

## Notes

- The builder terminal's job is orchestration across specialist
  subagents (architect, programmer, gto-expert, ml-architect,
  tester, reviewer)
- It should commit autonomously in the local repo — identity is
  already configured
- Repo: https://github.com/beytell1-sketch/river-rats-v2.git

## Links

- [SESSION_STATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md)
- [DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md)
- [HRP_INVESTIGATION_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/HRP_INVESTIGATION_2026-04-15.md)
- [BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md)
- [REVIEW_PARALLEL_TRACKS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/REVIEW_PARALLEL_TRACKS_2026-04-15.md)
