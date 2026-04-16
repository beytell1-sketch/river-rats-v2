# Startup Prompt — Game Design / Builder Terminal

Copy the block below into a fresh Claude Code session as the
first message.

---

```
I'm starting the River Rats game design terminal. This is a new
work stream in parallel with two others:

- Logic/oracle work: github.com/beytell1-sketch/river-rats-v2
- Teaching work: github.com/beytell1-sketch/river-rats-teaching

Both are mid-flight. You are not replacing or merging with them.
Your job is to define the USER-FACING PRODUCT — the coaching
app shape, session architecture, level progression, feedback
model, platform constraints. The logic layer produces oracle
actions + features; the teaching layer renders feature-driven
teaching text at levels L1–L3. You are the layer that turns
those outputs into a coherent product a human actually uses.

STEP 1 — Clone both sibling repos for read-only context:

  git clone https://github.com/beytell1-sketch/river-rats-v2.git \
    ~/river-rats-v2
  git clone https://github.com/beytell1-sketch/river-rats-teaching.git \
    ~/river-rats-teaching

Clone destination for this terminal's work:

  mkdir -p ~/river-rats-game

(Whether to make this a git repo now or later is deferred to
the first plan gate — see Phase A.)

STEP 2 — Read these files in order. Do NOT write anything yet.

FROM v2 CORE (~/river-rats-v2/):

1. CLAUDE.md — project conventions, protocols, anti-patterns
2. review/comms/SESSION_STATE_2026-04-15.md — where v2 is
3. review/comms/PLAN_CONSOLIDATED_2026-04-15.md — current v2.3
   plan (logic layer)
4. review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md — the
   phased work that produces the next oracle

FROM TEACHING (~/river-rats-teaching/):

5. CLAUDE.md — teaching repo conventions
6. review/comms/PHASE2_BASELINE_REPORT_2026-04-15.md — what L3
   output looked like before fixes
7. review/comms/PHASE2_RESCORE_2026-04-16.md — what shipped at
   Tier A
8. review/comms/DIRECTIVE_L3_HARDENING_BEFORE_PHASE3_2026-04-16.md
   — why L3 must be rock-solid before L2/L1 build, and what
   "fully happy" means
9. review/phase2/sample/ — 25 hands actually rendered at L3.
   Browse the HTML output. THIS is what the teaching layer
   produces for your product to consume.

FROM MAIN TERMINAL MEMORY (if accessible):

~/.claude/projects/-home-rupert-river-rats-v2/memory/

- user_teaching_philosophy.md — NON-NEGOTIABLE product
  constraints: highlight context (don't explain why),
  features-only (no custom per-hand text, no authored lesson
  content), range-based thinking central, level-gated
  simplification
- user_owner_style.md — slow / deliberate / quality-focused
- feedback_recommend_dont_defer.md — when you have enough to
  make a call, make it; don't push menus back
- feedback_l3_is_core_gate_lower_levels.md — L3 is the core
  substrate; anything weak at L3 gets inherited and amplified

If the memory dir isn't accessible, the four files above are
summarised in the handoff-safe form further down this prompt.

STEP 3 — Orient. Produce a short "understanding" doc at
~/river-rats-game/review/comms/UNDERSTANDING_2026-04-17.md
covering:

- What the oracle actually outputs (action, confidence,
  feature vector, teaching text at each level)
- What you think the product is (in 3-4 sentences)
- What you think the core user loop is (in a paragraph)
- What you don't yet understand

Submit for main-terminal review. Do not proceed to Phase B
(planning) until the understanding pass is acknowledged.

STEP 4 — Follow the phased plan below. Do NOT jump phases.

---

## Slow-start phase plan

### Phase A — Orient (read + write an understanding doc)

- Read the context files above
- Write UNDERSTANDING_2026-04-17.md
- Submit for main-terminal review
- Iterate until acknowledged
- **No code, no design artefacts, no mockups yet**

Gate out: main terminal confirms the understanding matches
project reality.

### Phase B — Plan v0 (product shape)

Produce PLAN_PRODUCT_SHAPE_2026-04-17.md covering:

1. Product vision + goals (who the user is, what outcome
   they want, why this product vs alternatives)
2. User journey (onboarding → first session → return →
   long-horizon progression)
3. Session architecture — end-to-end flow of a coaching
   session: hand enters system → oracle produces output →
   teaching layer renders at level L → product surfaces to
   user → user acts → next
4. Level progression model — when and how does a user move
   L1 → L2 → L3? Time? Assessed skill? User choice?
5. Feedback model — how level-appropriate teaching output
   becomes product UX. Cards, narrative, drill-down, history?
6. Platform constraints — mobile (iOS first? both?),
   inference latency budget, offline behaviour, session
   length target
7. Open questions (things genuinely undecided, flagged for
   owner input)

Submit for owner review. Iterate.

**Hard constraint:** no visual design in Phase B. No screen
mockups. No colour, typography, animation specs. Product
shape only. Those are Phase D.

Gate out: owner signs off on product shape.

### Phase C — Plan v1 (interface contract)

Now that product shape is locked, specify the interface
between the three layers:

- What does the game layer consume from the teaching layer?
  Structured JSON? Pre-rendered HTML panels? Raw feature
  vector + render-client-side?
- What does the game layer consume from the oracle layer
  directly (if anything)?
- What does the game layer produce back upstream? Analytics?
  Feature-attention signals? Nothing?

Produce PLAN_INTERFACE_CONTRACT_2026-04-17.md.

Submit for review. Main terminal verifies this is consistent
with what the teaching and oracle layers actually produce.
Logic- or teaching-side changes required by the contract get
flagged as dependencies, not blockers.

Gate out: interface contract approved and consistent with
upstream layers.

### Phase D — Plan v2 (experience design)

NOW visual / interaction design is in scope. Wireframes, UX
flow diagrams, screen composition, information density
studies. Still not code. Still plan.

Decide:
- Screen-level layout for a coaching session
- How L3 teaching text actually lays out (panel system, card
  stack, hand-history drawer, etc.)
- How level progression surfaces in the UI
- Onboarding flow specifics

Produce PLAN_EXPERIENCE_DESIGN_2026-04-17.md.

Submit for owner review.

Gate out: experience design approved.

### Phase E — Prototype scope

Choose ONE slice to prototype first. Candidates:
- Single-hand coaching loop at L3 (most informative; uses
  already-shipped teaching output)
- Level progression assessment (exercises the level-gating
  model but needs L2 renderer to be useful)
- Onboarding flow (exercises first-session UX but not core
  coaching)

Recommend one. Specify success criteria. Specify what the
prototype does NOT do (explicit non-goals).

Produce PLAN_PROTOTYPE_SCOPE_2026-04-17.md.

Submit for approval.

Gate out: scope locked + owner approves.

### Phase F — Prototype build

Finally. Plan-before-build applies at each sub-step.
Test-first. Commit and push per step.

---

## Non-negotiable product constraints (from memory)

These govern every decision. If you find yourself designing
something that conflicts with these, STOP and flag.

1. **Teaching output highlights context; it does not explain
   why.** Good: "You're near the top of your range; villain
   checked back capped." Bad: "BET because you're ahead and
   villain is weak." Product UX must not re-introduce causal
   explanation framing on top of teaching output.

2. **Features-only scalability.** The teaching layer produces
   text derived entirely from the feature vector. No bespoke
   per-hand prose anywhere in the stack. Product UX must not
   introduce hand-specific authored content, templated lesson
   plans, or narrative shells that break scalability. If a
   panel cannot produce useful output from features, the
   correct answer is "say less" — drop the panel.

3. **Range-based thinking is central.** Where hero sits in
   their range, villain's range shape, relative strength —
   these are the substrate at every level. Product UX must
   surface range framing in some form (numeric at L3,
   qualitative at L2, plain-language at L1).

4. **Level-gated complexity.** L3 vocabulary must not leak
   to L1. L2 vocabulary must not leak to L1. L1 surfaces
   perception cues that L3 takes for granted. Product UX
   must respect level gating — a single user at L1 does not
   see L3 terminology even if it appears correct.

5. **Slow and deliberate quality.** Every phase gate is real.
   Don't jump ahead. Don't compress planning. Time taken on
   getting the shape right now saves enormous time on rework
   later.

## Protocols (inherited from v2 + teaching CLAUDE.md)

- Plan before build at every gate
- Test-first when implementation starts
- Stop and report on any unexpected result; do not improvise
- Commit per deliverable, push immediately
- No destructive actions without explicit ask
- Write reviews / plans / directives to review/comms/
- Owner doesn't read long reports — summarise in chat after
  pushing

## Coordination model

- You cannot talk to the logic terminal or the teaching
  terminal directly. They are separate machines.
- Main terminal (the reviewer/orchestrator) reads across all
  three repos and coordinates. If you need something from
  upstream, file a comm in ~/river-rats-game/review/comms/
  and flag it. Main terminal surfaces it to the relevant
  builder.
- Owner is available for gate reviews and scope calls but
  otherwise runs on a slow/quality cadence. Don't assume
  rapid turnaround.

## Out of scope for this terminal

- Training / retraining models
- Labelling hands
- Writing teaching templates or renderer code
- Modifying the logic or teaching repos
- Solver work
- Gate 7 / v2.3 ship decisions

If you find yourself wanting to do any of the above, you are
out of scope. File a note for main terminal and stop.

---

**First action: Phase A. Clone the repos, read the context,
write UNDERSTANDING_2026-04-17.md, submit for review. Do
nothing else.**
```
