import xgboost as xgb
import os
from ift6758.features.question_4 import *
from ift6758.data.milestone2.question_2 import *
from ift6758.data.milestone2.question_3_angle import *
from ift6758.data.milestone2.question_3_distance import *
from ift6758.data.milestone2.question_3_dist_ang import *
from ift6758.data.milestone2.question_3 import roc_curve_and_auc_metrique, goal_rate_curve, goal_cumulative_proportion_curve, calibration_display_curve
import matplotlib.pyplot as plt



#%%%%%%%%%%%%%%%%%%%%%%%%%%
### Logistic Regression ###
#%%%%%%%%%%%%%%%%%%%%%%%%%%
featurizer = Featurizer(2019,2020)
season_data = featurizer.get_feature()
angle_feature(season_data)
distance_feature(season_data)
angle_distance_feature(season_data)
plt.show()

playoff_data = featurizer.get_feature("playoff")
angle_feature(season_data)
distance_feature(season_data)
angle_distance_feature(season_data)
plt.show()


#%%%%%%%%%%%%%%
### XGBOOST ###
#%%%%%%%%%%%%%%


year = 2019
shots_and_goals, other_events = load_data(year)
season_data = prepare_data_for_feature_engineering(shots_and_goals, other_events)
season_data = engineer_features(season_data)
season_data.loc[season_data.change_in_shot_angle.isna(), "change_in_shot_angle"] = 0
for col in season_data.columns:
    median = np.median(season_data.loc[~season_data[col].isna(),col])
    season_data.loc[season_data[col].isna(),col] = median

__file__ = '/home/olivier/Documents/IFT6758/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features/'
clf_xgb = xgb.XGBClassifier()
clf_xgb.load_model(os.path.dirname(__file__) + "/models/XGBoost_hyper_tuning/model.json")

train_feature = ~data.columns.isin(['event_type_0', 'event_type_1'])
Y_train_all = data["event_type_0"]

X = season_data.iloc[:,train_feature]
y = season_data.loc[:,["event_type_0"]]

proba = clf_xgb.predict_proba(X)
roc_curve_and_auc_metrique(proba, y, "goal")
goal_rate_curve(proba,y, "goal")
goal_cumulative_proportion_curve(proba, y, "goal")
calibration_display_curve(proba, y, "goal")
plt.show()
