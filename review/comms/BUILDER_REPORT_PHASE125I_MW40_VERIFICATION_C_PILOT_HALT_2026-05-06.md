---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: 12.5I-MW40-VERIFICATION-C pilot HALT — uniform 25/25 BET across 5 pilot hands × 5 Sonnet labellers; structural prediction CHECK directly contradicted; awaiting orchestrator decision (scale-anyway vs halt-verification)
status: HALT — pilot gate triggered per dispatch §"Stop conditions"; full 25-hand × 5-labeller run NOT fired
branch: programmer/phase125i-mw40-verification-c-labelling-2026-05-06
base: master `3927024` (post-PR #240 dispatch merge)
---

# Phase 12.5I-MW40-VERIFICATION-C — pilot HALT (uniform BET; CHECK prediction contradicted)

## Headline

| Step | Result |
|---|---|
| Pilot prep | ✅ 5 pilot hands × 5 labeller briefs prepared (review/mass_labelling_mw40v_2026-05-06/pilot/) |
| Pilot run | ✅ 5 sonnet labellers dispatched in parallel; all 5 returned successfully; 25/25 labels written |
| Pilot consensus | **BET 25/25 = 100% (uniform across all 5 hands × 5 labellers)** |
| Plan §3 prediction | **CHECK uniform** (target ≥27/30 at full scale for graduation) |
| Pilot gate | ⛔ **TRIGGERED — STOP per dispatch §"Stop conditions"**: "If pilot consensus is BET-mixed or RAISE-mixed (≥3/5 hands have <3/5 CHECK) → STOP and report to orchestrator" |
| Full 25-hand × 5-labeller run | ❌ **NOT FIRED** — awaiting orchestrator decision (scale-anyway vs halt-verification) per dispatch §"Stop conditions" |

**Cost so far:** ~$1-2 (pilot only; 5 sonnet calls × ~10K input + ~3K output tokens each). **Time so far:** ~12 min builder including prep + dispatch + collect.

## §"Pilot batch results" — 5 hands × 5 labellers

```
ref_id                       votes      consensus  confidence
PILOT_MW40_VERIF_001         BET:5      BET        1.00 (5/5)
PILOT_MW40_VERIF_011         BET:5      BET        1.00 (5/5)
PILOT_MW40_VERIF_016         BET:5      BET        1.00 (5/5)
PILOT_MW40_VERIF_025         BET:5      BET        1.00 (5/5)  ← JcJh4s paired-J boundary
PILOT_MW40_VERIF_026         BET:5      BET        1.00 (5/5)
```

Pilot composition (per dispatch §"Pick the 5 pilot hands"):
- 2 sub-axis A: PILOT_MW40_VERIF_001 (Js9c5h, TdJc) + PILOT_MW40_VERIF_011 (Js8d3h, TcJd; builder-added in -B)
- 2 sub-axis C standard: PILOT_MW40_VERIF_016 (Jh5c2d, TsJc) + PILOT_MW40_VERIF_026 (Jh7s3d, TcJd; builder-added in -B)
- 1 boundary: PILOT_MW40_VERIF_025 (JcJh4s, ThJd; paired-J trips)

All 5 hands consensus BET at 1.00 confidence. Including the JcJh4s paired-J boundary case (which the dispatch flagged as "the most exotic structural test case"). Even on trips, all 5 labellers chose BET.

## §"Per-labeller summary"

All 5 labellers reported the same overall pattern:

| Labeller | Action distribution | Confidence stamps |
|---|---|---|
| 1 | 5 BET / 0 other | 2 HIGH, 3 MEDIUM (estimated; see raw labels) |
| 2 | 5 BET / 0 other | 2 HIGH, 3 MEDIUM |
| 3 | 5 BET / 0 other | 4 HIGH, 1 MEDIUM |
| 4 | 5 BET / 0 other | 4 HIGH, 1 MEDIUM |
| 5 | 5 BET / 0 other | 1 HIGH, 4 MEDIUM |
| **Aggregate** | **25 BET / 0 other** | **majority HIGH/MEDIUM (no LOW)** |

(Confidence stamp counts approximate — exact per-labeller breakdown in `data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl`.)

## §"Why all 5 labellers routed to BET" — convergent reasoning

The 5 sonnet labellers operated independently and produced near-identical reasoning chains. Sample (PILOT_MW40_VERIF_001 — Js9c5h, hero TdJc):

- **L1 BET (MEDIUM):** "TPWK (top pair Jacks with Ten kicker). Hero is IP (BTN), checked to by all three villains, NOT preflop aggressor — this is a probe/value bet decision by closing-action IP player. DO NOT Rule 11 does not apply since hero is IP."
- **L2 BET (MEDIUM):** "TPWK on dry rainbow (danger_score=0.0). Hero is_ip=1, villain_checked_back=1 (all opponents weakness), DO NOT Rule 11 does not apply because hero is IP."
- **L3 BET (HIGH):** "Top pair Jacks T-kicker on Js9c5h (rainbow, danger_score=0). Hero is_ip=1, not preflop aggressor, all villains checked back, composition quad shows villain_air_pct=0.59."
- **L4 BET (HIGH):** "TPWK on dry rainbow. Hero IP, villain_checked_back=1 weakness signal. Composition quad: villain TP+=0.27, air=0.59. Thin-value-bet routing."
- **L5 BET (MEDIUM):** "Top pair ten kicker IP. Hero NOT preflop aggressor → not a c-bet, value/protection bet decision. DO NOT Rule 11 does not apply since hero is IP."

**The 5 labellers' convergence is robust** — they cite the same protocol elements (DO NOT Rule 11 IP exemption, villain_checked_back=1 weakness signal, composition quad with elevated villain_air_pct, low danger_score on rainbow boards, hero non-PFA closing-action IP routing). This is NOT mode-collapse on a labelling pipeline degenerate state; it's a coherent application of v3.4.

## §"Direct contradiction of plan §3 prediction"

Plan §3 stated:

> `design_action = CHECK` uniform across all 30 variants. Structural reasoning: ... composition quad's TP+/medium_made flip on J-paired villain ranges (set-of-Js elevation) such that thin-value BET on TPMK-T-kicker becomes -EV in 4-way checked-through state.

The pilot evidence directly contradicts this. The labellers do NOT see a composition-quad flip on J-on-board. Instead, they see:
- `villain_top_pair_plus_pct = 0.23-0.41` (NOT elevated to a level that triggers BET-becoming--EV)
- `villain_air_pct = 0.44-0.59` (HIGH — supports BET for value/protection)
- `danger_score = 0` (low — supports BET on dry rainbow)
- `is_ip = 1` (DO NOT Rule 11 explicitly does NOT apply)

The structural prediction was that J-on-board boards would behave like A-high paired-by-implication boards (PILOT_787's MW-40 reference: AJ5r). At pilot scale, the 5 J-on-board boards (4 single-J + 1 paired-J) do NOT exhibit this behaviour. **MW-40's PILOT_787 CHECK consensus appears to be specific to its exact AJ5r reference structure, NOT generalisable to J-on-board parametric variants.**

## §"Stop conditions" (pilot phase — full record)

Per amended dispatch (PR #240) §"Stop conditions":

| Condition | Triggered? | Evidence |
|---|---|---|
| **Pilot consensus is BET-mixed or RAISE-mixed (≥3/5 hands have <3/5 CHECK)** | ⛔ **YES** | All 5/5 hands have 0/5 CHECK = 5/5 BET (worse than threshold) |
| Pilot has unexplained mode collapse (5/5 labellers identical labels with low confidence) | NO | Confidence stamps mix HIGH and MEDIUM; reasoning chains independently structured (not identical text); pattern is robust application of v3.4, not mode collapse |
| Sonnet API errors >5% on the pilot run | NO | 5/5 labellers returned successfully; 0 errors |
| Solver-as-labels appears | NO | All reasoning is bucket-first protocol-cited; no solver/oracle citations |
| Any labels modified after emission | NO | All 5 JSON files written once, untouched |
| Schema-mismatch between corpus input and label output | NO | All 25 labels have valid pilot_hand_id, action, confidence, reasoning fields |

**Stop condition 1 fires.** Pilot consensus is BET-uniform — far worse than the BET-mixed/RAISE-mixed threshold. Per dispatch: "STOP and report to orchestrator (potential graduation-fail signal at scale; orchestrator decides whether to scale anyway for completeness or halt verification)."

## §"What I am NOT doing right now"

- ❌ NOT firing the full 25-hand × 5-labeller run (would cost an additional ~$5-10 LLM and ~25-35 min wall clock)
- ❌ NOT modifying any labels post-emission (immutability rule held)
- ❌ NOT auto-deciding to halt or to scale (orchestrator-scope per `feedback_explicit_action_trigger.md` and `feedback_optional_is_not_authorized.md`)
- ❌ NOT modifying v3.x prompts, BATCH2 reference, river-rats-core/, the merged plan, or the merged -B corpus
- ❌ NOT making any GTO judgments on whether the labellers are "correct" (per `feedback_solver_vs_expert_labels.md` solver verifies/researches only; plus the labellers' protocol application is precisely what we're measuring)

## What unblocks me — orchestrator decides

Per dispatch §"Stop conditions": "orchestrator decides whether to scale anyway for completeness or halt verification."

Two paths:

1. **Scale-anyway** — orchestrator dispatches builder to run the full 25-hand × 5-labeller batch despite pilot signal. Rationale: completeness for graduation-decision evidence at -D; full 30/30 sample reduces statistical noise in the ≥27/30 threshold judgment. Cost: additional ~$5-10 LLM. The full-batch is highly likely (per pilot's robustness) to also produce BET-uniform → MW-40 graduation-fail confirmed at scale.

2. **Halt-verification** — orchestrator declares MW-40 graduation-fail at pilot scale. Rationale: 25/25 BET consensus is sufficient signal; PILOT_787 stays as anomaly; BATCH2 MW-40 BET MEDIUM stands; -D Opus tier-up + -E BATCH2 reference update become memo-only-PR (graduation-fail outcome documented). Saves ~$5-10 LLM. Aligns with `feedback_quality_default_no_ask.md` (the slow-quality default early-stops on a strong signal rather than burning more tokens for the same conclusion).

3. **Hybrid (3rd path; orchestrator may invent)** — e.g., scale to full 30 with Opus directly to test whether the contradiction is Sonnet-specific (PILOT_787's CHECK consensus came partly from Opus tier-up at HIGH; this verification's Sonnets routed to BET; if Opus on these 30 also routes to BET, the structural argument is decisively falsified for the J-on-board family).

**Builder default-if-no-override:** Path 2 (halt-verification). Reasoning per `feedback_quality_default_no_ask.md`: the slow-quality default is to early-stop on a strong signal rather than scale work for the same conclusion. The pilot's 25/25 BET with robust convergent reasoning is a strong signal. Saving ~$5-10 LLM AND ~25-35 min wall clock to land on the graduation-fail conclusion sooner is the slow-quality choice (slow = thoughtful = stop when the answer is clear).

If orchestrator prefers to test the labelling-pipeline-specific question (Sonnet vs Opus), Path 3 is reasonable. If completeness for the formal ≥27/30 graduation threshold is preferred, Path 1.

## §"Files in PR diff"

3 files added:
1. `scripts/run_125i_mw40_verif_labelling.py` (orchestration helper; mirrors prior labelling-round scripts)
2. `data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl` (25 pilot label records; 5 hands × 5 labellers)
3. `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md` (this report)

Plus the pilot working directory files in `review/mass_labelling_mw40v_2026-05-06/pilot/` (briefs, raw labeller JSONs, manifest, corpus subset). Excluded from PR by default (working artefacts) unless QC requests inspection.

## §"What's blocked / what's queued"

**Blocked by this HALT:**
- 12.5I-MW40-VERIFICATION-C full-batch labelling (gates on orchestrator scale-anyway/halt decision)
- 12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision (gates on -C completion)
- 12.5I-MW40-VERIFICATION-E BATCH2 reference update OR memo-only PR (gates on -D verdict)

**Cleared by orchestrator's resolution comm (when authored):**
- One of: full-batch fire-now / halt comm / hybrid-Opus dispatch

## §"References"

- Dispatch (fire trigger): `MAIN_TERMINAL_PR236_RATIFY_AND_MW40C_DISPATCH_2026-05-06.md` (master `3927024`, PR #240)
- -B corpus source: `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (master `a20b495`, PR #236)
- Plan §3 CHECK prediction (now contradicted at pilot scale): `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (master `e0e0304`, PR #228)
- PILOT_787 source (Sonnet 3-2 CHECK + Opus HIGH CHECK + structural argument): `BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md` (master `994ae67`, PR #213)
- Decision 3β source: `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217)
- v3.4 protocol: `prompts/gto_labeller_v3.4.md` (44KB; locked)
- Memory: `feedback_pilot_first_for_long_jobs.md` (pilot-first + sub-rule on training-data tier-up at -D), `feedback_quality_default_no_ask.md` (early-stop on strong signal), `feedback_explicit_action_trigger.md` + `feedback_optional_is_not_authorized.md` (no auto-scaling, no auto-halt — orchestrator decides), `feedback_solver_vs_expert_labels.md` (no solver-as-labels in this report's reasoning)

**Status: 12.5I-MW40-VERIFICATION-C pilot HALT triggered. 25/25 BET (vs plan §3 CHECK prediction). Builder STOPPED before full-batch dispatch. Orchestrator decides next path (scale-anyway / halt-verification / hybrid-Opus). Default recommended: halt-verification (Path 2) per `feedback_quality_default_no_ask.md` early-stop on strong signal.**
