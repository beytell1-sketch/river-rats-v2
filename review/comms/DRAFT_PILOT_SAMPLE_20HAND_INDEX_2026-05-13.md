# Pilot Sample Index — 20-Hand Re-Label Consistency Audit (2026-05-13)

Source corpus: `data/4way_corpus/full_700/` (batches 001-007).
Seed: `20260513`. Algorithm: stratified round-robin, see SELECTION_NOTES.

| # | spot_id | batch | position | context | street | texture | old_consensus_action | old_agreement |
|---|---------|-------|----------|---------|--------|---------|----------------------|---------------|
| 1 | `4WF-4-WAY-3--002` | batch_001 | BTN | opener | flop | rainbow_dry | BET | 5/5 |
| 2 | `4WF-4-WAY-3--011` | batch_001 | UTG | opener | flop | two_tone | BET | 4/1 |
| 3 | `4WF-4-WAY-3--015` | batch_001 | CO | opener | flop | rainbow_dry | BET | 4/1 |
| 4 | `4WF-4-WAY-3--063` | batch_002 | HJ | opener | flop | rainbow_dry | CHECK | 3/2 |
| 5 | `4WF-4-WAY-3--075` | batch_002 | CO | opener | flop | paired | BET | 5/5 |
| 6 | `4WF-4-WAY-3--077` | batch_002 | CO | opener | flop | paired | CHECK | 4/1 |
| 7 | `4WF-4-WAY-3--110` | batch_003 | CO | opener | flop | rainbow_dry | BET | 3/2 |
| 8 | `4WF-4-WAY-3--114` | batch_003 | HJ | opener | flop | rainbow_dry | CHECK | 3/2 |
| 9 | `4WF-CLOSING--213` | batch_005 | SB | opener | flop | paired | BET | 5/5 |
| 10 | `4WF-CLOSING--214` | batch_005 | SB | facing-bet | flop | two_tone | CALL | 3-1-1 |
| 11 | `4WF-CLOSING--216` | batch_005 | MP | facing-bet | flop | rainbow_dry | CALL | 3/2 |
| 12 | `4WF-CLOSING--254` | batch_006 | MP | facing-bet | flop | paired | CALL | 4/1 |
| 13 | `4WF-CLOSING--271` | batch_006 | MP | facing-bet | flop | two_tone | RAISE | 4/1 |
| 14 | `4WF-CLOSING--284` | batch_006 | EP | opener | turn | rainbow_dry | CHECK | 5/5 |
| 15 | `4WF-CLOSING--306` | batch_007 | CO | facing-bet | flop | rainbow_dry | RAISE | 5/5 |
| 16 | `4WF-CLOSING--321` | batch_007 | SB | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 17 | `4WF-CLOSING--322` | batch_007 | CO | facing-bet | flop | rainbow_dry | RAISE | 4/1 |
| 18 | `4WF-MULTIWAY-151` | batch_003 | BB | facing-bet | turn | two_tone | RAISE | 5/5 |
| 19 | `4WF-MULTIWAY-155` | batch_004 | MP | opener | flop | two_tone | CHECK | 5/5 |
| 20 | `4WF-MULTIWAY-158` | batch_004 | BB | facing-bet | turn | monotone | RAISE | 4/1 |

## Coverage summary

- Batches covered: 7/7 — {'batch_001': 3, 'batch_002': 3, 'batch_003': 3, 'batch_005': 3, 'batch_006': 3, 'batch_007': 3, 'batch_004': 2}
- Positions covered: 8 — {'BTN': 1, 'UTG': 1, 'CO': 6, 'HJ': 2, 'SB': 3, 'MP': 4, 'EP': 1, 'BB': 2}
- Action contexts covered: 2 — {'opener': 11, 'facing-bet': 9}
- Streets covered: 2 — {'flop': 17, 'turn': 3}
- Textures covered: 4 — {'rainbow_dry': 10, 'two_tone': 5, 'paired': 4, 'monotone': 1}
- Agreement split: unanimous=7, split=13 (detail: {'5/5': 7, '4/1': 8, '3/2': 4, '3-1-1': 1})
- Stratification cells covered (position x context x street x texture): 16/38 of populated cells (populated universe in 350-hand corpus).