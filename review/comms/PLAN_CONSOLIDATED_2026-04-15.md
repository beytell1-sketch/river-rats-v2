---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Owner + Builder
re: Single consolidated plan forward — supersedes updates-d, -e, and #3
status: PLAN — active
supersedes: MAIN_TERMINAL_UPDATE_2026-04-15-d.md, MAIN_TERMINAL_UPDATE_2026-04-15-e.md, MAIN_TERMINAL_UPDATE_3_2026-04-15.md (trainer/eval scope)
---

# Consolidated Plan — Post ANOMALY-A Resolution

Two concurrent main-terminal threads converged on the same
conclusion. This document is the single source of truth for
what happens next. Anywhere earlier updates disagree, this
plan wins.

---

## 1. Verdict summary — what is and isn't true

### Resolved
- **ANOMALY-A is not a corruption.** Recovered trainer uses
  path 3 (explicit `CAT_MAPS` with float-fallback). The 185
  string rows were encoded correctly during v2.2 training.
- **v2.2 model is sound.** Training saw clean encoded data.
  No retrain needed for ANOMALY-A reasons.
- **MW 80% / FB-40 72.5% are real.** Not artifacts of
  encoding or harness bugs.
- **Bucket-first CHECK bias is the real diagnosis.** No
  need to fork Track 4 on path-2 vs path-5 scenarios.

### Still true
- Encoding inconsistency in `v2_2_training.csv` is real.
  Fix 1 to BP generators is correct as upstream defence —
  v2.3 regeneration produces clean data from source.
- Pre-flight schema gate is correct as belt-and-braces.
- Gate 7 (ship/iterate) still blocked on owner solver on
  the 10 MW misses.
- v2.3 hand generation still blocked on Track 6 + owner
  approval of corrected scope.

### Process gap being closed
- No more inline `python3 <<'EOF'` heredoc training. Every
  model-producing script lives in `river-rats-core/` with
  provenance docstring. CLAUDE.md §6 addendum (see §5.1).

---

## 2. Immediate work — builder executes in parallel

### Stream A — Port recovered scripts to `river-rats-core/`

**A.1** Port `review/recovered/train_v2_2_MODEL.py` →
`river-rats-core/train_model_v2_2.py`

- Provenance docstring pointing at commit `4b08805` and the
  original session transcript path.
- Same encoding logic (`CAT_MAPS` + float-first-then-map
  fallback) — this matches what trained the current model.
- Configurable I/O: input CSV path (default
  `training-data/v2_2_training.csv`), output model path
  (default `river-rats-core/models/v2_2_model_port.json`).
  **Do NOT overwrite `v2_2_model.json`** until A.3
  reproduction confirmed.
- Integrate `_preflight_schema_check()` from
  `train_model.py` — fails fast on mixed-encoding CSV by
  default. Provide `--allow-mixed-encoding` flag for
  reproducing v2.2 on the current (still-mixed) CSV. v2.3
  training runs without the flag.
- Replace `print()` spam with `logging`. Test-first.

**A.2** Port `review/recovered/eval_MW_test_set_50.py`
+ `eval_MW_with_legal_action_masking.py` + FB-40 evaluators
→ `river-rats-core/evaluate_v2_2.py`

- 108-feature inference: 54 raw via `extract_all_features`
  + 54 `attn_*=1`.
- Legal-action masking: `facing_bet=False`→{CHECK,BET};
  `facing_bet=True`→{CALL,RAISE,FOLD}.
- Reuses Track 1 completeness guard + Track 2 dtype guard.
- Entry points `evaluate_fb40()`, `evaluate_mw50()`, plus
  per-hand-detail mode.
- Test-first.

**A.3** Validation — reproduce v2.2 numbers

- Run ported evaluator against the existing `v2_2_model.json`.
- **Must produce:** FB-40 = 72.5% (29/40), MW-50 = 80.0%
  (40/50) with d2920-in / d4534-out.
- If either differs: STOP and report. Do not proceed.
- If both match: Track 2 formally closes.

**A.4** Keep `review/recovered/` as historical reference.
Do NOT delete. Do NOT execute from there.

**Deliverables:** code + `review/comms/V22_TRAINER_PORT_2026-04-15.md`
with reproduction numbers + ANOMALY-A = path 3 confirmation.

### Stream B — Track 4 MW bias deep-dive (parallel with Stream A)

**B.1 Programmer call** — evidence pack

For each of the 10 MW misses (already extracted in
`MW_MISSES_FEATURES_PREP_2026-04-15.jsonl`), assemble:
- Action history pre-flop → current street
- Hero cards + board cards
- Full 54-feature vector
- Corrected bias signature values (HRP, equity_vs_range,
  villain_air_pct, villain_top_pair_plus_pct, SPR,
  better_hand_pct, worse_hand_pct)
- Oracle's predicted action distribution over
  {FOLD, CHECK, CALL, BET, RAISE}
- Pass 1 labelling history if available

Deliverable:
`review/comms/MW_MISS_EVIDENCE_PACK_2026-04-15.md`

**B.2 GTO Expert call** — poker analysis

Reads B.1 pack only. Answers the four questions from the
parallel-tracks directive:
1. Trap bias — top-of-range hands the model wants to
   slowplay?
