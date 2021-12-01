import time
import requests

from abc import abstractmethod


class ApiRequester:
    def __init__(self, api_url):
        self.season_type = None
        self.api_url = api_url

    @abstractmethod
    def get_data(self, year):
        pass


class ApiGameSeasonRequester(ApiRequester):
    def __init__(self, api_url):
        self.season_type = "02"
        self.api_url = api_url

    def get_data(self, year):
        game_data = {}
        max_game = 1271
        for i in range(1, (max_game + 1)):
            print("ApiGameSeasonRequester : " + str(i))
            game_id = str(year) + self.season_type + str(i).zfill(4)
            response = requests.get(url=(self.api_url + game_id + "/feed/live"))
            game_data["regular" + game_id] = response.json()
            time.sleep(0.1)

        return game_data


class ApiGamePlayoffsRequester(ApiRequester):
    def __init__(self, api_url):
        self.season_type = "03"
        self.api_url = api_url

    def get_data(self, year):
        game_data = {}
        first_digit = 0

        for _round in range(1, 5):
            for matchup in range(1, ((8 // (2 ** (_round - 1))) + 1)):
                for game in range(1, 8):
                    game_id = str(year) + self.season_type + str(first_digit) + str(_round) + str(matchup) + str(game)
                    url = (self.api_url + game_id + "/feed/live")
                    print(url)
                    response = requests.get(url=(self.api_url + game_id + "/feed/live"))
                    if response.status_code == 404:
                        time.sleep(0.1)
                        break
                    game_data["playoff" + game_id] = response.json()
                    time.sleep(0.1)

        return game_data
