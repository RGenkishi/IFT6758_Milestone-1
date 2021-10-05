import json

from ift6758.data import *
from ift6758.data.api_requester import *
from ift6758.data.question_2 import *
from ift6758.data.question_4 import Tidyfier

def test_question4():
    tdf = Tidyfier()
    df = tdf.game_event_to_panda_df(2017)

    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)
    print(df.head(10))

test_question4()
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