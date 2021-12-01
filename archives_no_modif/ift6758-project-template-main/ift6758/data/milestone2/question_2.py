# Comet wants to be logged before I import xgboos and sklearn
'''from comet_ml import Experiment
with open("API_KEY", "r") as f:
    API_KEY = f.readline()[:-1]
exp = Experiment(
    api_key=API_KEY, # don’t hardcode!!
    project_name='milestone_2',
    workspace="genkishi"
)'''

import matplotlib.pyplot as plt

from ift6758.data.question_4 import Tidyer
from ift6758.data.question_6 import HeatMapShots
from ift6758.data.tidyDataKeys import *
import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None
x_net_coordinate = 10


class Featurizer():

    def __init__(self, period_start, period_end):
        self.period_start = period_start
        self.period_end = period_end

    def get_all_in_one(self, period_start, period_end):
        tfd = Tidyer()
        for period in range(period_start, period_end + 1):
            print("----------" + str(period) + "----------")
            dfs = tfd.game_event_to_panda_df(period)
            if period == self.period_start:
                df = dfs['regular']
            else:
                dfs = dfs['regular']
                df = pd.concat([df, dfs], ignore_index=True)
        return df

    def calculate_distance_from_net(self, season_data):
        season_data = HeatMapShots(2017).rearange_coordinates(season_data)
        season_data[DISTANCE_FROM_NET] = np.sqrt(
            (season_data.coord_x - x_net_coordinate) ** 2 + season_data.coord_y ** 2)
        return season_data

    def calculate_angle(self, season_data):
        season_data[ANGLE_FROM_NET] = np.arccos(
            (season_data.coord_x - x_net_coordinate) / season_data[DISTANCE_FROM_NET])
        season_data.loc[season_data.coord_y < 0, ANGLE_FROM_NET] = -season_data.loc[
            season_data.coord_y < 0, ANGLE_FROM_NET]
        return season_data

    def get_feature(self):
        df = self.get_all_in_one(self.period_start, self.period_end)
        df[IS_GOAL] = df[IS_GOAL].astype(int)
        df = df.assign(distance_from_net=0)
        df = df.assign(angle_from_net=0)
        df = df.assign(empty_net=2)
        feature_df = self.calculate_distance_from_net(df)
        feature_df = self.calculate_angle(feature_df)
        feature_df.loc[:, EMPTY_NET] = df.goalie_name.isna()

        return feature_df


class Dataset():
    def __init__(self, train_start=2015, train_end=2018, test_start=2019, test_end=2019, constructor_override=False):
        if constructor_override:
            self.all_train = None
            self.all_test = None
        else:
            self.all_train = Featurizer(train_start, train_end).get_feature()  # Données d'entraînement complètes
            self.all_test = Featurizer(test_start, test_end).get_feature()  # Données de test complètes
        self.x_train = None  # Données d'entraînement réservées à l'entraînement effectif du modèle
        self.y_train = None  # Labels de x_train
        self.x_valid = None  # Données d'entraînement réservées à la validation du modèle
        self.y_valid = None  # Labels de x_valid
        self.x_test = None
        self.y_test = None

    @classmethod
    def new(cls, x_train, y_train, x_valid, y_valid):
        new_dataset = Dataset(constructor_override=True)

        new_dataset.x_train = x_train
        new_dataset.y_train = y_train
        new_dataset.x_valid = x_valid
        new_dataset.y_valid = y_valid

        return new_dataset

    def split_train_set(self, train_percentage=.8, shuffle=True, target=IS_GOAL):
        all_train = self.all_train.sample(frac=1) if shuffle else self.all_train

        train = all_train[:int(train_percentage * all_train.shape[0])]
        self.x_train = train.drop(target, axis=1)
        self.y_train = train[target]

        valid = all_train[int(train_percentage * all_train.shape[0]):]
        self.x_valid = valid.drop(target, axis=1)
        self.y_valid = valid[target]


