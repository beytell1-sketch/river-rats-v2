# Restart Prompt — Teaching Terminal (GitHub-first)

**Teaching repo IS on GitHub:**
https://github.com/beytell1-sketch/river-rats-teaching

Copy the block below into a fresh Claude Code session as your
first message.

---

```
I'm restarting the River Rats teaching terminal on a new
machine.

STEP 1: Clone both repos.

git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching
git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2
cd ~/river-rats-teaching

STEP 2: Read in order:
1. review/restart/TEACHING_HANDOFF_2026-04-15.md — latest handoff
   (START HERE)
2. review/comms/PLAN_TEACHING_V2_ALIGNED_2026-04-13.md —
   teaching plan v2
3. review/comms/REVIEW_TEACHING_QUALITY_ENGINE_2026-04-13.md —
   owner's 5 amendments
4. CLAUDE.md — project conventions
5. ../river-rats-v2/review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md
   — logic team's handoff note (read-only reference)

STEP 3: Inspect the enriched data:

wc -l data/v2_2_enriched.jsonl
head -1 data/v2_2_enriched.jsonl | python3 -m json.tool | head -30

Should show 385 rows with fields: situation_id, consensus_action,
hand_bucket, intentions, primary_intention, street_plan_tags,
feature_attention, difficulty, reasoning_by_team,
full_feature_vector.

STEP 4: Verify git push works. Test with a trivial commit if
needed (e.g., touch review/comms/RESTART_CHECK_<date>.md, add,
commit, push). If it fails, report BLOCKED before any work.

STEP 5: Summarize teaching state in 3-4 sentences. Wait for
owner direction, or proceed with Phase 2 baseline generation
if already green-lit.

Current state:
- Phase 1 (templates + layout): SHIPPED
- Phase 2 (quality validation): READY TO START
- v2.2 enriched labels: just committed by owner (commit a898006)
- Logic team Gate 7 pending but does NOT block teaching
- Logic-side ANOMALY-A investigation in flight (don't worry —
  label schema unchanged)

Constraints you MUST follow:
- Templates fire on intention tags, NOT feature thresholds
  (owner directive)
- Don't duplicate logic — consume from the logic team's exports
- Don't modify the logic repo (~/river-rats-v2/) — it's
  read-only reference
- CHECK-over-BET bias may persist in borderline training hands
  — don't flag every CHECK-on-marginal-spot as a renderer bug
- Commit and push after every deliverable, don't batch
- Communicate with owner via commits to this repo — no direct
  messaging

If blocked on auth for git push, drop a file at
review/comms/TEACHING_BLOCKED_<date>.md explaining what failed.
```

---

## Notes

- **Teaching repo IS on GitHub** as of 2026-04-15 (previously
  was local-only)
- **Enriched data is committed** at `data/v2_2_enriched.jsonl`
  (commit a898006) — 385 hands, ready for Phase 2
- **Phase 1 is complete** — intention templates, L3 renderer
  v2, gold standards all shipped
- **Phase 2 is next** — 20-30 hand baseline generation + 3
  scorer agents (Utility / Coherence / Pattern)

## Links

### Teaching repo
- [Repo root](https://github.com/beytell1-sketch/river-rats-teaching)
- [Teaching handoff (latest)](https://github.com/beytell1-sketch/river-rats-teaching/blob/master/review/restart/TEACHING_HANDOFF_2026-04-15.md)
- [Teaching plan v2](https://github.com/beytell1-sketch/river-rats-teaching/blob/master/review/comms/PLAN_TEACHING_V2_ALIGNED_2026-04-13.md)
- [Owner review + amendments](https://github.com/beytell1-sketch/river-rats-teaching/blob/master/review/comms/REVIEW_TEACHING_QUALITY_ENGINE_2026-04-13.md)
- [Enriched data](https://github.com/beytell1-sketch/river-rats-teaching/blob/master/data/v2_2_enriched.jsonl)
- [L3 renderer v2](https://github.com/beytell1-sketch/river-rats-teaching/blob/master/interface/l3_renderer_v2.py)
- [Intention templates](https://github.com/beytell1-sketch/river-rats-teaching/blob/master/content/intention_templates.py)

### Logic repo (read-only reference)
- [Logic repo root](https://github.com/beytell1-sketch/river-rats-v2)
- [Logic handoff note](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md)
- [Current logic state](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md)
- [Tag vocabulary](https://github.com/beytell1-sketch/river-rats-v2/blob/master/training-data/tag_vocabulary.json)
