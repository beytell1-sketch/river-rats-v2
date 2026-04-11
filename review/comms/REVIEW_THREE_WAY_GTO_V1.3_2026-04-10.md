---
date: 2026-04-10
from: Independent auditor agent
to: Logic team
re: Independent audit of review/three_way_gto_v1.3.md
verdict: ISSUES FOUND
---

## Scope

Audited artifact: `/home/rupertbeytell/river-rats-v2/review/three_way_gto_v1.3.md`
(1005 lines). Compared against production `/home/rupertbeytell/river-rats-v2/knowledge/three_way_gto.md`
(v1.2, 705 lines).

Spec inputs read in full:
- `/home/rupertbeytell/.claude/projects/-home-rupertbeytell/memory/feedback_solver_findings.md`
- `/home/rupertbeytell/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- `/home/rupertbeytell/river-rats-v2/review/comms/TEACHING_VILLAIN_RANGE_FLAG_2026-04-10.md`
- `/home/rupertbeytell/river-rats-v2/docs/POKER_TERMINOLOGY.md`

Source-data references used:
- `/home/rupertbeytell/river-rats-v2/review/all_557_situations.jsonl` (line 120, MW-30 row)
- `/home/rupertbeytell/river-rats-v2/river-rats-core/feature_extractor.py` (used via `situation_factory.build_situation` for Example 6 re-extraction)
- `/home/rupertbeytell/river-rats-v2/river-rats-core/situation_factory.py`
- `/home/rupertbeytell/river-rats-teaching/interface/l3_renderer.py` (L3 renderer bucket thresholds)

Deliberately NOT read (to preserve independence, per scope brief):
- Any file in `review/comms/` with a `REVIEW_` prefix
- `review/comms/KB_V1.3_EDIT_PLAN.md`
- `review/comms/SCOPING_ACTION_HISTORY_*`
- `review/comms/REVIEW_ACTION_HISTORY_*`
- `review/comms/REVIEW_VILLAIN_RANGE_FLAG_*`

## Verdict

**ISSUES FOUND — not blocking, but should be fixed before v1.3 replaces production.**
The vocabulary purge is executed correctly, Section 1.9 is present and substantively correct,
all three reference corrections (MW-30, MW-46, MW-47) are respected, all KB-relevant solver
findings are preserved, and both independently verified feature sets (MW-30 feature row and
Example 6 live extraction) match v1.3's numbers within rounding tolerance. However, v1.3
contains one factually incorrect editorial assertion about Example 6 (the hero position was
*not* changed from v1.2), a small regression-side oddity where the KB cites reviewer notes on
a document the KB should not be describing as settled, and two NOTE-level tightenings that
should land before the cutover. None of the issues undermines the load-bearing content; the
audit clears pending the fixes below.

## Findings

### [SHOULD_FIX] F1 — Example 6 contains a factually wrong "rewrite" note

**v1.3 lines 663-666:**
> "This rewrite also changes the hero from BB to SB vs a BTN open. Both are valid 3-handed
> SRP configurations; the SB-vs-BTN setup was chosen so the feature extractor's gauntlet
> schema runs cleanly on the existing tooling..."

This is wrong. v1.2 Example 6 (`knowledge/three_way_gto.md` line 441) already reads:
> "Hero holds Qs Jd on Qc 8d 3s. SB (OOP, first to act), 2 opponents (BTN opened, BB called)."

The hero position in v1.2 is already SB, not BB. The v1.3 editorial note introduces a false
history claim about the position change. The setup itself is identical across v1.2 and v1.3
and matches what the extractor produced. The fix is to delete the two sentences at
lines 663-666 entirely (they misrepresent the edit history) and keep the rest of the example
as-is. No other lines need to change.

This is a SHOULD_FIX rather than a BLOCKER because the setup, features, and reasoning are all
correct — only the editorial meta-comment is wrong. But leaving it in would bake a false claim
about the document's own history into the KB.

### [SHOULD_FIX] F2 — Section 1.9 cites a reviewer note on an unread parallel review

**v1.3 lines 221-224 (cross-reference block at end of Section 1.9):**
> "The feature remains in the pipeline (no retraining forced this session — see reviewer
> note N2 on the villain_range_flag review), but the labelling agent must not treat it as
> a postflop signal."

The KB body is a reference document for the labelling agent; it should not contain bare
references to another in-flight review's note numbering ("reviewer note N2"). If retraining
is deferred, state it as a fact ("The feature remains in the pipeline; no retraining is
forced by this KB revision") and drop the reviewer-note pointer. The parallel review itself
is a working document that may be archived, merged, or renumbered — this cross-reference will
rot. Fix: replace "see reviewer note N2 on the villain_range_flag review" with a plain
statement of the deferral policy, or with a pointer to the feedback_solver_findings.md
"Bookmarked: upgrade extract_range_composition to combo-level" entry which actually captures
the retraining policy for feature churn.

A similar pointer exists at v1.3 lines 985-986 in the version-history block, citing
`review/comms/KB_V1.3_EDIT_PLAN.md` and `review/comms/REVIEW_VILLAIN_RANGE_FLAG_2026-04-10.md`.
Version-history pointers to working documents are less harmful (history is append-only) but
follow the same pattern — flagging as part of the same finding. At minimum, keep the
KB_V1.3_EDIT_PLAN pointer as traceable provenance and drop the reviewer-note reference inside
Section 1.9.

### [NOTE] F3 — Composition remainder characterization flagged as provisional but shipped anyway

**v1.3 lines 580-583 (Example 3 composition addendum):**
> "(Note: the '~40% weaker made hands and pocket pairs' characterisation of the unclassified
> remainder is provisional — it requires verification against `feature_extractor.py`
> classification logic before v1.4.)"

The same ~40% figure is then stated as fact three lines earlier (line 574) without the
provisional hedge:
> "~32% top pair or better, ~9% draws, ~19% air, with ~40% of the range in weaker made hands
> and pocket pairs across the remainder."

And the figure also appears in Section 1.9 lines 184-188 without any hedge:
> "roughly 32% strong, 9% draws, 19% air, and ~40% weaker made hands and pocket pairs in
> the remainder."

The composition triple sums to 0.3174 + 0.0878 + 0.1856 = 0.5908, leaving 0.4092 unclassified
— so the ~40% remainder figure is arithmetically correct. But v1.3 also asserts the
*composition* of that remainder ("weaker made hands and pocket pairs") without
`feature_extractor.py` classification verification. The TODO is logged in the addendum but
not in Section 1.9. Either:
(a) verify the remainder composition against `extract_range_composition` logic now and drop
the "provisional" tag, or
(b) add the same "provisional" hedge to Section 1.9 so the two sections are consistent about
what is solid and what is pending.

Recommend (a) — the verification is cheap (one script pass) and leaving a provisional
characterisation as KB load-bearing text is brittle.

### [NOTE] F4 — "Single-raised pot" phrasing is a carryover inconsistency with POKER_TERMINOLOGY.md

**v1.3 lines 689-690 and 713 (Example 6):**
> "Here, in a single-raised pot..."
> "— not to single-raised pots where the composition triple..."

`docs/POKER_TERMINOLOGY.md` defines the pot types as "limped pot" / "opened/standard pot" /
"raised pot (3-bet)". By that table, a "single-raised pot" (i.e. a single open bet, no
re-raise) is an *opened pot*, not a "raised" one — because opening preflop is a BET, not a
raise.

This is a carryover from v1.2 (lines 457 and 474 use the same phrasing), so it is not a
v1.3-introduced regression and not a blocker. But since v1.3 is already rewriting vocabulary,
the replacement is cheap: "single-raised pot" → "single-raised (SRP) pot" is the industry
convention that most readers will recognise, OR "standard single-raised pot (no 3-bet)" to
make the distinction from 3-bet pot explicit. Logging as a NOTE; fix opportunistically, not
a blocker for v1.3 cutover.

### [NOTE] F5 — DO NOT Rule #8 has grown but remains strictly compatible with v1.2's rule

v1.2 Rule 8 (v1.2 lines 647-651) was a 5-line statement: "DO NOT assume both opponents have
equivalent ranges. The cold-caller (BTN flat) is capped — no premiums. The blind defender
(BB) is wide but uncapped via squeeze. Reasoning must distinguish between them: the capped
player folds strong draws less, the wide player folds air more."

v1.3 Rule 8 (v1.3 lines 887-924) expands this to ~38 lines, converts the binary framing to
compositional language, and adds an explicit "do not use villain_range_capped as a postflop
strength signal" instruction. The operative asymmetry ("cold-caller folds strong draws less,
blind defender folds air more") is preserved verbatim at v1.3 lines 905-908. This is a clean
re-expression, not a regression. Flagging only to confirm the reviewer checked it — the
substantive content of v1.2 Rule 8 is fully preserved inside v1.3's larger Rule 8, and the
compositional addition strictly strengthens the rule.

## Protocol compliance

### Raw rule 1 (vocabulary purge): **PASS**

Case-insensitive word-boundary grep `\b[Cc]apped\b|\b[Uu]ncapped\b` against v1.3 returns
**5 hits**, all in permitted contexts:

| Line | Quote | Allowed category |
|------|-------|------------------|
| 552 | `composition the old "capped + bet+call → fold" reasoning collapsed:` | Quoted historical "old reasoning" framing (corrective teaching) |
| 585 | `The prior v1.2 reasoning — "capped BTN flat + bet+call → KT is` | Quoted "prior v1.2 reasoning" (corrective teaching) |
| 587 | `("capped") for the actual postflop composition.` | Continuation of the same quoted v1.2 framing |
| 961 | `reframing. Removed the words "capped" and "uncapped" from the KB` | Version-history block describing the removal |
| 982 | `audit. Rationale: the binary "capped/uncapped" framing was too` | Version-history block |

