
from ift6758.data.question_4 import Tidyer
from ift6758.data.tidyDataKeys import *
from ift6758.data.question_6 import HeatMapShots
import pandas as pd
import numpy as np

x_net_coordinate = 10
heatmap_function = HeatMapShots()

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

    def compute_distance(self,x,y):
        dist = np.sqrt((x - 90)**2 + (y - 0)**2)
        return dist

    def calculate_distance_from_net(self,season_data):
        season_data = heatmap_function.rearange_coordinates(season_data)
        season_data['distance'] = np.sqrt(
            (season_data.coord_x - x_net_coordinate) ** 2 + season_data.coord_y ** 2)
        return season_data

    def calculate_angle(self,season_data):
        season_data["angle"] = np.arccos(
            (season_data.coord_x - x_net_coordinate) / season_data.distance_from_net)
        season_data.loc[season_data.coord_y < 0,"angle"] = -season_data.loc[season_data.coord_y < 0,"angle"]
        return season_data

    def get_feature(self):
        df = self.get_all_in_one(self.period_start, self.period_end)
        df['is_goal'] = df['is_goal'].astype(int)
        df = df.assign(distance = 0)
        df = df.assign(angle = 0)
        df = df.assign(filet_vide = 2 )
        feature_df = df[['is_goal','distance','angle','filet_vide']]
        #feature_df = self.calculate_distance_from_net(feature_df)
        #feature_df = self.calculate_angle(feature_df)

        '''i=0
        for x,y,side in zip(df['coord_x'],df['coord_y'],df['rink_side']):

            if side == 'left' and x >= 0 or side == 'right' and x<= 0:
                dist = self.compute_distance(x, y)
                feature_df['distance'].loc[i] = self.compute_distance(x, y)
                feature_df['angle'].loc[i] = np.degrees(np.arccos(self.compute_distance(90, y)/dist))
            else:
                feature_df['distance'].loc[i] = np.nan
            i +=1
        '''
        j = 0
        for goalie in df['goalie_name']:
            if goalie is np.nan:
                feature_df['filet_vide'].loc[j] = 0
            else:
                feature_df['filet_vide'].loc[j] = 1
            j+=1

        return feature_df