---
date: 2026-04-15
from: Outgoing main terminal
to: New main terminal (orchestrator) — restart
re: Latest state + next actions — read me with SESSION_STATE_2026-04-15.md
status: HANDOFF — read before confirming the restart to owner
---

# Orchestrator Handoff — 2026-04-15

## Purpose

You are a new main terminal / orchestrator session taking over
from the previous one. The prior session is stopping. This
file has the latest state, decisions, and pending items so you
don't have to reconstruct them from scrolling comms history.

**Read this AFTER cloning the repo and reading
`review/comms/SESSION_STATE_2026-04-15.md` for the base plan.
Then come back here for what's happened since.**

---

## 1. Latest commits (most recent first)

- **8038b4a** — Main terminal update: Tracks 1+3 recovered,
  new Track 3.5 for ANOMALY-A
- **8e77e05** — Track 3: Training data completeness audit
- **b5d84b5** — Track 1: Harness hardening — fail fast on
  incomplete feat_dict
- **db8a0d2** — Restart pack: fix for GitHub-first access
- **8097f34** — Restart pack folder
- **d4b791a** — Session state snapshot
- **64e3d08** — Fix BP generator villain-seat drop
  (v2.3 backlog item 5) ← **Track 5 done by builder**
- **1312dac** — Directive: 6 parallel tracks post-HRP
- **6baa81b** — HRP investigation
- **6cd11ca** — Review: parallel tracks A, B, D, E

## 2. What's DONE (don't redo)

| Item | Status | Commit |
|---|---|---|
| Gates 1-6 | All passed | multiple |
| v2.2 training | Gate 7 pending | 5267a0b |
| Track 1: Harness hardening | DONE | b5d84b5 |
| Track 3: Training data audit | DONE | 8e77e05 |
| Track 5: BP generator fix | DONE | 64e3d08 |
| Track D: Teaching handoff | APPROVED | (older) |
| Track C: Vocab dedup | DONE | c01852c |
| HRP investigation | Test harness bug confirmed | 6baa81b |
| v2.2 label set | 385 hands × 108 features locked | 9dd1a68 |

## 3. What's PENDING (action needed)

### Blocker: owner solver time
- 10 MW misses need solver verification
  (`review/comms/SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html`)
- Drives Gate 7 ship/iterate decision
- Owner has not yet run this

### Builder tracks pending
Per `MAIN_TERMINAL_UPDATE_2026-04-15.md`:

- **Track 3.5 (NEW, BLOCKING):** ANOMALY-A verification
  - Training data audit found `street` encoded inconsistently
    (52% float, 48% string). If v2.2 pipeline coerced to float,
    185 rows read as 0 (flop), corrupting half the training
  - ML Architect must verify whether v2.2 training was actually
    corrupted
  - Deliverable target: `review/comms/ANOMALY_A_VERIFICATION_2026-04-15.md`
  - **This may partially or wholly reframe the MW miss
    diagnosis — Track 4 is on hold until this completes**

- **Track 2:** FB-40 re-eval with hardened harness
  (depends on Track 1, which is now done)

- **Track 4:** MW miss bias deep-dive
  (HOLD until Track 3.5 completes)

- **Track 6:** Track A v2.3 scope corrections
  (depends on Track 4 output)

### Owner amendments pending on scope docs

Track A v2.3 scope needs 3 amendments per
`REVIEW_PARALLEL_TRACKS_2026-04-15.md`:
1. Reconcile BET delta inconsistency
2. Update Section 2 bias signature (drop `hrp=0.00`, use
   corrected signature from HRP investigation + eventual
   Track 4 output)
3. Add explicit calibration gate (23/28 + reversals)

Track E test set needs 2 amendments:
1. Absolute accuracy floor on Groups A+B
2. Group D regression fallback definition

## 4. New findings since SESSION_STATE_2026-04-15.md

### ANOMALY-A is potentially bigger than HRP

HRP was a test-harness bug (evaluation-time). ANOMALY-A, if
confirmed, is a TRAINING-time bug that affected the model
itself. Half the training data may have had wrong street
values.

If ANOMALY-A corrupted training:
- v2.2 model has fuzzy street understanding
- "Bucket-first CHECK bias" diagnosis may be partially wrong
  (model might be confused about street, not passive)
- Gate 7 reasoning may need revisiting
- v2.3 must confirm encoding consistency before supplement
  generation

**Track 3.5 is blocking everything downstream because we can't
design v2.3 fixes for a bias that might not be what we think
it is.**

