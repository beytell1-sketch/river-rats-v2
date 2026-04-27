---
from: ml-architect (round 8 reviewer)
date: 2026-04-27
pr: 84
branch: orch/blueprint-v3-6-targeted-37-templates-2026-04-27
re: Round 8 review — Blueprint v3.6 routing verification
verdict: CHANGES_REQUESTED
---

# ML-Architect Review — Blueprint v3.6 Routing Verification

## Review method

Read blueprint v3.6 in full, the binding round 7 review (REVIEW_ML_ARCHITECT_PR80_PHASE6),
the Phase 7 directive, the F5 allocator source at origin/master, and all four expanded
module files at origin/master (magg_scenarios, pfa_scenarios, nfd_scenarios,
sb_hero_scenarios). All arithmetic is re-derived from source. Prior round 7 findings
are the baseline; this review focuses on routing correctness and quota fill projections.

---

## Item 1 — MAGG-A pot=50 count: 3, not 4

**Verdict: Architect is correct. Round 7 review was wrong.**

Source inspection of `magg_scenarios.py` at origin/master:

```
grep -B2 'pot.*50\.0' magg_scenarios.py
```

Results: five records at pot=50.0 at lines 43, 75, 204, 318, 455.

- Lines 43, 75: legacy records (original 10 templates), boards `Kd7s2c5hJd` and `Ah9c4d2sKh`.
- Lines 204, 318, 455: Phase 6 MAGG-A templates: A-04 (`Th4d2c6hAc`), A-14 (`Kc8h4d2sQd`), A-26 (`Qc9h6d3sTd`).

MAGG-A-24 (line ~428) is at pot=55.0, not 50.0. Round 7 review counted this as a fourth
MAGG-A at pot=50; that was an error. The actual count is 3 Phase-6 MAGG-A records at pot=50,
plus 2 legacy records. The architect's correction is verified correct.

This does not change the net +5 magg target (3 adjustments + 2 new = 5).

---

## Item 2 — F5 allocator scarcity mechanism

**Verified from source (lines 372–476, `scripts/build_corpus_revision_500_hand.py`).**

The algorithm:

1. Classifies all pool records into category sets (multi-membership allowed).
2. Computes `scarcity[cat] = PHASE_A_QUOTAS[cat] / max(1, yield_per_cat[cat])` — **frozen once at start**.
3. Sorts records descending by max-scarcity of their eligible categories.
4. Assigns each record to highest-scarcity still-open category; adds to `used_fps`.

Key properties confirmed:
- Scarcity is frozen at initial pool yield counts, not updated as records fill.
- Each record assigned once; `used_fps` prevents re-use.
- Ties within same scarcity value are broken by pre-shuffled order (seeded RNG).

Post-Phase-7 scarcity values (computed from expected yields):

| Category     | Quota | Phase-7 yield | Scarcity |
|-------------|-------|---------------|---------|
| nfd_boundary | 10    | 10            | 1.0000  |
| nfd_call     | 20    | 20            | 1.0000  |
| sb           | 20    | 20            | 1.0000  |
| nfd_raise    | 20    | 20            | 1.0000  |
| bac          | 20    | 20            | 1.0000  |
| monster      | 20    | 20            | 1.0000  |
| rule11       | 10    | 10            | 1.0000  |
| donk         | 25    | 25            | 1.0000  |
| magg         | 40    | 64            | 0.6250  |
| spr_med      | 40    | 53            | 0.7547  |
| pfa          | 80    | 166           | 0.4819  |
| spr_std      | 50    | 151           | 0.3311  |

Phase-7 yield deltas: pfa +28 (2 MAGG-NEW + 8 SPR-MED + 18 PFA-9), magg +2 (new templates),
spr_med +8 (SPR-MED new) -3 (MAGG-A-50 adjustments remove them from spr_med pool),
spr_std +24 (PFA-9 + NFD-B + NFD-CALL + SB), nfd_boundary +3, nfd_call +2, sb +1.

---

## Item 3 — MAGG routing (+5): CORRECT

**Verdict: Routing analysis correct.**

All five MAGG additions have category set `{magg, pfa}`:

