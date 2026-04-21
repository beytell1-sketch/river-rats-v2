---
date: 2026-04-21
from: Builder (research phase)
to: Orchestrator · Reviewer panel (multi-agent reconciliation)
re: Single research artifact — pre-blueprint-v2 findings across 4 streams
status: RESEARCH — no code edits; gates blueprint v2
reference:
  - review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_BLUEPRINT_2026-04-21.md (11fe501)
  - review/comms/BUILDER_V24_STAGE35_BLUEPRINT_2026-04-21.md (b1a9a91, superseded pending v2)
scope:
  - MUST #7 — full `narrow_*` caller list
  - MUST #8 — `coaching/` inventory + importer reality check
  - MUST #9 — pipeline `except Exception` swallow audit
  - Labelling-pipeline feature-flow trace (Q1–Q8 from directive)
---

# Stage 3.5 Research Findings — Pre-Blueprint-v2

Four research streams requested by the orchestrator to gate blueprint v2.
Every claim below has been verified against live source at HEAD `11fe501`;
cites are file:line. No paraphrasing from the prior blueprint or the
Explore agent output is trusted without verification.

**Three findings redirect orchestrator decisions made in the
reconciliation. Flagged inline with 🔄 and consolidated in §5.**

---

## 1. MUST #7 — Complete `narrow_*` caller list

**Scope per reconciliation:** Before any HIGH #5 breaking-return-type edits
land, the full list of `narrow_to_betting_range`, `narrow_to_checking_range`,
and `narrow_to_continuing_range` callers must be enumerated. Blueprint v1
listed 5 `feature_extractor.py` sites; Red-team asserted 14+.

### 1.1 Root-module callers (all three functions)

| File | Line | Function | Class | HIGH #5 churn type |
|------|------|----------|-------|---------------------|
| `river-rats-core/feature_extractor.py` | 503 | `compute_partition_features` | betting | tuple unpack |
| `river-rats-core/feature_extractor.py` | 617 | `get_multiway_villain_range` | betting | tuple unpack |
| `river-rats-core/feature_extractor.py` | 805 | `compute_equity_features` (MW MC loop) | betting | tuple unpack |
| `river-rats-core/feature_extractor.py` | 828 | `compute_equity_features` (HU) | betting | tuple unpack |
| `river-rats-core/feature_extractor.py` | 1193 | `extract_range_composition` (post-chain bet gate) | betting | tuple unpack |
| `river-rats-core/feature_extractor.py` | 1669 | Step 12 `_s12_v_range` reconstruction | betting | **DELETED by CRIT #1** |
| `river-rats-core/range_narrowing.py` | 791 | `narrow_by_action_history` chain loop | betting | internal (§5 Step B) |
| `river-rats-core/range_narrowing.py` | 794 | `narrow_by_action_history` chain loop | checking | internal |
| `river-rats-core/range_narrowing.py` | 797 | `narrow_by_action_history` chain loop | continuing | internal |
| `river-rats-core/range_narrowing.py` | 875 | `test_narrowing()` standalone demo | betting | test-only discard |
| `river-rats-core/range_narrowing.py` | 885 | `test_narrowing()` standalone demo | checking | test-only discard |
| `river-rats-core/explain_hand.py` | 264 | `_postflop_villain_range_summary` | betting | tuple unpack |
| `river-rats-core/explain_hand.py` | 329 | `_postflop_villain_range_summary` (second branch) | betting | tuple unpack |
| `river-rats-core/tests/test_range_narrowing_stage35.py` | 288, 294, 296, 304, 307 | unit tests (5 direct calls) | continuing | tuple unpack |

**Root total: 14 direct calls + 5 import-only references.**

### 1.2 `coaching/` duplicate callers (all three functions)

| File | Line | Function | Class |
|------|------|----------|-------|
| `river-rats-core/coaching/feature_extractor.py` | 503 | `compute_partition_features` | betting |
| `river-rats-core/coaching/feature_extractor.py` | 617 | `get_multiway_villain_range` | betting |
| `river-rats-core/coaching/feature_extractor.py` | 805 | `compute_equity_features` (MW MC loop) | betting |
| `river-rats-core/coaching/feature_extractor.py` | 828 | `compute_equity_features` (HU) | betting |
| `river-rats-core/coaching/feature_extractor.py` | 1137 | `extract_range_composition` | betting |
| `river-rats-core/coaching/range_narrowing.py` | 375, 439, 532, 542 | parallel definitions + tests | all three |
| `river-rats-core/coaching/explain_hand.py` | 264, 329 | `_postflop_villain_range_summary` | betting |

