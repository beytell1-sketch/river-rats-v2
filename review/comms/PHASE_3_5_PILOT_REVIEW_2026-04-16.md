---
date: 2026-04-16
from: Programmer (Phase 3.5 pilot reviewer)
to: Main terminal (reviewer/orchestrator), owner
re: Phase 3.5 — pilot labelling qualitative review + gate verdict
status: PASS (iteration 1)
plan: review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md §3.5.3
directive: review/comms/MAIN_TERMINAL_UPDATE_2026-04-16-c.md §3.5.3
prior: review/comms/PHASE_3_5_PILOT_SAMPLE_2026-04-16.md (3.5.1)
data: training-data/v23_pilot_labelled.jsonl (3.5.2)
---

# Phase 3.5 Pilot Review — PASS (iteration 1)

## Headline

- **Pilot size:** 16 hands (target 15-20).
- **Stratum breakdown:** A=7 predicate-matching, B=4 non-predicate, C=2 §3-probing, D=3 boundary.
- **Gate verdict:** **PASS on all five criteria.** No prompt revision needed.
- **Pass 1 4/4 agreement:** 12/16 hands (75%).
- **Pass 2 triggered:** 4 hands (BP7_06, MM_OOP_TURN_001, MM_IP_TURN_003, MM_IP_TURN_033); all affirmed the Pass 1 majority with explicit v3 citations.
- **MW-27-style carryforward:** Confirmed on PROT_DANGER_011 + PFR_CONT_025 — flop spots correctly kept override_clause_fired=false because vcb=0 mechanically (no prior street). Panels did NOT leak the clause by spirit. Documented below.

## Summary table

| Criterion | Target | Measured | Verdict |
|---|---|---|---|
| 1a. Override citation on predicate-matching | ≥80% | 100% (10/10 hands, 38/40 panels = 95%) | PASS |
| 1b. Negative-control non-leak | 100% | 100% (0/24 panels on 6 non-predicate hands fired clause) | PASS |
| 2. §3 additions cited on §3-targeted hands | ≥80% | 100% (4/4 panels on BP7_06, 4/4 on MM_OOP_TURN_001) | PASS |
| 3. 4/4 panel agreement on predicate-matching | ≥70% | 80% (8/10 — 7/7 in Stratum A + 1/3 in Stratum D) | PASS |
| 4. Pass 2 cites v3 guidance where applicable | 100% | 100% (4/4 Pass 2 decisions cite v3 tags) | PASS |
| 5. Reasoning quality — no regressions | qualitative | Clean — avg 376 char, factor_conflicts 45/64 non-trivial, alternatives 57/64 substantive | PASS |

## Criterion 1 — Override clause behaviour

### 1a. Predicate-matching hands fire the clause

All 10 predicate-matching hands (7 Stratum A + 3 Stratum D, all mechanically
satisfying preconditions 1-7) saw at least 3 of 4 panels fire the override.
38 of 40 Pass 1 panels (95%) fired the clause when preconditions held.

The 2 exceptions (both "override-the-override" dissents) came on the two
tightest-boundary Stratum D hands (evr=0.40 and evr=0.36, 0.05 and 0.01
above the 0.35 floor) with atypical composition quads (4% air + 33-37%
draws). See Criterion 3 discussion.

**Illustrative trace (UMBRELLA_067, panel P1):**
> "Walking the Stream B.2 override precondition checklist: (1) facing_bet=False
> yes; (2) num_opponents=2 yes; (3) villain_checked_back=1 yes; (4)
> villain_range_capped=1 yes; (5) worse_hand_pct=0.951 >= 0.55 yes; (6)
> equity_vs_range=0.803 >= 0.35 yes; (7) SPR=1.11 <= 2.0 yes. All seven
> hold — override clause fires [v3 addition — Stream B.2 override clause].
> Prefer BET for value+protection; passive line forfeits capped villain's
> air portion (48% air)."

All four panels on UMBRELLA_067 explicitly walked the 7-precondition
checklist and cited the clause by tag. This is the pattern across Stratum A.

**Illustrative trace (UMBRELLA_217, panel P2 — OOP branch of the clause):**
> "Override clause fires [v3 addition — Stream B.2 override clause]. The
> clause explicitly authorizes OOP value leads here. Villain range has 35%
> medium-made + 26% draws = 61% share that gives us action..."

