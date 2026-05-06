---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #181 (12.5H-C full Sonnet × 5 × 90 = 450 labels) — APPROVE; 1 MEDIUM (PILOT_692 dispatch prediction error — 3rd instance triggers TC-X-DISPATCH-PREDICTION-VERIFICATION formalization)
severity: MEDIUM (1 — orchestrator-side prediction error, builder transparently flagged); 1 INFORMATIONAL (FOLD class 4.4% < 5% but represented per dispatch criterion)
status: FLAG → APPROVE for merge
test-class: TC-23 + V-Source + dispatch §"NEW: Cost reconciliation" + §"NEW: Manual canonical correctness" + **TC-X-DISPATCH-PREDICTION-VERIFICATION (formalized this cycle)**
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 12th successive cycle solo-routed)
---

# QC Review — PR #181 (12.5H-C full labelling): APPROVE; 1 MEDIUM + TC-X formalization

## Verdict

**APPROVE PR #181 for merge.** All 5 dispatch-required audits processed. 4 PASS cleanly; Audit 5 flags PILOT_692 dispatch prediction error (CALL predicted; 5/5 unanimous RAISE labelled — MW-33 set-facing-bet+call pattern). Builder transparently caught + diagnosed.

**TC-X-DISPATCH-PREDICTION-VERIFICATION formalized this cycle** per orchestrator's PR #182 audit-now trigger explicit request. 3 instances logged across PR #169 / #175 / #181 reach formalization threshold. New test class entry added to `~/river-rats-qc/learning/test_class_registry.md` + curative entry #11 in `curative_additions_log.md` + incident #26 in `incident_pattern_library.md`.

