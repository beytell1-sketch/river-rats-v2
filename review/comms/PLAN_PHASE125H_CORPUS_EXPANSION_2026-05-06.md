---
date: 2026-05-06
from: LEAD-PROGRAMMER (architect hat — Phase 12.5H-A corpus-expansion design)
to: Main terminal (orchestrator) · Owner · GTO-EXPERT (review) · ML-ARCHITECT (review) · QC stream
re: Phase 12.5H corpus expansion — design comm with 12.5C/D/D'/E/G/H-pre empirical evidence baked in
status: DESIGN — corpus-side workstream blueprint; HOW-only per `feedback_orchestrator_decides_not_recommends.md`
---

# Phase 12.5H corpus expansion — design comm (B-then-C step 2)

## §1 Scope and authority

**Scope.** 12.5H is the corpus-side workstream for B-then-C step 2 (Direction C / corpus expansion), following 12.5G's empirical refutation of cap-as-lever. 12.5H targets the 5 reference-set stay-wrong hands at 12.5E-E (MW-17, MW-25, MW-40, MW-45, MW-47) by adding template families specifically aimed at the per-hand E-DIST diagnoses, plus a "T-RAISE-stabilize" template aimed at tightening the 12.5H-pre 60/40 bimodal `nut_flush_block` activation distribution. Trainer module is reused (12.5C blueprint, master `1e4e47e`); v3.4 prompt is reused (master `a598f0a`); no Path Y boundaries crossed.

