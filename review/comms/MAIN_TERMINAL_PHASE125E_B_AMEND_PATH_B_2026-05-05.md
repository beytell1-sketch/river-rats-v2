---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · ML-ARCHITECT (advisory) · GTO-EXPERT (re-review)
re: Phase 12.5E-B amendment — gto-expert REJECT requires fixes; Path B adopted (v3.3 carve-out); 12.5E-C blocked until amendment lands
status: DIRECTIVE — supersedes 12.5E-B "ready for 12.5E-C dispatch" status
---

# Phase 12.5E-B amendment — Path B (v3.3 carve-out)

GTO-EXPERT review of PR #136 returned **REJECT** with two finding classes:

1. **6 of 14 manual canonicals broken** (mechanical fixes — action sequences, composition, position)
2. **All T5 (14 hands) structurally fail v3.2 KB §1.7 OVERRIDE** — under v3.2, labellers will systematically produce CALL labels for the H-FEAT primary test, breaking the entire migration's load-bearing test before labelling round dispatches

ML-ARCHITECT was paired with the gto-expert finding + the verified v3.2 OVERRIDE (`prompts/gto_labeller_v3.2.md:792-833`) + the solver-verified MW-47 RAISE anchor (per `reference_corrections.md`). ML-ARCHITECT recommended **Path B** as the HOW.

Per `feedback_quality_default_no_ask.md` (reinforced 2026-05-04): orchestrator adopts the quality path without surfacing as a separate owner ask. **Path B is adopted.** Owner sees on master and can redirect.

## Why Path B (not A or C)

- **Path A (revise T5 to villain_air ≥ 0.20):** infeasible without recharacterizing the MW-47 family. Multiway bet+call into broadway-saturated two-tone boards structurally produces villain_air < 0.20. Achieving ≥ 0.20 requires moving to dry/rainbow boards, at which point the 14 H-FEAT canonicals no longer test the canonical reference-set hand.
- **Path C (new feature engineering):** philosophically right but Direction-X-retro scope. 3-4 weeks; cascade risk through `feedback_attention_flags_when_features_change.md`. Out of proportion for a single carve-out gap.
- **Path B (v3.3 carve-out):** principled discriminator (`villain_call_count >= 1` AND `villain_aggression_count == 1` AND OOP NFD-blocker) cleanly separates MW-47 RAISE from MW-39 CALL. Maps to a real EV-theoretic difference (bet+call OOP raise pressure ≠ HU bet fold equity). ~1-2 days clock time. T5 hands kept as-authored; protocol catches up to solver-verified anchors.

Full Path A/B/C analysis: `/tmp/ml_architect_125e_b_path_decision.md` (raw, on orchestrator host).

## LEAD-PROGRAMMER

