# Opus second-tier 12.5E-F gate evaluation

date: 2026-05-03
from: OPUS-4.7-EVALUATOR (second-tier gate verifier)
to: Main terminal (orchestrator) → owner
re: 12.5E-F gate decision; 12.5E-E re-train landed at median 32/40 (tie-gate band 31-32)
scope: HOW per direction; do NOT pre-empt owner WHAT
status: EVALUATION COMPLETE

---

## Q-eval-1 verdict — H-FEAT premise

- **Validated at feature layer? YES.**
  ml-architect's Q4 Section §"Verdict" predicted blocker importance
  would climb 0.0000 → ~0.02-0.05 once corpus expansion supplied
  reference-set-style RAISE/bluff coverage. Empirical 12.5E-E:
  `nut_flush_block` 0.0000 → 0.0268. The booster has clearly begun
  to split on the feature 2.7% of the time — a non-trivial,
  non-zero, top-15-by-importance signal. **This is not noise.**
  The corpus expansion (T5 NFD-blocker situations + Path B v3.3/v3.4
  RAISE labels for 10 of them, plus 4 CALL counter-examples)
  successfully created a learnable `nut_flush_block × villain_air`
  interaction. Premise vindicated at the layer at which it was
  testable.

- **Validated at gate-score layer? PARTIAL / NO.**
  ml-architect predicted the H-FEAT activation would translate to
  **median 35-37**. Actual median 32. Gate movement was **+1**
  (median 31 → 32) on the canonical 40-hand reference set;
  insufficient to clear the ≥33 promote threshold. The transfer
  assumption — "feature now load-bearing in importance →
  reference-set hands flip" — was over-confident.

