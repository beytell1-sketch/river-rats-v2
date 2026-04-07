# Handoff: Old Terminal → New Terminal

**Date:** 7 April 2026
**Context:** Old terminal has exhausted its useful context window. New terminal is running and ready to take over. Old terminal shifts to reviewer role.

---

## What the new terminal should do NEXT

### Priority 2+3 are combined: Research → Factory Batch 2 Design

**Research is DONE.** Three deep research files committed:
- `research/semi_bluff_multiway_research.md` (15+ sources)
- `research/blocker_effects_research.md` (20 sources)
- `research/draw_play_multiway_research.md` (18 sources)

**Research has been independently reviewed:**
- `review/REVIEW_RESEARCH_QUALITY.md` — PASS with 2 caveats

**Semi-bluff board designs exist but need revision:**
- `review/DESIGN_SEMI_BLUFF_SWEEPS.md` — 6 boards, 54 situations
- Reviewer found: Board 5 Hand 3 is a flopped straight mislabelled as middle pair
- Missing: 1 SPR-collapsed board, 1 river bricked-flush-draw board (Ace blocker paradox)

### What needs to happen now:

1. **Fix the 2 semi-bluff design issues** (Board 5 hand correction, add SPR-collapsed + river boards)

2. **Design the remaining ~206 situations** across these categories:
   - 45 flush-blocking spots (activate flush_block_pct feature)
   - 40 overcard spots (activate overcard_outs feature)
   - 35 thin value / raise spots
   - 86 general broad distribution
   - Target: 30 boards total, ~8.7 situations/board
   - Turn/river heavy (73% of new batch)
   - RAISE target: 10% of new batch

3. **Run calibration exam** with v1.2 knowledge base before labelling (MANDATORY — checksum changed)

4. **Generate through factory, label, combine with existing 348, retrain v9-3way-v3 on 48 features**

### Key context the new terminal needs:

- **Ace blocker paradox:** As is BEST for flop/turn semi-bluff raising, WORST for river bluffing (blocks villain's folding range). Factory must include BOTH to teach the distinction.

- **Low-kicker nut flush draws check-raise MORE** than high-kicker (counterintuitive — low kicker has less showdown value, prefers aggression). Include this in factory designs.

- **Draw out-threshold matrix** from research is synthesized, not solver-verified. Use with caution for designing factory situations.

- **facing_raise bug is FIXED** in self_play.py and situation_factory.py. All training data corrected.

- **v2.2 is production model** (45 features, 32/40 reference). v3 with 48 features showed no improvement at 349 samples — need 600+ to activate new features.

### Protocol reminders:
- Plan before build, present for review
- Multiple experts design, independent reviewer checks
- Blind calibration exam before labelling (graded against answer key, agent cannot see answers)
- Leakage check before every gate
- No predicted labels in factory designs — Expert labels everything fresh
- Solver verify RAISE/CALL boundaries
- Bettor goes LAST in villain_positions list (factory convention)

## Files to read first:
1. `review/RESTART_PROMPT_V9_3WAY.md` — full project state
2. `docs/LABELLING_PIPELINE.md` — step-by-step labelling process
3. `review/SPEC_KNOWLEDGE_BASE_V1.2.md` — what changed in KB
4. `review/REVIEW_FACTORY_BATCH_2_PLAN.md` — reviewer findings on batch 2
5. `review/REVIEW_RESEARCH_QUALITY.md` — research review with caveats
6. `review/DESIGN_SEMI_BLUFF_SWEEPS.md` — existing semi-bluff designs (need fixes)

## Old terminal's role going forward:
Reviewer. The new terminal presents work, the old terminal gives feedback. This handoff document is the bridge.
