---
date: 2026-04-26
from: Pilot Orchestrator (general-purpose subagent under Pilot Orchestrator persona)
to: Main terminal (orchestrator) · Owner · QC stream
re: Phase A.7 summary — A.4 OPTION C BOTH LANES FAIL on identical 2 Group-D reversal hands; HARD HALT per Option C decision tree row 4 + orchestrator Halt conditions ("A.4 calibration fails"); pattern is labeller-side (protocol/KB), not model-side; total spend ~$3.03 (well under $200 hard cap)
status: HARD HALT — A.4 GATE FAIL on both lanes; Phase B dispatch BLOCKED until protocol/KB revision OR pass-criterion adjustment; Pilot Orchestrator HALTed all downstream dispatch; surfacing for owner decision
session_persona: Pilot Orchestrator (active since ~19:55 SAST)
phase_a_wall_time: ~12 min total (A.5 ~1 min + A.4 dispatch + grading ~10 min)
phase_a_total_cost_estimate: ~$3.03 (Sonnet ~$0.41 + Opus ~$2.63; well under all halt thresholds)
---

# Pilot Phase A.7 Summary — HARD HALT

## Headline

**Option C parallel calibration: BOTH LANES FAIL.**

| Lane | Standard gate (≥23/33) | Reversal gate (100% / 10) | GATE | Cost | Wall-time |
|------|------------------------|----------------------------|------|------|-----------|
| Sonnet 4.6 | PASS (28/33; 84.8%) | **FAIL** (8/10) | **FAILED** | ~$0.41 | ~4.4 min |
| Opus 4.7 | PASS (29/33; 87.9%) | **FAIL** (8/10) | **FAILED** | ~$2.63 | ~4.4 min |

Per Option C decision tree row 4 + orchestrator Halt conditions ("A.4 calibration fails" = HARD halt): **Pilot Orchestrator HALTs all downstream dispatch.** Phase B blocked.

## Critical insight: failure pattern is labeller-side, not model-side

**Both lanes failed on the IDENTICAL 2 reversal hands** (and both failed MW-39 standard hand the same way). This is not a model-quality problem (both Sonnet AND Opus passed the 23/33 standard gate). This is a protocol/KB problem — the v3.1 labelling protocol + 3-way GTO knowledge base produces predictably-wrong outputs on these specific spots regardless of model strength.

| Hand | Type | Expert | Sonnet | Opus | Pattern |
|------|------|--------|--------|------|---------|
| **d3688_BB_flop** | REVERSAL | CHECK | BET | BET | Both invoke "<20% villain TP+ + high air → BET for protection" but expert wants CHECK on this 8cKc/KdTd4s BB OOP spot with 2-tone diamond board |
| **d9556_BB_flop** | REVERSAL | CHECK | BET | BET | Both invoke KB Worked Example 4 + DO NOT Rule #3 ("monsters must bet 3-way") — but on this 5h5d/5s6d6h paired board (flopped fives full), expert wants CHECK (likely value cession against capped villain on paired board) |
| **MW-39** | STANDARD | CALL | RAISE | RAISE | Both invoke KB §1.7 carve-out (nut FD + Ah blocker = RAISE) on AhJh/Kh8h3d — expert wants CALL |

These are KNOWN HARD reversal cases. `calibration_exam.py` line 73 comment for d3688: *"v2.2 BET, expert CHECK on KT4 flush board with second villain"* — i.e., v2.2 also got this wrong; v3.1 was supposed to fix it; **v3.1 did not fix it on either model**.

Per `feedback_solver_findings.md` ("8 solver findings: raise/call mixing, blocker effects, over-fold bias, nut draw raise rule"): the MW-39 RAISE-instead-of-CALL pattern matches "nut draw raise rule" — KB §1.7 carve-out is being applied too broadly. The d3688/d9556 BET-instead-of-CHECK pattern matches "over-bet on protection bias" — KB Rule #5 / DO NOT Rule #3 lacks an exception for paired-board / 2-tone-flush-board CHECK lines.

## Per-lane characteristic biases (informational)

Beyond the 3 common failures, each lane has its own characteristic bias on the standard exam:

**Sonnet 4.6** (3 unique failures):
- MW-17 CALL → FOLD (over-fold; AdKs hidden equity on Jd8d4c not credited)
- MW-44 CALL → FOLD (over-fold; Th8h TP+OESD on Ts9h4d7c folded to BB double-barrel)
- (MW-39 already counted as common failure)

