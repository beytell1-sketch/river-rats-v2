# MAIN_TERMINAL — Phase 2-F FIRE NOW: Positional Diversity + Re-Label Audit + v3.4 Prompt Fixes

**DATE:** 2026-05-XX (orchestrator: replace with dispatch date)
**AUTHOR:** Orchestrator
**STATUS:** FIRE NOW
**SUPERSEDES:** review/comms/MAIN_TERMINAL_PHASE2F_PREP_POSITIONAL_DIVERSITY_2026-05-13.md (STANDBY) — same scope, expanded A2.

---

## Pre-flight verification (orchestrator MUST confirm before this directive fires)

- [ ] Phase 2-E batch-008 shipped: PR #_____ merged at SHA _________
- [ ] QC verdict logged: findings/2026-05-XX-pr____-phase2e-full-batch008.md = PASS
- [ ] Builder branch builder-phase2-e-full-batch8-2026-05-12 archived or deleted
- [ ] No open PRs blocking architect work
- [ ] PR #457 (this directive's STANDBY predecessor) merged or marked superseded

If any box is unchecked, orchestrator does NOT fire this directive. Re-verify and re-issue.

---

## Trigger

**MAIN_TERMINAL — Builder (architect hat): fire now A1 + A2 + A3.**

Author Tasks A1, A2, A3 per spec below. Submit as 3 separate PRs. Each PR triggers an independent QC audit before the next architect deliverable proceeds.

---

## Background

Three independent audits performed 2026-05-13:

1. **Orchestrator positional-diversity audit** identified that the corpus generator and labeller brief do not enumerate sequential villain action chains. The 8-D stratification uses binary action_context, not n-ary chain fingerprint. 4-way pots have ~100 chain patterns, ~10 are explicitly enumerated; 5-way breaks (~240 patterns, 0 enumerated).

2. **Explore agent latent-issues audit of `prompts/gto_labeller_v3.4.md`** identified 11 issues, of which 3 are BLOCKERS:
   - BLOCKER: KB §1.7 carve-out has 3-layer override patches (v3.2 + v3.3 + v3.4 Fix 2.1.1) creating unmaintainable conditional logic at lines 792-909
   - BLOCKER: Solver-as-reasoning references at lines 12, 811, 816, 846 (violates `feedback_solver_vs_expert_labels.md` — solver verifies, never labels)
   - SHOULD_FIX (promoted to BLOCKER for v3.5): DO NOT Rule 11 threshold logic at lines 708-726 (violates `feedback_bucket_first_labelling.md` — no equity thresholds in prompt)

3. **Corpus stratification audit** (pilot-sample construction, agent-built; see `review/comms/DRAFT_PILOT_SAMPLE_20HAND_SELECTION_NOTES_2026-05-13.md`) revealed CRITICAL structural gaps in the existing 4-way corpus (batches 001-007):
   - **Facing-raise stratum is EMPTY**: 0 of 350 hands have a bet+raise sequence. The exact "EP bets → MP calls → CO raises → action returns to hero" pattern that motivated this directive is structurally absent from training data.
   - **River stratum is EMPTY**: 0 of 350 hands are river decisions. All 350 are flop or turn.
   - Position skew: BTN/UTG/EP each appear only once in a balanced 20-sample; CO is over-represented.

A2 scope is **expanded** to incorporate audits 1 + 2.
A1 scope is **expanded** to incorporate audit 3 (facing-raise + river enumerated quotas).

---

## Architect (Builder, architect hat)

**Task A1 — Design `positional_action_chain` stratification dimension**

Deliverable: `review/comms/BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-XX.md`

Pre-drafted by orchestrator: `review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md`. Architect reviews, ratifies, or supersedes.

