"""
Track D: Teaching handoff export — build v2_2_enriched_for_teaching.jsonl

Reads:
  training-data/pass1_final_labels.jsonl       — consensus action + label_source
  training-data/pass1_T{1-4}_labels.jsonl      — per-team labels (bucket, intentions,
                                                  street_plan_tags, feature_attention,
                                                  difficulty, reasoning)
  training-data/v2_2_training.csv              — 54 raw features per hand
  /tmp/pass1_discovery_results/T{5,6}_batch*.json — DISCOVERED feature tags

Writes:
  training-data/v2_2_enriched_for_teaching.jsonl

Schema per row:
  situation_id
  consensus_action
  hand_bucket
  intentions
  primary_intention
  street_plan_tags
  feature_attention
  difficulty
  reasoning_by_team
  full_feature_vector
"""

import json
import csv
import os
import glob
from collections import Counter

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = "/home/rupertbeytell/river-rats-v2"
TD = os.path.join(BASE, "training-data")
DISCOVERY_DIR = "/tmp/pass1_discovery_results"

FINAL_LABELS = os.path.join(TD, "pass1_final_labels.jsonl")
TEAM_FILES = [os.path.join(TD, f"pass1_T{i}_labels.jsonl") for i in range(1, 5)]
TRAINING_CSV = os.path.join(TD, "v2_2_training.csv")
OUTPUT = os.path.join(TD, "v2_2_enriched_for_teaching.jsonl")

# The 54 raw feature columns (order matches training CSV header, excluding attn_* and label cols)
RAW_FEATURES = [
    "street", "facing_bet", "pot_size", "to_call", "pot_odds", "bet_to_pot",
    "hero_position", "villain_position", "is_ip", "hand_category", "hand_rank",
    "is_made_hand", "is_strong_made", "is_monster", "has_flush_draw",
    "has_straight_draw", "draw_outs", "is_monotone", "is_two_tone", "is_rainbow",
    "is_paired", "is_double_paired", "connectivity_score", "high_card_rank",
    "danger_score", "flush_danger", "straight_danger", "raw_equity",
    "equity_vs_range", "better_hand_pct", "worse_hand_pct", "equity_margin",
    "spr", "is_3bet_pot", "villain_aggression_count", "villain_checked_back",
    "villain_call_count", "num_opponents", "villain_top_pair_plus_pct",
    "villain_draw_pct", "villain_air_pct", "villain_range_capped", "board_favour",
    "num_callers_to_bet", "facing_raise", "flush_block_pct", "overcard_outs",
    "improvement_probability", "hero_range_percentile", "has_showdown_value",
    "villain_fold_equity_estimate", "flush_draw_rank", "is_preflop_aggressor",
    "villain_medium_made_pct",
]

# Attention tier precedence (higher index = higher priority)
TIER_RANK = {"DISCOVERED": 0, "CONFIRMED": 1, "PRIMARY": 2}


# ---------------------------------------------------------------------------
# Load final labels (385 rows)
# ---------------------------------------------------------------------------
def load_final_labels():
    rows = {}
    with open(FINAL_LABELS) as f:
        for line in f:
            obj = json.loads(line)
            rows[obj["situation_id"]] = obj
    return rows


# ---------------------------------------------------------------------------
# Load per-team labels (T1-T4)
# ---------------------------------------------------------------------------
def load_team_labels():
    teams = {}  # team_idx (1-4) -> {situation_id: row}
    for i, path in enumerate(TEAM_FILES, start=1):
        team_data = {}
        with open(path) as f:
            for line in f:
                obj = json.loads(line)
                team_data[obj["situation_id"]] = obj
        teams[i] = team_data
    return teams


