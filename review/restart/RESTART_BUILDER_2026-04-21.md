# Restart Prompt — Logic Builder (2026-04-21)

Copy into a fresh Claude Code session.

---

```
I'm restarting the River Rats logic builder terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2

Working directory: ~/river-rats-v2
Repo HEAD at handoff: f38d47a
Role: v2 core builder — oracle, features, training, model artifacts

Read these files in order before doing anything else:
1. ~/river-rats-v2/CLAUDE.md
2. ~/river-rats-v2/RELEASE_MANIFEST.yaml (integrated approved state; v1.6)
3. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md (shared snapshot)
4. ~/river-rats-v2/review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md (5 MUSTs)
5. ~/river-rats-v2/review/comms/BUILDER_V24_STAGE35_HANDOFF_2026-04-21.md (previous builder's handoff)
6. ~/.claude/projects/-home-rupert-river-rats-v2/memory/MEMORY.md (memory index — read each referenced file)

Your current work — v2.4 Stage 3.5 (range-narrowing action-history fix)

Status: NOT SHIPPED despite prior "complete" report. Multi-agent
review (orchestrator's reconciliation at commit 0276653) surfaced
five MUSTs the prior builder did not address before stopping:

1. CRITICAL #1 — Blocker features bypass the chain.
   flush_block_pct + the 4 new v2.4 P1 blocker features
   (nut_flush_block, flush_draw_block_pct, straight_draw_block_pct,
   nut_made_block_pct) recompute _s12_v_range via
   get_villain_range() directly. They never call
   narrow_by_action_history. Plan's "all 10 features inherit"
   claim is false; only 6 do.
   Location: river-rats-core/feature_extractor.py:1648-1662, 1720+
   Fix: Step 12 + Step 17 must consume the already-narrowed range
   from classify_villain_range, not recompute.

2. CRITICAL #2 — Silent fallback when _action_history is absent.
   Code falls back to pre-Stage-3.5 behavior with no warning /
   error. Gauntlet/synthetic/backfill rows may lack the field.
   Same failure mode as v2.3.2.
   Fix: emit loud warning (or raise) on missing _action_history
   during Stage 4 feature extraction; audit all training-data
   pipelines (extract_features_parallel.py, extract_incremental.py,
   any gauntlet scripts); add _action_history_present boolean to
   training CSV for post-hoc audit.

3. HIGH #3 — Check-raise sign flip. Chain applies flop-CHECK ×
   flop-BET sequentially on same board for check-raise lines.
   Produces inverted composition (mediums up, nuts down).
   Recommend: treat check-raise as raise-only (skip the CHECK
   when followed by RAISE on same street). Confirm with GTO
   reviewer.

4. HIGH #4 — FOLD re-fetch silent bug at feature_extractor.py:1186.
   When chain returns empty range from FOLD, caller silently
   re-fetches get_villain_range() un-narrowed. Features compute
   against preflop range for folded villain.
   Fix: sentinel (meta['villain_folded'] = True) + feature
   extractor skips villain-composition features for folded
   villains (or marks as NaN/null).

5. HIGH #5 — surviving_weight uses hand count not probability
   mass. Safety rail gives false OK on degenerate distributions.
   Fix: compute true un-normalized weight sum inside each narrow
   step; thread through chain.

Plus: load the 81-case test corpus at
review/tests/range_narrowing_test_corpus_2026-04-20.yaml into a
unit test file. Replaces the 16-test file the prior builder wrote.

Patch order (ship-gated):
  CRITICAL #1 → CRITICAL #2 → HIGH #3 → HIGH #4 → HIGH #5 →
  unit test file from 81-case corpus → re-run M4 and M5 audits
  (which previously ran only on composition features; now must
  include the 5 blocker features that took the bypass path) →
  anchor regression check on v2.3.1 → report.

What's already landed (real and tested, don't redo):
- narrow_by_action_history + M1 tables + 16 unit tests pass
- M4 audit: 0/124 flop isolation violations, 455/455 chain
  firing on composition features
- M5: 3/3 β-panel anchors BET restored on v2.3.1 without
  retraining

After Stage 3.5 ships:
  Stage 4: re-label training data with v3.2 prompt (Stage 2
    produces KB §1.9; Stage 3 derives v3.2 prompt)
  Stage 5: retrain v2.4 with expanded 59-feature vector
  Stage 6: ship gate — calibration-anchor pre-flight +
    standard gates + air litmus + value litmus + self-play
    systemic

Hard rules (apply without exception):
- No sample_weight hacks, class_weight compensation, or pruning
- No below-floor ships with owner sign-off
- No skipping pre-flight gate before self-play
- Multi-agent review default for load-bearing changes — don't
  ask, escalate
- Panel reasoning per-hand; never static overrides
- Slow/quality, no rush

Orchestrator (main terminal) owns the cross-stream manifest,
reviews your work, and approves stage gates. Ping orchestrator
when:
- You finish patching each MUST (brief progress ping)
- Stage 3.5 ship gate passes (full report)
- Any new STOP condition surfaces

Standing by for owner direction or orchestrator signal.
```
