---
date: 2026-04-16
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.3 build plan — all 8 items APPROVED; execute Phase 0 now
status: DIRECTIVE
approves: review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md §12
---

# Main Terminal Update — 2026-04-16 (b)

Build plan approved. All 8 items in §12 are green. Execute
per the plan. Phase 0 starts now.

## Approvals

| # | Item | Decision |
|---|---|---|
| 1 | Interpretation U (Umbrella, ~420 total) | APPROVE |
| 2 | 11-bucket per-file JSONL output plan | APPROVE |
| 3 | 25% overshoot target | APPROVE |
| 4 | `generate_factory_batch6.py` parameterised generator | APPROVE |
| 5 | 7-phase pipeline with commit cadence | APPROVE |
| 6 | Stop-condition register | APPROVE |
| 7 | Create `prompts/gto_labeller_v3.md` | APPROVE with explicit override-clause requirement (see §1) |
| 8 | Update `calibration_exam.py` to 23/28 + 4 new anchors + Group-D ingestion | APPROVE |

## 1. Explicit requirement on the v3 prompt (item 7)

The v3 prompt MUST include the Stream B.2 override clause in
the BET-decision guidance section. Verbatim text:

> When villain_checked_back=1, villain_range_capped=1,
> num_opponents≥2, and hero's worse_hand_pct exceeds 0.55,
> prefer BET for value+protection even when OOP or holding a
> medium-strength made hand. The passive line forfeits the
> capped villain's air portion.

Without this clause, the v3 labelling panels will not have
the fix we designed, and the bias correction in the training
supplement will be undermined by continued label variance on
boundary spots. Non-negotiable.

Include a cross-reference comment in the prompt pointing at
`review/comms/MW_MISS_BIAS_ANALYSIS_2026-04-15.md` as the
source of the clause.

## 2. Curated-draw sourcing (rows 6-7) — light owner touchpoint

Per §1.4 of the plan, curated hands require manual nut-draw +
blocker confirmation. The filter surfaces candidates; a human
confirms. This is a small owner touchpoint (~30 candidates to
spot-check).

Sequence it so it does not block the factory-generated buckets:

- Run the pool filter now and land the candidate list in
  `review/comms/V23_CURATED_CANDIDATES_2026-04-16.md`
- Owner reviews the candidate list asynchronously — not
  blocking Phase 1 for other buckets
- Confirmed candidates land in `v23_curated_draw_{flop,turn}.jsonl`
  before Phase 2 assembly QA

## 3. Phase 0 gate — run now

Execute §2 pre-flight checks:
- §2.1 test gates (pytest)
- §2.2 schema sanity on existing JSONLs
- §2.3 disk check
- §2.4 prompt preparation — includes v3 prompt creation (with
  override clause)
- §2.5 git hygiene

Report gate pass/fail to
`review/comms/PHASE0_PREFLIGHT_2026-04-16.md`. If any check
fails, STOP and report — do not proceed to Phase 1.

## 4. Ordering through Phase 3

After Phase 0 clear:

**Phase 1 (generation) can run in parallel with v3 prompt
creation and calibration_exam.py update.**

- Phase 1 buckets are factory-generated; they don't depend
  on the v3 prompt.
- v3 prompt creation is a documentation task — gate for
  Phase 3, not Phase 1.
- calibration_exam.py update is a Phase 3 prerequisite.

Proceed per the plan's §7 checkpoint/commit cadence. One
commit per bucket JSONL + one per infrastructure change.

## 5. Phase 3 calibration gate — explicit blocker

Calibration must score ≥ 23/28 AND 100% on reversal hands
BEFORE any production labelling (Phase 4) begins. If first
attempt fails:

- Panel redesign per §3.3 (prompt re-edit, KB cross-reference
  pass, re-calibration)
- Re-run gate
- Do NOT proceed to Phase 4 on a failed gate

This is the hardest stop condition in the project. Honoring
it is the difference between v2.3 fixing the bias and v2.3
replicating v2.2's label noise.

## 6. Solver validation on 8 MW misses — Phase 7.3

Per the earlier directive, this runs during v2.3 validation
(Phase 7), not before. Owner allocates solver sessions when
available. Schedule:

- Phase 7.1 and 7.2 (automated evaluation) can complete
  independently
- Phase 7.3 is the last gate before ship-as-v2.3-production
- Solver confirms the bias correction landed on the exact
  8 hands that v2.2 missed

## 7. Ship gate for v2.3

v2.3 replaces v2.2 as production when ALL of:
- Phase 7.1 eval passes the scope §5 thresholds
- Phase 7.2 Group-A+B ≥ 70% absolute
- Phase 7.3 solver validates ≥ 6/8 MW misses corrected
- Group D regression ≤ 1 hand
- All calibration reversal hands still correct on v2.3

If any of the above fails, v2.3 does not ship — investigate
and iterate per scope §6.

## 8. Commit discipline (reminder)

Per CLAUDE.md §6 addendum: every model-producing script
committed. No inline heredoc training. Every bucket JSONL
commits individually. Push after each commit.

## 9. Owner items from here

Narrowed further. While v2.3 runs:
- Curated-draw candidate spot-check (§2 above) — async, ~30 hands
- Solver sessions for Section 4 auto-enqueue reserve + Section 1
  row 11 solver-sourced cohort (~10-20 hands) — scheduled at
  owner pace, does not block Phase 1/2
- Phase 7.3 solver validation (8 hands) — at ship gate
- v2.3 ship sign-off once all gates pass

All other work runs without owner.

---

**Builder: Phase 0 starts now. Report first results to
`review/comms/PHASE0_PREFLIGHT_2026-04-16.md`.**
