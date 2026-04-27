---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (builder; named author) · Reviewer streams · QC stream · Owner
re: Phase 4 directive — fix allocator bug in build_corpus_revision_500_hand.py (MAGG=0 root cause); re-run C2; defer module-expansion decision until allocator is correct
status: DIRECTIVE — Phase 4 build (allocator fix); blocks Phase 5 module-expansion-or-target-relax decision until we know what the allocator alone can recover
---

# Phase 4 directive — fix allocator (MAGG=0 root cause)

## Diagnosis

Builder's Phase 3 v2 report at PR #70 (DRAFT) head `174bbc3` shows C2 verification fails with **MAGG=0/40 despite 10 MAGG records being in the pool**. Root cause is **NOT** pool undersize; it's an allocator bug.

### The bug

`scripts/build_corpus_revision_500_hand.py` `_phase_a_select` (lines 302-380) uses **first-come-first-served greedy allocation** in a hard-coded category order:

```python
_pick(pfa_pool, 80, 'PFA c-bet (Rule 4)')
_pick(nfd_raise, 20, 'NFD RAISE (air >= 0.20)')
_pick(nfd_call, 20, 'NFD CALL (air < 0.20)')
_pick(nfd_boundary, 10, 'NFD boundary cases')
_pick(bac_pool, 20, 'BAC (MW-30 callers >= 1)')
_pick(monster_pool, 20, 'Monster facing bet (MW-33)')
_pick(magg_pool, 40, 'MAGG river (villain_agg >= 2)')   # <-- by now MAGG fingerprints are exhausted
_pick(spr_standard, 50, 'Standard SPR (4-8)')
...
```

Each `_pick` adds chosen fingerprints to `used_fps`. Subsequent `_pick`s skip those fingerprints. **A MAGG record that ALSO satisfies PFA/NFD/BAC/monster criteria is consumed by the earlier category and unavailable for MAGG.**

In the actual run: all 10 MAGG records (multi-aggressive river spots) presumably also satisfy PFA (`is_preflop_aggressor=1`) since the v3.2 v2 MAGG templates use BB-as-villain construction (BB calls preflop, hero is opener → hero IS PFA → record passes `_is_pfa_hand`). So the PFA pick at quota 80 consumes them before MAGG's turn.

### Why this fix matters before module expansion

If we reach a clean allocator and STILL fall short on category quotas, then we know module expansion is genuinely needed. If we fix the allocator and quotas fill, no module expansion needed. **Don't run an expensive 9-module redesign if it's avoidable.**

## Fix spec — F5: rare-category-first allocator

### File: `scripts/build_corpus_revision_500_hand.py`

Replace the greedy `_phase_a_select` algorithm with **constraint-aware assignment** that prioritises rare categories.

### Algorithm

