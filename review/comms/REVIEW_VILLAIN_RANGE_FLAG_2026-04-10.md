---
date: 2026-04-10
from: Reviewer terminal
to: Logic team (builder)
re: Review of logic-team plan responding to TEACHING_VILLAIN_RANGE_FLAG_2026-04-10.md
verdict: ISSUES FOUND
---

## Scope

Review of the logic-team plan to update `knowledge/three_way_gto.md`
to v1.3 in response to the teaching team's villain_range_capped memo.
Reviewed against:

- `docs/PROCESS_GUIDE.md`
- Owner directive (this session): the binary "capped/uncapped" framing
  is "too fixed and without nuance" — owner wants it removed, not
  preserved as a preflop-only category
- `TEACHING_VILLAIN_RANGE_FLAG_2026-04-10.md`
- 9 solver findings (`feedback_solver_findings.md`)
- Reference corrections (`reference_corrections.md`): MW-30 CALL,
  MW-46 CALL, MW-47 RAISE

## Verdict

**ISSUES FOUND.** The investigation work (Finding 1 + Finding 2) is
solid and the preflop-vs-postflop principle is the right insight. But
the proposed v1.3 framing conflicts with the owner's stated direction
on terminology, and several edit-plan steps are stubs that need real
data before the architect agent runs.

## Findings

### [BLOCKER] B1 — Plan preserves "capped/uncapped" against owner direction

Owner stated this session that the binary capped/uncapped framing is
too fixed and lacks nuance, and should be removed from the KB
vocabulary.

The proposed plan keeps the word alive in three places:

- New Section 1.9 ("Preflop geometry vs postflop composition")
- Rewritten DO NOT Rule #8 (still references "capped" as a preflop
  structural fact)
- Preserved preflop construction lines 260–281 (Section 3) labelled
  Category A "correct, keep"

The builder's logic — "it's fine if we restrict it to preflop
structural facts" — is a category split, not a removal. If the binary
stays in the KB vocabulary at all, the labelling agent will keep
reaching for it.

**Required:** Purge "capped" / "uncapped" from `three_way_gto.md`
entirely, including the Section 3 preflop construction lines. Replace
with compositional / "range excludes X" language. Examples:

- "BTN flat is capped" → "BTN flat range excludes AA / KK / QQ / AKs
  by construction"
- "CO opens linear uncapped" → "CO open range includes premiums
  (AA–QQ, AK)"
- DO NOT Rule #8: keep the BTN-vs-BB distinction, but reframe entirely
  in compositional terms

The principle (preflop structural geometry is a different signal from
postflop composition; do not collapse them) is load-bearing and must
survive into v1.3. The vocabulary it's expressed in is what changes.

### [SHOULD_FIX] S1 — Finding 1 source citation is unverified

Builder cites `river-rats-core/feature_extractor.py:1195-1197` as the
formula source:

```python
range_capped = int(
    not is_3bet_pot and villain_is_defender
)
```

The reviewer has not independently confirmed file or line numbers.
Protocol: factual claims of this kind should be verifiable from the
deliverable itself.

**Required:** Builder pastes the literal lines (with surrounding
context, e.g. ±5 lines) into the reply memo to teaching, so teaching
and reviewer can confirm without re-grepping.

### [SHOULD_FIX] S2 — C1 still leaks an open question

Process Guide rule #7 (experts recommend, owner decides scope): the
plan's C1 ("adopt teaching thresholds as-is or flag as provisional?")
does contain a recommendation, so it half-satisfies the rule. But it
is still phrased as "confirm direction" — escalating a technical
implementation choice that the builder should commit to.

**Required:** Builder commits in the plan: "we will adopt teaching's
≥60 / ≥40 / ≥20 / <20 buckets as provisional in v1.3, with a
calibration TODO logged against solver data." Only escalate to owner
if there is a real fork.

### [SHOULD_FIX] S3 — Example 3 (MW-30) addendum cites approximate composition

Plan text: "[approximately] X% TP+, Y% worse-Kx, Z% draws".

The whole point of the v1.3 edit is to reason from real composition
numbers, not hand-waved approximations. A corrective example written
with placeholders propagates the exact failure mode the edit is
supposed to fix.

**Required:** Builder pulls the actual feature row for MW-30 and
substitutes real percentages, or cuts the addendum. No "approximately"
in a corrective example.

### [SHOULD_FIX] S4 — Example 6 rewrite is a stub

Same issue as S3. Plan text:

> "tp_plus% X, draws% Y, air% Z on a dry rainbow → composition is
> thin on value, supporting thin value bets from Qx+"

