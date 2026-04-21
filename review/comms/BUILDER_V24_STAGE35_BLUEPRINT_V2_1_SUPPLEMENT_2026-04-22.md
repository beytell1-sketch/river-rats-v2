---
date: 2026-04-22
from: Builder (supplement to blueprint v2)
to: Orchestrator · Multi-agent reviewer panel (second reconciliation)
re: Attention-flag pipeline MUSTs #26 + #27 + audit column — supplement to blueprint v2 (8bb0f9f)
status: SUPPLEMENT — additive; keeps blueprint v2 at 8bb0f9f as base; second reconciliation reviews both together
extends: review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md (8bb0f9f)
sources:
  - review/comms/MAIN_TERMINAL_ATTENTION_FLAG_GAP_CORRECTION_2026-04-22.md (00:27 drop)
  - review/comms/BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md (Stage 2 COMPLETE verified)
  - review/comms/RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md (108-feature precedent)
  - knowledge/three_way_gto.md §1.10-§1.12 (verified at line-level)
---

# Blueprint v2.1 — Supplement for Attention-Flag Pipeline

Attention-flag gap was published after blueprint v2 commit (`8bb0f9f`)
landed. Per orchestrator directive + correction, this supplement adds
2 MUSTs + 1 audit column, retracts 2 over-claimed MUSTs. Blueprint v2
base stays intact at `8bb0f9f`; reconciliation pass #2 reviews this
supplement alongside v2 as a combined artifact.

**Net scope after supplement:** 25 MUSTs total.