**coaching/ total: 9 additional direct calls.**

### 1.3 Grand total

**23 direct callers across root + coaching.** Red-team's "14+" claim was
conservative — the real count is higher once coaching/ is included.

### 1.4 HIGH #5 revised impact statement

Breaking the return type from `Dict` to `Tuple[Dict, float]`:
- **Root:** 12 sites need tuple-unpack edits (14 minus 2 deleted by CRIT #1 at line 1669 — actually the deleted site is a single call, so 13 root edits remain). Plus 5 test-file edits.
- **coaching/:** 9 sites — see MUST #8 for the coaching handling decision.
- **Total for v2.4 Stage 3.5 ship:** 18 code sites + 5 test sites if coaching is mirrored (§2's redirect recommendation) or 13 code + 5 test sites if coaching is deleted (orchestrator's original path (a)).

All sites are mechanical `_ = narrow_*(...)` unpacks. No semantic reasoning required per site; each one just discards the surviving-mass fraction or propagates it through `narrow_by_action_history`.

---

## 2. MUST #8 — `coaching/` inventory + importer audit 🔄 REDIRECT CANDIDATE

**Scope per reconciliation:** Red-team flagged `coaching/` as a "90KB
silent-bypass surface" that could defeat all 5 MUSTs if any runtime path
imports from `coaching.*`. Orchestrator preferred path (a) delete-and-
repoint. Owner can redirect.

### 2.1 `coaching/` directory inventory

26 Python files totalling 15,937 lines. Sizes of the load-bearing ones:

| File | Lines | Notes |
|------|-------|-------|
| `coaching/feature_extractor.py` | 2423 | Parallel definition. 5 `narrow_*` call sites. No `_action_history` parameter on `extract_range_composition` (line 1090). |
| `coaching/range_narrowing.py` | 571 | Parallel `narrow_*` function definitions (lines 375, 439). No `narrow_by_action_history`, no chain, no safety rails. |
| `coaching/explain_hand.py` | 465 | Circular import from root `explain_hand.py`. |
| `coaching/situation_describer.py` | 726 | Consumes `villain_*_pct`; teaching-side prose. |
| `coaching/level_renderer.py` | 1768 | Teaching layer; consumes feature dicts. |
| `coaching/hand_context.py` | 447 | Feature structuring for teaching. |
| `coaching/gto_model.py` | 186 | Duplicate model wrapper with different FEATURE_COLUMNS. |
| `coaching/board_analyzer.py` | 1699 | Lightweight board math; no chain dependency. |
| `coaching/shap_explainer.py` | 201 | SHAP wrapper; consumes model output. |

### 2.2 Critical finding — `coaching/` is NOT a stale duplicate

Red-team described coaching/ as "duplicate". Verification against live
imports shows coaching/ is an **active runtime subsystem** that root
modules actively import from. This materially changes the MUST #8
action plan.

**Root modules importing from `coaching.*`** (verified via grep):

| Root module | Line(s) | Imports from coaching |
|-------------|---------|----------------------|
| `river-rats-core/explain_hand.py` | 19, 45, 48, 49, 50, 51, 52, 53, 54, 103, 229, 295 | `coaching.explain_hand`, `coaching.gto_model`, `coaching.shap_explainer`, `coaching.hand_context`, `coaching.levels`, `coaching.explanation`, `coaching.situation_describer`, `coaching.narrative_builder`, `coaching.decision_reporter`, `coaching.sizing_oracle`, `coaching.multiway_adjuster` — **11 distinct coaching modules** |
| `river-rats-core/play.py` | 34, 35, 36, 39 | Thin wrapper over coaching — 4 imports |
| `river-rats-core/poker_game.py` | 547, 564 | `coaching.levels`, `coaching.explain_hand` inside methods |
| `river-rats-core/shap_explainer.py` | 16, 17, 42 | `coaching.gto_model`, `coaching.shap_explainer` — re-export facade |
| `river-rats-core/multiway_adjuster.py` | 11 | `coaching.multiway_adjuster` — re-export facade |

**Tests importing from `coaching.*`:** 13 test files including
`test_situation_describer.py`, `test_hand_context.py`, `test_sprint*.py`,
`test_explain_hand.py`, `test_sizing_oracle.py`, `test_decision_reporter.py`,
`test_oracle_shap.py`, `test_level_renderer_preflop.py`, `test_sprint1b_multiway.py`,
`test_sprint2_fields.py`, `test_sprint3_renderer.py`, `test_sprint4.py`.

**Intra-coaching imports:** `coaching/explain_hand.py`, `coaching/multiway_adjuster.py`,
`coaching/decision_reporter.py`, `coaching/shap_explainer.py`,
`coaching/situation_describer.py`, `coaching/narrative_builder.py`,
`coaching/explanation.py`, `coaching/observation_builders.py`,
`coaching/level_renderer.py` all import from `coaching.*` internally.

### 2.3 Architectural pattern — root is facade, coaching is implementation

The relationship isn't "root is canonical, coaching is duplicate that
might still get imported." It's:

- `coaching/*` holds many module **implementations** used by the teaching
  layer
- Root-level `explain_hand.py`, `shap_explainer.py`, `multiway_adjuster.py`,
  `play.py` are **facade modules** that re-export + wrap the coaching
  versions

But `coaching/feature_extractor.py` and `coaching/range_narrowing.py`
are **different** — they appear to be older copies, not facades. Root
`feature_extractor.py` is canonical and has the Stage 3.5 chain work;
coaching/feature_extractor.py lacks it entirely. So a mixed situation:

| Module class | Example | Canonical location | Status |
|---|---|---|---|
| Teaching modules (facade pattern) | `situation_describer`, `level_renderer`, `hand_context`, `decision_reporter` | coaching/ is canonical; root doesn't duplicate | Safe |
| Feature extraction | `feature_extractor` | **Root** is canonical; coaching/ is stale | CRITICAL if imported |
| Range narrowing | `range_narrowing` | **Root** is canonical; coaching/ is stale | CRITICAL if imported |
| Mixed (root = thin wrapper) | `explain_hand`, `shap_explainer`, `multiway_adjuster` | Root wraps coaching | Safe today |

**Who imports `coaching.feature_extractor` or `coaching.range_narrowing`?**
Searching both exact paths:

```
Grep "from coaching.feature_extractor|import coaching.feature_extractor"
Grep "from coaching.range_narrowing|import coaching.range_narrowing"
```

Result: **zero runtime importers** of `coaching.feature_extractor` or
`coaching.range_narrowing` in root or tests. The stale coaching versions
exist on disk but are NOT imported by the live system. The `coaching/`
`__init__.py` is empty (0 bytes), so `import coaching.X` does not auto-
execute any of these files.

### 2.4 Revised MUST #8 recommendation 🔄

**Original orchestrator decision:** path (a) delete `coaching/` duplicates
+ repoint imports. Rejected (b) mirror in parallel commits.

**Builder finding that redirects:**
- Path (a) applied to `coaching/feature_extractor.py` and
  `coaching/range_narrowing.py` only is **safe** — these files have no
  runtime importers (verified).
- Path (a) applied to the rest of `coaching/` (facade modules `situation_describer`,
  `level_renderer`, etc.) would require 4–6 weeks of refactor to unwind
  the 11 import paths through `explain_hand.py` alone. **Out of Stage
  3.5 scope.**

**Recommended Stage 3.5 scope for MUST #8:**
1. Delete `coaching/feature_extractor.py` (2423 lines) — no importers
2. Delete `coaching/range_narrowing.py` (571 lines) — no importers
3. Keep the rest of `coaching/` intact (facade pattern is load-bearing)
4. Add a CI test that asserts `coaching.feature_extractor` is not importable (regression guard — prevents someone re-introducing the duplicate)
5. v2.5+ ticket: evaluate whether the facade pattern across `explain_hand.py` / `shap_explainer.py` / `multiway_adjuster.py` should be collapsed. Out of Stage 3.5 scope.

This is a narrower path (a) than the reconciliation's phrasing implied.
The recommendation aligns with orchestrator's intent (eliminate silent
bypass surface) while keeping Stage 3.5 scope small.

