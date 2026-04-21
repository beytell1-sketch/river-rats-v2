---
date: 2026-04-22
from: Builder (grounding pass per orchestrator directive)
to: Orchestrator · Owner
re: Grounding verification of blueprint v2 + supplement against origin/master; contradictions + clarifications needed BEFORE reconciliation pass #2
status: GROUNDING COMPLETE — 1 major contradiction surfaces; 4 clarifications needed; v2.2 amendment proposed
sources_verified:
  - origin/master HEAD = ce7ad3f (manifest v1.10 CORRECTION commit)
  - read via `git show origin/master:<path>` per directive discipline
---

# Stage 3.5 — Grounding Report

Per orchestrator directive (2026-04-22): ground blueprint v2 + v2.1
supplement against origin/master, report contradictions, raise
clarifications, DO NOT dispatch reviewer panel until clarified.

**Grounding commands executed:**
```
git fetch origin               # origin/master = ce7ad3f
git status                     # clean working tree
git log --oneline origin/master..HEAD      # local ahead by 1 (3166759 supplement)
git log --oneline HEAD..origin/master      # empty — local is not behind
```

**State:**
- Origin HEAD `ce7ad3f` — manifest v1.10 (the CORRECTION commit)
- Local HEAD `3166759` — my v2.1 supplement, **NOT pushed**
- Blueprint v2 base `8bb0f9f` **IS** on origin

---

## 1. Grounding confirmation — 14 files verified against origin/master

| File | Verification | Result |
|------|-------------|--------|
| `RELEASE_MANIFEST.yaml` | Read v1.10 changelog + Stage 4 gate | **Manifest is v1.10, not v1.9** (1 version ahead of my supplement references) |
| `river-rats-core/feature_extractor.py` | `extract_range_composition` (1116+), Step 12 (1651+), Step 17 (1729+), equity sites (500, 617, 805, 828), FOLD re-fetch (1186) | **All blueprint v2 BEFORE blocks match origin** — no HEAD drift |
| `river-rats-core/range_narrowing.py` | Exists; `narrow_to_betting_range`, `narrow_to_checking_range`, `narrow_to_continuing_range`, `narrow_by_action_history` | All four functions present; BEFORE blocks match |
| `river-rats-core/calibration_exam.py:279-298` | `hand_dict` construction | **No `_action_history` key** — MUST #20 gap confirmed |
| `river-rats-core/reference_evaluator.py:470-489, 693-713` | Both `hand_dict` sites | **No `_action_history` key at either** — MUST #22 gap confirmed |
| `river-rats-core/extract_features_parallel.py:81` | `except Exception:` swallow | Confirmed — MUST #9 target |
| `river-rats-core/extract_incremental.py:105` | `except Exception as e:` swallow | Confirmed — MUST #9 target |
| `river-rats-core/run_attention_experiments.py:462` | `col_names_108 = list(FEATURE_COLUMNS) + ['attn_' + f for f in FEATURE_COLUMNS]` | Confirmed — MUST #27 site (but see §2 for framing surprise) |
| `river-rats-core/assemble_pilot_data.py` | `/tmp/pilot_situations.json` + `/tmp/pilot_v2_consensus.json` readers; writes `pilot_20_attention.csv` (109 cols) | **Confirmed exists — but this is v2.2 Exp 3 pilot code, NOT the Stage 4/5 production writer** (see §2) |
| `river-rats-core/explain_hand.py:264, 329` | Inline `narrow_to_betting_range` calls | Confirmed bypass sites — MUST #19 targets |
| `river-rats-core/coaching/feature_extractor.py` + `coaching/range_narrowing.py` | Files exist; earlier research confirmed zero runtime importers | Confirmed — MUST #8 partial-delete still valid |
| `knowledge/three_way_gto.md` §1.10 + §1.11 + §1.12 | Read headings + multi-signal resolution rule | **KB §1.10–§1.12 exist with full blocker PRIMARY-tagging guidance** — MUST #24 RETRACTION correct; Stage 2 truly COMPLETE |
| `prompts/gto_labeller_v3.1.md:363-420` | Attention section — "54-feature vector", bucket mandatory-tag table | Confirmed — includes `flush_block_pct` but NOT the 4 new v2.4 blockers; MUST #25 REFRAMING (Stage 3 deliverable) correct |
| `review/comms/BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md` | Read Stage 3 plan + 6 GTO-review modifications applied | Confirms Stage 2 COMPLETE; Stage 3 plan explicitly includes v3.2 prompt bump with mandatory-tag rules for new blockers |
| `review/comms/RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md` | Read Exp 3 results | Confirms 108-feature (54 raw + 54 attention) precedent from pilot-20 dataset |
| `review/comms/PHASE_4_LABELLING_REPORT_2026-04-17.md` | Read production labelling round status | 470 hands labelled with v3 prompt (commit `3dfc35f`); 91.7% unanimous agreement; override rate 1.1% |

