---
date: 2026-05-04
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream · GTO-EXPERT · ML-ARCHITECT
re: Phase 12.5D' tie-gate (31/40 = 12.5D) — two-expert synthesis; owner WHAT decision (Ship / Cap / Abandon / Data-fix)
status: SYNTHESIS — owner gate
---

# Phase 12.5D' — two-expert synthesis on the tie-gate

LEAD-PROGRAMMER PR #131 BLOCKED at owner-tie-gate (median seed solver-corrected = 31/40 = 12.5D, per-seed identical). Hybrid weighting fixed held-out class collapse exactly as ml-architect Q3 predicted at the loss-function level. **It did NOT transfer to the reference set.** gto-expert's prediction (7-of-7 shared-cause flips) is empirically refuted: 1-of-7 flipped (MW-24).

Both experts dispatched via subagent (per `feedback_qc_routing_when_standalone_active.md` — applies to QC only; gto-expert + ml-architect do not have standalone streams documented). Standalone QC pre-merge audit on PR #131 in flight separately.

## What the two empirical runs (12.5D + 12.5D') jointly demonstrate

| Quantity | 12.5D | 12.5D' | Δ |
|---|---|---|---|
| Per-seed solver-corrected | [31, 30, 30, 31, 31] | [31, 30, 30, 31, 31] | **0 across all seeds** |
| Median solver-corrected | 31/40 | 31/40 | 0 |
| Held-out BET recall | 0.824 | 1.000 | +0.176 |
| Held-out RAISE recall | 0.500 | 0.667 | +0.167 |
| `nut_flush_block` importance | 0.0000 | 0.0000 | 0 (still never split on) |
| MW-45/47 RAISE flip | wrong | wrong | not flipped |
| MW-25/40/42 BET flip | wrong | wrong | not flipped |

**Held-out gates and reference-set gates measure different things on this corpus.** Hybrid weighting closes the in-distribution class collapse cleanly; it does not transfer to the structurally out-of-distribution reference-set RAISE/bluff failures.

## Convergence across two experts (and now two empirical runs)

### gto-expert (revised)

- **Q1-revised:** E-DIST dominates with smaller E-FEATURE sub-component. Per hand:
  - MW-25 (Ks7s monotone-spade FD checked-through 4-way), MW-40 (TP-T-kicker 4-way after PFR check), MW-45 (slowplayed set into turn lead 4-way): **E-DIST primary** — composition signal exists, corpus lacks training analogues for these action patterns
  - MW-42 (river thin-value-bet TPTK after multi-street action), MW-17 (NFD+overcards under pot odds, needs implied/blocker reasoning): **E-FEATURE primary** — action-sequence narrowing or implied-odds-with-blocker not in 59-feature surface
  - MW-47 (NFD+gutshot semi-bluff RAISE OOP): **E-DIST + E-FEATURE compound**
- **Q2-revised:** **H2 twice-confirmed.** Hybrid weighting boosted RAISE class weight (the exact direction that should reward discovering nut-FD blockers); booster found other gradient paths instead. `nut_flush_block` importance remained 0.0000.
- **Honest probability of close-the-gap per direction:**
  - A (Ship the tie): **0%** for the gap itself
  - B (Cap retuning 2.0/2.5/4.0): **~10-15%**
  - C (Abandon migration): **0%** on v9-student; preserves baseline 33/40
  - D (Data-side fix): **~50-70%** — only direction addressing E-DIST root cause; multi-week scope

### ml-architect (revised)

