---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #213 (12.5I-C labelling round, 5 Sonnet × 94 hands, v3.4) — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
severity: PASS (clean across all 7 dispatch audits)
status: FLAG → APPROVE for merge
test-class: TC-23 strict-scope + V-Source citation existence + G2 distribution sanity + cost-cap reconciliation + manual-canonical verdict + MW-25 4-source convergence + MW-40 graduation-candidate scope-discipline
multi-expert verdict: SOLO (19th successive cycle)
---

# QC Finding — PR #213 (12.5I-C labelling round): PASS; 0 findings

## Verdict

**PASS PR #213 for merge.** 7 audits (3 standard + 1 cost + 1 canonicals + 2 NEW graduation-evidence audits) processed; all clean.

## 7-audit summary

| # | Audit | Result |
|---|---|---|
| 1 | Diff scope strict | ✅ Exactly 3 files (2 jsonl + 1 builder report). No drift outside scope. |
| 2 | Citation existence | ✅ 470/470 raw rows declare `protocol_version="v3.4"` + `model="claude-sonnet-4-6"`; spot-check 5 hands × 5 labellers all reference v3.4 structure (Step 1/2/3, KB §1.7, DO NOT Rule N, Rule 11). 0 refusals. |
| 3 | Label distribution sanity (G2) | ✅ Bucketed by feature signature: T8' family 30 CHECK; T9' family 32 BET + 1 CHECK; T10' family 27 RAISE + 2 CALL + 2 FOLD. Matches report exactly. |
| 4 | Cost reconciliation | ✅ ~$3.30 reported (2.75% of $120 cap). Pilot $0.30 + Step 1 $0.85 + Step 2 $2.15 plausible for 470 Sonnet calls. |
| 5 | Manual canonicals vs predictions | ✅ PILOT_785 (MW-25 EXACT) CHECK 1.0 ✓, PILOT_786 (T8' adj) CHECK 1.0 ✓, PILOT_787 (MW-40 EXACT) CHECK 0.6 ✗ predicted-BET (1 ≤ 1 STOP threshold), PILOT_788 (MW-45 ADJ) RAISE 0.8 ✓. |
| 6 | MW-25 graduation evidence (NEW) | ✅ 4-source convergence documented; T8' rows uniformly CHECK / 1.0 (28 parametric + 2 canonicals = 30/30). |
| 7 | MW-40 graduation candidate (NEW) | ✅ Report § "MW-40 graduation candidate" surfaces PILOT_787 + recommends Opus tier-up; diff strict — builder did NOT touch BATCH2 reference, stay-wrong list, `memory/reference_corrections.md`, or v3.x prompts. |

## Audit 3 — distribution detail

Bucketing confusion note: pilot_hand_id ranges do NOT align with templates (PILOT_695-722 = T8' parametric flush draws; PILOT_723-754 = T9'-e parametric TPWK; PILOT_755-784 = T10'-r parametric sets; PILOT_785-788 = manual canonicals). Initial range-based bucketing flagged a false-positive HIGH (PILOT_723/724 BET) — investigation confirmed those are TPWK hands in T9'-e family, not T8'. Re-bucketed by `feat_dict.has_flush_draw + is_made_hand + is_strong_made` signature; results match report exactly.

| Family | Bucket method | n | Distribution |
|---|---|---|---|
| T8' (parametric + 2 canonicals) | has_flush_draw=1, is_made_hand=0 (+ canonical IDs 785/786) | 30 | 30 CHECK 1.0 |
| T9' (parametric + 1 canonical) | is_made_hand=1, is_strong_made=0 (+ canonical ID 787) | 33 | 32 BET 0.6 + 1 CHECK 0.6 |
| T10' (parametric + 1 canonical) | is_strong_made=1 OR is_monster=1 (+ canonical ID 788) | 31 | 27 RAISE + 2 CALL + 2 FOLD |
| **Total** | | **94** | matches |

## Audit 5 — manual canonical detail

| pilot_hand_id | template | predicted | consensus | conf | divergent? | votes |
|---|---|---|---|---|:---:|---|
| PILOT_785 | MW-25 EXACT | CHECK (post-PR #209 flip) | CHECK | 1.0 | ✓ match | 5/5 CHECK |
| PILOT_786 | T8' adjacent | CHECK | CHECK | 1.0 | ✓ match | 5/5 CHECK |
| PILOT_787 | MW-40 EXACT | BET | CHECK | 0.6 | ✗ DIVERGENT | 3 CHECK / 2 BET |
| PILOT_788 | MW-45 ADJ | RAISE | RAISE | 0.8 | ✓ match | 4 RAISE / 1 CALL |

1 divergence ≤ 1 dispatch STOP threshold. PILOT_787's 3-2 CHECK majority is the soft signal that drives Audit 7 (MW-40 graduation candidate).

## Audit 6 — MW-25 graduation evidence (4-source convergence)

| Source | Verdict on MW-25 / T8'-r | Confidence |
|---|---|---|
| 12.5I-C pilot (PR #208) | 5/5 CHECK | 5 hands × 1 labeller |
| Opus 4.7 gto-expert re-eval (PR #209) | CHECK HIGH | orchestrator-side |
| 12.5I-C Step 1 (this PR) | 30/30 CHECK 1.0 unanimous | 30 hands × 5 labellers = 150 calls |
| v3.4 protocol traces (KB §1.7 + DO NOT Rule 2) | uniform CHECK | reasoning citations across all 5 labellers on every T8' hand |

Empirically: BATCH2 MW-25 reference (BET HIGH on Ks7s/As9s5d 4-way checked-through-multiway) is GTO-incorrect under v3.4 protocol; CHECK is GTO-correct. **Evidence sufficient for owner-scope graduation decision** (orchestrator silent-default Option α per PR #209 = update BATCH2 reference + add to `memory/reference_corrections.md`).

QC does not decide reference correctness (owner-scope per `feedback_orchestrator_decides_not_recommends.md`); QC verifies the evidence chain is intact and the dispatch's 4-source convergence claim is empirically supported. **It is.**

## Audit 7 — MW-40 graduation candidate scope-discipline

Builder report § "MW-40 graduation candidate (NEW)" correctly:
- Surfaces PILOT_787 CHECK 0.6 finding with 3-2 split documented (L3/L4/L5 CHECK, L1/L2 BET)
- Notes echo of MW-25 pattern (parametric variants soft-BET vs EXACT canonical CHECK)
- Recommends Opus tier-up cross-check (~$5, mirrors MW-25 pathway from PR #209)
- Lists 3 orchestrator options (Opus tier-up / defer to 12.5L / drop T9'-e) with explicit slow-quality-default favoring Option 1

Crucially the diff is **strict 3 files** — builder did NOT silently:
- Update BATCH2 MW-40 reference (`design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` — untouched)
- Add MW-40 to `memory/reference_corrections.md` (untouched)
- Modify v3.x prompts (untouched)
- Modify stay-wrong list (untouched)

Reference-correctness decisions remain owner-scope. Builder report explicitly cites `feedback_orchestrator_decides_not_recommends.md`. Clean.

## Process observation

**19th successive solo-routed cycle.** Loop heartbeat detected dispatch within ~3 min (Monitor `bssngxfls` armed 15:35:22Z; QC_DISPATCH event 15:38:25Z; this audit response ~15:50Z). Wall-clock improvement vs prior pattern is from the just-installed dynamic-loop Monitor (this session set it up at owner direction at 15:35Z; first event detected at 15:38Z).

## False-positive avoided + lesson

Initial bucketing by `pilot_hand_id` range produced a false-positive HIGH (alleged 2 non-CHECK on T8'-r). Re-bucketing by feature signature corrected it. **Lesson for QC procedure:** for label-distribution audits on parametric corpora, bucket by `feat_dict` signature, not `pilot_hand_id` range, since templates do not necessarily occupy contiguous ID ranges (in this case canonicals at 785-788 are at the tail; parametrics are not 30/33/30 across 695-784 by 30-hand stride).

Adding to QC `learning/incident_pattern_library.md` as a procedural guard rule (not a project incident).

## Test class implications

- **TC-23 strict-scope (training-data variant)** — third activation (PR #181 12.5H-C labelling, PR #202 12.5I-B situation, this PR). Pattern stable across data PRs.
- **G2 distribution sanity** — first activation with feature-signature bucketing (vs ID-range bucketing). Procedure-update logged.
- **MW-XX graduation 4-source convergence** — first activation as a NEW audit class (Audit 6 MW-25). Pre-merge gate evidence-chain integrity check pattern. Would re-fire if/when MW-40 reaches similar convergence.
- **Owner-scope file scope discipline** — first explicit pre-merge audit checking reference set + stay-wrong + prompt files are untouched. Worth promoting to a standing TC-X test class for any data PR that surfaces graduation evidence; could become **TC-X-OWNER-SCOPE-DISCIPLINE**.

## What gates on this audit

Per dispatch:
- PR #213 merge → **on this PASS** + orchestrator-side Opus tier-up cross-check (post this audit, on MW-40 PILOT_787)
- 12.5I-D corpus QC dispatch → on PR #213 merge
- MW-40 Opus tier-up → orchestrator runs after this verdict
- 12.5K combined re-train → on 12.5I-E + 12.5J-E ship

## Full evidence

`~/river-rats-qc/findings/2026-05-06-pr213-12.5I-C-labelling.md`

## References

- PR #213 head: `5cfa5c1`
- PR #213 base (master): `077c168`
- QC audit trigger: PR #211 (master `cef0c61`) → comm `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR213_2026-05-06.md` at master `0b77bdd`
- 12.5I-C MW-25 resolution: master `077c168` (PR #209)
- 12.5I-C pilot HALT: master `52e5164` (PR #208)
- 12.5H-C precedent (label PR audit pattern): master `90e17dc` (PR #181)
- v3.4 protocol: `prompts/gto_labeller_v3.4.md`
- BATCH2 reference (untouched, owner-scope): `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`
- Prior cycle: `~/river-rats-qc/findings/2026-05-06-pr205-12.5J-B-feature-implementation.md`
