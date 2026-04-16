---
date: 2026-04-16
from: Programmer (Phase 3.5 pilot-sample selector)
to: Main terminal (reviewer/orchestrator)
re: Phase 3.5 — pilot hand selection (16 hands), stratified per builder directive
status: DELIVERABLE — Phase 3.5.1 complete
plan: review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md §3.5.1
directive: review/comms/MAIN_TERMINAL_UPDATE_2026-04-16-c.md §3.5.1
exclusion_source: river-rats-core/calibration_exam.py (33 Phase 3 exam hands)
records_path: training-data/v23_*.jsonl (486 records total)
---

# Phase 3.5 Pilot Sample — 16 hands

## Headline

- **Total sample: 16 hands** (target 15–20, inside range).
- Stratum A predicate-matching: 7 (target 6–8)
- Stratum B non-predicate / negative controls: 4 (target 3–4)
- Stratum C §3-additions exercising: 2 (target 2–3; §3.B unreachable, see note)
- Stratum D reversal-shaped boundary: 3 (target 2–3)
- **Zero overlap with Phase 3 calibration exam** — verified against 33-hand
  exclusion set (`STANDARD_EXAM_SIZE` 28 + 5 Group D extensions).

## Exclusion verification

The Phase 3 exam (per `calibration_exam.py`) contains 33 hands:

- 24 MW reference hands (MW-12 through MW-50)
- 4 new hard anchors (d8886/d2410/d8963/d3178)
- 5 Group D reversals (d3688, d4312, d9556, d2074, d5466)

None of the 16 pilot IDs overlap (all pilot IDs are `UMBRELLA_*`,
`MM_IP_TURN_*`, `MM_OOP_TURN_*`, `RAISE_VALUE_*`, `PROT_DANGER_*`,
`PFR_CONT_*`, `BP7_06`). Verified programmatically.

## Stratum A — predicate-matching (7 hands)

All 7 Stream B.2 override-clause preconditions hold (facing_bet=False,
num_opponents=2, villain_checked_back=1, villain_range_capped=1,
worse_hand_pct≥0.55, equity_vs_range≥0.35, SPR≤2.0). Pass 1 panels
should **fire the override clause** and set `override_clause_fired = true`.

| # | sid | street | pos | hero | board | whp | evr | SPR | hand cat |
|---|---|---|---|---|---|---|---|---|---|
| A1 | UMBRELLA_067 | turn | BTN | AhAs | Ts6s3d2h | 0.95 | 0.80 | 1.11 | overpair |
| A2 | UMBRELLA_064 | river | BTN | Ah9d | 9h4c2d2h3c | 0.84 | 0.40 | 1.11 | two_pair (boundary evr) |
| A3 | UMBRELLA_217 | turn | SB  | AhAd | Th7d3c2h | 0.96 | 0.77 | 1.11 | overpair, OOP |
| A4 | UMBRELLA_231 | river | SB  | AhAs | Ts6s3d2h3c | 0.96 | 0.88 | 1.11 | overpair, OOP |
| A5 | UMBRELLA_268 | turn | SB  | AhQh | Qc9c5h2h | 0.91 | 0.71 | 1.11 | TPTK, OOP |
| A6 | MM_IP_TURN_028 | turn | BTN | Ah8h | Qs8s3d2h | 0.76 | 0.39 | 1.11 | middle_pair (boundary evr) |
| A7 | MM_IP_TURN_027 | turn | BTN | Ah6c | Ts6s3d2h | 0.73 | 0.40 | 1.11 | middle_pair (boundary evr) |

**Diversity:** 4 turn / 2 river / 1 turn+OOP-to-BTN; 3 positions (BTN / SB / CO
via MM subbucket); 4 hand categories (overpair, two_pair, TPTK, middle_pair);
whp range 0.73→0.96; evr range 0.39→0.88. A6 and A7 sit near the evr=0.35
floor to probe whether the panel still fires the clause under minimum-equity
conditions. A3/A4/A5 are OOP → stresses the "OOP value+protection" branch.

## Stratum B — non-predicate / negative controls (4 hands)

Override clause MUST NOT fire. Stratum splits across the guard axes.

| # | sid | guard axis | hero | board | action_string |
|---|---|---|---|---|---|
| B1 | RAISE_VALUE_012 | facing_bet=1 | AhAc | Qs6d2h | SB check, BB bet, BTN ??? |
| B2 | RAISE_VALUE_013 | facing_bet=1 | AhAd | Jd8c3s | SB check, BB bet, BTN ??? |
| B3 | PROT_DANGER_011 | vcb=0 (flop, no prior check-back) | Ah9h | Jd9d8s | SB check, BB check, BTN ??? |
| B4 | PFR_CONT_025 | vcb=0 (flop, no prior check-back) | AhAd | Js6d2c | SB check, BB check, BTN ??? |

**Rationale:**

- **B1/B2** test `facing_bet` guard: clause is irrelevant when hero
  faces a live bet. Expect panels to reason from pot-odds / composition /
  hand strength (RAISE for value is the factory-intended action) without
  citing override.
