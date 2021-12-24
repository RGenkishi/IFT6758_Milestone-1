# Test Only
import pandas as pd
# Ce fichier ne doit être utilisé qu'à des fin de test.
# Le code répondant à une question devrait être directement
# dans le fichier correspondant à la question
# avec un "if __name__ == "__main__"
#from ift6758.models.CometModelManager import CometModelManager
#CometModelManager()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 200)
from ift6758.features.re_featurizer import *
last_game_time = None
dict_shot_goals, dict_other_event = load_data(2021)
if last_game_time == None :
    df_shot_goals = dict_shot_goals['regular']
    last_game_time = df_shot_goals.game_time.iloc[-1]
    df_other_event = dict_other_event['regular']
    df = prepare_data_for_feature_engineering(df_shot_goals, df_other_event)
    dfs = engineer_features(df)
else:
    dfs = pd.DataFrame()
    df_shot_goals = dict_shot_goals['regular']
    df_shot_goals = df_shot_goals[df_shot_goals['game_time'] >= last_game_time]
    if df_shot_goals.shape[0] > 1:
        last_game_time = df_shot_goals.game_time.iloc[-1]
        df_other_event = dict_other_event['regular']
        df = prepare_data_for_feature_engineering(df_shot_goals, df_other_event)
        dfs = engineer_features(df)
        df.drop(0, inplace=True)
    else:
        print("pas de nouvelles donnees depuis la derniere prediction ")


print(dfs)

#print(df.game_id)