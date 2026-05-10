---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (builder; architect-hat for §(c) infrastructure decisions)
re: (a) HU-1.4-LK-04 + HU-1.4-LK-05 owner-adjudication = CALL with solver-flag; HU-1.5-LK-10 re-confirm acknowledged + (b) Phase 1.5-D.3 FULL dispatch (700 lookalikes from HU-2..HU-6 anchors) + (c) architect-hat decisions: sanitized-JSONL-extract calibration + throttle-aware batching (commit-WHAT; builder-decides-HOW) + (d) solver-verification queue updated
status: DISPATCH — fire now
---

# (a) Owner-adjudication: HU-1.4-LK-04 + HU-1.4-LK-05 = CALL with solver-flag

## HU-1.4-LK-04 (NEW; PR #344 PILOT V2)

**Spot:** Hero TsTd in SB; opens 3bb; BB calls. Flop 8h5c2d (rainbow). SB checks; BB checks. Turn 6c (replaced anchor's Tc → 6c per generator board_runout variation; 6c brings 4-5-6-7-8 OESD potential + flush draw). SB checks. BB bets 4bb (33% pot, 4bb into 12bb). Pot=12bb → 16bb after bet. Effective stack 60bb. Hero acts.

**Composition (correct for lookalike, not anchor):** TT overpair on coordinated turn (not the anchor's "set of tens" — board mutated away from Tc).

**Labeller distribution:** RAISE×3, CALL×2 (Sonnet) + Opus tier-up = CALL → Opus DISAGREES with Sonnet majority → owner-arb required per dispatch consensus rule §4.3.

**Owner adjudication: CALL.** Reasoning frame:
- TT overpair on connected turn (4-5-6-7-8 OESDs + flush draw) facing a small 33% probe.
- Hero is OOP in SB; raising commits to building pot OOP, which is bad ergonomics.
- Calling preserves villain's range (lets villain bluff/give up on river); hero realizes equity vs full range.
- Raise charges draws but folds out air → net-EV ambiguous on small probe; CALL captures overpair value in standard manner.
- Solver may show frequency-mixed RAISE/CALL; pure-CALL is a safe deterministic label that aligns with hero's OOP-controlled-pot principle on coordinated boards.

**Solver-verification flag set.** Spot enters solver-verification queue per `feedback_solver_verification_queue.md` for pre-1.5-D.4 drain.

## HU-1.4-LK-05 (NEW; PR #344 PILOT V2)

**Spot:** Identical shape to HU-1.4-LK-04 except turn = 7c (replaced Tc → 7c; 7c brings 5-6-7-8-9 OESD + flush draw).

**Labeller distribution:** RAISE×3, CALL×2 (Sonnet) + Opus tier-up = CALL → Opus DISAGREES → owner-arb required.

**Owner adjudication: CALL.** Same reasoning as HU-1.4-LK-04 (same hero/position/sizing/composition; turn 7c is structurally similar to 6c — both add OESD + flush draw straight texture; pot-control OOP with overpair holds across both).

**Solver-verification flag set.** Spot enters solver-verification queue.

## HU-1.5-LK-10 re-confirmation acknowledged

V2 LK-10 board IDENTICAL to v1 anchor (Jc9c5d / Jc9c5d2s / Jc9c5d2sQd). Variation_axis = `villain_bet_sizing` (37.5bb → 56.2bb = 1.5x overbet); board unchanged. Per generator-fix dispatch §(a) item 4: "same board → CALL with solver-verification-pending propagates". V2 row correctly shows consensus_action = CALL (overriding labeller-pool 4-1 FOLD majority at the larger size); owner_arb = true; notes correctly cite §(b) item 4 propagation.

QC noted in §"Item 9": labeller-pool FOLD shift at 112% (vs 5/5 CALL at 75%) is "a real signal worth confirming in solver verification queue." Acknowledged. HU-1.5-LK-10 remains in solver-verification queue with explicit note that the sizing-axis labeller-divergence is a solver-priority verification item.

---

# (b) Phase 1.5-D.3 FULL — dispatch

## Scope

Per design memo §4.4: target ~750 HU labelled situations total. Pilot V2 produced 50 (HU-1 axis). FULL produces remaining 700 from HU-2..HU-6 anchors (25 anchors × ~28 lookalikes each = 700; final lookalike count per anchor balances 30x reference-spot density target).

**Anchors covered in FULL:** HU-2 axis (5 anchors), HU-3 axis (5 anchors), HU-4 axis (5 anchors), HU-5 axis (5 anchors), HU-6 axis (5 anchors). Excludes HU-6.5 (already adjudicated CALL by owner; in solver-verification queue). HU-6.5 anchor itself is not relabelled; lookalikes from HU-6 anchors that are similarity-band-close to HU-6.5 inherit the adjudication if the variation_axis preserves the board (per §(a) item 4 propagation rule from generator-fix dispatch).

**Generation:**
- Pool: ~3000 from `scripts/generate_hu_situations.py` (V2 patched generator) covering HU-2..HU-6.
- Filter: similarity-band selection per architect's distance threshold (already committed in 1.5-D.3 PILOT V2; same threshold applies).
- Output: `data/hu_corpus/full_HU2_HU6/situations.jsonl` (700 entries).

**Labelling:**
- 5 fresh Sonnet labellers (NEW pool; not L1..L5 from PILOT V2 — fresh draw to avoid same-pool overfit).
- Calibration: each labeller passes ≥20/24 (or ≥20/28 per current calibration scheme) + GTO-reversal anchors all correct.
- Opus tier-up: non-unanimous Sonnet hands sampled by 1 Opus labeller per §4.3 tier-up rule.
- Consensus rule: ≥4-of-5 → consensus; 3-2 → solver verification + majority; 2-2-1 OR Opus DISAGREES on 3-2 → owner-arbitrated.

**Outputs:**
- `data/hu_corpus/full_HU2_HU6/situations.jsonl` (700 entries).
- `data/hu_corpus/full_HU2_HU6/raw_labels.jsonl` + 5 per-labeller files (5×700 = 3500 entries).
- `data/hu_corpus/full_HU2_HU6/calibration_results.jsonl` + 5 per-labeller files.
- `data/hu_corpus/full_HU2_HU6/consensus.jsonl` (700 entries).
- `data/hu_corpus/full_HU2_HU6/opus_tier_up.jsonl` (non-unanimous Sonnet sampled by Opus).
- `data/hu_corpus/full_HU2_HU6/similarity_distance_audit.jsonl`.
- `data/hu_corpus/full_HU2_HU6/labeller_brief.md`.
- `review/comms/BUILDER_REPORT_PHASE15D3_FULL_2026-05-10.md` — execution log + flagged issues + per-axis confidence summary + owner-arb surface (if any).

**Gate:**
- Base ≥4-of-5 labeller-consensus rate ≥80% (matches pilot's 82%). Effective consensus rate after Opus tier-up resolves 3-2 splits should land in ~95% range (matches pilot's 96%).
- Owner-arbs surface as PR-level artifacts; orchestrator surfaces to owner BEFORE merging the FULL PR.

**STOP conditions** (per CLAUDE.md §5):
- Generator produces stale composition/action_summary fields when board mutates → BUILDER must FIX in generator (not workaround) OR explicitly flag as architect-hat consult before firing labelling. (PILOT V2 had stale fields — labellers correctly read board fields and ignored stale composition; for FULL builder must decide whether to fix-the-fields or accept-the-staleness with explicit architect-hat consult flag.)
- Calibration contamination via grep returns `expert_action`/`expert_reasoning`/`oracle_action` fields → BUILDER must use SANITIZED JSONL extracts per §(c) below.
- API rate-limit cascade replays beyond designed-throttle → BUILDER must throttle-aware-batch per §(c) below.
- Anchor consensus from PILOT V2 contradicts FULL labellers on shared lookalikes (none expected since anchors are partitioned HU-1 vs HU-2..HU-6, but flag if it occurs).

## Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT modify reference-set design (`design/hu_reference_set/`)
- ❌ Does NOT modify §4.3 labelling-pipeline architecture (5-labeller + Opus tier-up + consensus rule)
- ❌ Does NOT modify §4.4 corpus-assembly architecture (similarity-band + ~30x density)
- ❌ Does NOT include any HU-1 axis lookalikes (those are in PILOT V2 / pilot_50_v2/)
- ❌ Does NOT relabel HU-6.5 anchor (already adjudicated in PR #338)
- ❌ Does NOT use solver output as training label
- ❌ Does NOT relax pilot gate
- ❌ Does NOT improvise on STOP conditions

## Pilot V2 owner-adjudications baked in

For any HU-2..HU-6 lookalike whose variation_axis is `villain_bet_sizing` AND anchor board is unchanged AND anchor itself was owner-adjudicated (HU-6.5 → CALL): inherit the owner-adjudication per generator-fix dispatch §(a) item 4 propagation rule. Apply to consensus.jsonl row with explicit notes citing the source PR.

For HU-1.4-LK-04 and HU-1.4-LK-05 (new owner-adjudications in this comm): these are HU-1 axis lookalikes already in pilot_50_v2/consensus.jsonl with consensus_action=null. Builder updates pilot_50_v2/consensus.jsonl in a SEPARATE small-PR (or as part of FULL PR's data layer) to populate consensus_action=CALL + add notes citing this dispatch §(a). This is required before 1.5-D.4 corpus assembly (1.5-D.4 reads from both pilot_50_v2/consensus.jsonl AND full_HU2_HU6/consensus.jsonl).

Owner-arb propagation for HU-2..HU-6 (NEW spots): if any HU-2..HU-6 spot triggers owner-arb (consensus_kind = 3-2 with Opus disagree, OR 2-2-1+), surface to orchestrator via BUILDER_REPORT comm; orchestrator surfaces to owner before merging FULL PR.

---

# (c) Architect-hat decisions (orchestrator commits WHAT/WHEN; builder-architect decides HOW)

## (c.1) Sanitized JSONL extracts for calibration

**Orchestrator commits:** Calibration JSONL extracts that labellers grep MUST be sanitized to strip `expert_action`, `expert_reasoning`, `oracle_action`, and any other forward-leaking fields before labellers see them. This is a hard requirement for FULL.

**Why:** PR #344 PILOT V2 had 4th-instance contamination (L2 + L4 self-disclosed grep returning full rows). QC verdict (PR #346) accepted the deferral with note "FULL HOLDs on sanitized-JSONL-extract infrastructure." Pool ability shown by L1's clean 26/28 score in calibration; sanitization preserves transparency without blocking labellers' independent reasoning.

**Builder-architect-hat decides HOW:**
- Where the sanitization step lives (pre-extract script, post-extract sanitizer, on-disk-cleanup-then-grep, etc.)
- Which fields to strip beyond the named three (e.g., metadata fields that imply expert_action)
- How to verify sanitization (sample-check after extraction; assert grep returns no forbidden field)
- Whether to also sanitize labelling-pool data (situations.jsonl, raw_labels.jsonl) — likely YES for raw_labels (labellers shouldn't see other labellers' answers) but NO for situations (situation data is the prompt input).

**Verification gate:** Builder report must include explicit grep-result for each forbidden field returning ZERO matches across calibration + raw_labels output files BEFORE FULL labelling fires.

## (c.2) Throttle-aware batching for 14x scale

**Orchestrator commits:** PILOT V2 saw API rate-limit cascade with 4/5 labellers dying on initial parallel dispatch (per builder report; QC verified clean recovery via serial-overlap retry, but cascade increased wall-clock from ~10min to ~30min). FULL labelling is 3500 LLM calls (5 labellers × 700 spots) + Opus tier-up sampling — 14x the pilot's 250 calls. Without throttle-awareness, cascade likely repeats at scale and may corrupt batch state.

**Why:** 14x-scale rate-limit cascade with the same retry pattern would either (a) succeed but consume ~hours of serial wall-clock, or (b) fail mid-batch with partial-state on disk, requiring manual recovery. Both outcomes violate quality-default + STOP > improvise.

**Builder-architect-hat decides HOW:**
- Concurrency limit per labeller pool member (e.g., max-N-concurrent or token-bucket)
- Backoff strategy (exponential, jittered, retry-after-header-aware)
- Mid-batch durability: append-only output writes so a crash leaves partial-batch recoverable without re-running completed work
- Pool design: separate per-labeller pools? Shared pool with priority? Architect's call.
- Wall-clock budget: builder estimates expected wall-clock for FULL given the chosen design + reports in BUILDER_REPORT before FULL fires.

**Verification gate:** Builder report must document the chosen design + concurrency limit + estimated wall-clock + a recovery-resumption test (kill mid-batch; resume; assert no duplicate or missing entries).

## (c.3) Stale composition/action_summary fields in generator

**Orchestrator commits:** PILOT V2 generator produced situations where `composition` and `action_summary` fields described the ANCHOR (e.g., "set of tens; turned set on rainbow"; "Turn Tc rainbow no FD") even when the lookalike's board mutated away (e.g., turn 6c instead of Tc, hero now has TT overpair not set). Labellers correctly read board fields and ignored stale composition (verified via raw_labels reasoning audit; all 5 labellers said "TT overpair on 8h5c2d6c" not "set of tens"); pilot labels are valid.

For FULL: builder-architect-hat decides whether to (a) FIX the generator to mutate composition + action_summary alongside board fields, or (b) ACCEPT the staleness with explicit architect-hat consult flag in builder report (rationale: labellers read structured fields, prose is decorative).

**Why:** The fields are decorative for labellers (per PILOT V2 evidence) but represent a generator-correctness gap. Path (a) is the quality-default; path (b) is acceptable if builder explicitly justifies why the prose-decoration claim holds at FULL scale (3500 labelled outputs vs PILOT's 250).

**Verification gate:** Builder chooses path; documents in BUILDER_REPORT; if path (b), QC will assess whether the architect-hat justification holds.

---

# QC stream — what you audit (post-PR; standalone, ~25-30 min for FULL)

10-item audit:

1. Diff scope strict per dispatch (data files in `data/hu_corpus/full_HU2_HU6/` + builder report; no source/prompt/model edits beyond §(c) infrastructure work).
2. §(c.1) sanitized-JSONL-extract verification: grep for `expert_action`, `expert_reasoning`, `oracle_action` across calibration + raw_labels output files → ZERO matches.
3. §(c.2) throttle-aware-batching design: documented in builder report with concurrency limit + backoff + recovery-resumption test passed.
4. §(c.3) generator path (a vs b): builder choice documented; if (b), QC assesses architect-hat justification.
5. 700 spots × 5 labellers = 3500 raw_labels entries; per-labeller counts 700 each; per-spot counts 5 each.
6. Calibration ≥20/24 (or ≥20/28) + GTO-reversal anchors all correct for all 5 labellers; failed labellers NOT in raw_labels.jsonl.
7. Bucket-first compliance + solver-vs-labels separation in labeller_brief.
8. Consensus rule applied: ≥4-of-5 → consensus; 3-2 → tier-up + majority/owner-arb; 2-2-1+ → owner-arb.
9. Per-axis confidence summary (HU-2..HU-6) in builder report; gate ≥80% base ≥4-of-5 rate.
10. TC-X-DISPATCH-COMPLIANCE per this comm.

QC also assesses: any new owner-arbs surfaced (Opus disagree on 3-2; or 2-2-1+ splits); HU-6.5-propagation lookalikes (if any) correctly inheriting the owner-CALL adjudication; pilot_50_v2/consensus.jsonl update for HU-1.4-LK-04/05 = CALL applied (separately or in FULL PR).

QC routing per `feedback_qc_routing_when_standalone_active.md`. Heartbeat + cross-post per protocol.

---

# (d) Solver-verification queue (recurring annotation pattern)

Per `feedback_solver_verification_queue.md` (memory rule): owner-arbitrated spots flagged "check solver later" accumulate here. Queue MUST drain before Phase 1.5-D.4 (HU model retrain) ships.

**Current queue (after this comm):**

| spot_id | source PR | hero / board / action | owner adjudication | timestamp |
|---|---|---|---|---|
| HU-6.5 | PR #338 | Qd9h on 7h6c5s2d8d; BB 150% overbet (20.6bb into 13.7bb); pot odds 37.5% | CALL | 2026-05-10 |
| HU-1.5-LK-10 | PR #338 (this PR ref'd to PR #343) | Qd9h on 7h6c5s2d8d (same as HU-6.5); BB ~112% overbet (56.25bb into 50bb); pot odds ~35%. Note: labeller-pool 4-1 FOLD shift at 112% vs 5/5 CALL at 75% is solver-priority confirmation item per QC PR #346 | CALL | 2026-05-10 |
| HU-1.4-LK-04 | PR #344 (this comm) | TsTd on 8h5c2d6c; BB 33% probe (4bb into 12bb); SB OOP HU; eff 60bb. TT overpair on coordinated turn (4-5-6-7-8 OESD + flush draw); pot-control OOP CALL | CALL | 2026-05-10 |
| HU-1.4-LK-05 | PR #344 (this comm) | TsTd on 8h5c2d7c (turn 7c instead of 6c; otherwise identical to HU-1.4-LK-04); same straight-texture + flush-draw considerations | CALL | 2026-05-10 |

**Drain protocol** (per memory rule):
1. Confirm solver online
2. Run each queued spot through solver verification
3. Document agree/disagree per spot
4. If solver disagrees with owner adjudication on any spot: surface to owner for re-judgment BEFORE retrain corpus is finalized
5. Document outcome in `SOLVER_VERIFICATION_QUEUE_DRAINED_<date>.md` comm

**Trigger:** Before authoring the Phase 1.5-D.4 dispatch comm, orchestrator MUST check solver-status:
- Solver still offline: HOLD 1.5-D.4 with explicit owner-gate ask
- Solver online: DRAIN queue first (per protocol above) BEFORE 1.5-D.4 dispatch

This rule persists across orchestrator sessions via memory file `feedback_solver_verification_queue.md`.

---

# Owner — informational

- Standing directive: orchestrator merges this dispatch + builder FULL PR + QC verdict autonomously per quality default (post-owner-adjudication on any new owner-arbs that surface in FULL labelling).
- HU-1.4-LK-04 + HU-1.4-LK-05 + HU-1.5-LK-10 + HU-6.5 are the current solver-verification queue (4 spots; all CALL).
- After FULL PR + verdict merge → orchestrator authorizes Phase 1.5-D.4 (HU model retrain on 59-surface, from-scratch per §4.5) AFTER solver-queue drain (or solver-still-offline owner-gate ask).
- Loop CONTINUES through 1.5-D.4 → 1.5-E (router/coaching) → Phase 2 D5 (deferred per blueprint).

---

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `615feee` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.3 PILOT V2 merged: master `4432f68` (PR #344)
- v2 QC verdict PASS · 0/0/0 merged: master `b790524` (PR #346)
- Builder observation merged: master `615feee` (PR #347)
- Generator-fix dispatch: master `60bb850` (PR #343)
- 1.5-D.3 v1 PILOT merged: master `a2b97e2` (PR #339); v1 QC verdict: master `2f04f34` (PR #342; PASS-WITH-FINDINGS · 0/1/0 SHOULD_FIX)
- HU-6.5 owner-adjudication: master `c54eab1` (PR #338)
- HU reference set in master: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + per-axis breakouts (HU-2..HU-6 axes)
- Architect's design memo §4.3 + §4.4 + §4.5: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Generator file (V2 patched): `scripts/generate_hu_situations.py`
- Generator unit tests: `scripts/test_generate_hu_situations.py` (8 tests; PASS)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_river_rats_team_structure.md`, `project_qc_heartbeat_convention.md`

**Status: HU-1.4-LK-04 + HU-1.4-LK-05 adjudicated CALL with solver-flag (queue updated). HU-1.5-LK-10 re-confirm acknowledged. Phase 1.5-D.3 FULL fires LEAD-PROGRAMMER (700 lookalikes from HU-2..HU-6). Architect-hat decisions §(c.1) sanitized-JSONL-extract calibration + §(c.2) throttle-aware batching are commit-WHAT; builder-decides-HOW. §(c.3) stale-composition path (a vs b) is builder-architect choice. Solver-verification queue tracked for pre-1.5-D.4 drain. Loop CONTINUES through FULL → QC → solver-queue drain → 1.5-D.4 dispatch.**
