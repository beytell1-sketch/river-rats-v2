---
date: 2026-04-16
from: Builder
to: Main terminal / Owner
re: Round 6 — Phase 2 QA clean; Track D partial blocker (PA_Board3); Group D shortlist delivered
status: 2 ITEMS NEED OWNER ATTENTION (Track D options + Group D pick)
---

# Builder Status #6

3 commits this round.

| Commit | Item | Result |
|---|---|---|
| `35fcf4b` | Phase 2 Assembly QA | ✅ PASS (483 records, all checks clean) |
| `c92fdff` | Track D curated staging | ⚠️ **3 of 4 staged; PA_Board3 blocked** |
| `47ec600` | Group D shortlist | ✅ 11 candidates delivered for owner pick |

## Phase 2 Assembly QA — PASS

10 factory JSONLs, **483 records** — all checks clean:

- 2.1 Schema: 483/483 pass. All 54 FEATURE_COLUMNS present + numeric; `villain_positions` list len 2 = `num_opponents` in every record.
- 2.2 Uniqueness: 483 unique `situation_id`s, 0 duplicates.
- 2.3 Predicate compliance: **100% on all 10 buckets** once predicates anchored to generator taxonomy (`STRONG_CATS = {two_pair, overpair, TPTK, TPGK}`). PFR_CONT ∩ MM_IP_FLOP sid overlap = 0.
- 2.4 Overlap matrix: zero sid overlap across any pair of buckets.
- 2.5 Distribution: street 22.4 / 46.4 / 31.3% flop/turn/river; `num_opponents=2` all; `equity_vs_range` mean 0.698; HRP mean 0.812; boards dominated dry_high (42%) + paired_low (30%).
- 2.6 Preflight: 0 errors on combined set.

**Flags (non-blocking, informational):**
- Taxonomy asymmetry — overpair bucket hands read as medium-made via the binary `is_strong_made` flag (overpair requires two-pair+ to pass that flag). 100% against generator-intent; 24-68% against the binary feature. Not a defect — generator is internally consistent; the binary is just stricter than the taxonomy. Worth being aware of during Phase 4 labelling.
- Position concentration: only BTN (354) + SB (129) heroes appear. Generator permits CO/HJ/BB/UTG but didn't sample them. May want a CO/HJ pass in a future iteration; not blocking.
- Action field is placeholder `CALL` across all 483 records (Phase 1 = situations-only, expected).
- 4 curated draws (Track D): pending landing — QA re-run needed when complete.

**Verdict:** 10 factory buckets ready for Phase 3. Curated re-QA pending Track D resolution.

## Track D — 3 of 4 staged, PA_Board3 BLOCKED

| sid | Stream | Status |
|---|---|---|
| `d1983_BTN_turn` | turn (row 7) | ✅ staged |
| `BP7_06` | turn (row 7) | ✅ staged |
| `d5620_BTN_flop` | flop (row 6) | ✅ staged |
| `PA_Board3_Jh8h4h_h6` | flop (row 6) | ⚠️ BLOCKED |

**PA_Board3 blocker:** Two stop conditions tripped:
1. `street='f'` → `normalise_situation` KeyError (expected `'flop'`, `'turn'`, `'river'`, or numeric)
2. `num_opponents=2` but `len(villain_positions)=1` → `build_situation()` validator ValueError

**Upstream root cause:** All 30+ PA_Board* records in the source pool share this encoding. Pool likely emitted `num_opponents` as total table size rather than villain count. Filter admitted them on the field value despite seat-list contradiction. Cannot be fixed without touching source pool — which is out of scope per task constraint.

**Per stop condition, agent wrote no JSONLs for PA_Board3 and did not partial-stage.** Committed delivery report only (`PHASE_1_4_CURATED_DELIVERY_2026-04-16.md`) with 3 options.

**3 options for owner:**
1. **Drop to 3 curated hands** (builder recommendation) — net supplement 420→**398** (−1 from the 399 target, negligible). UMBRELLA 268 already absorbs the predicate coverage.
2. **Authorise one-line PA_Board3 fixup on the curated copy** — rewrite `street='f'` → `'flop'` (normalise-able), and either drop `num_opponents` to 1 or add a second villain. Pool stays untouched; only the v23 curated copy is mutated.
3. **Substitute from NO-blocker candidates** — contradicts the "confirmed nut-blocker" directive; builder does not recommend.

## Group D shortlist — 11 candidates delivered

Stratification (per directive):

- **Source A — near-bias CHECK labels in v2.2:** 6 (over-filled; target 3-5)
  - `d3687_HJ_turn`, `d6869_CO_turn`, `d5466_CO_flop`, `d1764_BTN_turn`, `d2074_BTN_turn`, `d6826_BB_turn`
- **Source B — Pass 2 solver-confirmed CHECK overrides:** 4 (at target)
  - `d4312_CO_turn` (gold-standard), `BP5_01`, `BP4_11`, `d9556_BB_flop`
- **Source C — solver-mixed ≥40% CHECK:** 1 (**under-filled — stop condition hit**)
  - `BP4_21` only qualifier after required exclusions; agent did not relax further

**Total:** 11 (within 10-15 floor/ceiling)

**Diversity:** flop 5 / turn 6 / river 0; hand types span monster/trap (3), strong-made (2), TP-weak (2), small/middle pair (3), draw+overcards (1); IP/OOP mixed.

**Flags:**
- Source C under-fill (acknowledged stop condition — not relaxed)
- No river candidates — v2.2 river CHECK pool is weak-hand give-ups; `d3229` excluded as MW miss

**Exclusions honored:** d8886, d2410, d8963, d3178, d3688 (already in exam) + 10 MW misses (evidence-duty elsewhere).

Shortlist ready at `review/comms/GROUP_D_SHORTLIST_2026-04-16.md`. Owner picks 4, ~5-10 min async. Registry is extensible — builder ingests with no code change.

## Items needing owner attention

1. **Track D — PA_Board3 decision** (3 options above; builder recommends #1, drop to 3)
2. **Group D — pick 4 from shortlist** (Source C under-filled to 1; Source A has 6 so owner has plenty of room there; diversity-aware pick encouraged)

## Phase grid

| Phase | Status |
|---|---|
| 0 Pre-flight | ✅ GO |
| 1 Generation (factory) | ✅ 483 records, QA clean |
| 1.4 Curated | ⚠️ 3/4 staged; awaiting PA_Board3 decision |
| 1.5 Solver-sourced | 🟡 owner-led, async |
| 2 Assembly QA | ✅ PASS on 10 factory (curated re-QA pending) |
| 3 Calibration | 🟡 ready — waiting on v3 prompt smoke + Group D finalisation |
| 3.5 Pilot review | ⏸️ gated on Phase 3 |
| 4 Production labelling | ⏸️ gated on Phase 3.5 |

## Builder holding

Nothing actionable without owner direction. Phase 3 can launch once:
- Group D picks are in (registry update: 1 line, no code change)
- Track D resolved (either 3 curated or PA_Board3 fixup)

Standing by.