All 5 are quoted/scare-quoted and framed as either the v1.2 reasoning being corrected or the
removal itself. **Zero operative uses remain.** The literal feature identifier
`villain_range_capped` appears 9 times (v1.3 lines 221, 280, 282, 290, 564, 888, 912, 970,
977) and every single occurrence is either (a) telling the labelling agent NOT to use the
feature as a postflop signal, or (b) documenting the removal — all permitted by raw rule 1's
first exception clause.

v1.2 by comparison had 19 occurrences of the bareword (grep count against
`knowledge/three_way_gto.md`), consistent with the version-history claim of "19 occurrences
purged". Purge arithmetic is consistent.

### Raw rule 2 (preflop/postflop principle): **PASS**

Section 1.9 "Preflop geometry vs postflop composition — do not collapse them" exists at
v1.3 lines 146-225. The principle is stated correctly:

- Preflop geometry vs postflop composition are *distinct signals* (lines 148-172).
- The composition triple is identified as the primary postflop strength signal (lines 158-168).
- The MW-30 trap is given as a worked illustration of the collapse (lines 173-193).
- The rule is stated explicitly: "Reason postflop decisions from the composition triple as
  the **primary** strength signal. Use preflop action sequence only to inform what the
  preflop range looked like — never substitute it for the current-street composition."
  (lines 195-198).
