---
date: 2026-05-06
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-F gate evaluation — median 32 unchanged across 12.5E/G/H; H-FEAT real but mistargeted; owner WHAT decision (A/B/C/D/E)
status: SYNTHESIS — owner gate
---

# Phase 12.5H-F — gate evaluation synthesis

12.5H-E re-train merged at master `283af91`. Median solver-corrected 32/40 — **identical to 12.5E-E and 12.5G across three iterations on identical reference set**. Primary gate threshold (≥33) NOT cleared.

H-FEAT primary gate (cross-seed `nut_flush_block` median ≥0.04) **CLEARED**: chosen-seed importance jumped 0.0000 → 0.0496 (+85%). Migration premise validated at feature layer.

**Same 5 stay-wrong hands across all three iterations** (MW-17/25/40/45/47). Corpus expansion +90 hands targeting these patterns flipped zero of them.

Orchestrator ran Opus second-tier evaluation per `feedback_pilot_first_for_long_jobs.md` tier-up sub-rule. Full analysis: `ORCH_OPUS_125H_F_EVALUATION_2026-05-06.md` (in this PR).

## Key findings (Opus second-tier)

### Q1: H-FEAT +85% interpretation — hybrid (a)+(c): real but mistargeted

`nut_flush_block` is genuinely the 5th-most-important feature now (above `is_monster`, `equity_vs_range`); +85% reflects real load-bearing behavior on SUITED-NFD-RAISE hands (T7-ext + T-RAISE-stabilize labels confirm).

**But only MW-17 and MW-47 have `nut_flush_block=1` at all; MW-25/MW-40/MW-45 have it at 0.** H-FEAT activation is structurally incapable of moving 3 of the 5 stay-wrong hands. Right mechanism; narrowly-targeted activation.

### Q2: Corpus expansion failure mode — per-hand mixed

- **MW-17:** (a) wrong diagnosis. E-FEATURE primary (implied-odds + nut-blocker reasoning outside 59-feature surface). T7-ext SUITED-NFD redesign trained the model on a SOUND concept but didn't transfer to MW-17's UNSUITED-overcards literal pattern.
- **MW-25 / MW-40:** (c) underpowered. 12-15 hands per template against ~100 populous-pattern CHECK/BET precedents in existing corpus — booster's gain on the new pattern doesn't dominate.
- **MW-45:** (b) + (c). T10' template likely doesn't isomorph-match MW-45's specific slowplay-action-sequence + AKQ-broadway-completed turn texture. Plus underpowered.
- **MW-47:** (a)+(b)+(c). E-FEATURE primary residual + T-RAISE-stabilize labels are SUITED-NFD-with-blocker (RAISE) but MW-47 has additional gutshot + bet+call-multiway features the booster doesn't isolate.

### Q3: Owner decision space (A/B/C/D/E) with revised probabilities

| Direction | Probability of closing gap to ≥33 | Cost / timeline | Notes |
|---|---|---|---|
| **A — PROMOTE at 32/40** | **5-10%** | ~1 builder day | Down from 12.5E-F's 10-15%; two iterations confirm no movement; weakest direction |
| **B — Abandon migration; v9-3way-v2.2 stays canonical** | **15-25%** of being right call | 10-line PR | Similar to 12.5E-F's 20-30%; H-FEAT validation continuing weakens abandonment slightly |
| **C — Feature engineering (Direction X retro)** | **35-45%** | 3-4 weeks; cascade risk per `feedback_attention_flags_when_features_change.md` | Uniquely addresses MW-17 E-FEATURE primary; only direction with tractable shot at MW-17 |
| **D — Corpus expansion to 30-40 hands per template (12.5I)** | **30-40%** | 2-3 weeks corpus + retrain | Down from 12.5E-F's 50-60% prior — 12.5H underperformance recalibrates expectation; addresses underpowered diagnosis |
| **E — Diagnostic investigation (12.5I-pre)** | **30-45% next-step EV** | ~$5 + 4-5 days | Cheap; per-hand classification before committing 2-3 weeks; breaks prediction-overconfidence pattern |

## Updated priors (transparent)

- 12.5E-F predicted 50-60% gap-close on Direction C corpus expansion. Empirical 0% (zero hands flipped).
- ml-architect 12.5D' Q4 predicted median 35-37 from H-FEAT activation. Actual 32 across two iterations.
- Cap=4.0 was empirically refuted (non-binding); cap dimension exhausted.
- Pattern: prior predictions over-estimated transfer from intermediate-layer validation to gate-score movement when residuals are heterogeneous. Owner-facing forecasts now more honest.