2. Defensive bias — CHECK preferred when both hero and
   villain ranges strong?
3. Label/model alignment — would Pass 1 labellers have
   voted CHECK here too? (i.e., is this upstream label
   conservatism vs. model-only bias?)
4. Pattern — dominant board texture / position / sandwich
   shape across the 10?

Also: fix-direction recommendation — prompt change,
training-data change, or both.

Deliverable:
`review/comms/MW_MISS_BIAS_ANALYSIS_2026-04-15.md`

### Stream ordering

- A and B run in parallel. A is one programmer; B is one
  programmer (B.1) feeding one GTO expert (B.2).
- A.3 validation must complete before any retrain work
  (see §4).
- B.2 must complete before Track 6 (§3).

---

## 3. Track 6 — v2.3 scope corrections (starts when B.2 lands)

Architect applies the three Track A amendments to
`PLAN_V23_SCOPE_2026-04-15.md`:

1. **BET delta reconciliation** — allocation table (+166)
   vs narrative (+155 + 31 protection). Pick one accounting,
   make consistent.
2. **Section 2 bias signature** — drop `hrp=0.00` claim,
   replace with HRP-investigation corrected signature +
   whatever Track 4 adds/refines from B.2.
3. **Explicit calibration gate** — 23/28 minimum + all
   reversal hands correct before any v2.3 production
   labelling.

Also apply Track E amendments to
`PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md`:

1. Absolute accuracy floor on Groups A+B (e.g. 70%+).
2. Group D regression fallback — if v2.3 regresses by >1
   hand on reversal accuracy, investigate before ship.

Deliverable: updated scope docs in-place, commit message
referencing the amendments.

---

## 4. Clean-CSV retrain — optional, deferred

This is NOT urgent and is NOT on the critical path.

When it runs (separate directive, after A.3 and B.2 both
lands):

1. Recover or rewrite the v2.2 CSV assembly script.
2. Regenerate `v2_2_training.csv` from clean BP JSONLs
   (post-Fix-1) + d-series JSONLs. Pre-flight gate must
   pass without `--allow-mixed-encoding`.
3. Run ported `train_model_v2_2.py` on the clean CSV.
4. Compare: CV 93.0% ± 3.5%, holdout 88.3%, FB-40 72.5%,
   MW-50 80.0%.

Expected under ANOMALY-A = path 3: numbers reproduce within
noise. Divergence would be a finding — stop and report
before overwriting the current model.

---

## 5. Process fixes

### 5.1 CLAUDE.md addendum — training provenance

Add to CLAUDE.md §6 (river-rats-core/ is sacred):

> Every model-producing script (trainer, evaluator) must
> live in `river-rats-core/` with a provenance docstring
> linking its commit to the model artifact it produced.
> Inline `python3 <<'EOF'` heredoc training is prohibited.
> If an experimental run produces a keeper model, commit
> the script that produced it before committing the model.

Builder adds this as part of Stream A.

### 5.2 Pre-flight gate as default

`_preflight_schema_check()` runs by default in all future
trainers. Opt-out only via explicit flag for reproducing
legacy mixed-CSV runs.

---

## 6. Blockers + owner items

| Item | Owner? | State |
|---|---|---|
| Solver on 10 MW misses | yes | pending |
| Gate 7 ship/iterate | yes | pending solver |
| v2.3 scope approval post-amendments | yes | pending Track 6 |
| Everything else | no | flows through builder + main terminal |

Nothing else is waiting on owner.

---

## 7. Deliverables map

| # | File | Stream | Gates |
|---|---|---|---|
| A.1 | `river-rats-core/train_model_v2_2.py` | A | — |
| A.2 | `river-rats-core/evaluate_v2_2.py` | A | — |
| A.3 | `review/comms/V22_TRAINER_PORT_2026-04-15.md` | A | closes Track 2 |
| B.1 | `review/comms/MW_MISS_EVIDENCE_PACK_2026-04-15.md` | B | — |
| B.2 | `review/comms/MW_MISS_BIAS_ANALYSIS_2026-04-15.md` | B | unblocks Track 6 |
| T6 | updated scope docs + commit | Track 6 | unblocks v2.3 gen |
| CM | CLAUDE.md §6 addendum | 5.1 | — |

Commit + push each deliverable separately.

---

## 8. Stop conditions (unchanged)

- A.3 numbers don't match 72.5% / 80.0% → STOP, report.
- B.2 GTO analysis finds the bias is NOT bucket-first-CHECK
  → STOP, review before Track 6 applies the signature.
- Retrain on clean CSV diverges materially from current
  numbers → STOP, investigate before swapping model.
- Any test harness error on previously-green path → STOP.

---

## 9. What is explicitly NOT in scope right now

- v2.2 ship (owner + Gate 7)
- v2.3 hand generation (blocked on Track 6 + owner)
- v3.0 action distributions (post-v2.2 backlog)
- Teaching repo work (separate track, unblocked by prior
  handoff)
- Retraining v2.2 on clean CSV (§4, deferred)
- 11 preexisting test failures (`test_oracle_router` missing
  `gto_model_v8_hu.json` etc.) — separate cleanup track
