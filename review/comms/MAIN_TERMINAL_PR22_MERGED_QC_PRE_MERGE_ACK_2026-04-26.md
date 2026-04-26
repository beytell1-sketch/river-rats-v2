---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed) · QC stream (briefed)
re: PR #22 MERGED at 970017e — v1.0.3 NITs sealed; Stage 6 held-out FULLY SEALED at canonical v1.0.3 hash-lock 65cfbf26... unchanged from v1.0.2; QC pre-merge audit on PR #21 ACK (CONVERGED APPROVE; 1 MEDIUM v1.1 follow-up + 3 NITs); HOLD #24 added (HIGH-2 indirect propagation gap in range_narrowing.py); pilot-dispatch gate at 6/9 sealed
status: CONFIRMATION + ACK + DIRECTIVE — PR #22 sealed; QC pre-merge audit acknowledged; QC pre-merge value pattern confirmed; MEDIUM follow-up queued for v1.1
---

# PR #22 Merged + QC Pre-Merge Audit ACK

## PR #22 — Task 4.3 v1.0.3 SEALED

| Field | Value |
|---|---|
| PR # | 22 |
| Title | Stage 4 prep Task 4.3: v1.0.3 NIT prose-consistency pass |
| Merge commit | `970017e` on origin/master |
| Feature commit | `7e6de19` preserved per `--merge` |
| Verdict commit | `46585fe` (preserved on master) |
| Feature branch | `stage4-prep/stage6-holdout-fill-4-3` deleted from origin |
| Merge time | 2026-04-26 ~12:34 SAST |
| Rollback tag | `pre-pr22-merge-2026-04-26` at `46585fe` (origin) |
| Reviewer verdict | **APPROVE clean** (no NITs) |

### v1.0.3 acceptance check (per reviewer + orchestrator)

| # | Criterion | Result |
|---|-----------|--------|
| 1 | NIT-A: §12 tally `1F/3C/2C/3B/1R` matches §6 canonical | ✅ |
| 2 | NIT-B: title (line 37) + lock-prose (line 50) say v1.0.2 (CONTENT version) | ✅ |
| 3 | NIT-C: prereq §1 says v1.0.2 | ✅ |
| 4 | HASH-LOCK INVARIANT: `65cfbf26...` over 47652 bytes UNCHANGED | ✅ |
| 5 | All 4 edit clusters OUTSIDE hashed block | ✅ |

**Stage 6 held-out test set is now FULLY SEALED at v1.0.3 canonical.**

The hash-lock invariant preservation is the load-bearing property:
v1.0.3 added prose-consistency fixes WITHOUT touching the hashed
spec-block. v1.0.2 hash `65cfbf26...` over 47652 bytes carries
forward as the canonical lock for pilot-use evaluation. No new
hash to track; v1.0.3 is a documentation-prose-only revision over
v1.0.2's spec lock.

## QC Pre-Merge Audit on PR #21 — ACK

### Headline ACK

QC stream produced a **pre-merge audit** on PR #21 (Task 4.5 logic
hardening bundle) before the PR was merged. **Multi-expert
convergence on APPROVE.** The audit predates orchestrator's
reviewer dispatch and ran in parallel — first run of QC's TC-10
**pre-merge variant** test class.

This is a new pattern: QC running pre-merge audits on substantive
PRs as a third independent voice, alongside the dispatched
reviewer (general-purpose with persona) and the orchestrator's
own pre-merge protocol-compliance checkpoint #4.

**Value demonstrated:** the QC pre-merge audit surfaced a MEDIUM
finding + 3 NITs that the dispatched reviewer didn't flag (the
dispatched reviewer found APPROVE clean; QC's adversarial agent
surfaced more). This is exactly the protocol-diversity outcome
the QC stream was created for — same-pipeline reviewer chain
misses what an adversarial framing catches.

### MEDIUM finding (advisory; v1.1 follow-up)

**HIGH-2 indirect propagation gap.** QC Agent #2 SOLO finding:
`range_narrowing.py:601, 673, 778`
(`narrow_to_betting_range/checking/continuing`) call
`classify_hand(hand, board)` WITHOUT try/except. These are invoked
from `narrow_by_action_history` which is called from
`feature_extractor.py:825` and `:1794`.

**Risk:** if an audit/pilot script loads a corrupted opp_range
from disk, the corrupted key reaches `narrow_to_betting_range` →
ValueError propagates UP past Task 4.5's HIGH-2 try/except guards
→ crashes feature extraction.

**Limited to corrupt-on-disk audit/pilot scenarios.** Not a
production-path issue (logic's internal range generation produces
well-formed combos).

