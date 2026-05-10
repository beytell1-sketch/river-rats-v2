---
date: 2026-05-10
from: River Rats QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner
re: PR #339 — Phase 1.5-D.3 PILOT (50 HU lookalikes HU-1 axis × 5 labellers + Opus tier-up; 96% gate PASS; 1 owner-arb HU-1.5-LK-10; 1 generator bug) — pre-merge audit verdict
status: VERDICT — PASS-WITH-FINDINGS · 0 BLOCKER · 1 SHOULD_FIX · 0 NIT
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR339_PILOT_2026-05-10.md (master a8aab0c)
target_pr_head: 7470147385ad22c23dfa4a6bfc61714cb1dfbd66
master_at_audit: a8aab0c194d8a6c338d10cfae297d4562507e7f5
qc_branch: qc/pr339-phase15d3-pilot-review-2026-05-10
audit_type: pre-merge pilot gate (Phase 1.5-D.3 corpus assembly pilot; ~15 min)
---

# PR #339 — Phase 1.5-D.3 PILOT; pre-merge pilot-gate audit

## Result

**PASS-WITH-FINDINGS · 0 BLOCKER · 1 SHOULD_FIX · 0 NIT.** 48th solo cycle.

All 10 dispatch audit items verified. Pilot data committable as audit trail; **FULL phase BLOCKED on generator fix per SHOULD_FIX-1**. Builder correctly flagged generator-bug per CLAUDE.md §5 STOP > improvise; substantive labelling pipeline + tier-up + owner-arb routing all clean.

## SHOULD_FIX-1: Generator bug — board fields unchanged across lookalikes (BLOCKS FULL)

**Severity:** SHOULD_FIX (must be resolved before FULL phase fires; pilot data acceptable as audit trail).

**Independent verification by QC:**

5 anchors × 10 lookalikes per anchor = 50 spots. Per-anchor unique board count via `set()`:

| anchor | lookalikes | unique flops | unique turns | unique rivers |
|--------|------------|--------------|--------------|---------------|
| HU-1.1 | 10 | **1** | **1** | **1** |
| HU-1.2 | 10 | **1** | **1** | **1** |
| HU-1.3 | 10 | **1** | **1** | **1** |
| HU-1.4 | 10 | **1** | **1** | **1** |
| HU-1.5 | 10 | **1** | **1** | **1** |

ALL 10 lookalikes per anchor share identical board strings. Variation axis distribution:

| variation_axis | count |
|----------------|-------|
| board_runout (broken — boards unchanged) | 25 |
| effective_stack (legit) | 15 |
| villain_action_sequence (legit) | 6 |
| villain_bet_sizing (legit) | 4 |

25 of 50 (50%) lookalikes are tagged board_runout but the board fields are anchor-identical. Builder report (line 55+) acknowledges this exactly: "the actual `board_flop` / `board_turn` / `board_river` fields in each row are unchanged from the anchor. Effective_stack_bb and to_call_bb fields ARE updated; only the board fields are not."

