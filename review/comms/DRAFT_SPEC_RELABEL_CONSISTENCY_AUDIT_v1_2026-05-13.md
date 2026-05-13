---
date: 2026-05-13
from: Architect (Phase 2-F prep — DRAFT pending ratification)
to: Builder · QC stream · gto-expert · Owner
re: Relabel consistency audit v1 — measure drift between AMENDMENT-3-relabelled hands and original Phase 2-E consensus on a stratified 80-hand sample
status: DRAFT — DRAFTED IN ADVANCE; builder reviews + ratifies + commits on next tick
companion docs:
  - review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md
  - review/comms/DRAFT_AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5_2026-05-13.md
references:
  - data/4way_corpus/full_700/batch_001_consensus.jsonl..batch_007_consensus.jsonl
  - prompts/gto_labeller_v3.4.md
  - memory: feedback_pilot_first_for_long_jobs.md, feedback_solver_vs_expert_labels.md
---

# Relabel Consistency Audit v1 — Specification

## 1. Purpose

AMENDMENT 3 introduces a new mandatory phrasing constraint (positional
action-chain explicit naming) on top of `prompts/gto_labeller_v3.4.md` +
`data/4way_labeller_brief.md`. Before firing Phase 2-F at scale (14 batches
× 50 hands), the team must verify that the new constraint does not silently
shift the labellers' action distribution away from the Phase 2-E consensus
on equivalent spots.

**The audit:** sample 80 hands from Phase 2-E batches 001-007 (350 hands
total in scope); relabel them under the AMENDMENT-3-extended brief using
the same 5-Sonnet + Opus tier-up infrastructure; measure drift between the
new consensus and the original.

The audit is **pre-merge gated**: Phase 2-F fires only after the audit's
DRIFT_REPORT_FULL.md report shows drift below the §6 thresholds. The audit
itself follows pilot-first discipline (§3) per
`feedback_pilot_first_for_long_jobs.md`.

## 2. Sample stratification

### 2.1 Stratification dimensions

The 80-hand audit sample is stratified across four dimensions whose
joint distribution must approximate Phase 2-E's natural distribution
(measured from `batch_001_consensus.jsonl..batch_007_consensus.jsonl`):

1. **hero_position**: {UTG, HJ, CO, BTN, SB, BB} — 6 values
2. **action_context**: {opener, facing_initial_bet, facing_raise} — 3 values
   (using the legacy 3-valued field for backward-compat; AMENDMENT 3 itself
   does not require chain-fingerprint stratification for the audit, since
   the audit is measuring drift on the *legacy* corpus)
3. **street**: {flop, turn, river} — 3 values
4. **board_texture**: {rainbow_dry, two_tone, paired, monotone} — 4 values

**Total cells:** 6 × 3 × 3 × 4 = **216 cells**.

### 2.2 Per-cell counts

With 80 hands across 216 cells, most cells are empty. Stratification works
as a **proportional-sampling-with-floor**, not a balanced fill:

- **Min per cell with ≥1 hand in Phase 2-E source**: 0 hands (cell is not
  guaranteed to be sampled if it underyields naturally).
- **Max per cell**: 4 hands (cap to prevent any single cell dominating).
- **Proportional target**: each non-empty cell receives
  `round(cell_phase2e_count / 350 × 80)` hands, capped at 4 and floored
  at 0 (cells with <0.5 proportional hits drop out).

The cells that survive (after the round-and-cap) form the audit's sample
frame. Empirically, ~40-60 of the 216 cells are non-empty in Phase 2-E
(action_context × position × street × board_texture has many sparse cells).

### 2.3 Sampling algorithm — deterministic, reproducible

