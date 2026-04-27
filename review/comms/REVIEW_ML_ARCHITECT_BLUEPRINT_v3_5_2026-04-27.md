---
from: ml-architect (Blueprint v3.5 reviewer)
date: 2026-04-27
pr: 76
branch: orch/blueprint-v3-5-scenario-expansion-2026-04-27
re: Round 5 review — Scenario Module Expansion Blueprint v3.5, 146 new templates
verdict: CHANGES_REQUESTED
---

# ML-Architect Review — Blueprint v3.5 Scenario Module Expansion

## Review method

Read the blueprint in full, the Phase 5 directive, the F5 allocator source (`git show
origin/master:scripts/build_corpus_revision_500_hand.py`), the feature extractor
(`git show origin/master:river-rats-core/feature_extractor.py`), and the blocker features
module (`git show origin/master:river-rats-core/blocker_features.py`). Also read
`situation_factory.py`, `game_state_bridge.py`, and the existing `nfd_scenarios.py` and
`magg_scenarios.py` modules. All findings are source-verified. Prior round 1, 2, and 4
reviews informed the lens but conclusions here are independent of them.

Computations for fingerprint checks, SPR math, aggression counts, and flush-draw / nut-block
logic were verified by running Python locally against the actual source logic.

---

## Area 1 — Allocator math correctness

### Architect's claim: 146 new records is the honest minimum

**Verified: correct for the structural claim.**

The F5 allocator assigns each record to at most one category (`used_fps` prevents re-use).
The only genuine dual-quota mechanism is overflow: a record fills its highest-scarcity
eligible category; once that quota is full, subsequent same-type records fall to the
next-highest eligible category. The architect correctly identified that only the MAGG-B
group (22 records) achieves this: magg fills first (30 MAGG-A + 10 existing = 40), then
the 22 MAGG-B records fall to spr_med.

The directive's estimate of ~80-120 assumed simultaneous multi-quota filling; the architect's
correction to 146 is accurate.

**However, the overflow analysis was done at pre-expansion scarcities, not post-expansion
scarcities. This matters.**

### MEDIUM risk: spr_med fill is seed-dependent post-expansion

The blueprint's scarcity analysis uses current (pre-expansion) values: spr_med = 2.22, pfa
= 1.74. Pre-expansion, MAGG-B records (eligible for {magg, pfa, spr_med}) deterministically
flow to spr_med after magg fills (2.22 > 1.74).

After all 146 templates are added, the F5 allocator recomputes scarcity from fresh yield
counts over the expanded pool. Post-expansion yields produce different scarcities:

- pfa: target=80, yield≈86 -> scarcity = 80/86 = 0.9302
- spr_med: target=40, yield≈43 -> scarcity = 40/43 = 0.9302

Both round to 0.9302. They are numerically equal at post-expansion pool size.

When MAGG-B records process (eligible = {pfa, spr_med} after magg fills),
`max(eligible, key=lambda c: scarcity[c])` faces a tie. Python's `max()` on a set with
equal-valued keys has no stability guarantee; the pre-shuffle seed determines which
assignment wins. This is not the deterministic "spr_med wins" path the blueprint describes.

**Impact quantification:** spr_med has 43 eligible records for a quota of 40. The slack
is only 3 records. Approximately 40 of the 43 spr_med-eligible records are also pfa-eligible
(the 18 existing Mode A records are typically pfa, plus all 22 MAGG-B). If the seeded
shuffle routes too many dual-eligible records to pfa before spr_med fills, spr_med may land
at 37-39 instead of 40.

**Mitigation already in the architecture:** The 3-record slack (43 vs 40) means that even
if a few dual-eligible records route to pfa first, spr_med will still likely fill. The
specific seed (20260427) will produce a deterministic outcome. The E2-B smoke test
(assert pool >= 250 records) must be extended to also assert spr_med Phase A count = 40
before this risk can be considered closed.

**Builder action required:** E2-B smoke test assertion must include per-category FULL
checks, not just total pool size. The smoke test spec (`assert Mode B pool >= 250`) is
insufficient on its own.

### PFA overflow from DONK templates: scarcity analysis is inverted post-expansion

The blueprint warns (Module 5): donk+pfa records may fill pfa quota (scarcity 1.74) rather
than donk (1.67) because pfa scarcity > donk scarcity pre-expansion. This is correct
pre-expansion.

Post-expansion the relationship reverses: donk scarcity = 25/25 = 1.00, pfa scarcity =
80/86 = 0.93. Donk now wins the tie-break (1.00 > 0.93), so donk+pfa records correctly
flow to donk.

