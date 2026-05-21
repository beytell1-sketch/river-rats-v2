# Orchestrator Ratification — A0.2 SHOULD_FIX-2: §6 vs §3.6 spec tension

**DATE:** 2026-05-22
**AUTHOR:** Orchestrator
**SOURCE:** QC findings `river-rats-qc/findings/2026-05-21-pr462-a0-2-backfill.md` SHOULD_FIX-2
**RELATED PRs:** #460 (A0.1), #461 (blueprint v2), #462 (A0.2 backfill)

---

## The tension

Blueprint v2 contains a documentation conflict on what happens to malformed-rejected labels in consensus_v2:

- **§6 PR A0.2** (line 630): "For every RAISE label classified `status=malformed_rejected`, that spot appears in `owner_arb_queue_normalizer.jsonl` and is **EXCLUDED from `consensus_v2.jsonl`**."

- **§3.6 (consensus_v2 modal-sizing logic)**: implies malformed labels stay in `consensus_v2.jsonl` with `sizing_status: "malformed-via-arb"` annotation (richer — has the consensus action AND the flag).

QC routed this as SHOULD_FIX. Builder followed §3.6 (richer reading) when implementing A0.2. QC notes data is fully recoverable either way.

---

## Ratification

**§3.6 reading is authoritative.** Malformed RAISE labels appear in BOTH `consensus_v2.jsonl` (with `sizing_status="malformed-via-arb"`) AND `owner_arb_queue_normalizer.jsonl`.

## Rationale

1. **Per `feedback_quality_default_no_ask.md`** — pick the quality path. The §3.6 reading preserves more information: the consensus_action is still computed (action consensus is independent of sizing consensus; modal action survives), only the sizing is flagged as unresolved. Excluding the spot entirely loses the action information.

2. **Per `feedback_failure_direction_classification.md`** — training-data pipeline needs per-spot direction labels (under-aggress / over-aggress). If a spot is excluded entirely from consensus_v2, the training pipeline loses that spot's action signal. Including-with-annotation preserves it.

3. **§6 wording was a simplification** — the architect's intent (revealed by §3.6's richer mechanism) was always to surface malformed-rejected spots to owner-arb, not to discard them. §6 conflates "route to owner-arb" with "exclude from consensus_v2," when the correct interpretation is "route to owner-arb in addition to consensus_v2 annotation."

4. **Builder followed §3.6 in PR #462 implementation** — A0.2 backfill files already use this reading. Ratifying §3.6 makes shipped data correct without re-work.

## Consequences

- **No corpus rework needed.** Existing v2 files (batches 001-007) already conform to §3.6.
- **Blueprint patch deferred** as a documentation cleanup. The textual conflict in §6 stays unresolved in the blueprint file but is settled by this ratification.
- **A0.3 (batch-008)**: builder followed the same §3.6 reading; A0.3 audit confirms consistency.
- **Downstream consumers** (training-data export, future trainer feature ingestion, evaluation pipelines) MUST handle `sizing_status="malformed-via-arb"` rows: typically, exclude from sizing-only training but include in action-classification training.

## Out of scope

- No code change required (Builder already implemented §3.6 correctly)
- Blueprint v2 §6 documentation correction can land as a small follow-up PR if owner wants; orchestrator considers low-priority since the ratification serves as the authoritative interpretation.