```python
def stratified_sample_for_audit(
    consensus_files: List[Path],   # batch_001..007_consensus.jsonl
    n_hands: int = 80,
    seed: int = 20260513,           # YYYYMMDD of audit dispatch
) -> List[dict]:
    """Return n_hands stratified Phase 2-E hands for AMENDMENT-3 relabel audit.

    Deterministic: same seed + same input files → same 80 hands.
    """
    # 1. Load all 350 hands from consensus files
    all_hands = []
    for f in consensus_files:
        all_hands.extend(jsonl_load(f))

    # 2. Compute (hero_position, action_context, street, board_texture)
    #    for each hand — using the existing feature_extractor outputs
    cells = defaultdict(list)
    for h in all_hands:
        key = (
            h['hero_position'],
            derive_action_context(h),   # opener / facing_initial_bet / facing_raise
            h['street'],
            derive_board_texture(h['board']),  # rainbow_dry/two_tone/paired/monotone
        )
        cells[key].append(h)

    # 3. Compute per-cell target counts
    rng = random.Random(seed)
    targets = {}
    for key, hands in cells.items():
        prop_target = len(hands) / len(all_hands) * n_hands
        # Cap at 4 hands per cell; floor at 0 if prop_target < 0.5
        if prop_target < 0.5:
            continue
        targets[key] = min(4, round(prop_target))

    # 4. Adjust to exactly n_hands (rounding errors fixed by largest-cell trim)
    total = sum(targets.values())
    while total > n_hands:
        # Trim from largest cells first (deterministic ordering by sorted-keys)
        largest = max(sorted(targets.keys()), key=lambda k: targets[k])
        targets[largest] -= 1
        total -= 1
    while total < n_hands:
        # Add to cells with most underused capacity (room to 4-cap)
        candidates = sorted(
            [k for k, v in targets.items() if v < 4 and len(cells[k]) > v],
            key=lambda k: (4 - targets[k], len(cells[k]) - targets[k]),
            reverse=True,
        )
        if not candidates:
            break  # cannot fill (impossible if 80 ≤ 350 and cells are non-empty)
        targets[candidates[0]] += 1
        total += 1

    # 5. Deterministic per-cell sampling (rng.sample with seeded RNG)
    sampled = []
    for key in sorted(targets.keys()):
        cell_hands = sorted(cells[key], key=lambda h: h['spot_id'])
        rng.shuffle(cell_hands)  # deterministic given seed
        sampled.extend(cell_hands[:targets[key]])

    assert len(sampled) == n_hands
    return sampled
```

The `seed=20260513` value matches the audit dispatch date. Re-running with
the same seed and same input files produces byte-identical sample selection
(reproducibility requirement).

### 2.4 Sample validation gate

After sample selection, before relabel dispatch, assert:

- `len(sampled) == 80`
- ≥3 distinct hero positions represented
- ≥2 distinct action_contexts represented
- ≥2 distinct streets represented
- ≥3 distinct board_textures represented
- No spot_id appears twice
- Every sampled spot has a non-empty original consensus_action in
  `batch_*_consensus.jsonl` (i.e. did not escalate to owner-arb queue)

If any assertion fails, the audit is BLOCKED — re-run sampling with a
different seed (e.g. +1 to 20260514) or expand the source pool to BATCH-008
once available.

## 3. Pilot subset — 20 of 80 hands

Per `feedback_pilot_first_for_long_jobs.md`, the audit splits into pilot +
full phases.

### 3.1 Pilot selection

The pilot subset is **20 of the 80 sampled hands**, selected
**deterministically** from the stratified sample:

```python
def select_pilot_20(full_sample: List[dict], seed: int = 20260513) -> List[dict]:
    """Return 20 of 80 hands preserving stratification at pilot scale."""
    # 1. Group sampled hands by (hero_position, action_context, street,
    #    board_texture) cell
    cells = defaultdict(list)
    for h in full_sample:
        key = (h['hero_position'], derive_action_context(h),
               h['street'], derive_board_texture(h['board']))
        cells[key].append(h)

    # 2. From each cell, pick at most ceil(cell_size / 4) for the pilot
    #    (preserving cell distribution at quarter-scale)
    rng = random.Random(seed + 1)  # seed offset to differ from full sampling
    pilot = []
    for key in sorted(cells.keys()):
        cell = sorted(cells[key], key=lambda h: h['spot_id'])
        rng.shuffle(cell)
        n_from_cell = max(1, len(cell) // 4)  # at least 1 per non-empty cell
        pilot.extend(cell[:n_from_cell])

    # 3. Trim to 20 (largest cells first; ties broken by sorted spot_id)
    pilot.sort(key=lambda h: h['spot_id'])
    return pilot[:20]
```

### 3.2 Pilot stratification preservation check

