---
date: 2026-05-05
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder) · GTO-EXPERT (re-review) · ML-ARCHITECT (advisory)
re: PR #136 amended (12.5E-B Path B / v3.3 carve-out) — APPROVE; 1 NIT (design plan §3 vs dispatch reconciliation)
severity: NIT (1); no HIGH; no MEDIUM; no BLOCKER
status: FLAG → APPROVE for merge
test-class: TC-23 (diff scope) + TC-23-CONTENT (v3.3 carve-out verbatim) + V-Source-1/3/4 (citation existence) + dispatch §"NEW: Convention uniformity" + dispatch §"NEW: v3.3 verbatim match"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — orchestrator solo-routed; no parallel general-purpose subagent dispatched this cycle)
---

# QC Review — PR #136 amended (12.5E-B Path B): APPROVE

## Verdict

**APPROVE PR #136 (amended) for merge.** All 5 dispatch-required audits clear cleanly. Path B discipline holds (T5 hand definitions structurally unchanged; convention applied uniformly across all 14 manuals + 96 parametric). v3.3 Fix 2.1 carve-out matches directive spec character-for-character. Distribution exactly hits the dispatch's parametric count spec. Zero collisions, zero baseline overlap, zero non-hero actions.

One NIT-class observation about plan-vs-dispatch reconciliation; does not block.

QC FLAG-only role per CLAUDE.md; merge gate decided by orchestrator + gto-expert re-review + (optional) ml-architect advisory + owner read.

## Audit scope (per `MAIN_TERMINAL_PHASE125E_B_AMEND_PATH_B_2026-05-05.md` §"QC stream")

5 audits — 3 standard (diff scope, citation existence, distribution sanity) + 2 NEW for the amendment (convention uniformity, v3.3 carve-out verbatim).

PR #136 amended head audited: `54f024f7bf1e1389a195419a16aa82644a0ef6d3` (force-pushed amendment over original `d65758c`). Merge-base: `6b991b2` (= PR #135 = 12.5D' synthesis ADDENDUM merge SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 5 files (was 4); the v3.3 prompt is the +1; no other source-surface edits"*

| File | additions | deletions | category |
|---|---|---|---|
| `scripts/build_corpus_revision_125e_situations.py` | 1796 | 0 | situation generator (UPDATE) |
| `data/corpus_revision_125e_situations_2026-05-04.jsonl` | 96 | 0 | parametric output (REGEN) |
| `data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl` | 14 | 0 | manual output (REGEN) |
| `prompts/gto_labeller_v3.3.md` | 923 | 0 | v3.3 prompt (NEW) |
| `review/comms/BUILDER_REPORT_PHASE125E_B_SITUATION_GENERATION_2026-05-04.md` | 308 | 0 | builder report (UPDATE) |
| **Total** | **3137** | **0** | 5 files / additions-only |

- File count = 5 ✅
- File list matches dispatch lines 32-38 prescription ✅
- Zero out-of-scope edits (verified via `git diff master..pr-136-audit --name-only` regex exclusion) ✅
- All-additions; no deletions on existing source surfaces (the .jsonls are new, the script is amended via force-push to a new file shape, the v3.3 prompt is new, the report is new) ✅

### Path B discipline check — T5 hands UNCHANGED

Compared T5 hands (PILOT_599, PILOT_600) between original PR #136 commit `d65758c` and amended commit `54f024f`:

| field | PILOT_599 (orig) | PILOT_599 (amended) | PILOT_600 (orig) | PILOT_600 (amended) |
|---|---|---|---|---|
| hero_cards | AsQs | AsQs ✓ | AhKh | AhKh ✓ |
| board | KsJs6c | KsJs6c ✓ | JhTh5c | JhTh5c ✓ |
| street | flop | flop ✓ | flop | flop ✓ |
| hero_position | BB | BB ✓ | BB | BB ✓ |
| villain_positions | [HJ, CO, BTN] | [HJ, CO, BTN] ✓ | [HJ, CO, BTN] | [HJ, CO, BTN] ✓ |
| pot | 22.5 | 22.5 ✓ | 22.5 | 22.5 ✓ |
| to_call | 6.0 | 6.0 ✓ | 6.0 | 6.0 ✓ |
| facing_bet | True | True ✓ | True | True ✓ |
| prior_actions | full-history | hero-only (convention applied uniformly per Path B) | full-history | hero-only (convention applied uniformly per Path B) |

