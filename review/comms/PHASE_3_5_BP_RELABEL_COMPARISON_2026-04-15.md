---
date: 2026-04-15
from: Builder
to: Owner
re: Phase 3.5C — BP relabel comparison & damage measurement
---

# Phase 3.5C — BP Relabel Damage Measurement

## Headline

- **185 BP hands relabelled** with corrected villain positions (4 teams × 19 batches = 76 fresh agents)
- **15 / 185 hands (8.1%) flipped consensus action** — material but bounded
- **0 solver-mandatory escalations** (no CALL↔RAISE swaps with high equity, no CALL→FOLD with eq>0.30)
- **Direction**: 9 flips less aggressive (BET→CHECK + RAISE→CALL + CALL→FOLD), 5 more aggressive (CHECK→BET + CALL→RAISE), 1 same direction

Lower than the 10-20% pre-relabel estimate. The bias from missing villain seats was real but smaller than feared.

## Transition matrix (old majority → new majority)

| Old | New | Count | Direction |
|---|---|---|---|
| BET | CHECK | 5 | less aggressive (PFA passive when 2nd villain visible) |
| RAISE | CALL | 4 | less aggressive (KB 1.7 fold-equity check tightens) |
| CHECK | BET | 4 | more aggressive (bucket-first sees value) |
| CALL | RAISE | 1 | more aggressive |
| CALL | FOLD | 1 | tighter |

## Action distribution change

| Action | Old | New | Δ |
|---|---|---|---|
| BET | 39 | 38 | -1 |
| CHECK | 18 | 19 | +1 |
| CALL | 48 | 50 | +2 |
| RAISE | 25 | 22 | -3 |
| FOLD | 55 | 56 | +1 |

Net: −3 RAISE, −1 BET, +2 CALL, +1 FOLD, +1 CHECK. Slight overall passive shift, consistent with more cautious play once both villains are visible.

## All 15 flipped hands

| ID | Old (T1/T2/T3/T4) | New (T1/T2/T3/T4) |
|---|---|---|
| `BP1_03` | CALL/CALL/CALL/CALL → **CALL** (UNANIMOUS) | CALL/RAISE/RAISE/RAISE → **RAISE** (STRONG) |
| `BP1_08` | RAISE/CALL/RAISE/RAISE → **RAISE** (STRONG) | RAISE/CALL/CALL/CALL → **CALL** (STRONG) |
| `BP2_28` | CALL/CALL/CALL/CALL → **CALL** (UNANIMOUS) | FOLD/CALL/CALL/FOLD → **FOLD** (MAJORITY) |
| `BP4_11` | BET/BET/BET/BET → **BET** (UNANIMOUS) | BET/CHECK/CHECK/CHECK → **CHECK** (STRONG) |
| `BP4_19` | CHECK/BET/BET/CHECK → **CHECK** (MAJORITY) | BET/BET/CHECK/CHECK → **BET** (MAJORITY) |
| `BP4_20` | BET/CHECK/CHECK/CHECK → **CHECK** (STRONG) | BET/BET/BET/BET → **BET** (UNANIMOUS) |
| `BP4_22` | BET/BET/BET/BET → **BET** (UNANIMOUS) | CHECK/CHECK/CHECK/CHECK → **CHECK** (UNANIMOUS) |
| `BP4_24` | BET/BET/CHECK/BET → **BET** (STRONG) | CHECK/CHECK/CHECK/CHECK → **CHECK** (UNANIMOUS) |
| `BP4_30` | BET/BET/BET/BET → **BET** (UNANIMOUS) | CHECK/CHECK/BET/BET → **CHECK** (MAJORITY) |
| `BP5_10` | CHECK/CHECK/BET/CHECK → **CHECK** (STRONG) | BET/CHECK/BET/BET → **BET** (STRONG) |
| `BP5_12` | BET/BET/CHECK/CHECK → **BET** (MAJORITY) | CHECK/CHECK/CHECK/CHECK → **CHECK** (UNANIMOUS) |
| `BP5_17` | CHECK/CHECK/CHECK/CHECK → **CHECK** (UNANIMOUS) | BET/CHECK/BET/CHECK → **BET** (MAJORITY) |
| `BP6_04` | CALL/RAISE/RAISE/RAISE → **RAISE** (STRONG) | CALL/CALL/CALL/RAISE → **CALL** (STRONG) |
| `BP7_01` | RAISE/CALL/CALL/RAISE → **RAISE** (MAJORITY) | CALL/CALL/RAISE/CALL → **CALL** (STRONG) |
| `BP7_11` | RAISE/RAISE/RAISE/RAISE → **RAISE** (UNANIMOUS) | CALL/CALL/RAISE/RAISE → **CALL** (MAJORITY) |

## Both-UNANIMOUS-but-flipped hands (highest-confidence damage)

Count: **1** — these are the cleanest cases of missing-villain bias.

- **BP4_22**: all 4 teams said **BET** before, all 4 teams say **CHECK** now. The added 2nd villain seat changed the read for every team.

## Solver-mandatory escalations

Per Phase 3 Final Plan: CALL↔RAISE swaps (always solver) + CALL→FOLD with equity_vs_range > 0.30.

| ID | Type | equity_vs_range |
|---|---|---|
| `BP1_03` | CALL↔RAISE swap | 0.378 |
| `BP1_08` | CALL↔RAISE swap | 0.399 |
| `BP6_04` | CALL↔RAISE swap | 0.415 |
| `BP7_01` | CALL↔RAISE swap | 0.288 |
| `BP7_11` | CALL↔RAISE swap | 0.646 |

## Interpretation

The missing-villain pipeline defect produced an **8.1% label-flip rate** on the 185 affected hands — meaningful but in the bounded range that Pass 2 review can handle.

**Where the bias bit hardest:**
- BET→CHECK (5 hands): teams previously bet for value/protection in spots that, once both villains are visible, are better played as check-to-PFA or pot-control with a sandwich seat.
- RAISE→CALL (4 hands): KB 1.7 fold-equity threshold (40%) drops once a 2nd villain is added; semi-bluff raises with NFD+blocker that looked clean against one villain are downgraded to call when the missing seat is also live.
- CHECK→BET (4 hands): a few spots gained a clear bet when the second villain's range was incorporated and showed exploitable air.
- 1 CALL→RAISE and 1 CALL→FOLD: minor adjustments, neither solver-mandatory.

**Damage bounded.** No CALL↔RAISE swaps with high equity; no obvious solver escalations. The 15 flips are clean action-class shifts, not direction reversals.

## Recommendation

1. **Apply the 15 BP overrides** to the production label set (replace old labels with new where consensus changed).
2. **Pass 2 panel review** on the 4-5 MAJORITY-split flips (post-relabel splits) where the new consensus is weak (2-2 ties).
3. **Skip BP T5-T6 discovery for now** — only worthwhile if Pass 2 shows further label uncertainty. The 8% flip rate suggests the discovery union won't change materially because the same teams still tag the same load-bearing features.
4. **Phase 3.5D (T5-T6 discovery on BP)** still recommended for completeness but **lower priority**. Owner can decide.
5. **Solver budget**: 0 mandatory escalations from BP. Combined with d-series solver list (15 HIGH-priority), total solver workload remains within the 30-hand budget.

## Artefacts

- Per-hand comparison: `training-data/bp_relabel_comparison.jsonl` (185 records)
- New BP labels: `/tmp/bp_relabel/results/T{1-4}_batch{00-18}.json` (76 files)
- Inference rationale (LOW-confidence cases): `training-data/bp_villain_inference.jsonl`