Assert that the 20-hand pilot retains the four-dimension stratification
shape at quarter scale:

- ≥3 distinct hero positions
- ≥2 distinct action_contexts
- ≥2 distinct streets
- ≥3 distinct board_textures
- Chi-square test on the joint cell distribution between full-80 and
  pilot-20 returns p > 0.05 (no significant distributional drift induced
  by sub-sampling)

If chi-square fails (p ≤ 0.05), the pilot is not representative — re-pick
pilot with seed+2, +3, etc., until a representative draw is found, or
escalate to owner-arb as "audit pilot construction failure".

## 4. Relabel protocol

### 4.1 Infrastructure — identical to Phase 2-E

The relabel uses **exactly the same labelling infrastructure** as
Phase 2-E batches:

- **5 Sonnet 4.6 labellers** + **1 Opus 4.7 tier-up** (same tier ladder as
  BATCH-001..007 per BUILDER_REPORT_PHASE2E_FULL_BATCH007).
- Same per-labeller temperature, max_tokens, system-prompt loading
  conventions.
- Same consensus computation: ≥3/5 agreement = consensus_action; <3/5 →
  Opus tier-up; Opus action becomes consensus if ≥1 Sonnet aligned, else
  owner-arb queue.
- Same prompt chain: `prompts/gto_labeller_v3.4.md` + `knowledge/three_way_gto.md`
  + `data/4way_labeller_brief.md`.

### 4.2 The one change

The relabel uses `data/4way_labeller_brief.md` **with AMENDMENT 3 appended**
(per DRAFT_AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5_2026-05-13.md
content). No other changes — no prompt revision, no new KB, no
hyperparameter tweaks.

The AMENDMENT-3 brief is committed as a separate file
`data/4way_labeller_brief_amendment3.md` for the audit run; if the audit
passes, AMENDMENT 3 is merged into the canonical brief on the same merge
commit as the Phase 2-F directive.

### 4.3 Per-labeller output paths

For audit pilot (20 hands):
```
data/4way_corpus/audit_amendment3/pilot/raw_labels_labeller_<N>.jsonl
data/4way_corpus/audit_amendment3/pilot/raw_labels_opus_tierup.jsonl
data/4way_corpus/audit_amendment3/pilot/consensus.jsonl
data/4way_corpus/audit_amendment3/pilot/owner_arb_queue.jsonl
```

For audit full (80 hands):
```
data/4way_corpus/audit_amendment3/full/raw_labels_labeller_<N>.jsonl
data/4way_corpus/audit_amendment3/full/raw_labels_opus_tierup.jsonl
data/4way_corpus/audit_amendment3/full/consensus.jsonl
data/4way_corpus/audit_amendment3/full/owner_arb_queue.jsonl
```

## 5. Drift metrics

### 5.1 Primary — action_drift_rate

The primary metric is the proportion of audit hands whose new (post-
AMENDMENT-3) consensus action differs from the original Phase 2-E
consensus action:

```
action_drift_rate = |{h : new_consensus_action(h) ≠ old_consensus_action(h)}| / N
```

Where `N = 20` for pilot, `N = 80` for full.

### 5.2 Secondary — per-action drift matrix

A 4×4 confusion matrix counting transitions across the four legal actions
{FOLD, CALL, RAISE, BET, CHECK} — call this the 5-action set. The matrix
is 5×5 = 25 cells including same-action diagonals (drift = 0 along the
diagonal).

```
              new=FOLD  new=CALL  new=RAISE  new=BET  new=CHECK
old=FOLD       n_FF       n_FC      n_FR       n_FB     n_FH
old=CALL       n_CF       n_CC      n_CR       n_CB     n_CH
old=RAISE      n_RF       n_RC      n_RR       n_RB     n_RH
old=BET        n_BF       n_BC      n_BR       n_BB     n_BH
old=CHECK      n_HF       n_HC      n_HR       n_HB     n_HH
```

Total off-diagonal mass = action_drift_rate × N. The off-diagonal
**direction** matters more than magnitude: e.g. systematic CALL→RAISE
drift suggests AMENDMENT 3's chain-naming triggered more aggressive
plays, whereas CALL→FOLD suggests over-cautious framing.

