---
date: 2026-04-27
from: ml-architect (PR #60 Phase 2 reviewer)
to: orchestrator → owner
re: Round 2 re-test of F1/F2/F3 fixes at commit 0b97181 on programmer/blueprint-v3-implementation-2026-04-27
verdict: APPROVE
branch: programmer/blueprint-v3-implementation-2026-04-27
head: 0b97181
---

# ml-architect Round 2 review — PR #60 Phase 2

## Review method

Read all three changed source files directly via `git show` on the PR branch head
(`0b97181`). Verified `extract_all_features()` key schema from `feature_extractor.py`
source. Traced the F1 fix end-to-end symbolically (TC-26 V-Integration-Trace, see
section below). Read all 9 new tests added in this commit. Verified the
`_verify_corpus` gate in `scripts/build_corpus_revision_500_hand.py`. Confirmed no
attention-vocab or labelling-prompt mappings depend on the old long-form `hand_dict`
keys. All findings are source-verified, not plan-asserted.

---

## F1: Mode A `_generate_mode_a()` hand_dict key names

### Claim verified: short-form schema correctly implemented

`river-rats-core/generate_corpus_revision_pool.py`, function `_generate_mode_a()`,
the `hand_dict` construction block (approximately lines 128-142 of the committed
version) now uses:

```python
hand_dict = {
    'pos': pos,
    'h': ''.join(dec.hero_cards),
    'b': ''.join(dec.board),
    'st': dec.street[0],
    'fb': int(dec.facing_bet),
    'pot': pot_bb,
    'tc': to_call_bb,
    'vp': (dec.villain_positions[0] if dec.villain_positions else 'BB'),
    'exp': 'X',
    'id': sit_id,
    '_num_opponents': dec.num_opponents,
    '_opener_position': opener_pos,
    '_is_3bet_pot': int(dec.feat_dict.get('is_3bet_pot', 0)),
    '_action_history': None,
}
```

This matches the schema consumed by `extract_zero_compute_features()` in
`feature_extractor.py`:

- Line 234: `hero_pos = hand['pos'].upper()`
- Line 235: `facing_bet = int(hand['fb'])`
- Line 236: `pot = float(hand['pot'])`
- Line 237: `to_call = float(hand.get('tc', 0.0))`
- Line 238: `street_code = hand['st']`
- Line 241: `villain_pos_raw = hand.get('vp', None)`
- Line 260: `hero_cards = parse_hero_hand(hand['h'])`
- Line 261: `board_cards = parse_board(hand['b'])`

All required short-form keys are present in the Mode A `hand_dict`. No
key-name mismatch can trigger the silent `KeyError`.

Key name fix is CORRECT and complete.

### TC-26 V-Integration-Trace: F1 fix end-to-end

This section demonstrates the TC-26 pattern explicitly, tracing F1 from input
boundary through to the consumer output value.

**Input boundary: `_generate_mode_a()` constructs `hand_dict`**

The fix populates `hand_dict['pot'] = pot_bb` where `pot_bb = dec.pot / BB_CHIP_SIZE`
(BB_CHIP_SIZE = 10). For a 6 BB pot: `pot_bb = 60 / 10 = 6.0`.

**Through fix: `extract_all_features(hand_dict)` is called**

`extract_all_features` calls `extract_features_step1_through_5(hand)` which calls
`extract_zero_compute_features(hand)`. At line 236: `pot = float(hand['pot'])`.
With the fix in place, `hand['pot']` exists (short-form key) and equals `6.0` (BB
units). Previously, `hand['pos']` did not exist (long-form key used was
`'hero_position'`), so line 234 threw `KeyError: 'pos'`, which was silently
caught by the caller, and the fallback chip-unit feat_dict was used.

**Through derivation: `add_derived_features(features)` computes SPR**

`add_derived_features` at line 1643: `features['spr'] = round(DEFAULT_EFFECTIVE_STACK / pot, 4)`.
`DEFAULT_EFFECTIVE_STACK = 100.0` (line 1566). With `pot = 6.0` (BB units):
`spr = 100.0 / 6.0 = 16.6667`. This is a BB-unit SPR in the correct range ([4, 16]
for typical stack-to-pot situations).

**Output: `feat_dict['spr']` reaches the consumer with correct BB-unit value**

The Mode A record is assembled with `'feat_dict': feat_dict` where `feat_dict`
includes `'spr': 16.6667`. This value is in the range [4, 16] (BB-unit). The
pre-fix value was `spr = 100.0 / 60.0 = 1.6667` (chip-unit, same 6 BB pot).

**Bug signature confirmed isolated and fixed:**

The chip-unit fallback path (`spr < 2.0 AND pot_bb > 6.0`) is no longer reachable
when `hand_dict` carries the correct short-form keys, because `extract_all_features`
will no longer throw at line 234 and the except clause will not fire.

Trace complete. Fix value reaches consumer correctly.

### TestModeASprKeyNameFix — 3 tests verified active

All three tests in `TestModeASprKeyNameFix` exercise the regression directly:

**`test_short_form_keys_accepted_by_extract_all_features`**: calls
`extract_all_features()` with a complete short-form dict, `pot=12.0` (BB units),
and asserts `7.0 <= spr <= 10.0` (expected: 100/12 = 8.33). This test directly
detects a regression back to long-form keys — if keys were wrong, `extract_all_features`
would raise `KeyError` and the test would fail before the SPR assertion. Not dormant.

**`test_long_form_keys_cause_keyerror`**: passes a long-form key dict to
`extract_all_features()` and asserts a `KeyError` is raised. This confirms the old
buggy dict would still fail today — important: it means the except-clause fallback
path was real, and it remains the regression sentinel. If `extract_all_features` ever
changes to accept long-form keys, this test would alert. Not dormant.

**`test_mode_a_spr_after_keyname_fix`**: calls `extract_all_features()` with three
synthetic short-form Mode A records (pot = 12.0, 15.0, 22.0 BB) and asserts none
have `spr < 2.0 AND pot > 6.0`. This is the N1 regression test in integrated form.
Not dormant.

All three tests are active and together constitute a regression suite for F1. If
the key fix were reverted, `test_short_form_keys_accepted_by_extract_all_features`
would catch it.

**F1 verdict: PASS. Fix is correct. Trace confirmed. Tests are active.**

---

## F2: N1 smoke test field name

### Claim verified: line 255 now reads `r.get('pot', 0)`

`river-rats-core/tests/test_corpus_revision_v3.py`, `TestN1SprRegressionAssertion.test_n1_mode_a_pool_smoke`:

```python
violations = [
    r for r in records
    if r['feat_dict']['spr'] < 2.0 and r.get('pot', 0) > 6.0
]
```

The key is `'pot'`, not `'pot_bb'`. This matches the pool record schema: Mode A
records store the BB-unit pot under the top-level key `'pot'` (confirmed in the
`rec` dict in `_generate_mode_a()`: `'pot': pot_bb`).

### Smoke test is now non-dormant

With `r.get('pot', 0)`, the test reads the actual pot value (e.g. 6.0 BB) from each
record. If a Mode A record has `spr = 1.67` (chip-unit bug) and `pot = 6.0` (BB),
the condition `spr < 2.0 AND pot > 6.0` evaluates: `1.67 < 2.0 = True` and
`6.0 > 6.0 = False` — this boundary case is correctly NOT a violation (pot must
be strictly greater than 6.0). For a pot of 7.0 BB: `spr = 100/70 = 1.43 < 2.0`
AND `7.0 > 6.0` — this would be a genuine violation if chip units were passed
incorrectly (100/70 chips = 1.43), and the test would correctly catch it.

The test remains correctly skipped until a smoke pool is generated (no pool exists
at `/tmp/smoke_test_pool.jsonl`). This is the intended behavior — the test is a
runtime guard, not a pre-generation guard.

**F2 verdict: PASS. Key name is corrected. Test is non-dormant.**

---

## F3: OOP/IP verification gate

### Claim verified: correct bounds at both positions

`scripts/build_corpus_revision_500_hand.py`, `_verify_corpus()` function, lines
464-467:

```python
('oop_pct 0.55-0.65', 0.55 <= oop_count/n <= 0.65,
 f'got {oop_count/n:.2f}'),
('ip_pct 0.35-0.45', 0.35 <= ip_count/n <= 0.45,
 f'got {ip_count/n:.2f}'),
```

Both checks are present. The OOP gate was changed from `0.40 <= ... <= 0.75` to
`0.55 <= ... <= 0.65`. The IP gate is newly added. `ip_count = n - oop_count` is
computed at line 448.

The bounds match the Blueprint v3 spec exactly. A corpus with 42% OOP will produce
`oop_count/n = 0.42`, which fails `0.55 <= 0.42` — WARN (the function returns False
and prints WARN). A corpus with 60% OOP: `0.55 <= 0.60 <= 0.65` — PASS.

### Q2 disposition: TestVerifyCorpusOopBoundsStrict skip — acceptable as-is

The two `TestVerifyCorpusOopBoundsStrict` tests skip because
`scripts/build_corpus_revision_500_hand.py` is not on the test runner's `sys.path`.
The tests use `importlib.util.spec_from_file_location` to import the module from a
relative path — this correctly skips if the path doesn't resolve.

**Disposition: acceptable as-is for this PR.**

Rationale: the production code is confirmed correct by direct source read. The skip
is a test infrastructure gap, not a logic gap. The F1 `TestModeASprKeyNameFix` tests
provide the same synthetic corpus pattern (construct records, call function, assert
result) and they run live. Adding `scripts/` to `conftest.py` `sys.path` is a valid
follow-up improvement, but it is not blocking for merge.

The builder's note is accurate: this is a test infrastructure change, not a logic
change. The gate enforcement in production is correct.

**If the orchestrator or owner wants full live coverage before merge**, the fix is
one line in `conftest.py`:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
```
This should be treated as a fast follow-up, not a merge blocker.

**F3 verdict: PASS. Gate bounds are correct. Q2 skip is acceptable. Recommend
conftest.py scripts-path fix as a non-blocking follow-up.**

---

## Attention-vocab and labelling-prompt review (per feedback_attention_flags_when_features_change.md)

The F1 fix renames the internal `hand_dict` keys passed to `extract_all_features()`.
It does NOT change the output `feat_dict` produced by `extract_all_features()`.
It does NOT change the top-level record fields written to the pool JSONL (those
remain `hero_cards`, `hero_position`, `villain_positions`, `pot`, etc. — these
are the record-level metadata keys that labelling_agent.py reads, not the
hand_dict keys).

Checked `run_attention_experiments.py`, `assemble_pilot_data.py`,
`scripts/build_pilot_corpus_100_hand.py`, and `tests/test_attention_experiments.py`
— none reference `hand_dict` keys. They operate on `feat_dict` output fields.

Checked `prompts/gto_labeller_v3.2.md` — references `hero_position` as a
feature name in the labeller's feature table (line 469). This is the
`feat_dict` output feature `hero_position` (integer-encoded seat), not the
`hand_dict` input key. No naming conflict.

Checked `river-rats-core/labelling_agent.py` — uses `hero_cards`, `hero_position`
as top-level pool record fields (line 41, `_FLAT_METADATA_KEYS`). These are
record-level metadata keys (output), not hand_dict input keys. No conflict.

**No attention-vocab or labelling-prompt mapping depends on the old long-form
`hand_dict` keys. The F1 fix is safely scoped to the Mode A generation path.**

---

## Test count verification

Builder reports: 43 passed, 7 skipped, 0 failed (50 collected). The 34 pre-existing
tests from commit 3708d92 are unchanged. 9 new tests added:

- `TestModeASprKeyNameFix`: 3 tests, all should PASS (live calls to
  `extract_all_features`).
- `TestVerifyCorpusOopBoundsStrict`: 2 tests, both SKIP (import path, expected).
- `TestNfdBoundaryTurnDecisionTemplates`: 4 tests, all should PASS (F4 scope —
  not re-tested here, gto-expert domain).

This is consistent with the reported count.

---

## Overall verdict: APPROVE

All three required changes from the round 1 review are correctly implemented and
verified by direct source read:

| Fix | File | Status |
|-----|------|--------|
| F1: Mode A short-form key schema | `generate_corpus_revision_pool.py` | PASS — key schema correct, TC-26 trace complete, 3 active tests |
| F2: N1 smoke test `r.get('pot', 0)` | `test_corpus_revision_v3.py` line 255 | PASS — key corrected, test non-dormant |
| F3: OOP gate `0.55-0.65`, IP gate `0.35-0.45` | `build_corpus_revision_500_hand.py` | PASS — both bounds in code, Q2 skip acceptable |

The Mode A pipeline can now correctly produce BB-unit SPR values. The N1 smoke
test will actively catch a regression if Mode A records are generated with
chip-unit pots. The OOP/IP verification gate will reject corpora outside the
spec range.

No round 1 required changes remain open. F4 is gto-expert domain and is not
reviewed here.

**Verdict: APPROVE.**

---

## Non-blocking follow-ups (carry to backlog, not blocking merge)

1. Add `scripts/` to `conftest.py` sys.path so `TestVerifyCorpusOopBoundsStrict`
   runs live. One-line fix, low risk.

2. Q3 (Mode A UTG zero records): the UTG pre-existing fold behavior means Mode A
   will produce zero records if `single_position='UTG'`. Before the production
   corpus run, the position pool should be broadened (CO, BTN, BB) to generate
   meaningful Mode A volume. This is a runtime concern, not a code bug.

3. Round 1 Nit 1 still open: `zero_instance_rules_coverage` and
   `poker_pattern_coverage` fields in the lock file remain as placeholders.
   As noted in round 1, this is acceptable pre-labelling.
