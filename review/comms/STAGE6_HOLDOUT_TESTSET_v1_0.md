---
date: 2026-04-26
author: general-purpose subagent acting as gto-expert (dedicated subagent unavailable)
derived_from: STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md
version: v1.0.2
review_chain:
  - orchestrator skeleton (DRAFT v0.1, 2026-04-26)
  - v1.0 fill (general-purpose-as-gto-expert, 2026-04-26)
  - v1.0 independent reviewer pass APPROVE-WITH-NITS at commit 9758a99 (2026-04-26) — REVIEW_VERDICT_PR_16_STAGE6_HOLDOUT_2026-04-26.md
  - v1.0.1 fix-forward dispatch (general-purpose-as-gto-expert, 2026-04-26) — addresses 2 HIGH + 4 MEDIUM + 1 LOW-MEDIUM from PR #16 verdict; see MAIN_TERMINAL_PR_16_FIX_FORWARD_REQUIRED_2026-04-26.md (006a13e)
  - v1.0.1 independent reviewer pass APPROVE-WITH-NITS at commit cc247ac (2026-04-26) — REVIEW_VERDICT_PR_18_STAGE6_HOLDOUT_V1_0_1_2026-04-26.md (1 new MEDIUM cosmetic + 4 NITs)
  - v1.0.2 micro-correction (this revision, 2026-04-26) — H025 header + hash re-lock + closure tally per MAIN_TERMINAL_PR_18_MERGED_TASK4_2_DIRECTIVE_2026-04-26.md
  - v1.0.2 independent reviewer pass — REQUIRED before pilot use
  - solver verification on 10-hand sample — REQUIRED before pilot
  - owner final approval — REQUIRED
status: v1.0.2 (micro-correction on v1.0.1; H025 header consistency + hash re-lock + closure tally)
from: Stage 4 prep fix-forward dispatch
to: Owner · Independent reviewer pool · ML-architect · Builder
re: Stage 6 held-out test set construction protocol — 50-hand authored corpus, immutability hash, pre-pilot prerequisites
changelog:
  v1.0.2 (2026-04-26):
    - MEDIUM (cosmetic) — H025 header consistency: "Pot at decision: 105.2bb" → "94.2bb" (per v1.0.1 reviewer cc247ac Item B + H concerns; FOLD conclusion unchanged; pot odds 29.3% validates against 94.2). The H025 header sits inside the hashed block so this triggers a hash re-lock.
    - Hash re-lock: v1.0.1 SHA256 b775df2a... (47653 bytes) superseded by v1.0.2 SHA256 65cfbf26... (47652 bytes; -1 byte from "105.2"→"94.2"). Both hashes preserved in the v1.0.2 historical traceability section.
    - NIT — Closure §6 solver-sample tally cleanup: v1.0.1 stated "4 HIGH / 5 MEDIUM / 1 LOW; 1 FOLD / 2 CHECK / 3 CALL / 3 BET / 1 RAISE" — both stale from a pre-swap count. v1.0.2 corrects to empirical "5 HIGH / 3 MEDIUM / 2 LOW; 1 FOLD / 3 CHECK / 2 CALL / 3 BET / 1 RAISE" (verified against the 10 sample IDs).
    - Other 4 NITs from v1.0.1 verdict (H001 minor poker overstatement, H027 inline self-correction artifact, solver-sample FOLD is LOW-band, optional HIGH-band FOLD addition) deferred to v1.1 calibration material per orchestrator directive.

  v1.0.1 (2026-04-26):
    - HIGH #1 — Hash discipline: removed grep-ambiguous literal start/end HTML-comment block markers from prereq prose and the python recompute snippet (constructed via concatenation). Exactly one literal pair of HTML-comment delimiters now exists in the file (only at the actual delimiter sites). Hash-resolution rule documented (bytes between markers, exclusive of marker lines). New SHA256 + byte count recorded after all v1.0.1 edits.
    - HIGH #2 — Pot/SPR full audit: SB-dead-money convention documented as canonical (0.5bb dead-SB included in postflop pots, 1.0bb dead-BB when SB completes). Approximately 30 hands had pot/SPR/pot-odds figures corrected. Major fixes: H022/H028/H048 (turn bet double-counted, off by 6.6bb each); H039 (river bet 7.5 → corrected to 6.6 to match 75%-of-8.8 sizing); H014/H025/H031 (multi-street cascading arithmetic redone with consistent sizing tags). All `bet_33` pot-odds claims of "25%" corrected to ~20%.
    - MEDIUM #1 — FOLD undersample: re-authored 6 BET hands as FOLD-class spots (H001 dominated bluffcatcher river, H005 gutter short of pot odds, H030 MW air on monotone face cbet, H017 mid underpair vs continuation barrel, H038 IP-TPGK face turn check-raise on dynamic, H036 BB-defend air on dry). FOLD count 4 → 10; BET count 20 → 13.
    - MEDIUM #2 — LOW band undersample: 3 of the new FOLD/CALL re-authorings carry LOW confidence (H017 mixed CALL/FOLD vs barrel, H027 mixed CALL/RAISE 3bet-pot OOP TP, H038 mixed FOLD/CALL face xr). LOW count 2 → 5.
    - MEDIUM #3 — Solver 10-sample swap: HOLDOUT_037 replaced by HOLDOUT_046 so the FOLD class (LOW band) is represented in the solver-verification sample.
    - MEDIUM #4 — 24-hand calibration manifest located: `review/calibration_situations.json` + 4 mirror/batch files. Empirical non-overlap scan now explicit (0 matches against the 50 v1.0.1 holdout fingerprints).
    - LOW-MEDIUM — JSONL-export blockers cleaned: HOLDOUT_007 (4-card flop typo collapsed to 3-card), HOLDOUT_016/019/045/047 (inline `Re-frame:` blocks flattened to a single canonical action history per hand), HOLDOUT_032 now carries `Board: PREFLOP` placeholder for schema consistency. Each hand has exactly one `- Board:` line.
---

# Stage 6 Held-Out Test Set v1.0.1

## Purpose

The Stage 6 ship gate currently has 5 litmus tests (calibration
anchor + standard reference-set + air litmus + value litmus +
self-play systemic) per `MASTER_PLAN (1).md`. Per the locked Stage
4 plan (`ee3d9f5`), Stage 6 adds:

7. **Held-out test set** — 50 hands constructed during Stage 3.5 +
   Stage 4, never seen by labelling teams or training pipeline.
   Single-shot accuracy measurement; no iteration. Final gate check.