Sonnet bias: **over-fold** on marginal pair+draw or pure-overcard spots where pot odds are thin. Sonnet is more conservative in folding range.

**Opus 4.7** (1 unique failure):
- MW-38 CALL → RAISE (over-raise; AhJh nut FD on Kh8h3d facing BB lead — invokes §1.7 too eagerly)

Opus bias: **over-raise** on the §1.7 carve-out spots (nut FD + blocker → RAISE more often than expert).

Net: **Sonnet 5 failures (3 standard + 2 reversal)**, **Opus 4 failures (2 standard + 2 reversal)**. Opus modestly outperforms but neither passes the reversal gate.

## A.4 cost telemetry (A.6 baseline + actuals)

| Component | Estimate | Actual | Halt threshold | Status |
|-----------|----------|--------|----------------|--------|
| Sonnet 4.6 lane | ~$0.40 | ~$0.41 (75K tokens, 80/20 split) | $80 | OK ✓ |
| Opus 4.7 lane | ~$1.50 | ~$2.63 (97K tokens, 80/20 split) | $200 | OK ✓ |
| **A.4 total** | ~$1.90 | **~$3.03** | $200 | OK ✓ |

Costs ~6× **under** orchestrator's $105-195 estimate (single-session-per-lane vs per-hand-per-lane interpretation). Total Phase A spend so far well within $700 envelope; significant remaining budget for revision-cycle dispatch.

## Phase A roll-up

| Sub-phase | Status | Detail |
|-----------|--------|--------|
| A.5 | PASS ✓ | All 5 partial-fold MW fixtures honor live-villain rule (HIGH-1 / S-A12 close) |
| A.1 | PARTIAL | API tier defaulted to Tier 1 per orchestrator Option C (owner console check still pending; non-blocking) |
| A.2 | LOCKED | Sonnet 4.6 (labeller) + Opus 4.7 (high-stakes) per orchestrator pre-spec; Option C tested both for A.4 |
| A.3 | SUBSUMED | Latency derived from A.4 telemetry: ~4.4 min wall-time per 33-hand session = ~8s/hand average; well under 120s/call halt threshold |
| A.4 | **FAIL** | Both lanes fail reversal gate; HARD HALT |
| A.6 | RECORDED | $3.03 actuals; well under all caps |
| A.7 | THIS COMM | HALT verdict + evidence |

## Halt verdict + recommendation

**Verdict:** HARD HALT. Per Option C decision tree row 4 ("FAIL | FAIL | HALT — escalate to owner; reasoning labeller-side, not model-side") and per orchestrator MERGE ACK Halt conditions ("A.4 calibration fails" → HARD halt).

**Pilot Orchestrator does NOT proceed to Phase B.** Phase B dispatch (15 labellers × 100 hands = 1500 calls) would inherit the v3.1 protocol's calibration failure into the entire pilot corpus. Stopping here costs $3.03; proceeding could waste $75-375 on unreliable labels.

**Recommended next steps (orchestrator + owner decision):**

1. **Path A: Protocol/KB revision (cleanest)** — revise v3.1 prompt + KB to:
   - Add a "paired-board exception" to KB Rule #5 / DO NOT Rule #3 (monsters CHECK on paired boards where villain is capped)
   - Tighten KB §1.7 carve-out: nut-FD-RAISE only when fold equity ≥ X% (specify threshold; both Sonnet + Opus invoked §1.7 on Kh8h3d where villain_air=5% i.e. effectively zero fold equity)
   - Add specific commentary on d3688-pattern (BB OOP weak TP on 2-tone-flush board with second villain → CHECK to control pot)
   - Then re-run A.4 with revised v3.2 prompt (~$3 + ~10 min)
2. **Path B: Adjust reversal set** — owner reviews whether d3688 and d9556 expert CHECK labels are themselves correct (per `feedback_solver_vs_expert_labels.md` solver verifies/researches but never overrides expert labels; if owner believes expert labels are right, Path A is needed)
3. **Path C: Accept partial pass for pilot** — relax reversal gate to 8/10 (was 100%); ship the pilot with these 2 known-bad spots flagged for adjudication. Risk: pilot inherits the bias; mitigation: adjudication in Phase F catches them
4. **Path D: Try Protocol B or C instead of A v3.1** — protocols B (composition-first) or C (adversarial elimination) may not exhibit the same failure mode; would need separate calibration runs for each

