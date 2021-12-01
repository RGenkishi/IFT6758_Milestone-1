from ift6758.data.question_4 import *
import matplotlib.pyplot as plt

def histo_shot(year):
    tdf = Tidyer()
    df = tdf.game_event_to_panda_df(year)['regular']
    df = df.astype('str')

    goal = df[df[EVENT_TYPE] == "Goal"][SHOT_TYPE].value_counts().rename_axis('shottype').reset_index( name='counts')
    shot = df[df[EVENT_TYPE] == "Shot"][SHOT_TYPE].value_counts().rename_axis('shottype').reset_index(name='counts')

    plt.rcParams['figure.figsize'] = [12, 8]
    plt.bar(shot['shottype'], shot['counts'], label="nombre de tirs", color='r')
    plt.bar(goal['shottype'], goal['counts'], label="nombre de buts", color='b')
    plt.plot()
    plt.xlabel("type de tirs")
    plt.ylabel("nombre de total de tirs et de buts")
    plt.title("Nombre de tirs et de buts par type de tirs pour la saison 2018", fontsize=16)
    plt.show()

    for i in range(len(shot['shottype'])):
        print(shot['shottype'][i], str(float(goal['counts'][i])*100 / float(shot['counts'][i])) + '%')

def calcDist(a, b):
    return np.sqrt(a**2+b**2)

def histo_distance():
    tdf = Tidyer()
    df18 = tdf.game_event_to_panda_df(2018)['regular']
    df18 = df18.astype('str')
    goal18 = df18[df18[EVENT_TYPE] == "Goal"]
    distances18 = []
    for i in goal18.index:
        if goal18[RINK_SIDE][i] == "right":
            distances18.append(calcDist(float(goal18[COORD_X][i]) + 100, float(goal18[COORD_Y][i])))
        else:
            distances18.append(calcDist(200 - (float(goal18[COORD_X][i]) + 100), float(goal18[COORD_X][i])))

    df19 = tdf.game_event_to_panda_df(2019)['regular']
    df19 = df19.astype('str')
    goal19 = df19[df19[EVENT_TYPE] == "Goal"]
    distances19 = []
    for i in goal19.index:
        if goal19[RINK_SIDE][i] == "right":
            distances19.append(calcDist(float(goal19[COORD_X][i]) + 100, float(goal19[COORD_Y][i])))
        else:
            distances19.append(calcDist(200 - (float(goal19[COORD_X][i]) + 100), float(goal19[COORD_X][i])))

    df20 = tdf.game_event_to_panda_df(2020)['regular']
    df20 = df20.astype('str')
    goal20 = df20[df20[EVENT_TYPE] == "Goal"]
    distances20 = []
    for i in goal20.index:
        if goal20[RINK_SIDE][i] == "right":
            distances20.append(calcDist(float(goal20[COORD_X][i]) + 100, float(goal20[COORD_Y][i])))
        else:
            distances20.append(calcDist(200 - (float(goal20[COORD_X][i]) + 100), float(goal20[COORD_X][i])))

    df21 = tdf.game_event_to_panda_df(2021)['regular']
    df21 = df21.astype('str')
    goal21 = df21[df21[EVENT_TYPE] == "Goal"]
    distances21 = []
    for i in goal21.index:
        if goal21[RINK_SIDE][i] == "right":
            distances21.append(calcDist(float(goal21[COORD_X][i]) + 100, float(goal21[COORD_Y][i])))
        else:
            distances21.append(calcDist(200 - (float(goal21[COORD_X][i]) + 100), float(goal21[COORD_X][i])))


    plt.hist(distances18, range=(0, 200), bins=100, label="2018", edgecolor='red', fc=(0, 0, 0, 0.01))
    plt.hist(distances19, range=(0, 200), bins=100, label="2019", edgecolor='blue', fc=(0, 0, 0, 0.01))
    plt.hist(distances20, range=(0, 200), bins=100, label="2020", edgecolor='green', fc=(0, 0, 0, 0.01))
    plt.hist(distances21, range=(0, 200), bins=100, label="2021", edgecolor='magenta', fc=(0, 0, 0, 0.01))
    plt.plot()
    plt.xlabel("Distance au centre du bord du terrain derrière les cages")
    plt.ylabel("nombre de buts")
    plt.title("Nombre de but en fonction de la distance", fontsize=16)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    #histo_distance()
    histo_shot(2019)