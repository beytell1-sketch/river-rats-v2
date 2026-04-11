---
date: 2026-04-10
from: Reviewer terminal
to: Logic team (builder)
re: Review of action-history feature-expansion side-quest investigation
    (villain_aggression backtrack + hero action history)
verdict: INVESTIGATION SOLID — NOT READY TO BUILD
context: side quest raised while KB_V1.3_EDIT_PLAN.md is in review
---

## Scope

Owner asked the reviewer to audit the builder's side-quest
investigation into backtracking villain's action sequence and
tracking hero's own action history as model features. Investigation
was presented inline with factual claims about:

- `river-rats-core/game_state_bridge.py:99-121` — villain aggression
  tracking code path
- `river-rats-core/feature_extractor.py:1647-1653` — hero preflop
  aggressor feature
- grep of every `*.py` for `hero_aggression` / `hero_bet_count` etc.
  (builder reports zero matches)

Reviewed against:

- `docs/PROCESS_GUIDE.md`
- `CLAUDE.md` (river-rats-v2) Section 1 (Plan Before Build), Section
  2 (Validate Assumptions Before Building), Section 4 (Blueprint
  Before Build), Section 5 (Stop Conditions)
- Owner direction: "cheap options while review is busy"
- Current training state (348 + 260 = 608 situations, 45/48-feature
  pipeline, v9-3way-v2.2 at 82.5%)
- Scheduling context: `KB_V1.3_EDIT_PLAN.md` currently approved for
  architect application

## Verdict

**INVESTIGATION SOLID — NOT READY TO BUILD.** The factual
investigation (what's tracked, what isn't, where the gaps are) is
useful scoping work and the builder correctly stopped at proposal
rather than building. But three things need to happen before any
feature code is written, and one framing assumption needs
correcting.

## Findings

### [BLOCKER] B1 — "Cheap while review is busy" is a category error

The code change is trivial — ~12 symmetric lines in
`game_state_bridge.py`, mirroring the existing villain
aggregation. But `hero_aggression_count` and friends are
**feature additions**, and feature additions in this pipeline
unavoidably trigger:

1. Retrain (new feature columns → can't load into the existing
   v9-3way-v2.2 model)
2. New quality gate against the 40-hand reference set
3. Leakage check (see S2)
4. Blueprint + programmer + tester + independent reviewer cycle
   per Process Guide task decomposition

Worse, running this as a **parallel** track to the v1.3 KB review
has a specific scheduling failure mode:

- If you retrain now (before v1.3 ships): the new model inherits
  v1.2-labelled training data, which carries the over-fold bias
  that v1.3 is explicitly correcting. The feature expansion's
  benefit gets measured against biased labels; the v1.3 vocabulary
  purge never reaches the new model.
- If you wait for v1.3 labels before retraining: this isn't a
  parallel track — it's a **sequential next step** after v1.3
  ships. The "parallel while review is busy" framing disappears.

Either way, the owner directive "cheap options now while review is
busy" does not actually apply to feature additions in this project.

**Required:** Do not treat this as a parallel side-quest. Park the
investigation as a scoping document in `review/`, and pick it up
as the natural *next* step after v1.3 labels land and you are
planning the next training round.

### [SHOULD_FIX] S1 — Verify the causal hypothesis BEFORE committing to the feature set

Builder speculated that MW-17 (under-calling), MW-25/40 (residual
passive thin-value), and MW-45 (under-raising) might all be
explained by "the model doesn't know hero's own prior line." The
builder correctly flagged this as speculative.

That speculation has to be falsified or confirmed against the
actual feature rows BEFORE any feature is added. If the MW-17/25/
40/45 failures are driven by something else (pot-odds reading
error, `tp_plus_pct` bucket mis-scaling, blocker logic from
finding 1), adding `hero_aggression_count` changes nothing and
you've retrained for no gain.

**Required before build:** spawn an ml-architect or gto-expert
agent to pull the feature rows for MW-17, MW-25, MW-40, MW-45,
reason about whether a hypothetical `hero_aggression_count` signal
would flip the model's prediction in each case, and write a
one-page finding to `review/comms/`. If fewer than 2 of the 4
cases would plausibly flip, the feature expansion is
unjustified on these specific failures and the owner needs a
different rationale before spending a retrain on it.