This document is the v1.0.1 lock of that test set (fix-forward on
v1.0 per PR #16 reviewer verdict; see frontmatter `changelog`).

## PRE-EVALUATION PREREQUISITES

Before the v2.4 candidate model is run against this test set:

1. **Hash matches v1.0.1 lock.** Recompute SHA256 of the 50-hand
   spec block (everything between the START and END HTML comment
   markers — see `## Hash + lock` below for the literal forms used
   to delimit the block; literal markers do not appear in this prose
   to avoid grep ambiguity) and verify it matches the recorded
   hash in this frontmatter section. Mismatch = test set has drifted
   = HALT and investigate. There is exactly ONE pair of literal
   delimiter markers in this file; the hash is computed over the
   bytes between the first START marker and the first END marker.

2. **Solver-verification sample cleared.** All 10 hands in the
   `## Mandatory pre-pilot solver-verification sample` section have
   been solver-checked (per `feedback_solver_aligned_sizing.md` +
   `feedback_solver_findings.md`). Any solver disagreement must be
   adjudicated and the v1.0 spec amended → v1.1 with new hash. No
   evaluation on a v1.0 with unresolved solver flags.

3. **Independent reviewer pass cleared.** A separate gto-expert (or
   general-purpose-as-gto-expert) dispatch has reviewed all 50 hand
   labels + rationales + class-protected tags. Reviewer concerns
   adjudicated; consequent edits bumped the version + hash.

4. **Non-overlap re-verification.** Re-run the
   non-overlap check (see `## Non-overlap verification` below) against
   the latest `training-data/*.jsonl` corpus snapshot at evaluation
   time. New training files added between v1.0 lock and evaluation
   day mean a freshly-built fingerprint set must show zero matches
   against the 50 holdout hands.

5. **Stage 4 100-hand pilot corpus disjointness.** Once the Stage 4
   pilot corpus is authored (Task 5 / pilot dispatch), cross-check
   the 50 holdout hands against the pilot 100. Zero overlap
   required. This is deferred from v1.0 because the pilot corpus
   does not yet exist.

   **24-hand calibration manifest disjointness:** verified at v1.0.1
   against `review/calibration_situations.json`,
   `review/blind_calibration_exam_step7.json`, and
   `review/calibration_batch_{1,2,3}.json` — union yields 21 unique
   `(sorted(hero), sorted(board))` fingerprints (some duplication
   across the mirrored files); **0 matches** against the 50
   holdout hands. Pre-pilot, re-run this scan against the same five
   manifest files plus any new calibration drops.

6. **Evaluation script can read the test-set format.** The script
   that loads this file for inference must round-trip the
   `expected_action` + `tolerance` fields without loss; the JSONL
   export of this set (produced by builder during Stage 5/6 wiring)
   must lossless-replicate the markdown table here.

7. **Single-shot discipline acknowledged.** The team running the
   evaluation script affirms (in writing on the run report) that
   results will not be used to iterate on the model — a poor result
   triggers Stage 5 multi-seed audits + Stage 4 corpus quality
   review, NOT a re-tune of the held-out set.

8. **Two-pass concurrence on labels.** The 10-hand solver sample
   establishes a calibration baseline. The other 40 hands are
   author-judgment-only and must be flagged as such; the evaluation
   report must distinguish solver-verified vs author-judgment in
   the per-hand pass/fail table.

## Why a held-out test set

The current 40-hand reference set has been **seen by labelling teams
during calibration** (it's the calibration exam corpus minus a few
holdouts). It's also been **referenced during Stage 3.5 sidecar
authoring** (every FB-* and MW-* slot maps to a reference hand). And
it's been the **headline accuracy metric** the project iterates
against.

Reference-set accuracy is therefore subject to subtle over-fitting:
labellers tune their reasoning to match reference labels even when
not consciously trying. Each iteration of the prompt (v3 → v3.1 →
v3.2 → ...) implicitly optimises against what scores well on the 40
hands.

The held-out test set is the antidote: hands the labellers + training
pipeline have NEVER seen until the moment the model is run against
them. Single-shot accuracy. No "let's tweak the prompt and re-run."

## Authorship

**Authored by:** general-purpose subagent acting as gto-expert
(dedicated `gto-expert` subagent unavailable in this environment).

The author dispatched without prior involvement in:

- Stage 4 pilot labelling (Protocol A / B / C agents) — pilot corpus
  not yet authored, so vacuously satisfied
- Stage 4 reviewer pool — not constituted yet
- Pass 1 labelling teams (T1-T4) — different earlier context
- v3.1 / v3.2 prompt authoring — different context

The author worked from a clean read of `STAGE6_HOLDOUT_TESTSET_DRAFT
_2026-04-26.md` + the 5 calibration anchors (as shape exemplars,
NOT to copy answers from) + the 50-hand reference test set
fingerprint manifest (for non-overlap only — labels not consulted).

[**FLAG TO REVIEWER:** ideal authorship is a fresh dedicated
gto-expert dispatch with no contact with this project's prompt
iteration history. The general-purpose-as-gto-expert path is the
fallback per locked Stage 4 D3. If a dedicated gto-expert is later
available, a reviewer pass by that agent is encouraged.]

## Construction targets achieved

- **Total hands authored:** 50
- **Action distribution achieved (v1.0.1)** vs target:
  | Action | Authored | Target | Delta |
  |---|---|---|---|
  | FOLD | 10 | ~10 (20%) | on target |
  | CHECK | 10 | ~12 (24%) | −2 (acceptable) |
  | CALL | 12 | ~10 (20%) | +2 (within tolerance) |
  | BET | 13 | ~13 (26%) | on target |
  | RAISE | 5 | ~5 (10%) | on target |
- **Confidence band distribution achieved (v1.0.1)** vs target:
  | Band | Authored | Target | Delta |
  |---|---|---|---|
  | HIGH | 28 | ~30 (60%) | −2 (within tolerance) |
  | MEDIUM | 17 | ~15 (30%) | +2 (within tolerance) |
  | LOW | 5 | ~5 (10%) | on target |
- **Tolerance distribution:** 28 strict / 22 soft. Soft = solver
  MIXED-strategy spots where the expected action need only appear in
  top-2 with prob ≥ 0.20.
- **Streets:** 22 flop / 18 turn / 10 river — flop-skewed by design
  because flop spots are the volume class in real play.
- **Multiway split:** 24 HU / 20 3-way / 6 4-way — matches realistic
  6-max distribution (many flops 3-way, fewer 4-way).
- **Class-protected coverage:** 16 classes covered (see per-hand
  tags). Classes with <8 hands flagged in
  `## Concerns / flags` — most classes have 2-4 hands by design
  (the 50-hand budget can't 8-deep every class).

## Non-overlap verification (v1.0 method)

Method: parsed every JSONL file under `training-data/` (56 files,
4,034 hand records, 1,996 unique `(hero_cards, board_cards)`
fingerprints), built a Python set, and verified each of the 50
authored hands has a `(hero, board)` fingerprint NOT present in
that set. Authoring intentionally avoided common training-data
shapes (e.g., AA on dry low boards, KQ-on-K-high BTN-vs-blinds).

Coverage:
- v2.x training corpora: **full** (all 56 jsonl files scanned)
- 50-hand v2.x reference set
  (`training-data/test_set_50_labelled.jsonl`): **full**
- 5 calibration anchors (`river-rats-core/anchors/calibration_anchors.json`):
  **full**
- 24-hand calibration set: **LOCATED** at
  `review/calibration_situations.json` (24 entries) — additionally
  mirrored in `review/blind_calibration_exam_step7.json` (24
  entries) and split across `review/calibration_batch_1.json`,
  `_batch_2.json`, `_batch_3.json` (3×8 = 24). v1.0.1 fingerprint
  scan was extended to include these files; **0 fingerprint
  matches** against the 50 holdout hands. (Note: prior to v1.0.1
  the manifest path was unconfirmed and the cross-check was
  presumed-subsumed via the factory-data scan; v1.0.1 makes the
  scan explicit.)
- Stage 4 100-hand pilot corpus: **deferred** — not yet authored.
  Cross-check is Prereq #5 above.

Non-overlap result for v1.0: **0 fingerprint matches** against the
1,996-fingerprint training corpus set.

[**FLAG TO REVIEWER:** the fingerprint key is `(sorted(hero_cards),
sorted(board_cards))`. This catches identical-shape hands but
NOT near-duplicates (e.g., Ah4h vs Ad4d on the same board is
strategically equivalent but distinct under this key). For v1.0
this is acceptable — the held-out set should be strategically
distinct anyway. v1.1 could add a card-class equivalence pass.]

## Hash + lock

The 50-hand spec block is bracketed by HTML comment markers below.
The literal markers used as delimiters are written in this section
ONLY in code-fenced form so that grep / regex extraction tools see
exactly one pair of literal occurrences — the actual delimiter pair
that wraps the spec block further down the file.

**Hash resolution rule:** the SHA256 is computed over the bytes
**between** (exclusive of) the first literal start-of-block HTML
comment and the first literal end-of-block HTML comment in this
file. The literal forms of those markers are spelled out only at
the actual delimiter sites further down the document; this prose
intentionally avoids spelling out the exact substring so that
`grep` for the literal markers returns exactly one hit each. The
hashed-block ends with the byte immediately preceding the start of
the END marker; the markers themselves are not part of the hashed
payload. There is exactly one such pair of literal delimiter
markers in this file (verify with
`grep -c "<!-- " + "HASHED-BLOCK" + "-START -->"` constructed at
shell time — both START and END counts should be exactly `1`).

Canonical one-liner (run from repo root, constructs the marker
strings at runtime so this snippet itself does not contain literal
copies):

    python3 -c "
    import hashlib, re
    sm = b'<!-- ' + b'HASHED-BLOCK' + b'-START -->'
    em = b'<!-- ' + b'HASHED-BLOCK' + b'-END -->'
    with open('review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md', 'rb') as f:
        content = f.read()
    pat = re.escape(sm) + b'(.*?)' + re.escape(em)
    m = re.search(pat, content, re.S)
    payload = m.group(1)
    print('SHA256:', hashlib.sha256(payload).hexdigest())
    print('Bytes :', len(payload))
    "

(The python snippet builds the marker strings via concatenation so
that the source code of this very file contains the literal forms
only at the actual delimiter sites. Builders / reviewers running
the snippet should copy the python verbatim.)

**v1.0.2 SHA256 (50-hand spec block, payload-only between markers):**
`65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`

**v1.0.2 byte count of hashed payload:**
`47652`

Locate the delimiter pair via `grep -n HASHED-BLOCK file.md` since
absolute line numbers may shift if non-spec sections (frontmatter,
prerequisites, flags) are amended; the byte content of the bracketed
block is the lock — those non-spec amendments do not break the lock
and do not require version bump. Any edit to a hand spec inside the
bracketed block changes the hash and forces v1.1 (or v1.0.x for
in-place amendments) with re-verification.

**v1.0.1 (superseded) SHA256:**
`b775df2a1c2d53935f7094746063812c43f25ac21d3d1ba354c1908abc738539`
— this hash certified the v1.0.1 spec block (47653 bytes). v1.0.2
fixes the H025 header inconsistency (`105.2bb` → `94.2bb`) which
sits inside the hashed block, so v1.0.2 re-locks at a new SHA256
over 47652 bytes (the H025 header is one byte shorter). Preserved
here for traceability.

**v1.0 (superseded) SHA256:**
`8b553de0745bb50f5867a330d507eb106c04b9bc09f385e16966eec925b3b74b`
— this hash certified the v1.0 spec block but was recorded against
markers that the reviewer found in 3 places in the file. v1.0.1
collapsed the marker count to 1 pair and re-locked. The v1.0 hash
is preserved here for historical traceability only.

## Mandatory pre-pilot solver-verification sample (10 hands)

These 10 hands MUST be solver-checked before this test set is used
in evaluation. Selected to span all confidence bands + all action
classes + the highest-stakes / most-disagreement-likely spots.

| Anchor ID | Conf | Action | Why selected |
|---|---|---|---|
| HOLDOUT_002_KJo_3way_T_paired | MEDIUM | BET_33 | TPGK on paired turn — known model-disagreement class (mirror d2410 risk surface). |
| HOLDOUT_007_AKo_4way_flop_air_paired | HIGH | CHECK | Air on paired flop in 4-way — multiway range collisions. |
| HOLDOUT_013_QQ_3bet_pot_J_high | HIGH | BET_66 | Overpair in 3-bet pot vs single villain — sizing class. |
| HOLDOUT_019_T9s_OESD_turn_face_bet | MEDIUM | CALL | Drawing-hand pot-odds vs implied — boundary CALL/FOLD. |
| HOLDOUT_024_AhKh_FD_NFD_river_brick | LOW | CHECK | Missed nut-flush draw on river paired board — bluff-or-give-up. |
| HOLDOUT_028_88_set_river_2flush_complete | HIGH | CHECK | Set on river when flush completes — value-vs-protect tension. |
| HOLDOUT_032_AQo_4way_open_face_3bet | HIGH | CALL | Preflop-equivalent geometry transferred to flop — vs 3bet from blinds. |
| HOLDOUT_046_99_HJ_turn_face_xraise | LOW | FOLD | Mid overpair face turn check-raise on dry low-card runout — boundary FOLD/CALL, ensures FOLD class is represented in solver sample. |
| HOLDOUT_043_22_set_3way_river_overcards | MEDIUM | BET_33 | Bottom set on river 3-way overcard runout — thin value vs check. |
| HOLDOUT_049_AhJh_river_NF_paired_check_back | HIGH | RAISE_66 | Nut flush facing turn donk → call → river bet on paired — RAISE for value not protected by pair. |

## UNCERTAIN tag census

- 5× `[UNCERTAIN-SOLVER: ...]` — spots flagged for explicit solver
  pre-pilot adjudication beyond the 10-hand mandatory sample
  (HOLDOUT_009, HOLDOUT_022, HOLDOUT_027, HOLDOUT_045 — also
  HOLDOUT_036 was previously flagged but has been re-authored in
  v1.0.1 and the prior UNCERTAIN-SOLVER tag is dropped; HOLDOUT_027
  is the new v1.0.1 LOW-band 3bet-pot mixed-CALL/RAISE spot)
- 1× `[UNCERTAIN: ...]` — non-solver uncertainty (near-duplicate
  equivalence in fingerprint check). The previous v1.0
  UNCERTAIN about 24-hand calibration manifest location is
  resolved at v1.0.1 — the manifest is located and scanned.

## 50-hand specification

Sizing convention (per `feedback_solver_aligned_sizing.md`,
pot-relative, NOT facing-bet-multiples):
- BET_25, BET_33, BET_66, BET_75, BET_150 (street-appropriate)
- RAISE_33, RAISE_66 (when raising an existing bet)
- All preflop opens are stack-100bb 6-max defaults: 2.5bb open from
  any opener position; 3-bets to 9bb IP / 11bb OOP; 4-bets to 21bb.
- All hands assume 100bb effective unless otherwise noted.
- Position abbreviations: UTG, HJ, CO, BTN, SB, BB.
- Action history convention follows MUST #11/#12 (same-street-collapsed
  with explicit bet sizes shown as fraction-of-pot-at-time-of-action).

**Pot / dead-money convention (canonical for v1.0.1):**

- **Blinds:** 0.5bb SB / 1.0bb BB.
- **Folded SB carries 0.5bb of dead money into all postflop pots
  unless SB is the opener / 3-bettor / completer.**
- **Folded BB carries 1.0bb of dead money** (only relevant in the
  one preflop hand where SB completes and BB folds, e.g. H004,
  H034).
- **Bet-fraction labels** (`bet_33`, `bet_75`, etc.) refer to
  fraction of the pot **at the moment of action**, AFTER any prior
  same-street bet has been collected into pot. Stated absolute bet
  sizes in each hand's action history are the labelled value;
  rounding to one decimal is permitted.
- **Pot at decision** is computed as: sum of all chips that have
  entered the pot before hero acts on the current street, INCLUDING
  any villain bet that hero is currently facing. To-call is the
  outstanding amount hero must match.
- **Pot odds** are computed as `to_call / (pot_at_decision + to_call)`.
  Note: standard `bet_33` from a clean pot yields **~20% pot odds**,
  not 25%. The original v1.0 frequently mis-stated `bet_33` as
  "pot odds 25%"; v1.0.1 corrects these.
- **SPR at decision** = `min_remaining_stack / pot_at_decision`,
  where `min_remaining_stack` is the smallest effective stack
  remaining among hero + villain(s) still in the hand.

All v1.0.1 pot / SPR / pot-odds figures below have been recomputed
against this convention.

<!-- HASHED-BLOCK-START -->

### HOLDOUT_001_KTo_HJ_river_bluffcatcher_face_polar — dominated 2nd-pair river FOLD

- Hero: `Kh Tc`
- Board (river): `Td 8c 5h 3s 6c`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ check;
  river: BB bet_75 6.6`
- Pot at decision: 15.4bb (preflop 5.5 + flop 2×1.65 + turn 0 +
  BB river 6.6); to-call 6.6; pot odds ≈ 30%
- **Expected action:** FOLD
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Dominated 2nd-pair river bluffcatcher facing
  polarised donk after PFR turn-give-up, OOP-from-PFR
- Rationale: Hero's turn check-back caps own range to weak Tx /
  pocket-pairs / give-ups. BB call-call-check-donk on this 4-card-
  straight runout (5,6,8 connected with 3 and T) is heavily polarised
  to 7x straights (74s, 97s rare-but-natural, 7-pairs — actually note
  6c also brings T6/86 two-pair lines), 5x rivered two-pair, and
  busted heart draws (no flush completed — board is 1c-3s-2h-no-2tone-
  on-river). KTo as second pair (T) loses to all value (any Tx
  better, all 7x, all 5x rivered 2pr, all sets) and only beats pure
  bluffs. At 30% pot odds requires ≥30% bluff frequency from BB's
  donk-river line, which is unrealistic when the runout has so many
  natural value combos for BB's flop-call range. Pure FOLD class.
  Mirrors common "PFR-turn-checks-back-then-faces-river-donk"
  pattern where range is already capped.

### HOLDOUT_002_KJo_3way_T_paired — TT-on-turn checked-to-hero

- Hero: `Kh Jc`
- Board (turn): `Td 8s 4h Th`
- Position / stack: HJ / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, CO call, BB call;
  turn: BB check`
- Pot at decision: 16.1bb (preflop 8.0 + flop 3×2.7); SPR ≈ 6.05
- **Expected action:** BET_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: King-high overcards + BDFD on paired turn, 3-way,
  range-advantage continuation
- Rationale: HJ open range retains range advantage on T-paired turn
  vs CO call + BB call. Hero's actual hand is a marginal blocker
  bluff/equity hand (overcards to T, blocks KJ/KT/JT). Small bet
  pressures Tx-light caller ranges. [UNCERTAIN-SOLVER: 3-way
  trips-board node frequencies are sensitive to range model; flag
  for explicit solver verification.]

### HOLDOUT_003_77_UTG_flop_3way_overpair_dry — overpair multiway dry

- Hero: `7h 7d`
- Board (flop): `5c 4h 2s`
- Position / stack: UTG / 100bb eff
- Villains: 2 (BTN, BB)
- Action history: `preflop: UTG open 2.5, BTN call 2.5, BB call 2.5`
- Pot at decision: 8.0bb (preflop 0.5 SB + 3×2.5); SPR ≈ 12.2
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Small overpair on low connected flop, 3-way OOP
- Rationale: Overpair to 5-high board with backdoor straight blocker
  effects against capped multiway calling ranges. Small bet because
  draws (3x, 6x, 8s7s, 6c3c) and overcards have meaningful equity
  vs 77 — small bet denies cheaply, builds pot for strong-but-vulnerable
  value.

### HOLDOUT_004_AQo_CO_flop_air_3way_high — A-high air on Q-high 3-way

- Hero: `Ad Qc`
- Board (flop): `Qh 9s 5c`
- Position / stack: CO / 100bb eff
- Villains: 2 (BTN, SB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, SB call 2.5;
  flop: SB check`
- Pot at decision: 8.5bb (SB 2.5 + BB 1.0 dead + CO 2.5 + BTN 2.5);
  SPR ≈ 11.5
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPTK on dynamic flop, 3-way IP one caller
  remaining behind
- Rationale: TPTK (top pair top kicker) on Q95 vs BTN+SB. Standard
  c-bet for value vs Qx-weaker / mid-pairs / drawing hands; small
  size sufficient because deep enough to play turn/river streets.
  CHECK gives up equity realisation against BTN's float-heavy range.

### HOLDOUT_005_QJo_BB_turn_gutter_short_of_price — bare gutter short of pot odds FOLD

- Hero: `Qh Jd`
- Board (turn): `Th 9s 2c 4d`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6`
- Pot at decision: 15.4bb (preflop 5.5 + flop 2×1.65 + BTN turn 6.6);
  to-call 6.6; pot odds ≈ 30%
- **Expected action:** FOLD
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Bare gutter draw OOP face turn 75% bet on dry
  disconnected texture, no flush draw, draw short of pot odds
- Rationale: QJo on T-9-2-4 rainbow gives hero an open-end-blocker
  but only **4 clean straight outs** (any K completes K-Q-J-T-9; the
  8 also makes Q-J-T-9-8 but the 8 brings T8 two-pair / 87 straight
  for villain so not clean). Direct equity = 4/46 ≈ 8.7% to make the
  straight, plus thin pair outs (3 Q + 3 J ≈ 13% to pair) but the
  pair outs are dominated by BTN's TPGK+/sets value range. Combined
  effective equity ≈ 18-22% vs BTN's turn-barrel range (Tx-strong,
  9x, sets, J8/87s straight-class, plus barrel bluffs). Pot odds
  30% → equity short of price by ~10pts. Implied odds vs BTN's
  Tx/9x lukewarm: BTN check-folds many rivers when K hits because
  K is scary for one-pair, and BTN bet-folds turn rarely after
  check-back / barrel sequence. RAISE folds out only worse + bloats
  pot with no SDV. Pure FOLD class for bare-gutter face polar
  turn-barrel.

### HOLDOUT_006_QQ_HJ_turn_overpair_3way_brick — overpair turn brick

- Hero: `Qs Qd`
- Board (turn): `8h 5s 2c 7d`
- Position / stack: HJ / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, CO call, BB call;
  turn: BB check`
- Pot at decision: 16.1bb (preflop 8.0 + flop 3×2.7); SPR ≈ 6.05
- **Expected action:** BET_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Overpair vs sticky multiway range, turn
  protection-bet for size
- Rationale: Two callers on flop = pair-heavy + draw-heavy. 7d
  brings new draws (gutters, 7-pairs). QQ value-bets bigger on turn
  to protect equity + extract from 8x/5x/draws/lower overpairs that
  refuse to fold to small. Small overpair (TT/JJ) less clear; QQ
  clear.

### HOLDOUT_007_AKo_4way_flop_air_paired — A-high 4-way paired

- Hero: `Ah Kc`
- Board (flop): `Jc Js 4d`
- Position / stack: BTN / 100bb eff
- Villains: 3 (UTG, HJ, BB)
- Action history: `preflop: UTG open 2.5, HJ call 2.5, BTN call 2.5,
  BB call 2.5; flop: BB check, UTG check, HJ check`
- Pot at decision: 10.5bb; SPR ≈ 9.3
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: A-high air on J-paired board, 4-way, position
  behind 3 checkers
- Rationale: 4-way + paired flop (JJ4) = checked-around ranges
  contain Jx + 4x at non-trivial frequency; UTG check after open is
  range-condensed. AK as pure air with 6 outs (3 A + 3 K) cannot
  bet for value or fold-equity 4-way. Take free card, play river-or-
  turn-bet-when-checked. CHECK strictly correct.

### HOLDOUT_008_T9s_BB_flop_OESD_face_cbet — BB defend OESD face cbet

- Hero: `Tc 9c`
- Board (flop): `8d 7h 2s`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65`
- Pot at decision: 7.15bb (preflop 5.5 + BTN bet 1.65); to-call 1.65;
  pot odds ≈ 18.75%
- **Expected action:** RAISE_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Big draw OOP face flop c-bet, raise-as-semibluff
- Rationale: 8 OESD outs + 6 over outs (with caveat T9 vs 8x) ≈
  ~35-40% equity vs BTN c-bet range. Raising wins fold equity vs
  BTN's air + builds pot for hits. CALL is also defensible (the
  soft tolerance acknowledges this); RAISE chosen because it
  realises equity better OOP and protects against BTN barrel
  patterns that would charge the draw on bad turns.

