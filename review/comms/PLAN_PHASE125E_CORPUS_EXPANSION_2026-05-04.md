---
date: 2026-05-04
from: ML-ARCHITECT (Phase 12.5E corpus-expansion design)
to: Main terminal (orchestrator) · Owner · GTO-EXPERT (review) · LEAD-PROGRAMMER (build) · QC stream
re: Phase 12.5E corpus expansion — design comm authoring the data-side fix selected at the 12.5D' synthesis owner gate
status: DESIGN — corpus-side workstream blueprint; HOW-only per `feedback_orchestrator_decides_not_recommends.md`
---

# Phase 12.5E corpus expansion — design comm

## §1 Scope and authority

**Scope.** 12.5E is a corpus-side workstream that addresses the
H-FEAT/H-DIST root cause empirically refuting the migration's "Direction X"
(model-side hybrid weighting at cap=3.0 closes the reference-set gap).
12.5D' refuted that link at the empirical level: median 31/40 unchanged,
1/7 shared-cause failures flipped, blocker importance still 0.0000. The
data-side fix expands the training corpus with reference-set-style
situations so the discriminative axes (blockers + multi-street action
narrowing + thin-value-river-bet patterns + slowplay-then-raise patterns)
become both populated AND load-bearing, and re-trains using the 12.5C
trainer module already on master.

**Authority chain.**
- ml-architect 12.5D' findings: `/tmp/ml_architect_125d_prime_findings.md`
  (Q4 H-FEAT primary + H-DIST secondary verdict; Q6 Direction-4 HOW spec)
- gto-expert 12.5D' findings: `/tmp/gto_expert_125d_prime_findings.md`
  (per-hand E-DIST/E-FEATURE classification for MW-17/25/40/42/45/47;
  Direction-D 50-70% gap-close prior)
- 12.5D' synthesis owner gate: owner picked Direction D (data-side fix)
- Standing instructions: `feedback_quality_default_no_ask.md`,
  `feedback_no_deadlines.md`, `feedback_solver_vs_expert_labels.md`,
  `feedback_bucket_first_labelling.md`

**Authority limits.** This is HOW-only. The WHAT decision (Direction D)
is owned by the orchestrator + owner. Sequencing within 12.5E is
owned by the orchestrator. Quality decisions inside the design (sample
size, expert count, QC gate thresholds) are made here per
`feedback_quality_default_no_ask.md` — not surfaced as open questions.

## §2 Diagnosis of the gap (recap)

12.5D' empirical evidence localised the failure mode to the corpus:

**H-FEAT primary (~70% weight).** The 4 P1 blocker features
(`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`,
`nut_made_block_pct`) carry no usable signal for the reference-set
failure spots on the current 494-hand corpus. `nut_flush_block`
importance is 0.0000 in BOTH 12.5D (pure confidence weighting) and
12.5D' (cap=3.0 hybrid weighting) — the booster never splits on it
under any tested loss surface, because the corpus contains no
situations where the feature co-varies with the label. Hybrid
weighting changed gradient mass on existing examples; it did not
change which features are available to discriminate on.

**H-DIST secondary (~30% weight).** The corpus's 29 RAISE rows
concentrate in `monster_*` (10/10 RAISE) and `nfd_*` (16/48 RAISE);
remaining RAISE supply: `magg_*` 1, `facing_*` 1, `donk_*`/d-prefix 1
(empirically verified at /home/rupertbeytell/river-rats-v2/data/corpus_revision_500_hand_2026-04-27.jsonl
via `pilot_hand_id` join, 494/494 cardinality). Cohort 1 d-prefix rows
contribute 1 RAISE across 225 hands — virtually no RAISE signal in the
larger cohort. The model learns "RAISE means monster-pattern OR
canonical nfd-pattern." MW-45 (BB slowplay-set into turn lead 4-way)
and MW-47 (SB nut-FD+gutshot semi-bluff RAISE OOP into bet+call 4-way)
are not monster-pattern and not canonical nfd-pattern; the learned
RAISE pattern doesn't fire. Exactly MW-24 flipped (the one hand whose
features matched the corpus's BET pattern under hybrid weighting).

**H-TREE rejected.** xgboost trees with `max_depth=5`,
`n_estimators=800`, 287-663 actual rounds at hyperparameter settings
that already passed Gate 2.3 overfit/underfit checks have ample
capacity. Importance 0.0000 on `nut_flush_block` is "the gradient at
every node found a stronger split elsewhere" — not "the tree wanted to
split there but couldn't."

**Failure-mode taxonomy from gto-expert per-hand analysis.** Of the 6
stay-wrong hands at 12.5D':

| Hand | gto-expert verdict | composition triple | board / street family |
|---|---|---|---|
| MW-17 | E-FEATURE primary (implied odds + nut-FD-blocker against CO range) | NFD + 2 overcards | Jd8d4c flop, facing CO 3-way bet |
| MW-25 | E-DIST primary (FD + overcard, monotone-flop checked-through 4-way) | 2nd-nut FD + overcard | As9s5d flop, IP after PFR check |
| MW-40 | E-DIST primary (TP-T-kicker IP 4-way after PFR check) | TP+ medium kicker | AJ5r flop, IP 4-way after PFR check |
| MW-42 | E-FEATURE primary (action-sequence narrowing CO check-call-check turn) | TPTK river | AK752 river, after multi-street narrowing |
| MW-45 | E-DIST primary (slowplayed set facing turn lead 4-way) | set | AKx-Q turn lead 4-way |
| MW-47 | E-DIST + E-FEATURE compound (NFD+gutshot semi-bluff RAISE OOP) | NFD + gutshot | KsJd5s flop, OOP facing bet+call 4-way |