**Recommended fix (v1.1):** add `try/except ValueError as exc:
logging.warning + skip` wrapper around either:
- `narrow_to_*` calls in `range_narrowing.py:601, 673, 778`, OR
- `narrow_by_action_history` callsites in
  `feature_extractor.py:825, 1794`

Either closes the gap.

**Disposition:** Out-of-scope for Task 4.5 per directive
(Task 4.5 scoped to direct classify_hand callsites; this finding
is the same-class gap on the indirect path). Adding as **HOLD #24**
in the register; v1.1 hardening pass or post-pilot housekeeping.

### 3 NITs (defer to v1.1+; non-blocking)

- NIT-1: `classify_hand('AhAh', board)` accepted (duplicate
  specific card not rejected). Not a regression.
- NIT-2: `_action_history_cache_key` doesn't flatten mutable inner
  values; TypeError if a future caller adds list/dict-typed `amount`
  field.
- NIT-3: timestamp 1s resolution in audit-runner can collide on
  rapid back-to-back runs (<1s). PR's own test sleeps 1.05s — implicit
  acknowledgment. Worth a 1-line millisecond suffix or PID
  disambiguator.

**Disposition:** Defer all 3 to v1.1+ or post-pilot housekeeping
per QC's recommendation. Not blocking.

### TC-10 pre-merge variant — first-run value confirmed

QC's standing roadmap includes pre-merge audits as a workstream;
this was the first execution. Value demonstrated:
1. **Surfaced 1 MEDIUM + 3 NITs** the standard reviewer chain
   missed
2. **Multi-expert convergence framework** worked again (4th TC-15
   demonstration)
3. **Cheaper than post-hoc fix-forward** — the MEDIUM is now
   queued for v1.1 instead of becoming a Task 4.6 incident later

**Going forward:** QC may continue running pre-merge audits on
substantive PRs at their discretion (Phase 4 hourly /loop is the
right cadence). Orchestrator's standing per-batch protocol +
QC pre-merge audit form a complementary pair: reviewer dispatched
verdict gates merge; QC pre-merge audit provides structural
robustness check.

This is a healthy multi-voice merge gate. **Welcome.**

## PR #23 disposition (Path B duplicate)

PR #23 contains the same QC pre-merge audit doc that's been
bundled into the orchestrator commit. Same pattern as PR #17/#19/#20.

**Closing PR #23 as byte-identical no-op duplicate.** Standing
dual-path protocol applies; comment will reference the bundle
disposition.

## Pilot-dispatch gate progress (updated to 6/9)

```
✅ Phase 2 HIGH-2 (game adapter passlist):       SEALED at b944621
✅ Phase 3 HIGH-1 (STREET_NAME_MAP whitelist):   SEALED via PR #21
✅ Phase 3 HIGH-2 (classify_hand raises):        SEALED via PR #21
✅ Phase 3 HIGH-3 (cache key + AH; PILOT GATE):  SEALED via PR #21
✅ Phase 1 HIGH (audit-runner immutability):     SEALED via PR #21
✅ Task 4.3 v1.0.3 (NITs):                       SEALED via PR #22 (just now)

⏳ Phase 2 HIGH-1 (teaching renderer translation):     pending teaching
⏳ Task 5 (Pilot orchestration v1.0):                  GREENLIT; awaits authoring
⏳ HIGH-4 (cross-stream aggregate semantics):           coordination doc queued
⏳ HOLD #21 (FEATURE_COLUMNS contract drift):          post-Task-4.5 investigation
⏳ HOLD #24 (HIGH-2 indirect propagation gap):         🆕 v1.1 follow-up
⏳ QC pre-pilot sweep clean (Phase 5):                 QC standing roadmap
```

**6 of 9 gate items SEALED.** Remaining critical-path:
1. Teaching HIGH-1 fix (renderer translation)
2. Task 5 (Pilot orchestration) authoring + sealing
3. HIGH-4 cross-stream coordination

The remaining 3 HOLDs (#21 FEATURE_COLUMNS, #24 indirect
propagation, QC pre-pilot sweep) are post-pilot or in-flight QC
operations.

## Stage 6 held-out canonical state

```
v1.0   = initial (PR #16; APPROVE-WITH-NITS verdict at 9758a99)
v1.0.1 = fix-forward (PR #18 merged afc815c; APPROVE-WITH-NITS at cc247ac)
v1.0.2 = micro-correction (direct push f43cd49; APPROVE-WITH-NITS at cc247ac post-hoc)
v1.0.3 = NIT prose-consistency (PR #22 merged 970017e; APPROVE clean at 46585fe)  ← canonical
```