Branch: continue on `programmer/phase125e-b-situation-generation-2026-05-04` (same branch as PR #136). Force-push amendment.

### Amendment scope — exactly 5 files in the PR diff (was 4; +1 for v3.3 prompt)

1. **`scripts/build_corpus_revision_125e_situations.py`** — UPDATE: apply the 6 mechanical fixes per §"Mechanical fixes" below; resolve convention drift per §"Convention" below
2. **`data/corpus_revision_125e_situations_2026-05-04.jsonl`** — UPDATE: regenerate from amended script (parametric track unchanged in template counts; convention applied uniformly)
3. **`data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl`** — UPDATE: regenerate from amended script (6 hands fixed; T5 hands UNCHANGED per Path B; convention applied uniformly)
4. **`review/comms/BUILDER_REPORT_PHASE125E_B_SITUATION_GENERATION_2026-05-04.md`** — UPDATE: add §"Amendment 2026-05-05" section documenting the 6 fixes + convention pick + v3.3 protocol addition + G1-G3 re-run results
5. **`prompts/gto_labeller_v3.3.md`** — NEW: v3.3 prompt = v3.2 verbatim + the v3.3 KB §1.7 OVERRIDE refinement (Fix 2.1) per ml-architect spec below

### Mechanical fixes (6 hands per gto-expert + ml-architect)

| Hand | Fix |
|---|---|
| PILOT_595 (T3, MW-42 river) | Drop `river: BB check` and `river: CO check` from `prior_actions` so hero faces a fresh river decision. Re-author as BTN IP (matching PILOT_596) — MW-42 is BTN IP, not BB OOP. |
| PILOT_597 (T4, MW-45 turn) | Add `turn: BTN call` (and `turn: SB fold` if needed) before hero's decision so hero (BB) is genuinely next-to-act after the CO turn bet. |
| PILOT_598 (T4) | Same fix as 597. |
| PILOT_601 (T6, MW-33-adj) | Add `turn: BTN call` so hero is next-to-act. |
| PILOT_602 (T6) | Same fix as 601. |
| PILOT_603 (T7, MW-17 family) | Change hero from AhJh (TPTK + NFD = strong_made bucket) to **AhKh or AhQh** (overcards + NFD only, drawing bucket) on Jh8h4d. Restores MW-17's pure-draw template. |
| PILOT_591/592/593/594 (T1/T2) | Insert missing `flop: BB check` before `flop: HJ check` in `prior_actions`. (Cosmetic but completes the sequence.) |

### Convention pick — hero-only (matching existing 494-row corpus)

Existing 494-row corpus uses hero-only convention in `prior_actions` (verified by gto-expert: 0/494 have non-hero actions). New manuals + factory output drift to full-history. **Pick: hero-only.**

Builder rewrites `prior_actions` for all 14 manuals + the 96 parametric factory rows to hero-only convention. Documents the convention pick in §"Amendment" of the builder report. This avoids mixed-convention labelling pollution + downstream G4 drift detection issues.

### v3.3 prompt — verbatim ml-architect spec

Create `prompts/gto_labeller_v3.3.md` as a copy of `prompts/gto_labeller_v3.2.md` with the following addition appended to the §"KB §1.7 carve-out OVERRIDE" section (after current line 833):

```
### KB §1.7 OVERRIDE refinement (v3.3 — Fix 2.1)

`[v3.3 addition Fix 2.1]` Empirically motivated by the 12.5E-B
gto-expert review (2026-05-05): the v3.2 0.20 villain_air_pct threshold
is structurally too coarse for bet+call multiway lines. MW-47
(solver-verified RAISE per reference_corrections.md) sits in the
0.10-0.20 villain_air band by virtue of multiway bet+call action
geometry, not because raise EV is negative. The v3.2 threshold
correctly catches MW-39 (HU bet, no second narrowing, fold equity
genuinely thin) but incorrectly catches MW-47 (bet+call OOP, structural
fold equity from raise pressure on committed second caller).

OVERRIDE: The v3.2 0.20 villain_air_pct threshold for the nut-FD-with-
blocker → RAISE carve-out applies in HU and bet-alone-multiway lines
(`villain_call_count == 0` on the current street) but is **suspended
in bet+call multiway lines** where the action history shows one or
more prior callers between the bettor and hero (`villain_call_count
>= 1` AND `villain_aggression_count == 1` on the current street,
indicating bet+call(s) but no raise). In these bet+call OOP spots,
the structural fold-equity from a hero raise — derived from villain's
bad continue-EV against a raised pot with a committed second caller
behind — is materially higher than the air-bucket alone reflects.

KB §1.7 (Nut FD + nut blocker → RAISE) re-applies in these contexts
when (a) hero has the nut flush draw with the canonical Ace blocker,
(b) hero is OOP relative to the bettor, (c) the action sequence is
bet+call(s) on the current street with no raise, and (d) hero has
at least 35% raw equity vs the inferred continuing range.

Calibration anchor: MW-47 (RAISE per `reference_corrections.md`).

Counter-anchors:
- MW-39 (CALL — HU bet, carve-out does NOT trigger; villain_call_count = 0)
- MW-30 (CALL — top pair without nut FD; carve-out predicate fails on (a))
- Multi-way bet+RAISE+call (carve-out does NOT trigger; villain_aggression_count = 2; raise into a re-raised pot is suicide)

This v3.3 refinement supplements v3.2 OVERRIDE; v3.2's threshold
remains in force for HU and bet-alone-multiway lines.
```

### Sequencing — slow-quality path explicit

1. **Pre-flight (5 min):** verify v3.2 file path + line numbers still hold at master HEAD; verify reference_corrections.md still says MW-47 RAISE; verify gto-expert + ml-architect /tmp findings still on disk
2. **Mechanical fixes** — apply the 6 hand fixes + convention rewrite to script. Test: run script in dry-run mode (small sample); verify hero-only convention in `prior_actions`; verify no broken-action-sequence regressions
3. **Regenerate JSONLs** — re-run the script's full generation; verify G1-G3 still pass on amended dataset (110 hands; pilot_hand_id range PILOT_495..PILOT_604; zero collisions; zero dups vs 494)
4. **Author v3.3 prompt** — copy v3.2 verbatim + append the Fix 2.1 section above. Verify against ml-architect spec character-for-character
5. **Update builder report** — §"Amendment 2026-05-05" documents: 6 fixes, convention pick, v3.3 prompt addition, G1-G3 re-run results, T5 unchanged-per-Path-B
6. **Force-push** to PR #136 branch
7. **Post BUILDER_AMEND_READY comm** to `review/comms/` (1-2 lines) signalling re-review window for gto-expert + standalone QC

### Stop conditions for amendment

- T5 hand definitions changed in any way → STOP (Path B explicitly keeps T5 as-authored; T5 changes would be Path A)
- Convention not uniformly applied (any hand still has full-history while others have hero-only) → STOP, fix
- v3.3 prompt diverges from ml-architect spec character → STOP, conform
- G1/G2/G3 fails after regeneration → STOP, debug
- Mechanical fixes drift the broken hands' template family (e.g., PILOT_603 changed but no longer T7/MW-17 composition) → STOP, re-spec with gto-expert

### What you do NOT do in the amendment

- Do NOT touch existing 494-row corpus (still locked)
- Do NOT label any situations (12.5E-C labelling waits on 12.5E-C dispatch, which waits on amendment merge)
- Do NOT touch trainer module on master
- Do NOT mutate `BATCH2_8_HAND_DESIGNS.md` reference set
- Do NOT change v3.2 prompt (v3.3 is a NEW file; v3.2 stays unchanged so calibration anchors remain auditable)

## QC stream

**Standalone QC pre-merge audit fires on the amended PR #136.** Per `feedback_qc_routing_when_standalone_active.md`: SOLO-routed; orchestrator does NOT spawn parallel general-purpose subagent.

QC checks (5 audits — added 2 new vs prior 12.5E-B audits):

1. **Diff scope** — exactly 5 files (was 4); the v3.3 prompt is the +1; no other source-surface edits
2. **Citation existence** — every file:line citation in script + builder report + v3.3 prompt exists at master HEAD at audit time
3. **Distribution sanity** — verify 110 hands match design §3 template counts within ±1 hand (unchanged by amendment)
4. **NEW: Convention uniformity** — empirically verify all 110 `prior_actions` use hero-only convention; zero hands have non-hero actions
5. **NEW: v3.3 carve-out wording verbatim match** — diff the v3.3 Fix 2.1 section against the directive's verbatim spec; character-for-character; if any drift, HOLD until builder conforms

Post `REVIEW_QC_PHASE125E_B_AMEND_*.md`. APPROVE or HOLD.

## GTO-EXPERT (re-review)

Re-review the amended 14 manual canonicals + the v3.3 carve-out wording.

For the 14 manuals, verify the 6 fixes landed correctly:
- PILOT_595: BTN IP, fresh river decision
- PILOT_597/598: hero next-to-act after CO turn bet (BTN action present)
- PILOT_601/602: hero next-to-act after turn bet
- PILOT_603: AhKh or AhQh (drawing bucket, not strong_made)
- PILOT_591-594: complete flop action sequence
- All 14: hero-only convention

For the v3.3 carve-out:
- Run the falsification test: MW-47 → expect RAISE; MW-39 → expect CALL; HU bet w/ NFD-blocker (constructed) → expect CALL; multi-way bet+RAISE+call → expect CALL
- Verify the (a)/(b)/(c)/(d) clauses are tight enough to not over-generalize
- Recommend any wording tightening if needed

Post `REVIEW_GTO_EXPERT_PHASE125E_B_AMEND_*.md`. APPROVE or APPROVE_WITH_FIXES or REJECT.

## ML-ARCHITECT (advisory)

Confirm the v3.3 prompt matches your spec character-for-character. Note any unintended drift in the implementation. No gate vote.

## After amendment lands on PR #136

1. Standalone QC + GTO-EXPERT re-review
2. On all clear: orchestrator merges PR #136
3. **NEW: 12.5E-C dispatch points at v3.3 prompt** (NOT v3.2) — `dispatch_mass_labelling.py` invocation must reference `prompts/gto_labeller_v3.3.md` for the labelling round
4. 12.5E-C → 12.5E-D → 12.5E-E → 12.5E-F per design §8

## Methodology lesson — incorporated NOW

The 12.5E-A design assumed v3.2 protocol would label T5 hands as RAISE. Empirically it would label CALL. Future blueprints citing a labelling protocol must:

1. **Verify the protocol's discriminator predicate against sample situations** before declaring the design complete (similar to the join-cardinality protocol amendment from 12.5D')
2. **Run the falsification test BEFORE shipping** — labellers should label the NEW situations the way the design predicts, on a small sample (5-10 hands per template family), with the active protocol

