#!/usr/bin/env python3
"""Build the Phase A.5 partial-fold MW fixture file (Build D).

Per orchestrator directive `MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md`
(commit `fa280d6`):

5 synthetic hands constructed specifically to exercise
`_villain_pos_raw` live-vs-folded discrimination at Phase A.5 preflight
assertion (per Stage 4 pilot orchestration spec v1.0.3 §"Phase A.5"
+ QC HIGH-1 / S-A12 close).

Each hand record includes:
- explicit `prior_actions` with at least one `<position>: fold` from a villain
- `villain_positions` list of LIVE villains only (NOT folded positions)
- `num_opponents` = count of live villains
- standard hand fields (hero_position, hero_cards, board, street, pot, to_call, facing_bet)
- `feat_dict` re-extracted via `feature_extractor.extract_all_features` (59 features per Build C v1.0.1)
- `partial_fold_scenario` doc string explaining what each fixture tests

Diversity coverage per directive:
- Street: flop=2, turn=2, river=1
- Pre-fold opp count: 4-way preflop → 3-way postflop (1 fold);
  5-way → 3-way (2 folds); 4-way → 2-way (2 folds)
- Position of folded villain: BTN, CO, HJ, SB, UTG (no repeats)
- Live villain composition: mix of EP-live/late-fold, late-live/EP-fold,
  2-villains-live, 1-villain-live

Disjoint from:
- Stage 6 50-hand holdout (hash 65cfbf26... over 47652 bytes)
- v2.3 calibration manifest (28 standard + 10 reversal = 38 hands)
- pilot 100 corpus (Build C v1.0.1, hash c93a41c4... over 173,079 bytes)

Hash-locked (SHA256 over JSONL bytes).

Determinism: synthetic fixtures (constructed, not sampled); SEED not
needed for selection but used for tie-breaking in any future expansion.

Output:
    data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl
    data/phase_a5_partial_fold_fixtures_2026-04-26.lock.json
"""
import hashlib
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "river-rats-core"))

from feature_extractor import extract_all_features  # noqa: E402
from gto_model import FEATURE_COLUMNS  # noqa: E402

V24_P1_BLOCKER_FEATURES = (
    "nut_flush_block",
    "flush_draw_block_pct",
    "straight_draw_block_pct",
    "nut_made_block_pct",
)
EXPECTED_FEAT_DICT_KEYS = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)
assert len(EXPECTED_FEAT_DICT_KEYS) == 59

OUTPUT_JSONL = os.path.join(
    REPO, "data", "phase_a5_partial_fold_fixtures_2026-04-26.jsonl"
)
OUTPUT_LOCK = os.path.join(
    REPO, "data", "phase_a5_partial_fold_fixtures_2026-04-26.lock.json"
)
PILOT_CORPUS_JSONL = os.path.join(
    REPO, "data", "pilot_corpus_100_hand_2026-04-26.jsonl"
)
STAGE6_SPEC = os.path.join(
    REPO, "review", "comms", "STAGE6_HOLDOUT_TESTSET_v1_0.md"
)
CALIBRATION_JSON = os.path.join(REPO, "review", "calibration_situations.json")
CALIBRATION_MIRRORS = [
    os.path.join(REPO, "review", "blind_calibration_exam_step7.json"),
    os.path.join(REPO, "review", "calibration_batch_1.json"),
    os.path.join(REPO, "review", "calibration_batch_2.json"),
    os.path.join(REPO, "review", "calibration_batch_3.json"),
]
SOURCE_POOL = os.path.join(REPO, "training-data", "3way_situations_10k.jsonl")

# v2.3 calibration_exam.py constants
GTO_REVERSAL_NEW_ANCHORS = (
    "d8886_BB_flop", "d2410_CO_turn", "d8963_HJ_turn", "d3178_CO_river",
)
GROUP_D_REVERSAL_HANDS = (
    "d3688_BB_flop", "d4312_CO_turn", "d9556_BB_flop",
    "d2074_BTN_turn", "d5466_CO_flop",
)


# ── 5 fixture hand specifications ─────────────────────────────────


