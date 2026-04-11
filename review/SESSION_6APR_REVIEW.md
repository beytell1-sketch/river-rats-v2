# Review: 6 April 2026 Session — Files for Approval

**Reviewer:** Claude Code (self-review before owner approval)
**Status:** BLOCKED — generation yield problem unresolved

---

## Files Produced This Session

### 1. oracle_router.py (NEW) — READY FOR REVIEW

**Purpose:** Selects specialist model by opponent count. Auto-discovers
model files, falls back to nearest available.

**What it does right:**
- Clean interface: `router.predict(feat_dict, num_opponents)`
- Legacy fallback (v8_38feat.json if v8_hu.json missing)
- Clamps 5+ opponents to 5-way slot
- `has_specialist()` for checking availability
- 11 tests pass

**Concerns:**
- None. This is simple routing logic. Works correctly.

**Decision needed:** None — ship to river-rats-core/.

---

### 2. self_play.py (MODIFIED) — NEEDS DISCUSSION

**Changes made:**
1. All 6 seats now use oracle callbacks (was: 1 hero + 5 heuristic)
2. `decision_log` made optional in `_make_oracle_callback()`
3. `HeroDecision` expanded with feat_dict, hero_cards, board,
   villain_positions, facing_bet
4. Router integration (accepts OracleRouter or GtoOracle)
5. Docstring still says "Opponents use the same heuristic AI" — STALE

**What it does right:**
- Oracle opponents produce realistic ranges and natural multiway pots
- Decision logging is opt-in (opponents don't log, saving memory)
- feat_dict capture enables training data export
- 18 tests pass, backward compatible

**Concerns:**

**[BLOCKER] Yield is still low.** 1000 deals → 37 three-way decisions
(3.7%). GTO preflop ranges at 6-handed are genuinely tight. Most pots
go heads-up even with oracle opponents. Need ~5400 deals for 200
three-way decisions (~7 minutes runtime). This is workable but wasn't
validated before writing the spec or building the pipeline.

**[SHOULD_FIX] The docstring at line 5 is wrong.** Still says
"Opponents use the same heuristic AI." Must be updated.

**[SHOULD_FIX] Performance regression.** 18 tests went from ~6s to
~20s (3.3x). All-oracle seats means 6x more feature extraction per
game. This is acceptable for generation but affects developer
experience on every test run.

**[QUESTION] Is the all-oracle approach correct for variant testing?**
The original self-play loop compared variants against identical
opponents. With oracle opponents, opponents use baseline params while
hero uses variant params. If opponent behaviour differs between
variant runs (because the hero's actions change the game state,
which changes opponent decisions), the duplicate-deal isolation is
weakened. Is this a problem?

**Decision needed:** Approve all-oracle, or discuss the variant
isolation concern first.

---

### 3. generate_3way_situations.py (NEW) — NEEDS REWORK

**Purpose:** Run self-play, filter to 3-way postflop, export JSONL.

**Problems:**

**[BLOCKER] Contains dead code.** The `_loose_opponent_callback`
function (lines 29-95) is from a failed attempt to boost yield by
making opponents call wider preflop. It's never used by the runner
(line 107 sets an attribute the runner ignores). This is dead code
that misleads readers.

**[BLOCKER] The print message "opponents use loose preflop" (line
102) is wrong.** Opponents use oracle callbacks (from self_play.py
change), not the loose callback. The message lies.

**[CONCERN] Yield problem unsolved.** The script works correctly —
it generates, filters, and exports. But 3.7% yield means it needs
~5400 deals for 200 decisions. The spec assumed 150 deals would
suffice. Nobody checked.

**Decision needed:** Remove dead code, fix message, decide on
generation approach (brute force 5400 deals, or situation
constructor, or hybrid).

---

### 4. label_3way_situations.py (NEW) — NEEDS DEEP REVIEW

**Purpose:** Rule-based GTO labeller. Reads features, applies poker
logic, outputs action + confidence + reasoning.

**What it does right:**
- Uses all relevant features (range composition, equity, hand
  strength, board texture, position, action context)
- Distinguishes facing_raise, num_callers (bet-and-call signal)
- Confidence tagging (HIGH/MEDIUM/LOW)
- Reasoning string for every label

**Concerns:**

**[MAJOR] This is a rule-based heuristic, not a GTO expert.** The
labeller is ~200 lines of if/elif chains. It's a more sophisticated
version of the multiway adjuster we just proved doesn't work.
Threshold-based rules like "if equity > pot_odds + 0.15 and
is_strong: RAISE" are exactly the kind of logic the self-play loop
proved is the wrong approach.

The spec says "GTO Expert labels each decision." This labeller is
not that — it's a coded heuristic. A real GTO expert labelling
process would involve either:
(a) An LLM agent reasoning about each hand with full poker context
(b) A human expert reviewing each situation
(c) A solver computing equilibrium strategies

This labeller will produce labels that are correlated with the
adjuster's existing biases. Training on these labels risks
circular learning — the model learns to match a heuristic that
we've already proved has a ceiling.

**[QUESTION] Was this intended as a placeholder, or is this the
actual labelling approach?** If placeholder, it needs to be clearly
marked. If actual, it undermines the entire progressive model chain
— we'd be training the model to match coded rules instead of
learning GTO play.

**Decision needed:** This is the critical question. The labeller
determines whether the training data is actually better than what
we have. If it's just another heuristic, the v9-3way model will
hit the same ceiling as the adjuster.

---

### 5. export_3way_training.py (NEW) — READY FOR REVIEW

**Purpose:** Convert labelled JSONL to 45-column CSV, excluding LOW
confidence labels.

**What it does right:**
- Excludes LOW confidence (per spec)
- Reports stratification stats
- Warns if volume drops below 180
- Clean CSV output matching FEATURE_COLUMNS

**Concerns:**
- Line 74-77: street stratification uses numeric encoding (0/1/2)
  but the feat_dict may have the encoded value, not the string.
  Minor — cosmetic reporting, doesn't affect training data.

**Decision needed:** None — ship after labeller question is resolved.

---

## Summary of Decisions Needed

| # | Question | Blocking? |
|---|----------|-----------|
| 1 | Generation yield: brute force (5400 deals, ~7 min) or different approach? | YES |
| 2 | Labeller: rule-based heuristic OK, or need real expert (LLM/human/solver)? | YES |
| 3 | All-oracle opponents: does this weaken variant isolation for future self-play? | NO (discuss) |
| 4 | oracle_router.py: approve for river-rats-core/? | NO (ready) |
| 5 | export_3way_training.py: approve for river-rats-core/? | NO (ready) |

**My recommendation:**

Q1: Brute force 5400 deals. It's 7 minutes, no new code, and the
situations are real 6-seated game play. The alternative (situation
constructor) produces synthetic data that may not match production.

Q2: This is the big one. The rule-based labeller is a risk. It's
better than the adjuster (it uses range features the adjuster
doesn't see), but it's still threshold-based heuristics. If you
want labels that actually represent GTO play, you need either an
LLM agent doing per-hand poker reasoning, or you accept the
heuristic labeller as "good enough for v9-3way" and plan to
improve labelling quality for v9-4way/5way. I'd flag this for
your review — you've been burned by heuristic ceilings before.