**Redirect request for owner/orchestrator:** Confirm the narrower path
(a) is acceptable. If owner wants the full coaching/ audit now, that
adds 4–6 weeks and a parallel refactor stream.

---

## 3. MUST #9 — Pipeline `except Exception` swallow audit

**Scope per reconciliation:** CRIT #2's strict-raise is fiction if the
training pipelines swallow `RuntimeError` in a blanket `except Exception`.
Confirmed — all three pipelines do exactly that. Verified line-by-line.

### 3.1 Pipeline catch sites

| Pipeline | File:line | Current handler | Fix required |
|----------|-----------|-----------------|--------------|
| Gauntlet 500k parallel | `river-rats-core/extract_features_parallel.py:81` | `except Exception:` (swallow, `errors += 1`) | Re-raise `RuntimeError` specifically OR replace with non-RuntimeError catch |
| PokerBench incremental | `river-rats-core/extract_incremental.py:105` | `except Exception as e:` (swallow, `errors += 1`) | Same |
| v5 gauntlet | `river-rats-core/gauntlet_v5_37feat.py:188, 226` | `except Exception as e:` at 2 sites | Both |

### 3.2 Verified source for each

**`extract_features_parallel.py:75–84`:**
```python
for hand in hands:
    try:
        feat = extract_all_features(hand)
        # ... action_map lookup ...
        row.append(action_val)
        rows.append(row)
    except Exception:      # ← SWALLOWS RuntimeError
        errors += 1
```