The blueprint's described mitigation ("pure PFA records fill pfa before donk-pfa are
processed") is mechanically wrong — the allocator doesn't process by source but by
scarcity priority across all records. The outcome is correct but the explanation is
incorrect. This is a documentation issue that could confuse the builder about why the
allocator behaves as expected.

**No action required on the implementation, but the builder should know:** donk fills
correctly because of the scarcity inversion, not because of pool ordering.

### Other overflow paths: none found

Verified: NFD templates have hero=BB (not preflop opener), so they don't satisfy pfa.
BAC templates at spr_std pots don't satisfy spr_med. SB templates don't satisfy pfa (hero
is SB, not opener in flop templates; BTN opens in turn templates where hero is SB caller).
The MAGG-B overflow to spr_med is the only genuine dual-quota path. Architect's claim is
correct on this point.

---

## Area 2 — Feature value plausibility

### MAGG: villain_aggression_count = 2

**Verified correct for all three patterns.**

The bridge (`game_state_bridge.py:108-119`) counts villain bet/raise actions on prior
streets only (`for s in street_sequence[:current_idx]`). At the river (`current_idx=3`),
it processes preflop, flop, and turn.

- Pattern A (BB bets flop + turn, hero calls both): flop-BB=bet(1), turn-BB=bet(1) = 2
- Pattern B (BB bets flop + turn + river): river bet is on the CURRENT street -> excluded.
  flop(1) + turn(1) = 2
- Pattern C (BB check-raises flop + bets turn): flop BB actions = [check, raise];
  `any(a in ('bet', 'raise') for acts)` = True = +1. Turn BB bet = +1. Total = 2.

Hero CO/BTN actions are excluded (bridge filters by villain position). All 52 MAGG
templates are structurally correct.

### PFA: is_preflop_aggressor = 1

**Verified correct.** The bridge sets `is_preflop_aggressor = int(opener_position is not
None and opener_position.upper() == hero_pos.upper())`. All PFA and MAGG templates
explicitly set `opener_position = hero_pos`. All donk sub-scenarios 8c/8d set
`opener_position = 'CO'` or `'BTN'` matching hero. The PFA-7 group (BTN opener,
CO+SB callers, BB folds) correctly includes `('preflop', 'BB', 'fold')` in action history
and does not list BB in villain_positions. This correctly produces is_preflop_aggressor=1.

### NFD: has_flush_draw = 1 and nut_flush_block = 1

**NFD-RAISE (16 templates): fully verified correct.**

All 16 templates have hero holding both cards of the flush suit, board holding exactly 2
cards of the same suit (total = 4), and hero's first card is always the Ace of that suit.
`_check_flush_draw` in `hand_evaluator.py` requires count=4 and `our_suited >= 1`. All 16
satisfy this. `compute_nut_flush_block` in `blocker_features.py` requires hero holds A of a
suit with 2+ board cards of that suit (flop threshold = 2). All 16 satisfy this. No card
conflicts found.

**CRITICAL BUG — NFD-CALL: 3 of 16 templates fail nut_flush_block.**

Three templates place the Ace of the flush suit on the BOARD rather than in the hero's
hand:

- **NFD-C-03**: hero `[Ks, 9s]`, board `[As, 7s, 3d]`. Ace of spades is on board. Hero
  holds King of spades, not Ace. `compute_nut_flush_block` returns 0.
- **NFD-C-09**: hero `[Kh, Jh]`, board `[Ah, Th, 3d]`. Ace of hearts is on board. Hero
  holds King and Jack of hearts. Returns 0.
- **NFD-C-14**: hero `[Kd, Qd]`, board `[Ad, 9d, 4s]`. Ace of diamonds is on board.
  Hero holds King and Queen of diamonds. Returns 0.

The blueprint notes for these templates say "hero K-blocker" (NFD-C-03) and "A-high K
blocker" (NFD-C-14), suggesting intentional design to test non-nut flush draws. However,
`_is_nfd_hand` requires `has_flush_draw == 1 AND nut_flush_block == 1`. With
`nut_flush_block = 0`, these records do not satisfy `_is_nfd_hand` at all. They will not
count toward nfd_call quota.

**Impact:** nfd_call yield after expansion = 4 existing + 13 valid new = 17, not 20.
Quota is 20. Short by 3. The Phase A nfd_call bucket will remain UNDER.

**Required fix:** All three templates must be redesigned. For each, the hero must hold the
Ace of the flush suit, and the Ace must not appear on the board. Examples:

- NFD-C-03: Replace hero `[Ks, 9s]` with `[As, 9s]`. Remove As from board; use a
  different spade (e.g., `[6s, 7s, 3d]` or similar low board).
