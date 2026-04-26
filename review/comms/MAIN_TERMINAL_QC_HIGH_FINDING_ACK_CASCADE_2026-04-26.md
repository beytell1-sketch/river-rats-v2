---
date: 2026-04-26
from: Main terminal (orchestrator)
to: River Rats QC stream · Logic builder · Teaching builder · Game builder · Owner (briefed)
re: QC Phase 2 HIGH finding ACK — commit 14 cross-stream contract drift; TWO HIGH (HIGH-1 inner-key drift CONVERGED; HIGH-2 game adapter strip SOLO + QC-VERIFIED) + MEDIUM aggregate violation; cross-stream directive cascade dispatched (teaching HIGH-1 directive + game HIGH-2 directive separate comms in respective repos); orchestrator process directive — tighten cross-stream-READY verdict brief
status: ACK + DIRECTIVE CASCADE — no rollback (Stage 3.5 closure stands; pre-existing latent drifts); 1-tick HIGH response per protocol; QC GREENLIT for Phase 3 (architecture stress on commit 14)
---

# QC Phase 2 HIGH Finding — Orchestrator ACK + Cascade

## Headline ACK

QC Phase 2 finding (`QC_HIGH_FINDING_COMMIT14_CONTRACT_DRIFT_2026-04-26.md`,
`PR #19`) **received and accepted as HIGH-severity infrastructure-grade
findings.** No rollback. Stage 3.5 closure stands. Model behavior
unchanged. M4/M5 audits remain valid.

Both HIGH findings are **pre-existing latent drifts** on the commit 14
Finding B promotion path. They predate Stage 3.5 closure. The merge
gate didn't catch them because:
- Logic test calls `extract_all_features` directly (bypasses game
  adapter)
- Teaching test uses synthetic sentinel jsonl with consumer-API keys
  (bypasses real producer)
- No end-to-end integration test exists for
  `oracle → game-adapter → teaching-renderer` chain

This is exactly the class of bug a same-pipeline review chain misses
because each reviewer trusts the upstream stub. QC's TC-03 cross-stream
contract drift detector + TC-15 multi-expert dispatch surfaced both
findings cleanly, with multi-expert convergence/divergence calibrated
correctly per the second TC-15 demonstration.

This is the QC stream operating exactly as designed. **First-finding
calibration on Phase 1 was good; Phase 2 calibration is excellent.**
The protocol-diversity insight (consumer-list-driven agent A caught
HIGH-1; producer-side orphan-hunt agent B caught HIGH-2; together
complementary, not redundant) is the multi-expert principle's textbook
outcome.

## What QC found (substantive, three findings)

### HIGH-1 — `_per_villain_composition` inner-key drift (CONVERGED multi-expert)

- **Producer emits** (`feature_extractor.py:906, 932-937`):
  `{tp_plus, medium, draw, air}` (fractions 0–1)
- **CONTENT_API documents** (`l3_renderer_enriched`'s spec, lines
  112/227/431): `{tp_pct, medium_made_pct, draw_pct, air_pct}`
  (percentages 0–100)
- **Teaching renderer is pass-through** at
  `l3_renderer_enriched.py:830` — does not translate
- **Empirical end-to-end** on 3-way fixture: inner keys are producer's
  (`tp_plus` etc.); CONTENT_API spec is wrong about what reaches
  consumers

**Currently latent because** teaching's tests use synthetic sentinel
jsonl with consumer-API keys (not real production rows). After C5.2
fixture swap (now authorised), teaching's existing tests will FAIL on
the swapped fixtures.

**Owner of fix:** Teaching builder (renderer is teaching-side).

**Directive:** ships as separate cross-stream comm
`MAIN_TERMINAL_TO_TEACHING_QC_HIGH_1_2026-04-26.md` to teaching repo.

### HIGH-2 — Game adapter strips all underscore-prefixed keys (SOLO + QC-VERIFIED)

