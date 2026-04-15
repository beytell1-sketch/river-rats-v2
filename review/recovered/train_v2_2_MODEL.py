# Recovered from Claude Code session transcript
# Session: 81bf3fe7-5f95-4ea9-90fc-04263a5e8161 (Apr 15 2026)
# Original execution: bash python3 heredoc, no script committed at the time
# Recovered for ANOMALY-A verification — see Track 3.5 trainer recovery

"""Phase 4: v2.2 XGBoost training on 108-column CSV (54 raw + 54 attn_*)."""
import csv, json, os
from collections import Counter
import numpy as np

# Load CSV
rows = []
with open('training-data/v2_2_training.csv') as f:
    for r in csv.DictReader(f):
        rows.append(r)
print(f"Loaded {len(rows)} rows")

# Feature columns: 54 raw + 54 attn_*
raw_features = [c for c in rows[0].keys() if c not in ('situation_id','label','label_source') and not c.startswith('attn_')]
attn_features = [c for c in rows[0].keys() if c.startswith('attn_')]
print(f"  Raw features: {len(raw_features)}")
print(f"  Attn features: {len(attn_features)}")

def to_float(v):
    if v in ('', None): return 0.0
    # Convert string categorical codes (e.g. hero_position='BTN') — map per feature
    try: return float(v)
    except: return 0.0

# Categorical columns that need encoding
CAT_MAPS = {
    'street': {'flop':0,'turn':1,'river':2,'':0},
    'hero_position': {'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
    'villain_position': {'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},
}

def encode(row, col):
    if col in CAT_MAPS:
        val = row[col]
        try: return float(val)
        except: return float(CAT_MAPS[col].get(val, 0))
    return to_float(row[col])

ACTION_TO_INT = {'FOLD':0,'CHECK':1,'CALL':2,'BET':3,'RAISE':4}
INT_TO_ACTION = {v:k for k,v in ACTION_TO_INT.items()}

X = np.array([[encode(r, c) for c in raw_features + attn_features] for r in rows], dtype=np.float32)
y = np.array([ACTION_TO_INT[r['label']] for r in rows], dtype=np.int32)
print(f"X shape: {X.shape}, y shape: {y.shape}")
print(f"Class distribution: {dict(Counter(INT_TO_ACTION[int(i)] for i in y))}")

# 80/20 split
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
print(f"\nTrain: {X_tr.shape[0]}, Test: {X_te.shape[0]}")

# Class weights
class_counts = Counter(y_tr)
max_c = max(class_counts.values())
raw_w = {c: min(max_c / n, 3.0 if INT_TO_ACTION[c]=='RAISE' else (2.0 if INT_TO_ACTION[c]=='BET' else 4.0))
         for c, n in class_counts.items()}
print(f"Class weights: {{ {', '.join(f'{INT_TO_ACTION[c]}:{w:.2f}' for c,w in raw_w.items())} }}")
sw_tr = np.array([raw_w[int(lbl)] for lbl in y_tr], dtype=np.float32)

model = xgb.XGBClassifier(
    n_estimators=800, max_depth=5, learning_rate=0.05,
    objective='multi:softprob', num_class=5,
    eval_metric='mlogloss', use_label_encoder=False,
    random_state=42, early_stopping_rounds=50, verbosity=0)
model.fit(X_tr, y_tr, sample_weight=sw_tr, eval_set=[(X_te, y_te)], verbose=False)
best_iter = model.best_iteration
print(f"Best iteration: {best_iter}")

# Test evaluation
y_pred = model.predict(X_te)
test_acc = accuracy_score(y_te, y_pred)
print(f"\nHoldout test accuracy: {test_acc:.4f}")
print("Per-class:")
print(classification_report(y_te, y_pred, target_names=[INT_TO_ACTION[i] for i in sorted(set(y))], zero_division=0))

# 5-fold stratified CV
print("\n--- 5-fold stratified CV ---")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_accs = []
for fold, (tr_idx, te_idx) in enumerate(cv.split(X, y)):
    cnt = Counter(y[tr_idx])
    mc = max(cnt.values())
    rw = {c: min(mc/n, 3.0 if INT_TO_ACTION[c]=='RAISE' else (2.0 if INT_TO_ACTION[c]=='BET' else 4.0)) for c,n in cnt.items()}
    sw = np.array([rw[int(lbl)] for lbl in y[tr_idx]], dtype=np.float32)
    m = xgb.XGBClassifier(n_estimators=best_iter, max_depth=5, learning_rate=0.05,
                          objective='multi:softprob', num_class=5, random_state=42, verbosity=0,
                          eval_metric='mlogloss')
    m.fit(X[tr_idx], y[tr_idx], sample_weight=sw, verbose=False)
    p = m.predict(X[te_idx])
    a = accuracy_score(y[te_idx], p)
    cv_accs.append(a)
    print(f"  Fold {fold+1}: {a:.4f}")
print(f"  Mean CV: {np.mean(cv_accs):.4f} ± {np.std(cv_accs):.4f}")

# Save model
os.makedirs('river-rats-core/models', exist_ok=True)
model.save_model('river-rats-core/models/v2_2_model.json')
print(f"\nSaved river-rats-core/models/v2_2_model.json")

# Save training report
report = {
    'model_version': 'v2_2',
    'n_samples': len(rows),
    'n_features': X.shape[1],
    'features_raw': len(raw_features),
    'features_attn': len(attn_features),
    'class_distribution': {INT_TO_ACTION[int(c)]: int(n) for c,n in Counter(y).items()},
    'class_weights': {INT_TO_ACTION[int(c)]: float(w) for c,w in raw_w.items()},
    'best_iteration': int(best_iter),
    'holdout_test_accuracy': float(test_acc),
    'cv_accuracies': [float(a) for a in cv_accs],
    'cv_mean': float(np.mean(cv_accs)),
    'cv_std': float(np.std(cv_accs)),
    'hyperparameters': {'n_estimators':800,'max_depth':5,'learning_rate':0.05},
}
with open('river-rats-core/models/v2_2_training_report.json','w') as f:
    json.dump(report, f, indent=2)
print(f"Saved river-rats-core/models/v2_2_training_report.json")