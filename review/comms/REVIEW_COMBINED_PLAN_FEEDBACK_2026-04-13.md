---
date: 2026-04-13
from: Reviewer (main terminal)
to: Builder team + Owner
re: Combined plan feedback — merging FULL_REBUILD and EXPERT_PANEL into one actionable plan
status: FOR DISCUSSION — suggestions for builder to incorporate
---

# Review: Combining Both Plans

## 1. What I'm comparing

- **Plan A (FULL_REBUILD):** Reconstruct all 351, keep same
  cards/board, relabel bucket-first, compare old vs new.
- **Plan B (EXPERT_PANEL Option H):** Discard 151 factory 2-way,
  reconstruct 200 self-play 3-way, generate ~200-270 new 3-way,
  relabel bucket-first, compare on the 200.

## 2. Where the expert panel improves on Plan A

### 2.1 Discard the 151 factory 2-way — AGREE

This is the strongest finding. Plan A treated all 351 equally.
The GTO expert is right: 2-way spots have no sandwich pressure,
no third-player dynamics. These are heads-up situations being
fed to a 3-way specialist model. The model doesn't just learn
nothing useful from them — it learns actively wrong things about
3-way dynamics.

Reconstructing their sequences is wasted effort. Even with
perfect sequences and perfect labels, the situations teach the
wrong lesson.

**Recommendation: Accept. Discard all 151 factory 2-way.**

### 2.2 Feature corruption blast radius — AGREE

Plan A treated the NULL features as a parallel problem to fix
during re-extraction. The ML architect correctly identifies that
10-14 features (20-30%) depend on action sequences, not just
the 6 obvious counters. This means the comparison between old
and new features is more informative than Plan A assumed — a
sequence correction can ripple into pot_odds, SPR, and
positional features.

**Recommendation: Accept. The feature diff report in Phase 1D
is more important than Plan A recognised. Give it an explicit
owner review gate.**

### 2.3 Reconstruction confidence tagging — AGREE

Plan B's CERTAIN/AMBIGUOUS/CORRUPT classification is the same
concept as Plan A but with the architect's feasibility estimates
(~140-160 CERTAIN, ~30-40 AMBIGUOUS, ~10-20 CORRUPT). These
numbers are useful for planning but should be verified, not
assumed.

**Recommendation: Accept. Build the tool, run it, and report
actuals vs estimates before proceeding.**

## 3. Where Plan A should be preserved

### 3.1 The comparison report — KEEP (Plan A was more detailed)

Plan B mentions a comparison matrix but Plan A's version is more
operationally specific. The comparison report should include:

```
situation_id | old_action | new_action | agree? |
sequence_status | features_changed_count | hand_bucket |
strategic_role | old_reasoning_available?
```

And the interpretation table:

| Old | New | Sequence | What it means |
|-----|-----|----------|---------------|
| Same | Same | CERTAIN | Both agree, valid hand — highest confidence |
| Same | Same | AMBIGUOUS | Agreement despite sequence ambiguity — trustworthy |
| Different | — | CERTAIN | Sequence was fine — bucket-first reasoning changed the call. Review each. |
| Different | — | CORRUPT→regen | Old label built on corrupt data — new label authoritative |

Plan B's matrix is simpler (just action pairs with counts). The
per-situation detail from Plan A is what the owner needs to make
case-by-case decisions on disagreements.

**Recommendation: Use Plan A's detailed comparison format.**

### 3.2 Disagreement thresholds — KEEP from Plan A

Plan A defined escalation bands:
- <10% disagreement: targeted improvements, proceed
- 10-25%: significant shift, review all individually
- >25%: stop and diagnose

Plan B doesn't define these. They're important because they tell
the owner what "normal" looks like and when to worry.

**Recommendation: Keep the thresholds.**

### 3.3 Solver verification triggers — KEEP from Plan A

Plan A added a specific solver trigger for disagreements: "any
disagreement where old label was CALL and new label is not." This
targets passive bias corrections specifically — the most likely
category of bucket-first changes.

Plan B doesn't specify solver triggers for the comparison.

**Recommendation: Keep Plan A's solver triggers, including the
CALL-disagreement trigger.**

### 3.4 Phase 0 pipeline hardening detail — KEEP from Plan A

Plan A's Phase 0 has 8 specific steps (0.1-0.8) with per-step
gates. Plan B references "hardened pipeline" but doesn't break
down the steps. The detail matters because this is the blocker
phase — if any step is unclear, it stalls everything.

**Recommendation: Use Plan A's Phase 0 detail verbatim.**

## 4. Where neither plan is quite right

### 4.1 AMBIGUOUS situations need a decision rule

Both plans tag AMBIGUOUS situations (multiple valid sequences)
but neither says what to do with them at labelling time. The
labelling agent receives the action string — which one does it
get?

Options:
- **A: Use any valid sequence.** The features are consistent
  regardless, so the label should be the same. Give the agent
  the first valid sequence found.
- **B: Use the sequence most consistent with prior_actions.**
  For self-play 3-way, `prior_actions` gives hero's side. Pick
  the valid sequence whose hero actions match.
- **C: Flag for manual review.** Owner picks the sequence.

**Recommendation: Option B first, then A as fallback.** Match
hero actions from `prior_actions` to narrow the candidates. If
multiple still remain and hero actions are the same across all
candidates, pick any (features are consistent). If hero actions
differ between candidates, flag for manual review.

### 4.2 The reconstruction tool's self-consistency check

Plan A mentioned this but didn't make it a gate. Plan B doesn't
mention it at all. This is critical:

> For any CERTAIN/AMBIGUOUS result, re-extract features from
> the reconstructed sequence and confirm they match the original
> feature values.

If re-extracted features DON'T match the originals on a CERTAIN
situation, something is wrong — either the reconstruction is
wrong or the original feature extraction was buggy. Either way,
the situation should be reclassified as SUSPECT (a fourth
category between AMBIGUOUS and CORRUPT).

**Recommendation: Add SUSPECT as a classification. Make the
self-consistency check a gate before labelling.**

### 4.3 New situation allocation (the ~200-270)

Plan B says "generate ~200-270 new 3-way situations" but doesn't
break down the allocation. Plan A's Phase 3 had BP7 (15-20 RAISE)
and batch 4 BET/CHECK (80-100) but that was on top of 351
reconstructed.

With only ~200 reconstructed surviving, the new situations need
to cover more ground. The allocation should be designed AFTER
seeing the reconstruction results — what action classes, streets,
and positions are under-represented in the 200 that survived?

**Recommendation: Phase 1C allocation is designed after Phase 1B
results are known. Don't pre-commit to BP1-BP7 counts until we
know what the surviving 200 look like.**

### 4.4 Bucket-first threshold sensitivity

The GTO expert flagged a real concern: "0.54 equity = medium_made,
0.56 = strong_made." Both plans acknowledge bucket-first has risks
but neither addresses this.

The labelling prompt should NOT use hard equity thresholds for
bucket classification. The bucket is a poker judgment ("is this
hand strong enough to raise for value in this spot?"), not a
threshold check. If we give agents hard thresholds, we're
building another decision tree — exactly what we're moving away
from.

**Recommendation: The bucket-first prompt should describe the
buckets qualitatively with examples, not with equity thresholds.
The thresholds in spot_classifier.py are for the teaching system
(which needs deterministic classification). The labelling agents
should use poker reasoning to classify, not if/elif on equity.**

This is important. If the labelling prompt says "equity > 0.55 =
strong_made", the agent will classify mechanically. If it says
"strong_made = a hand strong enough that you would raise for
value against a reasonable range in most spots (e.g. top two
pair, strong overpair, flush on safe board)", the agent reasons
about the actual hand.

## 5. Suggested combined plan structure

```
Phase 0: Pipeline hardening (from Plan A, 8 steps, BLOCKER)
  └─ Owner gate

Phase 1A: Triage (from Plan B)
  - Discard 151 factory 2-way
  - 200 self-play 3-way proceed to reconstruction

Phase 1B: Build + run reconstruction tool (from Plan B + Plan A detail)
  - Build tool with CERTAIN/AMBIGUOUS/SUSPECT/CORRUPT classification
  - Self-consistency check: re-extract features, compare to originals
  - Run on 200 situations, produce classification report
  └─ Owner gate (review classification actuals vs estimates)

Phase 1C: Re-extract features for surviving situations (from Plan A)
  - Full 48-feature extraction using validated sequences
  - Feature diff report: what changed from originals?
  - NULL features now populated
  └─ Owner gate (review feature diff)

Phase 1D: Design new situation allocation (informed by 1B results)
  - What survived from reconstruction?
  - What action classes / streets / positions need more coverage?
  - BP7 RAISE situations (mandatory — non-negotiable)
  - BET/CHECK factory to fill gaps
  - Target: ~400-470 total training situations
  └─ Owner gate

Phase 1E: Generate new situations through hardened factory
  - All validated, all 48 features, all with action_string
  - Small yield test (20) before scaling
  └─ Owner gate

Phase 2A: Update labelling prompt (bucket-first, qualitative buckets)
  - MW-30 FOLD→CALL
  - villain_range_capped demotion
  └─ Owner gate

Phase 2B: Calibration exam
  - 20/24 gate + 3 GTO-reversal hands

Phase 2C: Label all situations bucket-first
  - ≤10 per agent, assigned by tactical theme
  - Output: action, hand_bucket, strategic_role, reasoning

Phase 2D: Independent review

Phase 2E: Comparison report (Plan A's detailed format)
  - Per-situation: old vs new, sequence status, feature changes
  - Disagreement rate with escalation thresholds (<10%, 10-25%, >25%)
  - Disagreements flagged for solver verification

Phase 2F: Solver verification
  - Standard triggers + CALL-disagreement trigger
  └─ Owner gate (reviews comparison + solver results, decides each disagreement)

Phase 3: Train v2.2
  - Leakage check, ML config, export, train, evaluate
  └─ Owner gate

Phase 4: Teaching alignment
  - Notify teaching, L3 review runs, update river-rats-core/
```

## 6. Resource estimate for combined plan

| Phase | Agents |
|---|---|
| Phase 0 | 2 (architect + programmer) |
| Phase 1A-1E | 1 architect + 2 programmers + 1 GTO expert + 1 ML architect |
| Phase 2A-2F | ~40-47 GTO experts + ~20-24 reviewers + 2 calibration + 1 programmer |
| Phase 3 | 1 ML architect + 1 programmer + 1 reviewer |
| Phase 4 | Teaching team (separate) |
| **Total** | **~75-85 agents + 7 owner gates** |

~7-8 sessions. The extra gate on the feature diff (Phase 1C) is
worth it — it's the moment you see whether sequence corruption
actually changed feature values, before spending on labelling.

## 7. One-line summary

**Discard the 2-way (Plan B is right), reconstruct the 3-way
(owner's direction), use qualitative buckets not thresholds
(neither plan had this), compare with Plan A's detail, fill gaps
with new situations designed after seeing what survived.**

---

**For builder: please incorporate this feedback into a final
combined plan and send back for owner review.**