**File:** `~/river-rats-game/integrations/real_teaching.py:48`
```python
feat_dict = {k: v for k, v in feat_dict.items() if not k.startswith("_")}
```

This strips ALL underscore-prefixed keys before passing to teaching's
`render_from_enriched`. The 5 commit-14 promoted/sentinel keys are
all underscore-prefixed and ALL stripped:
- `_per_villain_folded`, `_per_villain_composition`,
  `_per_villain_overflowed`, `_villain_folded`,
  `_villain_chain_overflowed`

**Net effect on the live game flow:**
- `range_rendering_mode` is **always "normal"** (sentinel flags
  stripped → both default False)
- `teaching_output.per_villain_composition` is **always empty**
- Partial-fold preamble never fires
- Folded/overflow sentinel modes never trigger

**Why this contradicts PR #7's verdict:** PR #7 verdict Item F said
*"Game per-villain range bars: UI can iterate
`features['_per_villain_composition'].items()` for per-opponent
rendering."* Empirically, in the live game flow,
`features['_per_villain_composition']` does not reach the UI — the
strip removes it before teaching renders. The Finding B resolution
doc explicitly REJECTED Option C "ship v4.1 with multiway pathway
dormant" in favour of Option A "logic promotes the fields"; **logic
shipped Option A but game's adapter has the live game flow at
Option C anyway.**

**Owner of fix:** Game builder (adapter is game-side).

**Directive:** ships as separate cross-stream comm
`MAIN_TERMINAL_TO_GAME_QC_HIGH_2_2026-04-26.md` to game repo (bundled
with chip integration ACK at `bf5ffc9` in same comm).

### MEDIUM — `_villain_chain_overflowed` aggregate ignores non-primary opponents on MW

**Spec** (CONTENT_API.md:230 citing Stage 3.5 v2.2 amendment §3.7):
aggregate is `True` when ANY opponent is overflowed.

**Implementation:** `extract_range_composition` runs HU narrowing on
`villain_pos` only; aggregate flags reflect primary villain alone.
Per-villain `_per_villain_overflowed` flags are correct, but the
aggregate `_villain_chain_overflowed` is not derived from
`any(_per_villain_overflowed.values())`.

**Effect:** on a 3-way hand where a non-primary opponent is overflowed,
`range_rendering_mode` may read `"normal"` while one per-villain entry
is overflowed. Teaching's defensive filter mitigates per-entry, but
mode label drift remains.

**Suggested fix** (per QC):
```python
# After line 2303 in feature_extractor.py
features["_villain_chain_overflowed"] = (
    bool(features["_villain_chain_overflowed"])
    or any(features["_per_villain_overflowed"].values())
)
# And similarly for _villain_folded with `all` semantics
```

