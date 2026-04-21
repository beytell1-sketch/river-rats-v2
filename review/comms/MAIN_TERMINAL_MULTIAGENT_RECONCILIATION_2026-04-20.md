---
date: 2026-04-20
from: Main terminal (reviewer/orchestrator)
to: Builder · Owner
re: Multi-agent review reconciliation — Stage 3.5 has real gaps, 2 CRITICAL, must address before Stage 4
status: RECONCILIATION — supersedes single-reviewer dispatch plan; MUSTs before ship
---

# Multi-Agent Reconciliation — Stage 3.5

Six parallel agents ran review: GTO theorist, practical pro, red-team,
architecture, research, test-case generator. Results exposed real
issues single-reviewer discipline would have missed. Owner's
escalation call was justified.

## CRITICAL findings — MUST fix before Stage 4 / ship

### CRITICAL #1 — Blocker features BYPASS the chain (red-team Attack #8)

**The plan claimed** all 10 villain-derived features inherit Stage 3.5
automatically.

**The actual code** (feature_extractor.py:1648-1662, 1720+): Step 12
(`flush_block_pct`) + Step 17 (the 4 new v2.4 P1 blocker features)
reconstruct `_s12_v_range` via `get_villain_range(...)` DIRECTLY,
applying only `narrow_to_betting_range` when `facing_bet`. **They
never call `narrow_by_action_history`.**

Result: teaching will display chain-narrowed composition alongside
un-narrowed block percentages — two inputs disagreeing about what
villain's range is. Same-class failure as the SHAP-vs-action
contradictions we've hit before, but at the feature-computation
level.

**Fix:** Step 12 + Step 17 must consume the already-narrowed range
from `classify_villain_range`, not recompute. Single call-site
correction; high-leverage.

### CRITICAL #2 — Silent training distribution split (red-team Attack #7)

`_action_history` may not be populated on every training-data row
(gauntlet/synthetic fixtures, backfill, v2.3.1 base CSV).

When absent, the code falls back to pre-Stage-3.5 behavior SILENTLY
— no warning, no error, no audit trail.

Stage 4 re-label would then produce a MIXED training distribution:
chained for playtest-sourced hands, non-chained for synthetic/
gauntlet rows. Model learns the mixture.

**This is the exact failure mode that broke v2.3.2.**

**Fix:** 
- Emit loud warning (or raise) when `_action_history` absent during
  Stage 4 feature extraction
- Audit all training-data pipelines (extract_features_parallel.py,
  extract_incremental.py, gauntlet scripts) to confirm action_history
  propagation
- Add `_action_history_present: bool` flag to training CSV for
  post-hoc audit

## HIGH findings — MUST fix before ship (not just Stage 4)

### HIGH #3 — Check-raise sign flip (red-team Attack #5)

Chain applies flop-CHECK × flop-BET sequentially on the same board
for check-raise lines. Table values produce **inverted composition**
— mediums up, nuts down. Check-raise range should be 60-80% nuts;
chain produces medium-heavy.

**Fix:** `narrow_by_action_history` must handle double-actions-per-
street differently. Options: (a) use check-raise-specific frequency
table, (b) skip the CHECK when followed by RAISE on same street and
treat as single aggressive action, (c) document as known limit with
v2.5 fix.

My call: **(b) for v2.4.** A check-raise IS an aggressive action;
semantically it's closer to a bet than a check+bet sequence. Treat
check-raise as the raise only. GTO reviewer can confirm/redirect.

### HIGH #4 — FOLD re-fetch silent bug (architecture Q5)

feature_extractor.py:1186 — when chain returns empty range from FOLD,
caller silently re-fetches `get_villain_range()` un-narrowed. Features
compute against preflop range for a folded villain. Wrong.

**Fix:** Replace re-fetch with `meta['villain_folded'] = True`
sentinel; feature extractor skips villain-composition features for
folded villains (or marks them as `NaN`/null).

### HIGH #5 — `surviving_weight` proxy is wrong (red-team Attack #1, arch Q5)

