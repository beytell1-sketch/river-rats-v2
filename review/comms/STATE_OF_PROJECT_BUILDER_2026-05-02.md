---
date: 2026-05-02
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · QC stream · Owner
re: Phase 0 restart — three-way state alignment, builder seat
status: ALIGNMENT — state-of-project comm only; no forward work; no QC peek
---

# Builder state-of-project alignment

Authored independently per `MAIN_TERMINAL_STATE_OF_PROJECT_RESTART` directive
(received 2026-05-02). I have NOT consulted QC's parallel report.

Restart probe completed: master clean, up-to-date with origin, no open
PRs prior to this one, last commit `14c2db1` (2026-04-27).

---

## Q1 — Where are we?

**Master HEAD:** `14c2db1` *Orchestrator: Phase 12 directive — v9 student warm-start trainer (59-feat XGBoost) (#104)* — 2026-04-27.

**Gap since last activity:** 5 days (2026-04-27 → 2026-05-02). No
commits, comms, or PR activity in that window. The most recent comms doc
is dated 2026-04-27 21:51.

**Last shipped baseline (per `CLAUDE.md`):** v8 oracle 88.1% HU /
52.5% multiway on 40-hand reference set; 45-feature pipeline shipped;
progressive chain v8→v9-3way→v9-4way→v9-5way approved; v9 baseline
trained on 45-feat PokerBench, ready as warm-start anchor at
`river-rats-core/models/gto_model_v9_baseline_45feat.json`.

**Last merged code-bearing PR:** `#101` *Builder Phase 11C: 494-hand
mass labels (2470 labels, v3.2 protocol, 0% refusal)* — merged
2026-04-27, master commit `78bad39`. Adds
`data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (494 rows;
SHA-256 `329c43b6…7c64b` per the programmer report).

**Last merged orchestrator PR:** `#104` *Phase 12 directive*. The
directive itself is a comms doc, not code.

**Dominant workstream of the last week:** mass-labelling pipeline arc
— Phase 8 (scenario expansion v3.6) → Phase 10 (corpus revision FINAL,
494 hands, PR #70) → Phase 11A (mass-labelling scripts, PR #98) →
Phase 11B/11C (5×494 labels with consensus, PR #101) → Phase 12
(trainer directive issued, no PR yet).

The arc converged on a single deliverable: a 494-hand × 59-feature
corpus + 2470 v3.2-protocol consensus labels, ready for v9 student
warm-start training. Action distribution: CHECK 49.6% / BET 17.4% /
FOLD 14.6% / CALL 12.6% / RAISE 5.9% (RAISE is the rarest class).
Consensus: 62.6% unanimous, 22.1% 4/5, 14.4% 3/5, 1.0% plurality-tied.

---

## Q2 — Last open directive and its status

**Directive id:** `MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`
(commit `14c2db1`, PR #104 merged 2026-04-27 19:51 UTC).

**Named author:** LEAD-PROGRAMMER (me).

**Scope:** Train v9 student model — 59-feature XGBoost
`multi:softprob` 5-class — warm-started from
`gto_model_v9_baseline_45feat.json` on the 494-hand corpus + 2470
consensus labels. 5 seeds (0-4), 80/20 stratified split, confidence
weighting per row, 5 litmus tests, per-class precision/recall (esp.
RAISE), feature importance top 20, comparison vs 45-feat baseline on
same held-out.

**Work done:** None. No PR opened, no
`PROGRAMMER_REPORT_PHASE12_TRAINER_2026-04-27.md` exists in
`review/comms/`. The 5-day gap is the entire status of this directive.

**Work pending:** All of it — but the directive itself anticipates the
build will not run as written. From §"Operational sequence" Step 3:

> "Verify exact arg names against `train_model.py` argparse before
> running. If absent, do NOT improvise — report BLOCKED and surface
> what the script actually accepts."

> "If train_model.py doesn't support warm-start at this 45→59
> boundary, builder reports BLOCKED — Phase 12.5 directive will
> resolve."

**Blockers I see (verified end-to-end against master HEAD):**

I read `river-rats-core/train_model.py` (512 lines) end-to-end. The
directive's invocation is incompatible with the trainer in nine
distinct ways:

| # | Directive expects | `train_model.py` master HEAD | Severity |
|---|------------------|------------------------------|----------|
| B1 | `argparse` with `--corpus`, `--labels`, `--warm-start`, `--output`, `--seeds`, `--confidence-weighting` | No `argparse` at all. Only `'--45feat' in sys.argv` toggle (line 505). `if __name__ == '__main__'` hardcodes `csv_file = 'training-data/train_3way_v3_combined.csv'` (line 499) | **BLOCKER** — cannot invoke as directed |
| B2 | JSONL input (`data/corpus_revision_500_hand_2026-04-27.jsonl` + `..._labels_…jsonl`) | `load_csv()` reads a CSV via `csv.DictReader` (lines 167-193). No JSONL loader. | **BLOCKER** — wrong format |
| B3 | Warm-start from a 45-feature base model into 59-feature student | XGBoost's `xgb_model=` parameter is the supported path; `train_model.py` never passes it (`model.fit(X_train, y_train, eval_set=…, sample_weight=…)` on line 259). No 45→59 schema bridge. | **BLOCKER** — methodology not implemented |
| B4 | 5 seeds (0,1,2,3,4) for variance estimation | Single hardcoded `random_state=42` (lines 246, 309). No seed loop. | **BLOCKER** — multi-seed not implemented |
| B5 | Per-sample `consensus_confidence` weighting | Inverse-class-frequency weights with `RAISE` capped at `3.0` (lines 252-257). Different scheme — per-class, not per-sample. | **BLOCKER** — methodology divergence |
| B6 | 59-feature schema (per directive: "45 base + 14 v2.4 P1 blockers") | `train_model.py` `FEATURE_COLUMNS` = **55** (counted line-by-line, lines 131-160). `gto_model.py:64` explicitly: `N_FEATURES = len(FEATURE_COLUMNS)  # 55`. The 4 v2.4 P1 blockers (`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`) live in `feature_keys.py:89-92` but are NOT in `gto_model.py`/`train_model.py` `FEATURE_COLUMNS`. Real composition: **55 + 4 = 59**, not 45 + 14. | **DRIFT in directive arithmetic** + integration gap |
| B7 | Held-out litmus reference at `training-data/3way_reference_40hand.jsonl` (qualified by directive: "or whatever the canonical reference set is — verify path before running") | File does not exist. `ls training-data/*reference* training-data/*40hand*` returns nothing. | **BLOCKER** — canonical reference path unresolved |
| B8 | Join corpus + labels on `ref_id` | Corpus records have `pilot_hand_id` (e.g., "PILOT_001") and `source_situation_id` (e.g., "d6066_BB_flop") but **no `ref_id` field**. Labels records have BOTH `ref_id` (= corpus's `source_situation_id`) AND `pilot_hand_id`. Either join key works in practice, but the directive's literal instruction is wrong — ambiguous resolution needed. | **DRIFT** — directive cites a key the corpus doesn't carry |
| B9 | 80/20 stratified split (per ml-architect round 7 PR #80) at training time | `train_model.py:226-228` uses `train_test_split(stratify=y, random_state=42)` — single split, not multi-seed. | **PARTIAL** — present but not seed-looped |

The directive itself flagged B1+B3 as anticipated stop conditions. I
also surface B2, B4, B5, B6, B7, B8 as additional drift that the
directive's "Phase 12.5" mention will need to cover.

**Practical implication:** The Phase 12 build cannot be a small fix
to `train_model.py`. It needs a new training module (likely
`train_model_v9_student.py`) authored from scratch, with: JSONL
load, corpus+labels join, 59-feat schema, warm-start via
`xgb_model=base.json`, 5-seed loop, per-sample confidence weighting,
litmus suite hook, multi-seed reporting. Per the training-provenance
addendum in `CLAUDE.md` §6 (2026-04-15): the new trainer must live
in `river-rats-core/` with a provenance docstring linking commit →
model artifact.

---

## Q3 — Next step from my seat (recommendation, not authority)

**My recommendation:** Re-scope Phase 12 as Phase 12.5, where ml-architect
designs the new student trainer module before any code is written. The
directive's 9-flag invocation in §"Operational sequence" Step 3 should
be treated as illustrative — the actual entry point, hyperparameter
strategy, warm-start mechanics, and per-sample weighting math need ml
design first.

**Sequence I'd recommend (in priority order):**

1. **Resolve the four directive ambiguities first** (orchestrator
   responsibility, see Q5). Without those, ml-architect builds on
   guesses.

2. **ML-architect dispatch (1 agent):** design
   `river-rats-core/train_model_v9_student.py` — argparse contract,
   JSONL loader, join policy, 45→59 warm-start mechanics
   (`xgb_model=` + feature-name preservation), per-sample weighting
   math (`sample_weight = consensus_confidence` vs combined with
   inverse-class), 5-seed loop, eval pipeline integration, output
   manifest format. Output: design doc to
   `review/comms/PLAN_PHASE12_TRAINER_2026-05-XX.md`.

3. **Owner approves design.**

4. **Architect dispatch (1 agent):** read the ML design end-to-end,
   read existing `train_model.py` + `gto_model.py` + `feature_keys.py`,
   produce exact insertion-point blueprint with line numbers. Output:
   `review/comms/BLUEPRINT_TRAIN_V9_STUDENT_2026-05-XX.md`.

5. **Builder (me) dispatch:** implement from blueprint only. Run the
   training. Report.

6. **Round 12 review chain** as the directive specified: ml-architect
   + gto-expert + QC milestone gate.

**What I would NOT do without explicit greenlight:**

- I would NOT modify `train_model.py` in place. The 4 v2.4 P1 blocker
  features were added in Step 17 (`feature_keys.py:87-92`) but never
  propagated to the trainer's `FEATURE_COLUMNS` — that's a separate
  gap from Phase 12 and may have downstream implications I haven't
  scoped.

- I would NOT improvise on the join key (`ref_id` vs `pilot_hand_id`
  vs `source_situation_id`) without orchestrator confirmation — both
  surfaces are reachable, but committing to one in code without
  acknowledgement risks a silent mismatch.

- I would NOT pick a confidence-weighting scheme on my own (per-sample
  vs per-class vs hybrid) — that's an ml-architect call per
  `docs/PROCESS_GUIDE.md` §1.4 ("Experts decide HOW; owner decides
  WHAT").

**Per the directive Step 5:** I am stopping at this comm + PR. The
above is recommendation, not action.

---

## Q4 — Concerns and drift I see

### D1 — Directive feature-count arithmetic is wrong
Directive: "59 features per `feature_extractor.py` FEATURE_COLUMNS
(45 base + 14 v2.4 P1 blockers)".
Source: `gto_model.py:64` = 55 features. `feature_keys.py:89-92` = 4
v2.4 P1 blockers. Real composition is **55 + 4 = 59**. The "45 + 14"
framing collapses two unrelated milestones (v8→v9 step at 45 features,
then 45→55 via Steps 12-16 in `feature_keys.py:67-85`, then 55→59 via
Step 17 P1 blockers) into a single "v2.4" delta. A trainer designed
on the directive's framing would set up the wrong pre-flight check.
`scripts/verify_feature_schema_compatibility.py:39-41` already encodes
the correct math (`FEATURE_COLUMNS + V24_P1_BLOCKER_FEATURES == 59`)
— the directive should align to that. **Severity: HIGH-2.** Fixable
by directive amendment; doesn't change the corpus or labels.

### D2 — Join key cited by directive doesn't exist on corpus
Directive: "Join corpus + labels on `ref_id`". Corpus records have
`pilot_hand_id` + `source_situation_id` but no `ref_id`. Labels carry
both. The intended join is almost certainly
`corpus.source_situation_id == labels.ref_id` (verified on row 1:
both `d6066_BB_flop`) OR `corpus.pilot_hand_id == labels.pilot_hand_id`
(both `PILOT_001`). **Severity: HIGH-2** — picking the wrong key in a
silent corner case (e.g., if ref_id is normalised differently) could
mis-join. Builder asks orchestrator to commit to one before
implementation.

### D3 — Canonical reference set path is unresolved
Directive cites `training-data/3way_reference_40hand.jsonl` with the
caveat "or whatever the canonical reference set is — verify path
before running". It does not exist. Possible candidates from
`training-data/` listing: `3way_combined_350.jsonl`,
`3way_labelled.jsonl`, `3way_selected_200.jsonl`,
`3way_situations.jsonl`, `facing_bet_test_set_40.jsonl`. Without
orchestrator commit on which file is the canonical 40-hand reference
set, "5 litmus tests" in §"Operational sequence" Step 4 is
unresolvable. **Severity: HIGH-1** — a directive whose pass/fail gate
is undefined cannot be reviewed.

### D4 — `train_model.py` provenance and applicability
The Phase 12 directive points at `train_model.py` for the training
run, but that file (last touched 2026-04-21 per `ls -la`) was authored
for the original v9 student arc on the older 45-feature CSV pipeline
(`training-data/train_3way_v3_combined.csv`, hardcoded line 499). It
predates the corpus + label JSONL pipeline by ~2 weeks. The directive
treats it as a maintained training entry point; the source treats it
as a closed v9 single-seed script. The training-provenance addendum
in `CLAUDE.md` §6 prohibits editing existing model-producing scripts
in place when an experimental run produces a keeper — it implies
authoring a new script per major run. So even if the 9 blockers in
Q2 were patchable, the right answer is a new file. The directive
should reflect that. **Severity: MEDIUM** — process drift, not data drift.

### D5 — Models directory has 17 historic v9 model artefacts
`river-rats-core/models/` has 35 entries, including 8 distinct v9-3way
variants (`gto_model_v9_3way.json`, `_45feat`, `_v2.1`, `_v2.2`,
`_v2`, `_v3`, `_v3_45feat`, `_warmstart`). Not a current blocker.
Worth a separate housekeeping pass once Phase 12 ships and the new
v9 student model is the canonical artefact. **Severity: LOW**, NIT only.

### D6 — 5-day gap with active named directive
Per memory `feedback_named_author_builds_not_polls.md`: when a
directive names me as author, the next tick is authoring, not
polling. The 5-day silence is itself a process failure on my side —
the directive was issued 2026-04-27 21:51 and I should have authored
within the same session or next-day. The Phase 0 restart framing
acknowledges this. I take this as personal feedback; surfacing here
so the orchestrator + owner have a record. **Severity: SELF-FLAG.**

### D7 — Trainer 4-blocker integration is a separate gap
`feature_keys.py:87-92` defines the 4 v2.4 P1 blocker features (per
spec `BUILDER_V24_P1_SPEC_LOCKED_2026-04-19.md`). But neither
`gto_model.py:33-62` nor `train_model.py:131-160` includes them in
their respective `FEATURE_COLUMNS` constants. The corpus produces
59-feature `feat_dict` records (verified row 1: 59 keys), so the
extraction side is current. The training side is not. This is the
deepest cause of the Phase 12 directive's 45-vs-55 confusion and
needs to be reconciled before any 59-feature warm-start works. The
gap predates Phase 12. **Severity: HIGH-1** — blocks Phase 12 entirely.

---

## Q5 — Asks of the other two terminals

### To orchestrator (Main terminal)

**A1 (HIGH-1 — blocks all forward work):** Commit to the canonical
reference set path for §"Operational sequence" Step 4 litmus tests.
`training-data/3way_reference_40hand.jsonl` does not exist;
candidates listed in D3.

**A2 (HIGH-1 — blocks build):** Resolve the `gto_model.py` /
`train_model.py` 4-blocker integration gap (D7). Either (a) issue a
preparatory directive to extend `FEATURE_COLUMNS` to 59 in
`gto_model.py` + `train_model.py` (which would touch sacred core),
OR (b) confirm that the new student trainer module owns the
59-feature schema independently and `gto_model.py` will be updated
on a separate ship-gate. Either is workable; builder must not pick.

**A3 (HIGH-2 — directive amendment):** Amend Phase 12 directive
arithmetic to "55 base + 4 v2.4 P1 blockers = 59" (D1). Align to
`scripts/verify_feature_schema_compatibility.py:39-41`.

**A4 (HIGH-2 — directive amendment):** Commit to the corpus↔labels
join key (D2). Recommended:
`corpus.source_situation_id == labels.ref_id` (matches the directive's
"ref_id" wording on the labels side and is verified to coincide on
row 1). If you prefer the more durable
`corpus.pilot_hand_id == labels.pilot_hand_id`, say so explicitly so
the trainer can be coded to it.

**A5 (process):** Re-issue Phase 12 as Phase 12.5 with ml-architect
in the lead seat per `docs/PROCESS_GUIDE.md` §6 *Training Protocol —
Mandatory Team*. The current directive jumps straight from
"orchestrator → LEAD-PROGRAMMER" but Section 6 mandates Step 1 ML
design + owner approval before architect blueprint + before
programmer implements. The directive's review chain (ml + gto + QC)
is correct for the post-training gate but doesn't substitute for
the pre-build ML design step.

### To QC stream

**Q1 (independence):** Per the orchestrator's three-way alignment
framing, I have not consulted your parallel state-of-project comm.
This builder report is independent.

**Q2 (V-Implementation-Spec-Match audit on Phase 12 directive vs
master HEAD):** When orchestrator amends the directive (A1-A5), I'd
ask QC to run a TC-23 pre-merge audit on the amended directive vs
master HEAD source — specifically: (a) does the amended directive's
canonical reference set path exist? (b) does the amended directive's
feature-count arithmetic match `gto_model.py:64` +
`feature_keys.py:89-92`? (c) does the amended join-key claim verify
on row 1 of corpus + labels? Per memory
`feedback_spec_vs_infrastructure_code_drift.md`: this is exactly the
two-axis (CONTENT + EXISTENCE) drift pattern.

**Q3 (Phase 12 trainer pre-flight, when authored):** Once the new
student trainer module is built, QC pre-merge audit should validate
the 5 ship-gate criteria of `docs/PROCESS_GUIDE.md` §2 (calibration,
leakage, feature importance, reference gate, independent review)
against the as-built trainer, not against the directive — per
`feedback_verify_source_not_plan.md`.

---

## Compliance with Phase 0 restart constraints

| Constraint (per directive) | Compliance |
|----------------------------|------------|
| No modifications to `river-rats-core/` | ✅ — read-only |
| No pipeline / training runs | ✅ — none invoked |
| No QC peek (independence) | ✅ — only own reads + master HEAD source |
| No proposing new directives | ✅ — Q3 is recommendation, not authority |
| Single file PR, no src changes | ✅ — only this comm |
| STOP after PR | ✅ — pending orchestrator's `SHARED_STATE_BASELINE` synthesis + owner sign-off |

---

## References (cited evidence)

- Master HEAD: `14c2db1` (2026-04-27)
- Last code-bearing PR: `#101` master `78bad39`
- Phase 12 directive: `review/comms/MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md` (master `14c2db1`)
- Phase 11B/C builder report: `review/comms/PROGRAMMER_REPORT_MASS_LABELLING_2026-04-27.md`
- Trainer source: `river-rats-core/train_model.py` (no argparse, lines 498-512; CSV loader lines 167-193; FEATURE_COLUMNS=55 lines 131-160; class-frequency weighting lines 251-257)
- Oracle FEATURE_COLUMNS: `river-rats-core/gto_model.py:33-64` (`N_FEATURES = 55` line 64)
- Feature key constants: `river-rats-core/feature_keys.py:89-92` (4 v2.4 P1 blockers)
- Schema compatibility script: `scripts/verify_feature_schema_compatibility.py:33-42` (correct 55+4=59 math)
- Corpus row 1 sampled: keys = board, deal_id, facing_bet, feat_dict (59 keys), hero_cards, hero_position, num_opponents, **pilot_hand_id ("PILOT_001")**, pot, prior_actions, **source_situation_id ("d6066_BB_flop")**, street, to_call, villain_positions; **no `ref_id`**.
- Labels row 1 sampled: keys = **ref_id ("d6066_BB_flop")**, **pilot_hand_id ("PILOT_001")**, labels, **consensus_action ("CHECK")**, **consensus_confidence (0.6)**, vote_count, valid_vote_count, feat_dict.
- Process: `CLAUDE.md` §6 (training provenance addendum, 2026-04-15); `docs/PROCESS_GUIDE.md` §6 (mandatory training team).
- Memory: `feedback_listen_to_orchestrator_always.md`,
  `feedback_named_author_builds_not_polls.md`,
  `feedback_builder_grounds_before_executing.md`,
  `feedback_verify_source_not_plan.md`,
  `feedback_github_is_state_not_local.md`,
  `feedback_spec_vs_infrastructure_code_drift.md`,
  `feedback_qc_required_before_approval.md`,
  `reference_river_rats_v2_restart_protocol.md`.

**Status: BUILDER STATE-OF-PROJECT ALIGNMENT COMPLETE. Stopping per Step 5. Awaiting orchestrator's `SHARED_STATE_BASELINE` synthesis + owner sign-off before any forward work.**
