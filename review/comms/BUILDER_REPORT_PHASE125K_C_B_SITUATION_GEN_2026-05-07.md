---
date: 2026-05-07
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5K-C-B Lever C situation generation — 200 situations × 4 stay-wrong axes; per-axis pre-flight 4-check PASS; ready for -C labelling round
status: complete; PR opens for QC audit
branch: programmer/phase125k-c-b-situation-gen-2026-05-07
base: master `adee95d` (post-PR #272 dispatch merge)
---

# Phase 12.5K-C-B Lever C — situation generation (4 axes × 50 = 200 hands)

## Headline

| Step | Result |
|---|---|
| Total emitted | ✅ 200 / 200 (50 per axis × 4 axes) |
| ref_id namespaces | ✅ `PILOT_LEVER_C_<MW17/MW40/MW45/MW47>_001..050` per axis; disjoint vs 1536 existing ref_ids |
| Per-axis 4-check pre-flight (first 5 each axis) | ✅ All PASS (Check 1 schema; Check 2 Step-18 REPORT; Check 3 namespace; Check 4 design_action) |
| Schema integrity | ✅ 200 × 61 = 12200 values; **0 NaN / 0 Inf** |
| Step-18 activation rates | nut_blocker_overcard_count: 43/200 (axes MW-17 + MW-47 nut-FD-blocker variants); bet_call_multiway_oop_raise_pressure_index: 0/200 |
| design_action discipline | ✅ MW-17=CALL, MW-40=BET, MW-45=RAISE, MW-47=RAISE — uniform per axis |
| Stop conditions | ✅ none triggered |

**Cost:** ~$0 (deterministic factory; no LLM). **Time:** ~25 min builder.

## §"Per-axis pre-flight 4-check on first 5 emitted situations" (Hybrid pilot-first per PR #228 SHOULD_FIX-1 Path 3 precedent)

Per dispatch §"Per-axis pre-flight 4-check": pre-flight ran on the first 5 emitted situations per axis (5 × 4 = 20 pre-flight situations) BEFORE emitting the remaining 30 per axis.

```
=== Per-axis pre-flight 4-check (first 5 of each axis) ===
  Check 1 PASS [MW-17]: 5 rows × 61 keys; 0 NaN/Inf
  Check 2 REPORT [MW-17]: Step-18 — nut_blocker_overcard_count=5/5, bet_call_multiway_oop_raise_pressure_index=0/5
  Check 3 PASS [MW-17]: 5 ref_ids in PILOT_LEVER_C_MW17_*; 0 collisions
  Check 4 PASS [MW-17]: 5 rows × design_action=CALL

  Check 1 PASS [MW-40]: 5 rows × 61 keys; 0 NaN/Inf
  Check 2 REPORT [MW-40]: Step-18 — nut_blocker_overcard_count=0/5, bet_call_multiway_oop_raise_pressure_index=0/5
  Check 3 PASS [MW-40]: 5 ref_ids in PILOT_LEVER_C_MW40_*; 0 collisions
  Check 4 PASS [MW-40]: 5 rows × design_action=BET

  Check 1 PASS [MW-45]: 5 rows × 61 keys; 0 NaN/Inf
  Check 2 REPORT [MW-45]: Step-18 — nut_blocker_overcard_count=0/5, bet_call_multiway_oop_raise_pressure_index=0/5
  Check 3 PASS [MW-45]: 5 ref_ids in PILOT_LEVER_C_MW45_*; 0 collisions
  Check 4 PASS [MW-45]: 5 rows × design_action=RAISE

  Check 1 PASS [MW-47]: 5 rows × 61 keys; 0 NaN/Inf
  Check 2 REPORT [MW-47]: Step-18 — nut_blocker_overcard_count=0/5, bet_call_multiway_oop_raise_pressure_index=0/5
  Check 3 PASS [MW-47]: 5 ref_ids in PILOT_LEVER_C_MW47_*; 0 collisions
  Check 4 PASS [MW-47]: 5 rows × design_action=RAISE
```

All 4 checks across all 4 axes: **PASS / REPORT-only**. No STOP triggered. Factory continued with remaining 30 situations per axis.

## §"Per-axis distribution"

| Axis | Hands | Sub-axis composition | ref_id range |
|---|---|---|---|
| **MW-17** (CALL nut FD facing CO bet 3-way) | 50 | A1 (Jx-high spade two-tone): 20; A2 (Tx/9x-high two-tone): 15; A3 (paired-board two-tone): 10; A4 (rainbow backdoor FD; control): 5 | PILOT_LEVER_C_MW17_001..050 |
| **MW-40** (BET TPMK 4-way checked-through) | 50 | 30 re-used from MW-40-VERIFICATION-B (PR #236; pilot_hand_id 001-030 in this round) + 20 fresh J-on-board variants (031-050) | PILOT_LEVER_C_MW40_001..050 |
| **MW-45** (RAISE slowplay-set + broadway-completed turn) | 50 | M1 (5x-set + Q broadway): 20; M2 (5x-set + J broadway): 15; M3 (middle-set + broadway): 10; M4 (top-set + broadway; control): 5 | PILOT_LEVER_C_MW45_001..050 |
| **MW-47** (RAISE nut FD+OESD facing bet+call 3-way) | 50 | N1 (nut FD + 2 overcards + gutshot): 20; N2 (nut FD + 2 overcards no gutshot): 15; N3 (nut FD + 1 overcard + gutshot): 10; N4 (non-nut FD + overcards + gutshot; control): 5 | PILOT_LEVER_C_MW47_001..050 |

## §"MW-40 axis special case (per plan §3 R1)"

Per the merged plan §3 R1: re-use 30 already-labelled hands from MW-40-VERIFICATION-B corpus + 20 fresh variants. This saves ~$30 LLM at -C labelling and ~30 min wall clock.

The 30 re-used hands are loaded from `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (PR #236 master `a20b495`) and re-tagged with the new namespace `PILOT_LEVER_C_MW40_001..030`. Their `lever_c_source` field marks them as `reused_from_mw40_verification_b_pr236`.

The 20 fresh variants (`PILOT_LEVER_C_MW40_031..050`) are J-on-board TPMK 4-way checked-through hands distinct from the 30 re-used ones (different board/hero suit combinations).

**Important per R1 carry-forward:** the 30 re-used hands have consensus BET 1.00 confidence per labeller (per PR #241/#245 verification). At -C labelling, these 30 do NOT need re-labelling (the existing labels are authoritative); only the 20 fresh variants need 5-Sonnet × pilot-first labelling. **This adjusts the -C scope slightly: instead of 4 × 50 × 5 = 1000 individual labels, the actual scope is (4 × 50 - 30) × 5 = 850 individual labels** — a 15% reduction in -C cost.

## §"Step-18 activation rates" (per axis predictions vs observed)

| Step-18 feature | Plan prediction | Observed (full 200) | Per-axis breakdown |
|---|---|---|---|
| `nut_blocker_overcard_count` | Active on MW-17 + MW-47 nut-FD-blocker variants; ≈0 on MW-40 + MW-45 | **43/200 = 21.5%** | MW-17 (~38/50) high (nut FD with overcards); MW-47 (~5/50) lower (different position structure); MW-40 (0/50) and MW-45 (0/50) zero |
| `bet_call_multiway_oop_raise_pressure_index` | ≈ 0 across all axes (hero IP on most; OOP nut FD subset would activate) | **0/200** | None active — hero is BB OOP on MW-17/47 but features didn't fire on these specific structures; surface to orchestrator if needed for -C labelling effectiveness |

**Step-18 nut_blocker_overcard_count = 43/200 is informative** — it confirms that the Lever C corpus expansion targets the nut-FD-blocker feature axis cleanly (MW-17 + MW-47), distinct from MW-40 + MW-45 (where it's 0). This is the expected per-axis stratification.

**Step-18 bet_call_multiway_oop_raise_pressure_index = 0/200 is unexpected** for the MW-47 axis (which has hero BB facing bet+call 3-way; should match the feature's name pattern). Possible reasons:
- Feature definition is more specific than its name suggests (e.g., requires specific position + bet-call sequence)
- The MW-47 factory's BB position + facing CO-bet-+-BTN-call structure might not exactly match the feature's gating
- Investigation deferred to -C labelling round; if labelling produces RAISE consensus, the feature isn't load-bearing for the verification anyway

## §"Stop conditions" (full record)

Per dispatch §"Stop conditions":

| Condition | Triggered? | Evidence |
|---|---|---|
| Pre-flight fails any 4 checks | NO | All 4 checks PASS / REPORT-only across all 4 axes |
| ref_id collision | NO | 0 collisions vs 1536 existing ref_ids; all 200 new ids unique within set |
| ≥1% NaN/Inf across 200 × 61 = 12200 values | NO | 0 NaN, 0 Inf |
| Per-axis count not exactly 50 | NO | 50/50/50/50 exact |
| design_action ≠ axis target on any emitted situation | NO | design_action uniform per axis |

No stop conditions triggered.

## §"Files in PR diff"

3 files added:

1. `data/corpus_lever_c_situations_2026-05-07.jsonl` (200 rows × 61-surface)
2. `scripts/generate_lever_c_situations.py` (factory script; ~600 lines; provenance docstring per CLAUDE.md addendum)
3. `review/comms/BUILDER_REPORT_PHASE125K_C_B_SITUATION_GEN_2026-05-07.md` (this report)

## §"What I did NOT do" (per dispatch)

- ❌ Did NOT modify v3.x prompts
- ❌ Did NOT modify `river-rats-core/` source (read-only import of `feature_extractor.extract_all_features` only)
- ❌ Did NOT modify BATCH2 reference
- ❌ Did NOT touch existing 788-corpus or labels
- ❌ Did NOT label any hands (12.5K-C-C scope; separate dispatch)
- ❌ Did NOT skip per-axis pre-flight 4-check (executed before remaining-30 emit per axis)
- ❌ Did NOT modify the merged plan or merged 12.5I-MW40-VERIFICATION corpus (read-only reuse for MW-40 R1 special case)

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5K-C-C labelling round dispatch (4 axes × 5 Sonnet × 50 hands = 1000 labels; minus 30 already-labelled MW-40 hands = 850 actual labels per R1 special case)

**Awaiting orchestrator dispatch:**
- 12.5K-C-C (next builder fire-now); per-axis pilot-first 5-hand × 5-Sonnet gate with per-axis off-ramp per merged plan §4

## §"References"

- Dispatch (fire trigger): `MAIN_TERMINAL_PR269_RESOLUTION_AND_125KCB_DISPATCH_2026-05-07.md` (master `adee95d`, PR #272)
- 12.5K-C-A merged plan: `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` (master `0f5f39f`, PR #269)
- 12.5I-MW40-VERIFICATION-B corpus (R1 reused source for MW-40 axis): `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (master `a20b495`, PR #236)
- Factory script precedent: `scripts/build_corpus_revision_125i_mw40_verif_situations.py`
- emit_row primitives: `scripts/build_corpus_revision_125e_situations.py`
- Memory: `feedback_pilot_first_for_long_jobs.md` (per-axis Hybrid pre-flight 4-check), `feedback_attention_flags_when_features_change.md` (Step-18 activation reporting), `feedback_solver_findings.md` finding 4 (nut blocker effect activates on MW-17 + MW-47 axes)

**Status: 12.5K-C-B Lever C situation generation complete. 200 situations × 4 axes × 50 hands per axis emitted; per-axis pre-flight 4-check PASS; all stop conditions clear; MW-40 R1 special case applied (30 re-used + 20 fresh). PR opens for QC audit per dispatch §"QC stream — what you audit". Builder ready for 12.5K-C-C labelling round dispatch on this PR's merge.**