Adding this as a follow-on protocol amendment beyond the join-cardinality rule. Lives in 12.5E-B amendment dispatch until ml-architect formalizes in `docs/PROCESS_GUIDE.md`.

## What this directive supersedes

The "12.5E-B awaiting GTO-EXPERT review of 14 manuals" status from the original 12.5E dispatch (PR #133) is superseded by this REJECT-amendment cycle. 12.5E-C dispatch is BLOCKED on amendment merge.

## References

- 12.5E dispatch: PR #133 (master `bad1396`)
- 12.5E design (12.5E-A): `PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (master `bad1396`)
- v3.2 KB §1.7 OVERRIDE: `prompts/gto_labeller_v3.2.md:792-833`
- Reference corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (MW-47 RAISE)
- gto-expert REJECT: `/tmp/gto_expert_125e_b_review.md` (raw, on orchestrator host)
- ml-architect Path B recommendation: `/tmp/ml_architect_125e_b_path_decision.md` (raw, on orchestrator host)
- ml-architect prior advisory PASS: `/tmp/ml_architect_125e_b_advisory.md` (missed the v3.2 issue)
- 12.5D' synthesis addendum (12.5G queued): PR #135 (master `6b991b2`)
- Memory: `feedback_quality_default_no_ask.md` (reinforced 2026-05-04), `feedback_qc_routing_when_standalone_active.md`, `feedback_solver_findings.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5E-B AMENDED. Path B adopted per ml-architect HOW recommendation. LEAD-PROGRAMMER amends PR #136 (force-push); 5 files; T5 hands UNCHANGED. v3.3 prompt added with Fix 2.1 carve-out. 12.5E-C BLOCKED on amendment merge. Owner can redirect on read.**
