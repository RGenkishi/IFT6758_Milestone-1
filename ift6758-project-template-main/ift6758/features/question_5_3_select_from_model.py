#Comet wants to be logged before I import xgboos and sklearn
from comet_ml import Experiment
from ift6758.data.milestone2.question_3 import roc_curve_and_auc_metrique, goal_rate_curve, goal_cumulative_proportion_curve, calibration_display_curve
from ift6758.features.question_5_3_cross_validator import *
import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
import sklearn.feature_selection as fs
from sklearn.feature_selection import SelectFromModel
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score


with open("API_KEY", "r") as f:
    API_KEY = f.readline()
exp = Experiment(
    api_key=API_KEY, # don’t hardcode!!
    project_name='milestone_2',
    workspace="genkishi"
)

#We keep the same model as before
param = {}
param['max_depth'] = 6
param["scale_pos_weight"] = 5
param['min_child_weight'] = 4
param["eval_metric"] = "auc"

__file__ = '/home/olivier/Documents/IFT6758/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features/'
data = pd.read_pickle(os.path.dirname(__file__) + "/data_for_models/data.pkl")

cross_validator = CrossValidator(data, param)

clf_xgb = xgb.XGBClassifier(objective='binary:logistic',
                            missing=None,
                            seed=42,
                            scale_pos_weight = param["scale_pos_weight"],
                            max_depth=param['max_depth'],
                            min_child_weight = param["scale_pos_weight"])

slc = list(range(data.shape[1]))
slc.remove(16)
slc.remove(17)

X = data.iloc[:,slc]
y = data.loc[:,["event_type_0"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric=param["eval_metric"],
            eval_set=[(X_test, y_test)])

feature_selector = SelectFromModel(clf_xgb, prefit=True,threshold="0.65*mean")
feature_selector.feature_names_in_ = X_train.columns
best_features = feature_selector.get_support(indices=True)
best_features = X_train.columns[best_features]

feature_selection_results = cross_validator.cross_validation_on_best_features(best_features, X, y, exp, "select_from_model")
for auc in feature_selection_results.auc:
    print(auc)
    exp.log_metric("auc for each feature added", auc)

selected_features = best_features[:3]
X = data.loc[:, selected_features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric=param["eval_metric"],
            eval_set=[(X_test, y_test)])
proba = clf_xgb.predict_proba(X_test[selected_features])
roc_curve_and_auc_metrique(proba, y_test, "Feature_select_XGBoost")
goal_rate_curve(proba,y_test, "Feature_select_XGBoost")
goal_cumulative_proportion_curve(proba, y_test, "Feature_select_XGBoost")
calibration_display_curve(proba, y_test, "Feature_select_XGBoost")
clf_xgb.save_model(os.path.dirname(__file__) + "/models/XGBoost_feat_select/select_from_model.json")
exp.log_model("XGBoost_mutual_info", os.path.dirname(__file__) + "/models/XGBoost_feat_select/select_from_model.json")
plt.figure(1).savefig("/home/olivier/Documents/XGBoost_SM_roc_curve.png")
plt.figure(2).savefig("/home/olivier/Documents/XGBoost_SM_rate_curve.png")
plt.figure(3).savefig("/home/olivier/Documents/XGBoost_SM_goal_cumul.png")
plt.figure(4).savefig("/home/olivier/Documents/XGBoost_SM_calibration.png")

