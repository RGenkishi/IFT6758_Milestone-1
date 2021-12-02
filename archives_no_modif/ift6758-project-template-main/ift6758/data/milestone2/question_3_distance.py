from comet_ml import Experiment
import pickle
import os
from ift6758.data.milestone2.question_3 import *
from ift6758.data.tidyDataKeys import *
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import seaborn as sns
sns.set()


def distance_feature(features_df):
    # exp = Experiment(
    #    api_key=os.environ.get('COMET_API_KEY'),  # ne pas coder en dur!
    #    project_name='milestone_2',
    #     workspace= 'genkishi',
    # )
    X = features_df[[DISTANCE_FROM_NET]]
    X.fillna(X.median(), inplace=True)
    Y = features_df[IS_GOAL]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30)
    X_train = X_train.to_numpy().reshape(-1, 1)
    X_test = X_test.to_numpy().reshape(-1, 1)
    log_reg = LogisticRegression()
    log_reg.fit(X_train, Y_train)
    proba = log_reg.predict_proba(X_test)
    accuracy = accuracy_score(Y_test, log_reg.predict(X_test))
    print(accuracy)
    metrics = {"accuracy": accuracy}
    # pickle.dump(log_reg, open('log-reg_distance.pkl', 'wb'))
    # exp.log_model("log-reg_distance", "log-reg_distance.pkl")
    # exp.log_dataset_hash(X_train)
    # exp.log_metrics(metrics)
    # tracage de courbe
    roc_curve_and_auc_metrique(proba, Y_test, "log-reg_distance")
    goal_rate_curve(proba, Y_test, "log-reg_distance")
    goal_cumulative_proportion_curve(proba, Y_test, "log-reg_distance")
    calibration_display_curve(proba, Y_test, "log-reg_distance")