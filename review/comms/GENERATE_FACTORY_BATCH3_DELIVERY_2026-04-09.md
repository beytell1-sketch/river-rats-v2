# Generate Factory Batch 3 — Delivery Confirmation

**Date:** 9 April 2026
**From:** Lead Programmer
**To:** Reviewer / Owner
**Re:** `generate_factory_batch3.py` — 151-situation factory script

---

## Delivery

File written to:
`river-rats-v2/review/generate_factory_batch3.py`

---

## Scope Delivered

Script generates all 151 training situations across 10 sub-patterns:

| Sub-pattern | Label | Count |
|-------------|-------|-------|
| SP1 | Monster wet board RAISE | 18 |
| SP2 | Monster dry low-SPR RAISE | 10 |
| SP3 | OOP check-raise RAISE | 12 |
| SP4 | Monster suppressors CALL | 6 |
| SP5 | Semi-bluff raise RAISE | 28 |
| SP6 | Semi-bluff suppressed CALL | 13 |
| SP7 | OOP thin value RAISE | 25 |
| SP8 | River bluff raise RAISE | 16 |
| SP9 | Flat spots CALL | 10 |
| SP10 | Middle range CALL | 13 |
| **Total** | | **151** |

---

## Board Bases Defined

33 board bases defined (B01-B31, B33). Two boards require dual-SPR variants:

- **B10** (eff_stack=810, SPR=9.0) — used by SP10_02
- **B10_LOW** (eff_stack=135, SPR=1.5) — used by SP2_01, SP2_02
- **B17** (eff_stack=540, SPR=3.0) — used by SP3, SP7, SP9 situations
- **B17_LOW** (eff_stack=270, SPR=1.5) — used by SP2_03, SP2_04

B32 is defined in the allocation inventory but carries no situation assignments after FIX 1 from the board allocation review. It is omitted from the script to prevent accidental use.

---

## Critical Corrections Applied

All corrections from the board allocation review and design agent deliveries are incorporated:

1. **B05 effective_stack = 530** (SPR=5.89, below S4 threshold of 6.0 — all B05 SP1 situations are clean RAISE)
2. **B26 villain_positions = ['CO']** (FIX 3 — BTN folded on flop, CO is sole active villain and bettor)
3. **B25 villain_positions = ['BB']** (SB folded on flop)
4. **B27 villain_positions = ['SB']** (BB folded on flop)
5. **SP3_06 uses B13** (FIX 2 — moved from B10, which has to_call=0 and cannot produce a check-raise)
6. **SP4_01 and SP4_02 use B33** (FIX 4 — moved from B15/B06 per allocation review)
7. **SP5_09 on B08: ['Ac', '8d']** (Qc is on the board — cannot appear in hero hand)
8. **SP5_12 on B09: ['Kh', 'Jd']** (Ah is on the board — Kh is highest available heart draw)
9. **SP6_12: B14 ['As', 'Qh'], fold_equity failure mode** (flush_block_pct==0 structurally impossible when holding flush-suit card)
10. **SP6_13: B04 ['8s', '7d']** (no diamonds — demonstrates block=0 + no nut draw)
11. **SP8_10 on B26: ['Jc', '8d']** (Jc Th makes K-high straight with board — revised to gutshot that missed)

---

## Open Flags (for reviewer attention)

These were flagged by design agents and carried into the script as description notes. They require architectural or GTO Expert resolution, not programmer action.

**SP10_09 IP thin value threshold:**
SP10_09 (B28, range_pct=0.72) is 0.03 below the 0.75 threshold required for the "IP thin value CALL" contrast group. Only 2 of the required 3 qualifying IP situations (SP10_10 and SP10_11) meet the criterion. Design Agent 3 flagged this. Either the threshold needs relaxing or a replacement situation is needed.

**B17 to_call=0 leading action:**
SP3_10, SP7_05, SP7_11, and SP7_18 use B17 which has to_call=0 (hero leads, not check-raises or raises against a bet). Description fields in these situations note the flag. The feature extractor may still produce valid features from this game state, but the action context differs from the majority of SP3/SP7 situations.

---

## Script Behaviour

- **Pre-flight count check:** `_check_situation_counts()` runs before any I/O. If any sub-pattern count is wrong, the script aborts with a clear message.
- **BUILD_EXCEPTION:** Logged; situation skipped (not written to JSONL).
- **VALIDATION_ERRORS:** Logged; situation written with `has_errors=True`.
- **Clean situations:** Written with `has_errors=False`.
- **Output path:** `river-rats-v2/training-data/factory_batch3_situations.jsonl`

---

## Script Has NOT Been Run

Per protocol, this script awaits reviewer approval before execution.

---

## Ready for review