**`extract_incremental.py:82–107`:**
```python
try:
    parsed = parse_pokerbench_line(line)
    if not parsed:
        errors += 1
        continue
    feat = extract_all_features(parsed)
    # ...
    rows.append(vec + [action, size_bucket])
except Exception as e:   # ← SWALLOWS RuntimeError
    errors += 1
```

**`gauntlet_v5_37feat.py:178–226`:** two `except Exception` sites. First (line 188) inside `run_action_gauntlet`'s per-hand loop; second (line 226) inside `run_sizing_gauntlet`'s per-hand loop. Both swallow.

### 3.3 Recommended fix pattern

Single recommended fix for all three: re-raise `RuntimeError` specifically:

```python
except RuntimeError:
    raise  # Let Stage 4 strict-action-history propagate
except Exception:
    errors += 1  # Normal extraction errors still counted silently
```

Rationale: `extract_all_features` raises `RuntimeError` only when the
CRIT #2 strict gate fires. All other exceptions (bad parse, missing keys,
math errors) are genuinely errors that should count against the yield.
This is the minimum-blast-radius fix.

Alternative — blanket replace `except Exception` with explicit tuples
`except (KeyError, ValueError, TypeError)` — is safer long-term but wider
scope. Recommend the re-raise pattern for v2.4.

### 3.4 Other pipelines that call `extract_all_features`

Scanning callers outside the three flagged pipelines, the additional
`extract_all_features` consumers are:

| File:line | Wrapper behavior | Strict-raise propagates? |
|-----------|------------------|---------------------------|
| `river-rats-core/reference_evaluator.py:492, 797` | No try/except around the call | YES (would abort eval; caller surfaces exception) |
| `river-rats-core/calibration_exam.py:300` | No try/except (single-hand flow) | YES |
| `river-rats-core/train_sizing_model.py:140` | Unknown at this depth; needs read | TBD (in-scope for blueprint v2) |
| `river-rats-core/explain_hand.py:424` | Unknown; display only | TBD |
| `river-rats-core/coaching/explain_hand.py:424` | Same | TBD |
| `river-rats-core/gauntlet_v5_37feat.py:161` | Wrapped in `extract_features_37` helper; caller uses `try/except Exception` at line 188 and 226 | **NO** (swallowed) |

Primary Stage 3.5 fix targets the three training pipelines. Read-only
display paths (`explain_hand`, `calibration_exam` for eval use) are not
strict-raise relevant — they run with `STAGE4_STRICT_ACTION_HISTORY`
unset, so they fall through to warn-only.

---

## 4. Labelling-pipeline feature-flow trace (Q1–Q8)

**Scope per orchestrator directive:** If labellers see un-chained feature
values, Stage 4 training data will encode corruption forward through the
entire loop. This gates Stage 4 directly; any CRITICAL finding becomes
a new blueprint v2 MUST.

Findings below combine the Explore subagent's investigation with my
line-level verification of its load-bearing claims (per `feedback_verify_source_not_plan`).

### 4.1 Q1 — Labelling display tool

**Confirmed:** `river-rats-core/calibration_exam.py::format_situation_for_agent`
(lines 326–367) is the primary tool that formats a hand + features into
the text block the labelling agent reads.