- MAGG-A-04 adjusted (pot=52, SPR=1.923): SPR < 2.0 → not spr_med, not spr_std. `{magg, pfa}`.
- MAGG-A-14 adjusted (pot=52, SPR=1.923): same.
- MAGG-A-26 adjusted (pot=53, SPR=1.887): same.
- MAGG-NEW-01 (pot=54, SPR=1.852): same.
- MAGG-NEW-02 (pot=56, SPR=1.786): same.

Post-Phase-7 scarcity: `magg=0.625 > pfa=0.482`. All five route to magg. Correct.

Villain_aggression_count preservation: pot value change does not affect action_history
or aggression count computation. The magg assertion (`villain_aggression_count=2`) still
passes.

`_is_magg_hand` confirmed from source: requires `feat_dict.villain_aggression_count >= 2`
AND `rec['street'] == 'river'`. All five templates have this (existing action histories
preserved; new templates explicitly specify this structure).

magg fill projection: Phase-6 magg fill = 35. With 3 adjusted and 2 new records now
routing to magg: 35 + 3 + 2 = 40. Target met.

---

## Item 4 — SPR-MED routing (+8): ROUTING CORRECT; FILL COUNT INCORRECT

**Verdict: Routing analysis is correct. Fill count has an accounting error — CHANGES_REQUESTED.**

### Routing (correct)

All eight SPR-MED templates have category set `{pfa, spr_med}`:
- hero_pos CO or BTN → `_is_sb_hero_hand` = False (not SB, not sb_hero_scenarios).
- generation_source='pfa_scenarios' → not sb, not donk, not rule11.
- villain_aggression_count=0 (flop with no prior villain bet) + street=flop → `_is_magg_hand` = False.
- pot 28–45 BB → SPR 2.22–3.57 → spr_med (2.0 ≤ SPR < 4.0) = True.
- is_preflop_aggressor=1 → pfa = True.
- Category set: `{pfa, spr_med}`.

Post-Phase-7 scarcity: `spr_med=0.7547 > pfa=0.4819`. All eight route to spr_med. Routing
is correct.

### Fill count (incorrect — accounting error)

The blueprint's accounting note states:

> "Returns 3 spr_med slots to the unmet pool (freeing space for the 8 new SPR-MED templates
> to fill them)"

This is backwards. The three MAGG-A adjustments do not free spr_med slots for other templates;
they **remove three records that were actively filling spr_med in Phase 6**.

Phase 6 spr_med fill derivation (verified against round 7 analysis):

| Source | Count | Category set | Routing |
|--------|-------|-------------|---------|
| MAGG-B (22) | 22 | {magg, pfa, spr_med} | spr_med (0.83 > 0.65 > 0.58) |
| MAGG-A-04/14/26 (3) | 3 | {magg, pfa, spr_med} | spr_med |
| Legacy MAGG at pot=50 (2) | 2 | {magg, pfa, spr_med} | spr_med |
| Mode A pure spr_med | ~5 | {spr_med} | spr_med |
| **Total fills** | **32** | | |

The three MAGG-A-04/14/26 records were among the 32 fills. Adjusting their pot to 52–53 BB
removes them from the spr_med pool — they now have SPR < 2.0 and classify as `{magg, pfa}`
only. Removing them reduces spr_med fill by 3.

Phase 7 spr_med fill:

| Change | Delta |
|--------|-------|
| Phase 6 baseline | +32 |
| MAGG-A-04/14/26 adjusted (removed from spr_med) | −3 |
| 8 new SPR-MED templates | +8 |
| **Expected Phase 7 fill** | **37** |

**37 < 40. spr_med is still 3 short.**

The blueprint projection table shows spr_med going from 32 to 40 (+8), but the correct
projection is 32 → 37 (+5 net). The total corpus projection of 500 is therefore overstated
by 3: expected actual = 497, not 500.

**Required fix: add 3 more SPR-MED templates (total 11 new, not 8).**

Alternatively: accept 497/500 and document the 3-hand shortfall, with a note that the
fill can be attempted empirically.

The 2 legacy MAGG records at pot=50 are also noted as unresolved: they still route to
spr_med (blueprint correctly notes them as informational advisory, not mandatory fix).
If the builder adjusts them too, it further reduces spr_med fill by 2 more, requiring
13 new SPR-MED templates total. Blueprint's advisory not to adjust them without verifying
no side-effects is correct.

