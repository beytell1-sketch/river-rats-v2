---
date: 2026-04-13
from: Architecture Expert
to: Owner + Builder team
re: Phase 3A enriched output — architecture assessment
status: EXPERT FINDING — for owner review before any plan
---

# Architecture Assessment: Enriched Labelling Output

## Critical observation first

`label_3way_situations.py` is a rule-based if/elif heuristic, not an
LLM agent. The briefing assumes labelling agents produce free-text
reasoning that can be enriched with new fields. The current code
cannot produce `street_plan`, `intentions`, or `feature_attention` —
those fields require genuine per-hand reasoning, not threshold rules.

Phase 3A presumably replaces this with LLM-based labelling. This
assessment assumes that rewrite is happening. If it isn't, none of
the three additions are possible regardless of schema design.

---

## Section 1: street_plan

**Schema impact: minimal.** One optional string field. Omit on river,
require on flop and turn. The JSONL schema change is one new key.

**Pipeline impact: none on training.** The field is logged but the
v2.2 model trains only on `action`. The comparison report can surface
street_plan in disagreement cases without any structural change.

**Agent context:** No additional context burden. The agent already
reasons about future streets (DO NOT Rule 7). Formalising that
reasoning into a required output field costs nothing — it redirects
existing thinking rather than adding new thinking.

**Recommendation: include in v2.2.** Low cost, immediate teaching
value, and it enforces DO NOT Rule 7 compliance in a verifiable way.

---

## Section 2: multi-label intentions

**Schema: the `intentions` list + `primary_intention` scalar is
redundant.** `primary_intention` should be `intentions[0]` by
convention, not a separate field. A separate scalar creates a
consistency constraint that will occasionally be violated (agent
lists `protection` first but writes `value` as primary). Remove
`primary_intention` entirely. Callers that need it read `intentions[0]`.

**Pipeline impact: moderate.** The comparison report currently compares
`expert_action` strings. With intentions, it can also compare
`intentions[0]` between old and new labels to distinguish "same action,
different reason" from "different action entirely." That's a new report
column, not a structural change. Training is unaffected — the model
still sees only the action label.

**JSONL schema addition:** `intentions: list[str]` with 1-3 items from
the fixed vocabulary. The vocabulary of 15 is well-scoped and maps
cleanly onto the 5-factor framework the agents already use.

**Agent context:** No feature list required. The intention vocabulary
is short enough to embed directly in the prompt (< 30 lines). This
does not meaningfully increase context size.

**Recommendation: include in v2.2, with one change** — drop
`primary_intention` as a separate field.

---

## Section 3: feature_attention

**This is the risky one.** The schema itself is simple (a dict of
feature_name -> PRIMARY|SUPPORTING). The problem is agent reliability.

To tag features by exact name from the 48-feature vector, agents need
the full feature list in their prompt. The current prompt already
contains: KB + condensed reference data + full KB appended at runtime
+ 5-factor framework + DO NOT rules. Adding 48 feature names is
non-trivial context growth.

More importantly: agents will be tempted to tag features they are
*told to look at* (the features named in the 5-factor framework) rather
than the features that actually drove the specific decision. The
attention map will systematically over-represent `danger_score`,
`equity_vs_range`, and `villain_top_pair_plus_pct` because those are
the features the prompt foregrounds — not because they were primary on
that particular hand.

The SHAP-vs-attention comparison (Use 2) is only useful if the attention
is genuinely per-hand, not a reflection of the prompt's own emphasis.

**Simpler alternative that captures the same signal:** instead of a
full attention dict over 48 features, ask agents to name the 2-3
features that would change their decision if the values were different.
This is a counterfactual framing that forces genuine per-hand reasoning
rather than checklist tagging.

**Pipeline impact if adopted:** the comparison report needs a new
section; train.py is unaffected; JSONL schema adds one optional dict.
The SHAP comparison is post-training analysis code, not pipeline code.

**Recommendation: defer to v2.3.** The data collection cost (prompt
bloat, reliability risk) is real. The value (Use 2 and Use 3) depends
on LLM attention being genuinely per-hand, which is unverified. Collect
street_plan and intentions first — they are cheap and verified useful.
After v2.2 trains, run a 20-hand pilot of feature_attention with manual
audit before committing to it across 385 hands.

---

## Combined schema recommendation for v2.2

```json
{
  "situation_id": "d0244_CO_river",
  "hand_bucket": "strong_made",
  "action": "BET",
  "intentions": ["protection_fold_draws", "value_get_worse_to_call"],
  "street_plan": "Bet flop for protection. Evaluate turn — barrel safe runouts, check-call completing draws.",
  "confidence": "HIGH",
  "reasoning": "...",
  "key_factors": ["..."],
  "factor_conflicts": "None",
  "alternatives_considered": ["..."],
  "difficulty": 2
}
```

Changes from current schema: `intentions` added (list, 1-3 items),
`street_plan` added (omit on river), `hand_bucket` added (already
planned for Phase 3A bucket-first reasoning). `primary_intention`
not added — use `intentions[0]` by convention.

`feature_attention` deferred. Pilot it on 20 hands after v2.2 trains.

---

## Pipeline change summary

| Component | Change needed |
|---|---|
| `label_3way_situations.py` | Full rewrite — LLM agent replaces heuristic |
| JSONL schema | Add `intentions`, `street_plan`, `hand_bucket` |
| Comparison report | New column: intention agreement vs prior labels |
| `train_model.py` | No change — trains on `action` only |
| Teaching oracle | Can use `intentions` + `street_plan` immediately for richer explanations |
