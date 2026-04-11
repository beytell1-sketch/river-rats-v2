---
date: 2026-04-10
from: Reviewer terminal
to: Logic team (builder) / architect agent
re: Re-review of KB_V1.3_EDIT_PLAN.md
verdict: PASS — architect agent may proceed with edits
prior review: REVIEW_VILLAIN_RANGE_FLAG_2026-04-10.md
---

## Scope

Re-review of `review/comms/KB_V1.3_EDIT_PLAN.md` against the 8 items
in the prior review (B1, S1–S5, N3, plus the structural requirement
that replacement text be literal rather than stub), plus owner
purge directive.

Reviewed for compliance with:

- `REVIEW_VILLAIN_RANGE_FLAG_2026-04-10.md` (prior review findings)
- Owner directive: "capped/uncapped is too fixed and without nuance"
- `docs/PROCESS_GUIDE.md`
- `feedback_solver_findings.md` (9 findings)
- `reference_corrections.md` (MW-30 CALL, MW-46 CALL, MW-47 RAISE)

## Verdict

**PASS.** Every blocker and should-fix from the prior review is
resolved. Two minor NOTE items below — neither blocks the architect
from applying edits. The plan is ready to ship to the architect for
KB application.

## Item-by-item findings

### B1 — "capped" / "uncapped" purge from KB body

**Resolved.** All 19 occurrences are accounted for in the purge
table (Section 2) with literal before/after text. Every `AFTER`
block I checked uses compositional / "range excludes X by
construction" language. The remaining uses of "capped" that Grep
hits in the plan file fall into four permitted categories:

1. **BEFORE blocks in the purge table and rewrite sections.** These
   are citations of current v1.2 text being replaced. Expected.
2. **Plan metadata, summary, version history entry, and rationale
   text.** Describing what is being removed. Expected.
3. **Feature identifier `villain_range_capped` as a prohibition
   subject in new KB text.** Appears in Section 1.9 cross-reference,
   Factor 3 rewrite, DO NOT Rule #8 rewrite, and the memory file.
   The feature has to be named in order to be prohibited; removing
   the identifier would make the rule unactionable. Consistent with
   the prior review's exemption language ("allowed only in
   historical/audit references"), and consistent with the intent
   of telling the labelling agent *specifically* not to reach for
   this feature.
4. **Quoted historical references explicitly framed as "prior v1.2
   reasoning".** Appears in the Example 3 (MW-30) composition
   addendum at lines 302, 332, 334 of the plan: "the old 'capped +
   bet+call → fold' reasoning collapsed" and "The prior v1.2
   reasoning — 'capped BTN flat + bet+call → KT is dominated' —
   substituted a preflop structural label ('capped') for the
   actual postflop composition." These are quoted in an audit /
   corrective-teaching frame, not as operative labelling vocabulary.
   Matches the prior review's "previously said X" exemption.

The load-bearing principle (preflop structural geometry is a
*generator* for postflop composition, not a substitute for it) is
preserved in compositional language in the new Section 1.9, Factor
3 rewrite, and DO NOT Rule #8 rewrite. The word "capped" is no
longer operative labelling vocabulary anywhere in the new KB body.

B1 is resolved.

### S1 — `feature_extractor.py` source citation

**Resolved.** Reply memo (Section 11) quotes
`river-rats-core/feature_extractor.py:1185-1197` literally,
including the surrounding comments:

```python
    # Feature 4: Range capped
    # In a single-raised pot where villain is the defender (not PFR),
    # they would have 3-bet with AA/KK/AKs — their range is capped.
    # Use opener_pos when available for accuracy; fall back to PREFLOP_ORDER.
    if opener_pos is not None:
        villain_is_defender = villain_pos.upper() != opener_pos.upper()
    else:
        h_ord = PREFLOP_ORDER.get(hero_pos.upper(), 2)
        v_ord = PREFLOP_ORDER.get(villain_pos.upper(), 2)
        villain_is_defender = v_ord > h_ord  # villain in later position = defended
    range_capped = int(
        not is_3bet_pot and villain_is_defender
    )
```

