'''from comet_ml import Experiment
with open("API_KEY", "r") as f:
    API_KEY = f.readline()[:-1]
exp = Experiment(
    api_key=API_KEY, # don’t hardcode!!
    project_name='milestone_2',
    workspace="genkishi"
)'''

import numpy as np
import pandas as pd
from sklearn.calibration import CalibrationDisplay

from ift6758.data.milestone2.question_2 import Dataset
from ift6758.data.milestone2.Classifier import *
from ift6758.data.tidyDataKeys import *
from colorama import Fore, Style
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from joblib import dump, load


class Naming():
    def __init__(self):
        pass


def evaluate_log_reg_accuracy():
    dataset = Dataset()
    dataset.split_train_set(train_percentage=.8, shuffle=True, target=IS_GOAL)

    dataset.x_train = pd.DataFrame(dataset.x_train[DISTANCE_FROM_NET])
    dataset.x_train[np.isnan(dataset.x_train)] = 0

    dataset.x_valid = pd.DataFrame(dataset.x_valid[DISTANCE_FROM_NET])
    dataset.x_valid[np.isnan(dataset.x_valid)] = 0

    log_reg_clf = LogRegClf(dataset)
    log_reg_clf.train()

    prediction, accuracy = log_reg_clf.predict_accuracy_on_valid()
    nb_non_goal_pred = (1 - prediction).sum()
    nb_goal_pred = prediction.sum()
    print(f"predictions sur l'ensemble de validation: %s -- nb_0 : %s  -- nb_1 : %s"
          % (prediction, nb_non_goal_pred, nb_goal_pred))
    print(f"accuracy: {Fore.YELLOW}%s %%{Style.RESET_ALL}"
          % accuracy)
    print(f"Nombre de prédictions correctes: {Fore.CYAN}%s{Style.RESET_ALL}"
          % (prediction == dataset.y_valid).sum())
    print("Nombre total de prédiction:", prediction.shape)

    nb_non_goal = (1 - dataset.y_valid).sum()
    nb_goal = dataset.y_valid.sum()

    print(f"Nombre total de NON but: {Fore.CYAN}%s{Style.RESET_ALL}"
          % nb_non_goal)
    print("Nombre total de but", nb_goal)


def plot_roc_curves(y_true, y_probs, names, colors):
    """
    inspiré de https://www.delftstack.com/fr/howto/python/plot-roc-curve-python/
    fpr : false positive rate
    tpr : true positive rate
    """
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--', label='Random Baseline')

    for y_prob, name in zip(y_probs, names):
        if name == "Random Baseline":
            continue
        fpr, tpr, thresholds = roc_curve(y_true, y_prob)

        plt.plot(fpr, tpr, color=colors[name], label=f'{name} | auc = {auc(fpr, tpr):.3}')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic (ROC) Curve")
    plt.legend()
    plt.show()

def plot_goal_rate(y_true, y_probs, names, colors):
    _, ax = plt.subplots()

    for y_prob, name in zip(y_probs,names):
        if name == "Random Baseline":
            linestyle = '--'
        else:
            linestyle = '-'
        percentiles = np.fromiter((np.percentile(y_prob, n_percentile) for n_percentile in range(101)), dtype='float64')

        taux_iter = (y_true[(y_prob > centile)].sum() * 100 / y_true.shape[0] for centile in percentiles)
        taux = np.fromiter(taux_iter, dtype='float64')

        plt.plot([i for i in range(100, -1, -1)], taux, linestyle=linestyle, color=colors[name], label=name)
    plt.xlabel("Shot probability model percentile")
    plt.ylabel("#Goals / (#Shots + #Goals)")
    plt.title("Goal Rate")
    plt.ylim((0, 100))
    plt.xlim((100, 0))
    plt.legend()
    ax.yaxis.set_major_formatter(PercentFormatter())
    plt.show()


def plot_cumulative_goal_rate(y_true, y_probs, names, colors):
    _, ax = plt.subplots()

    for y_prob, name in zip(y_probs, names):
        if name == "Random Baseline":
            linestyle = '--'
        else:
            linestyle = '-'
        percentiles_iter = (np.percentile(y_prob, n_percentile) for n_percentile in range(101))
        percentiles = np.fromiter(percentiles_iter, dtype='float64')

        taux_iter = (y_true[y_prob < centile].sum() * 100 / y_true.sum() for centile in percentiles)
        taux = np.fromiter(taux_iter, dtype='float64')

        plt.plot([i for i in range(100, -1, -1)], taux, color=colors[name], linestyle=linestyle, label=name)
    plt.xlabel("Shot probability model percentile")
    plt.ylabel("#Goals / (#Shots + #Goals)")
    plt.title("LogReg Goal Rate")
    plt.ylim((0, 100))
    plt.xlim((100, 0))
    ax.yaxis.set_major_formatter(PercentFormatter())
    plt.legend()
    plt.show()


