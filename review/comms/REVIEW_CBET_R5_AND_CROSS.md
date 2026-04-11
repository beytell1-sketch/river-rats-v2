# Review: RESEARCH_CBET_R5_BLOCKERS.md + Cross-Consistency (R1–R5)

**Reviewer:** Independent Reviewer
**Date:** 9 April 2026
**Primary subject:** RESEARCH_CBET_R5_BLOCKERS.md
**Secondary scope:** Cross-consistency check across R1 (Frequency), R2 (Texture),
R3 (Sizing/SPR), R4 (Check-back), R5 (Blockers)
**Status:** ISSUES FOUND — see flagged items. Most are documentation improvements
or KB additions; no blockers are fatal to proceeding.

---

## Part 1: R5 (Blockers) Review

### 1.1 Source Count and Named Sources

R5 cites 14 numbered sources, all named with URLs. This exceeds the 8-source
minimum. Source quality is high: 8 of 14 are GTO Wizard solver-backed articles,
2 are Upswing Poker, 1 is Cardquant (solver-informed), 1 is Crush Live Poker
(practitioner), 1 is Pokercode (quantified combo reduction), 1 is Phil Galfond
(expert analysis). The source mix is appropriate for this topic — flush blockers
are discussed across the GTO literature and the document draws from all of it.

**Source count: PASS (14 >= 8)**
**Source quality: PASS**

---

### 1.2 Quantification: Sourced vs Derived

R5 contains several quantified claims. This section assesses each.

**Claim 1: "Nut flush blocker adds +8-15pp fold equity per opponent"**
Source: Pokercode (Queen = +5.7pp from 22% combo reduction) + first-principles
inference for Ace (larger effect, "estimated"). The +5.7pp figure for a Queen
blocker is directly sourced. The Ace estimate of +8-15pp is a derived inference
based on Ace blocking more combos than a Queen. The document states this is an
inference ("estimated from combo reduction ratios") and is transparent about it.
Math logic is internally consistent.

Finding 8 then does a second derivation: combined fold equity with nut flush
blocker vs without, across the bet-size table. The math is shown step by step
and is correct:
- Baseline combined fold: 0.70 x 0.70 = 49%
- With Ah against one flush-draw-heavy opponent: 0.79 x 0.70 = 55%
- The 0.79 estimate is flagged as a "rough estimate from combo removal," not a
  direct solver output.

This is the correct way to present derived estimates: show the math, flag the
uncertainty, do not claim false precision. PASS.

**Claim 2: Combo draw = 12-15 outs, ~50-55% equity vs single made hand**
Sourced directly (Upswing Poker, "How to Play Combo Draws in Cash Games"). PASS.

**Claim 3: Backdoor equity table (e.g., backdoor flush = ~3-4%)**
Document states "Synthesized from GTO Wizard equity research and Cardplayer
backdoor draw data." The 3-4% backdoor flush equity figure is a well-established
approximation (2 streets, ~4.2% to complete). Internally consistent and
standard. PASS.

**Claim 4: Large c-bet drops from 18% to 1.3% in 3-way**
Directly sourced (GTO Wizard, "Playing In Position Against Two Callers"). PASS.

Overall quantification assessment: R5 handles derived estimates correctly.
The estimates are flagged, the math is shown, and primary-sourced numbers are
distinguished from inferences. This is appropriate rigor for publicly available
GTO content.

---

### 1.3 Contradiction Check with KB Section 1.7 and 1.8

**KB Section 1.7** (Semi-Bluff Conditions) specifies:
- Nut draw REQUIRED
- Blocker to villain's continuing range REQUIRED
- Side equity strongly preferred
- Position: "Any (even OOP)"

**R5 Finding 6** qualifies the OOP claim:
> "For BET decisions without the raise component, IP amplifies the blocker value
> meaningfully."

R5 notes correctly that Section 1.7 specifies OOP-acceptable conditions for
RAISE decisions specifically. For initial BET (c-bet) decisions without a raise
component, IP is preferred. This is a legitimate refinement, not a contradiction.
The KB makes the OOP claim in the context of the AsQs check-raise example
(Example 9), which is a RAISE decision. R5's Rule 1 in the BET framework
correctly requires IP as preferred for pure blocker-justified c-bets.

