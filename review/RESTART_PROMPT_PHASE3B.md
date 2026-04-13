# Restart Prompt — Phase 3B Calibration

## Project

River Rats v2 — GTO poker coaching oracle. XGBoost 5-class model
(FOLD/CHECK/CALL/BET/RAISE), 54 features, 3-way postflop.

## Working directory

`/home/rupertbeytell/river-rats-v2`

## What just happened

Phase 3A is complete. The labelling prompt has been rewritten to
use bucket-first reasoning with enriched output (intentions, street
plans, feature attention). Features 49-54 are promoted. 385
training situations are ready (200 reconstructed self-play + 185
new factory). Gate 5 passed — owner approved the v2 prompt.

## What to do now — Phase 3B Calibration

Run the calibration exam: 24 three-way reference hands labelled
with the v2 prompt. Gate: 20/24 (83%) overall + all 3 GTO-reversal
hands correct.

### Key files to read FIRST

1. `prompts/gto_labeller_v2.md` — THE labelling prompt (bucket-first
   + enriched output). This is what the calibration agent uses.
2. `knowledge/three_way_gto.md` — the KB. Appended to the prompt
   at runtime. Contains worked examples and DO NOT rules.
3. `river-rats-core/calibration_exam.py` — the exam infrastructure.
   `load_3way_reference_hands()` loads 24 hands.
   `reference_hand_to_situation()` converts to agent input format.
   `format_situation_for_agent()` produces the text block.
   `score_results()` checks 20/24 gate + reversal gate.
4. `review/comms/PLAN_PHASE3_FINAL_2026-04-13.md` — the approved
   Phase 3 plan.
5. `review/comms/OWNER_APPROVAL_PHASE3_FINAL_2026-04-13.md` — owner
   approval with answers to all 5 questions.

### The 24 exam hands

Exported to `/tmp/calibration_situations.json` (may not survive
restart — regenerate with calibration_exam.py if missing).

Split into 3 batches of 8:
- Batch 1: MW-12, MW-13, MW-14, MW-15, MW-17, MW-18, MW-19, MW-23
- Batch 2: MW-24, MW-27, MW-28, MW-30, MW-33, MW-34, MW-35, MW-36
- Batch 3: MW-37, MW-38, MW-39, MW-41, MW-44, MW-48, MW-49, MW-50

### GTO-reversal hands (MUST be correct)

- **MW-30:** CALL (solver-corrected — 40% equity vs 18% pot odds,
  equity surplus overrides bet-and-call signal)
- **MW-33:** RAISE (set must raise vs bet+call for value extraction)
- **MW-50:** FOLD (BTN raised flop, range narrowed, action history
  overrides 30% raw equity)

### Calibration process

1. Regenerate `/tmp/calibration_situations.json` if missing:
   ```python
   cd river-rats-core
   python3 -c "
   from calibration_exam import load_3way_reference_hands, reference_hand_to_situation
   import json
   hands = load_3way_reference_hands()
   sits = [{'ref_id': h.ref_id, 'expert_action': h.expert_action,
            'expert_confidence': h.expert_confidence,
            'situation_text': format_situation_for_agent(reference_hand_to_situation(h)),
            'feat_dict': reference_hand_to_situation(h)['feat_dict']}
           for h in hands]
   with open('/tmp/calibration_situations.json', 'w') as f:
       json.dump(sits, f, indent=2)
   "
   ```

2. Launch 3 GTO Expert agents (one per batch of 8 hands). Each
   agent receives:
   - The 8 situation texts with full feature vectors
   - The v2 labelling prompt (`prompts/gto_labeller_v2.md`)
   - The KB (`knowledge/three_way_gto.md`)
   - Instruction: produce the full enriched JSON output per hand

3. Collect results. For each hand, record:
   - Agent's action vs expert's action
   - Whether it matches (correct/incorrect)
   - Agent's hand_bucket, intentions, reasoning

4. Score: 20/24 overall + all 3 reversals correct = PASS.
   If FAIL: diagnose which hands failed and why. Adjust prompt
   if needed, re-run. Do NOT proceed to pilot with a failing prompt.

5. Write calibration report to `review/comms/CALIBRATION_V2_REPORT_2026-04-14.md`

6. Commit results.

### After calibration passes

Proceed to **Pilot** (20 hands × 3 feature attention approaches,
10 agents). See PLAN_PHASE3_FINAL for full pilot spec.

## CLAUDE.md

Read `/home/rupertbeytell/river-rats-v2/CLAUDE.md` before starting.
It contains mandatory protocols: plan before build, test first,
blueprint before build, stop conditions, review folder protocol.

## Process Guide

Read `docs/PROCESS_GUIDE.md` for team protocols, agent allocation
rules (≤10 per GTO agent, ≥ labeller÷2 reviewers), and quality
gates.

## Recent commits (for context)

```
e0cdf50 Patch: Gate 5 feedback — forward-thinking in Step 3, fix example intention
c76b4be Phase 3A.3: bucket-first labelling prompt v2 + seed vocabulary
07eb1fa Re-generate 185 factory situations with 54 features
5a28a5d Phase 3A.1: promote features 49-54 to training (48→54 features)
3aa58dd Phase 3 approved by owner — start Phase 3A immediately
a214eb3 Phase 3 final plan: 6-team parallel labelling + targeted deep review
```

## Key decisions to remember

- **Bucket-first:** classify hand before considering actions. No
  equity thresholds in the prompt.
- **Enriched output:** intentions (reason-first, 6 seeds), street
  plans (two-tag, 10 seeds), feature attention (PRIMARY-only,
  pilot determines approach A/B/C).
- **54 features.** Feature 51 nonlinear (keep). Feature 54 new
  (villain_medium_made_pct).
- **6-team parallel labelling** in Pass 1 (after pilot).
- **Commit after every step** — power failure protection.
- **Difficulty assessed AFTER decision** (Step 5 in prompt).