Current `surviving_weight` = `len(current_range) / len(full_range)`
— hand COUNT, not probability MASS. A range of 3 hands at freq 0.33
passes the floor but is semantically collapsed. Safety rail gives
false OK on degenerate distributions.

**Fix:** Compute true surviving weight inside each narrow step
(un-normalized weight sum) and thread through chain. Low complexity.

## SHIP_WITH_REFACTOR — not SHIP_AS_IS

Architecture verdict is **SHIP_WITH_REFACTOR** with 3 MUSTs before
Stage 4 re-label:
1. FOLD re-fetch fix (HIGH #4 above)
2. Unit test file covering 10 canonical cases
3. Observability hooks (chain_steps, surviving_weight, truncated) in
   returned `_meta_` fields — Stage 4 drift must be auditable

**Good news:** test-case generator agent delivered 81 cases with
pre/post expected values at
`/home/rupert/river-rats-v2/review/tests/range_narrowing_test_corpus_2026-04-20.yaml`.
Direct pickup for the unit test file.

## Confirmed by multiple reviewers (convergent findings)

- **Bet-size conditioning** is the biggest v2.5 gap. GTO, practical,
  research agents all flag independently. Already in v2.5 queue.
- **Multiplicative chain is a legit first-order approximation** but
  not solver-equivalent. Research agent positions it as Flopzilla/
  Equilab lineage, not CFR-equivalent. Acceptable for a teaching
  tool.
- **Population-deviation layer** (pros don't play GTO-perfect) is a
  v3+ concern. Practical agent flagged; everyone else agreed it's
  out of v2.4 scope.
- **Compounding error** on deep chains (4-street) is real; research
  agent cited node-locking literature. Not a ship-blocker; monitor
  in validation.

## One conflict to resolve — same-street pre-hero actions

**GTO theorist:** Include. Theoretically correct — a check is a
check regardless of whether hero's decision is later-street or
same-street.

**Red-team:** Exclude per current spec. Attack #10 verified the 4
flop anchors stay stable only because same-street is excluded.
Including would create anchor flips alongside other changes,
muddying the validation signal.

**My call: EXCLUDE for v2.4** per current spec. Reasoning:
- Anchor stability is needed to validate Stage 3.5 works in
  isolation
- When v2.5 adds bet-sizing conditioning, we can also include
  same-street actions + re-calibrate anchors in one coordinated
  change
- Don't conflate two changes in one ship

GTO theorist's concern is valid and queued for v2.5.

## What this means for plan sequence

**Revised Stage 3.5:**

1. Builder fixes the 5 MUSTs (CRITICAL #1, #2, HIGH #3, #4, #5)
2. Unit test file lands (81-case corpus)
3. Observability hooks land
4. Anchor regression run
5. Retroactive audit on v2.3.1 training CSV
6. If anchors pass and audit is clean → Stage 3.5 ships
7. **Then** Stage 4 re-label opens

**The original "single GTO reviewer dispatch" would have missed
Attacks #8 and #7** — both CRITICAL, both repeat of past failure
modes. The escalation was worth it.

## Lessons for memory

Single-reviewer discipline insufficient for:
- Load-bearing architectural changes
- Features with cross-component blast radius
- Changes that touch training-data pipeline
- Anything where silent failure modes are plausible

Multi-agent review pattern (GTO + practical + red-team + architecture
+ research) should be the default for this class of work.

## Reports archived

Full agent outputs in this directive doc's history. Key findings
extracted above; deep-dive available from each agent's transcript.

## Immediate next action

Builder reads this reconciliation, then:

1. Acknowledge the 5 MUSTs
2. Patch CRITICAL #1 (Step 12 / Step 17 bypass) and CRITICAL #2
   (action_history missing warning + audit) before any GTO reviewer
   dispatch — those are bugs in the current code, not theory
   questions
3. Once patches land, dispatch GTO reviewer on the revised range
   narrowing plan + ship the unit test file
4. Stage 3.5 enters implementation-verify cycle

No model training, no teaching changes, no prompt work until
Stage 3.5 passes its revised ship gate.

Go.
