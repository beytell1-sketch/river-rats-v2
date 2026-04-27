---
date: 2026-04-27
from: River Rats QC stream
to: Main terminal (orchestrator) · Lead-programmer · Owner (briefed)
re: Audit 4 PRE-MERGE — PR #70 head c8df9663 (post-Phase-10 force-push); APPROVE clean; orchestrator may merge per HARD RULE
severity: APPROVE clean (BLOCKING gate cleared)
status: PRE-MERGE AUDIT COMPLETE — orchestrator unblocked to merge
test-class: V-Source + V-Implementation-Spec-Match + V-Integration-Trace + V-Allocator-Multi-Dim
PR head audited: c8df9663b9d912465db22d76ee59f1d1d56e154b
master HEAD: 938026f
---

# QC Audit 4 — PR #70 Pre-Merge (Post-Phase-10 Force-Push)

## Headline

**APPROVE clean.** Phase 10 force-push (head `fa82e96 → c8df9663`) successfully:
1. Deduplicated PILOT_009 prior_actions (now 3 entries; was 5 with 3x duplicate `'preflop: SB raise'`)
2. Confirmed dedup is **global** — 0 of 100 records have any duplicate prior_actions
3. Refined lock attestation counters with V-Allocator-Multi-Dim discipline (whole-corpus criterion-match counts + provenance-based template counts as separate gates)
4. Updated SHA256 hashes for both pilot 100 corpus and 494-hand combined corpus
5. Added regression test on PILOT_009 specifically

Per orchestrator's HARD RULE (`feedback_qc_required_before_approval.md`): **QC clearance complete — orchestrator may merge PR #70.**

## Vector results

| Vector | Result | Evidence |
|--------|--------|----------|
| **V-Source: PILOT_009 dedup** | ✅ PASS | `PILOT_009.prior_actions = ['preflop: SB raise', 'flop: SB check', 'turn: SB check']` — clean |
| **V-Source: dedup is global** | ✅ PASS | Sampled all 100 records; 0/100 have any duplicate prior_actions entries |
| V-Implementation-Spec-Match: lock attestation | ✅ PASS | 8 attestation fields: combined_corpus_count=494 (394 new + 100 existing), Phase A 349 + Phase B 45 = 394, SHA256_new + SHA256_combined present, disjointness 0 within-batch dups, structural_verification with 7 sub-gates |
| **V-Implementation-Spec-Match: counter refinement** | ✅ PASS | Build script change splits magg counter into criterion-match (`magg_villain_aggression_2_count: 73`, whole-corpus `== 2`) + provenance (`magg_template_count: 64`, `generation_source == magg_scenarios`); same pattern for sb (`sb_hero_count: 26` whole-corpus + `sb_hero_template_count: 20` provenance) |
| **V-Allocator-Multi-Dim at lock level** | ✅ PASS | The new magg_template_count + sb_hero_template_count fields explicitly distinguish criterion-match count from bucket-assignment / provenance count — exactly the discrimination V-Allocator-Multi-Dim demands. Lock attestation now self-documents the multi-dimension nature of category counting. |

## Force-push delta verification

```
data/corpus_revision_500_hand_2026-04-27.jsonl     | 198 +/-
data/corpus_revision_500_hand_2026-04-27.lock      |   8 +/-
data/pilot_corpus_100_hand_2026-04-26.lock.json    |   2 +
data/pilot_corpus_100_hand_2026-04-26_v2.jsonl     | 198 +/-
review/comms/MAIN_TERMINAL_PR70_DATA_SYNTHESIS    | 107 +
review/comms/PROGRAMMER_REPORT_PHASE10_FIX        | 185 +
review/comms/REVIEW_GTO_EXPERT_PR70_DATA          | 241 +
review/comms/REVIEW_ML_ARCHITECT_PR70_DATA        | 314 +
river-rats-core/tests/test_corpus_revision_v3.py  |  74 +
scripts/build_corpus_revision_500_hand.py         |  14 +/-
```

Changes match Phase 10 directive scope:
- Pilot 100 re-extracted (deduplicated prior_actions)
- C2 corpus rebuilt (since pilot data changed → SHA changed → re-allocation needed)
- Lock files updated with new SHA256 hashes
- Round 3 review comms + synthesis + programmer report copied for provenance
- Regression test added (74 lines in tests file — substantial test coverage)
- Build script counter semantics refined

## V-Integration-Trace (TC-26)

Builder report `PROGRAMMER_REPORT_PHASE10_FIX_2026-04-27.md` includes regression test on PILOT_009. The test will fire if any future re-extraction reintroduces duplicate prior_actions entries — operationalizes V-Integration-Trace at the data layer. Convergence between QC vector design + builder test design (per established pattern).

## Lock attestation values cross-check

| Field | Value | Sanity |
|-------|-------|--------|
| combined_corpus_count | 494 | matches builder Phase 8 report |
| new_hand_count | 394 | 494 - 100 existing = 394 ✓ |
| phase_a_count + phase_b_count | 349 + 45 = 394 | matches new_hand_count ✓ |
| facing_bet_count | 163 | reasonable for 494-hand corpus |
| pfa_count | 217 | reasonable (~44% of corpus is PFA) |
| magg_villain_aggression_2_count | 73 | criterion-match (whole corpus, == 2) |
| magg_template_count | 64 | provenance (magg_scenarios source) |
| sb_hero_count | 26 | criterion-match (hero_position == 'SB') |
| sb_hero_template_count | 20 | provenance (sb_hero_scenarios source) |
| disjointness within_batch_duplicates | 0 | clean |

The split between criterion-match (73, 26) and provenance (64, 20) reveals multi-cat routing dynamics: 9 records satisfy MAGG criterion (vac=2) but came from non-MAGG generators (likely pfa or other modules with vac=2 action histories); 6 records have hero_position='SB' but came from non-sb_hero generators. **This is exactly what V-Allocator-Multi-Dim discipline requires.**

## Findings

- **HIGH/MEDIUM/LOW/NIT:** none

All 4 vector classes PASS. Phase 10 fix is clean and global. Lock attestation evolution shows mature V-Allocator-Multi-Dim discipline.

## Recommendations

### To orchestrator
**APPROVE merge of PR #70.** No QC findings. HARD RULE gate cleared.

### Post-merge
- Mass labelling kickoff (next major directive)
- 494-hand corpus × ~5 labellers = ~2470 labels via v3.2 protocol
- Output → `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` for v9 student model warm-start

### Process learning — V-Allocator-Multi-Dim baked into attestation

Builder's lock-attestation refinement (separate criterion-match + provenance counters) is the canonical operationalization of V-Allocator-Multi-Dim. **Future allocator-class artifacts should follow this pattern**: each category quota gets two attestation fields (one for "satisfies criteria", one for "assigned to this category's bucket"). Add to QC `test_class_registry.md` as a recommended attestation shape.

## Audit speed

~5 min (force-push detected via head SHA change; surgical V-Source check on PILOT_009; mechanical sanity-check on lock fields; build script diff inspection).

## Reference

- PR #70: https://github.com/beytell1-sketch/river-rats-v2/pull/70
- PR head SHA: `c8df9663b9d912465db22d76ee59f1d1d56e154b`
- Master HEAD: `938026f`
- Phase 10 directive: master `0fd69b8` (PR #90)
- Phase 10 force-push delta: 10 files; pilot 100 re-extracted; corpus rebuilt; lock + reviews + report + test
- Audit speed: ~5 min

**Status: AUDIT 4 PRE-MERGE COMPLETE. APPROVE clean. Orchestrator may merge PR #70 per HARD RULE.**
