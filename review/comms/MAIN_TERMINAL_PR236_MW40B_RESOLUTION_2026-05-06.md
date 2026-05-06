---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #236 HALT resolution — Path γ' selected (drop sub-axis B; expand A+C to 15 each; hero TJ uniform; drop blocker rule); amend stop conditions; reaffirm builder authority on programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06
status: DIRECTIVE — resolves HALT; fires LEAD-PROGRAMMER on amended -B factory pass — fire now
---

# 12.5I-MW40-VERIFICATION-B HALT resolution — Path γ' (extended Path γ)

Builder PR #236 (`BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md`) correctly halted at design-translation phase before any factory emit. The HALT identified a real internal contradiction in PLAN §4 between hero-hand spec ("TT or T9" in sub-axis B; "TJ" in A and C) and the 5/5-per-sub-axis blocker variation rule.

Per `feedback_pilot_first_for_long_jobs.md`: Hybrid pilot-first 4-check pre-flight working as intended — caught a spec issue BEFORE any side-effect. Per `feedback_explicit_action_trigger.md` + `feedback_optional_is_not_authorized.md`: builder correctly routed to orchestrator instead of unilaterally redistributing.

## Decision rationale

Per `feedback_quality_default_no_ask.md` + `feedback_orchestrator_decides_not_recommends.md`. Slow-quality + orchestrator-decides analysis on the three offered paths plus a deeper diagnostic:

### The contradiction is broader than sub-axis B alone

Builder identified sub-axis B's blocker contradiction, but the same logic propagates through A and C: **hero hand class is the only meaningful lever for varying J-blocker count**. Hero TJ → 1 J in hand → blocks 1 villain JJ combo (uniform). Hero TT or T9 → 0 Js in hand → blocks 0. Suit variations within hero TJ do NOT change the J-blocker count (always 1). Therefore:

- Sub-axes A and C with hero TJ uniform = 100% with-J-blocker (10/0 each)
- Sub-axis B with hero TT or T9 uniform = 100% no-J-blocker (0/10)
- Plan total: 20/10, NOT 15/15

The plan's stop condition target "15/15 across 30 variants" was unattainable under any of plan §4's per-sub-axis rules. Builder's three offered paths each satisfy 15/15 only by mixing hand classes within sub-axes (which blurs the per-axis CHECK-consensus signal at -C) or by the redistribution Path α/β/γ each compromise differently.

### Quality-default reading: drop the broken constraint, sharpen the test

The verification's primary purpose is to test the structural prediction "J-on-board flips composition triple toward CHECK on TPMK T-kicker 4-way checked-through". The cleanest test is:

- All hands J-on-board at decision time
- All hands hero TPMK T-kicker (= hero TJ)
- All hands 4-way checked-through, BTN IP non-PFA
- No hand-class mixing within sub-axes (preserves per-axis CHECK-consensus measurement)

Blocker-effect sensitivity (`feedback_solver_findings.md` finding 2) is a *secondary* objective. The plan tried to package both objectives into the same 30 hands and the packaging was incoherent. Decoupling them is the slow-quality choice.

### Path comparison (orchestrator analysis)

| Path | Sub-axis split | Hand classes | J-blocker | Strength | Weakness |
|---|---|---|---|---|---|
| α (builder offered) | 10/10/10 | A: mixed TJ+TT; B: TT; C: TJ | 5/0/10 | Smallest hero-hand deviation | Concentrates J-blocker variation in C; introduces J-paired-flop confound |
| β (builder offered) | 10/10/10 | A: TJ; B: mixed TJ+TT; C: TJ | 5/5/5 | Per-sub-axis 5/5 satisfied | Hand-class mixing in B blurs per-axis CHECK signal |
| γ (builder default) | 15/0/15 | A: TJ; (B dropped); C: TJ | 30/0 (uniform) | Cleanest signal; plan §10 R1 pre-sanctioned | Forfeits future-J-expectation stress-test (sub-axis B) AND blocker-effect-sensitivity test |
| **γ' (orchestrator extension)** | **15/0/15** | **A: TJ; (B dropped); C: TJ** | **30/0 (uniform; rule dropped)** | **Cleanest verification of primary target; explicit board-list extension; explicit 15/15 stop condition revision** | **Same as γ — blocker-effect test deferred to follow-up** |

**Decision: Path γ' selected.**

Path γ is the right shape; γ' makes it executable by:
1. Specifying the additional 5 boards per sub-axis (builder selects per parametric class; architect-hat scoped within the merged plan template)
2. Explicitly amending the dispatch stop conditions (15/0/15 sub-axis split; uniform J-blocker = 30/0 acceptable)
3. Documenting blocker-effect-sensitivity deferral as a follow-up phase candidate (if MW-40 graduates, a 12.5I-MW40-VERIFICATION-2 round can specifically test blocker effects with mixed hand classes)

## Authoritative amended -B specification (binds on this comm merge)

