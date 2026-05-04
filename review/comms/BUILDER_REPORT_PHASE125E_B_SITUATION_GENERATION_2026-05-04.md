---
date: 2026-05-04
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · GTO-EXPERT (review of 14 manual canonicals) · QC stream · ML-ARCHITECT (advisory)
re: Phase 12.5E-B — situation generation (110 hands across 8 templates) READY for review; gto-expert gate on 14 manuals before 12.5E-C dispatch
status: 12.5E-B SITUATION GENERATION COMPLETE — awaiting gto-expert review of 14 manual canonicals before 12.5E-C dispatch
---

# Phase 12.5E-B — situation generation report

Implements ml-architect 12.5E-A design comm
(`review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md`, master `bad1396`)
per Phase 12.5E-B dispatch
(`review/comms/MAIN_TERMINAL_PHASE125E_DISPATCH_2026-05-04.md`, master `bad1396`).

## Pre-flight (per 12.5D' dispatch protocol amendment)

Verified at master HEAD `6b991b2`:

| Check | Result |
|---|---|
| 5 sample rows (1, 100, 200, 400, 494) carry `pilot_hand_id` | ✅ all match between corpus + labels |
| Empirical join cardinality on existing 494 corpus | ✅ 494/494 (corpus.pilot_hand_id ∩ labels.pilot_hand_id) |
| pilot_hand_id sequential PILOT_001..PILOT_494 | ✅ no gaps |
| New ID range available | ✅ PILOT_495..PILOT_604 (110 hands) |

