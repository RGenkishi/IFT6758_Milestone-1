"""
If you are in the same directory as this file (app.py), you can run run the app using gunicorn:
    
    $ gunicorn --bind 0.0.0.0:<PORT> app:app

gunicorn can be installed via:

    $ pip install gunicorn

"""
import os
from pathlib import Path
import logging
from ift6758.ift6758.utilitaires.logger import LoggingLogger
from ift6758.ift6758.utilitaires.keys import *
from ift6758.ift6758.features.re_featurizer import *
import json as jsn

from IPython.core.display import JSON
from flask import Flask, jsonify, request, abort
import sklearn
import pandas as pd
import numpy as np
import joblib

from ift6758.LANG.log_string import *
from ift6758.LANG.msg_string import *
from ift6758.ift6758.models.CometModelManager import CometModelManager

import ift6758

# Chemin du fichier de log
LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")

app = Flask(__name__)

cmm = None
model = None
logger = None


@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e.g. load model,
    setup logging handler, etc.)
    """
    global logger, cmm
    logging.basicConfig(filename=LOG_FILE,
                        level=logging.INFO,
                        format="{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': %(message)s, 'transmission': %(transmission)s,'file': '%(caller_file)s', 'function': '%(caller_func)s'}")
    logger = LoggingLogger()
    logger.log(LOG_LOGGER_INITIALIZED())
    cmm = CometModelManager()

    # DONE: any other initialization before the first request (e.g. load default model)
    pass


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model

    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.

    Recommend (but not required) json with the schema:

        {
            workspace: (required),
            model: (required),
            version: (required),
            ... (other fields if needed) ...
        }

    # Pour tester sur iris
    # Tester dans le terminal avec :
    # curl -v -H "Content-Type: application/json" -X POST -d '{"model_name": "iris-model"}' http://0.0.0.0:8080/download_registry_model
    """
    global model

    # Get POST json data
    json = request.get_json()
    logger.log(LOG_REQUEST_RECEIVED(), transmission=json)

    if not 'model_name' in json:
        response = {STATUS: WARNING,
                    MESSAGE: MSG_MISSING_KEY('model_name', example='\'iris-model\'')
                    }
        logger.log_warn(LOG_MISSING_KEY('model_name'), transmission=response)
    else:
        force = json['force'] if 'force' in json else False
        try:
            model_name = json['model_name']
            if 'workspace' in json:
                model = cmm.download_model(model_name, workspace=json['workspace'], force=force)
            else:
                model = cmm.download_model(model_name, force=force)
            response = {STATUS: SUCCESS,
                        MESSAGE: MSG_MODEL_LOADED_SUCCESSFULLY(model_name)
                        }
            logger.log(LOG_MODEL_LOADED_SUCCESSFULLY(model_name), transmission=response)
        except Exception as e:
            response = {STATUS: ERROR,
                        MESSAGE: MSG_MODEL_LOAD_ERROR(model_name),
                        ERROR: str(e)}
            logger.log_err({MESSAGE: LOG_MODEL_LOAD_ERROR(model_name),
                            ERROR: str(e)},
                           transmission=response)

    '''
    # DONE: check to see if the model you are querying for is already downloaded

    # DONE: if yes, load that model and write to the log about the model change.
    # eg: app.logger.info(<LOG STRING>, extra={'caller_file': 'hihi', 'caller_func': 'hoho'})

    # DONE: if no, try downloading the model: if it succeeds, load that model and write to the log
    # about the model change. If it fails, write to the log about the failure and keep the
    # currently loaded model

    # Tip: you can implement a "CometMLClient" similar to your App client to abstract all of this
    # logic and querying of the CometML servers away to keep it clean here
    '''

    return jsonify(response)  # response must be json serializable!


