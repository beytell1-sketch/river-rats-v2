---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT GTO reviewer (gto-expert subagent unavailable; persona spec embedded per builder dispatch; reviewer is NOT v1.0.1 author and NOT v1.0 reviewer)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #18 — Stage 6 held-out test set v1.0.1 (`3bbef9e`) fix-forward of v1.0
status: APPROVE-WITH-NITS — All 7 fix-forward items (2 HIGH + 4 MEDIUM + 1 LOW-MEDIUM) cleanly addressed; ONE NEW MEDIUM introduced (H025 header `105.2bb` ≠ body `94.2bb`) + cosmetic solver-sample tally drift in closure section. New MEDIUM is single-line cosmetic fix; substantive content sound.
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/18
branch: stage4-prep/stage6-holdout-fill-4-1
artifact: review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md (commits 3bbef9e + 8351b6f)
predecessor_pr: PR #16 verdict at `9758a99` (APPROVE-WITH-NITS, 2 HIGH + 4 MEDIUM)
predecessor_directive: `006a13e`
---

# Review Verdict — PR #18 (Stage 6 held-out test set v1.0.1 fix-forward)

## Provenance note

Independent reviewer dispatch under read-only constraint. Did NOT author v1.0 or v1.0.1; did NOT review v1.0 (different general-purpose subagent at `9758a99`). Worked from PR #18 head commit `3bbef9e`. Cross-referenced against `feedback_solver_aligned_sizing.md`, `calibration_situations.json`, training-data fingerprints, and full v1.0 → v1.0.1 diff.

## Builder verification spot-checks

- Hash recompute: `python3 -c "..."` matches `b775df2a1c2d53935f7094746063812c43f25ac21d3d1ba354c1908abc738539` over 47653 bytes ✓
- `grep -c "HASHED-BLOCK-START"` = 1; `grep -c "HASHED-BLOCK-END"` = 1 ✓
- All 5 calibration manifest files exist on disk ✓
- 0 fingerprint matches against 50 holdout hands ✓
- 50 hands have exactly 1 `^- Board` line each ✓

---

## Item A — HIGH #1 — Hash discipline

**OK / HIGH confidence.** Recomputed SHA256 matches recorded value byte-for-byte. Hash-resolution rule documented (lines 228-240). Python recompute snippet builds markers via concatenation so source itself produces only one literal hit. v1.0 hash preserved for traceability.

## Item B — HIGH #2 — Pot/SPR arithmetic

**MOSTLY OK with 1 NEW issue / HIGH confidence.**

Spot-checked 15+ hands:
- H022/H028/H048: turn-bet double-count fixed (5.5 + 3.3 + 13.2 = 22.0bb ✓)
- H039: river bet 7.5 → 6.6 (75% of 8.8) ✓
- H014: cascading 3-street redo correct (sizing-tag NIT only — author flagged)
- **H025: NEW ISSUE** — header says "Pot at decision: 105.2bb" but inline reframe correctly arrives at 94.2bb; pot odds 29.3% only validates against pot=94.2. Header inconsistent with body; FOLD conclusion unaffected.
- H031, H001, H005, H030, H017, H038, H046: all newly-FOLD hands have correct pot/odds figures ✓
- SB-dead-money convention prominently documented (lines 330-356) ✓

**HIGH #2 substantially fixed but introduces 1 new MEDIUM-severity arithmetic NIT (H025 header).**

## Item C — MEDIUM #1 — FOLD undersample

**OK / HIGH confidence.** FOLD count 10 ✓; BET count 13 ✓ (target). 6 newly-FOLD hands all verified poker-rigorous. Minor: H001 rationale has slight overstatement on "7-pairs in polar donk range" but FOLD conclusion is correct on dominated bluffcatcher logic.

## Item D — MEDIUM #2 — LOW band undersample

**OK / HIGH confidence.** LOW count 5 ✓ (target). All 5 LOW spots (H017/H024/H027/H038/H046) genuinely opinion-divided/boundary.

## Item E — MEDIUM #3 — Solver 10-sample swap

**OK with documentation NIT / HIGH confidence.** Sample = H002/007/013/019/024/028/032/043/046/049 ✓. H037 removed, H046 swapped in (FOLD class added). Spans all 5 action classes: 1 FOLD / 3 CHECK / 2 CALL / 3 BET / 1 RAISE; 5 HIGH / 3 MEDIUM / 2 LOW.

**NIT (documentation drift):** Self-consistency closure §6 + Concerns/Flags #12 contain stale band/action tallies that don't match the actual table. Substantive fix correct; closure tally cosmetic.

## Item F — MEDIUM #4 — Calibration manifest located

**OK / HIGH confidence.** All 5 files exist ✓. Independently re-ran fingerprint scan: 21 unique fingerprints, 0 matches against 50 holdout (matches author claim exactly). Prereq #5 cites manifest path.

## Item G — LOW-MEDIUM — JSONL-export blockers cleaned

**OK / HIGH confidence.** H007 single 3-card Board ✓; H016/019/045/047 no inline `Re-frame:` blocks ✓; H032 `Board: PREFLOP` placeholder ✓; `grep -c "Re-frame"` = 3 hits, all in changelog/closure prose (0 in hand specs); each of 50 hands has exactly 1 `^- Board` line.

## Item H — No new MEDIUMs introduced

**1 NEW MEDIUM + 1 NEW NIT / HIGH confidence.**

