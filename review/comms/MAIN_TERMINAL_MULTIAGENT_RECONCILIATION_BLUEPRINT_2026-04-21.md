---
date: 2026-04-21
from: Main terminal (orchestrator)
to: Builder · Owner
re: Multi-agent reconciliation on Stage 3.5 BLUEPRINT (b1a9a91)
status: REWORK — blueprint v2 required before any code edits
---

# Multi-Agent Reconciliation — Stage 3.5 BLUEPRINT (b1a9a91)

Five parallel reviewers ran on the blueprint: architecture, GTO theorist,
red-team, practical pro, research/solver-lineage. Aggregate verdict
**REWORK**. Red-team is the strongest signal; GTO + practical pro +
research converge on the §11 escalation; architecture verifies HEAD
drift is clean but flags caller-list incompleteness as CRITICAL.

Builder must re-cut the blueprint addressing the new MUSTs below before
implementation begins. This reconciliation supersedes blueprint b1a9a91
on the points it addresses; the BEFORE/AFTER patches that survive
this reconciliation are still valid.

## Verdict matrix

| Reviewer | Verdict | Strongest finding |
|---|---|---|
| Architecture | APPROVE_WITH_FIXES | HIGH #5 caller list incomplete (14 sites, blueprint listed 5) |
| GTO theorist | APPROVE_WITH_FIXES | §11 should be 6th MUST — equity inconsistency mistrains the model |
| Red-team | **REWORK** | Strict-raise broken (workers swallow RuntimeError); coaching/ duplicate is total bypass surface; CRIT #2 commit order leaves Stage 4 vulnerable mid-ship |
| Practical pro | APPROVE_WITH_FIXES | T_J01 (owner's canonical hand) post-fix values copy pre-fix — visible regression to owner |
| Research | APPROVE_WITH_FIXES | Mass floor 5% too permissive; tighten to 10% per chain-compounding literature |

## NEW MUSTs (additions to original 5)

### MUST #6 — CRITICAL — §11 equity-feature chain inheritance is IN-SCOPE

**4-of-5 reviewer vote.** GTO, Red-team, Practical pro, Research all
say defer is wrong. Architecture was the only (B) vote and conditional
on an audit column.

**Why it can't defer:** A single training row will carry
`_villain_top_pair_plus_pct` (chained, e.g. 0.45 TP+) alongside
`raw_equity` (un-chained vs preflop calling range, e.g. 0.42 hero
equity). Two views of the same villain disagree inside the same row.
Stage 4 re-label trains the model on the conflict; SHAP renders
contradictory attributions; teaching panel says villain is polarised
while equity says hero has X equity. **Same internal-contradiction
class as v2.3.2 mixture, just at a different layer.**

Magnitude (per Research literature review): 4–12 equity points,
sometimes 15+. Big enough to flip thin river BET/CHECK decisions.

**Scope:**
1. Plumb the chain-narrowed range through `compute_partition_features`
   (`feature_extractor.py:500-505, 605-617`) and `compute_equity_features`
   (`feature_extractor.py:790-806, 823-829`).
2. Equity Monte Carlo (2000 trials/hand) runs against the chained
   range. Builder must benchmark perf impact and report.
3. Re-audit equity-vs-range distribution shift on v2.3.1 training CSV.
4. M5 anchor regression must hold post-equity-chain (3/3 anchors still
   BET).

**Out of scope hybrid path rejected:** Research suggested chain-only-
for-SHAP-display, training-feature-equity unchanged. Doesn't actually
work — SHAP would explain a feature value that doesn't exist in the
model's training distribution. All-or-nothing.

### MUST #7 — CRITICAL — Caller-list audit for HIGH #5 breaking change

Architecture verified blueprint lists 5 callers; actual count is 14+:
- `feature_extractor.py:503, 617, 805, 828, 1193` ✓ (in blueprint)
- `range_narrowing.py:875, 885` ✗ (missed)
- `explain_hand.py:264, 329` ✗ (missed)
- `coaching/feature_extractor.py:503, 617, 805, 828, 1137` ✗ (missed)
- `coaching/explain_hand.py:264, 329` ✗ (missed)
- Test files via grep ✗ (incomplete in blueprint)
- Plus `blocker_features.py`, `range_decomposition.py` per Red-team H6

Builder must produce the complete grep before any HIGH #5 edits.

### MUST #8 — CRITICAL — Resolve `coaching/` duplicate

Red-team C3: `coaching/feature_extractor.py` is 90KB, has zero
`_action_history` references, lacks env-var strict guard. If any
caller imports from `coaching.*` at runtime (worker fallback, sys.path
ordering, test fixtures), it silently runs pre-Stage-3.5 code,
defeating ALL 5 MUSTs.

`coaching/range_narrowing.py` has its OWN parallel `narrow_to_betting_range`
/ `_checking_range` definitions (~lines 375, 439). HIGH #5 tuple-
return change applied only to root would break callers that hit
coaching-version dict-return path or vice versa.

**Builder action:** Inventory who imports from `coaching/`. Then
either:
- (a) **Delete** coaching/ duplicates + repoint all imports to root
  (architect + red-team preferred)
- (b) **Mirror** all 5 MUSTs into coaching/ in parallel commits

Orchestrator recommends (a). Owner sign-off requested ONLY if (a)
finds active runtime importers that can't be repointed.

### MUST #9 — CRITICAL — Strict-raise must NOT be swallowed

Red-team C1: `extract_features_parallel.py:81` wraps
`extract_all_features(hand)` in `except Exception: errors += 1`.
Same in `extract_incremental.py:105` and gauntlet runners. The
RuntimeError that CRIT #2 strict-raise emits will be caught silently
and counted as a row error. The run continues with reduced yield.
Loud fail becomes loud nothing.

**Builder action:** Three options, in priority:
1. Replace `except Exception` with explicit non-RuntimeError catches
   (allow strict-raise to propagate)
2. Re-raise RuntimeError specifically: `except RuntimeError: raise`
   inside the existing handler
3. Worker propagates a teardown signal that `sys.exit`s the parent

Without this fix, CRIT #2 is fiction. Architecture Q4 (env var
acceptable) is correct only after this is patched.