Structural hand definitions UNCHANGED ✅. Only the `prior_actions` convention was normalized to hero-only — applied uniformly across all 14 manuals + 96 parametric per dispatch §"Convention" line 56. T5 design intent (testing MW-47 family RAISE OOP into bet+call multiway) preserved.

Per dispatch line 115 stop condition ("T5 hand definitions changed in any way → STOP"): convention normalization is NOT a hand-definition change. The hand DEFINITION (cards/board/position/equity context) is what Path B preserves; the prior_actions array is the action-history format.

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

8 cited paths + 1 user-memory file all resolve at master HEAD:

| Citation | Resolution |
|---|---|
| `prompts/gto_labeller_v3.2.md:792-833` (KB §1.7 OVERRIDE source for v3.3) | ✅ TRACKED; lines 792-839 contain the KB §1.7 carve-out OVERRIDE section (dispatch's "line 833" is approximately the section content end; exact section span is 792-839) |
| `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` | ✅ exists (1731 bytes); contains MW-47 RAISE solver-corrected anchor |
| `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | ✅ TRACKED |
| `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md` | ✅ TRACKED |
| `review/comms/MAIN_TERMINAL_PHASE125E_DISPATCH_2026-05-04.md` (PR #133) | ✅ TRACKED |
| `review/comms/MAIN_TERMINAL_PHASE125E_B_AMEND_PATH_B_2026-05-05.md` (PR #137) | ✅ TRACKED |
| `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (12.5E-A design) | ✅ TRACKED |
| `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md` (cited in builder report) | ✅ TRACKED |
| `scripts/build_corpus_revision_500_hand.py` (existing pipeline reference) | ✅ TRACKED |
| `scripts/collect_mass_labels.py` (downstream 12.5E-C consumer) | ✅ TRACKED |
| `scripts/dispatch_mass_labelling.py` (downstream 12.5E-C consumer) | ✅ TRACKED |

**Citation existence: CLEAN.**

## Audit 3 — Distribution sanity ✅ CLEAN

**Dispatch line 137 spec:** *"verify 110 hands match design §3 template counts within ±1 hand (unchanged by amendment)"*

**Authority chain note:** PLAN §3 cites per-template totals `12+10+10+12+12+8+10+36 = 110` (combined). Dispatch PR #133 line 99 cites `12+10+10+12+12+8+10+22 = 96` (parametric only) plus 14 manuals = 110 combined. **Dispatch supersedes plan as the operative directive.** Builder report line 71 explicitly acknowledges: *"Compressed from design §3 T8=36 per dispatch's parametric-output spec."* See NIT-1 below.

### Distribution measurement

| metric | observed | expected (dispatch) | match |
|---|---|---|---|
| Manual canonical count | 14 | 14 (T1-T7 × 2) | ✅ |
| Parametric count | 96 | 96 | ✅ |
| Combined total | 110 | 110 | ✅ |
| pilot_hand_id range | PILOT_495..PILOT_604 | PILOT_495..PILOT_604 | ✅ |
| pilot_hand_id contiguous | yes | yes | ✅ |
| Internal collisions | 0 | 0 | ✅ |
| Overlap with baseline 494 | 0 | 0 | ✅ |

### Per-template parametric counts (dispatch line 99 spec)

| template | observed | dispatch spec | within ±1? |
|---|---|---|---|
| t1 (MW-25 family) | 12 | 12 | ✅ exact |
| t2 (MW-40 family) | 10 | 10 | ✅ exact |
| t3 (MW-42 family) | 10 | 10 | ✅ exact |
| t4 (MW-45 / slowplay-set) | 12 | 12 | ✅ exact |
| t5 (MW-47 / NFD-RAISE-OOP) | 12 | 12 | ✅ exact |
| t6 (MW-33-adj / monster-delayed) | 8 | 8 | ✅ exact |
| t7 (MW-17 / NFD+overcards CALL) | 10 | 10 | ✅ exact |
| t8 (controls) | 22 | 22 | ✅ exact |
| **Total** | **96** | **96** | ✅ |

All 8 templates hit the dispatch parametric spec **exactly** (variance = 0; well within ±1 tolerance). Combined per-template (manual + parametric):

| template | manual | parametric | combined |
|---|---|---|---|
| T1 | 2 | 12 | 14 |
| T2 | 2 | 10 | 12 |
| T3 | 2 | 10 | 12 |
| T4 | 2 | 12 | 14 |
| T5 | 2 | 12 | 14 (H-FEAT primary test population complete) |
| T6 | 2 | 8 | 10 |
| T7 | 2 | 10 | 12 |
| T8 | 0 | 22 | 22 |
| **Total** | **14** | **96** | **110** |

### Discriminative-axis verification (orthogonal cross-check)

Builder report lines 92-108 claim per-template discriminative-axis hit-rates (the actual learning-value check, beyond raw count):

| template | discriminative axis | observed hit-rate |
|---|---|---|
| T1 | `is_monotone=1 ∧ has_flush_draw=1 ∧ num_opponents≥3 ∧ villain_aggression_count=0` | 14/14 ✓ |
| T2 | `is_made_hand=1 ∧ is_rainbow=1 ∧ villain_checked_back=1 ∧ num_opponents≥2` | 12/12 ✓ |
| T3 | `street=river` | 12/12 ✓ |
| T4 | `is_monster=1 ∧ street=turn ∧ villain_aggression_count≥1 ∧ num_opponents≥2` | 14/14 ✓ |
| T5 | `has_flush_draw=1 ∧ nut_flush_block=1 ∧ num_callers_to_bet≥1 ∧ is_ip=0` | 14/14 ✓ (H-FEAT primary; **all 14 carry `nut_flush_block=1`**) |
| T6 | `is_monster=1 ∧ villain_aggression_count≥1` | 10/10 ✓ |
| T7 | `has_flush_draw=1 ∧ nut_flush_block=1 ∧ is_ip=0 ∧ num_opponents∈{1,2}` | 11/12 (1 K-high FD intentional non-blocker control) |

I did NOT independently re-verify these claims via re-extracting features (out of scope; that's a deeper TC-26 V-Integration-Trace check that would be appropriate for the 12.5E-D corpus QC gates, not this 12.5E-B audit). Builder claim is internally consistent with the dataset design.

**Distribution sanity: CLEAN.**

## Audit 4 (NEW) — Convention uniformity ✅ CLEAN

**Dispatch line 138:** *"empirically verify all 110 `prior_actions` use hero-only convention; zero hands have non-hero actions"*

Programmatic check: parsed every `prior_actions` array across both jsonls; for each action string, extracted the actor (token after `street: `) and compared against the row's `hero_position`. Counted any actions with actor ≠ hero_position.

| dataset | rows | violations |
|---|---|---|
| Manual canonicals | 14 | 0 |
| Parametric | 96 | 0 |
| **Total** | **110** | **0** |

T5 sample verification:
- PILOT_599 (hero=BB): `prior_actions = ["preflop: BB call", "flop: BB check"]` — both BB (hero) ✓
- PILOT_600 (hero=BB): `prior_actions = ["preflop: BB call", "flop: BB check"]` — both BB (hero) ✓

**Convention uniformity: CLEAN. Zero violations of 110.**

## Audit 5 (NEW) — v3.3 carve-out wording verbatim match ✅ BIT-FOR-BIT MATCH

**Dispatch line 139:** *"diff the v3.3 Fix 2.1 section against the directive's verbatim spec; character-for-character; if any drift, HOLD until builder conforms"*

**Method:** extracted the dispatch verbatim spec (lines 63-100 of `MAIN_TERMINAL_PHASE125E_B_AMEND_PATH_B_2026-05-05.md`, 38 content lines excluding the `````` markdown fence delimiter) + extracted the v3.3 inserted Fix 2.1 section (v3.3 lines 841-878, 38 content lines) + ran `diff`. Result:

```
$ diff /tmp/dispatch_spec_clean.txt /tmp/v33_clean.txt
(no output — files identical)
```

**v3.3 Fix 2.1 = dispatch spec, character-for-character, all 38 content lines.**

### v3.3 = v3.2 + Fix 2.1 structural check

- v3.2 base: 884 lines
- v3.3 total: 923 lines
- Diff: insertion at v3.2 line 840 of 39 lines (38 content + 1 blank closer) → v3.3 lines 841-879
- Insertion location: end of KB §1.7 carve-out OVERRIDE section content, before the `---` divider that separates it from `## Pass 2 Review`
- Dispatch said "after current line 833" — actual section ends at line 839; insertion at line 840 places Fix 2.1 within the KB §1.7 OVERRIDE section as semantically intended

**Note on "line 833" cited in dispatch:** the dispatch's literal line citation was approximate (the actual KB §1.7 OVERRIDE section content runs through line 839, not 833). The semantic intent (append to KB §1.7 OVERRIDE section) is correctly executed. This is NOT a finding — dispatch wording was approximate; builder did the right thing.

**v3.3 carve-out wording verbatim: BIT-FOR-BIT MATCH.**

## NIT-1 — Plan §3 vs dispatch §3 reconciliation gap (advisory)

**Evidence:** PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md §3 (master `bad1396`, lines 105-181) cites per-template totals:

> T1: 12 / T2: 10 / T3: 10 / T4: 12 / T5: 12 / T6: 8 / T7: 10 / **T8: 36** ⇒ total 110

Dispatch PR #133 line 99 + line 47-48 cite the operative spec:

> *"design §3 template counts (12+10+10+12+12+8+10+22)"* — totaling **96 parametric** + 14 manual = 110 combined

**T8 spec differs:** plan = 36, dispatch = 22. Dispatch supersedes plan as operative directive (per PROCESS_GUIDE convention; dispatch is the executable directive). Builder report line 71 explicitly notes the compression: *"Compressed from design §3 T8=36 per dispatch's parametric-output spec (12+10+10+12+12+8+10+22=96)."*

**Why it matters:** A reviewer reading PLAN §3 first (e.g., a future cycle's builder, or a reviewer cross-referencing the design plan) and trying to verify against §3 directly would see T8=22 in the corpus and read it as -14 from spec — a false positive HOLD. The dispatch's compression rationale (96 parametric + 14 manual = 110 combined) is correctly the authoritative spec, but PLAN §3 wasn't updated to reflect it.

**Suggested fix-forward (advisory):** in 12.5E-D or 12.5E-E follow-up, amend PLAN §3 T8 entry from "36 sampled" to "22 parametric (post-dispatch compression to fit 96 parametric + 14 manual = 110 combined target)". Alternatively, add a "Note" pointing readers to dispatch line 99 as the operative spec.

**Severity:** NIT. Substance is correct (builder hits dispatch spec exactly); only the upstream plan reference is stale relative to the dispatch.

This is the same V-X4 / TC-23-CONTENT family pattern as past findings (#18 incident family in `~/river-rats-qc/learning/incident_pattern_library.md`) — but on plan documents rather than builder comms. Less urgent than builder-comm V-X4 (which directly affects PR review readers); this is a "future-cycle reviewer trip hazard."

## What QC did NOT audit (scope partition)

QC's audit deliberately did NOT cover (per dispatch scope; reserved for parallel reviewers):

- **Per-hand poker correctness** of the 14 manual canonicals (PILOT_591..604) — gto-expert re-review per dispatch §"GTO-EXPERT (re-review)" lines 143-159. QC verified the 6 mechanical fixes from the dispatch landed (per spot-check + builder report claims) but did NOT independently verify that PILOT_595 is a valid BTN-IP river decision, PILOT_603 has the correct AhKh/AhQh hero, etc. That's gto-expert's poker-judgment scope.
- **v3.3 Fix 2.1 logical correctness** (does it actually catch MW-47 RAISE while preserving MW-39 CALL?) — gto-expert falsification test per dispatch §"GTO-EXPERT (re-review)" lines 156-158. QC verified verbatim wording match; gto-expert verifies the carve-out predicate's logical correctness on calibration anchors.
- **TC-26 V-Integration-Trace on the situation factory's feature-extraction pipeline** — out of scope for 12.5E-B PR audit (the corpus is data, not code with a fix-claim path). Will be appropriate at 12.5E-D corpus QC gates if needed.

## Test class implication

- **TC-23 (5-file-scope sub-vector)** demonstrated cleanly — convention-amendment + new-file PRs have a precedent for ±1 file count exactness.
- **TC-23-CONTENT (verbatim verbatim diff)** second activation (after PR #131 hybrid weighting) — same pattern, character-for-character match against directive spec. Pattern is reproducible.
- **NEW: TC-X-CONVENTION-UNIFORMITY** (queue-worthy?) — the convention-uniformity check (parse all `prior_actions` for hero-only conformance) generalizes to any future convention-normalization PR. Worth adding as a sub-vector under TC-23 if a similar pattern recurs.
- **NIT-1 pattern (plan-vs-dispatch staleness)** — recurrence-watch. If a future cycle's QC catches the same pattern (operative dispatch supersedes design plan but plan wasn't updated), formalize as a TC-X-PLAN-RECONCILIATION class.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` (saved 2026-05-04) continues to work as intended at 12.5E-B amendment. Orchestrator solo-routed through standalone QC stream. SOLO audit by design. Process improvement from PR #126 holding firm at 3rd successive cycle (PR #131 → 12.5E-B amendment).

## References

- PR #136: https://github.com/beytell1-sketch/river-rats-v2/pull/136
- PR #136 amended head: `54f024f7bf1e1389a195419a16aa82644a0ef6d3`
- PR #136 original head: `d65758c48071c952c4e475540f800ba2d5604dff` (force-pushed over)
- 12.5E-B amendment dispatch: `~/river-rats-v2/review/comms/MAIN_TERMINAL_PHASE125E_B_AMEND_PATH_B_2026-05-05.md` (PR #137, master `10f914b`)
- 12.5E original dispatch: `~/river-rats-v2/review/comms/MAIN_TERMINAL_PHASE125E_DISPATCH_2026-05-04.md` (PR #133, master `bad1396`)
- 12.5E design: `~/river-rats-v2/review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (PR #133)
- v3.2 KB §1.7 OVERRIDE source: `prompts/gto_labeller_v3.2.md:792-839`
- Solver-corrected MW-47 RAISE anchor: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- QC test class registry: `~/river-rats-qc/learning/test_class_registry.md` (TC-23 family + TC-26 + V-Source)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`

## Status

**APPROVE PR #136 (amended) for merge.** All 5 audits PASS. 1 NIT advisory (plan-vs-dispatch reconciliation, future-cycle reviewer trip hazard).

QC-side gate cleared. Awaiting:
- gto-expert re-review per dispatch §"GTO-EXPERT (re-review)" — 14 manual canonicals + v3.3 falsification test
- ml-architect advisory per dispatch §"ML-ARCHITECT (advisory)" — v3.3 prompt vs spec
- Orchestrator merge on all-clear
- 12.5E-C dispatch with v3.3 prompt reference