- Section 3 (lines 384-391) reinforces: "Preflop action sequence determines which combos were
  structurally allowed into each player's range. That is a *generator* for the postflop
  composition triple (Section 1.9, Factor 3) — it is not a substitute for it."
- Factor 3 (lines 254-316) is rewritten in compositional language, including the explicit
  demotion of `villain_range_capped` out of the postflop signal list at lines 280-293.

The principle is correctly expressed. PASS.

### Raw rule 3 (reference corrections): **PASS**

| Hand | Correct label (memory) | v1.3 line | v1.3 label | Match |
|------|------------------------|-----------|-----------|-------|
| MW-30 (KcTh on KdJc6s, BB, bet+call) | CALL | 536 | "**Corrected action:** CALL" | YES |
| MW-46 (K7 trips on 775-9-J, river check-raise) | CALL | 379-380 | "Trips or better facing a river check-raise is still a CALL... (MW-46: K7 trips on 775-9-J, solver says 100% CALL even with worse trips.)" | YES |
| MW-47 (AsQs on KsJd5s, SB, facing bet) | RAISE | 825 | "**Action:** RAISE" (Example 9) | YES |

All three corrections are reflected and explained. No contradictory text anywhere in the KB.

### Raw rule 4 (solver findings): **PASS** (9/9, with caveats on which findings are KB-scope)