Required content (EXPANDED from STANDBY directive — audit 3 findings):
- Canonical chain fingerprint: `(first_aggressor_pos, ordered_caller_positions, raiser_pos, hero_pos)`
- Enumerated chain cardinality per street with actual math (not "~100")
- Integration design: replace binary action_context with 9-D chain-fingerprint dim
- **EXPANDED:** mandatory enumerated quotas for chain types ABSENT from current corpus:
  - **Facing-raise quota:** minimum 10 hands per 50-hand batch with explicit bet+raise sequence before hero acts (NOT 0 as in batches 001-007)
  - **River decision quota:** minimum 5 hands per 50-hand batch with river hero-decision (NOT 0 as in batches 001-007)
  - **Position balance quota:** each of BTN/CO/MP/UTG/SB/BB appears in at least 5 hands per batch (NOT skewed as in current corpus where CO is 30%, BTN/UTG/EP each <5%)
- Generator module spec: `corpus_revision_scenarios/positional_action_chain_scenarios.py`
- Function signatures + minimum 12 enumerated chain types, of which at least 4 must include bet+raise sequences and at least 4 must include river decisions

**Task A2 — Labeller Brief v3.5 + Prompt v3.5 (EXPANDED SCOPE)**

Two deliverables (one for the brief, one for the prompt):

Deliverable A2a: `review/comms/AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5_2026-05-XX.md`

Pre-drafted: `review/comms/DRAFT_AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5_2026-05-13.md`

- New mandatory section: villain action-chain enumeration (FL6 failure class)
- 3 worked examples covering distinct chain types
- Preserves bucket-first compliance (no equity thresholds)

Deliverable A2b: `prompts/gto_labeller_v3.5.md` (full rewrite of v3.4) + `review/comms/DELIVER_PROMPT_V3_5_2026-05-XX.md` (justification + diff summary)

Required changes vs v3.4 (BLOCKERS from audit):
1. **Consolidate KB §1.7 carve-out**: replace 3-layer override (v3.2 + v3.3 + v3.4 Fix 2.1.1) with single decision rule. Rewrite: "KB §1.7 SEMI-BLUFF RAISE (nut FD + blocker): Apply when (1) hero has nut flush draw + ace blocker, (2) villain has sufficient fold equity (villain_air_pct ≥ 0.05 in HU bet; ≥ 0.05 in bet+call multiway with call_count ≥ 1), AND (3) hero has ≥35% equity vs continuing range. In pure chip-check spots (villain_air < 0.05), prefer CALL to realize equity."
2. **Decouple solver verification from labeller reasoning**: remove solver-EV-calculation references from teaching guidance at lines 12, 811, 816, 846. Move solver outputs to Calibration Notes ONLY as post-hoc anchors. Reframe `villain_air_pct ≥ 0.20` thresholds as poker principles ("fold equity only materializes if villain has fold-candidate hands; below 0.20 air, fold equity is marginal") rather than solver-derived EV.
3. **Remove DO NOT Rule 11 threshold logic** at lines 708-726. Replace deterministic predicate ("ONLY BET if BOTH (a) AND (b)") with qualitative guidance ("Prefer CHECK on paired/2-tone OOP multiway. Override to BET only when villain's range is value-heavy AND hero has genuine strength to extract, OR river-checked-to override applies").
4. **Add hand-strength composition triple instruction** (lines 234-249 area): explicit teaching that postflop strength comes from TP+/draws/air composition, NOT from preflop range labels.
5. **Add bucket-first enforcement** in output schema (line 586): "reasoning field MUST start with bucket classification: 'This is a [bucket] hand.'"

Architect must commit to a single design per memory `feedback_orchestrator_decides_not_recommends.md`. No menus.

**Task A3 — Re-label Consistency Audit Spec**

Deliverable: `review/comms/SPEC_RELABEL_CONSISTENCY_AUDIT_v1_2026-05-XX.md`

Pre-drafted: `review/comms/DRAFT_SPEC_RELABEL_CONSISTENCY_AUDIT_v1_2026-05-13.md`

Pre-built pilot sample: `review/comms/DRAFT_PILOT_SAMPLE_20HAND_2026-05-13.jsonl` + index + selection notes.

