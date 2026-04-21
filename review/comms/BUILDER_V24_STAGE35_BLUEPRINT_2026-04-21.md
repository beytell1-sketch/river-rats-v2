---
date: 2026-04-21
from: Builder (architect pass)
to: Orchestrator · GTO reviewer · Red-team reviewer · Architecture reviewer
re: Stage 3.5 single-artifact blueprint for 5 MUSTs + corpus load + re-audit
status: BLUEPRINT — awaiting multi-agent review reconciliation; no code edits yet
reference:
  - review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md (0276653)
  - review/comms/BUILDER_V24_STAGE35_HANDOFF_2026-04-21.md (f38d47a)
  - review/comms/BUILDER_V24_STAGE35_SPEC_LOCKED_2026-04-20.md
  - review/tests/range_narrowing_test_corpus_2026-04-20.yaml (81 cases)
---

# Stage 3.5 Blueprint — 5 MUSTs + Corpus + Re-audit

Single coherent blueprint per orchestrator directive. Each MUST specifies
exact file + line range, BEFORE code (verified at HEAD `12cb5d4`), AFTER
code, signature changes + affected callers, and rationale. No edits
land until multi-agent review approves or redirects.

Scope reminder (from reconciliation):
- CRITICAL #1 — Blocker features bypass chain
- CRITICAL #2 — Silent fallback when `_action_history` absent
- HIGH #3 — Check-raise sign flip
- HIGH #4 — FOLD re-fetch silent bug
- HIGH #5 — `surviving_weight` uses hand count, not mass
- Plus: load 81-case corpus as unit tests, re-run M4 + M5 audits

---

## 0. Summary — MUST → edit site → primary function

| MUST | Primary file | Line range | Functions touched |
|------|--------------|------------|-------------------|
| CRIT #1 | `river-rats-core/feature_extractor.py` | 1651–1754 | Step 12 `flush_block_pct`; Step 17 blocker features |
| CRIT #2 | `river-rats-core/feature_extractor.py` + 3 pipelines | 1116–1195, extract_features_parallel.py, extract_incremental.py, gauntlet_v5_37feat.py | `extract_range_composition`, training-data loaders |
| HIGH #3 | `river-rats-core/range_narrowing.py` | 695–843 | `narrow_by_action_history` per-street action pre-filter |
| HIGH #4 | `river-rats-core/feature_extractor.py` | 1182–1193 | post-chain FOLD fallback in `extract_range_composition` |
| HIGH #5 | `river-rats-core/range_narrowing.py` | 434–636, 695–843 | `narrow_to_betting_range` / `_checking_range` / `_continuing_range` thread weight-mass; `narrow_by_action_history` computes true surviving mass |
| Tests | `river-rats-core/tests/test_range_narrowing_stage35_corpus.py` (NEW) | — | 81-case pytest-parametrised consumer of corpus YAML |
| M4 re-audit | `review/run_stage35_backfill_audit.py` | expanded | also exercise Step 12 + Step 17 bypass path (pre/post) |
| M5 re-audit | `review/run_v231_anchor_recheck_stage35.py` | re-run | confirm 3/3 β-panel anchors still BET after fixes |

---

## 1. CRITICAL #1 — Blocker features bypass the chain

**File:** `river-rats-core/feature_extractor.py`
**Line range:** 1651–1754 (Step 12 block at 1651–1688, Step 17 block at 1729–1754)

### Why this MUST exists

`extract_range_composition` (line 1116) calls `narrow_by_action_history` at line 1174 and then `narrow_to_betting_range` at line 1193, producing a chain-narrowed villain range used for composition features (`_villain_top_pair_plus_pct`, etc.).

But Step 12 (line 1664) and Step 17 (line 1742) **re-call `get_villain_range()`** and apply only the single-street `narrow_to_betting_range`, ignoring the chain. Result: `flush_block_pct`, `nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct` are computed against an **un-chained** range while the composition features on the same hand see the **chained** range. Teaching displays both — an internal contradiction like SHAP-vs-action.

### BEFORE (current HEAD `12cb5d4`, lines 1651–1754)

```python
# Step 12: New features 46-48 (flush_block_pct, overcard_outs,
#          improvement_probability)
# These are ADDITIVE — they do not touch any existing feature computation.
hero_cards = features.get('_hero_cards', [])
board_cards = features.get('_board_cards', [])

# Reconstruct villain range the same way extract_range_composition does,
# so flush_block_pct uses the narrowed (betting) range.
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

# ... board suit-counts then flush_block_pct / overcard_outs / improvement_probability ...

# Step 17: v2.4 P1 blocker-direction features (56-59)
# ... uses _s12_v_range (still un-chained at this point) ...
features[F.NUT_FLUSH_BLOCK] = compute_nut_flush_block(hero_cards, board_cards)
_s17_block = compute_block_percentages(hero_cards, board_cards, _s12_v_range)
features[F.FLUSH_DRAW_BLOCK_PCT] = _s17_block['flush_draw_block_pct']
features[F.STRAIGHT_DRAW_BLOCK_PCT] = _s17_block['straight_draw_block_pct']
features[F.NUT_MADE_BLOCK_PCT] = _s17_block['nut_made_block_pct']
```

### AFTER

Two-step change. (1) Thread the chain-narrowed range out of `extract_range_composition`. (2) Consume it in Step 12 + Step 17.

**Step A — `extract_range_composition` returns the narrowed range in its metadata dict (line 1262–1272):**

```python
return {
    '_villain_top_pair_plus_pct': tp_pct,
    '_villain_draw_pct': draw_pct,
    '_villain_air_pct': air_pct,
    '_villain_medium_made_pct': medium_made_pct,
    '_villain_range_capped': range_capped,
    '_board_favour': board_favour,
    # v2.4 Stage 3.5 metadata
    '_villain_range_chain_steps': chain_steps,
    '_villain_range_chain_truncated': chain_truncated,
    # CRITICAL #1 fix: publish the narrowed range for downstream consumers
    # (Step 12 flush_block_pct, Step 17 blocker features). Carried as a
    # metadata field so model features stay scalar.
    '_villain_range_narrowed': v_range,
    # HIGH #4 fix (see §4): folded-villain sentinel
    '_villain_folded': villain_folded,
    # CRITICAL #2 fix (see §2): provenance for audit
    '_action_history_present': bool(action_history),
}
```

