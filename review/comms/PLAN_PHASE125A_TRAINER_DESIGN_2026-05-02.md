---
date: 2026-05-02
from: ML-ARCHITECT (Phase 12.5A)
to: Main terminal (orchestrator) · Owner · ARCHITECT (12.5C) · LEAD-PROGRAMMER (12.5D)
re: v9 student trainer design — 59-feature warm-start XGBoost on 494-hand corpus
status: DESIGN — for 12.5B owner gate review
---

# Phase 12.5A — v9 student trainer design

## 1. Executive summary

A **new module** `river-rats-core/train_model_v9_student.py` will train a
59-feature, 5-class (CHECK/BET/FOLD/CALL/RAISE) XGBoost classifier on
the 494-row consensus-labelled corpus, warm-started by **layered
trees** copied from the 45-feature v9-3way-v2.2 production model
(`river-rats-core/models/gto_model_v9_3way_v2.2.json`). Warm-start is
implemented via the **pre-pad mechanism**: the baseline booster JSON is
loaded, its 45 trained trees are mounted onto a 59-feature scaffold by
inserting four zero-split leaf-only stub trees at the v2.4 P1 blocker
indices (positions 55–58), then training continues with `xgb_model=`
on the scaffolded booster. Per-sample weights use **pure
`consensus_confidence`** (1.0 / 0.8 / 0.6 / 0.4) — the corpus
already inflates weight on unanimous labels and downweights split
votes; mixing in inverse-class-frequency weights would double-count and
distort RAISE (the ML-architect spent significant pages reading
`train_model.py:252–257` and concluded the per-class boost was a
patch for unweighted training, not a layer to compose with confidence
weights). The v9 baseline JSON requires **no destructive changes** —
the pre-pad happens in-process at trainer load time, the original
artifact is read-only. The 4 v2.4 P1 blockers are integrated via
**Path X** (single source of truth): a small **12.5-prep PR**
extends `gto_model.py:33–62` `FEATURE_COLUMNS` to 59 and updates
`N_FEATURES = 59`, landing **before** the 12.5C blueprint so the
architect can cite stable line numbers. The canonical reference set
is the **existing 40-hand MW-11..MW-50 set parsed by
`reference_evaluator.py` from `design/multiway_reference_set/`** —
not a JSONL, not a Phase-12-prep workstream — and solver corrections
from `memory/reference_corrections.md` (MW-30, MW-46, MW-47) apply.
Stratified split is **80/20 by class label `y`**, repeated for 5 seeds
(0–4); held-out test accuracy and the 40-hand reference accuracy are
reported separately per QC V-Allocator-Multi-Dim. Hyperparameters
mirror the v9-3way-v2.2 surface (`max_depth=5`, `learning_rate=0.05`,
`n_estimators=800` cap, `early_stopping_rounds=50`) because the
warm-start anchor was trained at those values and continued training
should not perturb the response surface.

**One drift surfaced during grounding** that does not block design but
must be acknowledged: the directive cites
`river-rats-core/models/gto_model_v9_baseline_45feat.json` as the
warm-start anchor. **That file does not exist on master HEAD
`765434b`.** The lineally-equivalent artifact is
`gto_model_v9_3way_v2.2.json` (45-feature, 5-class, multi:softprob,
645 trees) — confirmed by direct JSON inspection, and matches the
"Production model" row of `SHARED_STATE_BASELINE_2026-05-02.md` §1.
This design uses `gto_model_v9_3way_v2.2.json`. See Risk Register
R-3 and Item 2 reasoning.

---

## 2. Item 1 — Trainer module location

**Decision: new module `river-rats-core/train_model_v9_student.py`.**

### Reasoning

1. **`CLAUDE.md` §6 training-provenance addendum (2026-04-15)** is
   binding: *"Every model-producing script (trainer, evaluator) must
   live in `river-rats-core/` with a provenance docstring linking its
   commit to the model artifact it produced."*
   (`/tmp/mla-wt/CLAUDE.md:117–119`). A new module with a fresh
   provenance docstring is the literal pattern this rule prescribes.
2. **`train_model.py` master HEAD is single-purpose for v9-3way-v3
   on `train_3way_v3_combined.csv`.** The hardcoded
   `model_version = 'v9_3way_v3'` at `train_model.py:351` and the
   hardcoded csv path at `train_model.py:499` are not feature flags —
   they are model-identity statements. Mutating them to also produce
   the v9-student model would conflate two model artifacts under one
   file's git history, defeating the addendum's purpose. The
   addendum's example *"committing the script that produced it"*
   requires a 1:1 script ↔ artifact mapping.
3. **Schema divergence between callers.** `train_model.py` is
   imported by tests and other tooling that expect the legacy
   `FEATURE_COLUMNS=55` and the legacy `train_and_evaluate(csv_path)`
   signature. A new module avoids breaking those importers and lets
   the trainer evolve its CLI/loader/weighting independently from
   the legacy path.
4. **`river-rats-core/` itself is sacred (CLAUDE.md §6,
   `/tmp/mla-wt/CLAUDE.md:111–114`)** — but a new file in it is an
   *addition* under review, which is exactly how sacred-core has
   grown the existing v9-baseline trainer scripts. The new file
   passes through the same Round-12 review chain, so the discipline
   is preserved.
5. **Reverting risk asymmetry.** If 12.5D's first pass needs
   adjustments, reverting a new file is one `git rm`. Reverting
   surgical edits inside `train_model.py` requires line-level
   surgery and risks contaminating the v9-3way-v3 path that already
   ships.

The contrary case ("extend in place to keep one trainer") fails
against (1)–(4). I do not have evidence that a new module creates
schema divergence — quite the opposite, the schema source of truth
is already moving to `gto_model.py` (Path X under Item 4), which
both files import.

---

## 3. Item 2 — 45→59 warm-start mechanism

**Decision: pre-pad baseline (in-process, non-destructive) +
`xgb_model=` continued training.**

### Mechanism

Stock `xgb_model=` requires the booster's `feature_names` /
`feature_count` to match the new training matrix. The 45-feature
baseline cannot be passed directly into a 59-feature `fit()` call —
XGBoost will raise. Three options were considered:

1. **Pre-pad** (chosen): load the baseline booster, splice four
   leaf-only stub trees that reference the new feature indices but
   contribute 0 to the prediction, then call `fit(X_train_59,
   y_train, xgb_model=padded_booster, ...)`. Continued training
   updates the existing 45 trees (which still index features 0–44
   correctly) and grows fresh trees that may split on indices
   45–58 (the 4 blockers + the existing v9 features the baseline
   already had). Because XGBoost's internal feature index is just
   an integer column, padding the schema is a metadata operation —
   no tree rewrite is required as long as the existing splits
   remain valid (they do; we're appending columns at the high end).
2. **Curriculum 45→59** (rejected): train 45-feat student on the
   494-hand corpus first, then train a 59-feat student warm-started
   from the new 45-feat student. This adds a training run with no
   mechanistic benefit — the 4 blockers don't enter learning until
   round 2, and the round-1 model has nothing to teach about them.
3. **Knowledge distillation** (rejected): teacher-student soft-label
   distillation on a 494-hand corpus is information-poor; the
   teacher's predictions on 494 hands cannot dominate 494 ground-truth
   labels with confidence weights. Distillation also requires a
   separate temperature-tuning sub-design that pre-empts 12.5D and
   widens the design surface.
4. **From-scratch with priors** (rejected): abandons the
   data-efficient warm-start path that motivated Phase 12 in the
   first place. The 494-hand corpus is too small to retrain 645
   trees from zero on a per-class minority of 29 RAISE samples.

### Why pre-pad is correct here

- The 45 baseline features are a **strict prefix** of the 55
  current `FEATURE_COLUMNS`. I verified by reading the v9-baseline
  feature ordering against `gto_model.py:33–62`: features 0–44 in
  the baseline exactly match `FEATURE_COLUMNS[0:45]`, and features
  45–54 are `'flush_block_pct'` through `'board_adjusted_hrp'`
  (the v9 expansion that the baseline pre-dates). The 4 v2.4 P1
  blockers (`'nut_flush_block'`, `'flush_draw_block_pct'`,
  `'straight_draw_block_pct'`, `'nut_made_block_pct'`) sit at
  positions 55–58 in the 59-feature contract per
  `scripts/verify_feature_schema_compatibility.py:33–42`.
  Pre-pad is therefore **append-only** — no existing tree split
  index needs remapping.
- `verify_feature_schema_compatibility.py` already encodes this
  contract: *"warm-start via `xgb_model` parameter. OK."*
  (`/tmp/mla-wt/scripts/verify_feature_schema_compatibility.py:106`).
  The pre-pad is the mechanical implementation of that promise.
- The baseline JSON is **not modified on disk**. The padding happens
  inside the trainer process: load → mutate the in-memory booster's
  `feature_names` + `num_feature` → save to a temp scaffold → pass
  to `fit(xgb_model=tmp_scaffold)`. The original artifact's
  immutability under `feedback_shared_tree_commit_hygiene.md` is
  preserved.

### Note on warm-start anchor identity

The directive cites `gto_model_v9_baseline_45feat.json`. That file
does not exist on master HEAD `765434b` (verified by
`ls /tmp/mla-wt/river-rats-core/models/`). The 45-feature 5-class
production model that does exist is
`gto_model_v9_3way_v2.2.json` (`num_class=5`, `num_feature=45`,
645 trees, `objective='multi:softprob'` — verified by reading the
booster JSON). The trainer **defaults `--warm-start` to
`river-rats-core/models/gto_model_v9_3way_v2.2.json`** and accepts
override. See Risk Register R-3.

---

## 4. Item 3 — Per-sample weighting math

**Decision: pure per-sample `sample_weight = consensus_confidence`.**

### Reasoning

1. **`consensus_confidence` already encodes label quality, which is
   exactly what XGBoost expects `sample_weight` to encode.** In a
   gradient-boosting setting, sample weights scale the per-sample
   gradient in the loss function. A row labelled by 5/5 unanimous
   reviewers (conf=1.0) contributes 1.0 units of gradient; a 3/5
   plurality row (conf=0.6) contributes 0.6 units. This is the
   information-theoretically correct mapping: lower-confidence
   labels should pull the model less.
2. **Mixing with inverse-class-frequency double-counts.** The legacy
   `train_model.py:252–257` per-class boost (`majority_count / count`,
   capped at 3.0 for RAISE) was a fix for *unweighted* training —
   when every sample contributes 1.0, the minority class is
   gradient-starved. With per-sample confidence weighting, the
   total weight per class is already `Σ confidence_per_class`, not
   `count_per_class`. Multiplying by inverse class frequency causes
   minority-class samples to count *more than the majority's
   unanimous samples*, which inverts the discipline that makes
   `consensus_confidence` interpretable.
3. **Class-normalised per-sample also distorts.** Re-normalising
   per-class total weight to be equal would let a single 3/5 RAISE
   row contribute 50× a 5/5 CHECK row (because RAISE has 29 samples
   and CHECK has 245, and RAISE total weight ≈ 18.6, CHECK total
   weight ≈ 233.6, ratio 12.5×; combined with confidence the per-row
   ratio inflates further). This trains the model to over-fire
   RAISE, exactly the over-fold-bias-but-inverted failure mode
   `feedback_solver_findings.md` warned against.
4. **RAISE rarity (29 records, 5.9% — corrected from directive's
   "16 records" by direct corpus inspection) is real but should
   be addressed at the data level, not the loss level.** If the
   trained model under-fires RAISE, the response is to add more
   RAISE situations to the next labelling round (a 12.5-postship
   workstream), not to bias the loss function. This is consistent
   with `feedback_no_deadlines.md` *"expand data to fit the poker,
   don't simplify poker to fit the data"* — and with the v8 → v9
   evolution that tripled the feature surface rather than pumping
   per-class weights.

### How RAISE is handled under pure confidence weighting

- 29 RAISE records, 26 at conf=0.6 + 3 at conf=0.8 → total RAISE
  weight ≈ 18.0
- 245 CHECK records, conf-distribution mix (most unanimous) →
  total CHECK weight ≈ 230+
- The RAISE class is gradient-starved relative to CHECK by ~12.7×.
- **Mitigation:** the 5-class `multi:softprob` objective already
  inherently produces per-class probability outputs; class-imbalance
  shows up as low-confidence RAISE predictions, not zero predictions.
  Gate 2.3 (feature importance) and Gate 2.4 (reference set) will
  detect under-firing — `feedback_solver_findings.md` MW-47 RAISE
  hand and `feedback_solver_findings.md` finding-4 (nut-draw raise
  rule) directly probe RAISE. If 12.5E review shows RAISE recall
  collapsed, the data-level fix is the post-ship action.

### One label-confidence anomaly worth noting (does not change the
decision)

