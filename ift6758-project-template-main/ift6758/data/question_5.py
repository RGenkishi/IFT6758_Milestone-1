from .question_4 import *
import matplotlib.pyplot as plt

def histo_shot(year):
    tdf = Tidyer()
    df = tdf.game_event_to_panda_df(2017)['regular']
    df = df.astype('str')

    '''
    x1 = df[SHOT_TYPE]
    x2 = df[df[EVENT_TYPE] == "Goal"][SHOT_TYPE]

    plt.hist([x1, x2], color=['lightslategray', 'goldenrod'], label=['nombre de shot', 'nombre de goal'], histtype='barstacked')
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(df[SHOT_TYPE].unique(), rotation=90)

    plt.title("Nombre de shot et de goal par type de shot")
    plt.xlabel("Types de shot")

    plt.legend()
    plt.show()
    '''

    goal = df[df[EVENT_TYPE] == "Goal"][SHOT_TYPE].value_counts().rename_axis('shottype').reset_index( name='counts')
    shot = df[df[EVENT_TYPE] == "Shot"][SHOT_TYPE].value_counts().rename_axis('shottype').reset_index(name='counts')

    plt.bar(shot['shottype'], shot['counts'], label="nombre de tirs", color='r')
    plt.bar(goal['shottype'], goal['counts'], label="nombre de buts", color='b')
    plt.plot()
    plt.xlabel("type de tirs")
    plt.ylabel("nombre de total de tirs et de buts")
    plt.title("Nombre de tirs et de buts par type de tirs pour la saison 2019")
    plt.show()