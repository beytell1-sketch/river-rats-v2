---
date: 2026-04-27
from: Lead-programmer (builder; this session — Pilot Orch terminal switched to author mode per user course-correction at 12:30 SAST)
to: Main terminal (orchestrator) · Owner · QC stream
re: Build-execute pipeline E1 → E2-B → E2-A (workaround driver) → E3 → C2 — full pipeline ran; C2 verification gate FAILS (313 records ≠ 500; multiple Phase A quotas underfilled); per directive STOP + escalate
status: BLOCKED — C2 verification gate failure: corpus pool structurally undersized for Phase A category targets (PFA 46/80, MAGG 0/40, BAC 9/20, etc.); per directive "STOP and report BLOCKED. Do NOT manually patch the corpus — escalate"
revision: v2 (supersedes original at master 5685605 — ORCHESTRATION_STATE explicitly authorized Path B workaround driver, so executed E2-A + C2)
---

# Programmer Report — Build-execute v2 (full pipeline run)

## Authorization

Per `MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`) + `ORCHESTRATION_STATE_2026-04-27.md` (master `46818f5`) which explicitly authorized the Path B workaround driver: *"If the script has no --positions flag, write a small driver in scripts/ for that — but flag it for orchestrator review before merging."*

Per memory `feedback_listen_to_orchestrator_always.md` orchestrator directive sufficient + `feedback_named_author_builds_not_polls.md` named author = author mode.

## Step results

### Step 1 — E1: re-extract 100-hand pilot corpus ✓ PASS

Output: `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` (173,267 bytes; SHA256 `1afe69e7fbfa7bebfa319595a121115da68c3dbac369bb8b12edbe5e5184e9af`)

Verification gate:
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Record count | 100 | 100 | ✓ |
| SPR mean | [5.0, 15.0] BB-unit | 11.989 | ✓ |
| `is_preflop_aggressor` count | ≥30 | 48 | ✓ |
| 3-bet edge cases | 3 SB-3bet → IS_PFA=0 | 3 detected | ✓ |
| Labels untouched | hash match | hash match | ✓ |

### Step 2 — E2-B: Mode B factory pool ✓ PASS

Output: `data/corpus_revision_pool_mode_b_2026-04-27.jsonl` (200,834 bytes; SHA256 `be0c7ce9dc28b6f06d6c7c9301d410c833c5a9988653717f54fdcea58eb3b40f`)

