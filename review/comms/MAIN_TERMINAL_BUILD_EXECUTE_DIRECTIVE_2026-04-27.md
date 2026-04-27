---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Lead-programmer (builder) · QC stream · Owner (briefed)
re: Build-execute directive after PR #60 Phase 2 merge — E1 re-extract + E2 pool generation + E3 schema verify + C2 corpus assembly; Tier 1 manifest expansion runs in parallel
status: DIRECTIVE — pipeline execution greenlit on merged Phase 2 code
---

# Build-execute directive — corpus revision pipeline

## Context

PR #60 Phase 2 merged at master `d9b4b8d`. F1-F4 fixes plus the original C1-C7 corrections + 5 R-items are all in production code. 3-way APPROVE convergence (ml-architect + gto-expert + QC). Build-execute can begin.

## Authorization

This directive authorizes the builder to **execute the corpus revision pipeline scripts on live data**. Per CLAUDE.md §1 (Plan Before Build): code is reviewed and merged; pipelines may now run on the merged code. Per memory `feedback_listen_to_orchestrator_always.md`: orchestrator directive addressed to builder by name = sufficient authorization.

## Pipeline sequence

Run in order. Each step has a verification gate before the next step proceeds.

### Step 1 — E1: re-extract 100-hand pilot corpus

```
cd ~/river-rats-v2
python scripts/reextract_pilot_100_features.py \
  --input data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --output data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --bb-chip-size 10
```

**Verification gate:**
- Output file exists with same record count (100)
- `mean(spr)` in [5.0, 15.0] (BB-unit; was 0.117-1.25 chip-unit before fix)
- `is_preflop_aggressor` count >= 30 (reconstruction recovers IS_PFA from `prior_actions`)
- 3-bet edge cases handled (3 SB-3bet hands → IS_PFA=0)
- Labels untouched (verify by hashing label fields against original)

**If gate fails:** STOP and report BLOCKED. Do not proceed to E2.

### Step 2 — E2: pool generation (Mode B + Mode A)

**E2-B (Mode B factory pool):**
```
python river-rats-core/generate_corpus_revision_pool.py \
  --mode b \
  --output data/corpus_revision_pool_mode_b_2026-04-27.jsonl
```

Expected: 111 records across 9 scenario modules (PFA 22, facing-bet 16, BAC 9, MAGG 10, NFD 7 non-boundary + 4/5 boundary, monster 10, Rule 11 10, donk 15, SB-hero 12).

**Verification gate:**
- 111 records produced (exactly)
- All records have correct family fingerprints (no duplicates within family)
- NFD R4 ±0.03 gate: 4/5 boundary templates pass (T1-T4); T5 expected to fail (documented ceiling)
- All MAGG records have `villain_aggression_count == 2` at river

**E2-A (Mode A self-play pool):**

Per builder Phase 2 Q3 — UTG self-play folds preflop yielding 0 records. Use CO/BTN/BB positions:
```
python river-rats-core/generate_corpus_revision_pool.py \
  --mode a \
  --deals 1000 \
  --positions CO,BTN,BB \
  --seed 2026 \
  --output data/corpus_revision_pool_mode_a_2026-04-27.jsonl
```

If the script's `--positions` flag doesn't exist yet (it may not — builder Q3 was a flag, not yet a fix), report BLOCKED before running. Do NOT add the flag yourself; that's a code change requiring its own review cycle. If the flag is missing, the workaround is to invoke the underlying `generate_pool` function directly (or write a small driver script in `scripts/`) — but document this in your report and surface for orchestrator review.

**Verification gate:**
- ≥100 Mode A records produced (yield depends on self-play; 1000 deals should produce 100-200 records)
- All records have `feat_dict['spr']` in BB-unit range (mean 4-16, NOT 0.117-1.25). The N1 smoke test (now active) should pass — rerun it against the produced pool.
- No duplicate fingerprints between Mode A and Mode B pools (incremental forbidden_fingerprints threading per blueprint)

**If E2-A yield is < 50 records OR if SPR distribution is chip-unit:** STOP and report BLOCKED — F1 fix may have a remaining defect.

### Step 3 — E3: schema compatibility verification

```
python scripts/verify_feature_schema_compatibility.py \
  --base-model river-rats-core/models/gto_model_v9_baseline_45feat.json \
  --corpus-sample data/corpus_revision_pool_mode_b_2026-04-27.jsonl
```

**Expected outcome:**
- 45-vs-59 feature delta confirmed (14 new features); exit 0
- If v9 baseline model not at expected path: graceful skip with warning (per C6 resolution path)
- Hard fail only if corpus is missing base model features (regression)

**Verification gate:** exit 0 (or clean skip if model absent).

