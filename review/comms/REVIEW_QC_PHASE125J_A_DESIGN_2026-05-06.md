---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (architect hat)
re: PR #198 (12.5J-A feature engineering design — 3 features for MW-17/47; Direction-X-retro scope) — APPROVE; 0 NIT
severity: clean approval
status: FLAG → APPROVE for merge
test-class: TC-23 + V-Source + dispatch §"NEW: Cascade scope completeness" + §"NEW: Feature design specificity" + §"NEW: Direction-X-retro acknowledgment"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 16th successive cycle solo-routed; first parallel-PR audit cycle)
---

# QC Review — PR #198 (12.5J-A feature design): APPROVE; 0 NIT

## Verdict

**APPROVE PR #198 for merge.** All 5 dispatch-required audits PASS cleanly. 0 NIT new findings.

Design proposes 3 candidate features (2 for MW-17 implied-odds + nut-blocker-with-overcards axis; 1 for MW-47 SUITED-NFD-bet+call-multiway-OOP raise pressure axis). All 5 cascade points per `feedback_attention_flags_when_features_change.md` explicitly addressed in §5. Direction-X-retro scope explicitly warned in §2 with owner-approval reference.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR197_PR198_2026-05-06.md` master `ce2ee5e` + PR #196 dispatch §"PR #198")

5 audits — design-only.

PR #198 head: `58cb94e` (branch — design comm only).

## Audit 1 — Diff scope ✅ CLEAN

| File | category |
|---|---|
| `review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md` | NEW (design comm) |
| **Total** | **1 file** ✓ |

Zero `scripts/`, `river-rats-core/`, `prompts/`, `data/` edits ✓.

## Audit 2 — Citation existence ✅ CLEAN

3 distinct cited paths:

| Citation | Status |
|---|---|
| `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | ✅ TRACKED |
| `prompts/gto_labeller_v3.4.md` | ✅ TRACKED |
| `prompts/gto_labeller_v3.X.md` | NOT-TRACKED ✓ expected — **placeholder for "next protocol version" if cascade Surface 3 (prompt rules) requires update; design recommends NO PROMPT CHANGE so this is forward-looking** |

The `v3.X.md` reference is a placeholder citation — the design itself recommends NO prompt change in §3 / §5.3 (line 173: "Recommendation: NO PROMPT CHANGE. The 3 new features are MODEL-side discriminators, not labeller-side bucket-reasoning rules"). NOT-TRACKED is correct + expected.

## Audit 3 — Cascade scope completeness ✅ CLEAN — all 5 points addressed

**Dispatch:** *"verify all 5 cascade points addressed per `feedback_attention_flags_when_features_change.md`: raw feature + attention vocab + prompt rules (if applicable) + capture pipeline + trainer"*

Design §5 (lines 155+) enumerates all 5 surfaces:

| Cascade surface | 12.5J-A coverage | Status |
|---|---|---|
| **Surface 1: Raw feature** | `feature_keys.py` + `feature_extractor.py` + `FEATURE_COLUMNS` (length 59 → 62) | ✓ |
| **Surface 2: Attention vocabulary** | `assemble_pilot_data.py` + related attention-flag scripts; new attention vocab entries | ✓ |
| **Surface 3: Prompt rules** | `prompts/gto_labeller_v3.X.md` — design recommends NO change (features are model-side); recommendation explicit | ✓ (acknowledged with reasoned "no change" decision) |
| **Surface 4: Capture pipeline** | Re-run `extract_all_features(hand_dict)` with 62-feature surface; ~1-2 hours runtime | ✓ |
| **Surface 5: Trainer** | `STUDENT_FEATURE_COLUMNS_V9` extended 59 → 62; pre-pad metadata-only continues | ✓ |

§"Risk 3: cascade scope 5-point review" (line 247) explicitly cross-references the memory + confirms 12.5J-B through 12.5J-E phases enforce per-surface delivery.

**Cascade scope: CLEAN.** All 5 surfaces explicitly addressed; "no prompt change" is a reasoned decision not an omission.

## Audit 4 — Feature design specificity ✅ CLEAN

**Dispatch:** *"verify MW-17 axis (implied-odds + nut-blocker-with-overcards) + MW-47 axis (SUITED-NFD-bet+call-multiway raise pressure) have concrete computation specs, not handwave"*

### MW-17 axis (2 candidate features)

