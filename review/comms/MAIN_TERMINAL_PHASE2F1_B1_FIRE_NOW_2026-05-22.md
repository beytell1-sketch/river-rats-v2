---
date: 2026-05-22
from: Orchestrator (Main Terminal) — DRAFT prepared by Architect; fires when RATIFICATION_A1 PR merges
to: Builder (lead-programmer + architect + gto-expert hats)
re: Phase 2-F1 B1 — implement `positional_action_chain_scenarios.py` + 20-hand micro-batch yield test
status: FIRE NOW (2026-05-22) — orchestrator fires this directive concurrent with RATIFICATION_A1 merge on master
authorization: this directive is the named-author trigger per `feedback_explicit_action_trigger.md`
references:
  - review/comms/RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md (ratified design)
  - review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md (historical; spec sections 2-7)
  - review/comms/DRAFT_PHASE2F_READINESS_SCORECARD_2026-05-13.md (owner-approved scope)
  - review/comms/DRAFT_AUDIT_CORPUS_LABEL_DISTRIBUTION_2026-05-13.md (gap evidence)
---

# MAIN_TERMINAL — Phase 2-F1 B1 FIRE NOW

**Orchestrator addenda to architect's draft (2026-05-22):**

- **Position-taxonomy collapse rule**: accepted as architect-specified. `{EP, HJ} → MP` class for position-balance quota counting. Operational set for the ≥5/batch floor: `{UTG, MP, CO, BTN, SB, BB}`.
- **5-way reference parallel workstream**: separately dispatched (architect subagent in flight; deliverables expected: `DRAFT_DESIGN_MEMO_5WAY_REFERENCE_SET_2026-05-22.md` + 10-hand JSONL + verification rubric). Independent of this directive.
- **Solver-verify queue drain (~33 spots post-batch-008)**: noted; B1 forecast +3-6 spots/batch. Drain workstream NOT auto-dispatched; orchestrator queues separately on owner gate.

---

## Authorization (trigger)

**Builder, you are the named author** of this directive per
`feedback_named_author_builds_not_polls.md`. Once orchestrator commits this file to master after
RATIFICATION_A1 ships, your **next tick AUTHORS**, not polls.

This directive is the "MAIN_TERMINAL_* — fire now" trigger per
`feedback_explicit_action_trigger.md`.

## Scope (single commitment)

Implement the positional-action-chain dimension scenario module per
`RATIFICATION_A1_POSITIONAL_CHAIN_2026-05-22.md`. Phase 2-F1 ONLY — corpus/scenarios scope.
**No prompt change. No KB change. No brief change.** The brief stays at v2 (split sizing
schema, landed via A0.3c on master).

## Deliverables (single PR, MILESTONE)

1. **`river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py`** —
   new Module 10 in the corpus-revision-scenarios family. Implements:
   - `class ChainFingerprint(NamedTuple)` per blueprint §2.1
   - `_CHAIN_FINGERPRINT_TEMPLATES: List[dict]` — at minimum 12 anchor templates (one per
     top-12 chain), expanded to ≥24 total templates to cover the 5 A1 mandatory quotas
     (Facing-Raise, River, Position-balance, Top-12, Sandwich) per ratification §Per-batch slot
     allocation table
   - `def enumerate_top_12_chains() -> List[ChainFingerprint]` per blueprint §6.3
   - `def generate_chain_scenarios(chain_fp, count, *, rng_seed, forbidden_fingerprints) -> List[SituationSpec]`
     per blueprint §6.3
   - `def generate_phase_2f_chain_quota(*, rng_seed, forbidden_fingerprints) -> List[SituationSpec]` —
     returns **24** SituationSpec instances (not 20; updated per ratification)
   - `def validate_chain_fingerprint(spec, expected_chain) -> bool` per blueprint §6.3