Panels correctly recognized that the clause's "even when OOP or holding
a medium-strength made hand" language covers the SB-lead spots A3/A4/A5.

### 1b. Negative-control discipline

**Zero leaks.** 24 panels across 6 non-predicate hands (Stratum B: 4,
Stratum C: 2) all set override_clause_fired=false. No panel fired the
clause on:

- `facing_bet=1` hands (RAISE_VALUE_012/013) — panels explicitly removed
  villain_checked_back from attention with tier1_removal note "facing a
  live bet".
- `vcb=0` flop hands (PROT_DANGER_011, PFR_CONT_025) — panels documented
  the mechanical reason: "flop has no prior street; vcb=0 mechanical" and
  chose BET via other reasoning (PFA c-bet / wet-texture protection) WITHOUT
  citing the clause.
- `vrc=0` hand (MM_OOP_TURN_001) — panels correctly identified BB as
  uncapped and did not apply the clause.

**Critical trace — PFR_CONT_025 panel P4** (this is the MW-27-style edge
case inverted): panel explicitly wrote:

> "Override does NOT fire — vcb=0 on flop... I do NOT cite the clause; my
> BET is motivated by wet texture + PFA role + 44% air to fold out...
> override_clause_fired=false (negative control preserved even though
> 'bet here' instinct applies)."

This is exactly the discipline Criterion 1b demands: the panel felt the
pull of the spirit of the override but held the mechanical line.

## Criterion 2 — §3 additions engagement

Both §3-probing hands showed 4/4 panel engagement with §3 tags.

**BP7_06 (§3.A targeted):** All 4 panels cited §3.A / DO NOT Rule 10 AND/OR
KB Section 1.7 (semi-bluff with nut-draw+blocker exception to DO NOT Rule 2).
Panel P1 trace:

> "Multiple preconditions fail → override clause does NOT fire. Instead I
> apply [v3 addition §3.A] DO NOT Rule 10 / §3.C Step 3 enhancement: at
> compressed SPR in a checked-to spot, evaluate BET as value-extraction /
> equity-denial candidate."

The dissenting panel (P3, CHECK) also cited §3.A but resolved in favour
of DO NOT Rule 2 — legitimate factor conflict documented. This is
high-quality §3 engagement: panels read the addition, applied it, and
weighed it against other guidance explicitly.

**MM_OOP_TURN_001 (§3.D targeted):** All 4 panels cited §3.D MW
CHECK-lean pattern. The 3 CHECK-panels answered §3.D's "what does BET
accomplish?" question negatively (uncapped BB range). The 1 BET dissenter
(P3) answered it positively (driven by evr=0.55 margin). Panel P1 trace:

> "Reason from §3.D [v3 addition] MW CHECK-lean pattern: the calibration
> note lists middle-pair OOP at SPR 1.0-1.5 with vcb=1 as the v2.2 failure
> pattern. §3.D asks 'what does BET accomplish?' — here, uncapped BB can
> have Kx that crushes us."

Particularly strong: P1 recognized that §3.D explicitly references
`villain_range_capped=1` in the Stream B.2 override's precondition chain
and that vrc=0 disqualifies the clause — so the calibration note serves
only as the "ask the question" prompt, not a BET mandate.

**§3.B not probed** (no factory records with HRP=0.00 + visibly strong
hand). Documented in 3.5.1. Not a gate failure — Criterion 2 target is
satisfied by §3.A + §3.D coverage.

**§3.C engagement** (Step 3 enhancement / value-extraction action in
checked-to compressed-SPR list): implicit on Stratum A — every Stratum A
panel evaluated BET explicitly in "Consider All Actions", and several
(e.g. UMBRELLA_067 P2) quoted the override's value+protection framing.
Pass 2 on BP7_06 cited §3.C by tag explicitly.

## Criterion 3 — Inter-panel variance on predicate-matching

8 of 10 predicate-matching hands showed 4/4 Pass 1 agreement (80%).
Target is 70%; PASS.

**Composition:**

