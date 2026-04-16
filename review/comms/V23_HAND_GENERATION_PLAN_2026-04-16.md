---
date: 2026-04-16
from: Architecture Expert
to: Owner (Rupert)
re: v2.3 hand generation BUILD PLAN — per-bucket sequencing, gates, checkpoints, stop conditions
status: AWAITING OWNER REVIEW — no generation begins until approved
approved_scope: review/comms/PLAN_V23_SCOPE_2026-04-15.md (APPROVED 2026-04-16)
owner_directive: review/comms/V22_SHIP_DECISION_2026-04-16.md §4
diagnostic_test_set: review/comms/PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md (APPROVED with Track E amendments)
---

# v2.3 Hand Generation Build Plan

This plan operationalises the approved v2.3 scope into an
executable sequence. It does NOT generate any hands. Owner review
required before Phase 1 (pre-flight) begins.

---

## 0. Scope Reconciliation — the 206 / 400 Question

### The two numbers in the scope

Scope §1 specifies a **206-hand aggression supplement** with a
line-itemised allocation table across 12 rows (`PLAN_V23_SCOPE §1`,
lines 37-53). Scope §2 specifies a **400-hand defensive
multiway-checked-through CHECK bias supplement** sized to the
precondition predicate at Stream C's lower branch
(`PLAN_V23_SCOPE §2`, "Supplement Sizing — RESOLVED 2026-04-15",
lines 214-234).

### Scope's own resolution (lines 240-246, verbatim):

> Relation to Section 1's 206 figure. The 206-hand v2.3 supplement
> is the narrower, targeted MW miss pattern. The 400-hand
> predicate-bucket supplement is the broader Defensive
> Multiway-Checked-Through CHECK Bias correction. The 206 is a
> subset shape; the 400 is the umbrella. v2.3 hand generation must
> deliver both, with the 206 nested inside the 400 where
> preconditions overlap. Final allocation table to be reconciled
> before generation.

### The two readable interpretations

**Interpretation U (Umbrella).** Total new hands = **400**. The 206
Section-1 buckets are generated _inside_ the 400 — i.e. every
Section-1 row that satisfies the Section-2 predicate counts toward
both tallies. Section-2 predicate is:
`facing_bet=False ∧ num_opponents≥2 ∧ villain_checked_back=1 ∧
villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧
equity_vs_range≥0.35 ∧ SPR≤2.0`. The Section-1 rows that sit
inside this shape are the "checked-to" rows (most of the 186 BET
rows except the facing-bet raise rows).

**Interpretation A (Additive).** Total new hands = **606** (206 +
400). Section 1 and Section 2 are independent generation targets.
This matches the literal addition of the two scope sections but
ignores the scope-author's explicit "umbrella / subset" framing.

### Architect recommendation — Interpretation U (Umbrella), 400 total

Reasoning:

1. **Scope-author intent is explicit.** Lines 240-246 say
   verbatim: "The 206 is a subset shape; the 400 is the umbrella."
   "The umbrella" is singular — one deliverable covers both.
