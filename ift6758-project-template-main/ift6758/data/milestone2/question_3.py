from sklearn.metrics import roc_curve, auc
from sklearn.calibration import CalibrationDisplay
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set()

'''
Fonction pour tracer la courbe ROC et calculer la metrique AUC
'''
def roc_curve_and_auc_metrique(proba, Y_test):
    fpr, tpr, _ = roc_curve(Y_test, proba[:, 1])
    roc_auc = auc(fpr, tpr)
    plt.figure()
    lw = 2
    plt.plot(
        fpr,
        tpr,
        color="darkorange",
        lw=lw,
        label="courbe ROC (air = %0.2f)" % roc_auc)
    plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Taux de Faux Positifs ")
    plt.ylabel("Taux de vrai Positifs ")
    plt.title("courbe Receiver operating characteristic ROC et metrique AUC ")
    plt.legend(loc="lower right")
    plt.show()


'''
Fonction pour tracer la courbe du taux de but 
en fonctiion du centile du modele de probabilite de tire 
'''
def goal_rate_curve(proba, Y_test, label):
    proba_df = pd.DataFrame(proba[:, 1], columns=['proba'])
    Y_test_df = pd.DataFrame(Y_test.to_numpy(), columns=['label'])
    label_proba_concate = pd.concat([Y_test_df, proba_df], axis=1)
    label_proba_concate = label_proba_concate.sort_values(by='proba')
    val = 95
    percent_arr = []
    goal_rate_arr = []
    goal_rate = 0
    while val >= 0:
        percent = np.percentile(label_proba_concate['proba'].to_numpy(), val)
        goal_percent = label_proba_concate['label'][label_proba_concate['proba'] >= percent]
        goal_rate = (goal_percent.sum() / goal_percent.count()) * 100
        percent_arr.append(val)
        goal_rate_arr.append(goal_rate)
        val -= 5
    # Goal rate figure
    plt.figure()
    plt.plot(percent_arr, goal_rate_arr, color="blue", label=label)
    plt.xlim([100, -5])
    plt.ylim([0, 100])
    plt.yticks(np.arange(0, 110, 10), ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
    plt.xticks(np.arange(0, 110, 10))
    plt.xlabel("shot probability model percentile")
    plt.ylabel("Goals/(Goals+rate)")
    plt.title("Taux de but ")
    plt.legend(loc="upper right")
    plt.show()


'''
Fonction pour tracer la courbe de la proportion cumulé de but 
en fonctiion du centile du modele de probabilite de tire
'''
def goal_cumulative_proportion_curve(proba, Y_test, label):
    proba_df = pd.DataFrame(proba[:, 1], columns=['proba'])
    Y_test_df = pd.DataFrame(Y_test.to_numpy(), columns=['label'])
    label_proba_concate = pd.concat([Y_test_df, proba_df], axis=1)
    label_proba_concate = label_proba_concate.sort_values(by='proba')
    val = 100
    percent_arr = []
    goal_prop_arr = []
    goal_prop = 0
    while val >= 0:
        percent = np.percentile(label_proba_concate['proba'].to_numpy(), val)
        goal_percent = label_proba_concate['label'][label_proba_concate['proba'] >= percent]
        goal_nb_all = label_proba_concate['label'][label_proba_concate['label'] == 1]
        goal_prop = (goal_percent.sum() / goal_nb_all.count()) * 100
        percent_arr.append(val)
        goal_prop_arr.append(goal_prop)
        val -= 5
    # Cumultive % of goal figure
    plt.figure()
    plt.plot(percent_arr, goal_prop_arr, color="blue", label=label)
    plt.xlim([100, 0])
    plt.ylim([0, 100])
    plt.yticks(np.arange(0, 110, 10), ['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
    plt.xticks(np.arange(0, 110, 10))
    plt.xlabel("shot probability model percentile")
    plt.ylabel("Goals cumulative proportion")
    plt.title("% cumulé de but")
    plt.legend(loc="upper left")
    plt.show()

'''
courbe du diagramme de fiabilité
'''
def calibration_display_curve(proba, Y_test):
    disp = CalibrationDisplay.from_predictions(Y_test, proba[:, 1])
    plt.show()
