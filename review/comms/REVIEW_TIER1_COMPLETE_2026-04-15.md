---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Owner + Builder
re: Review of Tier 1 completion — Track 3.5 BLOCKED-ambiguity, Track 5 no-op, Track 2 authorisation
status: REVIEW + DIRECTIVE — owner decision required on Track 3.5 blocker
---

# Tier 1 Completion Review

## Summary

| Track | Verdict |
|---|---|
| 1 Harness hardening | ACCEPT (prior review) |
| 3 Training audit | ACCEPT (prior review) |
| **3.5 ANOMALY-A verification** | **ACCEPT deliverable, ENDORSE blocked-ambiguity call — owner decision needed on path forward** |
| 5 BP generator fix | ACCEPT no-op finding with one caveat (batch2) |
| 2 FB-40 / MW-50 re-eval | **AUTHORISED to launch** (protocol permits; independent of 3.5) |
| 4 MW bias deep-dive | Remains held — see §3 recommendation |
| 6 Scope corrections | Remains held on Track 4 |

---

## 1. Track 3.5 Review — ANOMALY_A_VERIFICATION_2026-04-15.md

### What's strong
- **Correctly escalated scope.** Builder caught that `hero_position` has the same mixed encoding as `street` — audit missed it. Scope is ~2× what Track 3 reported. This is exactly the kind of tightening the hardened-harness discipline is meant to produce.
- **Root cause cited to source.** BP-series factory generators at specific file:line (`review/generate_factory_batch5.py:65-78`, etc.) emit strings. d-series extractor emits ints. Phase 3.5H assembly (`9dd1a68`) merged without normalising. This is a clean diagnosis.
- **Correct stop-protocol behaviour.** The v2.2 trainer script is not in git. Instead of improvising from the in-tree `train_model.py` (which would crash on the v2.2 CSV), builder reported BLOCKED-ambiguity per CLAUDE.md. This is the right call.
- **Test-first deliverable in place.** `test_training_data_encoding.py` fails 3/1 on the current CSV, will flip green once generators normalise. Integration-ready for v2.3 pre-flight.
- **Honest uncertainty framing.** The 5-path loader table in §2 is a model of how to report ambiguity: enumerate possibilities, rule out what's provably eliminated (path 1 — would have crashed), and flag what remains distinguishable only by recovering the script.

### Concerns / caveats
- **"Silent-zero" worst case is plausible but not the most likely path.** Of the surviving paths (2, 3, 5), path 2 (NaN-as-missing) is the most common pandas/XGBoost pattern and is consistent with CV 93% / holdout 88%. Path 5 (silent-zero via error-suppressed float cast) is uncommon in production pipelines — most loaders either crash or emit NaN. Builder's report appropriately does not pick a path, but the 99-row "corrupted" framing in §3 risks being over-cited as a finding.
- **Report does not attempt feature-importance cross-check.** If the `street` and `hero_position` columns carried low XGBoost gain in the v2.2 model, path 2 is functionally indistinguishable from clean data. If they carry high gain, corruption is more impactful. The training report at `river-rats-core/models/v2_2_training_report.json` may contain feature importances — worth checking in a follow-up before committing to "held under worst-case."
- **No mention of whether the Track 1 hardened harness catches this class of error at eval time.** The harness guards against missing features; does it guard against string-where-numeric-expected? If it does, Track 2 (FB-40 re-eval) will surface this independently. If it doesn't, we should extend the guard — this is a small ask but closes the loop.

### Verdict
**ACCEPT the report. ENDORSE the BLOCKED-ambiguity call.** Do not take this as a "corruption confirmed" finding — it is a "corruption possible on 48% of rows, severity contingent on loader behaviour we cannot read" finding. That distinction matters for how we frame Gate 7.

---

## 2. Track 5 Review — no-op verification

### What's strong
- Builder verified all 4 blueprint fixes line-by-line rather than assuming prior-session commits did the right thing. Correct discipline after the Track 1/3 recovery episode.
- Pytest evidence cited (1036 pass / 11 fail / 128 skipped) with the 11 failures attributed to unrelated missing-model-artefact issues.

### Concerns
- **The 11 preexisting failures are tolerated but not triaged.** `test_oracle_router.py` and `test_attention_experiments.py` missing `gto_model_v8_hu.json` is separate from the v2 stream, but a clean `pytest` baseline is worth having before Track 2 / Track 4 run. Low priority, flag for a future cleanup track.
- **batch2 blueprint divergence.** Builder correctly did not improvise. Blueprint section 7 marks it LOW priority. Owner: confirm whether we want an Architecture Expert call to update the batch2 portion of the blueprint, or drop it for v2.3. My recommendation: drop it unless a v2.3 supplement hand is sourced from batch2 — in which case it becomes a real blocker.

