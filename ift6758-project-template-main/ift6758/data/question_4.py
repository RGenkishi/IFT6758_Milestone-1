''' --------------------------------------------------------------------------
Data we want :
game time / period information,
gameID,
team information(which team took the shot),
indicator if its a shot or a goal,
the on-ice coordinates,
the shooter name and
goalie name,
shot type,
if it was on an empty net, and
whether or not a goal was at even strength, shorthanded, or on the power play.
-------------------------------------------------------------------------------
'''


import os
import numpy as np
from ift6758.data.question_2 import *

pandasDatabasePath = os.path.dirname(__file__)+"/database/panda"  # chemin par défaut pour l'enregistrement des données tidyfiées

class Tidyfier:

    def list_player_types(self, players):
        return set((player["playerType"] for player in players))

    def there_is_no_goalie(self, players):
        return not ("Goalie" in self.list_player_types(players))

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

            elementToRetrive = ['matchId',
                                'dateYear',
                                'dateMonth',
                                'dateDay',
                                'event',
                                'period',
                                'teamId',
                                'teamName',
                                'teamLink',
                                'teamTriCode',
                                'coordX',
                                'coordY',
                                'shooterName',
                                'goalieName',
                                'shotSecondaryType']

            tidyData = {key: dict(zip(elementToRetrive, [[] for i in range(len(elementToRetrive))])) for key in data}

            for gameType, games in data.items():
                for gameId, game in games.items():
                    for play in game['liveData']['plays']['allPlays']:
                        if play['result']['event'] in ["Shot", "Goal"]:
                            tidyData[gameType]['matchId'].append(gameId)
                            tidyData[gameType]['dateYear'].append(game['gameData']['datetime']['dateTime'][0:4])
                            tidyData[gameType]['dateMonth'].append(game['gameData']['datetime']['dateTime'][5:7])
                            tidyData[gameType]['dateDay'].append(game['gameData']['datetime']['dateTime'][8:10])
                            tidyData[gameType]['event'].append(play['result']['event'])
                            tidyData[gameType]['period'].append(play['about']['periodTime'])
                            tidyData[gameType]['teamId'].append(play['team']['id'])
                            tidyData[gameType]['teamName'].append(play['team']['name'])
                            tidyData[gameType]['teamLink'].append(play['team']['link'])
                            tidyData[gameType]['teamTriCode'].append(play['team']['triCode'])
                            tidyData[gameType]['coordX'].append(play['coordinates']['x'] if 'x' in play['coordinates'].keys() else np.nan)
                            tidyData[gameType]['coordY'].append(play['coordinates']['y'] if 'y' in play['coordinates'].keys() else np.nan)
                            if len(play['players']) == 2:
                                player0Type = play['players'][0]['playerType']
                                tidyData[gameType]['shooterName' if player0Type == "Shooter" else 'goalieName'].append(play['players'][0]['player']['fullName'])
                                tidyData[gameType]['goalieName' if player0Type == "Shooter" else 'shooterName'].append(play['players'][1]['player']['fullName'])
                            else:
                                tidyData[gameType]['shooterName'].append(None)
                                tidyData[gameType]['goalieName'].append(None)
                            tidyData[gameType]['shotSecondaryType'].append(play['result']['secondaryType'] if 'secondaryType' in play['result'].keys() else np.nan)

            for games in tidyData.values():
                for column in games.items():
                    column = pd.Series(column)

            dfs = {gameType : pd.DataFrame(games) for gameType, games in tidyData.items()}
            for gameType, games in dfs.items():
                games.to_csv(filePaths[gameType], index=False, header=True)

            return dfs  # DataFrameS (dictionnaire de dataFrames)