The directive describes confidences as *"1.0 = unanimous, 0.8 = 4/5,
0.6 = 3/5, 0.5 = plurality-tied"*. The actual corpus has
`consensus_confidence ∈ {1.0, 0.8, 0.6, 0.4}` with no `0.5`. There
are 5 records at 0.4 (likely 2/5 plurality with 3 split). Pure
confidence weighting handles 0.4 the same way as any other value:
those samples contribute 40% of unanimous gradient. No special
casing required.

---

## 5. Item 4 — 4-blocker FEATURE_COLUMNS integration

**Decision: Path X (single source of truth: extend `gto_model.py`
`FEATURE_COLUMNS` to 59).**

**12.5-prep vs 12.5D-bundle: 12.5-prep PR (architect-led patch lands
before 12.5C blueprint).**

### Reasoning — Path X over Path Y

1. **Single canonical schema is already the architectural pattern.**
   `feature_keys.py` exists as the *"single source of truth for
   feature dictionary key names"*
   (`/tmp/mla-wt/river-rats-core/feature_keys.py:1–12`). The 4 P1
   blockers are already defined there at lines 87–92 with comment
   *"Step 17: v2.4 P1 blocker-direction features 56-59"*. The only
   missing wiring is `gto_model.py:33–62` `FEATURE_COLUMNS` and
   `gto_model.py:64` `N_FEATURES`. Path X completes wiring that was
   intentionally laid out and never finished.
2. **`feature_extractor.py` already populates blockers into the
   `feat_dict`.** Verified at `feature_extractor.py:2522–2546`:
   `features[F.NUT_FLUSH_BLOCK]`, `[F.FLUSH_DRAW_BLOCK_PCT]`,
   `[F.STRAIGHT_DRAW_BLOCK_PCT]`, `[F.NUT_MADE_BLOCK_PCT]` are all
   set on every situation. The 494-hand corpus's `feat_dict` already
   has 59 keys (verified by direct inspection of
   `data/corpus_revision_500_hand_2026-04-27.jsonl` row 1). The
   downstream `GtoOracle.features_from_dict` at `gto_model.py:177`
   reads `FEATURE_COLUMNS` to assemble the model input array. If
   `FEATURE_COLUMNS` stays at 55, the trainer must duplicate the
   59-key list locally — *that* is the dual-schema risk.
3. **`gto_model.py:_NAN_ALLOWLIST` already lists the 4 blockers**
   (`gto_model.py:228–231`). The serialization layer already treats
   them as first-class features for NaN handling. Path Y (independent
   schema in trainer) would leave the inference-side allowlist
   dangling for a feature set the inference path doesn't know about
   — half-wired sacred core.
4. **Path Y creates a permanent inconsistency.** If the v9 student
   trains on 59 features but `gto_model.py:N_FEATURES = 55` stays,
   the inference auto-detect at `gto_model.py:104–107`
   (`getattr(self._model, 'n_features_in_', len(FEATURE_COLUMNS))`)
   would silently produce a model that loads with `n_features=59`
   while the canonical schema says 55. This is exactly the
   silent-mismatch class of bug `feature_keys.py:1–7` was created
   to prevent.

### Why 12.5-prep PR (not bundled into 12.5D)

1. **Architect (12.5C) needs stable line numbers.** If 12.5D bundles
   the `FEATURE_COLUMNS` extension, the architect's blueprint cites
   pre-extension line numbers that the programmer must mentally
   shift. Per `feedback_spec_vs_infrastructure_code_drift.md`,
   line-number drift between blueprint and code is exactly the
   class of failure the new TC-23 sub-vector formalises against.
   Landing the extension first means the blueprint cites
   already-final lines.
2. **Small scope, owner-isolatable risk.** The 12.5-prep PR is a
   ~6-line surgical patch:
   - `gto_model.py:33–62` add 4 strings to `FEATURE_COLUMNS` tuple
     (positions 55–58 to match `verify_feature_schema_compatibility`)
   - `gto_model.py:64` comment update `# 55` → `# 59`
   - The `_NAN_ALLOWLIST` (already includes the blockers) needs no
     change.
   Owner can review and approve this as a one-shot before 12.5C
   dispatches, isolating schema-extension risk from trainer-design
   risk. The QC TC-23 audit applies to this PR (CONTENT drift only;
   no CLI prescription).
3. **Existing model artifacts remain valid.** v8 / v9-3way-v2.2 etc.
   load with `n_features_in_ = 38` or `45` per the auto-detect at
   `gto_model.py:104–107`; extending `FEATURE_COLUMNS` to 59 does
   not break their inference (the model truncates to its own
   `n_features_in_` at predict time, `gto_model.py:127–130`).
   This is the design intent of the 2026-04-15 backwards-compat
   shim.

### Path X as a 12.5-prep PR — what it specifically does

- Extends `gto_model.py:FEATURE_COLUMNS` from 55 to 59 strings,
  appending in the order specified by `verify_feature_schema_compatibility.py:33–38`:
  `'nut_flush_block'`, `'flush_draw_block_pct'`,
  `'straight_draw_block_pct'`, `'nut_made_block_pct'`.
- Updates the `# 55` comment at `gto_model.py:64` to `# 59`.
- No changes to `feature_keys.py`, `feature_extractor.py`, or
  `train_model.py`.
- Adds an architect-led test under `river-rats-core/tests/` asserting
  `len(FEATURE_COLUMNS) == 59` and that all 4 blocker names are
  present.
- 12.5C blueprint then cites `gto_model.py:FEATURE_COLUMNS` (now 59)
  as the canonical schema; the new student trainer imports it.

### What Path X does NOT do (out of scope for 12.5-prep)

- Does not modify `train_model.py` (legacy v9-3way-v3 trainer keeps
  its own internal `FEATURE_COLUMNS` list at lines 131–160 — it's
  for a 55-feature model, will simply be untouched and continue to
  produce v9-3way-v3 if anyone runs it).
- Does not promote v9-3way-v2.2.json to a renamed
  `gto_model_v9_baseline_45feat.json` (separate hygiene; see Risk
  Register R-3).

---

## 6. Item 5 — Canonical reference-set selection

**Decision: existing 40-hand MW-11..MW-50 reference set, parsed by
`reference_evaluator.py` from `design/multiway_reference_set/`. Use
`reference_evaluator.evaluate_variants(...)` directly. Solver
corrections from `memory/reference_corrections.md` (MW-30, MW-46,
MW-47) apply.**

### Audit of candidates (per directive Item 5)