Cross-checked each finding in `feedback_solver_findings.md` against v1.3:

| # | Finding | v1.3 treatment | Status |
|---|---------|----------------|--------|
| 1 | Non-set hands mix raise/call, default CALL in labels | Section 1.7 lines 119-124: "Default for non-set made hands at mixed SPR: ...default to CALL in training labels. ...Only sets and the pure nuts are labelled RAISE." — verbatim preservation | PRESERVED |
| 2 | facing_bet dominance in training data (62% feature importance) | Not KB-body material (concerns factory design, not labelling). v1.2 also does not mention it. | NOT KB-SCOPE |
| 3 | Bottom pair facing bet+call is CALL when equity > pot odds | Factor 5 lines 352-367, DO NOT Rule updated; generalised at Example 3 lines 595-603 ("When facing bet+call with a made hand that has equity well above pot odds (≥20pp margin)...") | PRESERVED + STRENGTHENED |
| 4 | Warm-start regime (from-scratch beats warm-start HU→3-way) | Training architecture, not KB content | NOT KB-SCOPE |
| 5 | Limped pots excluded from scope | Not KB content | NOT KB-SCOPE |
| 6 | MW-30 reference label CALL | Example 3 solver correction + Section 1.9 worked illustration | PRESERVED |
| 7 | MW-46 reference label CALL | Factor 5 exception at lines 375-380 (explicit MW-46 citation) | PRESERVED |
| 8 | MW-47 shared blind spot, CALL → RAISE | Example 9 lines 796-836 + Section 1.7 carve-out + DO NOT Rule #2 exception | PRESERVED |
| 9 | facing_raise bug (self_play.py fix) | Engineering fix, not KB content | NOT KB-SCOPE |

Four of the nine findings are engineering / training / data concerns outside KB scope. The
five KB-relevant findings (1, 3, 6, 7, 8) are all preserved. None is contradicted, weakened,
or removed. In particular the "default to CALL for non-set mixed hands" rule from finding 1
is present *unchanged* in Section 1.7 despite the vocabulary purge around it, and the
MW-30/MW-46/MW-47 corrections are all explicit and cited to the solver.

### Raw rule 5 (teaching coordination): **PASS**

