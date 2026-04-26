---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed) · QC stream (briefed)
re: PR #24 MERGED at f33e4f7 — Task 5 Pilot orchestration v1.0 SEALED CANONICAL; **Stage 4 prep Wave 2 COMPLETE (5/5 tasks)**; v1.0.1 pre-dispatch fix-forward directive (M-1 terminology drift + L-1/L-8/L-11/L-12 cross-protocol firewall + tool restrictions + API-tier prereqs + path corrections); QC pre-merge audit ACK; pilot-dispatch gate at 7/9 SEALED
status: CONFIRMATION + DIRECTIVE — PR #24 merged; Task 5 v1.0 sealed; v1.0.1 fix-forward bound to PILOT-DISPATCH approval (NOT to merge); pre-dispatch fix-list issued; QC pre-merge audit acknowledged
---

# PR #24 MERGED — Stage 4 Prep Wave 2 COMPLETE

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 24 |
| Title | Stage 4 prep Task 5: Pilot orchestration v1.0 (FINAL Wave 2 task) |
| Merge commit | `f33e4f7` on origin/master |
| Feature commit | `4b6c50a` preserved per `--merge` |
| Verdict commit | `ba8d062` (preserved on master) |
| Feature branch | `stage4-prep/pilot-orchestration-fill` deleted from origin |
| Merge time | 2026-04-26 ~12:44 SAST |
| Rollback tag | `pre-pr24-merge-2026-04-26` at `ba8d062` (origin) |
| Reviewer verdict | **APPROVE-WITH-NITS** (5 NITs, none block merge) |

Pre-merge protocol-compliance checkpoint #4:
- ✅ HARD branch check via atomic flow (master)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Independent ml-architect + orchestration-engineering reviewer
  dispatch
- ✅ All 6 ML-architect DRAFT v0.1 flags resolved with sound reasoning
- ✅ 13-prereq PRE-DISPATCH section sound + execution-ready
- ✅ Cross-references verified (Stage 6 hash `65cfbf26...` at line 282;
  Task 4.5 merge `add2617`; Stage 5 v1.0.1; 8 cited memory files;
  cost recalculation $142.84-$701.20 → stated $140-$700)
- ✅ Phase B 5h matches 60s/call midpoint math (300×60÷(5×3))

**Stage 4 prep Wave 2 = COMPLETE. 5/5 tasks SEALED.**

```
Task 1 (Protocol B v1.0.1)         ✅ sealed dc6fa1f
Task 2 (Protocol C v1.0.1)         ✅ sealed 435757f
Task 3 (Stage 5 retrain v1.0.1)    ✅ sealed b639776
Task 4 (Stage 6 held-out v1.0.3)   ✅ sealed 970017e
Task 5 (Pilot orchestration v1.0)  ✅ sealed f33e4f7 ← just now
```

## v1.0.1 Pre-Dispatch Fix-Forward Directive

**Pattern note:** Both reviewers (orchestrator's dispatched + QC
pre-merge audit) explicitly recommended:
- **Merge v1.0 NOW** ✅ done
- **Bind v1.0.1 pre-dispatch fixes to OWNER PILOT-DISPATCH APPROVAL,
  not to merge**

This is a different pattern from Task 4 (where v1.0 didn't merge until
v1.0.1 fix-forward landed). Task 5 v1.0 is on master canonical;
v1.0.1 cleanup happens before owner authorizes pilot dispatch.

### Fix-forward scope (5 items)

#### M-1 (MEDIUM) — Stage 5 contract terminology drift

QC's Phase 5 finding: spec line 591 (Highlighter H1 brief substitution
context) reads:
> "the 55-feature vector + post-commit-14 multiway promotions = 59
> raw features per Stage 5 retrain v1.0.1"

But Stage 5 v1.0.1 (lines 22, 57, 143, 234, 665) names the +4
features as **v2.4 BLOCKER features** (`nut_flush_block`,
`nut_made_block_pct`, etc.). The phrase "post-commit-14 multiway
promotions" appears nowhere in Stage 5 or in
`prompts/gto_labeller_v3.1.md`.

Arithmetic correct (55+4=59). Semantic label wrong. H1 highlighters
reading this brief look for "multiway-promotion features" that don't
exist as such → confusion + potential failure mode in Phase D.

