---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-C REDESIGNED — pilot phase (14 manuals) → owner gate-check → full (96 parametric); supersedes PR #140 + PR #141
status: DIRECTIVE — supersedes original 12.5E-C dispatch + Opus amendment
---

# Phase 12.5E-C — pilot + full redesign

Owner critique 2026-05-05 surfaced an orchestration failure: the original 12.5E-C dispatch (PR #140 + Opus amendment PR #141) committed $200 in a single 550-call batch with only a token "3-hand × 1 labeller schema smoke test" as pre-flight. That checks plumbing, not whether v3.3 carve-out + Opus + 5-labeller consensus actually produces the predicted outcome on T5 H-FEAT canonicals. If approach is wrong, full $200 + time burned before knowing.

Standing rule now in memory (`feedback_pilot_first_for_long_jobs.md`): any long batch splits into pilot + full with explicit gate. Applying retroactively to 12.5E-C.

## Why this redesign supersedes (not amends) the prior two

Owner statement: *"i cant patch like this."* Two amendment cycles on a dispatch that should have been right the first time creates churn. This single redesign replaces both PR #140 (Sonnet sequencing) and PR #141 (Opus model swap) with a coherent pilot + full design. Builder + QC read THIS comm only.

## LEAD-PROGRAMMER — what you do

**Branch:** `programmer/phase125e-c-labelling-2026-05-XX` (XX = your start date)

**12.5E-C splits into 12.5E-C-1 (pilot) and 12.5E-C-2 (full).** Two sequential PRs. Gate between them.

### LEAD-PROGRAMMER (default — implementation)

#### 12.5E-C-1 (pilot) — load-bearing test verification

Hands: **all 14 manual canonicals** (PILOT_591..PILOT_604 in `data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl`). This includes the T5 H-FEAT primary PILOT_599 + PILOT_600 (the load-bearing test for the entire 12.5E migration) plus canonical examples from T1, T2, T3, T4, T6, T7.

Configuration:
- Labeller model: **Claude Opus 4.7** (`claude-opus-4-7`) — verify the model name once at https://docs.anthropic.com/ before launch
- Labellers per hand: **5**
- Total calls: 14 × 5 = **70 calls**
- Cost cap (pilot): **$30** (estimate ~$15-25; cap generous for token-overage)
- Prompt: `prompts/gto_labeller_v3.3.md` (master `0eaac06`)
- Consensus calculation: existing `collect_mass_labels.py` logic

Pilot-only deliverables (1 PR, 4 files):
1. `scripts/dispatch_mass_labelling.py` — UPDATE: change hard-coded `claude-sonnet-4-6` at line 154 to `claude-opus-4-7`; update prose strings ("sonnet" → "opus" or "expert labeller") at lines 5, 21, 269, 290 for accuracy
2. `data/corpus_revision_125e_pilot_labels_raw_2026-05-XX.jsonl` — raw 70-row labeller output
3. `data/corpus_revision_125e_pilot_labels_2026-05-XX.jsonl` — consensus 14-row pilot output
4. `review/comms/BUILDER_REPORT_PHASE125E_C1_PILOT_2026-05-XX.md` — pilot report

#### Pre-flight before pilot launch

- Verify `prompts/gto_labeller_v3.3.md` exists at master HEAD; verify Fix 2.1 carve-out present
- Verify `claude-opus-4-7` is the correct current model identifier (check Anthropic docs once)
- Single-call test: 1 hand (PILOT_591), 1 Opus labeller — confirm output schema matches expected, confirm cost-per-call is in range. STOP if malformed or pricing significantly off-estimate.

### LEAD-PROGRAMMER (gto-expert hat — pilot result verification, before opening 12.5E-C-1 PR)

After pilot run completes, swap to gto-expert hat and verify pilot output against design predictions. Document in pilot report:

| pilot_hand_id | template | predicted action (per design) | actual consensus | match? |
|---|---|---|---|---|
| PILOT_591 | T1 | BET | <actual> | ✓/✗ |
| PILOT_592 | T1 | BET | | |
| PILOT_593 | T2 | BET | | |
| PILOT_594 | T2 | BET | | |
| PILOT_595 | T3 | BET (thin value river) | | |
| PILOT_596 | T3 | BET | | |
| PILOT_597 | T4 | RAISE | | |
| PILOT_598 | T4 | RAISE | | |
| **PILOT_599** | **T5 H-FEAT primary** | **RAISE** | | **load-bearing** |
| **PILOT_600** | **T5 H-FEAT primary** | **RAISE** | | **load-bearing** |
| PILOT_601 | T6 | RAISE | | |
| PILOT_602 | T6 | RAISE | | |
| PILOT_603 | T7 | CALL | | |
| PILOT_604 | T7 | CALL | | |

**Gate criteria (all must hold to proceed to 12.5E-C-2):**
- PILOT_599 consensus = **RAISE** (load-bearing — T5 H-FEAT primary; v3.3 carve-out empirical validation)
- PILOT_600 consensus = **RAISE** (load-bearing — T5 H-FEAT primary; v3.3 carve-out empirical validation)
- ≥ 12 of 14 manual hands match predicted action (≥86% match rate; tighter than Sonnet baseline expected for Opus)
- Per-call cost matches Opus 4.7 estimate (validates total budget for full phase)
- All 14 hands received exactly 5 labels each
- Output schema correct on all 70 raw + 14 consensus rows
- Reasoning traces (in `labels[].reasoning`) explicitly cite v3.3 carve-out clauses on T5 hands (sanity check that labellers actually read v3.3, not v3.2 or KB §1.7 unmodified)

#### Stop conditions for pilot

- PILOT_599 OR PILOT_600 consensus ≠ RAISE → **STOP, report. Path B refuted at labelling layer; route back to architect hat for v3.3 wording revision OR escalation to Path C** (this is the entire 12.5E migration's load-bearing test failing)
- Match rate < 12/14 manual canonicals → **STOP, report. Either design predictions wrong or labellers misreading prompt; investigate before $80-150 full spend**
- Per-call cost > 1.5× Opus 4.7 estimate → **STOP, report. Total budget projection broken; revise before full**
- Reasoning traces show v3.2 reasoning (no v3.3 Fix 2.1 mention on T5 hands) → **STOP, dispatch script may not be routing v3.3 prompt correctly**
- Any non-recoverable runtime error in dispatch pipeline → **STOP, fix in this PR**

#### What pilot does NOT do

- Does NOT label the 96 parametric hands (12.5E-C-2 only)
- Does NOT touch existing 494-row corpus or its labels
- Does NOT modify v3.3 prompt (architect-hat workstream if needed)
- Does NOT improvise wording revisions on STOP — route to orchestrator

### After pilot APPROVE — 12.5E-C-2 (full)

Hands: 96 parametric situations (`data/corpus_revision_125e_situations_2026-05-04.jsonl`).

Configuration:
- Identical to pilot (Opus 4.7, 5 labellers per hand, v3.3 prompt)
- Total calls: 96 × 5 = **480 calls**
- Cost cap (full): **$170** (estimate ~$80-150 if pilot estimates hold; cap leaves buffer)

Total program cost: pilot ($30) + full ($170) = **$200 cap** (same as Opus amendment).

Full deliverables (separate PR, 3 files — no script changes; that landed in pilot PR):
1. `data/corpus_revision_125e_full_labels_raw_2026-05-XX.jsonl` — raw 480-row output
2. `data/corpus_revision_125e_full_labels_2026-05-XX.jsonl` — consensus 96-row output
3. `review/comms/BUILDER_REPORT_PHASE125E_C2_FULL_2026-05-XX.md` — full report

Full-phase stop conditions: same as pilot but applied at 96-hand scale; full-phase gto-expert spot-check verifies T5 parametric hands (5 random samples) consensus to RAISE.

## QC stream — what you audit

**Two pre-merge audits, one per PR.** Standalone QC SOLO-routed per `feedback_qc_routing_when_standalone_active.md`. No subagent.

### Audit on 12.5E-C-1 (pilot) PR

5 audits, NEW-class items vs prior phases:
1. **Diff scope** — exactly 4 files (1 modified script + 3 new data/comm files)
2. **Citation existence** — every file:line citation in pilot report exists at master HEAD
3. **Pilot match rate** — verify ≥12 of 14 manual canonicals consensus matches predicted action (table in builder report); HOLD if <12
4. **NEW: Cost reconciliation** — verify pilot total ≤ $30; verify per-call cost matches Opus 4.7 pricing; verify 70 calls completed
5. **NEW: T5 H-FEAT primary correctness** — verify PILOT_599 + PILOT_600 consensus = RAISE; if either is CALL/FOLD, **HOLD** and surface to orchestrator (this is THE load-bearing test)
6. **NEW: v3.3 prompt routing verification** — sample 3 of the 70 raw labeller responses; verify reasoning traces mention v3.3 Fix 2.1 carve-out (or `villain_call_count`/`villain_aggression_count` predicates) on T5 hands

HOLD or APPROVE. Post `REVIEW_QC_PHASE125E_C1_PILOT_*.md`.

### Audit on 12.5E-C-2 (full) PR — only after pilot APPROVE

5 audits:
1. **Diff scope** — exactly 3 files (no script changes)
2. **Citation existence** — every file:line in full report exists at master HEAD
3. **Full-phase distribution sanity** — 96 hands, all 5 classes represented across 96 + 14 = 110 combined; no class with 0 labels
4. **Cost reconciliation** — full phase ≤ $170; combined pilot + full ≤ $200; per-call pricing consistent
5. **Per-template consensus sanity** — for each of T1-T8, verify majority consensus action matches design intent for the template family (small-sample acceptable; this is a sanity check not a strict match-rate)

HOLD or APPROVE. Post `REVIEW_QC_PHASE125E_C2_FULL_*.md`.

## Sequencing

1. LEAD-PROGRAMMER pre-flight (model name verify + 1-call test)
2. LEAD-PROGRAMMER pilot run (70 calls, ≤$30)
3. LEAD-PROGRAMMER (gto-expert hat) pilot result verification (table above)
4. If pilot gate criteria all pass: 12.5E-C-1 PR opens
5. Standalone QC pre-merge audit on 12.5E-C-1 (6 audits)
6. On QC APPROVE: orchestrator merges 12.5E-C-1
7. **12.5E-C-2 dispatched** (full run on 96 parametric)
8. LEAD-PROGRAMMER full run (480 calls, ≤$170)
9. LEAD-PROGRAMMER (gto-expert hat) full-phase T5 spot-check
10. 12.5E-C-2 PR opens
11. Standalone QC audit on 12.5E-C-2 (5 audits)
12. On QC APPROVE: orchestrator merges; 12.5E-D dispatched (corpus QC phase)

## What this directive supersedes

- PR #140 (original 12.5E-C dispatch — single 550-call batch design): **superseded in full**
- PR #141 (Opus amendment — model swap + cap raise): **folded into this redesign**

Both prior comms remain on master as historical record. This redesign is the active authority for 12.5E-C.

## What's blocked / what's queued

**Blocked:**
- 12.5E-C-1 PR opens → on pilot run + builder gto-expert-hat pilot verification PASS
- 12.5E-C-2 dispatch → on 12.5E-C-1 merge AND pilot gate criteria
- 12.5E-D dispatch → on 12.5E-C-2 merge

**Queued (no separate owner ask):**
- NIT-1 from PR #139 (PLAN §3.T8 wording 36→22+14 cleanup): at 12.5E-D
- PILOT_595 design_note cosmetic (TPTK→top-two-pair): at 12.5E-D
- MEDIUM-2 from PR #134 (V-X4 prose at trainer line 1371): at 12.5E-E
- 3 NITs from PR #134: ride along at 12.5E-E
- Model-drift assessment (Opus pilot/full vs existing 494 Sonnet): at 12.5E-E trainer report Section E
- 12.5G cap retuning sweep: post-12.5E-F
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations before declaring blueprint design complete): lives in dispatch until LEAD-PROGRAMMER (architect hat) formalizes in `docs/PROCESS_GUIDE.md`

## Methodology lesson saved (2026-05-05)

`feedback_pilot_first_for_long_jobs.md` saved as standing orchestration rule: any long batch must be pilot + full with explicit gate. Token smoke tests + STOP conditions are insufficient because they catch plumbing failures, not approach failures. Pilot phase forces direct comparison of pilot output vs design predictions, surfacing approach-level failures before full commitment.

This applies to ALL future River Rats v2 batch dispatches: mass labelling, mass corpus generation, mass training (where applicable), any automated multi-call workstream where total spend > 5× pilot spend AND the approach has any unverified assumption.

## References

- 12.5E-C original dispatch: master `e7d7843` (PR #140)
- 12.5E-C Opus amendment: master `ce1528a` (PR #141)
- 12.5E-B amendment merged (corpus + v3.3 prompt): master `0eaac06` (PR #136)
- v3.3 prompt: `prompts/gto_labeller_v3.3.md` (master `0eaac06`)
- 12.5E design: master `bad1396` (PR #133)
- Memory: `feedback_pilot_first_for_long_jobs.md` (NEW 2026-05-05), `feedback_quality_default_no_ask.md` (reinforced 2026-05-04), `feedback_river_rats_team_structure.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5E-C REDESIGNED. Pilot (14 manuals × 5 Opus = 70 calls; ≤$30) → gate → full (96 parametric × 5 Opus = 480 calls; ≤$170). Total $200 cap unchanged. PR #140 + PR #141 superseded. LEAD-PROGRAMMER picks up redesigned spec; pilot launches first.**
