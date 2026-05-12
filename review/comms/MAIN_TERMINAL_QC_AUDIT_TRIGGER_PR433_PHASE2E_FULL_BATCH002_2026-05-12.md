---
date: 2026-05-12
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #433 — Phase 2-E FULL BATCH-002 (50/700 hands with PATCHED brief; 98% consensus; 0/250 illegal votes; 1 owner-arb spot 4WF-4-WAY-3--071) — fire audit now (pre-merge milestone; first production batch with patched brief)
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #433 (Phase 2-E FULL BATCH-002)

PR #433: `builder-phase2-e-full-batch2-2026-05-12`. Pushed 12:20 SAST (~40 min after BATCH-002 resume directive landed at master `1e528dc` via PR #432). Title: "Builder Phase 2-E FULL BATCH-002 — 50/700 with PATCHED brief; 98% consensus; 0/250 illegal".

**Builder self-assessment: BATCH-002 COMPLETE; all gate sentinels green** — primary regression-watch (0/250 illegal votes) holds.

## Builder report summary

- **250 Sonnet + 3 Opus tier-up = 253 labels** delivered
- **0/250 illegal action votes** (regression-watch sentinel PASS; confirms brief patch holds at production scale)
- **49/50 = 98% consensus** (up from BATCH-001's 92%)
  - 41 all-agree (5/5) + 6 four-of-five + 2 (3-2 + Opus joins) = 49 consensus
  - 1 owner-arb (3-2 + Opus dissents)
- **1 owner-arb spot**: 4WF-4-WAY-3--071 (AJo IP 3-bet pot facing CO c-bet on Jh7d2s; Sonnet RAISE×3 / CALL×2; Opus CALL MEDIUM citing calibration anchor 4WC-3BET-2 precedent)
- **0 FL4-drift instances**
- **Decision class diversity 5-of-5**: BET 24 / CHECK 14 / FOLD 5 / CALL 3 / RAISE 3
- **Wall-clock**: ~30 min focused execution
- **Per-batch trend**: BATCH-002 vs BATCH-001: +6% consensus; -3 illegal; -3 arb; brief patch + accumulated experience yields measurable quality improvement

## Diff summary (per builder PR; QC verifies)

9 files expected:
- `data/4way_corpus/full_700/batch_002_50hand.jsonl` (NEW; 50-hand slice)
- `data/4way_corpus/full_700/batch_002_raw_labels_labeller_{1..5}.jsonl` (NEW; 250 labels)
- `data/4way_corpus/full_700/batch_002_raw_labels_opus_tierup.jsonl` (NEW; 3 Opus labels)
- `data/4way_corpus/full_700/batch_002_consensus.jsonl` (NEW; 49 records)
- `data/4way_corpus/full_700/batch_002_owner_arb_queue.jsonl` (NEW; 1 record)
- `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH002_2026-05-12.md` (NEW; report)

No river-rats-core/ code edits expected. No brief / calibration / pilot / mini-pilot / 35-ref / 700-subset modifications.

## Audit scope (~20-30 min — pre-merge milestone; first production batch with patched brief)

### Part A — Diff scope (TC-23)

1. All PR files match builder report. NO river-rats-core/ inference/router/model/trainer edits.
2. TC-23 EXISTENCE: all paths git-tracked post-commit.
3. NO production model file edits.
4. NO consensus rule / driver script changes (frozen from PR #417).
5. NO **brief** modifications (brief is PATCHED at master `8f7a7d0`; must remain unchanged in BATCH-002).
6. NO 29-hand calibration / 35-hand reference / 50-hand pilot / 10-hand mini-pilot / BATCH-001 label modifications (all frozen).
7. NO 700-hand subset modifications (`data/4way_lookalikes_700hand_full_2026-05-12.jsonl` frozen at master `1d5503e`).

### Part B — 50-hand subset validity

8. `data/4way_corpus/full_700/batch_002_50hand.jsonl` parses; exactly 50 lines.
9. **No spot_id overlap** with `batch_001_50hand.jsonl` (50 spots; frozen) AND `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl` (10 spots; frozen). 60 hands excluded; 640 remaining; BATCH-002 picks 50 of those.
10. Builder report notes BATCH-002 is "all 4-way-3-bet-pot axis" — QC verifies via grep on `primary_axis` field (expect ~all "4-way 3-bet/4-bet" or analog axis tag).

### Part C — Label JSONL validity

11. Each `batch_002_raw_labels_labeller_<N>.jsonl` has exactly 50 valid lines (5 × 50 = 250 Sonnet labels).
12. `batch_002_raw_labels_opus_tierup.jsonl` covers exactly the 3 disputed Sonnet spots (063, 066, 071 per builder report).
13. Required fields present per pilot pattern: spot_id, labeller_id, predicted_action, predicted_sizing_pct, confidence, bucket, reasoning, num_opponents_at_decision, primary_axis.

### Part D — PRIMARY GATE: 0/250 illegal action votes (regression-watch sentinel)

14. **0 illegal action votes** verified bit-exact:
    - For each of 250 Sonnet labels: check `predicted_action` field
    - On any spot where `facing_bet == 0`: action must be BET or CHECK (not FOLD/CALL/RAISE)
    - On any spot where `facing_bet > 0`: action must be FOLD/CALL/RAISE (not BET/CHECK)
    - Per-labeller counts in builder report: FL1[23 BET / 15 CHECK / 5 FOLD / 3 CALL / 4 RAISE = 50; 0 illegal]; FL2[24/14/5/4/3; 0]; FL3[25/13/5/3/4; 0]; FL4[27/11/6/2/4; 0]; FL5[22/16/5/4/3; 0]. Total 250; 0 illegal.
15. **Cross-check with batch_002_50hand.jsonl `facing_bet` field**: per-spot, verify Sonnet labellers' action-space discipline holds.

### Part E — Anti-rule-based attestation (FL4 prevention; still applies)

16. Spot-check 5-10 random Sonnet labels across all 5 labellers: NO if/elif chains, NO threshold cutoffs, NO function-definition / return-statement patterns, NO template repetition.
17. Cross-check FL4 pattern: NONE of the 250 labels resemble FL4's Python-script-style.

### Part F — Consensus rule application

18. Per design memo §4.3:
   - **41 all-agree** (5-of-5 Sonnet) → consensus
   - **6 four-of-five** → consensus
   - **2 (3-2 + Opus joins majority)** → consensus (spots 063 + 066; Opus CHECK)
   - **1 (3-2 + Opus dissents)** → owner-arb (spot 071; Opus CALL diverges from RAISE majority)
   - Total: 41+6+2+1 = 50 ✓
19. **Sonnet consensus rate**: (41+6+2)/50 = 49/50 = 98% ✓ matches builder claim.
20. Spot-check consensus.jsonl entries: state classification matches actual votes.

### Part G — Owner-arb queue integrity (1 spot)

21. **4WF-4-WAY-3--071**: AJo IP 3-bet pot vs CO c-bet on Jh7d2s. Sonnet RAISE×3 / CALL×2. Opus CALL MEDIUM. Verify:
    - Spot data shows facing_bet > 0 (CO c-bets); both RAISE and CALL are legal actions (NOT an illegal-action confusion).
    - This is a **substantive RAISE-vs-CALL GTO judgment call**, not a procedural action-space failure.
    - Opus cites calibration anchor 4WC-3BET-2 as precedent (same Jh7d2s board; hero AK → CALL); verify this anchor exists in `data/4way_calibration_29hand_2026-05-11.jsonl`.
22. **No silent adjudication**: confirm arb spot is in `batch_002_owner_arb_queue.jsonl` (NOT consensus.jsonl). Per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`.

### Part H — Process discipline

23. **TC-X-DISPATCH-COMPLIANCE per PR #432**: builder honored Task 1 (subset slice; non-overlap) + Task 2 (5 Sonnet + Opus tier-up with PATCHED brief) + Task 3 (sentinel regression-watch; 0 illegal verified) + Task 4 (builder report with BATCH-001 comparison).
24. **STOP-condition compliance**: all 5 STOP-conditions green per builder claim (0 illegal, 0 FL4, 2% consensus collapse, 2% arb, ~30 min wall-clock); builder did NOT improvise unilateral arb adjudication.

## What this PR does NOT change

- ❌ river-rats-core/ (no code edits)
- ❌ Production code path
- ❌ Models, full corpus, training data (this is BATCH-002 of 14; 12 batches remain)
- ❌ Brief (frozen at master 8f7a7d0)
- ❌ Phase 1.5 ship state (vNext-HU-59 in production)
- ❌ Phase 2-F / 2-G / 2-H scope
- ❌ Solver-verification queue (this PR adds 1 spot to existing 57 = 58 total; HOLD per §6.4)

## What gates next (post-QC-PASS orchestrator sequence)

1. Orchestrator merges PR #433 on QC PASS.
2. Solver-verify queue: +1 spot (4WF-4-WAY-3--071) → 58 total; HOLD per §6.4.
3. Orchestrator authors **BATCH-003 resume directive** (next 50 hands; same pipeline; same sentinels).
4. 12 batches remaining. After BATCH-014 + QC PASS → 750-hand corpus assembly → 2-F + 2-G + 2-H.

## QC routing + Output

Standalone stream. ~20-30 min wall-clock (50-hand subset + 253-label data + 1-spot arb verification + bit-exact illegal-vote sentinel). QC writes:
- `~/river-rats-qc/findings/2026-05-12-pr433-phase2e-full-batch002.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E_FULL_BATCH002_2026-05-12.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: ≥1 illegal action vote (PRIMARY GATE FAILURE; signals brief-patch regression); consensus rule misapplied; silent arb adjudication; brief modifications; spot_id overlap with BATCH-001 or mini-pilot or pilot or reference or calibration sets
- **SHOULD_FIX-substantive**: <50 labels per file; rationale word count consistently <150; missing required fields; FL4-drift detected
- **SHOULD_FIX-process**: solver-verify queue lacks per-spot rationale; minor wording/typo
- **PASS**: 0/250 illegal verified bit-exact + 98% consensus matches builder + 1 arb spot substantive (RAISE-vs-CALL not action-space) + dispatch compliance clean

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `1e528dc` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- BATCH-002 resume directive: master `1e528dc` (PR #432)
- 2-E.0.1 mini-pilot + QC PASS (brief patch validated): master `8f7a7d0` (PR #429 + #431)
- Phase 2-E FULL BATCH-001 + QC PASS (signal source): master `b9e723f` (PR #425 + #427)
- Phase 2-E FULL dispatch (Option A authorized; FULL ~700 scope): master `1d5503e` (PR #424)
- Phase 2-E pilot execution + QC PASS: master `bac08e1` (PR #423)
- 4-way labeller brief (PATCHED; frozen): `data/4way_labeller_brief.md`
- 29-hand calibration (frozen): `data/4way_calibration_29hand_2026-05-11.jsonl`
- 700-hand subset (frozen): `data/4way_lookalikes_700hand_full_2026-05-12.jsonl`
- BATCH-001 subset (non-overlap target): `data/4way_corpus/full_700/batch_001_50hand.jsonl`
- Mini-pilot subset (non-overlap target): `data/4way_corpus/mini_pilot_2e01/mini_pilot_10hand_2026-05-12.jsonl`
- Driver script (reuse): `scripts/dispatch_4way_labelling_pilot.py`
- Builder report: `review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH002_2026-05-12.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

**Status: QC stream — fire audit now on PR #433 Phase 2-E FULL BATCH-002 (first production batch with PATCHED brief). ~20-30 min wall-clock. 24-item audit covering subset non-overlap + 253-label data integrity + PRIMARY GATE bit-exact 0/250 illegal-vote verification (regression-watch sentinel) + consensus rule application + 1-spot owner-arb substantive-vs-procedural classification + FL4-drift verification + dispatch compliance. Builder self-assessed all sentinels green. After QC PASS + merge → orchestrator authors BATCH-003 resume directive; 12 batches remaining; final 750-hand corpus assembly at BATCH-014.**
