# Independent Review: BET_DECISION_TREE_V1.md

**Date:** 9 April 2026
**Reviewer:** Independent Reviewer (Creative Lead instance)
**Target file:** `review/BET_DECISION_TREE_V1.md`
**Reference files consulted:**
- `review/RAISE_DECISION_TREE_V2.md`
- `river-rats-core/feature_keys.py`
- `river-rats-core/feature_extractor.py`
- `review/RESEARCH_CBET_R2_TEXTURE.md`

**Verdict: ISSUES FOUND**

Three items require a fix before owner sign-off. Seven additional items are
flags, notes, or minor inconsistencies that do not block approval but should
be on record. Each is numbered and severity-rated below.

---

## Critical Issues (must fix)

### ISSUE 1 — CRITICAL: Quick Reference uses undefined alias `is_pfa`

**Location:** Quick Reference: Hands That BET table (all rows), Quick Reference:
Hands That CHECK table (row "NFD without blocker OOP").

**Problem:** Every row in the Quick Reference table uses `is_pfa=1` as a
shorthand. There is no feature named `is_pfa` anywhere in `feature_keys.py`
or the 53-feature vector. The correct feature name is `is_preflop_aggressor`.

The tree body uses the correct name throughout (Steps 2, 3, 4, 5). The Quick
Reference table then contradicts it with an undefined alias. A labelling agent
that is given ONLY the Quick Reference as a shortcut (which is exactly how quick
references get used) will try to look up `is_pfa` in the feature vector, fail,
and either crash or silently skip the condition.

**Required fix:** Replace every instance of `is_pfa=1` in the Quick Reference
tables with `is_preflop_aggressor=1`. Also replace `is_pfa=0` in the Step 5
row with `is_preflop_aggressor=0`.

---

### ISSUE 2 — CRITICAL: Step 3B OOP value bet threshold inconsistency with suppressor S2

**Location:** Step 3B conditions vs Suppressor S2 definition.

**Problem:** Suppressor S2 fires when:
- `is_ip == 0`
- `is_monster == 0`
- `hero_range_percentile < 0.72`
- `raw_equity < 0.60`

The note after S2 says: "Steps 2 and 6 provide the OOP exceptions that override
this suppressor." Step 3B is NOT listed as an S2 override. However, Step 3B
requires `hero_range_percentile >= 0.72` and `raw_equity` is not gated (Step 3B
requires `is_made_hand == 1` and `board_favour >= 0.35` but no raw_equity floor).

The tree body says S2 applies to "Steps 3, 4, and 5 only." This means S2 CAN
fire on Step 3B situations. But Step 3B requires `hero_range_percentile >= 0.72`,
which satisfies S2's `hero_range_percentile < 0.72` condition in reverse — so S2
would NOT fire when hero_range_percentile >= 0.72. That half is fine.

The gap is raw_equity. A hand could have `hero_range_percentile >= 0.72` (top 28%
of range) but `raw_equity < 0.60`. S2 would then fire and force CHECK before
Step 3B runs. But is that the right outcome? TPGK on a dry rainbow board can
realistically be in the top 28% of range while having raw equity below 60% in a
3-way pot.

More importantly, the Suppressor Summary table lists S2 as "Force CHECK (Steps
3, 4, 5)" — implying it blocks Step 3B (which is part of Step 3). But the step
ordering in the preamble says "Steps 2 and 6 have explicit OOP carve-outs built
into their conditions." Step 3B is neither Step 2 nor Step 6.

**The inconsistency:** The tree says S2 applies to "Steps 3, 4, and 5" which
includes 3B, but 3B is designed as an OOP exception. If S2 can suppress 3B, then
S2 and 3B are partially redundant and the labelling agent gets inconsistent
outputs depending on whether raw_equity happens to be above or below 0.60.

**Required fix:** Either (a) add Step 3B to the list of S2 overrides (alongside
Steps 2 and 6) and note why its conditions already enforce stricter standards than
S2, or (b) explicitly add a `raw_equity >= 0.50` floor to Step 3B so that the
S2 raw_equity gate can never silently kill a 3B that meets all 3B conditions.
Option (a) is simpler and more honest — Step 3B's seven conditions are already
tighter than S2's two conditions; S2 adding a redundant veto is just confusion.

---

### ISSUE 3 — CRITICAL: Tier boundary ambiguity creates dead zone at Tier 1/2 boundary

**Location:** Step 3A, Tier determination block.

**Problem:** The four tier definitions share boundary values, creating ambiguous
classification at the edges.