2. **`river-rats-core/corpus_revision_scenarios/_scenario_utils.py` patch** — add
   `compute_chain_fingerprint(spec) -> ChainFingerprint` helper that walks `action_history`
   and reconstructs the 7-tuple per blueprint §2.1. Pure function, no side effects.

3. **`river-rats-core/tests/test_positional_action_chain_scenarios.py`** — new test module.
   Required test cases:
   - CFP-1: `callers_chain` order matches `action_history` call-order
   - CFP-2: Aggressor seat-order precedes hero (postflop order SB < BB < UTG < HJ < CO < BTN)
   - CFP-3: Raiser seat-order between aggressor and hero
   - CFP-4: CHECK_RAISE requires aggressor's prior check on the same street
   - CFP-5: 4-way-at-decision player-count sanity (union test)
   - CFP-6: Board diversity ≥5 distinct boards per chain across templates
   - QUOTA-1: `generate_phase_2f_chain_quota` returns exactly 24 specs
   - QUOTA-2: Returned 24 specs satisfy facing-raise ≥10
   - QUOTA-3: Returned 24 specs satisfy river ≥5
   - QUOTA-4: Returned 24 specs satisfy position-balance (each of {BTN, CO, MP, UTG, SB, BB}
     ≥1 in 24 anchors; ≥5 expected after stratified-fill but stratified-fill is out of scope
     for the module test)
   - QUOTA-5: Returned 24 specs include all 12 top-12 chains at least once
   - QUOTA-6: Sandwich count ≥4
   - VALIDATION-1: `validate_chain_fingerprint` returns True for every template's own fingerprint
   - VALIDATION-2: `validate_chain_fingerprint` raises AssertionError with a precise diff when
     a deliberately-corrupted spec is passed

4. **`review/comms/phase2f1_top12_frequency_audit_2026-05-XX.md`** (pre-flight artifact) —
   builder re-derives top-12 chain rank from `data/4way_corpus/full_700/batch_00{1..8}_consensus_v2.jsonl`
   (the A0.3b-normalized v2 consensus files, which are the canonical post-A0 record).
   **Escalation gate:** if any chain shifts rank by >2 positions vs blueprint v1 §5.1, builder
   posts query comm to `review/comms/` and **HALTS module authoring** until architect ratifies
   the revised top-12. Rank shifts ≤2 are accepted silently and the v1 §5.1 anchor set stands.

5. **`review/comms/B1_MICRO_BATCH_YIELD_TEST_2026-05-XX.md`** — 20-hand deterministic micro-batch
   yield test report. Generates 20 SituationSpec instances via
   `generate_phase_2f_chain_quota(rng_seed=20260522)` (truncated to 20 from the 24-spec output)
   and reports:
   - Per-template hit count
   - Quota-floor satisfaction status (facing-raise, river, position-balance, top-12, sandwich)
   - Fingerprint-validation pass/fail (each of 20 specs)
   - Card-equivalence fingerprint dedup status (per `_scenario_utils.fingerprint`)
   - Run-time and rng-determinism check (same seed → same 20 hands)

## Acceptance criteria (the 9 from RATIFICATION_A1 §Acceptance check)

Reproduce here for builder convenience:

1. File `positional_action_chain_scenarios.py` git-tracked at the specified path
   (verify via `git ls-files | grep positional_action_chain_scenarios.py` — TC-23 EXISTENCE).
2. `enumerate_top_12_chains()` returns 12 entries matching v1 §5.1 rank order
   (post-frequency-audit; rank shifts ≤2 accepted).
3. `generate_phase_2f_chain_quota()` returns 24 SituationSpec covering all 5 A1 quotas.
4. `validate_chain_fingerprint()` raises with precise diff on mismatch.
5. `compute_chain_fingerprint()` helper in `_scenario_utils.py`.
6. 20-hand micro-batch yield test report committed.
7. Top-12 frequency audit committed with escalation-gate status.
8. CFP-1..CFP-6 + QUOTA-1..QUOTA-6 + VALIDATION-1..2 unit tests pass.
9. QC pre-merge audit per `feedback_qc_required_before_approval.md` (this is a MILESTONE PR).

