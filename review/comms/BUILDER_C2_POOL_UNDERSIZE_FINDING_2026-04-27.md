---
date: 2026-04-27
from: Lead-programmer (builder; this session — Pilot Orch terminal in author mode per user 12:30 SAST course-correction)
to: Main terminal (orchestrator) · Owner · QC stream
re: Phase 3 directive (Path A) ACK + critical C2 verification finding orchestrator hasn't yet seen — adding `--positions` flag will NOT unblock C2; pool is structurally undersized for Phase A category targets
status: ACK + FINDING — surfacing before authoring flag PR to save a wasted cycle; orchestrator path-decision check
---

# Phase 3 ACK + C2 pool-undersize finding

## Phase 3 directive ACK

Per `MAIN_TERMINAL_BUILD_EXECUTE_PHASE3_DIRECTIVE_2026-04-27.md` (master `2e317c5`): orchestrator chose Path A (add `--positions` flag to existing script) over Path B (workaround driver). Acknowledged. Per `feedback_listen_to_orchestrator_always.md` orchestrator directive sufficient.

## Race-condition disclosure

There's a timing overlap orchestrator should know about before I author the flag PR:

**Between 12:51 and 12:55 SAST**, I (this session) read `ORCHESTRATION_STATE_2026-04-27.md` (master `46818f5`) which **explicitly authorized the Path B workaround driver**: *"If the script has no `--positions` flag, write a small driver in `scripts/` for that — but flag it for orchestrator review before merging."* I executed Path B accordingly:
- Wrote `scripts/run_mode_a_pool_with_positions.py` (small monkey-patch driver; no production code modified)
- Ran E2-A → produced 212 Mode A records (CO 94 / BTN 42 / BB 76)
- Ran C2 → produced 313-record corpus (NOT 500-record target)
- Pushed all outputs to branch `programmer/corpus-revision-execution-2026-04-27` at commit `174bbc3` (NOT yet opened as PR per directive sequence)

**Orchestrator's Phase 3 directive at master `2e317c5` (13:04 SAST)** then chose Path A and stated *"Partial data PR rejected — 215 hands is not the 500-hand target"*. The Path B work I did pre-dates the Phase 3 directive — race-condition, not non-compliance. Per `feedback_listen_to_orchestrator_always.md` I'm now switching to Path A.

The Path B branch + commit can be discarded if you want a clean Path A-only history. Or kept as evidence that C2 verification fails regardless of which path produces the Mode A pool.

## CRITICAL FINDING: C2 fails on pool undersize, not on E2-A

**My already-completed C2 run (with valid Mode A pool of 212 records) produces this verification gate result:**

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total records | 500 (100 + 400) | **313** (100 + 213) | **FAIL** |
| OOP percentage | [0.55, 0.65] | **0.71** | FAIL |
| IP percentage | [0.35, 0.45] | **0.29** | FAIL |
| PFA c-bet (Rule 4) | 80 | **46** | UNDER |
| NFD RAISE (air ≥ 0.20) | 20 | **4** | UNDER |
| NFD CALL (air < 0.20) | 20 | **4** | UNDER |
| BAC (MW-30) | 20 | **9** | UNDER |
| **MAGG river (villain_agg ≥ 2)** | **40** | **0** | **CRITICAL — zero records** |
| Donk-bet defence | 25 | **15** | UNDER |
| SB-hero | 20 | **16** | UNDER |
| Medium SPR (2-4) | 40 | **11** | UNDER |
| Standard SPR (4-8) | 50 | 50 | ✓ |
| Monster facing bet | 20 | 20 | ✓ |
| Within-batch dupes | 0 | 0 | ✓ |
| Mode A ∩ Mode B fingerprint overlap | 0 | 0 | ✓ |

## Root cause

Phase A category targets sum to 355 hands; combined pool yields only 327 records (Mode A 212 + Mode B 115). Per-category gaps:

| Category | Phase A target | Mode B yield | Mode A yield (self-play, generic) | Achievable |
|----------|---------------|--------------|-----------------------------------|------------|
| PFA c-bet | 80 | 22 (pfa module) | low (self-play doesn't naturally PFA-tag) | ~46 |
| MAGG | 40 | 10 (magg module) | 0 (self-play doesn't produce 2-aggression river) | **10** |
| NFD RAISE | 20 | 11 (nfd module total) | low | 4 |
| NFD CALL | 20 | (shared with above) | low | 4 |
| BAC | 20 | 9 (bac module) | low | 9 |
| Donk | 25 | 15 (donk module) | 0 (donk patterns rare in self-play) | 15 |
| SB-hero | 20 | 12 (sb module) | low | 16 |

**Adding the `--positions` flag will NOT change Mode A's natural yield distribution** (Mode A produces general self-play decisions, not category-specific patterns). Mode A's contribution to PFA / MAGG / NFD-tagged / Donk / SB categories remains near-zero regardless of position selection.

## Implication

**Phase 3 (flag PR) alone is not sufficient to unblock C2.** After flag PR merges and Mode A re-runs with proper positions, C2 will likely produce the same 313-record corpus (or similar) with the same verification gate failures.

The structural root cause is **Phase A category targets exceed Mode B factory module yields by 2-4×**. Three options for orchestrator (revised from my v2 report):

### Path X (clean, recommended): expand Mode B factory scenario modules

Code-change PR cycle on `river-rats-core/corpus_revision_scenarios/*.py`:
- PFA module: 22 → 80+
- MAGG module: 10 → 40+
- NFD modules (RAISE + CALL + boundary): 11 → 50+
- Donk module: 15 → 25+
- SB module: 12 → 20+
- BAC module: 9 → 20+
- Rule 11 module: 10 → unchanged
- Monster module: 10 → 20+

Architect-level change. Estimated ~$50-100 cost + 2-4 hours wall-time for architect Phase 3-bis spec → programmer Phase 4 implementation → review → merge cycle. Cleanest path; addresses structural cause; produces clean 500-hand corpus matching blueprint design.

### Path Y (faster, lossy): reduce Phase A targets to match available pool

Update `scripts/build_corpus_revision_500_hand.py` Phase A quotas to match achievable yields. Loses the rebalanced distribution corpus revision was designed around. Total target reduces from 500 to ~350. Likely fails the corpus-revision project's stated quality bar.

### Path Z (mid): expand Mode A volume (more deals) + select Mode B module expansions

Combines Phase 3 (flag PR) with extra Mode A deal volume (`--deals 5000` instead of 1000 → ~1000 Mode A records) + targeted Mode B expansion of 1-2 worst-shortfall modules (MAGG 10→40, Donk 15→25). Saves architect cycle but doesn't fully resolve PFA/NFD shortfalls.

**Pilot Orch recommendation: Path X.** Per `feedback_quality_default_no_ask.md` slow/clean default. Path X is the only option that produces a clean 500-hand corpus matching blueprint v3 design.

## Next-action question for orchestrator

1. **Still proceed with Phase 3 flag PR?**
   - **Yes** → I author flag PR per directive; after merge re-run E2-A + C2; C2 will fail same way; orchestrator dispatches Phase 4 (Path X scenario expansion) addressing pool undersize. Adds 1-2 cycles.
   - **No** → orchestrator dispatches Phase 4 (Path X scenario expansion) directly; Phase 3 flag PR rolls into Phase 4 (or stays separate cycle for clean API). Saves 1-2 hours.

2. **Discard Path B branch `programmer/corpus-revision-execution-2026-04-27` at `174bbc3`?**
   - **Yes** → I delete branch; clean Path A-only history.
   - **No** → keep as draft for reference; orchestrator may want the C2 result evidence + workaround driver code as documentation.

3. **Path X / Y / Z choice?** (this is independent of the flag-PR question above)

## Action

**Orchestrator (me):**
1. Read this finding comm
2. Decide on Phase 3 vs Phase 4 jump (skip flag PR if Phase 4 will subsume it)
3. Decide on Path X / Y / Z for pool sizing
4. Decide on Path B branch retention vs discard
5. Dispatch revised directive with explicit next-action for builder

**Pilot Orchestrator (this session):**
1. Surfaced this finding (this commit)
2. Branch `programmer/corpus-revision-execution-2026-04-27` (Path B work at `174bbc3`) remains on origin in WIP/draft state — NOT yet opened as PR per directive sequence
3. Standby for orchestrator path decision before authoring Phase 3 flag PR (avoid wasted cycle on flag PR if C2 still blocks)

**QC stream:**
- Layer 3 watch may pick up this finding
- No QC action required until orchestrator path decision

## References

- Phase 3 directive: `MAIN_TERMINAL_BUILD_EXECUTE_PHASE3_DIRECTIVE_2026-04-27.md` (master `2e317c5`)
- Builder v2 report (full pipeline run with C2 results): `programmer/corpus-revision-execution-2026-04-27` branch at `174bbc3`
- Builder v1 report (E2-A blocked, before workaround): master `5685605`
- Build-execute directive: `MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`)
- Orchestration state (Path B authorization): `ORCHESTRATION_STATE_2026-04-27.md` (master `46818f5`)
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_queries_to_orchestrator.md`

**Status: PHASE 3 ACK + C2 POOL-UNDERSIZE FINDING SURFACED. Standby for orchestrator path decision (Phase 3 flag PR proceed vs Phase 4 jump; X/Y/Z pool sizing; Path B branch retention).**
