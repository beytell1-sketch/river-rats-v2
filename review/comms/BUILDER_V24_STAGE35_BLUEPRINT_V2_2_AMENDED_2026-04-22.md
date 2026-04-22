---
date: 2026-04-22
from: Builder (amendment per orchestrator STEP 2 directive)
to: Orchestrator · Multi-agent reviewer panel (reconciliation pass #3)
re: Amended supplement — consolidates reconciliation #2 16 MUSTs (#28–#43) + Q32–Q35 resolutions + MUST #44 + source re-verification
status: AMENDED SUPPLEMENT — supersedes v2.1 supplement (3166759); blueprint v2 base (8bb0f9f) still intact
replaces: review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_1_SUPPLEMENT_2026-04-22.md (3166759)
sources:
  - review/comms/MAIN_TERMINAL_DIRECTIVE_BLUEPRINT_V2_2_STEPS_2026-04-22.md (5774e51)
  - review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_BLUEPRINT_V2_2026-04-22.md (b8f9563)
  - review/comms/BUILDER_V24_GROUNDING_REPORT_2026-04-22.md (3e50dd5)
  - review/comms/PRACTICAL_PRO_REVIEW_PASS2_STAGE35_V2_2026-04-22.md
---

# Stage 3.5 — Blueprint v2.2 (Amended Supplement)

Per orchestrator directive 5774e51, this amendment consolidates:
- Source re-verification results per STEP 1 (all 5 sub-items)
- Q32–Q35 resolutions from directive (no options to pick)
- 16 new MUSTs #28–#43 from reconciliation pass #2
- New MUST #44 (Q35 verification result) with scope determined by finding
- Manifest version bumps v1.9 → v1.10 throughout

**Active MUST count: 42** (25 from blueprint v2 + supplement + 16 from reconciliation #2 + 1 from this amendment). #24 retracted, #25 reframed (inactive).

No code edits until multi-agent reconciliation pass #3 signals clean.

---

## Table of contents

1. STEP 1 source re-verification results
2. Q32–Q35 resolutions (orchestrator decisions, applied)
3. Reconciliation #2 MUSTs #28–#43 — detailed specs
4. MUST #44 — production labelling format verification finding
5. Updated commit sequence (post-reconciliation #2)
6. MUST inventory (definitive list with status)
7. Questions for reconciliation pass #3

---

## 1. STEP 1 — Source re-verification results

All five items read via `git show origin/master:<path>` per discipline.
Origin HEAD at verification time: `5774e51`.

### 1.1 `coaching/explain_hand.py` bypass sites — verified

Read `coaching/explain_hand.py` on origin. Two bypass blocks:

**Block A (lines 250–264):**
```python
# line 250
from range_decomposition import decompose_range
# line 251
from feature_extractor import get_villain_range
...
# line 259
v_range = get_villain_range(hero_pos_raw, villain_pos_raw)
if feat_dict.get('facing_bet', 0):
    # line 261
    from range_narrowing import narrow_to_betting_range
    street_map = {0: 'flop', 1: 'turn', 2: 'river'}
    street_name = street_map.get(int(feat_dict.get('street', 0)), 'flop')
    # line 264 — CALL SITE
    v_range = narrow_to_betting_range(v_range, board_cards_list, street_name)
```

**Block B (lines 315–329):**
```python
# lines 315–316
from range_decomposition import decompose_range
from feature_extractor import get_villain_range
...
# line 324
v_range = get_villain_range(hero_pos_raw, villain_pos_raw)
if feat_dict.get('facing_bet', 0):
    # line 326
    from range_narrowing import narrow_to_betting_range
    ...
    # line 329 — CALL SITE
    v_range = narrow_to_betting_range(v_range, board_cards_list, street_name)
```

**Correction to reconciliation #2 MUST #30 phrasing:**
- Reconciliation #2 stated "coaching/explain_hand.py:251, 261, 326 are MUST #6/#19 equity-bypass sites". Those line numbers are **IMPORT statements** within the bypass blocks. The actual CALL SITES are 264 and 329.
- The two BLOCKS together (250–264 and 315–329) are each a full get_villain_range + narrow_to_betting_range pair without action_history. Both need MUST #6 chain-inheritance AND MUST #5 tuple-unpack.

**Net scope for MUSTs #5 + #6 + #19:**
- 2 call sites at coaching/explain_hand.py:264, 329 → tuple-unpack (HIGH #5)
- 2 bypass blocks (250–264, 315–329) → chain-inheritance via `_get_chain_narrowed_villain_range` helper (MUST #6 + #19)

### 1.2 `gto_model.py:64` FEATURE_COLUMNS — verified

Read `gto_model.py` on origin. Lines 34–63 define `FEATURE_COLUMNS` as a 55-entry tuple. Final three entries (indices 52–54):
```python
# v9 feature 53: preflop aggressor flag
"is_preflop_aggressor",
# feature 54: medium/weak made hand pct in villain range
"villain_medium_made_pct",
# feature 55: board-adjusted hero range percentile
"board_adjusted_hrp",
```

Line 65: `N_FEATURES = len(FEATURE_COLUMNS)  # 55`

**Confirmed:** `FEATURE_COLUMNS` length = 55. Reconciliation #2 MUST #31 is correct; my v2.1 supplement's "54 → 59" framing was wrong. Truth is **55 → 59**.

### 1.3 `pilot_20_attention.csv` header — verified

Read CSV header on origin. Column count = **109**. Sample first 37 of the raw-feature columns (before attn_ prefix section) matches v2.2-era 54-feature set — **missing `board_adjusted_hrp`**.

**Held-back feature confirmed: `board_adjusted_hrp`.**

- `gto_model.FEATURE_COLUMNS` = 55 entries (source of truth)
- `pilot_20_attention.csv` = 54 raw + 54 attn + 1 label = 109 (misses `board_adjusted_hrp`)
- v2.3.1 training CSV: same held-back pattern (per `gto_model.py:144` comment "Auto-detect feature width for backwards compatibility (v8=38, v9=45)"; v2.3 model trained on 45 cols; v2.3.1 trained on ~54 cols with held-back board_adjusted_hrp)

**v2.4 target:**
- `FEATURE_COLUMNS` expands from 55 to 59 (adds nut_flush_block, flush_draw_block_pct, straight_draw_block_pct, nut_made_block_pct)
- Stage 5 training CSV: **58 raw** (55 - 1 held-back + 4 new) + 58 attn + 1 label = 117 cols; OR **59 raw** if Stage 5 un-holds-back `board_adjusted_hrp`

Per manifest v1.10 line 144: "feature_columns_exposed: 55 # gto_model.FEATURE_COLUMNS held back for backward compat; exposes 59 in Stage 5 training". **Confirmed: Stage 5 will un-hold-back board_adjusted_hrp and add 4 new blockers.** v2.4 target CSV: 59 raw + 59 attn + 1 label = 119 cols.

### 1.4 `train_v2_3_1.py` + `train_v2_3_2.py` hardcoded counts — verified

**`train_v2_3_1.py:97`:**
```python
raw_features, attn_features = split_feature_columns(list(rows[0].keys()))
feature_order = raw_features + attn_features
logger.info("Features: %d raw + %d attn = %d total",
            len(raw_features), len(attn_features), len(feature_order))
```

**`train_v2_3_2.py:91`:** identical pattern.

Both trainers **already use dynamic column-count discovery** via `split_feature_columns(...)` helper (reads CSV header, splits by `attn_` prefix). No hardcoded column counts.

**Finding:** Only `run_attention_experiments.py:461` (Exp 3 pilot code) has the `col_names_108 = list(FEATURE_COLUMNS) + ['attn_'+f for f in FEATURE_COLUMNS]` hardcoded variable name pattern. MUST #27 scope narrows significantly:
- `train_v2_3_1.py` / `train_v2_3_2.py` are reference implementations of the correct pattern — future `train_v2_4.py` clones directly from these, NOT from `run_attention_experiments.py`
- `run_attention_experiments.py:461` optional patch — rename `col_names_108 → col_names`, update docstring to dynamic language. Lock in the pattern.

### 1.5 Phase 4 production-labelled JSONL record — verified (MUST #44 OUTCOME)

Read sample records from two files:

**Pilot schema (`pilot_20_enriched.jsonl`):**
```json
{
  "situation_id": "d4534_BB_flop",
  "label": "CHECK",
  "feat_dict": {...},
  "attention_flags": {
    "street": 0, "facing_bet": 0, "pot_size": 0,
    "draw_outs": 1, "raw_equity": 1, ...
  }
}
```
- Key name: `attention_flags`
- Values: `0` or `1` (binary ints)

**Production schema (`pass1_T1_labels.jsonl` — per-labeller Phase 4 output):**
```json
{
  "situation_id": "BP1_01",
  "hand_bucket": "drawing",
  "action": "RAISE",
  "confidence": "HIGH",
  "reasoning": "...",
  "intentions_raw": "...",
  "intentions": ["deny_equity"],
  "street_plan_raw": "...",
  "street_plan_tags": ["bet_protect_evaluate", ...],
  "feature_attention": {
    "equity_vs_range": "PRIMARY",
    "draw_outs": "PRIMARY",
    "flush_block_pct": "PRIMARY",
    ...
    "villain_top_pair_plus_pct": "CONFIRMED",
    "villain_medium_made_pct": "CONFIRMED",
    ...
  },
  "tier1_removals": {...},
  "alternatives_considered": [...]
}
```
- Key name: **`feature_attention`** (different from pilot's `attention_flags`)
- Values: **`"PRIMARY"` / `"CONFIRMED"` strings** (different from pilot's 0/1 ints)

**Consensus schema (`pass1_final_labels.jsonl`):** minimal
```json
{"situation_id": "BP1_01", "action": "RAISE", "label_source": "Pass1+relabel consensus"}
```
No attention info at all — this is the post-consensus label-only output.

**MUST #44 OUTCOME: (ii) Different schema.** Pilot and production differ in both key name and value type. Three implications:

1. **MUST #26 patch must handle both:**
   - Pilot assembler (`assemble_pilot_data.py`) reads `record['attention_flags'][fc]` → already expects int 0/1
   - v2.4 production assembler (future `assemble_v2_4.py`) must read `record['feature_attention'][fc]` → map `"PRIMARY"|"CONFIRMED"` → 1; missing/None → 0

2. **Mapping layer required in production assembler:**
   ```python
   def _attention_value(record: dict, feature_name: str) -> int:
       """Map labeller's feature_attention tag → binary attention flag.
       Production schema: dict values are 'PRIMARY' or 'CONFIRMED' strings.
       Pilot schema: dict values are 0/1 ints.
       Returns 1 if tagged PRIMARY or CONFIRMED; 0 otherwise.
       """
       # Support both schemas
       fa = record.get('feature_attention') or record.get('attention_flags', {}) or {}
       val = fa.get(feature_name, 0)
       if isinstance(val, str):
           return 1 if val in ('PRIMARY', 'CONFIRMED') else 0
       return int(val) if val else 0
   ```

3. **Strict-gate fires at DIFFERENT criteria per schema:**
   - Pilot: missing key in `attention_flags` dict → strict warns/raises
   - Production: missing key in `feature_attention` dict for a feature on the **mandatory-tag list** (per v3.2 prompt) → strict warns/raises
   - Untagged-but-not-mandatory features default to 0 silently (legitimate; labeller just didn't mark it)

**Documented in `docs/ASSEMBLER_PATTERN.md` (outline below in §3.2 MUST #29 spec).**

---

## 2. Q32–Q35 resolutions (applied)

Per orchestrator directive (5774e51) Section A:

- **Q32 (MUST #26 scope) → (C) hybrid.** Patch `assemble_pilot_data.py` + `assemble_v23_clean.py` as reference implementations. Author `docs/ASSEMBLER_PATTERN.md`. Stage 4's future `assemble_v2_4.py` clones; Stage 4 review gates on conformance.
- **Q33 (MUST #27 scope) → (C) hybrid + audit.** Patch `run_attention_experiments.py:461` as reference implementation (rename `col_names_108 → col_names`, dynamic docstring). Audit `train_v2_3_1.py` + `train_v2_3_2.py` for same pattern — **STEP 1.4 found both already use dynamic `split_feature_columns`**. They are reference implementations; no patches needed.
- **Q34 (push approach) → (B) fix-forward.** This amended supplement IS the fix-forward. Single-document review trail.
- **Q35 (production format) → verified FIRST via STEP 1.5.** Result: different schema (ii). MUST #44 spec reflects mapping-layer requirement.

Q32–Q35 resolved. Applied throughout §3.

---

## 3. Reconciliation #2 MUSTs #28–#43 — detailed specs

### 3.1 MUST #28 — CRITICAL — Floor-truncation NaN-flag

**File:** `river-rats-core/feature_extractor.py`
**Line range:** 1174–1195 (post-chain block in `extract_range_composition`)

**Problem:** When MUST #13 floor truncates and `narrow_by_action_history` reverts to `last_valid_range`, `current_range` is non-empty. Caller at line 1186 sees `if not v_range:` = False and proceeds. `_villain_chain_overflowed` stays False. Downstream composition + MUST #6 equity + MUST #19 `explain_hand` all consume the **partial-chain range as if full-chain**. No sentinel fires — silent-fallback anti-pattern.

**BEFORE (blueprint v2 §2.5 AFTER, now partial):**
```python
if not v_range:
    _last_step = chain_steps[-1] if chain_steps else ''
    if _last_step.endswith(':FOLD'):
        villain_folded = True
    else:
        chain_overflowed = True
        # ... warn + NaN
```

**AFTER:**
```python
# MUST #28: truncation sentinel from chain metadata, not just empty-range.
# `truncated=True` means mass-floor fired mid-chain + reverted to last
# valid range. Downstream must treat this as NaN-territory, same as
# over-narrow-to-empty. Don't silently consume partial-chain range.
if not v_range:
    _last_step = chain_steps[-1] if chain_steps else ''
    if _last_step.endswith(':FOLD'):
        villain_folded = True
    else:
        chain_overflowed = True
        # ... warn + NaN (existing HIGH #4 / MUST #15 branch)
elif chain_truncated:
    # Chain mass-floor fired; reverted to last-valid; v_range is partial
    # not full. NaN-flag per MUST #28.
    chain_overflowed = True
    import logging
    logging.getLogger(__name__).warning(
        'extract_range_composition: chain truncated at mass floor; '
        'reverted to last valid. Treating as over-narrow; NaN-flagging '
        'composition features per MUST #28. hero=%s villain=%s chain=%r',
        hero_pos, villain_pos, chain_steps,
    )
```

Cascade: `chain_overflowed=True` triggers existing NaN branches in Step 12 + Step 17 (per blueprint v2 §2.5) AND in composition loop (§2.5 NaN-flag loop). No additional code churn; reuses HIGH #4 plumbing.

**Test plan:**
- New unit test `test_truncated_chain_nan_flags` — synthetic deep chain that triggers floor at cumulative_surviving=0.08 < 0.10; assert `_villain_chain_overflowed=True`, composition features NaN.

**Commit:** lands in commit 5 (HIGH #4 + MUST #10 + MUST #15 consolidated NaN-spec commit).

### 3.2 MUST #29 — CRITICAL — Re-verified BEFORE blocks for attention-write paths

**Files per Q32 (C) hybrid:**
- `river-rats-core/assemble_pilot_data.py` — pilot/Exp 3 reference implementation
- `assemble_v23_clean.py` (repo root) — v2.3-era reference implementation
- `docs/ASSEMBLER_PATTERN.md` (NEW) — pattern documentation

**Per reconciliation #2 + my grounding:** Stage 4/5 production scripts don't exist. Pattern prescriptive for future `assemble_v2_4.py`; corrective for pilot + v2.3 scripts that exist today.

**BEFORE verified on origin (`assemble_v23_clean.py:25-30` + write loop):**
```python
RAW_FEATURES = list(FEATURE_COLUMNS)  # already bound (Step A no-op)
ATTN_FEATURES = [f"attn_{c}" for c in RAW_FEATURES]
CSV_HEADER = RAW_FEATURES + ATTN_FEATURES + ['label']
```

And the write layer:
```python
# pilot-all-1 path (line 113):
for col in ATTN_FEATURES: out[col] = 1.0

# v2.2-base silent-0 path (line 61):
out[col] = float(row.get(col, 0))
```

**BEFORE verified on origin (`assemble_pilot_data.py:820-960`ish):** hardcoded `ATTENTION_LEVELS` table merged into record before CSV write. Silent-0 defaults on any feature not in the hardcoded table.

**AFTER — strict env gate + audit column across all paths:**

```python
# Shared helper (in docs/ASSEMBLER_PATTERN.md + implemented per-assembler):
def _attention_value(record: dict, feature_name: str,
                     mandatory: bool = False) -> int:
    """MUST #26 + MUST #29 + MUST #44 —
    Bi-schema attention-flag extractor.

    Reads from either `feature_attention` (production, string values)
    or `attention_flags` (pilot, int values). Returns binary 0/1.

    Strict mode controlled by ASSEMBLER_STRICT_ATTENTION env:
      unset/0  — silent 0-default (legacy-compat)
      warn     — log.warning per missing mandatory-tag feature
      raise    — RuntimeError (v2.4 re-assembly)

    Args:
        record: labeller's output dict
        feature_name: feature to look up (e.g. 'villain_top_pair_plus_pct')
        mandatory: True if v3.2 prompt mandates tagging this feature.
                   Strict-gate only fires on mandatory-but-missing.
                   Non-mandatory untagged → 0 silently (legitimate).
    """
    # Production schema (Phase 4 onwards): feature_attention dict
    # Pilot schema (Exp 3): attention_flags dict
    fa = record.get('feature_attention') or record.get('attention_flags', {}) or {}
    val = fa.get(feature_name, None)

    if val is None:
        if mandatory:
            import os
            strict = os.environ.get('ASSEMBLER_STRICT_ATTENTION', '0').lower()
            sid = record.get('situation_id', '<unknown>')
            if strict == 'raise':
                raise RuntimeError(
                    f'MUST #26: mandatory feature {feature_name!r} absent '
                    f'from labeller output on sid={sid}. '
                    f'Strict mode set. v3.2 prompt must tag this feature; '
                    f'check prompt version + labeller output.'
                )
            elif strict in ('warn', '1'):
                import logging
                logging.getLogger(__name__).warning(
                    'MUST #26: mandatory feature %r absent on sid=%s; '
                    'defaulting to 0. Enable strict mode for Stage 4 '
                    're-assembly.', feature_name, sid,
                )
        return 0

    if isinstance(val, str):
        return 1 if val in ('PRIMARY', 'CONFIRMED') else 0
    return int(val) if val else 0


# Audit column at CSV write:
ATTENTION_VOCAB_VERSION = f"v2.4_{len(FEATURE_COLUMNS)}flag"
# Written per row as last col before label:
row_values = raw_vals + attn_vals + [ATTENTION_VOCAB_VERSION, label_value]
```

**CSV_HEADER update:**
```python
CSV_HEADER = RAW_FEATURES + ATTN_FEATURES + ['_attention_vocabulary_version', 'label']
```

**Mandatory-tag list lookup:** derived from v3.2 prompt's bucket-mandatory-tag table (per KB §1.11 + Stage 3 deliverable). For Stage 3.5 reference implementations, use the v3.1-era mandatory-tag list (4 villain composition features + bucket-specific per bucket).

**`docs/ASSEMBLER_PATTERN.md` outline:**
```markdown
# Attention-Flag Assembler Pattern (MUST #26 / #29 / #44)

## Purpose
Single canonical pattern for attention-flag capture from labeller
output to training CSV. Applies across v2.4 + future oracle versions.

## Schemas supported
- Pilot / Exp 3: `attention_flags: {feat: 0|1}`
- Production (v3 prompt onwards): `feature_attention: {feat: "PRIMARY"|"CONFIRMED"}`
- Helper `_attention_value(record, feature_name, mandatory)` normalises both.

## CSV schema
`RAW_FEATURES + ATTN_FEATURES + ['_attention_vocabulary_version', 'label']`
- RAW_FEATURES: list(gto_model.FEATURE_COLUMNS) minus any held-back (v2.4: held-back `board_adjusted_hrp` lifted at Stage 5 per manifest)
- ATTN_FEATURES: `[f"attn_{c}" for c in RAW_FEATURES]`
- `_attention_vocabulary_version`: `v2.4_{len(FEATURE_COLUMNS)}flag`

## Strict env gate
`ASSEMBLER_STRICT_ATTENTION`:
- unset/`0` — silent 0 (legacy-compat)
- `warn` — log warning per mandatory-tag miss
- `raise` — RuntimeError on first mandatory-tag miss (Stage 4 re-assembly)

## Cloning for new oracle versions
- Copy an existing assembler (e.g., `assemble_v23_clean.py`)
- Re-bind `RAW_FEATURES` to current `gto_model.FEATURE_COLUMNS`
- Ensure `_attention_value` helper is imported or duplicated
- Add audit column
- Ship-gate on strict=raise re-assembly of sample fixtures
```

**Test plan:**
- `test_attention_value_pilot_schema` — int 0/1 in attention_flags
- `test_attention_value_production_schema` — PRIMARY/CONFIRMED in feature_attention
- `test_attention_value_missing_mandatory_raises` — env=raise + mandatory=True + missing key
- `test_attention_value_missing_nonmandatory_silent` — missing but not mandatory → returns 0
- `test_audit_column_emitted_at_expected_position` — read back CSV, assert column present

**Commit:** lands in commit 11A (MUST #26 assembler). Doc `docs/ASSEMBLER_PATTERN.md` lands in same commit.

### 3.3 MUST #30 — CRITICAL — Caller list completeness

**Scope expansion:**
- HIGH #5 tuple-unpack: add `coaching/explain_hand.py:264, 329` — **2 new sites**
- MUST #6 chain-inheritance: add `coaching/explain_hand.py` blocks at 250–264 and 315–329 — **2 new blocks**

**Updated HIGH #5 caller list (14 tuple-unpack sites):**
| File | Line | Class | Action |
|------|------|-------|--------|
| `feature_extractor.py` | 503 | betting | tuple unpack |
| `feature_extractor.py` | 617 | betting | tuple unpack |
| `feature_extractor.py` | 805 | betting | tuple unpack |
| `feature_extractor.py` | 828 | betting | tuple unpack |
| `feature_extractor.py` | 1193 | betting | tuple unpack |
| `feature_extractor.py` | 1669 | betting | **deleted by CRIT #1 (no edit)** |
| `range_narrowing.py` | 791, 794, 797 | internal | covered in HIGH #5 Step B |
| `range_narrowing.py` | 875, 885 | test_narrowing demo | discard mass |
| `explain_hand.py` | 264, 329 | betting | tuple unpack |
| `coaching/explain_hand.py` | 264, 329 | betting | tuple unpack (**NEW — MUST #30**) |
| `tests/test_range_narrowing_stage35.py` | 288, 294, 296, 304, 307 | test | tuple unpack |

Grand total: **14 non-deleted root+coaching sites + 5 test-file sites.**

**MUST #6 scope expansion (chain-inheritance blocks):**
| File | Block lines | Action |
|------|-------------|--------|
| `feature_extractor.py` | 500–505 (partition HU) | helper call |
| `feature_extractor.py` | 605–617 (multiway get_villain_range loop) | helper call |
| `feature_extractor.py` | 790–806 (equity MW MC loop) | helper call |
| `feature_extractor.py` | 823–829 (equity HU) | helper call |
| `explain_hand.py` | 258–264, 323–329 | helper call + chain |
| `coaching/explain_hand.py` | 250–264, 315–329 | helper call + chain (**NEW — MUST #30**) |

6 equity/explain_hand bypass blocks → `_get_chain_narrowed_villain_range` helper.

**Coordination note:** `coaching/explain_hand.py` is an active-facade-pattern file per grounding. Adding MUST #6 chain plumbing to it is safe (it imports root `get_villain_range` + `narrow_to_betting_range`, both of which we're modifying). No additional import-path risk.

**Commit:** tuple-unpack sites land in commit 1 (HIGH #5); chain-inheritance blocks land in commit 6 (MUST #6 + #19).

### 3.4 MUST #31 — CRITICAL — Feature-count reconciliation

Applied throughout this amendment per STEP 1.2 + 1.3 findings:

**Reality (verified on origin):**
- `gto_model.py` FEATURE_COLUMNS = **55 entries** (not 54)
- Pilot CSV = 54 raw + 54 attn + 1 label = 109 cols
- Held-back feature: **`board_adjusted_hrp`** (Layer 1 of v2.3.1; gto_model exposes it for SHAP but CSVs withheld it until v2.4 Stage 5)
- Manifest v1.10 line 144: confirms Stage 5 un-holds-back board_adjusted_hrp + adds 4 new blockers → v2.4 CSV target = **59 raw + 59 attn + 1 label = 119 cols**

**Wrong in v2.1 supplement (now corrected):**
- Framed as "54 → 59" (wrong; reality is 55 → 59 with held-back adjustment)
- Claimed v2.2 was 108 (wrong; v2.2 was 109 with 54+54+label after held-back)

**Corrections to v2.1 supplement §2–§3:**
- All "54" references → "55 (with board_adjusted_hrp held back from CSV until v2.4)"
- All "108" references → "109 (54+54+label)"
- MUST #27 expected total changes:
  - Pre-Stage-5: `2 * (len(FEATURE_COLUMNS) - 1)` if held-back is still held back
  - Post-Stage-5: `2 * len(FEATURE_COLUMNS)` = 118 data cols + 1 label = 119 CSV cols

**Implication for `run_attention_experiments.py:461`:** builds `col_names_108 = 55 + 55 = 110` entries against a 109-col CSV. **This means Exp 3 code is already broken or silently mis-reads CSV**. Needs audit — may have been working by accident of `load_feature_csv` tolerating mismatched col_names. MUST #27 patch (rename to `col_names`, add header check per MUST #36) surfaces this pre-existing bug.

**Updated MUST #27 spec:**
```python
# AFTER (updated per MUST #31 + MUST #36):
def exp3_feature_attention_training(...) -> dict:
    """
    Feature vector width: 2 * (len(FEATURE_COLUMNS) - N_HELD_BACK)
    Held-back features: listed in _HELD_BACK_FEATURES constant.
    """
    _HELD_BACK_FEATURES = frozenset(['board_adjusted_hrp'])  # until v2.4 Stage 5
    active_features = [c for c in FEATURE_COLUMNS if c not in _HELD_BACK_FEATURES]
    col_names = list(active_features) + [f'attn_{c}' for c in active_features]

    # MUST #36: CSV-header reconciliation (not tautological width assert)
    import pandas as pd
    csv_header = pd.read_csv(ATTENTION_CSV, nrows=0).columns.tolist()
    missing = [c for c in col_names if c not in csv_header]
    if missing:
        raise RuntimeError(
            f'MUST #36: CSV missing expected columns {missing!r}. '
            f'Vocabulary version drift likely; check '
            f'_attention_vocabulary_version audit column.'
        )

    X, y, _ = load_feature_csv(ATTENTION_CSV, col_names, 'label')
    # ... no tautological width assert ...
```

**Commit:** lands in commit 11B (MUST #27 trainer), includes MUST #36 header check.

### 3.5 MUST #32 — CRITICAL — Close commit-sequence poisoning windows

Two windows per reconciliation #2:

**(a) Commits 2 → 12 window:** After CRIT #2 env-gated strict lands (commit 2), default env is `warn`. Stage 4 re-label could silently ship without `STAGE4_STRICT_ACTION_HISTORY=raise` set.

**(b) Commits 4 → 5 window:** CRIT #1 lands chain consumer (commit 4); MUST #10 NaN downstream lands (commit 5). Mid-deploy extracts see composition=0.0 (pre-NaN behavior) not NaN.

**Builder decision per directive Section E.2.4 (DECIDE and EXECUTE):**

**(a) → Commits 4+5 MERGE.** Pick sub-option (b) from reconciliation #2 MUST #32 — merge commits 4 and 5 into a single ship-coherent commit. Rationale:
- Eliminates the mid-deploy distribution seam
- NaN branches + chain-consumer co-land (single logical change)
- Reduces commit count 15 → 14 (or 16 → 15 with 11A/11B from supplement)

**(b) → Orchestrator-level lockout for commits 2–12 window.** Rationale:
- Env-default-=-raise is attractive (no silent bypass) but breaks all read-only paths that don't need chain (display, eval, calibration in warn-only mode)
- Instead: manifest-level enforcement — Stage 4 cannot fire while Stage 3.5 implementation is in flight. Manifest v1.10 already has this gate; amendment strengthens with explicit "no re-label while MUSTs-in-flight" language.

**Revised commit sequence (merged 4+5):**

| # | Commit | Lands |
|---|--------|-------|
| 1 | HIGH #5 + MUST #13 | Tuple-return, mass thread, 10% floor, 14 call-site tuple unpacks (incl. coaching/explain_hand.py:264, 329) |
| 2 | CRIT #2 + MUST #9 | Strict env gate, pipeline unswallow, `_action_history_present` CSV col |
| 3 | HIGH #3 + MUST #11 + #12 | Same-street sequence collapse pre-filter |
| **4** | **CRIT #1 + HIGH #4 + MUST #10 + MUST #15 + MUST #28** | **Merged: publish `_villain_range_narrowed`, consume in Step 12+17, folded/overflow/truncated sentinels, NaN spec across 4 layers** |
| 5 | MUST #6 + MUST #19 + MUST #30 scope | Equity + explain_hand + coaching/explain_hand chain inheritance (helper with cache + multiway spec per MUST #34) |
| 6 | MUST #20 | calibration_exam.py `_action_history` plumbing + dry-run sidecar batch |
| 7 | MUST #22 | reference_evaluator.py `_action_history` plumbing + dry-run sidecar batch |
| 8 | MUST #23 | train_sizing_model.py (verify + plumb or document (y) bypass) |
| 9 | MUST #8 partial delete + MUST #37 audit | Delete 2 coaching files after sys.path side-effect audit |
| 10 | MUST #17 + MUST #38 + MUST #39 + MUST #40 | Frequency table coherence, KB §1.11 asymmetric thresholds + combo-draw max addendum |
| 11 | MUST #41 | Belt-and-braces count guard |
| 12 | MUST #42 + MUST #43 | NaN render player-English + CONTENT_API v4 ticket |
| 11A | MUST #26 + MUST #29 + MUST #44 helper | Assembler reference impls (pilot + v2.3 + doc), bi-schema helper |
| 11B | MUST #27 + MUST #31 + MUST #36 | Trainer dynamic vocab, feature-count reconciliation, CSV-header check |
| 13 | MUST #33 + corpus 81-case + coverage-gap tests | Reauthored T_J01/T_B05/T_J02 + 81-case consumer + 4 new tests |
| 14 | M4 re-audit (expanded) | Blocker bypass + NaN + mass + equity-shift distribution |
| 15 | M5 re-run + MUST #16 regression guard | Anchor non-empty chain assertion |
| 16 | Path (c) Phase 2 sidecars (owner-gated) + audit report + Stage 3.5 SHIP | Full sidecar authoring after dry-run approval |

**Total: 16 commits (merged 4+5 from 17 prior).**

**Commit:** MUST #32 is a meta-MUST — affects sequencing, not code. Documented here; no dedicated commit.

### 3.6 MUST #33 — HIGH — Corpus reauthoring with GTO-corrected targets

**File:** `review/tests/range_narrowing_test_corpus_2026-04-20.yaml`

Per reconciliation #2 GTO review, T_J01 / T_B05 / T_J02 values corrected:

```yaml
# T_J01 (owner canonical H_d9edab5d) — REAUTHORED per MUST #33
- id: "T_J01_owner_H_d9edab5d_turn_check_through_river_bet"
  expected_composition_post_fix:
    villain_tp_pct: 0.50       # not 0.55 — mediums RISE after turn-CHECK
    villain_medium_made_pct: 0.18   # not 0.04 — medium-heavy pot-control
    villain_draw_pct: 0.00
    villain_air_pct: 0.32       # not 0.41
  notes: "[REAUTHORED MUST #33] Donk-flop + turn-CHECK + river-bet.
          GTO correction: turn-CHECK is where mediums concentrate after
          donk-flop (villain donks wide, checks to pot-control on turn
          with mediums). River-bet is polarised but from a medium-heavy
          CHECK range → air density moderated."
  ship_criterion:
    verdict_flip_required: true
    pre_fix_oracle_action: "FOLD"
    post_fix_oracle_action_must_include: ["CALL", "MIXED_CALL_FOLD"]
    note: "If numbers move without verdict change, fix failed."

# T_B05 (donk-flop call-raise turn check) — REAUTHORED
- id: "T_B05_flop_bet_raise_call_three_step"
  expected_composition_post_fix:
    villain_tp_pct: 0.60
    villain_medium_made_pct: 0.28    # flat-call-a-raise IS medium pot-control
    villain_draw_pct: 0.05
    villain_air_pct: 0.07
  notes: "[REAUTHORED MUST #33] Flop BET-RAISE-CALL + turn-CHECK.
          Flat-call-a-raise range is medium-heavy; turn CHECK preserves
          that concentration (villain pot-controls with mediums after
          getting raised)."

# T_J02 (BET-CHECK-CALL-BET, 4 narrow classes) — NEW ENTRY
- id: "T_J02_owner_H_8dfb6ef8_bet_check_call_bet_line"
  category: "J. Owner-sourced canonical"
  description: "All 4 narrow classes in one chain: flop-BET, turn-CHECK, turn-CALL, river-BET"
  expected_composition_post_fix:
    villain_tp_pct: 0.60
    villain_medium_made_pct: 0.18    # turn-CHECK-CALL is medium pot-control
    villain_draw_pct: 0.00
    villain_air_pct: 0.22
  notes: "[NEW per MUST #33] Chain fires all 4 classes. Turn
          CHECK-CALL is textbook medium-made-pot-control. River bet
          is polarised but from a CHECK-heavy turn range → air moderated."
```

**Commit:** lands in commit 13 (corpus + tests).

### 3.7 MUST #34 — HIGH — MUST #6 helper cache + multiway branch spec

**File:** `river-rats-core/feature_extractor.py` — `_get_chain_narrowed_villain_range` helper

**(a) Cache contract — consume `_villain_range_narrowed` from `extract_range_composition` return dict:**

```python
def _get_chain_narrowed_villain_range(
    hero_pos: str,
    villain_pos: str,
    opener_pos: Optional[str],
    board_cards: List[str],
    facing_bet: bool,
    street_raw: str,
    action_history: Optional[List],
    num_opponents: int = 1,
    opponent_positions: Optional[List[str]] = None,
    bettor_pos: Optional[str] = None,
    # MUST #34(a): cache consumer — pre-computed range from extract_range_composition
    cached_range: Optional[Dict[str, float]] = None,
    cached_meta: Optional[Dict] = None,
) -> Tuple[Dict[str, float], Dict]:
    """MUST #6 + MUST #19 + MUST #34 — chain-narrowed villain range
    shared across composition + equity + partition + explain_hand.

    Cache contract: if cached_range is provided, return it directly
    (extract_range_composition already ran the chain for composition
    features; don't re-run for equity/partition).
    """
    if cached_range is not None:
        return cached_range, cached_meta or {}

    # HU path (first-compute)
    # ... existing body ...
```

`extract_all_features` threads the cached range through:
```python
# After range_feats = extract_range_composition(...)
_cached_vr = range_feats.get('_villain_range_narrowed')
_cached_meta = {
    'chain_steps': range_feats.get('_villain_range_chain_steps', []),
    'truncated': range_feats.get('_villain_range_chain_truncated', False),
    'surviving_weight': range_feats.get('_surviving_weight', 1.0),
    'villain_folded': range_feats.get('_villain_folded', False),
    'chain_overflowed': range_feats.get('_villain_chain_overflowed', False),
}
# Pass through to equity + partition via extract_all_features kwargs
```

Equity + partition call sites then pass `cached_range=_cached_vr, cached_meta=_cached_meta` — helper returns immediately.

**(b) Multiway branch — full spec per DECIDE and EXECUTE:**

**Decision: per-villain chain × MC trial loop.** Rationale:
- Composition features already compute per-villain (primary villain only); multiway equity MC loop samples from each opponent's range
- Consistency requires each opponent's range to be chain-narrowed by THAT opponent's action history (not just the primary's)
- Primary-villain-only approximation loses information when non-primary villain's actions constrain their range (e.g., non-primary checked through twice → range capped, affects equity)
- Cost: N × per-villain chain execution; narrowed ranges are smaller → MC per-trial is cheaper → net cost approximately flat or lower

**Implementation sketch:**
```python
def _get_chain_narrowed_villain_range(...):
    if num_opponents >= 2 and opponent_positions:
        # Multiway branch — per-villain chain narrowing
        merged = {}
        per_villain_ranges = {}
        for opp_pos in opponent_positions:
            opp_range = get_villain_range(hero_pos, opp_pos, opener_pos=opener_pos)
            # Chain narrow ONLY this opponent's actions
            if action_history:
                opp_history = [
                    e for e in action_history
                    if _normalize_action_entry(e).get('position', '').upper() == opp_pos.upper()
                ]
                # Only run chain if opponent acted post-flop
                if any(e.get('street', '').lower() in ('flop', 'turn', 'river')
                       for e in opp_history):
                    opp_range, _ = narrow_by_action_history(
                        full_range=opp_range,
                        board=board_cards,
                        action_history=opp_history,
                        villain_pos=opp_pos,
                        decision_street=STREET_NAME_MAP.get(street_raw, 'flop'),
                    )
            # Apply facing_bet filter only to the bettor
            is_bettor = (
                bettor_pos is not None
                and opp_pos.upper() == bettor_pos.upper()
            )
            if facing_bet and is_bettor:
                opp_range, _ = narrow_to_betting_range(
                    opp_range, board_cards, STREET_NAME_MAP.get(street_raw, 'flop')
                )
            per_villain_ranges[opp_pos] = opp_range

        # For composition/partition features (which read a single range), merge.
        # For equity MC (which samples per opponent), pass per_villain_ranges.
        # ... this helper returns both via meta ...
    else:
        # HU branch unchanged
```

The equity MC loop at `feature_extractor.py:790–806` then iterates over `per_villain_ranges.items()` instead of calling `get_villain_range` + `narrow_to_betting_range` inline.

**Perf benchmark plan (deferred to commit 5):**
- 10 representative multiway hands from v2.3.1 training CSV
- Measure: per-hand wall time, per-villain chain cost, MC iteration cost
- Expected: chain overhead ~5-10ms/villain × 2-3 villains = 10-30ms; MC speedup 5-15% on narrower ranges → net ~5-20ms per multiway hand
- If total extract_all_features time exceeds 500ms (current ~250ms): escalate to orchestrator

**Commit:** lands in commit 5 (MUST #6 + #19 + #30 scope).

### 3.8 MUST #35 — HIGH — Sidecar miss sentinel + validator

**Files:**
- `river-rats-core/calibration_exam.py` + `reference_evaluator.py` — sentinel in sidecar lookup
- `river-rats-core/tests/validate_sidecar_completeness.py` (NEW) — validator script

**Sentinel pattern:**
```python
# In calibration_exam.py (and parallel in reference_evaluator.py):
_SIDECAR_MISSING = object()   # unique sentinel; never present in dict

def _get_action_history_for_fixture(ref_id: str, hand_action_history: Optional[List]) -> List:
    """MUST #35: strict lookup. Missing sidecar entry raises in strict
    mode; silent-falls-back to empty list in legacy mode."""
    if hand_action_history:
        return hand_action_history   # JSONL record carries it natively
    entry = _CALIBRATION_ACTION_HISTORY.get(ref_id, _SIDECAR_MISSING)
    if entry is _SIDECAR_MISSING:
        import os
        strict = os.environ.get('STAGE4_STRICT_ACTION_HISTORY', '0').lower()
        if strict == 'raise':
            raise RuntimeError(
                f'MUST #35: sidecar entry missing for fixture {ref_id!r}. '
                f'Strict mode set. Fixture needs authored action_history '
                f'before Stage 4 re-label can proceed.'
            )
        elif strict in ('warn', '1'):
            import logging
            logging.getLogger(__name__).warning(
                'MUST #35: sidecar missing for %s; defaulting to empty '
                'list (chain will not fire for this fixture).', ref_id,
            )
        return []
    return entry
```

**Validator script (`validate_sidecar_completeness.py`):**
```python
"""MUST #35 validator — asserts sidecar completeness + well-formedness.

Usage:
    python3 river-rats-core/tests/validate_sidecar_completeness.py

Checks:
1. Every fixture ref_id in canonical labelled JSONLs has a sidecar entry
   in _CALIBRATION_ACTION_HISTORY or _REFERENCE_ACTION_HISTORY or
   _FB_ACTION_HISTORY_FULL.
2. Each sidecar entry is well-formed:
   - action_history is a non-empty list of tuples/dicts
   - streets are in {preflop, flop, turn, river} and monotonic
   - positions match the fixture's hero/villain_positions
   - actions are in {RAISE, CALL, FOLD, CHECK, BET} (plus check-raise as
     CHECK + RAISE pair on same street)
3. Fixture decision-street has action history up-to-but-not-including
   hero's current decision.

Returns: exit 0 if all valid; exit 1 with offender list if any fail.
"""
import sys
from pathlib import Path

def validate_all_sidecars():
    # ... implementation ...
    pass
```

**Run in CI:** validator is blocking — no Stage 4 re-label can run until validator exits 0.

**Commit:** lands in commit 6 (MUST #20) for calibration; commit 7 (MUST #22) for reference. Validator script in a separate commit right before Path (c) Phase 2 sidecar authoring.

### 3.9 MUST #36 — HIGH — CSV-header reconciliation

**File:** `river-rats-core/run_attention_experiments.py` (line 461)

Per MUST #31 spec above (§3.4), replaces tautological `X.shape[1] == 2 * len(FEATURE_COLUMNS)` assertion with:

```python
# MUST #36: CSV-header reconciliation (not tautological width assert)
import pandas as pd
csv_header = pd.read_csv(ATTENTION_CSV, nrows=0).columns.tolist()
missing = [c for c in col_names if c not in csv_header]
if missing:
    raise RuntimeError(
        f'MUST #36: CSV {ATTENTION_CSV!r} missing expected columns '
        f'{missing!r}. Vocabulary version drift likely; check '
        f'_attention_vocabulary_version audit column or re-assemble.'
    )
```

**Commit:** lands in commit 11B (MUST #27 + #31 + #36).

### 3.10 MUST #37 — HIGH — coaching/ sys.path side-effect audit

**Files:**
- Pre-delete audit of `coaching/feature_extractor.py:17` + `coaching/range_narrowing.py:41`

**Audit procedure (first 30 minutes of commit 9):**

```bash
# For each surviving coaching/* module, test import in isolation
for mod in coaching/*.py; do
    if [ "$mod" != "coaching/feature_extractor.py" ] && [ "$mod" != "coaching/range_narrowing.py" ]; then
        python3 -c "
import sys
sys.path.insert(0, 'river-rats-core')
# Simulate sys.path without feature_extractor/range_narrowing side effects
import $(basename $mod .py).coaching
" 2>&1 | grep -q "Error" && echo "BROKEN: $mod depends on deleted side effects"
    fi
done
```

Expected result: zero breaks (the 2 deleted files' side effects are `/mnt/project` and `/home/claude` paths, which are environment-specific not code-dependent). If any coaching/* module depends: either repoint the side-effect into a new init module OR defer that specific deletion.

**Commit:** lands in commit 9 (MUST #8 partial delete).

### 3.11 MUST #38 — MEDIUM — Frequency table coherence post-MUST-#17

**File:** `river-rats-core/range_narrowing.py` (lines ~137–146)

Full multi-line edit for coherence:

```python
# BEFORE:
RIVER_CHECKING_FREQUENCIES = {
    'nuts': 0.05,
    'strong_value': 0.10,
    'good_value': 0.45,
    'draw': 1.00,
    'medium_made': 0.92,
    'weak_made': 0.95,
    'bluff': 0.65,
    'air': 0.80,
}
RIVER_BETTING_FREQUENCIES['bluff'] = 0.20
RIVER_BETTING_FREQUENCIES['air']   = 0.10

# AFTER (MUST #17 + MUST #38 coherence):
RIVER_CHECKING_FREQUENCIES = {
    'nuts': 0.05,
    'strong_value': 0.10,
    'good_value': 0.45,
    'draw': 1.00,
    'medium_made': 0.85,   # MUST #17 — thin river value with medium pair exists
    'weak_made': 0.95,
    'bluff': 0.80,         # MUST #38 — mass parity with 3-way bet 0.20
    'air': 0.90,           # MUST #38 — mass parity with 3-way bet 0.10
}
# RIVER_BETTING_FREQUENCIES['bluff'/'air'] updates unchanged (already done)
```

Verify: bluff (0.80 check + 0.20 bet = 1.00), air (0.90 + 0.10 = 1.00), medium_made (0.85 + unspecified-bet — check table for bet freq; medium_made bet is typically low so 0.15 makes the pair sum to 1.00, consistent with "pure bluff-catcher").

**Commit:** lands in commit 10 (MUST #17 + #38 + #39 + #40).

### 3.12 MUST #39 — MEDIUM — KB §1.11 asymmetric FOLD-lean threshold

**File:** `knowledge/three_way_gto.md` §1.11

**Current (verified on origin):**
> If `(flush_draw_block_pct + straight_draw_block_pct) / 2 − nut_made_block_pct > 0.15`, **net FOLD lean**

**Updated per MUST #39:**
> If `(flush_draw_block_pct + straight_draw_block_pct) / 2 − nut_made_block_pct > 0.20`, **net FOLD lean** — threshold raised from 0.15 (CALL-lean threshold unchanged at 0.15 per asymmetric rationale: densification overstates FOLD confidence at solver benchmarks).

**Stage 2 KB edit.** Does not block Stage 3.5 code work (composition + equity chain is independent of labelling threshold), but must land before Stage 3 v3.2 prompt derives from KB §1.11.

**Commit:** lands in commit 10 (MUST #17 + #38 + #39 + #40).

### 3.13 MUST #40 — MEDIUM — Combo-draw use-max addendum

**File:** `knowledge/three_way_gto.md` §1.11

**Addendum text:**
> **Combo-draw addendum (MUST #40):** If hero holds a combo-draw blocker (a card that features in both `flush_draw_block_pct` and `straight_draw_block_pct` denominators simultaneously — e.g., a 9 of hearts on KsTsQh8h where villain's QhJh is blocked from both classes), use `max(flush_draw_block_pct, straight_draw_block_pct)` for the FOLD-lean delta rather than `mean(...)`. The mean over-counts combo-draw hands by factor 2 in the signal.

**Commit:** lands in commit 10 (co-edit with MUST #39).

### 3.14 MUST #41 — MEDIUM — Belt-and-braces count guard

**File:** `river-rats-core/range_narrowing.py` — `narrow_by_action_history`

Secondary guard below the mass floor:

```python
# After the mass-floor check:
if not warned_count_guard and cumulative_surviving >= 0.20 and len(current_range) < 5:
    import logging
    logging.getLogger(__name__).warning(
        'MUST #41: mass-concentrated-without-count-support. '
        'cumulative_surviving=%.3f but only %d hands survive. '
        'Inference brittle; flag for audit.',
        cumulative_surviving, len(current_range),
    )
    warned_count_guard = True
    # Does NOT truncate; audit-only flag
```

**Commit:** lands in commit 11 (MUST #41).

### 3.15 MUST #42 — MEDIUM — NaN render player-English

**File:** cross-stream → teaching terminal owns implementation

**Spec (for CONTENT_API v4 ticket):**
- HU folded villain: `"Villain folded earlier — no range to read."`
- Multiway with remaining live villain(s): `"Villain X folded; reading against villain Y only."` (name the remaining live)
- Over-narrow / truncated chain: `"Villain's line is too rare to read confidently — relying on equity alone."`
- NO partial-info rendering; never show "blocker_pct: N/A" as a feature line

**Ticket file:** `review/comms/TICKET_CONTENT_API_V4_NAN_RENDER_2026-04-22.md` (authored as MUST #43).

**Commit:** lands via MUST #43 ticket, not code.

### 3.16 MUST #43 — MEDIUM — CONTENT_API v4 cross-stream ticket

**New file:** `review/comms/TICKET_CONTENT_API_V4_NAN_RENDER_2026-04-22.md`

**Ticket contents (outline; full draft lands at commit time):**
```markdown
---
date: 2026-04-22
from: Builder (Stage 3.5 blueprint v2.2 cross-stream)
to: Teaching terminal · Orchestrator
re: CONTENT_API v4 — NaN render spec for Stage 3.5 sentinels
status: CROSS-STREAM TICKET — teaching implementation required to land before Stage 3.5 code commit 5 ships
---

# Ticket — CONTENT_API v4 NaN Render

## Background
Stage 3.5 emits NaN for composition + blocker features under 3 conditions:
  1. villain_folded=True (villain out of hand)
  2. villain_chain_overflowed=True (chain over-narrowed)
  3. mass-floor truncation (MUST #28 consolidates with #2)

## Contract
Teaching renders per MUST #42 player-English strings (above).
CONTENT_API v4 adds a schema field `range_rendering_mode`:
  - "normal" — standard range-composition prose
  - "folded" — villain folded rendering
  - "overflow" — line-too-rare rendering

## Test cases
  - Folded villain (HU) → single string
  - Folded villain (MW) → named-remaining-villain string
  - Over-narrowed chain → equity-only fallback string
  - Normal chain → unchanged

## Ship gate
Teaching CONTENT_API v4 MUST ship before Stage 3.5 commit 5
(CRIT #1 + HIGH #4 + NaN spec) can merge. Orchestrator gates.
```

**Commit:** ticket authored in commit 12 (co-lands with MUST #42 reference).

### 3.17 MUST #44 — CRITICAL (new) — Production format verification + scope

Per STEP 1.5 finding (§1.5 above):
- **Outcome (ii) — different schema.** Production uses `feature_attention: {feat: "PRIMARY"|"CONFIRMED"}`; pilot uses `attention_flags: {feat: 0|1}`.
- **MUST #26 patches both paths via bi-schema helper `_attention_value(...)`** (§3.2 spec).
- **Mandatory-tag list drives strict-gate** — v3.2 prompt (Stage 3 deliverable) will mandate tagging 4 new blockers + existing composition. Strict mode fires only on mandatory-but-missing; non-mandatory untagged → 0 silently.
- **`docs/ASSEMBLER_PATTERN.md` documents both schemas** (see §3.2).

MUST #44 spec complete; scope folded into MUST #26/#29 implementation.

---

## 4. Manifest version references

**Bumped throughout this amendment: v1.9 → v1.10.**

All references updated:
- Supplement v2.1 §7.1 cross-reference: v1.9 → v1.10
- Stage 4 gate citation: v1.10 (per origin)
- Manifest commit reference: `ce7ad3f` (CORRECTION commit; last written by orchestrator)

---

## 5. MUST inventory (definitive status)

| # | Source | Status | Patch site(s) | Commit |
|---|--------|--------|---------------|--------|
| 1 CRIT | Original | ACTIVE | feature_extractor.py 1651-1754 (Step 12/17) | 4 (merged) |
| 2 CRIT | Original + #9 | ACTIVE | feature_extractor.py 1168 + 3 pipelines | 2 |
| 3 HIGH | Original + #11/#12 | ACTIVE | range_narrowing.py pre-filter | 3 |
| 4 HIGH | Original + #10/#15/#28 | ACTIVE | feature_extractor.py 1169-1272 NaN spec | 4 (merged) |
| 5 HIGH | Original + #13 | ACTIVE | range_narrowing.py 434-843 mass thread | 1 |
| 6 CRIT | Reconciliation + #19/#30 | ACTIVE | 6 equity/explain_hand blocks + helper | 5 |
| 7 | Meta audit | COMPLETE | caller list in §3.3 | — |
| 8 HIGH | Reconciliation (narrowed) + #37 | ACTIVE | 2 coaching file deletions + audit | 9 |
| 9 → MUST #2 | Merged | — | — | — |
| 10 → MUST #4 | Merged | — | — | — |
| 11 → MUST #3 | Merged | — | — | — |
| 12 → MUST #3 | Merged | — | — | — |
| 13 → MUST #5 | Merged | — | — | — |
| 14 | Meta sequencing | COMPLETE | §3.5 above | — |
| 15 → MUST #4 | Merged | — | — | — |
| 16 | Regression guard | ACTIVE | M5 script assertion | 15 |
| 17 MEDIUM | Reconciliation | ACTIVE | range_narrowing.py freq table | 10 |
| 18 MEDIUM | Reconciliation | — superseded by #33 | — | — |
| 19 → MUST #6 | Merged | — | — | — |
| 20 CRIT | Research | ACTIVE | calibration_exam.py 279-298 | 6 |
| 21 Manifest | Research | LANDED (v1.10) | — | — |
| 22 CRIT | Research | ACTIVE | reference_evaluator.py 470-713 | 7 |
| 23 HIGH | Research | ACTIVE | train_sizing_model.py (verify) | 8 |
| 24 | Attention ticket | RETRACTED | — | — |
| 25 | Attention ticket | REFRAMED (Stage 3 deliverable) | — | — |
| 26 CRIT | Supplement + #29 + #44 | ACTIVE | assemble_pilot_data.py + assemble_v23_clean.py + docs/ASSEMBLER_PATTERN.md | 11A |
| 27 CRIT | Supplement + #31/#36 | ACTIVE | run_attention_experiments.py | 11B |
| 28 CRIT | Recon #2 | ACTIVE | feature_extractor.py truncation sentinel | 4 (merged) |
| 29 CRIT | Recon #2 | ACTIVE | re-verified BEFORE blocks; bi-schema helper | 11A |
| 30 CRIT | Recon #2 | ACTIVE | caller list +coaching/explain_hand.py | 1, 5 |
| 31 CRIT | Recon #2 | ACTIVE | feature-count 55→59 throughout | spans |
| 32 CRIT | Recon #2 | RESOLVED: (b) commits 4+5 merge | §3.5 | — |
| 33 HIGH | Recon #2 | ACTIVE | corpus T_J01/T_B05/T_J02 | 13 |
| 34 HIGH | Recon #2 | ACTIVE | helper cache + multiway spec | 5 |
| 35 HIGH | Recon #2 | ACTIVE | sentinel + validator script | 6, 7 |
| 36 HIGH | Recon #2 | ACTIVE | CSV-header reconciliation | 11B |
| 37 HIGH | Recon #2 | ACTIVE | sys.path side-effect audit | 9 |
| 38 MEDIUM | Recon #2 | ACTIVE | freq table bluff/air | 10 |
| 39 MEDIUM | Recon #2 | ACTIVE | KB §1.11 asymmetric FOLD-lean | 10 |
| 40 MEDIUM | Recon #2 | ACTIVE | KB §1.11 combo-draw use-max | 10 |
| 41 MEDIUM | Recon #2 | ACTIVE | count guard at 5 hands | 11 |
| 42 MEDIUM | Recon #2 | ACTIVE | MUST #43 ticket text | 12 |
| 43 MEDIUM | Recon #2 | ACTIVE | TICKET_CONTENT_API_V4 author | 12 |
| 44 CRIT | Amendment | ACTIVE | bi-schema helper in MUST #26 | 11A |

**Active: 37 (MUSTs #7, #14, #21, #24, #25, and merged duplicates don't count in the 42 active set).**

**Wait — let me reconcile the count precisely.**

Per directive:
- 25 active from v2 + supplement (original 5 + reconciliation 14 + research 4 + supplement 2)
- 16 from reconciliation #2 (#28-#43)
- 1 new (#44)
- Total 42 active

Reconciliation-merge accounting:
- MUSTs that are merged (not independent commits): #9→#2, #10→#4, #11→#3, #12→#3, #13→#5, #15→#4, #18→#33 supersession, #19→#6 — 8 merges
- MUSTs that are meta (no code): #7, #14, #21, #32 — 4 meta
- MUSTs retracted/reframed: #24, #25 — 2 inactive

Active code-editing MUSTs: 42 total − 2 inactive − 4 meta − 8 merged = 28 distinct patch groups landing in 16 commits.

(Discrepancy is because many MUSTs merge into shared commits rather than each getting independent ship.)

---

## 6. Questions for reconciliation pass #3

**Q-numbers 20–31 from blueprint v2 + supplement v2.1 resolved per directive.**

**Q32–Q35 resolved by orchestrator directive:** (C) hybrid both; fix-forward; MUST #44 verification first.

**NEW Q36–Q38 from this amendment:**

- **Q36 (architecture)** — MUST #34(b) multiway spec: per-villain chain × MC loop chosen. Any concern on perf (extract_all_features time may exceed 500ms)? If benchmark comes back above threshold, fallback to primary-villain-only; document as v2.5 perf work.
- **Q37 (GTO)** — MUST #33 T_J01 ship criterion (verdict-flip from FOLD to CALL or MIXED). Is that realistic for composition values 0.50/0.18/0.00/0.32? Or should the ship criterion be softer (e.g., oracle probability on CALL rises from <30% to >40%)? Practical pro said "numbers moving without verdict change = fix failed" but a mixed action may satisfy the spirit without a hard flip.
- **Q38 (red-team)** — MUST #44 outcome (ii) — bi-schema helper `_attention_value`. Does supporting BOTH `attention_flags` (pilot) AND `feature_attention` (production) in one function create a silent-schema-confusion risk? Alternative: separate assemblers per schema, force caller to know which schema their record uses.

---

## 7. Execution posture

**Amendment complete.** Supersedes supplement v2.1 at `3166759`. Blueprint v2 base at `8bb0f9f` unchanged.

Per STEP 3: commit + push this amendment. Orchestrator dispatches reconciliation pass #3.

If pass #3 surfaces new CRITICAL MUSTs: re-cut v2.3 amendment (NOT in-place patch; separate new document). Repeat steps 2-4 until clean.

If pass #3 lands clean: implementation per the 16-commit sequence in §3.5 begins.

No code edits. Standing by after push.
