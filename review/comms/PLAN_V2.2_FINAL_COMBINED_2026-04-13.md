---
date: 2026-04-13
from: Builder team
to: Owner (Rupert)
re: v2.2 FINAL COMBINED PLAN — reconstruction + bucket-first relabel + retrain
status: FOR OWNER REVIEW — nothing proceeds without approval
supersedes:
  - PLAN_V2.2_RETRAIN_2026-04-13.md
  - PLAN_V2.2_FULL_REBUILD_2026-04-13.md
  - EXPERT_PANEL_RECONSTRUCT_VS_REGENERATE_2026-04-13.md
  - BUILDER_RESPONSE_HAND_BUCKET_LABELLING_2026-04-13.md
incorporates:
  - Owner feedback on expert panel (bucket thresholds, SUSPECT
    category, AMBIGUOUS decision rule, allocation sequencing,
    feature diff gate, per-situation comparison format)
---

# v2.2 Final Combined Plan

## 0. What this plan does

1. Hardens the pipeline so no situation without a validated
   action sequence can enter any downstream step
2. Reconstructs sequences for the 200 self-play 3-way situations,
   preserving same cards/board/positions
3. Discards the 151 factory 2-way situations (heads-up spots —
   no sandwich pressure, actively harmful for 3-way training)
4. Re-extracts features from reconstructed sequences to verify
   integrity and populate the 3 NULL features
5. Designs new situation allocation AFTER reconstruction results
   show what survived and what gaps remain
6. Relabels everything with bucket-first reasoning (no thresholds
   in the labelling prompt — poker reasoning and examples only)
7. Compares old vs new labels per-situation on the reconstructed
   200 as a safety net
8. Trains v2.2 from scratch on clean, validated, bucket-first data

~75-85 agents. ~7-8 sessions. 7 owner gates.

---

## Phase 0: Pipeline Hardening (BLOCKER)

Nothing else starts until this is done and approved.

| Step | What | Who | Gate |
|---|---|---|---|
| 0.1 | Add `action_string` as mandatory field in situation JSONL schema. Update `situation_factory.py` to emit it. Update all JSONL writers. | Architect → Programmer | Schema documented, factory emits field |
| 0.2 | Add validator gate to `feature_extractor.py`. Before extracting features, run `validate_action_string()`. Reject with clear error on failure. No silent pass-through. | Architect → Programmer | Gate integrated, test written |
| 0.3 | Add validator gate to CSV export pipeline. Validate source action string before writing any row. Reject invalid. | Architect → Programmer | Gate integrated, test written |
| 0.4 | Add validator gate to labelling agent input. Every situation brief includes the validated action string. Agent reasons about action history from it. | Architect → Programmer | Labelling input format documented |
| 0.5 | Add `action_string` to both test set JSONL schemas (reference + facing-bet). | Architect → Programmer | Both test sets carry action strings |
| 0.6 | Run validator on facing-bet test set (40 hands). Re-add action strings from PHASE1_GATE_VALIDATION. Re-validate. Failures = fix or remove. | Programmer | 40/40 pass or failures documented |
| 0.7 | Run validator on reference set (MW-11–50). Same treatment. | Programmer | All pass or failures documented |

**Gate 1: Owner reviews Phase 0 deliverables.**

---

## Phase 1: Reconstruct + Verify Existing 200

### Phase 1A: Build sequence reconstruction tool

**Who:** Architect (design) → Programmer (build + test)

The tool takes a self-play situation record and produces all valid
action sequences consistent with its feature values.

**Inputs per situation:**
- `prior_actions` (hero-only free-text, e.g. `["flop: CO check"]`)
- `hero_position`, `villain_positions` → position order
- `facing_bet`, `facing_raise` → what hero faces
- `villain_aggression_count`, `villain_checked_back`,
  `villain_call_count`, `num_callers_to_bet` → counter constraints
- `pot`, `to_call`, `bet_to_pot` → sizing constraints

**AMBIGUOUS decision rule (owner directive):** When multiple valid
sequences exist, prefer the sequence whose hero actions match
`prior_actions` first. If multiple sequences still tie after
matching hero actions, select the simplest (fewest total actions).
Tag as AMBIGUOUS regardless — the labelling agent sees the selected
sequence but the tag flags it for review.