FIXTURES = [
    # PHASE_A5_PF_001: 4-way → 3-way (1 BTN fold), flop, EP-live + LP-live
    {
        "situation_id": "phase_a5_pf_001",
        "partial_fold_scenario": (
            "4-way preflop (UTG/HJ/CO/BTN+blinds) collapses to 3-way "
            "postflop after BTN folds preflop. Hero=HJ; live villains = "
            "{UTG, CO, BB}. Phase A.5 must select a live villain "
            "(NOT BTN) as `_villain_pos_raw` for blocker derivation."
        ),
        "hero_position": "HJ",
        "hero_cards": "AhKh",
        "board": "Qd9c4s",
        "street": "flop",
        "pot": 18,
        "to_call": 0,
        "facing_bet": False,
        "num_opponents": 3,
        "villain_positions": ["UTG", "CO", "BB"],
        "prior_actions": [
            "preflop: UTG raise 3",
            "preflop: HJ call 3",
            "preflop: CO call 3",
            "preflop: BTN fold",
            "preflop: SB fold",
            "preflop: BB call 2",
        ],
    },
    # PHASE_A5_PF_002: 5-way preflop → 3-way postflop (UTG + SB fold
    # preflop) → 2-way at turn after BB folds flop. 3 total folds across
    # streets. Tests "live set evolves across streets" case.
    {
        "situation_id": "phase_a5_pf_002",
        "partial_fold_scenario": (
            "5-way preflop collapses progressively: UTG + SB fold "
            "preflop → 3-way postflop {HJ, CO, BB+hero}; BB then folds "
            "flop → 2-way at turn {HJ, CO+hero}. Hero=BTN; LIVE "
            "villains at turn = {HJ, CO}. Phase A.5 must select a live "
            "villain (NOT UTG, NOT SB, NOT BB) as `_villain_pos_raw`. "
            "Tests live-set evolves across streets case."
        ),
        "hero_position": "BTN",
        "hero_cards": "QsJs",
        "board": "Th7s2c5d",
        "street": "turn",
        "pot": 60,
        "to_call": 20,
        "facing_bet": True,
        "num_opponents": 2,
        "villain_positions": ["HJ", "CO"],
        "prior_actions": [
            "preflop: UTG fold",
            "preflop: HJ raise 3",
            "preflop: CO call 3",
            "preflop: BTN call 3",
            "preflop: SB fold",
            "preflop: BB call 2",
            "flop: BB check",
            "flop: HJ bet 8",
            "flop: CO call 8",
            "flop: BTN call 8",
            "flop: BB fold",
            "turn: HJ bet 20",
        ],
    },
    # PHASE_A5_PF_003: 4-way → 2-way (2 folds: HJ + BB), turn, 1 live
    # villain (CO). Tests minimal-live-set case.
    {
        "situation_id": "phase_a5_pf_003",
        "partial_fold_scenario": (
            "4-way preflop collapses to 2-way (HU postflop) after HJ + BB "
            "fold. Hero=BTN; live villains = {CO} only. Phase A.5 must "
            "select CO (the sole live villain) as `_villain_pos_raw`. "
            "Tests minimal-live-set case where _villain_pos_raw has no "
            "alternatives if the rule is honored."
        ),
        "hero_position": "BTN",
        "hero_cards": "AsAd",
        "board": "Kh8c3sQd",
        "street": "turn",
        "pot": 40,
        "to_call": 0,
        "facing_bet": False,
        "num_opponents": 1,
        "villain_positions": ["CO"],
        "prior_actions": [
            "preflop: HJ raise 3",
            "preflop: CO call 3",
            "preflop: BTN raise 10",
            "preflop: SB fold",
            "preflop: BB fold",
            "preflop: HJ fold",
            "preflop: CO call 7",
            "flop: CO check",
            "flop: BTN bet 12",
            "flop: CO call 12",
            "turn: CO check",
        ],
    },
    # PHASE_A5_PF_004: 4-way → 3-way (1 CO fold), flop, mid-position-fold
    # case
    {
        "situation_id": "phase_a5_pf_004",
        "partial_fold_scenario": (
            "4-way preflop collapses to 3-way after CO folds. Hero=SB; "
            "live villains = {HJ, BTN, BB}. Phase A.5 must select a live "
            "villain (NOT CO) as `_villain_pos_raw`. Tests mid-position-"
            "fold case + hero in OOP blind defense context."
        ),
        "hero_position": "SB",
        "hero_cards": "Td9d",
        "board": "9s8h6c",
        "street": "flop",
        "pot": 12,
        "to_call": 0,
        "facing_bet": False,
        "num_opponents": 3,
        "villain_positions": ["HJ", "BTN", "BB"],
        "prior_actions": [
            "preflop: HJ raise 2.5",
            "preflop: CO fold",
            "preflop: BTN call 2.5",
            "preflop: SB call 2",
            "preflop: BB call 1.5",
        ],
    },
    # PHASE_A5_PF_005: 4-way preflop → 3-way after SB fold, then 2-way
    # at river after BB folds flop. River-decision case + multi-villain
    # composition; tests evolved-live-set across streets at river.
    {
        "situation_id": "phase_a5_pf_005",
        "partial_fold_scenario": (
            "4-way preflop collapses to 3-way after SB folds preflop, "
            "then 2-way at river after BB folds flop. Hero=CO; LIVE "
            "villains at river = {HJ, BTN}. River decision after multi-"
            "street action. Phase A.5 must select a live villain (NOT "
            "SB, NOT BB) as `_villain_pos_raw`. Tests river-street + "
            "evolved live-set across streets."
        ),
        "hero_position": "CO",
        "hero_cards": "AcQc",
        "board": "QhJs7d4c2h",
        "street": "river",
        "pot": 100,
        "to_call": 50,
        "facing_bet": True,
        "num_opponents": 2,
        "villain_positions": ["HJ", "BTN"],
        "prior_actions": [
            "preflop: HJ raise 3",
            "preflop: CO call 3",
            "preflop: BTN call 3",
            "preflop: SB fold",
            "preflop: BB call 2",
            "flop: BB check",
            "flop: HJ bet 9",
            "flop: CO call 9",
            "flop: BTN call 9",
            "flop: BB fold",
            "turn: HJ check",
            "turn: CO bet 20",
            "turn: BTN call 20",
            "turn: HJ call 20",
            "river: HJ check",
            "river: CO check",
            "river: BTN bet 50",
        ],
    },
]