The teaching memo (`TEACHING_VILLAIN_RANGE_FLAG_2026-04-10.md`) specifies TP+ buckets
≥60 / ≥40 / ≥20 / <20. v1.3 adopts the identical four buckets at lines 206-212 in Section
1.9 and cites `river-rats-teaching/interface/l3_renderer.py` `_villain_range_sentence` at
line 317+ as the shared source. I verified the l3_renderer reference: the function is
defined at line 317 in the current `l3_renderer.py`, and the bucket threshold at line 331 is
`if tp_plus >= 60:` — matching the KB. The threshold labels in v1.3 lines 206-212
("Heavy with strong hands" / "Meaningful value density" / "Some value but mostly weaker
holdings" / "Thin on value") are paraphrases of the L3 renderer's sentence fragments in the
memo — close enough to count as shared vocabulary.

v1.3 also flags the thresholds as "provisional pending calibration against solver data" at
lines 213-218, with a TODO logged for the next feature-importance audit and a note that if
calibration shifts the boundaries, both the KB and `l3_renderer.py` must be updated together.
This is the correct coordination discipline. PASS.

### Raw rule 6 (poker terminology): **PASS with one NOTE** (see F4)

Scanned all uses of bet/raise/open in v1.3. No slips on "blinds are posted not bet" (no
references to blinds being "bet"). Opening preflop is consistently described as "opens"
(lines 395 "CO opens ~27-28%", 419 "HJ opens tighter ~22-24%"). "Preflop raiser" at line 323
is a carryover from v1.2 and is an accepted industry term; POKER_TERMINOLOGY.md itself uses
"raised pot (3-bet)" for 3-bet pots but does not police the phrase "preflop raiser". The
only edge-case carryover is "single-raised pot" — see finding F4 — which is a v1.2 carryover
and not a v1.3-introduced issue. PASS.

### Raw rule 7 (regression check): **PASS with NOTEs**

Walked Examples 1–9 and DO NOT Rules 1–7 comparing v1.2 to v1.3:

- **Example 1 (KcQc on Kh8d3s):** v1.2 line 300-302 "BTN is capped but CO is uncapped with
  AK/KK in range" → v1.3 line 459-462 "BTN flat range excludes AA/KK/QQ/AKs, but CO open
  range still contains AK and KK". Pure vocabulary purge, semantically identical. OK.
- **Example 2 (Jh9h on Jc7d2s):** Identical across v1.2 and v1.3. OK.
- **Example 3 (KT on KJ6):** v1.3 adds a large "Composition addendum (v1.3, real feature
  row)" block at lines 548-603 with JSONL-verified feature values and a generalisation rule.
  Verified against source (see feature verification section below). This is additive
  corrective teaching on top of the v1.2 solver correction, not a regression. OK.
- **Example 4 (88 on Jd8s5c):** Identical. OK.
- **Example 5 (Td9d on Qd7h3d):** v1.2 line 421-422 "CO opened (uncapped), BTN called
  (capped but connected range hits middle boards)" → v1.3 line 638-641 "CO's open range
  contains premiums (AA-QQ, AK), BTN's cold-call range excludes those premiums by
  construction but connected range hits middle boards". Pure purge, semantically identical. OK.
- **Example 6 (QsJd on Qc8d3s):** Feature values rewritten from approximations
  (`villain_air_pct ~0.49`, `worse_hand_pct 88%`) to live extraction values
  (`villain_air_pct = 0.5222`, `worse_hand_pct = 0.9164`). The conclusion (BET, HIGH
  confidence) is unchanged. The new values are tighter and verified (see Example 6
  verification below). OK from a regression standpoint — but see F1 above for the
  factually-wrong editorial note about the position change.
- **Example 7 (AdKs on Jd8d4c):** v1.2 line 486 "CO uncapped, villain_tp_plus ~0.47 (strong)"
  → v1.3 line 725-726 "CO's open range contains premiums (AA/KK/AK),
  villain_top_pair_plus_pct ~0.47 (strong — ≥40% bucket per Section 1.9)". Pure purge +
  bucket annotation. OK.
- **Example 8 (QhTc on KsQd7cJh):** Identical across v1.2 and v1.3. OK.
- **Example 9 (AsQs on KsJd5s):** Identical across v1.2 and v1.3. OK.
- **DO NOT Rule 1 (equity alone):** Identical. OK.
- **DO NOT Rule 2 (semi-bluff exception):** Identical. OK.
- **DO NOT Rule 3 (checking player trap):** Identical. OK.
- **DO NOT Rule 4 (auto-c-bet IP):** Identical. OK.
- **DO NOT Rule 5 (TP as strong hand):** Identical. OK.
- **DO NOT Rule 6 (blockers for action selection):** Identical. OK.
- **DO NOT Rule 7 (streets in isolation):** Identical. OK.
- **DO NOT Rule 8 (opponent asymmetry):** Substantively expanded (see F5 above). The v1.2
  content is preserved as a proper subset of the v1.3 version, and the v1.3 additions all
  reinforce the principle. Not a regression.

No substantive content change is inconsistent with a vocabulary purge. All conclusions,
hand ranges, and confidence labels across all 9 examples and all 8 rules (v1.3 adds no new
rules; the count is still 8) are preserved.

