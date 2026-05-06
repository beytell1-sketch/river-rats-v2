---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: BATCH2 MW-25 graduation update — reference label BET HIGH → CHECK HIGH per 4-source convergence; stay-wrong list 5→4; reference_corrections.md MW-25 entry added
status: complete; PR opens for QC audit
branch: programmer/batch2-mw25-graduation-update-2026-05-06
base: master `c2021e7` (post-PR #213 + #215 merge)
---

# BATCH2 MW-25 graduation update — builder report

Per `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217) §"LEAD-PROGRAMMER — Step 1": author the BATCH2 MW-25 graduation update PR. Owner WHAT decision 2 = α (lock CHECK HIGH).

## §"Files edited" — diff scope

**4 files edited + 1 builder report (5 total in PR diff):**

| File | What changed |
|---|---|
| `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md` | (1) GTO Action Table row line 27: MW-25 BET HIGH → CHECK HIGH; (2) detail section line 383: GTO Action: BET → CHECK with corrected reasoning + original-reasoning-with-refutation footnote + expert_action_history annotation; (3) Axis 4 insight at line 1028: action list updated, axis insight rewritten to reflect that for non-nut DRAWS the IP/OOP position split does not flip the action |
| `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | MW-25 entry: added `Expert action history:` annotation documenting the 2026-05-06 graduation. The expected `expert_action: BET HIGH` field per dispatch §"Step 1 Files to edit" does not exist in this file; the canonical label lives in `BATCH2_8_RANGE_ANALYSIS.md` per `reference_evaluator._parse_gto_table` (river-rats-core/reference_evaluator.py:250-265). Added a redirect note pointing to the canonical location. |
| `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` | Added new section "## Empirically Corrected Reference Labels (6 May 2026)" with MW-25 entry (table format consistent with existing solver-corrected section + detail block with composition triple reasoning + stay-wrong status note) |
| `review/RESTART_PROMPT_V9_3WAY.md` | Stay-wrong list section updated: MW-25 row removed; "5 True Remaining Failures" → "4 True Remaining Failures"; graduation note added below the table; MW-40 entry annotated with graduation-candidate status (per orchestrator's Decision 3β queued verification round) |
| `review/comms/BUILDER_REPORT_BATCH2_MW25_GRADUATION_2026-05-06.md` | NEW — this report |

## §"Verification" — owner-scope discipline check

Confirmed against `feedback_orchestrator_decides_not_recommends.md`:
- ✓ NO touch to `prompts/gto_labeller_v3.4.md` (per dispatch §"Optional file" + §"Stop conditions")
- ✓ NO touch to `data/corpus_*.jsonl` files (training data unchanged)
- ✓ NO touch to `river-rats-core/` source code (reference_evaluator.py reads from edited file; no logic change needed)
- ✓ NO touch to `prompts/` directory at all
- ✓ NO retraining (per dispatch §"Why no QC tier-up here": doc + memory update only)

The 4 edited files all live within scopes the dispatch authorized: `design/multiway_reference_set/` (BATCH2 reference set authority owner-scope), `memory/` (reference_corrections.md), `review/` (RESTART_PROMPT_V9_3WAY.md). Cost: $0 (text edits, no LLM calls).

## §"Stay-wrong list state" — 5 → 4

Pre-graduation (from `review/RESTART_PROMPT_V9_3WAY.md`):
- MW-17 — Under-calling (low equity draw)
- MW-25 — Residual passive (thin value bet) ← **GRADUATES**
- MW-40 — Residual passive (very thin value bet)
- MW-45 — Under-raising
- MW-47 — Shared blind spot (nut draw should raise)

Post-graduation:
- MW-17 — Under-calling (low equity draw)
- MW-40 — Residual passive (very thin value bet) — *now annotated as 12.5I-MW40-VERIFICATION graduation candidate per Decision 3β*
- MW-45 — Under-raising
- MW-47 — Shared blind spot (nut draw should raise)

**Stay-wrong: 5 → 4 hands. MW-40 candidate flagged for queued verification round.**

## File-mapping clarification (for QC audit)

The dispatch §"Step 1 Files to edit" referenced an `expert_action: BET HIGH` field in `BATCH2_8_HAND_DESIGNS.md` that does NOT exist. The actual canonical location of the expert action label for the reference evaluator is `BATCH2_8_RANGE_ANALYSIS.md`'s GTO Action Table (line 27 of that file). I confirmed this against `river-rats-core/reference_evaluator.py:230-265` — `parse_reference_hands` reads expert actions from `_parse_gto_table(analysis_path)` which regexes the `| MW-XX | axis | equity | pot_odds | ACTION | CONFIDENCE |` table rows out of `BATCH2_8_RANGE_ANALYSIS.md`.

I edited the canonical location. This means the file diff scope is slightly broader than the dispatch's "2-3 files" estimate (4 files instead). I have NOT routed back to orchestrator because (a) the orchestrator's intent is unambiguous (lock MW-25 = CHECK HIGH in the canonical reference), (b) the slow-quality default per `feedback_quality_default_no_ask.md` favors editing the actual canonical location over forcing a non-existent field structure, (c) the dispatch's stop condition "BATCH2_8_HAND_DESIGNS.md MW-25 entry not found at expected path" does not literally trigger because the entry IS at the expected path — it just doesn't have the field structure the dispatch expected. Recording for QC TC-X-OWNER-SCOPE-DISCIPLINE audit.

## What I did NOT do (per dispatch)

- No edits to `prompts/gto_labeller_v3.4.md` (out of scope; protocol is correct)
- No edits to `data/corpus_*.jsonl` files (training data unchanged)
- No edits to `river-rats-core/` source code (no logic change needed)
- No retraining (doc + memory update only)
- No LLM calls (no Sonnet/Opus dispatches; text edits only)

## Stop conditions (none triggered)

| Condition | Triggered? | Notes |
|---|---|---|
| Touching v3.x prompts or training data | NO | scope held |
| BATCH2_8_HAND_DESIGNS.md MW-25 entry not found | NO | entry at expected path; field structure differed (canonical label lives in BATCH2_8_RANGE_ANALYSIS.md per reference_evaluator code; clarified in §"File-mapping clarification" above) |
| reference_corrections.md edit conflicts with existing memory entries | NO | added new "## Empirically Corrected Reference Labels (6 May 2026)" section preserving original (7 Apr 2026) section verbatim |

## Cost / time

$0 LLM cost. ~25 min builder time (file mapping + 4 edits + builder report).

## What's blocked / what's queued

**Cleared by this PR (after merge):**
- PR opens for QC audit per Step 3 of dispatch sequencing
- 12.5I-D corpus QC dispatch becomes unblocked (Step 4)
- 12.5I-MW40-VERIFICATION-A design dispatch becomes unblocked (Step 5)
- 12.5J-D-pre test-guard deflake dispatch becomes unblocked (Step 6)

**Builder serial queue (per dispatch §"Sequencing"):**
- Step 4: 12.5I-D corpus QC dispatch (next builder action after this PR merges)
- Step 5: 12.5I-MW40-VERIFICATION-A design (parallel queue with Step 6)
- Step 6: 12.5J-D-pre test-guard deflake

## References

- Dispatch (fire trigger): `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217)
- Opus tier-up HALT comm (4 hands): `MAIN_TERMINAL_PR213_OPUS_TIERUP_HALT_2026-05-06.md` (master `8b078bf`, PR #216)
- PR #213 (12.5I-C labelling round, 30/30 unanimous CHECK Step 1 evidence): master `994ae67`
- PR #215 (QC PASS verdict): master `c2021e7`
- PR #209 (MW-25 graduation pathway precedent + Opus 4.7 re-eval): master `077c168`
- PR #208 (12.5I-C pilot HALT, 5/5 CHECK first signal): master `52e5164`
- Reference evaluator (canonical label location): `river-rats-core/reference_evaluator.py:230-265`
- Memory: `feedback_quality_default_no_ask.md` (4th restatement), `feedback_orchestrator_decides_not_recommends.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `reference_corrections.md` (now extended with MW-25)

**Status: BATCH2 MW-25 graduation update complete. PR opens for QC audit per dispatch sequencing Step 3. Builder ready for Step 4 (12.5I-D dispatch) on PR merge.**