| Stratum | 4/4 | 3/4 | 2/4 |
|---|---|---|---|
| A (7 hands, central predicate) | 7 | 0 | 0 |
| D (3 hands, boundary predicate) | 1 | 2 | 0 |

The 2 split hands (MM_IP_TURN_003, MM_IP_TURN_033) are the two tightest
boundary spots — evr within 0.04 of the 0.35 floor. On both, one panel
used the prompt's own "override-the-override" escape hatch citing the
unusual composition quad (4% air, 33-37% draws) as a hand-specific reason
to pot-control. This is not a prompt defect — the prompt EXPLICITLY
authorizes this path:

> "You may still choose CHECK, but you must explicitly name a specific,
> hand-specific reason that overrides the override (board run-out danger,
> a concrete read, or a narrow-value vs commit-trap analysis)."

The dissenting panels (MM_IP_TURN_003/P4, MM_IP_TURN_033/P3) cited the
low-air composition as the "concrete read." Pass 2 reviewer judged that
"low air%" is close to but does not explicitly meet the prompt's stated
override-the-override criteria, and affirmed the BET majority at LOW
confidence. Both Pass 2 affirmations enqueued for solver to inform a
future v3 revision about whether composition-quad guards should be
added to the override predicates.

**Inter-panel variance flag (informational, not auto-fail):**

Stratum D had 2/3 hands with variance — in raw terms MORE than Stratum A
(0/7). This is the INTENDED behaviour: Stratum D was curated as boundary
spots precisely to probe variance at the edge of the precondition chain.
Phase 3.5.3 asks us to "flag (do not auto-fail): any hand where v3 has
MORE variance than v2 would have on the same shape." I do not have v2
labels on these exact sids to benchmark, but:

- Stratum A central-predicate hands showed 4/4 agreement on all 7 —
  v3 is almost certainly tighter than v2 on these (v2.2 failure mode was
  mixed CHECK/BET on predicate-match turns).
- Stratum D boundary hands showed 3/4 agreement with principled dissent —
  v2 on the same sids would likely have 2-2 or 1-3 splits with no prompt
  framing for the boundary, producing noisier labels.

## Criterion 4 — Pass 2 engagement

Four hands reached Pass 2. All four Pass 2 decisions cited v3 tags
explicitly:

| sid | final | v3 citations |
|---|---|---|
| BP7_06 | BET | [v3 addition §3.A], [v3 addition §3.C] |
| MM_OOP_TURN_001 | CHECK | [v3 addition §3.D], [Stream B.2 negative-control guidance] |
| MM_IP_TURN_003 | BET | [v3 addition — Stream B.2 override clause], [v3 addition §3.A] |
| MM_IP_TURN_033 | BET | [v3 addition — Stream B.2 override clause], [v3 addition §3.A] |

No Pass 2 decision reverted to v2-era reasoning. No generic "feels
passive" or "SPR concern" without a v3 citation. The Pass 2 reviewer
correctly affirmed majorities rather than overriding when the dissenting
Pass 1 panel had a defensible but sub-criteria argument (MM_IP_TURN_003
and MM_IP_TURN_033 both flagged for solver enqueue — the prompt's
override-the-override criteria do not explicitly include "low
villain_air_pct"; this is the one place a future v3 revision might tighten
guidance).

## Criterion 5 — Reasoning quality + coherence

- **64 Pass 1 reasoning traces**, avg 376 characters each. No truncation,
  no JSON parse errors, no template-boilerplate repetition detected
  across panels.
