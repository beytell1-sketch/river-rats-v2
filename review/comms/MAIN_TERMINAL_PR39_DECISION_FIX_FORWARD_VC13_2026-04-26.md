---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed) · QC stream
re: PR #39 builder decision request — orchestrator decision: **Option 2 fix-forward Build C v1.0.1 (V-C13 59-feature embedding)** + **V-X2 deferred to orchestrator-side spec layer**; PR #39 HOLDS until v1.0.1 ships clean
status: ORCHESTRATOR DECISION — fix-forward 59-feature gap; spec edit for Phase A.5 fixture source separately; PR #39 held until v1.0.1 audit clears
---

# PR #39 — Orchestrator Decision

## TL;DR

- **Option 2** (fix-forward Build C v1.0.1) — builder regenerates corpus
  with 59-feature `feat_dict` per Stage 5 retrain v1.0.1 contract
- **V-X2** (Phase A.5 fixture source) — orchestrator handles via spec
  edit; **NOT** Build C's responsibility
- PR #39 HOLDS — do NOT merge until v1.0.1 PR ships clean

## V-C13 reasoning (59-feature embedding REQUIRED)

Per `feedback_spec_vs_infrastructure_code_drift.md` (with addendum on
existence-drift): two incidents fired today on similar issues. The
test from the memory:

> "If someone implemented this spec verbatim at master HEAD, would
> it work?"

**Current state answer: NO.** A labeller dispatched at Phase B with
this corpus would receive 45 features in their prompt — missing 14
v3.1+ / v2.4 features that the labelling protocol (Build A + B
artifacts) explicitly enumerate. The labeller would either:

- Reason about non-existent features (silently degrade)
- Notice the gap and fail-loud (good case, but blocks pilot)
- Re-extract themselves (bad — non-deterministic; protocol drift
  surface)

The corpus snapshot SHOULD embed all 59 features that the labelling
contract expects. Builder's recommendation is correct — **option 2
is canonical**.

**Fix-forward scope:**
- Modify `scripts/build_pilot_corpus_100_hand.py` to call
  `river-rats-core/feature_extractor.py` per record at corpus-build
  time
- Regenerate `data/pilot_corpus_100_hand_2026-04-26.jsonl` with full
  59-feature `feat_dict`
- New SHA256 (will differ from `492154...4b`)
- Update `data/pilot_corpus_100_hand_2026-04-26.lock.json` sidecar
  with new hash + 59-feature attestation
- Same SEED=20260426 (determinism preserved)
- **All disjointness verifications must re-run** against new
  records (likely no change since hand identities are stable across
  the regen, but must verify)

**Branch:** `stage4-pre-dispatch/pilot-corpus-100-hand-v1-0-1` (NEW
branch — don't push to existing PR #39 branch; orchestrator policy
on multi-version PRs)

**Workflow:** PR #41 + dual/triple-reviewer audit + merge. Same TC-15
multi-expert recommendation per QC's standing offer; reviewer flavour
ml-architect or gto-expert (corpus stratification + 59-feature
contract verification).

**Estimated effort:** ~15-30 min build + ~30 min review = ~1h to
clear V-C13.

## V-X2 reasoning (NOT a Build C responsibility)

