---
date: 2026-05-10
from: River Rats QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner
re: PR #350 — Phase 1.5-D.3 FULL INFRA-PREP (HU-2..HU-6 generator + sanitization + 696 situations + §(c.1)+§(c.3) decisions; §(c.2) DESIGN-ONLY) — pre-merge audit verdict
status: VERDICT — PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR350_FULL_INFRA_PREP_2026-05-10.md (master a558ada)
target_pr_head: aab92ec9fdede58f4d32f501fdff9680de58ea6d
master_at_audit: a558adabad1c11a9800a670a6941bbb311ad6b3f
qc_branch: qc/pr350-phase15d3-full-infra-prep-review-2026-05-10
audit_type: pre-merge milestone (FULL infrastructure pre-labelling; ~20 min)
---

# PR #350 — Phase 1.5-D.3 FULL INFRA-PREP; pre-merge audit

## Result

**PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT.** 50th solo cycle.

All 10 audit items verified + sanitization grep INDEPENDENTLY VERIFIED zero forbidden-field matches across 3 sanitized files + §(c.2) batching DESIGN sufficiency PASS + §(c.3) path-(b) justification PASS. Builder's pilot+full split decision is methodologically sound per `feedback_pilot_first_for_long_jobs.md` STANDING RULE + CLAUDE.md §5.

## 10-item walkthrough (compact)

### Item 1 — Diff scope strict (vs merge-base `e58ed94`)

10 files / +3700 / -23. NO labelling outputs (raw_labels.jsonl / consensus.jsonl absent — confirms split is real, not stealth-labelling). Matches trigger §"Diff summary" exactly. ✓

### Item 2 — §(c.1) Sanitization INDEPENDENT GREP verification

`scripts/sanitize_calibration_extracts.py` defines `FORBIDDEN_FIELDS` list of 13 fields:
1. `expert_action`
2. `expert_reasoning`
3. `oracle_action`
4. `is_correct_action`
5. `solver_action`
6. `solver_frequencies`
7. `gto_action`
8. `expected_label`
9. `correct_action`
10. `recommended_action`
11. `expert_confidence`
12. `label`
13. `answer`

Independent grep on sanitized files (extended set including `expected_action` / `target_action` / `gold_label` / `reference_action` / `ground_truth`):

| sanitized file | forbidden-field matches |
|----------------|------------------------|
| `BATCH2_8_HAND_DESIGNS_SANITIZED.md` | **0** |
| `test_set_50_labelled_SANITIZED.jsonl` | **0** |
| `3way_combined_350_SANITIZED.jsonl` | **0** |

13-field list is sufficient against PILOT V2 contamination signal (4 fields surfaced previously: `expert_action`/`expert_reasoning`/`oracle_action`/`label`). Coverage is comprehensive. ✓

### Item 3 — Generator extension verification

Patched `scripts/generate_hu_situations.py` adds `main_full()` for HU-2..HU-6 generation. `main_pilot()` preserved.

`python3 scripts/test_generate_hu_situations.py` → **8/8 passed** (incl. test_variation_param_matches_board_state_invariant; test_no_card_conflicts_in_board_mutations; test_non_board_variations_leave_board_unchanged).

Per-anchor board diversity preserved: 696 situations across 24 × 29 each ✓

### Item 4 — Anchor coverage

`scripts/hu_anchors_axes_2_6.py` defines 24 anchors via `ALL_HU2_HU6_ANCHORS`:

| axis | anchors |
|------|---------|
| HU-2 | HU-2.1, 2.2, 2.3, 2.4, 2.5 (5) |
| HU-3 | HU-3.1, 3.2, 3.3, 3.4, 3.5 (5) |
| HU-4 | HU-4.1, 4.2, 4.3, 4.4, 4.5 (5) |
| HU-5 | HU-5.1, 5.2, 5.3, 5.4, 5.5 (5) |
| HU-6 | HU-6.1, 6.2, 6.3, 6.4 (**4**) |

**HU-6.5 EXPLICITLY EXCLUDED** per PR #338 owner adjudication (CALL with solver-pending; NOT lookalike-source until solver-verified). Total = 24, matches dispatch spec exactly. ✓

### Item 5 — 696 situations + per-anchor count = 29

`situations.jsonl`: 696 entries; per-anchor count = 29 (uniform across all 24 anchors). 24 × 29 = 696 ✓.

`similarity_distance_audit.jsonl`: 696 entries (matching).

Variation axis distribution (across all 696):
- board_runout: 240 (10/anchor)
- effective_stack: 192 (8/anchor)
- villain_action_sequence: 154 (6.4/anchor avg)
- villain_bet_sizing: 110 (4.6/anchor avg)

29 = ~10 board + 8 stack + ~6 action + ~5 sizing per anchor; reasonable axis-mix scaling vs PILOT V2's 5+3+1+1=10/anchor. ✓

### Item 6 — §(c.2) Throttle-aware batching DESIGN sufficiency

