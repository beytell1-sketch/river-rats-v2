---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-C labeller-model amendment — Opus 4.7 × 5 (was Sonnet 4.6 × 5); cap raised to $200
status: AMENDMENT — supersedes 12.5E-C dispatch §"Configuration" Sonnet line
---

# 12.5E-C labeller-model amendment

Owner question 2026-05-05: *"i noticed we used sonnet for labelling each at 110 hands. is this in line with our slow quality focused approach?"*

Honest answer: NO. Sonnet × 5 is the project's historical default, not the slow-quality maximum. Per `feedback_quality_default_no_ask.md` (reinforced 2026-05-04), labels are permanent training data; labeller blind spots poison the model forever; the H-FEAT primary test (PILOT_599/600) is the load-bearing test for the entire 12.5E migration. Opus × 5 is the slow-quality path.

**Amended:** 12.5E-C uses **Opus 4.7 × 5** labellers per hand (was Sonnet 4.6 × 5). Cost cap raised to **$200** (was $120) as buffer. Estimated actual cost ~$80-150 depending on token volume; cap is generous to avoid mid-run STOP on token-overage.

## LEAD-PROGRAMMER — what changes

### Pre-flight (mandatory before launching the labelling run)

Add to existing pre-flight checks:

- Verify `scripts/dispatch_mass_labelling.py` model-config defaults to `claude-sonnet-4-6`. The model is currently hard-coded at `dispatch_mass_labelling.py:154` (`"model": "claude-sonnet-4-6"`).
- **Update the model in this PR's diff** to `claude-opus-4-7`. This is a single-line edit in `scripts/dispatch_mass_labelling.py` plus matching docstring updates (lines 5, 21, 269, 290 reference "sonnet" — update to "opus" or generic "expert labeller" wording).
- Update `LABELLER_MODEL` constant if one exists; otherwise keep change minimal.
- Diff scope grows from 3 files to **4 files** (was: 3 new data/comm files; now: + 1 modified script).

### Configuration (amended)

| Parameter | 12.5E-C original | 12.5E-C amended |
|---|---|---|
| Labeller model | Sonnet 4.6 | **Opus 4.7** |
| Labellers per hand | 5 | 5 (unchanged) |
| Hands | 110 | 110 (unchanged) |
| Total calls | 550 | 550 (unchanged) |
| Cost cap | $120 | **$200** |
| Prompt | v3.3 | v3.3 (unchanged) |

### What you do NOT change

- 5-labellers-per-hand count (still quality default per design §6.2)
- Consensus protocol (majority class wins; existing `collect_mass_labels.py` logic unchanged)
- v3.3 prompt (unchanged)
- 110 hands and their pilot_hand_id range (unchanged)
- Any other dispatch script logic beyond the model-name change

### Stop conditions (amended)

- $200 cap reached before 550 calls complete → STOP, partial report
- All other stop conditions from original 12.5E-C dispatch unchanged

### Expected behavior change

Opus 4.7 should produce more rigorous reasoning on the per-hand poker analysis. PILOT_599/600 expected `consensus_action = RAISE` per v3.3 carve-out — same expectation as Sonnet × 5; if Opus × 5 also fails to consensus to RAISE, that's stronger empirical refutation of Path B than a Sonnet failure (because Opus is the higher-rigor model).

## QC stream — what changes for audit #4

| Audit | Original | Amended |
|---|---|---|
| 4. Cost reconciliation | ≤$120; per-call matches Sonnet 4.6 pricing; 550 calls | **≤$200; per-call matches Opus 4.7 pricing; 550 calls** |

All other audits unchanged.

**New audit hook (still under audit #1 diff scope):** the labeller model change should appear ONLY in `scripts/dispatch_mass_labelling.py` (single file). If the change touches other files, HOLD.

## Methodological consistency note (model drift between 494 and 110)

Existing 494-row corpus (master `0eaac06` and prior) was labelled with Sonnet × 5. New 110 rows will be labelled with Opus × 5. This introduces model-drift between cohorts that may or may not affect 12.5E-E re-train.

**Decision (orchestrator scope, no separate owner ask per `feedback_quality_default_no_ask.md`):** accept the drift for 12.5E-C; revisit at 12.5E-E if empirically it matters. Two failure modes to watch for at 12.5E-E:
- If 12.5E-E shows the new 110 rows have systematically different label distribution patterns (e.g., higher confidence, different RAISE rate) than the 494 rows, model drift is real and we must consider re-labelling the 494 with Opus × 5.
- If 12.5E-E shows the trainer still fails to surface `nut_flush_block` despite v3.3 carve-out + Opus labelling, the bottleneck is downstream of labelling and the drift is non-blocking.

**Queued for 12.5E-E:** drift assessment as part of trainer-report Section E. If owner wants to pre-emptively re-label the 494 with Opus × 5 NOW (full quality upgrade), that's a separate workstream (~5x cost; ~3-5 days). Not assumed.

## Why not full re-labelling of 494 NOW

Quality-maximum would re-label 494 with Opus × 5 in this PR. Reason not to:
1. The 494 corpus has been the project baseline for ~7-10 days; multiple trainer runs (12.5C, 12.5D, 12.5D') all reference the existing labels. Re-labelling changes the baseline retroactively.
2. 12.5E-E re-train on the 604-hand corpus will empirically show whether model drift matters. If it doesn't, re-labelling 494 is wasted spend.
3. Slow-quality doesn't mean "do every conceivable improvement now"; it means "don't cut corners on the work in front of you." The work in front of us is 12.5E-C. The 494 re-labelling decision is downstream of empirical evidence we don't have yet.

If owner disagrees and wants the full upgrade NOW, that's a separate amendment.

## Sequencing

1. LEAD-PROGRAMMER amends `scripts/dispatch_mass_labelling.py` model name (single-line edit + docstring updates)
2. Pre-flight + smoke test (3 hands × 1 Opus labeller — verify Opus completes successfully and outputs match expected schema)
3. Full run (550 Opus calls ≤ $200)
4. gto-expert-hat T5 spot-check (PILOT_599/600 = RAISE expected)
5. PR opens (4 files now: 3 new + 1 modified script)
6. Standalone QC audit (cost reconciliation uses Opus pricing)
7. On QC APPROVE: orchestrator merges; 12.5E-D dispatched

## What this directive supersedes

- Original 12.5E-C dispatch §"Configuration" Sonnet line
- Original 12.5E-C dispatch §"Stop conditions" $120 cap
- Original 12.5E-C dispatch §"Diff scope" 3-file count

All other content in original 12.5E-C dispatch (`MAIN_TERMINAL_PHASE125E_C_LABELLING_DISPATCH_2026-05-05.md`) stands.

## References

- 12.5E-C dispatch (original): master `e7d7843` (PR #140)
- 12.5E-A design §6.2 (5-labeller quality default): master `bad1396`
- 12.5D' synthesis addendum (12.5G queue): master `6b991b2`
- v3.2 KB §1.7 OVERRIDE motivation (both Sonnet AND Opus failed on MW-39): `prompts/gto_labeller_v3.2.md:792-833`
- Memory: `feedback_quality_default_no_ask.md` (reinforced 2026-05-04), `feedback_river_rats_team_structure.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_solver_findings.md` (Opus calibration history)

**Status: 12.5E-C AMENDED. Opus 4.7 × 5 labellers (was Sonnet 4.6 × 5). Cost cap $200 (was $120). Diff scope 4 files (was 3). 12.5E-E will assess model-drift if it matters empirically. LEAD-PROGRAMMER paused at pre-flight; pick up amendment before launching the run.**