if __name__ == "__main__":
    import seaborn as sns

    dataset = Dataset(train_start=2015, train_end=2018, test_start=2019, test_end=2019)

    features_df = dataset.all_train
    print(features_df)
    plt.figure()
    '''nombre de tire(but et tire separe) regrouper par distance'''
    dis1 = sns.displot(features_df, x=DISTANCE_FROM_NET, col=IS_GOAL)
    dis1.fig.suptitle('Nombre de tirs regroupés par distance')

    '''nombre de tire(but et tire separe) regrouper par angle'''
    dis2 = sns.displot(features_df, x=ANGLE_FROM_NET, col=IS_GOAL)
    dis2.fig.suptitle('Nombre de tirs regroupés par angle')

    '''Histograme 2D '''
    sns.jointplot(data=features_df, x=DISTANCE_FROM_NET, y=ANGLE_FROM_NET, hue=IS_GOAL)

    features_by_goal = features_df[features_df[IS_GOAL] == 1]
    features_by_non_goal = features_df[features_df[IS_GOAL] == 0]
    sns.jointplot(data=features_by_goal, x=DISTANCE_FROM_NET, y=ANGLE_FROM_NET, hue=IS_GOAL,
                  palette={1: 'tab:orange'})
    sns.jointplot(data=features_by_non_goal, x=DISTANCE_FROM_NET, y=ANGLE_FROM_NET, hue=IS_GOAL,
                  palette={0: 'tab:blue'})

    '''goal rate by distance'''
    features_df.sort_values(by=DISTANCE_FROM_NET, inplace=True)
    features_df['distance_binned'] = pd.cut(features_df[DISTANCE_FROM_NET], 10)
    goal = features_df[[IS_GOAL, 'distance_binned']].groupby(by=["distance_binned"]).sum()
    goal_shot = features_df[[IS_GOAL, 'distance_binned']].groupby(by=["distance_binned"]).count()
    goal_rate_distance = goal / goal_shot
    goal_rate_distance = goal_rate_distance.reset_index()
    goal_rate_distance['distance_binned'] = goal_rate_distance.distance_binned.astype(str)
    goal_rate_distance.plot.bar(x='distance_binned',
                                y=IS_GOAL,
                                xlabel='binned distance',
                                legend=False,
                                figsize=(8, 7),
                                ylabel='Goal rate',
                                title='goal rate by distance', rot=20, fontsize=8)

    '''goal rate by angle'''
    features_df['angle_binned'] = pd.cut(features_df[ANGLE_FROM_NET], 10)
    goal = features_df[[IS_GOAL, 'angle_binned']].groupby(by=["angle_binned"]).sum()
    goal_shot = features_df[[IS_GOAL, 'angle_binned']].groupby(by=["angle_binned"]).count()
    goal_rate_distance = goal / goal_shot
    goal_rate_distance = goal_rate_distance.reset_index()
    goal_rate_distance['angle_binned'] = goal_rate_distance.angle_binned.astype(str)
    goal_rate_distance.plot.bar(x='angle_binned',
                                y=IS_GOAL,
                                xlabel='binned angle',
                                legend=False,
                                figsize=(8, 7),
                                ylabel='Goal rate',
                                title='goal rate by angle', rot=20, fontsize=8)



    ''' histograme de but par filet vide et non vide '''
    dis3 = sns.displot(features_by_goal, x=DISTANCE_FROM_NET, hue=EMPTY_NET)
    dis3.fig.suptitle('Nombre de buts par filet vide et non vide')
    plt.show()

    features_by_goal_defense_zone = features_by_goal[features_by_goal[DISTANCE_FROM_NET] > 150]
    print(features_by_goal_defense_zone[[GAME_ID, GAME_TIME, PERIOD_TIME, PERIOD_WHICH, TEAM_NAME, COORD_X, COORD_Y, DISTANCE_FROM_NET]].head(10))
