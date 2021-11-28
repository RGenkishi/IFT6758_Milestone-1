
from ift6758.data.question_4 import Tidyer
from ift6758.data.tidyDataKeys import *
from ift6758.data.question_6 import HeatMapShots
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.mode.chained_assignment = None
x_net_coordinate = 10

class Featurizer():

    def __init__(self,period_start,period_end):
        self.period_start = period_start
        self.period_end = period_end
        
    def get_all_in_one(self,period_start,period_end):
        tfd = Tidyer()
        for period in range(period_start,period_end):
            print("----------"+str(period)+"----------")
            dfs = tfd.game_event_to_panda_df(period)
            if period == self.period_start:
                df = dfs['regular']
            else:
                dfs = dfs['regular']
                df = pd.concat([df,dfs], ignore_index=True)
        return df

    def calculate_distance_from_net(self,season_data):
        season_data = HeatMapShots(2017).rearange_coordinates(season_data)
        season_data['Distance_from_net'] = np.sqrt(
            (season_data.coord_x - x_net_coordinate) ** 2 + season_data.coord_y ** 2)
        return season_data

    def calculate_angle(self,season_data):
        season_data["Angle_from_net"] = np.arccos(
            (season_data.coord_x - x_net_coordinate) / season_data.Distance_from_net)
        season_data.loc[season_data.coord_y < 0,"Angle_from_net"] = -season_data.loc[season_data.coord_y < 0,"Angle_from_net"]
        return season_data

    def get_feature(self):
        df = self.get_all_in_one(self.period_start, self.period_end)
        df['is_goal'] = df['is_goal'].astype(int)
        df = df.assign(Distance_from_net = 0)
        df = df.assign(Angle_from_net = 0)
        df = df.assign(Empty_net = 2 )
        feature_df = self.calculate_distance_from_net(df)
        feature_df = self.calculate_angle(feature_df)
        feature_df = feature_df[['is_goal', 'Distance_from_net', 'Angle_from_net', 'Empty_net']]
        j = 0
        for goalie in df['goalie_name']:
            if goalie is np.nan:
                feature_df['Empty_net'].loc[j] = 0
            else:
                feature_df['Empty_net'].loc[j] = 1
            j+=1

        return feature_df