### MUST #10 — HIGH — NaN handling spec across 4 layers

Red-team Q2 attack: NaN does survive CSV write/read, passes
`gto_model` dtype guard (NaN is a Python float), routes through
XGBoost default-direction branch (which it learns at fit time),
and BREAKS the teaching layer (situation_describer renders literal
"nan" or silently fails ranking).

Practical pro: "flush_block_pct: nan" in player display is
unacceptable.

**Builder action — concrete sub-asks:**
1. **Teaching layer:** When `_villain_folded=True`, render
   "villain folded — blockers N/A" (no individual blocker fields).
   CONTENT_API spec change; coordinate with teaching terminal.
2. **Training (Stage 4):** Owner decision pending — drop folded-
   villain rows from blocker-feature columns (impute via mask),
   OR train with NaN as a learnable XGBoost category.
   **Orchestrator decision: drop folded rows from blocker-feature
   columns**; folded villain provides no blocker signal worth
   training on. Cleaner distribution.
3. **SHAP:** When input has NaN blocker features, skip blocker-
   feature contributions entirely in `feature_attention` PRIMARY
   tagging. Do not render NaN-derived SHAP top-features.
4. **`gto_model`:** Add `math.isnan` check on inference-side
   feature dict; raise on unexpected NaN in non-blocker columns
   (defensive — flags future-unknown NaN sources).

### MUST #11 — HIGH — Q7 collapse: extend pre-filter to check-call

GTO + Practical pro + Research converge on YES.

**Reasoning:** A check-call is semantically a single continuing
action. Applying CHECK (mediums up, nuts down) then CALL (mediums
up again, nuts slightly down) double-weights mediums and produces
a too-narrow continue range. Same logic as check-raise.

**Patch:** Extend HIGH #3's pre-filter rule from `(check, bet)` to
`(check, bet|raise|call)`. The CHECK is dropped whenever followed
by ANY same-street action that is the actual decision-bearing
move.

### MUST #12 — HIGH — Pre-filter handles all malformed sequences

Red-team H3: builder's pre-filter only handles `(check, bet)`. Misses:
- `(bet, raise)` — own bet then own raise (physically impossible
  but chain doesn't validate; both narrow to 'bet' class → double-
  betting narrowing)
- `(check, bet, raise)` — check-bet-3bet (legal in 4-way+ when
  villain check-bets one player and gets raised by another villain
  in his own action history filter; current filter logic doesn't
  handle the triple)
- Generic safety: any same-street sequence with >2 villain actions

**Patch:** Pre-filter must be a proper sequence collapser. For each
same-street villain action sequence, keep only the LAST aggressive
action (highest of FOLD < CHECK < CALL < BET < RAISE in semantic
"final stance" ordering). FOLD is a terminal — the sequence ends
there.

### MUST #13 — HIGH — Mass safety floor 5% → 10% with 20% WARN

