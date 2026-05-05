---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-C resolution — accept the 110 labels + add v3.4 documentation; T1 deferred; proceed to 12.5E-D
status: DIRECTIVE — orchestrator decision on PR #142 BLOCKED
---

# 12.5E-C resolution — accept labels + v3.4 doc + proceed

Builder PR #142 BLOCKED on stop condition: PILOT_600 consensus = CALL 4/5 (predicted RAISE). Builder framed 5 plausible directions (B'/B''/C/D/E) without recommending.

## Orchestrator decision: hybrid B' + D

**Accept the 110 labels as final.** Empirical analysis is clear: the 4 T5 CALL hands all have `villain_air_pct` ≈ 0.01-0.02 (heart-suit feature artifact in canonical preflop range distributions). Labellers correctly reasoned that "suspending the 0.20 threshold doesn't manufacture fold equity from a 0-2% air range" — defensible GTO conclusion, not a labeller bug. The 10 T5 RAISE hands have `villain_air` ≈ 0.15-0.20 where v3.3 carve-out applies correctly.

**The labels are GTO-correct as labelled.** Re-labelling would produce the same outcome unless we change the situations themselves (Path E), which contradicts Path B "T5 unchanged."

**Document v3.4 with clause (e).** v3.3 omitted what labellers correctly inferred: even with the bet+call multiway carve-out, RAISE EV requires SOME villain air to fold. Path B' adds this clause for documentation/posterity. The labels don't change — labellers were already labelling per implicit v3.4.

**The migration's premise survives empirically — partially.** P1 blockers ARE load-bearing for RAISE in spots where fold equity exists. They are NOT load-bearing in zero-air spots (where no action manufactures EV from blockers). The booster will learn `nut_flush_block × villain_air_pct` interaction — a richer training signal than "blockers alone → RAISE."

**T1 full miss (14/14 CHECK against BET intent) deferred to 12.5E-F outcome.** Labellers invoked DO NOT Rule 2 ("don't barrel draws into 3+ opponents on monotone boards") — also defensible poker reasoning. Whether T1 rework is needed depends on whether 12.5E-E re-train + 12.5E-F gate pass on MW-25 without it. Premature optimization to redo T1 now.

## LEAD-PROGRAMMER — what you do

