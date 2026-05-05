---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-C — Opus tier-up cross-check before declaring 110 Sonnet labels final; supersedes "accept labels" portion of PR #144
status: DIRECTIVE — supersedes PR #144 §"Orchestrator decision: hybrid B' + D" label-acceptance portion
---

# 12.5E-C — Opus tier-up cross-check before "labels final"

Owner critique 2026-05-05: *"did you test sonnet labels with an opus review? are you now applying slow quality approach?"*

Honest answer: NO and NO. PR #144 declared 110 Sonnet labels "final" based on labeller reasoning being defensible. That's a same-tier circular check — Sonnet judging Sonnet's reasoning. The slow-quality verification is Opus cross-check.

New sub-rule saved to `feedback_pilot_first_for_long_jobs.md`: training data outputs require a tier-up verification before "final." This applies retroactively to PR #142 labels.

## What this directive supersedes

PR #144 (master `45be508`) §"Orchestrator decision: hybrid B' + D" — specifically the "accept the 110 labels as final" line. That conclusion was premature.

What stays from PR #144:
- v3.4 prompt authoring (clause (e) `villain_air_pct ≥ 0.05`) — independent of label-acceptance; still correct
- T1 deferral to 12.5E-F outcome — still correct (T1 is design-vs-labeller-protocol mismatch, not a label-quality question)

What changes:
- Labels are NOT final until Opus cross-check completes
- 12.5E-D dispatch is BLOCKED on Opus cross-check, not just on PR #142 merge

## LEAD-PROGRAMMER — what you do

