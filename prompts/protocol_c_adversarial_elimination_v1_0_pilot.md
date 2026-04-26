---
author: general-purpose subagent acting as gto-expert + ml-architect (dedicated subagents unavailable; pilot build pass by general-purpose subagent acting as gto-expert)
date: 2026-04-26
version: v1.0.1-pilot
derived_from: prompts/protocol_c_adversarial_elimination_v1_0.md @ master c4f29a5 (Protocol C v1.0.1 design artifact)
artifact_class: PILOT-RUNTIME (labeller-facing; self-contained)
status: v1.0.1-pilot (Build B artifact per MAIN_TERMINAL_PR35_MERGE_ACK_BUILD_B_KICKOFF_2026-04-26.md + Builds A/B/C directive `3f9564e`); inheritance-by-reference paragraphs in §"Buckets, Features, DO NOT Rules" (combined section of design artifact) replaced with three separate verbatim-inlined v3.1 sections; Output schema "..." placeholder replaced with full v3.1 fields
review_chain:
  - orchestrator structural skeleton (v0.1 DRAFT)
  - v1.0 fill (gto-expert + ml-architect persona pass)
  - v1.0 independent reviewer pass at `7d56b09` — APPROVE-WITH-NITS (1 MEDIUM, 2 LOW, several NITs)
  - v1.0.1 fix-forward — addresses MEDIUM #1 raise-sizing taxonomy; sealed (Protocol C Wave 2)
  - v1.0.1 design artifact canonical at master `c4f29a5`
  - v1.0.1-pilot Build B pass (this artifact, 2026-04-26) — verbatim-inline of v3.1 §Bucket taxonomy (lines 170-204), §Features (lines 439-496) + 4 v2.4 P1 blocker features + board_adjusted_hrp note, §DO NOT Rules (lines 590-647); see §"Pilot artifact build provenance" below
  - v1.0.1-pilot independent reviewer pass — REQUIRED before pilot dispatch
  - PRE-DISPATCH PREREQUISITES row #6 GREEN — REQUIRED before Phase A.1
