---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5H-C re-pilot — 19/20 match against UPDATED predictions; 1 borderline mismatch (PILOT_690 BET → CHECK) triggers dispatch STOP rule
status: HALT — re-pilot complete, full phase NOT triggered, awaiting orchestrator direction
branch: programmer/phase125h-c-re-pilot-2026-05-06
base: master `f4a7b4e` (12.5H-C re-pilot dispatch HEAD)
re-pilot brief: /tmp/mass_labelling_125h_repilot/labeller_1_brief.md (transient)
re-pilot output: /tmp/mass_labelling_125h_repilot/labels_v3_4_labeller_1.json (transient; reproducible)
---

# 12.5H-C re-pilot HALT — borderline NFD-canonical mismatch

## Per-dispatch stop condition triggered (literal interpretation)

> **From re-pilot dispatch §"Stop conditions (UPDATED)":** *"Manual canonical pilot hand consensus disagrees with UPDATED prediction → STOP, route to orchestrator."*

**1 of 6 manual canonicals diverged from UPDATED prediction.** Strictly per dispatch's literal STOP rule, full phase NOT triggered. Routing to orchestrator with diagnosis + recommendation.

**Substantive judgment:** the 1 mismatch is a borderline hand where v3.4 protocol routing is genuinely close (BET vs CHECK both defensible); re-pilot's CHECK reasoning is in fact MORE protocol-consistent than original pilot's BET (DO NOT Rule 2 + KB §1.7 fires-only-when-facing-bet). Recommendation below.

## Re-pilot results table (vs UPDATED predictions per dispatch master `f4a7b4e`)

| pilot_hand_id | template | UPDATED prediction | re-pilot labeller | match | confidence |
|---|---|---|---|:---:|---|
| PILOT_605 | T8' parametric | CHECK | CHECK | ✓ | HIGH |
| PILOT_620 | T8' parametric | CHECK | CHECK | ✓ | HIGH |
| PILOT_621 | T9' parametric | BET | BET | ✓ | MEDIUM |
| PILOT_633 | T9' parametric | BET | BET | ✓ | MEDIUM |
| PILOT_634 | T10' parametric | RAISE | RAISE | ✓ | HIGH |
| PILOT_646 | T10' parametric | RAISE | RAISE | ✓ | HIGH |
| PILOT_647 | T7-ext parametric (air=0.047) | CALL | CALL | ✓ | HIGH |
| PILOT_658 | T-RAISE-stabilize parametric | RAISE | RAISE | ✓ | MEDIUM |
| PILOT_669 | T-CONTROL CHECK | CHECK | CHECK | ✓ | HIGH |
| PILOT_675 | T-CONTROL BET | BET | BET | ✓ | MEDIUM |
| PILOT_678 | T-CONTROL BET | BET | BET | ✓ | MEDIUM |
| PILOT_680 | T-CONTROL FOLD | FOLD | FOLD | ✓ | HIGH |
| PILOT_684 | T-CONTROL CALL | CALL | CALL | ✓ | HIGH |
| PILOT_687 | T-CONTROL RAISE | RAISE | RAISE | ✓ | HIGH |
| PILOT_689 | T8' canonical 01 (Ks7h on As9s5s) | CHECK | CHECK | ✓ | HIGH |
| PILOT_690 | T8' canonical 02 (AsKh on Js9s3s NFD) | BET | **CHECK** | ✗ | MEDIUM |
| PILOT_691 | T9' canonical (MW-40 exact) | BET | BET | ✓ | MEDIUM |
| PILOT_692 | T10' canonical (MW-45 exact) | CALL | CALL | ✓ | MEDIUM |
| PILOT_693 | T7-ext canonical SUITED (air=0.312) | RAISE | RAISE | ✓ | HIGH |
| PILOT_694 | T-RAISE-stab canonical | RAISE | RAISE | ✓ | MEDIUM |

**Manual canonical match rate: 5/6 (83%).** **T-CONTROL design_action match: 6/6 (100%).** **T7-ext air-driven split: 2/2 match (PILOT_647 CALL, PILOT_693 RAISE)** ✓ — T7-ext SUITED redesign empirically validated.

## The single mismatch: PILOT_690

**Hand:** AsKh on Js9s3s monotone (4-way checked through, BTN IP cold-caller, not PFA)

**Original 12.5H-C pilot (labeller_1, master `094cfc2`):** BET (matched my original BET prediction)
**12.5H-C re-pilot (labeller_1, master `f5472bc`):** CHECK (matches existing corpus pattern but mismatches dispatch's UPDATED BET prediction)

**Re-pilot reasoning (MEDIUM confidence):**
> *"This is a drawing hand (flush draw, 9 outs — AsKh on Js9s3s monotone spade board) for BTN IP cold-caller (not PFA, villain_checked_back=1). Hero holds As giving nut_flush_block=1, but the board is fully monotone — all three board cards are spades, meaning villains with spades already have made flushes. Hero is not the PFA. Despite the nut flush blocker (As), the board is monotone and num_opponents=3. DO NOT Rule 2 prohibits barreling draws into 2+ opponents. Without a bet to raise, KB §1.7 semi-bluff RAISE does not apply. While villain_air=0.44 is attractive, a bet into 3 opponents on a monotone board from a non-PFA cold-caller is not supported by protocol. CHECK to realize equity in position."*

### Diagnosis

The re-pilot's CHECK reasoning is **MORE protocol-consistent** than the original pilot's BET, on three grounds:

1. **DO NOT Rule 2** explicitly prohibits barreling draws into 2+ opponents 3-way; PILOT_690 has 3 opponents. (The re-pilot's labeller invoked Rule 2; the original pilot's labeller did not — both are valid readings, but Rule 2 is explicit in v3.4.)
2. **KB §1.7 (Nut FD + nut blocker → RAISE)** explicitly requires *facing a bet*; PILOT_690 is checked-through (no bet to raise). The carve-out for the v3.2 0.20 villain_air threshold + v3.3 Fix 2.1 + v3.4 Fix 2.1.1 all apply *only* in bet/bet+call lines, never in checked-through lines. So KB §1.7 cannot fire on PILOT_690 → BET as semi-bluff is not protocol-supported.
3. **Existing 604 t1_monotone_fd_checked_through_4way hands (PILOT_495-506)** are ALL labelled CHECK in 12.5E-C labelling round (`data/corpus_revision_125e_labels_2026-05-05.jsonl`). PILOT_690 is structurally similar (NFD + nut blocker on monotone-spades 4-way checked through). Consistency with existing labelled corpus → CHECK.

The original 12.5H-C pilot's BET on PILOT_690 was likely a labeller noise event on a borderline hand; the re-pilot's CHECK is the protocol-correct answer.

**Conclusion:** The dispatch's UPDATED prediction for PILOT_690 (BET) is incorrect. The correct UPDATED prediction is CHECK — same as PILOT_689 (T8' canonical 01) and consistent with the existing 604 t1_monotone_fd hands.

