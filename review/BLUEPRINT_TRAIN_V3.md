# Blueprint: train_model.py — v9-3way-v3 Changes

**Date:** 7 April 2026
**Author:** Architecture Expert agent
**Source plan:** review/TRAINING_PLAN_V3.md (all 5 open questions approved as recommended)
**Target file:** river-rats-core/train_model.py

All line numbers verified against the current file. If a line number
does not match, STOP and report BLOCKED.

---

## Programmer Instructions

Apply each edit in order, top to bottom. Each edit is specified as
an exact old_string → new_string for the Edit tool. After each edit,
the line numbers of subsequent edits shift — use the old_string match,
not the line number, to locate subsequent edits. Line numbers are
provided for initial orientation only.

Do not add imports not listed here. Do not reformat surrounding code.
Do not change anything not covered by a numbered change below.

---

## Change 1 — Label column detection

**File:** river-rats-core/train_model.py
**Location:** lines 60-66 (inside `load_csv`, after `reader = csv.DictReader(f)`)
**Rationale:** Current code uses `row.get('action')` which returns None for the v3
CSV (label column is `label`), causing a KeyError on `ACTION_TO_INT[None]`.

**old_string:**
```python
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            features = [float(row[col]) for col in FEATURE_COLUMNS]
            X_rows.append(features)
            action = row.get('action') or row.get('action_label')
            y_rows.append(ACTION_TO_INT[action])
```

**new_string:**
```python
    with open(filepath) as f:
        reader = csv.DictReader(f)
        # Detect label column from header — fail loudly if not found
        label_col = None
        for candidate in ['label', 'action', 'action_label']:
            if candidate in reader.fieldnames:
                label_col = candidate
                break
        if label_col is None:
            raise ValueError(f"No label column found. Headers: {reader.fieldnames}")
        for row in reader:
            features = [float(row[col]) for col in FEATURE_COLUMNS]
            X_rows.append(features)
            y_rows.append(ACTION_TO_INT[row[label_col]])
```

---

## Change 2 — Output directory default

**File:** river-rats-core/train_model.py
**Location:** line 81 (function signature of `train_and_evaluate`)
**Rationale:** Old path `/home/rupertbeytell/river-rats/river-rats-complete` does
not exist in the v2 repo. Output should go to `river-rats-core/models/`.

**old_string:**
```python
def train_and_evaluate(csv_path: str, output_dir: str = '/home/rupertbeytell/river-rats/river-rats-complete'):
```

**new_string:**
```python
def train_and_evaluate(csv_path: str, output_dir: str = 'river-rats-core/models'):
```

---

## Change 3 — Hyperparameters (primary model)

**File:** river-rats-core/train_model.py
**Location:** lines 114-130 (XGBClassifier instantiation inside `train_and_evaluate`)
**Rationale:** Update to v3 values per Section 4 of training plan.

**old_string:**
```python
    model = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=30,
    )
```

**new_string:**
```python
    model = xgb.XGBClassifier(
        n_estimators=800,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=50,
    )
```

---

## Change 4 — Sample weights + model.fit() call

**File:** river-rats-core/train_model.py
**Location:** lines 132-136 (model.fit() call, immediately after the XGBClassifier block)
**Rationale:** Add inverse-frequency sample weights with RAISE capped at 3.0,
then pass to model.fit(). This is the complete replacement of the fit block —
the weight computation and the fit call are one atomic change.

**old_string:**
```python
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False,
    )
```

**new_string:**
```python
    # Inverse-frequency sample weights — RAISE capped at 3.0 (see training plan Section 5)
    class_counts = Counter(y_train)
    majority_count = float(class_counts[ACTION_TO_INT['CHECK']])
    raw_weights = {cls: majority_count / count for cls, count in class_counts.items()}
    RAISE_IDX = ACTION_TO_INT['RAISE']
    raw_weights[RAISE_IDX] = min(raw_weights[RAISE_IDX], 3.0)
    sample_weight_train = np.array([raw_weights[label] for label in y_train], dtype=np.float32)

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        sample_weight=sample_weight_train,
        verbose=False,
    )
```

