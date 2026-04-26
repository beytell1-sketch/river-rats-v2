---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT GTO reviewer (gto-expert subagent unavailable; persona spec embedded per builder dispatch; reviewer is NOT v1.0 author and NOT v1.0/v1.0.1 Protocol B author or reviewer)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #12 — Stage 4 Protocol C v1.0 (`d77a95e`)
status: APPROVE-WITH-NITS — content structurally sound, cross-protocol alignment with Protocol B v1.0.1 verified, schema collision check clean (verified empirically by reviewer); 1 MEDIUM (raise-sizing taxonomy conflicts with feedback_solver_aligned_sizing.md — author self-flagged as highest-priority UNCERTAIN); 2 LOW; several NITs. Recommended fix-forward (Task 2.1) for the MEDIUM before pilot dispatch; not strictly merge-blocking
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/12
branch: stage4-prep/protocol-c-fill
artifact: prompts/protocol_c_adversarial_elimination_v1_0.md (1622 lines)
predecessor: prompts/stage4_drafts/protocol_c_adversarial_elimination_v0_1_DRAFT.md (342 lines)
sister: prompts/protocol_b_composition_first_v1_0.md (v1.0.1 merged at dc6fa1f)
---

# Review Verdict — PR #12 (Stage 4 Protocol C v1.0)

## Provenance note

Independent reviewer dispatch under read-only constraint. Did NOT author Protocol C v1.0; did NOT review Protocol B v1.0/v1.0.1. All file reads at `d77a95e` HEAD of `stage4-prep/protocol-c-fill`. Cross-references against `dc6fa1f` (Protocol B v1.0.1 merge commit). Builder writes this comms file from reviewer's message body.

## Builder verification spot-checks

