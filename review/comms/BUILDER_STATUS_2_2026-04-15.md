---
date: 2026-04-15
from: Builder
to: Main terminal / Owner
re: Round 2 status — cross-check forces Branch B, Track 2 also blocked, Fix 1 done
status: AWAITING DIRECTION on trainer recovery
---

# Builder Status #2

Four parallel jobs landed. Summary of pushed commits:

| Commit | Track | Result |
|---|---|---|
| `6501cbb` | Track 4 prep + batch2 disposition | ✅ done |
| `96212cc` | Track 3.5 cross-check | ✅ done — **Branch C → B** |
| `573dbb2` | Track 2 (FB-40/MW-50 re-eval) | ⚠️ partial — dtype guard landed; eval BLOCKED |
| `b69e668` | Fix 1 BP generators + pre-flight gate | ✅ done with caveats |

## Cross-check verdict (commit `96212cc`)

`street` is rank **20/108** by gain (0.943%), `hero_position` rank
44/108 (0.317%), combined 1.26%. The attention-mirror columns
(`attn_street`, `attn_hero_position`) have zero gain (never split).

**Branch decision:** Combined gain is well under 5% (Branch A
threshold) BUT `street` sits at rank 20 — inside the Branch C
borderline band (15–25). Per `MAIN_TERMINAL_UPDATE_2026-04-15-c.md`
§4, Branch C defaults to Branch B (NON-TRIVIAL) — quality
over speed.

**Consequence:** Track 4 stays HELD; trainer recovery required
before bias diagnosis can proceed.

Top-10 sanity check passed: equity_margin (15.0%), attn_pot_odds
(13.0%), facing_bet (9.8%), raw_equity (6.0%), better_hand_pct
(5.9%), etc. — usual suspects at the top, model gain distribution
is healthy.

## Track 2 — same blocker as Track 3.5 (commit `573dbb2`)

Hardened harness in `reference_evaluator.py` is 54-feature.
`v2_2_model.json` is 108-feature (54 raw + 54 `attn_*` with
legal-action masking). The eval script that produced 72.5% / 80.0%
is **not in the repo** — same gap as the v2.2 trainer.

Did not improvise a 108-feature inference path (stop condition).
Dtype-guard test-first deliverable did land: 4 new tests under
`TestDtypeGuard`, full harness suite 16/16, guards at both
`GtoOracle.features_from_dict` (TypeError) and
`_validate_feat_dict` (ValueError with column names + hand id).

**Track 2 unblocks at the same time as Track 4** — both need the
108-feature eval path recovered or rewritten.

## Fix 1 BP generators (commit `b69e668`)

- `normalise_situation()` helper added to `situation_factory.py`.
  Mapping verified: STREET (flop=0/turn=1/river=2),
  POSITION (UTG=0,HJ=1,CO=2,BTN=3,SB=4,BB=5) — confirmed against
  `feature_extractor.py:28-35`.
- All 5 generators patched at serialisation.
- factory_batch5_situations.jsonl regenerated in-place
  (185 string-encoded street + hero_position rows → numeric).
  Other 4 batch JSONLs were already numeric — no changes.
- Pre-flight schema gate wired in `train_model.py` —
  `_preflight_schema_check()` runs before training; raises
  `RuntimeError` listing offending files on mixed-encoding detect.
- Schema test: 18 pass, 2 skip, 3 fail. The 3 failures are on
  `v2_2_training.csv` (forbidden to regenerate per directive). All
  10 BP-JSONL assertions + 6 `normalise_situation()` unit tests
  PASS.

**Caveats:**
1. `v2_2_training.csv` remains corrupted per task constraint;
   pre-flight gate will block any v2.3 training attempt until
   regenerated from clean BP JSONLs.
2. Pre-existing `hand_sequence_validator` strictness +
   `generate_factory_batch4.py` count mismatch ("BP1: expected 30,
   got 32") prevent full `generate_all()` runs. Source is correctly
   patched; in-place transform delivered the same data outcome.
   These are pre-existing defects, not Fix 1 regressions.
3. Hard-coded `/home/rupertbeytell/...` paths in the generators
   were replaced with `__file__`-relative derivations (portable
   across checkouts).

## Track 4 prep (commit `6501cbb`)

10/10 MW-miss hands extracted via `extract_all_features()` →
`review/comms/MW_MISSES_FEATURES_PREP_2026-04-15.jsonl` (all 54/54
features populated, HRP range 0.43–0.83 matches HRP investigation).
Manifest at `…_PREP_2026-04-15.md`. Ready for Track 4 GTO analysis
once unblocked.

## Batch2 disposition (commit `6501cbb`)

**OUT OF SCOPE.** No fix spec needed. Justification at
`review/comms/BATCH2_DISPOSITION_2026-04-15.md`:
- Output JSONL lacks `villain_positions` plural — distinct schema
- Single git commit for both script + output (not regenerated)
- Only consumers: `check_leakage.py`, `review/deterministic_labeller.py`
  — neither on v2.2/v2.3 training hot path
- Tier 1 review already recommended dropping
- Blueprint §7 marked LOW priority

Track 5 is now fully closed.

## Updated track grid

| Track | Status | Tier |
|---|---|---|
| 1 Harness hardening | ✅ done (b5d84b5) | 1 |
| 3 Training audit | ✅ done (8e77e05) | 1 |
| 3.5 ANOMALY-A verify | ✅ done (498e076) | 1 |
| 3.5 cross-check | ✅ done — **Branch B** (96212cc) | 1 |
| 5 BP generator fix | ✅ no-op + Fix 1 (b69e668) | 1 |
| Batch2 disposition | ✅ out of scope (6501cbb) | 1 |
| 2 FB/MW re-eval | ⚠️ BLOCKED on eval-script absence | 2 |
| 4 MW bias deep-dive | ⏸️ HELD on trainer recovery (Branch B) | 2 |
| 4 prep (data only) | ✅ done (6501cbb) | 1 |
| 6 Scope corrections | ⏸️ HELD on Track 4 | 2 |

## What's next — owner decision required

Per `MAIN_TERMINAL_UPDATE_2026-04-15-c.md` §4 Branch B and the
remote-control note flagging "checking your local machines /
shell history may save a rewrite":

**Path 1 — Owner-side recovery (preferred per remote-control note):**
Owner checks local machines, shell history, notebooks for the
v2.2 training script and the 108-feature eval script. If found,
move them into `river-rats-core/` and confirm. This unblocks
Track 2 + Track 4 immediately.

**Path 2 — Builder rewrites (Branch B fallback):**
If recovery fails, Builder rewrites:
- `river-rats-core/train_model_v2_2.py` from training report +
  CSV schema
- A 108-feature eval path extension to `reference_evaluator.py`
  (or new `evaluate_v2_2.py`)
Verifies trainer reproduces CV 93.0% ± 3.5% / holdout 88.3%.

I will not start rewriting unless directed — Branch B specifies
recovery first.

## Awaiting

- Owner direction on Path 1 vs Path 2
- Anything else surfacing in `MAIN_TERMINAL_UPDATE_*`

I'll keep checking the comms folder.
