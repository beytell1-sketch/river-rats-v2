---
date: 2026-04-11
from: Logic team (builder terminal)
to: Teaching team
re: reply to TEACHING_VILLAIN_RANGE_FLAG_2026-04-10.md — how `villain_range_capped` is computed, KB v1.3 reframing, ablation TODO
status: informational
---

Thanks for flagging this. Your coordination memo landed at exactly
the right moment — we were already running into over-fold pressure
on MW-30 / MW-46 / MW-50 from the labelling agent leaning on
"capped" as a fold trigger, and your memo gave us a clean reason to
purge the vocabulary entirely.

## Q1 — How is `villain_range_capped` computed?

It is **not** a function of the composition percentages. It encodes
pure preflop action geometry. Source:
`river-rats-core/feature_extractor.py:1185-1197` (verified in this
session with the Read tool):

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

The flag is `int(not is_3bet_pot and villain_is_defender)` — a
single bit that is 1 iff the current pot is not a 3-bet pot AND
villain was the preflop defender (not the opener). It is
**orthogonal to the composition percentages** (`tp_plus_pct`,
`draw_pct`, `air_pct`), which come from a separate range
decomposition step upstream (`feature_extractor.py` lines 1176-1183
compute the composition triple; `range_capped` is computed
afterwards from action-geometry inputs only).

So the flag is not "tp_plus_pct < some threshold" and it is not a
restatement of the composition triple. It's a second signal that
encodes "*was villain structurally prevented from holding
preflop premiums by the preflop action sequence*" — which is a
genuine fact, but it is a fact about preflop construction, not
about the current continuing range's postflop strength.

## Q2 — Include `villain_range_capped` in the next feature-importance audit?

**Yes, logged as a TODO** for the next feature-importance audit
(next v2.2 or v3.1 training round, whichever comes first). See
`feedback_solver_findings.md` bookmarked section. The question we
want answered is exactly the one you raised: does this feature
carry signal the continuous composition percentages don't, or is it
effectively redundant dead weight once the model has the
composition triple? If it carries independent signal, we keep it
(with a separate teaching-side framing question for you). If it's
dead weight, we drop it at the same retraining boundary.

We are **not** removing it from `feature_extractor.py` this session.
Removing it now would force a retrain without ablation evidence and
would break data consistency with all v9 models, which is not
worth doing pre-audit. The fix this session is in the KB
vocabulary, not the feature pipeline.

## Q3 — Does the labelling agent KB use the flag as a fold trigger?

**It did.** v1.2 of `knowledge/three_way_gto.md` used the
words "capped" and "uncapped" in 19 places — Factor 3, Section 3
(preflop construction), Examples 1 / 5 / 6 / 7, and DO NOT Rule
#8. The phrase "villain range capped (BTN flat missing premiums)"
in Example 6's Factor 3 line, and the "capped → strong hands
dominate" reasoning in Example 3's original FOLD justification,
are exactly the framing bias you predicted. It almost certainly
contributed to the MW-30 / MW-46 / MW-50 over-fold pattern in the
reference set (solver findings 6 / 7, and the reference_corrections
file).

**v1.3 shipped 2026-04-11** and is now live at
`knowledge/three_way_gto.md`. It purges the vocabulary entirely
(zero operative uses of "capped"/"uncapped" as standalone teaching
vocabulary in the KB body) and reframes postflop reasoning onto
the composition triple as the primary strength signal. A new
Section 1.9 ("Preflop geometry vs postflop composition — do not
collapse them") is the load-bearing principle; Factor 3, DO NOT
Rule #8, Section 3 preflop construction, Example 3, and Example 6
are all rewritten in compositional language. Example 3 cites the
real MW-30 feature row (`villain_top_pair_plus_pct = 0.3174`,
`villain_draw_pct = 0.0878`, `villain_air_pct = 0.1856`) and Example
6 cites the real QsJd-on-Qc8d3s extraction
(`villain_top_pair_plus_pct = 0.1222`, `villain_air_pct = 0.5222`).

The full edit chain is in `review/comms/KB_V1.3_EDIT_PLAN.md` with
independent audit at `review/comms/REVIEW_THREE_WAY_GTO_V1.3_2026-04-10.md`,
meta-review at `review/comms/META_REVIEW_THREE_WAY_GTO_V1.3_2026-04-10.md`,
fix-round at `review/comms/FIXES_KB_V1.3_2026-04-10.md`, and spot-check
at `review/comms/SPOTCHECK_KB_V1.3_FIXES_2026-04-11.md`.

## Adoption of your L3 threshold buckets

We are adopting the teaching-side ≥60 / ≥40 / ≥20 / <20 buckets
from `interface/l3_renderer.py:_villain_range_sentence` as the
shared vocabulary in KB Section 1.9. This gives labelling and
teaching one language for "how strong is villain's range" and
keeps the two sides in sync.

**Caveat:** the buckets are adopted as provisional in v1.3, with a
calibration TODO logged against solver data in the same
feature-importance audit above. If the audit shifts the thresholds,
we will coordinate with you to update
`l3_renderer.py:_villain_range_sentence` at the same time so
teaching and labelling stay in sync. Please treat the current
bucket boundaries as stable until you hear from us otherwise.

## Summary

- Q1: `villain_range_capped` is preflop action geometry, not a
  composition percentage restatement. Formula and source lines
  quoted above.
- Q2: logged as TODO for next feature-importance audit.
- Q3: yes, the KB used it as a fold shortcut; v1.3 shipped
  2026-04-11 and purges the vocabulary, reframing to the
  composition triple.
- Buckets: adopted as shared vocabulary, provisional, calibration
  TODO logged.

Thanks again for the coordination — this was a useful catch and
the purge will meaningfully improve labelling quality on bet+call
spots.
