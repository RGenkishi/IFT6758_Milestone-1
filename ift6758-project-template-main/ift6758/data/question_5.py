from .question_4 import *
import matplotlib.pyplot as plt

def histo_shot(year):
    tdf = Tidyer()
    df = tdf.game_event_to_panda_df(2017)['regular']
    df = df.astype('str')

    goal = df[df[EVENT_TYPE] == "Goal"][SHOT_TYPE].value_counts().rename_axis('shottype').reset_index( name='counts')
    shot = df[df[EVENT_TYPE] == "Shot"][SHOT_TYPE].value_counts().rename_axis('shottype').reset_index(name='counts')

    plt.rcParams['figure.figsize'] = [12, 8]
    plt.bar(shot['shottype'], shot['counts'], label="nombre de tirs", color='r')
    plt.bar(goal['shottype'], goal['counts'], label="nombre de buts", color='b')
    plt.plot()
    plt.xlabel("type de tirs")
    plt.ylabel("nombre de total de tirs et de buts")
    plt.title("Nombre de tirs et de buts par type de tirs pour la saison 2019", fontsize=16)
    plt.show()