## Independent feature-value verification

### MW-30 (KcTh on KdJc6s, BB facing CO bet + BTN call)

- **Method:** grepped `/home/rupertbeytell/river-rats-v2/review/all_557_situations.jsonl` for
  the `KcTh` + `KdJc6s` row using a JSONL-walking Python script.
- **Source:** `review/all_557_situations.jsonl` line 120,
  `_situation_id = CALL_Board5_KdJc6s_h5`.
- **v1.3 claim** (lines 548-572):

| Feature | v1.3 cited | JSONL source | Match |
|---------|-----------|--------------|-------|
| `villain_top_pair_plus_pct` | 0.3174 | 0.3174 | EXACT |
| `villain_draw_pct` | 0.0878 | 0.0878 | EXACT |
| `villain_air_pct` | 0.1856 | 0.1856 | EXACT |
| `worse_hand_pct` | 0.8043 | 0.804281 | EXACT (3dp rounding) |
| `raw_equity` | 0.4323 | 0.43225 | EXACT (4dp rounding) |
| `pot_odds` | 0.1842 | 0.184211 | EXACT (4dp rounding) |
| `equity_margin` | +0.2480 | 0.248039 | EXACT (4dp rounding) |
| `villain_range_capped` | 0 | 0 | EXACT |

**Result: MATCH on all eight cited features.** v1.3's MW-30 numbers are independently
verified against the JSONL source within rounding tolerance. In particular the
`villain_range_capped = 0` observation (v1.3 lines 564-571) is correct and the commentary
about this being a structural quirk of single-villain feature extraction is consistent with
the data (the single villain indexed here is CO, the bettor — not the BTN cold-caller, so
the "range_capped" bit reflects CO's range construction, which is uncapped by definition).

### Example 6 (QsJd on Qc8d3s, SB, BTN opener, BB caller, not facing bet)

- **Method:** imported `situation_factory.build_situation` from
  `/home/rupertbeytell/river-rats-v2/river-rats-core/situation_factory.py` and built a
  `SituationSpec` with:
  - `hero_cards=['Qs','Jd']`
  - `board_cards=['Qc','8d','3s']`
  - `hero_pos='SB'`
  - `villain_positions=['BTN','BB']`
  - `pot=90.0, to_call=0.0, street='flop'`
  - `action_history=[('preflop','BTN','raise'), ('preflop','SB','call'), ('preflop','BB','call')]`
  - `opener_position='BTN', effective_stack=970.0`
  then called `build_situation(spec)` and read the returned feature dict.

Schema was adapted from `review/generate_factory_batch4.py` which uses the same pattern
(dict of board + hero_cards → SituationSpec → build_situation → feature dict).

- **v1.3 claim** (lines 670-680):

| Feature | v1.3 cited | Live extraction | Match |
|---------|-----------|-----------------|-------|
| `villain_top_pair_plus_pct` | 0.1222 | 0.1222 | EXACT |
| `villain_draw_pct` | 0.0000 | 0.0 | EXACT |
| `villain_air_pct` | 0.5222 | 0.5222 | EXACT |
| `worse_hand_pct` | 0.9164 | 0.91635 | EXACT (4dp rounding) |
| `raw_equity` (approx "~66%") | — | 0.65825 | MATCH (v1.3 says "~66%" in factor interaction at line 684) |
| `board_favour` | +0.1778 | 0.1778 | EXACT |
| `danger_score` | 0.00 | 0.0 | EXACT |
| `hero_range_percentile` | 0.7164 | 0.716393 | EXACT (4dp rounding) |

**Result: MATCH on all eight cited features.** Example 6 feature values are independently
verified by live re-extraction. The extraction ran cleanly on the gauntlet schema with no
warnings. The v1.3 factor-interaction commentary ("~65%+ raw equity", "≥90% worse hands",
"<20% TP+ bucket", "0.0 danger score") is entirely consistent with the extracted values.

## Structural checks

- **Line count:** v1.3 is **1005 lines** vs the ~705 line v1.2 (gain of ~300 lines). This is
  within the expected 750-1100 range the brief specified. Most of the gain is Section 1.9
  (~80 lines), the Example 3 composition addendum (~55 lines), the expanded Factor 3
  compositional language (~25 lines), DO NOT Rule #8 expansion (~30 lines), and the expanded
  version-history block (~25 lines). Balanced and traceable. OK.
- **Version number:** "Version: 1.3" at line 3. OK.
- **Version history:** v1.3 entry at lines 960-986 is the most detailed of the three;
  v1.2 entry preserved at lines 987-994; v1.1 entry preserved at lines 995-999; v1.0 entry
  preserved at lines 1000-1002. No historical drift. OK (modulo F2's concern about the
  pointer to the in-flight review documents).
- **Sections 1.1-1.8:** All present, preserved from v1.2 content-wise apart from the
  vocabulary purge. OK.
- **New Section 1.9:** Present at lines 146-225, titled "Preflop geometry vs postflop
  composition — do not collapse them". Principle clearly stated. OK.
- **Section 2 Decision Framework:** Factors 1-5 all present (Factor 1 line 236, Factor 2
  line 243, Factor 3 line 254, Factor 4 line 318, Factor 5 line 338). OK.
- **Section 3 Preflop Construction:** Present at lines 384-443, rewritten in compositional
  language. Framing as "generator for the postflop composition triple, not a substitute for
  it" at lines 387-391. OK.
- **Section 4 Worked Examples:** All 9 examples present (Example 1 line 451, 2 line 476,
  3 line 500, 4 line 605, 5 line 630, 6 line 657, 7 line 716, 8 line 752, 9 line 796). OK.
- **Section 5 DO NOT Rules:** All 8 rules present (Rule 1 line 845, 2 line 850, 3 line 861,
  4 line 865, 5 line 870, 6 line 875, 7 line 883, 8 line 887). OK.

## Recommendations

1. **Fix F1 before cutover.** Delete the two sentences at v1.3 lines 663-666 that falsely
   claim the Example 6 hero was changed from BB to SB. The claim is wrong (v1.2 already had
   SB hero) and writing false edit history into the KB body is a non-starter.

2. **Fix F2 before cutover.** Replace the "see reviewer note N2 on the villain_range_flag
   review" cross-reference in Section 1.9 (v1.3 lines 222-224) with a plain policy
   statement. The KB body should not cite working-document note numbering it has no
   control over.

3. **Address F3 opportunistically.** Either verify the ~40% "weaker made hands and pocket
   pairs" characterisation against `extract_range_composition` classification logic now, or
   add the "provisional" hedge to Section 1.9 (line 187) so the two mentions are consistent.
   Cheap to do now; brittle if left.

4. **Defer F4 and F5 as NOTEs.** F4 is a v1.2 carryover (single-raised pot phrasing) and
   does not affect the correctness of the v1.3 rewrite; fix opportunistically in the next
   revision. F5 is a confirmation note, not a finding — DO NOT Rule #8 is fine as expanded.

5. **Cutover:** After F1 and F2 are fixed, v1.3 is clear to replace `knowledge/three_way_gto.md`.
   All three reference corrections are respected, all KB-relevant solver findings are
   preserved, the vocabulary purge is clean with zero operative leaks, the preflop-vs-postflop
   composition principle is correctly expressed, Section 1.9 adopts the teaching-side
   thresholds with the right coordination discipline, and both independently verified feature
   sets match v1.3's cited numbers exactly. The load-bearing content is solid; the fixes
   above are cleanup of editorial slips and cross-reference hygiene, not content corrections.

6. **Open question for the logic team (not a finding):** Section 1.9's cross-reference at
   line 221 states that `villain_range_capped` "remains in the pipeline (no retraining forced
   this session)". Whether the feature should actually be retrained-out of v9-3way at some
   future point is a model-training decision, not a KB decision — but the KB body should
   not be asserting training policy. Consider moving the "no retraining this session"
   statement out of the KB and into the model gating notes. Not a blocker.
