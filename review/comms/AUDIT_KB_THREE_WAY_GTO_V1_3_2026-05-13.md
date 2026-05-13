# AUDIT — `knowledge/three_way_gto.md` v1.3 Runtime Worked Examples

**DATE:** 2026-05-13
**AUDITOR:** Orchestrator (Explore agent — independent audit)
**SCOPE:** Knowledge base v1.3 (2026-04-10) which gets runtime-appended to `prompts/gto_labeller_v3.4.md` per prompt lines 97-100. Previous audit (v3.4 prompt latent issues, 2026-05-13) could not access these; flagged as potential BLOCKER.
**SUMMARY:** 10 issues; **2 BLOCKERS**; 5 SHOULD_FIX; 3 NOTE. Verdict: **Yes-with-BLOCKER-fix** for 4-way runtime use. KB is out of sync with v3.4 prompt patches and shares the corpus' empty strata (river, facing-raise, sandwich).

---

## BLOCKER 1 — KB §1.7 carve-out has not been updated for v3.2/v3.3/v3.4 prompt patches

**EVIDENCE:** `knowledge/three_way_gto.md:97-124` (§1.7, finalised 2026-04-10) teaches the BASE carve-out: "nut FD + blocker → RAISE." Subsequent prompt patches add three override thresholds that the KB does NOT mention:

| Override | Prompt v3.4 lines | What it changes | KB v1.3 status |
|---|---|---|---|
| v3.2 Fix 2 | 805-806 | Gate: `villain_air_pct >= 0.20` required for RAISE | **absent** |
| v3.3 Fix 2.1 | 841-878 | Suspension: 0.20 gate relaxed in bet+call multiway lines; 35% equity threshold | **absent** |
| v3.4 Fix 2.1.1 | 880-909 | Floor: `villain_air_pct >= 0.05` for bet+call lines | **absent** |

**WHY IT MATTERS:** Labellers at runtime read PROMPT + KB. The prompt's Calibration Notes teach the overrides; the KB teaches the base rule. They see **contradictory guidance**. A labeller who relies on the KB section without reading the prompt's Calibration Notes will mis-apply §1.7 — RAISE in spots where the override prohibits.

This BLOCKER compounds the v3.4 prompt audit BLOCKER 1 (which calls for consolidating the 3-layer overrides into a single rule in the prompt). Once consolidated in the prompt, the KB must be re-synced to match.

**FIX (for v3.5 / KB v1.4):**

Two-part fix:
1. v3.5 prompt consolidates the 3-layer overrides into a single decision rule (per v3.4 audit BLOCKER 1)
2. KB v1.4 §1.7 mirrors the consolidated rule verbatim, with 3 worked examples spanning the override conditions

---

## BLOCKER 2 — Critical strata missing from worked examples (mirrors corpus gap)

**EVIDENCE:**

| Stratum | KB v1.3 examples | Corpus (350 hands) | Severity |
|---|---|---|---|
| **River decisions** | 0 of 9 examples | 0 of 350 hands | matched gap |
| **Facing-raise (bet+raise)** | 0 of 9 examples | 0 of 350 hands | matched gap |
| **Sandwich position** | 0 of 9 examples | unmeasured | KB gap |
| **Strong-made bucket (TPGK, overpair, two pair)** | 0 of 9 | n/a | KB gap |
| **Air bucket (pure bluffs)** | 0 of 9 | n/a | KB gap |

**WHY IT MATTERS:** Labellers were never taught how to label facing-raise, river, or sandwich hands — so corpus generators never produced them, and the KB never illustrated them. The gap is architectural, not statistical.

**FIX (for v3.5 / KB v1.4):**

Add 6 new worked examples to §4:
- **Example 13** — River check-raise (MW-31 pattern): BB faces SB check-raise; trips+ = CALL
- **Example 14** — River checked-to (d3178 pattern): AA on JQ paired board; monster checked-to = BET
- **Example 15** — Sandwich facing bet (multiway middle-position): TPGK facing UTG c-bet with players behind = CHECK to preserve optionality
- **Example 16** — Facing raise (bet-call-raise sequence): hero faces CO raise after BTN called UTG bet; nut hand = RAISE
- **Example 17** — Strong-made bucket (overpair on dry board IP): AA on K-7-2 rainbow facing check; BET 33% for value
- **Example 18** — Air bucket (overcards alone on missed board): AK on T-7-4 OOP multiway; CHECK and surrender

---

## SHOULD_FIX issues (5)

### 3. Worked examples don't teach the three KB §1.7 overrides

**EVIDENCE:** Example 9 (nut draw with blocker → RAISE, KB lines 1111-1151) demonstrates the BASE §1.7 rule but does not show: a hand below the 0.20 air threshold; a hand in the v3.3 suspension zone; a hand below the 0.05 floor.

**FIX:** Add 3 worked examples (re-using slots 13-15 from BLOCKER 2 fix or new slots):
- MW-39 pattern (HU bet, 0.05 air): CALL (gate blocks)
- MW-47 pattern (bet+call, 0.15 air): RAISE (suspension applies)
- PILOT_600 pattern (bet+call, 0.02 air): CALL (floor blocks)

### 4. Example 1 uses outdated terminology / composition language

