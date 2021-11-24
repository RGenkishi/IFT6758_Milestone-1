import pandas as pd
import numpy as np
import os

import sklearn.metrics
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
import sklearn.feature_selection as fs
import matplotlib.pyplot as plt

data = pd.read_pickle(os.path.dirname(__file__) + "/data_for_models/data.pkl")
data.loc[data.change_in_shot_angle.isna(), "change_in_shot_angle"] = 0
for col in data.columns:
    median = np.median(data.loc[~data[col].isna(),col])
    data.loc[data[col].isna(),col] = median

X_base = data.loc[:,['distance_from_net', 'angle_from_net']]
y = data.loc[:,["event_type_0"]]
slc = list(range(data.shape[1]))
slc.remove(16)
slc.remove(17)
X = data.iloc[:,slc]
X_train, X_test, y_train, y_test = train_test_split(X_base, y, test_size=0.33, random_state=42)
param = {'max_depth': 6, 'eta': 1, 'objective': 'binary:logistic'}
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)
evallist = [(dtest, 'eval'), (dtrain, 'train')]
num_round = 50
bst = xgb.train(param, dtrain, num_round, evallist)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify=y)
clf_xgb = xgb.XGBClassifier(objective='binary:logistic', missing=None, seed=42, scale_pos_weight = 5)
clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric="aucpr",
            eval_set=[(X_test, y_test)])
plot_confusion_matrix(clf_xgb, X_test, y_test)
plt.show()

feature_scores = fs.mutual_info_classif(X_train, y_train, random_state=0)
best_features = []
for score, f_name in sorted(zip(feature_scores, X_train.columns), reverse=True)[:10]:
        print(f_name, score)
        best_features.append(f_name)
X = data.loc[:,best_features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify=y)
clf_xgb = xgb.XGBClassifier(objective='binary:logistic', missing=None, seed=42, scale_pos_weight = 5)
clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric="aucpr",
            eval_set=[(X_test, y_test)])
plot_confusion_matrix(clf_xgb, X_test, y_test)
plt.show()