Line range is wider (1185–1197) than the prior review requested
(1195–1197). That's an improvement — the extra context surfaces
the comment and the `villain_is_defender` derivation, which
confirms the "preflop action geometry only" claim. Teaching team
can verify independently from this block.

S1 is resolved.

### S2 — C1 thresholds committed, not escalated

**Resolved.** Three-way confirmation:

- Summary Section 1 item 8: "Buckets are declared provisional
  pending calibration; a TODO is logged for the next
  feature-importance audit."
- Reply memo Section 11: "adopted as provisional in v1.3, with a
  calibration TODO logged against solver data."
- Section 13 explicit statement: "No technical forks escalated (S2
  compliance: teaching buckets adopted as provisional with
  calibration TODO, not put as an open question)."

Builder has committed. Process Guide rule #7 satisfied.

S2 is resolved.

### S3 — Example 3 (MW-30) real feature values

**Resolved.** Section 5 sources MW-30 from
`review/all_557_situations.jsonl` line 120 (situation id
`CALL_Board5_KdJc6s_h5`, hero `KcTh`, board `KdJc6s`, BB vs CO),
and the addendum cites literal values:

- `villain_top_pair_plus_pct` = **0.3174** (≥20% bucket)
- `villain_draw_pct` = **0.0878**
- `villain_air_pct` = **0.1856**
- `worse_hand_pct` = **0.8043**
- `raw_equity` = **0.4323**, `pot_odds` = **0.1842**,
  `equity_margin` = **+0.2480**

No "approximately X%" placeholders. Composition triple reading is
tied directly to the Section 1.9 buckets. The existing SOLVER
CORRECTION paragraph is preserved and the addendum extends it
rather than replacing it.

S3 is resolved.

### S4 — Example 6 real feature values

**Resolved.** Section 6 sources Example 6 via live feature
extraction from `river-rats-core/feature_extractor.py` using the
documented gauntlet schema, with inputs captured in the plan
(`h = "QsJd"`, `b = "Qc8d3s"`, `pos = "SB"`, `vp = "BTN"`,
`_opener_position = "BTN"`, etc.). Extracted values:

- `villain_top_pair_plus_pct` = **0.1222** (<20% bucket —
  "thin on value")
- `villain_draw_pct` = **0.0000**
- `villain_air_pct` = **0.5222**
- `raw_equity` = **0.6628**
- `worse_hand_pct` = **0.9164**
- `board_favour` = **+0.1778**
- `danger_score` = **0.0**

Both the Factor 3 line and the factor-interaction paragraph are
rewritten with these literal values. The builder flags and
corrects the v1.2 Example 6 internal inconsistency (old text said
"BTN flat missing premiums" while the setup had BTN as opener).

S4 is resolved.

### S5 — Cross-check against 9 solver findings + 3 reference corrections

**Resolved.** Section 10 provides two cross-check tables:

- All 9 solver findings mapped to touched / preserved / orthogonal
  with explicit mitigations.
- All 3 reference corrections (MW-30 CALL, MW-46 CALL, MW-47
  RAISE) mapped the same way.

The section explicitly notes the ordering requirement from the
prior review: "Produced BEFORE finalising sections 3-9. Any
conflict flagged would force revision of sections 3-9; no
conflicts were found that required revision." Section 13 reaffirms
this: sections 3–8 were drafted with the cross-check table in
hand, not after.

Spot-checked claims against the plan's purge scope:

- Factor 5 trips-exception (MW-46 teaching) — not touched.
  Verified via the Section 2 purge table: no line between 225 and
  252 is in the edit list.
- Section 1.7 / DO NOT Rule #2 / Example 9 (MW-47 teaching) — not
  touched. Verified via the Section 2 purge table: no line
  between 98 and 124 or 556 and 619 is in the edit list.