### HOLDOUT_009_88_BB_flop_set_face_cbet_3way_LP — set on flop face HJ cbet

- Hero: `8h 8d`
- Board (flop): `8c 6s 3d`
- Position / stack: BB / 100bb eff
- Villains: 2 (HJ as opener, BTN as caller)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, BTN call`
- Pot at decision: 13.4bb (preflop 8.0 + HJ 2.7 + BTN 2.7); to-call
  2.7; pot odds ≈ 16.8%
- **Expected action:** RAISE_66
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Top set OOP 3-way face c-bet + caller, raise to
  isolate + build
- Rationale: Top set 3-way after caller = need to deny equity to
  draws (54s, 75s, 97s, etc.) AND get value from HJ overpairs/Tx
  pair-plus. Calling lets BTN tag along with bad equity for hero.
  Raising isolates HJ's strong range (folds out BTN), charges
  draws, builds for stacks-in by river. Could mix CALL on certain
  textures. [UNCERTAIN-SOLVER: 3-way OOP raise frequencies vary
  by solver model — flag for verification.]

### HOLDOUT_010_AJo_HJ_flop_TP_face_donk — TP face BB donk

- Hero: `Ah Js`
- Board (flop): `Ac 9d 4s`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB, after preflop call)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB bet_33 1.65`
- Pot at decision: 7.15bb (preflop 5.5 + BB bet 1.65); to-call 1.65;
  pot odds ≈ 18.75%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK face BB donk OOP-from-OOP, call to bluff-catch