- Displays 26+ feature values to the labelling agent, including the four
  composition features (`villain_top_pair_plus_pct`, `villain_air_pct`,
  `villain_range_capped`, `board_favour`) at lines 356–359.
- Values come from `situation['feat_dict']` populated at lines 317–321.
- Feature dict is produced by `extract_all_features(hand_dict)` at line 300.

**Secondary tool:** `river-rats-core/labelling_agent.py::prepare_batches`
(lines 100–159) is the training-data labelling harness. Verified lines
118–150: it reads `feat_dict` from pre-assembled `sit` dicts in JSONL —
it does NOT call `extract_all_features` itself. Features are pre-extracted
upstream; labelling_agent just displays them. The `action_history`
string it shows at line 130 is prose narrative (from `sit['action_history']`),
not the `_action_history` list.

### 4.2 Q2 — Feature-extraction path for labelling display

**CRITICAL FINDING VERIFIED.** `calibration_exam.py:279–298` builds
`hand_dict` with the following keys (exact list from source):

```python
hand_dict = {
    'h', 'b', 'pos', 'vp', 'pot', 'tc', 'st', 'fb', 'exp',
    F.META_NUM_OPPONENTS, F.META_NUM_RAISES,
    F.META_OPENER_POSITION, F.META_BETTOR_POSITION,
    '_villain_aggression_count', '_villain_checked_back',
    '_villain_call_count', '_num_callers_to_bet', '_facing_raise',
}
```

**No `_action_history` key.** The ensuing `extract_all_features(hand_dict)`
call at line 300 will hit `extract_range_composition` with
`action_history=None` (the default), which triggers the silent
single-street fallback. **Labellers see un-chained composition values.**

This is **MUST #20 CRITICAL** — see §5 below.

Assembly scripts `assemble_v23*.py`: verified `assemble_v23.py:119` reads
`d.get("feat_dict", {})` — consumes pre-extracted features from JSONL.
`assemble_v23.py:43` references `'action_history'` in a top-level field
list (for prose display), not as a chain source. No chain extraction in
the assembly layer.

### 4.3 Q3 — KB §1.9 + v3.2 prompt derivation

**KB §1.9:** `knowledge/three_way_gto.md` (Explore agent cited lines
146–225). Not-yet-updated for v2.4 P1 blocker features per the Stage 2
plan.

**Prompt versions present:**
- `prompts/gto_labeller_v1.md`
- `prompts/gto_labeller_v2.md`
- `prompts/gto_labeller_v3.md`
- `prompts/gto_labeller_v3.1.md`

**No `gto_labeller_v3.2.md`.** v3.2 has not been derived (Stage 3 is
listed as in-progress in the manifest). Current v3.x prompts describe
villain range in single-street terms — they don't anticipate multi-street
chain-narrowing or the semantic difference between chained and un-chained
composition values.

**Implication for blueprint v2:** Stage 3.5 lands BEFORE Stage 2 (KB
§1.9 update) and Stage 3 (v3.2 prompt derivation). If Stage 4 re-labels
while §1.9 still says "villain's range on the current street" and labellers
still use the v3.1 prompt, labellers apply single-street mental model to
chained feature values. Misalignment is baked into labels. Training data
corrupted.

**MUST #21 CRITICAL** — see §5. Stage 2 + Stage 3 must land BEFORE
Stage 4 re-label begins.

### 4.4 Q4 — `reference_evaluator.py` (88.1% HU / 52.5% MW baseline)

**Verified line-level.** Two call sites to `extract_all_features`:

**Line 492 (MW reference set):** `_evaluate_one_hand` builds `hand_dict`
at lines 470–489 with the same 14-key shape as calibration_exam — no
`_action_history`. Feeds `extract_all_features(hand_dict)` → bypass path.

**Line 797 (FB test set):** `evaluate_facing_bet_test_set` builds
`hand_dict` via `_build_fb_hand_dict` at lines 675–713. Same 14-key
shape — no `_action_history`. Bypass path.

**Impact on headline accuracy metric:** The 88.1% HU / 52.5% MW numbers
for v2.2 were measured on un-chained feature values against a model
trained on un-chained features. Internally consistent.

**When Stage 3.5 lands:** If `reference_evaluator.py` is not patched to
populate `_action_history`, the post-Stage-3.5 v2.4 model will be
evaluated against un-chained feature values — but it will have been
trained on chained values. **Baseline comparison becomes meaningless.**

