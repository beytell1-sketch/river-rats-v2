---
date: 2026-04-26
from: Builder reviewer (V3-compliance + ml-architect flavor; general-purpose subagent under reviewer persona)
to: Main terminal (orchestrator) · Owner · Pilot Orchestrator
re: Independent review on PR #47 — v3.2 protocol revision (Fix 1 + Fix 2 + Fix 3 bundled)
status: REQUEST-CHANGES
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/47
branch: stage4-pre-dispatch/v3-2-protocol-revision
commit: 621567e
---

# Review Verdict — PR #47 (v3.2 protocol revision)

## Verdict

**REQUEST-CHANGES** — Fix 2 and Fix 3 are textually correct and empirically adequate; Fix 1 (DO NOT Rule 11) is textually well-formed but its **decision-rule predicate structurally fails to match d3688_BB_flop**, which is one of the two reversal hands the rule was designed to fix. v3.2 will plausibly resolve d9556 + MW-39 but is **at material risk of failing d3688 again** because the predicate gates on `is_strong_made = 1 OR is_monster = 1`, while d3688's hero hand (TPWK) is `is_strong_made = 0` and `is_monster = 0`. Fix needed before A.4 v3.2 retry.

## Per-dimension results

### V1. Fix 1 textual correctness — CONDITIONAL

**Rule 11 narrative (lines 669-718) PASSES the cosmetic checks:**
- Title explicitly addresses "paired or 2-tone-flush boards OOP with multiple live villains"
- Includes BOTH the paired-board EXCEPT clause (L681-687) AND the 2-tone-flush OOP ALSO EXCEPT clause (L689-696) per directive
- Has explicit carve-outs: HU spots (L708), IP spots (L709), dry boards (L710), river-checked-to including d3178 (L711)
- Cross-references DO NOT Rule 5 (TP medium-strength) at L713-718

**However, Rule 11 has a STRUCTURAL DEFECT in the decision rule (L699-705):**

```
- Hero hand class is `is_strong_made = 1` OR `is_monster = 1`
  (set+, two pair, overpair, top pair top kicker on dry board)?
```

The predicate excludes `is_made_hand = 1 AND is_strong_made = 0` (i.e., medium-made = TP weak kicker, second pair, pocket pair below top card per the bucket taxonomy at L205-208). Per the v3.2 feature contract:
- `is_strong_made` = 1 if two pair or better (L475)
- `is_monster` = 1 if set or better (L476)

**The narrative title also reinforces this scoping** — "DO NOT auto-bet **strong-made hands**". Medium-made is not in the rule's ambit.

**This means Rule 11 routes d9556 (monster on paired board) to CHECK correctly, but does NOT route d3688 (TPWK on 2-tone board) to CHECK** — d3688 is medium-made by the bucket taxonomy and the labeller's own assessment. See V7 walkthrough.

### V2. Fix 2 textual correctness — PASS (with NIT)

KB §1.7 OVERRIDE section (L758-800) is textually well-formed:
- Explicit `villain_air_pct >= 0.20` threshold present (L771, L787, L789)
- Rationale anchors to MW-30 solver-corrected anchor where `villain_air = 0.15` was insufficient (L777-782)
- Notes that v3.2 supplements (does NOT edit) standalone KB file `knowledge/three_way_gto.md` §1.7 (L765-768, L792-794)
- Decision rule explicitly handles `villain_air_pct < 0.20` → CALL preferred (L789-790)
- MW-39 walkthrough (V7 below) confirms the OVERRIDE routes correctly