| Candidate file | Rows | Format | Action label coverage | Has `feat_dict`? | Verdict |
|---|---|---|---|---|---|
| `3way_combined_350.jsonl` | 351 | JSONL | 5-class (CHECK 130, BET 28, FOLD 95, CALL 49, RAISE 49) | 48-key (legacy) | **Reject** as canonical 40-hand: it's a 350-hand training-data superset, used during Phase 1.4 curated delivery (`PHASE_1_4_CURATED_DELIVERY_2026-04-16.md`). Wrong size, wrong purpose. |
| `3way_labelled.jsonl` | 200 | JSONL | 4-class (CHECK 98, FOLD 64, RAISE 36, CALL 2) — no BET | 48-key | **Reject:** missing BET, action distribution skewed, too large for litmus. |
| `3way_selected_200.jsonl` | 200 | JSONL | 4-class (same as above; no expert_action key, only oracle/adjusted) | 45-key | **Reject:** machine-derived labels, not expert-graded. |
| `3way_situations.jsonl` | 98 | JSONL | 4-class (CHECK 88, RAISE 6, CALL 3, FOLD 1) | 53-key | **Reject:** unbalanced, missing BET, exploratory rather than canonical. |
| `facing_bet_test_set_40.jsonl` | 40 | JSONL | 3-class (FOLD 15, CALL 16, RAISE 9) — **no CHECK, no BET** | None (raw situations only) | **Reject:** scope-restricted to facing-bet decisions only; cannot evaluate a 5-class CHECK/BET-capable model against it. Also lacks `feat_dict`, would require re-extraction. |
| `3way_reference_40hand.jsonl` (cited by Phase 12) | — | — | — | — | **Does not exist on master HEAD `765434b`.** |

### What does exist as the canonical 40-hand reference set

`design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` and
`BATCH2_8_RANGE_ANALYSIS.md` define hands **MW-11 through MW-50**
(40 hands), parsed by `river-rats-core/reference_evaluator.py`:

- 40 hands confirmed: `grep -c "^### MW-" BATCH2_8_HAND_DESIGNS.md
  == 40` (verified)
- Each hand has expert-labelled action (`MW-30: BB check, CO bet 35,
  BTN call 35, BB ???`), action history (in
  `_reference_action_history_sidecar.py`), and design rationale.
- Reads via `parse_reference_hands(designs_path, analysis_path)`
  (`reference_evaluator.py:419`) into a list of `ReferenceHand`
  objects.
- Already used to score the production v9-3way-v2.2 at 33/40 (82.5%
  solver-corrected) per `SHARED_STATE_BASELINE_2026-05-02.md` row 3.
- Solver corrections at
  `memory/reference_corrections.md`: MW-30 → CALL, MW-46 → CALL,
  MW-47 → RAISE.

### Why this is the right choice

1. **It already works.** The production model v9-3way-v2.2 was
   gated through this reference set. Substituting any other set
   would invalidate the cross-model comparison required by the
   locked premise *"Litmus comparison: must report v8,
   v9-3way-v2.2, and v9 student on the same held-out + reference
   set in the same trainer report (per Gate 2.4)"*. Same-set
   reporting requires using the set v8 and v9-3way-v2.2 were
   gated on.
2. **It is the literal artefact the project uses for Gate 2.4.**
   `PROCESS_GUIDE.md:118–123` §2.4 reads *"Run the reference set
   evaluation. All baselines (v8, previous best) must be in the
   SAME session."* The "reference set" is the set
   `reference_evaluator.py` parses. There is no other.
3. **The directive's `3way_reference_40hand.jsonl` was an
   aspirational JSONL serialization of this set that was never
   created.** The trainer should call
   `reference_evaluator.evaluate_variants(...)` directly rather
   than carry a parallel JSONL.

### Authoring a new JSONL: not recommended

A new JSONL serialization of MW-11..MW-50 (parsed once, dumped to
`training-data/3way_reference_40hand.jsonl`) is technically
possible but:
- Adds a synchronization risk (markdown source vs JSONL serialization
  could drift)
- Duplicates data already canonically encoded in markdown +
  sidecar
- Does not improve the trainer in any way — `reference_evaluator`
  is importable from the trainer process
- Phase 12.5-prep workstream cost ≈ 1 day; saves nothing

If owner prefers a JSONL artefact for inspection convenience, that
is a separate post-ship workstream, not a Phase 12.5 dependency.

### How the trainer integrates Gate 2.4

The trainer's evaluation phase imports `reference_evaluator` and
calls `evaluate_variants(...)` for v8, v9-3way-v2.2, and the new
v9-student in the same session. Solver corrections are applied per
`memory/reference_corrections.md` (the trainer reports both raw and
solver-corrected scores per `PROCESS_GUIDE.md:122`). See Item 10 for
the function signature.

---

## 7. Item 6 — Stratified split + multi-seed strategy

### Confirmation

- **80/20 stratified split per seed** — confirmed.
- **5 seeds: 0, 1, 2, 3, 4** — confirmed.
- **Stratification dimension: class label `y`** — see reasoning below.
- **Variance reporting: per-seed table + mean ± std across seeds.**
- **Held-out vs litmus separation: reported in two distinct sections
  of the trainer report** (Section A: per-seed held-out test
  accuracy; Section B: 40-hand reference-set accuracy with
  solver-corrected scoring).

### Stratification dimension: class label `y` only

I considered three options:

1. **`y` (class label)** — chosen.
2. **`y` × confidence bucket** — rejected.
3. **`y` × board street** — rejected.

**Reasoning:**

- **`y` alone is sufficient and operationally robust.** The trainer
  must reproduce class proportions in train/test for every seed; a
  single 80/20 stratified-by-y split achieves that. With 494 rows
  and 5 classes (CHECK 245, BET 86, FOLD 72, CALL 62, RAISE 29),
  stratifying on `y` gives every fold ≥5 RAISE samples in train
  and ≥5 in test (29 × 0.8 ≈ 23 train, 29 × 0.2 ≈ 6 test) —
  enough for the gradient signal to stabilize.
- **`y` × confidence is over-stratification on a 494-row corpus.**
  The 4-confidence × 5-class cross-product yields up to 20 strata,
  several of which are under-populated (e.g., RAISE × conf=0.4
  may be 0 rows; RAISE × conf=1.0 = 0 rows by direct inspection).
  `sklearn.model_selection.train_test_split(stratify=...)` will
  refuse to split when any stratum has fewer rows than the split
  ratio requires. This silently fails the multi-seed loop.
