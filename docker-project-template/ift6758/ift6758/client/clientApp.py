import pandas as pd
import ipywidgets as widgets
from IPython.display import display


# An horrible thing is following..
try:  # when running on docker
    from ift6758.ift6758.client.serving_client import *
    from ift6758.ift6758.utilitaires.keys import *
except:  # when editing (running ?) "locally"
    from ift6758.client.serving_client import *
    from ift6758.utilitaires.keys import *



class ClientApp:
    def __init__(self, ip="0.0.0.0", port=8080):
        self.last_marker = None
        self.new_data = None
        self.w_pred_output = widgets.Output()
        self.w_dl_model_output = widgets.Output()
        self.client_serving = ServingClient(ip=ip, port=port)
        self.w_workspace = widgets.Text(placeholder='genkishi',
                                        value='genkishi',
                                        description='Workspace:',
                                        disabled=False
                                        )
        self.workspace = None
        # iris-model is a valid model for testing with iris
        self.w_model = widgets.Text(placeholder='log-reg-distance-angle',
                                    value='iris-model',
                                    description='Model:',
                                    disabled=False
                                    )
        self.model = None
        self.w_features = widgets.Text(placeholder='[[5.8, 2.8, 5.1, 2.4], [5.6, 2.8, 4.9, 2.0]',
                                       value='[[5.8, 2.8, 5.1, 2.4], [5.6, 2.8, 4.9, 2.0]]',
                                       description='Feature values:',
                                       disabled=False
                                       )
        self.features = None
        self.w_download_model = widgets.Button(description='Download model',
                                               disabled=False,
                                               button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                               tooltip='Click me',
                                               icon='check'  # (FontAwesome names without the `fa-` prefix),
                                               )
        self.w_predict = widgets.Button(description='Predict',
                                        disabled=False,
                                        button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                                        tooltip='Click me',
                                        icon='check'  # (FontAwesome names without the `fa-` prefix),
                                        )

    def download_model(self, _):
        with self.w_dl_model_output:
            self.workspace = self.w_workspace.value
            self.model = self.w_model.value
            res = self.client_serving.download_registry_model(workspace=self.workspace, model=self.model)
            print(res[MESSAGE])

    def lauchWidget(self):
        self.w_download_model.on_click(self.download_model)
        w_box = widgets.VBox([self.w_workspace, self.w_model, self.w_download_model, self.w_dl_model_output])
        display(w_box)

    def predict(self, _):
        # Ending point : prediction_widget
        with self.w_pred_output:
            self.features = self.w_features.value
            nan = 0
            pred = self.client_serving.predict(pd.DataFrame(eval(self.features)))
            pd.options.display.max_rows = 500
            print(pred)

    def prediction_widget(self):
        # Entry Point : prediction_widget
        self.lauchWidget()
        self.w_predict.on_click(self.predict)
        w_box = widgets.VBox([self.w_features, self.w_predict, self.w_pred_output])
        display(w_box)

    def get_new_data_for_prediction(self):
        self.last_marker, self.new_data = self.client_serving.get_new_data_for_prediction(last_marker=self.last_marker,
                                                                                          model_name=self.model)

        return self.new_data


    def logs(self):
        return self.client_serving.logs()
