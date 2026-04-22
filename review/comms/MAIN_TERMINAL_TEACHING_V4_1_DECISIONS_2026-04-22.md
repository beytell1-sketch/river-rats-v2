---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Teaching · Builder · Owner
re: Resolutions on teaching's v4.1 NaN-render review doc (teaching-repo commit 42dd794, not pushed to origin)
status: DECISIONS — 10 items resolved; teaching unblocked to draft plan + start C1
---

# Teaching v4.1 NaN-Render — Orchestrator Decisions

Teaching's review doc at `river-rats-teaching:review/comms/TEACHING_V4_1_ORCHESTRATOR_REVIEW_2026-04-22.md`
(local commit 42dd794; not pushed to teaching origin — see §11). Read
verbatim; teaching's analysis is sound on all 10 items.

Orchestrator policy on this type of doc: ticket vs directive
reconciliation is orchestrator work (confirming teaching's §9 framing).
Where my directive diverged from the ticket without strong reason,
ticket wins. Where the directive added specification detail not in the
ticket (sentinel render wording, flag-kind introduction), the merit
question is resolved here.

Summary of outcomes: **teaching's recommendations accepted on all 10
items**, with one cross-stream follow-up flagged to builder (see §4).

## Decisions

### §4.1 — `range_rendering_mode` vocabulary + public-field status

**Decision: ACCEPT teaching's recommendation.**

Final spec:
- Field name: `range_rendering_mode` (public, no underscore)
- Type: `Literal["normal", "folded", "overflow"]`
- `"folded"` iff `_villain_folded=True` (upstream)
- `"overflow"` iff `_villain_chain_overflowed=True` (upstream; covers
  both over-narrow-to-empty and mass-floor truncation per MUST #28)
- `"normal"` otherwise

Rationale: the mode names upstream **state** (what the signal was),
not renderer **strategy** (what the adapter chose). State-naming is
more stable: renderer strategy can evolve without schema breaks.
"Suppressed" collapsed folded+overflow into one label, losing
observably-different information. Field is public because it crosses
the adapter boundary — game UI reads it to decide which block to
render or skip.

My directive was wrong on both the underscore prefix and the vocabulary
collapse. Ticket wording stands.

### §4.2 — Overflow observation wording

**Decision: ACCEPT teaching's recommendation (ticket wording).**

Final string:
> "Villain's line is too rare to read confidently — relying on equity alone."

Rationale: ticket wording is more informative — names the fallback
("equity") explicitly and hedges accurately ("too rare to read
confidently" vs my directive's "too unusual to narrow — using equity
only"). Practical-pro's pass-#3 tweak ("unusual" over "rare") was a
minor polish; not load-bearing; teaching's ticket-wording preference
is correct.

### §4.3 — `kind: CONTEXT` interpretation

**Decision: (a) doc-only category.**

Final spec:
- `FlagEntry` dataclass stays structurally unchanged (3 fields:
  `kind: str`, `trigger_value: Optional[float]`, `observation_text: str`)
- `trigger_value` widens to `Optional[float]` to accommodate sentinels
  with no magnitude
- Two new `kind` string values: `villain_folded_sentinel`,
  `villain_chain_overflowed_sentinel`
- `CONTENT_API.md` groups these two kinds under a "CONTEXT" heading
  for readability. Documentation-only; not a new schema field.
- Game adapter needs zero breaking changes — just picks up the new
  `kind` strings + renders their verbatim `observation_text`.

Rationale: adding a `category: str` field to FlagEntry would be a
v4.1 schema break requiring adapter coordination. Doc-only category
achieves the readability goal at zero schema cost. Teaching's
"CONTEXT" interpretation was correct.

### §4.4 — `nut_flush_block` under sentinel

**Decision: ACCEPT teaching's recommendation — `nut_flush_block` is
hero-side; stays 0/1 in all modes.**

Final spec:
- `nut_flush_block` EXCLUDED from NaN suppression list
- Remains int 0 or 1 in `folded` and `overflow` modes
- Renders normally in primary window (subject to flag-window design
  when blocker 2-flag ticket ships)

Rationale: `nut_flush_block` is a boolean derivative of hero's own
hand + board (does hero hold the Ax of a 2+-suited board). Does not
depend on villain's range. When villain folds, the boolean is still
well-defined — hero either blocks the nut flush or not. My directive
wrongly grouped it with villain-composition-dependent features.

**CROSS-STREAM FOLLOW-UP TO BUILDER (§4 below):** logic-side commit
4/4.1 spec for MUST #10 needs to confirm `nut_flush_block` stays
int 0/1 under sentinel conditions (NOT NaN). If current implementation
NaN-flags it, small follow-up patch in a future commit. Builder
verifies + reports.

### §4.5 — Equity prose in folded mode

**Decision: ACCEPT teaching's recommendation — suppress equity in
folded mode per ticket §2.5.**

Final spec:
- `folded` mode: ONLY the sentinel observation text renders
  ("Villain folded earlier — no range to read.")
- No equity prose, no composition, no blocker flags, no board favour
- `overflow` mode: equity prose renders (raw_equity, equity_vs_range);
  composition + blockers suppressed per MUST #10

Rationale: equity against folded villain is semantically invalid.
Stricter-default is safer — revisit post-playtest if learners need
more context. Teaching's ticket-§2.5-alignment is correct.

### §4.6 — Version numbering

**Decision: v4.1.**

Final: CONTENT_API bumps 4.0 → 4.1; schema tag `l3_enriched_v4.1`.
Ticket's v3.0 → v4.0 reference was drafted with stale info (teaching
had already shipped v4.0 on 2026-04-20). Directive was correct; no
arbitration needed.

Orchestrator will bump `RELEASE_MANIFEST.yaml` `teaching_schema`
entry to `l3_enriched_v4.1` when teaching ships.

### §5-Q1 — Per-villain position identity in enriched_row

**Decision: iterate `_per_villain_folded.keys()` / `_per_villain_composition.keys()`.**

No explicit `folded_villain_positions` / `live_villain_positions`
fields needed at v4.1. Teaching derives:
```python
folded_positions = [p for p, folded in _per_villain_folded.items() if folded]
live_positions = [p for p, folded in _per_villain_folded.items() if not folded]
```

Rationale: dicts keyed by `opp_pos` already convey identity via
`.keys()`. Explicit convenience lists would be a logic-side addition
for marginal benefit. If teaching later finds iteration patterns
cumbersome, file as a small v2.5+ convenience-API ticket.

### §5-Q2 — Blocker flag placeholder suppression

**Decision: OUT OF v4.1 SCOPE.**

Blocker flag 2-flag design is deferred to post-Stage-6 (per manifest
`queued.teaching_blocker_flag_design`). When that ticket drafts, it
handles its own mode-awareness (folded → suppress blocker flag;
overflow → suppress). Not v4.1's job.

### §5-Q3 — Equity in folded mode

**Decision: same as §4.5 — suppress.**

### §6 — Fixture source for C5

**Decision: (a) synthetic first, (b) production rows when available.**

Teaching hand-authors 4 synthetic fixtures now:
1. HU folded (villain folded on a prior street)
2. HU overflow (chain over-narrowed OR mass-floor truncated)
3. Multiway partial-fold (one villain folded, one live)
4. Multiway all-live (both villains still in hand; per_villain rendering)

Swap for production rows once logic's commit 4.1 is clean and
real-shape data is available (expected soon — commit 4.1 approved
this session; remaining commits 5-16 are smaller per-MUST scope).
Hardening re-pass with production rows in SHIP REPORT catches any
drift.

Unblocks C3 renderer work in parallel with logic's ongoing Stage 3.5
implementation.

## 2. Additional orchestrator input — range rendering follow-up

Owner raised in separate playtest that current wording "where our
hand sits among all hands we'd play this way" (backed by
`hero_range_percentile`) is not useful. Filed as v2.5 ticket at
`TICKET_V25_HERO_RANGE_BOARD_COMPOSITION_2026-04-22.md`; manifest
v1.11.

Teaching impact — NOT v4.1 scope, but add to v4.1 plan as a
**separate sub-commit**:

**Immediate non-blocking fix** to the current hero_range_percentile
rendering. Teaching picks one:
- (a) Rewrite the current wording to honestly describe the scalar:
  "Relative rank of your hand within your opening range on this
  board (0-100%)."
- (b) Drop the field from display until v2.5 structured composition
  lands.

Orchestrator has no preference between (a) and (b); teaching owns
the learner-facing decision. If (a), GTO + V3 reviewer validates
the new wording; if (b), remove the rendering entry and add a
follow-up note to pick up at v2.5.

This is a **separate commit** (not entangled with NaN-render sentinel
work). Teaching may land it as C7 at the end of the v4.1 sequence,
or earlier if it's lighter than C1-C6. Builder's v2.5 hero-composition
work lands after Stage 6 v2.4 ship.

## 3. Consolidated final spec for teaching

Single table teaching can build to:

| Field | Type | Folded | Overflow | Normal |
|---|---|---|---|---|
| `range_rendering_mode` | Literal["normal","folded","overflow"] | "folded" | "overflow" | "normal" |
| villain_top_pair_plus_pct | float | absent | absent | present |
| villain_draw_pct | float | absent | absent | present |
| villain_air_pct | float | absent | absent | present |
| villain_medium_made_pct | float | absent | absent | present |
| flush_block_pct | float | absent | absent | present |
| flush_draw_block_pct | float | absent | absent | present |
| straight_draw_block_pct | float | absent | absent | present |
| nut_made_block_pct | float | absent | absent | present |
| `nut_flush_block` | int (0/1) | **present** | **present** | present |
| board_favour | float | absent | absent | present |
| raw_equity | float | absent | **present** | present |
| equity_vs_range | float | absent | **present** | present |
| Primary-window composition prose | string | absent | absent | present |
| Blocker flags | List[FlagEntry] | absent | absent | present (when blocker design ships) |
| Sentinel flag | FlagEntry | villain_folded_sentinel | villain_chain_overflowed_sentinel | none |

Sentinel observation strings (verbatim):
- `villain_folded_sentinel`: "Villain folded earlier — no range to read."
- `villain_chain_overflowed_sentinel`: "Villain's line is too rare to read confidently — relying on equity alone."

Multiway partial-fold preamble (verbatim):
- "Villain {FOLDED_POS} folded; reading against villain {LIVE_POS} only."

## 4. Cross-stream follow-up to builder

**Action required (NOT commit 7 scope; add to commit backlog):**

Verify commit 4/4.1 implementation treats `nut_flush_block` as
hero-side (stays int 0/1 under `_villain_folded=True` and
`_villain_chain_overflowed=True`), NOT NaN.

Specifically: MUST #10 spec said "NaN across composition + continuous
blockers." The word "continuous" matters — `flush_block_pct`,
`flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`
are continuous 0-1; `nut_flush_block` is boolean 0/1. Should not
NaN-flag.

If commit 4.1 correctly excludes `nut_flush_block` from NaN-flagging:
flag as ALREADY CORRECT; document in next commit message.

If commit 4.1 NaN-flags it: small follow-up patch in a near-term
commit (not urgent; playtest impact is teaching-layer render of a
stable boolean vs absent — both survivable).

Builder's commit 7 is not blocked on this.

## 5. Teaching's commit sequence (v4.1 plan)

Teaching may now draft `TEACHING_V4_1_NAN_RENDER_PLAN_2026-04-22.md`
in `river-rats-teaching:review/comms/` with decisions above folded
in. Expected sequence:

1. C1 — CONTENT_API.md v4.1 spec update (schema table, sentinel
   strings, mode vocabulary)
2. C2 — FlagEntry schema: `trigger_value: Optional[float]`; two new
   kind strings
3. C3 — Renderer logic (sentinel detection, mode routing, field
   suppression)
4. C4 — Guard-leak scanner extensions for new sentinel vocabulary
5. C5 — Fixture tests (4 synthetic hands now; swap to production
   when logic commit 4.1 real rows available)
6. C6 — SHIP REPORT + hardening re-pass with real rows
7. C7 (optional / separate) — hero_range_percentile wording cleanup
   per §2 above

GTO + V3 compliance reviewer pass on the plan. Per-commit V3 reviewer.
Hardening re-pass before ship-gate. Standard teaching discipline.

## 6. Stage-6 ship-gate dependency

Per revised MUST #57 gate timing (moved from commit-4-merge to
Stage-6-ship-gate in my commit-4 path-B directive): CONTENT_API v4.1
ship-readiness gates Stage 6 v2.4 production activation, not
commit 4 merge. Teaching works in parallel; orchestrator coordinates
at Stage 6 ship-gate pre-flight.