2. **Stream C verdict sized the 400 to resolve the full bias,
   inclusive of the MW miss pattern.** The 400 was chosen against
   the precondition predicate that the 10 MW misses all satisfy
   (see Stream C §7 "bucket CHECK fraction 20.8%, supplement lower
   end"). A separate additive 206 would either (a) duplicate the
   predicate-shape hands the 400 already covers, or (b) push the
   training set too far toward BET (see projected v2.3
   distribution table at scope §1 lines 115-122 — already 48.2%
   BET with +186 delta).
3. **Class-rebalance math checks out on 400.** Scope §1's delta
   accounting (+186 BET, +20 RAISE, +0 CHECK/CALL/FOLD) produces
   ~48.2% BET at 591 total hands. If we added 400 more on top
   (i.e. 606 new, 991 total), the BET share would climb past 55%
   and risk the Track 6 §2.4 Group-D regression fallback (>1 hand
   Group-D reversal regression = STOP). Interpretation U keeps the
   BET share inside the scope-author's intended zone.
4. **Owner directive.** V22_SHIP_DECISION §2 lists "Supplement
   sizing: 400 hands (per Stream C...)". It does not list 606. The
   single-number approval is consistent with Interpretation U.

### Final allocation — Interpretation U (RECOMMENDED)

| Category | Count | Section |
|----------|-------|---------|
| Section 1 allocation rows satisfying Section 2 predicate (checked-to, SPR≤2, num_opponents≥2) | ~186 | §1 ∩ §2 |
| Additional Section 2 hands filling out the 400-umbrella but outside Section 1's row list | ~214 | §2 only |
| Section 1 allocation rows NOT satisfying Section 2 predicate (facing-bet RAISE rows, value-raise rows) | ~20 | §1 only |
| **Total new hands** | **~420** | — |

Note: 420 vs 400 — the ~20 value-raise rows (Section 1 row 9) are
facing-bet, so they fall outside the Section-2 checked-to
predicate. They are additive to the 400 umbrella because the
umbrella is predicate-scoped, not deliverable-scoped. If Owner
prefers a strict 400-total, drop the 20 value-raise rows from the
supplement — the trade-off is that BP1_08-class RAISE training
coverage does not improve. Architect recommendation: keep the 20;
the corresponding risk is negligible.

**If Owner prefers Interpretation A (additive, 606 total):** see
§11 Appendix A for the alternative allocation table and the
class-balance implications.

---

## 1. Generation Tasks — Per Bucket

### 1.1 Source mix

| Source | Estimated hands | Role |
|--------|-----------------|------|
| `situation_factory.py` via new `generate_factory_batch6.py` | ~370 | Bulk generation, BP-format, validator-gated |
| Curated from existing pool (`3way_combined_350.jsonl` + `factory_batch5_situations.jsonl`) | ~20-30 | Drawing-hand row clones (Section 1 row 6-7) |
| Solver-sourced (Owner GTO Wizard sessions) | ~10-20 | Mixed-zone BET row (Section 1 row 11) + Section 4 auto-enqueue reserve |

### 1.2 Per-bucket plan

Each row below maps to Section 1's 12-row allocation table
(`PLAN_V23_SCOPE §1`, lines 41-53) plus a residual row for the
214 additional umbrella-filler hands.

Columns: `BP=net target (after validator)`, `OS=overshoot
generated`, `Output=JSONL filename`.

| # | Bucket | Action | Street | BP | OS | Source | Output JSONL | Validator risk |
|---|--------|--------|--------|----|----|--------|--------------|----------------|
| 1 | Medium made (IP, checked-to, SPR 1-2) | BET (protection) | Turn | 30 | 38 | Factory (MM_IP_TURN) | `v23_mm_ip_turn.jsonl` | LOW |
| 2 | Medium made (IP, checked-to, SPR 1-2) | BET (protection) | Flop | 15 | 19 | Factory (MM_IP_FLOP) | `v23_mm_ip_flop.jsonl` | LOW |
| 3 | Medium made (OOP, checked-to, SPR 1-2) | BET (thin value / protection) | Turn | 20 | 25 | Factory (MM_OOP_TURN) | `v23_mm_oop_turn.jsonl` | LOW |
| 4 | Strong made (IP, checked-to, low danger) | BET (value) | Turn | 20 | 25 | Factory (SM_IP_TURN) | `v23_sm_ip_turn.jsonl` | LOW |
| 5 | Strong made (IP, checked-to, low danger) | BET (value) | River | 15 | 19 | Factory (SM_IP_RIVER) | `v23_sm_ip_river.jsonl` | LOW |
| 6 | Drawing (nut draw + blocker) | BET (semi-bluff) | Flop | 15 | n/a | **Curated** from pool | `v23_curated_draw_flop.jsonl` | n/a — pool filter |
| 7 | Drawing (nut draw + blocker) | BET (semi-bluff) | Turn | 10 | n/a | **Curated** from pool | `v23_curated_draw_turn.jsonl` | n/a — pool filter |
| 8 | Monster (any position, checked-to) | BET (value) | Flop/Turn | 15 | 19 | Factory (MON_CHECKED) | `v23_mon_checked.jsonl` | LOW |
| 9 | Value RAISE (facing bet, strong/monster) | RAISE | Flop/Turn | 20 | 25 | Factory (RAISE_VALUE) | `v23_raise_value.jsonl` | MED — multi-street |
| 10 | Protection BET (medium made, danger board) | BET | Flop | 16 | 20 | Factory (PROT_DANGER) | `v23_prot_danger.jsonl` | LOW |
| 11 | Mixed-zone BET | BET | Any | 10 | n/a | **Solver-sourced** (pre-labelled) | `v23_solver_mixed.jsonl` | n/a — Owner curates |
| 12 | Aggressor continuation (PFR, checked-to, dry) | BET | Flop | 20 | 25 | Factory (PFR_CONT) | `v23_pfr_cont.jsonl` | LOW |
| U | Umbrella filler — Section-2-only predicate hands not in rows 1-12 | BET (≈80%) / CHECK (≈20%) per Stream C bucket distribution | Flop/Turn/River | 214 | 268 | Factory (UMBRELLA) | `v23_umbrella_fill.jsonl` | MED — predicate-gated |
| — | **Total net** | — | — | **420** | **483** | — | — | — |

**Overshoot justification.** The Section-1 notes (lines 55-58)
say 5-10% overshoot. The `num_opponents` validator in
`situation_factory.py` (Fix 1, commit b69e668) raises `ValueError`
on any `SituationSpec` where `len(villain_positions) <
num_opponents`. This validator did not exist when batch5 was
generated, so the ~5% failure rate is not empirically measured
for v2.3 sub-patterns. **Overshoot target: 25%.** Rationale: the
validator is conservative; we prefer to throw away valid-but-
unneeded hands to trimming a bucket below target.

**Validator hook specifics (per
`BP_GENERATOR_DEFECT_DIAGNOSIS §4` Fix 1):**

```python
# situation_factory.py build_situation(), after opponents list built:
if len(spec.villain_positions) < num_opponents_declared:
    raise ValueError(...)
```

Every factory spec built by a new `generate_factory_batch6.py`
MUST set `num_opponents` on the spec. Any sub-pattern that fails
validation is logged to the per-bucket error log and overshot
against.

### 1.3 Build `generate_factory_batch6.py`

The existing generators (`batch2/3/4/5`) are bucket-specific.
v2.3 needs its own generator script per the Section-1 row patterns.
**Recommendation:** build one `review/generate_factory_batch6.py`
parameterised by sub-pattern, with each sub-pattern corresponding
to a row in the allocation table (rows 1-5, 8, 9, 10, 12, plus
residual umbrella).

The new script must:
1. Import `SituationSpec`, `build_situation`, `validate_situation`,
   `normalise_situation` from `situation_factory` — same pattern
   as `batch5.py` (lines 34-36).
2. Set `num_opponents=2` on every spec (3-way context).
3. Write `villain_positions`, `hero_position`, `action_string`,
   `street` into `feat_dict` (batch5 lines 1944-1952 — already
   compliant; batches 2/3/4 are NOT compliant — Fix 2 in BP
   diagnosis).
4. Pipe every record through `normalise_situation()` before
   `json.dumps` (batch5 line 1985 — already compliant).
5. Write one JSONL per bucket (not a single mega-file) — makes
   per-bucket validator failures traceable.
6. Emit a per-bucket count summary at the end
   (expected vs generated vs validated).

**DO NOT modify `generate_factory_batch2/3/4/5.py`.** They are
committed, their outputs are v2.2 inputs. Fix 2 from the BP
diagnosis (batches 2/3/4 missing villain_positions write) is
low-priority per the diagnosis doc §8 — v2.2 labelling complete,
regeneration unlikely. Deferred to separate cleanup track.

### 1.4 Curated-bucket sourcing (rows 6-7)

Per Scope §1 "Curated from existing pool (approx 20 of 206)"
(lines 70-76):

- Pool filter: `3way_combined_350.jsonl` (350 3-way hands) plus
  `factory_batch5_situations.jsonl` (185 BP hands).
- Filter criteria: hands where `is_made_hand=0 AND (has_flush_draw=1
  OR has_straight_draw=1) AND draw_outs ≥ 8 AND
  facing_bet=0 AND num_opponents=2`.
- Spot-check each candidate for nut-draw + blocker (e.g.
  Ah + second-nut flush draw card; or Ace-high straight draw
  with blocker). Manual review required — pool filter surfaces
  candidates, Owner/Architect confirms blocker status.
- Curated hands run **through the same Pass 1 / Pass 2 pipeline
  as generated hands** — NOT pre-labelled. See scope line 75.

### 1.5 Solver-sourced sourcing (row 11)

Per Scope §1 (lines 77-83):

- Owner runs 10-20 hands in GTO Wizard where the solver shows
  clear BET (70%+ frequency).
- These are written directly into
  `training-data/v23_solver_mixed.jsonl` in labelled form
  (label_source = "solver_sourced_gto_wizard_v23").
- They count against the Section 4 (scope §4) 15-20% solver ratio
  and bypass Pass 1 / Pass 2.
- Owner session planning: Section 4's table estimates 30 min =
  4-5 hands / 60 min = 7-10 hands. 10-20 hands = 1-3 sessions.

---

## 2. Pre-flight Checks (Phase 0)

Before any hand generation begins, the following MUST pass:

### 2.1 Test gates

```bash
cd /home/rupert/river-rats-v2/river-rats-core
python3 -m pytest tests/test_situation_factory.py -v
python3 -m pytest tests/test_training_data_encoding.py -v
```

- `test_situation_factory.py` — 9 tests (verified via `grep "def test"`).
  Must pass. Tests the Fix-1 validator + normalise_situation.
- `test_training_data_encoding.py` — 3 test classes. Must pass on
  existing JSONLs. Verifies the ANOMALY-A dtype guard still holds
  post-commit b69e668.

### 2.2 Schema sanity

Round-trip `normalise_situation` on a random sample (10 records)
from each of:
- `training-data/factory_batch5_situations.jsonl`
- `training-data/factory_batch3_situations.jsonl`

Assert: input record → `normalise_situation(record)` →
`json.loads(json.dumps(...))` → identical keys, numeric types
preserved, `street` ∈ {0, 1, 2}, `hero_position` ∈ {0-5}. Write
test to `river-rats-core/tests/test_situation_factory.py` (new
test, one-shot).

### 2.3 Disk check

```bash
df -h /home/rupert/river-rats-v2/training-data
```

Require ≥ 2 GB free. The 420 new situations + overshoot are
small (JSONL records ~4-8 KB each → ~4 MB total), but solver
outputs and the eventual v2.3 training CSV are several MB. 2 GB
is a comfortable margin.

### 2.4 Prompt preparation

`prompts/gto_labeller_v3.md` does **not currently exist** (confirmed
via `ls prompts/`). It must be created by taking
`prompts/gto_labeller_v2.md` and applying Scope §3's Additions A,
B, C, D verbatim. **This is a v2.3 prerequisite, not a generation
prerequisite.** It must be in place before the calibration gate
(Phase 3) runs, but it does NOT gate hand generation (Phase 1).

### 2.5 Git hygiene

Working tree clean before generation starts. `git status` must
report `nothing to commit, working tree clean`. The per-bucket
commit cadence (§7) requires a clean start.

### 2.6 Pre-flight pass/fail gate

If any of 2.1 through 2.3 fails → STOP, report, fix before
proceeding. 2.4 is a separate dependency (Phase 3 blocker, not
Phase 1 blocker). 2.5 is a working-tree check.

---

## 3. Calibration Gate — Sequencing (Phase 3)

Per Scope §5 "Explicit Calibration Gate" (lines 487-513) and
V22_SHIP_DECISION §2 ("Calibration gate: 23/28 minimum + all
reversal hands correct before any production labelling"):

### 3.1 Calibration exam infrastructure — CONFIRMED PRESENT

`river-rats-core/calibration_exam.py` exists (337 lines,
verified). Key entry points:
- `run_calibration(label_fn, prompt_path, knowledge_path)` (line 262)
- `GTO_REVERSAL_HANDS = {'MW-30', 'MW-33', 'MW-50'}` (line 33)
- `score_results()` — returns `gate_passed` bool.
- Current thresholds: 20/24 + all 3 reversals (line 214).

**v2.3 update required (pre-Phase-3):** update
`calibration_exam.py` to:
- Add 4 new calibration candidates from Scope §5 (d8886, d2410,
  d8963, d3178). Requires new reference-hand entries or a
  separate load path for these non-MW-set hands.
- Update `_prompt` default to `prompts/gto_labeller_v3.md`.
- Update gate thresholds to 23/28 + all 7 hard anchors (MW-30/33/50
  + d8886/d2410/d8963/d3178).
- Add Group-D reversal hand ingestion (from the diagnostic test
  set) per Scope §5.3 "All reversal hands correct" — every Group D
  hand in `PLAN_V23_DIAGNOSTIC_TEST_SET` must also be correct.
  This increases the exam beyond 28; exact count depends on how
  many reversals Group D lands with (target 5 per diagnostic §2.D).

**This update is a separate engineering task — part of Phase 3
prep, NOT production labelling prep.** It may be deferred to
immediately before Phase 3 runs, but it blocks Phase 3.

### 3.2 Gate sequencing

```
Phase 1: Hand generation (situations only, no labels)
         ↓
Phase 2: Situation-assembly QA — per-bucket validation, overshoot
         trim, normalise_situation round-trip
         ↓
Phase 3: CALIBRATION GATE
         - Run calibration_exam.py against gto_labeller_v3.md
         - Pass threshold: 23/28 AND all reversal hands correct
         - PASS → proceed to Phase 4 (production labelling)
         - FAIL → STOP, return to panel redesign
         ↓
Phase 4: Production labelling (Pass 1 + Pass 2)
         ↓
Phase 5: Assembly
         ↓
Phase 6: v2.3 training
         ↓
Phase 7: Validation
```

**Gate is ABSOLUTE: no Phase 4 before Phase 3 PASS.** Scope §5
verbatim: "Any failure returns to panel redesign... No v2.3
production labelling (the 206-hand supplement) may begin until the
gate clears."

### 3.3 Panel redesign if gate fails

Per Scope §5.3:
1. Revise prompt (edit `gto_labeller_v3.md`).
2. KB cross-reference pass (check `knowledge/three_way_gto.md`
   against failure pattern).
3. Re-run calibration.
4. Re-run up to N=3 times; if still failing on iteration 3,
   escalate to Owner for scope revision.

---

## 4. Production Labelling — Sequencing (Phase 4)

After calibration gate PASSES:

### 4.1 Pass 1 — 4 independent panels

Per Scope §6 "No New Architecture Phases" (lines 548-559): use the
same 4+2 team structure as v2.2 — 4 Pass 1 panels + 2 Pass 2
review panels.

- Input: all 420 new unlabelled situations (Sections 1 +
  umbrella + curated) EXCLUDING the 10-20 solver-sourced (those
  are pre-labelled).
- Labeller: `gto_labeller_v3.md` + `knowledge/three_way_gto.md`.
- Pipeline: `labelling_agent.prepare_batches()` (now with
  `_normalise_flat_situation()` helper per commit b69e668 —
  confirmed at `labelling_agent.py:47-105`).
- Batching: same 10-per-batch as v2.2 (verified
  `prepare_batches` default `batch_size=10`).
- 4 panels × 42 batches = ~168 agent calls.

### 4.2 Pass 2 — 2 review panels

- Input: Pass 1 consensus + per-hand disagreement flags.
- Reviewers apply Scope §6 override discipline:
  - `override_kb_justification` required when Pass 2 diverges
    from Pass 1 majority.
  - `enqueue_for_solver` auto-set to true on 3/4+ overrides.
- Auto-enqueue triggers (Scope §4) fire during Pass 2:
  - LOW confidence → solver.
  - 2-2 split Pass 1 → solver.
  - 3/4-majority override → solver.

### 4.3 Solver cohort merging

- 10-20 solver-sourced hands (Section 1 row 11) enter the assembly
  CSV at known label (skip Pass 1/Pass 2).
- Auto-enqueued hands (Pass 1/2 triggers) wait for Owner solver
  sessions (90-min sessions, 7-15 hands each; Scope §4 estimates
  2-3 sessions per week during labelling).

### 4.4 Labels file

Final per-hand record: `training-data/pass1_final_labels_v23.jsonl`
(following v2.2 naming `pass1_final_labels.jsonl`).

Fields per record: situation dict + `expert_action` +
`expert_confidence` + `label_source` +
`feature_attention` (Pass-1 union) + any Pass-2 override metadata.

---

## 5. Assembly (Phase 5)

Per the v2.2 Phase 3.5H pattern (verified at
`review/comms/PHASE_3_5H_FINAL_ASSEMBLY_2026-04-15.md` lines 62-71):
108-column training CSV.

### 5.1 Merge JSONLs

```
v23_mm_ip_turn.jsonl + v23_mm_ip_flop.jsonl + ... + v23_umbrella_fill.jsonl
 + v23_curated_draw_*.jsonl + v23_solver_mixed.jsonl
 → training-data/v23_supplement_labelled.jsonl   (N hands, all with labels)
```

Then merge with v2.2:

```
training-data/pass1_final_labels.jsonl (385 hands)
 + v23_supplement_labelled.jsonl (~420 hands)
 → training-data/pass1_final_labels_v2_3.jsonl (~805 hands)
```

### 5.2 Build 108-column CSV

Use an assembly script modelled on
`river-rats-core/assemble_pilot_data.py:write_attention_csv()`
(line 926) — it already writes the 54 FEATURE_COLUMNS + 54 attn_*
+ label format. Extend to add `situation_id` and `label_source`
columns (matching v2.2's 111-col output: 1 sit_id + 54 raw + 54
attn + label + label_source).

Output: `training-data/v2_3_training.csv`

### 5.3 Schema preflight — MUST PASS

```bash
cd /home/rupert/river-rats-v2
python3 river-rats-core/train_model_v2_2.py \
    --csv training-data/v2_3_training.csv \
    --out river-rats-core/models/v2_3_model.json \
    --report river-rats-core/models/v2_3_training_report.json
```

The trainer's `_preflight_schema_check` (called from
`train_model_v2_2.py:65`) runs by default. The `--allow-mixed-
encoding` flag is NOT passed. Any mixed-encoding failure fails the
build → STOP, investigate the assembly path.

Note: the trainer refuses to overwrite `v2_2_model.json` (line
324-328). The v2.3 run writes to `v2_3_model.json` explicitly.

---

## 6. Validation (Phase 7)

Per Scope §5 + V22_SHIP_DECISION §2 + Track E diagnostic doc.

### 6.1 Evaluation harness

`river-rats-core/evaluate_v2_2.py` (437 lines, verified). Works
on any model path via `--model`. Copy/rename to
`evaluate_v2_3.py` (or invoke v2_2.py with `--model` pointing at
v2_3). Architect recommendation: **use v2_2.py with `--model` and
`--csv` overrides** — no rename needed, reduces code drift.

### 6.2 Evaluation sets

Per diagnostic §5 (Track E):

| Set | Path | v2.2 baseline | v2.3 target |
|-----|------|---------------|-------------|
| FB-40 | `training-data/facing_bet_test_set_40.jsonl` | 72.5% | ≥ 72.5% |
| MW-50 | `training-data/test_set_50_labelled.jsonl` | 84.0% | ≥ 84.0% |
| Group A+B mixed zones | new (Track E) | measured | ≥ 70% AND ≥ v2.2 + 5pp |
| Group C passive-lean | new (Track E) | measured | diagnostic only |
| Group D reversals | new (Track E) | measured | v2.2 accuracy − 1 floor |

### 6.3 Solver validation on 8 MW misses

Per V22_SHIP_DECISION §3: the 8 remaining MW misses are
solver-verified post-v2.3 training. Owner runs these in GTO
Wizard, compares v2.3 predictions vs solver output.
Pass criterion: the bias-correction hypothesis holds — v2.3 now
predicts BET (or the solver-mixed action) on those 8 hands where
v2.2 predicted CHECK.

### 6.4 Pass criteria summary

**SHIP v2.3 if all of:**
- FB-40 ≥ 72.5% AND MW-50 ≥ 84.0% (stability, Track E §5)
- Group A+B ≥ 70% AND ≥ v2.2 + 5pp (primary, Track E §5)
- Group D regression ≤ 1 hand (fallback, Track E §5.4)
- Solver on 8 MW misses: ≥ 6/8 corrected (post-hoc sanity)

**STOP (do NOT ship v2.3) if any of:**
- FB-40 or MW-50 regresses below v2.2 baseline
- Group A+B < 70% absolute or < v2.2 + 5pp
- Group D regression > 1 hand → trigger Scope §5.4 fallback
- Solver on 8 MW misses: ≤ 3/8 corrected (training didn't take)

---

## 7. Checkpoints + Commits

One commit per major phase milestone. Sequence:

| # | Commit message | Trigger |
|---|---------------|---------|
| C0 | `v2.3 gen: pre-flight checks pass` | Phase 0 complete |
| C1 | `v2.3 gen: <bucket> situations (N hands gen, M validated)` | Per Section-1 bucket (11 commits: rows 1-5, 8-10, 12, curated, umbrella) |
| C2 | `v2.3 gen: phase 2 assembly QA complete` | All buckets pass post-gen validation |
| C3 | `v2.3 gen: calibration exam <PASS/FAIL> (N/28 + reversals)` | Phase 3 complete |
| C4 | `v2.3 gen: Pass 1 labels complete (N hands)` | Phase 4.1 complete |
| C5 | `v2.3 gen: Pass 2 reconciliation complete` | Phase 4.2 complete |
| C6 | `v2.3 gen: solver cohort merged (N solver-queued, M solver-sourced)` | Phase 4.3 complete |
| C7 | `v2.3 gen: assembly + CSV (N hands, schema gate clean)` | Phase 5 complete |
| C8 | `v2.3 train: model saved river-rats-core/models/v2_3_model.json` | Phase 6 complete |
| C9 | `v2.3 eval: FB-40 = X%, MW-50 = Y%, Group A+B = Z%, Group D delta = ±N` | Phase 7.1-7.2 complete |
| C10 | `v2.3 validation: solver result on 8 MW misses = N/8 corrected` | Phase 7.3 complete |
| C11 | `v2.3 ship decision: <SHIP/ITERATE>` | Phase 7.4 complete |

Each commit includes only the artefacts produced by that phase.
No mixed-phase commits. Rebase on master before each commit.

---

## 8. Stop Conditions

Any condition triggers immediate STOP + report-to-Owner. No silent
recovery.

### Phase 0 (pre-flight)
- **S0.1** Test suite fails on `test_situation_factory.py` or
  `test_training_data_encoding.py`.
- **S0.2** `normalise_situation` round-trip fails on any
  existing-JSONL sample.
- **S0.3** Disk free < 500 MB.
- **S0.4** Working tree dirty at start.

### Phase 1 (generation)
- **S1.1** Any generator yield off target by > 25% (generated N <
  0.75 × overshoot target). Indicates structural bug, not
  yield-loss.
- **S1.2** `num_opponents` validator fires on > 5% of specs in
  any single bucket (e.g. > 1 fail in 20 for bucket 3). Indicates
  generator author did not follow spec conventions.
- **S1.3** Any `json.dumps` of a generated record fails (e.g.
  non-serialisable dtype from the factory).
- **S1.4** Curated pool filter (§1.4) returns < 20 candidates.
- **S1.5** Solver-sourced hand (row 11) fails pre-flight (solver
  sequence invalid, bet-size mismatch).

### Phase 2 (assembly QA)
- **S2.1** After per-bucket overshoot trim, any bucket is > 1
  hand below its BP target.
- **S2.2** `normalise_situation` round-trip fails on any generated
  record.

### Phase 3 (calibration gate)
- **S3.1** Calibration score < 23/28 → panel redesign.
- **S3.2** Any reversal hand (MW-30, MW-33, MW-50, or the 4 new
  hard-anchor candidates d8886/d2410/d8963/d3178, or any Group D
  reversal) incorrect → panel redesign.
- **S3.3** Panel redesign iteration count exceeds 3 → escalate to
  Owner for scope revision.

### Phase 4 (labelling)
- **S4.1** Pass 1 inter-panel disagreement rate > 35% (v2.2
  baseline was ~15% per 3.5C report — 35% is 2× baseline).
- **S4.2** Pass 2 override rate > 10% of total hands (v2.2 was
  22/385 ≈ 5.7%; 10% suggests panel dysfunction).
- **S4.3** Solver queue depth exceeds Owner session throughput
  (> 30 hands waiting for solver at any one time) → pause
  labelling, catch up.

### Phase 5 (assembly)
- **S5.1** `_preflight_schema_check` fails on the assembled v2.3
  CSV. This means Fix 1 did not cover some encoding path — major
  issue, full investigation required.
- **S5.2** Hand count in assembled CSV does not match
  385 (v2.2) + 420 (new) = 805 within ±5 (tolerance for LOW-
  confidence exclusions).

### Phase 6 (training)
- **S6.1** Training fails XGBoost internal validation (early-stop
  triggers on training loss diverging).
- **S6.2** Output `v2_3_model.json` accidentally targeted as
  `v2_2_model.json` (trainer SystemExit at line 324-328 — guard
  is in place).

### Phase 7 (validation)
- **S7.1** FB-40 drops below v2.2 baseline (< 29/40 correct).
- **S7.2** MW-50 drops below v2.2 baseline (< 42/50 correct).
- **S7.3** Group A+B < 70% absolute OR < v2.2 + 5pp → do NOT ship.
- **S7.4** Group D regression > 1 hand → Scope §5.4 fallback: do
  NOT ship, investigate supplement over-representation.
- **S7.5** Solver on 8 MW misses: ≤ 3/8 corrected → the training
  supplement did not shift the decision boundary in the intended
  direction.

---

## 9. Risk Register

### R1 — Factory yield loss after `num_opponents` validator (MEDIUM)

The Fix-1 validator fires at generation time on any spec where
`villain_positions` is shorter than `num_opponents`. Historical
yield data on this validator does not exist (it was added in
b69e668 after the batch5 generation). Estimated 5% yield drop
based on BP-diagnosis §2 evidence (176/185 BP hands had the
defect in the formatter layer, not the spec layer — so the
actual spec-side validator hit rate is likely < 5%).

**Mitigation.** 25% overshoot on every bucket (§1.2). If
actual yield drop < 5%, the excess is trimmed at Phase 2 to the
exact BP target. If actual drop is in the 5-25% range, the 25%
overshoot still nets target.

### R2 — Calibration gate fails on first iteration (MEDIUM-HIGH)

The Pass-1 prompt override clause (Scope §2.2, 199-212) is
significant new content. The calibration exam's 4 new hard anchors
(d8886, d2410, d8963, d3178) are the exact spots the override
targets — if the override is over-aggressive, the agent may now
BET on situations where CHECK is still correct (Group D-style
reversal). Vice versa, if under-aggressive, it fails the new
anchors.

**Mitigation.** Before the full calibration run, do a "prompt-
only" sanity pass: run the 4 new anchors alone with the v3
prompt, see whether the agent BETs. If 4/4 BET → good, run full
28-hand exam. If 0-1/4 BET → prompt under-aggressive, revise
before full exam. If 2-3/4 BET → proceed, full exam will clarify.

### R3 — Group D regression from over-aggressive supplement (HIGH)

Scope §1 projects BET rising from 25.7% (v2.2) to 48.2% (v2.3).
Track E §5.4 fallback: >1-hand Group D regression = STOP. The
supplement is heavily BET-weighted by design — Group D is
where the reversal bites.

**Mitigation.** Mid-training diagnostic: after Phase 6 completes,
before Phase 7, spot-check a handful of Group D candidates
against v2.3 predictions. If v2.3 over-BETs on any candidate
that v2.2 correctly CHECKs, flag the supplement for review
before full evaluation run.

### R4 — Owner solver-session throughput (MEDIUM)

Scope §4 Owner-time table: 90 hands at 60-min sessions = 9-13
sessions. At 2-3 sessions per week, 3-6 weeks of solver work.
The project schedule is post-v2.2-ship, but any long solver delay
stalls v2.3 shipping and downstream teaching work. The 8 MW-miss
solver validation (Phase 7.3) is separate from auto-enqueue
volume.

**Mitigation.** Phase 4.3 can proceed in parallel with solver
throughput — Pass-1/Pass-2 labels are provisional until solver
confirms. Flag provisionals as `DISPUTED_OVERRIDE` in assembly
CSV per Scope §6. Training can proceed on provisional labels with
a note to retrain if solver overrides them.

### R5 — Prompt v3 does not exist yet (LOW, but blocking)

`prompts/gto_labeller_v3.md` is referenced throughout scope but
not present in the repo. Creating it is a prerequisite for Phase
3. It is not a generation blocker — situations can be generated
(Phase 1) without v3 prompt being ready — but it blocks Phase 3
calibration.

**Mitigation.** Flag this as a Phase 3 prerequisite in the Owner
review. Prompt creation is a separate, small engineering task:
copy v2, apply Scope §3 Additions A-D.

---

## 10. Estimated Agent Calls + Duration

| Phase | Agent calls | Parallelisable? | Estimated duration |
|-------|-------------|-----------------|---------------------|
| Phase 0 (pre-flight) | 1 (bash + 2 pytest runs) | No | 15-30 min |
| Phase 1 (generation) | 1 (single python run) per bucket × 11 buckets = 11 | Yes (buckets independent) | 30-45 min total (factory gen is fast, ~30 hands/sec) |
| Phase 1.4 (curated) | 1 (filter script + Architect review) | No | 1-2 hours (manual review of ~30 candidates) |
| Phase 1.5 (solver-sourced) | n/a (Owner-led, external to agent) | n/a | 1-3 Owner solver sessions, 30-90 min each |
| Phase 2 (assembly QA) | 1 | No | 15 min |
| Phase 3 (calibration) | 1 × 28 = 28 calls (one per calibration hand) + prompt-only sanity = ~32 | Yes within exam | ~15 min (plus prompt iteration if fail) |
| Phase 4.1 (Pass 1) | 4 panels × 42 batches = 168 agent calls | Yes (panels independent) | 2-3 hours with parallel panels, 8+ hours serial |
| Phase 4.2 (Pass 2) | 2 review panels × ~15 disagreement batches = ~30 calls | Yes (panels independent) | 1-2 hours |
| Phase 4.3 (solver cohort) | 0 agent calls | n/a | Owner-time, parallel with 4.1/4.2 |
| Phase 5 (assembly) | 1 (assembly script run) | No | 15 min |
| Phase 6 (training) | 1 (trainer run) | No | 10-20 min (XGBoost on ~800 hands) |
| Phase 7.1-7.2 (evaluation) | 1 (evaluator run) | No | 10 min |
| Phase 7.3 (solver validation) | 0 agent calls | n/a | Owner-time, 1-2 sessions for 8 hands |

**Critical-path end-to-end (excluding Owner solver time):** 8-12
hours of active agent work, across ~250 agent calls.

**Wall-clock to ship (including Owner):** 3-6 weeks at 2-3 solver
sessions/week.

---

## 11. Appendix A — Interpretation A (Additive, 606 total)

If Owner overrides the architect recommendation and prefers the
Additive interpretation: generate 206 (per Section-1 allocation
table exactly) PLUS 400 (per Section-2 predicate bucket
independently). Total = 606 new hands.

Implication on projected v2.3 distribution (v2.2 base 385 + 606
new):

Assuming new 606 are ~85% BET (both sections' BET-heavy),
Total = 991 hands:
- BET: 99 + ~515 = 614 (62.0%)
- CHECK: 131 + ~85 = 216 (21.8%)
- CALL: 57 (5.8%)
- FOLD: 75 (7.6%)
- RAISE: 23 + ~20 = 43 (4.3%)

BET at 62% is above Scope §1's 48.2% projection and materially
raises Group-D regression risk per Scope §5.4. The class-weight
cap conversation from Scope §1 (lines 124-130) would need to be
revisited — current cap logic assumes 48.2% BET.

Architect maintains **Interpretation U recommendation** unless
Owner has a specific reason to prefer A.

---

## 12. Approval requested

- [ ] Owner confirms **Interpretation U (Umbrella, ~420 total)** as
      the allocation.
- [ ] Owner approves the 11-bucket per-file JSONL output plan
      (§1.2).
- [ ] Owner approves 25% overshoot target (§1.2).
- [ ] Owner approves `generate_factory_batch6.py` as a new
      parameterised generator script (§1.3).
- [ ] Owner approves the 7-phase pipeline with commit cadence (§7).
- [ ] Owner approves the stop-condition register (§8).
- [ ] Owner approves creating `prompts/gto_labeller_v3.md` from
      v2 + Scope §3 additions as a Phase-3 prerequisite.
- [ ] Owner approves updating `calibration_exam.py` to the 23/28
      threshold + 4 new hard anchors + Group-D reversal ingestion
      as a Phase-3 prerequisite.

On approval, Builder executes Phase 0, reports results, proceeds
per plan.

---

*Build plan complete. No hands generated. No code modified. Awaiting owner review per CLAUDE.md §1 Plan Before Build and V22_SHIP_DECISION §4.*