### Verdict
**ACCEPT. Minor follow-up items logged, not blocking.**

---

## 3. Owner decision required — Track 3.5 path forward

Builder presented three options. My recommendation with reasoning:

### Option 1 — Accept BLOCKED-ambiguity, proceed Track 4 under worst-case

**Pros:** Keeps momentum. Track 4 output would be a sensitivity analysis ("if path 5, bias is street-confusion; if path 2/3, bias is bucket-first") rather than a single diagnosis. That's informative.

**Cons:** Any Track 4 conclusion has a massive disclaimer attached. Track 6 (Track A scope correction) would then need to fork on path assumption. Cascade of ambiguity into v2.3 design.

### Option 2 — Recover / rewrite the v2.2 trainer before Track 4

**Pros:** Produces a citable, reproducible v2.2 trainer checked into `river-rats-core/`. Closes the ambiguity. Protects all future audits. Aligns with the "no in-flight work without source in repo" principle.

**Cons:** Labour — likely 1–2 agent calls for rewrite + verification that rerun reproduces CV 93% / holdout 88% / FB-40 72.5% / MW 80%. A rerun that doesn't match those numbers creates its own investigation.

### Option 3 (my recommendation) — Hybrid

1. **Authorise Track 2 now** (already done below). The hardened harness re-evaluation on FB-40 and MW-50 is independent of Track 3.5 and produces a clean data point.
2. **Before Track 4:** spend one programmer call on a **feature-importance cross-check** — read `v2_2_training_report.json` (or load the model and compute gain). If `street` and `hero_position` are low-gain, the worst-case impact is bounded regardless of loader path. This is a 30-minute test that potentially collapses Options 1 and 2 into "low-impact, proceed."
3. **If feature importance on those two columns is non-trivial:** commit to Option 2 — recover/rewrite the v2.2 trainer. No Track 4 under ambiguity on features the model leans on.
4. **Option 1 is only right if** we accept that v2.2 is a one-off and v2.3 will regenerate from fixed upstream (Fix 1 in the ANOMALY-A report) — which removes the need to know what v2.2 actually did. That's a defensible position but the owner should name it explicitly.

The cheap check in step 2 is worth doing before committing to the labour of Option 2.

### Gate 7 implication

Whichever option is chosen: **Gate 7 reasoning is now incomplete.** The solver verification pending on 10 MW misses was framed as "is the bucket-first CHECK bias real?" That framing assumed the model saw correct features. If ANOMALY-A corrupted training at path-5 severity, the bias is partially an artifact of street confusion. Owner should see the solver output + Track 4 output + feature-importance cross-check before deciding ship vs iterate.

---

## 4. Track 2 authorisation

Builder flagged Track 2 as "ready, awaiting go-ahead." Per the parallel-tracks directive and CLAUDE.md — Track 2 is Gate 7-independent, does not modify data or model, and uses the already-accepted Track 1 hardened harness. **Authorised. Launch Track 2 now.**

Ask on the Track 2 deliverable:
- Confirm FB-40 still lands at 72.5% with the hardened harness.
- Confirm MW-50 still lands at 80.0% with the hardened harness, and report the one-hand swap (d2920 in, d4534 out) explicitly.
- **Additional ask:** does the hardened harness reject the current `v2_2_training.csv` at evaluation if fed back through it? (It shouldn't need to — eval doesn't read training CSV — but if the extractor or any shared code hits string `street`/`hero_position`, we learn that here.)

---

## 5. Tier 1 / Tier 2 state (reviewer view)

| Track | Status after this review |
|---|---|
| 1 Harness hardening | ✅ done |
| 3 Training audit | ✅ done |
| 3.5 ANOMALY-A | ⚠️ Report accepted, owner decision pending on path forward |
| 5 BP generator fix | ✅ no-op verified; batch2 flagged low priority |
| 2 FB-40 / MW-50 re-eval | 🟢 AUTHORISED to launch now |
| 4 MW bias deep-dive | ⏸️ held — path conditional on owner's 3.5 decision |
| 6 Scope corrections | ⏸️ held on Track 4 |

---

## 6. What to watch for next

- `BUILDER_STATUS_2026-04-15-b.md` (or similar) — confirming Track 2 launch and reporting results.
- Owner direction on Track 3.5 (Option 1 / 2 / 3 / other).
- Solver verification results from owner on 10 MW misses (still outstanding).

I will check `ls -lt review/comms/ | head -10` periodically and will not batch commits — each directive or review pushes immediately.
