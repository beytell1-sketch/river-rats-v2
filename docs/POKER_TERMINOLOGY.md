# Poker Action Terminology — Reference Dictionary

## Preflop Actions

| Term | Definition | Example |
|------|-----------|---------|
| **Post** | Forced contribution before cards are dealt. NOT a bet. | SB posts 0.5bb, BB posts 1bb |
| **Bet** | First voluntary aggressive action. No prior bet to increase. | CO opens to 2.5bb = CO bets |
| **Call** | Matching an existing bet. | BTN calls CO's 2.5bb bet |
| **Raise** | Increasing over an existing voluntary bet. | CO bets 2.5bb, BTN makes it 7bb = BTN raises |
| **Check** | Declining to act when no bet faces you. | BB checks option in a limped pot |
| **Fold** | Surrendering your hand. | UTG folds preflop |

## Preflop Pot Types

| Pot type | What happened | Range implication |
|----------|--------------|-------------------|
| **Limped pot** | No one bet. Posts, calls, checks only. | Wide ranges for everyone |
| **Opened/standard pot** | Someone bet (opened). Others called. | Bettor has narrowed range |
| **Raised pot (3-bet)** | Someone raised over the open bet. | Raiser has very narrow range |

## Key Distinctions

- **Blinds are posts, not bets.** The BB posting 1bb is not a bet.
- **Opening is betting, not raising.** CO opening to 2.5bb is a bet — there is no prior voluntary bet to raise over.
- **Raising requires a prior bet.** Only when someone increases over a voluntary bet is it a raise.

## Postflop Actions

| Term | Definition | Example |
|------|-----------|---------|
| **Bet** | First aggressive action on a street. | Flop checks to CO, CO bets 33% pot |
| **Call** | Matching an existing bet. | CO bets, BTN calls |
| **Raise** | Increasing over an existing bet. | CO bets, BTN raises |
| **Check** | Declining to bet when no bet faces you. | BB checks flop |
| **Check-raise** | Checking, then raising after someone bets. | BB checks, CO bets, BB raises |

## Feature Mapping

| Feature name | What it encodes |
|-------------|----------------|
| `is_3bet_pot` | Was there a RAISE over the preflop open bet? |
| `had_preflop_open` | Was there a preflop bet (open) at all? 0 = limped pot |