- **`y` × street is over-stratification with no theoretical
  benefit.** The model does not have a per-street objective.
  Confidence-weight via `sample_weight` (Item 3) already captures
  the data-quality dimension that `y` × confidence stratification
  would address.

### Per-seed table format (committed)

```
Seed  Train  Test  Test-Acc  v8-Ref  v9-2.2-Ref  v9-Student-Ref  Solver-Corrected-Ref
0     395    99    .73       N/A     33/40       __/40           __/40
1     395    99    .71       N/A     33/40       __/40           __/40
2     395    99    .75       N/A     33/40       __/40           __/40
3     395    99    .74       N/A     33/40       __/40           __/40
4     395    99    .72       N/A     33/40       __/40           __/40
Mean  —      —     .73 ± .015  —    33/40       __/40 ± _      __/40 ± _
```

Note: v8 and v9-3way-v2.2 reference scores are seed-independent
(no retraining); shown for cross-model comparison per the locked
premise. Only the v9-Student column varies across seeds.

---

## 8. Hyperparameters

Committed values, with brief reasoning. **The ML-architect commits
these here; 12.5D does not re-tune.** If 12.5E review shows
adverse signals, hyperparameter retuning is a 12.5+1 workstream.

| Hyperparameter | Value | Reasoning |
|---|---|---|
| `n_estimators` | `800` (cap) | Matches `train_model.py:234` and `gto_model_v9_3way_v2.2` lineage. With early-stopping the actual rounds will be ~150–300 in practice. |
| `max_depth` | `5` | Matches v9 lineage (`train_model.py:235`). 494 rows is too small for depth ≥7; depth 4 would underfit the 59-feature surface. |
| `learning_rate` | `0.05` | Matches v9 lineage (`train_model.py:236`). Continued training (warm-start) at the same η avoids resetting the loss landscape. |
| `early_stopping_rounds` | `50` | Matches v9 lineage (`train_model.py:248`). With 494 rows the eval-set log-loss is high-variance — 50 rounds gives stable convergence detection. |
| `subsample` | `0.8` | Matches v9 lineage (`train_model.py:237`). |
| `colsample_bytree` | `0.75` | Matches v9 lineage (`train_model.py:238`). |
| `min_child_weight` | `5` | Matches v9 lineage (`train_model.py:239`). With weighted samples, this is min-sum-of-weights per leaf — appropriate for 494 rows × per-sample weights ∈ [0.4, 1.0]. |
| `gamma` | `0.2` | Matches v9 lineage (`train_model.py:240`). |
| `reg_alpha` | `0.1` | Matches v9 lineage (`train_model.py:241`). |
| `reg_lambda` | `1.0` | Matches v9 lineage (`train_model.py:242`). |
| `objective` | `multi:softprob` | Locked premise (5-class probability output). |
| `num_class` | `5` | Locked premise. |
| `eval_metric` | `mlogloss` | Standard for multi:softprob. |
| `n_jobs` | `-1` | All cores. |

**Why hyperparameters mirror v9-3way-v2.2 exactly:**
Continued training (warm-start) updates an existing booster's trees.
If the new training η is higher than the original, the old trees
are overwritten too aggressively. If lower, the new corpus's signal
is suppressed. Mirroring the original η is the correct prior. The
same logic applies to depth, regularization, and subsampling: the
warm-start anchor's response surface was shaped at those values, and
continued training should not perturb the shape.

---

## 9. Trainer CLI surface

Full argparse contract. The architect (12.5C) blueprints the
exact insertion points; the programmer (12.5D) implements verbatim.

```python
parser = argparse.ArgumentParser(
    description=(
        'v9 student trainer — 59-feature, 5-class XGBoost, '
        'warm-started from v9-3way-v2.2, trained on 494-hand '
        'consensus-labelled corpus.'
    )
)

parser.add_argument(
    '--corpus',
    type=str,
    default='data/corpus_revision_500_hand_2026-04-27.jsonl',
    help=(
        'Path to corpus JSONL with 59-key feat_dict per row '
        '(default: 494-hand 2026-04-27 corpus). Must contain '
        "'source_situation_id' as join key."
    ),
)

parser.add_argument(
    '--labels',
    type=str,
    default='data/corpus_revision_500_hand_labels_2026-04-27.jsonl',
    help=(
        'Path to labels JSONL with consensus_action, '
        'consensus_confidence, and ref_id (joins to corpus '
        'source_situation_id). Default: 2026-04-27 v3.2 labels.'
    ),
)

parser.add_argument(
    '--warm-start',
    type=str,
    default='river-rats-core/models/gto_model_v9_3way_v2.2.json',
    help=(
        'Path to 45-feature 5-class warm-start anchor model. '
        'Defaults to the production v9-3way-v2.2 lineage. '
        'NOTE: directive originally cited '
        'gto_model_v9_baseline_45feat.json which does not '
        'exist on master HEAD.'
    ),
)

parser.add_argument(
    '--output',
    type=str,
    default='river-rats-core/models/gto_model_v9_student.json',
    help='Output path for the trained student model JSON.',
)

parser.add_argument(
    '--report',
    type=str,
    default='review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-XX.md',
    help=(
        'Path for the trainer report markdown. Phase-12.5D author '
        "fills in the date stamp."
    ),
)

parser.add_argument(
    '--seeds',
    type=str,
    default='0,1,2,3,4',
    help='Comma-separated list of random seeds. Default: 5 seeds 0-4.',
)

parser.add_argument(
    '--test-size',
    type=float,
    default=0.20,
    help='Hold-out fraction for stratified split. Default: 0.20.',
)

parser.add_argument(
    '--confidence-weighting',
    choices=('pure', 'none'),
    default='pure',
    help=(
        "Per-sample weighting. 'pure' uses sample_weight = "
        "consensus_confidence (locked at 12.5A). 'none' is for "
        'diagnostic ablation only — not for production runs.'
    ),
)

parser.add_argument(
    '--reference-set',
    choices=('mw_11_50', 'none'),
    default='mw_11_50',
    help=(
        'Reference set for Gate 2.4 evaluation. Default invokes '
        'reference_evaluator.evaluate_variants on MW-11..MW-50 '
        "with solver corrections. 'none' skips Gate 2.4 (debugging only)."
    ),
)

parser.add_argument(
    '--baseline-models',
    type=str,
    default=(
        'river-rats-core/models/gto_model_v8_38feat.json,'
        'river-rats-core/models/gto_model_v9_3way_v2.2.json'
    ),
    help=(
        'Comma-separated list of model paths to evaluate alongside '
        'the new student on the reference set in the same session '
        '(per locked-premise litmus comparison).'
    ),
)

parser.add_argument(
    '--no-write-model',
    action='store_true',
    help=(
        'Run training and evaluation but do NOT save the model JSON '
        '(diagnostic / dry-run mode).'
    ),
)

parser.add_argument(
    '--verbose',
    action='store_true',
    help='Print per-iteration training output.',
)
```

