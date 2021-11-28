#Comet wants to be logged before I import xgboos and sklearn
from comet_ml import Experiment
with open("API_KEY", "r") as f:
    API_KEY = f.readline()
exp = Experiment(
    api_key=API_KEY, # don’t hardcode!!
    project_name='milestone_2',
    workspace="genkishi"
)
from ift6758.data.milestone2.question_3 import roc_curve_and_auc_metrique, goal_rate_curve, goal_cumulative_proportion_curve
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


#__file__ = '/home/olivier/Documents/IFT6758/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features/'
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
            eval_metric="aucpr",
            eval_set=[(X_test, y_test)])
proba = clf_xgb.predict_proba(X_test)
roc_curve_and_auc_metrique(proba, y_test)
goal_rate_curve(proba,y_test, "goal")
goal_cumulative_proportion_curve(proba, y_test)
acc = accuracy_score(y_test,clf_xgb.predict(X_test))
prec = precision_score(y_test,clf_xgb.predict(X_test))
recall = recall_score(y_test,clf_xgb.predict(X_test))
clf_xgb.save_model(os.path.dirname(__file__) + "/models/XGBoost_base_model/base_model.json")

proba_prediction = pd.DataFrame(clf_xgb.predict_proba(X_test))
proba_prediction = proba_prediction.iloc[:,1]
roc_auc_score(y_test, proba_prediction)
fpr, tpr, _ = roc_curve(y_test,proba_prediction)
roc_auc = auc(fpr, tpr)
plt.figure()
lw = 2
plt.plot(
    fpr,
    tpr,
    color="darkorange",
    lw=lw,
    label="ROC curve (area = %0.2f)" % roc_auc,
)
plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Receiver operating characteristic example")
plt.legend(loc="lower right")
plt.show()

exp.log_model("XGBoost_base_model", os.path.dirname(__file__) + "/models/XGBoost_base_model/")
exp.log_metrics({"accuracy": acc, "precision": prec, "recall": recall})
slc = list(range(data.shape[1]))
slc.remove(16)
slc.remove(17)
X = data.iloc[:,slc]

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