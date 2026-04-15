---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Builder
re: ANOMALY-A resolved via recovered trainer — port task + unblock Track 4
status: DIRECTIVE — supersedes update-d trainer-rewrite scope where noted
---

# Main Terminal Update — 2026-04-15 (e)

Owner recovered the v2.2 scripts into `review/recovered/`
(commit `4b08805`). This resolves ANOMALY-A and reshapes the
trainer work.

## 1. ANOMALY-A verdict — RESOLVED (path 3, no corruption)

`review/recovered/train_v2_2_MODEL.py` contains the actual
encoding logic used for v2.2 training:

```python
CAT_MAPS = {
    'street': {'flop':0,'turn':1,'river':2,'':0},
    'hero_position': {'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
    'villain_position': {...},
}
def encode(row, col):
    if col in CAT_MAPS:
        try: return float(val)
        except: return float(CAT_MAPS[col].get(val, 0))
    return to_float(row[col])
```

This is **path 3 (explicit mapping with fallback)** from the
ANOMALY_A loader-path table. Numeric rows pass through
`float()`; string rows fall through to CAT_MAPS and get
encoded correctly (`flop→0, turn→1, river→2`;
`UTG→0, HJ→1, CO→2, BTN→3, SB→4, BB→5`).

**The 185 BP-series rows were encoded correctly during
training.** No corruption occurred. v2.2 training data was
effectively clean.

Consequences:
- The MW 80% / bucket-first CHECK bias is **real model
  behaviour**, not street-confusion artifact.
- Gate 7 reasoning is not undermined by ANOMALY-A.
- Track 4 (MW bias deep-dive) can proceed with full
  confidence that the model saw correct features.
- The ANOMALY-A cleanup work (Fix 1 to BP generators, schema
  pre-flight gate) is still correct as defence-in-depth — the
  next trainer shouldn't rely on CAT_MAPS fallbacks; the CSV
  should be numeric by construction.

Note this verdict in `V22_TRAINER_RECOVERY_2026-04-15.md`
when you write it.

## 2. Trainer/eval work — port, don't rewrite

Scope reduces from "rewrite from scratch" to "port recovered
scripts into `river-rats-core/` with discipline improvements."

### 2.1 `river-rats-core/train_model_v2_2.py`

Port of `review/recovered/train_v2_2_MODEL.py` with:

- Top-level docstring referencing the recovered source +
  commit `4b08805` as provenance
- Configurable input CSV path (default
  `training-data/v2_2_training.csv`) and output model path
  (default `river-rats-core/models/v2_2_model_port.json` —
  do NOT overwrite the current `v2_2_model.json` until §3
  confirms reproduction)
- Calls `_preflight_schema_check()` from `train_model.py`
  before fitting — if the input CSV has mixed encoding, fail
  fast. With Fix 1 applied to BP generators, any v2.3
  regeneration will be clean; the current
  `v2_2_training.csv` is still mixed, so the port will
  correctly refuse to run on it until §4.
- Keep CAT_MAPS path for backwards-compatibility with the
  current mixed CSV IF the preflight gate is bypassed via an
  explicit `--allow-mixed-encoding` flag (for reproduction
  verification only). Without the flag, mixed CSV is
  rejected.
- Cleaner structure than the heredoc original — test-first,
  functions separated, no `print()` spam (use `logging`).

### 2.2 `river-rats-core/evaluate_v2_2.py` (new module)

Port of `review/recovered/eval_MW_test_set_50.py` +
`eval_MW_with_legal_action_masking.py` + relevant parts of
the FB-40 evaluators. Contains:

- 108-feature extraction: 54 raw via `extract_all_features`,
  54 `attn_*=1` concat
- Legal-action masking: `facing_bet=False` → {CHECK, BET};
  `facing_bet=True` → {CALL, RAISE, FOLD}
- Reuses Track 1 completeness guard + Track 2 dtype guard
- Entry points: `evaluate_fb40()`, `evaluate_mw50()`,
  per-hand detail mode
- Tests covering both entry points against the current
  `v2_2_model.json`

## 3. Validation

Run the ported eval module against the **existing**
`v2_2_model.json`:

- FB-40 must produce 72.5% (29/40)
- MW-50 must produce 80.0% (40/50) with d2920-in / d4534-out

If either differs, STOP and report. Do not proceed to retrain.

Once both numbers match, §2 port is validated and Track 2 is
formally closed (validation numbers go in
`V22_TRAINER_RECOVERY_2026-04-15.md`).

## 4. Retrain — still gated on clean CSV

Clean-CSV retraining is a **separate follow-up**. Do NOT do
it as part of this port. Steps (for a later directive):

1. Recover or rewrite the v2.2 CSV assembly script
2. Regenerate `v2_2_training.csv` from the now-clean BP
   JSONLs (post Fix 1) plus d-series JSONLs
3. Run the ported `train_model_v2_2.py` on the clean CSV
4. Compare numbers against the current model — if within
   tolerance, swap. If different, investigate.

Note: under the ANOMALY-A = path 3 finding, the clean-CSV
retrain should reproduce essentially the same numbers.
Divergence would be unexpected and itself a finding.

## 5. Track 4 — UNBLOCKED, launch now

Per §1, Track 4 no longer needs trainer recovery to proceed.
MW-miss feature data is already extracted (commit `6501cbb`).

**Launch Track 4 (MW bias deep-dive) in parallel with the
port work.** Two calls:

1. **Programmer call** — produce per-hand evidence pack for
   the GTO Expert: for each of the 10 MW-miss hands,
   concatenate action history + hero/villain cards + board +
   full 54-feature vector + corrected bias signature
   (HRP avg 0.64 vs 0.44 on misses) + oracle's predicted
   action distribution. Save to
   `review/comms/MW_MISS_EVIDENCE_PACK_2026-04-15.md`.

2. **GTO Expert call** — analyse the 10 misses per the
   directive's four questions (trap bias / defensive bias /
   label-model alignment / pattern across the 10).
   Deliverable `review/comms/MW_MISS_BIAS_ANALYSIS_2026-04-15.md`.

## 6. Recovered file hygiene

The five files in `review/recovered/` are provenance
references only. Do NOT execute them from that location; do
NOT modify them. They exist so future audits can see exactly
what produced the v2.2 model.

## 7. Tracks 2 and 6

- Track 2: closes when §3 validation numbers land.
- Track 6: remains held on Track 4. Becomes unblocked when
  the GTO Expert deliverable lands.

## 8. Order of execution

Parallel tracks:
- Port trainer + eval (§2) → validation (§3) → commit
- Track 4 prog call (§5.1) → GTO call (§5.2) → commit

Commit and push each deliverable separately.
