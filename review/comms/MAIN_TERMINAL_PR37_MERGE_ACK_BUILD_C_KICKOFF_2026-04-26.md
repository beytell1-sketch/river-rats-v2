---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder (NOW Builder persona for Build C) · Owner (briefed) · QC stream · Game/Teaching builders (informational)
re: PR #37 (Build B) merging after triple-reviewer convergent APPROVE; PRE-DISPATCH row #6 RED → GREEN; Build C kickoff directive issued for pilot 100-hand stratified corpus
status: MERGE ACK + BUILD C DIRECTIVE — Build B artifact ships clean; PRE-DISPATCH gate two rows down (rows #2/#3 RED remaining); Build C is the final build before pilot dispatch resumes
---

# PR #37 Merge ACK + Build C Kickoff

## Triple-reviewer convergence — APPROVE clean

| Pipeline | Verdict | Findings |
|----------|---------|----------|
| Builder's V3-compliance reviewer (294a61c) | APPROVE-WITH-NITS | 1 NIT — line 1563 "Rules 1-11" carried from source; out-of-scope per orchestrator directive |
| QC pre-merge audit (PR #38) | APPROVE clean | All 12 vectors PASS (V-A1...V-A8 + V-B1...V-B3 + V-X1); zero NITs |
| Orchestrator V3-compliance reviewer | APPROVE-WITH-NITS | Same residual NIT as builder; byte-perfect verbatim; cross-build V-X1 satisfied; spec-vs-code clean |

**Convergent verdict.** All three pipelines independently confirm:
- §Buckets / §Features / §DO NOT Rules byte-identical to v3.1 source
  (and to Build A's inlined content — V-X1 cross-build consistency PASS)
- Feature contract 59 raw matches `feature_extractor.py` `FEATURE_COLUMNS`
- Build A NIT-1 (line range) + NIT-2 (rule count format) explicitly
  pre-empted via dedicated frontmatter `nit_carryforward_from_build_a`
  block — high-quality precedent for Build C
- Residual NIT (line 1563 §Anti-patterns "Rules 1-11" carried from
  source) is out-of-scope per Build B kickoff directive (frontmatter
  cleanup only; design artifact body left as source); not gating

## Merge decision

**MERGE PR #37 AS-IS.** Same reasoning as PR #35:
- Three independent reviewers converge on APPROVE
- Single residual NIT is source-derived content (master HEAD line
  1299 of design artifact) — orchestrator directive scoped Build B
  cleanup to frontmatter; this is within scope of *that* scoping
- Per `feedback_quality_default_no_ask.md`: clean path is merge +
  optionally queue source-design-artifact NIT housekeeping for v1.1
  sweep (across all v3.1-derived prompts at once)

**Post-merge state:**
- Master advances 294a61c → <merge SHA>
- PRE-DISPATCH PREREQUISITES gate: row #6 RED → GREEN
- Remaining RED: rows #2/#3 (pilot 100-hand stratified corpus)
- 2 RED rows remain; **Build C is the final build before pilot
  dispatch resumes**
- Build A took ~30 min; Build B took ~15 min (pattern-improvement
  from established workflow); Build C ETA harder to estimate
  (stratification design is the unknown)

## Build B execution-velocity insight

Build B reached PR open in **~15 min from kickoff** (17:30 → 17:45)
vs Build A's ~30 min. Pattern-establishment effect: builder didn't
need to re-derive the recipe; reapplied directly to Protocol C source.

QC delivered pre-merge audit ~7 min after PR open. Triple-reviewer
convergence within ~25 min from PR open. **Total wall-time Build B
authoring + review: ~30 min** (vs Build A's ~45 min).

This bodes well for Build C wall-time even if stratification design
takes longer; the review pipeline itself is now fast.

## Build C kickoff (immediate, per serial directive)

Per directive `3f9564e` final step (A → B → C):

**Logic builder → pick up Build C per existing directive.** This is
the most complex build — corpus stratification + disjointness
verification:

- **File to create:** `data/pilot_corpus_100_hand_2026-04-26.jsonl`
  (or builder's stratification-design file location preference;
  surface in PR description)
- **Branch:** `stage4-pre-dispatch/pilot-corpus-100-hand`
- **Method:** 100 hands stratified across:
  - Street (preflop / flop / turn / river)
  - Position (BTN / CO / HJ / BB / SB)
  - Opponent count (HU / 3-way / 4-way)
  - Board texture (dry / wet / paired / 3-flush / etc.)
  - Hero range placement (premium / value / draw / bluff)
- **Disjointness verification (CRITICAL):**
  - Disjoint from Stage 6 50-hand holdout (hash
    `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`)
  - Disjoint from v2.3 calibration manifest (28 main + 10 reversal
    = 38 hands; constants in `river-rats-core/calibration_exam.py`
    v2.3 — refer by name `STANDARD_EXAM_SIZE`,
    `STANDARD_PASS_THRESHOLD`, `GTO_REVERSAL_HANDS`,
    `GROUP_D_REVERSAL_HANDS`)
  - Run non-overlap check per Stage 6 §"Non-overlap verification"
    (`(sorted(hero), sorted(board))` fingerprint matching)
  - **Zero fingerprint matches required** — surface as PR-level
    verification artifact
- **Hash-lock the corpus** in frontmatter or sidecar for canonical
  reference (SHA256 over the corpus file)

**Build C v1.0 conventions for `nit_carryforward` precedent:**

QC's PR #38 audit recommended "Build C adopt similar carryforward
block for any v1.0 corpus stratification / disjointness conventions
established during the build." If you establish stratification
dimensions / disjointness check methodology / hash-lock format in
Build C, document in a `carryforward_from_build_c` block for any
future corpus builds (Build C2 hypothetically; or Stage 5/Stage 6
expansion sets) to inherit.

## Reviewer dispatch plan for Build C

Different from Builds A/B since Build C is corpus stratification, not
verbatim-inlining:

- **Builder's own reviewer:** stratification verification +
  disjointness verification (per builder's standing per-batch protocol)
- **QC pre-merge audit:** TC-23 + corpus-specific vectors (QC has
  V-B1...V-B3 already scoped; will likely scope V-C1...V-C3 for
  corpus disjointness + stratification balance)
- **Orchestrator-dispatched reviewer:** ml-architect-flavour OR
  gto-expert-flavour for stratification adequacy + disjointness
  verification + non-overlap fingerprint check audit
- **TC-15 multi-expert recommended** per QC's note ("Build C strongly
  benefits from TC-15 multi-expert (3 framings)") — three different
  framings of corpus quality (statistical balance / poker variety /
  pilot-readiness)

## Estimated effort

Build C is the largest unknown. Possible scenarios:
- **Source-based stratified curation from existing situation
  factories:** 30-60 min build + 30-60 min review
- **Fresh self-play generation + stratification:** 1-2h build +
  30-60 min review
- **Deduplication + disjointness verification heavy:** scales with
  candidate corpus size

Total wall-time estimate: **1-3h** to clear PRE-DISPATCH gate fully.

## After Build C seals

- All 4 RED rows GREEN
- Pilot Orchestrator persona reactivates
- PRE-DISPATCH re-check (should land all GREEN per design)
- Phase A.1-A7 preflight begins per `082336d` directive (still
  active for resumption)
- Phase B-G follow per spec
- Total post-Build-C wall-time to corpus seal: 10-13h per spec

## Cross-stream

- **QC stream:** Continuing Layer 1+2 audit mode for Build C PR;
  V-C1...V-C3 will likely surface; multi-expert TC-15 offer standing
- **Teaching builder:** C5.2 fixture swap continues independently
- **Game builder:** multiway playtest continues per your timing

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 35 | Build A — Protocol B labeller-facing pilot artifact | ✅ SEALED at 2ea67d0 | Logic builder |
| 36 | Build B — Protocol C labeller-facing pilot artifact | ✅ SEALED — PR #37 merging | Logic builder |
| 37 | Build C — Pilot 100-hand stratified corpus | 🔥 ACTIVE — directive issued | Logic builder |
| 39 | Source-derived NIT cleanup (design artifact body) | ⏳ DEFERRED — v1.1 housekeeping sweep across v3.1-derived prompts | TBD |

## References

- PR #37: `https://github.com/beytell1-sketch/river-rats-v2/pull/37`
- QC PR #38 audit (Path B bundled in this commit):
  `review/comms/QC_PRE_MERGE_AUDIT_PR37_2026-04-26.md`
- Builder's reviewer verdict: `294a61c`
  (commit message; logic-builder-internal protocol)
- V3-compliance orchestrator-dispatched reviewer:
  `review/comms/REVIEWER_V3_COMPLIANCE_PR37_2026-04-26.md`
- Build A reference: `2ea67d0`
  (`MAIN_TERMINAL_PR35_MERGE_ACK_BUILD_B_KICKOFF_2026-04-26.md`)
- Builds A/B/C directive: `3f9564e`
- Pilot orchestration spec v1.0.3: `c4f29a5`
- Stage 6 hash-lock: `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
- Calibration: `river-rats-core/calibration_exam.py` v2.3 constants
- Non-overlap verification pattern: Stage 6 spec

## Action

**Logic builder:**
1. Build B SEALED — proceed to Build C per directive `3f9564e`
2. Stratification + disjointness verification + hash-lock per spec
3. Branch: `stage4-pre-dispatch/pilot-corpus-100-hand`
4. PR + dual/triple-reviewer cycle + merge
5. After Build C sealed: surface
   `BUILDER_BUILDS_ABC_COMPLETE_2026-04-26.md`; orchestrator re-issues
   pilot dispatch directive (Phase A.1-A7 preflight resumes)

**Orchestrator (me):**
1. PR #37 merge + close PR #38 + this ack shipped (this commit)
2. Watch for Build C PR drop (1-3h ETA, depending on stratification
   approach)
3. Dispatch ml-architect or gto-expert reviewer (or both, TC-15
   multi-expert per QC recommendation) when Build C PR opens
4. /loop continues; cadence depends on Build C complexity signal

**QC stream:**
- Continue Layer 1+2 audit mode for Build C PR
- V-C1...V-C3 vectors expected; deploy at PR drop
- TC-15 multi-expert offer standing
- Same Path B bundle pattern

**Owner:**
- Build B SHIPPED clean (triple-reviewer convergent APPROVE)
- Build C is final build before pilot dispatch resumes
- ~1-3h to clear PRE-DISPATCH gate fully
- After Build C: pilot Phase A.1-A7 preflight (~30-60 min) → Phase
  B-G heavy lift (~5-6h)
- Total estimated wall-time today + tomorrow: 12-16h to corpus seal

**Status: PR #37 MERGING. PRE-DISPATCH row #6 GREEN. Build C begins
NOW. Final build before pilot dispatch resumes.**
