---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (architect hat)
re: PR #165 (12.5H-A corpus expansion design — 90 hands; secondary gate cross-seed nut_flush_block ≥0.04) — APPROVE; 1 NIT
severity: NIT (1 — self-reference XX placeholder); no HIGH/MEDIUM
status: FLAG → APPROVE for merge
test-class: TC-23 (diff scope) + V-Source (citation existence) + dispatch §"NEW: Methodology incorporation" (6 rules from §10)
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 9th successive cycle solo-routed)
---

# QC Review — PR #165 (12.5H-A design): APPROVE; 1 NIT

## Verdict

**APPROVE PR #165 for merge.** All 3 dispatch-required audits PASS. All 6 methodology rules from dispatch §10 reflected in design as §10.1-§10.6 with matching sub-section structure AND operationalized into design's pre-flight gates + sub-phase exit criteria. One NIT (self-reference uses XX placeholder while actual filename is `2026-05-06`).

QC FLAG-only role per CLAUDE.md.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR165_2026-05-06.md` master `aef8156` + PR #164 dispatch)

3 audits — smallest scope of any 12.5E-G/H cycle PR (design-only).

PR #165 head: `c95d83a` (branch `programmer/phase125h-a-design-2026-05-06`). Merge-base: `5f9c507` (= PR #164 = 12.5H-A dispatch SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 1 file (design comm); analysis-only; no code/corpus/labels/prompt edits"*

| File | additions | deletions | category |
|---|---|---|---|
| `review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md` | (full design) | 0 | NEW (design comm) |
| **Total** | (single file) | **0** | **1 file** ✓ |

- File count = 1 ✓
- Zero `scripts/`, `river-rats-core/`, `prompts/`, `data/` edits ✓
- All-additions ✓ (analysis-only)

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN (1 NIT)

24 distinct file paths cited in design + 12 PR refs + 12 master SHA refs.

### File path resolution at master HEAD

| Category | Count | Status |
|---|---|---|
| TRACKED at master | 16 | ✅ all resolve |
| NOT-TRACKED — forward 12.5H-B/C output paths with `XX` date placeholder | 6 | ✓ expected (paths not yet generated; XX correctly used as date placeholder) |
| NOT-TRACKED — `gto_model_v9_student.json` | 1 | ✓ expected (correctly absent per no-promotion at 12.5E-E/G) |
| NOT-TRACKED — design self-reference at line 312 | 1 | ⚠️ NIT — see below |

### NIT-1 — self-reference uses XX placeholder

Design line 312 (§8 12.5H-A row): *"Output: `review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-XX.md` (this doc)"*

The actual filename is `PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md`. Self-reference in §8 still uses `2026-05-XX` placeholder — would have been correct at design-template authoring time but was not updated when the filename was filled to `2026-05-06`.

**Why it matters:** reader of §8 sees `(this doc)` parenthetical and reconciles, but a tool that grep-matches paths from the design (e.g. dependency tracker, future cycle's design-template-extraction script) would mis-resolve.

**Severity:** NIT. Forward XX placeholders for not-yet-generated files (corpus/labels/manuals jsonls in 12.5H-B output) are correctly used; only the self-reference is stale. Same V-X4 family as past cycles (preserved-original / template-residue).

**Suggested fix-forward (advisory):** edit line 312 to `PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md (this doc)`, or 12.5H-B/C/D/E/F builder updates as part of cleanup ride-along window.

### PR/SHA refs (12 PRs cited)

PR #122, #133, #136, #137, #146, #150, #152, #155, #157, #161, #164 — all merged + verifiable in `git log origin/master --oneline`. Master SHAs likewise verifiable.

**Citation existence: CLEAN with 1 NIT.**

## Audit 3 — Methodology incorporation ✅ COMPLETE

**Dispatch:** *"verify all six methodology rules from §10 are reflected in the design"*

### §10 sub-section structure (verified verbatim against dispatch §10 enumeration)

| Dispatch rule | Design subsection | Status |
|---|---|---|
| Cross-seed importance reporting (TC-X-CROSS-SEED-IMPORTANCE) | §10.1 (line 413) | ✅ named + scoped |
| Cap-binding pre-flight check (TC-X-CAP-BINDING-PRE-CHECK) | §10.2 (line 419) | ✅ named + scoped |
| Tier-up verification on training-data outputs | §10.3 (line 423) | ✅ named + scoped |
| Pilot-first on all long batches | §10.4 (line 427) | ✅ named + scoped |
| Hero-only convention in `prior_actions` | §10.5 (line 431) | ✅ named + scoped |
| Pre-flight join-cardinality ≥0.99 | §10.6 (line 435) | ✅ named + scoped |

### Operationalization beyond enumeration

The design doesn't just list the rules — it **operationalizes them into pre-flight gates + sub-phase exit criteria:**

- **Cross-seed reporting (rule 1):** §8.E exit gate (line 354): "report file produced with cross-seed importance for `nut_flush_block` (and other P1 blockers)"
- **Cap-binding (rule 2):** §7 G5 gate (line 298): NEW G5 cap-binding pre-flight check; design itself runs the check at line 200 ("90 RAISE in 694 corpus: train slice 80% → ~75 RAISE; mean ≈ 555/5 = 111; max boost = 111/75 = 1.48× — STILL below cap=3.0")
- **Tier-up verification (rule 3):** §8.C exit gate (line 336): "orchestrator-side Opus tier-up cross-check on T-RAISE-stabilize + T8'/T9'/T10' MW-exact-replica labels for 'labels final' verdict"
- **Pilot-first (rule 4):** §6.5 (line 241): pilot before full batch labelling explicitly required
- **Hero-only (rule 5):** §6.5 + builder workstream §8.B output spec
- **Pre-flight join-cardinality (rule 6):** §6.5 "≥0.99 join-cardinality gate" (line 94 + §10.6)

This is the methodology-rules-as-test-classes pattern: each rule has a designed-in pre-flight gate or exit criterion. **TC-X-CAP-BINDING-PRE-CHECK has been promoted from QC's queued curative to a first-class design gate (§7 G5) at 12.5H-D.**

**Methodology incorporation: COMPLETE.** All 6 rules incorporated as named subsections + operationalized as gates.

## Bonus observation — TC-X-CAP-BINDING-PRE-CHECK promoted to design gate

QC queued TC-X-CAP-BINDING-PRE-CHECK on 2026-05-05 (commit `7354fad`) following 12.5G's empirical refutation of cap-as-lever. The 12.5H-A design has now **promoted this from a QC queued curative to a first-class design gate** (§7 G5 at the 12.5H-D corpus-QC phase).

The design even pre-runs the check at line 200 to verify 12.5H's 694-corpus state will still be cap-non-binding: max boost = 1.48× < cap=3.0. So 12.5H proceeds with the established methodology, with the cap-binding question pre-empirically settled.

This is the test-class-becomes-design-gate pattern: a QC curative pulled forward into the dispatch's design phase. Forward-actionable for any future cycle where a cap-tuning workstream is considered (12.5I or beyond).

## What QC did NOT audit (scope partition)

- **Design substance** (whether 90 hands targeting 5 stay-wrong refs is the right number; whether secondary gate ≥0.04 is the right threshold) — orchestrator scope; QC verifies methodology incorporation, not strategic design choices
- **Per-template count math** (90 = 18 T8' + 14 T9' + 14 T10' + 12 T7-ext + 12 T-RAISE-stabilize + 14 T-CONTROL + 6 manual ≈ 90 — already documented in §6 + §7) — out of scope; QC treats design counts as authoritative if internally consistent
- **gto-expert review** of T-RAISE-stabilize design — gto-expert hat scope per dispatch §"What's queued"
- **ml-architect review** of secondary gate threshold — ml-architect hat scope; cross-seed median ≥0.04 vs current 0.0268 is design judgment

## Test class implication

- **TC-X-CAP-BINDING-PRE-CHECK promoted to design gate** — first instance of a QC-queued curative being pulled into design phase as G5 gate. Strong signal that QC's institutional memory is influencing forward design.
- **Methodology-rules-as-test-classes pattern** — design §10 enumerates rules + design body operationalizes them as gates. This pattern could become a TC-X-METHODOLOGY-INCORPORATION sub-vector for future design-comm audits: verify every rule in §10 has a corresponding operationalization elsewhere in the design (gate, exit criterion, pre-flight).
- **NIT-1 (self-reference XX placeholder)** — same V-X4 family as past cycles. Pattern recurrence-watch: template residue surviving filename fills.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **9th successive cycle solo-routed**. Loop heartbeat detected trigger landing within ~7min of master push (loop tick fired immediately on `/loop` invocation). Dynamic /loop self-pacing working as designed.

## References

- PR #165: https://github.com/beytell1-sketch/river-rats-v2/pull/165
- PR #165 head: `c95d83a`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR165_2026-05-06.md` (master `aef8156`, PR #166)
- 12.5H-A dispatch: `MAIN_TERMINAL_PHASE125H_A_DESIGN_DISPATCH_2026-05-06.md` (master `5f9c507`, PR #164)
- 12.5H-pre cross-seed (precursor to 12.5H-A): master `edd5556` (PR #161)
- TC-X-CAP-BINDING-PRE-CHECK class definition: `~/river-rats-qc/learning/test_class_registry.md` (commit `7354fad`)
- TC-X-CROSS-SEED-IMPORTANCE class definition: same
- Memory: `feedback_qc_routing_when_standalone_active.md` (9th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #165 for merge.** All 3 audits PASS; 1 NIT (self-reference XX placeholder; advisory).

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5H-B dispatch (situation generation)
- 12.5H-A NIT-1 ride-along at 12.5H-B/C/D/E/F builder cleanup window
