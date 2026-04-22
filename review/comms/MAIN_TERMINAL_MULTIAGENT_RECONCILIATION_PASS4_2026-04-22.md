---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: Multi-agent reconciliation pass #4 on Stage 3.5 cumulative (v2 + v2.2 amended + v2.3 amended)
status: FIX-FORWARD v2.3.1 — 8 new MUSTs (#60-#67); NO full re-cut; convergence on spec-level typos
---

# Multi-Agent Reconciliation #4 — Spec-Typo Debugging

Five reviewers on cumulative artifact (8bb0f9f + d7db3f1 + e940e8d).
Pattern holds: **Pass 1→14, Pass 2→16, Pass 3→15, Pass 4→8 new.**
This pass's findings are **spec-text typos and placeholders**, not
architecture/design gaps. Same class as proof-reading a near-final
document.

## Verdict matrix

| Reviewer | Verdict | Strongest finding |
|---|---|---|
| Architecture | APPROVE_WITH_FIXES | 2 self-flagged spec bugs at v2.3 lines 357-365 (Q39 + MED-A); everything else clean |
| GTO theorist | APPROVE_WITH_FIXES | Same spec bugs at 357/363; MUST #45 tri-state weighting 2× correct; Q41 0.15 slightly aggressive but defensible |
| Red-team | **REWORK** | 3 CRITICAL: case-insensitive claim false (frozenset of 3 literals); MUST #46 spec bugs unfixed; MUST #47 markers not landed on origin |
| Practical pro | APPROVE_WITH_FIXES | 8-entry list confirmed + T_J02 YAML spelled; only MED-A surviving_weight same Q39-class |
| Research | APPROVE_WITH_FIXES | Stratified sampling on MUSTs #54 + #52 |

**Aggregate:** REWORK-LITE. Red-team's 3 CRITICAL findings are real
but are 3 concrete text edits, not architecture work. Other 4
reviewers converge on MEDIUM-only fixes. **Call this a v2.3.1 fix-
forward patch, not a full v2.4 re-cut.**

## Why NOT full pass #5

Standing discipline: multi-agent review for load-bearing changes.
Red-team's CRITICALs this pass are:
- Typo-class (`case-insensitive` only handles 3 literals)
- Placeholder-class (AFTER block has `# placeholder; real: weight sum` unfixed)
- Metadata-class (SUPERSEDED markers described in amendment text but not physically inserted in v2/v2.2 files)

None require architectural redesign. All are fixable in single-site
edits. Running a 5-reviewer panel again would be disproportionate to
the scope. Orchestrator-only read-check on v2.3.1 is sufficient,
followed by ALL-CLEAR if clean.

Pattern convergence justifies the compression.

## NEW MUSTs

### CRITICAL (3 — spec text fixes required before commit 4)

#### MUST #60 — Fix §2.2 multiway aggregation spec bugs

Three related code bugs in v2.3 §2.2 AFTER block (lines 357-365):

**(a) Q39 chain_steps aggregation (self-flagged, unfixed):**
```python
# BROKEN (current spec):
chain_steps = sorted({s for opp in per_villain_ranges for s in per_villain_truncated})
# Iterates per_villain_truncated (Dict[str, bool]) — yields position strings, not steps.

# FIX: track per_villain_chain_steps dict inside loop; aggregate:
chain_steps = [
    f'{opp}:{step}'
    for opp, steps in per_villain_chain_steps.items()
    for step in steps
]
```

**(b) MED-A surviving_weight placeholder (self-flagged as "placeholder; real: weight sum", unfixed):**
```python
# BROKEN:
surviving_weight = min(per_villain_truncated.values(), default=1.0)
# Min over Dict[str, bool] returns bool, not weight.

# FIX: product-across-opponents (joint survival) OR min-across-opponents (tightest narrowed).
# Recommend: min across per-opponent surviving_weight values (captures tightest narrowing).
surviving_weight = min(
    meta['surviving_weight']
    for meta in per_villain_metas.values()
) if per_villain_metas else 1.0
```

**(c) MED-B — delete v2.2 §3.7 BEFORE block in commit 4 diff:**
v2.2's §3.7 contained placeholder multiway spec. Commit 4's diff plan
must explicitly delete it (not just amend AFTER block), otherwise
stale BEFORE text stays in the file.

All three land in the same v2.3.1 edit. No separate commits needed.

#### MUST #61 — SUPERSEDED markers actually landed on v2 + v2.2 files

Red-team verified via `git show origin/master` that:
- v2 line 942 still has raw `raise NotImplementedError  # placeholder for blueprint` with no marker
- v2 line 1728 still says "13 call-site tuple-unpacks" without SUPERSEDED note
- MUST #47 described the markers in v2.3 §2.3 text but no actual edits to v2 or v2.2 blueprint files

**Fix:** v2.3.1 commit actually edits:
- `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md` at lines 942 + 1728 (insert markers inline with the stale text)
- `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md` at any superseded line
- Markers: `⚠️ SUPERSEDED BY v2.3 §M46 — see review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_3_AMENDED_2026-04-22.md`

#### MUST #62 — MUST #45 helper true case-insensitive

Red-team attack verified: `_PRIMARY_STRINGS = {'PRIMARY', 'primary', 'Primary'}` handles 3 literals; 'PRiMARY', whitespace-padded ' PRIMARY ', full-width variants all fall to missing-WARN.

**Fix:**
```python
# Replace frozenset-of-3 with canonicalised comparison
def _canonicalize_attention_value(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        clamped = int(val)
        if clamped not in (0, 1, 2):
            raise RuntimeError(f'attention int out of range: {val}')
        return clamped
    if isinstance(val, str):
        s = val.strip().upper()
        if s == 'PRIMARY':
            return 2
        if s == 'CONFIRMED':
            return 1
        if s in ('', '0', 'FALSE', 'NONE'):
            return 0
        raise RuntimeError(f'unrecognised attention string: {val!r}')
    raise RuntimeError(f'attention value wrong type: {type(val)}')
```

Mixed-schema handling: if both `feature_attention` AND `attention_flags` present, raise iff BOTH are non-empty dicts (empty-dict on either side is legitimate migration artifact per pass #3's finding).

### HIGH (4 — fixes required before implementation but same v2.3.1)

#### MUST #63 — MUST #46 cache per-hand invalidation contract

Red-team: cache contract underspec'd; per-hand invalidation rule missing. A multi-hand extraction loop that forgets to null `cached_range` between hands silently reuses prior hand's chain.

**Fix:** Spec in v2.3.1 §M46 addendum:
- Cache is LOCAL to single `extract_all_features(hand)` call. Not persisted across hands.
- Cache populated at entry to helper; discarded at function exit.
- No module-level cache. If needed, use `functools.lru_cache` with per-hand `id(hand)` key.
- Add explicit assertion: if cache survives across calls, raise RuntimeError.

#### MUST #64 — MUST #46 merged-range weight-avg not max

GTO + Red-team + Architecture: `merged[hand] = max(merged.get(hand, 0.0), freq)` across opponents loses density information. Composition features consume `merged` as single "the range" — silently wrong for N>2.

**Fix (builder picks):**
- (a) Replace `max()` with weight-sum then normalise: `merged[hand] = sum(per_opp_freq.get(hand, 0.0) for per_opp_freq in per_villain_ranges.values()) / len(per_villain_ranges)`
- (b) Document that composition features in multiway consume `per_villain_ranges` directly (callers do per-opp composition + aggregate at display); deprecate `merged` entirely

Orchestrator recommends (b) — more poker-correct, eliminates ambiguous aggregation entirely. Composition features are rendered per-villain anyway in the teaching layer.

#### MUST #65 — MUST #48 _HELD_BACK derives from gto_model SOT

Red-team attack: if gto_model.py un-holds `board_adjusted_hrp` without updating the assembler's `_HELD_BACK` frozenset, transition logic silently misclassifies. Same for any new held-back feature.

**Fix:** Export `HELD_BACK_FEATURES` from `gto_model.py` as a module-level frozenset. Assembler + trainer import from there:
```python
from gto_model import HELD_BACK_FEATURES  # single source of truth
def _active_feature_columns():
    return [f for f in FEATURE_COLUMNS if f not in HELD_BACK_FEATURES]
```

#### MUST #66 — MUST #54 stratified sampling across shape categories

Research (Cochran 1977) + Red-team attack: uniform random 10% of ~140 = 14 samples can miss systematic 10-entry pattern errors (35% miss rate).

**Fix:** Stratify by the 8 shape categories from MUST #49 (T_J01/T_J02/T_B05/T_I03/overflow/mass-floor/T_K07/T_E02 type buckets). Guarantee ≥1 sample per shape. Cost negligible; coverage substantially better.

### MEDIUM (1 — optional in v2.3.1; acceptable to defer)

#### MUST #67 — MUST #52 benchmark stratify by num_opponents

Research (Sculley 2015): aggregate p95 across 2/3/4/5-way masks regressions. Should report median+p95 per opponent-count bin; trip gate on worst bin.

**Fix:** `benchmark_multiway_chain.py` bins results by `num_opponents`, emits per-bin + aggregate. Gate trips on WORST bin ≥ 500ms or aggregate p95 ≥ 750ms.

Acceptable to defer to post-Stage-3.5 benchmark run; document in v2.3.1 with planned-enforcement commit.

## Q-resolutions

- **Q39 (chain_steps aggregation syntax):** RESOLVED in MUST #60 — apply builder's proposed fix.
- **Q40 (tri-state binarisation audit log):** APPROVED. Retain tri-state at CSV; binarise at fit-time with per-row audit log. Unlocks v2.5 2-level attention for free.
- **Q41 (medium_made bet=0.15 GTO):** ACCEPTED AS IS with doc note. Slightly aggressive vs 0.10-0.12 solver-typical for 3-way, but defensible for teaching-tool calibration. Add KB §1.11 footnote: "v2.4 river medium_made bet-freq 0.15 chosen for teaching-asymmetric bias; v2.5 solver-alignment may lower."

## Stage 3 forward-looking

GTO flagged: Stage 3's v3.2 prompt should explicitly define PRIMARY
vs CONFIRMED vocabulary for labeller consistency. Not a Stage 3.5
MUST; track as Stage 3 deliverable prerequisite. Add to manifest
v1.11 note when Stage 3.5 ships.

## What v2.3.1 fix-forward must include

Single new commit on top of e940e8d. Naming: `BUILDER_V24_STAGE35_BLUEPRINT_V2_3_1_PATCH_2026-04-22.md`
(or amend v2.3 in-place — your call; single-document review trail
either way).

Required content:
- §M60 — three spec text fixes (Q39 + MED-A + MED-B)
- §M61 — actually edit v2 + v2.2 blueprints with markers
- §M62 — true case-insensitive helper
- §M63 — cache per-hand invalidation contract
- §M64 — weight-avg or per_villain_ranges-direct (pick one; orchestrator recommends b)
- §M65 — HELD_BACK from gto_model SOT
- §M66 — stratified sampling for MUST #54
- §M67 — (optional) stratified benchmark for MUST #52
- Q41 KB footnote addition to v3.1 prompt derivation notes

No commits to production code. Spec-only edits. Blueprint v2 base
AND v2.2 amendment both get small edits (markers); v2.3 gets a
patch or in-place update.

## Orchestrator-only read-check (not full pass #5)

After v2.3.1 pushed, orchestrator reads the amendment, verifies:
- MUST #60 code blocks are syntactically correct and semantically
  match the fix (no new placeholders)
- MUST #61 markers actually land on v2 + v2.2 files at the cited
  line numbers (`git show origin/master:...line 942` shows the marker)
- MUST #62 helper canonicalisation is complete
- Other MUSTs addressed or explicitly deferred with reasoning

If clean → **ALL-CLEAR directive** authorising implementation per
the commit sequence.

If orchestrator check surfaces new CRITICAL → dispatch pass #5 (full
5-reviewer panel). Expected to not happen.

## Discipline rules in force (unchanged)

- GitHub is project state (`git show origin/master:<path>`)
- DECIDE and EXECUTE
- Quality default
- Push back on unclear

## Immediate builder action

Auto mode. Builder executes without further orchestrator input:

1. Source-verify the 3 CRITICAL + 4 HIGH findings against origin
2. Cut v2.3.1 patch amendment
3. Actually edit v2 + v2.2 files on origin per MUST #61
4. Push
5. Ping orchestrator for single read-check

Then orchestrator issues ALL-CLEAR + implementation commit sequence
begins.
