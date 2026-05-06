---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #241 PASS+0/0/0 (25th solo cycle; reasoning CONVERGENT; empirical signal robust); merge PR #241 + PR #243; ratify Path 3 (Hybrid Opus tier-up on 5 pilot hands); dispatch 12.5I-MW40-VERIFICATION-D Opus tier-up
status: DIRECTIVE — merges PR #241 + PR #243; ratifies Path 3; fires LEAD-PROGRAMMER on -D Opus tier-up — fire now
---

# PR #241 + PR #243 merge + Path 3 ratification + 12.5I-MW40-VERIFICATION-D Opus tier-up dispatch

QC verdict on PR #241 (`REVIEW_QC_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md` on `qc/pr241-mw40-verification-c-pilot-review-2026-05-06`, PR #243): **PASS — 0 BLOCKER, 0 SHOULD_FIX, 0 NIT (25th solo cycle).** All 8 HALT-format audit items PASS. **Critical item 3 (reasoning convergence vs mode collapse) verdict: CONVERGENT.** The 25/25 BET unanimous result is empirically robust — 5 labellers each cite the v3.4 protocol-rule chain (DO NOT Rule 11 OOP-only exemption + villain_checked_back weakness signal + composition quad villain_air_pct=0.44-0.59 + danger_score=0 on rainbow → value/protection BET routing) with inter-labeller phrasing variation (= convergent reasoning, NOT mode collapse).

**Conclusion: the structural prediction "J-on-board flips composition triple toward CHECK on TPMK T-kicker 4-way checked-through" does NOT generalize from PILOT_787 to J-on-board parametric variants under the v3.4 production-prompt labelling protocol.** PILOT_787's CHECK was anomalous relative to the broader pattern; the structural argument was empirically too narrow.

## Path ratification — Path 3 (Hybrid Opus tier-up on 5 pilot hands)

QC verdict offered no preference between Path 1 (scale-anyway), Path 2 (halt-verification), Path 3 (Hybrid Opus). Per quality-default analysis:

### Decision: Path 3 selected

**Reasoning** per `feedback_quality_default_no_ask.md` + `feedback_pilot_first_for_long_jobs.md` sub-rule:

The pilot evidence is unanimous (25/25 BET at 1.00 confidence) AND convergent (5 labellers, same v3.4 protocol-rule chain). Path 2 (halt with Sonnet alone) would suffice for graduation-fail; the evidence is conclusive at the labelling-pipeline layer. BUT the slow-quality default mirrors the MW-25 4-source graduation pattern: graduation decisions (pass OR fail) gain integrity from multi-source confirmation. PR #209 ran Opus 4.7 tier-up on MW-25 to confirm Sonnet's 5/5 CHECK pilot; the same pattern applied here on the failing direction is the symmetric quality-default.

Path 1 (scale-anyway full 30 × 5 Sonnet) costs ~$5-8 to confirm what pilot already says with the same labelling pipeline (Sonnet + v3.4 prompt). Adding more Sonnet labels of the same configuration is REDUNDANT. Multi-source means a DIFFERENT model class (Opus); that's Path 3.

Path 3 cost: ~$2-5 Opus on 5 pilot hands; ~10-20 min wall clock. Cheaper AND more informative than Path 1.

### Outcome interpretation matrix

After -D Opus tier-up on the 5 pilot hands:

| Opus result | Interpretation | Next action |
|---|---|---|
| 5/5 BET (Sonnet-Opus consensus) | **Graduation-fail confirmed under both production and tier-up models.** Structural argument empirically too narrow. | Dispatch -E memo-only PR documenting graduation-fail; MW-40 stays in stay-wrong; document the v3.4 DO NOT Rule 11 finding for future structural-argument design |
| 4/5 BET, 1 CHECK (≥1 split) | **Mostly graduation-fail with minor labelling sensitivity.** Suggests the structural argument exists at the margin but isn't dominant under v3.4 protocol routing. | Dispatch -E memo-only PR (graduation-fail) + flag the 1 CHECK hand as a candidate for follow-up phase analysis |
| 3/5 BET, 2 CHECK (genuine split) | **Sonnet-Opus split.** Structural argument has model-class sensitivity. | Surface to orchestrator for deeper analysis; consider scaling Opus to 30 hands OR routing back to plan revision; do NOT merge -E yet |
| ≥3/5 CHECK (Opus contradicts Sonnet directionally) | **Significant Sonnet-Opus split.** v3.4 production-prompt labels diverge from Opus-tier-up labels on this pattern. | HALT verification round; route to orchestrator for plan-level reconsideration. Possibly indicates v3.4 prompt has a routing bug for this hand class. Owner-scope decision required. |

