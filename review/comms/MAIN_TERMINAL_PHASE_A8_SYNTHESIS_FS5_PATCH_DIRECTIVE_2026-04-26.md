---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder (transient builder persona for git ops) · Pilot Orchestrator · Owner · QC stream
re: A.8 audit synthesis — static prompt audit (MINOR_ISSUES) + teaching archaeology (TEACHING_FIX_ONLY); F-S5-1/F-S5-2 phantom feature MEDIUM patch directive issued; Phase B remains HELD pending patch + A.4 complete + trace audit clean; teaching-stream bugs deferred to post-pilot fix-forward (non-blocking)
status: DIRECTIVE — F-S5 patch (option c hand-class proxy) ACTIVE; Phase B HELD; A.4 + trace audit + final synthesis still pending
---

# A.8 — Synthesis + F-S5 Patch Directive

## Audit verdicts (2 of 4 components complete)

| Component | Status | Verdict |
|-----------|--------|---------|
| Static prompt audit | ✅ COMPLETE | MINOR_ISSUES (F-S5-1/F-S5-2 phantom feature MEDIUM; F-S5-4 NIT board_adjusted_hrp; F-S6 mixed-strategy gap; F4 NIT B-Ex4 sizing) |
| Teaching archaeology | ✅ COMPLETE | TEACHING_FIX_ONLY (root cause = renderer bugs, NOT labels; Phase B NOT structurally blocked) |
| Trace audit | ⏳ PENDING (post-A.4 completion ~21:00) | n/a |
| Calibration coverage audit | ⏳ PENDING | n/a |

## Static prompt audit — key findings

**CLEAN dimensions (don't fix what isn't broken):**
- HRP semantic consistency: 11 references all aligned (1.0=top, 0.0=bottom)
- DO NOT Rule 10 inheritance: byte-identical verbatim in both pilots
- Cross-protocol convergence: all 4 shared-example pairs (B-Ex2/C-Ex2 MW-30, B-Ex3/C-Ex3 LITMUS_KQ, B-Ex4/C-Ex4 d8886, B-Ex5/C-Ex5 post-fold A8) converge on action label + range-placement classification
- Real villain composition features (`villain_top_pair_plus_pct`, `villain_medium_made_pct`, `villain_draw_pct`, `villain_air_pct`): consistent semantics across all 3 artifacts

**MEDIUM findings — F-S5-1 + F-S5-2 (phantom hero feature):**

Protocol B pilot `prompts/protocol_b_composition_first_v1_0_pilot.md` L283-285:
```
- **Range-mass axis:** what fraction of hero's own range
  (`hero_top_pair_plus_pct` etc. if available) is in the same
  category as villain's? Used for range-vs-range balance.
```

`hero_top_pair_plus_pct` does NOT exist in the 59-feature contract:
- v3.1 feature table L441-496: not listed
- Pilot Feature 55 note: only `board_adjusted_hrp`
- v2.4 P1 blockers (56-59): `nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct` only
- `river-rats-core/feature_keys.py`: HERO_RANGE_PERCENTILE + `_board_adjusted_hero_range_percentile` only; no hero composition pcts

Same phantom inherited at design artifact `prompts/protocol_b_composition_first_v1_0.md` L265.

**Risk:** Labellers reading the pilot prompt may
1. Hallucinate a value for `hero_top_pair_plus_pct` (LLMs do this when prompted to read a named feature)
2. Skip the Range-mass axis silently (weakening Step 2 reasoning)
3. Generate inconsistent labels across the 4500 mass-labelling targets

**This is the V-C13 incident class** (spec-vs-infrastructure-code drift, with addendum on existence-drift). Same fix-forward pattern.

## Teaching archaeology — key findings

**Verdict: TEACHING_FIX_ONLY** — root cause is **(b) renderer bugs**, not (a) bad training labels.

Five recurring renderer-side range conflations identified:
1. **HRP-vs-bucket clash** — "We hold air. At the 51st percentile of our range" (BP4_24, BP4_21); HRP is preflop-native and shouldn't be used postflop per `PRO_RANGE_ANALYSIS_PREFLOP_VS_POSTFLOP.md`; migration started in commit `0e75102` but didn't flow to agent-student prompts
2. **"Hero range position" sentence carries villain-range numbers** — `l3_renderer.py:368-371` concatenates "near top of hero's range" with `worse_hand_pct` (a villain-range fraction)
3. **"Range capped at SPR"** — six rendered hands glue range-property to stack-geometry; BP4_09 has uncapped 33/33/33 distribution but text says "capped"
4. **Hardcoded action-keyed range strings** — "calling keeps strong hands in range" emitted for nut-flush-draw caller with no made hand
5. **L5 range-frequency reasoning fired at L3** — flagged in `GTO_EXPERT_REVIEW_2026-04-16.md` "Systemic issue #3"