**NIT:** Decision rule L785 references feature `nut_flush_block` which does NOT exist in the 54-feature contract (L459-516). The closest real feature is `flush_block_pct` (#46). A labeller checking the predicate strictly might be confused. The narrative motivating example does not depend on this feature, so the OVERRIDE will likely still fire on MW-39 via narrative pattern match — but the cited feature name is non-canonical.

### V3. Fix 3 textual correctness — PASS

Both pilot artifact (L283-297) and design artifact (L264-278) PASS:
- Phantom feature `hero_top_pair_plus_pct` removed from BOTH files (grep count = 0/0)
- Replacement uses hand-class proxy (TP+/medium/draws/air bucket-derived) per directive option (c)
- References `prior_actions` for preflop construction — `prior_actions` is real per the protocol's referenced feature contract
- Explicitly states "No `hero_*_pct` feature exists in the 59-feature contract" per directive
- Replacement text in pilot artifact is **byte-identical** to design artifact (verified with `diff` of L283-302 pilot vs L264-283 design — empty diff)

### V4. Cross-protocol convergence preserved — PASS

- v3.2 changes do NOT touch `knowledge/three_way_gto.md` (verified: `git diff 5cc7ba1 621567e -- knowledge/` returns empty). Worked Examples 1-9 preserved verbatim.
- Protocol B pilot edit is ONLY at Range-mass axis (L283-302); 2 lines removed, 14 added; no other changes in file (verified via `git diff` line counts: 14 additions, 2 deletions match the Range-mass replacement scope)
- Protocol B Examples 1-5 (the design's 5 worked examples — no "B-Ex" prefix in this file but functionally equivalent) untouched, located at L861+ (well outside the L283-302 edit window)
- Protocol C pilot + design NOT in this PR (verified: `git diff` returns empty for both Protocol C files)

### V5. Numbering integrity — PASS (with NIT)

- v3.1 has 10 DO NOT Rules (1-10); v3.2 has 11 (1-11). No duplicate Rule 11.
- v3.2 changelog at L11 explicitly notes the v3.1 numbering compaction + the v3.2 Rule 11 fresh-slot status: *"v3.1 numbering compacted v3's Rule 11 §3.B to Rule 10; this v3.2 Rule 11 is a fresh slot, not a revival"*

**NIT:** v3.2 changelog L15 says *"All v3.1 features, KB references, **DO NOT Rules 1-11**, output schema..."* preserved from v3.1 — but v3.1 only had Rules 1-10. Should read "DO NOT Rules 1-10 from v3.1, plus the new Rule 11" or similar. Minor wording inconsistency, no semantic impact.

The v3 → v3.1 changelog text (L41) referencing "DO NOT Rule 11 (§3.B)" was correctly carried over verbatim — the empirical context note in the directive flags this as historical (about v3 → v3.1, not the new Rule 11). v3.2's new note at L11 disambiguates.

### V6. Self-test independent verification — PASS

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| `EXCEPT` count in v3.2 | ≥2 (paired + 2-tone) | 2 | ✓ |
| `paired` (case-insensitive) count in v3.2 | substantial | 10 | ✓ |
| `0.20` count in v3.2 | ≥4 | 9 | ✓ |
| `hero_top_pair_plus_pct` in Protocol B pilot | 0 | 0 | ✓ |
| `hero_top_pair_plus_pct` in Protocol B design | 0 | 0 | ✓ |
| `hero_top_pair_plus_pct` in v3.2 | ≥1 (changelog mention) | 1 (L18 changelog) | ✓ |
| Line count v3.2 vs v3.1 | ~110 increase | 730 → 845 = +115 | ✓ |
| Files changed in PR | 3 (v3.2, B-pilot, B-design) | 3 (verified) | ✓ |

### V7. Empirical adequacy — CONDITIONAL (FAIL on d3688)

**Trace under v3.2 with actual feature values from `calibration_exam_payload.json`:**

#### d3688_BB_flop (8cKc on KdTd4s; expert CHECK; reversal)

Features:
- `is_made_hand=1, is_strong_made=0, is_monster=0` (medium-made: TPWK)
- `is_ip=0` (BB OOP)
- `is_paired=False` (KdTd4s — NO pair)
- 2-tone-flush: yes (Kd, Td both diamonds)
- `num_opponents=2`
- `villain_top_pair_plus_pct=0.198, villain_air_pct=0.338`

**Rule 11 decision-rule walk (L698-705):**
1. "Hero hand class is `is_strong_made = 1` OR `is_monster = 1`?" → BOTH = 0 → **PREDICATE FAILS**
2. Rule 11 doesn't trigger.

**Fallback to v3.1 reasoning** (which is what produced the v3.1 BET failure on Sonnet AND Opus): the labeller still has Rule 5 (TP is medium-strength → pot-control) but ALSO has KB Example 6 reasoning (low TP+ + high air → bet). v3.1 Sonnet's reasoning explicitly cited "Per KB Example 6 reasoning: when villain_top_pair_plus_pct is in the <20% bucket and villain_air_pct is high (0.34), OOP betting is justified." Opus likewise: "with composition thin on value, donk/lead small (25-33%) for protection."

**Nothing in v3.2 contradicts the Example 6 reasoning that produced the v3.1 BET error.** Rule 11 was the only structural change; its predicate excludes this hand. There is a high probability d3688 fails again under v3.2.

**This is a HIGH severity finding.**

#### d9556_BB_flop (5h5d on 5s6d6h; expert CHECK; reversal)

Features:
- `is_strong_made=1, is_monster=1` (full house)
- `is_ip=0` (BB OOP)
- `is_paired=True` (board has 6h+6d paired; also 5s and hero's 5h5d giving fives full)
- `num_opponents=2`
- `villain_top_pair_plus_pct=0.277, villain_air_pct=0.718`

**Rule 11 decision-rule walk:**
1. `is_monster = 1` → predicate check 1 PASS
2. `is_ip = 0` → check 2 PASS
3. Board paired → check 3 PASS
4. `num_opponents >= 2` → check 4 PASS
5. → Default to CHECK with confidence MEDIUM
6. BET only if `villain_top_pair_plus_pct >= 0.40` (here 0.277 < 0.40) → BET exception does NOT fire
7. → Final action: **CHECK** ✓

Rule 11 correctly routes d9556 to CHECK. **PASS.**

#### MW-39 (AhJh on Kh8h3d; expert CALL; standard)

Features:
- `is_made_hand=0, is_strong_made=0, is_monster=0` (drawing — nut FD)
- `is_ip=1` (BTN)
- `has_flush_draw=1`, hero is AhJh → nut flush block active (Ah)
- `villain_air_pct=0.0532` (5.3%)

**Fix 2 OVERRIDE walk (L770-790):**
- "Hero has nut flush draw + Ah blocker?" → YES (narrative match; `flush_draw_rank` would = 14, hero holds Ah blocker)
- "AND `villain_air_pct >= 0.20`?" → 0.0532 < 0.20 → NO
- → "CALL preferred; fold equity component insufficient; realise equity vs calling range instead"
- → Final action: **CALL** ✓

Fix 2 correctly routes MW-39 to CALL. **PASS** (with the V2 NIT about `nut_flush_block` being a non-canonical feature name — the narrative pattern match still fires).

### V8. Risk surface — PASS (no new failure modes for d3178 or WE9)

**d3178_CO_river (AcAs on JhQcJc+Ks+5h paired river; expert BET; reversal):**
- `is_strong_made=1, is_monster=0` → Rule 11 predicate triggers
- `is_ip=0` (CO OOP), board paired (JJ), `num_opponents=2` → all match
- BUT `villain_top_pair_plus_pct=0.827 >= 0.40` → BET exception (a) fires → **BET ✓**
- ALSO `villain_checked_back=1` (river checked-to) → Rule 11 explicit "this rule does NOT apply to" clause (L711) for river checked-to spots → Rule 11 disengages entirely → existing v3.1 reasoning applies → **BET ✓**

Either path lands on BET. d3178 not broken.

**Worked Example 9 (As Qs nut FD on Ks Jd 5s, OOP, 3-way flop, expert RAISE):**

Per knowledge/three_way_gto.md L1117 (factor 4): "Board: Ks Jd 5s — two spades, high cards favour raiser's range." Hero is OOP, has nut flush draw + As blocker + 6 overcard outs + gutshot.

The OVERRIDE applies if `villain_air_pct < 0.20`. WE9's KB text doesn't quote a specific `villain_air_pct` value, but the spot is "CO bets 30 into 90; 3-way pot (CO opened, BTN called)" — CO's preflop opening range is ~27-28% (KB §3) which contains substantial air pre-flop, and on Ks Jd 5s the CO c-bet range is the CO's broader continuing range. The V3.2 OVERRIDE is conditional on the actual feature value, not on the KB example. If WE9's actual feature row had `villain_air_pct >= 0.20`, the RAISE conclusion is preserved. If it had `villain_air_pct < 0.20`, the OVERRIDE would flip WE9 to CALL — but per `feedback_solver_findings.md` this would be the solver-correct call (the rule's whole point is that the v3.1/KB §1.7 raise was over-applied below the air threshold).

**Conclusion:** the OVERRIDE is feature-conditional, not narrative-conditional. WE9 is not structurally broken — the OVERRIDE either preserves WE9's RAISE (if air ≥ 0.20) or correctly flips it to CALL (if air < 0.20, in which case the v3.1 KB advice was wrong and v3.2 is fixing it). No new failure mode.

**Protocol B Step 2 weakening:**

Per directive option (c) instruction: hand-class proxy is empirically valid replacement. Protocol B Step 2's reasoning chain (Steps 1-4) does not collapse — the Range-mass axis is one of three axes (Composition, Realisable-equity, Range-mass). The replacement text strengthens the axis by grounding it in real features (`prior_actions` + bucket label) instead of a phantom feature. **No weakening detected.**

## Findings

| Severity | Finding | Disposition |
|----------|---------|-------------|
| **HIGH** | Rule 11 decision-rule predicate (L699) gates on `is_strong_made = 1 OR is_monster = 1`, structurally excluding d3688 (TPWK = `is_strong_made = 0`). The narrative title "DO NOT auto-bet **strong-made** hands" reinforces this scoping. d3688 will likely fail again under v3.2 because nothing else in v3.2 contradicts the v3.1 Example 6 reasoning that produced the original BET. The directive cited d3688 as a target hand for Fix 1 but the rule as authored cannot reach it. | **MUST-FIX** before A.4 retry. Either (a) extend Rule 11's predicate to include medium-made hands on 2-tone-flush boards OOP with multiple live villains (a TPWK-specific exception), or (b) add a separate Rule 11.5 for the d3688 pattern (TPWK OOP on 2-tone board with 2nd live villain → CHECK), or (c) augment KB Example 6 with a 2-tone-flush OOP-multiway carve-out so labellers don't reach BET via that path. |
| MED | Fix 2 decision rule L785 cites a feature `nut_flush_block` that does not exist in the 54-feature contract (closest is `flush_block_pct`). Labellers reading strictly may not match the predicate; narrative pattern matching will likely still fire for MW-39. | Recommend rename to `flush_block_pct >= ~0.40` (operationalised threshold matching nut-blocker semantics) OR rephrase narratively to "hero holds the nut blocker (Ax of suit) to villain's nut flush combos". |
| NIT | v3.2 changelog L15 says "DO NOT Rules 1-11" preserved from v3.1, but v3.1 only had Rules 1-10. Should be "Rules 1-10 from v3.1, plus the new Rule 11". | Cosmetic; fix when convenient. |
| NIT | The "Decision rule (when in doubt)" in Rule 11 says "(set+, two pair, overpair, top pair top kicker on dry board)" as elaboration of `is_strong_made = 1 OR is_monster = 1`. But TPTK on dry board is hand_category-derived classification, not a feature flag — labellers must interpret. Could be tightened. | Cosmetic. |

## Recommendation

**Fix-forward.** The HIGH finding is structural, not cosmetic, and directly impacts A.4 v3.2 retry pass probability for d3688. Without addressing it:

- d9556 + MW-39 will pass (high confidence)
- d3688 may fail again (substantive risk) — putting v3.2 at FAIL/PASS ambiguous on the reversal gate

Recommended minimal patch:

1. Edit Rule 11 narrative title from "DO NOT auto-bet **strong-made** hands" to "DO NOT auto-bet **made hands** (top pair and stronger)..." OR add a parenthetical "(also applies to medium-made TP-weak-kicker on 2-tone-flush OOP multiway per d3688 anchor)"
2. Edit decision rule predicate L699 to: `Hero hand class is is_made_hand = 1 (top pair or stronger) AND we are on a 2-tone-flush OOP multiway spot — OR — is_strong_made = 1 OR is_monster = 1 on paired-board OOP multiway` (split the two EXCEPT clauses by hand-class scope)
3. Add d3688 explicitly to the "Affected calibration anchors" list

Optionally, address the MED finding on `nut_flush_block` in the same patch.

## Reference

- v3.2 prompt under review: `/home/rupertbeytell/river-rats-v2/prompts/gto_labeller_v3.2.md` (845 lines; v3.1 was 730)
- Rule 11 narrative + decision rule: `prompts/gto_labeller_v3.2.md` L669-718
- Fix 2 OVERRIDE section: `prompts/gto_labeller_v3.2.md` L758-800
- Protocol B pilot Range-mass axis post-fix: `prompts/protocol_b_composition_first_v1_0_pilot.md` L283-297
- Protocol B design Range-mass axis post-fix: `prompts/protocol_b_composition_first_v1_0.md` L264-278
- d3688 features (definitive): `review/pilot_run_2026-04-26/calibration_exam_payload.json` exam_entries[d3688_BB_flop]; key values: `is_strong_made=0, is_monster=0, is_made_hand=1, is_ip=0, num_opponents=2, villain_top_pair_plus_pct=0.198, villain_air_pct=0.338`
- d9556 features: `is_strong_made=1, is_monster=1, is_ip=0, num_opponents=2, villain_top_pair_plus_pct=0.277, villain_air_pct=0.718`
- MW-39 features: `is_strong_made=0, is_monster=0, is_ip=1, has_flush_draw=1, villain_air_pct=0.0532`
- d3178 features: `is_strong_made=1, is_monster=0, is_ip=0, villain_top_pair_plus_pct=0.827, villain_air_pct=0.173, villain_checked_back=1` (Rule 11 BET exception (a) fires + checked-to override fires; both paths preserve BET)
- v3.1 failed-hand reasoning excerpts: `review/pilot_run_2026-04-26/calibration_results_sonnet.json` and `calibration_results_opus.json`
- Path A directive: `review/comms/MAIN_TERMINAL_PATH_A_V32_PROTOCOL_REVISION_DIRECTIVE_2026-04-26.md` (master `24494eb`)
- Path A revision (Opus revert): `review/comms/MAIN_TERMINAL_PATH_A_REVISION_ACK_OPUS_REVERT_2026-04-26.md` (master `5cc7ba1`)

**Bottom line:** Fix 2 + Fix 3 are mergeable as-is. Fix 1 needs a structural patch to cover d3688 (medium-made on 2-tone OOP multiway) before A.4 v3.2 retry. The current Rule 11 will fix half the reversal failure (d9556) but leaves the other half (d3688) unaddressed.
