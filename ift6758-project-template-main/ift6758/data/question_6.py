
from ift6758.data import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
from ift6758.data.question_2 import DataAquirer
from ift6758.data.question_4 import Tidyer
from ift6758.data.tidyDataKeys import *

pd.set_option("display.max_columns", None)

class HeatMapShots:

    def __init__(self, year):
        self.year = year
        tidyer = Tidyer()
        dfs = tidyer.game_event_to_panda_df(year)
        self.season_data = dfs['regular']
        self.playoffs_data = dfs['playoff']

    def prepare_data(self):
        self.season_data = self.rearange_coordinates(self.season_data)
        self.playoffs_data = self.rearange_coordinates(self.playoffs_data)
        self.season_data = self.divise_rink(self.season_data)
        self.playoffs_data = self.divise_rink(self.playoffs_data)
        self.counts_for_season = self.get_count_per_season(self.season_data)
        self.counts_for_playoffs = self.get_count_per_season(self.playoffs_data)

    def rearange_coordinates(self, tidy_data):
        right_side_x_coordinates = tidy_data[tidy_data.rink_side == "right"][COORD_X]
        tidy_data.loc[tidy_data.rink_side == "right", COORD_X] = right_side_x_coordinates - (2 * right_side_x_coordinates)

        shot_from_own_zone = tidy_data[(tidy_data.rink_side == "right") & (tidy_data[COORD_X] < 0)][COORD_X]
        shot_from_own_zone = shot_from_own_zone - (2 * shot_from_own_zone) + 100

        tidy_data.loc[(tidy_data.rink_side == "right") & (tidy_data[COORD_X] < 0), COORD_X] = shot_from_own_zone

        shot_from_own_zone = tidy_data[(tidy_data.rink_side == "left") & (tidy_data[COORD_X] < 0)][COORD_X]
        shot_from_own_zone = shot_from_own_zone - (2 * shot_from_own_zone) + 100

        tidy_data.loc[(tidy_data.rink_side == "left") & (tidy_data[COORD_X] < 0), COORD_X] = shot_from_own_zone

        no_rink_side_x_coordinate = tidy_data.loc[pd.isna(tidy_data.rink_side) & (tidy_data[COORD_X] < 0), COORD_X]
        tidy_data.loc[pd.isna(tidy_data.rink_side) & (tidy_data[COORD_X] < 0), COORD_X] = -no_rink_side_x_coordinate

        return tidy_data


    def divise_rink(self, tidy_data):
        tidy_data["x_case"] = tidy_data[COORD_X] // 20
        tidy_data["y_case"] = (tidy_data[COORD_Y] + 42.5) // 17
        return tidy_data

    def get_count_per_season(self, tidy_data):
        number_of_games = tidy_data.game_id.drop_duplicates().shape[0]
        counts_per_case = tidy_data.groupby(["x_case", "y_case"]).size().unstack(fill_value=0).stack().reset_index(name="counts")
        counts_per_case.groupby(["x_case", "y_case"]).sum("counts").reset_index()
        counts_per_case["counts_per_hour"] = counts_per_case.counts / (number_of_games * 2)
        return counts_per_case

    def get_count_for_team(self, tidy_data):
        number_of_games = tidy_data.game_id.drop_duplicates().shape[0]
        counts_per_case = tidy_data.groupby(["x_case", "y_case"]).size().unstack(fill_value=0).stack().reset_index(name="counts")
        counts_per_case.groupby(["x_case", "y_case"]).sum("counts").reset_index()
        counts_per_case["counts_per_hour"] = counts_per_case.counts / number_of_games
        return counts_per_case

    def get_above_average_for_team(self, team):
        team_data = self.season_data[self.season_data[TEAM_NAME] == team]
        team_data = self.get_count_for_team(team_data)
        team_data.counts_per_hour = team_data.counts_per_hour - self.counts_for_season.counts_per_hour
        return (team_data)

    def plot_heat_map(self, team):

        team_average_difference = heatmaper.get_above_average_for_team(team)
        team_average_difference = round(team_average_difference, 2)
        img = mpimg.imread('./figures/nhl_rink.png')
        matrix_for_heatmap = np.array(team_average_difference.counts_per_hour).reshape((10, 5))

        ## Inspiré par https://stackoverflow.com/questions/50091591/plotting-seaborn-heatmap-on-top-of-a-background-picture
        hmax = sns.heatmap(np.transpose(matrix_for_heatmap),
                           alpha=0.5,  # whole heatmap is translucent
                           annot=True,
                           zorder=2,
                           vmin=-1.0,
                           vmax=1.0,
                           cmap="vlag")

        # heatmap uses pcolormesh instead of imshow, so we can't pass through
        # extent as a kwarg, so we can't mmatch the heatmap to the map. Instead,
        # match the map to the heatmap:

        hmax.imshow(img,
                    aspect=hmax.get_aspect(),
                    extent=hmax.get_xlim() + hmax.get_ylim(),
                    zorder=1)  # put the map under the heatmap
        hmax.set_title("Nombre de tirs au dessus de la moyenne\n" + team + " saison " + str(self.year) + "-" + str(self.year + 1))
        plt.show()


