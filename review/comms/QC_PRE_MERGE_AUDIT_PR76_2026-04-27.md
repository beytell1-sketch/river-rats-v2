---
date: 2026-04-27
from: River Rats QC stream
to: Architect (logic-domain) · Main terminal (orchestrator) · ml-architect reviewer · gto-expert reviewer · Owner (briefed)
re: PR #76 pre-merge QC audit — Architect Phase 2.7 blueprint v3.5 (scenario module expansion: 146 templates / 6 modules); APPROVE (clean); V-Synthesis-Correction first application validates architect's directive correction
severity: APPROVE clean
status: FLAG (advisory; pre-merge informational)
---

# QC Pre-Merge Audit — PR #76 (Blueprint v3.5)

## Headline

**APPROVE clean.** All vectors PASS. 146 new scenario templates across 6 modules; sums verified. Architect's "overlap-math correction" of Phase 5 directive is sound and verifiable against master (F5 allocator is single-category-assignment).

## Vector results

| Vector | Result |
|--------|--------|
| V-X1 file existence (8 cited modules) | ✅ PASS |
| V-X4 carryforward to Phase 5 directive | ✅ PASS (yield gaps match F5 empirical run) |
| V-Source-2: F5 single-cat-assignment claim | ✅ PASS (verified at build_corpus_revision_500_hand.py:393, 454) |
| V-Synthesis-1: per-module sum = 146 | ✅ PASS (52+34+32+11+10+7=146) |
| **V-Synthesis-Correction (NEW)** | ✅ PASS — first application |
| V-OQ-Resolution: explicit risk flagged | ✅ PASS (Module 5 donk allocator risk noted) |

## Per-module verification (146 total)

| Module | Expansion | Yield gap fix |
|--------|-----------|---------------|
| Module 1: magg | +52 (30 quota + 22 spr_med overflow) | magg 10→40 + spr_med 18→40 |
| Module 2: pfa | +34 | pfa 46→80 |
| Module 3: nfd | +32 (raise+call) | nfd_raise 4→20 + nfd_call 4→20 |
| Module 4: bac | +11 | bac 9→20 |
| Module 5: donk | +10 | donk 15→25 (allocator risk flagged) |
| Module 6: sb | +7 | sb 13→20 |
| **Total** | **+146** | |

monster, facing_initial_bet, nfd_boundary, rule11, spr_std: not expanded (already at quota / acceptable yield).

## V-Synthesis-Correction (NEW, first application)

The architect explicitly **corrects** Phase 5 directive's claim "80-120 records via overlap" to honest minimum 146. The correction is sound:
- Phase 5 directive claimed multi-category overlap could yield 80-120 records via dual-quota satisfaction
- Architect correctly notes F5 allocator is **single-category-assignment** ("highest-scarcity category that still has unfilled target")
- Verified at `scripts/build_corpus_revision_500_hand.py:393, 454`

QC concurs: the correction is sound; the new claim (146 honest minimum) is sound; multi-cat membership only helps via scarcity-ranked redirect, not dual-quota fill.

**V-Synthesis-Correction subclass added to TC-24**: when architect blueprint corrects upstream directive, QC verifies (a) upstream-claim-error and (b) corrected-claim-validity. PR #76's overlap-math correction is canonical first application.

## Architecture design quality

The blueprint demonstrates strong discipline:
1. Critical-preamble section addresses the directive correction transparently
2. Scarcity table from F5 empirical run
3. SPR math reference with explicit pot ranges per SPR bucket
4. Per-module structure: state → expansion → rationale → templates → action history → expected feat_dict → bug-awareness checklist
5. Cross-module overlap table makes inter-module assignment dynamics explicit
6. Verification spec for Phase 6 acceptance criteria
7. Module 5 donk allocator risk flagged ("6 donk+pfa templates may all go to pfa") — V-Allocator-Multi-Dim awareness baked in

## Findings

- **HIGH/MEDIUM/LOW/NIT:** none

## Recommendations

### To Round 5 reviewers (gto-expert + ml-architect)
**APPROVE merge.** No QC findings.

### To gto-expert (Round 5 poker realism review)
Verify 146 templates are realistic poker scenarios. Pay attention to MAGG Group B (pot 26-45 BB SPR 2.22-3.85) — these are the overflow-to-spr_med records.

### To ml-architect (Round 5 feature contract review)
Verify 146 templates each satisfy `_classify_record` correctly. Module 5 donk: validate 4 donk-only templates are sufficient given 6 donk+pfa allocator risk.

### Post-merge sequence
1. Round 5 reviews + synthesis
2. PR #76 merges (or fix-forward)
3. Round 6 builder PR: implements 146 templates
4. Round 7 review on builder PR (paired V-Implementation-Spec-Match + V-Integration-Trace + V-Allocator-Multi-Dim)
5. Builder re-runs E2-B → re-pool → re-C2 → updates data PR
6. Final round on data PR

## Reference

- PR #76 head: `6872e7b166f6008c77508e7e0a824349f794f459`
- Master HEAD: `2b0ceff`
- Phase 5 directive (corrected): `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_PHASE5_DIRECTIVE_2026-04-27.md`
- F5 allocator (verified single-cat): `scripts/build_corpus_revision_500_hand.py:393, 454`
- QC full finding: `~/river-rats-qc/findings/2026-04-27-pr76-pre-merge-blueprint-v3-5-scenario-expansion.md`
- Audit speed: ~8 min

**Status: APPROVE clean. V-Synthesis-Correction first application validates architect's correction discipline.**
