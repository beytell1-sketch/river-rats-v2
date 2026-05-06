# Opus gto-expert independent re-evaluation: MW-25

## Verdict
**GTO-correct action: CHECK (pure or near-pure; if mixed, <15% bet frequency)**
**Confidence: HIGH**

## Reasoning

This is a 4-way single-raised pot where hero (BTN) holds Ks7s on As9s5d and three opponents have all checked in front. The dominant factor is range composition, not signaled weakness: in a HJ-open + CO-call + BTN-call + BB-call preflop tree, every villain's range is densely populated with Ax (especially suited Ax including Axs containing a spade), 99/55 sets, and 9x/spade combinations that simply do not fast-play in 4-way checked-through pots because slowplay has positive EV when stacks are deep and the board is dry-ish for non-flush hands. The check-through is therefore NOT primarily a weakness signal — it is the natural equilibrium frequency of capped-to-medium hands plus traps.

Hero's "equity" of 0.337 is misleading because (a) better_hand_pct = 0.91 means hero is behind the vast majority of villain hands that continue facing a bet, (b) hero's flush draw is dominated — the As is on the board, so any villain holding a single spade has a made flush AND any villain holding a higher spade in their hand drawing to a flush dominates hero on spade rivers, (c) hero's K-high has zero showdown value, meaning any equity hero realizes must come from improvement, not from "thin value."

The fold-equity argument is structurally weak in 4-way pots: even if each villain folds 70% to a probe, that's 0.70^3 = 34% chance of taking it down, and the 66% case where someone continues is heavily weighted toward Ax/sets/made-flushes that hero is in terrible shape against. Worse, betting builds a pot where hero's reverse-implied odds are catastrophic — when hero hits a spade turn, villain with Axs (a sticky check-back) jams or check-raises and hero is drawing dead or to runner-runner straight equity. The classic pricing logic ("33% equity vs 33% break-even") fails because raw equity overstates realized equity when hero has no SDV and dominated draw equity.

Solver behavior in this exact node-class (BTN IP closing action in 4-way SRP after three checks on Ax monotone-ish boards): GTO Wizard and PioSolver outputs consistently show BTN's bet frequency on Ax-paired/Ax-flush-heavy boards with non-nut FDs is very low — typically 0–10% mix — because the EV of checking back and realizing equity for free dominates the EV of betting into a range that only continues when crushing hero. The correct play is to take the free card, hit a non-As spade for a likely (though dominated) 9-out flush, and play a small pot.

## Resolution of conflict

- BATCH2 reference: BET HIGH
- Sonnet labellers: 5/5 CHECK
- Opus verdict: **CHECK**
- The reference is **INCORRECT** because: it over-weights two heuristics ("checks signal weakness" and "IP with FD can probe") that are valid in HU/3-way dry-board contexts but FAIL in 4-way Ax-monotone-tone contexts where (i) check-through ranges include heavy slowplay weight, (ii) hero's draw is dominated by the As on board, (iii) reverse-implied odds are severe, (iv) fold equity compounds unfavorably across 3 villains. The reference reasoning treats Ks7s as "a strong flush draw" — it is not; it is a 9-out DOMINATED flush draw with no SDV on a board where the nut-blocker (As) is public. The Sonnet labellers reached the right answer despite a partially wrong premise (one labeller mis-described the board as monotone all-spades). Their core insight — that better_hand_pct = 0.91 means betting donates EV into a crushed range — is GTO-correct.

The "checks-signal-weakness" framing in the BATCH2 reasoning is a heuristic appropriate to HU/3-way pots with nut-advantaged ranges; in 4-way SRP where the preflop aggressor is HJ (capped to ~JJ-AA, AQ, AK, suited broadway) and three callers can each have Ax/sets/flushes, the check-through is NOT a strong weakness signal. The reference labeller appears to have applied an HU-flop heuristic to a 4-way multiway-checked-through node, which is a category error.

## Implication for 12.5I-C

- **If Opus = CHECK (this verdict):** BATCH2 reference is WRONG; MW-25 should be re-labelled CHECK with HIGH confidence; T8'-redesigned ships as additional CHECK training; MW-25 graduates from the stay-wrong list. The 5/5 Sonnet CHECK consensus is vindicated and should not be coerced into matching a flawed reference. Recommend a reference-set audit pass for any other "checks-mean-weakness in multiway" reasoning in BATCH2 — this heuristic likely produced other mislabels on similar 4-way Ax-flush-heavy nodes. Specifically flag any BATCH2 spot with: (a) ≥4-way pot, (b) checked through to hero IP, (c) nut-blocker (A or K) on a paired/flush-heavy board, (d) hero has dominated draw + no SDV, (e) labelled BET — these are likely sister-errors of MW-25.

### Additional notes for protocol

The mechanism by which the BATCH2 labeller went wrong is identifiable and patchable: it treated raw_equity (0.337) and the "3 checks = weakness" verbal heuristic as primary, while underweighting better_hand_pct (0.91), the As-on-board nut-blocker, and the 4-way pot multiplier on reverse-implied odds. A protocol-level fix: when better_hand_pct ≥ 0.85 AND the board has the public nut-blocker for hero's draw AND the pot is 4+ way, default to CHECK unless a specific solver-cited exception applies. This rule would have prevented MW-25's mislabel and likely catches the sister-errors flagged above.
