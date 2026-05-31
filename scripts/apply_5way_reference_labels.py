"""
Promote the 5-way reference DRAFT to production JSONL.

Applies expected_action + expected_size_bb based on:
- 7 architect HIGH/MED-HIGH confidence hands (orchestrator sanity-checked rationale)
- 3 architect MEDIUM confidence hands (multi-viewpoint debate panel adjudicated 2026-05-30)

Panel adjudication: MW-51, MW-54, MW-58 all → CALL.
- MW-51: panel unanimous CALL, confirms architect CALL
- MW-54: panel unanimous CALL (R2), OVERRIDES architect's RAISE-primary (rests on phantom-gutshot factual error; A9 on J72 has no gutshot per enumeration)
- MW-58: panel unanimous CALL, confirms architect CALL (with fatter RAISE-mix shoulder ~30-35%)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "review" / "comms" / "DRAFT_5WAY_REFERENCE_PILOT_10HAND_2026-05-22.jsonl"
PROD = ROOT / "data" / "5way_reference_10hand_2026-05-30.jsonl"

LABELS = {
    # Architect HIGH / MED-HIGH (7 hands), rationale sanity-checked
    "MW-52": ("RAISE", 36),   # 4-bet for value with KK in 5-way squeeze pot
    "MW-53": ("RAISE", 14),   # SB closing squeeze with A5s
    "MW-55": ("RAISE", 28),   # turn check-raise value with top-two on Q83J
    "MW-56": ("CALL",  None), # BB closing 4 cold-callers with A4s — pot odds 11.5%
    "MW-57": ("CHECK", None), # TT overpair on paired-board 8842 checked-through
    "MW-59": ("FOLD",  None), # TT under-pair facing polarized river overbet + cold-call monotone
    "MW-60": ("FOLD",  None), # A5 two-pair facing 5-way bet-call-raise chain
    # Architect MEDIUM (3 hands), debate-panel adjudicated 2026-05-30
    "MW-51": ("CALL",  None), # K9 TPweak IP-closing 5-way (panel unanimous CALL)
    "MW-54": ("CALL",  None), # A9hh NFD 5-way (panel unanimous CALL — overrides architect RAISE)
    "MW-58": ("CALL",  None), # 88 bottom set on T98 5-way bet-raise (panel unanimous CALL)
}


def main():
    records = []
    with DRAFT.open() as f:
        for line in f:
            if not line.strip():
                continue
            d = json.loads(line)
            hid = d["hand_id"]
            assert hid in LABELS, f"Unknown hand_id {hid}"
            action, size = LABELS[hid]
            d["expected_action"] = action
            d["expected_size_bb"] = size
            # Strip architect-meta fields per design memo's production schema
            for k in ("architect_suggestion", "architect_confidence", "rationale_summary"):
                d.pop(k, None)
            records.append(d)
    assert len(records) == 10, f"Expected 10 records, got {len(records)}"

    PROD.write_text("\n".join(json.dumps(r) for r in records) + "\n")
    print(f"Wrote {len(records)} production records to {PROD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
