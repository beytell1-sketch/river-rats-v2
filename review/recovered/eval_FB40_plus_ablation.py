# Recovered from Claude Code session transcript
# Session: 81bf3fe7-5f95-4ea9-90fc-04263a5e8161 (Apr 15 2026)
# Original execution: bash python3 heredoc, no script committed at the time
# Recovered for ANOMALY-A verification — see Track 3.5 trainer recovery

"""Phase 4 continued: FB-40 test set evaluation + villain_range_capped ablation."""
import json, csv, os
from collections import Counter
import numpy as np

# Load v2.2 training CSV to get column order / feature vocab
with open('training-data/v2_2_training.csv') as f:
    header = next(csv.reader(f))
raw_features = [c for c in header if c not in ('situation_id','label','label_source') and not c.startswith('attn_')]
attn_features = [c for c in header if c.startswith('attn_')]
all_features = raw_features + attn_features

ACTION_TO_INT = {'FOLD':0,'CHECK':1,'CALL':2,'BET':3,'RAISE':4}
INT_TO_ACTION = {v:k for k,v in ACTION_TO_INT.items()}
CAT_MAPS = {
    'street': {'flop':0,'turn':1,'river':2,'':0},
    'hero_position': {'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
    'villain_position': {'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
}
def encode(row, col):
    v = row.get(col, '')
    if col in CAT_MAPS:
        try: return float(v)
        except: return float(CAT_MAPS[col].get(v,0))
    try: return float(v)
    except: return 0.0

# Load v2.2 training data again
import csv
train_rows = list(csv.DictReader(open('training-data/v2_2_training.csv')))
X_train_full = np.array([[encode(r, c) for c in all_features] for r in train_rows], dtype=np.float32)
y_train_full = np.array([ACTION_TO_INT[r['label']] for r in train_rows], dtype=np.int32)

# Class weights
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report

cnt = Counter(y_train_full); mc = max(cnt.values())
raw_w = {c: min(mc/n, 3.0 if INT_TO_ACTION[c]=='RAISE' else (2.0 if INT_TO_ACTION[c]=='BET' else 4.0)) for c,n in cnt.items()}
sw = np.array([raw_w[int(lbl)] for lbl in y_train_full], dtype=np.float32)

def train_model(X, y, sw, n_est=95):
    m = xgb.XGBClassifier(n_estimators=n_est, max_depth=5, learning_rate=0.05,
                          objective='multi:softprob', num_class=5, random_state=42, verbosity=0,
                          eval_metric='mlogloss')
    m.fit(X, y, sample_weight=sw, verbose=False)
    return m

# ============ FULL MODEL ============
print("Training full v2.2 model (108 features)...")
full_model = train_model(X_train_full, y_train_full, sw, n_est=95)

# ============ FB-40 evaluation ============
print("\n--- FB-40 evaluation ---")
# Load feature_extractor to compute features from test situations
import sys
sys.path.insert(0, 'river-rats-core')
from feature_extractor import extract_all_features
from gto_model import FEATURE_COLUMNS

fb_hands = [json.loads(l) for l in open('training-data/facing_bet_test_set_40.jsonl')]
print(f"  {len(fb_hands)} FB hands")

# Map FB field names to extract_all_features input format
street_map = {'flop':'f','turn':'t','river':'r'}

fb_X = []; fb_y = []; fb_ids = []
for h in fb_hands:
    # Build hand_dict for extractor
    try:
        hand_dict = {
            'h': h['hero_cards'], 'b': h['board'],
            'pos': h['hero_pos'], 'vp': h['villain_positions'][0] if h.get('villain_positions') else 'BB',
            'pot': h['pot'], 'tc': h['to_call'],
            'st': street_map.get(h['street'],'f'), 'fb': int(h['facing_bet']),
            'exp': 'C',
        }
        feats = extract_all_features(hand_dict)
    except Exception as e:
        print(f"  Extract failed for {h['situation_id']}: {e}")
        continue
    row = {'street': h['street'], 'hero_position': h['hero_pos'], 'villain_position': h.get('villain_positions',['BB'])[0]}
    row.update({k: v for k,v in feats.items()})
    # All attn flags = 1 (we don't have labelling info for test hands; assume all relevant)
    for col in attn_features: row[col] = 1.0
    fb_X.append([encode(row, c) for c in all_features])
    fb_y.append(ACTION_TO_INT[h['expected_action']])
    fb_ids.append(h['situation_id'])

fb_X = np.array(fb_X, dtype=np.float32); fb_y = np.array(fb_y)
fb_pred = full_model.predict(fb_X)
fb_acc = accuracy_score(fb_y, fb_pred)
print(f"  FB-40 accuracy: {fb_acc:.4f} ({sum(fb_pred==fb_y)}/{len(fb_y)})")
print(f"  Target: ≥0.70 → {'✓ PASS' if fb_acc >= 0.70 else '✗ FAIL'}")

# Per-class
print(classification_report(fb_y, fb_pred, target_names=['FOLD','CHECK','CALL','BET','RAISE'], zero_division=0, labels=[0,1,2,3,4]))

# ============ Reference set (MW hands from test_set_50) ============
print("\n--- MW reference set evaluation ---")
mw_hands = [json.loads(l) for l in open('training-data/test_set_50_labelled.jsonl')]
mw_hands = [h for h in mw_hands if h.get('situation_id','').startswith('MW-')][:50]
print(f"  {len(mw_hands)} MW hands")

mw_X = []; mw_y = []
for h in mw_hands:
    try:
        hand_dict = {
            'h': h['hero_cards'], 'b': h.get('board',''),
            'pos': h.get('hero_pos') or h.get('hero_position','BB'),
            'vp': (h.get('villain_positions') or ['BB'])[0],
            'pot': h.get('pot',90), 'tc': h.get('to_call',0),
            'st': street_map.get(h.get('street','flop'),'f'),
            'fb': int(h.get('facing_bet',0)),
            'exp': 'C',
        }
        feats = extract_all_features(hand_dict)
    except Exception as e:
        continue
    row = {'street': h.get('street','flop'), 'hero_position': hand_dict['pos'], 'villain_position': hand_dict['vp']}
    row.update(feats)
    for col in attn_features: row[col] = 1.0
    mw_X.append([encode(row, c) for c in all_features])
    expected = h.get('expected_action') or h.get('label') or h.get('action')
    mw_y.append(ACTION_TO_INT.get(expected, 0))

if mw_X:
    mw_X = np.array(mw_X, dtype=np.float32); mw_y = np.array(mw_y)
    mw_pred = full_model.predict(mw_X)
    mw_acc = accuracy_score(mw_y, mw_pred)
    print(f"  MW accuracy: {mw_acc:.4f} ({sum(mw_pred==mw_y)}/{len(mw_y)})")
    print(f"  Target: ≥0.825 → {'✓ PASS' if mw_acc >= 0.825 else '✗ FAIL'}")
else:
    print("  Could not extract MW features")
    mw_acc = None

# ============ Ablation: drop villain_range_capped ============
print("\n--- Ablation: villain_range_capped ---")
vrc_idx = all_features.index('villain_range_capped')
attn_vrc_idx = all_features.index('attn_villain_range_capped') if 'attn_villain_range_capped' in all_features else None

X_noablate = X_train_full.copy()
X_ablate = X_train_full.copy(); X_ablate[:, vrc_idx] = 0
if attn_vrc_idx is not None: X_ablate[:, attn_vrc_idx] = 0

fb_X_ablate = fb_X.copy(); fb_X_ablate[:, vrc_idx] = 0
if attn_vrc_idx is not None: fb_X_ablate[:, attn_vrc_idx] = 0

# Retrain without villain_range_capped
print("  Retraining without villain_range_capped...")
ablate_model = train_model(X_ablate, y_train_full, sw, n_est=95)
fb_pred_ab = ablate_model.predict(fb_X_ablate)
fb_acc_ab = accuracy_score(fb_y, fb_pred_ab)
print(f"  FB-40 accuracy (ablated): {fb_acc_ab:.4f}")
print(f"  Delta vs full: {fb_acc_ab - fb_acc:+.4f}")

# Summary report
report = {
    'model': 'v2.2',
    'n_features': X_train_full.shape[1],
    'training_cv_mean': 0.9299,
    'training_cv_std': 0.0345,
    'holdout_test_acc': 0.8831,
    'fb_40_accuracy': float(fb_acc),
    'fb_40_target': 0.70,
    'fb_40_pass': bool(fb_acc >= 0.70),
    'mw_reference_accuracy': float(mw_acc) if mw_acc is not None else None,
    'mw_reference_target': 0.825,
    'mw_reference_pass': bool(mw_acc >= 0.825) if mw_acc is not None else None,
    'villain_range_capped_ablation_fb': float(fb_acc_ab),
    'villain_range_capped_delta': float(fb_acc_ab - fb_acc),
}
with open('river-rats-core/models/v2_2_evaluation_report.json','w') as f:
    json.dump(report, f, indent=2)
print(f"\nWrote river-rats-core/models/v2_2_evaluation_report.json")
print(f"\n===== PHASE 4 EVAL SUMMARY =====")
for k,v in report.items(): print(f"  {k}: {v}")