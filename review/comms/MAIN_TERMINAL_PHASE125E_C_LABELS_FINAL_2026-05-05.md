---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-C Opus tier-up cross-check COMPLETE — 20/20 agreement; LABELS FINAL; supersedes PR #145 builder-pipeline-cross-check scope
status: DIRECTIVE — supersedes PR #145 §"LEAD-PROGRAMMER (default — implementation)" Opus pipeline run; builder amendment is simpler
---

# 12.5E-C Opus tier-up cross-check — LABELS FINAL

Orchestrator ran the Opus tier-up cross-check directly via subagent (Opus 4.7 model). 20 contested hands × Opus reasoning per hand. Result: **20/20 agreement with Sonnet × 5 consensus** across all five cohorts.

Pre-specified gate criteria (PR #145):
- ≥18/20 agreement AND both H-FEAT primaries match → LABELS FINAL ✓ (this outcome)
- 3-5 disagreement → PARTIAL DIVERGENCE
- ≥6 disagreement OR either H-FEAT primary disagrees → MATERIAL DIVERGENCE

**Verdict: LABELS FINAL.** Full Opus × 5 pipeline relabel NOT NEEDED.

Full cross-check details: `review/comms/ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md` (in this PR).

## Why orchestrator ran it directly

Per `feedback_pilot_first_for_long_jobs.md` tier-up sub-rule: training-data outputs require higher-rigor-tier verification before final. The cross-check is pilot-scale (20 hands) — a single careful Opus read per hand is sufficient to flag divergence. Builder's pipeline-based Opus × 5 was the original plan but takes longer and costs $15-30 extra. Orchestrator-side single-Opus cross-check produced an unambiguous 20/20 result.

If Opus had disagreed materially, the full pipeline relabel would have been mandatory. Since 20/20 agree, builder skips the pipeline cross-check and goes straight to amendment-with-cross-check-report.

Per `feedback_orchestrator_decides_not_recommends.md`: the LABELS FINAL decision is the gate criterion firing — that's not a "recommendation," it's the pre-specified outcome the criteria selected.

## Cohort-by-cohort agreement

| Cohort | Hands | Sonnet consensus | Opus verdict | Match |
|---|---|---|---|---|
| T5_CALL | PILOT_542/543/544/600 | CALL × 4 | CALL × 4 | 4/4 ✓ |
| T5_RAISE | PILOT_539/540/541/599 | RAISE × 4 | RAISE × 4 | 4/4 ✓ |
| T1_first6 | PILOT_495..500 | CHECK × 6 | CHECK × 6 | 6/6 ✓ |
| T7_CALL | PILOT_559/560/561 | CALL × 3 | CALL × 3 | 3/3 ✓ |
| T7_RAISE | PILOT_563/564/565 | RAISE × 3 | RAISE × 3 | 3/3 ✓ |
| **Total** | **20** | | | **20/20** |

H-FEAT primary load-bearing test:
- PILOT_599 (villain_air_pct = 0.153, clause-e satisfied): Sonnet RAISE; Opus RAISE ✓
- PILOT_600 (villain_air_pct = 0.020, clause-e fails): Sonnet CALL; Opus CALL ✓

The v3.4 carve-out + clause (e) floor cleanly partition the T5 cohort. Sonnet labellers correctly inferred the implicit clause; Opus reasoning confirms it. v3.4 documentation makes the inferred rule explicit.

## LEAD-PROGRAMMER — what you do (simplified scope)

PR #145 dispatched a builder Opus × 5 pipeline cross-check. That's no longer needed; orchestrator already ran the verification. **Simplified amendment scope on PR #142:**

Branch: continue on `programmer/phase125e-c-labelling-2026-05-05`. Force-push amendment.

### Amendment scope — exactly 6 files in PR diff (was 9 in PR #145; -3 because no pipeline cross-check files)

| File | Status | Source |
|---|---|---|
| `data/corpus_revision_125e_labels_raw_2026-05-05.jsonl` | UNCHANGED | (already in PR; 550 raw Sonnet labels) |
| `data/corpus_revision_125e_labels_2026-05-05.jsonl` | UNCHANGED | (already in PR; 110 consensus Sonnet labels — FINAL per cross-check) |
| `scripts/dispatch_mass_labelling.py` | UNCHANGED | (already in PR; version-agnostic refactor) |
| `scripts/collect_mass_labels.py` | UNCHANGED | (already in PR; glob refactor) |
| `prompts/gto_labeller_v3.4.md` | NEW | Author per PR #144 spec — v3.3 verbatim + Fix 2.1.1 carve-out paragraph |
| `review/comms/BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md` | UPDATE | Rename → `BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md`; preserve all empirical analysis; add §"Resolution" section pointing at orchestrator cross-check |

Diff scope: 6 files (5 from PR #142 prior commits + 1 new v3.4 prompt; report updates in-place).

### What you do NOT do

- Do NOT run the Opus × 5 pipeline cross-check (orchestrator already verified; saves $15-30 + ~30 min)
- Do NOT change the 110 Sonnet labels (LABELS FINAL per cross-check)
- Do NOT modify v3.4 prompt content from PR #144 spec
- Do NOT add new files beyond v3.4 prompt + report rename

### LEAD-PROGRAMMER (architect hat — author v3.4 prompt)

Per PR #144 spec already merged: copy v3.3 verbatim + append the Fix 2.1.1 carve-out paragraph. Verify against PR #144 directive character-for-character.

### LEAD-PROGRAMMER (default — minor edits)

Update the BUILDER report:
- Rename file from `BUILDER_BLOCKED_*` to `BUILDER_REPORT_*RESOLVED_*`
- Preserve §"Headline numbers" through §"References" (the empirical analysis is correct and load-bearing for posterity)
- Add new §"Resolution" section that:
  - Notes orchestrator ran tier-up cross-check via subagent (20/20 agreement)
  - Points at `review/comms/ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md`
  - Points at this directive
  - Notes T1 deferred to 12.5E-F outcome per PR #144 (still active)

### Stop conditions

- v3.4 prompt drift from PR #144 spec → STOP
- Any change to the 110 labels → STOP (LABELS FINAL)
- Any change to T5/T1/T7 hand definitions → STOP (Path B "T5 unchanged" still binds)
- Diff scope > 6 files → STOP

## QC stream — what you audit

Standalone QC SOLO-routed per memory.

**5 audits on amended PR #142:**

1. **Diff scope** — exactly 6 files; no edits to existing source surfaces or label files
2. **Citation existence** — every file:line in builder report + v3.4 prompt + this directive exists at master HEAD
3. **v3.4 prompt verbatim match** — diff Fix 2.1.1 section against PR #144 spec character-for-character (existing audit from PR #144)
4. **NEW: Cross-check report integrity** — verify `ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md` exists on master post-merge and contains the 20-hand agreement table + verdict
5. **NEW: Label-final invariance** — verify the 110 Sonnet labels and 550 raw labels are byte-identical to what was in PR #142 prior commit; any drift indicates label tampering

HOLD or APPROVE. Post `REVIEW_QC_PHASE125E_C_AMEND_FINAL_*.md`.

## Sequencing

1. LEAD-PROGRAMMER (architect hat) authors v3.4 prompt per PR #144 spec
2. LEAD-PROGRAMMER updates BUILDER report (rename + §Resolution section)
3. Force-push to PR #142
4. Standalone QC pre-merge audit (5 audits)
5. On QC APPROVE: orchestrator merges PR #142
6. **12.5E-D dispatched** (corpus QC phase per design §8.D + queued cleanup items)

## What this directive supersedes

- PR #145 §"LEAD-PROGRAMMER (default — implementation)" — Opus × 5 pipeline cross-check no longer required (orchestrator-side cross-check produced unambiguous 20/20)
- PR #145 §"Sequencing" steps 2-5 (pre-flight + run + agreement + report) collapse to "builder amends with cross-check report (already produced)"

What stays from PR #145:
- Pre-specified agreement criteria (LABELS FINAL outcome triggered)
- T1 deferred to 12.5E-F (PR #144 deferred this; still active)
- v3.4 prompt authoring (PR #144 spec; still required in this amendment)

## What's blocked / what's queued

**Blocked:**
- PR #142 merge → on builder amendment + standalone QC APPROVE
- 12.5E-D dispatch → on PR #142 merge

**Queued (no separate owner ask):**
- T1 deferred to 12.5E-F outcome (still active per PR #144)
- v3.4 prompt authoring (in this amendment per PR #144 spec)
- NIT-1 PLAN §3.T8 cleanup → at 12.5E-D
- PILOT_595 design_note cosmetic → at 12.5E-D
- MEDIUM-2 V-X4 prose at trainer line 1371 → at 12.5E-E re-train
- 3 NITs from PR #134 → at 12.5E-E
- 12.5G cap retuning sweep → post-12.5E-F
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations before declaring blueprint design complete) → builder formalizes in `docs/PROCESS_GUIDE.md`

## Methodology lesson — orchestrator-side cross-check is valid for pilot-scale verification

The pilot-first sub-rule (`feedback_pilot_first_for_long_jobs.md`) requires tier-up verification on training-data outputs. The verification can come from EITHER:
- Builder's pipeline (Opus × 5 via `dispatch_mass_labelling.py`) — produces apples-to-apples consensus comparison; canonical format
- Orchestrator subagent (single Opus per hand) — faster, cheaper, gate-decision-equivalent for pilot-scale

When the result is convergent (LABELS FINAL), the orchestrator-side cross-check is sufficient. When the result is divergent, the builder pipeline relabel is mandatory (full data integration). This pattern preserves slow-quality rigor while avoiding unnecessary spend.

Future tier-up dispatches use orchestrator-side first, escalate to builder pipeline only on divergence.

## References

- PR #145 (Opus cross-check dispatch — pipeline portion superseded): master `c299bab`
- PR #144 (label-acceptance + v3.4 spec — superseded by PR #145; v3.4 spec still active): master `45be508`
- PR #142 (12.5E-C BLOCKED labelling round): open
- v3.3 prompt: `prompts/gto_labeller_v3.3.md` (master `0eaac06`)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (NEW, in this amendment)
- Cross-check raw output: `review/comms/ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md` (in this PR)
- Memory: `feedback_pilot_first_for_long_jobs.md` (tier-up sub-rule), `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_river_rats_team_structure.md`, `feedback_qc_routing_when_standalone_active.md`

**Status: 12.5E-C LABELS FINAL. Orchestrator-side Opus cross-check 20/20. Builder amendment scope simplified (6 files vs PR #145's 9). 12.5E-D dispatch unblocked on PR #142 merge.**