- 23 from blueprint v2 (unchanged)
- 2 new (#26, #27) from correction

---

## 1. Retractions (MUSTs #24 + #25 dropped from blueprint scope)

### 1.1 MUST #24 — RETRACTED

**Original claim:** KB §1.9 must be updated to include attention-tag
conventions for the 4 new blocker features.

**Why retracted (verified against source):**

- **Wrong section number.** Attention-tag content landed at §1.10–§1.12,
  not §1.9. Verified at `knowledge/three_way_gto.md` lines 231, 263, 327,
  367, 391, 427, 483. §1.9 ("Preflop geometry vs postflop composition")
  was intentionally untouched to preserve v3.1 prompt cross-references.
- **Stage 2 COMPLETE.** `BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md` confirms
  Stage 2 shipped. KB §1.11 explicitly includes labelling-heuristic
  guidance for PRIMARY-tagging the new blockers (e.g., the CALL-lean
  rule: `nut_made_block_pct − (flush_draw_block_pct + straight_draw_block_pct) / 2 > 0.15`
  triggers "do not tag blocker features as PRIMARY").
- **GTO-reviewed.** `GTO_REVIEW_V24_STAGE2_KB_1_10_2026-04-20.md` applied
  6 modifications; Stage 2 sign-off recorded.

No blueprint action. Manifest already reflects Stage 2 COMPLETE (per
orchestrator's v1.9 correction commit).

### 1.2 MUST #25 — REFRAMED (Stage 3 deliverable, not blueprint v2 scope)

**Original claim:** v3.2 prompt must include mandatory-tag table entries
for the 4 new blocker features.

**Why reframed:**

- Stage 3's explicit goal (per `BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md`):
  derive v3.2 prompt from KB §1.10–§1.12 including mandatory-tag table
  extension for new features, DO NOT Rule 6 update, action-default
  table update, one-concrete-example-per-feature.
- This IS the Stage 3 plan. Not a MUST missed from blueprint v2's Stage
  3.5 scope; it's a Stage 3 deliverable verified on Stage 3 review gate.
- Builder (Stage 3 terminal or future context) owns the prompt update;
  orchestrator reviews.

Blueprint v2.1 action: none. Manifest v1.9 Stage 3 gate already requires
these deliverables per the cross-reference to Stage 2 COMPLETE doc.

---

## 2. MUST #26 — CRITICAL — Training pipeline writes expanded attention columns

**Files:**
- `river-rats-core/assemble_pilot_data.py` (v2.2 writer; may be superseded by `assemble_v23*.py` for v2.4)
- `assemble_v23_clean.py` + siblings (assembly entry points that invoke `RAW_FEATURES`)
- Per-file read TBD at commit time; verify which entry point produces the v2.4 training CSV

**Line range:** Entry-point-specific; anchored by `RAW_FEATURES` + `ATTN_FEATURES` + CSV header construction.

### 2.1 Why this MUST exists

Verified at source:
- `assemble_v23_clean.py:27` — `ATTN_FEATURES = [f"attn_{c}" for c in RAW_FEATURES]`. 1:1 mapping. Adding 4 raw blockers to `RAW_FEATURES` auto-extends `ATTN_FEATURES` IF `RAW_FEATURES` derives from `gto_model.FEATURE_COLUMNS` (which per manifest bumps 55→59 at Stage 5).
- `training-data/pilot_20_attention.csv` verified header: 54 raw + 54 `attn_*` + `label` = 109 columns. Precedent confirmed.
- Labeller output (`pilot_20_enriched.jsonl` sample): `"attention_flags": {"street": 0, "facing_bet": 0, ...}` — per-feature 0/1 dict. The writer pulls values from `rec['attention_flags'][fc]` (per `run_attention_experiments.py:330`).
- **Gap:** if the labeller's `attention_flags` dict lacks keys for the 4 new blockers (because labellers weren't prompted to tag them), the writer silently writes 0 for all 4 new attention columns. Training signal = pure noise.

This is the SAME silent-fallback failure mode as CRIT #2. Different layer, same v2.3.2-class corruption.

### 2.2 BEFORE — verified at `assemble_v23_clean.py:27` and sibling headers

```python
# assemble_v23_clean.py:25-30
RAW_FEATURES = [
    'street', 'facing_bet', 'pot_size', 'to_call', ...  # 54 entries
]
ATTN_FEATURES = [f"attn_{c}" for c in RAW_FEATURES]
CSV_HEADER = RAW_FEATURES + ATTN_FEATURES + ['label']
```

Per-row write pulls `record['attention_flags'].get(fc, 0)` — missing keys default to 0 silently.

### 2.3 AFTER

**Step A — bind `RAW_FEATURES` to `gto_model.FEATURE_COLUMNS` (source of truth):**

```python
# New import at top of assemble_v23_clean.py + any v2.4 assembler
from gto_model import FEATURE_COLUMNS

RAW_FEATURES = list(FEATURE_COLUMNS)
ATTN_FEATURES = [f"attn_{c}" for c in RAW_FEATURES]
# CSV_HEADER unchanged — derived from above
```

When `gto_model.FEATURE_COLUMNS` bumps 55→59 at Stage 5, `RAW_FEATURES`
auto-updates; `ATTN_FEATURES` auto-updates. Schema parity.

**Step B — strict mode for missing attention flags:**

```python
# Per-row write
def _attention_value(record: dict, feature_name: str) -> int:
    """Read attention flag for feature_name from record. Strict mode
    (MUST #26): warn/raise if a feature is expected but absent.

    Controlled by env ASSEMBLER_STRICT_ATTENTION:
      unset/0  — silent 0-default (legacy-compat)
      warn     — log.warning per missing key
      raise    — RuntimeError (v2.4 re-assembly)
    """
    af = record.get('attention_flags', {}) or {}
    if feature_name in af:
        return int(af[feature_name])
    # Feature absent from labeller output
    strict = os.environ.get('ASSEMBLER_STRICT_ATTENTION', '0').lower()
    sid = record.get('situation_id', '<unknown>')
    if strict == 'raise':
        raise RuntimeError(
            f'assemble: attention_flags[{feature_name!r}] missing on '
            f'situation_id={sid}. ASSEMBLER_STRICT_ATTENTION=raise is set. '
            f'Silent 0-default would corrupt the attention signal — fix '
            f'the labelling prompt (v3.2 per Stage 3) to tag this feature.'
        )
    elif strict in ('warn', '1'):
        import logging
        logging.getLogger(__name__).warning(
            'assemble: attention_flags[%r] missing on sid=%s — defaulting '
            'to 0. This silently drops training signal; enable strict mode '
            'for Stage 4 re-assembly.', feature_name, sid,
        )
    return 0
```

Per-row write loop calls `_attention_value(record, fc)` for each `fc in RAW_FEATURES`.

**Step C — audit column for vocabulary version:**

```python
# CSV_HEADER adds one audit column at the end:
CSV_HEADER = RAW_FEATURES + ATTN_FEATURES + ['label', '_attention_vocabulary_version']

# Per-row write appends version string:
ATTENTION_VOCAB_VERSION = "v2.4_NNflag"   # where NN = len(FEATURE_COLUMNS)
# or for backward-read compatibility: derive from len at write time
# so one assembler binary can re-label v2.2-era or v2.4-era data
row_values = [...] + [label_value, f"v2.4_{len(FEATURE_COLUMNS)}flag"]
```

Exp 3 mechanism won't treat this as a feature (it reads by column name,
not position); audit-only column. Trainer skips it when building X.