**My recommendation:** Path A. v3.1 protocol/KB has documented gaps that match `feedback_solver_findings.md` patterns. Revise the protocol once, validate via re-run A.4 (~$3 + 10 min cost), then proceed to Phase B with a clean calibration. Path A is also `feedback_quality_default_no_ask.md`-aligned (slow/clean over fast/loose).

Quick-fix sketch for Path A revision (orchestrator may dispatch builder to draft):

```
KB Rule #5 (monster CHECK exception):
  EXCEPT on paired boards where villain range is heavily capped (no
  trips combos in opener range AND no overpair combos that beat hero's
  monster), CHECK is preferred to extract by inducing later-street
  bluff-catches.

KB §1.7 (nut FD raise tightening):
  Carve-out applies ONLY when villain_air_pct >= 0.20 (genuine fold
  equity). When villain_air_pct < 0.20, nut FD prefers CALL even with
  blocker — fold equity insufficient to justify raise EV.
```

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 44 | Phase A preflight (A.5 PASS + A.4 FAIL) | ⏸️ HALT | Pilot Orchestrator |
| 45 | Phase B-G heavy lift | 🚫 BLOCKED on A.4 | Pilot Orchestrator |
| 47 | Protocol v3.1 → v3.2 revision | 🆕 RECOMMENDED — orchestrator + builder cycle | Orchestrator + Builder |
| 48 | Re-run A.4 with v3.2 prompt | ⏳ QUEUED post-Path-A | Pilot Orchestrator |

## Action

**Owner:**
1. Read this summary + decide between Path A / B / C / D
2. If Path A: greenlight orchestrator to commission v3.2 protocol revision (~30-60 min builder cycle + ~10 min A.4 re-run)
3. If Path C: explicitly authorize relaxed reversal gate (per spec this requires owner override since the 100% reversal rule is hardcoded in `calibration_exam.py` v2.3)

**Orchestrator (main terminal):**
1. Read this summary
2. Confirm or override Pilot Orchestrator HALT (per spec the HALT is mandatory but orchestrator can order specific path)
3. If Path A: dispatch builder for v3.2 revision; on v3.2 merge, re-issue A.4 directive
4. If Path C: issue revised Option C with relaxed reversal gate

**Pilot Orchestrator (this session):**
1. HALT Phase B dispatch (DONE)
2. Surface evidence (this comm; DONE)
3. Standby for orchestrator path-decision
4. On path resolution: re-engage A.4 retry OR proceed to Phase B per relaxed gate OR hand off

**QC stream:**
1. Layer 3 pilot-runtime watch may surface findings on this HALT comm; per spec QC is independent and may produce its own audit
2. Notable QC vector: V-A4-1 = "v3.1 fails Group-D BB-flop CHECK reversals on both Sonnet and Opus" — should be added to QC test corpus for protocol-revision validation

**Builder (if Path A activated):**
1. Receive v3.2 revision directive from orchestrator
2. Edit `prompts/gto_labeller_v3.1.md` → `prompts/gto_labeller_v3.2.md` with KB §1.7 + Rule #5 fixes per recommendation above
3. Standard PR + reviewer cycle
4. On v3.2 merge: Pilot Orchestrator re-runs A.4

## References

- Option C directive: `MAIN_TERMINAL_PILOT_PHASE_A_OPTION_C_DIRECTIVE_2026-04-26.md` (master `439cfd7`)
- Phase A status: `PILOT_PHASE_A_STATUS_2026-04-26.md` (master `70efde6`)
- Calibration exam v2.3: `river-rats-core/calibration_exam.py` (`STANDARD_PASS_THRESHOLD=23`, `GTO_REVERSAL_HANDS` = 10 hands)
- Sonnet results: `review/pilot_run_2026-04-26/calibration_results_sonnet.json`
- Opus results: `review/pilot_run_2026-04-26/calibration_results_opus.json`
- Grading summary (machine-readable): `review/pilot_run_2026-04-26/phase_a4_grading_summary.json`
- Grading key (private): `review/pilot_run_2026-04-26/calibration_grading_key.json`
- Solver findings memory: `feedback_solver_findings.md` (8 findings; over-fold + over-raise patterns documented)
- Quality default memory: `feedback_quality_default_no_ask.md` (Path A is the slow/clean option)

**Status: HARD HALT. A.4 GATE FAIL. Awaiting owner + orchestrator path decision (A/B/C/D). Pilot Orchestrator standing by.**
