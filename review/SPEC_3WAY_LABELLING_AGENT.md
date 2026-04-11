# SPEC: 3-Way Labelling Agent

**Date:** 6 April 2026
**Status:** Draft — awaiting review
**Depends on:** 45-feature pipeline (done), situation generation (approach decided, not yet run)
**Blocks:** v9-3way training

---

## Objective

Build a specialist LLM agent that labels ~200 three-way postflop
decisions with correct GTO actions. The agent has a curated 3-way
knowledge base, a structured reasoning protocol, and must pass a
calibration exam before labelling training data.

---

## Architecture

### One agent, self-scaling depth

One prompt file, one knowledge base. The agent assesses each hand's
difficulty (1-3) and spends proportional effort:

- **Difficulty 1 (clear):** 1 paragraph reasoning. Equity far from
  thresholds, obvious action.
- **Difficulty 2 (standard):** 2-3 paragraphs. Normal complexity,
  full reasoning protocol.
- **Difficulty 3 (boundary):** 4+ paragraphs. Explicitly considers
  2+ alternative actions. Flags for human review.

Why not three sub-specialists: routing requires most of the analysis
work (circular), and for 200 hands the engineering overhead doesn't
pay for itself.

### No live search

The agent reads a pre-built knowledge document. No web search during
labelling. Consistency is non-negotiable — same input must produce
same reasoning across runs. The knowledge base is version-controlled
and traceable.

### One hand per call

Each situation is labelled in an independent agent call. No anchoring
bias from prior hands, no batch failures, trivial output parsing.

---

## Files to Create

| File | Purpose |
|------|---------|
| `prompts/gto_labeller_v1.md` | Agent prompt: role, knowledge base, reasoning protocol, output format, DO NOT rules |
| `knowledge/three_way_gto.md` | Pre-built 3-way GTO reference (~2-3K words). Researched, curated, versioned. |
| `calibration_exam.py` | Feed 24 reference hands to agent, score against known labels, report |
| `labelling_agent.py` | Feed situations JSONL to agent one-by-one, collect structured labels |

---

## Knowledge Base: `knowledge/three_way_gto.md`

### Content Structure

The knowledge base uses **factor-weighting with growing examples**,
not hard thresholds. Quantified facts (fold equity = 36%, equity
dilution curves) are reference data — inputs to reasoning, not
decision rules. The agent weighs multiple factors per decision,
guided by worked examples that show the reasoning process.

**Why not thresholds:** Hard thresholds create ceilings under
iteration. Fixing one gate failure by moving a threshold breaks
labels that were correct at the old threshold. This is the same
pattern that limited the multiway adjuster through 4 calibration
rounds and 5 self-play rounds. Factor-weighting is additive —
improvements come from new worked examples, not threshold changes.

**Versioning:** After each training gate, failures are analyzed
and added as new worked examples. Principles stay stable. Examples
accumulate. The knowledge base grows smarter without contradicting
itself.

**Section 1 — Reference Data (facts, not rules)**

Quantified 3-way facts the agent uses as inputs to reasoning:

- Bluff compression: HU bluff:value ~1:2. 3-way: ~1:4-5. Combined
  calling frequency ~75%.
- Fold equity: P(fold_A) × P(fold_B). Each folds 60% → 36% 3-way.
- Equity dilution per hand class:
  - TP weak kicker: 55% HU → 38-42% 3-way
  - Overpairs: 80% HU → 60-65% 3-way
  - TPTK: 65% HU → 50-55% 3-way
- Position amplification: IP c-bet frequency 30-45% (not 65%+ as HU).
  Sandwich position: tighten 15-20% vs HU cutoffs.

These are reference points, not decision rules. The agent uses them
as one input alongside position, range composition, board texture,
and action history.

**Section 2 — Decision Framework (how to weigh factors)**

Every 3-way postflop decision depends on the interaction of:

1. **Equity position** — raw equity relative to pot odds
2. **Position** — IP (closing action), OOP (first to act), sandwich
3. **Range composition** — villain_air_pct, villain_tp_plus_pct,
   villain_range_capped, board_favour
4. **Board texture** — danger_score, connectivity, flush/straight
   draws present
5. **Action history** — facing bet, facing raise, bet-and-call,
   multi-street aggression pattern

No single factor is decisive. The correct action emerges from
weighing all five. When factors agree (high equity + IP + air-heavy
villain + dry board), the decision is clear. When factors conflict
(marginal equity but IP with capped villain on dry board), the agent
must reason through the interaction — this is where worked examples
guide the judgment.

**Section 3 — Preflop Construction → Postflop Ranges**