### 2.4 Vocabulary decision — option (a) 1:1 mapping (documented, no choice to make)

The correction asked the builder to decide between:
- (a) 1:1 mapping — every raw feature gets `attn_<name>`
- (b) Concept vocabulary — curated tag list aggregating features

**Decision: option (a).** Source verification shows v2.2 already used
(a) at `assemble_v23_clean.py:27` and `run_attention_experiments.py:461`.
Not a new decision; documented precedent. Option (b) would require
rebuilding the Exp 3 mechanism and is out of Stage 3.5 scope.

**Numbering convention:** `attn_<raw_feature_name>`. Already
established at `assemble_v23_clean.py:27`. Adding:
- `attn_nut_flush_block`
- `attn_flush_draw_block_pct`
- `attn_straight_draw_block_pct`
- `attn_nut_made_block_pct`

### 2.5 Signature changes + affected callers

- `assemble_v23_clean.py` + any v2.4-era assembler: `RAW_FEATURES` sources from `gto_model.FEATURE_COLUMNS`; `ATTN_FEATURES` derived; `_attention_value` helper new; CSV_HEADER adds audit column.
- `run_attention_experiments.py:461` — not touched here; MUST #27 owns that.
- Labeller output schema (`attention_flags` dict) — labellers must tag 4 new blockers per MUST #25 (Stage 3 deliverable). If `STAGE4_STRICT_ATTENTION=raise` fires on Stage 4 re-labelling: labelling prompt hasn't landed the new tag-rules → Stage 3 hasn't shipped → Stage 4 gate (manifest v1.9) should have blocked entry.

### 2.6 Test plan

- New unit test `test_assembler_emits_expanded_attn_columns` — mock `gto_model.FEATURE_COLUMNS` with 59 entries, call assembler, assert CSV header contains `attn_nut_flush_block` etc.
- New unit test `test_assembler_strict_raises_on_missing_attn` — strict=raise env, mock record without new blocker key in attention_flags, assert RuntimeError.
- New unit test `test_assembler_warns_on_missing_attn` — strict=warn, assert log captured, value defaults to 0.
- New integration test `test_vocabulary_audit_column_on_v24_csv` — assemble sample record through v2.4 path, read back CSV, assert `_attention_vocabulary_version == 'v2.4_59flag'`.
- Dry-run verification before Stage 4 re-label: assemble 5 hands from Stage 3-compatible labeller output, verify all 4 new attn columns are captured correctly.

### 2.7 Commit placement