### Step 4 — C2: 500-hand corpus assembly

```
python scripts/build_corpus_revision_500_hand.py \
  --pilot-input data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --pool-mode-a data/corpus_revision_pool_mode_a_2026-04-27.jsonl \
  --pool-mode-b data/corpus_revision_pool_mode_b_2026-04-27.jsonl \
  --output data/corpus_revision_500_hand_2026-04-27.jsonl \
  --lock-file data/corpus_revision_500_hand_2026-04-27.lock
```

**Verification gate (the structural attestation in `_verify_corpus()`):**
- Total 500 records (100 re-extracted + 400 from pools)
- OOP percentage in [0.55, 0.65] (now strict per F3)
- IP percentage in [0.35, 0.45] (now checked per F3)
- All 12 Phase A mandatory quotas filled (PFA, facing-bet, BAC, MAGG, NFD-RAISE, NFD-CALL, NFD-boundary, monster, Rule 11, donk, SB-hero, etc.)
- NFD-boundary slot: 10 hands (4 turn-decision templates × ~2-3 records + others); slot will be undersized due to T5 ceiling — flag in report, NOT a STOP condition (boundary slot understocked is acceptable per gto-expert disposition)
- Lock file present with SHA256 + disjointness attestation

**If verification fails:** STOP and report BLOCKED. Do NOT manually patch the corpus — escalate.

## Tier 1 calibration manifest expansion (parallel)

In parallel with the corpus build (or after), the Tier 1 calibration set grows from 33→45 hands. This is a separate workstream and a separate PR. Refer to architect's prior R-items for the 12 new calibration hands required.

This directive does NOT cover Tier 1 expansion. It runs as its own PR cycle. If Tier 1 expansion blocks on questions, raise a separate comm.

## Reporting

Builder produces two reports:

1. **`review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md`** — pipeline execution log:
   - Each step: command, exit status, verification gate outcome
   - Step 4 (C2): full structural attestation table (OOP%, IP%, all 12 quotas, lock SHA256)
   - Any STOP conditions or warnings
   - Total wall-time + any cost

2. **PR open** for the new data files:
   - Branch: `programmer/corpus-revision-execution-2026-04-27`
   - Files: `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl`, `data/corpus_revision_pool_mode_*.jsonl`, `data/corpus_revision_500_hand_2026-04-27.jsonl`, lock file, `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md`
   - DO NOT include any code changes (this is a data-only PR; if code changes are needed, they go through their own review cycle first)

## Round 3 review on the data PR

Once data PR is open, orchestrator dispatches:
- **gto-expert mini-review**: spot-check 10-15 records across families for poker realism (action histories valid, board/hero combinations sensible, opener positions correct)
- **ml-architect mini-review**: feature-distribution checks (SPR histogram, IS_PFA distribution, feature schema 59 keys per record, no NaNs except where expected)
- **QC pre-merge audit**: paired V-Implementation-Spec-Match (lock file fields populated correctly) + V-Integration-Trace (re-run a sample from the pool through `extract_all_features` and confirm output matches stored feat_dict bit-for-bit)

Per memory `feedback_qc_required_before_approval.md`: QC must be involved before merge. The QC stream's autonomous /loop will pick up the data PR; if it doesn't within ~30 min, orchestrator writes a nudge directive.

## What is NOT in scope for this directive

- v3.2 protocol changes (locked)
- New scenario modules (deferred to v2.3+ backlog)
- Mass labelling kickoff (separate directive after data PR merges + Tier 1 expansion completes)
- NFD T5 alternative spec (resolved; accept 4/5 as designed)
- Bare-except cleanup (QC NIT 1; deferred to next maintenance cycle)
- conftest.py scripts/ path (Builder Q2; deferred)

## References

- Master HEAD post-merge: `d9b4b8d`
- Round 2 synthesis: `review/comms/MAIN_TERMINAL_PR60_PHASE2_SYNTHESIS_2026-04-27.md`
- Builder Phase 2 report: `review/comms/PROGRAMMER_REPORT_BLUEPRINT_V3_PHASE2_2026-04-27.md`
- Blueprint v3: `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md`
- Reviewer round 2:
  - `review/comms/REVIEW_ML_ARCHITECT_PR60_PHASE2_2026-04-27.md`
  - `review/comms/REVIEW_GTO_EXPERT_PR60_PHASE2_2026-04-27.md`
  - `review/comms/QC_ROUND2_AUDIT_PR60_PHASE2_2026-04-27.md`

**Status: BUILD-EXECUTE DIRECTIVE OPEN. Builder picks up; runs E1 → E2-B → E2-A → E3 → C2; reports + opens data PR. Round 3 review chain dispatches when data PR opens.**