---

## Change 5 — Hyperparameters (CV model)

**File:** river-rats-core/train_model.py
**Location:** lines 168-183 (cv_model XGBClassifier instantiation)
**Rationale:** CV model must use same hyperparameters as primary model. Also
update early_stopping comment to remove (outdated note about external test set).

**old_string:**
```python
    cv_model = xgb.XGBClassifier(
        n_estimators=best_iteration,  # Use best iteration from above
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_weight=3,
        gamma=0.1,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
    )
```

**new_string:**
```python
    cv_model = xgb.XGBClassifier(
        n_estimators=best_iteration,  # Use best iteration from above
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
    )
```

---

## Change 5b — CV step must use sample weights (reviewer fix)

**File:** river-rats-core/train_model.py
**Location:** immediately before the `y_cv_pred = cross_val_predict(...)` call
(after Change 5's cv_model definition)
**Rationale:** The shipped model trains with RAISE weight 3.0 but the CV step
trains unweighted. This makes CV results non-comparable with the shipped model.
Fix: compute weights from full y and pass via fit_params.

**old_string:**
```python
    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv)
```

**new_string:**
```python
    # Sample weights for CV must match the shipped model's weighting
    cv_class_counts = Counter(y)
    cv_majority = float(cv_class_counts[ACTION_TO_INT['CHECK']])
    cv_weights = {cls: cv_majority / count for cls, count in cv_class_counts.items()}
    cv_weights[ACTION_TO_INT['RAISE']] = min(cv_weights[ACTION_TO_INT['RAISE']], 3.0)
    sample_weight_all = np.array([cv_weights[label] for label in y], dtype=np.float32)
    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv, fit_params={'sample_weight': sample_weight_all})
```

**Same fix in train_45feat_diagnostic:** The diagnostic function's CV call
(inside Change 8) must also pass sample weights. The programmer applies the
identical pattern: compute weights from full y, pass via fit_params.

In the diagnostic function, change:
```python
    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv)
```
to:
```python
    cv_class_counts = Counter(y)
    cv_majority = float(cv_class_counts[ACTION_TO_INT['CHECK']])
    cv_weights = {cls: cv_majority / count for cls, count in cv_class_counts.items()}
    cv_weights[ACTION_TO_INT['RAISE']] = min(cv_weights[ACTION_TO_INT['RAISE']], 3.0)
    sample_weight_all = np.array([cv_weights[label] for label in y], dtype=np.float32)
    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv, fit_params={'sample_weight': sample_weight_all})
```

---

## Change 6 — Version detection (replace path-based logic with explicit constant)

**File:** river-rats-core/train_model.py
**Location:** lines 216-225 (version detection block and model_path line)
**Rationale:** Path-based version detection is fragile and produces wrong version
strings (maps v3 path to 'v8', not 'v9_3way_v3'). Use an explicit constant.
The model filename also changes from `_38feat` suffix to no suffix.

**old_string:**
```python
    # ---- Determine version from data path ----
    if 'v3' in csv_path or '38feat_v3' in csv_path:
        model_version = 'v8'
    elif 'v2' in csv_path or '38feat_v2' in csv_path:
        model_version = 'v7'
    else:
        model_version = 'v6'

    # ---- Export Model as JSON ----
    model_path = os.path.join(output_dir, f'gto_model_{model_version}_38feat.json')
```

**new_string:**
```python
    # ---- Version (explicit — not derived from path) ----
    model_version = 'v9_3way_v3'

    # ---- Export Model as JSON ----
    model_path = os.path.join(output_dir, f'gto_model_{model_version}.json')
```

---

## Change 7 — Report filename (matches model_version change)

**File:** river-rats-core/train_model.py
**Location:** line 245 (report_path assignment)
**Rationale:** The report filename uses model_version, which now has no `_38feat`
suffix embedded in the path — this change is already implied by Change 6, but
the report_path line is separate and must be verified to still read correctly.

No edit required here — line 245 is:
```python
    report_path = os.path.join(output_dir, f'training_report_{model_version}.json')
```
This uses `model_version` which is now `v9_3way_v3`, so the report will be
`training_report_v9_3way_v3.json`. No change needed. Programmer confirms this
line is unchanged and still uses the `model_version` variable.

---

## Change 8 — Default CSV path and __main__ block

**File:** river-rats-core/train_model.py
**Location:** lines 265-276 (the `if __name__ == '__main__':` block)
**Rationale:** Default path points to old v1 repo. Replace the entire __main__
block to: (a) point default CSV to v3 training data, (b) add `--45feat` flag
for the diagnostic 45-feature run (training plan Section 8 Run 2), (c) remove
stale `--full` / `--v1` / `--v3` flags that reference non-existent paths.

**old_string:**
```python
if __name__ == '__main__':
    csv_file = '/home/rupertbeytell/river-rats/training_data_38feat_v2/train_action_38.csv'
    if '--full' in sys.argv or '--v1' in sys.argv:
        csv_file = '/home/rupertbeytell/river-rats/training_data_38feat/train_action_38.csv'
    elif '--v3' in sys.argv:
        csv_file = '/home/rupertbeytell/river-rats/training_data_38feat_v3/train_action_38.csv'

    if not os.path.exists(csv_file):
        print(f"ERROR: {csv_file} not found. Run feature extraction first.")
        sys.exit(1)

    train_and_evaluate(csv_file)
```

**new_string:**
```python
# Features to drop for the 45-feature diagnostic run (training plan Section 8 Run 2)
FEATURES_48_ONLY = ['flush_block_pct', 'overcard_outs', 'improvement_probability']


def train_45feat_diagnostic(csv_path: str, output_dir: str = 'river-rats-core/models'):
    """
    Diagnostic run on 45 features only (drops the 3 new v3 features).
    Compares directly against the 48-feature primary run.
    Output: gto_model_v9_3way_v3_45feat.json
    """
    import xgboost as xgb
    from sklearn.model_selection import (
        StratifiedKFold, cross_val_predict, train_test_split
    )
    from sklearn.metrics import accuracy_score, classification_report

    print("=" * 60)
    print("GTO Oracle V3 -- 45-Feature Diagnostic Run")
    print("=" * 60)

    feat_45 = [f for f in FEATURE_COLUMNS if f not in FEATURES_48_ONLY]
    feat_idx = [FEATURE_COLUMNS.index(f) for f in feat_45]

    X_full, y = load_csv(csv_path)
    X = X_full[:, feat_idx]
    print(f"  Using {X.shape[1]} features (dropped: {FEATURES_48_ONLY})")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    class_counts = Counter(y_train)
    majority_count = float(class_counts[ACTION_TO_INT['CHECK']])
    raw_weights = {cls: majority_count / count for cls, count in class_counts.items()}
    RAISE_IDX = ACTION_TO_INT['RAISE']
    raw_weights[RAISE_IDX] = min(raw_weights[RAISE_IDX], 3.0)
    sample_weight_train = np.array([raw_weights[label] for label in y_train], dtype=np.float32)

    model = xgb.XGBClassifier(
        n_estimators=800,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
        early_stopping_rounds=50,
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        sample_weight=sample_weight_train,
        verbose=False,
    )
    best_iteration = model.best_iteration
    print(f"  Best iteration: {best_iteration}")

    y_pred = model.predict(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    print(f"  Test Accuracy: {test_acc:.4f} ({test_acc:.1%})")
    print(classification_report(y_test, y_pred, target_names=ACTION_CLASSES, digits=3))

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_model = xgb.XGBClassifier(
        n_estimators=best_iteration,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.75,
        min_child_weight=5,
        gamma=0.2,
        reg_alpha=0.1,
        reg_lambda=1.0,
        objective='multi:softprob',
        num_class=5,
        eval_metric='mlogloss',
        random_state=42,
        n_jobs=-1,
    )
    y_cv_pred = cross_val_predict(cv_model, X, y, cv=cv)
    cv_acc = accuracy_score(y, y_cv_pred)
    print(f"  5-Fold CV Accuracy: {cv_acc:.4f} ({cv_acc:.1%})")
    print(classification_report(y, y_cv_pred, target_names=ACTION_CLASSES, digits=3))

    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'gto_model_v9_3way_v3_45feat.json')
    model.save_model(model_path)
    print(f"\n  Model saved: {model_path}")
    return model


if __name__ == '__main__':
    csv_file = 'training-data/train_3way_v3_combined.csv'

    if not os.path.exists(csv_file):
        print(f"ERROR: {csv_file} not found.")
        sys.exit(1)

    if '--45feat' in sys.argv:
        # Run 2: diagnostic 45-feature comparison (training plan Section 8)
        train_45feat_diagnostic(csv_file)
    else:
        # Run 1: primary 48-feature training (training plan Section 8)
        os.makedirs('river-rats-core/models', exist_ok=True)
        train_and_evaluate(csv_file)
```

---

## Change 9 — Add os.makedirs guard to train_and_evaluate

**File:** river-rats-core/train_model.py
**Location:** immediately before the model.save_model(model_path) call (line 226)
**Rationale:** `river-rats-core/models/` may not exist yet. Without this guard,
`model.save_model()` raises FileNotFoundError. The __main__ block calls makedirs
for Run 1, but train_and_evaluate should also be safe when called directly.

**old_string:**
```python
    model_path = os.path.join(output_dir, f'gto_model_{model_version}.json')
    model.save_model(model_path)
```

**new_string:**
```python
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, f'gto_model_{model_version}.json')
    model.save_model(model_path)
```

---

## Post-edit verification checklist

The programmer runs these checks after all edits are applied, before
declaring done:

1. `python3 -c "import ast; ast.parse(open('river-rats-core/train_model.py').read()); print('syntax OK')`
   — must print "syntax OK"

2. `grep -n "row.get('action')" river-rats-core/train_model.py`
   — must return no matches

3. `grep -n "river-rats-complete" river-rats-core/train_model.py`
   — must return no matches

4. `grep -n "model_version" river-rats-core/train_model.py`
   — must show the assignment `model_version = 'v9_3way_v3'` and usages only

5. `grep -n "n_estimators" river-rats-core/train_model.py`
   — must show 800 for both primary model and diagnostic model,
     and `best_iteration` for both cv_model instances

6. `grep -n "early_stopping_rounds" river-rats-core/train_model.py`
   — must show 50 (not 30)

7. `grep -n "sample_weight" river-rats-core/train_model.py`
   — must appear in both train_and_evaluate and train_45feat_diagnostic

8. `grep -n "45feat" river-rats-core/train_model.py`
   — must show the CLI flag check and the output filename

9. `grep -n "train_3way_v3_combined" river-rats-core/train_model.py`
   — must show as the default csv_file in __main__

If any check fails, STOP and report BLOCKED with the grep output.

---

## Summary of changes

| # | Location | What changes |
|---|----------|-------------|
| 1 | `load_csv` lines 60-66 | Header-detected label column replaces `row.get('action')` |
| 2 | `train_and_evaluate` signature line 81 | Output dir default to `river-rats-core/models` |
| 3 | Primary XGBClassifier lines 114-130 | n_estimators 500->800, max_depth 6->5, lr 0.1->0.05, colsample 0.8->0.75, min_child_weight 3->5, gamma 0.1->0.2, early_stopping 30->50 |
| 4 | `model.fit()` lines 132-136 | Add inverse-frequency sample_weight with RAISE cap 3.0 |
| 5 | CV XGBClassifier lines 168-183 | Same hyperparameter changes as primary model |
| 6 | Version detection lines 216-225 | Replace path-based detection with `model_version = 'v9_3way_v3'`; drop `_38feat` from filename |
| 7 | report_path line 245 | No change required — already uses `model_version` variable |
| 8 | `__main__` block lines 265-276 | Default CSV to v3 path; add `--45feat` flag; add `train_45feat_diagnostic` function |
| 9 | Before `model.save_model()` | Add `os.makedirs(output_dir, exist_ok=True)` |
