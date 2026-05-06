---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-B' amendment — path (c) per builder pilot-halt; T7-ext SUITED-NFD redesign + MW-17 demotion to evaluation-only; updated 12.5H-C predictions
status: TRIGGER — fire now
---

# 12.5H-B' amendment — path (c) adopted

Builder PR #173 PILOT HALT report identified a critical protocol-vs-reference gap on T7-ext / MW-17. Builder recommended path (c) with sound reasoning. Orchestrator adopts per `feedback_quality_default_no_ask.md` slow-quality default + `feedback_orchestrator_decides_not_recommends.md` (within scope; HOW-level decision; owner can redirect on read).

**Why path (c) over (a) v3.4 amendment or (b) MW-17 reference re-validation:**
- (a) risks contradicting `feedback_bucket_first_labelling.md` (encoding equity-threshold-with-blocker-override into protocol)
- (b) erodes reference set authority (BATCH2 was solver-vetted; unilateral re-validation is wrong scope)
- (c) preserves bucket-first protocol unchanged + preserves reference set authority + generates SOUND training data on a SUITED-NFD-with-nut-blocker discriminative axis (which v3.4 already handles correctly per PILOT_658/694)

**Honest implication of (c):** model trained on SUITED-NFD-with-blocker may NOT generalize to MW-17's UNSUITED-overcards-with-blocker pattern at gate. If 12.5H-F fails on MW-17, that's genuine evidence of E-FEATURE primary (per gto-expert 12.5D' diagnosis) and we'd escalate to feature engineering — that's the genuine next step, not a workaround.

## LEAD-PROGRAMMER — what you do

Branch: continue on `programmer/phase125h-b-situation-generation-2026-05-06` (same branch as PR #169; force-push amendment) OR open a new amendment PR — your choice (force-push preferred for clean history).

### LEAD-PROGRAMMER (architect hat — T7-ext template redesign)

Edit `scripts/build_corpus_revision_125h_situations.py`:

1. **T7-ext parametric configs:** change hero hand to SUITED variants where:
   - Hero has flush draw (`has_flush_draw=1`) of the nut-blocker suit
   - Hero holds the Ace of the flush suit (canonical nut blocker)
   - Hero has at least one overcard (per design intent of MW-17 family)
   - Examples: AhKh on Jh8h3c (NFD + K overcard + nut spade blocker — wait; reuse the existing pattern verified by PILOT_658/694 in T-RAISE-stabilize)
   - Specifically: AhKh on Jh8h3c gives NFD + K overcard + nut hearts blocker; or AdKd on Jd8d3c (different suit; same structural axis)
2. **PILOT_693 manual canonical:** change from `AdKs` (literal MW-17) to a SUITED variant matching new T7-ext structure (e.g., `AdKd` on `Jd8d4c` with `has_flush_draw=1` — adds the 4th diamond to make true NFD)
3. **`design_action`** for the new T7-ext canonical: **CALL** (matches predicted v3.4 output for SUITED-NFD-with-blocker on this texture per PILOT_658/694 reasoning chain — actually verify by predicting through v3.4 protocol)

Verify post-edit: factory regen produces 12 T7-ext hands (10 parametric + 2 manuals — or per design distribution); all have `has_flush_draw=1` AND `nut_flush_block=1`.

### LEAD-PROGRAMMER (default — implementation)

Force-push amended scope:

1. `scripts/build_corpus_revision_125h_situations.py` — UPDATE (T7-ext template redesign + PILOT_693 manual canonical change)
2. `data/corpus_revision_125h_situations_2026-05-06.jsonl` — UPDATE (regenerate from amended factory; T7-ext rows changed)
3. `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` — UPDATE (PILOT_693 changed)
4. `review/comms/BUILDER_REPORT_PHASE125H_B_SITUATION_GENERATION_2026-05-06.md` — UPDATE (add §"Amendment 2026-05-06" documenting path-c rationale + T7-ext redesign + new PILOT_693 spec)

Re-run G1-G3 self-checks on amended dataset. Verify 90/90 unique pilot_hand_id, zero collision, zero internal duplicates, hero-only convention preserved.

Diff scope: 4 files (same count as original PR #169 amendment scope; just different files updated).

### LEAD-PROGRAMMER (gto-expert hat — re-review of amended T7-ext)

After amendment force-push, swap to gto-expert hat and verify:
- T7-ext parametric hands now have `has_flush_draw=1` AND `nut_flush_block=1` (the discriminative axis)
- Manual canonical PILOT_693 (new SUITED version) v3.4 prediction = CALL (verify by predicting through v3.4 protocol; if v3.4 still says FOLD on the SUITED variant, we have a deeper protocol issue)
- All 90 hands maintain hero-only convention

Document in §"Amendment gto-expert-hat self-review" of the builder report.

### Stop conditions

- T7-ext SUITED hands STILL produce FOLD-predicted under v3.4 protocol → STOP, route to orchestrator (deeper protocol gap; path (c) doesn't resolve)
- G1/G2/G3 fails on amended dataset → STOP, fix
- Manual canonical change introduces template-family mismatch → STOP, fix
- Diff scope > 4 files → STOP, revert extras

### What you do NOT do in 12.5H-B' amendment

- Do NOT touch v3.4 prompt (path c preserves protocol unchanged)
- Do NOT touch MW-17 reference set spec (path c keeps it as evaluation target)
- Do NOT change T8'/T9'/T10'/T-RAISE-stabilize/T-CONTROL templates (only T7-ext)
- Do NOT label any situations (12.5H-C re-pilot fires after amendment merge)

## Updated 12.5H-C predictions (after amendment merges)

For the re-pilot of 12.5H-C, my (orchestrator) updated predictions per builder's diagnoses:

| Template | Old prediction | NEW prediction | Reason |
|---|---|---|---|
| T8' parametric | (none / BET implied) | **CHECK** | monotone-FD-on-As-public board → CHECK matches GTO + existing 604 corpus |
| T8' manual canonical (PILOT_689) | BET | **CHECK** | same; orchestrator-side prediction error caught by pilot |
| T9' parametric / canonical | BET | **BET** (unchanged) | confirmed by PILOT_621/633/691 |
| T10' parametric | RAISE | **RAISE** (unchanged) | confirmed by PILOT_634/646 |
| T10' manual canonical (PILOT_692, MW-45) | RAISE | **CALL** | broadway-completed turn; texture-specific; both GTO-defensible; accept labeller |
| T7-ext parametric | (none / CALL implied) | **CALL** (after SUITED redesign) | SUITED-NFD-with-blocker; v3.4 should fire correctly |
| T7-ext manual canonical (new PILOT_693, post-amendment) | CALL | **CALL** | SUITED variant; predicted via v3.4 chain |
| T-RAISE-stabilize | RAISE | **RAISE** (unchanged) | confirmed by PILOT_658/694 |
| T-CONTROL | per design_action | **per design_action** (unchanged) | 6/6 validated in pilot |

## QC stream — what you audit (when 12.5H-B' amended PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when builder force-pushes.

When triggered (5 audits — same as 12.5H-B + amendment-specific):

1. **Diff scope** — exactly 4 files; only T7-ext factory + JSONL regen + manual canonical change + builder report update
2. **Citation existence** — every file:line in builder report exists at master HEAD
3. **T7-ext discriminative axis** — verify all 12 T7-ext hands (10 parametric + 2 manuals) have `has_flush_draw=1` AND `nut_flush_block=1`; programmatic check on the JSONL
4. **Convention uniformity** — all 90 `prior_actions` use hero-only (preserved from original PR #169)
5. **NEW: PILOT_693 v3.4 prediction sanity** — verify the new SUITED PILOT_693 v3.4 prediction is CALL (orchestrator-side prediction; QC verifies the prediction-chain logic by running the protocol on the new spec)

Post `REVIEW_QC_PHASE125H_B_PRIME_AMEND_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER (architect hat) edits T7-ext template + PILOT_693 spec
2. Factory regen + G1-G3 self-checks
3. gto-expert-hat re-review on amended T7-ext
4. Force-push to amendment branch (or new PR)
5. Orchestrator posts QC audit-now trigger
6. Standalone QC audit
7. On QC APPROVE: orchestrator merges amendment; **re-triggers 12.5H-C labelling round** with updated predictions
8. 12.5H-C pilot re-runs; if all 6 manual canonicals match new predictions → full Sonnet × 5 × 90; else iterate

## What's blocked / what's queued

**Blocked:**
- 12.5H-B' amendment PR opens → on builder edits + factory regen + report
- 12.5H-B' QC trigger → on PR open
- 12.5H-B' merge → on QC APPROVE
- 12.5H-C re-pilot → on amendment merge
- 12.5H-D/E/F → all downstream

**Queued (independent of 12.5H-B'):**
- MW-17 outcome at 12.5H-F: if fails, escalates to feature engineering (Path C of original 12.5E-F decision matrix; Direction-X-retro scope; ~3-4 weeks)
- All other prior NIT cleanup queues

## Methodology lesson

Pilot-first rule (`feedback_pilot_first_for_long_jobs.md`) JUST validated for the second time (after 12.5G cap-non-binding). Catching this at 1-Sonnet × 20-hand pilot ($0.50) saved ~$120 on a polluted full run + ~1 day on garbage training labels + the genuine risk of REINFORCING a model misclassification rather than correcting it.

The pattern proves: when the protocol has subtle gaps (v3.4's bucket-first reasoning chain doesn't handle implied-odds-with-blocker), labellers correctly identify it via per-hand reasoning. Pilot phase forces direct comparison of predictions vs labeller output, catching protocol-vs-reference gaps cheaply.

This is now THIRD demonstration of the pilot-first pattern saving real cost (12.5C T5 H-FEAT mismatch; 12.5G cap non-binding; 12.5H-C T7-ext protocol gap).

## References

- PILOT HALT report: `review/comms/BUILDER_STATUS_PHASE125H_C_PILOT_HALT_2026-05-06.md` (PR #173)
- 12.5H-C dispatch: master `fb6983b` (PR #172)
- 12.5H-B merged: master `094cfc2` (PR #169)
- 12.5H-A design: master `858b032` (PR #165)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `094cfc2`)
- 12.5D' gto-expert per-hand classification (MW-17 = E-FEATURE primary): `/tmp/gto_expert_125d_prime_findings.md`
- Memory: `feedback_pilot_first_for_long_jobs.md` (pilot-first + tier-up sub-rule), `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_river_rats_team_structure.md`

**Status: 12.5H-B' AMENDMENT TRIGGER posted. Path (c) adopted. LEAD-PROGRAMMER amends T7-ext template + PILOT_693 spec. After QC APPROVE: 12.5H-C re-pilot with updated predictions. PR #173 (PILOT HALT comm) merges as historical record alongside the amendment.**
