---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #175 (12.5H-B' amendment — T7-ext SUITED-NFD redesign) — APPROVE; 1 MEDIUM advisory (dispatch prediction empirically falsified; builder caught + flagged)
severity: MEDIUM (1 — load-bearing for 12.5H-C re-pilot prediction-update planning); no HIGH; no BLOCKER
status: FLAG → APPROVE for merge
test-class: TC-23 + V-Source + dispatch §"NEW: T7-ext discriminative axis" + §"Convention uniformity" + §"NEW: PILOT_693 v3.4 prediction sanity"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 11th successive cycle solo-routed)
---

# QC Review — PR #175 (12.5H-B' amendment): APPROVE; 1 MEDIUM (orchestrator-side prediction update needed)

## Verdict

**APPROVE PR #175 for merge.** All 5 dispatch-required audits processed. 4 PASS cleanly; Audit 5 surfaces a MEDIUM-class finding — dispatch's CALL prediction is empirically falsified by v3.4 protocol walk (PILOT_693 villain_air = 0.312 → carve-out fires → RAISE), but builder transparently caught + flagged + the amendment's substantive purpose (resolve FOLD anti-training risk) IS achieved (12/12 T7-ext hands produce non-FOLD outcomes under v3.4).

The MEDIUM finding is orchestrator-side prediction text needing update before 12.5H-C re-pilot, NOT a builder issue and NOT a HOLD condition. Builder report line 90 already documents the gap.

