# MAIN_TERMINAL — Phase 2-F Prep: Positional Action-Chain Diversity + Re-Label Consistency Audit + 5-Way Pilot Stub

**DATE:** 2026-05-13
**AUTHOR:** Orchestrator
**STATUS:** STANDBY — do NOT fire while Phase 2-E batch-008 is in flight
**FIRE TRIGGER:** This directive will be re-issued as `MAIN_TERMINAL_*_FIRE_NOW` after Phase 2-E batch-008 ships AND merges to master AND QC verdict logs PASS

---

## Background

Independent orchestrator diversity audit (2026-05-13) identified that the 4-way corpus pipeline enumerates ~10 explicit action patterns and 8 stratification dimensions, but **does not enumerate sequential villain action chains** — i.e., "EP bets → MP calls → CO raises → action returns to hero." That dimension is left to organic sampling. Cited evidence:

- `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md:347-359` — 8-D stratification uses binary "action context" (opener / facing_initial_bet / facing_raise), not n-ary villain-chain fingerprint
- `review/comms/BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5_2026-04-27.md:221, 422` — most templates fix villain = BB, leaving multi-villain history to organic sampling
- `data/4way_labeller_brief.md:63-70` — AMENDMENT 1 (players-left-to-act) and AMENDMENT 2 (closing/early-action) require notation in rationale but **do not require explicit chain enumeration**

Combinatorial scale: 4-way ≈ ~100 villain-chain patterns (10 enumerated, 90 organic). 5-way ≈ ~240+ patterns (0 enumerated). Organic sampling fails at 5-way.

This dispatch covers three workstreams that run **in series** after Phase 2-E ships:
1. **Architect**: design 9th stratification dimension + brief amendment + positional-chain scenario module
2. **Builder**: 20-hand pilot re-label of existing 4-way pots using new prompt v3.5 (consistency audit) → if pilot passes, full 80-hand stratified re-label sample
3. **QC**: audit gates after each architect deliverable, pilot, and full re-label sample

5-way pilot stub appears at the end (post-audit, owner-gated).

---

## Architect (Builder, architect hat)

**Task A1 — Design `positional_action_chain` stratification dimension**

Deliverable: `review/comms/BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-XX.md`

Required content:
- Define the chain fingerprint: `(first_aggressor_pos, caller_positions_in_order, raiser_pos, hero_pos)` — canonical hash
- Enumerate the chain fingerprints expected for 4-way pots at flop, turn, river (count them; report cardinality per street)
- Propose the integration point into the existing 8-D stratification (`BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3:347-359`) — does it replace "action context" or extend it to 9-D?
- Propose mandatory quota allocation: how many hands per chain bucket per batch (recommend 20-30 reserved per 50-hand batch)
- Specify the corresponding generator module: `corpus_revision_scenarios/positional_action_chain_scenarios.py` — what scenarios it generates, what action sequences it enforces, what hero hand strengths it samples
- **Explicit recommendation** (not menu): per `feedback_orchestrator_decides_not_recommends.md`, architect commits to a single design. No "open questions" left for owner.

**Task A2 — Draft Labeller Brief v3.5 amendment**

Deliverable: `review/comms/AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5_2026-05-XX.md`

Required content:
- Mandatory requirement: every rationale MUST explicitly list villain positions in action order and identify which villain's action hero is responding to
- Example mandatory phrasing: "Hero faces CO's raise after BTN called EP's bet" — not "OOP-middle"
- Specify the **bucket-first compliance** flow (per `feedback_bucket_first_labelling.md`): chain fingerprint is part of bucket assignment, NOT part of equity-threshold reasoning
- Add an FL6 failure class: rationale that does not enumerate the villain action chain explicitly is rejected at consensus

**Task A3 — Spec the re-label consistency audit**

Deliverable: `review/comms/SPEC_RELABEL_CONSISTENCY_AUDIT_v1_2026-05-XX.md`

Required content:
- Sample stratification: 80 hands drawn from batches 001-007 (excluding batch-008 which is fresh-labelled under old prompt), balanced across: 7 batches (~11/batch); hero position (BTN/CO/MP/UTG/SB/BB); action context (opener/facing-bet/facing-raise); street (flop/turn/river); board texture
- **Pilot subset**: 20 of those 80 hands designated for v3.5-prompt pilot re-label FIRST (per `feedback_pilot_first_for_long_jobs.md`)
- Re-labelling protocol: same 5-labeller infrastructure as production; same Sonnet tier; consensus computed identically
- **Drift metric**: % hands where new-consensus action ≠ old-consensus action (per-action drift matrix: was-RAISE-now-CALL, was-CHECK-now-BET, etc.)
- **Tier-up gate** (per `feedback_pilot_first_for_long_jobs.md` sub-rule): on every drift hand, run Opus tier-up cross-check; if Opus agrees with new label → real shift; if Opus agrees with old → noise
- **Accept/reject thresholds**:
  - Pilot (20 hands) drift ≤ 1 (≤5%) → PROCEED to 80-hand full sample
  - Pilot drift 2-3 (10-15%) → owner gate: scope question (is amendment changing what we think GTO is, or just adding rigor?)
  - Pilot drift ≥ 4 (≥20%) → STOP; amendment is materially shifting labels; re-label of all 350 hands required before Phase 2-F begins

---

## Builder (Builder, lead-programmer hat)

**Builder does NOT fire until architect deliverables A1, A2, A3 have all received QC PASS verdicts.**

**Task B1 — Implement `positional_action_chain_scenarios.py`** (post-A1 QC PASS)

- Build the generator per architect's A1 blueprint
- Test yield on a 20-hand micro-batch; verify chain-fingerprint distribution matches blueprint quota
- Submit PR; orchestrator gates QC trigger