This is the Process Guide's "validate assumptions before building"
rule applied directly.

### [SHOULD_FIX] S2 — Leakage risk not assessed

Adding features derived from hero's prior actions is a natural
leakage surface:

- If the labelling agent saw hero's action history when producing
  the label, and the model now learns from features that encode
  that same history, the model can pick up label-leakage via the
  action sequence rather than genuine poker signal.
- Concretely: if the labelling KB says "hero bet flop then turn,
  so river should be CALL/FOLD based on story consistency," and
  the labeller wrote that reasoning into the label, a
  `hero_aggression_count` feature would let the model learn the
  labeller's reasoning shortcut rather than the underlying poker.

This must be assessed by an ml-architect before any feature is
added. Possible mitigations (leave-one-out training, SHAP
importance check on held-out situations, blind-calibration
before/after comparison) exist, but the owner should see the
options before committing.

**Required:** ml-architect leakage assessment, written to
`review/comms/`, before build.

### [SHOULD_FIX] S3 — Retrofit feasibility on existing 608 situations not investigated

The proposal implicitly assumes the existing training data can be
reprocessed to compute new features without full regeneration.
This depends on whether `game.street_actions` (or an equivalent
serialised form) is preserved in the stored training situations
in a form that can be replayed into the feature extractor.

If it IS preserved: the retrofit is ~15 minutes of recompute.
If it is NOT preserved: "trivial code change" becomes "regenerate
608 situations", which pulls in self-play runtime, labelling
agent time, and another quality gate — not trivial.

Builder did not check this. Easy grep — architect agent can
verify in 5 minutes.

**Required before build:** architect agent confirms
`game.street_actions` preservation in the training-data JSONL
schema, writes finding to `review/comms/`.

### [SHOULD_FIX] S4 — `any_villain_aggression_count` attribution loss not quantified

Builder correctly identified that a max/sum aggregation over all
villains loses attribution between "opponent A is a triple-barrel
maniac" and "opponents A and B alternated aggression." This is
**exactly** the 3-way signal the feature is supposed to carry.

The builder offers the aggregate as a cheaper alternative to
per-villain tracking without addressing whether the aggregate
preserves the signal that motivated the feature in the first
place. It may turn out that:

- The aggregate is useful (it still distinguishes "some opponent
  was aggressive" from "nobody was aggressive" — both are signals
  the model currently lacks)
- OR the aggregate is redundant with `num_callers_to_bet` and
  `facing_raise` (features that already exist) and adds nothing
- OR the aggregate is useful but only as a companion to
  attribution, not a replacement

This is an ml-architect call. Builder should not self-propose the
aggregate without that opinion.

**Required before build:** ml-architect opinion on whether the
aggregate form carries independent signal vs existing features.

### [SHOULD_FIX] S5 — Factual claims about code are not reviewer-verified

Builder cites specific line ranges and a negative-grep result:

- `game_state_bridge.py:99-121` (villain aggregation code)
- `feature_extractor.py:1647-1653` (is_preflop_aggressor)
- grep of every `*.py` returns zero matches for
  `hero_aggression`, `hero_bet_count`, `_hero_aggression`,
  `hero_action_count`

Reviewer has not run these independently. For any formal
feature-expansion proposal, the builder should post a standalone
delivery to `review/comms/` that includes:

1. The literal source blocks (with ±5 lines of context) for both
   cited line ranges.
2. The grep command and its complete output.
3. A schema excerpt from the training-data JSONL showing what
   action-history fields are actually preserved (ties to S3).

Then I can spot-check without re-grepping.

### [NOTE] N1 — Rule #7 compliance is correct

Process Guide rule #7 says experts recommend, owner decides scope.
The builder made a clear recommendation (the cheap+high-signal
pair: `hero_aggression_count` + `hero_checked_count` + a
conditionally approved `any_villain_aggression_count`), parked the
expensive variants (per-villain temporal, action-level, bet
sizing) explicitly, and did not dump a menu on the owner. Good.

### [NOTE] N2 — Do not save the proposed memory yet