---

## Item 5 — PFA routing (+18): CORRECT

**Verdict: Routing analysis correct.**

All 18 PFA-9 templates:
- is_preflop_aggressor=1 (opener_position=hero_pos for all) → pfa eligible.
- villain_aggression_count=0 (flop with no prior villain bet) → `_is_magg_hand` = False.
- pot 14–20 BB → SPR 5.0–7.14 → spr_std (SPR ≥ 4.0) → spr_std eligible.
- hero_pos ∈ {CO, BTN, HJ} → not SB → sb not eligible.
- generation_source will be 'pfa_scenarios' → not donk, not rule11.
- Category set: `{pfa, spr_std}` for all 18.

Post-Phase-7 scarcity: `pfa=0.4819 > spr_std=0.3311`. All 18 route to pfa. Correct.

No magg contamination: none of the 18 are river decisions with villain_aggression_count ≥ 2.
Three templates (PFA-9e, 9k, 9q) have BB fold preflop — blueprint correctly requires
`('preflop', 'BB', 'fold')` in action_history and BB excluded from villain_positions.

Turn-cbet cap note: max_turn_cbets=15 applies only to templates where `tmpl['street'] == 'turn'`.
All 18 are flop decisions. No cap conflict.

pfa fill: 62 + 18 = 80 = quota. Correct.

---

## Item 6 — nfd_boundary routing (+3): CORRECT WITH MANDATORY GATE

**Verdict: Routing analysis correct. Empirical verification gate correctly required.**

Three templates (NFD-B-08 spades, NFD-B-09 diamonds, NFD-B-10 clubs):
- All use 4-card turn boards with 3 flush-suit cards + villain two-barrel pattern.
- has_flush_draw=1 verified: hero Ace + 3 board flush cards = 4 total.
- nut_flush_block=1 verified: `compute_nut_flush_block` threshold for 4-card board is
  3 board cards of same suit; all three templates have exactly 3 board flush cards;
  hero holds Ace of that suit; made-flush exclusion (≥5 total) not triggered (3 board
  + 1 hero = 4 < 5).
- NFD-B-08 hero_cards conflict correctly identified and resolved: AsJd replaces AsKh
  (which was used by existing T4 board 6s3s2c9s). Fingerprints are distinct.
- Category set depends on empirical air_pct:
  - If `_validate_nfd_boundary` passes (|actual − target| ≤ 0.03): `{nfd_boundary, spr_std}`.
  - If fails: falls to `{nfd_raise, spr_std}` or `{nfd_call, spr_std}`.
- SPR=5.0 for all → spr_std co-category.
- Post-Phase-7 scarcity: nfd_boundary=1.0 >> spr_std=0.33 → routes to nfd_boundary.

Empirical verification protocol is correctly specified. Builder must run extraction
before commit. Architect also correctly notes the structural ceiling at ~0.21 for
two-barrel patterns, making target values 0.18–0.20 achievable.

NFD_AIR_TARGETS = [0.15, 0.17, 0.20, 0.22, 0.25], tolerance = 0.03 (confirmed from source).
Targets 0.18 and 0.19 fall within tolerance of 0.17 or 0.20. Target 0.20 is exactly on
the [0.20] target. All three designed targets are within the reachable zone.

nfd_boundary fill: 7 + 3 = 10 = quota, assuming all three pass R4 gate.

---

## Item 7 — nfd_call routing (+2): CORRECT WITH MANDATORY GATE AND ONE STRUCTURAL NOTE

**Verdict: Routing analysis correct. Self-correction of NFD-CALL-NEW-02 design is correct.
Structural risk noted.**

NFD-CALL-NEW-01 (board: KsQs9d, hero: AsJs):
- has_flush_draw=1: As+Js (hero) + Ks+Qs (board) = 4 spades.
- nut_flush_block=1: threshold for 3-card board = 2 board cards of same suit;
  board has Ks+Qs = 2 spades; hero holds As → nut_flush_block=1.
- Empirical air_pct required: K-Q-9 board is value-heavy for BTN opener (KQ, KJ, sets).
  Low air_pct expected. Must confirm < 0.20 before commit.