## Orchestrator structural read (per slow-quality default)

Slow-quality + the new explicit-trigger / pilot-first / tier-up rules → **E (diagnostic 12.5I-pre)** is the cheapest direction that breaks the prediction-overconfidence pattern. ~$5 + 4-5 days produces per-hand classification (which residuals are E-FEATURE, which are underpowered, which are isomorph-mismatch) before committing 2-3 weeks to D or C.

After E delivers diagnosis:
- If diagnosis confirms underpowered (mostly (c)) → commit D (12.5I corpus 30-40 hands/template; 30-40% gap close)
- If diagnosis confirms E-FEATURE primary on MW-17 (and likely MW-47) → commit C (feature engineering for those hands; 35-45% gap close on those specifically; doesn't help MW-25/40/45)
- If diagnosis confirms isomorph-mismatch (mostly (b)) → 12.5I redesigns templates more carefully; cheaper than C
- If diagnosis confirms NO single-direction fix → owner can pivot to B (abandon) with informed evidence rather than guessing

**E is structurally weakly-dominated by D and C in raw probability**, but it's the slow-quality path because the prior cycle's prediction errors mean we should DIAGNOSE before committing. Per `feedback_pilot_first_for_long_jobs.md` standing rule: long batches require pilot+full with explicit gate. 12.5I (D or C) is a long batch; E is its pilot.

If owner has no appetite for E, **D alone** is the next-best slow-quality direction (30-40% gap close on corpus underpowering). C alone is appropriate only if owner accepts that MW-25/40/45 stay wrong (C addresses MW-17/47 specifically).

## What does NOT happen at this gate

- No 12.5+1 dispatch until owner picks
- No model promotion at median 32 without owner explicit APPROVE
- v9-3way-v2.2 stays canonical until promotion happens

## On owner decision

| Owner picks | Next orchestrator action |
|---|---|
| A | "12.5-ship at 32/40" directive; QC + ml-architect re-review the ship-a-regression decision |
| B | "12.5 abandon close-out" directive; Variant 3a annotation; v9-3way-v2.2 stays canonical |
| C | "12.5J feature engineering" directive; new ml-architect design pass for E-FEATURE features beyond 59-surface; multi-week Direction X retro |
| D | "12.5I corpus expansion to 30-40 hands/template" directive; ml-architect-hat amends 12.5H-A design |
| E (recommended) | "12.5I-pre diagnostic investigation" directive; per-hand classification on the 5 stay-wrong; ~$5 + 4-5 days; gates D vs C decision |
| Other | Owner-defined; orchestrator authors the matching directive |

## What's blocked / what's queued

**Blocked:**
- All forward dispatch options on owner WHAT decision

**Queued (independent of WHAT pick):**
- TC-X-CROSS-SEED-IMPORTANCE first trainer-report activation (per QC PR #190) — already validated; standing rule
- TC-X-DISPATCH-PREDICTION-VERIFICATION formalized (per QC PR #183) — standing rule
- Cap=4.0 cap-tuning is exhausted as a lever (12.5G empirically refuted)
- Path Y discipline still binds for any of A/B/D options (no source surface edits beyond trainer); only C explicitly violates Path Y boundary

## References

- 12.5H-E re-train: master `283af91` (PR #188)
- 12.5H-E QC verdict: master `8ef358f` (PR #190)
- 12.5H-D APPROVE: master `a554d71` (PR #186)
- 12.5H-C LABELS FINAL: master `690ca8f` (PR #184)
- 12.5H-A design: master `858b032` (PR #165)
- Opus second-tier evaluation: `ORCH_OPUS_125H_F_EVALUATION_2026-05-06.md` (in this PR)
- 12.5E-F precedent (prior synthesis): master `16351e1` (PR #155)
- ml-architect 12.5D' Q4 prediction: `/tmp/ml_architect_125d_prime_findings.md`
- gto-expert 12.5D' per-hand classification: `/tmp/gto_expert_125d_prime_findings.md`
- 12.5C blueprint (trainer module): master `1e4e47e` (PR #122)
- Memory: `feedback_quality_default_no_ask.md` (slow-quality), `feedback_pilot_first_for_long_jobs.md` (E is the pilot for D/C), `feedback_orchestrator_decides_not_recommends.md` (HOW only on per-direction)

**Status: 12.5H-F SYNTHESIS COMPLETE. Owner gate ready: A / B / C / D / E. Orchestrator structural read: E (diagnostic 12.5I-pre) as slow-quality path; D as fallback; C addresses MW-17/47 only; A weakest; B is owner-scope clean close-out.**
