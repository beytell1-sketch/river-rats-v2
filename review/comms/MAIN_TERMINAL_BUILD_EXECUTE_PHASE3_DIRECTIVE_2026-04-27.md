---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (builder; named author) · Reviewer streams · QC stream · Owner
re: Phase 3 directive — Path A unblock E2-A; add --positions flag to generate_corpus_revision_pool.py; standard code-change PR cycle
status: DIRECTIVE — Phase 3 build (small code change) + completion of E2-A + C2 + full data PR
---

# Phase 3 build directive — Path A: add `--positions` flag

## Context

Builder report at master `5685605` confirmed: E1 + E2-B + E3 all PASS; E2-A BLOCKED on missing `--positions` flag (UTG hardcoded → 0 records). Builder offered Path A (add flag to existing script) or Path B (driver script). C2 blocked on E2-A.

**Orchestrator decision: Path A.** Cleaner long-term API; future Mode A generation needs this flag regardless; quality-first per memory `feedback_quality_default_no_ask.md`. Partial data PR rejected — 215 hands is not the 500-hand target; we must complete E2-A before round 3 review.

## Authorization

This directive authorizes the builder to **author a small code change** (add CLI flag + plumb through to `_generate_mode_a()`). Per CLAUDE.md §1 + memory `feedback_listen_to_orchestrator_always.md`: orchestrator-named-author directive is sufficient authorization.

## Code change spec

### File 1: `river-rats-core/generate_corpus_revision_pool.py`

Add a `--positions` argument to the argparse (mode A only). Default: `'CO,BTN,BB'` (the 3 positions where Mode A self-play yields actual decisions per Phase 2 Q3). Plumb through to `_generate_mode_a()` so it iterates over the comma-split list, calling `SelfPlayRunner` once per position with `single_position=<pos>`.

```python
# argparse:
parser.add_argument(
    '--positions',
    type=str,
    default='CO,BTN,BB',
    help='Comma-separated list of single-positions for Mode A self-play '
         '(default: CO,BTN,BB; UTG yields 0 records due to preflop fold)'
)

# _generate_mode_a signature:
def _generate_mode_a(num_deals: int, seed: int, positions: List[str], ...) -> List[dict]:
    records = []
    deals_per_position = num_deals // len(positions)
    for pos in positions:
        runner = SelfPlayRunner(..., single_position=pos)
        # existing per-runner record collection
        records.extend(per_pos_records)
    return records
```

Forbidden_fingerprints threading remains incremental across positions (each position adds to the disjointness set before the next position runs).

### File 2: `river-rats-core/tests/test_corpus_revision_v3.py` — add a test

```python
class TestModeAPositionsFlag:
    def test_positions_flag_default_excludes_utg(self):
        # default 'CO,BTN,BB' should not include UTG
        ...
    def test_positions_flag_distributes_deals(self):
        # num_deals=300 with 3 positions → 100 deals per position
        ...
    def test_mode_a_with_co_position_yields_records(self):
        # smoke test: invoke generate_pool(mode='a', positions=['CO'], deals=50) → ≥1 record
        ...
```

