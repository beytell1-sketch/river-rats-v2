---
date: 2026-04-27
from: ml-architect
to: LEAD-PROGRAMMER · orchestrator · QC stream
re: Mini-review of PR #98 — mass-labelling scripts (dispatch + collect + 24 tests)
verdict: APPROVE-WITH-NITS
head: 3ed2291
branch: programmer/mass-labelling-scripts-2026-04-27
scope: scripts/dispatch_mass_labelling.py + scripts/collect_mass_labels.py + 24 tests
---

# Mini-review: PR #98 mass-labelling scripts

## Verdict: APPROVE-WITH-NITS

Scripts are correct on all three checklist items. Two nits documented below,
neither is a blocker. QC can proceed with pre-merge audit in parallel.

---

## 1. ref_id transformation correctness — PASS

`compute_ref_id` implements a three-tier priority chain:

1. `source_situation_id` if present and non-null → used by pilot 100 records
2. `f"d{deal_id}_{hero_position}_{street}"` if `deal_id` present → Mode-A 100
3. `pilot_hand_id` fallback → Mode-B factory 294

Mental spot-check against the Phase B Protocol A artefact (`4bce49f`):
- Pilot record `d6066_BB_flop` has `source_situation_id="d6066_BB_flop"` → tier 1 returns it verbatim. Correct.
- Mode-A record with `deal_id=521, hero_position='BB', street='flop'` and `source_situation_id=None` → tier 2 returns `d521_BB_flop`. Correct.
- Mode-B record with only `pilot_hand_id='PILOT_101'` → tier 3 returns `PILOT_101`. Correct.

One subtle edge the code handles correctly: `source_situation_id` falsy check
uses `if ssi:` not `if ssi is not None:`, which catches both `None` and empty
string `""`. That is the right guard — an empty string ref_id would be a
collision risk.

The `prepare()` function enforces uniqueness post-computation via a Counter
check and raises `RuntimeError` with the collision list. The collision-rejection
test (`test_prepare_rejects_collisions`) verifies this path.

**Note on resolution directive §3 wording:** the directive states
`ref_id = f"{deal_id}_{hero_position}_{street}"`. The script produces
`f"d{deal_id}_{hero_position}_{street}"` (leading `d`). This matches the
Phase B Protocol A artefact format (`d6066_BB_flop`, `d521_BB_flop`, etc.)
and `reference_evaluator.py:95` keying. The directive wording omitted the
`d` prefix; the code is correct, the directive was slightly imprecise.

---

## 2. Consensus logic — PASS

The `consensus()` function in `collect_mass_labels.py`:

- Filters nulls before counting: `non_null = [v for v in votes if v is not None]`
- Confidence = `top_count / valid_count` (non-null denominator) — correct per directive §2
- Tie-break: `sorted(tied)[0]` → alphabetical. Deterministic.
- All-null case: returns `consensus_action=None, confidence=0.0` immediately.

Edge cases verified against tests:

| Scenario | Code result | Expected | Status |
|---|---|---|---|
| 5× BET | BET, 1.0 | BET, 1.0 | PASS |
| 3 BET + 2 CHECK | BET, 0.6 | BET, 0.6 | PASS |
| 3 BET + 1 CHECK + 1 null | BET, 0.75 (3/4) | BET, 0.75 | PASS |
| 5 nulls | None, 0.0 | None, 0.0 | PASS |
| 2 BET + 2 CHECK + 1 null | BET, 0.5 (2/4), alphabetical | BET | PASS |
| 1 RAISE + 4 nulls | RAISE, 1.0 (1/1) | RAISE, 1.0 | PASS |
| empty list | None, 0.0, vote_count=0 | None, 0.0 | PASS |

The end-to-end integration test (`test_collect_aggregates_5_labellers_on_2_hand_fixture`)
exercises the collect pipeline on a 2-hand × 5-labeller fixture including a
refusal, a tie, and a missing-file scenario. All assertions hold.

---

## 3. Cost-bounding logic — NIT (non-blocking)

The dispatch script does not invoke the Agent tool (Python can't; builder
dispatches from session) and therefore contains no cost-tracking code. This is
expected and documented in the script header and PR body.

