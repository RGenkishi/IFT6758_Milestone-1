from ift6758.data.question_4 import Tidyfier
import matplotlib.pyplot as plt
from PIL import Image
import ipywidgets as widgets
from IPython.display import display



class debugWidget:

    def __init__(self):
        self.tdf = Tidyfier()
        self.df = None
        self.subDf = []


    def drawIceRink(self, i):
        print("Event Type : " + self.subDf.iloc[int(i)]["event"])
        print("Shot Type : " + self.subDf.iloc[int(i)]["shotSecondaryType"])
        print("Coord : (x=" + str(self.subDf.iloc[int(i)]["coordX"]) + ", y=" + str(self.subDf.iloc[int(i)]["coordY"]) + ")")
        try:
            print("Shooter : " + self.subDf.iloc[int(i)]["shooterName"])
        except:
            print("Shooter : ?")
        try:
            print("Goalie : " + self.subDf.iloc[int(i)]["goalieName"])
        except:
            print("Goalie : ?")

        fig, ax = plt.subplots()
        img = Image.open('../../figures/nhl_rink.png')
        ax.imshow(img, extent=[-100, 100, -43, 43])
        # Add scatter point on the image.
        imgx, imgy = [float(self.subDf.iloc[int(i)]["coordX"])], [float(self.subDf.iloc[int(i)]["coordY"])]
        ax.scatter(imgx, imgy, s=5, lw=5, facecolor="none", edgecolor="magenta")


    def selectMatch(self, m):
        self.subDf = self.df[self.df["matchId"] == m]
        # print(subDf)
        print("Date : "
              + str(self.subDf.iloc[0]['dateYear'])
              + '_' + str(self.subDf.iloc[0]['dateMonth'])
              + '_' + str(self.subDf.iloc[0]['dateDay']))
        print("Team One : " + self.subDf["teamName"].drop_duplicates().iloc[0])
        print("Team Two : " + self.subDf["teamName"].drop_duplicates().iloc[1])
        lenDf = len(self.subDf)
        w = widgets.IntSlider(value=0, min=0, max=lenDf - 1, description='event:', continuous_update=False)
        interactive_IceRinkPlot = widgets.interactive(self.drawIceRink, i=w)
        display(interactive_IceRinkPlot)


    def selectYear(self, y):
        global df
        self.df = self.tdf.game_event_to_panda_df(y)
        matchIdList = self.df['matchId'].drop_duplicates()
        sliderSelectMatch = widgets.interactive(self.selectMatch, m=matchIdList)
        display(sliderSelectMatch)


    def lauchWidget(self):
        y = widgets.Dropdown(options=range(1917, 2021), value=2017, description='Year:', disabled=False)
        dropDownYearSelect = widgets.interactive(self.selectYear, y=y)
        display(dropDownYearSelect)