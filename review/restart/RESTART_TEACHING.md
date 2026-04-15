# Restart Prompt — Teaching Terminal (GitHub-first)

Copy the block below into a fresh Claude Code session as your
first message.

---

```
I'm restarting the River Rats teaching terminal on a new
machine. You can only access GitHub (no local filesystem
from prior session).

STEP 1: Teaching repo does NOT have a GitHub remote yet.

The teaching project at the owner's prior machine lives at
/home/rupertbeytell/river-rats-teaching/ but has no GitHub
remote. The owner needs to push it to GitHub first before you
can clone it.

Until that happens, you CANNOT restart the full teaching
terminal. You can still do design/review work by reading the
logic team's handoff document on GitHub (see Step 3 below).

If the owner has set up a remote and you have the URL, clone
it:

  git clone <teaching-repo-url> ~/river-rats-teaching

Otherwise, report BLOCKED waiting on teaching repo to be
pushed to GitHub.

STEP 2: Clone the logic repo (read-only reference).

You need the logic team's enriched label export as your
input data. Clone their repo:

  git clone https://github.com/beytell1-sketch/river-rats-v2.git \
    ~/river-rats-v2

You will READ ONLY from this repo. Do not modify anything in
it. The logic team owns it.

STEP 3: Read these files.

From the logic repo (read-only):
1. review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md —
   schema and 22 label changes to be aware of
2. training-data/v2_2_enriched_for_teaching.jsonl — your input
   data (385 hands with intentions, street_plan_tags,
   feature_attention, difficulty, etc.)
3. review/comms/SESSION_STATE_2026-04-15.md — overall project
   state for context

From the teaching repo (if available):
4. CLAUDE.md
5. review/comms/PLAN_TEACHING_V2_ALIGNED_2026-04-13.md —
   teaching plan
6. review/comms/REVIEW_TEACHING_QUALITY_ENGINE_2026-04-13.md —
   5 owner amendments

STEP 4: Current state.

- v2.2 logic training complete, Gate 7 pending (but schema
  won't change for teaching)
- Phase 1 teaching templates + layout were approved
- Phase 2 quality validation unblocked — you have real v2.2
  enriched data now
- Logic team is running 6 parallel tracks while waiting on
  owner solver time

Your scope:
- Build L3 renderer v2 consuming the enriched fields: intentions,
  primary_intention, street_plan_tags, feature_attention,
  hero_range_percentile, villain_medium_made_pct, difficulty
- Run quality validation per PLAN_TEACHING_V2_ALIGNED (Phase 2)
- Templates fire on intention tags, NOT on feature thresholds
  (owner directive) — labelling agent already decided the
  intention, teaching just presents
- Do NOT duplicate poker logic. Consume from logic team.
- Do NOT modify logic team's code. It's a separate repo.

Important awareness:
- The handoff note mentions CHECK-over-BET bias may persist in
  some borderline training hands. Don't flag every
  CHECK-on-marginal-spot as a renderer bug — it might be a
  label inheritance, not a renderer issue.
- 22 label changes were applied in Phase 3.5H. If you'd tested
  the renderer against older data, invalidate those tests.

Constraints:
- Test in isolation with real enriched data
- Structured JSON scoring output, not prose reports
- Every teaching value must trace to a named field
- No bespoke coaching prose — templates + numbers

STEP 5: Report status.

- Confirm whether the teaching repo has a GitHub remote yet
  (if not, report BLOCKED)
- Confirm you can clone and read the logic repo
- Summarize the teaching state in 3-4 sentences
- Then wait for owner direction
```

---

## Notes

- The teaching repo is local-only as of 2026-04-15
- To unblock a GitHub-first restart, the owner needs to run
  from the teaching directory:
  ```
  gh repo create river-rats-teaching --private --source=. \
    --remote=origin --push
  ```
- Then add the resulting URL to this file

## Links

**Logic repo (read-only reference):**

- [Repo root](https://github.com/beytell1-sketch/river-rats-v2)
- [TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md)
- [training-data/v2_2_enriched_for_teaching.jsonl](https://github.com/beytell1-sketch/river-rats-v2/blob/master/training-data/v2_2_enriched_for_teaching.jsonl)
- [SESSION_STATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md)

**Teaching repo:** no GitHub remote yet.