**Output per situation — one of four classifications:**

| Classification | Meaning | Action |
|---|---|---|
| **CERTAIN** | Exactly 1 valid sequence produces the observed features | Attach sequence. Proceed to re-extraction. |
| **AMBIGUOUS** | Multiple valid sequences, all consistent with features | Select per decision rule above. Proceed to re-extraction. Flag for review. |
| **CORRUPT** | Zero valid sequences produce the observed features | Features are impossible under any legal action order. **Exclude from training.** Replace in Phase 2 — attempt same cards/board through factory first, fall back to new situations if factory can't produce a valid 3-way with those cards. |
| **SUSPECT** | Reconstruction says CERTAIN or AMBIGUOUS, but re-extracted features don't match originals (see Phase 1C) | Sequence was probably wrong in the original data. **Exclude from training.** Replace in Phase 2 — same replacement policy as CORRUPT (attempt same cards/board first). |

**Tests required:**
- Unit tests: known valid, known ambiguous, known corrupt 3-way
- Self-consistency: for CERTAIN/AMBIGUOUS results, re-extract
  features and confirm they match originals (this is what surfaces
  SUSPECT situations)

**Gate 2: Owner reviews reconstruction tool design before it runs
on the full dataset.**

### Phase 1B: Run reconstruction on all 200 self-play situations

**Who:** Programmer

Batch run. Output: classification report per situation.

```
situation_id | classification | num_valid_sequences | selected_sequence | notes
d0244_CO_river | CERTAIN | 1 | "BB check, CO check, BTN bet 60, BB call 60, CO ???" | —
d1200_HJ_turn | AMBIGUOUS | 3 | "BB check, HJ check, BTN bet 45, BB fold, HJ ???" | selected: matches prior_actions
...
```

### Phase 1C: Re-extract features + feature diff report

**Who:** Programmer

For every CERTAIN and AMBIGUOUS situation:
1. Run the feature extractor using the reconstructed action string
2. Compare all 48 features against the original stored values
3. Flag any situation where the diff exceeds tolerance:
   - Integer features: exact match required
   - Float features: tolerance ±0.01
   - NULL→value: expected (the 3 formerly-NULL features)

**Feature diff report format:**

```
situation_id | classification | features_matched | features_differed | NULL_populated | verdict
d0244_CO_river | CERTAIN | 45/45 | 0 | 3 (flush_block, flush_draw, hero_range) | PASS
d1200_HJ_turn | CERTAIN | 42/45 | 3 (facing_bet, villain_agg, pot_odds) | 3 | → SUSPECT
```

Any situation where non-NULL features differ → reclassify as
**SUSPECT**. This is where sequence corruption actually shows up
in the data — the re-extraction proves the original features were
computed from a different (probably invalid) sequence.

**Gate 3: Owner reviews feature diff report.** This gate tells you
how much sequence corruption actually mattered. If 190/200 pass,
the problem was small. If 120/200 pass, the problem was systemic.
This informs Phase 2 allocation decisions.

### Phase 1 summary output

| Category | Expected count | Enters training? |
|----------|---------------|-----------------|
| CERTAIN + features match | ~140-160 | Yes |
| AMBIGUOUS + features match | ~20-30 | Yes (flagged) |
| CORRUPT | ~10-20 | No — replaced in Phase 2 |
| SUSPECT | ~5-15 | No — replaced in Phase 2 |
| Factory 2-way (discarded) | 151 | No — not 3-way |

**Surviving situations carry:** original hero cards, original
board, original positions, validated action string, re-extracted
48 features (including formerly-NULL), old label for comparison.

---

## Phase 2: Design + Generate New Situations

**This phase starts AFTER Gate 3** — because the allocation must
account for what survived reconstruction.

### Phase 2A: Situation allocation design

**Who:** GTO Expert + ML Architect

**Inputs:**
- Reconstruction results: how many survived, what action/street/
  position distribution remains
- Gaps to fill: whatever the surviving situations don't cover
- Mandatory additions: BP7 non-monster RAISE situations (15-20)
- Target total: ~400-470 training situations