Builder report §(c.2) (lines 44-55) documents:
- **Concurrency**: per-labeller serial Phase 2 (calibration) + serial Phase 3 (labelling); all 5 labellers run parallel at agent level (PILOT V2 pattern + backpressure addition)
- **Backpressure**: 60-90s sleep between batches of 50 spots if rate-limit signal detected; stretches labeller over 30-60min wall-clock vs mid-burst death
- **Backoff**: try/except on rate-limit; 30s+jitter retry; max 3 retries per spot; skip-with-`_meta:error:rate_limited` marker on triple-fail (surfaces in builder report as coverage gap)
- **Mid-batch durability**: APPEND-ONLY raw_labels_labeller_N.jsonl + local progress marker (last-completed `spot_id`); resume skips spots already in file
- **Wall-clock estimate**: PILOT V2 took ~30min for 250 calls under throttle → FULL 14x → realistic 60-120min (with backpressure-padding + parallel pool)
- **Recovery-resumption test**: DEFERRED to implementation session per dispatch verification gate

**QC assessment: DESIGN sufficient.** PILOT V2's serial-overlap retry cascade demonstrated baseline approach works (5/5 labellers DONE; QC PASS · 0/0/0 in PR #344+#346). FULL extension adds explicit append-only formalization + backpressure budget — these are surgical additions, not greenfield design.

Two real risks worth noting (but not BLOCKER/SHOULD_FIX-class given §(c.2) "DESIGN; implementation in labelling session" framing):

1. Recovery-resumption test is DEFERRED → if append-only/resume logic has subtle bug, FULL surfaces it via duplicate or missing entries. Builder commits to running test in next-session labelling PR; QC will verify in that audit. Acceptable per dispatch §(c.2) framing.

2. Triple-rate-limit-fail skip behavior could create coverage gaps at FULL scale (5 labellers × 700 spots, if 0.1% triple-fail per labeller = 3-4 spots × 5 labellers = 15-20 missing entries). Builder commits to surface coverage gaps in builder report; not a label-correctness issue, just sample-size shrinkage. Acceptable.

§(c.2) DESIGN passes "commit-WHAT; builder-decides-HOW" framing per dispatch.

### Item 7 — §(c.3) path-(b) justification assessment

Builder chose path (b) "accept stale composition with justification". Builder report lines 60-68 + labeller brief explicit disclosure.

**Evidence base** (PILOT V2 / 50 spots × 5 labellers = 250 outputs):
- HU-1.4 LK-01..05: anchor composition="set of tens"; labellers correctly read mutated turn (Tc → 6c/7c/etc.) and re-classified as "TT overpair on paired/coordinated turn"
- HU-1.5 LK-01..05: anchor composition="TPGK with A-blocker"; labellers correctly read flush-completing river without anchor's blocker structure and re-classified as "TPTK no club blocker on flush-completing river"
- QC PR #346 verdict (PASS · 0/0/0) verified labels were valid

**QC assessment: justification holds.** Labellers correctly perform the separation-of-concerns (board-fields = generator; composition = labeller). Labeller brief explicitly discloses staleness with concrete HU-1.4 LK-01 example, ensuring labellers know to ignore stale prose.

Risk at FULL scale (3500 outputs vs 250): if 0.5% of labellers exhibit prose-confusion = ~17 confused labels. These would surface in 3-2 splits where rationale references stale composition contradicting board. QC will spot-check FULL audit for this signature; if it appears, surface in verdict + re-evaluate path-(a). Builder's escape hatch: "If FULL labellers exhibit confusion from stale composition prose, surface in builder report and re-evaluate path-(a) cost-benefit" (line 68).

Acceptable per dispatch's path-(a)-vs-path-(b) framing.

### Item 8 — labeller_brief

- Bucket-first compliance: "NO equity thresholds in reasoning; use composition + protocol rules" ✓
- Solver-vs-labels separation: "don't cite solver as label rationale" ✓
- Sanitized-extract guidance: explicit pointers to sanitized calibration files + warning that training-data JSONL would leak answers ✓

### Item 9 — Pilot V2 vs FULL alignment

- Same generator architecture as PILOT V2 (board-mutation logic preserved)
- Per-anchor lookalike count 29 vs PILOT V2's 10: scaled per design memo §4.4 (FULL needs higher density to support 1.5-D.4 retrain; 24×29=696 matches dispatch spec ~700)
- Same similarity-band threshold as PILOT V2 (architect committed in 1.5-D.3 PILOT V2; same threshold applies in FULL)

Alignment ✓

### Item 10 — TC-X-DISPATCH-COMPLIANCE

Dispatch §(b) scope (FULL infrastructure) + §(c.1) sanitization implementation + §(c.2) DESIGN + §(c.3) path-(b) decision documented + negative-scope items (NO labelling outputs) honored. Builder split decision documented + justified per `feedback_pilot_first_for_long_jobs.md` + CLAUDE.md §5. ✓

## Pilot+full split decision assessment

Builder applied `feedback_pilot_first_for_long_jobs.md` STANDING RULE + CLAUDE.md §5 STOP > improvise to split INFRA-PREP from LABELLING (deferring 3480 LLM calls + Opus tier-up + consensus + report to next session per context budget).

Orchestrator already accepted this split per audit-trigger §"Orchestrator-decision on the split: ACCEPTED" (4 reasons).