Verification gate:
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total records | 111 (per directive) / 115 (per per-module sum) | 115 | ✓ (matches per-module sum; directive's "111" arithmetic typo) |
| Family breakdown | pfa 22 / facing 16 / bac 9 / magg 10 / nfd 11 / monster 10 / rule11 10 / donk 15 / sb 12 | exact match | ✓ |
| Within-family fingerprint dupes | 0 | 0 | ✓ |
| NFD R4 ±0.03 gate | 4/5 boundary templates pass | 4/5 pass (T5 filtered, expected) | ✓ |
| MAGG `villain_aggression_count` at river | == 2 | 10/10 | ✓ |

### Step 3 — E2-A: Mode A self-play pool ✓ PASS via workaround driver

**NEW FILE — flagged for orchestrator review:** `scripts/run_mode_a_pool_with_positions.py` (driver script that monkey-patches `SelfPlayRunner.__init__` to override `single_position` per iteration; calls `_generate_mode_a` 3 times with CO/BTN/BB; combines records into single output file). No production code modified.

Driver invocation:
```
python3 scripts/run_mode_a_pool_with_positions.py \
  --positions CO,BTN,BB --deals 1000 --seed 20260427 \
  --output data/corpus_revision_pool_mode_a_2026-04-27.jsonl
```

Output: `data/corpus_revision_pool_mode_a_2026-04-27.jsonl` (SHA256 `c5d7f437475da1fead0cf7f9084af34684310a74d33091638001fbd593f2aef8`)

Verification gate:
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Mode A record count | ≥100 | 212 (CO 94 + BTN 42 + BB 76) | ✓ |
| SPR mean | [4, 16] BB-unit (NOT chip-unit 0.117-1.25) | 12.312 | ✓ |
| SPR < 2.0 (chip-unit indicator) | 0 | 0 / 212 | ✓ |
| N1 smoke check (spr<2.0 AND pot>6.0) | 0 violations | 0 | ✓ (F1 fix verified working) |
| Mode A vs Mode B fingerprint overlap | 0 | 0 (212 unique A; 115 unique B) | ✓ |
| Position distribution | n/a | BB 74 / BTN 66 / CO 36 / HJ 24 / UTG 12 (positional decisions across all players' perspectives in self-play) | informational |

### Step 4 — E3: schema compatibility verification ✓ PASS (graceful skip per C6 path)

**NIT for orchestrator:** Directive's CLI flag spec for E3 didn't match actual script. Used actual `--model` flag (directive specified `--base-model` and `--corpus-sample`).

Output exit 0; corpus 59-feature contract confirmed.

### Step 5 — C2: 500-hand corpus assembly 🚫 BLOCKED (verification gate FAIL)

**NIT:** Directive's CLI flag spec for C2 didn't match actual script. Directive: `--pool-mode-a`, `--pool-mode-b`, `--lock-file`. Actual: single `--pool` (combined), `--existing-corpus`, `--target-new`, `--seed`, `--output`, `--lock-output`. Pre-step: combined Mode A + Mode B into single pool file `data/corpus_revision_pool_combined_2026-04-27.jsonl` (327 records).

Invocation:
```
python3 scripts/build_corpus_revision_500_hand.py \
  --pool data/corpus_revision_pool_combined_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --target-new 400 --seed 20260427 \
  --output data/corpus_revision_500_hand_2026-04-27.jsonl \
  --lock-output data/corpus_revision_500_hand_2026-04-27.lock
```

Output: `data/corpus_revision_500_hand_2026-04-27.jsonl` (SHA256 `3f0ed144a7a79c53d3c095e905be7aad94e864e04f77c64a16f1d678da0bdec6`); lock file SHA256 `91c4d7d97282d733b7ab71eedfc548fdd2dcfe535d27a9b7014691870d3ae2bf`.

**Verification gate FAILS — multiple Phase A quotas underfilled + total < 500:**

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total records | 500 (100 + 400) | **313** (100 + 213) | **FAIL** |
| OOP percentage | [0.55, 0.65] | **0.71** | **FAIL** (above 0.65 strict gate per F3) |
| IP percentage | [0.35, 0.45] | **0.29** | **FAIL** (below 0.35 strict gate per F3) |
| PFA c-bet (Rule 4) | 80 | **46** | UNDER |
| NFD RAISE (air ≥ 0.20) | 20 | **4** | UNDER |
| NFD CALL (air < 0.20) | 20 | **4** | UNDER |
| NFD boundary | 10 | 6 | UNDER (acceptable per directive) |
| BAC (MW-30) | 20 | **9** | UNDER |
| Monster facing bet (MW-33) | 20 | 20 | ✓ |
| MAGG river (villain_agg ≥ 2) | 40 | **0** | **CRITICAL** (zero MAGG records) |
| Standard SPR (4-8) | 50 | 50 | ✓ |
| Medium SPR (2-4) | 40 | **11** | UNDER |
| Rule 11 boundary | 10 | 8 | UNDER |
| Donk-bet defence | 25 | **15** | UNDER (matches Mode B donk yield 15) |
| SB-hero sandwich | 20 | **16** | UNDER (Mode B SB yield 12 + Mode A SB) |
| Within-batch duplicates | 0 | 0 | ✓ |

**Phase B 8D stratification:** 45/45 selected from non-quota records. ✓

**Per directive's verification gate:** *"If verification fails: STOP and report BLOCKED. Do NOT manually patch the corpus — escalate."*

## Root cause analysis

The corpus pool is **structurally undersized for Phase A category targets**. The Phase A targets sum to 80+20+20+10+20+20+40+50+40+10+25+20 = 355 hands across 12 categories. The combined pool has only 327 records (212 Mode A + 115 Mode B), and the per-category yield is far below targets:

- **PFA 80 needed:** Mode B has 22 PFA. Mode A self-play does not naturally produce PFA-tagged records in sufficient volume.
- **MAGG 40 needed:** Mode B has 10 MAGG. Mode A produced 0 MAGG (self-play doesn't naturally produce 2-aggression river spots without orchestration).
- **NFD RAISE/CALL 20+20 needed:** Mode B has 11 NFD total (7 non-boundary + 4 boundary). Mode A has near-zero NFD-tagged records.
- **Donk 25 needed:** Mode B has 15 (donk_bet_defence is the only source); Mode A doesn't naturally produce donk patterns.

**Net: Phase A targets exceed Mode B yields by 2-4× per category, and Mode A's contribution to most Phase A categories is near-zero.**

## Two paths forward (orchestrator decision)

### Path X (clean): expand Mode B yields per category

The simpler fix is to revise the Mode B factory scenario modules to produce more records per family. E.g.:
- PFA module produces 22 → expand to 80+
- MAGG module produces 10 → expand to 40+
- Donk module produces 15 → expand to 25+
- NFD module produces 11 → expand to 40+

This is a code-change cycle on `river-rats-core/corpus_revision_scenarios/*.py` (or related scenario files). Standard per-batch protocol (review + QC + merge). Likely a Phase 3 directive to architect/programmer.

### Path Y (faster, lossier): reduce Phase A targets to match available pool

Update `scripts/build_corpus_revision_500_hand.py` Phase A quotas to match achievable yields (PFA 46, MAGG 10, NFD 6+4 = 10, etc.), reducing total target from 500 to ~350. Loses the rebalanced distribution the corpus revision was designed around.

### Path Z (mid): mixed — re-run Mode A with more deals + expand specific Mode B modules

E.g., run Mode A with `--deals 5000` instead of 1000 (5× more records ≈ 1000 total Mode A). Plus expand 1-2 Mode B modules where shortfall is most painful (MAGG, donk).

**Pilot Orch recommendation: Path X (clean)** per `feedback_quality_default_no_ask.md`. Path X addresses the structural cause and produces a clean 500-hand corpus matching blueprint design.

## Pipeline output state

| File | Size | SHA256 | Status |
|------|------|--------|--------|
| `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` | 173,267 | `1afe69e7...4e9af` | ✓ E1 |
| `data/pilot_corpus_100_hand_2026-04-26.lock.json` | (updated v2) | (per script) | ✓ E1 |
| `data/corpus_revision_pool_mode_b_2026-04-27.jsonl` | 200,834 | `be0c7ce9...3b40f` | ✓ E2-B |
| `data/corpus_revision_pool_mode_a_2026-04-27.jsonl` | (212 records) | `c5d7f437...2aef8` | ✓ E2-A (via Path B workaround driver) |
| `data/corpus_revision_pool_combined_2026-04-27.jsonl` | (327 records) | (intermediate) | (concat for C2 input) |
| `data/corpus_revision_500_hand_2026-04-27.jsonl` | (313 records — UNDER target) | `3f0ed144...0bdec6` | 🚫 C2 BLOCKED on quota underfill |
| `data/corpus_revision_500_hand_2026-04-27.lock` | (per script) | `91c4d7d9...3ae2bf` | 🚫 |
| `scripts/run_mode_a_pool_with_positions.py` | (NEW workaround driver) | (driver code) | flagged for orchestrator review |

## Wall-time + cost

- E1: ~5 sec
- E2-B: ~30 sec
- E2-A (Path B workaround): ~2-3 min (3 × 1000 self-play deals × ~1 min each, due to multiway equity sampling)
- E3: ~3 sec
- C2: ~5 sec
- Total wall-time: ~3.5-4 min
- Cost: ~$0 (no model API calls; deterministic generation only)

## Action

**Orchestrator (me):**
1. Choose Path X (expand Mode B yields, cleanest), Path Y (reduce targets, lossy), or Path Z (mixed)
2. Decide if data PR opens NOW (with 313-hand corpus, flagged BLOCKED) OR waits for resolution
3. Review + decide on workaround driver script `scripts/run_mode_a_pool_with_positions.py` retention vs replacement (orchestrator may want to dispatch a code-change PR adding `--positions` flag to `generate_corpus_revision_pool.py` and removing the driver)

**Pilot Orchestrator (this session):**
1. Surfaced this v2 report (this commit)
2. Will open data PR on branch `programmer/corpus-revision-execution-2026-04-27` with all output files + driver script + this report; PR will be marked DRAFT/WIP until C2 unblocked
3. Standby for orchestrator path decision (X / Y / Z)
4. On Path X resolution (Mode B scenario expansion): standby for code-change PR cycle, then re-run E2-B + C2 with expanded scenarios
5. On Path Z resolution: re-run E2-A with `--deals 5000` (or similar) + standby for Mode B module expansion subset

**QC stream:**
- Layer 3 watch may pick up this v2 report
- Round-3 review on data PR is contingent on C2 verification PASS — currently FAIL, so round-3 paused until path decision resolves

## References

- Build-execute directive: `MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`)
- Orchestration state SSoT: `ORCHESTRATION_STATE_2026-04-27.md` (master `46818f5`) — explicit Path B workaround authorization
- Builder next-action nudge: `BUILDER_NEXT_ACTION_2026-04-27.md` (master `46818f5`)
- Round 2 synthesis: `MAIN_TERMINAL_PR60_PHASE2_SYNTHESIS_2026-04-27.md` (master `8621f9a`)
- PR #60 merge: `d9b4b8d`
- Original v1 of this report: master `5685605` (E2-A BLOCKED before workaround authorization read)
- Phase 2 builder report: `PROGRAMMER_REPORT_BLUEPRINT_V3_PHASE2_2026-04-27.md`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_shared_tree_commit_hygiene.md`

**Status: BUILD-EXECUTE v2 — E1+E2-B+E2-A+E3 PASS; C2 verification gate FAILS (313 records vs 500 target; structural pool undersize for Phase A categories: MAGG 0/40, PFA 46/80, etc.). Awaiting orchestrator path decision (X=expand Mode B yields, Y=reduce targets, Z=mixed). DRAFT data PR will open with all outputs + workaround driver script + this report; flagged for round-3 review pause.**