**The allocation table covers:**
- Action balance (target: not more than 35% any single action)
- Street coverage (flop/turn/river, weighted by frequency)
- Position coverage (all 3 hero positions: BB, CO/HJ, BTN)
- Board texture diversity (dry, wet, monotone, paired, connected)
- Facing-bet vs not-facing-bet balance (~40/60 split)
- RAISE situations with counterexamples (per retirement doc BP7)

**Gate 4: Owner reviews allocation table before generation.**

### Phase 2B: Generate new situations

**Who:** Programmer

All situations through hardened pipeline:
- `situation_factory.py` emits `action_string`
- `hand_sequence_validator` gates every situation
- `feature_extractor.py` extracts full 48 features
- Zero NULLs in any feature column

**Gate:** 100% validator pass. Zero NULLs report.

---

## Phase 3: Relabel Everything Bucket-First

### Phase 3A: Update labelling prompt

**Who:** Architect

Replace the reasoning protocol in `gto_labeller_v1.md` with
bucket-first structure. **Critical owner directive: NO equity
thresholds in the labelling prompt.** The thresholds (0.80
monster, 0.55 strong, etc.) belong in `spot_classifier.py` for
deterministic teaching classification. The labelling prompt uses
poker reasoning and examples.

**Updated reasoning protocol:**

```
For each hand, follow this sequence:

1. CLASSIFY THE HAND.
   Before considering any action, determine what kind of hand
   this is. Use poker reasoning, not numeric thresholds.

   Ask yourself:
   - Is this a monster? (Sets, straights, flushes, full houses.
     Hands that are almost never behind.)
   - Is this a strong made hand? (Top pair top kicker, overpair
     on a dry board. Hands that beat most of villain's range
     but can be outdrawn.)
   - Is this a medium made hand? (Top pair weak kicker, second
     pair, pocket pair below top card. Ahead of some hands,
     behind others.)
   - Is this a weak made hand? (Bottom pair, third pair. Rarely
     best but technically made.)
   - Is this a drawing hand? (Flush draws, straight draws, combo
     draws. Not currently made but significant equity.)
   - Is this air? (No made hand, no meaningful draw. Equity comes
     only from fold equity or runner-runner.)

   State the bucket explicitly: "This is a [bucket] hand."

   Examples of each bucket in 3-way:
   - Monster: Hero holds 8h8c on board 8d 5s 2c. Flopped set.
   - Strong made: Hero holds AhKd on board Ad 9c 3h. TPTK on
     dry rainbow.
   - Medium made: Hero holds KhJd on board Kc 8s 5d. Top pair
     but vulnerable kicker 3-way.
   - Drawing: Hero holds Th9h on board 7h 6h 2c. Flush draw
     with straight draw (combo draw).
   - Air: Hero holds Qc Jd on board 8s 5d 2c. Two overcards,
     no draw, no made hand.

2. READ THE SITUATION.
   What context shapes the decision?
   - Position: IP, OOP, or sandwich?
   - Board: static or dynamic? Who does it favour?
   - Villain ranges: composition triple (TP+/draws/air)
   - Action history: bet-and-call, check-raise, multi-street
     aggression? What does the action tell you about villain
     ranges that the preflop ranges don't?
   - SPR: committed (< 2), standard (2-6), deep (> 6)?

3. CONSIDER ALL ACTIONS.
   For this hand type in this situation, evaluate every legal
   action. For each, name the strategic role:
   - BET/RAISE with monster/strong → value
   - BET/RAISE with drawing → semi-bluff (requires nut draw
     + blocker 3-way, per KB Section 1.7)
   - CHECK with strong on safe board → trap or pot control
   - CALL with drawing hand getting right price → drawing call
   - FOLD with medium hand when action narrows ranges above
     you → range fold

   No action is the default. Each must earn its place.

4. CHOOSE AND VERIFY.
   Select the action with the strongest case. Then verify:
   "You have a [bucket] hand. The correct play is [action]
   because [strategic role] given [key situation factor]."
   If this sentence doesn't sound like a poker coach
   explaining the play, reconsider.
```

