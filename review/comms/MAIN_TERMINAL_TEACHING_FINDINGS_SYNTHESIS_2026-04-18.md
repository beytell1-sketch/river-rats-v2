---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Owner (decisions) · Teaching terminal · Builder · Game builder
re: Teaching's two findings — false-draw + WHY→WHAT — synthesis and recommendations
status: REQUESTS OWNER AUTHORIZATION on Path B scope
---

# Synthesis — Teaching's Two Findings

Teaching terminal surfaced two serious findings during playtest
review of the `continue_draw CALL` case. Three expert agents
reviewed in parallel (GTO correctness, feature extractor audit,
V3 philosophy compliance). Both findings confirmed.

Owner's original message:
> "please remove why we take a decision..unless it can be done
>  correctly..i thought we fully decided to not try and say why
>  we take a decision?"

This is not a question. It's an owner directive invoking the
V3 philosophy as written. The expert review confirms the "done
correctly" condition cannot be met in the surgical sense.

## Finding 1 — False-draw outs on drawing-dead air hands

**What:** Feature extractor counts "gutshot 4 outs" for hero
even when hero is drawing dead or drawing to a chop. Smoking
gun: `d5383_BB_turn` has `raw_equity = 0.097`, `improvement_
probability = 0.087`. Hero's entire equity IS the outs — and
with `has_showdown_value=0` those outs don't produce a winning
hand. Drawing dead.

**Scope:** 4 cases in the 3-way playtest set. Pattern: `air`
bucket + claimed gutshot + `has_sdv=0` + equity ≈ improvement_prob.

**Root cause layer:** v2 core `hand_evaluator.py`. "Out" is
defined structurally (hero contributes to a 4-card straight
window) without checking "does this card produce a hand that
beats villain's continuing range at showdown."

**Blast radius:** Oracle may be learning from wrong draw features
too — not just teaching. Needs logic-team audit.

## Finding 2 — V3 "no WHY" directive violated across all 6 intention templates

**What:** CLAUDE.md V3 philosophy states
> "Never claim to explain WHY GTO takes an action."

The "no Why" directive was applied to the **header only**
("Oracle's Read — BET" instead of "Why BET"). Sentences below
every header are textbook causal reasoning:

| Intention | Offending phrase |
|---|---|
| value_extract | "extracts value from X% who call with worse" |
| deny_equity | "charges those draws rather than letting them realize equity" |
| bluff_fold_better | "only profits when opponents fold" |
| continue_draw | "clears the 20% price by 17 points, making the check correct" |
| pot_control | "keeps the pot at a size hero can reach showdown" |
| range_fold_priced_out | "N-point deficit that villain's range fully explains" |

**Teaching reviewer's structural finding:** Path A (surgical
rewrite) collapses. Any sentence that combines an action verb
with a range/equity number is read causally. Fixing Path A
honestly = Path B with extra ceremony.

**Recommended:** Path B — delete `content/intention_templates.py`
(989 lines), remove `action_signal_lines` from enriched output.
Keep situation_describer (WHAT — hand, range, equity, pot odds,
SPR, draw identity, blocker, board texture). Add tightness
signal (TOSS_UP / CLOSE / SILENCE from oracle's top-two
probability gap). Learner constructs the WHY; system shows
WHAT and HOW-CLOSE.

This IS V3 architecture per CLAUDE.md.

## Recommendations

### Decision 1 — False-draw guard — **RECOMMEND APPROVE**

**Do both:**

1. **Teaching guard (immediate):** suppress gutshot/OESD claims
   when `(hand_bucket=='air' AND is_made_hand=0 AND has_sdv=0
   AND raw_equity ≈ improvement_probability)`. This is a
   **coherence guard that suppresses incoherent output**. Does
   not fabricate context. Allowed under the no-override rule.

2. **v2 core ticket (upstream):** redefine "out" in
   `hand_evaluator.py` as "hero strictly beats villain's
   continuing range at showdown after card arrives." Major
   logic change; owned by builder; coordinates with next
   feature-vector pass.

**Why both:** Guard prevents broken output shipping while
upstream fix takes time. Upstream is the right architectural
answer and also fixes any oracle feature-learning contamination.

### Decision 2 — WHY → WHAT Path B — **RECOMMEND APPROVE (scope auth needed)**

**Why I'm recommending this over waiting:**

- Owner directive is already given ("remove why we take a
  decision")
- V3 philosophy is the project spec (CLAUDE.md)
- Expert teaching reviewer verified Path A cannot satisfy the
  spec honestly
- `intention_templates.py` was architectural drift from V3 —
  correcting drift is realignment, not rework
- Owner style: catch now over ship broken

**Why I'm flagging scope to owner:**

- Deletes 989 lines across 6 intention templates
- Undoes recent Phase 2 work
- Obsoletes the `value_extract` air guard I directed in
  update-g Layer 3 (teaching terminal should PAUSE that work
  pending this decision)
- Game builder's "Why" panel content changes — needs
  coordination
- Teaching timeline shifts; L3 playtest delayed

**Scope envelope if approved:**

1. Teaching deletes `intention_templates.py` + `action_signal_lines`
2. Teaching adds tightness signal (TOSS_UP / CLOSE / SILENCE
   from oracle probability gap) per CLAUDE.md decision_reporter
3. Keeps all situation_describer WHAT content (hand description,
   range composition, equity, pot odds, SPR, draw identity,
   blocker, board texture)
4. Updates CONTENT API (`interface/CONTENT_API.md`) —
   EnrichedTeachingOutput schema change
5. Game builder updates adapter to new schema
6. Re-run L3 hardening tier on new output format

## Cross-stream implications

### v2.3.1 model ship — **proceeds independently**

v2.3.1 is about **action correctness**. Model gates and litmuses
are independent of teaching philosophy. Ship sequence unchanged:
- Broader-inference sweep passes → model ship
- Copy to `river-rats-core/models/`
- Game adapter swap v2.2 → v2.3.1

### Teaching Layer 3 (value_extract air guard) — **PAUSE**

If Path B approved, this guard becomes obsolete (we're deleting
the sentence that needs guarding). Teaching terminal: do not
continue this work until owner decides.

### Game playtest timeline — **delayed by Path B**

L3 playtest needs teaching output. Path B changes the output
format. Teaching gives estimate on Path B implementation; game
builder waits on that + v2.3.1 model ship.

## Requests

**From owner (decisions):**

1. **Decision 1 (false-draw):** approve guard + v2 ticket? Or
   wait for upstream only?
2. **Decision 2 (Path B):** authorize scope (delete 989 lines,
   add tightness signal, update CONTENT API)? Or want
   modifications to Path B (e.g., keep a bounded observation-
   only prose line with no intentional reasoning)?

**From teaching terminal (on owner approval):**

- Path B implementation plan with timeline estimate before
  deletion begins
- Draft of tightness signal spec for review
- CONTENT API schema diff

**From builder (on Decision 1 approval):**

- File v2 core ticket for `hand_evaluator.py` draw_outs
  semantics
- Estimate scope — is this a v2.3.2 or a bigger lift?
- Flag any oracle-feature implications

## Standing down on competing work

Until owner decides:
- Teaching terminal: pause value_extract air guard
- Builder: pause broader-inference sweep? No — Decision 1/2 are
  teaching-layer, model is independent. Sweep continues.
- Game builder: hold on adapter change until both decisions
  land

Awaiting owner.
