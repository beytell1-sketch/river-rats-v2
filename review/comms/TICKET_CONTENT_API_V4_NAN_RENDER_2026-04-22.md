---
date: 2026-04-22
from: Builder (Stage 3.5 blueprint v2.2 cross-stream)
to: Teaching terminal · Orchestrator
re: CONTENT_API v4 — NaN render spec for Stage 3.5 sentinels
status: CROSS-STREAM TICKET — teaching implementation required to land BEFORE Stage 3.5 code commit 4 ships
blocking: Stage 3.5 commit 4 (CRIT #1 + HIGH #4 + NaN spec merged per MUST #32)
---

# Ticket — CONTENT_API v4 NaN Render Spec

Stage 3.5 introduces NaN sentinels for villain composition + blocker
features under three conditions. Teaching must render player-English
strings for each condition; current CONTENT_API v3.0 does not handle
NaN-valued features gracefully (would render literal `"nan%"` or
silently fail ranking).

This ticket is **blocking** — Stage 3.5 code cannot merge commit 4
(CRIT #1 + HIGH #4 NaN spec) until teaching's CONTENT_API v4 ships
with NaN handling.

---

## 1. Background

v2.4 Stage 3.5 emits NaN for the following features under specified conditions:

### Sentinel conditions

| Condition | Trigger | Emitted by |
|-----------|---------|------------|
| `_villain_folded=True` | Chain terminates at `:FOLD` step (villain folded on prior street) | `extract_range_composition` in `feature_extractor.py` |
| `_villain_chain_overflowed=True` | Chain over-narrows to empty without FOLD OR mass-floor truncation fires | Same |
| Mass-floor truncation | `cumulative_surviving < 0.10` per MUST #13 + MUST #28 | Same, chain_truncated=True |

### Features NaN-flagged under each condition

All three conditions emit NaN on the same feature set:

**Composition (4 features):**
- `_villain_top_pair_plus_pct`
- `_villain_draw_pct`
- `_villain_air_pct`
- `_villain_medium_made_pct`

**Blockers (4 features):**
- `flush_block_pct` (existing, v2.2)
- `flush_draw_block_pct` (new, v2.4)
- `straight_draw_block_pct` (new, v2.4)
- `nut_made_block_pct` (new, v2.4)

**Other:**
- `nut_flush_block` stays as int 0 (boolean; "hero cannot block nothing")

Non-villain-range-derived features (`raw_equity`, `pot_odds`, etc.) are unaffected.

---

## 2. Contract — CONTENT_API v4

### 2.1 New schema field

Add to `EnrichedTeachingOutput` (teaching schema `l3_enriched_v4.0`):

```python
range_rendering_mode: Literal["normal", "folded", "overflow"]
# "normal" — standard range-composition prose (current v3.0 behavior)
# "folded" — villain folded; range analysis N/A
# "overflow" — chain over-narrowed OR mass-floor truncated; relying on equity alone
```

### 2.2 Derivation rule

Teaching reads `_villain_folded` + `_villain_chain_overflowed` from the feature dict:

```python
if feat_dict.get('_villain_folded', False):
    range_rendering_mode = "folded"
elif feat_dict.get('_villain_chain_overflowed', False):
    range_rendering_mode = "overflow"
else:
    range_rendering_mode = "normal"
```

### 2.3 Render strings (player English per MUST #42)

**Mode = "folded" (HU):**
> "Villain folded earlier — no range to read."

**Mode = "folded" (multiway, with remaining live villain(s)):**
> "Villain {folded_position} folded; reading against villain {live_position} only."
>
> (If multiple live villains remaining, use comma-separated list: `"villain BB and villain CO only"`.)

**Mode = "overflow":**
> "Villain's line is too rare to read confidently — relying on equity alone."

**Mode = "normal":** unchanged from v3.0.

### 2.4 Primary window + flag window implications

**Primary window — villain_*_pct line:**
- mode=normal: render current `villain_top_pair_plus_pct`/`villain_draw_pct`/`villain_air_pct` prose
- mode=folded OR overflow: **SKIP this line entirely.** Do not render a villain-range summary.

**Flag window — blocker flags (the 2 flags per teaching recentering §D.1):**
- mode=normal: render blocker flag(s) per v3.0 spec (once blocker flag design ships; currently placeholder)
- mode=folded OR overflow: **SKIP blocker flags.** They're meaningless against no/unknown villain range.

**Board favour + range capped features:** still render in normal mode only; skip in folded/overflow (they depend on range composition).

### 2.5 What NOT to render

- No partial-info rendering. NEVER show "blocker_pct: N/A" or "blocker_pct: nan" or any percentage-style rendering with a placeholder value.
- No "we're not sure what villain has" weasel phrasing. Either read the range OR say explicitly why we can't.
- No raw equity as a standalone metric in folded mode. Equity computed against a folded villain is meaningless. (Equity computed pre-fold is fine; check `_villain_folded` BEFORE rendering equity prose.)

---

## 3. Test cases

### 3.1 Folded-villain HU

**Input:**
- `num_opponents=1`
- `_villain_folded=True`
- Other sentinels False

**Expected render:**
```
Villain folded earlier — no range to read.
```
No composition prose; no blocker flags; no board favour.

### 3.2 Folded-villain multiway with 1 remaining live

**Input:**
- `num_opponents=2` (but one has folded)
- `_villain_folded=True` (primary villain folded)
- Non-primary live villain position = `BB`

**Expected render:**
```
Villain BTN folded; reading against villain BB only.
```

Note: requires teaching to receive the specific folded-villain position + live-villain position. CONTENT_API v4 may need new fields `folded_villain_positions: List[str]` + `live_villain_positions: List[str]`.

### 3.3 Over-narrowed chain

**Input:**
- `_villain_chain_overflowed=True`
- `_villain_folded=False`
- `_villain_range_chain_steps` non-empty (e.g., `["flop:CHECK", "turn:CHECK", "turn:CALL", "river:BET"]`)

**Expected render:**
```
Villain's line is too rare to read confidently — relying on equity alone.
```

Equity prose still renders (equity doesn't depend on chain narrowing in the same way composition does); other range-derived prose skipped.

### 3.4 Normal (regression guard)

**Input:** all sentinels False; standard chain fired or no chain (single-street decision).

**Expected render:** identical to v3.0 behavior. No regression.

### 3.5 Mass-floor truncation (MUST #28 path)

**Input:**
- Chain `truncated=True`
- `cumulative_surviving=0.08` (below 0.10 floor)
- `_villain_chain_overflowed=True` (MUST #28 sets this alongside truncated)

**Expected render:** same as §3.3 (overflow mode).

---

## 4. Schema bump

- Current: `l3_enriched_v3.0` (per manifest v1.10)
- After this ticket: `l3_enriched_v4.0`
- Backward compat: v4.0 consumers read both `range_rendering_mode` (v4) AND legacy v3.0 fields; v3.0 consumers don't see v4.0 fields (ignored — mode always "normal" in v3.0 rendering).
- CONTENT_API version in teaching/interface/CONTENT_API.md: v4.0 documents new field + render specs.

---

## 5. Ship gate coordination

**Sequence:**

1. Teaching terminal drafts CONTENT_API v4 spec in `river-rats-teaching/interface/CONTENT_API.md`
2. Teaching terminal ships v4 implementation in `l3_renderer_enriched.py`
3. Teaching terminal runs test cases §3.1–§3.5 against live stub data
4. Teaching terminal pings orchestrator: "CONTENT_API v4 ready"
5. **Orchestrator gates Stage 3.5 commit 4 (CRIT #1 + HIGH #4) on this ping.**
6. After commit 4 merges, game terminal picks up via `l3_renderer_enriched` → no game-side work beyond adapter pickup.

---

## 6. Questions for teaching terminal

- **Q1** — `folded_villain_positions` + `live_villain_positions` fields: does `enriched_row` already carry per-villain identity, or does v4 add new fields to the enriched-row schema?
- **Q2** — Blocker flag placeholder (currently gated on v2.4 blocker features landing; 2-flag design per teaching recentering §D.1): should folded/overflow mode also suppress the placeholder flag text, or leave it for the blocker-flag-design ship to handle?
- **Q3** — Equity prose in folded mode: render a simplified "hero wins by default" line, or skip entirely? (Not a hard block; default to skip for safety, revisit post-playtest.)

---

## 7. Cross-stream references

- `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md` MUST #10 / #42 / #43 — this ticket's origin
- `RELEASE_MANIFEST.yaml` v1.10 — Stage 4 gate dependency
- `knowledge/three_way_gto.md` §1.10-§1.12 — KB PRIMARY-tagging rules the new blockers feed
- `prompts/gto_labeller_v3.1.md` + future `v3.2.md` — labeller instructions (Stage 3 deliverable)

---

## 8. Standing by

Teaching terminal: pick up this ticket, spec CONTENT_API v4, implement,
run tests, ping orchestrator. Orchestrator gates Stage 3.5 commit 4.

If any spec in §2 is unclear or contradicts teaching architecture:
push back. Builder is available to revise the spec before teaching
implementation begins.
