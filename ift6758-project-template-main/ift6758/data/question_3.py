from ift6758.data.question_4 import Tidyfier
import matplotlib as plt
from PIL import Image
import ipywidgets as widgets



class debugWidget:

    def __init__(self, year):
        tdf = Tidyfier()
        self.df = tdf.game_event_to_panda_df(year)

    df = df[df['dateYear'] == "2017"]
    df = df[df['dateMonth'] == "10"]
    df = df[df['dateDay'] == "04"]

    def f(m, checkWithNhlExemple, checkWithNhlExemple):
        global df
        fig,ax = plt.subplots()
        img = Image.open('../../figures/nhl_rink.png')
        ax.imshow(img, extent=[-100,100,-43,43])
        # Add scatter point on the image.
        imgx,imgy = [float(df.loc[m,"coordX"])], [float(df.loc[m,"coordY"])]
        ax.scatter(imgx,imgy,s=5,lw=5,facecolor="none",edgecolor="magenta")



pd.set_option("max_rows", None)
pd.set_option("max_columns", None)
print(df.head(5))
#print(df.info())
#print(df.loc[0,"period"])


interactive_plot = widgets.interactive(f, m=(0, len(df)-1), checkWithNhlExemple=(True, False))
output = interactive_plot.children[-1]
output.layout.height = '350px'
interactive_plot