- Non-hearts board (spades) per Phase 7 directive.

NFD-CALL-NEW-02 (revised: board KdJd8s, hero AdTd):
- Original spec had Ad on board — correctly caught and redesigned by architect.
  Original board AdKd7s with hero QdJd: Ad on board, not in hero hand → nut_flush_block=0.
  Revised: board KdJd8s, hero AdTd. Ad in hero hand, board has Kd+Jd = 2 diamonds.
  has_flush_draw=1: Ad+Td + Kd+Jd = 4 diamonds. nut_flush_block=1. Correct.
- Empirical air_pct required: K-J board is value-heavy for CO opener. Must confirm < 0.20.
- Non-hearts board (diamonds) per directive.

Structural risk (flagged, not blocking if empirical gate passes):
Post-Phase-7 scarcity: nfd_call=1.0, nfd_boundary=1.0. These two categories are tied.
If a template's air_pct falls in the boundary window (0.15–0.25 within ±0.03 of any
NFD_AIR_TARGET), `_classify_record` uses the `if/elif` structure — `_validate_nfd_boundary`
is checked first. If it passes, category = `nfd_boundary` (not nfd_call). This is
deterministic (not a random tie), but means the builder needs air_pct clearly below 0.15
to guarantee nfd_call routing. Architect correctly notes this: target air_pct < 0.15
for a clean nfd_call. The 6-step verification protocol covers this adequately.

Non-hearts requirement per Phase 7 directive: The directive says non-hearts specifically
because the hearts-suit bias reliably produces air < 0.10 — that is the MECHANISM, not
a restriction. The constraint is: verify air < 0.20 empirically. Using non-hearts boards
for the two new nfd_call templates demonstrates the mechanism generalises beyond hearts.
Architect's interpretation of the directive is correct.

nfd_call fill: 18 + 2 = 20 = quota, assuming empirical air_pct gates pass.

---

## Item 8 — sb routing (+1): CORRECT

**Verdict: Routing analysis correct.**

SB-N-08:
- hero_pos=SB → `_is_sb_hero_hand` = True (both paths: generation_source='sb_hero_scenarios'
  AND hero_position='SB').
- opener_position=BTN → is_preflop_aggressor=0 → no pfa eligibility.
- pot=17 BB → SPR=5.88 → spr_std.
- street=flop, villain_aggression_count=1 (BTN bet on flop, first bet) + not river → no magg.
- BB folded preflop → BB not in villain_positions=['BTN']. Correctly included
  `('preflop', 'BB', 'fold')` in action_history.
- Closest existing SB board Qs7h2c vs Qs6c2d: different mid card and suits. Distinct.
- Category set: `{sb, spr_std}`.
- Post-Phase-7 scarcity: sb=1.0 > spr_std=0.33 → routes to sb.

sb fill: 19 + 1 (21 templates, ~20 pass at 95% rate) = 20 = quota.

---

## Item 9 — Per-template routing matrix (end of blueprint)

**Verdict: Matrix present and routing claims correct for all 37 entries, subject to the
spr_med accounting error identified in Item 4.**

The blueprint provides a complete per-template routing verification table (lines 1183–1199)
with columns: template, intended quota, all eligible categories, highest-scarcity category,
and reason.

All routing entries are correct per post-Phase-7 scarcity values:
- `{magg, pfa}` → magg (0.625 > 0.482) ✓ (5 MAGG entries)
- `{pfa, spr_med}` → spr_med (0.755 > 0.482) ✓ (8 SPR-MED entries)
- `{pfa, spr_std}` → pfa (0.482 > 0.331) ✓ (18 PFA-9 entries)
- `{nfd_boundary, spr_std}` → nfd_boundary (1.0 >> 0.33) ✓ (3 NFD-B entries)
- `{nfd_call, spr_std}` → nfd_call (1.0 >> 0.33) ✓ (2 NFD-CALL entries)
- `{sb, spr_std}` → sb (1.0 > 0.33) ✓ (1 SB entry)

Risk flags in the matrix are correctly identified (NFD empirical gate, SPR-MED overflow
to pfa if spr_med fills early). No routing entry is wrong.