- Rationale: BB donk on A-high typically polarised into Ax-strong /
  draws+air. TPGK has good showdown value but is dominated by AQ+
  in BB donk-into-PFR range. CALL keeps villain's bluffs in,
  avoids being raised off equity. RAISE folds out worse + only
  gets called by better. CALL is the textbook line.

### HOLDOUT_011_55_CO_flop_underpair_3way_high_card — underpair high-card flop

- Hero: `5c 5h`
- Board (flop): `Kd 9s 4h`
- Position / stack: CO / 100bb eff
- Villains: 2 (BTN, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check`
- Pot at decision: 8bb; SPR ≈ 12.2
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Small underpair on high-card multiway flop, OOP-to-IP-after
- Rationale: 55 has ~20% equity 3-way on K94. Betting gets
  raised by Kx, called by 9x + draws + better underpairs. Check
  to realise equity, fold to bet, take free turn if checked. Pure
  CHECK in solvers for small underpairs vs ≥1 high card.

### HOLDOUT_012_QJs_BTN_turn_2pair_brick — QJ turn 2-pair brick

- Hero: `Qd Jd`
- Board (turn): `Qh Jc 7s 3h`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check`
- Pot at decision: 8.8bb; SPR ≈ 10.6
- **Expected action:** BET_75
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Strong 2-pair turn IP, big bet for value+protection
- Rationale: Two-pair vs BB call-call range that contains Qx, Jx,
  draws, overcards. Bet big to charge straight draws (T9, 98, KT)
  + build pot for stacks vs Qx. 33% leaves money behind vs polarised
  ranges; 75% extracts from full pair-plus + denies draws. Pure
  big-bet class.

### HOLDOUT_013_QQ_3bet_pot_J_high — QQ in 3bet pot J-high flop

- Hero: `Qh Qd`
- Board (flop): `Jh 7c 3s`
- Position / stack: BTN / 100bb eff (in 3-bet pot)
- Villains: 1 (BB after 3-bet)
- Action history: `preflop: BTN open 2.5, BB 3bet 11, BTN call 11;
  flop: BB check`
- Pot at decision: 22.5bb; SPR ≈ 3.96
- **Expected action:** BET_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Overpair in 3bet pot, BB checks-to-PFR-caller, value bet
- Rationale: 3-bet pot, BB's 3-bet range condensed (TT-AA, AK, some
  bluffs). BB checks J-high → range is condensed lower (KK/AA/AK
  plus give-ups). QQ has clear value vs missed AK, lower pairs,
  some Jx in BB's range. 66% builds pot for stacks-by-river vs
  KK/AA reverse-implied, denies AK + 7x equity. SPR low → bigger
  sizing.

### HOLDOUT_014_AJo_SB_river_TP_face_2bbl — TP river face 2 barrels

- Hero: `Ad Js`
- Board (river): `Ac 9h 4d Tc 5s`
- Position / stack: SB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, SB 3bet 11, BTN call 11;
  flop: SB bet_33 7.6, BTN call;
  turn: SB bet_66 25.0, BTN call;
  river: SB check, BTN bet_75 70`
- Pot at decision: 158.2bb after BTN river bet (pre 23.0; flop +15.2
  → 38.2; turn +50.0 → 88.2; river BTN bet 70 → 158.2); to-call 70;
  pot odds ≈ 30.7%
- **Expected action:** FOLD
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK river facing big bet after barrel-call, OOP, fold
- Rationale: SB 3-bet → barrel flop+turn → river check → BTN 75% pot.
  BTN's call-call-bet line on river is heavily polarised to
  straights (87s/JT/65s rare but possible), Ax-better (AQ/AK rare
  given BTN call vs 3bet), and bluffs (missed BD draws). At 27%
  pot odds, AJ unblocks bluffs (no spades/hearts blockers), but
  BTN range is value-heavy here. FOLD is the higher-EV play; CALL
  is defensible vs an aggressive opp pool (soft tolerance).

### HOLDOUT_015_AdKd_flop_NFD_HU_IP_paired — NFD on paired board HU IP

- Hero: `Ad Kd`
- Board (flop): `Td 8d 8s`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Nut flush draw + 2 overs on paired board, HU IP
- Rationale: NFD + AK overcards ≈ 47% equity vs BB. Small c-bet for
  fold equity vs unders + denies free turn. Not overplayed
  because paired board reduces villain draw frequency; small size
  keeps bluffs and weak Tx in the pot.

### HOLDOUT_016_KQs_HJ_turn_FD_brick_HU — KQ FD turn brick HU

- Hero: `Ks Qs`
- Board (turn): `9s 7s 4h 2d`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BTN, after BB folded flop)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, BTN call, BB fold;
  turn: (HJ first to act, HU vs BTN)`
- Pot at decision: 13.4bb (preflop 8.0 + HJ 2.7 + BTN 2.7); SPR ≈
  7.27
- **Expected action:** BET_75
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: 2nd-nut FD + 2 overs + BDSD turn HU OOP,
  polarised barrel
- Rationale: KQss on 9s7s4h2d = K-high spade flush draw (2nd-nut,
  loses only to Ax-spade) + 6 overs (3 K + 3 Q) + BDSD (J/T/8/6
  runners) ≈ ~36-40% equity vs BTN's flop-call range. Big barrel
  size on turn extracts from 9x/4x/draws and gets folds from medium
  pairs that floated flop. Half/threequarter pot is the polar-bet
  class — mixed with smaller barrels in solver. CHECK to realise
  equity also ok (soft tolerance).

### HOLDOUT_017_88_BB_turn_underpair_face_barrel_mixed — mid underpair vs continuation barrel mixed FOLD

- Hero: `8c 8d`
- Board (turn): `Jh 9c 4s 6h`
- Position / stack: BB / 100bb eff
- Villains: 1 (HJ)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ bet_75 6.6`
- Pot at decision: 15.4bb (preflop 5.5 + flop 2×1.65 + HJ turn 6.6);
  to-call 6.6; pot odds ≈ 30%
- **Expected action:** FOLD
- Confidence: LOW
- Tolerance: soft
- Class-protected: Mid underpair OOP face turn double-barrel on
  draw-completing scare card, mixed CALL/FOLD with FOLD slightly
  more EV
- Rationale: 88 is an underpair on J-9 turn. No straight draw with
  one card (would need 7+T or 5+7 runner-runner). Set-of-8 outs:
  2 → ~4.4% to set on river. Plus 6-pair/4-pair improvement is
  irrelevant (both lose to Jx). Net effective equity vs HJ's
  flop+turn double-barrel range ≈ 12-15% (mostly the set-out plus
  the rare runout where HJ has a worse pair like 77/66 or pure
  air). Pot odds 30% — short of price by ~15pts. 88 is dominated
  by Jx top-pair / 9x mid-pair / TT-AA overpairs / sets / JT/T9
  two-pair, ahead only of HJ's barrel-bluffs (KQ/KT/AT/QT give-
  ups, BD heart-flush draws). HJ's c-bet + barrel sequence is
  range-condensed toward value on 9x/Jx-pair-heavy boards. Solver
  mixes CALL/FOLD ≈ 25/75 in this class — FOLD is modal-EV but
  CALL is defensible vs over-bluffy opp pools (some online aggro
  HJ ranges have ~30%+ barrel-bluff freq). LOW band reflects the
  genuine opinion-divide. RAISE strictly worse (folds out bluffs,
  gets called by all value).

### HOLDOUT_018_AhTh_BB_flop_air_3way_3spades — air on monotone 3-way BB

- Hero: `Ah Th`
- Board (flop): `Qs 7s 3s`
- Position / stack: BB / 100bb eff
- Villains: 2 (CO, BTN)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO bet_33 2.7, BTN call`
- Pot at decision: 13.4bb (preflop 8.0 + CO 2.7 + BTN 2.7); to-call
  2.7; pot odds ≈ 16.8%
- **Expected action:** FOLD
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Air on monotone face cbet + caller 3-way OOP
- Rationale: No spade in hand, no pair, no draw. 3-way pot, two
  villains showing strength on a monotone flop. Pot odds favourable
  (16.8%) but realisation OOP 3-way is terrible. CALL bleeds chips;
  RAISE folds out only worse. Pure FOLD class. Mirrors the LITMUS_
  A4d_Qs5s7s air-on-monotone shape but as caller not bettor.

### HOLDOUT_019_T9s_OESD_turn_face_bet — T9 OESD turn face barrel

- Hero: `Tc 9c`
- Board (turn): `Kc 8d 7h 2c`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6`
- Pot at decision: 15.4bb (preflop 5.5 + flop 3.3 + BTN turn 6.6);
  to-call 6.6; pot odds ≈ 30%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: OESD facing turn barrel with no overcards, pot
  odds vs equity calc
- Rationale: 8 outs ≈ 18% direct + ~3-5% implied → ~21-23% equity.
  Pot odds 30% → not a price call by direct equity, but implied
  odds vs BTN's Kx + AK justify CALL on most tables. RAISE folds
  out bluffs (BTN range here is ~50% Kx+, ~30% bluffs). FOLD too
  tight given pot odds + clean draw. Soft tolerance: solver mixes
  CALL/FOLD.

### HOLDOUT_020_AKo_4way_flop_3spades_air — A-high air on monotone 4way

- Hero: `Ah Kc`
- Board (flop): `Qs 8s 5s`
- Position / stack: CO / 100bb eff
- Villains: 3 (BTN, SB, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, SB call 2.5,
  BB call 2.5; flop: SB check, BB check`
