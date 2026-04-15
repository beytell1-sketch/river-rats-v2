# Recovered from Claude Code session transcript
# Session: 81bf3fe7-5f95-4ea9-90fc-04263a5e8161 (Apr 15 2026)
# Original execution: bash python3 heredoc, no script committed at the time
# Recovered for ANOMALY-A verification — see Track 3.5 trainer recovery

"""Try FB-40 again with per-feature training-rate attn values (instead of all 1)."""
import json, csv, os, sys
from collections import Counter
import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report

sys.path.insert(0, 'river-rats-core')
from feature_extractor import extract_all_features

rows = list(csv.DictReader(open('training-data/v2_2_training.csv')))
header = list(rows[0].keys())
raw_features = [c for c in header if c not in ('situation_id','label','label_source') and not c.startswith('attn_')]
attn_features = [c for c in header if c.startswith('attn_')]
all_features = raw_features + attn_features

ACTION_TO_INT = {'FOLD':0,'CHECK':1,'CALL':2,'BET':3,'RAISE':4}
INT_TO_ACTION = {v:k for k,v in ACTION_TO_INT.items()}
CAT_MAPS = {'street':{'flop':0,'turn':1,'river':2,'':0},
            'hero_position':{'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
            'villain_position':{'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0}}
def encode(row, col):
    v = row.get(col,'')
    if col in CAT_MAPS:
        try: return float(v)
        except: return float(CAT_MAPS[col].get(v,0))
    try: return float(v)
    except: return 0.0

X_train = np.array([[encode(r,c) for c in all_features] for r in rows], dtype=np.float32)
y_train = np.array([ACTION_TO_INT[r['label']] for r in rows], dtype=np.int32)

# attn_ training-set rates
attn_rate = {}
for c in attn_features:
    vals = [float(r[c]) for r in rows]
    attn_rate[c] = sum(vals) / len(vals)

cnt = Counter(y_train); mc=max(cnt.values())
raw_w = {c: min(mc/n, 3.0 if INT_TO_ACTION[c]=='RAISE' else (2.0 if INT_TO_ACTION[c]=='BET' else 4.0)) for c,n in cnt.items()}
sw = np.array([raw_w[int(l)] for l in y_train], dtype=np.float32)

model = xgb.XGBClassifier(n_estimators=95, max_depth=5, learning_rate=0.05,
    objective='multi:softprob', num_class=5, random_state=42, verbosity=0, eval_metric='mlogloss')
model.fit(X_train, y_train, sample_weight=sw, verbose=False)

# FB-40
fb_hands = [json.loads(l) for l in open('training-data/facing_bet_test_set_40.jsonl')]
street_map = {'flop':'f','turn':'t','river':'r'}
fb_X_rate=[]; fb_y=[]
for h in fb_hands:
    hand_dict = {'h':h['hero_cards'],'b':h['board'],'pos':h['hero_pos'],
                 'vp':h['villain_positions'][0] if h.get('villain_positions') else 'BB',
                 'pot':h['pot'],'tc':h['to_call'],'st':street_map.get(h['street'],'f'),
                 'fb':int(h['facing_bet']),'exp':'C'}
    feats = extract_all_features(hand_dict)
    row = {'street':h['street'],'hero_position':h['hero_pos'],'villain_position':hand_dict['vp']}
    row.update(feats)
    # Use training-rate as attn probability (threshold 0.5 for binary)
    for c in attn_features:
        row[c] = 1.0 if attn_rate[c] >= 0.5 else 0.0
    fb_X_rate.append([encode(row,c) for c in all_features])
    fb_y.append(ACTION_TO_INT[h['expected_action']])
fb_X_rate = np.array(fb_X_rate, dtype=np.float32); fb_y=np.array(fb_y)
pred_rate = model.predict(fb_X_rate)
acc_rate = accuracy_score(fb_y, pred_rate)
print(f"FB-40 with training-rate attn (>=50% threshold): {acc_rate:.4f} ({sum(pred_rate==fb_y)}/{len(fb_y)})")

# Try all-zero
fb_X_zero = fb_X_rate.copy()
for c in attn_features:
    idx = all_features.index(c)
    fb_X_zero[:, idx] = 0
pred_zero = model.predict(fb_X_zero)
acc_zero = accuracy_score(fb_y, pred_zero)
print(f"FB-40 with all attn=0: {acc_zero:.4f} ({sum(pred_zero==fb_y)}/{len(fb_y)})")

# Try all-one
fb_X_one = fb_X_rate.copy()
for c in attn_features:
    idx = all_features.index(c)
    fb_X_one[:, idx] = 1
pred_one = model.predict(fb_X_one)
acc_one = accuracy_score(fb_y, pred_one)
print(f"FB-40 with all attn=1: {acc_one:.4f} ({sum(pred_one==fb_y)}/{len(fb_y)})")

# Raw-features-only model (no attn)
print("\n--- Raw-features-only model (54 features, no attn) ---")
X_raw = X_train[:, :len(raw_features)]
model_raw = xgb.XGBClassifier(n_estimators=95, max_depth=5, learning_rate=0.05,
    objective='multi:softprob', num_class=5, random_state=42, verbosity=0, eval_metric='mlogloss')
model_raw.fit(X_raw, y_train, sample_weight=sw, verbose=False)
fb_X_raw = fb_X_rate[:, :len(raw_features)]
pred_raw = model_raw.predict(fb_X_raw)
acc_raw = accuracy_score(fb_y, pred_raw)
print(f"FB-40 raw-only: {acc_raw:.4f} ({sum(pred_raw==fb_y)}/{len(fb_y)})")

# 5-fold CV of raw-only
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_accs = []
for tr, te in cv.split(X_raw, y_train):
    c = Counter(y_train[tr]); m = max(c.values())
    w = {cl: min(m/n, 3.0 if INT_TO_ACTION[cl]=='RAISE' else (2.0 if INT_TO_ACTION[cl]=='BET' else 4.0)) for cl,n in c.items()}
    s = np.array([w[int(l)] for l in y_train[tr]], dtype=np.float32)
    mm = xgb.XGBClassifier(n_estimators=95, max_depth=5, learning_rate=0.05, objective='multi:softprob',
                          num_class=5, random_state=42, verbosity=0, eval_metric='mlogloss')
    mm.fit(X_raw[tr], y_train[tr], sample_weight=s, verbose=False)
    cv_accs.append(accuracy_score(y_train[te], mm.predict(X_raw[te])))
print(f"  Raw-only 5-fold CV: {np.mean(cv_accs):.4f} ± {np.std(cv_accs):.4f}")

# Full model 5-fold already done at 0.9299
print(f"\nSummary:")
print(f"  Training (108 feat, CV): 0.9299")
print(f"  Training (54 feat, CV):  {np.mean(cv_accs):.4f}")
print(f"  FB-40 all attn=1:        {acc_one:.4f}")
print(f"  FB-40 rate attn:         {acc_rate:.4f}")
print(f"  FB-40 all attn=0:        {acc_zero:.4f}")
print(f"  FB-40 raw-only model:    {acc_raw:.4f}")