```python
def _phase_a_select(pool, forbidden_fps, rng):
    # Step 1: classify each pool record into ALL categories it satisfies
    category_membership = {}  # rec_id -> set of category names
    for rec in pool:
        rid = id(rec)  # or use fingerprint
        cats = set()
        if _is_pfa_hand(rec): cats.add('pfa')
        if _is_magg_hand(rec): cats.add('magg')
        if _is_bac_hand(rec): cats.add('bac')
        if _is_monster_hand(rec): cats.add('monster')
        if _is_nfd_hand(rec):
            if _validate_nfd_boundary(rec): cats.add('nfd_boundary')
            elif rec['feat_dict'].get('villain_air_pct', 0) >= 0.20: cats.add('nfd_raise')
            else: cats.add('nfd_call')
        if _is_rule11_hand(rec): cats.add('rule11')
        if _is_donk_hand(rec): cats.add('donk')
        if _is_sb_hero_hand(rec): cats.add('sb')
        spr = rec['feat_dict'].get('spr', 0)
        if spr >= 4.0: cats.add('spr_std')
        elif 2.0 <= spr < 4.0: cats.add('spr_med')
        category_membership[rid] = cats
    
    # Step 2: count pool yield per category
    yield_per_cat = {cat: 0 for cat in QUOTAS}
    for cats in category_membership.values():
        for c in cats: yield_per_cat[c] += 1
    
    # Step 3: define target per category (the existing quotas)
    targets = {
        'pfa': 80, 'magg': 40, 'bac': 20, 'monster': 20,
        'nfd_raise': 20, 'nfd_call': 20, 'nfd_boundary': 10,
        'rule11': 10, 'donk': 25, 'sb': 20,
        'spr_std': 50, 'spr_med': 40,
    }
    
    # Step 4: compute "scarcity" per category: target / yield (higher = rarer relative to need)
    scarcity = {cat: targets[cat] / max(1, yield_per_cat[cat]) for cat in targets}
    # categories with scarcity >= 1.0 are at-or-over-capacity
    # categories with scarcity > 1.0 are under-yield (cannot fully fill)
    # categories with scarcity < 1.0 have surplus pool yield
    
    # Step 5: assign each record to ONE category, prioritising rare-AND-needed
    # For each record's set of matching categories:
    #   pick the category with highest scarcity that still has unfilled target
    selected_per_cat = {cat: [] for cat in targets}
    used_fps = set(forbidden_fps)
    
    # Sort records by their "hardest match" (record that fits only rare categories goes first)
    pool_sorted = sorted(pool, key=lambda r: (
        # rarity score: max scarcity among matching categories — higher = harder to place elsewhere
        -max((scarcity[c] for c in category_membership[id(r)]), default=0)
    ))
    
    for rec in pool_sorted:
        fp = _fingerprint_record(rec)
        if fp in used_fps: continue
        cats = category_membership[id(rec)]
        if not cats: continue
        # pick the category with max scarcity that still has unfilled target
        best_cat = max(cats, key=lambda c: (scarcity[c] if len(selected_per_cat[c]) < targets[c] else -1))
        if len(selected_per_cat[best_cat]) >= targets[best_cat]: continue
        selected_per_cat[best_cat].append(rec)
        used_fps.add(fp)
    
    # Step 6: flatten + return
    selected = [r for cat_recs in selected_per_cat.values() for r in cat_recs]
    for cat in targets:
        n_filled = len(selected_per_cat[cat])
        n_target = targets[cat]
        n_yield = yield_per_cat[cat]
        status = 'FULL' if n_filled >= n_target else f'UNDER (yield {n_yield})'
        print(f"[Phase A] {cat}: {n_filled}/{n_target} {status}")
    print(f"[Phase A] Total selected: {len(selected)}/{sum(targets.values())}")
    return selected, used_fps
```

### Key properties

1. Records are assigned to ONE category (their rarest-matching category), preventing double-counting.
2. Categories with high scarcity (target much greater than yield) get priority over abundant categories.
3. Records with limited match options get assigned first (so PFA records that fit only PFA stay for PFA; MAGG records that fit MAGG+PFA get assigned to MAGG since MAGG is rarer).
4. Output prints UNDER status with actual pool yield, making it obvious if category yields are genuinely insufficient (signalling Phase 5 module expansion need).

### Test additions

`river-rats-core/tests/test_corpus_revision_v3.py` — new test class `TestRareCategoryFirstAllocator`:

1. `test_magg_records_assigned_to_magg_not_pfa`: synthetic pool with 10 MAGG records that ALSO satisfy PFA criteria + 100 PFA-only records. Assert at least 10 of the 12 categories (MAGG) get filled.
2. `test_scarcity_ordering`: pool with rare-cat (5 yield, target 10) and common-cat (100 yield, target 10). Assert rare-cat fills first.
3. `test_no_fingerprint_dupes_after_assignment`: assert assigned records have unique fingerprints.
4. `test_targets_dict_matches_phase_a_quotas`: structural — targets dict matches the documented Phase A quota table.

## Verification gate (before opening F5 PR)

