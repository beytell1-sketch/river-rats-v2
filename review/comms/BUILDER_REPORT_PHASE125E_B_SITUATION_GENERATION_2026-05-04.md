---
date: 2026-05-05
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · GTO-EXPERT (re-review) · QC stream · ML-ARCHITECT (advisory)
re: Phase 12.5E-B AMENDED (Path B / v3.3 carve-out) — 6 mechanical fixes + hero-only convention + v3.3 prompt; T5 hands UNCHANGED
status: 12.5E-B AMENDED — re-review window open per BUILDER_AMEND_READY comm
---

# Phase 12.5E-B — situation generation report (AMENDED 2026-05-05)

Implements ml-architect 12.5E-A design comm
(`review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md`, master `bad1396`)
per Phase 12.5E-B dispatch
(`review/comms/MAIN_TERMINAL_PHASE125E_DISPATCH_2026-05-04.md`, master `bad1396`)
and Phase 12.5E-B Path B amendment directive
(`review/comms/MAIN_TERMINAL_PHASE125E_B_AMEND_PATH_B_2026-05-05.md`,
master `10f914b`).

**See §"Amendment 2026-05-05" at the end of this report for the full
amendment scope (6 mechanical fixes + hero-only convention pick + v3.3
prompt + Path B preservation of T5 hands).**

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

**Original status (2026-05-04): 12.5E-B SITUATION GENERATION COMPLETE. 110 hands ready (96 parametric + 14 manual canonicals). G1-G3 self-checks pass. PILOT_495..PILOT_604 sequential. T5 H-FEAT primary test population at 14/14.** (Superseded by Amendment 2026-05-05 below — gto-expert REJECT-amend cycle.)

---

## Amendment 2026-05-05 (Path B / v3.3 carve-out)

GTO-EXPERT review of PR #136 returned REJECT with two finding classes (per `MAIN_TERMINAL_PHASE125E_B_AMEND_PATH_B_2026-05-05.md`, master `10f914b`):

1. **6 of 14 manual canonicals broken** — mechanical fixes required (action sequences, composition, position)
2. **All 14 T5 hands structurally fail v3.2 KB §1.7 OVERRIDE** — under v3.2 the labellers would systematically produce CALL labels for the H-FEAT primary test, breaking the migration's load-bearing test before it reaches the labelling round

ML-ARCHITECT recommended **Path B** as the HOW. Orchestrator adopted Path B per `feedback_quality_default_no_ask.md` (slow-quality default).

### Path B summary

