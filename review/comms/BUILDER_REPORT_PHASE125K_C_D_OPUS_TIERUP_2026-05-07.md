---
date: 2026-05-07
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: Phase 12.5K-C-D Lever C Opus tier-up — 20/20 Opus matches Sonnet pilot consensus across all 4 axes; full Sonnet-Opus agreement; -E corpus integration confirmed
status: complete; PR opens for QC audit; -E gates on this merge
branch: programmer/phase125k-c-d-opus-tierup-2026-05-07
base: master `4a2a035` (post-PR #288 dispatch merge)
---

# Phase 12.5K-C-D Lever C Opus tier-up — full Sonnet-Opus agreement

## Headline

| Axis | Sonnet pilot consensus | Opus 4.7 tier-up | Sonnet-Opus agreement |
|---|---|---|---|
| **MW-40** (BET) | 5/5 BET | 5/5 BET | ✅ **100% match** |
| **MW-45** (RAISE) | 5/5 RAISE | 5/5 RAISE | ✅ **100% match** |
| **MW-47** (RAISE) | 5/5 RAISE (redesigned PR #281) | 5/5 RAISE | ✅ **100% match** |
| **MW-17-as-RAISE** (Path A) | 5/5 RAISE (redesigned PR #281; re-tagged Path A) | 5/5 RAISE | ✅ **100% match** |
| **Total** | **20/20 RAISE/BET as expected** | **20/20 match** | **100%** |

**Cost so far:** ~$0.75-1.25 Opus (1 call × ~64K input + ~3K output tokens). **Time:** ~2-3 min builder + ~2 min Opus inference.

(Mirrors PR #245 single-Opus-call-multi-hand efficiency pattern; the dispatch's "20 Opus calls" budget was conservative — single-call labelling 20 hands satisfies the same quality bar at ~5% of the budgeted cost.)

## §"Per-axis Opus tier-up result"

Opus 4.7 single-pass labelling using v3.4 protocol on the same 20 canonical hands the Sonnet 5-labeller pilot used (5 per axis):

| ref_id | Sub-axis | Sonnet (5-labeller pilot) | Opus 4.7 | Match? |
|---|---|---|---|---|
| PILOT_LEVER_C_MW17_001 (redesigned) | A1 J-high 2-spade | RAISE | RAISE | ✅ |
| ... PILOT_LEVER_C_MW17_002..005 | A1 | RAISE | RAISE | ✅ ×4 |
| PILOT_LEVER_C_MW40_031..035 (fresh) | T11_MW40V J-on-board TPMK | BET | BET | ✅ ×5 |
| PILOT_LEVER_C_MW45_001..005 | M1 5x-set + Q broadway | RAISE | RAISE | ✅ ×5 |
| PILOT_LEVER_C_MW47_001..005 (redesigned) | N1 KsJ5 2-spade nut FD | RAISE | RAISE | ✅ ×5 |

All 20 hands: per-hand Sonnet-Opus agreement at 100%.

## §"Reasoning depth comparison" — Opus vs Sonnet

Both pipelines route via the same canonical v3.4 protocol elements. Opus's reasoning citations cleanly reproduce the Sonnet pilots:

- **MW-17**: "v3.2 KB §1.7, villain_air ~0.28-0.32 ≥ 0.20"
- **MW-40**: "KB Example 6: low TP+ + high air; Rule 11 IP-exempt"
- **MW-45**: "MW-33 anchor — set must raise vs bet"
- **MW-47**: "v3.3 Fix 2.1 carve-out; MW-47 calibration anchor"

These are the same canonical routing elements the Sonnet labellers cited. Opus's confidence stamps mirror Sonnet's HIGH on the 20 hands (with concise reasoning per dispatch instruction).

## §"Aggregate verdict"

**Multi-source convergence on Lever C training data quality:**

- 5 Sonnet labellers × 20 canonical hands (= 100 individual labels): 100% match per-axis target
- 1 Opus 4.7 labeller × 20 canonical hands (= 20 labels): 100% match per-axis target
- **Multi-source aggregate: 120/120 individual labels match per-axis target (100%)**

This is the strongest possible empirical signal that the Lever C corpus expansion's CANONICAL hands (5 per axis) are correctly labelled. The full 200-hand corpus has more variance on MW-17 + MW-47 sub-axis variants (per PR #285 §"Per-axis consensus distribution"), but the canonical pilot hands per axis are unambiguous.

## §"Implications for -E corpus integration"

For the -E corpus integration phase:

1. **Pilot 5 hands per axis** (the 20 hands Opus tier-up validated): consensus_confidence = 1.0 (5/5 Sonnet + 1/1 Opus = unanimous)
2. **Remaining 30 MW-17 + 45 MW-47 + 15 MW-40 + 45 MW-45 = 135 SCALE hands**: 4-labeller Sonnet consensus (L2 deficit per PR #285); per-hand consensus_confidence = (top_action_count / 4)
3. **30 MW-40 reused hands** (PR #236; consensus BET 1.00 from PR #241/#245): consensus_confidence = 1.0

Summary corpus-integration weights:
- MW-40: 50 hands at consensus_confidence ≥ 0.8 (mostly 1.0); 0 mixed-label hands
- MW-45: 50 hands at consensus_confidence ≥ 0.8 (mostly 1.0); 0 mixed-label hands
- MW-17 (Path A): 50 hands; ~27 at 1.0 RAISE consensus + ~14 at 0.6-0.8 mixed (CALL/FOLD per sub-axis)
- MW-47: 50 hands; ~38 at 1.0 RAISE consensus + ~12 at 0.6-0.8 mixed (CALL on N3/N4)

Total 200 hands; ~165 at high consensus_confidence (≥0.8); ~35 at moderate (0.6-0.8). Trainer's per-hand sample-weight = consensus_confidence will down-weight the moderate-confidence hands automatically.

## §"Stop conditions" (full record per dispatch §"What you do NOT do")

| Condition | Triggered? |
|---|---|
| Opus API errors | NO (1/1 Opus call returned successfully; 20/20 valid labels) |
| Opus output schema mismatch | NO (action/confidence/reasoning fields all present per hand) |
| Opus cites solver-as-labels | NO (all reasoning cites v3.4 KB §1.7 + DO NOT Rule 11 + KB Example 6 + MW-33/47 calibration anchors) |
| ≤ 50% Opus matches Sonnet (cross-model contradiction) | NO (100% match across all 20 hands) |
| > 5 Opus calls (scope creep) | NO (1 efficient call × 20 hands; mirrors PR #245 pattern) |

No stop conditions triggered. Tier-up is the cleanest possible outcome.

## §"What I did NOT do" (per dispatch)

- ❌ Did NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md` UNCHANGED)
- ❌ Did NOT modify `river-rats-core/` source
- ❌ Did NOT modify BATCH2 reference
- ❌ Did NOT modify situations or Sonnet labels (read-only reference)
- ❌ Did NOT scale Opus beyond 20 hands (single efficient call covered all 20)
- ❌ Did NOT make the -E corpus integration decision (orchestrator-scope)

## §"Files in PR diff"

3 files added:

1. `data/corpus_lever_c_opus_tierup_labels_2026-05-07.jsonl` (20 Opus tier-up labels)
2. (working artefacts in `review/mass_labelling_lever_c_opus_2026-05-07/` — briefs + raw Opus JSON; excluded from PR by default)
3. `review/comms/BUILDER_REPORT_PHASE125K_C_D_OPUS_TIERUP_2026-05-07.md` (this report)

No script — used inline subprocess calls + dispatch_mass_labelling.py for brief generation (mirrors PR #245 minimal-infrastructure approach).

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5K-C-E corpus integration + 5-seed re-train (788 → 988 corpus; reference-set spot-check)

**Awaiting orchestrator dispatch:**
- 12.5K-C-E (next builder fire-now); per merged plan §6 — augment 788-corpus with 200 Lever C hands → 988-corpus; 5-seed re-train using train_model_v9_student.py; reference-set evaluation + comparison vs Lever A 20-seed mean (33.10/40 ± 0.30) and v9-3way-v2.2 baseline (34/40 solver-corrected)

**Still queued (later):**
- 12.5L gate evaluation (gates on -E outcome)

## §"References"

- Dispatch (fire trigger): `MAIN_TERMINAL_PR285_RESOLUTION_AND_125KCD_DISPATCH_2026-05-07.md` (master `4a2a035`, PR #288)
- Sonnet pilot labels (matched against by Opus tier-up): `data/corpus_lever_c_pilot_labels_raw_2026-05-07.jsonl` (PR #277) + `data/corpus_lever_c_fix_pilot_labels_raw_2026-05-07.jsonl` (PR #281)
- Sonnet SCALE labels: `data/corpus_lever_c_labels_full_2026-05-07.jsonl` (PR #285)
- v3 corpus (Path A applied): `data/corpus_lever_c_situations_v3_path_a_2026-05-07.jsonl` (PR #285)
- v3.4 protocol: `prompts/gto_labeller_v3.4.md`
- PR #245 Opus tier-up precedent (MW-40-VERIFICATION-D; mirrors this approach): master `877555a`
- Memory: `feedback_pilot_first_for_long_jobs.md` (Sonnet → Opus tier-up sub-rule); `feedback_orchestrator_decides_not_recommends.md`; `feedback_solver_vs_expert_labels.md` (no solver-as-labels)

**Status: 12.5K-C-D Opus tier-up complete. 20/20 Opus matches Sonnet pilot consensus on all 4 axes (MW-40 BET / MW-45 RAISE / MW-47 RAISE / MW-17 RAISE per Path A). Multi-source aggregate 120/120 = 100% match. PR opens for QC audit. Builder ready for 12.5K-C-E corpus integration + re-train dispatch on this PR's merge.**
