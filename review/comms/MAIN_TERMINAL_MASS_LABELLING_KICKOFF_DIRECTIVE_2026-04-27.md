---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner (sign-off requested) · Lead-programmer · gto-expert · ml-architect · QC stream
re: Mass labelling kickoff — 494-hand corpus × ~5 labellers; awaits owner go-ahead given cost scope
status: PROPOSAL — directive ready; owner sign-off required before dispatch (cost magnitude)
---

# Mass labelling kickoff directive (proposal)

## Context

494-hand corpus merged at master `9c8639a`. v3.2 protocol locked. v9 student model warm-start awaits labels.

## Proposal

| Item | Value |
|------|-------|
| Corpus | `data/corpus_revision_500_hand_2026-04-27.jsonl` (494 records) |
| Labellers | 5 sonnet labellers per hand (per established pilot pattern) |
| Total labels | 2470 (494 × 5) |
| Protocol | v3.2 (Rule 11 paired-board CHECK + KB §1.7 OVERRIDE villain_air_pct ≥ 0.20) |
| Output | `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` |
| Cost estimate | ~$120-200 (2470 labels × ~$0.05-0.08 each, sonnet rates) |
| Wall-time estimate | ~2-4 hours dispatch + collection |

## Reviewer chain

This is a **milestone PR** per memory `feedback_qc_required_before_approval.md`:
- gto-expert: label quality spot-check (e.g. 30 random labels for poker correctness vs v3.2)
- ml-architect: label distribution (refusal rate, RAISE/CALL/CHECK/BET/FOLD action mix per category)
- QC: paired V-Implementation-Spec-Match (label format matches contract) + V-Integration-Trace (a sample label can be loaded by the trainer pipeline end-to-end)

## Sequencing

```
Owner go-ahead → labeller dispatch (~2-4 hours) → labels land in data/
        ↓
Round 11 review chain (gto + ml + QC pre-merge per milestone gate)
        ↓
Synthesis → merge labels PR → student model warm-start training
        ↓
Round 12 review on trained model (held-out eval, 5 litmus tests)
```

## Blockers / open questions for owner

1. **Cost authorization**: ~$120-200. Approve?
2. **Labeller dispatch model**: same 5-labeller-per-hand pattern as Phase B pilot? Or revised (e.g. 3 labellers + tiebreaker)?
3. **PILOT_009 confidence**: post-Phase-10 fix verified clean by QC; 100% of records now have unique prior_actions. Proceed without manual spot-check?
4. **Tier 1 manifest 33→45**: was tagged as parallel separate PR. Do we want Tier 1 to land BEFORE mass labelling (so calibration set is current), or in parallel? My recommendation: parallel — Tier 1 expansion doesn't block Tier 2 mass labelling.

## What this directive does NOT do

- Dispatch labellers (waits for owner go-ahead)
- Touch v3.2 protocol
- Trigger student model training (separate downstream cycle)

## References

- Master `9c8639a` (PR #70 merged)
- Round 9 synthesis (494 FINAL): master `114961f`
- QC Audit 4 pre-merge: master `2793a34`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`

**Status: KICKOFF PROPOSAL OPEN. Owner go-ahead required on cost + labeller-dispatch model before dispatch fires.**