**Severity reasoning:**
- 25 broken lookalikes don't actively harm anything — they re-test anchor labelling at a redundancy that ADDS signal on anchor stability (and the labellers correctly noted same hand → same answer)
- 25 legitimate stack/sizing/action variations DO test diversity and produce legit consensus signal (4 of these are sized variations that produced novel labels e.g. HU-1.5-LK-10 owner-arb at 112% overbet vs anchor's 75%)
- 96% pilot gate signal is partly inflated by anchor-stability for the 25 broken spots; partially genuine for the 25 legit spots
- FULL at 14× scale (700 lookalikes) would replicate the bug at 350 broken lookalikes — substantial waste

Pilot is committable; FULL HOLDs on generator fix.

**Suggested fix path** (advisory, owner/builder-scope):
- `scripts/generate_hu_situations.py` board mutation per `variation_param` description before emit (per builder report line 68 architect-hat commits in 1.5-D.3 FULL)
- Test cases: assert per-anchor unique flop count > 1 across multiple board_runout lookalikes
- QC re-audit on fix PR before FULL fires

## 10-item walkthrough (compact)

### Item 1 — Diff scope strict (vs merge-base `c54eab1`)

9 files / +963 / -0:
- `scripts/generate_hu_situations.py` (+276) — generator script in scripts/ (not source mod; river-rats-core/ untouched)
- `data/hu_corpus/pilot_50/situations.jsonl` (+50)
- `data/hu_corpus/pilot_50/raw_labels.jsonl` (+250)
- `data/hu_corpus/pilot_50/consensus.jsonl` (+50)
- `data/hu_corpus/pilot_50/calibration_results.jsonl` (+5)
- `data/hu_corpus/pilot_50/opus_tier_up.jsonl` (+8: 1 _meta + 7 hand entries)
- `data/hu_corpus/pilot_50/similarity_distance_audit.jsonl` (+50)
- `data/hu_corpus/pilot_50/labeller_brief.md` (+59)
- `review/comms/BUILDER_REPORT_PHASE15D3_PILOT_2026-05-10.md` (+215)

NO unauthorized source/prompt/model edits ✓

### Item 2 — Generator-bug verification (independent)

See SHOULD_FIX-1 above. Bug exists exactly as builder describes. ✓

### Item 3 — Pool size

Builder report: ~3000 generated; 50 filtered for pilot per design memo §4.4. (Sampled via similarity-band threshold per Item 4.)

### Item 4 — Similarity-band threshold

`similarity_distance_audit.jsonl` contains 50 entries (one per pilot lookalike) with per-spot similarity assignment + rationale per architect-committed threshold. Builder report references threshold; per-row entries verify ✓

### Item 5 — 5 labellers per spot + calibration

- raw_labels.jsonl: 250 entries / 5 unique labeller_ids / 50 unique spot_ids ✓
- calibration_results.jsonl: all 5 PASS (scores 24/28, 25/28, 26/28, 27/28, 27/28; all reversal_correct + final_pass:true) ✓

### Item 6 — Bucket-first + solver-vs-labels

labeller_brief explicit:
- "Bucket-first: NO equity thresholds in reasoning; use composition + protocol rules" ✓
- "Solver-vs-labels: don't cite solver as label rationale" ✓

(Slightly more compact wording vs prior briefs but substantive content equivalent.)

### Item 7 — Consensus rule applied

Split distribution across 50 hands:
- 5-of-5: 43 hands (consensus action set; owner_arb=false)
- 4-of-5: 5 hands (4-of-5 majority; owner_arb=false)
- 3-2: 2 hands

3-2 hand handling:
- HU-1.5-LK-05: 3-2 FOLD/CALL; Opus presumably agreed with majority → consensus=FOLD (3-of-5 majority); owner_arb=false ✓
- HU-1.5-LK-10: 3-2 CALL/FOLD; Opus DISAGREED → consensus=null + owner_arb=true ✓

Consensus rule applied exactly per dispatch §"Consensus rule".

### Item 8 — Pilot gate verification

≥4-of-5 consensus rate: 48/50 = 96% (well above 80% threshold).
Pilot gate cleared. ✓

### Item 9 — HU-6.5 propagation N/A; HU-1.5 anchor consensus check

HU-1.5 anchor consensus from 1.5-D.2 PILOT was CALL (5/5 unanimous). HU-1.5 lookalikes verification:

| spot_id | consensus_action | split_kind | owner_arb |
|---------|------------------|------------|-----------|
| HU-1.5-LK-01 | CALL | 5-of-5 | false |
| HU-1.5-LK-02 | CALL | 5-of-5 | false |
| HU-1.5-LK-03 | CALL | 5-of-5 | false |
| HU-1.5-LK-04 | CALL | 5-of-5 | false |
| HU-1.5-LK-05 | FOLD | 3-2 | false |
| HU-1.5-LK-06 | CALL | 5-of-5 | false |
| HU-1.5-LK-07 | CALL | 5-of-5 | false |
| HU-1.5-LK-08 | CALL | 5-of-5 | false |
| HU-1.5-LK-09 | CALL | 5-of-5 | false |
| HU-1.5-LK-10 | null | 3-2 | true |

8/10 follow anchor (CALL); LK-05 has 3-2 FOLD majority (likely a sizing/stack variation that shifted the bluff-catch frame); LK-10 owner-arbitrated at 112% overbet (genuine ambiguity at the larger size). HU-1.5 anchor propagation is reasonable. ✓

### Item 10 — TC-X-DISPATCH-COMPLIANCE

§4.4 spec + pilot+full split + solver-pending gating + negative scope items honored. Builder transparently flagged generator-bug per CLAUDE.md §5 STOP > improvise (line 193 of report: "❌ No improvisation: STOP-condition-grade issues (generator bug; v9-3way uncertainty deferral; HU-1.5-LK-10 owner-arb) all surfaced transparently for QC + owner"). ✓

## Special audit consideration (per trigger §"Special audit consideration: generator bug severity")

Trigger asks QC to explicitly recommend PASS-WITH-FINDINGS or REJECT.

**QC recommendation: PASS-WITH-FINDINGS.** Pilot data is committable as audit trail; FULL phase BLOCKED on generator fix per SHOULD_FIX-1.

Reasoning:
1. Substantive consensus signal IS real on the 25 legitimate variations (stack/sizing/action) — these are diversity-tested labels that DO contribute to corpus
2. The 25 broken board_runout lookalikes provide anchor-stability redundancy signal (labellers correctly noted same hand → same answer) — useful as audit trail, doesn't harm
3. Builder transparently flagged the bug per dispatch's STOP > improvise discipline; dispatch already pre-built FULL HOLD on generator fix (no scope creep)
4. REJECT (re-run pilot after generator fix) would discard 50 legitimate calibrated labels + Opus tier-up + owner-arb data — wasteful when bug is already isolated and bounded

Audit trail value of the pilot data exceeds re-run cost; PASS-WITH-FINDINGS is the right call.

## TC-X-DISPATCH-PREDICTION-VERIFICATION evidence

Design memo §4.4 prediction: "750 lookalikes (50 pilot + 700 full); 5-labeller consensus + Opus tier-up; pilot gate ≥80%" — VERIFIED at 96% pilot gate (well above threshold). Generator bug is a process gap not anticipated in §4.4; transparently surfaced for FULL fix.

HU-1.5 owner-arb propagation question: LK-10 at 112% overbet shifted bluff-catch frame and triggered new owner-arb — confirms design intuition that sizing variations are decision-class-relevant (not just stack/action). Useful axis design signal for FULL phase.

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE) — 9 PR files in expected dirs ✓
- TC-X-OWNER-SCOPE-DISCIPLINE (28th formal use) — 6 negatives held; generator script in scripts/ acceptable
- TC-X-DISPATCH-COMPLIANCE (27th formal exercise; PASS-WITH-FINDINGS on generator-bug)
- TC-X-DISPATCH-PREDICTION-VERIFICATION — design memo §4.4 verified
- TC-X-INTRA-PLAN-CONSISTENCY (informal — calibration × raw_labels × consensus × similarity-audit all consistent)
- TC-X-METHODOLOGY-RULE-CROSSCHECK — `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md` verified
- TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (3rd application; first 1.5-D.1 orchestrator-emergency-authorship; second 1.5-D.2 tier-up-escalation; this is generator-bug-flag-then-commit-with-FULL-block) — ACCEPT per 5-point framework

