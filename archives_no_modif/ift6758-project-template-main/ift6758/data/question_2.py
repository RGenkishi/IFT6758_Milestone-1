import os.path
from .api_requester import *

'''
test = requests.get(url="https://statsapi.web.nhl.com/api/v1/game/2017021272/feed/live")
test.status_code == 404
'''

databasePath = os.path.dirname(__file__)+"/database/"  # chemin par défaut pour l'enregistrement des données

class DataAquirer:

    def __init__(self, path=databasePath):
        self.path = path

    def get_all_games_data_for_a_year(self, year):

        if self.file_exists(year):
            self.download_existing_file(year)
        else:
            self.get_data_from_api(year)


    def file_exists(self, year):
        path = self.path + str(year) + "_season_data.json"
        return os.path.isfile(path)

    def download_existing_file(self, year):
        self.season_data = {}
        season_data_path = self.path + str(year) + "_season_data.json"
        with open(season_data_path, "r") as file:
            self.season_data = json.load(file)

        self.playoffs_data = {}
        playoffs_data_path = self.path + str(year) + "_playoffs_data.json"
        with open(playoffs_data_path, "r") as file:
            self.playoffs_data = json.load(file)

    def get_data_from_api(self, year):
        season_requester = ApiGameSeasonRequester("https://statsapi.web.nhl.com/api/v1/game/")
        playoff_requester = ApiGamePlayoffsRequester("https://statsapi.web.nhl.com/api/v1/game/")

        self.season_data = season_requester.get_data(year)
        self.playoffs_data = playoff_requester.get_data(year)
        self.save_data(year)

    def save_data(self, year):
        print("Saving")
        path_season_data = self.path + str(year) + "_season_data.json"
        print(path_season_data)
        with open(path_season_data, "w") as file:
            file.write(json.dumps(self.season_data))


        path_playoffs_data = self.path + str(year) + "_playoffs_data.json"
        with open(path_playoffs_data, "w") as file:
            file.write(json.dumps(self.playoffs_data))

