---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #169 (12.5H-B situation generation; 90 hands across 6 templates) — APPROVE; 1 NIT (design §4/§8 inconsistency vs §3)
severity: NIT (1 — design-document arithmetic inconsistency, not builder issue)
status: FLAG → APPROVE for merge
test-class: TC-23 + V-Source + dispatch §"Distribution sanity" + §"Convention uniformity" + §"NEW: design_action per T-CONTROL hand"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 10th successive cycle solo-routed)
---

# QC Review — PR #169 (12.5H-B situation generation): APPROVE; 1 NIT

## Verdict

**APPROVE PR #169 for merge.** All 5 dispatch-required audits PASS. Builder matches design §3 (the canonical per-template count table) exactly: T8'=18, T9'=14, T10'=14, T7-ext=12, T-RAISE-stabilize=12, T-CONTROL=20. **All 20 T-CONTROL hands carry the new `design_action` field — the TC-X T8 schema gap fix QC surfaced in PR #150 NIT now operational as a first-class data field.** Convention uniformity: 0 violations of 90 hands.

One NIT-class observation about design-document internal inconsistency (§4 + §8 don't agree with §3 on T-CONTROL count); builder correctly resolved by following §3.

QC FLAG-only role per CLAUDE.md.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR169_2026-05-06.md` master `cef76a7` + PR #168 dispatch)

5 audits — 3 standard (diff scope, citation, distribution) + 2 NEW for 12.5H-B (convention uniformity, design_action per T-CONTROL).

PR #169 head: `e04d597` (branch `programmer/phase125h-b-situation-generation-2026-05-06`). Merge-base: `8c90649` (= PR #168 = 12.5H-B dispatch SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 4 files; no edits to existing source surfaces or existing 604-corpus data files"*

| File | category |
|---|---|
| `scripts/build_corpus_revision_125h_situations.py` | NEW (12.5H factory script) |
| `data/corpus_revision_125h_situations_2026-05-06.jsonl` | NEW (84 parametric) |
| `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` | NEW (6 manuals) |
| `review/comms/BUILDER_REPORT_PHASE125H_B_SITUATION_GENERATION_2026-05-06.md` | NEW (report) |
| **Total** | **4 files** ✓ |

- File count = 4 ✓
- Zero edits to `data/corpus_revision_500_hand_*` (existing 494-corpus locked) ✓
- Zero edits to `data/corpus_revision_125e_*` (existing 110-corpus locked) ✓
- Zero edits to `data/corpus_combined_604_*` (existing combined corpus locked) ✓
- Zero edits to `prompts/gto_labeller_v3.*` (locked) ✓
- Zero edits to `river-rats-core/` ✓ (Path Y discipline holds)

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

9 distinct file paths cited in builder report:

| Citation | Status |
|---|---|
| `data/corpus_combined_604_2026-05-05.jsonl` | ✅ TRACKED (existing combined corpus) |
| `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | ✅ TRACKED (reference set source) |
| `prompts/gto_labeller_v3.4.md` | ✅ TRACKED (locked v3.4 prompt) |
| `review/comms/PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md` | ✅ TRACKED (12.5H-A design) |
| `scripts/build_corpus_revision_125e_situations.py` | ✅ TRACKED (12.5E-B precursor factory) |
| `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` | NOT-TRACKED ✓ expected (NEW in PR) |
| `data/corpus_revision_125h_situations_2026-05-06.jsonl` | NOT-TRACKED ✓ expected (NEW in PR) |
| `review/comms/BUILDER_REPORT_PHASE125H_B_SITUATION_GENERATION_2026-05-06.md` | NOT-TRACKED ✓ expected (NEW in PR; self-reference) |
| `scripts/build_corpus_revision_125h_situations.py` | NOT-TRACKED ✓ expected (NEW in PR; self-reference) |

**Citation existence: CLEAN.**

## Audit 3 — Distribution sanity ✅ CLEAN at design §3 (with design-doc inconsistency NIT)

### Total + cohort breakdown

| Quantity | Observed | Design §4 | Match |
|---|---|---|---|
| Combined hands | **90** | 90 | ✅ |
| Parametric | **84** | 84 | ✅ |
| Manual canonicals | **6** | 6 | ✅ |

### Per-template counts (design §3 line 170 spec)

Design §3 has the canonical per-template count table at line 170. Builder matches exactly:

| Template | Parametric | Manual | Combined | Design §3 | Match |
|---|---|---|---|---|---|
| T8' (MW-25 monotone-FD checked-through 4-way) | 16 | 2 | **18** | 18 | ✅ exact |
| T9' (MW-40 TP-medium-kicker IP 4-way after PFR check) | 13 | 1 | **14** | 14 | ✅ exact |
| T10' (MW-45 slowplay set turn lead 4-way) | 13 | 1 | **14** | 14 | ✅ exact |
| T7-ext (MW-17 nut-blocker + overcards CALL pot odds 3-way) | 11 | 1 | **12** | 12 | ✅ exact |
| T-RAISE-stabilize (MW-47 + 60/40 bimodal fix; bet+call multiway) | 11 | 1 | **12** | 12 | ✅ exact |
| **T-CONTROL** (drift detection across 5 buckets w/ design_action) | 20 | 0 | **20** | 20 | ✅ exact (per §3 line 170) |
| **Total** | **84** | **6** | **90** | **90** | ✅ |

All 6 templates match design §3 exactly. Within ±1 dispatch tolerance — well within (variance = 0 across all 6).

### NIT-1 — design-document internal inconsistency on T-CONTROL count

While the canonical §3 line 170 specifies T-CONTROL = 20, two other sections of the same design contradict:

- **§4 enumerated math (line 187-198 class-distribution table):** T-CONTROL contributes only 4 FOLD + 6 CHECK + 2 CALL = 12 hands (no BET or RAISE breakouts). Total table rows sum to 82, but the Total row claims 90 — 8-hand arithmetic gap.
- **§8 workstream output spec (line 320):** *"~84 parametric hands; 18 T8' + 14 T9' + 14 T10' + 12 T7-ext + 12 T-RAISE-stabilize + **14 T-CONTROL parametric**, leaving 6 control + 6 manuals out"* — says 14 T-CONTROL parametric (vs §3 line 170 = 20).

So 3 different T-CONTROL counts in the same design: §3 = 20 (canonical), §4 = 12 (enumerated), §8 = 14 (workstream output spec). Builder followed §3 (the per-template count table is the natural authority); the §4 + §8 inconsistencies are stale / template-residue.

**Why it matters:** a future-cycle reviewer reading §4 first or §8 first would see a different count and potentially flag the builder PR as over-spec. Builder's actual T-CONTROL distribution (CHECK 6 + BET 5 + FOLD 4 + CALL 3 + RAISE 2 = 20) covers all 5 action buckets cleanly per §3's "drift detection across 5 buckets" stated purpose, which §4's FOLD/CHECK/CALL-only enumeration doesn't reflect.

**Severity:** NIT. Same V-X4 family as past cycles (template residue / partial section updates). The 12.5H-A design itself has the inconsistency; builder is correctly resolved against §3.

**Suggested fix-forward (advisory):** in 12.5H-C/D/E builder cleanup window or 12.5H-A design amendment, reconcile §4 + §8 to match §3. Specifically:
- §4 class-distribution table rows should add up to 90 (currently sum to 82); add T-CONTROL BET 5 + RAISE 2 + extra CALL 1 to the enumeration, OR change phrasing to indicate §4 is "core enumeration; T-CONTROL fills remaining via mixed buckets per §3".
- §8 line 320: change "14 T-CONTROL parametric" → "20 T-CONTROL parametric" to match §3.

**Distribution sanity: CLEAN at design §3 level. 1 NIT for design-document internal inconsistency.**

## Audit 4 — Convention uniformity ✅ CLEAN (0 violations of 90)

**Dispatch:** *"empirically verify all 90 `prior_actions` use hero-only convention; zero non-hero actions"*

Programmatic check: parsed every `prior_actions` array across both jsonls; for each action string, extracted the actor (token after `street: `) and compared against the row's `hero_position`.

| Dataset | Rows | Convention violations |
|---|---|---|
| Parametric | 84 | **0** |
| Manual canonicals | 6 | **0** |
| **Total** | **90** | **0** |

Hero-only convention applied uniformly per Path B precedent (12.5E-B amendment). Zero exceptions.

**Convention uniformity: CLEAN.**

## Audit 5 (NEW) — design_action present per T-CONTROL hand ✅ CLEAN

**Dispatch:** *"verify each T-CONTROL row has explicit `design_action` field (per TC-X T8 schema gap fix from PR #150); G4 same-action match relies on this for 12.5H-D drift detection"*

This is the **first operational instance of the TC-X T8 schema gap fix** that QC surfaced as a NIT in `REVIEW_QC_PHASE125E_D_CORPUS_QC_2026-05-05.md` (master `4070a11`, PR #150). The orchestrator pulled the curative forward into 12.5H as a required field.

| Check | Result |
|---|---|
| T-CONTROL hands found | 20 (parametric only; no T-CONTROL manuals per design) |
| T-CONTROL hands with `design_action` field | **20 / 20** ✅ all present |
| `design_action` is T-CONTROL-only (not present on H-FEAT/E-DIST templates) | ✅ confirmed (T-CONTROL-only fields = `{'design_action'}`) |

### T-CONTROL `design_action` distribution

| design_action | count | matches design §4 enumeration? |
|---|---|---|
| CHECK | 6 | ✓ matches §4 "6 T-CONTROL CHECK" |
| BET | 5 | (not enumerated in §4 — see NIT-1) |
| FOLD | 4 | ✓ matches §4 "4 T-CONTROL FOLD" |
| CALL | 3 | §4 enumerates 2; +1 over (see NIT-1) |
| RAISE | 2 | (not enumerated in §4 — see NIT-1) |
| **Total** | **20** | matches §3 line 170 exactly |

The 7 hands beyond §4's enumeration (5 BET + 2 RAISE) plus the 1 extra CALL fill the 8-hand gap between §4's enumerated 12 and §3's stated 20.

**Why this is the right design:** T-CONTROL is "drift detection across 5 buckets" per §3 line 153. To detect drift across all 5 action classes, T-CONTROL needs samples in each of FOLD/CHECK/CALL/BET/RAISE. Builder's distribution covers all 5 buckets (4/6/3/5/2 per class). §4's FOLD/CHECK/CALL-only enumeration would have made T-CONTROL drift-blind on BET + RAISE.

**design_action per T-CONTROL: CLEAN.** Schema gap fix from PR #150 NIT now operational.

## Bonus — TC-X T8 schema gap fix (PR #150 NIT) operationally promoted

QC surfaced this NIT in 2026-05-05 PR #150 review:
> *"NEW NIT: T8 schema gap. T8 control situations all carry generation_source = 't8_controls' (uniform); no design_action field per hand. Exact same-action match indeterminate. Suggested fix-forward: encode design_action per T8 hand when situation factory generates."*

The 12.5H-B dispatch + this PR demonstrate the curative pattern:
1. QC NIT in PR #150 review (2026-05-05)
2. Orchestrator queued for 12.5H+ work
3. 12.5H-A design §3 line 153: "T-CONTROL drift detection across 5 buckets w/ design_action"
4. 12.5H-B dispatch §"NEW audit 5": *"verify each T-CONTROL row has explicit design_action field (per TC-X T8 schema gap fix from PR #150)"*
5. 12.5H-B builder: all 20 T-CONTROL hands carry design_action; T-CONTROL-only field
6. This QC audit: verify operational ✓

**Closes the loop.** Same QC-curative-becomes-design-gate pattern as TC-X-CAP-BINDING-PRE-CHECK (queued from 12.5G; promoted to §7 G5 in 12.5H-A design). Forward-active when 12.5H-D fires G4 drift detection (now uses design_action per-hand match instead of aggregate-class approximation).

## What QC did NOT audit (scope partition)

- **Per-hand poker correctness** of the 6 manual canonicals (specific hero/board choices; whether T8' AsKh on Js9s4s actually exemplifies "monotone-FD checked-through 4-way") — gto-expert review at 12.5H-C dispatch
- **v3.4 protocol fit** for the new templates (would labellers actually produce the expected per-template consensus actions?) — gto-expert + Opus tier-up cross-check at 12.5H-C
- **Discriminative axis verification** (would `extract_all_features` produce the expected feature signatures on the new hands?) — out of scope; would be ml-architect review or 12.5H-D corpus QC bonus check
- **Per-T-CONTROL match-pair construction** (whether each T-CONTROL hand has a near-equivalent in the existing 604 corpus per design §6.3 line 292) — could be checked at 12.5H-D G4 drift detection time

## Test class implication

- **TC-X T8 schema gap fix operationally promoted** — the design_action field is now standing infrastructure. Future T-CONTROL-style drift-detection situation factories should carry the field by default.
- **TC-X-METHODOLOGY-INCORPORATION pattern continues** — design §3 cite + dispatch require + builder produce + QC verify is now a 4-step pipeline for QC-queued curatives. Pattern reproducible.
- **NIT-1 design-document inconsistency** — same V-X4 family. Could become **TC-X-DESIGN-DOC-CONSISTENCY** sub-vector if it recurs: when a design enumerates the same quantity in multiple sections (template counts, file paths, version numbers), QC verifies they reconcile. For now, surfaced as a one-off NIT.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **10th successive cycle solo-routed**. Loop heartbeat (25min self-pace) detected trigger landing within ~1 min of master push (loop tick fired immediately on `/loop` invocation). Dynamic /loop continues to work as designed.

## References

- PR #169: https://github.com/beytell1-sketch/river-rats-v2/pull/169
- PR #169 head: `e04d597`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR169_2026-05-06.md` (master `cef76a7`, PR #170)
- 12.5H-B dispatch: `MAIN_TERMINAL_PHASE125H_B_DISPATCH_2026-05-06.md` (master `8c90649`, PR #168)
- 12.5H-A design (§3 line 170 = canonical per-template counts): master `858b032` (PR #165)
- TC-X T8 schema gap fix origin: `~/river-rats-v2/review/comms/REVIEW_QC_PHASE125E_D_CORPUS_QC_2026-05-05.md` (PR #150)
- TC-X-CAP-BINDING-PRE-CHECK + TC-X-CROSS-SEED-IMPORTANCE class definitions: QC commit `7354fad`
- Memory: `feedback_qc_routing_when_standalone_active.md` (10th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #169 for merge.** All 5 audits PASS. 1 NIT (design-document internal inconsistency on T-CONTROL count: §3 = 20, §4 = 12 enumerated, §8 = 14; builder correctly resolved against §3).

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5H-C dispatch (labelling round with pilot+full + Opus tier-up cross-check + GTO-EXPERT review of manual canonicals)
- NIT-1 ride-along at 12.5H-A amendment or 12.5H-C/D/E cleanup window
