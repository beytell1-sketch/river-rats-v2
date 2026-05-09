---
date: 2026-05-09
from: Main terminal (orchestrator)
to: QC stream
re: PR #307 rev 2 — Phase 1.5-A unified-59-surface design memo (architect amend addressing SHOULD_FIX-1 + NIT-1; new owner-scope α/β item) — fire delta audit now
status: TRIGGER — fire now
---

# QC stream — fire delta audit now on PR #307 rev 2

PR #307 head advanced from `6164f14a6a98c3ec09ace3d0c624da6c558eb519` (rev 1) to `c7502e3f74f82318b82e3fe0c5b1cda3ecf5f16d` (rev 2). Architect amended per owner direction (Path A+: fix in PR #307, do not fix-forward in 1.5-B). Diff: 2 files / +83 / −28. Single rev-2 commit (`c7502e3` "Builder Phase 1.5-A rev 2: SHOULD_FIX-1 + NIT-1 fixes + owner-scope item added (Path A+)").

Pre-merge QC required per `feedback_qc_required_before_approval.md` (PR #307 is the design lock for the entire 1.5 workstream — milestone-class).

## Delta-audit scope (~10 min; focused on amend sections only)

This is a delta audit, NOT a full re-audit. The 11-item rev-1 audit (PR #311 verdict; PASS-WITH-FINDINGS · 0/1/1) carries forward on unchanged sections. QC verifies ONLY the amended sections + cross-cutting consistency.

### §1.2 — re-attestation against SHOULD_FIX-1

1. **Verification method correct**: §1.2 uses git-tracked verification (`git ls-files` / `git cat-file -e <ref>:<path>` / `git log --all -- <path>`) per `feedback_tc23_existence_must_be_git_tracked.md`. NOT `test -e` (which produced the rev-1 false negative).
2. **Result tabulation**: 17 GREEN / 2 RED across 19 cited paths (per amend commit message). QC verifies the count + the GREEN/RED labeling per actual git state at master `9c3b9ae`.
3. **2 RED documented faithfully**: `gto_model_v8_hu.json` + `gto_model_v8_38feat.json` — local FS exists (~11.7 MB each) but never git-tracked (`.gitignore` line 3: `*.json`; never force-added). Production-runtime status (router loads them) distinguished from git-provenance (absent).
4. **Inventory of other production-referenced-but-not-tracked model paths**: flagged for separate post-Phase-1.5 provenance-cleanup workstream. QC verifies the inventory exists + scope is clearly post-1.5.

### §4.2 cascade — close-hand-anchor model + new owner-scope α/β

5. **Owner-scope flag correctness**: §4.2 explicitly flags Path α (commit v8 artifacts to git; ~23 MB / ~38% repo growth on current 61 MB `.git`) vs Path β (re-anchor on v9-3way-on-59 model uncertainty) as **owner-scope decision**, NOT silently committed by architect. Per `feedback_orchestrator_decides_not_recommends.md`: experts recommend HOW (architect recommends β with reasoning); owner decides WHAT/WHETHER.
6. **Architect-hat recommendation present**: Path β recommended; reasoning cites repo growth tax, v9-3way handles HU via existing 59-feature surface, 1.5-C verification on critical path. Per `docs/PROCESS_GUIDE.md` §1.4: "experts must make clear recommendations with reasoning — not present menus". Verify the reasoning is committed-path style, not "open question".
7. **Gate timing correct**: owner directs Path α or Path β BEFORE 1.5-D.1 fires (not before 1.5-A merge). 1.5-A and 1.5-B and 1.5-C are unblocked by this owner-scope deferral.

### §4.5 cascade — lineage anchor reframing

8. **Reframing accuracy**: v8-HU-38 reframed from "lineage anchor (provenance only)" → "production-runtime-anchor without git provenance". Confirms the actual state (router loads v8 at runtime; not in git history). From-scratch HU retrain commitment unaffected (architect kept the commit).

### §4.6 cascade — production-swap framing

9. **Filename-pointer framing**: Production-swap reframed from "REPLACED in production" → "filename-pointer change at `oracle_router.py:34`". QC verifies `oracle_router.py:34` actually exists at master `9c3b9ae` and references the v8 model filename (TC-23 EXISTENCE on the cited line).
10. **1.5-E force-add commitment**: Architect commits to force-add the new HU model to git at 1.5-E (avoiding the v8 git-tracking gap recurring). Verify this commitment is explicit in §4.6 + any 1.5-E sub-phase spec in §5 / §4.7.

### NIT-1 fix

11. NIT-1 from PR #311 verdict — QC verifies the architect's fix matches the verdict's NIT-1 specification.

### Cross-cutting

12. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): rev-2 diff = 2 files (`BUILDER_REPORT_PHASE15A_2026-05-08.md` + `PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`). NO source / prompt / data / model edits.
13. **Single committed path preserved**: amend did not introduce new "open technical questions" elsewhere in the memo. Only the 1 owner-scope α/β flag (which IS genuine owner-scope per §4.2 reasoning).
14. **TC-X-DISPATCH-COMPLIANCE**: rev 2 addresses both findings from PR #311 verdict explicitly — no findings carried over un-addressed; no scope creep beyond addressing those findings.
15. **TC-X-OWNER-SCOPE-DISCIPLINE** continued: 6 negative-scope items from the original dispatch still held; new owner-scope α/β flag added is well-formed.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~10 min wall-clock (delta audit on paragraph-level changes). QC writes:
- `~/river-rats-qc/findings/2026-05-09-pr307-phase15a-design-rev2.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15A_DESIGN_REV2_2026-05-09.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master per `project_qc_heartbeat_convention.md`

## What gates

- PR #307 merge → on QC PASS (delta audit) + owner explicit `fire now` per going-forward rule
- After PR #307 merges → orchestrator dispatches Phase 1.5-B execution sub-phase (drafted; ready to author per design memo §2)
- Owner-scope α/β decision → independent gate; resolves before 1.5-D.1 fires (NOT before 1.5-A merge; non-blocking for 1.5-B / 1.5-C)
- LOOP CONTINUES

## Background — owner direction context

Per architect's amend commit message (`c7502e3`): owner directed Path A+ on 2026-05-09 (fix in PR #307, do not fix-forward in 1.5-B). Architect amended accordingly, addressing SHOULD_FIX-1 + NIT-1 + flagging the §4.2 v8-commit-vs-re-anchor trade-off as owner-scope rather than silently committing. Solid orchestration discipline; the new α/β flag is exactly the kind of "genuine owner-scope trade-off" the original dispatch §"Methodology constraints" carved out.

Orchestrator note: the architect explicitly cited `feedback_tc23_existence_must_be_git_tracked.md` (the new memory rule from PR #310's drift retro) when re-attesting §1.2. Closure of the loop: drift retro → memory rule → architect-hat applied it → QC verifies. Cross-stream learning capture working as designed.

## References

- PR #307 rev 2 head: `c7502e3f74f82318b82e3fe0c5b1cda3ecf5f16d`
- PR #311 (rev 1 verdict; PASS-WITH-FINDINGS · 0/1/1): OPEN; merges alongside or after PR #307 on rev-2 PASS
- Phase 1.5-A dispatch: `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (master `5863f13`, PR #306)
- Rev-1 trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR307_2026-05-08.md` (master `832d6d1`, PR #309)
- Drift retro + new TC-23 git-tracked rule: master `9c3b9ae` (PR #310)
- Memory rules: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire delta audit now on PR #307 rev 2. ~10 min (paragraph-level deltas; rev-1 audit carries on unchanged sections). Heartbeat sync to current master at end of tick.**
