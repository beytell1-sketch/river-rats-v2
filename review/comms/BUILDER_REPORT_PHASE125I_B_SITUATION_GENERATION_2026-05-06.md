---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5I-B — situation generation (94 hands across 3 redesigned templates targeting MW-25/40/45)
status: REPORT — PR open, ready for QC trigger
branch: programmer/phase125i-b-situation-generation-2026-05-06
base: master `3b31f2a`
---

# 12.5I-B builder report — situation generation (94 hands)

## Summary

94 new situations factory-generated across 3 redesigned templates per
12.5I-A design (`PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md`,
master `d045b03`). pilot_hand_id range PILOT_695..PILOT_788, zero
collisions vs existing 694-hand combined corpus. All G1-G3 PASS.

90 parametric + 4 manual = 94 hands. Combined corpus post-12.5I-merge
will be 694 + 94 = 788 hands.

12.5I-B is parallel with 12.5J-B (feature implementation; separate PR).
Combined re-train at 12.5K when both 12.5I-E and 12.5J-E ship.

## Files in PR diff (exactly 4)

1. `scripts/build_corpus_revision_125i_situations.py` (NEW) — factory + 3 redesigned template classes (`T8PrimeRedesigned`, `T9PrimeExpanded`, `T10PrimeRedesigned`) + 4 inline manual canonicals + G1-G3 self-checks. Reuses helpers from `scripts/build_corpus_revision_125e_situations.py`.
2. `data/corpus_revision_125i_situations_2026-05-06.jsonl` (NEW; 90 rows) — parametric situations PILOT_695..PILOT_784.
3. `data/corpus_revision_125i_manual_canonicals_2026-05-06.jsonl` (NEW; 4 rows) — manual canonical hands PILOT_785..PILOT_788. GTO-EXPERT review fires at 12.5I-C dispatch.
4. `review/comms/BUILDER_REPORT_PHASE125I_B_SITUATION_GENERATION_2026-05-06.md` (NEW; this file).

## Per-template count table

| Template | Parametric | Manual | Total | Design §4 target |
|---|---:|---:|---:|---:|
| T8'-redesigned (MW-25 family — non-nut FD checked-through 4-way) | 28 | 2 | 30 | 30-35 |
| T9'-expanded (MW-40 family — TP-medium-kicker IP 4-way after PFR check) | 32 | 1 | 33 | 32-33 |
| T10'-redesigned (MW-45 family — slowplay set + broadway-completed turn) | 30 | 1 | 31 | 28-32 |
| **Total** | **90** | **4** | **94** | 90-103 |

All per-template counts within ±2 of design §4 (G2 tolerance).

## G1-G3 self-check results

```
G1 PASS: 94 unique pilot_hand_ids; 0 collisions vs existing 694
G2 PASS: T8primeR=30/30, T9primeE=33/33, T10primeR=31/31
G3 PASS: 0 (board, hero_cards, hero_position, prior_actions) duplicates internal or vs existing 694
```

`scripts/build_corpus_revision_125i_situations.py --strict` exits 0.

### G3 dedup notes

Initial run found 1 internal collision (T8'-redesigned canonical 02 duplicated parametric #1 on the same `9c8c on Kh4c2c` fingerprint) and 1 cross-corpus collision (T10'-redesigned canonical was a literal MW-45 exact replica `6d6c on AcKd6hQs` which already existed as PILOT_692 in 12.5H). Resolutions:

- T8'-redesigned canonical 02 changed to `Tc9c on Qh5c3c` (different texture; preserves discriminative axis).
- T10'-redesigned canonical 01 changed from "MW-45 exact replica" to "MW-45 family suit-rotated" (`6d6s on AsKh6cQd`) — the literal MW-45 hand is already PILOT_692 in the combined corpus; including the same fingerprint twice would be wasted training data. Suit rotation preserves the AKx-broadway-completed-turn axis with a unique fingerprint.

## Discriminative axis verification (spot-checks)