How common 3-way constructions shape the ranges the agent reasons
about:

- CO open / BTN flat / BB defend: BTN is capped (no 3-bet premiums).
  BB is wide/weak. CO has range advantage on A-high and K-high boards.
- HJ open / CO flat / BB defend: CO more capped. HJ owns overpairs
  and AK at highest frequency.
- 3-bet pots that go 3-way: all ranges stronger, c-bet frequency
  drops 20%+.
- Key insight: the two opponents are NOT symmetric. The cold-caller
  is capped; the blind defender is wide. Reasoning must distinguish.

**Section 4 — Board Texture Interactions**

- Dry boards (K72r): PFR c-bets less often (vs HU) because the
  uncapped player still connects. Checking frequency rises for all.
- Monotone boards: equity converges. Aggression signals real holdings.
- Connected middling boards (875): ranges smear. Overbetting
  disappears. Check-call lines increase.

**Section 5 — Worked Examples (initial set, grows over time)**

10-15 fully reasoned examples covering clear/standard/boundary
decisions across the key axes. Each example shows:

1. The hand setup (hero cards, board, position, action context)
2. The factors identified and their values
3. How the factors interact (which dominate, which are overridden)
4. The correct action and why
5. What alternative actions were considered and why rejected

Example format (illustrative — not from the reference set):
```
EXAMPLE: Thin value bet IP on dry board

Setup: Hero Ah9h, board Qs7d2c, BTN (IP), 2 opponents,
       pot 90, checked to hero. CO opened, BTN called,
       BB defended. BB and CO check flop.
Factors:
  - Equity: 45.8% (marginal by reference data)
  - Position: IP with closing action (strong positive)
  - Range composition: villain_air_pct = 0.35 (high air)
  - Board texture: dry, rainbow (low danger)
  - Action: checked to hero (no aggression to respect)

Reasoning: Equity alone suggests CHECK (45.8% is below the
~50% reference for thin value). But IP + high villain air +
dry board shifts the decision. Hero's bet folds out villain's
35% air and gets called by worse pairs. The factor combination
(IP + air + dry) overrides the marginal equity signal.

Action: BET
Confidence: MEDIUM
Alternative: CHECK — reasonable but leaves value on table
             against wide villain range with high air.
```

Note: Initial worked examples will be drawn from real game
situations (not the 24 calibration hands, which are held out).
Each example must use real cards, real boards, and feature
values consistent with the 45-feature pipeline output.

The initial 10-15 examples are drawn from the reference set
reasoning (but NOT from the 24 calibration hands — those are
held out). After each training gate, failure analysis produces
new examples that are added to this section.

**Section 6 — Authoritative Sources**
- GTO Wizard (multiway solutions), MonkerSolver output databases,
  Peter Clarke multiway framework, PokerCoaching.com, Run It Once.

**Section 7 — Ignore List**
- Pre-2018 forum advice, HU-focused content applied to multiway,
  exploitative "read-based" frameworks, anything that uses HU
  c-bet frequencies in multiway spots.

### Research Phase

Before writing the knowledge document, conduct online research using
WebSearch/WebFetch from the main conversation:
1. Search for 3-way postflop GTO principles, solver outputs,
   multiway equity realisation studies
2. Save raw findings to `research/3way_gto_raw.md`
3. Curate into the structured knowledge document
4. Review the document before the agent uses it

This is a one-time pre-build step. The labelling agent never searches.

---

## Prompt File: `prompts/gto_labeller_v1.md`

### Structure

```
1. ROLE
   You are a specialist 3-way postflop GTO labelling agent...

2. KNOWLEDGE BASE
   [Include three_way_gto.md — reference data, decision
    framework, preflop constructions, board textures,
    worked examples]

3. REASONING PROTOCOL
   For each hand:
   a. Assess difficulty (1-3)
   b. Identify the 5 decision factors:
      - Equity position (raw equity vs pot odds)
      - Position (IP / OOP / sandwich)
      - Range composition (villain air, TP+, capped?)
      - Board texture (danger, connectivity, draws)
      - Action history (facing bet/raise, multi-street pattern)
   c. State which factors agree and which conflict
   d. For conflicting factors, reason through the interaction
      (cite a worked example if a similar factor combination exists)
   e. State the correct action with reasoning
   f. For difficulty 3: explicitly consider 2+ alternatives and
      explain why the chosen action is better

4. OUTPUT FORMAT
   Respond ONLY with valid JSON:
   {
     "situation_id": "...",
     "difficulty": 1-3,
     "action": "FOLD|CHECK|CALL|BET|RAISE",
     "confidence": "HIGH|MEDIUM|LOW",
     "reasoning": "2-3 sentences...",
     "key_factors": ["factor1", "factor2"],
     "factor_conflicts": "which factors disagreed and how resolved",
     "alternatives_considered": ["ACTION: why rejected"]
   }

5. DO NOT RULES
   [8 failure modes, each with WHY + example]
```

