---
date: 2026-05-05
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #142 amended (12.5E-C LABELS FINAL via Opus tier-up cross-check 20/20) — APPROVE; 1 NIT
severity: NIT (1); no HIGH; no MEDIUM; no BLOCKER
status: FLAG → APPROVE for merge
test-class: TC-23 (diff scope) + TC-23-CONTENT (v3.4 verbatim) + V-Source-1/3/4 (citation existence) + dispatch §"NEW: Cross-check report integrity" + dispatch §"NEW: Label-final invariance"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 4th successive cycle solo-routed)
---

# QC Review — PR #142 amended (12.5E-C LABELS FINAL): APPROVE

## Headline

**APPROVE PR #142 (amended) for merge.** All 5 audits per current operative dispatch (PR #146 master `3914fea`) clear cleanly. v3.4 Fix 2.1.1 = bit-for-bit match with PR #144 spec. Cross-check report on master has explicit 20/20 + verdict + per-cohort table + H-FEAT primary load-bearing test results. Labels byte-identical between original BLOCKED commit and amendment commit (LABELS FINAL invariance preserved). One NIT-class V-X4 observation (preserved-original section cites old BLOCKED filename; rename documented elsewhere in same report).

QC FLAG-only role per CLAUDE.md; merge gate decided by orchestrator + (no separate gto-expert team per `feedback_river_rats_team_structure.md`) + owner read.

## Authority chain note (operative dispatch)