The dispatch in `MAIN_TERMINAL_PR232_MERGE_AND_MW40B_DISPATCH_2026-05-06.md` (master `d584023`, PR #235) is amended as follows. All non-amended parts of the dispatch (Hybrid pilot-first 4-check, factory output structure, what-you-do-NOT-do, references) remain in force.

### §"Sub-axis distribution" — REPLACED

| Sub-axis | Count | Boards |
|---|---|---|
| A — J-high flop, hero TPMK on top of J-high (TJ) | **15** | The 10 boards from plan §4: Js9c5h, Js7d3c, Js8h4d, Js9d2c, Js8c4h, Js7h2d, Js9h3c, Js6d4s, Js9c3d, Js7c5d. **Builder selects 5 additional J-high parametric flops** matching plan §3 constraint table (J as the highest card on flop; non-paired; rainbow; 7-9 secondary). Examples valid: Js8d5c, Js7s3d (no — not rainbow; reject), Js6c2h, Js9h4c, Js5d2c. Builder may use `feature_extractor` consistency checks during the Hybrid pilot pre-flight to validate any board-class additions. |
| B — DROPPED | 0 | (Plan §4 sub-axis B removed from this verification round per Path γ'; future-J-expectation stress-test deferred to follow-up phase if MW-40 graduates.) |
| C — J-medium flop with paired-J or set-of-Js in range (TJ) | **15** | The 10 boards from plan §4: Jh5c2d, Jc8h3s, Jd9c4h, Jh6s3c, Jc7d2s, Jd8c5h, Jh4c2s, Jc9h6d, Jd7h3c, JcJh4s. **Builder selects 5 additional J-medium parametric flops** matching plan §3 constraint table (J as the middle card on flop; non-paired except for the one boundary paired-J variant from plan; rainbow). Boundary case JcJh4s remains. May add 1 more J-paired boundary if instructive (≤2 paired-J variants total to avoid spike). |

### §"Blocker variation" — REPLACED

**Replaced by:** "All 30 variants have hero TJ → uniform J-blocker = 1 (single J in hand). Blocker-effect-sensitivity test (per `feedback_solver_findings.md` finding 2) is deferred to a follow-up phase. The current verification round tests the primary structural prediction (J-on-board → CHECK on TPMK T-kicker 4-way checked-through) without the blocker-variation confound."

### §"Stop conditions" — REPLACED for 2 conditions; others stand

| Original | Amended |
|---|---|
| Sub-axis split not exactly 10/10/10 → STOP | **Sub-axis split not exactly 15/0/15 → STOP** |
| Blocker split not exactly 15/15 → STOP | **Blocker split = 30/0 (uniform with-J-blocker) is the expected outcome; no STOP on this condition; report to confirm.** |

All other stop conditions stand:
- Pre-flight fails ANY of the 4 checks on first 5 emitted → STOP
- ref_id collision with 788-corpus or prior 125i ref_ids on full 30 → STOP
- ≥1% NaN/Inf across 30 × 61 = 1830 feat_dict values → STOP
- Step-18 features show non-zero activation pattern → REPORT (not STOP)
- design_action ≠ CHECK on any emitted situation → STOP

### §"Hybrid pilot-first 4-check" — UNCHANGED

The Path 3 Hybrid 4-check pre-flight on first 5 emitted situations remains binding (schema parity / Step-18 plausibility / ref_id namespace / top-level structural fields per PR #228 SHOULD_FIX-1 resolution). Builder's HALT on PR #236 IS the pre-flight working as intended at the design-translation phase BEFORE the code-level pre-flight; reinforcing rather than weakening the discipline.

### §"Sub-axis B board-list expansion guidelines" — NEW

When builder selects the 5 additional boards per sub-axis (A and C):
1. Match plan §3 constraint table on every parameter (hero_seat=BTN, IP, non-PFA, num_opponents=3, street_of_decision=FLOP, villain_check_through_count=3, effective_stack=200bb, hand_category=6, kicker_class=T-kicker pinned, is_rainbow=1, pot_odds=0.0)
2. For sub-axis A: J as highest card on flop; rainbow; 7-9 secondary; no J-paired
3. For sub-axis C: J as middle card on flop; rainbow; bottom of flop ≥ 2; ≤2 paired-J variants total in C
4. Document the 5 additional boards explicitly in the builder report's §"Board list (PR #236-amended)" section
5. Builder may NOT add adjacent-kicker control variants (9-kicker, Q-kicker) — T-kicker stays pinned

## Builder authorization (binding on this comm merge)

LEAD-PROGRAMMER is authorized to fire the amended -B factory pass on:
- The same branch (`programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06`) — push the factory script + situations + amended report to PR #236, OR
- A new branch + new PR if cleaner — at builder's discretion

Either path is acceptable. PR #236 stays open as the work surface; if builder pushes to it, the PR title will likely need updating from "HALT — query orchestrator..." to the actual deliverable title.

## QC audit scope amendments (when -B PR is updated/replaced)

The 7-item QC scope in PR #235's dispatch is amended as follows; all non-amended items stand:

- **Item 4 (Sub-axis + blocker distribution):** REPLACED to "Sub-axis split 15/0/15 exact; sub-axis A = 15, sub-axis B = 0 (dropped per PR #236 resolution); sub-axis C = 15. Blocker split = 30/0 (uniform with-J-blocker; no variation in this round per Path γ' decision)."
- **Item 6 (Step-18 activation pattern):** UNCHANGED. Both Step-18 features still expected ≈ 0 across all 30 variants.
- **NEW item 8 (Path γ' compliance):** Verify builder selected 5 additional boards per sub-axis A and C; verify all 30 boards match plan §3 constraint table; verify no J-paired flops added beyond ≤2 total in C; verify T-kicker pinned uniformly.

## NIT carry-forward (still recorded for -E)

NIT-1 (terminology drift "composition quad" vs memory "composition triple") and NIT-2 (5th stop condition placement: <27/30 graduation threshold not in §8 STOP list) — both still carry forward to the 12.5I-MW40-VERIFICATION-E dispatch comm.

Additionally now: **NIT-3 (new, this resolution):** plan §4 contained an internal contradiction between hand-class binding and per-sub-axis blocker variation. Carry-forward: when authoring future verification-round design comms, run a contradiction-cross-check between hand-class spec and intra-sub-axis distribution rules before merge. Promote to TC-X-DISPATCH-COMPLIANCE class extension or a new TC-X-PLAN-INTERNAL-CONSISTENCY class? Surfacing for owner consideration.

## Why no Opus tier-up on this resolution

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs. This is an orchestrator decision-comm + spec-amendment; no labelling outputs produced, no factory pass run. Standard merge after this comm goes through normal orchestrator-PR cycle.

## What this comm does NOT do

- Does NOT modify the merged plan (`PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` on master `e0e0304`); it amends the dispatch via this resolution comm
- Does NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Does NOT modify river-rats-core/ source
- Does NOT modify BATCH2 reference
- Does NOT touch existing 788-corpus or any prior-phase corpus files
- Does NOT change cost / time estimates materially: factory pass is still ~$0; total -B time ~15-25 min (slight increase for the 5+5 board-selection step)

## What's blocked / what's queued

**Cleared by this comm:**
- PR #236 HALT resolved
- LEAD-PROGRAMMER authorized to fire amended -B factory pass on PR #236 branch (or fresh branch)
- Hybrid pilot-first 4-check pre-flight remains binding

**Newly queued (after -B factory pass + QC PASS + merge):**
- 12.5I-MW40-VERIFICATION-C labelling round (5 Sonnet × 30 hands; pilot-first 5-hand gate)
- 12.5J-C trainer integration test on 61-surface (parallel queue)

**Still queued (later):**
- 12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision
- 12.5I-MW40-VERIFICATION-E BATCH2 reference update OR memo-only PR (NIT-1 + NIT-2 + NIT-3 bind)
- Follow-up phase candidate (post-graduation): 12.5I-MW40-VERIFICATION-2 specifically testing blocker-effect sensitivity with mixed hand classes (only if MW-40 graduates from this round)
- 12.5K combined re-train (gates on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship)
- 12.5L gate eval (gates on 12.5K)

**Owner-scope items pending (informational, non-blocking):**
- TC-X-DISPATCH-COMPLIANCE curative addition to `learning/test_class_registry.md` (3 successful exercises now: PR #228 SHOULD_FIX-1, PR #232 clean PASS, PR #236 HALT-detection)
- TC-X-PLAN-INTERNAL-CONSISTENCY (new, proposed via NIT-3): cross-check spec internal consistency before merge — owner-scope to ratify class addition

## References

- PR #236 HALT query: branch `programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06`, file `BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md`
- PR #235 (original -B dispatch): master `d584023`
- PR #228 (Plan with §4 contradiction; merged but contradiction surfaced post-merge): master `e0e0304`
- PR #231 (Path 3 Hybrid pilot-first resolution): master `e44ed59`
- Plan §10 R1 (sub-axis B fallback pre-sanctioned): "If orchestrator wants pure 'J-at-decision-time' test → drop sub-axis B → 15/0/15"
- Memory: `feedback_quality_default_no_ask.md` (slow-quality default; Path γ' selection), `feedback_orchestrator_decides_not_recommends.md` (orchestrator decides among offered paths), `feedback_pilot_first_for_long_jobs.md` (Hybrid pre-flight working as intended), `feedback_explicit_action_trigger.md` + `feedback_optional_is_not_authorized.md` (builder correctly halted), `feedback_solver_findings.md` finding 2 (blocker effects deferred to follow-up phase)

**Status: HALT resolved via Path γ' (drop sub-axis B; expand A+C to 15 each; hero TJ uniform; drop blocker rule; amend stop conditions). LEAD-PROGRAMMER fires amended -B factory pass on this comm merge. ~15-25 min wall clock to PR update / new PR.**