Builder proposed writing `project_action_history_gap.md` to
memory. Do not do this until S1 confirms the gap is real (i.e.
the causal hypothesis survives contact with the MW-17/25/40/45
feature rows). Saving a memory for an unverified hypothesis would
encode a false belief into future sessions — exactly the "memory
must be verified before acting" rule in the memory system brief.

Save the memory AFTER the feature set is confirmed real, not now.

### [NOTE] N3 — The three identified limitations are real pre-existing gaps, not new regressions

Builder's three villain-side limitations are correctly identified:

1. Street-count, not action-count (reraise wars collapsed)
2. Primary-villain-only (3-way second opponent invisible)
3. `villain_checked_back` is 1 bit (temporal ordering lost)

All three are pre-existing. None are new regressions from any
recent change. Fixing any of them is a legitimate improvement,
but none are blockers for current training quality and none
should be used as urgency justification.

### [NOTE] N4 — Hero-side gap confirmation

Builder's grep claim — that nothing in the repo tracks hero's
postflop action history beyond `is_preflop_aggressor` — is
plausible and matches my independent prior reading of the
feature list. Not independently re-verified this session (see
S5), but flagged as likely correct. This is a genuine gap in the
feature vector regardless of whether the MW-17/25/40/45 causal
hypothesis pans out.

## Protocol compliance

- **Section 0 (phase transition):** N/A — scoping investigation,
  not a phase boundary.
- **Section 1 (resource allocation):** Builder did scoping work in
  main context. Acceptable for scoping. If approved to proceed,
  proper decomposition is ml-architect → architect → programmer
  → tester → reviewer.
- **Section 2 (quality gates):** No build happened, no gates to
  check. Required gates listed in B1 (retrain + reference set
  check + leakage check + blueprint + review).
- **Section 3 (research):** Factual citations present but not
  independently verified. See S5.
- **Section 4 (presentation):** Investigation presented before
  building. Correct.
- **Section 5 (poker protocols):** N/A for scoping stage.
- **Section 6 (training protocol):** N/A for scoping stage. Will
  apply if / when build is authorised.
- **Rule #7 (experts recommend, owner decides scope):** Satisfied.
  See N1.

## Recommendations to builder

1. **Park the build.** Keep the scoping investigation as a
   document in `review/`, do not write any feature code in
   `game_state_bridge.py` or `feature_extractor.py` this session.
   (B1)
2. **Do not run this in parallel with the v1.3 KB review.**
   Feature expansion should happen AFTER v1.3 labels ship, as
   the natural next step. (B1)
3. **Before any build is authorised, produce four investigations**
   and post each to `review/comms/`:
   - S1: MW-17/25/40/45 feature-row causal hypothesis check
     (ml-architect or gto-expert)
   - S2: leakage assessment (ml-architect)
   - S3: training-data retrofit feasibility (architect)
   - S4: aggregate-vs-per-villain attribution opinion (ml-architect)
4. **Formalise the factual claims** as a standalone delivery with
   literal source blocks and grep output attached. (S5)
5. **Do not write the memory file yet.** Wait for S1 confirmation.
   (N2)
6. **Update the framing.** The correct label for this work is
   "feature expansion proposal, sequential after v1.3", not "cheap
   side quest parallel to review". (B1)

## Recommendations to owner

1. **Answer to the "is this being done / can it be done" question:**
   villain side is partially done (street-level, primary-villain-
   only, no temporal ordering); hero side is effectively not done
   at all (just `is_preflop_aggressor`, one preflop bit). Both
   gaps can be filled mechanically — see builder's investigation —
   but the retrain cost is not optional and the work is not
   actually cheap.
2. **Scheduling:** treat this as a proper phase-boundary item
   after v1.3 ships, not as a side-quest. That respects the "slow
   and deliberate, quality over speed" directive and avoids the
   parallel-track scheduling failure in B1.
3. **If the MW-17/25/40/45 failures are the actual pain point,**
   the right first move is an ml-architect / gto-expert
   investigation of those 4 hands' feature rows to identify the
   real cause — BEFORE deciding that action-history features are
   the fix. There may be a cheaper non-feature-expansion remedy
   hiding in those 4 rows (a KB rule update, a label review, a
   hyperparameter tweak) that should be ruled out first.
