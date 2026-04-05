#!/usr/bin/env python3
"""
Parallel feature extraction with checkpoint/resume.
Processes gauntlet_500k.json in 1000-hand chunks using multiprocessing.
Each chunk saved as CSV immediately — survives interruptions.

Usage:
    nohup python3 extract_features_parallel.py &
    # Check progress:  tail -f /home/claude/extraction_progress.log
"""

import json
import csv
import os
import sys
import time
import multiprocessing as mp
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────
INPUT_FILE    = "/home/claude/gauntlet_500k.json"
OUTPUT_DIR    = "/home/claude/feature_chunks"
MERGED_OUTPUT = "/home/claude/features_500k.csv"
LOG_FILE      = "/home/claude/extraction_progress.log"
CHUNK_SIZE    = 1000
NUM_WORKERS   = 4  # match CPU cores

# The 38 features + label the model expects
MODEL_COLUMNS = [
    'street','facing_bet','pot_size','to_call','pot_odds','bet_to_pot',
    'hero_position','villain_position','is_ip',
    'hand_category','hand_rank','is_made_hand','is_strong_made','is_monster',
    'has_flush_draw','has_straight_draw','draw_outs',
    'is_monotone','is_two_tone','is_rainbow','is_paired','is_double_paired',
    'connectivity_score','high_card_rank','danger_score','flush_danger','straight_danger',
    'raw_equity','equity_vs_range','better_hand_pct','worse_hand_pct',
    'equity_margin','spr',
    'is_3bet_pot','villain_aggression_count','villain_checked_back','villain_call_count',
    'num_opponents',
    'action'
]

ACTION_MAP = {'FOLD': 0, 'CHECK': 1, 'CALL': 2, 'BET': 3, 'RAISE': 4}


def log(msg):
    """Write to log file and stdout."""
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def process_chunk(args):
    """
    Worker function: extract features for a list of hands.
    Returns (chunk_id, rows_list, error_count).
    Each row is a list of floats matching MODEL_COLUMNS order.
    """
    chunk_id, hands = args

    # Import inside worker to avoid pickle issues
    sys.path.insert(0, "/home/claude")
    from feature_extractor import extract_all_features

    rows = []
    errors = 0
    for hand in hands:
        try:
            feat = extract_all_features(hand)
            # Convert action string to int label
            action_val = ACTION_MAP.get(feat.get('action'), -1)
            if action_val == -1:
                errors += 1
                continue
            row = []
            for col in MODEL_COLUMNS[:-1]:  # all except 'action'
                row.append(float(feat[col]))
            row.append(action_val)
            rows.append(row)
        except Exception:
            errors += 1

    return chunk_id, rows, errors


def get_completed_chunks(output_dir):
    """Check which chunks are already done on disk."""
    done = set()
    if not os.path.exists(output_dir):
        return done
    for f in os.listdir(output_dir):
        if f.startswith("chunk_") and f.endswith(".csv"):
            try:
                cid = int(f.replace("chunk_", "").replace(".csv", ""))
                # Verify it's non-empty
                path = os.path.join(output_dir, f)
                if os.path.getsize(path) > 0:
                    done.add(cid)
            except ValueError:
                pass
    return done


def save_chunk(chunk_id, rows, output_dir):
    """Write one chunk's rows to CSV."""
    path = os.path.join(output_dir, f"chunk_{chunk_id:04d}.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        for row in rows:
            w.writerow(row)


def merge_all_chunks(output_dir, merged_path, total_chunks):
    """Merge all chunk CSVs into one file with header."""
    log(f"Merging {total_chunks} chunks into {merged_path}...")
    with open(merged_path, "w", newline="") as out:
        w = csv.writer(out)
        w.writerow(MODEL_COLUMNS)  # header
        for cid in range(total_chunks):
            chunk_path = os.path.join(output_dir, f"chunk_{cid:04d}.csv")
            if os.path.exists(chunk_path):
                with open(chunk_path) as f:
                    for line in f:
                        out.write(line)
    size_mb = os.path.getsize(merged_path) / (1024 * 1024)
    log(f"Merged: {merged_path} ({size_mb:.1f} MB)")


def main():
    t_start = time.time()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Clear log on fresh start (but keep if resuming)
    completed = get_completed_chunks(OUTPUT_DIR)
    if not completed:
        open(LOG_FILE, "w").close()

    log("=" * 60)
    log("PARALLEL FEATURE EXTRACTION")
    log("=" * 60)

    # Load data
    log(f"Loading {INPUT_FILE}...")
    with open(INPUT_FILE) as f:
        all_hands = json.load(f)
    total = len(all_hands)
    log(f"Loaded {total} hands")

    # Build chunks
    chunks = []
    for i in range(0, total, CHUNK_SIZE):
        chunk_id = i // CHUNK_SIZE
        chunks.append((chunk_id, all_hands[i:i + CHUNK_SIZE]))
    total_chunks = len(chunks)
    log(f"Split into {total_chunks} chunks of {CHUNK_SIZE}")

    # Filter out already-completed chunks
    completed = get_completed_chunks(OUTPUT_DIR)
    remaining = [(cid, hands) for cid, hands in chunks if cid not in completed]
    log(f"Already completed: {len(completed)} chunks")
    log(f"Remaining: {len(remaining)} chunks")
    log(f"Workers: {NUM_WORKERS}")
    log("")

    if not remaining:
        log("All chunks done! Merging...")
        merge_all_chunks(OUTPUT_DIR, MERGED_OUTPUT, total_chunks)
        return

    # Process with multiprocessing pool
    total_rows = sum(
        sum(1 for _ in open(os.path.join(OUTPUT_DIR, f"chunk_{cid:04d}.csv")))
        for cid in completed
    ) if completed else 0
    total_errors = 0
    done_count = len(completed)

    # Use imap_unordered for streaming results as they complete
    with mp.Pool(NUM_WORKERS) as pool:
        for chunk_id, rows, errors in pool.imap_unordered(process_chunk, remaining, chunksize=1):
            # Save immediately
            save_chunk(chunk_id, rows, OUTPUT_DIR)
            total_rows += len(rows)
            total_errors += errors
            done_count += 1

            # Progress
            elapsed = time.time() - t_start
            hands_done = done_count * CHUNK_SIZE
            rate = hands_done / elapsed if elapsed > 0 else 0
            eta = (total - hands_done) / rate if rate > 0 else 0
            pct = hands_done / total * 100

            if done_count % 10 == 0 or done_count == total_chunks:
                log(
                    f"  [{done_count}/{total_chunks}] "
                    f"{pct:.1f}% | {rate:.0f} h/s | "
                    f"ETA {eta/60:.0f}m | "
                    f"rows={total_rows} err={total_errors}"
                )

    elapsed = time.time() - t_start
    log("")
    log("=" * 60)
    log(f"EXTRACTION COMPLETE")
    log(f"  Total hands:  {total}")
    log(f"  Total rows:   {total_rows}")
    log(f"  Total errors: {total_errors}")
    log(f"  Time:         {elapsed/60:.1f} min ({elapsed/3600:.2f} hours)")
    log(f"  Rate:         {total/elapsed:.0f} hands/sec")
    log("=" * 60)

    # Merge
    merge_all_chunks(OUTPUT_DIR, MERGED_OUTPUT, total_chunks)
    log("DONE.")


if __name__ == "__main__":
    main()
