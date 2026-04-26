---
date: 2026-04-26
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable; persona spec embedded per builder dispatch)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #11 — Stage 4 Protocol B v1.0.1 fix-forward (`7b0d7d1`)
status: APPROVE — all 3 MEDIUMs + 2 NITs from PR #10 verdict addressed cleanly; one new LOW concern surfaced (MW-30 rule restatement); no new MEDIUMs introduced; ready for orchestrator merge as canonical Protocol B v1.0.1
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/11
branch: stage4-prep/protocol-b-fill-1-1
artifact: prompts/protocol_b_composition_first_v1_0.md (1229 lines, +238/-77 vs v1.0)
predecessor: stage4-prep/protocol-b-fill (v1.0, 1068 lines, PR #10)
---

# Review Verdict — PR #11 (Stage 4 Protocol B v1.0.1 fix-forward)

## Provenance note

Independent reviewer dispatch (different general-purpose subagent than v1.0.1 author and v1.0 reviewer). Read-only review per builder dispatch. Verdict returned via message body; builder writes the comms doc. All file reads at `7b0d7d1` HEAD of `stage4-prep/protocol-b-fill-1-1`. Diff command: `git diff stage4-prep/protocol-b-fill..stage4-prep/protocol-b-fill-1-1` (411 lines, 238 ins / 77 del). v1.0 → v1.0.1 surgical-delta only.

## Builder verification spot-checks

- Arithmetic verified by direct `python3 -c`: pot odds 30/(30+90) = **0.25** ✓; surplus 0.40 - 0.25 = **0.15** ✓; beatable slice 0.24 + 0.20 + 0.15 = **0.59** ✓; total composition sums to 1.00 ✓
- Example 1 100bb math: SBfold + BB1 + CO3 + BTN3 + BB+2 = 9.5bb pot ✓; stacks 100 - 3 = 97bb behind ✓; SPR = 97/9.5 = **10.21** ✓ (matches "SPR ≈ 10 deep" in body); 33% bet = ~3bb into 9.5bb ✓
- "wait... actually" search: zero hits in body (only in changelog describing the fix)
- "per village" search: zero hits in body (only in changelog)
- Stale 0.18 / 0.22 pot-odds: zero hits in body — all numbers consistent across Step 2/3/4/override/Trace of Example 2

All spot-checks hold.

---

## Item A — MEDIUM #1: Example 1 internal consistency

**OK / HIGH confidence.** Re-authored from scratch with internally-consistent 100bb math. Preflop sequence verified arithmetically. SPR ≈ 10 explicit and matches arithmetic. Editorial drift fully stripped. Board changed from `Jd 9d 3h | 6d` (flush-completing) to `Jd 9c 3h | 6s` (rainbow) — a poker-judgment-driven choice that removes the flush-draw ambiguity that triggered the original drift. Action conclusion (BET small for thin value) follows cleanly from the stated composition.

Minor: equity 0.58 for KJ on the new board vs the stated composition is plausible but author-flagged as estimate-grade (UNCERTAIN caveat preserved).

## Item B — MEDIUM #2: Anti-pattern #7 carve-out

**OK / HIGH confidence.** Option (a) carve-out implemented per orchestrator recommendation. Three components verified:
1. Allowed example: composition-derived equity with explicit slice-summation
2. Forbidden example: pre-computed `equity_vs_range` feature read
3. Grading rule: "in Step 3, citing pot-odds / equity surplus is OK iff the equity number is explicitly derived from the composition slices in the same trace"

Example 2 Step 3 explicitly frames equity 0.40 as composition-derived (sum of beatable slices: 0.24 + 0.20 + 0.15 = 0.59). Arithmetic corrections applied throughout (Step 2, Step 3, Step 4, override justification, Trace) — all five places consistent. No orphan 0.18 / 0.22 residue.

**LOW concern (new — see Item F):** The MW-30 anchor rule was restated from numerical-threshold form ("surplus > 0.15") to structural form ("positive surplus AND beatable-slice > losing-slice"). New rule is more general (threshold-free, harder to cargo-cult) and arguably better-aligned with composition-first ethos, but it's a content shift beyond strict arithmetic-correction scope. Author should have flagged in concerns. Same action conclusion (CALL); rule is philosophically better.

## Item C — MEDIUM #3: Verbatim-inlining for pilot build

**OK / HIGH confidence.** New "PRE-PILOT BUILD REQUIREMENT" section at top of file (lines 79-115) explicitly:
- Names 3 v3.1 sections to inline: Bucket taxonomy (170-204), Features (439-496), DO NOT Rules (595-647)
- Specifies output artifact: `prompts/protocol_b_composition_first_v1_0_pilot.md`
- Documents failure mode: "labeller agent chases v3.1 references mid-labelling, drifts away, OR operates on stale v3.1 content"
- Marks ownership: owner-gated build pipeline step at pilot-dispatch time

Placement is correct (immediately after title, before protocol content). Bold "DESIGN ARTIFACT, NOT LABELLER-FACING PROMPT" lead-in is appropriate emphasis.

## Item D — NIT bundle

**OK / HIGH confidence.** "per village" → "per villain" verified at line 647 (via Example 1 re-author; only in changelog now). Threshold row "≥0.40 medium" softened at line 232 + parallel softening at lines 210-214 (Equity-vs-range axis). Both correctly distinguish weak/medium-hero (pot control) from strong-made-hero (thin value) regimes; cross-reference Example 1.

## Item E — Frontmatter changelog

**OK / HIGH confidence.** All required elements verified:
- `version: v1.0.1` ✓
- `status: v1.0.1 (APPROVE-WITH-NITS fix-forward on v1.0)` ✓
- `review_chain` updated with `aa1c2f7` and v1.0.1 step ✓
- `changelog.v1.0.1` block lists all 3 MEDIUMs + 2 NITs explicitly with fix descriptions ✓
- References both verdict (`aa1c2f7`) and orchestrator directive (`099c9de`) ✓
- `out_of_scope_for_v1_0_1` block names what was deferred (solver verification, anti-pattern #11, 4B-rate floor, _pilot.md build) ✓

The frontmatter changelog captures reasoning per fix, not just the fix itself — good discipline for a review-chain artifact.

## Item F — No new MEDIUM-severity issues introduced

**OK with one LOW concern / MEDIUM-HIGH confidence.**

Cross-references verified intact:
- Threshold table line 231 still cites `d2410_CO_turn` calibration anchor; new Example 1 has identical composition pcts (0.30 / 0.32 / 0.16 / 0.22), so threshold-provenance citation aligns
- Anti-pattern #7 carve-out does NOT contradict any other anti-pattern (#1 retrofitting, #4 cargo-culting target distinct failure modes)
- PRE-PILOT BUILD REQUIREMENT does NOT conflict with later inheritance-by-reference paragraphs — it's a meta-instruction ABOUT them
- Equity-vs-range axis softening at lines 204-214 internally consistent with threshold table softening at line 232

**LOW concern (new):** Example 2's MW-30 anchor rule restated from numerical-threshold to structural form (see Item B). Content shift beyond stated scope; better rule philosophically; same action conclusion. Author should have flagged. Not blocking.

## Item G — Diff scope

**OK / MEDIUM-HIGH confidence.** Diff 411 lines (238/-77) exceeds author's <200 surgical target by ~2x. Component breakdown:
- Frontmatter changelog: ~50 lines (necessary per orchestrator request)
- PRE-PILOT BUILD REQUIREMENT: ~40 lines (necessary for MEDIUM #3)
- Example 1 full re-author: ~65 lines (necessary for MEDIUM #1; surgical patch wasn't viable due to intertwined issues)
- Example 2 rewrites: ~30 lines (necessary for MEDIUM #2 + arithmetic)
- Anti-pattern #7 carve-out: ~30 lines (necessary for MEDIUM #2)
- Threshold + axis softenings: ~10 lines (necessary for NIT)

Total content ≈ 225 lines; with diff-context overhead, 411 plausible. **No gold-plating.** Every component traces to one of the 3 MEDIUMs or 2 NITs.

Author's full Example 1 re-author was correct judgment — patching the original board for internal consistency would have either required ~180bb stack depth (non-canonical) or kept the flush-completing turn (re-introducing drift trigger).

## Item H — Author concerns assessment

**All four concerns are acceptable next-steps; none escalate to MEDIUM.**

1. Diff size 411 vs <200: justified per Item G
2. Example 1 medium=0.32 below 0.40 threshold: honest framing in body; v1.1 could add 6th example
3. Example 2 unit framing (chip vs bb): parenthetical adequate
4. Carve-out grading rule shifts judgment burden: see Item I — graderable; v1.1 calibration exam should include edge case

## Item I — Carve-out grading rule workability

**Graderable / MEDIUM-HIGH confidence.** Walking two hypothetical traces:

**Composition-derived equity trace (allowed):**
> "Hero TT beats medium 0.18 + draws 0.20 + air 0.22 = 0.60 of villain's range, equity ~0.42 derived from beatable-slice mass. Pot_odds 0.25, surplus 0.17 — CALL."
> Grader check: equity (0.42) explicitly derived from cited slices. Carve-out applies → STRONG.

**Pre-computed equity trace (forbidden):**
> "Hero TT, equity_vs_range = 0.43 per feature read. Pot_odds 0.25, surplus 0.18 — CALL."
> Grader check: equity (0.43) cited as feature read with no slice derivation. Carve-out does NOT apply → FAIL on Anti-pattern #7.

Distinction IS graderable: grader checks whether equity number in Step 3 is paired with explicit "Hero beats slice X + slice Y + slice Z = N" derivation in same trace.

**Edge case:** A trace citing BOTH slice-sum derivation AND `equity_vs_range` feature read — grading rule on line 1056-1061 forbids feature citation regardless. Workable; v1.1 calibration exam should include this exact edge case.

## Item J — Ready for orchestrator merge?

**APPROVE — ready for merge as canonical Protocol B v1.0.1.**

All 3 MEDIUMs cleanly addressed; both NITs bundled correctly; frontmatter changelog thorough and provenance-linked. One LOW-severity new concern (MW-30 rule restatement) — does not block.

**Recommended disposition per orchestrator's options: close PR #10 + merge PR #11 as canonical v1.0.1.** Produces clean master history (one commit lands v1.0.1) and avoids transient v1.0 with known issues.

---

## VERDICT

**APPROVE — overall confidence HIGH.**

**Required fixes:** None.
**Blockers:** None.

## NIT-level observations (non-blocking)

1. MW-30 anchor rule restated from numerical → structural — content change beyond stated scope; new rule is better; author should have flagged. (LOW)
2. Example 1 medium=0.32 below 0.40 heavy-medium threshold; v1.1 could add 6th example at medium ≥ 0.40. (NIT)
3. PRE-PILOT BUILD REQUIREMENT title says "v1.0.1 addition" — accurate for the section itself but the inheritance-by-reference paragraphs it references existed unchanged in v1.0. (NIT)
4. Carve-out grading edge case (slice-sum + feature-read in same trace) — v1.1 calibration exam should include. (NIT)

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | LOW | Note in v1.1 review chain that MW-30 rule was restated structurally in v1.0.1 |
| 2 | NIT | v1.1 calibration exam to include carve-out edge case |
| 3 | NIT | v1.1 to add 6th example at medium ≥ 0.40 |
| 4 | NIT | v1.1 to consider 4B-rate floor as Task 5 pilot design parameter (deferred) |
| 5 | NIT | v1.1 to consider Anti-pattern #11 (action-history-blindness) (deferred) |
| 6 | NIT | Solver-verify 0.35 TP+ and 0.40 medium thresholds before pilot dispatch (deferred) |
| 7 | NIT | Build `prompts/protocol_b_composition_first_v1_0_pilot.md` with v3.1 sections inlined (owner-gated build step at pilot dispatch) |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_11_PROTOCOL_B_V1_0_1_2026-04-26.md`.
2. Post comment on PR #11 referencing the verdict.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check.
3. **Recommended:** close PR #10 + merge PR #11 as canonical v1.0.1.
   `gh pr close 10 --comment "Superseded by PR #11 (v1.0.1 fix-forward)"` then `gh pr merge 11 --merge --delete-branch`.
4. After merge: builder may proceed to Task 2 (Protocol C).

**Owner:** wake to find Protocol B v1.0.1 design artifact landed on master with all reviewer-flagged MEDIUMs addressed. Pre-pilot polish items remain owner-gated next-steps.

## Reference

- PR #11: https://github.com/beytell1-sketch/river-rats-v2/pull/11
- v1.0.1 commit: `7b0d7d1`
- v1.0 commit: `25fc24a` (PR #10)
- v1.0 verdict: `aa1c2f7`
- Orchestrator directive: `099c9de`
- Source artifact: `prompts/protocol_b_composition_first_v1_0.md`
- gto-expert persona: `~/river-rats-v2/.claude/agents/gto-expert.md`

**FINAL VERDICT: APPROVE — HIGH confidence overall. Ready for orchestrator merge as canonical Protocol B v1.0.1. Recommended disposition: close PR #10 + merge PR #11.**
