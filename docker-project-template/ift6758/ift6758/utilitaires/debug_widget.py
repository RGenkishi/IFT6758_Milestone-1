import matplotlib.pyplot as plt
import ipywidgets as widgets
from ift6758.data.tidyDataKeys import *
from ift6758.data.tidyer import Tidyer
from PIL import Image
from IPython.display import display


class DebugWidget:

    def __init__(self):
        self.tdf = Tidyer()
        self.dfs = None
        self.df = None
        self.sub_df = None

    def draw_ice_rink(self, i):
        print("Event Type : " + self.sub_df.iloc[int(i)][EVENT_TYPE])
        print("Shot Type : " + self.sub_df.iloc[int(i)][SHOT_TYPE])
        print("Coord : (x=" + str(self.sub_df.iloc[int(i)][COORD_X]) +
              ", y=" + str(self.sub_df.iloc[int(i)][COORD_Y]) + ")")
        try:
            print("Shooter : " + self.sub_df.iloc[int(i)][SHOOTER_NAME])
        except Exception:
            print("Shooter : ?")
        try:
            print("Goalie : " + self.sub_df.iloc[int(i)][GOALIE_NAME])
        except Exception:
            print("Goalie : ?")

        fig, ax = plt.subplots()
        img = Image.open('../../figures/nhl_rink.png')
        ax.imshow(img, extent=[-100, 100, -43, 43])
        # Add scatter point on the image.
        imgx, imgy = [float(self.sub_df.iloc[int(i)][COORD_X])], [float(self.sub_df.iloc[int(i)][COORD_Y])]
        ax.scatter(imgx, imgy, s=5, lw=5, facecolor="none", edgecolor="magenta")

    def select_match(self, m):
        self.sub_df = self.df[self.df[GAME_ID] == m]
        # print(subDf)
        print("Date : "
              + str(self.sub_df.iloc[0][DATE_YEAR])
              + '_' + str(self.sub_df.iloc[0][DATE_MONTH])
              + '_' + str(self.sub_df.iloc[0][DATE_DAY]))
        print("Team One : " + self.sub_df[TEAM_NAME].drop_duplicates().iloc[0])
        print("Team Two : " + self.sub_df[TEAM_NAME].drop_duplicates().iloc[1])
        len_df = len(self.sub_df)
        w = widgets.IntSlider(value=0, min=0, max=len_df - 1, description='event:', continuous_update=False)
        interactive_ice_rink_plot = widgets.interactive(self.draw_ice_rink, i=w)
        display(interactive_ice_rink_plot)

    def select_game_type(self, t):
        self.df = self.dfs[t]
        game_id_list = self.df[GAME_ID].drop_duplicates()
        m = widgets.Dropdown(options=game_id_list, value=game_id_list[0], description='Match:', disabled=False)
        drop_down_select_match = widgets.interactive(self.select_match, m=m)
        display(drop_down_select_match)

    def select_year(self, y):
        self.dfs = self.tdf.game_event_to_panda_df(y)
        t = widgets.Dropdown(options=self.dfs.keys(), value=list(self.dfs.keys())[0], description='GameType:',
                             disabled=False)
        drop_down_game_type_select = widgets.interactive(self.select_game_type, t=t)
        display(drop_down_game_type_select)

    def launch_widget(self):
        y = widgets.Dropdown(options=range(1917, 2021), value=2017, description='Year:', disabled=False)
        drop_down_year_select = widgets.interactive(self.select_year, y=y)
        display(drop_down_year_select)


if __name__ == "__main__":
    dw = DebugWidget()
    dw.launch_widget()