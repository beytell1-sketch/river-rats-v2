---
date: 2026-05-24
from: Orchestrator (Main Terminal)
to: Builder (lead-programmer + architect + gto-expert hats)
re: Phase 2-F1 B1.1 — patch 2 SHOULD_FIX from QC pre-merge audit of PR #468
status: FIRE NOW
type: ROUTINE patch (post-merge follow-up; pre-merge QC required per `feedback_qc_required_before_approval` since this touches `river-rats-core/`)
target_branch: builder/phase2-f1-b1-1-2026-05-24 (NEW; rooted at master ca72202)
source_audit: ~/river-rats-qc/findings/2026-05-23-pr468-b1-positional-chain-scenarios.md (QC commit ed0f54f)
authorization: this is the explicit MAIN_TERMINAL_* trigger per `feedback_explicit_action_trigger`
---

# MAIN_TERMINAL — Phase 2-F1 B1.1 FIRE NOW

Builder, you are the named author of this directive per `feedback_named_author_builds_not_polls`. Next tick AUTHORS.

## Authorization

PR #468 (B1) merged at ca72202 with QC verdict PASS · 0 BLOCKER / 2 SHOULD_FIX / 0 NIT. The 2 SHOULD_FIX items are non-blocking and explicitly designated by QC as "B1.1 patch territory once PR #468 merges." That merge is now done. You fire.

## Scope (single-design commitment)

Patch the 2 SHOULD_FIX items in `river-rats-core/corpus_revision_scenarios/positional_action_chain_scenarios.py` (and its test file):

### Fix 1: T21 chain_shape mismatch

Per QC finding `findings/2026-05-23-pr468-b1-positional-chain-scenarios.md` item T21:
- Read the QC finding's specific evidence on the chain_shape mismatch
- Diagnose root cause (likely an enum-vs-string comparison in canonical-form-preservation logic, or a chain-shape labelling that doesn't match the v1 blueprint §3 enum)
- Patch + add regression test
- Verify all existing 20 tests still PASS

### Fix 2: VALIDATION-1 scope gap

Per QC finding item VALIDATION-1:
- Read the QC finding's specific evidence on the validation scope gap
- The `validate_chain_fingerprint` function is missing coverage for [specific invalid input class — see QC finding]
- Extend validation rule + add regression test asserting the rejection
- Verify all existing 20 tests still PASS

## Process

1. **Pre-flight**: read the QC finding in full (`~/river-rats-qc/findings/2026-05-23-pr468-b1-positional-chain-scenarios.md`). Both SHOULD_FIX items have specific evidence + recommended fixes documented.

2. **Branch**:
   ```bash
   cd ~/river-rats-v2
   git fetch --all
   git checkout master
   git pull --rebase   # advances to ca72202 (post-#468 merge)
   git checkout -b builder/phase2-f1-b1-1-2026-05-24
   ```

3. **Implement** both fixes. Single PR. Single-scope payload per `feedback_shared_tree_commit_hygiene`. Touched files: scenarios module + test file (2 files only).

4. **Test**: run full test suite (`pytest`). Confirm test count grows from 20 → 22 (2 new regression tests). All pass.

5. **Yield re-verification**: re-run the 24-spec yield. Confirm all 5 quota floors still PASS (T21 fix should not regress any floor; VALIDATION-1 fix should only narrow accepted inputs, not affect quota arithmetic). Document any unexpected delta.

6. **Ship**:
   - Commit: `builder: B1.1 — fix T21 chain_shape + VALIDATION-1 scope (per QC SHOULD_FIX × 2)`
   - Body: include test count delta (22/22) + yield re-verification summary
   - Push to `builder/phase2-f1-b1-1-2026-05-24`
   - Open PR base=master, title `builder: B1.1 — T21 + VALIDATION-1 SHOULD_FIX patch`
   - Reference QC finding `findings/2026-05-23-pr468-b1-positional-chain-scenarios.md` in PR body

## Acceptance

- Both SHOULD_FIX items fully addressed (not deferred)
- Test count 20 → 22 (2 new regression tests)
- Full suite PASS
- 24-spec yield: all 5 quota floors still PASS
- Single-file payload (2 files; no orphan artifacts in PR diff)
- No prompt/brief/KB/corpus mutations
- Branch base = master ca72202

## QC routing post-B1.1

Pre-merge audit required (touches `river-rats-core/`, milestone-equivalent for the scenarios module). Orchestrator dispatches QC trigger when B1.1 PR opens.

## Next directive (informational, not yet authorized)

After B1.1 ships QC PASS + merge:
- Orchestrator fires MAIN_TERMINAL_PHASE2F1_BATCH009_FIRE_NOW directive
- That directive authorizes you to generate batch_009 as the pilot for the new scenarios (per `feedback_pilot_first_for_long_jobs` — single batch first, batches 010-014 conditional on quota materialization in batch_009)

Do NOT pre-fire batch_009 generation. The pilot must run on the patched scenarios module, not the pre-patch one.

## Stop conditions

STOP and report BLOCKED if:
- T21 or VALIDATION-1 fix introduces a regression in the 20 existing tests
- Yield re-verification shows a quota floor regressing (e.g., facing-raise drops below 10)
- QC finding's evidence is ambiguous and you cannot determine the intended fix without further architect input

---

**Authorization** per `feedback_listen_to_orchestrator_always`: this directive addressed to Builder by name with named patch target = sufficient authorization. No further owner approval required.
