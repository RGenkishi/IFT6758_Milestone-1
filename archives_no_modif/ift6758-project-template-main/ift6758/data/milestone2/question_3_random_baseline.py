from ift6758.data.milestone2.question_3 import *
from ift6758.data.tidyDataKeys import *
import seaborn as sns
sns.set()

def random_baseline(features_df):
    Y = features_df[IS_GOAL]
    proba = np.random.uniform(0.0, 1.0, (Y.shape[0], 2))
    roc_curve_and_auc_metrique(proba, Y, "random_baseline")
    goal_rate_curve(proba, Y, "random_baseline")
    goal_cumulative_proportion_curve(proba, Y, "random_baseline")
    calibration_display_curve(proba, Y, "random_baseline")