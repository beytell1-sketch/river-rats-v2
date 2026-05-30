# Board-Reading Audit — 38(40)-spot Screening Verdicts — 2026-05-30

**Screener:** orchestrator (Opus 4.7 1M) — single reviewer, sequential pass
**Source flags:** `data/4way_corpus/board_reading_audit_2026-05-30.jsonl` (PR #480)
**Audit report:** `review/comms/BOARD_READING_AUDIT_REPORT_2026-05-30.md`
**Pilot precedent:** `data/4way_corpus/board_reading_audit_screening_5spot_pilot_2026-05-30.json` (1 ESCALATE, 4 AFFIRM)
**Full verdicts (machine-readable):** `data/4way_corpus/board_reading_audit_screening_38spot_full_2026-05-30.jsonl`

---

## Scope reconciliation

Task brief: "38 remaining unanimous-consensus spots." Audit report enumerates **44 unique 5/5 unanimous spots** with ≥1 LOW-fpr labeller; 4 of these are in the pilot (085, 138, 147, 358). Pilot's 5th spot (CHAIN-009-001) is 4/5, not 5/5.

44 - 4 = **40 remaining 5/5 unanimous spots**. The "38" figure in the task brief and pilot file appears to round/undercount by 2. To avoid leaving any unanimous-consensus flagged spot un-screened, I screened all **40** remaining spots.

---

## Verdict counts (out of 40)

| Verdict | Count | % |
|---|---|---|
| AFFIRM (right action, wrong reason — or terminology-only error) | **32** | 80% |
| ESCALATE_TO_PANEL | **7** | 17.5% |
| REVISE (proposed action change) | **1** | 2.5% |

**Pilot comparison (5 spots):** 4 AFFIRM, 1 ESCALATE, 0 REVISE. The 40-spot rate is broadly consistent: 80% AFFIRM (vs 80% pilot), 17.5% ESCALATE (vs 20% pilot), 2.5% REVISE (vs 0% pilot, first action-overturn found).

---

## AFFIRM bucket (32 spots)

Right-action, wrong-reason. Phantom-NFD/FD/OESD rationale was mechanically wrong, but the consensus action holds under corrected equity. Most common patterns:

- **Structural protocol bet (PFA/range-cbet in HU 3bet/4bet pots):** spots 058 (AcQc 852 IP 4bet), 129 (AhKh 842 IP 4bet), 366 (Ah3h 485 PFA 3bet IP), 376 (Ac4c T85 PFA 3bet IP). Small range-cbet is structural — equity claim irrelevant.
- **Top-of-range value bet (AA/KK/top set on dry/disconnected boards):** 023 (AA QJ3), 143 (AA top set A83), 149 (AA top set A84), 204 (AK top two-pair AK4), 314 (TT top set T24), 320 (KK 742).
- **Top pair value bet/raise in closing action:** 318 (AdQs A45 TPGK), 319 (AsJs J74 TPTK), 328 (AhJh J75 TPTK), 503 (AsJh J94 TPTK), 350 (KQ QJ4 TPGK CALL), 374 (AsQs QJ9 TPTK CALL), 396 (Td9c 496 mid-pair CALL).
- **Multiway IP semi-bluff (double-gutshot mislabeled as OESD — same 8 outs, same EV):** 173 (JT 982 DG), 188 (JT 984 DG), 104 (J9 QT5 DG, CHECK is correct as cold-caller).
- **Multiway IP MADE-STRAIGHT mislabeled as draw (labellers UNDERSTATED hand strength — same family as pilot 147):** 141 (JT on 987 = made straight), 142 (95s on 876 = made straight).
- **OOP cold-caller in 3bet pot — structural check-to-PFA:** 039 (AhKs QJ3 CHECK), 083 (AhKs QJ3 CHECK), 078 (Ks9s T85 CHECK), 095 (Kd9d T85 CHECK).
- **Multiway weak draw — conservative CHECK correct independent of equity claim:** 168 (95s 456), 190 (9c5c 276), 199 (9s5s 276).
- **Closing FOLD with overcards-only or BDFD-only:** 290 (As8s J75 FOLD), 189 (KhQh JT6 CALL — actually massive flush draw + double-gutshot, audit caught label rationale errors but action is unambiguous CALL).
- **Closing CALL with TPGK + BDFD:** 349 (9s8s 274 CALL), 374, 350.

---

## ESCALATE_TO_PANEL bucket (7 spots)

These need full 3-reviewer panel. Cluster pattern dominates:

### Cluster 1: AA cold-caller of 3bet, multiway OOP (4 spots)
- **4WF-4-WAY-3--072** — AhAs on QhJh3s (75bb stack, cold-caller UTG of CO 3bet, 4-way). Mass-vote BET 66%. Concern: standard OOP-vs-PFA protocol is check-to-PFA; donking AA OOP in 3bet pot is non-standard. Phantom FD rationale may have driven the BET vote.
- **4WF-4-WAY-3--090** — AhAs on 6hJh3s (same line, 100bb). Same concern.
- **4WF-4-WAY-3--099** — AsAh on QsJs3h (same line, 100bb). Same concern.
- **4WF-4-WAY-3--109** — AhAs on 2hJh3s (same line, dryer board, even more clearly check-to-PFA territory). Same concern.

**Why escalate:** Mass-vote pattern is consistent (5x BET 66% across all 4) which raises the chance it is correct via a labeller-known equilibrium I'm missing; equally it raises the chance the cohort had a shared blind spot ("AA = bet" instinct overriding 3bet-pot OOP protocol). Resolution should be a single panel decision applied to all 4 for consistency. **Could be REVISE-cluster (BET → CHECK) if panel agrees check-to-PFA dominates.**

### Cluster 2: AK/AK-class flop with Ac blocker, multiway OOP 3bet pot (1 spot)
- **4WF-4-WAY-3--016** — AcKd on Qc5c4d, 4-way OOP 3bet pot. Mass BET 66%. Structurally identical to pilot ESCALATE spot 085 (AcKd on Qc4c3s) which was escalated for the same Ac-blocker + BDFD + thin equity reasons. Panel should treat 016 + pilot's 085 as a paired decision.

### Cluster 3: Semi-bluff vs check with strong combo draw, multiway IP (1 spot)
- **4WF-MULTIWAY-193** — 9d5d on 4d7h6c, 4-way SRP MP IP. Double-gutshot (8 outs) + BDFD ≈ 10-12 outs. Mass CHECK. Solver likely bets this 30-50% as a semi-bluff. Genuinely close BET-vs-CHECK with strong draw. Comparable to spots 173/188 (also DG, also IP) which BET — inconsistency suggests the category needs a panel ruling on "when does DG IP semi-bluff vs check."

### Cluster 4: Marginal closing fold with corrected equity ~30% + Ah blocker (1 spot)
- **4WF-CLOSING--298** — AhJh on 3h7c5d, closing-action FOLD. Corrected equity ~28-33% (BDFD + 2 dirty overs + Ah blocker) vs pot odds 17%. Mass FOLD likely came from perceiving the small donk as a monster; with Ah blocker + overs + BDFD, CALL is mathematically defensible and possibly correct. **Could be REVISE (FOLD → CALL)** if panel confirms.

---

## REVISE bucket (1 spot)

### 4WF-MULTIWAY-205 — 9s5s on 8c7c4h, hero=HJ IP 4-way SRP — current consensus BET 66% → proposed CHECK

**Mechanical truth:** Hero 9s5s on 8c-7c-4h. Spades = 2 (hero's only — board has 0 spades) so **NO BDFD**. Clubs = 2 (board) + 0 (hero) → no relevance. Hero has GUTSHOT to 6 (4 outs: 5-6-7-8-9). NO flush draw of any kind. 1 dirty overcard (9) and 1 third pair card (5). Total ≈ 4 outs + thin SDV.

**Why mass-vote BET is wrong:** Labellers' rationale claimed flush draw + OESD (or claimed "FD+gutshot" combo draw worth ~12-15 outs ≈ 36%+ equity). Corrected: **4 outs only, no flush draw, equity ~18-24%**. Hero is non-PFA (UTG opens, hero MP→HJ calls, CO/BTN call) so betting is a leveraged stab into 3 players. A 4-out semi-bluff with no flush backup multiway IP from non-PFA has negative EV — fold equity is poor (3 players to fold), realized equity is thin (4 outs / 47 cards = ~17% by river single street).

**Proposed REVISE:** consensus changes from **BET 66%** → **CHECK**. Confidence MEDIUM-HIGH. (Note: this is the cleanest action-overturn candidate in the corpus — direct consequence of phantom-FD rationale.)

**Cross-check vs similar spots:**
- 199 (9s5s on 2-7-6, gutshot+BDFD, MP IP) → CHECK (mass-vote correct)
- 190 (9c5c on 2-7-6, gutshot+BDFD, MP IP) → CHECK (mass-vote correct)
- 168 (9s5s on 4-5-6, middle pair + BDFD, MP IP) → CHECK (mass-vote correct)
- 205 (9s5s on 8-7-4, gutshot only NO BDFD, HJ IP) → BET? **inconsistent** with siblings.

The inconsistency strongly suggests 205's BET vote was driven by phantom FD rhetoric (the "Spades+clubs both two-tone-ish" appearance triggered FD-reading errors) when the actual board has 2 spades total = no BDFD for hero. **REVISE recommended.**

---

## Corpus-level assessment: "right action, wrong reason" hypothesis

### Supported, with one explicit action-overturn

The pilot's hypothesis — that mass mis-classification of BDFD as FD typically does NOT change the action — is **broadly confirmed at 80% AFFIRM rate**, mirroring the pilot's 80% AFFIRM rate.

### Pattern decomposition (40 spots)

| Category | Count | Notes |
|---|---|---|
| Right action via STRUCTURAL protocol (cold-caller-checks-to-PFA, 4bet-pot range-cbet, top-of-range value) — phantom-draw rationale irrelevant | ~18 | The biggest single AFFIRM mechanism. Action is structural; equity is decoration. |
| Right action because hero has STRONG made hand or top-of-range value (AA, KK, top set, top two pair, TPTK in closing action) — phantom-draw rationale is window-dressing | ~10 | Labellers got the action right despite (or partly because of) wrong rationale. |
| TERMINOLOGY-only error: double-gutshot labeled as OESD (same 8 outs, same EV) | ~3 | Audit catches the wording; EV unchanged. |
| UNDERSTATED equity error: labellers called a MADE STRAIGHT an "OESD" or "draw" but bet for value anyway | 2 | 141 (JT on 987) and 142 (95s on 876). Like pilot 147. |
| Right action because corrected equity is still well above threshold (massive made/combo draw — 189) | 1 | KhQh on JhT-6h with real FD + double-gutshot. Audit caught label sloppiness; action unambiguously right. |
| Right action because corrected equity is still well below threshold (FOLD spots with BDFD-only and no SDV) | ~3 | E.g. 290 As8s J75 — even with no FD, FOLD is correct. |
| **Genuinely-close ESCALATE** — corrected equity changes which decision dominates | 7 | Five-spot cluster (AA-cold-caller 023/072/090/099/109), the AcKd-flop 016 (paired with pilot 085), the semi-bluff DG 193, and the closing FOLD 298. |
| **Action-overturn REVISE** — phantom FD rationale led to wrong BET when actual hand is just 4-out gutshot with no FD | **1** | 205. |

### Action-overturn rate

**1/40 = 2.5% confirmed REVISE.** If 4 of the 7 ESCALATEs eventually resolve to action-changes (worst case — the AA-cold-caller cluster + 298 all flip), the action-overturn rate reaches **5/40 = 12.5%**. Pilot estimate was "0-10%"; this confirms the LOW-but-non-zero hypothesis. The corpus is *mostly* a wrong-reason-right-action problem, but **205 is the first confirmed action-overturn** and demonstrates that the audit does occasionally catch a label that requires correction, not just rationale-rewriting.

### Implications for downstream training

- **Action labels:** 39/40 stand as-is; 1 needs revision (205 → CHECK).
- **Rationale text:** ~30 of 40 spots have measurably wrong rationale text mentioning phantom NFD/FD/OESD. If the labelling pipeline uses rationale text as training signal (not just action), the corpus needs targeted rationale rewrites or a CONFLATED_BDFD_AS_FD attention-feature suppression layer.
- **Mass-vote bias:** Sonnet labellers exhibit a consistent "miscounts BDFD as FD on 3-card-suited flops" failure mode. Worth a dedicated test in the labeller eval rubric: present 20 BDFD-only spots and check rationale text for "flush draw" claims.

---

## Recommended next steps

1. **Apply REVISE for 205** — update `consensus_v2.consensus_action` for `4WF-MULTIWAY-205` from `BET` to `CHECK`. Single-spot patch.
2. **Panel debate for 7 ESCALATEs** — bundle the AA-cold-caller cluster (072+090+099+109) into one panel ticket so it is resolved consistently. Add 016 (paired with pilot 085 — could be resolved together with that existing panel's continuation). Add 193 and 298 as standalone.
3. **Rationale-rewrite track (low priority but high volume)** — for the 32 AFFIRM spots with phantom-draw rationale, a sweep that rewrites "flush draw" → "backdoor flush draw" in the rationale text would clean the training signal without changing labels.
4. **Mass-labeller eval test** — bake a BDFD-vs-FD discrimination test into the next labeller calibration pass.

---

*Screening completed 2026-05-30 by orchestrator (Opus 4.7 1M).*
