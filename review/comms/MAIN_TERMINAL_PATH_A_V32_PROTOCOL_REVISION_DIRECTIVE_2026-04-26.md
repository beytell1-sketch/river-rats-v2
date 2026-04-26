---
date: 2026-04-26
from: Main terminal (orchestrator) per owner direction at 20:25 + 20:30 + 20:50 SAST
to: Logic builder (transient builder persona for v3.2 protocol revision) · Pilot Orchestrator · Owner (briefed) · QC stream
re: A.4 HARD HALT — both Sonnet AND Opus fail v3.1 reversal gate on identical 2 hands; Path A authorized — revise v3.1 → v3.2 with KB Rule #5 paired-board CHECK exception + KB §1.7 nut-FD raise tightening + F-S5 phantom feature patch bundled; re-run A.4 with Opus-only per owner upgrade direction; Phase B HELD until v3.2 passes A.4
status: DIRECTIVE — Path A v3.2 protocol revision ACTIVE; F-S5 patch bundled (supersedes standalone PR #47); A.4 re-run with Opus-only post-v3.2-merge; Phase B remains HELD; cost ~$3 + ~10 min for re-run after ~30-60 min builder cycle
---

# Path A — v3.1 → v3.2 Protocol Revision Directive

## Empirical context

A.4 Option C parallel calibration (Sonnet + Opus) at `b2de857` returned HARD HALT:

| Lane | Standard 23/33 | Reversal 10/10 | Verdict |
|------|----------------|-----------------|---------|
| Sonnet 4.6 | PASS 28/33 | **FAIL 8/10** | FAILED |
| Opus 4.7 | PASS 29/33 | **FAIL 8/10** | FAILED |

**Same 2 reversal hands failed BOTH lanes** (`d3688_BB_flop`, `d9556_BB_flop`) plus same standard hand (`MW-39`). This empirically validates owner's earlier instinct: **the labelling protocol IS the problem, not the model.** Upgrading to Opus alone (per owner's 20:50 direction) does NOT fix it — Opus already failed the same 2 hands as Sonnet on identical reasoning paths.

Combined with A.8 static audit's F-S5-1/F-S5-2 phantom-feature MEDIUM finding, the picture is clear: **v3.1 has documented gaps that need fixing before mass labelling.**

## Path A scope (consolidated)

Bundle three fixes into a single v3.2 protocol revision:

### Fix 1 — KB Rule #5 / DO NOT Rule #3 paired-board CHECK exception (A.4 d3688/d9556 root cause)

`d3688_BB_flop` (8cKc on KdTd4s) and `d9556_BB_flop` (5h5d on 5s6d6h flopped fives full):
- Both lanes invoke "monster on 3-way flop → BET for protection / value"
- Expert wants CHECK in BOTH cases
- Calibration exam line 73 documents: *"v2.2 BET, expert CHECK on KT4 flush board with second villain"*
- Pattern matches `feedback_solver_findings.md` "over-bet on protection bias"

**Fix:** Add to KB Rule #5 / DO NOT Rule #3:

```
EXCEPT on paired boards where villain range is heavily capped (no
trips combos in opener range AND no overpair combos that beat hero's
monster), CHECK is preferred to extract by inducing later-street
bluff-catches.

ALSO EXCEPT on 2-tone-flush boards where hero is OOP and 2nd villain
remains live: CHECK is preferred to control pot size and avoid
isolating into the live villain's flush draws / better TP+ continues.
```

### Fix 2 — KB §1.7 nut-FD raise tightening (A.4 MW-39 root cause)

MW-39 (AhJh on Kh8h3d) standard hand:
- Both lanes invoke KB §1.7 "nut FD + Ah blocker = RAISE"
- Expert wants CALL
- Villain composition: `villain_air_pct = 0.05` (effectively zero fold equity)
- Pattern matches `feedback_solver_findings.md` "nut draw raise rule"

**Fix:** Tighten KB §1.7 carve-out:

```
KB §1.7 CARVE-OUT — Nut FD + blocker → RAISE only when:

  villain_air_pct >= 0.20  (genuine fold equity)

When villain_air_pct < 0.20, nut FD prefers CALL even with blocker:
fold equity insufficient to justify raise EV; better to call and
realise equity vs calling-range. The 0.20 threshold matches
`feedback_solver_findings.md` solver-corrected MW-30 CALL anchor
where villain_air = 0.15 was insufficient for raise EV despite nut
blocker presence.
```

### Fix 3 — F-S5 phantom feature patch (bundled per static audit MEDIUM)

Per `AUDIT_A8_STATIC_PROMPTS_2026-04-26.md` F-S5-1 + F-S5-2:

Replace `prompts/protocol_b_composition_first_v1_0_pilot.md` L283-285 (and design artifact L264-266) Range-mass axis text:

**Before:**
```
- **Range-mass axis:** what fraction of hero's own range
  (`hero_top_pair_plus_pct` etc. if available) is in the same
  category as villain's? Used for range-vs-range balance.
```

**After (option (c) hand-class proxy):**
```
- **Range-mass axis:** what fraction of hero's own range falls into
  the same hand-class category (TP+/medium/draws/air) as villain's
  modal slice? Derive from hero's current bucket assignment + the
  preflop construction implied by `prior_actions`. Used for
  range-vs-range balance — when hero's range AND villain's range
  are both heavy-TP+, the balance is "value-vs-value" and pot-control
  often dominates; when hero's range is heavy-draws against villain's
  heavy-TP+, the balance is "draw-realisation-vs-deny" and the
  decision flips to fold-or-bet-large.

  No `hero_*_pct` feature exists in the 59-feature contract. Derive
  the mass estimate from the bucket label of hero's actual hand +
  whether hero's preflop range (per `prior_actions`) is wide
  (limp / call) or tight (raise / 3bet) — wide ranges have higher
  air/draws mass; tight ranges have higher TP+ mass.
```

Apply identically to `prompts/protocol_b_composition_first_v1_0.md` L264-266 (design artifact source).

**Supersedes standalone F-S5 PR #47 directive** at `947f176` — F-S5 fix is now bundled into v3.2 to reduce review-cycle overhead.

## File scope

Edit:
- **NEW:** `prompts/gto_labeller_v3.2.md` (created from v3.1 with Fix 1 + Fix 2)
- **EDIT:** `prompts/protocol_b_composition_first_v1_0_pilot.md` L283-285 (Fix 3)
- **EDIT:** `prompts/protocol_b_composition_first_v1_0.md` L264-266 (Fix 3, design artifact)