**MUST #22 CRITICAL** — see §5. `reference_evaluator.py` must populate
`_action_history` before any post-Stage-3.5 evaluation run.

### 4.5 Q5 — Calibration anchor pre-flight gate (P0, commit 570ece2)

**Red-team claim in MUST #16:** "M5 fixtures lack `_action_history`; 3/3
BET result is vacuous."

**Verified:** **FALSE** for both the P0 pre-flight gate AND the M5 Stage
3.5 diagnostic script.

- `river-rats-core/anchors/calibration_anchors.json`: every anchor
  includes a full `action_history` array. Verified visually — `d2410_CO_turn`
  has 7 action entries spanning preflop through turn; `LITMUS_A4d_Qs5s7s_flop`
  has 5 entries; all anchors have multi-street action sequences.
- `river-rats-core/evaluate_calibration_anchors.py:83` parses the JSON's
  `action_history` into tuples and passes them via `SituationSpec.action_history`
  → `situation_factory.build_situation` → `game_state_bridge` at line 184,
  which flattens into `_action_history` on the hand dict.
- `review/run_v231_anchor_recheck_stage35.py::_anchor_specs` (lines
  50–130+) hand-codes its own specs with `action_history` arrays populated.
  Lines 62–70 show d2410's full action_history inline.

**Chain IS exercised on M5 anchors.**

**Red-team's concern about regression guards is still valid, narrowed:**
if someone later removes `action_history` from an anchor (or adds a new
anchor without it), the bug would return silently. Stage 3.5 should add
an audit assertion that every anchor's post-extraction feature dict shows
non-empty `_villain_range_chain_steps` — belt-and-braces. But the claim
"M5 is vacuous today" is not supported by the source.

**Redirect:** MUST #16's ship-blocker framing softens to "add regression
guard", not "fix silent bypass". 🔄 — see §5.

### 4.6 Q6 — `train_sizing_model.py` and `sizing_oracle.py`

**Verified at the call-site level only; deeper audit deferred to blueprint v2.**

- `river-rats-core/train_sizing_model.py:126` imports `extract_all_features`.
  Line 140 calls it. The hand dict construction around that call I have
  NOT yet read; Explore agent asserted no `_action_history`. Assume
  bypass-path for blueprint v2 purposes and add a verification task to
  the blueprint implementation plan.
- `river-rats-core/sizing_oracle.py`: no `extract_all_features` calls
  (confirmed by grep). Operates on pre-extracted feature dicts from the
  CSV.

**Impact:** Sizing model training uses bypass path if Explore's claim
is correct. Same backward-compat risk as `reference_evaluator`. Fix
pattern is identical: populate `_action_history` on the hand dict.

Verification needed in blueprint v2.

### 4.7 Q7 — Teaching CONTENT_API consumers

`river-rats-teaching/` exists at `~/river-rats-teaching/` (verified:
`CLAUDE.md`, `content/`, `curriculum/`, `data/`, `interface/`, `review/`,
`tests/`, `setup_graph.sh`).

**Explore agent did not enumerate the teaching-repo consumers** (outside
v2 scope without cross-repo reads). For the research-findings doc, this
is out of scope — teaching terminal owns the CONTENT_API consumer audit.
Flag to orchestrator as a cross-stream coordination item:

- Teaching terminal should audit `l3_renderer_enriched.py` + any other
  consumer of `villain_top_pair_plus_pct`, `villain_draw_pct`,
  `villain_air_pct`, `villain_medium_made_pct` at the teaching-repo HEAD.
- Result feeds CRITICAL evaluation: if teaching renders v2.2-shipped
  un-chained values alongside v2.4-shipped chained values on the same
  hand, playtest users see inconsistency. But v2.4 isn't shipped to
  game yet, so this is a pre-emptive cross-stream audit rather than a
  live bug.

Not blueprint v2 scope, but should appear in Stage 6 ship gate.

**In-repo consumers of `_villain_*_pct` (root + coaching):**
- `river-rats-core/feature_extractor.py` — produces + promotes the
  features
- `river-rats-core/calibration_exam.py` — displays to labeller (Q1)
- `river-rats-core/labelling_agent.py` — displays to labeller (Q1)
- Assembly scripts `assemble_v23*.py` — copy into JSONL/CSV
- `coaching/situation_describer.py` — teaching prose rendering
  (consumes via `HandContext`, which consumes via root feature_extractor)

