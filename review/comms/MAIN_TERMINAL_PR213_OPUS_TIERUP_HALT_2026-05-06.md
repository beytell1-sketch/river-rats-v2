---
date: 2026-05-06
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: PR #213 Opus 4.7 tier-up complete — 17/20 AGREE (BORDERLINE-17, fails strict 18/20 gate by 1); all 3 disagreements same non-structural T-kicker A-high 4-way checked-through pattern; PILOT_787 MW-40 EXACT Opus CHECK HIGH locks MW-40 graduation pathway
status: HALT — owner WHAT decisions required on PR #213 disposition + MW-25/MW-40 graduation lock
---

# PR #213 Opus tier-up — BORDERLINE-17 HALT

QC PASSed PR #213 with 0 findings (PR #215). Per `feedback_pilot_first_for_long_jobs.md` sub-rule, orchestrator-side Opus 4.7 gto-expert tier-up cross-check was dispatched on 20 hands across 3 templates. Final result: **17/20 AGREE; 3/20 DISAGREE; gate (≥18/20) NOT MET by 1 hand.** Per orchestrator rule "<18/20 → author HALT resolution comm, surface to owner": this comm.

## Opus tier-up summary (full evidence)

### Aggregate by family

| Template | n audited | AGREE | DISAGREE | Match rate |
|---|---|---|---|---|
| T8' (FD multiway, MW-25 family) | 8 | 8 | 0 | 100% |
| T9' (TPMK 4-way checked-through, MW-40 family) | 7 | 4 | 3 | 57% |
| T10' (slowplay-set + tail variants, MW-45 family) | 5 | 5 | 0 | 100% |
| **Total** | **20** | **17** | **3** | **85%** |

### The 3 disagreements — same non-structural pattern

All 3 are T9' family hands where Sonnet's 3-2 BET majority sat on the **defensible minority-mix branch** while Opus's first-principles read landed on the solver-modal CHECK action. Opus classifies all 3 as **mix-frequency, not structural** (no misapplied clauses; no GTO errors; just the lower-frequency leg of a true mixed strategy).

| ref_id | hand | board | kicker class | Sonnet 3-2 | Opus | classification |
|---|---|---|---|---|---|---|
| PILOT_727 | AdTh | Ac8s3d | T-kicker on A-high | BET (mix) | CHECK MEDIUM | mix-frequency (T-kicker leans CHECK modal) |
| PILOT_745 | KsTh | Kd9c2s | T-kicker on K-high | BET (mix) | CHECK MEDIUM | mix-frequency (T-kicker leans CHECK modal) |
| PILOT_725 | AhTd | As7c2d | T-kicker on A-high | BET (mix) | CHECK MEDIUM | mix-frequency (T-kicker leans CHECK modal; same shape as 727) |

The disagreement subzone is **narrow and identifiable**: T-kicker TPMK on A-high or K-high boards in 4-way checked-through SRP, IP non-PFA. PILOT_750 (J-kicker on K92r in same family) AGREED with Sonnet's BET — confirming the disagreement clusters specifically on the T-kicker subset, not on the broader T9' family. v3.4 protocol routed cleanly; the 3-2 split itself is Sonnet correctly flagging fragile mix-frequency uncertainty.

### Structural integrity

Opus's verbatim verdict on structural integrity:
> *"No structural errors emerged in this batch. The T9' family clusters its disagreements on the T-kicker-on-A-high subset specifically; J-kicker on K-high (PILOT_750) and presumably stronger-kicker variants align with Sonnet majority. Recommendation: BORDERLINE-17 is acceptable for downstream training given (a) all 3 disagreements are same-pattern non-structural mix-frequency, (b) confidence already calibrated low (0.6) on the strained subset, and (c) the disagreements cluster on a narrow, identifiable subzone (T-kicker / A-high / 4-way) that downstream attention vocab can flag."*

## PILOT_787 (MW-40 EXACT) — graduation pathway locked at HIGH