Research literature review: chain compounding error per street is
1.3–1.6x; at <10% cumulative mass the distribution is dominated by
the last-applied filter (effectively single-street behavior in
chain's clothes).

Builder example: flop-CHECK 0.5 × turn-CHECK 0.4 × river-BET 0.3
= 6% — barely passes 5%. Distribution is too narrow to model
meaningfully.

**Patch:** `_STAGE35_WEIGHT_FLOOR_PCT = 0.10` (truncate). Add
`_STAGE35_WEIGHT_WARN_PCT = 0.20` (log WARN, don't truncate). Add
corpus calibration case using deep-chain shape (T_K20 baseline)
with synthetic distribution that lands at 7% (currently passes,
post-fix truncates).

Architecture's "ship at 5%, document for tuning" is overruled by
Research's evidence-grounded threshold.

### MUST #14 — HIGH — Commit order: CRIT #2 second, not last

Red-team rebuttal to §13's commit order: CRIT #2 last leaves Stage 4
vulnerable to mid-ship mixed-distribution injection. If Stage 4 fires
between commits 5 and 6, the training-CSV is poisoned.

**Re-sequenced commit order:**
1. HIGH #5 (mass threading + tuple return + caller list complete)
2. **CRIT #2 (strict-raise + audit column + pipeline propagation)** — moved
3. HIGH #3 (check-raise pre-filter + Q7 check-call collapse + Q12 generic)
4. CRIT #1 (blocker features consume chain)
5. HIGH #4 (folded-villain sentinel)
6. **MUST #6 (equity-feature chain inheritance)** — new
7. **MUST #8 (coaching/ duplicate resolution)** — new
8. Unit test corpus + audit re-runs

### MUST #15 — HIGH — Over-narrowing fallback NaN-flag, not warn+fallback

Red-team Q9: §4.1's "preserve pre-fix behavior + WARN" IS the
silent-fallback anti-pattern that the original reconciliation rejected.
Re-fetching un-narrowed preflop range when chain over-narrows lets
Stage 4 mix chained and un-chained composition silently. Same
v2.3.2 failure mode as CRIT #2.

**Patch:** When chain over-narrows to empty without FOLD, NaN-flag
composition features (parallel to folded-villain handling). Set a
new `_villain_chain_overflowed` audit flag. Do NOT re-fetch.

### MUST #16 — HIGH — M5 anchor regression must populate `_action_history`

Red-team: `run_v231_anchor_recheck_stage35.py` re-runs existing
fixtures. If fixtures lack `_action_history`, post-fix anchor run
silently takes pre-Stage-3.5 path; "3/3 BET" result is vacuous —
proves nothing about the fix.

**Patch:** Anchor fixtures must include `_action_history` populated
to a realistic shape per anchor. Audit assertion: `chain_steps`
non-empty for every anchor row. If chain_steps empty, FAIL the
audit (means the anchor isn't actually exercising the chain).

### MUST #17 — MEDIUM — Frequency table tweak

GTO: `RIVER_CHECKING_FREQUENCIES.medium_made` 0.92 → 0.85. Thin
river value with medium pair exists vs weak ranges, especially on
multi-street missed-draw lines. 0.92 over-compresses mediums into
the check-call branch.

**Patch:** Single-table edit in `range_narrowing.py:142`. Document
v2.5 path for board-texture-conditional table.

### MUST #18 — MEDIUM — Corpus expected-value reauthoring

**T_J01 (owner's canonical hand H_d9edab5d):** Practical pro flagged
expected_post_fix is a copy of pre-fix (0.70 TP+ / 0.04 med / 0.26
air ≈ pre-fix 0.72/0.06/0.22). Same shape as K_05/K_06 (delayed-
probe lines) which correctly show 0.55–0.62 TP+ / 0.33–0.41 air.

**Patch:** T_J01 `expected_composition_post_fix` rewritten to match
K_05/K_06 pattern (~0.55 TP+ / ~0.04 medium / ~0.41 air).

**T_B05 (donk-flop, call-raise, turn check):** GTO flagged
medium_made 0.25 too high. Post-fix should be ~0.65–0.75 TP+ /
0.10–0.15 medium. Reauthor.

**This is owner's canonical hand. If T_J01 ships showing "nothing
changed," the project looks broken to the person who flagged the
gap in the first place.**

### MUST #19 — MEDIUM — Additional bypass at `explain_hand.py`

Red-team H1 — 7th/8th bypass site. `explain_hand.py:264, 329` (and
coaching duplicates per MUST #8) call `decompose_range` with
`get_villain_range(...)` no chain. Teaching-time range decomposition
will contradict the model's composition features.

**Builder action:** Include in MUST #6 scope (extend chain to all
teaching range-decomposition paths) — same plumbing pattern.

## Q resolutions (consolidated, supersede blueprint §12)

| Q | Resolution | Source |
|---|---|---|
| Q1 | APPROVE metadata field for `_villain_range_narrowed` | architect (with red-team H7 caveat: never serialize whole feature dict) |
| Q2 | NaN unsafe across 4 layers — see MUST #10 for fixes | red-team |
| Q3 | NaN > 0 for folded blockers | GTO + architecture |
| Q4 | env var APPROVED, but BROKEN until MUST #9 lands | architecture + red-team |
| Q5 | Path (a) reconstruct `_action_history` from source logs | practical pro + orchestrator decision |
| Q6 | Option (b) sufficient for v2.4; (a) deferred to v2.5 | GTO + research + practical pro converge |
| Q7 | YES collapse check-call too — see MUST #11 | GTO + practical pro + research converge |
| Q8 | Sentinel needed (`_villain_folded` flag) | GTO |
| Q9 | NaN-flag, NOT warn+fallback — see MUST #15 | red-team |
| Q10 | Breaking return type APPROVED conditional on MUST #7 caller audit | architecture |
| Q11 | Mass floor 10% with 20% WARN — see MUST #13 | research overrules architecture |
| Q12 | Direction tests for v1; calibrate exact values post-merge | tester implicit |
| Q13 | Promote to CSV for Stage 4 audit; out of model feature vector | architecture |
| Q14 | (A) — §11 in-scope as MUST #6 (full chain, not hybrid) | 4 of 5 reviewers |

## Owner decisions (resolved by orchestrator)

Per orchestration discipline (DECIDE and EXECUTE; bar for asking is
ABSOLUTELY NECESSARY), I've made these calls. Owner can redirect any.

1. **Q5 path (a) — reconstruct `_action_history` from source logs.**
   Rejected (b) drops most river-decision training rows, the highest-
   signal hands.
2. **MUST #6 full scope (not hybrid).** Hybrid breaks SHAP integrity.
3. **MUST #8 path (a) — delete coaching/ duplicates + repoint imports.**
   Cleaner long-term; eliminates parallel-bypass surface entirely.
4. **MUST #10 sub-2 — drop folded-villain rows from blocker-feature
   columns at Stage 4 training.** Cleaner distribution than learning
   NaN as a category.

If owner disagrees with any of these, redirect before builder begins
re-cut.

## Cross-check against original 5 MUSTs

All 5 original MUSTs survive intact. Patches in blueprint b1a9a91
remain the foundation; reconciliation adds 14 new MUSTs and modifies
commit order, mass threshold, and pre-filter scope.

The poker-correctness of the original 5 was confirmed by GTO. The
HEAD drift was clean per architecture verification. The chain
narrowing direction is correct.

## What blueprint v2 must include

In addition to the original 5 MUSTs (with reconciliation tweaks above):

- §6 — full caller-list grep results for HIGH #5 (MUST #7)
- §7 — coaching/ duplicate inventory + delete-or-mirror plan (MUST #8)
- §8 — strict-raise propagation patches in pipelines (MUST #9)
- §9 — NaN handling spec across teaching/training/SHAP/gto_model
  (MUST #10)
- §10 — extended pre-filter spec (MUSTs #11 + #12)
- §11 — mass-floor + WARN + corpus case (MUST #13)
- §12 — re-sequenced commit order (MUST #14)
- §13 — over-narrowing NaN-flag (MUST #15)
- §14 — anchor fixture `_action_history` plan (MUST #16)
- §15 — frequency table edit (MUST #17)
- §16 — corpus reauthoring (MUST #18)
- §17 — explain_hand.py bypass plumbing (MUST #19)
- §18 — equity-feature chain inheritance: full spec, perf benchmark
  plan, re-audit plan, M5 hold confirmation (MUST #6)

Re-cut not in-place patch. Clean review trail.

## Reports archived

Five full reviewer outputs in agent transcripts. Architecture wrote
to `review/comms/REVIEW_ARCH_STAGE35_BLUEPRINT_2026-04-21.md`.
Other four returned in chat; key findings extracted above.

## Lessons for memory

- Single-pass blueprint review missed §11 — but builder caught it
  during architect pass and escalated. The escalation pattern
  (architect-finds-during-blueprint, escalate-to-multi-agent-before-
  edits) is the right discipline.
- Reconciliation should enumerate affected features by NAME, not
  narrative ("all 10 villain-derived features inherit" missed the
  4 blocker bypasses). New rule for reconciliation docs.
- Coaching/ duplicate is a project-wide hazard. After Stage 3.5,
  audit for other duplicate-file traps (e.g., `coaching/range_manager.py`).

## Immediate next action

Builder reads this reconciliation, then:

1. Acknowledge the 14 new MUSTs
2. Re-cut blueprint v2 addressing all of them (single artifact;
   replaces b1a9a91, do not patch in-place)
3. Confirm orchestrator decisions on the 4 owner-decision points
   (or flag specific ones for owner redirect)
4. Submit blueprint v2 for orchestrator review
5. Multi-agent reconciliation will run a second time on v2 if any
   MUST has CRITICAL ambiguity

No code edits, no model training, no teaching changes, no prompt
work until blueprint v2 passes its own reconciliation pass.

Go.
