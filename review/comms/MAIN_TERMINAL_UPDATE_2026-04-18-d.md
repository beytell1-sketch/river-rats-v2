---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder + Game builder + Teaching terminal
re: Strip override clause — revert to v2.2 for playtest, re-label supplement clean
status: DIRECTIVE — all three terminals
---

# Fix: Strip Override, Re-label Clean

The Stream B.2 override clause in gto_labeller_v3.md caused
the model to overgeneralize BET in checked-through spots.
The override is a manual patch that says "bet more" without
teaching the model when NOT to bet. This is a fundamental
approach problem, not a tuning issue.

## Game builder — revert to v2.2 NOW

Swap oracle adapter path back to `v2_2_model.json`. One line
change. Push. Playtest continues with v2.2 — it has the
CHECK bias (known, documented) but doesn't confidently tell
students to bet with air on monotone boards.

v2.2 is the production model until the clean v2.3.1 ships.

## Logic builder — strip override, re-label, retrain

### 1. Create `prompts/gto_labeller_v3.1.md`

Start from v3. Remove:
- **Stream B.2 override clause** (lines 294-383) — the
  entire BET-Decision Guidance section
- **§3.A** (DO NOT Rule 10 — compressed-SPR checked-to
  CHECK default)
- **§3.C** (Step 3 enhancement — checked-to value-extraction
  action addition)
- **§3.D** (Calibration notes — MW CHECK-lean pattern
  reference)
- **`override_clause_fired` field** from the output schema
- All references to "override clause" throughout the prompt

Keep:
- **§3.B** (HRP artifact warning — informational, not an
  action directive)
- **"Oracle's Read" headers** (non-override improvement)
- **Draw-type specificity** (template improvement, not a
  labelling directive)
- All v2 content unchanged (54-feature table, bucket
  taxonomy, DO NOT Rules 1-9, reasoning protocol)

The v3.1 prompt is v2 + cosmetic improvements. Panels
reason on poker merits per hand. No BET-preference rules.

Commit as `prompts/gto_labeller_v3.1.md`. Keep v3 as
historical reference — do not delete.

### 2. Run calibration gate on v3.1 prompt

Same gate: 23/28 + 100% on 5 reversal hands. The v2 prompt
produced 20/24 originally; v3.1 should perform at least as
well since it keeps v2's reasoning protocol intact.

If calibration fails: tune the prompt's reasoning guidance,
NOT by adding override rules. The panels must reach correct
answers through poker reasoning, not checklists.

### 3. Re-label Section 1 supplement with v3.1

Re-run Phase 4 labelling on the ~215 Section 1 hands using
the v3.1 prompt. Same 4-panel + Pass 2 pipeline. No Phase
3.5 pilot needed — v3.1 is simpler than v3 (less can go
wrong).

The labels that come back reflect what the panels genuinely
think on poker merits. If 80% are still BET: the original
signal was real (panels BET on merits, not because the
override told them to). If 60% are BET and 40% are CHECK:
we get balanced labels — exactly what the model needs.

Either outcome is correct. The point is honest labels.

### 4. Assemble + train + evaluate

| Source | Rows | Labels |
|---|---|---|
| v2.2 base | 385 | v2 prompt (clean) |
| Section 1 supplement | ~215 | v3.1 prompt (clean) |
| CALL supplement | 25 | keep (CALL-focused, not override-affected) |
| **Total** | ~625 | all clean |

No UMBRELLA. No class weighting.

Train with standard XGBoost config. Evaluate on all 5
criteria (with Criterion 5 reframed per earlier decision).

### 5. What to expect

- Some of the original 4 BET-misses may stay corrected
  (panels BET on merits → model learns from genuine signal)
- Some may revert (panels CHECK on merits → the override
  was the only thing making them BET). That's information.
- The air-on-monotone-board problem should NOT appear
  (model trained on honest labels, not BET-skewed ones)
- FB-40 should maintain ≥70% (CALL supplement still in)
- MW-50 may be lower than 82% if fewer hands are BET-
  labelled. That's acceptable — honest accuracy is better
  than override-inflated accuracy.

### Timeline

- Step 1 (v3.1 prompt): ~1 hour
- Step 2 (calibration): ~30 min
- Step 3 (re-label ~215 hands): ~1-2 hours
- Step 4 (assemble + train + eval): ~1 hour
- Total: ~half a day

## Teaching terminal — no changes needed

The teaching content (templates, coherence guards, L3
hardening) is independent of the labelling prompt. The
`render_from_enriched` API is stable. No teaching changes.

## The lesson

Fix biases through diverse training examples, not prompt
rules. If panels systematically get a shape wrong, add real
hands showing both correct actions in that shape. The model
learns the decision boundary from seeing examples of both
classes, not from a rule that says "prefer X."

The override approach was wrong. It was my recommendation
and it cascaded: override → skewed labels → skewed training
→ overgeneralized model → students told to bet with air.
The clean path was always "better examples, honest labels."
