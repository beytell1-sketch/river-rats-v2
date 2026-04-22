---
date: 2026-04-22
from: Builder (architect re-pass)
to: Orchestrator · Multi-agent reviewer panel (second reconciliation)
re: Stage 3.5 BLUEPRINT v2 — supersedes b1a9a91 wholesale
status: BLUEPRINT v2 — awaiting multi-agent reconciliation; no code edits yet
replaces: review/comms/BUILDER_V24_STAGE35_BLUEPRINT_2026-04-21.md (b1a9a91)
sources:
  - review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_BLUEPRINT_2026-04-21.md (11fe501)
  - review/comms/BUILDER_V24_STAGE35_RESEARCH_FINDINGS_2026-04-21.md (ae6160b)
  - Manifest v1.8 (e7dd240) — Stage 4 gate hardened
  - Orchestrator directive 2026-04-22 — Q15–Q19 resolutions
scope: 23 MUSTs (original 5 + reconciliation 14 + research 4) + Q18/Q19 data-source plan
---

# Stage 3.5 — Blueprint v2

Single-artifact blueprint replacing b1a9a91 per orchestrator REWORK
directive. 23 MUSTs organized by severity, with BEFORE/AFTER patches
verified at HEAD `e7dd240`, cross-MUST overlap map, data-source plan
for labelling-pipeline consumers, coaching/ partial-deletion plan,
frequency-table tweaks, re-sequenced commit order, and M4/M5
re-audit specs.

**Orchestrator redirects already incorporated:**
- Q15 — MUST #8 narrowed to just 2 files (coaching/feature_extractor.py + coaching/range_narrowing.py)
- Q16 — MUST #16 downgraded to regression guard
- Q17 — Stage 4 gate hardened in manifest v1.8; blueprint cross-references
- Q18/Q19 — Path (c) chosen: schema extension + authored sidecar table (per §18)

No code edits until this blueprint passes its own multi-agent
reconciliation pass.

---

## Table of contents

1. MUST priority summary table (23 MUSTs)
2. Original 5 MUSTs (with reconciliation tweaks)
   - 2.1 HIGH #5 — `surviving_weight` mass threading + MUST #13 floor
   - 2.2 CRITICAL #2 — Strict `_action_history` gate + MUST #9 pipeline unswallow
   - 2.3 HIGH #3 — Check-raise pre-filter extended for MUST #11 + MUST #12
   - 2.4 CRITICAL #1 — Blocker features consume chain
   - 2.5 HIGH #4 — Folded-villain sentinel + MUST #10 NaN spec + MUST #15 over-narrow NaN
3. Reconciliation MUSTs
   - 3.1 MUST #6 — Equity-feature chain inheritance + MUST #19 explain_hand
   - 3.2 MUST #7 — Caller list (complete)
   - 3.3 MUST #8 — Partial coaching/ deletion
   - 3.4 MUST #14 — Re-sequenced commit order
   - 3.5 MUST #17 — Frequency-table tweak
   - 3.6 MUST #18 — Corpus reauthoring (T_J01 + T_B05)
4. Research MUSTs
   - 4.1 MUST #20 — calibration_exam.py chain-clean
   - 4.2 MUST #21 — Stage 4 gate (manifest-level, no code)
   - 4.3 MUST #22 — reference_evaluator.py chain-clean
   - 4.4 MUST #23 — train_sizing_model.py chain-clean (verify)
5. Q18/Q19 data-source resolution — path (c) schema + sidecar
6. Cross-MUST edit-overlap map
7. Unit test corpus — 81 cases + 4 coverage-gap additions
8. M4 re-audit scope expansion
9. M5 anchor regression + MUST #16 guard
10. Observability hooks (consolidated)
11. Commit sequence (15 commits)
12. STOP conditions + verification items in-flight
13. Questions requiring orchestrator sign-off before implementation
14. Reviewer role assignments

---

## 1. MUST priority summary

| # | Severity | File | Line range / target | Summary |
|---|----------|------|---------------------|---------|
| 1 CRIT | Original | `feature_extractor.py` | 1651–1754 | Blocker features consume chain-narrowed range |
| 2 CRIT | Original + MUST #9 | `feature_extractor.py` + 3 pipelines | 1167–1188; parallel:81; incremental:105; gauntlet_v5:188,226 | Strict-raise gate + pipeline unswallow |
| 3 HIGH | Original + #11 + #12 | `range_narrowing.py` | 695–843 | Pre-filter collapses same-street (check, bet/raise/call) and triple sequences |
| 4 HIGH | Original + #10 + #15 | `feature_extractor.py` + teaching/gto_model/SHAP | 1169–1195, 1262–1272 + downstream | Folded-villain sentinel; NaN spec across 4 layers; over-narrow NaN-flag |
| 5 HIGH | Original + #13 | `range_narrowing.py` | 434–636, 695–843 | Narrow_* return mass; cumulative surviving mass; floor 10% / WARN 20% |
| 6 CRIT | Reconciliation + #19 | `feature_extractor.py` + `explain_hand.py` | 500–505, 605–617, 790–806, 823–829; explain_hand:261–264, 326–329 | Equity + partition + explain_hand chain inheritance |
| 7 — | Meta (audit) | — | — | Caller list complete (see §3.2) |
| 8 HIGH | Reconciliation (narrowed) | `coaching/` | delete 2 files | Partial coaching deletion — only confirmed-dead files |
| 9 → see MUST #2 | — | — | — | Merged into CRIT #2 |
| 10 → see MUST #4 | — | — | — | Merged into HIGH #4 |
| 11 → see MUST #3 | — | — | — | Merged into HIGH #3 |
| 12 → see MUST #3 | — | — | — | Merged into HIGH #3 |
| 13 → see MUST #5 | — | — | — | Merged into HIGH #5 |
| 14 Meta | Reconciliation | — | — | Commit sequence (§11) |
| 15 → see MUST #4 | — | — | — | Merged into HIGH #4 |
| 16 Regression guard | Reconciliation (downgraded) | `run_v231_anchor_recheck_stage35.py` | assert block | Chain_steps non-empty per anchor row |
| 17 MEDIUM | Reconciliation | `range_narrowing.py` | 142 | RIVER_CHECKING_FREQUENCIES.medium_made 0.92 → 0.85 |
| 18 MEDIUM | Reconciliation | `review/tests/range_narrowing_test_corpus_2026-04-20.yaml` | T_J01, T_B05 | Expected-value reauthoring |
| 19 → see MUST #6 | — | — | — | Merged into MUST #6 |
| 20 CRIT | Research | `calibration_exam.py` | 279–298 + ReferenceHand dataclass | Labelling display plumbs _action_history |
| 21 Manifest | Research | `RELEASE_MANIFEST.yaml` | Stage 4 gate | Landed in v1.8 (e7dd240); no code action |
| 22 CRIT | Research | `reference_evaluator.py` | 470–489, 693–713 | Baseline eval plumbs _action_history |
| 23 HIGH | Research | `train_sizing_model.py` | ~140 | Sizing model plumbs _action_history (pending verification) |

**Merged counting:** #9 into #2; #10/#15 into #4; #11/#12 into #3; #13
into #5; #19 into #6. Net distinct patch groups: 12.

---

## 2. Original 5 MUSTs (with reconciliation tweaks)

### 2.1 HIGH #5 — Surviving-weight mass threading + MUST #13 floor

**File:** `river-rats-core/range_narrowing.py`
**Line range:** 434–636 (each `narrow_*` function), 695–843 (`narrow_by_action_history`)

#### Why this MUST exists

`surviving_weight` is currently computed as `len(current_range) / len(full_range)` (hand count ratio) at line 839. A 3-hand range at uniform freq 0.33 passes the count-floor at line 820 (`len(current_range) < 3`) but is semantically collapsed. True surviving weight is the ratio of un-normalized probability MASS across chain steps to the original input mass. Each `narrow_*` function currently re-normalises and discards the un-normalized mass.

Per MUST #13 (research literature on chain compounding error, 1.3–1.6x per street): the 5% floor is too permissive — at <10% cumulative mass the distribution is dominated by the last-applied filter, effectively collapsing to single-street behavior. Threshold tightens to **10% (truncate)** with **20% WARN (log only)**.

#### BEFORE

**`narrow_to_betting_range` (line 434–495), `narrow_to_checking_range` (498–559), `narrow_to_continuing_range` (582–636):** each ends with:

```python
if total_weight > 0:
    for hand in out_range:
        out_range[hand] /= total_weight

return out_range
```

`total_weight` (un-normalized) is discarded.

**`narrow_by_action_history` (line 578 + 836–842):**

```python
_STAGE35_WEIGHT_FLOOR_PCT = 0.05

# ...
meta = {
    'surviving_weight': float(len(current_range)) / max(1, len(full_range)),
    'chain_steps': steps,
    'truncated': truncated,
}
```

And the safety rail at line 820:

```python
if len(current_range) < 3:
    # ... revert + truncated = True
```

#### AFTER

**Step A — each `narrow_*` returns `(range, surviving_fraction)`:**

```python
def narrow_to_betting_range(
    full_range: Dict[str, float],
    board: List[str],
    street: str = 'flop',
) -> Tuple[Dict[str, float], float]:
    """...
    Returns:
        (betting_range, surviving_fraction)
        surviving_fraction: fraction of input PROBABILITY MASS retained
            after applying category × frequency. Not count; mass.
            Threaded through narrow_by_action_history for true
            cumulative surviving-mass computation per MUST #13.
    """
    if not full_range or not board:
        return full_range, 1.0

    original_weight = sum(f for f in full_range.values() if f > 0)
    if original_weight <= 0:
        return full_range, 0.0

    # ... existing per-hand loop unchanged; accumulates total_weight ...

    surviving_mass_fraction = total_weight / original_weight if original_weight > 0 else 0.0

    if total_weight > 0:
        for hand in betting_range:
            betting_range[hand] /= total_weight

    return betting_range, surviving_mass_fraction
```

Identical treatment for `narrow_to_checking_range` and `narrow_to_continuing_range`.

**Step B — `narrow_by_action_history` threads cumulative mass + tightened floor:**