Stage 6 pre-flight will verify:
- CONTENT_API v4.1 shipped + version-pinned
- Game adapter picks up new kind strings + mode field
- Playtest log schema tolerates absent/NaN patterns
- Hardening re-pass SHIP REPORT clean

## 7. Push permission note

Teaching flagged that `git push origin master` in
`~/river-rats-teaching/` was denied by auto-mode classifier. The
previous 11 commits pushed successfully. This is a Claude auto-mode
permission, not a GitHub issue.

Owner: two reasonable paths (same as teaching offered):
- Keep auto-mode rule; teaching pushes doc commits to a feature
  branch (`teaching/v4-1-orchestrator-review`), orchestrator reads
  from there; merges to master when convenient
- Relax the rule via `~/river-rats-teaching/.claude/settings.json`
  or project-level settings to allow `git push origin master` in
  that repo, restoring direct-to-master flow

Not urgent for this decision exchange — orchestrator wrote response
into v2 repo's comms (which I can push), teaching reads from v2
origin. Going forward, teaching's own comms + commits need a push
path. Owner's call.

## 8. What unblocks now

Teaching:
1. Reads this doc from v2 origin (commit lands on push)
2. Drafts `TEACHING_V4_1_NAN_RENDER_PLAN_2026-04-22.md`
3. Dispatches GTO + V3 compliance reviewer parallel pass on plan
4. C1 begins per plan

Builder:
1. Proceeds to commit 7 (MUST #23 + #55) per prior directive — no
   change to logic-side commit sequence
2. Verifies nut_flush_block treatment per §4 follow-up in a
   convenient upcoming commit (not blocking commit 7)

Owner:
1. Reads this summary
2. Decides push-permission path for teaching if flow matters (see §7)
3. Standing by for teaching's plan drop + builder's commit 7 ping

## 9. Standing by

Orchestrator logs: v2.5 hero-range-board-composition ticket
(e259045), this decisions doc, and commit 7 directive all consistent
with manifest v1.11.

Teaching + builder work in parallel. Next status-point is whichever
pings first: teaching's v4.1 plan ready for multi-agent review, OR
builder's commit 7 ready for architect review.