@app.route("/download_registry_model", methods=["POST"])
def get_new_data_for_prediction():
    # Get POST json data
    json = request.get_json()
    logger.log(LOG_REQUEST_RECEIVED(), transmission=json)

    if not 'last_marker' in json:
        last_game_time = None
    else:
        last_game_time = json['last_marker']
    dict_shot_goals, dict_other_event = load_data(2021)
    if last_game_time is None:
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
            response = {STATUS: WARNING,
                        MESSAGE: MSG_NEW_DATA_DOWNLOADED(),
                        }
            logger.log_err({MESSAGE: LOG_NO_NEW_DATA_AVAILABLE(last_game_time)},
                           transmission=response)
            print(LOG_NO_NEW_DATA_AVAILABLE(last_game_time))
        else:
            response = {STATUS: SUCCESS,
                        MESSAGE: MSG_NEW_DATA_DOWNLOADED(),
                        }
            logger.log_err({MESSAGE: LOG_NEW_DATA_SENT(last_game_time)},
                           transmission=response)
            print(LOG_NEW_DATA_SENT(last_game_time))

    return response  # dfs


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    # pour tester dans un navigateur:
    # http://0.0.0.0:8080/logs

    logger.log(LOG_REQUEST_RECEIVED())
    logger.log(LOG_SENDING_LOGS_TO_CLIENT())  # before doing it in order to include it in the return for consistency

    raw_logs = []
    with open(LOG_FILE, 'r') as log_file:
        c_log = log_file.readline()
        while c_log:
            raw_logs.append(c_log.strip('\n\r'))
            c_log = log_file.readline()

    logs = []
    in_irregular_log = False
    irregular_log_index = 0
    for log_line in raw_logs:
        if log_line[0] == '{':
            in_irregular_log = False
            logs.append(eval(log_line))  # évalue le dico
        else:
            if not in_irregular_log:
                irregular_log_index = 0
                logs.append({'time': 'UNKNOWN', 'name': 'app', 'level': 'Python Traceback', 'message': log_line})
                in_irregular_log = True
            else:
                logs[-1]['message' + str('{0:03}'.format(irregular_log_index))] = log_line
                irregular_log_index += 1

    response = logs  # raw format for easy display in firefox

    return jsonify(response)  # response must be json serializable!


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Returns predictions

    # Pour tester sur iris
    # Tester une bonne prédiction dans le terminal:
    # curl -v -H "Content-Type: application/json" -X POST -d '{"features":[5.8, 2.8, 5.1, 2.4]}' http://0.0.0.0:8080/predict
    # retourne 2 pour

    # Tester une bonne prédiction dans le terminal:
    # curl -v -H "Content-Type: application/json" -X POST -d '{"features":[5.6, 2.8, 4.9, 2.0]}' http://0.0.0.0:8080/predict
    # retourne 1 au lieu de 2
    """
    global model

    # Get POST json data
    json = request.get_json()
    logger.log(LOG_REQUEST_RECEIVED(), transmission=json)

    if not 'features' in json:
        response = {STATUS: WARNING,
                    MESSAGE: MSG_MISSING_KEY('features', example="[5.8, 2.8, 5.1, 2.4]")
                    }
        logger.log_warn(LOG_MISSING_KEY('features'), transmission=response)
    else:
        if model is not None:
            frame = pd.json_normalize(json['features'])
            preds = model.predict(pd.DataFrame(json['features']))
            response = {STATUS: SUCCESS,
                        'predictions': preds.tolist()}
            logger.log(LOG_PREDICTION_SENT_TO_CLIENT(), transmission=response)

        else:
            response = {STATUS: ERROR,
                        MESSAGE: MSG_PREDICTION_ATTEMPT_ON_NONE_MODEL()}
            logger.log_err(LOG_PREDICTION_ATTEMPT_ON_NONE_MODEL())

    return jsonify(response)  # response must be json serializable!


@app.route("/test", methods=["POST"])
def test():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/test

    Returns the request
    """

    # Get POST json data
    json = request.get_json()
    logger.log(LOG_REQUEST_RECEIVED(), transmission=json)

    response = {STATUS: SUCCESS,
                'request': json,
                'API-KEY': os.environ["COMET_API_KEY"]
                }
    logger.log(LOG_SENDING_RESPONSE_TO_CLIENT(), transmission=json)
    return jsonify(response)  # response must be json serializable!


@app.route("/set_log_lang", methods=["POST"])
def set_log_lang():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/set_log_lang

    Returns the log language after setting it
    """

    json = request.get_json()
    logger.log(LOG_REQUEST_RECEIVED(), transmission=json)

    if not 'LANG' in json:
        response = {STATUS: WARNING,
                    MESSAGE: MSG_MISSING_KEY('LANG', example='\'LANG_LOG_FRA\'')
                    }
        logger.log_warn(LOG_MISSING_KEY('LANG'), transmission=response)
    else:
        try:
            launch_log_lang(json['LANG'])
            response = {STATUS: SUCCESS,
                        MESSAGE: MSG_LOG_LANG_CHANGED_SUCCESSFULLY(get_lang_log_source()),
                        'LANG': get_lang_log_source()}
            logger.log(LOG_LOG_LANG_CHANGED_SUCCESSFULLY(get_lang_log_source()), transmission=response)
        except Exception as e:
            response = {STATUS: ERROR,
                        MESSAGE: MSG_LOG_LANG_CHANGE_ERROR(get_lang_log_source()),
                        'LANG': get_lang_log_source()}
            logger.log_err({MESSAGE: LOG_LOG_LANG_CHANGE_ERROR(get_lang_log_source()),
                            ERROR: str(e)},
                           transmission=response)

    return jsonify(response)  # response must be json serializable!


@app.route("/set_lang", methods=["POST"])
def set_lang():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/set_lang

    Returns the language of the responses to the client after setting it
    """

    json = request.get_json()
    logger.log(LOG_REQUEST_RECEIVED(), transmission=json)

    if not 'LANG' in json:
        response = {STATUS: WARNING,
                    MESSAGE: MSG_MISSING_KEY('LANG', example='\'LANG_LOG_FRA\'')
                    }
        logger.log_warn(LOG_MISSING_KEY('LANG'), transmission=response)
    else:
        try:
            launch_msg_lang(json['LANG'])
            response = {STATUS: SUCCESS,
                        MESSAGE: MSG_MSG_LANG_CHANGED_SUCCESSFULLY(get_lang_msg_source()),
                        'LANG': get_lang_msg_source()}
            logger.log(LOG_MSG_LANG_CHANGED_SUCCESSFULLY(get_lang_msg_source()), transmission=response)
        except Exception as e:
            response = {STATUS: ERROR,
                        MESSAGE: MSG_MSG_LANG_CHANGE_ERROR(get_lang_msg_source()),
                        'LANG': get_lang_log_source()}
            logger.log_err({MESSAGE: LOG_MSG_LANG_CHANGE_ERROR(get_lang_msg_source()),
                            ERROR: str(e)},
                           transmission=response)

    return jsonify(response)  # response must be json serializable!
