---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: Multi-agent reconciliation pass #3 on Stage 3.5 blueprint v2 (8bb0f9f) + amended supplement v2.2 (d7db3f1)
status: REWORK — 15 new MUSTs (#45-#59); pattern converging; builder cuts v2.3 amendment
---

# Multi-Agent Reconciliation #3 — Pattern Converging

Five reviewers (architecture, GTO, red-team, practical pro, research)
on combined artifact. Aggregate verdict **REWORK**. Red-team strongest
signal again, but findings are smaller in scope than pass #2 — mostly
code-level correctness bugs + spec-completeness gaps rather than
whole-MUST-class gaps.

**Trajectory:** Pass 1 → 14 new MUSTs; Pass 2 → 16; Pass 3 → 15.
Scope per MUST shrinking (concrete code bugs + enumeration gaps vs
prior-pass architectural redesigns). Expect pass #4 to land mostly
clean.

**Total active MUSTs now: 57** (42 prior + 15 new). MUSTs #24, #25
inactive.

## Verdict matrix

| Reviewer | Verdict | Strongest finding |
|---|---|---|
| Architecture | APPROVE_WITH_FIXES | Multiway spec return mechanism (`meta['per_villain_ranges']` never populated); truncated-meta dropped per-villain |
| GTO theorist | APPROVE_WITH_FIXES | Bi-schema binary collapse loses PRIMARY/CONFIRMED signal; RIVER_CHECKING + RIVER_BETTING sum ≠ 1.00 post-MUST-#17 |
| Red-team | **REWORK** | 4 CRITICAL: bi-schema int/case-sensitive bugs; multiway cache cross-contamination; caller-list doc drift across v2/amended; `v2.4_55flag` vocab string wrong count (held-back = 54) |
| Practical pro | APPROVE_WITH_FIXES | 8-entry dry-run NEVER ENUMERATED in amended supplement; T_J02 corpus value drift between supplement §3.6 and YAML |
| Research | APPROVE_WITH_FIXES | Benchmark-gate fallback switch not specced; sidecar 10% solver sampling recommendation |

## NEW MUSTs

### CRITICAL — ship blockers (4 MUSTs)

#### MUST #45 — Bi-schema helper concrete bugs + tri-state retention

Red-team CRIT-P3-2 + GTO H-3a + Architecture Q38 attack:

**Concrete bugs:**
- `int(val) if val else 0` returns `2` when `val=2` (no binary clamp)
- Case-sensitive `in ('PRIMARY', 'CONFIRMED')` silently zeros `"primary"`, `"Primary"`, any typo
- Mixed-schema record (both `feature_attention` AND `attention_flags` present) silently prefers production; no assertion

**Signal loss (GTO):**
- Current helper collapses `PRIMARY` + `CONFIRMED` both → 1 (binary)
- PRIMARY = "decisive for my action" vs CONFIRMED = "supports but not pivot" is real training signal
- Research-validated: 2-level > binary at small N per Lu/Xu/Chen literature

**Fix:**
- Retain tri-state `{PRIMARY: 2, CONFIRMED: 1, missing: 0}` at CSV write
- Binarise only at train-time if v2.4 trainer locked to binary (accept as v2.4 ship, not tri-state lift)
- Explicit mixed-schema rejection: raise RuntimeError if both keys present
- Case-insensitive match with explicit canonicalization
- Typed return: clamp at helper edge
- Add `_schema_detected` audit column per CSV row (Q38 mitigation)

#### MUST #46 — Multiway spec completeness

Architecture H1 + H2 + Red-team CRIT-P3-1:

**Gaps in amended §3.7:**
- Return mechanism: helper constructs `per_villain_ranges` dict-of-dicts but declares `merged = {}` at line 685 that is never populated or returned. Callers at feature_extractor.py:500-505, 605-617, 805-810 each need a concrete dict.
- `opp_meta['truncated']` dropped at line 698: `opp_range, _ = narrow_by_action_history(...)` — if any villain's chain truncates, MUST #28 sentinel never fires for that opponent. Silent partial-range consumption.
- Cache contract underspec'd — possibility of cross-villain contamination if cache keyed wrong.

**Fix:**
- Populate `meta['per_villain_ranges']` explicitly
- Capture each villain's `opp_meta['truncated']`; propagate `chain_overflowed=True` per opponent
- Cache keyed on `(opp_pos, street_raw, action_history_hash)` — explicit in spec

#### MUST #47 — Caller-list + NotImplementedError reconciliation across v2 + v2.2

Red-team CRIT-P3-3 + Practical pro:

**Drift:**
- Blueprint v2 §2.1 says "12 root + 9 coaching deferred"
- Blueprint v2 line 1728 says 13
- Amended §1.1 says 14 (grounding-verified correct)
- Blueprint v2 line 942 still has `raise NotImplementedError` for multiway

**Fix:**
- Amend blueprint v2 (or annotate) to say "14 sites" consistently
- Delete or annotate line 942 `NotImplementedError` with big `SUPERSEDED BY AMENDED §3.7` marker
- Add cross-reference line on all v2 sections that are superseded by v2.2 amendments

#### MUST #48 — Attention vocabulary version string uses correct count

Red-team CRIT-P3-4:

**Bug:**
- Amended supplement writes `ATTENTION_VOCAB_VERSION = f"v2.4_{len(FEATURE_COLUMNS)}flag"` = `v2.4_55flag`
- But RAW_FEATURES is 54 (board_adjusted_hrp held back)
- Stage 5 will un-hold board_adjusted_hrp → raw = 55
- Same audit tag `v2.4_55flag` would cover both pre- and post-unhold silently
- MUST #36 trainer width assertion can't detect the held-back-lifted transition

**Fix:**
- Use actual active count not `len(FEATURE_COLUMNS)`: `v2.4_54flag` pre-Stage-5, `v2.4_55flag` post-Stage-5
- OR include held-back state in version: `v2.4_54_pre_unhold`, `v2.4_55_post_unhold`
- Also updates MUST #26 + #27 patches accordingly

### HIGH — must fix before ship (6 MUSTs)

#### MUST #49 — 8-entry dry-run batch enumeration

Practical pro F2: **Q21 resolution (8 shape-targeted entries) was never
enumerated in amended supplement.** Critical before commits 6-7 begin.

**Fix:** Enumerate in amended supplement addendum, per Practical pro's
list:
1. HU donk-flop + turn-check-through + river-bet (T_J01)
2. HU bet-check-call-bet four-class chain (T_J02)
3. HU BET-RAISE-CALL same-street collapse (T_B05)
4. Folded-villain multiway (sentinel path)
5. Over-narrow to empty (MUST #15 overflow)
6. Mass-floor truncated (MUST #28)
7. Delayed-probe large turn bet (T_K07)
8. Multiway per-villain chain (MUST #34b) — 3-way spot

Plus: Phase 2 midpoint 25-30 stratified check.

#### MUST #50 — Frequency table atomic coherence

GTO M-3a: **RIVER_CHECKING.medium_made = 0.85 + RIVER_BETTING.medium_made = 0.08 = 0.93 ≠ 1.00.** Table internally incoherent.

**Fix (atomic):** Pick one:
- (a) check=0.92, bet=0.08 (sum 1.00; reverts MUST #17 direction)
- (b) check=0.85, bet=0.15 (sum 1.00; more aggressive river medium betting)

GTO recommends (b). Also verify bluff/air reciprocals post-MUST #38:
- bluff: check=0.80, bet=0.20 (sum 1.00) ✓
- air: check=0.90, bet=0.10 (sum 1.00) ✓

Land atomically in commit 11 (or commit 10 per updated sequence).

#### MUST #51 — T_J02 corpus value reconciliation

Practical pro F1: Amended supplement §3.6 gives T_J02 = 0.60/0.18/0.00/0.22;
corpus YAML at `review/tests/range_narrowing_test_corpus_2026-04-20.yaml`
still has 0.65/0.10/0.00/0.25 at line 1683.

**Fix:** Commit 13 explicitly touches all three (T_J01, T_B05, T_J02);
supplement §3.6 spells out the YAML edits required.

#### MUST #52 — Benchmark-gate fallback switch for multiway

Architecture Q36 + Research:

**Fix:**
- Add env `MULTIWAY_CHAIN_MODE = 'per_villain' | 'primary_only'`
- Default `per_villain`; fallback `primary_only` if benchmark exceeds perf budget
- Pre-merge gate on commit 5: benchmark per-villain-chain on a 100-hand sample; if > 500ms median, flip default to `primary_only` and defer full per-villain to v2.5
- Document rationale: per Research literature (Brown/Sandholm) per-villain chain is feature-pipeline approximation not solver-lineage; primary-only is defensible fallback for teaching tool

#### MUST #53 — `_mandatory_tag_list_version` audit column

GTO addition:

**Reason:** `docs/ASSEMBLER_PATTERN.md` references mandatory-tag list "derived from v3.2 prompt" but v3.2 is future Stage 3 work; v3.1 doesn't cover 4 new blockers. When v3.2 lands, assembler must re-gate — otherwise a v3.1-era assembler silently drops new mandatory tags.

**Fix:** Add audit column `_mandatory_tag_list_version` parallel to `_attention_vocabulary_version`. MUST #27 trainer cross-checks both.

#### MUST #54 — Sidecar 10% solver-verify sampling

Research: Builder's validator checks structural validity (street-
monotonic, positions, action-classes). Doesn't check poker-plausibility
(authored "villain called an unraised pot" would pass structural but
be semantically wrong).

**Fix:**
- Structural validator (MUST #35) — kept
- GTO-reviewer manual pass on all sidecar entries — kept
- **ADD:** 10% random-sample solver-verify CI check. Solver used for VERIFICATION only, not as label source (per `feedback_solver_vs_expert_labels.md`). Cheaper than full solver pass; catches authoring drift.

### MEDIUM — hardening (5 MUSTs)

#### MUST #55 — Silent-fallback in review/recovered/eval_*.py

Red-team HIGH: `review/recovered/eval_FB40_plus_ablation.py:84, 123` +
siblings have silent-fallback patterns not addressed by MUST #2/#9.

**Fix:** Decide: (a) delete if obsolete recovered-script artifact; (b)
add audit column + strict-env gate. Builder decides based on live-path
status.

#### MUST #56 — Manifest-gate lockout tooling enforcement

Red-team HIGH: Manifest gates are YAML docs; not CI-enforceable.
Stage 4 re-label could fire without checking manifest.

**Fix:** Add pre-commit or CI check that reads manifest phase and
blocks Stage 4 scripts if `stage_3_5` not in `landed`. **OR** accept as
tech debt + document in `feedback_manifest_gate_is_docs_not_enforcement.md`
for future hardening. Acceptable to defer if cost prohibitive.

#### MUST #57 — CONTENT_API v4 tooling ship-gate

Red-team MEDIUM: Currently manual cross-stream ping from teaching
terminal. Partial-coverage risk (NaN render spec'd but tests missing).

**Fix:** Version-pin in game adapter + teaching CONTENT_API module.
Commit 4 (merged) cannot merge until teaching CONTENT_API v4
version-pin matches. Teaching terminal owns the version bump;
orchestrator gates commit 4.

#### MUST #58 — ASSEMBLER_PATTERN.md enforcement checklist

Red-team MEDIUM: Pattern doc without tooling enforcement. Stage 4's
future `assemble_v2_4.py` could clone the pattern wrong.

**Fix:** Add review checklist at end of `docs/ASSEMBLER_PATTERN.md`
that Stage 4 reviewer must check off. Each pattern element (strict
env, audit column, schema detection, width reconciliation) has a
line item.

#### MUST #59 — Commit 4 merge equity-inheritance coverage

Red-team HIGH (folded to MEDIUM after analysis): Commit 4 merge
covers CRIT #1 + HIGH #4 + MUST #10 + MUST #15 + MUST #28, but MUST #6
equity chain-inheritance lands commit 5. Mid-commit-pair poisoning
window: composition NaN lands commit 4, equity-bypass remains commit 5.

**Fix:** Builder picks:
- (a) Extend commit 4 to include MUST #6 helper stub/pass-through that
  avoids poisoning (but grows merge commit further)
- (b) Merge commits 4+5+6 into one ship-coherent commit (all chain-
  inheritance + NaN work in one atomic unit)
- (c) Accept short poisoning window during commit 4→5 transition;
  document; verify no Stage 4 work fires in the window

Orchestrator recommends (b) — MUST #6 is semantically tied to the
chain-inheritance surface; merging with commit 4 eliminates the window
entirely. Scope grows but single-atomic-unit discipline matches the
v2.3.2 lesson.

## Q-resolutions

- **Q36 (multiway perf threshold):** Architecture-recommended asymmetric
  gating. 500ms ship / 500-750ms orchestrator review / 750+ms hard
  fallback to primary-only. MUST #52 codifies the switch.
- **Q37 (T_J01 ship-criterion softness):** Hard criterion kept for T_J01
  (verdict flip FOLD→CALL). MIXED with CALL>40% acceptable for
  T_J02/T_K5-7. Soft-pass (confidence drop without verdict flip) is
  partial — if ALL 3 reauthored fixtures stay on wrong side of 0.50, it's
  a real failure; if 1-2 are soft, owner judgment call.
- **Q38 (bi-schema confusion risk):** Merged into MUST #45 with
  `_schema_detected` audit column + mixed-schema rejection.

## What blueprint v2.3 amendment must include

Same fix-forward pattern per Q34 (B). Single new commit on top of
d7db3f1.

- §M45-§M48 — CRITICAL ship blockers (code + spec + doc correctness)
- §M49-§M54 — HIGH scope items (enumeration + atomicity + corpus + fallback)
- §M55-§M59 — MEDIUM hardening (silent-fallback decisions + tooling enforcement)
- §Q36-Q38 resolutions documented
- 8-entry dry-run list (MUST #49)
- Atomic frequency table (MUST #50)
- Commit sequence: 16 commits may become 15 if MUST #59 (b) chosen
  (merges 4+5+6)

## Reports archived

All 5 reviewer outputs in agent transcripts. Key extracted above. One
reviewer (red-team) wrote to
`review/comms/REVIEWER_V24_STAGE35_PASS3_2026-04-22.md` locally
(check if pushed).

## Discipline notes

- Builder's source re-verification caught multiple real issues this
  pass. The discipline is working — Architecture/Red-team line-number
  checks confirmed 13/14 STEP 1 items clean; only minor drift.
- GTO caught a frequency-table math error that slipped in with MUST #17
  tweak. Atomic-set-coherence check needs to be a standing discipline:
  when you change ONE frequency, verify all pairs still sum to 1.00.
- Red-team's concrete-bug-level findings (`int(val) if val else 0`
  returns 2 not clamped; case-sensitive string match) are the kind of
  bugs that slip past architecture reviewers looking at logic flow but
  not type contracts. Useful pattern: red-team always runs a typed-
  contract audit on new helpers.
- Pattern convergence is real. If pass #4 is clean or MEDIUM-only,
  implementation can begin.

## Immediate next action

Builder reads this reconciliation, then:

1. Source-verify the 4 CRITICAL findings against origin/master (same
   discipline as prior — git show origin/master:<path>)
2. Cut blueprint v2.3 amendment (fix-forward on d7db3f1)
3. Address all 15 new MUSTs + the 3 Q-resolutions
4. Push; ping orchestrator
5. Orchestrator dispatches reconciliation pass #4

No code edits, no model training, no Stage 4 work until reconciliation
pass #4 lands clean (or APPROVE with only MEDIUM fixes).

Quality default. Slow/clean over fast/loose. Standing by.