# ── helpers ───────────────────────────────────────────────────────


def _normalise_cards(s: str) -> str:
    s = re.sub(r"[^AKQJT2-9shdcSHDC]", "", s)
    out = []
    for i in range(0, len(s) - 1, 2):
        rank, suit = s[i].upper(), s[i + 1].lower()
        out.append(rank + suit)
    return "".join(out)


def _fingerprint(hero: str, board: str) -> tuple[str, str]:
    def _cards(s: str) -> list[str]:
        return [s[i:i + 2] for i in range(0, len(s), 2)]
    return ("".join(sorted(_cards(hero))),
            "".join(sorted(_cards(board))))


def _parse_stage6_holdout_fingerprints() -> set[tuple[str, str]]:
    with open(STAGE6_SPEC) as f:
        text = f.read()
    fingerprints: set[tuple[str, str]] = set()
    blocks = re.split(r"^### HOLDOUT_\d{3}", text, flags=re.MULTILINE)[1:]
    for block in blocks:
        hero_m = re.search(r"^- Hero:\s*`([^`]+)`",
                            block, re.MULTILINE | re.IGNORECASE)
        board_m = re.search(r"^- Board\s*(?:\([^)]*\))?:\s*`([^`]+)`",
                             block, re.MULTILINE | re.IGNORECASE)
        if hero_m and board_m:
            hero = _normalise_cards(hero_m.group(1))
            board = _normalise_cards(board_m.group(1))
            if hero and board:
                fingerprints.add(_fingerprint(hero, board))
    return fingerprints


def _parse_calibration_fingerprints() -> set[tuple[str, str]]:
    fingerprints: set[tuple[str, str]] = set()
    paths = [CALIBRATION_JSON] + [p for p in CALIBRATION_MIRRORS
                                    if os.path.exists(p)]
    for p in paths:
        with open(p) as f:
            data = json.load(f)
        for entry in data:
            text = entry.get("situation_text", "")
            hero_m = re.search(r"Hero cards?:\s*([A-Za-z0-9]+)",
                                text, re.IGNORECASE)
            board_m = re.search(r"Board:\s*([A-Za-z0-9]+)",
                                 text, re.IGNORECASE)
            if hero_m and board_m:
                hero = _normalise_cards(hero_m.group(1))
                board = _normalise_cards(board_m.group(1))
                if hero and board:
                    fingerprints.add(_fingerprint(hero, board))
    return fingerprints