**Verdict:** Not a contradiction. R5 is adding precision that the KB should
acknowledge in a future update.

**KB Section 1.8** (Blocker Effects on Action Selection) states:
> "Blockers for choosing WHICH bluffs to run matter ~40% less 3-way (need to
> block both opponents). But blockers for deciding RAISE vs CALL... are still
> critical."

**R5 Contradiction A** (Section 4) explicitly flags this: blockers have
opposite effects on bluff c-bets vs thin value c-bets. KB Section 1.8 treats
blockers as uniformly positive for "action selection" (raise vs call) but the
BET-tree context (bet vs check) is different. In the RAISE context, blocking
villain's continuing range is always good. In the BET context, blocking
villain's flush draws means fewer callers with weak hands — potentially hurting
thin value bets. R5 surfaces this correctly.

**ISSUE 1 (KB Gap):** KB Section 1.8 does not distinguish between the RAISE
context (block villain's strong continuing hands = good) and the BET context
(block villain's weak drawing hands = reduces callers for value bets = may be
bad). R5's Contradiction A should be added to KB v1.3 as a clarifying note.

---

### 1.4 Feature Gap Claims: Are They Real or Already Covered?

R5 identifies three feature gaps:

**Gap A: Backdoor flush draw not captured in draw_outs**
Status: REAL AND CONFIRMED. The KB (Example 7) already acknowledges that
draw_outs misses overcard equity. R5 extends this: the same gap applies to
backdoor flush equity (3-4%). The pipeline counts frontdoor draws only. This
is a genuine labelling quality issue that R5 correctly identifies and that KB
Example 7 had partially flagged for overcards but not for backdoor draws
specifically. Gap is real, is additive to existing documentation.

**Gap B: Made-hand nut blocker not in flush_block_pct**
Status: REAL. flush_block_pct measures villain's flush draw combos blocked.
It does not capture the "value safety" effect of holding Ah on an Ace-high
board (blocking AA, AK). R5 correctly notes this is a separate mechanism with
no current feature representation. Gap is real and is a labelling quality
issue: thin value c-bets on Ace-high boards where hero holds Ah may be
under-labelled.

**Gap C: Straight blocker absent from features**
Status: REAL but lower priority. draw_outs counts outs but does not encode
whether hero blocks villain's straight combos. R5 correctly marks this as
lower-priority than Gaps A and B. Real but not urgent.

All three gaps are legitimate. None are "already covered" by existing features.

---

### 1.5 Additional R5-Specific Observations

**Observation 1 (Minor inconsistency in Contradiction B):**
R5 raises a contradiction between PROPOSAL_BLUFF_FEATURES.md (combo draws at
67%+ equity are checks, not bluffs) and KB Section 1.7 (nut draws as primary
semi-bluff candidates). R5 resolves this correctly: the distinction is between
draws with 40-50% equity (semi-bluff territory) and draws with 55-67%+ equity
(pure equity call, fold equity is irrelevant). R5's own Rule 3 handles this
correctly. However, the KB does not make this threshold explicit — KB Section
1.7 says "nut draw required" without specifying an upper equity bound above
which the semi-bluff logic inverts. This should be clarified in KB v1.3.

**Observation 2 (Source Reuse):**
Three sources are reused across multiple findings (GTO Wizard Playing IP Against
Two Callers, GTO Wizard Probing OOP, Upswing). Reuse is clearly flagged ("Source
3 reuse"). This is acceptable practice — these articles cover multiple topics —
and the attribution is transparent.

**Observation 3 (Gutshot + blocker edge case, Rule 2):**
R5 Rule 2 labels "gutshot (4 outs) + nut flush blocker" as a weak c-bet
candidate requiring "dry board + IP + villain_air >= 0.30." The KB's DO NOT
Rule #2 states "pure bluffs are unprofitable 3-way" and its carve-out is
"nut draw with blocker." A 4-out gutshot is not a nut draw. R5's Rule 2 is
treating this as a thin exception, which it is, but the exception language
should make clear this is an edge case that should not be generalized. R5
does note "this is a marginal edge case" — acceptable, but worth flagging for
the labelling agent so it doesn't over-weight this.

---

### R5 Verdict: PASS WITH RECOMMENDED KB UPDATES

R5 meets all review criteria:
- Sources: 14 named, all with URLs. PASS.
- Quantification: derived estimates are flagged with math shown. PASS.
- No fundamental contradictions with KB 1.7 or 1.8; R5 adds precision where
  the KB is correct but incomplete.
- Feature gaps identified are all real, none are already covered.

Recommended KB updates (for v1.3):
1. Section 1.8: Add note that flush blockers have opposite effects on bluff
   c-bets (positive) vs thin value c-bets (neutral-to-negative). The current
   framing is correct for raise decisions but incomplete for bet-vs-check.
2. Section 1.7: Add upper equity threshold note — draws with 55%+ equity do
   not require or benefit from a semi-bluff framing. They are equity calls.
3. New section or note: Backdoor flush equity is not captured in draw_outs.
   Labelling agent should note ~3-4% hidden equity for backdoor flush hands.

---

## Part 2: Cross-Consistency Check (R1 through R5)

### 2.1 Core Frequency Numbers — Do They Agree?

The central anchor number is c-bet frequency: HU ~54%, 3-way ~43%.

| Document | HU c-bet | 3-way c-bet | Source |
|----------|----------|-------------|--------|
| KB (v1.2) | ~54% | ~43% | GTO Wizard |
| R1 (Frequency) | ~54-60% | ~33-43% | GTO Wizard, Acevedo |
| R2 (Texture) | Not stated (uses 43% as aggregate) | ~20-70% by texture | GTO Wizard |
| R3 (SPR) | Not stated | ~43% aggregate, SPR-modified | GTO Wizard |
| R4 (Check-back) | ~54% | ~43%, check ~57% | GTO Wizard |
| R5 (Blockers) | Not stated | Uses 1.3% large c-bet, consistent with KB | GTO Wizard |

**Assessment:** All five documents use the same 43% aggregate as the baseline.
R1 provides the most detail, noting the 43% is an IP-weighted average and that
OOP PFA c-bets closer to 22-30%. R3 independently confirms that the 43%
aggregate comes from the specific GTO Wizard LJ-opens/two-callers configuration.
R4 confirms the check frequency corollary (57%). R2 places the 43% correctly
as the aggregate behind a 20-70% texture range. No contradictions.

**ISSUE 2 (Internal refinement, not a contradiction):** R1 argues the KB's 43%
figure overstates OOP PFA frequency (OOP is 22-30%, not 43%). R4 uses 43% as
a general anchor without breaking out OOP separately. Both documents are written
by different researchers but neither directly contradicts the other — they are
describing different levels of granularity. However, the labelling agent reading
both R1 and R4 could come away with a slightly inconsistent mental model if
the position-split is not explicitly flagged. This should be resolved in KB
integration: the 43% is an IP-weighted aggregate; OOP PFA c-bets ~22-30%.

---

### 2.2 Fold Equity Math — Do All Documents Agree?

KB Section 1.1: 0.70 x 0.70 = 49% combined fold equity vs pot-sized bet.
R4 (Finding 2): 0.70 x 0.70 = 49%. "Right at break-even."
R5 (Finding 8): Uses 49% baseline, then adds blocker to get 55%.
R3 (Finding 6): Does the MDF math independently (pot geometry). Arrives at
requiring each opponent to fold 86.7% for a pure 33% pot bluff to break even
— correctly notes this is unrealistically high, so small bets are for VALUE not
bluffing. This is a different framing (per-opponent independence math) but fully
consistent with the 49% combined fold equity figure.
R1 (Finding 2): Does not redo the fold equity math but references the existing
KB calculation.

**Assessment:** Consistent across all documents. The fold equity math is
identical everywhere. PASS.

---

### 2.3 Sizing Consensus

| Document | Small c-bet (25-33%) | Large c-bet (>50%) |
|----------|---------------------|--------------------|
| KB | Default 3-way | ~1.3% only |
| R1 | 25-40% standard; 75%+ eliminated | Confirmed eliminated |
| R2 | 25-33% most textures; A-high allows ~40-50% | Only sets and nut hands on A-high |
| R3 | 25-33% at medium-high SPR; 50-75% at SPR<2 | SPR<2 only |
| R4 | Not a primary focus; accepts KB sizing | Consistent with KB |
| R5 | Rule 2: small only (25-33%) for blocker c-bets | Not addressed |

**ISSUE 3 (Apparent Contradiction — Resolved):** R2 states A-high boards
support sizing up to ~50-66% (poker.pro source citing solver for AK/AA/KK
holdings). R3 states large bets (>50%) are justified at "low SPR or with nut
edge on specific textures." These are not contradictory — R2's sizing-up on
A-high applies specifically to nut-holding c-bets (AA, AK) which represent
the nut edge R3 requires. The condition is the same; the documents describe it
from different angles (texture in R2, SPR + nut edge in R3).

However, R1 states "c-bets above 50% pot in a 3-way pot [are] near-premium-only
action" and "virtually never bet 75%+ pot as a first bet in a 3-way pot." R2
allows up to 66% sizing on A-high boards for AA/AK. R1 would include AA and
AK as "near-premium" — these are in agreement at the intent level, but the
specific language creates a surface tension. Someone reading R1 in isolation
might think 50-66% is ruled out on the flop, while R2 allows it for specific
premium holdings.

**Recommendation:** KB integration should note: the 25-33% default applies to
non-premium hands. Premium holdings (AA, AK, sets) on boards where they have
clear nut advantage can size to ~40-50%. The 66% figure from R2 is an upper
bound for the most extreme nut-advantage situations, not a regular option.

---

### 2.4 Position Split — Cross-Document Consistency

R1: Explicit. IP PFA ~38-45%, OOP PFA ~22-30%.
R2: Implicit. Uses "PFA" without IP/OOP split most of the time. The frequency
tables (Section 2.1-2.8) do not separate IP from OOP.
R3: Notes OOP c-bets less; the probing OOP article is cited but OOP exact
frequencies are in the "gap" section (data not publicly available).
R4: Notes OOP checks more at 75-80% for monsters. Finding 5 distinguishes OOP
vs IP check purposes. Consistent with R1's position-split conclusion.
R5: Notes IP blockers are more valuable than OOP blockers (Finding 6). Consistent.

**ISSUE 4 (Gap in R2):** R2 provides texture-specific frequency tables (e.g.,
A-high dry: "~60-70%") without specifying whether these are IP PFA or aggregate
figures. R1's data shows IP PFA reaches 58-65% on A-high dry boards, and OOP
PFA reaches 38-45%. R2's "~60-70%" appears to reflect IP PFA (or an average
skewed toward IP). If R2's figures are fed to the labelling agent without the
IP/OOP qualifier, OOP PFA will be systematically over-labelled as betting on
high-card boards. This is a documentation gap in R2, not a contradiction with
R1 — the numbers are compatible if you assume R2 is reporting IP figures.

**Recommendation:** R2 should note whether its texture-specific frequency tables
are IP PFA, OOP PFA, or aggregate. If the intent was aggregate, a downward
adjustment for OOP is needed. If the intent was IP, the document should say so.

---

### 2.5 Slow-playing / Trapping — Cross-Document Consistency

KB: "Sets MUST bet multiway" (Example 4, Jd 8s 5c — semi-connected, two-tone).
R4: Sets check 30-50% even IP 3-way on DRY boards (Finding 4, citing GTO Wizard).
"The trap rule: Slowplay monsters on dry, disconnected boards. Bet monsters on
dynamic boards."
R3: Strong hands check OOP at high SPR; bets strong hands at low SPR.

**Assessment:** No contradiction. The KB's Example 4 uses a semi-connected
two-tone board, which is a protection situation. R4 correctly states this is
the wet-board case. R4 also flags this explicitly as "Contradiction 1" in its
own gaps section, noting the KB example is correct but narrow. The underlying
principle is consistent: sets bet on wet boards (protection), sets check on dry
boards (trap). R4 adds appropriate dry-board worked examples as a gap.

---

### 2.6 BET Tree Implications — Composite Framework

Do the five documents compose into a coherent BET decision tree? Synthesizing:

**Gate 1: Board Texture (R2 primary source)**
A-high dry: ~60-70% IP / ~38-45% OOP
K-high dry: ~50-60% IP / ~30-38% OOP
Connected mid: ~30-40% IP / ~14-20% OOP
Low connected: ~20-30% IP / ~12-18% OOP
Flush danger: -5 to -25pp vs rainbow equivalent

**Gate 2: Position (R1 primary source)**
IP: use frequencies from Gate 1 as stated
OOP: reduce ~30-40% from IP figure
OOP modifier is larger in 3-way than HU

**Gate 3: SPR (R3 primary source)**
High SPR (typical flop in 100bb SRP): use Gate 1+2 frequencies (~43% aggregate)
Low SPR (3BP flop, SRP turn): increase frequency, increase sizing
Very low SPR (<2): bet strong hands, size 50-75%

**Gate 4: Blocker / Draw quality (R5 primary source)**
Combo draw (12+ outs): c-bet regardless of fold equity
NFD + nut blocker: strong semi-bluff c-bet candidate
NFD only (no blocker): call, not raise; c-bet marginal
Blocker only (no draw): thin c-bet, dry board + IP + air-heavy villain required

**Gate 5: Hand Class / Protection (R4 primary source)**
Wet board + strong hand: bet for protection
Dry board + monster: check to trap
Weak hand / air: check-fold
Medium made hand: pot control, gate by villain aggression

These five gates compose without contradictions. There are surface-level
tensions (sizing language, OOP frequencies) but these resolve on closer reading.
The framework is coherent.

---

### 2.7 Cross-Document Issues Summary

| Issue | Severity | Which Documents | Resolution Needed |
|-------|----------|-----------------|-------------------|
| Issue 1: KB 1.8 does not distinguish bluff vs value direction for blockers | Minor | R5 vs KB | KB v1.3 update |
| Issue 2: 43% figure is IP-weighted; OOP PFA is 22-30% | Minor | R1 vs R4 (R4 doesn't break out OOP) | KB integration note |
| Issue 3: Sizing language — R1 says 50%+ is "premium only"; R2 allows up to 66% for AA/AK | Minor | R1 vs R2 | Clarify: 66% is upper bound for nut situations, not a general option |
| Issue 4: R2 texture frequency tables do not specify IP/OOP | Moderate | R2 vs R1 | R2 should be annotated with IP PFA assumption |
| Issue 5: KB 1.7 lacks upper equity bound — combo draws at 67%+ are equity calls, not semi-bluffs | Minor | R5 vs KB | KB v1.3 clarification |

None of these issues represent fundamental research errors. They are
documentation gaps or incomplete specification that would cause labelling
agent confusion if not resolved.

---

## Part 3: Overall Verdict

**R5 verdict: PASS WITH RECOMMENDED KB UPDATES**

R5 is a high-quality research document. Sources are named, numerous, and
appropriate. Quantified estimates are properly flagged as derived. Feature
gaps identified are real. The blocker framework for c-bet decisions (as
distinct from the raise framework in KB 1.7/1.8) is a genuine and valuable
addition. No fundamental errors.

**Cross-consistency verdict: PASS — framework is coherent**

The five research documents compose into a coherent BET decision tree. The
issues found are documentation gaps and specification ambiguities, not
contradictions in poker logic. The most important gap for the labelling agent
is Issue 4: R2's texture frequency tables should be marked as IP PFA figures,
or a position-split version should be provided before those tables are used
to assign labels.

**Priority actions before KB integration:**
1. Annotate R2's frequency tables with "IP PFA" qualifier (or provide OOP
   equivalents). This affects labelling directly.
2. KB v1.3: add the blocker direction reversal note (bluff vs value c-bets)
   to Section 1.8.
3. KB v1.3: add upper equity bound to Section 1.7 (combo draws at 55%+
   equity are equity calls, not semi-bluffs).
4. KB integration note: consolidate the 43% figure into "IP-weighted average;
   OOP PFA c-bets 22-30%."

Items 2-4 are non-blocking for proceeding. Item 1 is the only item that could
cause systematic labelling errors if not addressed.

---

*Reviewer sign-off: ISSUES FOUND — addressed above. No fatal errors. Proceed
to KB integration after resolving Item 1 (R2 annotation) and noting Items 2-5
for KB v1.3.*
