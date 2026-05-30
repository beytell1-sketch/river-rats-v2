# Board-Reading Audit Report — 2026-05-30

**Audit type:** Mechanical (non-LLM) scan of rationale text vs computed draw features.
**Scope:** Batches 001-009, postflop spots only.
**Read-only:** No consensus_v2 or label files modified.

---

## Summary Counts

| Metric | Count |
|--------|-------|
| Postflop spots scanned | 376 |
| (spot, labeller) pairs scanned | 1926 |
| Total flagged (spot, labeller) pairs | 1924 |
| LOW false-positive-risk flags (high-confidence genuine errors) | 901 |
| HIGH false-positive-risk flags (mostly villain-range noise) | 1023 |

### Flags by mismatch type (total / LOW-fpr / HIGH-fpr)

LOW-fpr = mechanically verifiable as a genuine hero board-read error.
HIGH-fpr = pattern likely fired on villain-range or board-texture text.

| Mismatch type | Total | LOW-fpr | HIGH-fpr | Description |
|---------------|-------|---------|----------|-------------|
| PHANTOM_NFD | 186 | 60 | 126 | Claims NFD but hero lacks Ace of flush-draw suit (HIGH = 'backdoor NFD' phrasing) |
| PHANTOM_FD | 634 | 329 | 305 | Claims flush draw but no suit reaches 4 cards (HIGH = no BDFD at all; villain range) |
| CONFLATED_BDFD_AS_FD | 329 | 329 | 0 | Claims full FD when only BDFD exists — the canonical CHAIN-009-016 error class |
| MISSED_FD | 26 | 26 | 0 | Flush draw exists but no flush-draw mention in rationale |
| PHANTOM_GUTSHOT | 224 | 3 | 221 | Claims gutshot but 0 hero straight outs (HIGH = villain-range mention) |
| PHANTOM_OESD | 525 | 154 | 371 | Claims OESD but no OESD found (LOW = has outs but they're gutshot-class) |

---

## Top 10 Most-Impactful Flagged Spots

Sorted by: unanimous consensus first, then LOW-fpr errors present, then opus-flagged, then labeller count.

| Spot ID | Batch | Hero | Board | Consensus | Action | Flagged | Low-FPR flags | Opus? | Mismatch types |
|---------|-------|------|-------|-----------|--------|---------|---------------|-------|----------------|
| 4WF-4-WAY-3--016 | 1 | AcKd | Qc5c4d | all-agree | BET | 5/5 labellers | 3 labellers | no | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_GUTSHOT(1), PHANTOM_NFD(4) |
| 4WF-4-WAY-3--023 | 1 | AhAs | QhJh3d | all-agree | BET | 5/5 labellers | 5 labellers | no | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_GUTSHOT(2), PHANTOM_NFD(2), PHANTOM_OESD(3) |
| 4WF-4-WAY-3--039 | 1 | AhKs | QhJh3s | all-agree | CHECK | 5/5 labellers | 3 labellers | no | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_GUTSHOT(2), PHANTOM_NFD(3), PHANTOM_OESD(2) |
| 4WF-4-WAY-3--058 | 2 | AcQc | 8c5h2s | all-agree | BET | 5/5 labellers | 3 labellers | no | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(4) |
| 4WF-4-WAY-3--072 | 2 | AhAs | QhJh3s | all-agree | BET | 5/5 labellers | 5 labellers | no | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(1), PHANTOM_OESD(2) |
| 4WF-4-WAY-3--078 | 2 | Ks9s | Th8s5d | all-agree | CHECK | 5/5 labellers | 4 labellers | no | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(3), PHANTOM_OESD(5) |
| 4WF-4-WAY-3--083 | 2 | AhKs | QhJh3s | all-agree | CHECK | 5/5 labellers | 4 labellers | no | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(3), PHANTOM_NFD(4), PHANTOM_OESD(4) |
| 4WF-4-WAY-3--085 | 2 | AcKd | Qc4c3s | all-agree | BET | 5/5 labellers | 5 labellers | no | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(5), PHANTOM_OESD(1) |
| 4WF-4-WAY-3--090 | 2 | AhAs | 6hJh3s | all-agree | BET | 5/5 labellers | 4 labellers | no | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_NFD(4), PHANTOM_OESD(1) |
| 4WF-4-WAY-3--095 | 2 | Kd9d | Tc8d5s | all-agree | CHECK | 5/5 labellers | 4 labellers | no | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(2), PHANTOM_OESD(4) |

---

## High-Risk: Unanimous Consensus + 3+ Labellers + LOW-FPR Board-Read Error

These are the highest-risk training data points. Consensus action was reached
unanimously AND 3+ labellers have at least one LOW false-positive-risk flag
(i.e. a mechanically verifiable hero board-read error, not villain-range noise).

| Spot ID | Batch | Hero | Board | Action | Flagged labellers (any) | Low-FPR labellers | Mismatch types |
|---------|-------|------|-------|--------|-------------------------|-------------------|----------------|
| 4WF-4-WAY-3--016 | 1 | AcKd | Qc5c4d | BET | 5/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_GUTSHOT(1), PHANTOM_NFD(4) |
| 4WF-4-WAY-3--023 | 1 | AhAs | QhJh3d | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_GUTSHOT(2), PHANTOM_NFD(2), PHANTOM_OESD(3) |
| 4WF-4-WAY-3--039 | 1 | AhKs | QhJh3s | CHECK | 5/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_GUTSHOT(2), PHANTOM_NFD(3), PHANTOM_OESD(2) |
| 4WF-4-WAY-3--058 | 2 | AcQc | 8c5h2s | BET | 5/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(4) |
| 4WF-4-WAY-3--072 | 2 | AhAs | QhJh3s | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(1), PHANTOM_OESD(2) |
| 4WF-4-WAY-3--078 | 2 | Ks9s | Th8s5d | CHECK | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(3), PHANTOM_OESD(5) |
| 4WF-4-WAY-3--083 | 2 | AhKs | QhJh3s | CHECK | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(3), PHANTOM_NFD(4), PHANTOM_OESD(4) |
| 4WF-4-WAY-3--085 | 2 | AcKd | Qc4c3s | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(5), PHANTOM_OESD(1) |
| 4WF-4-WAY-3--090 | 2 | AhAs | 6hJh3s | BET | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_NFD(4), PHANTOM_OESD(1) |
| 4WF-4-WAY-3--095 | 2 | Kd9d | Tc8d5s | CHECK | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(2), PHANTOM_OESD(4) |
| 4WF-4-WAY-3--099 | 2 | AsAh | QsJs3h | BET | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_NFD(2), PHANTOM_OESD(3) |
| 4WF-4-WAY-3--104 | 3 | Jd9s | QhTs5d | CHECK | 5/5 | 5 | PHANTOM_OESD(5) |
| 4WF-4-WAY-3--109 | 3 | AhAs | 2hJh3s | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(1) |
| 4WF-4-WAY-3--129 | 3 | AhKh | 8h4s2d | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(4) |
| 4WF-4-WAY-3--138 | 3 | AcKc | 8c5h2s | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(5) |
| 4WF-MULTIWAY-141 | 3 | JdTh | 9s8s7h | BET | 5/5 | 5 | PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_OESD(5) |
| 4WF-MULTIWAY-142 | 3 | 9s5s | 8c7c6h | BET | 5/5 | 4 | PHANTOM_FD(5), PHANTOM_OESD(4) |
| 4WF-MULTIWAY-143 | 3 | AsAd | Ac8h3c | BET | 5/5 | 2 | PHANTOM_FD(5), PHANTOM_NFD(2) |
| 4WF-MULTIWAY-147 | 3 | QsKs | JsTh9s | RAISE | 5/5 | 5 | PHANTOM_NFD(4), PHANTOM_OESD(4) |
| 4WF-MULTIWAY-149 | 3 | AdAs | Ah8c4c | BET | 5/5 | 1 | PHANTOM_FD(5), PHANTOM_GUTSHOT(2), PHANTOM_NFD(1), PHANTOM_OESD(1) |
| 4WF-MULTIWAY-168 | 4 | 9s5s | 4s5h6h | CHECK | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(2), PHANTOM_OESD(4) |
| 4WF-MULTIWAY-173 | 4 | JdTh | 9s8s2d | BET | 5/5 | 5 | PHANTOM_FD(2), PHANTOM_OESD(5) |
| 4WF-MULTIWAY-188 | 4 | JcTs | 9h8h4c | BET | 5/5 | 5 | PHANTOM_FD(1), PHANTOM_OESD(5) |
| 4WF-MULTIWAY-189 | 4 | QhKh | JhTs6h | CALL | 5/5 | 5 | MISSED_FD(1), PHANTOM_NFD(3), PHANTOM_OESD(4) |
| 4WF-MULTIWAY-190 | 4 | 9c5c | 2c7s6d | CHECK | 5/5 | 5 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_OESD(4) |
| 4WF-MULTIWAY-193 | 4 | 9d5d | 4d7h6c | CHECK | 5/5 | 5 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_OESD(5) |
| 4WF-MULTIWAY-199 | 4 | 9s5s | 2s7c6h | CHECK | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_OESD(4) |
| 4WF-MULTIWAY-204 | 5 | AcKs | AhKh4s | BET | 5/5 | 1 | PHANTOM_FD(5), PHANTOM_NFD(1) |
| 4WF-MULTIWAY-205 | 5 | 9s5s | 8c7c4h | BET | 5/5 | 4 | PHANTOM_FD(3), PHANTOM_OESD(4) |
| 4WF-CLOSING--290 | 6 | As8s | Js7d5c | FOLD | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_GUTSHOT(1), PHANTOM_NFD(2), PHANTOM_OESD(2) |
| 4WF-CLOSING--298 | 6 | AhJh | 3h7c5d | FOLD | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(1), PHANTOM_OESD(3) |
| 4WF-CLOSING--314 | 7 | TcTd | Th2d4d | RAISE | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(1) |
| 4WF-CLOSING--318 | 7 | AdQs | Ah4d5d | RAISE | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_NFD(2), PHANTOM_OESD(3) |
| 4WF-CLOSING--319 | 7 | AsJs | Js7d4d | RAISE | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_OESD(2) |
| 4WF-CLOSING--320 | 7 | KcKh | 7d4c2c | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_NFD(1), PHANTOM_OESD(4) |
| 4WF-CLOSING--328 | 7 | AhJh | Jh7c5d | RAISE | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_NFD(3), PHANTOM_OESD(4) |
| 4WF-RANGE-AS-349 | 7 | 9s8s | 2h7s4d | CALL | 5/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_GUTSHOT(1), PHANTOM_OESD(5) |
| 4WF-RANGE-AS-350 | 7 | KcQc | QdJs4h | CALL | 5/5 | 1 | PHANTOM_FD(2), PHANTOM_GUTSHOT(2), PHANTOM_NFD(1), PHANTOM_OESD(4) |
| 4WF-RANGE-AS-358 | 8 | Td8c | Jh9d6c | CALL | 5/5 | 5 | PHANTOM_OESD(5) |
| 4WF-RANGE-AS-366 | 8 | Ah3h | 4d8d5h | BET | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_GUTSHOT(2), PHANTOM_OESD(4) |
| 4WF-RANGE-AS-374 | 8 | AsQs | QcJh9s | CALL | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_OESD(3) |
| 4WF-RANGE-AS-376 | 8 | Ac4c | Th8s5c | BET | 5/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_OESD(4) |
| 4WF-RANGE-AS-396 | 8 | Td9c | 4d9d6c | CALL | 5/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_GUTSHOT(1), PHANTOM_NFD(2), PHANTOM_OESD(2) |
| 4WF-MW-AXIS-503 | 9 | AsJh | Js9s4h | RAISE | 5/5 | 5 | CONFLATED_BDFD_AS_FD(5), PHANTOM_FD(5), PHANTOM_GUTSHOT(1), PHANTOM_NFD(4), PHANTOM_OESD(2) |
| 4WF-4-WAY-3--005 | 1 | JdJs | QhTs5s | CHECK | 4/5 | 1 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_GUTSHOT(3), PHANTOM_OESD(2) |
| 4WF-4-WAY-3--009 | 1 | AhQh | 8h5c2d | BET | 4/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_NFD(3) |
| 4WF-4-WAY-3--018 | 1 | JdJs | 4h2d5d | BET | 4/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_OESD(2) |
| 4WF-4-WAY-3--043 | 1 | AhKs | Qh3h3d | BET | 4/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(2) |
| 4WF-4-WAY-3--059 | 2 | AhAs | QhJh5s | BET | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_GUTSHOT(1), PHANTOM_NFD(2), PHANTOM_OESD(3) |
| 4WF-4-WAY-3--067 | 2 | TcTs | As6s2d | FOLD | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4) |
| 4WF-4-WAY-3--079 | 2 | JdJs | Qh5c3c | CHECK | 4/5 | 1 | PHANTOM_FD(4), PHANTOM_NFD(1) |
| 4WF-4-WAY-3--082 | 2 | AhJh | 8h5c2d | BET | 4/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(2) |
| 4WF-4-WAY-3--097 | 2 | AhKh | 4h5c2d | BET | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_NFD(1) |
| 4WF-4-WAY-3--111 | 3 | AcKd | Qc9h4h | BET | 4/5 | 1 | PHANTOM_FD(4), PHANTOM_NFD(1), PHANTOM_OESD(1) |
| 4WF-MULTIWAY-145 | 3 | JcTs | 9h8h7s | BET | 4/5 | 3 | PHANTOM_FD(3), PHANTOM_GUTSHOT(1), PHANTOM_OESD(3) |
| 4WF-MULTIWAY-151 | 3 | AsAc | Qc6c5sAh | RAISE | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_NFD(2) |
| 4WF-MULTIWAY-170 | 4 | JhTd | 9c8c7d | BET | 4/5 | 3 | PHANTOM_FD(2), PHANTOM_OESD(3) |
| 4WF-MULTIWAY-184 | 4 | 9s5s | 6s7c6h | CHECK | 4/5 | 4 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_OESD(4) |
| 4WF-MULTIWAY-186 | 4 | AsAc | Qc6c5cAh | RAISE | 4/5 | 4 | MISSED_FD(4) |
| 4WF-MULTIWAY-208 | 5 | AsAc | Qc7c4sAh | RAISE | 4/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(2) |
| 4WF-CLOSING--278 | 6 | AsJs | 2s7d5c | FOLD | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_OESD(2) |
| 4WF-CLOSING--297 | 6 | AsAd | Kc9d2d | RAISE | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4) |
| 4WF-RANGE-AS-345 | 7 | Ah4h | Tc8d5d | BET | 4/5 | 1 | PHANTOM_FD(3), PHANTOM_NFD(1), PHANTOM_OESD(1) |
| 4WF-RANGE-AS-346 | 7 | Ks6s | Kd9h7s | CALL | 4/5 | 1 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_GUTSHOT(2), PHANTOM_OESD(3) |
| 4WF-RANGE-AS-365 | 8 | AsKs | Qc5h9s | CALL | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4) |
| 4WF-RANGE-AS-391 | 8 | JdJs | 6s5s3h | CALL | 4/5 | 4 | CONFLATED_BDFD_AS_FD(4), PHANTOM_FD(4), PHANTOM_OESD(1) |
| 4WF-RANGE-AS-394 | 8 | Kc8c | Kh9d7c | CALL | 4/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_OESD(2) |
| 4WF-RANGE-AS-401 | 8 | JsJd | 8d5d3s | CALL | 4/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(1), PHANTOM_OESD(3) |
| 4WF-CHAIN-009-001 | 9 | Tc9s | Jc8h3d | CALL | 4/5 | 4 | PHANTOM_OESD(4) |
| 4WF-MW-AXIS-515 | 9 | Th8h | 7s4d2h9c | CHECK | 4/5 | 4 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_OESD(4) |
| 4WF-4-WAY-SR-660 | 9 | 9s8s | 5s6c2sJc4h | FOLD | 4/5 | 4 | MISSED_FD(3), PHANTOM_OESD(3) |
| 4WF-MW-AXIS-539 | 9 | Td9d | 7c4h2d2h | CHECK | 4/5 | 1 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_GUTSHOT(4), PHANTOM_OESD(1) |
| 4WF-4-WAY-SR-632 | 9 | 9c8c | 3hTs6d | CALL | 4/5 | 3 | PHANTOM_FD(1), PHANTOM_OESD(3) |
| 4WF-4-WAY-3--013 | 1 | Td9h | Ah6h2c | FOLD | 3/5 | 1 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_GUTSHOT(1), PHANTOM_OESD(1) |
| 4WF-4-WAY-3--029 | 1 | AdKd | 8d5s2h | BET | 3/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(1) |
| 4WF-4-WAY-3--037 | 1 | AsKs | 8s5d2c | BET | 3/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(1) |
| 4WF-4-WAY-3--041 | 1 | Td8h | 5h6h2c | FOLD | 3/5 | 1 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_GUTSHOT(2), PHANTOM_OESD(1) |
| 4WF-4-WAY-3--053 | 2 | AsJs | Jc5c4h | CHECK | 3/5 | 2 | PHANTOM_FD(2), PHANTOM_NFD(2), PHANTOM_OESD(1) |
| 4WF-4-WAY-3--056 | 2 | AcKs | Jh7d4d | CALL | 3/5 | 1 | PHANTOM_FD(3), PHANTOM_NFD(1) |
| 4WF-4-WAY-3--065 | 2 | AhJh | 4c5c2d | BET | 3/5 | 1 | PHANTOM_FD(3), PHANTOM_NFD(1) |
| 4WF-4-WAY-3--107 | 3 | AhJh | 6d5c2d | BET | 3/5 | 2 | PHANTOM_FD(3), PHANTOM_NFD(2) |
| 4WF-4-WAY-3--140 | 3 | Kc9c | Td8c6d | CHECK | 3/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_GUTSHOT(2), PHANTOM_OESD(2) |
| 4WF-MULTIWAY-154 | 4 | AcAs | Qs7s5s5h | RAISE | 3/5 | 3 | MISSED_FD(3) |
| 4WF-MULTIWAY-163 | 4 | 9h5h | 8d7d6s | CHECK | 3/5 | 3 | PHANTOM_FD(2), PHANTOM_OESD(3) |
| 4WF-MULTIWAY-164 | 4 | 9s5s | 2d7c6h | CHECK | 3/5 | 3 | PHANTOM_OESD(3) |
| 4WF-CLOSING--218 | 5 | Th8d | 9c4h2dQs | CHECK | 3/5 | 3 | PHANTOM_OESD(3) |
| 4WF-CLOSING--233 | 5 | Tc8s | 9h4c2sQd | CHECK | 3/5 | 3 | PHANTOM_OESD(3) |
| 4WF-CLOSING--255 | 6 | Tc8d | Th6d4d | RAISE | 3/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_OESD(1) |
| 4WF-CLOSING--282 | 6 | KsJd | 7h5d4d | CHECK | 3/5 | 1 | CONFLATED_BDFD_AS_FD(1), PHANTOM_FD(1), PHANTOM_GUTSHOT(2), PHANTOM_OESD(1) |
| 4WF-CLOSING--286 | 6 | Ah9h | Jh7c5d | CALL | 3/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_NFD(3) |
| 4WF-RANGE-AS-354 | 7 | AsKs | Qc4c9s | CALL | 3/5 | 3 | CONFLATED_BDFD_AS_FD(3), PHANTOM_FD(3), PHANTOM_GUTSHOT(1), PHANTOM_OESD(2) |
| 4WF-RANGE-AS-405 | 8 | Td9c | 3c9d6c | CALL | 3/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_OESD(1) |
| 4WF-4-WAY-SR-617 | 9 | AdQd | 8h5s2d | FOLD | 3/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_GUTSHOT(1) |
| 4WF-RANGE-AS-436 | 9 | As4s | Td8c5s | BET | 3/5 | 2 | CONFLATED_BDFD_AS_FD(2), PHANTOM_FD(2), PHANTOM_GUTSHOT(1), PHANTOM_OESD(1) |

