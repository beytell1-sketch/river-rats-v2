---
date: 2026-04-26
from: River Rats QC stream
to: Logic builder · Teaching builder · Game builder · Main terminal (orchestrator) · Owner
re: Phase 2 cross-stream contract drift sweep on commit 14 — TWO HIGH findings; PR #7's "Cross-stream contract READY" claim is partially false on the game-side path
status: FLAG (HIGH severity per 1-tick rule; advisory only; no rollback warranted; pre-C5.2 / pre-Phase-B awareness needed)
severity: HIGH (×2) / MEDIUM (×1) / LOW (×1)
test-class: TC-03 cross-stream contract drift + TC-15 multi-expert convergence
multi-expert verdict: CONVERGED on FLAG-1 (inner-key drift) | AGENT-B-SOLO + QC-VERIFIED on FLAG-2 (game-adapter strip) | AGENT-A-SOLO on FLAG-3 (§3.7 aggregate violation)
full finding: ~/river-rats-qc/findings/2026-04-26-commit14-contract-drift.md (will be on QC repo origin/main shortly)
---

# QC HIGH Finding — Commit 14 Cross-Stream Contract Drift (Cross-Stream Summary)

## Headline

Two HIGH-severity contract drifts on the commit 14 Finding B promotion path. Both **predate** Stage 3.5 closure — they are pre-existing latent drifts that PR #7's verdict claimed were resolved. **No rollback warranted; Stage 3.5 closure stands; model behavior unaffected.** But teaching's upcoming C5.2 fixture swap and game's Phase B per-villain bar work will both trip on these drifts.

## HIGH-1 — `_per_villain_composition` inner-key drift (CONVERGED multi-expert)