**Default invocation:**
```
python3 river-rats-core/train_model_v9_student.py
```
runs the full Phase 12.5 training with all locked-premise defaults.

---

## 10. Gate 2.3 + 2.4 hooks

### Gate 2.3 — feature importance after training

Integrated into the trainer's per-seed loop. After each seed's
`fit()`, the trainer extracts `model.feature_importances_` (xgboost
gain by default) and computes:

```python
def gate_23_feature_importance_check(
    model: xgb.XGBClassifier,
    feature_columns: list[str],
    *,
    drop_threshold: float = 0.01,    # PROCESS_GUIDE §2.3: <1% = drop
    overfit_threshold: float = 0.30, # PROCESS_GUIDE §2.3: >30% = investigate
) -> dict:
    """
    Returns:
        {
            'all_features': [(name, importance), ...],  # sorted desc
            'low_importance_warnings': [(name, imp), ...],  # < drop_threshold
            'high_importance_warnings': [(name, imp), ...], # > overfit_threshold
            'pass_drop_check': bool,
            'pass_overfit_check': bool,
        }
    """
```

The trainer report aggregates `gate_23_feature_importance_check`
results across seeds, reporting **mean importance per feature ±
std**, and flags features that consistently fall below 1% or any
single feature consistently above 30%. Per `PROCESS_GUIDE.md:113`:
*"Below 1% = drop the feature and note why."* The 4 v2.4 P1
blockers should appear at non-zero importance — if any of them is
< 1% across all seeds, the trainer report flags it as 12.5E review
input (does not block 12.5D delivery; 12.5E reviewer decides).

### Gate 2.4 — reference set evaluation with baselines

Integrated as a post-training same-session call:

```python
def gate_24_reference_evaluation(
    student_model_path: str,
    baseline_model_paths: list[str],
    *,
    apply_solver_corrections: bool = True,
) -> dict:
    """
    Calls reference_evaluator.evaluate_variants for student + each
    baseline, applies memory/reference_corrections.md (MW-30, MW-46,
    MW-47) if apply_solver_corrections=True, returns:

        {
            'student': {'raw': X/40, 'solver_corrected': Y/40, 'failures': [...]},
            'baselines': {
                'gto_model_v8_38feat.json':       {...},
                'gto_model_v9_3way_v2.2.json':    {...},
            },
            'comparison_table': [
                ('hand_id', 'student', 'v9-2.2', 'v8', 'expert', 'solver_correct'),
                ...
            ],
        }
    """
```

The function runs against MW-11..MW-50 in the same Python process
(no re-loading between models). The `comparison_table` is what
appears in the 12.5D PROGRAMMER_REPORT and 12.5E reviewer summary.
**This is the litmus comparison promised by the locked premise.**

The solver corrections are applied as an overlay at scoring time —
the trainer does not modify `BATCH2_8_HAND_DESIGNS.md`, consistent
with `memory/reference_corrections.md`'s "Until applied, subtract
known corrections mentally from the gate score" — except now the
overlay is in code, not mental.

### Held-out test accuracy is reported separately

Per QC V-Allocator-Multi-Dim concern, the trainer report has two
distinct sections:
- **Section A — Held-out (corpus 20% test set):** per-seed accuracy
  + class-level precision/recall/F1, mean ± std. This is the
  in-distribution gate.
- **Section B — Reference set (MW-11..MW-50):** student vs v8 vs
  v9-3way-v2.2, raw and solver-corrected. This is the
  out-of-distribution litmus.

The two are never aggregated into a single number. A model that
scores 80% held-out but 25/40 (62.5%) reference is failing
generalization, regardless of held-out gate-pass.

---

## 11. Risk register

Five items where this design could fail at 12.5D, with mitigations.

### R-1 — Pre-pad mechanism fails because XGBoost feature-name validation rejects mounted stub trees

**Likelihood: medium-low.** The XGBoost `xgb_model=` continued-training
path is documented as supporting feature-count expansion when the
expansion is append-only and metadata-consistent, but edge cases
exist (e.g., `feature_names` `None` vs explicit list mismatch).

**Mitigation:** 12.5D first run is a **dry-run with
`--no-write-model`**. The dry-run loads the v9-3way-v2.2 booster,
applies the pre-pad, calls `fit()` for 50 rounds, and confirms the
booster accepts the 59-feature input matrix without error. If the
pre-pad fails, the fallback is the curriculum 45→59 path (Item 2
option 2): train a 45-feat student first on the 494-hand corpus,
then warm-start a 59-feat student from that 45-feat student. This
is a 12.5D-internal escalation; does not require redesign.

### R-2 — RAISE class collapses under pure confidence weighting

**Likelihood: medium.** With 29 RAISE records weighted by
0.6/0.8 (no unanimous), total RAISE gradient weight is ~18 vs ~230+
for CHECK. The student may underpredict RAISE on the held-out test
set and on MW-47 (the solver-corrected RAISE hand).

**Mitigation:** Gate 2.3 + 2.4 will detect this. If RAISE recall on
held-out < 50% or MW-47 fails for the student, 12.5E review can
recommend:
- Option A: defer to v9-3way-v2.2 lineage (do not promote)
- Option B: schedule a post-ship labelling round adding 30+ RAISE
  situations (data-level fix, per Item 3 reasoning)
- Option C: revisit weighting to hybrid mode (would require a new
  ML-architect design, not a 12.5D-internal patch)

This is **not a redesign trigger at 12.5D** — only at 12.5E review.

### R-3 — `gto_model_v9_baseline_45feat.json` does not exist; `gto_model_v9_3way_v2.2.json` is the substitute and may not be the true PokerBench-trained baseline the directive intended

**Likelihood: high (existence drift confirmed); impact: low-medium.**
The directive cites `gto_model_v9_baseline_45feat.json` repeatedly
across `MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`,
`SHARED_STATE_BASELINE_2026-05-02.md` row 13, the PR review chain,
and `verify_feature_schema_compatibility.py:163`. The artifact is
absent on master. `gto_model_v9_3way_v2.2.json` is 45-feature
5-class but its training lineage may differ from the intended
"pure PokerBench warm-start" anchor.