| pilot_hand_id | template | hero | board | hand_cat | made | monster | FD | nut_blk | villain_agg | checked_back | raw_eq |
|---|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|
| PILOT_695 | T8'-redesigned (parametric #1) | 9c8c | Kh4c2c | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0.281 |
| PILOT_725 | T9'-expanded (parametric #1) | AhTd | As7c2d | 6 | 1 | 0 | 0 | 0 | 0 | 1 | 0.347 |
| PILOT_758 | T10'-redesigned (parametric #1) | 6h6d | AcKh6cQs | 12 | 1 | 1 | 0 | 0 | 1 | 0 | 0.506 |
| PILOT_785 | T8' canonical 01 (MW-25 exact) | Ks7s | As9s5d | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0.355 |
| PILOT_786 | T8' canonical 02 (non-nut FD contrast) | Tc9c | Qh5c3c | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0.300 |
| PILOT_787 | T9' canonical (MW-40 exact) | AhTs | AdJc5h | 6 | 1 | 0 | 0 | 0 | 0 | 1 | 0.215 |
| PILOT_788 | T10' canonical (MW-45 adjacent) | 6d6s | AsKh6cQd | 12 | 1 | 1 | 0 | 0 | 1 | 0 | 0.515 |

All discriminative axes match design §3 specifications.

### Note: PILOT_787 fixes 12.5H PILOT_691's texture defect

12.5H PILOT_691 used board `AcJc5d` which is 2-tone clubs (not rainbow per MW-40 reference spec `AdJc5h`). 12.5I PILOT_787 uses the literal MW-40 reference board `AdJc5h` (rainbow s-c-h actually d-c-h). This brings the canonical into compliance with the BATCH2 reference set spec. Not a fingerprint conflict with PILOT_691 since boards differ.

## Hero-only convention verification

All 94 rows have `prior_actions` filtered to hero-only entries via `_hero_only_prior_actions` (reused from 12.5E-B factory line 119). 0 violations.

## design_action verification

