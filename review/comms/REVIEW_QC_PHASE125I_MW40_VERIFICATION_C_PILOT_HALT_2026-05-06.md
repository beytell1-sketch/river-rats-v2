---
date: 2026-05-06
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #241 — Phase 12.5I-MW40-VERIFICATION-C pilot HALT (25/25 BET unanimous; CHECK refuted) — pre-merge audit (HALT format)
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR241_2026-05-06.md (master `aea6488`, PR #242)
pr_branch: programmer/phase125i-mw40-verification-c-labelling-2026-05-06 (head `4e3b34c`)
qc_branch: qc/pr241-mw40-verification-c-pilot-review-2026-05-06
---

# PR #241 — pre-merge QC verdict: PASS (0/0/0)

25th solo cycle. **HALT-format audit** — verifying empirical-signal integrity for graduation-decision use, not normal labelling-round audit. **Reasoning is convergent (NOT mode-collapsed)**; empirical signal is robust.

The pilot's 25/25 BET unanimous result is a **strong empirical refutation** of plan §3's CHECK prediction at the labelling-pipeline layer. Builder HALTed correctly per dispatch §"Stop conditions" first item. Pilot-first 5-hand gate fired exactly as `feedback_pilot_first_for_long_jobs.md` intends: caught the prediction-falsification at pilot scale before scaling to full 30 hands × 5 Sonnet (~$5-8 saved + ~30 min wall-clock saved).

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. Pilot label integrity (25 well-formed) | ✅ PASS |
| 3. **Reasoning convergence (NOT mode collapse)** [critical item] | ✅ **CONVERGENT** |
| 4. No solver-as-labels | ✅ PASS |
| 5. Per-hand consensus math (5 hands × 5 labellers = 25) | ✅ PASS |
| 6. TC-X-OWNER-SCOPE-DISCIPLINE | ✅ PASS |
| 7. TC-X-DISPATCH-COMPLIANCE (4th formal exercise; HALT triggered correctly) | ✅ PASS |
| 8. TC-X-INTRA-PLAN-CONSISTENCY (informal continuation; new contradictions?) | ✅ PASS (none) |

**Verdict: PASS — clear to merge. Empirical signal is robust; orchestrator's path decision (halt-verification / scale-anyway / hybrid-Opus) is well-founded on this pilot data.** No QC-side blocker.

## §1 — Diff scope strict

`git diff --stat master...origin/programmer/phase125i-mw40-verification-c-labelling-2026-05-06` (three-dot):

```
 data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl |  25 +++
 review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md | 153 +++++++++++++++
 scripts/run_125i_mw40_verif_labelling.py | 215 +++++++++++++++++++++
 3 files changed, 393 insertions(+)
```

Exactly 3 files: 25 raw labels jsonl + factory script + builder report. **No working-dir artifacts in PR diff** (per trigger's "optional"; builder kept those local). 0 deletions, 0 modifications.

Verified NOT touched (perimeter sweep):
- `prompts/` (v3.x prompts including `gto_labeller_v3.4.md`) — 0 changes
- `design/multiway_reference_set/BATCH2_*` — 0 changes
- `river-rats-core/` — 0 changes
- `data/corpus_combined_*` (788 corpus) — 0 changes
- `data/corpus_revision_125i_mw40_verif_situations_*` (the 30 from PR #236) — 0 changes
- `training-data/`, model files, plan/comm files, memory files — 0 changes

Owner-scope perimeter held. **PASS.**

## §2 — Pilot label integrity

Independent QC inspection of the 25 raw labels:

| Field | Per-row spec | QC measurement |
|---|---|---|
| `pilot_hand_id` | non-empty | 25/25 present (5 hands: PILOT_MW40_VERIF_001 / 011 / 016 / 025 / 026) |
| `labeller_id` | 1-5 per hand | 25/25 present; complete coverage (each hand sees labellers 1, 2, 3, 4, 5) |
| `action` | enum {CHECK, BET, RAISE, CALL, FOLD} | 25/25 = BET |
| `confidence` | enum {LOW, MEDIUM, HIGH} | 15 HIGH + 10 MEDIUM (no LOW) |
| `reasoning` | non-empty, non-boilerplate | 25/25 present; lengths 704–1352 chars (mean 911); 0 empty |
| `model` | sonnet variant | per-row present |
| `protocol_version` | v3.4 | per-row present |

**Note on confidence:** trigger §2 referenced "All 25 confidences = 1.00 (builder claim) or as reported." The "1.00" in builder PR title refers to *consensus_confidence* (`N_majority/N_labellers = 5/5 = 1.00` per hand). Per-labeller `confidence` is the discrete enum (HIGH/MEDIUM here). Both interpretations are consistent: 5/5 unanimous BET per hand → consensus_confidence 1.00; per-labeller individual ratings split 60% HIGH / 40% MEDIUM. **PASS.**

## §3 — Reasoning convergence (CRITICAL ITEM): CONVERGENT, NOT MODE-COLLAPSED

QC sampled 5 reasoning blocks (1 per `labeller_id` 1-5, distributed across 5 different hands) for character analysis:

### Common rule-chain across all 5 sampled labellers

All 5 reasoning blocks reach BET via the same protocol-rule chain:

1. **Bucket-first hand identification** (per `feedback_bucket_first_labelling.md`): each labeller correctly classifies the hand (TPWK / monster trips on the JcJh4s boundary case)
2. **DO NOT Rule 11 OOP-only carve-out**: cited verbatim by all 5 ("DO NOT Rule 11 does not apply here because hero is IP" / "is_ip=1, which is an explicit carve-out" / "the rule governs OOP multi-way checked-to spots only")
3. **Composition quad data analysis**: each labeller cites specific per-hand values for `villain_top_pair_plus_pct`, `villain_air_pct`, `worse_hand_pct`, `better_hand_pct`
4. **Board texture + danger_score**: each cites `danger_score=0.0`, rainbow texture, low connectivity
5. **Action conclusion**: BET for thin value + protection given villain weakness

### Inter-labeller phrasing variation (anti-mode-collapse signal)

Each labeller phrases the same conclusion differently:

| Labeller | Hand class phrasing |
|---|---|
| 1 | "medium-made hand (TPWK: TdJc gives top pair with Ten kicker on Js9c5h)" |
| 2 | "medium made hand (TPWK: Jack with Ten kicker on Js8d3h)" |
| 3 | "medium-made hand: TsJc gives hero top pair (Jacks) with a Ten kicker on Jh5c2d" |
| 4 | "monster hand (trips Jacks: hero holds ThJd on board JcJh4s, giving three Jacks with a ten kicker; hand_category=11, is_monster=1)" |
| 5 | "medium made hand (top pair ten kicker, Jd on Jh7s3d) held in position (is_ip=1)" |

This is **convergent reasoning, not mode collapse**: same rule-chain, same conclusion, different phrasing per labeller, hand-specific composition values cited correctly. Strong empirical signal.

### Per-hand-specific composition values are real (not boilerplate)

Each labeller cites distinct values per hand. Sample evidence:

- PILOT_001 (`Js9c5h`): `villain_top_pair_plus_pct=0.274`, `villain_air_pct=0.443`
- PILOT_011 (`Js8d3h`): `villain_top_pair_plus_pct=0.232`, `villain_air_pct=0.485`, `worse_hand_pct=0.792`
- PILOT_016 (`Jh5c2d`): `villain_air_pct=0.570`, `villain_top_pair_plus_pct=0.232`, `worse_hand_pct=0.797`
- PILOT_025 (`JcJh4s`): `raw_equity=0.8345`, `worse_hand_pct=0.9320`, `villain_top_pair_plus_pct=0.4093`
- PILOT_026 (`Jh7s3d`): `villain_air_pct=0.5063`, `better_hand_pct=0.1815`

Distinct values per hand confirm labellers are reading per-hand `feat_dict` data (not pasting boilerplate). **PASS.**

### Why the structural prediction was empirically falsified

Plan §3 predicted CHECK based on the structural argument: "J-on-board flips composition quad → set-of-Js + JJ slowplay + suited-J broadways elevate `villain_top_pair_plus_pct` → BET no longer +EV on TPMK-T-kicker." The actual pipeline rule-walk:

- **Step 1: DO NOT Rule 11 evaluation.** Rule 11 governs OOP multi-way checked-to spots; it has an explicit IP carve-out. Hero is IP (BTN closing 4-way SRP) → Rule 11 inapplicable → no CHECK directive triggered at this layer.
- **Step 2: composition quad analysis.** The empirical composition quad on the 5 pilot J-on-board boards shows `villain_top_pair_plus_pct ≈ 0.23-0.27` (NOT elevated as plan §3 hypothesized) and `villain_air_pct ≈ 0.44-0.57` (substantial weakness). The set-of-Js / JJ slowplay component does not dominate enough to flip the composition; villain check-through range is air-heavy.
- **Step 3: action conclusion.** With composition weak and IP carve-out clearing the OOP-CHECK path, the protocol concludes BET for thin value + protection.

The structural argument was supported by PILOT_787 single-hand evidence (Sonnet 3-2 CHECK + Opus HIGH CHECK at PR #213). The verification round's empirical answer at pilot scale (5 hands × 5 labellers) refutes the generalisation. PILOT_787 may have been a structural outlier or a sampling-noise CHECK majority on a close-split spot. The verification round's job was exactly this: distinguish "PILOT_787 generalises" from "PILOT_787 is an outlier." Pilot stage answers definitively at this scale: it's the latter.

(QC's role is to verify the answer is well-founded — convergent reasoning, no mode collapse, no solver-as-labels — not to make GTO judgments on whether 25/25 BET is "correct." Per trigger §"What you do NOT do".)

## §4 — No solver-as-labels

QC scanned all 25 reasoning blocks for solver / GTO-solver / PIO / PIOSolver / Hold'em Resources / equity-solver citations as authority for action. **0 citations as label-source.** 

Authorities cited per block (per QC sample inspection):
- v3.4 protocol surface: "DO NOT Rule N", "composition quad", "danger_score", "bucket-first" hand classification
- `feat_dict` features: `villain_*_pct`, `is_ip`, `villain_checked_back`, `worse_hand_pct`, `raw_equity`, `hand_category`, `is_monster`
- Board characterisation: rainbow / paired / connectivity / SPR

Per `feedback_solver_vs_expert_labels.md`: solver may be cited descriptively but not as label-source. None of the 25 reasoning blocks does either. **PASS.**

## §5 — Per-hand consensus math

| Hand | Labellers (1-5) | Action distribution | Consensus action | Consensus confidence |
|---|---|---|---|---|
| PILOT_MW40_VERIF_001 | 1, 2, 3, 4, 5 (5/5) | BET ×5 | BET | 1.00 |
| PILOT_MW40_VERIF_011 | 1, 2, 3, 4, 5 (5/5) | BET ×5 | BET | 1.00 |
| PILOT_MW40_VERIF_016 | 1, 2, 3, 4, 5 (5/5) | BET ×5 | BET | 1.00 |
| PILOT_MW40_VERIF_025 | 1, 2, 3, 4, 5 (5/5) | BET ×5 | BET | 1.00 |
| PILOT_MW40_VERIF_026 | 1, 2, 3, 4, 5 (5/5) | BET ×5 | BET | 1.00 |
| **Total** | **25 labels** | **25 BET, 0 CHECK, 0 RAISE, 0 CALL, 0 FOLD** | **5/5 hands BET 1.00** | — |

Builder claim verified: 25/25 BET unanimous; 5 hands × 5 labellers each; no missing labellers; no missing hands.

**Note:** PILOT_MW40_VERIF_025 is the JcJh4s paired-J boundary case (hero TJ on paired-J flop = trips, not TPMK with T-kicker). Hand class differs from the other 4 pilot hands (TPMK-T-kicker on J-high non-paired boards). PILOT_025's BET is justified by the trips hand-class on its own merits (high `raw_equity=0.8345`, `worse_hand_pct=0.9320`); the structural argument in plan §3 was about TPMK-T-kicker, not trips. Removing the trips boundary case still leaves 4 hands × 5 labellers = 20/20 BET on TPMK-T-kicker proper — the structural-argument-test cohort is still 100% BET. Empirical refutation holds with margin.

**PASS.**

## §6 — Owner-scope discipline

(Verified in §1 above; restating for completeness.)

- 0 v3.x prompt edits
- 0 BATCH2 reference edits
- 0 `river-rats-core/` source edits
- 0 existing corpus / training-data edits
- 0 plan-comm edits (the merged PR #228 plan + PR #237 resolution + PR #240 dispatch all unchanged)
- 0 memory file edits

**PASS.**

## §7 — TC-X-DISPATCH-COMPLIANCE (4th formal exercise)

Cross-check builder's HALT-trigger against amended dispatch (`MAIN_TERMINAL_PR236_RATIFY_AND_MW40C_DISPATCH_2026-05-06.md`) §"Stop conditions" first item:

> "Pilot consensus is BET-mixed or RAISE-mixed (≥3/5 hands have <3/5 CHECK) → STOP and report to orchestrator."

Builder result: **5/5 hands have 0/5 CHECK** (all 5 hands unanimously BET; 0 CHECK across all 25 labels). This is **strictly stronger than "BET-mixed"** — the most extreme BET signal possible at pilot scale. Stop-condition margin: 5 of 5 hands trigger the threshold (≥3/5 hands required); each hand has 5/5 BET (vs the <3/5 CHECK threshold).

Builder correctly:
- HALTed before scaling to full 30 hands × 5 Sonnet
- Did NOT auto-fix or attempt to "explain away" the contradicted prediction
- Routed to orchestrator via PR title + builder report (no AskUser; standalone HALT comm)
- Did NOT modify v3.x prompt (which would be the only "fix-forward" path that could change the rule chain; orchestrator-scope per memory)

**PASS.** Builder's HALT-and-route discipline is exactly what the dispatch's Stop conditions intended. TC-X-DISPATCH-COMPLIANCE class continues to validate as durable on its 4th formal exercise.

## §8 — TC-X-INTRA-PLAN-CONSISTENCY (informal continuation)

Looking for new dispatch-internal contradictions surfaced by the pilot data:

| Check | Observation |
|---|---|
| Did any pilot hand violate plan §3 constraint table? | No — all 5 pilot hands match BTN / IP / 4-way / FLOP / villain_check_through=3 / 200bb / hero TJ / kicker T |
| Did any feat_dict surface contradict the corpus's documented Step-18 ≈ 0 expected pattern? | No — Step-18 features confirmed 0/30 in PR #236 audit (§5 there); pilot uses subset of 30 with same expected pattern |
| Did the 25/25 BET refutation expose a previously-hidden plan §3 prediction-vs-protocol-surface gap? | YES (informational) — plan §3's structural composition-quad argument did not anticipate that DO NOT Rule 11's IP carve-out short-circuits the entire OOP-CHECK path. The plan reasoned about composition quad VALUES but not about which RULES route to which actions. This is a genuine plan-internal-coverage gap. **Not a finding** — the audit-trigger §"What you do NOT do" prohibits GTO judgments; this observation is for orchestrator/owner forward learning, not a current-PR action item. |

No new contradictions found that QC should surface as findings. **PASS.**

## §"Stop conditions" — pilot-stage triggers

Per dispatch §"Stop conditions":
- ✅ TRIGGERED #1: "Pilot consensus is BET-mixed or RAISE-mixed (≥3/5 hands have <3/5 CHECK)" → 5/5 hands with 0/5 CHECK (extreme case; HALT-and-report fired)
- ❌ Not triggered: "Pilot reasoning incoherent or rule-cite missing" — reasoning is convergent and rule-cited per §3 above
- ❌ Not triggered: "Solver-as-labels" — none per §4
- ❌ Not triggered: schema / namespace / per-hand-math integrity — all PASS per §2 + §5
- ❌ Not triggered: any owner-scope perimeter violation — 0 per §6

Stop-condition #1 was the correct trigger; builder routed correctly to orchestrator.

## Test classes exercised

- TC-23 spec/infrastructure drift (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (6th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (4th formal exercise; HALT-trigger discipline; clean PASS)** — class continues to validate as durable
- TC-X-INTRA-PLAN-CONSISTENCY (informal continuation; no new contradictions)
- TC-X-DISPATCH-PREDICTION-VERIFICATION (entry #11; **2nd formal exercise** — dispatch's CHECK prediction empirically falsified at pilot scale; exactly the class's purpose; the class continues to be a durable diagnostic)
- **NEW informal sub-class exercised: TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE** — for high-stakes labelling pilots, sample reasoning blocks for inter-labeller phrasing variation + common rule-chain. Convergent (variant phrasing, common chain, hand-specific values) vs mode-collapsed (identical-token sequences, no hand-specific cited values). This audit's reasoning-block sampling is the first formal exercise of the sub-class. Logging to `~/river-rats-qc/learning/curative_additions_log.md` as informal entry #14 pending owner ratification.

## Smarter-over-time observations

Three classes activated together on this audit:

1. **TC-X-DISPATCH-PREDICTION-VERIFICATION (entry #11):** dispatch CHECK prediction → 5 hands × 5 labellers = 25/25 BET. The class's 2nd formal exercise validates: dispatch predictions matter empirically and the class catches falsifications when they happen.
2. **TC-X-DISPATCH-COMPLIANCE (entry #12, informal):** builder HALT-and-route discipline matches dispatch §"Stop conditions" exactly. 4th formal exercise confirms the class is durable.
3. **TC-X-INTRA-PLAN-CONSISTENCY (entry #13, informal):** no new contradictions surfaced, but the audit notes a plan-internal-coverage gap (plan §3 didn't anticipate DO NOT Rule 11 IP carve-out short-circuit). Informal observation; not a current-PR finding.

A new informal sub-class (TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE) was exercised for the first time in this audit. Will log to curative additions on next QC commit.

The QC → orchestrator → builder feedback loop continues to close cleanly: orchestrator's audit trigger §3 explicitly identified "reasoning convergence" as the critical audit item, QC delivered convergent-not-mode-collapsed verdict, decision-relevant signal surfaced for path selection.

## Audit cost / time

- Wall clock: ~14 min (data audit + reasoning-block sampling + dispatch cross-check + verdict authoring). Within HALT-format estimate (~10-15 min, +5 min over normal -C audit).
- LLM cost: $0 (mechanical Python + git operations; no inference).

## Gates

PR #241 cleared from QC side. Per dispatch §"What gates on this audit":

- 12.5I-MW40-VERIFICATION-D Opus tier-up dispatch — gates on PR #241 merge AND orchestrator path decision (Path 1 scale-anyway / Path 2 halt-verification / Path 3 hybrid-Opus)
- QC tentatively favors **Path 3 (Hybrid Opus on 5 pilot hands)** for 2nd-source confirmation per `feedback_pilot_first_for_long_jobs.md` sub-rule (training-data outputs require Sonnet → Opus tier-up; verification-decision outputs warrant the same multi-source confirmation pattern that MW-25 graduated through). But QC has no veto; orchestrator decides.
- 12.5I-MW40-VERIFICATION-E memo-only PR (graduation-fail framing) — gates on -D Opus confirmation of BET (or escalation if Opus splits)

No QC-side blocker on either downstream dispatch.

## References

- 12.5I-MW40-VERIFICATION-C dispatch (the binding spec): `MAIN_TERMINAL_PR236_RATIFY_AND_MW40C_DISPATCH_2026-05-06.md` (master `3927024`, PR #240)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR241_2026-05-06.md` (master `aea6488`, PR #242)
- PR #228 plan (CHECK prediction source): master `e0e0304`
- PILOT_787 source (Sonnet 3-2 + Opus HIGH evidence; Decision 3β motivator): `BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md` (master `994ae67`, PR #213)
- v3.4 prompt protocol (DO NOT Rule 11 OOP-only carve-out; the rule chain that overrode the structural argument): `prompts/gto_labeller_v3.4.md`
- Curative log: `~/river-rats-qc/learning/curative_additions_log.md` entries #11 (TC-X-DISPATCH-PREDICTION-VERIFICATION; 2nd exercise here), #12 (TC-X-DISPATCH-COMPLIANCE; 4th exercise here), #13 (TC-X-INTRA-PLAN-CONSISTENCY; informal continuation here), #14 (TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE; will be logged on next QC commit)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `project_river_rats_qc.md` (owner-curated coverage)

**Status: VERDICT = PASS. PR #241 cleared for merge from QC side. Empirical signal robust (convergent reasoning, no mode collapse). Decision 3β graduation-fail signal at pilot stage. 25th solo QC cycle. New informal class TC-X-REASONING-CONVERGENCE-VS-MODE-COLLAPSE exercised first time; logging to curative additions on next QC commit.**