QC FLAG-only role per CLAUDE.md.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR175_2026-05-06.md` master `0c15354` + PR #174 dispatch)

5 audits — 3 standard + 2 NEW for amendment-specific verification.

PR #175 head: `fcb2aa1` (branch `programmer/phase125h-b-prime-amendment-2026-05-06`). Merge-base: `c01b799` (= PR #173 PILOT HALT).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 4 files; only T7-ext factory + JSONL regen + manual canonical change + builder report update; no other template touched"*

| File | additions | deletions | category |
|---|---|---|---|
| `scripts/build_corpus_revision_125h_situations.py` | 59 | 39 | UPDATE (T7-ext config redesign) |
| `data/corpus_revision_125h_situations_2026-05-06.jsonl` | 82 | 82 | REGEN (full row replacement) |
| `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` | 6 | 6 | UPDATE (PILOT_693 row swap) |
| `review/comms/BUILDER_REPORT_PHASE125H_B_SITUATION_GENERATION_2026-05-06.md` | 88 | 6 | UPDATE (amendment section prepended) |
| **Total** | **+235** | **-133** | **4 files** ✓ |

- File count = 4 ✓
- Zero edits to `prompts/`, `river-rats-core/`, or other-corpus data files ✓
- Per-template counts UNCHANGED (only T7-ext rows regenerated; T8'/T9'/T10'/T-RAISE-stabilize/T-CONTROL untouched per dispatch §"Path C scope") ✓

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

9 distinct file paths cited; all 9 TRACKED at master HEAD (the PR-modified files exist at master from prior PR #169 merge; amendment overwrites on merge).

## Audit 3 — T7-ext discriminative axis ✅ BIT-EXACT

**Dispatch:** *"verify all 12 T7-ext hands (parametric + manuals) have `has_flush_draw=1` AND `nut_flush_block=1`; programmatic check on the JSONL"*

Programmatic check on `feat_dict.has_flush_draw` and `feat_dict.nut_flush_block` for all T7-ext hands (parametric `t7ext_suited_nfd_nut_blocker_call_pot_odds` + manual `T7ext`):

| Cohort | Count | All `has_flush_draw=1` | All `nut_flush_block=1` |
|---|---|---|---|
| T7-ext parametric | 11 | ✅ 11/11 | ✅ 11/11 |
| T7-ext manual (PILOT_693) | 1 | ✅ 1/1 | ✅ 1/1 |
| **Total** | **12** | ✅ **12/12** | ✅ **12/12** |

Distribution check:
- `has_flush_draw` values: `{1: 12}` ✓ (no other values)
- `nut_flush_block` values: `{1: 12}` ✓ (no other values)

**T7-ext discriminative axis: BIT-EXACT.** Path C SUITED-NFD redesign achieves the redesigned discriminative target on all 12 hands.

## Audit 4 — Convention uniformity (preserved) ✅ CLEAN

**Dispatch:** *"all 90 `prior_actions` use hero-only (preserved from original)"*

Programmatic check on all 90 prior_actions (84 parametric + 6 manuals): **0 violations.** Convention preserved across the amendment.

## Audit 5 (NEW) — PILOT_693 v3.4 prediction sanity ⚠️ MEDIUM-1

**Dispatch:** *"verify the new SUITED PILOT_693 v3.4 prediction = CALL by walking the v3.4 protocol clause set on the new spec"*

### QC walk on PILOT_693 (independent verification)

PILOT_693 facts (extracted from amended JSONL):
- hero_cards: `AdKd`
- board: `Jd8d4c` (two-tone, two diamonds)
- street: flop
- hero_position: BB
- facing_bet: True
- num_opponents: 2
- prior_actions: `["preflop: BB call", "flop: BB check"]` (hero-only convention)
- feat_dict: `has_flush_draw=1`, `nut_flush_block=1`, `villain_air_pct=0.312`, `villain_call_count=0`, `villain_aggression_count=1`, `raw_equity=0.463`

### v3.4 protocol clause walk

1. **Carve-out predicate (a)/(b)/(c):** has_flush_draw=1 + nut_flush_block=1 + OOP relative to bettor + bet-alone-multiway (`villain_call_count=0`, `villain_aggression_count=1`) → predicate eligible for KB §1.7
2. **v3.3 Fix 2.1 carve-out (bet+call multiway):** requires `villain_call_count >= 1`. Here 0 → NOT triggered.
3. **v3.4 Fix 2.1.1 clause-e floor (bet+call multiway with air ≥ 0.05):** N/A since v3.3 carve-out doesn't trigger.
4. **v3.2 KB §1.7 OVERRIDE base case (HU or bet-alone-multiway):** requires `villain_air_pct >= 0.20`. Here **0.312 ≥ 0.20** → carve-out **FIRES** → **RAISE**.

**QC walk produces RAISE, NOT CALL.**

### Builder's independent verification (matches QC)

Builder report line 79 (4-hand verification subagent run table):

| pilot_hand_id | hero | board | villain_air_pct | v3.2 ≥ 0.20 threshold | predicted action |
|---|---|---|---:|:---:|:---:|
| PILOT_647 | AhKh | Jh9h3c | 0.047 | FAILS | **CALL** |
| PILOT_651 | AdKd | Jd9d3c | 0.282 | PASSES | **RAISE** (KB §1.7 fires) |
| PILOT_656 | AcKc | Jc9c3d | 0.282 | PASSES | **RAISE** (KB §1.7 fires) |
| **PILOT_693** | AdKd | Jd8d4c | **0.312** | **PASSES** | **RAISE (KB §1.7 fires)** |

Builder report line 90 explicitly flags the orchestrator-side prediction error:

> *"Note on orchestrator-side prediction: Dispatch §'Updated 12.5H-C predictions' predicted CALL for the new PILOT_693. Actual v3.4 verification produces RAISE because villain_air_pct = 0.312 (> 0.20 threshold) on the J-high two-tone with broadway-overcards hero. ... RAISE is GTO-correct and not a stop condition; flagging here for orchestrator's information so 12.5H-C re-pilot predictions can be updated to CALL/RAISE-mix-driven-by-villain_air rather than uniform CALL."*

QC + builder converge on RAISE. Both walks produce the same answer via the same v3.4 protocol clauses.

### Why this is MEDIUM not HOLD

A literal reading of dispatch line 19 ("verify v3.4 prediction = CALL") would HOLD. But:

1. **Substantive purpose achieved:** the amendment's primary goal per dispatch §"Path C objective" was to resolve FOLD anti-training risk. 12/12 T7-ext hands produce non-FOLD outcomes under v3.4 (split between RAISE and CALL based on villain_air). FOLD anti-training is empirically resolved. ✓
2. **GTO correctness preserved:** RAISE on PILOT_693 is GTO-correct under v3.4 protocol — the carve-out predicate is satisfied + villain_air clears the 0.20 threshold. The amendment does not introduce GTO-incorrect labels.
3. **Builder transparently caught + flagged:** report line 90 explicitly documents the orchestrator-side prediction error. No hidden divergence.
4. **Dispatch §"Sequencing on QC verdict" line 27** says: *"APPROVE → orchestrator merges; re-triggers 12.5H-C labelling round with **updated predictions** per PR #174"* — "with updated predictions" anticipates the prediction text may need amendment between merge and re-pilot.
5. **HOLD would route back to LEAD-PROGRAMMER for amendment** — but the issue is the orchestrator-side dispatch prediction wording, not the builder's data. Routing to builder for "fix" makes no sense; the right correction is orchestrator updating their dispatch text.

So: APPROVE the amendment. MEDIUM-1 advisory: orchestrator updates 12.5H-C re-pilot predictions to reflect the actual v3.4 protocol output (CALL when villain_air < 0.20; RAISE when villain_air ≥ 0.20) BEFORE re-triggering 12.5H-C labelling.

### Suggested fix-forward (advisory)

Before re-triggering 12.5H-C labelling round, orchestrator updates the predictions document for T7-ext hands per the actual v3.4 protocol output. The 4-hand verification table in builder report line 79 provides the canonical mapping; the rest of the 11 parametric T7-ext hands follow the same air-driven split.

### Severity rationale

**MEDIUM** because:
- Load-bearing for 12.5H-C re-pilot dispatch (predictions inform labelling-round expected outcomes)
- Empirically falsifies a specific dispatch prediction
- Builder caught + flagged transparently — process working
- Not a HOLD because amendment is GTO-sound + serves substantive purpose

NOT HIGH because:
- The carve-out math is correct under v3.4 protocol
- Builder's verification is independent + converges with QC
- No data corruption or training contamination risk

## Bonus — pattern: orchestrator-side prediction errors caught by builder self-review

This is the second instance in the cycle of orchestrator-side dispatch wording diverging from substantive reality (first: PR #169 NIT-1 §3/§4/§8 inconsistency on T-CONTROL count; this: PR #175 dispatch CALL prediction vs v3.4 actual RAISE). Both caught by builder self-review + transparently flagged. Pattern is healthy: orchestrator drafts at high cadence, builder + QC catch.

Could become **TC-X-DISPATCH-PREDICTION-VERIFICATION** sub-vector if recurs: when a dispatch makes a specific prediction about a deterministic protocol output (here: v3.4 protocol on a specific spec), QC walks the protocol independently to verify. Already operationalized informally; queue-worthy if a third instance appears.

## What QC did NOT audit (scope partition)

- **Per-hand poker correctness** of all 11 parametric T7-ext hands (whether AhKh on Jh9h3c is well-designed for the air=0.047 → CALL outcome) — gto-expert review at 12.5H-C re-pilot
- **Whether the air-driven RAISE/CALL split is the right corpus signal** for MW-17 — the amendment dispatch §"Honest implication of (c)" already flags MW-17 may not be fixed by 12.5H if E-FEATURE primary; that's an open empirical question for 12.5H-F gate evaluation
- **Updated dispatch wording** for 12.5H-C re-pilot — orchestrator scope post-merge

## Test class implication

- **TC-23 + amendment-scope discipline reproducible** — full-row regen with no out-of-scope template touches. Pattern reproducible.
- **Pattern: builder self-review catches orchestrator-side dispatch errors** — this is the second instance (after PR #169 NIT-1). Process is working as designed; healthy distributed verification.
- **Possible TC-X-DISPATCH-PREDICTION-VERIFICATION sub-vector** if recurs — when dispatch makes deterministic predictions about protocol outputs, QC walks the protocol independently.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **11th successive cycle solo-routed**. Loop heartbeat detected trigger landing within ~1 min of master push (loop fired immediately on `/loop` invocation).

## References

- PR #175: https://github.com/beytell1-sketch/river-rats-v2/pull/175
- PR #175 head: `fcb2aa1`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR175_2026-05-06.md` (master `0c15354`, PR #176)
- 12.5H-B' amendment dispatch: `MAIN_TERMINAL_PHASE125H_B_PRIME_AMEND_2026-05-06.md` (master `a84793c`, PR #174)
- PILOT HALT comm: `BUILDER_STATUS_PHASE125H_C_PILOT_HALT_2026-05-06.md` (master `c01b799`, PR #173)
- Memory: `feedback_qc_routing_when_standalone_active.md` (11th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #175 for merge.** All 5 audits processed; 4 PASS cleanly; Audit 5 surfaces MEDIUM-1 advisory (orchestrator-side prediction text needs update — builder's substantive output is GTO-correct).

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5H-C re-pilot dispatch
- **MEDIUM-1 fix-forward:** orchestrator updates T7-ext predictions to reflect actual v3.4 air-driven RAISE/CALL split (per builder report line 79 table) before 12.5H-C re-pilot labelling fires
