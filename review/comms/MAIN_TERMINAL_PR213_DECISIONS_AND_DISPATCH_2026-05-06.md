---
date: 2026-05-06
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: PR #213 BORDERLINE-17 resolution — orchestrator quality-default decisions on all 3 coupled WHAT items per `feedback_quality_default_no_ask.md` 4th restatement; merge PR #213/#215 and dispatch BATCH2 MW-25 update + queue MW-40 verification round + 12.5I-D + 12.5J-D-pre
status: DIRECTIVE — merges PR #213 + #215; dispatches LEAD-PROGRAMMER for BATCH2 MW-25 update PR
---

# PR #213 — orchestrator quality-default decisions

Owner restated standing rule (4th time across sessions, latest 2026-05-06): "please recommend the best quality focused decision, slow and steady we have all the time. please always do this approach without asking. this should be a rule." Memory `feedback_quality_default_no_ask.md` updated with the restatement + new anti-pattern. Per the rule: orchestrator decides + executes; owner overrides on read.

## Decisions made (quality defaults applied)

### Decision 1 — PR #213 disposition: α (merge as-is)

**Reasoning:** Opus's tier-up explicitly recommends accept-with-caveat. The 3 mix-frequency labels at 0.6 confidence are not noise to discard — they encode the *real* GTO mixed-strategy property of T-kicker TPMK in 4-way checked-through SRP. Dropping them (β) discards the signal that the model SHOULD learn (mixed strategies are real GTO). Redesign (γ) is over-engineered: the disagreement subzone is narrow and identifiable (T-kicker / A-high or K-high / 4-way checked-through / IP non-PFA), addressable via attention vocab in 12.5J or 12.5L per `feedback_attention_flags_when_features_change.md`. The 0.6 confidence sample-weighting is the natural slow-quality calibration; trust the ensemble's encoded uncertainty.

**Action:** merge PR #213 + PR #215.

### Decision 2 — MW-25 BATCH2 reference update: α (lock CHECK HIGH)

**Reasoning:** 4-source convergence + 30-hand 100% unanimous parametric. Overwhelming. Has been silent-default since 08:16 SAST per PR #209. Deferring to 12.5L (β) creates a known-wrong-reference footnote in 12.5I-D corpus QC — that's quality loss, not gain. Reference accuracy = single-hand correctness; we have 4 independent verifications on the exact hand (Ks7s on As9s5d 4-way checked-through-multiway).

**Action:** dispatch LEAD-PROGRAMMER to author BATCH2 + reference_corrections.md update PR (this comm § "LEAD-PROGRAMMER step 1").

### Decision 3 — MW-40 BATCH2 reference update: β (defer; queue parametric verification round)

**Reasoning:** 3 sources on PILOT_787 (Sonnet 3-2 + Opus HIGH + structural composition argument) is meaningful but does not yet meet the slow-quality bar set by MW-25's 4-source + 30-hand parametric pattern. Per `feedback_quality_default_no_ask.md` "fewer-dry-runs vs more-dry-runs → pick more-dry-runs" + "add one more gate". We have time. Cost of the verification round (~$10-15 + 1-2 hours wall clock) is small relative to the cost of locking a wrong reference. The structural argument (J-on-board flips composition triple) is a *prediction* about all J-on-board TPMK 4-way checked-through hands; the parametric round tests that prediction empirically before committing the reference update.

The verification round design: ~30 J-on-board parametric variants (4-way checked-through, IP non-PFA, varying kickers and J-board textures) → 5 Sonnet × 30 → Opus tier-up on key canonicals. If 30/30 (or ≥27/30) CHECK consensus → MW-40 graduates with the same evidence pattern as MW-25. If <27/30 → structural argument is too narrow; MW-40 stays wrong; PILOT_787 stays as a single anomaly.

**Action:** queue 12.5I-MW40-VERIFICATION mini-phase (separate dispatch comm after BATCH2 MW-25 update merges).

