---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #232 + PR #234 merged (QC PASS 0/0/0; 23rd solo cycle); dispatch 12.5I-MW40-VERIFICATION-B situation generation (30 J-on-board variants; Hybrid pilot-first 4-check pre-flight on first 5)
status: DIRECTIVE — merges PR #232 + PR #234; fires LEAD-PROGRAMMER on MW-40-VERIFICATION-B (programmer hat) — fire now
---

# PR #232 cleared + 12.5I-MW40-VERIFICATION-B situation-generation dispatch

QC verdict on PR #232 (`REVIEW_QC_PHASE125J_D_PRE_TEST_GUARD_DEFLAKE_2026-05-06.md` on `qc/pr232-jdpre-test-guard-review-2026-05-06`, PR #234): **PASS — 0 BLOCKER, 0 SHOULD_FIX, 0 NIT (23rd solo cycle).** TC-X-DISPATCH-COMPLIANCE 2nd formal exercise = clean PASS, closing the QC → orchestrator → builder feedback loop within 1 PR cycle on the Path 3 Hybrid resolution. Implementation note: builder used `min(cp_gap, sp_gap) < TOLERANCE` (more rigorous than dispatch's literal "top_gap < 0.05" since BLAS noise can flip argmax on either side) — net stricter test, not weaker.

Per loop directive: engineering PR with QC PASS clean → merge after re-checking findings.

## LEAD-PROGRAMMER — Step: 12.5I-MW40-VERIFICATION-B situation generation (fire on this comm merge)

Per `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` § "Sequencing — what fires after MW-40-A merges" + `MAIN_TERMINAL_PR228_RESOLUTION_AND_JDPRE_DISPATCH_2026-05-06.md` § "Hybrid pilot-first" authoritative spec.

Branch: `programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06`. Base: master post-this-comm-merge.

### Scope — emit 30 situations per `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`

