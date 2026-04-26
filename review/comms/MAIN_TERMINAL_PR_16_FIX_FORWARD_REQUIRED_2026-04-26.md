---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #16 (Task 4 Stage 6 held-out v1.0) — APPROVE-WITH-NITS verdict with 2 HIGH-severity findings; fix-forward to v1.0.1 required (hash mismatch + arithmetic errors + 4 MEDIUM rebalances)
status: DIRECTIVE — 2 HIGH + 4 MEDIUM + several NITs to address; reviewer notes "stricter reading would escalate to REQUEST-CHANGES"; same fix-forward pattern as prior tasks
---

# PR #16 Fix-Forward Required — Stage 6 Held-Out v1.0.1

## Reviewer verdict summary

PR #16 verdict at `9758a99`: **APPROVE-WITH-NITS** with 2
HIGH-severity + 4 MEDIUM-severity + several NITs. Reviewer notes:
*"stricter reading would escalate to REQUEST-CHANGES."*

Strong design artifact (50 hands well-authored, non-overlap
verified, sizing solver-aligned, prereqs disciplined) BUT 7
substantive issues require Task 4.1 fix-forward before pilot
dispatch / evaluation use.

Per memory `feedback_quality_default_no_ask.md`: HIGH-severity
findings require fix-forward; MEDIUM/non-blocking still address.
PR #16 held pending v1.0.1 fix-forward.

## The 2 HIGH-severity findings (must fix)

### HIGH #1 — SHA256 hash mismatch (Item F)

The single most consequential finding. **The lock currently
certifies nothing.**

- **Claimed hash:** `8b553de0745bb50f5867a330d507eb106c04b9bc09f385e16966eec925b3b74b`
- **Recomputed hash on file at `30ec324`:** `b3970aa595bba9e6d0c107e2c07d1ec4165bd214d0262914a3d96a15d11322ae`
- **Claimed bytes:** 40,404
- **Actual bytes between markers:** 40,655

3 occurrences of each marker in the file (START at offsets 1512,
9169, 12508; END at 1574, 9224, 53163) because the prereq prose
AND the recommended `python3` one-liner reference markers
literally. The recommended `re.search(re.S)` non-greedy `.*?`
matches FIRST pair (empty 62-byte span) producing different hash.
Neither greedy/non-greedy/LAST-LAST matches the recorded hash.

Most likely author computed hash on in-progress version then made
post-hash edits (H007 fix-up, re-frame notes for H016/19/45/47,
post-fact line renumbering) and committed without re-hashing.

**Fix-forward action:**
1. Recompute hash on final byte content of v1.0.1
2. Record corrected hash in the v1.0.1 file
3. Document resolution rule (e.g., "use LAST-LAST markers")
4. Remove literal markers from prereq prose OR escape them as
   code-fenced examples that don't grep-match the literal strings

### HIGH #2 — Pot/SPR arithmetic errors (Item H)

Spot-check of 10 hands:
- H001, H013: ✓
- H002, H006, H023, H047, H049, H050: off by 0.5 (SB dead-money
  inconsistency)
- **H022, H028: claimed pot 28.6, recomputed 22 — off by 6.6bb
  (~30%); double-counted turn bet**

H022 and H028 are the serious cases — 30% pot mis-statement
materially affects whether hero's action is profitable.

**Fix-forward action:**
1. Recompute pot/SPR on H022 and H028 from action history
2. Recompute pot/SPR on 6 off-by-0.5 hands; either correct OR
   document the SB dead-money convention explicitly so
   convention-following readers don't trip
3. Run a sweep across all 50 hands' pot/SPR claims; flag any
   other arithmetic drift before pushing v1.0.1

## The 4 MEDIUM-severity rebalances

### MEDIUM #1 — Action distribution skew (Item B)

Achieved 4 FOLD / 10 CHECK / 11 CALL / 20 BET / 5 RAISE vs target
10/12/10/13/5.

- **FOLD −6 is real evaluation gap.** Effective FOLD-class sample
  size 4 — single mislabel swings per-class metric by 25pp.
  Cannot reliably score FOLD behavior. Model's known weak class
  historically is FOLD discipline (over-fold MW textures,
  under-fold dominated bluffcatcher rivers per
  `feedback_solver_findings.md`).
- BET +7 mostly defensible but pushes evaluation imbalanced.

**Fix-forward action:** re-author 6 hands as face-bet → FOLD spots
covering:
- Dominated bluffcatcher rivers
- Draws short of pot odds
- MW air on monotone face-cbet
- IP TP face turn-x-raise on dynamic boards

### MEDIUM #2 — Confidence band distribution (Item C)

Achieved 30 HIGH / 18 MEDIUM / 2 LOW vs target 30/15/5.

**LOW −3 is meaningful.** Only 2 LOW (H024, H046) → no statistical
power for LOW-band stratum. LOW spots are highest-signal
evaluation hands.

**Fix-forward action:** add 3 more LOW-confidence hands. Candidates:
- Thin river bluffs into capped ranges
- MW turn underpair vs continuation barrel
- 3-bet pot OOP check-raise frequency calls

### MEDIUM #3 — Solver-verification 10-sample has NO FOLD (Item D)

Sample H002, 007, 013, 019, 024, 028, 032, 037, 043, 049 covers
4 HIGH / 5 MEDIUM / 1 LOW + CHECK/CALL/BET/RAISE — but **NO FOLD
spots**. FOLD spots' equity/fold-equity split is solver
verification's primary value.