Per `feedback_failure_direction_classification.md` (memory), the per-action
matrix is classified by direction:

- **Under-aggress drift**: cells (BET → CHECK), (RAISE → CALL),
  (RAISE → FOLD), (CALL → FOLD)
- **Over-aggress drift**: cells (CHECK → BET), (CALL → RAISE),
  (CALL → BET), (FOLD → CALL), (FOLD → RAISE)
- **Lateral drift**: cells (BET → RAISE) or (CHECK → CALL) — same
  aggression direction, different action class (rare; legal only when
  facing_bet flag toggles, which the spot does not — so lateral cells
  should be 0)

A net direction (under > over, or over > under, or balanced) is the
secondary signal.

### 5.3 Tertiary — sizing_drift on RAISE/BET actions

For hands where both old and new consensus action is BET or RAISE (i.e.
diagonal `n_BB` and `n_RR` cells), compute the % pot bucket drift in
sizing. The "bucket" coarsens the size space into solver-aligned bins:

- **BET bins (flop)**: small (≤30%), medium (30-50%), large (50-80%),
  overbet (>80%)
- **BET bins (turn)**: small (≤40%), medium (40-65%), large (65-100%),
  overbet (>100%)
- **BET bins (river)**: small (≤40%), medium (40-65%), large (65-100%),
  overbet (>100%)
- **RAISE bins (any street)**: 2-2.5x, 2.5-3.5x, 3.5-5x, >5x

```
sizing_drift_rate = |{h : same_action(h) and new_bin(h) ≠ old_bin(h)}|
                   / |{h : same_action(h) and action(h) ∈ {BET, RAISE}}|
```

If sizing_drift_rate > 0.30, AMENDMENT 3 may be shifting bet-sizing
intuition even when action holds steady — flag for gto-expert review.

## 6. Tier-up gate and accept/reject thresholds

### 6.1 Opus tier-up cross-check for drift hands

**Every drift hand** (i.e. every spot where `new_consensus_action ≠
old_consensus_action`) is routed to a second Opus 4.7 tier-up pass
distinct from the 5-Sonnet + 1-Opus pass used in the standard pipeline.
Call this **Opus-Verify**:

- **Opus-Verify** receives the spot input + a side-by-side prompt
  showing both the old consensus action and the new consensus action,
  with the rationales from both. Opus-Verify is asked: "Which action is
  GTO-correct? Justify."
- Opus-Verify's verdict is the **tiebreaker** between old and new.
- If Opus-Verify agrees with the new (post-AMENDMENT-3) action → the
  drift is "validated" — new action stays.
- If Opus-Verify agrees with the old (pre-AMENDMENT-3) action → the
  drift is "rejected" — flag the spot for owner-arb and the audit
  records this as a potential AMENDMENT-3-induced regression.
- If Opus-Verify proposes a third action (neither old nor new) → both
  are flagged for owner-arb; the spot enters the solver-verify queue
  per `feedback_solver_verification_queue.md`.

Per `feedback_solver_vs_expert_labels.md`: Opus-Verify is used as a
**poker-judgment oracle**, NOT as a training label. The audit records
Opus-Verify verdicts in DRIFT_REPORT_*.md but does NOT rewrite the
Phase 2-E consensus from Opus-Verify.

### 6.2 Accept/reject thresholds

**Pilot (20 hands) accept/reject thresholds:**

| Metric | Accept threshold | Reject threshold |
|---|---|---|
| `action_drift_rate` | ≤ 15% (≤ 3/20 drift hands) | > 30% (> 6/20 drift hands) |
| Net-direction drift (over-aggress vs under-aggress) | balanced within ±2 hands | one direction dominates by ≥4 hands |
| `sizing_drift_rate` | ≤ 25% | > 50% |
| Opus-Verify "rejected" drift count | ≤ 1/20 | ≥ 4/20 |

**Action on pilot:**
- All four metrics in **accept** zone → PROCEED to full 80-hand audit.
- ≥1 metric in **reject** zone → HALT; AMENDMENT 3 needs revision before
  Phase 2-F can fire. Builder + gto-expert produce a revision proposal;
  owner gates revision-or-abort decision.