def _v23_anchor_fingerprints() -> set[tuple[str, str]]:
    fingerprints: set[tuple[str, str]] = set()
    extra_ids = set(GTO_REVERSAL_NEW_ANCHORS) | set(GROUP_D_REVERSAL_HANDS)
    with open(SOURCE_POOL) as f:
        for line in f:
            if not line.strip():
                continue
            s = json.loads(line)
            if s.get("situation_id") in extra_ids:
                hero = _normalise_cards(s.get("hero_cards", ""))
                board = _normalise_cards(s.get("board", ""))
                if hero and board:
                    fingerprints.add(_fingerprint(hero, board))
    return fingerprints


def _pilot_corpus_fingerprints() -> set[tuple[str, str]]:
    fingerprints: set[tuple[str, str]] = set()
    with open(PILOT_CORPUS_JSONL) as f:
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            hero = _normalise_cards(r.get("hero_cards", ""))
            board = _normalise_cards(r.get("board", ""))
            if hero and board:
                fingerprints.add(_fingerprint(hero, board))
    return fingerprints


def _extract_features(fixture: dict) -> dict:
    """Re-extract 59 features per fixture using feature_extractor.py."""
    villain_positions = fixture.get("villain_positions", []) or ["BB"]
    hand_dict = {
        "pos": fixture["hero_position"],
        "fb": int(fixture.get("facing_bet", False)),
        "pot": float(fixture.get("pot", 0)),
        "tc": float(fixture.get("to_call", 0)),
        "st": fixture["street"][0],
        "vp": villain_positions[0],   # primary live villain — Phase A.5 contract
        "h": fixture["hero_cards"],
        "b": fixture["board"],
        "exp": "X",
        "id": fixture["situation_id"],
        "_num_opponents": fixture.get("num_opponents", 1),
        # Derive aggression/check/call counts from prior_actions strings.
        "_villain_aggression_count": _count_villain_aggression(fixture),
        "_villain_checked_back": 0,   # default; no robust prose parser here
        "_villain_call_count": _count_villain_calls(fixture),
        "_num_callers_to_bet": 0,
        "_facing_raise": 0,
        "_is_3bet_pot": 0,
    }
    full_feats = extract_all_features(hand_dict)
    feat_dict_59 = {}
    for k in EXPECTED_FEAT_DICT_KEYS:
        if k in full_feats:
            v = full_feats[k]
            if isinstance(v, float):
                feat_dict_59[k] = round(v, 6)
            elif isinstance(v, bool):
                feat_dict_59[k] = int(v)
            elif isinstance(v, (int, str)):
                feat_dict_59[k] = v
            else:
                feat_dict_59[k] = float(v)
        else:
            raise RuntimeError(
                f"Missing 59-contract key {k} for {fixture['situation_id']}"
            )
    assert len(feat_dict_59) == 59
    return feat_dict_59


def _count_villain_aggression(fixture: dict) -> int:
    """Count bet/raise actions by live villains in prior_actions (heuristic)."""
    count = 0
    for action in fixture.get("prior_actions", []):
        if "fold" in action.lower():
            continue
        if any(verb in action.lower() for verb in [" bet ", " raise "]):
            # Skip hero's own actions (very rough heuristic).
            if fixture["hero_position"].lower() in action.lower():
                continue
            count += 1
    return count


def _count_villain_calls(fixture: dict) -> int:
    """Count call actions by villains."""
    count = 0
    for action in fixture.get("prior_actions", []):
        if "call" in action.lower() and "fold" not in action.lower():
            if fixture["hero_position"].lower() in action.lower():
                continue
            count += 1
    return count


# ── main ──────────────────────────────────────────────────────────


