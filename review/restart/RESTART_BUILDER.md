# Restart Prompt — Builder Terminal (GitHub-first)

Copy the block below into a fresh Claude Code session as your
first message.

---

```
I'm restarting the River Rats v2 builder terminal on a new
machine. You can only access GitHub (no local filesystem from
prior session).

STEP 1: Clone the repo if it doesn't exist locally.

Check if /home/rupert/river-rats-v2 (or a similar path you can
write to) exists as a valid clone of
https://github.com/beytell1-sketch/river-rats-v2.git
with a `.git` directory. If not, clone it:

  git clone https://github.com/beytell1-sketch/river-rats-v2.git \
    ~/river-rats-v2

Then cd into the clone and confirm `git status` shows a clean
tree on master. This is your working directory for the rest of
the session.

If any existing local path has partial content (e.g.
river-rats-complete without review/ or without recent commits),
do NOT try to merge. Clone fresh to a new path and work from
there.

STEP 2: Read these files in order, from your cloned repo:

1. CLAUDE.md — project conventions (MUST follow Plan-Build-
   Review, test-first, blueprint-before-build, stop conditions,
   sacred river-rats-core/)
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
- review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md (Track B blueprint)

STEP 3: Confirm current state.

- v2.2 model trained, saved at river-rats-core/models/v2_2_model.json
- Gate 7 PENDING on owner solver verification of 10 MW misses
- Previous builder session stopped responding mid-directive
- Tier 1 tracks should launch; Tier 2 waits on Tier 1

Tier 1 tracks to launch (in parallel, no dependencies):
- Track 1: Harness hardening (Programmer, test-first)
- Track 3: Training data completeness audit (Programmer + ML Architect)
- Track 4: MW miss bias deep-dive (GTO Expert + Programmer)
- Track 5: BP generator fix implementation (Programmer, test-first
  per BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md blueprint)

Tier 2 (after Tier 1):
- Track 2: FB-40 re-eval with hardened harness (after Track 1)
- Track 6: Track A scope corrections (after Track 4)

STEP 4: Commit protocol.

- Commit autonomously with descriptive messages
- After each track artifact is ready, commit AND push to
  origin/master so the owner can review via GitHub URLs
- Do NOT create branches — commit direct to master as prior
  sessions did
- If `git push` needs credentials, report BLOCKED and request
  credentials from owner

Constraints you MUST follow:
- Plan → Review → Build → Review (never skip)
- Test-first before implementation
- Blueprint before build — architect reads source, writes
  exact insertion points
- Stop conditions: if source differs from blueprint, STOP and
  report BLOCKED, do not improvise
- Do NOT re-run BP labelling
- Do NOT ship v2.2 — Gate 7 is owner's decision
- Do NOT generate v2.3 hands yet — waiting on Track B fix and
  Track A amendments

Report status:
- Confirm clone path and that you can read the required files
- Confirm `git push` works (or report BLOCKED if credentials
  missing)
- Summarize current state in 3-4 sentences
- Then await owner direction before launching tracks
```

---

## Notes

- The builder's previous machine had the repo at
  `/home/rupertbeytell/river-rats-v2/` — paths in comms files
  reference that. The new builder machine just needs to know
  that all paths in the docs are relative to the repo root, so
  they work in any clone.
- `git push` requires auth on the new machine. If it fails, the
  builder reports BLOCKED and the owner sets up a PAT or SSH key
  before continuing.
- The clone path can be anything writable on the builder's
  machine — `/home/rupert/river-rats-v2` is suggested but not
  required.

## Links

- [Repo root](https://github.com/beytell1-sketch/river-rats-v2)
- [SESSION_STATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md)
- [DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md)
- [HRP_INVESTIGATION_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/HRP_INVESTIGATION_2026-04-15.md)
- [BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md)
- [REVIEW_PARALLEL_TRACKS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/REVIEW_PARALLEL_TRACKS_2026-04-15.md)