- Field-name collision check: empirical enumeration vs `gto_model.py` FEATURE_COLUMNS → **NONE** ✓
- All 5 example composition triples sum to 1.0 exactly ✓
- Example 2 arithmetic: 30/(30+90) = 0.25 ✓; beatable slice 0.59 ✓; surplus 0.15 ✓
- Example 1 EV claim 0.30 × 9bb ≈ 2.7bb ✓; BET_66 = 5.94 ≈ 6bb ✓
- Example 5 SPR (100-7.5)/18 ≈ 5.14 ✓; turn BET_33 = 0.33 × 18 ≈ 6bb ✓
- Editorial drift search: zero hits (PR #10 failure mode NOT reproduced) ✓
- Cross-protocol Examples 2+4 spot match Protocol B v1.0.1 (boards, action histories, compositions) ✓
- CSV-pipeline trace: Protocol C metadata never enters CSV path (verified) ✓

---

## Item A — Sizing enumeration completeness for 3-way postflop

**OK-WITH-MEDIUM / HIGH confidence.** Bet sizings (flop 25%/66%, turn 33%/75%, river 33%/75%/150%) match `feedback_solver_aligned_sizing.md` verbatim.

**MEDIUM #1 — Raise-sizing taxonomy conflicts with `feedback_solver_aligned_sizing.md`.** Author uses **2.5× / 3× facing-bet multiples** (`RAISE_2_5X`, `RAISE_3X`). The memory feedback explicitly prescribes **RAISE all streets: 33% / 66% (pot-relative)**. Author self-flagged at the highest-priority UNCERTAIN. Real misalignment: a labeller using Protocol C will enumerate `RAISE_2_5X` / `RAISE_3X` and the pilot's solver-verification pass will hit a sizing mismatch — exactly the failure mode the memory was created to prevent (Phase B 12 Apr 2026 incident, 11 of 19 hands had red-flag sizing warnings).

**Recommended fix:** Task 2.1 fix-forward replaces schema with `RAISE_33` / `RAISE_66` (pot-relative); updates Examples 2 prose and §"Step 1" raise-sizings paragraph.

3-way-specific cases addressed adequately: multi-call protection, IP/OOP after SRP/3BP with SPR-collapse, donk lines, behind-villain raise frequency.

## Item B — 4-tier rubric workability

**OK / MEDIUM-HIGH confidence.** STRONG / MODERATE / WEAK / STRAWMAN signals largely disjoint with conjunctive criteria. Boundary cases handled by explicit "considers villain's BEST counter-strategy (not just one possible)" requirement at STRONG tier. Two-grader agreement ≥80% plausible on most cases.

**LOW concern:** WEAK tier "<5% EV cost" boundary fuzzier than rubric implies for hands at 4-6% EV cost. Note in v1.1 calibration material.

## Item C — Worked examples poker-rigour AND self-consistency

**OK / HIGH confidence.** All 5 examples pass Task 1 lessons:
- Pot/SPR/sizing arithmetic verified
- No editorial drift (zero "wait... actually" hits)
- Examples 2+4 align with Protocol B v1.0.1 Examples 2+4 (boards, positions, compositions identical)
- Action follows from elimination chain

**LOW concerns (NIT-level):**
- Example 3 EV cost claim "~4-5bb" doesn't compute on 9bb pot; author handwaves draw-frequency × stack-realisation magnitude. Direction (drawn-denial value > 0) correct; magnitude unsupported.
- Example 5 `worse_hand_pct ~0.66` vs slice-sum 0.80 — author appears to haircut for residual completed-flush combos plus Ac-blocker reweighting; math works (0.80 - 0.05 - haircut ≈ 0.66) but isn't shown in trace.

## Item D — Anti-pattern list cross-check

**OK / MEDIUM-HIGH confidence.** Walked all 10 × 5 pairs. **No anti-pattern flags any example.** This is the test that PR #10 / Protocol B v1.0 failed (Anti-pattern #7 vs Example 2). Protocol C cleared it cleanly — author's self-consistency pass worked.

Notable: AP#7 (bucket-aligned auto-survivor) is exercised positively in Examples 1 and 3 which STRONG-eliminate `BET_25` despite it being a bucket-aligned candidate. Good adversarial test.

## Item E — Calibration grading rubric workability

**OK / MEDIUM confidence.** STRONG/OK/WEAK/FAIL signals disjoint. Single-FAIL = calibration-failure rule reasonable (FAIL signals represent fundamental protocol failure, not just poker mistakes). ≥2 WEAK = failure adds robustness against systematic mediocrity.

κ ≥ 0.65 target borrowed from Protocol B is **defensible but probably loose for trail-grading**. Trail-grading is higher-judgment than action-labelling. Realistic pilot κ may land 0.55-0.70. Recommend κ measured + reported at v1.0 calibration with no go/no-go gate; tighten in v1.1 from empirical data.

## Item F — Mixed-strategy GTO answer handling

**OK / HIGH confidence.** Option (a) (label MIXED, tag both candidates) is right for cross-protocol convergence. Mixing-pair coverage covers canonical solver-mixing pairs (BET/CHECK on flop/turn, CALL/RAISE facing bet, BET_25/BET_66 sizing mix, CALL/FOLD river bluff-catcher).

JSON schema self-consistent: `mixed_action_pair` (2-tuple), `mixed_confidence_band` ([0.40, 0.60] default; [0.30, 0.70] otherwise), `mixed_strategy_acknowledged`, `primary_action` tie-break. `primary_action == final_action` invariant clean for non-MIXED.

`primary_action` correctly supports cross-protocol convergence checker — Protocol C MIXED collapses to single action for A/B/C cross-comparison.

**NIT:** could add CHECK/RAISE-on-donk and defensive CALL/FOLD-on-flop bluff-catch mixes (rare but real). Not blocking.

## Item G — Schema/CSV compatibility

**OK / HIGH confidence — empirically verified.** Author flagged this as inherited rather than re-run; reviewer ran the verification:
- `gto_model.py:33-62` FEATURE_COLUMNS = 55 columns; **NO collisions** with Protocol C's 14 new field names
- `assemble_pilot_data.py:926-941 write_attention_csv` uses FEATURE_COLUMNS + attn_*; Protocol C metadata never consulted
- `export_3way_training.py:48,64` writes FEATURE_COLUMNS + ['action']; Protocol C metadata never consulted
- `train_model_v2_2.py:113-117 split_feature_columns` excludes meta-tuple; moot since Protocol C fields never enter CSV

**Author's "schema verification inherited" caveat is partially overstated.** Compatibility holds because Protocol C metadata lives in JSONL and CSV writers only consult FEATURE_COLUMNS + label/attn. Schema-collision risk genuinely zero. Forward-looking risk only when v2.5+ wants to train on `case_against_*_count` as features — `feedback_attention_flags_when_features_change.md` 4-stream protocol applies. Author acknowledges. No action required for v2.4 ship.

## Item H — Anti-pattern #8 (equity/pot-odds carve-out)

**OK / HIGH confidence.** Wording parallels Protocol B v1.0.1 AP#7. Forbidden: pre-computed `equity_vs_range` feature read OR tracker-style raw equity-vs-pot-odds as primary driver. Allowed: equity derived FROM composition slices in same trace. Allowed: cite `equity_vs_range` as confirmation in separate sentence.

Example 2 exercises the carve-out exactly as designed: composition-derived equity (slice sum 0.59 → equity 0.40). Cross-references with Protocol B v1.0.1 Example 2 same structure.

## Item I — PRE-PILOT BUILD REQUIREMENT section

**OK / HIGH confidence.** Lines 32-69 mirror Protocol B v1.0.1 lines 79-115. Names 3 v3.1 sections, output artifact, failure mode, ownership. Bold "DESIGN ARTIFACT, NOT A LABELLER-FACING PROMPT" lead-in present.

**NIT:** Cites v3.1 lines 590-647 vs Protocol B's 595-647 for DO NOT Rules — off-by-5 line range. Re-pin at build time. Not blocking for v1.0 design artifact.

## Item J — UNCERTAIN tag rigor

**OK / MEDIUM-HIGH confidence.** All 7 UNCERTAIN tags legitimate. No over-tagging or under-tagging detected. Tags #3 (schema collisions) and #6 (AP#8 carve-out parallel) can be downgraded to "reviewer-verified" post this verdict.

## Item K — Ready for orchestrator merge?

**APPROVE-WITH-NITS — confidence MEDIUM-HIGH.**

Recommend merge as v1.0 design artifact AND open Task 2.1 fix-forward for the MEDIUM (raise-sizing taxonomy) before Protocol C is dispatched to calibration exam or pilot.

**Rationale for not-BLOCK:**
- Bet-sizing schema (load-bearing flop/turn/river sizings) IS solver-aligned correctly
- Raise-sizing is smaller surface (only when hero faces a bet AND chooses RAISE — minority of 3-way postflop decisions)
- Author self-flagged with verbatim UNCERTAIN tag asking for solver verification
- Fix is mechanical (rename `RAISE_2_5X`/`RAISE_3X` → `RAISE_33`/`RAISE_66`; update prose; one-paragraph addition to §"Step 1") and surgical in v1.0.1
- Merging v1.0 lets Tasks 3 / 5 reference Protocol C in their fill-in work without waiting for v1.0.1

If orchestrator prefers stricter discipline: BLOCK + require v1.0.1 fix-forward before merge is also defensible (mirrors PR #10 → #11 pattern). Reviewer leans APPROVE-WITH-NITS because the issue is surgical and self-flagged, not structural.

---

## VERDICT

**APPROVE-WITH-NITS — overall confidence MEDIUM-HIGH.**

**Required fixes (Task 2.1 fix-forward, before pilot dispatch):**
1. **MEDIUM #1** — Replace `RAISE_2_5X` / `RAISE_3X` taxonomy with pot-relative `RAISE_33` / `RAISE_66` per `feedback_solver_aligned_sizing.md`. Update §"Step 1" raise sizings prose, output schema sample, and Example 2 case-against arguments.

**Blockers:** None for v1.0 merge as design artifact. The MEDIUM is a pre-pilot blocker.

## NIT-level observations (non-blocking)

1. Example 3 EV cost claim "~4-5bb" doesn't compute on 9bb pot — handwave; tighten in v1.1 (LOW)
2. Example 5 `worse_hand_pct ~0.66` vs slice-sum 0.80 — haircut math not shown; tighten in v1.1 (LOW)
3. WEAK tier "<5% EV cost" boundary fuzzy at 4-6% — note in v1.1 calibration (NIT)
4. Mixing-pair list could add CHECK/RAISE-on-donk + defensive CALL/FOLD-on-flop bluff-catch (NIT)
5. PRE-PILOT BUILD REQUIREMENT cites v3.1 lines 590-647 vs Protocol B's 595-647 — re-pin at build time (NIT)
6. UNCERTAIN tags #3 (schema) + #6 (AP#8 parallel) can downgrade to "reviewer-verified" (NIT)
7. κ ≥ 0.65 trail-grading target borrowed without trail-grading-specific empirical basis — measure + adjust empirically in v1.1 (NIT)

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | MEDIUM | Task 2.1 fix-forward — replace 2.5×/3× raise sizings with 33%/66% pot-relative per feedback_solver_aligned_sizing.md |
| 2 | LOW | Tighten Example 3 EV-cost arithmetic in v1.1 |
| 3 | LOW | Tighten Example 5 worse_hand_pct derivation in v1.1 |
| 4 | NIT | Note WEAK-tier 4-6% EV boundary fuzziness in v1.1 calibration material |
| 5 | NIT | Add CHECK/RAISE-on-donk + CALL/FOLD-on-flop bluff-catch to mixing-pair list (v1.1) |
| 6 | NIT | Re-pin v3.1 line ranges at build time (590-647 vs 595-647) |
| 7 | NIT | Downgrade UNCERTAIN tags #3 + #6 to reviewer-verified in v1.0.1 frontmatter |
| 8 | NIT | Measure trail-grading κ at calibration; adjust gate empirically in v1.1 |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_12_PROTOCOL_C_2026-04-26.md`.
2. Post comment on PR #12 referencing the verdict.
3. Stand by for orchestrator merge / fix-forward direction.

**Orchestrator:**
1. Read this verdict.
2. Decide: (a) merge v1.0 + open Task 2.1 fix-forward for the MEDIUM, OR (b) block merge until v1.0.1 fix-forward lands (mirrors PR #10 → #11 pattern). Reviewer recommends (a).
3. Either way: MEDIUM #1 raise-sizing taxonomy must be resolved before Protocol C is dispatched to calibration exam or pilot.

**Owner:** wake to find Protocol C v1.0 design artifact with one identified MEDIUM (raise-sizing taxonomy mismatch) — surgical fix the author self-flagged and the reviewer confirmed.

## Reference

- PR #12: https://github.com/beytell1-sketch/river-rats-v2/pull/12
- v1.0 commit: `d77a95e`
- Source artifact: `prompts/protocol_c_adversarial_elimination_v1_0.md`
- Predecessor v0.1 DRAFT: `prompts/stage4_drafts/protocol_c_adversarial_elimination_v0_1_DRAFT.md`
- Cross-reference Protocol B v1.0.1: `prompts/protocol_b_composition_first_v1_0.md` (`dc6fa1f`)
- Solver-aligned sizing memory: `~/.claude/projects/-home-rupertbeytell/memory/feedback_solver_aligned_sizing.md`
- Schema source files: `river-rats-core/gto_model.py:33-62`, `river-rats-core/assemble_pilot_data.py:926-941`, `river-rats-core/export_3way_training.py:48,64`, `river-rats-core/train_model_v2_2.py:113-117`
- Directive: `review/comms/MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md` §"Task 2"
- PR #11 verdict (Task 1 fix-forward applied lessons here): `review/comms/REVIEW_VERDICT_PR_11_PROTOCOL_B_V1_0_1_2026-04-26.md`

**FINAL VERDICT: APPROVE-WITH-NITS — MEDIUM-HIGH confidence overall. Ready for orchestrator merge as v1.0 design artifact. Task 2.1 fix-forward required to resolve raise-sizing taxonomy MEDIUM before pilot dispatch.**
