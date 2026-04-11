---
date: 2026-04-09
from: Independent Reviewer
re: FACTORY_DESIGN_BET_CONTEXTS.md — review
verdict: ISSUES FOUND (3 issues, 1 open question — none are blockers if addressed)
---

## Verdict: ISSUES FOUND

The brief is well-constructed. It is grounded in the recalibration results, each
sub-pattern traces directly to a blocked step, and the diversity framework is
specific and measurable. However, three issues require correction before the brief
is used as a build spec, and one open question must be resolved by the owner.

---

## Check 1: Do BP1-BP6 Target the Correct Blocked Tree Steps?

PASS.

| Sub-pattern | Target step | Recalibration blocking condition | Match? |
|-------------|-------------|----------------------------------|--------|
| BP1 | 3A | No IP PFA situations | Yes |
| BP2 | 3B | villain_air_pct never reaches 0.40 | Yes |
| BP3 | 4A-D | All OOP + suppressed; no 12+ out draws | Yes |
| BP4 | 5 | Zero IP made-hand situations with hand_category >= 7 | Yes |
| BP5 | 6 | villain_aggression_count always >= 1 for eligible candidates | Yes |
| BP6 | Default/suppressors | (counterexamples — correct approach) | Yes |

Every sub-pattern addresses the exact failure mode reported in
BET_TREE_RECALIBRATION_RESULTS_2026-04-09.md. No step is missing.

---

## Check 2: Do Feature Requirements Match the Tree's Conditions?

PASS with one exception — see Issue 1 below.

All step conditions are correctly transcribed:
- Step 3A tier conditions (high_card_rank, flush_danger, connectivity_score thresholds) match the tree.
- Step 3B conditions (villain_air_pct >= 0.40, villain_aggression_count = 0,
  high_card_rank >= 13, hero_range_percentile >= 0.72, is_rainbow = 1) match.
- Step 4 sub-conditions 4A-4D match.
- Step 5 conditions match (danger_score <= 0.35, villain_range_capped = 1,
  villain_top_pair_plus_pct <= 0.35, villain_aggression_count <= 1).
- Step 6 conditions match (raw_equity >= 0.65, villain_air_pct >= 0.45,
  is_rainbow = 1, connectivity_score <= 3, villain_aggression_count = 0).
- The Tree Alignment table at the end of the brief is accurate.

ISSUE 1 — BP3 sub-condition 4C board_favour inconsistency:

The tree alignment table correctly lists sub-condition 4C as requiring
board_favour >= 0.30. The tree step 4 itself states board_favour is retained in
the 53-feature vector and is valid as a design constraint. However, the Feature
Reference Table in BET_DECISION_TREE_V1.md marks board_favour as [DEMOTED] with
the note "no longer used as primary gate." The brief's use of board_favour as a
design parameter for sub-condition 4C (not as a primary gate, but as a
situational specification) is technically correct — the condition still exists in
step 4C of the tree. But the brief does not explain this distinction. A builder
reading the Feature Reference Table will see [DEMOTED] and may incorrectly exclude
board_favour from the 4C specification.

FIX REQUIRED: Add a note in the BP3 sub-condition 4C section: "board_favour is
demoted as a primary gate but remains an active condition in sub-condition 4C
specifically. It is not computed from high_card_rank — it is a separate feature
in the 53-vector. Do not substitute high_card_rank >= 12 here."

---

## Check 3: Are the Counts Reasonable?

PASS.

- BP1 at 30 is appropriate: Step 3A is the highest-frequency BET generator in
  real poker and has the most sub-variation (3 texture tiers, 4 hand types).
- BP2 at 15 is appropriate: Step 3B is a narrow OOP exception; 15 situations with
  5 unique boards is sufficient to establish the pattern.
- BP3 at 20 with 4A:8 / 4B:6 / 4C:3 / 4D:3 distribution is appropriate given
  that 4A is the broadest sub-condition and 4D is the most restricted edge case.
