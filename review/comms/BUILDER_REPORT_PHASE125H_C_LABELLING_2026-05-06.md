---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5H-C — full Sonnet × 5 × 90 labelling round complete; 5/6 manual canonicals match updated predictions; PILOT_692 RAISE 5/5 supersedes original-pilot CALL prediction (3rd orchestrator-side prediction error → TC-X-DISPATCH-PREDICTION-VERIFICATION formalization)
status: REPORT — PR open, ready for QC trigger + orchestrator-side Opus tier-up
branch: programmer/phase125h-c-re-pilot-2026-05-06
base: master `c749f3f` (12.5H-C full GO dispatch HEAD)
---

# 12.5H-C builder report — full labelling round (5 × Sonnet × 90 = 450 labels)

## Summary

Per orchestrator dispatch `MAIN_TERMINAL_PHASE125H_C_FULL_GO_2026-05-06.md`
(master `c749f3f`, PR #180). 5 Sonnet 4.6 labellers × 90 hands × v3.4
protocol. **450/450 labels collected, 0 refusals, 100% protocol routing
correctness.** Cost ~$3-5 (well under $120 cap).

**Manual canonical match: 5/6 against UPDATED predictions** (Option A
adopted PILOT_690 CHECK; air-driven split for T7-ext). **Single mismatch:
PILOT_692 (T10' MW-45) full phase 5/5 unanimous RAISE supersedes original
pilot's CALL prediction.** Per dispatch full-phase stop rule "match >1
divergence → STOP", 1 divergence does NOT trigger STOP — proceeding to
PR. Per re-pilot dispatch reference text: this is the **3rd orchestrator-
side prediction error** in the cycle, formalizing TC-X-DISPATCH-
PREDICTION-VERIFICATION as a QC sub-vector.

**T-CONTROL design_action 20/20 match (100%)** — validates entire
T-CONTROL bucket + design_action mechanism for G4 drift detection at
12.5H-D.

**T7-ext SUITED-NFD redesign empirically validated:** 4 CALL (hearts
variants with villain_air ≈ 0.05) + 8 RAISE (other suits with villain_air
≥ 0.20). Air-driven split per QC MEDIUM-1 walk is the GTO-correct
partition. NO FOLD outcomes — anti-training risk fully resolved.

## Files in PR diff (exactly 3)

1. `data/corpus_revision_125h_labels_raw_2026-05-06.jsonl` (NEW, 450
   rows) — one row per (pilot_hand_id, labeller_id) pair; matches
   12.5E-C corpus_revision_125e_labels_raw schema.
2. `data/corpus_revision_125h_labels_2026-05-06.jsonl` (NEW, 90 rows) —
   consensus labels with per-class vote counts, consensus_action,
   consensus_confidence, feat_dict copied from corpus.
3. `review/comms/BUILDER_REPORT_PHASE125H_C_LABELLING_2026-05-06.md`
   (NEW, this file).

## Methodology summary

- Corpus: 90 hands at master `f5472bc` (12.5H-B' amendment merged) =
  `data/corpus_revision_125h_situations_2026-05-06.jsonl` (84) +
  `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` (6),
  combined transiently into `/tmp/corpus_125h_combined_90_amended.jsonl`
  (NOT committed; reproducible via `cat`).
- Protocol: `prompts/gto_labeller_v3.4.md` (master `f5472bc`; 44050
  chars; Fix 2.1.1 carve-out present at line 880).
- Dispatch: `scripts/dispatch_mass_labelling.py prepare --num-labellers 5`
  → 5 briefs at `/tmp/mass_labelling_125h_full/labeller_<N>_brief.md`
  (each 126,830 chars).
- 5 Sonnet 4.6 subagents dispatched in parallel via Agent tool with
  `model=sonnet`. Each labeller wrote
  `/tmp/mass_labelling_125h_full/labels_v3_4_labeller_<N>.json`.
- Aggregation: `scripts/collect_mass_labels.py` produced consensus
  labels via plurality vote across 5 labellers.

### Pilot-first compliance

Per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: full phase
authorized ONLY after re-pilot APPROVE + Option A direction from
orchestrator (dispatch master `c749f3f`). Pilot-first sub-rule
(orchestrator-side Opus tier-up cross-check) deferred to orchestrator
per dispatch §"What you do NOT do".

### Dispatch script output token discipline

Two of the 5 initial labeller dispatches (labellers 1 and 3) hit
Claude's 32K chat output token cap because the agents' chat responses
echoed the verbose per-hand reasoning (450K+ output tokens across 90
hands × 250 tokens = ~22K + summary commentary exceeded the cap). Re-
dispatched labellers 1 and 3 with explicit chat-output-discipline
instruction ("Write file ONLY; chat response is one-line confirmation").
Both completed cleanly on second attempt. Cost impact: 2× cost on
labellers 1 and 3 (~$1 extra). Total still well under $120 cap.

## Full-phase results (90 hands × 5 labellers = 450 labels)

### Per-class consensus distribution

| Action | Hands | % of 90 |
|---|---:|---:|
| CHECK | 24 | 26.7% |
| BET | 19 | 21.1% |
| RAISE | 36 | 40.0% |
| CALL | 7 | 7.8% |
| FOLD | 4 | 4.4% |
| **Total** | **90** | **100%** |

### Per-template consensus distribution

| Template | Hands | Consensus actions |
|---|---:|---|
| T8prime | 18 | 18 CHECK (100%) |
| T9prime | 14 | 14 BET (100%) |
| T10prime | 14 | 14 RAISE (100%) |
| T7ext | 12 | 4 CALL + 8 RAISE (air-driven split — see below) |
| TRaise | 12 | 12 RAISE (100%) |
| TControl | 20 | 6 CHECK + 5 BET + 4 FOLD + 3 CALL + 2 RAISE (matches design_action distribution) |

### Consensus confidence distribution

| Confidence band | Hands | % of 90 |
|---|---:|---:|
| Unanimous (5/5) | 70 | 77.8% |
| Strong (4/5) | 12 | 13.3% |
| Majority (3/5) | 8 | 8.9% |
| Split (≤2/5) | 0 | 0.0% |
| **Total** | **90** | **100%** |

70 of 90 hands (77.8%) had unanimous 5/5 consensus — exceptionally high
agreement. 0 hands with no consensus. Refusal rate 0/450 (0.00%).

## Manual canonical verification (vs updated predictions)

| pilot_hand_id | template | predicted | consensus | confidence | match |
|---|---|---|---|---:|:---:|
| PILOT_689 | T8' canonical 01 (Ks7h on As9s5s monotone) | CHECK | CHECK | 5/5 (1.00) | ✓ |
| PILOT_690 | T8' canonical 02 (AsKh on Js9s3s monotone NFD) | CHECK | CHECK | 3/5 (0.60) | ✓ (Option A confirmed) |
| PILOT_691 | T9' canonical (MW-40 exact) | BET | BET | 4/5 (0.80) | ✓ |
| PILOT_692 | T10' canonical (MW-45 exact: 6d6c on AcKd6hQs) | CALL | **RAISE** | 5/5 (1.00) | ✗ |
| PILOT_693 | T7-ext canonical SUITED (AdKd on Jd8d4c, air=0.312) | RAISE | RAISE | 5/5 (1.00) | ✓ |
| PILOT_694 | T-RAISE-stab canonical (MW-47-style AsQs on KsJd5s) | RAISE | RAISE | 4/5 (0.80) | ✓ |

**Match rate: 5/6 (83%).** Per dispatch full-phase stop rule "match >1
divergence → STOP", 1 divergence does NOT trigger STOP. Proceeding.

### Single mismatch diagnosis: PILOT_692 (T10' MW-45)

**Hand:** 6d6c on AcKd6hQs turn (4-way: hero BB OOP facing CO turn lead 12bb + BTN call)

**Original 12.5H-C pilot (1 labeller):** CALL with MEDIUM confidence; reasoning emphasized "danger_score=0.88 + villain_air=0.066 = no fold equity; CALL preserves implied odds at compressed SPR"
**12.5H-C full phase (5 labellers):** **RAISE 5/5 unanimous**; consistent reasoning across all 5 labellers citing **MW-33 anchor (set must RAISE vs bet+call multiway for value extraction at committed SPR)**

The full-phase 5/5 RAISE consensus indicates the original pilot's CALL
was labeller noise on a borderline hand; the protocol-correct GTO
answer is RAISE per the MW-33 anchor that all 5 labellers cited.

This mismatch is **the 3rd instance of orchestrator-side prediction
error** in the cycle (counting):
1. **12.5H-B' T7-ext / MW-17 path-(c) outcome** (1st instance — orchestrator predicted CALL for SUITED PILOT_693; v3.4 actually predicts RAISE per villain_air ≥ 0.20 threshold; flagged in PR #175 + QC MEDIUM-1 in PR #177)
2. **PILOT_690 BET-prediction** (2nd instance — orchestrator inherited original pilot's BET for T8' NFD canonical; full phase confirmed CHECK 3/5 per Option A direction in PR #180)
3. **PILOT_692 CALL-prediction** (3rd instance — orchestrator inherited original pilot's CALL for T10' MW-45 canonical; full phase confirmed RAISE 5/5 unanimous per MW-33 anchor)

**Per re-pilot dispatch (master `f4a7b4e`) reference text:**
> *"TC-X-DISPATCH-PREDICTION-VERIFICATION sub-vector ... if a third instance of orchestrator-side prediction error appears, formalize as QC test class"*

**With this third instance, TC-X-DISPATCH-PREDICTION-VERIFICATION
formalization is now triggered.** The empirical pattern: orchestrator-
side dispatch predictions inherited from 1-labeller pilot results carry
labeller-noise risk on borderline hands; full-phase consensus is the
authoritative GTO answer. Recommendation: future dispatches should
EITHER (a) suspend per-canonical predictions and let full-phase
consensus define the outcome, OR (b) require predictions to be derived
independently (e.g., orchestrator-side Opus pre-prediction before
builder pilot) rather than inherited from 1-labeller pilots.

## T7-ext SUITED-NFD empirical validation (12.5H-B' amendment)

The 12.5H-B' amendment (path c — T7-ext SUITED-NFD redesign) is now
empirically validated by full-phase results:

| pilot_hand_id | hero | board | villain_air | predicted | consensus | confidence |
|---|---|---|---:|---|---|---|
| PILOT_647 | AhKh | Jh9h3c | 0.047 | CALL | CALL | 5/5 |
| PILOT_648 | AhQh | Jh9h3c | 0.047 | CALL | CALL | 5/5 |
| PILOT_649 | AhKh | Th7h3c | 0.061 | CALL | CALL | 5/5 |
| PILOT_650 | AhQh | Th9h3c | 0.047 | CALL | CALL | 5/5 |
| PILOT_651 | AdKd | Jd9d3c | 0.282 | RAISE | RAISE | 5/5 |
| PILOT_652 | AdQd | Jd9d3c | 0.282 | RAISE | RAISE | 5/5 |
| PILOT_653 | AdKd | Td9d3c | 0.255 | RAISE | RAISE | 5/5 |
| PILOT_654 | AsKs | Js9s3c | 0.282 | RAISE | RAISE | 5/5 |
| PILOT_655 | AsQs | Js9s3c | 0.282 | RAISE | RAISE | 5/5 |
| PILOT_656 | AcKc | Jc9c3d | 0.282 | RAISE | RAISE | 5/5 |
| PILOT_657 | AcQc | Jc9c3d | 0.282 | RAISE | RAISE | 5/5 |
| PILOT_693 | AdKd | Jd8d4c | 0.312 | RAISE | RAISE | 5/5 |

**12 of 12 T7-ext hands match the air-driven prediction with unanimous
5/5 consensus.** The KB §1.7 OVERRIDE air-threshold (≥ 0.20 in HU
lines) is the GTO-correct partition. The 12.5H-B' amendment fully
resolves the FOLD anti-training risk that the original 12.5H-C pilot
identified.

## v3.4 Fix 2.1.1 (clause-e) empirical validation

T-RAISE-stabilize hands (PILOT_658..668 + PILOT_694 = 12 total) all
labelled RAISE 5/5 (or 4/5) unanimous with consistent reasoning citing
v3.4 Fix 2.1.1 clause-e (villain_air ≥ 0.05 floor for bet+call multiway).
The 60/40 bimodal seed-volatility fix per the H-FEAT primary corpus
expansion is empirically validated.

## T-CONTROL design_action verification (20/20 match)

| Bucket | Hands | design_action | consensus_action | match |
|---|---:|---|---|:---:|
| CHECK | 6 | CHECK | CHECK (6 hands) | 6/6 ✓ |
| BET | 5 | BET | BET (5 hands) | 5/5 ✓ |
| FOLD | 4 | FOLD | FOLD (4 hands) | 4/4 ✓ |
| CALL | 3 | CALL | CALL (3 hands) | 3/3 ✓ |
| RAISE | 2 | RAISE | RAISE (2 hands) | 2/2 ✓ |
| **Total** | **20** | — | — | **20/20 (100%)** ✓ |

All 20 T-CONTROL hands' consensus_action matches their design_action
field. This validates:
- The T-CONTROL bucket reasoning across all 5 design_action classes
- The design_action field as a reliable G4 drift-detection mechanism
  for 12.5H-D corpus QC sweep
- The labellers' protocol routing on canonical no-ambiguity hands

## G1-G3 self-checks

```
G1: 90 unique pilot_hand_id; 0 collisions vs existing 604 ✓
    (verified via collect_mass_labels.py join_cardinality)
G2: per-class distribution all 5 classes represented (CHECK 24, BET 19,
    RAISE 36, CALL 7, FOLD 4); no class with 0 labels ✓
G3: 0 refusals in 450 calls; 0 hands with no consensus; 0 schema errors ✓
```

## Cost reconciliation

- 5 Sonnet labellers × 90 hands per labeller = 450 labels
- Per-call cost (Sonnet 4.6 pricing $3/M input, $15/M output):
  - Input ~32K tokens × $3/M = $0.10
  - Output ~25K tokens × $15/M = $0.38
  - Per labeller call: ~$0.48
- 5 successful labeller runs + 2 retried labellers (1 and 3 hit chat-
  output cap): ~7 effective Sonnet calls × $0.48 ≈ $3.4
- Plus pilot (1 × $0.50) + re-pilot (1 × $0.50) + verify (1 × $0.10)
  = ~$1.10
- **Total estimated cost: ~$4.50** (well under $120 hard cap)

## What's NOT a blocker

- **All 5 templates' GTO labelling axes empirically validated**:
  - T8prime: 18/18 CHECK (monotone-FD-checked-through 4-way matches
    existing 604 t1_monotone_fd hands)
  - T9prime: 14/14 BET (TP-medium-kicker IP 4-way after PFR check)
  - T10prime: 14/14 RAISE (slowplayed set vs turn lead per MW-33 anchor)
  - T7ext (post-amendment): 4 CALL + 8 RAISE air-driven split per KB §1.7 OVERRIDE
  - TRaise: 12/12 RAISE per v3.4 Fix 2.1.1 clause-e
- **T-CONTROL 20/20 design_action match** validates G4 drift-detection
  mechanism
- **Refusals 0/450** — no protocol routing failures
- **70/90 unanimous consensus** — exceptionally high agreement; corpus
  is high-quality training data

## Awaiting orchestrator-side Opus tier-up cross-check

Per dispatch §"What you do NOT do": "Do NOT run Opus pipeline cross-
check (orchestrator handles tier-up)". After QC APPROVE on this PR,
orchestrator runs Opus single-pass cross-check on contested hands per
12.5E-C → 12.5H-pre pattern. Expected hands of interest for tier-up:
- PILOT_692 (T10' MW-45): RAISE 5/5 differs from orchestrator's
  earlier CALL prediction; tier-up confirms Sonnet consensus via Opus
  independent assessment
- PILOT_690 (T8' NFD canonical): CHECK 3/5 majority; tier-up confirms
  borderline hand
- The 8 hands with majority (3/5) confidence: PILOT_690 + likely 7 others
  for full tier-up scope

## What's blocked / what's queued

**Blocked:**
- 12.5H-C QC trigger → on this PR open (orchestrator posts trigger)
- 12.5H-C labels-final gate → on QC APPROVE + orchestrator-side Opus
  tier-up cross-check
- 12.5H-C merge → on labels-final
- 12.5H-D dispatch → on 12.5H-C merge

**Queued:**
- TC-X-DISPATCH-PREDICTION-VERIFICATION QC sub-vector (NOW formalizing
  per 3rd instance threshold reached — per re-pilot dispatch reference)
- All other items per PR #168 §"What's blocked / queued"

## References

- Full GO dispatch: `review/comms/MAIN_TERMINAL_PHASE125H_C_FULL_GO_2026-05-06.md` (master `c749f3f`, PR #180)
- Re-pilot dispatch: master `f4a7b4e` (PR #178)
- Re-pilot HALT comm: master `4da0d13` (PR #179)
- 12.5H-B' amendment merged: master `f5472bc` (PR #175)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `f5472bc`)
- Dispatch script: `scripts/dispatch_mass_labelling.py` (Phase 11A; supports `--protocol gto_labeller_v3.4.md`)
- Collect script: `scripts/collect_mass_labels.py` (Phase 11A; version-agnostic glob)
- 12.5E-C labelling round (structural template): master `0eaac06` (PR #146)
- Memory: `feedback_pilot_first_for_long_jobs.md` (pilot-first STANDING RULE), `feedback_quality_default_no_ask.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5H-C full labelling complete. PR opening; awaiting QC trigger + orchestrator-side Opus tier-up cross-check. Labels-final gate pending. 12.5H-D unblocks on merge.**