**Active authority chain (chronological):**
- 12.5C blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (master `1e4e47e`, PR #122) — trainer module spec
- 12.5E-A design (structural template for this design): `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (master `bad1396`, PR #133)
- 12.5E-B amendment merged: master `0eaac06` (PR #136) — Path B carve-out + 14 manual canonicals + hero-only convention + v3.3 prompt
- 12.5E-C labels final via Opus tier-up cross-check: master `3914fea` (PR #146) — 110 labels accepted; v3.4 prompt added
- 12.5E-D corpus QC APPROVE: master `4070a11` (PR #150) — 4 G-gates passed; G4 RAISE drift design-intended
- 12.5E-E re-train BLOCKED owner-tie-gate: master `b51e525` (PR #152) — median 32; H-FEAT confirmed at chosen seed (0.0268)
- 12.5E-F synthesis owner gate (B-then-C compound recommendation): master `16351e1` (PR #155)
- Opus second-tier evaluation: `review/comms/ORCH_OPUS_125E_F_EVALUATION_2026-05-05.md` (master `16351e1`)
- 12.5G cap-non-binding refuted: master `2135fc8` (PR #157) — B-then-C step 1 null result; cap as lever empirically refuted
- 12.5H-pre cross-seed validation: master `edd5556` (PR #161) — H-FEAT validated at cross-seed median (0.0268), volatile (60/40 bimodal)
- 12.5H-A dispatch: `review/comms/MAIN_TERMINAL_PHASE125H_A_DESIGN_DISPATCH_2026-05-06.md` (master `5f9c507`, PR #164)

**Authority limits.** This is HOW-only. The WHAT decision (Direction C / corpus expansion) is owned by orchestrator + owner (decided at 12.5E-F synthesis owner gate, default = slow-quality compound B-then-C). Sequencing within 12.5H is owned by orchestrator. Quality decisions inside the design (sample size, expert count, QC gate thresholds) are made here per `feedback_quality_default_no_ask.md` — not surfaced as open questions.

## §2 Empirical diagnosis (refined per 12.5H-pre + 12.5G)

12.5H is informed by THREE empirical updates beyond 12.5E-A's diagnosis:

### 2.1 H-FEAT validated at cross-seed median, but volatile

Per 12.5H-pre cross-seed analysis (5 seeds × 2 caps; cap=3.0 byte-identical to cap=4.0 at trainer time):

| seed | nut_flush_block importance |
|---|---|
| 0 | 0.1406 |
| 1 | 0.0577 |
| 2 | **0.0268** ← 12.5E-E chosen seed |
| 3 | **0.0054** ← 12.5G chosen seed |
| 4 | 0.0000 |
| **median** | **0.0268** |

- Median **0.0268 ≥ ml-architect Q4 floor 0.02** → H-FEAT VALIDATED at the median level
- Range [0.0000, 0.1406]; 60% (3 of 5) seeds activate the feature ≥ 0.02; 40% near-zero
- **Bimodal**: the booster either learns `nut_flush_block` heavily OR not at all per seed; train/test split variance per seed determines which
- Of 4 P1 blockers, ONLY `nut_flush_block` is cross-seed validated; `flush_draw_block_pct` 20% seeds ≥ 0.02; `straight_draw_block_pct` 0%; `nut_made_block_pct` 0% — 3 of 4 P1 blockers are dead weight in the 59-feature surface

**Implication for 12.5H design:** the 60/40 bimodal pattern signals corpus signal is at the boundary of consistent learnability. More T5-pattern situations (or similar NFD-blocker-discriminative situations) would shift the distribution toward consistent activation (target ≥80% seeds ≥ 0.02). This motivates the new T-RAISE-stabilize template (§3 below).

### 2.2 Cap is non-binding on the 604 corpus

Per 12.5G + 12.5H-pre byte-identical confirmation: the 12.5E corpus expansion (5.9% → 11.26% RAISE share) lifted the natural per-class inverse-frequency boost below cap=3.0 (max RAISE boost = 1.776×). cap=3.0 vs cap=4.0 produces byte-identical models per seed (Δ = 0.0000 across all 5 seeds on `nut_flush_block`, held-out acc, boosted rounds). **Cap is no longer a meaningful lever on this corpus.** Future cap-tuning workstreams (12.5I or beyond) require a pre-flight check that the cap actually binds (TC-X-CAP-BINDING-PRE-CHECK).

12.5H takes this as locked: no cap tuning in scope; corpus expansion is the only viable direction.

### 2.3 Per-hand E-DIST/E-FEATURE classification (Opus second-tier evaluation, PR #155)

Of 5 reference-set stay-wrong hands at 12.5E-E:

| Hand | Direction | Diagnosis (Opus 12.5E-F + gto-expert 12.5D' twice-confirmed) | 12.5H Template family |
|---|---|---|---|
| **MW-17** | under-aggress (FOLD vs CALL) | E-FEATURE primary (implied-odds + nut-FD-blocker against CO range; signal partially outside 59-feature surface) | T7-extension (NFD+overcards CALL implied-odds) |
| **MW-25** | under-aggress (CHECK vs BET) | Pure E-DIST (monotone-multiway-checked-through semi-bluff with FD + overcard; corpus has no analogues) | T8' (monotone-multiway-checked-through) |
| **MW-40** | under-aggress (CHECK vs BET) | Pure E-DIST (TP-medium-kicker 4-way IP after PFR check; "PFR-checks-back-Ax 4-way" sub-pattern is rare in corpus) | T9' (PFR-checks-back-Ax-multiway) |
| **MW-45** | under-aggress (CALL vs RAISE) | Pure E-DIST (slowplayed set → turn lead → raise for value; structurally rare in corpus) | T10' (slowplay-set-turn-lead expansion beyond 12.5E T4) |
| **MW-47** | under-aggress (CALL vs RAISE corrected) | Compound E-DIST + E-FEATURE with partial H-FEAT leverage; feature now active (0.0268 cross-seed median) but specific 4-way bet+call OOP profile differs from T5 exemplars | T-RAISE-stabilize (additional bet+call multiway with villain_air ≥ 0.05) |

Plus **MW-20 newly broken at 12.5E-E** (over-aggress; RAISE vs CALL) — over-rotation downstream of stronger RAISE-class corpus signal. 12.5H aims to NOT amplify this regression; the T-RAISE-stabilize template is sized conservatively to avoid further RAISE inflation.

**Aggregate diagnosis:**
- 3 of 5 are pure E-DIST (MW-25, MW-40, MW-45): corpus expansion targeting their patterns is the ONLY lever; H-FEAT activation provides zero leverage
- 1 of 5 is E-FEATURE primary (MW-17): T7-extension provides marginal leverage; full fix would require feature-engineering (out of Path Y / 12.5H scope; would be 12.5I or beyond)
- 1 of 5 is compound (MW-47): T-RAISE-stabilize aims to push the booster's NFD-blocker pattern coverage to include MW-47's exact spec

**Distinct-cause hands** MW-31, MW-46 stay wrong (feature-surface gap; out of Path Y scope; documented as residual).

### 2.4 H-TREE rejected (carries forward from 12.5E-A)

xgboost trees with `max_depth=5`, `n_estimators=800`, 287-720 actual rounds at hyperparameter settings that already passed Gate 2.3 overfit/underfit checks have ample capacity. Corpus expansion is the intervention; hyperparameter tuning is locked.

## §3 Target situations to add (failure templates per E-DIST diagnoses)

Five new template families addressing the 5 stay-wrong hands + the seed-volatility gap. Per Opus second-tier evaluation Q-eval-3 §C and 12.5E-A §3 structural template.

### Template T8' — BET-stays-wrong: monotone-flop FD-with-overcard checked-through 4-way (MW-25 family expansion)

- **Composition triple:** drawing (FD + 1-2 overcards, hero NOT necessarily the nut FD) / IP / multiway-checked-through
- **Board family:** monotone flop, high card 7-A; intentional variation across suits beyond 12.5E T1
- **Action family:** PFR opens, callers, hero IP, all check to hero on flop
- **Hands to add:** 18 (substantially expanded vs 12.5E T1's 12; MW-25 still wrong → high-priority + variation needed)
- **Source:** Track A situation factory; reuse `T1MonotoneFDCheckedThrough` class with extended config list (cover suit variations + hero hand variations the 12.5E T1 missed; specifically include K-high FD + 2 overcards configurations matching MW-25's `Ks7s on As9s5d` pattern)
- **Labelling rule (bucket-first):** drawing-bucket BET; semi-bluff for fold equity + equity denial + protection at low cost when villains all signal weakness; classic Position Amplification axis. **Critical:** labellers must consider K-high FD (not just nut FD) so the corpus contains BET examples for hero-not-the-blocker variants
- **Discriminative axis:** `is_monotone=1 ∧ has_flush_draw=1 ∧ num_opponents>=3 ∧ villain_aggression_count=0 ∧ is_paired=0`; encodable in 59-feature surface; corpus needs more analogues to teach generalization (12.5E T1's 12 hands all consensus to CHECK, signaling labellers are sensitive to DO NOT Rule 2 — the 18-hand expansion explicitly tests both BET and CHECK reasoning)
- **Predicted v3.4 protocol output:** majority BET (drawing-bucket reasoning anchor) per labeller round; 12.5E T1's 14/14 CHECK consensus suggests labellers may invoke DO NOT Rule 2 over drawing-bucket BET intent. Expect 60-80% BET / 20-40% CHECK split (mixed; informative either way for the booster)

### Template T9' — BET-stays-wrong: TP-medium-kicker IP 4-way after PFR check (MW-40 family expansion)

- **Composition triple:** TP+ (top pair, T-J kicker) / IP / multiway after PFR check-back
- **Board family:** rainbow A-high or K-high flop, no draws, no pair
- **Action family:** PFR (HJ/CO) opens, hero IP NOT preflop aggressor; flop checks through PFR to hero
- **Hands to add:** 14 (expanded vs 12.5E T2's 10; MW-40 still wrong → broader board + kicker variation)
- **Source:** Track A; reuse `T2TPMediumKickerAfterPFRCheck` extended config; specifically include AJ5r-board + AT/AJ kicker matching MW-40's exact spec
- **Labelling rule:** strong_made bucket; PFR check-back on Ax/Kx in 4-way condenses range to weak Jx, broadways without ace, air; thin value + protection + equity denial
- **Discriminative axis:** `is_strong_made=1 ∧ is_rainbow=1 ∧ villain_checked_back=1 ∧ num_opponents>=2`; encodable; corpus needs more analogues
- **Predicted v3.4 protocol output:** majority BET (12.5E T2 was 12/12 BET — labellers consistently BET this pattern; expansion should preserve)

### Template T10' — RAISE-stays-wrong: slowplayed set into turn lead 4-way (MW-45 family expansion)

- **Composition triple:** set / OOP or IP / 4-way after slowplayed flop (all-check on flop)
- **Board family:** rainbow flop containing hero's pair; turn brings broadway connectivity but NO flush
- **Action family:** PFR opens, multiple callers including hero in BB or BTN; flop all-check; turn villain leads
- **Hands to add:** 14 (expanded vs 12.5E T4's 12; MW-45 still wrong — exact spec of slowplay-then-raise on turn-lead is rare; bigger sample needed for booster to learn the action-tree position)
- **Source:** Track A; extend `T4SlowplaySetTurnLead` with intentional variation across:
  - Set rank (deeper coverage 22-99 with explicit 66 matching MW-45's `6d6c set on AcKd6h-Q`)
  - Turn lead size (50%-75%-pot range)
  - Hero position (BB primary; add BTN secondary as control)
  - Board top-card on turn (J-A)
- **Labelling rule:** monster bucket; CO/HJ leading 75 into 120 4-way represents two-pair (AK, AQ, KQ) + AK-strong + occasional bluffs/draws; raise for value vs AK/two-pair + protection vs gutshots/runner-runner FDs
- **Discriminative axis:** `hand_category=set ∧ villain_aggression_count` showing villain JUST became aggressor (turn lead) ∧ `num_opponents>=2`; encodable; corpus needs more analogues to break generalization from "set bets/raises immediately"
- **Predicted v3.4 protocol output:** majority RAISE (12.5E T4 was 14/14 RAISE — pattern is consistent; expansion preserves and adds variation)

### Template T7-extension — CALL-stays-wrong: NFD+overcards under direct pot odds with implied/blocker reasoning (MW-17 family expansion)

- **Composition triple:** NFD + 1-2 overcards / OOP / facing single bet 3-way (NEW: also include facing-bet-2-way variants to cover MW-17's exact 3-way structure)
- **Board family:** two-tone flop with broadway top card containing hero's nut-FD suit; pot odds threshold 22-30%
- **Action family:** PFR opens, callers, hero in BB facing CO single bet 3-way (no callers behind)
- **Hands to add:** 12 (expanded vs 12.5E T7's 10; MW-17 is E-FEATURE primary so corpus expansion provides marginal leverage only — but 12 hands is enough to cover variant board textures + draw strengths the 12.5E T7 missed)
- **Source:** Track A; extend `T7NFDOvercardsCall` with:
  - raw_equity range 0.22-0.32 to bracket implied-odds reasoning above and below pot odds
  - Pure-NFD AND blocker-without-FD variants (so labellers reason from composition, not just pot odds)
  - Specifically include AdKs/AdQs/AdJs on Jd8d4c-style boards matching MW-17's pattern
- **Labelling rule (BUCKET-FIRST, NOT THRESHOLD per `feedback_bucket_first_labelling.md`):** drawing bucket; reasoning anchor = "raw_equity below pot odds direct, but implied odds + nut-FD blocker against CO's range + 6 likely-clean overcard outs make CALL profitable; absent fold-equity for semi-bluff (not multiway-deep enough), CALL realises equity cheaply"
- **Discriminative axis:** `has_flush_draw=1 ∧ nut_flush_block=1 ∧ overcard_outs>=4 ∧ is_ip=0 ∧ num_opponents=2 (single-bet 3-way)`; encodable in 59-feature surface; **partial leverage — full E-FEATURE fix would require feature-engineering that is out of Path Y / 12.5H scope**
- **Predicted v3.4 protocol output:** majority CALL (12.5E T7 was 6 CALL + 5 RAISE + 1 FOLD split — labellers split between Fix-2 CALL and Fix-2 RAISE depending on villain_air_pct; expansion should cover both regimes more thoroughly)

### Template T-RAISE-stabilize — additional bet+call multiway with villain_air ≥ 0.05 (12.5H-pre seed-volatility fix)

- **Composition triple:** NFD + Ace blocker / OOP / multiway facing bet+call (similar to 12.5E T5)
- **Board family:** two-tone broadway boards with **villain_air_pct ≥ 0.05** (clause-e satisfied per v3.4 carve-out)
- **Action family:** PFR opens, callers including hero in BB/SB, BB checks (or hero IS BB), CO bets, BTN calls, hero faces bet+call OOP
- **Hands to add:** 12 (purely additive to 12.5E T5; aimed at making the 60/40 bimodal H-FEAT activation tighter — target ≥80% seeds ≥ 0.02 importance floor)
- **Source:** Track A; extend `T5NFDGutshotRaiseOOP` with config list specifically chosen to have villain_air_pct in the 0.10-0.20 band (avoid heart-suit broadway-saturated boards which produce villain_air ≈ 0.01-0.02 per 12.5E-C empirical; prefer spades/diamonds/clubs variants on broader board structures). Include MW-47's exact spec (`AsQs on KsJd5s` 4-way bet+call OOP; with villain_air_pct in clause-e-satisfying range)
- **Labelling rule:** drawing bucket (combo-draw with nut blocker); v3.4 Fix 2.1.1 carve-out applies; reasoning anchor = "OOP raise semi-bluff against bet+call 4-way folds out CO's medium-pair barrels and BTN's float range; sets up clean 9 nut-flush outs with fold equity; combined Axes 3+4+5"
- **Discriminative axis:** `nut_flush_block=1 ∧ has_flush_draw=1 ∧ num_callers_to_bet>=1 ∧ villain_aggression_count==1 ∧ is_ip=0 ∧ villain_air_pct >= 0.05` — exactly the v3.4 clause set; aim to provide MORE redundant exemplars per pattern so all 5 seeds activate `nut_flush_block`
- **Predicted v3.4 protocol output:** majority RAISE (10 of 14 12.5E T5 hands consensus RAISE under v3.3, then validated under v3.4 clause-e; expansion should preserve and tighten distribution)

### Template T-CONTROL — control hands across 5 buckets (drift detection for 12.5H-D G4)

- **Composition triple:** mixed across 5 buckets
- **Board family:** mixed
- **Action family:** mixed
- **Hands to add:** 20 (per Opus second-tier "Controls: ~20% to detect labeller drift"; ~22% of 90 = 20)
- **Source:** Track A; reuse `T8Controls` extended; specifically sample patterns that have 494-hand AND 12.5E-110-hand near-equivalents for double-drift detection (12.5E-D's G4 fired on 12.5E-110 vs 494; 12.5H-D's G4 will fire on 12.5H-90 vs 12.5E-604 + 12.5H-90 vs 494)
- **Labelling rule:** bucket-first per memory; same rules
- **Discriminative axis:** detects drift in the new labelling round vs prior rounds (target ≥70% same-action rate on matched controls per design 12.5E-A §7 G4)

### Coverage summary

| Template | Family | Hands |
|---|---|---|
| T8' | Monotone-flop FD-with-overcard checked-through 4-way (MW-25) | 18 |
| T9' | TP-medium-kicker IP 4-way after PFR check (MW-40) | 14 |
| T10' | Slowplayed set into turn lead 4-way (MW-45) | 14 |
| T7-ext | NFD+overcards CALL under pot odds (MW-17) | 12 |
| T-RAISE-stabilize | NFD+gutshot RAISE OOP into bet+call multiway (MW-47 + 12.5H-pre seed-volatility fix) | 12 |
| T-CONTROL | Control hands (mixed bucket) | 20 |
| **Total** | | **90** |

## §4 Quantity and class distribution

### Total: 90 new hands (slow-quality default per Opus second-tier eval upper-bound; not 50)

Per Opus second-tier evaluation Q-eval-3 §C: "50-90 new hands" recommended range. Per `feedback_quality_default_no_ask.md` standing rule, default = upper bound (90). 12.5E-A's analogous decision was 110 vs 100 (chose 110); 12.5H follows the same pattern (90 vs 50; chose 90).

### Why 90 and not 50 or 200?

- **50 hands** would compress the per-template counts below the 12.5E-A `min_child_weight=5` × 2 headroom rule (8-12 per template). Per Opus eval, 50 covers the targeted patterns at the low end but doesn't have headroom for booster generalization.
- **90 hands** gives every template ≥10 hands (T-CONTROL aside) — `min_child_weight=5` × 2 headroom preserved; matches 12.5E-A's per-template sizing logic.
- **200 hands** would help if the 12.5E experience predicted "150+ hands per pattern" was the binding constraint. 12.5E empirical evidence does NOT support that (T5 12 hands DID activate H-FEAT cross-seed median; the volatility issue is bimodal seed activation, not per-template under-sizing). Going to 200 in 12.5H is methodology drift; reserve as escalation point if 12.5H-F gate misses.

### Class distribution after merge

Post-12.5H corpus = 604 + 90 = 694 hands. Predicted class distribution shifts:

| Class | 12.5E corpus (604) | +12.5H predicted adds | Post-12.5H (694) | Pre/post % |
|---|---|---|---|---|
| FOLD | 75 | 4 (T-CONTROL split) | 79 | 12.4% → 11.4% |
| CHECK | 271 | 14 (8 T8' minority + 6 T-CONTROL) | 285 | 44.9% → 41.1% |
| CALL | 72 | 14 (12 T7-ext + 2 T-CONTROL) | 86 | 11.9% → 12.4% |
| BET | 118 | 24 (10 T8' majority + 14 T9') | 142 | 19.5% → 20.5% |
| RAISE | 68 | 26 (14 T10' + 12 T-RAISE-stabilize) | 94 | 11.3% → 13.5% |
| **Total** | **604** | **90** | **694** | |

**RAISE class shifts modestly 11.3% → 13.5% (+2.2pp)** — intentionally smaller shift than 12.5E's +5.4pp jump. MW-20 newly-broken in 12.5E-E was attributed to over-rotation downstream of corpus RAISE-class shift; 12.5H sizing is conservative to avoid amplifying that pattern.

**Cap-binding pre-flight check (TC-X-CAP-BINDING-PRE-CHECK)** at 90 RAISE in 694 corpus: train slice 80% → ~75 RAISE; mean ≈ 555/5 = 111; max boost = 111/75 = 1.48× — STILL below cap=3.0. Cap remains non-binding. Confirmed via this design's pre-flight; documented in §10 methodology.

## §5 Sourcing strategy

### 5.1 Two-track sourcing (carries forward from 12.5E-A)

**Track A — situation factory (deterministic, parametric).** Templates T8', T9', T10', T7-ext, T-RAISE-stabilize all reuse `scripts/build_corpus_revision_125e_situations.py` (master `0eaac06`) with extended config lists per template. T-CONTROL also uses Track A. Each module emits deterministic hands keyed by template + parameter values.

**Track B — manual canonical authoring.** A subset of 6-8 hands across T8', T9', T10', T-RAISE-stabilize (specifically: 1 manual canonical for the MW-25-exact-replica in T8', 1 for MW-40-exact in T9', 1 for MW-45-exact in T10', 1-2 for MW-47-exact in T-RAISE-stabilize, plus 2-3 spares). These are GTO-correctness load-bearing for the migration's empirical test on the specific reference-set hands. Gto-expert reviews the 6-8 manual hands before they enter the labelling pipeline (per 12.5E-B precedent).

### 5.2 Solver usage policy (per `feedback_solver_vs_expert_labels.md`)

- **Solver MUST NOT generate the labels.** Per memory: solver outputs are for verification and research only.
- **Solver MAY be used in two narrow modes** (carries forward from 12.5E-A §5.2):
  1. *Verify-after.* After the multi-expert labelling round produces consensus labels, run the resulting (situation, label) pairs through GTO Wizard / PioSolver to flag situations where consensus disagrees with solver. Flagged situations are reviewed: if expert reasoning is sound but uses features not in the surface (i.e., solver-reasoning that the model can't replicate), the EXPERT label stands. If expert reasoning is empirically flawed, the situation is sent back for re-labelling — but the solver does NOT supply the new label.
  2. *Research preflight.* Before the labelling round, gto-expert can use solver to research whether T-RAISE-stabilize / T8' / T10' spots have a single canonical GTO answer or a mixed-strategy. If mixed, the labelling round documents the mix and labellers vote on the dominant action.
- **Boundary check.** Solver may NOT be cited inside the labeller prompt as a rule. Solver may NOT influence the bucket definitions (these are poker-reasoning anchors per `feedback_bucket_first_labelling.md`). Solver-corrections to the reference set apply ONLY at the gate stage (12.5H-F), never on the training labels.

### 5.3 Expansion to existing pipeline

The 12.5H builder (LEAD-PROGRAMMER in 12.5H-B) extends `scripts/build_corpus_revision_125e_situations.py` with new template config lists for T8'/T9'/T10'/T7-ext/T-RAISE-stabilize/T-CONTROL. Output file: `data/corpus_revision_125h_situations_2026-05-XX.jsonl` + `data/corpus_revision_125h_manual_canonicals_2026-05-XX.jsonl`. Existing 604-hand corpus is locked; the new 90 hands are additive only.

## §6 Labeller pipeline reuse

Same pipeline as 12.5E-C with the following:

### 6.1 Reuse (no changes)

- `scripts/dispatch_mass_labelling.py` (master `0eaac06` post-12.5E-C parameterization) — pass `--protocol prompts/gto_labeller_v3.4.md`
- `scripts/collect_mass_labels.py` (master `0eaac06` post-12.5E-C glob refactor)
- v3.4 protocol prompt at `prompts/gto_labeller_v3.4.md` (master `a598f0a`) — Fix 2.1.1 clause-e villain_air floor at 0.05
- Per-labeller JSON output schema (Phase B Protocol A)
- Plurality-consensus aggregation (consensus action = mode of valid votes; consensus confidence = count_max / vote_count)

### 6.2 Quality default — 5 expert labellers per hand (NOT 3)

Per `feedback_quality_default_no_ask.md`. The 12.5E-C labelling round used 5 sonnet labellers per hand and produced 0 refusals on 110 × 5 = 550 calls; 83/110 hands at unanimous (1.00) confidence. 12.5H uses the same: 5 sonnet labellers × 90 hands = 450 labels. Estimated cost: ~$15-40 (5 sonnet subagents × ~140K-token brief × ~25K-token output each); hard cap: $120 per 12.5E-C precedent.

### 6.3 Pilot-first per `feedback_pilot_first_for_long_jobs.md`

- **Pilot phase**: dispatch first labeller on the 6-8 manual canonicals + 12 random parametric hands = ~18-20 hands (smoke test). Verify v3.4 prompt accepted, JSON output well-formed, per-class distribution sensible.
- **Tier-up verification per same memory**: if pilot output passes structural checks but H-FEAT primary canonicals (MW-47 exact, MW-25 exact, MW-40 exact, MW-45 exact) labels are unexpected, orchestrator-side Opus cross-check on contested hands BEFORE committing to full 5×90 round
- **Full phase**: only fires after pilot APPROVE
- This pattern was empirically validated at 12.5E-C → 12.5H-pre cycle (pilot-first caught the cap-non-binding finding cheaply; tier-up caught the Sonnet=Opus alignment to make labels final without full Opus relabel)

### 6.4 Hero-only convention (per 12.5E-B amendment)

`prior_actions` field contains ONLY actions performed by hero (where actor matches `hero_position`). Existing 494 corpus convention; 12.5E-B amendment applied to 110 new hands; 12.5H carries forward.

### 6.5 Pre-flight join-cardinality gate (per 12.5D' dispatch protocol amendment)

Builder in 12.5H-B runs the existing pre-flight pattern:

```
Pre-flight 1 (sample): on ≥5 sample rows from new factory output spanning the file
  (e.g., row 1, 23, 45, 67, last), verify pilot_hand_id present + unique + non-null
  in BOTH situations and labels JSONLs. STOP if cardinality < 1.0 on the sample.

Pre-flight 2 (empirical): on the full 90 new rows + 604 existing, verify joined
  cardinality = 694/694 = 1.0. STOP if < 0.99.

Pre-flight 3 (no duplicate detection): assert that pilot_hand_id values in the new
  90 rows do NOT collide with PILOT_001..PILOT_604. STOP if collision detected.
```

New `pilot_hand_id` range: PILOT_605..PILOT_694 (90 hands).

The `<0.99 = STOP` threshold is intentionally tight for milestone data PRs (per 12.5D' amendment); this is a milestone PR.

### 6.6 Bucket-first protocol unchanged

Per `feedback_bucket_first_labelling.md`, the labeller prompt describes buckets qualitatively. No equity thresholds in the prompt. Reasoning anchors per template (§3) inform what poker reasoning each template requires but DO NOT enter the prompt as template-specific rules — the prompt remains template-agnostic.

## §7 QC gates (pre-merge for the data PR)

### G1 — Join-cardinality check (paired with 12.5H-B builder)

Per §6.5 pre-flight. QC verifies builder ran the pre-flight, that the 12.5H-B report includes the 3 pre-flight outputs, and that the merged corpus joins 694/694.

### G2 — Label distribution sanity

Empirical distribution of the new 90 labels MUST satisfy:
- No class < 5% of the new 90 (i.e., no class has < 5 labels)
- Class distribution within ±20% of the §4 target per class (e.g., 26 RAISE target → 21-31 RAISE acceptable)
- Median consensus_confidence ≥ 0.6 across the 90 hands (12.5E-C round was 1.0 median; 0.6 is conservative floor)

### G3 — Duplicate detection vs existing 604 rows

QC computes the (board, hero_cards, hero_position, prior_actions) tuple for each of the 90 new rows and asserts NO tuple matches any of the 604 existing rows. STOP on any match.

### G4 — Labeller-drift detection (compare new round vs old round on T-CONTROL hands)

The 20 T-CONTROL hands must be sampled such that ~half (≥10) have near-equivalents in the 494-hand and/or 110-hand 12.5E rounds (matched on bucket + board family + facing-bet status). For each matched pair, QC computes consensus action + confidence on both; reports:
- Same-action rate (target ≥ 70%; <70% = drift, BLOCKER)
- Mean confidence-Δ (|new - old|; target < 0.15)

This catches labeller-protocol drift between the v3.4 labelling round and prior rounds. If drift detected, REJECT the round and re-run.

### G5 — NEW: cap-binding pre-flight check (TC-X-CAP-BINDING-PRE-CHECK)

Pre-merge to 12.5H-D: verify that any future cap-tuning workstream's cap value would bind on the merged 694-hand corpus. Compute `mean(class_counts) / min(class_counts)` and compare against candidate caps. If cap < computed boost, cap is non-binding (per 12.5G empirical refutation). 12.5H itself does NOT tune cap; this gate is forward-looking for any 12.5I cap-related dispatch.

Per §4 prediction at 90 RAISE in 694 corpus: max boost ≈ 1.48× — cap=3.0 remains non-binding. G5 documents this and queues the implication for any forward cap-tuning dispatch.

## §8 12.5H workstream phases

Six phases. Each phase has an entry condition and a blocking exit gate. Orchestrator owns phase sequencing (per `feedback_explicit_action_trigger.md`: each phase fires on prior phase merge + explicit `MAIN_TERMINAL_*_TRIGGER` comm). This design owns each phase's HOW.

### 12.5H-A — Design comm (THIS DOC)

- Entry: 12.5H-pre merged + orchestrator dispatch (PR #164)
- Owner: LEAD-PROGRAMMER architect hat
- Output: `review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-XX.md` (this doc)
- Exit gate: standalone QC pre-merge audit (3 audits per dispatch); on QC APPROVE, orchestrator merges; dispatches 12.5H-B

### 12.5H-B — Situation generation

- Entry: 12.5H-A approved + 12.5H-B dispatch trigger
- Owner: LEAD-PROGRAMMER default hat
- Output:
  - `data/corpus_revision_125h_situations_2026-05-XX.jsonl` (~84 parametric hands; 18 T8' + 14 T9' + 14 T10' + 12 T7-ext + 12 T-RAISE-stabilize + 14 T-CONTROL parametric, leaving 6 control + 6 manuals out)
  - `data/corpus_revision_125h_manual_canonicals_2026-05-XX.jsonl` (~6 manual canonicals — 1 per high-priority template)
  - Extended `scripts/build_corpus_revision_125e_situations.py` with new template config lists
  - Builder report with G1-G3 self-checks
- Pre-flight gates: §6.5 G1 + §7 G3 (duplicate detection vs 604 existing)
- Exit gate: gto-expert reviews the 6 manual canonical hands for poker correctness; APPROVE required before 12.5H-C

### 12.5H-C — Labelling round

- Entry: 12.5H-B merged
- Owner: LEAD-PROGRAMMER (dispatch) + 5 sonnet expert labellers (per-hand label authoring) + orchestrator (Opus tier-up cross-check on contested hands per `feedback_pilot_first_for_long_jobs.md`)
- Output:
  - `data/corpus_revision_125h_labels_raw_2026-05-XX.jsonl` (450 raw 5-labeller responses)
  - `data/corpus_revision_125h_labels_2026-05-XX.jsonl` (90 consensus rows)
  - Builder report with §"Pilot phase results" + §"Tier-up cross-check" + per-template consensus breakdown
- Cost cap: $120 hard cap (per §6.2)
- Exit gate: §7 G1 + G2 + G4 (drift); orchestrator-side Opus tier-up cross-check on T-RAISE-stabilize + T8'/T9'/T10' MW-exact-replica labels for "labels final" verdict

### 12.5H-D — QC the new corpus

- Entry: 12.5H-C labels PR opened
- Owner: standalone QC stream
- Output: QC findings report
- Exit gate: all 4 G-gates §7 G1-G4 pass + new G5 cap-binding pre-flight observation; QC APPROVE

### 12.5H-E — Re-train using existing trainer module on master

- Entry: 12.5H-D approved + corpus + labels merged to master
- Owner: LEAD-PROGRAMMER default hat
- Output:
  - Re-run of `river-rats-core/train_model_v9_student.py` (no trainer code changes; only `--corpus` and `--labels` paths updated to merged 694-hand files; `--phase-label "12.5H"`)
  - 5-seed sweep with cross-seed importance reporting (per TC-X-CROSS-SEED-IMPORTANCE methodology amendment activated at 12.5H-pre)
  - Chosen-seed model artifact at `river-rats-core/models/gto_model_v9_student.json` (NOT promoted yet; staged for 12.5H-F gate)
- Hyperparameters: identical to 12.5E-E (cap=3.0 hybrid weighting; pre-pad metadata-only; 5 seeds 0-4) — cap is non-binding so this is structural identity not trade-off
- Exit gate: 5-seed run completes; report file produced with cross-seed importance for `nut_flush_block` (and other P1 blockers); `_StudentInferenceLike45` invariant test passes

### 12.5H-F — Gate evaluation against reference set

- Entry: 12.5H-E run complete
- Owner: standalone QC stream + orchestrator-side Opus second-tier evaluation
- Gate threshold (PRIMARY): **median seed solver-corrected ≥ 33** ⇒ PROMOTE. Reference set = MW-11..MW-50; solver-correction overlay applies per `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Gate threshold (SECONDARY): cross-seed `nut_flush_block` median ≥ 0.04 (target; up from 12.5H-pre 0.0268); ≥80% seeds above 0.02 floor (up from 60%); held-out CHECK recall ≥ 0.85 (up from 12.5E-E 0.815)
- Held-out-vs-reference-set transfer-correlation check: per-seed correlation between held-out class-recall and reference-set correctness; report for diagnostic
- Exit gate: owner gate. Outcomes:
  - Median ≥33 AND secondary cleared → PROMOTE
  - Median 33-34 with secondary partial → PROMOTE WITH RESERVATION (model card noting residual gaps per Opus 12.5E-F precedent)
  - Median 31-32 → owner-tie-gate; orchestrator authors synthesis comm with options
  - Median <31 → STOP; corpus expansion refuted at gate; 12.5I escalation (feature engineering or methodology recharacterization)

## §9 Predicted outcome (per Opus 12.5E-F evaluation refined)

### Median seed solver-corrected (the primary gate)

- 12.5E-E baseline: 32/40
- 12.5H prediction (corpus expansion working as designed): **33-35/40 conservative range**
  - Reasoning: of 5 stay-wrong hands, T8'/T9'/T10' targets 3 pure E-DIST (MW-25, MW-40, MW-45) — Opus 50-60% gap-close estimate × 3 hands = ~1.5-2 hand expected flips
  - T7-ext targets 1 E-FEATURE primary (MW-17) — partial leverage; Opus 30-40% flip estimate = ~0.3-0.4 hands
  - T-RAISE-stabilize targets 1 compound (MW-47) — H-FEAT now active + closer exemplars; Opus 40-50% flip estimate = ~0.4-0.5 hands
  - Total expected: ~2.2-2.9 hand flips; minus ~0-1 newly-broken downstream of new RAISE-class signal
  - Net: **+1 to +3 hands** beyond 12.5E-E median 32 → **median 33-35**
- Best-case 36-37: all targeted hands flip + 0 collateral loss + T-RAISE-stabilize tightens H-FEAT activation cross-seed
- Worst-case (still ≥31) 32-33: only T10' MW-45 flips (most amenable to corpus expansion); MW-47 H-FEAT helps but doesn't close; MW-25/40 stay E-DIST-locked
- Below baseline (<31): structural finding that 12.5H corpus expansion introduced new failure modes (e.g., over-aggression amplification) at scale; 12.5I escalation required

### Cross-seed `nut_flush_block` importance (the secondary gate)

- 12.5H-pre baseline: median 0.0268 ± std 0.0514 (60% above floor; bimodal)
- 12.5H prediction: median **0.04-0.06** (above 0.02 floor); **≥80% of seeds ≥ 0.02** (up from 60%)
  - Reasoning: T-RAISE-stabilize adds 12 NFD-blocker exemplars at villain_air ≥ 0.05 (clause-e satisfied); these supply MORE consistent signal for the lower-end seeds (3 + 4) that previously didn't activate the feature
  - Existing T5 12 hands + T-RAISE-stabilize 12 = 24 NFD-blocker exemplars (doubled); booster has more redundancy → more train/test splits hit the activation pattern
- Falsification: if cross-seed median stays at 0.0268-0.0300 with bimodal pattern → seed-volatility hypothesis from 12.5H-pre is wrong; likely root cause is warm-start anchor or booster initialization (not corpus signal density). 12.5I would need to investigate.

### MW-31 / MW-46 distinct-cause hands

Both stay wrong as in 12.5E/G. Feature-surface gap (no encoded signal for villain check-raise credibility); out of Path Y / 12.5H scope. 12.5I or beyond may add a "villain check-raise frequency" feature.

### MW-20 (newly broken at 12.5E-E)

Predicted: stays broken (over-aggression downstream of RAISE-class signal). T-RAISE-stabilize is sized conservatively (12 hands; +2.2pp RAISE share, vs 12.5E's +5.4pp jump that triggered MW-20 break) to avoid further amplification, but cannot un-break what's already broken without recharacterizing the model's BET/RAISE boundary. 12.5I if needed.

### Escalation point: median stays at 31-32

If 12.5H median fails to clear ≥33, this is direct evidence that:
1. Corpus expansion sizing (50-90 hands range) is insufficient for the E-DIST gap
2. OR the E-DIST hands' transfer assumption (Opus 50-60%) was over-confident
3. OR the per-template patterns chosen (T8'/T9'/T10') don't match the reference hands' exact discriminative axes closely enough

12.5I would then face a choice: (a) further corpus expansion (200+ hands) targeting the same 5 stay-wrong patterns more densely; (b) feature engineering for E-FEATURE-primary residuals (out of Path Y); (c) accept the 32/40 ceiling on this corpus + feature-surface combination and ship with explicit reservation note.

## §10 Methodology lessons baked in

From the 12.5C/D/D'/E/G/H-pre cycle, these methodology rules are now active and apply to all future trainer + corpus dispatches:

### 10.1 Cross-seed feature-importance reporting (TC-X-CROSS-SEED-IMPORTANCE)

Future trainer reports MUST include cross-seed median + std + min/max + % above-floor for any feature whose importance is invoked as evidence for/against a migration premise. Single-seed snapshots are insufficient — proven empirically by 12.5E-E chosen seed `nut_flush_block`=0.0268 vs 12.5G chosen seed=0.0054 discrepancy that necessitated 12.5H-pre.

12.5H-E trainer report Section C must include this; 12.5H-E may also implement per-seed importance logging directly in trainer module so future runs report this without post-hoc Path 2 extraction (per 12.5H-pre dispatch §"What's queued").

### 10.2 Cap-binding pre-flight check (TC-X-CAP-BINDING-PRE-CHECK)

Before any cap-tuning workstream, compute `mean(class_counts) / min(class_counts)` and compare against candidate caps. If cap > computed natural boost, cap is non-binding (per 12.5G empirical refutation byte-confirmed at 12.5H-pre). 12.5H-D G5 documents this for the 694-hand corpus (max boost ≈ 1.48× at predicted distribution; cap=3.0 remains non-binding).

### 10.3 Tier-up verification on training-data outputs

Per `feedback_pilot_first_for_long_jobs.md` tier-up sub-rule (added 2026-05-04 via 12.5E-C cycle): training-data outputs (labels) require higher-rigor-tier verification before final. Sonnet labels are the primary source; Opus tier-up cross-check on contested hands is the secondary verification. 12.5E-C → 12.5H-pre validated this pattern (orchestrator-side Opus single-pass on 20 contested hands produced 20/20 agreement; full Opus×5 pipeline relabel was unnecessary). 12.5H-C uses the same pattern.

### 10.4 Pilot-first on all long batches

Per `feedback_pilot_first_for_long_jobs.md` (originating rule). 12.5H-C pilot phase = first labeller × ~18-20 hands; gate; full only on pilot APPROVE. Trainer at 12.5H-E pilot = 1-seed dry-run before 5-seed full (per 12.5E-E precedent and dispatch's standing pattern).

### 10.5 Hero-only convention in `prior_actions` (per 12.5E-B amendment)

Existing 494 corpus convention (verified empirically: 0/494 have non-hero actions); 12.5E-B amendment applied to 110 new hands; 12.5H carries forward via `_hero_only_prior_actions` filter in `emit_row` (existing in `scripts/build_corpus_revision_125e_situations.py`).

### 10.6 Pre-flight join-cardinality ≥0.99 (per 12.5D' amendment)

For milestone data PRs (12.5H is one), join-cardinality threshold is `<0.99 = STOP`. Verified at 5+ sample rows AND on full corpus.

## §11 References

All claims in this design are grounded in master HEAD `5f9c507` (commit at design authoring time, verified via `git log -1 origin/master`). Per `feedback_spec_vs_infrastructure_code_drift.md` dispatch protocol amendment, every cited file path is verified to exist on master HEAD before this design is committed.

| Citation | What it asserts | Verified |
|---|---|---|
| 12.5H-A dispatch | `review/comms/MAIN_TERMINAL_PHASE125H_A_DESIGN_DISPATCH_2026-05-06.md` (master `5f9c507`, PR #164) | This design's authorisation |
| 12.5H-pre cross-seed validation | `review/comms/BUILDER_REPORT_PHASE125H_PRE_CROSSSEED_2026-05-05.md` (master `edd5556`, PR #161) | H-FEAT median 0.0268; bimodal 60/40 |
| 12.5H-pre extractor script | `scripts/extract_cross_seed_importance.py` (master `edd5556`) | Cross-seed importance methodology validated |
| 12.5G cap-non-binding refutation | `review/comms/BUILDER_BLOCKED_PHASE125G_CAP_NON_BINDING_2026-05-05.md` + `PROGRAMMER_REPORT_PHASE125G_CAP_RETUNE_2026-05-05.md` (master `2135fc8`, PR #157) | Cap is non-binding on 604 corpus |
| 12.5E-F synthesis (Opus second-tier) | `review/comms/ORCH_OPUS_125E_F_EVALUATION_2026-05-05.md` (master `16351e1`, PR #155) | Per-hand E-DIST/E-FEATURE classification + 50-90 hand recommendation |
| 12.5E-E re-train | `review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` (master `b51e525`, PR #152) | 12.5E-E baseline data; chosen seed importances |
| 12.5E-D corpus QC | `review/comms/REVIEW_QC_PHASE125E_D_CORPUS_QC_2026-05-05.md` (master `4070a11`, PR #150) | Corpus QC pattern + G4 drift detection |
| 12.5E-C LABELS FINAL | `review/comms/MAIN_TERMINAL_PHASE125E_C_LABELS_FINAL_2026-05-05.md` (master `3914fea`, PR #146) | v3.4 prompt + tier-up verification pattern |
| 12.5E-B amendment | `review/comms/MAIN_TERMINAL_PHASE125E_B_AMEND_PATH_B_2026-05-05.md` (master `10f914b`, PR #137) | Hero-only convention + Path B + v3.3 |
| 12.5E-A design (structural template) | `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (master `bad1396`, PR #133) | §-structure + sourcing strategy + QC gate pattern |
| 12.5C blueprint | `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (master `1e4e47e`, PR #122) | Trainer module spec |
| v3.4 prompt | `prompts/gto_labeller_v3.4.md` (master `0eaac06` post-12.5E-C) | Fix 2.1.1 clause-e villain_air floor |
| Existing situation factory | `scripts/build_corpus_revision_125e_situations.py` (master `0eaac06`) | Reuse target for 12.5H-B template extension |
| Existing labeller pipeline | `scripts/dispatch_mass_labelling.py` + `scripts/collect_mass_labels.py` (master `0eaac06` post-12.5E-C parameterization) | Reuse unchanged for 12.5H-C |
| Trainer module | `river-rats-core/train_model_v9_student.py` (master `5f9c507`) | Reuse unchanged for 12.5H-E (modulo `--phase-label "12.5H"`) |
| Existing 604-hand corpus | `data/corpus_combined_604_2026-05-05.jsonl` (master `b51e525` post-12.5E-E) | Locked baseline; 12.5H is additive-only |
| Existing 604-hand labels | `data/corpus_combined_604_labels_2026-05-05.jsonl` (master `b51e525` post-12.5E-E) | Locked baseline |
| Reference corrections | `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` | MW-30 CALL, MW-46 CALL, MW-47 RAISE solver overlay at 12.5H-F |
| Memory: quality default | `~/.claude/projects/-home-rupertbeytell/memory/feedback_quality_default_no_ask.md` | 90 hands (upper bound) per slow-quality default |
| Memory: pilot first | `~/.claude/projects/-home-rupertbeytell/memory/feedback_pilot_first_for_long_jobs.md` | Pilot-first + tier-up verification |
| Memory: explicit trigger | `~/.claude/projects/-home-rupertbeytell/memory/feedback_explicit_action_trigger.md` | Phase sequencing requires explicit MAIN_TERMINAL_*_TRIGGER |
| Memory: orchestrator decides | `~/.claude/projects/-home-rupertbeytell/memory/feedback_orchestrator_decides_not_recommends.md` | HOW-only design discipline |
| Memory: bucket-first | `~/.claude/projects/-home-rupertbeytell/memory/feedback_bucket_first_labelling.md` | No equity thresholds in labeller prompt |
| Memory: solver vs expert | `~/.claude/projects/-home-rupertbeytell/memory/feedback_solver_vs_expert_labels.md` | Solver verify-only; never as labels |
| Memory: spec/infrastructure drift | `~/.claude/projects/-home-rupertbeytell/memory/feedback_spec_vs_infrastructure_code_drift.md` | Pre-flight all citations on master HEAD |
| Memory: cross-seed importance | (TC-X-CROSS-SEED-IMPORTANCE; QC institutional memory; activated at 12.5H-pre) | Cross-seed reporting methodology |
| Memory: cap-binding pre-check | (TC-X-CAP-BINDING-PRE-CHECK; QC queued at 12.5G/H-pre) | Cap-binding pre-flight before tuning |
| Memory: failure direction | `~/.claude/projects/-home-rupertbeytell/memory/feedback_failure_direction_classification.md` | Trainer reports classify by direction not just class |

---

**Status: DESIGN COMPLETE. 90-hand corpus expansion across 6 templates targeting 5 stay-wrong reference hands (3 pure E-DIST, 1 E-FEATURE primary, 1 compound) + seed-volatility fix; 5-expert labelling round with v3.4 prompt; 5 QC gates (G1-G4 + new G5 cap-binding pre-flight); 6 phases (12.5H-A through 12.5H-F); reference-set-primary ship gate at median ≥ 33; secondary gate cross-seed `nut_flush_block` median ≥ 0.04 + ≥80% seeds above floor. 6 methodology rules baked in (cross-seed reporting + cap-binding check + tier-up verification + pilot-first + hero-only + pre-flight join-cardinality).**

**Provenance:** Authored at master HEAD `5f9c507`, on branch `programmer/phase125h-a-design-2026-05-06`, per orchestrator dispatch PR #164. LEAD-PROGRAMMER architect-hat authority per orchestrator-named-author rule (`feedback_listen_to_orchestrator_always.md`).
