# Process Guide — River Rats Development

**Purpose:** Operating manual for how Claude Code terminals should work
on this project. Read before starting any task. Also serves as the
review checklist — the reviewer terminal uses these rules to verify
the working terminal followed protocol, and makes recommendations
based on findings.

**Who reads this:**
- Working terminal: follow these rules
- Reviewer terminal: check these rules were followed, recommend fixes

---

## 1. Resource Allocation

### 1.1 Agent batch sizes
- **GTO labelling agents:** ≤ 10 hands per agent. Never more.
  Smaller batches = deeper reasoning per hand.
- **GTO review agents:** ≤ 15 hands per reviewer.
- **Research agents:** 1 topic per agent. Never combine "research
  semi-bluffs AND blockers" in one agent. Split them.
- **Design agents:** 1 category per agent (e.g., "flush-blocking
  boards" is one agent, "overcard boards" is another).

### 1.2 Minimum agent counts
- Any expert task with > 10 items: MUST use multiple agents.
- Any labelling round: labellers + independent reviewers.
  Reviewer count ≥ labeller count ÷ 2.
- Any design task: ≥ 2 design agents + 1 independent reviewer.
- Any research task: ≥ 2 research agents (different angles) +
  1 independent reviewer.

### 1.3 Parallelism
- Launch independent agents in parallel, not sequentially.
- If you're dispatching 10+ agents, send them all in one message.
- Don't wait for batch 1 results before dispatching batch 2
  unless batch 2 depends on batch 1 output.

### 1.4 The stinginess trap
- When in doubt, use MORE agents, not fewer.
- The cost of too many agents is near-zero (some redundancy).
- The cost of too few is quality degradation, context overload,
  and missed errors.
- If you catch yourself thinking "one agent can handle this" for
  any task involving > 10 items of expert judgment, stop and split.

**Reviewer check:** Count the agents dispatched. If any expert task
used fewer than the minimums above, flag it. Recommend re-doing
with proper allocation.

---

## 2. Quality Gates

### 2.1 Calibration before labelling
- MANDATORY before every labelling round.
- Must use the BLIND exam: agent sees situations without answers.
- Must be GRADED against the answer key by a separate process.
- Agent must NOT have access to calibration_exam.py, answer keys,
  or any file containing expected answers.
- Gate: 20/24 minimum + all 3 GTO-reversal hands correct.
- If knowledge base checksum changed since last calibration,
  re-calibrate. No exceptions.

### 2.2 Leakage check before training
- Compare ALL training situations against the reference set.
- Check: exact match on (hero_cards, board, position, street).
- Check: board-only overlap (same board, different hands).
- Check: feature-space nearest neighbor (distance < 0.1 = flag).
- ANY exact match = remove from training data.
- Report all overlaps for review.

### 2.3 Feature importance after training
- Check every new feature's importance.
- Below 1% = drop the feature and note why.
- Top feature > 30% = investigate for overfitting.
- Compare before/after CV log-loss (same folds, fixed seed).

### 2.4 Reference gate after training
- Run the reference set evaluation.
- All baselines (v8, previous best) must be in the SAME session.
- Apply solver corrections (see memory/reference_corrections.md).
- Report raw score AND solver-corrected score.
- No regression below previous best on any axis.

### 2.5 Independent review before building
- Every design doc must be reviewed by an independent agent
  before any code is written.
- The reviewer must NOT have seen the design process.
- Card conflicts, board overlaps, hand classification errors,
  coverage gaps — all must be checked.

**Reviewer check:** For each gate, verify it was actually run (not
just claimed). Look for evidence: scores, file outputs, comparison
numbers. "Calibration passed" without a graded score = not verified.
Recommend re-running any gate that lacks evidence.

---

## 3. Research Protocol

### 3.1 When to research
- Before designing ANY new training situations.
- Before adding ANY new feature.
- Before updating the knowledge base.
- When the solver shows something unexpected.

### 3.2 Research standards
- Minimum 8 distinct sources per topic.
- Sources must be named with URLs (not "various sources").
- Prefer: GTO Wizard, Upswing, Galfond, PioSolver, academic papers.
- Reject: pre-2018 forum posts, fixed-limit content applied to
  no-limit, HU-specific content applied to multiway.
- Each finding must state: source, specific data point, implication.

### 3.3 Research review
- Research must be independently reviewed before informing design.
- Reviewer checks: source quality, cross-file contradictions,
  contradictions with knowledge base, unsourced claims.
- Research is NOT used directly as training labels — it informs
  factory design, the GTO Expert labels independently.

**Reviewer check:** Was research done before design? Were sources
cited? Was the research reviewed? If any design doc references
facts without research backing, flag it. Recommend research before
proceeding.

---

## 4. Presentation Protocol

### 4.1 Present for review, don't decide
- Working terminal presents findings to the review folder.
- Working terminal does NOT make decisions based on findings.
- Format: what was found, what it means, options, trade-offs.
- The reviewer (or owner) decides.

### 4.2 Review folder discipline
- All deliverables go to `review/` first.
- Each review document states: what was done, findings, concerns,
  open questions.
- Files move to production only after explicit approval.

### 4.3 Solver data
- Every solver session must be logged with:
  - Exact board, exact hero hand, exact action sequence
  - Solver output (frequencies per action, per suit if relevant)
  - Interpretation and implications
- Solver data goes to `review/SOLVER_VERIFIED_*.md` files.
- Solver findings that change the knowledge base go to
  `memory/feedback_solver_findings.md`.

### 4.4 Progress reporting
- At each phase boundary, present a summary table.
- Include: what was done, what passed, what failed, what's next.
- Don't bury failures in long text — table format, clear pass/fail.

**Reviewer check:** Were findings presented before actions taken?
Were decisions made by the working terminal that should have been
presented for review? Flag any instance of "decided and built"
without a review step. Recommend adding a review checkpoint.

---

## 5. Poker-Specific Protocols

### 5.1 Vocabulary
- **Post:** blinds are posted, not bet
- **Bet:** first aggressive action (opening)
- **Raise:** increasing over an existing bet
- **Check:** declining to act when no bet faces you
- Reference: `docs/POKER_TERMINOLOGY.md`
- Verify labels match context: RAISE requires facing_bet=True,
  BET requires facing_bet=False.

### 5.2 Solver verification triggers
- Any RAISE label on a non-set/non-nut hand → verify
- Any FOLD label with equity > pot_odds + 5pp → verify
- Any label where labeller and reviewer disagree at HIGH
  confidence → flag for solver
- All solver results logged permanently

### 5.3 Knowledge base updates
- Require solver evidence (not just expert opinion)
- Require independent review of the changes
- Checksum must be updated in pipeline doc
- Re-calibration mandatory after any KB change

### 5.4 Factory situation design
- No predicted labels in design docs — Expert labels fresh
- Bettor goes LAST in villain_positions list
- Check for card conflicts (hero card on board)
- Check for leakage against reference set
- Verify facing_bet matches action history

**Reviewer check:** Was terminology used correctly throughout?
Were solver verification triggers respected? Were any labels
accepted without verification that should have been verified?
Recommend verification for any flagged labels.

---

## 6. Common Mistakes (Learned From Experience)

These are traps this project has fallen into. Watch for them.

| Mistake | What happens | How to catch it |
|---------|-------------|-----------------|
| Stingy agent allocation | One agent handles 50+ hands, quality drops | Count agents vs items |
| Self-reviewing | Agent reviews its own output, finds nothing wrong | Check if reviewer is independent |
| Running before review | Code built and run before design was reviewed | Check timeline: review before build? |
| Trusting calibration transcript | Agent "passed" but wasn't graded against key | Is there a graded score with evidence? |
| Vocabulary mismatch | RAISE used for opening bets, inflates features | Assert facing_bet matches action |
| Warm-start assumption | Warm-start from different domain hurts | Check if base model domain matches |
| Leakage from reference set | Factory designs unconsciously copy reference boards | Run leakage check, compare boards |
| Feature addition without data consistency check | Changing existing features breaks trained models | Verify old features unchanged |
| Unit confusion | Deals vs games vs situations | Write out unit conversion explicitly |
| Targeting individual failures | Overfits to reference set | Train general principles, not patches |
| Solver output as direct training label | Model features may not capture what solver exploits | Expert review of feature compatibility |

**Reviewer check:** Scan for any of these patterns in the session.
Flag with specific evidence. Recommend corrective action.

---

## 7. Reviewer Recommendations

After reviewing a working terminal's session, the reviewer produces:

### 7.1 Protocol compliance report
| Rule | Followed? | Evidence | Recommendation |
|------|-----------|----------|----------------|
| (each rule from sections 1-6) | Yes/No | (specific reference) | (if No, what to do) |

### 7.2 Quality assessment
- What went well (specific examples)
- What was missed (specific gaps)
- What should change next session

### 7.3 Recommendations for next session
- Priority-ordered list of actions
- Process improvements to carry forward
- Unresolved questions that need attention

The reviewer writes this to `review/SESSION_REVIEW_[date].md`
and presents it to the owner.

---

## Quick Reference — When In Doubt

| Situation | Do this |
|-----------|---------|
| Task has > 10 expert items | Split across multiple agents |
| Design is ready | Get independent review first |
| About to label | Run calibration exam first |
| About to train | Run leakage check first |
| Solver showed something new | Log it, don't act on it yet |
| Agent says "I can handle this alone" | Split it anyway |
| Feature importance looks wrong | Check for data issues first |
| Two experts disagree | Present both, don't pick a winner |
| Not sure if research is needed | It's needed. Do the research. |
| Reviewer says "looks fine" | Push back — find something specific |
