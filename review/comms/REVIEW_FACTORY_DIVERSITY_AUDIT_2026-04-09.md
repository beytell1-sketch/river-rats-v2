# Review: Factory Diversity Audit

**Reviewer:** Process reviewer
**Date:** 9 April 2026
**File reviewed:** review/FACTORY_DIVERSITY_AUDIT.md

**VERDICT: PASS — strong deliverable**

---

## Assessment

This is the most thorough audit produced in the project so far. It
answers the owner's question directly: the existing factory has real
diversity problems (SPR uniformity, OOP concentration, villain-feature
constants within boards), and the audit produces concrete, measurable
requirements to prevent the same problems in the new batch.

## What went well

**Data-driven.** Every claim is backed by counts from the actual JSONL
files. SPR=1.11 on 80/151 Batch 1 situations, OOP at 65%, monotone
at 11% vs 5% real-world — these are verifiable numbers, not opinions.

**Concrete requirements (R1-R7).** Each requirement has a number, a
threshold, and a measurement method. The reviewer checklist (Section 6)
maps directly to these requirements. This is reviewable — I can verify
every item with a count or range check.

**Per-sub-pattern variation specs (Section 4).** Instead of saying
"vary the boards," the audit specifies exactly what must vary within
each sub-pattern: feature ranges, minimum unique boards, position
splits, street distributions. SP5 alone has 9 variation requirements.

**Honest about existing problems.** The SPR uniformity finding
(Concern 1) is significant — over half of Batch 1 uses an unrealistic
SPR that "almost never occurs in real 3-way flop spots at 100bb."
The audit doesn't minimize this.

## Findings

**[NOTE] No issues found.** The audit is thorough, data-driven,
and produces actionable requirements with a verification checklist.

**[NOTE] The reviewer checklist (Section 6) is exactly what I need.**
14 measurable checks I can run against the new batch when it's
delivered. This makes my review job concrete — count, compute range,
verify. No judgment calls needed on most items.

**[NOTE] Concern 1 (SPR uniformity) is the most important finding.**
The new batch's R3 requirement (4 SPR tiers, no tier above 25%)
directly addresses this. Worth monitoring: when the full training set
is assembled (existing + new), check whether the existing SPR=1.11
cluster still dominates the combined dataset.

**[NOTE] Concern 4 (HU board in 3-way training) is worth tracking.**
The audit recommends awareness, not removal. If the new batch includes
HU boards, they should be clearly marked. Agree.

## Process Compliance

| Rule | Followed? | Evidence |
|------|-----------|----------|
| §3.1 Research before design | Yes | Audit of existing data before designing new batch |
| §3.2 Sources | N/A | Internal data audit, not external research |
| §1.4 Expert recommends | Yes | Concrete requirements, not options |
| §4.1 Present for review | Yes | In review/ folder |

## Recommendation

Ready for owner approval. The 14-item reviewer checklist should be
the acceptance criteria for the new factory batch — when the batch
is delivered, I will verify against this checklist.

The factory brief v2 should be updated to reference these diversity
requirements (R1-R7) before the factory build begins. The builder
should not start designing boards until both the brief and the
diversity requirements are approved together.
