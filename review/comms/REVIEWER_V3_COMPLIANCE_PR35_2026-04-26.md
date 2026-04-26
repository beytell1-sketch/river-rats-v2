---
date: 2026-04-26
from: V3-compliance reviewer (orchestrator-dispatched)
to: Main terminal (orchestrator) · Logic builder · Owner (briefed)
re: PR #35 (Build A — Protocol B labeller-facing pilot v1.0.1-pilot) — V3-compliance content verification
status: APPROVE-WITH-NITS
---

# V3-Compliance Review — PR #35 (Build A)

## Verdict: APPROVE-WITH-NITS

Content fidelity to v3.1 source is **byte-perfect verbatim** in all
three inlined sections (§Buckets, §Features, §DO NOT Rules). Feature
names 55–59 match the canonical `feature_extractor.py` `FEATURE_COLUMNS`
at master `c4f29a5` exactly (no spec-vs-code drift). The 59-feature
contract is correctly enumerated. The only outstanding items are the
two NITs already raised by QC; no new HIGH/MEDIUM/LOW findings beyond
those.

Method: extracted `prompts/gto_labeller_v3.1.md` at master `c4f29a5`
and `prompts/protocol_b_composition_first_v1_0_pilot.md` at PR HEAD
`f95cdab`, ran `diff` on the cited line ranges (after stripping the
markdown blockquote `> ` prefix from the pilot). Three diffs all
clean. Then cross-checked feature names against the canonical
`river-rats-core/feature_extractor.py` at master `c4f29a5`.

---

## §Buckets (v3.1 lines 170–204)

**Diff result: CLEAN — byte-perfect verbatim.**

Pilot lines 404–438 (with `> ` blockquote prefix stripped) are
byte-identical to v3.1 master lines 170–204:

- Six bucket headers verbatim: Monster · Strong made · Medium made ·
  Weak made · Drawing · Air
- All six worked examples verbatim (8h8c on 8d 5s 2c, AhKd on Ad 9c
  3h, KhJd on Kc 8s 5d, 5h4h on Kc 8s 5d, Th9h on 7h 6h 2c, Qc Jd on
  8s 5d 2c)
- Closing line `**State the bucket explicitly:** "This is a [bucket]
  hand."` verbatim
- "Use poker reasoning, not numeric thresholds." verbatim — preserves
  the bucket-first-labelling rule from
  `feedback_bucket_first_labelling.md`

No findings.

---

## §Features (v3.1 lines 439–496 + v2.4 P1 blockers)

**Diff result on lines 439–496: CLEAN — byte-perfect verbatim.**

Pilot lines 453–510 (with blockquote prefix stripped) are byte-
identical to v3.1 master lines 439–496. All 54 rows of the feature
table match: feature numbers, backtick-wrapped names, and free-text
descriptions including pipe-table formatting.

### 59-feature contract enumeration

Pilot enumerates:

- Features 1–54: verbatim from v3.1 lines 439–496 (54 raw)
- Feature 55: `board_adjusted_hrp` (per Stage 5 un-hold; held back
  per Stage 3.5 manifest)
- Features 56–59: v2.4 P1 blocker features
  - 56: `nut_flush_block`
  - 57: `flush_draw_block_pct`
  - 58: `straight_draw_block_pct`
  - 59: `nut_made_block_pct`

Total: **54 + 1 + 4 = 59 raw**, matching Stage 5 retrain v1.0.1
§Hyperparameters point #4 ("55 raw + 4 v2.4 blocker = 59 raw").

### Feature-name vs. feature_extractor.py at master HEAD (spec-vs-code drift check)

Verified `river-rats-core/feature_extractor.py` `FEATURE_COLUMNS` at
master `c4f29a5` (file lines 1605–1612):

```
'board_adjusted_hrp',          # feature 55
'nut_flush_block',              # feature 56
'flush_draw_block_pct',         # feature 57
'straight_draw_block_pct',      # feature 58
'nut_made_block_pct',           # feature 59
```

Pilot artifact lines 514, 527–530 cite the **identical names**.
`len(FEATURE_COLUMNS)` confirmed = 59 via direct import at master
`c4f29a5`. **No spec-vs-code drift.**