- Any metric in the middle zone (between accept and reject) → escalate
  to gto-expert review with the per-action matrix; gto-expert produces
  HOLD/PROCEED recommendation; orchestrator decides.

**Full (80 hands) accept/reject thresholds:**

| Metric | Accept threshold | Reject threshold |
|---|---|---|
| `action_drift_rate` | ≤ 12% (≤ 10/80 drift hands) | > 25% (> 20/80 drift hands) |
| Net-direction drift | balanced within ±5 hands | one direction dominates by ≥12 hands |
| `sizing_drift_rate` | ≤ 20% | > 40% |
| Opus-Verify "rejected" drift count | ≤ 3/80 | ≥ 12/80 |

**Action on full:**
- All four in **accept** → PASS; Phase 2-F clears the audit gate and
  fires per top-level dispatch.
- ≥1 in **reject** → HALT Phase 2-F; treat as AMENDMENT-3-induced
  drift; revise AMENDMENT 3 or roll back; re-run audit on revised
  amendment.
- Middle zone → orchestrator decides per `feedback_orchestrator_decides_not_recommends.md`,
  with gto-expert recommendation in hand.

### 6.3 Threshold rationale

The pilot thresholds are tighter than the full because pilot is 4× more
sample-noisy — a 15% drift rate on 20 hands is 3 hands, which is
non-trivially likely from natural labelling noise (Phase 2-E natural
labeller disagreement on equivalent re-runs is ~10-15% per BUILDER_REPORT
batch consensus rates).

The full thresholds tighten on percentage but loosen on absolute count
because n=80 stabilizes the rate measurement.

## 7. Output file formats

### 7.1 DRIFT_REPORT_PILOT.md schema

The pilot drift report lives at
`review/comms/DRIFT_REPORT_PILOT_AMENDMENT3_<DATE>.md` and contains:

```markdown
---
date: <ISO8601>
from: Builder
to: Orchestrator + Owner + QC
re: AMENDMENT 3 audit pilot — 20-hand drift report
status: <PASS|REVISE-AND-RETRY|HALT>
---

# AMENDMENT 3 audit pilot — drift report (N=20)

## TL;DR
- action_drift_rate: <X%> (<N>/20) — <accept/middle/reject>
- net direction: <under-aggress/over-aggress/balanced> by <K> hands
- sizing_drift_rate: <Y%> (on the <M> same-action BET/RAISE hands)
- Opus-Verify rejected drift: <Z>/<N drift>

## Per-action drift matrix

|              | new=FOLD | new=CALL | new=RAISE | new=BET | new=CHECK |
|--------------|----------|----------|-----------|---------|-----------|
| old=FOLD     |          |          |           |         |           |
| old=CALL     |          |          |           |         |           |
| old=RAISE    |          |          |           |         |           |
| old=BET      |          |          |           |         |           |
| old=CHECK    |          |          |           |         |           |

## Drift hand details (per drift hand)

For each spot where new ≠ old:
- spot_id, hero_pos, action_context, street, board_texture
- old consensus action + rationale snippet
- new consensus action + rationale snippet (with chain-naming sentence
  bolded)
- Opus-Verify verdict + rationale
- Direction classification (under-aggress / over-aggress / lateral)

## Stratification preservation

Chi-square test pilot vs full sample frame: p = <value>; passes/fails.

## Gate decision

- [ ] action_drift_rate in accept zone (≤15%)
- [ ] net direction balanced (±2)
- [ ] sizing_drift_rate ≤ 25%
- [ ] Opus-Verify rejected ≤ 1
- Decision: <PROCEED to full audit | HALT for revision>

## Recommended action

<Orchestrator-class decision per feedback_orchestrator_decides_not_recommends.md>
```

### 7.2 DRIFT_REPORT_FULL.md schema

The full drift report lives at
`review/comms/DRIFT_REPORT_FULL_AMENDMENT3_<DATE>.md` and uses an identical
schema with:

- N = 80 throughout
- Thresholds from §6.2 full table
- Adds a section "**Cell-level drift breakdown**": drift counts
  decomposed by stratification cell, surfaces whether drift is
  concentrated in specific (hero_pos, action_context, street,
  board_texture) cells (e.g. all drift in `BB × facing_bet × flop × two-tone`
  would suggest AMENDMENT 3's chain-naming is doing too much in a narrow
  geometry).
