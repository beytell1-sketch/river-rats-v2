---
date: 2026-04-26
from: River Rats QC stream
to: Logic builder · Main terminal (orchestrator) · Owner (briefed)
re: PR #43 pre-merge QC audit — Build D (5-hand synthetic partial-fold MW fixtures for Phase A.5; closes V-X2 from QC PR #40); APPROVE (clean); all 9 vectors PASS; final pre-dispatch artifact
status: FLAG (advisory; pre-merge informational)
severity: APPROVE / V-X2 fully closed; no findings
PR head: 70bb66f9548c421c4dbc416a65192b1a7c4d02d7
full finding: ~/river-rats-qc/findings/2026-04-26-pr43-pre-merge-build-d.md
---

# QC Pre-Merge Audit — PR #43 (Build D)

## Headline

**APPROVE.** Build D cleanly closes QC V-X2 finding from PR #40 audit. 5 partial-fold MW fixtures with full diversity; 59-feature embedding (Build C v1.0.1 pattern); disjointness verified against 4 forbidden corpora (179 total fingerprints, 0 overlaps). SHA256 matches.

After merge: V-X2 closed; PRE-DISPATCH gate fully resolved; pilot dispatch resumes.

## Vector results

| Vector | Result | Note |
|--------|--------|------|
| V-D1 fixture count = 5 | ✅ PASS | exact 5 (`wc -l` confirmed) |
| V-D2 each fixture has fold in prior_actions | ✅ PASS | all 5 |
| V-D3 villain_positions = LIVE only | ✅ PASS | validator caught 2 bugs pre-commit (PF_002 + PF_005 BB-after-BB-fold) |
| V-D4 num_opponents matches len(villain_positions) | ✅ PASS | all 5 |
| V-D5 59-feature feat_dict | ✅ PASS | `jq '.feat_dict \| length' \| sort -u` = 59 |
| V-D6 synthetic generation provenance | ✅ PASS | sidecar build_directive + build_version + diversity_coverage |
| V-D7 SHA256 hash-lock | ✅ PASS | `c196fb...513` declared = computed |
| V-D8 TC-23 file existence | ✅ PASS | 3 files at canonical paths |
| V-X3 disjointness vs pilot 100 corpus | ✅ PASS | 0 overlap (179 forbidden fingerprints total) |

## Diversity coverage

- Streets: flop=2, turn=2, river=1
- Folded positions: 6 unique (BB, SB, CO, BTN, HJ, UTG — all 6 covered)
- Live villain count: 1 (1×), 2 (2×), 3 (2×)
- Pre-fold opp count evolution: 4→3 / 5→3→2 (multi-fold) / 4→2

## Phase A.5 usage

`_villain_pos_raw` intentionally NOT stored in fixture `feat_dict` — it's set at runtime by `feature_extractor.extract_all_features`. Phase A.5 assertion at runtime checks runtime-derived `_villain_pos_raw` is in fixture's `villain_positions` (live set). This is the HIGH-1 fix-surface verification per QC S-A12 close (sealed v1.0.3 PR #31).

## Multi-expert verdict

SOLO + concrete-finding-driven. Pre-emptive V-D vector design at tick 45 enabled fast audit (~6 min). Builder's validator pre-commit catches V-D3 class — convergence between QC vector design + builder validator = healthy team alignment.

## Recommendation

**APPROVE merge.** No findings. V-X2 fully closed.

After merge:
- PRE-DISPATCH PREREQUISITES gate fully resolved (rows #2/#3/#5/#6 all GREEN; V-X2 closed)
- Orchestrator re-issues pilot dispatch directive
- Pilot Orchestrator persona reactivates
- Phase A.1-A.7 preflight runs per spec
- QC resumes Layer 3 pilot-runtime watch per `QC_PILOT_RUNTIME_WATCH_2026-04-26.md`

## HALT recovery summary

Initial HALT at 16:42 SAST → all 4 RED rows GREEN + V-X2 closed at PR #43 audit time (~3-3.5h). Within orchestrator's ~2-2.5h estimate plus V-C13 fix-forward iteration. Sequence:

1. ✅ Build A (Protocol B labeller-facing) — sealed at PR #35 / 17:36 SAST
2. ✅ Build B (Protocol C labeller-facing) — sealed at PR #37 / 18:05 SAST
3. ✅ Build C v1.0 (pilot 100-hand corpus) — surfaced QC V-C13 + V-X2
4. ✅ Build C v1.0.1 (V-C13 fix-forward) — sealed at PR #41 / 19:01 SAST
5. ✅ Build D (V-X2 close — Phase A.5 fixtures) — APPROVE-pending-merge at PR #43

11 successive pre-merge audits completed (PR #21 through PR #43; bridging Tasks 4.5 through Build D).

## Process learning

- V-D vectors designed at tick 45 pre-emptive scoping; applied within 1 tick of Build D PR opening. Pre-emptive vector design enables fast audit on novel artifact classes.
- Builder's validator pre-commit catching V-D3 class (live-set integrity) shows close convergence between QC vector design + builder validator design.

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-pr43-pre-merge-build-d.md`
- PR #43: https://github.com/beytell1-sketch/river-rats-v2/pull/43
- V-X2 origin (QC PR #40): `~/river-rats-qc/findings/2026-04-26-pr39-pre-merge-build-c.md`
- Build D directive: `MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md` (`fa280d6`)
- Build C v1.0.1 pattern predecessor: `~/river-rats-qc/findings/2026-04-26-pr41-pre-merge-build-c-v1-0-1.md`

**Status: APPROVE. V-X2 closed. Final pre-dispatch artifact. After merge: pilot dispatch resumes.**
