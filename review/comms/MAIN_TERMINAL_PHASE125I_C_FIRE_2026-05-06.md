---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5I-C labelling round — fire now (post-MW25-resolution; slow-quality T8'-r confirm + T9'-e + T10'-r + T-CONTROL)
status: TRIGGER — fire now
branch: programmer/phase125i-c-labelling-2026-05-06 (force-push, continues PR #208 work)
base: master `077c168` (PR #209 — MW-25 resolution merged)
---

# 12.5I-C labelling round — fire now

MW-25 T8'-r resolution merged (PR #209). Owner authorized fire on the slow-quality path. **LEAD-PROGRAMMER — fire now.**

## LEAD-PROGRAMMER — what you do

Branch: continue on `programmer/phase125i-c-labelling-2026-05-06` (force-push). Base: master `077c168`.

### Step 1 — T8'-redesigned slow-quality confirm (5 Sonnet × 30)

Per `feedback_quality_default_no_ask.md` and PR #209 §"Step 1": full slow-quality confirm, NOT extrapolation from pilot.

- 5 Sonnet labellers × 30 T8'-r parametric hands = 150 calls
- Expected outcome: 30/30 CHECK consensus per pilot's 5/5 pattern
- v3.4 prompt; hero-only convention preserved
- Cost target: $3-5
- Any T8'-r hand returning non-CHECK consensus → STOP and route to orchestrator (would empirically refute the 3-source convergence — Opus + 5/5 pilot + protocol traces — and reopen MW-25 question)

### Step 2 — T9'-expanded + T10'-redesigned + T-CONTROL full phase

Per PR #209 §"Step 2" + the original 12.5I-C dispatch (PR #206):

- 5 Sonnet × ~64 hands (T9'-e MW-40 family + T10'-r MW-45 family + T-CONTROL drift-detection)
- v3.4 prompt; same join-cardinality + schema gates as 12.5H-C precedent
- Manual canonical correctness check against predictions:
  - T9'-e prediction: BET (TP-medium-kicker IP 4-way after PFR check)
  - T10'-r prediction: RAISE (slowplay-set on AKQx-broadway-completed turn)
  - T-CONTROL: per design_action
- Manual canonical >1 divergence from prediction → STOP, route to orchestrator (per 12.5H-C precedent)

### Cost cap

$120 total for 12.5I-C labelling round (Step 1 + Step 2 combined). Pilot already spent ~$0.30 (PR #208).

### Stop conditions (full set)

- T8'-r 5×30: any hand returning non-CHECK → STOP, route to orchestrator
- T9'-e or T10'-r manual canonical >1 divergence from prediction → STOP, route to orchestrator
- $120 cap reached → STOP, partial report
- Schema malformed → STOP
- Labeller protocol mismatch (v3.2 / v3.3) → STOP

### Deliverable

3 files on the branch:
1. `data/corpus_revision_125i_labels_raw_2026-05-06.jsonl` (raw 5-labeller × 94 hand outputs)
2. `data/corpus_revision_125i_labels_2026-05-06.jsonl` (consensus per hand)
3. `review/comms/BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md`

Builder report sections (per PR #209 §"Step 3"):
- §"T8'-redesigned outcome" — 30/30 CHECK (or per slow-quality results); MW-25 reference disagreement noted
- §"T9'-e outcome"
- §"T10'-r outcome"
- §"T-CONTROL outcome" — drift detection
- §"MW-25 graduation note" — flag for owner (3-source + 30-hand convergence)

### What you do NOT do

- Do NOT run Opus pipeline cross-check (orchestrator handles tier-up post-QC-APPROVE)
- Do NOT touch existing 694-row corpus or labels
- Do NOT touch v3.x prompts
- Do NOT exceed $120 cost cap
- Do NOT extrapolate T8'-r CHECK from pilot (slow-quality means full 5×30)

## QC stream — what you audit (when 12.5I-C PR opens)

Same audit pattern as 12.5H-C + new audit for MW-25 graduation evidence (per PR #209 §"QC stream"):

1. Diff scope (3 files: raw labels + consensus + report)
2. Citation existence
3. Label distribution sanity (G2)
4. Cost reconciliation ≤ $120
5. Manual canonical correctness against predictions (T9'-e BET, T10'-r RAISE)
6. **MW-25 graduation evidence** — verify builder report documents 3-source CHECK convergence (5/5 pilot + Opus HIGH + 30/30 T8'-r consensus) supporting reference-set re-eval recommendation

QC stays IDLE until I post `MAIN_TERMINAL_QC_AUDIT_TRIGGER_*` for the 12.5I-C PR.

## Sequencing

1. LEAD-PROGRAMMER fires Step 1 (T8'-r 5×30) — runs ~30-45 min
2. On Step 1 30/30 CHECK: LEAD-PROGRAMMER fires Step 2 (T9'-e + T10'-r + T-CONTROL)
3. On Step 2 complete: PR opens
4. Orchestrator posts QC audit-now trigger
5. Standalone QC pre-merge audit
6. Orchestrator-side Opus tier-up cross-check post-QC-APPROVE
7. On Opus 18+/20 agreement: orchestrator merges; dispatches 12.5I-D corpus QC

## What's blocked / what's queued

**Blocked on this directive:**
- 12.5I-C PR opens → on LEAD-PROGRAMMER Step 1 + Step 2 + report
- 12.5I-D corpus QC dispatch → on PR merge + Opus tier-up
- 12.5K combined re-train → on 12.5I-E + 12.5J-E ship

**Parallel (independent):**
- PR #205 (12.5J-B feature implementation) — separate dispatch this session for MW-33 invariant root-cause memo before merge (see companion comm `MAIN_TERMINAL_PR205_MW33_INVESTIGATION_2026-05-06.md`)
- PR #210 (QC verdict comm on PR #205) — orchestrator merges as record this session

**Queued (owner WHAT, not blocking):**
- BATCH2 MW-25 reference update (Option α default, lock pending 30/30 confirm at Step 1)

## References

- 12.5I-C MW-25 resolution: master `077c168` (PR #209)
- 12.5I-C pilot HALT: master `52e5164` (PR #208)
- 12.5I-C dispatch (original): master `a635bcb` (PR #206)
- 12.5I-B merged: master `5df39f7` (PR #202)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_explicit_action_trigger.md`, `feedback_named_author_builds_not_polls.md`

**Status: 12.5I-C labelling round — LEAD-PROGRAMMER fire now. Step 1 (T8'-r 5×30 CHECK confirm) → Step 2 (T9'-e + T10'-r + T-CONTROL) → PR.**