**Fix:** rewrite spec line 591 to:
> "the 55-feature vector + 4 v2.4 blocker features = 59 raw features
> per Stage 5 retrain v1.0.1 §Hyperparameters point #4"

Single-paragraph edit. ~5 min.

#### L-1 (LOW; pre-dispatch) — Cross-protocol output-path firewall

QC: Protocol C labellers could path-traverse to read Protocol A/B
outputs. Same-stream isolation needed for protocol-diversity
guarantee.

**Fix:** add labeller tool restriction in each Labeller brief:
> "Read/Write only within
> `review/pilot_run_<date>/labels/protocol_<your_protocol>/agent_<your_slot>/`."

Apply to all 3 Labeller briefs (A/B/C). ~10 min.

#### L-8 (LOW; pre-dispatch) — Tool restrictions across all 6 briefs

QC: tool restrictions absent from Labeller / Highlighter / Reviewer /
Adjudicator briefs. Pilot Orchestrator brief has explicit
allowed/prohibited (whitelist-or-raise per Task 4.5 lesson); other
5 briefs don't.

**Fix:** apply Task 4.5 whitelist-or-raise discipline consistently
across all 6 briefs. Each brief gets:
- ALLOWED tools list (specific tool names)
- PROHIBITED tools list (everything else; explicit rejection on use)

~20-30 min total.

#### L-11 (LOW; pre-dispatch) — API-tier + model-selection promote to PRE-DISPATCH PREREQUISITES

QC: API-tier and model-selection are footnotes; drive 5× cost swing
+ rate-limit risk. Should be operator-checkable PRE-DISPATCH items.

**Fix:** add 2 rows to PRE-DISPATCH PREREQUISITES section near top:
- "Anthropic API tier confirmed (Tier ≥ X for Phase B 5-way × 3-batch
  parallelism; verifiable via live tier check or rate-limit headers)"
- "Model selection locked (Opus vs Sonnet) for Labeller / Highlighter
  / Reviewer / Adjudicator roles — drives cost envelope from $140 to
  $700"

~5 min.

#### L-12 (LOW; pre-dispatch) — Path resolution: `LABELLING_PIPELINE.md`

QC: `LABELLING_PIPELINE.md` cited without `docs/` prefix in 2
locations.

**Fix:** path correction → `docs/LABELLING_PIPELINE.md` (or whatever
the canonical path is per the file's actual location).

~2 min.

### Workflow

**Standing per-batch protocol** (per the protocol-drift note —
NO direct-push):

1. Branch: `stage4-prep/pilot-orchestration-fill-1-0-1`
2. Implement 5 fixes
3. Self-test: rerun any cross-references; verify line 591 correctly
   replaced; verify all 6 briefs have tool restrictions; verify path
   resolution
4. Open PR
5. Reviewer dispatch (general-purpose with ml-architect or
   orchestration-engineering persona; different than v1.0 reviewer
   at `ba8d062`)
6. Verdict on master (precedes merge)
7. Orchestrator merge

### Acceptance criteria

1. Line 591 reads "v2.4 blocker features" not "multiway promotions"
2. All 6 phase agent briefs have ALLOWED/PROHIBITED tool restriction
   sections
3. PRE-DISPATCH PREREQUISITES has 15 rows (was 13; +API tier +model
   selection)
4. `LABELLING_PIPELINE.md` references all use `docs/` prefix where
   applicable
5. v1.0.1 changelog block in frontmatter cites the 5 fixes
6. Reviewer APPROVE before owner pilot-dispatch authorization

### Estimated effort

~45-60 min (5 small fixes + reviewer cycle).

### Sequencing — relative to other queued work

After PR #24 merge, builder may work in any order:
- v1.0.1 pre-dispatch fixes (this directive)
- HIGH-4 fix (Option B; ~30-60 min; coordination shipped at `dfa57e3`)
- HOLD #21 FEATURE_COLUMNS investigation (post-Task-4.5 task)

**Quality-default sequencing recommendation:**
1. v1.0.1 pre-dispatch fixes (small; clears pilot-dispatch path)
2. HIGH-4 Option B fix (cross-stream alignment; clears another gate
   item)
3. HOLD #21 FEATURE_COLUMNS investigation (lower-stakes; can be
   between cycles)

