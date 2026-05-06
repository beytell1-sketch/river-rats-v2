# Opus second-tier 12.5H-F gate evaluation

date: 2026-05-06
from: OPUS-4.7-EVALUATOR (second-tier gate verifier)
to: Main terminal (orchestrator) -> owner
re: 12.5H-F gate decision; 12.5H-E re-train landed at median 32/40 unchanged from 12.5E-E
scope: HOW per direction; do NOT pre-empt owner WHAT
status: EVALUATION COMPLETE

---

## Q-eval-1 — H-FEAT +85% interpretation

**Verdict: hybrid (a) + (c) — real but mistargeted.** The feature is
genuinely load-bearing for the booster's RAISE/CALL discrimination on
in-distribution corpus rows, but the 5 stay-wrong reference hands are
NOT in the cluster the activated feature serves.

### Reasoning from Section C top 15

`nut_flush_block` at 0.0496 is the **5th-most-important feature** in
the chosen-seed model — above `is_monster` (0.0416), `equity_vs_range`
(0.0361), `better_hand_pct` (0.0321), `has_straight_draw` (0.0310). It
sits in a tier with `flush_block_pct` (0.0458), `flush_draw_block_pct`
(0.0528), `raw_equity` (0.0447). This is not noise — the booster is
genuinely splitting on this feature at a rate comparable to its primary
equity features. Refutes (b) epiphenomenal.

### Cross-seed instability tells us where the feature fires

Per Section F cross-seed table: `nut_flush_block` median 0.0496, mean
0.0465, std 0.0430, range 0.0000-0.0910, 60% of seeds clear the 0.02
floor. That bimodal-with-wide-range pattern says: when the booster
finds a useful split, the split is large; when it doesn't, it ignores
the feature entirely. This is exactly the signature of a feature that's
load-bearing on a SUBSET of training rows (the T5 + T7-ext + T-RAISE-
stabilize NFD-blocker exemplars where `nut_flush_block=1` correlates
with RAISE/CALL labels) but does not generalize across all rows.

### Reconciling with Section B per-hand

The 5 stay-wrong hands' compositions versus `nut_flush_block`:

- **MW-17** (BB AdKs NFD on Jd8d4c, 3-way face bet, expert CALL): hero
  IS the nut FD; `nut_flush_block=1`. The booster's learned association
  is "nut_flush_block + face_bet -> RAISE on T5 SB-OOP profile" or
  "+villain_air -> RAISE." MW-17 is 3-way face-bet with implied-odds
  CALL reasoning, NOT a raise-with-fold-equity profile. The activated
  feature fires the WRONG direction here (or doesn't fire at all
  because other features dominate). Evidence: 12.5H-targeted MW-17
  with T7-ext SUITED template, 12 hands; still FOLD. The booster
  learned the SUITED-NFD pattern but linked it to RAISE-class behavior
  in the corpus, not to CALL-with-implied-odds.

- **MW-25** (BTN Ks7s on As9s5d 4-way checked-through, expert BET):
  hero is the K-high FD, NOT nut FD. `nut_flush_block=0`. H-FEAT
  activation is structurally irrelevant. Pure E-DIST.

- **MW-40** (BTN AhTs on AJ5r 4-way HJ-checked, expert BET): hero is
  rainbow TPWK; no flush draws on board. `nut_flush_block` not active
  at all. Pure E-DIST. H-FEAT cannot help.

- **MW-45** (BB 6d6c set on AcKd6h-Q turn slowplay+lead, expert RAISE):
  hero is a set, not a flush draw. `nut_flush_block=0`. Pure E-DIST.

- **MW-47** (SB AsQs NFD+gutshot OOP, KsJd5s 4-way bet+call, expert
  RAISE): hero IS nut FD; `nut_flush_block=1`. T-RAISE-stabilize added
  12 hands targeting exactly this profile. The booster's learned RAISE
  signal does fire, BUT under-aggresses: model says CALL, not RAISE.
  The 12 stabilize hands gave it confidence to attend to the feature
  but didn't push the discriminative mass over the CALL/RAISE boundary
  for this specific 4-way-bet+call positional profile.

