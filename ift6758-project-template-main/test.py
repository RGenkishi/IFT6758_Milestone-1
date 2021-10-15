import json

import pandas as pd

from ift6758.data import *
from ift6758.data.api_requester import *
from ift6758.data.question_2 import *
#from ift6758.data.question_3 import Tidyer
from ift6758.data.question_4 import Tidyer
from ift6758.data.question_5 import *
from PIL import Image
import ipywidgets as widgets
import json
import math

from ift6758.data import *
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pointbiserialr

def test_question4():
    tdf = Tidyer()
    dfs = tdf.game_event_to_panda_df(2019)
    df1 = dfs['regular']
    df2 = dfs['playoff']
    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)
    print("REGULAR :")
    print(df1.head(10))
    print("\n PLAYOFF :")
    print(df2.head(10))
    print(df1.info())

def test_question5():
    histo_shot(2018)


def test_question3():
    tdf = Tidyer()
    df = tdf.game_event_to_panda_df(2017)

    df = df[df['dateYear'] == "2017"]
    df = df[df['dateMonth'] == "10"]
    df = df[df['dateDay'] == "04"]
    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)
    print(df)
    print(df.info())



#df = pd.read_json("ift6758/data/database/2017_season_data.json")
#df.info()

test_question4()



'''
pd.set_option("display.max_columns", 100)

data_acquirer = DataAquirer()
data_acquirer.get_all_games_data_for_a_year(2017)
playoffs_raw_data = data_acquirer.playoffs_data

tidyer = Tidyer()
playoffs_tidy_data = tidyer.tidy_data(playoffs_raw_data)
shots_count_per_shot_type = playoffs_tidy_data.groupby("shot_type").size().reset_index(name='counts')
goals_count_per_shot_type = playoffs_tidy_data[playoffs_tidy_data.is_goal].groupby("shot_type").size().reset_index(name='counts')

plt.bar(x=shots_count_per_shot_type.shot_type, height=shots_count_per_shot_type.counts)
plt.bar(x=goals_count_per_shot_type.shot_type, height=goals_count_per_shot_type.counts, color="red")
plt.xticks(rotation=45)
plt.show()

goalie_x_coord = 89
goalie_y_coord = 0

def calculate_distance(df):
    x = df["x_coordinate"]
    y = df["y_coordinate"]
    return math.sqrt((goalie_x_coord - abs(x))**2 + (goalie_y_coord - abs(y))**2)

playoffs_tidy_data["distance_from_net"] = playoffs_tidy_data.apply(calculate_distance, axis=1)

pointbiserialr(playoffs_tidy_data.is_goal, playoffs_tidy_data.distance_from_net)


season_data = data_acquirer.season_data
season_data= tidyer.tidy_data(season_data)

coordinate_is_missing = pd.isna(season_data.x_coordinate)
shot_type_is_missing = pd.isna(season_data.shot_type)

season_data = season_data[~(coordinate_is_missing | shot_type_is_missing)]

season_data["distance_from_net"] = list(season_data.apply(calculate_distance, axis=1))

pointbiserialr(season_data.is_goal, season_data.distance_from_net)

for shot_type in season_data.shot_type.drop_duplicates():
    shot_type_data = season_data[season_data.shot_type == shot_type]
    pb_test = pointbiserialr(shot_type_data.is_goal, shot_type_data.distance_from_net)
    print("shot type : " + shot_type + " correlation : " + str(pb_test.correlation))
'''

'''
import requests
response = requests.get(url=("https://statsapi.web.nhl.com/api/v1/game/" + str(2017) + "02" + str(1).zfill(4) +"/feed/live"))
with open(databasePath+"/file.json", 'w') as file:
    file.write(json.dumps(response.json()))
print(response.json())
'''

'''
data_acquirer = DataAquirer()
data_acquirer.get_all_games_data_for_a_year(2017)

print(data_acquirer.season_data)
'''


'''
data_acquirer2 = DataAquirer("/home/olivier/")
data_acquirer2.get_all_games_data_for_a_year(2017)
with open("/home/olivier/season_data.json", "w") as file:
    for game in data_acquirer.season_data:
        file.write(str(game))
        file.write("\n")
reloading_data = []
with open("/home/olivier/season_data.json", "r") as file:
    for line in file:
        reloading_data.append(eval(line))
api_requester = ApiRequester("https://statsapi.web.nhl.com/api/v1/game/")
test = api_requester.get_playoffs_data("2017")

import os.path
os.path.isfile("/home/olivier/2017_season_data.json")
'''
