---
date: 2026-04-27
from: Lead-programmer (named author)
to: Main terminal (orchestrator) · ml-architect · QC stream · Owner
re: Phase 10 fix complete — re-extract dedup of consecutive-identical prior_actions + lock structural_verification corrections; PR #70 refreshed
status: REPORT — Phase 10 fix executed per MAIN_TERMINAL_PR70_DATA_SYNTHESIS_2026-04-27.md (master 0fd69b8)
---

# Phase 10 fix report

## Scope per directive

Per `MAIN_TERMINAL_PR70_DATA_SYNTHESIS_2026-04-27.md` § "Phase 10 fix directive":

1. Re-extract script — collapse consecutive duplicate `prior_actions` entries
2. Regression test — `PILOT_009` specifically
3. Re-run E1 + verify all 100 records have no duplicates
4. NIT-B — fix lock `structural_verification` stale fields (magg + sb_hero)
5. Re-run C2 → updated 494-hand corpus
6. Force-push PR #70

## Code changes

### `scripts/reextract_pilot_100_features.py`

- Added `_dedupe_prior_actions(prior_actions)` helper. Collapses consecutive
  identical entries (preserves legitimate non-adjacent repeats like
  `raise → call → raise`).
- Wired into `reextract_record()`: after `dict(hand)` clone, replaces
  `prior_actions` with the deduped list.
- Extended `_verify()` with a third gate: assert no consecutive duplicates
  remain across the 100 re-extracted records. Reports per-record offender
  list on failure.

### `scripts/build_corpus_revision_500_hand.py`

Lock `structural_verification` block — definitions corrected to match the
final-corpus semantics ml-architect used in TC-26 audit:

| Field | Old definition | New definition |
|-------|---------------|----------------|
| `magg_villain_aggression_2_count` | `vagg >= 2 AND street == 'river'` (= 64) | `vagg == 2` any street (= **73**, matches audit) |
| `sb_hero_count` | `generation_source == 'sb_hero_scenarios'` (= 20) | `hero_position == 'SB'` any source (= **26**, matches audit) |

Template-provenance counts preserved in two new fields for audit trail:
- `magg_template_count` (= 64)
- `sb_hero_template_count` (= 20)

### `river-rats-core/tests/test_corpus_revision_v3.py`

New class `TestPhase10ReExtractDedup` (5 tests):

1. `test_dedupe_helper_collapses_consecutive_duplicates` — unit test on the
   PILOT_009 input pattern (3x raise + check + check → raise + check + check).
2. `test_dedupe_helper_preserves_non_adjacent_repeats` — `raise → call → raise`
   stays intact; not all duplicates collapsed.
3. `test_dedupe_helper_handles_empty` — `[]` and `None or []` both pass.
4. `test_pilot_009_no_consecutive_duplicates` — regression on the specific
   record gto-expert flagged.
5. `test_no_record_has_consecutive_duplicates` — corpus-wide gate; was the
   failure mode before the fix (3/100 affected: PILOT_009, _057, _096).

Helper loaded via `importlib.util.spec_from_file_location` since `scripts/`
is not on `sys.path` in pytest.

## Pre-fix state

3/100 pilot records had consecutive duplicate `prior_actions`. All hero=SB
with the same pattern: 3x `"preflop: SB raise"` at the start of the list.

| Record | prior_actions (BEFORE) |
|--------|------------------------|
| `PILOT_009` | `["preflop: SB raise", "preflop: SB raise", "preflop: SB raise", "flop: SB check", "turn: SB check"]` |
| `PILOT_057` | `["preflop: SB raise", "preflop: SB raise", "preflop: SB raise"]` |
| `PILOT_096` | `["preflop: SB raise", "preflop: SB raise", "preflop: SB raise", "flop: SB check"]` |

## Post-fix state

| Record | prior_actions (AFTER) |
|--------|------------------------|
| `PILOT_009` | `["preflop: SB raise", "flop: SB check", "turn: SB check"]` |
| `PILOT_057` | `["preflop: SB raise"]` |
| `PILOT_096` | `["preflop: SB raise", "flop: SB check"]` |

`_verify` reports `consecutive prior_actions dups: 0/100 — PASS`.

## Pipeline run results

### E1 (re-extract pilot 100)

```
[verify] is_preflop_aggressor=1: 48/100         # unchanged from prior PFA reconstruction
[verify] mean(spr): 11.989                       # unchanged (BB-unit fix preserved)
[verify] consecutive prior_actions dups: 0/100   # NEW gate — PASS
[reextract] SHA256: bd951cf9f27c7f85e9e7468de462db35eb1f398d0288c2b9be3ff0181b9f3dfb
```

Output: `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl`
Lock updated: `data/pilot_corpus_100_hand_2026-04-26.lock.json` SHA `c6318559...`