12.5I-B does NOT include T-CONTROL-style hands per 12.5I-A design §4 (no design_action requirement for T8'-r/T9'-e/T10'-r). 0 design_action fields expected; 0 present.

## gto-expert-hat self-review (4 manual canonicals)

### PILOT_785 — T8'-redesigned canonical 01 (MW-25 exact replica: Ks7s on As9s5d)

- composition: K-high spade FD (1 hole spade Ks + 3 board spades) + no overcards (As is on board, 9 below K, 5 below K)
- board texture: monotone spades A-9-5; As public → hero K-spade dominated by any villain holding any spade
- expert per BATCH2 reference: BET HIGH ("strong flush draw with three opponents who all checked")
- expected v3.4 routing: CHECK (per 12.5H PILOT_689 same monotone+As-public pattern; DO NOT Rule 2 + KB §1.7 facing-bet requirement preempt BET)
- **VERDICT: This canonical is the protocol-vs-reference disagreement anchor.** The labelling round at 12.5I-C MUST verify whether v3.4 produces BET (matches BATCH2 reference) or CHECK (matches 12.5H precedent). On CHECK consensus, route to orchestrator with the open question raised in 12.5I-A §9 (BATCH2 MW-25 reference re-evaluation).

### PILOT_786 — T8'-redesigned canonical 02 (non-nut-FD contrast: Tc9c on Qh5c3c)

- composition: clubs FD (2 hole clubs Tc+9c + 1 board club 5c... wait that's only 3 clubs)

**HOLD — feature mismatch detected.** Tc9c on Qh5c3c: hero has Tc + 9c (2 clubs); board has Qh (heart) + 5c + 3c (2 clubs). Total clubs = 4 → has_flush_draw=1 ✓. Verified above (PILOT_786 spot-check shows FD=1, eq=0.300). Discriminative axis intact.

- board texture: 2-tone clubs Q-high; hero non-nut FD with no overcards above the Q (T+9 both below Q)
- expert per design §3 prediction: BET (denial + thin value via fold equity from three checks)
- expected v3.4 routing: uncertain — DO NOT Rule 2 may fire (3-way semi-bluff into multiway); pilot phase verifies
- **VERDICT: PASS for situation generation; protocol routing uncertainty is a 12.5I-C gate concern, not 12.5I-B.**

### PILOT_787 — T9'-expanded canonical (MW-40 exact: AhTs on AdJc5h)

- composition: TP T-kicker on rainbow A-J-5
- board texture: rainbow d-c-h (corrected from 12.5H PILOT_691's 2-tone-clubs AcJc5d)
- expert per BATCH2 reference: BET MEDIUM
- expected v3.4 routing: BET (per existing 12.5H T9' precedent — 14/14 BET unanimous in 12.5H-C labelling)
- **VERDICT: PASS — same as 12.5H PILOT_691 family with corrected rainbow texture.**

### PILOT_788 — T10'-redesigned canonical (MW-45 adjacent: 6d6s on AsKh6cQd)

- composition: bottom set (6d+6s pair with board 6c) on rainbow A-K-6 flop; turn Q completes broadway (JT straight)
- board texture: rainbow s-h-c-d (broadway-completed turn)
- expert per BATCH2 reference (MW-45 axis): RAISE HIGH (set + protect vs straight-completed range; MW-33 anchor)
- expected v3.4 routing: RAISE (per 12.5H T10' parametric 13/13 RAISE + PILOT_692 5/5 RAISE in 12.5H-C full phase)
- **VERDICT: PASS — suit-rotated to avoid PILOT_692 fingerprint duplicate; preserves MW-45 family discriminative axis.**

### Self-review summary

3 of 4 canonicals PASS internal gto-expert hat self-review. 1 (PILOT_785, T8' MW-25 exact) is intentionally the protocol-vs-reference disagreement anchor; pilot phase must verify which prediction wins. GTO-EXPERT review at 12.5I-C dispatch will be the binding gate.

## Pre-flight verification (architect hat)

- `scripts/build_corpus_revision_125e_situations.py` exists at master HEAD (1796 lines; helpers verified)
- `data/corpus_combined_694_2026-05-06.jsonl` exists (694 rows; G1+G3 reference)
- `data/corpus_combined_694_labels_2026-05-06.jsonl` exists (694 rows)
- `prompts/gto_labeller_v3.4.md` exists (untouched)
- `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` exists (MW-25/40/45 references checked)

No drift found vs design.

## Stop conditions checked

- ✅ Pre-flight: no drift vs design
- ✅ Per-template counts: all within design §4 tolerance (Δ within ±2)
- ✅ G1/G2/G3: all PASS
- ✅ Hero-only convention uniform: 0 violations across 94 rows
- ✅ No solver call: factory uses only feature_extractor
- ✅ Diff: exactly 4 files

## Open question carried forward from 12.5I-A §9

**MW-25 BET expert may itself be GTO-incorrect.** Per 12.5I-pre diagnostic: v3.4 + 12.5H corpus + model all align on CHECK on the MW-25 pattern. PILOT_785 (T8' canonical 01) is the literal MW-25 hand; the 12.5I-C labelling round will produce a definitive label. If labellers consensus to CHECK (matching 12.5H precedent), the open question becomes urgent: orchestrator should commission gto-expert reference re-evaluation to determine whether MW-25 should be CHECK in BATCH2 (in which case MW-25 graduates from stay-wrong list at zero corpus cost — the 30 T8'-redesigned hands become "extra training signal for non-nut-FD-checked-through" but don't move MW-25 specifically).

## What's blocked / what's queued

**Blocked:**
- 12.5I-B QC trigger → on this PR open
- 12.5I-C labelling dispatch → on QC APPROVE
- Subsequent 12.5I phases → on prior phase merge

**Parallel (independent of 12.5I):**
- 12.5J workstream (feature engineering for MW-17/47) — separate PR cycle
- 12.5K combined re-train — fires AFTER both 12.5I-E and 12.5J-E ship

## References

- 12.5I-B dispatch: master `3b31f2a` (PR #201)
- 12.5I-A merged: master `d045b03` (PR #197)
- 12.5I-pre diagnostic: master `54e2943` (PR #193)
- 12.5H-B (structural template): master `094cfc2` (PR #169)
- 12.5J-B parallel dispatch: master `3b31f2a` (PR #201)
- BATCH2 reference set: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`
- Existing 694 combined corpus: `data/corpus_combined_694_2026-05-06.jsonl`

**Status: 12.5I-B SITUATION GENERATION COMPLETE. PR opening; awaiting QC trigger. After QC APPROVE: 12.5I-C labelling round dispatches.**
