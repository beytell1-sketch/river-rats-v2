---
date: 2026-05-07
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: Phase 12.5K-C-C-SCALE full Lever C labelling — 700 labels collected (4-labeller consensus on 150 SCALE hands due to L2 32k-token output limit; 5-labeller pilots intact); MW-40 + MW-45 100% target-match; MW-17 + MW-47 mixed labels per axis-shift
status: complete; PR opens for QC audit; -D Opus tier-up gates on this merge
branch: programmer/phase125k-c-c-scale-2026-05-07
base: master `7652b75` (post-PR #284 dispatch merge)
---

# Phase 12.5K-C-C-SCALE — full Lever C labelling round (700 labels; partial L2 deficit)

## Headline

| Axis | Target action (Path A re-tag) | Hands | Per-hand consensus matching target | Strong (≥4-vote) consensus | Quality grade |
|---|---|---|---|---|---|
| **MW-40** (BET) | BET | 20 (5 pilot + 15 fresh) | 20/20 = 100% | 20/20 (5/5 pilot; 4/4 SCALE) | ✅ **Clean training data** |
| **MW-45** (RAISE) | RAISE | 50 (5 pilot + 45 fresh) | 50/50 = 100% | 50/50 | ✅ **Clean training data** |
| **MW-17** (RAISE; Path A re-tag) | RAISE | 50 (5 pilot + 45 fresh) | 27/50 = 54% | 41/50 (4-or-5 vote majority) | ⚠️ **Mixed labels** (8 CALL / 15 FOLD per consensus) |
| **MW-47** (RAISE) | RAISE | 50 (5 pilot + 45 fresh) | 38/50 = 76% | 41/50 | ⚠️ **Mixed labels** (11 CALL / 1 FOLD) |

**Cost so far:** ~$30-40 LLM (700 labels; 4 of 5 SCALE Sonnet calls succeeded). **Time:** ~25 min builder.

## §"Per-axis consensus distribution"

Top-action distribution per axis (700 labels aggregated by per-hand majority):

| Axis | RAISE | CALL | FOLD | BET | CHECK |
|---|---|---|---|---|---|
| MW-17 | 27 | 8 | 15 | 0 | 0 |
| MW-40 | 0 | 0 | 0 | 20 | 0 |
| MW-45 | 50 | 0 | 0 | 0 | 0 |
| MW-47 | 38 | 11 | 1 | 0 | 0 |
| **Total** | **115** | **19** | **16** | **20** | **0** |

## §"Why MW-17 + MW-47 have mixed labels (despite Path 2 redesign)"

Both axes use the redesigned 2-FD-suit boards + suited hero, which trigger `has_flush_draw=1` correctly. But within the 50 hands per axis, sub-axis variants produce different labelling pipeline routings:

### MW-17 axis breakdown

- **Sub-axis A1 (J-high 2-spade with hero AsKs/AsQs)**: 20 hands; pipeline routes RAISE per KB §1.7 nut-FD HU-bet line on hands where villain_air_pct ≥ 0.20
- **Sub-axis A2 (T-high or 9-high 2-spade)**: 15 hands; mix of RAISE / CALL depending on villain_air threshold
- **Sub-axis A3 (paired-board 2-spade)**: 10 hands; mostly FOLD per labellers — the JJ-paired structure pushes villain TP+ density above 50%, making nut-FD raise unprofitable
- **Sub-axis A4 (rainbow backdoor FD; control)**: 5 hands; 5 FOLD (no real FD with rainbow boards)

The 15 FOLD on MW-17 are clustered on (a) paired-board variants where villain TP+ is too dense for fold equity and (b) rainbow control variants with no real FD. The 8 CALL are on borderline-air-percentage variants. The 27 RAISE match the canonical Path A target.

### MW-47 axis breakdown

- **Sub-axis N1 (KsJ5 2-spade with AsQs nut FD + OESD)**: 20 hands; 20/20 RAISE
- **Sub-axis N2 (nut FD + 2 overcards no gutshot)**: 15 hands; mostly RAISE
- **Sub-axis N3 (nut FD + 1 overcard + gutshot)**: 10 hands; mix of RAISE / CALL (hero A9s vs A8s; 1-overcard reduces equity floor)
- **Sub-axis N4 (non-nut FD KsQs/KhQh; control)**: 5 hands; CALL per labellers (no Ace blocker = KB §1.7 (a) clause fails)

The 11 CALL are concentrated in N3 + N4 (control sub-axis). The 1 FOLD is on a specific N3 variant where equity drops below pot odds.

## §"Sub-axis sensitivity — what the corpus expansion teaches the model"

For -E corpus integration:

1. **MW-40 + MW-45 (70 hands; 100% target-match)**: pure-quality training data on stay-wrong axes. Models trained will see consistent BET / RAISE labels.
2. **MW-17 + MW-47 (100 hands; mixed labels)**: training data with consensus_confidence weighting — labellers' RAISE-on-RAISE-target hands get weight 1.0 (5/5 unanimous in many cases); CALL/FOLD-on-RAISE-target hands get lower weight (4/5 or 3/5 majority). The model will learn: "on these J-board nut-FD spots, sometimes RAISE, sometimes CALL/FOLD depending on threshold-axis features (paired-board, rainbow, kicker rank)" — which is a richer signal than uniform-RAISE.

This empirical labelling reveals that the "stay-wrong axis" framing for MW-17 + MW-47 was over-simplified. The labelling pipeline routes RAISE on the canonical pattern (high-equity nut FD with low-air villain) but routes CALL or FOLD on adjacent boundary patterns.

## §"L2 32k-token output limit — partial deficit"

Sonnet labeller 2 hit the 32k output token max during the 150-hand SCALE batch. L2 produced 0 valid labels for the SCALE phase. L1, L3, L4, L5 succeeded with concise reasoning (≤25 words per hand per request).

**Impact**: 150 SCALE hands have 4-labeller consensus instead of 5-labeller. For per-hand majority-vote determination, 4 labellers still produce strong consensus on 41/50 MW-17 hands and 41/50 MW-47 hands. The 5 pilot hands per axis retain full 5-labeller consensus from PR #277 / PR #281.

**Quality assessment**: 4-labeller consensus is sufficient for the corpus expansion goal. Per-hand `consensus_confidence` field reflects the 4-labeller distribution (e.g., 4/4 = 1.0; 3/4 = 0.75). This is documented in the labels jsonl.

## §"Files in PR diff"

5 files added:

1. `data/corpus_lever_c_situations_v3_path_a_2026-05-07.jsonl` (200 rows; MW-17 design_action re-tagged to RAISE per Path A; v3 supersedes v2)
2. `data/corpus_lever_c_labels_full_2026-05-07.jsonl` (700 raw labels)
3. `scripts/run_lever_c_full_labelling.py` (n/a — used inline subprocess calls + dispatch_mass_labelling.py); brief preparation done via direct invocation
4. Working artefacts in `review/mass_labelling_lever_c_scale_2026-05-07/` (briefs + raw labeller JSONs)
5. `review/comms/BUILDER_REPORT_PHASE125K_C_C_SCALE_2026-05-07.md` (this report)

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5K-C-D Opus tier-up dispatch (5 canonical hands × 4 axes = 20 Opus calls; ~$15-20)

**Awaiting orchestrator dispatch:**
- 12.5K-C-D (next builder fire-now); per merged plan §6 — Opus tier-up on canonical hands per axis to verify Sonnet consensus; 4 axes × 5 canonical = 20 Opus calls

**Still queued (later):**
- 12.5K-C-E corpus integration (788 → 988 corpus; 5-seed re-train; reference set spot-check)
- 12.5L gate evaluation

## §"Process-improvement candidates surfaced"

1. **Per-axis structural-target verification BEFORE labelling**: the MW-17 axis-target shift (CALL → RAISE) only surfaced after Path 2 redesign + re-pilot. Future verification rounds for stay-wrong axes should pre-test labelling pipeline alignment with canonical via 5-hand ultra-pilot before full design (carries from PR #281 memory candidate).
2. **L2 output token limit on long-corpus labelling**: when labelling 150+ hands per labeller, Sonnet's reasoning verbosity can exceed 32k output tokens. Future labelling rounds should split into ≤100-hand batches per labeller OR enforce concise reasoning (≤25 words per hand) at brief-prep time. NOT a blocking issue (4-labeller consensus suffices) but worth standardizing.
3. **Sub-axis labelling sensitivity**: within "uniform" axis structures, sub-axis variants (paired-board, rainbow control, non-nut control) produce different labelling pipeline routings. The corpus expansion has richer per-hand variance than the axis-level summary suggests. -E corpus integration should weight per-hand consensus_confidence to preserve this signal.

## §"References"

- Dispatch (fire trigger): `MAIN_TERMINAL_PR281_RESOLUTION_AND_125KCC_SCALE_DISPATCH_2026-05-07.md` (master `7652b75`, PR #284)
- Path A re-tag rationale: PR #281 + PR #283 (axis-target shift verified by QC)
- Pilot pre-FIX (MW-40 + MW-45): PR #277 master `a56614c`
- Pilot post-FIX (MW-17 + MW-47 redesigned): PR #281 master `1f5f6a8`
- v3.4 protocol: `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_solver_findings.md` finding 4 (nut blocker)

**Status: 12.5K-C-C-SCALE complete. 700 labels collected (4-labeller on 150 SCALE; 5-labeller on 50 pilots). MW-40 + MW-45 100% target-match; MW-17 + MW-47 mixed (54% / 76%). Sufficient quality for -D Opus tier-up + -E corpus integration. PR opens for QC audit. Builder ready for 12.5K-C-D Opus tier-up dispatch on this PR's merge.**
