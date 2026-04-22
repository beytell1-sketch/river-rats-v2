---
date: 2026-04-22
from: Practical-pro reviewer (pass #4, fourth-pass)
to: Orchestrator
re: River Rats v2.4 Stage 3.5 — blueprint v2.3 AMENDED (e940e8d) practical-pro review
authority: origin/master HEAD = e940e8d
---

```
PRACTICAL PRO REVIEW PASS #4

VERDICT: APPROVE_WITH_FIXES

Prior findings fixed:
- 8-entry dry-run enumerated: yes (v2.3 §3.1, lines 508-527, table rows 1-8)
- T_J02 YAML edit spelled out: yes (v2.3 §3.3, lines 595-605 — explicit
  villain_tp_pct=0.60, medium_made=0.18, draw=0.00, air=0.22)
- NaN render wording: clean (commit 11 unchanged from pass #3, no drift)

NEW findings (from pass #4):
- MED-A: v2.3 line 363 `surviving_weight: min(per_villain_truncated.values(),
  ...)` takes min over Dict[str, bool] — yields bool, not float. Q39
  self-flags only the chain_steps nonsense; the surviving_weight line has
  the same "iterating the wrong dict" defect. Replace with
  `min(per_villain_chain_meta[opp]['surviving_weight'] for opp in ...)`
  or analogous. Should be added to Q39 scope or spelled out in commit 4.
- MED-B: No commit 4 gate that asserts v2.2 §3.7 merged=empty bug is
  actually removed (v2.3 §2.2 AFTER replaces but doesn't say "delete
  BEFORE block"). Low-risk, builder discipline on diff review catches it.
- LOW: Q41 left to reviewer — flagged below.

MUST #49 dry-run coverage:
- Shape variety adequate: yes (HU donk, HU four-class, same-street collapse,
  folded-sentinel, overflow, mass-floor truncation, delayed probe, multiway)
- Multiway proportion: adequate for dry-run (1 of 8). The dry-run is a
  shape-variety check, not a multiway-stress check. MUST #52 benchmark
  already runs 100 multiway hands against v2.3.1 CSV in commit 5 — that's
  where multiway coverage density belongs, not in the 8-entry list.
  Non-issue.

MUST #45 tri-state labeller workflow:
- Requires Stage 3 v3.2 prompt addition: nuanced. Labeller side of the
  panel already emits PRIMARY vs CONFIRMED — Stage 3 v3.1 prompt carries
  this distinction. What v3.2 should ADD is a worked example distinguishing
  "drove the decision" (PRIMARY=2) from "supports the decision, checked as
  consistent" (CONFIRMED=1) — currently labellers drift to PRIMARY for
  anything they noticed. Recommendation: file v3.2 prompt ticket (not
  blocking commit 11A); trainer audit log per Q40 catches drift meanwhile.

MUST #57 CONTENT_API v4 version-pin:
- Commit 4 gate on teaching ship: tight — v2.3 §4.3 pins BOTH
  CONTENT_API.md carrying `version: v4.0` AND game adapter importing
  `l3_enriched_v4_0`. Pre-merge grep is manual (consistent with MUST #56
  deferral). If commit 4 merges before teaching ships v4, pre-merge grep
  fails at the `version: v4.0` token absence → block. Gate holds.

MUST #50 bet=0.15 player-sanity: acceptable. 15% river medium_made bet
  matches GTO thin-value density for blocker-driven bets + some range-
  balancing vs polarised check-call villains. Q41's 0.08 alternative is
  too passive for HU; keep 0.15. Q41 resolve: ship 0.15.

MULTIWAY fallback verdict-shift impact: small for most hands; significant
  on: hands where secondary villain has a distinct action chain that
  narrows their range vs primary (e.g. MW-40 flop-check + turn-call vs
  primary MW-30 aggressor). Verdict shift expected on ~5-10% of multiway
  hands in fallback mode. Acceptable for perf-degradation path; should
  be logged so player sees "simplified villain model" badge when fallback
  fires.

MANDATORY CHECKS:
- NotImplementedError/TODO/placeholder: found 1 non-audit-trail `placeholder`
  at v2.3 line 363 (code block, not design note) — see MED-A above.
  Line 34 + 401 placeholder references are audit-trail annotations for
  v2 base file §942, acceptable.
- 8-entry list present: confirmed (lines 508-527)
- T_J01/T_B05/T_J02 commit-13 YAML: spelled (T_J02 explicit per lines
  595-605; T_J01/T_B05 reauthored per MUST #33 referenced at §3.1 row 1+3
  and commit 12 row in §4.5 table)

READY TO IMPLEMENT?: MEDIUM fixes first (fold MED-A surviving_weight bug
  into Q39 scope; then implementation begins per §4.5 commit sequence)
```
