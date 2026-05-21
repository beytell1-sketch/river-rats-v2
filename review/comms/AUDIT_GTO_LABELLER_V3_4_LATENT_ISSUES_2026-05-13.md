# AUDIT — `prompts/gto_labeller_v3.4.md` Latent Issues

**DATE:** 2026-05-13
**AUDITOR:** Orchestrator (Explore agent — independent audit)
**SCOPE:** Latent issues in v3.4 prompt beyond positional-diversity (audited separately)
**SUMMARY:** 11 issues identified; 3 BLOCKERS; 4 SHOULD_FIX; 4 NOTE. Verdict: **Yes-with-fixes** for 4-way labelling. Top 3 issues feed into Phase 2-F Task A2b (prompt v3.5 rewrite).

---

## BLOCKER 1 — KB §1.7 3-Layer Override Patches

**EVIDENCE:** `prompts/gto_labeller_v3.4.md:792-909` — three layered patches on top of the same rule:
- v3.2 Fix 2 (lines 792-839): `villain_air_pct >= 0.20` threshold
- v3.3 Fix 2.1 (lines 841-876): suspends 0.20 threshold in bet+call multiway; requires `villain_call_count >= 1`
- v3.4 Fix 2.1.1 (lines 880-909): adds floor `villain_air_pct >= 0.05` to the v3.3 carve-out

**WHY IT MATTERS:** The rule is no longer "nut FD + blocker → RAISE". It is "nut FD + blocker → RAISE UNLESS [v3.2 condition] UNLESS [v3.3 exception] UNLESS [v3.4 floor]." A labeller navigating this 3-tier conditional tree is reasoning from rules, not poker principles — and it is the exact pattern (`if/elif` chains) prohibited by `data/4way_labeller_brief.md:11-17`.

**FIX (for v3.5):**

Consolidate into a single decision rule:

> **KB §1.7 SEMI-BLUFF RAISE (nut FD + blocker):** Apply when (1) hero has nut flush draw + ace blocker, (2) villain has sufficient fold equity (`villain_air_pct >= 0.05` in HU bet; `>= 0.05` in bet+call multiway with `call_count >= 1`), AND (3) hero has >=35% equity vs continuing range. In pure chip-check spots (`villain_air < 0.05`), prefer CALL to realize equity.

---

## BLOCKER 2 — Solver-as-Reasoning Conflation

**EVIDENCE:** `prompts/gto_labeller_v3.4.md`
- Line 12 (preamble): references "solver-verified" as labelling justification
- Line 811: "feedback_solver_findings.md solver-corrected MW-30 CALL anchor"
- Line 816: "raise EV... clears the EV threshold per solver simulations"
- Line 846: "solver-verified RAISE per reference_corrections.md"

**WHY IT MATTERS:** Violates `feedback_solver_vs_expert_labels.md`: solver verifies, never labels. The prompt teaches labellers to reason from "the solver says this is +EV" rather than from poker principles (range composition, fold equity geometry, board texture). This inverts the relationship and degrades label quality — labellers anchor on solver outputs instead of independent judgement.

**FIX (for v3.5):**

1. Remove all solver-EV-calculation references from the prompt's *reasoning guidance*
2. Move solver outputs to **Calibration Notes** as **post-hoc anchors only** (not teaching examples)
3. Reframe `villain_air_pct` thresholds as poker-first principles:
   - Before: "raise EV clears threshold per solver simulations"
   - After: "Fold equity only materializes if villain has fold-candidate hands. Below 0.20 air, fold equity is marginal regardless of draw strength."

---

## BLOCKER 3 (was SHOULD_FIX, promoted) — DO NOT Rule 11 Threshold Logic

**EVIDENCE:** `prompts/gto_labeller_v3.4.md:708-726`

Rule contains hardcoded equity-adjacent decision logic:
- Line 718: `villain_top_pair_plus_pct >= 0.40` acts as a threshold
- Line 720: hand strength predicates (`is_strong_made = 1 OR is_monster = 1`) function as equity proxies
- Decision tree is threshold-based: "default to CHECK UNLESS both (a) AND (b) OR (c) fire"

**WHY IT MATTERS:** Directly violates the anti-threshold principle at lines 93-94 ("No single number determines the correct action") and `feedback_bucket_first_labelling.md` (no equity thresholds in labelling prompt; thresholds live in `spot_classifier.py`).

**FIX (for v3.5):**

Convert to qualitative guidance:

