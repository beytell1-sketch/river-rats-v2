---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: Phase 12.5I-MW40-VERIFICATION-E memo-only PR — graduation-fail documentation; 4-source convergence symmetric to MW-25 graduation; stay-wrong list 4 → 4 (unchanged); NIT-1 / NIT-2 / NIT-3 carry-forward fold-in complete
status: complete; PR opens for QC audit
branch: programmer/phase125i-mw40-verification-e-memo-2026-05-06
base: master `92e2d85` (post-PR #248 dispatch merge)
---

# Phase 12.5I-MW40-VERIFICATION-E — graduation-fail memo

## §"Verification round summary" — A → B → C → D → E

| Phase | Scope | PR / Outcome |
|---|---|---|
| **A — Design** | Single template T11'-MW40V; 30 J-on-board parametric variants; design_action=CHECK uniform per structural prediction | PR #228 (master `e0e0304`); QC PR #230 PASS+1SHOULD_FIX (pilot-first divergence; resolved Path 3 Hybrid in PR #231) |
| (orch) | Path γ' resolution: drop sub-axis B (plan §4 contradiction); 15/0/15 split; hero TJ uniform | PR #237 (master `42460ae`) |
| **B — Situations** | 30 J-on-board variants emitted; Hybrid pilot-first 4-check on first 5 PASS; 0 NaN/Inf; ref_id namespace disjoint; Step-18 0/30 (matches plan §5 prediction) | PR #236 (master `a20b495`); QC PR #239 PASS+1SHOULD_FIX (sub-axis C "J-middle-card" terminology drift; ratified Path 1 in PR #240) |
| **C — Sonnet pilot** | 5 hands × 5 sonnet labellers; **25/25 BET at 1.00 confidence per hand**; pilot gate triggered (BET-uniform contradicts CHECK prediction); HALT before full 25-hand × 5-labeller run; ~$5-10 LLM saved | PR #241 (master `d411cb8`); QC PR #243 PASS 0/0/0 (reasoning CONVERGENT, signal robust) |
| **D — Opus tier-up** | Path 3 Hybrid: 1 Opus 4.7 call × same 5 pilot hand-ids × same v3.4 protocol; **5/5 BET; full Sonnet-Opus consensus**; multi-source aggregate 30/30 BET | PR #245 (master `877555a`); QC PR #247 PASS 0/0/0 (CONVERGENT + INDEPENDENT corroboration) |
| **E — This memo PR** | Documentation only; stay-wrong annotation; memory entry; BATCH2 footnote; NIT carry-forward fold-in | This PR (≤30 min builder; ~$0 LLM) |

**Final outcome: graduation-fail confirmed.** MW-40 stays in BATCH2 reference at BET MEDIUM. Stay-wrong list count: 4 → 4 (UNCHANGED). MW-17, MW-40, MW-45, MW-47 remain.

## §"4-source convergence table" (mirror MW-25 graduation pattern, opposite direction)

| Source | Result | Reference |
|---|---|---|
| 1. v3.4 production-prompt Sonnet pilot (5 hands × 5 labellers) | **25/25 BET** at 1.00 confidence; CONVERGENT reasoning across 5 independent labellers | PR #241 (master `d411cb8`) |
| 2. Opus 4.7 tier-up on the same 5 pilot hands (1 call × 5 hands) | **5/5 BET**; CONVERGENT + INDEPENDENT reasoning (same v3.4 routing chain reached via independent v3.4 paths) | PR #245 (master `877555a`) |
| 3. v3.4 protocol-rule chain (DO NOT Rule 11 OOP-only exemption + villain_checked_back=1 weakness signal + composition quad villain_air_pct=0.44-0.59 + danger_score=0 on rainbow → value/protection BET routing) | Production-prompt deterministic routing | `prompts/gto_labeller_v3.4.md` |
| 4. PR #209 Opus 4.7 HIGH on PILOT_787 (the original CHECK signal) | Anomalous to broader pattern at parametric scale (single-hand; AhTs / AJ5r exact reference) | master `077c168` |

The 4-source convergence is unambiguous in the BET direction at the labelling-pipeline layer. PILOT_787's CHECK was a **single-hand anomaly** that did NOT generalize to the broader J-on-board TPMK T-kicker 4-way checked-through IP non-PFA pattern. The structural argument ("J-on-board flips composition triple toward CHECK") is empirically TOO NARROW under the v3.4 production-prompt protocol routing.

This pattern is **structurally symmetric to MW-25's graduation evidence in PR #218**, but in the OPPOSITE direction:
- MW-25 graduation: 5/5 pilot CHECK + Opus HIGH CHECK + 30/30 unanimous parametric CHECK + v3.4 traces → BATCH2 reference UPDATED to CHECK HIGH
- MW-40 verification-fail: 25/25 Sonnet BET + 5/5 Opus 4.7 BET + v3.4 production-prompt traces routing to BET + PILOT_787 CHECK as outlier → BATCH2 reference STAYS at BET MEDIUM

## §"Files edited" (3 files in PR diff + 1 memory file)

```
 design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md (footnote on MW-40 commentary; +6 lines)
 review/RESTART_PROMPT_V9_3WAY.md                          (MW-40 stay-wrong row annotation; +1 line modified)
 review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md (this report)
```

Plus, edited via direct-write outside v2-repo per dispatch §"Deliverable scope" + PR #218 precedent:
```
 ~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md (Verified Negative Result section + MW-40 entry)
```

### Diff summary

- **`review/RESTART_PROMPT_V9_3WAY.md`** — MW-40 stay-wrong list row annotation. The "graduation candidate" wording REPLACED with "BATCH2 BET MEDIUM stands. Verification round complete..." annotation citing PRs #228/#236/#241/#245. No other rows touched. List header still "4 True Remaining Failures."
- **`design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`** — single new "Verification round footnote" paragraph appended to the MW-40 section reasoning. The canonical label table row at line 42 (`| MW-40 | spr_interactio | 0.206 | 0.000 | BET | MEDIUM |`) UNCHANGED. The textual GTO Action / Reasoning UNCHANGED. Only the new footnote added.
- **`reference_corrections.md`** (memory file) — new "Verified Negative Reference Verifications (6 May 2026)" section between the existing "Empirically Corrected Reference Labels (6 May 2026)" section (which has the MW-25 entry) and the "Unverified But Likely Corrections" section. MW-25 entry, solver-corrected section, and unverified section all UNCHANGED.

## §"NIT-1 / NIT-2 / NIT-3 carry-forward fold-in"

Per dispatch §"NIT carry-forward fold-in":

### NIT-1 (terminology drift "composition quad" vs memory "composition triple")

The v3.4 prompt surface uses **"composition quad"** (4 features: `villain_top_pair_plus_pct`, `villain_medium_made_pct`, `villain_draw_pct`, `villain_air_pct`). The memory note `feedback_preflop_geometry_vs_postflop_composition.md` uses "composition triple" (3 components, collapsing medium_made into TP+ or air). Throughout this -E memo and the appended `reference_corrections.md` entry, **"composition quad"** is used as the canonical project terminology (matches the v3.4 prompt surface, which is the protocol the labellers actually apply).

**Surface for owner read (memory edit is owner-scope):** the memory note `feedback_preflop_geometry_vs_postflop_composition.md` should be refreshed to reflect the 4-component model. NOT done in this PR per `feedback_explicit_action_trigger.md` (memory note refresh is not in dispatch scope).

### NIT-2 (5th stop condition placement: <27/30 graduation threshold)

The plan §10 R4 placed the threshold (≥27/30 CHECK consensus → MW-40 graduates; <27/30 → graduation-fail) as an "open question for orchestrator" rather than a §8 STOP condition. In this -E memo, the threshold is **elevated to the top-level outcome reference** (cited in §"Decision 3β outcome — graduation-fail confirmed" of the orchestrator's PR #248 + this memo's §"4-source convergence table" + the `reference_corrections.md` entry's "Decision 3β graduation threshold: ≥27/30 CHECK consensus; observed 0/30 effective" line). NIT-2 carry-forward is now satisfied: the threshold has its first formal application as the outcome criterion, not a hidden risk.

### NIT-3 (plan-internal-consistency cross-check)

PR #236 surfaced sub-axis B's blocker-variation contradiction (hero TT/T9 ⇒ no J ⇒ within-sub-axis 5/5 J-blocker rule unsatisfiable). PR #240 ratified PR #237's "J as middle card" terminology drift via Path 1. Both were caught at the verification execution stage rather than at plan-merge time.

**Process-improvement candidate (surface for owner ratification):** future verification-round design comms should run a contradiction-cross-check between (a) hand-class spec, (b) intra-sub-axis distribution rules, and (c) literal vs informal terminology BEFORE merge. This is the motivating evidence for both `TC-X-INTRA-PLAN-CONSISTENCY` (informal class; curative entry #13; QC stream) and `TC-X-DISPATCH-COMPLIANCE` (informal class; 5 successful exercises now: PR #228 + PR #232 + PR #236 + PR #241 + PR #245). Owner ratifies-or-declines class formalization at convenience; NOT in scope for this PR.

## §"Lessons learned"

1. **Structural arguments must cross-check against v3.4 DO NOT rules before submission to verification rounds.** The plan §3 structural prediction ("J-on-board flips composition triple toward CHECK on TPMK T-kicker 4-way checked-through") did not account for v3.4's DO NOT Rule 11 IP-exemption: the rule's OOP paired/2-tone exception is explicitly inactive when hero is IP. With Rule 11 OFF, the routing reduces to standard composition-quad-driven value/protection BET on rainbow checked-through 4-way TPMK — exactly what both Sonnet and Opus 4.7 produced.

2. **Single-hand pilot anomalies don't generalize without parametric verification.** PILOT_787 (Sonnet 3-2 CHECK + Opus HIGH CHECK on AhTs / AJ5r) was a meaningful 3-source signal at the time. Decision 3β's verification round was the correct response — it tested whether the structural argument generalizes. The answer is empirical "no" at the labelling-pipeline layer. PILOT_787's CHECK signal is real BUT specific to its exact reference structure (AhTs / AJ5r) or to small-N sampling artefacts at 5 labellers.

3. **Pilot-first gate saved ~$5-10 + ~30 min.** Per `feedback_pilot_first_for_long_jobs.md`, the 5-hand × 5-labeller pilot gate triggered correctly when consensus contradicted the structural prediction. The remaining 25 hands × 5 labellers were not run; the empirical signal was already conclusive at pilot scale. Subsequent Path 3 Hybrid Opus tier-up on the same 5 hands (~$1-2 + ~10 min) provided the cross-model corroboration. Total verification round cost ~$2-4 LLM (vs the ~$15-25 budget had Path 1 scale-anyway been chosen).

4. **The 4-source pattern works symmetrically.** MW-25 graduated via 4-source positive convergence (CHECK, in PR #209/#213/#215/#218). MW-40 verification-fails via 4-source negative convergence (BET, in PR #209/#213/#241/#245). The same evidence framework is robust in both directions; this gives high confidence in BOTH MW-25's graduation AND MW-40's stays-as-is outcome.

## §"Stay-wrong list state"

```
4 True Remaining Failures (post-2026-05-06; UNCHANGED by this verification round)
| MW-17 | Under-calling (low equity draw)
| MW-40 | Residual passive (very thin value bet); BATCH2 BET MEDIUM stands. Verification round complete 2026-05-06: graduation-fail confirmed. (annotation added by this PR)
| MW-45 | Under-raising
| MW-47 | Shared blind spot (nut draw should raise)
```

Count: 4 → 4. No graduation occurred. Per dispatch §"Stop conditions": "Stay-wrong list count modified (should remain 4) → STOP" — count UNMODIFIED; STOP not triggered.

## §"Stop conditions" (full record)

| Condition | Triggered? | Evidence |
|---|---|---|
| Stay-wrong list count modified (should remain 4) | NO | RESTART_PROMPT_V9_3WAY.md still has "4 True Remaining Failures"; only MW-40 row annotation modified |
| BATCH2 reference label changed (MW-40 BET MEDIUM stands) | NO | `BATCH2_8_HAND_DESIGNS.md` UNCHANGED (not even opened); `BATCH2_8_RANGE_ANALYSIS.md` MW-40 label table row at line 42 UNCHANGED; only the post-Reasoning footnote added |
| New labels added to corpus | NO | No corpus jsonl files modified |
| v3.x prompts touched | NO | `prompts/gto_labeller_v3.4.md` UNCHANGED |
| `river-rats-core/` touched | NO | No files in `river-rats-core/` modified |

All stop conditions clear.

## §"What I did NOT do" (per dispatch)

- ❌ Did NOT label any hands (verification round complete; no new labelling)
- ❌ Did NOT modify the -B corpus or -C/-D label files (immutable empirical record)
- ❌ Did NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md` UNCHANGED)
- ❌ Did NOT modify `river-rats-core/` source
- ❌ Did NOT modify BATCH2 reference labels (MW-40 BET MEDIUM stands; only optional footnote added per dispatch builder-discretion clause)
- ❌ Did NOT update the stay-wrong list COUNT (still 4 — no graduation)
- ❌ Did NOT promote informal classes to formal classes (owner-scope; surfaced for read)
- ❌ Did NOT modify the merged plan (`PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` UNCHANGED at master `e0e0304`)
- ❌ Did NOT refresh the memory note `feedback_preflop_geometry_vs_postflop_composition.md` for NIT-1 (owner-scope)

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5J-C trainer integration test on 61-surface dispatch (engineering work; non-blocking on MW-40 verification round outcome)
- 12.5K combined re-train design (gates on -E + 12.5J-E ship)

**Awaiting orchestrator dispatch:**
- 12.5J-C trainer integration test (next builder fire-now after this PR merges)

**Still queued (later):**
- 12.5J-D / 12.5J-E (post-12.5J-C)
- 12.5K combined re-train + 12.5L gate eval
- Owner ratification of TC-X-INTRA-PLAN-CONSISTENCY + TC-X-DISPATCH-COMPLIANCE class formalization (informational; non-blocking)
- Owner-scope memory note refresh for "composition quad" terminology (NIT-1 surfaced)

## §"References"

- PR #209 (Opus 4.7 MW-25 tier-up; precedent for -D pattern AND original PILOT_787 Opus HIGH source): master `077c168`
- PR #213 (PILOT_787 Sonnet 3-2 CHECK source; the candidate signal Decision 3β tested): master `994ae67`
- PR #217 (Decision 3β source; ≥27/30 graduation threshold): master `d6912ad`
- PR #218 (MW-25 graduation BATCH2 update; precedent for the 4-source positive pattern): master `e01b296`
- PR #228 (Plan; J-on-board structural prediction): master `e0e0304`
- PR #236 (Builder situation gen 30 J-on-board variants; Path γ' amended): master `a20b495`
- PR #237 (Orchestrator Path γ' resolution): master `42460ae`
- PR #239 (QC verdict on -B; first informal TC-X-INTRA-PLAN-CONSISTENCY activation): master `861d947`
- PR #240 (Orchestrator -C dispatch + SHOULD_FIX-1 Path 1 ratification): master `3927024`
- PR #241 (Builder -C pilot HALT; 25/25 BET): master `d411cb8`
- PR #243 (QC verdict on -C pilot HALT; reasoning CONVERGENT): master `f5aebe2`
- PR #244 (Orchestrator -D Path 3 Hybrid Opus dispatch): master `966fcbd`
- PR #245 (Builder -D Opus tier-up; 5/5 BET): master `877555a`
- PR #247 (QC verdict on -D Opus tier-up; CONVERGENT + INDEPENDENT): master `8edc771`
- PR #248 (Orchestrator -E dispatch; this comm's source): master `92e2d85`
- v3.4 prompt protocol: `prompts/gto_labeller_v3.4.md` (DO NOT Rule 11 OOP-only exemption; the dominant routing rule)
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestration_efficiency_rules.md`, `reference_corrections.md` (this PR appends to it)

**Status: 12.5I-MW40-VERIFICATION-E memo-only PR complete. Verification round (A→B→C→D→E) closed. MW-40 graduation-fail documented; 4-source pattern symmetric to MW-25 graduation; BATCH2 BET MEDIUM stands; stay-wrong list 4 → 4 (unchanged). NIT-1 / NIT-2 / NIT-3 carry-forward fold-in complete. PR opens for QC audit per dispatch §"QC stream — what you audit". Builder ready for 12.5J-C trainer integration test dispatch on this PR's merge.**
