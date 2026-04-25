---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Teaching builder · Owner
re: Commit 14 (Finding B fold-in) LANDED on v2 origin/master at b0ef6c5; teaching HOLD #5 + #3 cleared upstream-side; teaching may begin C5.2 fixture swap on owner confirmation
status: CROSS-STREAM UNBLOCK — teaching's PRE-VERIFICATION HOLD trigger has fired; per 3-gate rule from MAIN_TERMINAL_TEACHING_LOOP_SETUP_2026-04-25.md, teaching surfaces to user + waits for explicit "begin C5.2" confirmation before foregrounding execution
---

# Teaching — Commit 14 Landed — Unblock Signal

## What landed

PR #7 merged at `b0ef6c5` on v2 origin/master. Commit 14 (Finding
B fold-in) promotes the multiway per-villain fields from
`chain_meta` onto the features dict in
`extract_range_composition`:

- `_per_villain_folded` — Dict[str, bool], opponent → folded flag
- `_per_villain_composition` — Dict[str, Dict[str, float]],
  opponent → {tp_plus, medium, draw, air} composition fractions
- `_per_villain_overflowed` — Dict[str, bool], opponent → over-
  narrow sentinel flag

Plus 4 new tests in `test_commit14_finding_b.py` covering:
- `test_must46_per_villain_folded_promoted_in_multiway`
- `test_must46_per_villain_composition_promoted_in_multiway`
- `test_must46_per_villain_overflowed_promoted_in_multiway`
- `test_must46_per_villain_empty_dict_in_HU` (regression: HU rows
  produce empty dicts, not absent keys)

GTO verdict at `36e18be` confirmed cross-stream contract READY.

## What this unblocks for teaching

Per the locked Stage 4 plan + held SHIP REPORT:

1. **HOLD #5 CLEARED** — multiway field promotion is on master.
   Real commit-14-era `extract_all_features` output now populates
   the three `_per_villain_*` fields that C5.2 fixture swap needs.

2. **HOLD #3 (C5 fixture swap F3/F4) NOW EXECUTABLE** — the
   plumbing teaching pre-prepared in C5.2-pre-prep (`6ca0492`) was
   waiting on these upstream fields. With commit 14 landed,
   teaching can:
   - Run `extract_all_features()` from v2 commit-14 production
     state on F3 / F4 multiway hands
   - Swap the synthetic `data/sentinel_mw_partial.jsonl` and
     `data/sentinel_mw_live.jsonl` for real commit-14 production
     rows
   - Re-run the V3 scanner on all 4 fixtures (F1 was real from
     C5.1; F2 real from C5.1; F3 + F4 will become real now)
   - Update SHIP REPORT to drop PRE-VERIFICATION marker on §5.3

## C5.2 sequence (from MAIN_TERMINAL_TEACHING_C7_HOLD_2026-04-25.md)

Per the locked teaching sequence, post-commit-14:

```
[commit 14 LANDED — this trigger]
  → C5.2 (real-row F3/F4 swap, data-only on the C5.2-pre-prep
     plumbing)
  → V3 per-commit review on C5.2
  → C7 (hero_range_percentile wording cleanup, doc-only)
  → V3 per-commit review on C7
  → SHIP REPORT promotes from PRE-VERIFICATION to FULL VERIFICATION
  → Orchestrator pre-Stage-6 gate (HOLD #4)
  → Merge greenlight
  → Open PR `teaching/v4-1-nan-render` → master
  → Merge teaching v4.1 ship
```

C5.2 + C7 are both relatively bounded scopes. C5.2 is data-only
(fixture swap on the existing C5.2-pre-prep plumbing). C7 is
doc-only.

## Three-gate rule for teaching execution

Per the loop setup directive, teaching DOES NOT auto-start C5.2
even with commit 14 landed. Three gates required:

1. ✅ **Commit 14 on v2 master** — fired now
2. ✅ **Orchestrator cross-stream notification** — this doc
3. ⏳ **Explicit user confirmation** — teaching's loop surfaces to
   owner: "begin C5.2 fixture swap?"; awaits explicit go

If teaching is in /loop overnight, the loop catches commit 14 +
this notification on its next sweep (default cadence 30 min once
commit 14 detected). User wakes to teaching surfacing the unblock
+ asking confirmation.

If teaching is NOT in /loop (loop activation block was provided
but unverified): owner can manually paste the activation block in
the teaching terminal on wake, OR direct teaching builder to begin
C5.2 manually.

## Session-launch reminder

Per `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md`: teaching
builder's session must be launched from `~/river-rats-teaching/`
for V3 reviewer dispatch availability. If the current teaching
session was launched from elsewhere, exit and re-launch from
`~/river-rats-teaching/` BEFORE C5.2 begins (so V3 review can
dispatch when C5.2 commit lands).

Smoke-test V3-compliance-reviewer in available subagent list before
beginning C5.2 work.

## What teaching does NOT need to do

- Does NOT touch v4.1 SHIP REPORT until C5.2 + C7 both ship + V3
  reviewed
- Does NOT auto-merge teaching/v4-1-nan-render to master until
  orchestrator pre-Stage-6 gate clears (HOLD #4)
- Does NOT modify Path B (range_position_desc) in this sequence —
  Path B is a separate workstream (HOLD #6) with its own trigger

## Cross-stream contract verification

Before teaching begins C5.2, RECOMMEND a quick verification pass:

```bash
cd ~/river-rats-v2
git pull --ff-only
python3 -c "
from feature_extractor import extract_all_features
# Construct a 3-way multiway hand with one fold
... (teaching team's standard test harness)
result = extract_all_features(hand)
assert '_per_villain_folded' in result
assert '_per_villain_composition' in result
assert '_per_villain_overflowed' in result
print('Cross-stream contract verified')
"
```

If verification fails: STOP, surface BLOCKED to orchestrator. Do
not proceed with C5.2 against a broken contract.

If verification passes: proceed with C5.2 fixture swap when user
confirms.

## Action

**Teaching builder:**

1. (Loop will surface) commit 14 detected + this notification
   landed → ASK user "begin C5.2 fixture swap?"
2. Confirm session launched from `~/river-rats-teaching/` (V3
   reviewer subagent available)
3. On user confirmation: cross-stream contract verification (above)
4. On verification PASS: foreground C5.2 fixture swap
5. On verification FAIL: surface BLOCKED to orchestrator

**Orchestrator (me):**

1. This notification committed (one of three docs in this batch)
2. Loop continues; will see teaching's response on next tick
3. When teaching completes C5.2 → V3 review → C7 → V3 review →
   SHIP REPORT update: that's the trigger for orchestrator
   pre-Stage-6 gate (HOLD #4)
4. Pre-Stage-6 gate clears → teaching merge greenlight

**Owner:** confirm C5.2 begin when ready (or sleep through it;
teaching will hold for the explicit confirmation per 3-gate rule).

## Reference

- `MAIN_TERMINAL_PR_7_MERGED_COMMIT15_GREENLIGHT_2026-04-26.md` —
  parent merge confirmation
- `MAIN_TERMINAL_TEACHING_C7_HOLD_2026-04-25.md` — locked C5.2 → C7
  → SHIP REPORT sequence
- `MAIN_TERMINAL_TEACHING_LOOP_SETUP_2026-04-25.md` — three-gate
  C5.2 start rule
- `MAIN_TERMINAL_GTO_DISPATCH_RESOLUTION_2026-04-25.md` — session-
  launch cwd requirement for teaching subagents
- `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md` —
  Finding B resolution context
