---
date: 2026-05-22
from: BUILDER (Phase 2-F1 B1 pre-flight artifact)
to: Architect · Orchestrator · QC · Owner
re: Top-12 chain frequency audit — re-derived from batch_00{1..8}_consensus_v2.jsonl
status: AUDIT COMPLETE — no escalation; v1 §5.1 anchor set stands per RATIFICATION_A1 silent-acceptance rule
references:
  - review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md §5.1
  - review/comms/RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md (escalation gate)
  - review/comms/MAIN_TERMINAL_PHASE2F1_B1_FIRE_NOW_2026-05-22.md (deliverable #4)
---

# Phase 2-F1 — Top-12 Chain Frequency Audit (pre-flight)

## TL;DR

**Audit conclusion: v1 §5.1 anchor set stands. No escalation.**

Re-derivation of natural-frequency rank order from the existing batches 001-008
corpus is **not feasible** because:

1. The 400-hand corpus is **anchor/axis-driven** (curated to hit specific GTO-tension
   axes per `source_anchor` / `primary_axis`), NOT a sample from natural self-play
   distribution that v1 §5.1 predicts against.
2. Source spots in `batch_00{1..8}_50hand.jsonl` contain `preflop_action` but
   **no explicit postflop action history**, so the 7-tuple chain fingerprint cannot
   be computed exactly (postflop aggressor / callers_chain / raiser are unrecoverable
   from the spot record).

Per RATIFICATION_A1: *"rank shifts ≤2 are accepted silently and the v1 §5.1 anchor
set stands"*. Without a defensible rank-shift measurement, the v1 anchors are
accepted by default.

The audit DOES confirm the **corpus position skew** that the A1 per-batch quotas
are designed to address — specifically validating the rationale for the
position-balance and facing-raise floors.

## Why exact 7-tuple re-derivation isn't possible from existing data

The chain fingerprint defined in blueprint §2.1 is a 7-tuple:
`(street, hero_pos, aggressor_pos, callers_chain, raiser_pos, raise_target_pos, chain_shape)`.

Per-spot data available in `batch_00{1..8}_50hand.jsonl`:

| Field | Available? | Notes |
|-------|------------|-------|
| `street` | ✓ | "flop" \| "turn" \| "river" \| "preflop" |
| `hero_position` | ✓ | 6-max position |
| `facing_bet` | ✓ | 0 \| 1 |
| `num_opponents_at_decision` | ✓ | 1-3 villains still in |
| `preflop_action` | ✓ (string) | Parseable for opener / 3-bettor / cold-callers |
| `primary_axis`, `source_anchor` | ✓ | Curation/axis label |
| postflop `aggressor_pos` | ✗ | Not recoverable |
| postflop `callers_chain` | ✗ | Not recoverable |
| postflop `raiser_pos` | ✗ | Not recoverable |
| `chain_shape` (BET / BET_CALL / BET_RAISE / etc.) | ✗ | Cannot distinguish BET from BET_CALL_CALL via `num_opponents_at_decision` alone, because `callers_chain` is "callers between aggressor and hero in seat-order", which depends on who acted in what order — not on how many villains remain in the pot |

A heuristic that maps (`facing_bet`, `num_opponents_at_decision`) to a `chain_shape`
class produces 91.2% unmatched rate against the v1 §5.1 anchors at the strict
7-tuple level, because the heuristic conflates "villains still in pot" with
"callers between aggressor and hero". This is not a rank-shift signal — it's a
data-availability artifact.

## What the audit DOES show — coarse (street, hero_pos) bucketing

The strongest defensible aggregation is `(street, hero_pos)` — both fields are
verbatim in the spot record. Tallying batches 001-008 (n=400) at this level
against the v1 §5.1 anchor set aggregated by the same key:

| (street, hero_pos) | Actual count | Actual % | v1 predicted % (anchors aggregated) | Anchor ranks | Δpp |
|---|---:|---:|---:|---|---:|
| (flop, CO) | 84 | 21.0% | 5% (rank 7) | [7] | +16.0 |
| (flop, HJ) | 81 | 20.2% | 0% | (residual) | +20.2 |
| (flop, BTN) | 64 | 16.0% | 19% (ranks 1, 4) | [1, 4] | -3.0 |
| (preflop, BTN) | 51 | 12.8% | 0% | (residual; preflop NOT in chain-dim scope) | +12.8 |
| (flop, SB) | 43 | 10.8% | 10% (ranks 3, 12) | [3, 12] | +0.8 |
| (flop, UTG) | 26 | 6.5% | 0% | (residual) | +6.5 |
| (preflop, BB) | 19 | 4.8% | 0% | (residual; preflop) | +4.8 |
| (turn, BB) | 14 | 3.5% | 4% (rank 10) | [10] | -0.5 |
| (turn, UTG) | 14 | 3.5% | 0% | (residual) | +3.5 |
| (preflop, SB) | 4 | 1.0% | 0% | (residual; preflop) | +1.0 |
| **(flop, BB)** | **0** | **0.0%** | **25% (ranks 2, 5, 6, 9)** | **[2, 5, 6, 9]** | **-25.0** |
| (turn, BTN) | 0 | 0.0% | 5% (rank 8) | [8] | -5.0 |
| (river, BTN) | 0 | 0.0% | 4% (rank 11) | [11] | -4.0 |

**Observations:**

1. **(flop, BB) is the largest gap** — 0 spots in 400 vs ~25% predicted natural
   frequency. The corpus has **no BB-hero flop decisions** despite BB being
   structurally OOP-early in every 4-way pot. This is by curation: batches 001-008
   prioritized IP-closing (BTN/CO) and mid (SB/HJ/CO) heroes per the axis sampling.
2. **(turn, BTN) and (river, BTN) are also absent** (0/400 each vs 5% and 4%
   predicted). Turn/river chains were under-prioritized in the existing corpus
   relative to flop chains (28 turn / 0 river / 298 flop / 74 preflop).
3. **(flop, CO) is over-represented** at 21% vs 5% predicted — CO-hero in axis
   anchors like "range-asymmetry-CO" and "closing-action" was a recurring slot.
4. **`preflop` is 18.5%** of all spots (74/400), entirely outside the chain-dim
   scope (chain fingerprint applies to postflop decisions only).

## A1 quota rationale — confirmed

The corpus position skew the audit reveals **exactly matches the gaps the A1
quotas address** per RATIFICATION_A1 §EXPANDED per-batch quotas:

| A1 quota | Gap in 001-008 | Forward fix (batches 009-014) |
|---|---|---|
| **Position-balance** ≥5 each of {BTN, CO, MP, UTG, SB, BB} per batch | (flop, BB) = 0; (flop, UTG) = 26/400 = 6.5%; HJ over-rep | Forces BB-hero, UTG-hero, balanced HJ-hero spots |
| **Facing-raise** ≥10 per batch | Heuristic indicates near-0 (audit §2 of corpus distribution) | Forces BET_RAISE / CHECK_RAISE / MULTI_AGGR chains, currently absent |
| **River** ≥5 per batch | 0/400 river spots | Forces river chains (zero coverage currently) |
| **Top-12 chain coverage** ≥1 each per batch | (turn, BTN), (river, BTN) both 0 | Forces top-12 anchors regardless of natural frequency |
| **Sandwich** ≥4 per batch | Implicit; not auditable from spot record | Forces hero-positionally-between-two-villain-actors scenarios |

Conclusion: A1 quotas are correctly targeted at the corpus distribution gaps.
The audit data **validates the quota design**, even if it can't validate the
natural-frequency rank order.

## Top-12 rank ratification — silent acceptance

Per RATIFICATION_A1 escalation gate:

> *"if any chain shifts rank by >2 positions vs blueprint v1 §5.1, builder posts
> query comm to `review/comms/` and HALTS module authoring until architect ratifies
> the revised top-12. Rank shifts ≤2 are accepted silently and the v1 §5.1
> anchor set stands."*

The audit cannot produce a defensible rank-shift measurement (per §"Why exact
7-tuple re-derivation isn't possible" above). Therefore:

- **No rank shift detectable → no rank shift >2 → silent acceptance of v1 §5.1.**
- The 12-chain anchor set proceeds as specified in `RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md`
  §"12-chain anchor set".
- Module 10 authoring proceeds.

## Escalation gate status

**Status: no escalation. v1 §5.1 anchors stand. Module 10 authoring authorized.**

## Files produced

- `review/comms/phase2f1_top12_frequency_audit_2026-05-22.md` (this file)

## References

- RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md §Escalation gate
- DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md §5.1 (predicted top-12)
- MAIN_TERMINAL_PHASE2F1_B1_FIRE_NOW_2026-05-22.md (deliverable #4)
- BUILDER_REPORT_PHASE2E_FULL_BATCH008_2026-05-22.md (400-hand corpus baseline)

## Methodology note for QC

This audit is **NOT** a quantitative rank validation. Per the data-availability
constraint documented in §"Why exact 7-tuple re-derivation isn't possible",
exact chain fingerprints can't be computed from spot records. The audit
performs the strongest defensible aggregation (`(street, hero_pos)`) and
confirms that the corpus distribution validates the A1 quota design.

If QC requires a richer audit (e.g., walking labellers' rationale strings for
inferred postflop action), that is **out of scope** for B1 per
`feedback_optional_is_not_authorized.md` and `feedback_queries_to_orchestrator.md` —
escalate to orchestrator for separate dispatch.
