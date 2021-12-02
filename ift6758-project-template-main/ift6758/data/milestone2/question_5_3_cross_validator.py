import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split

class CrossValidator:
    def __init__(self, data, param):
        self.data = data
        self.param = param

    def cross_validation_on_best_features(self, best_features, X, y, experiment, type_feature_selection):
        feature_selection_results = pd.DataFrame()
        for i in range(1, (len(best_features)+1)):
            bf = best_features[:i]
            X = self.data.loc[:,bf]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
            dtrain = xgb.DMatrix(X_train, label=y_train)
            cv_results = xgb.cv(
                self.param,
                dtrain,
                seed=42,
                nfold=5,
                metrics={'auc'},
                early_stopping_rounds=10
            )
            best_auc = cv_results["test-auc-mean"].max()
            experiment.log_metric(("auc_" + type_feature_selection), best_auc)
            result_row = {"kbest_features" : [i],
                          "auc" : [best_auc]}
            result_row = pd.DataFrame(result_row)
            feature_selection_results = pd.concat([feature_selection_results, result_row])
            print(i)
        return feature_selection_results