---
date: 2026-04-15
from: Main terminal (owner-assisted recovery)
to: Builder terminal
re: ANOMALY-A UNBLOCKED — v2.2 trainer recovered, model is sound
status: DIRECTIVE — proceed with Tracks 4 and 2
---

# Main Terminal Update #3 — Trainer recovered, ANOMALY-A resolved

## TL;DR

**ANOMALY-A had ZERO training-time impact on v2.2.** The
trainer at `review/recovered/train_v2_2_MODEL.py` (commit
`4b08805`) handled the mixed string/numeric encoding correctly.

You were right to flag BLOCKED-ambiguity. Owner located the
trainer in the Claude Code session transcript at
`~/.claude/projects/-home-rupertbeytell/81bf3fe7-5f95-4ea9-90fc-04263a5e8161.jsonl`.
The training was executed via inline `python3 <<'EOF'` bash
heredocs — that's why no script was in the repo.

## What the trainer actually does

Lines 31-41:

```python
CAT_MAPS = {
    'street': {'flop':0,'turn':1,'river':2,'':0},
    'hero_position': {'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
    'villain_position': {'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
}

def encode(row, col):
    if col in CAT_MAPS:
        val = row[col]
        try: return float(val)
        except: return float(CAT_MAPS[col].get(val, 0))
    return to_float(row[col])
```

This is **PATH 3 in your branch list — explicit mapping.**
String inputs (`'flop'`, `'BTN'`, etc.) raise `ValueError` on
`float()`, fall back to the dict lookup, get the correct integer
encoding. Both 200 numeric rows and 185 string rows end up at
the same correct encoding.

**v2.2 model was trained on clean encoded data.** Mixed CSV
encoding is real (and your Fix 1 is still correct to apply
upstream), but it had no impact on the model itself.

## Implications

### For Gate 7
- v2.2 model is sound — training was not corrupted
- The 80% MW miss is genuine model behaviour
- Bucket-first CHECK bias diagnosis stands as the working
  hypothesis
- Owner's solver verification of 10 MW misses still drives the
  ship/iterate decision

### For Track 4
- **UNBLOCKED.** Bias deep-dive can proceed using your already-
  prepped feature data
- The corrected bias signature (HRP HIGH at top of range, equity
  HIGH, BET-true predicted CHECK) is what to investigate
- GTO Expert reads all 10 MW misses with full feature context,
  identifies bias pattern (trap / defensive / label/model
  alignment)

### For Track 2
- **UNBLOCKED.** Use `review/recovered/eval_FB40_plus_ablation.py`
  and `review/recovered/eval_MW_with_legal_action_masking.py`
  as the canonical inference pattern
- Re-implement with the hardened 54-or-108-feature harness
- Confirm 72.5% / 80.0% reproduce exactly with the recovered
  inference logic
- Promote the recovered scripts into `river-rats-core/` with
  proper structure (don't leave them in `review/recovered/`
  long-term)

### For ANOMALY-A
- Builder's Fix 1 to BP generators is STILL correct — apply
  it as planned
- The pre-flight schema gate is STILL correct — wire it
- The encoding inconsistency in `v2_2_training.csv` is real;
  fix at the upstream source for v2.3
- But the v2.2 model itself is sound — no retraining needed
  for ANOMALY-A reasons

### For v2.3
- Prerequisite: clean encoded BP JSONLs (your Fix 1)
- Prerequisite: `train_model_v2_2.py` properly checked into
  `river-rats-core/` with the recovered logic — so v2.3
  trainer can be a clean refactor instead of guesswork

## Next actions for builder

1. **Promote the recovered scripts.** Move `review/recovered/`
   content into `river-rats-core/` with proper structure:
   - `river-rats-core/train_model_v2_2.py` (the trainer)
   - `river-rats-core/eval_v2_2.py` (consolidated FB-40 + MW
     evaluator using the legal-action masking version that
     produced the 80% MW number)
   Keep recovered/ as historical reference.

2. **Track 4 GO.** GTO Expert deep-dive on the 10 MW misses
   with the corrected bias signature. Deliverable:
   `review/comms/MW_MISS_BIAS_ANALYSIS_2026-04-15.md`

3. **Track 2 GO.** FB-40 + MW-50 re-eval using the recovered
   inference logic + the hardened 54-feature harness from Track 1.
   Confirm reproduction or document differences.
   Deliverable: `review/comms/EVAL_RERUN_HARDENED_2026-04-15.md`

4. **Track A scope corrections** can now be drafted properly.
   The bias signature is final (Track 4 confirms or refines
   it), the trainer is recovered, the encoding fix is upstream.
   Architect can complete Track 6 amendments to
   `PLAN_V23_SCOPE_2026-04-15.md`.

5. **Process fix:** going forward, every training run commits
   its script to `river-rats-core/`. No more inline heredoc
   training. Add to CLAUDE.md if it isn't already there.

## What does NOT change

- Don't ship v2.2 yet — Gate 7 still pending solver
- Don't generate v2.3 hands yet — wait for Track A scope to be
  finalised post-Track 4
- Don't retrain v2.2 — it's sound, the encoding fix is for
  upstream regeneration only

## Commit discipline

You're doing this right since the restart. Keep pushing after
every commit. Owner will continue checking GitHub for new
artifacts.

---

**Builder: proceed with the 5 actions above. Tracks 2 and 4
unblocked. ANOMALY-A reframed as a real defect that did not
affect v2.2 outcomes. Gate 7 still owner's call after solver.**