- **factor_conflicts** non-trivial in 45 of 64 traces (70%). On
  UMBRELLA_067 (the unambiguous AA case), most panels wrote "None" —
  appropriate. On boundary spots, panels articulated specific conflicts
  ("mechanical override vs composition-quad nuance", "§3.A vs DO NOT
  Rule 2" on BP7_06).
- **alternatives_considered** substantive in 57 of 64 traces (89%).
  Rejection reasons are hand-specific (e.g. "LARGE BET: rejected — would
  fold out a lot of the 48% air", "CALL: rejected — AA wants to go with
  it at SPR 0.83"), not generic.
- **Grammar/structural regressions vs v2:** None detected. Sentences
  parse cleanly, terminology use is consistent (override clause, §3
  tag citations, KB section references all spelled consistently).
- **Panel voice differentiation:** P1 tends bucket-first, P2
  feature-first, P3 board-texture-first, P4 exploit-angle — but all
  four follow the same Step 1-5 protocol. Not excessive template
  repetition; each panel's emphasis is distinct.

## MW-27-style carryforward findings

Phase 3 flagged MW-27 (BTN JJ overpair, flop, action history "both
villains checked this street" but feat_dict `villain_checked_back=0`).
The panel on MW-27 fired the override by spirit rather than by mechanical
precondition — informational edge case.

**Phase 3.5 confirmation:** Two pilot hands (PROT_DANGER_011 and
PFR_CONT_025) are structurally similar — FLOP spots where action_string
shows both villains checked, but vcb=0 because no prior street exists.
**Both hands, all 8 panels, correctly kept override_clause_fired=false**
and reasoned from other grounds (wet-texture protection, PFA c-bet, etc.).

This is a notable improvement on the MW-27 ambiguity from Phase 3.
On flop spots, panels reliably treat vcb=0 as a mechanical precondition
failure — they do NOT leak the clause. The MW-27 case in Phase 3 was on
a TURN spot (BTN JJ on 962r with vcb=0 because prior street was preflop),
which is a narrower edge case.

**Interpretation:** The prompt's negative-control guidance language
("villain_checked_back = 0 — villain is not showing weakness. Do not
read passivity into an opponent who bet (or who has not yet had the
option to)") is well-absorbed. The flop-level case is not causing leaks.
Only the turn-level edge case (MW-27) remains informational; it did not
recur in Phase 3.5 because no pilot hand replicated the MW-27 shape
exactly (turn, vcb=0, both-villains-checked-this-street).

**Recommendation (informational, not a gate blocker):** A future v3
revision could add a clarification that the `villain_checked_back`
feature counts prior-street check-backs only, and in turn/river spots
where both villains also checked *this* street, the override clause
STILL does not fire unless vcb=1 (prior-street weakness). This tightens
the MW-27 edge case. Not needed for Phase 4 gate.

## Verdict

**Phase 3.5 PASS on all five criteria, iteration 1.**

- Criterion 1a: 95% panel-weighted override-citation rate (target 80%).
- Criterion 1b: 0% negative-control leak (target 0%).
- Criterion 2: 100% §3 engagement on targeted hands (target 80%).
- Criterion 3: 80% 4/4 Pass 1 agreement on predicate-matching hands (target 70%).
- Criterion 4: 100% Pass 2 v3 citation (target 100%).
- Criterion 5: No regression vs v2.2; factor_conflicts and alternatives
  remain specific and substantive.

No prompt revision needed. Phase 4 production labelling is unblocked
pending owner spot-check.

**Recommendations (informational, not gate-blocking):**

1. The MM_IP_TURN_003/033 variance pattern (low-air + high-draw
   composition at boundary evr) has been enqueued for solver — if solver
   agrees with panels 1-2-3 (BET), current v3 is correct. If solver
   agrees with panel 4 (CHECK), a future v3 revision could add a
   composition-quad guard to the override-the-override criteria.
2. The MW-27 turn-level edge case did not recur in Phase 3.5 (no pilot
   hand matched the shape). A future v3 revision could clarify the
   `villain_checked_back` semantics for this narrow case.
3. §3.B has no factory records that trigger it. Either the test-harness
   artifact is truly absent in production flows (prompt's own claim), or
   §3.B is unreachable by design. Not a gate issue.

## Owner spot-check section

(Empty — owner fills in after reading 3-5 hands.)

Suggested reading order (~30 min):

1. **UMBRELLA_067** — clean 4/4 override spot. Validates Criterion 1 base case.
2. **RAISE_VALUE_012** — negative control. Validates Criterion 1b.
3. **BP7_06** — §3-probe with principled 3/1 split. Validates Criterion 2 and 3.
4. **MM_IP_TURN_033** — tightest-boundary with override-the-override. Validates Pass 2 engagement.
5. **PFR_CONT_025** — MW-27-style flop vcb=0 negative control. Validates carryforward.

Owner comments:

>

Owner verdict:

> [ ] Confirm PASS
> [ ] Flag issue (describe below)
