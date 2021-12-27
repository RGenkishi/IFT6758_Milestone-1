import requests
import pandas as pd
import logging

try:
    from ift6758.utilitaires.keys import *
    from LANG.log_string import *
    from LANG.msg_string import *
except:
    from ift6758.ift6758.utilitaires.keys import *
    from ift6758.LANG.log_string import *
    from ift6758.LANG.msg_string import *

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

        res = requests.post(url=self.base_url + "/predict", json={'features': X.values.tolist()}).json()

        if not STATUS in res:
            print(MSG_MISSING_KEY(STATUS, example="\'success\'"))
            return None
        if res[STATUS] == SUCCESS:
            print(res[MESSAGE])
            predictions = pd.DataFrame(res['predictions'])
            return predictions
        else:
            print(STATUS, res[STATUS])
            print(res[MESSAGE])

    def logs(self) -> dict:
        """Get server logs"""

        res = requests.get(url=self.base_url + "/logs")

        logs_list = res.json()
        logs_dict = {key: logs_list[key] for key in range(len(logs_list))}

        return logs_dict

    def get_new_data_for_prediction(self, last_marker=None, verbose=False, output=None):
        with output:

            print(MSG_LAST_GAME_TIME_IS(last_marker if not last_marker is None else 'forever'))
            print(MSG_WAIT_FOR_THE_DOWNLOAD("60 sec"))
            res = requests.post(url=self.base_url + "/get_new_data_for_prediction", json={LAST_MARKER: last_marker})
            if verbose:
                print(res)
            res = res.json()

            if not STATUS in res:
                print(MSG_MISSING_KEY(STATUS, example="\'success\'"))
                return None
                print(STATUS, res[STATUS])
            print(res[MESSAGE])
            if res[STATUS] == SUCCESS:
                return res[LAST_MARKER], res[NEW_DATA]
            else:
                return res[LAST_MARKER], None

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

    def change_log_lang(self, new_log_lang):
        res = requests.post(url=self.base_url + "/set_log_lang",
                            json={'LANG': new_log_lang})
        res = res.json()
        if MESSAGE in res:
            return res[MESSAGE]
        else:
            return res

    def change_msg_lang(self, new_log_lang):
        try:
            launch_msg_lang(new_log_lang)
        except:
            print(MSG_MSG_LOCAL_LANG_CHANGE_ERROR(new_log_lang))
        res = requests.post(url=self.base_url + "/set_lang",
                            json={'LANG': new_log_lang})
        res = res.json()
        if MESSAGE in res:
            return res[MESSAGE]
        else:
            return res


if __name__ == "__main__":
    sc = ServingClient()

    '''print(sc.download_registry_model(workspace="genkishi", model="iris-model"))
    print()

    print(sc.predict(pd.DataFrame([[5.8, 2.8, 5.1, 2.4],
                             [5.6, 2.8, 4.9, 2.0]])))

    print(sc.get_new_data_for_prediction())
    print()

    print(sc.logs())'''
    sc.change_log_lang('LANG_LOG_FRA')