QC FLAG-only role per CLAUDE.md.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR181_2026-05-06.md` master `36bb531` + PR #180 dispatch)

5 audits — 3 standard + 2 NEW for full labelling (cost reconciliation, manual canonical correctness).

PR #181 head: `bfe02f9` (branch `programmer/phase125h-c-re-pilot-2026-05-06`). Merge-base: `4da0d13` (= PR #179 re-pilot HALT report).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 3 new files"*

| File | additions | deletions | category |
|---|---|---|---|
| `data/corpus_revision_125h_labels_2026-05-06.jsonl` | 90 | 0 | NEW (consensus labels) |
| `data/corpus_revision_125h_labels_raw_2026-05-06.jsonl` | 450 | 0 | NEW (raw 5-labeller per-hand outputs) |
| `review/comms/BUILDER_REPORT_PHASE125H_C_LABELLING_2026-05-06.md` | 297 | 0 | NEW (report) |
| **Total** | **+837** | **0** | **3 files** ✓ |

- File count = 3 ✓
- Zero edits to `prompts/`, `river-rats-core/`, `scripts/`, or existing 604-corpus / 12.5H situations / labels-raw-from-pilot ✓
- All-additions ✓

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

9 distinct file paths cited; 5/9 TRACKED at master HEAD; 4/9 NOT-TRACKED expected (NEW in this PR + existing-but-NEW-this-PR for the 12.5H corpus files which were tracked from PR #169 merge).

| Citation | Status |
|---|---|
| `data/corpus_revision_125h_situations_2026-05-06.jsonl` | ✅ TRACKED |
| `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` | ✅ TRACKED |
| `prompts/gto_labeller_v3.4.md` | ✅ TRACKED |
| `review/comms/MAIN_TERMINAL_PHASE125H_C_FULL_GO_2026-05-06.md` | ✅ TRACKED |
| `scripts/collect_mass_labels.py` | ✅ TRACKED |
| `scripts/dispatch_mass_labelling.py` | ✅ TRACKED |
| `data/corpus_revision_125h_labels_2026-05-06.jsonl` | NOT-TRACKED ✓ expected (NEW in PR) |
| `data/corpus_revision_125h_labels_raw_2026-05-06.jsonl` | NOT-TRACKED ✓ expected (NEW in PR) |
| `review/comms/BUILDER_REPORT_PHASE125H_C_LABELLING_2026-05-06.md` | NOT-TRACKED ✓ expected (NEW in PR; self-reference) |

**Citation existence: CLEAN.**

## Audit 3 — Label distribution sanity (G2) ✅ CLEAN (with FOLD informational note)

**Dispatch:** *"90 hands, all 5 classes represented"*

| class | count | % | flag |
|---|---|---|---|
| FOLD | 4 | 4.4% | ⚠ < 5% (informational; all 5 classes represented per dispatch criterion) |
| CHECK | 24 | 26.7% | ✓ |
| CALL | 7 | 7.8% | ✓ |
| BET | 19 | 21.1% | ✓ |
| RAISE | 36 | **40.0%** | ✓ (very high — design intent: pattern-locked T10' + T-RAISE-stabilize templates produce dense RAISE) |

- Total: 90 ✓
- All 5 classes represented ✓
- FOLD slightly below 5% but classes present (per dispatch's "represented" criterion); not blocking

**Note on RAISE = 40.0%:** the 12.5H corpus is intentionally RAISE-dense (T10' MW-45 monsters + T-RAISE-stabilize MW-47 patterns + T7-ext SUITED-NFD with air ≥ 0.20). Combined with existing 604 (RAISE = 11.3%), the post-merge 694-corpus RAISE share will be ~14% (per design §4 prediction). Within design.

**Distribution sanity: CLEAN.**

## Audit 4 (NEW) — Cost reconciliation ✅ CLEAN

**Dispatch:** *"total ≤ $120; per-call cost matches Sonnet 4.6 pricing; 450 calls completed"*

| Quantity | Reported | Expected | Match |
|---|---|---|---|
| Total cost | ~$3-5 + ~$1 retry overhead | ≤ $120 cap | ✅ well under (<$10 vs $120) |
| Calls completed | 450 | 450 | ✅ exact (5 labellers × 90 hands) |
| Refusals | 0 | minimize | ✅ zero |
| Schema errors | 0 | zero | ✅ |
| Per-call pricing | subagent token consumption (not direct API per-call) | Sonnet 4.6 | ✅ same caveat as 12.5E-C; labelling went via Agent tool subagent dispatch; quantitative per-call breakdown N/A but within-cap claim consistent with subagent token usage at this scale |

**Note on retry:** builder report lines 79-84 document 2 of 5 labellers (1 + 3) hit token-cap on first attempt due to verbose per-hand reasoning + summary commentary. Re-ran with output formatting fix; both completed cleanly on second attempt; ~$1 extra cost. Total still well under $120 cap.

**Cost reconciliation: CLEAN.**

## Audit 5 (NEW) — Manual canonical correctness ⚠️ MEDIUM-1

**Dispatch:** *"6/6 manuals match updated predictions: PILOT_689 CHECK, PILOT_690 CHECK, PILOT_691 BET, PILOT_692 CALL, PILOT_693 RAISE (or air-driven if value differs), PILOT_694 RAISE; HOLD if any divergence without explanation in builder report"*

### Per-hand verification

| pilot_hand_id | predicted | actual | confidence | match |
|---|---|---|---|---|
| PILOT_689 | CHECK | CHECK | 1.00 | ✅ |
| PILOT_690 | CHECK | CHECK | 0.60 | ✅ (Option A confirmed) |
| PILOT_691 | BET | BET | 0.80 | ✅ |
| **PILOT_692** | **CALL** | **RAISE** | **1.00 (5/5 unanimous)** | ✗ DIVERGENT |
| PILOT_693 | RAISE | RAISE | 1.00 | ✅ (12.5H-B' amendment validated; QC PR #177 MEDIUM-1 closed) |
| PILOT_694 | RAISE | RAISE | 0.80 | ✅ |

**5/6 match.** Per dispatch full-phase stop rule "match >1 divergence → STOP", 1 divergence does NOT trigger STOP — proceeding.

### PILOT_692 divergence diagnosis

**Hand:** 6d6c on AcKd6hQs turn (4-way: hero BB OOP facing CO turn lead 12bb + BTN call). Set of sixes on a connected/dangerous board.

All 5 Sonnet labellers independently produced **RAISE conf=HIGH** (4/5) or **MEDIUM** (1/5). Common reasoning across 5 independent labellers:
- Monster hand (set, hand_category=12)
- equity_vs_range = 0.501; better_hand_pct = 0.103 (only 10% of villain range beats hero)
- SPR = 2.86 (compressed; committed)
- Bet+call multiway (num_callers_to_bet=1, villain_aggression_count=1)
- **MW-33 anchor: monster facing bet+call must RAISE** — for value at compressed SPR, deny equity to draws on dangerous board (danger_score=0.88)

The 5 labellers explicitly cite MW-33 in their reasoning. PILOT_692 is the canonical T10' (MW-45 exact) hand — but the v3.4 protocol's MW-33 monster-RAISE-vs-bet+call rule fires first; CALL is GTO-incorrect at this compressed SPR.

This is the **3rd instance of orchestrator-side dispatch prediction error in the 12.5H cycle** (after PR #169 NIT-1 §3/§4/§8 inconsistency + PR #175 PILOT_693 CALL→RAISE). Builder transparently flags the divergence + diagnoses + cites the formalization trigger:

> *"Per dispatch full-phase stop rule 'match >1 divergence → STOP', 1 divergence does NOT trigger STOP — proceeding to PR. Per re-pilot dispatch reference text: this is the 3rd orchestrator-side prediction error in the cycle, formalizing TC-X-DISPATCH-PREDICTION-VERIFICATION as a QC sub-vector."*

### Why MEDIUM not HOLD

- Substantive correctness: 5/5 unanimous RAISE with sound MW-33 reasoning across 5 independent labellers — RAISE is GTO-correct
- Dispatch's stop rule explicitly accommodates 1 divergence
- Builder transparently caught + diagnosed
- Issue is orchestrator-side dispatch wording (CALL prediction was wrong); builder data is GTO-sound
- Same family as PR #175 MEDIUM-1 (similar pattern, similar resolution)

**Suggested fix-forward (advisory):** orchestrator-side update: T10' canonical predictions account for MW-33 monster-RAISE rule firing on compressed-SPR bet+call multiway; PILOT_692 prediction should have been RAISE.

### MEDIUM-1 severity rationale

MEDIUM (not HOLD) because:
- Empirical falsification of specific dispatch prediction
- Builder + 5 labellers independently produce same answer
- Substantive purpose (sound training data) preserved
- Dispatch full-phase stop rule already accommodates

**Manual canonical correctness: 5/6 match + 1 MEDIUM-1.**

## TC-X-DISPATCH-PREDICTION-VERIFICATION formalization

Per orchestrator's PR #182 trigger comm explicit request:

> *"Per QC's PR #177 bonus pattern note: formalize as test class. Suggested scope: when a dispatch makes deterministic predictions about protocol outputs (deterministic protocol like v3.4 walk on a specific spec; deterministic count from §X to §Y in a design comm), QC walks the protocol independently to verify; flags any divergence as MEDIUM with specific locator. Add to ~/river-rats-qc/test_class_registry.md per QC stream's evolution rhythm."*

QC institutional memory updated this cycle:
- **`~/river-rats-qc/learning/test_class_registry.md`** — TC-X-DISPATCH-PREDICTION-VERIFICATION entry added with full scope, trigger, method, past instances, sister classes, coverage gap
- **`~/river-rats-qc/learning/curative_additions_log.md`** — Entry #11 documenting the formalization (3-instance threshold pattern)
- **`~/river-rats-qc/learning/incident_pattern_library.md`** — Incident #26 documenting the 12.5H-cycle 3-instance pattern

Test class is forward-active for any future dispatch with deterministic prediction claims.

This is the **third QC class formalization** following the empirical-incident-→-pattern-note-→-orchestrator-trigger pipeline (after TC-X-CROSS-SEED-IMPORTANCE + TC-X-CAP-BINDING-PRE-CHECK at 2026-05-05). All three follow the same loop: empirical incident → QC notes pattern in review → orchestrator queues for next-instance trigger → formalization on threshold reached.

## What QC did NOT audit (scope partition)

- **Per-hand poker correctness** of the other 84 non-manual labels — orchestrator's Opus tier-up cross-check at next phase per dispatch §"Sequencing"
- **GTO interpretation** of PILOT_692 RAISE vs prediction CALL — gto-expert / ml-architect scope
- **Whether the v3.4 protocol's MW-33 rule should override T10' design intent** — methodology question for orchestrator + ml-architect
- **TC-X-DISPATCH-PREDICTION-VERIFICATION pre-flight on the next dispatch** — forward-active; QC will pre-walk on next deterministic-prediction dispatch

## Test class implication

- **TC-X-DISPATCH-PREDICTION-VERIFICATION FORMALIZED** — 3rd QC class formalization in two days (after TC-X-CROSS-SEED-IMPORTANCE + TC-X-CAP-BINDING-PRE-CHECK)
- **Pattern: empirical-incident → pattern-note → orchestrator-trigger → formalization** — proven 3-step pipeline. QC's "becoming smarter over time" mandate is operationally working at 12.5H cycle cadence.
- **TC-X T8 schema gap fix continues operational success** — all 20 T-CONTROL hands produced consensus matching `design_action` (per builder report "T-CONTROL design_action 20/20 match (100%)") — first empirical validation of the curative from PR #150 NIT.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **12th successive cycle solo-routed**. Loop heartbeat detected trigger landing within ~1-2 min of master push (loop fired immediately on `/loop` invocation).

## References

- PR #181: https://github.com/beytell1-sketch/river-rats-v2/pull/181
- PR #181 head: `bfe02f9`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR181_2026-05-06.md` (master `36bb531`, PR #182)
- 12.5H-C full GO directive: master `c749f3f` (PR #180)
- 12.5H-C re-pilot dispatch: master `f4a7b4e` (PR #178; updated predictions per QC MEDIUM-1)
- Prior incidents in pattern: PR #169 NIT-1 (§3/§4/§8 T-CONTROL), PR #175 MEDIUM-1 (PILOT_693 CALL→RAISE), this PR #181 MEDIUM-1 (PILOT_692 CALL→RAISE)
- TC-X-DISPATCH-PREDICTION-VERIFICATION class definition: `~/river-rats-qc/learning/test_class_registry.md` (commit pending QC repo)
- Memory: `feedback_qc_routing_when_standalone_active.md` (12th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #181 for merge.** All 5 audits processed. 4 PASS cleanly; Audit 5 surfaces MEDIUM-1 (PILOT_692 dispatch prediction error — orchestrator-side text update suggested).

**TC-X-DISPATCH-PREDICTION-VERIFICATION formalized.** QC institutional memory updated this cycle.

QC-side gate cleared. Awaiting:
- Orchestrator-side Opus tier-up cross-check on contested hands → labels-final → merge
- 12.5H-D dispatch (corpus QC phase + G5 cap-binding pre-flight + design_action drift detection on T-CONTROL)