```python
# --- constants (top of module) ---
# MUST #13: tighter thresholds per chain-compounding literature
_STAGE35_WEIGHT_FLOOR_PCT = 0.10   # truncate below this; was 0.05
_STAGE35_WEIGHT_WARN_PCT  = 0.20   # log WARN below this; no truncation


def narrow_by_action_history(...):
    # ... existing setup ...
    cumulative_surviving = 1.0
    warned_at_20 = False

    for street in STREET_ORDER:
        # ... existing same-street-exclusion + villain_street_actions collection ...

        # MUST #3 extension: pre-filter same-street (check, bet/raise/call)
        # and generic-collapse sequences. See §2.3.
        villain_street_actions = _collapse_same_street_sequence(villain_street_actions)

        for act in villain_street_actions:
            narrow_class = _action_to_narrow(act.get('action', ''))
            if narrow_class == 'fold':
                return {}, {
                    'surviving_weight': 0.0,
                    'chain_steps': steps + [f'{street}:FOLD'],
                    'truncated': False,
                }
            if narrow_class == 'bet':
                current_range, step_surv = narrow_to_betting_range(
                    current_range, street_board, street
                )
                steps.append(f'{street}:BET')
            elif narrow_class == 'check':
                current_range, step_surv = narrow_to_checking_range(
                    current_range, street_board, street
                )
                steps.append(f'{street}:CHECK')
            elif narrow_class == 'call':
                current_range, step_surv = narrow_to_continuing_range(
                    current_range, street_board, street
                )
                steps.append(f'{street}:CALL')
            else:
                continue

            cumulative_surviving *= step_surv

            # Empty-chain fallback unchanged
            if not current_range:
                # ... revert ...
                truncated = True
                break

            # MUST #13: mass-based floor + WARN
            if cumulative_surviving < _STAGE35_WEIGHT_FLOOR_PCT:
                import logging
                logging.getLogger(__name__).warning(
                    'narrow_by_action_history: cumulative surviving mass '
                    '%.3f below floor %.2f after %s; reverting to last valid',
                    cumulative_surviving, _STAGE35_WEIGHT_FLOOR_PCT,
                    steps[-1] if steps else '?',
                )
                current_range = last_valid_range
                truncated = True
                break

            if not warned_at_20 and cumulative_surviving < _STAGE35_WEIGHT_WARN_PCT:
                import logging
                logging.getLogger(__name__).info(
                    'narrow_by_action_history: cumulative surviving mass '
                    '%.3f below WARN %.2f after %s (still continuing)',
                    cumulative_surviving, _STAGE35_WEIGHT_WARN_PCT,
                    steps[-1] if steps else '?',
                )
                warned_at_20 = True

            last_valid_range = dict(current_range)

        if truncated:
            break

    meta = {
        'surviving_weight': cumulative_surviving,   # true mass 0.0–1.0
        'chain_steps': steps,
        'truncated': truncated,
    }
    return current_range, meta
```

Delete the old count-based `if len(current_range) < 3` safety rail — the mass-based rail replaces it.

#### Signature change + affected callers (23 total, per MUST #7)

Mechanical tuple-unpack at each root call site:

```python
# BEFORE: v_range = narrow_to_betting_range(v_range, board, street)
# AFTER:  v_range, _ = narrow_to_betting_range(v_range, board, street)
```

**Root sites (12 edits + 5 test-file edits):**
- `feature_extractor.py:503, 617, 805, 828, 1193` — tuple unpack (5 sites)
- `feature_extractor.py:1669` — **DELETED** by CRIT #1 (no action needed here)
- `range_narrowing.py:791, 794, 797` — internal to `narrow_by_action_history` (covered in Step B above)
- `range_narrowing.py:875, 885` — `test_narrowing` demo function; discard the mass
- `explain_hand.py:264, 329` — tuple unpack (2 sites); **these are MUST #19-merged-into-MUST-#6 sites; see §3.1**
- `tests/test_range_narrowing_stage35.py:288, 294, 296, 304, 307` — 5 test-file edits

**Coaching sites (9 edits) — deferred to MUST #8 partial-delete commit.** The two files with these call sites (`coaching/feature_extractor.py`, `coaching/range_narrowing.py`) are deleted wholesale; no tuple-unpack edits needed on them. This simplifies HIGH #5 scope substantially vs. blueprint v1.

#### Test plan

- **Corpus:** all 81 cases (direction test; surviving_weight within bounds)
- **Targeted unit test:** `test_surviving_weight_is_mass_not_count` — synthetic 10-hand range where count-fraction and mass-fraction diverge. Assert `meta['surviving_weight']` reflects mass.
- **MUST #13 threshold test:** `test_mass_floor_truncates_at_10pct` — deep-chain shape (analogous to T_K20) synthetic distribution at 7% cumulative mass. Pre-MUST-#13: passes. Post: truncates.
- **MUST #13 WARN-only test:** synthetic at 15% cumulative mass. Asserts log captures WARN but chain continues.

---

### 2.2 CRITICAL #2 — Strict `_action_history` gate + MUST #9 pipeline unswallow

**Files:** `river-rats-core/feature_extractor.py` (emit point), plus 3 training pipelines (unswallow points).

#### Why this MUST exists

- CRIT #2: When `_action_history` is absent on the hand dict, `extract_range_composition` at line 1172 falls through silently to pre-Stage-3.5 behavior. Training-data pipelines don't populate the field. Stage 4 re-label produces mixed distribution → v2.3.2-class corruption.
- MUST #9: Even if CRIT #2 emits `RuntimeError`, training pipelines wrap `extract_all_features(hand)` in blanket `except Exception:` that swallows the error. Loud-fail becomes silent counter-increment. CRIT #2 becomes fiction without MUST #9.

Both MUSTs land in the same commit because neither works without the other.

#### AFTER — part 1: `extract_range_composition` emits env-gated RuntimeError

Insert at line 1168 (immediately before `if action_history:`):

```python
# CRIT #2 — loud surfacing when action_history is missing.
# Env-gated so live-play callers (bridge always populates _action_history)
# don't spam logs, while Stage 4 re-label + training paths force a raise.
#
# STAGE4_STRICT_ACTION_HISTORY semantics:
#   unset / "0" — silent fallback (legacy-compat for read-only display paths)
#   "warn"     — logging.WARNING per call
#   "raise"    — RuntimeError (training / re-label)
_action_history_present = bool(action_history)
if not _action_history_present:
    _strict = os.environ.get('STAGE4_STRICT_ACTION_HISTORY', '0').lower()
    if _strict == 'raise':
        raise RuntimeError(
            f'extract_range_composition: action_history missing at '
            f'board={board_cards!r} hero={hero_pos} villain={villain_pos}. '
            f'STAGE4_STRICT_ACTION_HISTORY=raise is set. This is the '
            f'v2.3.2-class silent-fallback failure mode; fix the caller '
            f'to populate _action_history before re-running.'
        )
    elif _strict in ('warn', '1'):
        import logging
        logging.getLogger(__name__).warning(
            'extract_range_composition: action_history MISSING — falling '
            'back to pre-Stage-3.5 single-street behavior. '
            'board=%r hero=%s villain=%s', board_cards, hero_pos, villain_pos,
        )
```

`_action_history_present` propagates through the return dict (see §2.5 return-block changes).

#### AFTER — part 2: pipeline unswallow (MUST #9)

Three pipelines identified by research (§3 of RESEARCH_FINDINGS):

**`extract_features_parallel.py:75–84`:**
```python
for hand in hands:
    try:
        feat = extract_all_features(hand)
        action_val = ACTION_MAP.get(feat.get('action'), -1)
        if action_val == -1:
            errors += 1
            continue
        row = []
        for col in MODEL_COLUMNS[:-2]:   # features only (MUST #9b below)
            row.append(float(feat[col]))
        row.append(action_val)
        row.append(int(feat.get('_action_history_present', 0)))  # audit
        rows.append(row)
    except RuntimeError:
        raise   # Let CRIT #2 strict propagate
    except Exception:
        errors += 1
```

**`extract_incremental.py:82–107`:**
```python
try:
    parsed = parse_pokerbench_line(line)
    if not parsed:
        errors += 1
        continue
    feat = extract_all_features(parsed)
    vec = [float(feat.get(c, 0.0)) for c in FEATURE_COLUMNS]
    # ... action / size_bucket as before ...
    rows.append(vec + [action, size_bucket, int(feat.get('_action_history_present', 0))])
except RuntimeError:
    raise
except Exception as e:
    errors += 1
```

**`gauntlet_v5_37feat.py:178–226`** — two loop sites, identical pattern at both:
```python
except RuntimeError:
    raise
except Exception as e:
    errors += 1
```

#### AFTER — part 3: training-CSV schema bump (audit column)

**`extract_features_parallel.py:29–41`** MODEL_COLUMNS append:
```python
MODEL_COLUMNS = [
    # ... existing 37 feature columns unchanged ...
    'action',
    '_action_history_present',   # audit column, not a model feature
]
```

The model trainer reads `FEATURE_COLUMNS` (v-specific), not the CSV header list. Adding a column at the end is backward-compatible with existing model-loading code.

**`extract_incremental.py:59`:**
```python
header = list(FEATURE_COLUMNS) + ['action_label', 'size_bucket', '_action_history_present']
```

#### Signature changes + callers

- `extract_range_composition` return dict — adds `_action_history_present: bool`. See §2.5's consolidated return-block.
- MODEL_COLUMNS / header bumps — additive only; no reader code breaks.
- No function signature changes.

#### Test plan

- New unit test `test_stage4_strict_action_history_raises` — set env var, call `extract_range_composition` without action_history, assert RuntimeError.
- `test_stage4_strict_action_history_warns` — env=warn, assert log captured.
- `test_pipeline_unswallow_runtime_error` — mock extract_all_features to raise RuntimeError, call into extract_features_parallel's process_chunk, assert propagation.
- Corpus case `T_I01_missing_action_history` (already in corpus) — gates the behavior.

#### Q18/Q19 dependency

**Training pipelines will HARD-FAIL for Stage 4 re-label** once MUST #2 + #9 land and strict is set. Per path (c) chosen in §5: `_action_history` sidecar authoring is required BEFORE strict-raise can be safely set for Stage 4. See §5 for the authoring plan.

Temporarily between CRIT #2 landing and the sidecar completing, Stage 4 re-label is blocked by design. This matches MUST #21's Stage 4 gate.

---

### 2.3 HIGH #3 — Check-raise pre-filter extended (+ MUST #11 + MUST #12)

**File:** `river-rats-core/range_narrowing.py`
**Line range:** 695–843 (`narrow_by_action_history`), plus new helper `_collapse_same_street_sequence`

#### Why this MUST exists

- HIGH #3 baseline: applying CHECK × BET sequentially produces inverted composition for check-raise lines (mediums up from CHECK step, under-weighted by BET normalisation; IRL check-raise is 60–80% nuts).
- MUST #11: same logic applies to CHECK-CALL (mediums doubly weighted). Practical + GTO + research converge.
- MUST #12: generic safety — sequences with >2 villain actions on a single street (e.g., check-bet-raise triples) currently apply all narrowings in order, compounding the bias.

Resolution: collapse per-street sequences to the LAST decision-bearing action. Specifically, skip CHECK when followed by any same-street BET/RAISE/CALL. Honour FOLD as terminal.

#### BEFORE (`range_narrowing.py:763–801`)

```python
for street in STREET_ORDER:
    if street == decision_street:
        break

    villain_street_actions = [
        _normalize_action_entry(e)
        for e in action_history
        if _normalize_action_entry(e).get('street') == street
           and _normalize_action_entry(e).get('position') == villain_pos.upper()
    ]

    if not villain_street_actions:
        continue

    street_board = _street_board(board, street)

    for act in villain_street_actions:
        # ... apply narrow per action class ...
```

#### AFTER

New helper `_collapse_same_street_sequence` + call site change at the loop:

```python
def _collapse_same_street_sequence(actions: List[Dict]) -> List[Dict]:
    """MUST #3 + MUST #11 + MUST #12 — collapse same-street villain
    action sequences to the last decision-bearing action.

    Reasoning (convergent from GTO / practical / research reviews):
      - check-bet (check-raise line): CHECK is a sandbag, RAISE is the
        concentrated-value action. The pair is semantically one action;
        chaining both produces inverted composition.
      - check-call: CHECK is passive, CALL is the continuing action.
        Chaining doubly weights mediums.
      - check-check-bet or deeper triples: all prior CHECKs are
        sandbagged; only the final aggressive/continuing move matters.
      - FOLD terminates the sequence — villain's out of the hand.

    Collapse rule:
      - Walk the sequence in order.
      - On encountering CHECK followed by {BET, RAISE, CALL} on same
        street: drop the CHECK (and any earlier CHECKs in the run),
        keep the decision-bearing action.
      - On FOLD: keep FOLD, drop everything after (shouldn't occur in
        a single same-street sequence, but safe).

    Returns a filtered list preserving action metadata for the
    downstream narrow-class branch.
    """
    if len(actions) <= 1:
        return list(actions)

    # Convert to narrow classes for inspection, but keep the original
    # dicts (the caller needs street/position/action for labeling).
    classes = [_action_to_narrow(a.get('action', '')) for a in actions]

    # Find the LAST decision-bearing action (bet/call/fold).
    # Everything before it that's a CHECK gets dropped.
    last_decisive_idx = -1
    for i, cls in enumerate(classes):
        if cls in ('bet', 'call', 'fold'):
            last_decisive_idx = i

    if last_decisive_idx < 0:
        # All CHECKs (e.g., check-through sequence). Keep the last CHECK
        # — that IS the decision on this street.
        return [actions[-1]] if actions else []

    # Keep the decisive action + anything AFTER it (defensive — usually
    # nothing follows, but don't silently drop). Drop preceding CHECKs.
    kept = [actions[last_decisive_idx]] + actions[last_decisive_idx + 1:]
    return kept
```

Call site (line 778, between `villain_street_actions` construction and the action loop):

```python
    # MUST #3 / #11 / #12: collapse same-street multi-action sequences
    # to the decision-bearing action before narrowing.
    villain_street_actions = _collapse_same_street_sequence(villain_street_actions)
```

#### Alternative (a) documented in-line

```python
# ALTERNATIVE (a) — check-raise-specific frequency table. Richer, but
# requires introducing a new CHECK_RAISE_BETTING_FREQUENCIES category
# and solver-grounded calibration. Deferred to v2.5 unless GTO reviewer
# redirects during multi-agent reconciliation pass #2. See TICKET_V25_
# PRO_LEVEL_NARROWING_GAPS_2026-04-20.md.
```

#### Signature changes

None external. Internal helper added.

#### Test plan

