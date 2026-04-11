# Knowledge Base v1.3 — Required Changes from Solver Session

**Date:** 7 April 2026
**Sources:** Expert B1 (Ah3h), B2 (BD_Board6), B3 (BD_Board9), B4 (FB_Board4)
**Status:** REQUIREMENTS — awaiting owner review before implementation

---

## HIGH PRIORITY (affects labelling correctness)

### 1. Section 1.7 — Side equity: "Strongly preferred" → "Required (unless showdown value is low)"

**Source:** Expert B1 (Ah3h vs Kh6h)

Ah3h (nut FD + Ah blocker, no side equity) = CALL.
Kh6h (2nd nut FD + Kh blocker, no side equity) = RAISE.

The deciding factors are showdown value (Ah3h has more → prefers calling) and blocker direction (Ah blocks villain's folding range → reduces fold equity).

**Change:** Update conditions table row. Add Ah3h to "What does NOT qualify" list.

### 2. Section 1.7 — Ace blocker paradox for semi-bluffs

**Source:** Expert B1, B3

Holding the Ah on a heart draw board REDUCES fold equity (blocks villain's busted Ah-high hands that would fold). Kh raises more effectively than Ah because: (a) doesn't block folds, (b) less showdown value, prefers aggression.

**Change:** New subsection or boxed note in Section 1.7. Cross-reference from Example 9.

### 3. Section 1.7 — Non-set CALL default needs scoping

**Source:** Expert B2, B4

Current rule: "Only sets and the pure nuts are labelled RAISE." Too narrow.

Three exceptions found:
- **Blocker effect:** Kc9d two pair is 100% RAISE when Kc blocks club draws (BD_Board6)
- **River polarization:** All flushes raise on 4-flush board, even 5s4s (FB_Board4)
- **OESD+overcards:** KcJd raises without any flush draw or blocker (BD_Board9)

**Change:** Scope the rule to pre-river mixed-SPR spots. Add three carve-outs:
1. Non-set hands with dominant blocker effect (solver 70%+ raise)
2. River spots where hand is in the nut category for that board
3. OESD+overcard draws with high total equity (see #4)

### 4. Section 1.7 — OESD carve-out (non-flush combo draw raises)

**Source:** Expert B3

All KJ variants raise on Qh9h4dTc purely on OESD + overcard equity. No flush draw, no blocker. Current Section 1.7 only describes flush-draw-based semi-bluffs.

**Change:** Add second semi-bluff pathway: strong straight draws (OESD, 8+ outs) with overcards can raise without a blocker when combined equity is high enough (~50%+).

### 5. Section 1.7 — Sets don't always raise on flush-heavy boards

**Source:** Expert B3

9s9c (set) CALLS on Qh9h4dTc because flush-heavy board means villain's betting range has many flush draws with ~35% equity against the set.

**Change:** Caveat on the set=raise rule: sets call (not raise) on flush-heavy boards at low SPR where raising commits stacks against draws with live outs.

---

## MEDIUM PRIORITY (improves consistency)

### 6. Section 1.8 — Magnitude update: "40+" → "40 to 100+"

**Source:** Expert B2

BD_Board6 shows a full 0-100% raise swing based on suits alone. "40+" undersells the effect.

**Change:** Update magnitude language in Section 1.8 and DO NOT Rule #6. Cite Kc9d as anchor.

### 7. Section 1.8 — Ace blocker non-monotonic effect

**Source:** Expert B3

Ah can reduce fold equity by blocking villain's folding range. Blocker effects are not uniformly positive.

**Change:** Qualifying sentence in Section 1.8 about ace-rank blockers.

### 8. Section 1.8 — Secondary-suit blocker gap acknowledgment

**Source:** Expert B2 (analysis batch A)

flush_block_pct only tracks dominant suit. Kd9h's heart-blocking effect is invisible.

**Change:** Note that secondary-suit blocking is not captured by current features.

### 9. Example 5 — Contrast note vs KhJh

**Source:** Expert B3

Both are flush draw + straight draw OOP. Example 5 checks, KhJh raises. Primary distinction is nut-draw quality + blocker, not position.

**Change:** Add contrast note explaining the real decision driver.

### 10. New Example 10 — River raise polarization (FB_Board4)

**Source:** Expert B4

No existing worked example shows value raise / bluff raise / call simultaneously. FB_Board4 is the cleanest illustration.

**Change:** Add worked example with flush=raise, Ace-blocker=raise(bluff), two pair=call.

### 11. New Example 11 — Blocker-driven two pair raise (BD_Board6)

**Source:** Expert B2

No existing example shows a made non-set hand raising based on blocker effect. Kc9d vs Kh9d is the most counterintuitive solver finding.

**Change:** Add worked example contrasting Kc9d (RAISE) vs Kh9d (CALL).

### 12. Section 1.1 — Non-nut FD threshold clarification

**Source:** Expert B3

6h7h folds, 8h7h calls — one gutshot flips the decision. Currently implicit.

**Change:** Explicit note: non-nut FD alone folds 3-way OOP; non-nut FD + gutshot calls.

---

## LOW PRIORITY (nice to have)

### 13. DO NOT Rule #6 — Non-monotonic blocker qualifier

**Source:** Expert B3

Ace-rank blockers can have paradoxical effects.

### 14. Section 1.6 — SPR regime change at river

**Source:** Expert B4

SPR 0.33 on river = commit vs showdown decision, categorically different from earlier streets.

### 15. Section 1.7 title mismatch

**Source:** Expert B4

Section titled "Semi-Bluff Conditions" but contains the non-set CALL default for made hands.

---

## Proposed new features (from analysis agents)

| Feature | Effort | Impact | Unblocks |
|---------|--------|--------|----------|
| flush_draw_rank | Low | High | Kh6h/Ah3h training, BD_Board9 hands 1-2 |
| secondary_flush_block | Medium | Medium | Kd9h training, BD_Board6 hand 2 |
| ace_rank_blocker | Medium | Medium | Ad8c training, FB_Board4 hand 7 |
| combo_draw_strength | Low | Low | Cleaner OESD+FD representation (v10) |