Per the merged design plan (master `e0e0304`, PR #228) §5 "Track A — situation factory specification". Programmer-hat task; deterministic factory pass; no labelling.

**Output target:** 30 situations with ref_ids `PILOT_MW40_VERIF_001..030` (zero-padded 3-digit).

### Hybrid pilot-first — 4-check pre-flight on FIRST 5 emitted (binding per PR #228 SHOULD_FIX-1 Path 3 resolution)

**Per `MAIN_TERMINAL_PR228_RESOLUTION_AND_JDPRE_DISPATCH_2026-05-06.md` § "Authoritative specification (binds at 12.5I-MW40-VERIFICATION-B dispatch)":**

Before generating the full 30 variants, the factory MUST emit the first 5 situations as a pre-flight batch and run the following validation pass against them:

1. **Schema parity** — verify `feat_dict` keys match the canonical 61-surface (post-PR #205); 0 NaN; 0 Inf; 0 missing keys. Any failure → STOP and report; no further situations emit.
2. **Step-18 feature plausibility** — verify `nut_blocker_overcard_count` and `bet_call_multiway_oop_raise_pressure_index` compute deterministically. Per plan §5 prediction: both should be ≈ 0 across J-on-board variants (hero is IP not OOP, no nut-FD blocker semantics). Any deviation flags (does NOT halt; explicitly report per `feedback_attention_flags_when_features_change.md`).
3. **ref_id namespace integrity** — verify the 5 ref_ids fall in the new disjoint namespace (`PILOT_MW40_VERIF_001..005`) and do NOT collide with existing 788-corpus ref_ids OR any prior 12.5I ref_ids. Any collision → STOP.
4. **Top-level structural fields** — verify `hero_seat=BTN`, `hero_position=IP non-PFA`, `street_of_decision=FLOP`, `villain_check_through_count=3`, `hand_category=6` (TPMK), `kicker_class=T-kicker (TJ)` match plan §3 constraint table on all 5 emitted hands. Any drift → STOP.

Only on all 4 checks passing does the factory continue with the remaining 25 situations to reach 30. Pre-flight cost: ~$0 (no LLM; pure schema/feature/ref_id validation).

### Sub-axis distribution (per plan §4)

| Sub-axis | Count | Boards |
|---|---|---|
| A — J-high flop, hero TPMK on top of J-high (TJ) | 10 | Js9c5h, Js7d3c, Js8h4d, Js9d2c, Js8c4h, Js7h2d, Js9h3c, Js6d4s, Js9c3d, Js7c5d |
| B — J-low flop with J-on-turn (decision on FLOP; hero TT or T9) | 10 | 9c5d3h, 7c4d2s, 8h6c2d, 9h6c3s, 8c5d2h, 7d4s2c, 9s6h4d, 8d5c3s, 7s5h2d, 9d6s4c (turn = Js for each) |
| C — J-medium flop with paired-J or set-of-Js in range (TJ) | 10 | Jh5c2d, Jc8h3s, Jd9c4h, Jh6s3c, Jc7d2s, Jd8c5h, Jh4c2s, Jc9h6d, Jd7h3c, JcJh4s (last = J-paired boundary case) |

**Blocker variation per `feedback_solver_findings.md` finding 2:** within each sub-axis, **5 of 10** include hero J-blocker; **5 of 10** do not. Total: 15 with-J-blocker / 15 without across the 30 variants. The `blocker_variant` field (`with_J_blocker`/`no_J_blocker`) is in the situation metadata.

### Per-situation factory output structure (per plan §5)

- `ref_id`: `PILOT_MW40_VERIF_NNN` (zero-padded 3-digit)
- `feat_dict`: 61-surface; all 61 keys populated by `feature_extractor.extract_features` (read-only import; no `river-rats-core/` modifications)
- `hero_cards`: top-level field (matches 788-corpus pattern)
- `prior_actions`: hero-only convention (no villain action records beyond preflop opener position + check-through count)
- `design_action`: `CHECK` per plan §3 prediction
- Standard metadata: `template_id = T11_MW40V`, `sub_axis = A`/`B`/`C`, `blocker_variant = with_J_blocker`/`no_J_blocker`

### Stop conditions

- Pre-flight fails ANY of the 4 checks on first 5 emitted → STOP and report (no further situations emit)
- ref_id collision with 788-corpus or prior 125i ref_ids on full 30 → STOP
- ≥1% NaN/Inf across 30 × 61 = 1830 feat_dict values → STOP
- Sub-axis split not exactly 10/10/10 → STOP
- Blocker split not exactly 15/15 → STOP
- Step-18 features show non-zero activation pattern that contradicts plan §5 prediction (hero IP, no nut-FD blocker, J-on-board → both expected ≈ 0) → REPORT (does NOT halt; explicit attention flag)
- design_action ≠ CHECK on any emitted situation → STOP (factory drift from plan)

### What you do NOT do

- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source (read-only import only)
- Do NOT modify BATCH2 reference (orchestrator-scope; locked until -E)
- Do NOT touch existing 788-corpus or any prior-phase corpus files
- Do NOT label hands (12.5I-MW40-VERIFICATION-C scope; separate dispatch)
- Do NOT run any LLM inference (12.5I-MW40-VERIFICATION-B is deterministic factory; LLM is at -C)
- Do NOT skip the 4-check pre-flight (Path 3 Hybrid is binding per PR #228 SHOULD_FIX-1 resolution; skipping = TC-X-DISPATCH-COMPLIANCE violation)
- Do NOT auto-fix NIT-1 or NIT-2 from PR #228 audit (orchestrator records carry-forward to next design-comm touch — see § "NIT carry-forward" below)

### Cost / time

~$0 (factory script; no LLM calls). ~15-20 min builder time including pre-flight + report.

### Deliverable scope

Expected 3 files in PR diff (4 with optional script):
1. `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (30 situations; 61-surface feat_dict)
2. `scripts/generate_125i_mw40_verif_situations.py` (factory script — mirrors prior `generate_*.py` precedent if such exists; otherwise a minimal new script)
3. `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md` — the report:
   - §"Pre-flight 4-check on first 5" — exact result per check (PASS/FAIL/REPORT for each)
   - §"Sub-axis distribution" — 10/10/10 confirmed
   - §"Blocker distribution" — 15/15 confirmed
   - §"Step-18 activation prediction" — observed activation rates vs predicted (≈0)
   - §"Schema integrity" — 30/30 rows × 61 keys; 0 NaN/Inf
   - §"ref_id namespace" — `PILOT_MW40_VERIF_001..030`; 0 collisions with 788-corpus or prior 125i
   - §"Stop conditions" — full record (which triggered, which didn't)
   - §"Files in PR diff"
   - §"What's blocked / what's queued"
   - §"References"

### Builder report sections (mandatory; per 12.5I-D corpus assemble + 12.5I-B situation gen format)

- Headline table (steps + results)
- Stop conditions (full record)
- What I did NOT do (per dispatch)
- What's blocked / what's queued
- References

## NIT carry-forward (recorded for future design-comm touches)

Per PR #231 § "NIT-1 + NIT-2 fix-forward":

- **NIT-1 (terminology drift):** v3.4 prompt uses "composition quad" (`villain_top_pair_plus_pct`, `villain_medium_made_pct`, `villain_draw_pct`, `villain_air_pct`); memory note `feedback_preflop_geometry_vs_postflop_composition.md` uses "composition triple" (TP+/draws/air). For this dispatch, "composition quad" is the canonical reference (the v3.4 prompt is the protocol surface that produces labels at -C). Memory edit is owner-scope; surfacing for owner read but no action requested. Builder MUST NOT auto-fix the memory note.
- **NIT-2 (5th stop condition placement):** the <27/30 graduation threshold lives in plan §10 R4 (orchestrator-decision item) rather than §8 STOP list. Carry-forward: if/when 12.5I-MW40-VERIFICATION-E ships a graduation-pass / graduation-fail PR, that dispatch's stop conditions block must explicitly include the threshold floor as a STOP-or-redesign criterion. NOT in scope for -B.

Builder DOES NOT modify the merged plan in -B PR per `feedback_explicit_action_trigger.md`. NITs are advisory carry-forward; orchestrator binds them at the next design-comm touch.

## QC stream — what you audit (when 12.5I-MW40-VERIFICATION-B PR opens)

Standalone audit, ~10-15 min, 7-item scope:

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly the 3 files above (+ optional script). No drift outside `data/` + `scripts/` + `review/comms/`. Verify NOT touched: v3.x prompts, BATCH2 reference, `river-rats-core/` source, training-data, existing 788-corpus.
2. **Pre-flight 4-check correctness** — verify builder ran the 4 pre-flight checks on first 5 emitted situations BEFORE emitting the remaining 25 (Hybrid pilot-first compliance per PR #228 SHOULD_FIX-1 Path 3 resolution). Builder report must explicitly show pre-flight result per check.
3. **Row count integrity** — 30 / 30 emitted; ref_id namespace `PILOT_MW40_VERIF_001..030` exact; 0 collisions with existing 788-corpus or prior 12.5I ref_ids.
4. **Sub-axis + blocker distribution** — 10/10/10 sub-axis split exact; 15/15 blocker split exact across the 30.
5. **Schema integrity** — 61-surface uniform across all 30; 0 NaN/Inf in 30 × 61 = 1830 values.
6. **Step-18 activation pattern** — verify both Step-18 features ≈ 0 across all 30 variants (hero IP + no nut-FD blocker semantics on J-on-board); flag any non-zero pattern as informational (not a finding).
7. **TC-X-DISPATCH-COMPLIANCE (3rd formal exercise)** — cross-check builder's implementation against this dispatch's authoritative spec. Specifically: did builder run all 4 pre-flight checks? Did builder emit only the planned sub-axis/blocker distribution? Did builder leave PR #228's NIT-1/NIT-2 alone (no auto-fix)? Any unilateral deviation → SHOULD_FIX.

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md` on `qc/pr<N>-mw40-verification-b-review-2026-05-06`.

## Why no Opus tier-up on 12.5I-MW40-VERIFICATION-B

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs (Sonnet judgments on poker hands). 12.5I-MW40-VERIFICATION-B is deterministic factory generation — no new poker judgments produced; situations are emitted from a parametric specification. Standard QC PASS suffices. Opus tier-up runs at 12.5I-MW40-VERIFICATION-D on canonical hands selected from the -C labelling round.

## Sequencing — what fires after 12.5I-MW40-VERIFICATION-B merges

Per plan §7 sequencing table:

1. **12.5I-MW40-VERIFICATION-C labelling round** (5 Sonnet × 30 hands; pilot-first 5-hand gate per `feedback_pilot_first_for_long_jobs.md`; ~$5-10 LLM cost) — fires on -B merge.
2. **12.5J-C trainer integration test on 61-surface** — fires on -B merge (parallel queue with -C in builder serial; orchestrator decides interleave order based on -C QC duration).
3. **12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision** — fires on -C QC PASS.
4. **12.5I-MW40-VERIFICATION-E** — BATCH2 reference update PR (graduation-pass) OR memo-only PR (graduation-fail) — fires on -D verdict; NIT-2 binds (5th stop condition explicit in -E dispatch).

## What's blocked / what's queued

**Cleared by this comm:**
- PR #232 merge (12.5J-D-pre test-guard deflake)
- PR #234 merge (QC verdict record)
- 12.5I-MW40-VERIFICATION-B dispatch fires
- Hybrid pilot-first clause activated in -B scope

**Newly queued (after -B merges):**
- 12.5I-MW40-VERIFICATION-C labelling round (pilot-first 5-hand × 5-Sonnet gate)
- 12.5J-C trainer integration test on 61-surface (parallel queue)

**Still queued (later):**
- 12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision
- 12.5I-MW40-VERIFICATION-E BATCH2 reference update OR memo-only PR (NIT-2 binds)
- 12.5K combined re-train (gates on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship)
- 12.5L gate eval (gates on 12.5K)

**Owner-scope items pending (informational, non-blocking):**
- TC-X-DISPATCH-COMPLIANCE curative addition to `learning/test_class_registry.md` (now 2 successful exercises: PR #228 surfaced SHOULD_FIX-1, PR #232 closed it cleanly; ratify-or-decline at owner convenience)

## References

- PR #232 (12.5J-D-pre Option b): branch `programmer/phase125j-d-pre-test-guard-deflake-2026-05-06`
- PR #234 (QC PASS 0/0/0 verdict): branch `qc/pr232-jdpre-test-guard-review-2026-05-06`
- PR #233 (QC trigger): master `18570ed`
- PR #231 (orchestrator: PR #228 + #230 merge + Path 3 Hybrid + J-D-pre dispatch): master `e44ed59`
- PR #228 (Builder MW-40-VERIFICATION-A design merged): master `e0e0304`
- PR #226 (orchestrator: PR #222 merge + MW-40-A dispatch): master `f52a93d`
- 12.5I-A design plan (authoritative for -B scope): `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestration_efficiency_rules.md`, `feedback_pilot_first_for_long_jobs.md` (sub-rule on -B exemption + Hybrid clause), `feedback_attention_flags_when_features_change.md` (Step-18 activation reporting), `feedback_solver_findings.md` finding 2 (blocker-effect sensitivity)

**Status: PR #232 + PR #234 cleared for merge. LEAD-PROGRAMMER fires 12.5I-MW40-VERIFICATION-B situation generation (programmer hat) on this comm merge. ~15-20 min wall clock to PR open.**