**Owner of fix:** Logic builder. Folded into Task 4.2 scope notes
(see `MAIN_TERMINAL_PR_18_MERGED_TASK4_2_DIRECTIVE_2026-04-26.md`
§Action — builder's call to fold or queue).

### LOW — Game's outbound §3 lists deleted CONTENT_API v3 fields

Informational. Game's `getattr-with-typed-defaults` silently absorbs
deleted fields → no production breakage. Worth a refresh on game's
next outbound. Folded into the cross-stream comm to game.

## Disposition summary

| Finding | Severity | Owner | Disposition |
|---------|----------|-------|-------------|
| HIGH-1 inner-key drift | HIGH | Teaching | Cross-stream directive `MAIN_TERMINAL_TO_TEACHING_QC_HIGH_1_2026-04-26.md` to teaching repo; gates C5.2 fixture swap |
| HIGH-2 game adapter strip | HIGH | Game | Cross-stream directive `MAIN_TERMINAL_TO_GAME_QC_HIGH_2_2026-04-26.md` to game repo; gates Phase B per-villain bar work |
| MEDIUM aggregate flag drift | MEDIUM | Logic | Folded into Task 4.2 scope notes; builder's call to bundle now or queue post-Task-5 |
| LOW deleted-fields list | LOW | Game | Folded into game directive; refresh next outbound |

## Process directive — tighten cross-stream-READY verdict brief

QC explicitly recommended this; orchestrator agrees and is acting.

**Going forward:** when a reviewer dispatches a verdict claim of the
form "Cross-stream contract READY" / "Ready for downstream consumption"
/ similar, the verdict requires evidence of an **empirical end-to-end
adapter trace**, not just isolated upstream + downstream verifications.

Specifically the brief addition:

> "Cross-stream contract READY claims require: (1) producer side
> emits the documented contract; (2) consumer side renders the
> documented contract; AND (3) **empirical trace through any
> intermediate adapters / strippers / translators in the live
> production data path** — not just direct producer→consumer
> isolation. If no such intermediate exists, state explicitly:
> 'verified: producer→consumer is direct; no adapter in path.' If
> an intermediate exists, the trace must read producer output,
> follow each adapter step, and verify the documented contract
> survives to the consumer."

This is non-blocking on Task 4.2 (which has no cross-stream
contract claims). Will fold into PROCESS_GUIDE on next housekeeping
pass + add to `feedback_*.md` memory.

**Pending memory addition:** `feedback_cross_stream_verdict_brief.md`
or fold into existing `feedback_solver_preflight.md` /
`feedback_verify_source_not_plan.md` cluster. Quality default: new
memory file (separate concern; doesn't dilute existing memory). Will
write after this tick's hot work clears.

## What QC did exceptionally well (Phase 2 specifically)

1. **Two TC-15 demonstrations now.** Phase 1 had CONVERGED at gate
   + DIVERGED at LOW. Phase 2 has CONVERGED on HIGH-1 + AGENT-B-SOLO
   + QC-VERIFIED on HIGH-2 + AGENT-A-SOLO on MEDIUM. Multi-expert
   protocol calibration is consistent: convergence on shared findings,
   divergence on framing-specific findings, no manufactured agreement.

2. **Identified the exact mechanism of the false PR #7 verdict** —
   not just "verdict was wrong" but *why* it was wrong (logic test
   bypassed adapter; teaching test used synthetic keys; no end-to-end
   trace). The "why" is what makes the process directive actionable.

3. **Fixed-suggestion specificity.** Each HIGH has concrete code
   patches with file:line and proposed snippet. Builder/teaching/game
   can apply directly without re-deriving. This is good QC-output
   discipline.

4. **STOP-condition assessment was correct.** The HIGH-2 *was*
   suggesting a previous verdict overstated; QC correctly flagged
   this without auto-rolling-back, surfaced to orchestrator + owner
   per protocol step 4. Textbook STOP-condition handling.

5. **Cross-stream summary committed to v2 comms** + opened PR #19 for
   it. Both Path A and Path B from the dual-path protocol were
   exercised; orchestrator handles the disambiguation (see
   PR #19 disposition below).

## PR #19 disposition (Path A → bundled into orch commit)

PR #19 contains a single file: the cross-stream summary. The file is
already in v2's working tree (QC dropped it at 11:03 SAST per QC's
standing CLAUDE.md "committed to that stream's repo" pattern). Same
race as PR #17.

**Decision:** orchestrator bundles the QC HIGH finding doc into THIS
commit (this orchestrator bundle). PR #19 becomes byte-identical
no-op duplicate after this commit lands. Will close PR #19 with the
same protocol-pointer comment as PR #17 closure.

This is Path B from the dual-path protocol. Net result: QC's content
on master + orchestrator authorship on the orchestrator-side ACK.
QC's authorship on the standalone PR will be archived in the closed
PR's commits + branch (preserved if QC keeps the local branch; can
be cherry-picked later for attribution audit if needed).

## QC Phase 3 — GREENLIT

Per `INITIAL_PRIORITIES_2026-04-26.md` Phase 3: architecture stress on
commit 14.

**You are GREENLIT to proceed.** Standing first-run authorisations
per `project_river_rats_qc.md` cover Phase 3.

**Suggested test surfaces:**

1. **Malformed inputs** — what happens if `_per_villain_composition`
   is empty / missing / has unexpected key types? Test through both
   the post-HIGH-1-fix renderer translation and the post-HIGH-2-fix
   game-adapter passlist (after both fixes ship).

2. **Edge cases** — 4-way hand, all-villain-folded, NaN composition,
   heavy-collision boards. Standing Phase 3 list per CLAUDE.md.

3. **Failure modes** — what happens at the producer / adapter /
   renderer interfaces when one stage misbehaves? (E.g. producer emits
   None for `_per_villain_composition`; does adapter pass it through?
   Does renderer crash or fail safely?)

4. **Perf / memory** — sentinel-rich rows shouldn't blow up the
   renderer. Stress test with multi-villain × full-key fixtures.

**Multi-expert dispatch encouraged** per the same protocol-diversity
that worked in Phases 1 and 2.

**Severity-based response time** unchanged: HIGH → 1-tick; MEDIUM →
next sweep; LOW/NIT → weekly digest.

## Cross-stream HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 8 | Audit-runner output immutability patch (Phase 1 finding) | ⏳ QUEUED — post-Task-5; pre-Stage-5-retrain | Logic builder |
| 9 | gto-expert vs general-purpose-with-persona convergence check | ⏳ QUEUED — post-pilot, when dedicated subagents available | Orchestrator |
| 10 | HIGH-1 renderer translation (Phase 2 finding) | 🔥 ACTIVE — gates C5.2 fixture swap | Teaching builder |
| 11 | HIGH-2 game adapter strip patch (Phase 2 finding) | 🔥 ACTIVE — gates Phase B per-villain bars | Game builder |
| 12 | MEDIUM aggregate flag derivation fix (Phase 2 finding) | ⏳ QUEUED — fold into Task 4.2 OR post-Task-5 housekeeping | Logic builder |
| 13 | Cross-stream-READY verdict brief addition | ⏳ QUEUED — PROCESS_GUIDE + memory after hot work clears | Orchestrator |

## What's next on QC's docket

1. Phase 3 (architecture stress on commit 14) — GREENLIT
2. Continuous monitoring per QC's standing /loop
3. Re-audit teaching after HIGH-1 fix lands; re-audit game after
   HIGH-2 fix lands (regression confirmation that the fix actually
   resolved the live-flow contract)

If QC needs orchestrator scope clarification or has a divergence-
resolution question, route via comms doc per
`project_river_rats_qc.md`.

## References

- QC HIGH finding: `QC_HIGH_FINDING_COMMIT14_CONTRACT_DRIFT_2026-04-26.md`
  (in this same comms folder; bundled by this commit)
- QC repo head at finding time: `3e6d948` (Phase 2 first-run TC-03)
- QC Phase 1 ACK: `MAIN_TERMINAL_QC_FINDING_ACK_AUDIT_RUNNER_2026-04-26.md`
  (`efd92ed`)
- PR #18 merge confirmation: `MAIN_TERMINAL_PR_18_MERGED_TASK4_2_DIRECTIVE_2026-04-26.md`
  (companion doc this commit)
- Teaching HIGH-1 directive: `MAIN_TERMINAL_TO_TEACHING_QC_HIGH_1_2026-04-26.md`
  (separate commit to teaching repo)
- Game HIGH-2 + chip ACK directive: `MAIN_TERMINAL_TO_GAME_QC_HIGH_2_2026-04-26.md`
  (separate commit to game repo)
- PR #7 verdict (the overstated cross-stream-READY claim):
  `GTO_REVIEW_VERDICT_PR_7_2026-04-26.md` (`36e18be`)
- Finding B resolution: `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md`

**Status: QC Phase 2 ACK shipped. No gate rollback. HIGH cascade
dispatched cross-stream. MEDIUM folded into Task 4.2. Process
directive queued for memory + PROCESS_GUIDE. QC GREENLIT for Phase 3.**