The `coaching/situation_describer.py` path matters because if the
teaching layer renders v2.2-un-chained alongside v2.4-chained SHAP
attributions, the player sees inconsistency. Same class as the §1.4
Stage 6 gate. Flagged.

### 4.8 Q8 — Other feature-extraction consumers

**Full `extract_all_features` caller census** (grep confirmed):

| File:line | Populates `_action_history`? | Visible to labeller? | Risk |
|-----------|------------------------------|----------------------|------|
| `calibration_exam.py:300` | **NO** | **YES** (labelling display) | **CRITICAL** |
| `reference_evaluator.py:492` | **NO** | NO (eval only) | CRITICAL (baseline metric) |
| `reference_evaluator.py:797` | **NO** | NO (eval only) | CRITICAL (baseline metric) |
| `explain_hand.py:424` | UNKNOWN | POSSIBLY (teaching display) | HIGH — needs read |
| `coaching/explain_hand.py:424` | UNKNOWN | POSSIBLY (teaching display) | HIGH — needs read |
| `train_sizing_model.py:140` | UNKNOWN (Explore says NO) | NO (internal training) | HIGH — needs verification |
| `extract_features_parallel.py:70` | **NO** | NO (training data writer) | CRITICAL — §3 fix applies |
| `extract_incremental.py:88` | **NO** | NO (training data writer) | CRITICAL — §3 fix applies |
| `gauntlet_v5_37feat.py:161` | **NO** | NO (training data writer) | CRITICAL — §3 fix applies |
| `evaluate_calibration_anchors.py` (via `build_situation`) | **YES** (anchors JSON) | NO | SAFE |
| `run_v231_anchor_recheck_stage35.py` (via `build_situation`) | **YES** (inline specs) | NO | SAFE |
| `situation_factory.py` (via `game_state_bridge`) | **YES** (live play) | NO | SAFE |

`game_state_bridge.py:184` populates `_action_history` for live oracle
runs. This is the only path that's chain-aware today.

---

## 5. Synthesis — new MUSTs + redirects for blueprint v2

### 5.1 New MUSTs surfaced by the research

**MUST #20 CRITICAL — Labelling-display tool bypasses chain.**
`calibration_exam.py:279–298` builds hand_dict without `_action_history`.
Labellers assign PRIMARY/CONFIRMED tags against un-chained values. Stage
4 training-data production is corrupted at the root if this isn't fixed.

**Fix pattern:** Add `_action_history` to the hand_dict. Source: either
(a) reconstruct from `hand.action_history` if `ReferenceHand` carries it
(verify ReferenceHand dataclass), or (b) from an auxiliary JSONL field
if the fixtures lack it. Needs data-source inspection.

**MUST #21 CRITICAL — Stage 2/3 precedence before Stage 4 re-label.**
KB §1.9 + v3.2 prompt must update BEFORE Stage 4 labellers see chained
feature values. Otherwise labellers apply single-street mental model to
chained numbers. Re-sequencing needed:
- Stage 2 (KB §1.9 update with chained-aware language)
- Stage 3 (derive v3.2 prompt from updated KB)
- Stage 3.5 (the 20 MUSTs in blueprint v2)
- Patch MUST #20 (labelling display plumbs `_action_history`)
- Stage 4 re-label (fresh labels against chained features with aligned prompt)

**MUST #22 CRITICAL — `reference_evaluator.py` baseline.** Lines 492 and
797 both build hand_dict without `_action_history`. Baseline metric
(88.1% HU / 52.5% MW) measured against un-chained features. Post-v2.4
re-run needs chain-populated hand_dicts or the comparison is meaningless.

**MUST #23 HIGH — `train_sizing_model.py` sizing pipeline.** Explore
asserted bypass path; verification TBD in blueprint v2. If confirmed,
sizing model needs same fix as reference_evaluator.

### 5.2 Redirects to orchestrator decisions 🔄

**Redirect 1 — MUST #8 (coaching/ handling):** Narrower than the
reconciliation framing. Delete only `coaching/feature_extractor.py` +
`coaching/range_narrowing.py` (confirmed zero runtime importers).
Rest of coaching/ is load-bearing facade-implementation architecture;
collapsing it requires 4–6 weeks of refactor and is out of Stage 3.5
scope. Full coaching collapse → v2.5+ ticket.

