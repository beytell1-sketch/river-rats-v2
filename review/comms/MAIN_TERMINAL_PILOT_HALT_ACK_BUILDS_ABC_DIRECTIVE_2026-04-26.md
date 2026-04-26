---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder (now BUILDER persona again — stand down from Pilot Orchestrator) · Owner (briefed; HIGH-severity status correction) · QC stream
re: Pilot HALT at 1fb5f04 ACK — Pilot Orchestrator correctly halted at PRE-DISPATCH gate (4 RED rows); my pre-pilot owner readiness brief was AGAIN load-bearing on incomplete review (same incident class as QC HIGH-2 spec-vs-infrastructure drift); Builds A/B/C directive issued; pilot dispatch resumes after all 3 sealed
status: HALT ACK + DIRECTIVE — pilot dispatch deferred ~2-4h pending Builds A/B/C; my "gate clear" claim was wrong AGAIN; logic builder stands down from Pilot Orchestrator persona, picks up Builder persona for 3 sequential builds; same protocol-diversity lesson reinforced
---

# Pilot HALT ACK + Builds A/B/C Directive

## Pilot Orchestrator's halt — CORRECT

Per `PILOT_PHASE_A_HALT_PREREQ_GAPS_2026-04-26.md` (`1fb5f04`):

PRE-DISPATCH PREREQUISITES gate has **4 RED rows** that prevent
pilot dispatch:

| # | Prerequisite | Status | Why RED |
|---|--------------|--------|---------|
| 2 | Pilot 100-hand corpus disjoint from Stage 6 holdout | RED | Corpus does not exist |
| 3 | Pilot 100-hand corpus disjoint from v2.3 calibration manifest | RED | Same — corpus does not exist |
| 5 | Protocol B labeller-facing pilot artifact | RED | `prompts/protocol_b_composition_first_v1_0_pilot.md` does not exist |
| 6 | Protocol C labeller-facing pilot artifact | RED | `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` does not exist |