### Builder push discipline

Prior builder session completed Track 1 and Track 3 locally
but did not push. Main terminal recovered both when owner
asked about local state. New commit discipline documented in
`MAIN_TERMINAL_UPDATE_2026-04-15.md`: push after every commit,
don't batch.

## 5. How main terminal and builder communicate

Builder and main terminal are on separate machines and cannot
talk directly. Communication is via GitHub files:

- **Main terminal → Builder:**
  `review/comms/MAIN_TERMINAL_UPDATE_<date>.md`
- **Builder → Main terminal:**
  `review/comms/BUILDER_STATUS_<date>.md` or
  `review/comms/BUILDER_BLOCKED_<date>.md`
- **Deliverables:** builder writes per-track reports to
  `review/comms/<TRACK_NAME>_<date>.md` and commits + pushes
- **Main terminal checks:** `ls -lt review/comms/ | head -10`
  periodically

## 6. Your first actions as new main terminal

1. **Clone the repo** (if not already):
   ```
   git clone https://github.com/beytell1-sketch/river-rats-v2.git \
     ~/river-rats-v2
   cd ~/river-rats-v2
   ```

2. **Read in order:**
   - `review/comms/SESSION_STATE_2026-04-15.md`
   - `review/comms/HRP_INVESTIGATION_2026-04-15.md`
   - `review/comms/TRAINING_DATA_AUDIT_2026-04-15.md`
   - `review/comms/MAIN_TERMINAL_UPDATE_2026-04-15.md`
   - This file

3. **Check for new builder drops:**
   ```
   ls -lt review/comms/ | head -15
   ```
   Look for `ANOMALY_A_VERIFICATION_*`, `BUILDER_STATUS_*`, or
   `BUILDER_BLOCKED_*`.

4. **Verify `git push` works** on your machine. If not, report
   to owner before any commits.

5. **Summarize current state to owner** in 3-4 sentences.

6. **Wait for direction or builder drop.**

## 7. Owner preferences (from memory, carry forward)

- Slow/deliberate quality work over fast iteration
- Solver is labour-intensive, not unlimited — used for pattern
  detection + clear-wrong cases, not per-hand arbitration
- 4-team Pass 1 unanimous + complete data = highly reliable
- Pass 2 overrides of Pass 1 unanimous need solver confirmation
- Never commit someone else's in-progress work without
  verifying it works
- Reviewer writes to review/comms/ without asking
- Commit autonomously with descriptive messages + push
- Verify source files before asserting claims
- Check `ls -lt review/comms/ | head -5` before declaring a
  wait state

## 8. What NOT to do

- Do NOT ship v2.2 — Gate 7 is owner's call after solver
- Do NOT generate v2.3 hands — blocked on Track 3.5 +
  Track A amendments
- Do NOT make code changes — main terminal writes comms only
- Do NOT run `git push --force` or rewrite history
- Do NOT touch the teaching repo (separate, no GitHub remote
  yet)

## 9. What to watch for

### Builder drop: `ANOMALY_A_VERIFICATION_<date>.md`
This is the critical pending deliverable. When it lands,
review it — it determines whether Gate 7 reasoning changes
and how much v2.3 scope needs to shift.

### Builder drop: `BUILDER_BLOCKED_<date>.md`
If builder hits an issue (auth, infrastructure, ambiguous
blueprint), they'll drop this file. Read it, diagnose, and
write a `MAIN_TERMINAL_UPDATE_<date>.md` response.

### Owner signal: solver results
Owner may drop solver verification results in a file like
`SOLVER_VERIFICATION_MW_RESULTS_*.md`. This unblocks Gate 7.

## 10. v2.3 backlog (don't lose these)

Stored in memory as `project_river_rats_v23_backlog.md`:
1. Action distributions (gauge labels) — v3.0
2. Model 2: intention prediction — viable, experiment post-v2.2
3. Model 3: feature attention prediction
4. Multi-street linked training
5. Villain seat validator — Track 5 DONE
6. ~~SPR<2 semi-bluff guard~~ — INVALIDATED
7. v2.3 calibration: bucket-first passive lean
8. Pass 2 override discipline reframed

Memory path:
`~/.claude/projects/-home-rupertbeytell/memory/project_river_rats_v23_backlog.md`

If you don't have that memory file (different machine), the
summary above is sufficient.

---

**Welcome to the session. Everything you need is committed to
origin/master. Push after every commit, read comms files
regularly, and wait for owner direction before launching
anything proactive.**