The single most load-bearing audit hand. Sonnet 3-2 CHECK majority at 0.6 confidence; Opus call **CHECK HIGH**. Three-source convergence locked:

| Source | Verdict on PILOT_787 (AhTs on AdJc5h, 4-way checked-through, IP non-PFA) | Confidence |
|---|---|---|
| Sonnet 5-labeller v3.4 ensemble | CHECK 0.6 (3-2) | MEDIUM |
| Opus 4.7 gto-expert independent re-eval | CHECK | **HIGH** |
| First-principles composition triple | CHECK | structural |

Opus's structural argument (verbatim):
> *"The Jack on board is the load-bearing feature. Villain TP+ rises to 0.211 (vs 0.170 on Ace-low boards) because AJ becomes 2-pair + AJ heavily in 4-way preflop calling ranges + J-x pairs (JJ, KJ, QJ) all enter as TP+/overpair. Villain air drops to 0.274 (vs 0.380). Raw equity falls to 0.215 (vs 0.314). Hero is dominated by AK, AQ, AND AJ — three full top-pair-better-kicker classes plus AJ two-pair, plus AA/JJ/55 sets. The composition triple is decisively against thin value."*

**This is the same shape as MW-25 graduation (PR #209).** A reference label that surface-level routing treats as BET but where the underlying composition triple structurally rejects BET. MW-40 reference (BATCH2 BET HIGH on AhTs/AdJc5h 4-way checked-through) is empirically refuted by Opus + Sonnet majority + structural argument.

## Owner WHAT decisions required (3 coupled)

Per `feedback_orchestrator_decides_not_recommends.md` (reference-set + scope changes are owner-scope):

### Decision 1 — PR #213 disposition (BORDERLINE-17 gate failure)

- **Option α (orchestrator recommendation):** merge PR #213 as-is. The 3 mix-frequency labels at 0.6 confidence already encode the uncertainty correctly — sample weighting in 12.5K combined re-train will down-weight them appropriately (vs 1.0 unanimous T8'). Document Opus findings in tier-up record. The narrow T-kicker subzone is addressable via attention vocab in 12.5J or 12.5L. Cost: 0.
- **Option β:** drop PILOT_727, PILOT_745, PILOT_725 from `data/corpus_revision_125i_labels_2026-05-06.jsonl` (consensus); preserve in raw labels for audit trail. Ship 91 hands instead of 94. Cleaner training signal at the cost of ~3% lost T9' coverage. Cost: 1 builder iteration + 1 mini QC delta-audit (~20 min, ~$0.50).
- **Option γ:** full HALT; revisit gate failure as a protocol-design question (e.g., "should T9' family carve out a separate T-kicker template for cleaner signal?"). Re-design 12.5I-A with explicit T-kicker isolation. Cost: ~2-4 hours design work; defers 12.5I-D and 12.5K.

**Recommendation: α.** All 3 disagreements are non-structural mix-frequency on a narrow identifiable subzone; 0.6 confidence is the natural sample-weight encoding of that uncertainty; β throws away signal that Sonnet's ensemble correctly flagged as fragile; γ is over-engineered for what is structurally a clean labelling round.

### Decision 2 — MW-25 BATCH2 reference update (carried forward; 4-source convergence + 30-hand consensus + Opus HIGH)

Now overdue. Three orchestrator surfacings since 08:16 SAST:

- **Option α (orchestrator silent-default per PR #209):** update `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` MW-25 from BET HIGH → CHECK HIGH; add MW-25 entry to `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`. Stay-wrong list 5 → 4. Lock as part of next phase dispatch (12.5I-D BATCH2 update PR).
- **Option β:** defer to 12.5L gate eval; ship 12.5I-D corpus QC against the unupdated reference (with footnote that MW-25 is empirically wrong on the reference but right in the model).

**Recommendation: α.** Evidence is now overwhelming (5/5 pilot + Opus HIGH + 30/30 unanimous + Sonnet protocol traces). Deferring to 12.5L just creates a known-wrong-reference footnote in 12.5I-D corpus QC.

### Decision 3 — MW-40 BATCH2 reference update (NEW; 3-source convergence)

Mirrors MW-25 graduation pathway. PILOT_787 Opus CHECK HIGH + Sonnet 3-2 CHECK + structural composition argument all converge.

- **Option α:** update `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` MW-40 from BET → CHECK HIGH; add MW-40 entry to `memory/reference_corrections.md`. Stay-wrong list 4 → 3 (assuming Decision 2 = α). Bundle into the same 12.5I-D BATCH2 update PR as MW-25.
- **Option β:** defer; require additional Opus-side or solver-side verification before locking. (Only Opus + Sonnet in current evidence; MW-25 had Opus + Sonnet + 30 unanimous parametric; MW-40 has Opus + Sonnet 3-2 with 1 EXACT canonical, no 30-hand parametric pattern.)

**Recommendation: α** but with a softer endorsement than MW-25. The structural argument is decisive (J-on-board flips composition triple identically to A-paired board flipping it for MW-25), but the parametric corpus support is thinner (1 canonical CHECK vs 32 BET parametrics — the parametrics are themselves at 0.6 mix-frequency confidence, not unanimous). β is defensible on slow-quality grounds (more verification before locking the reference). Owner's call.

## What's blocked / what's queued

**Blocked on owner WHAT (Decisions 1+2+3):**
- PR #213 merge (Decision 1)
- PR #215 (QC verdict record) merge — bundles with PR #213
- 12.5I-D corpus QC dispatch — needs PR #213 merged + Decision 2 path locked + Decision 3 path locked
- BATCH2 reference update PR — needs Decisions 2 and 3 locked (1 PR can carry both)
- 12.5J-D-pre test-guard deflake — independent of these (can dispatch in parallel; no blocker)

**In flight (independent):**
- None — builder idle pending direction.

**Queued post-resolution:**
- 12.5I-D corpus QC dispatch (after PR #213 merges)
- 12.5J-D-pre test-guard deflake dispatch (Option b: tier-2 Δ-tolerance)
- BATCH2 reference update PR (if Decisions 2+3 = α)
- 12.5K combined re-train design (after 12.5I-E + 12.5J-E ship)

## What you do not need to decide

- Sequencing of 12.5I-D vs 12.5J-D-pre: orchestrator-scope; will run 12.5J-D-pre in parallel (it's CI-only, doesn't touch corpus).
- QC routing for the next round: orchestrator-scope; standalone QC stream.
- Opus tier-up scope on 12.5I-D corpus QC: orchestrator-scope; will mirror this audit pattern.

## References

- PR #213: `programmer/phase125i-c-labelling-2026-05-06` (commit `5cfa5c1`)
- PR #215: `qc/pr213-labelling-review-2026-05-06` (QC PASS 0 findings)
- Opus tier-up evidence: this comm + agent transcripts (`add71f97253fb38a3` and `a4fbd37784c6e24b1` agent IDs in this session)
- 12.5I-C MW-25 resolution (graduation pathway precedent): master `077c168` (PR #209)
- BATCH2 reference: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` (MW-25 + MW-40 entries pending update)
- Memory: `feedback_pilot_first_for_long_jobs.md` (tier-up requirement), `feedback_orchestrator_decides_not_recommends.md` (reference + scope owner-scope), `feedback_quality_default_no_ask.md` (slow-quality default), `feedback_solver_findings.md` (mix-frequency labelling discipline), `reference_corrections.md` (will gain MW-25 + MW-40 entries on Decision 2/3 = α)

**Status: PR #213 Opus tier-up BORDERLINE-17. Three coupled owner WHAT decisions queued. Orchestrator recommendations: 1α + 2α + 3α. Builder + QC idle pending direction.**
