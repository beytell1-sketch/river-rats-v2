---
date: 2026-04-24
from: Main terminal (orchestrator)
to: Builder · Teaching · Owner
re: Resolutions on teaching C5.1 cross-stream Findings A + B
status: DECISIONS — Finding A resolved; Finding B authorises option (A); builder folds promotion into commit 14
triggered_by: Teaching C5.1 at cff8159 (teaching/v4-1-nan-render)
---

# Cross-Stream Findings — Resolutions

Teaching's C5.1 fixture swap (cff8159) surfaced two findings via
empirical verification against real commit-4.1 output. Both resolved
here.

## Finding A — `nut_flush_block` hero-side treatment VERIFIED

**Teaching empirical observation** (C5.1 fixture swap):
> "Empirical confirmation from real `extract_all_features` output at
> commit 4.1 on both F1 (`_villain_folded=True`) and F2
> (`_villain_chain_overflowed=True`): `nut_flush_block = 0` (plain
> int). Hero-side truth preserved under both sentinels."

**Verdict: RESOLVED.** The cross-stream follow-up flagged in
`MAIN_TERMINAL_TEACHING_V4_1_DECISIONS_2026-04-22.md` §4 is CLEARED
without a builder fix-forward. Commit 4.1's MUST #10 NaN-allowlist
correctly excluded `nut_flush_block` (4 continuous blockers only;
the boolean stays int).

**Builder action:** none required. Commit 13 addendum already
documented the stable behavior.

**Teaching action:** proceed on the confirmed assumption (`nut_flush_block`
stays int 0/1 in ALL modes). Hardening re-pass can finalise on this.

**Teaching HOLD item #2 CLEARED.**

## Finding B — Multiway fields NOT promoted to features dict

**Teaching observation:**
> "`extract_all_features` at commit 4.1 does not expose
> `_per_villain_folded` or `_per_villain_composition` on the features
> dict. The data exists inside `_get_chain_narrowed_villain_range`'s
> meta return (lines 907-915 of feature_extractor.py) but isn't
> promoted onto the output features dict."

**Consequence:** teaching's multiway partial-fold preamble + per_villain
composition rendering cannot fire from real commit-4.1 production
rows. Multiway hands would silently fall through to HU rendering.

**Teaching proposed 3 options:**
- (A) Logic promotes the fields (~30 LoC). RECOMMENDED.
- (B) Teaching derives locally. REJECTED (duplicates logic).
- (C) Ship v4.1 with multiway pathway dormant. Graceful degradation.

**Decision: (A) — logic promotes.**

Rationale:
- 30 LoC is small. Not worth architectural compromise.
- (B) duplicates logic's chain narrowing into teaching layer —
  violates project's "teaching doesn't fabricate; feature data pipes
  through" contract.
- (C) ships a known-broken multiway path. Teaching's v4.1 render
  specifically calls this out as a first-class case. Shipping dormant
  means v4.1.x or v4.2 is a known follow-up we know we'll need.
  Quality default: fix at source.

**Builder action — fold into commit 14 (M4 re-audit expansion):**

Commit 14's scope already includes M4 distribution-report expansion
that audits composition + NaN + mass + equity-shift. Adding
`_per_villain_folded` + `_per_villain_composition` + (optional)
`_per_villain_overflowed` as promoted features dict keys:
- Natural fit — M4 audit would want these promoted anyway to
  verify multiway chain fires correctly per-opponent
- Single file edit (`extract_range_composition` return dict) + the
  existing meta already contains the data
- 30 LoC estimate aligns with teaching's measurement

Spec for the promotion:

```python
# In extract_range_composition's return dict (commit 14 addition):
# Promote per-villain fields from _chain_meta so downstream consumers
# (teaching renderer, M4 re-audit, debug dumps) can read without
# re-invoking the chain helper.
#
# Only populates on multiway hands (num_opponents >= 2); HU stays
# unchanged.
return {
    # ... existing fields ...
    '_per_villain_folded': chain_meta.get('per_villain_folded', {}),
    '_per_villain_composition': chain_meta.get('per_villain_composition', {}),
    '_per_villain_overflowed': chain_meta.get('per_villain_overflowed', {}),
    # Existing: '_villain_range_chain_steps', '_villain_folded', etc.
}
```

Test plan addition to commit 14:
- `test_must46_per_villain_folded_promoted_in_multiway`
- `test_must46_per_villain_composition_promoted_in_multiway`
- `test_must46_per_villain_overflowed_promoted_in_multiway`
- Assert HU hands have empty dicts (no regression)
- Assert multiway hand with one folded has correct {BTN: True, BB: False} shape

Not commit 13.1 scope. Builder proceeds with commit 13 mid-lift
owner-gated authoring independently of this.

**Teaching HOLD item #5 OPENED:** teaching's full SHIP REPORT cannot
finalise until logic commit 14 lands with the promoted fields.
Teaching's F3/F4 multiway fixtures currently synthetic — swap to
production rows after commit 14.

## Teaching HOLD status updated

| # | Item | Status |
|---|---|---|
| 1 | Stage 3.5 commit 16 landed + M4/M5 clean | ⏳ in flight (commit 13 mid-lift pending owner) |
| 2 | nut_flush_block hero-side verified | ✅ CLEARED (Finding A) |
| 3 | C5 synthetic → production fixture swap | 🟡 PARTIAL (F1/F2 done; F3/F4 blocked by Finding B) |
| 4 | Orchestrator pre-Stage-6 gate check | ⏳ pending |
| 5 | Commit 14 promotes multiway fields | ⏳ NEW (from Finding B) |

Teaching stays HOLD at C6 SHIP REPORT PRE-VERIFICATION state.
Proceed with:
- Per-commit V3 review on C5.1 (as teaching flagged — optional but
  good discipline; dispatch if scope has doubt)
- Draft SHIP REPORT with all 5 HOLD items marked
- Wait for commit 14 to complete F3/F4 fixture swap

## Builder action summary

1. Proceed to commit 13.1 authoring IF owner greenlights mid-lift gate
   (separate decision; not affected by Finding B resolution)
2. In commit 14 (M4 re-audit), fold in the 30-LoC promotion of
   `_per_villain_folded` + `_per_villain_composition` +
   `_per_villain_overflowed` per spec above
3. Add the 4 test cases listed above to commit 14's test coverage
4. Commit 14 commit message explicitly notes the Finding-B resolution

## Orchestrator action summary

1. This doc pushed ✓
2. Teaching relay via comms (paste below) ✓
3. Commit 13.1 gate still owner-pending — no change
4. On commit 14 landing, check that Finding B is addressed before
   greenlighting further commits
5. Post-commit-16: pre-Stage-6 gate check triggers teaching merge
   greenlight

## Reference

- Teaching C5.1 findings doc: `teaching/v4-1-nan-render:review/comms/TEACHING_V4_1_CROSS_STREAM_FINDINGS_2026-04-24.md`
- Teaching C5.1 at cff8159 on feature branch
- Logic commit 13 at 79c618e on master