**Why Phase B is safe:**
- Structured training fields (`hero_range_percentile`, `worse_hand_pct`) are computed correctly in `feature_extractor.py:2266` and stored faithfully in `data/v2_2_enriched.jsonl`
- Team-reasoning text fields T1-T4 in spot-checked rows use range concepts correctly (proper "semi-bluff" / "polar" / "capped" usage)
- **Bugs live in the rendering/prompt layer DOWNSTREAM of labelling**

These bugs DO need fixing — but post-pilot, in the teaching-stream's own fix-forward cycle. Adding them as HOLD register items.

## Combined Phase B disposition

Phase B is **NOT structurally blocked** per teaching archaeology. **Phase B IS held pending F-S5-1/F-S5-2 patch** because the phantom feature would corrupt mass labelling.

Path to Phase B dispatch:
1. **F-S5 patch ships** (this directive — ~30-45 min builder cycle)
2. **A.4 calibration completes** (~21:00)
3. **Trace audit on A.4 reasoning paragraphs** (~15-30 min)
4. **Calibration coverage audit** (orchestrator-owned ~15 min)
5. **A.8 synthesis comm** (orchestrator-owned ~15 min)
6. **Phase B dispatch decision** at A.8 synthesis CLEAN

Estimated wall-time to Phase B dispatch: ~21:30-22:00 SAST.

## F-S5 patch directive (logic builder)

**Logic builder transients-reactivates from Pilot Orchestrator persona for git ops; Pilot Orchestrator persona resumes after F-S5 patch merges.**

### Scope

Edit:
- `prompts/protocol_b_composition_first_v1_0_pilot.md` L283-285 (Range-mass axis text)
- `prompts/protocol_b_composition_first_v1_0.md` L264-266 (design artifact, same text)

### Recommended fix — Option (c): hand-class proxy

Replace the Range-mass axis text with hand-class-derived range-mass reasoning that uses ONLY features that actually exist in the 59-feature contract.

**Suggested replacement text (verbatim — apply to both files in identical form):**

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

**Why option (c) over (a) remove or (b) note absence:**
- Per `feedback_quality_default_no_ask.md` — quality default; preserves the 3-axis Step 2 structure
- Derivation uses features that DO exist: bucket assignment (Step 1 output) + `prior_actions` (already in feat_dict)
- Avoids labellers hallucinating a phantom feature
- Avoids weakening Step 2 by silently skipping an axis
- Matches the `feedback_preflop_geometry_vs_postflop_composition.md` memory
  rule (reason from TP+/draws/air composition triple, not preflop range
  construction labels — the patch correctly anchors range-mass to the
  bucket triple, not to preflop labels)

### Workflow

Standing per-batch protocol:
1. Branch: `stage4-pre-dispatch/protocol-b-fs5-phantom-feature-patch`
2. Edit both files identically (preserve byte-equivalence to the design
   artifact pattern — same rule that made Build A/B verbatim-inlining work)
