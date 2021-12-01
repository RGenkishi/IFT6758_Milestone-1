from ift6758.data.tidyDataKeys import *
from ift6758.data.tidyer import Tidyer
import matplotlib.pyplot as plt
from PIL import Image
import ipywidgets as widgets
from IPython.display import display

class debugWidget:

    def __init__(self):
        self.tdf = Tidyer()
        self.dfs = None
        self.df = None
        self.subDf = []


    def drawIceRink(self, i):
        print("Event Type : " + self.subDf.iloc[int(i)][EVENT_TYPE])
        print("Shot Type : " + self.subDf.iloc[int(i)][SHOT_TYPE])
        print("Coord : (x=" + str(self.subDf.iloc[int(i)][COORD_X]) + ", y=" + str(self.subDf.iloc[int(i)][COORD_Y]) + ")")
        try:
            print("Shooter : " + self.subDf.iloc[int(i)][SHOOTER_NAME])
        except:
            print("Shooter : ?")
        try:
            print("Goalie : " + self.subDf.iloc[int(i)][GOALIE_NAME])
        except:
            print("Goalie : ?")

        fig, ax = plt.subplots()
        img = Image.open('../../figures/nhl_rink.png')
        ax.imshow(img, extent=[-100, 100, -43, 43])
        # Add scatter point on the image.
        imgx, imgy = [float(self.subDf.iloc[int(i)][COORD_X])], [float(self.subDf.iloc[int(i)][COORD_Y])]
        ax.scatter(imgx, imgy, s=5, lw=5, facecolor="none", edgecolor="magenta")


    def selectMatch(self, m):
        self.subDf = self.df[self.df[GAME_ID] == m]
        # print(subDf)
        print("Date : "
              + str(self.subDf.iloc[0][DATE_YEAR])
              + '_' + str(self.subDf.iloc[0][DATE_MONTH])
              + '_' + str(self.subDf.iloc[0][DATE_DAY]))
        print("Team One : " + self.subDf[TEAM_NAME].drop_duplicates().iloc[0])
        print("Team Two : " + self.subDf[TEAM_NAME].drop_duplicates().iloc[1])
        lenDf = len(self.subDf)
        w = widgets.IntSlider(value=0, min=0, max=lenDf - 1, description='event:', continuous_update=False)
        interactive_IceRinkPlot = widgets.interactive(self.drawIceRink, i=w)
        display(interactive_IceRinkPlot)


    def selectGameType(self, t):
        self.df = self.dfs[t]
        gameIdList = self.df[GAME_ID].drop_duplicates()
        m = widgets.Dropdown(options=gameIdList, value=gameIdList[0], description='Match:', disabled=False)
        dropDownSelectMatch = widgets.interactive(self.selectMatch, m=m)
        display(dropDownSelectMatch)

    def selectYear(self, y):
        self.dfs = self.tdf.game_event_to_panda_df(y)
        t = widgets.Dropdown(options=self.dfs.keys(), value=list(self.dfs.keys())[0], description='GameType:', disabled=False)
        dropDownGameTypeSelect = widgets.interactive(self.selectGameType, t=t)
        display(dropDownGameTypeSelect)


    def lauchWidget(self):
        y = widgets.Dropdown(options=range(1917, 2021), value=2017, description='Year:', disabled=False)
        dropDownYearSelect = widgets.interactive(self.selectYear, y=y)
        display(dropDownYearSelect)