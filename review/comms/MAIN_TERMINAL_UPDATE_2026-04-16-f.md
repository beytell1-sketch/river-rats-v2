---
date: 2026-04-16
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Track D PA_Board3 decision + Group D registry finalisation — Phase 3 unblocks
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-16 (f)

Both pending items resolved. Phase 3 can launch once these
land.

## 1. Track D — Drop to 3 curated

Accept the 3 cleanly-staged curated hands (`d1983_BTN_turn`,
`BP7_06`, `d5620_BTN_flop`). Drop `PA_Board3_Jh8h4h_h6`. Do
NOT patch the v23 copy.

### Rationale

- The PA_Board* pool has **systemic** defects (`street='f'` +
  table-size-not-villain-count). Patching one record doesn't
  fix the pool and creates undocumented drift that will
  confuse future audits.
- Supplement total: 420 → 398. UMBRELLA (268 hands) already
  covers the Section 2 predicate shape including drawing
  hands with `equity_vs_range ≥ 0.35 ∧ worse_hand_pct ≥ 0.55`.
  Coverage loss is marginal.
- 3 concentrated nut-blocker hands is still real-distribution
  signal.
- The Phase 7 backup clause (factory sub-pattern) remains
  available if drawing-signal gap surfaces post-validation.

### Commits

- Commit the 3 curated hands to
  `training-data/v23_curated_draw_{flop,turn}.jsonl` as split
  by their streets.
- Update `V23_HAND_GENERATION_PLAN_2026-04-16.md §1.2` rows
  6-7 entry: "3 confirmed nut-blocker curated hands staged;
  `PA_Board3_Jh8h4h_h6` dropped per PA_Board* upstream defect
  (see §2). UMBRELLA absorbs predicate coverage."
- Update `V23_CURATED_CANDIDATES_2026-04-16.md` with
  disposition notes.

### Separate cleanup ticket (non-blocking)

Open a ticket tracking the PA_Board* pool upstream defect:
`review/comms/TICKET_PA_BOARD_POOL_DEFECT_2026-04-16.md`

Content:
- Defect: PA_Board* records emit `street='f'|'t'|'r'` (single
  char) not `'flop'|'turn'|'river'`; `num_opponents` set to
  table size not villain count
- Scope: unknown (count PA_Board* records in source pool,
  list affected sids)
- Fix target: normalise at serialisation boundary, similar to
  Fix 1 for BP generators
- Priority: post-v2.3-ship cleanup unless another v2.3 track
  needs PA_Board* data
- Owner: not blocking anyone right now; log for v2.3 backlog

This is a record-keeping ticket, not a work item to execute
now.

## 2. Group D — 4 picks final

Ingest the builder's suggested default into
`river-rats-core/calibration_exam.py`
`GROUP_D_REVERSAL_HANDS`:

```python
GROUP_D_REVERSAL_HANDS = {
    'd3688_BB_flop',     # existing (Stream B.2 d3688 over-bet)
    'd4312_CO_turn',     # bias-sig + solver CHECK override (gold standard)
    'd9556_BB_flop',     # solver-confirmed trap on paired flop, OOP, SPR 1.25
    'd2074_BTN_turn',    # vrc=0 guard test, IP, turn, paired board
    'd5466_CO_flop',     # vcb=0 guard test + flop PFR-first-to-act
}
```

### Why these four (not d3687 or BP4_21)

The Group D purpose is to test whether v2.3 **resists
over-applying** the BET override on hands that look similar
to the bias signature but should be CHECK. Picks must:

1. Represent both "override-fires-correctly" shapes and
   "guard-prevents-over-firing" shapes
2. Carry clean poker reasoning that v2.3 can test against
3. Avoid mixed-zone ambiguity (100%-pass gate intolerant of
   GTO-ambiguous spots)

The selected four cover:
- **Full bias-sig + solver CHECK override** (d4312) — hardest
  legitimate anchor
- **Solver-confirmed trap** (d9556) — tests slowplay discipline
  without relying on vcb/vrc triggers
- **vrc=0 guard** (d2074) — tests the override does NOT fire
  when villain range is uncapped
- **vcb=0 guard + flop diversity** (d5466) — tests the
  override does NOT fire when villains haven't checked back

**Explicit exclusions with reasoning:**
- `d3687_HJ_turn` (quads) — features so extreme (worse=1.0,
  evr=1.0) any rational BET-leaning system BETs here. Signal
  uninformative about override calibration specifically.
- `BP4_21` — solver says BET 25%, v2.2 label kept CHECK in
  mixed zone. Genuinely GTO-ambiguous. 100%-pass gate should
  not punish a defensible action choice.
- `BP4_11` (set trap) — d9556 is diagnostically stronger for
  the same slowplay slot (solver-confirmed vs Pass-2-only).
- `BP5_01` (bottom 2pair OOP) — non-bias-sig shape with
  different failure mode; strong pick but 4 slots are full,
  d9556 edges it on clarity.
- Source A hands d6869, d1764, d6826 — each is a valid
  single-axis-fail test but d2074 and d5466 cover the same
  guard semantics with stronger poker clarity.

### Ingestion verification

After commit, the existing extensibility test
(`test_calibration_exam_extensibility` at line ~246 of
`calibration_exam.py` tests) must still pass without
modification. Run it to confirm.

## 3. What unblocks

With both items resolved:

| Track | State |
|---|---|
| Phase 1 generation | ✅ 483 factory + 3 curated = 486 hands |
| v3 prompt | ✅ |
| Calibration exam (23/28 + Group D full) | ✅ on commit |
| Phase 2 assembly QA | ✅ (prior) |
| Phase 3 calibration gate | 🟢 ready to launch |
| Phase 3.5 pilot | ⏸️ gated on Phase 3 |
| Phase 4 production labelling | ⏸️ gated on Phase 3.5 |

## 4. Launch Phase 3

Once §2 lands (Group D ingested + extensibility test passes):

- Run the calibration exam
- Target: 23/28 correct + 100% on all 5 reversal hands
  (d3688, d4312, d9556, d2074, d5466)
- If PASS: proceed to Phase 3.5 pilot
- If FAIL: panel redesign per plan §3.3 — do NOT proceed to
  Phase 3.5

Deliverable: `review/comms/PHASE_3_CALIBRATION_2026-04-16.md`
with per-hand verdict, aggregate score, reversal-hand tally,
pass/fail.

Push immediately.

## 5. Owner touchpoints (further narrowed)

- Phase 3.5 pilot spot-check on 3-5 hands (~30 min) when
  pilot report lands
- Solver sessions for row 11 + auto-enqueue reserve at owner
  pace (non-blocking)
- Phase 7.3 solver validation on 8 MW misses at v2.3 ship gate
- v2.3 ship sign-off after all gates pass

Everything else runs.