3. PR (call it PR #47 for tracking)
4. Builder reviewer dispatch — verify substitution doesn't create new
   inconsistencies; verify both files have identical replacement text
5. QC pre-merge audit (Path B as standard)
6. Orchestrator V3-compliance reviewer (this is a labeller-prompt edit;
   V3-compliance flavor applies)
7. Merge after triple-pipeline convergent APPROVE

### Expected hash impact

The Build A pilot artifact's frontmatter records:
- `derived_from`: `prompts/protocol_b_composition_first_v1_0.md @ master c4f29a5`
- `inlined_sections`: byte-equivalence with v3.1 line ranges

The patch is OUTSIDE the verbatim-inlined sections (Range-mass axis is in
Protocol B's body, not in §Buckets/§Features/§DO NOT Rules). So no
verbatim-inlined section changes; no v3.1 source edit needed; cross-
protocol consistency on the 4 shared examples PRESERVED (none of those
examples reference `hero_top_pair_plus_pct`).

Hash will change in both files post-patch:
- Pilot SHA256 (currently in lockfile?): TBD — patch is post-pilot-build,
  but Build A's PR #35 was merged so re-attestation IS needed if we want
  to maintain the hash-locked attestation pattern; otherwise patch lands
  as a normal master-branch edit since Build A is post-merge already

Builder's call on whether to update Build A's hash-lock attestation OR
treat as a master-branch edit. Surface decision in PR description.

## Teaching-stream fix-forward (deferred, non-blocking)

Adding to HOLD register; teaching builder addresses post-pilot:

| # | Item | Status | Owner |
|---|------|--------|-------|
| 47 | Teaching-stream renderer fix: HRP-postflop conflation | ⏳ DEFERRED post-pilot | Teaching builder |
| 48 | Teaching-stream renderer fix: hero-vs-villain-range concatenation | ⏳ DEFERRED post-pilot | Teaching builder |
| 49 | Teaching-stream renderer fix: capped-vs-SPR conflation | ⏳ DEFERRED post-pilot | Teaching builder |
| 50 | Teaching-stream renderer fix: hardcoded action-keyed range strings | ⏳ DEFERRED post-pilot | Teaching builder |
| 51 | Teaching-stream renderer fix: L5 frequency reasoning at L3 | ⏳ DEFERRED post-pilot | Teaching builder |
| 52 | Phase B safety net: 5% sample of mass-labelled output for team-reasoning text conflation check | ⏳ POST-PHASE-B | Orchestrator |
| 53 | Regenerate `full_50_prompts.json` from enriched renderer (legacy was used at 2026-04-18 playtest commit `ab8d172`) | ⏳ POST-PILOT | Teaching builder |
| 54 | Fix `gold_standards.md` so Phase 2 scorer doesn't reward wrong frame | ⏳ POST-PILOT | Teaching builder |

I'll surface these to teaching stream after Phase B completes.

## Pending audit components

### Trace audit (post-A.4 completion, ~21:00)

Apply rubric R1-R6 (per A.8 directive) to the 76 reasoning traces from
A.4 (Sonnet × 38 + Opus × 38). Specifically:
- R1. HRP referenced when relevant?
- R2. HRP overridden when hand visibly strong (Rule 10)?
- R3. Top/middle/bottom of range classified explicitly?
- R4. Hero composition features cited alongside bucket?
  (NOTE: post-F-S5 patch, this is now bucket-derived not phantom-feature-derived)
- R5. Mixed-strategy frequency reasoning?
- R6. Cross-trace agreement on range placement for same hand?

I'll dispatch a gto-expert agent for trace audit when A.4 completes.

### Calibration coverage audit (orchestrator-owned, ~15 min)

Verify the 38 calibration hands cover:
- Top-of-range value-bet scenarios (target: ≥3 hands)
- Middle-of-range pot-control / mixed scenarios (target: ≥3 hands)
- Bottom-of-range bluff-catch / fold scenarios (target: ≥3 hands)
- Range-vs-range matchups across positions (target: ≥3 hands)

I'll do this directly post-A.4 completion.

## Action items

**Logic builder (transient builder persona):**
1. Take F-S5 patch directive above
2. Branch `stage4-pre-dispatch/protocol-b-fs5-phantom-feature-patch`
3. Apply option (c) replacement text to both files (pilot + design)
4. PR #47; standing per-batch protocol
5. Builder reviewer + QC + orch V3-compliance triple-pipeline
6. Merge after triple-APPROVE
7. Resume Pilot Orchestrator persona post-merge

**Pilot Orchestrator (resumes post-F-S5 patch + A.4 completion):**
1. Continue A.4 dispatch (no change — running)
2. Surface A.7 summary normally with empirical winner-pick
3. **CONTINUE TO HOLD Phase B dispatch** — wait for A.8 synthesis (orchestrator-owned) before Phase B
4. Surface 76 raw reasoning traces in `review/pilot_run_2026-04-26/` for trace audit

**Orchestrator (me):**
1. This synthesis + F-S5 directive shipped (atomic flow next)
2. Dispatch trace audit agent post-A.4 completion
3. Run calibration coverage audit (~15 min)
4. Compose A.8 final synthesis comm
5. After F-S5 patch merges + A.4 GO + trace audit clean + coverage audit clean → green-light Phase B

**QC stream:**
- Continue Layer 3 watch
- Audit PR #47 per standard pre-merge protocol (Path B Bundle)
- TC-23 + V-X3 vectors apply to F-S5 patch

**Owner:**
- Audit verdicts: MINOR_ISSUES on prompts (1 MEDIUM patchable in 30-45 min) + TEACHING_FIX_ONLY on teaching stream (8 HOLDs queued post-pilot)
- Phase B not structurally blocked; held only on F-S5 patch + A.4 + trace audit
- Wall-time impact: ~30-45 min added by F-S5 patch cycle; ETA Phase B dispatch ~21:30-22:00 SAST
- Cost impact: ~$5 patch dispatch; A.4 budget unchanged

## References

- A.8 directive: `1c6f674` (`MAIN_TERMINAL_PHASE_A8_RANGE_REASONING_AUDIT_DIRECTIVE_2026-04-26.md`)
- Static prompt audit: `review/comms/AUDIT_A8_STATIC_PROMPTS_2026-04-26.md`
- Teaching archaeology: `review/comms/AUDIT_A8_TEACHING_ARCHAEOLOGY_2026-04-26.md`
- Option C directive: `439cfd7` (`MAIN_TERMINAL_PILOT_PHASE_A_OPTION_C_DIRECTIVE_2026-04-26.md`)
- Pilot Phase A status: `review/comms/PILOT_PHASE_A_STATUS_2026-04-26.md`
- Memory: `feedback_spec_vs_infrastructure_code_drift.md` (with existence-drift addendum); `feedback_quality_default_no_ask.md`; `feedback_preflop_geometry_vs_postflop_composition.md`

**Status: A.8 SYNTHESIS PARTIAL (2 of 4 components clean). F-S5 PATCH
DIRECTIVE ACTIVE. Phase B HELD pending F-S5 merge + A.4 + trace audit
+ coverage audit. ETA ~21:30-22:00 SAST.**