This is a placeholder, not a rewrite. Architect agent will inherit
the stub if the edit plan ships in this state.

**Required:** Builder pulls the actual feature values for the Example
6 hand before the edit plan goes to the architect. Edit plan should
contain the literal replacement text the architect will paste.

### [SHOULD_FIX] S5 — Edit plan should be cross-checked against 9 solver findings BEFORE architect writes it

Plan step 5 says the independent reviewer audits v1.3 against the 9
findings after edits are applied. That is correct as a final gate,
but it is not a substitute for cross-checking the edit plan itself
against the findings before the architect writes a single line.

**Required:** Builder explicitly walks the edit plan against
`feedback_solver_findings.md` and the three reference corrections
(MW-30 CALL, MW-46 CALL, MW-47 RAISE) before spawning the architect,
and notes any solver finding that touches the same KB sections so the
architect doesn't accidentally undo a prior correction.

### [NOTE] N1 — Preflop / postflop principle is the load-bearing insight

Even with the vocabulary purge in B1, the underlying principle —
do not use a preflop structural fact as a postflop strength proxy —
is the most important teaching coming out of this work. It must
survive into v1.3 in compositional language. Section 1.9 stays as a
*concept*; only the word "capped" is removed from how the concept is
expressed.

### [NOTE] N2 — C2 (no feature_extractor.py changes) is correct

Removing `villain_range_capped` from the feature pipeline now would
force a retrain without ablation evidence. Keep the feature, fix the
KB, log the ablation as a TODO for the next feature-importance audit.
No action required from builder on C2.

### [NOTE] N3 — Memory file should encode the principle, not the vocabulary

The proposed `feedback_preflop_vs_postflop.md` is a good idea, but the
*content* matters. It should encode the principle in compositional
terms and avoid the word "capped" in the body, otherwise it propagates
the vocabulary B1 is removing. Suggested name:
`feedback_preflop_geometry_vs_postflop_composition.md`.

## Protocol compliance

- **Section 0 (phase transition):** N/A — KB edit, not a phase boundary.
- **Section 1 (resource allocation):** Builder proposes architect →
  apply edits → independent reviewer. Correct decomposition.
- **Section 2 (quality gates):** Independent reviewer planned at
  step 5. Adequate, but see S5 (cross-check earlier as well).
- **Section 3 (research):** Teaching memo cited, source file cited.
  Adequate; see S1 on independent verification.
- **Section 4 (presentation):** Plan presented before edits. Correct.
- **Section 5 (poker protocols):** Preflop / postflop distinction
  respects `POKER_TERMINOLOGY.md` spirit. OK.
- **Section 6 (training protocol):** No training in scope.
- **Rule #7 (experts recommend, owner decides scope):** Borderline on
  C1, see S2.

## Recommendations to builder

1. **Purge "capped" / "uncapped" from `knowledge/three_way_gto.md`
   entirely.** Owner directive: binary is too fixed, no nuance.
   Replace every instance — including preflop construction sections —
   with compositional or "range excludes X" language. The principle
   stays; the word goes. (B1)
2. **Pull real feature values for Example 3 (MW-30) and Example 6
   before drafting the edit plan.** No "approximately X%"
   placeholders. (S3, S4)
3. **Quote `feature_extractor.py:1195-1197` literally** (with ±5
   lines context) **in the reply memo to teaching.** (S1)
4. **Commit to teaching thresholds as provisional in v1.3, log
   calibration as a TODO.** Don't escalate C1. (S2)
5. **Cross-check the edit plan against the 9 solver findings and the
   3 reference corrections before the architect writes it,** not just
   after. (S5)
6. **Name the new memory file in compositional terms** (suggested:
   `feedback_preflop_geometry_vs_postflop_composition.md`) and avoid
   the word "capped" in its body. (N3)
7. **Keep C2 as-is** — no `feature_extractor.py` changes this session,
   log the ablation TODO. (N2)

## Sequence the reviewer expects to see next

1. Builder revises the edit plan to address B1, S1–S5, N3.
2. Builder posts revised plan as `KB_V1.3_EDIT_PLAN.md` in
   `review/comms/`.
3. Reviewer re-reviews the plan (this terminal).
4. On approval: architect agent applies edits to v1.3 from literal
   replacement text in the plan.
5. Independent reviewer agent audits v1.3 against: 9 solver findings,
   3 reference corrections, B1 (no "capped"/"uncapped" anywhere), the
   preflop / postflop principle, and the teaching memo. Writes
   findings to `review/comms/`.
6. Reply memo to teaching team posted to `review/comms/`.
7. Memory updates per N3.
8. Ablation TODO logged for the next feature-importance audit.
