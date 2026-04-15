---
date: 2026-04-15
from: Owner (Rupert) + main terminal
to: Future session / restarted builder
re: Current state snapshot — where we are, what's pending, what to do next
status: REFERENCE — not a directive, a snapshot
---

# River Rats v2.2 — Session State Snapshot

## TL;DR

- **v2.2 training complete.** Model at `river-rats-core/models/v2_2_model.json`.
- **Gate 7 DECISION PENDING.** Model missed MW reference target
  by 2.5pp (80.0% vs 82.5%). FB-40 passed (72.5% vs 70.0%).
  Owner awaiting solver time on 10 MW misses to decide ship vs iterate.
- **HRP investigation resolved.** `hero_range_percentile = 0.00`
  on MW misses was a test harness bug, not a feature extraction
  defect. Training data intact. Bias signature corrected (see below).
- **6 parallel tracks directive issued** while waiting on solver.
  Builder stopped responding partway through — may need restart.

## What's been approved and committed

| Item | Status |
|---|---|
| v2.2 training data (385 hands × 108 features) | Committed, Gate 6 passed |
| v2.2 XGBoost model | Trained, saved |
| Teaching handoff export | Both repos, approved |
| HRP investigation | Root-cause: test harness bug |
| Track A v2.3 scope | Draft with 3 pending amendments |
| Track B generator fix blueprint | Approved for implementation |
| Track D teaching handoff | Approved |
| Track E v2.3 diagnostic test set | Approved with 2 amendments |
| Track C vocab dedup | Committed as-is |

## What's pending

### Blocker: Owner solver time
10 MW misses need solver verification. Export at
`review/comms/SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html`.
Owner runs when available. Drives Gate 7 decision.

### Builder work in progress (may need restart)
Per `DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md`:

**Tier 1 (should have started):**
- Track 1: Harness hardening (Programmer, 1 call)
- Track 3: Training data completeness audit (Programmer + ML Architect, 2 calls)
- Track 4: MW miss bias deep-dive (GTO Expert + Programmer, 2 calls)
- Track 5: BP generator fix implementation (Programmer, 1-2 calls)

**Tier 2 (after Tier 1):**
- Track 2: FB-40 re-eval with hardened harness (Programmer, 1 call)
- Track 6: Track A scope corrections (Architect, 1 call)

## Corrected bias signature (from HRP investigation)

The original Track A scope claimed `hero_range_percentile = 0.00`
was the bias signature. That was wrong — it was a test harness
artifact. The corrected signature from re-extracted MW misses:

| Feature | Miss avg | Non-miss avg |
|---|---|---|
| hero_range_percentile | 0.641 | 0.443 |
| equity_vs_range | 0.656 | 0.431 |
| villain_air_pct | 0.320 | 0.280 |
| villain_top_pair_plus_pct | 0.371 | 0.425 |
| spr | 1.250 | 1.250 |
| better_hand_pct | 0.292 | 0.549 |
| worse_hand_pct | 0.697 | 0.428 |

**Reading:** Model under-bets when hero is at TOP of range with
strong equity — specific pattern, not generic passivity. GTO
Expert deep-dive (Track 4) analyses whether this is trap bias,
defensive bias, or label/model alignment issue.

## v2.3 Amendments pending (not yet applied to scope doc)

Three Track A amendments from REVIEW_PARALLEL_TRACKS_2026-04-15.md:

1. **Reconcile BET delta** — allocation table says +166 BET,
   narrative says +155 + 31. Pick one, make consistent.
2. **Update Section 2 CHECK-bias signature** — drop hrp=0.00,
   use corrected signature above (coordinate with Track 4 GTO
   deep-dive output).
3. **Add explicit calibration gate** — 23/28 + reversals must
   pass before v2.3 production labelling.

Two Track E amendments:

1. **Absolute accuracy floor on Groups A+B** — not just 5pp
   improvement. E.g., must hit 70%+ absolute.
2. **Group D regression fallback** — if v2.3 regresses on
   reversal accuracy by >1 hand, investigate before ship.

## Key files for a restarted builder

### Reference
- `review/comms/PLAN_V2.2_FINAL_COMBINED_2026-04-13.md` — overall plan
- `review/comms/PLAN_PHASE3_FINAL_2026-04-13.md` — Phase 3 plan
- `review/comms/PHASE_3_5H_FINAL_ASSEMBLY_2026-04-15.md` — Gate 6 submission
- `review/comms/PHASE_4_TRAINING_REPORT_2026-04-15.md` — Gate 7 submission
- `review/comms/HRP_INVESTIGATION_2026-04-15.md` — test harness bug finding

### Active directives
- `review/comms/DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md` — the 6 tracks

### Owner reviews to address
- `review/comms/REVIEW_PARALLEL_TRACKS_2026-04-15.md` — amendments for A, E

### Approved blueprints ready to implement
- `review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md` — Track B fix

### Scope documents needing update
- `review/comms/PLAN_V23_SCOPE_2026-04-15.md` — needs Track A amendments
- `review/comms/PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md` — needs Track E amendments

## Memory notes

- Owner prefers slow/deliberate quality work over fast iteration
- Solver is labour-intensive for owner, not unlimited
- Solver output is informed but not absolute — mixed strategies
  matter
- 4-team Pass 1 unanimous + complete data = highly reliable
- Pass 2 overrides of Pass 1 unanimous need solver confirmation
- Never commit someone else's in-progress work
- River Rats v2 repo: origin = github.com/beytell1-sketch/river-rats-v2.git
- River Rats teaching repo: no GitHub remote

## v2.3 backlog items (logged in memory)

1. Action distributions (gauge labels) — v3.0
2. Model 2: intention prediction — confirmed viable
3. Model 3: feature attention prediction
4. Multi-street linked training
5. **BLOCKER:** villain seat data integrity validator
   (Track B implementation pending)
6. ~~SPR<2 semi-bluff guard~~ — INVALIDATED by solver
7. v2.3 calibration: bucket-first passive lean in mixed spots
8. Pass 2 override discipline — reframed

## What a restart should do first

1. Read this file
2. Read `HRP_INVESTIGATION_2026-04-15.md`
3. Read `DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md`
4. Check git status — what's uncommitted from the previous
   builder session?
5. Ask owner: resume at which track? Tier 1 tracks are
   independent, can start any of them.

## What is NOT done (do not skip)

- Do NOT ship v2.2 until Gate 7 decision is made (owner + solver)
- Do NOT generate v2.3 supplement hands until:
  - Track B generator fix is merged
  - Track A scope is corrected (amendments applied)
  - Owner approves corrected scope
- Do NOT implement v3.0 action distributions — separate project,
  post-v2.2

---

**Last activity:** Owner approved parallel tracks directive.
Builder was expected to launch Tier 1 tracks (1, 3, 4, 5) but
has stopped responding. Restart should begin with Tier 1 or
confirm with owner.
