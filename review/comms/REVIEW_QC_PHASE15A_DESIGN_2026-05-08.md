---
date: 2026-05-09
from: River Rats QC (standalone stream)
to: Main terminal (orchestrator) · Owner · LEAD-PROGRAMMER (architect-hat)
re: PR #307 — Phase 1.5-A unified-59-surface design memo (architect-hat; design only) — pre-merge milestone audit
verdict: PASS-WITH-FINDINGS
severity_summary: 0 BLOCKER · 1 SHOULD_FIX · 1 NIT
audit_type: pre-merge milestone (Phase 1.5 workstream design lock; 11-item expanded-scope)
qc_branch: qc/pr307-phase15a-design-review-2026-05-09
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR307_2026-05-08.md (master `832d6d1`, PR #309)
target_pr_head: 6164f14a6a98c3ec09ace3d0c624da6c558eb519
master_at_audit: 9c3b9ae
---

# QC pre-merge audit — PR #307 (Phase 1.5-A design memo)

## Result

**PASS-WITH-FINDINGS** (0 BLOCKER · **1 SHOULD_FIX** · 1 NIT). 41st solo cycle.

The memo is a thorough, single-committed-path design lock for the unified-59-surface workstream covering all 5 dispatch design areas, 7 falsifiable predictions, and 3 genuine owner-scope items. All 8 methodology rules are explicitly addressed. All pilot-first binding gates are present.

The single SHOULD_FIX is a **TC-23 EXISTENCE drift on §1.2** that propagates into §4.2 / §4.5 / §4.6 framing: 2 cited model artifacts attested as present at master HEAD have **never** been committed to this repo. The substantive design path is unaffected; the fix is paragraph-level correction of attestation + lineage framing + close-hand baseline methodology. Architect should resolve before 1.5-D.1 fires (a sub-phase that depends on the cited baseline).

## 11-item expanded-scope walkthrough

### Item 1 — Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) ✓

PR diff: 2 in-repo files (710 additions / 0 deletions).

| File | Operation | Lines |
|---|---|---|
| `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` | CREATE | +614 |
| `review/comms/BUILDER_REPORT_PHASE15A_2026-05-08.md` | CREATE | +96 |

`grep -E '^(river-rats-core/|prompts/|training-data/|data/|scripts/|design/|docs/|.*\.py$|.*\.csv$|.*\.jsonl$|.*\.json$)'` against `git diff master...pr307-tmp --name-only` returns **0 matches**. No source/prompt/data/model/script/design/docs edits. Owner-scope perimeter held.

### Item 2 — All 5 design areas covered as committed paths ✓

All 5 areas committed without open technical questions:

- §1 (59-surface canonical): full enumeration of 59 features by index + axis-of-targeting + chosen-seed importance; 2 J-B drops named with file:line refs.
- §2 (drop-2-J-B migration): re-extract committed (§2.1 reasoning); bit-equality verification command (§2.3); output artifact spec (§2.4); invariant-tests scope adjudication (§2.5).
- §3 (3-way verification at 59): 5-seed pre-pad warm-start committed (§3.3); PASS/STOP/HALT decision matrix (§3.4); 1-seed smoke pilot (§3.5).
- §4 (HU re-train cascade): 30-hand 6-axis HU reference set (§4.2); 5-labeller v3.4 + Sonnet→Opus tier-up (§4.3); ~750-situation HU corpus (§4.4); from-scratch HU retrain (§4.5); 28/30 ship gate (§4.6); 5-stage decomposition (§4.7).
- §5 (cost/time forecast): per-sub-phase $$/wall-clock/binding-pilot-gate/HALT table (§5.1); critical path (§5.2); off-ramps (§5.3).

Owner-scope items in §7 are flagged AS owner-scope (not technical punts). See Item 10.

### Item 3 — TC-23 EXISTENCE grep-loop on cited file:function paths

Verified at master HEAD `9c3b9ae` (forward-binding from dispatch's `5863f13`; same source content for these paths):

**GREEN (23 of 25 paths):**

- `river-rats-core/feature_extractor.py` (FEATURE_COLUMNS at line 1569; J-B at 1618-1619; `compute_nut_blocker_overcard_count` at 2136; `compute_bet_call_multiway_oop_raise_pressure_index` at 2174; call sites at 2645-2663) ✓
- `river-rats-core/feature_keys.py` (J-B keys present in declared block) ✓
- `river-rats-core/train_model_v9_student.py` (61-asserts + `_N_FEATURES_STUDENT = 61` at line 127; `_HYPERPARAMETERS` at 137-152; `is_git_tracked` at 196; `prepad_baseline_booster` at 409) ✓
- `river-rats-core/gto_model.py` (FEATURE_COLUMNS at 33; `N_FEATURES = 55` at 64; auto-detect comment at 104) ✓
- `river-rats-core/coaching/gto_model.py` (FEATURE_COLUMNS at 33) ✓
- `river-rats-core/oracle_router.py` (HU slot at line 34; legacy fallback at line 41 — but see Item 3 RED below) ✓
- `river-rats-core/models/gto_model_v9_3way_v2.2.json` ✓
- `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json` ✓
- `data/corpus_combined_988_2026-05-07.jsonl` ✓
- `data/corpus_combined_988_labels_2026-05-07.jsonl` ✓
- `scripts/assemble_125k_c_e_988.py` ✓
- `scripts/assemble_125i_d_788.py` ✓
- `scripts/generate_lever_c_situations.py` ✓
- `scripts/build_corpus_revision_125i_mw40_verif_situations.py` ✓
- `docs/PROCESS_GUIDE.md` ✓
- `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` ✓
- `prompts/gto_labeller_v3.4.md` ✓
- `training-data/tag_vocabulary.json` ✓
- `river-rats-core/calibration_exam.py` ✓
- `river-rats-core/coaching/spot_classifier.py` ✓
- `river-rats-core/tests/test_features_125j.py` ✓
- `river-rats-core/tests/test_train_model_v9_student.py` ✓
- `river-rats-core/extract_features_parallel.py` ✓

**RED (2 of 25 paths):**

- `river-rats-core/models/gto_model_v8_hu.json` — **NOT EXTANT at master HEAD; never committed in any branch (`git log --all --oneline -- <path>` returns empty).**
- `river-rats-core/models/gto_model_v8_38feat.json` — **NOT EXTANT at master HEAD; never committed in any branch.**

The §1.2 attestation lists both files as "exists" + "exists (legacy)". Both are materially incorrect. See **SHOULD_FIX-1** below.

### Item 4 — Pilot-first binding gates per `feedback_pilot_first_for_long_jobs.md` ✓

All 5 long-batch sub-phases have committed pilot+full split with binding gate language:

| Sub-phase | Pilot | Full | Binding gate (HALT condition) |
|---|---|---|---|
| §3.5 (3-way 59 retrain) | 1-seed smoke | 5-seed run | smoke crash OR within 5pts of median 12.5K-C-E |
| §4.2 (HU ref set design) | 5 hands (HU-1 axis) | 25 hands (HU-2..HU-6) | inter-labeller agreement < 80% OR Opus tier-up disagrees |
| §4.3 (HU labelling) | 5 hands | 25 hands | consensus rate < 80% |
| §4.4 (HU corpus assembly) | 50 situations | 700 situations | consensus < 80% OR solver agreement < 90% |
| §4.5 (HU model retrain) | 1-seed smoke | 5-seed full | smoke score > 5pts below v8-HU on reference |

Sonnet → Opus tier-up sub-rule explicitly committed in §4.3 (Sonnet 5-labeller consensus → Opus cross-check on non-unanimous-Sonnet sample → if disagreement > 10%, full Opus re-label of disagreeing hands).

### Item 5 — Methodology rule cross-check (8 rules) ✓

All 8 cited methodology rules explicitly addressed:

| Rule | Memo location | Verdict |
|---|---|---|
| `feedback_solver_aligned_sizing.md` | §4.2 (flop 25/66, turn 33/75, river 33/75/150 explicitly adopted) | ✓ |
| `feedback_solver_vs_expert_labels.md` | §4.3 ("solver verifies disagreements and informs research; solver output is NEVER used as a training label") | ✓ |
| `feedback_bucket_first_labelling.md` | §4.3 ("NO equity thresholds in the labelling prompt; thresholds in `coaching/spot_classifier.py`") | ✓ |
| `feedback_terminology_raise_vs_bet.md` | §4.2 (raise/bet/open definitions verbatim adopted in spot specs) | ✓ |
| `feedback_attention_flags_when_features_change.md` | §1.3 inventory + §1.3.2 documents the 12.5J-B attention-layer gap | ✓ |
| `feedback_failure_direction_classification.md` | §3.4 (under-aggress / over-aggress / class-collapse format committed for both 1.5-C and 1.5-D.4 reports) | ✓ |
| `feedback_preflop_geometry_vs_postflop_composition.md` | §4.2 ("Hand strength composition follows TP+/draws/air ... NOT preflop range buckets") | ✓ |
| `feedback_close_hand_selection.md` | §4.2 ("3 of 5 hands per axis are CLOSE per … model uncertainty on v8-HU-38 + poker difficulty") — **see SHOULD_FIX-1 cascade** | ✓ (caveat) |

### Item 6 — TC-X-DISPATCH-PREDICTION-VERIFICATION ≥3 falsifiable (7 expected) ✓

7 falsifiable predictions registered in §6 (P1-P7); exceeds dispatch's ≥3 requirement. Each prediction names a concrete observable that could fail. See Item 11 for per-prediction falsifiability detail.

### Item 7 — TC-X-OWNER-SCOPE-DISCIPLINE (21st formal use) ✓

Builder report §"Negative scope (mandatory)" explicitly enumerates 6 negatives, all held against PR diff:

1. No source / data / model / prompt edits ✓ (diff is 2 docs only)
2. No execution of feature drop, corpus re-extract, retrain, HU labelling ✓
3. No modification of `feature_extractor.py` / `feature_keys.py` / any river-rats-core source ✓
4. No modification of v3.x prompts / BATCH2 / 988-corpus / model files / 40-hand reference set ✓
5. No execution of D5 ✓
6. No "open technical questions" in the memo ✓ (genuine owner-scope items in §7 flagged AS owner-scope)

3 owner-scope items in §7 are genuine trade-offs (HU corpus 750 vs 1500 size; Phase 1.5 ship boundary; Phase 2 D5 entry). See Item 10.

### Item 8 — Per-design-area dispatch-compliance ✓

Each of the 5 dispatch-required per-area requirements is met:

| Dispatch §" Memo scope" requirement | Memo location | Verdict |
|---|---|---|
| Area 1 — architect names every file path (no hand-waving) | §1.1 + §1.3 file:line refs | ✓ (with §1.2 RED caveat from Item 3) |
| Area 2 — determinism verification command | §2.3 bash script + bit-equality `diff` invocation | ✓ |
| Area 3 — warm-start strategy committed | §3.3 pre-pad warm-start (single committed path with reasoning vs alternatives) | ✓ |
| Area 4 — HU-on-59 ship-gate parity metric committed | §4.6 28/30 (single committed path with reasoning vs PokerBench alternative) | ✓ |
| Area 5 — Phase 1.5-B/C/D/E sub-phase decomposition | §5.1 per-sub-phase table + §5.2 critical path | ✓ |

### Item 9 — Single-committed-path scan ✓

`grep -nE 'TBD|tbd|open question|either … or|Option A vs|Option B'` against the memo body returns:

- "Reasoning vs the dispatch's posed alternatives" appears 3 times (§3.3, §4.5, §4.6) — each is the architect's commitment-with-reasoning pattern, not an open question. Each names the dispatch's options + commits to one + states why. Matches `feedback_quality_default_no_ask.md`.
- §1.3.3 has 2 parenthetical "(architect identifies exact line in 1.5-B)" + "(architect-hat in 1.5-B identifies the exact closing line; precommitment: function body ends at the return statement following the body in the file as it exists at master `e66e2e6`)" — these are committed-actions with execution-time line-number resolution, not open questions. The architect commits to "delete this function body"; the only deferred element is the closing line number (resolvable mechanically when the file is opened). Acceptable.
- §2.5 ends with "If QC reads this differently, the architect will adjust before merge" — a cross-check provision, not a punt. Acceptable.
- §5.1 estimates labelled "rough" / "estimate" — appropriate per `feedback_no_deadlines.md`.

No open technical questions. Genuine owner-scope items in §7 are explicitly bucketed.

### Item 10 — 3 owner-scope items genuinely separated ✓

§7 enumerates 3 owner-scope items, each a genuine cost/coverage/sequencing trade-off (not a punted technical decision):

1. **HU corpus size 750 vs 1500.** Architect commits to 750 in §4.4 with reasoning; 1500 doubles labelling cost (~$80-160 add) for marginal coverage gain. Genuine cost trade-off.
2. **Phase 1.5 ship boundary.** Currently committed: ship after 1.5-E (router/coaching alignment). Alternative: ship after 1.5-D.4 with 1.5-E follow-on. Genuine sequencing trade-off; both have real costs.
3. **Phase 2 D5 entry condition.** Depends on whether Phase 1.5 fully or partially ships. Genuine conditional sequencing item; cannot be resolved at design time.

All 3 are clearly separated from architect's committed decisions in §1-§5.

### Item 11 — Per-prediction falsifiability ✓

Each of the 7 §6 predictions specifies an observable that could empirically fail:

| Prediction | Sub-phase | Observable that could fail | Falsifiable? |
|---|---|---|---|
| P1 | 1.5-B | bit-equality `diff` produces non-empty output | ✓ |
| P2 | 1.5-C | 5-seed mean falls below stated probability bounds (≥32.50/40 @ 80% conf; ≥33.00/40 @ 60% conf) | ✓ |
| P3 | 1.5-C | stay-wrong taxonomy moves a hand between PIPELINE-MISMATCH ↔ MODEL-STUCK categories OR new stay-wrong appears | ✓ |
| P4 | 1.5-D.1 | < 5 of 30 HU spots are CLOSE OR < 3 in axes HU-2/HU-6 | ✓ |
| P5 | 1.5-D.2 | Sonnet 5-labeller consensus rate < 80% on the 30-hand HU set | ✓ |
| P6 | 1.5-D.4 | vNext-HU-59 5-seed mean < 26/30 OR < 28/30 with stated probability OR first-run clear-rate falls outside the stated ≤30% range | ✓ |
| P7 | 1.5-E | coaching pipeline tests fail after the production swap, or test-suite changes are required | ✓ |

All 7 are falsifiable observations with concrete thresholds, not tautologies.

---

## SHOULD_FIX-1 — §1.2 TC-23 EXISTENCE drift on v8-HU model artifacts (cascading framing)

### Evidence

```
RED river-rats-core/models/gto_model_v8_hu.json
RED river-rats-core/models/gto_model_v8_38feat.json
```

Verified at master `9c3b9ae`:

```bash
$ git ls-tree -r master --name-only | grep "^river-rats-core/models/" | grep -iE "v8_hu|v8_38feat"
# (no output — neither file is tracked)

$ git log --all --oneline -- 'river-rats-core/models/gto_model_v8_hu.json' \
                              'river-rats-core/models/gto_model_v8_38feat.json'
# (no output — never committed in any branch)
```

The repo's `models/` directory contains v9-3way + v2.x legacy + 12.5K-A + 12.5K-C-E artifacts; **no v8 model artifact is present**. `oracle_router.py:34` references `'gto_model_v8_hu.json'` as the HU slot filename and `:41` references `'gto_model_v8_38feat.json'` as the legacy fallback — both are dangling filename pointers.

### Where the drift propagates

Three downstream sections depend on the v8-HU-38 artifact's existence:

1. **§1.2** — explicit attestation: "`river-rats-core/models/gto_model_v8_hu.json` — exists." and "`river-rats-core/models/gto_model_v8_38feat.json` — exists (legacy)." Both are factually wrong at master HEAD.

2. **§4.2** — close-hand selection methodology: "3 of 5 hands per axis are CLOSE (per `feedback_close_hand_selection.md`: model uncertainty on **v8-HU-38** + poker difficulty, NOT feature-stat extremes)." The methodology requires running the v8-HU-38 model on candidate spots to compute prediction uncertainty. Without the artifact in the repo, this step has no defined input.

3. **§4.5** — lineage framing: "v8-HU-38 stays as a **lineage anchor (provenance only)**; vNext-HU-59 is a clean training run on the 750 HU corpus + 59-surface." Implies v8-HU-38 is currently in production. It isn't; there is no production HU artifact in this repo.

4. **§4.6** — production-swap framing: "On gate clear, `models/gto_model_v8_hu.json` (38-feat) is **REPLACED** in production by `models/gto_model_vNext_hu_59feat.json`." Implies a current production model to replace. There isn't one in the tree; the swap is a CREATE, not a REPLACE.

### Severity reasoning

Per `feedback_spec_vs_infrastructure_code_drift.md`:

> If you find drift, it's a HIGH-severity finding (not a NIT).

And per the dispatch's own critical audit emphasis:

> TC-23 EXISTENCE strict — if architect cites a file:function path that doesn't exist, downstream sub-phases will TC-23-FAIL on the cascade

This is exactly that case. Severity classified **SHOULD_FIX (not BLOCKER)** because:

- The substantive design path (drop 2 J-B → re-extract → train HU on 59) is **correct and unaffected**.
- The fix is a paragraph-level correction in §1.2 / §4.2 / §4.5 / §4.6 (clarify v8-HU status; re-frame baseline + lineage + swap), **not a structural redesign**.
- The 1.5 workstream's first 2 sub-phases (1.5-B feature-prune, 1.5-C 3-way verification at 59) are **independent** of the v8-HU-38 status; they can fire while the SHOULD_FIX is resolved.
- 1.5-D.1 close-hand-selection methodology **cannot fire** until the v8-HU-38 status is resolved — that's the binding gate where this becomes blocking.

### Suggested resolution (architect-discretion; not a directive)

One of the following, per `feedback_quality_default_no_ask.md` single-committed-path:

1. **Bring v8-HU-38 into the repo** (if the artifact exists on a development machine, commit it under `river-rats-core/models/` with a provenance docstring per CLAUDE.md §6 training-provenance). Then §1.2 attestation becomes correct retroactively.
2. **Re-frame the baseline as PokerBench 88.1% directly** (drop the v8-HU-38 dependency in §4.2 close-hand selection; replace with PokerBench-API-based uncertainty OR a model-uncertainty proxy on the 988-corpus 3-way model on HU spots). §4.5 / §4.6 reframe lineage / swap as CREATE-not-REPLACE.
3. **Reframe close-hand selection methodology** (§4.2) without requiring a baseline HU model — e.g., poker-difficulty-only, or expert-judgment selection.

Owner-scope to direct which path; orchestrator can route via routine dispatch comm.

### Routing

Per `feedback_explicit_action_trigger.md`: this finding is QC-FLAG (advisory). Owner / orchestrator decides whether the fix lands as architect amendment to PR #307 pre-merge OR as a fix-forward in 1.5-B PR with §1.2 carrying a known-issue note. Either path is consistent with `feedback_qc_required_before_approval.md` SHOULD_FIX-on-milestone-PR semantics.

---

## NIT-1 — §1.3.3 trainer assertion arithmetic prose

### Evidence

§1.3.3 trainer hard-asserts paragraph:

> `river-rats-core/train_model_v9_student.py:97` (61 → 59); **`:115` (`_V24_P1_BLOCKERS` at indices `-5:-1` post-drop, was `-6:-2` pre-drop)** — note this is one of the few places where an off-by-N exists in the assertion structure; architect commits to: "assert v2.4 P1 blockers occupy positions 56-59 of the 59-feature list (indices `-4:` of the 59-list)" with rationale that the J-B drop frees the tail.

The "**indices `-5:-1` post-drop**" arithmetic is wrong:

- 61-list with 4 v2.4 P1 blockers at positions 56-59 + 2 J-B at positions 60-61: blockers at indices `-6:-2` of 61-list ✓ (matches actual code at `train_model_v9_student.py:115-117`).
- 59-list (post-J-B-drop): blockers at positions 56-59, indices `-4:` of 59-list. **Not `-5:-1`.**

The architect's actual commitment (`-4:`) is correct. The wrong "`-5:-1`" arithmetic is then-immediately-flagged ("note this is one of the few places where an off-by-N exists") and corrected.

### Severity reasoning

NIT — confusing prose; the architect's commitment is correct. A reader skimming the paragraph could be misled by the "`-5:-1`" line; the corrected commitment is one sentence later. Cleanup recommendation: drop the wrong "`-5:-1` post-drop" mention entirely; the corrected `-4:` commitment is sufficient on its own.

### Suggested resolution

§1.3.3 paragraph rewrite:

> `river-rats-core/train_model_v9_student.py:97` (61 → 59); `:115-117` (current assert: `_V24_P1_BLOCKERS` at indices `-6:-2` of the 61-list; post-drop, blockers occupy positions 56-59 = indices `-4:` of the 59-list; J-B drop frees the tail).

Non-blocking; architect-discretion on whether to apply pre-merge.

---

## Test classes exercised

- **TC-23** (CONTENT + EXISTENCE) — 25 cited paths + sub-line:function refs verified at master HEAD; **2 of 25 RED on file existence** (SHOULD_FIX-1 evidence)
- **TC-X-OWNER-SCOPE-DISCIPLINE** (21st formal use) — 6 mandatory negatives held; 3 owner-scope items genuinely separated
- **TC-X-DISPATCH-COMPLIANCE** (20th formal exercise; durable) — 5 design-area per-area requirements + dispatch's 11-item expanded scope
- **TC-X-DISPATCH-PREDICTION-VERIFICATION** (1st formal exercise) — 7 falsifiable predictions registered for retrospective verification at each sub-phase close
- **TC-X-INTRA-PLAN-CONSISTENCY** (informal — checked across §1-§5 + §6 + §7 for cross-section consistency on the 59-surface and the sub-phase decomposition)
- **TC-X-METHODOLOGY-RULE-CROSSCHECK** (informal — 8 methodology rules cited and addressed; pilot-first BINDING gates present on all 5 long-batch sub-phases)

## Smarter-over-time

This is the **first** Phase 1.5 design-lock audit; the 11-item expanded-scope template (7 ship-format items + per-design-area + single-committed-path scan + 3-owner-scope-item separation + per-prediction falsifiability) is now durable for future workstream design locks (Phase 1.5-D.1 HU reference set design comm; Phase 2 D5 design comm; v9-4way design lock).

The TC-23 EXISTENCE finding here is the first concrete instance of the dispatch-spec drift class on a forward-binding (architect's own attestation, not synthesis citing an upstream comm). Pattern surfaces a generalization: TC-23 EXISTENCE on architect attestations is load-bearing precisely because architects are the source-of-truth on infrastructure paths; if an architect's "I verified at master HEAD" is wrong, downstream sub-phases inherit the error.

The retrospective analysis: the architect's grounding step (per builder report §"Pre-execution grounding") read most of the cited paths individually but did NOT enumerate `models/` directory contents — instead it asserted 4 model artifacts existed without `git ls-tree`-style verification. **Suggested addition to `feedback_builder_grounds_before_executing.md`** (curative; QC-flag): when architect attests file existence, run `git ls-tree -r master --name-only | grep <pattern>` for each artifact class (models/, data/, prompts/) rather than relying on memory or recently-read state. Routing: orchestrator surfaces the suggestion; owner decides whether to formalize.

## Curative-additions log update (per orchestrator drift-retro PR #310 suggestion)

Per `MAIN_TERMINAL_PR308_DRIFT_RETRO_2026-05-08.md` §"QC stream — catch acknowledged + curative-additions suggestion":

QC ratifies the suggestion. **New test class `TC-X-ORCHESTRATOR-BRANCH-BASE-VERIFICATION`** added to `~/river-rats-qc/learning/test_class_registry.md` and `~/river-rats-qc/learning/incident_pattern_library.md`. Trigger: any orchestrator-authored PR. Check: PR's diff vs master matches the orchestrator's stated single-file-comm intent (typically 1 file; trigger PRs are exactly 1 trigger comm; dispatch PRs are exactly 1 dispatch comm). Past finding: PR #308 (closed; bundled-content drift caught pre-merge by QC).

## Gates

PR #307 cleared from QC side **with 1 SHOULD_FIX surfaced for owner+architect resolution before 1.5-D.1 fires**.

Per `feedback_qc_required_before_approval.md` SHOULD_FIX-on-milestone-PR semantics + going-forward owner-merge-fire rule:

- **Path A:** Owner directs architect to amend PR #307 with §1.2/§4.2/§4.5/§4.6 resolution → re-fire QC for delta-verification → owner fires merge.
- **Path B:** Owner accepts PR #307 as-is with SHOULD_FIX-1 carried into 1.5-B PR's known-issues list → owner fires merge → architect resolves in 1.5-B with no critical-path delay (1.5-B is feature-prune mechanical, independent of HU baseline).
- **Path C:** Owner directs architect to drop the v8-HU-38 dependency entirely (e.g., re-frame close-hand selection as PokerBench-baseline) → architect amends → re-fire QC → owner fires merge.

QC-recommended path: **Path B** (lowest critical-path cost; SHOULD_FIX is bounded and resolvable in 1.5-B without blocking the 1.5-C 3-way verification on the 59-surface). But this is owner-scope per `feedback_orchestrator_decides_not_recommends.md`.

After PR #307 + this verdict comm merge, orchestrator dispatches Phase 1.5-B (feature-prune mechanical execution) per architect's committed sequencing in §4.7. **LOOP CONTINUES.**

## Cycle stats

- 41st solo QC cycle.
- Wall clock: ~28 min (within the 20-30 min heads-up estimate).
- LLM cost: $0.

---

**Verdict: PASS-WITH-FINDINGS · 0/1/1 · milestone-class Phase 1.5 design lock substantively cleared · 1 SHOULD_FIX on §1.2 TC-23 EXISTENCE drift (cascade into §4.2/§4.5/§4.6 framing) for owner+architect resolution; QC-recommended path = fix-forward in 1.5-B · 1 NIT on §1.3.3 prose · LOOP CONTINUES on owner-fire-now of merge.**
