---
date: 2026-04-15
from: Builder (Programmer)
to: Teaching team
re: v2.2 enriched label export — handoff for L3 renderer Phase 2
---

# Teaching Handoff — v2.2 Enriched Labels

## Files

| File | Location | Rows |
|---|---|---|
| `v2_2_enriched_for_teaching.jsonl` | `river-rats-v2/training-data/` | 385 |
| `v2_2_enriched.jsonl` (copy) | `river-rats-teaching/data/` | 385 |

Both files are byte-identical copies.

---

## Schema

Each row is one hand. Fields:

| Field | Type | Description |
|---|---|---|
| `situation_id` | string | Unique hand identifier (e.g. `BP1_01`, `d4312_CO_turn`) |
| `consensus_action` | string | Final v2.2 label post-Phase 3.5H — one of: BET, CHECK, CALL, RAISE, FOLD |
| `hand_bucket` | string | Majority hand_bucket across T1-T4 (see bucket values below) |
| `intentions` | list[string] | Union of T1-T4 intention tags, deduped, order preserves first-seen |
| `primary_intention` | string | Most common first-intention across T1-T4; tie-break by team order |
| `street_plan_tags` | list[string] | Union of T1-T4 street_plan_tags for flop/turn hands; **empty list for river hands** |
| `feature_attention` | dict[string, string] | Feature name → highest tier across T1-T6 (see tier semantics below) |
| `difficulty` | int | Consensus difficulty across T1-T4: 1=clear, 2=likely_clear, 3=standard, 4=hard |
| `reasoning_by_team` | dict[string, string] | Keys `T1`–`T4`; full reasoning text per team — not aggregated |
| `full_feature_vector` | dict[string, any] | All 54 raw features from the situation text |

### Hand bucket values

- `drawing` — primary equity comes from flush/straight draw
- `value` — strong made hand betting for value
- `bluff_catcher` — medium made hand with showdown value facing aggression
- `air` — no made hand, no significant draw
- `protection` — made hand betting to deny free cards
- `made_hand` — general made hand (used when sub-category is unclear)

### Intention tag vocabulary (6 canonical)

- `value_extract` — betting or raising with a hand that expects to be called by worse
- `pot_control` — checking or calling to manage pot size with a medium-strength hand
- `range_fold_priced_out` — folding because pot odds don't justify continuing
- `deny_equity` — raising or betting to force draws to pay a price or fold
- `continue_draw` — calling to realize draw equity at a profitable price
- `bluff_fold_better` — betting or raising as a bluff targeting a better-but-foldable range

### Street plan tag vocabulary (10 canonical)

`bet_protect_evaluate`, `continue_on_blank`, `draw_continue`, `give_up_on_complete`,
`check_evaluate`, `check_raise_strong`, `bet_fold`, `check_call`, `barrel_turn`,
`pot_control`

---

## Multi-intention hands

Most hands have a single `primary_intention`. Some have 2–3 in the `intentions` list.

Reading multi-intention rows:
- `primary_intention` is the dominant strategic motivation (the reason the action was taken)
- Additional `intentions` are supplementary — they describe secondary effects or plan legs that a single-intention label would miss
- Example: a hand with `intentions: ["deny_equity", "continue_draw"]` is primarily raising to fold out equity (deny_equity) but also has a draw that justifies continuing when called (continue_draw)
- Do not interpret supplementary intentions as equal-weight motivations — `primary_intention` is the load-bearing label for any model that needs a single target

---

## Feature_attention tier semantics

Each feature in the `feature_attention` dict carries one of three tiers:

| Tier | Source | Meaning |
|---|---|---|
| `PRIMARY` | T1-T4 labelling teams | Feature **drove the decision** — removing it would change the action |
| `CONFIRMED` | T1-T4 labelling teams | Feature **verified the decision** — consistent with the action, not the primary driver |
| `DISCOVERED` | T5-T6 bottom-up discovery scan | Feature was **not initially tagged** by T1-T4 but the discovery teams found it relevant from the feature vector up, without knowing the action |

When a feature appears at multiple tiers across teams, the exported value is the highest tier (PRIMARY > CONFIRMED > DISCOVERED). A CONFIRMED tag from T2 and a DISCOVERED tag from T6 for the same feature will export as CONFIRMED.

---

## The 22 Phase 3.5H label changes

