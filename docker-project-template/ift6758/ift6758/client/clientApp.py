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
# Please don't look too much above..


class ClientApp:
    def __init__(self, ip="0.0.0.0", port=8080):
        self.client_serving = ServingClient(ip=ip, port=port)
        self.w_workspace = widgets.Text(placeholder='genkishi',
                                        description='Workspace:',
                                        disabled=False
                                        )
        self.workspace = None
        self.w_model = widgets.Text(placeholder='iris-model',
                                    description='Model:',
                                    disabled=False
                                    )
        self.model = None
        self.w_features = widgets.Text(placeholder='[[5.8, 2.8, 5.1, 2.4], [5.6, 2.8, 4.9, 2.0]]',
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
        self.workspace = self.w_workspace.value
        self.model = self.w_model.value
        res = self.client_serving.download_registry_model(workspace=self.workspace, model=self.model)
        if res[STATUS] == SUCCESS:
            print(res[MESSAGE])

        print(res)

    def lauchWidget(self):
        w_box = widgets.VBox([self.w_workspace, self.w_model, self.w_download_model])
        self.w_download_model.on_click(self.download_model)
        display(w_box)

    def predict(self, _):
        self.features = self.w_features.value
        pred = self.client_serving.predict(pd.DataFrame(eval(self.features)))
        print(pred)

    def prediction_widget(self):
        self.download_model(None)
        w_box = widgets.VBox([self.w_features, self.w_predict])
        self.w_predict.on_click(self.predict)
        display(w_box)


    def logs(self):
        return self.client_serving.logs()
