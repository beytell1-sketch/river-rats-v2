---
date: 2026-04-26
from: A.8 static prompt audit (orchestrator-dispatched gto-expert)
to: Main terminal (orchestrator) · Owner · Pilot Orchestrator
re: Static range-reasoning audit on Protocol B + C + v3.1 source
status: AUDIT — synthesis pending orchestrator
verdict: MINOR_ISSUES
---

# A.8 — Static Prompt Audit

## Verdict: MINOR_ISSUES

**Bottom line:** Range semantics (1.0 = top, 0.0 = bottom) are
**internally consistent** across all three artifacts at the level of
the canonical feature description and DO NOT Rule 10. There are NO
internal HRP semantic contradictions. Cross-protocol convergence on
the 5 shared example structures (B-Examples 1-5 vs C-Examples 1-5)
is preserved on the action label, with B-Example 4 and C-Example 4
showing an INTENDED divergence (single-action vs MIXED label) that
the convergence checker explicitly classifies as convergent.

The findings below surface 3 MINOR coherence issues rooted in
**under-use** of HRP and absent hero-side range-composition
features, plus 2 NIT-level documentation drifts. None of these
falsify the protocols' range-placement reasoning, but they DO
narrow the hero range-placement signal to a single feature (#49)
plus implicit hand-class judgment, which weakens range-placement
robustness when the rebuild trains on the same data.

The verdict is MINOR_ISSUES (not CLEAN) because:

1. Protocol B's "Range-mass axis" cites a phantom feature
   (`hero_top_pair_plus_pct`) that does NOT exist in the
   54+1+4=59-feature contract. Labellers reading this will either
   skip the axis silently or hallucinate values for it.
2. Protocol B and Protocol C bodies make ZERO direct use of HRP
   in their reasoning steps; HRP only appears via the verbatim
   v3.1-inlined Feature table and DO NOT Rule 10. Range placement
   in the body of B/C reasons from `worse_hand_pct`, hand-class
   bucket, and composition slices, NOT from HRP. This is fine on
   its own but means there is no positive guidance on how
   labellers should consume HRP in B/C — they fall back to v3.1
   Step 2's "Hero's range position" guidance, which v3.1 line
   233-234 frames correctly (1.0 top, 0.0 bottom).
3. v3.1 still names HRP as a default PRIMARY feature for
   CALL/FOLD/BET/RAISE/CHECK in Step 5 feature_attention defaults
   (lines 419-428). The B/C bodies do NOT echo this; B/C labellers
   inherit it via the verbatim-inlined feature description but
   never engage it in the worked examples (none of the 10 worked
   examples cite HRP in feature_attention).

The verdict is NOT MAJOR because none of the protocols treat HRP
inconsistently with itself, none of them say "1.0 = bottom"
anywhere, and the worked examples that touch range placement
(MW-30 shape in B-Ex2 / C-Ex2; LITMUS_KQ shape in B-Ex3 / C-Ex3)
all reason from `worse_hand_pct` and composition slices in a
direction consistent with HRP semantics. The inconsistency would
be MAJOR if a worked example said "hero is bottom of range
because HRP=1.0" or similar; nothing of that nature exists.

---

## S1 — HRP usage consistency

### Observations

**v3.1 (`prompts/gto_labeller_v3.1.md`):** HRP is referenced 6 times.

- L231-234: Step 2 "Hero's range position" — semantics stated
  explicitly as "1.0 = top of range, 0.0 = bottom".
- L404: bucket-specific mandatory feature for `medium_made`.
- L419: feature_attention default for CALL/FOLD.
- L423: feature_attention default for BET/RAISE.
- L428: feature_attention default for CHECK.
- L491: 54-feature table row #49 — "Where hero sits in own range
  (1.0 = top)".
- L637-647: DO NOT Rule 10 — full HRP=0.00 test-harness artifact
  warning.

All six references are consistent: 1.0 = top, 0.0 = bottom; HRP
is a feature you consume in the bucket-first reasoning; HRP=0.00
is suspect when hero holds a visibly strong hand. **No
contradiction.**

**Protocol B pilot (`prompts/protocol_b_composition_first_v1_0_pilot.md`):**
HRP is referenced 4 times — all inside verbatim-inlined v3.1 blocks.

- L23, L107, L444 (frontmatter / build provenance / section header).
- L505: feature table row #49 verbatim from v3.1.
- L514, L533, L1353: `board_adjusted_hrp` (feature 55) note.
- L593-602: DO NOT Rule 10 verbatim from v3.1.

**Protocol B's body — no Step 1/2/3/4 reasoning step references
HRP.** The composition-first reasoning chain reads villain
composition only; range placement is handled implicitly via the
"Range-mass axis" in Step 2 (which references the phantom
`hero_top_pair_plus_pct` — see S5).

**Protocol C pilot (`prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`):**
HRP is referenced 4 times — all inside verbatim-inlined v3.1 blocks
or frontmatter.

- L743: feature table row #49 verbatim from v3.1.
- L752, L771: `board_adjusted_hrp` note.
- L831-840: DO NOT Rule 10 verbatim from v3.1.

**Protocol C's body — no Step 1/2/3/4/5 reasoning step references
HRP.** The adversarial-elimination chain reasons from
worse_hand_pct, composition slices, equity-vs-pot-odds, position,
and SPR. Range placement is implicit via hand-class + worse_hand_pct.

### Verdict on S1

The semantics 1.0 = top / 0.0 = bottom are **consistent in every
place HRP appears**, in every artifact. There are NO contradictions
where one section treats HRP differently from another.

The MINOR issue is **under-use, not contradiction**: B/C bodies
do not actively engage HRP in their reasoning steps, only inherit
it via the verbatim-inlined v3.1 sections. A labeller who follows
the B/C body literally will reason about range placement entirely
from hand-class + composition + worse_hand_pct, never from HRP.
This is a coherence issue (the inherited feature_attention
defaults at v3.1 L419-428 list HRP as a default PRIMARY for
all 5 actions, but the B/C examples never tag it).

| File:line | Reference | Semantic |
|-----------|-----------|----------|
| v3.1 L231-234 | Step 2 "Hero's range position" | 1.0 top / 0.0 bottom |
| v3.1 L404 | medium_made mandatory | (consume HRP) |
| v3.1 L419 | CALL/FOLD default | PRIMARY |
| v3.1 L423 | BET/RAISE default | PRIMARY |
| v3.1 L428 | CHECK default | PRIMARY |
| v3.1 L491 | feature table #49 | "1.0 = top" |
| v3.1 L637-647 | DO NOT Rule 10 | HRP=0.00 artifact warning |
| Protocol B L505 | inlined feature table | "1.0 = top" |
| Protocol B L593-602 | inlined DO NOT Rule 10 | HRP=0.00 artifact warning |
| Protocol C L743 | inlined feature table | "1.0 = top" |
| Protocol C L831-840 | inlined DO NOT Rule 10 | HRP=0.00 artifact warning |

**S1 Status: CLEAN on semantic consistency. MINOR on under-use in
B/C bodies — labellers inherit HRP via v3.1 sections but never see
worked B/C reasoning that engages HRP.**

---

## S2 — DO NOT Rule 10 application

### Observations

DO NOT Rule 10 (HRP=0.00 test-harness artifact warning) is
present **verbatim** in:

- v3.1 L637-647 (canonical source).
- Protocol B pilot L593-602 (verbatim-inlined block, marked as
  "End verbatim block").
- Protocol C pilot L831-840 (verbatim-inlined block, marked as
  "End verbatim block").

All three reproductions are **byte-identical** in semantic content
(the `[v3 addition §3.B]` tag, the HRP_INVESTIGATION_2026-04-15.md
reference, the visibility-of-strong-hand override, and the
"composition quad" fallback are all present in all three).

### Cross-referencing check

The audit task asks: is Rule 10 cross-referenced in every place
HRP is used? Or is HRP referenced elsewhere without the artifact
caveat?

**v3.1:**
- L231-234 (Step 2 Hero's range position) does NOT cross-reference
  Rule 10. **Minor finding** — a labeller reading Step 2 does not
  see the artifact caveat unless they also read the DO NOT Rules
  section. The flow `Step 1 → Step 2 → Step 3 → Step 4 → Step 5
  → DO NOT Rules` means the labeller reads Step 2 first; reads the
  artifact caveat later. In practice this works (labellers read
  the whole prompt), but it's a coherence weakness.
- L404 (medium_made mandatory feature list) does NOT cross-reference
  Rule 10. Same minor finding.
- L419, L423, L428 (feature_attention defaults) do NOT
  cross-reference Rule 10. Same minor finding.

**Protocol B pilot:** B's body does not reference HRP at all
outside the verbatim-inlined sections, so cross-referencing is
moot for the body. The verbatim feature table (L505) and DO NOT
Rule 10 (L593-602) co-exist in the same file. **No mis-reference.**

**Protocol C pilot:** Same as Protocol B — body does not reference
HRP outside verbatim-inlined sections. **No mis-reference.**

### Verdict on S2

DO NOT Rule 10 is correctly inlined verbatim in all three pilot
artifacts. The MINOR issue is in v3.1 itself: the Step 2 / L404 /
L419-428 references to HRP do not point to Rule 10. This is
inherited by B/C through the verbatim-inlined feature table.

This is the kind of coherence issue that production v3.1
shipped with — not introduced by the pilot artifacts.

**S2 Status: CLEAN on inheritance fidelity. MINOR on cross-
referencing in v3.1 (inherited).**

---

## S3 — Worked examples

### Examples per artifact

- v3.1: contains **no worked examples** in the body — examples
  are appended at runtime from `knowledge/three_way_gto.md`
  (per v3.1 L77-80). Out of scope for this static audit.
- Protocol B pilot: 5 worked examples (L868-1159).
- Protocol C pilot: 5 worked examples (L1153-1557).

### Protocol B Examples 1-5 — range-placement reasoning

**B-Example 1 (Mixed-medium-skewed, hero TPGK, BET small thin
value):**
- Range placement is implicit: "Hero TPGK is strong-medium hand
  class against this composition" (L893).
- HRP is **not cited** in the trace.
- Range-placement reasoning derives from hand-class (TPGK) +
  worse_hand_pct (0.66) + composition slices.
- Direction is consistent with HRP semantics: hero is in the upper
  portion of his own range on a J-high rainbow turn (TPGK is among
  the stronger combos in CO's pre-flop opening range that connects
  here), which is the correct direction for thin-value-bet.
- **No HRP=0.00 artifact concern** — hero hand is visibly strong
  (TPGK with K kicker), Rule 10 doesn't apply.

**B-Example 2 (Heavy-TP+ MW-30 shape, weak-made, CALL):**
- Range placement is implicit: "Hero pocket-tens is weak-made vs
  Kxx (second pair, unimproved overpair-below-top)" (L957).
- HRP is **not cited** in the trace.
- Range-placement reasoning derives from composition-derived
  equity (0.40 from beatable-slice 0.59) + bucket label
  (weak_made).
- Direction is consistent with HRP semantics: TT on Kxx is in
  the **middle to lower** part of BB's calling range (BB's range
  contains many K-x hands as well as small pairs and connectors;
  TT is a borderline made hand that falls in the middle-to-bottom
  of the calling range on this board), which makes the CALL action
  consistent with "I'm bottom-ish, my equity comes from beating
  villain's air/draws/medium, not from being top of my range."
- **No HRP=0.00 artifact concern** — hero hand is a pair (visible
  showdown value), Rule 10 doesn't trigger.

**B-Example 3 (Heavy-draws LITMUS_KQ shape, strong-made, BET
large):**
- Range placement is implicit: "Hero KQ is strong-made (TPGK)"
  (L1027).
- HRP is **not cited** in the trace.
- Range-placement reasoning derives from worse_hand_pct (0.85) +
  bucket (strong_made) + composition.
- Direction consistent: KQ on K-T-3ss is **top** of BTN's
  preflop range that connects here; BET large is the
  range-placement-consistent action.
- **No HRP=0.00 artifact concern.**

**B-Example 4 (d8886 mixed shape, OOP donk, BET small):**
- Range placement is implicit: "Hero TPGK on J-high two-tone flop"
  + "with TPGK and IP-first-to-act on a flop the BB can lead small"
  (L1075-1078).
- HRP is **not cited** in the trace.
- Direction consistent with HRP: TPGK on J-high two-tone is upper
  portion of BB's calling range that connects, which is consistent
  with the donk-lead-small action.
- **No HRP=0.00 artifact concern.**

**Note on B-Ex4 inconsistency:** L1078 says "and IP-first-to-act
on a flop the BB can lead small" — but BB is OOP, not IP. This is
a typo / misuse of "IP" (BB is structurally OOP relative to BTN
and CO). It's an EXAMPLE INTERNAL INCONSISTENCY but does not
affect HRP semantics; flagged as MINOR documentation drift in S3.

**B-Example 5 (per-villain post-fold, TPWK with nut blocker, BET
small):**
- Range placement is implicit: "Hero A8 = TPWK + Ac nut-flush
  blocker" (L1126).
- HRP is **not cited** in the trace.
- Direction consistent: A8 with the Ac is upper portion of HJ's
  preflop range that connects here on the 4th-club turn (the Ac
  is critical) — BET small for thin value + denial.
- **No HRP=0.00 artifact concern.**

### Protocol C Examples 1-5 — range-placement reasoning

**C-Example 1 (Heavy-air, TPGK on dry rainbow, BET_66):**
- Range placement is implicit: "Hero's TPGK has equity ~0.78 vs
  the 0.85 beatable slice" (L1175).
- HRP is **not cited** in the elimination trail.
- Direction consistent with HRP: TPGK on Q-high dry rainbow is
  top of BTN's range; BET_66 is the range-placement-consistent
  action.
- **No HRP=0.00 artifact concern.**

**C-Example 2 (MW-30 shape, weak-made, CALL):**
- Range placement is implicit: "Hero TT beats medium (0.24) +
  draws (0.20) + air (0.15) = 0.59 of villain's range" (L1264).
- HRP is **not cited** in the elimination trail.
- Cross-protocol parity with B-Example 2: same MW-30 anchor; same
  CALL action; both protocols derive CALL via different reasoning
  paths.
- **No HRP=0.00 artifact concern.**

**C-Example 3 (LITMUS_KQ shape, strong-made, BET_66):**
- Range placement is implicit: "hero's TPGK with K kicker is the
  top of the bet-66 range" (L1376).
- HRP is **not cited** in the elimination trail.
- Cross-protocol parity with B-Example 3: same shape; same BET
  large action.
- **No HRP=0.00 artifact concern.**

**C-Example 4 (d8886 mixed shape, OOP, MIXED BET_25/CHECK):**
- Range placement is implicit: "Hero QcJc is TPGK on J-high
  two-tone with backdoor flush draw. Worse_hand_pct ~0.78"
  (L1424-1425).
- HRP is **not cited** in the elimination trail.
- Cross-protocol comparison vs B-Example 4: B picks single BET,
  C picks MIXED with primary BET. Direction agrees; mix-vs-single
  differs (intentional design — Protocol C preserves solver-mix
  signal).
- **No HRP=0.00 artifact concern.**

**C-Example 5 (per-villain post-fold, TPWK with nut blocker,
BET_33):**
- Range placement is implicit: "Hero A8 = TPWK + Ac nut-flush
  blocker. Worse_hand_pct ~0.66" (L1507).
- HRP is **not cited** in the elimination trail.
- Cross-protocol parity with B-Example 5: same shape; same BET
  small action.
- **No HRP=0.00 artifact concern.**

### Findings on S3

1. **All 10 examples (B 1-5 + C 1-5) reason about range placement
   IMPLICITLY via hand-class + worse_hand_pct + composition
   slices, NEVER via HRP directly.** This is consistent within
   each protocol and across protocols, but it means the worked
   examples never demonstrate HOW to consume HRP, never engage
   DO NOT Rule 10, and never tag HRP in feature_attention. A
   labeller who studies these examples and applies the patterns
   to a hand where HRP=0.00 alongside an obviously strong hand
   will not have seen Rule 10 in action.

2. **Direction-consistency check passes:** in every example, the
   implicit range placement (top / middle / bottom) matches the
   direction HRP would assign. No example reverses the
   semantics.

3. **B-Example 4 has a minor "IP-first-to-act" wording issue
   (L1078)** — BB is OOP, not IP. This is a typo / misuse of
   position vocabulary; does NOT affect HRP semantics. Logged
   as F4 NIT below.

4. **DO NOT Rule 10 is never exercised in any worked example.**
   None of the 10 examples show a hand where HRP=0.00 alongside
   an obviously strong hand. Pilot labellers will encounter the
   rule only via the verbatim-inlined DO NOT block; they will
   not have seen it applied.

**S3 Status: CLEAN on direction-consistency. MINOR on worked-
example coverage of HRP / Rule 10 (no example exercises it).
NIT on B-Example 4 IP/OOP wording.**

---

## S4 — Cross-protocol consistency

### Shared example structures

The Stage 4 plan requires inter-protocol convergence on the same
target action. B-Examples 2-5 and C-Examples 2-5 share spots
with each other (cross-protocol pairs) by design. The audit
question is: do they converge?

| Example | Spot | B action | C action | Convergent? |
|---------|------|----------|----------|-------------|
| B-Ex2 / C-Ex2 | MW-30 (TT on Kxx vs bet+call) | CALL | CALL | YES |
| B-Ex3 / C-Ex3 | LITMUS_KQ (KQ on KTx ss two-tone) | BET ~66% | BET_66 | YES |
| B-Ex4 / C-Ex4 | d8886 (QcJc on 2s5dJd OOP donk) | BET ~33% | MIXED [BET_25, CHECK] primary BET_25 | CONVERGENT-by-design |
| B-Ex5 / C-Ex5 | A8 on 6c8c2d3c (post-fold) | BET ~33% | BET_33 | YES |

**B-Ex1 and C-Ex1 are NOT cross-protocol pairs** (different spots
by design — B-Ex1 is the mixed-medium TPGK turn; C-Ex1 is the
heavy-air Q-high TPGK flop). No divergence to flag.

### Range-placement classification consistency

For the 4 cross-protocol pairs (B-Ex2/C-Ex2, B-Ex3/C-Ex3,
B-Ex4/C-Ex4, B-Ex5/C-Ex5), do B and C arrive at the same
range-placement classification?

**B-Ex2 / C-Ex2 (MW-30):** Both implicitly classify TT as
weak-made / middle-to-lower-portion-of-range relative to villain's
heavy-TP+ continuing range. B uses "weak_made" bucket explicitly
(L985); C does not name a bucket but the case-against arguments
treat TT as "weak-made hand vs heavy-TP+ shape" (L1274). **Same
classification.**

**B-Ex3 / C-Ex3 (LITMUS_KQ):** Both implicitly classify KQ as
strong-made / top-of-range. B uses "strong_made" bucket
(L1042); C says "hero's TPGK with K kicker is the top of the
bet-66 range" (L1376). **Same classification.**

**B-Ex4 / C-Ex4 (d8886):** Both implicitly classify QcJc as
TPGK / upper-medium. B uses "medium_made" bucket given two-tone
draw threats (L1083); C says "TPGK on J-high two-tone with
backdoor flush draw" (L1424). **Same classification.** B picks
BET single; C picks MIXED — but the direction (BET) is the
same primary action.

**B-Ex5 / C-Ex5 (post-fold A8):** Both implicitly classify A8
as TPWK + nut-flush blocker. B uses "medium_made or weak_made"
(L1141); C says "TPWK + Ac nut-flush blocker" (L1507). **Same
classification.** Both pick BET ~33% with HIGH confidence.

### Action label convergence

| Pair | B action | C action | Match? |
|------|----------|----------|--------|
| Ex2 | CALL | CALL | YES |
| Ex3 | BET 66% | BET_66 | YES |
| Ex4 | BET 33% | MIXED, primary BET_25 | DIRECTIONAL |
| Ex5 | BET 33% | BET_33 | YES |

The Ex4 case is the only "divergence" and it is **intentional**
per Protocol C's MIXED handling design (L617-621): the convergence
checker treats MIXED [BET_25, CHECK] + Protocol B's BET as
**convergent** because B's single answer is in C's MIXED pair.

### Sizing nit

B-Ex3 says "BET 66%" (L1042); C-Ex3 says "BET_66" — same. B-Ex4
says "BET small (~33% pot)" (L1090); C-Ex4 primary is "BET_25"
(L1469). **Sizing direction agrees** (both small donk leads on
flop) but the exact size differs by one solver-aligned step:
B writes "33% pot" but flop solver-aligned sizings are 25% / 66%
per `feedback_solver_aligned_sizing.md`. This is a NIT — B-Ex4
should write "BET_25" or "BET 25%" to match the canonical sizing.

### Verdict on S4

**Cross-protocol convergence is preserved on all 4 shared
examples.** Range-placement classification is consistent in all
4 pairs. Action labels match (or are convergent-by-design for
Ex4 via the MIXED handling rule).

The MINOR issue is the **B-Ex4 sizing wording**: "33% pot" on
flop should be "25% pot" or "66% pot" per solver-aligned sizings.
B-Ex1 also writes "BET ~33% pot, ~3bb into 9.5bb" on a TURN
(L906) where the canonical turn sizing IS 33%, so this is fine.
But B-Ex4 is a FLOP and writes 33% (L1090) — that's a
non-canonical flop sizing.

**S4 Status: CLEAN on cross-protocol action convergence and
range-placement classification. NIT on B-Ex4 flop sizing wording.**

---

## S5 — Feature semantics

### The features the audit asks about

| Feature | Real or phantom? | Source |
|---------|------------------|--------|
| `hero_range_percentile` | REAL (#49) | v3.1 L491; production `feature_keys.py` L73 |
| `board_adjusted_hrp` | REAL (#55, held back per Stage 3.5) | v3.1 not in 54-table; pilot artifacts L514 / L752; `feature_keys.py` L84 |
| `hero_top_pair_plus_pct` | **PHANTOM** | Only in B-pilot L284 + B-design L265; NOT in `feature_keys.py` |
| `hero_overpair_pct` | **PHANTOM** | Not referenced anywhere |
| `hero_two_pair_pct` | **PHANTOM** | Not referenced anywhere |
| `hero_set_pct` | **PHANTOM** | Not referenced anywhere |
| `villain_top_pair_plus_pct` | REAL (#39) | v3.1 L481 |
| `villain_medium_made_pct` | REAL (#54) | v3.1 L496 |
| `villain_draw_pct` | REAL (#40) | v3.1 L482 |
| `villain_air_pct` | REAL (#41) | v3.1 L483 |

### Findings

**F-S5-1: Phantom hero composition features in Protocol B
(MEDIUM).** Protocol B pilot L283-285:

> - **Range-mass axis:** what fraction of hero's own range
>   (`hero_top_pair_plus_pct` etc. if available) is in the same
>   category as villain's? Used for range-vs-range balance.

`hero_top_pair_plus_pct` does NOT exist in the 54-feature v3.1
vector, the held-back feature 55, OR the 4 v2.4 P1 blockers
(56-59). Verified by:

- v3.1 feature table L441-496: no hero_top_pair_plus_pct.
- Pilot Feature 55 note L514-519: `board_adjusted_hrp` only.
- Pilot v2.4 P1 blocker table L527-530: only `nut_flush_block`,
  `flush_draw_block_pct`, `straight_draw_block_pct`,
  `nut_made_block_pct`.
- Production `river-rats-core/feature_keys.py` `hero` grep:
  HERO_POSITION, HERO_RANGE_PERCENTILE,
  `_board_adjusted_hero_range_percentile`,
  META_HERO_CARDS, META_HERO_POS_RAW. **No hero composition
  pcts.**

The "if available" caveat in L284 means this is technically
guarded — labellers should know the feature is absent and skip
the Range-mass axis. But this is fragile:

- A labeller may hallucinate the feature value (LLMs do this
  when prompted to read a named feature).
- The Range-mass axis is part of Step 2's situation
  classification (3 axes: equity-vs-range, realisable-equity,
  range-mass). Skipping one axis silently weakens Step 2
  reasoning.
- The fix is either (a) remove the Range-mass axis paragraph,
  (b) add an explicit "this feature is not currently available;
  skip this axis" note, or (c) replace with a hand-class-based
  proxy ("hero's bucket relative to a typical bucket distribution
  for hero's preflop range").

**F-S5-2: Same phantom in Protocol B design artifact
(MEDIUM, inherited).** `prompts/protocol_b_composition_first_v1_0.md`
L265 has the same text. The design artifact is the source of the
pilot artifact's body, so this is one issue manifesting in two
places.

**F-S5-3: Real features semantics consistency (CLEAN).** The 4
villain composition features have consistent semantics across
all three artifacts:

- v3.1 L481, L482, L483, L496: villain_top_pair_plus_pct,
  villain_draw_pct, villain_air_pct, villain_medium_made_pct
  with the standard "% of villain range that is X" semantic.
- B-pilot L495-497, L510 (verbatim-inlined): same semantics.
- C-pilot L733-735, L748 (verbatim-inlined): same semantics.

No semantic drift. No "0.0 = TP+ heavy" or similar reversals.

**F-S5-4: `board_adjusted_hrp` semantic consistency (CLEAN).**

- v3.1 does not list this feature in the 54-table (correctly
  documented as v3.1 going up to 54 only, with feature 55 added
  later per Stage 3.5).
- B-pilot L514-519 / C-pilot L752-757 both document
  board_adjusted_hrp identically as "feature 55, held back per
  Stage 3.5 manifest, present in `gto_model.py` FEATURE_COLUMNS
  (length 55) at master HEAD, treated as 'known absent' by
  Stage 3.5 ship, v2.4+ unholds for labellers consuming the
  full 55-feature contract."
- The semantic (board-adjusted version of HRP, presumably with
  the same 1.0 = top / 0.0 = bottom convention) is **NOT
  explicitly stated**. This is an inheritance gap — labellers
  reading "board-adjusted HRP" need to assume the same semantic
  as HRP. **NIT — should be made explicit.**

### S5 Verdict

| ID | Severity | File:line | Description |
|----|----------|-----------|-------------|
| F-S5-1 | MEDIUM | B-pilot L284 | Phantom feature `hero_top_pair_plus_pct` cited in Range-mass axis; no such feature exists in the 59-feature contract |
| F-S5-2 | MEDIUM (inherited) | B-design L265 | Same phantom in design artifact (source of F-S5-1) |
| F-S5-3 | CLEAN | n/a | Real villain composition features semantics are consistent across A/B/C |
| F-S5-4 | NIT | B-pilot L514, C-pilot L752 | `board_adjusted_hrp` semantic (1.0 = top?) is not explicitly stated |

**S5 Status: MINOR_ISSUES (1 MEDIUM phantom feature reference,
inherited from design artifact; 1 NIT on board_adjusted_hrp
semantic).**

---

## S6 — Mixed-strategy treatment

### v3.1

v3.1 does NOT have a dedicated mixed-strategy section. Mixed-
strategy reasoning is handled implicitly:

- Calibration anchors d8886 and d8963 are explicitly
  mixed-strategy spots (v3.1 L671-679); the prompt says "Pass:
  action = BET (or difficulty = 3 with BET as primary alternative
  explicitly evaluated)" or "difficulty = 3 with both BET and
  CHECK explicitly evaluated and mixed-strategy nature noted".
- Step 5 difficulty=3 (Boundary) is the mechanism: "A strong
  player might mix between them. You must explicitly evaluate
  at least 2 alternatives" (v3.1 L290-292).

This is **frequency-from-difficulty**, not
**frequency-from-range-placement**. The audit asks for the
latter ("AK is top-25% of my range vs villain's composition,
so value-bet 75% / check-to-induce 25%"). v3.1 has none of
this.

### Protocol B pilot

Protocol B does NOT have a dedicated mixed-strategy section.
Mixed-strategy reasoning is handled via:

- B-Example 4 (d8886) Outcome 4B with `4B_anchor_match_override`
  picking a single action (BET) per the anchor's expert label
  (L1090-1094). The "solver mixed 50/50" is acknowledged in the
  reasoning trace but the labeller still picks one action.

This is **single-action label even when solver is mixed** —
which is correct for the Stage 4 cross-protocol convergence
target (Protocols A and B always emit single-action labels per
the convergence checker's input contract).

Frequency-from-range-placement reasoning is **NOT present** in
Protocol B's body.

### Protocol C pilot

Protocol C has a **dedicated §"Mixed-strategy GTO answer
handling" section** (L544-628). Key features:

- Option (a) chosen: when solver is mixed and case-against
  profiles are comparable, label as MIXED with `mixed_action_pair`
  + `mixed_confidence_band` + `primary_action`.
- C-Example 4 exercises this: MIXED [BET_25, CHECK],
  confidence_band [0.40, 0.60], primary BET_25 (L1467-1473).
- Cross-protocol comparison rule (L616-621): when C labels MIXED
  and A/B label single, if A/B's single is in C's MIXED pair,
  scored convergent.

Protocol C also has anti-pattern #6 "Ignoring villain's mixed-
strategy responses" (L1640-1651) — labellers must specify response
frequencies in the case-against, not pure-strategy assumptions.

But: frequency-from-range-placement reasoning ("AK is top-25% of
my range, so value-bet 75% / check-to-induce 25%") is **NOT
present** in Protocol C either. C's mixed-strategy handling is
**solver-mixed-pair → MIXED label**, not
**range-placement → frequency**.

### S6 Verdict

**Frequency-from-range-placement reasoning is missing from all
three artifacts.**

This is consistent across the protocols (no internal
inconsistency), but it means range placement is treated as a
**single-action driver**, not a **frequency driver**. A hand
where HRP=0.75 (top quartile of hero's range) and the GTO answer
is 70% BET / 30% CHECK is currently labelled as either:

- A single BET (Protocols A, B), with difficulty=3 acknowledging
  the mix.
- A MIXED label (Protocol C) if the case-against profiles are
  comparable AND the pair is recognised.

Neither protocol uses HRP to GENERATE the frequency. Frequency
is either pre-decided by the calibration anchor, derived from
the solver, or surfaced via the MIXED label.

**This is a coherence concern** but not a contradiction. The
question for owner / pilot orchestrator is whether Stage 4 needs
frequency-from-range-placement, OR whether the current
single-action + MIXED approach is sufficient. If the latter,
this finding can be downgraded to "documented as out-of-scope
for v1.0.1-pilot, to revisit in v1.1+".

| ID | Severity | File:line | Description |
|----|----------|-----------|-------------|
| F-S6-1 | MINOR | B-pilot, C-pilot, v3.1 | No frequency-from-range-placement reasoning in any artifact; range placement is a single-action driver, not a frequency driver |
| F-S6-2 | CLEAN | n/a | Mixed-strategy handling is consistent within each protocol (B uses single-action + difficulty; C uses MIXED label) |

**S6 Status: MINOR_ISSUES — gap in frequency-from-range-placement
reasoning across all three protocols. Consistent gap, not a
contradiction.**

---

## S7 — Bottom-up vs top-down reasoning

### Definitions (per audit task)

- **Top-down:** start from "what does my range look like overall"
  then place this specific hand.
- **Bottom-up:** start from "this specific hand has X equity" then
  ask where it sits in the range.

### v3.1 reasoning order

v3.1 Step 1 "CLASSIFY THE HAND" (L170-204) starts from the
**specific hand** ("Hero holds 8h8c on board 8d 5s 2c. Flopped
set"). This is **bottom-up**.

v3.1 Step 2 "READ THE SITUATION" (L207-247) reads villain ranges
(top-down on villain) AND "Hero's range position" (top-down on
hero, L231-234). This is a **mix**.

v3.1 is therefore **bottom-up-then-top-down**: classify the hand
first (bottom-up), then situate it in ranges (top-down).

### Protocol B reasoning order

B-Step 1 (L184-214) reads villain composition pcts FIRST. This
is **top-down on villain**.

B-Step 2 (L218-285) classifies hero's situation along three
axes:
- Equity-vs-range (top-down): "approximately how much equity
  does hero's hand class realize against the composition?"
- Realisable-equity (top-down on position).
- Range-mass (top-down on hero — but the cited feature is
  phantom, see S5).

B-Step 3 (L289-309) derives candidate actions from the
composition-derived situation. The hand-class is a feature (cited
in L307: "hero's hand-strength category (which IS a feature:
`hand_class`, `made_hand_strength`, etc.)").

B-Step 4 (L311-331) cross-checks against the bucket taxonomy —
this is bottom-up (the bucket is a hand-class label).

**Protocol B is therefore top-down-first-then-bottom-up:**
composition + range-mass first (top-down), then bucket cross-check
(bottom-up). This is INVERTED relative to v3.1.

### Protocol C reasoning order

C-Step 1 (L183-308) enumerates feasible candidate actions —
**neither top-down nor bottom-up**, just enumeration.

C-Step 2 (L309-394) constructs the case-against each candidate.
Cases-against cite composition pcts (top-down) and hand-class
(bottom-up) freely. Templates at L342-389 mix both.

C-Step 3 (L396-501) tier-rates the cases-against — independent
of top-down vs bottom-up.

C-Step 4-5 (L502-541) eliminates and picks survivor.

**Protocol C is mixed throughout** — not committed to either
top-down or bottom-up; the case-against arguments use whichever
features are most relevant.

### Findings on S7

**F-S7-1: Protocol B is top-down-first; v3.1 is
bottom-up-first; Protocol C is mixed.** This is **a deliberate
design feature**, not a bug — the entire purpose of multiple
protocols is to vary the reasoning order to surface biases.
Protocol B's distinguishing feature is composition-first (L146-150).

**F-S7-2: Within each protocol, the reasoning order is
consistent.** Protocol B does not switch from top-down in Step 1
to bottom-up in Step 3 (Step 4 is the explicit cross-check; Step
3 is still composition-derived). Protocol C does not commit to
either, which is its design (adversarial elimination is
order-agnostic).

**F-S7-3: Mid-reasoning mixing concern (NIT).** Protocol B's
worked examples sometimes blend top-down and bottom-up:

- B-Ex2 (L957): "Hero pocket-tens is weak-made vs Kxx (second
  pair, unimproved overpair-below-top)." — bottom-up
  hand-classification embedded in Step 1's composition reading.
- B-Ex3 (L1027): "Hero TPGK (KQ on Ks-high) is strong-made;
  equity ~0.62, worse_hand_pct ~0.85" — same.

This is mid-reasoning mixing within a Step that is supposed to
be top-down (Step 2 situation reading). The labeller is reading
hand-class while reading composition. This is the
**bottom-up-disguised-as-top-down** failure mode that B's
Anti-pattern #1 (L1171-1183) explicitly forbids. The worked
examples themselves come close to violating Anti-pattern #1 —
they are technically allowed because hand-class is a feature
(per L306-308 carve-out: "the candidate action(s) come from
composition + hero's hand-strength category (which IS a feature:
`hand_class`, `made_hand_strength`, etc.) ONLY"), but the
reasoning trace blends both.

A strict reading of B's Anti-pattern #1:
> "I see TPGK on a J-high board, so bucket = medium_made →
> CHECK; let me check composition… yep, heavy-TP+ confirms."
> This is rule-first wearing composition clothing.

The B-Examples 2-5 do the inverse (composition first, then
hand-class) but the hand-class is named in Step 1/2, not just
Step 4. This is a borderline coherence issue — graded as NIT
because the protocol explicitly carves out `hand_class` /
`made_hand_strength` as features that may be read in Step 3.

### S7 Verdict

| ID | Severity | File:line | Description |
|----|----------|-----------|-------------|
| F-S7-1 | INFO | n/a | Reasoning order varies by design: v3.1 bottom-up-first; B top-down-first; C mixed. Within each protocol, internally consistent. |
| F-S7-2 | CLEAN | n/a | No mid-reasoning order-flipping within any protocol. |
| F-S7-3 | NIT | B-pilot Ex 2-5 | Worked examples blend hand-class into Step 1/2 composition reading — borderline against B's Anti-pattern #1, but technically allowed by L306-308 carve-out. |

**S7 Status: CLEAN on within-protocol consistency. NIT on
B-Examples blending hand-class into top-down Steps.**

---

## Findings summary

| ID | Severity | File:line | Description |
|----|----------|-----------|-------------|
| F-S1-1 | MINOR | B-pilot L505/593-602 + C-pilot L743/831-840 | HRP only appears in verbatim-inlined v3.1 sections in B/C pilots; no body reasoning step engages HRP, so labellers will not have seen HRP-driven range placement modelled in B/C |
| F-S2-1 | MINOR (inherited from v3.1) | v3.1 L231-234, L404, L419, L423, L428 | Step 2 / mandatory feature / feature_attention default references to HRP do not cross-reference DO NOT Rule 10 — labellers must read full prompt for the artifact caveat |
| F-S3-1 | MINOR | B-pilot L868-1159 + C-pilot L1153-1557 | None of the 10 worked examples cite HRP in their reasoning OR exercise DO NOT Rule 10 — labellers will not have seen Rule 10 applied |
| F-S3-2 | NIT | B-pilot L1078 | "and IP-first-to-act on a flop the BB can lead small" — BB is OOP, not IP; wording confusion |
| F-S4-1 | NIT | B-pilot L1090 | B-Ex4 says "BET small (~33% pot)" on a FLOP — flop solver-aligned sizings are 25%/66%, not 33%; mismatch with `feedback_solver_aligned_sizing.md` and with C-Ex4's "BET_25" |
| F-S5-1 | MEDIUM | B-pilot L284 | Phantom feature `hero_top_pair_plus_pct` cited in Range-mass axis — does NOT exist in 59-feature contract (54 v3.1 + 1 board_adjusted_hrp + 4 v2.4 P1 blockers); labellers may hallucinate values |
| F-S5-2 | MEDIUM (inherited) | B-design L265 | Same phantom in design artifact (source of pilot artifact's body); fix-forward should patch both |
| F-S5-3 | CLEAN | n/a | Real villain composition features (#39, #40, #41, #54) have consistent semantics across A/B/C |
| F-S5-4 | NIT | B-pilot L514 + C-pilot L752 | `board_adjusted_hrp` semantic (1.0 = top assumed by parallel to HRP) is not explicitly stated |
| F-S6-1 | MINOR | All three artifacts | No frequency-from-range-placement reasoning ("hand is top-25% of my range, so 75% bet / 25% check") in any prompt; range placement is a single-action driver |
| F-S6-2 | CLEAN | n/a | Mixed-strategy handling is internally consistent within each protocol (B: single-action + difficulty; C: MIXED label option (a)) |
| F-S7-1 | INFO | n/a | Reasoning order varies BY DESIGN: v3.1 bottom-up-first; B top-down-first; C mixed |
| F-S7-2 | CLEAN | n/a | No mid-reasoning order-flipping within any single protocol |
| F-S7-3 | NIT | B-pilot Ex 2-5 | Worked examples blend hand-class into top-down Steps 1/2 composition reading — borderline against B Anti-pattern #1 but technically permitted by L306-308 carve-out |

---

## Recommendation

**Verdict: MINOR_ISSUES.** Phase B mass labelling is **NOT
blocked by range-reasoning coherence concerns**, but the
following fix-forward items SHOULD land before 4500 labels
commit. None of them is a hard blocker; all are tractable.

### Fix-forward items (recommended pre-Phase B)

**Required (MEDIUM):**

1. **F-S5-1 + F-S5-2 (phantom hero composition feature):**
   Patch B-pilot L283-285 (and B-design L264-266). Three
   options, ranked by quality:
   - (a) **REMOVE** the Range-mass axis paragraph entirely; it
     is non-functional with no `hero_top_pair_plus_pct` etc.
     in the contract.
   - (b) **REPLACE** with an explicit "this axis is held until
     hero composition pcts ship in v2.5+; skip in v1.0.1-pilot."
   - (c) **REWRITE** to use a hand-class-derived proxy: "hero's
     bucket position (monster / strong_made / medium_made /
     weak_made / drawing / air) relative to a typical bucket
     distribution for hero's preflop range on this board".
     Most useful in the long run; most expensive to spec.

   Recommend (b) for Phase B (smallest fix-forward; preserves
   axis structure for v1.1+ rebuild) — see also feedback rule
   on slow/clean execution.

**Recommended (MINOR):**

2. **F-S1-1 + F-S3-1 (HRP under-use in B/C bodies):** Add an
   "HRP usage in Protocol B/C" subsection (1 paragraph each) in
   B-Step 4 and C-Step 5, explicitly noting that HRP and
   board_adjusted_hrp are inherited from v3.1 and SHOULD be
   tagged in feature_attention when the bucket-specific
   mandatory rule applies (medium_made bucket, per v3.1 L404).
   This patches the inheritance gap without re-architecting the
   reasoning order.

3. **F-S6-1 (frequency-from-range-placement gap):** This is the
   biggest substantive gap. Two options:
   - (a) **Document as out-of-scope** for v1.0.1-pilot; defer to
     v1.1+ rebuild after Phase B trains the model on the
     single-action + MIXED-label data we have.
   - (b) **Add range-placement-frequency rules** to all three
     prompts (e.g. for Protocol A: a Step 5.5 "Frequency
     calibration" section that maps HRP × composition shape →
     mix frequency).

   Recommend (a) for v1.0.1-pilot. Phase B will produce data
   from 4500 labels under single-action + MIXED conventions; that
   data plus calibration anchors gives the model the frequency
   signal indirectly. v1.1 can revisit.

**NIT-tier (defer to v1.1):**

4. F-S3-2 (B-Ex4 IP/OOP wording at L1078) — fix in v1.0.2 PR.
5. F-S4-1 (B-Ex4 flop sizing 33% → 25% to match solver-aligned) —
   fix in v1.0.2 PR.
6. F-S2-1 (v3.1 cross-references) — fix in v3.2 if v3 is
   touched; otherwise defer.
7. F-S5-4 (board_adjusted_hrp semantic explicit) — add 1
   sentence in B-pilot L514 and C-pilot L752: "Same semantics
   as HRP: 1.0 = top of board-adjusted range, 0.0 = bottom."
8. F-S7-3 (B-Examples blending hand-class into Steps 1-2) —
   defer; technically permitted by carve-out.

### Pilot-readiness implication

If F-S5-1 + F-S5-2 are patched (estimated 30-min builder edit),
Phase B can proceed with this audit dimension marked CLEAN.
Without the patch, Phase B will produce ~4500 labels where some
fraction of Protocol B labellers will silently skip the
Range-mass axis (best case) or hallucinate
`hero_top_pair_plus_pct` values (worst case) — both produce
training noise rather than wrong labels, but the training noise
is non-trivial.

The other MINOR items (under-use of HRP in B/C; gap in
frequency-from-range-placement) do NOT need to be fixed before
Phase B. They are sufficient-as-is for v1.0.1-pilot scope.

### Cross-audit synthesis suggestion

This audit's MINOR finding on phantom hero composition features
suggests Phase B trace audit should include a **per-label
spot-check** for any Protocol B trace that cites
`hero_top_pair_plus_pct` (or any hero-side composition pct).
Hits indicate hallucination; misses confirm the "if available"
guard worked. Recommend the orchestrator dispatch this
spot-check as part of the Phase B trace audit gate.

---

## Auditor's certification

This audit was conducted against the master HEAD versions of:

- `prompts/gto_labeller_v3.1.md` (730 lines, full read)
- `prompts/protocol_b_composition_first_v1_0_pilot.md` (1458
  lines, full read across 3 reads)
- `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`
  (1964 lines, full read across 4 reads)
- Cross-referenced: `prompts/protocol_b_composition_first_v1_0.md`
  (design artifact); `prompts/protocol_c_adversarial_elimination_v1_0.md`
  (design artifact); `river-rats-core/feature_keys.py` (production
  feature contract).

git HEAD at audit time: `1c6f674` ("Phase A.8 — Range-Reasoning
Coherence Audit directive (HALT Phase B until clean)").

Read-only investigation. No source files modified. Output landed
at the single requested path:
`/home/rupertbeytell/river-rats-v2/review/comms/AUDIT_A8_STATIC_PROMPTS_2026-04-26.md`.
