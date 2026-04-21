---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: Correction to MAIN_TERMINAL_ATTENTION_FLAG_GAP_2026-04-22.md (commit 8c4466c)
status: CORRECTION — supersedes prior ticket on overclaimed scope; retains real gaps
supersedes: review/comms/MAIN_TERMINAL_ATTENTION_FLAG_GAP_2026-04-22.md (8c4466c)
---

# Correction — Attention-Flag Gap Was Overclaimed

The prior ticket (`MAIN_TERMINAL_ATTENTION_FLAG_GAP_2026-04-22.md` at
8c4466c) framed the v2.4 attention-flag work as 4 missed CRITICAL
MUSTs. After actually reading project state on GitHub — KB
`knowledge/three_way_gto.md` §1.10-§1.12 + `BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md`
+ `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md` + the labelling
pipeline docs — the actual scope is smaller. Two of the four MUSTs
were wrong to claim as missed.

## What the prior ticket got wrong

### MUST #24 (KB §1.9 attention conventions) — RETRACTED

**Wrong on two counts:**

1. **The KB section is §1.10-§1.12, not §1.9.** §1.9 was untouched
   ("Preflop geometry vs postflop composition" since pre-v2.4).
   Builder explicitly avoided renumbering §1.9 because v3.1 prompt
   has hardcoded cross-references. v2.4 work added new sections
   §1.10 (Defensive Blocker Direction), §1.11 (Covering-triple
   framework + multi-signal resolution rule), §1.12 (DO NOT Rule 6
   expansion).

2. **KB §1.11 already covers PRIMARY-tagging rules for blockers.**
   Direct quote from origin/master:
   > "If `nut_made_block_pct − (flush_draw_block_pct + straight_draw_block_pct) / 2 > 0.15`, **net CALL lean**... do not tag blocker features as PRIMARY in this case."
   > "This rule is a labelling heuristic for panel feature-attention decisions."

   The labelling-heuristic / PRIMARY-tagging guidance for the new
   features is on GitHub at HEAD origin/master, GTO-reviewed
   (`GTO_REVIEW_V24_STAGE2_KB_1_10_2026-04-20.md`), all 6 modifications
   applied. Stage 2 is **COMPLETE** (`BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md`),
   not "in progress" as my ticket and manifest implied.

### MUST #25 (v3.2 prompt mandatory-tag rules) — REFRAMED

**Not a missed gap; this IS the Stage 3 plan.** Builder's Stage 2
complete doc explicitly stated Stage 3 will:

> "Adding feature_attention guidance per decision context (defender-side contexts tag blocker features PRIMARY; aggressor-side uses §1.7 + §1.10.1 semi-bluff pattern)"
> "Updating DO NOT Rule 6 to reflect the expanded §1.12 language"
> "Bumping prompt version to v3.2 (new file `gto_labeller_v3.2.md`)"

The mandatory-tag table update for new features is exactly what
Stage 3 is designed to produce. Reframing as: "Stage 3 deliverable
must include the mandatory-tag table extension; verify on Stage 3
review." Not a CRITICAL MUST blocking blueprint v2.

## What was real (retained)

### MUST #26 (training-CSV writer captures expanded attention) — REAL

`river-rats-core/assemble_pilot_data.py` and the training assembly
path that produces `pilot_20_attention.csv` (109 cols) writes 54
existing attention flags. v2.4 adds 4 raw blocker features. The
capture path needs:

- New attention-flag column definitions corresponding to the new
  blockers
- Capture from labellers' `key_factors` / `attention_levels` output
- Audit column `_attention_vocabulary_version` (e.g. "exp3_54flag" → "v2.4_NNflag")

Without this: even if labellers correctly tag the new blockers as
PRIMARY in their JSON output (per Stage 3's v3.2 prompt), the tags
are silently dropped at CSV write. v2.4 model trains without the
new attention signal.

**Status:** real gap. Stage 4 prereq.

### MUST #27 (trainer reads expanded vocabulary) — REAL

`river-rats-core/run_attention_experiments.py` was the Exp 3 mechanism
runner. Per `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md`,
Exp 3 trained on 108 features (54 raw + 54 attention). Hardcoded
counts exist per project history. v2.4 trainer must read column
counts from CSV header rather than hardcode.

**Status:** real gap. Stage 5 prereq.

### Vocabulary-version audit column — REAL

Subset of MUST #26. Captures which attention vocabulary was used
to label each row, so post-hoc audits can filter by vintage. Not
controversial; cheap to add at writer change.

## Net effect on blueprint v2

Builder's blueprint v2 (untracked draft, 1845 lines, NOT yet on
GitHub) lists 23 MUSTs. The corrected attention-flag scope adds
two MUSTs (writer + trainer) plus one audit column, not four. Net:
25 MUSTs in scope, not 27.

If builder integrates this correction before pushing blueprint v2,
the document stays clean. If builder pushes blueprint v2 first,
they amend with this correction in v2.1 or a follow-up commit.

## Discipline failure that produced the overclaim

I wrote the original attention-flag ticket without reading:
- KB §1.10-§1.12 on origin/master (would have shown PRIMARY
  guidance is already there)
- `BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md` (would have shown
  Stage 2 COMPLETE + Stage 3 plan includes prompt updates)
- `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md` (would have
  shown the actual mechanism + 108-feature precedent)
- `docs/LABELLING_PIPELINE.md` (would have shown the calibration
  exam + dispatch flow + the v2.4 equivalents I'd need to plumb)

Memory at `feedback_github_is_state_not_local.md` records the
verification rule going forward: GitHub `origin/master` is project
state, not the local working tree, and not assumed-current local
caches. Always git fetch + git log + git status + read source from
origin before writing tickets that assert what's missing.

## Action

- Builder: when integrating MUSTs #26 + #27 into blueprint v2, drop
  the wrongly-numbered #24 and reframe #25 as Stage 3 deliverable
  (not blueprint v2 scope).
- Orchestrator (this commit): correcting the manifest §1.9 → §1.10-§1.12
  references; marking Stage 2 status COMPLETE; adjusting the v2.4
  ship sequence comments.
- No retraction of the prior ticket on GitHub — superseded with this
  correction in the comms trail (per project convention).