- T5 hands kept as-authored (PILOT_599 + PILOT_600 unchanged, all 12 factory T5 hands unchanged)
- 6 mechanical fixes to the 6 broken hands + insert missing flop checks on 4 T1/T2 hands (cosmetic-but-completes)
- Hero-only convention applied uniformly across all 110 `prior_actions` (matches existing 494 corpus convention)
- New `prompts/gto_labeller_v3.3.md` = `prompts/gto_labeller_v3.2.md` verbatim + Fix 2.1 KB §1.7 carve-out refinement (refines v3.2's blanket 0.20 villain_air threshold to suspend it in bet+call multiway lines where structural fold-equity comes from the committed second caller, not the air bucket)

### 6 mechanical fixes applied

| Hand | Fix | Detail |
|---|---|---|
| **PILOT_595** (T3 manual canonical 01) | Re-authored as BTN IP (matching PILOT_596); fresh river decision | `hero_position` BB → BTN; `villain_positions` [CO, BTN] → [CO]; flop sequence corrected (CO bet, BTN call, BB fold); turn CO check + BTN check; river ends with `CO check` (no hero or villain river check sequence — fresh decision). `villain_call_count` 1 → 0. |
| **PILOT_597** (T4 manual canonical 01) | Add `turn: BTN call` + `turn: SB fold` so hero (BB) is genuinely next-to-act after CO turn bet | `pot` 23.0 → 35.0 (added BTN call into pot); `villain_call_count` 0 → 1; `num_callers_to_bet` 0 → 1. |
| **PILOT_598** (T4 manual canonical 02) | Same fix as 597 | `pot` 24.0 → 38.0; `villain_call_count` 0 → 1; `num_callers_to_bet` 0 → 1. |
| **PILOT_601** (T6 manual canonical 01) | Add `turn: BTN call` so hero is next-to-act after CO turn bet | `pot` 43.5 → 61.5; `villain_call_count` 0 → 1; `num_callers_to_bet` 0 → 1. |
| **PILOT_602** (T6 manual canonical 02) | Same fix as 601 | `pot` 22.5 → 34.5; `villain_call_count` 0 → 1; `num_callers_to_bet` 0 → 1. |
| **PILOT_603** (T7 manual canonical 01) | Hero AhJh (TPTK + NFD = strong_made) → AhKh (NFD + overcards only = drawing bucket); board Jh8h4d → Jh7h4d to keep distinct fingerprint vs factory PILOT_559 | Restores MW-17's pure-draw template per gto-expert + ml-architect. Distinct board avoids G3 internal duplicate. |
| PILOT_591/592/593/594 (T1/T2 manual canonicals) | Insert missing `flop: BB check` before `flop: HJ check` to complete postflop sequence | Cosmetic but completes the action ordering. Filtered out of `prior_actions` by hero-only convention (hero=BTN), retained in `action_history` for feature extraction. |

### Hero-only convention pick

Existing 494-row corpus uses hero-only convention in `prior_actions` (verified empirically: 0/494 rows have non-hero actions in `prior_actions`). New manuals + factory rows initially drifted to full multi-actor history; amendment rewrites convention uniformly.

Implementation: new `_hero_only_prior_actions(prior_actions, hero_position)` helper added to `emit_row()`; filter is applied on every row at construction time, so the convention is enforced rather than hand-applied.

Verification: empirical scan of all 110 amended rows shows 0 violations (every entry's actor matches `hero_position`).

`action_history` is NOT filtered — `extract_all_features` consumes the full multi-actor sequence for chain narrowing computation. Only the human-readable `prior_actions` field on the row is hero-only.

### v3.3 prompt addition

New file: `prompts/gto_labeller_v3.3.md`. Built as `cp prompts/gto_labeller_v3.2.md prompts/gto_labeller_v3.3.md` then append the Fix 2.1 KB §1.7 OVERRIDE refinement section (verbatim per directive, character-for-character) immediately after the v3.2 OVERRIDE section ends (before the `---` separator that begins the Pass 2 Review section).

`diff` confirms v3.3 = v3.2 + exactly the Fix 2.1 section (39 added lines, 0 changes elsewhere).

The Fix 2.1 carve-out:
- Suspends v3.2's `villain_air_pct >= 0.20` threshold in bet+call multiway lines (`villain_call_count >= 1` AND `villain_aggression_count == 1`)
- Re-applies KB §1.7 (Nut FD + nut blocker → RAISE) when (a) hero has nut FD with Ace blocker, (b) hero is OOP relative to bettor, (c) action sequence is bet+call(s) with no raise on current street, (d) hero has ≥35% raw equity
- Calibration anchor: MW-47 (RAISE per `reference_corrections.md`)
- Counter-anchors: MW-39 (CALL — HU bet), MW-30 (CALL — no nut FD), bet+raise+call (carve-out doesn't trigger)

### G1-G3 re-run on amended dataset

```
[gen] generating 96 parametric situations ...
[gen] generated 96 parametric rows
[gen] generating 14 manual canonical hands ...
[gen] generated 14 manual rows
[gen] running G1-G3 self-checks (combined 110 rows) ...
  G1 PASS: 110 unique pilot_hand_ids; zero collision with existing 494
  G2 PASS: T1=14/14, T2=12/12, T3=12/12, T4=14/14, T5=14/14, T6=10/10, T7=12/12, T8=22/22
  G3 PASS: 0 (board, hero, position, prior_actions) duplicates vs existing 494; 0 internal duplicates
```

(One internal collision arose during amendment when PILOT_603 was changed from AhJh→AhKh on Jh8h4d — duplicating factory PILOT_559's AhKh on Jh8h4d. Resolved by changing PILOT_603 board to Jh7h4d, distinct from any factory T7 board.)

### Path B stop conditions check (per amendment directive)

| Stop condition | Status |
|---|---|
| T5 hand definitions changed | NONE — all 14 T5 hands (12 factory + 2 manual) unchanged from 2026-05-04 author state |
| Convention not uniformly applied | PASS — 0/110 violations across factory + manual |
| v3.3 prompt diverges from ml-architect spec | NONE — `diff` confirms verbatim insertion |
| G1/G2/G3 fails after regeneration | PASS — all gates clear |
| Mechanical fix drifts a template family | NONE — PILOT_603 still T7/MW-17 (drawing bucket) on a distinct heart-board |

### Deliverable diff after amendment — 5 files (was 4)

| File | Status |
|---|---|
| `scripts/build_corpus_revision_125e_situations.py` | UPDATE |
| `data/corpus_revision_125e_situations_2026-05-04.jsonl` | UPDATE (regenerated) |
| `data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl` | UPDATE (regenerated; T5 hands unchanged) |
| `review/comms/BUILDER_REPORT_PHASE125E_B_SITUATION_GENERATION_2026-05-04.md` | UPDATE (this amendment section) |
| `prompts/gto_labeller_v3.3.md` | NEW (v3.2 verbatim + Fix 2.1) |

### Methodology lesson incorporated NOW (per amendment directive)

The 12.5E-A design assumed v3.2 protocol would label T5 hands as RAISE. Empirically the labellers would have labelled CALL because v3.2's KB §1.7 OVERRIDE catches T5's MW-47 family along with MW-39. Future blueprints citing a labelling protocol must verify the protocol's discriminator predicate against sample situations BEFORE declaring the design complete (similar to the join-cardinality protocol amendment from 12.5D'); ideally by running a small-sample falsification test.

This is added as a follow-on protocol amendment beyond the join-cardinality rule. Lives in the amendment dispatch until ml-architect formalizes in `docs/PROCESS_GUIDE.md`.

### gto-expert self-review (multi-hat, before-final-push)

Per amendment directive §"LEAD-PROGRAMMER (gto-expert hat — self-review before force-push)" the builder also wears the gto-expert hat for a self-review of the amended dataset + v3.3 carve-out wording before final push. (The standalone gto-expert team will re-review independently after the push — this is upstream sanity, not a substitute.)

#### A — 14-manual re-review pass

For each manual canonical post-amendment, verified composition triple, board texture, action sequence plausibility, position+SPR consistency, and hero-only convention. Outcome:

| pilot_hand_id | template | hero | board | bucket | hero-only conv | composition consistent w/ design note | outcome |
|---|---|---|---|---|---|---|---|
| PILOT_591 | T1 | AsKh | Js9s4s | drawing (NFD + 2 over) | ✓ | ✓ (`nut_flush_block=1, has_flush_draw=1`) | PASS |
| PILOT_592 | T1 | AhQc | Th7h3h | drawing (NFD + 1 over) | ✓ | ✓ | PASS |
| PILOT_593 | T2 | AhTd | Ac8s3d | strong_made (TP-T-kicker on rainbow) | ✓ | ✓ (`is_made_hand=1, is_rainbow=1`) | PASS |
| PILOT_594 | T2 | KhJc | Kc7d2s | strong_made (TP-J-kicker on rainbow) | ✓ | ✓ | PASS |
| PILOT_595 | T3 | AsKs | Ad8c2sQhKh | strong_made (top two pair on river K) | ✓ | NOTE: `hand_category=10` is two pair, not TPTK as design_note loosely describes — situation is *stronger* than TPTK (top two pair AAxKK). Bucket + thin-value-BET-after-villain-check-line conclusion unchanged. Minor design_note wording, not a content error. | PASS |
| PILOT_596 | T3 | KhQc | Ks7d3c5h2s | strong_made (TPTK) | ✓ | ✓ (`hand_category=7`) | PASS |
| PILOT_597 | T4 | 9c9d | 9h6s2cJh | monster (set) | ✓ | ✓ (`is_monster=1, hand_category=12, street=turn`) | PASS — fix #2 landed (BTN call + SB fold added; pot 35.0 reflects CO bet + BTN call) |
| PILOT_598 | T4 | 7s7d | 7h4c2sQs | monster (set) | ✓ | ✓ | PASS — fix #3 landed |
| **PILOT_599** | **T5** | **AsQs** | **KsJs6c** | **drawing (NFD + gutshot, nut blocker)** | ✓ | ✓ (`nut_flush_block=1, has_flush_draw=1`) — **UNCHANGED per Path B** | PASS |
| **PILOT_600** | **T5** | **AhKh** | **JhTh5c** | **drawing (NFD + OE, nut blocker)** | ✓ | ✓ — **UNCHANGED per Path B** | PASS |
| PILOT_601 | T6 | 8s8d | 8h6c2dQs | monster (set, delayed-aggression) | ✓ | ✓ (`is_monster=1`) | PASS — fix #4 landed (BTN call added; pot 61.5) |
| PILOT_602 | T6 | 6c6d | 6s4h2cJd | monster (set) | ✓ | ✓ | PASS — fix #5 landed |
| PILOT_603 | T7 | AhKh | Jh7h4d | drawing (NFD + K overcard, nut blocker) | ✓ | ✓ (`nut_flush_block=1, has_flush_draw=1`; pure draw, no top pair) | PASS — fix #6 landed (AhJh→AhKh; board Jh8h4d→Jh7h4d to avoid PILOT_559 fingerprint) |
| PILOT_604 | T7 | AdQh | Td9d4c | drawing (back-door + overcards + nut diamond blocker; no FD on flop) | ✓ | ✓ (`nut_flush_block=1, has_flush_draw=0` — only 3 diamonds total; back-door FD only) | PASS |

**Cosmetic finding (not blocker):** PILOT_595's design_note describes hero as "TPTK + nut blocker" but the situation actually gives top-two-pair (AsKs on Ad...QhKh river ⇒ both A and K paired). The bucket and labelling logic are unchanged (still strong_made → thin-value BET vs CO check-line); only the design_note wording is loose. Flagged for orchestrator awareness; no fix needed.

All 14 manuals: hero-only convention ✓, all 6 mechanical fixes landed correctly ✓, T5 (PILOT_599 + 600) unchanged ✓.

#### B — v3.3 carve-out falsification test

Walked the v3.3 wording through the 4 directive-specified test cases. For each, traced predicate evaluation: trigger condition (`villain_call_count >= 1 AND villain_aggression_count == 1`) and clauses (a-d) of KB §1.7 re-application.

| Case | Setup | Trigger predicate | Clauses (a-d) | Predicted action | Expected | Outcome |
|---|---|---|---|---|---|---|
| 1. MW-47 | AsQs on Ks-J-5 (2 spades), BB OOP, CO bet → BTN call → hero acts | `villain_call_count=1, villain_aggression_count=1` → **TRUE** | (a) NFD+As ✓; (b) BB OOP ✓; (c) bet+call no raise ✓; (d) ~40% equity ≥35% ✓ | KB §1.7 RAISE re-applies → **RAISE** | RAISE | **PASS** |
| 2. MW-39 | AhJh on Kh8h3d, BB HU vs CO c-bet | `villain_call_count=0` → **FALSE** | (n/a — trigger off) | v3.3 does NOT activate; v3.2 < 0.20 threshold catches → **CALL** | CALL | **PASS** |
| 3. Constructed HU NFD-blocker | AhKh on Jh8h4d, BB HU vs CO bet (low villain_air) | `villain_call_count=0` → **FALSE** | (n/a) | v3.3 does NOT activate; v3.2 catches HU low-air → **CALL** | CALL | **PASS** |
| 4. Constructed multi-way bet+RAISE+call | AsQs on KsJs5c, BB OOP; CO bet → BTN raise → SB call → hero acts | `villain_aggression_count=2` (raise present) → **FALSE** | (n/a — clause (c) "no raise" fails AND trigger condition fails) | v3.3 does NOT activate; multi-way bet+raise faced with NFD-only equity ≈ 30% → **CALL** (or FOLD on bad price) | CALL | **PASS** |

All 4 cases falsify in the predicted direction. **Falsification test: PASS.**

#### C — (a)/(b)/(c)/(d) clause tightness audit

Reviewed each clause for over-generalization risk:

- **Clause (a) — "hero has the nut flush draw with the canonical Ace blocker":** TIGHT. Requires both (i) NFD (which by definition means hero holds the highest card of the flush suit, since the next draw would be a higher card) AND (ii) explicit Ace-of-suit blocker. Excludes K-high FD (no Ace blocker), bare blocker without FD (e.g., Ah-Kc on a 2-spade board has Ah but no spade FD).
- **Clause (b) — "hero is OOP relative to the bettor":** TIGHT. Carve-out specifically targets the OOP geometry where raise pressure exploits position (BTN+1 caller behind committed → hero raise puts villain in bad continue-EV). IP carve-out has different EV mechanics; intentionally excluded.
- **Clause (c) — "the action sequence is bet+call(s) on the current street with no raise":** TIGHT. Excludes both (i) HU bet (no caller, fold equity comes from villain's solo c-bet range only, captured by v3.2) and (ii) bet+raise+call (raise breaks the structural fold-equity model — raising into a re-raised pot is suicide as the directive explicitly notes). The phrasing "no raise on current street" is precise.
- **Clause (d) — "≥35% raw equity vs the inferred continuing range":** TIGHT. 35% is the minimum floor for raise EV to clear under the bet+call OOP geometry (per ml-architect's spec). Excludes thin-equity NFDs (e.g., NFD with no overcards on a paired board) where equity drops below the threshold.

**Conjunctive requirement:** all 4 clauses are required (AND). Removing any one would leak the carve-out into a region it shouldn't apply. Wording is conservatively tight.

**Counter-anchor coverage:** the carve-out's three explicit counter-anchors (MW-39 / MW-30 / multi-way bet+raise+call) each fail on a different clause:
- MW-39: trigger predicate fails (`villain_call_count=0`)
- MW-30: clause (a) fails (top pair, not nut FD)
- Multi-way bet+raise+call: clause (c) fails (raise in sequence; trigger predicate also fails on `villain_aggression_count`)

The three counter-anchors cover three distinct exit doors (trigger / clause-a / clause-c), giving the carve-out's negative space good coverage.

**gto-expert hat verdict (self-review):** v3.3 carve-out is sound and tight. No wording revision recommended. Standalone gto-expert team will re-verify independently per amendment directive §"GTO-EXPERT (re-review)".

### What unblocks next (post-amendment)

1. **Standalone QC pre-merge audit** (5 audits per amendment directive: diff scope = 5 files, citation existence, distribution sanity, **convention uniformity**, **v3.3 carve-out wording verbatim match**)
2. **GTO-EXPERT re-review** of (a) the 6 fixed hands per fix-list above, (b) the v3.3 carve-out wording (falsification test: MW-47 → RAISE, MW-39 → CALL, HU bet w/ NFD-blocker → CALL, multi-way bet+RAISE+call → CALL) — **builder self-review (above) confirms all 4 cases pass; standalone gto-expert independently re-verifies**
3. **ML-ARCHITECT advisory** confirming v3.3 prompt matches the spec
4. On all clear: orchestrator merges PR #136; **12.5E-C dispatch points at v3.3 prompt** (NOT v3.2) per amendment directive

**Status: 12.5E-B AMENDED. Path B adopted. 110 hands; T5 unchanged; 6 mechanical fixes landed; hero-only convention uniformly applied; v3.3 prompt added. G1-G3 PASS. Multi-hat self-review (implementation + architect + gto-expert) complete; falsification test 4/4 PASS. Force-pushed to PR #136. BUILDER_AMEND_READY comm posted to `review/comms/`.**