1. All 43 prior tests still pass + 4 new tests pass = 47 passed.
2. Run C2 against the existing pool (master `174bbc3` files) and confirm:
   - MAGG: ≥10 (the 10 records in pool should now actually land)
   - Other categories: per-category yield reported correctly; categories with under-yield reported as UNDER with explicit yield count
   - Total improvement vs the 313-hand failing run

## PR

- Branch: `programmer/allocator-rare-cat-first-2026-04-27`
- Files: `scripts/build_corpus_revision_500_hand.py` + tests only — no other changes
- PR title: `Builder Phase 4: rare-category-first allocator (fixes MAGG=0/40 bug)`
- Body: explain the bug, the fix, before/after verification

## Round 4 review

Two reviewers (gto-expert NOT needed — this is allocator algorithm, not poker domain):

1. **ml-architect**: algorithm correctness; corner cases (empty pool, single-cat records, scarcity ties); test coverage of the synthetic MAGG-PFA scenario
2. **QC**: paired V-Implementation-Spec-Match (rare-cat-first algorithm at canonical paths) + V-Integration-Trace (run on existing 327-record pool; confirm MAGG ≥ 10 actually flows end-to-end)

QC gate per memory `feedback_qc_required_before_approval.md`.

## After F5 PR merges — RE-RUN C2

Builder runs:
1. `git pull --ff-only origin master`
2. Re-execute C2 against existing pool files (Mode A + Mode B already on the data branch are still valid):
   ```
   python3 scripts/build_corpus_revision_500_hand.py \
     --pool data/corpus_revision_pool_combined_2026-04-27.jsonl \
     --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
     --target-new 400 --seed 20260427 \
     --output data/corpus_revision_500_hand_2026-04-27.jsonl \
     --lock-output data/corpus_revision_500_hand_2026-04-27.lock
   ```
3. Generate **Phase 4 verification report** at `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_PHASE4_2026-04-27.md`. Compare before/after per-category yields.
4. Force-push the data PR (#70) with new corpus + lock + report. Update PR body.

## Phase 5 decision (deferred)

After F5 + re-run C2, the per-category report tells us:
- **If all quotas fill (or fall back to known-acceptable understocks like NFD-boundary 4)**: PR #70 unblocks; round 3 review chain dispatches; corpus revision pipeline complete.
- **If some quotas still UNDER**: those are categories with genuine pool yield insufficiency. Phase 5 directive then targets only those modules (NOT a 9-module redesign). Architect Phase 2.7 dispatched ONLY for under-yielding modules.

This sequencing avoids over-investing in scenario expansion if the allocator fix alone resolves the issue.

## Workaround driver script disposition (deferred to Phase 6)

`scripts/run_mode_a_pool_with_positions.py` (builder's Path B workaround for missing `--positions` flag) is currently in the data PR. After Phase 4 + Phase 5 resolve the corpus, Phase 6 directive cleans it up: dispatch a small code-change PR adding `--positions` flag to `generate_corpus_revision_pool.py` (the original Phase 3 directive's Path A) and removes the workaround driver. Tracked.

## NIT items (tracked for future cycles)

- Phase 3 directive's E3 + C2 CLI flag specs were wrong (mismatch with actual scripts). Fix in next directive's spec block by reading the script's argparse first.
- Builder's `5685605` direct push of v1 report to master violated PR workflow. Discussed; not blocking.
- Phase 3 directive's "111 records" Mode B count was a typo (actual 115). Update directive references.

## References

- Builder Phase 3 v2 report: `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md` on PR #70 branch (head `174bbc3`)
- Phase 3 directive: `MAIN_TERMINAL_BUILD_EXECUTE_PHASE3_DIRECTIVE_2026-04-27.md` (master `2e317c5`)
- Build-execute directive: `MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`)
- Round 2 synthesis: `MAIN_TERMINAL_PR60_PHASE2_SYNTHESIS_2026-04-27.md` (master `8621f9a`)
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`

**Status: PHASE 4 DIRECTIVE OPEN. Builder authors F5 (rare-cat-first allocator). ml-architect + QC review. After merge, re-run C2. Decide on Phase 5 (module expansion) only after seeing post-fix yields.**
