---
date: 2026-04-26
from: A.8 teaching-stream archaeology agent (orchestrator-dispatched)
to: Main terminal (orchestrator) · Owner · Pilot Orchestrator
re: Root-cause analysis on owner-observed range-reasoning inconsistency in teaching messages
status: AUDIT
verdict: TEACHING_FIX_ONLY (root cause = bad teaching prompts / renderer-side label conflation; training-data fields are sound, so Phase B mass labelling is NOT structurally blocked)
---

# A.8 — Teaching-Stream Archaeology

## Verdict: TEACHING_FIX_ONLY — Phase B is NOT blocked by this finding.

The owner-observed range inconsistency is rooted in the **teaching renderer
and prompt-templating layer**, not in the labelled training fields. The
underlying logic features (`hero_range_percentile`, `worse_hand_pct`,
`better_hand_pct`, `villain_top_pair_plus_pct`, etc.) are computed
correctly in `~/river-rats-v2/river-rats-core/feature_extractor.py` and
recorded faithfully in the training jsonl. The inconsistency lives in
how the renderer translates those numbers into English — specifically,
it conflates four distinct range concepts into one sentence template
and uses a preflop-native metric (HRP) postflop where the teaching repo's
own research explicitly says it should not.

**Phase B can proceed.** Two caveats below in `Recommendation`.

## T1 — Files + sources surveyed

Repo: `~/river-rats-teaching/` (102 commits, earliest `9790839 Scaffold`,
HEAD `f0dffb5 PR #1 MERGED`). Time range covered: 2026-04-09 → 2026-04-26.

Investigated:
- `~/river-rats-teaching/CLAUDE.md` — project charter (logic vs teaching
  separation, 5-level model)
- `~/river-rats-teaching/interface/l3_renderer.py` — the v1 (older) range
  context renderer
- `~/river-rats-teaching/interface/l3_renderer_enriched.py` — current
  (post-`1dab76e` Phase 2) renderer
- `~/river-rats-teaching/interface/agent_student_test.py` — student
  prompt builder (training-prompt format)
- `~/river-rats-teaching/content/architect_framework_review.md` —
  architect's own audit of the renderer
- `~/river-rats-teaching/content/data_availability_audit.md` — data-side
  audit, includes acknowledgement of conflation
- `~/river-rats-teaching/content/gold_standards.md` — "ground truth"
  reference outputs (Phase 1.4 creative lead)
- `~/river-rats-teaching/review/research/PRO_RANGE_ANALYSIS_PREFLOP_VS_POSTFLOP.md`
  — research doc establishing the rule HRP = preflop-native, postflop
  uses hand categories
- `~/river-rats-teaching/review/gto_review/GTO_EXPERT_REVIEW_2026-04-16.md`
  — independent GTO reviewer's verdicts on 10 outputs
- `~/river-rats-teaching/review/phase2/sample/*.html` (25 hands) — rendered
  teaching outputs scored in Phase 2
- `~/river-rats-teaching/review/hardening/sample/*.html` (~50 hands) —
  rendered teaching outputs from L3 hardening pass
- `~/river-rats-teaching/review/agent_student/full_50_prompts.json` (50
  prompts) — prompts shown to model in agent-as-student playtest
- `~/river-rats-teaching/data/v2_2_enriched.jsonl`,
  `agent_student_50.jsonl`, `phase2_sample.jsonl`, `hardening_sample.jsonl`,
  `adversarial_sample.jsonl` — training-data jsonl
- `~/river-rats-teaching/review/teaching_v2_review.html` — Phase 2 v2
  range-first layout
- `~/river-rats-teaching/review/framework_test_v*.html` — earliest
  prototypes (April 13)

Methodology: surveyed git log; greppped for `range`, `percentile`,
`HRP`, `capped`, `polari[sz]ed`, `top of range`, `bottom of range`
across renderer source, training prompts, rendered HTML outputs,
gold standards, and reviewer comments. Cross-referenced with the
underlying logic-side feature definition in
`~/river-rats-v2/river-rats-core/feature_extractor.py:2266`
(`compute_hero_range_percentile`).

## T2 — Inconsistencies identified

The renderer / prompt layer commits **five recurring range-concept
conflations**:

1. **HRP-vs-hand-bucket label clash.** Postflop training prompts and
   teaching outputs lead with "At the X percentile of our range" + an
   English label ("top of the range" / "middle of the range" /
   "near the bottom"). The label is computed from `hero_range_percentile`
   (a preflop-opening-range-on-board percentile) yet it is presented as
   if it tells the student something about postflop hand strength. This
   produces literal contradictions: e.g. "We hold **air**. At the **51st
   percentile** of our range" (BP4_24, BP4_21) and "We hold a
   **medium-strength made hand** at the **75th percentile** … FOLD"
   (BP2_11). Not a metric bug — a teaching-label bug. The teaching repo's
   own research doc
   (`review/research/PRO_RANGE_ANALYSIS_PREFLOP_VS_POSTFLOP.md`) says
   explicitly: "Postflop, replace HRP with hand category." The renderer
   was migrated only halfway: the new
   `_range_position_desc()` (l3_renderer_enriched.py L346–401, from
   commit `0e75102 Structural fix: board-relative hand strength replaces
   HRP-led framing`) leads with hand category but the **prompts in
   `full_50_prompts.json` (the training corpus shipped to the agent
   student playtest 2026-04-18, commit `ab8d172`) still lead with
   `RANGE POSITION: At the X percentile … middle of the range`.**

