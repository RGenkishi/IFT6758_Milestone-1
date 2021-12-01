from comet_ml import Experiment
from ift6758.data.milestone2.question_3 import roc_curve_and_auc_metrique, goal_rate_curve, goal_cumulative_proportion_curve, calibration_display_curve
import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
import sklearn.feature_selection as fs
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve, auc

with open("API_KEY", "r") as f:
    API_KEY = f.readline()
exp = Experiment(
    api_key=API_KEY, # don’t hardcode!!
    project_name='milestone_2',
    workspace="genkishi"
)
__file__ = '/home/olivier/Documents/IFT6758/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features/'
data = pd.read_pickle(os.path.dirname(__file__) + "/data_for_models/data.pkl")


##Base case
X_base = data.loc[:,['distance_from_net', 'angle_from_net']]
y = data.loc[:,["event_type_0"]]
X_train, X_test, y_train, y_test = train_test_split(X_base, y, test_size=0.30, random_state=42)

clf_xgb = xgb.XGBClassifier(objective='binary:logistic', missing=None, seed=42, scale_pos_weight = 5)
clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric="auc",
            eval_set=[(X_test, y_test)])
proba = clf_xgb.predict_proba(X_test)
df_proba = pd.DataFrame(proba)
roc_curve_and_auc_metrique(proba, y_test, "baseline_XGBoost")
goal_rate_curve(proba, y_test, "baseline_XGBoost")
goal_cumulative_proportion_curve(proba, y_test, "baseline_XGBoost")
calibration_display_curve(proba, y_test, "baseline_XGBoost")





