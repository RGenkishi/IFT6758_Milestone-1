import os.path
import json

from ift6758.data.api_requester import *
from ift6758.utilitaires.logger import *


# chemin pour l'enregistrement des données : dans le sous-dossier database du dossier contenant le module
databasePath = os.path.dirname(__file__)+"/database/"


class DataAquirer:

    def __init__(self, path=databasePath, verbose=True, logger=ConsoleLogger):
        self.logger = logger()
        self.path = path
        self.verbose = verbose
        self.season_data = {}
        self.playoffs_data = {}

    def log(self, *kwargs):
        if self.verbose:
            self.logger.log(kwargs)

    def get_all_games_data_for_a_year(self, year):
        if self.file_exists(year):
            self.download_existing_file(year)
        else:
            self.get_data_from_api(year)

    def file_exists(self, year):
        path = self.path + str(year) + "_season_data.json"
        return os.path.isfile(path)

    def download_existing_file(self, year):
        season_data_path = self.path + str(year) + "_season_data.json"
        with open(season_data_path, "r") as file:
            self.season_data = json.load(file)

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
        self.log("Saving")
        path_season_data = self.path + str(year) + "_season_data.json"
        print(path_season_data)
        with open(path_season_data, "w") as file:
            file.write(json.dumps(self.season_data))

        path_playoffs_data = self.path + str(year) + "_playoffs_data.json"
        with open(path_playoffs_data, "w") as file:
            file.write(json.dumps(self.playoffs_data))