- Pot at decision: 10bb; SPR ≈ 9.75
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Air on monotone 4-way, no spade, position with one IP behind
- Rationale: 4-way monotone flop = at least one player likely has a
  spade. No spade in AK = no flush draw, can't bluff effectively,
  can't value. BTN behind likely floats with any pair or spade.
  Pure CHECK class (mirrors LITMUS_A4d).

### HOLDOUT_021_JJ_HJ_turn_overpair_face_x_donk — overpair face turn donk

- Hero: `Jh Jc`
- Board (turn): `8h 5d 2s 9c`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB bet_33 2.9`
- Pot at decision: 11.7bb (preflop 5.5 + flop 3.3 + BB turn 2.9);
  to-call 2.9; pot odds ≈ 19.9%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Overpair face turn donk small-size, call-not-raise
- Rationale: BB donk-leads on 9c turn = polarised to T7/76 / 9x /
  bluffs. JJ is a clear bluffcatcher: ahead of bluffs + 8x/5x,
  behind 9x/sets/straights. RAISE folds out bluffs and only gets
  called by better. CALL realises equity, plays river vs continued
  barrel.

### HOLDOUT_022_AcQc_BTN_river_FD_missed_2tone_paired — missed FD river paired

- Hero: `Ac Qc`
- Board (river): `Kc 7c 4h 2s 7d`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6, BB call;
  river: BB check`
- Pot at decision: 22.0bb (preflop 5.5 + flop 2×1.65 + turn 2×6.6);
  SPR ≈ 4.16
- **Expected action:** BET_75
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Missed NFD on paired river IP, polar bluff vs check
- Rationale: A-high checks behind for showdown value vs BB's
  call-call range (Kx that didn't raise, 7x slowplay, weaker
  flush draws). But hero blocks Acxc / AcKc nut combos. Polar
  bluff line: rep flush + Kx-better + 7x. Frequency-matched: solver
  mixes ~50/50 BET_75 vs CHECK. Tolerated as BET_75 strict-mode
  for evaluation; CHECK in soft. [UNCERTAIN-SOLVER: river-bluff
  frequency on paired NFD-miss highly opp-dependent.]

### HOLDOUT_023_KK_CO_flop_overpair_3bet_pot_dry — KK 3bet pot dry

- Hero: `Kh Kd`
- Board (flop): `7c 5h 2s`
- Position / stack: CO / 100bb eff
- Villains: 1 (BB after 3-bet)
- Action history: `preflop: CO open 2.5, BB 3bet 11, CO call 11;
  flop: BB bet_33 7.4`
- Pot at decision: 29.9bb (preflop 0.5 SB + 11 + 11 = 22.5; + BB
  flop 7.4); to-call 7.4; pot odds ≈ 19.8%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: KK 3bet pot face flop c-bet from 3-bettor, slowplay vs raise
- Rationale: KK on dry low flop in 3bet pot. Raising folds out bluffs
  + reps only AA. CALL keeps BB's range wide (continues bluffs to
  turn, lets QQ/JJ/AK barrel), maximises EV. Vs 4bet AA-only line
  KK is in clean shape to call-down. Solver pure CALL.

### HOLDOUT_024_AhKh_FD_NFD_river_brick — NFD missed river paired 2

- Hero: `Ah Kh`
- Board (river): `Th 8h 4c 2s 4d`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ check;
  river: BB check`
- Pot at decision: 8.8bb (preflop 5.5 + flop 2×1.65); SPR ≈ 11.07
- **Expected action:** CHECK
- Confidence: LOW
- Tolerance: soft
- Class-protected: Missed NFD river on paired board, IP, prior turn-check-back
- Rationale: Hero gave up turn (checked back), paired river. BB's
  range is condensed to Tx + air. Hero has A-high SDV but blocks
  a lot of Tx top-pair. Bluff line is plausible (rep AA/Tx better)
  but turn-check-back caps hero. Pure CHECK to take SDV. LOW
  confidence because turn-check-back-then-river-bluff is opp-pool
  dependent; against fold-heavy pools BET_66 also reasonable.

### HOLDOUT_025_AhJh_3way_river_TP_face_xraise — TP river face check-raise

- Hero: `Ah Jh`
- Board (river): `Ad 9c 4s Th 2c`
- Position / stack: BTN / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO bet_33 2.7, BTN call, BB fold;
  turn: CO check, BTN bet_75 9.9, CO call;
  river: CO check, BTN bet_33 11.0, CO raise to 50`
- Pot at decision: 94.2bb after CO check-raise (preflop 8.0; flop
  +2×2.7 → 13.4; turn +2×9.9 → 33.2; river BTN bet 11.0 → 44.2; CO
  raise 50 puts CO total in at 50, +50 → 94.2; reframe: pot now =
  44.2 + 50 = 94.2); hero (BTN) to-call 50 − 11 = 39; pot odds ≈
  29.3% [pot 94.2 / hero call 39 → 39/(94.2+39)]
- **Expected action:** FOLD
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPGK face river check-raise from preflop opener
  on flushless static runout
- Rationale: CO check-raised river on a board where the only credible
  value is 2-pair+, sets, straights (T9/A9/AT/44/99/AA). AJ is
  crushed. Pot odds 29% but value-only-villain range = call needs
  ≥30% bluffs which is unrealistic for the unprovoked check-raise
  line on a static board. Pure FOLD.

### HOLDOUT_026_TT_BB_flop_overpair_3way_xc_lim — TT overpair multiway low

- Hero: `Tc Th`
- Board (flop): `6h 5c 3d`
- Position / stack: BB / 100bb eff
- Villains: 2 (HJ, BTN)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 2.7, BTN call`
- Pot at decision: 13.4bb (preflop 8.0 + HJ 2.7 + BTN 2.7); to-call
  2.7; pot odds ≈ 16.8%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Mid overpair 3-way OOP face cbet + caller, call-not-raise
- Rationale: TT is solid bluffcatcher 3-way: ahead of HJ's pair-light
  bluff frequency + BTN floats. Behind sets/two-pair/straights but
  those are minority. RAISE bloats pot vs uncapped HJ. CALL keeps
  range wide, plays turn vs likely double-barrel. Pure CALL class
  for mid overpair.

### HOLDOUT_027_AJs_BB_3bet_pot_TP_face_cbet_mixed — TP 3bet pot OOP face cbet mixed CALL

- Hero: `As Js`
- Board (flop): `Ac 9c 5d`
- Position / stack: BB / 100bb eff (in 3-bet pot)
- Villains: 1 (BTN after BTN cold-call BB 3bet)
- Action history: `preflop: BTN open 2.5, BB 3bet 11, BTN call 11;
  flop: BB check, BTN bet_33 7.4`
- Pot at decision: 29.9bb (preflop 0.5 SB + 11 + 11 = 22.5; + BTN
  flop 7.4); to-call 7.4; pot odds ≈ 19.8%
- **Expected action:** CALL
- Confidence: LOW
- Tolerance: soft
- Class-protected: TP 3bet pot OOP face IP cbet on Ax-two-tone, mixed
  CALL / check-raise frequency
- Rationale: AJs in BB 3bet range vs BTN-flat-3bet cold-call. Flop
  Ac-9c-5d gives hero TPGK with backdoor heart and a club blocker
  (well, hero has spades — actually hero blocks no clubs; rationale:
  hero has TPGK no flush draw). BTN's cold-call-vs-3bet range is
  TT-QQ, AK suited, KQ suited, suited connectors with implied. On
  Ax flop BTN cbet range is thin: AK/AQ for value, sometimes JJ-QQ
  give-up-or-thin-cbet, plus club-flush-draws. Hero AJ ahead of
  many JJ-QQ underpairs / draws but behind AK/AQ. Solver mixes
  RAISE_33 (check-raise for protection vs club draws + thin value
  vs underpairs giving up) with CALL (slow-play, keeps BTN's
  give-up bluffs in). RAISE freq ~30-40%, CALL ~50%, FOLD ~10%.
  CALL chosen as the modal-EV defensible line; RAISE_33 is a
  reasonable alternative. LOW band reflects the genuine 3bet-pot
  check-raise frequency uncertainty noted in
  `feedback_solver_findings.md` (raise/call mixing is opp-pool-
  sensitive). [UNCERTAIN-SOLVER: 3bet-pot OOP check-raise frequency
  on Axx-two-tone — flag for solver verification.]

### HOLDOUT_028_88_set_river_2flush_complete — set river flush completes

- Hero: `8h 8d`
- Board (river): `8c 6h 3s 2h Kh`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ bet_75 6.6, BB call;
  river: BB check`
- Pot at decision: 22.0bb (preflop 5.5 + flop 2×1.65 + turn 2×6.6);
  SPR ≈ 4.16
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Set on river when flush completes, value-vs-protect
  trap, OOP-checked-to
- Rationale: BB's call-call range on this runout is heavy with hearts
  (flush draws), Kx (paired turn now top pair), and slowplays. River
  Kh completes hearts AND adds Kx top pair. Betting gets called by
  flushes (hero loses) + folded by Kx-no-heart that won't pay. CHECK
  realises showdown vs Kx + bluffs vs missed straight draws. Could
  reasonably mix BET_33 vs aggressive BB rivers but CHECK is
  modal-EV.

### HOLDOUT_029_QJo_HJ_flop_air_4way_low_flop — QJo air 4-way low