**Also update:**
- MW-30 calibration note: FOLD → CALL (solver-corrected)
- Factor 3: demote `villain_range_capped` to preflop structural
  label per KB v1.3 Section 1.9

**Gate 5: Owner reviews updated prompt before calibration.**

### Phase 3B: Calibration

**Who:** 1 GTO Expert (examiner) + 1 Grader

One agent takes the 24-question blind exam using the updated
prompt + KB v1.3. Gate: 20/24 minimum + all 3 GTO-reversal hands
correct.

**Verified GTO-reversal hands (from calibration_exam.py and
calibration_answers_batch_3.md):**
- MW-30: **CALL** (solver-corrected — equity surplus too large
  for fold despite bet-and-call signal)
- MW-33: **RAISE** (set must raise vs bet+call)
- MW-50: **FOLD** (BTN raised flop, range narrowed)

Note: the labelling prompt line 270 still lists MW-30 as FOLD —
this is fixed in Phase 3A. The calibration exam code
(`calibration_exam.py`) already has MW-30 as CALL in the answer
key. MW-46/MW-47 from the reference corrections memory are
reference set labels, not calibration reversal hands.

### Phase 3C: Labelling

**Who:** ≤10 situations per GTO Expert agent. Agents assigned by
tactical theme, not by number.

Each agent receives:
- Situation data including validated `action_string`
- Full 48-feature vector
- KB v1.3
- Updated labelling prompt (bucket-first, no thresholds)

Each agent outputs:
```json
{
  "situation_id": "...",
  "hand_bucket": "drawing",
  "action": "RAISE",
  "strategic_role": "semi_bluff",
  "confidence": "HIGH",
  "reasoning": "...",
  "alternatives_considered": ["CALL: rejected because..."],
  "difficulty": 2
}
```

Note: `hand_bucket` is now a required output field. This enables
the per-situation comparison and ensures the agent actually
classified the hand first.

### Phase 3D: Independent review

**Who:** ≥ labeller count ÷ 2 reviewer agents. ≤15 situations each.

Reviewer checklist:
- Did the agent classify the hand bucket FIRST, before
  considering actions?
- Is the bucket classification reasonable? (Not using thresholds
  — using poker reasoning about what the hand IS)
- Does the action follow from (bucket + situation)?
- KB v1.3 consistency
- Action string coherence (action matches what's legal given the
  sequence)
- Vocabulary (no BET when facing_bet=1, no RAISE when
  facing_bet=0)

### Phase 3E: Per-situation comparison report (200 reconstructed)

**Who:** Programmer (automated) + Owner (review)

For each of the ~160-190 surviving reconstructed situations,
produce a per-situation comparison row:

```
situation_id | hand_bucket | old_label | new_label | agree? | old_reasoning_summary | new_reasoning_summary | flag
d0244_CO_river | medium_made | CALL | FOLD | NO | "equity 48% > pot odds" | "medium made facing multi-street agg, range above us" | CALL_DISAGREE
d1971_BTN_river | air | FOLD | FOLD | YES | — | — | —
```

**Disagreement escalation thresholds:**

| Disagreement type | Threshold | Escalation |
|---|---|---|
| CALL→RAISE or RAISE→CALL | Any | Solver verification mandatory |
| CALL→FOLD or FOLD→CALL | Any where equity > 0.30 | Solver verification mandatory |
| CHECK→BET or BET→CHECK | >10% of not-facing-bet situations | Review bucket classifications for systematic bias |
| Overall disagreement rate | >25% | STOP. Review bucket-first prompt for over-correction before continuing. Owner gate. |
| Overall disagreement rate | ≤15% | Proceed with confidence. Disagreements are edge cases. |
| Overall disagreement rate | 15-25% | Proceed but flag all disagreements for solver verification. |

**Solver verification triggers (owner runs in GTO Wizard):**
- All non-monster RAISE labels
- All CALL-disagreements where old label was FOLD (or vice versa)
  with equity 0.25-0.45 (the marginal zone)
- All BET labels with equity < 0.50 on non-monster hands
- Pre-flight mandatory: sequences validated AND sizing matches
  solver options EXACTLY

