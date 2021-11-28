#Comet wants to be logged before I import xgboos and sklearn
from comet_ml import API
from comet_ml import Experiment
from ift6758.data.milestone2.question_3 import roc_curve_and_auc_metrique, goal_rate_curve, goal_cumulative_proportion_curve, calibration_display_curve
import pandas as pd
import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
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
param['max_depth'] = 7
param["scale_pos_weight"] = 7
param['min_child_weight'] = 7
param["eval_metric"] = "auc"

clf_xgb = xgb.XGBClassifier(objective='binary:logistic',
                            missing=None,
                            seed=42,
                            scale_pos_weight = param["scale_pos_weight"],
                            max_depth=param['max_depth'],
                            min_child_weight = param["scale_pos_weight"])

__file__ = '/home/olivier/Documents/IFT6758/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features/'
data = pd.read_pickle(os.path.dirname(__file__) + "/data_for_models/data.pkl")

slc = list(range(data.shape[1]))
slc.remove(16)
slc.remove(17)

##Mutual information
X = data.iloc[:,slc]
y = data.loc[:,["event_type_0"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
feature_scores = fs.mutual_info_classif(X_train, y_train, random_state=0)
best_features = []
for score, f_name in sorted(zip(feature_scores, X_train.columns), reverse=True)[:20]:
        print(f_name, score)
        best_features.append(f_name)

def cross_validation_on_best_features(best_features, X, y):
    mutual_information_results = pd.DataFrame()
    for i in range(1, (len(best_features)+1)):
        bf = best_features[:i]
        X = data.loc[:,bf]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
        dtrain = xgb.DMatrix(X_train, label=y_train)
        cv_results = xgb.cv(
            param,
            dtrain,
            seed=42,
            nfold=5,
            metrics={'auc'},
            early_stopping_rounds=10
        )
        best_auc = cv_results["test-auc-mean"].max()
        result_row = {"kbest_features" : [i],
                      "auc" : [best_auc]}
        result_row = pd.DataFrame(result_row)
        mutual_information_results = pd.concat([mutual_information_results, result_row])
        print(i)

clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric=param["eval_metric"],
            eval_set=[(X_test, y_test)])

##Select from model feature selection
X = data.iloc[:,slc]
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
X = data.loc[:,best_features]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)

clf_xgb.fit(X_train,
            y_train,
            verbose=True,
            early_stopping_rounds=10,
            eval_metric=param["eval_metric"],
            eval_set=[(X_test, y_test)])
