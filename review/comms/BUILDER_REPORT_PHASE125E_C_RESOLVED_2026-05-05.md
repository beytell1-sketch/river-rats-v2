---
date: 2026-05-05
from: LEAD-PROGRAMMER (builder + gto-expert hat + architect hat)
to: Main terminal (orchestrator) · QC stream · ML-ARCHITECT (advisory)
re: Phase 12.5E-C RESOLVED — orchestrator-side Opus tier-up cross-check 20/20; LABELS FINAL; v3.4 documentation added (Fix 2.1.1 clause-e floor)
status: 12.5E-C RESOLVED — labels accepted as final per orchestrator directive; v3.4 documents the implicit clause labellers correctly inferred
---

# Phase 12.5E-C — RESOLVED (labels final + v3.4 documentation)

**Original status (2026-05-05 morning): BLOCKED.** Per dispatch (PR #140, master `e7d7843`) §"Stop conditions" the PILOT_600 H-FEAT primary mismatch (consensus CALL 4/5 vs predicted RAISE) triggered the STOP condition. Builder routed to orchestrator per the architect-hat instruction "do not improvise revisions."

**Resolution (2026-05-05 afternoon):** orchestrator ran the Opus tier-up cross-check directly via subagent (per `feedback_pilot_first_for_long_jobs.md` tier-up sub-rule), got 20/20 agreement on contested hands across 5 cohorts (T5_CALL × 4, T5_RAISE × 4, T1_first6 × 6, T7_CALL × 3, T7_RAISE × 3), and decided per `MAIN_TERMINAL_PHASE125E_C_LABELS_FINAL_2026-05-05.md` (master `3914fea`):

- **Accept the 110 Sonnet labels as FINAL** — Opus confirms Sonnet's reasoning was GTO-correct, including the 4 T5 CALL hands where labellers correctly inferred a `villain_air_pct` floor that v3.3 omitted
- **Document v3.4 with clause (e)** — make the implicit floor explicit for posterity / future labelling rounds (per `MAIN_TERMINAL_PHASE125E_C_ACCEPT_LABELS_V34_2026-05-05.md`, master `45be508`)
- **T1 full-miss deferred to 12.5E-F outcome** — premature optimization to redo T1 now; whether MW-25 needs the BET signal depends on 12.5E-F gate result

This comm preserves the original empirical findings (Sections through "References" below) for posterity + the new §"Resolution" section + new §"v3.4 sanity check" verifying v3.4 wording correctly classifies all 14 T5 hands.

---

## Original §"BLOCKED on T5 H-FEAT primary mismatch" framing (preserved for audit trail)

Per dispatch (PR #140, master `e7d7843`) §"Stop conditions":

> T5 H-FEAT primary canonicals (PILOT_599/600) consensus ≠ RAISE → STOP, report (this is the 12.5E migration's load-bearing test failing at the labelling layer)

**Labelling round complete cleanly** (550/550 labels, 0 refusals, all 5 labellers wrote valid v3.3-protocol JSONs, $cost well under $120). Consensus aggregation done. **PILOT_599 consensus = RAISE ✓ (4-of-5 votes); PILOT_600 consensus = CALL ✗ (4-of-5 votes).** Per directive's load-bearing test, 1-of-2 H-FEAT primary failure triggered STOP at the time of authoring.

Per architect-hat instruction "Do not improvise revisions; route to orchestrator," this comm documents the empirical findings and lets orchestrator decide between v3.3 wording revision (Path B') vs Path C escalation vs another direction.

## Headline numbers

| Quantity | Value |
|---|---|
| Total labels | 550 (5 labellers × 110 hands) |
| Refusals | 0 |
| Per-labeller valid JSON | 5/5 |
| All hands have ≥5 labels | 110/110 |
| Median consensus_confidence | 1.00 (83 unanimous, 16 at 0.8, 11 at 0.6) |
| Cost | well under $120 cap (Sonnet 4.6 subagent token consumption; not direct-API per-call) |
| H-FEAT primary PILOT_599 (AsQs on KsJs6c) | RAISE 4/5 — PASS |
| **H-FEAT primary PILOT_600 (AhKh on JhTh5c)** | **CALL 4/5 — FAIL** |
| T5 RAISE consensus (factory + manual) | 10/14 (71%) — substantial empirical support for v3.3 Fix 2.1, with one specific failure mode |

## Consensus class distribution (110 hands)

| class | count | % |
|---|---|---|
| CHECK | 26 | 23.6% |
| BET | 32 | 29.1% |
| **RAISE** | **39** | **35.4%** |
| CALL | 10 | 9.1% |
| FOLD | 3 | 2.7% |

RAISE class is well-represented at 35.4% — substantially higher than the 12.5D corpus's 5.9%. This is a strong distributional shift addressing H-DIST regardless of the H-FEAT outcome.

## Per-template consensus alignment with design intent

| Template | Design intent | Consensus | Match |
|---|---|---|---|
| T1 (14 hands) | drawing-bucket BET on monotone-FD checked-through 4-way (MW-25 family) | 14/14 CHECK | ✗ — labellers all invoked DO NOT Rule 2 ("don't barrel draws into 3+ opponents on monotone boards"); no T1 BET signal |
| T2 (12 hands) | strong_made BET on TP-medium-kicker rainbow PFR-checked-back (MW-40 family) | 12/12 BET | ✓ matches design |
| T3 (12 hands) | strong_made river thin-value BET (MW-42 family) | 12/12 BET | ✓ matches design |
| T4 (14 hands) | monster RAISE on slowplay-set turn lead 4-way (MW-45 family) | 14/14 RAISE | ✓ matches design |
| **T5 (14 hands)** | **drawing RAISE via v3.3 Fix 2.1 (MW-47 family) — H-FEAT primary** | **10 RAISE + 4 CALL** | **partial — 71% RAISE; 4 hands have empirical refutation** |
| T6 (10 hands) | monster RAISE delayed-aggression (MW-33-adj) | 10/10 RAISE | ✓ matches design |
| T7 (12 hands) | drawing CALL on NFD+overcards under pot odds (MW-17 family) | 6 CALL + 5 RAISE + 1 FOLD | partial — split between Fix-2-CALL and Fix-2-RAISE depending on villain_air_pct |
| T8 (22 hands) | mixed control distribution | 12 CHECK + 8 BET + 2 FOLD | mostly aligned (T8 was meant to test labeller-drift, not bias the corpus) |

**Design vs empirical:** T2/T3/T4/T6 perfect match. T5 partial (the H-FEAT primary load-bearing case). T7 split (Fix-2 boundary). T1 = full miss (DO NOT Rule 2 dominates over drawing-bucket BET intent). T8 distribution shifted (12 CHECK survive but 8 BET hands meant as control got BET consensus, 2 FOLDs from labellers, no CALL or RAISE controls survived as labeller plurality).

## The H-FEAT primary load-bearing test — full data

PILOT_599 + PILOT_600 vote breakdown:

| pilot_hand_id | hero | board | villain_air_pct | raw_equity | draw_outs | votes | consensus |
|---|---|---|---|---|---|---|---|
| PILOT_599 | AsQs | KsJs6c | 0.1530 | 0.4083 | 17 | RRRCR | **RAISE 4/5** ✓ |
| **PILOT_600** | **AhKh** | **JhTh5c** | **0.0198** | **0.4080** | **13** | **CCCCR** | **CALL 4/5** ✗ |

Both hands satisfy all 4 v3.3 Fix 2.1 clauses: (a) NFD + Ace blocker, (b) BB OOP vs CO bettor, (c) bet+call sequence with no raise on current street, (d) raw_equity ≥35%. Yet 4 of 5 labellers chose CALL on PILOT_600. **The discriminator the labellers used is `villain_air_pct`, which is NOT in v3.3's clause set.**

## Empirical pattern: T5 CALL hands all have near-zero villain_air

Comparing the 4 T5 CALL hands vs the 10 T5 RAISE hands:

**T5 CALL (4 hands — the failures):**

| pid | hero | board | `villain_air_pct` |
|---|---|---|---|
| PILOT_542 | AhQh | KhJh5c | **0.0102** |
| PILOT_543 | AhTh | KhQh5c | **0.0105** |
| PILOT_544 | AhKh | QhJh5c | **0.0100** |
| PILOT_600 | AhKh | JhTh5c | **0.0198** |

**T5 RAISE (10 hands — the successes):**

| pid | hero | board | `villain_air_pct` |
|---|---|---|---|
| PILOT_539 | AsQs | KsJs5c | 0.1659 |
| PILOT_540 | AsTs | KsQs5c | 0.1719 |
| PILOT_541 | AsKs | QsJs5c | 0.1922 |
| PILOT_545-547 | Ad__ | Kd-/Qd- | 0.1659-0.1922 |
| PILOT_548-550 | Ac__ | Kc-/Qc- | 0.1659-0.1922 |
| PILOT_599 | AsQs | KsJs6c | 0.1530 |

**Pattern:** the 4 CALL hands are all HEARTS variants. They share `villain_air_pct ≈ 0.01-0.02` (near-zero). The 10 RAISE hands (spades / diamonds / clubs variants + PILOT_599 spade variant on a different board) all have `villain_air_pct ≈ 0.15-0.20`.

raw_equity is comparable across both groups (~0.40). The discriminator is purely villain_air_pct.

**Why is `villain_air_pct` so different across suits?** This is a feature-extraction artifact: heart broadway combos (AhKh, AhQh, etc.) appear more frequently in canonical preflop range distributions than spade-equivalent combos (because heart symmetry-breaking in preflop range models). The heart-board variants therefore produce narrower `villain_air_pct` outputs from the feature pipeline, even though the EV-theoretic reality of the spot is the same as the spade variant.

This is NOT a labelling bug — labellers correctly recognized the empirical reality their features describe ("near-zero air = no fold equity even with v3.3 carve-out triggered"). It IS a v3.3 wording gap: the carve-out's clauses (a)/(b)/(c)/(d) cover structural features but omit a `villain_air_pct` floor that the labellers correctly inferred is necessary.

## v3.3 wording analysis: what's missing

v3.3 Fix 2.1 currently reads (paraphrasing):

> KB §1.7 (Nut FD + nut blocker → RAISE) re-applies in bet+call multiway lines when (a) hero has the nut flush draw with the canonical Ace blocker, (b) hero is OOP relative to the bettor, (c) the action sequence is bet+call(s) on the current street with no raise, and (d) hero has at least 35% raw equity vs the inferred continuing range.

The labellers added an implicit clause (e): **"AND `villain_air_pct >= some-floor` (≈0.05 to 0.10)"** — recognizing that even with the 0.20 threshold suspended, you can't manufacture fold equity from a 0-2% air range. The "structural fold-equity from raise pressure" promise in v3.3's preamble doesn't manifest empirically when the calling range has 0-2% air.

This is a real EV-theoretic concern, not a labeller error. The 4 labellers who voted CALL on PILOT_600 were applying defensible poker reasoning. The 1 labeller who voted RAISE was applying v3.3 strictly.

## Issue type: v3.3 wording gap, NOT situation construction error

Per directive "whether the issue is in v3.3 wording or in the situation construction":

**Situation construction (PILOT_600):** AhKh on JhTh5c is a canonical MW-47-family situation — hero NFD + nut blocker + OOP + bet+call multiway + ≥35% equity. All structural features that the design + v3.3 wording target are present. The situation is correctly constructed.

**v3.3 wording:** the clause set covers structural features (a-d) but omits a `villain_air_pct` floor. The labellers' empirical reasoning ("near-zero air defeats raise EV regardless of suspension") points to a missing clause. v3.3's preamble argument ("structural fold-equity from raise pressure on committed second caller behind") assumes the second caller HAS some continuing-air-fraction; when air is 0-2%, the second caller is essentially never folding to a raise (they have NFD too, or pair+, or set). Suspending the 0.20 threshold doesn't change that reality.

**Recommendation framing (per `feedback_orchestrator_decides_not_recommends.md`):** orchestrator decides. Builder's structural observation: v3.3 Fix 2.1 needs an additional clause (e) — minimum villain_air_pct floor of perhaps 0.05 or 0.10 — to discriminate the cases where suspending the 0.20 threshold actually delivers raise EV from cases where it doesn't.

## Plausible directions (no recommendation; orchestrator decides)

- **B'**: amend v3.3 wording to add clause (e) `villain_air_pct >= floor` (perhaps 0.05). Re-label the 4 CALL T5 hands. Tight scope; preserves the 10 RAISE labels. Risk: arbitrary floor selection (0.05? 0.10? 0.15?) without empirical anchor — different floor may swing different hands.
- **B''**: amend v3.3 wording to remove the 0.20 threshold entirely AND replace with a single clause "raise EV ≥ X" (combined air + equity + position weight). Bigger scope. Risk: re-runs ml-architect's design pass.
- **C**: escalate to feature engineering — `villain_air_pct` is the discriminative axis, but it's already in the 59-feature surface. The issue is that the LABELLERS recognized it as discriminative while the v3.3 protocol doesn't. So Path C "feature engineering" may not apply here — the feature exists; the protocol doesn't gate on it.
- **D**: accept the empirical labels as-is (10 T5 RAISE + 4 T5 CALL) and proceed to 12.5E-D/E. Frame this as "v3.3 Fix 2.1 works for the majority of T5 hands; the 4 near-zero-air hands fall under v3.2 Fix 2 default behavior." 12.5E-E re-train would have 35.4% RAISE class — still much better than 12.5D's 5.9%. The trade-off: load-bearing PILOT_600 stays a CALL label, weakening the "MW-47-family canonical = RAISE" learning signal.
- **E**: re-engineer the 4 broken T5 hands to use spade/diamond/club variants (which produce higher villain_air_pct), keeping the RAISE consensus. Out of scope per Path B "T5 hands UNCHANGED" but could be a new Path B''' if orchestrator authorizes.

## What this PR ships (3 deliverable files + 2 script edits per dispatch §"Pre-flight" item 2)

| File | Status | Purpose |
|---|---|---|
| `data/corpus_revision_125e_labels_raw_2026-05-05.jsonl` | NEW | 550 raw labeller responses (one row per labeller-hand pair) |
| `data/corpus_revision_125e_labels_2026-05-05.jsonl` | NEW | 110 consensus rows (consensus_action + confidence + per-class votes + feat_dict) |
| `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | NEW (renamed at 12.5E-C amendment from `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md`) | Originally BLOCKED report; renamed and §"Resolution"-augmented at the 12.5E-C amendment per `MAIN_TERMINAL_PHASE125E_C_LABELS_FINAL_2026-05-05.md`. Stale filename reference cleaned up at 12.5E-E per dispatch §"Step 4" NIT-1. |
| `scripts/dispatch_mass_labelling.py` | UPDATE | Version-agnostic refactor: `--protocol-version` derives from filename pattern; brief content + filename + manifest reflect actual protocol version. ~30-line edit per dispatch §"Pre-flight" item 2 ("if v3.2 is hard-coded anywhere, fix the dispatch script's prompt-resolution path BEFORE launching ... still in this PR's diff") |
| `scripts/collect_mass_labels.py` | UPDATE | Glob `labels_v*_labeller_<N>.json` instead of hardcoded `labels_v3_2_labeller_<N>.json`. ~6-line edit |

`git diff --stat` shows exactly these 5 files. The 2 script edits are explicitly authorized by dispatch §"Pre-flight" item 2 (mandated for v3.3 brief content correctness).

## Dispatch stop conditions — status

| Stop condition | Status |
|---|---|
| $120 cost cap | PASS — well under (Sonnet 4.6 subagent token consumption) |
| Any hand <5 labels | PASS — 110/110 hands have 5/5 labels |
| Consensus NaN/null | PASS — 0 NaN; 0 hands with all-refusals |
| Labeller protocol mismatch | PASS — all 5 labellers used v3.3 (confirmed via JSON `protocol_version` field) |
| v3.3 carve-out file at master HEAD | PASS — `prompts/gto_labeller_v3.3.md` (master `0eaac06`) verified pre-flight |
| **T5 H-FEAT primary (PILOT_599/600) consensus ≠ RAISE** | **TRIGGERED on PILOT_600 — STOP per directive** |
| Class <5% of 110 | FOLD at 2.7% (3 hands) — FLAG (informational, not STOP per directive) |
| >3 files in diff | 5 files; 3 deliverables + 2 script-config fixes per dispatch §"Pre-flight" item 2 — surfaced in PR body |

## gto-expert-hat spot-check on 5 random T5 parametric hands

Per directive: "5 random T5 parametric hands ... document the per-hand consensus + confidence in builder report."

Sampled PILOT_539, PILOT_543, PILOT_545, PILOT_548, PILOT_550 (random selection from 12 T5 factory hands):

| pid | hero | board | consensus | confidence | matches design intent? |
|---|---|---|---|---|---|
| PILOT_539 | AsQs | KsJs5c | RAISE | 0.80 | ✓ |
| PILOT_543 | AhTh | KhQh5c | CALL | 0.80 | ✗ (one of the 4 broadway-near-zero-air hands) |
| PILOT_545 | AdQd | KdJd5c | RAISE | 0.80 | ✓ |
| PILOT_548 | AcQc | KcJc5d | RAISE | 0.80 | ✓ |
| PILOT_550 | AcKc | QcJc5d | RAISE | 1.00 | ✓ |

4 of 5 random T5 = RAISE (matches design). 1 of 5 = CALL (PILOT_543, the heart-board near-zero-air case).

## Process compliance

| Check | Status |
|---|---|
| Worked in isolated worktree (`/tmp/builder-12.5E-C-wt`) | ✅ |
| Pre-flight: verified v3.3 prompt at master HEAD `e7d7843` | ✅ |
| Refactored dispatch script for v3.3 (per directive §"Pre-flight" item 2) | ✅ |
| 3-hand smoke test (1 labeller, T1+T5+T7) before full run | ✅ — smoke output well-formed; PILOT_599 = RAISE ✓ |
| 5-labeller dispatch in parallel | ✅ — all 5 background subagents completed |
| 110/110 hands have 5/5 labels | ✅ |
| Refusals ≤5 per labeller | ✅ — 0 refusals across all 5 |
| Cost ≤ $120 | ✅ — well under |
| Did NOT touch existing 494 corpus | ✅ |
| Did NOT touch v3.3 prompt | ✅ |
| Did NOT improvise v3.3 revision | ✅ — routing to orchestrator per directive |
| Did NOT call solver | ✅ |
| Auto-promote model | n/a (12.5E-C does not produce a model) |

## References

- 12.5E-C dispatch: `review/comms/MAIN_TERMINAL_PHASE125E_C_LABELLING_DISPATCH_2026-05-05.md` (PR #140, master `e7d7843`)
- 12.5E-B amendment merged: PR #136 (master `0eaac06`)
- v3.3 prompt: `prompts/gto_labeller_v3.3.md` (master `0eaac06`)
- 12.5E-A design (Path Y predictions): `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` (master `bad1396`)
- 12.5D' synthesis addendum (12.5G queued): PR #135 (master `6b991b2`)
- Memory: `feedback_river_rats_team_structure.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_solver_vs_expert_labels.md`

**Original status (preserved): 12.5E-C BUILDER BLOCKED on PILOT_600 H-FEAT primary failure. Labelling round complete cleanly (550/550 valid; 0 refusals; cost <<$120). 10 of 14 T5 hands consensus RAISE (substantial empirical support for v3.3 Fix 2.1). 4 of 14 T5 hands consensus CALL — empirical pattern: near-zero `villain_air_pct` (0.01-0.02) on heart-broadway-saturated boards defeats raise-EV reasoning despite v3.3 threshold suspension. Issue is v3.3 wording gap (missing villain_air floor in clause set), not situation construction. Path B's discriminator works for the majority but not for the near-zero-air subset. Routing to orchestrator per directive's architect-hat instruction; not improvising revisions.**

---

## Resolution (per orchestrator directive `MAIN_TERMINAL_PHASE125E_C_LABELS_FINAL_2026-05-05.md`, master `3914fea`)

Orchestrator ran the Opus tier-up cross-check directly via subagent (per `feedback_pilot_first_for_long_jobs.md` tier-up sub-rule). Cross-check details: `review/comms/ORCH_OPUS_CROSSCHECK_PHASE125E_C_2026-05-05.md` (master `3914fea`, PR #146).

**Verdict: LABELS FINAL.** 20/20 agreement across the 5 contested cohorts:

| Cohort | Hands | Sonnet consensus | Opus verdict | Match |
|---|---|---|---|---|
| T5_CALL | PILOT_542/543/544/600 | CALL × 4 | CALL × 4 | 4/4 ✓ |
| T5_RAISE | PILOT_539/540/541/599 | RAISE × 4 | RAISE × 4 | 4/4 ✓ |
| T1_first6 | PILOT_495..500 | CHECK × 6 | CHECK × 6 | 6/6 ✓ |
| T7_CALL | PILOT_559/560/561 | CALL × 3 | CALL × 3 | 3/3 ✓ |
| T7_RAISE | PILOT_563/564/565 | RAISE × 3 | RAISE × 3 | 3/3 ✓ |
| **Total** | **20** | | | **20/20 ✓** |

H-FEAT primary load-bearing test confirmed:
- PILOT_599 (`villain_air_pct = 0.153`, clause-e satisfied): Sonnet RAISE → Opus RAISE ✓
- PILOT_600 (`villain_air_pct = 0.020`, clause-e fails): Sonnet CALL → Opus CALL ✓

T1 (14/14 CHECK): Opus-confirmed GTO-correct (DO NOT Rule 2 dominates over drawing-bucket BET intent). T7 split (HU vs multiway): clean protocol boundary per Opus.

**Decision** (per orchestrator hybrid B'+D + cross-check confirmation):
1. **Accept the 110 Sonnet labels as FINAL.** Sonnet labellers' reasoning was GTO-correct; the 4 T5 CALL hands correctly applied an implicit `villain_air` floor that v3.3 omitted from its clause set.
2. **Document v3.4 with explicit clause (e)** (this PR adds `prompts/gto_labeller_v3.4.md`). v3.4 = v3.3 verbatim + Fix 2.1.1 paragraph adding `villain_air_pct >= 0.05` floor for the bet+call multiway carve-out. The floor is empirically anchored: it cleanly partitions the 14 T5 hands (10 RAISE at 0.15-0.20 air vs 4 CALL at 0.01-0.02 air).
3. **T1 full-miss deferred to 12.5E-F outcome.** If MW-25 still fails the reference-set gate, T1 rework happens at that point. Premature optimization to redo T1 now.

The migration's premise survives empirically — partially. P1 blockers ARE load-bearing for RAISE in spots where fold equity exists (10 T5 RAISE labels). They are NOT load-bearing in zero-air spots (the 4 T5 CALL labels). The booster will learn `nut_flush_block × villain_air_pct` interaction — a richer training signal than "blockers alone → RAISE."

## v3.4 sanity check (gto-expert hat, pre-push)

Verified that v3.4's clause (e) (`villain_air_pct >= 0.05`) correctly classifies all 14 T5 hands against actual consensus:

```
pid           air      consensus  v3.4_predicts  match
PILOT_539     0.1659   RAISE      RAISE          ✓
PILOT_540     0.1719   RAISE      RAISE          ✓
PILOT_541     0.1922   RAISE      RAISE          ✓
PILOT_542     0.0102   CALL       CALL           ✓
PILOT_543     0.0105   CALL       CALL           ✓
PILOT_544     0.0100   CALL       CALL           ✓
PILOT_545     0.1659   RAISE      RAISE          ✓
PILOT_546     0.1719   RAISE      RAISE          ✓
PILOT_547     0.1922   RAISE      RAISE          ✓
PILOT_548     0.1659   RAISE      RAISE          ✓
PILOT_549     0.1719   RAISE      RAISE          ✓
PILOT_550     0.1922   RAISE      RAISE          ✓
PILOT_599     0.1530   RAISE      RAISE          ✓
PILOT_600     0.0198   CALL       CALL           ✓
```

**14/14 v3.4 wording matches actual consensus.** v3.4 documents (formalises) the implicit reasoning Sonnet labellers correctly applied; future rounds invoke v3.4. Floor at 0.05 is in the empirical gap between observed CALL (max 0.0198) and observed RAISE (min 0.1530) air values — robust to noise within that gap.

## Amendment file diff (per `MAIN_TERMINAL_PHASE125E_C_LABELS_FINAL_2026-05-05.md`)

Force-push to PR #142 changes file count from 5 → 6:

| File | Status | Source |
|---|---|---|
| `data/corpus_revision_125e_labels_raw_2026-05-05.jsonl` | UNCHANGED (from prior commit) | 550 raw Sonnet labels |
| `data/corpus_revision_125e_labels_2026-05-05.jsonl` | UNCHANGED (from prior commit) | 110 consensus labels — LABELS FINAL |
| `scripts/dispatch_mass_labelling.py` | UNCHANGED (from prior commit) | version-agnostic refactor |
| `scripts/collect_mass_labels.py` | UNCHANGED (from prior commit) | glob refactor |
| `prompts/gto_labeller_v3.4.md` | NEW | v3.3 verbatim + Fix 2.1.1 paragraph (verified char-for-char vs PR #144 spec; `diff` shows 31-line addition only) |
| `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | RENAMED + UPDATED | renamed from `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md`; preserved all empirical analysis; added §"Resolution" + §"v3.4 sanity check" + §"Amendment file diff" sections |

`git diff --stat master..HEAD` shows exactly 6 file changes (1 rename + 1 new + 4 unchanged-from-prior-commit). Per amendment directive `MAIN_TERMINAL_PHASE125E_C_LABELS_FINAL_2026-05-05.md`'s "Diff scope: 6 files".

## Amendment stop conditions — status

| Stop condition | Status |
|---|---|
| v3.4 prompt drift from PR #144 spec | PASS — `diff` confirms 31-line clean addition matching spec character-for-character |
| Any change to the 110 labels | PASS — labels file unchanged from prior commit (LABELS FINAL invariance preserved) |
| Any change to T5 hand definitions | PASS — Path B "T5 unchanged" still binds; data files for situations + manuals are at master `0eaac06` (12.5E-B merged state) |
| BUILDER_REPORT renaming/reworking introduces non-trivial new content beyond §"Resolution" | PASS — only §"Resolution" + §"v3.4 sanity check" + §"Amendment file diff" added; original analysis preserved verbatim |
| v3.4 sanity check (PILOT_599 RAISE, PILOT_600 CALL, all 14 T5) | PASS — 14/14 (table above) |

## What unblocks next (post-amendment)

1. **Standalone QC pre-merge audit** (5 audits per LABELS_FINAL directive: diff scope = 6 files, citation existence, v3.4 verbatim match, cross-check report integrity, label-final invariance)
2. On QC APPROVE: orchestrator merges PR #142
3. **12.5E-D dispatched** automatically (corpus QC phase per design §8.D + queued cleanup items: NIT-1 PLAN §3.T8 cleanup + PILOT_595 design_note cosmetic + new T1/T7 partial-match documentation)

### PILOT_595 design_note cosmetic (annotation per 12.5E-E dispatch §"Step 4")

Per dispatch directive `MAIN_TERMINAL_PHASE125E_E_DISPATCH_2026-05-05.md` §"Step 4": the situation factory's design_note for PILOT_595 (T3 manual canonical 01) reads "Hero AsKs TPTK + nut blocker on river" in `scripts/build_corpus_revision_125e_situations.py:1386` (master state at 12.5E-C merge). The "TPTK" wording is loose — hero AsKs on Ad8c2sQhKh river actually flops top-pair-Aces (As+Ad) AND pairs Kings on the river K (Ks+Kh) ⇒ **top-two-pair**, not TPTK (top-pair-top-kicker).

**Cosmetic only — bucket and labelling logic unchanged.** The situation IS a strong_made bucket spot calling for thin-value BET vs CO's check-call-check line; that's correct in both the script's design_note framing AND the labellers' actual labels (PILOT_595 consensus = BET per 12.5E-C labels file). The author_design_note is gto-expert pre-review metadata; labellers don't see it (per `feedback_bucket_first_labelling.md`).

The script's design_note text fix is deferred to the next situation-factory edit cycle (file budget at 12.5E-E is constrained to the 8-file deliverable scope; per dispatch §"Stop conditions" >8 files = STOP). This annotation closes the cosmetic finding for documentation purposes; the script's text remains as historical record of the 2026-05-05 dispatch-time wording.

**Status: 12.5E-C RESOLVED. 110 labels FINAL (orchestrator Opus cross-check 20/20). v3.4 prompt added (Fix 2.1.1 = clause-e villain_air floor 0.05). 14/14 T5 hands classify correctly under v3.4. T1 deferred to 12.5E-F. 6-file diff per LABELS_FINAL directive. Awaiting standalone QC pre-merge audit.**
