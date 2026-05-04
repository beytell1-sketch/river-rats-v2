---
date: 2026-05-04
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #126 audit (now POST-MERGE) — CONVERGED APPROVE with parallel-dispatched QC subagent; +1 SOLO NIT
severity: NIT (no HIGH / MEDIUM / LOW)
status: POST-MERGE confirmation — PR #126 already merged at d7d2cdd per orchestrator's parallel QC verdict; this finding adds 1 NIT not caught by the parallel subagent
test-class: TC-23-CONTENT + TC-23-CANONICAL-STATE + V-Source-1/3/4 + V-X4 + TC-15 (multi-expert convergence)
multi-expert verdict: **CONVERGED** with `/tmp/qc_125d_findings.md` (orchestrator's parallel QC subagent) on APPROVE + NIT-2; **SOLO** add of NIT-1
---

# QC Finding — PR #126 audit (TC-23 sub-vector): CONVERGED APPROVE + 1 SOLO NIT

## Process note (read first)

This finding was produced **independently and in parallel** with the QC subagent the orchestrator dispatched as part of the three-way A/B/C decision sequence (referenced as `/tmp/qc_125d_findings.md` in `MAIN_TERMINAL_PHASE125D_SYNTHESIS_OWNER_GATE_2026-05-04.md` line 136). Neither voice was aware of the other during execution.

The orchestrator's synthesis already merged PR #126 (commit `d7d2cdd`) on the parallel subagent's APPROVE verdict before this finding landed. **No corrective action needed** — verdicts converge on the merge decision.

This finding serves three purposes now that it lands post-merge:
1. **TC-15 multi-expert convergence record** — independent confirmation of the parallel subagent's APPROVE
2. **+1 SOLO NIT (V-X4)** that the parallel subagent missed
3. **Process observation** — the orchestrator dispatched QC via fallback subagent without routing through the standalone QC stream session that was active. Not a problem this cycle (CONVERGED), but worth noting for future cycles.

## Headline

**CONVERGED APPROVE.** Both QC voices (this standalone stream + orchestrator's parallel-dispatched subagent) independently APPROVE PR #126. Both flag the NIT-2 "promoted to /tmp" wording cleanup. This standalone audit additionally surfaces NIT-1 (V-X4 carryforward overclaim in BLOCKED comm) which the parallel subagent missed.

All three orchestrator-dispatched sub-axes (diff scope + citation existence + provenance) cleared cleanly. Two NIT-class prose inconsistencies; substance correct in both. PR #126 now merged.

## Audit scope (per `MAIN_TERMINAL_PHASE125D_GATE_FAIL_DECISION_2026-05-04.md`)

> QC — pre-merge audit on PR #126 (TC-23 sub-vector: diff scope + citation existence + provenance). HOLD or APPROVE.

PR #126 head audited: `d20297d94981269efc597f1c0c912046bfedf4da` (branch `programmer/phase125d-trainer-impl-2026-05-03`).

## Verification summary

| Sub-axis | Findings | Verdict |
|---|---|---|
| **Diff scope** | 4 files, +2097 / -0, no model artifact, zero `gto_model.py` edits, all-additions / no-canonical-mutation | ✅ CLEAN |
| **Citation existence** | 8/8 cited paths resolved (incl. 1 correctly-noted-absent v8-38feat per #PSH-01); 4/4 cited PRs merged at cited SHAs; 6 load-bearing symbol-level citations corroborated | ✅ CLEAN |
| **Provenance** | Master HEAD `e3c0dfc` matches dispatch SHA; warm-start anchor SHA256 matches bit-for-bit (`9f3845bb...`); all 10 numerical claims (per-seed scores, mean/std, baseline gap, P1 blocker importances, test count) cross-source-consistent | ✅ CLEAN |

**Bonus check:** orchestrator's "5 under-bet + 2 over-aggress + 2 RAISE collapse" decomposition cross-checked against the per-hand divergence table (PROGRAMMER_REPORT lines 138-148). Empirically correct: 9 failures × 40 = 31/40 score arithmetic holds. Orchestrator's load-bearing observation gating the WHAT decision is sound.

## Two NIT-class findings (advisory, do-not-block)

### NIT-1 — V-X4 carryforward overclaim in BLOCKED comm

`BUILDER_BLOCKED_PHASE125D_GATE_FAIL_2026-05-03.md` lines 83-90 say "Three files (NOT four — no model artifact per stop condition)" + "Plus this BUILDER_BLOCKED comm, separately." But the comm IS in PR #126 (4 files total per `gh pr view 126`); it didn't ship "separately." `PROGRAMMER_REPORT` line 251 correctly says "4-file deliverable diff" — so the BLOCKED comm contradicts both PR reality AND its own sibling report.

Substance ("no model artifact") is correct. Wording is stale relative to the executed plan (looks like a pre-bundle draft that didn't get updated when the comm was rolled into the PR instead of pushed separately).

**Suggested fix-forward (advisory):** small textual edit in a follow-up comm or PR — "Four files (no model artifact per stop condition)" + drop "Plus this BUILDER_BLOCKED comm, separately."

### NIT-2 — "promoted to /tmp/" terminology drift

`PROGRAMMER_REPORT` line 261: "Median-litmus seed promoted to `/tmp/builder-12.5D-wt/...gto_model_v9_student.json`. Awaiting QC pre-merge audit + ml-architect/gto-expert review."

Section A (line 22) and Section D (line 239) get the terminology right — "no model promoted." Only line 261 drifts. The model was *written to worktree for inspection*, not *promoted to canonical path*; "promotion" is a defined term in this project meaning canonical-path write-and-commit, which deliberately did NOT happen per stop condition #3.

**Suggested fix-forward (advisory):** rephrase line 261 — "Median-litmus seed model was written to `/tmp/builder-12.5D-wt/...` for ml-architect/QC inspection but NOT promoted to canonical path per stop condition."

## Recommended scope partition (the two parallel dispatches)

QC's mechanical audit deliberately did NOT cover (per orchestrator dispatch scope; reserved for the parallel dispatches):

- **TC-23-CONTENT line-by-line patch-vs-spec** against blueprint §6 — recommend ml-architect picks up in their post-mortem
- **Methodological soundness of `_StudentInference` mirror** — explicitly ml-architect's parallel dispatch
- **Per-hand poker analysis of failures** — explicitly gto-expert's parallel dispatch

QC verified the mirror EXISTS and is structured as the report describes (line 522-535 header + line 536 class + line 582-585 helper docstring + line 681-682 baseline-vs-student split). QC did NOT verify the mirror is CORRECT under all inference conditions — that's ml-architect.

QC verified the orchestrator's COUNT-BASED mixed-direction decomposition. QC did NOT interpret the poker-theoretic implications — that's gto-expert.

The 3-way parallel dispatch is well-partitioned; this finding is independent of and complementary to the other two.

## Test class implication

Both NITs are V-X4 hits (existing class added 2026-04-26). No new test class needed; no curative-additions-log entry needed.

NIT-1 is worth noting as a **sub-pattern** worth tracking in `incident_pattern_library.md` — "comm self-describes its own ship state, but ship state changed during PR finalization and the prose didn't get updated" — sub-pattern of #18 (carryforward overclaim). If it recurs, promote to its own pattern.

## Full finding location

`~/river-rats-qc/findings/2026-05-04-pr126-pre-merge-tc23-subvector.md` (QC repo; full evidence + table-by-table verification trace).

## Status

**POST-MERGE confirmation:** PR #126 already merged (`d7d2cdd`) on parallel-dispatched QC subagent's APPROVE per `MAIN_TERMINAL_PHASE125D_SYNTHESIS_OWNER_GATE_2026-05-04.md`. This standalone QC voice converges on APPROVE; no action change.

**Owner WHAT decision (A/B/C/C') is the live gate**, not this finding.

Two advisory NITs (NIT-1 SOLO + NIT-2 CONVERGED): orchestrator + builder decide whether to fix-forward or leave as-is. They do not gate anything.

## TC-15 multi-expert convergence record

| Axis | Standalone QC stream verdict | Parallel QC subagent verdict (per synthesis lines 64-73) | Outcome |
|---|---|---|---|
| Overall | APPROVE | APPROVE | **CONVERGED** |
| Diff scope | CLEAN (4 files, +2097/-0, no model artifact) | "Diff scope — exactly 4 files; zero edits to existing source surfaces; no model artifact" | **CONVERGED** |
| Citation existence | CLEAN (8/8 paths, 4/4 PRs, 6/6 symbols) | "Citation existence (TC-23) — zero drift at current master HEAD; all citations verified live" | **CONVERGED** |
| Provenance | CLEAN (warm-start SHA256 bit-for-bit; 10/10 numerical claims; e3c0dfc HEAD) | "Provenance — warm-start anchor SHA256 9f3845bb...c366900 matches; xgboost/numpy/python versions match" | **CONVERGED** |
| NIT-2 ("promoted to /tmp") | flagged | flagged ("trainer report line 261 says...wording cleanup, technical state correct") | **CONVERGED** |
| NIT-1 (BLOCKED comm "Three files NOT four" V-X4) | flagged | NOT flagged | **SOLO** (this stream) |
| Mixed-direction decomposition cross-check | empirically corroborated (5+2+2 = 9 failures = 31/40 holds) | NOT in subagent scope | **SOLO** (this stream) — but converges with gto-expert finding 2 in synthesis |

**Confidence boost:** TC-15 protocol-diversity outcome as expected — CONVERGED at gate-decision level (high confidence on APPROVE) + DIVERGED at finding level (one extra NIT surfaced by single voice). This is the "ideal" multi-expert pattern per `~/river-rats-qc/learning/test_class_registry.md` TC-15.

## Test class implication updated

- **TC-15** instance recorded — second pre-merge audit demonstration of CONVERGE-at-gate / DIVERGE-at-finding pattern (first was 2026-04-26 TC-10 first-run on PRs #5-#9). Pattern now confirmed on a second high-stakes audit.
- **NIT-1 surfacing pattern** — sub-pattern of incident #18 (carryforward overclaim) — comm self-describes its ship state but ship state changes during PR finalization. Worth tracking; promote to its own pattern if it recurs.
- **Process observation** — dispatching QC via fallback subagent in parallel with active standalone QC stream is a TC-18 (reviewer-pool diversity) sub-case. Not a process bug this time (CONVERGED), but if the standalone QC voice were to DIVERGE significantly from a parallel subagent verdict in the future, that's a process integrity question worth surfacing.