### DO NOT Rules (with reasoning and examples)

Each rule explains WHY the naive reasoning fails, so the agent
can generalise rather than memorise.

1. DO NOT decide based on equity alone. 3-way decisions depend on
   the interaction of 5 factors. 55% equity is a BET with IP +
   air-heavy villain + dry board, but a CHECK with OOP + strong
   villain range + wet board. Always weigh all factors.

2. DO NOT barrel draws into 2 opponents hoping for folds. 3-way
   fold equity is ~36% (0.6 × 0.6). A flush draw semi-bluff that
   prints money HU (60% fold equity) loses money 3-way. Check and
   realize equity, or check-raise with the nut draw only.

3. DO NOT assume the checking player has nothing. In 3-way pots,
   players trap more because a third opponent may bet for them.
   BB checks, CO checks, BTN bets — BB may check-raise with a set
   they slowplayed specifically because three-way incentivizes it.

4. DO NOT auto-c-bet IP just because you have position. IP c-bet
   frequency 3-way is 30-45%, not 65%+. Two opponents = two chances
   to run into strength. The board texture and range composition
   determine whether to bet, not position alone.

5. DO NOT treat top pair as a strong hand. Top pair is medium-strength
   3-way. The threshold for "strong enough to build a pot" shifts up
   by roughly one hand class: two pair+ to bet big, vs TP+ in HU.
   Top pair good kicker is a pot-control hand, not a value hand.

6. DO NOT overweight blockers. Blocking the nut flush draw matters
   less when there are two opponents — you'd need to block both
   players' draws simultaneously. Blockers are ~40% less influential
   3-way than HU.

7. DO NOT analyze the flop decision without considering turn/river
   SPR. A pot-sized flop bet 3-way leaves SPR ~1.5 on the turn,
   which commits stacks. The flop decision must account for how
   the hand plays on later streets at compressed SPR.

8. DO NOT assume both opponents have equivalent ranges. The preflop
   caller (BTN flat) is capped — no 3-bet premiums. The blind
   defender (BB) is wide but uncapped. Your bet targets them
   differently: the capped player folds strong draws less, the
   wide player folds air more.

### Estimated Prompt Size

- Role + protocol: ~500 words
- Knowledge base: ~2500 words
- DO NOT rules with examples: ~800 words
- Output format + examples: ~200 words
- **Total: ~4000 words (~5K tokens)** — well within the ~8K practical limit

---

## Calibration Exam: `calibration_exam.py`

### Process

1. Convert the 24 three-way reference hands into situation JSONL
   format (same format as training situations)
2. Feed each to the labelling agent (one per call)
3. Compare agent's action to the known expert label
4. Score and report

### Gate: 20/24 (83%)

- Must get 20 of 24 correct
- Must get ALL 3 GTO-reversal hands in the 3-way subset correct:
  - MW-30: expert=FOLD despite 0.399 equity (bet-and-call signal)
  - MW-33: expert=RAISE despite 0.885 equity (set should raise for
    value against bet+call, not flat)
  - MW-50: expert=FOLD despite 0.329 equity (BTN raised flop, strong
    range narrowing)
  Note: MW-31, MW-45, MW-46 are NOT 3-way at decision point
  (they become HU or are 4-way). They appear in other subsets.
- If gate fails: examine failures, adjust knowledge base or prompt,
  re-run. Do NOT proceed to labelling training data.

### Why 20/24

- 3-4 of the 24 are genuine toss-ups (LOW confidence in expert labels)
- 20/24 means the agent can miss only the toss-ups and nothing else
- v8 oracle scores 13/24 — the agent must be substantially better
  than the model it's training

### Script Structure

```python
# calibration_exam.py
def run_calibration(prompt_path, reference_hands_path) -> dict:
    hands = load_reference_hands()  # 24 three-way hands
    results = []
    for hand in hands:
        situation = reference_hand_to_situation(hand)
        label = label_one_hand(situation, prompt_text)
        correct = label["action"] == hand.expert_action
        results.append({...})
    return {
        "accuracy": correct_count / total,
        "gto_reversal_score": reversal_correct / 6,
        "failures": [...],
        "by_confidence": {...},
    }
```

---