**Gap:** The resolution directive §5 requires the builder to STOP dispatch if
actual cost approaches $180. There is currently no running-cost log written
by the dispatch side — the builder will need to manually track cost in their
session or via the Claude Code UI during the 5-agent dispatch loop.

**Recommendation (nit):** Before firing the dispatch loop, the builder should:
1. Note the session cost at dispatch start.
2. After each labeller completes, record cumulative cost to
   `review/mass_labelling_2026-04-27/cost_log.txt`.
3. Abort if cumulative cost >= $180 before dispatching the next labeller.

This is operationally lightweight (5 dispatches, sequential) and doesn't
require a code change to this PR. Surfaced as a reminder for the builder's
session protocol, not a CHANGES_REQUESTED item.

---

## 4. Test coverage — ADEQUATE

24 tests across:

- `TestComputeRefId` (6 tests): covers all 3 schema paths, falsy SSI fallthrough,
  missing-all-ids raises, and full-corpus smoke (skipped if file absent).
- `TestConsensus` (8 tests): unanimous, majority, null exclusion, all-null,
  empty, two-way tie, three-way tie, single valid vote.
- `TestLoadLabellerFile` (6 tests): well-formed load, invalid action coercion,
  explicit null preserved, lowercase normalization, invalid confidence default,
  missing ref_id skipped.
- `TestCollectIntegration` (2 tests): 5-labeller 2-hand fixture + missing
  labeller file handling.
- `TestDispatchPrepare` (2 tests): brief + manifest output, collision rejection.

Coverage is adequate for the deterministic helpers. Agent-tool dispatch is
correctly excluded from unit testing per PR body.

**Minor gap (nit):** No test exercises the `majority_wins_3v2` confidence path
with `valid_count == total_count == 5` (i.e., no nulls, 3 vs 2 split) to
confirm confidence = 0.6 exactly. The `test_plurality_majority` test covers
this case (`['BET', 'BET', 'BET', 'CHECK', 'CALL']` → 0.6). On re-read:
this IS covered. No gap.

Actual minor gap: no test for the refusal-rate warning path in `collect()`
(>5% refusal rate triggers stderr warning). Low-risk omission given the
warning is informational only.

---

## 5. Schema match to Phase B Protocol A — PASS

The brief template in `_build_brief()` embeds the output schema contract
verbatim in markdown. The schema specified is:

```
{lane, model, protocol_version: "v3.2", protocol: "<path>",
 total_labels, labels: [{ref_id, action, confidence, reasoning}]}
```

This matches the Phase B Protocol A artefact on master `4bce49f`
(`{lane, model, protocol_version, protocol, total_labels, labels: [...]}`).

The `_load_labeller_file()` function in collect reads exactly these fields.
The `_write()` helper in `TestLoadLabellerFile` also produces this schema,
so the round-trip is exercised in tests.

One alignment note: the Phase B artefact has `"protocol": "A"` (a short label).
The new schema uses `"protocol": "prompts/gto_labeller_v3.2.md"` (a path).
This is an intentional improvement per resolution directive §2 ("matching Phase
B Protocol A schema" refers to structure, not the literal string in the
`protocol` field). Not a defect.

---

## Summary

| Check | Result |
|---|---|
| ref_id handles all 3 schemas | PASS |
| ref_id uniqueness enforced | PASS |
| Consensus plurality correct | PASS |
| Null votes excluded from tally | PASS |
| Alphabetical tie-break deterministic | PASS |
| All-null case handled | PASS |
| Cost-bounding in script | N/A (no Agent calls in script; session protocol gap noted as nit) |
| 24 tests adequate | PASS |
| Schema matches Phase B Protocol A structure | PASS |

**Nit 1 (operational, no code change):** Builder should maintain a
`cost_log.txt` during dispatch to enforce the $180 abort threshold
from resolution directive §5.

**Nit 2 (trivial):** Resolution directive §3 wording omits the leading `d` in
the ref_id format. Code is correct; directive wording was imprecise.
No action needed on the code side.

QC: clear to proceed with V-Impl-Spec-Match + V-Integration-Trace audit.
Scripts may merge.
