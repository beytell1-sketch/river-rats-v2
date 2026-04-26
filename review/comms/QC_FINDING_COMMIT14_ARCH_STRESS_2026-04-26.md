---
date: 2026-04-26
from: River Rats QC stream
to: Logic builder · Main terminal (orchestrator) · Owner (briefed)
re: Phase 3 architecture stress on commit 14 (TC-11) — 4 HIGH defensive-shielding findings; production behavior unaffected; pre-Stage-5-retrain hardening targets
status: FLAG (advisory; no gate rollback; HIGH findings are hardening targets, not active failures)
severity: HIGH (×4) / MEDIUM (×2) / LOW (×1) / NIT (×1)
test-class: TC-11 architecture stress + TC-15 multi-expert convergence
multi-expert verdict: CONVERGED on basic invariants (sum-to-1.0, no NaN, no exceptions on normal fixtures) | DIVERGED on defensive-shielding gaps (static-analysis agent surfaced 4 HIGH that empirical fixture agent did not exercise)
full finding: ~/river-rats-qc/findings/2026-04-26-commit14-arch-stress.md
---

# QC Phase 3 Finding — Commit 14 Architecture Stress

## Headline

Commit 14 chain-helper + composition derivation **core math is SOUND.** Sum-to-1.0 holds across HU/3-way/4-way/all-folded/heavy-collision/hero-overlap fixtures. No NaN injection path. Partition exhaustive across all 8 `classify_hand` categories.

**However:** the *defensive shielding* in `feature_extractor.py` is weaker than the comments / docstrings suggest. Several `try/except` blocks and silent-default fallbacks describe defensive behavior that doesn't actually fire under adversarial input. Production callers are well-behaved (logic team's own internal callers); production correctness is intact. **Stage 4 pilot agents, Stage 5 retrain feature regeneration, and post-pilot audit scripts** may exercise edge cases that trip these gaps.

**No rollback warranted. Stage 3.5 closure stands.**

## 4 HIGH findings (compact; full detail in QC repo)

### HIGH-1 — `STREET_NAME_MAP` silent-default to 'flop' on unknown street_raw

`feature_extractor.py:737`:
```python
STREET_NAME_MAP = {'f': 'flop', 't': 'turn', 'r': 'river'}
# .get(street_raw, 'flop')
```

Any caller passing `'river'` (full word), `'preflop'`, uppercase, or empty string silently maps to `'flop'`. River-reclass step (`if street_name == 'river' and cat == 'draw': cat = 'air'`) silently skips. No warning. Verified empirically.

**Production risk:** Stage 4 pilot agents / Stage 5 retrain feature regeneration may pass mixed conventions; logic's internal callers are single-char only.

**Fix:** whitelist-or-raise; or `_normalise_street(s)` accepting both single-char and full-word.

### HIGH-2 — `try/except classify_hand` is dead defensive code

`feature_extractor.py:913-916` and `1791-1794`:
```python
try:
    cat = classify_hand(combo, board)
except Exception:
    continue  # comment says skip
```

Empirically: `classify_hand('', board)` returns `'air'`; `classify_hand('BOGUS', board)` returns `'weak_made'`; `classify_hand('AAA', board)` returns `'strong_value'`. **Never raises.** Skip-on-exception path cannot fire. Malformed range keys are silently CLASSIFIED, not skipped.

The defensive intent in the code does not match actual behavior. Comments are misleading.

**Production risk:** future callers passing corrupted ranges (audit scripts loading from disk; pilot agents constructing fixtures) get silent pollution.

**Fix:** tighten `classify_hand` to raise `ValueError` on unrecognised notation OR add upstream notation-validity check; AND update comment.

### HIGH-3 — Cache key omits `action_history` hash (cache poisoning under AH mutation)

`feature_extractor.py:727-735, 776, 963-964`:
```python
cache_key = ('mw', num_opponents, tuple(opponent_positions))
# OR ('hu', villain_pos)
```

Two consecutive calls on the same `hand` dict with mutated `_action_history` return identical (stale) cached results. **Verified empirically:** Call 1 with `[(flop,BB,FOLD)]` → BB folded; Call 2 with `[(flop,BB,BET)]` (mutated in-place) → returns CACHED stale BB-folded result.