- 80-hand stratified sample (20-hand pilot subset pre-built)
- Drift metrics: action_drift_rate, per-action drift matrix, sizing_drift
- Tier-up gate: Opus cross-check on every drift hand
- Thresholds: ≤1 drift → proceed; 2-3 → owner scope question; ≥4 → STOP, full 350 re-label

---

## Builder (Builder, lead-programmer hat)

**Builder does NOT fire until QC G1, G2 (×2), G3 PASS for A1, A2a, A2b, A3.**

**Task B1 — Implement `positional_action_chain_scenarios.py`** (post-A1 QC PASS)
**Task B2 — Execute 20-hand pilot re-label with prompt v3.5** (post-A2/A3 QC PASS)

Critical: pilot uses v3.5 prompt (the FULL rewrite with all BLOCKER fixes), not just the brief amendment. Drift measurement includes ALL fixes, not just chain-amendment.

**Task B3 — Execute 80-hand full re-label sample** (conditional on pilot drift ≤ 1)

---

## QC

**Gates (FLAG-only):**

1. **QC-G1 (post-A1):** TC-23 EXISTENCE + CONTENT on positional chain blueprint
2. **QC-G2a (post-A2a):** TC-23 on brief amendment
3. **QC-G2b (post-A2b):** TC-23 on prompt v3.5 — must verify all 5 BLOCKER fixes implemented + diff vs v3.4 documented
4. **QC-G3 (post-A3):** Audit re-label consistency spec + stratification correctness
5. **QC-G4 (post-B1):** Audit scenario module PR + 20-hand yield
6. **QC-G5 (post-B2):** Audit pilot drift report + Opus tier-up coverage
7. **QC-G6 (post-B3):** Audit full sample drift report (4×4 matrix complete)

Per `feedback_qc_required_before_approval.md`: QC PASS required before each subsequent task fires.

---

## Owner gates

- **Gate 1:** Post-QC-G1/G2a/G2b/G3 PASS → owner approves architect deliverables (4 deliverables total: blueprint, brief, prompt v3.5, audit spec)
- **Gate 2:** Post-QC-G5 (pilot) → owner reads DRIFT_REPORT_PILOT and decides:
  - drift ≤ 1: GREENLIGHT 80-hand full
  - drift 2-3: scope question
  - drift ≥ 4: STOP; full 350 re-label likely
- **Gate 3:** Post-QC-G6 (full sample) → owner decides: ship Phase 2-F with v3.5 + existing labels; re-label all 350; or roll back v3.5

---

## 5-Way Pilot Stub (owner-gated; do not fire without explicit go)

Per `feedback_pilot_first_for_long_jobs.md`: 5-way work MUST start with a pilot.

- 50 deliberately-constructed 5-way hands using post-A1 9th-dim chain generator
- Validates labellers can reason about 4-villain action chains coherently
- Triggers AFTER Phase 2-F ships and v9-4way retrain validates

---

## Files referenced (orchestrator restart checklist)

| File | Status |
|---|---|
| review/comms/MAIN_TERMINAL_PHASE2F_PREP_POSITIONAL_DIVERSITY_2026-05-13.md | STANDBY directive (predecessor) |
| review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md | architect input (pre-drafted) |
| review/comms/DRAFT_AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5_2026-05-13.md | architect input (pre-drafted) |
| review/comms/DRAFT_SPEC_RELABEL_CONSISTENCY_AUDIT_v1_2026-05-13.md | architect input (pre-drafted) |
| review/comms/DRAFT_PILOT_SAMPLE_20HAND_2026-05-13.jsonl | builder input (pre-drafted) |
| prompts/gto_labeller_v3.4.md | source for v3.5 rewrite |
| data/4way_labeller_brief.md | source for amendment |

---

## Out of scope

- Modifying any of batches 001-007 (only re-labelling 80 selected hands per A3)
- Re-labelling all 350 hands (only if drift gate forces it)
- 5-way production corpus
- Building Phase 3 chain ahead of Phase 2-F retrain validation
- Solver as labelling oracle (per `feedback_solver_vs_expert_labels.md`)
