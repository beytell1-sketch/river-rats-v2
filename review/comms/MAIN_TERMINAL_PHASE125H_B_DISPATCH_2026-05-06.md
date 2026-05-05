---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-B — situation generation (90 hands across 6 templates per 12.5H-A design)
status: TRIGGER — fire now
---

# Phase 12.5H-B — situation generation

12.5H-A design merged at master `858b032`. Builder generates 90 new situations across 6 templates per design §3.

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125h-b-situation-generation-2026-05-XX` (XX = your start date)

### LEAD-PROGRAMMER (default — implementation)

#### Templates per 12.5H-A §3 (with per-template counts to be confirmed against design §4 by builder)

- T8' — BET-stays-wrong: monotone-flop FD-with-overcard checked-through 4-way (MW-25 family expansion)
- T9' — BET-stays-wrong: TP-medium-kicker IP 4-way after PFR check (MW-40 family expansion)
- T10' — RAISE-stays-wrong: slowplayed set into turn lead 4-way (MW-45 family expansion)
- T7-ext — CALL-stays-wrong: NFD+overcards under direct pot odds with implied/blocker reasoning (MW-17 family expansion)
- T-RAISE-stabilize — additional bet+call multiway with `villain_air_pct ≥ 0.05` (seed-volatility fix targeting 60/40 bimodal H-FEAT activation)
- T-CONTROL — drift detection across 5 buckets

Per-template counts: read design §4 for exact distribution. Total = 90 hands.

#### Methodology rules (per 12.5H-A §10 — all standing for this phase)

1. **Hero-only convention** in `prior_actions` (matches existing 604 corpus uniformly)
2. **Pre-flight join-cardinality** ≥0.99 vs existing 604 (per 12.5D' protocol amendment)
3. **`design_action` field per hand** for T-CONTROL (per QC's TC-X T8 schema gap finding from PR #150) — encode expected GTO action explicitly so G4 drift detection can do exact same-action match in 12.5H-D
4. **Pilot-first does NOT apply at 12.5H-B** — situation generation is deterministic factory output, not a multi-call API batch with unverified assumptions; same as 12.5E-B
5. **Solver-as-labels prohibited** per `feedback_solver_vs_expert_labels.md` — situations only at this phase; no labels until 12.5H-C

#### Deliverable scope — exactly 4 files in PR diff

1. `scripts/build_corpus_revision_125h_situations.py` — NEW: factory + 6 templates + 14 (or per-design) manual canonicals + G1-G3 self-checks. Reuse `scripts/build_corpus_revision_125e_situations.py` (master `858b032`) as structural template.
2. `data/corpus_revision_125h_situations_2026-05-XX.jsonl` — NEW: parametric situations (factory output)
3. `data/corpus_revision_125h_manual_canonicals_2026-05-XX.jsonl` — NEW: manual canonical hands (subject to GTO-EXPERT review at 12.5H-C trigger)
4. `review/comms/BUILDER_REPORT_PHASE125H_B_SITUATION_GENERATION_2026-05-XX.md` — NEW: report with G1-G3 results + per-template count table + hero-only convention verification

`pilot_hand_id` range: PILOT_605..PILOT_694 (or per-design exact range). No collisions with existing 604.

#### G1-G3 self-checks (must PASS before opening PR)

- **G1 (join-cardinality):** 90/90 unique `pilot_hand_id`, zero collisions with existing 604
- **G2 (distribution):** per-template counts within ±1 of design §4 spec
- **G3 (duplicate detection):** zero exact-match duplicates vs existing 604 on (board, hero_cards, action_history, hero_position)

#### Stop conditions

- Pre-flight finds drift in cited file:lines vs design → STOP, route to architect hat
- Any template count off ±1 from design → STOP, fix
- G1/G2/G3 fails → STOP, fix
- Convention not uniform (any hand has non-hero action in `prior_actions`) → STOP, fix
- Solver call appears anywhere → STOP per `feedback_solver_vs_expert_labels.md`
- >4 files in diff → STOP, revert extras

#### What you do NOT do

- Do NOT label situations (12.5H-C is the labelling phase)
- Do NOT touch existing 604-row corpus or its labels
- Do NOT modify v3.4 prompt or any v3.x prompt
- Do NOT touch trainer module
- Do NOT mutate `BATCH2_8_HAND_DESIGNS.md` reference set

### LEAD-PROGRAMMER (architect hat — manual canonicals)

The N manual canonical hands per design §5.1 Track B go into `data/corpus_revision_125h_manual_canonicals_*.jsonl`. These are GTO-correctness-load-bearing for the H-FEAT primary stabilization (T-RAISE-stabilize family) and the MW-25/40/45 family expansions. GTO-EXPERT review fires at 12.5H-C dispatch (BEFORE labelling round).

For each manual hand:
- composition triple matches template family
- board texture canonical for the failure pattern
- action history plausible (no "would never happen at the table")
- position + SPR consistent with the GTO reasoning the hand captures
- includes `author_design_note` describing intent

### LEAD-PROGRAMMER (gto-expert hat — pre-PR self-review)

After factory run + manual hands, swap to gto-expert hat and self-review the 14 (or per-design) manual canonicals. Document in §"gto-expert-hat self-review" section of builder report. Same pattern as 12.5E-B amendment.

## QC stream — what you audit (when 12.5H-B PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when builder force-pushes.

When triggered (5 audits — same as 12.5E-B amendment + design_action verification):

1. **Diff scope** — exactly 4 files
2. **Citation existence** — every file:line in builder report exists at master HEAD
3. **Distribution sanity** — 90 hands, per-template counts within ±1 of design §4
4. **Convention uniformity** — all 90 `prior_actions` use hero-only; zero non-hero actions
5. **NEW: design_action present per T-CONTROL hand** — verify each T-CONTROL row has explicit `design_action` field (per TC-X T8 schema gap fix); G4 same-action match relies on this

Post `REVIEW_QC_PHASE125H_B_SITUATION_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER (architect hat) reads design §3 + §4 + §5; pre-flight at master HEAD
2. LEAD-PROGRAMMER (default) implements factory + manual canonicals
3. G1-G3 self-checks pass
4. LEAD-PROGRAMMER (gto-expert hat) self-review of manual canonicals
5. PR opens
6. Orchestrator posts QC audit-now trigger
7. Standalone QC audit
8. On QC APPROVE: orchestrator merges; **dispatches 12.5H-C labelling round** (with pilot+full + Opus tier-up cross-check + GTO-EXPERT review of manual canonicals)

## What's blocked / what's queued

**Blocked:**
- 12.5H-B PR opens → on builder factory + report + self-review
- 12.5H-B QC trigger → on PR open
- 12.5H-B merge → on QC APPROVE
- 12.5H-C/D/E/F → all downstream of 12.5H-B merge

**Queued:** all items per PR #164 §"What's blocked / queued"

## References

- 12.5H-A design (master): master `858b032` (PR #165)
- 12.5H-A QC verdict: master `68b6924` (PR #167)
- 12.5H-A dispatch: master `5f9c507` (PR #164)
- 12.5E-B (structural template): master `0eaac06` (PR #136)
- Memory: `feedback_explicit_action_trigger.md` (this comm IS the trigger), `feedback_quality_default_no_ask.md`, `feedback_river_rats_team_structure.md`, `feedback_solver_vs_expert_labels.md`

**Status: 12.5H-B TRIGGER posted. LEAD-PROGRAMMER fires factory + manuals + report. QC trigger fires after PR opens.**
