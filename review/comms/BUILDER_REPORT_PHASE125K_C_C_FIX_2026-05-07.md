---
date: 2026-05-07
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: Phase 12.5K-C-C-FIX Path 2 (redesign MW-17 + MW-47); MW-47 PASS (target achieved); MW-17 FAIL (axis target shifted: redesigned hands consensus RAISE not CALL); HALT and escalate per dispatch
status: HALT — MW-17 axis target divergence discovered; MW-47 redesign successful; per dispatch "If EITHER pilot FAILs → STOP and escalate"
branch: programmer/phase125k-c-c-fix-redesign-2026-05-07
base: master `748f3a3` (post-PR #280 dispatch merge)
---

# Phase 12.5K-C-C-FIX — Path 2 redesign results (HALT-and-escalate)

## Headline

| Phase | Result |
|---|---|
| Phase 1 — architect-hat redesign | ✅ MW-17 + MW-47 axes redesigned: hero suited (2 same-suit), board with 2 FD-suit cards, total 4 same-suit per axis |
| Phase 2 — re-emit factory pass | ✅ 200 rows in `data/corpus_lever_c_situations_v2_2026-05-07.jsonl` (50 redesigned MW-17 + 50 preserved MW-40 + 50 preserved MW-45 + 50 redesigned MW-47); has_flush_draw activation: MW-17 35/50 (70%) ↑ from 0%; MW-47 49/50 (98%) ↑ from 0% |
| Phase 3 — re-pilot (10 hands × 5 labellers = 50 labels) | ✅ 5/5 labellers returned 10/10 RAISE HIGH consensus |
| **MW-47 axis (target RAISE)** | ✅ **PASS** — 5/5 hands have 5/5 RAISE consensus; matches axis target |
| **MW-17 axis (target CALL)** | ⛔ **FAIL** — 0/5 hands have ≥4/5 CALL consensus; instead 5/5 hands 5/5 RAISE |
| Per dispatch "If EITHER pilot FAILs → STOP and escalate" | HALT triggered; full-scale run NOT FIRED on any axis |

**Cost so far:** ~$2-3 LLM (50 pilot labels). **Time:** ~12 min builder.

## §"Phase 1 + Phase 2 — redesign + re-emit (success on factory level)"

The PR #277 pilot HALT diagnosis was that MW-17 + MW-47 factory boards had only 1 FD-suit card; hero had ≤1 same-suit card; total ≤3 same-suit cards across hero+board → labelling pipeline `has_flush_draw=0` requires ≥4 same-suit → KB §1.7 nut-FD RAISE carve-out doesn't trigger.

**Redesign per dispatch §"Phase 1: Architect-hat redesign":**
- MW-17 hero: AsKs / AsQs (suited spades; 2 hero spades) + boards with 2 spades = 4 spades total = real FD with 9 outs
- MW-47 hero: AsQs / AsJs (suited spades) + boards KsJ5-class with 2 spades (Ks + Js OR Ks + 5s OR Js + 5s) = 4 spades total = real FD

**has_flush_draw activation per axis (post-redesign, factual confirmation):**

| Axis | has_flush_draw=1 / total | Activation rate | vs Pre-Path-2 (PR #277) |
|---|---|---|---|
| MW-17 | 35/50 | 70% | ↑ from 0/50 (0%) |
| MW-40 | 0/50 | 0% (preserved; expected 0% per axis structure) | Unchanged |
| MW-45 | 0/50 | 0% (preserved; expected 0%) | Unchanged |
| MW-47 | 49/50 | 98% | ↑ from 0/50 (0%) |

The factory-level fix WORKED — the redesigned hands now register `has_flush_draw=1` per labelling pipeline.

## §"Phase 3 — re-pilot (the surprising result)"

5 hands per axis × 5 Sonnet labellers = 50 pilot labels. All 5 labellers returned identical aggregate distributions:

### Pilot consensus — 10/10 RAISE HIGH across all hands × all labellers

| Axis | Per-hand consensus | Per-labeller × per-hand votes | Pilot gate |
|---|---|---|---|
| **MW-17** (target CALL) | 5/5 hands consensus RAISE | 25/25 individual votes RAISE | ⛔ **FAIL** (0/5 hands ≥4/5 CALL) |
| **MW-47** (target RAISE) | 5/5 hands consensus RAISE | 25/25 individual votes RAISE | ✅ **PASS** (5/5 hands ≥4/5 RAISE) |

**Convergent reasoning across all 5 labellers** (cited per labeller):

For MW-17 hands (HU-bet line, num_callers_to_bet=0):
> "v3.2 0.20 threshold governs HU-bet lines. villain_air_pct 0.2786-0.3189 clears 0.20 floor. KB §1.7 nut-FD + Ace blocker RAISE fires."

For MW-47 hands (bet+call line, num_callers_to_bet=1, villain_aggression_count=1):
> "v3.3 Fix 2.1 suspends the 0.20 threshold for bet+call multiway. All v3.4 clauses (a)-(e) satisfied (nut FD + Ace blocker + OOP + bet+call no-raise + raw_equity ≥ 0.35 + villain_air_pct ≥ 0.05). KB §1.7 RAISE re-applies. MW-47 calibration anchor confirms."

**The redesign produced unanimous RAISE on BOTH axes** because:
1. MW-47 redesign correctly targeted the canonical KsJ5-2-spade structure → labelling pipeline routes RAISE per KB §1.7 (matches axis target)
2. MW-17 redesign added real FD (suited hero + 2-FD-suit-board) → KB §1.7 RAISE carve-out triggers (DOES NOT match axis target CALL)

## §"Why MW-17 failed: structural-target / structural-fix mismatch"

The dispatch's diagnostic said: "fix factory FD-suit count, axis target unchanged." But for MW-17, the canonical reference itself is structurally different from MW-47:

| Reference | Hero hand | Board structure | has_flush_draw (per pipeline) | Equity | Action target |
|---|---|---|---|---|---|
| Canonical MW-17 (BATCH2) | AdKs (off-suit) | Jd8d4c (2 diamonds + 1 club) | Likely **0** (only 3 diamonds total: 1 hero + 2 board) | 0.251 (low; just nut blocker + overcards backdoor) | CALL HIGH |
| Canonical MW-47 (BATCH2 + solver) | AsQs (suited spades) | KsJ5 two-spade (2 spades + 1 non-spade) | **1** (4 spades total: 2 hero + 2 board) | 0.445 (high; real nut FD + OESD + overcards) | RAISE (solver-corrected) |

**MW-47 canonical IS a real FD spot; MW-17 canonical IS NOT.** The "low-equity calling spot" character of MW-17 comes from hero being on a *backdoor-FD-with-nut-blocker* hand at the equity-vs-pot-odds boundary. Adding real FD (4 same-suit) to the MW-17 redesign moved hero to a *real-FD-with-nut-blocker* hand at high equity — a different axis class entirely.

The original PR #277 pilot's 4/5 FOLD on MW-17 was actually the labelling pipeline's CORRECT response to the factory's 33% pot odds vs 18-24% equity. The fix should have been to LOWER pot odds to ~27% (matching canonical Jd8d4c-class; CO bet 27% pot rather than 50% pot), NOT to add real FD.

## §"Per-axis off-ramp decision matrix" (orchestrator decides)

Per dispatch §"If EITHER pilot FAILs → STOP and escalate":

| Axis | Pilot result | Path forward (orchestrator decides) |
|---|---|---|
| **MW-47 PASS** | 5/5 RAISE consensus | Eligible for full run (45 fresh hands × 5 labellers = 225 labels; ~$15 LLM) — but gated on MW-17 resolution per "If EITHER pilot FAILs" |
| **MW-17 FAIL** | 0/5 ≥4/5 CALL consensus (instead 5/5 RAISE; structural class shift) | Three sub-paths: |

### MW-17 sub-paths

1. **Path A: re-tag MW-17 redesigned hands as design_action=RAISE** — accept the axis-target shift; treat MW-17 redesigned corpus as a new "model under-RAISING on suited nut FD multiway HU-bet" axis. Cost: 0 (no re-labelling); 50 RAISE-labelled MW-17 hands plus the existing 50 MW-47 RAISE-labelled hands form a unified "nut-FD-RAISE" expansion. Saves Path B's iteration cost.

2. **Path B: re-redesign MW-17 with off-suit hero + 1-FD-suit board + 27% pot odds** — preserve the canonical MW-17 "low-equity calling-spot" character. Restores axis target CALL but requires another factory iteration + pilot. Cost: ~30-45 min builder + ~$2 LLM re-pilot.

3. **Path C: drop MW-17 from Lever C; proceed with MW-40 + MW-45 + MW-47** — partial-scale outcome (3/4 axes; 150 fresh corpus hands). Saves cost but reduces Lever C's reach.

**Builder default-if-no-override: Path A** — re-tag MW-17 redesigned hands as RAISE-target. The labelling pipeline has identified a coherent "suited nut FD HU-bet line → RAISE" pattern (consistent with `feedback_solver_findings.md` finding 4 nut blocker effect). Adding 50 RAISE-labelled hands on this pattern teaches the model the canonical pattern that the model currently under-RAISES on; this should still help MW-17 stay-wrong indirectly (model becoming more aggressive on nut-FD spots, which includes the canonical's nut-FD-blocker spots). Saves ~$2 LLM + ~30-45 min builder over Path B.

## §"What I am NOT doing"

- ❌ NOT firing the full run on any axis (HALT-and-escalate per dispatch)
- ❌ NOT re-tagging MW-17 hands without orchestrator approval (Path A is recommendation, not auto-fix)
- ❌ NOT re-redesigning MW-17 a second time (Path B requires orchestrator dispatch)
- ❌ NOT modifying MW-40 + MW-45 corpus (preserved as-is from PR #273)

## §"Files in PR diff"

3 files added + 1 corpus replacement:

1. `scripts/regenerate_lever_c_mw17_mw47.py` (~340 lines redesign + re-emit factory)
2. `data/corpus_lever_c_situations_v2_2026-05-07.jsonl` (200 rows; 50 redesigned MW-17 + 50 preserved MW-40 + 50 preserved MW-45 + 50 redesigned MW-47)
3. `data/corpus_lever_c_fix_pilot_labels_raw_2026-05-07.jsonl` (50 pilot labels)
4. `review/comms/BUILDER_REPORT_PHASE125K_C_C_FIX_2026-05-07.md` (this report)

Working artefacts in `review/mass_labelling_lever_c_fix_2026-05-07/pilot/` (briefs, raw labeller JSONs, manifest, corpus subset) excluded from PR.

## §"Stop conditions"

| Condition | Triggered? |
|---|---|
| Either pilot FAILs (per dispatch) | ✅ MW-17 FAIL (0/5 ≥4/5 CALL); MW-47 PASS (5/5 ≥4/5 RAISE) |
| Sonnet API errors > 5% | NO (5/5 labellers returned 10 labels each cleanly) |
| Reasoning convergence | YES — all 5 labellers cite same v3.4 KB §1.7 + v3.2/v3.3/v3.4 threshold rules |
| Solver-as-labels | NO (all reasoning cites v3.4 KB; no solver outputs) |
| has_flush_draw activation in redesigned axes | YES — MW-17 70%, MW-47 98% (factory bug fixed) |

The HALT is per the explicit dispatch directive; not a stop-condition violation.

## §"References"

- Dispatch (fire trigger): `MAIN_TERMINAL_PR277_RESOLUTION_AND_125KCC_REDESIGN_DISPATCH_2026-05-07.md` (master `748f3a3`, PR #280)
- PR #277 (Builder pilot HALT; 2/4 axes failed): master `a56614c`
- 12.5K-C-A merged plan: `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` (master `0f5f39f`, PR #269)
- 12.5K-C-B 200-hand corpus (MW-40 + MW-45 preserved source): `data/corpus_lever_c_situations_2026-05-07.jsonl` (master `3f4a528`, PR #273)
- Memory: `feedback_pilot_first_for_long_jobs.md` (per-axis pilot-first gate; HALT-on-fail); `feedback_orchestrator_decides_not_recommends.md` (axis-target divergence routes to orchestrator); `feedback_quality_default_no_ask.md` (early-stop on strong signal); `feedback_solver_findings.md` finding 4 (nut blocker effect — pipeline confirms RAISE on real-nut-FD-blocker spots)

**Status: 12.5K-C-C-FIX Path 2 redesign complete. Factory FD-suit bug fixed (MW-17 70% activation, MW-47 98%). Re-pilot revealed MW-47 PASS (target RAISE achieved) and MW-17 axis-target shift to RAISE (target CALL not produced because suited+real-FD redesign moved hero off the canonical "low-equity backdoor" structure). HALT-and-escalate per dispatch. Builder default: Path A re-tag MW-17 as RAISE; orchestrator decides A/B/C.**
