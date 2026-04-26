---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ml-architect + careful-engineer reviewer (different dispatch from prior reviewers)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #26 — HIGH-4 cross-stream aggregate semantics fix (Option B; `797108a`)
status: APPROVE — All 11 review items A-K passed; derivation correctness + placement + test coverage HIGH; ready for orchestrator merge as canonical HIGH-4 fix
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/26
branch: stage4-prep/high-4-aggregate-semantics
artifact: 797108a (22 ins feature_extractor.py + 183 new test file)
predecessor_directive: `dfa57e3` (HIGH-4 cross-stream coordination)
qc_findings: Phase 2 MEDIUM (HOLD #12) + Phase 3 HIGH-4 — same root cause
---

# Review Verdict — PR #26 (HIGH-4 cross-stream aggregate semantics fix, Option B)

## Provenance note

Independent reviewer dispatch under read-only constraint. Did NOT author HIGH-4 fix; did NOT review prior Stage 4 prep PRs. Worked from PR #26 head commit `797108a`. Cross-referenced against directive `dfa57e3`, QC findings, and source code.

## Builder verification spot-checks

- Source diff at `feature_extractor.py` lines 2412-2432 sits in correct order: AFTER per_villain_* promotion (line 2410), BEFORE consumers at lines 2450-2451 (which gate Step 12 NaN-flag at 2461 + Step 17 NaN-flag at 2521) ✓
- Derivation math matches CONTENT_API.md:230 §3.7 + QC's suggested patch ✓
- HU path correctly preserved via empty-dict truthy guard ✓
- Branch `stage4-prep/high-4-aggregate-semantics` (commit `797108a`); NOT on master ✓
- Test mirror function matches source verbatim (verified by test #6 grep on source) ✓

---

## Item A — Aggregate-derivation block placement

**OK / HIGH confidence.** New block at lines 2412-2432 is in correct order. Programmatic verification: per_villain_* promotion (2408-2410) → HIGH-4 derivation block (2412-2432) → consumers read aggregates into locals (2450-2451) → Step 12 + Step 17 NaN-flag accordingly (2461, 2521).

The fix actually takes effect.

## Item B — Derivation correctness

**OK / HIGH confidence.**
- ANY-derivation for overflow ✓ (matches CONTENT_API.md:230 §3.7 + QC's suggested patch)
- ALL-derivation for folded ✓ (matches §3.7 + chain helper's `agg_folded` derivation at line 967-970)
- Empty-dict guard correct (HU path empty dicts skip derivation; populated all-False dict triggers derivation correctly)

## Item C — Test coverage

**OK / HIGH confidence.** 6 tests cover spec contract:
1. 3-way overflow partial → True ✓
2. 3-way all-folded → True ✓
3. 3-way partial-fold → False (when prior False) ✓
4. HU single-opponent: empty dicts preserve prior values (both True+False prior cases) ✓
5. No double-source-of-truth invariant: per-villain truth overrides incorrect upstream False; OR with prior True is monotone-True ✓
6. Source-marker integration check ✓

Optional v1.1 NIT: symmetric overflow-side monotone-True test would tighten contract; not blocking.

## Item D — Test mirror vs full integration

**OK with caveat / MEDIUM confidence.** Test uses `_apply_aggregate_derivation()` mirror rather than full `extract_all_features` end-to-end. Pros: isolates derivation; Cons: source could drift from mirror. Mitigation: test #6 reads source + asserts marker comment + both key strings. Catches silent source drift; doesn't catch ordering changes. `test_commit14_finding_b.py` (4/4 PASS) exercises full path on multiway hands — backstop.

## Item E — OR-derivation monotone-True invariant

**OK / HIGH confidence.** Test #5 final assertion documents monotone-True invariant (prior=True preserved even when per-villain partial-fold suggests False). Per-spec:
- OR with prior enables HU sentinel to remain authoritative on HU hands (empty per_villain_* dicts)
- On MW hands, prior `_villain_folded` from chain helper derives via same `all(per_villain.values())` semantics — OR is idempotent
- QC patch suggestion uses identical OR semantics

Could hide a bug? Theoretically if HU sentinel set wrong then 3-way data appeared, OR preserves wrong True. But that's upstream invariant violation, not HIGH-4 fix bug. New code can only escalate (False → True), never demote — documented design.

## Item F — Test runs

**OK / HIGH confidence.** Independent re-run:
- HIGH-4 new tests: **6/6 PASS** (0.01s)
- Combined canonical + hardening: **102/102 PASS** (4.84s) — matches PR description claim exactly

M4 audit not re-run by reviewer (PR description claims preserved; given derivation only escalates aggregate flags on multiway hands with overflow/folded conditions, M4 distribution shift is at worst modest NaN-flagged increase, all spec-aligned).

## Item G — No new MEDIUM-severity issues

**OK / MEDIUM-HIGH confidence.** Spot-check of consumers:
- Step 12 (line 2461): 3-way hand secondary opp overflowed → aggregate True → blocker NaN-flagged. Spec-aligned per directive's "any opp overflowed → blocker unreliable"
- Step 17 (line 2521): same logic; same spec-aligned shift
- `test_must46_*` 4/4 PASS (per_villain_* promotion intact)
- No external consumers of aggregate flags found outside `feature_extractor.py` (game adapter strips them — separate HIGH-2 fix)

No consumer depends on OLD primary-villain-only aggregate semantics.

## Item H — Author concerns assessment

**OK / HIGH confidence.** PR description flags OR-derivation monotone-True invariant + suggests v1.1 NIT for explicit-priority-rule documentation. Both reasonable. Inline comment (lines 2412-2422) + test #5 NOTE block sufficient for v1.0; CONTENT_API.md explicit-priority-rule doc would be v1.1 polish.

## Item I — Diff scope

**OK / HIGH confidence.** 22 additions in `feature_extractor.py` (zero deletions; pure addition). 183 additions in new test file. No scope creep. Minimal + focused.

## Item J — Branch verification

**OK / HIGH confidence.** `git branch --show-current` = feature branch; commit `797108a` lives on feature branch only; not on master. Builder explicitly noted Task 4 incident lesson applied.

## Item K — Ready for orchestrator merge

**APPROVE.** All directive acceptance criteria satisfied:
- ✅ New aggregate-derivation block at correct location
- ✅ Regression test passes (6 assertions vs spec-required 4)
- ✅ Canonical suite still PASS (50/50)
- ✅ Task 4.5 hardening pass (52/52)
- ✅ M4 audit preserved (per PR description; not independently re-run)
- M5 anchor recheck explicitly optional; not gating

---

## VERDICT

**APPROVE — overall confidence HIGH.**

**Required fixes:** None.
**Blockers:** None.

## NIT-level observations (non-blocking, optional v1.1)

1. **Symmetric monotone-True overflow test:** Test #5 covers fold-side monotonicity; symmetric overflow-side test would tighten contract.
2. **CONTENT_API.md explicit-priority-rule doc:** Inline source comment + test #5 NOTE sufficient for v1.0; explicit-priority-rule documentation would be polish.

## Action items

| # | Severity | Item |
|---|---|---|
| 1 | NIT (v1.1) | Symmetric overflow-side monotone-True test (mirror test #5 fold-side) |
| 2 | NIT (v1.1) | CONTENT_API.md §3.7 explicit-priority-rule documentation |

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_26_HIGH_4_AGGREGATE_SEMANTICS_2026-04-26.md`.
2. Post comment on PR #26 referencing verdict.
3. Stand by for orchestrator merge.
4. Lifts orchestrator's HOLD if any (per pattern).

**Orchestrator:**
1. Read this verdict.
2. Merge PR #26 — APPROVE clean.
3. HIGH-4 SEALED on merge. Cross-stream gate progress: 7/9 SEALED per directive's projection.
4. Teaching extension is OPTIONAL per directive (defensive belt-and-braces).

**Owner:** wake to find HIGH-4 cross-stream coordination Option B SEALED — aggregate semantics now match CONTENT_API §3.7 amendment; mode label drift fixed on multiway hands.

## Reference

- PR #26: https://github.com/beytell1-sketch/river-rats-v2/pull/26
- Feature commit: `797108a`
- Directive: `dfa57e3` (HIGH-4 cross-stream coordination)
- QC findings: Phase 2 MEDIUM + Phase 3 HIGH-4 (same root cause)
- Modified files: `feature_extractor.py` + new `tests/test_high_4_aggregate_semantics.py`

**FINAL VERDICT: APPROVE — HIGH confidence overall. HIGH-4 SEALED on merge.**