**Step B — Step 12 + Step 17 consume the narrowed range instead of re-fetching (lines 1651–1754 replaced):**

```python
# Step 12 + 17: features that measure blocker effects against villain's
# range. Consume the SAME chain-narrowed range as the composition
# features (propagated through _villain_range_narrowed by
# extract_range_composition). No independent range reconstruction —
# all villain-range-derived features share one source of truth.
hero_cards = features.get('_hero_cards', [])
board_cards = features.get('_board_cards', [])

# HIGH #4 fix: skip blocker + composition-dependent features when
# villain folded on a prior street. Features are emitted as NaN so
# downstream can detect the sentinel rather than silently reading 0.
_villain_folded = bool(features.get('_villain_folded', False))

_v_range_narrowed = features.get('_villain_range_narrowed', None) or {}

# Board suit counts (shared between flush_block_pct and Step 17)
if board_cards:
    _s12_analysis = analyze_board_cached(tuple(board_cards))
    _s12_suit_counts = _s12_analysis.suit_counts
else:
    _s12_suit_counts = {}

if _villain_folded:
    features[F.FLUSH_BLOCK_PCT] = float('nan')
    features[F.NUT_FLUSH_BLOCK] = 0
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
        # Defensive: never fail feature extraction on blocker computation.
        features[F.NUT_FLUSH_BLOCK] = 0
        features[F.FLUSH_DRAW_BLOCK_PCT] = 0.0
        features[F.STRAIGHT_DRAW_BLOCK_PCT] = 0.0
        features[F.NUT_MADE_BLOCK_PCT] = 0.0

# overcard_outs + improvement_probability are hero-only; unaffected
features[F.OVERCARD_OUTS] = compute_overcard_outs(
    hero_cards, features.get('high_card_rank', 14)
)
features[F.IMPROVEMENT_PROBABILITY] = compute_improvement_probability(
    hero_cards, board_cards, features.get('hand_category', 0)
)
```

### Signature changes + affected callers

- `extract_range_composition` — return dict adds three keys: `_villain_range_narrowed`, `_villain_folded`, `_action_history_present`. **Additive only.** Callers that `features.update(range_feats)` (the only caller, at line 1636) pick up the new fields automatically.
- Public `compute_flush_block_pct`, `compute_block_percentages`, `compute_nut_flush_block` — **unchanged signatures**. They already accept a range dict; the fix is what we feed them, not their API.
- `_s12_*` locals are deleted; `_v_range_narrowed` reads from features dict.

### Decision points for reviewers

- **Q1 (architect):** Acceptable to carry the narrowed range as a metadata field on the feature dict? Alternative is a second function call (`_get_narrowed_villain_range(hand, features)`) that re-does the chain — but that double-computes the chain and diverges at the first refactor.
- **Q2 (red-team):** NaN propagation for folded villains — does downstream (training CSV writer, gto_model.predict, SHAP) handle NaN gracefully, or do we need a different sentinel? Current `gto_model.py:192` suggests feature-width checks, not NaN checks; needs confirmation.
- **Q3 (GTO):** For folded villain, are blocker features meaningfully NaN or should they be 0? NaN = "question not applicable"; 0 = "hero blocks nothing". Recommend NaN for semantic correctness + downstream audit; GTO reviewer can confirm.

---

## 2. CRITICAL #2 — Silent fallback when `_action_history` absent

**File:** `river-rats-core/feature_extractor.py` (emit point) + 3 training-data pipelines (population points)
**Line range:** `extract_range_composition` 1167–1188; pipelines listed in §2.3

### Why this MUST exists

`_action_history` is populated by `game_state_bridge.py:184` for live-play / factory runs. Training-data pipelines — `extract_features_parallel.py`, `extract_incremental.py`, `gauntlet_v5_37feat.py` — call `extract_all_features(hand)` where `hand` comes from gauntlet / PokerBench parsing. **None of those paths populate `_action_history`.**

When absent, `extract_range_composition` silently falls through the `if action_history:` branch (line 1172) and runs pre-Stage-3.5 behavior. Stage 4 re-label would produce a **mixed** training distribution: chained-narrowed for the playtest-sourced hands + non-chained for every gauntlet/PokerBench row. Model learns the mixture — same failure mode as v2.3.2.

### 2.1 AFTER — `extract_range_composition` emits loud warning

Insert at line 1168 (immediately before the `if action_history:` branch):

```python
# CRITICAL #2 fix: loud surfacing when action_history is missing.
# Controlled by env var so live-play callers (bridge always populates
# _action_history) don't spam logs; training/audit paths set this to
# force a warning or raise.
#
# STAGE4_STRICT_ACTION_HISTORY semantics:
#   unset / "0" — silent fallback (back-compat for legacy callers)
#   "warn"      — emit logging.WARNING once per call with hand id
#   "raise"     — raise RuntimeError (for Stage 4 re-label + training)
_action_history_present = bool(action_history)
if not _action_history_present:
    _strict = os.environ.get('STAGE4_STRICT_ACTION_HISTORY', '0').lower()
    if _strict == 'raise':
        raise RuntimeError(
            f'extract_range_composition: action_history missing at '
            f'board={board_cards!r} hero={hero_pos} villain={villain_pos}; '
            f'STAGE4_STRICT_ACTION_HISTORY=raise is set. This is the '
            f'v2.3.2 silent-fallback failure mode.'
        )
    elif _strict in ('warn', '1'):
        import logging
        logging.getLogger(__name__).warning(
            'extract_range_composition: action_history MISSING — falling '
            'back to pre-Stage-3.5 single-street behavior. board=%r '
            'hero=%s villain=%s', board_cards, hero_pos, villain_pos,
        )
```

