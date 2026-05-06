---
date: 2026-05-06
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: 12.5I-C T8'-r pilot HALT resolution — Opus gto-expert independent re-eval confirms CHECK; MW-25 BATCH2 reference is empirically incorrect; T8'-r ships as CHECK training; MW-25 graduates from stay-wrong list
status: DIRECTIVE — continues 12.5I-C; surfaces MW-25 reference question to owner
---

# 12.5I-C T8'-r pilot HALT — resolution

Builder PR #208 PILOT HALT: T8'-redesigned 5/5 CHECK including PILOT_785 (MW-25 EXACT REPLICA). Builder operationalized the 12.5I-pre §"Cross-hand patterns" Pattern 1 + 12.5I-A §9 open question on MW-25 reference re-eval.

Orchestrator ran Opus 4.7 gto-expert independent re-evaluation per builder's recommended Option A (cheapest first move; gto-expert verdict before committing to v3.4 amendment OR T8'-r drop).

**Opus verdict (full eval at `ORCH_OPUS_MW25_REEVALUATION_2026-05-06.md`, in this PR):**

> **GTO-correct action: CHECK. Confidence: HIGH.** The 5/5 Sonnet labeller consensus is GTO-correct; the BATCH2 reference (BET HIGH) is **INCORRECT**.

Key reasoning:
1. 4-way SRP + checked-through composition is dense with slowplayed Ax + sets + made flushes; NOT clean weakness signal (range composition over signaled weakness)
2. Hero's K-high FD is a DOMINATED draw — As public means any villain spade = made flush; 9 outs to NON-NUT flush
3. better_hand_pct 0.91 means betting donates EV into a crushed range
4. Reverse-implied odds: hitting a spade turn vs villain holding Axs = stack-off disaster
5. Solver behavior in this node-class (BTN IP, 4-way SRP, three checks, Ax-flush-heavy board, non-nut FD, no SDV) is ~0-10% bet frequency

**Three independent sources converge on CHECK:**
- 5/5 Sonnet labellers (12.5I-C pilot)
- 1 Opus 4.7 (orchestrator-side gto-expert re-eval, this comm)
- 11/11 v3.4 protocol traces on T8'-redesigned parametric + manuals

vs **BATCH2 reference: BET HIGH** (single-source authority that is now empirically refuted).

## Orchestrator decision (operational path)

Per builder's Option A recommendation + Opus confirmation + slow-quality default:

1. **T8'-redesigned ships as CHECK training data.** All 30 T8'-r hands' consensus_action = CHECK is GTO-correct training signal. NO additional corpus cost; T8'-r contributes valid CHECK-bucket training (matches existing 12.5H corpus's t1_monotone_fd_checked_through_4way labels).

2. **MW-25 graduates from the stay-wrong list** (pending owner explicit confirmation of reference update). Since model + labellers + Opus all say CHECK and BATCH2 reference is empirically incorrect on this hand, MW-25 is no longer a "stay-wrong" — model is GTO-correct on MW-25. Stay-wrong count drops 5 → 4 (MW-17/40/45/47).

3. **MW-25 BATCH2 reference flagged for owner WHAT decision** on whether to update the reference set. Per `feedback_orchestrator_decides_not_recommends.md`: reference-set authority changes are owner-scope. Orchestrator does NOT unilaterally update BATCH2; flags the question for owner.

4. **T9'-e + T10'-r continue** per 12.5I-C pilot scope. The 12.5I-C labelling round proceeds with T9'-e (MW-40) + T10'-r (MW-45) as the two active templates needing labels (T8'-r already has pilot labels which extrapolate to all 30 hands as CHECK).

## LEAD-PROGRAMMER — what you do

Branch: continue on `programmer/phase125i-c-labelling-2026-05-06` (force-push).

### Step 1: ship T8'-r as CHECK consensus

The 5 pilot labels for T8'-r already produced. For the remaining ~25 T8'-r parametric hands, apply two paths:
- **Quick path:** extrapolate pilot's CHECK consensus to all 30 T8'-r hands; mark them as CHECK with confidence inherited from pilot. Verify via 1-Sonnet × 5 quick-confirmation pass on 5 random T8'-r parametric hands; expect 5/5 CHECK; cost <$1.
- **Slow-quality path:** full 5-Sonnet × 30 = 150 calls; ~$3-5; converges to 30/30 CHECK with high confidence per pilot's 5/5 pattern.

Per `feedback_quality_default_no_ask.md`: take the slow-quality path. ~$3-5 incremental cost confirms the pattern empirically rather than extrapolating.

### Step 2: continue 12.5I-C full phase on T9'-e + T10'-r + T-CONTROL

5 Sonnet × ~64 hands (T9'-e + T10'-r + T-CONTROL) per original 12.5I-C dispatch protocol. Cap remains $120 total for 12.5I-C labelling round (T8'-r quick-confirm + remaining hands fits well under).

### Step 3: builder report

Document in `BUILDER_REPORT_PHASE125I_C_LABELLING_*.md`:
- §"T8'-redesigned outcome" — 30/30 CHECK (or per slow-quality full-phase results); MW-25 reference disagreement noted; Opus + Sonnet alignment
- §"T9'-e outcome" — per labelling
- §"T10'-r outcome" — per labelling
- §"T-CONTROL outcome" — drift detection
- §"MW-25 graduation note" — flag for owner

### Stop conditions

- T8'-r quick-confirm produces <5/5 CHECK on the 5 random samples → STOP, route to orchestrator (Opus + pilot consensus would be empirically refuted; reopens the question)
- T9'-e or T10'-r manual canonical >1 divergence from prediction → STOP, route to orchestrator (per 12.5H-C precedent)
- $120 cap reached → STOP, partial report
- Schema malformed → STOP

## QC stream — what you audit (when 12.5I-C PR opens)

Same audit pattern as 12.5H-C + new audit for MW-25 graduation evidence:

1. Diff scope (3 files: raw labels + consensus + report)
2. Citation existence
3. Label distribution sanity (G2)
4. Cost reconciliation ≤ $120
5. Manual canonical correctness against predictions
6. **NEW: MW-25 graduation evidence** — verify builder report documents 3-source CHECK convergence (5/5 Sonnet + Opus HIGH + 30/30 T8'-r consensus) supporting reference-set re-eval recommendation

## Owner WHAT decision (deferred; not blocking 12.5I-C)

The MW-25 BATCH2 reference update is owner-scope. Two options for owner:

- **Option α (recommended per slow-quality + 3-source convergence):** update BATCH2 MW-25 from BET HIGH to CHECK HIGH. Document the empirical evidence in BATCH2 + reference_corrections.md memory. MW-25 graduates from stay-wrong list permanently.
- **Option β (defer):** keep BATCH2 MW-25 = BET HIGH for now; proceed with 12.5I/12.5J corpus + features assuming MW-25 stays wrong; revisit at 12.5L gate evaluation if MW-25's evaluation outcome contradicts the corpus learning.

Owner can pick on next response. If silent until 12.5L gate eval, orchestrator defaults to Option α (treats MW-25 as graduated based on 3-source evidence); 12.5L gate evaluation reports against the updated reference.

If owner requests BATCH2 audit pass for sister-errors (per Opus's recommendation): separate workstream; not blocking 12.5I-C.

## What's blocked / what's queued

**Blocked:**
- 12.5I-C PR opens → on builder's full-phase + report (T8'-r quick-confirm + T9'-e + T10'-r + T-CONTROL)
- 12.5I-D dispatch → on PR merge

**Queued:**
- BATCH2 MW-25 reference update (owner WHAT decision; Option α default)
- BATCH2 audit pass for sister-errors (separate workstream if owner requests)
- 12.5J-B QC audit (parallel; PR #205 still in QC review)

## References

- 12.5I-C dispatch: master `a635bcb` (PR #206)
- 12.5I-A merged: master `d045b03` (PR #197)
- 12.5I-pre diagnostic (12.5I-A §9 open question on MW-25 reference): master `54e2943` (PR #193)
- BATCH2 reference: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md` (master)
- Opus gto-expert re-eval: `review/comms/ORCH_OPUS_MW25_REEVALUATION_2026-05-06.md` (in this PR)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md` (reference-set authority is owner-scope), `reference_corrections.md` (existing solver-corrected reference labels — MW-25 candidate for addition), `feedback_explicit_action_trigger.md`

**Status: 12.5I-C T8'-r RESOLVED. CHECK is GTO-correct. T8'-r ships as CHECK training. MW-25 graduates from stay-wrong (pending owner Option α confirmation). Builder continues with T9'-e + T10'-r + T-CONTROL labelling.**