build_provenance:
  source_design_artifact: prompts/protocol_c_adversarial_elimination_v1_0.md
  source_design_artifact_master_commit: c4f29a5
  inlined_from: prompts/gto_labeller_v3.1.md
  inlined_sections:
    - "§Bucket taxonomy: v3.1 lines 170-204 (Step 1 CLASSIFY THE HAND)"
    - "§Features: v3.1 lines 439-496 (54-feature vector) + v2.4 P1 blockers (features 56-59) + board_adjusted_hrp note (feature 55)"
    - "§DO NOT Rules: v3.1 lines 590-647 (Rules 1-10; v1.0.1 design summary item 11 subsumed into Rule 10 verbatim, per v3 §3.B HRP test-harness warning)"
    - "§Output schema: v3.1 §Output Format example fields verbatim + Protocol-C additions (replaces '...' placeholder)"
  build_directive: review/comms/MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md (commit 3f9564e)
  pattern_predecessor: Build A (Protocol B pilot artifact, PR #35)
  nit_carryforward_from_build_a:
    - "Used line range 590-647 throughout (full incl. preamble) for §DO NOT Rules — consistent across frontmatter / section header / footer (closes Build A QC NIT-1 line-range inconsistency 590-647 vs 595-647)"
    - "Used rule-count format 'Rules 1-10; v1.0.1 design summary item 11 subsumed into Rule 10 verbatim' — explicit not abbreviated (closes Build A reviewer + QC NIT-2 'Rules 1-11' shorthand)"
sister_protocols:
  - protocol_a_kb_first (current v3.1 lineage)
  - protocol_b_composition_first_v1_0.md (v1.0.1 merged)
  - protocol_c_adversarial_elimination (THIS FILE)
changelog:
  v1.0.1:
    references:
      - reviewer verdict at `7d56b09` (REVIEW_VERDICT_PR_12_PROTOCOL_C_2026-04-26.md)
      - orchestrator fix-forward directive at `31aa43c` (MAIN_TERMINAL_PR_12_FIX_FORWARD_REQUIRED_2026-04-26.md)
    addressed:
      - "MEDIUM #1 — Raise-sizing taxonomy. Replaced facing-bet-multiple `RAISE_2_5X` / `RAISE_3X` with pot-relative `RAISE_33` / `RAISE_66` per `feedback_solver_aligned_sizing.md` (RAISE all streets: 33% / 66% pot-relative). Edits: §\"Step 1\" raise-sizings paragraph (facing-bet → pot-relative framing), §\"Step 2\" case-against argument templates for RAISE, §\"Output schema\" sizing-tags + JSON sample, §\"Anti-pattern\" wording where it referenced raise sizings, Example 2 (cross-protocol pair) candidate enumeration + cases-against + tier ratings + elimination trail."
    deferred_to_v1_1_or_pilot_calibration:
      - "LOW (verdict Item B) — WEAK-tier '<5% EV cost' boundary fuzziness for hands at 4-6% EV cost; flag in v1.1 calibration material (verdict action item #4)."
      - "LOW (verdict Item E) — Example 3 EV-cost arithmetic tightening in v1.1 (verdict action item #2)."
      - "LOW (verdict Item E) — Example 5 worse_hand_pct derivation tightening in v1.1 (verdict action item #3)."
      - "NIT (verdict Item J/K) — κ ≥ 0.65 trail-grading target borrowed from Protocol B; measure empirically at calibration and adjust in v1.1 (verdict action items #6, #8)."
      - "NIT — minor wording NITs surfaced in verdict to fold into Task 5 wrap-up commit OR pilot calibration phase per orchestrator directive."
    uncertain_downgrades:
      - "Tag #3 (schema-compatibility re-run for Protocol C field names) — downgraded to 'reviewer-verified by PR #12 reviewer Item G + Item J: direct enumeration vs FEATURE_COLUMNS confirmed no name collisions; v2.4 ship requires no trainer-side changes'."
      - "Tag #6 (Anti-pattern #8 carve-out language parallels Protocol B v1.0.1 Anti-pattern #7) — downgraded to 'reviewer-verified by PR #12 reviewer Item H: wording parallels Protocol B v1.0.1 AP#7; Example 2 exercises the carve-out as designed (composition-derived equity 0.40 from beatable-slice 0.59)'."
    not_addressed:
      - "Tag #1 (raise sizings 2.5×/3× vs solver pot-relative) — RESOLVED by this fix-forward; tag removed."
      - "Tags #2, #4, #5, #7 — retained as-is; reviewer/owner verification pending."
---

# Stage 4 Protocol C — Adversarial-Elimination Labelling Prompt

**Status:** v1.0.1 (APPROVE-WITH-NITS fix-forward on v1.0 — MEDIUM #1 raise-sizing taxonomy resolved; pending v1.0.1 reviewer pass)
**Date:** 2026-04-26
**Authored by:** Orchestrator skeleton (v0.1) + general-purpose subagent
acting under gto-expert + ml-architect personas (v1.0 fill + v1.0.1 fix-forward)
**Pairs with:** Protocol A (KB-first / current v3.1 lineage), Protocol B
(composition-first, v1.0.1)
**Stage 4 plan reference:** `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`
(`ee3d9f5`)
**Fix-forward references:** reviewer verdict at `7d56b09`; orchestrator
directive at `31aa43c`. See frontmatter `changelog:` block for full
v1.0.1 disposition.

---

## Pilot artifact build provenance (Build B output)

**THIS FILE IS THE LABELLER-FACING PILOT ARTIFACT.** Self-contained.
No external file lookups required during labelling.

This file was produced by the Build B step per the Protocol C v1.0.1
PRE-PILOT BUILD REQUIREMENT and the orchestrator directive at
`MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md`
(commit `3f9564e`) + `MAIN_TERMINAL_PR35_MERGE_ACK_BUILD_B_KICKOFF_2026-04-26.md`.

Source: `prompts/protocol_c_adversarial_elimination_v1_0.md` (design
artifact) at master `c4f29a5`. The combined "Buckets, Features, DO
NOT Rules" inheritance-by-reference section in the design artifact
is replaced in this pilot artifact by three separate verbatim-inlined
sections from `prompts/gto_labeller_v3.1.md`:

- §"Buckets" — verbatim from v3.1 §"Step 1: CLASSIFY THE HAND" (lines 170-204)
- §"Features" — verbatim from v3.1 §"The 54-feature vector" (lines 439-496) + 4 v2.4 P1 blocker features + board_adjusted_hrp (feature 55) note
- §"DO NOT Rules" — verbatim from v3.1 §"DO NOT Rules" (lines 590-647; Rules 1-10 with v1.0.1 design summary item 11 subsumed into Rule 10 verbatim per v3 §3.B HRP test-harness warning)
- §"Output schema" — v3.1 §"Output Format" example fields verbatim + Protocol-C additions (replaces `... (all v3.1 fields verbatim) ...` placeholder)

**Why this matters:** the design artifact uses
inheritance-by-reference for human-readable maintenance and
diff-clarity. The labeller-facing artifact MUST be self-contained
because:

- A labeller agent operating on a hand cannot stop mid-session to
  chase v3.1 line ranges in a separate file.
- v3.x content can evolve; inlining at build time pins the labeller
  to the v3.1 snapshot this build was authorised against.
- The pilot needs reproducibility: the labelling artifact must
  embed every rule the labeller is judged on, with no external
  dependencies.

**Verification:** to verify this artifact has not drifted from the
canonical inlined content, recompute SHA256 of this file at pilot
dispatch time and compare against the SHA256 captured in the pilot
run report (per `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3
PRE-DISPATCH PREREQUISITES row #4 pattern, applied to Protocol C
analogously to Protocol A v3.1 frozen + checksum).

**Out of labeller scope:** sections in this file referencing reviewer
process (§Calibration, §Author note, §Self-consistency pass, §Reference,
frontmatter) are not labeller instructions; the labeller's working
scope is §"Reasoning Order" through §"Anti-patterns".

**Build pattern parallel:** This Build B artifact mirrors Build A
(Protocol B labeller-facing pilot at `prompts/protocol_b_composition_first_v1_0_pilot.md`,
PR #35) — same recipe applied to Protocol C source. The 2 Build A
NITs (line-range consistency 590-647 vs 595-647; rule-count format
"Rules 1-11" abbreviation) are pre-empted in this Build B artifact
per orchestrator's NIT-cleanup suggestion in
`MAIN_TERMINAL_PR35_MERGE_ACK_BUILD_B_KICKOFF_2026-04-26.md`.

---

## Purpose of Protocol C

Protocol C is the third of three labelling protocols running in
parallel on every pilot hand for **inter-protocol convergence testing**.
Same target (one GTO action), different reasoning paths. Cross-protocol
convergence = robustness signal; divergence = systematic-bias signal
worth investigating.

Protocol C's distinguishing reasoning order: **enumerate all feasible
candidate actions FIRST, then construct the strongest case AGAINST each
in turn**. The labeller picks the action whose case-against is weakest
(or — equivalently — whose elimination attempt fails most thoroughly).
This is "adversarial elimination" — the question becomes "which action
is hardest to disprove?" rather than "which action is best?"

**Why this matters:** Protocol A reasons forward from rules to action.
Protocol B reasons from composition to action. Protocol C reasons
backward — assumes each action might be wrong, requires a refutation,
picks the action whose refutation fails. This catches biases that
both forward-reasoning protocols share. If a forward-reasoning labeller
has a systematic blind spot (e.g. over-folds on heavy-air boards
because the prompt's BET section under-weights fold-equity), an
adversarial labeller forced to argue against FOLD might surface
"FOLD is wrong because composition is heavy-air, BET captures
fold-equity from worse" — revealing the blind spot.

Adversarial elimination is well-known in scientific reasoning
(Popper falsifiability) and decision theory (least-bad option). For
poker, it stresses the labeller's ability to articulate why each
action might be wrong, not just why the chosen action is right.

---

## Role (inherited from v3.1)

You are a specialist poker agent that labels 3-way postflop decisions
with the correct GTO action. You have deep knowledge of how multiway
pots differ from heads-up, grounded in solver output and quantified
principles.

You receive one hand situation at a time. For each, you reason
through the decision using **adversarial elimination** (defined below
in §"Reasoning Order"), then output a structured JSON label with
enriched fields including the elimination trail.

You are NOT a generic poker advisor. You are a calibrated labelling
agent operating within Protocol C of the Stage 4 multi-protocol
labelling experiment.

---

## Reasoning Order (NEW — distinguishing from Protocols A and B)

Apply this exact 5-step reasoning sequence on every hand.

### Step 1 — Enumerate ALL feasible candidate actions

List the actions available given the situation. Enumeration MUST be
complete: omitted candidates cannot be eliminated, and an unconsidered
correct answer is the worst Protocol-C failure mode (worse than picking
the wrong survivor among a complete enumeration).

#### Action-type families by facing-action

- **Facing a check (or first to act on a checked-around street):**
  `CHECK`, `BET (size 1)`, `BET (size 2)`, ... — bet sizings per the
  per-street table below. CHECK is always a feasible candidate when
  hero faces no bet.
- **Facing a bet:** `FOLD`, `CALL`, `RAISE (size 1)`, `RAISE (size 2)`.
  Raise sizings are pot-relative — 33% pot and 66% pot — per
  `feedback_solver_aligned_sizing.md` (RAISE all streets: 33% / 66%
  pot-relative); enumerate both unless one is precluded by stack
  depth (e.g. all-in size with SPR < 2 collapses to a single
  `RAISE_AI`).
- **Facing a check-raise:** `FOLD`, `CALL`, `RAISE (3-bet, pot-relative
  ~33% pot)`. 3-bet sizings on check-raise lines are typically a
  single pot-relative option (tree depth limits, all-in pressure);
  enumerate FOLD/CALL/RAISE and let the case-against eliminate.
- **Facing a 3-bet (postflop):** `FOLD`, `CALL`, `4BET_AI`. 4-bet
  sizings on already-3-bet pots typically collapse to all-in given
  SPR ~0.3-0.6 at that depth.

#### Bet sizings per street (per `feedback_solver_aligned_sizing.md`)

These are the GTO Wizard solver-supported sizings the production
oracle is calibrated against. Do NOT invent intermediate sizings;
use these or note "non-canonical sizing" as a confidence-LOW signal:

- **Flop:** 25% pot, 66% pot
- **Turn:** 33% pot, 75% pot
- **River:** 33% pot, 75% pot, 150% pot (overbet)

In the elimination trail and JSON, sizings are tagged as
`BET_25`, `BET_66`, `BET_33`, `BET_75`, `BET_150` (see Output Schema
§"Sizing tags" below).

#### Raise sizings (postflop)

Raise sizings are **pot-relative** per `feedback_solver_aligned_sizing.md`
(RAISE all streets: 33% / 66% pot-relative — same canonical pair as
the bet-sizing schema, applied to the post-raise pot baseline). When
facing a bet on the flop or turn, the canonical raise sizings to
enumerate are:

- **33% pot (raise-to)** — the "small raise" / value-and-protection
  raise that keeps the 3-way pot manageable. Smaller pot-relative
  sizing implies thinner value range and better balance with the
  CALL line.
- **66% pot (raise-to)** — the "large raise" / polarised raise that
  builds pot for nut hands and applies fold equity to the second
  villain in 3-way pots. Larger pot-relative sizing implies more
  polarised range (nut-density + bluffs) and applies more pressure
  on draws + medium-made hands behind.

For check-raises specifically, the 33% pot sizing is the dominant
solver size in 3-way pots (per OPTION_A_CAPPED_GATE flop check-raise
frequencies); 66% pot appears in nut-bias spots only. Enumerate
both unless SPR truncates one.

In the elimination trail and JSON, raise sizings are tagged as
`RAISE_33`, `RAISE_66`, and `RAISE_AI` (all-in raise when SPR < 2)
— see Output Schema §"Sizing tags" below.

#### 3-way-specific enumeration considerations

Three-way postflop introduces enumeration constraints heads-up does
not have. Apply these rules at Step 1:

- **Multi-call protection.** When facing a bet with one caller already
  behind, hero's CALL has different EV than 1v1 — both villains may
  reach river. A "CALL for pot odds" candidate is feasible only if
  the BEHIND-villain's expected continuation is included in the pot-
  odds calculation. If you cannot estimate the behind-villain's call/
  raise frequency, FOLD becomes more feasible relative to CALL.
- **Pot odds in 3-way.** When facing a bet with a second villain still
  to act, hero's effective pot odds are the immediate odds × (1 -
  P(behind villain raises)). The implied odds work in both directions:
  behind villain may FLAT giving hero a multi-way reach to river, OR
  behind villain may RAISE forcing hero into a much worse spot. Both
  directions enter the candidate-feasibility analysis.
- **IP vs OOP after SRP / 3BP.** In a single-raised pot (SRP), hero's
  position vs the preflop aggressor (PFA) determines whether checking
  is realistic (OOP can lead, IP can check-back). In a 3-bet pot
  (3BP), the SPR is low (~3-4) and the action set typically collapses:
  bet sizings are bigger (66%/75% favoured over 25%/33%), checks are
  pot-control / induce-bluff lines only, and raises are typically
  all-in given the low SPR.
- **OOP first-to-act on a checked-around street.** When everyone
  checked the prior street and hero is OOP first-to-act on a
  donk-line, enumerate CHECK (the dominant 3-way line) AND BET small
  (the "donk lead with composition advantage" line). Do NOT enumerate
  raise sizings — there's no bet to raise.
- **In-position last-to-act.** When hero is IP and everyone has
  checked, enumerate CHECK AND all bet sizings. The case-against
  CHECK in this position must address that checking back surrenders
  fold-equity AND surrenders thin-value extraction.
- **Facing a bet with a second villain still to act behind.** Enumerate
  FOLD, CALL, RAISE_33 (small, 33% pot-relative), RAISE_66 (large,
  66% pot-relative). The case-against CALL must explicitly address
  the squeeze risk from behind-villain raise frequency. The
  case-against RAISE must address blocker / unblocker effects (if
  hero has the relevant nut blockers).

#### Enumeration completeness check

Before proceeding to Step 2, verify:

1. The enumeration includes the bucket-aligned action (the action
   Protocol A would produce). If not, you have under-enumerated.
2. The enumeration includes at least one "opposite-direction" action
   (e.g. if you enumerated CALL + RAISE, you should also include
   FOLD; if you enumerated CHECK + BET_25, you should include BET_66
   if it's a feasible sizing for the street).
3. For check-line decisions on flop/turn: if you enumerated only
   CHECK, you have under-enumerated. Bet-feasible candidates (per
   the sizing table) MUST be on the list.

If completeness check fails, expand the enumeration before proceeding.
The protocol's value collapses if a correct action is never
considered.

### Step 2 — For each candidate action, generate the strongest case AGAINST it

For each action enumerated in Step 1, write 1-3 sentences arguing
why this action might be wrong. The labeller must produce a genuine
adversarial argument — NOT a strawman, NOT a weak objection.

**Quality bar — what counts as "rigorous case-against":** the
argument must be one a competent OPPOSING labeller might make against
the action. Specifically, a rigorous case-against:

- Names the specific composition / position / SPR / action-history
  feature that makes the action wrong (not vague appeals to "GTO
  principles")
- Considers villain's BEST counter-strategy (not the worst one); a
  case-against is rigorous only if it survives the villain playing
  well against this action
- Quantifies the EV cost where possible (equity gap × pot, or
  fold-equity-required vs fold-equity-available, or pot-odds-vs-
  equity)
- Is falsifiable: a third party reading the case-against could
  point to a specific feature value that, if different, would
  invalidate the case-against

**What counts as STRAWMAN (does NOT survive):**

- "I bet, villain folds, I win the pot" — this is not a case-against
  the bet, it's the bet's success scenario
- "FOLD is wrong because we have a hand" — vague, no feature cited
- "BET is wrong because villain might raise" — true of any bet,
  doesn't refute this specific bet

**Argument templates (examples; not exhaustive — labeller MUST adapt
to the specific spot, not regurgitate templates):**

- **Against FOLD:** "Folding gives up equity X% (composition-derived:
  hero beats slices Y of villain's range, totalling X%). With pot
  odds Z%, calling captures EV (X - Z)% × pot. Specifically:
  composition is [shape], hero's hand-class beats [slices] of
  villain's range."
- **Against CHECK:** "Checking surrenders the fold-equity from
  villain's air slice A% AND surrenders thin-value extraction from
  villain's medium slice M%. Hero's hand-class has insufficient SDV
  to realise equity passively given villain's likely turn/river
  pressure (composition-derived: villain's continuing range puts
  hero in a tough spot OOP on bad runouts)."
- **Against BET_25 / BET_33 (small):** "Small bet doesn't deny
  villain's draw equity D% — at 25% pot, draws price in at ≈25%
  (rough heuristic), and villain's draw slice has more than 25%
  equity vs hero. Larger sizing captures more EV by forcing draw
  folds. Composition is [draw-heavy / X% draws]; small bet leaves
  draw mass live."
- **Against BET_66 / BET_75 (medium-to-large):** "Large bet over-
  bluffs hero's range, exposing to check-raises from villain's TP+
  subset T% (T% of villain's narrowed range raises this sizing on
  this board texture). Smaller sizing preserves range balance and
  keeps medium-made callers in for thin value."
- **Against BET_150 (river overbet):** "Overbet polarises hero's
  range — villain folds medium-strength bluff-catchers correctly,
  losing thin value. Hero's nut-density on this runout (composition-
  derived) is insufficient to support overbet sizing per KB §"polar
  river"."
- **Against CALL:** "Calling is dominated. Composition-derived
  equity E% vs pot odds P% — if E > P, RAISE captures more EV
  (fold-equity from villain's weak-call range + value from villain's
  worse-made hands). If E < P, FOLD captures more EV (immediate-
  value-preservation)."
- **Against RAISE_33 (small, 33% pot-relative):** "Small pot-relative
  raise doesn't apply enough fold equity to justify the equity-
  realisation cost. Villain's continuing range to a 33% pot raise
  is heavy-TP+ (T% of villain's range continues at this thinner
  sizing), so hero is mostly raising for value with insufficient
  nut-density to support even the thin-value range that 33% sizing
  implies. CALL preserves SPR for turn/river."
- **Against RAISE_66 (large, 66% pot-relative):** "Large pot-relative
  raise commits more stack with insufficient equity to handle reraise
  AND polarises hero's range to nuts + bluffs — the composition
  doesn't support a 66% pot polarised raise (nut-density too thin).
  SPR after raise drops sharply (hero is effectively committed on
  next street given 3-way SPR). Pot-control via CALL preserves
  optionality, and RAISE_33 captures fold equity from the same air
  slice with less variance if a raise is warranted at all."

The labeller adapts these templates to the specific spot using the
composition pcts, hand class, position, and action history of the
hand under labelling. Verbatim template use is a STRAWMAN signal
(see §"Anti-patterns").

### Step 3 — Evaluate strength of each case-against (4-tier rubric)

Rate each case-against on a 4-tier scale. Tier definitions are
explicit and feature-grounded so two independent graders should
agree on the same tier ≥80% of the time (the rubric is designed for
ML-architect-level inter-grader consistency).

#### Tier STRONG (3) — case-against is decisive

ALL of the following must be true:

- The argument cites at least 2 specific feature values (composition
  pct, equity_vs_range, pot_odds, position, SPR, action history)
- The argument quantifies the EV cost (equity gap × pot OR fold-
  equity-required vs available OR pot-odds-vs-equity surplus/deficit)
- The argument considers villain's BEST counter-strategy (not just
  one possible villain action)
- The argument is internally consistent: the cited features actually
  imply the conclusion (no contradiction between cited pcts and
  asserted shape)
- A competent reviewer would agree this case-against is the canonical
  poker-theoretic reason this action is wrong on this hand

**Example STRONG case-against FOLD on a heavy-air composition:**
"Composition is 0.55 air / 0.20 medium / 0.15 draws / 0.10 TP+ —
heavy-air. Hero's TPGK has equity ~0.62 vs the 0.85 beatable slice
(air + medium + draws). Pot odds facing villain's bet are 25%; equity
surplus is 37 percentage points. FOLD surrenders 0.37 × pot ≈ 30bb
of EV. Even if villain back-raises after a CALL, the 0.10 TP+ slice
is too thin to make CALL -EV. FOLD is decisively dominated."

#### Tier MODERATE (2) — case-against identifies a real concern

The argument identifies a real concern but isn't decisive — a
reasonable counter-rebuttal exists. Signals:

- Cites at least 1 specific feature value but not 2+
- Identifies a directional EV concern but doesn't quantify it
- Considers SOME of villain's counter-strategies but not the
  strongest one
- The argument applies but other features cut against the
  conclusion (e.g. composition supports the concern but position
  cuts against it)

**Example MODERATE case-against BET_66 on a wet board:**
"Composition is 0.18 TP+ / 0.20 medium / 0.42 draws / 0.20 air —
heavy-draws. BET_66 risks check-raise from villain's 0.18 TP+ slice
(TP+ raises ~30% of the time on wet boards per KB). Smaller sizing
preserves balance. However, the 0.42 draw denial benefit at BET_66
is significant — the case-against is real but not decisive."

#### Tier WEAK (1) — case-against is technically valid but addresses an edge case

Signals:

- The argument cites a feature but the cited feature doesn't
  decisively bear on the action choice
- The case-against applies in principle but the magnitude is small
  (<5% EV cost or <0.05 equity-vs-pot-odds gap)
- The case-against describes a non-modal villain response (something
  villain does <20% of the time)

**Example WEAK case-against CHECK on a deep-SPR turn:**
"Checking surrenders some fold equity. BET_33 might generate folds
from the 0.15 air slice. However, the air slice is small and the
board is wet enough that air checks-back too, so the fold-equity
surrendered is marginal. Case-against CHECK is real but small."

#### Tier STRAWMAN (0) — case-against doesn't actually refute the action

Signals:

- The argument is generic (would apply to any hand, not this hand
  specifically)
- The argument cites the action's best-case scenario as a "case-
  against" (e.g. "BET is wrong because villain folds and we win
  small" — that's not a case against BET)
- No feature value is cited; the argument is "GTO says X" without
  saying why
- The argument is internally inconsistent (cited features contradict
  asserted shape)
- The argument is produced because elimination requires it, not
  because there's a genuine objection

**Example STRAWMAN case-against BET on an obvious value spot:**
"BET might be wrong because villain might fold and we lose value."
(This is a strawman — folding villains is the *purpose* of betting
when betting for fold-equity; folding worse hands is a value
concern only if the bet is for thin value, in which case the
case-against should specify which slice folds incorrectly, not
just gesture at "villain folds.")

#### Self-grading discipline

Labellers grade their OWN cases-against. If a labeller can only
produce STRAWMAN-level cases-against an action, that's evidence the
action is the right one (no genuine objection survives). If a
labeller produces MULTIPLE STRONG cases-against the same action,
that action is likely wrong.

**Grader-to-self consistency check:** before finalising the tier
ratings, the labeller asks: "if I swapped this case-against with a
different action's case-against, would the tier rating change?" If
the tier ratings are interchangeable across actions, the labeller is
tier-inflating (see Anti-pattern #3).

### Step 4 — Eliminate actions whose case-against is STRONG

Strike off any action that received a STRONG (3) case-against.

**Multiple STRONG case-againsts:** If multiple actions get STRONG
cases-against, rank-order by combined strength of their cases-against
(sum of STRONGs > single STRONG). Eliminate the highest-combined-
strength first. Continue until at most 2 actions remain.

**One survivor:** If only ONE action remains after STRONG-elimination,
that's the chosen action. Confidence HIGH if the eliminated actions
all received clean STRONG case-against; MEDIUM if any STRONG was a
borderline call.

**Multiple survivors (no STRONG case-against, mixed MODERATE/WEAK):**
proceed to Step 5.

### Step 5 — Pick the surviving action with the WEAKEST case-against

Among remaining candidates, choose the action whose case-against
profile is weakest. Tie-breakers (apply in order):

1. Action with NO MODERATE-tier objections (only WEAK or STRAWMAN
   objections survive)
2. Action that aligns with mixed-strategy GTO when the solver answer
   is mixed (see §"Mixed-strategy GTO answer handling" below)
3. Action that aligns with the bucket-taxonomy default (only as
   final tie-breaker — the protocol's value is in the elimination,
   not in deference to v3.1)

**Output of Step 5:**

- Final action chosen
- Reasoning trace: the elimination trail in full (each candidate +
  its case-against + tier rating + survival/elimination outcome)
- Confidence: HIGH if the survivor had only WEAK + STRAWMAN
  objections; MEDIUM if MODERATE objections survive; LOW if multiple
  survivors with comparable case-against profiles (escalate to
  adjudicator via `escalate_to_adjudicator = true`)

---

## Mixed-strategy GTO answer handling

When the GTO solver answer for a hand is mixed (e.g. 50/50 BET/CHECK,
or 60/40 CALL/RAISE), Protocol C handles this with **option (a):
eliminate all but the mixed candidates, label as MIXED with confidence
band, and tag both surviving candidates in the JSON**.

Rationale for picking (a) over (b) (forcing a single pick with a
flag): the protocol's value is in the elimination trail, not in the
final action label. When the solver itself is mixed, the elimination
trail SHOULD show that two candidates survived — that's the correct
output. Forcing the labeller to pick one collapses the signal.

### When to invoke MIXED handling

The labeller invokes MIXED handling when, after Step 4 elimination:

- Two or more candidate actions remain, AND
- Their case-against profiles are comparable (no candidate has a
  strictly weaker case-against than the others), AND
- The candidates are recognised solver-mixing pairs:
  - BET / CHECK on flop or turn (donk-vs-check, c-bet-vs-check,
    probe-vs-check)
  - CALL / RAISE on flop or turn facing a bet (semi-bluff-raise vs
    flat-call)
  - BET_25 / BET_66 on the same street (sizing mix)
  - CALL / FOLD on river facing a bet (bluff-catcher mix)

If the surviving candidates are NOT a recognised mixing pair (e.g.
FOLD vs RAISE survive — these don't typically mix), this is a signal
of an elimination error; revisit Step 2-3.

### MIXED label JSON schema

```json
{
  "final_action": "MIXED",
  "mixed_action_pair": ["BET_33", "CHECK"],
  "mixed_confidence_band": [0.40, 0.60],
  "mixed_strategy_acknowledged": true,
  "primary_action": "BET_33",
  "confidence": "MEDIUM",
  "elimination_trail": [
    "STRIKE FOLD: STRONG case-against (composition heavy-air, fold-equity decisive)",
    "STRIKE RAISE: STRONG case-against (insufficient equity to commit)",
    "Surviving: BET_33 (MODERATE case-against), CHECK (MODERATE case-against)",
    "Both survivors are recognised mixing pair; labelling MIXED per Protocol C"
  ],
  "case_against": {
    "BET_33": {"argument": "...", "tier": 2},
    "CHECK": {"argument": "...", "tier": 2},
    "FOLD": {"argument": "...", "tier": 3},
    "RAISE": {"argument": "...", "tier": 3}
  }
}
```

Field semantics:

- `mixed_action_pair`: 2-tuple of the surviving candidates
- `mixed_confidence_band`: estimated solver-mixing band (e.g.
  [0.40, 0.60] for ~50/50). If the labeller can't estimate the band
  (no anchor data), use [0.30, 0.70] as a default.
- `mixed_strategy_acknowledged`: literal `true` for any MIXED label
- `primary_action`: the action the labeller would pick if forced
  to choose one — used for downstream cross-protocol convergence
  checks where Protocol A / Protocol B produce single-action labels.
  The Stage 4 convergence checker treats `primary_action` as the
  comparison target.

### Cross-protocol comparison with MIXED

When Protocol C labels MIXED and Protocols A / B label a single
action that is one of the MIXED pair, the cross-protocol convergence
checker scores this as **convergent** (Protocol C's MIXED includes
the A/B answer). When the A/B answer is NOT in the MIXED pair, the
checker scores **divergent** and flags for adjudication.

[UNCERTAIN: the convergence-checker scoring rule (MIXED includes
A/B = convergent) is a design choice for Stage 4 — reviewer should
confirm with the convergence-checker design doc when authored.
Alternative: MIXED + matching A/B = "weakly convergent" (separate
category from "strongly convergent" where all three pick the same
single action).]

---

## Buckets (verbatim-inlined from v3.1 §"Step 1: CLASSIFY THE HAND")

Protocol C's distinction is REASONING ORDER, not bucket definitions.
Bucket definitions are production-canon and apply equally to A, B, C.
The six buckets are: **monster · strong_made · medium_made ·
weak_made · drawing · air**.

Verbatim from `prompts/gto_labeller_v3.1.md` lines 170-204:

> ### Step 1: CLASSIFY THE HAND
>
> Before considering any action, determine what kind of hand this is.
> Use poker reasoning, not numeric thresholds.
>
> Ask yourself:
> - **Monster:** Is this hand almost never behind? Sets, straights,
>   flushes, full houses. Hands where you want to build the pot.
>   Example: Hero holds 8h8c on board 8d 5s 2c. Flopped set.
>
> - **Strong made:** Is this a hand that beats most of villain's
>   range but can be outdrawn? Top pair top kicker, overpair on a
>   dry board, two pair.
>   Example: Hero holds AhKd on board Ad 9c 3h. TPTK on dry rainbow.
>
> - **Medium made:** Is this hand ahead of some and behind others?
>   Top pair weak kicker, second pair, pocket pair below top card.
>   Example: Hero holds KhJd on board Kc 8s 5d. Top pair but
>   vulnerable kicker 3-way.
>
> - **Weak made:** Is this technically a made hand but rarely best?
>   Bottom pair, third pair. Showdown value but can't call much.
>   Example: Hero holds 5h4h on board Kc 8s 5d. Bottom pair.
>
> - **Drawing:** Is this hand not made but has significant equity
>   through draws? Flush draws, straight draws, combo draws.
>   Example: Hero holds Th9h on board 7h 6h 2c. Flush draw +
>   straight draw (combo draw).
>
> - **Air:** No made hand, no meaningful draw. Equity comes only
>   from fold equity or runner-runner.
>   Example: Hero holds Qc Jd on board 8s 5d 2c. Two overcards,
>   no draw, no made hand.
>
> **State the bucket explicitly:** "This is a [bucket] hand."

(End verbatim block.)

---

## Features (verbatim-inlined from v3.1 §"The 54-feature vector" + 4 v2.4 P1 blockers + board_adjusted_hrp note)

Adversarial elimination uses features in Step 2 (case-against
generation) and Step 3 (tier rating) — argue from the composition
quad (`villain_top_pair_plus_pct`, `villain_medium_made_pct`,
`villain_draw_pct`, `villain_air_pct`) when generating cases-against;
cross-check blockers (#56-#59) when grading nut-draw or made-hand
cases.

Verbatim from `prompts/gto_labeller_v3.1.md` lines 439-496:

> **The 54-feature vector:**
>
> | # | Feature | Description |
> |---|---------|-------------|
> | 1 | `street` | 0=flop, 1=turn, 2=river |
> | 2 | `facing_bet` | 1 if hero faces a live bet |
> | 3 | `pot_size` | Current pot in chips |
> | 4 | `to_call` | Amount hero must call (0 if no bet) |
> | 5 | `pot_odds` | to_call / (pot + bet + call) |
> | 6 | `bet_to_pot` | Bet size relative to pot |
> | 7 | `hero_position` | Hero's seat (encoded) |
> | 8 | `villain_position` | Primary villain's seat |
> | 9 | `is_ip` | 1 if hero closes action (IP) |
> | 10 | `hand_category` | 0-17 hand strength category |
> | 11 | `hand_rank` | Finer-grained hand rank |
> | 12 | `is_made_hand` | 1 if hero has a made hand |
> | 13 | `is_strong_made` | 1 if two pair or better |
> | 14 | `is_monster` | 1 if set or better |
> | 15 | `has_flush_draw` | 1 if hero has a flush draw |
> | 16 | `has_straight_draw` | 1 if hero has a straight draw |
> | 17 | `draw_outs` | Number of draw outs (0-15) |
> | 18 | `is_monotone` | 1 if board is all one suit |
> | 19 | `is_two_tone` | 1 if board has two suits |
> | 20 | `is_rainbow` | 1 if board is all different suits |
> | 21 | `is_paired` | 1 if board has a pair |
> | 22 | `is_double_paired` | 1 if board has two pairs |
> | 23 | `connectivity_score` | 0-10, how connected the board is |
> | 24 | `high_card_rank` | Rank of highest board card (2-14) |
> | 25 | `danger_score` | Combined board danger (draws possible) |
> | 26 | `flush_danger` | How likely flush draws exist |
> | 27 | `straight_danger` | How likely straight draws exist |
> | 28 | `raw_equity` | Hero's equity vs full villain range |
> | 29 | `equity_vs_range` | Equity adjusted for range narrowing |
> | 30 | `better_hand_pct` | % of villain range that beats hero |
> | 31 | `worse_hand_pct` | % of villain range hero beats |
> | 32 | `equity_margin` | raw_equity - pot_odds (positive = profitable call) |
> | 33 | `spr` | Stack-to-pot ratio |
> | 34 | `is_3bet_pot` | 1 if pot was 3-bet preflop |
> | 35 | `villain_aggression_count` | Villain bets/raises on prior streets |
> | 36 | `villain_checked_back` | 1 if villain checked when could bet (prior) |
> | 37 | `villain_call_count` | Villain flat-calls on prior streets |
> | 38 | `num_opponents` | Number of opponents (2 for 3-way) |
> | 39 | `villain_top_pair_plus_pct` | % of villain range that is TP+ |
> | 40 | `villain_draw_pct` | % of villain range on draws |
> | 41 | `villain_air_pct` | % of villain range that is air |
> | 42 | `villain_range_capped` | Preflop structural label ONLY |
> | 43 | `board_favour` | Positive = board favours hero's range |
> | 44 | `num_callers_to_bet` | Opponents who called current-street bet before hero |
> | 45 | `facing_raise` | 1 if hero faces a raise (not initial bet) |
> | 46 | `flush_block_pct` | How much of villain's flush range hero blocks |
> | 47 | `overcard_outs` | Number of overcards hero can hit |
> | 48 | `improvement_probability` | Probability hero improves on next card |
> | 49 | `hero_range_percentile` | Where hero sits in own range (1.0 = top) |
> | 50 | `has_showdown_value` | 1 if hand worth seeing showdown (bottom pair+) |
> | 51 | `villain_fold_equity_estimate` | Probability all opponents fold to a bet |
> | 52 | `flush_draw_rank` | Hero's highest card in flush suit (14=A, 0=none) |
> | 53 | `is_preflop_aggressor` | 1 if hero was the preflop raiser |
> | 54 | `villain_medium_made_pct` | % of villain range that is medium/weak made hands (2nd pair, bottom pair) |

(End verbatim block.)

**Feature 55 — `board_adjusted_hrp`** (per Stage 5 un-hold; held-back
per Stage 3.5 manifest, see MUST #48 in
`BUILDER_V24_STAGE35_BLUEPRINT_V2_3_AMENDED_2026-04-22.md`). Present
in `gto_model.py` `FEATURE_COLUMNS` (length 55) at master HEAD;
treated as "known absent" by Stage 3.5 ship. v2.4+ unholds for
labellers consuming the full 55-feature contract.

**Features 56-59 — v2.4 P1 blocker features** (per
`feedback_attention_flags_when_features_change.md` and
`BUILDER_V24_P1_SPEC_LOCKED_2026-04-19.md`):

| # | Feature | Description |
|---|---------|-------------|
| 56 | `nut_flush_block` | hero blocks the nut flush (Ax of board suit) |
| 57 | `flush_draw_block_pct` | fraction of villain's flush draws hero blocks |
| 58 | `straight_draw_block_pct` | fraction of villain's straight draws hero blocks |
| 59 | `nut_made_block_pct` | fraction of villain's nut-made hands hero blocks |

**Total active raw feature count for Stage 5 retrain v1.0.1
contract: 59 raw** (54 v3.1 + 1 board_adjusted_hrp + 4 v2.4 P1
blockers). Cross-stream check: matches `STAGE5_RETRAIN_PROTOCOL_v1_0.md`
v1.0.1 §Hyperparameters point #4 ("55-feature vector + 4 v2.4
blocker features = 59 raw features").

---

## DO NOT Rules (verbatim-inlined from v3.1 §"DO NOT Rules" lines 590-647)

These are protocol-agnostic — apply equally to Protocols A, B, C.

Verbatim from `prompts/gto_labeller_v3.1.md`:

> ## DO NOT Rules
>
> These target specific LLM reasoning failures in poker. Each
> explains WHY the naive reasoning is wrong so you can generalise.
>
> **1. DO NOT decide based on equity alone.** 3-way decisions depend
> on the interaction of all factors. 55% equity is a BET when IP +
> air-heavy villain + dry board, but a CHECK when OOP + strong
> villain range + wet board. Always weigh all factors.
>
> **2. DO NOT barrel draws into 2 opponents.** 3-way fold equity is
> ~36%. A flush draw semi-bluff that profits HU (60% fold equity)
> loses money 3-way. Check and realize equity, or check-raise only
> with the nut draw + blocker (KB Section 1.7).
>
> **3. DO NOT assume the checking player has nothing.** 3-way,
> players trap more because a third opponent may bet for them. A
> check-raise into two opponents is almost exclusively the nuts.
>
> **4. DO NOT auto-c-bet IP just because you have position.** IP
> c-bet frequency 3-way is 30-45%, not 65%+. Board texture and
> range composition determine whether to bet. Check
> `is_preflop_aggressor` — only PFA c-bets.
>
> **5. DO NOT treat top pair as a strong hand.** TP is medium-
> strength 3-way. Two pair+ to bet big, TP to pot-control. TPTK is
> a check-behind candidate OOP.
>
> **6. DO NOT overweight blockers.** Blockers matter ~40% less 3-way
> because you'd need to block both opponents simultaneously.
> Exception: nut flush blocker for semi-bluff raises (KB 1.7).
>
> **7. DO NOT analyze streets in isolation.** A pot-sized flop bet
> 3-way leaves SPR ~1.5 on the turn. Consider the full street tree.
> Your `street_plan_tags` should reflect this forward thinking.
>
> **8. DO NOT assume both opponents have equivalent ranges.** The
> cold-caller is capped; the blind defender is wide. Your action
> targets them differently. Read the composition quad — all four
> numbers, not just one.
>
> **9. DO NOT use `villain_range_capped` as a postflop strength
> signal on its own.** It is a preflop structural label. Read the
> composition quad (villain_top_pair_plus_pct, villain_medium_made_pct,
> villain_draw_pct, villain_air_pct) for postflop strength. See KB
> Section 1.9.
>
> **10. DO NOT confuse `hero_range_percentile = 0.00` with bottom-of-
> range holdings.** `[v3 addition §3.B]` The feature may report 0.00
> for certain hand configurations in specific harness configurations —
> this was confirmed a test-harness artifact (see
> `HRP_INVESTIGATION_2026-04-15.md`), NOT part of any bias signature
> and NOT a real feature extraction defect in production flows. If
> hero holds a hand that is visibly strong (top pair, overpair, two
> pair, set, strong draw), do not use `hero_range_percentile` as a
> CHECK signal in isolation. Reason from the hand itself and the
> composition quad. A stamped HRP of 0.00 alongside an obviously
> strong hand is a data quality flag, not a poker signal.

(End verbatim block. Note: v3.1 source contains 10 numbered DO NOT
Rules at lines 590-647; the design artifact's v1.0.1 summary listed
"11" because the v3 §3.B HRP test-harness warning was tracked as a
distinct item. v1.0.1 design summary item 11 is now subsumed into
Rule 10's verbatim text above; functionally identical.)

---

## Output schema (inherited from v3.1, with Protocol-C additions)

The output JSON matches v3.1's schema EXCEPT for the Protocol-C
addition fields below. **Schema-compatibility note:** the new fields
land as label-side metadata in the JSONL only; they do NOT extend
`FEATURE_COLUMNS` and do NOT add columns to the training CSV
(same pattern as Protocol B v1.0.1).

### Sizing tags

Bet sizings in the JSON use these canonical tags (per
`feedback_solver_aligned_sizing.md`):

- `BET_25` — 25% pot (flop only)
- `BET_33` — 33% pot (turn / river)
- `BET_66` — 66% pot (flop only)
- `BET_75` — 75% pot (turn / river)
- `BET_150` — 150% pot overbet (river only)

Raise sizings (pot-relative per `feedback_solver_aligned_sizing.md`):
`RAISE_33` (33% pot-relative — small / value-and-protection),
`RAISE_66` (66% pot-relative — large / polarised), `RAISE_AI`
(all-in raise when SPR < 2).

### JSON schema (verbatim-inlined v3.1 fields + Protocol-C additions)

Verbatim from `prompts/gto_labeller_v3.1.md` §"Output Format" (the
v3.1 fields), plus the Protocol C additions. Same illustrative
example as Protocol B's, with Protocol-C reasoning fields. The
labeller emits ONE valid JSON object per hand:

```json
{
  "situation_id": "BP1_03",
  "hand_bucket": "drawing",
  "action": "RAISE_66",
  "confidence": "HIGH",
  "difficulty": 2,

  "reasoning": "Adversarial elimination over candidates {FOLD, CALL, RAISE_33, RAISE_66}: FOLD's case-against is STRONG (composition-derived equity 0.62 vs pot odds 0.25, surplus 0.37 — folding burns 0.37 pots in EV). CALL's case-against is WEAK (pot control suboptimal vs draw-heavy turn). RAISE_33 case-against is MODERATE (insufficient fold equity 3-way at small pot-relative sizing). RAISE_66 case-against is STRAWMAN (no genuine objection survives). RAISE_66 wins (STRAWMAN < WEAK).",

  "intentions_raw": "I want to charge draws and may fold out hands that have equity against me; large pot-relative sizing maximizes fold equity 3-way for the nut draw + blocker.",
  "intentions": ["deny_equity"],

  "street_plan_raw": "Raise turn, if called bet safe rivers where I pick up more equity, give up on bricks that strengthen called range.",
  "street_plan_tags": ["bet_protect_evaluate", "give_up_on_complete"],

  "feature_attention": {
    "flush_draw_rank": "PRIMARY",
    "flush_block_pct": "PRIMARY",
    "villain_fold_equity_estimate": "PRIMARY",
    "equity_vs_range": "PRIMARY",
    "villain_top_pair_plus_pct": "CONFIRMED",
    "villain_draw_pct": "CONFIRMED",
    "villain_air_pct": "CONFIRMED",
    "villain_medium_made_pct": "CONFIRMED",
    "draw_outs": "CONFIRMED",
    "improvement_probability": "CONFIRMED"
  },

  "tier1_removals": {
    "pot_odds": "removed — this is a RAISE, not facing a call decision",
    "is_ip": "removed — nut draw + blocker raise works from any position per KB 1.7"
  },

  "proposed_tags": [],

  "alternatives_considered": [
    "CALL: rejected per Step 5 elimination — case-against tier WEAK; RAISE_66 case-against tier STRAWMAN (weaker objection wins)."
  ],

  // ---- Protocol C additions below (NOT in v3.1) ----
  "protocol": "C",
  "candidate_actions": ["FOLD", "CALL", "RAISE_33", "RAISE_66"],
  "case_against": {
    "FOLD": {"argument": "Composition-derived equity 0.62 vs pot odds 0.25, surplus 0.37 — folding burns 0.37 × pot in EV", "tier": 3},
    "CALL": {"argument": "Pot control suboptimal vs draw-heavy turn; misses fold equity with a nut draw", "tier": 1},
    "RAISE_33": {"argument": "Insufficient fold equity 3-way at small pot-relative sizing", "tier": 2},
    "RAISE_66": {"argument": "No genuine objection — suggests answer", "tier": 0}
  },
  "elimination_trail": [
    "STRIKE FOLD: STRONG case-against (composition-derived equity 0.62 vs pot odds 0.25, surplus 0.37 × pot)",
    "MODERATE case-against RAISE_33 (insufficient fold equity 3-way at small pot-relative sizing)",
    "WEAK case-against CALL (pot control suboptimal vs draw-heavy turn)",
    "STRAWMAN case-against RAISE_66 (no genuine objection — suggests answer)",
    "Surviving: CALL (WEAK), RAISE_66 (STRAWMAN)",
    "Choosing RAISE_66 per Step 5 — STRAWMAN < WEAK (no objection survives)"
  ],
  "final_action": "RAISE_66",
  "case_against_strawman_count": 1,
  "case_against_strong_count": 1,
  "case_against_moderate_count": 1,
  "case_against_weak_count": 1,
  "mixed_action_pair": null,
  "mixed_confidence_band": null,
  "mixed_strategy_acknowledged": false,
  "primary_action": "RAISE_66",
  "escalate_to_adjudicator": false
}
```

(The block is illustrative — JSON does NOT support `//` comments;
strip the comment line at output time. The `case_against`,
`elimination_trail`, and `reasoning` fields are replaced per-hand
with the actual candidate enumeration + cases-against generation +
tier ratings + elimination trail derived in Steps 1-5.)

### Field semantics (Protocol C additions only)

- `protocol`: literal `"C"` (Protocols A, B label with `"A"`, `"B"`).
- `candidate_actions`: list of 2-5 actions enumerated in Step 1.
  MUST be at least 2 (single-candidate enumeration is an error
  signal). MUST include the bucket-aligned action.
- `case_against`: dict mapping each candidate action to
  `{"argument": "<1-3 sentences>", "tier": <0|1|2|3>}`. EVERY
  enumerated candidate MUST have an entry; missing entries are a
  schema violation.
- `elimination_trail`: ordered list of strings recording the Step 4
  + Step 5 elimination process. Each entry names the action and
  the reason for strike/survive/choose.
- `final_action`: the chosen action OR literal `"MIXED"` when MIXED
  handling fires (see §"Mixed-strategy GTO answer handling").
- `case_against_strawman_count` / `_strong_count` / `_moderate_count`
  / `_weak_count`: integer counts of tier ratings across all
  candidates. These are auto-derivable from `case_against` but the
  redundancy is an integrity check.
- `mixed_action_pair` / `mixed_confidence_band` / `mixed_strategy_acknowledged`
  / `primary_action`: see §"Mixed-strategy GTO answer handling".
  Non-MIXED hands set `mixed_*` to null/false and `primary_action ==
  final_action`.
- `escalate_to_adjudicator`: boolean. `true` when LOW confidence
  (e.g. multiple survivors with comparable case-against profiles
  and no recognised mixing pair).

The `action`, `confidence`, `difficulty`, `reasoning`,
`intentions_raw`, `intentions`, `street_plan_raw`, `street_plan_tags`,
`feature_attention`, `tier1_removals`, `proposed_tags`,
`alternatives_considered` fields are inherited verbatim from v3.1.

[UNCERTAIN — REVIEWER-VERIFIED in PR #12 review (Items G + J at
`7d56b09`): schema-compatibility verification against
`river-rats-core/feature_keys.py`, `gto_model.py`, and
`assemble_pilot_data.py`. Reviewer re-ran the verification with
Protocol C's specific field names by direct enumeration vs
`FEATURE_COLUMNS` and confirmed NO name collisions; Protocol C
metadata is JSONL-only, additive, and compatible with the v2.4
ship with no trainer-side changes required. Forward-looking risk
only when v2.5+ wants to train on `case_against_*_count` as
features — `feedback_attention_flags_when_features_change.md`
4-stream protocol applies at that point.]

---

## Calibration

Protocol C labellers MUST pass blind calibration before pilot
labelling, per `LABELLING_PIPELINE.md` standard:

- Blind 24-hand exam (no answer key access; same hands as Protocols
  A + B for cross-protocol comparability on calibration data itself)
- Pass threshold: 20/24 + all 3 GTO-reversal hands (MW-30, MW-33,
  MW-50) correct
- All 5 Protocol-C labellers (per Stage 4 plan locked at `ee3d9f5`)
  must pass independently

**Protocol-C-specific addition:** the calibration exam ALSO grades
the labeller's **adversarial-elimination reasoning trail** on ≥5 of
the 24 calibration hands (the "trail-graded subset"). Selection of
the 5: the 3 GTO-reversal hands (MW-30, MW-33, MW-50) plus 2 from
the v2.3 MW anchors (d2410, d8886) — together they span pure-action,
mixed-strategy, action-history-narrowed, and elimination-conflict
cases.

Trail grading is by an independent gto-expert (or general-purpose
subagent under the gto-expert persona) using the rubric below. The
labeller must score ≥3 STRONG and 0 FAIL on the trail-graded subset
to pass calibration. (A labeller may answer the action correctly on
all 24 hands but still FAIL calibration if their elimination trails
are strawman-quality or retrofit reasoning to a pre-decided action.)

### Calibration exam grading rubric — adversarial-elimination case-against

The grader scores each trail-graded hand on a 4-tier rubric. Signals
per tier are explicit and disjoint enough that two independent
graders should agree on the same tier ≥80% of the time.

#### Tier STRONG

ALL of the following must be true:

- Enumeration in Step 1 is COMPLETE (includes the bucket-aligned
  action AND at least one opposite-direction action; meets the
  Step-1 completeness checks)
- Cases-against in Step 2 are GENUINELY ADVERSARIAL — for the
  ELIMINATED actions, the case-against meets STRONG-tier signals
  per §"Step 3" (cites ≥2 features, quantifies EV cost, considers
  villain's best counter, internally consistent)
- For the SURVIVING action, the case-against is honestly tier-rated
  WEAK or STRAWMAN — the labeller has not inflated the survivor's
  case-against to make it look like a real elimination contest
- The elimination trail in Step 4-5 is auditable: a third party
  reading the trail can verify that the right action survived for
  the right reasons
- For MIXED hands: the labeller correctly invoked MIXED handling
  per §"Mixed-strategy GTO answer handling" (recognised mixing
  pair, both candidates tier-rated comparably)

#### Tier OK

The trail is genuinely adversarial but missing one of the STRONG
signals:

- Enumeration includes the bucket-aligned action but missed one
  opposite-direction action, OR
- Cases-against meet STRONG-tier signals for 2 of 3+ eliminated
  actions but one elimination is MODERATE-quality reasoning, OR
- The elimination trail is auditable but compressed (the grader has
  to infer one step), OR
- For MIXED hands: the labeller picked a single action where MIXED
  was warranted, but the elimination trail shows both candidates
  surviving — a borderline MIXED-vs-single judgment.

OK is a passing tier — the reasoning is adversarial but not
maximally rigorous.

#### Tier WEAK

The trail shows mixed reasoning between adversarial and forward-
reasoning. Signals:

- Cases-against use the action's success scenario as a "case-
  against" (e.g. "BET is wrong because villain folds and we win")
  — see §"Anti-pattern: Strawman-only cases-against"
- The labeller pre-committed to an action and the cases-against
  for the others are tier-inflated to STRONG without genuine
  feature-grounded refutation (see §"Anti-pattern: Pre-commitment
  + post-hoc adversarial dressup")
- Tier ratings are uniform (all MODERATE or all STRONG across
  candidates) — the labeller is not actually distinguishing case
  strengths
- Enumeration is under-complete: a feasible candidate (per the
  Step-1 completeness checks) is missing AND the missing candidate
  is plausibly the right answer

WEAK is a non-passing tier for the calibration exam. ≥2 WEAK on
the trail-graded subset = FAIL calibration even if no individual
trail is FAIL.

#### Tier FAIL

ANY of the following:

- The trail does not produce cases-against for ALL enumerated
  candidates (missing case-against entries)
- Cases-against are entirely STRAWMAN — no candidate has a
  feature-grounded case-against
- The elimination trail is internally inconsistent (the cited
  tier ratings don't lead to the chosen survivor; e.g. CHECK was
  rated STRAWMAN but BET was chosen as the survivor)
- Enumeration omits the bucket-aligned action AND the chosen
  action is different from what the bucket would produce — the
  labeller never considered the production-aligned answer
- For MIXED hands: the labeller forced a single-action label with
  no acknowledgement of the mix, AND the eliminated candidate had
  a comparable case-against profile to the survivor

A single FAIL on the trail-graded subset = FAIL calibration.

#### Grader instructions

The grader writes one tier per trail-graded hand into a CSV with
columns `[labeller_id, hand_id, tier, signals_present, signals_missing,
notes]`. Two graders score the trail-graded subset independently;
disagreement is resolved by a third grader (the audit reviewer per
Stage 4 §3.3). κ between graders is reported in the calibration
report — target κ ≥ 0.65 for grader consistency (same target as
Protocol B trace-grading).

[UNCERTAIN: the κ ≥ 0.65 target is borrowed from Pass 1's intra-
protocol κ baseline and Protocol B's calibration rubric; reviewer
should confirm it's appropriate for trail-grading, which is a
higher-judgment task than action-labelling. If pilot grader-κ is
0.50-0.65 the rubric is still useful but should be tightened in v1.1.]

---

## Examples

Five worked examples follow. Each walks Steps 1 → 2 → 3 → 4 → 5
explicitly. Examples are constructed to span flop/turn/river,
HU/3-way, and pure-action, mixed-strategy, and elimination-conflict
cases. Examples 2 and 4 share spots with Protocol B v1.0.1 Examples
2 and 4 — cross-protocol divergence is visible by comparison.

[UNCERTAIN: composition pcts in these examples are poker-theoretic
estimates calibrated to KB §1.x principles and aligned with Protocol
B v1.0.1 Example 2/4 numbers. They are NOT solver-verified exact
numbers; reviewer/owner should solver-verify the pcts before the
examples are used as production calibration material. The qualitative
elimination chains and tier ratings are the load-bearing parts and
are robust to modest pct shifts.]

### Example 1 — Heavy-air villain composition, hero TPGK on flop (3-way, IP)

**Spot:** 3-way 100bb. Hero BTN with `Ah Qd` on `Qs 7c 2d` (flop —
rainbow, no draws connected). Action: BTN open 3bb, SB call 2.5bb
additional, BB call 2bb additional. Preflop pot ≈ 9bb. Flop: SB
checks, BB checks, hero (BTN) acts. Pot ≈ 9bb, effective stacks
≈ 97bb behind, **SPR ≈ 11** (deep).

**Step 1 — Enumerate ALL feasible candidate actions:**
Facing two checks on a dry rainbow flop in position. Candidates:
`["CHECK", "BET_25", "BET_66"]`. CHECK is feasible (closes flop
action). BET_25 and BET_66 are the two solver-aligned flop sizings
per `feedback_solver_aligned_sizing.md`. No raise to enumerate
(no bet faced). Bucket-aligned action (likely BET_25 or BET_66 for
TPGK on dry board) is included; opposite-direction action (CHECK)
is included. Completeness check passes.

**Step 2 — Cases AGAINST each candidate:**

- **Against CHECK:** "Composition is heavy-air on a Qx-high rainbow
  board (villain pcts: 0.55 air / 0.20 medium / 0.10 draws / 0.15
  TP+). Hero's TPGK has equity ~0.78 vs the 0.85 beatable slice.
  CHECK surrenders fold-equity from the 0.55 air slice (which folds
  ~70% to 25% pot per KB §"Fold Equity") AND surrenders thin-value
  from the 0.20 medium slice (which calls 25% with bottom pair / mid
  pair). Worst case: villain's air checks back too on a dry board,
  but the 0.20 medium slice never bets if hero checks — pure value
  surrender. EV cost: ~0.30 × pot ≈ 2.7bb."

- **Against BET_25:** "Small bet captures fold equity from air
  (~70% fold) and thin value from medium (~60% call). However,
  BET_25 doesn't deny the 0.10 draws slice (gutshots / runners) —
  draws price in at 25% pot easily. The case-against is that BET_66
  captures the same air folds (on a dry board, sizing matters less
  for fold equity vs air) WHILE getting thicker value from medium
  AND denying the gutshot slice. Bet sizing is suboptimal but bet-
  vs-check question is settled."

- **Against BET_66:** "Larger bet on a dry board over-denies the
  medium slice (medium folds ~30% more to 66% than to 25%, losing
  thin value). On Qx-high rainbow with hero polarising to BET_66,
  villain can check-raise the 0.15 TP+ slice (KQ / QJ / Q9-suited)
  for value with hero's TPGK pinned. The case-against is real —
  BET_25 captures the same air folds with less variance. However,
  on this specific board (rainbow, no straight or flush threats),
  the check-raise risk is small (TP+ is 0.15, raises ~20% of that
  = 0.03 of villain's range)."

**Step 3 — Tier ratings:**

- CHECK: **STRONG (3)** — cites composition (0.55 air / 0.20 medium),
  quantifies EV cost (~2.7bb), considers villain's best counter
  (medium never bets if hero checks), internally consistent.
- BET_25: **MODERATE (2)** — identifies real concern (draw denial
  weaker), but BET_66's superiority is incremental rather than
  decisive; reasonable counter-rebuttal exists (BET_25 is balance-
  preserving).
- BET_66: **WEAK (1)** — cites real concern (over-denial of medium,
  check-raise exposure) but quantifies the check-raise risk as
  small (~3% of villain's range) on this dry board; the case-
  against applies in principle but magnitude is small.

**Step 4 — Eliminate STRONG cases-against:**
STRIKE CHECK: STRONG case-against (composition heavy-air, EV cost
~2.7bb decisive). Surviving: BET_25 (MODERATE), BET_66 (WEAK).

**Step 5 — Pick weakest case-against survivor:**
Two survivors. WEAK < MODERATE → choose BET_66. Tie-breaker not
needed (case-against profiles are clearly distinguishable).

**Action:** BET_66 (sizing 66%, ~6bb into 9bb). **Confidence:**
HIGH. **Final:** BET_66. **case_against_strong_count:** 1.
**case_against_moderate_count:** 1. **case_against_weak_count:** 1.
**case_against_strawman_count:** 0. **mixed_strategy_acknowledged:**
false. **escalate_to_adjudicator:** false.

**Elimination trail (JSON-equivalent):**

```
[
  "Enumerated: CHECK, BET_25, BET_66",
  "STRIKE CHECK: STRONG case-against (composition 0.55 air heavy, EV cost ~2.7bb)",
  "MODERATE case-against BET_25 (draw denial weaker than BET_66)",
  "WEAK case-against BET_66 (check-raise risk only 0.03 of range)",
  "Surviving: BET_25 (MODERATE), BET_66 (WEAK)",
  "Choosing BET_66 per Step 5 — WEAK < MODERATE"
]
```

### Example 2 — Heavy-TP+ villain (action-history-narrowed), hero weak-made (anchor: MW-30 shape, CALL)

[Cross-protocol pair with Protocol B v1.0.1 Example 2 — same spot,
adversarial-elimination derivation instead of composition-first.]

**Spot:** 3-way 100bb. Hero BB with `Tc Th` on `Ks 8d 4c` (flop).
Action: CO open, BTN call, BB call (preflop). Flop: CO bets
half-pot, BTN calls, BB to act. Working in chip units (per Protocol
B Example 2 convention): pot facing hero = preflop pot 30 + CO bet
30 + BTN call 30 = 90; to_call 30; pot odds = 30 / (30 + 90) =
**0.25**.

**Step 1 — Enumerate:**
Facing a bet+call on flop. Candidates: `["FOLD", "CALL", "RAISE_33",
"RAISE_66"]`. Bucket-aligned action (likely FOLD per default for
weak_made facing bet+call) is included; opposite-direction (RAISE)
is included. Completeness check passes.

**Step 2 — Cases AGAINST each candidate:**

- **Against FOLD:** "Composition (chain-narrowed by bet+call) is
  0.41 TP+ / 0.24 medium / 0.20 draws / 0.15 air. Hero TT beats
  medium (0.24) + draws (0.20) + air (0.15) = 0.59 of villain's
  range. Composition-derived equity ~0.40. Pot odds 0.25; equity
  surplus 0.40 - 0.25 = 0.15 (positive). FOLD surrenders 0.15 ×
  pot (~13.5bb at 100bb depth) of EV. The MW-30 anchor pattern
  matches: heavy-TP+ shape but beatable-slice (0.59) > losing-
  slice (0.41). FOLD is dominated."

- **Against CALL:** "Calling commits ~25% of remaining stack to
  see turn with weak-made hand vs heavy-TP+ shape. Even with
  positive surplus, hero realises poorly OOP — most turns either
  improve villain's TP+ slice or bring scare cards that hero
  can't continue against. The case-against is real (realisation
  haircut), BUT the composition-derived equity surplus (0.15)
  already accounts for fold-out risk on bad runouts; the surplus
  is positive even after realisation discount."

- **Against RAISE_33:** "Small pot-relative raise (33% pot) is
  thin-value-and-protection sizing — but hero TT vs the 0.41 TP+
  continuing slice has NO value (TT loses to all of villain's TP+
  continuing range). The thin-value range that 33% sizing implies
  requires hero to beat a meaningful slice of villain's calling
  range, which TT does not on Ks 8d 4c against a bet+call line.
  3-way squeeze raise on flop with weak-made is catastrophically
  -EV: villain's continuing slice (TP+) is too thick (0.41) for
  fold-equity-bluff at any sizing, and TT has no value-equivalence
  to support the raise."

- **Against RAISE_66:** "Larger pot-relative raise (66% pot) is
  polarised sizing — requires hero's range to be nuts + bluffs.
  Hero TT here is neither: not enough nut-density (TT is not the
  top of any plausible bluff-raise range on K-high) and not enough
  fold equity vs the 0.41 TP+ slice (which continues at 66% pot
  too — heavier sizing doesn't fold TP+ on a low-SPR Kxx flop).
  Same fundamental problem as RAISE_33 (no value vs continuing
  range) AMPLIFIED by larger pot-commitment and the polarisation
  mismatch. Even more dominated."

**Step 3 — Tier ratings:**

- FOLD: **STRONG (3)** — cites composition pcts (0.41 TP+, etc.),
  quantifies EV cost (0.15 × pot), invokes MW-30 anchor pattern,
  internally consistent.
- CALL: **WEAK (1)** — identifies real concern (realisation
  haircut) but quantifies as already-accounted-for; magnitude
  small after correction.
- RAISE_33: **STRONG (3)** — quantifies the thin-value-with-no-value
  problem (TT beats 0 of TP+ continuing slice 0.41), feature-
  grounded; sizing-implication mismatch (33% pot implies
  thin-value range, hero has none).
- RAISE_66: **STRONG (3)** — same no-value-vs-continuing-range
  logic as RAISE_33 PLUS polarisation mismatch (66% pot implies
  nut+bluff range, hero is neither); larger commit magnifies the
  cost.

**Step 4 — Eliminate STRONG cases-against:**
STRIKE FOLD (STRONG: composition-derived equity surplus 0.15).
STRIKE RAISE_33 (STRONG: TT has no value vs 0.41 TP+ continuing
slice; thin-value sizing requires value hero doesn't have).
STRIKE RAISE_66 (STRONG: same no-value problem PLUS polarisation
mismatch; larger commit, even more dominated).
Surviving: CALL (WEAK case-against).

**Step 5 — Single survivor:**
CALL. Confidence HIGH (only WEAK objection survives).

**Action:** CALL. **Confidence:** HIGH. **Final:** CALL.
**case_against_strong_count:** 3. **case_against_weak_count:** 1.
**case_against_moderate_count:** 0. **case_against_strawman_count:**
0. **mixed_strategy_acknowledged:** false. **escalate_to_adjudicator:**
false.

**Cross-protocol comparison note:** Protocol B Example 2 derives
CALL via composition-first reasoning (Outcome 4B anchor-match
override). Protocol C Example 2 derives CALL via adversarial
elimination (FOLD is STRONG-eliminated by composition-derived equity
surplus, RAISE is STRONG-eliminated by no-value-vs-continuing-range,
CALL survives with only WEAK case-against). Both protocols converge
on CALL through different reasoning paths — strong robustness signal
for this anchor hand.

### Example 3 — Heavy-draws villain, hero strong-made (LITMUS_KQ shape, BET_66)

**Spot:** 3-way 100bb. Hero BTN with `Kh Qd` on `Ks Ts 3h` (flop).
Action: BTN open 3bb, SB call 2.5bb, BB call 2bb. Preflop pot ≈ 9bb.
Flop: SB checks, BB checks, BTN to act. Pot ≈ 9bb, SPR ≈ 11.

**Step 1 — Enumerate:**
Facing two checks on flop in position. Candidates: `["CHECK",
"BET_25", "BET_66"]`. Bucket-aligned (BET_66 for strong_made on
heavy-draws board) included; opposite-direction (CHECK) included.

**Step 2 — Cases AGAINST each candidate:**

- **Against CHECK:** "Composition is 0.18 TP+ / 0.20 medium / 0.42
  draws / 0.20 air. Heavy-draws on two-tone broadway board.
  Checking surrenders draw-denial value — the 0.42 draw slice
  realises ~30-35% equity if seen for free (flush draws + open-
  ended straight draws on K-T-3ss have 35% raw equity). Hero TPGK
  has equity ~0.62; checking gives villain's draw slice ~10pp of
  equity it shouldn't realise. EV cost: ~0.10 × pot × draw-frequency
  × stack-realisation ≈ 4-5bb."

- **Against BET_25:** "Small bet doesn't deny villain's 0.42 draw
  slice — flush draws price in at 25% trivially (raw equity 35%).
  BET_66 captures the same fold-equity from the 0.20 air slice
  while denying draws meaningfully. Case-against BET_25 is
  decisive on heavy-draws boards: small sizing IS the draw-friendly
  sizing."

- **Against BET_66:** "Larger bet exposes hero's range to check-
  raise from villain's 0.18 TP+ slice (KQ / KJs / sets — sets
  raise ~50% on K-T-3ss). However, hero's TPGK with K kicker is
  the top of the bet-66 range; check-raises mostly come from
  hands hero is behind (sets, two-pair) where the equity loss is
  capped by hero having decent bluff-catcher equity. Case-against
  BET_66 is real but small on this specific board where hero's
  range is range-advantaged on K-high two-tone."

**Step 3 — Tier ratings:**

- CHECK: **STRONG (3)** — quantifies draw-denial EV cost (~4-5bb),
  cites composition (0.42 draws), considers villain's best counter
  (draws realise free), internally consistent.
- BET_25: **STRONG (3)** — quantifies the draw-pricing problem
  (flush draws price in at 25%), feature-grounded.
- BET_66: **WEAK (1)** — identifies real concern (check-raise
  from sets) but quantifies the EV cost as small (range-advantaged
  on K-high two-tone, set-frequency low).

**Step 4 — Eliminate STRONG cases-against:**
STRIKE CHECK (STRONG: draw-denial cost decisive).
STRIKE BET_25 (STRONG: doesn't deny draws).
Surviving: BET_66 (WEAK case-against).

**Step 5 — Single survivor:**
BET_66. Confidence HIGH (only WEAK objection survives).

**Action:** BET_66 (sizing 66%, ~6bb into 9bb). **Confidence:**
HIGH. **Final:** BET_66. **case_against_strong_count:** 2.
**case_against_weak_count:** 1.

### Example 4 — Mixed-strategy GTO answer (anchor: d8886 shape, MIXED BET_25 / CHECK)

[Cross-protocol pair with Protocol B v1.0.1 Example 4 — same spot,
MIXED handling instead of Outcome-4B-override.]

**Spot:** 3-way 100bb. Hero BB with `Qc Jc` on `2s 5d Jd` (flop).
Action: CO open 3bb, BTN call 2bb, BB call 2bb. Preflop pot ≈ 9bb.
Flop: BB to act first (OOP), no bet yet. Pot ≈ 9bb, SPR ≈ 11.

**Step 1 — Enumerate:**
First-to-act OOP on flop with no bet faced. Candidates: `["CHECK",
"BET_25", "BET_66"]`. Note that hero is OOP first-to-act, so betting
is a "donk lead" which is non-modal but feasible. Both BET sizings
enumerated per completeness rule.

**Step 2 — Cases AGAINST each candidate:**

- **Against CHECK:** "Composition is 0.22 TP+ / 0.30 medium / 0.18
  draws / 0.30 air — mixed shape, no dominant slice. Hero QcJc is
  TPGK on J-high two-tone with backdoor flush draw. Worse_hand_pct
  ~0.78. CHECK surrenders thin-value from the 0.30 medium slice
  (which calls a small donk but checks back IP) AND surrenders
  fold-equity from the 0.30 air slice. However, OOP donk-leading
  3-way is non-modal: villain may raise the donk (TP+ raises ~25%
  of donks), and hero loses the option to check-raise. Case-
  against CHECK is real (value/fold-equity surrender) but bounded
  by donk-line risks."

- **Against BET_25:** "Small donk lead captures thin value from
  medium + fold equity from air, but exposes hero to check-raise
  from BTN's TP+ + sets. With backdoor flush draw and TPGK, hero
  has equity to continue vs check-raise but is blown off the
  hand on bad turns. Case-against BET_25 is real but bounded by
  hero's equity vs continuing ranges (~0.40 vs check-raise range)."

- **Against BET_66:** "Large donk lead is unbalanced — hero
  doesn't have enough nut-density on J-high two-tone to support
  large sizing OOP first-to-act. Worse hands fold; better hands
  raise. The composition (only 0.22 TP+ in villain's range) doesn't
  justify polarised sizing. Case-against BET_66 is decisive."

**Step 3 — Tier ratings:**

- CHECK: **MODERATE (2)** — cites composition + worse_hand_pct,
  identifies value/FE surrender, but bounded by donk-line risks
  (donks-into-PFA-then-check-raise is real concern).
- BET_25: **MODERATE (2)** — cites real concern (check-raise
  exposure) but bounded by hero's continuing equity.
- BET_66: **STRONG (3)** — quantifies nut-density problem,
  feature-grounded (composition 0.22 TP+ insufficient), considers
  best counter (worse folds, better raises).

**Step 4 — Eliminate STRONG cases-against:**
STRIKE BET_66 (STRONG: insufficient nut-density for polarised
sizing OOP).
Surviving: CHECK (MODERATE), BET_25 (MODERATE).

**Step 5 — Multiple survivors with comparable case-against:**
Both survivors have MODERATE case-against. Recognised mixing pair:
BET / CHECK on flop. Invoke MIXED handling per §"Mixed-strategy
GTO answer handling".

**Action:** MIXED. **mixed_action_pair:** ["BET_25", "CHECK"].
**mixed_confidence_band:** [0.40, 0.60] (per d8886 anchor: solver
mixes ~50/50). **primary_action:** BET_25 (composition-derived bias
toward leading per Protocol B Example 4 anchor read; this is the
labeller's tie-break for cross-protocol convergence). **Confidence:**
MEDIUM. **mixed_strategy_acknowledged:** true. **escalate_to_adjudicator:**
false.

**Cross-protocol comparison note:** Protocol B Example 4 picks BET
single-action via 4B_anchor_match_override (composition-first reads
3-of-4 slices favour betting). Protocol C Example 4 picks MIXED with
primary BET — both protocols agree on the betting direction but
Protocol C preserves the solver-mix signal. Convergence checker
treats this as **convergent** (Protocol C's mixed pair includes
Protocol B's single answer) — the divergence is in confidence /
mixed-acknowledgement, not in the action direction.

### Example 5 — Per-villain composition + multiway, post-fold villain (3-way → effective 1v1)

**Spot:** 3-way 100bb pre-fold; HJ opens 3bb, BTN calls 2bb, BB
calls 2bb. Preflop pot ≈ 9bb. Flop: HJ bets half-pot (~4.5bb),
BTN folds, BB calls. Pot after flop ≈ 18bb. Turn: hero is HJ with
`Ac 8h` on `6c 8c 2d | 3c` (turn — third club, flush completes).
BB checks, hero acts. Pot ≈ 18bb, effective stacks ≈ 92bb behind,
**SPR ≈ 5**.

**Step 1 — Enumerate:**
Facing a check on turn with flush-completing card. Candidates:
`["CHECK", "BET_33", "BET_75"]`. Turn sizings per
`feedback_solver_aligned_sizing.md`. No raise to enumerate (no bet
faced). Bucket-aligned (likely BET_33 thin value with blocker)
included; opposite-direction (CHECK) included.

**Step 2 — Cases AGAINST each candidate:**

- **Against CHECK:** "Per-villain composition (BTN folded, BB only):
  0.20 TP+ / 0.35 medium / 0.30 draws / 0.15 air. Mixed shape
  skewed medium+draws. The 4th club arrived on turn — 0.30 draws
  slice now includes ~5pp of completed-flush combos (residual)
  but Ac blocker reduces nut-flush combos in villain's hand. Hero
  A8 = TPWK + Ac nut-flush blocker. Worse_hand_pct ~0.66. CHECK
  surrenders thin value from 0.35 medium (which calls 33% pot) AND
  surrenders fold equity from the non-nut completed-flush portion
  of draws (Ac blocks villain's nut flushes, so completed flushes
  in villain's range are mostly sub-nut and fold to BET_33 ~50%
  of the time). EV cost: ~0.10-0.12 × pot ≈ 2bb."

- **Against BET_33:** "Small turn bet captures thin value + non-
  nut-flush fold equity, but exposes hero to check-raise from
  villain's flushed combos (residual ~5pp). Hero loses big when
  check-raised — TPWK has poor equity vs flush (~15%). Case-
  against BET_33 is real (variance from check-raises) but bounded:
  Ac blocker reduces flush combos; 5pp × 30% raise frequency =
  ~1.5% of villain's range raises this; EV impact small."

- **Against BET_75:** "Large turn bet over-bluffs hero's range —
  TPWK on 4-flush turn is not the right shape for polarised
  sizing. Villain's continuing range to BET_75 is heavy completed-
  flushes + sets + 2-pair, all of which beat A8. Case-against
  BET_75 is decisive: wrong sizing for hero's hand-class on this
  texture."

**Step 3 — Tier ratings:**

- CHECK: **MODERATE (2)** — cites composition + blocker, quantifies
  value+FE surrender (~2bb) but magnitude moderate (not decisive
  on this texture given check-raise risk).
- BET_33: **WEAK (1)** — identifies real concern (check-raise
  variance) but quantifies as small (1.5% of range raises);
  magnitude bounded.
- BET_75: **STRONG (3)** — quantifies sizing-mismatch (continuing
  range beats hero), feature-grounded, considers best counter
  (heavy continuing range to large sizing).

**Step 4 — Eliminate STRONG cases-against:**
STRIKE BET_75 (STRONG: continuing range to large sizing beats hero).
Surviving: CHECK (MODERATE), BET_33 (WEAK).

**Step 5 — Multiple survivors:**
WEAK < MODERATE → choose BET_33. Tie-breaker not needed.

**Action:** BET_33 (sizing 33%, ~6bb into 18bb). **Confidence:**
HIGH (WEAK survivor only). **Final:** BET_33.
**case_against_strong_count:** 1. **case_against_moderate_count:** 1.
**case_against_weak_count:** 1.

**Per-villain note:** Step 1 composition uses BB-only (post-fold)
chain-narrowed range per Stage 3.5 MUST #46 (folded villain
contributes 0 weight). The case-against arguments cite per-villain
composition explicitly. Cross-protocol parity with Protocol B
Example 5 — both protocols converge on BET_33 with HIGH confidence.

---

## Anti-patterns (Protocol C specific)

In addition to v3.1's anti-patterns (DO NOT Rules 1-11 + v3.1
§"Anti-patterns"), Protocol C labellers MUST avoid the following
Protocol-C-specific failure modes. Each item names the failure,
gives an example of the disguised reasoning to watch for, and the
corrective action.

1. **Strawman-only cases-against.** Producing case-against arguments
   that don't survive even cursory scrutiny. The protocol's value
   REQUIRES genuine adversarial arguments. A labeller who can only
   strawman has nothing to eliminate.
   - *Example of disguise:* "BET is wrong because villain might
     fold." (Folding is the BET's success scenario for fold equity,
     not a refutation.)
   - *Corrective:* every case-against must cite at least one
     specific feature value AND quantify (or directionally argue)
     EV cost. Vague gestures at "GTO principles" without feature-
     grounding are STRAWMAN.

2. **Pre-commitment then post-hoc adversarial dressup.** Picking the
   action you'd have picked under v3.1, then writing cases-against
   the others to justify it. This destroys the protocol's blind-
   spot-detection value.
   - *Example of disguise:* labeller writes case-against FOLD as
     "FOLD surrenders equity, BAD" without specifying the equity
     gap; then writes case-against BET as "BET commits chips, BAD"
     without specifying SPR/equity. Both cases-against are
     symmetric-vague — sign of pre-commitment.
   - *Corrective:* the case-against tier ratings must be
     DIFFERENTIATED across candidates. If all candidates have the
     same tier, the labeller is not actually doing adversarial
     elimination. Self-grading rule: swap any two case-against
     arguments and check whether the tier ratings would change —
     if no, you are tier-inflating.

3. **Tier inflation.** Rating all cases-against at MODERATE because
   it's safer than committing to STRONG. A labeller who never
   produces STRONG cases-against is not actually eliminating —
   they're just ranking.
   - *Example of disguise:* "BET MODERATE, CHECK MODERATE, FOLD
     MODERATE — pick BET because bucket says BET." This is rule-
   first reasoning hidden behind uniform MODERATE tiers.
   - *Corrective:* on every hand, the elimination trail MUST
     contain at least one STRONG OR at least one STRAWMAN tier
     rating (i.e. the tier distribution can't be uniform). If you
     find yourself uniformly MODERATE, ask: "is there a candidate
     I should be willing to eliminate?" If yes, write its STRONG
     case-against. If no, the surviving action profile is genuinely
     close — invoke MIXED handling if the survivors are a recognised
     mixing pair.

4. **Skipping enumeration.** Jumping to a 2-candidate field because
   "the others are obviously wrong." Sometimes the obvious-wrong is
   exactly the answer (cf. solver findings on hands experts thought
   were obvious — see `feedback_solver_findings.md`).
   - *Example of disguise:* on a check-line decision, labeller
     enumerates only `[CHECK, BET]` and never considers RAISE or
     opposite sizing. Misses the spot where overbet is the GTO
     answer.
   - *Corrective:* enumerate ALL feasible candidates per the
     Step-1 sizing tables. If the bucket-aligned action is not in
     the enumeration, you have under-enumerated. The Step-1
     completeness check exists for this purpose.

5. **Retrofitting elimination order.** Eliminating candidates in
   service of a pre-decided action. The ELIMINATION ORDER must
   follow the case-against tier ratings, not the labeller's
   preference.
   - *Example of disguise:* labeller wants to choose BET_66; rates
     CHECK as STRONG case-against (correct), then rates BET_25 as
     STRONG case-against just to leave BET_66 alone — but the
     case-against BET_25 is actually MODERATE.
   - *Corrective:* tier ratings come from the case-against quality
     per §"Step 3" rubric, not from the desired survivor. If two
     candidates have comparable case-against quality, both should
     get the same tier — and Step 5's tie-breakers / MIXED
     handling resolve the contest.

6. **Ignoring villain's mixed-strategy responses.** Treating villain
   as pure-strategy when constructing the case-against. Villain
   often mixes (e.g. "raises 30% of TP+ to a c-bet, calls 70%") —
   the case-against must consider the mix, not the pure response.
   - *Example of disguise:* "BET_66 is wrong because villain's TP+
     ALWAYS check-raises." Villain's TP+ raises ~30% of c-bets, not
     100%. The case-against is overstated.
   - *Corrective:* when citing villain's response to an action,
     specify the response frequency. If you don't know the
     frequency, cite a directional argument ("villain raises some
     TP+ to BET_66, magnitude limited by [feature]") rather than
     pure-strategy assumptions.

7. **Treating bucket-aligned action as automatic survivor.** The
   bucket-aligned action is NOT immune to STRONG case-against. If
   you find yourself never producing STRONG cases-against the
   bucket-aligned action, you are deferring to v3.1 instead of
   eliminating.
   - *Example of disguise:* "Bucket says CHECK, so case-against
     CHECK is WEAK by default." Bucket-aligned action might still
     be STRONG-eliminable (e.g. on hands where Protocol A's
     systematic bias is the bug Protocol C is supposed to surface).
   - *Corrective:* tier-rate the bucket-aligned action's case-
     against using the same §"Step 3" rubric you use for non-
     bucket actions. Bucket-aligned actions can and should be
     STRONG-eliminated when the case-against is feature-grounded
     and decisive.

8. **Equity-vs-pot-odds conflation in the case-against.** Citing
   `equity_vs_range = 0.43` (a pre-computed feature) AND a
   composition pct in the same case-against argument — the
   tier-grader can't tell whether the equity number drove the
   case-against or the composition did.
   - *Example of disguise:* "FOLD is wrong because equity_vs_range
     = 0.43 + heavy-air composition." The 0.43 came first.
   - *Corrective:* the case-against argument should derive equity
     FROM the composition slices (per Protocol B Example 2 carve-
     out: "hero beats 0.59 of villain's range, equity ~0.40") OR
     cite `equity_vs_range` as a confirmation in a separate
     sentence — but not as the primary feature-grounded argument.
     This mirrors Protocol B Anti-pattern #7's carve-out: equity-
     derived-from-composition is allowed; tracker-style raw
     equity-vs-pot-odds is not.

9. **Adversarial-elimination failure on capped or near-degenerate
   ranges.** Adversarial elimination assumes villain's range has
   meaningful candidate-action variance. When `villain_range_capped
   = 1` OR when chain narrowing produces a near-degenerate range
   (one slice > 0.70), the case-against arguments may be
   misleading.
   - *Example of disguise:* "STRONG case-against CHECK because
     villain's TP+ slice is 0.78." But 0.78 TP+ on a cold-caller's
     range may be a capped-range artifact — the surviving TP+ is
     mostly TP-weak-kicker.
   - *Corrective:* if any slice exceeds 0.70 OR `villain_range_capped
     = 1`, set confidence = MEDIUM at best AND note the degenerate-
     range condition in the elimination trail. The case-against
     arguments may still be valid but the confidence cannot be HIGH.

10. **Borrowing Protocol A vocabulary in the case-against.** Citing
    "DO NOT Rule X" or "Bucket-3W-Y" as the PRIMARY justification
    for a case-against tier rating is a sign the labeller is
    reasoning Protocol-A-style and back-fitting. These references
    are LEGAL as confirmation but not as primary justification.
    - *Example of disguise:* "STRONG case-against BET because DO
      NOT Rule 5 says don't treat TP as strong." DO NOT Rule 5 is
      a v3.1 rule; the case-against should derive from features
      (composition, position, SPR) and CITE DO NOT Rule 5 as
      confirmation if relevant.
    - *Corrective:* every case-against tier rating must be
      justified by at least one feature value (composition pct,
      equity, position, SPR, action history). DO NOT Rules and
      bucket names are PERMITTED as confirmation but not as the
      primary feature-grounded argument.

[UNCERTAIN — REVIEWER-VERIFIED in PR #12 review (Item H at
`7d56b09`): anti-pattern #8's carve-out parallels Protocol B v1.0.1's
Anti-pattern #7 carve-out. Reviewer confirmed wording consistency
across protocols. Forbidden in BOTH: pre-computed `equity_vs_range`
feature read OR tracker-style raw equity-vs-pot-odds as primary
driver. Allowed in BOTH: equity derived FROM composition slices in
the same trace; `equity_vs_range` cited as confirmation in a separate
sentence. Example 2 exercises the carve-out exactly as designed
(composition-derived equity 0.40 from beatable-slice 0.59 — same
structure as Protocol B v1.0.1 Example 2).]

---

## Schema/CSV verification (Protocol C addition)

**Verified against** (per Protocol B v1.0.1 verification — same
infrastructure, additive label-side metadata):
`river-rats-core/feature_keys.py` (FEATURE_COLUMNS),
`river-rats-core/gto_model.py` (FEATURE_COLUMNS, ACTION_CLASSES),
`river-rats-core/assemble_pilot_data.py` (CSV writers),
`river-rats-core/export_3way_training.py` (CSV header).

**Compatibility status:** Protocol C's new JSON fields (`protocol`,
`candidate_actions`, `case_against`, `elimination_trail`,
`final_action`, `case_against_*_count`, `mixed_action_pair`,
`mixed_confidence_band`, `mixed_strategy_acknowledged`,
`primary_action`, `escalate_to_adjudicator`) are **label-side
metadata only** — they do NOT extend `FEATURE_COLUMNS` and do NOT
add columns to the training CSV. Compatible with v2.4 trainer with
no trainer-side changes required.

**Where Protocol C's metadata lands:**

The Protocol C JSON fields are written to the canonical JSONL only
(per `assemble_pilot_data.py:893-904 write_enriched_jsonl`). They
become inputs to the cross-protocol convergence checker (a Stage 4
deliverable) and to the Stage 4 reviewer dashboard. They are NOT
consumed by `train_v2_4.py` (when authored).

**Required trainer updates:** NONE for v2.4 ship.

**Optional v2.5+ extension (not in scope for Stage 4):** if a future
model wants to train on `case_against_strawman_count` or
`mixed_strategy_acknowledged` as a hard-spot signal, it would land
as additional binary/integer features per the
`feedback_attention_flags_when_features_change.md` 4-stream update
(raw feature + attention vocab + prompt rule + capture). OUT OF
SCOPE for Protocol C v1.0.

[UNCERTAIN: same as Protocol B v1.0.1 — `train_v2_4.py` does not
exist on disk yet; verification confirms backwards-compatibility
with `train_v2_3_2.py`. Reviewer should re-run verification once
v2.4 trainer is authored.]

---

## Author note (v1.0 fill)

This file is the STRUCTURAL FRAMEWORK + CONTENT FILL for Protocol C.
The skeleton + reasoning order + DO NOT additions + output-schema
additions were locked-in design at v0.1 by the orchestrator. The
poker-judgment specifics (sizing enumeration completeness, 4-tier
case-against rubric with examples, calibration grading rubric,
worked examples, anti-pattern list, MIXED handling) were filled in
at v1.0 by a general-purpose subagent acting under gto-expert +
ml-architect personas (per Task 2 dispatch, dedicated subagents
unavailable).

**Lessons applied from Protocol B v1.0 → v1.0.1 fix-forward:**

- Worked examples use 100bb depth with realistic preflop opens
  (~3bb) and conventional sizing — pot/SPR math is internally
  consistent (verified in self-consistency pass below)
- PRE-PILOT BUILD REQUIREMENT section added explicitly (mirror of
  Protocol B v1.0.1 §"PRE-PILOT BUILD REQUIREMENT")
- Anti-patterns cross-checked against worked examples — no
  anti-pattern flags any worked example as failing (see self-
  consistency pass below)
- Equity-vs-pot-odds carve-out (Anti-pattern #8) parallels Protocol
  B v1.0.1 Anti-pattern #7 carve-out for cross-protocol consistency

Remaining review chain:

1. Owner review of the v1.0 / v1.0.1 framework + content
2. v1.0 independent reviewer pass at `7d56b09` — APPROVE-WITH-NITS
   (1 MEDIUM, 2 LOW, several NITs); MEDIUM #1 (raise-sizing taxonomy)
   addressed in this v1.0.1 fix-forward
3. v1.0.1 independent reviewer pass (different reviewer dispatch) —
   verify MEDIUM #1 fix; verify no new MEDIUMs introduced; remaining
   focus on `[UNCERTAIN: ...]` tags and the 4-tier case-against
   rubric (ML-grading-consistency target; inter-grader κ verification
   to land at pilot calibration per verdict action item #8)
4. Calibration exam against the 24-hand reference set per the
   rubric in §"Calibration"
5. Owner final approval before pilot uses Protocol C

Provenance discipline: every revision of this draft records its
authoring lineage at the top of the file (see frontmatter).

This is v1.0.1. Subsequent revisions land as
`protocol_c_adversarial_elimination_v1_1.md`, etc. The v0.1 DRAFT
remains on disk in `prompts/stage4_drafts/` as a historical artifact
per `feedback_quality_default_no_ask.md`. The v1.0 file is preserved
in this same path with frontmatter `version: v1.0.1` per fix-forward
discipline (no parallel v1.0 file on disk; git history at `d77a95e`
is the v1.0 reference).

---

## Self-consistency pass (v1.0 author note)

Per Task 2 mandatory self-consistency pass, the author verified:

**Worked examples — pot/SPR/sizing arithmetic:**

- Example 1: BTN open 3bb + SB call 2.5 + BB call 2 = 9 chips into
  preflop pot (correct: BTN posts 3, SB completes 2.5, BB
  completes 2). Both check to BTN. Pot 9bb, stacks ~97bb behind,
  SPR = 97/9 ≈ 10.8 ≈ 11. BET_66 sizing 6bb into 9bb pot ✓.
- Example 2: chip-unit form per Protocol B Example 2 convention
  (preflop pot 30, CO bet 30, BTN call 30, hero faces 90 with
  to_call 30, pot odds 30/120 = 0.25 ✓). Equity surplus 0.40 -
  0.25 = 0.15 ✓. Stack-depth conversion: at 100bb depth, preflop
  pot 9.5bb, CO bet 4.75bb (half-pot), etc.
- Example 3: BTN open 3bb + SB call 2.5 + BB call 2 = 9bb pot ✓.
  SPR ≈ 11 ✓. BET_66 sizing 6bb ✓.
- Example 4: CO open 3bb + BTN call 2 + BB call 2 = 9bb pot ✓.
  SPR ≈ 11 ✓.
- Example 5: HJ open 3bb + BTN call 2 + BB call 2 = 9bb preflop
  pot. Flop: HJ bets 4.5bb (half-pot), BTN folds, BB calls 4.5bb.
  Pot after flop = 9 + 4.5 + 4.5 = 18bb ✓. Stacks ~92bb behind
  (started 100, posted 3, called/bet 4.5+0+0 = 0 more contribution
  via flop; actually HJ committed 3 preflop + 4.5 flop = 7.5bb;
  stacks ≈ 92.5bb behind). SPR = 92.5/18 ≈ 5.1 ≈ 5 ✓. BET_33
  sizing on turn = 6bb into 18bb ✓.

**Anti-pattern cross-check against examples:**

- Anti-pattern #1 (strawman-only): Examples 1-5 all cite specific
  feature values and quantify EV — none flag.
- Anti-pattern #2 (pre-commitment + dressup): Tier ratings in all
  examples are differentiated (mix of STRONG/MODERATE/WEAK across
  candidates) — none flag.
- Anti-pattern #3 (tier inflation): Each example has at least one
  STRONG OR MIXED handling — none flag.
- Anti-pattern #4 (skipping enumeration): All examples enumerate
  bucket-aligned + opposite-direction action — none flag.
- Anti-pattern #5 (retrofitting elimination order): Tier ratings
  derive from §"Step 3" rubric in all examples — none flag.
- Anti-pattern #6 (ignoring villain mixed-strategy): Examples 1, 3,
  4 cite villain response frequencies (e.g. "TP+ raises ~30% of
  c-bets", "0.20 medium calls 60%") — none flag.
- Anti-pattern #7 (bucket-aligned auto-survivor): Examples 1, 3
  STRONG-eliminate the smallest-sizing bet (BET_25) which is a
  legitimate bucket-aligned candidate; bucket-aligned action is
  not immune — none flag.
- Anti-pattern #8 (equity-pot-odds conflation): Example 2 cites
  composition-derived equity (0.40 derived from beatable-slice
  0.59) per the explicit carve-out — does NOT flag (intentional
  parallel to Protocol B Example 2 carve-out).
- Anti-pattern #9 (capped-range failure): No example has
  villain_range_capped = 1 or slice > 0.70; not exercised. Not a
  flag.
- Anti-pattern #10 (Protocol A vocabulary in case-against):
  Examples cite features (composition, equity, SPR) as primary
  justification; bucket / DO NOT Rule references appear as
  confirmation only — none flag.

**UNCERTAIN tags added:**

1. ~~Step 1 raise sizings (2.5×/3× facing-bet multiples vs solver
   pot-relative)~~ — **RESOLVED in v1.0.1 fix-forward.** Replaced
   with pot-relative `RAISE_33` / `RAISE_66` per
   `feedback_solver_aligned_sizing.md`. Tag retired.
2. Mixed-strategy convergence-checker scoring (MIXED includes
   single-A/B = convergent vs weakly convergent) — reviewer should
   confirm with convergence-checker design doc.
3. ~~Schema-compatibility verification re-run for Protocol C field
   names~~ — **REVIEWER-VERIFIED in PR #12 review (Items G + J at
   `7d56b09`).** Direct enumeration vs `FEATURE_COLUMNS` confirmed
   no name collisions; Protocol C metadata is JSONL-only and
   compatible with v2.4 ship with no trainer-side changes. Tag
   downgraded; v2.5+ training on `case_against_*_count` features
   would re-trigger the 4-stream protocol per
   `feedback_attention_flags_when_features_change.md`.
4. κ ≥ 0.65 grader-consistency target — borrowed from Protocol B
   v1.0.1, may need tightening. Reviewer Item J/K + verdict action
   item #8: measure empirically at calibration; adjust gate in v1.1.
5. Composition pcts in worked examples are poker-theoretic
   estimates calibrated to KB §1.x and Protocol B v1.0.1 numbers
   — solver-verification deferred.
6. ~~Anti-pattern #8 carve-out language parallels Protocol B v1.0.1
   Anti-pattern #7~~ — **REVIEWER-VERIFIED in PR #12 review (Item H
   at `7d56b09`).** Wording parallels Protocol B v1.0.1 AP#7
   (forbidden: pre-computed `equity_vs_range` OR tracker-style raw
   equity-vs-pot-odds as primary driver; allowed: equity derived
   FROM composition slices in same trace; allowed: `equity_vs_range`
   as confirmation in separate sentence). Example 2 exercises the
   carve-out exactly as designed (composition-derived equity 0.40
   from beatable-slice 0.59). Tag downgraded.
7. v2.4 trainer (`train_v2_4.py`) does not exist on disk yet —
   verification confirms v2.3.2 backwards-compatibility; v2.4 to
   re-verify when authored.

Tags 2, 4, 5, 7 remain open (real verification gaps requiring
reviewer/owner input or future infrastructure). Tags 1, 3, 6
resolved in v1.0.1 (1 by fix-forward; 3 + 6 by reviewer
verification).

---

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` — locked
  Stage 4 plan; Protocol C is one of 3 labelling protocols
- `prompts/gto_labeller_v3.1.md` — Protocol A baseline (current
  production prompt); inherited Buckets / Features / DO NOT Rules
- `prompts/protocol_b_composition_first_v1_0.md` (v1.0.1 merged) —
  Protocol B; cross-protocol pair for Examples 2 + 4
- `BUILDER_V24_STAGE35_BLUEPRINT_V2_3_AMENDED_2026-04-22.md` —
  chain-narrowing semantics; per-villain composition; MUST #28,
  #46, #48, #52
- `BUILDER_V24_STAGE35_COMPLETE_2026-04-20.md` — Stage 3.5
  closeout including `_per_villain_composition` plumbing
- `BUILDER_V24_P1_SPEC_LOCKED_2026-04-19.md` — 4 v2.4 P1 blocker
  features (#56-#59)
- `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md` — Exp 3
  auxiliary attention flags (production highlighting approach;
  Protocol C inherits)
- `PASS1_COMPARISON_REPORT_2026-04-14.md` — 4-team Pass 1 baseline
  (motivates protocol diversity for Stage 4)
- `feedback_solver_aligned_sizing.md` — flop 25%/66%, turn 33%/75%,
  river 33%/75%/150%; canonical sizings used in Step 1 enumeration
- `feedback_solver_findings.md` — solver findings on hands experts
  thought were obvious; motivates Anti-pattern #4 (don't skip
  enumeration)
- `feedback_terminology_raise_vs_bet.md` — raise=raise of existing
  bet, bet=first postflop bet
- `feedback_close_hand_selection.md` — close hands are exactly
  where Protocol C's elimination should add the most value vs
  forward-reasoning protocols
- `feedback_preflop_geometry_vs_postflop_composition.md` — the
  insight that motivated Protocol B's existence; relevant to
  Protocol C's case-against arguments which read composition pcts
- `river-rats-core/anchors/calibration_anchors.json` — calibration
  anchor JSON (d2410, d8411, LITMUS_*, MW-30, MW-46, MW-47, etc.)
  used in Examples 2 and 4
- Adversarial reasoning / Popper falsifiability — methodological
  background for the protocol design (no direct doc; adopted from
  scientific-reasoning best practice)
