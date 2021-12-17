"""
If you are in the same directory as this file (app.py), you can run run the app using gunicorn:
    
    $ gunicorn --bind 0.0.0.0:<PORT> app:app

gunicorn can be installed via:

    $ pip install gunicorn

"""
import os
from pathlib import Path
import logging
import json as jsn

from IPython.core.display import JSON
from flask import Flask, jsonify, request, abort
import sklearn
import pandas as pd
import numpy as np
import joblib

from ift6758.ift6758.models.CometModelManager import CometModelManager

import ift6758


LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")

app = Flask(__name__)

cmm = CometModelManager()
model = None


@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e.g. load model,
    setup logging handler, etc.)
    """
    logging.basicConfig(filename=LOG_FILE,
                        level=logging.INFO,
                        format="{'time':'%(asctime)s', 'name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s'}")
    logging.log(logging.INFO, "logging initialized")

    # TODO: any other initialization before the first request (e.g. load default model)
    pass


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""
    # pour tester dans un navigateur:
    # http://0.0.0.0:8080/logs

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

    response = logs

    return jsonify(response)  # response must be json serializable!


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
    
    """
    global model
    # Pour tester sur iris
    # Tester dans le terminal avec :
    # curl -v -H "Content-Type: application/json" -X POST -d '{"model_name": "iris-model"}' http://0.0.0.0:8080/download_registry_model

    # Get POST json data
    json = request.get_json()
    app.logger.info(jsn.dumps(json))

    if not 'model_name' in json:
        app.logger.info("la clé model_name doit être spécifié pour download_registry_model")
        response = "la clé model_name doit être spécifié pour download_registry_model"
    else:
        force = json['force'] if 'force' in json else False

        model = cmm.download_model(json['model_name'])


    # TODO: check to see if the model you are querying for is already downloaded

    # TODO: if yes, load that model and write to the log about the model change.  
    # eg: app.logger.info(<LOG STRING>)
    
    # TODO: if no, try downloading the model: if it succeeds, load that model and write to the log
    # about the model change. If it fails, write to the log about the failure and keep the 
    # currently loaded model

    # Tip: you can implement a "CometMLClient" similar to your App client to abstract all of this
    # logic and querying of the CometML servers away to keep it clean here

        response = "modèle " + json['model_name'] + " téléchargé"
    print(model)

    app.logger.info(jsn.dumps(response))
    return jsonify(response)  # response must be json serializable!


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Returns predictions
    """
    global model

    # Pour tester sur iris
    # Tester une bonne prédiction dans le terminal:
    # curl -v -H "Content-Type: application/json" -X POST -d '{"features":[5.8, 2.8, 5.1, 2.4]}' http://0.0.0.0:8080/predict
    # retourne 2 pour

    # Tester une bonne prédiction dans le terminal:
    # curl -v -H "Content-Type: application/json" -X POST -d '{"features":[5.6, 2.8, 4.9, 2.0]}' http://0.0.0.0:8080/predict
    # retourne 1 au lieu de 2


    # Get POST json data
    json = request.get_json()
    app.logger.info(str(json).replace("'", '"'))

    if not 'features' in json:
        app.logger.info("la clé features doit être spécifié pour predict et pointer vers une liste")
        response = "la clé features doit être spécifié pour predict et pointer vers une liste"
    else:
    
        pred = model.predict(np.array(json['features']).reshape(1, -1))[0]
        response = {'predicted_class': str(pred)}

    print("resp")
    print(type(response))
    print(response)
    app.logger.info(response)
    return jsonify(response)  # response must be json serializable!


@app.route("/test", methods=["POST"])
def test():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/test

    Returns the request
    """
    # Get POST json data
    json = request.get_json()
    app.logger.info(json)

    response = json

    app.logger.info(response)
    return jsonify(response)  # response must be json serializable!