3 tests minimum; add live smoke test (#3) to catch regressions in the CO position pathway.

### Do NOT change

- `_generate_mode_b()` — unchanged
- `extract_all_features()` — unchanged
- Output record schema — unchanged
- Phase 2 F1 short-form key handling — unchanged (verify your change doesn't accidentally regress F1)

## Verification gate (before opening PR)

1. `python -m pytest river-rats-core/tests/test_corpus_revision_v3.py` — all 43 prior tests still pass + 3 new tests pass = 46 passed (or 51 if old skips graduate). Report exact counts.
2. `python river-rats-core/generate_corpus_revision_pool.py --mode a --deals 30 --positions CO --seed 99 --output /tmp/smoke.jsonl` → ≥1 record produced; SPR mean ≥ 4.0 BB-unit.
3. `python river-rats-core/generate_corpus_revision_pool.py --mode a --deals 300 --positions CO,BTN,BB --seed 99 --output /tmp/smoke3.jsonl` → SPR distribution looks reasonable; no chip-unit values (mean ≥ 4.0).
4. `python river-rats-core/generate_corpus_revision_pool.py --help` shows `--positions` flag with CO,BTN,BB default.

## PR

- Branch: `programmer/mode-a-positions-flag-2026-04-27`
- Files: `generate_corpus_revision_pool.py` + test additions only — no other changes
- PR title: `Builder Phase 3: add --positions flag to generate_corpus_revision_pool.py (Mode A position selection)`
- Body: explain the bug it unblocks (Phase 2 Q3 + Phase 3 BLOCKED), reference build-execute directive
- DO NOT push directly to master (builder's prior commit `5685605` was a comm-only push that violated PR workflow per CLAUDE.md §1+§9 — flag for the future, but not blocking this cycle)

## Round 3 review on the flag PR

Two reviewers (gto-expert is overkill for a flag change):

1. **ml-architect**: API design of the flag, plumbing through to `_generate_mode_a()`, F1 regression check (Mode A's short-form key handling MUST still work for all positions). Live test (verification gate #3) sanity check.
2. **QC**: paired V-Implementation-Spec-Match (flag present at canonical paths; tests cover the intended bug) + V-Integration-Trace (CO position → SelfPlayRunner → records yielded with BB-unit SPR end-to-end). Per memory `feedback_qc_required_before_approval.md`, QC must weigh in before merge.

If gto-expert auto-picks-up via their own /loop, fine — but orchestrator does not pre-emptively dispatch gto-expert for this flag-change cycle.

## After flag PR merges

Builder runs in this exact order:

1. `git pull --ff-only origin master`
2. `python river-rats-core/generate_corpus_revision_pool.py --mode a --deals 1000 --positions CO,BTN,BB --seed 2026 --output data/corpus_revision_pool_mode_a_2026-04-27.jsonl`
3. **E2-A verification gate**: ≥100 records, no SPR < 2.0 with pot > 6.0 (N1 smoke), no within-mode dupes, no Mode A↔Mode B fingerprint dupes
4. `python scripts/build_corpus_revision_500_hand.py --pilot-input data/pilot_corpus_100_hand_2026-04-26_v2.jsonl --pool-mode-a data/corpus_revision_pool_mode_a_2026-04-27.jsonl --pool-mode-b data/corpus_revision_pool_mode_b_2026-04-27.jsonl --output data/corpus_revision_500_hand_2026-04-27.jsonl --lock-file data/corpus_revision_500_hand_2026-04-27.lock`
5. **C2 verification gate**: 500 records, OOP 0.55-0.65, IP 0.35-0.45, all 12 quotas filled (NFD-boundary slot expected understocked at ≤4 per gto-expert disposition — flag in report, not blocker), lock SHA256 present
6. **Verify NIT from Phase 3 report:** the directive's E3 CLI spec was wrong (`--base-model`/`--corpus-sample`); actual flags are `--model`/`--feature-keys`. Re-run E3 with correct flags as a sanity check (already PASSed via graceful skip, but re-verify).

Then open the **full data PR**:
- Branch: `programmer/corpus-revision-execution-2026-04-27`
- Files: all data files (pilot v2, mode A pool, mode B pool already on master, 500-hand corpus, lock file) + this final report at `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_FINAL_2026-04-27.md`
- DO NOT include code changes (those went through the flag PR cycle separately)

Round 3 review chain on the full data PR:
- gto-expert: spot-check 10-15 records across families for poker realism
- ml-architect: feature-distribution checks (SPR histogram, IS_PFA distribution, 59 keys, no NaNs)
- QC: paired V-Impl-Spec-Match + V-Integration-Trace on the final lockfile + a sample re-extraction trace

## Why this sequencing (small code PR before full data PR)

- Code changes go through their own review cycle so reviewers can isolate code concerns from data concerns
- The flag is reusable — once merged, future Mode A regenerations just call with `--positions`
- Full data PR is data-only → faster review, smaller blast radius, easier to merge

## Pipeline state right now

- E1 ✓ output on disk: `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl`
- E2-B ✓ output on disk: `data/corpus_revision_pool_mode_b_2026-04-27.jsonl`
- E2-A 🚫 blocked → unblocks via this directive's flag PR
- E3 ✓ verified (re-run after flag PR merges; trivial)
- C2 🚫 blocked → unblocks after E2-A → runs in step 4 above

## NIT items I'll fix after this cycle

- Directive E3 CLI spec mismatch (will correct in next directive)
- The `5685605` direct master push was protocol-incorrect (programmer report should have come via PR per PR workflow); document for future

## References

- Builder Phase 3 report: `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md` (master `5685605`)
- Build-execute directive: `MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`)
- Phase 2 round 2 synthesis: `MAIN_TERMINAL_PR60_PHASE2_SYNTHESIS_2026-04-27.md` (master `8621f9a`)
- Phase 2 builder report: `PROGRAMMER_REPORT_BLUEPRINT_V3_PHASE2_2026-04-27.md` (Q3 = the original UTG observation)
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`

**Status: PHASE 3 DIRECTIVE OPEN. Builder authors flag PR (Mode A `--positions` flag); ml-architect + QC review; merge; then E2-A + C2 run; full data PR opens; round 3 reviews chain dispatches.**