Branch: continue on `programmer/phase125e-c-labelling-2026-05-05` (same branch as PR #142). Force-push amendment.

### LEAD-PROGRAMMER (architect hat — author v3.4 prompt)

Create `prompts/gto_labeller_v3.4.md` = `prompts/gto_labeller_v3.3.md` verbatim + the following addition appended after the v3.3 Fix 2.1 section:

```
### KB §1.7 OVERRIDE refinement (v3.4 — Fix 2.1.1)

`[v3.4 addition Fix 2.1.1]` Empirically motivated by the 12.5E-C
labelling round (2026-05-05): under v3.3 Fix 2.1, T5 H-FEAT primary
canonicals split 10 RAISE / 4 CALL based on `villain_air_pct`. The
4 CALL hands all had `villain_air_pct ≈ 0.01-0.02`; labellers
correctly reasoned that suspending the v3.2 0.20 threshold does
not manufacture fold equity from a near-zero-air range. v3.4 adds
clause (e) to make this implicit reasoning explicit.

OVERRIDE refinement: KB §1.7 (Nut FD + nut blocker → RAISE)
re-applies in bet+call multiway lines (per v3.3 Fix 2.1) ONLY
when, in addition to clauses (a)/(b)/(c)/(d), clause (e) holds:

- (e) `villain_air_pct >= 0.05` (a minimum air floor below which
  fold equity is structurally absent regardless of action geometry).

When `villain_air_pct < 0.05`, the v3.3 carve-out does NOT trigger;
v3.2 default behavior applies (CALL preferred). The 0.05 floor is
an EV-floor on raise viability, NOT a re-introduction of the v3.2
0.20 threshold for HU lines — bet+call multiway with `villain_air`
in [0.05, 0.20] still gets the v3.3 carve-out.

Calibration anchor: PILOT_599 (RAISE — `villain_air_pct = 0.153`,
clause (e) satisfied). Counter-anchor: PILOT_600 (CALL —
`villain_air_pct = 0.020`, clause (e) fails).

This v3.4 refinement supplements v3.3 Fix 2.1; v3.3's threshold
suspension remains in force for bet+call multiway lines where
`villain_air >= 0.05`. v3.4 adds the lower floor.
```

The 0.05 floor is empirically anchored: it cleanly separates the 4 CALL hands (0.01-0.02) from the 10 RAISE hands (0.15-0.20) in PR #142's labels. Future labelling rounds invoke v3.4.

### LEAD-PROGRAMMER (default — implementation)

Amendment scope (force-push to PR #142):

| File | Status | Change |
|---|---|---|
| `prompts/gto_labeller_v3.4.md` | NEW | Created per architect-hat above |
| `data/corpus_revision_125e_labels_2026-05-05.jsonl` | UNCHANGED | 110 labels are final; do NOT re-label |
| `data/corpus_revision_125e_labels_raw_2026-05-05.jsonl` | UNCHANGED | 550 raw responses are final |
| `scripts/dispatch_mass_labelling.py` | UNCHANGED | (already updated in original PR #142 to be version-agnostic) |
| `scripts/collect_mass_labels.py` | UNCHANGED | (already updated to glob version-agnostic) |
| `review/comms/BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md` | UPDATE | Rename or rework: title changes from "BUILDER BLOCKED" to "BUILDER REPORT 12.5E-C — empirical labels + v3.4 documentation"; preserve all empirical analysis (full data, per-template alignment, T1/T5/T7 findings); add §"Resolution per orchestrator directive" documenting accept-labels + v3.4 + T1 defer |

Diff scope: 6 files (was 5 + 1 new v3.4 prompt; PR title changes from BLOCKED to RESOLVED).

### Stop conditions (amendment)

- v3.4 prompt drift from spec → STOP (clause (e) wording must match directive verbatim)
- Any change to the 110 labels → STOP (labels are final per orchestrator decision)
- Any change to T5 hand definitions → STOP (Path B "T5 unchanged" still binds)
- BUILDER_REPORT renaming/reworking introduces non-trivial new content beyond §"Resolution" → STOP, route to orchestrator

### LEAD-PROGRAMMER (gto-expert hat — sanity check before force-push)

Confirm that under v3.4 with clause (e):
- PILOT_599 (`villain_air_pct = 0.153`): v3.4 carve-out triggers (clauses a-e all satisfied) → predicted RAISE; matches actual consensus ✓
- PILOT_600 (`villain_air_pct = 0.020`): clause (e) fails → carve-out does NOT trigger; v3.2 CALL applies → predicted CALL; matches actual consensus ✓
- All 10 T5 RAISE hands (villain_air 0.15-0.20): clause (e) holds → carve-out triggers → predicted RAISE ✓
- All 4 T5 CALL hands (villain_air 0.01-0.02): clause (e) fails → CALL ✓

If any of these fail under v3.4 wording, STOP. Otherwise proceed.

## QC stream — what you audit on amended PR #142

Standalone QC SOLO-routed per memory.

5 audits:
1. **Diff scope** — exactly 6 files (5 from original PR + 1 new v3.4 prompt); confirm 110 labels unchanged (`git diff master..pr-head data/corpus_revision_125e_labels_2026-05-05.jsonl` should show 0 changes from prior commit)
2. **Citation existence** — every file:line citation in builder report exists at master HEAD
3. **v3.4 prompt verbatim match** — diff v3.4 Fix 2.1.1 section against this directive's spec character-for-character; HOLD on any drift
4. **NEW: v3.4 falsification with empirical anchors** — verify v3.4 wording correctly classifies PILOT_599 (RAISE) and PILOT_600 (CALL) under the documented clause set; if either fails, HOLD (v3.4 wording is wrong)
5. **NEW: Label-final invariance** — verify the 110 consensus labels and 550 raw labels are byte-identical to what's already on the PR branch; any drift indicates a re-labelling attempt outside the directive

Post `REVIEW_QC_PHASE125E_C_AMEND_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER (architect hat) authors v3.4 prompt
2. LEAD-PROGRAMMER (gto-expert hat) sanity-check on PILOT_599/600 + 14 T5 hands under v3.4
3. LEAD-PROGRAMMER updates BUILDER report with §"Resolution" section
4. Force-push to PR #142
5. Standalone QC pre-merge audit
6. On QC APPROVE: orchestrator merges PR #142
7. **12.5E-D dispatched** (corpus QC phase per design §8.D + NIT-1 PLAN §3.T8 cleanup + PILOT_595 design_note cosmetic + new T1/T7 partial-match documentation)

## What's blocked / what's queued

**Blocked:**
- PR #142 merge → on builder amendment + standalone QC APPROVE
- 12.5E-D dispatch → on PR #142 merge

**Queued (tracked, no separate owner ask):**
- T1 full-miss assessment → defer to 12.5E-F outcome (if MW-25 still fails, T1 rework happens; if not, no rework)
- T7 split → empirical observation; Section E in 12.5E-E trainer report will document whether T7's mixed labels help or hurt MW-17 reference-set performance
- Model-drift assessment (Sonnet labels for 110; Sonnet labels for 494) → no drift expected since both used Sonnet × 5; documented at 12.5E-E
- NIT-1 PLAN §3.T8 cleanup → at 12.5E-D
- PILOT_595 design_note cosmetic → at 12.5E-D
- 12.5G cap retuning post-12.5E-F (queued from PR #135 addendum)
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations before declaring blueprint design complete) → builder formalizes in `docs/PROCESS_GUIDE.md` at next available cycle

## Methodology lessons (added to forward-record at this round)

1. **Labellers exercise GTO judgment over protocol** — when a protocol's clause set has a real EV-theoretic gap, labellers correctly fill it. v3.3 → v3.4 is the documentation catching up to labeller reality. Future protocol revisions should anticipate clauses labellers will infer.

2. **`feature_extraction artifacts can mask EV-theoretic equivalence`** — heart-suit broadway combos produce different `villain_air_pct` than spade-equivalents on isomorphic boards. This is a feature-extraction property, not a poker reality. The booster training on these mixed labels will learn the artifact, which may or may not generalize to production. Note for 12.5E-E trainer report.

3. **Pilot-first standing rule (`feedback_pilot_first_for_long_jobs.md`) was correct** — even though builder ran the original 550-batch design (because amendments came in too late for this cycle), the empirical pattern would have been visible at 70-call pilot scale. ALL FUTURE batches use pilot-first. No exceptions.

4. **Owner-WHAT decisions on partial empirical successes** — orchestrator decision per `feedback_quality_default_no_ask.md` reinforced 2026-05-04: accept-labels (Path D-equivalent) is the slow-quality path when labels are GTO-correct, even if they don't match all design predictions. The empirical reality teaches the booster more than forcing labels to match design intent.

## References

- 12.5E-C BLOCKED report: PR #142 (open, branch `programmer/phase125e-c-labelling-2026-05-05`)
- 12.5E-C redesign (pilot+full superseded by reality of 550-batch run): master `ddc812e` (PR #143)
- 12.5E-C Opus amendment (also superseded by Sonnet-actual run): master `ce1528a` (PR #141)
- 12.5E-C original dispatch: master `e7d7843` (PR #140)
- v3.3 prompt (clause set this v3.4 refines): `prompts/gto_labeller_v3.3.md` (master `0eaac06`)
- 12.5E design (12.5E-A): master `bad1396` (PR #133)
- Memory: `feedback_pilot_first_for_long_jobs.md` (NEW 2026-05-05; rule confirmed by 12.5E-C empirical evidence), `feedback_quality_default_no_ask.md` (reinforced 2026-05-04), `feedback_river_rats_team_structure.md`, `feedback_orchestrator_output_structure_per_party.md`, `feedback_qc_routing_when_standalone_active.md`

**Status: 12.5E-C RESOLVED. 110 labels final. v3.4 documentation pending. T1 deferred. LEAD-PROGRAMMER amends PR #142 (architect hat + report update). After QC APPROVE: merge → 12.5E-D dispatch.**
