---
date: 2026-04-26
from: River Rats QC stream
to: Logic builder · Main terminal (orchestrator) · Owner (briefed)
re: PR #35 pre-merge QC audit — Build A (Protocol B labeller-facing pilot v1.0.1-pilot); APPROVE-WITH-NITS; V-A1...V-A8 adversarial vectors PASS; 2 frontmatter consistency NITs
status: FLAG (advisory; pre-merge informational)
severity: APPROVE-WITH-NITS at gate / no HIGH/MEDIUM findings
PR head: f95cdab74a76ebbb78fe9cf1c2519aa0552de682
full finding: ~/river-rats-qc/findings/2026-04-26-pr35-pre-merge-build-a.md
---

# QC Pre-Merge Audit — PR #35 (Build A)

## Headline

**APPROVE-WITH-NITS.** Build A cleanly closes PRE-DISPATCH PREREQUISITES row #5 (RED → GREEN candidate). All 8 V-A adversarial vectors (pre-scoped per QC's `2026-04-26-builds-abc-pre-merge-audit-scope.md`) PASS. 2 frontmatter consistency NITs; doesn't affect inlined-content correctness.

## V-A1...V-A8 vector results

| Vector | Result | Note |
|--------|--------|------|
| V-A1 inheritance markers | ✅ PASS | grep returns 0 matches across {see source artifact, see canonical, copy verbatim, design artifact, etc.} |
| V-A2 §Buckets verbatim | ✅ PASS | v3.1 lines 170-204 §"Step 1: CLASSIFY THE HAND"; section header explicit |
| V-A3 §Features verbatim + infra contract | ✅ PASS | 54 v3.1 + 1 board_adjusted_hrp + 4 v2.4 P1 = **59 raw**; matches Stage 5 retrain v1.0.1 §Hyperparameters point #4 |
| V-A4 §DO NOT Rules verbatim | ✅ PASS | Rules 1-10 quoted with `> ` prefix; v1.0.1 design summary item 11 subsumed into Rule 10 |
| V-A5 frontmatter pilot-runtime + provenance | ✅ PASS | version=v1.0.1-pilot; artifact_class=PILOT-RUNTIME; build_provenance + derived_from-with-master-commit. Sha256 absent but git commit hash anchors equivalence |
| V-A6 byte differential | ✅ PASS | pilot 73247 bytes vs source 61515 bytes (delta +11732 from inlining; expected) |
| V-A7 design→pilot scope | ✅ PASS | §"Pilot artifact build provenance (Build A output)" header replaces design-artifact framing |
| V-A8 TC-23 file existence | ✅ PASS | `prompts/protocol_b_composition_first_v1_0_pilot.md` at canonical path |

## NITs

### NIT-1 — Frontmatter §DO NOT Rules line-range inconsistency

| Location | Range |
|----------|-------|
| Line 14 | 590-647 |
| Line 24 | 590-647 (Rules 1-11) |
| Section header line 540 | 590-647 |
| Footer line 606 | 595-647 |
| PR body | 590-647 (Rules 1-10) |

Footer + section content suggest 595-647 is rules content range; 590 may include preamble. NIT-level — doesn't affect inlined-content correctness.

**Suggested fix:** standardize on either 590-647 (full incl. preamble) or 595-647 (rules only) across frontmatter + section header + footer.

### NIT-2 — Frontmatter rule-count "Rules 1-11" vs "Rules 1-10"

Line 24 says `(Rules 1-11)`; PR body + footer + actual content say "Rules 1-10 with item 11 subsumed into Rule 10". Internal consistency drift.

**Suggested fix:** frontmatter line 24 → `(Rules 1-10; v1.0.1 design summary 11 subsumed into Rule 10 verbatim)`.

## Multi-expert verdict

SOLO. Single-file 1458-line spec-aligned build; multi-expert overkill. Vector pre-scoping was the multi-expert layer (independent QC framing of what to check).

## Recommendation

**APPROVE merge.** All V-A1...V-A8 vectors PASS. NIT-1 + NIT-2 are reviewer + builder call; doesn't gate.

After merge: PRE-DISPATCH row #5 transitions RED → GREEN. Build B (Protocol C labeller-facing pilot artifact) starts next per orchestrator's serial directive.

## QC mode

Continuing Layer 1+2 audit for Build B PR drop. Adversarial vectors V-A1...V-A8 + V-B1...V-B3 ready per pre-emptive scoping.

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-pr35-pre-merge-build-a.md`
- PR #35: https://github.com/beytell1-sketch/river-rats-v2/pull/35
- Pre-emptive vector scoping: published QC-internal at PR #34 absorbed via Path B
- Orchestrator directive: `MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md` (master `3f9564e`)

**Status: APPROVE-WITH-NITS. Recommend merge.**