def plot_calibration(y_true, y_probs, names, colors, zoom=False):
    ref_line = True

    _, ax = plt.subplots()
    for y_prob, name in zip(y_probs, names):
        CalibrationDisplay.from_predictions(y_true=y_true, y_prob=y_prob, ref_line=ref_line, ax=ax, color=colors[name])
        prob_min, prob_max = y_prob.min(), y_prob.max()

        ref_line = False
    legende = ["Perfectly calibrated"]
    legende = legende + names
    plt.legend(legende)
    plt.xlabel("Mean predicted probability")
    plt.ylabel("Fraction of positives")
    if zoom:
        plt.ylim((0.05, 0.15))
        plt.xlim((0, 0.25))
    plt.title("Calibration") #\nprob_min = %s, prob_max = %s" % (prob_min, prob_max))
    plt.show()


def plot_four_plots():
    # dataset général utilisé pour récupérer et formater les données de base
    dataset = Dataset()
    dataset.split_train_set(train_percentage=.8, shuffle=True, target=IS_GOAL)

    # Distance seulement
    x_train_dist = pd.DataFrame(dataset.x_train[DISTANCE_FROM_NET])
    x_train_dist[np.isnan(x_train_dist)] = 0

    x_valid_dist = pd.DataFrame(dataset.x_valid[DISTANCE_FROM_NET])
    x_valid_dist[np.isnan(x_valid_dist)] = 0

    # Angle seulement
    x_train_angle = pd.DataFrame(dataset.x_train[ANGLE_FROM_NET])
    x_train_angle[np.isnan(x_train_angle)] = 0

    x_valid_angle = pd.DataFrame(dataset.x_valid[ANGLE_FROM_NET])
    x_valid_angle[np.isnan(x_valid_angle)] = 0

    # Distance et angle
    x_train_dist_angle = pd.concat([x_train_dist, x_train_angle], axis=1)
    x_valid_dist_angle = pd.concat([x_valid_dist, x_valid_angle], axis=1)


    datasets = {'dist': Dataset.new(x_train_dist, dataset.y_train, x_valid_dist, dataset.y_valid),
                'angle': Dataset.new(x_train_angle, dataset.y_train, x_valid_angle, dataset.y_valid),
                'dist_angle': Dataset.new(x_train_dist_angle, dataset.y_train, x_valid_dist_angle, dataset.y_valid)}

    log_reg_clfs = {feature: LogRegClf(datasets[feature]) for feature in datasets}
    log_reg_clfs['random'] = RandomClf(dataset)

    '''baseName = input("Saisir un nom pour l'enregistrement des modèles : ")
    dir = "models/"
    for feature in log_reg_clfs:
        dump(log_reg_clfs[feature], dir + baseName + "_" + feature+'.joblib')
        exp.log_model("log Reg (" + feature + ")", dir + baseName + "_" + feature+'.joblib')
    '''

    for log_reg in log_reg_clfs.values():
        log_reg.train()

    predict_proba_goal = [c_log_reg.predict_proba_on_valid()[:, 1] for c_log_reg in log_reg_clfs.values()]
    names = ["Random Baseline"] + ["Log Reg (" + feature + ")" for feature in datasets]
    colors = {'Random Baseline': 'navy',
              'Log Reg (dist)': 'darkorange',
              'Log Reg (angle)': 'darkgreen',
              'Log Reg (dist_angle)': 'darkmagenta'}

    plot_roc_curves(y_true=dataset.y_valid, y_probs=predict_proba_goal, names=names, colors=colors)

    plot_goal_rate(y_true=dataset.y_valid, y_probs=predict_proba_goal, names=names, colors=colors)

    plot_cumulative_goal_rate(y_true=dataset.y_valid, y_probs=predict_proba_goal, names=names, colors=colors)

    plot_calibration(y_true=dataset.y_valid, y_probs=predict_proba_goal, names=names, colors=colors)


if __name__ == "__main__":
    evaluate_log_reg_accuracy()
    plot_four_plots()

