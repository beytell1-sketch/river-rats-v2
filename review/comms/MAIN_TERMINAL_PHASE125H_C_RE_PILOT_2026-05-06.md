---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-C re-pilot — 12.5H-B' amendment merged; T7-ext predictions updated per QC MEDIUM-1; pilot 1-Sonnet × 18-20 hands
status: TRIGGER — fire now
---

# Phase 12.5H-C re-pilot

12.5H-B' amendment merged at master `f5472bc`. T7-ext now SUITED-NFD-with-blocker; PILOT_693 changed to AdKd on Jd8d4c; 12/12 T7-ext hands produce non-FOLD under v3.4 (resolves FOLD anti-training risk).

QC MEDIUM-1 (PR #177): orchestrator-side prediction in 12.5H-B' amendment dispatch was wrong. T7-ext hands produce **mixed RAISE/CALL split driven by `villain_air_pct`**, NOT uniform CALL.

**Updated T7-ext predictions per QC walk:**
- `villain_air_pct ≥ 0.20` → v3.4 carve-out fires → **RAISE** (e.g., PILOT_693 with air=0.312)
- `villain_air_pct < 0.20` → v3.4 default below threshold → **CALL** (e.g., PILOT_647 with air=0.047)

Builder verifies via pilot.

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125h-c-re-pilot-2026-05-XX` (XX = your start date) — fresh branch (PR #173 was the PILOT HALT report on the prior branch; clean slate for re-pilot).

### LEAD-PROGRAMMER (default — implementation)

#### Pre-flight (mandatory before launch)

- Verify master HEAD is `f5472bc` (12.5H-B' amendment merged)
- Verify `data/corpus_revision_125h_situations_2026-05-06.jsonl` and `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` reflect the amended T7-ext (all T7-ext rows have `has_flush_draw=1` AND `nut_flush_block=1`)
- Verify `prompts/gto_labeller_v3.4.md` at master HEAD with Fix 2.1.1 carve-out present
- Verify `scripts/dispatch_mass_labelling.py` model defaults to Sonnet 4.6, prompt resolution version-agnostic
- Pre-flight join-cardinality: 90 new `pilot_hand_id` (PILOT_605..694), zero collision with existing 604

#### Pilot phase (per `feedback_pilot_first_for_long_jobs.md`)

Pilot = first labeller × ~18-20 hands spanning all 6 templates (especially the 6-8 manual canonicals).

**Pilot gate criteria (UPDATED per QC MEDIUM-1):**

| Template | Updated prediction | Rationale |
|---|---|---|
| T8' parametric | **CHECK** | monotone-FD-on-As-public; matches existing 604 corpus; predicted-error from 12.5H-C dispatch corrected |
| T8' manual canonical (PILOT_689) | **CHECK** | same |
| T8' NFD canonical (PILOT_690 if SUITED-NFD without As-public) | **BET** | confirmed by 12.5H-C original pilot |
| T9' parametric / canonical | **BET** | confirmed |
| T10' parametric | **RAISE** | confirmed |
| T10' manual canonical (PILOT_692, MW-45) | **CALL** | broadway-completed turn; texture-specific; both GTO-defensible; accept labeller per 12.5H-C original pilot |
| T7-ext | **air-driven split**: villain_air ≥ 0.20 → RAISE; < 0.20 → CALL | per QC MEDIUM-1 walk |
| T-RAISE-stabilize | **RAISE** | confirmed by PILOT_658/694 |
| T-CONTROL | **per design_action** | 6/6 validated in 12.5H-C original pilot |

For T7-ext hands specifically:
- PILOT_647 (parametric, air ~0.047) → predicted CALL
- PILOT_693 (manual canonical, air 0.312) → predicted RAISE
- Other 10 T7-ext parametric hands: builder reads `villain_air_pct` per-hand and assigns predicted RAISE/CALL accordingly per the air-threshold rule

**Stop conditions (UPDATED):**
- Schema malformed → STOP
- Reasoning traces don't cite v3.4 → STOP
- Manual canonical pilot hand consensus disagrees with UPDATED prediction → STOP, route to orchestrator
- Per-call cost > 1.5× Sonnet 4.6 estimate → STOP

#### Full phase (only on pilot APPROVE)

5 Sonnet labellers × all 90 hands = 450 labels. Hard cap $120 (per design §6.2 + 12.5E-C precedent).

#### Orchestrator-side Opus tier-up cross-check (post-QC-APPROVE)

Per `feedback_pilot_first_for_long_jobs.md` sub-rule + 12.5E-C → 12.5H-pre pattern: orchestrator runs Opus single-pass cross-check on contested hands BEFORE labels-final gate. Builder doesn't need to dispatch Opus pipeline; orchestrator handles via subagent.

### Deliverable scope (PR diff)

Exactly 3 new files:
1. `data/corpus_revision_125h_labels_raw_2026-05-XX.jsonl` — raw 5-labeller responses (450 rows)
2. `data/corpus_revision_125h_labels_2026-05-XX.jsonl` — consensus labels (90 rows)
3. `review/comms/BUILDER_REPORT_PHASE125H_C_LABELLING_2026-05-XX.md` — report with G1-G3 self-checks (G4 fires at 12.5H-D) + pilot phase outcome table + full phase results

### What you do NOT do

- Do NOT run Opus pipeline cross-check (orchestrator handles tier-up)
- Do NOT touch existing 604-row corpus or its labels
- Do NOT modify v3.4 prompt or any v3.x prompt
- Do NOT exceed $120 cost cap
- Do NOT label hands beyond the 90 in the 12.5H amended corpus

## QC stream — what you audit (when 12.5H-C re-pilot PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when builder force-pushes.

When triggered (5 audits — same as original 12.5H-C dispatch + updated prediction verification):

1. **Diff scope** — exactly 3 new files; no edits to existing source surfaces or 604-corpus / 12.5H amended-corpus data files
2. **Citation existence** — every file:line in builder report exists at master HEAD
3. **Label distribution sanity (G2)** — 90 hands, all 5 classes represented; no class with 0 labels (informational)
4. **Cost reconciliation** — total ≤ $120; per-call cost matches Sonnet 4.6; 450 calls completed (or partial documented)
5. **NEW: Manual canonical air-driven split correctness** — for the 6-8 manual canonicals, verify consensus_action matches UPDATED predicted v3.4 output (T7-ext per-hand air split; T8'/T9'/T10' per updated table); HOLD if any divergence without explanation in builder report

Post `REVIEW_QC_PHASE125H_C_LABELLING_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER pre-flight + pilot Sonnet × 1 × ~18-20 hands
2. Pilot APPROVE → full Sonnet × 5 × 90
3. PR opens
4. Orchestrator posts QC audit-now trigger
5. Standalone QC pre-merge audit
6. Orchestrator-side Opus tier-up cross-check (post-QC; before labels-final)
7. On Opus 18+/20 (or all-90 verified) agreement: orchestrator merges; **dispatches 12.5H-D corpus QC sweep**
8. On Opus material divergence: route back to LEAD-PROGRAMMER for full Opus × 5 relabel

## What's blocked / what's queued

**Blocked:**
- 12.5H-C PR opens → on builder pilot APPROVE + full + report
- 12.5H-C QC trigger → on PR open
- 12.5H-C labels-final gate → on QC APPROVE + Opus tier-up
- 12.5H-C merge → on labels-final
- 12.5H-D dispatch → on PR merge

**Queued:**
- All items per PR #168 §"What's blocked / queued"
- TC-X-DISPATCH-PREDICTION-VERIFICATION sub-vector (per QC's bonus pattern note in PR #177): if a third instance of orchestrator-side prediction error appears, formalize as QC test class

## References

- 12.5H-B' amendment merged: master `f5472bc` (PR #175)
- 12.5H-B' QC verdict: master `2eaf206` (PR #177)
- 12.5H-B' amendment dispatch: master `a84793c` (PR #174)
- PILOT HALT comm: master `c01b799` (PR #173)
- 12.5H-C original dispatch (superseded by this re-pilot directive): master `fb6983b` (PR #172)
- 12.5H-A design: master `858b032` (PR #165)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `f5472bc`)
- Memory: `feedback_explicit_action_trigger.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_river_rats_team_structure.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5H-C RE-PILOT TRIGGER posted. Updated predictions per QC MEDIUM-1. Path C empirically validated at amendment audit; air-driven RAISE/CALL split for T7-ext is the GTO-correct partition.**
