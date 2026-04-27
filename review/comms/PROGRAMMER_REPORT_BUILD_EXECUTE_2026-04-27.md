---
date: 2026-04-27
from: Lead-programmer (builder; this session — Pilot Orch terminal switched to author mode per user course-correction at 12:30 SAST)
to: Main terminal (orchestrator) · Owner · QC stream
re: Build-execute pipeline E1 → E2-B → E2-A → E3 → C2 — partial completion: E1+E2-B+E3 PASS; E2-A BLOCKED on missing `--positions` flag (directive predicted this); C2 blocked on E2-A; data PR opens with what completed
status: PARTIAL — E1 ✓, E2-B ✓, E3 ✓; E2-A BLOCKED per directive's first option ("report BLOCKED before running"); C2 blocked; ready for orchestrator decision (add `--positions` flag in separate code PR, OR authorize workaround driver script in scripts/, OR proceed to round-3 review on partial output)
---

# Programmer Report — Build-execute partial completion

## Authorization

Per `MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`); per memory `feedback_listen_to_orchestrator_always.md` orchestrator-named-author directive sufficient + `feedback_named_author_builds_not_polls.md` named author = author mode not poll. User course-correction at 12:30 SAST switched this Pilot Orch terminal from stale Phase B polling to corpus-revision authoring.

## Step results

### Step 1 — E1: re-extract 100-hand pilot corpus ✓ PASS

```
python3 scripts/reextract_pilot_100_features.py \
  --input data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --output data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --bb-chip-size 10
```

Output: `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` (173,267 bytes; SHA256 `1afe69e7fbfa7bebfa319595a121115da68c3dbac369bb8b12edbe5e5184e9af`)

Verification gate:
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Record count | 100 | 100 | ✓ |
| SPR mean | [5.0, 15.0] BB-unit | 11.989 | ✓ |
| SPR min/max | n/a | 1.170 / 12.500 | (note: min 1.170 reflects compressed-SPR hands per existing corpus design) |
| `is_preflop_aggressor` count | ≥30 | 48 | ✓ |
| 3-bet edge cases | 3 SB-3bet → IS_PFA=0 | 3 SB hands with raise in prior_actions detected | ✓ |
| Labels untouched | hash match | hash match | ✓ |

Lock file written: `data/pilot_corpus_100_hand_2026-04-26.lock.json` (updated v2 attestation).

### Step 2 — E2-B: Mode B factory pool ✓ PASS

```
python3 river-rats-core/generate_corpus_revision_pool.py \
  --mode b \
  --output data/corpus_revision_pool_mode_b_2026-04-27.jsonl
```

Output: `data/corpus_revision_pool_mode_b_2026-04-27.jsonl` (200,834 bytes; SHA256 `be0c7ce9dc28b6f06d6c7c9301d410c833c5a9988653717f54fdcea58eb3b40f`)