- BP4 at 15 and BP5 at 10 are proportionate to their step frequency.
- BP6 at 10 is the minimum acceptable counterexample count for a 90-BET-intent
  batch. It is on the low side but defensible given the targeted failure-mode
  structure (7 specific failure modes).

The projected label yield calculation (73-78 confirmed BETs post-labelling,
reaching ~82-87 total with the existing 9) is reasonable based on the 85% RAISE
batch precedent.

---

## Check 4: Are Diversity Requirements Present and Measurable?

PASS.

All R1-R7 requirements are specific and verifiable:
- R1: 15 unique boards minimum, max 8 per board — countable.
- R2: Texture distribution with explicit min/max per texture type — countable.
- R3: SPR tier distribution with percentage thresholds — computable.
- R4: Street distribution with explicit min/max — countable.
- R5: Position distribution 55-65% IP — countable. Sub-pattern breakdown is provided
  and the arithmetic checks out (67 IP, 33 OOP, within target).
- R6: Per-sub-pattern board/situation limits — specific.
- R7: Villain-feature variance requirements for large sub-patterns — measurable
  (min range specified as max - min).

The reviewer checklist at the end (18 items) maps directly to these requirements.

---

## Check 5: Will Specified Action Histories Produce the Right Feature Values?

PASS for most. One structural ambiguity flagged — see Issue 2.

villain_air_pct: The construction guidance is detailed and plausible. The K42r
example for BP2 (40-48% air from BTN cold-caller) follows correct range logic.
The instruction to avoid BB as villain for BP2 (air fraction 25-35%) is correct.
The BP5 guidance on low boards (7-6-2r giving 40-50% air for wide openers) is
directionally sound, with the appropriate caveat that 7-6 adjacent boards may
push connectivity_score above 3 — the brief correctly redirects to genuinely
disconnected low boards (7-4-2r, 8-4-2c) and confirms these are preferred.

villain_aggression_count: The guidance correctly defines that villain calling
preflop and checking the flop produces villain_aggression_count = 0. The turn
variant (villain check-called flop) is also correctly identified as
villain_aggression_count = 0. The note that villain_aggression_count counts
prior-street bets (not this street) is important and correct.

ISSUE 2 — BP4 villain_range_capped construction contains an internal contradiction:

In the BP4 action sequence prototypes, two structures are offered:

Structure A: BTN opens, hero (CO) cold-calls, BB calls.
  Flop: BB checks, BTN checks → CO acts. Villain is BTN (opener).
  The brief states villain (BTN) range is capped. This is WRONG.
  BTN is the PFA (opener). Openers are not capped — they can hold AA, KK, AK.
  villain_range_capped = 1 should not be set for an opener's range.

Structure B: CO opens, hero (BTN) calls, BB calls. CO checks flop → BTN acts.
  villain = CO (PFA who checked). A PFA who checked back is not capped by default.

The "Preferred structure" section then introduces a third structure:
  CO opens → BTN calls (hero) → BB calls.
  The brief states "CO is PFA but CHECKED — this is a common delayed c-bet situation.
  BTN has to_call = 0. CO's checked range has villain_range_capped considerations."
  The brief then says "This structure works." — but does not resolve whether
  villain_range_capped = 1 applies here.

A PFA who checked the flop does NOT have a capped range in the standard sense.
villain_range_capped = 1 should apply only to cold-callers or limp-callers.
Structure A is the cleanest source of villain_range_capped = 1, but the villain
in Structure A must be the COLD-CALLER (CO or BB), not the BTN opener.

