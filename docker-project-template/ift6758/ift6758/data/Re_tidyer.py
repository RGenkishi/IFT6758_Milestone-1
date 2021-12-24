import os
import numpy as np
import pandas as pd
from ift6758.data.dataAquirer import DataAquirer
from ift6758.data.tidyDataKeys import *
from ift6758.utilitaires.logger import ConsoleLogger

# chemin pour l'enregistrement des données tidyfiées : dans le sous-dossier database du dossier contenant le module
pandasDatabasePath = os.path.dirname(__file__)+"/database/panda"


class Tidyer:

    def __int__(self, verbose=True, logger=ConsoleLogger):
        self.logger = logger()
        self.verbose = verbose


    def log_warn(self, *kwargs):
        self.logger.log_warn(kwargs)

    def list_player_types(self, players):
        return set((player["playerType"] for player in players))


    def there_is_no_goalie(self, players):
        return not ("Goalie" in self.list_player_types(players))


    def get_ring_side(self, game, team, period):
        home_team = game["gameData"]["teams"]["home"]["name"]
        away_team = game["gameData"]["teams"]["away"]["name"]
        periods = game["liveData"]["linescore"]["periods"]
        try:
            if team == home_team:
                return periods[period - 1]["home"][RINK_SIDE] if RINK_SIDE in periods[period - 1]["home"].keys() else np.nan
            else:
                return periods[period - 1]["away"][RINK_SIDE] if RINK_SIDE in periods[period - 1]["home"].keys() else np.nan
        except:
            self.log(f"{self.logger.colors.YELLOW}" + str(game["gamePk"]))
            self.log(f"{self.logger.colors.YELLOW}" + str(team))
            self.log(f"{self.logger.colors.YELLOW}" + str(period))
            return np.nan


    def game_event_to_panda_df(self, year):
        # Création du dossier database/panda si inexistant
        if not os.path.isdir(pandasDatabasePath):
            os.makedirs(pandasDatabasePath)

        # Chemin pour l'enregistrement des données tidyfiées
        basePath = pandasDatabasePath + '/' + str(year) + '_'
        extension = '_tidydata.csv'
        filePaths = {'regular' : basePath + 'regular' + extension,
                     'playoff' : basePath + 'playoff' + extension
                     }

        # Si les fichiers csv existent déjà, on les récupère sans tout re-tidyfier
        if not False in set((os.path.isfile(filePath) for filePath in filePaths.values())):
            dfs = {dataType : pd.read_csv(filePath) for dataType, filePath in filePaths.items()}
            return dfs  # DataFrameS (dictionnaire de dataFrames)
        else:
            dataGetter = DataAquirer()
            dataGetter.get_all_games_data_for_a_year(year)

            data = {'regular' : dataGetter.season_data,
                    'playoff' : dataGetter.playoffs_data
                    }

            elementToRetrive = [GAME_ID,
                                GAME_TIME,
                                DATE_YEAR,
                                DATE_MONTH,
                                DATE_DAY,
                                PERIOD_TIME,
                                PERIOD_WHICH,
                                PERIOD_TYPE,
                                EVENT_TYPE,
                                IS_GOAL,
                                SHOT_TYPE,
                                STRENGTH,
                                TEAM_ID,
                                TEAM_NAME,
                                TEAM_LINK,
                                TEAM_TRI_CODE,
                                SHOOTER_NAME,
                                GOALIE_NAME,
                                RINK_SIDE,
                                COORD_X,
                                COORD_Y]

            tidyData = {key: dict(zip(elementToRetrive, [[] for i in range(len(elementToRetrive))])) for key in data}

            for gameType, games in data.items():
                for gameId, game in games.items():
                    try:
                        game['liveData']
                    except:
                        break
                    for play in game['liveData']['plays']['allPlays']:
                        if play['result']['event'] in ["Shot", "Goal"]:
                            tidyData[gameType][GAME_ID].append(gameId)
                            tidyData[gameType][GAME_TIME].append(play['about']['dateTime'])
                            tidyData[gameType][DATE_YEAR].append(game['gameData']['datetime']['dateTime'][0:4])
                            tidyData[gameType][DATE_MONTH].append(game['gameData']['datetime']['dateTime'][5:7])
                            tidyData[gameType][DATE_DAY].append(game['gameData']['datetime']['dateTime'][8:10])

                            tidyData[gameType][PERIOD_TIME].append(play['about']['periodTime'])
                            tidyData[gameType][PERIOD_WHICH].append(play['about']['period'])
                            tidyData[gameType][PERIOD_TYPE].append(play['about']['periodType'])

                            tidyData[gameType][EVENT_TYPE].append(play['result']['event'])
                            tidyData[gameType][IS_GOAL].append((play['result']['event'] == "Goal"))

                            tidyData[gameType][TEAM_ID].append(play['team']['id'])
                            tidyData[gameType][TEAM_NAME].append(play['team']['name'])
                            tidyData[gameType][TEAM_LINK].append(play['team']['link'])
                            tidyData[gameType][TEAM_TRI_CODE].append(play['team']['triCode'])
                            tidyData[gameType][COORD_X].append(play['coordinates']['x'] if 'x' in play['coordinates'].keys() else np.nan)
                            tidyData[gameType][COORD_Y].append(play['coordinates']['y'] if 'y' in play['coordinates'].keys() else np.nan)
                            tidyData[gameType][SHOT_TYPE].append(play['result']['secondaryType'] if 'secondaryType' in play['result'].keys() else np.nan)

                            isGoalieSet = False
                            isShooterSet = False
                            isStrengthSet = False
                            for player in play['players']:
                                if (not isShooterSet) and (player['playerType'] == "Shooter"):
                                    tidyData[gameType][SHOOTER_NAME].append(player['player']['fullName'])
                                    tidyData[gameType][STRENGTH].append(None)
                                    isShooterSet = True
                                    isStrengthSet = True
                                if (not isShooterSet) and (player['playerType'] == "Scorer"):
                                    tidyData[gameType][SHOOTER_NAME].append(player['player']['fullName'])
                                    tidyData[gameType][STRENGTH].append(play['result']['strength']['name'])
                                    if self.there_is_no_goalie(play['players']):
                                        tidyData[gameType][GOALIE_NAME].append(None)
                                        isGoalieSet = True
                                    isShooterSet = True
                                    isStrengthSet = True
                                if (not isGoalieSet) and (player['playerType'] == "Goalie"):
                                    tidyData[gameType][GOALIE_NAME].append(player['player']['fullName'])
                                    isGoalieSet = True

                            if not isShooterSet:
                                tidyData[gameType][SHOOTER_NAME].append(None)
                            if not isGoalieSet:
                                tidyData[gameType][GOALIE_NAME].append(None)
                            if not isStrengthSet:
                                tidyData[gameType][STRENGTH].append(None)

                            if play['about']['periodType'] != 'SHOOTOUT':
                                rink_side = self.get_ring_side(game, play['team']['name'], play['about']['period'])
                                tidyData[gameType][RINK_SIDE].append(rink_side)
                            else:
                                tidyData[gameType][RINK_SIDE].append(np.nan)

            for games in tidyData.values():
                for column in games.items():
                    column = pd.Series(column)

            dfs = {gameType : pd.DataFrame(games) for gameType, games in tidyData.items()}

            return dfs  # DataFrameS (dictionnaire de dataFrames)

    def other_events_to_panda_df(self, year):
        # Création du dossier database/panda si inexistant
        if not os.path.isdir(pandasDatabasePath):
            os.makedirs(pandasDatabasePath)

        # Chemin pour l'enregistrement des données tidyfiées
        basePath = pandasDatabasePath + '/' + str(year) + '_'
        extension = '_tidydata.csv'
        filePaths = {'regular' : basePath + 'regular' + extension,
                     'playoff' : basePath + 'playoff' + extension
                     }


        dataGetter = DataAquirer()
        dataGetter.get_all_games_data_for_a_year(year)

        data = {'regular' : dataGetter.season_data,
                'playoff' : dataGetter.playoffs_data
                }

        elementToRetrive = [GAME_ID,
                            GAME_TIME,
                            DATE_YEAR,
                            DATE_MONTH,
                            DATE_DAY,
                            PERIOD_TIME,
                            PERIOD_WHICH,
                            PERIOD_TYPE,
                            EVENT_TYPE,
                            IS_GOAL,
                            SHOT_TYPE,
                            STRENGTH,
                            TEAM_ID,
                            TEAM_NAME,
                            TEAM_LINK,
                            TEAM_TRI_CODE,
                            SHOOTER_NAME,
                            GOALIE_NAME,
                            RINK_SIDE,
                            COORD_X,
                            COORD_Y]

        tidyData = {key: dict(zip(elementToRetrive, [[] for i in range(len(elementToRetrive))])) for key in data}

        for gameType, games in data.items():
            for gameId, game in games.items():
                break
                try:
                    game['liveData']
                except:
                    break
                for play in game['liveData']['plays']['allPlays']:
                    if play['result']['event'] not in ["Shot", "Goal"]:
                        tidyData[gameType][GAME_ID].append(gameId)
                        tidyData[gameType][GAME_TIME].append(play['about']['dateTime'])
                        tidyData[gameType][DATE_YEAR].append(game['gameData']['datetime']['dateTime'][0:4])
                        tidyData[gameType][DATE_MONTH].append(game['gameData']['datetime']['dateTime'][5:7])
                        tidyData[gameType][DATE_DAY].append(game['gameData']['datetime']['dateTime'][8:10])

                        tidyData[gameType][PERIOD_TIME].append(play['about']['periodTime'])
                        tidyData[gameType][PERIOD_WHICH].append(play['about']['period'])
                        tidyData[gameType][PERIOD_TYPE].append(play['about']['periodType'])

                        tidyData[gameType][EVENT_TYPE].append(play['result']['event'])
                        tidyData[gameType][IS_GOAL].append((play['result']['event'] == "Goal"))

                        tidyData[gameType][TEAM_ID].append(play['team']['id'] if "team" in play.keys() else np.nan)
                        tidyData[gameType][TEAM_NAME].append(play['team']['name'] if "team" in play.keys() else np.nan)
                        tidyData[gameType][TEAM_LINK].append(play['team']['link'] if "team" in play.keys() else np.nan)
                        tidyData[gameType][TEAM_TRI_CODE].append(play['team']['triCode'] if "team" in play.keys() else np.nan)
                        tidyData[gameType][COORD_X].append(play['coordinates']['x'] if 'x' in play['coordinates'].keys() else np.nan)
                        tidyData[gameType][COORD_Y].append(play['coordinates']['y'] if 'y' in play['coordinates'].keys() else np.nan)
                        tidyData[gameType][SHOT_TYPE].append(play['result']['secondaryType'] if 'secondaryType' in play['result'].keys() else np.nan)


                        isGoalieSet = False
                        isShooterSet = False
                        isStrengthSet = False
                        if "players" in play.keys():
                            for player in play['players']:
                                if (not isShooterSet) and (player['playerType'] == "Shooter"):
                                    tidyData[gameType][SHOOTER_NAME].append(player['player']['fullName'])
                                    tidyData[gameType][STRENGTH].append(None)
                                    isShooterSet = True
                                    isStrengthSet = True
                                if (not isShooterSet) and (player['playerType'] == "Scorer"):
                                    tidyData[gameType][SHOOTER_NAME].append(player['player']['fullName'])
                                    tidyData[gameType][STRENGTH].append(play['result']['strength']['name'])
                                    if self.there_is_no_goalie(play['players']):
                                        tidyData[gameType][GOALIE_NAME].append(None)
                                        isGoalieSet = True
                                    isShooterSet = True
                                    isStrengthSet = True
                                if (not isGoalieSet) and (player['playerType'] == "Goalie"):
                                    tidyData[gameType][GOALIE_NAME].append(player['player']['fullName'])
                                    isGoalieSet = True

                        if not isShooterSet:
                            tidyData[gameType][SHOOTER_NAME].append(None)
                        if not isGoalieSet:
                            tidyData[gameType][GOALIE_NAME].append(None)
                        if not isStrengthSet:
                            tidyData[gameType][STRENGTH].append(None)

                        if play['about']['periodType'] != 'SHOOTOUT' and "team" in play.keys():
                            rink_side = self.get_ring_side(game, play['team']['name'], play['about']['period'])
                            tidyData[gameType][RINK_SIDE].append(rink_side)
                        else:
                            tidyData[gameType][RINK_SIDE].append(np.nan)

            for games in tidyData.values():
                for column in games.items():
                    column = pd.Series(column)


            dfs = {gameType : pd.DataFrame(games) for gameType, games in tidyData.items()}

            return dfs  # DataFrameS (dictionnaire de dataFrames)
