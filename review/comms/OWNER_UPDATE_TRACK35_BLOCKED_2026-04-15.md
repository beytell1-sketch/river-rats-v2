---
date: 2026-04-15
from: Main terminal (reviewer)
to: Owner (Rupert)
re: Track 3.5 complete — ANOMALY-A confirmed, scope is 2x audit, training script missing
status: BLOCKED-AMBIGUITY — owner decision needed
---

# Track 3.5 Report — ANOMALY-A Verification

The builder came back, ran Track 3.5 properly, and pushed to
GitHub. They correctly stopped at an ambiguity and flagged
BLOCKED per CLAUDE.md. Full report at commit `498e076` —
`review/comms/ANOMALY_A_VERIFICATION_2026-04-15.md`.

## What's confirmed

1. **Root cause found.** BP-series factory generators in
   `review/generate_factory_batch*.py` write `street='flop'` and
   `hero_pos='BTN'` as Python strings. D-series pipeline emits
   them as integers. Phase 3.5H assembly merged both without
   normalising. The 185/200 string/numeric split is exact.

2. **Scope is DOUBLE what the audit reported.** `hero_position`
   has the same defect as `street` — 185 string rows,
   200 numeric, same row set. The audit only flagged `street`.
   Two columns corrupted, not one. 48% of training data affected
   on TWO features.

3. **`villain_position` is clean.** Always numeric. Unaffected.

4. **Pre-training schema test is written** (test-first protocol).
   Currently fails on `v2_2_training.csv`. Will pass after the
   fix is applied upstream.

## What's BLOCKED (and why)

**The v2.2 training script is not in the repo.**

Commit 5267a0b added only the model + reports — no training
code. The existing `train_model.py` targets a DIFFERENT CSV
(54 columns, not 108) and would crash on `float('flop')`.

So we can't cite exactly how v2.2 handled the mixed encoding.
Three behaviours remain possible:

| Path | What happened on 185 string rows |
|---|---|
| `pd.to_numeric(errors='coerce')` | NaN → XGBoost learns directed default split |
| Proper mapping (`{'flop':0,...}` fallback) | Clean encoding, no corruption |
| Silent zero on exception | 185 rows all became `street=0` (flop) regardless |

If it was the third path (worst case), **99 rows (25.7% of
training data) had their turn/river examples shown as flop
examples.** That would bias the model toward flop-like (less
aggressive) decisions on turn/river — which exactly matches
the bucket-first CHECK bias we see on MW.

If it was the second path (best case), no impact — we retrain
cleanly for v2.3 and move on.

We cannot tell without the script.

## What the builder did NOT do (correctly)

- Did not retrain v2.2
- Did not modify the CSV in place
- Did not improvise a fix for the missing trainer
- Did not guess the behaviour

This is exactly the right response per the stop conditions in
CLAUDE.md.

## Connection to Gate 7

The builder flags this explicitly: the MW miss bias (all 10
BET-true predicted CHECK) is **consistent with** a model that
saw 99 turn/river hands as flop hands. Not diagnostic, but
consistent. This is a legitimate reason to hold v2.2 ship —
the model may have been trained on systematically corrupted
street signal.

## Owner decisions needed

### Decision 1: Training-impact verdict

Accept BLOCKED-ambiguity, OR authorise recovering the v2.2
trainer. Recovery options:

- **A.** You have the script on a local machine somewhere — check
  your bash history or local dirs (`~/Downloads`, `~/scripts`,
  Google Drive, etc.) and push it to GitHub
- **B.** Re-run training on the same CSV with explicit logging,
  observe what the loader does with strings, infer the original
  behaviour by matching CV numbers (93% ± 3.5%)
- **C.** Accept "worst case" assumption and proceed as if path 3
  was used — means treat v2.2 as corrupted and prioritise v2.3
  retrain
- **D.** Accept BLOCKED and make the Gate 7 decision assuming
  the corruption MIGHT be real

My recommendation: **A first, C as fallback.** If the script
isn't recoverable from your local machine, assume worst case
and don't ship v2.2 — retrain for v2.3 with clean encoding.

### Decision 2: Fix sequencing

Builder proposes:

1. Apply Fix 1 to BP-series generators (normalise at write time)
2. Regenerate affected JSONLs
3. Re-run schema test — must pass
4. THEN consider any v2.3 training

This is correct. Approve and builder implements.

### Decision 3: Process fix

Check the v2.2 training script into `river-rats-core/` with a
version suffix (`train_model_v2_2.py`) so future audits can
cite it. Going forward, every training run commits its script.

## Connection to Gate 7 decision

You now have three data points to weigh for v2.2 ship:

1. **FB-40 passed** — model works on facing-bet decisions
2. **MW missed by 2.5pp** — bias toward CHECK on hero-at-top-of-range hands
3. **NEW: street may have been corrupted on 48% of training data** — could be partial explanation of #2

And pending: **10 MW misses need solver verification** to
understand whether the bias is real bucket-first passivity or a
data artifact from #3.

My recommendation shifts slightly with this finding. Earlier I
said run solver on the 10 misses to decide Gate 7. Now I'd say:

- **If we can recover the v2.2 trainer:** run solver + verify
  training used clean encoding. If both confirm clean, ship.
- **If we cannot recover the v2.2 trainer:** don't ship v2.2.
  Too much uncertainty. Fix the encoding, retrain for v2.3, and
  make the ship decision on the clean version.

Solver on 10 misses is still worth doing either way — if it
confirms genuine bucket-first bias regardless of street, we
know v2.3 needs both encoding fix AND prompt guards. If it
confirms misses are plausibly street-confused, the encoding
fix alone may solve it.

## What I'm committing

This file. It captures the state for future sessions and gives
you the decision framework.

## What I need from you

1. Check your local machines for the v2.2 training script
2. Decide on training-impact verdict approach
3. Authorise (or not) the Fix 1 application to BP generators

When you have solver time, run the 10 MW misses — that data is
still useful regardless of the encoding decision.

---

**Everything is on GitHub up through commit a3a9e25. Builder
is standing by.**