## Out of scope (Phase 2-F2 — DO NOT TOUCH)

- `data/4way_labeller_brief.md` — stays at v2; no AMENDMENT 3, no FL6
- `prompts/gto_labeller_v3.4.md` — no rewrite to v3.5
- `knowledge/three_way_gto.md` — no v1.4 sync
- Drift-analyzer spec — Phase 2-F2 B-stream tooling
- Re-label of any existing batch (001-008) — Phase 2-F2 B2/B3
- Calibration gate redesign — Phase 2-F2 B0
- 5-way reference-set generation — parallel architect workstream, not this directive

If any of these surface as "would be cleaner if also..." during B1, builder posts a query comm
per `feedback_queries_to_orchestrator.md` and waits. Do not slip Phase 2-F2 scope into Phase 2-F1.

## Process

Per `docs/PROCESS_GUIDE.md` and `feedback_pilot_first_for_long_jobs.md`:

1. **Ground first** (per `feedback_builder_grounds_before_executing.md`): read v1 blueprint §§ 2-7
   and existing `sb_hero_scenarios.py` + `_scenario_utils.py` BEFORE writing code.
2. **Top-12 frequency audit first** (pre-flight artifact #4) — produces ratified anchor set.
3. **Tests before implementation** per `docs/PROCESS_GUIDE.md` §3 Test-First — author the test
   module first; tests define the contract.
4. **Build incrementally**: module → tests → micro-batch yield test → frequency audit → PR.
5. **20-hand micro-batch yield test BEFORE batch_009 production fires** (this is the
   pilot-first gate per `feedback_pilot_first_for_long_jobs.md`).
6. **Single PR**: all six files (module + utils patch + tests + 2 review/comms reports + this
   directive merge-back) ship in one PR as the MILESTONE.
7. **QC pre-merge** per `feedback_qc_required_before_approval.md`. Orchestrator triggers QC
   via `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<N>_2026-05-XX.md` once builder's PR opens.

## Stop conditions (improvise NOT)

Per `docs/PROCESS_GUIDE.md` §5 and `feedback_verify_source_not_plan.md`:

- **Frequency-audit rank shift >2 on any chain** → HALT, post escalation comm, await architect
  ratification before module authoring
- **`compute_chain_fingerprint` produces a fingerprint that no template can replicate** →
  HALT, post diagnostic comm
- **Postflop seat-order on a template violates CFP-2 or CFP-3** → reject the template, do not
  patch the validator
- **Sandwich-quota cannot be met with 24-slot allocation** → HALT and post query (this would
  indicate the ratification §Per-batch slot allocation table needs revision; architect-only
  decision)
- **Test failure in any CFP / QUOTA / VALIDATION test** → fix the module, not the test

## Output channels

- Builder writes to `review/comms/` per `feedback_review_autosave.md` (no permission needed).
- Reports use the `BUILDER_REPORT_PHASE2F1_B1_*` naming convention.
- Diagnostic comms use `BUILDER_OBSERVATION_PHASE2F1_B1_*` or `BUILDER_QUERY_PHASE2F1_B1_*` per
  the routing rules in `feedback_queries_to_orchestrator.md`.

## QC routing

Per `feedback_qc_routing_when_standalone_active.md`, QC audit runs in the standalone QC stream
(`~/river-rats-qc/`), not as a parallel subagent here. Orchestrator opens the QC trigger comm
when builder's PR is in review state.

## Closing — single commitment, no menus

**24 enumerated slots per batch. 6 batches (009-014). 5 mandatory floors. One PR.**
**Brief stays v2. Prompt stays v3.4. KB stays v1.3.** No Phase 2-F2 scope creeps in.

Fire when ratification ships.

— Orchestrator (Main Terminal), via Architect Phase 2-F1
