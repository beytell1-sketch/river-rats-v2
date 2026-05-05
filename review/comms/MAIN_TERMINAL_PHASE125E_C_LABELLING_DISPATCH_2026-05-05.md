---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-C — labelling round (5 sonnet labellers × 110 hands; v3.3 prompt; $120 cap)
status: DIRECTIVE — owner picked Data-fix; 12.5E-B Path B amendment merged at master 0eaac06; 12.5E-C dispatched
---

# Phase 12.5E-C — labelling round

12.5E-B Path B amendment merged. Master HEAD `0eaac06` includes the 110 new situations + v3.3 labeller prompt + builder gto-expert-hat self-review (PASS on falsification test + per-hand re-verification) + standalone QC APPROVE (5 audits all PASS).

Two convergent stamps cleared the merge: standalone QC mechanical/structural audit (APPROVE) + builder gto-expert-hat self-review (PASS). Per `feedback_river_rats_team_structure.md` (3 parties only), no separate "standalone gto-expert team" exists — builder's gto-expert-hat self-review IS the gto-expert pass.

## LEAD-PROGRAMMER — what you do

**Branch:** `programmer/phase125e-c-labelling-2026-05-XX` (XX = your start date)

**Authority chain:**
1. This dispatch directive (operational scope, sequencing, stop conditions)
2. 12.5E-A design §8.C labelling phase spec (master `bad1396`, `PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md`)
3. 12.5E-B amended (master `0eaac06`) — situations + v3.3 prompt + manual canonicals all merged
4. Existing labeller pipeline (`scripts/dispatch_mass_labelling.py`, `scripts/collect_mass_labels.py`) — reused unchanged
5. CLAUDE.md §6 + addendum

### LEAD-PROGRAMMER (default — implementation)

**Deliverable — exactly 3 new files in PR diff:**

1. `data/corpus_revision_125e_labels_raw_2026-05-XX.jsonl` — raw 5-labeller responses (550 rows = 110 hands × 5 sonnet labellers; one row per labeller-hand pair)
2. `data/corpus_revision_125e_labels_2026-05-XX.jsonl` — consensus labels (110 rows; one row per hand with `consensus_action`, `consensus_confidence`, per-class vote counts, `pilot_hand_id` matching the situations file)
3. `review/comms/BUILDER_REPORT_PHASE125E_C_LABELLING_2026-05-XX.md` — report with G1-G4 self-checks (G4 fires here for the first time)

**Configuration:**
- **Labeller protocol:** `prompts/gto_labeller_v3.3.md` (NEW; merged at master `0eaac06`). NOT v3.2.
- **Labellers:** 5 × Anthropic Claude Sonnet 4.6 (per design §6.2 quality default)
- **Hands:** all 110 from `data/corpus_revision_125e_situations_2026-05-04.jsonl` (96 parametric) + `data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl` (14 manuals) — combined dataset PILOT_495..PILOT_604
- **Hard cost cap:** $120 (per design §6.2). If cap reached before all 550 calls complete → STOP, report partial; do not exceed
- **Consensus protocol:** majority class wins; confidence = (votes for winning class) / 5; ties on majority resolved per existing `collect_mass_labels.py` logic

**Pre-flight checks (mandatory before launching the labelling run):**
1. Verify `prompts/gto_labeller_v3.3.md` exists at master HEAD; verify Fix 2.1 carve-out present at the bottom of the file
2. Verify `scripts/dispatch_mass_labelling.py` accepts a `--prompt` flag pointing at v3.3 (or matching mechanism); if v3.2 is hard-coded anywhere, fix the dispatch script's prompt-resolution path BEFORE launching (this is a 1-line config change, not a methodology change — but still in this PR's diff)
3. Run a **3-hand smoke test** (1 each from T1, T5, T7) with v3.3 prompt + 1 labeller before the full 550-call run. Verify the smoke output's `consensus_action` field is sensible. STOP if any smoke output is malformed.
4. Pre-flight join cardinality on the combined situations+manuals JSONL: verify 110/110 unique `pilot_hand_id`, zero collision with existing 494

### LEAD-PROGRAMMER (gto-expert hat — labeller-output spot-check)

After the full run completes and `collect_mass_labels.py` produces the consensus JSONL, swap to gto-expert hat and spot-check **the H-FEAT primary canonicals**:

- **PILOT_599** (MW-47 family, AsQs on KsJs6c): expected `consensus_action = RAISE` per v3.3 carve-out. If consensus is CALL or FOLD → v3.3 carve-out did NOT trigger as predicted; STOP and report (this is the load-bearing test for the entire 12.5E migration)
- **PILOT_600** (MW-47 family, AhKh on JhTh5c): expected `consensus_action = RAISE`. Same STOP condition.
- **5 random T5 parametric hands** from PILOT_495..PILOT_604: expected `consensus_action = RAISE` for the majority. Document the per-hand consensus + confidence in the builder report.

If T5 H-FEAT primary canonicals consensus to CALL despite v3.3 carve-out: this is empirical refutation of Path B at the labelling layer. STOP and report; orchestrator routes back to architect hat for v3.3 wording revision OR escalation to Path C.

If T5 hands consensus to RAISE: Path B's discriminator works empirically; 12.5E-D dispatches automatically.

### LEAD-PROGRAMMER (architect hat — only if needed)

ONLY engage architect hat IF the gto-expert spot-check above flags T5 mismatch. If engaged: author a `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_*.md` comm documenting which hands failed, what the v3.3 wording predicted vs what labellers chose, and whether the issue is in v3.3 wording or in the situation construction. Do not improvise revisions; route to orchestrator.

### Stop conditions (any hat)