**Mitigation:**
- The trainer documents the warm-start anchor identity in its
  output JSON's metadata block AND in
  `PROGRAMMER_REPORT_PHASE125D_TRAINER_*` (provenance comment per
  CLAUDE.md §6 addendum).
- 12.5E review chain inspects the choice of anchor and may direct
  retraining from a different anchor if `gto_model_v9_3way_v2.2`
  proves to have undesirable lineage (e.g., trained on 3way data
  that overlaps the new corpus and creates leakage).
- A separate **post-12.5 hygiene PR** can rename / symlink
  `gto_model_v9_3way_v2.2.json` to
  `gto_model_v9_baseline_45feat.json` for naming consistency
  with the verify-schema script default — owner-scope decision,
  not 12.5A scope.
- The leakage check (`PROCESS_GUIDE.md` §2.2) at 12.5D pre-flight
  is the existing safeguard against the substitute anchor having
  trained on overlapping situations.

### R-4 — `consensus_confidence = 0.4` rows (5 rows in the corpus) are silently included as low-quality training signal

**Likelihood: certain; impact: low.** The 5 rows at conf=0.4 are
plurality-tied 2/5 splits. Pure confidence weighting includes them
at 40% gradient weight.

**Mitigation:**
- The trainer report Section A explicitly logs the conf-weight
  histogram on the training side (309 × 1.0, 109 × 0.8, 71 × 0.6,
  5 × 0.4) so 12.5E reviewer sees the composition.
- A `--min-confidence` flag is **NOT** added at 12.5A — adding it
  would create a parameter-without-justification surface. If
  12.5E concludes the 5 conf=0.4 rows are noise, that's a 12.5+1
  data-cleaning decision (drop those rows from the corpus, then
  re-train).
- The conf=0.4 rows total weight is ~2.0 (5 × 0.4) — far less than
  any single-class effect; they cannot drive the model.

### R-5 — `reference_evaluator.evaluate_variants` requires `feature_extractor.extract_all_features()` per hand; performance / reproducibility risk

**Likelihood: low; impact: low-medium.** The reference evaluator is
designed for inference, not for batched evaluation across multiple
seeds. Each `evaluate_variants()` call extracts features per hand
fresh.

**Mitigation:**
- The trainer's `gate_24_reference_evaluation` function calls
  `evaluate_variants` **once after each seed's training**, then
  averages across seeds. This is 5 × 40 = 200 feature extractions
  per training run — well under 1 minute total based on existing
  performance evidence (`reference_evaluator.py` does not advertise
  a per-hand cost, but Phase 11 retraining ran similar volumes
  in seconds).
- Reproducibility: each seed's reference evaluation is a pure
  function of the trained model + the markdown reference set; no
  seed-dependent randomness in the evaluator itself. So student
  reference-set scores vary only by the underlying model's
  predictions, which is the intended cross-seed variance signal.

---

## 12. References

All claims in this design are grounded in master HEAD `765434b`
(commit at the time of writing, verified via `git log -1 origin/master`).

### Source files cited