FIX REQUIRED: Replace the BP4 action sequence prototype with this unambiguous
version: "CO opens. BTN calls (villain, cold-caller — range capped at ~JJ/TT).
Hero is BB who called. Flop: CO checks, BTN checks → BB acts. But wait: BB is OOP.
For IP hero (BP4 requires is_ip = 1), the correct structure is:
CO opens. Hero (BTN) calls (hero is IP non-PFA). BB calls.
Flop: BB checks, CO checks → hero (BTN) acts. Villain = CO (PFA) OR villain = BB.
If the relevant villain for capped-range purposes is CO (the opener), villain is
NOT capped. If the relevant villain is BB (cold-caller into the CO-open), then
BB's range is assessed — BB defended preflop (not a cold-call, so partial cap).
Cleanest structure: CO opens (villain), hero (BTN) calls (cold-caller, hero is non-PFA
and IP), BB folds. Flop: CO checks → BTN acts. villain = CO. CO is the PFA
(opener), range is not capped. villain_range_capped = 0.

The brief needs to identify a structure where villain is the cold-caller AND
hero is IP AND hero is non-PFA. One valid structure: HJ opens, CO calls (villain,
cold-caller, capped), hero (BTN) calls (non-PFA, IP). Flop: HJ checks, CO checks
→ BTN acts. villain = CO (cold-caller, capped). hero is BTN (IP, non-PFA). This
is the correct BP4 prototype."

The brief's preferred structure does not cleanly deliver villain_range_capped = 1
for the villain. This needs clarification before the builder designs hands.

---

## Check 6: Is villain_air_pct Construction Explained and Plausible?

PASS. Covered under Check 5 above. The construction is explained in detail,
is range-theoretically sound, and the example calculations are plausible.

---

## Check 7: Does Position Distribution Fix the 95% OOP Bias?

PASS.

The brief specifies 55-65% IP (min 55 situations). The sub-pattern arithmetic
confirms 67 IP against 33 OOP (~67%/33%). This corrects the 138/146 OOP
concentration (95%) that blocked Steps 3A, 4B-D, and 5.

---

## Check 8: Does SPR Guidance Prevent the Batch 1 SPR=1.11 Artifact?

PASS.

The brief explicitly identifies and addresses the Batch 1 artifact: "Do NOT use
pot=90 with effective_stack=100 (gives SPR=1.1, which is a 3-bet-pot stack depth,
not SRP)." The correct formula is given (effective_stack = 970, pot = 90, SPR = 10.8
for standard SRP flop). R3 limits any single SPR value to no more than 15% of
situations within +/- 0.15. This is sufficient.

---

## Check 9: BP6 CHECK Counterexamples — Are Failure Modes Specific?

PASS with one observation.

All 7 failure modes (BP6-A through BP6-G) are specific:
- BP6-A: S1 conditions are exact (flush_danger >= 0.60, is_made_hand = 0, draw_outs < 12).
- BP6-B: S2 conditions are exact (hero_range_percentile = 0.62, raw_equity = 0.55).
- BP6-C: S3 is explicit (villain_aggression_count = 2, hero_range_percentile = 0.78).
- BP6-D: Tier 4 board failure is illustrated with two examples.
- BP6-E: villain_air_pct = 0.32 is the specific near-miss value.
- BP6-F: danger_score = 0.42 (above the 0.35 gate) is the specific failure value.
- BP6-G: danger_score = 0.28 is the specific dry-board trap value.

The BP6-G situation design note adds an important requirement: "make sure no other
step fires (e.g., is_preflop_aggressor = 0, is_ip = 0 for OOP trap)." This is
correct — a monster OOP non-PFA with no draws and danger_score < 0.45 should reach
Step 7 cleanly. The brief correctly steers away from allowing Steps 3/4/5/6 to fire
on BP6-G situations. Good.