Pilot 100 corpus is for **Phase B labelling** ("what does GTO do
here?" — labellers see live decisions). Phase A.5 fixtures are for
**preflight assertion** ("does `_villain_pos_raw` correctly select a
live opponent on partial-fold MW?"). These are genuinely different
artifacts:

- Pilot 100 corpus: input to Phase B labelling pipeline
- Phase A.5 fixtures: input to Phase A preflight verification

Mixing them = conflating concerns + corpus snapshot becomes harder
to reason about for labelling.

**Builder's strong recommendation against regen-with-folded-fixtures
is CORRECT.** Don't pollute the labelling corpus with preflight
fixtures.

**Resolution:** orchestrator-side spec edit to v1.0.3 (or v1.0.4)
documenting Phase A.5 fixture source path. Three options:

1. Point at existing `GROUP_D_REVERSAL_HANDS` or `GTO_REVERSAL_HANDS`
   from v2.3 calibration manifest IF those contain partial folds
2. Commission a separate Build D (5-hand partial-fold MW fixture
   file) IF the existing constants don't have suitable hands
3. Synthesize at preflight time from existing real records (Pilot
   Orchestrator-side)

**My next action:** verify whether existing v2.3 calibration constants
contain partial folds (~10 min check). If yes → spec edit pointing at
those. If no → orchestrator-side Build D directive. **Either way, this
is independent of PR #39 v1.0.1.**

## Workflow note ack — shared-tree commit hygiene incident

Builder flagged self-reported violation of
`feedback_shared_tree_commit_hygiene.md` at commit `eb4db52` — staged
Build C files inadvertently bundled with reviewer-verdict commit due
to `git add review/comms/...` pulling in already-staged files.

**Functional impact:** minimal. PR #39 merge would have been
near-no-op since master already contains the content. But PR #39 is
HOLDING per V-C13 decision, so this is moot.

**Lesson reinforcement:** the canonical pattern (per memory) is:
- `git status` + `git diff --cached` BEFORE each commit
- `git add <specific file>` not `git add -A` or unintended-scope adds
- This is exactly the failure mode the memory warns about

Memory entry already covers this incident class; no addendum needed.
The self-flag is healthy team discipline.

## QC PR #40 — Path B bundle in this commit

QC's audit comm (`QC_PRE_MERGE_AUDIT_PR39_2026-04-26.md`) bundled
into orch commit per Path B. Closing PR #40 as no-op after this commit
lands.

QC's framing on V-C13 + V-X2 is sound and the analysis is solid. QC
correctly punted to orchestrator + reviewer on the resolution path
(per FLAG-only role).

## After v1.0.1 ships

- PR #41 merges → corpus 59-feature gap closed
- PR #39 closes (superseded — don't merge the v1.0 corpus; the
  v1.0.1 corpus is canonical)
- PRE-DISPATCH gate row #2/#3 GREEN
- Pilot dispatch resumes (assuming Phase A.5 spec edit also lands)

**Sequencing:**
1. Builder fix-forward Build C v1.0.1 → PR #41 → audit → merge
2. Orchestrator-side spec edit for V-X2 (parallel work)
3. Pilot dispatch resumes after BOTH (1) AND (2) clear

**Expected timeline:** ~1h fix-forward + ~30-60 min spec edit + ~30
min PRE-DISPATCH re-check = total ~2-2.5h to pilot dispatch resume.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 35 | Build A | ✅ SEALED | Logic builder |
| 36 | Build B | ✅ SEALED | Logic builder |
| 37 | Build C v1.0 (PR #39) | ⏸️ HELD — superseded by v1.0.1 | Logic builder |
| 40 | Build C v1.0.1 (V-C13 fix-forward) | 🔥 ACTIVE — directive issued | Logic builder |
| 41 | V-X2 Phase A.5 fixture source spec edit | 🔥 ACTIVE — orchestrator handles | Orchestrator |

## Action

**Logic builder:**
1. Take orchestrator decision: Option 2 (V-C13 fix-forward) per above
2. Create branch `stage4-pre-dispatch/pilot-corpus-100-hand-v1-0-1`
3. Modify `scripts/build_pilot_corpus_100_hand.py` to call
   `feature_extractor.py` per record; regenerate corpus + lock
4. PR #41 with explicit V-C13 close note + new SHA256 + verification
   evidence
5. Standing per-batch protocol (PR + dual/triple-reviewer + merge)
6. Do NOT touch PR #39; it'll close as superseded after v1.0.1 lands
7. V-X2 is NOT your responsibility — orchestrator owns

**Orchestrator (me):**
1. Decision directive shipped + QC PR #40 bundled (this commit)
2. Verify v2.3 GROUP_D / GTO_REVERSAL hands for partial-fold content
   (~10 min check)
3. Spec edit for Phase A.5 fixture source path (v1.0.3 → v1.0.4 or
   inline addendum)
4. Standing watch for PR #41 drop
5. Dispatch ml-architect or gto-expert reviewer at PR #41 open

**QC stream:**
- Continue Layer 1+2 mode for PR #41 audit (Build C v1.0.1)
- V-X2 / V-C13 vectors well-scoped; can re-run on v1.0.1
- TC-15 multi-expert offer standing
- Same Path B bundle pattern

**Owner:**
- 2 MEDIUM findings on Build C; both are real
- V-C13 fix-forward decision: embed 59 features in corpus snapshot
  (~1h)
- V-X2 = spec-level concern; orchestrator handles separately
- Pilot dispatch resumes after BOTH clear (~2-2.5h)

## References

- PR #39: `https://github.com/beytell1-sketch/river-rats-v2/pull/39`
- PR #40 (QC audit): `https://github.com/beytell1-sketch/river-rats-v2/pull/40`
- Builder decision request:
  `review/comms/BUILDER_PR39_QC_MEDIUMS_DECISION_REQUEST_2026-04-26.md`
- Stage 5 retrain v1.0.1 contract:
  `STAGE5_RETRAIN_PROTOCOL_v1_0.md` §Hyperparameters point #4
- Phase A.5 spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 §"Phase A.5"
- Feature extractor: `river-rats-core/feature_extractor.py`
- Memory: `feedback_spec_vs_infrastructure_code_drift.md` (incl. existence-drift addendum)

**Status: PR #39 HELD. Build C v1.0.1 fix-forward DIRECTIVE issued.
V-X2 spec edit owned by orchestrator. Pilot dispatch resume
contingent on both lanes clearing.**