### C2 (494-hand assembly)

```
[Phase A] Total selected: 349/355
[Phase B] Selected 45/45
[build] Combined corpus: 494 hands
[verify] PASS: facing_bet_count >= 125 — got 163
[verify] PASS: pfa_count >= 150 — got 217
[verify] PASS: spr_ge4_count >= 125 — got 395
[verify] WARN: spr_2to4_count >= 100 — got 56     # known structural shortfall, accepted per round 9
[verify] PASS: oop_pct 0.55-0.65 — got 0.65
[verify] PASS: ip_pct 0.35-0.45 — got 0.35
[verify] PASS: magg_villain_agg2 >= 20 — got 64
[verify] PASS: donk_bet_defence >= 25 — got 25
[verify] PASS: sb_hero >= 20 — got 26
[disjoint] PASS: no within-batch duplicates
```

Total: **494 hands** (unchanged FINAL count per round 9 synthesis).
10/11 gates PASS, 1 WARN unchanged.

## Final SHA256 attestation

| File | SHA256 |
|------|--------|
| `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` | `bd951cf9f27c7f85e9e7468de462db35eb1f398d0288c2b9be3ff0181b9f3dfb` |
| `data/pilot_corpus_100_hand_2026-04-26.lock.json` | `c6318559a723825663a06669a052f03605663e7dbbb130bff925b7e043ab6341` |
| `data/corpus_revision_500_hand_2026-04-27.jsonl` | `09c1881bf1b3ebac2b2a44d7abf1db9a62bc35b5adfb85333fa67bce9147ede9` |
| `data/corpus_revision_500_hand_2026-04-27.lock` | `5891f8100ed5958073192666288d5f48f3718d53625a1b5329eee5216c015111` |

Mode A pool, Mode B pool, combined pool — unchanged from PR #70 prior force-push (verified 0 consecutive-dup offenders before re-running C2; the 3 affected records are pilot-only).

## Test suite

- 5 new Phase 10 tests — all PASS
- 57 / 62 corpus-revision tests pass (5 skipped — gates that require pool files not regenerated this cycle; pre-existing skip-pattern preserved)

## Lock structural_verification — final

```json
{
  "facing_bet_count": 163,
  "pfa_count": 217,
  "magg_villain_aggression_2_count": 73,
  "magg_template_count": 64,
  "donk_bet_defence_count": 25,
  "sb_hero_count": 26,
  "sb_hero_template_count": 20
}
```

`magg_villain_aggression_2_count` and `sb_hero_count` now match ml-architect
TC-26 audit numbers (73 and 26 respectively). Template-provenance preserved
under `*_template_count` aliases for traceability.

## Other NITs (tracked, non-blocking)

Per directive § "Other NITs (non-blocking; track to backlog)":

- gto NIT-1 (`PILOT_219` `is_two_tone` advisory; flop-only flag on turn board) — no action this cycle; passed to label-brief tracking
- gto NIT-2 (`PILOT_408` thin equity) — no action this cycle; passed to label-brief tracking
- ml-architect NIT-A (3 pilot SPR<2.0 with vagg=1) — pre-existing pilot characteristic; advisory only

## Files in this force-push

| File | Status |
|------|--------|
| `scripts/reextract_pilot_100_features.py` | MODIFIED — dedup helper + verify gate |
| `scripts/build_corpus_revision_500_hand.py` | MODIFIED — lock structural_verification semantics |
| `river-rats-core/tests/test_corpus_revision_v3.py` | MODIFIED — 5 Phase 10 tests added |
| `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` | REGENERATED — 0 consecutive dups |
| `data/pilot_corpus_100_hand_2026-04-26.lock.json` | UPDATED — new pilot v2 SHA |
| `data/corpus_revision_500_hand_2026-04-27.jsonl` | REGENERATED — pilot dup fix propagated |
| `data/corpus_revision_500_hand_2026-04-27.lock` | UPDATED — new corpus SHA + corrected counts |
| `review/comms/PROGRAMMER_REPORT_PHASE10_FIX_2026-04-27.md` | NEW — this report |

## References

- Synthesis directive (master `0fd69b8`): `MAIN_TERMINAL_PR70_DATA_SYNTHESIS_2026-04-27.md`
- ml-architect round 3: `REVIEW_ML_ARCHITECT_PR70_DATA_2026-04-27.md` § NIT-B
- gto-expert round 3: `REVIEW_GTO_EXPERT_PR70_DATA_2026-04-27.md` § NIT-3
- Round 9 synthesis (494 FINAL): master `114961f`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_shared_tree_commit_hygiene.md`

**Status: PHASE 10 FIX COMPLETE. PR #70 refreshed with deduped pilot v2 + corrected lock counts + regenerated corpus. Awaits round 3.5 mini-review (ml-architect + QC).**
