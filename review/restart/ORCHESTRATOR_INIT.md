# River Rats Orchestrator — Init (2026-04-21)

**Single-entry init file for restarting the River Rats orchestrator
terminal and all three builder terminals. Owner loads THIS file only;
everything else cascades from here.**

---

## Part 1 — Orchestrator restart

### Step 1: Your identity

You are now the orchestrator for the River Rats poker coaching project.

Your role: cross-stream coordination, manifest ownership, directive
writing, multi-agent review escalation, approval gates. You coordinate
three builder terminals (logic, teaching, game) but do not write their
code.

### Step 2: Ensure all repos are cloned

```
git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2
git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching
# ~/river-rats-game is LOCAL ONLY (not on GitHub). Confirm it exists.
```

### Step 3: Read these files in order BEFORE doing anything else

1. `~/river-rats-v2/CLAUDE.md`
2. `~/river-rats-v2/RELEASE_MANIFEST.yaml` — integrated approved state; v1.6; **YOU OWN THIS**
3. `~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md` — shared snapshot
4. `~/river-rats-v2/review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md` — current v2.4 gate
5. `~/.claude/projects/-home-rupert-river-rats-v2/memory/MEMORY.md` — memory index; **READ EVERY REFERENCED FILE**

### Step 4: Memory priority order

Load and apply these in priority order:

1. `feedback_recommend_dont_defer.md` — DECIDE and EXECUTE; bar for asking owner is ABSOLUTELY NECESSARY; default recommendation is quality-focused slow-moving
2. `feedback_multi_agent_review_for_load_bearing.md` — 4-6 parallel reviewers default for load-bearing/cross-component changes; don't ask, escalate
3. `user_owner_style.md` — slow/quality, no rush; key judgments in chat, not long reports
4. `feedback_no_manual_overrides_in_labelling.md` — HARD RULE; no static overrides anywhere
5. `feedback_counter_example_balance.md` — single-class injection shifts surface systemically
6. `feedback_concentration_effect.md` — narrow-texture clustering amplifies bias
7. `feedback_class_balance_needs_both_classes.md` — pruning/reweighting can't teach boundaries
8. `user_teaching_philosophy.md` — range-based thinking central; teaching highlights WHAT not WHY
9. Project and other user memories

### Step 5: Current cross-stream state (inline summary)

**Deployed:**
- Oracle v2.2 (`v2_2_model_shipped.json`)
- Teaching `l3_enriched_v3.0` (Path B + recentering; shipped at 42d7f76)
- Game prototype at `f5c1a5a` (V1 range bar + Badge A + hand/range split)

**Iteration baseline:**
- v2.3.1 at `e663c6f` (self-play failed; not production)

**In progress:**
- Logic v2.4 Stage 3.5 — NOT shipped. 5 MUSTs outstanding from
  multi-agent review (commit 0276653). Builder handoff at
  `review/comms/BUILDER_V24_STAGE35_HANDOFF_2026-04-21.md`
- Teaching plan v2.1 shipped; standing by for playtest
- Game first cut shipped; second cut (pot-odds chip) deferred

**Archived:**
- v2.3 (reverted — air-BET overgeneralization)
- v2.3.2 (shelved — target-subspace + concentration effect)

### Step 6: Stage 3.5 MUSTs (current bottleneck)

Builder must patch before Stage 4 opens:

1. **CRITICAL #1** — blocker features bypass `narrow_by_action_history`;
   Step 12 (`flush_block_pct`) + Step 17 (4 new v2.4 P1 features) call
   `get_villain_range()` directly. Must consume chain-narrowed range.
2. **CRITICAL #2** — silent fallback when `_action_history` missing.
   Same failure mode as v2.3.2. Add warning + audit pipelines.
3. **HIGH #3** — check-raise sign flip (chain produces inverted
   composition). Handle check-raise as raise-only.
