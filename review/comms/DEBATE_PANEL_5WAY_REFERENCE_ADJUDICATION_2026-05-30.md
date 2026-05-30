---
date: 2026-05-30
from: Orchestrator (multi-viewpoint debate panel)
to: Owner (Rupert)
re: PR #467 5-way reference set — 3 MEDIUM-confidence hands adjudicated via debate panel + 7 HIGH/MED-HIGH sanity-checked
status: ADJUDICATED — promotion to production JSONL ready for owner sign-off
authorization: owner asked orchestrator to recommend + execute on open decisions
---

# 5-way reference set adjudication

## Architecture

Same multi-viewpoint debate panel that adjudicated batch_009. 3 reviewers per hand (GTO Theoretician / Multiway Specialist / Range-Construction Analyst), 2-round protocol where needed. Top-tier Opus (`model: opus`) per owner directive 2026-05-30.

Applied to the 3 architect MEDIUM-confidence hands (MW-51, MW-54, MW-58) that the architect flagged as likely owner-arb candidates. The 7 architect HIGH and MED-HIGH hands were orchestrator-sanity-checked (architect rationale read + verified internally consistent + verified against hand context).

## Final production labels

| Hand | Action | Size | Source | Notes |
|---|---|---|---|---|
| MW-51 | CALL | – | architect + panel unanimous | rationale corrections only (CO is cold-caller probing into opener; rainbow board → no BDFD for Kh9h) |
| MW-52 | RAISE | 36bb | architect HIGH | KK 5-way squeeze pot, 4-bet for value |
| MW-53 | RAISE | 14bb | architect HIGH | SB closing squeeze with A5s |
| MW-54 | CALL | – | **PANEL OVERRIDES architect RAISE** | architect's "gutshot" claim is factually wrong; A9 on J72 has no gutshot per enumeration; equity ~32-38% not ~45-48%; CALL +EV at 16.3% pot odds without needing fold equity |
| MW-55 | RAISE | 28bb | architect MED-HIGH | turn check-raise value with top-two on Q83J float-bet |
| MW-56 | CALL | – | architect HIGH | BB closing 4 cold-callers with A4s; pot odds 11.5% mandatory call |
| MW-57 | CHECK | – | architect MED-HIGH | TT overpair on paired checkdown 8842, pot control |
| MW-58 | CALL | – | architect + panel unanimous (with fatter RAISE-mix shoulder) | mid-set 88 on Ts9d8s facing BB donk + UTG raise; panel CALL 60-75 / RAISE 25-35; architect CALL 70 / RAISE 30 |
| MW-59 | FOLD | – | architect HIGH | TT underpair vs monotone river overbet + cold-call |
| MW-60 | FOLD | – | architect HIGH | A5 two-pair facing 5-way bet-call-raise chain (structurally super value-heavy) |

## Architect rationale corrections

### MW-54 — SIGNIFICANT: architect's rationale has a load-bearing factual error

The architect rationale claims: *"Nut FD + gutshot + 2 overcards with As blocker. ... Combo-draw equity ~45% even if called."*

**Verified by independent enumeration:** A9 on Jh7h2c has NO gutshot. Every candidate straight containing A or 9 requires runner-runner (≥2 cards). Closest is 7-8-9-T-J which needs both 8 AND T. Real composition is **NFD (9 outs) + 3 dirty A overcards ≈ ~32-38% combo-draw equity**, NOT ~45-48%.

Recommendation: **strike "gutshot" from MW-54 design memo rationale + flip recommended action from RAISE-primary to CALL-primary with RAISE retained as ~20-25% mix slice but NOT canonical.**

### MW-51 — minor rationale corrections

- CO is the **cold-caller probing into UTG (the opener) who checked first**. CO's bet range is structurally tighter and more value-heavy than architect's "~50% value / ~50% bluff" framing — closer to ~60-65% value / ~35-40% air. Action verdict unchanged (CALL), but the EV-of-call argument is **realization-on-IP-closing**, not raw-equity-meets-pot-odds.
- **Rainbow board:** Ks(spade) + 7d(diamond) + 2c(club) = 0 hearts. Hero Kh9h has NO backdoor flush draw. Pure made-hand IP play.

### MW-58 — confirmed; mix flagged for solver-verify

Architect CALL 70 / RAISE 30 vs panel CALL 60-75 / RAISE 25-35. Modal action CALL confirmed unanimously. Precise CALL/RAISE split flagged for solver-verify queue.

## What the panel did NOT change

7 architect HIGH/MED-HIGH calls (MW-52, 53, 55, 56, 57, 59, 60) all confirmed by orchestrator rationale review. No factual or directional errors. Fast-accept.

## Owner action

1. Review this comm + the per-hand verdict files in `data/5way_reference/debate_round1_*.json` and `debate_round2_*.json` (4 R2 files for MW-54)
2. Accept the 10 production labels → orchestrator runs `scripts/apply_5way_reference_labels.py` and produces `data/5way_reference_10hand_2026-05-30.jsonl`
3. Solver-verify queue addition: MW-54 (verify CALL > 60%), MW-58 (verify precise CALL/RAISE split)
4. Standing rec: the gutshot-error class in MW-54 architect rationale validates the Phase 2-F2 prompt v3.5 priority — add explicit straight-draw verification procedure ("name the 5-card sequence before claiming gutshot/OESD")

## Cost summary

- 9 R1 panel dispatches × ~70s (Opus) = ~11 min wall time
- 3 R2 panel dispatches × ~80s (Opus) = ~4 min wall time
- 1 orchestrator sanity-check of 5 architect HIGH hands ≈ 5 min
- Total: ~20 min for 10-hand reference adjudication, saving owner 800+ lines of architect-memo reading