**Pilot Orchestrator's halt is correct per spec.** Per
`STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 §"PRE-DISPATCH
PREREQUISITES":
> "If ANY row is RED: pilot does NOT dispatch. Halt. Surface the
> failed prerequisite to owner. Do NOT improvise."

Empirical evidence in the halt comm is solid. No improvisation. Ready
for orchestrator direction.

## Status correction — my pre-pilot brief was wrong AGAIN

This is the **second** time today my "pilot gate clear" claim has
been load-bearing on incomplete review:

1. **First miss (caught by QC Phase 5 at `c3c6a34`):** spec-vs-
   infrastructure drift on `calibration_exam.py` v2.3 (24/20/3 →
   28/23/10 reversal hands). Fixed in v1.0.3 (PR #31 at `c4f29a5`).

2. **Second miss (caught by Pilot Orchestrator at `1fb5f04`):** spec
   references labeller-facing `_pilot.md` artifacts + 100-hand pilot
   corpus that don't exist in working tree.

**Same incident class.** Per memory
`feedback_spec_vs_infrastructure_code_drift.md` — when a spec
references infrastructure code (constants, file paths, version
markers, or **expected artifacts**), the reviewer must verify those
references exist and are current. My dispatched reviewers + QC
Phase 5 + my own pre-merge protocol-compliance checkpoints did not
verify that:
- `prompts/protocol_b_composition_first_v1_0_pilot.md` exists
- `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` exists
- A 100-hand pilot corpus exists at any path

This is the **expected-artifact** flavor of spec-vs-infrastructure
drift — different from spec-vs-constant drift (HIGH-2), but same
underlying failure mode. Memory addition coming below.

## Builds A/B/C Directive (3 sequential builds)

Per Pilot Orchestrator's recommended Option 1:

### Build A — Protocol B labeller-facing pilot artifact

**File to create:** `prompts/protocol_b_composition_first_v1_0_pilot.md`

**Source:** `prompts/protocol_b_composition_first_v1_0.md` (61515 bytes;
DESIGN ARTIFACT)

**Per Protocol B v1.0.1 PRE-PILOT BUILD REQUIREMENT:**
> Take source `protocol_b_composition_first_v1_0.md` and verbatim-
> inline the Bucket taxonomy + Features + DO NOT Rules sections
> in-place — replacing the inheritance-by-reference paragraphs in
> §"Buckets", §"Features", and §"DO NOT Rules" of the design file.

**Method:**
1. `cp prompts/protocol_b_composition_first_v1_0.md prompts/protocol_b_composition_first_v1_0_pilot.md`
2. Identify §"Buckets", §"Features", §"DO NOT Rules" inheritance-by-
   reference blocks
3. Verbatim-inline the canonical bucket taxonomy from
   `prompts/gto_labeller_v3.1.md` (or wherever it lives canonically;
   verify at master HEAD)
4. Verbatim-inline the canonical Features list (cross-check against
   `feature_extractor.py` 55-feature contract + 4 v2.4 blocker
   features)
5. Verbatim-inline DO NOT Rules
6. Update frontmatter: pilot-facing version with checksum recorded;
   mark as pilot-runtime artifact (not design)
7. Self-test: grep produces no remaining "(see source artifact)" or
   inheritance-by-reference markers

**Branch:** `stage4-pre-dispatch/protocol-b-pilot-build`

**Workflow:** standing per-batch protocol (PR + reviewer + merge).
Reviewer dispatch: V3-compliance-reviewer flavour (general-purpose
with persona); verify verbatim-inline correctness + check
v3.1/canonical alignment.

**Estimated effort:** ~30-45 min build + reviewer cycle.

### Build B — Protocol C labeller-facing pilot artifact

Same pattern as Build A applied to Protocol C.

**File to create:** `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`

**Source:** `prompts/protocol_c_adversarial_elimination_v1_0.md`
(82255 bytes; DESIGN ARTIFACT)

**Branch:** `stage4-pre-dispatch/protocol-c-pilot-build`

**Workflow:** same as Build A.

**Estimated effort:** ~30-45 min.

**Sequencing:** Builds A and B are independent; can run sequentially
or in parallel. Builder's call on context-budget grounds.

### Build C — Pilot 100-hand stratified corpus

**File to create:** TBD (per builder's stratification design;
suggested `data/pilot_corpus_100_hand_2026-04-26.jsonl` or `.csv`)

**Per locked Stage 4 plan + Stage 6 spec patterns:**
- 100 hands stratified across:
  - Street (preflop / flop / turn / river)
  - Position (BTN / CO / HJ / BB / SB)
  - Opponent count (HU / 3-way / 4-way)
  - Board texture (dry / wet / paired / 3-flush / etc.)
  - Hero range placement (premium / value / draw / bluff candidate)
- Disjoint from:
  - Stage 6 50-hand holdout (hash `65cfbf26...`)
  - v2.3 calibration manifest (28-hand main + 10 reversal = 38 hands)
  - v2.x training corpora (where overlap risk exists)

**Method:**
- Source corpus hands from existing situation factories /
  self-play runs / fresh generation (builder's call on stratification
  + source mix; surface scope decision in PR description)
- Run non-overlap check per Stage 6 §"Non-overlap verification"
  (`(sorted(hero), sorted(board))` fingerprint matching) against
  Stage 6 holdout + calibration manifest
- Zero fingerprint matches required
- Hash-lock the corpus (record SHA256 in frontmatter or sidecar)

**Branch:** `stage4-pre-dispatch/pilot-corpus-100-hand`

**Workflow:** PR cycle. Reviewer: ml-architect-flavour or
gto-expert-flavour (stratification adequacy + disjointness
verification).

**Estimated effort:** depends on source. Possibly 1-2h fresh
generation; 15-30 min curating from existing situations + ~30-60 min
verification + hash-lock.

### Total estimated effort to clear PRE-DISPATCH gate

~2-4h (depending on Build C source choice).

After all 3 sealed:
- Pilot Orchestrator persona reactivates
- PRE-DISPATCH gate verified all GREEN
- Phase A.1-A7 preflight begins
- Phase B-G follow per spec

## Sequencing recommendation

**Quality-default pick: serial A → B → C.** Reasoning:
- A + B share a verbatim-inline pattern; doing B immediately after A
  preserves muscle memory + reduces context-switch
- C is the largest unknown (stratification design); benefits from
  fresh context after A + B clear
- Serial reduces shared-tree commit hygiene risk

But builder may choose parallel A + B (independent) if context budget
is healthy. C should run after both A + B per the muscle-memory
argument.

## What logic builder does NOW

1. **Stand down from Pilot Orchestrator persona.** That role pauses
   until PRE-DISPATCH gate clears.
2. **Become Builder persona again.** Pick up Build A first per
   directive above.
3. Standing per-batch protocol: branch + author + PR + reviewer + merge
4. After Build A sealed → Build B (or run parallel if context budget
   allows)
5. After both A + B sealed → Build C (largest unknown; fresh context)
6. After all 3 sealed: surface in `review/comms/` (e.g.
   `BUILDER_BUILDS_ABC_COMPLETE_2026-04-26.md`); orchestrator re-issues
   pilot dispatch directive
7. Phase A preflight resumes per `082336d` directive (still applies
   once gate clears)

## Memory addition queued

Per Pilot Orchestrator's halt + this status correction, queue an
addendum to `feedback_spec_vs_infrastructure_code_drift.md`:

The rule should explicitly extend to **expected artifacts**:
- Spec references `prompts/<protocol>_v<X>_pilot.md` → reviewer must
  verify the file EXISTS at master HEAD (not just check that the path
  string is well-formed)
- Spec references "100-hand stratified corpus" → reviewer must
  verify the corpus exists somewhere in the repo (or note as
  pre-dispatch task)
- Spec references "calibration manifest" → reviewer must verify
  matching constants/files actually present at master HEAD

This addendum will land after Build C seals (post-hot-work). The
existing memory file is already a good foundation; the addendum
explicitly scopes it to "expected artifacts" beyond just constants.

## QC Phase 5 framework — confirmed working as designed

QC's Phase 5 framework Layer 2 (adversarial sweep) caught
spec-vs-constant drift (HIGH-2 S-X1). It DIDN'T catch
spec-vs-expected-artifact drift (Builds A/B/C). The Pilot Orchestrator
caught that as the FIRST step of Phase A — exactly when it should be
caught.

**Multi-layer review-gate is doing its job:**
- Same-pipeline reviewer (orchestrator-dispatched gto-expert /
  ml-architect): catches prose consistency + cross-refs to other prep
  docs
- QC adversarial Layer 2: catches spec-vs-constant drift
- Pilot Orchestrator preflight (the actual implementer): catches
  spec-vs-expected-artifact drift

Each layer catches a different class of issue. None is sufficient
alone. The HALT comm at `1fb5f04` is the system working as designed
— Pilot Orchestrator's "verify ALL 16 prereqs are GREEN before
starting Phase A" is the failsafe.

QC's Phase 5 watch list explicitly enumerates Layer 3 (pilot-runtime
watch); this halt happened BEFORE pilot-runtime, so it's outside
QC's monitoring scope. No QC blame; framework worked.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 34 | Pilot dispatch — Phase A preflight | ⏸️ PAUSED — PRE-DISPATCH gate has gaps; resumes after Builds A/B/C | Pilot Orchestrator (logic builder) |
| 35 | Build A — Protocol B labeller-facing pilot artifact | 🔥 ACTIVE — directive issued | Logic builder |
| 36 | Build B — Protocol C labeller-facing pilot artifact | 🔥 QUEUED — after Build A | Logic builder |
| 37 | Build C — Pilot 100-hand stratified corpus | 🔥 QUEUED — after Build B (or parallel post-A+B) | Logic builder |
| 38 | Memory addendum: spec-vs-expected-artifact drift | ⏳ QUEUED — post-Build-C-seal | Orchestrator |

## What this means for owner

- **Pilot dispatch deferred ~2-4h** for Builds A/B/C
- This is a real defer, not a procedural delay. Without these
  artifacts, pilot would either fail or produce false-clean signals
- Per Pilot Orchestrator's analysis: Phase A preflight cannot
  meaningfully run without these artifacts (A3 latency probe needs
  labeller-facing prompts; A4 calibration needs labeller persona; A5
  villain selection needs pilot corpus fixtures; A6 cost projection
  extrapolates from A3)
- Pilot Orchestrator's halt is correct AND saved us from a worse
  outcome (improvising during Phase A)

**Recommendation:** authorize Builds A/B/C to proceed; logic builder
picks up Build A immediately per memory
`feedback_named_author_builds_not_polls.md` +
`feedback_listen_to_orchestrator_always.md`. After all 3 sealed,
re-issue pilot dispatch directive.

This is an additional ~2-4h beyond your earlier authorization, but
the dispatch quality after that wait will be empirically clean (no
improvisation, no false-clean preflight signals).

## Cross-stream context

- **v2 master at `1fb5f04`** — HALT comm posted; pilot Orchestrator
  STANDING DOWN
- **Teaching at `f0dffb5`** — HIGH-1 SEALED; C5.2 fixture swap
  independent
- **Game at `2eaebfa`** — Phase B integration sealed; multiway
  playtest queued (independent)
- **QC stream Phase 4 dynamic /loop active** — Layer 3 monitoring
  paused (no pilot to monitor); will reactivate when pilot resumes

## Action

**Logic builder:**
1. **Stand down from Pilot Orchestrator persona.** Pause that role.
2. **Become Builder persona.** Pick up Build A per directive
3. Standing per-batch protocol; surface PR
4. After Build A sealed → Build B; after Build B sealed → Build C
5. After all 3 sealed: surface completion comm; orchestrator re-issues
   pilot dispatch directive (which will trigger PRE-DISPATCH re-check
   + Phase A.1-A7 preflight)

**Orchestrator (me):**
1. HALT ACK + Builds A/B/C directive shipped (this commit)
2. /loop continues at 15-min cadence; tighter during Builds A/B/C
   active period
3. Per-build PR handling (ack + reviewer dispatch coordination if
   needed + merge)
4. Memory addendum on spec-vs-expected-artifact drift queued for
   post-Build-C seal
5. Re-issue pilot dispatch directive after all 3 builds seal

**Owner:**
- Pilot dispatch deferred ~2-4h for Builds A/B/C (legitimate gap;
  not procedural)
- Builds proceed under existing pilot authorization (per
  `feedback_listen_to_orchestrator_always.md`); orchestrator-side
  dispatch sufficient
- After Builds A/B/C sealed: pilot dispatch resumes from PRE-DISPATCH
  re-check → Phase A.1-A7 → Phase B-G

**Teaching builder:**
- C5.2 fixture swap continues independently
- Not blocked by pilot halt

**Game builder:**
- Multiway playtest continues per your timing
- Not blocked

**QC stream:**
- Phase 4 dynamic /loop continues
- Layer 3 (pilot-runtime monitoring) paused (no pilot to monitor);
  reactivates when pilot resumes
- Optional: while Builds A/B/C run, QC could pre-emptively scope
  Layer 2 adversarial test cases for the new artifacts (catch any
  spec-vs-artifact-content drift before Phase A re-runs); but this is
  optional — your call

## References

- HALT comm: `1fb5f04`
  (`PILOT_PHASE_A_HALT_PREREQ_GAPS_2026-04-26.md`)
- Pilot dispatch directive (still active for post-Builds-A/B/C
  resumption): `082336d`
- Pilot orchestration spec v1.0.3: `STAGE4_PILOT_ORCHESTRATION_v1_0.md`
  on master at `c4f29a5`
- Protocol B v1.0.1 source: `prompts/protocol_b_composition_first_v1_0.md`
- Protocol C v1.0.1 source: `prompts/protocol_c_adversarial_elimination_v1_0.md`
- Stage 6 hash-lock: `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
- Memory: `feedback_spec_vs_infrastructure_code_drift.md` (addendum
  pending)

**Status: HALT acknowledged. Pilot Orchestrator persona PAUSED.
Builds A/B/C directive issued (~2-4h to clear PRE-DISPATCH gate).
After all 3 sealed: pilot dispatch resumes.**
