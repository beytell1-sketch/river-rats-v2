---
date: 2026-04-27
from: River Rats QC stream
to: Architect (logic-domain) · Main terminal (orchestrator) · ml-architect reviewer · gto-expert reviewer · Lead-programmer (post-merge handoff) · Owner (briefed)
re: PR #56 pre-merge QC audit — Blueprint v2 (Architect Phase 2.5 update); APPROVE (clean); all V-Source + V-X1 + V-X4 + V-Synthesis + V-OQ-Resolution vectors PASS
severity: APPROVE / no findings
status: FLAG (advisory; pre-merge informational); HIGH-impact recommendation to lead-programmer for OQ-4 pre-implementation verification step
---

# QC Pre-Merge Audit — PR #56 (Blueprint v2)

## Headline

**APPROVE clean.** Single-file design blueprint v2 (+1016/-0 markdown, 0 code changes; supersedes PR #53). All 5 R-items from synthesis (`cde6672`) incorporated; 2 new scenario modules (8 + 9); OQ-1/2/3 dispositions match synthesis verbatim; OQ-4 + OQ-5 raised with graceful-degradation discipline + quality-first defaults.

QC PR #54 (PR #53 audit) was absorbed via Path B pattern in synthesis comm (verdict cited + Path A or C recommendation adopted). Should close as superseded post PR #56 merge.

## Vector results

| Vector | Result |
|--------|--------|
| V-X1 file existence | ✅ PASS |
| V-X4 carryforward consistency to synthesis `cde6672` | ✅ PASS |
| V-Source-1/2/3/4 (inherited from v1) | ✅ PASS |
| V-Synthesis-1 (NEW) — all 5 R-items + 2 scope additions traced to synthesis | ✅ PASS |
| V-OQ-Resolution (NEW) — OQ-1/2/3 dispositions match synthesis | ✅ PASS |
| V-OQ-4 graceful-degradation | ✅ PASS |
| V-OQ-5 quality-first default | ✅ PASS |

## OQ-4 master verification

Blueprint v2 OQ-4 asks: can `_opener_position` be reconstructed from `prior_actions`?

QC sampled `data/pilot_corpus_100_hand_2026-04-26.jsonl` first record:
```python
prior_actions = ['preflop: BB call']
```

Does NOT include opener identity. Blueprint v2 correctly flags pre-implementation verification step + graceful fallback (lines 993-995): if `prior_actions` lacks preflop opener AND no separate `opener_position` field exists, re-extracted hands keep `is_preflop_aggressor=0`; SPR confound still resolved (ml-architect's primary concern handled).

**This is excellent design discipline**: identifies unknown ahead of implementation, defines verification step, specifies graceful fallback, documents trade-off.

## Synthesis ↔ blueprint v2 fidelity (all match)

| Synthesis decision | Blueprint v2 |
|--------------------|--------------|
| Path A adopted | OQ-1 line 977 ✅ |
| 5 R-items required | R1-R5 all present ✅ |
| 2 scope additions | Module 8 (donk-bet defence) + Module 9 (SB sandwich) ✅ |
| OQ-1 RESOLVED | line 975 ✅ |
| OQ-2 DEFERRED PER QC | line 979 ✅ |
| OQ-3 RESOLVED informational | line 985 ✅ |

## R-item verification

- **R1** Path A re-extraction script: present at line 625, 865 — correctly scoped
- **R2** schema-compatibility verifier: present in Implementation Handoff
- **R3** MAGG action histories extended to river: present
- **R4** NFD ±0.03 tolerance: present + threshold matches v3.2 OVERRIDE at `villain_air_pct >= 0.20`
- **R5** Rule 11 boundary pairs across 5 textures: present (dry-paired, 2-tone-paired, dynamic-paired, monotone, draw-heavy-paired)

## Module 8/9 scope check

- **Module 8** (donk-bet defence): IP facing OOP donk lead. 25-hand quota. Realistic poker scenario covering pattern oracle self-play under-produces.
- **Module 9** (SB-as-hero sandwich): MW-30 pattern. 20-hand quota. Addresses Gap 4 (`num_callers_to_bet >= 1`).

Phase A grows 310 → 355; Phase B drops 90 → 45. OQ-5 NEW raises whether 45 hands are sufficient distributional fill across 8-dim space (2592 cells); blueprint correctly notes Phase B is distributional fill not exhaustive coverage and provides quality-first default with structural-verification gate.

## HIGH-impact recommendation to lead-programmer (post-merge implementation handoff)

**Pre-implementation verification step** (per OQ-4):

Before implementing R1 `scripts/reextract_pilot_100_features.py`:
1. Sample 5-10 hands from `data/pilot_corpus_100_hand_2026-04-26.jsonl` and check whether `prior_actions` contains the preflop opener's bet (e.g., entries like `'preflop: BTN raise to 2.5'`).
2. Alternatively, check whether the source-pool record (`training-data/3way_situations_10k.jsonl`) has a separate `opener_position` field accessible via `situation_id` linkage.
3. **If neither path works**: implement the graceful-degradation fallback per blueprint OQ-4 (R1 still corrects SPR; IS_PFA remains 0 for old 100; new 400 hands have correct IS_PFA from generation-time capture).

QC's single-hand sample showed `['preflop: BB call']` — does NOT include opener. Programmer should sample broader before assuming worst case. **If broader sampling confirms worst case, take the fallback path; do not delay R1 on a perfect-IS-PFA-recovery rabbit hole.**

## Recommendations

### To orchestrator's dispatched reviewers (ml-architect + gto-expert)
**APPROVE merge.** All vectors PASS. No findings. Blueprint v2 cleanly implements synthesis decisions.

### Post-merge sequence (anticipated)
1. PR #56 merges; lead-programmer dispatches implementation
2. Programmer pre-flight: OQ-4 verification step (above)
3. Build E1: `scripts/reextract_pilot_100_features.py` (R1 Path A re-extraction)
4. Build E2: source-pool generator with corrected SPR units + opener_position capture
5. Build E3: `scripts/verify_feature_schema_compatibility.py` (R2)
6. Build C2: 500-hand corpus on revised pool (100 re-extracted + 400 new)
7. Tier 1 calibration manifest 33→45 PR (HIGH-2 fix surface check)

QC pre-merge audits each via worktree → branch → PR pattern.

## Process learning — V-Synthesis-1 + V-OQ-Resolution + V-OQ-Graceful-Degradation (TC-24 subclasses)

Add to QC `test_class_registry.md`:
- **V-Synthesis-1**: synthesis comm decisions match downstream blueprint/spec content
- **V-OQ-Resolution**: each OQ disposition consistent across synthesis ↔ blueprint pair
- **V-OQ-Graceful-Degradation**: when blueprint raises NEW OQ with unknown-state precondition, verify graceful-degradation fallback is specified

Activate for design-blueprint round-N PRs (N>1, after synthesis cycle).

## Reference

- PR #56 head: `21b99fec74ac3768416b83a19340ba3a2d66aa58`
- Master HEAD: `f5008b9`
- Synthesis: `review/comms/MAIN_TERMINAL_BLUEPRINT_REVIEW_SYNTHESIS_2026-04-27.md` (master `cde6672`)
- Predecessor PR #53 (CLOSED): QC audit at `~/river-rats-qc/findings/2026-04-27-pr53-pre-merge-blueprint-corpus-generation.md`
- QC full finding (this audit): `~/river-rats-qc/findings/2026-04-27-pr56-pre-merge-blueprint-v2.md`
- Audit speed: ~10 min

**Status: APPROVE clean.**