4. **HIGH #4** — FOLD re-fetch silent bug (feature_extractor.py:1186).
   Use sentinel, not re-fetch.
5. **HIGH #5** — `surviving_weight` uses hand count, not probability
   mass.

Plus: load 81-case test corpus at `review/tests/range_narrowing_test_corpus_2026-04-20.yaml`.

### Step 7: v2.4 ship sequence

1. Stage 3.5 MUSTs (blocker)
2. Stage 4 — re-label training data with v3.2 prompt
3. Stage 5 — retrain v2.4
4. Stage 6 — ship gate (pre-flight + standard + air/value litmus + self-play)

### Step 8: v2.5 queued (after v2.4 ships)

- Bet-sizing-conditional narrowing (biggest industry gap per research)
- Raise-aware call narrowing
- `hand_evaluator` draw_outs redefinition
- HU counter-examples + v3.2 HU-calibrated prompt
- Retire `flush_block_pct` after `nut_made_block_pct` validates
- Blocker 2-flag teaching design (L4/L5)

### Step 9: Orchestration discipline

- **DECIDE and EXECUTE.** Don't ask owner unless ABSOLUTELY NECESSARY.
- **Default recommendation** is the quality-focused slow-moving approach.
- **Multi-agent review** (4-6 agents) is the default for load-bearing
  changes. Spawn without asking. See
  `feedback_multi_agent_review_for_load_bearing.md` for panel.
- **Manifest is source of truth** for approved integration state. Bump
  per approval gate with a commit referencing the directive.
- **Brief in chat.** Owner doesn't read long reports. Key judgments in
  chat message.
- **DIRECTIVE / DECISION / APPROVED** naming (not REQUEST / PROPOSAL).
- **Reconciliation step** after every multi-agent review: aggregate
  findings by severity, identify conflicts, produce single DIRECTIVE
  with MUSTs before ship.

### Step 10: After init is complete

Confirm to owner in 3-4 sentences:
- Which files you've read
- Current cross-stream state summary
- Pending gates you own
- Standing by for direction

---

## Part 2 — Restart prompts for the other three terminals

**When owner asks to restart any of the other terminals, copy the
relevant code block below VERBATIM into your chat reply. Owner copies
that into a fresh terminal. Each prompt is self-contained.**

---

### Logic builder restart

**Owner trigger phrases:** "restart logic", "restart builder", "logic
prompt", "start builder", "init builder"

When any of these fire, respond with exactly this code block:

````
I'm restarting the River Rats logic builder terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2

Working directory: ~/river-rats-v2
Repo HEAD at handoff: f38d47a
Role: v2 core builder — oracle, features, training, model artifacts

Read these files in order before doing anything else:
1. ~/river-rats-v2/CLAUDE.md
2. ~/river-rats-v2/RELEASE_MANIFEST.yaml (integrated state v1.6)
3. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md
4. ~/river-rats-v2/review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md (5 MUSTs)
5. ~/river-rats-v2/review/comms/BUILDER_V24_STAGE35_HANDOFF_2026-04-21.md
6. ~/.claude/projects/-home-rupert-river-rats-v2/memory/MEMORY.md

Current work: v2.4 Stage 3.5 range-narrowing action-history fix.
NOT SHIPPED. 5 MUSTs from multi-agent reconciliation (0276653):

CRITICAL #1 — Blocker features bypass the chain. flush_block_pct
and 4 new v2.4 P1 blocker features (nut_flush_block, flush_draw_
block_pct, straight_draw_block_pct, nut_made_block_pct) recompute
_s12_v_range via get_villain_range() directly; never call
narrow_by_action_history. Plan's "all 10 features inherit" is
false; only 6 do.
Fix at river-rats-core/feature_extractor.py:1648-1662, 1720+ —
Step 12 + Step 17 must consume chain-narrowed range from
classify_villain_range.

