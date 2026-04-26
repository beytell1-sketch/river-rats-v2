---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed) · QC stream
re: V-X2 lookup CONFIRMED zero existing v2.3 calibration hands have usable partial-fold structured data; commissioning Build D — 5-hand synthetic partial-fold MW fixture file for Phase A.5 preflight assertion
status: BUILD D DIRECTIVE — queued after Build C v1.0.1 ships; pilot dispatch resume now contingent on (1) Build C v1.0.1 + (2) Build D + (3) Phase A.5 spec edit
---

# Build D Directive — 5-Hand Partial-Fold MW Fixture File

## Background — V-X2 lookup result

Per `V_X2_PARTIAL_FOLD_LOOKUP_2026-04-26.md` (orchestrator-dispatched
agent, completed 18:36 SAST):

**Zero of 12 v2.3 calibration hands** (`GROUP_D_REVERSAL_HANDS` ∪
`GTO_REVERSAL_HANDS`) carry usable partial-fold structured data:

- 9 d-prefixed hands: `prior_actions` is hero-only (no villain
  actions; zero "fold" tokens across entire 401-record canonical pool)
- MW-30/33/50: no JSONL records; live as prose in
  `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`. Prose
  narrates villain folds but is unstructured (parsed via
  `_parse_action_history_prose()` for label loading, not consumable
  by `_villain_pos_raw` selection logic)

**Conclusion:** existing constants point at the wrong test surface
— they exercise the "live 2-villain selection" path, not the
"live-vs-folded discrimination" path Phase A.5 is meant to cover.

**Cleaner path:** purpose-built 5-hand synthetic fixture file. The
alternative (retrofitting prose on MW-30/33/50 + schema migration on
the prose-parser/loader) tangles Phase A.5 with an MW ingestion-path
refactor — larger surface area for no benefit.

## Build D scope