**Gate 6: Owner reviews comparison report + solver results.**

---

## Phase 4: Train v2.2

| Step | What | Who | Gate |
|---|---|---|---|
| 4.1 | Leakage check against both test sets + internal dedup | Programmer | Zero leakage |
| 4.2 | ML architect designs training config (from-scratch XGBoost, 800 rounds, max_depth=5, lr=0.05, class weights: BET≤2.0, RAISE≤3.0, 5-fold stratified CV, villain_range_capped ablation) | ML Architect | Config reviewed |
| 4.3 | Export validated training CSV. Every row has: validated action_string (metadata), 48 non-NULL features, bucket-first label. | Programmer | Export audit |
| 4.4 | Train model. Report: CV scores, feature importance, per-class metrics. | Programmer | Training report |
| 4.5 | Evaluate on both test sets. Side-by-side with v2.1. Per-class breakdown including RAISE accuracy. | Programmer + Reviewer | Evaluation report |

**Gate 7: Owner reviews training + evaluation. Ship or iterate.**

---

## Phase 5: Post-Ship Alignment

| Step | What | Who |
|---|---|---|
| 5.1 | Notify teaching team: new model, updated features, RAISE rate, action distribution changes | Builder → Teaching |
| 5.2 | Teaching L3 review against new model (non-monster RAISE predictions appear for first time) | Teaching team |
| 5.3 | Update river-rats-core/ with approved model, updated prompts, hardened pipeline, and reconstruction tool (permanent pipeline tool alongside hand_sequence_validator.py) | Programmer |

---

## Success Criteria

v2.2 ships if ALL of:

| # | Criterion | Threshold |
|---|---|---|
| 1 | Every training situation has a validated action string | 100% |
| 2 | Every training row has all 48 features non-NULL | 100% |
| 3 | Every label produced via bucket-first protocol | Verified by reviewers |
| 4 | Reference set accuracy | ≥ 82.5% (no regression) |
| 5 | Facing-bet set accuracy | ≥ 70.0% overall |
| 6 | Facing-bet CALL accuracy | ≥ 55% |
| 7 | Facing-bet RAISE accuracy | ≥ 56% (baseline), target 67%+ |
| 8 | 5-fold CV accuracy | No drop > 3pp from v2.1 |
| 9 | No single feature above 30% importance | Verified |
| 10 | Zero leakage against either test set | Verified |

---

## Owner Gates (7 total)

| Gate | When | What owner reviews |
|---|---|---|
| **Gate 1** | After Phase 0 | Pipeline hardening: action_string mandatory everywhere, validator gates integrated, test sets validated |
| **Gate 2** | After Phase 1A | Reconstruction tool design: logic, tests, AMBIGUOUS decision rule, SUSPECT classification |
| **Gate 3** | After Phase 1C | Feature diff report: how many CERTAIN/AMBIGUOUS/CORRUPT/SUSPECT. Shows whether sequence corruption was systematic or isolated. Informs Phase 2 allocation. |
| **Gate 4** | After Phase 2A | Situation allocation table: action/street/position/texture coverage, designed around what survived reconstruction |
| **Gate 5** | After Phase 3A | Updated labelling prompt: bucket-first with poker reasoning (no thresholds), MW-30 fix, villain_range_capped demotion |
| **Gate 6** | After Phase 3E | Per-situation comparison report + solver verification results. Disagreement escalation applied. |
| **Gate 7** | After Phase 4.5 | Training + evaluation results. Ship or iterate. |

---

## Resource Summary