**EVIDENCE:** KB:762-785. Example 1 says "villain_air_pct ~0.25 (moderate)" then invokes "BTN flat range excludes AA/KK/QQ/AKs, but CO open range still contains AK and KK" — preflop range structure instead of postflop composition triple per §1.9.

**FIX:** Rewrite Example 1 reasoning to cite the composition triple buckets explicitly (e.g., "villain_top_pair_plus_pct ≈ 0.35 = §1.9 medium bucket — meaningful value but mostly weaker holdings").

### 5. Example 4 references Example 6 which uses threshold-based reasoning

**EVIDENCE:** KB:677-678 (Example 4) cites "KB Example 6 as 'low villain TP+ + high air → bet'" in DO NOT Rule 11. But Example 6 (KB:977-1030) reasons threshold-style on composition triple. The same reasoning is flagged as a failure mode for paired/2-tone boards (Rule 11) but taught as correct for dry rainbow boards.

**FIX:** Add teaching note to Example 6 distinguishing dry vs paired/2-tone applicability: "This reasoning is correct on DRY boards but FAILS on PAIRED or 2-tone OOP multiway (Rule 11 exception). The difference: dry boards don't trap hero in larger pots when called; 2-tone/paired boards do."

### 6. Multiple examples lack explicit bucket classification

**EVIDENCE:** Examples 1, 2, 7, 8 do not state "This is a [bucket] hand" as required by prompt v3.4 Step 1 (line 224).

**FIX:** Add one sentence to top of each example's "Factors" section: "**Hand bucket:** [monster/strong_made/medium_made/weak_made/drawing/air]."

### 7. DO NOT Rule coverage incomplete

**EVIDENCE:** 6 of 11 DO NOT Rules lack worked examples:

| Rule | Covered? | Gap |
|---|---|---|
| 3 (check ≠ nothing) | NO | Needs check-raise scenario |
| 4 (don't auto-c-bet IP) | PARTIAL | Needs IP-check-decision example |
| 7 (street-plan reasoning) | PARTIAL | Needs explicit street_plan_tags example |
| 9 (range_capped misuse) | PARTIAL | Needs counter-example |
| 10 (HRP=0.00 = artifact) | NO | No examples flag HRP artifact |
| 11 (don't auto-bet on paired/2-tone OOP) | PARTIAL | Needs monster-on-paired-OOP → CHECK example |

**FIX:** Add 6 examples covering Rules 3, 4, 7, 9, 10, 11. (Note: Example 20 from BLOCKER 2's Example 15 covers Rule 11.)

---

## NOTE issues (3)

### 8. Bucket coverage skew

**EVIDENCE:** Strong-made 0%, Air 0%, Monster 22%, Medium-made 44%, Weak-made 11%, Drawing 22%.

**FIX:** Examples added under BLOCKER 2 fix (Strong-made → Example 17; Air → Example 18) address this.

### 9. Position coverage skew

**EVIDENCE:** Sandwich 0%, OOP 44%, IP 33%.

**FIX:** Example 15 (Sandwich) under BLOCKER 2 addresses this.

### 10. Solver-as-reasoning controlled, but Examples 1 and 6 lack solver-verification annotation

**EVIDENCE:** Examples 3, 8, 9 cite solver as verification (correct usage). Examples 1, 6 don't note whether the action is solver-verified.

**FIX:** Add "Solver verification: [confirmed in range / not needed (clear from bucket+composition)]" to Examples 1 and 6.

---

## What PASSES (no fix needed)

- No illegal-action predictions in any example
- No outdated v3.1/v3.2/v3.3 feature references
- Solver usage is generally correct (verification-mode, not labelling-source)
- Bucket-first protocol is taught (Examples 3, 4, 6 follow it)

---

## VERDICT

**Fitness for purpose:** **Yes, with BLOCKER fix**

The KB provides solid conceptual foundations and 9 worked examples demonstrating core principles. However:

1. KB §1.7 is **out of sync with v3.4 prompt** — labellers reading both see contradictory guidance (BLOCKER 1)
2. KB has the **same architectural blind spots as the corpus** — no river, no facing-raise, no sandwich (BLOCKER 2)

Both are fixable in a coordinated v3.5 prompt + v1.4 KB update. The fixes are scoped: ~2-3 hours of architect time per the agent's estimate.

---

## Phase 2-F integration

This audit feeds into Phase 2-F Task **A2c** (NEW — KB v1.4 update). The architect MUST:

1. Coordinate A2b (prompt v3.5) and A2c (KB v1.4) so §1.7 consolidation is reflected in both
2. Add 6 new worked examples per BLOCKER 2 (3 hr effort)
3. Add 6 examples per SHOULD_FIX 7 covering missing DO NOT Rules
4. Revise Examples 1, 4, 6 per SHOULD_FIX 4, 5, 6

**Per `docs/PROCESS_GUIDE.md` §2.3:** Re-calibration is **mandatory** after any KB change. This locks in the new B0 calibration task before B2 pilot fires.

---

## Audit confidence

This audit is **READ-ONLY** independent review. No code modified. Findings based on KB text analysis against memory rules and v3.4 prompt cross-reference. Architect should validate against actual runtime concatenation (prompt + KB) before committing v3.5/v1.4.