- $120 cost cap reached before all 550 calls complete → STOP, report partial
- Any of 110 hands receives <5 labels → STOP, fix dispatch script + retry the missing hands
- Consensus calculation produces NaN/null on any hand → STOP, fix
- Labeller protocol mismatch detected mid-run (some calls used v3.2 by mistake) → STOP, discard polluted run, restart with v3.3
- v3.3 carve-out file not at master HEAD when pre-flight runs → STOP (something drifted)
- T5 H-FEAT primary canonicals (PILOT_599/600) consensus ≠ RAISE → STOP, report (this is the 12.5E migration's load-bearing test failing at the labelling layer)
- Any class <5% of 110 labels (e.g., RAISE class <6 hands) → FLAG in report (per design §7 G2; informational, not STOP — we expected this distribution from the corpus design)
- >3 files in diff → STOP, revert extras

### What you do NOT do

- Do NOT run any solver call (per `feedback_solver_vs_expert_labels.md`; solver is verify-after only at 12.5E-F)
- Do NOT touch existing 494-row corpus or its labels
- Do NOT modify v3.3 prompt during the run (if wording needs revision, that's an architect-hat workstream after STOP)
- Do NOT change the 5-labeller-per-hand count (design §6.2 quality default; lowering = quality regression)
- Do NOT exceed $120 cost cap

## QC stream — what you audit

**Standalone QC pre-merge audit fires on the 12.5E-C PR.** Per `feedback_qc_routing_when_standalone_active.md`: SOLO-routed; orchestrator does NOT spawn parallel general-purpose subagent (process improvement confirmed at 3 successive cycles).

**5 audits on 12.5E-C PR:**

1. **Diff scope** — exactly 3 new files; no edits to existing source surfaces or existing data files; no edits to v3.3 prompt
2. **Citation existence** — every file:line citation in builder report exists at master HEAD at audit time
3. **Label distribution sanity** (G2, design §7) — 110 hands, all 5 classes (FOLD/CHECK/CALL/BET/RAISE) represented; per-class count documented; no class with 0 labels (would indicate labeller misconfiguration)
4. **NEW: Cost reconciliation** — verify total labelling cost ≤ $120; verify per-call cost matches Sonnet 4.6 pricing; verify 550 calls completed (or partial-run documented per stop condition)
5. **NEW: T5 H-FEAT primary correctness** — verify PILOT_599 + PILOT_600 consensus = RAISE; if either is CALL/FOLD, HOLD on the PR and surface to orchestrator (this is the load-bearing test for Path B's empirical validation)

**HOLD or APPROVE.** Post `REVIEW_QC_PHASE125E_C_LABELLING_*.md`.

## Sequencing

1. LEAD-PROGRAMMER pre-flight (verify v3.3 prompt + dispatch script + smoke test)
2. LEAD-PROGRAMMER full labelling run (5 × 110 = 550 sonnet calls; ≤ $120)
3. LEAD-PROGRAMMER (gto-expert hat) spot-check T5 H-FEAT primary canonicals
4. If T5 spot-check PASS: LEAD-PROGRAMMER opens 12.5E-C PR
5. Standalone QC pre-merge audit (5 audits)
6. On QC APPROVE: orchestrator merges PR
7. **12.5E-D dispatched** automatically (corpus QC phase per design §8.D + cleanup of NIT-1 PLAN §3.T8 wording from PR #139)

## What's blocked / what's queued

**Blocked:**
- 12.5E-C PR opens → blocked on labelling run completion + builder gto-expert-hat T5 spot-check PASS
- 12.5E-C PR merge → blocked on standalone QC APPROVE
- 12.5E-D dispatch → blocked on 12.5E-C merge
- All downstream (E/F/G) → blocked on prior phase

**Queued (no separate owner ask):**
- **NIT-1 from PR #139 QC review** (PLAN §3.T8 cites 36 hands; dispatch superseded to 22+14): cleanup at 12.5E-D in a single comm amend
- **MEDIUM-2 from PR #134** (V-X4 prose recurrence at trainer line 1371): cleanup at 12.5E-E re-train phase
- **3 NITs from PR #134** (framing, stale dispatch reference, "Schema discoveries during 12.5D" prose): ride along at 12.5E-E
- **PILOT_595 design_note cosmetic** (TPTK→top-two-pair wording): non-blocking; document at 12.5E-D
- **12.5G** (cap retuning sweep): fires automatically post-12.5E-F
- **Protocol amendment #2** (verify labeller protocol's discriminator on sample situations before declaring blueprint design complete): lives in 12.5E-B amendment dispatch until ml-architect-hat formalizes in `docs/PROCESS_GUIDE.md`

## References

- 12.5E-B amendment merged: master `0eaac06` (PR #136)
- 12.5E-B amendment dispatch (Path B): master `10f914b` (PR #137)
- v3.3 prompt: `prompts/gto_labeller_v3.3.md` (master `0eaac06`)
- Standalone QC verdict on PR #136 amended: master `083f8b1` (PR #139)
- 12.5E design (12.5E-A): master `bad1396` (PR #133)
- 12.5D' synthesis addendum (12.5G queued): master `6b991b2` (PR #135)
- Memory: `feedback_river_rats_team_structure.md` (NEW 2026-05-05; 3-party model), `feedback_orchestrator_output_structure_per_party.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5E-C DISPATCHED. LEAD-PROGRAMMER named author (default + gto-expert hats). 3-file deliverable. v3.3 prompt + 5 labellers × 110 hands ≤ $120. T5 H-FEAT primary canonicals are the load-bearing test — if PILOT_599/600 consensus ≠ RAISE, STOP and report (Path B refuted at labelling layer).**
