---
date: 2026-04-21
from: Architecture reviewer
to: Orchestrator (Stage 3.5 review panel)
re: Architecture pass on BUILDER_V24_STAGE35_BLUEPRINT (b1a9a91)
verdict: APPROVE_WITH_FIXES
---

# ARCHITECTURE REVIEW — Stage 3.5 blueprint b1a9a91

VERDICT: **APPROVE_WITH_FIXES**

## CRITICAL findings (must fix before code edits)

- **Caller list for HIGH #5 breaking change is INCOMPLETE.** Blueprint
  §5 lists `feature_extractor.py:503, 617, 805, 828, 1193` plus
  internal sites. Grep finds 9 more call sites that must also tuple-
  unpack or the import will crash at startup:
  - `river-rats-core/feature_extractor.py:1669` (deleted by CRIT #1 —
    but only if CRIT #1 lands BEFORE HIGH #5; blueprint sequences
    HIGH #5 first → this site must be updated in HIGH #5 commit and
    re-deleted in CRIT #1 commit)
  - `river-rats-core/explain_hand.py:264, 329` (2 sites, both inside
    `narrow_to_betting_range(...)` calls — not mentioned anywhere in
    blueprint)
  - `river-rats-core/coaching/feature_extractor.py:503, 617, 805,
    828, 1137` (5 sites — duplicate-file churn that §2.3 row 9 only
    flags for CRITICAL #2 staleness, not for HIGH #5 tuple surgery)
  - `river-rats-core/coaching/explain_hand.py:264, 329` (2 more)
  - `river-rats-core/range_narrowing.py:875, 885` (self-test fixtures)
  Total: **14 callers**, not 5. If blueprint is executed as-written
  the coaching/ files will ImportError on next load.

- **Stale `MODEL_COLUMNS` in `extract_features_parallel.py:29–41`
  lists 38 features, but `FEATURE_COLUMNS` in `feature_extractor.py:
  1012-1056` is 54 features.** Blueprint §2.2 tells the builder to
  edit `MODEL_COLUMNS` as though it is the canonical v2.4 schema.
  Either (a) this file is dead and should be removed as a pre-req,
  or (b) it is live and has silently been writing a 38-feature CSV
  since v9 shipped — flag for owner before any CRITICAL #2 edit
  lands.

## HIGH findings (must fix before ship)

- **`docs/training-data-schema.md` does NOT exist.** Blueprint §2.3
  conditionally flags this ("document if it exists; flag if it
  doesn't"). This is the flag. Adding `_action_history_present`,
  `_surviving_weight`, `_chain_steps`, `_villain_folded` to CSV is
  a schema bump — there needs to be *a* document of record. Not a
  blocker for the code edits, but the audit trail needs at minimum
  a CHANGELOG-style entry in `review/` before Stage 4 re-label.

- **NaN propagation is safe at inference but LOSSY at CSV round-
  trip.** `gto_model.predict` calls `XGBClassifier.predict_proba`,
  which handles NaN via XGBoost's native missing-value branch — no
  crash. `features_from_dict` at `gto_model.py:196-215` enforces
  int/float/bool dtype; `float('nan')` passes. BUT
  `extract_features_parallel.py:78` casts `float(feat[col])` for
  CSV — a NaN cell writes literal `nan` which most readers (pandas)
  re-load as NaN, but custom audit scripts that do
  `float(row[col])` can handle it. Risk: SHAP explainer
  (TreeExplainer) treats NaN as the missing-value path; SHAP values
  on folded-villain blocker features will concentrate on the
  missing-branch contribution — semantically correct but audit
  tooling must know. **Recommend: builder add a unit test
  `test_predict_proba_accepts_nan_blocker_features` in the corpus
  commit.**

## MEDIUM findings (consider)

- §6 HIGH #5 → HIGH #3 → CRIT #1 → HIGH #4 → CRIT #2 order: correct
  in principle (mass-threading first unblocks verification for
  every downstream MUST). But HIGH #3's pre-filter is inserted
  BEFORE the action loop, while HIGH #5 rewrites action-loop call
  signatures. Conflict surface is narrow (different line ranges)
  but the commits should explicitly rebase against each other, not
  be authored from the BEFORE blocks of this blueprint after the
  first commit lands. Blueprint BEFORE blocks go stale after commit 1.

- `_STAGE35_WEIGHT_FLOOR_PCT = 0.05` under mass semantics is STRICTLY
  MORE PERMISSIVE than under count semantics (mass-0.05 means ≥5%
  of probability surviving, which can happen with just 1-2 hands
  concentrated; count-0.05 of a 200-hand range is 10 hands).
  Tightening to 0.02 under mass is defensible — but corpus doesn't
  have calibration cases for this. Defer tuning post-ship is OK.

## Answers to assigned questions

**Q1:** **Metadata-field approach APPROVED.** Re-running the chain
via a second function call doubles the work (chain normalizes
through 2-3 narrow_* calls, each O(combos-in-range)) and invites
divergence at the first refactor. Carrying `_villain_range_narrowed`
on the features dict is clean IF and only if:
  (a) the field is never written to CSV (confirmed — `FEATURE_COLUMNS`
      and `MODEL_COLUMNS` both use explicit column lists; a dict value
      can't leak)
  (b) the field is never read by a non-extraction consumer — add
      an assertion `assert '_villain_range_narrowed' not in csv_row`
      at the end of `process_chunk`.

**Q4:** **Env var for MVP APPROVED.** `STAGE4_STRICT_ACTION_HISTORY`
is the right choice for Stage 3.5 scope discipline. Reasons:
  - Training pipelines (`extract_features_parallel.py`,
    `extract_incremental.py`, `gauntlet_v5_37feat.py`) invoke
    `extract_all_features(hand)` with no other knobs — adding a
    `strict=...` kwarg requires changing 3 signatures + the dozen
    call sites in tests and tooling. Env var is one line per binary.
  - Live-play (`game_state_bridge.py`) never sets the env var, so
    production is unaffected.
  - Parameterise for Stage 5 once the ground-truth path is decided.
  Nit: use `os.getenv` once at module load, not per-call — the
  per-call `os.environ.get` in the blueprint (§2.1) burns a syscall
  per hand.

**Q10:** **Breaking return type APPROVED**, conditional on the
expanded caller list (Critical finding above). Reasons:
  - Clean single-API is worth the 14-site mechanical edit.
  - Adding `narrow_to_betting_range_with_mass` leaves a permanent
    fork where callers disagree about whether mass matters — v2.5
    gets harder, not easier.
  - The 14-site edit is mechanical (`x = f(...)` → `x, _ = f(...)`)
    and greppable.
  **BUT: the coaching/ duplicate files must be updated too or
  blueprint STOPs on the ImportError. Add coaching/ to the explicit
  touch list in the HIGH #5 commit.**

**Q11:** **Ship at 5% APPROVED, but add a dedicated corpus case
to calibrate.** Current `_STAGE35_WEIGHT_FLOOR_PCT = 0.05` was a
count proxy and is strictly more permissive under mass. Tightening
pre-ship risks masking the actual fix in HIGH #5 behind a threshold
re-calibration debate. Queue a single pytest case
`test_mass_floor_distinguishes_count_from_mass` that asserts the
direction (mass < count when range concentrates) and document that
0.01–0.02 is the likely post-ship tune.

**Q13:** **Promote to CSV for Stage 4 audit APPROVED, keep OUT of
model feature vector.** Rationale:
  - Stage 4 re-label uses per-row filters (`_action_history_present
    == True`, `_villain_folded == False`) — cannot do that without
    CSV columns.
  - Adding them to the model feature vector would change the 54-
    feature contract — post-training-only columns (audit cols) are
    the right pattern. `train_model.py:131-160 FEATURE_COLUMNS` is
    the authoritative list; the CSV can have additional cols with
    no effect on training.
  - `_villain_range_narrowed` stays OUT of CSV (too wide; not a
    scalar). §10 table already correct.
  Concrete: add `_action_history_present`, `_surviving_weight`,
  `_chain_steps` (string-repr), `_villain_folded` (int 0/1) as
  audit cols; keep `_villain_range_narrowed` in-process only.

**Q14:** **(B) Defer to v2.5 APPROVED** — with one required
mitigation. Reasons:
  - Equity path is Monte Carlo 2000 trials/hand; chain-narrowing
    the villain range BEFORE MC sampling changes `raw_equity`,
    `equity_vs_range`, `better_hand_pct`, `worse_hand_pct`,
    `equity_margin` — the core 5 equity features that every
    model uses. That is a training-distribution shift much larger
    than blocker features (which only affect v2.4 P1 features
    56-59 and teaching SHAP).
  - Stage 3.5 scope is SHIP_WITH_REFACTOR and blueprint's
    reconciliation was explicit about "blocker features bypass"
    as CRITICAL #1. The reconciliation's "all villain-derived
    features inherit" language is aspirational; CRIT #1's concrete
    fix-point was Step 12 + Step 17.
  - v2.5 ticket
    `review/comms/TICKET_V25_EQUITY_CHAIN_NARROWING.md` (name TBD)
    should be created as part of this Stage 3.5 ship.
  **Required mitigation:** Add a single audit column
  `_equity_path_unchained` (int 1) to the CSV for every Stage 4
  re-label row. When v2.5 lands, the re-audit can compare
  pre/post across both feature families in one pass. Zero-cost
  now, saves a re-label later.

## HEAD drift check

**PASS.** Verified BEFORE blocks against HEAD `12cb5d4`:
- `feature_extractor.py:1116-1272` matches blueprint §1 BEFORE
- `feature_extractor.py:1651-1754` matches blueprint §1 Step 12 + 17
- `feature_extractor.py:1169-1195` matches blueprint §4 FOLD block
- `feature_extractor.py:500-505, 605-617, 790-806, 823-829` all
  match blueprint §11 (the 4 additional §11 sites are real)
- `range_narrowing.py:434-636` narrow_* functions match blueprint §5
- `range_narrowing.py:695-843` `narrow_by_action_history` matches
  blueprint §3 + §5 BEFORE (including the 5% floor at 579 and the
  count-based `len(current_range) < 3` at 820)

## Caller-list completeness for HIGH #5

**MISSING** (see Critical finding): 14 callers total, not 5.
Specifically flagged:
- `explain_hand.py:264, 329`
- `coaching/feature_extractor.py:503, 617, 805, 828, 1137`
- `coaching/explain_hand.py:264, 329`
- `range_narrowing.py:875, 885` (self-test at module bottom)

Blueprint must be amended to include coaching/ in the HIGH #5
commit OR the coaching/ duplicate files must be retired before
HIGH #5 lands (and both options need orchestrator sign-off).

## NaN propagation through model

**SAFE at inference, LOSSY with audit tooling.**
- XGBoost: NaN handled natively (missing-value branch). No crash.
- `features_from_dict` at `gto_model.py:196-215`: NaN passes
  `isinstance(v, (int, float))` — no rejection. Confirmed safe.
- SHAP TreeExplainer: treats NaN as missing-value path; feature-
  importance attributions will distribute along that branch. Not
  a bug but teaching pipeline consumers should be aware.
- CSV round-trip: `float('nan')` → literal `nan` string → pandas
  NaN on load. Audit scripts that do `float(cell)` also work
  (Python's `float('nan')` accepts that string).
- **Risk zone:** `train_model.py:183` does `float(row[col]) for
  col in FEATURE_COLUMNS` — would accept NaN, but XGBoost training
  on NaN labels in feature cols is fine (not label NaN, feature
  NaN). Confirmed safe.

## Other architectural concerns

- §11 finding surfaced DURING this architect pass is a red flag
  that reconciliation was scoped too narrowly. If framing (A) had
  been taken, the reconciliation's "10 villain-derived features"
  count is actually >15. Builder's recommendation to defer is
  sound but future reconciliations should explicitly enumerate
  by feature NAME not by narrative.

- `_villain_range_narrowed` as a dict on the feature dict is a
  300-2000 byte object held in memory per hand-extraction. For a
  500k-hand CSV extract at 4 workers, worst-case 8GB — but the
  field is local to one hand's dict and garbage-collected when
  the dict is consumed for CSV write. Not a risk.

- `extract_features_parallel.py` is stale (38 features in
  `MODEL_COLUMNS`; 54 features is current). Blueprint §2.2 tells
  the builder to edit it as though it's the current schema.
  **This file's status needs owner review BEFORE Stage 4 re-label
  runs anywhere.** Not in blueprint scope but it's a landmine.

## Summary for orchestrator

Blueprint is structurally sound. Three issues need fixing before
code edits:
1. HIGH #5 caller list must include coaching/ + explain_hand.py
   (14 sites total).
2. `extract_features_parallel.py` staleness needs owner decision —
   retire the file OR bump to 54-feature schema FIRST.
3. `docs/training-data-schema.md` is missing — create minimum
   audit record before Stage 4 re-label.

Once those land, the 5 MUSTs + corpus + re-audits ship order is
correct and the breaking signature change is defensible.

Architecture-level: APPROVE_WITH_FIXES. No rework needed on the
MUSTs themselves.
