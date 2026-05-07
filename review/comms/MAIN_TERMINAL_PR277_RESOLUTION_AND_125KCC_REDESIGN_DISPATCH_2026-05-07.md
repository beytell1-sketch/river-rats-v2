---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #277 + PR #279 merged (QC PASS; 34th solo cycle; factory FD-suit diagnosis VERIFIED); ratify Path 2 (redesign MW-17 + MW-47 boards with 2 FD-suit cards + re-emit + re-pilot); 12.5K-C-C-FIX dispatch
status: DIRECTIVE — merges PR #277 + PR #279; fires LEAD-PROGRAMMER on 12.5K-C-C-FIX — fire now
---

# PR #277 + PR #279 merge + 12.5K-C-C-FIX (factory redesign + re-emit + re-pilot for MW-17 + MW-47)

QC verdict on PR #277: **PASS — diagnosis VERIFIED**. 34th solo cycle. Factory FD-suit configuration bug confirmed: MW-17 + MW-47 axes' 100 situations had only 1 FD-suit board card (need 2 for `has_flush_draw=1` per labelling pipeline). MW-40 + MW-45 axes' 100 situations PASS pilot (5/5 unanimous on target action each).

## Path 2 (redesign + re-emit + re-pilot) ratified

Per quality-default `feedback_quality_default_no_ask.md` + per-axis off-ramp pattern: fix the factory bug, re-emit only the 100 broken situations (MW-17 + MW-47), re-pilot, then scale all 4 axes if pilots PASS.

**Path 1 (proceed-with-2-axes) rejected**: 50% reduction in Lever C corpus expansion is compromise; the slow-quality choice is to fix the bug.

**Path 3 (halt Lever C entirely) rejected**: bug is fixable; 2 axes already PASS; halting wastes the work.

## LEAD-PROGRAMMER — Step: 12.5K-C-C-FIX (fire on this comm merge)

Branch: `programmer/phase125k-c-c-fix-redesign-2026-05-07`. Base: master post-this-comm-merge.

### Scope — redesign + re-emit + re-pilot MW-17 + MW-47 only

#### Phase 1: Architect-hat redesign

Update plan `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` §4 sub-axis tables for MW-17 + MW-47:
- **MW-17 axis**: boards must have 2 FD-suit cards (e.g., `9s7s4d` if FD suit = ♠) for `has_flush_draw=1` to trigger
- **MW-47 axis**: boards must have 2 FD-suit cards aligned with hero's nut-FD blocker

Builder picks 50 corrected boards per axis (specifying the FD-suit configuration); document in updated plan.

Constraint: keep the structural pattern of each axis (MW-17 = under-calling on low-equity draw + facing-bet 3-way+; MW-47 = nut FD + blocker should RAISE) intact; only fix the FD-suit count.

#### Phase 2: Re-emit factory pass

Replace the existing MW-17 + MW-47 situations in `data/corpus_lever_c_situations_2026-05-07.jsonl` with corrected versions (or write a new `corpus_lever_c_situations_v2_2026-05-07.jsonl` and document the schema fix). Keep MW-40 + MW-45 situations UNCHANGED.

Per-axis pre-flight 4-check on first 5 of each corrected axis before remaining emit (mirrors original -B pattern).

#### Phase 3: Re-pilot MW-17 + MW-47

5 hands × 5 Sonnet labellers per axis (= 50 pilot labels; ~$2-3 LLM). Per-axis gate:
- ≥4/5 hands consensus on axis target action → PASS; scale to remaining 45 in that axis
- <4/5 → REPORT to orchestrator (escalate; possibly indicates the structural argument is too narrow even with correct FD config)

If BOTH pilots PASS → scale to remaining 90 (45 each); produce final 4-axis 200-hand label set (combining MW-40 + MW-45 from original PR #277 + MW-17 + MW-47 from this PR).

If EITHER pilot FAILs → STOP and escalate.

### Cost / time

- Phase 1 redesign: ~$0; ~30-45 min architect-hat
- Phase 2 re-emit: ~$0; ~10-15 min factory
- Phase 3 re-pilot: ~$2-3; ~10 min wall clock
- Phase 3 full-scale (if both pilots PASS): ~$10-15 (90 hands × 5 labellers × $0.05); ~30-45 min
- Total: ~$15-20; ~1.5-2 hours wall clock
- Within ~$300/30h cap

### What you do NOT do

- Do NOT modify MW-40 + MW-45 situations (those PASSed pilot; preserved as-is)
- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/ source
- Do NOT modify BATCH2 reference
- Do NOT skip any per-axis pilot gate
- Do NOT auto-decide to halt or proceed without orchestrator on FAIL

### Deliverable scope

1. Updated `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` (or new `_v2` plan) with corrected MW-17 + MW-47 board specs
2. `data/corpus_lever_c_situations_v2_2026-05-07.jsonl` (or in-place edit if cleaner) with corrected MW-17 + MW-47 situations
3. `data/corpus_lever_c_labels_v2_2026-05-07.jsonl` (full 4-axis labels: MW-40 + MW-45 from PR #277 + MW-17 + MW-47 fresh)
4. `scripts/regenerate_lever_c_mw17_mw47.py` (factory script)
5. `review/comms/BUILDER_REPORT_PHASE125K_C_C_FIX_2026-05-07.md`

## QC stream — what you audit (when -C-FIX PR opens)

Standalone audit, ~15-20 min, 9-item HALT-fix scope (combines redesign + re-emit + re-pilot + full-scale verifications).

QC writes `review/comms/REVIEW_QC_PHASE125K_C_C_FIX_2026-05-07.md`.

## Sequencing

After -C-FIX merges:
- 12.5K-C-D Opus tier-up (20 Opus × 5 canonical × 4 axes)
- 12.5K-C-E corpus integration + re-train (788 → 988 corpus; 5-seed re-train)
- 12.5L gate eval

## What's blocked / what's queued

**Cleared**: PR #277 + #279 merge + 12.5K-C-C-FIX dispatch.

**Queued**: 12.5K-C-D / -E + 12.5L.

**Memory candidates**: 4-check pre-flight does NOT catch domain-specific feature semantics like FD-suit count. Pilot labelling pipeline IS the only validator for these. Future factory designs should explicitly cross-check feature-semantic preconditions per labelling-pipeline rule (e.g., "if KB §1.7 nut-FD carve-out is the predicted routing, board MUST have ≥2 cards of FD suit"). Owner-scope to ratify.

**Status: PR #277 + #279 cleared. LEAD-PROGRAMMER fires 12.5K-C-C-FIX (Phase 1 redesign → Phase 2 re-emit → Phase 3 re-pilot → full-scale on PASS) on this comm merge. ~$15-20; ~1.5-2h wall clock.**