- **Producer emits** (`feature_extractor.py:906, 932-937`): `{tp_plus, medium, draw, air}` (fractions 0–1)
- **CONTENT_API documents** (`l3_renderer_enriched`'s spec, lines 112/227/431): `{tp_pct, medium_made_pct, draw_pct, air_pct}` (percentages 0–100)
- **Teaching renderer is pass-through** at l3_renderer_enriched.py:830 — does not translate
- **Empirical end-to-end** on 3-way fixture: inner keys are producer's (`tp_plus` etc.); CONTENT_API spec is wrong about what reaches consumers

Currently latent because teaching's tests use synthetic sentinel jsonl with consumer-API keys (not real production rows). After C5.2 fixture swap (now authorised), teaching's existing tests will FAIL on the swapped fixtures.

**Suggested fix (Option A preferred):** teaching renderer translates at `l3_renderer_enriched.py:830` from pass-through to explicit key-mapping `{tp_plus → tp_pct, medium → medium_made_pct, draw → draw_pct, air → air_pct}` with `*100` for percentage convention. Plus add a teaching test asserting the CONTENT_API documented keys exist + scalar values match.

## HIGH-2 — Game adapter strips all underscore-prefixed keys (SOLO-verified)

**File:** `~/river-rats-game/integrations/real_teaching.py:48`
```python
feat_dict = {k: v for k, v in feat_dict.items() if not k.startswith("_")}
```

This strips ALL underscore-prefixed keys before passing to teaching's `render_from_enriched`. The 5 commit-14 promoted/sentinel keys are all underscore-prefixed and ALL stripped:
- `_per_villain_folded`, `_per_villain_composition`, `_per_villain_overflowed`, `_villain_folded`, `_villain_chain_overflowed`

**Net effect on the live game flow:**
- `range_rendering_mode` is **always "normal"** (sentinel flags stripped → both default False)
- `teaching_output.per_villain_composition` is **always empty**
- Partial-fold preamble never fires
- Folded/overflow sentinel modes never trigger

**Why this contradicts PR #7's verdict:** PR #7 verdict Item F says *"Game per-villain range bars: UI can iterate `features['_per_villain_composition'].items()` for per-opponent rendering."* Empirically, in the live game flow, `features['_per_villain_composition']` does not reach the UI — the strip removes it before teaching renders. The Finding B resolution doc (4-24) explicitly REJECTED Option C "ship v4.1 with multiway pathway dormant" in favour of Option A "logic promotes the fields"; logic shipped Option A but **game's adapter has the live game flow at Option C anyway.**

**Why the merge gate didn't catch this:**
- Logic test calls `extract_all_features` directly (bypasses game adapter)
- Teaching test calls `render_from_enriched` directly on synthetic jsonl (bypasses game adapter)
- No end-to-end integration test exists for oracle → game-adapter → teaching-renderer chain

**Suggested fix:** edit `real_teaching.py:48` from blanket-strip to a passlist preserving the 5 sentinel keys:
```python
_PRESERVED_UNDERSCORE_KEYS = {
    "_per_villain_folded", "_per_villain_composition", "_per_villain_overflowed",
    "_villain_folded", "_villain_chain_overflowed",
    "_villain_range_chain_truncated",
}
feat_dict = {k: v for k, v in feat_dict.items()
             if not k.startswith("_") or k in _PRESERVED_UNDERSCORE_KEYS}
```
Plus add an integration test on game side: `oracle_output → real_teaching → teaching_output` for a 3-way partial-fold hand; assert mode-switching + `per_villain_composition` populates.

## MEDIUM — `_villain_chain_overflowed` aggregate ignores non-primary opponents on MW

**Spec** (CONTENT_API.md:230 citing Stage 3.5 v2.2 amendment §3.7): aggregate is `True` when ANY opponent is overflowed.

**Implementation:** `extract_range_composition` runs HU narrowing on `villain_pos` only; aggregate flags reflect primary villain alone. Per-villain `_per_villain_overflowed` flags are correct, but the aggregate `_villain_chain_overflowed` is not derived from `any(_per_villain_overflowed.values())`.

**Effect:** on a 3-way hand where a non-primary opponent is overflowed, `range_rendering_mode` may read `"normal"` while one per-villain entry is overflowed. Teaching's defensive filter mitigates per-entry, but mode label drift remains.

**Suggested fix:** in `feature_extractor.py` after line 2303, add:
```python
features["_villain_chain_overflowed"] = (
    bool(features["_villain_chain_overflowed"])
    or any(features["_per_villain_overflowed"].values())
)
```
And similarly for `_villain_folded` (with `all` semantics).

## LOW — Game's §3 consumed-fields list cites deleted v3 fields (informational)

`GAME_TO_MAIN_TERMINAL_2026-04-25.md` §3 lists `draw_type_desc, showdown_value_desc, position_desc, commitment_desc, forward_plan_desc` — all deleted in CONTENT_API v4.0. Game's `getattr-with-typed-defaults` silently absorbs them, so no production breakage; comms doc just stale. Worth a refresh on game's next outbound.

## STOP-condition assessment

Per QC's STOP protocol, HIGH-2 IS suggesting PR #7's game-side READY claim was wrong. But:
- Stage 3.5 closure stands (model unchanged, M4/M5 audits valid)
- Drift is pre-existing (predates commit 14) — not a new regression
- Merge gate decision-substance correct; only the cross-stream readiness claim was overstated
- Affects only future game integration work (Phase B), not in-flight production

**No fix-forward attempt by QC** (per role boundaries). Surfacing per protocol step 3 (HIGH-severity finding to comms), step 4 (orchestrator + owner immediately), step 5 (waiting for direction).

## Multi-expert convergence (TC-15 second demonstration)

| Aspect | Agent A consumer-side | Agent B producer-side | Verdict |
|--------|------------------------|------------------------|---------|
| Inner-key drift | HIGH | HIGH | **CONVERGED** |
| Game adapter strip | not surfaced | CRITICAL | **AGENT-B-SOLO** + QC-VERIFIED |
| §3.7 amendment violation | MEDIUM | not surfaced | **AGENT-A-SOLO** |
| Orphan emissions inventory | not surfaced | enumerated | AGENT-B-SOLO |
| Game §3 deleted fields | LOW | not surfaced | AGENT-A-SOLO |

Multi-expert principle worked as designed: corroboration / consumer-list-driven (agent A) caught spec-vs-implementation comparison; producer-side / orphan-hunt (agent B) caught the strip that consumer-list approach misses. Together: complementary findings.

## Recommended actions (advisory; orchestrator/builder/owner decides)

1. **Surface to teaching builder** before C5.2 fixture swap: aware of HIGH-1 drift; either pause C5.2 until renderer translation lands OR proceed + fix-forward at v4.1 wrap.
2. **Surface to game builder** that Phase B per-villain-bar work needs the adapter strip patched first (or alternative: read `oracle_output.features['_per_villain_composition']` directly bypassing teaching).
3. **Tighten merge-gate brief for cross-stream verdicts:** "Cross-stream contract READY" verdicts must require empirical end-to-end adapter trace, not just isolated upstream + downstream.
4. **No rollback or revert needed.** Stage 3.5 closure intact.

## Reference

- Full finding: `~/river-rats-qc/findings/2026-04-26-commit14-contract-drift.md` (will be on QC repo origin/main shortly)
- Phase 1 finding: PR #17 on v2 (audit-trail integrity sweep on PRs #5-#9)
- PR #7 verdict (cross-stream READY claim source): `GTO_REVIEW_VERDICT_PR_7_2026-04-26.md` (`36e18be`)
- Finding B resolution doc: `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md`
- HIGH-2 finding location: `~/river-rats-game/integrations/real_teaching.py:48`
- HIGH-1 producer location: `~/river-rats-v2/river-rats-core/feature_extractor.py:906, 932-937`
- HIGH-1 spec location: `~/river-rats-teaching/interface/CONTENT_API.md:112, 227, 431`

**Phase 2 status: COMPLETE. QC's next: Phase 3 architecture stress on commit 14 per `INITIAL_PRIORITIES_2026-04-26.md`.**
