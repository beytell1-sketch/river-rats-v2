---
date: 2026-04-21
from: Main terminal (outgoing orchestrator)
to: All four restarting terminals
re: Shared state snapshot — read before doing anything else
---

# Session State — 2026-04-21

All four terminals (orchestrator + logic builder + teaching + game
builder) read this file on startup for integrated state.

## Source of truth

**`~/river-rats-v2/RELEASE_MANIFEST.yaml` v1.6** is the integrated
approved-state tracker. It captures:

- `deployed` — what owner plays against now
- `iteration` — staged artifacts (v2.3.1 baseline, shelved v2.3.2)
- `in_progress` — active work per stream
- `archived` — what was reverted and why
- `queued` — v2.5+ backlog
- `pipeline` — end-to-end data flow across streams
- `interfaces` — per-boundary contract specs
- `import_dependencies` — runtime import graph
- `integration_protocol` — cross-repo coordination rules
- `pro_level_narrowing_gaps` — dimensional coverage map (owner-audited)

Read the manifest BEFORE doing anything else.

## Three repos, four terminals

| Terminal | Repo | Current HEAD |
|---|---|---|
| Orchestrator (main) | ~/river-rats-v2 | (see restart pack) |
| Logic builder | ~/river-rats-v2 | f38d47a |
| Teaching | ~/river-rats-teaching | 42d7f76 |
| Game builder | ~/river-rats-game (local only) | 4fe1d41 |

## Current state by stream

### Deployed (what owner is playing against)

- **Oracle:** v2.2 (`v2_2_model_shipped.json`)
- **Teaching:** `l3_enriched_v3.0` (plan v2.1 shipped at 42d7f76 — flag window + range-first)
- **Game prototype:** `f5c1a5a` with V1 range bar + Badge A inline + hand-vs-range split (shipped at 143993a)

### In progress

- **Logic v2.4 Stage 3.5** — range-narrowing action-history fix. **5 MUSTs outstanding** per multi-agent reconciliation (`MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md`, commit 0276653). Builder's handoff at `BUILDER_V24_STAGE35_HANDOFF_2026-04-21.md`.
- **Teaching** — plan v2.1 shipped. Standing by for playtest findings + cross-stream pings.
- **Game** — first cut shipped. Second cut (pot-odds chip on felt) not started; owner-paced.

### Archived

- v2.3 (reverted — air-BET overgeneralization)
- v2.3.2 (shelved — target-subspace mis-scope + concentration effect)

## Load-bearing hard rules (from memory)

All terminals apply:

1. **No static overrides anywhere in the pipeline** — fix with features + diverse training examples
2. **Pruning/reweighting can't teach a boundary** — need real counter-examples in target feature subspace
3. **Single-class counter-example injection shifts surface systemically** — pair both classes in same shape
4. **Panel-correct labels in narrow texture subspace can amplify bias** — distribution inspection beats count threshold
5. **Teaching highlights context, never explains why** — range-based thinking central
6. **Multi-agent review (4-6 agents) is default for load-bearing changes** — don't ask, escalate
7. **Slow/quality, no rush** — catching a problem now over shipping and fixing later

## Pending v2.4 ship sequence

1. Stage 3.5 MUSTs (builder) — CRITICAL #1 (bypass fix) → CRITICAL #2 (silent fallback) → HIGH #3-5 → 81-case test corpus → re-audit
2. Stage 4 — re-label training data with v3.2 prompt (Stage 2 produces KB §1.9; Stage 3 derives v3.2)
3. Stage 5 — retrain v2.4
4. Stage 6 — ship gate (calibration anchor pre-flight + standard + air litmus + value litmus + self-play systemic)

Stage 3.5 is the current bottleneck. Nothing downstream opens until MUSTs patched.

## v2.5 queued (after v2.4 ship)

- Bet-size-conditional range narrowing (biggest industry gap per research agent)
- Raise-aware call narrowing
- hand_evaluator draw_outs redefinition
- HU counter-examples + v3.2 HU-calibrated prompt
- Retire flush_block_pct after nut_made_block_pct validates
- Blocker flag 2-flag teaching design (gated on v2.4 features + teaching flag window live — now both true)

## Cross-stream contracts (unchanged)

- Feature vector: 55 current, target 59 on v2.4 ship
- Oracle output: `action + probs + sizing + top_two_gap`
- SHAP output: `shap_values + shap_values_by_action + feature_attention`
- Teaching schema: `l3_enriched_v3.0` (Path B + recentering); primary fields `range_position_desc + villain_*_pct + board_favour + villain_actions_desc`
- Playtest log schema: v2 with full reproducibility payload

## Roles

- **Orchestrator:** decides, writes directives, owns manifest, coordinates cross-stream. DECIDE and EXECUTE; bar for asking owner is ABSOLUTELY NECESSARY.
- **Logic builder:** oracle, features, training, model. v2.4 Stage 3.5 current focus.
- **Teaching:** L3 rendering, flag window, CONTENT_API. Plan v2.1 shipped; standing by.
- **Game builder:** prototype, adapters, playtest logs, UI. First cut shipped; standing by for direction.

## Owner preferences (hard)

- Slow/quality, no rush. Verification steps ARE the work.
- Recommend, don't defer. Owner does not read long reports; key judgments in chat.
- Quality-focused slow-moving approach is the default recommendation.
- Range-based thinking is CORE across all three streams.

Each terminal now reads its own RESTART_*_2026-04-21.md for role-specific next steps.