- Corpus B-section (`T_B01`–`T_B05`) — check-raise shapes. `T_B01`, `T_B04` are explicit check-raise; post-fix composition should be ~60–80% nuts+strong_value.
- Corpus C-section selections exercising check-call (`T_C01` through `T_C07` include call-continuations after earlier CHECKs).
- Corpus K-section: `T_K04_checkraise_then_call_turn_bet`, `T_K11_checkraise_fold_flop_river_na`, `T_K20_deep_chain_flop_bet_turn_raise_river_bet`.
- New unit test `test_collapse_check_call_same_street` — synthetic (CHECK, CALL) pair on flop, assert only CALL step fires.
- New unit test `test_collapse_triple_check_check_bet` — synthetic (CHECK, CHECK, BET), assert only BET step fires.
- New unit test `test_collapse_pure_check_through` — (CHECK, CHECK), assert final CHECK remains (don't lose check-through signal).

---

### 2.4 CRITICAL #1 — Blocker features consume chain

**File:** `river-rats-core/feature_extractor.py`
**Line range:** 1651–1754 (Step 12 + Step 17)

#### Why this MUST exists

`extract_range_composition` (line 1116) produces a chain-narrowed villain range for composition features. But Step 12 (`flush_block_pct`) at line 1664 and Step 17 (4 new v2.4 blocker features) at line 1742 re-fetch `get_villain_range()` and apply only single-street `narrow_to_betting_range`. The 5 blocker features are computed against an un-chained range while composition features on the same hand see the chained range — SHAP-vs-action-contradiction class bug. Teaching displays both.

#### BEFORE (lines 1651–1754, Step 12 + Step 17 blocks)

```python
# Step 12: New features 46-48 (flush_block_pct, overcard_outs,
#          improvement_probability)
_s12_hero_pos = features.get('_hero_pos_raw', 'BTN')
_s12_villain_pos = features.get('_villain_pos_raw', 'BB')
_s12_facing_bet = bool(features.get('facing_bet', 0))
_s12_street_raw = features.get('_street_raw', 'f')
_s12_opener_pos = hand.get('_opener_position', None)
_s12_v_range = get_villain_range(
    _s12_hero_pos, _s12_villain_pos, opener_pos=_s12_opener_pos
)
if _s12_facing_bet and _s12_v_range:
    _s12_street_name = STREET_NAME_MAP.get(_s12_street_raw, 'flop')
    _s12_v_range = narrow_to_betting_range(
        _s12_v_range, board_cards, _s12_street_name
    )

# ... board suit counts ...

features[F.FLUSH_BLOCK_PCT] = compute_flush_block_pct(
    hero_cards, board_cards, _s12_v_range, _s12_suit_counts
)
# ... overcard_outs / improvement_probability ...

# Step 17: v2.4 P1 blocker-direction features (56-59)
try:
    from blocker_features import (
        compute_nut_flush_block,
        compute_block_percentages,
    )
    features[F.NUT_FLUSH_BLOCK] = compute_nut_flush_block(
        hero_cards, board_cards
    )
    _s17_block = compute_block_percentages(
        hero_cards, board_cards, _s12_v_range,
    )
    features[F.FLUSH_DRAW_BLOCK_PCT] = _s17_block['flush_draw_block_pct']
    features[F.STRAIGHT_DRAW_BLOCK_PCT] = _s17_block['straight_draw_block_pct']
    features[F.NUT_MADE_BLOCK_PCT] = _s17_block['nut_made_block_pct']
except Exception:
    features[F.NUT_FLUSH_BLOCK] = 0
    features[F.FLUSH_DRAW_BLOCK_PCT] = 0.0
    features[F.STRAIGHT_DRAW_BLOCK_PCT] = 0.0
    features[F.NUT_MADE_BLOCK_PCT] = 0.0
```

#### AFTER — two-step change

**Step A:** `extract_range_composition` publishes the chain-narrowed range in its return dict (consolidates with §2.5's folded-villain + CRIT #2's action_history_present additions — single return block):

```python
return {
    # Existing scalar features
    '_villain_top_pair_plus_pct': tp_pct,
    '_villain_draw_pct': draw_pct,
    '_villain_air_pct': air_pct,
    '_villain_medium_made_pct': medium_made_pct,
    '_villain_range_capped': range_capped,
    '_board_favour': board_favour,
    # Stage 3.5 metadata
    '_villain_range_chain_steps': chain_steps,
    '_villain_range_chain_truncated': chain_truncated,
    '_surviving_weight': chain_surviving_weight,      # from HIGH #5
    # CRIT #1 — publish narrowed range for Step 12 + Step 17 + downstream
    '_villain_range_narrowed': v_range,
    # HIGH #4 — folded sentinel
    '_villain_folded': villain_folded,
    # HIGH #4 / MUST #15 — over-narrow sentinel
    '_villain_chain_overflowed': chain_overflowed,
    # CRIT #2 — provenance
    '_action_history_present': _action_history_present,
}
```

**Step B:** Step 12 + Step 17 consume the narrowed range. See §2.5 for the NaN-flag branch for folded-villain (MUST #10 interaction). Non-NaN branch:

```python
# Step 12 + 17: features that measure blocker effects against villain's
# range. Consume the SAME chain-narrowed range as composition features
# (propagated through _villain_range_narrowed by extract_range_composition).
# No independent range reconstruction — all villain-range-derived features
# share one source of truth. CRIT #1 fix.
hero_cards = features.get('_hero_cards', [])
board_cards = features.get('_board_cards', [])

_villain_folded = bool(features.get('_villain_folded', False))
_villain_chain_overflowed = bool(features.get('_villain_chain_overflowed', False))
_v_range_narrowed = features.get('_villain_range_narrowed', None) or {}

# Board suit counts
if board_cards:
    _s12_analysis = analyze_board_cached(tuple(board_cards))
    _s12_suit_counts = _s12_analysis.suit_counts
else:
    _s12_suit_counts = {}

if _villain_folded or _villain_chain_overflowed:
    # MUST #10 / #15: NaN-flag the blocker-dependent features.
    # Teaching layer skips their display; training drops these rows
    # from blocker-feature columns (see §2.5 NaN spec).
    features[F.FLUSH_BLOCK_PCT] = float('nan')
    features[F.NUT_FLUSH_BLOCK] = 0   # boolean: hero can't block vs folded/overflow; keep 0
    features[F.FLUSH_DRAW_BLOCK_PCT] = float('nan')
    features[F.STRAIGHT_DRAW_BLOCK_PCT] = float('nan')
    features[F.NUT_MADE_BLOCK_PCT] = float('nan')
else:
    features[F.FLUSH_BLOCK_PCT] = compute_flush_block_pct(
        hero_cards, board_cards, _v_range_narrowed, _s12_suit_counts
    )
    try:
        from blocker_features import (
            compute_nut_flush_block,
            compute_block_percentages,
        )
        features[F.NUT_FLUSH_BLOCK] = compute_nut_flush_block(
            hero_cards, board_cards
        )
        _s17_block = compute_block_percentages(
            hero_cards, board_cards, _v_range_narrowed,
        )
        features[F.FLUSH_DRAW_BLOCK_PCT] = _s17_block['flush_draw_block_pct']
        features[F.STRAIGHT_DRAW_BLOCK_PCT] = _s17_block['straight_draw_block_pct']
        features[F.NUT_MADE_BLOCK_PCT] = _s17_block['nut_made_block_pct']
    except Exception:
        # Defensive defaults (not NaN — this is a computation failure,
        # not a semantic "not applicable").
        features[F.NUT_FLUSH_BLOCK] = 0
        features[F.FLUSH_DRAW_BLOCK_PCT] = 0.0
        features[F.STRAIGHT_DRAW_BLOCK_PCT] = 0.0
        features[F.NUT_MADE_BLOCK_PCT] = 0.0

# overcard_outs + improvement_probability are hero-only; always compute
features[F.OVERCARD_OUTS] = compute_overcard_outs(
    hero_cards, features.get('high_card_rank', 14)
)
features[F.IMPROVEMENT_PROBABILITY] = compute_improvement_probability(
    hero_cards, board_cards, features.get('hand_category', 0)
)
```

#### Signature changes + affected callers

- `extract_range_composition` return dict gains 4 keys: `_villain_range_narrowed`, `_villain_folded`, `_villain_chain_overflowed`, `_action_history_present`, `_surviving_weight`. Additive; existing `features.update(range_feats)` absorbs them.
- `compute_flush_block_pct`, `compute_block_percentages`, `compute_nut_flush_block` — signatures unchanged.
- Step 12 locals `_s12_hero_pos`, `_s12_villain_pos`, `_s12_facing_bet`, `_s12_street_raw`, `_s12_opener_pos`, `_s12_v_range` — deleted.

#### Test plan

- New integration test `test_blocker_features_use_chain_narrowed_range` (in `test_range_features.py`):
  - Build hand_dict with `_action_history` = [preflop RAISE, preflop CALL, flop CHECK, flop CHECK, turn CHECK, turn CALL].
  - Compute FLUSH_BLOCK_PCT via current (post-fix) code.
  - Compute an expected reference by manually building the chain-narrowed range and calling `compute_flush_block_pct` externally.
  - Assert they match.
  - Also compute the pre-fix bypass value (un-chained range + single-street betting filter) and assert it DIFFERS from the chained value on at least one hand shape.
- Corpus `T_J03_owner_conceptual_blocker_mid_pair_flush_blocker` — end-to-end realism check on owner-sourced shape.
- M4 re-audit expected to surface ~455 rows where chain-consumed vs bypass values differ (§8).

---

### 2.5 HIGH #4 — Folded-villain sentinel + MUST #10 NaN spec + MUST #15 over-narrow NaN

**File:** `river-rats-core/feature_extractor.py` (fix site) + teaching/gto_model/SHAP (downstream spec)
**Line range:** 1169–1195, 1262–1272

#### Why these MUSTs exist

- HIGH #4: `feature_extractor.py:1186` re-fetches `get_villain_range()` when chain returns empty, erasing the FOLD sentinel. Features compute composition against the preflop range of a folded villain.
- MUST #10: NaN must be safe across 4 layers (teaching renders, training drops, SHAP skips, gto_model asserts).
- MUST #15: "Warn + fallback" when chain over-narrows to empty without FOLD is itself the silent-fallback anti-pattern. NaN-flag instead.

#### BEFORE (lines 1169–1195)

```python
chain_steps: List[str] = []
chain_truncated = False
if action_history:
    from range_narrowing import narrow_by_action_history
    v_range, chain_meta = narrow_by_action_history(
        full_range=v_range,
        board=board_cards,
        action_history=action_history,
        villain_pos=villain_pos,
        decision_street=street_name,
    )
    chain_steps = chain_meta.get('chain_steps', [])
    chain_truncated = chain_meta.get('truncated', False)
    if not v_range:
        v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)

if facing_bet:
    v_range = narrow_to_betting_range(v_range, board_cards, street_name)
```

#### AFTER

```python
chain_steps: List[str] = []
chain_truncated = False
chain_surviving_weight = 1.0
villain_folded = False
chain_overflowed = False

if action_history:
    from range_narrowing import narrow_by_action_history
    v_range, chain_meta = narrow_by_action_history(
        full_range=v_range,
        board=board_cards,
        action_history=action_history,
        villain_pos=villain_pos,
        decision_street=street_name,
    )
    chain_steps = chain_meta.get('chain_steps', [])
    chain_truncated = chain_meta.get('truncated', False)
    chain_surviving_weight = chain_meta.get('surviving_weight', 1.0)

    if not v_range:
        _last_step = chain_steps[-1] if chain_steps else ''
        if _last_step.endswith(':FOLD'):
            # HIGH #4: distinguish FOLD from over-narrow.
            villain_folded = True
            # Leave v_range empty; composition loop short-circuits,
            # Step 12 + 17 NaN-flag via _villain_folded sentinel.
        else:
            # MUST #15: over-narrow without FOLD is still a silent-
            # fallback failure mode. Do NOT re-fetch; NaN-flag.
            chain_overflowed = True
            import logging
            logging.getLogger(__name__).warning(
                'extract_range_composition: chain over-narrowed to empty '
                'without FOLD on hero=%s villain=%s board=%r chain_steps=%r; '
                'NaN-flagging composition features (MUST #15).',
                hero_pos, villain_pos, board_cards, chain_steps,
            )
            # Leave v_range empty; composition loop short-circuits below.

# Current-street facing-bet filter — only when villain is still in hand.
if facing_bet and not villain_folded and not chain_overflowed:
    v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)
```

The composition loop at lines 1196–1238 already handles empty `v_range` cleanly (`total_weight` stays 0 → all pct = 0). For folded/over-narrow cases, we need to emit NaN-flags on composition features too:

```python
# After the existing per-hand loop, before the return dict:
if villain_folded or chain_overflowed:
    # MUST #10 — composition features are not applicable when villain
    # isn't in the hand with a meaningful range. NaN-flag so training
    # can drop rows + teaching can render "villain folded".
    tp_pct = float('nan')
    draw_pct = float('nan')
    air_pct = float('nan')
    medium_made_pct = float('nan')
    # Keep board_favour as 0.0 (hero-range-derived, not villain-range)
```

Consolidated return dict (matches §2.4 Step A; repeated here for completeness):

```python
return {
    '_villain_top_pair_plus_pct': tp_pct,
    '_villain_draw_pct': draw_pct,
    '_villain_air_pct': air_pct,
    '_villain_medium_made_pct': medium_made_pct,
    '_villain_range_capped': range_capped,
    '_board_favour': board_favour,
    '_villain_range_chain_steps': chain_steps,
    '_villain_range_chain_truncated': chain_truncated,
    '_surviving_weight': chain_surviving_weight,
    '_villain_range_narrowed': v_range,
    '_villain_folded': villain_folded,
    '_villain_chain_overflowed': chain_overflowed,
    '_action_history_present': _action_history_present,
}
```

#### MUST #10 — NaN spec across 4 layers

| Layer | Surface | Spec |
|-------|---------|------|
| **Training (Stage 4)** | CSV writer (extract_features_parallel, extract_incremental) | **Drop folded-villain rows from blocker-feature + composition-feature columns via mask.** Per orchestrator decision (reconciliation Q's resolution): cleaner distribution than NaN-as-category. Implementation: trainer reads `_action_history_present` + `_villain_folded` audit columns; rows where folded=True get dropped entirely from the training set. |
| **Teaching** | `river-rats-teaching/interface/l3_renderer_enriched.py` | When `_villain_folded=True`: render `"villain folded — range analysis N/A"`. Skip the villain_* composition line entirely. When `_villain_chain_overflowed=True`: render a softer `"villain line too rare to narrow confidently"`. CONTENT_API v4 spec change; coordinate with teaching terminal. **Cross-stream ping required.** |
| **SHAP** | `shap_explainer.py::feature_attention` | When input hand has NaN composition or blocker features, skip those feature IDs from `feature_attention` PRIMARY tagging. Do not render NaN-derived SHAP top-features. Implementation: `if math.isnan(value): continue` inside the PRIMARY loop. |
| **`gto_model.py`** | `gto_model.predict` / `features_from_dict` | Add `math.isnan` check on inference-side feature dict. Raise `ValueError` on unexpected NaN in non-NaN-permitted columns (defensive — flags future-unknown NaN sources). Allowlist: the 5 composition + 4 blocker columns may be NaN when `_villain_folded` or `_villain_chain_overflowed`. |

#### Signature changes + affected callers

- `extract_range_composition` return dict — 5 new fields, additive.
- `gto_model.predict` / `features_from_dict` — add NaN-allowlist parameter. Callers unchanged if defaults allow.
- Teaching CONTENT_API v4 — **cross-stream change**. Not blueprint v2's patch scope but flagged for teaching terminal.

#### Test plan

- Corpus `T_I03_villain_folded_midchain_turn` — existing case in corpus gates HIGH #4 + MUST #10.
- New unit test `test_over_narrow_without_fold_nan_flags` — contrived deep chain that over-narrows, assert `_villain_chain_overflowed=True` and composition features are NaN.
- New unit test `test_nan_skipped_in_shap_attention` — mock SHAP explainer with NaN blocker, assert PRIMARY tags don't include NaN features.
- New unit test `test_gto_model_rejects_unexpected_nan` — feed model a feature dict with NaN in `raw_equity` (not in allowlist), assert ValueError.
- Integration test for training CSV: write a row with `_villain_folded=True`, run trainer's pre-processing, assert row is dropped from the X matrix.

---

## 3. Reconciliation MUSTs

### 3.1 MUST #6 — Equity-feature chain inheritance + MUST #19 explain_hand

**Files:**
- `river-rats-core/feature_extractor.py` lines 500–505, 605–617, 790–806, 823–829
- `river-rats-core/explain_hand.py` lines 261–264, 326–329 (MUST #19 merge)

#### Why this MUST exists

Composition features chain-narrow; equity + partition + explain_hand range summaries do NOT. Same internal-contradiction class as CRIT #1 but at a different layer. The training model learns equity on un-chained villain range while the composition features encode chained range. Magnitude per research literature: 4–12 equity points, sometimes 15+.

MUST #19: `explain_hand.py:261–264, 326–329` call `narrow_to_betting_range` directly for teaching-time range decomposition. Same bypass pattern. Merged into MUST #6 because they're the same plumbing pattern.

#### Scope

4 equity-feature sites + 2 explain_hand sites = 6 plumbing edits.

#### BEFORE — summary (each site)

All 4 equity sites share the pattern:
```python
v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)
if facing_bet:
    street_name = STREET_NAME_MAP.get(street_raw, 'flop')
    v_range = narrow_to_betting_range(v_range, board_cards, street_name)
```

`explain_hand.py:261–264, 326–329` — very similar pattern.

#### AFTER — shared helper + call-site rewrite

Add a shared helper in `feature_extractor.py` that mirrors the chain logic in `extract_range_composition`:

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
) -> Tuple[Dict[str, float], Dict]:
    """MUST #6 shared helper — returns the chain-narrowed villain range
    used by equity / partition / explain_hand. Single source of truth so
    equity + composition see the same villain distribution.

    Returns:
        (v_range, meta) where meta matches extract_range_composition's
        chain metadata ('chain_steps', 'truncated', 'surviving_weight',
        'villain_folded', 'chain_overflowed').
    """
    # Multiway branch — only narrow the bettor's range
    if num_opponents >= 2 and opponent_positions:
        # Use existing get_multiway_villain_range path but inject chain
        # narrowing for the bettor's per-opp range. (Implementation note:
        # multiway equity is Monte Carlo — chain-narrowing the bettor's
        # range reduces its hand count; MC loop runs on narrower range.)
        # ...details deferred to the implementation commit; see §11.
        raise NotImplementedError  # placeholder for blueprint
        # ⚠️ SUPERSEDED BY v2.2 AMENDMENT §3.7 (d7db3f1) + v2.3 AMENDMENT §2.2 (e940e8d) + v2.3.1 PATCH §M60 (this commit)
        # Multiway branch fully spec'd in the later amendments with per_villain_ranges dict + per-villain sentinels.
        # Do not implement from this blueprint-v2 section — read the v2.3/v2.3.1 helper spec.
    # HU branch
    v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)
    meta = {
        'chain_steps': [], 'truncated': False, 'surviving_weight': 1.0,
        'villain_folded': False, 'chain_overflowed': False,
    }
    if action_history:
        v_range, chain_meta = narrow_by_action_history(
            full_range=v_range,
            board=board_cards,
            action_history=action_history,
            villain_pos=villain_pos,
            decision_street=STREET_NAME_MAP.get(street_raw, 'flop'),
        )
        meta['chain_steps'] = chain_meta.get('chain_steps', [])
        meta['truncated'] = chain_meta.get('truncated', False)
        meta['surviving_weight'] = chain_meta.get('surviving_weight', 1.0)

        if not v_range:
            _last_step = meta['chain_steps'][-1] if meta['chain_steps'] else ''
            if _last_step.endswith(':FOLD'):
                meta['villain_folded'] = True
            else:
                meta['chain_overflowed'] = True

    if facing_bet and not meta['villain_folded'] and not meta['chain_overflowed']:
        street_name = STREET_NAME_MAP.get(street_raw, 'flop')
        v_range, _ = narrow_to_betting_range(v_range, board_cards, street_name)

    return v_range, meta
```

Each of the 4 equity-feature call sites replaces the local `get_villain_range` + `narrow_to_betting_range` pair with `_get_chain_narrowed_villain_range(...)`. Specifically:

- `compute_partition_features` (HU branch at line 500–505): single helper call
- `get_multiway_villain_range` (line 605–617): multiway branch of helper
- `compute_equity_features` MW MC loop (line 790–806): helper call per opponent
- `compute_equity_features` HU (line 823–828): single helper call

`explain_hand.py:261–264, 326–329`: same helper call. MUST #19.

#### Data-flow plumbing

`action_history` must be plumbed into `compute_partition_features` and `compute_equity_features` as a new parameter. Both are called from `extract_all_features` at lines ~1582+. Add `action_history=hand.get('_action_history')` to the kwarg list at each call site.

#### Equity MC performance impact (in-blueprint benchmark plan)

Orchestrator asked for perf benchmark plan. Concretely:

1. Pick 10 representative hands from the v2.3.1 training CSV (mix of HU + multiway, mix of action-history depths).
2. Extract features twice: once with current code, once with MUST #6 applied.
3. Measure:
   - Total `extract_all_features` wall time per hand
   - Equity MC iteration count (should be unchanged at 2000)
   - Per-hand chain narrowing cost in `_get_chain_narrowed_villain_range`
4. Expected: chain narrowing adds ~5–15ms per hand (narrow_by_action_history runs the classify_hand loop once per narrow step; 3-street chain = ~3 loops over ~150-hand ranges = fast). MC time should DROP marginally (narrower range = fewer cards to sample from, faster card removal).
5. Report in a follow-up comms doc; if overall per-hand time exceeds 500ms (current ~250ms), escalate to orchestrator before merging.

#### Re-audit scope

- Re-run v2.3.1 training CSV feature extraction with MUST #6 applied.
- Compute equity-vs-range distribution shift:
  - Per-row diff = |equity_post - equity_pre|
  - Expected mean diff: 4–12 points per research (literature-cited magnitude).
  - Expected distribution: heavy on multi-street river decisions; light on flop.
  - Flag any row with >20-point shift for manual GTO review (may indicate chain bug).
- M5 anchor regression must hold: 3/3 β-panel anchors still predict BET on v2.3.1 post-MUST-#6.

#### Test plan

- Corpus `T_J01` (owner canonical H_d9edab5d), `T_J02` (H_8dfb6ef8) — end-to-end integration must show equity shifts match composition shifts in direction.
- Unit test `test_equity_uses_chain_narrowed_range` — compute equity on synthetic multi-street line with + without chain; assert shift magnitude.
- Unit test `test_explain_hand_uses_chain_narrowed_range` — explain_hand output on synthetic line; assert range summary references chain_steps.

---

### 3.2 MUST #7 — Caller list (complete, from research §1)

All 23 callers enumerated. See RESEARCH_FINDINGS §1.1–1.3. No additional action required for this MUST — it's the evidence base that validated HIGH #5's tuple-unpack scope. Referenced here for completeness; blueprint implementation uses this list to verify no site is missed.

---

### 3.3 MUST #8 — Partial coaching/ deletion (narrowed per Q15)

**Scope:** delete exactly 2 files.
- `river-rats-core/coaching/feature_extractor.py` (2423 lines)
- `river-rats-core/coaching/range_narrowing.py` (571 lines)

#### Rationale (narrowed from orchestrator's original path (a))

Research §2 established:
- `coaching/` is NOT a stale duplicate — 11+ coaching modules are actively imported by root modules (`explain_hand.py`, `shap_explainer.py`, `multiway_adjuster.py`, `play.py`, etc.).
- The 2 named files ARE stale duplicates with ZERO runtime importers (verified by grep).
- Full coaching/ collapse is a 4–6 week refactor; out of Stage 3.5 scope. Queued as v2.5+ ticket.

#### Implementation

Two file deletions + 1 CI regression-guard test:

```bash
git rm river-rats-core/coaching/feature_extractor.py
git rm river-rats-core/coaching/range_narrowing.py
```

**Regression guard** — new test at `river-rats-core/tests/test_coaching_duplicate_regression.py`:

```python
"""Regression guard — ensures coaching/feature_extractor.py and
coaching/range_narrowing.py do not re-appear.

Deleted 2026-04-XX per MUST #8 (Stage 3.5 blueprint v2). Both files
were stale duplicates with no runtime importers but represented a
silent-bypass surface: if re-introduced and imported, they'd defeat
the Stage 3.5 chain narrowing at the composition-feature level.

v2.5+ ticket exists for full coaching/ collapse; until then, this
test gates the partial-delete."""

import os

def test_coaching_feature_extractor_is_deleted():
    core = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad = os.path.join(core, 'coaching', 'feature_extractor.py')
    assert not os.path.exists(bad), (
        'coaching/feature_extractor.py re-appeared. This file was '
        'deleted per Stage 3.5 MUST #8 because it lacked action-history '
        'chain narrowing. If you need a coaching-side feature extractor, '
        'import from the root river-rats-core/feature_extractor.py or '
        'file a v2.5+ ticket to do the full coaching/ collapse.'
    )

def test_coaching_range_narrowing_is_deleted():
    core = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad = os.path.join(core, 'coaching', 'range_narrowing.py')
    assert not os.path.exists(bad), (
        'coaching/range_narrowing.py re-appeared. Same reasoning as '
        'coaching/feature_extractor.py.'
    )

def test_no_new_importers_of_coaching_feature_extractor():
    """Also fail if any file imports coaching.feature_extractor or
    coaching.range_narrowing (even indirectly)."""
    import subprocess, re
    core = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo = os.path.dirname(core)
    result = subprocess.run(
        ['grep', '-rn', '--include=*.py',
         '-E', 'from coaching\\.(feature_extractor|range_narrowing)|'
               'import coaching\\.(feature_extractor|range_narrowing)',
         repo],
        capture_output=True, text=True,
    )
    # stdout empty + returncode 1 (grep found nothing) is the pass condition
    assert result.returncode in (1, 0), f'grep failed: {result.stderr}'
    offenders = [l for l in result.stdout.splitlines() if l.strip()]
    assert not offenders, (
        f'Found importers of coaching.feature_extractor or '
        f'coaching.range_narrowing (deleted):\n' + '\n'.join(offenders)
    )
```

#### Risk assessment

- Any path that imports `coaching.feature_extractor` at runtime will fail with `ModuleNotFoundError`. Research confirmed zero importers. Third-party test runs (CI) may still hit cache. Safe because:
  - No `__init__.py` re-exports (coaching/__init__.py is 0 bytes)
  - No `sys.path` manipulation preloads these modules
  - pytest / unittest discovery is unaffected (these are duplicate-path files, not test files)
- If a hidden caller surfaces post-deletion, the test above fails loudly with the offending file list.

---

### 3.4 MUST #14 — Re-sequenced commit order

See §11 below for the authoritative 15-commit sequence. MUST #14's key
change (CRIT #2 moves from last to second) is incorporated.

---

### 3.5 MUST #17 — Frequency-table tweak

**File:** `river-rats-core/range_narrowing.py`
**Line range:** 142 (or equivalent — `RIVER_CHECKING_FREQUENCIES` dict)

#### Change

```python
# BEFORE:
RIVER_CHECKING_FREQUENCIES = {
    # ...
    'medium_made': 0.92,    # Almost ALWAYS check! Bluff-catcher
    # ...
}

# AFTER:
RIVER_CHECKING_FREQUENCIES = {
    # ...
    'medium_made': 0.85,    # MUST #17 — GTO review: thin river value
                             # with medium pair exists vs weak ranges,
                             # especially on multi-street missed-draw
                             # lines. 0.92 over-compresses mediums into
                             # check-call band. v2.5 path: board-
                             # texture-conditional table.
    # ...
}
```

Single-line change. Documented v2.5 follow-up.

---

### 3.6 MUST #18 — Corpus reauthoring (T_J01 + T_B05)

**File:** `review/tests/range_narrowing_test_corpus_2026-04-20.yaml`

#### T_J01 (owner canonical H_d9edab5d)

**Problem:** Practical-pro review found `T_J01`'s `expected_composition_post_fix` is a near-copy of `expected_composition_pre_fix` (0.70 TP+ / 0.04 med / 0.26 air ≈ pre-fix 0.72 / 0.06 / 0.22). If shipped, this hand — the one that motivated the whole Stage 3.5 project — will show "nothing changed" to the owner.

**Rewritten post-fix values match K_05/K_06 pattern (delayed-probe line):**

```yaml
- id: "T_J01_owner_H_d9edab5d_turn_check_through_river_bet"
  # ... existing pre-fix values unchanged ...
  expected_composition_post_fix:
    villain_tp_pct: 0.55        # was 0.70 — should drop from pre
    villain_medium_made_pct: 0.04
    villain_draw_pct: 0.00
    villain_air_pct: 0.41        # was 0.26 — should rise substantially
  notes: "[approx, REAUTHORED per MUST #18] Turn check-through followed
          by river bet. Villain's turn check drops nuts/strong_value
          (they'd bet for value); river bet repolarizes into air-heavy
          (delayed probe / polarised bluff). Matches K_05 / K_06 pattern.
          Original post-fix values (0.70/0.04/0.26) were a copy-error
          per practical-pro review; corrected 2026-04-22."
```

#### T_B05 (donk flop, call-raise, turn check)

**Problem:** GTO review flagged `medium_made: 0.25` too high.

**Rewritten:**
```yaml
- id: "T_B05_flop_bet_raise_call_three_step"
  expected_composition_post_fix:
    villain_tp_pct: 0.70          # was ~0.50
    villain_medium_made_pct: 0.12  # was 0.25 — over-weighted mediums
    villain_draw_pct: 0.03
    villain_air_pct: 0.15
  notes: "[approx, REAUTHORED per MUST #18] Flop bet-raise-call-turn-
          check line. Villain bet-raises then check-backs turn: mostly
          strong value now pot-controlling on safe turn. TP+ rises."
```

---

## 4. Research MUSTs (MUST #20–#23)

### 4.1 MUST #20 — calibration_exam.py chain-clean

**File:** `river-rats-core/calibration_exam.py`
**Line range:** 158–193 (`_labelled_record_to_reference_hand`), 279–300 (`reference_hand_to_situation`)

#### Why

Research established that `calibration_exam.py::format_situation_for_agent` (line 326) is the **primary labelling-display tool**. Labellers see features coming from `extract_all_features(hand_dict)` at line 300. `hand_dict` at lines 279–298 has NO `_action_history`. Labellers see un-chained composition values. **Stage 4 re-label would bake corruption into labels at the root.**

#### Fix — combined with Q18 data source (path (c))

See §5 for the full data-source plan. Summary:

1. Extend `ReferenceHand` dataclass (reference_evaluator.py:92-116) with `action_history: List[Tuple[str, str, str]] = field(default_factory=list)`.
2. Extend canonical labelled JSONL schema with top-level `action_history` field.
3. `_labelled_record_to_reference_hand` (calibration_exam.py:170) reads `record.get('action_history', [])`, converts to tuples, sets on ReferenceHand.
4. `reference_hand_to_situation` (calibration_exam.py:279) adds `'_action_history': hand.action_history` to `hand_dict`.
5. For fixtures that don't yet have the field, authored sidecar table `_CALIBRATION_ACTION_HISTORY` in calibration_exam.py (same style as `_FB_ACTION_HISTORY` but with full sequences, not counts) provides a fallback during schema migration.

#### BEFORE (lines 279–298 excerpt)

```python
hand_dict = {
    'h': hand.hero_cards,
    'b': hand.board,
    'pos': hand.hero_position,
    # ... 13 more keys ...
    '_facing_raise': hand.facing_raise,
}   # no _action_history
```

#### AFTER

```python
hand_dict = {
    'h': hand.hero_cards,
    'b': hand.board,
    'pos': hand.hero_position,
    # ... existing keys ...
    '_facing_raise': hand.facing_raise,
    # MUST #20 — chain narrowing for labelling display
    '_action_history': (
        hand.action_history
        if hand.action_history
        else _CALIBRATION_ACTION_HISTORY.get(hand.ref_id, [])
    ),
}
```

Sidecar table:

```python
# MUST #20 — per-fixture authored action histories for calibration
# hands that don't yet carry the structured field in the canonical
# JSONL. Same pattern as _FB_ACTION_HISTORY in reference_evaluator.py
# but with full (street, position, action) tuples instead of counts.
#
# Structure: ref_id -> list of (street, position, action) tuples
# Once JSONL records carry this field natively (Stage 4 data prep),
# the sidecar becomes empty and can be deleted.
_CALIBRATION_ACTION_HISTORY: Dict[str, List[Tuple[str, str, str]]] = {
    # MW-11 to MW-50 + any test_set_50 IDs authored here
    # Each entry authored from the prose annotations in
    # _ACTION_HISTORY + the source BATCH*_DESIGNS.md docs.
    'MW-11': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'CO', 'CHECK'),
        ('flop', 'BTN', 'CHECK'),
    ],
    # ... one entry per fixture; ~150 entries total once MW-50 + test_set_50 covered ...
}
```

#### Data-authoring lift estimate

- MW-50 (50 fixtures): ~50 entries
- test_set_50 (50 fixtures): ~50 entries
- 3way_combined_350 subset used by calibration: ~40 entries (not all 350 are labelled)

Total ~140 entries, each ~5–8 lines of YAML-in-Python. ~2 days of authoring with GTO reviewer pass per batch.

**Dependency:** This work cannot complete without the source prose
annotations. Those exist at `_ACTION_HISTORY` (reference_evaluator.py:123+)
and in `BATCH2_8_HAND_DESIGNS.md` + siblings. Authoring is tedious but
mechanical — expand 5-tuple counts into full sequences per fixture.

---

### 4.2 MUST #21 — Stage 4 gate (landed in manifest v1.8)

**File:** `RELEASE_MANIFEST.yaml`
**Status:** ALREADY LANDED in commit `e7dd240` (manifest v1.8).

No code action. Blueprint v2 cross-references the manifest's hardened
Stage 4 gate:

> Stage 4 cannot open until ALL of:
> 1. Stage 2 KB §1.9 complete + GTO-reviewed
> 2. Stage 3 v3.2 prompt complete + derives from updated KB
> 3. Stage 3.5 all 23 MUSTs landed + audits clean
> 4. Labelling-pipeline consumers chain-clean (MUST #20 + #22)

Each MUST in this blueprint maps to one of the 4 gate items. Gate
enforcement belongs to the orchestrator at Stage 4 handoff.

---

### 4.3 MUST #22 — reference_evaluator.py chain-clean

**File:** `river-rats-core/reference_evaluator.py`
**Line range:** 460–492 (`_evaluate_one_hand` hand_dict), 675–713 (`_build_fb_hand_dict`)

#### Why

88.1% HU / 52.5% MW baseline metric uses the bypass path. Post-v2.4
evaluation must use chain-populated hand_dicts or the comparison is
meaningless.

#### BEFORE (lines 470–489 and 693–712)

Both sites build a 14-key hand_dict without `_action_history`. Same
structure as calibration_exam.py.

#### AFTER — both sites

**`_evaluate_one_hand` (lines 470–489):** add `_action_history` to hand_dict.

```python
hand_dict = {
    'h': hand.hero_cards,
    # ... existing keys ...
    '_facing_raise': hand.facing_raise,
    # MUST #22 — chain narrowing for eval baseline
    '_action_history': (
        hand.action_history if hand.action_history
        else _REFERENCE_ACTION_HISTORY.get(hand.ref_id, [])
    ),
}
```

**`_build_fb_hand_dict` (lines 693–712):** similar but reads from `_FB_ACTION_HISTORY_FULL`:

```python
hand_dict = {
    # ... existing 14 keys ...
    '_facing_raise': ah[4],
    # MUST #22 — chain narrowing for FB-40 baseline
    '_action_history': _FB_ACTION_HISTORY_FULL.get(sid, []),
}
```

#### Sidecar table `_FB_ACTION_HISTORY_FULL`

Mirror of `_FB_ACTION_HISTORY` (which currently holds 5-tuple counts) but with full (street, position, action) sequences. Each of FB-01 through FB-40 gets authored; existing prose comments at lines 630–672 provide the source truth for each.

Example:

```python
_FB_ACTION_HISTORY_FULL: Dict[str, List[Tuple[str, str, str]]] = {
    # FB-01: "Flop. CO c-bet; BTN folded; hero (BB) faces HU bet."
    'FB-01': [
        ('preflop', 'CO', 'RAISE'),
        ('preflop', 'BTN', 'CALL'),
        ('preflop', 'BB', 'CALL'),
        ('flop', 'CO', 'BET'),
        ('flop', 'BTN', 'FOLD'),
    ],
    # ... 39 more entries, each ~6–10 lines, derived from comments
    # at lines 630–672 ...
}
```

`_REFERENCE_ACTION_HISTORY` similarly authored from the MW-11+ prose
at lines 123+.

#### Authoring lift estimate

- FB-40: 40 entries × ~7 lines = ~280 lines
- MW-50: 50 entries × ~7 lines = ~350 lines
- Additional reference hands (if used): TBD

Total ~500 authored lines. ~1.5 days with GTO reviewer pass per batch
of 10.

#### M4 re-audit implication

Once MUST #22 lands, re-run the 88.1% HU / 52.5% MW baseline against
v2.2 (unchanged model). Expected: baseline MOVES. Direction uncertain
— chain may produce more accurate predictions (HU up, MW up) or expose
training data blind spots (down). **This re-baseline is part of Stage 6
ship gate, not a Stage 3.5 ship-blocker.**

#### Test plan

- New integration test `test_reference_evaluator_uses_chain` — sample FB fixture with authored action_history; assert hand_dict carries `_action_history`; assert chain_steps non-empty in extracted feat_dict.
- Audit run on small subset (5 FB hands + 5 MW hands) to validate sidecar authoring before full re-baseline.

---

### 4.4 MUST #23 — train_sizing_model.py chain-clean (verify first)

**File:** `river-rats-core/train_sizing_model.py`
**Line range:** ~140 (`extract_all_features` call)

#### Verification task (first 30 minutes of implementation)

Read `train_sizing_model.py:120–160` to confirm:
1. Does hand_dict construction include `_action_history`?
2. What is the data source (PokerBench / gauntlet / factory)?

If bypass confirmed: apply the same fix pattern as MUST #20 + #22. Path (c) authoring required for sizing-specific fixtures.

**If sizing uses gauntlet_500k:** this becomes a Path-(c)-or-defer question. Gauntlet_500k doesn't carry action history; authoring 500k sequences is infeasible. Two options:

- (x) Drop gauntlet_500k from sizing training; retrain sizing on a
  smaller chain-clean corpus (same approach as MUST #20).
- (y) Sizing model uses bypass path permanently; flag `_action_history_present=False`
  on sizing rows in a separate audit column; accept that sizing is
  single-street-aware until v2.5+ introduces a sizing-specific re-label.

**Recommendation:** (y) for Stage 3.5 — sizing and action model are
distinct, and sizing's training distribution is less chain-sensitive
(sizing is primarily texture-driven, not history-driven). Escalate if
orchestrator disagrees.

#### Test plan

- Unit test `test_sizing_model_audit_column` — after retrain, audit
  column for sizing CSV shows `_action_history_present=False` uniformly;
  verify the sizing model's FEATURE_COLUMNS doesn't depend on
  composition or blocker features (those require chain-correctness).

---

## 5. Q18/Q19 data-source resolution — path (c)

**Path (c) chosen:** extend JSONL schema with structured `action_history`
field; author sidecar tables for fixtures that predate the schema
extension. Cleanest path given the data that exists today.

### 5.1 Data reality (from research)

- **ReferenceHand dataclass** (`reference_evaluator.py:92–116`): carries only COUNTS, no per-street action sequences.
- **Canonical labelled JSONL records**: have prose fields (`action_string`, `prior_actions`) but not structured action-history lists.
- **Existing annotation tables** (`_FB_ACTION_HISTORY`, `_ACTION_HISTORY`): hand-authored prose comments describing each fixture's action line. Perfect substrate for extending to full sequences.
- **Fixtures were NOT constructed from gauntlet** (research §5.6 verified) — they were authored or factory-built. Action data exists as prose; was never structured.

### 5.2 Path (c) plan in phases

**Phase 1 — Schema extension (code):**
- Extend `ReferenceHand` dataclass with `action_history: List[Tuple[str, str, str]] = field(default_factory=list)`.
- Extend `_labelled_record_to_reference_hand` to read `record.get('action_history', [])`.
- Extend canonical JSONL schema documentation: new top-level field.

**Phase 2 — Sidecar tables (code + data):**
- Author `_FB_ACTION_HISTORY_FULL` (40 entries) from existing prose comments.
- Author `_REFERENCE_ACTION_HISTORY` (50–100 entries) from MW-11+ prose.
- Author `_CALIBRATION_ACTION_HISTORY` (overlapping with `_REFERENCE_ACTION_HISTORY`).
- GTO reviewer pass per batch.

**Phase 3 — hand_dict plumbing (code):**
- `calibration_exam.py:279–298` — MUST #20.
- `reference_evaluator.py:470–489, 693–712` — MUST #22.
- `train_sizing_model.py:~140` — MUST #23 (pending verification).

**Phase 4 — JSONL schema migration (data):**
- Once sidecars are complete + verified, migrate JSONL records to carry the structured field natively.
- Sidecars become empty; can be deleted in a follow-up commit.

### 5.3 Owner approval gate

Phase 1 + 3 are code plumbing — ~2 days for all three files. Phase 2 is
authoring — ~3–4 days including GTO reviewer passes. Phase 4 is a
cleanup migration — ~1 day.

**Recommend owner approval gate between Phase 1 and Phase 2:** after
code plumbing lands, run a dry run on 5 authored sidecar entries and
verify the chain fires as expected. Go/no-go on the remaining ~135
entries based on the dry-run quality.

### 5.4 Alternative (rejected)

- **(a) parse prose `action_string` at runtime:** fragile; prose is
  under-specified (`"SB check, CO check, BTN ???"` infers hero's slot
  from `???`). Error-prone.
- **(b) author per-fixture sidecar only, no schema extension:** less
  work short-term, but the JSONL records would carry no action history
  in their source form, so every new consumer would need sidecar lookup.
  Technical debt.

Path (c) is the highest-upfront-cost / lowest-ongoing-cost choice. Per
quality-default, correct pick.

---

## 6. Cross-MUST edit-overlap map

Commit-order-aware overlap view to prevent churn.

### 6.1 `range_narrowing.py` chain loop — HIGH #5 ↔ HIGH #3 (+ MUST #11 + #12)

Both touch `narrow_by_action_history` body (lines 770–843):

| Lines | HIGH #5 change | HIGH #3 / #11 / #12 change |
|-------|----------------|----------------------------|
| Top of module | Add `_STAGE35_WEIGHT_FLOOR_PCT = 0.10`, `_STAGE35_WEIGHT_WARN_PCT = 0.20` | — |
| ~530 (new) | — | Add `_collapse_same_street_sequence` helper |
| 770 | — | Unchanged |
| 775–777 | — | `villain_street_actions = _collapse_same_street_sequence(...)` insert |
| 781–800 | Each `narrow_*` call → tuple unpack `(range, step_surv)` | Loop iterates on filtered actions |
| 802–832 | Mass-based safety rail replaces count-based | Unchanged |
| 836–842 | Meta: `surviving_weight` now mass | Unchanged |

**Sequencing:** HIGH #5 FIRST (all tuple-unpack churn). HIGH #3 SECOND (collapse helper added on top).

### 6.2 `feature_extractor.py::extract_range_composition` return dict — CRIT #1 + CRIT #2 + HIGH #4 + HIGH #5

All 4 MUSTs contribute fields to the `extract_range_composition` return
dict. Single consolidated return block (§2.4 Step A + §2.5):

```python
return {
    # Stage 3.0+ scalar composition features
    '_villain_top_pair_plus_pct', '_villain_draw_pct', '_villain_air_pct',
    '_villain_medium_made_pct', '_villain_range_capped', '_board_favour',
    # Stage 3.5 chain metadata (HIGH #5)
    '_villain_range_chain_steps', '_villain_range_chain_truncated',
    '_surviving_weight',
    # Stage 3.5 range publication (CRIT #1)
    '_villain_range_narrowed',
    # Stage 3.5 sentinels (HIGH #4 + MUST #15)
    '_villain_folded', '_villain_chain_overflowed',
    # Stage 3.5 provenance (CRIT #2)
    '_action_history_present',
}
```

**Sequencing:** All 4 MUSTs land their partial return-dict changes in separate commits per MUST #14's per-MUST discipline. Each commit adds its key(s); prior commits' keys remain. Final state is the consolidated block.

### 6.3 `extract_all_features` Step 12 + Step 17 — CRIT #1 + HIGH #4 + MUST #10

CRIT #1 rewrites Step 12 + Step 17 consumption. HIGH #4 + MUST #10 add
NaN branches inside the rewrite. Single consolidated block (§2.4 Step B).

**Sequencing:** CRIT #1 lands the rewrite with NaN branches pre-authored
(even though `_villain_folded` sentinel doesn't exist yet in the return
dict). HIGH #4 then extends the return dict to populate `_villain_folded`.
The NaN branch is dormant until HIGH #4 fires it.

### 6.4 MUST #6 independence

MUST #6's shared helper (`_get_chain_narrowed_villain_range`) is newly
written and doesn't collide with any existing MUST. Lands in commit 6
post-CRIT #1 (so the helper can pattern-match the `extract_range_composition`
logic).

### 6.5 MUST #20 + MUST #22 + MUST #23 parallelism

All three plumb `_action_history` into hand_dict at distinct call sites
(`calibration_exam.py`, `reference_evaluator.py`, `train_sizing_model.py`).
No overlap with each other; serialized into commits 7–9 after MUST #6
because they depend on MUST #6's `_action_history` being honored by
equity feature computation.

---

## 7. Unit test corpus — 81 cases + 4 coverage-gap additions

Corpus file: `review/tests/range_narrowing_test_corpus_2026-04-20.yaml` (81 cases).
New consumer: `river-rats-core/tests/test_range_narrowing_stage35_corpus.py` (new pytest-parametrised).

### 7.1 Existing 81 cases → MUST mapping

Same table as blueprint v1 §7 (unchanged). Summary:

| Section | Cases | Primary MUST(s) gated |
|---------|-------|------------------------|
| A. Simple chains (10) | T_A01–T_A10 | Baseline + HIGH #5 |
| B. Double-action per street (5) | T_B01–T_B05 | HIGH #3 + MUST #11 + MUST #12 (+ MUST #18 for T_B05 reauthoring) |
| C. CALL edge cases (8) | T_C01–T_C08 | `narrow_to_continuing_range` + MUST #11 |
| D. Street-transition (6) | T_D01–T_D06 | Chain at decision-street boundary |
| E. Multiway (5) | T_E01–T_E05 | Multiway primary-villain selection |
| F. Board-texture (10) | T_F01–T_F10 | Baseline; regression catches |
| G. Position variety (5) | T_G01–T_G05 | `villain_pos` filter in chain |
| H. Anchor regression (5) | T_H01–T_H05 | MUST #16 regression guard |
| I. Safety rails (3) | T_I01–T_I03 | CRIT #2 (T_I01) + HIGH #4 (T_I03) |
| J. Owner canonical (3) | T_J01–T_J03 | CRIT #1 (T_J03) + MUST #18 (T_J01 reauthoring) |
| K. Extra breadth (20) | T_K01–T_K20 | Check-raise (K04, K11, K20), deep chain (K20), malformed (K18), tuple form (K17), zero-baseline (K16) |

### 7.2 Coverage gap additions (4 new cases or unit tests)

| New | Gates | Location |
|-----|-------|----------|
| `test_step12_uses_chain_narrowed_range` | CRIT #1 integration | `test_range_features.py` |
| `test_stage4_strict_action_history_raises` + `...warns` | CRIT #2 env gate | `test_range_features.py` or new file |
| `test_surviving_weight_is_mass_not_count` + `test_mass_floor_truncates_at_10pct` + `test_mass_warn_at_20pct` | HIGH #5 + MUST #13 | new `test_surviving_weight.py` |
| `test_collapse_check_call_same_street` + `test_collapse_triple_check_check_bet` + `test_collapse_pure_check_through` | HIGH #3 / MUST #11 / MUST #12 | new `test_pre_filter.py` |

### 7.3 Existing 16-test file

`river-rats-core/tests/test_range_narrowing_stage35.py` (325 lines) stays
and extends. Covers module-level constants, tuple-action acceptance,
schema-mismatch guard. Corpus consumer is a NEW test file.

### 7.4 Expected-value calibration strategy

Per Q12 (tester) from blueprint v1 reconciliation: first pass uses
**direction tests** (post-fix differs from pre-fix in expected direction
by >X%). Exact values calibrated in a follow-up commit after the
implementation is merged and the real output is observed. Prevents
blocking on expected-value precision debates.

---

## 8. M4 re-audit scope expansion

**File:** `review/run_stage35_backfill_audit.py`
**Pre-fix baseline:** 579 rows; 0/124 flop isolation violations; 455/455 chain firing on composition features.

### 8.1 New audit checks post-fix

1. **Step 12 + Step 17 chain-consumption check (CRIT #1):**
   - For every row with `_action_history_present=True` and non-empty `chain_steps`:
     - Compute `FLUSH_BLOCK_PCT` via production code (chain-consumed).
     - Re-compute via bypass path (get_villain_range + narrow_to_betting_range only).
     - **Pre-patch expectation:** 455 rows differ (same as chain-firing count).
     - **Post-patch expectation:** 0 rows differ.

2. **Folded-villain NaN check (HIGH #4 + MUST #10):**
   - Count rows with `_villain_folded=True`.
   - Assert `FLUSH_BLOCK_PCT`, `FLUSH_DRAW_BLOCK_PCT`, `STRAIGHT_DRAW_BLOCK_PCT`, `NUT_MADE_BLOCK_PCT` all NaN on those rows.
   - Assert composition features `_villain_top_pair_plus_pct`, etc. also NaN.

3. **Over-narrow chain check (MUST #15):**
   - Count rows with `_villain_chain_overflowed=True`.
   - Same NaN assertions.

4. **CRIT #2 column presence:**
   - Assert `_action_history_present` in every CSV.
   - Expected distribution: 100% True for live-play rows, 0% for gauntlet/PokerBench (pre-sidecar); transitions during Path (c) authoring.

5. **HIGH #5 mass surviving-weight range:**
   - Assert `_surviving_weight ∈ [0.0, 1.0]` per row.
   - Strictly decreasing across `chain_steps`.
   - Rows at 0.0 must have `_villain_folded=True`.

6. **MUST #6 equity shift distribution:**
   - Per-row diff = |equity_post - equity_pre|.
   - Expected mean diff: 4–12 points (per literature).
   - Flag rows with >20-point shift for GTO review.

7. **MUST #13 threshold enforcement:**
   - Rows with `_villain_range_chain_truncated=True` must have `_surviving_weight < 0.10`.

---

## 9. M5 anchor regression + MUST #16 guard

**File:** `review/run_v231_anchor_recheck_stage35.py`
**Pre-fix baseline:** 3/3 β-panel anchors BET on v2.3.1.

### 9.1 Re-run post-all-MUSTs

Same script, same 3 anchors, same expected result (3/3 BET). If any
anchor flips to CHECK after MUSTs land: STOP and report.

Possible failure causes to be prepared for:
- HIGH #3 pre-filter unexpectedly matches a non-check-raise shape.
- HIGH #5 mass threshold truncates an anchor's chain.
- CRIT #1's NaN-flag for folded villains accidentally applied to a non-folded anchor.
- MUST #6's equity chain shifts an anchor's equity past its decision boundary.

### 9.2 MUST #16 regression guard

Per Q16 redirect: downgraded from ship-blocker to regression guard.

New assertion in `run_v231_anchor_recheck_stage35.py`:

```python
# MUST #16 — regression guard. Ensure chain is actually exercised on
# each anchor (fixtures include action_history → chain_steps populated).
for anchor in anchors:
    spec = build_spec(anchor)
    feat_dict = extract_features(spec)  # via situation_factory
    chain_steps = feat_dict.get('_villain_range_chain_steps', [])
    assert chain_steps, (
        f'Anchor {anchor["anchor_id"]} produced empty chain_steps. '
        f'Expected multi-street action_history to fire the chain. '
        f'If this anchor was added without action_history, restore it '
        f'or flag the fixture.'
    )
```

Applies to both `evaluate_calibration_anchors.py` P0 pre-flight AND the Stage 3.5 M5 diagnostic script.

---

## 10. Observability hooks (consolidated)

All `_meta_` fields surfaced by the MUSTs, and their destination in
training CSV / audit tools:

| Field | Source | Type | CSV column? | Reason |
|---|---|---|---|---|
| `_villain_range_chain_steps` | extract_range_composition + MUST #6 helper | `List[str]` | Yes (stringified) | Stage 4 audit; verify chain exercised |
| `_villain_range_chain_truncated` | same | `bool` | Yes (int 0/1) | Flag rare lines |
| `_surviving_weight` | MUST #5 helper | `float` | Yes | Distribution audit |
| `_action_history_present` | CRIT #2 | `bool` | Yes (int 0/1) | Stage 4 mixture detection |
| `_villain_folded` | HIGH #4 | `bool` | Yes (int 0/1) | Stage 4 row-drop mask |
| `_villain_chain_overflowed` | MUST #15 | `bool` | Yes (int 0/1) | Same |
| `_villain_range_narrowed` | CRIT #1 | `Dict[str, float]` | **No** (too wide) | Used only inside feature_extractor |

All flags land in CSV via the additive-column bumps in
`extract_features_parallel.py` MODEL_COLUMNS + `extract_incremental.py`
header (see §2.2 part 3). Model inference is unaffected — `FEATURE_COLUMNS`
governs what the model sees.

---

## 11. Commit sequence (15 commits)

**Re-sequenced per MUST #14** (CRIT #2 second, not last). Per CLAUDE.md
one-MUST-per-commit discipline, with reviewer pass between commits.

| # | Commit | Lands |
|---|--------|-------|
| 1 | `Stage 3.5 HIGH #5 + #13: narrow_* return mass; surviving_weight thread; floor 10%/WARN 20%` | Tuple-return API, mass threading, updated thresholds, deleted old count-safety-rail. ⚠️ SUPERSEDED: canonical tuple-unpack count is **14 root+coaching + 5 test = 19 sites** per v2.2 amendment §1.1 (d7db3f1) + v2.3 §2.3 canonical table + v2.3.1 §M61 (this commit). The "13" figure here is stale; do not use. |
| 2 | `Stage 3.5 CRIT #2 + MUST #9: strict action_history gate + pipeline unswallow` | Env-gated RuntimeError in extract_range_composition; `except RuntimeError: raise` in 3 training pipelines; MODEL_COLUMNS bump for `_action_history_present`. |
| 3 | `Stage 3.5 HIGH #3 + MUST #11 + #12: same-street sequence collapse pre-filter` | `_collapse_same_street_sequence` helper; call-site insertion in `narrow_by_action_history`. |
| 4 | `Stage 3.5 CRIT #1: blocker features consume chain-narrowed range` | Publish `_villain_range_narrowed` from `extract_range_composition`; rewrite Step 12 + Step 17 to consume; delete `_s12_*` locals. |
| 5 | `Stage 3.5 HIGH #4 + MUST #10 + #15: folded + overflow sentinels; NaN spec` | Sentinel logic post-chain; NaN branches in Step 12/17 composition loop; SHAP + gto_model NaN handling; teaching CONTENT_API cross-stream ping. |
| 6 | `Stage 3.5 MUST #6 + MUST #19: equity + explain_hand chain inheritance` | `_get_chain_narrowed_villain_range` helper; 4 equity site rewrites + 2 explain_hand site rewrites; per-hand benchmark plan doc. |
| 7 | `Stage 3.5 MUST #20: calibration_exam.py _action_history plumbing` | ReferenceHand dataclass extend; `_labelled_record_to_reference_hand` read; `reference_hand_to_situation` write; `_CALIBRATION_ACTION_HISTORY` sidecar (5-entry dry-run batch). |
| 8 | `Stage 3.5 MUST #22: reference_evaluator.py _action_history plumbing` | Both hand_dict sites; `_FB_ACTION_HISTORY_FULL` sidecar (5-entry dry-run batch); `_REFERENCE_ACTION_HISTORY` same. |
| 9 | `Stage 3.5 MUST #23: train_sizing_model.py verification + chain plumb` | Read hand_dict construction; if bypass, apply same fix OR document (y) bypass-accepted with audit column; decision + reasoning. |
| 10 | `Stage 3.5 MUST #8 partial: delete coaching/ stale duplicates` | git rm 2 files; regression-guard test. |
| 11 | `Stage 3.5 MUST #17: freq table — RIVER_CHECKING medium_made 0.92 → 0.85` | Single-line change. |
| 12 | `Stage 3.5 corpus: 81-case pytest consumer + 4 coverage-gap additions + MUST #18` | New `test_range_narrowing_stage35_corpus.py`; reauthor T_J01 + T_B05. |
| 13 | `Stage 3.5 M4 re-audit: blocker bypass + NaN + mass checks` | Extend `run_stage35_backfill_audit.py` with 7 new check categories. |
| 14 | `Stage 3.5 M5 re-run: anchor regression + MUST #16 guard` | Re-run script; add chain_steps non-empty assertion. |
| 15 | `Stage 3.5 SHIP: audit report + Path (c) Phase 2 authored sidecars` | Full sidecar tables (post-dry-run owner approval); audit reports in review/comms/; mark Stage 3.5 complete in manifest. |

### 11.1 Gate between commits 6 and 7

Commits 1–6 are pure code changes. Commits 7–9 require sidecar authoring
(Path (c) Phase 2 dry-run batch). **Owner approval gate** between commit
6 and commit 7: run dry-run batch of 5 authored sidecar entries, verify
chain fires correctly, owner go/no-go on remaining ~140 entries.

### 11.2 Parallelism opportunities

Commits 7, 8, 9 are data-plumbing in 3 different files. Could land in
parallel or sequence. Per CLAUDE.md per-MUST discipline: sequence.

Commits 10, 11 are small and independent. Could land earlier in the
sequence if scheduling demands. Kept late for clean audit trail.

---

## 12. STOP conditions + verification items in-flight

### 12.1 STOP conditions per CLAUDE.md §5

Apply throughout:
- File/line doesn't match blueprint (HEAD drift between blueprint and implementation start)
- Test corpus assertion fails in a way this blueprint didn't anticipate (direction-test tolerance is the first safety net)
- M4 or M5 re-audit produces unexpected output
- Any MUST surfaces a new bypass site (would become MUST #24+, requires re-cut)
- Owner approval gate (§11.1) fails dry-run

### 12.2 Verification items deferred to commit time (30-minute reads)

From research §5.6:

1. `train_sizing_model.py:140` hand_dict contents (for MUST #23)
2. `explain_hand.py:424` hand_json source and whether it carries action history
3. `coaching/explain_hand.py:424` — moot if MUST #8 partial-delete applies, but this file survives Stage 3.5
4. Full JSONL reader path for canonical labelled JSONL records — confirm no existing `action_history` field that supersedes sidecar
5. v2.3.1 training CSV format — action history in any column?

All five can be resolved in commit 6 or commit 7 work time. Blueprint
doesn't block on them.

---

## 13. Questions requiring orchestrator sign-off before implementation

| Q | Topic | Recommended answer |
|---|-------|--------------------|
| Q20 | MUST #23: if train_sizing_model uses gauntlet_500k, accept option (y) bypass-permanent-with-audit-column for v2.4? | YES — sizing is less chain-sensitive; v2.5+ revisit |
| Q21 | Owner approval gate between commits 6 and 7 — 5-entry dry-run batch before ~140-entry authoring lift? | YES (quality default) |
| Q22 | Teaching CONTENT_API v4 cross-stream ping for NaN render spec (MUST #10 teaching layer) — who drives? | Builder drafts; teaching terminal owns CONTENT_API implementation; orchestrator coordinates |
| Q23 | Path (c) Phase 4 (JSONL schema migration + sidecar cleanup) — in Stage 3.5 scope or defer to Stage 4 data prep? | Recommend defer — Stage 4 data prep is the natural home |
| Q24 | Frequency-table tweak (MUST #17) — land in Stage 3.5 (this blueprint) or defer to Stage 4 data prep? | Land in Stage 3.5; single-line change; re-audit runs on v2.3.1 with new table |
| Q25 | MUST #18 corpus reauthoring — only T_J01 + T_B05, or audit all 81 cases? | Only the two flagged by reviewer panel; other 79 use direction-test tolerance |
| Q26 | M4 re-audit check #6 (MUST #6 equity shift distribution) — 20-point outlier threshold appropriate? | Yes for v1; calibrate from observed distribution post-merge |

---

## 14. Reviewer role assignments

Second-pass multi-agent reconciliation:

| Role | Primary questions |
|------|-------------------|
| Architecture | Q20 (sizing bypass), Q22 (CONTENT_API), Q23 (schema migration), Q26 (threshold), plus any structural concerns about the shared `_get_chain_narrowed_villain_range` helper |
| GTO theorist | MUST #11 (check-call collapse), MUST #17 (freq table), MUST #18 (corpus reauthoring directional expectations), MUST #13 (mass floor value), alternative (a) check-raise-specific frequency table reconsideration |
| Red-team | NaN safety across 4 layers (MUST #10 sub-2/3/4), Path (c) sidecar authoring as a silent-error risk, commit sequence for potential poisoning windows, coaching/ partial-delete importer risk |
| Practical pro | T_J01 reauthored values direction check, whether 5-entry dry-run covers realistic shapes, live-play vs labeller consistency for folded villains |
| Research | MUST #13 floor (10% vs tighter), MUST #6 equity-shift magnitude (4–12 vs 15+), mass-based vs count-based safety rail validation |

---

## 15. Scope + cost forecast

- Total lines of production code edit: ~400–500 lines across 12 files
- Total lines of test code added: ~600–800 lines
- Total lines of authored sidecar data: ~800–1000 lines
- Total blueprint v2 lines: ~1800 (this document)
- Implementation time: ~3–4 weeks serial per commit + reviewer pass
  - Commits 1–6 (code): ~2 weeks
  - Commits 7–9 (data plumbing + dry-run): ~3–4 days with owner gate
  - Commits 10–15 (cleanup + audits + sidecar authoring): ~1.5 weeks

Authoring sidecars is the critical-path item for Phase 2; mitigate with
parallel authoring passes (builder + GTO reviewer concurrent on 10-entry
batches).

---

## 16. Execution posture

**Blueprint v2 complete.** Single artifact replacing b1a9a91 wholesale.
23 MUSTs organized; original 5 retained with reconciliation tweaks;
reconciliation 14 + research 4 incorporated; Q15–Q19 resolutions
reflected; Q18/Q19 data-source plan documented (path (c) chosen);
commit sequence re-sequenced (CRIT #2 second); 4 coverage-gap tests
identified; M4 / M5 re-audit specs complete.

Ready for multi-agent reconciliation pass #2. If reconciliation produces
new MUSTs: re-cut blueprint v3 as single artifact (not patch-in-place).
If clean: implementation begins per §11 commit sequence.

No code edits until reconciliation signal. Standing by.
