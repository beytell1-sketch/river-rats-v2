---
date: 2026-04-16
from: Programmer
to: Architecture Expert / Owner
re: Phase 2 Assembly QA dry-run — v2.3 supplement JSONLs
scope: `review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md` Phase 2
directive: Owner directive `10247b6` — QA-only, hard stop before production labelling
status: PASS
---

# Phase 2 Assembly QA — dry-run report

Read-only QA pass on the 10 factory-generated v2.3 supplement JSONLs.
No labelling performed. No model touches. No Phase 3 work.

## Files inspected

**Factory files (10/10 present):**
- `training-data/v23_mm_ip_flop.jsonl` (19)
- `training-data/v23_mm_ip_turn.jsonl` (38)
- `training-data/v23_mm_oop_turn.jsonl` (25)
- `training-data/v23_mon_checked.jsonl` (19)
- `training-data/v23_pfr_cont.jsonl` (25)
- `training-data/v23_prot_danger.jsonl` (20)
- `training-data/v23_raise_value.jsonl` (25)
- `training-data/v23_sm_ip_river.jsonl` (19)
- `training-data/v23_sm_ip_turn.jsonl` (25)
- `training-data/v23_umbrella_fill.jsonl` (268)

**Curated files (0/2 present):** The parallel agent has not yet landed
`v23_curated_draw_flop.jsonl` / `v23_curated_draw_turn.jsonl`. Per
directive, QA run proceeds on the 10 factory JSONLs alone; curated-file
QA is a follow-up task once they land.

**Total records:** **483** (matches generator overshoot targets exactly:
OS sum 19+38+25+19+25+20+25+19+25+268 = 483).

---

## 2.1 Combined schema check — PASS

- Every record has all **54 `FEATURE_COLUMNS`** present.
- Every `FEATURE_COLUMNS` value is numeric (int / float / bool) —
  no stringified `street='flop'` or similar ANOMALY-A-class regressions.
- `street` is numeric in 483/483 records.
- `hero_position` is numeric in 483/483 records.
- `villain_positions` is a list in 483/483 records; length equals
  `num_opponents = 2` in **all** 483 records (0 integrity issues).
- Required metadata (`situation_id`, `hero_cards`, `board_cards`,
  `action_string`) present in 483/483.

**Result:** 483 / 483 schema-pass.

## 2.2 Hand-ID uniqueness — PASS

- `situation_id` count: 483
- Unique `situation_id`s: 483
- Duplicate count: **0** (within-file and cross-file)

## 2.3 Per-bucket predicate compliance — PASS

