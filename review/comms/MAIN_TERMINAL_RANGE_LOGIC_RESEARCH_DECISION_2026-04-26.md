---
date: 2026-04-26 → 2026-04-27 (research conducted overnight SAST)
from: Main terminal (orchestrator)
to: Owner · Pilot Orchestrator (released) · QC stream · architecture/gto-expert/ml-architect (next round)
re: Range-logic research conclusion — drop the structured-format / mixed-strategy approach; keep v3.2 rule-based protocol; corpus revision is the next blocker before Phase B resumes
status: STRATEGIC DECISION — Phase B Protocol B/C paused. Phase B Protocol A labels (master 4bce49f, PR #50) stand. No further labelling on current corpus. Corpus design audit needed before resume.
---

# Range-logic research — conclusion + strategic decision

## Trigger

Owner flagged that the 500 Protocol A labels (sealed at master `4bce49f` via PR #50) "did not assess range logic" — the pilot 100-hand corpus has 97/100 hands at `facing_bet=0`, producing 0 RAISE / 1 CALL labels across all 5 labellers. Owner reframed the question: *do experts (labeller subagents) actually understand range logic, and is range balance teachable at scale via labels?*

## Research conducted (overnight SAST)

Five rounds of probe dispatches, no further mass labelling:

### Round 1: 7-layer scaffolded range-reasoning probe (d3688 only)
- Sonnet subagent with explicit 7-layer scaffold (range composition / position-in-range / villain composition / range vs range / equity distribution shape / action-history narrowing / blocker effects)
- Result: **CHECK ✓** — agent did real range decomposition (BB defend range distribution, K8 at middle-bottom of Kx hierarchy, KB Example 1 analog)
- Conclusion: Real range reasoning is achievable with explicit scaffold

### Round 2: Same scaffold on MW-39 + d9556
- MW-39: agent **RAISE ✗** (expert CALL). Pattern-matched on KB Example 9, rationalised away the `villain_air_pct=0.05 < 0.20` contradiction.
- d9556: agent **BET ✗** (expert CHECK). No KB pattern to anchor on; reasoned from first principles to exploitatively-tempting BET; missed the GTO-balanced CHECK-for-range-protection answer.
- Conclusion: 1/3 success even WITH 7-layer scaffold. Range vocabulary present; range-balance reasoning systematically failed.

### Round 3: Mixed-strategy structured output test (d9556, leading prompt)
- Asked for primary/alternative/frequency-tier output
- Agent produced format successfully
- Agent's own meta-commentary: *"OFTEN/SOMETIMES/RARELY — without running this exact spot in a solver the split could plausibly be CHECK ~80-85% / BET ~15-20%. The SOMETIMES label for BET reflects that — it could be as low as RARELY (~10%). The exact frequency split is a reasoned estimate, not solver-verified output."*
- Conclusion: Frequency tiers are vibes-based estimates. Useless as ML training signal without numeric ground truth.

### Round 4: Range-decisive flag structured output test (d3688, leading prompt)
- Asked for surface_signal_action vs range_signal_action + is_range_decisive flag + concept tagging
- Format works elegantly with seeded answer
- Confounded: leading prompt told agent the answer

### Round 5: UNLEADING structured output test — 5 hands × 2 labellers (10 probes)
- Hands: MW-50 (FOLD), d8886 (BET), d3688 (CHECK), d9556 (CHECK), d3178 (BET)
- Each labeller: identical prompt, no answer hint, structured JSON required

**Final scoreboard:**

| Hand | Expert | Labeller A | Labeller B |
|------|--------|-----------|-----------|
| MW-50 | FOLD | FOLD ✓ HIGH | FOLD ✓ HIGH |
| d8886 | BET | BET ✓ HIGH | BET ✓ MED |
| d3688 | CHECK | **BET ✗ MED** | CHECK ✓ HIGH |
| d9556 | CHECK | **BET ✗ HIGH** | **BET ✗ HIGH** |
| d3178 | BET | **CHECK ✗ HIGH** | **CHECK ✗ HIGH** |

**Action correctness: 5/10 (50%)** — coin flip without seeding.

## Three structural failure patterns identified

Each on hands v3.2 specifically built rule-overrides for:

1. **d9556 systematic (both labellers wrong, both confident HIGH):** Cited `range_balance` then reasoned away from it. Invoked KB Example 4 ("monsters must bet 3-way") but missed Example 4 is IP — this hand is OOP on paired-low where range-tipping is the GTO concern.

2. **d3178 systematic (both labellers wrong, both confident HIGH):** Reasoned toward "OOP + max danger + 83% TP+ = pot control." Missed v3.2's river-checked-to override: hero's CO range must bet KK/QQ/AK as value, and AA must come along to balance the bet range — checking AA tips hero's checking range as range-cap-revealing.

3. **d3688 inter-labeller variance (50/50 split):** Same prompt, opposite answers. A rationalised away dominated kicker; B engaged with it correctly. Coin flip on the spot v3.2 needed Rule 11 for.

**Common thread:** Labellers cite the right range concepts as vocabulary, then reason toward equity-extraction or composition-bucket selection, producing reasoning that *names* the balance/range-tipping concept while concluding against it.

## What worked

- **Easy hands (MW-50, d8886):** Strong inter-labeller agreement; correct action; calibrated confidence.
- **Composition reasoning:** When the answer requires "high villain TP+ → fold dominated kicker" or "high air + high worse_hand_pct → bet thin value," labellers reliably get it right.

## What didn't work

- **`teaching_flag` enum misused:** RANGE_DECISIVE applied indiscriminately (5/10 outputs); BALANCE_PROTECTION never applied (d9556 should have triggered it; tagged TRAP_HAND instead with wrong action).
- **Frequency tiers without solver:** "OFTEN / SOMETIMES / RARELY" map to "main play / occasional / rare" prose, not training signal.
- **Range balance specifically:** The layer where most v3.2 corrections live is also the layer labellers most reliably fail.

## Strategic decision

**Drop the structured-format / mixed-strategy approach.** Keep v3.2 rule-based protocol.

Rationale:
1. Labellers can't reliably produce range-balance reasoning at production scale (50% on hard hands without seeding).
2. The v3.2 procedural rules (Rule 11 paired-board exception, KB §1.7 OVERRIDE, river-checked-to carve-out) are not shortcuts — they are solver-corrected guards that labellers consistently fail to derive independently.
3. Labellers' range-concept *vocabulary* is rich; their range-concept *reasoning* lands in the wrong action half the time on the hands that matter.

## Path forward (in priority order)

### 1. Corpus revision is the next blocker (architect + gto-expert)

Current pilot 100-hand corpus (Build C v1.0.1):
- 97/100 hands have `facing_bet=0` → opener decisions only
- 0 RAISE labels possible on most of corpus (no facing bet to raise)
- 1 CALL label across 500 Protocol A labels
- The v3.2 reversal hands (d3688/d9556/MW-39/d3178) are CALIBRATION hands, NOT in the 100-hand pilot corpus

This means the 500 labels currently on master at `4bce49f` test labelling consistency on a narrow opener-decision distribution — they do NOT exercise range logic at the depth Owner asked about.

**Required corpus characteristics for range-logic teaching:**
- Action diversity: facing-bet decisions (CALL/RAISE/FOLD candidates) at meaningful frequency
- Range-decisive hand inclusion: spots where surface features mislead and range positioning resolves (TPWK on dangerous boards, dominated-kicker situations, paired boards with capped ranges)
- Balance-protection coverage: spots where GTO mixing exists (paired-low boards OOP, range-tipping textures)
- Solver-verified anchors: hands where the labelling protocol's rule-overrides are testable

**Proposed action:** architect agent reviews Build C v1.0.1 corpus design + pilot spec; gto-expert audits action-distribution coverage against the hand-class taxonomy that v3.2 protocol's rules target. Output: corpus revision plan or supplement-with-additional-hands plan.

### 2. Phase B labelling resumes ONLY on revised corpus

- Phase B Protocol A labels at `4bce49f` (500 labels) are committed — preserved for now; may be superseded by a revised-corpus run
- Phase B Protocol B labellers were killed earlier (no Protocol B labels exist)
- Phase B Protocol C never dispatched
- **Do not resume Phase B mass labelling on the current opener-heavy corpus.**

### 3. Teaching layer extracts range concepts from v3.2 reasoning text

The Protocol A v3.2 labels already cite range concepts in their `reasoning` field (Rule 11 paired-board exception, KB §1.7 OVERRIDE, dominated kicker, range advantage, etc.). The teaching system can:
- Parse reasoning prose for named concepts
- Surface RANGE_TRAP / DOMINATED_KICKER / BALANCE_PROTECTION moments as teaching examples
- Activate range-concept lessons only on spots where range matters (per parsed reasoning)

This avoids depending on labellers to self-classify (which they can't do reliably) and instead lets the protocol-driven labels serve double duty: train the student model on primary action + provide reasoning text the teaching layer mines.

### 4. Architecture decision deferred until corpus is right

The user's question "is the architecture able to consume mixed-strategy / alternative-action labels?" is downstream of corpus. With single-action labels (v3.2 protocol) the existing classification architecture works. Mixed-strategy isn't viable at scale anyway (labellers can't produce reliable frequency tiers without solver). Architecture stays single-action classification.

## Cost spent on research

- 3 scaffolded probes (d3688/MW-39/d9556): ~$15
- 2 leading-prompt structured output tests (d9556/d3688): ~$10
- 10 unleading structured output tests (5 hands × 2 labellers): ~$30
- **Research total: ~$55**

Cumulative pilot-related spend (including Phase A + Phase B Protocol A): ~$95-110 of $200 cap.

## What is NOT changing

- Master state at `4bce49f` (Phase B Protocol A labels) — preserved
- v3.2 protocol — sealed, no revision
- Calibration anchors and grading rubric — unchanged
- v3.2 GO from A.7 — still holds

## What IS changing

- Phase B Protocol B/C dispatch — INDEFINITELY HELD pending corpus revision
- Mixed-strategy / alternative-action label format — REJECTED based on this research
- Corpus design — flagged for architect + gto-expert review as next priority

## Action items

**Owner:**
- Decision check on the corpus revision path: supplement vs rebuild
- Authorize architect + gto-expert dispatch for corpus audit when ready
- (No urgency — pilot is paused, no spend in flight)

**Orchestrator (me):**
- This decision comm is the ship of conclusions
- Stop further autonomous building — the orchestrator-as-builder antipattern was the failure mode flagged earlier today
- Hold for owner direction before any agent dispatches

**Pilot Orchestrator:**
- Released; no active responsibility

**QC stream:**
- May audit this decision comm
- No active labelling to monitor

## References

- Phase B Protocol A labels (preserved, possibly superseded): `4bce49f` (PR #50)
- Phase B re-dispatch comm: `57d92db` (PR #49)
- Phase B BLOCKED comm (pre-Option-1): `7d5467b`
- A.7 GO at: `903c5c9`
- v3.2 protocol seal: `42cace2` (PR #47)
- Owner's reframing message (excerpted from session): *"we want to be able to teach range logic, we cant do that if labelers dont use it. i am also not sure if experts udnerstand rangel ogic. it is broad, complex and situationally different. it needs to be researched and understood."*
- Memory: `feedback_quality_default_no_ask.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_solver_vs_expert_labels.md`, `feedback_attention_flags_when_features_change.md`, `feedback_preflop_geometry_vs_postflop_composition.md`

**Status: STRATEGIC DECISION CAPTURED. PILOT PAUSED. CORPUS REVISION IS THE NEXT BLOCKER. AWAITING OWNER DIRECTION.**
