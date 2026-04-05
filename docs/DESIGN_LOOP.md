# River Rats — Optimal Design Loop

## The Problem With the Old Loop

```
Claude Web (consultant) writes coordinator brief
    ↓
You copy brief into Claude Code terminal
    ↓
Coordinator reads brief, delegates to tmux agents
    ↓
Agents produce output files
    ↓
You copy output back to Claude Web for review
    ↓
Claude Web reviews, writes another brief
    ↓
You copy that back into Claude Code
    ↓
Repeat...
```

**Why this breaks down:**
- You are the message bus. Every handoff loses context.
- Claude Web never sees the actual code — only what you paste.
- The coordinator brief format is rigid and burns tokens restating
  things the agents already know.
- 583 lines of protocols exceed reliable instruction following (~150-200
  instructions is the ceiling for frontier models).
- Each anti-pattern patch added instructions, making the problem worse.

---

## The New Loop

### Two modes of operation. Pick the right one per task.

---

### MODE A: Planning & Architecture (Claude Web)

Use Claude Web when you need to THINK — not build.

```
You describe what needs to happen
    ↓
Claude Web interviews you (gaps, edge cases, tradeoffs)
    ↓
Together you produce a SPEC.md file
    ↓
You save SPEC.md into the project repo
    ↓
Done. Close the Claude Web session.
```

**Claude Web's job in Mode A:**
- Challenge your assumptions
- Catch structural gaps before building starts
- Produce a spec with: objective, constraints, acceptance criteria,
  risk flags
- NOT coordinator briefs. NOT role assignments. NOT implementation
  detail.

**The spec is a CONTRACT, not a screenplay.** It says WHAT must be true
when the work is done. It does NOT say which agent does what — that's
Claude Code's job now.

**Why this works better:** Claude Web operates in a completely separate
context window. It hasn't been primed with 500 lines of protocol docs.
It thinks fresh. That's the independent review value you noticed — and
it's real. But you get that value at the PLANNING stage, not as a
review bottleneck during implementation.

---

### MODE B: Execution (Claude Code with agents)

Use Claude Code when you need to BUILD.

```
Start a fresh Claude Code session
    ↓
Point it at SPEC.md: "Read docs/SPEC.md and implement it"
    ↓
Claude Code reads CLAUDE.md (slim — project context only)
    ↓
Claude Code decomposes the spec into tasks
    ↓
Claude Code delegates to subagents or agent teams
    ↓
Built-in reviewer agent checks each deliverable
    ↓
Tests run. Output goes to river-rats-core/ if passing.
    ↓
Done. Session ends clean.
```

**Claude Code's job in Mode B:**
- Decompose the spec into buildable chunks
- Delegate to the right specialist agent (defined in .claude/agents/)
- Enforce test-first and blueprint-before-build via CLAUDE.md
- Run the reviewer agent after each deliverable
- Report results

**You intervene when:**
- A stop condition fires (agent reports BLOCKED)
- The reviewer agent flags a BLOCKER
- Tests fail after implementation
- You want to course-correct mid-build

**You do NOT need to:**
- Write coordinator briefs
- Manually assign roles
- Copy text between Claude Web and Claude Code
- Manage tmux panes yourself (agent teams handle this)

---

### MODE C: Independent Review (Claude Web — post-build)

Use Claude Web AFTER a build session to audit results.

```
Build session completes. Tests pass.
    ↓
You open Claude Web with the changed files attached
    ↓
"Review these changes against SPEC.md. Flag anything
 that technically passes tests but misses the intent."
    ↓
Claude Web reviews with fresh eyes (no implementation bias)
    ↓
If issues found → new SPEC.md addendum → back to Mode B
If clean → ship it
```

**This is where Claude Web's independent context shines.** It didn't
watch the implementation happen. It doesn't have sunk-cost bias on the
approach taken. It reads the spec and the output cold.

**But it happens AFTER the build, not during.** This is the key change.
You're not relaying messages mid-build — you're doing a final quality
gate.

---

## When to use which mode

| Situation | Mode |
|-----------|------|
| "I need to figure out what to build" | A (Claude Web) |
| "I know what to build, let's go" | B (Claude Code) |
| "It's built, does it actually match the intent?" | C (Claude Web) |
| "Something went wrong mid-build" | Stay in B — use stop conditions |
| "I'm not sure if the approach is right" | A first, then B |
| "Quick bug fix, I know exactly what's wrong" | B only |
| "Major architecture change" | A → B → C |

---

## The Spec File Format

Keep it short. The spec is for Claude Code to act on, not for humans
to admire.

```markdown
# SPEC: [Feature/Fix Name]

## Objective
One sentence. What must be true when this is done.

## Context
What exists now. What's broken or missing. 2-3 sentences max.

## Requirements
- [Requirement 1 — testable assertion]
- [Requirement 2 — testable assertion]
- [Requirement 3 — testable assertion]

## Constraints
- [Things that must NOT change]
- [Performance bounds if relevant]
- [Files that are off-limits]

## Acceptance Criteria
- [ ] [Test that proves requirement 1]
- [ ] [Test that proves requirement 2]
- [ ] All existing tests still pass
- [ ] No regressions in [specific area]

## Risks
- [What could go wrong]
- [What to watch for]

## Notes
[Anything Claude Code needs to know that doesn't fit above]
```

---

## What Stays the Same

Your good instincts are preserved:

- **Independent review from separate context** → Mode C
- **Test-first** → enforced in CLAUDE.md
- **Blueprint before build** → architect agent produces blueprint
  before programmer agent executes
- **Stop conditions** → in CLAUDE.md, agents report BLOCKED
- **Anti-patterns awareness** → condensed into CLAUDE.md gotchas
- **No improvising** → agents have scoped tools, can't go off-piste
- **river-rats-core/ as clean folder** → enforced in CLAUDE.md

## What Changes

- **No more coordinator briefs** → Claude Code decomposes specs itself
- **No more manual role assignment** → agents are defined in files
- **No more copying between Claude Web and terminal** → specs live in
  the repo, both can read them
- **No more 583-line protocol doc** → slim CLAUDE.md + focused agent
  files
- **No more you-as-message-bus** → agent teams communicate peer-to-peer
