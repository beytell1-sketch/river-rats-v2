---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: Step-by-step directive to blueprint v2.2 — consolidates Q32-Q35 + reconciliation #2 MUSTs + grounding findings
status: DIRECTIVE — single source of next steps; no options; quality default applies
---

# Stage 3.5 Blueprint v2.2 — Step-by-Step Directive

Combines:
- Builder's grounding report (3e50dd5) — Q32-Q35 + 1 major contradiction surfaced
- Multi-agent reconciliation #2 (b8f9563) — 16 new MUSTs (#28-#43)
- Owner direction: "clear direction, in steps, no more confusion"

Decisions made. No optionality. Builder executes the steps.

═══════════════════════════════════════════════════════════════
SECTION A — Q32-Q35 RESOLUTIONS
═══════════════════════════════════════════════════════════════

**Q32 (MUST #26 target scope) — (C) hybrid.** Patch
`assemble_pilot_data.py` AND `assemble_v23_clean.py` as reference
implementations + author `docs/ASSEMBLER_PATTERN.md`. Stage 4's
future `assemble_v2_4.py` clones from this pattern; Stage 4 review
gates on conformance.

**Q33 (MUST #27 target scope) — (C) hybrid + audit.** Same hybrid for
`run_attention_experiments.py`. ALSO audit `train_v2_3_1.py` +
`train_v2_3_2.py` for the same hardcoded-count pattern. If they share
it, patch as reference implementations in the same commit.

**Q34 (push supplement now vs fold) — (B) fix-forward.** Builder
amends supplement at `3166759` in-place via a NEW commit on top.
Single-supplement review trail. Reviewer panel sees blueprint v2
(8bb0f9f) + final amended supplement (whatever new HEAD lands).

**Q35 (production labelling format vs pilot format) — verify FIRST,
not embedded.** New MUST #44 (CRITICAL) below. Read 1 production-
labelled JSONL record from Phase 4 output (per `PHASE_4_LABELLING_REPORT_2026-04-17.md`),
diff against pilot schema. Result determines WHERE MUST #26's strict
gate fires (pilot assembler vs production assembler vs both). Cannot
patch correctly without this verification.

═══════════════════════════════════════════════════════════════
SECTION B — MUST #29 REFRAMING
═══════════════════════════════════════════════════════════════

My reconciliation #2 MUST #29 was framed against builder's wrong
supplement framing. Reframe per grounding:

**MUST #29 (REFRAMED) — Establish reference pattern; future Stage 4
script gates on conformance.**

- `assemble_pilot_data.py` (v2.2 pilot) + `assemble_v23_clean.py`
  (v2.3) both gain MUST #26 strict-mode + audit-column pattern as
  reference implementations
- New `docs/ASSEMBLER_PATTERN.md` documents the pattern
- Stage 4's `assemble_v2_4.py` (future work, doesn't exist yet)
  must clone the pattern; gated on Stage 4 review
- Original MUST #29 wording about "actual silent-0 surface" still
  applies AT each reference implementation, just not as a corrective
  patch to a single existing v2.4 file

═══════════════════════════════════════════════════════════════
SECTION C — NEW MUST #44 (from Q35)
═══════════════════════════════════════════════════════════════

**MUST #44 (CRITICAL) — Production labelling format verification
PRECEDES MUST #26 patching.**

Read one production-labelled JSONL record produced by Phase 4
labelling pipeline (per `PHASE_4_LABELLING_REPORT_2026-04-17.md`,
labelled with v3 prompt at commit `3dfc35f`). Diff against pilot
schema (`pilot_20_enriched.jsonl`'s `attention_flags` dict format).

Three possible outcomes; each determines MUST #26 patch scope:

- **(i)** Same schema → MUST #26 patches both pilot + v2.3 reference
  implementations identically; v2.4 production assembler clones either
- **(ii)** Different schema → MUST #26 needs separate strict-gate
  variants per schema; document both in `docs/ASSEMBLER_PATTERN.md`
- **(iii)** Production output doesn't carry `attention_flags` at all
  → MUST #26 strict-gate fires at the labelling-output → assembly
  bridge; broader scope shift

Verification + outcome reported in blueprint v2.2 supplement amendment
BEFORE MUST #26 patches are spec'd.

═══════════════════════════════════════════════════════════════
SECTION D — TOTAL MUST INVENTORY (41 + 1 = 42)
═══════════════════════════════════════════════════════════════

For the avoidance of confusion:

| # | Source | Status |
|---|---|---|
| 1-5 | Original reconciliation (11fe501) | Original 5; in blueprint v2 |
| 6-19 | Multi-agent reconciliation #1 (11fe501) | 14 from first reviewer panel; in blueprint v2 |
| 20-23 | Builder research findings (ae6160b) | 4 from builder's own research; in blueprint v2 |
| 24 | Orchestrator attention-flag ticket (8c4466c) | RETRACTED per correction (ce7ad3f); KB §1.11 already covers |
| 25 | Same | REFRAMED as Stage 3 deliverable (already in builder's plan) |
| 26-27 | Supplement (3166759) | In supplement; reframed per Section B above |
| 28-43 | Reconciliation #2 (b8f9563) | 16 from second reviewer panel |
| 44 | This directive (Section C) | Production format verification |

**Net: 25 active MUSTs from blueprint v2 + supplement + 16 from
reconciliation #2 + 1 new from Q35 = 42 active MUSTs.** #24 and #25
are inactive (retracted/reframed).

═══════════════════════════════════════════════════════════════
SECTION E — STEP-BY-STEP TO BLUEPRINT V2.2 SUPPLEMENT
═══════════════════════════════════════════════════════════════

Execute in order. No skipping. No reordering without orchestrator
approval. Each step has a clear deliverable.

### STEP 1 — Source re-verification pass

Before any blueprint edit, re-verify ALL the source-level claims
flagged by reconciliation #2 + this directive:

1.1 `coaching/explain_hand.py` — confirm bypass sites at lines
    251, 261, 264, 326, 329 (verify exact line numbers via
    `git show origin/master:river-rats-core/coaching/explain_hand.py`).
    Per MUST #30.
1.2 `gto_model.py:64` — confirm `N_FEATURES = len(FEATURE_COLUMNS)`
    actual value (verify it's 55, not 54). Identify the held-back
    feature. Per MUST #31.
1.3 `pilot_20_attention.csv` header — confirm column count (54 raw +
    54 attn + label = 109 vs 55 raw + 55 attn + label = 111). Per
    MUST #31.
1.4 `train_v2_3_1.py` + `train_v2_3_2.py` — read full files;
    identify any hardcoded column counts. Per Q33.
1.5 **Phase 4 production-labelled JSONL record** — read 1 record
    from output of the 470-hand labelling round. Per MUST #44.
    Document schema in supplement.

Output: a single section in the supplement amendment titled
"Source re-verification results" with each item + finding.

### STEP 2 — Amend supplement v2.1 in-place (Q34 = B)

Cut the supplement amendment. Single new commit on top of `3166759`.
Naming: `BUILDER_V24_STAGE35_BLUEPRINT_V2_1_SUPPLEMENT_AMENDED_2026-04-22.md`
(or amend the existing supplement file in place — your call,
single-document review trail either way).

Required content (in this order):

2.1 Section "Source re-verification results" from STEP 1
2.2 Reframe MUST #26 + MUST #27 per Q32/Q33 (C) hybrid scope
    - Explicit BEFORE/AFTER for `assemble_pilot_data.py` + `assemble_v23_clean.py`
    - Explicit BEFORE/AFTER for `run_attention_experiments.py` + (if hardcoded count present) `train_v2_3_1.py` + `train_v2_3_2.py`
    - `docs/ASSEMBLER_PATTERN.md` outline (full draft can land at commit time)
    - Stage 4 + Stage 5 prescriptive language ("future `assemble_v2_4.py` must follow…")
2.3 New MUST #44 spec — Q35 verification result + scope adjustment
    if needed
2.4 Address ALL 16 MUSTs from reconciliation #2 (#28-#43):
    - MUST #28: floor-truncation NaN-flag — patch `extract_range_composition`
      to consume `chain_meta['truncated']`
    - MUST #29: REFRAMED per Section B above (already addressed in 2.2)
    - MUST #30: 14-site caller list with `coaching/explain_hand.py:264, 329`
      added to commit 1; `coaching/explain_hand.py:251, 261, 326` added to
      MUST #6 commit 6
    - MUST #31: feature-count reconciliation per STEP 1.2-1.3 findings
    - MUST #32: commit-sequence lockout — pick (a) env default = raise
      OR (b) commits 4+5 merged. Document choice + reasoning
    - MUST #33: corpus reauthoring values updated to GTO-corrected targets
      (T_J01: 0.50/0.18/0.32; T_B05: 0.60/0.28/0.05/0.07; T_J02 added:
      0.60/0.18/0.22) + verdict-flip ship criterion for T_J01
    - MUST #34: MUST #6 helper consumes `_villain_range_narrowed` cache;
      multiway branch FULLY SPEC'D (per-villain chain × MC trial loop OR
      primary-villain-only with multi-villain composition aggregated)
    - MUST #35: sidecar sentinel `_SIDECAR_MISSING = object()` + automated
      validator script
    - MUST #36: CSV-header reconciliation replaces tautological width assert
    - MUST #37: pre-deletion sys.path-side-effect audit for surviving
      coaching/* modules
    - MUST #38: frequency table coherence — bluff/air check freqs adjusted
      alongside medium_made
    - MUST #39: KB §1.11 asymmetric thresholds (FOLD-lean 0.20 vs CALL-lean
      0.15)
    - MUST #40: combo-draw use-max addendum to KB §1.11
    - MUST #41: belt-and-braces count guard (`>=5 hands when surviving>=0.20`)
    - MUST #42: NaN render player-English wording
    - MUST #43: `TICKET_CONTENT_API_V4_NAN_RENDER_2026-04-22.md` authored
2.5 Updated commit sequence (15 + 11A/11B from supplement + any new
    commits for #28/#34/#35/#36/#37/#41) + lockout per #32
2.6 Updated questions list (Q20-Q31 from prior + Q32-Q35 resolved
    here)
2.7 Manifest version reference fix v1.9 → v1.10 throughout

### STEP 3 — Push the amended supplement

Push to origin. Single commit on top of `3166759`. Builder controls
the commit message; orchestrator does not pre-author it.

### STEP 4 — Orchestrator dispatches reconciliation pass #3

Same 5-reviewer panel (architecture, GTO, red-team, practical,
research). Reviewer prompts will:

- Direct readers to use `git show origin/master:<path>` exclusively
- Point at the new combined artifact: blueprint v2 (8bb0f9f) + amended
  supplement (new HEAD)
- Carry forward this directive's resolutions so reviewers don't
  re-litigate Q32-Q35
- Explicitly grep for `NotImplementedError`, `TODO`, `placeholder`
  markers (lesson from pass #2)

### STEP 5 — Reconciliation outcome

If pass #3 surfaces NEW CRITICAL MUSTs: re-cut supplement amendment
v3 (NOT in-place patch) addressing them. Repeat steps 2-4 until clean.

If pass #3 lands clean: orchestrator publishes a final ALL-CLEAR
directive that authorises code edits per the commit sequence.

### STEP 6 — Implementation begins

Per the commit sequence in the amended supplement. One MUST per
commit (or merged 4+5 if MUST #32 (b) chosen). Reviewer pass between
each commit. Stage 3.5 SHIP gate after all commits land + audits run.

═══════════════════════════════════════════════════════════════
SECTION F — DISCIPLINE RULES THAT REMAIN IN FORCE
═══════════════════════════════════════════════════════════════

1. **GitHub is project state.** All file reads via `git show
   origin/master:<path>`. Local files are drafts; not authoritative.
2. **Source re-verification AFTER drafting.** STEP 1 above is
   mandatory; reviewers in pass #2 caught source-staleness errors
   that grounding-before-drafting didn't catch.
3. **DECIDE and EXECUTE.** No options-back-to-orchestrator.
   Builder picks within ranges; documents reasoning; orchestrator
   approves at next gate.
4. **Quality default.** Slow/clean over fast/loose. Owner reaffirmed.
5. **Push back on unclear directives.** The answer to "is it OK to
   ask" is always YES. This directive is final but if any specific
   step has unclear scope, raise it before executing.

═══════════════════════════════════════════════════════════════
SECTION G — WHAT BUILDER DOES RIGHT NOW
═══════════════════════════════════════════════════════════════

Without further orchestrator input:

1. Execute STEP 1 (source re-verification, 5 sub-items)
2. Execute STEP 2 (cut amended supplement; address all 16 MUSTs +
   MUST #44 + Q32-Q35 resolutions; update commit sequence)
3. Execute STEP 3 (push)
4. Ping orchestrator: "amended supplement at <new-SHA>; ready for
   reconciliation pass #3"

Then wait for reconciliation pass #3 dispatch.

If during STEP 1 or STEP 2 a NEW source-level surprise is found
(e.g., the production labelling format diverges in a way that breaks
multiple MUSTs simultaneously): STOP and report. Don't push fix-it
commits in working flow.

═══════════════════════════════════════════════════════════════

End directive. Single source of next steps. Standing by for
"amended supplement pushed at <SHA>" ping.