> Prefer CHECK on paired/2-tone OOP multiway. Override to BET only when villain's continuing range is value-heavy (TP+ dominant, low draw density) AND hero has genuine strength to extract, OR the board + action history create river-checked-to override (d3178 pattern).

Remove the predicate checklist; ground decisions in reasoning.

---

## SHOULD_FIX issues (4)

### 4. Equity-threshold leakage in Calibration Notes

**EVIDENCE:** `prompts/gto_labeller_v3.4.md:764-768` (MW-30 anchor): "solver-verified: 40% equity vs 18% pot odds, composition shows <40% TP+" — quantifies decision via equity comparison rather than poker reasoning.

**FIX:** Rewrite calibration anchors to show range composition + equity realization reasoning, not solver-output thresholds.

### 5. Solver-aligned sizing constraint missing

**EVIDENCE:** Line 132 references "Default sizing 25-33% pot" but does not enforce solver-aligned buckets (flop 25%/66%, turn 33%/75%, river 33%/75%/150% per `feedback_solver_aligned_sizing.md`).

**FIX:** Add explicit sizing-bucket teaching under Step 3.

### 6. Bucket-first compliance not enforced in output schema

**EVIDENCE:** Step 1 (lines 190-224) requires bucket-first, but `reasoning` field schema (line 586) does NOT enforce ordering. Labeller could write action-first reasoning and backfill the bucket.

**FIX:** Add to schema: `reasoning field MUST start with "This is a [bucket] hand." All subsequent reasoning flows from the bucket.`

### 7. KB §1.7 wording: "Default to..." vs "ONLY BET IF BOTH..."

**EVIDENCE:** Line 717 conflates probabilistic guidance ("Default to CHECK") with deterministic predicates ("ONLY BET if BOTH").

**FIX:** Pick one framing. Recommended: qualitative (per BLOCKER 3 fix).

---

## NOTE issues (4)

### 8. Failure-direction classification structure missing

**EVIDENCE:** No `reasoning_direction` field. Trainer reports cannot post-hoc classify misses as under-aggression vs over-aggression vs class-collapse per `feedback_failure_direction_classification.md`.

**FIX:** Add optional/mandatory `reasoning_direction` field for difficulty >= 2 hands.

### 9. Hand-strength composition triple not explicit

**EVIDENCE:** Lines 234-249 use composition quad correctly but do NOT state: "derive hand strength from the triple (TP+/draws/air), NOT from preflop range labels."

**FIX:** Add explicit teaching in Step 2.

### 10. Multi-villain range tracking not enforced

**EVIDENCE:** Prompt uses singular "villain" framing; does not enforce per-villain bucket reasoning in 3-way/4-way scenarios.

**FIX:** Add to Step 2: "In 3-way+, opponents are asymmetric. Do NOT treat both opponents identically." (This will overlap with Phase 2-F positional-chain amendment.)

### 11. Worked examples absent from prompt body

**EVIDENCE:** Lines 97-100 reference examples appended at runtime from `knowledge/three_way_gto.md`. Audit could not verify examples follow all 11 DO NOT rules.

**FIX (or verify):** Confirm runtime-loaded examples demonstrate all 11 DO NOT Rules. If not, supplement.

---

## VERDICT

**Fit for purpose (4-way labelling):** **Yes-with-fixes**

The prompt establishes a sound bucket-first protocol and correctly reframes multiway decision-making. The composition-quad guidance is valuable. However, the prompt has absorbed solver-verification references and threshold-based decision trees that subtly teach rule-based reasoning — the exact pattern the brief prohibits.

**Deployable for 3-way:** if BLOCKERS 1-3 are fixed before use.

**Deployable for 4-way (Phase 2-E):** the existing batches 001-008 were labelled under v3.4. Drift will be measured in the re-label consistency audit (Phase 2-F Task B2).

---

## Phase 2-F Integration

This audit feeds into Phase 2-F Task A2b (prompt v3.5 rewrite). The architect MUST address BLOCKER 1, 2, 3 in v3.5 alongside the positional-chain amendment. SHOULD_FIX items 4, 5, 6 are recommended but not blocking. NOTE items 8-11 are deferred to v3.6 unless architect determines they're trivial to bundle.

---

## Audit confidence

This audit is **READ-ONLY** independent review. No code modified. No verification ran (e.g., did not test that labellers actually fail FL5 illegal-action checks). Findings are based on prompt text analysis against memory rules. Architect should validate findings against actual labelling runs before committing v3.5.
