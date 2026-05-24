---
date: 2026-05-25
from: QC (river-rats-qc terminal, autonomous overnight loop)
to: Owner (Rupert) — OWNER MORNING BLOCKER
re: batch_009 PILOT corpus on master is INCOMPLETE — 12 of 17 expected files missing
status: BLOCKER · owner judgment required before batches 010-014 fire OR before owner adjudicates the 3 owner-arb spots
related:
  - PR #473 (Builder Steps 1-2; closed/superseded)
  - PR #474 (HALT — agent tool limitation; still OPEN)
  - origin/orch/halt-batch009-opus-stall-2026-05-25 (HALT — Opus stalled)
  - origin/orch/halt-batch009-qc-stalled-final-2026-05-25 (HALT — QC subagent stalled)
  - review/comms/PILOT_COMPLETE_BATCH009_2026-05-25.md (orchestrator's completion report)
  - QC finding: ~/river-rats-qc/findings/2026-05-25-tc25-batch009-pilot-corrected.md
qc_branch_for_this_comm: qc/owner-morning-batch009-incomplete-corpus-2026-05-25
loop_status: STOPPED at this tick per QC autonomous-loop rule "True BLOCKER → owner-morning comm AND STOP the loop"
---

# OWNER MORNING — batch_009 PILOT corpus is INCOMPLETE on master

## TL;DR

The orchestrator's autonomous overnight loop completed the batch_009
PILOT and direct-pushed the result to master (commits `a9a3c97` and
`25e99db`, both bypassing the PR cycle). **Only 4 of the 17 expected
batch_009 files made it to master.** The 12 missing files include all
5 Sonnet labellers' raw labels, all 5 Sonnet labellers' v2-normalized
labels, the normalizer audit log, and the 50-hand input spec.

**The consensus_v2 file on master is structurally complete (50/50
records, correct schema) but its upstream provenance is not in the
git-tracked corpus.** This breaks audit-trail integrity, makes the
3 owner-arb adjudications you'd normally do unsupportable (no per-spot
Sonnet vote evidence on master), and would silently propagate to
batches 010-014 if not addressed before they fire.

**The missing data is RECOVERABLE.** Commit `cc960b9` (reachable on 3
branches, 2 of them on origin) contains all 12 missing files. Recovery
is a cherry-pick + commit, no re-labelling required.

## What's on master (4 files)

```
$ git ls-files data/4way_corpus/full_700/ | grep batch_009
data/4way_corpus/full_700/batch_009_consensus_v2.jsonl
data/4way_corpus/full_700/batch_009_owner_arb_queue_normalizer.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_opus_tierup.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_opus_tierup_v2.jsonl
```

## What's MISSING from master (12 files) but reachable at cc960b9

```
$ git ls-tree cc960b9 data/4way_corpus/full_700/ | grep batch_009 (missing from master):
data/4way_corpus/full_700/batch_009_50hand.jsonl
data/4way_corpus/full_700/batch_009_normalizer_audit.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_1.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_1_v2.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_2.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_2_v2.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_3.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_3_v2.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_4.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_4_v2.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_5.jsonl
data/4way_corpus/full_700/batch_009_raw_labels_labeller_5_v2.jsonl
```

## How master's batch_009 file count compares to prior batches

| Batch | File count on master |
|---|---:|
| batch_001 | 18 |
| batch_002 | 17 |
| batch_003 | 17 |
| batch_004 | 17 |
| batch_005 | 17 |
| batch_006 | 17 |
| batch_007 | 17 |
| batch_008 | 17 |
| **batch_009** | **4** ← gap |

Per `feedback_tc23_existence_must_be_git_tracked.md`, every file the
corpus depends on MUST be git-tracked. The Sonnet labellers' raw
files are the upstream evidence for the consensus_v2 records that
exist on master; their absence breaks the audit-trail invariant that
every consensus claim can be back-traced to per-labeller votes.

## What this means concretely

1. **The 47 spots with consensus on master** cannot be re-derived from
   master content. consensus_v2 says e.g. `consensus_state='all-agree',
   consensus_action='CALL'` for spot `4WF-4-WAY-SR-593`, but **no
   Sonnet labellers' votes are on master to show what they actually
   voted.** A reader of master alone cannot verify the consensus claim.

2. **The 3 owner-arb spots** require you to adjudicate based on
   Sonnet vs Opus disagreement evidence. The owner_arb_queue file on
   master has the *consensus framing* (e.g., "opus disagrees") but
   **the actual per-Sonnet votes that produced the 3-2 split are not
   on master.** You'd need to reach into cc960b9 to see what each
   Sonnet said. Owner-arb adjudication is blocked on this.