---

## Pattern-Matching False-Positive Analysis

The main false-positive source is villain-range discussion. Labellers explain
what draws villains hold (e.g. 'villain's 98s has OESD', 'CO may have diamond FD').
Our pattern matching cannot distinguish hero-draw claims from villain-range mentions.

| Type | False-positive mechanism | Mitigation applied | Residual risk |
|------|--------------------------|--------------------|-|
| PHANTOM_NFD (Type B) | Labeller says 'backdoor nut flush draw' for hero; 'nut flush draw' pattern fires | Negative lookbehind: 'nut flush draw' preceded by 'backdoor' within 15 chars is excluded | LOW — mechanism specific |
| PHANTOM_NFD (Type A/C) | Real errors: hero lacks Ace of FD suit (A) or has no FD at all (C) | None needed | NONE — genuine catches |
| PHANTOM_FD (HIGH-fpr) | Hero has no flush connection; pattern fires on 'villain has flush draw' or 'board has diamond flush draw' | Claims suppressed when 'no flush draw' present in same rationale | MODERATE — suppression incomplete |
| PHANTOM_FD (LOW-fpr) | Hero has BDFD; labeller called it full FD (same as CONFLATED_BDFD_AS_FD) | — | LOW |
| CONFLATED_BDFD_AS_FD | Hero has BDFD, labeller says full FD | All LOW-fpr | LOW — mechanical catch |
| PHANTOM_GUTSHOT | Hero has 0 straight outs; 'gutshot' fires on villain range | claims_no_straight suppression | HIGH (221/224 have 0 hero outs) |
| PHANTOM_OESD | Same — 371/525 have 0 hero outs (villain range) | Same | HIGH for 0-out cases; LOW for 154 cases where gutshot exists |
| MISSED_FD | FD exists, rationale says nothing about it | — | LOW (26 cases, mechanical) |

**Bottom line:** The reliable (LOW-fpr) signal columns are:
- CONFLATED_BDFD_AS_FD: 329 genuine hero board-read errors
- PHANTOM_NFD (Types A+C): ~60 flags, minus Type B false positives
- PHANTOM_OESD (non-zero-outs): ~154 cases of gutshots misclaimed as OESD
- MISSED_FD: 26 cases of unreported flush draws

---

*Generated: 2026-05-30 — scripts/audit_corpus_board_reading_errors.py*