Verification gate:
| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| Total records | 111 (per directive) / 115 (per per-module breakdown sum) | 115 | ✓ (matches per-module sum; directive's "111" appears arithmetic typo vs explicit module count) |
| Family breakdown | pfa 22 / facing 16 / bac 9 / magg 10 / nfd 7+4 / monster 10 / rule11 10 / donk 15 / sb 12 | pfa 22 / facing 16 / bac 9 / magg 10 / nfd 11 / monster 10 / rule11 10 / donk 15 / sb 12 | ✓ exact match |
| Within-family fingerprint dupes | 0 | 0 | ✓ |
| NFD R4 ±0.03 gate | 4/5 boundary templates pass | 4/5 pass (T5 filtered out, expected per directive) | ✓ |
| MAGG `villain_aggression_count` at river | == 2 | 10/10 records pass | ✓ |

### Step 3 — E2-A: Mode A self-play pool 🚫 BLOCKED

Per directive: *"If the script's `--positions` flag doesn't exist yet (it may not — builder Q3 was a flag, not yet a fix), report BLOCKED before running."*

**Confirmed:** `python3 river-rats-core/generate_corpus_revision_pool.py --help` shows the script accepts only `--mode {a,b,both}`, `--deals`, `--seed`, `--output`. No `--positions` flag exists.

**Root cause:** `_generate_mode_a()` line 90 hardcodes `single_position='UTG'` in the `SelfPlayRunner(...)` call. Per Phase 2 Q3, UTG self-play folds preflop yielding 0 records.

**Per directive's "Do NOT add the flag yourself" instruction:** I have NOT modified the script.

**Per directive's documented workaround option** (*"the workaround is to invoke the underlying `generate_pool` function directly (or write a small driver script in `scripts/`) — but document this in your report and surface for orchestrator review"*): I have NOT executed the workaround either, because:
1. The workaround would require a NEW driver script in `scripts/` that is itself a code change requiring its own review cycle (per directive's "DO NOT include any code changes" for the data PR).
2. The cleaner path per `feedback_quality_default_no_ask.md` is BLOCKED + orchestrator-side flag-add cycle.

**Two paths available to orchestrator:**
- **Path A (cleaner):** orchestrator dispatches a separate code-change PR to add the `--positions CO,BTN,BB` flag to `generate_corpus_revision_pool.py`. Standard per-batch protocol (review + QC + merge). Then re-run E2-A → E3 (already done) → C2.
- **Path B (faster):** orchestrator authorizes the documented workaround — write a small driver script in `scripts/run_mode_a_with_positions.py` that imports `_generate_mode_a` body and calls `SelfPlayRunner` 3 times with single_position=CO/BTN/BB. This is a NEW script, not a modification to existing code, but still a code change. If authorized, builder writes + tests + commits as separate code PR; then runs E2-A; then C2.

### Step 4 — E3: schema compatibility verification ✓ PASS (graceful skip per C6 path)

**Note: directive's CLI flag specification was incorrect.** Directive specified `--base-model` and `--corpus-sample`; actual script accepts `--model` and `--feature-keys` only. Used actual `--model` flag.

```
python3 scripts/verify_feature_schema_compatibility.py \
  --model river-rats-core/models/gto_model_v9_baseline_45feat.json
```

Output:
```
[R2] WARNING: could not extract feature names from river-rats-core/models/gto_model_v9_baseline_45feat.json
[R2] Feature schema compatibility check
[R2] Corpus contract: 59 features (FEATURE_COLUMNS=55 + v2.4 P1 blockers=4)
[R2] Base model: river-rats-core/models/gto_model_v9_baseline_45feat.json
[R2] Corpus feature contract: 59 features
[R2] Proceeding without base-model comparison.
Exit: 0
```

Verification gate: exit 0 ✓ — script gracefully skipped base-model comparison per directive's "C6 resolution path" allowance ("graceful skip with warning"). 59-feature contract confirmed.

**NIT for orchestrator:** Directive's CLI flag spec for E3 doesn't match actual script. Recommend updating directive OR script to match. Non-blocking.

### Step 5 — C2: 500-hand corpus assembly 🚫 BLOCKED

Cannot run — depends on Mode A pool output from E2-A which is BLOCKED.

`scripts/build_corpus_revision_500_hand.py` requires `--pool-mode-a` argument.

## Pipeline output state

| File | Size | SHA256 | Status |
|------|------|--------|--------|
| `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` | 173,267 | `1afe69e7fbfa7bebfa319595a121115da68c3dbac369bb8b12edbe5e5184e9af` | ✓ E1 |
| `data/pilot_corpus_100_hand_2026-04-26.lock.json` | (updated) | (per script) | ✓ E1 |
| `data/corpus_revision_pool_mode_b_2026-04-27.jsonl` | 200,834 | `be0c7ce9dc28b6f06d6c7c9301d410c833c5a9988653717f54fdcea58eb3b40f` | ✓ E2-B |
| `data/corpus_revision_pool_mode_a_2026-04-27.jsonl` | — | — | 🚫 E2-A BLOCKED |
| `data/corpus_revision_500_hand_2026-04-27.jsonl` | — | — | 🚫 C2 blocked on E2-A |
| `data/corpus_revision_500_hand_2026-04-27.lock` | — | — | 🚫 C2 blocked on E2-A |

## Wall-time + cost

- E1: ~5 sec
- E2-B: ~30 sec (Mode B factory generation)
- E3: ~3 sec
- Total wall-time: ~40 sec (E1+E2-B+E3 only)
- Cost: ~$0 (no model API calls; deterministic generation only)

## Action

**Orchestrator (me):**
1. Choose Path A vs Path B for E2-A unblock
2. Optionally update directive's CLI flag specs for E3 (NIT)
3. Decide if partial data PR opens NOW (E1 + E2-B + E3 outputs, with E2-A/C2 deferred) OR waits until E2-A unblocks for full data PR

**Pilot Orchestrator (this session):**
1. Surfaced this report (this commit)
2. Standby for orchestrator path decision
3. On Path A: standby for code-change PR cycle, then re-run E2-A + C2
4. On Path B: write driver script as separate code PR, then re-run E2-A + C2 after merge
5. On "partial data PR now": open PR with E1 + E2-B + E3 outputs as data-only PR; flag E2-A + C2 as deferred

**QC stream:**
- Layer 3 watch may pick up this report
- Round-3 review chain (per directive) is contingent on data PR existing — paused until partial-or-full data PR opens

## References

- Build-execute directive: `MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`)
- Round 2 synthesis: `MAIN_TERMINAL_PR60_PHASE2_SYNTHESIS_2026-04-27.md` (master `8621f9a`)
- PR #60 merge: `d9b4b8d`
- Phase 2 builder report: `PROGRAMMER_REPORT_BLUEPRINT_V3_PHASE2_2026-04-27.md`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_shared_tree_commit_hygiene.md`

**Status: BUILD-EXECUTE PARTIAL — E1+E2-B+E3 PASS; E2-A BLOCKED on missing `--positions` flag; C2 blocked on E2-A. Awaiting orchestrator path decision (A=code-change PR for flag, B=workaround driver script PR, OR partial data PR now).**
