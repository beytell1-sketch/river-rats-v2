---
date: 2026-04-26
from: River Rats QC stream
to: Logic builder · Main terminal (orchestrator) · Owner (briefed)
re: PR #45 pre-merge QC audit — Build D v1.0.1 (V-D9 hash-lock determinism fix-forward); APPROVE (clean); reviewer + QC CONVERGED on V-D9 closure
status: FLAG (advisory; pre-merge informational)
severity: APPROVE / V-D9 fully closed; no findings
PR head: 1d2c23e4b14d8e301ebd9d94113bbcbb46b871d4
full finding: ~/river-rats-qc/findings/2026-04-26-pr45-pre-merge-build-d-v1-0-1.md
---

# QC Pre-Merge Audit — PR #45 (Build D v1.0.1)

## Headline

**APPROVE.** PR #45 cleanly closes V-D9 hash-lock determinism finding. `random.seed(SEED=20260426)` added at module load before `feature_extractor.extract_all_features` MC equity calls. Two-run byte-identical verified per builder PR body. Reviewer concurred APPROVE at commit `3c24ae2`. **TC-15 CONVERGED.**

## V-D9 closure

### Static
```python
SEED = 20260426
import random
random.seed(SEED)
```
At module load (lines 47-52). Comment explicitly references V-D9 closure. Same SEED as Build C v1.0.1 (consistency).

### Dynamic
```
$ sha256sum data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl
98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319
$ python3 scripts/build_phase_a5_partial_fold_fixtures.py
$ sha256sum data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl
98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319
# IDENTICAL — V-D9 closed
```

QC's local hash equality verified.

## Vector results

| Vector | Result |
|--------|--------|
| V-D1 fixture count = 5 | ✅ PASS |
| V-D2 each has fold | ✅ PASS |
| V-D3 villain_positions = LIVE only | ✅ PASS (preserved) |
| V-D4 num_opponents matches len(villain_positions) | ✅ PASS (preserved 3,2,1,3,2) |
| V-D5 59-feature feat_dict | ✅ PASS (preserved) |
| V-D6 provenance | ✅ PASS (sidecar v1.0.1 attestation + v1_0_to_v1_0_1_change note) |
| V-D7 SHA256 hash-lock | ✅ PASS — `98e4309a...4319` declared = computed |
| V-D8 TC-23 file existence | ✅ PASS |
| V-D9 build-process determinism | ✅ **CLOSED** — random.seed(SEED) at module load; two-run byte-identical |
| V-X3 disjointness vs pilot 100 corpus | ✅ PASS (preserved) |

## Hash transition

| | v1.0 (PR #43) | v1.0.1 (this PR) |
|---|---|---|
| SHA256 | `c196fb...0f513` | `98e4309a...4319` |
| Bytes | 10,761 | 10,760 |
| Determinism | Non-reproducible | Two-run byte-identical |

Same 5 fixture specs verbatim; only equity-derived feat_dict fields differ (now deterministic).

## Multi-expert verdict

CONVERGED. Reviewer + QC both APPROVE. V-D9 (originally surfaced by reviewer's PR #43 audit + QC tick-47 curative) is exactly the issue this PR closes. Convergence on the FIX = high confidence.

## Recommendation

**APPROVE merge.** No findings. After merge:
- PR #43 closes as superseded
- PRE-DISPATCH gate fully resolved (rows #2/#3/#5/#6 GREEN; V-X2 + V-D9 closed)
- Pilot dispatch resumes
- QC resumes Layer 3 pilot-runtime watch

## Process learning

- Module-level `random.seed(SEED)` is the canonical pattern for spec-vs-process determinism when downstream stochastic calls are unseeded.
- TC-15 protocol-diversity worked end-to-end Build D v1.0 → v1.0.1 (mirroring Build C v1.0 → v1.0.1): reviewer flagged determinism; orchestrator fix-forward; v1.0.1 cleanly closes; CONVERGED close verdict.

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-pr45-pre-merge-build-d-v1-0-1.md`
- PR #45: https://github.com/beytell1-sketch/river-rats-v2/pull/45
- V-D9 origin: `REVIEW_VERDICT_PR_43_BUILD_D_2026-04-26.md` + QC tick-47 incident #19
- Orchestrator decision: `MAIN_TERMINAL_PR43_DECISION_FIX_FORWARD_VD9_2026-04-26.md` (`47275da`)

**Status: APPROVE. V-D9 closed. Recommend merge.**
