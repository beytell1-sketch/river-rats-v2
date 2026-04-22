"""
Incremental feature extraction â€” processes N hands per call.
Tracks progress via a simple offset file per chunk.

Usage:
    python3 extract_incremental.py CHUNK_ID [BATCH_SIZE]
    
Example:
    python3 extract_incremental.py 0         # next 2000 from chunk 00
    python3 extract_incremental.py 0 3000    # next 3000 from chunk 00
"""

import sys
import os
import csv
import time

sys.path.insert(0, '/mnt/project')
sys.path.insert(0, '/home/claude')

from pokerbench_parser import parse_pokerbench_line
from feature_extractor import extract_all_features, FEATURE_COLUMNS
from sizing_oracle import assign_raise_bucket, assign_bet_bucket

OUTPUT_DIR = '/home/claude/training_data'
CHUNK_DIR = '/mnt/user-data/uploads'

ACTION_MAP = {'Fold': 'FOLD', 'Check': 'CHECK', 'Call': 'CALL'}

def classify_action(s):
    s = s.strip()
    if s in ACTION_MAP: return ACTION_MAP[s]
    if s.startswith('Bet'): return 'BET'
    if s.startswith('Raise'): return 'RAISE'
    return None

def main():
    chunk_id = int(sys.argv[1])
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    chunk_file = f'{CHUNK_DIR}/pokerbench_chunk_{chunk_id:02d}'
    out_file = f'{OUTPUT_DIR}/features_chunk_{chunk_id:02d}.csv'
    offset_file = f'{OUTPUT_DIR}/.offset_{chunk_id:02d}'
    
    # Read current offset
    offset = 0
    if os.path.exists(offset_file):
        with open(offset_file) as f:
            offset = int(f.read().strip())
    
    # Check if chunk is done (25000 lines)
    if offset >= 25000:
        print(f"Chunk {chunk_id:02d}: COMPLETE (offset={offset})")
        return
    
    # Write header if new file.
    # CRIT #2 audit column appended at end for post-hoc filtering.
    header = list(FEATURE_COLUMNS) + ['action_label', 'size_bucket',
                                       '_action_history_present']
    if not os.path.exists(out_file):
        with open(out_file, 'w', newline='') as f:
            csv.writer(f).writerow(header)
    
    # Skip to offset, then extract batch_size hands
    rows = []
    errors = 0
    line_num = 0
    t0 = time.time()
    
    with open(chunk_file) as f:
        for line in f:
            line_num += 1
            if line_num <= offset:
                continue
            if line_num > offset + batch_size:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                parsed = parse_pokerbench_line(line)
                if not parsed:
                    errors += 1
                    continue

                feat = extract_all_features(parsed)
                vec = [float(feat.get(c, 0.0)) for c in FEATURE_COLUMNS]

                correct = parsed.get('_correct_action_raw', '')
                action = classify_action(correct)
                if not action:
                    errors += 1
                    continue

                size_bucket = ''
                pot_ratio = parsed.get('_pot_ratio', 0.0)
                if action == 'RAISE' and pot_ratio > 0:
                    size_bucket = assign_raise_bucket(pot_ratio)
                elif action == 'BET' and pot_ratio > 0:
                    size_bucket = assign_bet_bucket(pot_ratio)

                ah_present = int(feat.get('_action_history_present', 0))  # CRIT #2
                rows.append(vec + [action, size_bucket, ah_present])
            except RuntimeError:
                # MUST #9 — let CRIT #2 strict-raise propagate; swallowing
                # would reduce loud-fail to silent errors++ and make
                # STAGE4_STRICT_ACTION_HISTORY=raise a no-op.
                raise
            except Exception as e:
                errors += 1
    
    elapsed = time.time() - t0
    new_offset = min(line_num, offset + batch_size)
    
    # Append rows to CSV
    with open(out_file, 'a', newline='') as f:
        csv.writer(f).writerows(rows)
    
    # Save offset
    with open(offset_file, 'w') as f:
        f.write(str(new_offset))
    
    # Count total rows in file
    with open(out_file) as f:
        total_rows = sum(1 for _ in f) - 1
    
    done_pct = new_offset / 25000 * 100
    print(f"Chunk {chunk_id:02d}: +{len(rows)} rows ({errors} err) in {elapsed:.0f}s | "
          f"offset {offset}â†’{new_offset} ({done_pct:.0f}%) | total={total_rows}")

if __name__ == '__main__':
    main()