The original 12.5E-C dispatch (PR #140 master `e7d7843`) prescribed 5 audits including 3-file scope + Sonnet pricing + PILOT_599/600 RAISE-required. That dispatch has been **superseded 5 times**:

| PR | master | superseding action |
|---|---|---|
| #140 | `e7d7843` | original 12.5E-C dispatch (Sonnet × 5; $120; v3.3) |
| #141 | `ce1528a` | upgrade to Opus 4.7 × 5; cap $200 |
| #143 | `ddc812e` | REDESIGN to pilot (14 manuals, $30) → gate → full (96 parametric, $170) |
| #144 | `45be508` | accept 110 Sonnet labels + add v3.4 doc; T1 deferred |
| #145 | `c299bab` | Opus tier-up cross-check (builder pipeline) before labels-final |
| **#146** | **`3914fea`** | **orchestrator-side Opus cross-check 20/20 — LABELS FINAL; current operative authority** |

PR #146 §"QC stream" lines 99-107 prescribes the **revised 5 audits** + filename `REVIEW_QC_PHASE125E_C_AMEND_FINAL_*.md`. This audit follows PR #146; the old PR #140 audit list is stale.

## Sub-axis verification (all PASS)

PR #142 amended head: `2de166f61304ea261c29d742b6ccada62e97bc13`. Two commits: original BLOCKED (`4e4a731`) + amendment (`2de166f` — "LABELS FINAL... v3.4 added... report renamed BLOCKED → RESOLVED"). Merge-base: `e7d7843` (= PR #140 dispatch SHA).

### Audit 1 — Diff scope ✅ CLEAN

**Dispatch lines 53-64:** *"exactly 6 files in PR diff (was 9 in PR #145; -3 because no pipeline cross-check files)"*

| File | additions | deletions | category |
|---|---|---|---|
| `data/corpus_revision_125e_labels_2026-05-05.jsonl` | 110 | 0 | consensus labels (NEW; UNCHANGED in amendment) |
| `data/corpus_revision_125e_labels_raw_2026-05-05.jsonl` | 550 | 0 | raw 5-labeller (NEW; UNCHANGED in amendment) |
| `prompts/gto_labeller_v3.4.md` | 954 | 0 | v3.4 prompt (NEW per PR #144 spec) |
| `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | 300 | 0 | report (RENAMED from BUILDER_BLOCKED_*) |
| `scripts/collect_mass_labels.py` | 18 | 3 | glob refactor (UNCHANGED in amendment) |
| `scripts/dispatch_mass_labelling.py` | 78 | 21 | version-agnostic refactor (UNCHANGED in amendment) |
| **Total** | **2010** | **24** | **6 files** ✓ |

- File count = 6 ✓
- BLOCKED report file is NOT present at PR head (clean rename, not duplicate) ✓
- Script refactors authorized: `dispatch_mass_labelling.py` adds `_extract_protocol_version()` + `_filename_safe()` helpers (genuinely version-agnostic per PR #146 description); `collect_mass_labels.py` changes hardcoded `labels_v3_2_*.json` to glob `labels_v*_*.json` (matches PR #146 "glob refactor" exactly). Both authorized by PR #140 line 43 ("if v3.2 is hard-coded anywhere, fix... in this PR's diff") + PR #146 line 59-60 explicit description.
- Path Y discipline: zero edits to `gto_model.py`, `feature_extractor.py`, `reference_evaluator.py`, `train_model.py`, etc. ✓

**Diff scope: CLEAN.**

### Audit 2 — Citation existence ✅ CLEAN (1 NIT advisory)

11 distinct `<dir>/<file>.<ext>` citations extracted from builder report + cross-check report. Existence at master HEAD:

| Citation | Status |
|---|---|
| `prompts/gto_labeller_v3.3.md` | ✅ TRACKED on master |
| `review/comms/MAIN_TERMINAL_PHASE125E_C_LABELLING_DISPATCH_2026-05-05.md` | ✅ TRACKED on master |
| `review/comms/ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md` | ✅ TRACKED on master |
| `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` | ✅ TRACKED on master |
| `scripts/collect_mass_labels.py` | ✅ TRACKED on master |
| `scripts/dispatch_mass_labelling.py` | ✅ TRACKED on master |
| `data/corpus_revision_125e_labels_2026-05-05.jsonl` | NOT-TRACKED on master (NEW in PR #142; will track post-merge) ✓ expected |
| `data/corpus_revision_125e_labels_raw_2026-05-05.jsonl` | NOT-TRACKED (NEW in PR #142) ✓ expected |
| `prompts/gto_labeller_v3.4.md` | NOT-TRACKED (NEW in PR #142) ✓ expected |
| `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | NOT-TRACKED (NEW in PR #142, RENAMED from BLOCKED) ✓ expected |
| `review/comms/BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md` | NOT-TRACKED ⚠️ — old filename, renamed away (see NIT-1 below) |

The 4 NEW-in-PR citations (labels jsonls × 2, v3.4, RESOLVED report) are correctly NOT-TRACKED at master pre-merge — they'll be tracked post-merge.

The BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH citation is the rename-source: file existed at original BLOCKED commit (`4e4a731`); renamed to `BUILDER_REPORT_*RESOLVED_*` in amendment commit (`2de166f`); does NOT exist at PR head or master HEAD. See NIT-1.

**Citation existence: CLEAN with 1 NIT advisory.**

### Audit 3 — v3.4 prompt verbatim match ✅ BIT-FOR-BIT MATCH

**Dispatch line 103:** *"diff Fix 2.1.1 section against PR #144 spec character-for-character"*

**Method:** extracted PR #144 dispatch spec (between code fences in `MAIN_TERMINAL_PHASE125E_C_ACCEPT_LABELS_V34_2026-05-05.md`, 30 content lines) + extracted v3.4 inserted Fix 2.1.1 section (v3.4 lines 880-909, 30 content lines) + ran `diff`.

```
$ diff /tmp/spec_clean.txt /tmp/v34_clean.txt
(no output — files identical)
BIT-FOR-BIT MATCH ON 30 CONTENT LINES ✓
```

v3.3 base: 923 lines; v3.4 total: 954 lines; delta: 31 lines (30 content + 1 trailing blank). Clause (e) wording, calibration anchor citations (PILOT_599 RAISE / PILOT_600 CALL), 0.05 floor specification — **all character-for-character identical to dispatch spec**.

**v3.4 verbatim: BIT-FOR-BIT MATCH.**

### Audit 4 (NEW) — Cross-check report integrity ✅ CLEAN

**Dispatch line 104:** *"verify `ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md` exists on master post-merge and contains the 20-hand agreement table + verdict"*

| Check | Result |
|---|---|
| File exists on master HEAD | ✅ TRACKED via PR #146 |
| 20 cohort entries in body | ✅ T5_CALL × 4 (PILOT_542/543/544/600), T5_RAISE × 4 (PILOT_539/540/541/599), T1_first6 × 6 (PILOT_495..500), T7_CALL × 3 (PILOT_559/560/561), T7_RAISE × 3 (PILOT_563/564/565) = 20 |
| Agreement table present | ✅ "pilot_hand_id \| cohort \| sonnet \| opus \| agree?" with 20 rows |
| Per-cohort summary | ✅ T5_CALL 4/4, T5_RAISE 4/4, T1_first6 6/6, T7_CALL 3/3, T7_RAISE 3/3 = 20/20 |
| Load-bearing H-FEAT primary explicit | ✅ PILOT_599 (T5 H-FEAT primary) RAISE/RAISE match Y; PILOT_600 (T5 H-FEAT counter-anchor) CALL/CALL match Y |
| Pre-specified gate criteria reference | ✅ "≥18/20 agreement AND both H-FEAT primaries match → LABELS FINAL" cited |
| Final verdict | ✅ "**Final verdict: LABELS FINAL**" + "Agreement: 20/20 (well above 18/20 threshold). Both H-FEAT primaries match. No divergences." |

**Cross-check integrity: CLEAN.**

### Audit 5 (NEW) — Label-final invariance ✅ BYTE-IDENTICAL

**Dispatch line 105:** *"verify the 110 Sonnet labels and 550 raw labels are byte-identical to what was in PR #142 prior commit; any drift indicates label tampering"*

Computed sha256 of label files at original BLOCKED commit (`4e4a731`) vs amendment commit (`2de166f`):

| File | line count | sha256 (BLOCKED) | sha256 (amended) | match |
|---|---|---|---|---|
| `corpus_revision_125e_labels_2026-05-05.jsonl` | 110 | `406560de...c0a12` | `406560de...c0a12` | ✅ **BYTE-IDENTICAL** |
| `corpus_revision_125e_labels_raw_2026-05-05.jsonl` | 550 | `d6ea183e...685b` | `d6ea183e...685b` | ✅ **BYTE-IDENTICAL** |

LABELS FINAL invariance preserved. Zero drift between commits — amendment did NOT modify the 110 consensus labels or 550 raw labels (per dispatch line 91 stop condition "Any change to the 110 labels → STOP").

**Label-final invariance: CLEAN.**

## NIT-1 — V-X4 carryforward in preserved-original section

**Evidence:** PR #142 builder report line 151:

> | `review/comms/BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md` | NEW | This BLOCKED report (replaces success-path BUILDER_REPORT) |

This citation is in the §"What the BLOCKED PR ships" table that was preserved verbatim from the original BLOCKED commit. Post-rename, the file at that path no longer exists — the report itself is now at `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md`.

**Mitigation:** The same builder report at line 280 explicitly documents the rename:

> | `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | RENAMED + UPDATED | renamed from `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md`; preserved all empirical analysis; added §"Resolution" + §"v3.4 sanity check" + §"Amendment file diff" sections |

So a careful reader can reconcile (preserved-original section claims one file; amendment-file-diff section documents the rename). But a skim-reader of just the §"Original" section sees a stale citation.

**Same V-X4 family as past findings:**
- PR #126 NIT-1: BLOCKED comm "Three files NOT four" while ship reality was 4
- PR #131 MEDIUM-2: builder claimed "fixed wording-cleanup" but trainer line 1371 was missed
- PR #136 (no V-X4 issue this cycle — clean)
- This cycle (PR #142) NIT-1: preserved-original section cites pre-rename filename

**Why this is NIT not MEDIUM:** the pattern is now well-established and the report itself surfaces the resolution at line 280. This is the "preserve original framing for posterity" pattern that PR #146 dispatch lines 78-85 explicitly authorized — the stale citation is a side-effect of preservation, not an active claim.

**Suggested fix-forward (advisory):** in 12.5E-D or 12.5E-E follow-up, either:
- Add a header note to §"Original" sections like "**Note: filename has since been renamed to `*RESOLVED*`. See §'Amendment file diff' below.**"
- OR explicitly mark preserved-original-section file references with a `(historical, see Amendment §)` annotation

Severity: NIT.

## Old-dispatch audits (PR #140) — for the record

The user prompt to QC earlier today was based on PR #140 dispatch which has been superseded 5 times. Two of the old audits are not in the current dispatch but may be of interest for the synthesis. Brief notes for the record:

- **Old Audit 4 — Cost reconciliation (≤$120, Sonnet 4.6 pricing, 550 calls):** builder report headline says "Cost: well under $120 cap (Sonnet 4.6 subagent token consumption; not direct-API per-call)." Run was via subagent with token consumption, not direct API per-call billing — quantitative per-call breakdown not applicable to the actual dispatch path. Qualitative claim "well under $120" is unverifiable from PR data alone but consistent with subagent token usage at this scale. Not surfaced as a finding because PR #146 dispatch dropped this audit.
- **Old Audit 5 — T5 H-FEAT primary correctness (PILOT_599 + 600 = RAISE):** Under v3.3 wording, PILOT_600 = CALL would have been a STOP condition. Under v3.4 wording with clause-e floor (`villain_air_pct >= 0.05`), PILOT_600's air = 0.020 correctly fails the carve-out → CALL is GTO-correct. Both Sonnet × 5 + Opus single-shot agree. Path B works empirically when the implicit floor is documented. NOT a finding (the entire amendment chain resolves this correctly).

## What QC did NOT audit (scope partition)

- **Per-hand poker correctness** of the 110 consensus labels — orchestrator's Opus cross-check (PR #146) did this on 20 of 110 hands, finding 20/20 agreement with Sonnet × 5. QC verifies the cross-check happened + verdict integrity, not the underlying poker judgment.
- **v3.4 Fix 2.1.1 logical correctness** (does it actually catch MW-47 RAISE while preserving the air-floor for CALL?) — orchestrator's cross-check confirmed empirically (PILOT_599 RAISE / PILOT_600 CALL both match design under v3.4). QC verifies the wording matches dispatch spec; orchestrator verified the wording matches GTO theory.
- **TC-26 V-Integration-Trace on the dispatch_mass_labelling.py refactor** — not in dispatch scope. The script changes are config refactor (version-agnostic prompt resolution + glob filename pattern), not fix-claim code paths requiring integration tracing. Could be picked up at 12.5E-D corpus QC gates if needed.

## Test class implication

- **TC-23 (6-file-scope sub-vector) demonstrated cleanly** — amended-PR with mixed UNCHANGED + NEW + RENAMED file types. Pattern reproducible.
- **TC-23-CONTENT verbatim** — third successive cycle activation (PR #131 hybrid weighting + PR #136 v3.3 carve-out + this PR v3.4 Fix 2.1.1). Pattern stable; the dispatch-verbatim-spec → builder-implements-bit-for-bit pipeline is working.
- **NEW: TC-X-LABEL-FINAL-INVARIANCE** sub-vector queue-worthy. Sha256 byte-comparison between commits is a clean check for label-tampering invariants. Activates when a dispatch declares an invariant ("LABELS FINAL — no further modifications") and a subsequent amendment touches the same data files.
- **NEW: TC-X-CROSSCHECK-INTEGRITY** sub-vector queue-worthy. Verifies an orchestrator-side cross-check artifact contains the verdict structure (cohort table, agreement count, gate-criteria-reference, explicit verdict). Activates whenever a dispatch declares cross-check verification (vs builder-side pipeline verification).
- **NIT-1 pattern recurrence-watch** — preserved-original-section staleness is V-X4 family; if it recurs, formalize the "preserve-with-explicit-historical-marker" curative.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **4th successive cycle solo-routed** (PR #126 → PR #131 → 12.5E-B amendment → 12.5E-C amendment). Orchestrator's tier-up cross-check via subagent (PR #146) was orchestrator-side verification, NOT a parallel QC dispatch. Distinction holds: QC continues SOLO-routed for pre-merge mechanical/structural audit; orchestrator-side subagent cross-checks for content-correctness verification are a separate workflow.

The methodology lesson at PR #146 line 144 ("orchestrator-side cross-check is valid for pilot-scale verification") is process-design-class, not QC-routing — separate concerns.

## References

- PR #142: https://github.com/beytell1-sketch/river-rats-v2/pull/142
- PR #142 amended head: `2de166f61304ea261c29d742b6ccada62e97bc13`
- PR #142 original BLOCKED commit: `4e4a731` (preserved in git history; renamed to RESOLVED in amendment)
- Current operative dispatch: `MAIN_TERMINAL_PHASE125E_C_LABELS_FINAL_2026-05-05.md` (PR #146, master `3914fea`)
- v3.4 spec source: `MAIN_TERMINAL_PHASE125E_C_ACCEPT_LABELS_V34_2026-05-05.md` (PR #144, master `45be508`)
- Cross-check raw output: `review/comms/ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md` (master)
- Authority chain: PR #140 → #141 → #143 → #144 → #145 → **#146** (current)
- QC test class registry: `~/river-rats-qc/learning/test_class_registry.md` (TC-23 family)
- Memory: `feedback_qc_routing_when_standalone_active.md` (4th cycle confirmation), `feedback_pilot_first_for_long_jobs.md` (tier-up sub-rule), `feedback_river_rats_team_structure.md` (3-party model)

## Status

**APPROVE PR #142 (amended) for merge.** All 5 audits per current operative authority (PR #146) PASS. 1 NIT-class V-X4 advisory (preserved-original-section stale citation; mitigated by §"Amendment file diff" in same report).

QC-side gate cleared. Awaiting orchestrator merge → 12.5E-D dispatch (corpus QC phase per design §8.D + queued cleanup items: NIT-1 PLAN §3.T8, PILOT_595 design_note cosmetic, T1 deferral documentation).
