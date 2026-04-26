---
date: 2026-04-26
from: V3-compliance reviewer (orchestrator-dispatched)
to: Main terminal (orchestrator) · Logic builder · Owner (briefed)
re: PR #37 (Build B — Protocol C labeller-facing pilot v1.0.1-pilot) — V3-compliance content verification
status: APPROVE-WITH-NITS
---

# V3-Compliance Review — PR #37 (Build B)

## Verdict: APPROVE-WITH-NITS

Content fidelity is byte-perfect across all three verbatim-inlined
sections. Spec-vs-code feature contract clean. NIT-1 + NIT-2
carryforward from Build A pre-empted exactly as the PR claims.
Cross-build inlined-content consistency vs Build A is byte-identical.

The single residual NIT (already raised by builder-reviewer 294a61c
at body line 1563) is verbatim source content from the design
artifact at master HEAD `c4f29a5` and is correctly OUT-OF-SCOPE for
the orchestrator's frontmatter-only NIT-cleanup directive. Not
blocking.

**Recommendation: merge as-is.**

## Source / artifact provenance verified

- master HEAD (source of truth): `c4f29a5` (current `~/river-rats-v2/` master tip)
- Build A merge SHA (cross-build comparator): `2ea67d0`
- PR #37 head: `2a597b4aea3d553c75c682a8d8919ab806f05618` on
  `stage4-pre-dispatch/protocol-c-pilot-build`
- Verbatim source: `prompts/gto_labeller_v3.1.md` @ master `c4f29a5`
  (730 lines)
- Pilot artifact under review: `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`
  on PR #37 head (1964 lines)
- Build A pilot (cross-build comparator): `prompts/protocol_b_composition_first_v1_0_pilot.md`
  @ `2ea67d0` (1458 lines)

All comparisons below run against staged copies of these exact blobs
(via `git show <sha>:<path>`).

## §Buckets (v3.1 lines 170-204)

**Result: BYTE-PERFECT VERBATIM. Clean diff.**

Pilot quotes lines 640-674 (35 lines) of the pilot artifact;
stripping `> ` blockquote prefix + restoring blank-line markers
yields a byte-identical match to v3.1 lines 170-204. All 6 buckets
present in correct order: monster · strong_made · medium_made ·
weak_made · drawing · air. All worked examples (8h8c on 8d 5s 2c,
AhKd on Ad 9c 3h, KhJd on Kc 8s 5d, 5h4h on Kc 8s 5d, Th9h on
7h 6h 2c, QcJd on 8s 5d 2c) preserved. Closing line "State the
bucket explicitly..." preserved.

Section-header line range citation (line 638: "lines 170-204") is
correct.

## §Features (v3.1 lines 439-496 + v2.4 P1 blockers; 59-feature contract)

**Result: BYTE-PERFECT VERBATIM for rows 1-54. Spec-vs-code feature names 55-59 CLEAN.**

Pilot quotes lines 691-748 (58 lines including header + table-format
row + 54 data rows); stripping `> ` blockquote prefix yields a
byte-identical match to v3.1 lines 439-496. All 54 feature rows
present in correct order with exact descriptions, including the
v3.1-specific descriptors (e.g. row 42 `villain_range_capped`
"Preflop structural label ONLY"; row 54 `villain_medium_made_pct`
description with "(2nd pair, bottom pair)" parenthetical).

**Feature 55 (`board_adjusted_hrp`):** present at pilot line 752 as
prose note (not table), correctly attributing Stage 5 un-hold per
MUST #48 in `BUILDER_V24_STAGE35_BLUEPRINT_V2_3_AMENDED_2026-04-22.md`.

**Features 56-59 (v2.4 P1 blockers):** pilot lines 765-768.
Cross-checked against `river-rats-core/feature_extractor.py`
`FEATURE_COLUMNS` at master HEAD `c4f29a5` (lines 1606-1612):

| # | Pilot name | feature_extractor.py name | Match |
|---|------------|---------------------------|-------|
| 55 | `board_adjusted_hrp` | `board_adjusted_hrp` | YES |
| 56 | `nut_flush_block` | `nut_flush_block` | YES |
| 57 | `flush_draw_block_pct` | `flush_draw_block_pct` | YES |
| 58 | `straight_draw_block_pct` | `straight_draw_block_pct` | YES |
| 59 | `nut_made_block_pct` | `nut_made_block_pct` | YES |

