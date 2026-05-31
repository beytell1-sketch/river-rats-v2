"""
Apply debate panel adjudication to batch_009_consensus_v2.jsonl.

Sets consensus_action + consensus_state for the 3 owner-arb spots per
the 2026-05-30 multi-viewpoint debate panel outcome.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "4way_corpus" / "full_700"
CONSENSUS = CORPUS / "batch_009_consensus_v2.jsonl"
ARB_QUEUE = CORPUS / "batch_009_owner_arb_queue_normalizer.jsonl"

ADJUDICATIONS = {
    "4WF-CHAIN-009-004": {
        "consensus_action": "FOLD",
        "consensus_state": "debate-panel-adjudicated",
        "predicted_bet_pct": None,
        "predicted_raise_to_bb": None,
    },
    "4WF-CHAIN-009-016": {
        "consensus_action": "FOLD",
        "consensus_state": "debate-panel-adjudicated",
        "predicted_bet_pct": None,
        "predicted_raise_to_bb": None,
    },
    "4WF-RANGE-AS-457": {
        "consensus_action": "CALL",
        "consensus_state": "debate-panel-adjudicated",
        "predicted_bet_pct": None,
        "predicted_raise_to_bb": None,
    },
}


def main():
    records = [json.loads(line) for line in CONSENSUS.read_text().splitlines() if line.strip()]
    touched = 0
    for rec in records:
        sid = rec.get("spot_id")
        if sid in ADJUDICATIONS:
            patch = ADJUDICATIONS[sid]
            rec.update(patch)
            touched += 1
    assert touched == 3, f"Expected to touch 3 records, touched {touched}"

    CONSENSUS.write_text("\n".join(json.dumps(r) for r in records) + "\n")
    ARB_QUEUE.write_text("")

    print(f"Adjudicated {touched} spots in {CONSENSUS.name}")
    print(f"Emptied {ARB_QUEUE.name}")


if __name__ == "__main__":
    main()