## Sequencing — what fires when

The merges and dispatches are partially ordered. Builder is one party (per `feedback_river_rats_team_structure.md`); workstreams sequence through builder serially.

| # | Action | Party | Status / Trigger |
|---|---|---|---|
| 1 | Merge PR #213 + PR #215 | Orchestrator | **NOW** (this comm merges) |
| 2 | BATCH2 MW-25 update PR | LEAD-PROGRAMMER | **fire on this comm merge** (Step 1 below) |
| 3 | QC audit on PR step 2 | QC stream | post-PR-open by orchestrator trigger |
| 4 | 12.5I-D corpus QC dispatch | LEAD-PROGRAMMER | post step 2 merge |
| 5 | 12.5I-MW40-VERIFICATION-A design dispatch | LEAD-PROGRAMMER | post step 2 merge |
| 6 | 12.5J-D-pre test-guard deflake | LEAD-PROGRAMMER | post step 4 merge (parallel queue with step 5) |

Builder serial execution: step 2 → step 4 (12.5I-D) → step 5 (MW-40-A design) → step 6 (12.5J-D-pre). Each step opens its own PR; orchestrator triggers QC + tier-up + merges per loop protocol.

## LEAD-PROGRAMMER — Step 1: BATCH2 MW-25 update PR (fire now on this comm merge)