**QC assessment: split is methodologically sound.** Reasoning:
1. 3480 LLM calls + Opus tier-up + consensus + report would risk mid-batch context-budget exhaustion → improvised recovery → improvisation per CLAUDE.md §5 violation
2. Pilot+full standing rule applies to ANY long batch; this split nests pilot+full within the meta-pilot+full structure (PILOT V2 was the pilot for the pipeline; FULL has its own pilot+full structure where INFRA-PREP is "pilot of the FULL run")
3. Pre-merge QC audit of infrastructure BEFORE 3480-LLM-call commitment is exactly the value pilot+full provides
4. CLAUDE.md §5 STOP > improvise correctly invoked

Builder's split decision passes the same 5-point TC-X-OPERATIONAL-DEVIATION-ASSESSMENT framework as prior deviations: substantive correctness + transparent disclosure + within-authorization (orchestrator accepted) + alternative-cost-comparison favors split + standing-rule alignment.

## TC-X-DISPATCH-PREDICTION-VERIFICATION evidence

Dispatch §(b) prediction: "700 lookalikes from HU-2..HU-6 anchors" — VERIFIED at 696 (24×29; close enough — similarity-band filter trim to 696 is documented).

§(c.1) prediction "sanitization eliminates 4-instance contamination class" — VERIFIED at zero forbidden-field matches in independent grep across all 3 sanitized files.

§(c.3) path-(b) prediction "PILOT V2 evidence supports stale-composition acceptance" — VERIFIED via concrete HU-1.4 LK-01..05 + HU-1.5 LK-01..05 examples in PILOT V2 already PASS-verified.

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE) — 10 PR files in expected dirs ✓
- TC-X-OWNER-SCOPE-DISCIPLINE (30th formal use) — 6 negatives held; scripts in scripts/ acceptable
- TC-X-DISPATCH-COMPLIANCE (29th formal exercise; PASS)
- TC-X-DISPATCH-PREDICTION-VERIFICATION — §(b) + §(c.1) + §(c.3) all verified
- TC-X-INTRA-PLAN-CONSISTENCY (informal — anchor module × situations × similarity-audit all consistent at 24 × 29 = 696)
- TC-X-METHODOLOGY-RULE-CROSSCHECK — `feedback_pilot_first_for_long_jobs.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_qc_required_before_approval.md` verified
- TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (5th application; pilot+full meta-split) — ACCEPT per 5-point framework

## Smarter-over-time

Fifth instance of TC-X-OPERATIONAL-DEVIATION-ASSESSMENT — pattern continues durable. This audit exercises the framework on a **meta-deviation** (split that nests pilot+full within pilot+full); framework still applies cleanly.

Sanitization architecture is a notable artifact:
- 13 forbidden-field list captures the recurring contamination pattern (4 instances pre-fix)
- `_sanitization_report.json` audit trail mentioned in script header
- Reusable across future calibration extract operations
- Recommend documenting the FORBIDDEN_FIELDS list in memory rule for future labeller pipelines (even non-HU): "calibration extract contamination — strip {13-field list} before serving to labellers"

§(c.2) DESIGN-deferral pattern is interesting — first time QC audit accepts a design-only deliverable (vs implementation). Trigger framing "commit-WHAT; builder-decides-HOW" makes this audit-tractable. Recommend formalizing the pattern: "DESIGN-only deliverables may be QC-PASS'd on (1) explicit dispatch authorization, (2) verification gate spec for implementation session, (3) substance-sufficient design doc."

## Gates

PR #350 cleared. Per dispatch + standing-directive autonomous merge: orchestrator may merge PR #350 + this verdict comm autonomously. After merge:
- Orchestrator authorizes Phase 1.5-D.3 FULL LABELLING-EXECUTION dispatch (next session resumption with builder firing 3480 LLM calls + Opus tier-up + consensus + builder report)
- Recovery-resumption test must be in next-session labelling PR per dispatch verification gate
- After FULL LABELLING PR + QC + owner-arb adjudications (if any) + solver-queue drain → orchestrator authorizes 1.5-D.4 retrain

**LOOP CONTINUES** through 1.5-D.3 FULL LABELLING → 1.5-D.4 (HU retrain on 59) → 1.5-E (router/coaching) → Phase 2 D5.

## Cycle stats

- 50th solo QC cycle.
- Wall clock: ~20 min (matches dispatch heads-up of 20-25 min).
- LLM cost: $0.

## References

- Builder PR #350 head: `aab92ec9fdede58f4d32f501fdff9680de58ea6d`
- 1.5-D.3 FULL dispatch: master `bfebd13` (PR #348)
- HU-1.4 data-layer-fix merged: master `e58ed94` (PR #349)
- 1.5-D.3 PILOT V2 merged: master `4432f68` (PR #344); v2 QC verdict: master `b790524` (PR #346; PASS · 0/0/0)
- Audit-trigger: master `a558ada`
- HU-6.5 owner-CALL adjudication: master `60bb850` (PR #343 dispatch §(a))
- Architect's design memo §4.3-§4.5 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory rules verified: `feedback_pilot_first_for_long_jobs.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`