- **Reconciliation:**
  The premise had two layers: (i) **feature activation** ("does the
  booster split on `nut_flush_block` once the corpus rewards it?")
  and (ii) **per-hand transfer** ("does that activation flip the 5-7
  shared-cause reference hands?"). Layer (i) is now empirically
  validated. Layer (ii) is empirically refuted at the +4-6 hand
  scale — only 1 net flip on the gto-expert tracked set (MW-42
  flipped, MW-20 newly broke), and exactly 1 hand of net gate
  movement from non-tracked hands. The feature became active but
  the activation pattern did not align with the specific reference
  hands' discriminative axes.

  This is the SAME error class as 12.5D' Q3 (loss-function fix
  worked on held-out, did not transfer to reference set). 12.5D' was
  a "calibration vs distribution" mismatch; 12.5E-E is a "feature
  activation vs per-hand applicability" mismatch. The structural
  pattern recurring across two iterations is: **fixing the next layer
  in the chain does not guarantee the chain's terminal output
  changes when the residual gap is heterogeneous (mix of E-DIST and
  E-FEATURE per gto-expert).** Update prior: validation at an
  intermediate layer is necessary but not sufficient for gate
  movement; future predictions must explicitly model the per-hand
  applicability of the intermediate-layer fix.

  Net: H-FEAT premise CORRECT in mechanism (booster CAN learn the
  feature when corpus supplies the signal); ml-architect's transfer
  arithmetic (5-7 shared-cause hands flip when blocker activates)
  was wrong because 5 of 7 shared-cause hands are dominantly E-DIST,
  not E-FEATURE primary, per gto-expert's per-hand classification.
  The corpus expansion delivered the H-FEAT mechanism but did not
  deliver the E-DIST coverage those 5 hands actually needed.

---

## Q-eval-2 verdict — where the +4-6 hand prediction fell short

Per Section E2 of the trainer report, the 5 stay-wrong hands on
the gto-expert tracked set are MW-17, MW-25, MW-40, MW-45, MW-47.
gto-expert per-hand classification (twice now) gives:

### Per-hand diagnosis (12.5E-E empirical)

**MW-17 (BB AdKs NFD on Jd8d4c, facing CO bet 3-way; expert CALL, model FOLD)**
- Direction: under-aggress (FOLD vs CALL)
- Diagnosis: **E-FEATURE primary.** gto-expert 12.5D' Q1: the model
  FOLDs because `raw_equity 0.251 < pot_odds 0.268` is the dominant
  CALL/FOLD discriminator the booster learned. The discriminating
  signal here is implied odds + nut-FD blocker on a board where
  hero is the relevant blocker, not the existing equity feature.
  12.5E-E corpus added 14 T5 NFD-blocker situations, and
  `nut_flush_block` is now active (0.0268), but the ACTIVATION
  pattern was specifically NFD + face bet + RAISE (10 hands) or NFD
  + face bet + near-zero villain air + CALL (4 hands). MW-17 is
  NFD + face bet + 3-way + CALL with implied-odds reasoning, not
  exactly the activated cluster. The booster learned "NFD-blocker
  → RAISE if villain has air" but did not learn "NFD-blocker →
  CALL with implied odds vs 3-way bet." Feature exists, signal
  partially present, applicability mismatch.

**MW-25 (BTN Ks7s on As9s5d, 4-way checked-to flop; expert BET, model CHECK)**
- Direction: under-aggress (CHECK vs BET)
- Diagnosis: **E-DIST.** gto-expert 12.5D' Q1: monotone-flop
  4-way-checked-through semi-bluff with FD + overcard. The corpus's
  BET examples skew TPGK-thin-value, not semi-bluff-FD-on-monotone-
  4-way. 12.5E-E corpus expansion was T5 (NFD-blocker situations)
  and T7 — not monotone-multiway-checked-through. The corpus still
  doesn't contain analogues. `nut_flush_block` activation is
  irrelevant here because hero has the K-high FD (not the nut FD).
  Pure E-DIST; H-FEAT activation cannot help.

**MW-40 (BTN AhTs on AJ5r, 4-way HJ-opened SRP, checked-to flop; expert BET, model CHECK)**
- Direction: under-aggress (CHECK vs BET)
- Diagnosis: **E-DIST.** gto-expert 12.5D' Q1: TPWK 4-way IP after
  PFR checks. The "PFR-checked-back-Ax 4-way" sub-pattern is rare
  in the corpus; the dominant 4-way-CHECK pattern is "BB defends,
  flop checks through, CHECK is correct." The model generalises
  from the populous pattern. 12.5E-E expansion did not target this
  sub-pattern. `worse_hand_pct = 0.676` exists as a feature but the
  composition signal is not linked to the action-tree position
  (PFR-checks-back). Pure E-DIST; H-FEAT activation cannot help.

**MW-45 (BB 6d6c set on AcKd6h-Q turn, 4-way slowplay then face CO turn lead; expert RAISE, model CALL)**
- Direction: under-aggress (CALL vs RAISE)
- Diagnosis: **E-DIST.** gto-expert 12.5D' Q1: slowplayed set →
  turn lead → raise for value vs AK/two-pair + protection vs
  picked-up draws. `worse_hand_pct = 0.91` and `category = set`
  both exist; signal is in features. The corpus's set-RAISE
  patterns are "set bets/raises immediately"; slowplay-then-raise-
  on-turn-lead is structurally rare. 12.5E-E expansion did not
  target turn-lead-into-raise. `nut_flush_block` activation is
  irrelevant — this is a set, not a nut FD. Pure E-DIST; H-FEAT
  activation cannot help.

**MW-47 (SB AsQs NFD+gutshot OOP, KsJd5s 4-way bet+call; expert RAISE corrected, model CALL)**
- Direction: under-aggress (CALL vs RAISE corrected)
- Diagnosis: **E-DIST + E-FEATURE compound, with H-FEAT now
  partially in play.** This is the canonical NFD-RAISE spot.
  gto-expert 12.5D' Q1: hero IS the nut FD; `nut_flush_block` would
  be 1; pre-12.5E the booster never split on it. Post-12.5E, the
  booster DOES split on `nut_flush_block` 2.7% of the time AND has
  10 corpus exemplars of NFD-blocker → RAISE-with-fold-equity. So
  why didn't MW-47 flip? Two candidate reasons:
  (1) The 10 T5 RAISE exemplars are SB-OOP NFD raises, but their
  configuration (positions, num_opponents, action sequence,
  villain_air_pct profile) may differ from MW-47's specific
  4-way-bet+call OOP profile. The booster learned a narrower
  pattern than the reference hand's pattern.
  (2) The cap=3.0 hybrid weighting may still under-amplify the
  RAISE class on the specific MW-47 feature vector because
  `villain_air_pct` for MW-47 (4-way bet+call) is structurally
  different from the average T5 RAISE exemplar.
  This hand is the BEST candidate for cap-retuning helping
  (Direction B) — the feature is now active, the corpus has
  closer exemplars than before, but the booster's split point /
  weighting may not be calibrated for this exact specification.

### Aggregate

- **3 of 5 stay-wrong hands are pure E-DIST** (MW-25, MW-40, MW-45)
  — corpus expansion did not target their patterns; H-FEAT
  activation provides zero leverage. Only Direction C (further
  corpus expansion targeting these specific patterns) can move
  them.

- **1 of 5 is E-FEATURE primary** (MW-17) — the discriminating
  signal is implied-odds + 3-way reasoning that the 59-feature
  surface does not encode. H-FEAT activation provides marginal
  leverage (NFD-blocker is now active) but the canonical
  CALL-with-implied-odds reasoning is missing. Direction C with
  T7-style additions could partially help; new feature-engineering
  would help most.

- **1 of 5 is compound E-DIST + E-FEATURE with partial H-FEAT
  leverage** (MW-47) — the booster IS now splitting on
  `nut_flush_block` and DID see closer exemplars. Cap retuning
  (Direction B) has the highest leverage on this specific hand.

- **Newly-broken MW-20** (over-aggress, RAISE vs CALL): consistent
  with the trainer's hypothesis that the new RAISE-class corpus
  signal is teaching the booster to fire RAISE more readily. This
  is exactly what ml-architect Q5 warned about for cap=4.0+ — and
  it materialised at cap=3.0 because the corpus expansion shifted
  RAISE supply from 28 (12.5D') to ~38-40 (12.5E-E, post-T5
  additions). The booster has slightly over-rotated toward RAISE
  on configurations that resemble T5 exemplars.

- **Held-out CHECK recall dropped** 0.939 → 0.815 (−0.124) and
  CHECK precision rose to 1.000 — the model now under-predicts
  CHECK and over-predicts BET (BET precision dropped 0.824 →
  0.706). This is consistent with the corpus shift toward more
  aggressive labels, and is a leading indicator that further
  cap-up or further RAISE-supply additions risk MORE
  newly-broken hands.

The +4-6 hand prediction's structural error: ml-architect treated
all 7 shared-cause hands as approximately equally responsive to
H-FEAT activation. gto-expert's per-hand E-DIST/E-FEATURE
classification (which was twice-confirmed by 12.5D' and is
re-confirmed by 12.5E-E empirics) shows only ~2 of 7 are
H-FEAT-primary candidates. The realistic per-hand-flip-yield from
H-FEAT activation alone was always ~1-2 hands, not 4-6.

---

## Q-eval-3 — per-direction HOW

### A — PROMOTE at 32/40

- **Probability of "the right call": ~10-15%.**
  This frames promotion as right ONLY if owner judgment weights the
  secondary criteria (held-out class metrics; per-class balance;
  std tightening 0.49 → 0.40; H-FEAT validation; broader feature
  surface for future iterations) above the canonical reference-set
  regression of 1 hand. Most teams with a hard ≥33 gate would not
  ship a regression; the case for shipping rests on
  "production inference distribution may resemble the corpus more
  than the reference set," which is uncertain and unverifiable.

- **Strongest case FOR:**
  1. H-FEAT validation establishes a load-bearing feature that
     unblocks future iterations (without an active blocker feature,
     no further blocker-style work could be motivated; with one
     active, future gains are credible).
  2. Per-class held-out improvements: BET recall +0.176, RAISE
     recall +0.429 vs 12.5D, std tightened 0.49 → 0.40. If
     production inference distribution is corpus-like (passive-
     skewed user actions), production users see the calibration
     gain, not the reference-set gap.
  3. Mean improvement 30.6 → 32.2 (+1.6 hands across seeds) —
     median is 1 unit but mean is 1.6, suggesting the distribution
     is genuinely tighter and slightly higher.
  4. v9-3way-v2.2 baseline 33/40 was achieved on a 38/45-feature
     surface; v9-student 32/40 on 59-feature surface preserves
     the wider feature platform for future work.

- **Strongest case AGAINST:**
  1. Canonical reference set is the contractual gate. Shipping
     a regression on the canonical gate normalises a new pattern:
     "we promote based on auxiliary metrics when the canonical
     gate misses by 1." This is a slippery slope owner has been
     explicit about avoiding (`feedback_no_deadlines.md`,
     `feedback_quality_default_no_ask.md`).
  2. Newly-broken MW-20 is a NEW miss not previously in the
     gto-expert tracked failure set — the model has acquired a
     defect (over-aggression) it did not previously have. The
     +1 net gate movement masks a worsening on a previously-correct
     hand. From a pure "is-the-model-better?" standpoint, the
     answer is genuinely ambiguous.
  3. Held-out CHECK recall dropped 0.939 → 0.815 (−0.124) — the
     model now misclassifies passive spots more often. This is
     the OPPOSITE direction of the pattern v9-3way-v2.2 was
     calibrated for and is an unfavourable trade in production.

- **HOW design (if picked):**
  Ship `gto_model_v9_student.json` (chosen seed 2) to
  `river-rats-core/models/`. Update model card with explicit
  regression note: "v9-student is canonical for 59-feature paths
  with the following known regressions vs v9-3way-v2.2: MW-20 newly
  broken (over-aggression), 5 of 7 gto-expert shared-cause hands
  remain wrong (E-DIST primary). Held-out class-recall gains:
  BET +0.176, RAISE +0.429 vs 12.5D unweighted." Pair the ship
  with an EXPLICIT next-iteration commitment to Direction C
  (corpus expansion targeting the 3 E-DIST stay-wrong hands) or
  abandonment timer (e.g., "if 12.5G or corpus-expansion does not
  close the gap by date X, revert and revisit"). Without a
  forward path, this becomes "interim ship that became terminal."

---

### B — 12.5G cap retuning sweep

- **Probability of closing gap to ≥33: ~10-15%** (revised UP from
  ml-architect Q5's ~5%).

- **Reasoning: with H-FEAT now active, does cap tuning have more
  leverage?**
  ml-architect's Q5 5% prior was computed under the H-FEAT-inactive
  regime: cap controls amplification of patterns the model has
  learned, and the model had not learned the blocker patterns. That
  regime no longer holds. As of 12.5E-E, the booster IS splitting
  on `nut_flush_block` 2.7% of the time, AND there are 10 RAISE +
  4 CALL T5 exemplars in the corpus. This means cap tuning now has
  a NEW lever: amplifying the (just-learned, marginal) blocker-
  pattern signal. Specifically MW-47, where the feature is now
  active and the closest corpus exemplars exist, is the best
  candidate hand for cap-up to flip. Cap-up may also push MW-25/40/45
  (E-DIST) the wrong way (over-amplify aggressive corpus patterns
  on situations whose features don't match), risking more
  newly-broken hands.
  Cap-down is empirically NOT helpful — gto-expert 12.5D' Q3
  estimated cap=2.0 would drop held-out RAISE recall toward 0.583
  and possibly drop reference-set median below 32. The asymmetry
  of the cap dimension at this point suggests cap=4.0 is the only
  informative point; cap=2.0 and 2.5 are likely regressions.

  Honest probability decomposition: if cap=4.0 flips MW-47 (50%
  chance given H-FEAT activation + closer exemplars), and breaks
  no new hands (60% chance — already 1 newly-broken at cap=3.0),
  median goes 32 → 33. Joint probability ≈ 0.5 × 0.6 = 30% for
  cap=4.0 alone clearing the gate. Across the sweep (2.0, 2.5, 4.0),
  one cap value clearing ≥33 is ~30% × (probability cap=4.0 is the
  best of the three on reference set). I'd estimate the integrated
  probability of ANY cap producing ≥33 at ~10-15% — higher than
  ml-architect's 5% prior because of the new empirical context, but
  still low because the cap dimension does not address the 3 pure-
  E-DIST hands at all.

- **HOW design (if picked):**
  - 3-point cap sweep: `cap = 2.0, 2.5, 4.0` — keep the existing
    `pure-confidence × class_weight` formula; only the cap value
    changes.
  - Re-use the 12.5E-E trainer module unchanged; same 5-seed
    protocol (seeds 0-4); same 604-hand corpus
    (`corpus_combined_604_2026-05-05.jsonl`); same warm-start
    anchor (v9-3way-v2.2); same hyperparameters.
  - Report: per-seed solver-corrected litmus per cap; per-class
    held-out metrics per cap; per-hand outcome on the gto-expert
    9-hand tracked set + MW-20 (newly-broken-watch); P1 blocker
    importances per cap. Ship the model only if any cap produces
    median ≥33 AND no new hands are broken vs 12.5E-E baseline.
  - Specifically targeted boundary cases: MW-47 (canonical NFD-RAISE,
    H-FEAT active, closer corpus exemplars). MW-20 (newly-broken at
    cap=3.0) is the watch case for over-rotation on cap-up.
  - Cost: 1 builder day (3 trainer runs × 5 seeds = 15 model fits;
    each ~5-10 min on 604 hands). No new spend on labelling, no
    QC on new corpus. ~$5-10 of compute. 1 PR with the swept
    artefacts as research output (no model promoted unless gate
    clears).
  - Decision criterion: any cap producing solver-corrected median
    ≥33 with no new newly-broken hands ships; otherwise this
    direction is exhausted, and orchestrator/owner pivot to C or D.

---

### C — Corpus expansion 110→150-200

- **Probability of closing gap to ≥33: ~50-60%** (lower than
  gto-expert 12.5D' Q3's 50-70% range because the empirical
  12.5E-E result already absorbed ~30 hands of the 100-hand
  expansion budget without delivering the predicted +4-6 movement
  — the marginal yield per corpus hand has empirically been
  lower than gto-expert's prior assumed).

- **Specific template families to expand:**
  Looking at the 5 stay-wrong + 1 newly-broken empirical residuals:
  - **3 E-DIST hands** (MW-25, MW-40, MW-45): each has a distinct
    structural pattern that's not in the corpus. Need targeted
    new template families:
    - **T8 (proposed):** monotone-flop multiway-checked-through
      semi-bluff IP with FD + overcard (covers MW-25). 12-15
      hands targeting BET label on this configuration; 4-5
      counter-examples (CHECK label) for hands without enough FD
      equity or fold equity.
    - **T9 (proposed):** PFR-checks-back-Ax-multiway-IP TPWK
      thin-value-bet (covers MW-40). 12-15 hands targeting BET;
      4-5 counter-examples.
    - **T10 (proposed):** slowplay-set-then-face-turn-lead-multiway
      raise-for-value (covers MW-45). 8-10 hands targeting RAISE;
      3-4 counter-examples.
  - **1 E-FEATURE primary hand** (MW-17): no further T-template can
    fully fix this without feature engineering. Best done as a
    secondary feature-engineering iteration AFTER corpus expansion
    — adding an `implied_odds_proxy` or `nut_blocker_call_signal`
    feature. For now, T7-extension with 8-10 NFD-CALL situations
    that look like MW-17's profile (3-way, face bet, NFD blocker,
    overcards) may partially help by analogy.
  - **MW-47 already partially addressed** by current 12.5E-E
    expansion + cap=3.0; further T5 expansion (5-10 more SB-OOP
    NFD RAISE situations specifically matching MW-47's positional
    profile) would push reliability higher.
  - **MW-20 newly-broken** is over-aggression telling us the T5
    RAISE expansion was effective enough to over-rotate on
    similar-but-not-identical configurations. New T-templates need
    counter-example density: for every T5/T8/T9/T10 BET/RAISE
    exemplar, at least 1 in 3 should be a same-feature-profile
    CALL/CHECK exemplar to prevent over-rotation.

- **HOW design (if picked):**
  - **Sizing:** 50-90 new hands across 4 template families.
    Conservative end (50): T8 = 15, T9 = 15, T10 = 10, T7-extension
    = 10 = total 50 hands. Aggressive end (90): each family +5 to
    +10, total 90. 50 brings corpus to 654 hands; 90 brings to 694
    hands — both within design §4 escalation range (150-200 was
    cumulative; we'd be at corpus_revision_700 cumulatively).
  - **Labelling protocol:** identical to 12.5E (5 labellers, MEDIUM/
    HIGH/CERTAIN confidence framework per
    `feedback_bucket_first_labelling.md`); solver-verify per
    `feedback_solver_findings.md`; use exactly the GTO Wizard
    flop 25%/66% / turn 33%/75% / river 33%/75%/150% solver bet
    sizes per `feedback_solver_aligned_sizing.md`.
  - **Source situations:** for each template, pre-design 15-20
    candidate situations from solver databases matching the
    failure-mode template; labellers pick the cleanest 12-15 per
    family. No improvisation — situations must match the template
    spec.
  - **Re-train (12.5G or 12.5H):** same trainer module, same
    hyperparameters, cap=3.0. Predicted outcome: 2 of 3 E-DIST
    hands flip (MW-25 + MW-45 with high confidence; MW-40 medium);
    MW-47 reliability tightens; MW-20 newly-fixed by counter-
    example density. Median target: 33-35.
  - **Cost:** 2-3 weeks corpus work (labelling + solver-verify +
    QC join-cardinality gate + integration); 1 builder day re-train.
    Labelling spend approx $X (depends on labeller costs at
    river-rats-v2 standard rate) — owner has budget visibility I
    don't. Compatible with `feedback_no_deadlines.md`: expand data
    to fit the poker.
  - **Risk:** the empirical shortfall from 110-hand expansion to
    +1 hand suggests the marginal yield per labelled hand is
    lower than gto-expert's prior. Plan for a 2nd round if the
    1st round delivers ≤+2 hands; budget 4-5 weeks total elapsed
    in the worst case.

---

### D — Abandon migration; v9-3way-v2.2 stays canonical

- **Probability of "the right call given evidence": ~20-30%.**
  The case for abandonment got WEAKER post-12.5E-E. ml-architect Q4's
  H-FEAT premise is now empirically validated at the feature layer.
  Abandoning closes the line on a feature platform that just
  cleared its first major activation hurdle. That said, the case
  for abandonment is still credible if owner judges that the
  marginal yield per iteration (12.5D 31, 12.5D' 31, 12.5E-E 32)
  is too slow given the corpus + retrain investment, and that
  v9-3way-v2.2's 33/40 is acceptable for the 33/40 region.

- **Strongest case FOR:**
  - Two iterations of "the next layer of the chain" (12.5D' loss
    fix → 12.5E-E corpus expansion) produced 0 + 1 = 1 hand of
    gate movement total. v9-3way-v2.2 holds at 33/40 with a
    simpler feature surface (45 vs 59 features) and is already
    canonical.
  - The compound effort (labelling, training, evaluation) per
    iteration is multi-week. If the next iteration (12.5G corpus
    expansion) yields another +1 to +2, that's 2-3 weeks for
    median 33-34, marginal vs v9-3way-v2.2's 33.

- **Strongest case AGAINST:**
  - H-FEAT validation just landed empirically. Abandoning at the
    moment of first-feature-activation forfeits the platform
    investment.
  - ~$X spent on 110-hand corpus expansion is sunk; abandonment
    means that spend produced research artefact only.
  - No OTHER credible path to a wider feature surface is in
    flight — abandonment closes the only active migration to a
    59-feature platform.

- **HOW design (if picked) — Variant 3a per ml-architect 12.5D' Q6:**
  - Keep `train_model_v9_student.py`, `STUDENT_FEATURE_COLUMNS_V9`,
    the 4 P1 blocker feature definitions, the 17-test suite, and
    the 604-hand corpus on master as research artefacts.
  - Add an abandoned-banner to `train_model_v9_student.py` top of
    module:
    ```
    """
    ABANDONED 2026-05-XX per 12.5E-F gate decision.
    Retained as research artefact: established that
    (a) hybrid weighting cap=3.0 closes held-out class collapse
        (12.5D'); (b) corpus expansion to 110 T5/T7 hands activates
    nut_flush_block feature in booster (12.5E-E, 0.0000 → 0.0268);
    (c) reference-set median moved 31 → 32, did not clear ≥33 gate.
    Stay-wrong hands MW-17/25/40/45/47 are E-DIST/E-FEATURE
    residuals not addressable by hybrid-weighting + 110-hand
    corpus expansion. Future work must (i) target E-DIST stay-wrong
    patterns with new template families, AND (ii) consider feature
    engineering for MW-17-style implied-odds reasoning.
    Do not promote without (a) corpus rebuild AND (b) re-evaluation.
    v9-3way-v2.2 remains canonical.
    """
    ```
  - Update `reference_corrections.md` (or model card) to record
    that v9-3way-v2.2 is canonical at 33/40; v9-student trainer
    is research-only.
  - PR scope: ~10 lines (banner + model-card update + 1 doc note).
    No revert, no LOC removed from sacred core. Reviewer checklist:
    confirm banner text, confirm v9-3way-v2.2 path remains active
    in `oracle_router.py`.
  - Cost: 1 builder day; 1 reviewer day. No re-train.

---

## Brief — methodology assessment for owner

**Highest-probability gap-closer (honest poker+ML judgment;
NOT pre-empting WHAT):**

**Direction C (corpus expansion 110 → 160-200) at ~50-60% probability
to clear ≥33** is the most credible single direction. Reasoning:
- Empirical 12.5E-E confirms the H-FEAT mechanism works when corpus
  supplies the right exemplars. This directly supports doing more
  of what worked.
- 3 of 5 stay-wrong hands are pure E-DIST — only data can move
  them. Cap retuning (B) cannot address E-DIST. Promotion (A) and
  abandonment (D) decline to address them.
- The empirical 12.5E-E shortfall (+1 hand from 110-hand expansion
  vs predicted +4-6) is informative: it tells us the marginal yield
  per labelled hand is lower than priors estimated, which means a
  larger expansion (+50-90 more hands) is needed, not that the
  approach is wrong.

**Possible compound: B then C.** Run the 1-day cap=4.0 sweep first
(low cost, ~30% chance of flipping MW-47 alone for median 33). If it
clears the gate, ship. If it doesn't, fold the empirical evidence
(actual cap=4.0 reference-set behaviour, with H-FEAT now active)
into the C corpus-design rationale. This sequencing extracts the
most signal from the H-FEAT validation moment without committing
3 weeks of labelling work upfront.

**Honest update from prior predictions:**
- ml-architect 12.5D' Q4 predicted median 35-37 from corpus
  expansion. Actual 32. Update: predictions of multi-hand reference-
  set transfer must factor in per-hand E-DIST/E-FEATURE
  classification, not just feature-importance activation.
- gto-expert 12.5D' Q3 estimated Direction D at 50-70% probability.
  Update: with empirical evidence of lower-than-expected marginal
  yield per corpus hand, the realistic probability for the next
  expansion increment is ~50-60% (low end of original range), and
  may need an explicit sizing top-up.
- The structural lesson (relevant to future tier-up evaluations):
  **validation at one layer of a chain does not predict gate
  movement when the residual is heterogeneous.** Future H-FEAT-
  style premises should be paired with a per-hand applicability
  forecast at design time, not just a population-level activation
  forecast.

This is methodology only. Owner picks WHAT among A/B/C/D (or
B-then-C, or any other compound) for cost/timeline/strategic
reasons. The HOW for each is laid out above; orchestrator + owner
own the WHAT decision.