The default-and-most-likely outcome is "5/5 BET" or "4/5 BET" (mirrors MW-25's strong Sonnet-Opus consensus pattern). Path 3 is configured to gracefully handle all 4 outcomes.

## LEAD-PROGRAMMER — Step: 12.5I-MW40-VERIFICATION-D Opus tier-up (fire on this comm merge)

Per `MAIN_TERMINAL_PR236_RATIFY_AND_MW40C_DISPATCH_2026-05-06.md` (master `3927024`, PR #240) §"Sequencing — what fires after -B merges" item 4 (originally queued post-C QC PASS; now adapted for HALT-format -C with Path 3 Hybrid Opus on the 5 pilot hands).

Branch: `programmer/phase125i-mw40-verification-d-opus-tierup-2026-05-06`. Base: master post-this-comm-merge.

### Scope — Opus 4.7 tier-up on 5 pilot hands

Same 5 hands the Sonnet pilot batch used. Read the pilot ref_ids from `data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl` (PR #241; 5 distinct hand-ids). Run Opus 4.7 with the SAME v3.4 production prompt (`prompts/gto_labeller_v3.4.md`) — single invocation per hand (Opus is the tier-up model; not 5 labellers, just 1 high-quality pass per hand mirroring the PR #209 pattern).

**Mirror PR #209 pattern exactly:**
- Opus 4.7 (claude-opus-4-7) — single labeller per hand
- Same v3.4 protocol prompt — no prompt modifications
- Same constraint table inputs (read from -B corpus row)
- Output per hand: action + confidence + reasoning text
- Cost: ~$0.50-1.00 per Opus call × 5 hands = ~$2-5 total
- Wall clock: ~10-20 min

### Comparison output

For each of the 5 hands, builder report includes side-by-side:
- Sonnet pilot consensus (5/5 BET 1.00 conf; reasoning chain summary)
- Opus 4.7 result (action + confidence + reasoning text)
- Match/diverge flag

### Aggregate verdict (graduation-decision input)

Builder report's §"Aggregate Sonnet-Opus comparison" produces the input for the orchestrator's -E decision:

| Sonnet-Opus consensus on 5 pilot hands | -E action |
|---|---|
| 5/5 Opus = BET (full Sonnet-Opus match) | -E memo-only PR (graduation-fail confirmed; clean 4-source pattern) |
| 4/5 Opus = BET (1 hand splits) | -E memo-only PR + flag the split hand for follow-up |
| 3/5 Opus = BET (2 hands split) | route to orchestrator for deeper analysis (no -E yet) |
| ≤2/5 Opus = BET (Opus contradicts Sonnet directionally) | HALT verification; route to orchestrator |

Builder does NOT make the -E decision; builder produces the comparison data and routes to orchestrator (per `feedback_orchestrator_decides_not_recommends.md`).

### Stop conditions

- Opus API errors >20% (1+/5 hands) → STOP and report (infrastructure issue; orchestrator decides retry vs investigate)
- Opus output schema mismatch vs v3.4 expected output (action / confidence / reasoning) → STOP
- Opus output cites solver-as-labels in reasoning → STOP per `feedback_solver_vs_expert_labels.md`
- ≤2/5 Opus = BET (Opus contradicts Sonnet directionally) → STOP at this scale; route to orchestrator (do NOT proceed to broader Opus run without orchestrator directive)

### What you do NOT do

- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source
- Do NOT modify BATCH2 reference (orchestrator-scope; locked until -E ratification)
- Do NOT modify the merged corpus or the merged pilot labels
- Do NOT run Opus on more than the 5 pilot hands (Path 3 scope)
- Do NOT make the -E decision (orchestrator-scope per `feedback_orchestrator_decides_not_recommends.md`)
- Do NOT auto-fix any divergent Opus result (route to orchestrator)

### Cost / time

~$2-5 (Opus on 5 hands; ~$0.50-1.00 per call). ~10-20 min builder wall clock including comparison + report.

### Deliverable scope

Expected files in PR diff:
1. `data/corpus_revision_125i_mw40_verif_labels_opus_tierup_2026-05-06.jsonl` (5 Opus labels; same schema as Sonnet pilot)
2. `scripts/run_125i_mw40_verif_opus_tierup.py` (orchestration script; mirrors PR #209's Opus tier-up pattern)
3. `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_D_OPUS_TIERUP_2026-05-06.md` (the report)

### Builder report sections (mandatory)

- §"Opus 4.7 setup" — model id; same v3.4 prompt; identical hand inputs as Sonnet pilot
- §"Per-hand Opus result" — 5 hands × 1 Opus call; action + confidence + reasoning text per hand
- §"Sonnet-Opus side-by-side" — 5-row comparison table (Sonnet consensus / Opus action / match-diverge)
- §"Aggregate verdict" — Sonnet-Opus match/divergence summary; routing decision per outcome matrix above
- §"Reasoning depth comparison" — qualitative note on whether Opus reasoning chain matches Sonnet's DO NOT Rule 11 + composition quad chain, or routes via different rules
- §"Stop conditions" — full record (which triggered, which didn't)
- §"References" — PR #209 Opus tier-up precedent; PR #241 Sonnet pilot source

## QC stream — what you audit (when -D PR opens)

Standalone audit, ~10-15 min, 7-item scope (HALT-tier-up format):

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly the 3 expected files. NO touch to v3.x prompts, BATCH2, river-rats-core/, training-data, existing corpora, plan, memory.
2. **Opus 4.7 model id correctness** — verify `claude-opus-4-7` exact (not Sonnet, not Haiku, not opus-3); cite PR #209 precedent.
3. **Same v3.4 prompt** — Opus called with `prompts/gto_labeller_v3.4.md` content; no prompt modifications.
4. **5 hands matched** — Opus run on EXACTLY the same 5 hand-ids as Sonnet pilot in PR #241; no hand swaps.
5. **No solver-as-labels in Opus reasoning** — Opus output should cite v3.4 protocol rules, not solver outputs.
6. **Sonnet-Opus comparison correctness** — table rows match the actual data; match/diverge flags computed correctly.
7. **TC-X-DISPATCH-COMPLIANCE (5th formal exercise)** — Path 3 implemented; Opus only on 5 hands (not 30 like Path 1); no auto-fix on divergent result.

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_D_OPUS_TIERUP_2026-05-06.md` on `qc/pr<N>-mw40-verification-d-review-2026-05-06`.

## Sequencing — what fires after -D merges

Conditional on Opus outcome (per outcome matrix above):

1. **Default outcome (4-5/5 Opus = BET)** → Dispatch **12.5I-MW40-VERIFICATION-E memo-only PR** (graduation-fail). MW-40 stays in stay-wrong: 4 → 4 (MW-17, MW-40, MW-45, MW-47). NIT-1, NIT-2, NIT-3 fold-forward applied. The structural-argument-empirically-too-narrow finding gets documented for future verification design.
2. **Split outcome (3/5 Opus = BET, 2 split)** → Route to orchestrator for deeper analysis; -E held.
3. **Contradiction outcome (≤2/5 Opus = BET)** → HALT verification; orchestrator-scope plan-level reconsideration; -E held; potentially escalate to owner.

After -E (whichever variant) merges:
- 12.5J-C trainer integration test on 61-surface (parallel queue; non-blocking)
- 12.5K combined re-train design (gates on 12.5I-E + 12.5J-E ship)
- 12.5L gate eval (gates on 12.5K)

## What's blocked / what's queued

**Cleared by this comm:**
- PR #241 merge (Builder pilot HALT)
- PR #243 merge (QC verdict record)
- 12.5I-MW40-VERIFICATION-D Opus tier-up dispatch fires
- Path 3 (Hybrid Opus on 5 pilot hands) ratified

**Newly queued (after -D merges):**
- 12.5I-MW40-VERIFICATION-E memo-only PR (graduation-fail) [default outcome]
- OR orchestrator escalation [split / contradiction outcome]

**Still queued (later):**
- 12.5J-C trainer integration test on 61-surface
- 12.5K combined re-train design
- 12.5L gate eval

**Owner-scope items pending (informational, non-blocking):**
- TC-X-INTRA-PLAN-CONSISTENCY curative addition to `learning/test_class_registry.md` (1 surfaced finding now: PR #236 SHOULD_FIX-1; class is delivering value)
- TC-X-DISPATCH-COMPLIANCE curative addition (4 exercises now: PR #228 surfaced + PR #232 PASS + PR #236 PASS + PR #241 PASS)
- Memory note refresh for "composition quad" vs "composition triple" terminology drift (NIT-1 carry-forward to -E)
- The empirical finding from -C pilot HALT (DO NOT Rule 11 OOP-only exemption is the routing rule that overrode the structural composition argument) is itself a candidate for memory: structural arguments must cross-check against v3.4 DO NOT rules before submission to verification rounds

## References

- PR #241 (Builder pilot HALT; 25/25 BET): branch `programmer/phase125i-mw40-verification-c-labelling-2026-05-06`, head `4e3b34c`
- PR #243 (QC PASS 0/0/0; reasoning CONVERGENT verdict): branch `qc/pr241-mw40-verification-c-pilot-review-2026-05-06`
- PR #242 (QC trigger): master `aea6488`
- PR #240 (orchestrator: -C dispatch with halt condition that triggered): master `3927024`
- PR #209 (Opus 4.7 MW-25 tier-up; the precedent for -D Opus tier-up pattern): master `077c168`
- PR #213 (PILOT_787 Sonnet 3-2 source; original 3-source evidence Decision 3β tested): master `994ae67`
- v3.4 prompt protocol (DO NOT Rule 11 OOP-only exemption; the rule that overrode structural composition argument): `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_quality_default_no_ask.md` (Path 3 selection), `feedback_orchestrator_decides_not_recommends.md` (orchestrator decides path), `feedback_pilot_first_for_long_jobs.md` (sub-rule: training-data outputs require Sonnet→Opus tier-up), `feedback_orchestration_efficiency_rules.md` (single comm: ratification + merge + dispatch), `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`

**Status: PR #241 + PR #243 cleared for merge. Path 3 (Hybrid Opus on 5 pilot hands) ratified. LEAD-PROGRAMMER fires 12.5I-MW40-VERIFICATION-D Opus tier-up on this comm merge. ~10-20 min wall clock + ~$2-5 Opus to PR open.**
