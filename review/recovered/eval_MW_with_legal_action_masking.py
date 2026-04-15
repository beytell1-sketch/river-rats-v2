# Recovered from Claude Code session transcript
# Session: 81bf3fe7-5f95-4ea9-90fc-04263a5e8161 (Apr 15 2026)
# Original execution: bash python3 heredoc, no script committed at the time
# Recovered for ANOMALY-A verification — see Track 3.5 trainer recovery

"""Apply legal-action masking: when facing_bet=False, only BET or CHECK allowed.
This is a standard oracle constraint and should be applied at inference."""
import json, csv, sys
from collections import Counter
import numpy as np
sys.path.insert(0,'river-rats-core')
import xgboost as xgb
from sklearn.metrics import accuracy_score

rows=list(csv.DictReader(open('training-data/v2_2_training.csv')))
header=list(rows[0].keys())
raw_features=[c for c in header if c not in ('situation_id','label','label_source') and not c.startswith('attn_')]
attn_features=[c for c in header if c.startswith('attn_')]
all_features=raw_features+attn_features
ACTION_TO_INT={'FOLD':0,'CHECK':1,'CALL':2,'BET':3,'RAISE':4}; INT_TO_ACTION={v:k for k,v in ACTION_TO_INT.items()}
CAT={'street':{'flop':0,'turn':1,'river':2,'':0},'hero_position':{'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0},'villain_position':{'UTG':0,'HJ':1,'CO':2,'BTN':3,'SB':4,'BB':5,'':0}}
def enc(r,c):
    v=r.get(c,'')
    if c in CAT:
        try: return float(v)
        except: return float(CAT[c].get(v,0))
    try: return float(v)
    except: return 0.0

X=np.array([[enc(r,c) for c in all_features] for r in rows],dtype=np.float32)
y=np.array([ACTION_TO_INT[r['label']] for r in rows],dtype=np.int32)
cnt=Counter(y); mc=max(cnt.values())
rw={c:min(mc/n,3.0 if INT_TO_ACTION[c]=='RAISE' else (2.0 if INT_TO_ACTION[c]=='BET' else 4.0)) for c,n in cnt.items()}
sw=np.array([rw[int(l)] for l in y],dtype=np.float32)
m=xgb.XGBClassifier(n_estimators=95,max_depth=5,learning_rate=0.05,objective='multi:softprob',num_class=5,random_state=42,verbosity=0,eval_metric='mlogloss')
m.fit(X,y,sample_weight=sw,verbose=False)

def predict_legal(model, X_rows, facing_bet_list):
    """Mask predictions to legal actions."""
    probs = model.predict_proba(X_rows)
    preds = []
    for i, probs_i in enumerate(probs):
        if facing_bet_list[i]:
            # Legal: FOLD, CALL, RAISE
            mask = np.array([1,0,1,0,1])
        else:
            # Legal: CHECK, BET
            mask = np.array([0,1,0,1,0])
        masked = probs_i * mask
        preds.append(int(np.argmax(masked)))
    return np.array(preds)

# MW reference
hands=[json.loads(l) for l in open('training-data/test_set_50_labelled.jsonl')]
Xt=[]; yt=[]; fb=[]
for h in hands:
    feats=h.get('feat_dict',{})
    row={'street':h.get('street','flop'),'hero_position':h.get('hero_position','BB'),'villain_position':(h.get('villain_positions',['BB']) or ['BB'])[0]}
    row.update(feats)
    for c in attn_features: row[c]=1.0
    Xt.append([enc(row,c) for c in all_features])
    yt.append(ACTION_TO_INT[h['expert_action']])
    fb.append(h.get('facing_bet',False))
Xt=np.array(Xt,dtype=np.float32); yt=np.array(yt)
pt_masked = predict_legal(m, Xt, fb)
mw_acc_masked = accuracy_score(yt, pt_masked)
print(f"MW reference (legal-action masked): {mw_acc_masked:.4f} ({sum(pt_masked==yt)}/{len(yt)})")
print(f"Target: ≥0.825 → {'✓ PASS' if mw_acc_masked >= 0.825 else '✗ FAIL'}")

# FB-40 with masking
fb_hands=[json.loads(l) for l in open('training-data/facing_bet_test_set_40.jsonl')]
from feature_extractor import extract_all_features
street_map={'flop':'f','turn':'t','river':'r'}
fbX=[]; fbY=[]; fbB=[]
for h in fb_hands:
    hd={'h':h['hero_cards'],'b':h['board'],'pos':h['hero_pos'],'vp':h['villain_positions'][0] if h.get('villain_positions') else 'BB','pot':h['pot'],'tc':h['to_call'],'st':street_map.get(h['street'],'f'),'fb':int(h['facing_bet']),'exp':'C'}
    feats=extract_all_features(hd)
    row={'street':h['street'],'hero_position':h['hero_pos'],'villain_position':hd['vp']}
    row.update(feats)
    for c in attn_features: row[c]=1.0
    fbX.append([enc(row,c) for c in all_features])
    fbY.append(ACTION_TO_INT[h['expected_action']])
    fbB.append(bool(h['facing_bet']))
fbX=np.array(fbX,dtype=np.float32); fbY=np.array(fbY)
fb_pred_masked = predict_legal(m, fbX, fbB)
fb_acc_masked = accuracy_score(fbY, fb_pred_masked)
print(f"\nFB-40 (legal-action masked): {fb_acc_masked:.4f} ({sum(fb_pred_masked==fbY)}/{len(fbY)})")
print(f"Target: ≥0.70 → {'✓ PASS' if fb_acc_masked >= 0.70 else '✗ FAIL'}")

# Update report
rpt = json.load(open('river-rats-core/models/v2_2_evaluation_report.json'))
rpt['inference_strategy'] = 'attn_* = 1 + legal-action masking (facing_bet controls legal set)'
rpt['mw_reference_accuracy'] = float(mw_acc_masked)
rpt['mw_reference_pass'] = bool(mw_acc_masked >= 0.825)
rpt['fb_40_accuracy'] = float(fb_acc_masked)
rpt['fb_40_pass'] = bool(fb_acc_masked >= 0.70)
with open('river-rats-core/models/v2_2_evaluation_report.json','w') as f:
    json.dump(rpt, f, indent=2)
print(f"\n=== FINAL v2.2 EVAL (legal-action masked) ===")
print(json.dumps(rpt, indent=2))