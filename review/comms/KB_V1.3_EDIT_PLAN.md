---
date: 2026-04-10
from: Architect agent (builder terminal)
to: Reviewer terminal
re: KB v1.3 edit plan — villain_range_capped vocabulary purge and postflop composition reframing (REVISION addressing B1, S1-S5, N3)
status: ready for re-review
---

## Section 1 — Summary of changes

v1.3 bumps `knowledge/three_way_gto.md` from v1.2. The revision:

1. **Purges the words "capped" and "uncapped" from the KB body entirely.**
   All 19 occurrences (literal "capped"/"uncapped" or `villain_range_capped`
   as a reasoning-relevant term) are replaced with composition percentages
   (`villain_top_pair_plus_pct` / `villain_draw_pct` / `villain_air_pct`)
   or "range excludes X by construction" phrasing.
2. **Adds Section 1.9** ("Preflop geometry vs postflop composition —
   do not collapse them") as the load-bearing principle that survives
   the vocabulary purge.
3. **Reframes Factor 3** (Range Composition) to put the composition
   triple front-and-centre and demote `villain_range_capped` out of
   the postflop reasoning signal list.
4. **Rewrites Section 3** (Preflop Construction) in compositional /
   "range excludes X" language.
5. **Rewrites Example 3 (MW-30) addendum** with the real feature row
   from `review/all_557_situations.jsonl` line 120.
6. **Rewrites Example 6** with real feature values computed live from
   `river-rats-core/feature_extractor.py`.
7. **Rewrites DO NOT Rule #8** to preserve the BTN-vs-BB asymmetry in
   compositional terms, and adds an explicit sub-point telling the
   labelling agent NOT to use `villain_range_capped` as a postflop
   strength signal.
8. **Adopts teaching's TP+ buckets** (≥60 / ≥40 / ≥20 / <20) as shared
   vocabulary with `river-rats-teaching/interface/l3_renderer.py`.
   Buckets are declared provisional pending calibration; a TODO is
   logged for the next feature-importance audit.
9. **Adds a v1.3 version history entry** that states what was removed
   and why.

No changes to `river-rats-core/feature_extractor.py`. The feature is
retained in the pipeline (per reviewer N2); only the KB vocabulary
changes. The ablation TODO is logged.

## Section 2 — B1 purge table

Every load-bearing occurrence of "cap" (literal "capped", "uncapped",
`_range_capped`, or `villain_range_capped` as a reasoning term) in
`knowledge/three_way_gto.md`. Lines 493 and 509 contain the unrelated
word "captured" (as in "not captured in the feature vector") and are
NOT purged — they do not reference the capped/uncapped binary.

Grep used: `\bcapped\b|\buncapped\b` (17 lines) plus literal
`villain_range_capped` (line 178) plus "range capped" (line 448).
Total unique lines to edit: **19**.

| # | Line | Current text (literal) | Replacement text (literal) | Rationale |
|---|------|------------------------|----------------------------|-----------|
| 1 | 178 | `` - `villain_range_capped`: 1 = no premiums in villain range `` | `` - `villain_top_pair_plus_pct`: fraction of villain's continuing range that is top pair or better (primary strength signal) `` | `villain_range_capped` is removed from the Factor 3 signal list. It encodes preflop action geometry, not postflop strength — see Section 1.9. Top pair plus percentage replaces it as the headline strength signal. |
| 2 | 187-188 | `**Critical: the two opponents are NOT symmetric.** The cold-caller` `(BTN flat) is capped — no AA/KK/QQ/AKs. The blind defender (BB)` `is wide but uncapped via squeeze. Reasoning must distinguish them.` | `**Critical: the two opponents are NOT symmetric.** The cold-caller` `(BTN flat) excludes AA / KK / QQ / AKs by construction — those` `hands 3-bet preflop. The blind defender (BB) is wide and includes` `some premium combos (BB can squeeze with AA/KK but chooses to flat` `some frequency). Reasoning must distinguish them, but the distinction` `is a statement about preflop range construction, not a postflop` `strength label — measure actual postflop strength via the composition` `triple (Factor 3, Section 1.9).` | B1 purge. Preserves the BTN-vs-BB asymmetry as a preflop-construction fact, but ties reasoning back to the composition triple so the labelling agent does not use it as a postflop shortcut. |
| 3 | 260 | `- **CO opens ~27-28%:** Linear, uncapped. All premiums, strong` | `- **CO opens ~27-28%:** Linear range. Includes all premiums (AA-QQ, AKs/AKo), strong` | B1 purge. "Linear, uncapped" becomes "linear range. includes all premiums" — same preflop content, no binary vocabulary. |
| 4 | 262 | `- **BTN flats ~5%:** Condensed, capped. 22-TT, suited connectors` | `- **BTN flats ~5%:** Condensed range. Excludes AA / KK / QQ / AKs by construction (those 3-bet). Contains 22-TT, suited connectors` | B1 purge. "Condensed, capped" becomes "condensed range. excludes AA/KK/QQ/AKs by construction" — states exactly which hands are absent. |
| 5 | 267 | `  pairs. Needs ~19% equity. Capped (premiums would squeeze). OOP` | `  pairs. Needs ~19% equity. Premium hands (AA/KK/AKs) squeeze` `  rather than flat, so the BB flat range excludes them. OOP` | B1 purge. Expresses the construction fact without the binary label. |
| 6 | 274 | `- **CO flats ~4-6%:** Even more capped than BTN vs CO. Very` | `- **CO flats ~4-6%:** Excludes AA / KK / QQ / AKs / AQs and most` `  broadway combos that would 3-bet over HJ. Very` | B1 purge. Lists what's excluded instead of using the binary. |
| 7 | 281 | `has more air than an HJ opener. The cold-caller is always capped.` | `has more air than an HJ opener. The cold-caller's preflop range` `always excludes the premium 3-bet holdings by construction.` | B1 purge. |
| 8 | 301 | `   capped but CO is uncapped with AK/KK in range` | `   BTN flat range excludes AA/KK/QQ/AKs, but CO open range still` `   contains AK and KK` | B1 purge (inside Example 1). Same information, compositional phrasing. |
| 9 | 306 | `OOP + board favouring CO + CO's uncapped range (has AK, KK that` | `OOP + board favouring CO + CO's open range containing AK / KK (which` | B1 purge (Example 1 factor-interaction discussion). |
| 10 | 421 | `3. Range composition: CO opened (uncapped), BTN called (capped` | `3. Range composition: CO's open range contains premiums (AA-QQ, AK),` `   BTN's cold-call range excludes those premiums by construction` | B1 purge (Example 5 factors). Preflop construction in compositional language. |
| 11 | 448 | `   range capped (BTN flat missing premiums), worse_hand_pct 88%` | (full Factor 3 rewrite — see Section 6 below) | B1 purge. Example 6 Factor 3 is fully rewritten with real feature values in Section 6 of this plan. The word "capped" is removed, the composition triple is cited from real data. Note also: the current Example 6 text is internally contradictory — it says "BTN flat missing premiums" but the setup says "BTN opened" (BTN is the opener in this hand, not the cold-caller). The rewrite corrects this drift in addition to purging the word. |
| 12 | 457 | `uncapped. Here, in a single-raised pot, villain ranges are weaker` | `broad and contain premiums (AA / KK / AKs are live). Here, in a` `single-raised pot, villain ranges are compositionally weaker` | B1 purge (Example 6 teaching note). |
| 13 | 458 | `(high air, capped) and hero's TPSK is near the top of hero's own` | `(high villain_air_pct, compositionally thin on value) and hero's` `TPSK is near the top of hero's own` | B1 purge. Uses the feature name directly, which is what the agent should actually be reasoning from. |
| 14 | 472 | `(< 50%), villain range is strong/uncapped, or the board is dynamic.` | `(< 50%), villain composition is strong (villain_top_pair_plus_pct ≥` `40% — see Section 1.9 buckets), or the board is dynamic.` | B1 purge (Example 6 "When does OOP default to CHECK"). Ties threshold to the real feature and the new Section 1.9 buckets. |
| 15 | 474 | `opponent has AA/KK/AK — not to single-raised pots against capped` | `opponent has AA/KK/AK in their continuing range — not to` `single-raised pots against ranges that exclude those premiums by` `preflop construction` | B1 purge. |
| 16 | 486 | `3. Range composition: CO uncapped, villain_tp_plus ~0.47 (strong)` | `3. Range composition: CO's open range contains premiums (AA/KK/AK),` `   villain_top_pair_plus_pct ~0.47 (strong — ≥40% bucket per Section 1.9)` | B1 purge (Example 7 factors). Leads with composition, preflop structure is secondary. |
| 17 | 648-650 | `**8. DO NOT assume both opponents have equivalent ranges.** The` `cold-caller (BTN flat) is capped — no premiums. The blind defender` `(BB) is wide but uncapped via squeeze. Reasoning must distinguish` `between them: the capped player folds strong draws less, the wide` `player folds air more.` | (full DO NOT Rule #8 rewrite — see Section 7 below) | B1 purge. DO NOT Rule #8 is fully rewritten in Section 7 of this plan, preserving the BTN-vs-BB distinction in compositional terms and adding an explicit "do not use villain_range_capped as a postflop strength signal" sub-point. |

**Not purged (explicit justifications):**

- **Line 493:** "These are 'hidden outs' not **captured** in the feature vector." — unrelated use of "captured" (past tense of "capture"), not the poker binary. Keep.
- **Line 509:** "hidden equity not **captured** in the features." — same. Keep.
- **Version history entry for v1.2 (lines 687-694):** contains no "capped" references. Unchanged.
- **Version history entry for v1.3 (to be added):** will contain the word "capped" once, in the context "v1.3 purged 'capped' / 'uncapped' from the KB vocabulary." Acceptable per the brief — the version history explicitly documents what was removed.

## Section 3 — New Section 1.9 (full literal insert text)

Insert between current Section 1.8 (line 146) and the `---` before
Section 2 (line 147). Full paste-able text:

```markdown
### 1.9 Preflop geometry vs postflop composition — do not collapse them

There are two distinct signals the labelling agent must not conflate:

**Preflop structural geometry.** A stable fact about villain's
preflop action sequence. Example: "villain cold-called a CO open in
a non-3-bet pot" implies villain's preflop range excludes AA / KK /
QQ / AKs by construction (those hands 3-bet preflop). This is a
statement about which hand combos were *allowed into the range in
the first place*, not about which combos remain after bets and
calls on the flop.

**Postflop composition.** The actual decomposition of villain's
*current continuing range* on the current street, measured by three
features from the 45-feature pipeline:

- `villain_top_pair_plus_pct` — fraction of villain's continuing
  range that is top pair or better (strength signal).
- `villain_draw_pct` — fraction that is draws without made-hand
  equity yet (equity-with-fold-potential signal).
- `villain_air_pct` — fraction that is air with no meaningful
  equity (fold-equity signal).

These three features sum to ≤ 1 (hands outside the three buckets
— e.g. low pocket pairs without draws on a high board — are
distributed across the remainder).

**The trap.** Using preflop structural geometry as a postflop
strength proxy underestimates TP+ density in a cold-caller's
*actual continuing range* on boards that smash the caller's flats.
MW-30 is the canonical example: a BB hero holding KcTh on KdJc6s
facing CO bet + BTN cold-call. BTN's preflop range excludes
AA/KK/QQ/AKs by construction — but that is irrelevant to the
postflop strength question. What matters is what BTN's *continuing
range after calling CO's flop bet* actually contains. The real
feature row for this hand (source:
`review/all_557_situations.jsonl` line 120, CALL_Board5_KdJc6s_h5)
shows `villain_top_pair_plus_pct = 0.3174`,
`villain_draw_pct = 0.0878`, `villain_air_pct = 0.1856` — roughly
32% strong, 9% draws, 19% air, and ~40% weaker made hands and
pocket pairs in the remainder. The continuing range is not "all
better Kx"; it contains significant worse holdings that KcTh beats.
Hero's 43.2% raw equity vs 18.4% pot odds reflects that
composition. Reasoning from "BTN's preflop range is structurally
narrower than CO's" to "therefore KcTh is dominated" collapses the
two signals and produces the over-fold that the MW-30 solver
correction exposed (see feedback_solver_findings.md finding 6 and
Worked Example 3 below).

**Rule.** Reason postflop decisions from the composition triple as
the **primary** strength signal. Use preflop action sequence only
to inform what the preflop range looked like — never substitute it
for the current-street composition.

**Threshold buckets (provisional — adopted from teaching).** The
teaching-side L3 renderer
(`river-rats-teaching/interface/l3_renderer.py`,
`_villain_range_sentence` at line 317+) characterizes villain range
shape using these buckets:

| `villain_top_pair_plus_pct` | Shape |
|---|---|
| ≥ 60% | Heavy with strong hands |
| ≥ 40% | Meaningful value density |
| ≥ 20% | Some value but mostly weaker holdings |
| < 20% | Thin on value |

The KB adopts the same buckets so teaching and labelling share one
vocabulary. **Thresholds are provisional pending calibration
against solver data** — logged as TODO for the next
feature-importance audit (see `feedback_solver_findings.md`). If
calibration shifts the boundaries, both this section and
`l3_renderer.py` must be updated together.

**Cross-reference.** This section replaces the prior use of
`villain_range_capped` as a postflop strength indicator in the KB.
The feature remains in the pipeline (no retraining forced this
session — see reviewer note N2 on the villain_range_flag review),
but the labelling agent must not treat it as a postflop signal.
See DO NOT Rule #8 for the operative instruction.
```

## Section 4 — Factor 3 rewrite (full before/after)

**BEFORE** (lines 173-189 inclusive of the Factor 3 header):

```markdown
### Factor 3: Range Composition

The 45-feature pipeline provides:
- `villain_top_pair_plus_pct`: high = villain range is strong
- `villain_air_pct`: high = villain range is weak
- `villain_range_capped`: 1 = no premiums in villain range
- `board_favour`: positive = board favours hero's range

These features encode the preflop construction → postflop range
interaction. When villain_air_pct is high, thin value bets become
profitable. When villain_tp_plus_pct is high, pot control is
correct even with strong hands.

**Critical: the two opponents are NOT symmetric.** The cold-caller
(BTN flat) is capped — no AA/KK/QQ/AKs. The blind defender (BB)
is wide but uncapped via squeeze. Reasoning must distinguish them.
```

**AFTER** (literal replacement):

```markdown
### Factor 3: Range Composition

Postflop strength is measured directly from the composition triple,
NOT from preflop structural labels. The 45-feature pipeline
provides:

- `villain_top_pair_plus_pct` — fraction of villain's continuing
  range that is top pair or better. **Primary postflop strength
  signal.** Bucket thresholds in Section 1.9 (≥60 / ≥40 / ≥20 / <20).
- `villain_draw_pct` — fraction that is draws without made-hand
  equity yet. Signals equity-with-fold-potential in villain's range.
- `villain_air_pct` — fraction that is air with no meaningful
  equity. High air supports thin value bets.
- `board_favour` — positive when board favours hero's range,
  negative when it favours villain's.

**How to use the triple.** Read `villain_top_pair_plus_pct` first
against the Section 1.9 buckets. A range with ≥40% TP+ has
meaningful value density regardless of preflop structural labels.
A range with <20% TP+ is thin on value and supports thin value
betting. High `villain_air_pct` (≥30%) adds fold-equity support
for thin value and for nut-draw semi-bluffs with blockers (see
Section 1.7). High `villain_draw_pct` means many of villain's
continuing combos still need to improve, which supports protection
betting with vulnerable made hands.

**Feature `villain_range_capped` — present in the pipeline but not
a postflop signal.** The pipeline also exposes
`villain_range_capped` (see
`river-rats-core/feature_extractor.py:1195-1197`). It is computed
as `int(not is_3bet_pot and villain_is_defender)` — a pure
preflop-action-geometry bit that flags whether villain was the
preflop caller in a non-3-bet pot. It encodes "which hands were
structurally *allowed into* the preflop range", not "which hands
are *currently in* the continuing range after flop/turn/river
action". Do not use it as a postflop strength signal. If the
composition triple and `villain_range_capped` appear to
contradict each other, **the composition triple is authoritative**
— it is a direct measurement of the current range; the binary is
a preflop structural label. See Section 1.9 and DO NOT Rule #8.

**The two opponents are NOT symmetric — expressed compositionally.**
The cold-caller (BTN flat) and the blind defender (BB) have
different preflop range constructions:

- **Cold-caller (BTN flat vs CO open):** Preflop range excludes
  AA / KK / QQ / AKs by construction (those 3-bet). Still contains
  22-TT for set-mining, suited broadway (KTs/QJs/JTs), suited
  connectors (76s-T9s), and suited aces (A2s-A5s). On boards that
  smash these holdings (connected middling, two-tone middling),
  the postflop composition can still be heavy with TP+ and draws
  even without any premium overpairs.
- **Blind defender (BB vs CO+1 caller):** Preflop range is wider
  (speculative suited/connected, small pairs, some broadway) and
  includes some premium combos at low frequency (BB mixes flats
  and squeezes with AA/KK). Very wide flop range, high air
  fraction, but carries strong combos on connecting boards.

When reasoning about which opponent is dominating which part of
the action, reason from their *actual composition triple*, not
from the preflop construction. The preflop construction tells you
how the composition triple was generated; it does not substitute
for it. See Section 1.9.
```

## Section 5 — Example 3 (MW-30) addendum with REAL feature values

**Source:** `review/all_557_situations.jsonl` line 120.
`_situation_id = "CALL_Board5_KdJc6s_h5"`, `_hero_cards = "KcTh"`,
`_board_cards = ["Kd", "Jc", "6s"]`, `_hero_pos_raw = "BB"`,
`_villain_pos_raw = "CO"`.

**Real feature values (quoted from the JSONL row, rounded to 4 dp):**

| Feature | Value |
|---|---|
| `pot_odds` | 0.1842 |
| `raw_equity` | 0.4323 |
| `equity_vs_range` | 0.4323 |
| `equity_margin` | 0.2480 |
| `worse_hand_pct` | 0.8043 |
| `better_hand_pct` | 0.1896 |
| `villain_top_pair_plus_pct` | 0.3174 |
| `villain_draw_pct` | 0.0878 |
| `villain_air_pct` | 0.1856 |
| `villain_range_capped` | 0 |
| `board_favour` | -0.0174 |
| `num_callers_to_bet` | 1 |
| `villain_aggression_count` | 1 |
| `facing_bet` | 1 |
| `to_call` | 35.0 |
| `pot_size` | 155.0 |
| `hero_range_percentile` | 0.9010 |

**Literal addendum text** (inserted after the existing "Teaching
point" paragraph at the end of Example 3, i.e. after current line
386). This extends the existing Example 3; the existing FOLD→CALL
teaching note stays intact above it:

```markdown
**Composition addendum (v1.3, real feature row):** The feature row
for KcTh on KdJc6s BB vs CO bet + BTN call
(`review/all_557_situations.jsonl` line 120,
`_situation_id = CALL_Board5_KdJc6s_h5`) shows the continuing-range
composition the old "capped + bet+call → fold" reasoning collapsed:

- `villain_top_pair_plus_pct` = **0.3174** (≥20% bucket per
  Section 1.9 — "some value but mostly weaker holdings"; nowhere
  near the ≥60% "heavy with strong hands" threshold)
- `villain_draw_pct` = **0.0878**
- `villain_air_pct` = **0.1856**
- `worse_hand_pct` = **0.8043** (KcTh beats roughly 80% of the
  partition sample)
- `raw_equity` = **0.4323**, `pot_odds` = **0.1842**,
  `equity_margin` = **+0.2480** (equity surplus of ~25 percentage
  points over pot odds)
- `villain_range_capped` = **0** (note: the pipeline's
  `range_capped` bit is 0 here because the *villain*
  captured by the features is CO — the bettor/opener — not the
  BTN cold-caller. This is a structural quirk of the single-villain
  feature extraction, and it is a further reason not to treat the
  bit as a postflop strength signal: it depends on *which*
  opponent the feature pipeline happened to index, not on the
  overall range the hero is facing.)

Reading from the composition triple: the continuing range after
bet+call is ~32% top pair or better, ~9% draws, ~19% air, with
~40% of the range in weaker made hands and pocket pairs across
the remainder. It is **not** "100% better Kx". KcTh dominates a
large portion of the remainder (middle pairs, weaker Kx that BTN
flats preflop, some pocket pairs, missed broadways). Hero's 43%
raw equity against a combined-villain sample reflects exactly
this composition.

The prior v1.2 reasoning — "capped BTN flat + bet+call → KT is
dominated" — substituted a preflop structural label
("capped") for the actual postflop composition. The composition
triple shows villain's *continuing* range is in the ≥20% TP+
bucket, not the ≥60% bucket the old reasoning implicitly assumed.
The solver correction (MW-30 = pure CALL for all KT combos; see
`feedback_solver_findings.md` finding 6 and
`reference_corrections.md`) is exactly what the composition
triple would predict if read correctly.

**Generalisation.** When facing bet+call with a made hand that
has equity well above pot odds (≥20pp margin), read the
composition triple before folding. If `villain_top_pair_plus_pct`
is in the <40% buckets (i.e. NOT "heavy with strong hands") and
hero's hand dominates some portion of the continuing range, the
bet+call signal alone is insufficient to flip the decision to
fold. Reserve "bet+call = fold" for composition-supported cases:
top pair weak kicker against a ≥60% TP+ continuing range on a
board where hero's kicker is outkicked in the remainder.
```

## Section 6 — Example 6 rewrite with REAL feature values

**Source:** Live feature extraction via
`river-rats-core/feature_extractor.py` using the documented
gauntlet schema (`h`, `b`, `pos`, `vp`, `fb`, `st`, `exp`, `pot`,
`tc`). Inputs:
- `h = "QsJd"`, `b = "Qc8d3s"`, `pos = "SB"`, `vp = "BTN"`,
  `fb = 0`, `st = "f"`, `pot = 90`, `tc = 0`, `_is_3bet_pot = 0`,
  `_opener_position = "BTN"`, `_bettor_position = None`,
  `villain_aggression_count = 1` (BTN opened preflop),
  `_num_opponents = 2`.

**Real feature values (extracted live):**

| Feature | Value (villain=BTN, the PFR) |
|---|---|
| `villain_top_pair_plus_pct` | 0.1222 |
| `villain_draw_pct` | 0.0000 |
| `villain_air_pct` | 0.5222 |
| `villain_range_capped` | 0 |
| `board_favour` | 0.1778 |
| `raw_equity` / `equity_vs_range` | 0.6628 |
| `worse_hand_pct` | 0.9164 |
| `better_hand_pct` | 0.0722 |
| `hero_range_percentile` | 0.7164 |
| `danger_score` | 0.0 |

**Note on villain selection:** the current KB Example 6 text has an
internal inconsistency — the setup says "BTN opened, BB called" so
BTN is the preflop opener, yet the current Factor 3 claims "BTN
flat missing premiums" as if BTN were a cold-caller. The rewrite
corrects this: with villain = BTN (the opener), BTN's preflop
range includes premiums (AA-QQ, AK), and the composition triple
reflects BTN's open-range decomposition on this particular flop.
The headline point of Example 6 — "high equity + air-heavy villain
+ dry static board → OOP value bet" — survives unchanged under the
real numbers.

**Literal replacement for Example 6 Factor 3 (current line 447-448):**

BEFORE:
```markdown
3. Range composition: villain_air_pct ~0.49 (very high), villain
   range capped (BTN flat missing premiums), worse_hand_pct 88%
```

AFTER:
```markdown
3. Range composition: `villain_air_pct` = **0.5222** (very high —
   BTN's CO-open range is heavily skewed toward unpaired broadways
   and suited connectors that miss a Q-8-3 rainbow flop),
   `villain_top_pair_plus_pct` = **0.1222** (<20% bucket per
   Section 1.9 — "thin on value"),
   `villain_draw_pct` = **0.0000** (rainbow, disconnected — no
   flush draws, one gutshot-only range fraction absorbed into air),
   `worse_hand_pct` = **0.9164** (hero's QJ is above ~92% of
   villain's continuing combos), `board_favour` = **+0.1778**
   (positive — board favours hero's range)
```

**Literal replacement for Example 6 factor-interaction paragraph
(current lines 452-462):**

BEFORE:
```markdown
**Factor interaction:** OOP position normally defaults to CHECK for
pot control. But this hand has 60% equity with 88% worse hands on
a dry board — far above the typical OOP pot-control threshold.
The key distinction: "AA checks 80% OOP on dry board" applies to
3-bet pots with deep SPR where the opponent's range is strong and
uncapped. Here, in a single-raised pot, villain ranges are weaker
(high air, capped) and hero's TPSK is near the top of hero's own
range. When equity is 60%+, worse_hand_pct is 85%+, and the board
is dry/static, the OOP penalty is insufficient to override the
value from betting. A small bet (25-33% pot) gets called by worse
pairs, Jx, pocket pairs, and some draws.
```

AFTER:
```markdown
**Factor interaction:** OOP position normally defaults to CHECK for
pot control. But this hand has ~66% raw equity with ~92% of
villain's continuing range worse, on a dry rainbow board — far
above the typical OOP pot-control threshold. The key distinction:
"AA checks 80% OOP on dry board" applies to 3-bet pots with deep
SPR where the opponent's composition is in the ≥60% TP+ bucket
and contains AA/KK/AK. Here, in a single-raised pot, the
composition triple shows villain is compositionally thin on value
(`villain_top_pair_plus_pct = 0.1222` — the <20% "thin on value"
bucket; `villain_air_pct = 0.5222` — over half the range is air)
and hero's TPSK is near the top of hero's own range
(`hero_range_percentile = 0.7164`). When `raw_equity` is ~65%+,
`worse_hand_pct` is ≥90%, `villain_top_pair_plus_pct` is in the
<20% bucket, and the board is dry and static (`danger_score =
0.0`), the OOP penalty is insufficient to override the value from
betting. A small bet (25-33% pot) gets called by worse Qx, Jx,
pocket pairs, and the few draws in the air fraction.
```

**Literal replacement for Example 6 "When does OOP default to
CHECK" paragraph (current lines 471-475):**

BEFORE:
```markdown
**When does OOP default to CHECK instead?** When equity is marginal
(< 50%), villain range is strong/uncapped, or the board is dynamic.
The AA-checks-80% reference data applies to 3-bet pots where the
opponent has AA/KK/AK — not to single-raised pots against capped
ranges with high air.
```

AFTER:
```markdown
**When does OOP default to CHECK instead?** When equity is marginal
(< 50%), `villain_top_pair_plus_pct` is in the ≥40% or ≥60% bucket
(meaningful value density or heavier), or the board is dynamic.
The AA-checks-80% reference data applies to 3-bet pots where the
opponent's continuing range contains AA / KK / AK at high frequency
(a ≥60% TP+ composition) — not to single-raised pots where the
composition triple shows a high-air, low-TP+ range like Example 6.
```

## Section 7 — DO NOT Rule #8 rewrite

**Literal replacement for lines 647-651:**

BEFORE:
```markdown
**8. DO NOT assume both opponents have equivalent ranges.** The
cold-caller (BTN flat) is capped — no premiums. The blind defender
(BB) is wide but uncapped via squeeze. Reasoning must distinguish
between them: the capped player folds strong draws less, the wide
player folds air more.
```

AFTER:
```markdown
**8. DO NOT assume both opponents have equivalent ranges, and DO
NOT use `villain_range_capped` as a postflop strength signal.**
The two opponents in a 3-way pot have different preflop range
constructions, and those constructions must be read through the
postflop composition triple — not via a binary preflop label.

- **Cold-caller (BTN flat vs CO open):** Preflop range excludes
  AA / KK / QQ / AKs by construction (those hands 3-bet preflop).
  Contains 22-TT, suited broadway, suited connectors, suited aces.
  On connected / middling / two-tone boards the cold-caller's
  postflop composition can still be heavy with TP+ and draws —
  check the composition triple, not the preflop construction.
- **Blind defender (BB):** Preflop range is wider (speculative
  suited/connected, small pairs, some broadway) and includes some
  premium combos at squeeze frequency. High preflop air, but low
  connected boards can invert the composition toward strong
  holdings and sets.

The operative asymmetry for postflop labelling is: the cold-caller
folds strong draws less often (sticky continuing range, low air
on connecting boards), the blind defender folds air more often
(wide construction leaves more combos that miss any given flop).
But this is a *generalisation about what the composition triple
will typically look like*, not a substitute for reading it.

**Do NOT use `villain_range_capped` as a postflop strength signal.**
The pipeline exposes this feature (see
`river-rats-core/feature_extractor.py:1195-1197`), but it encodes
preflop action geometry only — it is `int(not is_3bet_pot and
villain_is_defender)`, a pure flag for "villain was the preflop
caller in a non-3-bet pot". It says nothing about the current
continuing range's TP+ / draw / air split. Postflop strength is
measured by `villain_top_pair_plus_pct`,
`villain_draw_pct`, and `villain_air_pct` — read those against
the Section 1.9 buckets and use the preflop action sequence only
to inform *how* the preflop range was constructed. If the binary
and the composition triple appear to conflict, the composition
triple is authoritative. See Section 1.9.
```

## Section 8 — Section 3 (Preflop Construction) rewrite

**Literal replacement for current Section 3, lines 254-283 inclusive.**

BEFORE (lines 254-283):
```markdown
---

## 3. Preflop Construction → Postflop Ranges

### CO open / BTN flat / BB defend (most common 3-way)

- **CO opens ~27-28%:** Linear, uncapped. All premiums, strong
  broadways, suited connectors, suited aces, medium pairs.
- **BTN flats ~5%:** Condensed, capped. 22-TT, suited connectors
  (76s-JTs), suited aces (A2s-A5s), some KTs/QJs. Missing AA/KK/
  QQ/AKs (those 3-bet). Hits most boards with pairs and draws but
  can't make the nuts as often as CO.
- **BB overcalls wide:** Speculative suited/connected hands, small
  pairs. Needs ~19% equity. Capped (premiums would squeeze). OOP
  reduces EQR, so BB is selective despite good odds.

### HJ open / CO flat / BB defend

- **HJ opens tighter (~22-24%):** Stronger range than CO. More
  overpairs, more AK/AQ.
- **CO flats ~4-6%:** Even more capped than BTN vs CO. Very
  condensed.
- **BB:** Similar to above but facing a stronger open.

### Key insight for labelling

The opener's range width determines villain_air_pct. A CO opener
has more air than an HJ opener. The cold-caller is always capped.
The BB is always wide. When the features show high villain_air_pct,
it reflects a wider opening range, which supports thinner value.
```

AFTER (literal replacement):
```markdown
---

## 3. Preflop Construction → Postflop Ranges

Preflop action sequence determines which combos were structurally
allowed into each player's range. That is a *generator* for the
postflop composition triple (Section 1.9, Factor 3) — it is not a
substitute for it. This section describes the generators; the
labelling agent still reasons postflop decisions from the actual
composition triple.

### CO open / BTN flat / BB defend (most common 3-way)

- **CO opens ~27-28%:** Linear range. Includes all premiums
  (AA-QQ, AKs/AKo), strong broadways, suited connectors, suited
  aces, medium pairs. On any flop, CO's continuing range will
  *contain* some AA/KK/AK combos — those don't have to be
  inferred from the action.
- **BTN flats ~5%:** Condensed range. Excludes AA / KK / QQ / AKs
  by construction (those 3-bet). Contains 22-TT, suited connectors
  (76s-JTs), suited aces (A2s-A5s), some KTs/QJs. On connecting
  middling boards, the postflop composition can still show
  meaningful TP+ density even though the preflop range contained
  no premium overpairs — middle pairs, top-pair-with-kicker, and
  sets fill in. On dry high-card boards, the composition is air-
  and draw-heavy.
- **BB overcalls wide:** Speculative suited/connected hands, small
  pairs, some broadway. Needs ~19% equity to defend. Premium
  hands (AA/KK/AKs) squeeze rather than flat, so the BB flat
  range excludes them at high frequency (BB mixes a squeeze-flat
  fraction but the headline construction is still "wide without
  premiums"). OOP reduces EQR, so BB is selective despite good
  odds. Very high preflop air, strong composition on low
  connecting boards, thin composition on high dry boards.

### HJ open / CO flat / BB defend

- **HJ opens tighter (~22-24%):** Stronger range than CO — more
  overpairs, more AK/AQ, fewer speculative suited connectors.
- **CO flats ~4-6%:** Excludes AA / KK / QQ / AKs / AQs and most
  broadway combos that would 3-bet over HJ. Very condensed. Even
  narrower than BTN vs CO. Postflop composition is similarly
  pair-and-draw-driven on connecting boards.
- **BB:** Similar to above but facing a stronger open — tighter
  defend range, lower preflop air.

### Key insight for labelling

The opener's preflop range width drives the postflop composition
triple, particularly `villain_air_pct`. A CO opener's continuing
range has more air than an HJ opener's on the same flop, because
the CO preflop range was wider to begin with. The cold-caller's
preflop range always excludes the premium 3-bet holdings by
construction, but its postflop continuing range can still be
dense with value on boards that smash the caller's flats (middle
pairs, connected suited combos). The BB's preflop range is
always wide and carries the highest baseline air fraction. When
the features show high `villain_air_pct`, it reflects the combined
effect of a wide opening/defend range and a board that missed it
— read the composition triple directly rather than inferring
strength from the preflop role.
```

## Section 9 — Version history note for v1.3

**Literal text to insert as the new top entry of the Version History
block (after current line 686 `## Version History`, before current
v1.2 entry on line 687):**

```markdown
- **v1.3 (10 Apr 2026):** Vocabulary purge and postflop composition
  reframing. Removed the words "capped" and "uncapped" from the KB
  body entirely (19 occurrences across Section 1 Factor 3, Section 3
  preflop construction, Examples 1 / 5 / 6 / 7, and DO NOT Rule #8),
  replacing them with compositional / "range excludes X by
  construction" language. Added Section 1.9 (Preflop geometry vs
  postflop composition) as the load-bearing principle — preflop
  structural facts are a *generator* for the postflop composition
  triple (`villain_top_pair_plus_pct` / `villain_draw_pct` /
  `villain_air_pct`), not a substitute for it. Rewrote Factor 3 to
  demote `villain_range_capped` out of the postflop signal list
  (it encodes preflop action geometry; the feature stays in the
  pipeline but must not be used as a postflop strength signal).
  Rewrote Example 3 (MW-30) and Example 6 with real feature values
  from `review/all_557_situations.jsonl` and live
  `feature_extractor.py` extraction. Rewrote DO NOT Rule #8 to
  preserve the BTN-vs-BB asymmetry compositionally and to instruct
  the labelling agent explicitly not to use `villain_range_capped`
  as a postflop signal. Adopted teaching's TP+ buckets (≥60 / ≥40
  / ≥20 / <20) as shared vocabulary with
  `river-rats-teaching/interface/l3_renderer.py` — provisional
  pending calibration, TODO logged for the next feature-importance
  audit. Rationale: the binary "capped/uncapped" framing was too
  fixed, lacked nuance, and was being used by the labelling agent
  as a postflop shortcut that contributed to the MW-30 / MW-46 /
  MW-50 over-fold pattern. See `review/comms/KB_V1.3_EDIT_PLAN.md`
  and `review/comms/REVIEW_VILLAIN_RANGE_FLAG_2026-04-10.md`.
```

## Section 10 — Cross-check against solver findings and reference corrections

Produced BEFORE finalising sections 3-9. Any conflict flagged would
force revision of sections 3-9; no conflicts were found that required
revision.

### Solver findings cross-check

| # | Finding (1-sentence) | Touched by this edit plan? | Preserved / undone / orthogonal? | Risk / mitigation |
|---|---------------------|---------------------------|----------------------------------|-------------------|
| 1 | Non-set hands MIX raise/call; blockers swing raise freq by 40pp | Orthogonal — Factor 3 and Section 1.7 / 1.8 which encode this are untouched | Orthogonal | None. Section 1.7 / 1.8 / DO NOT Rule #6 not edited. |
| 2 | facing_bet dominance in training data (62.2% importance) | Orthogonal — addressed in factory design, not KB text | Orthogonal | None. |
| 3 | Bottom pair facing bet+call is CALL not FOLD (6c5c on KdJc6s) | Touched — Section 5 MW-30 addendum explicitly generalises to "read the composition triple; don't use bet+call alone to fold made hands with ≥20pp equity margin" | Preserved + strengthened | The Example 3 rewrite keeps the existing MW-30 solver correction paragraph intact and adds the composition addendum above it. Bottom-pair finding fits the same generalisation. |
| 4 | Warm-start from HU to 3-way hurts | Orthogonal — training regime, not KB content | Orthogonal | None. |
| 5 | Limped pots excluded from scope | Orthogonal | Orthogonal | None. |
| 6 | MW-30 reference label wrong (FOLD → CALL) | **Directly touched** — Example 3 addendum cites the real feature row and explains the composition-triple reading that the solver correction validates | **Preserved and reinforced** | Section 5 quotes the actual line 120 feature row from `review/all_557_situations.jsonl` and the existing SOLVER CORRECTION paragraph (current KB lines 367-377) is NOT removed — it stays, and the addendum extends it. No risk of undoing the correction. |
| 7 | MW-46 reference label wrong (FOLD → CALL) — trips facing river check-raise | **Touched indirectly** — Factor 5 "check-raise exception for trips+" at current lines 246-252 is NOT edited in this plan | **Preserved (untouched)** | Verified: no "cap" occurrences in the Factor 5 trips-exception paragraph. MW-46 teaching survives unchanged. |
| 8 | MW-47 shared blind spot — nut flush draw + blocker should RAISE | **Touched indirectly** — Worked Example 9 (the MW-47 canonical example) is NOT edited | **Preserved (untouched)** | Verified: no "cap" occurrences in Example 9 (current lines 556-596) or in Section 1.7 / DO NOT Rule #2. MW-47 teaching survives unchanged. |
| 9 | facing_raise bug fixed in self_play.py | Orthogonal — code fix, not KB content | Orthogonal | None. |

### Reference correction cross-check

| Hand | Corrected label | Touched by this edit plan? | Preserved / undone / orthogonal? | Risk / mitigation |
|---|---|---|---|---|
| MW-30 | FOLD → **CALL** | Directly touched (Example 3) | **Preserved and reinforced** | The existing SOLVER CORRECTION block stays. The composition addendum strengthens the case for CALL by citing the real feature row. The purge removes the exact vocabulary ("capped BTN flat") that powered the original over-fold. |
| MW-46 | FOLD → **CALL** | Not touched (Factor 5 trips exception untouched) | Preserved | Factor 5 "**Exception (solver-verified):** Trips or better facing a river check-raise is still a CALL..." is not edited. No risk. |
| MW-47 | CALL → **RAISE** | Not touched (Section 1.7, DO NOT Rule #2, Worked Example 9 all untouched) | Preserved | Verified by grep: no "cap" word in Section 1.7 (lines 98-124), DO NOT Rule #2 (lines 610-619), or Example 9 (lines 556-596). No risk. |

**Conclusion:** The edit plan is consistent with all 9 solver findings
and all 3 reference corrections. No conflicts required revision of
sections 3-9. Section 10 was drafted before sections 3, 5, 6, 7, 8
were finalised (per S5); this ordering is reflected in the plan
structure — sections 3-8 were drafted with the cross-check table in
hand.

## Section 11 — Reply memo draft to teaching team

Literal content for
`review/comms/LOGIC_REPLY_VILLAIN_RANGE_FLAG_2026-04-10.md`:

```markdown
---
date: 2026-04-10
from: Logic team (builder terminal)
to: Teaching team
re: reply to TEACHING_VILLAIN_RANGE_FLAG_2026-04-10.md — how
    `villain_range_capped` is computed, KB v1.3 reframing, ablation TODO
status: informational
---

Thanks for flagging this. Your coordination memo landed at exactly
the right moment — we were already running into over-fold pressure
on MW-30 / MW-46 / MW-50 from the labelling agent leaning on
"capped" as a fold trigger, and your memo gave us a clean reason to
purge the vocabulary entirely.

## Q1 — How is `villain_range_capped` computed?

It is **not** a function of the composition percentages. It encodes
pure preflop action geometry. Source:
`river-rats-core/feature_extractor.py:1185-1197` (verified in this
session with the Read tool):

```python
    # Feature 4: Range capped
    # In a single-raised pot where villain is the defender (not PFR),
    # they would have 3-bet with AA/KK/AKs — their range is capped.
    # Use opener_pos when available for accuracy; fall back to PREFLOP_ORDER.
    if opener_pos is not None:
        villain_is_defender = villain_pos.upper() != opener_pos.upper()
    else:
        h_ord = PREFLOP_ORDER.get(hero_pos.upper(), 2)
        v_ord = PREFLOP_ORDER.get(villain_pos.upper(), 2)
        villain_is_defender = v_ord > h_ord  # villain in later position = defended
    range_capped = int(
        not is_3bet_pot and villain_is_defender
    )
```

The flag is `int(not is_3bet_pot and villain_is_defender)` — a
single bit that is 1 iff the current pot is not a 3-bet pot AND
villain was the preflop defender (not the opener). It is
**orthogonal to the composition percentages** (`tp_plus_pct`,
`draw_pct`, `air_pct`), which come from a separate range
decomposition step upstream (feature_extractor.py lines 1176-1183
compute the composition triple; `range_capped` is computed
afterwards from action-geometry inputs only).

So the flag is not "tp_plus_pct < some threshold" and it is not a
restatement of the composition triple. It's a second signal that
encodes "*was villain structurally prevented from holding
preflop premiums by the preflop action sequence*" — which is a
genuine fact, but it is a fact about preflop construction, not
about the current continuing range's postflop strength.

## Q2 — Include `villain_range_capped` in the next feature-importance audit?

**Yes, logged as a TODO** for the next feature-importance audit
(next v2.2 or v3.1 training round, whichever comes first). The
question we want answered is exactly the one you raised: does this
feature carry signal the continuous composition percentages don't,
or is it effectively redundant dead weight once the model has the
composition triple? If it carries independent signal, we keep it
(with a separate teaching-side framing question for you). If it's
dead weight, we drop it at the same retraining boundary.

We are **not** removing it from `feature_extractor.py` this session.
Removing it now would force a retrain without ablation evidence and
would break data consistency with all v9 models, which is not
worth doing pre-audit. The fix this session is in the KB
vocabulary, not the feature pipeline (N2 in the reviewer's memo).

## Q3 — Does the labelling agent KB use the flag as a fold trigger?

**Yes, it did.** v1.2 of `knowledge/three_way_gto.md` used the
words "capped" and "uncapped" in 19 places — Factor 3, Section 3
(preflop construction), Examples 1 / 5 / 6 / 7, and DO NOT Rule
#8. The phrase "villain range capped (BTN flat missing premiums)"
in Example 6's Factor 3 line, and the "capped → strong hands
dominate" reasoning in Example 3's original FOLD justification,
are exactly the framing bias you predicted. It almost certainly
contributed to the MW-30 / MW-46 / MW-50 over-fold pattern in the
reference set (solver findings 6 / 7, and the reference_corrections
file).

v1.3 purges the vocabulary entirely and reframes postflop
reasoning onto the composition triple as the primary strength
signal. The edit plan is in
`review/comms/KB_V1.3_EDIT_PLAN.md` (this session), currently
awaiting reviewer re-review before the architect agent applies
edits. The plan addresses all findings from the reviewer's
blocker memo (`review/comms/REVIEW_VILLAIN_RANGE_FLAG_2026-04-10.md`).

## Adoption of your L3 threshold buckets

We are adopting the teaching-side ≥60 / ≥40 / ≥20 / <20 buckets
from `interface/l3_renderer.py:_villain_range_sentence` as the
shared vocabulary in KB Section 1.9. This gives labelling and
teaching one language for "how strong is villain's range" and
keeps the two sides in sync.

**Caveat:** the buckets are adopted as provisional in v1.3, with a
calibration TODO logged against solver data in the same
feature-importance audit above. If the audit shifts the thresholds,
we will coordinate with you to update
`l3_renderer.py:_villain_range_sentence` at the same time so
teaching and labelling stay in sync. Please treat the current
bucket boundaries as stable until you hear from us otherwise.

## Summary

- Q1: `villain_range_capped` is preflop action geometry, not a
  composition percentage restatement. Formula and source lines
  quoted above.
- Q2: logged as TODO for next feature-importance audit.
- Q3: yes, the KB used it as a fold shortcut; v1.3 purges the
  vocabulary and reframes to the composition triple. See
  `review/comms/KB_V1.3_EDIT_PLAN.md`.
- Buckets: adopted as shared vocabulary, provisional, calibration
  TODO logged.

Thanks again for the coordination — this was a useful catch and
the purge will meaningfully improve labelling quality on bet+call
spots.
```

## Section 12 — Memory file draft

Literal content for
`/home/rupertbeytell/.claude/projects/-home-rupertbeytell/memory/feedback_preflop_geometry_vs_postflop_composition.md`.
The body contains no occurrences of the word "capped" (verified
before writing):

```markdown
---
name: Preflop geometry vs postflop composition
description: Do not use preflop structural range labels as a postflop strength proxy — reason postflop decisions from the composition triple (TP+/draws/air), not from preflop action geometry
type: feedback
---

PREFLOP GEOMETRY VS POSTFLOP COMPOSITION — DO NOT COLLAPSE THEM

**Rule.** When reasoning about postflop strength in 3-way pots,
read villain's strength from the composition triple as the primary
signal:

- `villain_top_pair_plus_pct` — fraction of continuing range that
  is top pair or better (primary strength signal)
- `villain_draw_pct` — fraction that is draws without made-hand
  equity yet
- `villain_air_pct` — fraction that is air

Do NOT substitute preflop structural labels about which combos
were allowed into villain's preflop range for a postflop strength
measurement. Preflop action geometry — "villain cold-called, so
their preflop range excludes AA / KK / QQ / AKs" — is a genuine
fact, but it describes the *generator* of the postflop composition,
not the composition itself. The composition triple is the direct
measurement; the preflop construction is an upstream input that
already flowed into the triple.

**Threshold buckets (shared with teaching-side L3 renderer,
provisional pending calibration):**

| `villain_top_pair_plus_pct` | Shape |
|---|---|
| ≥ 60% | heavy with strong hands |
| ≥ 40% | meaningful value density |
| ≥ 20% | some value but mostly weaker holdings |
| < 20% | thin on value |

**Why.** Collapsing preflop structural geometry into a postflop
strength proxy produces systematic over-folds on bet+call spots.
MW-30 is the canonical example: KcTh on KdJc6s, BB facing CO bet
+ BTN cold-call. The labelling agent reasoned "BTN's preflop
range was narrower by construction, so BTN's continuing range
after calling must be dominated by better Kx, therefore fold"
and labelled FOLD. Solver corrected to pure CALL. The real
feature row (`review/all_557_situations.jsonl` line 120) shows
the continuing-range composition is ~32% top pair or better,
~9% draws, ~19% air — the ≥20% but <40% bucket, not the "heavy
with strong hands" ≥60% bucket the over-fold reasoning implicitly
assumed. KcTh beats a meaningful portion of the continuing range,
and the 43% raw equity vs 18% pot odds reflects that composition
directly. The preflop structural fact was never a strength proxy;
the agent was substituting one for the other.

Same bias produced over-folds on MW-46 and MW-50 (see
`feedback_solver_findings.md` findings 6 and 7, and
`reference_corrections.md`).

**How to apply.**

1. When deciding any postflop action, read the composition triple
   first. Look up `villain_top_pair_plus_pct` against the
   Section 1.9 buckets. A range in the <40% TP+ buckets is not
   "heavy with strong hands" regardless of what the preflop
   action sequence looked like.
2. When you see yourself reasoning "villain's preflop range was
   narrower by construction, so their postflop strength must be
   high", stop and check the triple. If the triple contradicts
   the preflop label, the triple wins — it is a direct measurement
   of the current range.
3. Use preflop action sequence only to *understand* how the
   composition triple was generated, never as a substitute for
   reading it. "BTN's preflop range excluded the premium 3-bet
   holdings" is information about the *generator*, not about the
   *current continuing range*.
4. The feature pipeline still exposes `villain_range_capped` — do
   NOT use it as a postflop strength signal. It encodes preflop
   action geometry only (it is `int(not is_3bet_pot and
   villain_is_defender)`, a pure binary for "villain was the
   preflop caller in a non-3-bet pot"). See
   `river-rats-core/feature_extractor.py:1195-1197` and
   `knowledge/three_way_gto.md` Section 1.9 / DO NOT Rule #8.
5. When equity exceeds pot odds by ≥20 percentage points AND
   hero holds a made hand that dominates some portion of the
   triple's remainder, default to CALL facing bet+call. Reserve
   "bet+call = fold" for composition-supported cases: hero's
   hand is dominated AND `villain_top_pair_plus_pct` is in the
   ≥60% "heavy with strong hands" bucket.

**References.** `river-rats-v2/knowledge/three_way_gto.md` (v1.3)
Section 1.9, Factor 3, DO NOT Rule #8, Examples 3 and 6.
`river-rats-v2/river-rats-core/feature_extractor.py:1195-1197`.
`feedback_solver_findings.md` findings 3 / 6 / 7.
`reference_corrections.md` MW-30 and MW-46.
```

**MEMORY.md index line to add** (one-line pointer, insert in
feedback section of
`/home/rupertbeytell/.claude/projects/-home-rupertbeytell/memory/MEMORY.md`):

```markdown
- [feedback_preflop_geometry_vs_postflop_composition.md](feedback_preflop_geometry_vs_postflop_composition.md) — Reason postflop strength from the TP+/draws/air composition triple, not from preflop range construction labels; MW-30 over-fold generalisation
```

## Section 13 — Outstanding questions or blocks

**No blocks.** All real feature values required for Sections 5 and
6 were successfully obtained:

- MW-30: pulled directly from
  `river-rats-v2/review/all_557_situations.jsonl` line 120
  (situation id `CALL_Board5_KdJc6s_h5`, `_hero_cards = "KcTh"`,
  `_board_cards = [Kd, Jc, 6s]`). All composition triple values,
  equity, pot odds, and worse_hand_pct are literal JSONL field
  values — no placeholders.
- Example 6: computed live via
  `river-rats-v2/river-rats-core/feature_extractor.py` using the
  documented gauntlet schema (`h = "QsJd"`, `b = "Qc8d3s"`,
  `pos = "SB"`, `vp = "BTN"`, `fb = 0`, `st = "f"`, `pot = 90`,
  `tc = 0`, `_opener_position = "BTN"`,
  `villain_aggression_count = 1`, `_num_opponents = 2`). Output
  captured in this session. All values in Section 6 are literal
  extractor output — no placeholders.

All file paths and line numbers in this plan were verified in this
session via `Read` or `Grep` (per S1). Specifically:

- `feature_extractor.py:1185-1197` — verified by Read (offset 1180,
  limit 30), formula text literal-quoted in Section 11 reply memo.
- `review/all_557_situations.jsonl` line 120 — verified by grep
  for `KdJc6s` and read of the full row.
- `knowledge/three_way_gto.md` line counts for the 19 "cap"
  occurrences — verified by Grep with `\bcapped\b|\buncapped\b`
  and literal `villain_range_capped` + `range capped`.
- `l3_renderer.py` `_villain_range_sentence` at line 317+ — read
  (offset 300, limit 120), bucket thresholds captured.
- Reference corrections and solver findings — read from memory
  files (flagged as 3-day-old point-in-time observations; content
  still matches the v1.2 KB's existing solver correction paragraph
  at lines 225-252 and 367-377, so no drift detected).

No outstanding questions for the owner. No technical forks escalated
(S2 compliance: teaching buckets adopted as provisional with
calibration TODO, not put as an open question).

---

**End of edit plan.** Ready for reviewer re-review. On approval,
the architect agent will apply the edits from the literal
replacement text in Sections 2-9 of this plan.