**Task B2 — Execute 20-hand pilot re-label** (post-A2/A3 QC PASS)

- Construct the 20-hand pilot subset per A3 stratification
- Re-label using prompt v3.5 (post-A2 amendment), same 5-labeller infrastructure
- Compute consensus; compute drift vs original consensus
- Run Opus tier-up on every drift hand
- Submit PR with: pilot-input.jsonl, 5 raw-label files, consensus.jsonl, Opus-tierup.jsonl, DRIFT_REPORT_PILOT.md
- **STOP at pilot result** — do NOT fire 80-hand full sample without orchestrator gate

**Task B3 — Execute 80-hand full re-label sample** (post-B2 QC PASS + orchestrator gate)

- Only fires if pilot drift ≤ 1 (≤5%)
- Same protocol scaled to 80 hands
- Submit PR with full deliverables + DRIFT_REPORT_FULL.md

---

## QC

**QC audits each deliverable independently. FLAG-only. Per `feedback_qc_required_before_approval.md`: QC PASS required before each subsequent task fires.**

**Gates:**

1. **QC-G1 (post-A1):** Audit architect blueprint for positional_action_chain dimension
   - TC-23 EXISTENCE check: blueprint commits to single design (no menus)
   - Chain-fingerprint cardinality math is correct
   - Generator module spec is concrete (file path, function signatures, scenario types enumerated)
   - Quota allocation justified, not handwaved

2. **QC-G2 (post-A2):** Audit labeller brief v3.5 amendment
   - Mandatory phrasing requirement is unambiguous
   - FL6 failure class definition is operational (consensus rejection rule is testable)
   - Bucket-first compliance preserved (no equity thresholds smuggled in)

3. **QC-G3 (post-A3):** Audit re-label consistency audit spec
   - Stratification balance is correct (no missing batches, positions, action contexts)
   - Drift metric definition is unambiguous
   - Tier-up gate matches `feedback_pilot_first_for_long_jobs.md` sub-rule
   - Accept/reject thresholds match `feedback_quality_default_no_ask.md` (no fast-path option)

4. **QC-G4 (post-B1):** Audit `positional_action_chain_scenarios.py` PR
   - Standard TC-23 CONTENT + EXISTENCE drift audit
   - 20-hand micro-batch yield matches blueprint quota

5. **QC-G5 (post-B2):** Audit 20-hand pilot re-label PR
   - 5-labeller raw labels follow new brief v3.5 (FL6 enforced)
   - Consensus computation is bit-equal to production formula (per `feedback_bit_equality_requires_rng_seed_preservation.md`)
   - Opus tier-up was run on every drift hand
   - Drift report cites per-hand evidence

6. **QC-G6 (post-B3):** Audit 80-hand full re-label PR
   - Same checklist as G5 at scale
   - Drift matrix is complete (all 4×4 = 16 transition cells reported, including zeros)

---

## Owner gates (explicit decision points)

- **Gate 1:** After QC-G1/G2/G3 PASS → owner approves architect deliverables before builder fires
- **Gate 2:** After QC-G5 (pilot result) → owner reads DRIFT_REPORT_PILOT and decides:
  - drift ≤ 1: GREENLIGHT 80-hand full sample
  - drift 2-3: SCOPE QUESTION discussion before proceeding
  - drift ≥ 4: STOP and re-plan (likely full 350-hand re-label required)
- **Gate 3:** After QC-G6 (full sample) → owner decides whether to:
  - Ship Phase 2-F with new prompt + existing labels (if drift acceptable)
  - Re-label all 350 hands (if drift material)
  - Roll back the amendment (if drift suggests amendment is wrong)

---

## 5-Way Pilot Stub (owner-gated; do not fire without explicit go)

Per `feedback_pilot_first_for_long_jobs.md`: 5-way work MUST start with a pilot before any full-scale labelling. Pilot spec:

- **Sample:** 50 deliberately-constructed 5-way hands using the 9th-dim chain generator (post-Phase-2-F architecture)
- **Goal:** Confirm labellers can reason coherently about 4-villain action chains; measure rationale-quality drift vs 4-way baseline
- **Decision:** if pilot rationales are coherent → proceed to full 5-way corpus design; if rationales degrade → architect must redesign multi-villain reasoning protocol BEFORE any 5-way production labelling

Owner triggers this pilot AFTER Phase 2-F ships and the v9-4way retrain validates.

---

## Out of scope

- Modifying Phase 2-E batch-008 (let it complete on the current spec)
- Re-labelling all 350 hands (only fires if drift gate forces it)
- Building 5-way production corpus (pilot only, post-Phase-2-F)
- Any threshold/equity logic in the new brief (per `feedback_bucket_first_labelling.md`)
- Solver as labelling oracle (per `feedback_solver_vs_expert_labels.md` — solver verifies, never labels)

---

## File checklist (deliverables by party)

| Party | File | Status |
|---|---|---|
| Architect | `review/comms/BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-XX.md` | pending |
| Architect | `review/comms/AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5_2026-05-XX.md` | pending |
| Architect | `review/comms/SPEC_RELABEL_CONSISTENCY_AUDIT_v1_2026-05-XX.md` | pending |
| Builder | PR: `positional_action_chain_scenarios.py` + 20-hand micro-batch | pending |
| Builder | PR: 20-hand pilot re-label + DRIFT_REPORT_PILOT.md | pending |
| Builder | PR: 80-hand full sample + DRIFT_REPORT_FULL.md (conditional) | pending |
| QC | 6 audit findings: `findings/2026-05-XX-pr###-phase2f-prep-*.md` | pending |