| Phase | Agents | Notes |
|---|---|---|
| Phase 0: Pipeline hardening | 1 Architect + 1 Programmer | Sequential. BLOCKER. |
| Phase 1A: Reconstruction tool | 1 Architect + 1 Programmer | Design + build + test |
| Phase 1B-C: Run + feature diff | 1 Programmer | Batch jobs |
| Phase 2A: Allocation design | 1 GTO Expert + 1 ML Architect | After Gate 3 |
| Phase 2B: Generate situations | 1 Programmer | Through hardened pipeline |
| Phase 3A: Prompt update | 1 Architect | Bucket-first, no thresholds |
| Phase 3B: Calibration | 1 GTO Expert + 1 Grader | 20/24 gate |
| Phase 3C: Labelling | ~40-47 GTO Experts | ≤10 per agent, parallel |
| Phase 3D: Review | ~20-24 Reviewers | ≤15 per agent, parallel |
| Phase 3E: Comparison + solver | 1 Programmer + Owner | Automated report + GTO Wizard |
| Phase 4: Train + evaluate | 1 ML Architect + 1 Programmer + 1 Reviewer | Sequential |
| Phase 5: Post-ship | Teaching team + 1 Programmer | After ship |
| **Total** | **~75-85 agents + 7 owner gates** | |

---

## Session Estimate

| Session | Work | Commit at end |
|---|---|---|
| 1 | Phase 0 (pipeline hardening) → **Gate 1** | Hardened pipeline code |
| 2 | Phase 1A (reconstruction tool design + build) → **Gate 2** | Reconstruction tool + tests |
| 3 | Phase 1B-C (run reconstruction + feature diff) → **Gate 3** | Classification + diff reports |
| 4 | Phase 2 (allocation design + generation) → **Gate 4** | New situations JSONL |
| 5 | Phase 3A-B (prompt update + calibration) → **Gate 5** | Updated labelling prompt |
| 6 | Phase 3C-D (labelling + review, parallel) | All labels + review reports |
| 7 | Phase 3E (comparison report + solver) → **Gate 6** | Comparison report + solver results |
| 8 | Phase 4 (train + evaluate) → **Gate 7** | Model + training report |

~7-8 sessions. Could compress if phases within a session
complete quickly.

**Owner directive: commit all work at end of each session** in
case of power failure. Each session's commit should be
self-contained — if the next session never starts, the prior
session's work is preserved and resumable.

**Session 6 note:** This is the heaviest session (~60-70 parallel
agents: ~47 labellers + ~24 reviewers). Labellers and reviewers
run sequentially (reviewers need labeller output), so this may
naturally split into two sub-sessions: 6a (labelling, parallel)
and 6b (review, parallel). Both committed separately.

---

## Risk Register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Reconstruction shows most situations are CORRUPT/SUSPECT | Medium | Gate 3 catches this early. If <100 survive, shift to full regeneration for those slots. Allocation design in Phase 2 adapts. |
| Bucket-first prompt produces aggressive bias (over-RAISE/BET) | Medium | No thresholds in prompt prevents mechanical triggering. Calibration gate 20/24. KB v1.3 defaults are conservative. Comparison report at Gate 6 catches it. |
| Disagreement rate >25% triggers stop | Low-Medium | If triggered, review prompt for systematic over-correction before continuing. Owner decides whether to adjust prompt or accept higher disagreement. |
| New situations don't cover same tactical space as old 200 | Medium | Allocation designed AFTER reconstruction results (Gate 4). GTO Expert + ML Architect design coverage together. |
| 2-way discard loses useful data | Low | GTO Expert confirmed: 2-way spots are actively harmful for 3-way training. No sandwich dynamics. Not a loss. |
| Feature diff reveals widespread corruption | Medium | That's the point of Gate 3. If corruption is widespread, it validates the decision to rebuild. If isolated, it builds confidence in the surviving data. |

---

## What This Plan Supersedes

- `PLAN_V2.2_RETRAIN_2026-04-13.md`
- `PLAN_V2.2_FULL_REBUILD_2026-04-13.md`
- `EXPERT_PANEL_RECONSTRUCT_VS_REGENERATE_2026-04-13.md`
- `BUILDER_RESPONSE_HAND_BUCKET_LABELLING_2026-04-13.md`
- RAISE tree retirement Section 4 builder actions

## What This Plan Does NOT Change

- KB v1.3 (no changes)
- Facing-bet test set labels (already shipped, solver-verified)
- Reference set labels (already corrected)
- Teaching system code (spot_classifier.py keeps its thresholds)
- Calibration exam design (20/24 gate, 3 GTO-reversals)

---

**Awaiting approval. On "go" the architect starts Phase 0.1.**
