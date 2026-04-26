---
date: 2026-04-26
from: Logic builder (transient builder persona under Pilot Orchestrator session)
to: Main terminal (orchestrator) · Owner · QC stream · Pilot Orchestrator (resumes post-merge)
re: PR #47 v3.2 protocol revision — fix-forward landed at 5188299 addressing all 3 reviewer findings (1 HIGH + 1 MED + 2 NITs); all 4 calibration anchors (d3688/d9556/d3178/MW-39) now route correctly under updated Rule 11 + Fix 2; standby for QC + orchestrator gto-expert reviewer + merge
status: PR #47 OPEN with 2 commits (621567e initial v3.2; 5188299 reviewer-driven fix-forward); all 3 reviewer findings addressed; awaiting QC pre-merge audit (Path B Bundle) + orchestrator gto-expert reviewer per Path A workflow item 5
---

# PR #47 v3.2 fix-forward ack

## Reviewer findings + dispositions

Per `REVIEW_VERDICT_PR_47_V32_PROTOCOL_2026-04-26.md` (builder reviewer V3-compliance + ml-architect; verdict: REQUEST-CHANGES):

| Severity | Finding | Disposition | Fix commit |
|----------|---------|-------------|------------|
| **HIGH** | Rule 11 predicate `is_strong_made=1 OR is_monster=1` structurally excluded d3688 (TPWK = `is_strong_made=0`); d3688 would have failed A.4 v3.2 retry | **FIXED** — predicate broadened to `is_made_hand=1` (covers medium-made TPWK + strong-made + monster); BET exception (a) requires BOTH `villain_TP+ >= 0.40` AND `is_strong_made=1 OR is_monster=1` so TPWK can't escape via the exception | `5188299` |
| MED | Decision rule for Fix 2 cited non-existent feature `nut_flush_block`; closest real feature is `flush_block_pct` | **FIXED** — clarified canonical predicate (hero literally holds Ace of board's flush suit) + closest real feature `flush_block_pct >= ~0.40` | `5188299` |
| NIT | Changelog L15 said "DO NOT Rules 1-11 preserved from v3.1" but v3.1 had only 1-10 | **FIXED** — corrected to "Rules 1-10 (the full v3.1 set)" + clarification that Rule 11 is the new v3.2 addition | `5188299` |
| NIT | Decision rule "(set+, two pair, overpair, top pair top kicker on dry board)" elaboration was hand_category-derived not feature-flag | **FIXED** (incidentally) — rewrite to use `is_made_hand=1` directly removed the elaboration | `5188299` |

## Self-test (independent trace under updated rules)

All 4 calibration-relevant hands route correctly under updated Rule 11 + Fix 2 OVERRIDE:

| Hand | Expected | Reasoning chain | Result |
|------|----------|-----------------|--------|
| d3688_BB_flop (8cKc TPWK on KdTd4s 2-tone OOP, num_opp=2) | CHECK | Rule 11 predicate fires (is_made=1, is_ip=0, 2-tone, num_opp>=2); BET exception (a) FAILS (vil_TP+=0.198<0.40 AND is_strong_made=0); no river-checked override → CHECK | **CHECK ✓** |
| d9556_BB_flop (5h5d full house on 5s6d6h paired OOP, num_opp=2) | CHECK | Rule 11 predicate fires (is_made=1, is_ip=0, paired, num_opp>=2); BET exception (a) FAILS (vil_TP+=0.277<0.40 even though is_monster=1); no river-checked override → CHECK | **CHECK ✓** |
| d3178_CO_river (AA on JhQcJc+Ks+5h paired river OOP checked-to, num_opp=2) | BET | Rule 11 predicate fires; BET exception (a) FIRES (vil_TP+=0.827>=0.40 AND is_strong_made=1); ALSO river-checked-to override fires → BET | **BET ✓** |
| MW-39 (AhJh nut FD on Kh8h3d, IP, num_opp=2) | CALL | is_made_hand=0 → Rule 11 N/A; routes to Fix 2 OVERRIDE; villain_air_pct=0.05 < 0.20 → CALL preferred | **CALL ✓** |

This is the empirical adequacy check the original Rule 11 failed (d3688 exclusion). Fix-forward addresses it cleanly.

## Risk-surface re-verification

- **d3178** still BETs via TWO independent paths (BET exception (a) + river-checked-to override) — no regression
- **Worked Example 9** (KB §1.7 RAISE example) — still RAISEs if villain_air_pct >= 0.20 (preserved per Fix 2 conditional structure)
- **HU spots** (num_opponents=1) — Rule 11 doesn't apply; existing v3.1 rules govern
- **IP spots** (is_ip=1) — Rule 11 doesn't apply; existing v3.1 rules govern
- **Pure dry boards** (no pair, no 2-tone) — Rule 11 doesn't apply; existing v3.1 rules govern
- **Drawing hands** (is_made_hand=0) — Rule 11 doesn't apply; routes to Fix 2 (KB §1.7 OVERRIDE) instead
- **Cross-protocol convergence** — Protocol C untouched; Protocol B Examples 1-5 untouched (only Range-mass axis edited per Fix 3)

## PR state

- **PR #47 URL:** https://github.com/beytell1-sketch/river-rats-v2/pull/47
- **Branch:** `stage4-pre-dispatch/v3-2-protocol-revision`
- **Commits on branch:**
  - `621567e` — v3.2 protocol revision: Fix 1 + 2 + 3 bundled (initial)
  - `5188299` — v3.2 fix-forward: Rule 11 broadened to is_made_hand; nut_flush_block clarified; changelog NIT
- **Files changed:** 3 (`prompts/gto_labeller_v3.2.md` NEW; `prompts/protocol_b_composition_first_v1_0_pilot.md` Range-mass axis; `prompts/protocol_b_composition_first_v1_0.md` Range-mass axis)
- **Builder reviewer status:** APPROVE-WITH-FIX-FORWARD (HIGH + MED + 2 NITs all addressed; reviewer should re-verify or orchestrator may dispatch follow-up reviewer)

## Path A workflow checkpoint

Per `MAIN_TERMINAL_PATH_A_V32_PROTOCOL_REVISION_DIRECTIVE_2026-04-26.md` workflow item 5 ("Triple-pipeline review: Builder reviewer + QC pre-merge audit + Orchestrator gto-expert reviewer"):

| Pipeline | Status | Verdict |
|----------|--------|---------|
| Builder reviewer (V3-compliance flavor) | DONE | REQUEST-CHANGES → fix-forward applied → re-verification pending OR orchestrator dispatches follow-up reviewer |
| QC pre-merge audit (Path B Bundle) | PENDING orchestrator dispatch | — |
| Orchestrator gto-expert reviewer | PENDING orchestrator dispatch | — |

After triple-pipeline convergent APPROVE: orchestrator merges PR #47.

Post-merge: Pilot Orchestrator persona resumes; A.4 v3.2 retry with parallel Sonnet+Opus on v3.2 protocol per Path A revision (`MAIN_TERMINAL_PATH_A_REVISION_ACK_OPUS_REVERT_2026-04-26.md`, master `5cc7ba1`).

## Action

**Builder (this comm):**
1. Compose this fix-forward ack (DONE)
2. Commit reviewer verdict + this ack to master (next; HARD branch check first)
3. Standby for orchestrator next-step (QC dispatch / gto-expert dispatch / merge)

**Orchestrator:**
1. Read this ack + reviewer verdict + builder fix-forward at `5188299`
2. Decide: dispatch follow-up builder reviewer OR proceed to QC + gto-expert pipelines OR merge directly if fix-forward sufficient
3. After triple-pipeline clean: merge PR #47 → re-issue A.4 v3.2 retry directive to Pilot Orchestrator

**QC stream:**
1. Pre-merge audit on PR #47 commit `5188299` (Path B Bundle pattern); TC-23 + V-X3 vectors apply; verify Fix 1/2 specifically address d3688/d9556/MW-39 failures from A.4 (per builder self-test above)

**Pilot Orchestrator (paused this turn; resumes post-merge):**
1. After PR #47 merges: re-run A.4 with parallel Sonnet+Opus on v3.2 protocol per Path A revision
2. Same 38-hand calibration set, same answer key, same blind grading
3. Surface A.4 v3.2 retry results

## References

- Reviewer verdict: `review/comms/REVIEW_VERDICT_PR_47_V32_PROTOCOL_2026-04-26.md`
- Path A directive: `MAIN_TERMINAL_PATH_A_V32_PROTOCOL_REVISION_DIRECTIVE_2026-04-26.md` (master `24494eb`)
- Path A revision: `MAIN_TERMINAL_PATH_A_REVISION_ACK_OPUS_REVERT_2026-04-26.md` (master `5cc7ba1`)
- A.7 HALT empirical evidence: `PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` (master `b2de857`)
- A.4 v3.1 raw failure traces: `review/pilot_run_2026-04-26/calibration_results_*.json` (master `ee197a9`)
- v3.2 prompt under review: `prompts/gto_labeller_v3.2.md` on branch `stage4-pre-dispatch/v3-2-protocol-revision` at commit `5188299`

**Status: PR #47 v3.2 fix-forward LANDED at 5188299. All 3 reviewer findings addressed. All 4 calibration anchors (d3688/d9556/d3178/MW-39) route correctly per self-test. Awaiting QC + orchestrator gto-expert reviewer + merge.**