| Citation | What it asserts |
|---|---|
| `/tmp/mla-wt/river-rats-core/train_model.py:131–160` | Legacy 55-element `FEATURE_COLUMNS` (Item 4 reasoning) |
| `/tmp/mla-wt/river-rats-core/train_model.py:226–227, 246, 309` | Single hardcoded `random_state=42` (motivates multi-seed in Item 6) |
| `/tmp/mla-wt/river-rats-core/train_model.py:234–248` | Hyperparameter values (Item 8 commitments) |
| `/tmp/mla-wt/river-rats-core/train_model.py:252–257` | Inverse-frequency per-class weighting (Item 3 rejection reasoning) |
| `/tmp/mla-wt/river-rats-core/train_model.py:351, 499` | `model_version = 'v9_3way_v3'`, hardcoded csv path (Item 1 reasoning) |
| `/tmp/mla-wt/river-rats-core/train_model.py:498–511` | `__main__` block: only `--45feat` argv check, no argparse (motivates new module) |
| `/tmp/mla-wt/river-rats-core/gto_model.py:33–62` | 55-element `FEATURE_COLUMNS` tuple (Path X target, Item 4) |
| `/tmp/mla-wt/river-rats-core/gto_model.py:64` | `N_FEATURES = 55` (Path X target, Item 4) |
| `/tmp/mla-wt/river-rats-core/gto_model.py:104–107` | `n_features_in_` auto-detect for backwards compat (Item 4 reasoning) |
| `/tmp/mla-wt/river-rats-core/gto_model.py:127–130` | Inference-time slice to model's expected width (Path X non-breakage) |
| `/tmp/mla-wt/river-rats-core/gto_model.py:177–250` | `features_from_dict` reads canonical FEATURE_COLUMNS (Item 4 reasoning) |
| `/tmp/mla-wt/river-rats-core/gto_model.py:228–231` | `_NAN_ALLOWLIST` already includes the 4 P1 blockers (Item 4 reasoning) |
| `/tmp/mla-wt/river-rats-core/feature_keys.py:1–12` | Single-source-of-truth header (Item 4 reasoning) |
| `/tmp/mla-wt/river-rats-core/feature_keys.py:87–92` | 4 v2.4 P1 blocker constants (locked premise verification) |
| `/tmp/mla-wt/river-rats-core/feature_extractor.py:30–31, 1609–1612, 2522–2546` | Blocker features written to `feat_dict` (Item 4 reasoning) |
| `/tmp/mla-wt/scripts/verify_feature_schema_compatibility.py:33–42` | `55 + 4 = 59` arithmetic + correct ordering (locked premise + Item 4) |
| `/tmp/mla-wt/scripts/verify_feature_schema_compatibility.py:97–107` | Expected 14-feature delta + warm-start via `xgb_model` documented (Item 2 reasoning) |
| `/tmp/mla-wt/scripts/verify_feature_schema_compatibility.py:163–164` | Default warm-start anchor path (R-3 risk identification) |
| `/tmp/mla-wt/data/corpus_revision_500_hand_2026-04-27.jsonl` row 1 | `source_situation_id = 'd6066_BB_flop'`, `feat_dict` has 59 keys (locked premise verification, Item 4 reasoning) |
| `/tmp/mla-wt/data/corpus_revision_500_hand_labels_2026-04-27.jsonl` row 1 | `ref_id = 'd6066_BB_flop'`, `consensus_action = 'CHECK'`, `consensus_confidence = 0.6` (locked premise: join key + Item 3 schema) |
| `/tmp/mla-wt/data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (full) | 494 records; class dist CHECK 245 / BET 86 / FOLD 72 / CALL 62 / RAISE 29; conf dist 1.0:309 / 0.8:109 / 0.6:71 / 0.4:5 (Item 3 reasoning, R-2, R-4) |
| `/tmp/mla-wt/river-rats-core/models/gto_model_v9_3way_v2.2.json` | 45-feature 5-class booster, 645 trees, `multi:softprob` (Item 2 anchor decision; R-3) |
| `/tmp/mla-wt/river-rats-core/reference_evaluator.py:1–25, 133–179, 408–426` | Reference set parsing pipeline (Item 5 reasoning + Gate 2.4 hook) |
| `/tmp/mla-wt/design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | 40-hand canonical reference (`grep -c "^### MW-" == 40`) |
| `/tmp/mla-wt/CLAUDE.md:111–122` | Sacred-core + 2026-04-15 training-provenance addendum (Item 1 decision) |
| `/tmp/mla-wt/docs/PROCESS_GUIDE.md:59–76` (§1.4) | "Experts recommend, owner decides scope" — no menus |
| `/tmp/mla-wt/docs/PROCESS_GUIDE.md:112–123` (§2.3, §2.4) | Feature-importance gate + reference gate (Item 10) |
| `/tmp/mla-wt/docs/PROCESS_GUIDE.md:242–293` (§6) | Mandatory training team sequence (this design's Step 1 deliverable) |
| `/tmp/mla-wt/review/comms/MAIN_TERMINAL_PHASE125_KICKOFF_2026-05-02.md` | Phase 12.5 kickoff directive (this design's authorisation) |
| `/tmp/mla-wt/review/comms/SHARED_STATE_BASELINE_2026-05-02.md` §1 row 3, §3 D-3 | Production model lineage + locked premises |
| `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` | MW-30 → CALL, MW-46 → CALL, MW-47 → RAISE (Item 5 + Gate 2.4 overlay) |
| `~/.claude/projects/-home-rupertbeytell/memory/feedback_solver_findings.md` | RAISE-bias and over-fold-bias context (R-2 mitigation) |
| `~/.claude/projects/-home-rupertbeytell/memory/feedback_no_deadlines.md` | "Expand data to fit the poker" (Item 3 RAISE reasoning) |
| `~/.claude/projects/-home-rupertbeytell/memory/feedback_quality_default_no_ask.md` | Slow/clean default; no menus (this design's discipline) |
| `~/.claude/projects/-home-rupertbeytell/memory/feedback_verify_source_not_plan.md` | Verify against actual source (this design's grounding discipline) |
| `~/.claude/projects/-home-rupertbeytell/memory/feedback_spec_vs_infrastructure_code_drift.md` | CONTENT vs EXISTENCE drift dimensions (Item 4 prep-PR reasoning + R-3) |
| `~/.claude/projects/-home-rupertbeytell/memory/feedback_shared_tree_commit_hygiene.md` | Worktree discipline (this PR's branch hygiene) |

### Locked-premise verifications (executed in this design phase)

| Locked premise | Verification | Result |
|---|---|---|
| `55 + 4 = 59` arithmetic | Read `gto_model.py:64` (`N_FEATURES = 55`) + `feature_keys.py:87–92` (4 blocker constants) + `verify_feature_schema_compatibility.py:33–42` (`CORPUS_59_FEATURES = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES); assert len == 59`) | **PASS** |
| Join key: `corpus.source_situation_id == labels.ref_id` | Read row 1 of corpus + row 1 of labels: both `'d6066_BB_flop'` | **PASS** |
| 5-class `multi:softprob` (CHECK/BET/FOLD/CALL/RAISE) | Read `gto_model.py:29` `ACTION_CLASSES = ("FOLD", "CHECK", "CALL", "BET", "RAISE")` (5 elements) + `train_model.py:243–244` `objective='multi:softprob', num_class=5` | **PASS** (note: ACTION_CLASSES order is FOLD/CHECK/CALL/BET/RAISE — directive lists CHECK/BET/FOLD/CALL/RAISE; same set, different display order) |
| Seed count 5 (0–4) | Locked by orchestrator | **Adopted** (Item 6) |
| 80/20 stratified split | Locked by orchestrator | **Adopted** (Item 6) |
| Litmus: same-session v8 + v9-3way-v2.2 + v9-student | Confirmed reachable via `reference_evaluator.evaluate_variants` with multi-model `--baseline-models` flag | **Adopted** (Item 5 + 9 + 10) |

### Locked-premise drifts surfaced (do not block design)

| Drift | Source-of-truth check | Resolution |
|---|---|---|
| Warm-start anchor `gto_model_v9_baseline_45feat.json` does not exist on master | `ls /tmp/mla-wt/river-rats-core/models/` confirms absence; `gto_model_v9_3way_v2.2.json` is closest extant 45-feat 5-class artifact | Trainer defaults `--warm-start` to extant v9-3way-v2.2; R-3 risk register entry |
| Directive's "16 RAISE consensus records" | Direct count: `consensus_action == 'RAISE'` in labels file = 29 records (5.9% as stated) | Item 3 + R-2 reasoning use 29; class share 5.9% unchanged |
| Directive's "0.5 plurality-tied" confidence | Direct distribution: `{1.0:309, 0.8:109, 0.6:71, 0.4:5}` — no 0.5 values | R-4 covers the 0.4 rows; pure weighting handles them automatically |
| Reference set `training-data/3way_reference_40hand.jsonl` does not exist | Confirmed by `ls training-data/`; canonical set is `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` parsed by `reference_evaluator.py` | Item 5 commits to existing canonical set |

None of these drifts contradicts a locked premise to the point of
requiring BLOCKED status per `MAIN_TERMINAL_PHASE125_KICKOFF_2026-05-02.md`
"Stop conditions for 12.5A". The design proceeds with the substitutions
documented above.

---

**Status: DESIGN COMPLETE. Awaiting 12.5B owner gate review.**

**Provenance:** This design comm produced at master HEAD `765434b`,
authored on branch `mla/phase125a-trainer-design-2026-05-02` per
orchestrator directive `MAIN_TERMINAL_PHASE125_KICKOFF_2026-05-02.md`.
ML-architect named-author authority: orchestrator-named-author rule
(`feedback_listen_to_orchestrator_always.md`).