### Verdict synthesis

(a) is partially true: feature is load-bearing for SUITED-NFD-RAISE
hands (think: hands resembling T5 + T7-ext + T-RAISE-stabilize
exemplars). The 60% seed-pass rate for the 0.02 floor confirms this
across seeds.

(c) is the dominant story: only 2 of 5 stay-wrong hands (MW-17, MW-47)
have `nut_flush_block=1` at all, and even those have positional/
sequence profiles outside the activated cluster. 3 of 5 (MW-25/40/45)
have `nut_flush_block=0` entirely; H-FEAT activation is structurally
incapable of moving them.

The +85% relative jump (0.0268 -> 0.0496) reflects the corpus expansion
specifically reinforcing the SUITED-NFD-blocker -> RAISE association,
not a generalized blocker-as-discriminator capability. Right
mechanism, narrowly-targeted activation.

---

## Q-eval-2 — corpus expansion failure mode

**Verdict: (a) wrong-diagnosis-for-3-of-5, (c) underpowered-for-2-of-5;
(b) wrong-implementation rejected as primary.**

The 90-hand corpus expansion empirically failed because the diagnosis
treated 5 disparate failure modes as if they shared a common axis (data
density on E-DIST patterns). gto-expert's 12.5D' per-hand classification
already established 3 of 5 as pure E-DIST (MW-25/40/45) requiring
template-specific corpus coverage, 1 as E-FEATURE primary (MW-17), and
1 as compound (MW-47). The 12.5H expansion delivered 12-15 hands per
template across 4 templates, which:

- For 2 hands, was approximately the correct intervention but
  underpowered (need bigger N to overcome competing-pattern noise).
- For 3 hands, was the wrong axis entirely.

### Per-hand reasoning (clearest signal first)

