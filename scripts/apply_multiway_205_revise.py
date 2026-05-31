"""
Apply the 4WF-MULTIWAY-205 action-overturn from the mechanical board-reading
audit screening (2026-05-30 / PR #481).

Owner authorized 2026-05-31 ("please execute all six steps").

Spot: hero 9s5s on 8c7c4h, 4-way SRP, hero non-PFA, facing_bet=0 (checked
to hero). Original consensus: BET 66% (5/5 Sonnet unanimous).

Mechanical board read: 0 BDFD for hero (only 2 spades total, both in hero's
hand), only GUTSHOT to 6 (4 outs). Phantom NFD + phantom OESD in labellers'
rationales inflated equity ~15-22pp. Corrected equity ~18-24% probing into
3 villains' check-back ranges is negative-EV; CHECK preserves realization.

First confirmed action-overturn from the corpus audit (1/450 corpus-label
delta).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSENSUS = ROOT / "data" / "4way_corpus" / "full_700" / "batch_005_consensus_v2.jsonl"

SPOT = "4WF-MULTIWAY-205"
NEW_ACTION = "CHECK"


def main():
    records = [json.loads(line) for line in CONSENSUS.read_text().splitlines() if line.strip()]
    touched = 0
    for rec in records:
        if rec.get("spot_id") == SPOT:
            rec["consensus_action"] = NEW_ACTION
            rec["consensus_bet_pct"] = None
            rec["consensus_state"] = "board-read-audit-revised"
            rec["rationale"] = (
                "REVISED 2026-05-31 from BET 66% to CHECK via mechanical board-reading "
                "audit screening (PR #481). Original 5/5 BET vote rested on phantom NFD + "
                "phantom OESD; corrected board read gives 0 BDFD, gutshot only (~18-24% "
                "raw equity). Non-PFA probe into 3 villains' check-back ranges with "
                "sub-pot-odds equity is negative-EV; CHECK preserves realization."
            )
            touched += 1
    assert touched == 1, f"Expected to touch 1 record, touched {touched}"

    CONSENSUS.write_text("\n".join(json.dumps(r) for r in records) + "\n")
    print(f"Patched {SPOT}: consensus_action BET 66% -> CHECK in {CONSENSUS.name}")


if __name__ == "__main__":
    main()