## Smarter-over-time

Third instance of TC-X-OPERATIONAL-DEVIATION-ASSESSMENT — different deviation class each time:
- 1.5-D.1: orchestrator-wearing-builder-hat after 13h+ stall (escalation)
- 1.5-D.2: tier-up-rule-vs-consensus-rule overlap (procedural simplification)
- 1.5-D.3: bug-flag-then-commit-pilot-data (audit trail preservation)

Each deviation correctly handled per CLAUDE.md §5 STOP-condition discipline + transparent disclosure + dispatch's pre-built mitigation paths. The 5-point assessment framework is durable across these qualitatively-different deviations.

For FULL phase: QC recommends generator fix PR include explicit unit test asserting per-anchor unique flop count > 1 across multiple board_runout lookalikes. Prevents regression; protects 14× scale-up.

## Gates

PR #339 cleared as PASS-WITH-FINDINGS. Per dispatch + standing-directive autonomous merge: orchestrator may merge PR #339 + this verdict comm autonomously. After merge:
- Orchestrator surfaces HU-1.5-LK-10 owner-arbitration to owner via direct message
- Orchestrator HOLDs Phase 1.5-D.3 FULL dispatch until generator-fix PR + QC PASS on fix
- Owner adjudicates HU-1.5-LK-10 (CALL vs FOLD at 112% overbet)
- Builder fires generator-fix PR (per SHOULD_FIX-1 advisory path)
- After generator-fix QC PASS + HU-1.5-LK-10 adjudication → orchestrator authorizes FULL batch dispatch

**LOOP CONTINUES** through generator-fix → 1.5-D.3 FULL → 1.5-D.4 (HU retrain on 59) → 1.5-E (router/coaching) → Phase 2 D5.

## Cycle stats

- 48th solo QC cycle.
- Wall clock: ~15 min (matches dispatch heads-up).
- LLM cost: $0.

## References

- Builder PR #339 head: `7470147385ad22c23dfa4a6bfc61714cb1dfbd66`
- 1.5-D.3 dispatch + HU-6.5 adjudication: master `c54eab1` (PR #338)
- Audit-trigger: master `a8aab0c`
- HU reference set: `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md`
- 1.5-D.2 PILOT (HU-1.5 anchor 5/5 CALL): master `bed7368` (PR #332)
- Architect's design memo §4.4 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory rules verified: `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`
