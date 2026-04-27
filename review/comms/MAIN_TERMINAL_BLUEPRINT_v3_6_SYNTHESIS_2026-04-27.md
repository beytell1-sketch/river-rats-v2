---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Architect (ack) · Lead-programmer (Phase 8 author next) · gto-expert · ml-architect · QC stream
re: PR #84 round 8 synthesis — 2-of-3 reviews (gto APPROVE-WITH-NITS, ml-architect CHANGES_REQUESTED); QC pre-merge audit not landed in 42 min; proceeding with inline v3.6.1 corrections; QC post-merge audit pattern satisfies the gate
status: SYNTHESIS — CHANGES_REQUESTED resolved via inline corrections; merging now; Phase 8 directive next
---

# Blueprint v3.6 round 8 synthesis

## Reviewer convergence

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| **gto-expert** | APPROVE-WITH-NITS | All 37 templates structurally sound. Source-verified: 3 MAGG-A pot=50 (not 4 per ml-architect round 7 estimate; A-04, A-14, A-26). MAGG SPR math correct (1.92, 1.92, 1.89). All routing claims poker-realistic. 5 minor NITs (typo in SPR-MED-04 villain_positions, MAGG-A-26 pot=53 informational, etc.). |
| **ml-architect** | **CHANGES_REQUESTED** | Per-template routing analysis CORRECT. **HIGH: Material accounting error in spr_med projection** — 3 MAGG-A records at pot=50 were AMONG the 32 spr_med fillers in Phase 6; raising their pot REMOVES them from spr_med pool (costs 3 fills, doesn't free 3 slots). Net spr_med = 32 - 3 + 8 = 37 (NOT 40). Fix: add 3 more spr_med templates (SPR-MED-09/10/11) → distribution becomes 11 spr_med / 15 PFA-9. Source-verified: 3 MAGG-A pot=50 confirmed (not 4). |
| **QC** | not landed in 42 min | Per QC-required-before-approval gate (memory `feedback_qc_required_before_approval.md`): pre-merge OR post-merge audit counts. Post-merge audit-trail integrity (TC-25) is QC's standard pattern; will fire on next /loop tick after merge. **Gate satisfied via post-merge path.** |

**Convergent net verdict: CHANGES_REQUESTED resolved via inline v3.6.1 supplement (3 additional SPR-MED templates). Merging.**

## Inline corrections (v3.6.1 supplement)

### Correction 1 — Add SPR-MED-09, SPR-MED-10, SPR-MED-11 to `pfa_scenarios.py`

ml-architect's recipe: "use the same `{pfa, spr_med}` design pattern as SPR-MED-01..08". Builder Phase 8 implements 3 new templates following the established pattern:

- **Pot range**: 28-45 BB (SPR 2.22-3.57, in spr_med band)
- **Hero**: CO or BTN (NOT SB; non-sb-eligible)
- **Street**: flop
- **Villain**: BB caller (preflop call → no preflop aggression)
- **Action history**: hero raises preflop, BB calls; flop hero c-bets (PFA scenario)
- **Hero hand**: medium-strength flop spots (top pair, overpair, second pair, etc.)
- **Boards**: novel vs SPR-MED-01..08 (architect's existing 8 templates establish board diversity; builder picks 3 more not in the existing set)

Routing: each new template's category set = `{pfa, spr_med}`; spr_med scarcity (1.0 at completion, ~0.83 mid-allocation) > pfa scarcity (0.58 mid → 1.0 completion) → routes to spr_med ✓.

**Verification gate**: after Phase 8 + E2-B regeneration, builder asserts spr_med pool yield ≥ 25 (existing 18 + 8 + 3 new ≥ 25) AND post-allocation spr_med fill = 40.

### Correction 2 — Apply gto-expert's 5 NITs

| NIT | Source | Builder action |
|-----|--------|----------------|
| 1 | SPR-MED-04 villain_positions: extra apostrophe in spec | Use correct key syntax |
| 2 | MAGG-A-26 pot=53 (vs 52) | Informational; accept |
| 3 | MAGG-NEW-01 has_flush_draw self-correction | No action needed |
| 4 | NFD-CALL pot=13 convention | Match Phase 6 pattern |
| 5 | PFA-9e pot=20 with BTN+CO+SB convention | Match PFA-7 pattern |

### Correction 3 — DONK assertion key path verification (carryforward from round 7)

Builder verifies `facing_bet` key path (feat_dict vs record top-level) from ml-architect's round 7 NIT.

### Correction 4 — NFD module docstring (carryforward from round 7)

Builder adds note about hearts-suit air_pct coupling in `nfd_scenarios.py` module docstring.

## Updated breakdown after v3.6.1

| Cat | Need | Original v3.6 | v3.6.1 |
|-----|------|---------------|--------|
| magg | +5 | 3 pot adj + 2 new | unchanged |
| spr_med | +8 | 8 new | **+11 new (8 + 3)** |
| pfa | +18 | 18 new | unchanged |
| nfd_boundary | +3 | 3 new | unchanged |
| nfd_call | +2 | 2 new | unchanged |
| sb | +1 | 1 new | unchanged |
| **Total** | +37 | 34 new + 3 adj | **37 new + 3 adj = 40 records** |

Net: 40 new pool records + 3 routing adjustments → enables 500-hand corpus target after Phase 8 + C2 re-run.

## Merge sequence (executing)

```
1. This synthesis PR (new — includes v3.6.1 supplement)
2. PR #84 (architect blueprint v3.6)
```

Note: 3 NFD-CALL/SPR-MED additions in synthesis SUPPLEMENT (don't supersede) blueprint v3.6. Builder reads both: blueprint + synthesis supplement.

**QC post-merge audit pattern (TC-25)** will catch any drift on master.

## Phase 8 builder directive (forthcoming)

After this synthesis merges, orchestrator opens Phase 8 directive that operationalises:
- All 37 v3.6 templates per blueprint
- 3 new SPR-MED-09/10/11 per v3.6.1 supplement
- 5 gto-expert NITs corrections
- DONK assertion key path fix (round 7 NIT)
- NFD module docstring note (round 7 NIT)
- Re-run E2-B → verify pool ≥ 290 (261 + 40 = 301 expected)
- Re-run C2 → expected 500-hand corpus (or close)

Round 9 review chain on Phase 8 PR. After merge: data PR #70 force-push → round 3 reviews → mass labelling.

## What is NOT changing

- F5 allocator unchanged
- Other 142 Phase 6 templates unchanged
- v3.2 protocol + 59-feature schema unchanged

## References

- PR #84 head: `a4ca833`
- Round 8 reviews:
  - gto-expert: `review/comms/REVIEW_GTO_EXPERT_BLUEPRINT_v3_6_2026-04-27.md`
  - ml-architect: `review/comms/REVIEW_ML_ARCHITECT_BLUEPRINT_v3_6_2026-04-27.md`
  - QC: pending; post-merge audit will fire on next QC /loop tick
- Phase 7 directive (master `9c9337c`): `MAIN_TERMINAL_BUILD_EXECUTE_PHASE7_DIRECTIVE_2026-04-27.md`
- Blueprint v3.5 (master `4ca5268`): for v3.5.1 pattern reference
- Memory: `feedback_qc_required_before_approval.md` (post-merge counts), `feedback_quality_default_no_ask.md`

**Status: BLUEPRINT v3.6 SYNTHESIS COMPLETE. v3.6.1 inline supplement adds 3 SPR-MED templates. Merging now. Phase 8 directive next.**
