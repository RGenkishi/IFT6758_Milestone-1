import time
import requests

from abc import abstractmethod

try:
    from ift6758.utilitaires.logger import ConsoleLogger
except:
    from ift6758.ift6758.utilitaires.logger import ConsoleLogger


class ApiRequester:
    def __init__(self, api_url, logger=ConsoleLogger):
        self.logger = logger()
        self.season_type = None
        self.api_url = api_url

    @abstractmethod
    def get_data(self, year):
        pass

    def log(self, kwargs):
        self.logger.log(kwargs)


class ApiGameSeasonRequester(ApiRequester):
    def __init__(self, api_url, logger=ConsoleLogger):
        super().__init__(api_url)
        self.season_type = "02"
        self.max_game = 1271

    def get_data(self, year, latest_season_i=1):
        '''for i in range(10):
            print(inspect.stack()[i][3])'''
        game_data = {}
        for i in range(latest_season_i-1, (self.max_game + 1)):
            self.log("ApiGameSeasonRequester : " + str(i) + " / " + str(self.max_game))
            game_id = str(year) + self.season_type + str(i).zfill(4)
            response = requests.get(url=(self.api_url + game_id + "/feed/live"))
            response = response.json()
            response['game_api_i'] = i
            game_data["regular" + game_id] = response
            time.sleep(0.1)

        return game_data


class ApiGamePlayoffsRequester(ApiRequester):
    def __init__(self, api_url, logger=ConsoleLogger):
        super().__init__(api_url, logger)
        self.season_type = "03"
        self.api_url = api_url

    def get_data(self, year, latest_round_api=1, latest_matchup_api=1):
        game_data = {}
        first_digit = 0

        for _round in range(latest_round_api, 5):
            for matchup in range(latest_matchup_api, ((8 // (2 ** (_round - 1))) + 1)):
                for game in range(1, 8):
                    game_id = str(year) + self.season_type + str(first_digit) + str(_round) + str(matchup) + str(game)
                    url = (self.api_url + game_id + "/feed/live")
                    print(url, str(_round) + "_" + str(matchup), "/", str(5) + "_" + str(((8 // (2 ** (_round - 1))) + 1)))
                    response = requests.get(url=(self.api_url + game_id + "/feed/live"))
                    if response.status_code == 404:
                        time.sleep(0.1)
                        return game_data
                    response = response.json()
                    response['_round_api'] = _round
                    response['matchup_api'] = matchup
                    game_data["playoff" + game_id] = response
                    time.sleep(0.1)

        return game_data