**File to create:** `data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl`
(or builder's preferred location; surface in PR description)

**Branch:** `stage4-pre-dispatch/phase-a5-partial-fold-fixtures`

**5 hands**, each constructed specifically to exercise `_villain_pos_raw`
live-vs-folded discrimination:

For each hand, the JSONL record must include:
- `situation_id`: `phase_a5_pf_001` ... `phase_a5_pf_005`
- `prior_actions`: explicit list with at least one `<position>: fold`
  entry from a villain (e.g. `["preflop: SB raise", "preflop: CO call",
  "preflop: BTN fold", "flop: SB check", "flop: CO check"]`)
- `villain_positions`: list of LIVE villains only (i.e. positions
  whose action ≠ fold; Phase A.5 expects `_villain_pos_raw` to select
  from this set, NOT from folded positions)
- `num_opponents`: count of live villains (matches
  `len(villain_positions)`)
- `hero_position`: standard position string
- `hero_cards`: representative 2-card hand
- `board_cards`: street-appropriate (flop=3, turn=4, river=5)
- `street`: 'flop' | 'turn' | 'river' (postflop only — preflop
  doesn't have the same partial-fold discrimination relevance)
- Standard feature fields (will be re-extracted at fixture-load time
  per Build C v1.0.1 pattern, OR pre-computed via
  `feature_extractor.py`)

### Diversity coverage (recommended)

Spread the 5 hands across:
- **Street:** flop=2, turn=2, river=1 (or similar mix)
- **Pre-fold opp count:** 4-way preflop → 3-way postflop (1 fold);
  5-way → 3-way (2 folds); 4-way → 2-way (2 folds)
- **Position of folded villain:** different positions across the 5
  (BTN/CO/HJ/SB/UTG); avoid same-position-fold across all 5
- **Live villain composition:** mix of "early position(s) live, late
  folded" + "late position(s) live, early folded" + 2-villains-live +
  1-villain-live cases

This diversity ensures Phase A.5 catches `_villain_pos_raw` bugs that
might only fire on specific position configurations.

### Disjointness verification

Per Stage 6 §"Non-overlap verification" same as Build C:
- Disjoint from Stage 6 50-hand holdout (hash
  `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`)
- Disjoint from v2.3 calibration manifest
- Disjoint from pilot 100 corpus (Build C output)
- `(sorted(hero), sorted(board))` fingerprint matching; **0
  fingerprint matches required**

Since these are synthetic fixtures (constructed, not sampled), the
disjointness is structural — but verify regardless.

### Hash-lock

SHA256 over the JSONL bytes; record in sidecar
`data/phase_a5_partial_fold_fixtures_2026-04-26.lock.json`

### Documentation in fixture frontmatter

Each fixture record should include a brief comment field documenting
the partial-fold scenario it tests, so future readers (and the Pilot
Orchestrator at Phase A.5 runtime) understand the test rationale.

## Workflow

Standard per-batch protocol:

1. Builder picks up Build D **AFTER** Build C v1.0.1 (PR #41) merges
   (serial sequence preserves shared-tree commit hygiene)
2. Branch `stage4-pre-dispatch/phase-a5-partial-fold-fixtures`
3. Build the 5-hand fixture JSONL
4. PR + dual/triple-reviewer audit
5. Reviewer dispatch: gto-expert-flavour OR ml-architect-flavour
   (corpus structure correctness + position-coverage diversity)
6. QC pre-merge audit (V-D1...V-D3 vectors expected; QC will likely
   scope per-fixture validity + cross-fixture diversity)
7. Merge after triple-reviewer convergent APPROVE

**Estimated effort:** ~30-45 min build + ~30-45 min review = ~1-1.5h
total

## Phase A.5 spec edit (orchestrator-side, after Build D)

After Build D ships, I'll write a small spec addendum to
`STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 §"Phase A.5":

> "PRE-DISPATCH PREREQUISITES row #X: Phase A.5 fixture source =
> `data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl` (Build D
> output, hash-locked). Pilot Orchestrator loads these 5 fixtures as
> Phase A.5 test cases for `_villain_pos_raw` live-vs-folded
> discrimination assertion."

This spec edit is small (~5-10 min) and orchestrator-owned. It lands
in a follow-up commit after Build D merges.

## Cross-build consistency precedent

Per Build B + Build C v1.0.1 NIT-carryforward pattern, Build D should
include a `nit_carryforward_from_build_c` block (or similar) noting
the corpus-construction conventions inherited from Build C v1.0.1
(SEED-driven determinism, hash-lock, disjointness verification
methodology) and adapt them to the 5-hand synthetic-fixture scope.

## Pilot dispatch resume — updated dependency list

Pilot dispatch resume now contingent on:
1. ✅ Build A — SEALED at 2ea67d0
2. ✅ Build B — SEALED at 3241413
3. 🔥 Build C v1.0.1 (PR #41) — ACTIVE; ETA ~30-45 min
4. 🔥 Build D (this directive) — QUEUED post-v1.0.1; ETA ~1-1.5h
5. 🔥 Phase A.5 spec edit — orchestrator-owned; ETA ~5-10 min
   post-Build-D
6. PRE-DISPATCH gate re-check
7. Phase A.1-A7 preflight begins

**Total estimated time to pilot dispatch resume:** ~2-3h from now
(18:36 SAST → ~20:30-21:30 SAST).

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 35 | Build A | ✅ SEALED | Logic builder |
| 36 | Build B | ✅ SEALED | Logic builder |
| 37 | Build C v1.0 (PR #39) | ⏸️ HELD — superseded by v1.0.1 | Logic builder |
| 40 | Build C v1.0.1 (V-C13 fix-forward) | 🔥 ACTIVE — ~30-45 min | Logic builder |
| 41 | V-X2 spec edit (Phase A.5 fixture source) | ⏳ QUEUED post-Build-D | Orchestrator |
| 42 | Build D — 5-hand partial-fold MW fixtures | 🔥 QUEUED post-Build-C-v1.0.1 | Logic builder |

## Action

**Logic builder:**
1. Continue Build C v1.0.1 fix-forward (PR #41 expected ~30-45 min)
2. After v1.0.1 merges, pick up Build D per directive above
3. Standing per-batch protocol (PR + dual/triple-reviewer + merge)
4. Surface `BUILDER_BUILDS_ABCD_COMPLETE_*.md` after Build D ships
   (final builder signal before pilot dispatch resumes)

**Orchestrator (me):**
1. Build D directive shipped + V-X2 lookup result bundled (this commit)
2. Watch for PR #41 (Build C v1.0.1) drop
3. Dispatch ml-architect / gto-expert reviewer at PR #41 open
4. After v1.0.1 merges: ack + signal Build D start
5. Watch for Build D PR drop (~30-45 min from v1.0.1 merge)
6. Dispatch reviewer at Build D PR open
7. After Build D merges: write Phase A.5 spec edit + push
8. Re-issue pilot dispatch directive (Phase A.1-A7 preflight resumes)

**QC stream:**
- Continue Layer 1+2 mode for PR #41 (Build C v1.0.1) audit
- After v1.0.1: prepare V-D1...V-D3 vectors for Build D PR audit
- TC-15 multi-expert offer standing (recommended for Build D
  per-fixture validity check)
- Same Path B bundle pattern

**Owner:**
- V-X2 lookup confirmed: existing v2.3 constants don't have
  partial-fold structured data; Build D synthetic fixtures is the
  cleanest path
- Build C v1.0.1 + Build D + Phase A.5 spec edit ≈ 2-3h to pilot
  dispatch resume
- All 4 builds + spec edit unblock the pilot

## References

- V-X2 lookup: `review/comms/V_X2_PARTIAL_FOLD_LOOKUP_2026-04-26.md`
- PR #39 decision: `MAIN_TERMINAL_PR39_DECISION_FIX_FORWARD_VC13_2026-04-26.md` (master `75d9136`)
- Phase A.5 spec text: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 §"Phase A.5"
- Stage 6 hash-lock pattern: `65cfbf26...`
- Build C v1.0 disjointness method: see PR #39 stratification report

**Status: BUILD D DIRECTIVE issued. QUEUED post-Build-C-v1.0.1.
Pilot dispatch resume contingent on v1.0.1 + Build D + Phase A.5
spec edit.**
