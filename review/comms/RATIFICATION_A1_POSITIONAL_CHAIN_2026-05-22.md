---
date: 2026-05-22
from: Architect (Phase 2-F1 — A1 ratification)
to: Builder · QC · Owner · Orchestrator
re: RATIFICATION of `DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md` — scope-trimmed to Phase 2-F1 (corpus-only, STAGED)
status: RATIFIED with scope trim and expanded quotas (single-commit; no v2 rewrite)
gates: orchestrator dispatch (B1 STANDBY directive); QC pre-merge on builder PR
references:
  - review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md (PRESERVED as historical)
  - review/comms/DRAFT_PHASE2F_READINESS_SCORECARD_2026-05-13.md (owner-approved scope)
  - review/comms/DRAFT_AUDIT_CORPUS_LABEL_DISTRIBUTION_2026-05-13.md (gap evidence)
  - review/comms/BUILDER_REPORT_PHASE2E_FULL_BATCH008_2026-05-22.md (400/700; 6 batches remain)
---

# A1 RATIFICATION — Positional Action-Chain Dimension

## TL;DR

**Decision:** RATIFY v1 blueprint **with two scope-trim edits and one quota-expansion** —
a single commitment, not a menu.

1. **Trim to corpus-only (Phase 2-F1):** the chain-fingerprint dimension, the scenario module,
   the 6-D stratified sampler, and the per-batch enumerated quota are ALL **IN** scope. Any
   reference in v1 to prompt rewrite (FL6, AMENDMENT 3, KB v1.4) is **OUT** of scope for A1
   and deferred to Phase 2-F2. The brief stays at v2 (split sizing schema; landed via A0.3c).
2. **Update batch math:** v1 §7.2 assumed 14 batches; actual remaining = **6 batches (009-014)**,
   300 hands total. Quota math below reflects this.
3. **Expand the per-batch enumerated quota** (was 20/50 top-12 in v1) to **24/50** to absorb the
   scorecard's three new mandatory floors (facing-raise ≥10, river ≥5, position balance ≥5 each).

The 7-tuple definition, the 274-chain enumeration (108 flop + 94 turn + 72 river), the
chain-shape enum, the `BET_CALL`/`BET_RAISE`/`CHECK_RAISE` semantics, the canonical-ordered
hash, the scenario module path, and the function signatures from v1 are **accepted as-is**.

## What v1 commits to (accepted)

| § | Commitment | Status |
|---|---|---|
| §2.1 | Chain fingerprint = 7-tuple (street, hero_pos, aggressor_pos, callers_chain, raiser_pos, raise_target_pos, chain_shape) | ACCEPTED |
| §2.2 | Hash over ordered tuple; callers_chain NOT sorted | ACCEPTED |
| §3 | Chain-shape enum: {OPEN, BET, BET_CALL, BET_CALL_CALL, BET_RAISE, CHECK_RAISE, MULTI_AGGR} | ACCEPTED |
| §4 | 274 enumerated chains: 108 flop + 94 turn + 72 river | ACCEPTED (counting methodology is the design basis) |
| §6.1 | File path: `river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py` | ACCEPTED (matches existing 9-module convention) |
| §6.3 | Function signatures: `generate_chain_scenarios`, `enumerate_top_12_chains`, `generate_phase_2f_chain_quota`, `validate_chain_fingerprint` | ACCEPTED |
| §6.5 | Validation gate before corpus assembly (`compute_chain_fingerprint(spec) == spec.chain_fingerprint`) | ACCEPTED |
| §6.6 | Bug-awareness checklist CFP-1 .. CFP-6 | ACCEPTED |
| §7.1 | Sampler: 8-D → 6-D (chain_shape, street, position, spr_bucket, hand_class, board_texture) + mandatory quota | ACCEPTED |
| §7.3 | Backward-compat: `action_context_from_chain()` derives v3 field from fingerprint | ACCEPTED |

## What v1 commits to (DEFERRED to Phase 2-F2 — OUT of A1 scope)