Inserted as commit 11A in blueprint v2 sequence (between commit 11 MUST #17 freq table and commit 12 corpus load). Logical siblings: both are post-code changes; attention pipeline parity can run in parallel with corpus prep.

---

## 3. MUST #27 — CRITICAL — Trainer reads dynamic vocabulary

**File:** `river-rats-core/run_attention_experiments.py`
**Line range:** 461 (hardcoded `col_names_108`) + any other hardcoded counts

### 3.1 Why this MUST exists

Verified at source: `run_attention_experiments.py:461`:

```python
col_names_108 = list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS]
```

The name "108" is cosmetic — the content derives from `FEATURE_COLUMNS`. BUT:

- `FEATURE_COLUMNS` length has been 54 through v2.2 / v2.3 / v2.3.1.
- v2.4 bumps it to 59 at Stage 5 per manifest.
- The file name + variable name baked "108" in several places (verified by grep at lines 456, 461, 702–746 context). Cosmetic naming is fine; structural hardcoding is not.

Risk: any downstream code that reads `col_names_108` expects 108 entries. Trainer error paths, output diffing, validation harnesses may hard-fail at 118.

### 3.2 BEFORE (`run_attention_experiments.py:454–463`)

```python
def exp3_feature_attention_training(...) -> dict:
    """
    108 features: 54 original + 54 attn_* binary flags.
    """
    col_names_108 = list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS]
    X, y, _ = load_feature_csv(ATTENTION_CSV, col_names_108, 'label')
```

### 3.3 AFTER

```python
def exp3_feature_attention_training(...) -> dict:
    """
    Feature vector: 2 × len(FEATURE_COLUMNS) — raw + attn_* binary flags.
    Dynamic count per MUST #27: v2.2 was 108 (54 raw + 54 attn); v2.4
    projects to 118 (59 raw + 59 attn). Vocabulary version captured in
    training-CSV audit column (_attention_vocabulary_version) per MUST #26.
    """
    col_names = list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS]
    expected_total = 2 * len(FEATURE_COLUMNS)
    X, y, _ = load_feature_csv(ATTENTION_CSV, col_names, 'label')

    # Sanity assertion — X width must match expected total.
    # Catches CSV-header-vs-code-count drift loudly.
    assert X.shape[1] == expected_total, (
        f'MUST #27: X.shape[1]={X.shape[1]} != expected {expected_total}. '
        f'Training-CSV column count drifted from FEATURE_COLUMNS. '
        f'Likely cause: CSV has old vocabulary version; check '
        f'_attention_vocabulary_version audit column.'
    )
```

### 3.4 Vocabulary-version cross-check

On load, read the `_attention_vocabulary_version` audit column from the CSV header (if present) and assert it matches the expected version:

```python
# At CSV load time, before building X:
import pandas as pd
csv_header = pd.read_csv(ATTENTION_CSV, nrows=0).columns.tolist()
if '_attention_vocabulary_version' in csv_header:
    sample_row = pd.read_csv(ATTENTION_CSV, nrows=1)
    vocab = sample_row['_attention_vocabulary_version'].iloc[0]
    expected = f'v2.4_{len(FEATURE_COLUMNS)}flag'
    assert vocab == expected, (
        f'MUST #27: attention vocabulary mismatch. '
        f'CSV vocab={vocab!r}, trainer expects={expected!r}. '
        f'Either CSV was produced with old FEATURE_COLUMNS or '
        f'trainer is outdated; reconcile before retraining.'
    )
else:
    # Pre-MUST-#26 CSV; log a warning but proceed
    import logging
    logging.getLogger(__name__).warning(
        'MUST #27: _attention_vocabulary_version audit column absent '
        'from %s. This CSV predates MUST #26. Assuming vocab matches '
        'current FEATURE_COLUMNS; if load fails, re-assemble with v2.4 '
        'writer.', ATTENTION_CSV,
    )
```

### 3.5 Backward compat decision (left to builder per correction)

Correction asked: "should v2.4 trainer be able to load a v2.2 CSV (54+54) and zero-pad the new attention columns for warm-start?"

**Decision: NO zero-pad backward load.** Reasoning:
- Zero-padding new attention columns would train v2.4 on a warm-start where the new attention signal is uniformly 0. XGBoost would learn "never attend to the new blockers" and that bias would persist past warm-start.
- v2.4 training should begin from a freshly-assembled CSV that includes real attention values for the new blockers.
- Warm-start from v2.3.1 raw-feature weights is still possible — XGBoost `xgb_model` param loads the prior model, and new columns are trained from scratch. But the CSV feeding the warm-start must have the full 118-column shape.

If owner/orchestrator wants zero-pad backward compat, flip the decision; cheap to add `if csv_width == 108: X = np.hstack([X, np.zeros((len(X), 10))])`. Recommend NOT doing it; defer to post-Stage-5 if training-data authoring is slower than expected.

### 3.6 Signature changes + affected callers

- `run_attention_experiments.py`:
  - Rename `col_names_108` → `col_names` internally
  - Add X width assertion
  - Add vocabulary-version cross-check
  - Docstring "108 features" → dynamic language
- Any downstream consumer reading the `exp3_feature_attention_training` return dict — unchanged; return shape is the same.

### 3.7 Test plan

- New unit test `test_trainer_loads_v24_csv_59flag` — synthetic CSV with 118 cols + `v2.4_59flag` audit, trainer loads clean.
- New unit test `test_trainer_assert_fires_on_width_mismatch` — CSV with 108 cols but FEATURE_COLUMNS at 59, assert raises.
- New unit test `test_trainer_vocab_version_mismatch_raises` — CSV with `v2.2_54flag`, FEATURE_COLUMNS at 59, assert raises.
- New unit test `test_trainer_warns_on_missing_audit_column` — pre-MUST-#26 CSV without audit column, assert warning log.

### 3.8 Commit placement

Commit 11B in blueprint v2 sequence (sibling of MUST #26). Both are Stage 5 prereqs; land together so Stage 5 kick-off has both fixes available.

---

## 4. Updated 25-MUST summary

Appended to blueprint v2 §1 master table:

| # | Severity | File | Summary |
|---|----------|------|---------|
| 24 | RETRACTED | — | KB §1.10-§1.12 already covers PRIMARY-tagging; Stage 2 COMPLETE |
| 25 | REFRAMED | — | v3.2 prompt extension is Stage 3 deliverable, not Stage 3.5 scope |
| 26 CRIT | NEW | `assemble_v23_clean.py` + siblings | Assembler writes expanded attention columns; strict env mode; audit column |
| 27 CRIT | NEW | `run_attention_experiments.py` | Trainer reads dynamic vocabulary; width assertion; version cross-check |

**Blueprint v2 §1 + this supplement §4 = 25 MUSTs net.**

---

## 5. Updated commit sequence

Blueprint v2 §11 sequence remains 15 commits; supplement inserts 2 new commits:

| # | Commit | Source |
|---|--------|--------|
| 1–10 | Blueprint v2 §11 commits 1–10 (HIGH #5 through MUST #8 partial delete) | Blueprint v2 |
| 11 | `Stage 3.5 MUST #17: freq table medium_made 0.92 → 0.85` | Blueprint v2 |
| **11A (NEW)** | **`Stage 3.5 MUST #26: assembler writes expanded attn cols + audit column`** | **Supplement** |
| **11B (NEW)** | **`Stage 3.5 MUST #27: trainer dynamic vocab + version cross-check`** | **Supplement** |
| 12 | `Stage 3.5 corpus: 81-case consumer + MUST #18` | Blueprint v2 |
| 13 | `Stage 3.5 M4 re-audit: blocker bypass + NaN + mass` | Blueprint v2 |
| 14 | `Stage 3.5 M5 re-run: MUST #16 guard` | Blueprint v2 |
| 15 | `Stage 3.5 SHIP: audit report + Path (c) sidecars authored` | Blueprint v2 |

**Net commits: 17 (15 base + 2 supplement).** Re-numbering kept verbose
(11A/11B) to preserve blueprint v2's §11 authoritative numbering.

---

## 6. New questions for second-pass reconciliation

Appended to blueprint v2 §13's list:

| Q | Topic | Recommended answer |
|---|-------|--------------------|
| Q27 | Option (a) 1:1 attention vocabulary confirmed by v2.2 precedent — any case for (b) concept vocabulary in v2.4 scope? | No — (b) is a v2.5+ research ticket; (a) matches shipped mechanism |
| Q28 | Strict env-gated mode for assembler (`ASSEMBLER_STRICT_ATTENTION`) acceptable, or prefer function-parameter strict? | env for MVP (matches CRIT #2 pattern); parameterise if Stage 5 trainer wants finer control |
| Q29 | Zero-pad backward compat for v2.2 CSV load at v2.4 trainer? | No — would corrupt warm-start; retrain on real values or skip warm-start |
| Q30 | Vocabulary-version audit column format `v2.4_59flag` vs alternatives? | Builder pick; alternatives `v2.4_59f` or semver-like `v2.4.0/59attn`. Current pick: `v2.4_59flag` for continuity with `exp3_54flag` label |
| Q31 | Stage 3 deliverable gate — verify Stage 3 terminal's v3.2 prompt includes mandatory-tag entries for all 4 new blockers before Stage 4 opens? | YES — part of manifest v1.9 Stage 4 gate, cross-stream check |

---

## 7. Cross-MUST overlap additions

Additions to blueprint v2 §6:

### 7.1 MUST #26 ↔ MUST #27

Both read from / write to the same CSV schema. Overlap is additive —
#26 writes `_attention_vocabulary_version`, #27 reads + asserts on it.
No edit conflict; land in #26-first order (writer produces the column
the trainer later validates).

### 7.2 MUST #26 ↔ CRIT #2 (MUST #2)

Parallel patterns. CRIT #2's `_action_history_present` audit column
and MUST #26's `_attention_vocabulary_version` audit column both land
in training-CSV schema. Both env-gated for strict mode. Both guard
against silent training-data corruption at Stage 4.

Consolidated audit column set appended to training CSV:
- `_action_history_present` (CRIT #2, bool/int)
- `_villain_folded` (HIGH #4, bool/int)
- `_villain_chain_overflowed` (MUST #15, bool/int)
- `_surviving_weight` (HIGH #5, float)
- `_villain_range_chain_steps` (stringified list, for audit only)
- `_attention_vocabulary_version` (MUST #26, string)

Six audit columns. All appended after raw + attn + label. Trainer
skips these when building X.

### 7.3 MUST #27 backward compat decision affects M4 re-audit

Blueprint v2 §8 M4 re-audit runs extraction against v2.3.1 training
CSV (54 raw + 54 attn = 108 cols). Once MUST #26 + #27 land, the v2.3.1
CSV is still the audit baseline BUT its column count mismatches the
new trainer. Solutions:

- (a) M4 audit runs through extraction only (not trainer) — no conflict.
  Confirmed by reading `run_stage35_backfill_audit.py`: it writes a new
  CSV, doesn't load into the attention trainer. No-op.
- (b) If a post-MUST-27 audit variant loads the v2.3.1 CSV through the
  trainer, it'd hit the MUST #27 width assertion. Expected behavior —
  the audit would fail loudly and prompt re-assembly.

No blueprint change needed; flag for orchestrator awareness.

---

## 8. Consolidated observability hooks (supersedes blueprint v2 §10)

Single definitive list of all audit columns landed by MUSTs:

| Column | MUST | Type | Purpose |
|---|---|---|---|
| `_action_history_present` | CRIT #2 / #2 | int (0/1) | Stage 4 mixture detection; per-row strict-gate provenance |
| `_villain_folded` | HIGH #4 / #4 | int (0/1) | Stage 4 training row-drop mask for blocker columns |
| `_villain_chain_overflowed` | MUST #15 / merged #4 | int (0/1) | Same; over-narrow variant |
| `_surviving_weight` | HIGH #5 / #5 | float | Distribution audit; chain quality metric |
| `_villain_range_chain_steps` | HIGH #5 / #5 | string (JSON list) | Audit-only; verify chain exercised |
| `_villain_range_chain_truncated` | HIGH #5 / #5 | int (0/1) | Safety rail fired |
| `_attention_vocabulary_version` | MUST #26 | string | Vocab versioning for multi-vintage training sets |

Model inference reads `FEATURE_COLUMNS` (the raw + attn names); audit
columns never enter the X matrix. Trainer skips all columns with
leading underscore.

---

## 9. Verification items added to in-flight list

Blueprint v2 §12.2 deferred items gain:

1. `assemble_v23_clean.py` vs `assemble_v23.py` vs `assemble_v23_1.py`
   vs `assemble_v23_2.py` — which is the canonical v2.4-era assembler?
   Read during MUST #26 implementation; fix patches targeted at the
   canonical one; others either updated in parallel or marked superseded.
2. `assemble_pilot_data.py` (v2.2-era writer) — is it still called by
   any live path, or superseded by `assemble_v23_*` family? Read
   during MUST #26 implementation.
3. Full labeller-output-schema audit — confirm the `attention_flags`
   dict comes from the labeller (per Stage 3 v3.2 prompt) vs a
   downstream transformation. If the latter, strict mode needs to fire
   at the transformation, not at `assemble_pilot_data`.
4. `FEATURE_COLUMNS` in `gto_model.py` — when does it flip from 55 to
   59? Manifest says Stage 5. Blueprint v2 references the held-back
   schema. MUST #26's `RAW_FEATURES = list(FEATURE_COLUMNS)` needs to
   see the 59-column version at Stage 4 assembly time; Stage 5 trainer
   reads the same list. Ordering: Stage 4 must un-hold-back
   `FEATURE_COLUMNS` before re-assembly. Timing verification.

All four can be resolved in commit 11A's first 30 minutes.

---

## 10. Execution posture

**Blueprint v2.1 supplement complete.** Additive to blueprint v2 at
`8bb0f9f`. Net scope: 25 MUSTs. 17 commits. Adds 2 new MUSTs (#26, #27),
retracts 2 (#24, #25). New audit column + env-strict mode for assembler
mirrors CRIT #2's pattern for actions.

Multi-agent reconciliation pass #2 should review blueprint v2 + this
supplement as a combined artifact. If reconciliation produces new
MUSTs on this supplement: re-cut v2.2 or continue amending with
follow-up supplements per orchestrator's convention.

No code edits until reconciliation signal. Standing by.