Hash-lock chain:
- v1.0.1: `b775df2a...` over 47653 bytes
- v1.0.2: `65cfbf26...` over 47652 bytes (–1 byte from H025 header)
- v1.0.3: `65cfbf26...` over 47652 bytes (UNCHANGED from v1.0.2 — prose-only fixes outside hashed block)

**Pilot evaluation can use v1.0.3 (= v1.0.2 spec-block) NOW** as
the hash-locked test set. Prereqs remaining are only the standing
ones (solver verification on 10-hand sample + owner final
approval).

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 18 | v1.0.2 reviewer verdict + pilot-use sealing | ✅ SEALED via PR #22 v1.0.3 merge | — |
| 20 | Task 4.3 v1.0.3 NIT prose-consistency | ✅ SEALED via PR #22 merge | — |
| 21 | FEATURE_COLUMNS vs model 55-feature contract drift | ⏳ QUEUED — investigate | Logic builder |
| 22 | RERUN_ gitignore | ⏳ QUEUED — small fix | Logic builder |
| 23 | Cache-key docstring update | ⏳ QUEUED — small fix | Logic builder |
| **24** | **HIGH-2 indirect propagation gap (range_narrowing.py:601/673/778)** | **🆕 ACTIVE — v1.1 hardening pass or post-pilot housekeeping** | **Logic builder** |
| 17 | Phase 3 HIGH-4 aggregate semantics (cross-stream) | ⏳ QUEUED — coordination doc | Orchestrator → logic + teaching |
| 12 | MEDIUM aggregate flag derivation (Phase 2) | ⏳ QUEUED — folds into HIGH-4 | Same |
| 9 | gto-expert vs general-purpose-with-persona convergence check | ⏳ QUEUED — post-pilot | Orchestrator |
| 13 | Cross-stream-READY verdict brief addition | ⏳ QUEUED — PROCESS_GUIDE + memory | Orchestrator |
| 19 | Procedural option codification (merge-first vs review-first) | ⏳ OPTIONAL | Orchestrator (on builder request) |

## Cross-stream context

- **Teaching at `e29aec1`** — held; HIGH-1 directive shipped;
  awaiting builder's renderer translation fix
- **Game at `b944621`** — HIGH-2 SEALED; chip playtest unblocked;
  Phase B per-villain bars unblocked
- **QC stream Phase 4 active** — TC-10 pre-merge variant first-run
  successful; Phase 4 hourly /loop continues; standing re-audits
  queued (game post-HIGH-2; logic post-Task-4.5)

## Action

**Builder:**
1. **Begin Task 5 (Pilot orchestration v1.0)** per `9093998`
   directive — branch `stage4-prep/pilot-orchestration-fill`
2. Standing per-batch protocol (PR + reviewer + merge — NO direct-push)
3. Surface in `review/comms/` when PR opens
4. **HOLD #24 (HIGH-2 indirect propagation gap)** noted for v1.1
   hardening pass or post-pilot housekeeping
5. **HOLDs #21/#22/#23/#24** are queued non-blocking items;
   investigate when between substantial work

**Orchestrator (me):**
1. PR #22 merged + QC pre-merge audit ACK shipped (this commit)
2. PR #23 closure with byte-identical no-op comment + dual-path
   protocol pointer (immediately after this comm lands)
3. **Should now write the HIGH-4 cross-stream coordination doc** —
   teaching held / between cycles; logic between cycles (post-PR-22-merge);
   right window for cross-stream alignment proposal
4. Loop continues at 15-min cadence
5. Watch for Task 5 PR + teaching HIGH-1 fix + QC re-audits

**Owner:**
- 6 of 9 pilot-dispatch gates SEALED (most substantial single-day
  progress in Stage 4 prep arc)
- Stage 6 held-out canonical at v1.0.3
- Critical-path items remaining: teaching HIGH-1 + Task 5 + HIGH-4
- Pilot dispatch still owner-gated; gate clearing rapidly

## References

- PR #22 commit: `7e6de19`
- PR #22 verdict: `46585fe`
- PR #22 merge: `970017e`
- Rollback tag: `pre-pr22-merge-2026-04-26` at `46585fe`
- QC pre-merge audit (Path B bundled): `QC_PRE_MERGE_AUDIT_PR21_2026-04-26.md`
  in this same comms folder
- Task 4.3 directive: `cb4ef48`
- Task 5 greenlight: `9093998` / `MAIN_TERMINAL_PR21_MERGED_TASK5_GREENLIGHT_2026-04-26.md`

**Status: PR #22 MERGED — Stage 6 held-out v1.0.3 SEALED canonical.
QC pre-merge audit ACKed. HOLD #24 added. Pilot-dispatch gate at
6/9 SEALED. Task 5 next critical-path.**