**Fix-forward action:** swap HOLDOUT_046 (mid overpair face turn
check-raise, FOLD, LOW) into the 10-sample for H019 or H037 (both
CALL/MEDIUM/soft over-represented). Consider also adding 3-bet
pot OOP check-raise hand (H045 or H047).

### MEDIUM #4 — Calibration manifest location verification (Item E)

24-hand calibration manifest location unknown. Author's "subsumed
in pass1/factory" claim plausible but not verified.

**Fix-forward action:** owner / builder verify whether separate
manifest exists; document explicit calibration-set fingerprint
list in the held-out non-overlap verification.

## NITs (lower priority; can fold into Task 5 wrap-up if ergonomic)

- **Item A NITs (JSONL export risk):**
  - H007: dual `Board:` lines (4-card depiction error + corrected line)
  - H016, H019, H045, H047: `Re-frame action history` blocks may
    confuse JSONL exporter
  - H032: preflop hand with no `Board:` field — schema
    accommodate or silent-break risk
- **Item G NIT:** H041 BET_66 on flop is sanctioned but atypical
  (most solvers use 25/50/66/75 mix)
- **Item I NIT:** H022 polar-bluff classification — author flagged
  `[UNCERTAIN-SOLVER]` and soft tolerance; acceptable as-is given
  the flag; solver verification should add H022 to pre-pilot pass

These NITs don't break v1.0 as design artifact but **Prereq #6
(format round-trip) cannot pass without a flatten pass** for the
H007/16/19/32/45/47 export issues. So in practice they're MEDIUM
rather than NIT.

**Fix-forward recommendation:** also resolve these JSONL-export
issues as part of Task 4.1 to avoid Prereq #6 failure later.

## Fix-forward workflow (mirror Tasks 1.1 / 2.1 / 3.1)

1. **New branch:** `stage4-prep/stage6-holdout-fill-4-1`
2. **Author dispatch:** address all HIGH + MEDIUM findings:
   - HIGH #1: recompute hash + resolution rule + fix marker
     ambiguity
   - HIGH #2: pot/SPR sweep on all 50 hands
   - MEDIUM #1-4: action distribution rebalance, LOW band fill,
     solver-sample swap, calibration manifest verification
   - JSONL export issues (escalated MEDIUM)
3. **Reviewer dispatch (different agent):** verify all HIGH + 4
   MEDIUM addressed; verify hash recomputes correctly; verify
   pot/SPR arithmetic on full corpus; flag any new issues
4. **Open PR #17** with title "Stage 4 prep Task 4.1: Stage 6
   held-out test set v1.0.1 (HIGH-severity fix-forward)"
5. **Standing PR pattern:** 4-checkpoint, verdict on PR thread,
   builder writes verdict comms, orchestrator merges on APPROVE
6. **PR #16 disposition:** orchestrator merges PR #17 (which
   contains PR #16's content as ancestor) — same auto-resolution
   pattern as PRs #10→#11, #12→#13, #14→#15

## Estimated fix-forward effort

Heavier than prior fix-forwards (HIGH-severity items + corpus-wide
arithmetic sweep + 6+ hand re-authoring):

- HIGH #1 hash: ~15 min (recompute + document)
- HIGH #2 arithmetic sweep: ~45-60 min (verify all 50 pot/SPR)
- MEDIUM #1 FOLD spots authoring: ~60-90 min (6 hands)
- MEDIUM #2 LOW band fill: ~30-45 min (3 hands)
- MEDIUM #3 solver-sample swap: ~10 min (table edit)
- MEDIUM #4 manifest verification: ~15 min
- JSONL export fixes: ~20-30 min
- **Total: ~3-4.5 hours**

Plus reviewer dispatch ~30-45 min on the larger v1.0.1 surface.

This is a substantial fix-forward. Multi-expert dispatch on the
re-authoring is encouraged (per Stage 4 plan protocol-diversity)
to keep the FOLD-spot rationale rigour high.

## Cross-stream — unchanged

Task 5 (Pilot orchestration) sequencing unchanged. Builder may run
Task 4.1 sequential before Task 5, OR start Task 5 in parallel if
context budget allows (per existing builder discretion).

## Action

**Builder:**
1. Open `stage4-prep/stage6-holdout-fill-4-1` branch
2. Author dispatch addressing 2 HIGH + 4 MEDIUM + JSONL NITs
3. Reviewer dispatch (independent)
4. PR #17 per standing pattern
5. After PR #17 APPROVE: orchestrator merges (auto-resolves PR #16)

**Orchestrator (me):**
1. PR #16 held pending fix-forward
2. PR #17 (Task 4.1) merge per standing pattern after APPROVE
3. Loop continues at 15-min cadence

**Owner:**
- 3 of 5 Stage 4 prep tasks sealed; Task 4 mid-fix-forward
- The HIGH findings (hash + arithmetic) are integrity issues
  with the test artifact itself — fix-forward is mandatory
  before pilot dispatch
- Held-out test set v1.0.1 will be the single-shot evaluation
  artifact for Stage 6 ship gate; rigour matters

## Reference

- `MAIN_TERMINAL_PR_15_MERGED_TASK4_GREENLIGHT_2026-04-26.md` (`623a029`)
  — Task 4 greenlight
- `MAIN_TERMINAL_BUILDER_TASK4_PROCEED_2026-04-26.md` (`6d8f2a1`)
  — Task 4 explicit unblock
- `9758a99` — PR #16 reviewer verdict (APPROVE-WITH-NITS,
  2 HIGH + 4 MEDIUM)
- `feedback_quality_default_no_ask.md` — quality discipline
- `feedback_solver_findings.md` — model's FOLD-class weakness
  history (motivates MEDIUM #1 FOLD-spot rebalance)