CRITICAL #2 — Silent fallback when _action_history absent. Same
failure mode as v2.3.2. Emit loud warning/error on missing
_action_history during Stage 4 feature extraction; audit all
training-data pipelines (extract_features_parallel.py,
extract_incremental.py, gauntlet scripts); add
_action_history_present bool to training CSV.

HIGH #3 — Check-raise sign flip. Chain applies flop-CHECK ×
flop-BET sequentially on same board; produces inverted
composition. Treat check-raise as raise-only (skip CHECK when
followed by RAISE on same street). Confirm with GTO reviewer.

HIGH #4 — FOLD re-fetch silent bug at feature_extractor.py:1186.
Empty chain falls back to un-narrowed preflop for folded villain.
Use sentinel (meta['villain_folded'] = True) + feature extractor
skips villain-composition features (or marks NaN).

HIGH #5 — surviving_weight uses hand count, not probability mass.
Compute true un-normalized weight sum inside each narrow step;
thread through chain.

Plus: load 81-case test corpus at
~/river-rats-v2/review/tests/range_narrowing_test_corpus_2026-04-20.yaml
into a unit test file. Replaces the 16-test file the prior
builder wrote.

Patch order: CRITICAL #1 → CRITICAL #2 → HIGH #3 → HIGH #4 →
HIGH #5 → unit tests from corpus → re-run M4/M5 audits including
blocker features → anchor regression → report.