| Candidate | Feature | Formula / spec | Discriminative on MW-17 |
|---|---|---|---|
| Candidate 1 | `implied_outs` | overcards above board high-card count | AdKs on Jd8d4c → 6 implied outs (line 62) |
| Candidate 2 | `blocker_overcard_count` | overcards × `nut_flush_block` count | AdKs on Jd8d4c → 2 (line 76) |

Both have explicit computation formulas + discriminative-on-MW-17 calculation. Recommended both candidates.

Plus optional Candidate 3 (more aggressive): `effective_pot_odds` reduced by `(1 + nut_blocker_overcard_count × 0.05)` premium factor; gives effective_pot_odds=0.334 from raw_pot_odds=0.367 on MW-17. Trade-off documented (over-fitting risk; not recommended).

### MW-47 axis (1 candidate feature)

| Candidate | Feature | Formula / spec | Discriminative on MW-47 |
|---|---|---|---|
| Candidate above | bet+call-multiway-OOP raise pressure index | Boolean-gated: 1.0 base + 0.3 (NFD+nut blocker) - 0.2 (raise risk) = **1.1** | All conditions satisfied → 1.1 (line 140) |

Concrete formula + boolean gate definitions + discriminative calculation. Trade-off documented (boolean-gated returns 0 most of time; mitigation via cross-seed importance reporting).

**Feature design specificity: CLEAN.** All 3 candidates have concrete computation specs (no handwave); trade-offs documented.

## Audit 5 — Direction-X-retro acknowledgment ✅ CLEAN

**Dispatch:** *"verify design explicitly notes Path Y boundary relaxation (owner approved at 12.5H-F gate)"*

Design §2 explicitly titled **"Direction-X-retro scope warning"** (line 21+).

Design §1 line 19 cites: *"Direction-X-retro scope (Path Y intentionally relaxed; owner approved at 12.5H-F)"*.

§5 cascade scope explicitly enumerates the source-surface edits Path Y previously prohibited (`feature_extractor.py`, `feature_keys.py`, `gto_model.py FEATURE_COLUMNS`, `train_model_v9_student.py STUDENT_FEATURE_COLUMNS_V9`).

**Direction-X-retro acknowledgment: CLEAN.** Path Y boundary relaxation documented with explicit owner-approval citation + scope enumerated.

## Test class implication

- **TC-23 1-file design-only audit pattern reproducible** (parallel with PR #197)
- **Cascade scope completeness pattern** — when feature engineering adds raw features, QC verifies all 5 cascade points addressed per `feedback_attention_flags_when_features_change.md`. Pattern formalized for future Direction-X-retro-scope cycles.
- **Direction-X-retro acknowledgment pattern** — explicit Path Y relaxation + owner-approval citation in design = reviewable scope. Pattern reproducible.
- **"Feature is model-side discriminator, not labeller-side rule"** — clean reasoning for NO prompt change. Future feature-engineering designs can cite this as precedent.

## What QC did NOT audit (scope partition)

- **GTO correctness of feature formulas** — gto-expert / ml-architect at 12.5J-B implementation phase
- **Cross-seed importance prediction** for the 3 candidates (will they activate ≥0.02 floor?) — empirical question for 12.5K combined re-train
- **Path Y relaxation downstream consequences** (does relaxing Path Y open scope creep?) — orchestrator scope; design's §"Risk" sections address this
- **Whether 3 features is the right candidate-set size** vs e.g. 5 or 1 — orchestrator/owner WHAT decision

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **16th successive cycle solo-routed**. **First parallel-PR audit cycle** alongside PR #197 (12.5I-A corpus design).

## References

- PR #198: https://github.com/beytell1-sketch/river-rats-v2/pull/198
- QC audit trigger (combined): master `ce2ee5e` (PR #199)
- 12.5J dispatch: master `c536c30` (PR #196)
- 12.5I-pre diagnostic (MW-17/47 E-FEATURE primary verdicts): master `54e2943` (PR #193)
- 12.5H-F synthesis (owner approved Direction-X-retro at E option): master `ea642ed` (PR #191)
- Memory: `feedback_attention_flags_when_features_change.md` (cascade scope), `feedback_qc_routing_when_standalone_active.md` (16th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #198 for merge.** All 5 audits PASS cleanly; 0 NIT new findings.

QC-side gate cleared. Awaiting orchestrator merge → 12.5J-B feature implementation dispatch.