- **B3** tests `vcb=0` guard AND probes whether the MW-27 ambiguity
  (action_history says "both checked this street", feature `villain_checked_back`
  counts prior-street only) causes panels to fire the clause via "spirit"
  rather than precondition. A correct negative-control pass keeps
  `override_clause_fired=false` because vcb=0 mechanically.
- **B4** same as B3 but hero is PFR on a dry board — the "default c-bet
  IP" temptation may make panels want to fire the clause even though vcb=0.
  Double-test of negative-control discipline.

## Stratum C — §3-additions (2 hands)

The v3 prompt adds 4 tagged sections (§3.A–§3.D). §3.B has **zero** factory
records satisfying its trigger condition (HRP=0.00 **and** visibly strong
hand), so §3.B cannot be probed from the Phase 1 record set. §3.C tag
overlaps substantially with §3.A (Step 3 enhancement ↔ DO NOT Rule 10);
§3.A is the harder test.

| # | sid | §3 tag | angle probed |
|---|---|---|---|
| C1 | BP7_06 | §3.A (compressed-SPR checked-to) | AhJh on Qh9d5h7c turn; CO in 3-way checked-to, SPR 1.11, whp=0.31 (fails predicate's whp gate). Hero is a strong semi-bluff (NFD + overcard). Probes whether panels apply §3.A's "default to BET" framing WITHOUT firing the override clause (predicate fails on whp). |
| C2 | MM_OOP_TURN_001 | §3.D (MW CHECK-lean pattern) | Ah9h on Kh9d3c2h turn; SB OOP, middle pair+BDFD, vcb=1, vrc=0 (BB defender is uncapped). Exercises DO NOT Rule 10 language but predicate fails on vrc=0 — panels must reason from the calibration note without citing Stream B.2 override clause. |

**Note on §3.B:** Every factory record checked has `hero_range_percentile`
in [0.41, 0.97]; none at 0.00. This is consistent with the prompt's own
framing — §3.B warns about a test-harness artifact, not a production
pattern. Documented, not a stop condition.

**Note on §3.C:** The tag maps to "Step 3 action-enumeration enhancement"
— adding the "value extraction / deny further equity" choice at
compressed-SPR checked-to. This overlaps with the predicate itself (A1–A7
exercise it implicitly). C1 and C2 both exercise §3.C indirectly by
including the compressed-SPR checked-to frame.

## Stratum D — reversal-shaped boundary (3 hands)

All three are mechanically **inside** the predicate (all 7 preconditions
hold) but sit at the MEDIUM-confidence boundary: `equity_vs_range ≈ 0.35–0.40`.
These will stress whether panels maintain 4/4 agreement under reduced-
margin value-bet conditions or fracture into CHECK (pot-control) /
BET (override-clause-driven) splits.

| # | sid | hero | board | whp | evr | boundary axis |
|---|---|---|---|---|---|---|
| D1 | MM_IP_TURN_003 | Ah9s | Kh9d3c2h | 0.76 | 0.40 | near-evr-floor |
| D2 | MM_IP_TURN_030 | Ah8c | Qs8s3d2h | 0.76 | 0.38 | near-evr-floor |
| D3 | MM_IP_TURN_033 | Ah8c | Ks8s4h2h | 0.75 | 0.36 | near-evr-floor (closest) |

All three are middle-pair+A-kicker on turn IP vs two checks. D3 sits at
evr=0.36 — within 0.01 of the 0.35 precondition floor; the panel's
evr-reading stability is tested here. Informational: if panels split
on these three, the prompt's "equity_vs_range ≥ 0.35" threshold may
need a buffer (or the tightness of this boundary documented).

## Per-criterion coverage map

| Gate criterion | Stratum coverage |
|---|---|
| 1 — override clause behaviour | Stratum A (positive: 7 hands should fire), Stratum B (negative: 4 hands must NOT fire), Stratum D (boundary: should fire per predicate, but at the precondition-floor) |
| 2 — §3 additions engagement | Stratum C (2 hands target §3.A + §3.D explicitly); Stratum A indirectly exercises §3.C |
| 3 — inter-panel variance | Stratum A (expect 4/4 on strong spots A1/A3/A4/A5), Stratum D (expect some variance at boundary D2/D3) |
| 4 — Pass 2 engagement | Any Pass 2 instance (depends on Pass 1 disagreements); most likely surfaced on D2/D3 |
| 5 — reasoning quality | All 16 hands contribute |

## Stop-condition check

- [x] 15+ hands sampled with proper stratification (16 ≥ 15)
- [x] Zero overlap with Phase 3 exam (exclusion set verified programmatically)
- [x] Enough non-predicate hands across available buckets (4 hands across
      2 guard axes — facing_bet and vcb=0)
- [ ] §3.B probe skipped — factory records have no HRP=0.00 cases. This
      limits Criterion 2 coverage to §3.A + §3.D + indirect §3.C. Not
      blocking.

## Next step

3.5.2 — run 4 Pass 1 panels + 0–2 Pass 2 review panels on these 16 hands,
preserving verbatim reasoning. Output to
`training-data/v23_pilot_labelled.jsonl`.