**13 of 14 files confirm blueprint v2 BEFORE blocks and research findings are accurate against origin.**

---

## 2. ONE MAJOR CONTRADICTION — MUST #26 + #27 target scope

The supplement at `3166759` (LOCAL ONLY, not pushed) frames MUSTs #26
and #27 as PATCHES to `assemble_pilot_data.py` and
`run_attention_experiments.py`. After grounding, this framing is
**wrong**.

### 2.1 What grounding revealed

**`assemble_pilot_data.py`** is a v2.2-era pilot-experimental script.
Evidence from origin:
- Docstring (`river-rats-core/assemble_pilot_data.py:2-12`): "reads `/tmp/pilot_situations.json` and `/tmp/pilot_v2_consensus.json`, merges with hardcoded ATTENTION_LEVELS and INTENTION_TAGS tables, writes `pilot_20_enriched.jsonl` (canonical JSONL) and four CSV files"
- Blueprint reference in docstring: "`BLUEPRINT_FEATURE_ATTENTION_TRAINING_2026-04-14.md`" — **this is the Exp 3 pilot blueprint**, not a Stage 4 production writer
- Input paths hardcoded to `/tmp/pilot_*` — not a parameterised production assembler
- Writes specifically `pilot_20_*.csv` naming convention

**`run_attention_experiments.py`** is the Exp 3 pilot experiment runner, not a Stage 5 trainer:
- Reads `training-data/pilot_20_attention.csv` (hardcoded pilot-20 dataset)
- Docstring (`run_attention_experiments.py:454-456`): "Runs Experiment 3 (auxiliary attention flags as extra features). 108 features: 54 original + 54 attn_* binary flags."
- The `col_names_108` variable name is cosmetic; content is dynamic but variable name burns "108" in place

**v2.3 assembly/training scripts exist:**
- `assemble_v23.py`, `assemble_v23_1.py`, `assemble_v23_2.py`, `assemble_v23_clean.py` (repo root) — v2.3 assembly scripts
- `river-rats-core/train_v2_3_1.py` + `river-rats-core/train_v2_3_2.py` — v2.3 trainers referencing upstream `assemble_v23_1.py` / `assemble_v23_2.py`

**v2.4 assembly/training scripts do NOT exist yet:**
- No `assemble_v2_4.py` on origin (verified by grep)
- No `train_v2_4.py` on origin (verified by grep)
- Per manifest v1.10: Stage 4 = "expand training data with distribution audit" (future work); Stage 5 = "retrain and full eval" (future work)

### 2.2 Why my supplement's framing is wrong

The supplement at `3166759` §2.2–§2.3 shows BEFORE/AFTER edits to
`assemble_v23_clean.py:27` (root-level script) and implies the fix
goes into `assemble_pilot_data.py` also. But:

- Patching `assemble_pilot_data.py` edits the Exp 3 pilot code; it
  doesn't influence Stage 4 production assembly (which doesn't exist
  yet).
- Patching `run_attention_experiments.py` edits Exp 3 experiment code;
  it doesn't influence Stage 5 production training (trainer doesn't
  exist yet).
- The `assemble_v23_clean.py:27` pattern I quoted (`ATTN_FEATURES = [f"attn_{c}" for c in RAW_FEATURES]`) is accurate, but that's a v2.3 script — v2.4 will clone from it.

