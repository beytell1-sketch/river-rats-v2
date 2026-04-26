---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Teaching builder · Owner (briefed) · QC stream (briefed)
re: HIGH-4 cross-stream coordination — `_villain_chain_overflowed` / `_villain_folded` aggregate semantics; logic + teaching alignment proposal; quality-default pick is Option B (honor §3.7 amendment per CONTENT_API.md:230); cross-stream directive cascade
status: PROPOSAL + DIRECTIVE — Option B greenlit per quality default; logic builder adds aggregate derivation; teaching keeps current spec + extends test coverage; queued for owner override if Option A preferred
---

# HIGH-4 Cross-Stream Coordination — Aggregate Semantics

## Background

QC Phase 2 + Phase 3 surfaced the same finding from two angles:

- **Phase 2 MEDIUM** (HOLD #12, in `QC_HIGH_FINDING_COMMIT14_CONTRACT_DRIFT_2026-04-26.md`):
  CONTENT_API.md:230 cites Stage 3.5 v2.2 amendment §3.7 — aggregate
  `_villain_chain_overflowed` is `True` when ANY opponent is
  overflowed. But `extract_range_composition` runs HU narrowing on
  `villain_pos` only; aggregate flags reflect primary villain alone.

- **Phase 3 HIGH-4** (in `QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md`):
  Same finding grounded in code at `feature_extractor.py:888-894`.
  Aggregate `_villain_folded` / `_villain_chain_overflowed` propagate
  to:
  - Teaching's `_detect_range_mode` (mode label drift)
  - Logic's Step 12 blocker NaN-flagging at `feature_extractor.py:2332`

**Effect:** on a 3-way+ hand where a non-primary opponent is
overflowed, `range_rendering_mode` may read `"normal"` while one
per-villain entry is overflowed. Per-entry sentinels are correct;
aggregate is not.

This finding was held back from Task 4.5 (logic hardening) because
it needed cross-stream alignment with teaching first. Now is the
time.

## Two options

### Option A — Aggregates = primary-villain-only

- Logic keeps current behavior at `feature_extractor.py:888-894`
- Teaching CONTENT_API.md:230 retracted (the §3.7 amendment removed
  or restated)
- Teaching's `_detect_range_mode` keeps current consumption
- Mode label always reflects primary villain

**Pros:**
- No logic code change
- Implementation is simpler
- Aggregate has a single source-of-truth (the primary villain
  narrowing)

**Cons:**
- Walks back a deliberate spec amendment (§3.7 was added to
  CONTENT_API.md:230 explicitly to capture the per-villain →
  aggregate semantics)
- Multiway-clarity loss: a 3-way hand where the secondary opponent
  has overflow won't surface in mode label even though the per-
  entry sentinel is correct
- Documentation gymnastics needed to explain why the amendment
  was retracted

### Option B — Aggregates per §3.7 amendment

- Logic adds aggregate derivation per QC's suggested patch:
  ```python
  # After line 2303 in feature_extractor.py
  features["_villain_chain_overflowed"] = (
      bool(features["_villain_chain_overflowed"])
      or any(features["_per_villain_overflowed"].values())
  )
  features["_villain_folded"] = (
      bool(features["_villain_folded"])
      or all(features["_per_villain_folded"].values())
  )
  ```
- Teaching CONTENT_API.md:230 + `_detect_range_mode` stays
- Mode label correctly reflects "any opp overflowed → mode
  reflects overflow" / "all opps folded → mode reflects folded"

**Pros:**
- Honors the §3.7 amendment that's already in CONTENT_API
  (deliberate documentation choice, not accidental drift)
- Multiway-clarity: mode label reflects the most stringent state
  across opponents (matches teaching's intent of "this hand has
  some overflow risk to address")
- Correctness: aggregates derived from per-villain sentinels means
  no double-source-of-truth confusion
- Backward-compatible at the contract surface (consumers reading
  the aggregate get the spec-documented value)

**Cons:**
- Requires logic code change (~6 lines)
- Need to verify that derivation doesn't break anything in
  blocker NaN-flagging at Step 12 (probably fine; Step 12
  consumes the aggregate, and any/all derivation just makes the
  aggregate more conservative on overflow + less conservative on
  fold — both are spec-aligned)

### Quality-default pick: Option B

`feedback_quality_default_no_ask.md`: "Always recommend AND execute
the slow/quality path."

**Option B honors the spec.** §3.7 amendment was added deliberately;
walking it back requires more justification than implementing it.
The implementation is small (~6 lines + test coverage), the
correctness is improved (aggregates match per-villain truth on
multiway), and there's no production-state migration cost (no
historical data shape change; the aggregate flags are derived
on-the-fly per feature extraction).

**Quality default: Option B.** Owner has authority to overrule;
surface preference if Option A wins.

## Sequencing

**This is NOT gating Task 5 (Pilot orchestration v1.0)** — Task 5
can document the aggregate semantics choice (whichever way it
lands) without depending on a specific value. Task 5 authoring
proceeds in parallel.

**This IS gating Stage 5 retrain** — model retraining on commit-14-era
multiway training rows depends on stable aggregate semantics. We
want this aligned BEFORE Stage 5 retrain dispatch, but AFTER Task 5
authoring (Task 5 doesn't depend on it; Stage 5 does).

**Recommended sequence:**
1. **NOW:** Owner reviews Option A vs B; quality-default pick (B) is
   the standing recommendation. If owner overrules → Option A.
2. Logic builder ships Option B (if confirmed) on a small branch
   (`stage4-prep/high-4-aggregate-semantics`) — ~30-60 min including
   test coverage
3. Teaching extends test coverage on `_detect_range_mode` to
   exercise the aggregate-derivation behavior — ~15-30 min on a
   small branch in teaching repo
4. QC re-audits both streams post-fix (game-side re-audit if Phase B
   integration consumes aggregate semantics)
5. Pilot dispatch gate: HIGH-4 SEALED on this PR pair landing

## What logic builder does (Option B)

### Branch

`stage4-prep/high-4-aggregate-semantics`

### Scope

1. After the per-villain composition derivation at
   `feature_extractor.py:888-894`, add the aggregate-derivation
   block per QC's suggested patch:
   ```python
   features["_villain_chain_overflowed"] = (
       bool(features["_villain_chain_overflowed"])
       or any(features["_per_villain_overflowed"].values())
   )
   features["_villain_folded"] = (
       bool(features["_villain_folded"])
       or all(features["_per_villain_folded"].values())
   )
   ```
   (Adjust to actual surrounding code shape; QC's snippet is
   illustrative.)

2. Add a regression test in
   `river-rats-core/tests/test_high_4_aggregate_semantics.py` (new
   file or extension to existing) asserting:
   - 3-way hand with `_per_villain_overflowed = {BB: False, CO: True}`
     produces aggregate `_villain_chain_overflowed = True`
   - 3-way hand with `_per_villain_folded = {BB: True, CO: True}`
     produces aggregate `_villain_folded = True`
   - 3-way hand with `_per_villain_folded = {BB: True, CO: False}`
     produces aggregate `_villain_folded = False`
   - HU hand (single opponent) preserves current behavior
   - The aggregates are functions of the per-villain sentinels
     (not separate sources of truth)

3. Verify that Step 12 blocker NaN-flagging at
   `feature_extractor.py:2332` still behaves correctly after the
   aggregate change. Specifically: a 3-way hand where the
   secondary opponent is overflowed should now produce
   `_villain_chain_overflowed = True` → blocker features get
   NaN-flagged. This is spec-aligned ("any opp overflowed → blocker
   unreliable") and is the change the §3.7 amendment intended.

### Acceptance criteria

1. New aggregate-derivation block lands at `feature_extractor.py`
   per spec
2. Regression test passes (4 assertions: 3-way overflow, 3-way
   folded-all, 3-way folded-partial, HU single-opponent)
3. Canonical suite still 50/50 PASS (no regression)
4. Task 4.5 hardening regressions still pass (160/160)
5. M4 audit re-run: 0/124 isolation violations, 455/455 chain
   activity (preserved)
6. M5 anchor recheck: d8411=0.661 (preserved or strengthened — the
   §3.7 fix may shift NaN-flagging on multiway hands; if it shifts,
   document the shift in the test + verify it's spec-aligned not a
   regression)

### Reviewer dispatch

Standing per-batch protocol. Independent reviewer (general-purpose
with ml-architect or gto-expert persona; small change but
load-bearing on aggregate semantics).

### Estimated effort

~30-60 min (small derivation + 4-assertion test + reviewer pass).

## What teaching builder does

### Cross-stream comm shipping to teaching repo:

`~/river-rats-teaching/review/comms/MAIN_TERMINAL_TO_TEACHING_HIGH_4_COORDINATION_2026-04-26.md`

Will be a thin pointer doc indicating:
1. Option B picked (logic adds aggregate derivation)
2. Teaching CONTENT_API.md:230 §3.7 amendment STAYS (no spec change)
3. Teaching's `_detect_range_mode` consumption STAYS (no code change)
4. **Optional but recommended:** teaching extends test coverage on
   `_detect_range_mode` to assert aggregate-derivation propagates
   to mode label correctly. Same 4-assertion shape as logic-side
   test, but at teaching layer. ~15-30 min.

### Sequencing

- Wait for logic's Option B fix to merge first (so teaching tests
  against the corrected aggregate semantics, not the broken one)
- THEN extend teaching test coverage if you want belt-and-braces
  regression guard on teaching layer
- This is OPTIONAL — logic-side fix is sufficient; teaching test
  is defensive and not gating

## What game builder does

### Phase B integration awareness

Game's Phase B per-villain bars (currently in flight per `62fee00`
greenlight) doesn't directly consume the aggregate flags — it
consumes `per_villain_composition` per-key entries. So Phase B is
not affected by Option A vs B choice.

**No game directive needed for HIGH-4.** Phase B continues per
greenlight.

## What QC does

### Re-audit queue addition

Add to QC Phase 4 standing tasks:
- Re-audit logic post-HIGH-4 fix (verify aggregate derivation
  matches §3.7 amendment + no regression on canonical/M4/M5)
- Re-audit teaching post-test-extension (if teaching ships the
  optional test extension)
- Mode-label drift re-check on multiway hands with non-primary
  overflow

These fold into QC's existing Phase 4 hourly-cadence /loop.

## Pilot-dispatch gate impact

After HIGH-4 SEALED:
- Pilot-dispatch gate: 7/9 SEALED (was 6/9)
- Remaining: teaching HIGH-1 + Task 5 + QC pre-pilot sweep + HOLD
  #21 FEATURE_COLUMNS investigation + HOLD #24 indirect propagation

```
✅ Phase 2 HIGH-2 (game adapter passlist):       SEALED
✅ Phase 3 HIGH-1/2/3 + Phase 1 HIGH (Task 4.5): SEALED
✅ Task 4.3 v1.0.3 NITs:                          SEALED
🆕 HIGH-4 cross-stream aggregate semantics:       proposal NOW;
                                                   target seal post-Option-B
⏳ Phase 2 HIGH-1 (teaching renderer translation): pending teaching
⏳ Task 5 (Pilot orchestration):                   in flight authoring
⏳ HOLD #21 FEATURE_COLUMNS contract drift:        post-Task-4.5
⏳ HOLD #24 HIGH-2 indirect propagation:           v1.1
⏳ QC pre-pilot sweep (Phase 5):                   QC standing roadmap
```

## Owner override mechanism

If owner prefers Option A:
- Surface via comms doc OR /loop tick
- Orchestrator updates this directive to Option A
- Logic builder's task changes to retracting aggregate derivation
  + teaching CONTENT_API.md:230 amendment removal directive

If owner agrees with Option B:
- No action needed; logic builder may begin when between cycles
- Quality-default pick stands

If owner has no strong preference:
- Quality default proceeds (Option B)

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 12 | MEDIUM aggregate flag derivation (Phase 2) | 🔥 ACTIVE — folds into HIGH-4 fix | Logic builder |
| 17 | Phase 3 HIGH-4 aggregate semantics (cross-stream) | 🔥 ACTIVE — Option B greenlit per quality default; awaits owner override or builder pickup | Logic builder + Teaching builder |

## References

- QC Phase 2 finding (HIGH-4 origin angle 1):
  `QC_HIGH_FINDING_COMMIT14_CONTRACT_DRIFT_2026-04-26.md` MEDIUM
  section
- QC Phase 3 finding (HIGH-4 origin angle 2):
  `QC_FINDING_COMMIT14_ARCH_STRESS_2026-04-26.md` HIGH-4 section
- CONTENT_API.md:230 (the §3.7 amendment)
- `feature_extractor.py:888-894` (current aggregate derivation site)
- `feature_extractor.py:2332` (Step 12 blocker NaN-flagging
  consumer)
- Phase 2 ACK + cross-stream cascade (`aedc3fd`):
  `MAIN_TERMINAL_QC_HIGH_FINDING_ACK_CASCADE_2026-04-26.md`
- Phase 3 ACK + Task 4.5 directive (`c1a7c0e`):
  `MAIN_TERMINAL_QC_PHASE3_ACK_TASK4_5_DIRECTIVE_2026-04-26.md`

**Status: HIGH-4 coordination proposal shipped. Quality-default pick
is Option B. Owner override available. Logic builder may pick up the
~30-60 min fix when between cycles. Teaching extension OPTIONAL.
Cross-stream directive to teaching shipping next.**