Branch: continue on `programmer/phase125e-c-labelling-2026-05-05` (same branch as PR #142). The cross-check ADDS to the PR diff.

### LEAD-PROGRAMMER (default — implementation)

**Opus cross-check pilot (mandatory before "labels final"):**

20-hand cross-section × 5 Opus 4.7 labellers each = 100 calls. Estimated cost ~$15-30. Hard cap **$50**.

**Hand selection (pre-specified — no orchestrator second-guessing):**

| Cohort | Hands | Reason |
|---|---|---|
| T5 CALL (the failures) | PILOT_542, 543, 544, 600 | 4 hands; verify Sonnet's CALL on near-zero-air heart variants is GTO-correct |
| T5 RAISE (the successes) | PILOT_539, 540, 541, 599 | 4 hands; verify Sonnet's RAISE on moderate-air variants is GTO-correct |
| T1 (full miss) | first 6 of T1's 14 hands (PILOT_495..500 — verify exact pilot_hand_ids in situations.jsonl) | 6 hands; verify Sonnet's CHECK consensus is GTO-correct or whether Opus disagrees with DO NOT Rule 2 invocation |
| T7 (split) | 3 hands from each side of T7's CALL/RAISE/FOLD split | 6 hands; verify the split direction matches Opus reading |
| **Total** | **20 hands** | |

**Configuration:**
- Labeller model: **Claude Opus 4.7** (`claude-opus-4-7`) — verify model identifier at https://docs.anthropic.com once before launch
- Labellers per hand: **5** (matches Sonnet protocol for apples-to-apples comparison)
- Total calls: 20 × 5 = **100**
- Prompt: **v3.4** (the new file from PR #144 amendment); falls back to v3.3 if v3.4 not yet authored
- Output: same schema as Sonnet labelling (raw + consensus JSONLs)

**Pre-flight before launching:**
- Confirm `prompts/gto_labeller_v3.4.md` exists (if not, this directive runs after PR #144 amendment lands; coordinate sequencing)
- Single-call test: 1 hand × 1 Opus labeller; verify schema + cost-per-call estimate

**Deliverables (extend PR #142 force-push):**

| File | Status | Purpose |
|---|---|---|
| `data/corpus_revision_125e_opus_crosscheck_raw_2026-05-05.jsonl` | NEW | 100 raw Opus labeller responses |
| `data/corpus_revision_125e_opus_crosscheck_consensus_2026-05-05.jsonl` | NEW | 20 consensus rows from Opus × 5 |
| `review/comms/BUILDER_REPORT_PHASE125E_C_OPUS_CROSSCHECK_2026-05-05.md` | NEW | Cross-check report with side-by-side Sonnet vs Opus consensus per hand + agreement analysis |
| `prompts/gto_labeller_v3.4.md` | NEW (from PR #144) | Already specified |
| Existing PR #142 deliverables | UNCHANGED | 5 files from prior PR #142 push |

PR #142 diff scope grows from 6 (original + v3.4) to **9 files** total.

### LEAD-PROGRAMMER (gto-expert hat — agreement analysis)

After Opus cross-check completes, swap to gto-expert hat and produce the agreement table:

| pilot_hand_id | Sonnet consensus | Opus consensus | Agreement | Notes |
|---|---|---|---|---|
| PILOT_542 | CALL 4/5 | <opus> | ✓/✗ | (any divergent reasoning) |
| ... | ... | ... | ... | ... |

**Agreement criteria for "labels final" decision:**

| Outcome | Action |
|---|---|
| Opus agrees with Sonnet on ≥18 of 20 hands (≥90%) AND both H-FEAT primaries (PILOT_599 RAISE + PILOT_600 CALL) match | LABELS FINAL — proceed to PR #142 merge + 12.5E-D dispatch |
| Opus disagrees on 3-5 of 20 (10-25%) | PARTIAL DIVERGENCE — orchestrator decides per-hand whether divergent hands need full Opus re-label or stay as Sonnet labels |
| Opus disagrees on 6+ of 20 (≥30%) OR either H-FEAT primary disagrees | MATERIAL DIVERGENCE — full Opus re-label of all 110 hands ($80-150 extra spend); Sonnet labels superseded |

### Stop conditions for cross-check

- Opus model identifier is wrong (API rejects) → STOP, fix
- $50 cap reached before 100 calls complete → STOP, partial report
- Any of 20 hands receives <5 Opus labels → STOP, fix dispatch + retry
- Output schema malformed on >2 raw labels → STOP, investigate dispatch script
- Opus cross-check report shows MATERIAL DIVERGENCE on H-FEAT primaries → STOP, route to orchestrator (not "decide and proceed")

### What you do NOT do

- Do NOT re-label all 110 hands with Opus pre-emptively (that's $80-150; only do it if cross-check shows MATERIAL DIVERGENCE)
- Do NOT modify the 110 Sonnet labels themselves regardless of Opus outcome (they stay as Sonnet labels; if MATERIAL DIVERGENCE, Opus labels REPLACE them in a separate file/PR cycle)
- Do NOT skip the cross-check on T7 hands (they're contested; verification is highest-value there)
- Do NOT improvise the agreement criteria thresholds (the 90%/10-25%/≥30% bands are pre-specified)

## QC stream — what you audit

Standalone QC SOLO-routed per memory.

When the amended PR #142 lands with cross-check:

**6 audits:**
1. **Diff scope** — exactly 9 files (5 from original PR #142 + 1 v3.4 prompt + 3 cross-check files); no edits to existing 110 labels
2. **Citation existence** — every file:line in cross-check report exists at master HEAD
3. **v3.4 prompt verbatim match** — diff against PR #144 spec (existing audit from PR #144)
4. **NEW: Opus cross-check cost reconciliation** — total Opus spend ≤ $50; per-call matches Opus 4.7 pricing; 100 calls completed
5. **NEW: Agreement analysis correctness** — verify the side-by-side table in cross-check report accurately reflects raw + consensus JSONLs (programmatic check, not interpretive)
6. **NEW: Tier-up decision routing** — based on agreement criteria, verify the cross-check report's conclusion (LABELS FINAL / PARTIAL DIVERGENCE / MATERIAL DIVERGENCE) matches the empirical numbers

If MATERIAL DIVERGENCE: HOLD on PR #142 merge; surface to orchestrator for full Opus re-label decision.
If PARTIAL DIVERGENCE: HOLD on PR #142 merge; surface to orchestrator for per-hand decision.
If LABELS FINAL: APPROVE.

Post `REVIEW_QC_PHASE125E_C_AMEND_OPUS_*.md`.

## Sequencing

1. LEAD-PROGRAMMER (architect hat) finishes v3.4 prompt authoring (from PR #144 directive)
2. LEAD-PROGRAMMER (default) launches Opus cross-check pilot (20 hands × 5 Opus = 100 calls; ≤$50)
3. LEAD-PROGRAMMER (gto-expert hat) agreement analysis + tier-up decision routing
4. Force-push to PR #142 with cross-check files + agreement report
5. Standalone QC pre-merge audit (6 audits)
6. **Branch point on Opus outcome:**
   - LABELS FINAL → orchestrator merges PR #142 → 12.5E-D dispatched
   - PARTIAL DIVERGENCE → orchestrator decides per-hand; possible re-label of N divergent hands; 12.5E-D delayed
   - MATERIAL DIVERGENCE → orchestrator dispatches full Opus re-label ($80-150 extra) + new 12.5E-C-2 PR; 12.5E-D delayed by ~1 day

## Cost accounting (cumulative)

- 12.5E-C original Sonnet × 5 × 110 hands = $0 (under cap; Sonnet 4.6 subagent cost)
- 12.5E-C Opus cross-check 5 × 20 hands = ≤$50 (this dispatch)
- 12.5E-C contingent full Opus re-label 5 × 110 hands = ≤$170 (only if MATERIAL DIVERGENCE)
- Total budget envelope: $200 cap from PR #143 still applies; cross-check well within; full re-label would consume the rest

## What's blocked / what's queued

**Blocked:**
- PR #142 merge → on Opus cross-check + standalone QC APPROVE
- 12.5E-D dispatch → on PR #142 merge AND tier-up decision = LABELS FINAL (or post-re-label equivalent)

**Queued (no separate owner ask):**
- T1 deferral to 12.5E-F (still correct per PR #144)
- v3.4 prompt authoring (already in PR #144 directive)
- All other queued items from PR #144 (NIT-1, PILOT_595 cosmetic, MEDIUM-2, 3 NITs, 12.5G, protocol amendment #2)
- **NEW: tier-up verification rule** (`feedback_pilot_first_for_long_jobs.md` sub-rule) — applies to all future training-data outputs

## Methodology lesson — surfaced now (not deferred)

Owner has now restated the slow-quality rule in three sessions. Each restatement reveals an orchestration shortcut I rationalized as "fine because reasoning was defensible." That's not slow-quality. Slow-quality is verification across tiers, not within-tier consensus.

This is the third time the rule has been restated. The orchestration drift is on me. Saving the sub-rule explicitly + applying retroactively here. Future training-data dispatches automatically include tier-up verification as a phase, not as an afterthought.

## References

- PR #144 (label-acceptance decision being superseded): master `45be508`
- PR #142 (12.5E-C BLOCKED labelling round): open
- v3.3 prompt: `prompts/gto_labeller_v3.3.md` (master `0eaac06`)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (NEW, in PR #142 amendment)
- Memory: `feedback_pilot_first_for_long_jobs.md` (UPDATED 2026-05-05 with tier-up verification sub-rule), `feedback_quality_default_no_ask.md`, `feedback_river_rats_team_structure.md`

**Status: 12.5E-C labels NOT FINAL pending Opus tier-up cross-check. PR #142 amendment grows by 3 files (cross-check raw + consensus + report). Builder dispatches Opus on 20 contested hands; agreement analysis decides labels-final vs partial-divergence vs material-divergence; 12.5E-D blocked until labels-final.**
