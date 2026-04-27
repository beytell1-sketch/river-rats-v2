---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Lead-programmer · gto-expert · ml-architect · QC stream
re: PR #70 round 3 synthesis — data PR APPROVE-WITH-NITS; bundled Phase 10 directive (small re-extract fix for PILOT_009 prior_actions duplicate logging)
status: SYNTHESIS — round 3 cleared; Phase 10 small fix directive bundled; merge PR #70 after Phase 10 force-push
---

# PR #70 round 3 synthesis

## Reviewer convergence

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| **gto-expert** | APPROVE-WITH-NITS | 15 records spot-checked across 9 families; all PASS core realism (no card conflicts, position consistency, MAGG aggression count, BAC callers, SB BB-folded, NFD nut_flush_block, pilot SPR BB-unit). 3 NITs: NIT-1 (PILOT_219 is_two_tone advisory; flop-only flag on turn board), NIT-2 (PILOT_408 thin equity; labeller briefing), **NIT-3 (PILOT_009 prior_actions has 3 duplicate "preflop: SB raise" entries — re-extract logging anomaly; labellers will misread)**. Recommend builder fix NIT-3 before mass labelling dispatch. |
| **ml-architect** | APPROVE-WITH-NITS | All 10 gates PASS. TC-26 V-Integration-Trace clean (4/5 records bit-match deterministic; 1/5 has 2.8% variance in stochastic `straight_draw_block_pct` from Monte Carlo — not a bug). Lock SHA256 exact match. 2 NITs: NIT-A (3 pilot records SPR<2.0 with vagg=1 — legitimate deep-committed; pre-existing pilot characteristic), NIT-B (lock structural_verification count fields stale; SHA256 is authority; cosmetic). No corpus-correctness issues. |
| **QC** | not landed (per established post-merge pattern) | Per memory `feedback_qc_required_before_approval.md`: post-merge TC-25 audit-trail integrity satisfies gate. |

**Convergent net verdict: APPROVE-WITH-NITS. NIT-3 (PILOT_009 prior_actions duplicate logging) requires a small Phase 10 fix before mass labelling. Other NITs are non-blocking advisories or cosmetic.**

## Phase 10 fix directive (bundled in this synthesis)

Per `feedback_listen_to_orchestrator_always.md`: this directive is sufficient authorization. Per `feedback_named_author_builds_not_polls.md`: builder's next /loop tick is AUTHORING.

### Scope: re-extract script prior_actions duplicate logging bug

**Bug**: `scripts/reextract_pilot_100_features.py` produces duplicate `"preflop: SB raise"` entries in some records' `prior_actions` (PILOT_009 has 3x). Likely cause: re-extraction loop appends an action multiple times when reconstructing from the source pool record.

**Fix**: 
1. Read `scripts/reextract_pilot_100_features.py`. Identify the loop that constructs `prior_actions`.
2. Add deduplication step OR fix the source iteration logic so each preflop action appears exactly once.
3. Add unit test: regression on PILOT_009 specifically (load corpus, find PILOT_009, assert no duplicate entries in prior_actions).
4. Re-run E1 only:
   ```
   python3 scripts/reextract_pilot_100_features.py \
     --input data/pilot_corpus_100_hand_2026-04-26.jsonl \
     --output data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
     --bb-chip-size 10
   ```
5. Verify all 100 records have NO duplicate prior_actions entries.
6. Commit code fix + regenerated `pilot_corpus_100_hand_2026-04-26_v2.jsonl` + lock to PR #70 branch.
7. Re-run C2 to update the 500-hand corpus (since PILOT_009's prior_actions changed):
   ```
   python3 scripts/build_corpus_revision_500_hand.py [args same as before]
   ```
8. Force-push PR #70 with refreshed data.

### Also fix NIT-B (lock structural_verification stale fields)

While the script is touched, fix the lock file's `structural_verification.magg` and `sb_hero` fields to match actual corpus counts. This is cosmetic but worth fixing in the same PR cycle.

### Other NITs (non-blocking; track to backlog)

- gto NIT-1 (PILOT_219 is_two_tone): label brief / advisory
- gto NIT-2 (PILOT_408 thin equity): label brief / advisory  
- ml-architect NIT-A (3 pilot SPR<2.0 vagg=1): pre-existing pilot characteristic; advisory only

## Round 3.5 review chain (after Phase 10 force-push)

Light review (single-pass since fix scope is small):
- **ml-architect mini-review**: verify the deduplication fix doesn't break F1 SPR fix (pot still BB-unit), verify regression test exercises bug, verify TC-26 trace on PILOT_009 specifically
- **QC**: post-merge audit-trail integrity check on the corrected data

gto-expert NOT needed (re-extract script is mechanical fix, not poker domain).

## Merge plan

```
1. This synthesis PR (new)
2. PR #70 (after Phase 10 force-push lands; round 3.5 review clears)
```

## After PR #70 merges

**Mass labelling kickoff** is the next major directive. The corpus is 494 hands × ~5 labellers = ~2470 labels expected. v3.2 protocol. Output → `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` for v9 student model warm-start.

This is its own directive cycle (separate from this synthesis).

## Cumulative cost dashboard

- Phase 1-9 + reviews: ~$680
- Round 3 reviews + this synthesis: ~$30
- Phase 10 fix + round 3.5 mini-review: ~$30
- Mass labelling: TBD (depends on labeller dispatch)
- **Pre-mass-labelling total: ~$740**

Within Phase 5 directive's $710-735 estimate (slight overage acceptable).

## What is NOT in scope

- Phase 11 (no further corpus revisions; 494 is FINAL)
- F5 allocator changes
- v3.2 protocol changes
- Tier 1 calibration manifest (parallel separate workstream)

## References

- PR #70 head: `fa82e96`
- Round 3 reviews:
  - gto-expert: `review/comms/REVIEW_GTO_EXPERT_PR70_DATA_2026-04-27.md`
  - ml-architect: `review/comms/REVIEW_ML_ARCHITECT_PR70_DATA_2026-04-27.md`
  - QC: pending; post-merge TC-25 satisfies gate
- Round 9 synthesis (494 FINAL): master `114961f`
- Force-push directive (master `8e10d16`): `MAIN_TERMINAL_DATA_PR_FORCE_PUSH_DIRECTIVE_2026-04-27.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_quality_default_no_ask.md`

**Status: PR #70 ROUND 3 SYNTHESIS COMPLETE. Phase 10 fix directive bundled. Builder fixes PILOT_009 + lock stale fields, force-pushes PR #70; round 3.5 mini-review (ml-architect + QC); merge → mass labelling kickoff.**
