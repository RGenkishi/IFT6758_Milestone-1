from .question_4 import *
import matplotlib.pyplot as plt

def histo_shot(year):
    tdf = Tidyfier()
    df = tdf.game_event_to_panda_df(2017)
    df = df.astype('str')

    x1 = df['shotSecondaryType']
    x2 = df[df.event == "Goal"]['shotSecondaryType']

    plt.hist([x1, x2], color=['lightslategray', 'goldenrod'], label=['nombre de shot', 'nombre de goal'], histtype='barstacked')
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(df['shotSecondaryType'].unique(), rotation=90)

    plt.title("Nombre de shot et de goal par type de shot")
    plt.xlabel("Types de shot")

    plt.legend()
    plt.show()