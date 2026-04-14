---
date: 2026-04-14
from: Owner (Rupert)
to: Builder team
re: Pilot Gate decisions + Approach C amendment + rerun pilot
status: DIRECTIVE — incorporate and rerun
---

# Pilot Gate: Decisions + Amendment

## Decisions from Pilot Report

### 1. Feature attention approach: Approach C (amended)

Approach C (action-dependent auto-tags) with the amendment
described below in Section 2.

Rationale for C over B: Approach B missed `villain_medium_made_pct`
70% of the time and `villain_draw_pct` 80% of the time. These are
features we specifically promoted because they were missing from
the old pipeline. If agents naturally skip them, the feature
attention data for thin value and protection decisions has a blind
spot. C's action-dependent defaults ensure composition features
are always considered.

### 2. 6-team structure: CONFIRMED

19/20 unanimous with 1 legitimate dissent. Calibration cross-check
4/4 corrected. The structure works.

### 3. 10-hand batch size: CONFIRMED

No quality drift observed.

### 4. Proceed to Pass 1: APPROVED — after pilot rerun

Rerun the pilot with Approach C amended (below) to verify the
amendment works. If the rerun confirms, proceed to Pass 1
immediately without another gate.

---

## Amendment to Approach C: CONFIRMED tier + mandatory composition

### The problem

The pilot showed agents don't tag range composition features as
PRIMARY when those features confirm rather than change the
decision. A monster betting on a dry board where `villain_draw_pct`
is 3% — the agent doesn't tag it because the 3% didn't drive
the bet. But the agent DID look at it. If it were 35%, the
decision might be different (bet for protection, not value, or
check).

This matters because:
1. Range thinking is the core of GTO. A solver evaluates the
   full range for every action. Agents should too.
2. The teaching oracle needs to know which range features the
   expert verified, not just which ones drove the action.
3. "Confirmed it doesn't change the decision" IS part of the
   reasoning — it's a negative finding that strengthened the
   choice.

### The amendment: add CONFIRMED tier

Two attention levels:

| Level | Definition | When to use |
|---|---|---|
| **PRIMARY** | Without this feature's value, the action might change. | The feature drove the decision. |
| **CONFIRMED** | Checked this feature, its current value supports the action. If it were very different, the action might change. | The feature was verified as part of range reasoning. Its value aligns with the chosen action. |

**CONFIRMED is NOT "not relevant."** CONFIRMED means: "I looked
at this, it matters in general, its current value supports what
I'm doing, and I'm noting that I checked it." This is the
difference between a solver (evaluates everything) and a heuristic
player (only looks at what seems important).

### Mandatory composition for BET/RAISE

For BET and RAISE actions, the agent MUST tag all 4 villain
composition features as either PRIMARY or CONFIRMED:

- `villain_top_pair_plus_pct`
- `villain_medium_made_pct`
- `villain_draw_pct`
- `villain_air_pct`

**Prompt language:**

```
For BET and RAISE actions: you MUST tag all 4 villain
composition features (villain_top_pair_plus_pct,
villain_medium_made_pct, villain_draw_pct, villain_air_pct)
as either PRIMARY or CONFIRMED.

PRIMARY: this feature's value drove your decision to bet/raise.
CONFIRMED: you checked this feature, its value supports your
decision. If it were very different, your action might change.

You are betting INTO this range. You must know what it contains.
```

For CHECK, CALL, FOLD: no mandatory tags. Tag what drove the
decision organically. These are responsive actions where the
specific tipping-point feature matters more than the full
composition.

### Updated output example (BET)

```json
{
  "action": "BET",
  "feature_attention": {
    "equity_vs_range": "PRIMARY",
    "villain_top_pair_plus_pct": "PRIMARY",
    "hero_range_percentile": "PRIMARY",
    "villain_air_pct": "CONFIRMED",
    "villain_medium_made_pct": "CONFIRMED",
    "villain_draw_pct": "CONFIRMED",
    "is_ip": "CONFIRMED"
  }
}
```

This tells the teaching oracle: "equity, villain strength, and
hero's range position drove the bet. Villain air, medium made,
draws, and position were all verified and support the decision."

### Updated output example (CALL)

```json
{
  "action": "CALL",
  "feature_attention": {
    "draw_outs": "PRIMARY",
    "pot_odds": "PRIMARY",
    "equity_vs_range": "PRIMARY"
  }
}
```

No mandatory composition for CALL. The agent tagged what drove
the call. Organic and clean.

### Approach C defaults updated

For BET/RAISE, the Tier 1 defaults now include all 4 composition
features as pre-tagged CONFIRMED (agent can upgrade to PRIMARY
or remove with justification if truly irrelevant — but removal
of a composition feature on a BET/RAISE requires explicit
justification: "villain_draw_pct removed because this is a
river hand and draws are dead").

For CALL/FOLD/CHECK, defaults unchanged from the original
Approach C.

---

## Pilot Rerun

Rerun the pilot with these changes:

1. **All 6 teams use Approach C (amended)** — no more A/B/C
   comparison. The approach is decided.
2. **Same 20 hands** as the original pilot.
3. **Same 6-team structure** (different random orders per team).
4. **New agents** — do NOT reuse pilot 1 agents. Fresh agents
   with no knowledge of prior pilot results.

### What the rerun tests

- Does the CONFIRMED tier produce useful data or just noise?
- Does mandatory composition for BET/RAISE change any labels?
  (It shouldn't — it changes metadata, not actions.)
- Is the removal burden acceptable when agents must justify
  removing composition features?
- Does feature attention Jaccard improve with the structured
  approach?

### Rerun evaluation

| Metric | Target |
|---|---|
| Action agreement | Still ≥ 95% (no regression from pilot 1) |
| Feature Jaccard (within teams) | Higher than pilot 1 Approach C |
| Composition coverage on BET/RAISE | 100% (all 4 tagged) |
| CONFIRMED tags per hand | 2-4 on average |
| Removal justifications | Substantive, not perfunctory |
| No new action disagreements introduced | Labels should match pilot 1 |

### If rerun confirms

Proceed directly to Pass 1 production labelling. No additional
gate — the rerun IS the final validation.

### If rerun shows problems

- CONFIRMED tier is noisy (agents tag everything CONFIRMED) →
  simplify to PRIMARY-only with mandatory composition as PRIMARY
- Action labels change from pilot 1 → investigate what the
  mandatory composition revealed
- Feature Jaccard doesn't improve → the tier isn't adding signal,
  drop it and use PRIMARY-only with mandatory composition

---

## Pilot 1 labels

The 20 labels from pilot 1 are NOT production labels yet. If
rerun confirms and labels match, the rerun labels become
production labels (they have the correct feature attention
format). If labels differ, owner reviews the differences.

---

**Builder: update the v2 prompt with the CONFIRMED tier and
mandatory composition for BET/RAISE. Rerun the pilot on the
same 20 hands with all 6 teams using amended Approach C.
Fresh agents only.**