Plumb `_action_history_present` through to the returned dict (already covered in §1's return-block change).

### 2.2 AFTER — training CSV writers capture the flag

Training-data pipelines that write to CSV must emit `_action_history_present` as a column so post-hoc audits can filter.

**`extract_features_parallel.py` (line 29 MODEL_COLUMNS + loop at 54–84):**

```python
# Add column at the END so existing models reading MODEL_COLUMNS[:-1] as
# features still work. The model trainer reads _action_history_present
# from the separate audit column, NOT from the feature matrix.
MODEL_COLUMNS = [
    # ... existing 37 feature columns unchanged ...
    'action',
    '_action_history_present',  # audit column, not a model feature
]
```

In `process_chunk`:
```python
row = []
for col in MODEL_COLUMNS[:-2]:  # features only
    row.append(float(feat[col]))
row.append(action_val)
row.append(int(feat.get('_action_history_present', 0)))  # audit
rows.append(row)
```

**`extract_incremental.py` (line 59 header + line 89):**
```python
header = list(FEATURE_COLUMNS) + ['action_label', 'size_bucket', '_action_history_present']
# ...
rows.append(vec + [action, size_bucket, int(feat.get('_action_history_present', 0))])
```

**`gauntlet_v5_37feat.py` (line 161 consumer):** same additive column.

### 2.3 CRITICAL #2 audit plan — pipelines grep

| Pipeline / caller | File:line | Populates `_action_history`? | Action |
|---|---|---|---|
| Live / factory game | `river-rats-core/game_state_bridge.py:184` | **YES** (flattens `game.street_actions`) | No change (canonical path) |
| Training — gauntlet 500k | `river-rats-core/extract_features_parallel.py:64,70` | **NO** (hand from `gauntlet_500k.json`; no action field) | Requires source-schema decision (below) |
| Training — PokerBench | `river-rats-core/extract_incremental.py:22,88` | **NO** (hand from `parse_pokerbench_line`; single decision point, no history) | Requires source-schema decision |
| Training — v5 gauntlet | `river-rats-core/gauntlet_v5_37feat.py:48,161` | **NO** | Requires source-schema decision |
| Reference eval | `river-rats-core/reference_evaluator.py:492,797` | **NO** (FB JSONL records) | Warn-only OK for eval, not strict |
| Calibration | `river-rats-core/calibration_exam.py:300` | **NO** (hand built per-fixture) | Warn-only OK; anchors run in HU context |
| Sizing trainer | `river-rats-core/train_sizing_model.py:140` | **NO** | Warn-only OK; sizing trained separately |
| Hand explainer | `river-rats-core/explain_hand.py:422` | **NO** (used for display only) | Warn-only OK |
| Reference eval (2nd site) | `river-rats-core/coaching/feature_extractor.py:1294,1312` | **NO** (duplicate file, duplicate risk) | Warn-only; also audit for staleness |

### 2.4 Expected `_action_history_present` distribution per pipeline

| Pipeline | Pre-fix distribution | Post-fix (with `STAGE4_STRICT_ACTION_HISTORY=raise`) |
|---|---|---|
| Live / factory / playtest | 100% present | 100% present |
| Gauntlet / PokerBench training | 0% present (silent) | **Run aborts** — forces decision: reconstruct `_action_history` from source logs OR accept non-chained training data for those rows and mark in CSV |
| Eval / calibration (read-only) | 0% present (silent) | Still runs; warn-only path |

### 2.5 Owner decision queued (flag for orchestrator)

Training pipelines for Stage 4 re-label **must** either:
- (a) Reconstruct `_action_history` from the source `gauntlet_500k.json` / PokerBench records, OR
- (b) Ship with `_action_history_present=False` rows marked in CSV, re-label only on `True` rows, and train on the resulting subset.

This is an **architecture decision the MUSTs don't resolve**. Flagged for orchestrator + multi-agent review. Recommend (a) when the source format contains per-street action sequences (PokerBench does; gauntlet_500k format unknown — escalate for inspection). Otherwise (b) with explicit rejection of `False` rows during Stage 4 re-label.

### Signature changes + affected callers

- `extract_range_composition` — return dict adds `_action_history_present` (already covered in §1)
- `MODEL_COLUMNS` in `extract_features_parallel.py` — additive column at end; old model inference unaffected (it reads `FEATURE_COLUMNS`, not the CSV header)
- Training CSV schema bump — document in `docs/training-data-schema.md` if it exists; flag if it doesn't

### Decision points for reviewers

- **Q4 (architecture):** Environment variable as the switch, or function parameter? Env variable is terser but global-state-y; parameter requires plumbing through `extract_all_features(hand, strict=...)`. Recommend env for MVP; parameterise if Stage 5 training wants finer control.
- **Q5 (orchestrator):** Path (a) vs (b) for gauntlet / PokerBench retrofit — who owns that inspection?

---

## 3. HIGH #3 — Check-raise sign flip

**File:** `river-rats-core/range_narrowing.py`
**Line range:** 695–843 (`narrow_by_action_history`); new helper at ~760–775

### Why this MUST exists

Current chain applies each per-street villain action sequentially (line 781–800). For a check-raise line (villain CHECK then RAISE on the same street after hero bets), both narrowings apply:
1. `narrow_to_checking_range` first (mediums UP, nuts DOWN)
2. `narrow_to_betting_range` second (nuts UP, mediums DOWN-ish)

The combined distribution is **roughly preserved** at population level but the first narrowing's re-normalization truncates hands that would have survived in a pure raise-only narrowing. Check-raise range IRL is ~60–80% nuts / strong_value. The chain produces a medium-heavy distribution because the CHECK step re-weights mediums up at step 1 and the subsequent BET narrowing can't un-concentrate the distribution.

Reviewer's call: **option (b) — treat check-raise as the raise only**, skipping the CHECK when followed by BET/RAISE on the same street.

### BEFORE (`range_narrowing.py:763–801`)

```python
for street in STREET_ORDER:
    if street == decision_street:
        break

    # Collect villain's actions on this prior street, in order
    villain_street_actions = []
    for entry in action_history:
        normed = _normalize_action_entry(entry)
        if normed.get('street') == street and normed.get('position') == villain_pos.upper():
            villain_street_actions.append(normed)

    if not villain_street_actions:
        continue

    street_board = _street_board(board, street)

    for act in villain_street_actions:
        narrow_class = _action_to_narrow(act.get('action', ''))
        if narrow_class == 'fold':
            return {}, { ... }
        if narrow_class == 'bet':
            current_range = narrow_to_betting_range(current_range, street_board, street)
            steps.append(f'{street}:BET')
        elif narrow_class == 'check':
            current_range = narrow_to_checking_range(current_range, street_board, street)
            steps.append(f'{street}:CHECK')
        elif narrow_class == 'call':
            current_range = narrow_to_continuing_range(current_range, street_board, street)
            steps.append(f'{street}:CALL')
        else:
            continue
        # ... safety rails ...
```

### AFTER

Add pre-filter that collapses CHECK-followed-by-RAISE/BET on same street into the aggressive action alone. Insert after the `villain_street_actions` list is built (line 775) and before the action loop (line 781):

```python
    # HIGH #3 fix — check-raise sign flip.
    # When villain's same-street action sequence is [CHECK, BET/RAISE, ...],
    # the CHECK is a sandbag in front of an aggressive action. Treating the
    # pair as two separate narrowings produces an inverted composition
    # (mediums up from the CHECK step, then normalized down by the BET
    # step — but the intermediate normalisation loses nuts mass).
    # A check-raise is a concentrated-value action; semantically closer
    # to a single raise. Skip the CHECK entry when the next same-street
    # action is BET or RAISE.
    #
    # ALTERNATIVE (a) — check-raise-specific frequency table
    # (CHECK_RAISE_BETTING_FREQUENCIES with nuts:0.85, strong_value:0.75,
    # bluff:0.10, medium_made:0.05). Richer, but requires introducing a
    # new category of narrowing + solver-grounded calibration. Deferred
    # to v2.5 unless GTO reviewer redirects. See:
    # review/comms/TICKET_V25_PRO_LEVEL_NARROWING_GAPS_2026-04-20.md
    filtered_actions = []
    for i, act in enumerate(villain_street_actions):
        nc = _action_to_narrow(act.get('action', ''))
        next_nc = (
            _action_to_narrow(villain_street_actions[i + 1].get('action', ''))
            if i + 1 < len(villain_street_actions) else None
        )
        if nc == 'check' and next_nc == 'bet':
            # Skip — the check-raise is the concentrated-value action;
            # the RAISE narrowing alone captures it.
            continue
        filtered_actions.append(act)
    villain_street_actions = filtered_actions
```

The action loop then runs unchanged, but on the filtered list.

### Signature changes + affected callers

None. `narrow_by_action_history` signature unchanged. Internal-only.

### Test plan

- Corpus **B. Double-action per street** (5 cases at `T_B01`–`T_B05`) — gates this MUST. `T_B01` and `T_B04` are the check-raise shapes; pre-fix composition expected to be medium-heavy, post-fix expected ~60–80% nuts/strong_value.
- Corpus **K. Extra breadth** `T_K04_checkraise_then_call_turn_bet`, `T_K11_checkraise_fold_flop_river_na`, `T_K20_deep_chain_flop_bet_turn_raise_river_bet` — cross-checks.
- The existing 16-test `test_deep_chain_safety_rail` (uses check-raise shape in setup) should still pass.

### Decision points for reviewers

- **Q6 (GTO):** Confirm option (b) is preferred for v2.4. Alternative (a) is documented but not implemented. GTO can redirect to (a) if the composition fidelity matters enough that a solver-calibrated table is worth the extra scope in v2.4.
- **Q7 (GTO):** Check-raise boundary handling — what about CHECK followed by CALL (check-call)? Current code applies both narrowings; the CALL narrowing is solver-weaker (heuristic) but semantically a check-call should also be treated as single-action (call-only). Recommend we apply the same collapse rule to `nc == 'check' and next_nc == 'call'` — worth explicit reviewer sign-off.

---

## 4. HIGH #4 — FOLD re-fetch silent bug

**File:** `river-rats-core/feature_extractor.py`
**Line range:** 1169–1195 (post-chain block inside `extract_range_composition`)

### Why this MUST exists

After `narrow_by_action_history` at line 1174, line 1186 checks `if not v_range:` and re-fetches `get_villain_range()` un-narrowed. `narrow_by_action_history` returns `{}` for folded villains (see `range_narrowing.py:783–789`) and this re-fetch erases that sentinel, causing villain-composition features to compute against the full preflop range of a folded villain. Wrong.

### BEFORE (`feature_extractor.py:1169–1195`)

```python
# v2.4 Stage 3.5: action-aware chaining (prior streets only).
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
    # If chain produced empty range (villain folded on a prior street,
    # which should never happen if we got here, but guard anyway), fall
    # back to unnarrowed preflop range to avoid zeroing composition.
    if not v_range:
        v_range = get_villain_range(hero_pos, villain_pos, opener_pos=opener_pos)

# Current-street facing-bet filter — same gate as pre-Stage-3.5 for
# decisions where hero faces a live bet. Applied AFTER the prior-street
# chain so the bet filter runs on the post-chain range.
if facing_bet:
    v_range = narrow_to_betting_range(v_range, board_cards, street_name)
```

### AFTER

```python
# v2.4 Stage 3.5: action-aware chaining (prior streets only).
chain_steps: List[str] = []
chain_truncated = False
villain_folded = False
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
    # HIGH #4 fix — distinguish "chain returned empty because villain
    # folded" from "chain produced empty range through over-narrowing".
    # narrow_by_action_history explicitly emits chain_steps ending in
    # ":FOLD" for the former. Do NOT re-fetch the preflop range in
    # that case — villain is out of the hand; composition features
    # must be sentinel-flagged rather than silently computed.
    if not v_range:
        _last_step = chain_steps[-1] if chain_steps else ''
        if _last_step.endswith(':FOLD'):
            villain_folded = True
            # Keep v_range empty; composition loop will short-circuit.
        else:
            # Over-narrowing fallback — preserve pre-fix behavior, but
            # raise visibility so Stage 4 audit catches it.
            import logging
            logging.getLogger(__name__).warning(
                'extract_range_composition: chain over-narrowed to empty '
                'without FOLD; falling back to unnarrowed preflop range. '
                'hero=%s villain=%s board=%r chain_steps=%r',
                hero_pos, villain_pos, board_cards, chain_steps,
            )
            v_range = get_villain_range(
                hero_pos, villain_pos, opener_pos=opener_pos
            )

# Current-street facing-bet filter — but only when villain is still
# in the hand.
if facing_bet and not villain_folded:
    v_range = narrow_to_betting_range(v_range, board_cards, street_name)
```

Then the composition loop (line 1196) already handles empty `v_range` correctly (`total_weight` stays 0 → all pct = 0). The returned dict must include `villain_folded` so Step 12 + Step 17 (see §1) can NaN-flag:

```python
# Already covered in §1's return block:
'_villain_folded': villain_folded,
```

### Signature changes + affected callers

- `extract_range_composition` — return dict adds `_villain_folded: bool` (covered in §1).
- No external API change.

### Decision points for reviewers

- **Q8 (GTO):** For folded villains the current behavior (zeroed composition) is arguably correct — composition features against "no villain" are 0. Is there value in distinguishing folded-villain from degenerate-narrowing at the feature level, or is zero sufficient? Architecture Q5 from the reconciliation recommended explicit sentinel for downstream SHAP interpretability; GTO can confirm the training impact.
- **Q9 (red-team):** The over-narrowing fallback preserves pre-fix behavior (re-fetch). Is this the right call, or should over-narrowing also NaN-flag? Recommendation: keep fallback + WARN for v2.4 (don't change two things at once), revisit after corpus tests.

---

## 5. HIGH #5 — `surviving_weight` uses hand count, not mass

**File:** `river-rats-core/range_narrowing.py`
**Line range:** 434–636 (each narrow function) + 695–843 (`narrow_by_action_history`)

### Why this MUST exists

`surviving_weight` is currently computed at line 839 as `float(len(current_range)) / max(1, len(full_range))` — hand COUNT ratio. A 3-hand range each at freq 0.33 passes the 5% floor test (line 820 — actually that test is `len(current_range) < 3`, which is also count-based) but is semantically a collapsed distribution. Floor rail gives false OK.

True surviving weight is the ratio of un-normalized probability mass after each narrow step to the original input mass. Each `narrow_*` function currently re-normalizes its output to sum to 1.0, so the mass is lost at the function boundary.

### BEFORE

**`narrow_to_betting_range` (434–495), `narrow_to_checking_range` (498–559), `narrow_to_continuing_range` (582–636):**

Each has:
```python
# Normalize to maintain probability distribution
if total_weight > 0:
    for hand in out_range:
        out_range[hand] /= total_weight

return out_range
```

Un-normalized `total_weight` is discarded.

**`narrow_by_action_history` (line 836–842):**
```python
meta = {
    'surviving_weight': float(len(current_range)) / max(1, len(full_range)),
    'chain_steps': steps,
    'truncated': truncated,
}
```

### AFTER

**Step A — each `narrow_*` returns a `(range, surviving_fraction)` tuple.** New API:

```python
def narrow_to_betting_range(
    full_range: Dict[str, float],
    board: List[str],
    street: str = 'flop',
) -> Tuple[Dict[str, float], float]:
    """... (docstring updated) ...
    Returns:
        (betting_range, surviving_fraction)
        surviving_fraction: fraction of input PROBABILITY MASS that
            survived narrowing (not count).
    """
    # ... existing body through the per-hand loop ...

    original_weight = sum(freq for freq in full_range.values() if freq > 0)
    if original_weight <= 0:
        return full_range, 0.0

    # Normalize to maintain probability distribution, but capture the
    # un-normalized mass first so callers can compute true surviving
    # weight across a chain.
    surviving_mass = total_weight  # pre-normalization
    if total_weight > 0:
        for hand in betting_range:
            betting_range[hand] /= total_weight

    return betting_range, (surviving_mass / original_weight)
```

Same pattern for `narrow_to_checking_range` and `narrow_to_continuing_range`.

**Step B — `narrow_by_action_history` threads the fraction across steps.**

```python
cumulative_surviving = 1.0
# ... existing chain loop ...

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

    # Safety rails (empty-chain, weight-floor) — now MASS-based:
    if not current_range:
        # ... existing revert + break ...

    if cumulative_surviving < _STAGE35_WEIGHT_FLOOR_PCT:
        import logging
        logging.getLogger(__name__).warning(
            'narrow_by_action_history: cumulative surviving mass %.3f '
            'below floor %.3f after %s; reverting to last valid',
            cumulative_surviving, _STAGE35_WEIGHT_FLOOR_PCT,
            steps[-1] if steps else '?',
        )
        current_range = last_valid_range
        truncated = True
        break

    last_valid_range = dict(current_range)
```

Final meta:
```python
meta = {
    'surviving_weight': cumulative_surviving,  # TRUE mass, 0.0–1.0
    'chain_steps': steps,
    'truncated': truncated,
}
```

### Signature changes + affected callers

- `narrow_to_betting_range` — return changes from `Dict[str, float]` to `Tuple[Dict[str, float], float]`. **Breaking change.** Affected callers:
  - `feature_extractor.py:503, 617, 805, 828, 1193` (all `_, _ = narrow_to_betting_range(...)` or tuple unpack)
  - `range_narrowing.py:791` (inside `narrow_by_action_history` — already updated)
  - `test_range_features.py:23` (discard the mass)
  - `test_board_adjusted_hrp.py`, other test files that call directly — greppable
- `narrow_to_checking_range` — same breaking change. Callers:
  - `range_narrowing.py:794` (internal)
- `narrow_to_continuing_range` — same breaking change. Callers:
  - `range_narrowing.py:797` (internal)

All external callers need tuple unpacking. Concretely in `feature_extractor.py`:
```python
# BEFORE: v_range = narrow_to_betting_range(v_range, board, street)
# AFTER:  v_range, _ = narrow_to_betting_range(v_range, board, street)
```

Mechanical edit across ~5 call sites in `feature_extractor.py` + ~3 test files.

### Decision points for reviewers

- **Q10 (architecture):** Breaking return type vs adding a second function (`narrow_to_betting_range_with_mass(...)`). Breaking is cleaner long-term (surviving mass is always relevant metadata) but churns callers. Recommend breaking for v2.4 since we're already touching those call sites for §1. Architecture reviewer can redirect if the call-site churn + test-file churn is judged too risky for Stage 3.5 scope.
- **Q11 (architecture):** Safety rail thresholds — `_STAGE35_WEIGHT_FLOOR_PCT = 0.05` is currently the count-floor proxy. With true mass, is 5% still the right threshold or should it tighten (1% / 2%)? Mass-based 5% is strictly more permissive than count-based — a range of 10 hands at uniform frequency narrowed to 2 hands of freq 0.04 each = mass 0.08 = pass, count 0.2 = also pass. Needs per-corpus-case calibration. Recommend: ship with 5% for consistency; document in M4 audit that the threshold may need tuning post-ship.

---

## 6. Cross-MUST edit-overlap map

Commit-order-aware view of where edits collide.

### 6.1 Overlap: HIGH #3 ↔ HIGH #5 (`range_narrowing.py` chain loop)

Both touch the per-action loop inside `narrow_by_action_history` (lines 781–829). Specifically:

| Lines | HIGH #3 change | HIGH #5 change |
|-------|----------------|----------------|
| 770–775 | Unchanged | Unchanged |
| ~778 (NEW) | Insert `filtered_actions` pre-filter pass (§3 AFTER) | — |
| 781 | Loop source: `filtered_actions` (per §3) instead of `villain_street_actions` | Same |
| 790–800 | Action branches unchanged | Each call unpacks `(range, surv)` tuple (per §5) |
| 802–832 | Safety rails — `if not current_range:` + truncation | Replace count-based `if len(current_range) < 3` with mass-based `if cumulative_surviving < _STAGE35_WEIGHT_FLOOR_PCT` |
| 836–842 | — | `surviving_weight` becomes true cumulative mass |

**Sequencing:** Land HIGH #5 FIRST (mechanical tuple-unpack across codebase + mass thread), THEN HIGH #3 (pre-filter pass on top of the new call pattern). Rationale: HIGH #3's pre-filter doesn't depend on HIGH #5's return type, but HIGH #5's safety-rail rewrite would churn again if we changed the action order afterward. Alternative order also works — HIGH #3 first, HIGH #5 as second — but more churn.

### 6.2 Overlap: CRIT #1 ↔ HIGH #4 (`feature_extractor.py:1169–1272` + Step 12/17)

Both edit `extract_range_composition` return dict + Step 12 / 17 consumption. Specifically:

| Lines | CRIT #1 change | HIGH #4 change |
|-------|----------------|----------------|
| 1169–1195 | No change (just reads `v_range` after chain) | Add `villain_folded` flag based on `chain_steps[-1] == ':FOLD'` |
| 1262–1272 | Add `_villain_range_narrowed` to return | Add `_villain_folded` to return |
| 1651–1754 | Consume `_villain_range_narrowed` in Step 12 + 17; delete `_s12_*` reconstruction | Short-circuit blocker features to NaN when `_villain_folded` |

**Sequencing:** CRIT #1 + HIGH #4 can land in one commit (same function, same return-dict surgery) OR two commits (CRIT #1 first for isolation). Per orchestrator directive "one MUST per commit", they land separately — CRIT #1 first, HIGH #4 second. HIGH #4 adds one extra field to the return dict and one extra branch in Step 12/17 — minor additional edit.

### 6.3 Overlap: CRIT #2 ↔ CRIT #1 (`extract_range_composition` return)

CRIT #2 adds `_action_history_present` to the return dict; CRIT #1 adds `_villain_range_narrowed`. Additive, no conflict. Can land in either order.

### 6.4 No overlap

- HIGH #5 touches `range_narrowing.py` and tuple-unpack sites in `feature_extractor.py:503, 617, 805, 828, 1193`. The Step 12 in-line `narrow_to_betting_range` call at 1669–1671 is **deleted** by CRIT #1, so HIGH #5 doesn't need to update that call site if CRIT #1 lands first.

**Recommended commit order** (one MUST per commit, per directive):
1. HIGH #5 (mass threading — foundational; every other MUST can use `surviving_weight` for its own verification)
2. HIGH #3 (check-raise pre-filter, builds on HIGH #5's tuple API)
3. CRIT #1 (blocker features consume chain; deletes Step 12's obsolete narrow call — removes one HIGH #5 churn site)
4. HIGH #4 (folded-villain sentinel, small extension of CRIT #1's return dict)
5. CRIT #2 (silent-fallback audit + training-CSV schema bump; lands last because §2.5's owner decision must be resolved first)
6. Unit test corpus + audit re-runs

---

## 7. Unit test mapping — 81-case corpus → MUSTs

Corpus file: `review/tests/range_narrowing_test_corpus_2026-04-20.yaml`. New consumer: `river-rats-core/tests/test_range_narrowing_stage35_corpus.py` (pytest-parametrised).

| Corpus section | Cases | MUST gated |
|---|---|---|
| **A. Simple chains** (10) | `T_A01`–`T_A10` | Baseline `narrow_by_action_history` (existing + HIGH #5 mass) |
| **B. Double-action per street** (5) | `T_B01`–`T_B05` | **HIGH #3** (check-raise sign flip) |
| **C. CALL edge cases** (8) | `T_C01`–`T_C08` | `narrow_to_continuing_range` + chain (HIGH #5) |
| **D. Street-transition** (6) | `T_D01`–`T_D06` | Chain at decision-street boundary (existing) |
| **E. Multiway** (5) | `T_E01`–`T_E05` | Baseline + confirms multiway primary-villain selection |
| **F. Board-texture** (10) | `T_F01`–`T_F10` | Baseline; catches regressions by category |
| **G. Position variety** (5) | `T_G01`–`T_G05` | Baseline; confirms `villain_pos` filter in chain |
| **H. Anchor regression** (5) | `T_H01`–`T_H05` | **M5 β-panel anchors** + CRIT #1 composition fidelity |
| **I. Safety rails** (3) | `T_I01`–`T_I03` | **CRIT #2** (`T_I01` missing action_history), **HIGH #4** (`T_I03` folded midchain) |
| **J. Owner-sourced canonical** (3) | `T_J01`–`T_J03` | **CRIT #1** (`T_J03` blocker mid-pair flush blocker), end-to-end realism |
| **K. Extra breadth** (20) | `T_K01`–`T_K20` | Rounds out coverage — check-raise (K04, K11, K20), deep chain (K20), malformed (K18), tuple form (K17), baseline weight (K16) |

### Coverage gaps — additional cases to author

Reviewing MUSTs vs corpus, these gaps exist:

| MUST | Gap | Required additional case |
|---|---|---|
| **CRIT #1** | Corpus tests `narrow_by_action_history` in isolation; no case gates the `feature_extractor.py::Step 12/17` bypass itself. | Add `test_step12_uses_chain_narrowed_range` (integration test at `test_range_features.py`): build a hand with `_action_history` = flop-check-check, turn-bet-call, and assert `FLUSH_BLOCK_PCT` computed post-chain differs from the un-chained value (pre-fix should be one; post-fix should be the other). |
| **CRIT #2** | `T_I01` covers the missing-action-history fallback inside `narrow_by_action_history`. Doesn't cover the env-var gate at `extract_range_composition`. | Add `test_stage4_strict_action_history_raises` and `test_stage4_strict_action_history_warns` as unit tests in `test_range_features.py`. |
| **HIGH #3** | `T_B01`, `T_B04` exist but lack mirror cases for CHECK-CALL (Q7). | If Q7 resolves as "collapse check-call too", add one case there. |
| **HIGH #5** | Corpus doesn't assert surviving_weight numerically. | Add `test_surviving_weight_is_mass_not_count` (direct) with a synthetic 10-hand range where count-fraction and mass-fraction diverge. |

### Replaces the existing 16-test file?

Existing file: `river-rats-core/tests/test_range_narrowing_stage35.py` (325 lines, 16 tests).

**Recommendation: KEEP and extend.** The 16 tests exercise module-level constants (M1 freq tables, tuple-action-history acceptance, schema-mismatch guard). The corpus exercises full-chain behavior on realistic hand shapes. Two files, both pass, different layers of coverage. The corpus file is a new pytest-parametrised module that loads the YAML and asserts expected_composition_post_fix.

### Decision points for reviewers

- **Q12 (tester):** Corpus expected values are labeled `[approx]` per the YAML header — refinement to actual output required in CI. Recommend: first pass asserts "post-fix value differs from pre-fix value by at least X%" (direction test) rather than exact match; calibrate exact values in a follow-up after the implementation is merged.

---

## 8. M4 re-audit scope expansion

**File:** `review/run_stage35_backfill_audit.py`
**Pre-fix baseline:** 579 rows, 0/124 flop isolation violations, 455/455 chain firing on composition features.

### Why re-audit

The pre-fix M4 audit passed because it only exercised the **composition-features path** (which already goes through `classify_villain_range`'s chain). The blocker-features bypass path (Step 12 + Step 17) was never instrumented. Post-fix M4 must exercise the bypass path too.

### Audit expansion

Add these checks:

1. **Step 12 + Step 17 chain-consumption check:**
   - For every row with `_action_history_present=True` and non-empty `_villain_range_chain_steps`, compute `FLUSH_BLOCK_PCT` both via the current code path (chain-consumed) AND via the pre-fix bypass path (reimport `get_villain_range` + `narrow_to_betting_range` only).
   - **Pre-patch expectation:** non-zero rows where the two differ (validating the bug exists on production data). Expected count: `455` rows (same as chain-firing count on composition features).
   - **Post-patch expectation:** `0` rows where the two differ (validating the fix).

2. **Blocker-feature NaN check (HIGH #4 interaction):**
   - Count rows where `_villain_folded=True`. Assert `FLUSH_BLOCK_PCT`, `FLUSH_DRAW_BLOCK_PCT`, `STRAIGHT_DRAW_BLOCK_PCT`, `NUT_MADE_BLOCK_PCT` are all NaN on those rows.
   - **Post-patch expectation:** `>= 1` row (if the 579-row sample contains any folded-villain shapes — verify via chain_steps).

3. **CRIT #2 column presence:**
   - Assert `_action_history_present` column exists in every backfill CSV.
   - Assert distribution across rows matches pipeline expectations (§2.4).

4. **Mass-based surviving-weight check (HIGH #5):**
   - Scan `_surviving_weight` in chain metadata (if propagated to CSV — recommend adding). Assert it's within [0.0, 1.0].
   - **Post-patch expectation:** surviving_weight strictly decreasing across chain steps; no entry at 0.0 except folded chains.

### Decision points for reviewers

- **Q13 (architecture):** Should `_surviving_weight`, `_chain_steps`, `_action_history_present` all be promoted to training-CSV columns for post-hoc audit, or kept as `_meta_` only? Recommend: promote to CSV for Stage 4 re-label only; keep out of model feature vector. Architecture reviewer can confirm CSV schema bump.

---

## 9. M5 anchor regression

**File:** `review/run_v231_anchor_recheck_stage35.py`
**Pre-fix baseline:** 3/3 β-panel anchors BET restored on v2.3.1 without retraining.

### Why re-audit

Fixes touch composition paths that anchors depend on. Must re-confirm post-fix.

### Re-run plan

- Run existing script as-is against v2.3.1 model after all 5 MUSTs land + tests green.
- **Expected:** 3/3 β-panel anchors still predict BET.
- **If any anchor flips to CHECK:** STOP and report. Possible causes: HIGH #3 check-raise pre-filter unexpectedly matches a non-check-raise shape (false positive); HIGH #5 mass threshold tightens enough to truncate an anchor hand's chain.

### Corpus anchor cases (Section H)

Five `T_H0N` cases in the corpus are built from β-panel + LITMUS anchors. Post-fix:
- `T_H01_anchor_d2410_CO_turn` — flop-check narrowing fires (same-street excluded on decision street); post-fix composition must match M5's stability claim.
- `T_H02_anchor_LITMUS_A4d_Qs5s7s_flop` — flop decision, no prior postflop; chain empty; composition unchanged.
- `T_H03_anchor_LITMUS_T5h_JJ2_flop` — same.
- `T_H04_anchor_LITMUS_AA_7h5d2c_flop` — same.
- `T_H05_anchor_LITMUS_KQ_KsTs3h_flop` — same.

Expected: corpus anchor cases assert *zero change* in composition pre-vs-post for flop-decision anchors. Validates the same-street exclusion is working.

---

## 10. Observability hooks

Per architecture SHIP_WITH_REFACTOR verdict, surface these via `_meta_` fields into the training CSV (for Stage 4 audit):

| Field | Source | CSV column? |
|---|---|---|
| `_villain_range_chain_steps` | `extract_range_composition` return | Yes (string representation) |
| `_villain_range_chain_truncated` | `extract_range_composition` return | Yes (int 0/1) |
| `_action_history_present` | `extract_range_composition` return (§2) | Yes (int 0/1) |
| `_villain_folded` | `extract_range_composition` return (§4) | Yes (int 0/1) |
| `_surviving_weight` | `narrow_by_action_history` meta (§5) | Yes (float) |
| `_villain_range_narrowed` | `extract_range_composition` return (§1) | No — too wide; used only by Step 12/17 within feature extraction |

Implementation: extend the training CSV writer in `extract_features_parallel.py` (and the other two pipelines) to append these as audit columns after the existing 37+ feature columns + action. Model inference unaffected.

---

## 11. Unplanned finding (NEW — for orchestrator escalation)

**Same-class bypass exists at 4 additional call sites in `feature_extractor.py`.** Not in the reconciliation's CRITICAL #1 scope. Surfaced during this architect pass.

| File:line | Function | What it does |
|---|---|---|
| `feature_extractor.py:500–505` | `compute_partition_features` (HU branch) | `v_range = get_villain_range(...); if facing_bet: narrow_to_betting_range(...)` — **no action_history chain** |
| `feature_extractor.py:605–617` | `get_multiway_villain_range` (inside `compute_partition_features` path) | Same pattern, multiway; narrows only the bettor, no chain |
| `feature_extractor.py:790–806` | Multiway equity path inside `compute_equity_features` | Same pattern |
| `feature_extractor.py:823–829` | HU equity path inside `compute_equity_features` | Same pattern |

These feed `raw_equity`, `equity_vs_range`, `better_hand_pct`, `worse_hand_pct`, `equity_margin`, and the partition features — all of which are **model features** (not just teaching metadata). Pre-Stage-3.5 behavior; chain-narrowing was added only to `extract_range_composition`.

### Two possible framings

**(A) In-scope for CRITICAL #1.** The reconciliation's phrasing was "all 10 villain-derived features inherit Stage 3.5". By that language, equity features are also villain-derived and should inherit. Fix would plumb `action_history` into `compute_partition_features` and `compute_equity_features` the same way `extract_range_composition` does.

**(B) Out-of-scope for v2.4.** Reconciliation's concrete fix-point was Step 12 + Step 17. Equity path has a very different risk profile — it's on the hot path (Monte Carlo 2000 trials per hand) and a chain-narrowed villain range will materially change `raw_equity` on every multi-street decision. That's a larger model-behavior change than the blocker features (which only feed SHAP + teaching + new v2.4 model training).

### My recommendation

**Document + defer for orchestrator + multi-agent review to decide.** Framing (B) is defensible for Stage 3.5 scope discipline; framing (A) is defensible for consistency with the "all villain-derived features inherit" claim. If deferred, add a v2.5 queue entry: `equity_features_inherit_chain_narrowing`. If included, this becomes a 6th MUST and requires its own re-audit + anchor regression run.

**Flag for multi-agent review:** GTO theorist should weigh composition-vs-equity feature equivalence. Red-team should assess blast radius — does Stage 4 re-label's training distribution for equity_vs_range change materially if we include this? Architecture should confirm plumbing feasibility.

---

## 12. STOP conditions + open questions

Per CLAUDE.md §5, implementation stops and reports if:
- File/line doesn't match blueprint (HEAD drift)
- Test corpus assertions fail in a way the blueprint didn't anticipate (§7 Q12 direction tests give us tolerance for value drift)
- M4 or M5 re-audit produces unexpected output
- Any MUST surfaces a new bypass site (cf. §11 finding — this would become the 7th, 8th, etc.)

**Open questions requiring reviewer input (consolidated):**

- Q1 (architecture): narrowed range as metadata field vs separate function? (§1)
- Q2 (red-team): NaN propagation through model inference + SHAP? (§1)
- Q3 (GTO): folded-villain blocker features NaN vs 0? (§1)
- Q4 (architecture): env var vs function parameter for STAGE4_STRICT? (§2)
- Q5 (orchestrator): gauntlet/PokerBench action_history retrofit path (a) vs (b)? (§2.5)
- Q6 (GTO): option (b) sufficient, or demand option (a) in v2.4? (§3)
- Q7 (GTO): apply same check-raise collapse rule to check-call? (§3)
- Q8 (GTO): folded-villain composition sentinel necessary? (§4)
- Q9 (red-team): over-narrowing fallback NaN-flag? (§4)
- Q10 (architecture): breaking return type on narrow_* vs new function? (§5)
- Q11 (architecture): _STAGE35_WEIGHT_FLOOR_PCT threshold revisit under mass semantics? (§5)
- Q12 (tester): corpus expected-value calibration strategy? (§7)
- Q13 (architecture): observability fields → CSV columns scope? (§8)
- **Q14 (orchestrator + GTO + red-team + architecture): §11 new finding — equity bypass in-scope or deferred to v2.5?** (High priority; affects sequencing)

---

## 13. Commit sequence (post-approval)

Per directive "one MUST per commit", in overlap-aware order:

1. `Stage 3.5 HIGH #5: narrow_* return mass; true surviving_weight thread` — foundational tuple-unpack + mass threading across `range_narrowing.py` + `feature_extractor.py` call sites + test file updates.
2. `Stage 3.5 HIGH #3: check-raise pre-filter (option b)` — new pass in `narrow_by_action_history`.
3. `Stage 3.5 CRITICAL #1: blocker features consume chain-narrowed range` — rewrite Step 12/17, thread `_villain_range_narrowed` through return dict.
4. `Stage 3.5 HIGH #4: folded-villain sentinel + NaN blocker features` — minor extension of CRITICAL #1's return dict + Step 12/17 short-circuit.
5. `Stage 3.5 CRITICAL #2: action_history missing audit + training CSV schema bump` — env-gated strict mode + `_action_history_present` column; pipelines audited.
6. `Stage 3.5 corpus: 81-case pytest consumer + coverage gap cases` — new test file.
7. `Stage 3.5 M4 re-audit: blocker bypass path instrumented` — extend `run_stage35_backfill_audit.py`.
8. `Stage 3.5 M5 re-run: 3/3 anchors post-fix` — re-run existing script, attach report.

Between each commit: reviewer pass from orchestrator against this blueprint. STOP if any commit's verification fails.

---

## 14. Requested from reviewers

- Architecture reviewer: Q1, Q4, Q10, Q11, Q13, Q14
- GTO reviewer: Q3, Q6, Q7, Q8, Q14
- Red-team reviewer: Q2, Q9, Q14
- Tester: Q12
- Orchestrator: Q5, Q14

Standing by. No code edits land until reconciliation is posted. If reconciliation produces new MUSTs or scope changes (especially on §11), this blueprint will be re-cut and re-submitted rather than patched in place — keeping a clean review trail.
