---
date: 2026-04-13
from: Architecture Expert
to: Owner + Builder team
re: Phase 3A enriched output — revised architecture assessment (post-clarifications)
status: EXPERT FINDING — for owner review before any plan
supersedes: EXPERT_ARCHITECTURE_ENRICHED_OUTPUT_2026-04-13.md
---

# Revised Architecture Assessment: Enriched Labelling Output

## What changed and what stayed the same

The previous assessment recommended fixed vocabularies. That changes.
The recommendation on `primary_intention` as redundant field stands.
The recommendation to defer `feature_attention` stands.

---

## 1. Emergent vocabulary — schema design

A growing vocabulary requires a separate vocabulary registry, not
inline enums. The JSONL labels file is append-only during labelling
and must not be re-parsed to evolve a schema. Keep vocabulary state
separate.

**Vocabulary registry file:** `training-data/tag_vocabulary.json`

```json
{
  "schema_version": 1,
  "batches_applied": ["batch_001"],
  "intentions": {
    "value_thin": {
      "definition": "Betting or raising expecting worse hands to call.",
      "introduced_batch": "seed",
      "status": "accepted"
    }
  },
  "street_plans": {
    "barrel_value": {
      "definition": "Continue betting on future streets for value on safe runouts.",
      "introduced_batch": "seed",
      "status": "accepted"
    }
  }
}
```

Status values: `seed`, `accepted`, `merged_into:<tag>`, `rejected`.
Vocabulary is versioned by batch, not by hand. Labels reference tag
strings — if a tag is later merged, a migration script renames it in
the JSONL. That migration is a one-time batch operation, not
continuous.

Seed list (5-6 tags per category) is hardcoded at project start and
marked `"introduced_batch": "seed"`. Everything else emerges.

---

## 2. Reason-first, tag-second — pipeline complexity

This is not complex but it must be enforced in the prompt structure,
not in code. The prompt must require the agent to output fields in
order:

1. `reasoning` — written freely, no tag list visible at this step
2. `intentions_raw` — agent's own words for why they chose the action
3. `intentions` — after writing `intentions_raw`, agent consults the
   vocabulary and selects matching tags OR proposes new ones
4. `street_plan_tags` — same pattern

There is no pipeline enforcement of ordering — LLMs don't reliably
respect field-generation order. Enforcement is structural: the prompt
must instruct the agent to produce `intentions_raw` before producing
`intentions`, and the reviewer spot-checks that `intentions_raw` is
not a paraphrase of the tag definitions.

**The `intentions_raw` field is not optional.** It is the audit trail
proving reason-first happened. Include it in the JSONL.

---

## 3. Street plans as tags — resolved and creates one new constraint

The essay problem is resolved. Tags are correct.

New constraint: street plan tags must be composable, not mutually
exclusive. A hand can have both `barrel_value` and `pot_control_check_call`
if the plan is "barrel value on blank turns, pot control on completing
draws." The schema must be `street_plan_tags: list[str]` not a scalar.
Same 1-3 item limit as intentions.

Same reason-first protocol applies: agent writes `street_plan_raw`
(one sentence, own words) before consulting the tag list.

---

## 4. Propose-new-tag schema

When no existing tag fits, the agent outputs a `proposed_tags` block
alongside the label. This is a separate field, not a replacement for
the tag selection.

```json
"proposed_tags": [
  {
    "category": "intentions",
    "proposed_name": "block_bet_ip",
    "definition": "Small bet in position to control pot size and deny free equity to draws.",
    "hand_id": "d0244_CO_river"
  }
]
```

`proposed_tags` is an empty list when no new tags are needed. The
batch reviewer reads all non-empty `proposed_tags` entries at the
end of a batch and decides: accept (add to vocabulary), merge (map
to existing tag and note the alias), or reject (drop, leave label
with `intentions_raw` as the record).

If a proposed tag is rejected, the label is not invalidated — the
`intentions_raw` field carries the meaning. If accepted, a migration
renames the proposed string to the canonical tag in the JSONL.

---

## 5. Vocabulary versioning across batches

Each batch produces: (a) label JSONL, (b) proposed tags list. The
batch review step produces: (c) updated `tag_vocabulary.json` with
`schema_version` incremented if any tags were accepted or merged.

Labels store the schema_version at write time:

```json
"vocab_version": 1
```

This makes migration auditable: find all labels where
`vocab_version < current` and check whether any used a tag that was
later merged or rejected. No automatic re-labelling — flag for human
review only.

Batches do not wait for vocabulary to stabilise before labelling
continues. Labelling proceeds with the current vocabulary. Vocabulary
changes are reconciled post-batch, not mid-batch.

---

## Revised combined schema (v2.2 target)

```json
{
  "situation_id": "d0244_CO_river",
  "vocab_version": 1,
  "hand_bucket": "strong_made",
  "action": "BET",
  "reasoning": "...",
  "intentions_raw": "I'm betting because worse pairs will call and I'm not afraid of draws completing.",
  "intentions": ["value_thin"],
  "street_plan_raw": "Will barrel blank turns, check back completing draws.",
  "street_plan_tags": ["barrel_value", "check_evaluate_draws"],
  "proposed_tags": [],
  "confidence": "HIGH",
  "key_factors": ["..."],
  "factor_conflicts": "None",
  "alternatives_considered": ["..."],
  "difficulty": 2
}
```

Dropped from prior schema: `street_plan` as free text.
Added: `intentions_raw`, `street_plan_raw`, `street_plan_tags`,
`proposed_tags`, `vocab_version`.
Still dropped: `primary_intention` as separate field — use `intentions[0]`.

---

## ML learnability check

`intentions` and `street_plan_tags` are multi-label classification
targets. They are machine-learnable as-is: each tag becomes a binary
column, one model per tag or one multi-label model. The emergent
vocabulary means the label space grows, but only by accepting new
tags at batch boundaries — no mid-training label space changes.
Training on v2.3 begins after the vocabulary has stabilised (defined
as: no new tags accepted in the most recent full batch).

---

## One open question for owner

Should `intentions_raw` and `street_plan_raw` be stripped before
export to the training CSV, or retained for qualitative review?
Recommendation: retain in JSONL, strip from training CSV. The raw
fields are audit evidence, not model inputs.