Builder's call on actual order; quality default just orders by
"clears most gate items soonest."

## QC Pre-Merge Audit on PR #24 — ACK

QC stream's TC-10 pre-merge variant ran on PR #24. **CONVERGED
APPROVE-WITH-NITS.** Multi-expert TC-15 fifth demonstration:
- Agent #1 (operator-readability): APPROVE-WITH-NITS, all 5 fill-ins
  PASS, 13 prereqs verifiable, all cross-refs verified, 0 HIGH /
  0 MEDIUM / 2 LOW
- Agent #2 (adversarial): APPROVE-WITH-NITS, deep-probe surfaced
  M-1 + 11 LOW; same merge call

CONVERGED on merge call. DIVERGED at finding depth — adversarial
agent's failure-mode probing surfaced gaps operator-readability
framing didn't reach. Same protocol-diversity outcome as prior 4
TC-15 demonstrations. **Five consecutive demonstrations of the
multi-expert principle working as designed.**

### M-1 (this orchestrator's directive includes it)
QC's M-1 (terminology drift on H1 brief) folded into v1.0.1 fix-
forward scope above.

### L-1, L-8, L-11, L-12 (pre-dispatch fixes)
QC's pre-dispatch fix-list folded into v1.0.1 fix-forward scope above.

### L-2 through L-7, L-9, L-10, N-1, N-2 (deferred to v1.1 / pilot-runtime)
- L-2 "Anonymised" reasoning aggregation undefined
- L-3 Adjudicator role-separation enforcement is assertion not
  mechanical guard
- L-4 No HARD CAP on aggregate cost telemetry
- L-5 No aggregate schema-violation DROP halt
- L-6 Labeller resumption mid-batch rule ambiguous
- L-7 Marginal-calibration chain doesn't trigger HALT
- L-9 Protocol C raise-sizing scope unclear (RAISE vs BET)
- L-10 Inter-batch dispatch gating not specified
- N-1 Phase A 33-way concurrency may need rate-limit preflight
- N-2 Locked plan §4.2 line 146 stale agent count (pre-existing)

**Disposition:** all deferred to v1.1+ or pilot-runtime monitoring.
Some (L-3 mechanical guard, L-4 HARD cost cap, L-5 schema-violation
HALT) are good candidates for a v1.1 hardening pass after pilot-run
empirical data informs the threshold values. Not blocking pilot
dispatch.

### Author concerns (PR #24 description) — verified adequate

QC verified each of the 4 builder-surfaced concerns:
1. 5-vs-15 parallelism — preflight live tier check + upgrade escape
2. Per-call latency ~30-90s — concrete "instrument first 5 calls +
   halt if >2×" gate
3. Highlighter context-scope independence — judgment call, both
   reviewers found principled
4. Adjudicator role 1+3 different subagents — assertion in spec, not
   mechanical (same as L-3); pilot-runtime verifiable

## Pilot-dispatch gate progress (NOW 7/9 SEALED)

```
✅ Phase 2 HIGH-2 (game adapter passlist):           SEALED at b944621
✅ Phase 3 HIGH-1/2/3 + Phase 1 HIGH (Task 4.5):     SEALED via PR #21
✅ Task 4.3 v1.0.3 NITs:                             SEALED via PR #22
✅ Task 5 (Pilot orchestration v1.0):                SEALED via PR #24 ← just now

⏳ Phase 2 HIGH-1 (teaching renderer translation):    pending teaching
⏳ HIGH-4 (cross-stream aggregate semantics):         coordination at dfa57e3; awaits builder
⏳ Task 5 v1.0.1 pre-dispatch fixes:                  this directive (~45-60 min)
⏳ HOLD #21 FEATURE_COLUMNS contract drift:           post-Task-4.5
⏳ HOLD #24 HIGH-2 indirect propagation:              v1.1 post-pilot
⏳ QC pre-pilot sweep clean (Phase 5):                QC standing roadmap
```

**7/9 SEALED.** Critical-path remaining for pilot-dispatch gate:
1. Teaching HIGH-1 fix
2. HIGH-4 Option B fix
3. Task 5 v1.0.1 pre-dispatch fixes
4. QC Phase 5 pre-pilot sweep