- v1 references AMENDMENT 3 to `data/4way_labeller_brief.md` (FL6 + chain phrasing). **Out** — Phase 2-F2 task A2a.
- v1 references `prompts/gto_labeller_v3.5.md` rewrite (BLOCKERS 1-3). **Out** — Phase 2-F2 task A2b.
- v1 references `knowledge/three_way_gto.md` v1.4 sync. **Out** — Phase 2-F2 task A2c.
- v1 §8 ratification checklist item "builder re-derives top-12 frequencies from BATCH-001..007":
  **CARRIED into B1** as a pre-flight artifact (builder must produce
  `phase2f1_top12_frequency_audit.md` from existing `batch_00{1..7}_consensus_v2.jsonl`
  before scenario authoring; uses v2 normalized consensus files per A0.3b backfill).
- v1 §9 open item "20-hand pilot of chain quota before full fire": **CARRIED into B1** as the
  20-hand micro-batch yield test pattern (per blueprint §3.5 in scenario expansion v3.5 conventions).

The brief stays **v2** (split sizing schema, landed A0.3c on master via PR #464). **No further
brief change in Phase 2-F1.** Labellers in batches 009-014 operate against v2 brief unchanged.

## Updated batch math (state delta from v1 → today)

| Quantity | v1 assumption (2026-05-13) | Today (2026-05-22) |
|---|---|---|
| Batches done | 7 (350 hands) | **8 (400 hands)** |
| Batches remaining | 7 (350 hands) | **6 (300 hands; batches 009-014)** |
| New-dimension applies to | "Phase 2-F batches" (ambiguous) | **batches 009-014 ONLY** (not retroactive to 001-008) |
| Total Phase 2-F1 target | 14×50 = 700 (in v1 §7.2) | **6×50 = 300** new hands; combined corpus = 700 |
| Hands subject to A1 quotas | 700 (v1) | **300 (009-014)** |

**Retroactivity:** Batches 001-008 are **frozen** (already normalized to split-schema via A0.2 +
A0.3b backfill; consensus_v2 files are the canonical record). The A1 quotas apply to **batches
009-014 forward only**. Drift-analysis on batches 001-008 against A1 quotas is informational, not
a re-label trigger (re-label is Phase 2-F2 B2 scope).

## EXPANDED per-batch quotas (supersedes v1 §5.2)

Phase 2-F1 expands v1's 20-hand top-12 quota to **24 hands enumerated** per 50-hand batch, to absorb
the scorecard's three new mandatory floors. Distribution within those 24 is engineered so each floor
is met without double-counting (overlap is allowed and expected — a hand can satisfy more than one
quota simultaneously).

### A1 per-batch mandatory quotas (batches 009-014; 6 batches; 300 hands)

| Quota | Floor per batch | Cumulative (009-014) | Rationale |
|---|---:|---:|---|
| **Facing-raise** (chain_shape ∈ {BET_RAISE, CHECK_RAISE, MULTI_AGGR}) | **≥10** | **≥60** | Corpus gap: 0/337 facing-raise (audit §2) |
| **River** (street = 'river') | **≥5** | **≥30** | Corpus gap: 0/337 river (audit §1, §5) |
| **Position balance** — each of {BTN, CO, MP, UTG, SB, BB} as hero_pos | **≥5 each** (= 30 of 50) | **≥30 per position** | Corpus skew: HJ 5.9%, EP 3.9%, UTG 7.7% (audit §5) |
| **Top-12 chain coverage** — each top-12 chain fingerprint | **≥1 each** | **≥6 each** | v1 §5.3 floor preserved |
| **Sandwich position** — hero is positionally between two villain actors on the current decision street | **≥4** | **≥24** | KB/prompt gap: 0 sandwich examples (scorecard §3) |

**Note on positions:** The scorecard quota mentions {BTN, CO, MP, UTG, SB, BB}. The chain-fingerprint
spec uses 6-max positions {UTG, HJ, CO, BTN, SB, BB}. **Resolution:** the scenario module emits both
labels — `hero_pos_6max ∈ {UTG, HJ, CO, BTN, SB, BB}` (used by chain fingerprint), and `hero_pos_class
∈ {EP, MP, CO, BTN, SB, BB}` (used by quota; EP = {UTG, UTG+1}, MP = {HJ, LJ}). Builder treats MP and
UTG as scorecard-class buckets and ensures each bucket gets ≥5 per batch. EP and HJ in 6-max collapse
into MP for quota purposes.

### A1 per-batch slot allocation (24 of 50)

| Slot block | Count | Quotas satisfied |
|---|---:|---|
| 12-chain anchor set (one per top-12) | 12 | Top-12 chain floor; subset hits facing-raise (rank 9), river (rank 11), turn (ranks 8, 10) |
| Facing-raise expansion (chains beyond rank 9) | 6 | Facing-raise ≥10 (4 from anchor at rank 9 covers 1; need 9 more; allocate 6 here + 3 from sandwich overlap) |
| River expansion (chains beyond rank 11) | 4 | River ≥5 (anchor at rank 11 = 1; need 4 more here) |
| Sandwich enforcement (hero positionally sandwiched) | 2 | Sandwich ≥4 (overlap with facing-raise + river anchors picks up 2 more) |
| **Enumerated subtotal** | **24** | All A1 mandatory floors met |
| 6-D stratified fill (chain_shape × street × position × spr × hand_class × board_texture) | 26 | Position balance ≥5 per scorecard-class + natural tail diversity |
| **Per-batch total** | **50** | |

**Floor verification (per batch):**
- Facing-raise: 1 (anchor rank 9) + 6 (expansion) + ≥3 (sandwich overlap with BET_RAISE) = ≥10 ✓
- River: 1 (anchor rank 11) + 4 (expansion) = ≥5 ✓
- Position balance: 4 anchors per position avg (from 12-chain set) + ≥1 each from stratified fill = ≥5 ✓
- Top-12: 12 explicit anchors = ≥1 each ✓
- Sandwich: 2 explicit + ≥2 overlap = ≥4 ✓

### 12-chain anchor set (v1 §5.1, accepted as-is)

| Rank | Chain (short label) | Anchors per batch |
|---|---|---:|
| 1 | flop IP-closing BET | 1 |
| 2 | flop OOP-early BET_CALL | 1 |
| 3 | flop OOP-early BET (BB-folded) | 1 |
| 4 | flop IP-closing BET_CALL | 1 |
| 5 | flop OOP-early BET_CALL_CALL | 1 |
| 6 | flop OOP-early OPEN | 1 |
| 7 | flop OOP-middle BET_CALL | 1 |
| 8 | turn IP-closing BET | 1 |
| 9 | flop OOP-early BET_RAISE | 1 |
| 10 | turn OOP-early BET_CALL | 1 |
| 11 | river IP-closing BET | 1 |
| 12 | flop OOP-middle BB-donk | 1 |
| | **Top-12 anchor total** | **12** |

Top-12 frequency table in v1 §5.1 is the **architect's prediction**; B1 re-derives from
`batch_00{1..8}_consensus_v2.jsonl` and produces `phase2f1_top12_frequency_audit.md` as a pre-flight
artifact (carry-over from v1 §9). If the re-derived ranking differs materially (>2 rank-positions
on any chain), B1 escalates back to architect via `review/comms/` before authoring the module.
The 12 slots are 1-per-anchor regardless of re-derived weights — Phase 2-F1 prioritizes coverage
breadth over natural-frequency proportionality. Proportional reweighting is a Phase 2-F2 task.

## Acceptance check (carried from v1 §7 / §8)

Builder's PR for B1 must demonstrate:

1. File exists at `river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py`
   and is git-tracked (`git ls-files | grep positional_action_chain_scenarios.py`); per TC-23.
2. `enumerate_top_12_chains()` returns 12 `ChainFingerprint` namedtuples matching v1 §5.1 rank order.
3. `generate_phase_2f_chain_quota(rng_seed, forbidden_fingerprints)` returns **24** SituationSpec
   instances (not 20) covering all 5 A1 mandatory quotas (Facing-Raise, River, Position-balance,
   Top-12, Sandwich) for any rng_seed.
4. `validate_chain_fingerprint(spec, expected_chain)` raises AssertionError with a precise diff
   when the spec's reconstructed fingerprint mismatches `expected_chain`.
5. `compute_chain_fingerprint(spec)` helper added to `_scenario_utils.py`; walks `action_history`
   and reconstructs the 7-tuple per v1 §2.1.
6. **20-hand micro-batch yield test** produces a deterministic sample (fixed seed) that passes
   the quota checker; results saved to `review/comms/B1_MICRO_BATCH_YIELD_TEST_2026-05-XX.md`.
7. **Top-12 frequency audit** produced as `review/comms/phase2f1_top12_frequency_audit_2026-05-XX.md`
   from existing `batch_00{1..8}_consensus_v2.jsonl`. Escalation gate: if rank shift >2 on any chain,
   builder posts query comm and waits for architect ratification before module authoring.
8. Bug-awareness checklist CFP-1 .. CFP-6 each has at least one passing unit test in
   `river-rats-core/tests/test_positional_action_chain_scenarios.py`.
9. QC pre-merge audit per `feedback_qc_required_before_approval.md` (MILESTONE PR — first 9th-D ship).

## Single-design commitments (no menus)

- **Top-12 frequencies are architect's prediction**, re-derived by B1 from v2 consensus files; rank
  shifts ≤2 are accepted silently; shifts >2 escalate. **One** policy, not a menu.
- **24 enumerated slots per batch**, not 20 or 30. **One** number.
- **Sandwich = positional-only** (hero in seat-order between two villain actors on the current
  decision street). Range-decomposition definitions of sandwich are Phase 2-F2 scope.
- **Position-balance taxonomy = scorecard 6-class** {BTN, CO, MP, UTG, SB, BB}; 6-max EP/HJ
  collapse into MP for quota counting. **One** taxonomy.
- **Validation gate is blocking**, not a warning. Specs that fail `validate_chain_fingerprint`
  are dropped from the batch before assembly, not normalised after.
- **Retroactivity policy: no re-spec of batches 001-008.** A1 applies forward-only.

## Items needing orchestrator attention before B1 fires

1. **Confirm the B1 STANDBY directive (file pair below) fires only after this RATIFICATION_A1 PR
   merges to master** — per `feedback_explicit_action_trigger.md`. Orchestrator's MAIN_TERMINAL
   fire-now is the trigger; builder does not auto-build off a ratification PR.
2. **Confirm QC's `feedback_spec_vs_infrastructure_code_drift.md` TC-23 EXISTENCE check uses
   `git ls-files` not `test -e`** — per `feedback_tc23_existence_must_be_git_tracked.md`.
   B1's PR must include the new scenarios file in git diff (untracked-only would fail).
3. **Phase 2-F2 sequencing:** A2a/A2b/A2c (brief AMENDMENT 3, prompt v3.5, KB v1.4) are explicitly
   deferred until Phase 2-F1 ships. Owner's STAGED decision is preserved here. No Phase 2-F2 work
   should ship in parallel with B1 absent owner re-gate.
4. **Solver-verify queue:** batch-008 added 5 spots (queue size now ~33). Per
   `feedback_solver_verification_queue.md`, queue must drain before any 1.5-D.4-equivalent retrain
   (Phase 2-G). Phase 2-F1 will add more spots (forecast: ~3-6 per batch over 6 batches).
   Orchestrator queues this as a parallel workstream, not as a B1 blocker.
5. **A0 schema fix (PR #461)** is the upstream gate; verified MERGED (PR #464 batch-008 brief patch
   landed). A1 builds on top — no further A0 dependency.

## Files changed by this ratification

- **NEW (this commit):** `review/comms/RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md` (this file)
- **NEW (this commit):** `review/comms/MAIN_TERMINAL_PHASE2F1_B1_FIRE_NOW_2026-05-22.md` (STANDBY)
- **PRESERVED:** `review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md` (historical)
- **NO CHANGE:** `data/4way_labeller_brief.md` (stays v2)
- **NO CHANGE:** `prompts/gto_labeller_v3.4.md` (Phase 2-F2 scope)
- **NO CHANGE:** `knowledge/three_way_gto.md` (Phase 2-F2 scope)

End RATIFICATION_A1.
