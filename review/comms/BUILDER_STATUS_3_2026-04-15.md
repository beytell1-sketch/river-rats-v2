---
date: 2026-04-15
from: Builder
to: Main terminal / Owner
re: Round 3 status — Stream A shipped with A.3 STOP, Stream B complete, Track 6 unblocked
status: AWAITING DIRECTION on MW-50 canonical number; Track 6 ready to launch
---

# Builder Status #3

Six commits landed this round.

| Commit | Stream | Result |
|---|---|---|
| `cb444ef` | A.1 trainer port | ✅ done |
| `d2287e8` | A.2 evaluator port | ✅ done |
| `2fd63c5` | A.3 validation | ⚠️ **STOP — MW-50 = 84% vs target 80%** |
| `a606c7e` | CLAUDE.md addendum | ✅ done |
| `3b69360` | B.1 evidence pack | ✅ done |
| `747f638` | B.2 GTO bias analysis | ✅ done |

## Stream A — A.3 STOP detail

- **FB-40: 72.5% (29/40) — matches target exactly.**
- **MW-50: 84.0% (42/50)** vs target 80.0% (40/50). `d4534_BTN_river`
  is IN (correct) where the target says OUT.

**Root cause hypothesis:** the recovered
`eval_MW_with_legal_action_masking.py` retrains its own model
in-script (`n_estimators=95`, no early stopping) and reports against
that fresh model — producing 80%. The committed `v2_2_model.json` was
produced by Phase-4 training (`n_estimators=800` + `early_stopping=50`)
and scores 84% on MW-50. Two different models. FB-40 is invariant
between them.

**Implication:** the live model is BETTER than reported. The 4-hand
gap is between two model artifacts, not between model and reality.

**Three options for owner adjudication** (per
`V22_TRAINER_PORT_2026-04-15.md` §4):
1. Accept 84% as the corrected canonical MW-50 number for the live
   model; note 80% was an artifact of the recovered eval's
   self-trained shadow.
2. Re-verify by running the recovered eval as-is (will self-train and
   should reproduce 80%).
3. Investigate further (feature drift, schema change between
   training and eval).

Builder recommends 1 + 2 in sequence.

ANOMALY-A path-3 confirmed via passing encoding tests on the ported
trainer.

CLAUDE.md §6 addendum committed (no heredoc training, model-producing
scripts in `river-rats-core/` with provenance).

## Stream B.2 — GTO verdict (commit `747f638`)

**Dominant bias: Defensive multiway-checked-through CHECK bias** —
not a pure trap-lean.

- 10/10 misses share `facing_bet=False ∧ num_opponents=2 ∧ SPR≈1.25`
- 7/10 also have `villain_checked_back=1 ∧ villain_range_capped=1`
- Model reads mutual passivity + villain_TP+ density as range-vs-range
  standoff → defaults to pot control, overriding the value+protection
  case that the capped/weak villain line actually enables
- HRP varies 0.43–0.83, so trap-lean contributes (AA, QQ two-pair,
  TPGK) but is **subordinate**

**Label/model alignment: predominantly model-only.** Aggregated Pass 1
reasoning engages the CHECK alternative and rejects it on explicit
override grounds (villain_checked_back + capped + high
worse_hand_pct → BET). d3688 is the confirming case: labellers
correctly declined the override when villain was uncapped (HJ opened);
model failed to make that distinction.

**Fix-direction (both, training-data primary):**
- **Primary:** v2.3 supplement of 400–800 hands in bucket
  `facing_bet=F ∧ num_opponents≥2 ∧ villain_checked_back=1 ∧
  villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧ equity_vs_range≥0.35
  ∧ SPR≤2.0` labelled BET.
- **Secondary:** add the override clause to Pass 1 prompt to reduce
  panel variance.

**Track 6 Section 2 wording (recommended):** Replace "bucket-first
CHECK bias" with **"Defensive multiway-checked-through CHECK bias"**
and pin the preconditions (villain checked back, capped,
worse_hand_pct ≥ 0.55, low SPR). A uniform "bet more" correction would
overshoot into spots where villain did not check back.

GTO Expert noted: stop conditions did not fire — bias IS
bucket-first-CHECK in the narrow conditional sense; Track 6 proceeds
with refined wording. Requested follow-ups (not blocking): per-agent
d* Pass 1 votes if persisted, label-distribution spot-check on the
bias-signature bucket.

## Track 6 — READY TO LAUNCH

B.2 has shipped. Architect can now apply the 3 Track A amendments +
2 Track E amendments per consolidated plan §3. Holding for owner
go-ahead OR will proceed in next round if no objection.

## Updated track grid

| Track | Status | Notes |
|---|---|---|
| 1 Harness hardening | ✅ done | b5d84b5 |
| 2 FB/MW re-eval | ⚠️ STOP — owner adjudication | A.3 surfaced model artifact mismatch |
| 3 Training audit | ✅ done | 8e77e05 |
| 3.5 ANOMALY-A | ✅ resolved (path 3 confirmed) | port encoding tests pass |
| 4 MW bias deep-dive | ✅ done | B.1 + B.2 shipped |
| 5 BP generator fix | ✅ done | b69e668 + Fix 1 |
| 6 Scope corrections | 🟡 ready to launch | unblocked by B.2 |
| Stream A.1/A.2/A.4 | ✅ done | trainer + eval + recovered preserved |
| CLAUDE.md addendum | ✅ done | a606c7e |

## Awaiting

1. Owner ruling on MW-50 canonical number (80% recovered shadow vs
   84% live model)
2. Owner go-ahead to launch Track 6 (or proceed without explicit
   approval per protocol)
3. Anything else surfacing in `MAIN_TERMINAL_UPDATE_*` or
   `PLAN_CONSOLIDATED_*`

Standing by.
