---
date: 2026-05-07
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #289 — Phase 12.5K-C-D Lever C Opus tier-up (20/20 Sonnet-Opus match; 100% across 4 axes; Path A validated) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR289_2026-05-07.md (master `b7404eb`)
pr_branch: programmer/phase125k-c-d-opus-tierup-2026-05-07
qc_branch: qc/pr289-125kcd-opus-tierup-review-2026-05-07
---

# PR #289 — pre-merge QC verdict: PASS (0/0/0)

37th solo cycle. **Lever C Opus tier-up complete; 20/20 Sonnet-Opus match across 4 axes (100%).** Path A re-tag (MW-17 → RAISE) validated at Opus tier — strongest possible empirical signal that Lever C corpus expansion's canonical hands are correctly labelled. Multi-source aggregate **120/120 individual labels** at 100% target-match (5 Sonnet × 20 hands + 1 Opus × 20 hands = 120).

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict | ✅ PASS (2 files; script reused) |
| 2. Opus 4.7 model id (`claude-opus-4-7` × 20) | ✅ PASS |
| 3. Same v3.4 prompt (protocol_version=v3.4 × 20) | ✅ PASS |
| 4. 5 canonical hands per axis × 4 axes = 20 | ✅ PASS |
| 5. No solver-as-labels (0/20) | ✅ PASS |
| 6. Sonnet-Opus comparison correctness (100% per axis) | ✅ PASS |
| 7. TC-X-DISPATCH-COMPLIANCE (16th formal exercise) | ✅ PASS |

**Verdict: PASS — clear to merge. -E corpus integration gates on PR merge with 120/120 unanimous canonical labels.**

## §1 — Diff scope strict

`git diff --stat master...origin/programmer/phase125k-c-d-opus-tierup-2026-05-07`:

```
 data/corpus_lever_c_opus_tierup_labels_2026-05-07.jsonl              |  20 ++++
 review/comms/BUILDER_REPORT_PHASE125K_C_D_OPUS_TIERUP_2026-05-07.md  | 130 +++++++++++++++++++++
 2 files changed, 150 insertions(+)
```

2 files (labels jsonl + builder report). **Note:** trigger §1 expected "exactly 3 files (script + labels + report)"; builder delivered 2 files (labels + report) without a new script — reusing existing Opus tier-up infrastructure from PR #245 (`scripts/run_125i_mw40_verif_opus_tierup.py`) per builder-discretion. The actual deliverable (labels + report) is complete; absence of new script means the work was implementable with existing tooling.

This is a benign deviation from dispatch's expected file count, not a substantive issue. Builder report explicitly references the Opus tier-up methodology mirrors PR #245.

Owner-scope perimeter held (no v3.x / BATCH2 / core / corpus / training-data / memory edits).

## §2 — Opus 4.7 model id correctness

QC inspection of all 20 rows: `model = claude-opus-4-7` for every row. Matches PR #245 precedent. **PASS.**

## §3 — Same v3.4 prompt

QC inspection of all 20 rows: `protocol_version = v3.4` for every row. v3.x prompts unchanged in PR diff (perimeter sweep §1). **PASS.**

## §4 — 5 canonical hands per axis × 4 axes = 20

QC verified canonical hand selection:

| Axis | Selected hands | Count |
|---|---|---|
| MW-17 | PILOT_LEVER_C_MW17_001..005 | 5 ✓ |
| MW-40 | PILOT_LEVER_C_MW40_031..035 (the FRESH 5 of the 50; 001-030 reused per PR #245) | 5 ✓ |
| MW-45 | PILOT_LEVER_C_MW45_001..005 | 5 ✓ |
| MW-47 | PILOT_LEVER_C_MW47_001..005 | 5 ✓ |
| **Total** | — | **20 ✓** |

**Smart selection:** MW-40 axis selected 031..035 (the genuinely-fresh hands) rather than 001..030 which already have authoritative Opus tier-up from PR #245. This avoids duplicate Opus labelling on the reused 30. **PASS.**

## §5 — No solver-as-labels

QC scanned all 20 Opus reasoning blocks: 0 solver-as-labels citations. Authorities cited: v3.4 protocol surface (KB §1.7 nut-FD carve-out; v3.3 Fix 2.1; v3.2 OVERRIDE threshold) + composition quad + bucket-first hand classification + MW-47 calibration anchor (descriptive cross-reference, not solver-as-label). **PASS.**

## §6 — Sonnet-Opus comparison correctness

QC verified per-axis Opus action distribution:

| Axis | Target | Opus actions (5/5 per axis) | Sonnet pilot consensus (per builder report) | Match |
|---|---|---|---|---|
| MW-17 (Path A target RAISE) | RAISE | 5 RAISE / 5 HIGH | 5/5 RAISE | ✅ 100% match |
| MW-40 (target BET) | BET | 5 BET / 5 HIGH | 5/5 BET | ✅ 100% match |
| MW-45 (target RAISE) | RAISE | 5 RAISE / 5 HIGH | 5/5 RAISE | ✅ 100% match |
| MW-47 (target RAISE) | RAISE | 5 RAISE / 5 HIGH | 5/5 RAISE | ✅ 100% match |

**Multi-source aggregate per builder report §"Aggregate verdict":**
- 5 Sonnet labellers × 20 canonical hands = 100 individual labels: 100% match per-axis target
- 1 Opus 4.7 × 20 canonical hands = 20 labels: 100% match per-axis target
- **Total: 120/120 individual labels at 100% target-match**

This is the strongest possible empirical signal for the Lever C corpus expansion's canonical hands. The full 200-hand corpus has more variance on MW-17 + MW-47 sub-axis variants (per PR #285 §"Per-axis consensus distribution"), but the canonical pilot hands per axis are unambiguous.

**Path A re-tag validated at Opus tier:** MW-17 axis-target shift (CALL → RAISE) confirmed by 5/5 Opus RAISE consensus. The Lever C-C-FIX (PR #281) HALT-escalate diagnosis is now empirically validated multi-source.

**PASS.**

## §7 — TC-X-DISPATCH-COMPLIANCE (16th formal exercise)

| Compliance check | Match |
|---|---|
| Path A applied (MW-17 axis-target = RAISE) | ✅ 5/5 Opus RAISE on MW-17 confirms Path A validation |
| Opus tier-up on canonical hands per axis | ✅ 5 per axis × 4 axes = 20 |
| Same v3.4 prompt | ✅ protocol_version=v3.4 × 20 |
| Mirror PR #245 pattern | ✅ same Opus 4.7 model + same evaluation methodology |
| Builder did NOT modify v3.x prompts | ✅ v3.x untouched in PR diff |
| Builder did NOT modify Sonnet labels | ✅ Sonnet labels from PR #285 unchanged (referenced via PR #285 master) |

Per `feedback_listen_to_orchestrator_always.md` + `feedback_explicit_action_trigger.md`: builder discipline matches dispatch authoritative wording.

Class durable on 16th formal exercise. **PASS.**

## §"Implications for -E corpus integration"

Builder report §"Implications for -E corpus integration" provides a clean roadmap for Lever C corpus integration at -E:

- Pilot 5 hands per axis (the 20 Opus tier-up validated): consensus_confidence = 1.0 (5/5 Sonnet + 1/1 Opus = unanimous) — top-quality training rows
- Remaining 135 SCALE hands (200 - 30 reused - 20 pilot - 15 partially-overlapping): 4-labeller Sonnet consensus per PR #285; consensus_confidence = (top_action_count / 4)
- 30 MW-40 reused hands: consensus_confidence = 1.0 (PR #241/#245 multi-source)

Predicted final Lever C corpus distribution per builder report:
- MW-40: 50 hands at consensus_confidence ≥ 0.8 (mostly 1.0)
- MW-45: 50 hands at consensus_confidence ≥ 0.8 (mostly 1.0)
- MW-17 (Path A): 50 hands; ~27 at 1.0 RAISE consensus + ~14 at 0.6-0.8 mixed
- MW-47: 50 hands; ~38 at 1.0 RAISE consensus + ~12 at 0.6-0.8 mixed

Total 200 hands integrated into 988-corpus (788 + 200) at -E.

QC notes: this is sound corpus-integration planning. Mixed-confidence hands (0.6-0.8) are training-data-suitable — the trainer's sample-weight = consensus_confidence will down-weight them automatically (per PR #253's training methodology).

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (18th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (16th formal exercise; durable)**
- **TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE (entry #14; 6th informal exercise — Opus tier-up confirms Sonnet's per-axis distinct rule chains)** — class extends across model classes consistently
- **TC-X-DISPATCH-PREDICTION-VERIFICATION (entry #11; 6th formal exercise)** — Path A prediction (MW-17 → RAISE) validated by Opus 5/5 RAISE
- TC-X-INTRA-PLAN-CONSISTENCY (informal continuation)

## Smarter-over-time observations

**Lever C cycle complete with full multi-source validation:**

PR #228-249 MW-40 verification → PR #269 Lever C-A design → PR #277 -C pilot HALT (factory diagnosis) → PR #281 -C-FIX (MW-17 axis-target shift) → PR #285 -C-SCALE (700 labels Path A) → **PR #289 -C-D Opus tier-up (20/20 100%)** → -E corpus integration next.

The Lever C 6-PR sequence is now complete with multi-source consensus on canonical hands. Path A re-tag (MW-17 → RAISE) was a non-trivial decision that:
1. Discovered at PR #277 (factory FD-suit failure on MW-17 + MW-47)
2. Diagnosed at PR #281 (MW-17 axis-target shift; canonical-vs-pipeline mismatch parallel to MW-40)
3. Decided by orchestrator at PR #283 (Path A ratification)
4. Applied at PR #285 (700 labels with Path A)
5. **Validated at PR #289 (Opus 5/5 RAISE confirms Path A)**

This validates the canonical-vs-pipeline mismatch pattern (entry-watchlist class TC-X-CANONICAL-HAND-CLASS-PRESERVATION): MW-17's canonical reference (AdKs on Jd8d4c, backdoor-FD-class) doesn't match the parametric expansion (suited-FD class), so the labelling pipeline correctly RAISEs on the suited-FD parametric variants. The training data should reflect what the pipeline produces on the parametric class, not what canonical's narrow class assumes.

**Class durability:** 6 informal/formal exercises of TC-X-DISPATCH-PREDICTION-VERIFICATION + 6 informal exercises of TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE + 16 formal TC-X-DISPATCH-COMPLIANCE exercises. The QC class system has accompanied this cycle from end to end.

## Audit cost / time

- Wall clock: ~12 min (data audit + per-axis verification + Sonnet-Opus comparison + verdict authoring). Within 10-15 min estimate.
- LLM cost: $0.

## Gates

PR #289 cleared from QC side. Per dispatch §"What gates":
- PR #289 merge: clear from QC; multi-source 120/120 100% target-match
- 12.5K-C-E corpus integration dispatch: gates on PR #289 merge

Lever C corpus expansion (788 → 988 = +200 hands; +700 fresh labels + 150 reused-or-MW-40 labels) ready for -E integration into 12.5K combined re-train.

## References

- 12.5K-C-D dispatch: `MAIN_TERMINAL_PR285_RESOLUTION_AND_125KCD_DISPATCH_2026-05-07.md` (master `4a2a035`, PR #288)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR289_2026-05-07.md` (master `b7404eb`)
- Builder report: `BUILDER_REPORT_PHASE125K_C_D_OPUS_TIERUP_2026-05-07.md` (in PR #289; 130L)
- Lever C-C-SCALE source (PR #285 Sonnet labels): master via PR #285
- PR #245 Opus tier-up precedent: master `877555a`
- v3.4 protocol: `prompts/gto_labeller_v3.4.md` (KB §1.7; v3.3 Fix 2.1; v3.2 OVERRIDE)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: VERDICT = PASS. PR #289 cleared for merge from QC side. Multi-source 120/120 individual labels at 100% target-match (5 Sonnet + 1 Opus per canonical hand × 20 hands × 4 axes). Path A re-tag validated at Opus tier. 37th solo QC cycle. TC-X-DISPATCH-COMPLIANCE 16th formal exercise; TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE 6th informal exercise; TC-X-DISPATCH-PREDICTION-VERIFICATION 6th formal exercise. Lever C cycle complete; -E corpus integration next.**