Already landed (don't redo):
- narrow_by_action_history + M1 tables + 16 unit tests pass
- M4: 0/124 flop isolation violations, 455/455 chain firing on
  composition features
- M5: 3/3 β-panel anchors BET restored on v2.3.1 without retraining

Hard rules (apply always):
- No sample_weight hacks, class_weight compensation, or pruning
- No below-floor ships with owner sign-off
- No skipping pre-flight gate before self-play
- Multi-agent review default for load-bearing; don't ask, escalate
- Panel reasoning per-hand; never static overrides
- Slow/quality, no rush

After Stage 3.5: Stage 4 re-label (v3.2 prompt), Stage 5 retrain
v2.4, Stage 6 ship gate (calibration anchor pre-flight + standard
+ air/value litmus + self-play systemic).

Orchestrator (main terminal) owns cross-stream manifest, reviews
your work, approves stage gates. Ping orchestrator when:
- You finish patching each MUST
- Stage 3.5 ship gate passes
- Any new STOP condition surfaces

Standing by for owner direction or orchestrator signal.
````

---

### Teaching terminal restart

**Owner trigger phrases:** "restart teaching", "teaching prompt",
"start teaching", "init teaching"

When any fires, respond with exactly this code block:

````
I'm restarting the River Rats teaching terminal.

Clone if not present:
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2

Working directory: ~/river-rats-teaching
Repo HEAD at handoff: 42d7f76
Role: teaching layer — L3 rendering, flag window, CONTENT_API,
observation-only discipline

Read these files in order before doing anything else:
1. ~/river-rats-teaching/CLAUDE.md (teaching-specific rules)
2. ~/river-rats-v2/CLAUDE.md (project-level)
3. ~/river-rats-v2/RELEASE_MANIFEST.yaml (integrated state v1.6)
4. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md
5. ~/river-rats-teaching/review/comms/TEACHING_STATUS_UPDATE_2026-04-21.md
6. ~/river-rats-v2/review/comms/MAIN_TERMINAL_DIRECTIVE_2026-04-18-v.md (locked recentering)
7. ~/.claude/projects/-home-rupert-river-rats-v2/memory/MEMORY.md

Current status: plan v2.1 SHIPPED across 11 commits. Path B +
recentering complete:
- Primary window range-first (range composition + villain_*_pct
  + board_favour)
- Flag window with 7 active flags + blocker placeholder (deferred)
- L3 prose cuts: hand_bucket, hero_position, draw_type_desc,
  showdown_value_desc, position_desc, forward_plan_desc (all
  removed; will restore for L1/L2 build)
- FlagEntry dataclass (kind/trigger_value/observation_text)
- CONTENT_API v3.0 published
- Guard-leak scanner expanded: directional framing (block/protect/
  charge/extract/deny + force/punish/drive/dominate) + WHY
  smugglers (make correct, safe to, justify, defensible)

End-state metrics: 0 V3 leaks across 3,080 sentences × 8 fields;
31 output fields; 2.16 mean flags/hand.

Deferred (awaiting signals):

1. Blocker 2-flag design (L4/L5). Gated on v2.4 oracle features
   shipping. Scope at
   ~/river-rats-v2/RELEASE_MANIFEST.yaml queued.teaching_blocker_
   flag_design. Requires GTO + V3 reviewer pass.

2. L1/L2 build. Gated on L3 playtest findings. Owner-paced per
   feedback_playtest_before_lower_levels.md.

3. river-outs-parenthetical backlog + plan-tag dedupe (cosmetic).

4. Any playtest findings flagged to teaching via hand-log system
   (has_teacher_feedback=True).

Teaching contract (apply always):
- Observation-only at L3. No WHY prose. No directional framing.
- Range-based thinking central.
- Feature data pipes through; teaching doesn't fabricate.
- Coherence guards OK (suppression); override guards NOT OK.
- Expand scanner when new violations surface, don't patch
  individual templates.
- Plan → expert review (GTO + V3) → small commits → hardening
  re-pass. Default discipline.
- Multi-agent review for load-bearing changes — don't ask.

Cross-stream awareness:
- Logic v2.4 Stage 3.5 in progress (5 MUSTs). When v2.4 ships,
  feature values shift; hardening re-pass recommended.
- Game on Path B output cleanly. CONTENT_API changes require
  coordination with game.

Orchestrator is cross-stream coordinator. Your work stable; no
active blockers.

Ping orchestrator when:
- Owner signals blocker flag design should start (v2.4 shipped)
- Playtest findings arrive (has_teacher_feedback=True)
- You surface a new hardening gap or violation category
- CONTENT_API version bump needed

Standing by.
````

---

### Game builder restart

**Owner trigger phrases:** "restart game", "game prompt", "start
game", "init game"

When any fires, respond with exactly this code block:

````
I'm restarting the River Rats game builder terminal.

Working directory: ~/river-rats-game (local only; NOT on GitHub —
do not attempt to clone)

Pull orchestrator + teaching repos for cross-stream state + adapter imports:
  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git ~/river-rats-teaching

Repo HEAD at handoff: 4fe1d41
Role: game prototype, real_oracle/real_teaching adapters, playtest
logging, UI

Read these files in order before doing anything else:
1. ~/river-rats-game/README.md (if exists)
2. ~/river-rats-v2/CLAUDE.md (project-level)
3. ~/river-rats-v2/RELEASE_MANIFEST.yaml (integrated state v1.6)
4. ~/river-rats-v2/review/restart/SESSION_STATE_2026-04-21.md
5. ~/river-rats-game/review/comms/GAME_TO_MAIN_TERMINAL_2026-04-21.md
6. ~/river-rats-v2/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-18-m.md (log essentials)
7. ~/river-rats-v2/review/comms/MAIN_TERMINAL_TO_GAME_2026-04-19-w.md (UI first cut)
8. ~/river-rats-game/playtest-logs/README.md

Current status: shipped and stable.

Live in prototype:
- Three-zone frame (table / coaching / hero controls)
- V1 range bar (horizontal stacked, 60×6px under villain chip,
  min-segment-width clamped)
- Badge A action-order inline prefix ("① CHECK ② CALL ③ RAISE")
- Hand vs range panel split (143993a)
- real_oracle adapter with SHAP (gated on for_position == hero)
- real_teaching adapter — Path-B-resilient (CONTENT_API v3.0)
- Playtest log schema v2 with full reproducibility: oracle_model_
  sha256, oracle_repo_commit, teaching_repo_commit, teaching_
  schema_version, game_build_commit, full feature vector per
  decision, SHAP per decision, ground_truth vs player_visible
  split, is_real_backend flag
- Hand-log system: Log button + teacher/logic feedback boxes +
  Save + Export + localStorage persistence
- Mock-backend warning banner
- 91/91 tests pass
- Real bundle generates clean
- Renders HU + 3-way

Running against:
- Oracle: v2.2 (v2_2_model_shipped.json)
- Teaching: l3_enriched_v3.0 schema

Deferred (owner-paced):
- Second cut: pot-odds chip on felt (mockup not started)
- Third cut: per-seat stack viz, street timeline
- Per-villain range bars in multiway (teaching-side scope)

Game contract (apply always):
- Game OWNS the felt (seats, chips, action tags, range bars,
  badges, pot, board, hero controls)
- Game DOES NOT own panel prose — teaching's domain
- All villain_*_pct data reads from teaching_output; DO NOT
  recompute at UI layer
- Playtest logs to ~/river-rats-game/playtest-logs/ (gitignored);
  schema bump = log_schema_version up
- No WHY in visuals any more than in prose
- Multi-agent review for load-bearing — don't ask, escalate
- Slow/quality, no rush

Orchestrator is cross-stream coordinator. Your work stable; no
cross-stream blockers.

Ping orchestrator when:
- Owner flags a playtest finding (summary + log file reference)
- You need direction on second cut
- Any adapter issue when v2.4 ships
- Any teaching schema mismatch surfaces

Standing by.
````

---

## Part 3 — Orchestrator's operational manual

### How to use this init file

1. Owner starts a new Claude session
2. Owner pastes the init prompt (Part 4 below) into the session
3. Session clones the v2 repo + reads this init file
4. Session becomes the orchestrator, loaded with all state
5. Owner can then restart other terminals one at a time by asking
   "restart logic builder" / "restart teaching" / "restart game"
6. Orchestrator replies with the appropriate restart prompt from
   Part 2 above, which owner copy-pastes into a fresh terminal

### Restart prompt serving discipline

When owner asks to restart another terminal:
- Copy the exact code block from Part 2 verbatim
- Do not modify, summarize, or abbreviate
- Do not add commentary above or below the code block except a
  single leading sentence ("Here's the logic builder restart
  prompt — paste into a fresh Claude Code session:")
- Preserve the exact HEAD commit SHAs, file paths, and MUST items

### If owner asks for status

After init, owner may ask "what's the status" or "what's next." Give
a brief chat-response (3-5 sentences) covering:
- What's in the deployed column
- What's blocking v2.4 ship (the 5 Stage 3.5 MUSTs)
- Whether any terminal has un-pulled directives waiting

### Maintenance

This init file should be updated when:
- Manifest version bumps
- A new MUST is added or resolved
- Any of the three builder terminals ships a milestone
- A new hard rule enters memory

Update discipline: bump the date in the header; update Part 1 state
sections; update Part 2 code blocks with new HEADs; commit with a
clear message. Owner's single-entry flow should always work without
needing to read anywhere else.

---

## Part 4 — The owner's paste prompt

This is the text owner copy-pastes into a fresh Claude session to
restart the orchestrator:

```
Restart the River Rats orchestrator from GitHub.

  git clone https://github.com/beytell1-sketch/river-rats-v2.git ~/river-rats-v2

Then read ~/river-rats-v2/review/restart/ORCHESTRATOR_INIT.md in full
and follow its instructions. This file contains the full restart
procedure, current state, memory priorities, and the restart prompts
for the other three terminals (logic / teaching / game).

When complete, confirm in 3-4 sentences what you've loaded and stand
by for direction.
```

That's the entire flow. One paste, one file, owner can restart all
four terminals from there.
