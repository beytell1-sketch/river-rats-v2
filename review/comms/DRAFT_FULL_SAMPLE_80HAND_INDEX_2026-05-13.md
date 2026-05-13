# Full Sample Index — 80-Hand Re-Label Consistency Audit (2026-05-13)

Source corpus: `data/4way_corpus/full_700/` (batches 001-007, 350 input hands; 337 consensus rows; 265 postflop in-consensus universe).
Seed: `20260513`. Algorithm: pilot-pinned anchor + 60 deterministic Stage B free picks (see SELECTION_NOTES).

The 20-hand pilot (`DRAFT_PILOT_SAMPLE_20HAND_2026-05-13.jsonl`) is a strict subset; pilot rows marked with `*` in the # column.

| # | spot_id | batch | position | context | street | texture | old_consensus_action | old_agreement |
|---|---------|-------|----------|---------|--------|---------|----------------------|---------------|
| 1* | `4WF-4-WAY-3--002` | batch_001 | BTN | opener | flop | rainbow_dry | BET | 5/5 |
| 2 | `4WF-4-WAY-3--004` | batch_001 | HJ | opener | flop | two_tone | CHECK | 5/5 |
| 3* | `4WF-4-WAY-3--011` | batch_001 | UTG | opener | flop | two_tone | BET | 4/1 |
| 4 | `4WF-4-WAY-3--013` | batch_001 | BTN | facing-bet | flop | two_tone | FOLD | 5/5 |
| 5* | `4WF-4-WAY-3--015` | batch_001 | CO | opener | flop | rainbow_dry | BET | 4/1 |
| 6 | `4WF-4-WAY-3--017` | batch_001 | HJ | opener | flop | rainbow_dry | CHECK | 5/5 |
| 7 | `4WF-4-WAY-3--021` | batch_001 | BTN | facing-bet | flop | two_tone | CALL | 5/5 |
| 8 | `4WF-4-WAY-3--023` | batch_001 | UTG | opener | flop | two_tone | BET | 5/5 |
| 9 | `4WF-4-WAY-3--039` | batch_001 | UTG | opener | flop | two_tone | CHECK | 5/5 |
| 10 | `4WF-4-WAY-3--041` | batch_001 | BTN | facing-bet | flop | two_tone | FOLD | 5/5 |
| 11 | `4WF-4-WAY-3--043` | batch_001 | MP | opener | flop | paired | BET | 5/5 |
| 12 | `4WF-4-WAY-3--053` | batch_002 | HJ | opener | flop | two_tone | CHECK | 5/5 |
| 13* | `4WF-4-WAY-3--063` | batch_002 | HJ | opener | flop | rainbow_dry | CHECK | 3/2 |
| 14 | `4WF-4-WAY-3--064` | batch_002 | BTN | opener | flop | paired | CHECK | 5/5 |
| 15 | `4WF-4-WAY-3--066` | batch_002 | UTG | opener | flop | two_tone | CHECK | 3/2 |
| 16 | `4WF-4-WAY-3--072` | batch_002 | EP | opener | flop | two_tone | BET | 5/5 |
| 17* | `4WF-4-WAY-3--075` | batch_002 | CO | opener | flop | paired | BET | 5/5 |
| 18 | `4WF-4-WAY-3--076` | batch_002 | BTN | opener | flop | paired | BET | 5/5 |
| 19* | `4WF-4-WAY-3--077` | batch_002 | CO | opener | flop | paired | CHECK | 4/1 |
| 20 | `4WF-4-WAY-3--083` | batch_002 | EP | opener | flop | two_tone | CHECK | 5/5 |
| 21 | `4WF-4-WAY-3--086` | batch_002 | MP | opener | flop | rainbow_dry | BET | 4/1 |
| 22 | `4WF-4-WAY-3--090` | batch_002 | EP | opener | flop | two_tone | BET | 5/5 |
| 23 | `4WF-4-WAY-3--091` | batch_002 | BTN | facing-bet | flop | rainbow_dry | CALL | 4/1 |
| 24 | `4WF-4-WAY-3--109` | batch_003 | EP | opener | flop | two_tone | BET | 5/5 |
| 25* | `4WF-4-WAY-3--110` | batch_003 | CO | opener | flop | rainbow_dry | BET | 3/2 |
| 26* | `4WF-4-WAY-3--114` | batch_003 | HJ | opener | flop | rainbow_dry | CHECK | 3/2 |
| 27 | `4WF-4-WAY-3--118` | batch_003 | EP | opener | flop | rainbow_dry | BET | 5/5 |
| 28 | `4WF-4-WAY-3--119` | batch_003 | BTN | facing-bet | flop | two_tone | FOLD | 4/1 |
| 29 | `4WF-4-WAY-3--121` | batch_003 | CO | opener | flop | paired | BET | 5/5 |
| 30* | `4WF-CLOSING--213` | batch_005 | SB | opener | flop | paired | BET | 5/5 |
| 31* | `4WF-CLOSING--214` | batch_005 | SB | facing-bet | flop | two_tone | CALL | 3-1-1 |
| 32* | `4WF-CLOSING--216` | batch_005 | MP | facing-bet | flop | rainbow_dry | CALL | 3/2 |
| 33 | `4WF-CLOSING--218` | batch_005 | UTG | opener | turn | rainbow_dry | CHECK | 5/5 |
| 34 | `4WF-CLOSING--220` | batch_005 | SB | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 35 | `4WF-CLOSING--223` | batch_005 | CO | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 36 | `4WF-CLOSING--231` | batch_005 | MP | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 37 | `4WF-CLOSING--246` | batch_005 | HJ | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 38 | `4WF-CLOSING--248` | batch_005 | EP | opener | turn | rainbow_dry | BET | 5/5 |
| 39 | `4WF-CLOSING--253` | batch_005 | SB | facing-bet | flop | two_tone | RAISE | 4/1 |
| 40* | `4WF-CLOSING--254` | batch_006 | MP | facing-bet | flop | paired | CALL | 4/1 |
| 41 | `4WF-CLOSING--261` | batch_006 | SB | facing-bet | flop | rainbow_dry | RAISE | 5/5 |
| 42 | `4WF-CLOSING--263` | batch_006 | MP | facing-bet | flop | two_tone | FOLD | 5/5 |
| 43 | `4WF-CLOSING--269` | batch_006 | SB | opener | flop | paired | BET | 5/5 |
| 44 | `4WF-CLOSING--270` | batch_006 | SB | facing-bet | flop | rainbow_dry | RAISE | 5/5 |
| 45* | `4WF-CLOSING--271` | batch_006 | MP | facing-bet | flop | two_tone | RAISE | 4/1 |
| 46 | `4WF-CLOSING--279` | batch_006 | UTG | opener | turn | two_tone | CHECK | 5/5 |
| 47* | `4WF-CLOSING--284` | batch_006 | EP | opener | turn | rainbow_dry | CHECK | 5/5 |
| 48 | `4WF-CLOSING--291` | batch_006 | UTG | opener | turn | paired | CHECK | 4/1 |
| 49 | `4WF-CLOSING--298` | batch_006 | HJ | facing-bet | flop | rainbow_dry | FOLD | 5/5 |
| 50 | `4WF-CLOSING--300` | batch_006 | SB | opener | flop | paired | BET | 5/5 |
| 51 | `4WF-CLOSING--302` | batch_006 | UTG | opener | turn | rainbow_dry | CHECK | 4/1 |
| 52* | `4WF-CLOSING--306` | batch_007 | CO | facing-bet | flop | rainbow_dry | RAISE | 5/5 |
| 53 | `4WF-CLOSING--318` | batch_007 | SB | facing-bet | flop | two_tone | RAISE | 5/5 |
| 54* | `4WF-CLOSING--321` | batch_007 | SB | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 55* | `4WF-CLOSING--322` | batch_007 | CO | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 56 | `4WF-CLOSING--327` | batch_007 | CO | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 57 | `4WF-CLOSING--329` | batch_007 | UTG | opener | turn | paired | CHECK | 5/5 |
| 58 | `4WF-CLOSING--333` | batch_007 | UTG | opener | turn | paired | CHECK | 5/5 |
| 59 | `4WF-CLOSING--335` | batch_007 | CO | facing-bet | flop | paired | RAISE | 4/1 |
| 60 | `4WF-MULTIWAY-142` | batch_003 | HJ | opener | flop | two_tone | BET | 5/5 |
| 61 | `4WF-MULTIWAY-148` | batch_003 | MP | opener | flop | two_tone | BET | 4/1 |
| 62 | `4WF-MULTIWAY-149` | batch_003 | EP | opener | flop | two_tone | BET | 5/5 |
| 63* | `4WF-MULTIWAY-151` | batch_003 | BB | facing-bet | turn | two_tone | RAISE | 5/5 |
| 64 | `4WF-MULTIWAY-152` | batch_003 | EP | opener | flop | two_tone | BET | 5/5 |
| 65 | `4WF-MULTIWAY-154` | batch_004 | BB | facing-bet | turn | monotone | RAISE | 5/5 |
| 66* | `4WF-MULTIWAY-155` | batch_004 | MP | opener | flop | two_tone | CHECK | 5/5 |
| 67* | `4WF-MULTIWAY-158` | batch_004 | BB | facing-bet | turn | monotone | RAISE | 4/1 |
| 68 | `4WF-MULTIWAY-162` | batch_004 | BB | facing-bet | turn | monotone | CALL | 3/2 |
| 69 | `4WF-MULTIWAY-165` | batch_004 | EP | opener | flop | two_tone | BET | 5/5 |
| 70 | `4WF-MULTIWAY-167` | batch_004 | BB | facing-bet | turn | paired | RAISE | 4/1 |
| 71 | `4WF-MULTIWAY-174` | batch_004 | BB | facing-bet | turn | monotone | RAISE | 4/1 |
| 72 | `4WF-MULTIWAY-175` | batch_004 | BTN | facing-bet | flop | monotone | RAISE | 4/1 |
| 73 | `4WF-MULTIWAY-184` | batch_004 | MP | opener | flop | paired | CHECK | 5/5 |
| 74 | `4WF-MULTIWAY-186` | batch_004 | BB | facing-bet | turn | monotone | RAISE | 5/5 |
| 75 | `4WF-MULTIWAY-195` | batch_004 | BB | facing-bet | turn | paired | RAISE | 4/1 |
| 76 | `4WF-MULTIWAY-201` | batch_004 | BB | facing-bet | turn | paired | RAISE | 4/1 |
| 77 | `4WF-MULTIWAY-208` | batch_005 | BB | facing-bet | turn | two_tone | RAISE | 5/5 |
| 78 | `4WF-RANGE-AS-337` | batch_007 | BTN | facing-bet | flop | paired | FOLD | 5/5 |
| 79 | `4WF-RANGE-AS-341` | batch_007 | HJ | facing-bet | flop | rainbow_dry | FOLD | 5/5 |
| 80 | `4WF-RANGE-AS-343` | batch_007 | HJ | facing-bet | flop | rainbow_dry | FOLD | 5/5 |