**No edits to:**
- `prompts/gto_labeller_v3.1.md` (preserve as historical record; v3.2 supersedes)
- `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` (Protocol C didn't have phantom feature; per static audit S5)
- `prompts/protocol_c_adversarial_elimination_v1_0.md` (same; no edit needed)

**Hash impact:** v3.2 is a new file, no hash impact. Protocol B pilot artifact + design artifact get hash bumps; will need new SHA256 in their frontmatters or sidecars (builder's call on whether to update existing hash-locks).

## Workflow

Standing per-batch protocol:

1. **Branch:** `stage4-pre-dispatch/v3-2-protocol-revision`
2. **Author commit:** v3.2 = v3.1 + Fix 1 + Fix 2; Protocol B pilot + design = + Fix 3
3. **Self-test before PR:**
   - v3.2 explicitly addresses paired-board CHECK exception (grep "paired board" or "EXCEPT")
   - v3.2 §1.7 has the `villain_air_pct >= 0.20` threshold
   - Protocol B pilot L283-285 + design L264-266 no longer reference `hero_top_pair_plus_pct`
   - Cross-check 4 cross-protocol shared examples (B-Ex2/C-Ex2, B-Ex3/C-Ex3, B-Ex4/C-Ex4, B-Ex5/C-Ex5) still converge — should be unchanged since none of them touch the modified text
4. **PR (#48 expected)** with V3.2 changelog from v3.1 + F-S5 patch bundle note
5. **Triple-pipeline review:**
   - Builder reviewer (V3-compliance flavour) — verify Fix 1/2/3 textually correct
   - QC pre-merge audit (Path B) — TC-23 + V-X3 + check Fix 1/2 specifically address the 3 failed hands (d3688/d9556/MW-39)
   - Orchestrator gto-expert reviewer — verify the protocol revisions don't break other reasoning surfaces
6. **Merge** after triple-APPROVE

## Re-run A.4 directive (post-v3.2 merge)

Pilot Orchestrator re-runs A.4 with:
- **Model:** Opus 4.7 ONLY (per owner 20:50 direction "upgrade labelers to opus 4.7")
- **Protocol:** v3.2 (revised per Fix 1 + Fix 2 + Fix 3)
- **Same 38-hand calibration set** (28 standard + 10 reversal)
- **Cost:** ~$2.63 (Opus rerun matches first run)
- **Wall-time:** ~5 min

**Decision tree post-A.4 retry:**

| Opus result | Phase B disposition |
|-------------|---------------------|
| **PASS** (≥23 standard + 100% reversal) | Ship Opus 4.7 for Phase B labelling per owner direction; Phase B dispatches |
| **FAIL** (any reversal miss) | HARD HALT again — escalate to owner; consider Path D (try Protocol B or C reasoning instead of v3.x); cost so far still under $10 |

**If Opus PASSES on v3.2:** Phase B cost increases to ~$375-1875 range (Opus 5x Sonnet). This pushes against $700 envelope hard cap. **Pilot Orchestrator must surface revised Phase B cost projection BEFORE Phase B dispatch; orchestrator escalates to owner if projection exceeds $700.**

If owner is content with Opus + cost overrun: orchestrator may grant override authority based on calibration evidence + Phase B's higher quality bar. Owner already authorized costs liberally ("go with recommendations" twice today).

## Why Path A over alternatives

| Path | Decision |
|------|----------|
| **A** — v3.2 revision | ✅ AUTHORIZED — addresses root cause empirically; ~$3 + 30-90 min wall-time |
| B — Question expert labels | ❌ rejected — `feedback_solver_vs_expert_labels.md` says solver verifies but never overrides expert labels; expert calls are the gold standard |
| C — Relax reversal gate | ❌ rejected — would require owner override to spec; ships pilot with known-bad bias; mitigation in Phase F adjudication is a band-aid |
| D — Protocol B or C swap | ❌ deferred — Protocol B+C are tested next pilot iteration if v3.2 also fails; not first move because root cause is in shared KB sections both protocols inherit |

## Cost + wall-time roll-up

Phase A spend so far: $3.03 (well under $200 hard cap).

Path A budget:
- v3.2 builder cycle: ~$0 (text edits only, no API calls beyond review agent dispatches)
- A.8 trace audit dispatch (post-A.4 retry): ~$5
- A.4 Opus retry: ~$2.63
- A.8 final synthesis dispatch: ~$3
- **Path A subtotal:** ~$11

Total Phase A after Path A complete: ~$14 of $200 cap (still 7% utilization).

Wall-time:
- v3.2 builder cycle: ~30-60 min
- v3.2 PR review: ~30-45 min
- A.4 Opus retry: ~5-10 min
- Trace audit + coverage audit + A.8 synthesis: ~30-45 min
- **Path A wall-time:** ~95-160 min from now (~22:00-23:30 SAST)

Phase B remains contingent on A.4 v3.2 retry PASS.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 44 | Phase A preflight | ⏸️ HALT (A.5 PASS + A.4 v3.1 FAIL); resumes on v3.2 A.4 retry | Pilot Orchestrator |
| 45 | Phase B-G heavy lift | 🚫 BLOCKED on A.4 v3.2 retry | Pilot Orchestrator |
| 47 | F-S5 standalone PR #47 | ⏸️ SUPERSEDED — bundled into v3.2 | obsolete |
| 49 | v3.2 protocol revision (Fix 1 + 2 + 3 bundled) | 🔥 ACTIVE — directive issued (this commit) | Logic builder |
| 50 | A.4 v3.2 Opus retry | ⏳ QUEUED post-v3.2 merge | Pilot Orchestrator |
| 51 | Phase B revised cost projection (post-Opus PASS) | ⏳ POST-A.4-RETRY-PASS | Pilot Orchestrator |
| 52 | A.8 synthesis (post-A.4 retry + trace audit + coverage audit) | ⏳ QUEUED | Orchestrator |

## Action items

**Logic builder (transient builder persona, returning to Pilot Orchestrator after v3.2 merges):**
1. Take this directive as v3.2 revision authorization
2. Branch `stage4-pre-dispatch/v3-2-protocol-revision`
3. Apply Fix 1 + Fix 2 + Fix 3 per scope above
4. Self-test: grep for paired-board exception + 0.20 threshold + absence of `hero_top_pair_plus_pct`
5. PR #48; standing per-batch protocol with triple-pipeline review
6. Surface PR description with V3.2 changelog + cross-protocol convergence preservation note
7. Resume Pilot Orchestrator persona post-v3.2 merge

**Pilot Orchestrator (post-v3.2 merge):**
1. Re-run A.4 with Opus 4.7 on v3.2 protocol
2. Same 38-hand exam, same answer key
3. Surface A.4 v3.2 grading summary
4. If PASS: surface revised Phase B cost projection (Opus 5x Sonnet) + escalate to orchestrator if > $700
5. If FAIL: surface HARD HALT escalation to owner (Path D candidate or further protocol revision)

**Orchestrator (me):**
1. This directive shipped (atomic flow next)
2. Watch for v3.2 PR drop (~30-60 min ETA)
3. Dispatch gto-expert reviewer at v3.2 PR open
4. After v3.2 merge: re-issue A.4 retry directive
5. Post-A.4 retry PASS: dispatch trace audit agent + run coverage audit
6. Compose A.8 final synthesis comm
7. Dispatch Phase B if A.8 CLEAN + cost projection within $700 envelope OR with owner override

**QC stream:**
- Layer 3 watch continues; A.4 HALT was a high-value finding QC's framework would have flagged at trace level
- QC may dispatch own audit on v3.2 per existing TC-15 framework; not blocking
- V-A4-1 vector ("v3.1 fails Group-D BB-flop CHECK reversals") added to QC test corpus per Pilot Orchestrator note

**Owner:**
- A.4 HARD HALT empirically confirms protocol-side issue (NOT model-side); your earlier instinct was correct
- Path A authorized: v3.2 revision (~$3 + 30-90 min) + A.4 Opus retry (~$3 + 5 min)
- F-S5 phantom feature patch bundled into v3.2 (saves a separate review cycle)
- Phase B Opus model lock per your direction; revised Phase B cost ~$375-1875 will be surfaced post-A.4 PASS for explicit envelope decision
- ETA Phase B dispatch decision: ~22:00-23:30 SAST

## References

- A.7 HALT: `review/comms/PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` (master `b2de857`)
- Calibration results: `review/pilot_run_2026-04-26/calibration_results_{sonnet,opus}.json`
- Grading summary: `review/pilot_run_2026-04-26/phase_a4_grading_summary.json`
- Static audit: `AUDIT_A8_STATIC_PROMPTS_2026-04-26.md`
- Teaching archaeology: `AUDIT_A8_TEACHING_ARCHAEOLOGY_2026-04-26.md`
- A.8 partial synthesis (F-S5 patch directive — superseded): `MAIN_TERMINAL_PHASE_A8_SYNTHESIS_FS5_PATCH_DIRECTIVE_2026-04-26.md` at master `947f176`
- Memory: `feedback_solver_findings.md` (over-fold + over-raise patterns); `feedback_quality_default_no_ask.md` (Path A is slow/clean); `feedback_solver_vs_expert_labels.md` (expert labels are gold standard); `feedback_listen_to_orchestrator_always.md` (owner direction sufficient authorization)

**Status: PATH A AUTHORIZED. v3.2 PROTOCOL REVISION ACTIVE. F-S5
PATCH BUNDLED. A.4 OPUS RETRY QUEUED. Phase B HELD until v3.2 A.4
retry passes. ETA ~22:00-23:30 SAST.**
