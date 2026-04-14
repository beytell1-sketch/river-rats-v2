# Restart Prompt — Pass 1 Production Labelling

## Project

River Rats v2 — GTO poker coaching oracle. XGBoost 5-class model
(FOLD/CHECK/CALL/BET/RAISE), 54 features, 3-way postflop.

## Working directory

`/home/rupertbeytell/river-rats-v2`

## What just happened

All prerequisites are complete:
- Phase 3A: features 49-54 promoted, v2 prompt with bucket-first reasoning
- Phase 3B: calibration 20/24 + 3/3 reversals PASSED
- Pilot v1: 6-team structure validated (19/20 unanimous)
- Pilot v2: CONFIRMED tier + mandatory composition validated (18/20 unanimous)
- Feature attention experiments: all 4 passed mechanically. Exp 3
  (auxiliary flags) chosen for production — 108 training columns
  (54 features + 54 binary attention flags)
- Owner issued Pass 1 GO directive

## What to do now — Pass 1 Execution

Label all 385 hands with 4 labelling teams (T1-T4) + 2 discovery
teams (T5-T6). Then build comparison report for owner review.

### Key files to read FIRST

1. `review/comms/OWNER_DIRECTIVE_PASS1_GO_2026-04-14.md` — THE
   directive. Team structure, agent allocation, comparison report
   format, Pass 2 design, vocabulary management, gates.
2. `prompts/gto_labeller_v2.md` — the labelling prompt (bucket-first
   + enriched output + CONFIRMED tier + mandatory composition +
   bucket-specific features + action-dependent defaults)
3. `knowledge/three_way_gto.md` — the KB v1.3
4. `training-data/tag_vocabulary.json` — intention/street plan seeds
5. `review/comms/PLAN_PHASE3_FINAL_2026-04-13.md` — the approved
   Phase 3 plan (comparison report format, Pass 2 escalation)
6. `CLAUDE.md` — mandatory protocols
7. `docs/PROCESS_GUIDE.md` — team protocols, quality gates

### The 385 training situations

Two sources:
- `training-data/3way_selected_200.jsonl` — 200 reconstructed
  self-play situations (45 features — need re-extraction to 54)
- `training-data/factory_batch5_situations.jsonl` — 185 factory
  situations (54 features)

**IMPORTANT:** The 200 reconstructed situations have only 45
features. They must be re-extracted with the 54-feature pipeline
before labelling. The pilot did this for 10 hands using
`feature_extractor.extract_all_features()` — the same approach
must be applied to all 200. See the pilot session for the exact
re-extraction code pattern.

### Situation preparation

1. Re-extract all 200 reconstructed hands with 54 features
2. Combine with 185 factory hands into a single 385-hand file
3. Format as situation text blocks (same format as calibration
   exam and pilot — situation_id, hero cards, board, street,
   position, action history, full 54-feature vector)
4. Write to `/tmp/pass1_situations.json`

### Team structure

| Team | Role | Approach | Agent-calls |
|------|------|----------|-------------|
| T1 | Labelling | Approach C amended | 39 |
| T2 | Labelling | Approach C amended | 39 |
| T3 | Labelling | Approach C amended | 39 |
| T4 | Labelling | Approach C amended | 39 |
| T5 | Discovery | Bottom-up scan | 39 |
| T6 | Discovery | Bottom-up scan | 39 |

- Each labelling team gets all 385 hands in a different random
  order (4 different seeds)
- Each agent gets ≤10 hands (Process Guide §1.1)
- 39 batches per team × 4 teams = 156 labelling agent-calls
- T5-T6 run AFTER T1-T4 comparison report is built

### Labelling agent prompt

Each labelling agent receives:
- The v2 labelling prompt (gto_labeller_v2.md)
- The KB (knowledge/three_way_gto.md)
- Tag vocabulary (tag_vocabulary.json)
- Approach C feature attention instructions with CONFIRMED tier
- Mandatory composition for BET/RAISE/CALL/FOLD
- Bucket-specific mandatory features
- 10 situation texts with full 54-feature vectors
- NO access to other teams' or agents' labels

### Discovery agent prompt

Each discovery agent receives:
- The KB
- 10 situations with consensus labels from T1-T4
- Bottom-up scan protocol (start feature 54, work up)
- Excluded features (already covered by T1-T4)

### Execution plan

**Phase 1: Prepare (1 step)**
1. Re-extract 200 reconstructed hands with 54 features
2. Combine all 385 into /tmp/pass1_situations.json
3. Create 4 random orderings (one per team)
4. Split into 39 batches of 10 per team
5. Write batch files to /tmp/pass1_T*_batch*.json

**Phase 2: T1-T4 labelling (4-5 sessions)**
Launch in waves due to agent limits:
- Wave 1: 6 agents (batch 1 of each team + 2 extra)
- Continue until all 156 agents complete
- Collect results into per-team JSONL files

**Phase 3: Build comparison report (0.5 session)**
- 4-team consensus per hand
- Action/difficulty/bucket agreement
- Intention and feature Jaccard scores
- CONFIDENT_SPLIT detection
- Old vs new label comparison (200 reconstructed)
- Present for Pass 1 gate owner review

**Phase 4: T5-T6 discovery (2 sessions)**
- After Pass 1 gate approval
- 78 discovery agents
- Build union + untagged features

**Phase 5: Pass 2 targeted review (2-3 sessions)**
- Based on Pass 1 gate decisions
- Expert panels for splits
- Solver verification for escalated hands

### Recent commits

```
66b6da8 Pass 1 GO directive: 385 hands, 4+2 teams, Exp 3 auxiliary flags
7e7fa9c Feature attention training experiments: all 4 pass mechanically
a0349ba Architect blueprint: feature attention training experiments
9fecff2 ML Architect plan: 4 feature attention training experiments
729dbbf Pilot v2 complete: 18/20 unanimous, full union + untagged report
95c34ae Pilot v2 rerun: prompt updated, 12 agents complete, results pending report
2a08cfd Pilot complete: 19/20 unanimous across 6 teams, 3 approaches
a8335b4 Phase 3B: calibration exam passed — 20/24 + 3/3 reversals
```

### Key decisions to remember

- **Exp 3 (auxiliary flags):** 54 binary attn_* columns added to
  training. attn_{feature} = 1 if ANY team tagged it at any level.
- **4 labelling teams, not 6:** Reduced from pilot's 6 to 4 for
  production. Still sufficient for consensus detection.
- **Mandatory composition:** BET/RAISE/CALL/FOLD must tag all 4
  villain composition features. Only CHECK exempt.
- **Bucket-specific features:** Drawing=draw_outs+improvement_prob,
  Air=overcard_outs+has_showdown_value+fold_equity, etc.
- **CONFIRMED tier:** PRIMARY (drove decision) vs CONFIRMED
  (checked, supports) vs DISCOVERED (bottom-up find)
- **Pilot v2 labels are production labels** for those 20 hands.
  T1-T4 relabel them alongside the other 365 — if they match
  pilot consensus, they stand.
- **Commit after every step** — power failure protection.
- **No mid-stream vocabulary changes** — one review after all
  labelling complete.

### Pass 1 is NOT started yet

The previous session committed the GO directive but did not begin
execution. Start with situation preparation (Phase 1 above).
