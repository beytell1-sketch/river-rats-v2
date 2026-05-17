# Orchestrator Ratification — A0 Schema Fix Blueprint

**Blueprint reviewed:** `review/comms/DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v1_2026-05-17.md` (567 lines)
**Date:** 2026-05-17
**Verdict:** **RATIFIED WITH ONE OVERRIDE.** Blueprint accepted as A0 design; minor sequencing change applied by orchestrator.

---

## What's accepted as-designed

All §1–§5, §7 sections, and Rabbit-Holes RH-1 through RH-5 are accepted as-designed. No changes.

Specifically the orchestrator endorses:
- **§1 schema split** (`predicted_bet_pct` + `predicted_raise_to_bb`) over alternatives. Structural fix, no ambiguity, supports failure-direction reporting per `feedback_failure_direction_classification.md`.
- **§3.2 canonical-value tie-break** algorithm. Three-tier interpretation (bb / pct-raise-by / multiplier-of-bet) is well-justified and the tie-break-prefers-bb rule honours brief-intent.
- **§4 batch-008 strategy** (resume under old brief + normalize post-hoc) over restart. Saves ~132 labels with no quality loss.
- **§5.2 normalization basis** (`raise_to_bb / pot_bb`) for the single-axis "fraction of pot committed" feature representation.
- **§3.5 12-test acceptance suite.** Sufficient coverage; mandatory before A0.1 merges.

---

## ORCHESTRATOR OVERRIDE — §6 rollout sequencing

**Problem with as-designed sequence:**

`§6 PR A0.1` includes the brief patch (`data/4way_labeller_brief.md` lines 31–34, 105–112, 173–187). But `§6 PR A0.3` says "Labellers 2–5 complete batch-008 under OLD brief." If A0.1 merges before batch-008 resumes, labellers 2–5 will read the patched (NEW schema) brief but be expected to write OLD schema. Contradiction.

**Override (orchestrator decision per `feedback_orchestrator_decides_not_recommends.md` — sequencing is orchestrator's call):**

Move the brief patch from PR A0.1 to PR A0.3, as the FINAL step of A0.3. New sequence:

### PR A0.1 — Schema + normalizer (foundation), NO BRIEF CHANGE
- `river-rats-core/sizing_schema_normalizer.py` (new)
- `river-rats-core/tests/test_sizing_schema_normalizer.py` (new, 12 tests)
- **NO** brief change. The brief stays at v1 (legacy `predicted_sizing_pct` single field).
- Acceptance: all 12 unit tests pass; `--dry-run` against batch_001_raw_labels_labeller_1.jsonl produces clean summary.

### PR A0.2 — Backfill batches 001–007 (UNCHANGED from blueprint)
- Same scope as architect's blueprint §6 PR A0.2.

### PR A0.3 — Batch-008 resume + normalize + brief patch (FINAL)
- Step 1: labellers 2–5 resume batch-008 under v1 brief (unchanged).
- Step 2: all 5 batch-008 labellers complete; orchestrator confirms.
- Step 3: run normalizer on batch-008 → produce v2 files.
- Step 4 (FINAL): apply brief patch per architect's §2.1–§2.4. Brief becomes v2 (split schema).
- Brief patch takes effect at batch-009.

Acceptance criteria from architect's §6 A0.3 apply, plus:
- Brief change is the LAST commit on the A0.3 branch (after batch-008 normalization is verified).
- Batch-009 mini-pilot acceptance test (per architect's §6) is part of A0.3 verification — if batch-009 first 5 labels comply with new schema, A0.3 is complete; if not, brief is reverted and A0.3 is reopened for clarification.

---

## Acknowledged limitations the orchestrator accepts (not blocking)

- **Example C "tie-break" doesn't actually trigger in the spot used** (v=22 at pot=36.5 has pct interpretation illegal at 17 < 18 min-raise). Architect noted this and pointed to a hypothetical case. The unit test `test_raise_tiebreak_both_legal_prefers_bb` covers the real tie-break with v=22 at pot=45. Not a blueprint defect.
- **CANONICAL_BB ∪ CANONICAL_PCT ∪ CANONICAL_MULT ∪ legality filter** does not cover every possible labeller-written value. Values like 270 fall outside all three canonical sets and resolve via legality alone. Architect's §7.5 prediction of ~12–18 malformed-rejected total covers this; acceptable.
- **`raise-by` vs `raise-to` semantic ambiguity** in pct-of-pot interpretation: architect committed to "raise-by" (the `pct_to_bb` formula in §3.2 adds `facing_bet_bb + v% * pot_bb`). A labeller who meant "raise-TO 75% of pot" would produce a different value. Orchestrator accepts: legality + canonical-set check is the disambiguation; if a labeller wrote a value that's illegal under both raise-by and raise-to interpretations, it gets malformed-rejected. Owner-arb queue absorbs these.

---

## Ratification checklist (architect's §7) — orchestrator pass

- [x] 7.1.1 Min-raise rule — to be verified pre-PR-A0.1-merge against `river-rats-core/poker_game.py` (builder-time check, RH-1)
- [x] 7.1.2 All-in cap correct
- [x] 7.1.3 Preflop facing-open reads `to_call_bb` from context, not recomputed
- [x] 7.2 Deep-stack handling correct (no hard-coded 100bb)
- [x] 7.3 All-in handling correct
- [x] 7.4 3-bet/4-bet pot legality robust against `to_call_bb` context
- [x] 7.5 Malformed rate predicted at ~2% / 12–18 spots; orchestrator accepts
- [x] 7.6 Cross-stream sanity items all valid; will be verified pre-dispatch
- [x] 7.7 Sign-off:
  - Architect: blueprint commits to single design throughout (verified by orchestrator)
  - Orchestrator: ratified with one override (this document)
  - Owner: notified pending; reserves override on §3.2 tie-break or §4 batch-008 strategy if disagrees

---

## What this directive authorizes when builder fires

The builder (when restarted) executes PR A0.1, A0.2, A0.3 in strict sequence per the OVERRIDE sequence above. QC pre-merge audit per `feedback_qc_required_before_approval.md` on each PR.

The orchestrator will dispatch via `MAIN_TERMINAL_A0_FIRE_NOW_2026-05-XX.md` (date filled at dispatch).

---

## What this directive does NOT authorize

- Modifying any of batches 001–007 v1 files (only writes v2 alongside v1)
- Touching `prompts/gto_labeller_v3.4.md` (orthogonal; A2b will rewrite to v3.5 separately)
- Modifying `knowledge/three_way_gto.md` (orthogonal; A2c)
- Anything related to v9-3way model (frozen; only affects v9-4way forward)
- Solver-verify queue draining (parallel workstream; independent of A0)