This passes the HIGH-severity check from
`feedback_spec_vs_infrastructure_code_drift.md` (rule fired twice
already today; pilot artifact is clean of EXISTENCE drift and
CONTENT drift).

No findings.

---

## §DO NOT Rules (v3.1 lines 590–647)

**Diff result: CLEAN — byte-perfect verbatim for all 10 Rules.**

Pilot lines 546–603 (with blockquote prefix stripped) are byte-
identical to v3.1 master lines 590–647. Each Rule verified
individually:

- Rule 1 (decide based on equity alone) — verbatim
- Rule 2 (barrel draws into 2 opponents; 3-way fold equity ~36%) —
  verbatim
- Rule 3 (assume the checking player has nothing) — verbatim
- Rule 4 (auto-c-bet IP just because you have position; 30–45%) —
  verbatim
- Rule 5 (treat top pair as a strong hand; TPTK check-behind OOP) —
  verbatim
- Rule 6 (overweight blockers; ~40% less 3-way) — verbatim
- Rule 7 (analyze streets in isolation; SPR ~1.5 turn forward
  thinking) — verbatim
- Rule 8 (assume both opponents have equivalent ranges; cold-caller
  capped, BB wide) — verbatim
- Rule 9 (use `villain_range_capped` as a postflop strength signal;
  composition quad reference) — verbatim
- Rule 10 (`hero_range_percentile = 0.00` HRP_INVESTIGATION_2026-04-15
  test-harness artifact note) — verbatim, including the `[v3 addition
  §3.B]` tag and the file reference

No findings.

---

## Findings summary

| ID | Severity | Description | Location |
|----|----------|-------------|----------|
| (none) | — | No HIGH / MEDIUM / LOW content-fidelity findings. All three sections diff-clean against v3.1 master `c4f29a5`. Feature names 55–59 match `feature_extractor.py` master HEAD verbatim. | — |
| QC NIT-1 | NIT | Frontmatter cites DO NOT lines as `590-647` (Build A) vs. body's `595-647` (matches actual rule content start). Pilot artifact line 605–609 acknowledges the discrepancy in the parenthetical. Already known. | pilot lines 14, 24, 50, 540 vs 605 |
| QC NIT-2 | NIT | Build provenance describes DO NOT block as "Rules 1-11" while the verbatim block contains 10 numbered rules (item 11 was subsumed into Rule 10). Already explicitly acknowledged in pilot lines 605–609. Already known. | pilot line 24 vs 546–603 |

No new findings beyond QC's pre-merge audit.

### Cross-stream consistency check (informational)

Pilot lines 532–536 quote Stage 5 retrain protocol §Hyperparameters
point #4 as `"55-feature vector + 4 v2.4 blocker features = 59 raw
features"`. Stage 5 doc at master `c4f29a5` actually phrases it as
`"118-column v2.4 contract (55 raw + 4 v2.4 blocker = 59 raw + 59
attn_*)"`. The arithmetic and the contract are identical (59 raw);
the pilot's quotation is a paraphrase, not a verbatim block, and is
not flagged as such — clearly informational ("Cross-stream check:
matches"). **Not a finding.**

---

## Recommendation

**Merge as-is OR merge after QC NIT cleanup — orchestrator's call.**

From a content-fidelity perspective, this PR is ready to merge.
Build A faithfully verbatim-inlines the cited v3.1 source ranges and
correctly enumerates the 59-feature contract using the canonical
feature names from `feature_extractor.py` at master HEAD. There is no
spec-vs-code drift, no semantic rewording, and no content drift
beyond the two cosmetic NITs QC already raised (line-range and
"Rules 1-11"-vs-"1-10" labels in frontmatter / provenance — both of
which are explicitly acknowledged inside the artifact body itself).

If orchestrator wants belt-and-braces, NIT cleanup is a 2-line edit
to the frontmatter and the build_provenance block; otherwise the
artifact is functionally and semantically correct and the labeller
AI agent will read the verbatim-inlined v3.1 content faithfully.

**Pilot dispatch unblocked from V3-compliance perspective.**