- **Q3 transfer assumption refuted, owned.** Loss-function math worked; assumption that this propagates to reference set was the broken link. Asserting transfer without verifying held-out fold's structural similarity to MW-11..MW-50 was the methodological error.
- **Q4 verdict:** **H-FEAT primary (~70%) + H-DIST secondary (~30%); H-TREE rejected (~0%).**
  - **Specific structural finding** (corpus inspection): cohort 1 has 1 RAISE total; cohort 2's 28 RAISE rows concentrate in `monster_*` (10/10) and `nfd_*` (16/48). Booster learned "RAISE when monster-pattern OR nfd-pattern fires" — strengthens under hybrid weighting (held-out gain) — but MW-45/47 are situation-specific GTO RAISE spots not matching either pattern.
  - xgboost with 287-663 actual rounds at depth 5 has ample capacity — **signal-limited, not capacity-limited.**
- **Q5 cap retuning prior: ~5%.** Cap is orthogonal to H-FEAT failure mode. Cap controls amplification of learned patterns; cannot change which patterns are learned. cap=4.0 risks over-firing MW-31-style situations without flipping MW-45/47.
- **Highest-probability gap-closer methodology-wise: Direction D (data-side).** Predicted blocker importance 0.0000 → 0.02-0.05; predicted target median 35-37.

### Cross-expert agreement

Both experts independently agree:
1. Migration's premise (P1 blockers as load-bearing) is **empirically refuted twice** (12.5D + 12.5D')
2. Cap retuning will not close the gap (orthogonal to root cause)
3. Direction D is the only direction that addresses the root cause with non-trivial probability of success
4. Ship-the-tie ships a regression with no evidence of production-side benefit

## Owner WHAT decision space (Ship / Cap / Abandon / Data-fix)

Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator presents options; owner decides WHAT.