# ---------------------------------------------------------------------------
# Load feature vectors from training CSV
# ---------------------------------------------------------------------------
def load_feature_vectors():
    vectors = {}
    with open(TRAINING_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row["situation_id"]
            fv = {}
            for feat in RAW_FEATURES:
                if feat in row:
                    val = row[feat]
                    # Convert to numeric where possible
                    try:
                        fv[feat] = float(val)
                    except (ValueError, TypeError):
                        fv[feat] = val
            vectors[sid] = fv
    return vectors


# ---------------------------------------------------------------------------
# Load T5/T6 discovery results
# DISCOVERED tags are only feature names (not PRIMARY/CONFIRMED).
# We extract the feature name from whichever schema the batch uses.
# ---------------------------------------------------------------------------
def load_discovery_results():
    """
    Returns: {situation_id: set_of_feature_names_discovered}
    """
    discovered = {}  # situation_id -> set of feature names

    batch_files = sorted(glob.glob(os.path.join(DISCOVERY_DIR, "T[56]_batch*.json")))
    for path in batch_files:
        with open(path) as f:
            try:
                batch = json.load(f)
            except json.JSONDecodeError:
                continue

        if not isinstance(batch, list):
            continue

        for entry in batch:
            sid = entry.get("situation_id")
            if not sid:
                continue
            features = set()

            # Schema A: discovered_features is a dict {feature_name: "DISCOVERED — ..."}
            if "discovered_features" in entry and isinstance(entry["discovered_features"], dict):
                features.update(entry["discovered_features"].keys())

            # Schema B: discovered_features is a list of {feature: name, reasoning: ...}
            elif "discovered_features" in entry and isinstance(entry["discovered_features"], list):
                for item in entry["discovered_features"]:
                    if isinstance(item, dict) and "feature" in item:
                        features.add(item["feature"])
                    elif isinstance(item, str):
                        features.add(item)

            # Schema C: newly_discovered_features is a list of feature name strings
            elif "newly_discovered_features" in entry:
                items = entry["newly_discovered_features"]
                if isinstance(items, list):
                    for item in items:
                        if isinstance(item, str):
                            features.add(item)

            if features:
                if sid not in discovered:
                    discovered[sid] = set()
                discovered[sid].update(features)

    return discovered


# ---------------------------------------------------------------------------
# Helpers: consensus logic over T1-T4
# ---------------------------------------------------------------------------
def majority_vote(values):
    """Return the majority value from a list; tie-break by first occurrence."""
    if not values:
        return None
    counter = Counter(values)
    max_count = max(counter.values())
    # Preserve order: pick first value that has max_count
    for v in values:
        if counter[v] == max_count:
            return v
    return values[0]


def difficulty_label_to_int(val):
    """Normalise difficulty: teams may emit int or string."""
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            # Some teams emit "HARD", "STANDARD", etc. — map to ints
            mapping = {"CLEAR": 1, "LIKELY_CLEAR": 2, "STANDARD": 3, "HARD": 4, "CONTESTED": 4}
            return mapping.get(val.upper(), 3)
    return 3


def consensus_difficulty(team_rows):
    """Consensus difficulty across T1-T4 rows for one hand."""
    vals = []
    for row in team_rows:
        raw = row.get("difficulty")
        if raw is not None:
            vals.append(difficulty_label_to_int(raw))
    return majority_vote(vals) if vals else None


def consensus_bucket(team_rows):
    """Majority hand_bucket across T1-T4."""
    vals = [r.get("hand_bucket") for r in team_rows if r.get("hand_bucket")]
    return majority_vote(vals)


def union_intentions(team_rows):
    """Union of intentions lists across T1-T4, deduped, order preserved by first seen."""
    seen = set()
    result = []
    for row in team_rows:
        for intent in row.get("intentions", []):
            if intent and intent not in seen:
                seen.add(intent)
                result.append(intent)
    return result


def primary_intention(team_rows):
    """Most common single intention across T1-T4 intention lists; tie-break by team order."""
    flat = []
    for row in team_rows:
        intents = row.get("intentions", [])
        if intents:
            flat.append(intents[0])  # each team's first intention = their primary
    return majority_vote(flat) if flat else None


def union_street_plan_tags(team_rows, street):
    """
    Union of street_plan_tags across T1-T4; only for flop/turn hands.
    street is the value from the feature vector (0=flop, 1=turn, 2=river).
    """
    # street 2 = river in the feature encoding; skip river hands
    if street == 2.0 or street == "2" or street == 2:
        return []
    seen = set()
    result = []
    for row in team_rows:
        for tag in (row.get("street_plan_tags") or []):
            if tag and tag not in seen:
                seen.add(tag)
                result.append(tag)
    return result


def merge_feature_attention(team_rows, discovered_features):
    """
    Build feature_attention dict: feature_name -> highest tier across all teams.
    T1-T4 contribute PRIMARY or CONFIRMED.
    discovery set contributes DISCOVERED (if not already tagged by T1-T4).

    Tier precedence: PRIMARY > CONFIRMED > DISCOVERED
    """
    merged = {}  # feature -> best tier

    # T1-T4 attention dicts
    for row in team_rows:
        for feat, tier in row.get("feature_attention", {}).items():
            tier_upper = str(tier).upper()
            # Normalise to canonical tier
            if "PRIMARY" in tier_upper:
                canonical = "PRIMARY"
            elif "CONFIRMED" in tier_upper:
                canonical = "CONFIRMED"
            else:
                canonical = "CONFIRMED"  # unknown → treat as CONFIRMED

            current_rank = TIER_RANK.get(merged.get(feat, ""), -1)
            new_rank = TIER_RANK.get(canonical, 0)
            if new_rank > current_rank:
                merged[feat] = canonical

    # Discovery (T5-T6) — only add if not already present from T1-T4
    for feat in discovered_features:
        if feat not in merged:
            merged[feat] = "DISCOVERED"

    return merged


def reasoning_by_team(team_rows, team_indices):
    """Dict of team_label -> reasoning string."""
    result = {}
    for i, row in zip(team_indices, team_rows):
        reasoning = row.get("reasoning", "")
        if reasoning:
            result[f"T{i}"] = reasoning
    return result


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------
def build_enriched():
    print("Loading data sources...")
    final_labels = load_final_labels()
    teams = load_team_labels()
    feature_vectors = load_feature_vectors()
    discovery = load_discovery_results()

    print(f"  Final labels: {len(final_labels)} hands")
    print(f"  Feature vectors: {len(feature_vectors)} hands")
    print(f"  Discovery entries: {len(discovery)} unique situation_ids")

    # Gather all situation_ids in stable order (from final_labels file)
    situation_ids = list(final_labels.keys())
    print(f"  Processing {len(situation_ids)} hands...")

    rows_written = 0
    missing_fv = []

    with open(OUTPUT, "w") as out_f:
        for sid in situation_ids:
            # Consensus action from final labels
            consensus_action = final_labels[sid]["action"]

            # T1-T4 rows for this hand
            team_rows = []
            team_indices = []
            for i in range(1, 5):
                row = teams[i].get(sid)
                if row:
                    team_rows.append(row)
                    team_indices.append(i)

            # Feature vector
            fv = feature_vectors.get(sid, {})
            if not fv:
                missing_fv.append(sid)

            street_val = fv.get("street", None)

            # Aggregate from T1-T4
            bucket = consensus_bucket(team_rows)
            intents = union_intentions(team_rows)
            prim_intent = primary_intention(team_rows)
            spt = union_street_plan_tags(team_rows, street_val)
            disc_feats = discovery.get(sid, set())
            feat_attn = merge_feature_attention(team_rows, disc_feats)
            diff = consensus_difficulty(team_rows)
            reasoning = reasoning_by_team(team_rows, team_indices)

            enriched = {
                "situation_id": sid,
                "consensus_action": consensus_action,
                "hand_bucket": bucket,
                "intentions": intents,
                "primary_intention": prim_intent,
                "street_plan_tags": spt,
                "feature_attention": feat_attn,
                "difficulty": diff,
                "reasoning_by_team": reasoning,
                "full_feature_vector": fv,
            }

            out_f.write(json.dumps(enriched, ensure_ascii=False) + "\n")
            rows_written += 1

    print(f"\nDone. Rows written: {rows_written}")
    if missing_fv:
        print(f"WARNING: {len(missing_fv)} hands had no feature vector: {missing_fv[:10]}")
    return rows_written


if __name__ == "__main__":
    build_enriched()