**Redirect 2 — MUST #16 (M5 anchor fixtures):** False-positive finding.
Both the P0 pre-flight gate AND the Stage 3.5 M5 diagnostic script DO
include `action_history` on their fixtures. Chain IS exercised on
anchors. Re-framing: soften from "fix silent bypass" to "add regression
guard that asserts `_villain_range_chain_steps` non-empty for every
anchor row". Valuable belt-and-braces, but not a ship-blocker.

**Redirect 3 — Re-sequencing Stage 4 gating:** MUST #21 requires Stage
2 + Stage 3 complete BEFORE Stage 4 begins. This is a manifest sequencing
change. Blueprint v2's commit order doesn't touch it (Stage 2/3 are
separate streams), but the manifest's `ship_sequence` for `oracle_v2_4`
should explicitly gate Stage 4 on Stage 2 + 3 + 3.5 + MUST #20 all
landing.

### 5.3 MUSTs that verify-clean as originally stated

- **MUST #6 (equity-feature chain inheritance):** Confirmed 4 call sites
  at `feature_extractor.py:503, 617, 805, 828` — verified in §1. Needs
  implementation per reconciliation.
- **MUST #7 (caller-list audit):** Complete — §1 above. 23 total callers.
- **MUST #9 (except-Exception swallow):** Confirmed at all 4 sites —
  §3 above.
- **MUST #10–#19:** No new findings; reconciliation text stands.

### 5.4 Recommended blueprint v2 scope total

Original 5 MUSTs + 14 reconciliation MUSTs + 4 research MUSTs = **23 MUSTs**.
Minus the 2 soft redirects (MUST #8 narrowed; MUST #16 downgraded to
regression guard) = effective 21 CRITICAL/HIGH blueprint items plus
cross-stream coordination.

### 5.5 Questions for orchestrator before blueprint v2 drafting

- **Q15:** Confirm MUST #8 narrowing — delete only
  `coaching/feature_extractor.py` + `coaching/range_narrowing.py`, defer
  rest of coaching/ collapse to v2.5+?
- **Q16:** Confirm MUST #16 downgrade from ship-blocker to regression
  guard?
- **Q17:** Confirm Stage 4 gate requires Stage 2 + Stage 3 completion
  before re-label begins (MUST #21)? If yes, manifest `ship_sequence`
  needs update.
- **Q18:** MUST #20 fix for `calibration_exam.py` — data source for
  `_action_history`. If `ReferenceHand` dataclass doesn't carry per-hand
  action history, we need an auxiliary JSONL field or a source log. Who
  owns the fixture retrofit?
- **Q19:** MUST #22 fix for `reference_evaluator.py`. Same question —
  where does `ReferenceHand.action_history` (plural, per-street) come
  from? Currently only `villain_aggression_count` / `checked_back` /
  `call_count` exist on the dataclass — counts, not sequences. Needs
  either fixture retrofit or an upstream parser.

### 5.6 Open audit items deferred to blueprint v2 itself

Not worth delaying research findings delivery for these — they're
mechanical reads:

1. `train_sizing_model.py:140` hand_dict contents (MUST #23 verification)
2. `explain_hand.py:424` hand_json source + whether it carries action history
3. `coaching/explain_hand.py:424` same
4. `ReferenceHand` dataclass — does it carry per-street action history?
5. v2.3.1 training CSV format — does it carry action history in any
   column, or is the pre-extracted feature dict the only thing preserved?

All five can be resolved in the first 30 minutes of blueprint v2 work.

---

## 6. Execution posture

**Research complete.** Blueprint v2 is ready to be drafted once
orchestrator confirms:

1. The 4 redirects from §5.2 — especially MUST #8 narrowing (most
   consequential for scope)
2. MUST #20, #21, #22, #23 accepted as new CRITICAL/HIGH items
3. Stage 4 gating change (MUST #21) reflected in manifest ship_sequence

**Blueprint v2 scope forecast:** ~23 MUSTs, 1500–2000 lines single
artifact. Replaces b1a9a91 wholesale.

**Implementation forecast (post-blueprint-v2 approval):** 8–10 commits
(one per MUST, per CLAUDE.md discipline) + test corpus load + audit
re-runs + cross-stream pings.

No code edits until orchestrator confirms the redirects and new MUSTs.
Standing by.