12.5E targets the E-DIST root cause directly by adding situations to
the corpus. The 2 E-FEATURE-primary hands (MW-17, MW-42) are partly
addressable through DIST coverage (more analogues = more training
signal even without a new feature) but escape the 12.5E reach if the
discriminative reasoning genuinely requires a feature outside the
59-column surface. §9 prediction calls this out explicitly.

## §3 Target situations to add (the failure templates)

Eight failure-template families. Each entry specifies: composition
triple (TP+ / draws / air), board texture family, hand count to add,
sourcing strategy, and labelling-rule anchor. Counts chosen for
statistical learnability per pattern (per-template ≥10 hands so the
booster can find a stable split on the discriminative axis); densities
within a pattern vary slightly to reflect the corpus's existing
balance.

### Template T1 — BET-stays-wrong: monotone-flop FD-with-overcard checked-through 4-way (MW-25 family)

- **Composition triple:** drawing (FD + 1-2 overcards) / IP / multiway checked-through
- **Board family:** monotone flop (any single suit), high card 8-A, no pair
- **Action family:** PFR opens, callers, hero IP, all check to hero on flop
- **Hands to add:** 12 (varying suit / board high card 8-A / hero suit dominance)
- **Source:** situation factory with parametric monotone-flop generator; hero hand structured to give 1-2 overcards + same-suit FD; board roll generator iterates flop high-card 8-A
- **Labelling rule (bucket-first):** bucket = drawing (FD-with-overcard); reasoning anchor = "checked-through-4-way condenses villain ranges; semi-bluff for fold equity + equity denial + protection at low cost when villains all signal weakness; classic Position Amplification axis"
- **Discriminative axis the model must learn:** `is_monotone=1` AND `villain_aggression_count` low AND `num_opponents>=3` AND `has_flush_draw=1` AND `is_paired=0` ⇒ BET-friendly bucket; the existing 59-feature surface CAN encode this — it just doesn't have enough analogues to learn it on the current 494 corpus

### Template T2 — BET-stays-wrong: TP-medium-kicker IP 4-way after PFR check (MW-40 family)

- **Composition triple:** TP+ (top pair, 9-T-J kicker) / IP / multiway after PFR check-back
- **Board family:** rainbow A-high or K-high flop, no draws on board, no pair
- **Action family:** PFR (HJ/CO) opens, callers including hero IP, hero NOT preflop aggressor; flop checks through PFR to hero
- **Hands to add:** 10 (board high card A or K; hero kicker T or J or Q; sometimes light overpair-flavoured spot folded into next template)
- **Source:** situation factory with rainbow-A-high or rainbow-K-high generator; hero hand parametrically structured TP+ medium kicker; PFR-checks-back signal injected via `villain_aggression_count=1` + `villain_checked_back=1`
- **Labelling rule:** bucket = strong_made (TP medium kicker); reasoning anchor = "PFR check-back on Ax/Kx in 4-way condenses field's range to weak Jx, broadways without ace, air; thin value + protection + equity denial"
- **Discriminative axis:** `is_strong_made=1` AND `is_rainbow=1` AND `villain_checked_back=1` AND `num_opponents>=2` ⇒ BET-friendly; encodable in the 59-feature surface, dist-limited on current corpus

### Template T3 — BET-stays-wrong: river thin-value TPTK after multi-street action (MW-42 family)

- **Composition triple:** TPTK / IP / heads-up-by-river after villain check-call-check pattern
- **Board family:** rainbow A-high or K-high run-out where hero TPTK survives (no obvious draw completion)
- **Action family:** flop bet→hero call→other folds; turn check→hero bet→villain call; river blank→villain check
- **Hands to add:** 10 (board run-out variations; villain position varied across CO/HJ/BTN)
- **Source:** situation factory with multi-street trace builder; CRUCIAL — this template has E-FEATURE risk per gto-expert (action-sequence narrowing across 3 streets is the discriminative axis). To make it 59-feature-encodable, the factory MUST populate `villain_aggression_count`, `villain_call_count`, `villain_checked_back`, and `street=river` such that the joint distribution distinguishes "villain check-called turn → check-call river bottom of value" from "villain check-called turn with strength → check-raise river"
- **Labelling rule:** bucket = strong_made (TPTK); reasoning anchor = "villain's check-call turn caps range to one-pair bluff-catchers + missed draws; thin value vs missed draws calling river; better hands check-raise rare; classic Range Narrowing axis"
- **Discriminative axis caveat:** if the 59-feature surface can't distinguish T3 from "TPTK river vs villain who check-called turn AND just check-raised river" (MW-46 territory), the gain on T3 will be limited. Predicted partial gain — 5-7 of 10 T3 family hands flip in held-out, MW-42 has ~50% probability of flipping at the reference-set gate. Documented as known E-FEATURE residual

### Template T4 — RAISE-stays-wrong: slowplayed set into turn lead 4-way (MW-45 family)

- **Composition triple:** set / OOP / 4-way after slowplayed flop (all-check on flop)
- **Board family:** rainbow flop containing hero's pair, turn brings broadway connectivity but NO flush
- **Action family:** PFR opens, multiple callers including hero in BB; flop all-check; turn villain leads
- **Hands to add:** 12 (set rank varied 22-99; flop board varied; turn lead size varied 50-75% pot)
- **Source:** situation factory with slowplay-then-turn-lead builder; hero pocket pair flops set; flop checked through; turn villain leads — must populate `street=turn`, `villain_aggression_count` showing villain just bet, `is_set` (encoded via `hand_category`), `num_opponents>=3`
- **Labelling rule:** bucket = monster (flopped set); reasoning anchor = "CO leading 75 into 120 4-way represents two-pair (AK, AQ, KQ) + AK-strong + occasional bluffs/draws; raise for value vs AK/two-pair + protection vs gutshots/runner-runner FDs; range Narrowing axis"
- **Discriminative axis:** `hand_category=set` AND `villain_aggression_count` showing villain JUST became aggressor (turn) AND `num_opponents>=2` ⇒ RAISE-friendly; the corpus currently has the inverse pattern ("set bets/raises immediately") and 0 of these slowplay-then-raise turn patterns. Adding 12 makes it learnable

