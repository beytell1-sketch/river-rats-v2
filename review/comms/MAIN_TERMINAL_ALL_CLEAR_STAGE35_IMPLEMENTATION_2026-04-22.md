---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: ALL-CLEAR on Stage 3.5 cumulative (v2 + v2.2 + v2.3 + v2.3.1) — implementation authorised
status: ALL-CLEAR — implementation begins per the 16-commit sequence; quality default applies per commit
---

# Stage 3.5 — ALL-CLEAR

Orchestrator read-check on v2.3.1 patch (commit `98f6d40`) complete.
**Implementation authorised.**

## Read-check results (verified against origin/master)

Cumulative artifact: 4 documents totaling ~4500 lines across blueprint
v2 + v2.2 amended + v2.3 amended + v2.3.1 patch. Plus CONTENT_API v4
ticket.

### CRITICAL — all 3 addressed cleanly

**MUST #60 — multiway aggregation spec bugs:** Both Q39 chain_steps
+ MED-A surviving_weight replacement expressions land correctly.
`per_villain_chain_steps: Dict[str, List[str]]` tracked in loop;
flat-aggregates as `f'{opp}:{step}'`. `surviving_weight = min(m.get(...) for m in per_villain_metas.values())` captures tightest
narrowing. MED-B v2.2 §3.7 BEFORE deletion added to commit 4 todo.

**MUST #61 — physical SUPERSEDED markers:** Verified on origin via
`git show origin/master:<path>`:
- `BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md` line 942 ✓ (post-NotImplementedError)
- `BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md` line 1728 ✓ (commit-sequence table, stale "13" count)
- `BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md` line 680 ✓ (multiway sketch header)

All markers include cross-reference to v2.3 + v2.3.1 with explicit
"do not implement from this section" guidance.

