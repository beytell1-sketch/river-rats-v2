---
date: 2026-05-09
from: River Rats QC (standalone stream)
to: Main terminal (orchestrator) · Owner · LEAD-PROGRAMMER (architect-hat)
re: PR #307 rev 2 — Phase 1.5-A unified-59-surface design memo (Path A+ amend addressing SHOULD_FIX-1 + NIT-1; new owner-scope α/β item) — pre-merge delta audit
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
audit_type: pre-merge milestone delta (rev 2 over rev 1 PASS-WITH-FINDINGS verdict)
qc_branch: qc/pr307-rev2-delta-review-2026-05-09
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR307_REV2_2026-05-09.md (master `4dbfa94`, PR #312)
target_pr_head: c7502e3f74f82318b82e3fe0c5b1cda3ecf5f16d
master_at_audit: 4dbfa94
prior_verdict: REVIEW_QC_PHASE15A_DESIGN_2026-05-08.md (rev 1; PASS-WITH-FINDINGS · 0/1/1; in master via PR #311 if/when merged)
---

# QC pre-merge delta-audit — PR #307 rev 2 (Path A+ amend)

## Result

**PASS** (0 BLOCKER · 0 SHOULD_FIX · 0 NIT). 42nd solo cycle.

Both findings from the rev 1 verdict (SHOULD_FIX-1 + NIT-1) are cleanly addressed. The new §4.2 owner-scope α/β flag is well-formed and routes the v8-artifact-commit decision through the correct discipline (`feedback_orchestrator_decides_not_recommends.md` HOW-not-WHETHER). The rev-1 11-item PASS-WITH-FINDINGS verdict carries forward on unchanged sections; rev 2 introduces no new findings.

## 15-item delta-audit walkthrough (per trigger)

### §1.2 — re-attestation against SHOULD_FIX-1

**Item 1 — Verification method correct ✓**

§1.2 amendment header: "**git-tracked verification (`git ls-files <path>`)**" with explicit citation of the new memory rule `feedback_tc23_existence_must_be_git_tracked.md`. Replaces rev 1's `ls`/`test -e` prose. Method now matches the rule that QC's rev-1 TC-23 used to catch SHOULD_FIX-1 in the first place.

**Item 2 — Result tabulation (17 GREEN / 2 RED across 19 paths) ✓**

QC independently verified at master `4dbfa94` (forward-binding from architect's claim at `9c3b9ae` — same source content for these paths):

```
GREEN river-rats-core/feature_extractor.py
GREEN river-rats-core/feature_keys.py
GREEN river-rats-core/train_model_v9_student.py
GREEN river-rats-core/gto_model.py
GREEN river-rats-core/coaching/gto_model.py
GREEN river-rats-core/oracle_router.py
RED   river-rats-core/models/gto_model_v8_hu.json
RED   river-rats-core/models/gto_model_v8_38feat.json
GREEN river-rats-core/models/gto_model_v9_3way_v2.2.json
GREEN river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json
GREEN data/corpus_combined_988_2026-05-07.jsonl
GREEN data/corpus_combined_988_labels_2026-05-07.jsonl
GREEN scripts/assemble_125k_c_e_988.py
GREEN docs/PROCESS_GUIDE.md
GREEN design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md
GREEN prompts/gto_labeller_v3.4.md
GREEN training-data/tag_vocabulary.json
GREEN river-rats-core/calibration_exam.py
GREEN river-rats-core/coaching/spot_classifier.py
```

Tally: **17 GREEN / 2 RED — exact match with §1.2 attestation table.** Per-path GREEN/RED labels also match.

**Item 3 — 2 RED documented faithfully ✓**

§1.2 explicitly notes for each RED path: "on disk (11.7 MB) but NOT git-tracked; `*.json` excluded by .gitignore line 3; never committed in any branch (`git log --all --oneline -- <path>` empty)". Production-runtime status is distinguished from git-provenance: "loaded at runtime by `oracle_router.py:34` + `:41` (legacy fallback) but have zero git history."

**Item 4 — Inventory of other production-referenced-but-not-tracked paths ✓**

§1.2 "Production status note" section lists `gto_model_v9_3way.json` (referenced by `oracle_router.py:35`; on disk 397 KB; NOT git-tracked). Scope explicitly bounded as a "separate provenance-cleanup workstream after Phase 1.5 ships. NOT addressed in this PR." Architect did NOT silently expand scope; clean separation of concerns.

### §4.2 cascade — close-hand-anchor model + new owner-scope α/β

**Item 5 — Owner-scope flag correctness ✓**

§4.2 has explicit "**⚠️ Owner-scope decision (surfaced 2026-05-09 per QC PR #311 SHOULD_FIX-1 cascade): close-hand-anchor model**" section. Path α (commit v8 artifacts ~23 MB / ~38% repo growth) vs Path β (re-anchor on v9-3way-on-59 model uncertainty) presented with pros/cons for both. Routes through `feedback_orchestrator_decides_not_recommends.md`: experts recommend HOW; owner decides WHAT/WHETHER. Not silently committed by architect.

**Item 6 — Architect-hat recommendation present ✓**

"**Architect-hat recommendation (HOW, not WHETHER, per `docs/PROCESS_GUIDE.md:59-77`): Path β.**" Reasoning provided in 3 substantive points (recurring repo-tax economics; coupling to 1.5-C is non-load-bearing because 1.5-C is on critical path; "v9-3way handles HU spots" is structural via `num_opponents` feature, not workaround). Single committed recommendation; not "open question" or menu-style hedge.

**Item 7 — Gate timing correct ✓**

§7's 4th item explicitly states: "**Owner-gate BEFORE 1.5-D.1 fires. Independent of (does not block) Phase 1.5-A merge — fires in 1.5-D.1 dispatch sequencing.**" Correctly sequenced: 1.5-A merge unblocked by α/β; 1.5-B feature-prune mechanical unblocked; 1.5-C 3-way verification unblocked; only 1.5-D.1 (HU reference set design) gates on this resolution.

### §4.5 cascade — lineage anchor reframing

**Item 8 — Reframing accuracy ✓**

§4.5 amendment paragraph: "v8-HU-38's 'lineage anchor (provenance only)' framing requires nuance — v8-HU-38 is currently the production HU oracle (loaded at runtime by `oracle_router.py:34`/`:41`) but is NOT git-tracked (§1.2 RED entries). Provenance therefore lives in disk artifacts + the `oracle_router.py` filename pointer, not in git history." Reframes "lineage-anchor (provenance only)" → "production-runtime-anchor without git provenance." From-scratch HU retrain commitment "unaffected" (architect kept the 5-class transition + corpus origin reasoning intact).

### §4.6 cascade — production-swap framing

**Item 9 — Filename-pointer framing + TC-23 EXISTENCE on `oracle_router.py:34` ✓**

§4.6 amendment: "the swap is a filename-pointer change at `oracle_router.py:34` from `gto_model_v8_hu.json` (currently runtime-only, not git-tracked per §1.2) to `gto_model_vNext_hu_59feat.json`."

QC verified `oracle_router.py:34` at master `4dbfa94`:

```
$ git show master:river-rats-core/oracle_router.py | sed -n '33,42p'
_MODEL_FILES = {
    1: 'gto_model_v8_hu.json',                    # ← line 34
    2: 'gto_model_v9_3way.json',
    3: 'gto_model_v9_4way.json',
    4: 'gto_model_v9_5way.json',
}

# Legacy filename (before rename)
_LEGACY_HU = 'gto_model_v8_38feat.json'           # ← line 41
```

Line 34 contains the HU slot dict entry referencing `gto_model_v8_hu.json`. ✓

**Item 10 — 1.5-E force-add commitment ✓**

§4.6 amendment last paragraph: "The new model file SHOULD be force-added at 1.5-E to avoid recreating the same git-tracking gap; architect commits to this. Total ship action is therefore: (1) train HU model in 1.5-D.4; (2) at 1.5-E, `git add -f` the new HU model file + change `oracle_router.py:34` filename pointer + run coaching-pipeline tests + commit + open 1.5-E PR." Explicit + sequenced; matches the established `gto_model_v9_3way_v2.2.json` force-add pattern.

### NIT-1 fix

**Item 11 — §1.3.3 prose corrected ✓**

Diff verification (rev 1 → rev 2 at `train_model_v9_student.py:115` reference):

Before (rev 1):
> `:115` (`_V24_P1_BLOCKERS` at indices `-5:-1` post-drop, was `-6:-2` pre-drop) — note this is one of the few places where an off-by-N exists in the assertion structure...

After (rev 2):
> `:115` (`_V24_P1_BLOCKERS` are at indices `-6:-2` of the 61-list pre-drop; after the 2-feature J-B drop, the tail is freed and the v2.4 P1 blockers occupy the final 4 positions of the 59-list — i.e., indices `-4:`).

The wrong "`-5:-1` post-drop" string is removed. The correct `-4:` framing is now the only formulation. Prose is cleaner: arithmetic shown with explicit pre-drop/post-drop reasoning. Matches QC-PR-#311 NIT-1 specification.

### Cross-cutting

**Item 12 — Diff scope strict ✓**

`git diff 6164f14 c7502e3 --name-only`:

```
review/comms/BUILDER_REPORT_PHASE15A_2026-05-08.md
review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md
```

2 files (both already in rev 1; only paragraph-level deltas). +83 / −28. No source / prompt / data / model edits. ✓

**Item 13 — Single committed path preserved ✓**

`grep -E 'TBD|Option A vs|either … or'` against rev 2 returns:

- "Option α: …" / "Option β: …" — the new owner-scope item in §4.2 + §7. Genuine owner-scope per Item 5 above; not technical menu.
- All §3.3, §4.5, §4.6 "Reasoning vs the dispatch's posed alternatives" pattern preserved from rev 1; commitment-with-reasoning style.

No new "open technical questions" introduced. ✓

**Item 14 — TC-X-DISPATCH-COMPLIANCE (21st formal exercise; durable) ✓**

Rev 2 addresses both PR #311 verdict findings explicitly:

| PR #311 finding | Rev 2 addressing section | Status |
|---|---|---|
| SHOULD_FIX-1 (§1.2 + cascade into §4.2/§4.5/§4.6) | §1.2 re-attestation; §4.2 owner-scope α/β; §4.5 lineage reframe; §4.6 filename-pointer + force-add commit | Closed (or routed to owner-scope) |
| NIT-1 (§1.3.3 prose) | §1.3.3 prose corrected | Closed |

No findings carried over un-addressed. No scope creep beyond addressing those findings (memo §0-§8 substantive design path unchanged).

**Item 15 — TC-X-OWNER-SCOPE-DISCIPLINE (22nd formal use) ✓**

6 negative-scope items from original dispatch still held (verified by absence of source/prompt/data/model/D5/`project_v9_3way_ceiling.md` edits in PR diff). New owner-scope α/β flag is well-formed: explicitly labelled "⚠️ Owner-scope"; pros/cons enumerated; architect-recommendation flagged AS-recommendation; gate timing precisely scoped (1.5-D.1, not 1.5-A merge); does not block 1.5-A / 1.5-B / 1.5-C critical path.

## Test classes exercised

- **TC-23** (CONTENT + EXISTENCE; git-tracked verification per `feedback_tc23_existence_must_be_git_tracked.md`) — 17 GREEN / 2 RED on 19 paths; matches §1.2 attestation
- **TC-X-OWNER-SCOPE-DISCIPLINE** (22nd formal use) — 6 negatives held + new α/β flag well-formed
- **TC-X-DISPATCH-COMPLIANCE** (21st formal exercise; durable) — both rev-1 findings closed
- **TC-X-DISPATCH-PREDICTION-VERIFICATION** (carries from rev 1; 7 predictions still registered for retrospective verification at sub-phase closes)
- **TC-X-INTRA-PLAN-CONSISTENCY** (informal — §1.2 ↔ §4.2 ↔ §4.5 ↔ §4.6 ↔ §7 cross-checked; v8-HU-38 status consistent across all 5 sections post-amend)
- **TC-X-METHODOLOGY-RULE-CROSSCHECK** (informal — `feedback_tc23_existence_must_be_git_tracked.md` correctly applied; `feedback_orchestrator_decides_not_recommends.md` correctly applied to α/β routing)

## Smarter-over-time

This is the first delta-audit on a milestone-class design lock. The 15-item delta template is durable for future "QC verdict-PR-cycle → architect-amend → QC re-audit" cycles. Pattern: (a) verify each rev-1 finding has a corresponding rev-2 amendment section; (b) verify the amendment matches the rev-1 verdict's specification; (c) verify no new findings introduced; (d) verify dispatched discipline (owner-scope flagging, methodology-rule citation) intact. Wall-clock ~10 min as forecast.

The architect explicitly cited `feedback_tc23_existence_must_be_git_tracked.md` (the new memory rule from PR #310's drift retro) when re-attesting §1.2. Closure of the cross-stream learning loop: drift retro → memory rule → architect-hat applied → QC verifies. Cross-stream learning capture working as designed; this is the second concrete instance after the curative-additions ratification of TC-X-ORCHESTRATOR-BRANCH-BASE-VERIFICATION in the rev-1 audit.

## Gates

PR #307 rev 2 cleared from QC side. **0 BLOCKER · 0 SHOULD_FIX · 0 NIT.**

Per `feedback_qc_required_before_approval.md` + going-forward owner-merge-fire rule:

- Orchestrator may proceed to merge PR #307 on owner explicit `fire now`.
- After PR #307 + this verdict comm + (still-open PR #311 rev-1 verdict) merge, orchestrator dispatches Phase 1.5-B (feature-prune mechanical execution) per architect's §4.7 sequencing.
- **Owner-scope α/β decision** is a separate, independent gate that resolves before 1.5-D.1 fires (NOT before 1.5-A merge; non-blocking for 1.5-B / 1.5-C).
- **LOOP CONTINUES.**

## Cycle stats

- 42nd solo QC cycle.
- Wall clock: ~10 min (matches dispatch heads-up).
- LLM cost: $0.

---

**Verdict: PASS · 0/0/0 · rev 2 amend cleanly closes both rev-1 findings · new α/β flag is well-formed owner-scope · LOOP CONTINUES on owner-fire-now of merge.**
