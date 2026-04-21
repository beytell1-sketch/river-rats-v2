---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: Multi-agent reconciliation pass #2 on Stage 3.5 BLUEPRINT v2 (8bb0f9f) + v2.1 supplement (3166759)
status: REWORK — v2.2 supplement required addressing 16 new MUSTs before code edits
---

# Multi-Agent Reconciliation #2 — Blueprint v2 + v2.1 Supplement

Five parallel reviewers (architecture, GTO, red-team, practical pro,
research) ran on the combined artifact. Aggregate verdict **REWORK**.
Red-team is strongest signal again; architecture + GTO converge on
verifiable source-level errors; practical + research validate
direction with specific deltas.

Net new scope: **16 new MUSTs (#28-#43)**. Total now 41 MUSTs across
v2 + supplement + this reconciliation. Quality default applies; owner
reaffirmed slow/quality on this work.

## Verdict matrix

| Reviewer | Verdict | Strongest finding |
|---|---|---|
| Architecture | APPROVE_WITH_FIXES | Caller list missing `coaching/explain_hand.py:264, 329`; MUST #6 helper double-computes; multiway branch literally `NotImplementedError` |
| GTO theorist | APPROVE_WITH_FIXES | T_J01 reauthored values directionally wrong (copies K_05 pattern; T_J01 is different shape — donk-then-slowdown, not delayed probe) |
| Red-team | **REWORK** | MUST #15 floor-truncation NaN-flag NOT closed; MUST #26 BEFORE block doesn't match source; feature-count math wrong (55 not 54); commit-sequence poisoning windows |
| Practical pro | APPROVE_WITH_FIXES | 5-entry dry-run inadequate; "N/A" UX is coder-speak; T_J01 ship criterion needs verdict-flip not just feature-shift |
| Research | APPROVE_WITH_FIXES | Add belt-and-braces count guard for mass-rail pathology; vocabulary structured-dict for v2.5+ |

## NEW MUSTs (additions to v2 + supplement scope)

### MUST #28 — CRITICAL — Floor-truncation NaN-flag (Red-team #1)

**Real bug.** When MUST #13 floor truncates and reverts to
`last_valid_range`, the caller at `extract_range_composition` sees
non-empty `v_range` and proceeds. `_villain_chain_overflowed` stays
False. Downstream composition + MUST #6 equity + MUST #19
`explain_hand` all consume the partial-chain range as if it were a
full-chain range. **No sentinel fires. This IS the silent-fallback
anti-pattern MUST #15 was meant to kill** — same v2.3.2 failure mode
in a different layer.

**Fix:** `extract_range_composition` consumes `chain_meta['truncated']`,
not just `if not v_range`. When `truncated == True`, set
`_villain_chain_overflowed = True` and apply NaN sentinel exactly
like the empty-range path.

### MUST #29 — CRITICAL — Re-verify MUST #26 BEFORE block (Red-team C2 + Architecture C2)

Builder's supplement §2.2 BEFORE block doesn't match `origin/master`.
- Actual `assemble_v23_clean.py` at origin already has
  `RAW_FEATURES = list(FEATURE_COLUMNS)` (Step A is a no-op).
- Cited per-row write at `record['attention_flags'][fc]` doesn't exist
  in `assemble_v23_clean.py`. Multiple write paths exist:
  - line 113: `for col in ATTN_FEATURES: out[col] = 1.0` (pilot all-1)
  - line 61: `out[col] = float(row.get(col, 0))` (v2.2 base silent-0)
- The actual silent-0-default surface may be `assemble_pilot_data.py`
  (hardcoded ATTENTION_LEVELS) or a v2.4-era assembler not yet
  written.

**Fix:** Builder reads ALL `assemble_v23_*.py` + `assemble_pilot_data.py`
+ any v2.4 successor on origin/master and identifies WHICH file
actually consumes `attention_flags` from labeller output for v2.4
re-assembly. Then patches all 3 attention-write paths (pilot, v22_base,
labeller) with strict-mode coverage. Without this, MUST #26 doesn't
close the silent-attention-corruption surface.

### MUST #30 — CRITICAL — Caller list completeness (Architecture C1 + Red-team #6/coaching)

`coaching/explain_hand.py:264, 329` calls root `narrow_to_betting_range`
and is **NOT** in MUST #8's partial-deletion list. HIGH #5 tuple-return
change crashes these sites. Real root tuple-unpack count is **14, not 12**.

`coaching/explain_hand.py:251, 261, 326` are MUST #6/#19 equity-bypass
sites that remain unpatched in v2 (blueprint v2 §15.4 line 1778
references "coaching/explain_hand.py:424" but real bypass is at
261/329 per origin grep — line-number staleness suggests blueprint
wasn't re-verified against origin post-build).

**Fix:** Add `coaching/explain_hand.py:264, 329` to MUST #7 + commit 1
tuple-unpack list. Add `coaching/explain_hand.py:251, 261, 326` to
MUST #6 commit-6 chain-inheritance scope. Re-verify ALL line numbers
against `git show origin/master:`<file>` before commit work begins.

### MUST #31 — CRITICAL — Feature-count math reconciliation (Red-team C3)

Supplement claims "v2.2 was 108 (54 raw + 54 attn)" but
`gto_model.py:64` at origin shows `N_FEATURES = len(FEATURE_COLUMNS) = 55`.
`pilot_20_attention.csv` is 109 cols (54 raw + 54 attn + label).
There's a held-back feature (`board_adjusted_hrp` likely) that's in
FEATURE_COLUMNS but not the v2.2/v2.3 CSVs. The 54→59 framing is
wrong; the truth is 55→59 with one already-held-back column.

`run_attention_experiments.py:461` generates `list(FEATURE_COLUMNS) +
['attn_'+f for f in FEATURE_COLUMNS]` = 110 col_names against
54-raw-col CSV — Exp 3 training path may already be broken pre-Stage-3.5.

**Fix:** Builder traces actual feature-count state on origin and
documents:
- Real current FEATURE_COLUMNS length (verify 55)
- Which feature is held back from CSVs (likely `board_adjusted_hrp`)
- Whether Exp 3 trainer currently runs against a 54-or-55-col CSV
- Update supplement §2/§3 math throughout to reflect reality

This affects MUST #26 capture math, MUST #27 width assertion, MUST #43
audit column expectations.

### MUST #32 — CRITICAL — Close commit-sequence poisoning windows (Red-team C4)

Two windows where mid-sequence Stage 4 firing produces mixed
distribution:

**(a) Commits 2 → 12:** After commit 2 (CRIT #2 env-gated strict),
default env is `warn` (silent bypass). If Stage 4 re-label fires
without `STAGE4_STRICT_ACTION_HISTORY=raise` explicitly set,
corruption ships silently. Env-only guard is too soft.

**(b) Commits 4 → 5:** CRIT #1 lands chain consumer at commit 4;
MUST #10 NaN downstream lands at commit 5. In-between extracts have
composition=0.0-on-empty-range (commit 4 behavior) instead of NaN
(commit 5 behavior). Distribution has a seam.

**Fix (a):** Orchestrator-level lockout — manifest gate or
git-hook-level check that Stage 4 cannot fire while Stage 3.5
implementation is in flight. OR: change the env default to `raise`
and require explicit `=warn` for legacy paths.

**Fix (b):** Co-land NaN sentinel logic with CRIT #1 in commit 4
(NaN branches pre-authored, dormant until HIGH #4 populates
`_villain_folded` in commit 5). OR: merge commits 4 + 5 into single
ship-coherent commit. Builder picks; orchestrator approves either.

### MUST #33 — HIGH — Corpus reauthoring values corrected (GTO C1 + H1)

T_J01, T_B05, and adding T_J02 to scope. Builder's draft direction
copies wrong analogue (K_05 delayed-probe pattern); GTO source-corrected:

| Case | Pre-fix | Builder draft | GTO-correct target |
|---|---|---|---|
| T_J01 (donk-flop, x-turn, bet-river) | 0.72/0.06/0.22 | 0.55/0.04/0.41 (WRONG) | **0.50 TP+ / 0.18 medium / 0.32 air** — mediums RISE because turn-CHECK is where mediums concentrate after donk-flop |
| T_B05 (flat-call-a-raise + turn-check) | TBD | 0.70/0.12 (under-corrected) | **0.60 TP+ / 0.28 medium / 0.05 draw / 0.07 air** — flat-call-a-raise IS the medium-pot-control line |
| T_J02 (BET-CHECK-CALL-BET, 4 narrow classes) | TBD | 0.65/0.10/0.25 (mediums too low) | **0.60 TP+ / 0.18 medium / 0.22 air** — turn-CALL after CHECK is medium-made pot-control |

**Fix:** Update corpus values per GTO targets. Practical pro adds
ship-criterion: T_J01 oracle verdict must FLIP from FOLD to CALL
(or MIXED-with-CALL). Numbers moving without verdict change = fix
failed.

### MUST #34 — HIGH — MUST #6 helper completeness (Architecture H1 + H2)

Two issues with `_get_chain_narrowed_villain_range` (v2 §3.1):

**(a)** Re-runs `narrow_by_action_history` rather than consuming
`_villain_range_narrowed` already published by CRIT #1. Per-hand
chain executes 2x (composition + equity); 4x in multiway equity MC
loop. Perf cost real but bounded.

**(b)** Multiway branch is literally `raise NotImplementedError #
placeholder for blueprint`. Multiway is ~47% of v2.3 training data.
Un-shippable as written.

**Fix (a):** Helper consumes `_villain_range_narrowed` from
`extract_range_composition`'s return dict via thread-through cache,
not re-runs chain. Document the cache contract.

**Fix (b):** Multiway branch must be specified before code edits
begin. Builder picks: per-villain chain × MC trial loop, OR
primary-villain-only with multi-villain composition aggregated
elsewhere. Blueprint v2.2 supplement spec'd before commit 6.

### MUST #35 — HIGH — Sidecar miss sentinel (Red-team #5)

`_CALIBRATION_ACTION_HISTORY.get(hand.ref_id, [])` returns empty list
on lookup miss → `if action_history` False → chain bypasses → strict-
warn logs and continues silently. A ~140-entry sidecar with even 2
transcription errors silently corrupts those fixtures.

**Fix:** Use sentinel `_SIDECAR_MISSING = object()` for missing keys
and raise `RuntimeError` in Stage 4 mode. Plus: automated sidecar
validator script that asserts (a) every fixture's ref_id has a
sidecar entry, (b) action sequences are well-formed (street-monotonic,
positions match fixture's hero/villain, action-classes valid).

### MUST #36 — HIGH — Replace tautological width assertion (Red-team #9)

Supplement §3.3 assertion `X.shape[1] == 2 * len(FEATURE_COLUMNS)`
can never fire — `col_names = list(FEATURE_COLUMNS) + ['attn_'+f for
f in FEATURE_COLUMNS]` IS already `2 * len(FEATURE_COLUMNS)`, and
`load_feature_csv` builds X from exactly `len(col_names)` cols.

**Fix:** Real drift catch is CSV-header reconciliation BEFORE X
construction. Read CSV header, verify each expected column name
exists, raise on missing. The vocabulary-version cross-check
addresses one drift class; need a column-name set check too.

### MUST #37 — HIGH — Audit coaching/ sys.path side-effects (Red-team #6)

`coaching/feature_extractor.py:17` does `sys.path.insert(0, '/mnt/project')`;
`coaching/range_narrowing.py:41` does `sys.path = ['/home/claude'] + ...`.
These mutate sys.path as IMPORT SIDE EFFECTS. The 11+ surviving
coaching modules may transitively depend on these mutations. Regression
guard checks direct importers but not the post-deletion sys.path state.

**Fix:** Pre-deletion audit step: import each surviving coaching/*
module in isolation, confirm it functions without the deleted modules'
sys.path side-effects. If any depends, either repoint the side-effect
into a new init module OR defer that specific deletion.

### MUST #38 — MEDIUM — Frequency table coherence post-MUST-#17 (GTO M1)

`RIVER_CHECKING_FREQUENCIES.medium_made` 0.92 → 0.85 leaves the table
internally incoherent post-3-way-tightening. Companion adjustments:
- `bluff` check 0.65 → 0.80 (mass parity with bet 0.20)
- `air` check 0.80 → 0.90 (mass parity with bet 0.10)
- `good_value` 0.45 stays (already coherent)

**Fix:** Single multi-row edit at `range_narrowing.py:142+`. Document
the coherence rationale in the commit message.

### MUST #39 — MEDIUM — KB §1.11 asymmetric FOLD-lean threshold (GTO)

Current rule: 0.15 delta for both CALL-lean and FOLD-lean PRIMARY
tagging. GTO source check: densification effect overstates FOLD
confidence; a 0.15 draw-block advantage routinely flips at solver to
still-CALL when `equity_vs_range > 0.42`.

**Fix:** Update KB §1.11 to asymmetric thresholds:
- CALL-lean: `nut_made_block_pct − mean(flush_dr, straight_dr) > 0.15` (unchanged)
- FOLD-lean: `mean(flush_dr, straight_dr) − nut_made_block_pct > 0.20` (was 0.15)

Stage 2 KB edit — does NOT block Stage 3.5 code work but must land
before Stage 3 v3.2 prompt derives.

### MUST #40 — MEDIUM — Combo-draw double-counting addendum (GTO)

KB §1.11 caveat exists ("two percentages can sum above 1.0") but the
multi-signal resolution rule uses their mean — degrades when a
combo-draw hand is effectively counted twice in the FOLD-lean signal.

**Fix:** Addendum to §1.11: "if hero holds a combo-draw blocker, use
max(flush_draw_block_pct, straight_draw_block_pct) for the FOLD-lean
delta, not mean."

### MUST #41 — MEDIUM — Belt-and-braces count guard (Research)

Mass-based safety rail can fire OK on a chain that has 5% mass
spread across 50 hands vs 5% mass concentrated in 2 hands. Solver-
literature notes mass concentration without count support yields
brittle inference (Moravcik DeepStack supplementary, Brown Libratus
range-decomposition).

**Fix:** Secondary guard at `narrow_by_action_history`: `if
cumulative_surviving >= 0.20 and len(current_range) < 5: log
WARN("mass-concentrated-without-count-support")`. Doesn't truncate;
flags for audit.

### MUST #42 — MEDIUM — NaN render UX in player English (Practical pro)

"flush_block_pct: N/A" is coder-speak. CONTENT_API v4 NaN render spec
should be:

> "Villain folded earlier — no range to read."

In multiway: name the remaining live villain. No partial-info even
when folded — would mislead the player.

**Fix:** MUST #10 sub-1 amended with player-English wording. CONTENT_API
v4 spec (MUST #43) carries this language.

### MUST #43 — MEDIUM — CONTENT_API v4 elevated to blocking cross-stream task (Architecture M1)

"Builder drafts, teaching implements, orchestrator coordinates" is a
dependency, not a MUST. Risk: commit 5 lands code-side NaN sentinel
while teaching renders literal "nan%". Cross-stream coordination must
gate.

**Fix:** Ticket file in `review/comms/` named
`TICKET_CONTENT_API_V4_NAN_RENDER_2026-04-22.md` covering: NaN render
strings (player English per MUST #42), test cases, schema bump.
Teaching terminal owns implementation; orchestrator gates commit 5
merge on teaching's CONTENT_API v4 ship.

## Owner-decision points (resolved by orchestrator)

Per quality default + DECIDE and EXECUTE:

- **Q21 dry-run width:** **8 shape-targeted entries** (HU cbet-call,
  HU x/r-call, delayed probe, 3way non-primary, 3bet pot, turn x/r,
  folded-villain NaN, triple-bet mass-floor) per Practical pro.
  Plus **25-30 stratified sample at Phase 2 midpoint** per Research.
  Two-level gate.
- **Q26 outlier threshold:** **25pp for street=river, 15pp for flop/turn**
  per GTO. Builder's flat-20pp was acceptable but the asymmetric split
  matches the literature better.
- **Q30 vocabulary version format:** **`v2.4_NNflag` for Stage 3.5;
  structured dict (`vocabulary_id`, `n_features`, `n_attn_flags`,
  `mechanism_version`, `assembler_commit_sha`) for v2.5+** per Research.
  File the dict-format change as v2.5 ticket.

Q-resolutions accepted as builder proposed (no orchestrator change):
Q20 (sizing bypass), Q22 (CONTENT_API ownership — but elevated to
MUST #43 ticket), Q23 (Phase 4 defer), Q27 (1:1 vocabulary —
research-validated), Q28 (env-strict), Q29 (no zero-pad — accepted
with Red-team caveat documented in MUST #32(a) lockout), Q31 (Stage 3
deliverable gate — already manifest v1.10).

## Cross-MUST observations

- Path (c) sidecar authoring (~140 entries) is the critical-path
  item. MUST #35 (sentinel + validator) + Practical pro's required
  shape coverage (FB-40 includes ≥4 donk leads, ≥3 delayed-probes,
  multi-street barrels, multiway-with-shifting-primary) makes this
  more rigorous, not optional.
- Multiple reviewers independently flagged that blueprint v2 contains
  source-staleness errors (caller line numbers, BEFORE blocks not
  matching origin, feature-count math). MUST #29-#31 force a re-
  verification pass against origin/master before any commit work.
  Builder's discipline rule (read source, not plan) needs to apply
  to their own blueprint too.
- MUST #6 multiway branch literally raises `NotImplementedError`.
  The fact that this passed the first reconciliation as APPROVE
  suggests the panel didn't hit the §3.1 multiway sub-section.
  Reviewers in this pass caught it. Lesson for next reconciliation:
  reviewers should grep blueprint for `NotImplementedError` /
  `TODO` / `placeholder` markers.

## What blueprint v2.2 must include

In addition to v2 (8bb0f9f) + supplement v2.1 (3166759):

- §M28 — floor-truncation NaN-flag patch
- §M29 — re-verified MUST #26 with correct BEFORE blocks for ALL
  attention-write paths in `assemble_v23_clean.py` + sibling assemblers
- §M30 — caller list with 14 sites (incl. coaching/explain_hand.py)
  + MUST #6 scope expansion to coaching/explain_hand.py:251, 261, 326
- §M31 — feature-count reconciliation: real FEATURE_COLUMNS length,
  which feature is held back, Exp 3 trainer state today, math fixed
  throughout supplement
- §M32 — commit-sequence lockout: env default change OR commits 4+5
  merge; orchestrator-level Stage 4 gate during Stage 3.5 in-flight
- §M33 — corpus reauthoring with GTO-corrected targets (T_J01, T_B05,
  T_J02) + verdict-flip ship criterion for T_J01
- §M34 — MUST #6 helper consumes `_villain_range_narrowed` cache;
  multiway branch fully spec'd
- §M35 — sidecar sentinel + automated validator
- §M36 — CSV-header reconciliation replaces tautological width assert
- §M37 — coaching/ sys.path side-effect audit pre-delete
- §M38 — frequency table coherence (bluff + air check freqs adjusted)
- §M39 — KB §1.11 asymmetric FOLD-lean threshold 0.20
- §M40 — combo-draw use-max addendum to §1.11
- §M41 — belt-and-braces count guard at 5-hand floor
- §M42 — player-English NaN render wording
- §M43 — CONTENT_API v4 ticket file authored, teaching-terminal-
  ownership coordinated

Re-cut blueprint v2.2 OR amend with supplement v2.2. Either format;
clarity over brevity.

## Reports archived

Five full reviewer outputs in agent transcripts. Practical pro wrote
to `review/comms/PRACTICAL_PRO_REVIEW_PASS2_STAGE35_V2_2026-04-22.md`
during their pass. Other four returned in chat; key findings
extracted above.

## Lessons for memory

- Reviewers should grep blueprints for `NotImplementedError`, `TODO`,
  `placeholder` markers as a first-pass sweep. Adding to
  `feedback_verify_source_not_plan.md` related rule set.
- Builder's blueprint contained source-staleness errors despite the
  builder being grounded. Ground-then-write is necessary but not
  sufficient — a re-verification pass against origin/master AFTER
  draft completion catches what drift introduces during writing.

## Immediate next action

Builder reads this reconciliation, then:

1. Acknowledge the 16 new MUSTs
2. Re-verify the source-level errors (MUST #29, #30, #31) before any
   blueprint edit — reading actual `assemble_v23_*.py`,
   `coaching/explain_hand.py`, `gto_model.py:64`, `pilot_20_attention.csv`
   header, `run_attention_experiments.py:461` on origin/master
3. Cut blueprint v2.2 (or supplement v2.2) addressing all 16 new MUSTs
4. Submit for orchestrator review; if clean, dispatch reconciliation
   pass #3 (same panel)
5. If reconciliation pass #3 lands clean, implementation begins per
   the re-sequenced commit order (now with merged or re-sequenced
   commits 4+5, lockout for commits 2-12)

No code edits, no model training, no teaching changes, no Stage 4
re-label work until blueprint v2.2 passes its own reconciliation.

Quality default applies. Owner reaffirmed slow/quality. Builder's
question-back posture stays open: ask before executing on any
unclear MUST.

Go.
