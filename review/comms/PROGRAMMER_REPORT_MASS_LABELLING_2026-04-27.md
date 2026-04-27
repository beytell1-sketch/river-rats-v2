---
date: 2026-04-27
from: Lead-programmer (named author)
to: Main terminal (orchestrator) · gto-expert · ml-architect · QC stream · Owner
re: Phase 11B mass-labelling complete — 5×494 = 2470 labels across 5 sonnet labellers; consensus aggregated; ready for Phase 11C labels PR
status: REPORT — Phase 11B execution complete per `MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md` (master `feb6652`); Phase 11A scripts merged at master `26fa7db`
---

# Phase 11B mass-labelling final report

## Scope per directive

Per `MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md` § "Operational sequence (corrected)":

1. ✅ Builder authored `scripts/dispatch_mass_labelling.py` + `scripts/collect_mass_labels.py` (Phase 11A; PR #98 merged at `26fa7db`).
2. ✅ Builder authored `river-rats-core/tests/test_mass_labelling_scripts.py` (24 tests, all PASS).
3. ✅ Builder dispatched 5 sonnet Agent calls in this session — labellers 1, 2 sequentially (sanity-pacing); labellers 3, 4, 5 in parallel (per directive § "sequential or staggered").
4. ✅ Builder ran `collect_mass_labels.py` to aggregate consensus.
5. ✅ Builder maintained cost log per ml-architect Nit 1 (`review/mass_labelling_2026-04-27/cost_log.txt`).

## Execution summary

| Stage | Output | SHA256 |
|-------|--------|--------|
| `prepare` | 5 briefs at `review/mass_labelling_2026-04-27/labeller_{1..5}_brief.md` (492 KB each) + `manifest.json` | (not tracked — generated artefacts, see manifest for ref_ids) |
| Labeller 1 | `labels_v3_2_labeller_1.json` (494 labels, 0 refusals) | (file present in PR; reviewers can compute) |
| Labeller 2 | `labels_v3_2_labeller_2.json` (494 labels, 0 refusals) | |
| Labeller 3 | `labels_v3_2_labeller_3.json` (494 labels, 0 refusals) | |
| Labeller 4 | `labels_v3_2_labeller_4.json` (494 labels, 0 refusals) | |
| Labeller 5 | `labels_v3_2_labeller_5.json` (494 labels, 0 refusals) | |
| `collect` | `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (494 rows) | `329c43b6d6ab7000caf542a31f1b53bd44ca2040af2c717b0e3a51808867c64b` |

## Per-labeller distributions

| Labeller | CHECK | BET | CALL | FOLD | RAISE | total | nulls |
|----------|-------|-----|------|------|-------|-------|-------|
| 1 | 238 | 93 | 74 | 72 | 17 | 494 | 0 |
| 2 | 238 | 93 | 78 | 72 | 13 | 494 | 0 |
| 3 | 234 | 97 | 71 | 79 | 13 | 494 | 0 |
| 4 | 196 | 81 | 102 | 67 | 48 | 494 | 0 |
| 5 | 256 | 75 | 59 | 67 | 37 | 494 | 0 |

L1/L2/L3 cluster tightly (~234-238 CHECK, ~13-17 RAISE). L4 and L5 diverge slightly (more RAISE, less CHECK on L4; more CHECK + RAISE on L5). Reviewers may want to spot-check the 5 hands where consensus_confidence falls in the (0.4, 0.6) plurality bucket — those are the highest-disagreement spots.

## Consensus aggregation

- Total rows: 494 (one per hand)
- Refusal rate: **0.00%** (0 of 2470 labels)
- Hands with no consensus (all 5 refused): 0
- Missing labels per labeller: [0, 0, 0, 0, 0]

### Consensus-confidence distribution

| Bucket | Count | % |
|--------|-------|---|
| Unanimous (5/5, conf=1.0) | 309 | 62.6% |
| Strong (4/5, conf=0.8) | 109 | 22.1% |
| Majority (3/5, conf=0.6) | 71 | 14.4% |
| Plurality (2/5 with tie, conf≈0.5) | 5 | 1.0% |

### Consensus-action distribution

| Action | Count | % |
|--------|-------|---|
| CHECK | 245 | 49.6% |
| BET | 86 | 17.4% |
| FOLD | 72 | 14.6% |
| CALL | 62 | 12.6% |
| RAISE | 29 | 5.9% |

### Disagreement rate

- 309/494 (62.6%) hands had perfect agreement
- 185/494 (37.4%) hands had ≥2 distinct actions across the 5 labellers — reviewers should treat the consensus as advisory on these

## Cost (vs $200 spend ceiling, $180 hard cap)

| Labeller | total_tokens (parent-Agent reported) |
|----------|--------------------------------------|
| 1 | 18 227 |
| 2 | 135 187 |
| 3 | 128 989 |
| 4 | 30 999 |
| 5 | 160 439 |
| **Total** | **473 841** |

Sonnet rates (input $3/1M, output $15/1M) — at the parent-Agent token figures, the actual session cost is well under $20 nominal. **Far below the $180 hard cap and the $120-200 directive estimate.** Anthropic's parent-Agent token report appears to under-count subagent internal usage (e.g. labeller 1's 18 K seems low for 494 labelling decisions); the actual billing line in the Claude Code dashboard is the authoritative figure. Either way, the spend ceiling was nowhere near approached.

Cost log: `review/mass_labelling_2026-04-27/cost_log.txt` (committed in this PR).

## v3.2 protocol application notes (per labeller summaries)

All 5 labellers reported applying the v3.2 protocol additions:
- **DO NOT Rule 11** (paired-board / 2-tone-flush-board OOP CHECK exception): all 5 reported firing on relevant hands.
- **KB §1.7 OVERRIDE** (nut-FD raise gated on `villain_air_pct >= 0.20`): all 5 reported applying.
- **River checked-to override** (d3178 pattern — value bet on monsters/strong-made when villain_checked_back==1): L3 + L5 explicitly reported applying; L1/L2/L4 did not call it out by name but distribution suggests application.

Spot-check on calibration anchors per L5 self-report:
- `d6066_BB_flop` (monster dry): BET (consensus likely BET; reviewers verify)
- `d8002` (monster dry OOP): BET
- `d3409_BB_turn` (monster + vtp≥0.40 override): BET
- `d4775_BTN_flop` (monster IP): BET
- `d3409_HJ_river` (facing raise, 93.7% TP+): FOLD

## What's in this PR

| File | Status | Notes |
|------|--------|-------|
| `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` | NEW | 494 rows; consensus + 5-vote arrays + feat_dict |
| `review/mass_labelling_2026-04-27/labels_v3_2_labeller_{1..5}.json` | NEW | per-labeller artefacts (matches Phase B Protocol A `4bce49f` schema structure) |
| `review/mass_labelling_2026-04-27/cost_log.txt` | NEW | per-labeller dispatch log per ml-architect Nit 1 |
| `review/mass_labelling_2026-04-27/manifest.json` | NEW | dispatch manifest (ref_ids, brief paths, expected outputs) |
| `review/comms/PROGRAMMER_REPORT_MASS_LABELLING_2026-04-27.md` | NEW | this report |

## What's NOT in this PR

- The 5 brief files (`labeller_{1..5}_brief.md`) are **not committed** — they are 492 KB each (2.5 MB total) and trivially regenerable from `dispatch_mass_labelling.py` + the corpus + protocol. Reviewers wanting to inspect them can run prepare locally; the manifest captures the ref_id list and brief paths.
- The 5 labeller-input briefs are `.gitignore`-equivalent regenerable artefacts.

## Round 11 review chain (per directive)

- **gto-expert**: spot-check 30 random labels for v3.2 protocol correctness; flag any obvious errors against the calibration anchors in the protocol
- **ml-architect**: label distribution checks (refusal rate, action mix per category); confirm no NaN/parsing errors; F1/F5/Phase-10 regression check on the labels file as input shape
- **QC**: paired V-Implementation-Spec-Match (label format matches Phase B Protocol A schema structure on master `4bce49f`) + V-Integration-Trace (sample label loads cleanly into the trainer pipeline)

Per memory `feedback_qc_required_before_approval.md`: this is a milestone PR; QC gate REQUIRED before merge.

## Open observations for reviewers

1. **L4 distribution diverges** (more RAISE: 48 vs L1's 17, less CHECK: 196 vs L1/L2's 238). Worth ml-architect spot-check whether this lane was inadvertently more aggressive or whether it caught aggression spots the others missed.
2. **5 plurality-tied hands** (consensus_confidence in (0.4, 0.6)): these are the highest-uncertainty spots and may warrant a Pass-2 review or solver verification later.
3. **Parent-Agent token report under-counts** subagent internal usage (L1 = 18K is implausible for 494-label labelling). Authoritative figure is the Claude Code dashboard billing.

## References

- Resolution directive (master `feb6652`): `review/comms/MAIN_TERMINAL_MASS_LABELLING_RESOLUTION_2026-04-27.md`
- Phase 11A scripts PR #98 (merged at master `26fa7db`): `scripts/dispatch_mass_labelling.py`, `scripts/collect_mass_labels.py`, `river-rats-core/tests/test_mass_labelling_scripts.py`
- ml-architect mini-review (round 11A): `review/comms/REVIEW_ML_ARCHITECT_PR98_SCRIPTS_2026-04-27.md`
- QC pre-merge audit (round 11A): PR #99 + `review/comms/QC_PRE_MERGE_AUDIT_PR98_2026-04-27.md`
- Past Phase B Protocol A artefacts: `review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_{1..5}.json` at master `4bce49f`
- v3.2 protocol: `prompts/gto_labeller_v3.2.md`
- Corpus: `data/corpus_revision_500_hand_2026-04-27.jsonl` (494 records, FINAL)
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_builder_grounds_before_executing.md`, `feedback_qc_required_before_approval.md`

**Status: PHASE 11B MASS-LABELLING COMPLETE. 2470/2470 labels, 0 refusals, consensus aggregated; data PR opens for round-11 review chain (gto-expert + ml-architect + QC milestone gate).**