**NEW MEDIUM:** H025 pot header inconsistency. Header states "Pot at decision: 105.2bb" but inline reframe says "pot now = 44.2 + 50 = 94.2"; pot odds 29.3% only validates with pot=94.2. Fix: change header to `94.2bb`. FOLD conclusion unaffected. **Hash will need re-lock if H025 header changed (it's inside the hashed block).**

**NEW NITs:**
- Self-consistency closure §6 + Concerns #12: solver-sample band/action tallies stale (cosmetic; no pre-pilot decision impact)
- H001 rationale minor poker overstatement on "7-pairs in polar donk range"
- H027 rationale contains inline self-correction artifact

## Item I — Frontmatter changelog

**OK / HIGH confidence.** All elements verified.

## Item J — Diff scope

**OK / HIGH confidence.** 814-line diff (520 ins / 294 del) justified by 6 hand re-authorings + 30 arithmetic corrections + JSONL flattening + frontmatter changelog. No scope creep.

## Item K — Author concerns assessment

All 7 author concerns assessed:
1. Parallel-terminal turbulence — process-only, RESOLVED. NIT.
2. H014 sizing-tag relabeling — within ±5pts of label, acceptable. NIT.
3. H025 high-stakes recomputation — author flagged; my recompute confirms pot=94.2, FOLD unchanged. **MEDIUM for header bug, not math.**
4. H001/H005 board-card geometry — verified clean. NIT.
5. H027 LOW-band 3bet-pot — UNCERTAIN-SOLVER tag in place. NIT.
6. H039 river bet correction — verified, CALL unchanged. NIT (clean fix).
7. Solver-sample FOLD swap (H046 LOW) — defensible; reviewer notes a HIGH-band FOLD (H001 or H030) would give cleaner signal. NIT.

## Item L — Ready for orchestrator merge?

**APPROVE-WITH-NITS.**

Fix-forward addresses all 2 HIGH + 4 MEDIUM + 1 LOW-MEDIUM items from PR #16 cleanly. Hash discipline verified by independent recomputation (exact match). Pot/SPR convention documented + arithmetic corrected. FOLD/LOW undersamples fixed. Solver-sample FOLD coverage. Calibration manifest non-overlap empirically verified.

**One NEW MEDIUM finding** (H025 header `105.2bb` should be `94.2bb`) introduced by v1.0.1 redo. Cosmetic header-vs-body inconsistency; underlying pot-odds calc + FOLD action correct.

**Recommended path:** APPROVE-WITH-NITS for merge as canonical v1.0.1, with H025 header fix + solver-sample tally cleanup deferred to single-touch v1.0.2 micro-correction. Hash will need re-lock if H025 header changed.

If orchestrator prefers HIGH-severity discipline (no header inconsistencies inside hashed block): REQUEST-CHANGES for one-line H025 fix + solver-sample tally cleanup, then approve.

---

## VERDICT

**APPROVE-WITH-NITS — overall confidence HIGH.**

Single new MEDIUM is narrow-scope and cosmetic; substantive fix is sound.

**Required fixes for design-artifact ship:** None (cosmetic only).
**Required fixes for pilot evaluation use:** H025 header fix + hash re-lock (v1.0.2 micro-correction).
**Blockers:** None for design-artifact merge.

## NIT-level observations

1. H025 header `105.2bb` → `94.2bb` (MEDIUM-cosmetic, hash re-lock required)
2. Self-consistency closure §6 + Concerns #12 solver-sample tallies stale (NIT)
3. H001 rationale minor poker overstatement (NIT)
4. H027 rationale inline self-correction artifact (NIT)
5. H014 sizing-tag at ±5pts (within tolerance, NIT)
6. Solver-sample FOLD is LOW-band; HIGH-band FOLD would give cleaner signal (NIT)

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | MEDIUM (cosmetic) | H025 header `105.2bb` → `94.2bb` + hash re-lock (v1.0.2 micro-correction) |
| 2 | NIT | Self-consistency closure §6 + Concerns #12 solver-sample tally cleanup |
| 3 | NIT | H001 rationale "7-pairs in polar donk" wording |
| 4 | NIT | H027 inline self-correction cleanup |
| 5 | NIT | Consider HIGH-band FOLD addition to solver 10-sample (H001 or H030) |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_18_STAGE6_HOLDOUT_V1_0_1_2026-04-26.md`.
2. Post comment on PR #18 referencing the verdict.
3. Stand by for orchestrator merge / v1.0.2 fix-forward direction.

**Orchestrator:**
1. Read this verdict.
2. Decide: (a) merge PR #18 as v1.0.1 + open Task 4.2 micro-fix for H025 header + hash re-lock; OR (b) BLOCK PR #18 until v1.0.2 micro-fix lands. PR #11/#13/#15 precedents went fix-forward path.
3. Either way: H025 header fix is required before pilot evaluation use.

**Owner:** wake to find Stage 6 held-out v1.0.1 substantively complete; one cosmetic micro-fix needed before pilot use.

## Reference

- PR #18: https://github.com/beytell1-sketch/river-rats-v2/pull/18
- v1.0.1 commits: `3bbef9e` + `8351b6f` (PROCEED comm restore)
- v1.0 commit: `30ec324`
- v1.0 verdict: `9758a99` (APPROVE-WITH-NITS)
- Orchestrator directive: `006a13e`
- Source artifact: `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md`
- Calibration manifest: `review/calibration_situations.json` + 4 mirrors
- Tasks 1.1 / 2.1 / 3.1 fix-forward precedents: PR #11, #13, #15

**FINAL VERDICT: APPROVE-WITH-NITS — HIGH confidence overall. Recommend v1.0.2 micro-fix for H025 header + hash re-lock before pilot evaluation use.**