The accounting error is in the corpus projection table (line 1145–1159), not the routing
matrix itself.

---

## Item 10 — TC-26 V-Integration-Trace

One representative template traced per module.

### MAGG — MAGG-A-04 (adjusted)

Spec: hero_pos=BTN, villain=['BB'], board=['Th','4d','2c','6h','Ac'], hero=['9s','8d'],
pot=52.0 (adjusted from 50.0), street=river.

SituationFactory: opener_position='BTN' = hero_pos → is_preflop_aggressor=1.
action_history: BB bets flop + bets turn → villain_aggression_count=2.
spr = 100/52 = 1.923 (below 2.0, not spr_med, not spr_std).

`_classify_record`: magg=True (aggression_count=2, street=river). pfa=True (is_pfa=1).
spr=1.923 → neither spr_med nor spr_std.
Category: `{magg, pfa}`.

`_phase_a_select`: scarcity[magg]=0.625 > scarcity[pfa]=0.482. Assigned to magg.

Corpus: record reaches magg quota with villain_aggression_count=2 feature. Trace complete.

### SPR-MED — SPR-MED-01

Spec: hero_pos=CO, villain=['BTN','BB'], board=['Kh','8s','3d'], hero=['Ac','Jc'],
pot=30.0, street=flop. opener_position=CO.

SituationFactory: is_preflop_aggressor=1. villain_aggression_count=0.
spr = 100/30 = 3.333 (spr_med range).
has_flush_draw: Ac+Jc hero, 0 clubs on board → 2 clubs total < 4 → has_flush_draw=0.
generation_source='pfa_scenarios' → not sb, not donk.

`_classify_record`: pfa=True, not magg (flop, aggression=0), not sb. spr_med=True.
Category: `{pfa, spr_med}`.

`_phase_a_select`: scarcity[spr_med]=0.755 > scarcity[pfa]=0.482. Assigned to spr_med.

Corpus: record reaches spr_med quota with spr=3.333 feature. Trace complete.

### PFA — PFA-9a

Spec: hero_pos=HJ, villain=['BTN','BB'], board=['Ad','5c','3h'], hero=['Kh','Ks'],
pot=14.0, street=flop. opener_position=HJ.

SituationFactory: is_preflop_aggressor=1. villain_aggression_count=0.
spr = 100/14 = 7.14 (spr_std range, ≥4.0). Not spr_med.

`_classify_record`: pfa=True, not magg, not sb. spr_std=True.
Category: `{pfa, spr_std}`.

`_phase_a_select`: scarcity[pfa]=0.482 > scarcity[spr_std]=0.331. Assigned to pfa.

Corpus: record reaches pfa quota with is_preflop_aggressor=1 feature. Trace complete.

### NFD-B-08 (nfd_boundary)

Spec: hero_pos=BB, villain=['BTN'], board=['8s','4s','2d','6s'], hero=['As','Jd'],
pot=20.0, to_call=7.0, street=turn.

SituationFactory: 3 board spades (8s+4s+6s) + As (hero) = 4 spades → has_flush_draw=1.
threshold for 4-card board = 3; board_s=3 → flush_suits={s}; hero holds As → nut_flush_block=1.
spr = 100/20 = 5.0 (spr_std).

`_classify_record`: nfd=True (has_flush_draw=1 AND nut_flush_block=1).
_validate_nfd_boundary called: if actual villain_air_pct within ±0.03 of any target → nfd_boundary.
spr=5.0 → spr_std.
Category (if passes R4): `{nfd_boundary, spr_std}`.

`_phase_a_select`: scarcity[nfd_boundary]=1.0 >> spr_std=0.33. Assigned to nfd_boundary.

Corpus: record reaches nfd_boundary quota. R4 gate must be empirically cleared. Trace complete.

### NFD-CALL-NEW-02 (nfd_call)

Spec: hero_pos=BB, villain=['CO'], board=['Kd','Jd','8s'], hero=['Ad','Td'],
pot=13.0, to_call=4.0, street=flop.