**MW-25 (T8' monotone-FD: 12-15 hands; expert BET, model still CHECK)**
- Wrong diagnosis or underpowered? Diagnostic-level call: BORDERLINE
  underpowered, leaning underpowered. The T8' template is the right
  axis (monotone-flop-checked-through-multiway-semi-bluff). 12-15 hands
  is small relative to the corpus's 295 CHECK-class examples that
  dominate the model's "4-way checked through -> CHECK" generalization
  prior. With the existing class imbalance (CHECK 295, BET 137) and
  the strong "checked-through 4-way -> CHECK is correct" pattern in
  cohort 1 (per ml-architect 12.5D' Q4: 136 CHECK + 54 BET in cohort 1
  225-row), the booster's path of least resistance is still CHECK on
  any 4-way-checked-through situation. 12 BET counter-examples can't
  outweigh 100+ CHECK precedents. **Verdict: (c) underpowered; need
  ~30-40 hands of T8' to shift the booster's prior, or a partial
  feature signal (e.g., a "checked_through_count" feature) to encode
  the discriminator.**

**MW-40 (T9' PFR-checks-back-Ax: 12-15 hands; expert BET, model still
CHECK)**
- Same structural pattern as MW-25 but on a rainbow board. The
  populous corpus pattern is "BB defends, flop checks through, CHECK
  is correct"; T9' is the rare "PFR-checked-back-Ax-multiway-IP TPWK
  thin-value-bet" sub-pattern. 12 hands per template against 100+
  populous-pattern hands is again underpowered. **Verdict: (c)
  underpowered, with a hint of (b): the T9' implementation may not
  capture the "PFR-checked-back" action-sequence narrowing; the
  booster sees feature similarity to checked-through-multiway and
  generalizes from the populous pattern.**

**MW-45 (T10' slowplay-set-turn-lead: 8-10 hands; expert RAISE, model
still CALL)**
- This is the most likely **(b) wrong-implementation OR (c) underpowered
  + (b) compound**. Slowplay-set-into-turn-lead-into-raise is a 3-action
  multi-street pattern. T10' templates are isomorphic to MW-45 only if
  they capture the slowplay-on-flop -> face-turn-lead -> raise sequence
  AND the corresponding feature-vector signature (worse_hand_pct ~0.91,
  category=set, action_history showing flop-CHECK + turn-face-bet). If
  T10' templates have set-on-turn but the action-history feature
  doesn't encode the slowplay sequence the same way, the booster
  generalizes from "set + face-bet -> CALL" (the more common
  set-played-fast-then-face-bet pattern). Without seeing the actual T10'
  feature vectors, I lean (b) primary + (c) secondary. **Verdict:
  likely (b) wrong-implementation primary; T10' may not isomorph-match
  MW-45's action-sequence signature.**

**MW-17 (T7-ext path-c SUITED: 12 hands; expert CALL, model still FOLD)**
- This is the cleanest **(a) wrong-diagnosis** signal. gto-expert
  diagnosed MW-17 as E-FEATURE primary in 12.5D'; the discriminating
  signal is implied-odds + 3-way reasoning that the 59-feature surface
  doesn't encode. T7-ext SUITED added 12 hands with `nut_flush_block=1`
  and CALL labels — a partial corpus-side intervention against an
  E-FEATURE-primary problem. Per Q-eval-1, the booster did learn to
  attend to `nut_flush_block` (0.0496 importance), but learned to
  associate it with RAISE-class profiles (T5 SB-OOP, T-RAISE-stabilize)
  more than CALL-class profiles. The 12 CALL exemplars couldn't move
  the booster off the dominant `raw_equity 0.251 < pot_odds 0.268 ->
  FOLD` discriminator, because the feature-vector signal that DID flip
  in the corpus (nut_flush_block) was outweighed by the existing
  raw_equity-vs-pot_odds split. **Verdict: (a) wrong-diagnosis primary;
  E-FEATURE residual cannot be closed by 12 corpus hands when no
  feature encodes implied-odds magnitude or 3-way bet-defense reasoning.**

**MW-47 (T-RAISE-stabilize NFD bet+call multiway: 12 hands; expert
RAISE corrected, model still CALL)**
- This was the OPPOSITE-direction prediction from Opus 12.5E-F: I said
  cap=4.0 + closer corpus exemplars had ~50% chance of flipping MW-47.
  Actual: didn't flip even with 12 added hands at cap=3.0 + H-FEAT
  active. Two candidate explanations:
  (1) Cap=3.0 vs cap=4.0 difference: the T-RAISE-stabilize exemplars
      may need a cap-up to push their RAISE-class weight high enough
      to flip the boundary. The 12.5H run was held at cap=3.0; the
      cap dimension wasn't tested.
  (2) The T-RAISE-stabilize exemplars may have positional/action
      profiles slightly different from MW-47's specific 4-way-bet+call
      OOP profile (e.g., if 3-way exemplars dominate). 12 hands is too
      thin to populate the configuration space densely.
  **Verdict: ambiguous between (b) wrong-implementation (template not
  isomorph-matching) and (c) underpowered (12 hands insufficient given
  tight cap=3.0). Cap=4.0 sweep would disambiguate.**

### Aggregate

- **(a) wrong-diagnosis primary**: MW-17 (1 hand). Corpus alone cannot
  close E-FEATURE primary residuals.
- **(b) wrong-implementation primary**: MW-45 (1 hand, likely; would
  need corpus inspection to confirm).
- **(c) underpowered primary**: MW-25, MW-40 (2 hands). Need 30-40
  hands per template instead of 12-15.
- **Mixed (b)+(c)**: MW-47 (1 hand). Cap dimension not yet tested with
  H-FEAT active.

The empirical failure of 12.5H-E is not "the data approach is wrong,"
it's "the data approach was the wrong axis for 60% of the residuals."
Owner WHAT decision sees this as a partial-success diagnostic: H-FEAT
mechanism vindicated; corpus-side intervention works on (c) cases with
proper sizing; corpus-side cannot close (a) cases regardless of size.

---

## Q-eval-3 — per-direction HOW

### A — PROMOTE 32/40

- **Probability of "right call": 5-10%.** Lower than 12.5E-F's 10-15%
  because two iterations of corpus work (12.5E-E + 12.5H-E) now empirically
  failed to move median; shipping the regression normalises a slippery
  slope after a documented "we tried more data, no movement" record.
- **HOW (if picked):** ship `gto_model_v9_student.json` (chosen seed 2)
  with model-card regression note. Document H-FEAT validation
  (cross-seed median 0.0496) as platform achievement. Pair with explicit
  forward path commitment to one of C/D/E. v9-3way-v2.2 retained as
  45-feat fallback; no production-router default change without
  conditional gating. Cost: 1 builder day + 1 reviewer day; no re-train.

---

### B — abandon migration

- **Probability of "right call": 15-25%.** Empirical case for abandonment
  strengthened by 12.5H-E (90 more hands, no movement) but weakened by
  H-FEAT continuing to strengthen (+85% cross-seed). Owner judgment
  call: is the platform-investment value enough to keep alive after two
  iterations didn't move the canonical gate?
- **HOW (if picked):** ml-architect Variant 3a from 12.5E-F. Add
  abandoned-banner to `train_model_v9_student.py` documenting:
  (a) hybrid weighting (12.5D'); (b) corpus expansion 110 + 90 = 200
  hands validated H-FEAT primary (cross-seed median 0.0000 -> 0.0496);
  (c) reference-set median 31 -> 32, gate not cleared. Stay-wrong
  MW-17/25/40/45/47 are E-FEATURE/E-DIST/compound residuals not
  addressable by hybrid weighting + 200-hand corpus expansion at
  templates attempted. Do not promote without corpus rebuild AND
  re-evaluation. Update `reference_corrections.md` + model card; v9-3way-
  v2.2 stays canonical. PR scope ~10 lines. Cost: 1 builder day + 1
  reviewer day; no re-train.

---

### C — feature engineering (Direction X retro)

- **Probability of closing gap >=33: 35-45%.** Lower than D's nominal
  rate because feature-engineering integration risk is high (per
  `feedback_attention_flags_when_features_change.md`: attention
  vocabulary + capture + trainer changes coordinated). But UNIQUELY
  addresses E-FEATURE primary residuals (MW-17) and E-FEATURE secondary
  contribution to MW-47/MW-42 that D structurally cannot.
- **HOW (if picked):**
  - **Phase 1 — feature design (1 week, gto-expert + ml-architect):**
    3 candidate features from 12.5D' per-hand diagnosis:
    (1) `implied_odds_proxy` — SPR + draw-outs + position; targets
    MW-17 directly. (2) `nut_blocker_call_signal` — 3-way variant of
    nut_flush_block firing when hero is defender against multi-bet
    on nut-blocker-relevant board; targets MW-17 + similar CALL spots.
    (3) `action_sequence_capped` — boolean for "villain's check-call
    line caps range"; targets MW-42 + capped-range thin-value bets.
  - **Phase 2 — integration (per attention-flags memory):** feature-
    extractor + feature-keys (V9 -> V10) + attention vocabulary (raw +
    parallel attention flags Exp 3) + capture pipeline + corpus
    backfill (694 rows) + trainer pre-pad (45 -> 59 -> 62 with metadata
    bump) + pilot inference helper + 17-test suite updates.
  - **Phase 3 — corpus backfill + re-train (1 week):** re-extract
    features for 694 corpus + 40 reference rows; re-train cap=3.0;
    5-seed protocol.
  - **Phase 4 — gate evaluation (1 day):** target median 33-35.
    Predicted: MW-17 flips high-confidence; MW-42 + MW-47 each ~50%
    via action_sequence_capped + nut_blocker_call_signal; MW-25/40/45
    unchanged (E-DIST residuals). Realistic: 1-2 flips; median 33-34.
  - **Cost:** 3 weeks elapsed; ~1.5 builder weeks + ~0.5 ml-architect
    + ~0.5 QC. No new labelling spend (existing situation descriptors).
    Spec/infrastructure code drift risk per
    `feedback_spec_vs_infrastructure_code_drift.md`.
  - **Risk:** features may not cleanly capture discriminator; sacred
    core integration extensive.

---

### D — corpus expansion to 200-300/template (12.5I)

- **Probability of closing gap >=33: 30-40%.** Down from 12.5E-F's
  50-60% direction-C prior. 12.5H-E delivered +0 at 12-15 hands per
  template. If Q-eval-2c (underpowered) right, 30-40 hands flips
  MW-25/40 -> median 34. If Q-eval-2b right for MW-45, even 200 hands
  won't flip. If Q-eval-2a right for MW-17, no corpus expansion alone
  closes. Realistic: 1-2 flips; median 33-34.
- **HOW (if picked):**
  - **Sizing:** scale 4 templates from 12-15 to 30-40 hands each.
    Net +110 hands; corpus 694 -> 804.
  - **Per-template priority:**
    1. **T8' (MW-25 monotone-FD-checked):** 12 -> 35. Highest priority
       (populous 4-way-checked-CHECK pattern needs most counter-examples).
    2. **T9' (MW-40 PFR-checks-back-Ax):** 12 -> 35. Same generalization-
       prior overhead as T8'.
    3. **T-RAISE-stabilize (MW-47):** 12 -> 30. Compound residual;
       cap=4.0 + denser exemplars likely needed.
    4. **T10' (MW-45 slowplay-set-turn-lead):** 8 -> 25. PREREQUISITE:
       audit existing 8 hands for action-sequence isomorphism with
       MW-45; expansion wasted if T10' doesn't isomorph-match.
    5. **T7-ext SUITED (MW-17):** SKIP — E-FEATURE primary;
       direction C is the right intervention.
  - **Labelling protocol:** 5 labellers, MEDIUM/HIGH/CERTAIN buckets
    per `feedback_bucket_first_labelling.md`; solver-verify per
    `feedback_solver_findings.md`; GTO Wizard solver bet sizes per
    `feedback_solver_aligned_sizing.md`.
  - **Re-train (12.5I):** same trainer, cap=3.0 baseline; optionally
    cap=4.0 sweep for MW-47/MW-45.
  - **Cost:** 2-3 weeks corpus + 1 builder day re-train. ~$150-200
    labelling spend.
  - **Risk:** if Q-eval-2 diagnosis wrong (MW-25/40 not underpowered
    but wrong-impl), expansion delivers same 0 movement as 12.5H-E.

---

### E — diagnostic investigation (12.5I-pre)

- **Probability of being right next step: 30-45%.** Highest-EV first
  move because A/B/C/D all depend on knowing WHICH of (a)/(b)/(c) per
  Q-eval-2 is dominant per stay-wrong hand. ~$5 cost; 2-4 days.
  Asymmetrically valuable: results confirm (c) -> commit D; results
  confirm (b) for MW-45 -> redesign T10' (cheaper than D blanket);
  results confirm (a) for MW-17 -> commit C.
- **HOW (if picked):**
  - **Inv 1 — feature-vector + SHAP attribution on 5 stay-wrong**
    (1 day, ml-architect): extract feature vectors via
    `reference_evaluator._evaluate_one_hand`; identify top-3 features
    driving each predicted action via SHAP / feature_importance ×
    split-count leaf attribution. Cross-reference vs expected
    discriminator (e.g., MW-17 driven by raw_equity vs pot_odds
    confirms (a) E-FEATURE primary).
  - **Inv 2 — template-isomorphism audit** (1 day, gto-expert):
    inspect T8'/T9'/T10'/T-RAISE-stabilize designs vs MW-25/40/45/47.
    For each template, sample 3 hands, compute feature-vector cosine
    similarity to reference hand. >0.85 rules out (b); <0.7 confirms
    (b) likely.
  - **Inv 3 — booster split-path trace** (1 day, ml-architect): for
    each stay-wrong hand, trace which splits were taken at each node;
    identify whether leaf reached via expected poker-theoretic
    discriminator or via populous-pattern generalization (e.g., MW-25
    reaching CHECK via "4-way + checked_through" vs proper monotone-
    FD-semibluff branch).
  - **Inv 4 — counterfactual mini-train** (1 day, ml-architect):
    single-seed v9-student on corpus_combined_694 with 5x artificial
    boost on T8'/T9'/T10' rows (vs global cap=3.0). MW-25/40/45 flip
    under boost -> confirms (c) underpowered (density-equivalent).
    Don't flip -> confirms (b) wrong-implementation.
  - **Inv 5 — synthesis** (0.5 day, orchestrator): per-hand verdict
    matrix MW-17/25/40/45/47 -> {(a)/(b)/(c)} with Inv 1-4 evidence.
  - **Cost:** 4-5 builder/expert days, ~$5 compute, $0 labelling, no
    source-surface edits.
  - **Decision criterion:** ≥3 of 5 hands are (c) -> commit D with
    confidence. ≥2 are (a) or (b) -> commit C or C+D compound. Mixed
    -> owner picks pragmatically.

---

## Brief — methodology assessment for owner

**Highest-EV gap-closer based on empirical evidence:** the slow-quality
sequence is **E (diagnostic) -> commit to either C or D based on
diagnostic results**, NOT either C or D blindly.

**Why E first:**
- 12.5E-E and 12.5H-E both delivered "median didn't move" at a cumulative
  ~$200-300 labelling + ~6 weeks elapsed cost. Spending another 2-3
  weeks on D or 3-4 weeks on C without first knowing whether the
  per-hand cause is (a)/(b)/(c) is repeating the 12.5H-E error pattern
  at larger scale.
- E costs 4-5 expert/builder days and ~$5; cheap relative to C or D.
- Per `feedback_orchestrator_decides_not_recommends.md`: this is
  methodology, not WHAT. Owner can pick D directly if cost preference
  outweighs diagnostic certainty.

**Honest update from prior predictions:**
- 12.5E-F predicted ~50-60% probability that direction C (corpus
  expansion) would close the gap. Empirical: 0%. Update: marginal yield
  per labelled hand at the 12-15-hands-per-template scale is
  approximately zero on the canonical reference set. Future corpus-
  expansion predictions must explicitly model per-template density
  thresholds (likely 30-40 hands per template minimum to overcome
  populous-pattern generalization).
- 12.5E-F predicted ~30% probability that B-then-C would clear MW-47.
  Empirical: didn't clear (B was not run; C was run via 12.5G/H; 0
  movement). Update: cap=4.0 was never empirically tested; the cap
  dimension remains a 1-day experiment that could disambiguate MW-47.
- The structural lesson re-confirmed across 3 iterations (12.5D/D'/E/H):
  **fixing the next layer in the chain does not guarantee terminal
  output movement when the residual is heterogeneous across hands.**
  Each iteration verified the next-layer mechanism (loss collapse fix,
  H-FEAT activation, corpus expansion to T-templates) without
  delivering predicted gate movement. The pattern holds: per-hand
  applicability forecasting at design time is necessary but absent.

**On owner decision:** A is structurally weak (-1 regression now
empirically confirmed across 200 corpus hands). B is structurally
weakened (90 more hands of corpus didn't move it; future iterations
may also not). C addresses the unique residual (E-FEATURE primary)
that D structurally cannot. D addresses (c) underpowered residuals
that C cannot. E disambiguates which is dominant before committing.

The slow-quality default (per `feedback_quality_default_no_ask.md` +
`feedback_no_deadlines.md`) is E-then-{C,D,or-compound}. If owner
prefers a faster commit, D alone has ~30-40% probability and ships
cheapest of the gap-closing directions; C alone has ~35-45% and
addresses more residual classes; D-then-C compound has ~50-60%
combined and ~5-7 weeks elapsed.

This is methodology only. Owner picks WHAT among A/B/C/D/E (or any
compound) for cost/timeline/strategic reasons. The HOW for each is
laid out above; orchestrator + owner own the WHAT decision.
