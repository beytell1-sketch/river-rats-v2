---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Lead-programmer (Phase 2 dispatch next) · gto-expert · ml-architect · QC stream
re: PR #60 review synthesis — four-reviewer convergence on CHANGES_REQUESTED; 4 required fixes (F1-F4); programmer Phase 2 dispatch next
status: SYNTHESIS — PR #60 holds CHANGES_REQUESTED; programmer Phase 2 fix-forward to address 4 fixes; QC PRs #61 + #62 ready to merge alongside this synthesis after owner go-ahead
---

# PR #60 review synthesis

## Four-reviewer convergence

| Reviewer | Verdict | HIGH/Med findings |
|----------|---------|-------------------|
| gto-expert (full GTO domain audit) | CHANGES_REQUESTED | HIGH-1 — NFD boundary scenarios fundamentally mis-designed (low boards + BTN/CO c-bet → 0.37-0.42 air, target 0.15-0.25); fix = turn-decision redesign |
| ml-architect (executable code audit) | CHANGES_REQUESTED | BUG 1 (Med-High) Mode A SPR re-extraction silently fails — wrong key names → silent KeyError → C7 fix never executes for Mode A. BUG 2 (Low-Med) N1 smoke test field name. BUG 3 (Med) OOP/IP gate uses 0.40-0.75 not 0.55-0.65 |
| QC PR #61 (pre-merge audit) | APPROVE-CHANGES-REQUESTED | Concurs gto-expert HIGH-1. C1-C7 mechanical match clean. No independent HIGH/MEDIUM findings. |
| QC PR #62 (addendum) | LEARNING + concurrence | Acknowledges ml-architect BUG 1 as second HIGH concurrence. Adds TC-26 V-Integration-Trace test class. **Notes BUG 1 is HIGHER-priority than NFD: without it, Mode A SPR rebuild is no-op — the entire BB-conversion path the corpus revision was designed around.** |

**Convergent verdict: PR #60 is CHANGES_REQUESTED. Mechanical landing of C1-C7 is clean; structural defects are integration (BUG 1) + scenario design (NFD boundary) + verification gate (BUG 3).**

## Required fixes before merge

| F# | Source | Severity | File | Change |
|----|--------|----------|------|--------|
| **F1** | ml-architect BUG 1 + QC #62 | **Med-High (highest priority)** | `river-rats-core/generate_corpus_revision_pool.py` `_generate_mode_a()` | Rename `hand_dict` keys for `extract_all_features` call from long form (`hero_cards`/`board`/`street`/`hero_position`/`to_call`/`facing_bet`/`villain_positions`) to short form (`h`/`b`/`st`/`pos`/`tc`/`fb`/`vp`). Without this, KeyError silently caught and Mode A falls back to chip-unit feat_dict — SPR remains 1.25 — entire Mode A SPR rebuild is no-op. |
| **F2** | ml-architect BUG 2 | Low-Med | `river-rats-core/tests/test_corpus_revision_v3.py` `test_n1_mode_a_pool_smoke` | Change `r.get('pot_bb', 0)` to `r.get('pot', 0)`. Mode A records store BB-unit pot under `'pot'`; current test always sees 0 → `0 > 6.0` always False → cannot detect SPR-unit regression even if F1 is wrong. |
| **F3** | ml-architect BUG 3 | Med | `scripts/build_corpus_revision_500_hand.py` `_verify_corpus()` | Tighten OOP/IP gate from `0.40 <= oop_count/n <= 0.75` to spec `0.55 <= oop_count/n <= 0.65`. Add explicit ip_pct check `0.35 <= ip_count/n <= 0.45`. Current gate admits 42% OOP corpora — would teach IP-bias. |
| **F4** | gto-expert HIGH-1 + QC #61 concurrence | **Blocker** | `river-rats-core/corpus_revision_scenarios/nfd_scenarios.py` (5 boundary templates) | Replace 5 flop-decision boundary templates (lines 124-183) with 5 turn-decision templates per gto-expert spec below. After implementation, run feature extractor on all 5 and confirm at least 3 of 5 pass R4 ±0.03 gate before declaring done. |

### F4 NFD turn-decision template specs (per gto-expert)

All 5 use action history: `('preflop', V, 'raise'), ('preflop', 'BB', 'call'), ('flop', 'BB', 'check'), ('flop', V, 'bet'), ('flop', 'BB', 'call'), ('turn', 'BB', 'check'), ('turn', V, 'bet')` with `street='turn'` and 4-card boards.

| # | Target air | Villain | Flop board | Turn card | Hero |
|---|------------|---------|------------|-----------|------|
| 1 | ~0.15 | BTN | 7h-4h-2d | 9s | Ah-Jh |
| 2 | ~0.17 | CO | 6c-3c-2h | Ks | Ac-Jc |
| 3 | ~0.20 | BTN | 8d-5d-3h | Ah (or 2c if conflict) | Ad-Td |
| 4 | ~0.22 | BTN | 9s-5s-2c | 3d | As-Qs |
| 5 | ~0.25 | CO | Ts-6s-2h | 4c | As-Ks |

Update flop pot to reflect post-flop-bet turn pot (e.g. flop pot=12, BTN bets ~4 = 33%, BB calls → turn pot ≈ 20-22).

### NFD diagnosis disagreement reconciliation

