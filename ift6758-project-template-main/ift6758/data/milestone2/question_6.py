from comet_ml import Experiment
import os
import pickle
import pandas as pd
import matplotlib as plt
pd.set_option("display.max_columns", 100)
from ift6758.data.milestone2.question_3 import *
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import power_transform
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import cross_val_score,cross_val_predict
import multiprocessing
cores = multiprocessing.cpu_count()

data = pd.read_pickle(os.path.dirname('/Users/macbook/Documents/GitHub/IFT6758_Milestone-1/ift6758-project-template-main/ift6758/features') + "/data_for_models/data.pkl")


'''
Les pretraitements
'''
train_feature = data.loc[:, ~data.columns.isin(['event_type_0', 'event_type_1'])]
Y_train_all = data["event_type_0"]

#normalisation
X_train_all = power_transform(train_feature)
''' 
les algorithmes d'apprentissage et validation croisée stratifiée
'''

def classifers(classifier, title):
    # exp = Experiment(
    #    api_key=os.environ.get('COMET_API_KEY'),  # ne pas coder en dur!
    #    project_name='milestone_2',
    #     workspace= 'genkishi',
    # )
    print('----------------- '+title+' ----------------------')
    proba = cross_val_predict(classifier, X_train_all, Y_train_all, cv=5, method='predict_proba')
    score = cross_val_score(classifier, X_train_all, Y_train_all, cv=5, scoring='f1')
    f1_accuracy = score.mean()
    auc_accuracy = roc_auc_score(Y_train_all, proba[:, 1])
    print(auc_accuracy)
    print(f1_accuracy)
    metrics = {"f1_accuracy": f1_accuracy,
               "auc_accuracy":auc_accuracy}
    pickle.dump(classifier, open(title+'.pkl', 'wb'))
    # exp.log_model(title, title+'.pkl')
    # exp.log_dataset_hash( X_train_all)
    # exp.log_metrics(metrics)
    roc_curve_and_auc_metrique(proba, Y_train_all, title)
    goal_rate_curve(proba, Y_train_all, title)
    goal_cumulative_proportion_curve(proba, Y_train_all, title)
    calibration_display_curve(proba, Y_train_all, title)

#DecisionTreeClassifier
des_tree = DecisionTreeClassifier(criterion = "gini",max_depth=10,min_samples_leaf=1)
des_tree_title = 'DecisionTreeClassifier'


#MLPClassifier
MLP = MLPClassifier(hidden_layer_sizes=(70, 70, 70),
                    activation='tanh',
                    solver='adam',
                    alpha=0.01, learning_rate='adaptive', max_iter=1000, early_stopping=True)
MLP_title = 'MLPClassifier'

#VotingClassifier
clf_vote = VotingClassifier(estimators=[
        ('MLP', MLP), # MLP
        ('Des_tree', des_tree), # Decision Tree
        ],voting='soft', n_jobs=cores)
clf_vote_title = 'VotingClassifier'


#choix du classifieur
classifers(des_tree, des_tree_title)
classifers(MLP, MLP_title)
classifers(clf_vote, clf_vote_title)
plt.show()