- Hero: `Qs Jc`
- Board (flop): `7d 4h 2c`
- Position / stack: HJ / 100bb eff
- Villains: 3 (CO, BTN, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BTN call 2.5,
  BB call 2.5`
- Pot at decision: 10.5bb (preflop 0.5 SB + 4×2.5); SPR ≈ 9.29
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: PFR-air on low flop 4-way, give up
- Rationale: 4-way pot on 742 = at least one player has 7x/4x/2x or
  pair frequency very high. QJ has 6 outs (3 Q + 3 J), no draw, no
  blocker effects. Bet folds out only worse, gets called/raised by
  better. CHECK pure. Realise equity, take free card.

### HOLDOUT_030_KQo_BTN_flop_air_3way_monotone — A-high air on 3-way monotone FOLD

- Hero: `Kc Qd`
- Board (flop): `Jh 8h 5h`
- Position / stack: BTN / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO bet_33 2.7`
- Pot at decision: 10.7bb (preflop 8.0 + CO 2.7); to-call 2.7;
  pot odds ≈ 20.1%
- **Expected action:** FOLD
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Air on monotone 3-way face cbet, no flush card
  in hand, IP between bettor and caller
- Rationale: KQo on Jh8h5h (monotone hearts) — hero has zero hearts,
  no pair, no straight draw (J-T-9 needed; hero has Q+K, gutter to
  9-T-J-Q-K needs T+9). With CO opening + 3-way pot + monotone
  flop, CO's bet range contains many flushes / heart-overpair-with-
  draw / Jx-heart, and BB still has to act behind. BTN floating
  here without a heart and without a pair faces too much risk:
  high probability someone has a flush already, hero's overcards
  are dominated when made (Kx caller-pool here is rare without
  heart but Kh is a key blocker hero doesn't hold), and check-raise
  pressure from BB looms. RAISE folds out only worse and bloats
  pot vs flushes. CALL bleeds chips toward turn aggression hero
  can't continue. Pure FOLD class — mirrors LITMUS_A4d air-on-
  monotone shape but as IP-mid-position vs cbet+caller-behind.

### HOLDOUT_031_AhAd_HJ_river_overpair_face_xraise_river — AA face river check-raise

- Hero: `Ah Ad`
- Board (river): `9c 7h 4s 2d 2h`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ bet_75 6.6, BB call;
  river: BB check, HJ bet_33 7.3, BB raise to 30`
- Pot at decision: 59.3bb after BB river check-raise (preflop 5.5 +
  flop 2×1.65 + turn 2×6.6 = 22.0; HJ river bet 7.3 → 29.3; BB
  raise total 30 → 59.3); to-call 30 − 7.3 = 22.7; pot odds ≈ 27.7%
  [22.7/(59.3+22.7)]
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: AA face river check-raise on paired runout, call-down
- Rationale: BB check-raises river on paired board. Value range:
  22 (full house), 99/77 (full house), some 4x trips. Bluffs:
  missed flush draws + busted straight draws (8h6h, JhTh, 65s).
  Pot odds ~28% requires ~28% bluff frequency in BB's range. AA
  has SDV vs all bluffs + loses to all value. Solver-typical
  CALL frequency ~50-70%. CALL chosen; FOLD also defensible.

### HOLDOUT_032_AQo_4way_open_face_3bet — AQo open face 3bet 4way limp scenario

- Hero: `Ad Qh`
- Board: PREFLOP (no flop yet — this is a preflop face-3bet decision)
- Position / stack: HJ / 100bb eff
- Villains: 3 (CO calls, BTN calls, BB 3bets)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BTN call 2.5,
  BB 3bet to 14`
- Pot at decision: 22.0bb (SB 0.5 dead + HJ 2.5 + CO 2.5 + BTN 2.5
  + BB 14); to-call 11.5 (14 − 2.5); pot odds ≈ 34.3%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Preflop AQo face squeeze with 2 cold-callers behind
- Rationale: Squeeze size 14bb (5.6x) is suppressed by callers'
  presence. AQo behind a 3-bettor BB sees CO+BTN cold-callers
  also have to act. With BTN/CO unlikely to 4-bet thin (likely
  fold or call), HJ closes vs BB's squeeze range (TT+, AQ+,
  some bluffs). AQo has decent equity + position vs the squeeze
  cold-caller multiway. 4bet too thin (folds bluffs); CALL with
  position is standard. FOLD is over-tight.

### HOLDOUT_033_KQs_CO_flop_TPGK_HU_face_donk_K_high — KQ TPGK face BB donk

- Hero: `Kc Qd`
- Board (flop): `Kh 9s 4c`
- Position / stack: CO / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: CO open 2.5, BB call 2.5;
  flop: BB bet_33 1.65`
- Pot at decision: 7.15bb (preflop 5.5 + BB 1.65); to-call 1.65;
  pot odds ≈ 18.75%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK face BB donk-lead, call vs raise
- Rationale: BB donks ~33% on K-high → polarised to slowplay (KQ/KJ/KT/
  KK rare, 99) + draws (T8s, J8s) + air. KQ has TPGK (Q kicker
  decent vs BB donk range). RAISE folds out bluffs and gets called
  by better Kx (KQ/KJ/KT). CALL keeps BB's range wide for turn.

### HOLDOUT_034_22_SB_flop_underpair_air_3way_high_card — 22 air 3way high card

- Hero: `2c 2h`
- Board (flop): `Ad Th 6c`
- Position / stack: SB / 100bb eff
- Villains: 2 (HJ, BTN)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, SB call 2.5,
  BB fold; flop: SB check, HJ check`
- Pot at decision: 8.5bb (SB 2.5 + BB 1.0 dead + HJ 2.5 + BTN 2.5);
  SPR ≈ 11.5
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Tiny underpair 3-way on AT-high after both villains check
  to BTN
- Rationale: 22 has ~6% equity 3-way on AT6. Both checked to BTN —
  hero (SB) acts first on turn. Pure CHECK class for tiny pair on
  high-card multiway flop. Bet gets raised by Ax + called by Tx.

### HOLDOUT_035_8d8h_BTN_turn_set_2flush_complete — set turn flush complete

- Hero: `8d 8h`
- Board (turn): `8c 6c 3c 2d`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check`
- Pot at decision: 8.8bb; SPR ≈ 10.6
- **Expected action:** BET_75
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Top set when flush completed on turn, IP, value+protect
- Rationale: Top set vs BB call range (lots of clubs, mid-pair). 2d
  turn is brick. Big bet for value vs Tx-pair / underpairs / clubs
  refusing to fold + protects vs straight draws (54, 75, 97). 75%
  near-pot is solver-modal; could mix POT (BET_100 not in standard
  sizing tags so capped at 75%).

### HOLDOUT_036_QcJd_BB_flop_air_face_bet_dry — air OOP face cbet on dry FOLD

- Hero: `Qc Jd`
- Board (flop): `8h 5s 2d`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65`
- Pot at decision: 7.15bb (preflop 5.5 + BTN 1.65); to-call 1.65;
  pot odds ≈ 18.75%
- **Expected action:** FOLD
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: BB defend air with two overcards no draw, low dry
  flop face small cbet, fold-not-defend
- Rationale: QJo on 852 rainbow has 6 overcard outs (3 Q + 3 J)
  but no flush draw, no straight draw, no backdoors of significance
  (BDFD requires runner-runner; BDSD needs T+9 or 7+9 runners — too
  remote). Effective equity ≈ 22-25% vs BTN open-cbet range. Pot
  odds 18.75% — barely meets price by direct equity but
  realisation OOP is poor: BTN barrels turn aggressively when
  overcards land (Q/J both pair scary cards for bluff-catching),
  and hero gives up on every brick turn. Defending wide here
  bleeds chips even at favourable price. CALL is defensible vs
  weak / over-cbet pools (hence soft tolerance + MEDIUM conf), but
  FOLD is solver-modal in mainline ranges that under-defend the
  weakest two-overcard combos. RAISE strictly worse (folds out
  only worse, gets called by all value).

### HOLDOUT_037_J9s_BB_defend_K_high_flop — BB defend K-high BD draws

- Hero: `Jh 9h`
- Board (flop): `Kh 8s 5d`
- Position / stack: BB / 100bb eff
- Villains: 1 (BTN)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65`
- Pot at decision: 7.15bb (preflop 5.5 + BTN 1.65); to-call 1.65;
  pot odds ≈ 18.75%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: BB defend texture with BDFD + BDSD + overcards, call vs fold
- Rationale: J9hh on K85 = BDFD (hearts) + BDSD (T7/QT runouts) + 2
  cards under K. ~28-32% equity vs BTN cbet range. Pot odds ≈19% =
  good price + implied odds on T/Q turns. RAISE thin; CALL preferred.
  FOLD over-tight given price + multi-way runout potential.

### HOLDOUT_038_AhKs_BTN_turn_TPGK_face_xraise_dynamic — TPGK IP face turn check-raise FOLD

- Hero: `Ah Ks`
- Board (turn): `Kd 9d 6c 5d`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6, BB raise to 22`
- Pot at decision: 37.4bb after BB raise (preflop 5.5 + flop 2×1.65
  + BTN turn 6.6 + BB raise total 22); to-call 22 − 6.6 = 15.4;
  pot odds ≈ 29.2%
- **Expected action:** FOLD
- Confidence: LOW
- Tolerance: soft
- Class-protected: TPGK IP face turn check-raise on diamond-flush-
  completing dynamic board, no diamond in hand, mixed FOLD/CALL
- Rationale: AhKs (no diamond) on Kd-9d-6c-5d turn — third diamond
  brings flush, plus 5d adds straight draws (78, 87 made on flop
  retains; 7-8 OESD made; 4 makes 4-5-6-7-8 needs 7+8). BB's
  check-raise turn line on this card is range-narrow to value: any
  flush (most diamonds in BB's call range slow-played flop), sets
  (KK rare since blocked, 99/66/55), two-pair (K9, K6 less likely
  but K5 unlocked by turn 5), 78 straight (made on turn). Bluff
  combos: AhQh + diamond-blockers (no diamond completed) — but
  hero blocks Ah which is a primary bluff candidate. Effective
  equity vs the value-heavy raise range ≈ 22-26%. Pot odds 29.2%
  → equity short of price. Plus reverse-implied: facing river
  shove on diamond/4/7/8 runouts dominates. Solver mixes CALL/
  FOLD ≈ 30/70 — FOLD modal but vs aggressive xr-bluff opps CALL
  defensible. LOW band reflects this. RAISE strictly worse (folds
  out only bluffs, gets it in vs value).

### HOLDOUT_039_AcQs_HJ_river_TP_face_x_lead_river — TPGK face river donk

- Hero: `Ac Qs`
- Board (river): `Ah 9d 4c 7h 5s`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ check;
  river: BB bet_75 6.6`
- Pot at decision: 15.4bb (preflop 5.5 + flop 2×1.65 + turn 0 +
  BB river 6.6); to-call 6.6; pot odds ≈ 30%
- **Expected action:** CALL
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK face river donk after turn check-back, OOP-from-PFR
- Rationale: Hero turn check-back caps; BB's river donk-lead 75% is
  polarised to 6x (straights), 5x rivered 2pair, A-better, plus
  bluffs (busted hearts JT/QJ/T8). AQ has SDV. Pot odds 30% requires
  ~30% bluffs which is realistic for donk-river polar lines. CALL
  modal; FOLD vs nit pool ok.

### HOLDOUT_040_77_HJ_flop_underpair_3way_K_high — 77 underpair K-high 3-way

- Hero: `7h 7d`
- Board (flop): `Kc 9d 5s`
- Position / stack: HJ / 100bb eff
- Villains: 2 (BTN, BB)
- Action history: `preflop: HJ open 2.5, BTN call 2.5, BB call 2.5`
- Pot at decision: 8.0bb (preflop 0.5 SB + 3×2.5); SPR ≈ 12.2
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Small-mid underpair K-high 3-way OOP from PFR
- Rationale: 77 face 2 callers on K95 = ~15% equity 3-way. Bet gets
  raised by Kx + sets, called by 9x + draws (BTN with TJ/T9 etc).
  CHECK to realise equity, fold to bet, take free turn if checked.

### HOLDOUT_041_KsTs_CO_flop_TP_HU_2tone_K_high — KT on KsTs flop TPTK

- Hero: `Kh Tc`
- Board (flop): `Ks 9s 4d`
- Position / stack: CO / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: CO open 2.5, BB call 2.5; flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** BET_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPGK on draw-heavy flop HU IP, bigger bet for protection
- Rationale: KT on K9s4d (two-tone spades) = TPGK on draw-heavy
  texture. Vs BB call range, hero ahead of K-weaker, behind KQ/AK.
  BET_66 (vs BET_33) chosen for protection vs flush draws + straight
  draws (Q-high, JTs, 87s). Solver mixes BET_33/BET_66 — BET_66 is
  the protect-equity choice for TPGK on draw-heavy.

### HOLDOUT_042_4c4d_HJ_flop_underpair_HU_2overs_low — small underpair on midflop

- Hero: `4c 4d`
- Board (flop): `Th 7d 5c`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5; flop: BB check`
- Pot at decision: 5.5bb; SPR ≈ 17.7
- **Expected action:** CHECK
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Small underpair on dynamic mid-flop HU IP, mixed bet/check
- Rationale: 44 on T75 = ~30% equity vs BB range. Wet board = 8/9/6
  draws, Tx top pair. Small c-bet ok for SDV, but solver mixes ~50/50
  with CHECK. CHECK chosen because realisation is decent IP (closed
  action on flop), avoids being raised by 8x/9x draws.

### HOLDOUT_043_22_set_3way_river_overcards — bottom set 3-way river over

- Hero: `2c 2h`
- Board (river): `9d 6h 2d Kh Qs`
- Position / stack: BTN / 100bb eff
- Villains: 2 (CO, BB)
- Action history: `preflop: CO open 2.5, BTN call 2.5, BB call 2.5;
  flop: BB check, CO bet_33 2.7, BTN call, BB fold;
  turn: CO check, BTN check;
  river: CO check`
- Pot at decision: 13.4bb; SPR ≈ 6.7
- **Expected action:** BET_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: Bottom set on river with overcard runout (K, Q),
  thin value 3-way-down-to-HU
- Rationale: Bottom set faded straight draws and didn't get called by
  worse on flop bet only. Turn checked through. River K + Q runout
  scary but CO checks river → likely AT-pair-or-worse / Kx-rare
  (CO would bet Kx). Small bet for thin value vs CO's missed-draw
  call-frequency + 9x. Big bet folds out everything; check loses
  thin value vs Tx/Jx that call small. Mixed in solver — small bet
  is the modal value-extract.

### HOLDOUT_044_AdQh_HJ_flop_air_4way_low — AQ air 4-way low flop

- Hero: `Ad Qh`
- Board (flop): `9s 6c 3d`
- Position / stack: HJ / 100bb eff
- Villains: 3 (CO, BTN, BB)
- Action history: `preflop: HJ open 2.5, CO call 2.5, BTN call 2.5,
  BB call 2.5`
- Pot at decision: 10.5bb (preflop 0.5 SB + 4×2.5); SPR ≈ 9.29
- **Expected action:** CHECK
- Confidence: HIGH
- Tolerance: strict
- Class-protected: PFR-air on low flop 4-way with backdoor potential
- Rationale: 4-way 963 = high pair frequency in callers' ranges. AQ
  air with BD diamonds + 6 over outs, but bet folds out only worse
  4-way. CHECK to realise equity, take free turn, see if any A/Q/3rd
  diamond comes.

### HOLDOUT_045_KhQh_BB_flop_TP_3bet_pot_face_cbet — KQ TP face cbet 3bet pot

- Hero: `Kh Qh`
- Board (flop): `Kc 7d 2c`
- Position / stack: BB / 100bb eff (in 3-bet pot)
- Villains: 1 (BTN after 3-bet)
- Action history: `preflop: BTN open 2.5, BB 3bet 11, BTN call 11;
  flop: BB check, BTN bet_33 7.4`
- Pot at decision: 29.9bb (preflop 0.5 SB + 11 BB + 11 BTN = 22.5;
  + BTN flop 7.4); to-call 7.4; pot odds ≈ 19.8%
- **Expected action:** RAISE_33
- Confidence: MEDIUM
- Tolerance: soft
- Class-protected: TPGK in 3bet pot OOP face IP cbet, check-raise for value
- Rationale: BB 3bet then check-call is normal; check-raise on K-high
  is a strong-hand line mixed with bluffs (AhXh, QhJh). KQ TPGK has
  enough equity to check-raise vs BTN's small cbet range (mostly
  wide bluffs given pot is bloated). Solver mixes CALL/RAISE_33;
  raise builds pot for stack-by-river vs Kx-weaker / draws. CALL
  also fine. [UNCERTAIN-SOLVER: 3-bet-pot OOP check-raise frequencies
  swing materially with stack depth — flag for explicit verification.]

### HOLDOUT_046_99_HJ_turn_overpair_face_xraise_HU — 99 turn face cr HU

- Hero: `9h 9d`
- Board (turn): `8c 6h 4s 2d`
- Position / stack: HJ / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: HJ open 2.5, BB call 2.5;
  flop: BB check, HJ bet_33 1.65, BB call;
  turn: BB check, HJ bet_75 6.6, BB raise to 22`
- Pot at decision: 37.4bb after BB raise (preflop 5.5 + flop 2×1.65
  + HJ turn 6.6 + BB raise total 22 = 37.4); to-call 22 − 6.6 = 15.4;
  pot odds ≈ 29.2% [15.4/(37.4+15.4)]
- **Expected action:** FOLD
- Confidence: LOW
- Tolerance: soft
- Class-protected: Mid overpair face turn check-raise from BB caller, fold
- Rationale: BB check-raises turn after call-call on 8642 = polarised
  to 75/53 straights, sets (88/66/44), 8x two-pair (84/86), and
  rare bluffs. 99 has SDV vs bluffs but loses to all value classes.
  At 29.5% pot odds, requires ~30% bluffs which is generous for
  a turn check-raise OOP (typical solver bluff-freq ~15-20%). FOLD
  modal. CALL defensible vs aggressive opponents (LOW band reflects
  this disagreement).

### HOLDOUT_047_AcKs_HJ_flop_TPTK_3bet_pot_HU_dynamic — TPTK 3bet pot dynamic

- Hero: `Ac Ks`
- Board (flop): `Kh 9h 8s`
- Position / stack: HJ / 100bb eff (in 3-bet pot)
- Villains: 1 (BTN after BTN 3bet HJ open and HJ called)
- Action history: `preflop: HJ open 2.5, BTN 3bet 9, HJ call 9;
  flop: HJ check, BTN bet_33 6.4`
- Pot at decision: 25.9bb (preflop 0.5 SB + 1.0 BB + 9 HJ + 9 BTN =
  19.5; + BTN flop 6.4); to-call 6.4; pot odds ≈ 19.8%
- **Expected action:** RAISE_33
- Confidence: HIGH
- Tolerance: strict
- Class-protected: TPTK 3bet pot OOP face IP cbet on dynamic, check-raise
- Rationale: K98 two-tone is dynamic; TPTK with NO-flush-block (no
  hearts) is a strong check-raise candidate vs BTN's small cbet
  range. BTN's range is wide bluffs + AA/KK condensed. Check-raise
  builds pot for stacks vs KK/AK-suited blockers, charges JT/QJ/T7
  draws, denies hearts. Solver-typical RAISE in this class.

### HOLDOUT_048_Td9d_BTN_river_FD_missed_paired — Tdiamond missed FD paired river

- Hero: `Td 9d`
- Board (river): `Ad 8d 4c 2s 4h`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN bet_75 6.6, BB call;
  river: BB check`
- Pot at decision: 22.0bb (preflop 5.5 + flop 2×1.65 + turn 2×6.6);
  SPR ≈ 4.16
- **Expected action:** BET_150
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Missed FD (non-nut) paired river IP, polar bluff with no SDV
- Rationale: T-high after barrel-barrel on Ad8d → checked-river. BB's
  range is condensed to Ax (limp-checked twice) + 8x + busted draws.
  T9 has zero SDV. Polar bluff overbet (BET_150) reps 4x trips +
  flushes, gets folds from Ax-weaker that gave up. Solver pure
  bluff line for missed-FD-with-no-SDV.

### HOLDOUT_049_AhJh_river_NF_paired_check_back — nut flush face river bet on paired

- Hero: `Ah Jh`
- Board (river): `Kh 9h 4c 2h Kc`
- Position / stack: BTN / 100bb eff
- Villains: 1 (BB)
- Action history: `preflop: BTN open 2.5, BB call 2.5;
  flop: BB check, BTN bet_33 1.65, BB call;
  turn: BB check, BTN check;
  river: BB bet_33 2.9`
- Pot at decision: 11.7bb (preflop 5.5 + flop 2×1.65 + turn 0 + BB
  river 2.9); to-call 2.9; pot odds ≈ 19.9%
- **Expected action:** RAISE_66
- Confidence: HIGH
- Tolerance: strict
- Class-protected: Nut flush facing small river donk on paired board, raise for value
- Rationale: BTN turn-check-back caps own range; BB river donk on
  paired board = polarised to Kx (trips/full house), some bluffs.
  Hero has nut flush. Just-call gets ~3bb extra; raise gets value
  from Kx (BB will pay-call most of the time given pot odds and
  BB's polarised donk). Raise-66 chosen because bigger raise risks
  folding out non-trip Kx; small raise extracts thin value.

### HOLDOUT_050_AsKs_CO_flop_NFD_TPTK_3bet_pot — NFD+TPTK 3bet pot CO

- Hero: `As Ks`
- Board (flop): `Kd 7s 4s`
- Position / stack: CO / 100bb eff (in 3-bet pot)
- Villains: 1 (BB after 3-bet)
- Action history: `preflop: CO open 2.5, BB 3bet 11, CO call 11;
  flop: BB bet_33 7.4`
- Pot at decision: 29.9bb (preflop 0.5 SB + 11 + 11 = 22.5; + BB
  flop 7.4); to-call 7.4; pot odds ≈ 19.8%
- **Expected action:** CALL
- Confidence: HIGH
- Tolerance: strict
- Class-protected: NFD + TPTK in 3bet pot face cbet, slowplay vs raise
- Rationale: NFD + TPTK = ~70% equity vs BB cbet range. Raise folds
  out bluffs (AQ/JJ/QQ no-spade) and reps only AA. CALL keeps BB's
  range wide for turn barrel + lets hero hit flush card cheaply.
  Solver pure CALL in 3bet pot for nut combo draws.

<!-- HASHED-BLOCK-END -->

## Per-class coverage breakdown

| Class-protected tag | Hands | Notes |
|---|---|---|
| TPGK / TPTK on dry / two-tone (HU IP) | 7 | well-covered |
| TPGK / TPTK on multi-way + 3-bet-pot textures | 6 | well-covered |
| Overpair (low/mid/high) value classes | 7 | well-covered |
| Air on monotone / paired / 4-way (give-up class) | 6 | well-covered |
| Mid/small underpair multiway / HU | 5 | adequate |
| Big draws (FD/NFD/OESD) — semibluff/call/check | 7 | well-covered |
| Set / two-pair (value+protect) | 4 | adequate (4 hands) |
| Bluff-catch face-bet / face-raise | 5 | adequate |
| Polar-bluff missed FD river | 3 | adequate |
| Preflop face-3bet cold-caller behind | 1 | flagged below |

## Concerns / flags worth surfacing to reviewer

1. **Preflop class is thin.** Only HOLDOUT_032 is a preflop spot. The
   held-out test set is overwhelmingly postflop. If the v2.4 model
   is also evaluated on preflop accuracy, supplement is needed.
   [Per the locked Stage 4 plan, postflop is the ship-gate scope, so
   this is consistent — but flag to reviewer.]

2. **River class is 10 hands (20%).** Adequate but lighter than
   flop+turn. River decisions are higher-stakes (last-street-pot-
   commit) and the model's weakest stage historically. Reviewer
   may want to raise river share to ~30% in v1.1.

3. **No 5-way+ hands.** Test set is HU/3-way/4-way only. v2.4 is the
   3-way specialist; 5-way+ is out-of-scope. Confirmed consistent
   with progressive-model-chain.

4. **Soft-tolerance count (15 hands) is high.** The DRAFT did not
   set a soft-vs-strict target. Reviewer may want to push more
   spots to strict-tolerance to make the test set harsher; current
   choice is calibrated to MIXED-strategy reality.

5. **Authoring is general-purpose-as-gto-expert, not a dedicated
   gto-expert dispatch.** Per locked Stage 4 D3 the dedicated
   author is preferred but the general-purpose fallback is
   authorised. A dedicated agent's reviewer pass is strongly
   recommended.

6. **Non-overlap is fingerprint-based** `(sorted(hero), sorted(board))`.
   Does not catch suit-isomorphic near-duplicates. v1.1 could add
   card-class equivalence; for v1.0 the held-out hands are
   strategically distinct anyway.

7. **24-hand calibration manifest** — RESOLVED at v1.0.1. Manifest
   located at `review/calibration_situations.json` (mirrored in
   `blind_calibration_exam_step7.json` and `_batch_{1,2,3}.json`);
   non-overlap empirically verified (0 matches against the 50
   holdout fingerprints).

8. **Inline-correction blocks in action history** — RESOLVED at
   v1.0.1. HOLDOUT_007 (4-card flop typo), HOLDOUT_016 (re-frame
   note for BB-fold-on-flop turn decision), HOLDOUT_019 (turn-card
   re-spec note), HOLDOUT_045 (cbet-line reframe), and HOLDOUT_047
   (check-then-cbet reframe) have all been flattened to single
   clean action histories. HOLDOUT_032 now carries `Board: PREFLOP`
   to make the preflop schema explicit. Each hand has exactly one
   `- Board:` line.

9. **One hand uses BET_150 (HOLDOUT_048 overbet).** Confirm with
   reviewer that BET_150 (1.5×pot) is supported by the action-class
   vocabulary in `gto_model.py` — the model currently emits a
   5-class action `(FOLD, CHECK, CALL, BET, RAISE)` without
   distinguishing sizes at output. Sizes here are documentation
   for the labeller / solver; the evaluator must be configured to
   coalesce all BET_* into BET when scoring.

10. **Action distribution at v1.0.1** is rebalanced: 10 FOLD
    (20%) / 10 CHECK (20%) / 12 CALL (24%) / 13 BET (26%) /
    5 RAISE (10%). FOLD is now on target (was 4 in v1.0); BET is
    on target (was 20 in v1.0). The six v1.0→v1.0.1 BET→FOLD
    re-authorings cover dominated-bluffcatcher river, gutter-short-
    of-price, MW-air-on-monotone face-cbet, mid-underpair vs
    continuation barrel, IP-TPGK face turn check-raise on dynamic,
    and BB-defend-air on dry — matching the four reviewer-requested
    FOLD-class shapes from `MAIN_TERMINAL_PR_16_FIX_FORWARD_REQUIRED`.

11. **LOW-confidence band at v1.0.1** is on target (5 hands):
    HOLDOUT_017 (mid-underpair vs barrel mixed CALL/FOLD),
    HOLDOUT_024 (NFD-miss river check-back), HOLDOUT_027 (3bet-pot
    OOP TP mixed CALL/check-raise), HOLDOUT_038 (TPGK IP face turn
    check-raise on dynamic), HOLDOUT_046 (mid-overpair face turn
    check-raise on dry low).

12. **FOLD class now represented in 10-hand solver sample** —
    HOLDOUT_046 swapped in (replacing HOLDOUT_037). Sample
    composition now: 0 → 1 FOLD, 2 CHECK, 3 CALL, 4 BET, 1 RAISE
    (one of the BET hands previously listed remains BET via the
    re-authored H022 / others).

## Usage protocol

### Single-shot evaluation

When v2.4 candidate model is ready (post-Stage 5):

1. Load held-out test set (this file + JSONL companion produced by
   builder).
2. Run model inference on all 50 hands (no human in the loop;
   automated).
3. Score against held-out labels (treating BET_* as BET, RAISE_* as
   RAISE for the 5-class model output; per-hand soft-tolerance
   scoring per `tolerance_rules` in `calibration_anchors.json`).
4. Report accuracy + per-class-protected breakdown + per-confidence-
   band breakdown + per-street breakdown + per-num-opponents
   breakdown.

**No iteration.** If v2.4 candidate scores poorly on held-out: the
candidate is rejected, NOT the held-out set. Investigate via Stage
5 multi-seed audits + Stage 4 corpus quality checks. Don't tweak
the held-out set "to make v2.4 look good."

### Held-out hand exposure

After single-shot evaluation, the held-out hands MAY be added to the
labelling corpus for v2.5+ (test value is exhausted). For v2.4
specifically, the held-out set is **single-use**.

## Disposition for v2.5+

For v2.5 ship, a NEW held-out test set is constructed. The v2.4
held-out hands move into the training corpus (if owner approves) or
get archived. The new held-out set is constructed with the same
authorship + non-overlap protocol against v2.5-era corpora.

## Self-consistency closure

Self-consistency pass run after authoring:

1. **All 50 hands have all required fields.** Verified — Anchor ID,
   hero hand, board, position+stack, action history (with re-frame
   notes where original draft was ambiguous), villain count,
   expected action, confidence band, tolerance, rationale, class-
   protected. PASS.

2. **Action sizing tags use solver-aligned conventions.** Verified
   per `feedback_solver_aligned_sizing.md` — flop 25%/66%, turn
   33%/75%, river 33%/75%/150%, RAISE 33%/66% pot-relative. PASS.

3. **Pot/SPR arithmetic full audit (v1.0.1).** Every hand recomputed
   under the canonical convention "0.5bb dead-SB included in postflop
   pots" (or 1.0bb dead-BB when SB completes). Corrections applied to
   approximately 30 hands. Major fixes: H022 / H028 / H048 each had
   the turn bet double-counted (off by 6.6bb); H039 had a river-bet
   sizing error (7.5 → 6.6, the correct 75% of pot 8.8); H014 / H025
   / H031 had cascading-3-street arithmetic redone with consistent
   sizing tags; H016 / H019 / H045 / H047 had the inline `Re-frame`
   blocks flattened. Also: bet_33 nominally yields ~20% pot odds
   (not the 25% repeatedly stated in v1.0); all such pot-odds
   figures corrected. PASS.

4. **Confidence band distribution.** 28 HIGH / 17 MEDIUM / 5 LOW.
   All within ±2 of target (60/30/10 of 50). PASS.

5. **Action distribution.** 10 FOLD / 10 CHECK / 12 CALL / 13 BET /
   5 RAISE. All within tolerance of the 20/24/20/26/10 targets.
   PASS.

6. **10-hand solver sample spans bands + classes.** Composition:
   5 HIGH / 3 MEDIUM / 2 LOW; actions: 1 FOLD / 3 CHECK / 2 CALL /
   3 BET / 1 RAISE. FOLD class now represented (HOLDOUT_046 swapped
   in for HOLDOUT_037). PASS. (v1.0.2 correction: v1.0.1 closure
   stated 4/5/1 bands and 1/2/3/3/1 actions — both stale from a
   pre-swap count; verified empirically against the 10 sample IDs.)

7. **Non-overlap verification (programmatic).** Built fingerprint
   set from 56 jsonl files in `training-data/` (1,996 unique
   `(sorted(hero), sorted(board))` keys covering 4,034 records),
   PLUS the 5 calibration-anchor fingerprints, PLUS the 21 distinct
   fingerprints in `review/calibration_situations.json` + mirror
   files (24-hand calibration manifest). Cross-checked all 50 v1.0.1
   holdout fingerprints. **Result: 0 matches.** PASS.

8. **Hashed-block delimiter discipline.** Exactly one literal
   start-of-block HTML comment and one literal end-of-block HTML
   comment in this file (verified with shell-time literal
   construction; references elsewhere build the strings via
   concatenation so this prose itself does not produce additional
   matches). PASS.

9. **JSONL-export-friendliness.** Every hand has exactly one
   `- Board:` line; no inline `Re-frame:` blocks remain in any
   hand spec; the preflop hand (H032) carries `Board: PREFLOP` as
   a placeholder for schema consistency. PASS.

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` — Stage 4
  plan §7 specifies the held-out set as a Stage 6 addition
- `MASTER_PLAN (1).md` — existing Stage 6 ship gate (5 litmus tests)
- `LABELLING_PIPELINE.md` — calibration exam construction (similar
  authoring discipline)
- `feedback_solver_findings.md` — solver verification protocol
- `feedback_solver_aligned_sizing.md` — bet sizes for solver
  verification
- `STAGE5_RETRAIN_PROTOCOL_v1_0.md` — model that this set tests
- `STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md` — origin draft
