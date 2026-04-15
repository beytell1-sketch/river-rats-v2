# Restart Prompt — Teaching Terminal

Copy the block below into a fresh Claude Code session as your
first message.

---

```
I'm restarting the River Rats teaching project. You are the
TEACHING terminal — you design and build the L3 teaching
renderer and its quality validation.

The teaching project lives at /home/rupertbeytell/river-rats-teaching/.
The LOGIC project is a separate repo at /home/rupertbeytell/river-rats-v2/
— you consume its outputs but do not modify its code.

Please start by reading these files:

From /home/rupertbeytell/river-rats-teaching/:
1. CLAUDE.md — teaching project conventions
2. review/comms/PLAN_TEACHING_V2_ALIGNED_2026-04-13.md —
   teaching plan, replaces all prior teaching plans
3. review/comms/REVIEW_TEACHING_QUALITY_ENGINE_2026-04-13.md —
   5 amendments owner requested
4. data/v2_2_enriched.jsonl — v2.2 enriched labels from the
   logic team (your input data)

From /home/rupertbeytell/river-rats-v2/ (read-only reference):
5. review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md —
   schema and 22 label changes to be aware of
6. review/comms/SESSION_STATE_2026-04-15.md — overall project state

Current state:
- v2.2 logic training complete, Gate 7 pending (but schema
  won't change for teaching)
- Phase 1 teaching templates + layout were approved
- Phase 2 quality validation unblocked — you have real v2.2
  enriched data now
- logic team is running 6 parallel tracks while waiting on
  owner solver time

Your scope:
- Build L3 renderer v2 consuming the enriched fields: intentions,
  primary_intention, street_plan_tags, feature_attention,
  hero_range_percentile, villain_medium_made_pct, difficulty
- Run quality validation per PLAN_TEACHING_V2_ALIGNED (Phase 2)
- Templates fire on intention tags, NOT on feature thresholds
  (owner directive) — labelling agent already decided the
  intention, teaching just presents
- Do NOT duplicate poker logic. Consume from v2.
- Do NOT modify v2 code. It's a separate repo.

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

Confirm you've read the files and summarize the teaching state
in 3-4 sentences. Then wait for owner direction.
```

---

## Notes

- The teaching repo has no GitHub remote yet. If you want it
  synced to GitHub, create a repo and add a remote first.
- The enriched label export is the main input
- Keep the L3 renderer and scoring pipeline independent of the
  logic team's Gate 7 decision — schema won't change

## Links

**Logic repo (read-only reference for teaching):**

- [TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md)
- [training-data/v2_2_enriched_for_teaching.jsonl](https://github.com/beytell1-sketch/river-rats-v2/blob/master/training-data/v2_2_enriched_for_teaching.jsonl)
- [SESSION_STATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md)

**Teaching repo:** no GitHub remote yet. Local only.
