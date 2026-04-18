---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.1 Layer 2 — HU counter-example labelling path query
status: QUERY — building generator now; flagging dependency for labelling step
---

# HU Labelling Path Query

Incorporating the 3 adjustments from REVIEW_BUILDER_AIR_CHECK_PLAN
(0a2467e) and starting the generator build now. One downstream
concern to surface before the labelling step so we can resolve it
in parallel.

## Concern

`prompts/gto_labeller_v3.1.md` is hardcoded 3-way:

- Line 1 title: "3-Way Postflop GTO Labelling Agent"
- Line 52: "You are a specialist poker agent that labels **3-way**
  postflop decisions"
- Feature 38 comment (line 480): `num_opponents` — "Number of
  opponents (2 for 3-way)"
- 26 total mentions of "3-way" / "3way"
- Knowledge base compares HU vs 3-way equity/frequencies but the
  labelling role itself is scoped to 3-way

Reviewer directive #1 asks for HU (`num_opponents=1`) counter-
examples (15–20 BP of them). The generator produces situations
fine — `SituationSpec` supports `num_opponents=1` and the factory
will build HU scenarios cleanly. But those situations then need
labels, and v3.1 isn't a labelling tool for HU spots.

## Options

### A. Adapt v3.1 in place to accept `num_opponents ∈ {1, 2}`

Cheapest option. Minor rewording: role statement, feature 38
comment, any hard 3-way assumptions in the DO NOT rules (most are
generic — some are genuinely 3-way-specific like Rule 2's
fold-equity math and Rule 8's asymmetric-ranges). Would need a
new document `gto_labeller_v3.2.md` rather than in-place edit,
per project convention.

Risk: HU calibration anchors don't exist (v2.3 calibration exam
is 3-way). Labels would be unanchored against a calibration
reference. Panels may quietly drift on HU hands.

### B. Keep v3.1 as-is (3-way only); defer HU to v2.4

Generator still builds HU specs (cheap); they sit in a separate
file `v23_air_check_hu.jsonl` unlabelled. Not in v2.3.1 training
set. Retrain on 3-way counter-examples only.

Risk: HU air-BET overgeneralization stays broken after v2.3.1
ships. But we'd at least have the data ready for v2.4.

### C. Owner manually labels the HU set

30-40 hands × ~2 min each = 1-2 hours of owner time. Highest
quality (no agent drift) but blocks on owner.

### D. 3-way only (drop reviewer adjustment #1)

Revert scope to 30-40 BP all 3-way. Requires reviewer to reverse
their directive and acknowledge the HU gap as v2.4 scope.

## Builder recommendation

**A, with B as fallback.** v3.2 derivation is ~30 minutes of work
(strip 3-way-specific reasoning aids, keep the generic
bucket-first protocol). Risk of unanchored calibration on HU is
real but labels can still be sanity-spot-checked by owner. If v3.2
derivation looks like it's eroding prompt quality, fall back to B
— keep the HU spots ready but unlabelled for v2.4.

Calling out now so we can resolve in parallel: I'll build the
generator with both HU and 3-way spec outputs (separate JSONLs:
`v23_air_check_3way.jsonl` + `v23_air_check_hu.jsonl`), run the
yield test, and report stats. By the time stats land, I'd like a
direction on A/B/C/D.

If you want to decide now, say so and I'll wait. Otherwise
proceeding with the build.