### Direction Ship — promote v9-student at 31/40 on held-out gain
- **Implementation:** ~1 builder day; promote to `gto_model_v9_student.json`; update model card with documented regression; v9-3way-v2.2 stays as fallback
- **Pros:** ships the migration; uses the work; held-out gains are real for inference distributions that resemble the corpus
- **Cons:** ships a measurable regression vs baseline on the canonical reference set; **gto-expert + ml-architect both implicitly reject**; both runs (12.5D + 12.5D') refute that this model is gate-passing
- **Structural read:** weakest direction; not recommended

### Direction Cap — retune the cap (2.0 / 2.5 / 4.0)
- **Implementation:** ~1 builder day for 3-point sweep
- **Pros:** completes the cap-orthogonality empirical test; produces 1 more data point
- **Cons:** ml-architect estimates ~5% probability of helping; cap controls amplification, not which patterns are learned; expected outcome is "confirms orthogonality, no gap close"
- **Structural read:** information-value direction without expected-value direction; useful only if owner wants the cap-orthogonality conclusion in writing for posterity

### Direction Abandon — close out the migration; v9-3way-v2.2 stays canonical
- **Implementation (ml-architect Variant 3a, preferred):** keep trainer + tests + features as research artefact with abandoned-banner; ~10 line PR. Variant 3b (full revert) destroys negative evidence.
- **Pros:** preserves negative-result trail; closes out cleanly; queues team to next initiative; baseline is unchanged
- **Cons:** the 12.5C-D-D' arc produced no shipped model upgrade; "we tried 55→59 with hybrid weighting; it didn't deliver on this corpus + reference set" is the lesson on record
- **Structural read:** clean close-out path; cheapest forward move; harvests methodology lessons (held-out vs reference-set decoupling; pre-flight protocol amendment from 12.5D' dispatch)

### Direction Data-fix — rebuild corpus with reference-set-style situations
- **Implementation (ml-architect spec):** ~100 new hands sourced from solver databases targeting the 7 shared-cause failure templates (40 BET, 20 RAISE, 10 CALL, 30 control); same labeller pipeline + bucket-first prompt; QC join-cardinality gate per Q1 amendment; 12.5E re-train. Predicted blocker importance 0.0000 → 0.02-0.05; target median 35-37.
- **Cost:** 1-2 weeks corpus + 1 day train
- **Pros:** **only direction with non-trivial probability of closing the reference-set gap.** Both experts converge on this as the structural answer. Acts on H-FEAT/H-DIST root cause directly.
- **Cons:** longest timeline; commits another 1-2 weeks before knowing if the close-the-gap prediction holds
- **Structural read:** highest-EV direction if owner has appetite for the timeline; only direction that uses the diagnostic to its conclusion

## Orchestrator structural read (observation, owner decides)

Per owner's standing instruction "please do your job and recommend next actions": clean reads given the converged evidence —

- **Ship:** structurally rejected (regression, no transfer evidence)
- **Cap:** information-only, ~5% probability of helping; defer or skip
- **Abandon:** clean close-out; preserves baseline; harvests lessons; cheapest forward move
- **Data-fix:** highest-EV; ~50-70% probability of closing the gap per gto-expert; methodology-supported by ml-architect

**If owner has 1-2 weeks of appetite for the rebuild:** Data-fix is the structural answer. Both experts converge.

**If owner does NOT have appetite for the rebuild:** Abandon (Variant 3a) is the cleanest close-out. Preserves the trainer + tests + invariant test on master as a re-runnable research artefact; v9-3way-v2.2 stays canonical for the 33/40 region; the 55→59 migration is documented as "tried, evaluated, didn't deliver on this evaluation set."

**Cap retuning** is the only direction the orchestrator structurally argues against doing FIRST; if owner picks it, frame as "let's confirm orthogonality before deciding between Abandon and Data-fix" — i.e., a 1-day epistemic intermediate, not a standalone direction.

**Ship the tie** is structurally weak enough that orchestrator does not present it as a serious option for an owner who has read the synthesis. Reserved as a fallback if Abandon's "preserve baseline" path is somehow unavailable.

## What does NOT happen at this gate

- **PR #131 holds open** until standalone QC pre-merge audit lands (per dispatch directive + `feedback_qc_routing_when_standalone_active.md`)
- **No 12.5+1 / 12.5E dispatch** until owner picks a direction
- **No source-surface edits** under any direction (Path Y still binds; Variant 3a Abandon is annotation-only)
- **No model promotion** under any direction without owner gate on the regression-vs-baseline trade-off

## Next gates (in order)

1. **Standalone QC pre-merge audit on PR #131** lands (independent; orchestrator does NOT spawn parallel subagent)
2. **Owner WHAT decision** (Ship / Cap / Abandon / Data-fix) — informed by this synthesis
3. **On owner decision:**
   - Ship → orchestrator authors "12.5F regression-promotion" directive; QC + owner ship-gate; promote
   - Cap → orchestrator authors "12.5D'' cap sweep" directive; ~1 builder day; synthesis after
   - Abandon → orchestrator authors "12.5 abandon close-out" directive; Variant 3a annotation; v9-3way-v2.2 stays canonical
   - Data-fix → orchestrator authors "12.5E corpus rebuild" directive; new ml-architect labelling-round design; multi-week scope
4. **Methodology lesson saved to memory** (orchestrator scope): held-out gates ≠ reference-set gates on this corpus; future trainer designs must verify transfer empirically before promotion

## References

- BLOCKED PR #131 (open, branch `programmer/phase125d-prime-hybrid-weighting-2026-05-04`)
- 12.5D' dispatch: PR #130 (master `1b95648`)
- 12.5D synthesis: PR #128 (master `d6dd36d`)
- 12.5D BLOCKED baseline: PR #126 (master `d7d2cdd`)
- Findings (raw, on orchestrator host):
  - `/tmp/gto_expert_125d_prime_findings.md`
  - `/tmp/ml_architect_125d_prime_findings.md`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_qc_routing_when_standalone_active.md` (NEW 2026-05-04), `feedback_quality_default_no_ask.md`

**Status: SYNTHESIS COMPLETE. PR #131 holds open pending standalone QC. Owner gate ready: Ship / Cap / Abandon / Data-fix. Orchestrator structural read: Data-fix if 1-2 weeks appetite; Abandon (Variant 3a) otherwise. Cap as epistemic intermediate only. Ship not seriously presented.**
