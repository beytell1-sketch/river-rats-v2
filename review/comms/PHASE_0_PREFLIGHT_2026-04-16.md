# Phase 0 Preflight — v2.3 Hand Generation

**Date:** 2026-04-16
**Branch:** master @ `4668269`
**Role:** Programmer
**Plan ref:** `review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md` §Phase 0
**Verdict:** **GO** for Phase 1

---

## Checklist

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 0.1 | Test-suite health | **PASS (with expected CSV-only failures)** | 47 passed, 3 failed, 2 skipped across 5 files. All 3 failures are on `v2_2_training.csv` (ANOMALY-A), which is explicitly NOT part of Phase 0 gate. |
| 0.2 | `normalise_situation` round-trip | **PASS** | 10/10 street numeric, 10/10 hero_position numeric, 10/10 idempotent on both batch3 and batch5 JSONL samples. |
| 0.3 | Schema preflight on BP JSONLs | **PASS** | 4/4 present BP JSONLs clean. batch4 absent (never generated; Phase 1 target). |
| 0.4 | Disk check | **PASS** | 769 GB free on `/dev/nvme0n1p2` (required ≥ 2 GB). |
| 0.5 | Git clean | **PASS** | `git status --porcelain` empty. |
| 0.6 | `gto_labeller_v3.md` existence | **ABSENT (expected)** | Only v1 and v2 present in `prompts/`. Phase 3 prerequisite, not Phase 1 blocker. |
| 0.7 | Calibration exam infrastructure | **PASS** | `river-rats-core/calibration_exam.py` exists. Entry point `run_calibration(...)` cited in module docstring; `GTO_REVERSAL_HANDS` defined at line 33. |
| 0.8 | Generator scripts accessible | **PASS** | All 5 generators present under `review/`, each exposes `generate_all()`. |

---

## 0.1 Test counts (per file)

| File | Passed | Failed | Skipped |
|------|--------|--------|---------|
| `test_situation_factory.py` | 9 | 0 | 0 |
| `test_training_data_encoding.py` | 9 | **3** (CSV-only, expected) | 2 |
| `test_train_model_v2_2.py` | 10 | 0 | 0 |
| `test_evaluate_v2_2.py` | 6 | 0 | 0 |
| `test_harness_feature_completeness.py` | 16 | 0 | 0 |
| **Total** | **50** | **3** | **2** |

The 3 failures are:
- `test_training_csv_column_is_numeric[street-training-data/v2_2_training.csv]` — 185 rows `street ∈ {flop, turn, river}`
- `test_training_csv_column_is_numeric[hero_position-training-data/v2_2_training.csv]` — 185 rows `hero_position ∈ {BB, BTN, CO, SB}`
- `test_training_csv_street_has_no_string_literals` — same 185 rows

All three are the known ANOMALY-A on the pre-existing `v2_2_training.csv`. The task brief explicitly calls this out as expected and **not** part of the Phase 0 gate (the `--allow-mixed-encoding` flag exists for exactly this reason; Phase 0 only gates on BP JSONLs).

---

## 0.2 Round-trip results

| JSONL | street numeric (0/1/2) | hero_position numeric (0–5) | idempotent |
|-------|------------------------|------------------------------|------------|
| `factory_batch5_situations.jsonl` | 10/10 | 10/10 | 10/10 |
| `factory_batch3_situations.jsonl` | 10/10 | 10/10 | 10/10 |

Sampled with `random.seed(42)`, 10 records each. `normalise_situation(normalise_situation(x)) == normalise_situation(x)` via `json.loads(json.dumps(...))` equality.

---

## 0.3 Schema preflight per BP JSONL

Ran the body of `train_model._preflight_schema_check` against each BP JSONL:

| JSONL | Result |
|-------|--------|
| `factory_situations.jsonl` | PASS |
| `factory_batch2_situations.jsonl` | PASS |
| `factory_batch3_situations.jsonl` | PASS |
| `factory_batch4_situations.jsonl` | ABSENT (not generated yet — Phase 1 target) |
| `factory_batch5_situations.jsonl` | PASS |

All present BP JSONLs have numeric `street` and `hero_position` throughout. Fix 1 is holding.

---

## 0.4 Disk free

```
/dev/nvme0n1p2   938G used=122G avail=769G (14% used)
```

769 GB available — well above 2 GB minimum.

---

## 0.5 Git status

Clean — `git status --porcelain` produced no output. HEAD at `4668269`.

---

## 0.6 v3 prompt status

`prompts/gto_labeller_v3.md` — **ABSENT (expected)**. `prompts/` contains only `gto_labeller_v1.md` and `gto_labeller_v2.md`. Matches plan expectation: v3 is a Phase 3 prerequisite, created by taking v2 + Scope §3 Additions A/B/C/D verbatim.

---

## 0.7 Calibration exam entry point

`river-rats-core/calibration_exam.py:11` — module docstring:
```
Usage:
    python3 calibration_exam.py
    python3 calibration_exam.py --prompt prompts/gto_labeller_v1.md
```

Key identifiers:
- `GTO_REVERSAL_HANDS = {'MW-30', 'MW-33', 'MW-50'}` — `calibration_exam.py:33`
- Primary entry: `run_calibration(label_fn, prompt_path, knowledge_path)` (per plan §3.1)

Infrastructure confirmed present. Not executed (per read-only constraint).

---

## 0.8 Generator scripts

| Script | Entry point |
|--------|-------------|
| `review/generate_factory_situations.py` | `generate_all()` @ line 616 |
| `review/generate_factory_batch2.py` | `generate_all()` @ line 1212 |
| `review/generate_factory_batch3.py` | `generate_all()` @ line 1349 |
| `review/generate_factory_batch4.py` | `generate_all()` @ line 1537 |
| `review/generate_factory_batch5.py` | `generate_all()` @ line 1914 |

All 5 present. Each also has `main()` + `__main__` guard. Not executed (per read-only constraint).

---

## Overall verdict

**GO for Phase 1.**

All blocking gates pass:
- Test suite clean on Phase-0-relevant modules (ANOMALY-A CSV failures are out of scope and explicitly expected).
- `normalise_situation` is idempotent and produces numeric street/hero_position.
- Schema preflight is clean on every present BP JSONL — Fix 1 holds.
- Working tree is clean.
- Disk headroom is ample.
- Generator entry points are all callable.

---

## Flags (non-blocking)

- **F1.** `training-data/factory_batch4_situations.jsonl` is absent on disk. This is expected (Phase 1 target), but the owner should confirm that batch 4 is part of the planned Phase 1 generation set.
- **F2.** `prompts/gto_labeller_v3.md` is absent. Not a Phase 1 blocker but Phase 3 (calibration gate) cannot proceed until it is authored from v2 + Scope §3 Additions A/B/C/D.
- **F3.** The 3 ANOMALY-A CSV failures mean that any future retrain that does NOT use `--allow-mixed-encoding` will refuse to proceed. Builder should keep the flag wired into v2.3 retrain scripts or plan a one-shot upstream fix of `v2_2_training.csv` before Phase 4.

---

*Builder: Phase 0 complete, awaiting Architect sign-off or Phase 1 kick-off order.*