After all 4 land → owner pilot-dispatch authorization.

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 25 | Task 5 reviewer verdict + sealing | ✅ SEALED via PR #24 merge | — |
| 26 | Task 5 v1.0.1 pre-dispatch fix-forward (M-1 + L-1/L-8/L-11/L-12) | 🆕 ACTIVE — directive issued | Logic builder |
| 17 | Phase 3 HIGH-4 aggregate semantics (cross-stream) | ⏳ ACTIVE — Option B greenlit at dfa57e3; awaits builder | Logic builder |
| 12 | Phase 2 MEDIUM aggregate flag derivation | (folds into HIGH-4) | Same |
| 21 | FEATURE_COLUMNS vs model 55-feature contract drift | ⏳ QUEUED — post-Task-4.5 | Logic builder |
| 22 | RERUN_ gitignore | ⏳ QUEUED — small fix; v1.1 housekeeping | Logic builder |
| 23 | Cache-key docstring update | ⏳ QUEUED — small fix; v1.1 | Logic builder |
| 24 | HIGH-2 indirect propagation gap (range_narrowing.py:601/673/778) | ⏳ QUEUED — v1.1 post-pilot | Logic builder |
| 9 | gto-expert vs general-purpose-with-persona convergence check | ⏳ QUEUED — post-pilot | Orchestrator |
| 13 | Cross-stream-READY verdict brief addition | ⏳ QUEUED — PROCESS_GUIDE + memory | Orchestrator |

## Cross-stream context

- **Teaching at `b75d867`** — held; HIGH-1 directive shipped;
  awaiting builder's renderer translation fix
- **Game at `62fee00`** — Phase B mockup approved; integration
  greenlit
- **QC stream Phase 4 dynamic /loop active** — TC-10 pre-merge
  variant working consistently (5 demonstrations); will continue
  hourly + accelerate near pre-pilot milestone

## Action

**Builder:**
1. **Begin Task 5 v1.0.1 pre-dispatch fix-forward** (5 fixes; ~45-60 min)
2. After v1.0.1 sealed: HIGH-4 Option B fix (~30-60 min)
3. After HIGH-4 sealed: HOLD #21 FEATURE_COLUMNS investigation
   (between cycles; lower stakes)
4. Standing per-batch protocol (PR + reviewer + merge — no direct-push)

**Orchestrator (me):**
1. PR #24 merged + v1.0.1 directive shipped (this commit)
2. Watch for v1.0.1 PR + HIGH-4 PR + teaching HIGH-1 fix + game Phase
   B integration
3. Continue 15-min loop cadence
4. **Queued: PROCESS_GUIDE + memory addition for cross-stream-READY
   verdict brief** — natural moment when builder is on a v1.1
   housekeeping cycle

**Owner:**
- Stage 4 prep Wave 2 COMPLETE (5/5 tasks)
- Pilot-dispatch gate at 7/9 SEALED
- Critical-path: teaching HIGH-1 + HIGH-4 + Task 5 v1.0.1 + QC Phase 5
- After all 4 land: pilot-dispatch authorization is the next owner
  decision

## References

- PR #24 commit: `4b6c50a`
- PR #24 reviewer verdict: `ba8d062`
- PR #24 merge: `f33e4f7`
- Rollback tag: `pre-pr24-merge-2026-04-26` at `ba8d062`
- QC pre-merge audit: `5bd58fd` (QC repo) +
  `QC_PRE_MERGE_AUDIT_PR24_2026-04-26.md` (in this same comms folder;
  bundled by this commit per Path B dual-path)
- Task 5 directive: `9093998`
  (`MAIN_TERMINAL_PR21_MERGED_TASK5_GREENLIGHT_2026-04-26.md`)
- HIGH-4 coordination: `dfa57e3`
  (`MAIN_TERMINAL_HIGH_4_CROSS_STREAM_COORDINATION_2026-04-26.md`)

**Status: PR #24 MERGED. Task 5 v1.0 SEALED CANONICAL. Stage 4 prep
Wave 2 COMPLETE (5/5). v1.0.1 pre-dispatch fix-forward directive
issued. QC pre-merge audit ACKed. Pilot-dispatch gate at 7/9 SEALED.**
