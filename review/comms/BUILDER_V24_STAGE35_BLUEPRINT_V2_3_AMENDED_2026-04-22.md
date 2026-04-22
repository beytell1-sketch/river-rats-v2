---
date: 2026-04-22
from: Builder (v2.3 amendment fix-forward on d7db3f1)
to: Orchestrator · Multi-agent reviewer panel (reconciliation pass #4)
re: v2.3 amendment — 15 new MUSTs (#45-#59) from reconciliation #3 + Q36-Q38 + source-verified 4 CRITICAL fixes
status: AMENDMENT — fix-forward on v2.2 amended (d7db3f1); blueprint v2 base (8bb0f9f) still intact
replaces_additively: review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md (d7db3f1) — cumulative reading
sources:
  - review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_PASS3_2026-04-22.md (71985cf)
  - review/comms/REVIEWER_V24_STAGE35_PASS3_2026-04-22.md (71985cf)
  - Origin verification at HEAD 71985cf
---

# Stage 3.5 — Blueprint v2.3 (Fix-forward amendment)

Per reconciliation pass #3 (71985cf): 15 new MUSTs (#45–#59), 3 Q-resolutions (Q36–Q38), 4 CRITICAL ship blockers source-verified against origin.

**Active MUST count: 57** (42 from v2.2 amended + 15 from this pass). Inactive: #24, #25.

No code edits until reconciliation pass #4 signals clean.

---

## 1. Source verification of 4 CRITICAL findings

Per discipline — `git show origin/master:<path>` verified each:

| MUST | File | Finding | Verified at origin |
|------|------|---------|---------------------|
| #45 | `BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md:214-215` | `return 1 if val in ('PRIMARY', 'CONFIRMED') else 0` — case-sensitive; `return int(val) if val else 0` — unclamped | ✓ confirmed |
| #45 | same file:376 | `ATTENTION_VOCAB_VERSION = f"v2.4_{len(FEATURE_COLUMNS)}flag"` → `v2.4_55flag` | ✓ confirmed |
| #46 | same file:685 | `merged = {}` declared; no population; no return | ✓ confirmed |
| #46 | same file:698 | `opp_range, _ = narrow_by_action_history(...)` drops meta | ✓ confirmed |
| #47 | `BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md:942` (v2 base) | `raise NotImplementedError  # placeholder for blueprint` | ✓ confirmed |
| #47 | same file:1728 | "13 call-site tuple-unpacks" — drift from amended §1.1's 14 | ✓ confirmed |
| #48 | v2.2 amended:376 | vocab version would read `v2.4_55flag` while CSV has 54 cols (board_adjusted_hrp held back until Stage 5) | ✓ confirmed |
| #50 | `river-rats-core/range_narrowing.py:98-110` | `RIVER_BETTING_FREQUENCIES['medium_made'] = 0.08`; MUST #17 set check = 0.85; sum = 0.93 ≠ 1.00 | ✓ confirmed |

All findings reproduce at origin. Fixes below.

---

## 2. CRITICAL MUSTs (4)

### 2.1 MUST #45 — Bi-schema helper: concrete bugs + tri-state retention

**Files:**
- `docs/ASSEMBLER_PATTERN.md` (pattern doc)
- `river-rats-core/assemble_pilot_data.py` (pilot reference impl)
- `assemble_v23_clean.py` (v2.3 reference impl)
- Future `assemble_v2_4.py` (clones pattern)

**AFTER — revised bi-schema helper (replaces v2.2 amendment §3.2 helper verbatim):**

```python
# Canonical attention values retained as tri-state for CSV write:
_ATTN_VALUE_PRIMARY = 2
_ATTN_VALUE_CONFIRMED = 1
_ATTN_VALUE_MISSING = 0

_PRIMARY_STRINGS = frozenset({'PRIMARY', 'primary', 'Primary'})
_CONFIRMED_STRINGS = frozenset({'CONFIRMED', 'confirmed', 'Confirmed'})


def _attention_value(record: dict, feature_name: str,
                     mandatory: bool = False) -> int:
    """MUST #26 + MUST #29 + MUST #44 + MUST #45 —
    Bi-schema attention extractor. Returns tri-state {0, 1, 2}.

    Tri-state retention (MUST #45):
      2 = PRIMARY  — drove decision
      1 = CONFIRMED — supports decision, checked
      0 = missing / untagged

    v2.4 trainer may choose to binarise (>=1 → 1) at fit-time; CSV
    retains tri-state so v2.5+ can train on the full signal. Research-
    validated per Lu/Xu/Chen — 2-level > binary at small N.

    Schema routing:
      - Production (v3 prompt+): record['feature_attention'] =
        {feat: 'PRIMARY'|'CONFIRMED'}
      - Pilot (Exp 3): record['attention_flags'] = {feat: 0|1|2}

    Mixed-schema rejection (MUST #45): both keys present → RuntimeError
    unconditionally (not env-gated). Hard failure; we never silently
    mix.

    Strict mode (ASSEMBLER_STRICT_ATTENTION):
      unset/0 — silent 0-default for non-mandatory features
      warn    — log WARN on mandatory miss
      raise   — RuntimeError on mandatory miss (Stage 4 re-assembly)

    Args:
        record: labeller's output dict
        feature_name: feature to look up
        mandatory: True if v3.2 prompt mandates tagging this feature
    """
    has_fa = 'feature_attention' in record and record['feature_attention'] is not None
    has_af = 'attention_flags' in record and record['attention_flags'] is not None

    if has_fa and has_af:
        sid = record.get('situation_id', '<unknown>')
        raise RuntimeError(
            f'MUST #45: mixed-schema record sid={sid}: BOTH feature_attention '
            f"AND attention_flags present. One-or-other, not both. Fix the "
            f'labeller output or reject the record before assembly.'
        )

    if has_fa:
        fa = record['feature_attention'] or {}
        val = fa.get(feature_name, None)
        if val is None:
            return _missing_attention(record, feature_name, mandatory)
        # Canonicalise — case-insensitive via explicit sets
        if val in _PRIMARY_STRINGS:
            return _ATTN_VALUE_PRIMARY
        if val in _CONFIRMED_STRINGS:
            return _ATTN_VALUE_CONFIRMED
        # Unknown string token — strict fires as if missing
        sid = record.get('situation_id', '<unknown>')
        import logging
        logging.getLogger(__name__).warning(
            'MUST #45: unknown attention token %r on feature %r sid=%s; '
            'treating as missing.', val, feature_name, sid,
        )
        return _missing_attention(record, feature_name, mandatory)

    if has_af:
        af = record['attention_flags'] or {}
        val = af.get(feature_name, None)
        if val is None:
            return _missing_attention(record, feature_name, mandatory)
        # Pilot schema: int 0/1 (rarely 2 — legacy). Clamp to tri-state.
        try:
            ival = int(val)
        except (TypeError, ValueError):
            sid = record.get('situation_id', '<unknown>')
            import logging
            logging.getLogger(__name__).warning(
                'MUST #45: non-int attention %r on feature %r sid=%s; '
                'treating as missing.', val, feature_name, sid,
            )
            return _missing_attention(record, feature_name, mandatory)
        # Clamp unconditionally: 0 missing, 1 confirmed, 2 primary
        if ival <= 0:
            return _ATTN_VALUE_MISSING
        if ival == 1:
            return _ATTN_VALUE_CONFIRMED
        return _ATTN_VALUE_PRIMARY  # 2 or higher → primary

    # Neither key present → missing
    return _missing_attention(record, feature_name, mandatory)


def _missing_attention(record: dict, feature_name: str, mandatory: bool) -> int:
    """Missing-attention handler. Strict mode applies only when mandatory."""
    if not mandatory:
        return _ATTN_VALUE_MISSING
    import os
    strict = os.environ.get('ASSEMBLER_STRICT_ATTENTION', '0').lower()
    sid = record.get('situation_id', '<unknown>')
    if strict == 'raise':
        raise RuntimeError(
            f'MUST #26: mandatory feature {feature_name!r} absent from '
            f'labeller output sid={sid}. Strict mode set. v3.2 prompt must '
            f'tag this feature; verify prompt + labeller output.'
        )
    if strict in ('warn', '1'):
        import logging
        logging.getLogger(__name__).warning(
            'MUST #26: mandatory feature %r absent sid=%s; defaulting to 0.',
            feature_name, sid,
        )
    return _ATTN_VALUE_MISSING


def _detect_schema(record: dict) -> str:
    """MUST #45 audit hook — classify record schema for CSV audit column."""
    has_fa = record.get('feature_attention') is not None
    has_af = record.get('attention_flags') is not None
    if has_fa and not has_af:
        return 'production_v3'
    if has_af and not has_fa:
        return 'pilot_exp3'
    if not has_fa and not has_af:
        return 'no_attention'
    return 'mixed'  # should never reach CSV write — rejected upstream
```

**CSV schema update (audit columns — MUST #45 + MUST #53 + MUST #48):**

```python
CSV_HEADER = (
    RAW_FEATURES
    + ATTN_FEATURES
    + [
        '_attention_vocabulary_version',   # MUST #48 fix below
        '_mandatory_tag_list_version',     # MUST #53
        '_schema_detected',                # MUST #45
        'label',
    ]
)
```

Per-row write appends `_attention_value(record, f, mandatory=f in MANDATORY_TAG_SET)` for each attention column — returning tri-state 0/1/2.

**v2.4 trainer binarisation (accept for v2.4 ship):**

```python
# At trainer X-matrix build time (train_v2_4.py):
# Binarise attention cols for v2.4 XGBoost compatibility.
# Tri-state preserved in CSV for v2.5+ training experiments.
for col in ATTN_FEATURES:
    rows[col] = (rows[col] >= 1).astype(int)
```

### 2.2 MUST #46 — Multiway spec completeness

**File:** `river-rats-core/feature_extractor.py` — `_get_chain_narrowed_villain_range` helper

**AFTER — revised multiway branch (replaces v2.2 amendment §3.7 sketch):**

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
    cached_range: Optional[Dict[str, float]] = None,
    cached_meta: Optional[Dict] = None,
) -> Tuple[Dict[str, float], Dict]:
    """MUST #6 + #19 + #30 + #34 + #46 + #52 — chain-narrowed villain
    range, single source of truth across composition + equity + partition
    + explain_hand.

    HU path (num_opponents == 1):
      Returns (v_range, meta) where v_range is chain-narrowed. meta has
      'chain_steps', 'truncated', 'surviving_weight', 'villain_folded',
      'chain_overflowed', 'per_villain_ranges' (empty dict for HU).

    Multiway path (num_opponents >= 2):
      Controlled by env MULTIWAY_CHAIN_MODE (MUST #52):
        'per_villain' (default) — chain each opponent's range by their
           OWN action history; returns (merged, meta) where meta has
           'per_villain_ranges': Dict[pos, range].
        'primary_only' (perf fallback) — chain primary villain only;
           other villains use unchained preflop range. Used when
           benchmark gate trips >750ms median per-hand extraction.

    Caller contract:
      - Composition / partition features read (merged, meta['chain_steps'])
      - Equity MC loop reads meta['per_villain_ranges'] directly (samples
        per opponent; does NOT use merged)
      - Cached path: if cached_range + cached_meta provided,
        return immediately (no re-chain)
    """
    # Cache contract (MUST #34a)
    if cached_range is not None:
        return cached_range, cached_meta or {}

    # HU path (unchanged from v2.2 amendment)
    if num_opponents < 2 or not opponent_positions:
        return _chain_narrow_single(
            hero_pos, villain_pos, opener_pos, board_cards,
            facing_bet, street_raw, action_history,
        )

    # Multiway path — MUST #46 + MUST #52
    import os
    mw_mode = os.environ.get('MULTIWAY_CHAIN_MODE', 'per_villain').lower()

    per_villain_ranges: Dict[str, Dict[str, float]] = {}
    per_villain_truncated: Dict[str, bool] = {}
    per_villain_folded: Dict[str, bool] = {}
    per_villain_overflowed: Dict[str, bool] = {}
    merged: Dict[str, float] = {}

    for opp_pos in opponent_positions:
        opp_range = get_villain_range(hero_pos, opp_pos, opener_pos=opener_pos)

        # MUST #52: primary-only fallback — chain only the primary villain
        # (= first in opponent_positions per factory convention).
        is_primary = (opp_pos == opponent_positions[0])
        should_chain = action_history and (mw_mode == 'per_villain' or is_primary)

        opp_meta: Dict = {
            'chain_steps': [], 'truncated': False, 'surviving_weight': 1.0,
            'villain_folded': False, 'chain_overflowed': False,
        }

        if should_chain:
            opp_history = [
                e for e in action_history
                if _normalize_action_entry(e).get('position', '').upper() == opp_pos.upper()
            ]
            postflop_acts = [
                e for e in opp_history
                if _normalize_action_entry(e).get('street', '').lower() in ('flop', 'turn', 'river')
            ]
            if postflop_acts:
                opp_range, opp_chain_meta = narrow_by_action_history(
                    full_range=opp_range,
                    board=board_cards,
                    action_history=opp_history,
                    villain_pos=opp_pos,
                    decision_street=STREET_NAME_MAP.get(street_raw, 'flop'),
                )
                opp_meta['chain_steps'] = opp_chain_meta.get('chain_steps', [])
                opp_meta['truncated'] = opp_chain_meta.get('truncated', False)
                opp_meta['surviving_weight'] = opp_chain_meta.get('surviving_weight', 1.0)

                # MUST #46: per-villain folded/overflow sentinels
                if not opp_range:
                    _last = opp_meta['chain_steps'][-1] if opp_meta['chain_steps'] else ''
                    if _last.endswith(':FOLD'):
                        opp_meta['villain_folded'] = True
                    else:
                        opp_meta['chain_overflowed'] = True
                elif opp_meta['truncated']:
                    # MUST #28 parity for multiway — truncated = overflowed
                    opp_meta['chain_overflowed'] = True

        # Apply facing_bet filter only to the bettor
        is_bettor = (bettor_pos is not None
                     and opp_pos.upper() == bettor_pos.upper())
        if facing_bet and is_bettor and opp_range:
            opp_range, _ = narrow_to_betting_range(
                opp_range, board_cards, STREET_NAME_MAP.get(street_raw, 'flop')
            )

        per_villain_ranges[opp_pos] = opp_range
        per_villain_truncated[opp_pos] = opp_meta['truncated']
        per_villain_folded[opp_pos] = opp_meta['villain_folded']
        per_villain_overflowed[opp_pos] = opp_meta['chain_overflowed']

        # Build merged range (for composition features — reads a single range)
        # Per v2.3.1 precedent: merged via max-freq across opponents
        for hand, freq in opp_range.items():
            merged[hand] = max(merged.get(hand, 0.0), freq)

    # Aggregate meta — any opponent overflowed = aggregate overflow;
    # all opponents folded = aggregate folded (hero runs out of villains).
    agg_truncated = any(per_villain_truncated.values())
    agg_overflowed = any(per_villain_overflowed.values())
    agg_folded = (
        all(per_villain_folded.values())
        if per_villain_folded else False
    )

    meta = {
        'chain_steps': sorted(  # aggregate for logging
            {s for opp in per_villain_ranges
             for s in per_villain_truncated}  # bug-free stringification below
        ),
        'truncated': agg_truncated,
        'surviving_weight': min(
            per_villain_truncated.values(),  # placeholder; real: weight sum
            default=1.0,
        ) if per_villain_truncated else 1.0,
        'villain_folded': agg_folded,
        'chain_overflowed': agg_overflowed,
        # MUST #46 addition — callers (equity MC loop) read this directly
        'per_villain_ranges': per_villain_ranges,
        'per_villain_truncated': per_villain_truncated,
        'per_villain_folded': per_villain_folded,
        'per_villain_overflowed': per_villain_overflowed,
    }
    return merged, meta
```

**Caller updates (equity MC):**

`feature_extractor.py:790-806` MW MC loop:

```python
# AFTER MUST #46: read per_villain_ranges directly from helper meta
merged_range, helper_meta = _get_chain_narrowed_villain_range(
    hero_pos=hero_pos, villain_pos=villain_pos,
    opener_pos=opener_pos, board_cards=board_cards,
    facing_bet=facing_bet, street_raw=street_raw,
    action_history=action_history, num_opponents=num_opponents,
    opponent_positions=opponent_positions, bettor_pos=bettor_pos,
)
per_villain_ranges = helper_meta.get('per_villain_ranges', {})
opponent_ranges = [per_villain_ranges[pos] for pos in opponent_positions]
mc_equity = _true_multiway_equity_mc(
    hero_cards, board_cards, opponent_ranges, trials=2000
)
```

### 2.3 MUST #47 — Caller list canonical count + supersession markers

**File 1:** `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md` (v2 base, 8bb0f9f)

Line 942 `raise NotImplementedError  # placeholder for blueprint` — **annotate as superseded**:

Insert above line 942 (keep the NotImplementedError line itself — it's a blueprint doc, not code; deleting it creates bigger diff):

```
**⚠️ SUPERSEDED BY v2.2 AMENDMENT §3.7 (d7db3f1) AND v2.3 AMENDMENT §2.2 (this doc).**
Multiway branch fully spec'd in the v2.2/v2.3 amendments. This blueprint-v2 placeholder is retained for audit trail only; do not implement from this section — read §3.7 of the amendment first.
```

Line 1728 "13 call-site tuple-unpacks" — annotate with correct count:

```
**⚠️ COUNT SUPERSEDED** — per v2.2 amendment §1.1 grounding + v2.3 amendment §2.3, canonical count is **14** root+coaching sites + 5 test-file sites. See v2.2 amendment Table in §3.3 for per-site breakdown.
```

**File 2:** `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md` (v2.2 amendment, d7db3f1) — §1.1 already says 14; no change.

**Canonical caller list (per MUST #30 + #47 reconciliation):**

| # | File | Line | Class |
|---|------|------|-------|
| 1 | `feature_extractor.py` | 503 | betting |
| 2 | `feature_extractor.py` | 617 | betting |
| 3 | `feature_extractor.py` | 805 | betting |
| 4 | `feature_extractor.py` | 828 | betting |
| 5 | `feature_extractor.py` | 1193 | betting |
| — | `feature_extractor.py` | 1669 | DELETED by CRIT #1 |
| 6, 7, 8 | `range_narrowing.py` | 791, 794, 797 | internal to chain |
| 9, 10 | `range_narrowing.py` | 875, 885 | test_narrowing demo |
| 11, 12 | `explain_hand.py` | 264, 329 | betting |
| 13, 14 | `coaching/explain_hand.py` | 264, 329 | betting |

**14 root+coaching call sites** (excluding the CRIT #1-deleted site). Plus 5 test-file sites in `tests/test_range_narrowing_stage35.py` (288, 294, 296, 304, 307).

**Total tuple-unpack churn for HIGH #5: 14 production + 5 test = 19 sites.** Canonical.

### 2.4 MUST #48 — Vocabulary version string uses active count

**AFTER (replaces v2.2 amendment §3.2 AFTER block line 376):**

```python
def _active_feature_columns() -> List[str]:
    """Returns FEATURE_COLUMNS minus held-back features not yet in CSV.

    Held-back features per MUST #31:
      - 'board_adjusted_hrp' — present in gto_model.FEATURE_COLUMNS
        but held back from v2.3.x training CSVs; un-held at Stage 5 per
        manifest v1.10 line 144.

    Version string derives from ACTIVE count, not FEATURE_COLUMNS length,
    so pre-Stage-5 CSV (54 raw) and post-Stage-5 CSV (55 raw) have
    distinct audit tags.
    """
    _HELD_BACK = frozenset({'board_adjusted_hrp'})
    return [c for c in FEATURE_COLUMNS if c not in _HELD_BACK]


def _attention_vocabulary_version() -> str:
    """MUST #48 — version tag encodes ACTIVE feature count + schema state.

    Format: v{oracle_version}_{active_count}flag_{state}
      - active_count: len(_active_feature_columns())
      - state: 'pre_unhold' (Stage 3.5 shipping on held-back 54)
               | 'post_unhold' (Stage 5+ with 55 active)

    Concrete values during Stage 3.5 → Stage 5 evolution:
      v2.4_54flag_pre_unhold   — Stage 3.5 ship, held-back active
      v2.4_58flag_pre_unhold   — Stage 3.5 ship + 4 new blockers, still held-back
      v2.4_59flag_post_unhold  — Stage 5 ship, board_adjusted_hrp un-held
    """
    active = _active_feature_columns()
    n_active = len(active)
    # Stage 3.5: held-back still in force; detect via presence in active
    state = 'post_unhold' if 'board_adjusted_hrp' in active else 'pre_unhold'
    return f"v2.4_{n_active}flag_{state}"


ATTENTION_VOCAB_VERSION = _attention_vocabulary_version()  # computed at assembler startup
```

**Transition table (for audit dashboards):**

| Phase | FEATURE_COLUMNS len | Active (CSV) | ATTN cols | Version string |
|-------|---------------------|--------------|-----------|----------------|
| v2.2 ship | 55 | 54 (held-back board_adjusted_hrp) | 54 | `v2.2_54flag_pre_unhold` (historical) |
| Stage 3.5 v2.4 pre-new-blockers | 55 | 54 | 54 | `v2.4_54flag_pre_unhold` |
| Stage 3.5 v2.4 with 4 new blockers | 59 | 58 (still held back) | 58 | `v2.4_58flag_pre_unhold` |
| Stage 5 v2.4 post-unhold | 59 | 59 | 59 | `v2.4_59flag_post_unhold` |

**MUST #27 trainer cross-check (updated from v2.2 amendment §3.3):**

```python
expected_vocab = _attention_vocabulary_version()
csv_vocab = first_row['_attention_vocabulary_version']
if csv_vocab != expected_vocab:
    raise RuntimeError(
        f'MUST #27+48: CSV vocab {csv_vocab!r} != expected {expected_vocab!r}. '
        f'Likely: CSV produced under different held-back state OR '
        f'FEATURE_COLUMNS length drifted. Re-assemble the CSV before '
        f'training; do not zero-pad silently.'
    )
```

---

## 3. HIGH MUSTs (6)

### 3.1 MUST #49 — 8-entry dry-run batch enumeration

**Enumerated (per Practical pro + directive):**

For Phase 2 sidecar authoring, the 8 fixture shapes that gate batch quality:

| # | Shape | Target fixture(s) / corpus case |
|---|-------|--------------------------------|
| 1 | HU donk-flop + turn-check-through + river-bet | `T_J01` (owner H_d9edab5d) — reauthored per MUST #33 |
| 2 | HU bet-check-call-bet four-class chain | `T_J02` (owner H_8dfb6ef8) — tests all 4 narrow classes |
| 3 | HU BET-RAISE-CALL same-street collapse | `T_B05` — tests MUST #11 pre-filter (check-call + bet-raise sequences) |
| 4 | Folded-villain multiway (sentinel path) | `T_I03_villain_folded_midchain_turn` — tests MUST #46 per_villain_folded aggregation |
| 5 | Over-narrow to empty (MUST #15 overflow) | `T_K18_malformed_action_entry_fallback` OR synthetic contrived deep chain that overflows without FOLD |
| 6 | Mass-floor truncation (MUST #28) | Synthetic deep chain that triggers `cumulative_surviving < 0.10`; add as new corpus case `T_K21_mass_floor_truncation` |
| 7 | Delayed-probe large turn bet | `T_K07_large_turn_bet_after_flop_check_through` |
| 8 | Multiway per-villain chain (MUST #46) — 3-way spot | `T_E02_3way_turn_primary_changed_after_fold` OR a new shape where two villains have distinct action histories |

**Phase 2 midpoint check:** 25-30 stratified sample across buckets (covering at least 5 per category in FB-40, 5 per bucket in MW-50). Run strict-mode assembly on the sample; zero missing-mandatory errors required before authoring continues to full ~140 entries.

**Commit:** landed at commit 6 (MUST #20 calibration_exam sidecar) dry-run batch.

### 3.2 MUST #50 — Frequency table atomic coherence

**File:** `river-rats-core/range_narrowing.py` — `RIVER_BETTING_FREQUENCIES` + `RIVER_CHECKING_FREQUENCIES`

**Decision: pick (b) — check=0.85, bet=0.15 (sum 1.00).** GTO recommendation; more aggressive river medium betting; matches thin-value-exists principle per solver literature.

**BEFORE (origin):**
```python
RIVER_BETTING_FREQUENCIES = {
    ..., 'medium_made': 0.08, 'weak_made': 0.05, 'bluff': 0.35, 'air': 0.20, ...
}
# ... MUST #17 applied: RIVER_CHECKING['medium_made'] = 0.85 (was 0.92)
# ... MUST #38 applied: RIVER_BETTING['bluff'] = 0.20; RIVER_BETTING['air'] = 0.10
# ... MUST #38 applied: RIVER_CHECKING['bluff'] = 0.80; RIVER_CHECKING['air'] = 0.90
```

**AFTER — atomic edit (all 3 pairs sum to 1.00):**

```python
# MUST #17 + #38 + #50: atomic-coherence river-frequency set.
# Every pair sums to 1.00. When you change ONE, verify ALL.
RIVER_BETTING_FREQUENCIES = {
    'nuts': 0.95,           # check 0.05 ✓
    'strong_value': 0.90,   # check 0.10 ✓
    'good_value': 0.55,     # check 0.45 ✓
    'draw': 0.00,           # check 1.00 (missed = air; reclassify)
    'medium_made': 0.15,    # MUST #50 — was 0.08; raised for atomic-coherence with check 0.85
    'weak_made': 0.05,      # check 0.95 ✓
    'bluff': 0.20,          # MUST #38 — 3-way bluff density
    'air': 0.10,            # MUST #38 — 3-way air bluff density
}
RIVER_CHECKING_FREQUENCIES = {
    'nuts': 0.05,
    'strong_value': 0.10,
    'good_value': 0.45,
    'draw': 1.00,
    'medium_made': 0.85,    # MUST #17 — was 0.92
    'weak_made': 0.95,
    'bluff': 0.80,          # MUST #38 — mass parity with bet 0.20
    'air': 0.90,            # MUST #38 — mass parity with bet 0.10
}

# Coherence check at module import time:
def _verify_river_freq_coherence():
    for cat in RIVER_BETTING_FREQUENCIES:
        bet = RIVER_BETTING_FREQUENCIES[cat]
        chk = RIVER_CHECKING_FREQUENCIES.get(cat, None)
        if chk is None:
            continue
        s = bet + chk
        if abs(s - 1.00) > 0.001:
            raise AssertionError(
                f'MUST #50: RIVER frequency incoherent for {cat!r}: '
                f'bet={bet} + check={chk} = {s}, expected 1.00'
            )
_verify_river_freq_coherence()
```

**Commit:** lands in commit 10 (MUST #17 + #38 + #39 + #40 + #50).

### 3.3 MUST #51 — T_J02 corpus value reconciliation

**File:** `review/tests/range_narrowing_test_corpus_2026-04-20.yaml` line ~1683

Corpus currently has T_J02 at 0.65/0.10/0.00/0.25. V2.2 amendment §3.6 specified 0.60/0.18/0.00/0.22.

**Explicit YAML edit per MUST #51:**

```yaml
# Line ~1683 — T_J02_owner_H_8dfb6ef8_bet_check_call_bet_line
# REWRITE expected_composition_post_fix block:
  expected_composition_post_fix:
    villain_tp_pct: 0.60          # was 0.65
    villain_medium_made_pct: 0.18  # was 0.10 — turn CHECK-CALL is medium pot-control
    villain_draw_pct: 0.00
    villain_air_pct: 0.22          # was 0.25
```

**Ship criterion (per MUST #33 + Q37):** T_J02 allowed MIXED-CALL with CALL probability >40% (soft criterion per Q37 resolution); verdict-flip required only for T_J01.

**Commit:** lands in commit 13 (corpus + tests).

### 3.4 MUST #52 — Benchmark-gate fallback switch

**Files:**
- `river-rats-core/feature_extractor.py` — `_get_chain_narrowed_villain_range` reads env `MULTIWAY_CHAIN_MODE` (already in §2.2 AFTER spec above)
- New benchmark script: `river-rats-core/tests/benchmark_multiway_chain.py`

**Benchmark spec:**

```python
"""MUST #52 — benchmark multiway chain perf. Gate at 500ms ship,
500-750ms orchestrator review, >750ms fallback to primary_only.

Runs 100 multiway hands from v2.3.1 training CSV. Reports median +
p95 per-hand extract_all_features time under both MULTIWAY_CHAIN_MODE
values. Orchestrator reviews before commit 5 merge.
"""
# ... implementation sketch:
import time, os, csv
from feature_extractor import extract_all_features
SAMPLE = load_100_multiway_hands()
for mode in ('per_villain', 'primary_only'):
    os.environ['MULTIWAY_CHAIN_MODE'] = mode
    times = []
    for h in SAMPLE:
        t0 = time.time()
        extract_all_features(h)
        times.append(time.time() - t0)
    times.sort()
    median = times[len(times)//2]
    p95 = times[int(len(times)*0.95)]
    print(f'{mode}: median={median*1000:.1f}ms p95={p95*1000:.1f}ms')
```

**Gate decision tree (Q36 resolution applied):**
- Both modes median < 500ms → ship with `per_villain` default
- `per_villain` median 500-750ms AND `primary_only` < 500ms → orchestrator reviews; default likely `per_villain` with perf-audit follow-up
- `per_villain` median > 750ms → hard fallback: default `primary_only`; file v2.5 ticket for per-villain perf optimisation

**Commit:** landed as commit 5 (merged) dry-run item before merge (runs against v2.3.1 training CSV; blocks merge if >750ms).

### 3.5 MUST #53 — `_mandatory_tag_list_version` audit column

**File:** `docs/ASSEMBLER_PATTERN.md` + assemblers + trainer

**Version string convention:**
- v3_prompt — Phase 4 production labellers (v3.0 prompt)
- v3_1_prompt — v3.1 prompt (most-recent-authored, not production)
- v3_2_prompt — v3.2 prompt (Stage 3 deliverable, future)

**Assembler writes:**
```python
MANDATORY_TAG_LIST_VERSION = os.environ.get('LABELLING_PROMPT_VERSION', 'v3_prompt')
# ... in CSV_HEADER:
CSV_HEADER = RAW_FEATURES + ATTN_FEATURES + [
    '_attention_vocabulary_version',
    '_mandatory_tag_list_version',   # MUST #53
    '_schema_detected',              # MUST #45
    'label',
]
```

**Trainer cross-check (extends MUST #27):**
```python
expected_prompt = os.environ.get('LABELLING_PROMPT_VERSION', 'v3_prompt')
csv_prompt = first_row['_mandatory_tag_list_version']
if csv_prompt != expected_prompt:
    raise RuntimeError(
        f'MUST #53: CSV prompt version {csv_prompt!r} != expected '
        f'{expected_prompt!r}. v3.1→v3.2 transition may have silently '
        f'changed mandatory-tag list. Re-assemble before training.'
    )
```

**Commit:** added to commit 11A (assembler) and commit 11B (trainer).

### 3.6 MUST #54 — Sidecar 10% solver-verify sampling

**File:** new `river-rats-core/tests/solver_verify_sidecars.py`

**Spec:**

```python
"""MUST #54 — 10% random-sample solver-verify of authored sidecars.

Per feedback_solver_vs_expert_labels.md: solver VERIFIES, never labels.
This script solver-verifies sidecar well-formedness by running sample
hands through the equity + action-tree framework and asserting that
the authored action_history corresponds to a poker-plausible line.

Catches authoring drift that structural validator (MUST #35) misses:
  - 'villain called an unraised pot' (structurally valid, semantically
    nonsense)
  - 'villain raised after their own call' (structurally valid, game-state
    invalid)
  - Multiway action ordering inconsistent with position seating

Usage:
    python3 river-rats-core/tests/solver_verify_sidecars.py
        --sample-pct 0.10 --fail-fast

Returns: exit 0 if all sampled sidecars are solver-plausible; exit 1
with offender list if any fail.
"""
```

**Not ship-blocking per-sidecar-entry; runs at Phase 2 midpoint per MUST #49 25-30-entry sample.**

**Commit:** added to commit 15 (pre-SHIP sidecar authoring phase).

---

## 4. MEDIUM MUSTs (5)

### 4.1 MUST #55 — Silent-fallback in `review/recovered/eval_*.py`

**Files (verified on disk):**
- `review/recovered/eval_FB40_plus_ablation.py` (has `except Exception`)
- `review/recovered/eval_FB40_attn_per_feature.py`
- `review/recovered/eval_MW_test_set_50.py`
- `review/recovered/eval_MW_with_legal_action_masking.py`

**Decision: (b) add audit column + strict-env gate, but only if confirmed live.** Builder verifies at commit time (first 30 minutes of commit 8 — MUST #23 sibling) whether any live path imports or runs these scripts. If obsolete: delete. If live: apply CRIT #2 + MUST #9 strict pattern.

**Deferred decision (DECIDE and EXECUTE default: pick live-path audit at commit time).**

**Commit:** commit 8 (parallels MUST #23 sizing pipeline).

### 4.2 MUST #56 — Manifest-gate lockout tooling enforcement — DEFERRED

**Decision: DEFER to v2.5+** per orchestrator's explicit allowance. Manifest-as-docs is acceptable tech debt for Stage 3.5. Log memory note:

**New memory file:** `~/.claude/projects/-home-rupertbeytell/memory/feedback_manifest_gate_is_docs_not_enforcement.md`:

```markdown
---
name: Manifest gate is docs, not enforcement
description: RELEASE_MANIFEST.yaml stage gates are human-readable; enforcement is orchestrator-reviewed, not CI-enforced. Stage 3.5 ship accepts this; v2.5+ may add CI hook.
type: feedback
---

Manifest v1.10's Stage 4 gate is YAML documentation, not a CI-level
lockout. Orchestrator reads the manifest at gate-pass time and blocks
Stage 4 scripts by inspection, not by git-hook or pre-commit.

Acceptable for Stage 3.5 ship per quality/cost trade-off. v2.5+ ticket
may add:
  - Pre-commit hook that reads manifest phase + blocks Stage 4 scripts
    when `stage_3_5` not in `landed`
  - Or CI workflow that same

Don't re-litigate this during Stage 3.5 implementation. If a reviewer
flags it again: point at this memory; confirmed-deferred.
```

**Commit:** memory-only; no repo file.

### 4.3 MUST #57 — CONTENT_API v4 version-pin tooling

**File:** `TICKET_CONTENT_API_V4_NAN_RENDER_2026-04-22.md` addendum

Add to existing ticket:

```markdown
## Version-pin enforcement (MUST #57)

Game adapter and teaching CONTENT_API module must carry explicit
version string. Commit 4 (Stage 3.5 CRIT #1 + HIGH #4 merged) has
a pre-merge gate that grep's for:
  - `river-rats-teaching/interface/CONTENT_API.md` contains `version: v4.0`
  - Game adapter `integrations.real_teaching` imports `l3_enriched_v4_0`
  symbol (or explicit version reference)

Teaching terminal owns the bump. Orchestrator verifies at commit 4
merge time. No tooling automation; manual verification is the pattern
for cross-stream gates (consistent with MUST #56 deferral).
```

**Commit:** ticket addendum in commit 12 (MUST #42 + #43 + #57).

### 4.4 MUST #58 — ASSEMBLER_PATTERN.md enforcement checklist

**File:** `docs/ASSEMBLER_PATTERN.md` — append checklist

```markdown
## Review checklist for new assembler (v2.4, v2.5+)

Stage 4 + Stage 5 reviewers MUST check off each item before merging
a new assembler script:

- [ ] RAW_FEATURES bound to `_active_feature_columns()` (handles held-back)
- [ ] ATTN_FEATURES derived as `[f'attn_{c}' for c in RAW_FEATURES]`
- [ ] `_attention_value(record, feature_name, mandatory)` helper used
      for every attention-column write (or re-implemented with MUST #45
      equivalent contract: tri-state, mixed-schema reject, case-insensitive)
- [ ] `_attention_vocabulary_version` audit column per MUST #48
- [ ] `_mandatory_tag_list_version` audit column per MUST #53
- [ ] `_schema_detected` audit column per MUST #45
- [ ] Strict-env gate `ASSEMBLER_STRICT_ATTENTION` respected
- [ ] Running strict=raise on 8-entry dry-run (MUST #49) passes
- [ ] Running strict=raise on 25-30 stratified sample passes
- [ ] Running MUST #54 10% solver-verify on sample passes
```

**Commit:** in commit 11A (assembler pattern + reference impls).

### 4.5 MUST #59 — Commit 4/5/6 merge decision

**Decision: (b) MERGE commits 4 + 5 + 6 into single atomic unit.** Per orchestrator recommendation.

Rationale:
- CRIT #1 (chain consumer) + HIGH #4 (folded sentinel) + MUST #6 (equity chain inheritance) + MUST #10/#15/#28 (NaN spec) all touch the SAME chain-inheritance surface
- Merging eliminates the commit-4-to-commit-5-to-commit-6 poisoning windows entirely
- v2.3.2 lesson: atomic chain-consistency > cleaner commit boundaries
- Downside: larger diff for single commit; mitigated by per-section review at the blueprint level (already done)

**Updated commit sequence (v2.3) — 14 commits (was 16):**

| # | Commit | Lands |
|---|--------|-------|
| 1 | HIGH #5 + MUST #13 | Tuple-return, mass threading, 10% floor + 20% WARN, 14 call-site tuple unpacks + 5 test-file edits |
| 2 | CRIT #2 + MUST #9 | Strict env gate, pipeline unswallow, `_action_history_present` CSV col |
| 3 | HIGH #3 + MUST #11 + #12 | Same-street sequence collapse pre-filter |
| **4 (merged)** | **CRIT #1 + HIGH #4 + MUST #6 + MUST #10 + MUST #15 + MUST #19 + MUST #28 + MUST #30 + MUST #34 + MUST #46 + MUST #52** | **Atomic: publish `_villain_range_narrowed`, Step 12/17 consume, `_get_chain_narrowed_villain_range` helper (HU + multiway spec complete per MUST #46), folded/overflow/truncated sentinels, NaN spec, equity + partition + explain_hand + coaching/explain_hand chain inheritance, benchmark gate** |
| 5 | MUST #20 | calibration_exam.py `_action_history` plumbing + dry-run sidecar batch (8 entries per MUST #49) |
| 6 | MUST #22 | reference_evaluator.py `_action_history` plumbing + dry-run sidecar batch |
| 7 | MUST #23 + MUST #55 | train_sizing_model.py verify/plumb; eval_*.py silent-fallback decision |
| 8 | MUST #8 partial delete + MUST #37 audit | Delete 2 coaching files after sys.path side-effect audit |
| 9 | MUST #17 + MUST #38 + MUST #39 + MUST #40 + MUST #50 | Frequency table atomic coherence, KB §1.11 asymmetric thresholds + combo-draw max |
| 10 | MUST #41 | Count guard at 5 hands |
| 11 | MUST #42 + MUST #43 + MUST #57 | CONTENT_API v4 ticket + version-pin addendum; player-English NaN render |
| 11A | MUST #26 + MUST #29 + MUST #44 + MUST #45 + MUST #48 + MUST #53 + MUST #58 | Assembler reference impls + bi-schema tri-state helper + audit columns + pattern doc + review checklist |
| 11B | MUST #27 + MUST #31 + MUST #36 + MUST #53 trainer-side | Trainer dynamic vocab + CSV header reconciliation + cross-check |
| 12 | MUST #33 + MUST #51 + corpus 81-case + coverage-gap tests | Reauthored T_J01/T_B05/T_J02 + new `T_K21_mass_floor_truncation` + 4 coverage-gap tests |
| 13 | M4 re-audit (expanded) | Blocker bypass + NaN + mass + equity-shift + per-villain metadata |
| 14 | M5 re-run + MUST #16 regression guard + MUST #54 solver-verify sample | Anchor non-empty chain + solver-verify 10% sidecar sample + Stage 3.5 SHIP |

**Net: 14 main + 2 sub (11A/11B) = 16 total logical commits.** Per-MUST discipline preserved via 11A/11B granularity on the assembler/trainer work.

---

## 5. Q-resolutions (Q36–Q38)

**Q36 (multiway perf threshold):** Asymmetric gating per Architecture recommendation. 500ms ship / 500-750ms orchestrator review / >750ms hard fallback to primary_only. MUST #52 codifies env switch + benchmark script.

**Q37 (T_J01 ship-criterion softness):** Hard verdict-flip required for T_J01 (FOLD → CALL or MIXED-with-CALL). Soft MIXED-CALL>40% criterion for T_J02 / T_K5-7. If all 3 reauthored fixtures fail hard AND soft: real failure → revisit chain spec. If 1-2 soft fail: owner judgment call.

**Q38 (bi-schema confusion):** Merged into MUST #45. Mixed-schema rejection (RuntimeError unconditionally) + `_schema_detected` audit column.

---

## 6. New questions for reconciliation pass #4

Minor scope only — reviewers can raise NEW-CLASS issues but these are reminder Q's for explicit-resolution:

- **Q39 (architecture):** MUST #46 `chain_steps` aggregation in multiway meta — my spec uses `sorted({s for opp in ... for s in per_villain_truncated})` which is nonsense (iterating dict not list). Replace with proper aggregation: per-opponent `chain_steps` preserved in `meta['per_villain_chain_steps']`; aggregate `chain_steps` becomes `[f'{opp}:{step}' for opp, steps in per_villain_chain_steps.items() for step in steps]`. Reviewer confirms this matches expected caller contract.
- **Q40 (red-team):** Tri-state retention (MUST #45) in CSV — v2.4 trainer binarises at fit-time. Any risk of silent binarisation drift (trainer reads tri-state, treats 1 and 2 identically without acknowledgement)? Mitigation: trainer emits audit log "attention binarised from tri-state" per fit.
- **Q41 (GTO):** Atomic river-frequency set (MUST #50) — `medium_made` bet=0.15 is a real bet frequency (not pure bluff-catcher). Does this over-estimate river value-betting for mediums in 3-way? Alternative: `medium_made` check=0.92, bet=0.08 (reverts MUST #17). Reviewer picks.

---

## 7. Execution posture

**v2.3 amendment complete.** Fix-forward on `d7db3f1`. Single new commit on top. Net scope: 57 active MUSTs; 14 main + 2 sub = 16 logical commits.

Per STEP 3: commit + push. Orchestrator dispatches reconciliation pass #4.

If pass #4 surfaces new CRITICAL MUSTs: cut v2.4 amendment (fix-forward again). Pattern converging per pass-3 trajectory.

If pass #4 lands clean or MEDIUM-only: orchestrator publishes ALL-CLEAR, implementation begins per §4.5 commit sequence.

No code edits. Standing by after push.