### Template T5 — RAISE-stays-wrong: NFD+gutshot semi-bluff RAISE OOP into bet+call multiway (MW-47 family)

- **Composition triple:** NFD + gutshot (combo draw, 9+4 outs) / OOP / multiway facing bet+call
- **Board family:** two-tone flop with broadway top card containing hero's nut-FD suit; second card connects for gutshot-broadway
- **Action family:** PFR opens, callers including hero in SB/BB, BB checks (or hero IS BB), CO bets, BTN calls, hero faces bet+call OOP
- **Hands to add:** 12 (NFD suit varied across 4 suits; flop top card K/Q/J; gutshot turn card T/A varied)
- **Source:** situation factory with two-tone-flop bet+call OOP combo-draw generator; hero hand parametrically structured AsQs / AsTs / AsKs across hero-suit dominance; CRITICAL — `nut_flush_block` MUST be set to 1 in the feature dict (hero IS the nut-FD), and the factory must verify this. If the existing factory does not populate this feature consistently, that's a finding for 12.5E-B
- **Labelling rule:** bucket = drawing (combo-draw with nut blocker); reasoning anchor = "OOP raise semi-bluff against bet+call 4-way folds out CO's medium-pair barrels and BTN's float range; sets up clean 9 nut-flush outs with fold equity; denies BB's overcard realisation; combined Axes 3+4+5"
- **Discriminative axis:** `nut_flush_block=1` AND `has_flush_draw=1` AND `draw_outs>=9` AND `villain_aggression_count` showing recent bet AND `num_callers_to_bet>=1` AND `is_ip=0` ⇒ RAISE-friendly. THIS IS THE PRIMARY TEST OF H-FEAT — if 12 of these hands plus 0-12 from T4 don't move `nut_flush_block` importance from 0.0000 to ≥0.02-0.05, the H-FEAT diagnosis is wrong (escalation per §9)

### Template T6 — RAISE-stays-wrong: monster-on-rainbow facing turn check-raise (MW-33-adjacent reinforcement)

