---
date: 2026-04-22
from: Builder (v2.3.1 fix-forward patch per pass #4 directive)
to: Orchestrator (single read-check, not full panel)
re: v2.3.1 patch — 8 new MUSTs (#60–#67) from reconciliation #4 + Q39–Q41 + physical SUPERSEDED markers on v2 + v2.2
status: PATCH — fix-forward on v2.3 amended (e940e8d); SUPERSEDED markers physically landed on v2 + v2.2 files
extends: review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_3_AMENDED_2026-04-22.md (e940e8d)
sources:
  - review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_PASS4_2026-04-22.md (a7fd1fe)
  - Origin verification at HEAD a7fd1fe
---

# Stage 3.5 — Blueprint v2.3.1 Patch

Per orchestrator pass-#4 directive (auto-mode). 8 new MUSTs (#60–#67):
3 CRITICAL spec-text fixes, 4 HIGH scope refinements, 1 MEDIUM
optional. All verified at origin; fix-forward on v2.3 amended.

**Active MUST count: 65** (57 from v2.3 + 8 new). Inactive: #24, #25.

Expected next step after push: **orchestrator-only read-check**, then
ALL-CLEAR + implementation begins. No full 5-panel dispatch unless
new CRITICAL surfaces.

---

## 1. Source verification

| MUST | File | Finding | Verified |
|------|------|---------|----------|
| #60 | v2.3 §2.2 lines 357-361 | `sorted({s for opp in per_villain_ranges for s in per_villain_truncated})` iterates Dict[str, bool] → position names not steps | ✓ |
| #60 | v2.3 §2.2 line 363 | `min(per_villain_truncated.values(), default=1.0)` min-over-bool returns bool | ✓ |
| #61 | v2 base line 942 | `raise NotImplementedError  # placeholder for blueprint` unmarked | ✓ verified on origin before patching |
| #61 | v2 base line 1728 | "13 call-site tuple-unpacks" — stale vs canonical 14 | ✓ |
| #61 | v2.2 amendment line 685 | `merged = {}` in multiway sketch without spec completion | ✓ |
| #62 | v2.3 lines 61-62, 115-117 | `_PRIMARY_STRINGS = frozenset({'PRIMARY', 'primary', 'Primary'})` — 3 literals only | ✓ |
| #65 | v2.3 line 454 | `_HELD_BACK = frozenset({'board_adjusted_hrp'})` hardcoded in assembler | ✓ |

All findings reproduce. Physical SUPERSEDED markers applied to v2 + v2.2 files as part of this commit (see §2.2).

---

## 2. CRITICAL (3)

### 2.1 MUST #60 — Fix §2.2 multiway aggregation spec bugs

Three fixes in one edit. Supersedes v2.3 §2.2 lines 357-365 AFTER block.

**AFTER — replacement for the broken `meta = {...}` assembly block:**

```python
    # Build per-villain chain-steps map — tracked as we iterate opponents
    per_villain_chain_steps: Dict[str, List[str]] = {}
    per_villain_metas: Dict[str, Dict] = {}

    for opp_pos in opponent_positions:
        # ... existing per-opponent narrowing loop (unchanged) ...
        per_villain_ranges[opp_pos] = opp_range
        per_villain_truncated[opp_pos] = opp_meta['truncated']
        per_villain_folded[opp_pos] = opp_meta['villain_folded']
        per_villain_overflowed[opp_pos] = opp_meta['chain_overflowed']
        per_villain_chain_steps[opp_pos] = opp_meta['chain_steps']
        per_villain_metas[opp_pos] = opp_meta
        # merged-range construction DELETED per MUST #64 (see §3.2)

    # Aggregate meta fields
    agg_truncated = any(per_villain_truncated.values())
    agg_overflowed = any(per_villain_overflowed.values())
    agg_folded = (
        all(per_villain_folded.values())
        if per_villain_folded else False
    )

    # MUST #60(a): chain_steps aggregation as flat list with pos-prefix
    # Example: ['BB:flop:CHECK', 'BB:turn:CALL', 'CO:flop:BET']
    agg_chain_steps: List[str] = [
        f'{opp}:{step}'
        for opp, steps in per_villain_chain_steps.items()
        for step in steps
    ]

    # MUST #60(b): surviving_weight as min across per-opponent metas
    # (captures tightest narrowing; joint survival would be product but
    # that double-counts independence assumptions).
    agg_surviving_weight = (
        min(m.get('surviving_weight', 1.0) for m in per_villain_metas.values())
        if per_villain_metas else 1.0
    )

    meta = {
        'chain_steps': agg_chain_steps,
        'truncated': agg_truncated,
        'surviving_weight': agg_surviving_weight,
        'villain_folded': agg_folded,
        'chain_overflowed': agg_overflowed,
        # MUST #46 + #60(c): callers consume per_villain_ranges directly;
        # merged-range deprecated per MUST #64.
        'per_villain_ranges': per_villain_ranges,
        'per_villain_chain_steps': per_villain_chain_steps,
        'per_villain_metas': per_villain_metas,  # full meta per opponent
        'per_villain_truncated': per_villain_truncated,
        'per_villain_folded': per_villain_folded,
        'per_villain_overflowed': per_villain_overflowed,
    }
    # MUST #64 (§3.2): return None for merged; callers raise if they try to use.
    return None, meta
```

**MUST #60(c) MED-B — v2.2 §3.7 BEFORE block deletion in commit 4 diff:**

Commit 4 (merged CRIT #1 + HIGH #4 + MUST #6 + #46 per MUST #59) must explicitly DELETE the v2.2 §3.7 placeholder sketch from the feature_extractor.py multiway branch (it's in the amendment doc, not in code yet, so the delete is cleaning up a sketch that never got implemented). Added to commit-4 todo list in §3.5 updated commit sequence.

### 2.2 MUST #61 — Physical SUPERSEDED markers on v2 + v2.2 (LANDED)

**Applied in this commit** — not just described. Physical file edits:

**`review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md`:**
- Line 942 (after `raise NotImplementedError`): inserted 3-line `⚠️ SUPERSEDED BY v2.2 AMENDMENT §3.7 (d7db3f1) + v2.3 AMENDMENT §2.2 (e940e8d) + v2.3.1 PATCH §M60 (this commit)` marker with explicit cross-reference and implementation guidance.
- Line 1728 (commit sequence table first row): inline annotation `⚠️ SUPERSEDED: canonical tuple-unpack count is 14 root+coaching + 5 test = 19 sites per v2.2 amendment §1.1 + v2.3 §2.3 canonical table + v2.3.1 §M61. The "13" figure here is stale; do not use.`

**`review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md`:**
- Before §3.7 "Implementation sketch" line 680: inserted 5-line `⚠️ SUPERSEDED BY v2.3 §2.2 + v2.3.1 PATCH §M60 + §M64` marker pointing at the three bugs (unpopulated-unreturned `merged`, dropped opp_meta, placeholder return comment) + the weight-avg-vs-deprecation resolution.

Verification: `git show origin/master:<path>` will show markers at cited lines after push.

### 2.3 MUST #62 — True case-insensitive helper

**AFTER — replacement for v2.3 §2.1 `_attention_value` helper + `_PRIMARY_STRINGS`/`_CONFIRMED_STRINGS` constants:**

```python
# MUST #62 — replace frozenset-of-3 with canonicalisation function.
# Handles all case variants + whitespace + fullwidth by normalising
# before comparison. No more silent-miss on PRiMARY, ' PRIMARY ', etc.

def _canonicalize_attention_value(val) -> Optional[int]:
    """MUST #62 — canonicalise any attention value (int or string)
    to tri-state {0, 1, 2} or None if missing.

    Handles:
      - None → None
      - int / float → clamp to {0, 1, 2}; raise if out of range
      - str → strip + upper; match PRIMARY/CONFIRMED/missing-class
      - any other type → raise RuntimeError

    Returns:
      2 (PRIMARY), 1 (CONFIRMED), 0 (missing/untagged), or None (not
      present in dict).
    """
    if val is None:
        return None

    if isinstance(val, bool):
        # bool is subclass of int — treat True=1 CONFIRMED, False=0
        return 1 if val else 0

    if isinstance(val, (int, float)):
        clamped = int(val)
        if clamped == 0:
            return 0
        if clamped == 1:
            return 1
        if clamped >= 2:
            return 2
        raise RuntimeError(
            f'MUST #62: attention int out of range (got {val!r}); '
            f'expected 0/1/2 or convertible.'
        )

    if isinstance(val, str):
        # MUST #62: strip whitespace + upper-case for canonical match.
        # Handles 'PRIMARY' / 'primary' / 'Primary' / 'PRiMARY' /
        # ' PRIMARY ' / 'primary\n' etc.
        s = val.strip().upper()
        if s == 'PRIMARY':
            return 2
        if s == 'CONFIRMED':
            return 1
        if s in ('', '0', 'FALSE', 'NONE'):
            return 0
        raise RuntimeError(
            f'MUST #62: unrecognised attention string {val!r} '
            f'(canonicalised to {s!r}); expected PRIMARY/CONFIRMED/empty.'
        )

    raise RuntimeError(
        f'MUST #62: attention value wrong type {type(val).__name__!r} '
        f'(value={val!r}); expected int, float, str, bool, or None.'
    )


def _attention_value(record: dict, feature_name: str,
                     mandatory: bool = False) -> int:
    """MUST #26 + #29 + #44 + #45 + #62 — bi-schema attention extractor.

    Replaces v2.3 frozenset-of-3 literals with full canonicalisation.
    Mixed-schema rejection: raise iff BOTH feature_attention AND
    attention_flags are non-empty dicts (empty-dict on either side
    is a legitimate migration artifact per pass #3 + MUST #62).
    """
    fa = record.get('feature_attention')
    af = record.get('attention_flags')

    # MUST #62: empty-dict-both treated as legitimate. Reject only when
    # BOTH are non-None AND at least one of each has a value.
    fa_populated = bool(fa)  # non-None and non-empty
    af_populated = bool(af)
    if fa_populated and af_populated:
        sid = record.get('situation_id', '<unknown>')
        raise RuntimeError(
            f'MUST #45+62: mixed-schema record sid={sid}: BOTH '
            f'feature_attention AND attention_flags non-empty. One-or-other, '
            f'not both. Fix the labeller output or reject the record.'
        )

    # Route to the populated schema
    source = fa if fa_populated else (af if af_populated else None)
    if source is None:
        return _missing_attention(record, feature_name, mandatory)

    val = source.get(feature_name, None)
    try:
        canon = _canonicalize_attention_value(val)
    except RuntimeError:
        # Unknown value → treat as missing + log WARN
        import logging
        logging.getLogger(__name__).warning(
            'MUST #62: feature %r has unrecognised attention value %r '
            'on sid=%s; treating as missing.',
            feature_name, val, record.get('situation_id', '<unknown>'),
        )
        return _missing_attention(record, feature_name, mandatory)

    if canon is None:
        return _missing_attention(record, feature_name, mandatory)
    return canon
```

`_missing_attention` function unchanged from v2.3 §2.1.

**Delete from v2.3:** `_PRIMARY_STRINGS` + `_CONFIRMED_STRINGS` frozenset constants (replaced by canonicalisation function).

---

## 3. HIGH (4)

### 3.1 MUST #63 — Cache per-hand invalidation contract

**Addition to v2.3 §2.2 / §3.7 helper spec:**

```python
def _get_chain_narrowed_villain_range(
    # ... all existing params ...
    cached_range: Optional[Dict[str, float]] = None,
    cached_meta: Optional[Dict] = None,
) -> Tuple[Optional[Dict[str, float]], Dict]:
    """...

    Cache contract (MUST #34 + MUST #63):
    - Cache is LOCAL to a single `extract_all_features(hand)` call.
      Helper populates cache at first-compute; caller retains reference
      for subsequent calls WITHIN the same extract_all_features invocation
      (composition → equity → partition → explain_hand).
    - NO module-level cache. NO cross-hand reuse. If the caller persists
      cached_range across hands, the second hand's chain-narrowing is
      SILENTLY WRONG.
    - extract_all_features(hand) creates a local dict `_chain_cache`
      scoped to the function; passes cached_range from it; discards on
      return. Per-hand invalidation by construction.
    """
    # MUST #63: defensive assertion — cached_range + cached_meta either
    # both present or both absent. Mismatched pairs indicate misuse.
    if (cached_range is None) != (cached_meta is None):
        raise RuntimeError(
            'MUST #63: cache contract violation — cached_range and '
            'cached_meta must be provided together or not at all. '
            'Likely a caller bug; investigate before continuing.'
        )

    if cached_range is not None:
        return cached_range, cached_meta
    # ... rest unchanged ...
```

**Caller side (`extract_all_features` in `feature_extractor.py`):**

```python
def extract_all_features(hand: Dict) -> Dict:
    # ... existing setup ...

    # MUST #63: per-hand cache — LOCAL to this function call.
    _chain_cache: Dict[str, Any] = {'range': None, 'meta': None}

    # Step 8/9 range composition (first-compute + populate cache)
    range_feats = extract_range_composition(
        # ... existing args ...
        action_history=hand.get('_action_history'),
    )
    features.update(range_feats)
    _chain_cache['range'] = range_feats.get('_villain_range_narrowed')
    _chain_cache['meta'] = {
        'chain_steps': range_feats.get('_villain_range_chain_steps', []),
        'truncated': range_feats.get('_villain_range_chain_truncated', False),
        'surviving_weight': range_feats.get('_surviving_weight', 1.0),
        'villain_folded': range_feats.get('_villain_folded', False),
        'chain_overflowed': range_feats.get('_villain_chain_overflowed', False),
        # MW-specific
        'per_villain_ranges': range_feats.get('_per_villain_ranges', {}),
        'per_villain_metas': range_feats.get('_per_villain_metas', {}),
    }

    # Equity / partition / explain calls then pass cached_range + cached_meta
    # from _chain_cache. LOCAL dict; garbage-collected at function exit.
```

No module-level state. Per-hand invalidation by construction.

### 3.2 MUST #64 — Deprecate `merged`; callers consume per_villain_ranges directly

**Decision: (b) deprecate `merged` entirely.** Per orchestrator recommendation.

Rationale:
- `max()` across opponents double-counts hands present in multiple ranges
- Weight-avg via `sum / N` conflates independent ranges
- Composition features in multiway are **per-villain** (teaching renders "villain BB has X% TP+; villain CO has Y% TP+"). No correct single merged distribution.
- Equity MC already consumes per-villain ranges directly

**Caller updates in commit 4 merged unit:**

1. `compute_partition_features` (feature_extractor.py:500-505) — HU path unchanged; multiway path computes partition features per-villain via `per_villain_ranges`, aggregates at display layer (teaching owns aggregation strategy).

2. `extract_range_composition` (feature_extractor.py:1116+) — multiway path reads `per_villain_ranges` and runs the composition loop per-villain. Returns per-villain composition in metadata:
   ```python
   '_per_villain_composition': {
       'BB': {'tp_pct': 0.32, 'draw_pct': 0.18, 'air_pct': 0.25, 'medium_made_pct': 0.25},
       'CO': {'tp_pct': 0.18, 'draw_pct': 0.22, 'air_pct': 0.35, 'medium_made_pct': 0.25},
   }
   ```
   Scalar composition features (e.g., `_villain_top_pair_plus_pct`) in multiway become the PRIMARY-VILLAIN's values (first in `opponent_positions`). Teaching layer reads `_per_villain_composition` for multi-villain rendering.

3. Helper returns `(None, meta)` for multiway; callers raise if they try to use the range. MUST #63 assertion catches misuse.

**Implication for blueprint v2 CRIT #1 spec:** Step 12 + Step 17 blocker features in multiway need re-scoping. Current spec: "consume `_villain_range_narrowed`". Updated: "consume primary villain's range from `_per_villain_ranges[opponent_positions[0]]`; multiway blocker features are primary-villain-only until v2.5 per-villain blocker features land." v2.5 ticket queued.

### 3.3 MUST #65 — `HELD_BACK_FEATURES` from gto_model SOT

**Edit to `river-rats-core/gto_model.py`** (add after FEATURE_COLUMNS definition, ~line 63):

```python
# MUST #65 — held-back features: present in FEATURE_COLUMNS (for model
# inference / SHAP compatibility) but withheld from training CSVs in
# v2.3.x. Un-held at Stage 5 per manifest v1.10.
#
# Single source of truth. Assemblers + trainers import this name,
# do NOT hardcode their own list.
HELD_BACK_FEATURES = frozenset({
    'board_adjusted_hrp',
})

ACTIVE_FEATURE_COLUMNS = tuple(
    f for f in FEATURE_COLUMNS if f not in HELD_BACK_FEATURES
)
```

**Assembler import update (replaces v2.3 line 454):**

```python
# DELETED from assembler:
#   _HELD_BACK = frozenset({'board_adjusted_hrp'})

# ADDED:
from gto_model import HELD_BACK_FEATURES, ACTIVE_FEATURE_COLUMNS

def _active_feature_columns():
    """MUST #48 + #65 — active features (FEATURE_COLUMNS minus held-back).
    Sources from gto_model SOT; local definition removed.
    """
    return list(ACTIVE_FEATURE_COLUMNS)
```

Trainer uses same import. Stage 5 un-hold flips `HELD_BACK_FEATURES` to empty frozenset in gto_model; all consumers pick up automatically.

### 3.4 MUST #66 — Stratified 10% sampling for solver-verify

**Update to `river-rats-core/tests/solver_verify_sidecars.py` (v2.3 §3.6 spec):**

```python
"""MUST #54 + #66 — stratified 10% solver-verify of authored sidecars.

Stratification per MUST #49 shape categories (8 buckets):
  1. HU donk-flop + turn-check-through + river-bet
  2. HU bet-check-call-bet four-class chain
  3. HU BET-RAISE-CALL same-street collapse
  4. Folded-villain multiway
  5. Over-narrow to empty
  6. Mass-floor truncation
  7. Delayed-probe large turn bet
  8. Multiway per-villain chain

Per MUST #66: ≥1 sample per shape category; total sample = max(14, 8).
When sidecar volume is ~140 entries, 10% is ~14; stratification ensures
≥1 from each bucket.

Cochran 1977: stratified > uniform random at small N when population
has systematic sub-group differences. This is the case here
(per-shape-category error modes are distinct).
"""

def _stratify_sidecars_by_shape(sidecars: List[Dict]) -> Dict[str, List[Dict]]:
    """Classify each sidecar by shape category per MUST #49 buckets."""
    # ... implementation: read each sidecar's action_history, match
    # against shape-pattern regexes, return dict-of-lists ...

def sample_stratified(sidecars: List[Dict], pct: float = 0.10) -> List[Dict]:
    """Sample pct across shapes; guarantee ≥1 per shape."""
    by_shape = _stratify_sidecars_by_shape(sidecars)
    sampled = []
    for shape, entries in by_shape.items():
        n_target = max(1, int(len(entries) * pct))
        sampled.extend(random.sample(entries, min(n_target, len(entries))))
    return sampled
```

---

## 4. MEDIUM (1, optional)

### 4.1 MUST #67 — Benchmark stratify by num_opponents — DEFERRED with planned commit

**Decision: DEFER — acceptable per orchestrator directive.**

Add to `benchmark_multiway_chain.py` (MUST #52) as a follow-up commit planned post-Stage-3.5 ship:

```python
# MUST #67 — future work. Current benchmark reports aggregate median/p95.
# Planned-enforcement commit will bin by num_opponents ∈ {2, 3, 4, 5}
# and trip gate on worst-bin median >= 500ms OR aggregate p95 >= 750ms.
#
# Rationale for deferral: Stage 3.5 ship gate runs benchmark against v2.3.1
# training CSV. If aggregate passes, commit 5 (merged) merges. Per-opp-bin
# gating becomes relevant if Stage 5 training data shifts opponent-count
# distribution — that's Stage 5 scope, not Stage 3.5.
```

v2.5+ ticket tracked.

---

## 5. Q-resolutions (applied)

- **Q39 (chain_steps syntax):** RESOLVED in MUST #60(a) per builder's proposed fix. Applied.
- **Q40 (tri-state binarisation audit):** APPROVED. Trainer emits audit log per fit — added to MUST #27 + commit 11B:
  ```python
  # At trainer X-matrix build time, after binarising attention cols:
  import logging
  logging.getLogger(__name__).info(
      'MUST #40: attention cols binarised from tri-state (>=1 → 1). '
      'CSV retains 0/1/2; trainer consumes 0/1. v2.5+ may re-train on '
      'full tri-state. attention_cols=%d, vocab=%s',
      len(ATTN_FEATURES), csv_vocab,
  )
  ```
- **Q41 (medium_made bet=0.15 defensibility):** ACCEPTED with KB §1.11 footnote. Footnote added per orchestrator directive — lands in commit 9 (MUST #17 + #38 + #39 + #40 + #50 combined KB edit):
  > **Footnote (v2.4 calibration note):** RIVER_BETTING `medium_made` frequency set to 0.15 per MUST #50 atomic-coherence fix (check 0.85 + bet 0.15 = 1.00). Slightly aggressive vs 0.10–0.12 solver-typical for 3-way river; defensible for teaching-tool calibration. v2.5 solver-alignment pass may lower to 0.10; calibration anchor tests will flag if this produces unexpected BET predictions.

---

## 6. Stage 3 forward-looking note (NOT v2.3.1 scope)

Per GTO review + directive: v3.2 prompt must explicitly define PRIMARY vs CONFIRMED labeller vocabulary. Tracked as Stage 3 deliverable prerequisite, not Stage 3.5 MUST. **Added to manifest v1.11 hand-off note when Stage 3.5 ships.**

---

## 7. Commit sequence (no change from v2.3 §4.5)

v2.3.1 is spec-text only. Commit sequence unchanged: **14 main + 2 sub = 16 logical commits.**

MUST #60(c) MED-B adds one line item to commit 4's todo list: "explicitly delete v2.2 §3.7 placeholder sketch from feature_extractor.py diff" — but the sketch was never implemented in code (it was in amendment docs only), so this is documentation-hygiene only, not a code delete.

---

## 8. Execution posture

v2.3.1 patch commit includes:
1. This document (new file)
2. Physical SUPERSEDED markers on:
   - `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md` lines 942 + 1728
   - `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md` line 680

Push + ping orchestrator for single read-check.

If orchestrator read-check clean → ALL-CLEAR + implementation begins.

If orchestrator read-check surfaces new CRITICAL → pass #5 dispatches (not expected per convergence pattern).

No code edits. Standing by.