Tier 1: `high_card_rank >= 13` AND `flush_danger <= 0.20` AND `connectivity_score <= 0.30`
Tier 2: `high_card_rank >= 11` AND `flush_danger <= 0.35` AND `connectivity_score <= 0.55`

A board with `high_card_rank == 13` (King), `flush_danger == 0.25`,
`connectivity_score == 0.35` satisfies Tier 2 but NOT Tier 1 (flush_danger > 0.20
and connectivity_score > 0.30). So it is Tier 2. That is fine.

But consider: `high_card_rank == 13`, `flush_danger == 0.18`, `connectivity_score == 0.28`.
This satisfies BOTH Tier 1 (all three conditions pass) AND Tier 2. No priority rule
is stated. Which tier applies?

Then consider Gate 3A-3's requirement: "Tier 1: hand_category >= 6. Tier 2:
hand_category >= 7." A hand with hand_category == 6 (top_pair, weak kicker) on a
board qualifying as BOTH Tier 1 and Tier 2 gets BET under Tier 1 rules but would
need hand_category >= 7 under Tier 2 rules.

The tree never states "use the most favorable tier" or "use Tier 1 if all Tier 1
conditions are met, else check Tier 2." Without a priority rule, a hand_category
== 6 hand on an ambiguously classified board has an undefined label.

**Required fix:** Add an explicit priority rule: tiers are evaluated from 1 to 4
in descending favorability; the first tier whose conditions are satisfied applies.
Equivalently, make the tier conditions mutually exclusive by adjusting the boundary
values so no board can satisfy both Tier 1 and Tier 2. The simplest fix is a single
sentence: "Evaluate Tier 1 first. If all Tier 1 conditions pass, apply Tier 1 gate.
Otherwise evaluate Tier 2, then Tier 3, then Tier 4."

---

## Should-Fix Items (do not block approval but should be addressed)

### ISSUE 4 — SHOULD_FIX: Step 2 static board path is implicit, not explicit

**Location:** Step 2, closing note: "Dry board monster (does NOT fire this step):
`is_monster == 1` AND `danger_score < 0.30` — proceed to Step 3 (trap check) or
Default CHECK."

**Problem:** The tree correctly notes that monsters on dry boards skip Step 2 and
trap via the Default (Step 7 CHECK). But the stated threshold for "does NOT fire"
is `danger_score < 0.30`, while Step 2's positive trigger requires `danger_score >= 0.45`.
There is a gap between 0.30 and 0.45. A monster with `danger_score == 0.38` neither
fires Step 2 (requires >= 0.45) nor falls into the "dry board" definition (requires
< 0.30). The tree gives no guidance for this gap range.

In poker terms: a monster on a semi-wet board (mild danger, not quite dynamic, not
quite dry). The correct answer is likely CHECK (lean toward trap), but the tree does
not say so.