One observation: BP6-A example 2 contains an in-line correction ("Hero holds 8h-7d
on 9c-8s-6h" then corrects to "Hero holds J-T on 9-8-6: no pair, OESD"). The final
corrected version is correct, but leaving the initial wrong example in the document
risks a builder using the wrong card holding. The brief should remove the uncorrected
first attempt. Not a logic error — just a documentation hygiene issue.

---

## Check 10: BP6-D Open Question — Tier 4 vs S1?

ISSUE 3 — this needs an owner decision.

BP6-D description states: "Very connected or monotone board. Step 3A exits at Tier 4."
The second example is: "Flop is Tc-9d-8c (connected, two-tone, straight_danger = 0.55).
Hero holds PFA overcards (no pair). Step 3A Tier 4. Step 4 sub-conditions: does hero
have a draw? Tc-9d-8c + hero holds Jh-7h: has an OESD (J-T-9-8-7), draw_outs = 8.
But OOP and sub-condition 4A requires draw_outs >= 12. CHECK."

This describes a situation where the hero is OOP with draw_outs = 8 and the
S2 suppressor fires (OOP, hero_range_percentile implied < 0.72). The brief
attributes the CHECK to "Tier 4 board → Step 3A exits" — but the more precise
cause is that S1 fires if straight_danger >= 0.50 AND is_made_hand = 0 AND
draw_outs < 12. With straight_danger = 0.55, is_made_hand = 0, draw_outs = 8,
S1 fires before Step 3A is even evaluated.

This is not wrong — the final label is CHECK either way. But the brief presents
this as a "Step 3A Tier 4" counterexample when it is actually an "S1 wet bluff
suppressor" counterexample. This overlaps with BP6-A.

The design question is: which suppressor/step is this situation demonstrating?
If it is Tier 4 → Step 3A exits, then the situation needs a MADE hand (so S1
does not fire) that hits Tier 4 and is blocked there. For example: hero holds
T-9 on Tc-9d-8c (two pair, hand_category = 10, is_made_hand = 1). Step 3A:
Tier 4 does not fire. Step 5 might fire (IP check needed). OOP → S2 fires.
The correct Tier 4 demonstration requires constructing a situation where S1 does
NOT fire but Step 3A still exits at Tier 4.

OWNER DECISION NEEDED: For BP6-D example 2, should the failure mode illustrate
(a) Tier 4 exit from Step 3A (requires is_made_hand = 1 so S1 does not fire), or
(b) the S1 wet bluff suppressor on a connected board (which it currently is, making
it a duplicate of BP6-A's intent). If (a), the example needs a made hand in the
design. If (b), BP6-D and BP6-A are partially redundant and the allocation should
be consolidated.

---

## Summary of Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | LOW | BP3, sub-condition 4C | board_favour [DEMOTED] label in the tree's feature table creates ambiguity. Add clarifying note. |
| 2 | MEDIUM | BP4, action sequence prototypes | Villain_range_capped = 1 cannot be set for an opener (PFA). Preferred structure delivers a non-capped villain. Needs a corrected prototype. |
| 3 | LOW | BP6-D example 2 | S1 fires before Tier 4 exit is reached. Example conflates two failure modes. Owner must decide which one to demonstrate. |
| - | HYGIENE | BP6-A example 2 | Inline correction leaves a wrong card holding in the text. Remove the uncorrected first attempt. |

---

## What Is Not Disputed

- All six sub-patterns target the correct blocked steps.
- All critical feature thresholds (villain_air_pct, villain_aggression_count,
  high_card_rank, connectivity_score as integer) match the recalibrated tree.
- The position correction plan is sound and the arithmetic is verified.
- The SPR anti-artifact guidance is specific and actionable.
- The diversity framework (R1-R7) is measurable and the reviewer checklist is complete.
- The villain_air_pct construction guidance is range-theoretically correct.
- BP6 failure modes are specific, not generic.

---

## Recommendation

Do not send to the builder until Issue 2 is corrected (BP4 prototype) and the
owner resolves Issue 3 (BP6-D failure mode identity). Issue 1 (board_favour note)
and the hygiene fix can be addressed in the same edit pass. The brief is otherwise
ready and well-specified.

*Written to: review/comms/REVIEW_BET_FACTORY_BRIEF.md*