gto-expert (0.30-0.45 expected on these boards from solver theory) and programmer's empirical observation (0.37-0.42 from feature extractor) **converge**. ml-architect's review notes inconsistent values across boards (0.08-0.42), reflecting that the range_analyzer's output depends on board details — both reviewers AGREE the 5 boundary templates as currently designed do not produce 0.15-0.25 air. The fix is the same: turn-decision redesign. ml-architect's separate observation that the KB §1.7 0.20 threshold may not exactly map to the range_analyzer's feature-space 0.20 is a deeper calibration concern — flagged for v2.3+ backlog, not blocking this PR.

## Non-blocking nits (fold into Phase 2 or follow-up)

- gto-expert N1: `donk_bet_defence_scenarios.py` template 7 — dead `hero_cards: ['Ks', 'Ks']` line + confused comment (Python dict overwrite makes this functionally OK but messy)
- gto-expert N2: `facing_initial_bet_scenarios.py` scenario 9 — stale Q9 hand-equity comment (cosmetic)
- gto-expert N3: Module 9 (SB-hero) at 12 records vs blueprint target 20 — flag as known shortfall; recommend expanding to 18-20 in next iteration
- gto-expert N4: MAGG 6:4 first-to-act vs facing-bet ratio — canonical lesson taught by only 4/10 templates; flag for future iteration
- ml-architect Nit 2: zero_instance_rules + poker_pattern_coverage attestation fields are placeholders in lock file — populate before corpus submission for labelling

## Process learning

QC PR #62 introduces TC-26 V-Integration-Trace: when an implementation PR claims to "fix prior bug X", trace from input boundary → through claimed fix → to output, asserting fix value reaches consumer. ml-architect caught BUG 1 because executable review traces this; QC's mechanical V-Implementation-Spec-Match did not. The two reviews are complementary, not redundant. **For future implementation PRs, both vectors run in parallel.**

## Decision: Programmer Phase 2 dispatch

Apply F1-F4 to PR #60. All four are contained and have explicit specifications.

**Estimated scope: ~2-4 hours wall-time, ~$30-50.**

- F1: rename 7 dict keys + verify (~30 min)
- F2: 1-character key change in test (~5 min)
- F3: tighten 1 conditional + add ip_pct check (~15 min)
- F4: redesign 5 NFD templates per gto-expert spec + validate against feature extractor (~1-2 hours, iterative)

After Phase 2 lands:
- Round 2 reviews on the 4 fixes (gto-expert mini-review on NFD diff only; ml-architect re-test of F1 + F2 + F3; QC pre-merge audit on the diff with V-Implementation-Spec-Match + V-Integration-Trace paired)
- Synthesis → owner approval → merge
- Then: build E1 (R1 100-hand re-extraction), build E2 (Mode A pool), build E3 (schema verify), build C2 (500-hand assembly), Tier 1 calibration manifest 33→45

## What is NOT changing

- Blueprint v3 unchanged (no new R-items / scope additions)
- v3.2 protocol unchanged
- Mode B factory pool (111 records) is production-ready per ml-architect's audit
- 500 Phase A v3.2 labels untouched (preserved from earlier corpus)

## Sequencing

```
QC #61 + QC #62 + this synthesis PR
        ↓ (owner go-ahead)
        merge all 3
        ↓
Lead-programmer Phase 2 dispatch (F1-F4 on PR #60 branch or successor branch)
        ↓
Round 2 reviews (gto-expert NFD-diff + ml-architect re-test + QC paired vectors)
        ↓
Round 2 synthesis → owner approval → merge
        ↓
[Build E1 / E2 / E3 / C2 / Tier 1 manifest sequence]
```

## Open queries to owner

1. **QC PR #61 + #62 + this synthesis PR — merge alongside?** All 3 are comms-only docs with no code; established Path B pattern. Default = yes. **Hook denied auto-merge in this session — explicit owner go-ahead requested.**
2. **Programmer Phase 2 dispatch — go now?** F1-F4 are contained; quality-first default = dispatch immediately on owner go-ahead.
3. **NFD calibration concern (ml-architect Q3 deep finding) — defer to v2.3+ backlog?** Default = yes; out of scope for current corpus revision.

## References

- PR #60 (programmer): https://github.com/beytell1-sketch/river-rats-v2/pull/60 — head `3708d92`
- PR #61 (QC pre-merge): https://github.com/beytell1-sketch/river-rats-v2/pull/61 — comms-only
- PR #62 (QC addendum): https://github.com/beytell1-sketch/river-rats-v2/pull/62 — comms-only
- gto-expert review: `review/comms/REVIEW_GTO_EXPERT_PR60_PROGRAMMER_IMPL_2026-04-27.md`
- ml-architect review: `review/comms/REVIEW_ML_ARCHITECT_PR60_PROGRAMMER_IMPL_2026-04-27.md`
- QC pre-merge audit: `~/river-rats-qc/findings/2026-04-27-pr60-pre-merge-blueprint-v3-implementation.md` + `review/comms/QC_PRE_MERGE_AUDIT_PR60_2026-04-27.md` (PR #61)
- QC addendum: `review/comms/QC_ADDENDUM_PR60_INTEGRATION_TRACE_LEARNING_2026-04-27.md` (PR #62)
- Programmer report: `review/comms/PROGRAMMER_REPORT_BLUEPRINT_V3_IMPLEMENTATION_2026-04-27.md`
- Blueprint v3: `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md` (master `1086de2`)

**Status: PR #60 SYNTHESIS COMPLETE. CHANGES_REQUESTED. F1-F4 ready for programmer Phase 2 dispatch. Owner go-ahead requested for: (a) merge QC #61 + #62 + this synthesis PR; (b) dispatch programmer Phase 2 with F1-F4.**