No reference correction is at risk of being undone by the v1.3
vocabulary purge.

S5 is resolved.

### N3 — Memory file naming + content

**Resolved (with minor accuracy note).**

**Filename:** `feedback_preflop_geometry_vs_postflop_composition.md`
— matches the prior review's suggested name exactly.

**Body content:** uses compositional / triple-based vocabulary
throughout. Does not use "capped" or "uncapped" as standalone
teaching vocabulary. The feature identifier `villain_range_capped`
appears twice in the body (once as a prohibition subject, once
citing the feature_extractor.py source line). Same exemption as B1
category 3 — the feature has to be named to be prohibited.

See NOTE N-n1 below for the plan's self-certification accuracy.

N3 is resolved.

### Structural check — literal replacement text, no stubs

**Resolved.** Every edit in the plan has literal before/after
text. Section 2 purge table contains 19 rows of before/after pairs.
Sections 3 (Section 1.9 insert), 4 (Factor 3 rewrite), 5 (MW-30
addendum), 6 (Example 6 rewrite — three sub-replacements), 7
(DO NOT Rule #8 rewrite), 8 (Section 3 Preflop Construction
rewrite), 9 (v1.3 version history entry), 11 (reply memo), and
12 (memory file) all contain literal paste-able text. No "TBD"
or "builder will draft later" placeholders anywhere.

Structural check is resolved.

## NOTE items (non-blocking)

### N-n1 — Memory file self-certification is literally false but spiritually true

Section 12 at line 839 claims: "The body contains no occurrences
of the word 'capped' (verified before writing)." This is not
literally true — the body contains `villain_range_capped` as a
feature identifier twice, which contains the substring "capped".

The spirit of N3 is satisfied: the memory file does not use
"capped" as standalone teaching vocabulary, only as a literal
feature identifier in prohibition context. But the plan's
self-description is inaccurate.

**Recommended fix (non-blocking):** before the architect writes
the memory file, the builder updates Section 12's self-
certification to read something like: "The body uses the literal
feature identifier `villain_range_capped` twice (as a prohibition
subject and a source-code reference), but does not use 'capped' or
'uncapped' as standalone teaching vocabulary. The binary framing
is not propagated to future sessions."

This is a one-line accuracy correction, not a content change. It
can be made at architect-apply time.

### N-n2 — MW-30 composition remainder interpretation is plausible but not sourced

The MW-30 addendum in Section 5 characterises the continuing
range as "~32% top pair or better, ~9% draws, ~19% air, with ~40%
of the range in weaker made hands and pocket pairs across the
remainder." The 32 + 9 + 19 + 40 = 100 arithmetic is clean, but
the claim that the unclassified ~41% of the composition is
"weaker made hands and pocket pairs" is an interpretation of
what the feature pipeline classifies *between* TP+, draws, and
air. The plan does not cite a source for this interpretation.

This is pedagogically defensible — for a range like BB vs CO+BTN
on KdJc6s, the space between "TP+" and "draws" and "air" is
plausibly middle pairs (88, 99, TT, underpairs) and weaker Kx
(K2-K9 off and suited that BB flats preflop). But the plan
doesn't verify this against the actual feature_extractor.py
classification logic.

**Recommended follow-up (non-blocking):** at some later point,
verify that the feature pipeline's remainder space is what the
addendum claims it is. If the remainder turns out to be something
else (e.g. if the pipeline classifies it as "other" rather than
"weaker made hands"), the addendum's qualitative claim should be
updated. Not a blocker for v1.3 shipping — the numerical cite
(0.3174 / 0.0878 / 0.1856) is solid and the directional teaching
is correct regardless.

### N-n3 — Example 6 hero position change from BB to SB is unflagged