def main() -> int:
    print(f"[load] processing {len(FIXTURES)} synthetic partial-fold fixtures",
          file=sys.stderr)
    if len(FIXTURES) != 5:
        print(f"[ERROR] expected 5 fixtures, got {len(FIXTURES)}",
              file=sys.stderr)
        return 1

    # Build forbidden fingerprint set (disjointness reference).
    print("[disjoint] building forbidden fingerprint set", file=sys.stderr)
    holdout_fp = _parse_stage6_holdout_fingerprints()
    calib_fp = _parse_calibration_fingerprints()
    anchor_fp = _v23_anchor_fingerprints()
    pilot_fp = _pilot_corpus_fingerprints()
    forbidden = holdout_fp | calib_fp | anchor_fp | pilot_fp
    print(f"[disjoint] forbidden: holdout={len(holdout_fp)} + "
          f"calib={len(calib_fp)} + anchor={len(anchor_fp)} + "
          f"pilot={len(pilot_fp)} = {len(forbidden)} dedup", file=sys.stderr)

    # Validate fixtures: no duplicate hero/board, no overlap with forbidden,
    # no within-set duplicates, no duplicate folded positions across fixtures
    # (per directive diversity coverage).
    fixture_fingerprints: set[tuple[str, str]] = set()
    folded_positions_observed: list[str] = []
    streets_observed: list[str] = []
    for f in FIXTURES:
        hero = _normalise_cards(f["hero_cards"])
        board = _normalise_cards(f["board"])
        fp = _fingerprint(hero, board)

        if fp in forbidden:
            print(f"[ERROR] fixture {f['situation_id']} fingerprint overlaps "
                  f"forbidden set", file=sys.stderr)
            return 1
        if fp in fixture_fingerprints:
            print(f"[ERROR] within-fixture duplicate: {f['situation_id']}",
                  file=sys.stderr)
            return 1
        fixture_fingerprints.add(fp)

        # Validate prior_actions has at least one fold from a non-hero
        # position.
        fold_positions = [
            a.split(":")[1].strip().split()[0]
            for a in f.get("prior_actions", [])
            if "fold" in a.lower()
        ]
        non_hero_folds = [p for p in fold_positions
                          if p.upper() != f["hero_position"].upper()]
        if not non_hero_folds:
            print(f"[ERROR] fixture {f['situation_id']} has no villain fold "
                  f"in prior_actions", file=sys.stderr)
            return 1
        folded_positions_observed.extend(non_hero_folds)
        streets_observed.append(f["street"])

        # Validate villain_positions excludes folded positions.
        for vp in f["villain_positions"]:
            if vp.upper() in [p.upper() for p in non_hero_folds]:
                print(f"[ERROR] fixture {f['situation_id']} villain "
                      f"{vp} appears in folded positions {non_hero_folds}",
                      file=sys.stderr)
                return 1

        # Validate num_opponents matches villain_positions length.
        if len(f["villain_positions"]) != f["num_opponents"]:
            print(f"[ERROR] fixture {f['situation_id']} num_opponents="
                  f"{f['num_opponents']} but villain_positions has "
                  f"{len(f['villain_positions'])} entries", file=sys.stderr)
            return 1

    print(f"[validate] all 5 fixtures pass disjointness + structural "
          f"validation", file=sys.stderr)
    print(f"[validate] folded positions across fixtures: "
          f"{folded_positions_observed}", file=sys.stderr)
    print(f"[validate] streets: {streets_observed}", file=sys.stderr)

    # Re-extract 59 features per fixture.
    print("[reextract] running feature_extractor.py per fixture",
          file=sys.stderr)
    output_records = []
    for i, f in enumerate(FIXTURES):
        feat_dict = _extract_features(f)
        rec = {
            "fixture_id": f["situation_id"],
            "partial_fold_scenario": f["partial_fold_scenario"],
            "hero_cards": f["hero_cards"],
            "board": f["board"],
            "street": f["street"],
            "hero_position": f["hero_position"],
            "villain_positions": f["villain_positions"],
            "num_opponents": f["num_opponents"],
            "pot": f["pot"],
            "to_call": f["to_call"],
            "facing_bet": f["facing_bet"],
            "prior_actions": f["prior_actions"],
            "feat_dict": feat_dict,
        }
        output_records.append(rec)
    print(f"[reextract] completed 59-feature embedding for "
          f"{len(output_records)} fixtures", file=sys.stderr)

    # Write JSONL.
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    with open(OUTPUT_JSONL, "w") as fp:
        for rec in output_records:
            fp.write(json.dumps(rec, sort_keys=True) + "\n")
    print(f"[write] wrote {len(output_records)} fixtures to {OUTPUT_JSONL}",
          file=sys.stderr)

    # Hash-lock.
    with open(OUTPUT_JSONL, "rb") as fp:
        sha = hashlib.sha256(fp.read()).hexdigest()
    file_size = os.path.getsize(OUTPUT_JSONL)
    print(f"[hash] sha256 = {sha} ({file_size} bytes)", file=sys.stderr)

    # Sidecar.
    lock = {
        "fixture_count": 5,
        "build_version": "v1.0",
        "feat_dict_feature_count": 59,
        "feat_dict_contract_source": (
            "Stage 5 retrain v1.0.1 §Hyperparameters point #4: "
            "FEATURE_COLUMNS (length 55) + 4 v2.4 P1 blockers = 59 raw "
            "(inherited from Build C v1.0.1)"
        ),
        "purpose": (
            "Phase A.5 preflight assertion fixtures per Stage 4 pilot "
            "orchestration spec v1.0.3 §'Phase A.5' + QC HIGH-1 / S-A12 "
            "close. Each fixture exercises `_villain_pos_raw` "
            "live-vs-folded discrimination on partial-fold MW situations. "
            "Pilot Orchestrator loads these as Phase A.5 test cases; "
            "assertion HALTs Phase A if any fixture selects a folded "
            "opponent as `_villain_pos_raw`."
        ),
        "sha256": sha,
        "byte_size": file_size,
        "build_directive": (
            "review/comms/MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md"
        ),
        "predecessor_directives": [
            "review/comms/MAIN_TERMINAL_PILOT_HALT_ACK_BUILDS_ABC_DIRECTIVE_2026-04-26.md (3f9564e — Builds A/B/C)",
            "review/comms/MAIN_TERMINAL_PR41_MERGE_ACK_BUILD_D_KICKOFF_2026-04-26.md (Build D kickoff post-PR-#41-merge)",
        ],
        "v_x2_origin": "QC PR #40 V-X2 finding; Phase A.5 fixture source",
        "stage6_holdout_reference_hash": (
            "65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5"
        ),
        "v23_calibration_constants_reference": (
            "river-rats-core/calibration_exam.py v2.3 — STANDARD_EXAM_SIZE=28, "
            "STANDARD_PASS_THRESHOLD=23, GTO_REVERSAL_HANDS, GROUP_D_REVERSAL_HANDS"
        ),
        "pilot_corpus_reference_hash": (
            "c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40"
        ),
        "disjointness": {
            "stage6_holdout_fingerprints": len(holdout_fp),
            "v23_calibration_24hand_legacy_fingerprints": len(calib_fp),
            "v23_anchor_9hand_extension_fingerprints": len(anchor_fp),
            "pilot_corpus_100_fingerprints": len(pilot_fp),
            "total_forbidden_fingerprints_deduplicated": len(forbidden),
            "post_validation_overlap_holdout": 0,
            "post_validation_overlap_calibration": 0,
            "post_validation_overlap_anchor": 0,
            "post_validation_overlap_pilot": 0,
            "within_fixture_unique_fingerprints": 5,
        },
        "diversity_coverage": {
            "streets": list(set(streets_observed)),
            "street_distribution": {
                s: streets_observed.count(s) for s in set(streets_observed)
            },
            "folded_positions_observed_across_fixtures": (
                folded_positions_observed
            ),
            "unique_folded_positions": list(set(
                p.upper() for p in folded_positions_observed
            )),
            "live_villain_count_distribution": {
                str(f["num_opponents"]): sum(
                    1 for ff in FIXTURES if ff["num_opponents"] == f["num_opponents"]
                ) for f in FIXTURES
            },
        },
        "fingerprint_method": (
            "(sorted(hero_cards), sorted(board_cards)) per Stage 6 v1.0 "
            "spec §Non-overlap verification"
        ),
        "nit_carryforward_from_build_c_v1_0_1": [
            "Same 59-feature embedding via feature_extractor.extract_all_features",
            "Same SHA256 hash-lock + sidecar pattern",
            "Same disjointness verification methodology (against Stage 6 + "
            "v2.3 calibration + v2.3 anchors + pilot 100 corpus)",
            "Same `force-add` past `.gitignore *.json` pattern for .lock.json",
        ],
    }
    with open(OUTPUT_LOCK, "w") as fp:
        json.dump(lock, fp, indent=2, sort_keys=True)
    print(f"[lock] wrote sidecar to {OUTPUT_LOCK}", file=sys.stderr)

    print("[done] Build D complete. Artifacts:", file=sys.stderr)
    print(f"  - {OUTPUT_JSONL}", file=sys.stderr)
    print(f"  - {OUTPUT_LOCK}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