**MUST #62 — true case-insensitive helper:** `_canonicalize_attention_value`
function uses `val.strip().upper()` for string comparison; handles
int/float/bool/str/None with typed branches; raises RuntimeError on
unrecognised values (loud fail, not silent-miss). Mixed-schema reject
only on BOTH non-empty dicts (empty-dict migration artifact allowed
per pass #3 finding).

### HIGH — all 4 addressed cleanly

**MUST #63** cache contract: LOCAL to `extract_all_features(hand)`;
assertion on mismatched (cached_range, cached_meta) pair; garbage-
collected at function exit; no module-level state.

**MUST #64** merged-range deprecation: Helper returns `(None, meta)`
for multiway. Callers consume `per_villain_ranges` directly.
`_per_villain_composition` in metadata for teaching layer. Step 12/17
multiway blocker features = primary-villain-only until v2.5.

**MUST #65** HELD_BACK_FEATURES from gto_model SOT: Exported from
gto_model.py; assembler + trainer import rather than hardcode. Stage 5
un-hold flips the frozenset; all consumers pick up automatically.

**MUST #66** stratified 10% sampling: Across 8 shape categories from
MUST #49; ≥1 sample per shape (Cochran 1977 grounded).

### MEDIUM — 1 acceptable deferral

**MUST #67** benchmark stratify by num_opponents: DEFERRED per
orchestrator directive allowance; v2.5+ ticket tracked.

### Q-resolutions applied

- Q39: applied in MUST #60(a) ✓
- Q40: tri-state binarisation audit log at trainer (commit 11B) ✓
- Q41: KB §1.11 footnote on 0.15 asymmetric vs solver ✓

### Stage 3 forward note

v3.2 prompt PRIMARY/CONFIRMED vocabulary definition tracked as Stage 3
deliverable prerequisite. Manifest v1.11 note to add when Stage 3.5
ships. Not Stage 3.5 scope.

## Minor follow-up (non-blocking)

v2.3 file (`BUILDER_V24_STAGE35_BLUEPRINT_V2_3_AMENDED_2026-04-22.md`)
at lines 357-365 still contains the original broken spec
(`per_villain_truncated` dict-iteration + `min(dict.values())` bool
return) that v2.3.1 supersedes textually. For full-trail consistency
with v2 + v2.2 markers, a mirror SUPERSEDED marker on v2.3 §2.2 would
be nice. **NOT ship-blocking** — v2.3.1 is the latest spec; readers
following the chronological amendment chain land correctly.

Builder may land the v2.3 marker in a small follow-up commit or skip
it. Implementation can begin in either case.

## What happens now — implementation sequence

Per the 16-commit plan (14 main + 2 sub = 11A/11B):

| # | Commit | Source |
|---|--------|--------|
| 1 | HIGH #5 + #13: narrow_* return mass; cumulative surviving_weight; floor 10%/WARN 20% | v2 §2.1 + v2.3 |
| 2 | CRIT #2 + MUST #9: strict `_action_history` gate + pipeline unswallow + `_action_history_present` audit column | v2 §2.2 + v2.3 |
| 3 | HIGH #3 + MUSTs #11 + #12: same-street sequence collapse pre-filter | v2 §2.3 + v2.3 |
| **4** | **ATOMIC MERGE** CRIT #1 + HIGH #4 + MUSTs #6 + #10 + #15 + #19 + #28 + #30 + #34 + #46 + #52 + chain consumer + NaN sentinels + equity inheritance + merged-range deprecation + multiway cache contract | v2 §2.4/2.5 + §3.1 + v2.2 §3.7 + v2.3 §2.2 + v2.3.1 §M60/63/64 |
| 5 | MUST #20: `calibration_exam.py` `_action_history` plumbing | v2.2 §5 |
| 6 | MUST #22: `reference_evaluator.py` `_action_history` plumbing | v2.2 §5 |
| 7 | MUST #23: `train_sizing_model.py` verification + plumb OR bypass-with-audit | v2.2 §5 |
| 8 | MUST #8 partial: delete `coaching/feature_extractor.py` + `coaching/range_narrowing.py` | v2 §3.3 |
| 9 | MUSTs #17 + #38 + #39 + #40 + #50 + Q41 footnote: freq table atomic coherence (check=0.85/bet=0.15 + bluff/air reciprocals) + KB §1.11 asymmetric threshold + combo-draw max addendum + KB §1.11 footnote | v2 + v2.2 + v2.3 + v2.3.1 |
| 10 | MUST #41: belt-and-braces count guard (audit-only non-truncating) | v2.2 §5 |
| 11 | MUST #17 only frequency edit if separate from §9 | v2 §3.5 |
| 11A | MUST #26 + #29 + #44 + #45 + #62 + #65: assembler strict + bi-schema helper + tri-state CSV + HELD_BACK SOT | v2.1 + v2.3 + v2.3.1 |
| 11B | MUST #27 + #36 + #40 Q40: trainer dynamic vocab + CSV-header reconciliation + binarisation audit log | v2.1 + v2.3 + v2.3.1 |
| 12 | Corpus: 81-case pytest consumer + 4 coverage-gap additions + MUST #18 + #33 + #51 reauthoring (T_J01, T_B05, T_J02) | v2 §7 + v2.2 §3 |
| 13 | MUST #35 + #54 + #66 sidecar authoring: Path (c) Phase 2 structured authoring + validator + stratified solver-verify | v2.2 §5 + v2.3.1 §3.4 |
| 14 | M4 re-audit: blocker-bypass + NaN + mass + equity-shift + MUST #6 distribution | v2 §8 |
| 15 | M5 re-run: 3/3 anchors + MUST #16 regression guard | v2 §9 |
| 16 | SHIP: audit report + manifest bump + Stage 3.5 landed | v2 §16 |

## Ship gates between commits

Per CLAUDE.md discipline + quality default:

- **Per-commit reviewer pass.** Orchestrator spawns a single reviewer
  (architecture default; GTO for commits 9/12; red-team for commit
  4 merge) per commit. Not full 5-panel.
- **Commit 4 merge review: 2 reviewers.** Architecture + red-team in
  parallel given the 11-MUST scope. Single reconciliation step if
  both approve; otherwise fix-forward.
- **STOP conditions.** Per CLAUDE.md §5. Any file/line mismatch,
  unexpected test failure, audit output contradiction → STOP + report.
- **Owner approval gate between commit 6 and commit 13.** After code
  commits (1-12) land, owner reviews:
  - Dry-run sidecar batch (8-entry shape-targeted per MUST #49)
  - Validator script exit-0 proof
  - M4 re-audit distribution report preview
  - T_J01/T_J02/T_B05 verdict-flip proof (MUST #33 + #37)
  Then owner go/no-go on sidecar authoring lift (commit 13).

## Active MUSTs at implementation start: 65

(57 from prior reconciliations + 8 new from v2.3.1; inactive #24, #25.)

## Discipline reaffirmed

- GitHub is project state (`git show origin/master:<path>`)
- DECIDE and EXECUTE within ranges; document choices
- Quality default (slow/clean over fast/loose)
- Push back on unclear; answer to "is it OK to ask" is always YES
- One MUST per commit (except commits 4, 9 explicitly merged)
- Per-commit reviewer pass between each

## Trajectory recap

| Pass | New MUSTs | Scope class |
|------|-----------|-------------|
| 1 | 14 | Whole-MUST-class gaps (equity bypass, §1.10 misname, coaching duplicate, commit-order poisoning) |
| 2 | 16 | Scope expansions + redesigns |
| 3 | 15 | Concrete code bugs + caller-list drift |
| 4 | 8 | Spec text typos + placeholder fixes |

Pattern converged. Implementation begins.

## Immediate builder action

Auto mode. Begin commit 1 without further orchestrator input:

1. Source-verify commit 1 BEFORE blocks at HEAD 98f6d40 (paranoia
   discipline — drift check one last time)
2. Implement commit 1 per v2 §2.1 + v2.3 supplements
3. Run tests; all green
4. Push commit 1
5. Ping orchestrator for single-reviewer pass on commit 1
6. After approval, commit 2

Continue through the 16-commit sequence.

Stage 4 opens when:
- Stage 3.5 all 23 MUSTs + amendments land (commits 1-16)
- Audits clean (M4 + M5)
- Owner gate at commit 6→13 boundary passes
- Stage 3 v3.2 prompt ships (tracked separately)

Then Stage 4 re-label begins. Then Stage 5 retrain. Then Stage 6 ship
gate. Then v2.4 ships.

## Notes for future sessions

If new CRITICAL surfaces mid-implementation: STOP, report to
orchestrator, await directive. Don't improvise workarounds. The
review discipline that got us here is what prevents the next
v2.3.2-class silent failure.

Go.
