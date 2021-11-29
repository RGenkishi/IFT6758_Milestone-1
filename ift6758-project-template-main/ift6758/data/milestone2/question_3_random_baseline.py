from ift6758.data.milestone2.question_3 import *
from ift6758.data.milestone2.question_2 import Featurizer
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set()

ftz = Featurizer(2015, 2019)
features_df = ftz.get_feature()
print(features_df)
X = features_df[['Angle_from_net']]
print(X)
X.fillna(X.median(), inplace=True)
Y = features_df['is_goal']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30)
proba = np.random.uniform(0.0, 1.0, (Y_test.shape[0], 2))
roc_curve_and_auc_metrique(proba, Y_test)
goal_rate_curve(proba, Y_test, "model_1_random_baseline")
goal_cumulative_proportion_curve(proba, Y_test, "model_1_random_baseline")
calibration_display_curve(proba, Y_test)