Total raw feature count claim ("59 raw" = 54 v3.1 + 1 board_adjusted_hrp + 4 v2.4 P1 blockers) matches `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4. Clean.

## §DO NOT Rules (v3.1 lines 590-647)

**Result: BYTE-PERFECT VERBATIM. Clean diff.**

Pilot quotes lines 784-841 (58 lines); stripping `> ` blockquote
prefix yields a byte-identical match to v3.1 lines 590-647. Full
preamble ("These target specific LLM reasoning failures in poker.
Each explains WHY the naive reasoning is wrong so you can
generalise.") preserved. All 10 numbered rules present:

| Rule | Topic | Status |
|------|-------|--------|
| 1 | DO NOT decide based on equity alone | VERBATIM |
| 2 | DO NOT barrel draws into 2 opponents | VERBATIM |
| 3 | DO NOT assume the checking player has nothing | VERBATIM |
| 4 | DO NOT auto-c-bet IP just because you have position | VERBATIM |
| 5 | DO NOT treat top pair as a strong hand | VERBATIM |
| 6 | DO NOT overweight blockers | VERBATIM |
| 7 | DO NOT analyze streets in isolation | VERBATIM |
| 8 | DO NOT assume both opponents have equivalent ranges | VERBATIM |
| 9 | DO NOT use `villain_range_capped` as a postflop strength signal | VERBATIM |
| 10 | DO NOT confuse `hero_range_percentile = 0.00` with bottom-of-range holdings (incl. `[v3 addition §3.B]` HRP test-harness warning) | VERBATIM |

The footer (pilot lines 843-847) explicitly notes Rule 10 subsumes
the v1.0.1 design summary's "item 11" (HRP test-harness warning),
correctly framing this as an enumeration-numbering housekeeping
note, not a content change.

## Build A NIT carryforward verification

**NIT-1 (line range "590-647" consistency throughout) — PRE-EMPTED CLEAN.**

Build A QC flagged "590-647 vs 595-647" inconsistency. Audit on
PR #37 head — every line-range citation for the §DO NOT Rules
inlining uses **590-647** (no 595-647 stragglers anywhere):

- frontmatter L14: "lines 590-647"
- frontmatter L24: "v3.1 lines 590-647 (Rules 1-10..."
- frontmatter L29 (NIT-1 self-attestation): "Used line range 590-647 throughout..."
- provenance §body L90: "(lines 590-647; Rules 1-10..."
- provenance §body L121-122: "(line-range consistency 590-647 vs 595-647...) are pre-empted"
- §DO NOT Rules section header L778: "lines 590-647"
- §DO NOT Rules footer L843-844: "10 numbered DO NOT Rules at lines 590-647"

Result: 7 occurrences, all 590-647. NIT-1 cleanly closed.

**NIT-2 (rule count format expanded, not "Rules 1-11" shorthand) — PRE-EMPTED CLEAN in declared scope (frontmatter + section meta).**

Build A QC + reviewer flagged "Rules 1-11" shorthand. Audit on PR
#37 head — frontmatter / provenance / section-meta all use the
expanded format:

- frontmatter L24: "Rules 1-10; v1.0.1 design summary item 11 subsumed into Rule 10 verbatim, per v3 §3.B HRP test-harness warning"
- frontmatter L30 (NIT-2 self-attestation): explicit format used
- provenance §body L90: same expanded format
- §DO NOT Rules footer L843-847: explicit elaboration that v3.1 source has 10 rules, design summary's item 11 is subsumed into Rule 10

In the orchestrator-declared scope (frontmatter + section meta), NIT-2 is cleanly closed.

## Cross-build consistency vs PR #35 (Build A at 2ea67d0)

**Result: BYTE-IDENTICAL across all three inlined sections.**

| Section | Build A lines | Build B lines | Diff |
|---------|--------------|---------------|------|
| §Buckets blockquote (Step 1: CLASSIFY THE HAND) | 404-438 | 640-674 | ZERO bytes differ |
| §Features blockquote (rows 1-54) | 453-510 | 691-748 | ZERO bytes differ |
| §DO NOT Rules blockquote (Rules 1-10 + preamble) | 546-603 | 784-841 | ZERO bytes differ |

Both pilots inline from the same v3.1 master HEAD source, and the
inlined byte-streams match exactly. V-X1 cross-build framing
satisfied.

## Findings summary

| ID | Severity | Description | Location |
|----|----------|-------------|----------|
| F1 | NIT (carried, not blocking) | Body line 1563 §Anti-patterns intro carries "DO NOT Rules 1-11" from design-artifact source verbatim. Source is `prompts/protocol_c_adversarial_elimination_v1_0.md` @ master `c4f29a5` line 1299. Out of scope for orchestrator's frontmatter-only NIT-cleanup directive. Already raised by builder-reviewer 294a61c. | `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md:1563` |

No HIGH, MEDIUM, or LOW findings. No verbatim-inlining errors. No
spec-vs-code drift. No cross-build divergence.

## Recommendation

**Merge as-is.**

Rationale:
1. All three verbatim-inlined sections are byte-perfect against v3.1
   master HEAD `c4f29a5`.
2. Feature contract names 55-59 match `feature_extractor.py`
   `FEATURE_COLUMNS` exactly at master HEAD.
3. Build A NIT-1 + NIT-2 are pre-empted exactly as PR description
   claims, in the scope orchestrator declared (frontmatter + provenance
   + section meta).
4. Cross-build (Build A vs Build B) inlined-content blocks are
   byte-identical — V-X1 satisfied.
5. The single residual NIT at body line 1563 is design-artifact
   source content not requested for cleanup, and tracking it in this
   pilot would imply edit-divergence from the design artifact.
   Best resolution path: address it in a future v3.2 / v1.0.2 cycle
   that sweeps "Rules 1-11" → "Rules 1-10" across the design
   artifact (and consequently Protocol B's design + pilot anti-pattern
   intros, which will carry the same source-line drift). Out of scope
   for PR #37.

Pilot dispatch prerequisite row #6 GREEN from a V3-compliance
perspective.

---

*Review performed via diff against staged blobs from master `c4f29a5`
(source) and PR head `2a597b4` (artifact under review) and Build A
merge `2ea67d0` (cross-build comparator). No PR description trust;
all claims verified against actual file contents.*