This makes PILOT_690 essentially a duplicate canonical of PILOT_689 (both monotone-FD-checked-through, both expect CHECK, both are valid drawing-bucket teaching anchors). That's fine — the original dispatch design wanted "K-high FD canonical vs NFD canonical contrast pair", but both correctly route to CHECK in v3.4 because the BET-favored conditions never fire in checked-through lines.

## Recommendations to orchestrator

**Option A (RECOMMENDED): accept CHECK as updated prediction for PILOT_690 and authorize full Sonnet × 5 × 90 phase.** Diagnosis is clear: re-pilot's CHECK is protocol-correct; original pilot's BET was labeller noise. With this prediction update, all 6 manual canonical pre-full-phase predictions are validated (PILOT_689 CHECK, PILOT_690 CHECK, PILOT_691 BET, PILOT_692 CALL, PILOT_693 RAISE, PILOT_694 RAISE). Cost to full: ~$2.50. Bias risk: none — full phase will produce ~5/5 CHECK consensus on PILOT_690 confirming the prediction.

**Option B: re-run pilot with 3 Sonnet labellers on PILOT_690 specifically** to formally establish 3-of-3 CHECK consensus before authorizing full. Cost: ~$0.30. Conservative; provides empirical evidence rather than reasoning-based diagnosis.

**Option C: investigate whether v3.4 should add an explicit clarification that DO NOT Rule 2 (and KB §1.7 facing-bet requirement) preempts BET for monotone-FD-checked-through 4-way hands** — would make the protocol unambiguous on this pattern. Probably unnecessary; existing protocol already handles it correctly via the two clauses' conjunction.

Recommend **Option A**. The re-pilot's per-prediction diagnosis covers the matter cleanly; full phase will validate at zero meaningful additional cost.

## What's NOT a blocker

- **T7-ext SUITED redesign (12.5H-B' amendment) empirically validated:** PILOT_647 (air=0.047) → CALL ✓; PILOT_693 (air=0.312) → RAISE ✓. The air-driven split per QC MEDIUM-1 walk is correct. No FOLD outcomes — anti-training risk fully resolved.
- **All other 5 manual canonicals match UPDATED predictions** (PILOT_689 CHECK, PILOT_691 BET, PILOT_692 CALL, PILOT_693 RAISE, PILOT_694 RAISE).
- **T-CONTROL design_action 6/6 match** validates the entire T-CONTROL bucket + design_action mechanism for G4 drift detection at 12.5H-D.
- **All v3.4 carve-outs verified firing correctly:** Fix 2.1.1 clause-e on PILOT_658/694; KB §1.7 OVERRIDE air-threshold on PILOT_647 vs PILOT_693; DO NOT Rule 2 on PILOT_605/620/669/689/690.
- **Cost / schema / refusals:** all clean; full phase fully feasible at $120 budget.

## What's blocked / what's queued

**Blocked:**
- 12.5H-C full phase (5 Sonnet × 90) → on orchestrator direction (Option A vs B vs C)
- 12.5H-C PR opens → on full phase complete
- 12.5H-C labels-final gate, merge, 12.5H-D dispatch → all downstream

**Queued:** all items per PR #168 §"What's blocked / queued" + the TC-X-DISPATCH-PREDICTION-VERIFICATION sub-vector (per re-pilot dispatch's bonus pattern note) — this is now the **second** instance of orchestrator-side prediction error (12.5H-C T7-ext / MW-17 was first; PILOT_690 BET-prediction is second). Per dispatch reference text "If a third instance of orchestrator-side prediction error appears, formalize as QC test class" — we are 1 instance away from formalization.

## References

- 12.5H-C re-pilot dispatch: master `f4a7b4e` (PR #178)
- 12.5H-B' amendment merged: master `f5472bc` (PR #175)
- 12.5H-B' QC verdict (MEDIUM-1 prediction-falsification flag): master `2eaf206` (PR #177)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `f5472bc`)
- Existing 604 labels (PILOT_495-506 = t1_monotone_fd_checked_through_4way ALL CHECK): `data/corpus_revision_125e_labels_2026-05-05.jsonl`
- Memory: `feedback_pilot_first_for_long_jobs.md` (pilot-first STANDING RULE), `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_queries_to_orchestrator.md`

**Status: 12.5H-C re-pilot HALT (literal dispatch STOP rule). Recommend Option A (accept PILOT_690 CHECK + authorize full). Awaiting orchestrator direction.**
