---
date: 2026-05-04
from: River Rats QC
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #126 pre-merge audit — APPROVE for merge; 2 NIT-class prose inconsistencies (advisory)
severity: NIT (no HIGH / MEDIUM / LOW)
status: FLAG → APPROVE; QC-side hold lifts
test-class: TC-23-CONTENT + TC-23-CANONICAL-STATE + V-Source-1/3/4 + V-X4
multi-expert verdict: SOLO (mechanical sub-vector audit per orchestrator dispatch scope)
---

# QC Finding — PR #126 pre-merge audit (TC-23 sub-vector): APPROVE

## Headline

**APPROVE PR #126 for merge.** All three orchestrator-dispatched sub-axes (diff scope + citation existence + provenance) clear cleanly. Two NIT-class prose inconsistencies surfaced; substance is correct in both. QC's hold on PR #126 lifts. Other gates (gto-expert, ml-architect, owner WHAT decision) remain.

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

**QC-side gate cleared. PR #126 may merge whenever the orchestrator and other reviewers (gto-expert, ml-architect) clear and the owner makes the WHAT decision.**

Two advisory NITs: orchestrator + builder decide whether to fix-forward or leave as-is. They do not block.
