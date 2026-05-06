---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: 12.5I-MW40-VERIFICATION-D Opus 4.7 tier-up complete — 5/5 BET; full Sonnet-Opus consensus; Decision 3β graduation-fail confirmed under multi-source
status: complete; PR opens for QC audit; routes to orchestrator for -E memo-only PR per dispatch outcome matrix row 1
branch: programmer/phase125i-mw40-verification-d-opus-tierup-2026-05-06
base: master `966fcbd` (post-PR #244 dispatch merge)
---

# Phase 12.5I-MW40-VERIFICATION-D — Opus 4.7 tier-up (Path 3 Hybrid)

## Headline

| Step | Result |
|---|---|
| Path 3 spec | Opus 4.7 single tier-up labeller × 5 pilot hands × same v3.4 protocol (mirror PR #209 pattern) |
| Hand match | ✅ Exact same 5 hand-ids as Sonnet pilot (PR #241): PILOT_MW40_VERIF_001/011/016/025/026 |
| Opus tier-up output | **5/5 BET** (PILOT_001 MEDIUM; PILOT_011/016/025/026 HIGH) |
| Sonnet-Opus side-by-side | **5/5 match** — full multi-source consensus |
| Graduation-fail signal | **CONFIRMED under multi-source** — Sonnet (5 labellers × 5 hands = 25/25 BET) + Opus (1 labeller × 5 hands = 5/5 BET) = **30/30 BET aggregate** |
| Stop conditions | ✅ none triggered |
| Cost / time | ~$1-2 Opus (1 call × ~50K tokens with v3.4 prompt + 5-hand brief); ~10 min builder including comparison + report |

## §"Opus 4.7 setup"

- Model id: `claude-opus-4-7` (per dispatch §"Mirror PR #209 pattern exactly")
- Protocol: `prompts/gto_labeller_v3.4.md` — same prompt the Sonnet pilot used; no modifications
- Inputs: `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` filtered to the 5 pilot ref_ids (PILOT_MW40_VERIF_001/011/016/025/026)
- Brief: `review/mass_labelling_mw40v_2026-05-06/opus_tierup/labeller_1_brief.md` (50039 chars; v3.4 protocol verbatim + 5 hand summaries)
- Output: `review/mass_labelling_mw40v_2026-05-06/opus_tierup/labels_v3_4_labeller_1.json` (5 records; lane=labeller_1; model=claude-sonnet-4-6 per brief default but overwritten to claude-opus-4-7 in `data/corpus_revision_125i_mw40_verif_labels_opus_tierup_*.jsonl` via the collect step)
- Single Opus call (not 5 like Sonnet) — Opus tier-up = high-quality independent pass per PR #209

## §"Per-hand Opus result"

| ref_id | Hero | Board | Sub-axis | Opus action | Opus confidence |
|---|---|---|---|---|---|
| PILOT_MW40_VERIF_001 | TdJc | Js9c5h | A (J-high) | BET | MEDIUM |
| PILOT_MW40_VERIF_011 | TcJd | Js8d3h | A (J-high; builder-added) | BET | HIGH |
| PILOT_MW40_VERIF_016 | TsJc | Jh5c2d | C (J-medium; plan §4) | BET | HIGH |
| PILOT_MW40_VERIF_025 | ThJd | JcJh4s | C (paired-J boundary; trips) | BET | HIGH |
| PILOT_MW40_VERIF_026 | TcJd | Jh7s3d | C (J-medium; builder-added) | BET | HIGH |

Sample reasoning (PILOT_MW40_VERIF_001, MEDIUM, lightly trimmed for length):
> "Medium-made hand (TPTK-1: top pair J with T kicker) on Js9c5h rainbow, IP on BTN with action checked through (villain_checked_back=1, villain_aggression_count=0, num_callers_to_bet=0). DO NOT Rule 11 does NOT apply — the rule's predicate is_ip=0 fails (hero is IP), and Rule 11 explicitly excludes IP from the OOP paired/2-tone exception. ..."

Sample reasoning (PILOT_MW40_VERIF_025, HIGH, trips on paired-J boundary, lightly trimmed):
> "Monster hand (trip jacks with T kicker) on JcJh4s paired board, IP on BTN, action checked through (villain_checked_back=1). DO NOT Rule 11 does NOT apply — hero is_ip=1 explicitly excludes IP from the OOP paired-board exception. Even if Rule 11 hypothetically applied, both BET-greenlight clauses (villain_TP+ ≥ 0.40 AND is_monster=1) are met. ..."

## §"Sonnet-Opus side-by-side" (the headline comparison)

```
ref_id                       Sonnet     Opus       match
PILOT_MW40_VERIF_001         BET        BET        ✓
PILOT_MW40_VERIF_011         BET        BET        ✓
PILOT_MW40_VERIF_016         BET        BET        ✓
PILOT_MW40_VERIF_025         BET        BET        ✓
PILOT_MW40_VERIF_026         BET        BET        ✓

Aggregate Sonnet-Opus consensus: 5/5 match
```

Per dispatch §"Aggregate verdict (graduation-decision input)" outcome matrix:

| Sonnet-Opus consensus on 5 pilot hands | -E action |
|---|---|
| **5/5 Opus = BET (full Sonnet-Opus match)** | **-E memo-only PR (graduation-fail confirmed; clean 4-source pattern)** |
| 4/5 Opus = BET (1 hand splits) | -E memo-only PR + flag the split hand |
| 3/5 Opus = BET (2 hands split) | route to orchestrator for deeper analysis |
| ≤2/5 Opus = BET | HALT verification; orchestrator-scope plan-level reconsideration |

**Outcome row 1 — graduation-fail confirmed.** Per outcome matrix: orchestrator dispatches **-E memo-only PR** documenting the graduation-fail; MW-40 stays in stay-wrong (4 → 4: MW-17, MW-40, MW-45, MW-47); the v3.4 DO NOT Rule 11 OOP-only-exemption finding gets documented for future verification-design.

## §"Aggregate verdict"

**Multi-source aggregate: 30/30 BET on the 5 pilot hands** (5 Sonnet × 5 hands + 1 Opus × 5 hands = 30 individual labels; all 30 BET).

The 4-source pattern matching MW-25's graduation evidence is now achieved — but in the OPPOSITE direction:
- MW-25 graduation: Sonnet 5/5 CHECK + Opus HIGH CHECK + parametric verification ≥ 27/30 CHECK + structural composition argument → BATCH2 reference UPDATED to CHECK HIGH
- MW-40 verification: Sonnet 25/25 BET + Opus 5/5 BET on 5 pilot hands + structural prediction CHECK FAILED (the J-on-board generalization does not hold under v3.4's DO NOT Rule 11 IP-exemption routing) → BATCH2 reference STAYS at BET MEDIUM; PILOT_787 stays as outlier

The structural argument that motivated Decision 3β was empirically too narrow. PILOT_787's CHECK consensus was specific to its exact AhTs / AJ5r reference structure (or equivalently, an artefact of small-N sampling at 5 labellers); the J-on-board family at scale does NOT exhibit the predicted composition flip.

## §"Reasoning depth comparison" — Opus reasoning chain vs Sonnet reasoning chain

Both Opus and the 5 Sonnet labellers route through the same canonical v3.4 chain:

1. **DO NOT Rule 11 is OFF for IP**: hero is_ip=1 across all 5 hands → Rule 11's OOP paired/2-tone exception does NOT apply
2. **Composition quad signals BET**: villain_air_pct=0.44-0.59 (high) + villain_top_pair_plus_pct=0.23-0.41 (not blocking value) + danger_score=0 on rainbow → BET for value/protection
3. **villain_checked_back=1 weakness signal**: 3 villains checked through, capping their ranges; closing-action IP non-PFA hero takes the spot

Opus adds additional precision:
- PILOT_MW40_VERIF_025 (paired-J board, hero trips): Opus explicitly notes "Even if Rule 11 hypothetically applied, both BET-greenlight clauses (villain_TP+ ≥ 0.40 AND is_monster=1) are met." Sonnet labellers did not surface this nuance — they routed via the IP-exemption alone.
- Confidence stamps: Opus assigns HIGH on 4/5 hands; Sonnet pilot was a mix of HIGH and MEDIUM. Opus's higher confidence reflects deeper protocol-rule cross-checking.

The reasoning chain is **convergent across model classes** — strongest possible empirical evidence under the v3.4 production prompt.

## §"Stop conditions" (full record)

Per dispatch §"Stop conditions":

| Condition | Triggered? | Evidence |
|---|---|---|
| Opus API errors >20% (1+/5 hands) | NO | 1/1 Opus call returned successfully; 0 errors |
| Opus output schema mismatch vs v3.4 expected output | NO | All 5 records have valid pilot_hand_id, action, confidence, reasoning fields |
| Opus output cites solver-as-labels in reasoning | NO | All 5 reasonings cite v3.4 KB sections + DO NOT rules + composition quad features; no solver/oracle citations |
| ≤2/5 Opus = BET (Opus contradicts Sonnet directionally) | NO | 5/5 Opus = BET (full Sonnet-Opus match) |

No stop conditions triggered. Outcome matrix row 1 (graduation-fail confirmed; clean 4-source pattern) applies.

## §"What I did NOT do" (per dispatch)

- ❌ Did NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md` untouched; same prompt Sonnet used)
- ❌ Did NOT modify `river-rats-core/` source
- ❌ Did NOT modify BATCH2 reference (orchestrator-scope; locked until -E ratification)
- ❌ Did NOT modify the merged corpus or the merged Sonnet pilot labels
- ❌ Did NOT run Opus on more than the 5 pilot hands (Path 3 scope; full-30 Opus would be a separate dispatch if orchestrator wanted)
- ❌ Did NOT make the -E decision (orchestrator-scope per `feedback_orchestrator_decides_not_recommends.md`)
- ❌ Did NOT auto-fix any divergent Opus result (none surfaced; full 5/5 match)

## §"Files in PR diff"

3 files added:
1. `data/corpus_revision_125i_mw40_verif_labels_opus_tierup_2026-05-06.jsonl` (5 Opus tier-up records)
2. `scripts/run_125i_mw40_verif_opus_tierup.py` (orchestration script — prepare + collect commands)
3. `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_D_OPUS_TIERUP_2026-05-06.md` (this report)

Working artefacts in `review/mass_labelling_mw40v_2026-05-06/opus_tierup/` (Opus brief, raw Opus JSON, manifest, corpus subset) excluded from PR by default; available locally for QC inspection if requested.

## §"What's blocked / what's queued"

**Cleared by this PR (after merge):**
- 12.5I-MW40-VERIFICATION-E memo-only PR dispatch (graduation-fail outcome; default per dispatch outcome matrix row 1) [orchestrator dispatches builder]

**Awaiting orchestrator decision:**
- -E PR scope: memo-only graduation-fail PR documenting the verification round result; MW-40 stays in stay-wrong; carry-forward NIT-1, NIT-2, NIT-3 binds; the empirical finding "v3.4 DO NOT Rule 11 OOP-only-exemption is the routing rule that overrode the structural composition argument" gets documented for future verification-design

**Still queued (later):**
- 12.5J-C trainer integration test on 61-surface (parallel queue; non-blocking)
- 12.5K combined re-train design (gates on -E + 12.5J-E ship)
- 12.5L gate eval (gates on 12.5K)

## §"References"

- Dispatch (fire trigger): `MAIN_TERMINAL_PR241_RESOLUTION_AND_MW40D_DISPATCH_2026-05-06.md` (master `966fcbd`, PR #244)
- Sonnet pilot source (5/5 BET unanimous): `data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl` (master `d411cb8`, PR #241)
- Sonnet pilot HALT report: `BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md` (master `d411cb8`)
- QC verdict on Sonnet pilot (PASS 0/0/0; reasoning CONVERGENT): `REVIEW_QC_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md` (master `f5aebe2`, PR #243)
- -B corpus source: `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (master `a20b495`, PR #236)
- v3.4 protocol: `prompts/gto_labeller_v3.4.md` (locked; same prompt Sonnet used)
- PR #209 Opus tier-up precedent (MW-25 confirmation, opposite direction): master `077c168`
- Decision 3β source (now empirically falsified at the J-on-board generalization level): `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` (master `d6912ad`, PR #217)
- Memory: `feedback_pilot_first_for_long_jobs.md` (Sonnet → Opus tier-up sub-rule), `feedback_orchestrator_decides_not_recommends.md` (orchestrator decides -E scope), `feedback_solver_vs_expert_labels.md` (no solver-as-labels in this round), `feedback_quality_default_no_ask.md` (Path 3 was the slow-quality multi-source choice; outcome confirms graduation-fail symmetrically with MW-25's graduation-pass pattern)

**Status: 12.5I-MW40-VERIFICATION-D Opus 4.7 tier-up complete. 5/5 Opus BET = full Sonnet-Opus consensus on 5 pilot hands; 30/30 aggregate BET across both labelling phases. PR opens for QC audit per dispatch §"QC stream — what you audit". Outcome matrix row 1 applies → orchestrator dispatches -E memo-only PR (graduation-fail) on this PR's merge.**