- NFD-C-09: Replace hero `[Kh, Jh]` with `[Ah, Jh]`. Replace Ah on board with a different
  high card (e.g., board `[Kh, Th, 3d]` -> but then Kh might conflict; use `[Qh, Th, 3d]`
  or design a new A-high connected board without Ah).
- NFD-C-14: Replace hero `[Kd, Qd]` with `[Ad, Qd]`. Remove Ad from board; use board
  `[9d, 4s, Kd]` (K-high, A not on board) — but then Kd conflicts; design a fresh board.

The architect must submit corrected templates for these 3 slots before the blueprint can
be approved for Phase 6 build.

### SPR math: MAGG-B, BAC, SB-turn

Verified against `add_derived_features`: `spr = DEFAULT_EFFECTIVE_STACK / pot_size`
where `DEFAULT_EFFECTIVE_STACK = 100.0`.

- MAGG-B (22 templates, pot 26-45 BB): SPR range 2.22-3.85. All satisfy `2.0 <= spr < 4.0`.
- BAC (11 templates, pot 14-24 BB): SPR range 4.17-6.25. All satisfy `spr >= 4.0`.
- SB-turn (3 templates, pot 32-36 BB): SPR 2.78-3.13. All satisfy `2.0 <= spr < 4.0`.

All SPR claims in the blueprint are correct.

---

## Area 3 — Fingerprint generation and disjointness

### Fingerprint logic

Confirmed: `_fingerprint_record` in `build_corpus_revision_500_hand.py` computes
`(sorted_cards(hero), sorted_cards(board))` using canonical normalisation. The
`_scenario_utils.fingerprint()` function uses the same sorted-cards approach. They are
compatible.

### Spot-check: 5 new template fingerprints

Computed fingerprints for:

- MAGG-A-01: `('AhQd', '2s4h7c9dJc')` — 5-card river board, unique combination.
- MAGG-B-01: `('AhKd', '2c3h5s7dTc')` — 5-card river board, unique combination.
- PFA-5a: `('KhQd', '4d9sAc')` — 3-card flop board.
- NFD-R-01: `('AhTh', '2s3h6h')` — 3-card flop board.
- NFD-C-09: `('JhKh', '3dAhTh')` — 3-card flop board. Note: this template also fails
  nut_flush_block (see Area 2 above).

No collisions found among the 5 sampled templates against their respective existing
module boards (the blueprint lists existing MAGG boards: `Kd7s2c5hJd`,
`Qs8h3cTd6s`, etc. — none match the new templates). Board-level disjointness
confirmed by checking all 52 new MAGG board fingerprints against the 10 existing MAGG
boards: 0 collisions.

### Cross-module disjointness: reliant on builder verification

The blueprint correctly specifies: "builder must run fingerprint collision check across the
combined pool after generation." This is appropriate. The review cannot run
`generate_scenarios()` without a live execution environment. The E2-B smoke test must
include the fingerprint disjointness assertion that is already part of the allocator
pipeline (`used_fps` check).

No fingerprint duplication issues were detected in the spot-check. The board and hero-card
choices across all modules appear sufficiently diverse to avoid collisions without
active conflict — but the builder must confirm with the live generation run.

---

## Area 4 — Pool size scaling

### Mode B pool: 115 + 146 = 261 verified

The Phase A quota totals: pfa(80) + nfd_raise(20) + nfd_call(20) + nfd_boundary(10) +
bac(20) + monster(20) + magg(40) + spr_std(50) + spr_med(40) + rule11(10) + donk(25) +
sb(20) = 355. Confirmed by summing PHASE_A_QUOTAS in the allocator source.

Corpus math: 100 re-extracted pilot hands + 400 new = 500. Of the 400 new: Phase A
(355) + Phase B (45) = 400. This arithmetic is correct.

Post-expansion category yields (assuming all 3 NFD-C failures are fixed):

| Category   | Post-expansion yield | Target | Status          |
|------------|---------------------|--------|-----------------|
| pfa        | ~86                 | 80     | FULL            |
| magg       | 62 (10+52)          | 40     | FULL            |
| spr_med    | ~40-43              | 40     | FULL (seed-dep) |
| nfd_raise  | 20 (4+16)           | 20     | FULL            |
| nfd_call   | 17 (4+13, if bugs fixed) | 20 | SHORT BY 3 (blocked) |
| bac        | 20 (9+11)           | 20     | FULL            |
| donk       | 25 (15+4+6)         | 25     | FULL            |
| sb         | 20 (13+7)           | 20     | FULL            |
| monster    | 20                  | 20     | FULL (unchanged)|
| rule11     | 10                  | 10     | FULL (unchanged)|
| spr_std    | >50                 | 50     | FULL (unchanged)|
| nfd_boundary | 6                | 10     | UNDER (acceptable per gto-expert) |