## Labelling Pipeline: `labelling_agent.py`

### Process

1. Read situations from `training-data/3way_situations.jsonl`
2. Load prompt from `prompts/gto_labeller_v1.md`
3. For each situation:
   a. Format the hand context into the prompt
   b. Call the agent (one hand per call)
   c. Parse the JSON response
   d. Append to `training-data/3way_labelled.jsonl`
4. Report: action distribution, confidence distribution, agreement
   with oracle, flagged difficulty-3 hands

### Output Format (per line of JSONL)

```json
{
  "situation_id": "d0042_BTN_flop",
  "difficulty": 1,
  "action": "CHECK",
  "confidence": "HIGH",
  "reasoning": "With 5h4h on Qd7c2s 3-way, hero has gutshot + backdoor flush. Equity ~18% too low to bet. Fold equity is ~36% against 2 opponents — not enough. Check to realize equity cheaply.",
  "key_factors": ["low_equity", "insufficient_fold_equity", "draw_potential"],
  "factor_conflicts": "None — all factors agree on CHECK. Low equity, insufficient fold equity, OOP.",
  "alternatives_considered": ["BET: rejected — fold equity only 36% 3-way, naked gutshot not enough"],
  "feat_dict": { ... },
  "hero_cards": "5h4h",
  "board": "Qd7c2s",
  "oracle_action": "CHECK",
  "expert_action": "CHECK"
}
```

### Integration with Export

`export_3way_training.py` (already built) reads this JSONL, excludes
LOW confidence, writes the 45-column CSV. No changes needed to the
exporter.

---

## Sequence

```
1. Research phase: WebSearch/WebFetch for 3-way GTO content
   → Save to research/3way_gto_raw.md
   → Curate into knowledge/three_way_gto.md
   → REVIEW knowledge document

2. Write prompt: prompts/gto_labeller_v1.md
   → REVIEW prompt file

3. Build calibration_exam.py
   → REVIEW script

4. Run calibration on 24 reference hands
   → REVIEW results (must hit 20/24 + all 6 reversals)
   → If fail: adjust knowledge base or prompt, re-run

5. Build labelling_agent.py
   → REVIEW script

6. Generate situations (brute force ~5400 deals, ~7 min)
   → REVIEW output stats (volume, stratification)

7. Run labelling on ~200 situations
   → REVIEW: action distribution, confidence distribution,
     sample of 20 labels for spot-check

8. Export CSV, train v9-3way
   → REVIEW training results + gate check
```

Each numbered step requires review approval before proceeding to
the next step.

---

## What This Spec Does NOT Cover

- Generation approach (decided: brute force 5400 deals with
  all-oracle self-play)
- Training mechanics (decided: warm-start, early_stopping_rounds=10)
- Gate criteria (decided: 14/24 on 3-way reference hands)
- The 4-way and 5-way labelling (future specs, same pattern)

---

## Risk

**LLM reasoning quality.** The agent is Claude reasoning about poker
from a curated document, not a solver computing equilibrium. It will
get some boundary hands wrong. The calibration exam catches systematic
errors. The confidence tagging catches per-hand uncertainty. LOW
confidence labels are excluded from training. This is a quality floor,
not a guarantee.

**Knowledge base gaps.** The pre-built document may miss edge cases
(e.g., squeeze pots, 3-bet pots that go 3-way, specific board
textures). The calibration exam exposes gaps — if the agent fails
on a reference hand, the knowledge base is updated and the exam
re-run.

**Prompt sensitivity.** Small changes to the prompt may shift labels.
The prompt is version-controlled. If we update it, we re-run
calibration to verify the change helped.

---

## Iteration Model

The knowledge base is designed to grow, not change.

```
v1.0: Initial principles + 10-15 worked examples
      → Calibration exam → Label 200 hands → Train v9-3way
      → Gate check: 14/24 on reference set

If gate fails (say 13/24, same as v8):
      → Analyze failures: which hands, which factor interactions
      → Add 3-5 new worked examples from the failures
      → v1.1: Same principles + new examples (additive)
      → Re-run calibration (must still pass 20/24)
      → Relabel the failed situations + supplemental batch
      → Retrain v9-3way, re-gate

If gate passes but accuracy is marginal (14-16/24):
      → Same process: analyze, add examples, relabel, retrain
      → Push toward 18/24, then 20/24 over iterations
```

Each iteration adds examples. Principles stay stable. The agent
gets smarter without contradicting its prior reasoning. No
thresholds change. No previous labels become invalid.

This is why the factor-weighting approach matters: it makes the
knowledge base a living document that improves monotonically.