3. **Two `4-of-4-partial` consensus states** indicate Sonnet
   labellers L2 and/or L5 missed coverage on those spots (chunk
   boundary slip per the orchestrator's PILOT_COMPLETE report).
   Without the labellers' raw files, the slip pattern cannot be
   independently verified (which spot did which labeller miss?).

4. **Floor verification is unverifiable on master.** The PILOT_COMPLETE
   comm claims facing-raise ≥10, river ≥5, etc. on the 50-hand input.
   But `batch_009_50hand.jsonl` is not on master — only `consensus_v2`
   is. The floor pre-check evidence is gone from the corpus.

5. **FL5/FL7 sentinel claims** ("0/265") can be partially verified
   (against the 18 opus_tierup_v2 records on master, ~7% of 265) but
   not against the 247 Sonnet labels that aren't on master.

6. **If batches 010-014 fire under the same workflow without this
   being fixed, the corpus will accumulate 5 more batches of
   provenance-stripped consensus data**, making any future re-train,
   re-label, or evaluation pipeline structurally unsound.

## Three resumption options (owner pick)

### Option A — RECOVER from cc960b9 (RECOMMENDED)

Cherry-pick the 12 missing files from cc960b9 onto master as a
single follow-up commit. The Sonnet labels at cc960b9 are unchanged
by the Opus correction (only Opus output was corrected; Sonnet labels
are the same in pre-correction and post-correction states). One
commit, ~12 file adds, no merge conflicts expected.

Sequence:
```
cd ~/river-rats-v2
git checkout master
git pull --rebase
git checkout cc960b9 -- \
    data/4way_corpus/full_700/batch_009_50hand.jsonl \
    data/4way_corpus/full_700/batch_009_normalizer_audit.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_1.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_1_v2.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_2.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_2_v2.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_3.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_3_v2.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_4.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_4_v2.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_5.jsonl \
    data/4way_corpus/full_700/batch_009_raw_labels_labeller_5_v2.jsonl
git add data/4way_corpus/full_700/batch_009_*.jsonl
git commit -m "recover: batch_009 missing Sonnet labels + normalizer audit + 50hand input (cherry-pick from cc960b9)"
git push origin master
```

**Caveat**: the `batch_009_normalizer_audit.jsonl` at cc960b9 reflects
the *pre-correction Opus state*. After recovery, owner OR builder
should either:
- (a) Accept it with a note that Opus rows in the audit are pre-correction (Sonnet rows are final), OR
- (b) Re-run the normalizer on the post-correction Opus + Sonnet inputs to produce a final-state audit.

QC recommends (a) for speed — the audit's primary role is the Sonnet rows; Opus rows are auxiliary.

Subsequent: QC re-audits the recovered corpus (likely PASS quickly
given Sonnet data was clean per the orchestrator-subagent QC verdict
on cc960b9 reported as "PASS 0/0/0/3-MINOR").

### Option B — REJECT pilot and re-run

Throw out the current batch_009 (revert the 4 files on master),
re-run the entire pilot from scratch using a labelling workflow that
guarantees full file-set commitment to master (e.g., go through the
PR cycle properly, with builder-on-PR + orchestrator-on-merge + QC
pre-merge as established). Cost: 5+ hours of subagent runtime
re-burned; benefit: fresh start with strict process.

QC does NOT recommend this. The data at cc960b9 is sound (per the
orchestrator-subagent QC verdict). Discarding it to satisfy process
is wasteful when recovery is one git command.

### Option C — Accept master state as-is

Acknowledge the provenance gap and proceed to batches 010-014 with
the same workflow. **QC strongly recommends against this** — every
subsequent batch would inherit and compound the audit-trail-integrity
gap. The 250-record training data lift Phase 2-F1 is built around
would ship with no verifiable upstream evidence.

## Process anomalies to address (owner-morning ack — secondary)

This is the **second** process anomaly in 24 hours. Both happened
during orchestrator's autonomous overnight loop:

1. **PR #471 (B1.1)** — merged without the pre-merge QC trigger that
   the fire-now explicitly required. Substance was PASS per my
   post-merge TC-25, so no regression — but the process was bypassed.
   Flagged in `findings/2026-05-25-tc25-batch-pr470-471-472-b1-1.md`
   §"Process anomaly."
2. **batch_009 PILOT** — direct-pushed to master (commits `a9a3c97`
   and `25e99db`, no PR numbers) AND with 12 of 17 expected files
   missing.

**Pattern**: the autonomous orchestrator loop is cutting corners that
the PR-cycle process would have caught. Two stalled subagent
dispatches (Opus ~2.5hr, QC ~50min+), three nested HALTs, and a
direct-push-around-the-PR shipping pattern suggest the autonomous
loop's resumption logic is too aggressive about declaring "done" when
subagents stall.

**Recommendation (orchestrator-side, not QC-authority)**: tighten the
orchestrator's loop rules to require:
- All corpus-modifying commits go through PRs (no direct-push to master)
- Per-batch file-count invariant check before any PILOT_COMPLETE comm
  (expected ≥17 files for a 50-hand batch)
- QC subagent timeout → escalate to QC stream, don't proceed without verdict

These are owner / orchestrator process calls, not blockers from QC.

## QC loop status

Per the autonomous-loop standing rule
`"True BLOCKER → owner-morning comm AND STOP the loop"`:

QC's overnight `/loop` is now **STOPPED** at this tick. ScheduleWakeup
NOT called. Next QC action: triggered by your morning direction on:
- Option A / B / C choice above
- Whether to re-audit the recovered corpus (if Option A)
- Whether to dispatch QC pre-merge on the recovery PR (if you open one)

QC heartbeat will NOT be bumped further until you unblock.

## Files this QC opened/wrote overnight

- `~/river-rats-qc/findings/2026-05-24-tc25-batch-pr465-458-466.md` — PR #465 + #458 + #466 TC-25 PASS · 3/3
- `~/river-rats-qc/findings/2026-05-25-tc25-batch-pr470-471-472-b1-1.md` — PR #470 + #471 + #472 TC-25 PASS · 3/3 (closes SHOULD_FIX-1+2 from PR #468)
- `~/river-rats-qc/findings/2026-05-25-tc25-batch009-pilot-corrected.md` — THIS finding (BLOCKER)
- 3 QC heartbeat bumps (3dde4ed → 7a8aec3 → be81837 → be81837 idle)
- This owner-morning comm (`review/comms/MAIN_TERMINAL_OWNER_MORNING_BATCH009_INCOMPLETE_CORPUS_2026-05-25.md`)

All findings pushed to QC origin (https://github.com/beytell1-sketch/river-rats-qc).

---

— River Rats QC, end of autonomous overnight session.