**Without fixing the 3 NFD-C-03/09/14 templates, nfd_call remains UNDER at 17/20.**

---

## Area 5 — Implementation risk surface

### 146 templates × ~30 LOC: mechanical but substantial

4,400 LOC added across 8 module files is within normal range for this type of expansion.
The list-append pattern (`_X_TEMPLATES: List[dict] = [...]`) is straightforward to
extend. No function signatures change. The builder adds entries to existing lists only,
per blueprint note 1. Risk is proportional to template count but each addition is
isolated; a malformed template fails at generation time (not silently in the list).

### Test count growth: acceptable

Existing tests use `for r in records` patterns on the full template list. Adding entries
to `_MAGG_TEMPLATES`, `_PFA_TEMPLATES`, etc. automatically exercises all new templates
through existing per-module tests. No structural test changes required — though the
builder should add at least the category-assertion tests specified in the blueprint's
verification spec.

### Silent failure risk: two architectural gaps found

**Gap 1 (HIGH): NFD nut_flush_block assertion missing from generate_scenarios()**

The MAGG module has an existing `assert villain_aggression_count == 2` in
`generate_scenarios()`. This makes MAGG failures loud. No equivalent assertion exists
for NFD templates at generation time. If a template has `nut_flush_block=0` (as found in
3 of the 16 NFD-C templates), `build_record_from_spec()` succeeds — it returns a valid
record — but the record will not satisfy `_is_nfd_hand`. The allocator silently skips it
for nfd_raise/nfd_call quota, and it ends up either in an unexpected category or in Phase
B only.

**Required action for builder:** Add per-template assertions in `nfd_scenarios.py`'s
`generate_scenarios()`:

```python
assert feat_dict.get('has_flush_draw') == 1, f"NFD template missing flush draw: {sid}"
assert feat_dict.get('nut_flush_block') == 1, f"NFD template missing nut block: {sid}"
```

**Gap 2 (MEDIUM): BAC num_callers_to_bet assertion missing**

BAC classification depends on `num_callers_to_bet >= 1` computed by the bridge from
current-street action history. If a BAC template's action_history omits the caller's
action on the current street (a common transcription error with multi-street histories),
`num_callers_to_bet = 0` and the record silently fails bac classification.

**Required action for builder:** Add per-template assertion in `bac_scenarios.py`'s
`generate_scenarios()`:

```python
assert feat_dict.get('num_callers_to_bet', 0) >= 1, f"BAC template missing callers: {sid}"
```

**Gap 3 (LOW): DONK and SB generation_source string**

`_is_donk_hand` checks `generation_source == 'donk_bet_defence_scenarios'` (exact string).
`_is_sb_hero_hand` checks `generation_source == 'sb_hero_scenarios'` OR
`hero_position == 'SB'`. SB templates will satisfy the position check regardless of source
string. DONK templates depend entirely on the source string being set correctly by
`generate_scenarios()`. Builder must follow the existing module pattern exactly (this is a
discipline issue, not an architecture gap).

### Builder note on BAC-4 action history spec

The blueprint spec for BAC-4 includes a flop action by 'SB' that the module says to omit
if SB folded preflop. The corrected spec (with SB folded preflop) is the right one and is
provided in the blueprint. Builder must use the `('preflop', 'SB', 'fold')` form and omit
SB from postflop actions.

---

## Area 6 — TC-26 V-Integration-Trace pre-design

### Trace path for new templates

The trace for any new template:

```
spec (dict in _X_TEMPLATES list)
  -> generate_scenarios() builds SituationSpec
  -> build_record_from_spec(spec, sid, generation_source) calls build_situation(spec)
  -> build_features_from_game_state(hero, game, context)
  -> extract_all_features(hand_dict) (59-feature contract)
  -> record dict with feat_dict (59 keys)
  -> _classify_record(record) assigns to category set
  -> _phase_a_select() assigns to one quota bucket
  -> used_fps prevents re-use
```

This trace is clean for MAGG, PFA, BAC, DONK, and SB templates, assuming action_history
is correct. The bridge correctly reads villain_aggression_count from prior-street actions
(not including current-street actions). The `opener_position` field in each spec correctly
drives `is_preflop_aggressor`.

### Silent failure scenario matching the F1 bug pattern

