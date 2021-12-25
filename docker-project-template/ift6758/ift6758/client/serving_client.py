import json
import requests
import pandas as pd
import logging
from ift6758.features.re_featurizer import *


logger = logging.getLogger(__name__)


class ServingClient:
    def __init__(self, ip: str = "0.0.0.0", port: int = 8080, features=None):
        self.base_url = f"http://{ip}:{port}"
        logger.info(f"Initializing client; base URL: {self.base_url}")

        if features is None:
            features = ["distance"]
        self.features = features

        # any other potential initialization

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Formats the inputs into an appropriate payload for a POST request, and queries the
        prediction service. Retrieves the response from the server, and processes it back into a
        dataframe that corresponds index-wise to the input dataframe.
        
        Args:
            X (Dataframe): Input dataframe to submit to the prediction service.
        """

        res = requests.post(url=self.base_url+"/predict", json={'features': X.values.tolist()})

        predictions = pd.DataFrame(res.json()['predictions'])

        return predictions

    def logs(self) -> dict:
        """Get server logs"""

        res = requests.get(url=self.base_url + "/logs")

        logs_list = res.json()
        logs_dict = {key: logs_list[key] for key in range(len(logs_list))}

        return logs_dict

    def get_new_data_for_prediction(self, last_marker):
        last_game_time = last_marker
        dict_shot_goals, dict_other_event = load_data(2021)
        if last_game_time == None:
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

        return dfs

    # def download_registry_model(self, workspace: str, model: str, version: str) -> dict:
    def download_registry_model(self, workspace: str, model: str) -> dict:
        """
        Triggers a "model swap" in the service; the workspace, model, and model version are
        specified and the service looks for this model in the model registry and tries to
        download it. 

        See more here:

            https://www.comet.ml/docs/python-sdk/API/#apidownload_registry_model
        
        Args:
            workspace (str): The Comet ML workspace
            model (str): The model in the Comet ML registry to download
            version (str): The model version to download
        """

        res = requests.post(url=self.base_url + "/download_registry_model",
                            json={'workspace': workspace, 'model_name': model})

        res = res.json()

        return res


if __name__ == "__main__":
    sc = ServingClient()

    print(sc.download_registry_model(workspace="genkishi", model="iris-model"))
    print()

    print(sc.predict(pd.DataFrame([[5.8, 2.8, 5.1, 2.4],
                             [5.6, 2.8, 4.9, 2.0]])))
    print()

    print(sc.logs())