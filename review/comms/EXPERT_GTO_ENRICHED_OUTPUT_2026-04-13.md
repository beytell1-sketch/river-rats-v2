---
date: 2026-04-13
from: GTO Expert
to: Owner + Builder team
re: Phase 3A enriched output — GTO Expert assessment (Sections 1-3)
status: EXPERT FINDING — input for owner decision, not a directive
---

# GTO Expert Assessment: Enriched Labelling Output

## Section 1 — Street Plans

**Can agents reliably produce 1-2 sentences?**

No. Not without hard structural enforcement. The labelling prompt
already requires 2-4 sentence reasoning blocks and factor-conflict
resolution. When an agent is doing that work AND forming a street
plan, the plan will expand to fill available reasoning space — it
will become a third paragraph of the existing reasoning field, not a
disciplined 1-2 sentence forward-looking statement. The constraint
has to be mechanical (max 20 words, specific sentence templates) or
it will not hold at scale across 10 hands.

**Are street plans GTO reasoning or coaching artifact?**

Street plans are a coaching artifact. They are not how GTO reasoning
operates — a solver does not produce narrative plans, it produces
action frequencies at each node. The plans are a translation of
forward-looking SPR/equity-realization logic into human language.
That translation is useful for teaching but it is not the label
quality problem. The current prompt already captures forward-looking
logic through DO NOT Rule #7 (full street tree) and the SPR
compression data. The gap is not that the agent fails to think
ahead — it is that the thinking-ahead logic is buried in reasoning
prose rather than surfaced as a structured field.

**Recommendation:** Defer to v2.3. The signal is real but the
reliability risk is high for Phase 3A. If adopted later, constrain
to a fixed template: "{flop_action} for {primary_intention}. If
called, {turn_trigger} on {runout_type}." Free text will drift.

---

## Section 2 — Multi-Label Intentions

**Is the 15-intention vocabulary complete?**

Mostly yes. Two gaps:

1. `slow_play_build_pot` is missing as a CHECK intention. Checking a
   strong made hand to let a villain catch up (not trapping a bet,
   but building equity in the pot) is distinct from `trap_induce_villain_bet`.
   Trap means you expect a bet and plan to raise. Slow-play means you
   are happy with a check-check and a better-connected villain on
   turn. The current `trap` covers both and conflates them.

2. `fold_out_better_with_equity` is missing for RAISE situations. The
   semi-bluff vocabulary covers fold equity plus draw equity, but a
   raise with a strong draw against a medium-strength range is
   sometimes primarily about folding out hands that are currently
   ahead with board equity rather than pure bluff fold equity. This
   sits between `semi_bluff_fold_equity_plus_draw` and
   `bluff_fold_out_better` and is currently unrepresented.

**Can agents consistently identify 2-3 intentions?**

For clear spots (difficulty 1): yes, reliably. The intention is
obvious and the second intention, if any, is also obvious.

For difficulty 2-3 spots: agents will pad. The pressure to provide
2-3 intentions will cause agents to add a second intention that is
technically defensible but not actually driving the decision. A
protection bet on a wet board against a weak villain range is
primarily `protection_fold_draws`. Adding `value_get_worse_to_call`
because "worse hands exist" is noise, not signal. The
`primary_intention` field partially corrects this by forcing the
agent to commit — but only if the prompt is explicit that 1 intention
is acceptable for clear spots. Currently the proposal implies 2-3
minimum, which will cause padding.

**Are any intentions redundant?**

`thin_value_target_marginal_calls` and `value_get_worse_to_call` are
too similar. The distinction (clear worse-hand-calls vs borderline
calls) is real in poker but agents will not apply it consistently
without an operationalized threshold. Merge them or add a concrete
distinguishing rule: `thin_value` = villain air pct below 15%,
`value` = villain air pct 15%+.

`equity_denial_prevent_free_cards` and `protection_fold_draws` also
overlap significantly. Equity denial is mechanically the same action
as protection — you bet to prevent free cards because villain has
draws. These should be one intention with a context qualifier, not two
separate vocabulary items.

**Recommendation:** Adopt multi-label intentions in Phase 3A. It is
the strongest of the three additions. But enforce: (a) 1-3 items, not
2-3 minimum; (b) merge the two redundant pairs; (c) `primary_intention`
is required and must appear as first item in the list.

---

## Section 3 — Feature Attention

**Can agents tag 2-4 PRIMARY features using exact feature names?**

No, not without the feature list in the prompt. The 48-feature vector
includes names like `villain_draw_pct`, `board_favour`, `draw_outs`,
`villain_range_capped` — agents will paraphrase these in natural
language ("villain draw percentage was high") unless the exact names
are visible. Paraphrase breaks the downstream SHAP comparison because
the mapping from natural-language description to feature key becomes
ambiguous.

**Do agents need the feature list in their prompt?**

Yes. But not all 48 features. The labelling agent currently uses a
subset of features in its reasoning (danger_score, villain_draw_pct,
villain_top_pair_plus_pct, equity_vs_range, is_ip, facing_bet,
pot_odds, villain_air_pct, villain_range_capped, draw_outs). A
curated list of the 20 most decision-relevant features is sufficient
and keeps context cost manageable. Agents will not invent features
outside what they can see in the prompt context.

**Will agents tag the same features consistently?**

Not reliably for the SUPPORTING tier. PRIMARY features are stable —
the agent used them to reach the label, they are visible in the
reasoning. SUPPORTING features are retroactively justified and will
vary across agents even for similar hands. This is exactly the
problem that makes the NOT_RELEVANT tier unreliable (correctly
excluded from the proposal) — but it applies to SUPPORTING as well.

**Recommendation:** Adopt feature attention but reduce to PRIMARY
only. Drop the SUPPORTING level entirely. PRIMARY = "without this
feature, the decision label might change" is operationally clear and
agents can apply it consistently. SUPPORTING = "reinforces the
decision" is too subjective and will produce noisy data. A list of
2-4 PRIMARY feature names per hand is clean, verifiable against the
reasoning text, and directly usable for the SHAP comparison (Use 2).

---

## Overall Assessment

**Adopt in Phase 3A:**
- Multi-label intentions (with the vocabulary fixes above)
- Feature attention as PRIMARY-only (with a curated 20-feature list
  in the prompt)

**Defer to v2.3:**
- Street plans (real signal, reliability risk too high without
  template enforcement, and the forward-looking gap is the weaker of
  the three problems)

**Agent overload at 10 hands:**

With both adopted additions, the output per hand increases but the
reasoning load does not increase proportionally — the agent already
does the thinking. Tagging intentions and PRIMARY features is
extraction, not additional reasoning. 10 hands per agent is
manageable if the prompt is structured clearly. The risk is not
overload per hand but drift across hands 7-10 where an agent begins
applying looser intention labels to satisfy the vocabulary requirement.
Cap at 8 hands per agent if quality degradation is observed in testing.

**The one field that adds noise without improving poker judgment:**

Street plans as free text. Everything else adds structure to
reasoning the agent already does. Street plans ask the agent to
produce new content that is prone to drift and difficult to validate.