The F1 bug (PR #60) caused wrong key names in `hand_dict` to trigger a silent `KeyError`
caught upstream, producing a fallback feat_dict with chip-unit SPR. That specific path
is fixed.

The analogous risk here is: a template produces a valid `build_situation()` result, but
the feat_dict values are wrong (e.g., nut_flush_block=0), causing the record to be
mis-categorized. This is worse than build failure because it produces no error signal.
The NFD-C-03/09/14 templates demonstrate exactly this failure mode.

**The architect's per-template verification spec (assert nut_flush_block==1) would catch
this IF the builder runs it at generation time.** The blueprint requires the builder to
run extraction and confirm before committing. That requirement is correct. The gap is that
no existing generate_scenarios() assertion enforces it automatically.

### Architectural recommendation for TC-26 integration

When builder implements Phase 6, the generate_scenarios() function in each module should
validate the key category-defining features after `build_record_from_spec()`:

- nfd_scenarios.py: assert has_flush_draw==1 AND nut_flush_block==1
- bac_scenarios.py: assert num_callers_to_bet>=1
- magg_scenarios.py: existing assert villain_aggression_count==2 is sufficient
- pfa_scenarios.py: assert is_preflop_aggressor==1
- donk_bet_defence_scenarios.py: assert facing_bet==1
- sb_hero_scenarios.py: assert hero_position==4 (SB ordinal)

These assertions are cheap, loud on failure, and prevent the mis-categorization silent
failure mode. Builder should add these to each module's generate_scenarios() loop.

---

## Attention vocabulary impact

No impact. The 146 new templates produce records using the existing 59-feature schema
(`EXPECTED_59_KEYS` in `_scenario_utils.py`). No new features are added, no features
removed. The feature contract is unchanged. Attention vocabulary (which maps to feature
dimensions, not record sources) is unaffected. Class balance in the training data will
shift — this is the intended goal of the expansion. Applying the same lens as PR #60
round 2 review: template-source additions are safely scoped and do not trigger the
attention-flag update protocol from `feedback_attention_flags_when_features_change.md`.

---

## Summary of findings

| Finding | Severity | Area | Action required |
|---------|----------|------|----------------|
| NFD-C-03 fails nut_flush_block (Ace on board, not in hero hand) | HIGH | 2, 5 | Replace template before Phase 6 build |
| NFD-C-09 fails nut_flush_block (same failure pattern) | HIGH | 2, 5 | Replace template |
| NFD-C-14 fails nut_flush_block (same failure pattern) | HIGH | 2, 5 | Replace template |
| nfd_call quota under-fills by 3 if bugs not fixed | HIGH | 4 | Blocked on above fixes |
| Missing generate_scenarios() assertion for nut_flush_block | HIGH | 5, 6 | Builder must add in Phase 6 |
| Missing generate_scenarios() assertion for num_callers_to_bet | MEDIUM | 5, 6 | Builder must add in Phase 6 |
| spr_med vs pfa scarcity tie post-expansion (both 0.93) | MEDIUM | 1 | E2-B must assert spr_med==40 specifically |
| Blueprint scarcity analysis is pre-expansion only; post-expansion scarcities differ | MEDIUM | 1 | Documentation; no code change |
| Donk fill analysis uses wrong mechanism (scarcity inversion, not pool ordering) | LOW | 1 | Documentation nit; outcome is correct |
| E2-B smoke test spec (>= 250 records) insufficient without per-category assertions | MEDIUM | 4 | Builder must extend smoke test |

---

## Verdict: CHANGES_REQUESTED

Three NFD-CALL templates (NFD-C-03, NFD-C-09, NFD-C-14) have a verified feature contract
error: they place the Ace of the flush suit on the board rather than in the hero's hand,
producing nut_flush_block=0. These records will not satisfy `_is_nfd_hand`, will not count
toward nfd_call quota, and will silently fall into uncategorized status. Without fixing
these, nfd_call fills to 17/20 and Phase A nfd_call remains UNDER.

The fixes are straightforward (redesign board+hero for 3 templates) and do not require
architectural changes. The blueprint is otherwise well-constructed: MAGG action history
patterns are correct, SPR math is correct, 13 of 16 NFD-CALL templates are correct, all 16
NFD-RAISE templates are correct, and the pool size arithmetic is sound.

Two additional builder-phase requirements must be folded into Phase 6 implementation:
(1) add feature assertions to generate_scenarios() for nfd and bac modules to prevent
silent mis-categorization, and (2) extend the E2-B smoke test to assert per-category Phase
A fills, not just total pool size.

Submit corrected NFD-C-03, NFD-C-09, NFD-C-14 templates and this review will clear to
APPROVE-WITH-NITS on the remaining medium-severity items.
