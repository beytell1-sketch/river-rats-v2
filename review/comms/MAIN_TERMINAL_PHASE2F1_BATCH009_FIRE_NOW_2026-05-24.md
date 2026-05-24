---
date: 2026-05-24
from: Orchestrator (Main Terminal, autonomous loop)
to: Builder (lead-programmer + architect + gto-expert hats)
re: Phase 2-F1 batch_009 generation — PILOT for new positional_action_chain scenarios module
status: FIRE NOW
type: PILOT (per `feedback_pilot_first_for_long_jobs` — single batch first; batches 010-014 conditional on owner sign-off of pilot result)
target_branch: builder/phase2-f1-batch009-pilot-2026-05-24 (NEW; rooted at master 04ef681)
authorization: explicit MAIN_TERMINAL_* trigger per `feedback_explicit_action_trigger`
---

# MAIN_TERMINAL — Phase 2-F1 batch_009 PILOT FIRE NOW

Builder, you are the named author per `feedback_named_author_builds_not_polls`. Next tick AUTHORS.

## Authorization

PR #471 (B1.1 patch) merged at 04ef681. The positional_action_chain_scenarios module now ships with:
- T21 self-consistency fixed (declared chain_shape=CHECK_RAISE)
- VALIDATION-1 covers all 24 templates
- `test_no_floor_regression` guards the 5 A1 floors

Scenario module is production-ready. You fire batch_009 generation as the PILOT for the new scenarios.

## Scope (single-design commitment, no menus)

Generate batch_009 = 50 hands using the new `positional_action_chain_scenarios.py` module + the existing batch driver pattern from batches 001-008.

### Step 1 — Generate 50-hand input (`batch_009_50hand.jsonl`)