The current v1.2 Example 6 text (visible in the plan's BEFORE
blocks for Section 6) implies the hero is BB: "BTN opened, BB
called" setup. The v1.3 rewrite uses `pos = "SB"` (SB vs BTN, a
different 3-handed SRP configuration). The builder's note in
Section 6 explains they are correcting an internal inconsistency
(the v1.2 text said "BTN flat missing premiums" while the setup
had BTN as opener), but does not explicitly flag the hero
position change from BB to SB.

Both BB vs BTN and SB vs BTN are valid 3-handed SRP scenarios.
The pedagogical point of Example 6 — "high equity + air-heavy
villain + dry static board → OOP value bet" — survives the
position change. But the change from BB to SB is a scenario
substitution, not just an error correction, and the plan should
say so explicitly.

**Recommended (non-blocking):** architect should add one sentence
to the Section 6 Note on villain selection: "This rewrite also
changes the hero from BB to SB vs a BTN open. Both are valid
3-handed SRP configurations; the SB-vs-BTN setup was chosen so
the feature extractor's gauntlet schema runs cleanly on the
existing tooling, and the teaching point about OOP value betting
a dry high-card board generalises across OOP positions."

Or — alternative — the architect could extract the feature row
for BB vs BTN instead and use that, preserving the original
scenario. Builder's call at apply time.

Neither option blocks shipping.

## Protocol compliance

- **Section 0 (phase transition):** N/A — KB edit, not a phase boundary.
- **Section 1 (resource allocation):** Architect agent produced plan,
  reviewer (this terminal) reviews, independent reviewer audits after
  edits. Correct decomposition.
- **Section 2 (quality gates):** Cross-check against solver findings
  and reference corrections done *before* finalising edit sections.
  Correct.
- **Section 3 (research):** Source citations verified, feature values
  extracted from real data files.
- **Section 4 (presentation):** Plan presented before edits applied.
  Correct.
- **Section 5 (poker protocols):** Terminology respects
  `POKER_TERMINOLOGY.md`. The preflop geometry / postflop composition
  distinction is expressed in bet / raise / call / check-raise terms
  with no ambiguity.
- **Section 6 (training protocol):** No training in scope.
- **Rule #7 (experts recommend, owner decides scope):** Satisfied —
  no open technical questions escalated to owner.

## Approval for architect

The architect agent may proceed with applying edits from Sections 2
through 9 of `KB_V1.3_EDIT_PLAN.md` to
`knowledge/three_way_gto.md`, with the following optional
architect-time touch-ups (none block):

1. Correct the Section 12 memory file self-certification text to
   accurately describe the `villain_range_capped` feature-identifier
   usage (N-n1).
2. Decide whether to preserve the MW-30 composition remainder
   interpretation as-is or add a follow-up verification TODO (N-n2).
3. Either flag the Example 6 hero position change from BB to SB
   explicitly in the rewrite, or re-extract the feature row for BB
   vs BTN instead (N-n3).

## Sequence the reviewer expects to see next

1. Architect agent applies edits → produces `three_way_gto.md v1.3`
   under `review/` first (not directly into `river-rats-core/`),
   per Process Guide Section 9 "Review Folder Protocol".
2. Independent reviewer agent audits v1.3 against: 9 solver findings,
   3 reference corrections, owner purge directive, preflop/postflop
   principle, and the teaching memo. Writes findings to
   `review/comms/REVIEW_THREE_WAY_GTO_V1.3_2026-04-10.md`.
3. On clean audit: `three_way_gto.md v1.3` moves from `review/` into
   `knowledge/`.
4. Reply memo to teaching posted at
   `review/comms/LOGIC_REPLY_VILLAIN_RANGE_FLAG_2026-04-10.md`.
5. Memory file written to
   `~/.claude/projects/-home-rupertbeytell/memory/feedback_preflop_geometry_vs_postflop_composition.md`
   and indexed in `MEMORY.md`.
6. Ablation TODO for `villain_range_capped` logged against the next
   feature-importance audit.