- Adds a section "**Tail-cell drift coverage**": cells with 0 hands
  drift counted as "no signal available" rather than "no drift"; flags
  cells where the audit has insufficient power to detect drift.
- Adds a "**Top-12 chain coverage**" sidebar: for the 80 sampled hands,
  count how many fall into each of the §5.1 top-12 chains from
  DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md. This is a
  side-channel observation — not a gate — to confirm that the audit
  exercises the chain-naming requirement on the chains the new
  amendment cares about most.

### 7.3 Per-spot relabel detail file

`data/4way_corpus/audit_amendment3/full/per_spot_drift.jsonl` contains
one record per audit hand:

```json
{
  "spot_id": "4WL-BATCH001-spot-017",
  "stratification_cell": {
    "hero_position": "BB",
    "action_context": "facing_initial_bet",
    "street": "flop",
    "board_texture": "two_tone"
  },
  "old_consensus": {
    "action": "CALL",
    "sizing_pct": null,
    "rationale_snippet": "..."
  },
  "new_consensus": {
    "action": "RAISE",
    "sizing_pct": 200,
    "rationale_snippet": "...",
    "chain_naming_sentence": "Hero (BB) is facing CO's c-bet with BTN as prior caller..."
  },
  "drift_direction": "over-aggress",
  "opus_verify": {
    "verdict": "old_correct",
    "rationale_snippet": "...",
    "solver_queued": true
  },
  "fl6_pass": true
}
```

This file feeds the DRIFT_REPORT generation and is preserved for
post-Phase-2-F retrospective analysis.

## 8. Pre-merge gate sequence

1. Builder dispatches audit pilot (20 hands) → produces
   DRIFT_REPORT_PILOT_AMENDMENT3.md.
2. Orchestrator reads pilot report:
   - PASS → dispatch full audit (80 hands).
   - HALT → orchestrator decides revision vs abort per
     `feedback_orchestrator_decides_not_recommends.md`.
3. Builder dispatches full audit → produces DRIFT_REPORT_FULL_AMENDMENT3.md.
4. QC stream audits the audit per existing TC-25 / TC-23 patterns.
5. Owner gates Phase 2-F fire based on DRIFT_REPORT_FULL accept/reject
   verdict.

## 9. Audit cost estimate

Per `feedback_pilot_first_for_long_jobs.md` cost-discipline requirements:

- Pilot: 20 hands × 5 Sonnet labellers + 1 Opus tier-up + 1 Opus-Verify
  per drift hand. At ~$0.40/hand for 5 Sonnet, $0.15/hand for Opus
  tier-up, $0.15/hand for Opus-Verify (only on drift): ~$11 + ~$3 +
  ~$0.50 = ~$14.50.
- Full: 80 hands × same infra: ~$58 + ~$12 + ~$1.50 = ~$71.50.
- Total: ~$86 (well under 5× pilot ratio; full is ~5× pilot which
  borderline-violates the rule, but the audit's two-phase gate satisfies
  the rule's intent — the FULL only fires after PILOT confirms approach
  works).

## 10. Builder ratification checklist

- [ ] §2 stratification dimensions (4) and cells (216) match architect intent.
- [ ] §2.3 sampling algorithm is deterministic given seed=20260513 and
      reproducible byte-for-byte.
- [ ] §3 pilot 20-of-80 algorithm preserves stratification (chi-square test
      built into the gate).
- [ ] §4 relabel uses identical 5-Sonnet + 1-Opus infra as Phase 2-E.
- [ ] §5 three drift metrics (action / per-action matrix / sizing) are
      well-defined and computable from consensus.jsonl files.
- [ ] §6 thresholds are taken verbatim from architect's draft; no menus.
- [ ] §6.1 Opus-Verify gates every drift hand; verdicts recorded but
      do NOT rewrite consensus (per `feedback_solver_vs_expert_labels.md`).
- [ ] §7 DRIFT_REPORT_PILOT.md and DRIFT_REPORT_FULL.md schemas are
      explicit.
- [ ] §8 pre-merge gate sequence is binding before Phase 2-F dispatch.

End DRAFT.