Branch: `programmer/batch2-mw25-graduation-update-2026-05-06`. Base: master post-this-comm-merge (will include PR #213 + #215 merged).

### Files to edit (3)

1. **`design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`** — MW-25 entry:
   - Change `expert_action: BET HIGH` → `expert_action: CHECK HIGH`
   - Change `expert_reasoning:` block to reflect the empirical evidence:
     > "Updated 2026-05-06 per 4-source convergence: 5/5 12.5I-C pilot CHECK + Opus 4.7 gto-expert HIGH (PR #209) + 30/30 12.5I-C parametric step-1 unanimous CHECK 1.0 conf + v3.4 protocol traces (KB §1.7 + DO NOT Rule 2). The original BET HIGH expert action did not adequately weight: (a) hero K-high FD is non-nut (As public on board → no nut blocker), (b) 4-way checked-through composition contains slowplayed Ax + sets + made flushes (better_hand_pct=0.80 dominates), (c) reverse-implied odds 3+ way punish drawing-equity bets, (d) 4-way collective fold equity collapses below thin-value-bet break-even. CHECK HIGH preserves equity realization while avoiding stack-off scenarios."
   - Update `expert_action_history:` (or add if absent) with: `2026-05-06: BET HIGH → CHECK HIGH (4-source graduation, PR #209 + PR #213)`

2. **`design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`** (if MW-25 has a range-analysis section — check; if absent, skip) — update commentary on MW-25 to reflect new action.

3. **`/home/rupertbeytell/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`** — add MW-25 entry:
   ```
   ## MW-25 (Ks7s on As9s5d, 4-way checked-through multiway, BTN IP, BB+CO+HJ checked through)
   - Original BATCH2 expert action: BET HIGH
   - Corrected action: CHECK HIGH
   - Date corrected: 2026-05-06
   - Evidence sources: (1) 12.5I-C pilot 5/5 CHECK (PR #208), (2) Opus 4.7 gto-expert independent re-eval CHECK HIGH (PR #209), (3) 12.5I-C step-1 30/30 unanimous CHECK 1.0 conf (PR #213), (4) v3.4 protocol traces (KB §1.7 + DO NOT Rule 2)
   - Stay-wrong list: graduates (5 → 4 hands remaining: MW-17, MW-40, MW-45, MW-47)
   ```

### Optional file (DO NOT touch unless asked)

- `prompts/gto_labeller_v3.4.md` — protocol is correct; no change needed
- Stay-wrong list lives in `review/RESTART_PROMPT_V9_3WAY.md` per CLAUDE.md — update IF that file currently lists MW-25; otherwise skip (orchestrator can also handle in a later session-state update)

### Builder report

`review/comms/BUILDER_REPORT_BATCH2_MW25_GRADUATION_2026-05-06.md`:
- §"Files edited" — exact diff scope
- §"Verification" — diff against `feedback_orchestrator_decides_not_recommends.md` § "owner-scope" — confirm only the 2-3 files above are touched, no v3.x prompts or training-data files
- §"Stay-wrong list state" — note 5 → 4 graduation
- §"References" — link back to PR #209 + PR #213 + PR #215 evidence

### Stop conditions

- Touching v3.x prompts or training data → STOP (out of scope)
- BATCH2_8_HAND_DESIGNS.md MW-25 entry not found at expected path → STOP (route to orchestrator for path verification)
- reference_corrections.md edit conflicts with existing memory entries → STOP

### Cost / time

~$0.10 (text edits, no LLM calls beyond this). ~15 min builder time.

## QC stream — what you audit (when step 2 PR opens)

Standalone audit pattern per `feedback_qc_routing_when_standalone_active.md`. New audit class: TC-X-OWNER-SCOPE-DISCIPLINE (per QC's PR #213 audit observation, formalize as test class):

1. **Diff scope strict** — exactly the 2-3 files in step 2 above. No drift outside scope. v3.x prompts UNTOUCHED. Training-data jsonl files UNTOUCHED.
2. **Citation existence** — BATCH2 MW-25 entry's new `expert_reasoning` cites the 4 evidence sources by PR #.
3. **reference_corrections.md format** — entry follows the standing format (hand description + original action + corrected action + date + sources + stay-wrong status).
4. **Stay-wrong list integrity** — if RESTART_PROMPT_V9_3WAY.md was edited, MW-25 removed; otherwise note as deferred.

QC writes `review/comms/REVIEW_QC_BATCH2_MW25_GRADUATION_2026-05-06.md`. PR opens. Orchestrator merges on PASS.

## Why no QC tier-up here

This is a doc + memory update, not training-data or model code. Per `feedback_pilot_first_for_long_jobs.md` sub-rule, tier-up is for training-data outputs. Standard QC PASS suffices; no Opus second pass needed.

## What's blocked / what's queued

**Cleared by this comm:**
- PR #213 + PR #215 merge (Decision 1α)
- Step 2 dispatch (Decision 2α)
- Step 5 queued (Decision 3β)

**Queued for future dispatches (after step 2 merges):**
- 12.5I-D corpus QC dispatch (verifies merged PR #213 corpus integrity)
- 12.5I-MW40-VERIFICATION-A design dispatch (~30 J-on-board parametric variants)
- 12.5J-D-pre test-guard deflake dispatch (Option b: tier-2 Δ-tolerance)

**Newly queued post-MW-40-verification (conditional):**
- If MW-40 verification 30/30 (or ≥27/30) CHECK → BATCH2 MW-40 graduation update PR (mirrors step 2 pattern)
- If MW-40 verification <27/30 CHECK → MW-40 stays wrong; PILOT_787 retains its 3-2 CHECK label as anomaly; MW-40 verification round labels still ship as training data

## References

- PR #213 (12.5I-C labelling): `programmer/phase125i-c-labelling-2026-05-06`
- PR #215 (QC PASS verdict): `qc/pr213-labelling-review-2026-05-06`
- PR #216 (HALT comm): master `8b078bf`
- PR #209 (MW-25 graduation pathway precedent): master `077c168`
- Opus tier-up evidence: this session's agent transcripts
- Memory: `feedback_quality_default_no_ask.md` (4th restatement), `feedback_orchestrator_decides_not_recommends.md`, `feedback_pilot_first_for_long_jobs.md`, `reference_corrections.md` (target file for new MW-25 entry)

**Status: Decisions 1α + 2α + 3β. PR #213 + #215 merge on this comm merge. LEAD-PROGRAMMER fires Step 1 (BATCH2 MW-25 update) immediately after.**
