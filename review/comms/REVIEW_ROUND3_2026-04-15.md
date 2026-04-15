---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Owner + Builder
re: Round 3 review — Stream A STOP adjudicated, Stream B accepted, Gate 7 reframed
status: REVIEW — decisions inline; see MAIN_TERMINAL_UPDATE_2026-04-15-f.md for directive
---

# Round 3 Review

## 1. Stream A — decision on the 80% vs 84% divergence

**Canonical MW-50 number on the live model is 84.0% (42/50).**

Root cause confirmed: the recovered
`eval_MW_with_legal_action_masking.py` trains its own shadow model
in-script (`n_estimators=95`, no early stopping) and evaluates that
freshly-fit model — producing 80.0%. The live `v2_2_model.json`
(produced by the recovered heredoc trainer with `n_estimators=800 +
early_stopping_rounds=50`, settling on best iteration 95) scores
84.0% when evaluated via the ported `river-rats-core/evaluate_v2_2.py`.
FB-40 is invariant between the two at 72.5% — coincidence of that
set, not evidence of no divergence elsewhere.

These are two different models. The one that ships is the committed
`v2_2_model.json`. Therefore:

- **MW-50 canonical: 84.0% (42/50).** Live model.
- **MW-50 shadow: 80.0% (40/50).** Historical measurement from the
  recovered-eval self-trained model. Forensic reference only.
- **FB-40: 72.5% (29/40).** Unchanged.

### Gate 7 implication

The MW-50 target was 82.5%. The live model is 84.0% — clears the
target by +1.5pp. The framing that drove ANOMALY-A, the solver-time
ask, and the six parallel tracks ("model missed MW-50 by 2.5pp") was
measuring the shadow, not the shipped model. On the shipped model,
MW-50 is a PASS.

Gate 7 decision (ship/iterate) is therefore materially different:
no gate is failing. Solver verification on the remaining MW misses
(now ~8 hands, not 10) is still valuable for understanding the
defensive-multiway-checked-through bias before v2.3, but it is no
longer unblocking — the numeric case for shipping v2.2 is intact.

### Track 2 closure

With the 84% number adopted as canonical, **Track 2 closes** on the
ported evaluator + provenance. Builder should note in
`V22_TRAINER_PORT_2026-04-15.md` that the original report number
(80%) corresponds to a shadow model that is now preserved in
`review/recovered/` for reference and is not the shipped reference.

### Forensic verification (low priority, non-blocking)

Run the recovered `eval_MW_with_legal_action_masking.py` as-is from
`review/recovered/` and confirm it reproduces 80.0% with the d4534-OUT
hand swap. If yes, the shadow-model finding is fully corroborated and
the investigation closes cleanly. If no, something else differs and
we revisit. Single programmer call, ~30 min.

## 2. Stream B — accepted; diagnosis reframed

The MW_MISS_BIAS_ANALYSIS is strong work. Key findings:

- **Dominant bias: defensive (range-vs-range) CHECK preference in
  multiway checked-through spots.** Not generic passivity.
- **Trap-lean is a secondary compounding factor**, not the primary
  mechanism — HRP varies 0.43–0.83 across misses, so "slowplays
  monsters" doesn't cover it.
- **Bias is predominantly model-only**, not label conservatism —
  Pass 1 reasoning correctly engaged the override clause; the model
  failed to learn the conditional structure.
- **Precondition signature pins the bucket tightly**:
  `facing_bet=False ∧ num_opponents≥2 ∧ villain_checked_back=1 ∧
   villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧
   equity_vs_range≥0.35 ∧ SPR≤2.0`

### Fix direction — accepted

- **Primary: v2.3 training supplement**, 400–800 hands in the
  precondition bucket labelled BET with position/texture stratification.
- **Secondary: Pass 1 prompt reword** with an explicit override
  clause reducing panel variance on boundary spots.
- Both, not either-or. Compounds the signal.

### Track 6 Section 2 wording — adopted

Track 6 uses the proposed wording:

> **Defensive multiway-checked-through CHECK bias.** The v2.2 model
> underbets in multiway pots where villain(s) have checked the
> previous street, villain ranges are capped, hero sits at or above
> median range strength with worse_hand_pct ≥ 0.55, and SPR is low
> (≤ 2). The model reads mutual passivity plus villain_top_pair_plus
> density as range-vs-range standoff and defaults to pot-control
> CHECK, overriding the value+protection case that the passive
> villain line actually enables. The v2.3 supplement should target
> this bucket specifically; a uniform "bet more often" correction
> would overshoot.

This replaces "bucket-first CHECK bias" across v2.3 scope docs.

### Stop-condition disclosures — addressed

Stream B.2 flagged three follow-ups. All authorised, none blocking
Track 6:

1. **Per-agent Pass 1 votes for d* sids** — not in repo. Confirm
   they were not persisted; if they exist anywhere on owner's
   machine, surface them. Otherwise accept the aggregated-reasoning
   analysis as sufficient.
2. **Training CSV label-distribution spot-check** for the bias
   signature bucket — authorised as Stream C (§3 of directive).
   Informs v2.3 supplement sizing: if > 30% CHECK in training
   bucket, label conservatism compounds and supplement target
   rises toward 800; if ≤ 30%, 400 is adequate.
3. **SPR=1.25 on 10/10** — test-set construction artifact is
   plausible; de-prioritise for now, revisit during v2.3 test-set
   design (Track E).

## 3. Round 3 track grid

| Track | Status |
|---|---|
| 1 Harness hardening | ✅ done |
| 3 Training audit | ✅ done |
| 3.5 ANOMALY-A | ✅ resolved — path 3 confirmed |
| 5 BP generator fix | ✅ done (Fix 1 applied) |
| Batch2 disposition | ✅ out of scope |
| 2 FB-40 / MW-50 re-eval | ✅ **closed — canonical numbers 72.5% / 84.0%** |
| 4 MW bias deep-dive | ✅ done — defensive-multiway-checked-through diagnosis |
| 4 prep | ✅ done |
| A.1 trainer port | ✅ done |
| A.2 evaluator port | ✅ done |
| A.3 validation | ✅ closed via canonical-number decision |
| A.4 recovered preserved | ✅ done |
| CLAUDE.md provenance addendum | ✅ done |
| 6 Scope corrections | 🟢 **launched** (see directive) |
| Stream C: training label spot-check | 🟢 **launched** (see directive) |
| Forensic verification (shadow eval) | 🟢 launched — low priority |

## 4. Gate 7 status — reframed

| Criterion | Target | Actual (live model) | Status |
|---|---|---|---|
| FB-40 | ≥ 70.0% | 72.5% | PASS |
| MW-50 | ≥ 82.5% | 84.0% | **PASS** |

Numeric criteria are satisfied. The solver verification on the
remaining MW misses (now ~8 hands after the d4534-IN correction)
is **not a gate** — it's useful context for v2.3 bias-fix sizing
and a general confidence check. Owner call whether to run it
before ship, run it as post-ship diligence, or skip.

Builder is not blocked by Gate 7 either way — v2.3 work is
independent.

## 5. What the owner still owns

Narrower than before:
- Solver verification on remaining MW misses (no longer gating;
  owner call on sequencing)
- Gate 7 ship/iterate (criterion-pass clears the numeric case;
  owner call on qualitative factors)
- Final v2.3 scope approval after Track 6 lands

Everything else runs.
