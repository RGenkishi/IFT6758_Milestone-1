import xgboost as xgb
from ift6758.data.milestone2.question_4 import *
from ift6758.data.milestone2.question_2 import *
from ift6758.data.milestone2.question_3_angle import *
from ift6758.data.milestone2.question_3_distance import *
from ift6758.data.milestone2.question_3_dist_ang import *
from ift6758.data.milestone2.question_3 import roc_curve_and_auc_metrique, goal_rate_curve, goal_cumulative_proportion_curve, calibration_display_curve
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import power_transform




def create_comparing_graphs(season_type):
    #%%%%%%%%%%%%%%%%%%%%%%%%%%
    ### Logistic Regression ###
    #%%%%%%%%%%%%%%%%%%%%%%%%%%

    featurizer = Featurizer(2019,2020)
    season_data = featurizer.get_feature()
    angle_feature(season_data)
    distance_feature(season_data)
    angle_distance_feature(season_data)
    plt.show()

    playoff_data = featurizer.get_feature(season_type=season_type)
    angle_feature(season_data)
    distance_feature(season_data)
    angle_distance_feature(season_data)



    #%%%%%%%%%%%%%%
    ### XGBOOST ###
    #%%%%%%%%%%%%%%


    year = 2019
    shots_and_goals, other_events = load_data(year)
    season_data = prepare_data_for_feature_engineering(shots_and_goals, other_events, season_type)
    season_data = engineer_features(season_data)
    season_data.loc[season_data.change_in_shot_angle.isna(), "change_in_shot_angle"] = 0
    for col in season_data.columns:
        median = np.median(season_data.loc[~season_data[col].isna(),col])
        season_data.loc[season_data[col].isna(),col] = median

    __file__ = '/ift6758/features/'
    clf_xgb = xgb.XGBClassifier()
    clf_xgb.load_model(os.path.dirname(__file__) + "/models/XGBoost_hyper_tuning/model.json")

    train_feature = ~season_data.columns.isin(['event_type_0', 'event_type_1', 'which_period_5', 'which_period_6', 'which_period_7'])

    X = season_data.iloc[:,train_feature]
    y = season_data.loc[:,["event_type_0"]]

    proba = clf_xgb.predict_proba(X)
    roc_curve_and_auc_metrique(proba, y, "XGBoost")
    goal_rate_curve(proba,y, "XGBoost")
    goal_cumulative_proportion_curve(proba, y, "XGBoost")
    calibration_display_curve(proba, y, "XGBoost")


    ### MLP Classifier ###

    #MLPClassifier

    train_feature = season_data.loc[:, ~season_data.columns.isin(['event_type_0', 'event_type_1'])]
    Y_train_all = season_data["event_type_0"]

    #normalisation
    X_train_all = power_transform(train_feature)
    classifier = MLPClassifier(hidden_layer_sizes=(70, 70, 70), #(70, 70, 70)
                        activation='tanh',
                        solver='adam',
                        alpha=0.01, learning_rate='adaptive', max_iter=1000, early_stopping=True)
    title = 'MLPClassifier'
    proba = cross_val_predict(classifier, X_train_all, Y_train_all, cv=5, method='predict_proba')
    roc_curve_and_auc_metrique(proba, y, title)
    goal_rate_curve(proba, y, title)
    goal_cumulative_proportion_curve(proba, y, title)
    calibration_display_curve(proba, y, title)

    ### Saving plots ###
    plt.figure(1).savefig("/home/olivier/Documents/" + season_type + "_roc_curve.png")
    plt.figure(2).savefig("/home/olivier/Documents/" + season_type + "_rate_curve.png")
    plt.figure(3).savefig("/home/olivier/Documents/" + season_type + "_goal_cumul.png")
    plt.figure(4).savefig("/home/olivier/Documents/" + season_type + "_calibration.png")

create_comparing_graphs("regular")
create_comparing_graphs("playoff")

