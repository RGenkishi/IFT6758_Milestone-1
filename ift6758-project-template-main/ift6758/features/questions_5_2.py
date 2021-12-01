#Comet wants to be logged before I import xgboos and sklearn
from comet_ml import Experiment
from ift6758.data.milestone2.question_3 import roc_curve_and_auc_metrique, goal_rate_curve, goal_cumulative_proportion_curve, calibration_display_curve
import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


with open("API_KEY", "r") as f:
    API_KEY = f.readline()
exp = Experiment(
    api_key=API_KEY, # don’t hardcode!!
    project_name='milestone_2',
    workspace="genkishi"
)

__file__ = '/home/olivier/Documents/IFT6758/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features/'
data = pd.read_pickle(os.path.dirname(__file__) + "/data_for_models/data.pkl")

train_feature = ~data.columns.isin(['event_type_0', 'event_type_1'])
X = data.iloc[:,train_feature]
y = data.loc[:,["event_type_0"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

gridsearch_parameters = [
    (scale_pos_weight, max_depth, min_child_weight)
    for scale_pos_weight in range(1,8,2)
    for max_depth in range(4,9)
    for min_child_weight in range(4,9)
]

param = {'max_depth': 5, 'min_child_weight': 6, 'objective': 'binary:logistic', "scale_pos_weight" : 5}

gridsearch_results = pd.DataFrame()
for scale_pos_weight, max_depth, min_child_weight in gridsearch_parameters:
    param['max_depth'] = max_depth
    param["scale_pos_weight"] = scale_pos_weight
    param['min_child_weight'] = min_child_weight

    cv_results = xgb.cv(
        param,
        dtrain,
        seed=42,
        nfold=5,
        metrics={'auc'},
        early_stopping_rounds=10
    )
    best_auc = cv_results["test-auc-mean"].max()
    result_row = {'max_depth': [max_depth],
                  'min_child_weight': [min_child_weight],
                  "scale_pos_weight" : [scale_pos_weight],
                  "auc" : [best_auc]}
    result_row = pd.DataFrame(result_row)
    gridsearch_results = pd.concat([gridsearch_results, result_row])
    exp.log_metric("auc", best_auc)
    print(param.values())

best_params = gridsearch_results[gridsearch_results.auc == gridsearch_results.auc.max()]
param['max_depth'] = best_params.max_depth.values[0]
param["scale_pos_weight"] = best_params.scale_pos_weight.values[0]
param['min_child_weight'] = best_params.min_child_weight.values[0]
param["eval_metric"] = "auc"
evallist = [(dtest, 'eval'), (dtrain, 'train')]
clf_xgb = xgb.XGBClassifier(objective='binary:logistic',
                            missing=None,
                            seed=42,
                            scale_pos_weight = param["scale_pos_weight"],
                            max_depth=param['max_depth'],
                            min_child_weight = param["scale_pos_weight"])
clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric=param["eval_metric"],
            eval_set=[(X_test, y_test)])

proba = clf_xgb.predict_proba(X_test)
roc_curve_and_auc_metrique(proba, y_test, "Hyper_tune_XBoost")
goal_rate_curve(proba,y_test, "Hyper_tune_XBoost")
goal_cumulative_proportion_curve(proba, y_test, "Hyper_tune_XBoost")
calibration_display_curve(proba, y_test, "Hyper_tune_XBoost")
clf_xgb.save_model(os.path.dirname(__file__) + "/models/XGBoost_hyper_tuning/model.json")
exp.log_model("XGBoost_hyper_tuning", os.path.dirname(__file__) + "/models/XGBoost_hyper_tuning/")
plt.figure(1).savefig("/home/olivier/Documents/XGBoost_HT_roc_curve.png")
plt.figure(2).savefig("/home/olivier/Documents/XGBoost_HT_rate_curve.png")
plt.figure(3).savefig("/home/olivier/Documents/XGBoost_HT_goal_cumul.png")
plt.figure(4).savefig("/home/olivier/Documents/XGBoost_HT_calibration.png")