These are the hands where `consensus_action` differs from the original Pass 1 label. Any renderer tests that were built against Pass 1 labels will need to be updated for these 22 hands.

| situation_id | Old label | New label | Source |
|---|---|---|---|
| `BP1_03` | CALL | RAISE | Pass1+relabel consensus |
| `BP2_28` | CALL | FOLD | Pass1+relabel consensus |
| `BP4_11` | BET | CHECK | Pass1+relabel consensus |
| `BP4_19` | CHECK | BET | Pass1+relabel consensus |
| `BP4_20` | CHECK | BET | Pass1+relabel consensus |
| `BP4_21` | BET | CHECK | Pass 2 — solver mixed zone, owner kept CHECK |
| `BP4_22` | BET | CHECK | Pass1+relabel consensus |
| `BP4_24` | BET | CHECK | Pass1+relabel consensus |
| `BP4_30` | BET | CHECK | Pass1+relabel consensus |
| `BP5_01` | BET | CHECK | Pass 2 + solver override |
| `BP5_10` | CHECK | BET | Pass1+relabel consensus |
| `BP5_12` | BET | CHECK | Pass1+relabel consensus |
| `BP5_17` | CHECK | BET | Pass1+relabel consensus |
| `BP6_04` | RAISE | CALL | Pass1+relabel consensus |
| `BP7_01` | RAISE | CALL | Pass 2 — no solver, Pass 2 CALL stands |
| `BP7_11` | RAISE | CALL | Pass1+relabel consensus |
| `d4312_CO_turn` | BET | CHECK | Pass 2 + solver override |
| `d5222_BTN_flop` | CALL | FOLD | Pass 2 — solver confirms FOLD (close) |
| `d5620_CO_turn` | CALL | FOLD | Pass 2 — solver confirms FOLD |
| `d5749_HJ_turn` | CALL | FOLD | Pass 2 — solver confirms FOLD |
| `d8886_BTN_flop` | BET | CHECK | Pass 2 — solver mixed, owner kept CHECK |
| `d8963_HJ_turn` | BET | CHECK | Pass 2 — solver mixed, owner kept CHECK |

Direction of change: 8 BET→CHECK, 3 CHECK→BET, 4 RAISE→CALL, 3 CALL→FOLD, 2 CALL→RAISE+FOLD.
Net effect: CHECK +6, FOLD +4, BET -6, RAISE -2, CALL -2.

---

## Data provenance

- **385 hands** = 200 reconstructed d-series + 185 factory-generated BP-series
- **Pass 1 labelling**: 4 teams (T1-T4), 39 batches each, using amended Approach C + Exp 3 auxiliary flags
- **Pass 2**: full-panel review on 13 split/hard spots; solver verification on 13 hands
- **Phase 3.5**: villain-seat inference, BP situation regeneration, BP relabel, final assembly
- **Discovery**: T5 (20 batches) and T6 (39 batches) performed bottom-up feature scans after labels were finalised

---

## Known caveats

### 10 MW reference set misses (Gate 7 pending)

The v2.2 model scores 80.0% on the 50-hand MW reference set against a target of 82.5%. All 10 misses are hands where the correct action is BET but the model predicted CHECK. This is a systematic bucket-first CHECK bias identified in both solver verification (v2.3 backlog item 7) and training evaluation.

These 10 MW misses are drawn from hands in the `test_set_50.jsonl` test set, not from the 385 training hands. However, the bias originates from the training label distribution (CHECK is the largest class at 34% and the labelling prompt had a passive lean on mixed-strategy spots).

If teaching is conducting quality audits against this export, the same CHECK-over-BET bias may appear in borderline hands in the training set — particularly in the hand classes BET/CHECK on wet boards with medium made hands (e.g. top-pair hands OOP on dynamic boards). The 22 label changes listed above already corrected the most clear-cut cases from this category.

Gate 7 decision (ship v2.2 / iterate) is pending owner solver time. The export reflects the current approved label set regardless of that decision.

---

## What this export does not contain

- The `attn_*` binary columns from `v2_2_training.csv` — those are training-pipeline artifacts. The `feature_attention` dict in this export conveys the same information in a more interpretable form.
- Pass 2 override rationale — available in `training-data/bp_pass2_final_overrides.json` and `review/comms/PHASE_3_5_BP_PASS2_REPORT_2026-04-15.md`
- Solver verification details — available in `training-data/solver_verification_log.jsonl`