**The correct framing for MUSTs #26 and #27 is prescriptive, not corrective:**
- When `assemble_v2_4.py` and `train_v2_4.py` are written (Stage 4/5
  future work), they must follow the MUST #26 pattern (dynamic
  `RAW_FEATURES` binding, strict env gate, audit column) and MUST #27
  pattern (dynamic col_count, width assertion, version cross-check)
  from the start.
- Optionally: preemptively patch `assemble_pilot_data.py` and
  `run_attention_experiments.py` as reference implementations that
  lock in the pattern. Future scripts clone from them.

### 2.3 Subtle sub-contradiction — `train_v2_3_1.py` + `train_v2_3_2.py` ARE on origin

`river-rats-core/train_v2_3_1.py` and `train_v2_3_2.py` exist on origin
and would be the closest templates for `train_v2_4.py`. I did NOT read
them during blueprint v2 or supplement drafting. If they have similar
hardcoded column counts, they're also within MUST #27 scope as pattern
references. Verification needed.

---

## 3. Minor contradictions

### 3.1 Manifest reference staleness in supplement

My supplement at `3166759` repeatedly references "manifest v1.9" in
its Stage 4 gate cross-references. Origin manifest is v1.10. Manifest
v1.10's changelog explicitly states: "Manifest references corrected
throughout."

**Impact:** cosmetic. The gate content is identical between v1.9 and
v1.10; only the version label changed. Fix: bump references in
supplement v2.2 amendment.

### 3.2 Labelling prompt version in production labelling

Phase 4 Labelling Report (2026-04-17) states 470 hands labelled with
the **v3 prompt** (commit `3dfc35f`), not v3.1. My supplement
referenced `gto_labeller_v3.1.md` as "current production labelling
prompt".

**Impact:** naming. v3.1 is the most recent file in `prompts/`; v3
was the version actually used for the last production labelling round.
Stage 3's v3.2 derives from v3.1 per manifest. Update supplement's
"current production" phrasing: v3.1 is the most-recent-authored
version; v3 was the last production-run version.

### 3.3 `narrow_by_action_history` line numbers

Supplement's MUST #3 patch references `narrow_by_action_history` body
at lines 695–843. I spot-checked origin and that matches. No drift.

---

## 4. State items that surprised me

### 4.1 Stage 2 COMPLETE doc extremely well-specified

`BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md` documents 6 applied
modifications from the GTO reviewer. Line 1-80 sample I read confirms
the retraction reasoning: KB §1.11 multi-signal resolution rule is
already there ("nut_made_block_pct − (flush_draw_block_pct + straight_draw_block_pct) / 2 > 0.15, **net CALL lean**... do not tag blocker features as PRIMARY in this case"). This is the exact PRIMARY-tagging guidance that an attention-training labeller needs.

### 4.2 Manifest v1.10 is a self-correcting commit

Its v1.10 changelog entry directly states: "orchestrator wrote v1.9
without reading project state on GitHub" and acknowledges the Section
number error. This is the same discipline failure this grounding
directive exists to fix. Good case study.

### 4.3 Exp 3 (pilot-20) was supervised attention training on 20 hands

Phase 4 Labelling Report (470 hands) is production labelling; Exp 3
(20 hands) was a supervised-attention experiment. The 54 attention
flags in `pilot_20_attention.csv` came from the 20 pilot labellers,
not from the 470-hand production labelling round. So MUSTs #26 + #27
when applied to Stage 4 re-label need to handle the production
labelling output format, which may differ from the pilot format.
I did not verify the production labelling output format during
grounding — additional verification needed.

---

## 5. Clarifications needed before reconciliation pass #2

### Q32 (HIGH) — MUST #26 target scope

Two framings; I need orchestrator to pick:

- **(A)** Preemptively patch `assemble_pilot_data.py` +
  `assemble_v23_clean.py` (etc.) as reference implementations;
  document the pattern so `assemble_v2_4.py` (Stage 4 future work)
  clones it cleanly.
- **(B)** MUST #26 is purely prescriptive — a rule that the
  future `assemble_v2_4.py` must follow. No current-file edits. Flag
  the pattern in a new file `docs/ASSEMBLER_PATTERN.md`. Stage 4
  terminal owns applying it when writing the v2.4 assembler.
- **(C)** Hybrid — patch `assemble_pilot_data.py` as reference;
  future `assemble_v2_4.py` clones. Stage 4 assembler gates on the
  pattern during review.

