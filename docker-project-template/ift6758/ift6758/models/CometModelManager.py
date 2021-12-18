from comet_ml import Experiment
from comet_ml import API
import joblib
import time
import os
from ift6758.ift6758.utilitaires.logger import LoggingLogger

module_path = os.path.dirname(__file__) + '/'
default_model_dataBase = os.path.dirname(__file__) + "/modelDatabase/"


class CometModelManager:
    def __init__(self, workspace="genkishi", project_name="milestone-3", model_database=default_model_dataBase):
        os.makedirs(model_database, exist_ok=True)
        self.workspace = workspace
        self.project_name = project_name
        self.model_database = model_database
        with open(module_path + "API_KEY", "r") as f:
            self.API_KEY = f.readline()
        self.api = API(api_key=self.API_KEY)
        self.logger = LoggingLogger()

    def get_model_path(self, model_name):
        """
        retourne le chemin vers le fichier où le model model_name devrait être enregistré
        """
        return self.model_database + model_name + '.joblib'

    def sklearn_model_to_file(self, sklearn_model, model_name):
        """
        Enregistre le model sklearn sous le nom model_name + ".joblib" dans le dossier self.model_database
        """
        file_path = self.get_model_path(model_name)
        joblib.dump(sklearn_model, file_path)

        return file_path

    def file_to_sklear_model(self, model_name):
        """
        Retourne le model sklearn enregistré dans le fichier self.model_database + model_name + ".joblib"
        """
        return joblib.load(self.get_model_path(model_name))

    def log_model(self, model_name, experience_name=None, model_path=None):
        """
        Enregistre le model dans les expériences Comet_ml
        Lorsque l'on veut garder une trace d'un modèle sans savoir si on le réutilisera vraiment plus tard
        """
        exp = Experiment(api_key=self.API_KEY,  # don’t hardcode!!
                         project_name=self.project_name,
                         workspace=self.workspace,
                         )
        exp.set_name(model_name if experience_name is None else model_name)

        model_path = self.get_model_path(model_name) if model_path is None else model_path
        exp.log_model(name=model_name, file_or_folder=model_path)

    def register_model(self, model_name):
        """
        Enregistre le model dans Model Registry sur Comet ML.
        Pour des modèles "intéresants" dont on se servira plus tard
        """
        experiment = self.api.get(self.workspace, self.project_name, model_name)
        print(self.workspace, self.project_name, model_name)
        experiment.register_model(model_name=model_name, registry_name=model_name)

    def log_and_register_model(self, model_name, experience_name=None, model_path=None, n_attempts=10, sleep_time=0.5):
        """
        Enregistre le model dans les expériences Comet_ml
        puis enregistre le model dans Model Registry sur Comet ML.
        Lorsque l'on est sûr que le modèle est intéressant
        """
        # log the model
        self.log_model(self, model_name=model_name, experience_name=experience_name, model_path=model_path)

        # give some time to the model to be availaible on Comet_ML
        experiment = self.api.get(self.workspace, self.project_name, model_name)
        for i in range(n_attempts):
            if experiment is None:
                experiment = self.api.get(self.workspace, self.project_name, model_name)
            else:
                continue
            time.sleep(0.5)

        # register the model for future use
        self.register_model(model_name)

    def download_model(self, model_name, force=False):
        """
        Télécharge un modèle de Model Registry sur Comet ML
        """
        if force or not os.path.exists(self.get_model_path(model_name)):
            if force:
                self.logger.log("Tentative de telechargement forcee du model (" + model_name + ")")
            else:
                self.logger.log("Tentative de telechargement du modele non present en local (" + model_name + ")" )
            self.api.download_registry_model(workspace="genkishi",
                                             registry_name=model_name,
                                             output_path=self.model_database,
                                             expand=True)
        else:
            self.logger.log("Model (" + model_name + ")" + " deja present en local")
        return self.file_to_sklear_model(model_name=model_name)

    def download_model_from_experiment(self, model_name, force=False):
        """
        Télécharge un modèle depuis les éxpériences sur Comet ML
        """
        if force or not os.path.exists(self.get_model_path(model_name)):
            experiment = self.api.get(self.workspace, self.project_name, model_name)
            experiment.download_model(model_name, output_path=self.model_database, expand=True)
        return self.file_to_sklear_model(model_name=model_name)
