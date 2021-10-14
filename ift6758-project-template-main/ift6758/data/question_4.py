import pandas as pd
import numpy as np

from ift6758.data.question_2 import *

pandasDatabasePath = os.path.dirname(__file__)+"/database/Panda"  # chemin par défaut pour l'enregistrement des données

class Tidyfier:
    def game_event_to_panda_df(self, year):
        dataGetter = DataAquirer()
        dataGetter.get_all_games_data_for_a_year(year)

        season_data = dataGetter.season_data

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

        data = dict(zip(elementToRetrive, [[] for i in range(len(elementToRetrive))]))

        for matchKey in season_data:
            for play in season_data[matchKey]['liveData']['plays']['allPlays']:
                if play['result']['event'] in ["Shot", "Goal"]:
                    data['matchId'].append(matchKey)
                    data['dateYear'].append(season_data[matchKey]['gameData']['datetime']['dateTime'][0:4])
                    data['dateMonth'].append(season_data[matchKey]['gameData']['datetime']['dateTime'][5:7])
                    data['dateDay'].append(season_data[matchKey]['gameData']['datetime']['dateTime'][8:10])
                    data['event'].append(play['result']['event'])
                    data['period'].append(play['about']['periodTime'])
                    data['teamId'].append(play['team']['id'])
                    data['teamName'].append(play['team']['name'])
                    data['teamLink'].append(play['team']['link'])
                    data['teamTriCode'].append(play['team']['triCode'])
                    data['coordX'].append(play['coordinates']['x'] if 'x' in play['coordinates'].keys() else np.nan)
                    data['coordY'].append(play['coordinates']['y'] if 'y' in play['coordinates'].keys() else np.nan)
                    if len(play['players']) == 2:
                        player0Type = play['players'][0]['playerType']
                        data['shooterName' if player0Type == "Shooter" else 'goalieName'].append(play['players'][0]['player']['fullName'])
                        data['goalieName' if player0Type == "Shooter" else 'shooterName'].append(play['players'][1]['player']['fullName'])
                    else:
                        data['shooterName'].append(None)
                        data['goalieName'].append(None)
                    data['shotSecondaryType'].append(play['result']['secondaryType'] if 'secondaryType' in play['result'].keys() else np.nan)

        for column in data.items():
            column = pd.Series(column)

        return pd.DataFrame(data)