Predicates use the generator's taxonomy (`generate_factory_batch6.py`,
lines 212-226): `STRONG_CATS = {two_pair, overpair, top_pair_top_kicker,
top_pair_good_kicker}`, `MONSTER_CATS = {trips, set, straight, flush,
full_house, quads, straight_flush}`, `MEDIUM_CATS = {top_pair, mid_pair,
middle_pair, low_pair, bottom_pair, pair, underpair}`. (Note: the binary
feature `is_strong_made` uses the canonical "two-pair-or-better"
definition from `hand_categories.is_strong_made`, which differs from
the generator's taxonomy — the generator's taxonomy is the correct
anchor for verifying the generator's bucket intent.)

| Bucket                 | Predicate                                                                                                           | Match | Total | %      |
|------------------------|---------------------------------------------------------------------------------------------------------------------|------:|------:|-------:|
| `v23_mm_ip_flop`       | medium-made hero ∧ `is_ip=1`                                                                                        |    19 |    19 | 100.0% |
| `v23_mm_ip_turn`       | medium-made hero ∧ `is_ip=1`                                                                                        |    38 |    38 | 100.0% |
| `v23_mm_oop_turn`      | medium-made hero ∧ `is_ip=0`                                                                                        |    25 |    25 | 100.0% |
| `v23_mon_checked`      | monster hero ∧ prev-street check in action history                                                                  |    19 |    19 | 100.0% |
| `v23_pfr_cont`         | `is_preflop_aggressor=1` ∧ checked-to                                                                               |    25 |    25 | 100.0% |
| `v23_prot_danger`      | medium-made ∧ `danger_score≥0.25 ∨ flush_danger≥0.25 ∨ straight_danger≥0.25`                                        |    20 |    20 | 100.0% |
| `v23_raise_value`      | `facing_bet=1` ∧ strong/monster hero                                                                                |    25 |    25 | 100.0% |
| `v23_sm_ip_river`      | strong/monster hero ∧ `is_ip=1` ∧ river                                                                             |    19 |    19 | 100.0% |
| `v23_sm_ip_turn`       | strong/monster hero ∧ `is_ip=1` ∧ turn                                                                              |    25 |    25 | 100.0% |
| `v23_umbrella_fill`    | `facing_bet=0 ∧ num_opponents=2 ∧ villain_checked_back=1 ∧ villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧ equity_vs_range≥0.35 ∧ spr≤2.0` | 268 |   268 | 100.0% |

**All buckets ≥ 95%.** No flags.

**PFR_CONT ∩ MM_IP_FLOP sid overlap check:** 0 — no significant overlap
between PFR continuation and MM IP flop buckets, per scope clarification.

### Note on canonical vs generator taxonomy

A first pass using the canonical `is_strong_made=1` flag produced
compliance flags at SM_IP_TURN (40%), SM_IP_RIVER (68%), RAISE_VALUE
(24%), and PROT_DANGER (50%). The cause is that the generator counts
`overpair` as strong-made (per its STRONG_CATS set, consistent with
common poker usage) while the 54-feature vector's binary
`is_strong_made` flag does not (two-pair-or-better). Every record in
those buckets is either `two_pair` / `set` (canonical strong) or
`overpair` (generator strong), so the generator-intent predicate holds
at 100% everywhere. **This is not a defect**, but it is a taxonomy
asymmetry worth noting: downstream code that branches on the binary
`is_strong_made` flag will treat overpair-bucket hands as medium-made.
Flagged for Architect awareness — may or may not be action-relevant
for Phase 4 labelling prompts.

## 2.4 Cross-bucket sid overlap — PASS

No `situation_id` overlaps across any pair of the 10 factory buckets.
Each bucket occupies a disjoint sid namespace.

Note on content overlap (not sid): the umbrella (268 hands) satisfies
the Section-2 predicate by construction. Some Section-1 rows
(MM_IP_FLOP / MM_IP_TURN / SM_IP_TURN / SM_IP_RIVER / MM_OOP_TURN /
MON_CHECKED / PFR_CONT) produce hands that would ALSO satisfy the
umbrella predicate if overlaid, but the generator writes each hand to
a single bucket with a unique sid, so there is no accidental
double-counting. This matches scope §0 Interpretation U (umbrella
absorbs Section-1 shapes via predicate, not via sid reuse).

## 2.5 Distribution sanity

### Street distribution (combined, n=483)
- flop (0): 108 (22.4%)
- turn (1): 224 (46.4%)
- river (2): 151 (31.3%)

Matches the build-plan weighting (turn-heavy for MM + SM + PROT +
umbrella; flop for PFR + MM_IP_FLOP; river for SM_IP_RIVER).

### Hero position (numeric encoding, n=483)
- 3 (BTN): 354 (73.3%)
- 4 (SB): 129 (26.7%)

All IP hands are BTN, all OOP hands are SB. The generator supports
CO/HJ/BB/UTG but the current Phase-1 output uses only BTN (IP) and SB
(OOP). **Informational flag** — this is a narrower position
distribution than the generator's `ARCHETYPES_IP / _OOP` lists permit.
It does not fail the QA gate (no position-diversity gate is defined in
the build plan), but Architect may want to confirm this is the
intended distribution before Phase 4.

### num_opponents
- 2: 483 (100%) — uniform, matches scope (3-way = hero + 2 villains).

### equity_vs_range
- mean = 0.698, median = 0.745, std = 0.176
- min = 0.289, max = 0.964
Heavy right skew — expected, since 9/10 buckets target medium-to-strong
hero hands in checked-to or facing-bet spots.

### hero_range_percentile
- mean = 0.812, median = 0.885, std = 0.180
- min = 0.184, max = 0.997
Strong skew toward top-of-range hero hands — expected for a BET-biased
supplement.

### Board-type distribution
- dry_high: 205 (42.4%)
- paired_low: 147 (30.4%)
- wet_connected: 54 (11.2%)
- dynamic: 42 (8.7%)
- wet_flush: 31 (6.4%)
- dry_low: 4 (0.8%)

### Action placeholder observation
All 483 records show `action: CALL`. This is the default placeholder
from `extract_all_features()` (no `exp` passed at spec time). Phase 1
is situations-only — production labels arrive in Phase 4. Confirmed
this is a placeholder, not a real label. **Informational only.**

### villain_checked_back / villain_range_capped
- `villain_checked_back=1`: 375 / 483 (77.6%) — the 108 with =0 are
  mostly flop hands (PFR_CONT + MM_IP_FLOP + PROT_DANGER) and
  RAISE_VALUE (facing-bet).
- `villain_range_capped=1`: 458 / 483 (94.8%) — the 25 with =0 are
  all RAISE_VALUE (villain is the aggressor in that bucket).

## 2.6 Schema preflight on combined — PASS

Ran the equivalent of `train_model._preflight_schema_check()` (numeric
`street` + numeric `hero_position` guard) across all 483 records.
Result: **0 preflight errors**. No ANOMALY-A regression.

---

## Verdict

**PASS — ready for Phase 3 (calibration gate), pending curated file
arrival.**

All six QA sections (2.1-2.6) clean. No duplicate sids, no schema
failures, 100% predicate compliance on all 10 buckets, no
cross-bucket sid overlap, expected distribution shapes,
preflight clean.

### Flags (informational, non-blocking)

1. **Taxonomy asymmetry** — generator's `STRONG_CATS` includes
   `overpair` but binary feature `is_strong_made` does not.
   Downstream code branching on the binary flag will see
   overpair-bucket hands as medium-made. Non-action-item unless
   Phase 4 prompts reference the binary feature.
2. **Position concentration** — only BTN and SB heroes appear, even
   though the generator's archetype lists permit CO/HJ/BB/UTG.
   Architect to confirm intended.
3. **Curated files not yet present** — 4 curated drawing-hand
   JSONLs (flop + turn, nut-draw + blocker) are still pending from
   the parallel agent. Follow-up QA required once they land.
4. **Action placeholder** — all records carry `action: CALL`.
   This is the default serialisation placeholder; real labels come
   in Phase 4. Not a defect.

### Recommendation

**Ready for Phase 3** on the 10 factory buckets. Do NOT proceed past
Phase 3 until the 4 curated JSONLs arrive and pass the same QA.

### Blockers

None.

---

## Reproducibility

QA script: `/tmp/v23_qa/run_qa.py` (ephemeral; not committed). Runs
read-only against `training-data/v23_*.jsonl` and emits the six-section
output above. Can be re-run on the combined 14-file set once curated
files land.