SituationFactory: Ad+Td (hero) + Kd+Jd (board) = 4 diamonds → has_flush_draw=1.
board_d=2 (Kd+Jd), threshold for 3-card board = 2 → flush_suits={d}.
hero holds Ad → nut_flush_block=1. Made-flush exclusion: 2+2=4 < 5 → not triggered.
spr = 100/13 = 7.69 (spr_std).

`_classify_record`: nfd=True.
_validate_nfd_boundary called. K-J board with CO opener is value-heavy → air_pct expected
well below 0.15. If air_pct < 0.15: not boundary (does not fall within ±0.03 of any
NFD_AIR_TARGET in [0.15,0.17,0.20,0.22,0.25]). Category = `{nfd_call, spr_std}`.
If 0.15 ≤ air_pct < 0.20 and within boundary window: category = `{nfd_boundary, spr_std}`.
Empirical verification gate required.

`_phase_a_select` (assuming air_pct < 0.15): scarcity[nfd_call]=1.0 >> spr_std=0.33.
Assigned to nfd_call.

Corpus: record reaches nfd_call quota with nut_flush_block=1. Trace complete (conditional
on empirical gate).

### SB — SB-N-08

Spec: hero_pos=SB, villain=['BTN'], board=['Qs','6c','2d'], hero=['8h','7h'],
pot=17.0, to_call=5.0, street=flop.

SituationFactory: generation_source='sb_hero_scenarios', hero_position='SB'.
opener_position=BTN → is_preflop_aggressor=0.
villain_aggression_count=1 (BTN bet on flop, only one aggression action, not river) → not magg.
spr = 100/17 = 5.88 (spr_std). No flush draw (0 hearts on board, 2 hearts in hero hand = 2 < 4).

`_classify_record`: sb=True (both generation_source and hero_position paths).
pfa=False (is_pfa=0). spr_std=True.
Category: `{sb, spr_std}`.

`_phase_a_select`: scarcity[sb]=1.0 > spr_std=0.33. Assigned to sb.

Corpus: record reaches sb quota with hero_position='SB'. Trace complete.

All six traces complete. Value flows correctly from spec to category fill for all six
modules — subject to empirical verification gates for nfd_boundary and nfd_call templates.

---

## Summary of findings

| Finding | Severity | Item | Disposition |
|---------|----------|------|-------------|
| spr_med fill count error: +8 claimed but +5 net (3 MAGG-A adjustments remove 3 spr_med fills) | HIGH | 4 | CHANGES_REQUESTED: add 3 more SPR-MED templates (11 total) or accept 497-hand corpus |
| MAGG-A pot=50 count: architect corrected to 3 (round 7 said 4) — verified from source | INFO | 1 | No action needed; architect is right |
| SPR-MED-04 has stray apostrophe in key name `villain_positions':` in blueprint doc | LOW | 4 | Fix formatting in spec doc before build |
| NFD-CALL routing: boundary/call distinction is deterministic (elif chain), not a scarcity tie | INFO | 7 | Architect's risk note slightly overstates ambiguity; determinism confirmed |
| All per-template routing claims correct (both category membership and scarcity ordering) | PASS | 9 | No action |
| Empirical air_pct verification protocols correctly specified for NFD-B and NFD-CALL | PASS | 6,7 | Builder must execute before commit |

---

## Verdict: CHANGES_REQUESTED

The routing analysis for all 37 templates is correct — every template's category membership
and scarcity-based routing destination is verified against actual `_classify_record` and
`_phase_a_select` source. No template would route to the wrong quota.

However, the corpus projection table contains a material accounting error: the blueprint
claims spr_med goes from 32 to 40 (+8 net), but the correct projection is 32 − 3 + 8 = 37
(+5 net), because the three MAGG-A pot adjustments remove three records that were actively
filling spr_med in Phase 6. The total 500-hand projection is overstated by 3.

The fix is straightforward: add 3 more pure `{pfa, spr_med}` templates (same design
pattern as SPR-MED-01 through -08, extending to SPR-MED-09/10/11). This maintains the
37-template count but adjusts the distribution (11 SPR-MED, 15 PFA-9, everything else
unchanged). Alternatively, accept 497/500 and document the residual gap.

All other routing claims are correct and approve-ready. The MAGG +5, PFA +18, NFD-B +3,
NFD-CALL +2, and SB +1 projections are mathematically sound.
