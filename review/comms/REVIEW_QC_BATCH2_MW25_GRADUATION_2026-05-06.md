---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #218 (BATCH2 MW-25 graduation update; BET HIGH → CHECK HIGH; stay-wrong 5→4) — PASS; 0 BLOCKER, 0 SHOULD_FIX, 1 NIT
severity: PASS (clean across all 4 dispatch audits; 1 NIT on citation form not content)
status: FLAG → APPROVE for merge
test-class: TC-X-OWNER-SCOPE-DISCIPLINE (first formal use; promoted from candidate via PR #213 finding)
multi-expert verdict: SOLO (20th successive cycle)
---

# QC Finding — PR #218 (BATCH2 MW-25 graduation update): PASS; 1 NIT

## Verdict

**APPROVE PR #218 for merge.** All 4 dispatch audits processed; 1 NIT on citation form (not content).

## 4-audit summary

| # | Audit | Result |
|---|---|---|
| 1 | Diff scope strict (TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ 3 v2 files + 1 builder report (4 in PR diff); memory file edited externally; **NO touch to v3.x prompts, data/corpus_*.jsonl, river-rats-core/ source, or any other owner-scope file** |
| 2 | Citation existence | ⚠ **NIT-1** — `BATCH2_8_RANGE_ANALYSIS.md` cites 3 sources by PR # (PR #209 + PR #213 + PR #215) + 1 by description ("5/5 pilot CHECK" — PR #208 alluded but not cited by #). Dispatch asked for "4 sources by PR # and confidence level". `reference_corrections.md` (memory) cites all 4 by PR # cleanly. Cross-cite chain intact; reader can resolve PR #208 from memory. |
| 3 | Canonical label correctness | ✅ Summary table line 27 `MW-25 ... BET \| HIGH` → `CHECK \| HIGH`; detail section line 383+ `GTO Action: BET → CHECK` HIGH; Axis 4 insight (line 1028) updated `BET, BET, BET, CHECK, BET, BET` → `BET, BET, CHECK, CHECK, BET, BET` with rewritten axis explanation; original reasoning preserved as footnote with empirical-refutation citation; expert_action_history annotation present. |
| 4 | Stay-wrong list integrity | ✅ Header `5 True Remaining Failures` → `4 True Remaining Failures (solver-corrected + 2026-05-06 graduation update)`; MW-25 row removed; graduation note added below table citing PR #209 + PR #213 + PR #215; MW-40 annotated as "graduation candidate; Opus CHECK HIGH on PILOT_787 (PR #213); 12.5I-MW40-VERIFICATION queued"; MW-17/MW-45/MW-47 unchanged; MW-31/MW-50 footer line preserved. |

## Audit 1 detail — TC-X-OWNER-SCOPE-DISCIPLINE first formal use

This is the first formal activation of the test class promoted from candidate in QC's PR #213 finding (`~/river-rats-qc/findings/2026-05-06-pr213-12.5I-C-labelling.md` § "Test class implications"). The audit verifies the diff stays strictly within orchestrator-authorized scope and does not silently mutate adjacent owner-scope files.

**True PR diff (against merge-base `c2021e7`, not stale origin/master):**

```
design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md       (+3/-0)
design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md     (+9/-5)
review/RESTART_PROMPT_V9_3WAY.md                             (+4/-3)
review/comms/BUILDER_REPORT_BATCH2_MW25_GRADUATION_*.md      (+105/-0; new)
```

**Memory file edited outside v2 repo** (cannot appear in PR diff): `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` — verified at QC end via direct read; new "Empirically Corrected Reference Labels (6 May 2026)" section + MW-25 entry exists with all 4 source PR # cites.

**Confirmed NOT touched** (per spec § "Verify NOT touched"):
- `prompts/gto_labeller_v3.4.md` ✓
- any `data/corpus_*.jsonl` ✓
- any `river-rats-core/` source (e.g., `reference_evaluator.py`) ✓
- any other v3.x prompt file ✓
- other stay-wrong list entries (MW-17/MW-40/MW-45/MW-47/MW-31/MW-50) — only MW-40 received an authorized annotation per dispatch ✓

**Diff anomaly note (transient):** Initial `git diff origin/master..PR-head` showed an extra 5th file (`MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR218_*.md`) because origin/master had advanced past PR #218's branch point with PR #219 (which added the trigger comm itself). True diff via `git merge-base` = clean 4 files. Documenting for QC procedural log.

## NIT-1 detail — Audit 2 citation form

Dispatch §"Audit 2" said: *"BATCH2_8_RANGE_ANALYSIS.md MW-25 entry's new reasoning cites the 4 evidence sources (PR #208 / PR #209 / PR #213 / v3.4 protocol traces) by PR # and confidence level."*

Actual citations in `BATCH2_8_RANGE_ANALYSIS.md` MW-25 detail block:

```
*[Empirically refuted by 12.5I-C 4-source convergence:
  5/5 pilot CHECK +
  Opus 4.7 HIGH (PR #209) +
  30/30 unanimous CHECK 1.0 conf parametric (PR #213) +
  v3.4 protocol traces.]*
```

And the new "Expert action history" line:

```
2026-05-06: BET HIGH → CHECK HIGH (4-source graduation per PR #209 + PR #213 + PR #215).
```

**3 of 4 sources cited by PR # (PR #209 + PR #213 + PR #215); 1 source (PR #208 pilot) cited by description ("5/5 pilot CHECK") without PR #.** Information is complete; form deviates from dispatch's "by PR #" instruction on one source.

`reference_corrections.md` (memory) DOES cite all 4 by PR # (PR #208 / PR #209 / PR #213 + protocol traces) cleanly, so the cross-cite chain reader can resolve PR #208 within one hop.

**Why NIT not SHOULD_FIX:**
- Information complete + correct (no missing evidence)
- Cross-cite chain intact via memory file
- Reader navigation cost ~0 (memory file is one-click reachable)
- Dispatch's "by PR #" specifies form, not content; substantive evidence integrity is preserved

**Suggested fix-forward (optional, not blocking):** add `(PR #208)` after "5/5 pilot CHECK" in the BATCH2_8_RANGE_ANALYSIS.md detail block. 1-line edit, can be folded into the next BATCH2 reference touch (e.g., MW-40 graduation update if it lands).

## Audit 3 detail — canonical label correctness

The reference_evaluator pipeline reads the MW-25 expert action from `BATCH2_8_RANGE_ANALYSIS.md` GTO Action Table at line 27 (per builder report's correct cite of `river-rats-core/reference_evaluator.py:230-265`). The summary-table edit alone is sufficient for downstream pipeline behavior to pick up CHECK HIGH on next reference evaluation.

**Builder report's "File-mapping clarification"** (re: dispatch said `BATCH2_8_HAND_DESIGNS.md` has `expert_action: BET HIGH` field that does not exist) — verified by QC: the canonical label IS in `BATCH2_8_RANGE_ANALYSIS.md`, NOT in `BATCH2_8_HAND_DESIGNS.md`. Builder's correct call to (a) edit the canonical location and (b) annotate `BATCH2_8_HAND_DESIGNS.md` with a redirect note. Slow-quality default per `feedback_quality_default_no_ask.md` correctly applied.

The triple-edit pattern in `BATCH2_8_RANGE_ANALYSIS.md` (summary table + detail section + Axis 4 insight) is consistent — no internal contradictions.

## Audit 4 detail — stay-wrong list integrity

`review/RESTART_PROMPT_V9_3WAY.md` updates verified:

- Header: `5 True Remaining Failures` → `4 True Remaining Failures (solver-corrected + 2026-05-06 graduation update)` ✓
- MW-25 row removed from table ✓
- MW-40 row annotated: `Residual passive (very thin value bet) — graduation candidate; Opus CHECK HIGH on PILOT_787 (PR #213); 12.5I-MW40-VERIFICATION queued` ✓
- Other rows (MW-17, MW-45, MW-47) unchanged ✓
- Graduation paragraph added below table citing 4-source convergence + PR #209/213/215 + ending statement "Stay-wrong count 5 → 4" ✓
- Footer line `Plus MW-31, MW-50 (unverified, likely model correct).` preserved ✓

No silent modifications to other entries. No scope creep.

## Process observation

**20th successive solo-routed cycle.** Loop heartbeat (Monitor) detected this dispatch within ~1 min of master commit (master `cb86c9d` at 16:51:31Z; QC_DISPATCH event at 16:51:31Z; this audit response ~17:00Z).

Note: two Monitors (`bssngxfls` from initial loop install; `b6to9rj7z` from re-arm during fallback tick) emitted duplicate events for this dispatch. No correctness impact (same dispatch is in flight; QC writes only one PR). One Monitor will be retired at next session-end or via TaskStop. Logging for QC procedural improvement.

## Test class implications

- **TC-X-OWNER-SCOPE-DISCIPLINE first formal activation** ✓. Promoted from candidate (PR #213 finding) to standing class. Pattern: pre-merge audit on any owner-scope reference-set / stay-wrong list / `memory/reference_corrections.md` / v3.x prompt change verifies (a) diff strict to authorized scope, (b) no silent mutation of adjacent owner-scope files, (c) cross-cite chain integrity. Adding to `learning/test_class_registry.md`.
- **Stale-master-diff false positive**: when comparing PR head to a moving master, use `git merge-base` to derive the true PR diff. Procedural improvement note for `learning/incident_pattern_library.md`.
- **Citation form audit** — first NIT-level finding on citation completeness vs dispatch wording. Worth registering as a sub-audit class under TC-X-OWNER-SCOPE-DISCIPLINE: "verify cite-by-# count matches dispatch spec for evidence sources."

## What gates on this audit

Per dispatch:
- PR #218 merge → **on this PASS** (no Opus tier-up needed; doc + memory only)
- 12.5I-D corpus QC dispatch → on PR #218 merge
- 12.5I-MW40-VERIFICATION-A design dispatch → on PR #218 merge
- 12.5J-D-pre test-guard deflake → tail of queue

## Full evidence

`~/river-rats-qc/findings/2026-05-06-pr218-batch2-mw25-graduation.md`

## References

- PR #218 head: `ee5aa5c`
- PR #218 base (merge-base): `c2021e7`
- QC audit trigger: PR #219 (master `cb86c9d`) → comm `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR218_2026-05-06.md`
- Orchestrator decisions + Step 1 dispatch: PR #217 (master `d6912ad`)
- BORDERLINE-17 HALT comm with 3 owner WHAT decisions: PR #216 (master `8b078bf`)
- PR #213 (12.5I-C labelling, 30/30 unanimous CHECK Step 1 evidence): master `994ae67`
- PR #215 (QC PASS verdict on PR #213): master `c2021e7`
- PR #209 (Opus 4.7 MW-25 re-eval): master `077c168`
- PR #208 (12.5I-C pilot 5/5 CHECK): master `52e5164`
- Reference evaluator (canonical label location): `river-rats-core/reference_evaluator.py:230-265`
- Memory file (verified externally): `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `feedback_spec_vs_infrastructure_code_drift.md`
- Prior cycle: `~/river-rats-qc/findings/2026-05-06-pr213-12.5I-C-labelling.md`
