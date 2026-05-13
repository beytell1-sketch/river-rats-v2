# Orchestrator Restart Cheat-Sheet — 2026-05-13

For the new orchestrator terminal when the owner restarts tonight.

---

## First 15 minutes

### Minute 0-5: Ground in current state

```bash
cd ~/river-rats-v2
git fetch --all
git status
gh pr list --state open
```

You should see:
- 2 open PRs: #457 (STANDBY directive) + #458 (drafts bundle)
- Active branch: `builder-phase2-e-full-batch8-2026-05-12` (builder's mid-flight work)

### Minute 5-10: Read the synthesis

```
review/comms/DRAFT_PHASE2F_READINESS_SCORECARD_2026-05-13.md
```

This is the SINGLE document that summarises 4 audits + protocol gaps + 3 owner decisions.

### Minute 10-15: Verify Phase 2-E batch-008 state

```bash
wc -l data/4way_corpus/full_700/batch_008_raw_labels_labeller_*.jsonl
```

Expected (from 2026-05-13 snapshot):
- labeller_1: 50/50 ✓ complete
- labeller_2: 36/50 (72%)
- labeller_3: 11/50 (22%)
- labeller_4: 10/50 (20%)
- labeller_5: 25/50 (50%)

**If labellers haven't progressed since restart: builder needs to resume them. This is the first builder directive — finish batch-008 before Phase 2-F fires.**

---

## The order things must happen

```
1. Builder resumes batch-008 labellers 2-5 → ships PR → QC PASS → merge
2. Owner reads scorecard, makes 3 decisions
3. Orchestrator updates DRAFT_MAIN_TERMINAL_PHASE2F_FIRE_NOW with date + scope
4. Architect ratifies 5 drafts (4 from PR #458 + 1 new for KB if scope expanded)
5. QC G1-G4 audits
6. Owner approves architect deliverables
7. Builder fires B1 → B0 (calibration) → B2 (pilot) → B3 (full)
8. QC G5-G8
9. Owner gates at 3 checkpoints
10. Phase 2-F ships
```

---

## 3 owner decisions

| # | Decision | Default recommendation |
|---|---|---|
| 1 | Drift thresholds | PERMISSIVE (≤15% pilot accept) |
| 2 | Bundled or staged | STAGED (Phase 2-F1 = corpus only; Phase 2-F2 = prompt+KB) |
| 3 | 5-way reference timing | PARALLEL (start now) |

If owner approves all defaults: dispatch **Phase 2-F1** (chain dim + corpus regen only, no prompt change).

---

## Files prepared in PR #458

Already on GitHub. Architect ratifies or supersedes:

| File | Architect task |
|---|---|
| DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1 | A1 |
| DRAFT_AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5 | A2a |
| DRAFT_SPEC_RELABEL_CONSISTENCY_AUDIT_v1 | A3 |
| DRAFT_PILOT_SAMPLE_20HAND (3 files) | B2 input |
| AUDIT_GTO_LABELLER_V3_4_LATENT_ISSUES | A2b reference (v3.4 → v3.5 prompt rewrite) |
| AUDIT_KB_THREE_WAY_GTO_V1_3 | A2c reference (KB v1.3 → v1.4) |
| DRAFT_MAIN_TERMINAL_PHASE2F_FIRE_NOW | directive template — fill date + chosen scope |
| DRAFT_PHASE2F_READINESS_SCORECARD | OWNER reads this FIRST |

PENDING (agents finishing):

| File | Status |
|---|---|
| DRAFT_FULL_SAMPLE_80HAND | building |
| DRAFT_SPEC_DRIFT_ANALYZER_v1 | building |
| DRAFT_AUDIT_CORPUS_LABEL_DISTRIBUTION | building |

---

## Critical things NOT in the original STANDBY directive (PR #457)

Audits found these gaps; the FIRE_NOW directive needs them added before dispatch:

1. **A2c: KB v1.4 update** — KB v1.3 is out of sync with v3.4 prompt patches (3-layer override absent); 6 worked-example gaps (river, facing-raise, sandwich, strong-made, air)
2. **B0: Pre-pilot calibration** — per PROCESS_GUIDE §2.1 + §2.3, mandatory after KB change; gate = 20/24 + all 3 GTO-reversals correct
3. **Solver-verify routing** — per PROCESS_GUIDE §5.2, drift hands + RAISE hands need solver-verify queue routing
4. **Corpus quota expansion** — A1 must mandate facing-raise (≥10/batch) + river (≥5/batch) + position balance (≥5/batch per position), not just chain enumeration

---

## Solver-verify queue (pre-existing blocker)

Per Builder Report PR #453: queue is at **28 spots** (23 prior + 5 from batch-007). Per `feedback_solver_verification_queue.md`, queue MUST drain before retrain. Phase 2-F will likely ADD spots. Plan a parallel workstream to drain.

---

## Default ship sequence (if all defaults accepted)

1. **Today (2026-05-13):** Owner restarts, reads scorecard, accepts defaults
2. **Tonight:** Phase 2-E batch-008 resumes, ships
3. **2026-05-14:** Architect ratifies A1/A3; Builder fires B1
4. **2026-05-15:** Builder fires B2 (Phase 2-F1 pilot — no prompt change, just corpus chain regen baseline)
5. **2026-05-16:** Owner Gate 2 (pilot drift report)
6. **2026-05-17:** Builder fires B3 (full sample) if greenlit
7. **2026-05-18:** Phase 2-F1 ships
8. **Parallel from 2026-05-14:** A2b (prompt v3.5) + A2c (KB v1.4) drafted, gated for Phase 2-F2
9. **2026-05-20:** Phase 2-F2 dispatches with prompt+KB scope
10. **2026-05-23:** Phase 2-F2 ships → v9-4way warm-start training begins (Phase 2-G)

---

## What NOT to do

- Don't dispatch Phase 2-F before batch-008 ships (would create conflicting in-flight work)
- Don't merge PR #457 (STANDBY) — it's superseded by the FIRE_NOW directive that you'll create at dispatch
- Don't pick the BUNDLED scope (Decision 2 Option A) — multi-variable drift attribution is hard
- Don't skip B0 calibration — PROCESS_GUIDE §2.1 is mandatory
- Don't let drift thresholds default to STRICT (≤5%) — base-process noise floor is ~6%, you'd fail before starting

---

## If owner picks non-default scope

- **STRICT thresholds:** Architect's drift spec needs to be re-authored with new thresholds
- **BUNDLED scope:** Skip Phase 2-F1; dispatch full Phase 2-F (chain + prompt + KB) at once
- **5-WAY DEFERRED:** Drop the parallel 5-way reference workstream; reference set generation becomes blocker for v9-5way training later

Whatever scope is chosen, orchestrator updates `DRAFT_MAIN_TERMINAL_PHASE2F_FIRE_NOW` with:
- Real date (replace `2026-05-XX`)
- Chosen scope (delete unused sections)
- Verified batch-008 PR# and SHA in pre-flight checklist
- Then commit as `MAIN_TERMINAL_PHASE2F_FIRE_NOW_<date>.md` and dispatch by triggering architect
