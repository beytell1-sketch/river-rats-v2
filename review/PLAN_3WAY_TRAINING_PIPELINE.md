# Plan: 3-Way Training Pipeline

**Date:** 6 April 2026
**Status:** PLAN — awaiting review before any building
**Context:** Infrastructure shipped (45-feat pipeline, model router,
v9-baseline, all-oracle self-play). This plan covers generating,
labelling, and training v9-3way.

---

## What We Have

- `self_play.py` — all 6 seats use oracle callbacks (tested, 18/18 pass)
- `oracle_router.py` — model selection by opponent count (tested, 11/11 pass)
- `v9-baseline` — 45-feature model trained on PokerBench (91.9% HU, 52.5% MW)
- `HeroDecision` — captures full feat_dict + hand context per decision
- 24 three-way reference hands — validation gate (v8 baseline: 12/24)

## What We Need to Build

Four things, in order. Each one reviewed before the next starts.

---

### Step 1: Generate situations

**What:** Run self-play with all-oracle seats, collect 3-way postflop
decisions with full feature vectors.

**Open question — yield:**
1000 deals produced 37 three-way decisions (3.7% yield). GTO preflop
at 6-handed is genuinely tight. Options:

| Approach | Deals needed | Runtime | Pros | Cons |
|----------|-------------|---------|------|------|
| Brute force | ~5400 | ~7 min | Real game play, no new code | Slow, wasteful |
| Multiple seeds | 5 × 1000 | ~7 min | Same as above, more variety | Same yield problem |
| Situation constructor | 0 | Seconds | Unlimited volume, fast | Synthetic — no real game context, action-history features are guesses |

**My recommendation:** Brute force with multiple seeds. It's 7 minutes
of compute, produces real 6-seated game situations with natural preflop
filtering, and requires no new code beyond fixing the dead code in
generate_3way_situations.py.

**Files involved:**
- `generate_3way_situations.py` — REWRITE (remove dead loose_callback
  code, fix misleading print message, increase default deals to 2000)

**Your decision needed:** Which approach?

---

### Step 2: Label situations

**What:** Assign correct GTO action + confidence to each situation.

**Open question — this is the critical one:**

The current `label_3way_situations.py` is a rule-based heuristic
(~200 lines of if/elif). It uses the features to make threshold-based
decisions. This is a more sophisticated adjuster, not a GTO expert.
Training on its output risks circular learning.

Three labelling approaches:

| Approach | Quality | Speed | Risk |
|----------|---------|-------|------|
| **A. Rule-based heuristic** (current code) | MEDIUM — uses range features the adjuster doesn't, but still threshold logic | Fast (seconds) | Circular — model learns to match coded rules, same ceiling |
| **B. LLM agent per hand** — Claude reads the hand context, reasons about ranges, assigns action | HIGH — real poker reasoning, considers context holistically | Slow (~2-3 hours for 200 hands) | LLM may have poker knowledge gaps, needs spot-checking |
| **C. Hybrid** — rule-based for clear situations (equity >> pot odds = CALL, no hand = FOLD), LLM agent for ambiguous spots (marginal made hands, semi-bluffs, thin value) | HIGH where it matters — expert reasoning on the decisions that actually move the needle | Medium (~1 hour) | Complexity of deciding which hands are "clear" vs "ambiguous" |

**My recommendation:** Option B (LLM agent). The whole point of the
progressive chain is to get BETTER labels than the adjuster produces.
Rule-based heuristics are what we're trying to replace. The 2-3 hour
cost is a one-time investment for the 3-way training set.

The LLM agent would receive for each hand:
- Hero cards, board, street, position
- Villain positions and what ranges they represent (from preflop action)
- Pot, to_call, facing_bet/raise context
- The range composition features (villain_air_pct, tp_plus_pct, etc.)
- The oracle's current prediction (for reference, not as anchor)

And would output:
- action: FOLD/CHECK/CALL/BET/RAISE
- confidence: HIGH/MEDIUM/LOW
- reasoning: 2-3 sentences of poker logic

**Files involved:**
- `label_3way_situations.py` — REWRITE (replace rule engine with LLM
  agent calls, or delete and build fresh)

**Your decision needed:** Which labelling approach? If B, do you want
the LLM agent to be a Claude API call, or a subagent within Claude
Code, or something else?

---

### Step 3: Export and train

**What:** Convert labelled JSONL to CSV, warm-start v9-baseline into
v9-3way.

**No open questions.** The spec is clear:
- Exclude LOW confidence labels
- Minimum 180 usable rows
- Warm-start with `xgb_model` parameter
- `early_stopping_rounds=10` on 24 reference hands
- Save as `gto_model_v9_3way.json`

**Files involved:**
- `export_3way_training.py` — EXISTS, reviewed, minor fix needed
  (street encoding in reporting)
- `train_v9_3way.py` — NEW script for warm-start training

---

### Step 4: Gate check

**What:** Evaluate v9-3way on reference set.

**No open questions.** Gate: >= 14/24 on 3-way hands. No HU regression.

**Files involved:**
- `reference_evaluator.py` — EXISTS, works
- `run_eval.py` — EXISTS, needs update to test v9-3way via router

---

## Files That Need Cleanup Before Proceeding

| File | Issue | Fix |
|------|-------|-----|
| `generate_3way_situations.py` | Dead `_loose_opponent_callback` code (95 lines), wrong print message | Remove dead code, fix message |
| `label_3way_situations.py` | Rule-based heuristic pretending to be GTO expert | Rewrite or delete depending on labelling decision |
| `self_play.py` line 5 | Docstring says "heuristic AI" | Update to "oracle callbacks" |

---

## Sequence

```
1. You review this plan, answer the two open questions
2. I clean up the files listed above
3. You review the cleaned files
4. I run generation (Step 1) — present output stats for review
5. You approve the situations
6. I run labelling (Step 2) — present sample labels for review
7. You spot-check labels
8. I export + train (Step 3) — present training results
9. I run gate check (Step 4) — present results
10. You decide: pass/fail/iterate
```

Nothing runs without your go-ahead at each step.