2. **"Hero's range position" sentence carries villain-range numbers.**
   `l3_renderer.py:368-371` (and the gold-standard mirror) produces:
   `"This hand sits {top|upper|lower|bottom} of hero's range here ({worse}% of villain's range is worse, {better}% is better)."`
   The lead clause refers to hero's own range; the parenthetical reports
   `worse_hand_pct` / `better_hand_pct` which are fractions of
   **villain's** range. These are not equivalent. `data_availability_audit.md:78`
   admits the bug verbatim: "`worse_hand_pct` measures position vs
   villain's range, not hero's own range." The same conflation appears
   in `gold_standards.md` (Hand 2: "This hand sits near the top of the
   BB continuing range here (91% of villain's range is worse)") — i.e.,
   the supposedly-canonical reference outputs replicate the bug.

3. **Position bar visual axis vs underlying number.**
   `~/river-rats-teaching/review/teaching_v2_review.html` renders a bar
   labelled `weak in range ↔ strong in range` (a hero-range axis), with
   a marker positioned by `worse_hand_pct` (a vs-villain quantity). The
   visual label tells the student they are reading their position in
   their own range; the underlying number tells the student what
   fraction of villain's range they beat. The student sees one frame,
   the data is from a different frame. Earliest prototype
   (`review/framework_test_hand.html`) carries the same conflation:
   "lower half of the continuing range — 66% of villain's range is
   currently ahead."

4. **"Capped at SPR" — a range concept glued to a stack-geometry
   concept.** Six rendered hands (`BP2_11`, `BP4_06`, `BP4_09`, `BP4_10`,
   `BP2_41`, `BP7_06`) carry sentences like "Villain checked back on an
   earlier street — the river range is **capped at SPR 0.6**." "Capped"
   is a range property (top of range removed); SPR is a stack-to-pot
   ratio. The two concepts are joined by the word "at" with no
   intervening clause, suggesting the cap is somehow a function of SPR.
   It is not. In `BP4_09` the rendered villain composition is 33%/33%/33%
   (uniform) — a literally not-capped range — yet the sentence still
   says "capped." The renderer is concatenating two flag fields without
   reasoning about whether the underlying claim holds.

5. **Action-suffix hardcoded to range-construction labels regardless of
   hand category.** `l3_renderer.py:300-309` (now patched in the enriched
   renderer per commit `5dd9c77 delete _blocker_desc + register
   directional-framing guard` and friends) used to append fixed range
   sentences for every action: `CALL → "calling keeps strong hands in
   range for later streets"`, `RAISE → "raising polarizes the range to
   strong hands and bluffs"`, etc. These were emitted with no check on
   whether hero actually has a strong hand. The classic bug, called out
   in `architect_framework_review.md:122-130`: hero AdKd with nut flush
   draw on a paired Jh-board outputs "calling keeps strong hands in
   range" — hero has no made hand, so there are no strong hands in
   range. Fixed in the enriched renderer; older training prompts still
   carry it.

Additional non-range surface bugs spotted in the same files (logged
because they correlate with the same teaching-stream lineage but are
out of scope for this audit's verdict):

- Broken ordinal suffixes: `33th`, `51th`, `66th`, `76th`, `81th`,
  `88th`, `91th`, `92th`, `93th`, `95th` percentile across
  `phase2/sample/*.html` (already partially fixed in commit
  `a1aeaa0 Fix D1+D7: ordinal suffix`).
- Header/body mismatch on intention labels (`deny_equity` for CALL,
  `pot_control` for BET) — flagged by GTO reviewer's "Systemic issue
  #1: Intention-header mismatch" (5 of 10 hands flagged).

## T3 — Root-cause synthesis

The owner's observation maps cleanly to **(b) bad teaching prompts /
renderer**, with weak secondary contributions from labels and zero
contribution from model behaviour visible in this audit's evidence
window.

**Why not (a) bad training labels:**
The structured training fields (`hero_range_percentile`,
`worse_hand_pct`, `better_hand_pct`, `villain_top_pair_plus_pct`, etc.)
are scalar features with single, clear logic-side definitions
(`feature_extractor.py:2266`). Sampled `data/v2_2_enriched.jsonl` rows:
the structured fields are internally consistent (e.g. BP1_01:
`worse_hand_pct=0.32`, `better_hand_pct=0.68`, sum = 1.00, hand_bucket
= "drawing", consistent with a flush draw that beats 32% of villain
combos). The `reasoning_by_team` text fields T1–T4 use range concepts
correctly throughout the spot-checked sample (proper labels
"semi-bluff", "value range", "polar range", "capped"). No evidence the
labelled team-reasoning conflates ranges in a way that would corrupt
mass labelling.

**Why (b) bad teaching prompts / renderer:**
Three independent in-repo audits (`architect_framework_review.md`,
`data_availability_audit.md` §1c, `GTO_EXPERT_REVIEW_2026-04-16.md`
"Systemic issue #3") plus a research doc
(`PRO_RANGE_ANALYSIS_PREFLOP_VS_POSTFLOP.md`) all converge on the
same locus: the renderer collapses distinct range concepts into a
single sentence template. The bug-trail is the renderer
(`interface/l3_renderer.py`) and its ancillary outputs
(`gold_standards.md`, `teaching_v2_review.html`,
`agent_student/full_50_prompts.json`), not the training data. The
enriched renderer (commits `0e75102` and `1dab76e` onwards) has begun
remediation; it has not yet flowed back to the agent-student playtest
prompt format, which still carries the old labels.

**Why not (c) model behaviour:**
This audit didn't observe model outputs that diverge from the prompt
they were given. The agent-student prompt at BP1_01 is unambiguous about
HRP=60th and the model's consensus action was RAISE — the model did the
right thing for the wrong narrative reason, but that's a pedagogy
failure, not a model-disagreement failure. Phase B is meant to fix the
training-data side; this finding is renderer-side and orthogonal.

## T4 — Top 5 representative examples

### Example 1 — air at the 51st percentile (HRP-vs-bucket clash)
- Quote: `"<strong>Hero:</strong> CO · We hold **air**. At the **51st percentile** of our range."` (then headline action: CHECK)
- File: `~/river-rats-teaching/review/phase2/sample/hand_BP4_24.html:119`
  + mirror in `hand_BP4_21.html:119` (BTN, air, 51st, CHECK)
- Source: `interface/l3_renderer_enriched.py:761`
  (`where_we_sit_pct = round(hrp * 100, 1)`) + the older
  `where_we_sit_desc` template `f"At the {where_we_sit_pct:.0f}th
  percentile of our range."` (commit `1dab76e`).
- Root-cause hypothesis: **(b) renderer**. HRP is correctly computed
  (it represents preflop hand-rank conditioned on board), but the
  English label "51st percentile of our range" reads as a hand-strength
  claim postflop. Air can be at 51st HRP because HRP measures preflop
  rank conditioned on board — not postflop strength. Research doc says
  "do not show HRP postflop". Renderer was migrated only in the
  rendered-HTML path; the agent-student prompt path still emits it.
- Phase B implication: not blocking. The training-data record itself
  contains `hand_bucket="air"` and the equity scalar — both correct.
  Mass labelling will still produce sound team-reasoning. The
  renderer-side fix is a prompt-template change downstream of labelling.

### Example 2 — "hero's range" sentence built from villain-range numbers
- Quote: `"This hand sits near the top of the BB continuing range here (91% of villain's range is worse); hands that beat hero — AJ, KJ, sets of 2s and 5s — represent 8% of villain combos…"`
- File: `~/river-rats-teaching/content/gold_standards.md:100-104`
  (Hand 2, d8886). Implementation source: `interface/l3_renderer.py:368-371`.
- Root-cause hypothesis: **(b) renderer + (a-light) gold standards.**
  The renderer template is structurally wrong (it labels a vs-villain
  quantity as a hero-range position). The same wrong frame is baked
  into the gold-standard reference outputs that the Phase 2 scorer
  measures against — meaning even passing scoring runs do not detect
  the bug. The data-availability-audit (`§1c, line 78`) already flags
  this as a known proxy: "`worse_hand_pct` measures position vs
  villain's range, not hero's own range. This is a reliable proxy but
  technically describes 'what I beat' not 'where I sit in my full
  opening range.'"
- Phase B implication: not blocking, but the gold-standards file
  needs a follow-up fix-forward; otherwise post-pilot scoring will
  reward the wrong frame.

### Example 3 — "Range capped at SPR" (range-property ⊕ stack-geometry)
- Quote: `"Villain checked back on an earlier street — the river range is capped at SPR 0.6. Facing a bet (33%-pot small) at SPR 0.6 from BB's perspective — villain range is 71% TP+."`
- File: `~/river-rats-teaching/review/phase2/sample/hand_BP2_11.html:137`
  (also BP4_06, BP4_09, BP4_10, BP2_41, BP7_06).
- Counter-evidence in same set: `BP4_09` shows 33%/33%/33% TP+/Med/Air
  — that is **not a capped range** in any standard sense. The sentence
  fires anyway because the renderer simply concatenates
  `villain_checked_back == 1` with the SPR scalar.
- Root-cause hypothesis: **(b) renderer**. The "capped" label is
  triggered by a binary flag (`villain_checked_back`) without checking
  whether the composition actually supports the claim, and the SPR
  glue word makes the sentence read as if SPR causes the cap. The
  enriched renderer comment block (`l3_renderer_enriched.py:425-427`,
  `V3 scrub: em-dash editorialising clauses removed ("— a range
  weighted toward value", "— the range is capped", etc.)`) acknowledges
  this and removes the editorialising clauses from the new path. Older
  outputs still carry it.
- Phase B implication: not blocking. The underlying flag + composition
  fields are correct; only the prose template is wrong.

### Example 4 — action-suffix hardcoded across hand categories
- Quote: `"Hero's BB range is wide and often capped after flatting … calling keeps strong hands in range for later streets."` (rendered for hero AdKd / nut flush draw / no made hand)
- File: `interface/l3_renderer.py:289-307`. Bug doc:
  `content/architect_framework_review.md:122-130`.
- Quote (architect): `"Hand d4211 (AdKd calling with a nut flush draw)
  outputs 'calling keeps strong hands in range for later streets.'
  Hero has zero made hand — there are no strong hands in range."`
- Root-cause hypothesis: **(b) renderer**. Action-keyed string
  constants (CALL → "keeps strong hands in range", RAISE → "polarizes
  the range") are appended without reading `hand_bucket` /
  `is_made_hand`. Already scheduled to be fixed in the enriched
  renderer Path B work (commits `bb362ad`, `a7e63a2`, `c6dff6a`).
- Phase B implication: not blocking. Range-construction sentences
  here are renderer-side text generation; they do not enter the
  training corpus.

### Example 5 — range-frequency reasoning at hand level (L5 misapplied at L3)
- Quote: `"the 24%-made density turns hero's range into a losing caller as a whole … hero's range-position forces a disciplined fold rather than a spot-specific call."`
- File: `~/river-rats-teaching/review/phase2/sample/hand_BP1_25.html`,
  scored in `gto_review/GTO_EXPERT_REVIEW_2026-04-16.md:55-60`.
- Reviewer verdict: `"At L3, the student needs to understand WHY this
  specific hand folds, not just that 'the range folds.' The range-
  frequency argument is an L5 concept being misapplied at the hand
  level."` Cited as `Systemic issue #3`.
- Root-cause hypothesis: **(b) renderer + curriculum-tagging.** The
  range-construction reasoning is fired by the SHAP-driven Why builder
  in `build_why()` regardless of `PlayerLevel`. Per the project's own
  `CLAUDE.md` rule "Tag everything by level. A learner at L2 should
  never see L4 concepts without scaffolding," this fires L5 reasoning
  at L3. Not a label problem — a level-gating problem in the renderer.
- Phase B implication: not blocking. Curriculum-level gating is
  rendering-time logic; it does not affect what the labellers produce
  in mass labelling.

## Findings summary

| ID | Severity | Type | Description |
|----|----------|------|-------------|
| A8-1 | HIGH | (b) renderer/prompt | HRP postflop label clashes with hand bucket — "air at 51st percentile of our range" type contradictions; persists in `agent_student/full_50_prompts.json` despite enriched-renderer fix |
| A8-2 | HIGH | (b) renderer + (a-light) gold standards | "Hero's range position" sentence carries `worse_hand_pct` numbers (a villain-range fraction). Bug is replicated in the gold-standard reference. Documented as known proxy in `data_availability_audit.md:78` but never fixed |
| A8-3 | MED  | (b) renderer | "Range capped at SPR" — concatenates a range concept and a stack-geometry concept; fires even when composition is uniform/uncapped |
| A8-4 | MED  | (b) renderer | Action-keyed range-construction string constants emitted without reading `hand_bucket` ("calling keeps strong hands in range" for nut-flush-draw caller). Partly remediated in enriched renderer |
| A8-5 | MED  | (b) renderer + level-gating | L5 range-frequency reasoning ("range is a losing caller as a whole") fired at L3; per CLAUDE.md anti-pattern. Flagged by GTO reviewer |
| A8-6 | LOW  | (b) renderer | Position bar in `teaching_v2_review.html` labelled `weak in range ↔ strong in range` with marker placed by `worse_hand_pct` (different frame) |
| A8-7 | LOW  | cosmetic | Broken ordinal suffixes (`33th`, `76th`, `91th`) in rendered HTML — partially patched in commit `a1aeaa0` |

## Recommendation

**TEACHING_FIX_ONLY → Phase B mass labelling can proceed.**

Rationale: the inconsistencies live in the prose layer
(renderer + prompt template + gold-standard reference text). The
underlying labelled training fields are correct, internally consistent,
and computed from auditable logic-side functions. Mass-labelling
produces structured fields plus team-reasoning text; the team-reasoning
text in the spot-checked sample uses range concepts correctly. Phase B
will not propagate these renderer bugs.

**Caveats / required follow-ups (not blocking, queued for fix-forward):**

1. **Renderer-side fix** (high-priority post-pilot): finish the
   migration started by commits `0e75102` / `1dab76e`. Specifically
   (a) regenerate
   `~/river-rats-teaching/review/agent_student/full_50_prompts.json`
   from the enriched renderer rather than the legacy renderer; (b) fix
   `_position_in_range_sentence()` to either say
   "Hero beats X% of villain's range" (truthful frame) or split into
   two sentences for the two distinct ranges; (c) gate the
   "range-capped" sentence on actual composition, not just
   `villain_checked_back`; (d) delete the SPR concatenation; (e) tag
   range-frequency reasoning as L5 and gate it.

2. **Gold-standards fix-forward** (medium): update
   `~/river-rats-teaching/content/gold_standards.md` Hand 2 / Hand 4 /
   any "{N}% of villain's range is worse" sentence to match the corrected
   frame. Otherwise the Phase 2 scorer rewards the wrong frame.

3. **Owner attention** (information): owner observed the inconsistency
   in "earlier" teaching messages — the audit confirms this and shows
   that earlier prototypes (April 13 framework_test_v* files) had the
   same conflation. The remediation has already started in the renderer
   (April 21 / enriched path) but has not flowed to all downstream
   surfaces (April 18 agent-student playtest prompts). This is a
   plumbing-completion task, not a redo.

4. **Phase B safety net**: when Phase B mass labelling runs, sanity-check
   a 5% sample to confirm the produced team-reasoning text does NOT
   exhibit conflations 1–5 above. The samples spot-checked here come
   back clean, but a larger sample is the cheap insurance.

No structural blocker for Phase B. Verdict TEACHING_FIX_ONLY stands.