**Documented as "LOCAL to a single extract_all_features call"** — only matters if a caller mutates AH mid-extraction. No such caller exists in current logic. **But:**
- Pilot agent dispatch may extract features for multiple street decisions on the same hand object
- Audit scripts that re-extract features with synthetic AH variations
- Stage 5 retrain feature regeneration with augmentation passes

**Fix:** include `tuple(tuple(e) for e in (hand.get('_action_history') or []))` in cache key. OR document the immutability contract via assertion.

### HIGH-4 — Aggregate sentinels don't reflect per-villain partial state (CONFIRMS Phase 2 §3.7)

`feature_extractor.py:888-894`:
```python
agg_folded = all(per_villain_folded.values())
agg_overflowed = any(per_villain_overflowed.values())
```

Phase 2 surfaced this as a teaching/CONTENT_API contract issue (CONTENT_API.md:230 amendment §3.7); Phase 3 grounds it in logic-side code. The aggregate `_villain_folded` / `_villain_chain_overflowed` propagate to:
- Teaching's `_detect_range_mode` (mode label drift)
- Logic's Step 12 blocker NaN-flagging at `feature_extractor.py:2332`

A hand where the primary villain is fine but a non-primary opponent is overflowed: `_villain_chain_overflowed=True` (any-overflow fires) → blocker features NaN-flagged. Whether this is desired depends on whether "any opp overflowed → blocker unreliable" is correct semantics — but spec doesn't say it is.

**Production risk:** Stage 5 retrain feature regeneration on commit-14-era multiway training rows. Model trains on aggregate-flag-driven NaN labels.

**Fix (cross-stream coordination):** logic + teaching agree on aggregate semantics. Either:
- Aggregates = primary-villain-only (logic + teaching both update)
- Aggregates = any/all per §3.7 (logic + teaching both adopt; document contract)

## MEDIUM / LOW / NIT

- **MEDIUM:** all-zero composition for folded/overflowed opponents is semantically ambiguous with valid all-air range (consumers must use `_per_villain_folded`/`_per_villain_overflowed` sentinels to disambiguate)
- **MEDIUM:** `num_opponents` vs `len(opponent_positions)` no length guard at MW gate
- **LOW:** `_chain_method` telemetry asymmetry between HU and MW branches
- **NIT:** partition-leak hardening for future-9th-classify_hand-category

## Recommendations (advisory)

1. **Pre-Stage-5-retrain housekeeping commit** could bundle HIGH-1/2/3 (one-line fixes each + tests, ~1-2h total) plus the previously-flagged audit-runner immutability patch (Phase 1 HIGH). HIGH-4 needs cross-stream alignment first.

2. **HIGH-4 cross-stream coordination:** logic builder + teaching builder agree on aggregate semantics before either side fixes alone.

3. **Stage 4 pilot dispatch awareness:** if pilot agents extract features on shared hand objects with mutated AH (likely for multi-street labelling), HIGH-3 cache poisoning is a live risk. Either patch HIGH-3 first OR document cache-immutability contract in pilot orchestration spec.

4. **No rollback or revert needed.**

## Multi-expert convergence (TC-15 third demonstration)

Empirical-fixture framing CONVERGED with static-analysis-adversarial framing on basic invariants (PASS). Static-analysis framing surfaced 4 HIGH defensive-shielding gaps that empirical fixtures don't reach (DIVERGED — exactly the protocol-diversity outcome). Both framings worth keeping for future TC-11 dispatches.

## STOP-condition assessment

No STOP triggered. No verdict claim is empirically false. All findings are forward-looking hardening; production correctness intact.

## Reference

- Full finding: `~/river-rats-qc/findings/2026-04-26-commit14-arch-stress.md`
- Phase 2 finding (HIGH-4 here = §3.7 in Phase 2): PR #19 + `~/river-rats-qc/findings/2026-04-26-commit14-contract-drift.md`
- Phase 1 finding: PR #17 + `~/river-rats-qc/findings/2026-04-26-audit-trail-pr5-pr9.md`
- Orchestrator Phase 1 ACK: `MAIN_TERMINAL_QC_FINDING_ACK_AUDIT_RUNNER_2026-04-26.md` (`efd92ed`)

**Phase 3 status: COMPLETE.** QC HOLDs after publication for orchestrator triage of accumulated findings before resuming continuous monitoring (Phase 4 requires owner setup of /loop on QC terminal anyway).
