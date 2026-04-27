---
date: 2026-04-27
from: ml-architect (round 2 reviewer)
to: orchestrator → owner
re: Round 2 review of blueprint v2 at PR #56
verdict: APPROVE-WITH-NITS
---

# Round 2 ml-architect review — blueprint v2

## Source files read for this review

- `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v2_2026-04-27.md` (PR #56 head)
- `review/comms/MAIN_TERMINAL_BLUEPRINT_REVIEW_SYNTHESIS_2026-04-27.md`
- `review/comms/REVIEW_ML_ARCHITECT_BLUEPRINT_PR53_2026-04-27.md` (my prior R1 review)
- `river-rats-core/generate_3way_situations.py` (full)
- `river-rats-core/feature_extractor.py` (lines 2490-2515)
- `river-rats-core/feature_keys.py` (lines 80-109)
- `river-rats-core/gto_model.py` (lines 33-65)
- `river-rats-core/poker_game.py` (lines 1155-1177)
- `data/pilot_corpus_100_hand_2026-04-26.jsonl` (live inspection — all 100 records)
- `data/pilot_corpus_100_hand_2026-04-26.lock.json`
- `review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_*.json` (5 files)
- `training-data/3way_situations_10k.jsonl` (first 5 records)
- `river-rats-core/models/` (directory listing + gto_model_v9_baseline_45feat.json structure)

---

## Q1 — Is R1 (re-extract 100 hands) implementation spec correct?

### prior_actions stores hero's OWN actions only — confirmed

The `generate_3way_situations.py` code at lines 49-51:

```python
prior = []
for prev in decisions[:i]:
    prior.append(f"{prev.street}: {pos} {prev.action}")
```

The variable `pos` is `dec.player_position` — this is the hero's position. The loop iterates over `decisions[:i]` — these are the hero's own prior decisions in the same deal. Critically: `prior_actions` contains **only the hero's own actions**, not all players' actions. Villain preflop actions (opens, calls) are NOT recorded in `prior_actions`.

This was not obvious from the blueprint's description of OQ-4 ("The opener is the first player who made a preflop bet"), which implies searching for any player's preflop raise. The actual reconstruction algorithm is simpler and different: if hero's own `prior_actions` includes a preflop raise, then hero IS the opener.

### OQ-4 is resolvable — algorithm confirmed by live data inspection

I inspected all 100 records from `data/pilot_corpus_100_hand_2026-04-26.jsonl` directly.

**Finding**: `prior_actions` contains preflop actions for all 100 records (100%). The format is `"preflop: POSITION action"` where POSITION is always hero's own position.

**Reconstruction algorithm** (derived from actual data, not blueprint description):

```
if any action in prior_actions satisfies:
    "preflop" in action AND "raise" in action AND hero_position in action:
    _opener_position = hero_position  (hero IS the opener)
    is_preflop_aggressor = 1
else:
    _opener_position = None
    is_preflop_aggressor = 0  (hero called preflop; someone else is the opener)
```

This produces correct results because the hero's `prior_actions` only ever records hero's own actions. A "preflop raise" entry means hero raised preflop = hero opened.

**Count breakdown** (confirmed from live data):
- 51/100 records: `prior_actions` contains `"preflop: {hero_position} raise"` → `is_preflop_aggressor=1`
- 49/100 records: hero called preflop (BB/BTN) → `is_preflop_aggressor=0` (correct default)

**Conclusion for 97/100 hands**: OQ-4 is NOT BLOCKING. The reconstruction is correct.

### Edge case: 3-bet pots — minor error, not blocking

There are 3 records with `is_3bet_pot=1` (all SB position, pot=855 chips). These have `prior_actions = ['preflop: SB raise', 'preflop: SB raise', 'preflop: SB raise', ...]`.

In a 3-bet pot (BTN opens, SB 3-bets, BTN calls), the game's `opener_position` is set to BTN (the first raiser per `poker_game.py` lines 1161-1162 and 1174-1175: `if not self.opener_position: self.opener_position = player.position`). So `is_preflop_aggressor` for SB should be 0 (SB is NOT the opener, BTN is).

The naive reconstruction algorithm (`"preflop raise in prior_actions" → is_preflop_aggressor=1`) will INCORRECTLY set `is_preflop_aggressor=1` for these 3 SB hands.

**Severity**: 3/100 hands (3%). Easily detectable: `is_3bet_pot=1` AND hero is SB AND preflop raise in prior_actions → hero is the 3-bettor, NOT the opener. The programmer should add this guard:

```python
is_3bet = hand.get('feat_dict', {}).get('is_3bet_pot', 0)  # from original corpus
if preflop_raise_found and is_3bet and hero_pos == 'SB':
    _opener_position = None  # hero is 3-bettor, not opener
```

**NOT a blocking issue**. The existing is_3bet_pot feature is available during re-extraction (it's in the original feat_dict), and the fix is 3 lines.

### BB_CHIP_SIZE=10 is correct

Confirmed against `poker_game.py` line 962: `BIG_BLIND = 10`. A standard 3-way raised pot = 80 chips (confirmed in live data: 94 records have pot=80). Conversion: `pot_bb = 80/10 = 8bb`. SPR = `100.0 / 8.0 = 12.5` (correct). The blueprint's `BB_CHIP_SIZE=10` constant is correct.

### extract_all_features inputs are compatible

The blueprint's re-extraction algorithm (Section Q6, script 2) calls `extract_all_features(hand_dict)` with:
- `_opener_position`: reconstructed as described above
- `pot`: `pot_bb = pot_chips / BB_CHIP_SIZE` (in BB units)
- All other fields unchanged

This matches the expected interface. `feature_extractor.py` line 2501: `_opener_pos = hand.get('_opener_position', None)` — matches the passed key name. The pot conversion is correct.

### Labels are confirmed untouched

500 labels (5 labellers × 100) are stored in `review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_N.json` as lists keyed by `ref_id` = `source_situation_id`. Re-extraction modifies only `feat_dict` in a new `_v2.jsonl`; `source_situation_id` is preserved unchanged. Labels remain 100% valid and linked.

**R1 verdict**: Spec is correct with one nit (3-bet SB edge case, 3 hands). Add the `is_3bet_pot` guard to the re-extraction algorithm. Not blocking.

---

## Q2 — Is R2 (feature schema compatibility check) correctly placed?

### Gate placement is correct

R2 runs before warm-start training kickoff, not before corpus generation. This is the right gate point. Corpus generation does not require schema compatibility (it generates new features regardless). Training requires it. The placement in the handoff execution order (Step 5 in Section Q6's test plan) is correct.

### Model naming error: blueprint says "v8 oracle" — should be "v9-baseline"

The blueprint Section Q6 states:
> "Load the warm-start base model artifact (v8 oracle model from `river-rats-core/models/`)"

This is wrong. The v8 model (`gto_model_v8_38feat.json`, `gto_model_v8_hu.json`) is the HU oracle with 38 features — it is not the warm-start base for the 3-way corpus.

From `CLAUDE.md`: "v9-baseline: trained on 45-feature PokerBench, ready for warm-start."

The correct warm-start base is `gto_model_v9_baseline_45feat.json` (45 features). The programmer who implements R2 using the blueprint's "v8 oracle" reference will load the wrong model and get incorrect schema comparison results.

**This is a programmer-blocking NIT**: the wrong model name will cause R2 to compare the wrong schema. The blueprint must correct "v8 oracle" → "v9-baseline" in the R2 script specification.

### The mismatch R2 will find is expected and real

The new corpus has 59 features (confirmed by live inspection of `pilot_corpus_100_hand_2026-04-26.jsonl`). The v9-baseline warm-start model has 45 features. XGBoost warm-start requires identical feature schemas; the mismatch will cause training to fail silently or visibly.

R2's job is correct: detect this mismatch before training. The `--model river-rats-core/models/v8_oracle.json` CLI argument in the blueprint must be changed to `--model river-rats-core/models/gto_model_v9_baseline_45feat.json`.

Additionally, the blueprint spec says "Compare against the 59-feature corpus contract (`FEATURE_COLUMNS` in `river-rats-core/feature_keys.py`)". The actual `FEATURE_COLUMNS` in `gto_model.py` has 55 features (not 59) — the v2.4 P1 blocker features 56-59 (`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`) are defined in `feature_keys.py` but are NOT yet in `gto_model.py`'s `FEATURE_COLUMNS`. The R2 script needs to derive the 59-feature list from the actual corpus (or from a complete enumeration), not from `gto_model.py`'s current `FEATURE_COLUMNS`.

### Missing: resolution path when R2 fails

The blueprint correctly says: "If it fails, the programmer must STOP and report BLOCKED." But R2 WILL fail (45-feature base vs 59-feature corpus). The blueprint offers no resolution path. The programmer will STOP and have no instructions for what to do next.

This is an incompleteness in the spec. The expected failure is not a blocker in the traditional sense — it is a known pre-condition that requires a decision: either train from scratch (no warm-start), or use a model already trained on 59 features as the base. The blueprint should state: "R2 failure on feature-count mismatch is expected at this stage. The lead-programmer should STOP and surface the feature schema decision to the orchestrator before training."

**R2 verdict**: Gate placement is correct. Two deficiencies: (1) wrong model name ("v8" should be "v9-baseline"), (2) no resolution path when the expected mismatch is found. Both need correction before programmer dispatch.

---

## Q3 — Are nits N1, N2, N3 properly incorporated?

### N1 (SPR regression assertion) — CORRECTLY INCORPORATED

The blueprint's Step 1 smoke test (Section Q6, test plan) includes:

> "N1 (nit): Zero Mode A records with `spr < 2.0` AND `pot_chips > 60`"

The assertion is specific and actionable. "Mode A records" is well-defined (generation_source == "self_play_v2"). The condition `spr < 2.0 AND pot_chips > 60` catches the unit-mismatch regression (a chip-unit pot of 60-120 should produce SPR 12.5+, not 1.25). **N1: PASS.**

One minor ambiguity: the smoke test records from Mode A (self-play) will not naturally contain `pot_chips` as a separate field — after conversion, only `pot` (in BB units) is stored in the record. The assertion should be phrased as: "Zero Mode A records where `pot_bb < 6.0` (i.e., pot_chips < 60 chips = less than 6 BB) AND `spr < 2.0`", since the converted `pot` field is in BB units. If the programmer implements the assertion as written with `pot_chips`, they will need to reconstruct the chip value from `pot_bb * BB_CHIP_SIZE`. A minor clarification.

### N2 (pairwise correlation check) — CORRECTLY INCORPORATED AS RISK 3 MITIGATION

The blueprint's Risk 3 section (Q8) states:

> "Additionally (ml-architect N2, nit): before mass generation, run a pairwise correlation check between `villain_air_pct`, `villain_top_pair_plus_pct`, `villain_draw_pct`, and `villain_aggression_count` across the factory pool. Compare to the same correlations in the self-play pool. Flag if any pairwise correlation differs by > 0.3."

This matches my original N2 specification exactly. The placement (as part of Risk 3 mitigation, before mass generation) is correct. **N2: PASS.**

### N3 (forbidden fingerprints incremental update) — CORRECTLY INCORPORATED

The blueprint's Q5 disjointness section and the `generate_corpus_revision_pool.py` interface (Section Q6) show the incremental threading pattern:

```python
fp_set = load_all_forbidden_fingerprints()
for generator_fn in [generate_pfa_scenarios, ..., generate_sb_hero_scenarios]:
    new_records = generator_fn(forbidden_fingerprints=fp_set)
    fp_set.update(fingerprint(r) for r in new_records)
    all_records.extend(new_records)
```

This matches my N3 specification. The pattern threads `fp_set` sequentially through all 9 scenario families. **N3: PASS.**

All three nits are properly incorporated. N1 has a minor field-naming clarification needed (see above).

---

## Q4 — Is OQ-5 (Phase B at 45 vs Phase A at 355) a real concern?

### What Phase A and Phase B actually represent

Phase A is the **mandatory quota allocation**: 355 hands that MUST appear in the corpus to cover specific structural gaps (Rule 4 PFA c-bet, KB §1.7 NFD, MW-30 BAC, MW-33 RAISE, MW-50 FOLD, MAGG river, SPR buckets, Rule 11 boundary, Modules 8+9).

Phase B is the **stratified distributional fill**: the remaining 45 hands drawn from the general pool to broaden distributional coverage across the 8-dimension stratification space.

OQ-5 is not a misnumbering. The architect correctly identifies that Phase B dropping from 90 to 45 hands (due to Modules 8+9 consuming 45 Phase A slots) raises a question about adequacy.

### Is 45 Phase B hands adequate?

**The honest ML answer**: 45 hands is marginally adequate for its purpose, but the reduction from 90 to 45 does measurably increase corpus skew toward curated scenarios.

The proportional breakdown:
- Original design: Phase A 310/400 = 77.5% mandatory + Phase B 90/400 = 22.5% distributional
- New design: Phase A 355/400 = **88.75% mandatory** + Phase B 45/400 = **11.25% distributional**

The corpus at 88.75% mandatory-pattern coverage is heavily curated. The model will train almost entirely on structured scenarios rather than organic poker situations. This is an acceptable tradeoff for a first-generation corpus specifically designed to fill structural gaps, but it should be flagged explicitly in the lock file and noted in the training plan.

**The 45-hand Phase B cannot meaningfully sample from 2592+ cells** (the blueprint's claimed cell count). At 45 hands / 1296 6-dimension cells, coverage is 3.5% of cells. Phase B's actual function is not stratified coverage — it is a diversity top-up to prevent the corpus from being 100% factory-constructed. At 45 hands it still accomplishes this minimum purpose.

**Is OQ-5 a real concern?** Yes, but it is not a design flaw. The correct response is:
1. Accept the 355/45 split as designed.
2. Note in the lock file that Phase B is a diversity top-up, not exhaustive stratification.
3. After corpus generation, inspect Phase B hands' distribution by dimension and note if any cell is pathologically underrepresented.
4. Flag as a v2.3 corpus expansion candidate: increase Phase B to 90+ by reducing factory pool overgeneration ratios.

The blueprint's OQ-5 disposition ("proceed with 355/45 and flag if structural verification gate fails") is the correct quality-first default. **OQ-5 is a real concern, correctly handled by proceeding and monitoring.**

---

## Q5 — Are Module 8 (donk-bet defence) and Module 9 (SB sandwich) ML-feasible?

### Module 8 (donk-bet defence): ~25 corpus hands — MARGINAL but acceptable

IP-facing-donk decisions with CALL/RAISE/FOLD outcomes across ~25 hands. Expected label split (based on blueprint's donk range polarisation description): approximately 10 CALL / 8 FOLD / 7 RAISE.

From an ML standpoint: 25 hands is below my 50-hand class-learnability floor from the original audit. However, Module 8 is not introducing a new action class — it contributes to the existing CALL/RAISE/FOLD distributions in the combined corpus. Its purpose is **structural diversity** (IP-facing-OOP-donk is a distinct facing-bet subtype that v3.2 has no explicit rule for), not class isolation.

The model will not reliably learn "donk-bet defence" as a separable pattern from 25 hands. But those 25 hands add IP-perspective facing-bet variance, which broadens the CALL/FOLD/RAISE training signal beyond the other modules' OOP or symmetric scenarios. **MARGINAL — acceptable as diversity signal, not class isolation.**

### Module 9 (SB-as-hero): ~20 corpus hands — BELOW MINIMUM for position-specific learning

OOP SB hands with tighter MDF decisions across ~20 hands. Expected label split: approximately 12 FOLD / 6 CALL / 2 RAISE (tight SB ~20% MDF vs BB ~33% MDF).

20 hands is insufficient to teach the model SB-specific behavioral differences from BB. The `hero_position` feature is a categorical variable encoding 6 positions (UTG/HJ/CO/BTN/SB/BB). Distinguishing SB from BB behavior through position-specific interaction requires roughly 30-50 examples per position with varied hand classes and boards. 20 examples is **token coverage**: the model will see SB as a position but will not reliably generalize SB-specific fold rates.

This is honestly stated as "token coverage" — 20 hands cannot teach a model that SB folds more than BB to the same c-bet, given that the overall FOLD class has 48+ examples and the position information has low per-position sample density.

**NOT blocking**: The synthesis correctly identified this as a MEDIUM-severity pattern gap. Adding 20 SB examples is better than adding 0. The limitation should be documented: Module 9 provides SB representation in the corpus but does not provide sufficient signal for the model to learn SB-specific fold thresholds. This is a known limitation to address in v2.3 corpus expansion.

**Module 9 recommendation**: If feasible within pool generation budget, increase to 30-35 SB hands. This brings it above the marginal threshold while staying within the compute envelope. Not a blueprint-blocking change — note it as a programmer-discretion expansion if the pool yields allow.

---

## Q6 — Final verdict on blueprint v2

**Verdict: APPROVE-WITH-NITS**

The five required fixes from R1 are incorporated correctly. The three nits are incorporated correctly. The two new scope modules are specified with reasonable completeness. The blueprint is ready for programmer dispatch with the following corrections made before the programmer starts.

### Corrections required before programmer dispatch (not blocking blueprint, but must be addressed in code implementation)

**C1 (PROGRAMMER-BLOCKING NIT): R2 script references wrong warm-start base model.**

Section Q6, `scripts/verify_feature_schema_compatibility.py`, CLI example:
```bash
# WRONG in blueprint:
--model river-rats-core/models/v8_oracle.json

# CORRECT:
--model river-rats-core/models/gto_model_v9_baseline_45feat.json
```

The programmer must use the v9-baseline model, not v8. Using v8 will compare the wrong feature schema (38 HU features vs 59 3-way features) and produce a misleading diagnostic.

**C2 (PROGRAMMER-BLOCKING NIT): R2 resolution path is missing.**

R2 WILL find a mismatch (v9-baseline: 45 features vs new corpus: 59 features). The blueprint's instruction is "STOP and report BLOCKED" — but the mismatch is known and expected. The programmer should understand:

> "A feature-count mismatch between v9-baseline (45 features) and the new corpus (59 features) is EXPECTED and does not mean the corpus is wrong. It means warm-start from v9-baseline is not viable for the 59-feature schema expansion. When R2 fails, the programmer surfaces this to the orchestrator with the specific diff. Do NOT attempt warm-start training with mismatched schemas; also do NOT discard the corpus. The resolution (train from scratch, or identify a 59-feature base model if one exists) is an orchestrator decision."

**C3 (NIT): R1 re-extraction algorithm needs 3-bet pot guard.**

The blueprint's re-extraction algorithm (Section Q6, script 2, step 2) says: "The opener is the first player who made a preflop bet (raise). If `prior_actions` does not contain preflop action, `_opener_position` remains None."

This is incomplete. The algorithm will incorrectly flag 3 SB hands (`is_3bet_pot=1`, pot=855 chips) as `is_preflop_aggressor=1`. The programmer should add:

```python
# Guard for 3-bet pots: if hero raised preflop but the hand is a 3-bet pot,
# hero is the 3-bettor (not the opener). Original opener is unknown from prior_actions.
original_feat = record.get('feat_dict', {})
if original_feat.get('is_3bet_pot', 0) and hero_pos == 'SB':
    _opener_position = None  # hero is 3-bettor, not original opener
```

Three records affected. Not blocking.

**C4 (NIT): N1 smoke test assertion needs field clarification.**

The smoke test assertion reads: "Zero Mode A records with `spr < 2.0` AND `pot_chips > 60`". After the pot-to-BB conversion, Mode A records store pot in BB units (`pot_bb`), not chip units. The assertion should read:

> "Zero Mode A records where `spr < 2.0` AND `pot_bb > 6.0`" (6 BB = 60 chips / BB_CHIP_SIZE=10)

This is the equivalent regression check and uses the field name that actually exists in the record.

### Positive confirmations

- Root cause 1 diagnosis and fix path: VERIFIED CORRECT against source
- Root cause 2 diagnosis and fix path: VERIFIED CORRECT against source
- BB_CHIP_SIZE=10 constant: VERIFIED CORRECT (poker_game.py BIG_BLIND=10)
- Labels untouched: VERIFIED (labels stored by source_situation_id, separate from feat_dict, 500 total)
- R3 MAGG fix (river decision point, villain_aggression_count=2): CORRECTLY SPECIFIED
- R4 NFD boundary validation (±0.03 tolerance): CORRECTLY PLACED in corpus assembly Phase A loop
- R5 Rule 11 boundary texture variation (≥3 textures, 5 pairs): CORRECTLY SPECIFIED with GTO rationale
- N1, N2, N3 nits: INCORPORATED (with field-naming clarification for N1)
- OQ-5 disposition (proceed with 355/45, monitor): ACCEPTABLE quality-first default
- Module 8/9 ML feasibility: MARGINAL to TOKEN COVERAGE — expected and documented

### What to note for the training plan

The following items are out of scope for this corpus-generation blueprint but must be carried into the training plan:

1. The R2 mismatch (45-feature base vs 59-feature corpus) requires a decision on warm-start vs train-from-scratch. Orchestrator must gate this explicitly.
2. The combined corpus is 88.75% mandatory-pattern (Phase A) — the training plan should note this and assess if phase-B distributional fill at 45 hands is sufficient before first training run.
3. Module 9 SB representation is token coverage (20 hands). The training plan should not claim SB-specific MDF calibration from this corpus version.

---

## Summary table

| Item | Blueprint v2 claim | Verification | Assessment |
|---|---|---|---|
| OQ-4: prior_actions includes preflop | Flagged as uncertain | CONFIRMED (100/100 records) | RESOLVED — not blocking |
| OQ-4: reconstruction correct (97/100) | Not fully worked out | CONFIRMED via live inspection | Algorithm documented above |
| OQ-4: 3-bet SB edge case (3/100) | Not flagged | FOUND | NIT — add is_3bet_pot guard |
| BB_CHIP_SIZE=10 | Asserted | CONFIRMED (poker_game.py BIG_BLIND=10) | CORRECT |
| Labels at 4bce49f untouched | Asserted | CONFIRMED (keyed by source_situation_id) | CORRECT |
| R2 gate placement | Before training kickoff | CORRECT | PASS |
| R2 model name ("v8 oracle") | Wrong model referenced | CONFIRMED error | C1 — programmer-blocking NIT |
| R2 resolution path | Missing | CONFIRMED missing | C2 — add to spec |
| N1 SPR regression assertion | Incorporated in smoke test | CORRECT with field-name clarification | C4 (minor) |
| N2 correlation check | Risk 3 mitigation | CORRECTLY INCORPORATED | PASS |
| N3 incremental fingerprints | Q5 + generate_scenarios() | CORRECTLY INCORPORATED | PASS |
| OQ-5 (Phase B 45 vs 90) | Real concern, proceed+monitor | CONFIRMED — real but acceptable | PASS with documentation |
| Module 8 (25 hands) | MEDIUM — adopt | Marginal ML signal | Acceptable as diversity |
| Module 9 (20 hands) | MEDIUM — adopt | Token coverage | Acceptable with documented limitation |

**Blueprint v2 is substantially correct. Four programmer nits require attention before implementation begins (C1 is the most important — wrong model name will break R2). No structural design issues remain. All required fixes from R1 are verified incorporated.**

---

*Review complete. No code written. No blueprint modified. No files staged for commit.*