**Required fix:** Either close the gap (change the "does NOT fire" note to
`danger_score < 0.45` to match the step's own trigger threshold) or add a sentence
explaining what happens in the 0.30–0.45 range. The most accurate statement is
"danger_score in range 0.30–0.45 with is_monster == 1: Step 2 does not fire
(danger insufficient to mandate protection); proceed to Default CHECK (trap)."

---

### ISSUE 5 — SHOULD_FIX: Feature vector count discrepancy (52 vs 53)

**Location:** RAISE tree preamble and feature reference table says "52-feature
vector." BET tree preamble says "53-feature vector." feature_keys.py comments
label features up through "Step 14: new feature 53" (IS_PREFLOP_AGGRESSOR).

**Observation:** The RAISE tree was written before IS_PREFLOP_AGGRESSOR was added
(it was "feature 53" added in Step 14). The BET tree correctly counts 53. However,
the RAISE tree's feature reference table does NOT list `is_preflop_aggressor`, and
the RAISE tree does NOT use it in any condition. If the RAISE tree is used with the
53-feature vector, `is_preflop_aggressor` is silently available but unused.

**Impact on BET tree:** None directly. The BET tree correctly uses feature 53.
This is flagged as a cross-tree hygiene issue. The RAISE tree should be updated
at its next revision to acknowledge the 53-feature vector and note whether
`is_preflop_aggressor` is relevant to any RAISE condition (e.g., Step 4 OOP
thin value check-raise might benefit from knowing if hero is the PFA).

**No change required in BET tree.** Flag for RAISE tree next revision.

---

### ISSUE 6 — SHOULD_FIX: Step 4D rainbow-board restriction may over-suppress

**Location:** Sub-condition 4D, last two conditions.

**Condition:** `is_rainbow == 1` with rationale "on two-tone board, one villain has
flush draw regardless of blocker."

**Problem:** The rationale is correct in direction but overstated. On a two-tone
board, one villain MIGHT have a flush draw — it is not guaranteed. `flush_block_pct`
measures how much of villain's flush combos are blocked by hero's holding. On a
two-tone board, if hero holds the Ace of the flush suit AND a blocker card, the
`flush_block_pct` already captures this. Requiring `is_rainbow == 1` on top of
`flush_block_pct > 0` double-gates the condition and may exclude legitimate
edge-case bets on lightly two-tone boards where hero holds the nut blocker.

**Severity:** Low. The 4D sub-condition is already heavily restricted (IP only,
high_card_rank >= 13, villain_air >= 0.40, draw_outs >= 4). An additional
is_rainbow gate makes it an extremely narrow path. The poker cost is probably
small. However, the stated rationale is logically imprecise.

**Suggested fix:** Replace the is_rainbow requirement with `flush_danger <= 0.25`
(the two-tone vs rainbow boundary is more precisely captured by flush_danger than
by the binary is_rainbow flag, which only encodes "zero suited cards on board").
Alternatively, keep is_rainbow but correct the rationale to say "is_rainbow
preferred because two-tone boards add villain flush draw equity that flush_block_pct
alone may not fully capture."

---

### ISSUE 7 — NOTE: Research alignment on middle connected boards

**Location:** Frequency-to-Threshold Mapping table, row "IP PFA, connected mid
(T86): 22-30%."

**Observation:** The BET tree notes the R1/R2 disagreement (R1: 22-30%, R2: 25-40%)
and resolves it conservatively with hand_category >= 10 (two_pair). RESEARCH_CBET_R2_TEXTURE
Section 2.5 gives the middle connected board (T-8-6r, J-9-7r) frequency as 30-40%,
with sources citing "betting only with genuine two-pair+ or nut draw-type hands."

The tree's resolution (two_pair+ for Tier 3) is consistent with R2 Section 2.5's
language and is appropriately conservative. This is not an error — it is correctly
documented in Gap 4. No change required; confirming alignment.

---

### ISSUE 8 — NOTE: Reviewer reconciliation item R2 IP annotation — addressed

**Location:** Changelog entry 7 and Key Design Decisions.

**Observation:** The cross-review Issue 4 (R2 frequency tables were IP PFA figures,
OOP approximately 30-40% lower) is explicitly called out in the Preamble and
enforced structurally via S2 and the OOP carve-outs in Steps 3B and 6. This is
fully addressed. No gap found.

---

### ISSUE 9 — NOTE: Reviewer reconciliation items R3/R4 MDF conflict — addressed

**Location:** Known Limitations and Gaps, Gap 6.

**Observation:** The R3/R4 MDF framing difference (per-opponent 86.7% vs combined
56% fold rate) is acknowledged in Gap 6 and correctly noted as two framings of the
same math. The tree's output is consistent: pure air does not bet. No structural
issue.

---

### ISSUE 10 — NOTE: Step 5 validator check redundancy

**Location:** Step 5, Validator check paragraph.

**Observation:** Step 5 already requires `villain_aggression_count <= 1` in its
main conditions. The "Validator check" paragraph then repeats: "If
`villain_aggression_count >= 2`, do NOT fire this step." This is a direct duplicate
of the main condition stated as a second check. This is not harmful but is mildly
confusing — a labelling agent reading carefully will wonder if there is a gap
between the main condition and the validator that requires separate handling.

**Suggested fix:** Remove the Validator check paragraph and consolidate into the
main condition list with a clarifying comment. Alternatively, keep it but label
it "Note: this condition is already encoded above — included for emphasis only."

---

## Structural Checks Checklist

| Check | Result |
|-------|--------|
| Every branch outputs BET or CHECK (never a frequency) | PASS — all steps output BET or CHECK |
| Every condition references a named feature from 53-vector | PASS (body) / FAIL (Quick Reference — see Issue 1) |
| All feature names real (match feature_keys.py class F) | PASS (body) / FAIL (Quick Reference `is_pfa` — see Issue 1) |
| Default is CHECK | PASS — Step 7 is explicit Default CHECK |
| Pre-check: `to_call == 0` | PASS — Global Pre-Check A is correct |
| Pre-check: `num_callers_to_bet == 0` | PASS — Pre-Check B is present |
| `num_opponents >= 1` check | PASS — Pre-Check C is present |

---

## Poker Logic Checks

| Check | Result |
|-------|--------|
| Monster protection distinguishes dynamic (bet) vs static (check/trap) | PASS — Step 2 fires only on danger_score >= 0.45; dry board falls to Default CHECK. Gap in 0.30–0.45 range documented in Issue 4 |
| PFA bluff c-bet requires outs or blocker (pure air never bets 3-way) | PASS — Step 4 has no path for draw_outs < 4; backdoor-only explicitly suppressed |
| OOP thresholds consistently tighter than IP | PASS — S2 enforces OOP restriction; Steps 3B and 6 have stricter conditions than Step 3A/5 |
| Tree uses is_preflop_aggressor (feature 53) | PASS — used in Steps 2, 3, 4, 5; correctly identified as feature 53 |
| Path exists for non-PFA defenders to bet (narrow donk-bet path) | PASS — Steps 5 and 6 provide non-PFA bet paths; correctly narrow and documented |

---

## Research Alignment

| Check | Result |
|-------|--------|
| A-high dry: 60-70% frequency maps to wide gate (hand_category >= 6) | PASS — Tier 1 gate matches R2 Section 2.1 and R1 Finding 6 |
| Low connected: 20-30% maps to narrow gate (hand_category >= 10 or no fire) | PASS — Tier 4 excluded; Tier 3 gate at two_pair matches R2 Section 2.4/2.5 |
| Monotone boards excluded from Step 3A (Tier 4) | PASS — Tier 4 routes to Default; consistent with R2 Section 2.6 (monotone ~20-30%, sets/nut flush only) |
| OOP 22-30% enforced via hero_range_percentile >= 0.72 | PASS — S2 threshold is consistent with top 28% = 22-30% of range betting |
| R2 IP annotation (Issue 4 from cross-review) | PASS — documented and enforced throughout |
| R3/R4 MDF conflict (Issues R3/R4) | PASS — resolved and documented in Gap 6 |
| R4 unsourced check-fold rate | NOTE — not explicitly located in this tree; no check-fold rate is cited as a hard threshold. R4 material appears as directional references. No error found |

---

## Comparison With RAISE Tree

| Check | Result |
|-------|--------|
| Trees cover all situations (RAISE: to_call > 0; BET: to_call == 0) | PASS — Pre-checks are complementary and non-overlapping |
| No overlapping conditions where both trees could fire | PASS — BET tree requires to_call == 0; RAISE tree applies when to_call > 0. Mutually exclusive by pre-check |
| Structural quality comparable (changelog, preamble, feature reference, quick reference) | PASS — BET tree matches or exceeds RAISE tree structure. Changelog is more detailed. Feature Reference table is more complete. Known Limitations section is an improvement over RAISE tree |
| Feature vector count discrepancy (52 vs 53) | NOTE — RAISE tree says 52; BET tree says 53. BET tree is correct. RAISE tree predates feature 53. See Issue 5 |

---

## Summary of Findings

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | CRITICAL | Quick Reference tables | `is_pfa` alias used — not a real feature name; must be `is_preflop_aggressor` |
| 2 | CRITICAL | Step 3B vs Suppressor S2 | S2 override list excludes Step 3B; raw_equity gate in S2 can silently kill valid 3B bets |
| 3 | CRITICAL | Step 3A Tier definitions | No priority rule for overlapping Tier 1/2 conditions; ambiguous classification for hands at boundary |
| 4 | SHOULD_FIX | Step 2 closing note | Gap between danger_score 0.30–0.45 for monsters — neither "fire Step 2" nor "dry board trap" |
| 5 | SHOULD_FIX | Cross-tree | RAISE tree still says 52-feature vector; should be updated to 53 at next revision |
| 6 | SHOULD_FIX | Step 4D | `is_rainbow == 1` double-gates with `flush_block_pct > 0`; rationale overstated |
| 7 | NOTE | Freq mapping table | R1/R2 middle connected disagreement — correctly resolved and documented; no error |
| 8 | NOTE | Changelog | R2 IP annotation reconciliation — fully addressed |
| 9 | NOTE | Gap 6 | R3/R4 MDF conflict — acknowledged and correctly resolved |
| 10 | NOTE | Step 5 | Validator check paragraph duplicates a main condition — minor cleanup recommended |

**Issues 1, 2, and 3 must be resolved before this document is approved.**
Issues 4 and 6 are recommended fixes that improve precision without changing
the tree's fundamental logic. Issues 5, 7, 8, 9, and 10 are documentation
notes that do not require tree changes.

---

*Reviewer: Independent Review Agent*
*File reviewed: `/home/rupertbeytell/river-rats-v2/review/BET_DECISION_TREE_V1.md`*
*Review written to: `/home/rupertbeytell/river-rats-v2/review/comms/REVIEW_BET_DECISION_TREE_V1.md`*