- Use `generate_phase_2f_chain_quota(rng_seed=20260524)` to produce 24 enumerated chain specs
- Stratified-fill the remaining 26 slots via existing corpus_revision_scenarios building blocks (match the pattern used by batches 001-008's generators in `scripts/generate_4way_lookalikes_700.py` or similar)
- Concatenate to 50 hands; ensure all schema fields populated (hero_cards, board, action_history, pot_bb, to_call_bb, stack_size_bb, facing_bet, hero_position, villain_positions, street, opener_position)
- Output: `data/4way_corpus/full_700/batch_009_50hand.jsonl`

### Step 2 — Verify quotas (PILOT acceptance pre-check)

Before dispatching labellers, count on the 50-hand input:
- Facing-raise: ≥10 (was floor 10 on 24-spec; should land at 10-15 on 50-hand)
- River: ≥5
- Position-balance: each of {UTG, MP, CO, BTN, SB, BB} ≥1; floor target ≥5/seat per RATIFICATION_A1 (extrapolated)
- Sandwich: ≥4
- Top-12: 12/12 anchors covered

If any floor breaks, STOP and report — escalate to orchestrator.

### Step 3 — Spawn 5 labelling subagents per labeller per PROCESS_GUIDE §1.1

- Each labeller (L1..L5) labels all 50 hands
- ≤10 hands per labelling subagent → 5 chunks per labeller × 5 labellers = 25 parallel subagents
- (Alternative: split per chunk: 1 subagent runs L1+L2+...+L5 for 10 hands = 5 subagents × 10 hands. Use judgment matching existing batch pattern.)
- Each labeller subagent reads:
  - `data/4way_labeller_brief.md` (v2 — split sizing schema)
  - Their assigned chunk of `batch_009_50hand.jsonl`
  - Optionally: prior labels from same labeller_id in earlier batches for persona continuity
- Output: append to `batch_009_raw_labels_labeller_{1..5}.jsonl`
- Use v2 schema natively: `predicted_bet_pct` for BET, `predicted_raise_to_bb` for RAISE

### Step 4 — Opus tier-up on non-unanimous spots

After all 5 labellers complete:
- Identify spots with 3-2 or 4-1 splits (modal action lacks unanimous agreement)
- Dispatch Opus tier-up subagent on those spots → `batch_009_raw_labels_opus_tierup.jsonl`
- Opus also labels in v2 schema (`labeller_id="opus_tierup"`)

### Step 5 — Run normalizer

- For each raw labeller file: `python river-rats-core/sizing_schema_normalizer.py --apply <input> --context batch_009_50hand.jsonl --output <input>_v2.jsonl --audit batch_009_normalizer_audit.jsonl`
- For Opus: same pattern (now supports str labeller_id post-A0.1.1)
- Expected malformed rate: ~0% (labellers writing v2 schema natively per brief v2 — no legacy ambiguity)
- If malformed rate > 5% on batch_009, STOP and report (unexpected — v2 brief should eliminate dual-semantics)

### Step 6 — Compute consensus_v2

- Use `compute_consensus_v2()` from `river-rats-core/sizing_schema_normalizer.py` per A0.2/A0.3 pattern
- Output: `data/4way_corpus/full_700/batch_009_consensus_v2.jsonl`
- Spots that fail sizing-consensus (≥3 malformed in action-voters) route to `batch_009_owner_arb_queue_normalizer.jsonl`

### Step 7 — Build summary report

Author `review/comms/BUILDER_REPORT_PHASE2F1_BATCH009_PILOT_2026-05-24.md`:
- File manifest (raw × 5 + opus + normalized × 6 + consensus + audit + owner-arb)
- Per-floor count on materialized batch_009 (compare to RATIFICATION_A1 floors)
- FL5 illegal-action sentinel count (target: 0/250)
- Action distribution
- Consensus state breakdown (all-agree / 4-of-5 / 3-2 / owner-arb)
- Opus tier-up dissent rate
- Malformed-rejected count from normalizer audit
- Owner-arb queue summary
- Cumulative: 400 + 50 = 450/700 = 64.3%

### Step 8 — Ship PR

Single PR with all batch_009 artifacts:
- `builder: Phase 2-F1 batch_009 PILOT — first batch with new positional-chain scenarios`
- 10+ files (50hand + 5 raw + 1 opus + 5 v2 + 1 consensus + 1 audit + 1 owner-arb + 1 builder report) ≈ 15 files
- Branch base = master 04ef681

## PILOT ACCEPTANCE CRITERIA (per `feedback_pilot_first_for_long_jobs`)

- FL5 sentinel: 0/250 illegal Sonnet labels (8th-batch baseline; do not regress)
- Malformed-rejected: ≤5% per labeller (much lower than 15% A0.x gate since brief v2)
- All 5 A1 floors met on materialized 50-hand output
- Consensus rate: ≥90% (batches 002-007 averaged 94-98%)
- Opus tier-up dissents: track but don't gate (PILOT is for spotting issues, not enforcing limits)

## POST-SHIP

When batch_009 PR opens, orchestrator dispatches QC pre-merge audit. If QC PASS, orchestrator HALTS the autonomous loop and writes a HALT summary for owner. Owner reviews pilot result before authorizing batches 010-014.

**Do NOT pre-fire batches 010-014.** Pilot gate is owner-only per `feedback_pilot_first_for_long_jobs`.

## STOP CONDITIONS

STOP and report BLOCKED if:
- Step 2 floor pre-check fails (insufficient diversity from scenario module)
- Any labeller subagent produces >5% FL5 illegal votes
- Normalizer malformed-rejected rate exceeds 5% per labeller
- Consensus rate drops below 80% (unexpected; batches 001-008 averaged 96%)
- Any subagent reports a STOP CONDITION

Per CLAUDE.md protocol 5: NEVER improvise. Escalate to orchestrator.

## Cost budget

This is the heavy work of the night. Cost cap from loop authorization: 4hr aggregate subagent runtime. Budget for batch_009:
- 25 labeller subagents × 5-10 min = ~2-4 hours parallel runtime
- Opus tier-up: ~10 min
- Normalizer + consensus: ~5 min
- Report authoring: ~10 min

If approaching 3.5 hours aggregate, prioritize finishing labellers in flight; defer Opus tier-up to a follow-up if needed.

---

**Authorization**: this directive addressed to Builder by name with named scope = sufficient per `feedback_listen_to_orchestrator_always`. No further owner approval before authoring.