Recommend **(C)** for quality-default: patch the existing reference
implementation (cheap; small; visible) AND document the pattern so
Stage 4 can't drift.

### Q33 (HIGH) — MUST #27 target scope

Same question for `run_attention_experiments.py` vs future
`train_v2_4.py`. Also: `train_v2_3_1.py` and `train_v2_3_2.py` exist
on origin — should they be audited for the same hardcoded-count
pattern as reference cases?

Recommend: audit v2_3_1 and v2_3_2 trainers during first 30 minutes
of commit 11B work; if they share the pattern, patch them as
reference implementations.

### Q34 (MEDIUM) — Push supplement now vs fold into v2.2 amendment

My v2.1 supplement at `3166759` is local-only. Two paths:

- **(A)** Push supplement now so reviewer panel can see it; follow
  with a v2.2 amendment doc addressing §§2–3 above.
- **(B)** Amend supplement in-place by committing a fix on top of
  `3166759`, then push the combined. Keeps review trail to one
  supplement document.
- **(C)** Supersede supplement with a v2.2 document that incorporates
  fixes; reviewer panel sees v2 + v2.2 (two docs). v2.1 becomes
  obsolete.

Recommend **(B)** — fix-forward on the supplement, then push, then
reviewer panel reviews blueprint v2 + final supplement as a pair.
Cleanest single-supplement pattern.

### Q35 (MEDIUM) — Production labelling output format vs pilot format

Did not verify during grounding: does the Phase 4 production labelling
pipeline write the same `attention_flags` dict schema as
`pilot_20_enriched.jsonl`? If differs, MUST #26's strict-env gate
fires at a different layer (the production assembler) than my
supplement targets.

Resolution: read 1 production-labelled JSONL record; diff against
pilot schema; report in first 30 minutes of commit 11A.

---

## 6. Proposed blueprint v2.2 amendment (if orchestrator confirms §5)

### 6.1 Amendments to v2.1 supplement

- Bump manifest references from v1.9 to v1.10 throughout
- Reframe MUST #26 + #27 per chosen Q32/Q33 framing:
  - If (C): patch `assemble_pilot_data.py` as reference + document
    pattern; reframe BEFORE/AFTER blocks to target pilot code, not
    Stage 4 production code
- Clarify labelling prompt versioning: v3.1 = most-recent-authored;
  v3 = last-production-run; Stage 3 v3.2 derives from v3.1
- Add verification items for `train_v2_3_1.py` + `train_v2_3_2.py`
  pattern audit

### 6.2 No amendments needed to blueprint v2 base (8bb0f9f)

Grounding confirmed 13 of 14 files match blueprint v2 BEFORE blocks
cleanly. No HEAD drift at line ranges cited. No contradictions
surface. Blueprint v2 base is solid.

### 6.3 New questions added to reconciliation pass #2 Q-list

Q32, Q33, Q34, Q35 appended to blueprint v2 §13's existing Q-list
and supplement's §6 Q27–Q31.

Total questions for reconciliation pass #2: 14 (Q1–Q14 from blueprint
v1 reconciliation already resolved; Q15–Q19 resolved; Q20–Q26 from v2;
Q27–Q31 from supplement; Q32–Q35 from grounding).

---

## 7. Reviewer panel dispatch — NOT YET

Per directive: "NO reviewer panel dispatch until you confirm grounding
+ raise clarifications."

Grounded: §1.
Clarifications raised: §5.
Amendments proposed: §6.

**Standing by for orchestrator responses to Q32–Q35** (or direct
redirects) before reviewer panel dispatch. Reviewer prompts will be
updated per directive to use `git show origin/master:<path>` rather
than local reads.

---

## 8. Discipline reflection (short)

Grounding discipline caught one real substantive contradiction (§2)
that would have otherwise made it into the reviewer panel and wasted
that review pass. Worth the pre-flight. Memory rule
`feedback_github_is_state_not_local.md` already indexed from an
earlier session — it was in effect but I didn't apply it to
`assemble_pilot_data.py` specifically (I verified file existence but
didn't read the docstring to confirm scope). Lesson: file existence
≠ file role. Verify both before citing as a patch target.

No code edits. Standing by.