## Coverage summary

- Total hands: 80 (of which 20 pilot, marked `*`)
- **Pilot ⊂ Full: VERIFIED** (20/20 pilot spot_ids in full sample)
- Batches covered: 7/7 — {'batch_002': 12, 'batch_006': 12, 'batch_004': 12, 'batch_001': 11, 'batch_003': 11, 'batch_005': 11, 'batch_007': 11}
- Positions covered: 8 — {'BTN': 10, 'UTG': 10, 'CO': 10, 'HJ': 10, 'SB': 10, 'MP': 10, 'EP': 10, 'BB': 10}
- Action contexts covered: 2 — {'opener': 42, 'facing-bet': 38}
- Streets covered: 2 — {'flop': 62, 'turn': 18}
- Textures covered: 4 — {'two_tone': 28, 'rainbow_dry': 27, 'paired': 19, 'monotone': 6}
- Agreement split: unanimous=47, split=33 (detail: {'5/5': 47, '4/1': 26, '3/2': 6, '3-1-1': 1})
- 4-D stratification cells populated (pos × ctx × street × tex): 32 cells

## Chi-square stratification preservation (pilot ⊂ full)

- chi² = **5.550**
- dof = 7 (8 effective buckets from 32 populated cells; cells with expected count < 1 pooled into a 'rare' bucket)
- minimum expected per-cell count (before pooling) = 0.250
- critical value at p=0.05: 14.067
- decision: chi² < critical → **PRESERVED (p > 0.05)**
- interpretation: the pilot's 4-D cell distribution is statistically indistinguishable from a quarter-scale draw from the 80-hand sample; the audit spec §3.2 preservation gate is satisfied.