- **Composition triple:** set / facing immediate aggression / 3-way to multiway
- **Board family:** rainbow paired-low or low-connector flop that gave hero set; turn unrelated
- **Action family:** PFR opens, hero in BB calls preflop, flop bet+call, hero raises or faces a raise
- **Hands to add:** 8 (existing 10 monster_* RAISE rows are all immediate-bet patterns; this family adds delayed-aggression monster patterns to break the corpus's "monster ⇒ RAISE iff first to act" learned simplification)
- **Source:** situation factory; reuses the 10-row monster_* generator with a delayed-aggression branch; this is a control template to prevent corpus-coverage-fix from over-narrowing the model's monster-RAISE pattern
- **Labelling rule:** bucket = monster; reasoning anchor varies per spot
- **Discriminative axis:** prevents the model from learning "monster-pattern ⇒ RAISE only when first to act"; reinforces the bucket independence from action-order

### Template T7 — CALL-stays-wrong: NFD+overcards under direct pot odds with implied/blocker reasoning (MW-17 family)

- **Composition triple:** NFD + 1-2 overcards / OOP / facing single bet 3-way
- **Board family:** two-tone flop with broadway top card containing hero's nut-FD suit; pot odds threshold 24-30%
- **Action family:** PFR opens, callers, hero in BB facing CO single bet 3-way (no callers behind)
- **Hands to add:** 10 (raw_equity range 0.22-0.28 to bracket the pot-odds line; nut-FD suit varied; overcard count 1-2)
- **Source:** situation factory; hero hand parametrically structured AhKx / AhQx / AhJx / KhQh with hero suit on board's two-tone suit
- **Labelling rule (BUCKET-FIRST, NOT THRESHOLD):** bucket = drawing (NFD + overcards); reasoning anchor = "raw_equity below pot odds direct, but implied odds + nut-FD blocker against CO's range + 6 likely-clean overcard outs make CALL profitable; absent fold-equity for semi-bluff (not multiway-deep enough), CALL realises equity cheaply"
- **CRITICAL — labeller prompt MUST NOT contain a pot-odds threshold rule.** Per `feedback_bucket_first_labelling.md`, the bucket triggers reasoning, not the equity number. The reasoning must reach CALL via composition (NFD + overcards + nut-FD-blocker against narrow CO range), not via a numeric threshold lookup
- **Discriminative axis:** `has_flush_draw=1` AND `nut_flush_block=1` AND `overcard_outs>=4` AND `is_ip=0` AND `num_opponents=2` (single-bet 3-way) ⇒ CALL-friendly even when raw_equity slightly under pot odds; encodable in the 59-feature surface

### Template T8 — Control hands (preserve corpus class distribution + detect labeller drift)

- **Composition triple:** mixed across all 5 buckets (monster / strong_made / medium_made / drawing / air)
- **Board family:** mixed (rainbow + paired + two-tone + monotone, low-card + middle + high)
- **Action family:** mixed across street + facing-bet + facing-check states
- **Hands to add:** 36 sampled to balance the new corpus's class distribution within ±15% of the existing 494-hand mix per class (see §4 sizing math). Specifically: 12 CHECK, 8 BET, 8 FOLD, 6 CALL, 2 RAISE controls. **Post-dispatch compression note (added at 12.5E-E cleanup per dispatch §"Step 4" NIT-1; extended at 12.5H-E ride-along clarification):** Phase 12.5E dispatch (PR #133) and 12.5E-B amendment (Path B / PR #137) compressed T8 to 22 hands (8 CHECK + 5 BET + 4 FOLD + 3 CALL + 2 RAISE = 22 parametric) so the combined parametric file totals 96 (12+10+10+12+12+8+10+22) and the 14 manual canonicals (2 per T1-T7) bring overall 12.5E-B output to 110. The original §3.T8 design-intent of 36 hands was the pre-compression target; effective T8 in the merged 604-hand corpus is 22 parametric per the dispatch-compression decision (= 22+14 manuals after the per-template manual canonicals are counted). At 12.5H this corpus-design pattern continues: 12.5H-B replaces T8 controls with the structurally similar T-CONTROL family (20 parametric, all carrying explicit `design_action` per TC-X T8 schema gap fix) and adds 5 new template classes T8'/T9'/T10'/T7-ext/T-RAISE-stabilize totaling 64 additional parametric + 6 manual canonicals = 90 hands; the merged 12.5H-E corpus is 694 hands (604 + 90). See `review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md` §3 for 12.5H template specification.
- **Source:** situation factory + targeted manual sampling from the existing source-pool (`training-data/3way_situations_10k.jsonl` 962-hand pool) for any control patterns the factory can't reach cleanly
- **Labelling rule:** bucket-first per memory; same rules as the 494-hand round
- **Discriminative axis:** detects drift in the new labelling round vs the old round (if T8 controls produce labels at 70%+ agreement with the corresponding 494-hand-round labels, the new round is consistent; if <70%, the new round drifted and is rejected)

### Coverage summary

| Template | Family | Hands |
|---|---|---|
| T1 | Monotone-flop FD checked-through 4-way (MW-25) | 12 BET |
| T2 | TP-T-kicker 4-way after PFR check (MW-40) | 10 BET |
| T3 | River thin-value TPTK after multi-street narrowing (MW-42) | 10 BET |
| T4 | Slowplayed set into turn lead 4-way (MW-45) | 12 RAISE |
| T5 | NFD+gutshot semi-bluff RAISE OOP into bet+call multiway (MW-47) | 12 RAISE |
| T6 | Monster delayed-aggression patterns (MW-33-adjacent) | 8 RAISE |
| T7 | NFD+overcards CALL under pot odds (MW-17) | 10 CALL |
| T8 | Control hands (mixed class) | 36 mixed |
| **Total** | | **110** |

## §4 Quantity and class distribution

### Total: 110 new hands (post-quality default; not 100)

ml-architect 12.5D' Q6 estimated ~70 target + ~30 control = ~100. Per
`feedback_quality_default_no_ask.md`, 110 is the chosen count: the
extra 10 hands distribute across T1-T7 templates (3 in T5 NFD+gutshot
which is the H-FEAT primary test, 2 in T4 slowplay-set which is the
second-most-critical, and 1-2 across T1/T2/T3/T6/T7) to add headroom
for any template where 5+ near-identical situations are needed to
establish a stable booster split (per ml-architect 12.5D' Q6 risk note).

### Why 110 and not 150 or 200

The H-FEAT diagnosis predicts the booster needs ~10 same-pattern
examples per discriminative axis to surface a stable split. With 12
NFD-RAISE-OOP-into-bet+call hands (T5) + 12 slowplay-set-turn-lead
(T4) + 12 monotone-FD-checked-through (T1), each axis has
`booster_min_split_size = min_child_weight = 5` headroom by 2x. Going
to 150 doesn't strengthen the per-template signal more than going to
110 does — the marginal hands beyond ~12 per template start sampling
similar patterns and the booster's gain from the extra rows
diminishes per the `min_child_weight=5` floor. **150 or 200 would help
if the diagnosis is "10 per template is too few"** — that's an
escalation point covered in §9, not a default.

The opposite risk — under-sizing — is mitigated by the +10 buffer
relative to the ml-architect Q6 estimate. If 12.5E re-train shows that
the 12-per-template T5 still doesn't surface `nut_flush_block`
importance, escalation to 150 (adding 12 more T5 hands + 12 more T4
hands) becomes Phase 12.5F.

### Class distribution after merge

Post-12.5E corpus = 494 + 110 = 604 hands.

| Class | 12.5D corpus | +12.5E adds | Post-12.5E | Pre/post % |
|---|---|---|---|---|
| FOLD | 72 | 8 | 80 | 14.6% → 13.2% |
| CHECK | 245 | 12 | 257 | 49.6% → 42.5% |
| CALL | 62 | 16 (10 T7 + 6 T8) | 78 | 12.6% → 12.9% |
| BET | 86 | 32 (12 T1 + 10 T2 + 10 T3) | 118 | 17.4% → 19.5% |
| RAISE | 29 | 32 (12 T4 + 12 T5 + 8 T6) | 61 | 5.9% → 10.1% |
| **Total** | **494** | **110** | **604** | |

RAISE class doubles from 5.9% to 10.1% — the single most important
distributional shift, addressing H-DIST. CHECK class drops from 49.6%
to 42.5% — still the dominant class but no longer crushing every
gradient-mass calculation. BET class shifts up from 17.4% to 19.5% —
modest, addressing the 4 BET-stays-wrong reference-set hands. CALL
class shifts negligibly (12.6 → 12.9%) — addressing MW-17 specifically
without introducing CALL-class drift.

## §5 Sourcing strategy

### 5.1 Two-track sourcing

**Track A — situation factory (deterministic, parametric).**
Templates T1, T2, T3, T4, T5, T6, T7 are parametric in board, hero
hand, position, and action family. The existing corpus-generation
pipeline (`scripts/build_corpus_revision_500_hand.py` per
`BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md`) can be
extended with new module branches per template. Each module emits
deterministic hands keyed by template + parameter values. T6 and T8
mixed-control may reuse existing modules (`monster_*`, `nfd_*` etc)
with new parameter sweeps.

**Track B — manual canonical authoring.** A subset of T1-T7 hands
(roughly 2 per template, 14 hands total) are authored manually as
canonical reference-set-style spots. These mirror the BATCH2 reference
set's quality bar (precise board, precise hero hand, precise action
sequence, no ambiguity in opponent count or position). The factory
output covers parametric breadth; the manual hands ensure depth at
the discriminative axis. Gto-expert reviews the 14 manual hands
before they enter the labelling pipeline.

### 5.2 Solver usage policy (per `feedback_solver_vs_expert_labels.md`)

- **Solver MUST NOT generate the labels.** Per memory: solver
  outputs are for verification and research only.
- **Solver MAY be used in two narrow modes:**
  1. *Verify-after.* After the multi-expert labelling round produces
     consensus labels, run the resulting (situation, label) pairs
     through GTO Wizard / PioSolver to flag situations where the
     consensus expert label disagrees with solver. Flagged
     situations are reviewed: if expert reasoning is sound but uses
     features not in the surface (i.e. solver-reasoning that the
     model can't replicate), the EXPERT label stands. If expert
     reasoning is empirically flawed (e.g. a misread of villain
     range that contradicts solver-confirmed common sense), the
     situation is sent back for re-labelling — but the solver does
     NOT supply the new label.
  2. *Research preflight.* Before the labelling round, gto-expert
     can use solver to research whether T5/T4 spots have a single
     canonical GTO answer (e.g. "is RAISE 100% correct on MW-47, or
     is it a mixed-strategy with 60% RAISE / 30% CALL / 10% FOLD").
     If mixed, the labelling round documents the mix and labellers
     vote on the dominant action — they don't try to encode a mix.
- **Boundary check.** Solver may NOT be cited inside the labeller
  prompt as a rule. Solver may NOT influence the bucket definitions
  (these are poker-reasoning anchors per `feedback_bucket_first_labelling.md`).
  Solver may NOT post-process expert labels into majority-vote
  overrides. Solver-corrections to the reference set
  (`reference_corrections.md`) are evaluation-overlay only and apply
  ONLY at the gate stage (§8 phase F), never on the training labels.

### 5.3 Expansion to existing pipeline

The 12.5E builder (LEAD-PROGRAMMER in 12.5E-B) extends
`scripts/build_corpus_revision_500_hand.py` with new module branches
for T1-T8 templates. Output file:
`data/corpus_revision_604_hand_2026-05-XX.jsonl`. The 494-hand corpus
is preserved unchanged; the new file appends the 110 new rows after a
deterministic re-emission of all 494 existing rows (so the new file
is self-contained). Builder verifies file diffs vs 494-hand file are
exactly +110 rows, no row mutations.

## §6 Labeller pipeline reuse

The 110-hand round reuses the existing labeller pipeline with one
amendment.

### 6.1 Reuse (no changes)

- `scripts/dispatch_mass_labelling.py` (existing on master per
  `MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md`)
- `scripts/collect_mass_labels.py` (existing on master)
- v3.2 protocol prompt at `prompts/gto_labeller_v3.2.md`
- Per-labeller JSON output schema (Phase B Protocol A)
- Plurality-consensus aggregation (consensus action = mode of valid
  votes; consensus confidence = count_max / vote_count)

### 6.2 Quality default — 5 expert labellers per hand (NOT 3)

Per `feedback_quality_default_no_ask.md`. The 494-hand round used 5
sonnet labellers per hand and produced acceptable confidence
(consensus_confidence median 0.8 across the 494 rows per spot-check).
12.5E uses the same: 5 sonnet labellers × 110 hands = 550 labels.
Cost estimate: ~$50-80 (5 dispatches × ~$10-16 each). Hard cap: $120.

### 6.3 Ref-id schema decision: pilot_hand_id from the start

12.5D' empirically refuted the `corpus.source_situation_id ==
labels.ref_id` join-key claim (cohort 2 has `situation_id`, labels
have heterogeneous `ref_id` mixing `d####_POS_street` + `PILOT_###`).
The universally-populated key is `pilot_hand_id` (494/494 in both
files at the 494-hand corpus, empirically verified at design time).

For 12.5E:
- Each new corpus row gets a new `pilot_hand_id` continuing the
  sequence (PILOT_495 through PILOT_604)
- The labeller dispatch's `compute_ref_id` function in
  `scripts/dispatch_mass_labelling.py` is amended to emit BOTH
  `ref_id` (legacy, computed as before) AND `pilot_hand_id` per row
  — this is the join-key amendment
- Collect-time aggregation in `scripts/collect_mass_labels.py` is
  amended to write `pilot_hand_id` as the canonical join field on the
  output JSONL (alongside `ref_id` for backward-compat with the
  existing 494-hand labels file)
- The trainer module already joins on `pilot_hand_id` per 12.5D'
  Section A schema discoveries (master HEAD `1b95648`)

### 6.4 Pre-flight join-cardinality gate (per 12.5D' dispatch protocol amendment)

Builder in 12.5E-B runs a pre-flight on ≥5 sample rows, then on the
full 110:

```
Pre-flight 1 (sample): on 5 sample rows from the new factory output,
verify pilot_hand_id present + unique + non-null in BOTH corpus_*.jsonl
and labels_*.jsonl. STOP if cardinality < 1.0 on the 5-sample.

Pre-flight 2 (empirical): on the full 110 new rows + 494 existing,
verify joined cardinality = 604/604 = 1.0. STOP if < 0.99.

Pre-flight 3 (no duplicate detection): assert that pilot_hand_id values
in the new 110 rows do NOT collide with any of PILOT_001..PILOT_494.
STOP if collision detected.
```

The `<0.99 = STOP` threshold is intentionally tight for milestone
data PRs; routine PRs use `<1.0 = STOP` per the dispatch amendment.
Both gates are tighter than the 12.5D round's join-key discovery
(which surfaced AFTER the join failed in the trainer).

### 6.5 Bucket-first protocol unchanged

Per `feedback_bucket_first_labelling.md`, the labeller prompt
describes buckets qualitatively. No equity thresholds in the prompt.
Reasoning anchors per template (§3) inform what kind of poker
reasoning each template requires but DO NOT enter the prompt as
template-specific rules — the prompt remains template-agnostic. The
labellers see hands one at a time and reason from features +
composition + board + action history. Template-anchored reasoning
emerges naturally from the bucket+context, not from prompt
engineering.

## §7 QC gates (pre-merge for the data PR)

Four pre-merge gates. Each must pass before the labels PR is
mergeable.

### G1 — Join-cardinality check (paired with 12.5E-B builder)

Per §6.4 pre-flight. QC verifies builder ran the pre-flight, that
the report includes the 3 pre-flight outputs, and that the merged
corpus joins 604/604.

### G2 — Label distribution sanity

Empirical distribution of the new 110 labels MUST satisfy:

- No class < 5% of the new 110 (i.e., no class has < 6 labels). The
  threshold is 5% because RAISE class targets ~29% of the new 110
  (32/110), much above 5%, so the gate catches a labelling
  failure where a class is suppressed below natural floor.
- Class distribution within ±20% of the §4 target per class
  (e.g. 32 RAISE target → 26-38 RAISE acceptable; 16 CALL target →
  13-19 CALL acceptable). Tighter than ±50% to catch labellers
  systematically refusing the harder templates.
- Median consensus_confidence ≥ 0.6 across the 110 hands. (494-hand
  round was 0.8; 0.6 is a deliberately permissive floor accepting
  that reference-set-style spots are harder to reach 5/5 consensus
  on.)

### G3 — Duplicate detection vs existing 494 rows

QC computes the (board, hero_cards, hero_position, prior_actions)
tuple for each of the 110 new rows and asserts NO tuple matches any
of the 494 existing rows. (This catches a builder bug where the
factory accidentally re-emits an existing situation under a new
pilot_hand_id.) STOP on any match.

### G4 — Labeller-drift detection (compare new round vs old round on T8 controls)

The 36 T8 control hands must be sampled such that ~half of them
(≥18) have a near-equivalent situation in the 494-hand corpus
(matched on bucket + board family + facing-bet status). For each
matched pair, QC computes the consensus action + consensus confidence
of both the 12.5E label and the corresponding 494-hand label and
reports:

- Same-action rate (target ≥ 70%; <70% = drift, BLOCKER)
- Mean confidence-Δ (|new - old|; target < 0.15; ≥0.15 = drift)

This gate catches systematic labeller-protocol drift between the
494-hand round and the 12.5E round (e.g. one labeller subagent ran a
different model version, or the v3.2 protocol prompt was edited
without bumping version). If drift detected, the round is REJECTED
and a re-run is dispatched (cost: re-run; not patched in place).

## §8 12.5E workstream phases

Six phases. Each phase has an entry condition and a blocking exit
gate. Orchestrator owns phase sequencing; this design owns each
phase's HOW.

### 12.5E-A — Design comm (THIS DOC)

- Entry: Direction D selected at 12.5D' synthesis owner gate
- Owner: ML-ARCHITECT
- Output: `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-XX.md`
  (this doc; merge after orchestrator owner gate)
- Exit gate: orchestrator + owner approve design (single owner gate;
  no re-cycling on design once approved unless owner-redirect)

### 12.5E-B — Situation generation

- Entry: 12.5E-A approved
- Owner: LEAD-PROGRAMMER
- Output: `data/corpus_revision_604_hand_2026-05-XX.jsonl` (494 + 110
  new) + extension of `scripts/build_corpus_revision_500_hand.py`
  (renamed to `_604_hand` form) + tests for new modules
- Pre-flight gates: §6.4 G1 + §7 G3 (duplicate detection)
- Exit gate: gto-expert reviews 14 manual canonical hands (§5.1
  track B) for poker correctness; approve required before 12.5E-C

### 12.5E-C — Labelling round

- Entry: 12.5E-B merged
- Owner: LEAD-PROGRAMMER (dispatch) + 5 sonnet expert labellers
  (per-hand label authoring) + GTO-EXPERT (spot-check round)
- Output: `data/corpus_revision_604_hand_labels_2026-05-XX.jsonl`
  (110 new label rows) + 5 per-labeller JSON files in
  `review/mass_labelling_2026-05-XX/`
- Cost cap: $120 hard cap (per §6.2)
- Exit gate: §7 G1 + G2 + G4 (drift detection)

### 12.5E-D — QC the new corpus

- Entry: 12.5E-C labels PR opened
- Owner: QC stream (V-Implementation-Spec-Match + V-Integration-Trace
  per `feedback_qc_required_before_approval.md` milestone scope)
- Output: QC findings report; PR review comment
- Exit gate: all 4 QC gates §7 G1-G4 pass; QC APPROVE

### 12.5E-E — Re-train using existing trainer module on master

- Entry: 12.5E-D approved + corpus + labels PRs merged to master
- Owner: LEAD-PROGRAMMER
- Output: re-run of `river-rats-core/train_model_v9_student.py` (no
  trainer code changes; only `--corpus` and `--labels` paths updated
  to the new 604-hand files); 5-seed sweep; chosen-seed model
  artifact at `river-rats-core/models/gto_model_v9_student.json`
  (NOT promoted yet; staged for gate)
- Hyperparameters: identical to 12.5D' (cap=3.0 hybrid weighting,
  pre-pad metadata-only, all hyperparameters from the
  Blueprint §2.6)
- Exit gate: 5-seed run completes; report file produced;
  `_StudentInferenceLike45` invariant test passes (the 17-test suite
  on master)

### 12.5E-F — Gate evaluation against reference set

- Entry: 12.5E-E run complete
- Owner: ML-ARCHITECT (gate evaluation) + GTO-EXPERT (reference-set
  per-hand review of any change vs 12.5D' chosen seed)
- Gate threshold (PRIMARY): median seed solver-corrected ≥ 33 ⇒
  PROMOTE. Reference set = MW-11..MW-50; solver-correction overlay
  applies (MW-30, MW-46, MW-47 per `reference_corrections.md`)
- Gate threshold (SECONDARY): held-out class metrics — BET recall
  ≥ 0.95, RAISE recall ≥ 0.65, CHECK recall ≥ 0.85 (the 12.5D'
  numbers minus 0.05 floor for stability). Both primary AND
  secondary must pass for PROMOTE
- Held-out-vs-reference-set transfer-correlation check (§10): for
  each of the 5 seeds, log per-hand reference-set correctness and
  per-class held-out recall. Pearson correlation reported. Used
  for diagnostic ONLY — does not gate the promote decision
- Exit gate: Owner gate. If median 35-37 (per §9 prediction):
  PROMOTE. If 33-34: PROMOTE with reservation note. If 31-32:
  STOP, reset to escalation per §9. If <31: regression vs 12.5D';
  Direction D refuted; full ml-architect/gto-expert post-mortem

## §9 Predicted outcome (per 12.5D' Q6 spec, refined)

### Blocker importance (the H-FEAT primary test)

- 12.5D / 12.5D' baseline: `nut_flush_block` = 0.0000;
  `flush_draw_block_pct` = 0.0040; `straight_draw_block_pct` =
  0.0086; `nut_made_block_pct` = 0.0095
- 12.5E prediction (H-FEAT correct): `nut_flush_block` ≥ 0.02 (at
  least one bucket of NFD-RAISE situations forces the booster to
  split on the feature); other 3 blockers move to ≥0.01-0.03 each
- 12.5E falsification (H-FEAT wrong, gap deeper): `nut_flush_block`
  stays at 0.0000-0.005 ⇒ corpus expansion did NOT activate the
  feature; H-FEAT diagnosis was incomplete; 12.5F escalation
  required

### Median seed solver-corrected (the primary gate)

- 12.5D / 12.5D' baseline: 31/40
- 12.5E prediction (H-FEAT + H-DIST correct): **35-37/40 (range, not
  point estimate)**. Reasoning: 4 BET-stays-wrong (MW-25/40/42 +
  MW-49) flip on T1+T2+T3 templates ⇒ +3-4. 2 RAISE-stays-wrong
  (MW-45+MW-47) flip on T4+T5 ⇒ +2. 1 CALL-stays-wrong (MW-17)
  flips on T7 ⇒ +0-1 (E-FEATURE component partly resists). 0 to -1
  loss on the over-aggression edge (MW-31, MW-46) if the model
  starts firing RAISE more readily on low-evidence spots. Net:
  +4-7, landing 35-38; 35-37 is the conservative range
- Best-case 38-40: all 7 stay-wrongs flip cleanly + 0 collateral
  loss. Plausible if T3 + T7 fully encode in the feature surface
  AND the labeller round produces tight 5/5 consensus on T5
- Worst-case (still > baseline) 33-34: T5 corpus boost is enough to
  flip MW-47 alone; MW-45 partially flips (mixed-strategy noise);
  MW-25/40 flip cleanly; MW-42 stays wrong (E-FEATURE residual);
  MW-17 stays wrong (E-FEATURE residual). +2-3 net
- Below baseline (<31): structural finding that data-side fix has
  introduced a new failure mode (e.g. RAISE class drift causes
  MW-31 / MW-32 to flip from FOLD → CALL or CALL → RAISE
  incorrectly). Full post-mortem; 12.5F redesign required

### Escalation point: median stays at 31-32

If 12.5E median is 31-32 after the corpus expansion, this is direct
evidence the gap is DEEPER than corpus coverage:

- Either the 110-hand sizing was insufficient (escalate to 150-200,
  +50-100 more T4/T5/T7 hands targeting the H-FEAT primary axis)
- Or the 59-feature surface genuinely cannot encode the
  discriminative reasoning for MW-17/42/45/47 (E-FEATURE primary
  for those four, not just MW-17/42; gto-expert revision required)
- Or both, in which case 12.5F is a JOINT corpus + feature-surface
  expansion requiring a new ml-architect blueprint (out of scope
  for 12.5E)

This escalation point is a known structural risk per 12.5D' Q6
("Sizing could need a 2nd round"). The 12.5E design ships with this
risk acknowledged. The owner gate at 12.5E-F decides whether to
escalate or accept.

## §10 Methodology lesson incorporated

### 10.1 Held-out gates ≠ reference-set gates on this corpus (12.5D' empirical refutation)

12.5D' produced clean held-out class-recall gains (BET +0.176, RAISE
+0.167) AND zero reference-set median movement. The transfer
assumption was the broken link. 12.5E-F evaluates BOTH gates:

- **Held-out gate (secondary).** Same hyperparameters, same 5-seed
  protocol; reports per-class precision/recall/f1 + confusion matrix
- **Reference-set gate (PRIMARY).** Median seed solver-corrected on
  MW-11..MW-50 with `reference_corrections.md` overlay
- **Ship gate is reference-set-primary.** Held-out gate is
  diagnostic (catches data-pipeline breakage); reference-set gate is
  the ship-decision gate. Promote only on reference-set ≥ 33

### 10.2 Held-out-vs-reference-set transfer-correlation check

The trainer report (Section A or new Section F) adds a
transfer-correlation block:

- For each of the 5 seeds, compute (a) per-class held-out recall and
  (b) per-hand reference-set correctness (40-vector of 0/1)
- Compute Pearson correlation between (mean held-out recall, RS
  correctness count) across the 5 seeds
- Report the correlation in Section F. Document expectation: weak
  positive correlation (~0.1-0.3) is normal; near-zero or negative
  is the same pattern 12.5D'/12.5D showed (indicates the corpus
  doesn't predict the reference set; further data-side iteration
  needed)

This is a diagnostic, not a gate. It informs whether 12.5E's
data-side fix successfully tightened the held-out↔reference-set
relationship — or whether the gap is structural and persists.

### 10.3 The "sizing-could-need-a-2nd-round" risk made explicit

Per 12.5D' Q6: 110 hands is conservatively-sized for
H-FEAT/H-DIST coverage. If 12.5E's predicted blocker importance
movement (0.0000 → ≥0.02) does NOT materialise, this is the
falsification signal. Owner is forewarned that 12.5F may be needed.
This is NOT a quality compromise — it's the empirical reality that
big-DL-style "more data fixes everything" doesn't apply when the
discriminative axes are partly outside the feature surface.

## §11 References

All citations pre-flighted on master HEAD `1b95648` per
`feedback_spec_vs_infrastructure_code_drift.md` dispatch protocol
amendment.

| Citation | File:Path | Verified |
|---|---|---|
| 12.5D' findings | `/tmp/ml_architect_125d_prime_findings.md` | exists; read in full |
| Per-hand E-DIST/E-FEATURE diagnosis | `/tmp/gto_expert_125d_prime_findings.md` | exists; read in full |
| 12.5D' BLOCKED comm | `/tmp/blocked_125d_prime.md` | exists; read in full |
| 12.5D' trainer report | `/tmp/report_125d_prime.md` | exists; read in full |
| Current corpus | `/home/rupertbeytell/river-rats-v2/data/corpus_revision_500_hand_2026-04-27.jsonl` | exists; 494 lines verified |
| Current labels | `/home/rupertbeytell/river-rats-v2/data/corpus_revision_500_hand_labels_2026-04-27.jsonl` | exists; 494 lines verified |
| Reference set designs | `/home/rupertbeytell/river-rats-v2/design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | exists; MW-11..MW-50 read |
| Mass labelling resolution | `/home/rupertbeytell/river-rats-v2/review/comms/MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md` | exists; pipeline pattern read |
| Dispatch script (existing pipeline) | `/home/rupertbeytell/river-rats-v2/scripts/dispatch_mass_labelling.py` | exists |
| Collect script (existing pipeline) | `/home/rupertbeytell/river-rats-v2/scripts/collect_mass_labels.py` | exists |
| Corpus generation blueprint v3 | `/home/rupertbeytell/river-rats-v2/review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md` | exists; pipeline pattern read |
| 12.5C trainer module | `river-rats-core/train_model_v9_student.py` (master `1b95648`) | confirmed via report's Section A schema notes |
| Solver-vs-expert-labels | `~/.claude/projects/-home-rupertbeytell/memory/feedback_solver_vs_expert_labels.md` | read; constraints applied (§5.2) |
| Bucket-first labelling | `~/.claude/projects/-home-rupertbeytell/memory/feedback_bucket_first_labelling.md` | read; constraints applied (§3 + §6.5) |
| Quality default no ask | `~/.claude/projects/-home-rupertbeytell/memory/feedback_quality_default_no_ask.md` | read; applied at §4 + §6.2 |
| No deadlines | `~/.claude/projects/-home-rupertbeytell/memory/feedback_no_deadlines.md` | read; applied (no timeline pressure in §8) |
| Spec/infrastructure drift audit | `~/.claude/projects/-home-rupertbeytell/memory/feedback_spec_vs_infrastructure_code_drift.md` | read; applied to this §11 |
| Reference corrections | `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` | read; applied at §8-F |
| 12.5D' dispatch | `review/comms/MAIN_TERMINAL_PHASE125D_PRIME_DISPATCH_2026-05-04.md` | cited via 12.5D' BLOCKED comm |
| 12.5D' synthesis (owner gate) | (orchestrator-authored; 12.5D' synthesis comm) | inferred from owner direction-D pick at the gate |

---

**Status: DESIGN COMM AUTHORED. 110-hand expansion across 8 templates;
5-expert labelling round; 4 QC gates; 6 phases (12.5E-A through
12.5E-F); reference-set-primary ship gate at median ≥ 33;
H-FEAT-falsification escalation point at median 31-32. Awaiting
orchestrator + owner approval.**