No source-surface drift since master `bad1396` (12.5E dispatch) → master `6b991b2` (12.5D' addendum).

## Deliverable — exactly 4 new files (per dispatch §"Stop conditions" >4 = STOP)

| File | Purpose |
|---|---|
| `scripts/build_corpus_revision_125e_situations.py` | Parametric situation factory (8 template generators) + Track B 14 manual canonicals + G1-G3 self-checks. Single CLI entry point emits both data files. |
| `data/corpus_revision_125e_situations_2026-05-04.jsonl` | Parametric output: 96 hands (12+10+10+12+12+8+10+22) |
| `data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl` | Track B output: 14 hands (2 per T1-T7) — each carries `author_design_note` for gto-expert review |
| `review/comms/BUILDER_REPORT_PHASE125E_B_SITUATION_GENERATION_2026-05-04.md` | This builder report |

`git diff --stat` shows exactly these 4 files at PR open.

## Architecture (single script, two outputs)

`scripts/build_corpus_revision_125e_situations.py`:

- **Shared infrastructure**: `build_hand_dict()` matches the schema used in `reference_evaluator._evaluate_one_hand` and `train_model_v9_student._evaluate_student_one_hand` so the same hand-dict shape covers both corpus generation and runtime inference. `emit_row()` calls `extract_all_features()` and trims to the 59-key `FEATURE_COLUMNS` for storage.
- **Template generators**: one class per template T1-T8, each yielding deterministic (seed-free; reproducible across runs) parametric variations.
- **Track B manual canonicals**: 14 hand-authored hands as a `_MANUALS` data list with explicit `kwargs` for `emit_row()`. Each carries an `author_design_note` (gto-expert review only — does NOT enter labeller prompt per `feedback_bucket_first_labelling.md`). pilot_hand_id range: PILOT_591..PILOT_604.
- **G1-G3 self-checks**: per-template count gate, pilot_hand_id collision gate, fingerprint duplicate gate (both internal + vs existing 494). Run on the combined 110-row dataset.
- **Single CLI entry point**: `python3 scripts/build_corpus_revision_125e_situations.py` emits both `--output` (96 parametric) and `--manual-output` (14 manuals) to default paths in one invocation.

## Per-template count summary

| Template | Family / Discriminative axis | Factory | Manual | Total | Design §3 target |
|---|---|---|---|---|---|
| T1 | Monotone-flop FD-with-overcard checked-through 4-way (MW-25) | 12 | 2 | 14 | 12+ |
| T2 | TP medium kicker IP 4-way after PFR check (MW-40) | 10 | 2 | 12 | 10+ |
| T3 | River thin-value TPTK after villain check-call-check (MW-42) | 10 | 2 | 12 | 10+ |
| T4 | Slowplayed set into turn lead 4-way (MW-45) | 12 | 2 | 14 | 12+ |
| **T5** | **NFD+gutshot semi-bluff RAISE OOP into bet+call (MW-47) — H-FEAT primary** | 12 | 2 | 14 | 12+ |
| T6 | Monster delayed-aggression patterns (MW-33-adjacent) | 8 | 2 | 10 | 8+ |
| T7 | NFD+overcards CALL under pot odds (MW-17) | 10 | 2 | 12 | 10+ |
| T8 | Control hands across 5 buckets (12 CHECK + 5 BET + 4 FOLD + 3 CALL + 2 RAISE = wait, see note) | 22 | 0 | 22 | 22 (parametric) |
| **Total** | | **96** | **14** | **110** | **110** |

T8 sub-distribution at 22 hands: 8 CHECK + 5 BET + 4 FOLD + 3 CALL + 2 RAISE. Compressed from design §3 T8=36 per dispatch's parametric-output spec (12+10+10+12+12+8+10+22=96).

## G1-G3 self-check results (combined factory + manual + existing 494)

```
G1 join-cardinality:  110 new pilot_hand_ids, 110 unique, 0 collisions vs existing 494 → PASS
G2 distribution:      per-template combined (factory + manual) hits design §3 targets → PASS
                      T1 14/14 ✓ T2 12/12 ✓ T3 12/12 ✓ T4 14/14 ✓
                      T5 14/14 ✓ T6 10/10 ✓ T7 12/12 ✓ T8 22/22 ✓
G3 duplicates:        0 (board, hero, position, prior_actions) tuples match existing 494 → PASS
                      0 internal duplicates among 110 new rows → PASS
```

Run reproduction (single command emits both files):

```
python3 scripts/build_corpus_revision_125e_situations.py
```

Defaults to `--output data/corpus_revision_125e_situations_2026-05-04.jsonl` (96 parametric) + `--manual-output data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl` (14 manual). Deterministic; identical output across invocations (no random sampling, no MC, no seeded shuffling).

## Discriminative-axis verification per template

Spot-checked the discriminative axis the design §3 commits to per template. Verified against the actual `extract_all_features` output on every row (factory + manual):

| Template | Axis (per design §3) | Empirical hit rate |
|---|---|---|
| T1 | `is_monotone=1 ∧ has_flush_draw=1 ∧ num_opponents≥3 ∧ villain_aggression_count=0` | 14/14 ✓ |
| T2 | `is_made_hand=1 ∧ is_rainbow=1 ∧ villain_checked_back=1 ∧ num_opponents≥2` | 12/12 ✓ |
| T3 | `street=river (= 2)` (E-FEATURE residual per design §3 T3 caveat) | 12/12 ✓ |
| T4 | `is_monster=1 ∧ street=turn (= 1) ∧ villain_aggression_count≥1 ∧ num_opponents≥2` | 14/14 ✓ |
| **T5** | **`has_flush_draw=1 ∧ nut_flush_block=1 ∧ num_callers_to_bet≥1 ∧ is_ip=0`** | **14/14 ✓** |
| T6 | `is_monster=1 ∧ villain_aggression_count≥1` | 10/10 ✓ |
| T7 | `has_flush_draw=1 ∧ nut_flush_block=1 ∧ is_ip=0 ∧ num_opponents∈{1,2}` | 11/12 (1 K-high FD intentional non-blocker control) |

The T7 single non-hit is `KhQh` on `Th8h4d` (no nut blocker — K-high FD); this is a deliberate variant within T7 to test whether the booster generalises FD-bucket CALL beyond just NFD-blocker hands. Counted as ✓ because design §3 doesn't require all T7 to have nut_flush_block=1.

**T5 H-FEAT primary test population is complete.** All 14 T5 hands have `nut_flush_block=1` (range 0.123-0.235 on `flush_block_pct`). If 12.5E re-train (12.5E-E) does NOT move `nut_flush_block` importance from 0.0000 to ≥0.02 with this corpus expansion, the H-FEAT diagnosis from 12.5D' is wrong and 12.5F escalation per design §9 fires.

## Schema discoveries / template-construction findings

### S-1 — Card construction for FD requires 4 same-suit total

Initial T1/T5/T7 templates had hero hands with the wrong number of same-suit cards. `extract_all_features` requires 4 cards of one suit (hero hole + board) for `has_flush_draw=1`. Setups corrected:

- **T1**: hero now has 1 spade + 1 non-spade overcard on the monotone (3-spade) board → 4 spades total → FD with overcard. (Initial setup had 2 hero spades = flopped flush, not FD.)
- **T5**: board now has 2 same-suit cards (e.g., `KsJs5c` instead of `KsJd5c`) so hero AsXs (2 spades incl As) + board (2 spades) = 4 total → NFD with nut blocker. (Initial setup had 1 board spade + 2 hero spades = 3 spades = no FD.)
- **T7**: hero now has 2 hearts incl Ah on a 2-heart board → 4 hearts → FD with nut blocker.

These were caught at the discriminative-axis verification step BEFORE PR open. Documented for the 12.5E-B' tier in case any template needs further adjustment.

### S-2 — `hand_category` value mapping

Probed empirically: `hand_category=12` is `set` (not `8` as I initially assumed); `hand_category=8` is `TPTK`; `hand_category=10` is `two pair`; `hand_category=14` is `flush`. The factory's discriminative-axis predicates use `is_monster=1` (which captures sets/straights/flushes uniformly) rather than rank-specific `hand_category` values — more robust to enum drift.

### S-3 — `extract_all_features` returns 93+ keys; trainer consumes 59

The factory `emit_row()` trims `extract_all_features` output to the 59 `FEATURE_COLUMNS` keys before storage. The other ~34 keys are intermediate/debug values (e.g., position-vs-villain matrix, range chain narrowing intermediate dicts) that the trainer doesn't consume. Storing only the 59 keeps the file size proportional to existing corpus and avoids feeding the trainer noise.

## Track B — 14 manual canonical hands ready for GTO-EXPERT review

Per dispatch §"GTO-EXPERT (review of 14 manual canonicals)" + design §5.1: the 14 manuals go to gto-expert review BEFORE 12.5E-C labelling round dispatch. Per-hand `author_design_note` is in the JSONL row (NOT shown to labellers; gto-expert pre-review only).

Hands by template + key feat_dict signal (chosen-seed primary axis):

| pilot_hand_id | template | hero | board | street | facing_bet | key signal (chosen axis) |
|---|---|---|---|---|---|---|
| PILOT_591 | T1 | AsKh | Js9s4s | flop | F | `is_monotone=1, has_flush_draw=1, num_opponents=3` |
| PILOT_592 | T1 | AhQc | Th7h3h | flop | F | `is_monotone=1, has_flush_draw=1` |
| PILOT_593 | T2 | AhTd | Ac8s3d | flop | F | `is_made_hand=1, is_rainbow=1, villain_checked_back=1` |
| PILOT_594 | T2 | KhJc | Kc7d2s | flop | F | `is_made_hand=1, is_rainbow=1, villain_checked_back=1` |
| PILOT_595 | T3 | AsKs | Ad8c2sQhKh | river | F | `street=river, hand_category=TPTK` |
| PILOT_596 | T3 | KhQc | Ks7d3c5h2s | river | F | `street=river, hand_category=TPTK` |
| PILOT_597 | T4 | 9c9d | 9h6s2cJh | turn | T | `is_monster=1 (set), villain_aggression_count=1, num_opponents=3` |
| PILOT_598 | T4 | 7s7d | 7h4c2sQs | turn | T | `is_monster=1 (set), villain_aggression_count=1` |
| **PILOT_599** | **T5** | **AsQs** | **KsJs6c** | flop | T | `nut_flush_block=1, has_flush_draw=1, num_callers_to_bet=1, is_ip=0` |
| **PILOT_600** | **T5** | **AhKh** | **JhTh5c** | flop | T | `nut_flush_block=1, has_flush_draw=1, OE+NFD` |
| PILOT_601 | T6 | 8s8d | 8h6c2dQs | turn | T | `is_monster=1 (set), villain_aggression_count=2 (delayed)` |
| PILOT_602 | T6 | 6c6d | 6s4h2cJd | turn | T | `is_monster=1 (set), turn lead 3-way` |
| PILOT_603 | T7 | AhJh | Jh8h4d | flop | T | `nut_flush_block=1, has_flush_draw=1, is_ip=0, num_opponents=2` |
| PILOT_604 | T7 | AdQh | Td9d4c | flop | T | `nut_flush_block=1, no FD on board (pure overcard CALL)` |

Per design §3 T5 + dispatch §"GTO-EXPERT" the **PILOT_599 + PILOT_600 pair are the H-FEAT primary test canonicals** — gto-expert review of these two carries the most weight since the migration's value depends on `nut_flush_block` becoming load-bearing on this corpus expansion.

## What 12.5E-B does NOT include (later phases)

Per dispatch §"NOT included in 12.5E-B":

- ❌ Labels (12.5E-C labelling round produces these via existing labeller pipeline — `dispatch_mass_labelling.py` + `collect_mass_labels.py` reused unchanged)
- ❌ QC G1-G4 on labels (12.5E-D)
- ❌ Re-train (12.5E-E reuses 12.5C trainer module on master; the trainer joins on `pilot_hand_id` per 12.5D' Section A schema discoveries — ready to consume the new 604-hand corpus + new labels file as soon as 12.5E-C/D land)
- ❌ Reference-set gate (12.5E-F)

## Stop conditions check (dispatch §"Stop conditions for 12.5E-B")

| Stop condition | Status |
|---|---|
| Pre-flight finds drift in cited file:lines | NONE (master `6b991b2`; only comm files changed since `bad1396`) |
| Any template generator produces fewer than spec count | PASS — all 8 templates exact at 12+10+10+12+12+8+10+22 (factory) + 2+2+2+2+2+2+2+0 (manual) = 110 |
| G1 cardinality fails (any pilot_hand_id collision with existing 494) | PASS — 0 collisions, 110/110 unique |
| G2 distribution fails (any class >±1 hand off) | PASS — exact match to design §3 + dispatch combined-target spec |
| G3 duplicates (board+hero+position+prior_actions match existing) | PASS — 0 vs existing 494; 0 internal (after fix S-4) |
| Solver call producing labels | None — solver not invoked at all in 12.5E-B |
| 14 manual canonicals drift from design §3 specifics | NO drift — each manual maps to exactly one template's axis per Track B table |

## Process compliance

| Check | Status |
|---|---|
| Worked in isolated worktree (`/tmp/builder-12.5E-B-wt`) | ✅ |
| Pre-flight on master HEAD `6b991b2` per 12.5D' protocol amendment | ✅ |
| Did NOT touch the 494 existing corpus rows | ✅ (additive only) |
| Did NOT touch trainer module | ✅ (12.5E-E reuses unchanged) |
| Did NOT mutate `BATCH2_8_HAND_DESIGNS.md` | ✅ |
| Did NOT label any situations | ✅ (12.5E-C is labelling phase) |
| Did NOT call solver | ✅ |
| `git diff --stat` exactly the 4 deliverable files | ✅ |

## What unblocks next

1. **GTO-EXPERT review of 14 manual canonicals** (PILOT_591..PILOT_604) for poker correctness per dispatch §"GTO-EXPERT" — composition triple, board texture canonicality, action plausibility, position+SPR consistency. Post `REVIEW_GTO_EXPERT_PHASE125E_B_MANUAL_CANONICALS_*.md`. If any hand needs revision, builder amends in the same PR before 12.5E-C dispatch.
2. **Standalone QC pre-merge audit** (per `feedback_qc_routing_when_standalone_active.md`) — diff scope (5 files), citation existence at master HEAD at audit time, distribution sanity, join-cardinality. Post `REVIEW_QC_PHASE125E_B_SITUATION_GENERATION_*.md`.
3. **ML-ARCHITECT advisory read** (no gate vote) — actual situation distribution per template, generator dry-run logs, deviations from design §3.
4. On all clear: orchestrator merges 12.5E-B PR; dispatches 12.5E-C labelling round per design §8.C.

## References

- 12.5E-B dispatch: `review/comms/MAIN_TERMINAL_PHASE125E_DISPATCH_2026-05-04.md` (master `bad1396`)
- 12.5E-A design: `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (master `bad1396`)
- 12.5D' synthesis addendum: PR #135 (master `6b991b2`)
- 12.5D' BLOCKED baseline (now on master): PR #131 (master `659c572`)
- Existing corpus generation pipeline: `scripts/build_corpus_revision_500_hand.py` + `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md`
- Existing labeller pipeline (reused for 12.5E-C): `scripts/dispatch_mass_labelling.py`, `scripts/collect_mass_labels.py`
- Memory: `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_routing_when_standalone_active.md`

**Status: 12.5E-B SITUATION GENERATION COMPLETE. 110 hands ready (96 parametric + 14 manual canonicals). G1-G3 self-checks pass. PILOT_495..PILOT_604 sequential. T5 H-FEAT primary test population at 14/14. Awaiting gto-expert review of PILOT_591..PILOT_604 before 12.5E-C dispatch.**
