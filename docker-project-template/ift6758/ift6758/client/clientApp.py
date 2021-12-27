import pandas as pd
import ipywidgets as widgets
import functools
from IPython.display import display

# An horrible thing is following..
try:  # when running on docker
    from ift6758.ift6758.client.serving_client import *
    from ift6758.ift6758.utilitaires.keys import *
    from ift6758.LANG.msg_string import *
except:  # when editing (running ?) "locally"
    from ift6758.client.serving_client import *
    from ift6758.utilitaires.keys import *
    from LANG.msg_string import *

class Wrapper:
    def __init__(self, object):
        self.value = str(object)


class WidgetGen:
    @classmethod
    def new_w_choice_model(cls, model_name):
        return widgets.Text(placeholder=model_name,
                            value=model_name,
                            description=W_MODEL_IS(),
                            disabled=False
                            )

    @classmethod
    def new_w_choice_workspace(cls):
        return widgets.Text(placeholder='genkishi',
                            value='genkishi',
                            description=W_WORKSPACE_IS(),
                            disabled=False
                            )

    @classmethod
    def new_w_choice_features_values(cls, default_values):
        # default values : '[[5.8, 2.8, 5.1, 2.4], [5.6, 2.8, 4.9, 2.0]]'
        return widgets.Text(placeholder=default_values,
                            value=default_values,
                            description=W_VALUES_ARE(),
                            disabled=False
                            )

    @classmethod
    def new_w_button(cls, button_name, icon='check'):
        return widgets.Button(description=button_name,
                              disabled=False,
                              button_style='',  # 'success', 'info', 'warning', 'danger' or ''
                              tooltip=W_CLICK_ME(),
                              icon=icon  # (FontAwesome names without the `fa-` prefix),
                              )

    @classmethod
    def new_w_output(cls):
        return widgets.Output()

    @classmethod
    def new_w_dropdown_log_language(cls):
        return widgets.Dropdown(options=[('Anglais', 'LANG_LOG_ANG'),
                                         ('Français', 'LANG_LOG_FRA'),
                                         ('klingon', 'LANG_LOG_KLI')],
                                value='LANG_LOG_ANG',
                                description=W_LANG(),
                                )

    @classmethod
    def new_w_dropdown_msg_language(cls):
        return widgets.Dropdown(options=[('Anglais', 'LANG_MSG_ANG'),
                                         ('Français', 'LANG_MSG_FRA'),
                                         ('klingon', 'LANG_MSG_KLI')],
                                value='LANG_MSG_ANG',
                                description=W_LANG(),
                                )


class ClientApp:
    def __init__(self, ip="0.0.0.0", port=8080):
        self.client_serving = ServingClient(ip=ip, port=port)
        self.widgets = {}
        self.last_widget_id = 0
        self.last_marker = None
        self.new_data = None
        self.workspace = None
        self.model = None  # iris-model is a valid model for testing with iris
        self.features = None

    # Méthodes utilitaires

    def next_widget_id(self):
        self.last_widget_id += 1
        return self.last_widget_id - 1

    def download_model(self, _, calling_widget_id):
        with self.widgets[calling_widget_id]['output']:
            self.workspace = self.widgets[calling_widget_id]['workspace'].value
            self.model = self.widgets[calling_widget_id]['model'].value
            res = self.client_serving.download_registry_model(workspace=self.workspace, model=self.model)
            print(res[MESSAGE])

    def get_new_data_for_prediction(self, _, calling_widget_id):
        verbose = self.widgets[calling_widget_id]['verbose']
        output = self.widgets[calling_widget_id]['output']
        self.last_marker, self.new_data = self.client_serving.get_new_data_for_prediction(last_marker=self.last_marker,
                                                                                          verbose=verbose,
                                                                                          output=output)
        self.widgets[self.widgets[calling_widget_id]['pred_calling_widget_id']]['features_values'] = Wrapper(
            self.new_data)
        with output:
            if verbose and not (self.new_data is None):
                print([self.new_data[0]])

    def reset_last_game_time(self, _, calling_widget_id):
        output = self.widgets[calling_widget_id]['output']
        self.last_marker = None
        with output:
            print(MSG_GAME_TIME_RESET())

    def predict(self, _, calling_widget_id):
        with self.widgets[calling_widget_id]['output']:
            features_values = self.widgets[calling_widget_id]['features_values'].value
            if features_values == "None":
                print(MSG_NO_NEW_PREDICTION())
            else:
                nan = 0
                pred = self.client_serving.predict(pd.DataFrame(eval(features_values)))
                pd.options.display.max_rows = 500
                print(pred)

    def change_log_lang(self, _, calling_widget_id):
        new_log_lang = self.widgets[calling_widget_id]['new_log_lang'].value
        res = self.client_serving.change_log_lang(new_log_lang)
        with self.widgets[calling_widget_id]['output']:
            print(res)

    def change_msg_lang(self, _, calling_widget_id):
        new_log_lang = self.widgets[calling_widget_id]['new_msg_lang'].value
        res = self.client_serving.change_msg_lang(new_log_lang)
        with self.widgets[calling_widget_id]['output']:
            print(res)
            try:
                launch_msg_lang(new_log_lang)
            except:
                print(MSG_MSG_LOCAL_LANG_CHANGE_ERROR(new_log_lang))


    # méthodes de création de widgets
    def launch_widget_download_model(self, defaut_choice_model_name="log-reg-distance-angle"):
        calling_widget_id = self.next_widget_id()

        w_choice_workspace = WidgetGen.new_w_choice_workspace()
        w_choice_model = WidgetGen.new_w_choice_model(model_name=defaut_choice_model_name)
        w_button_download = WidgetGen.new_w_button(button_name=W_DOWNLOAD_MODEL(), icon='circle-arrow-down')
        w_button_download.on_click(functools.partial(self.download_model, calling_widget_id=calling_widget_id))
        w_output = WidgetGen.new_w_output()

        self.widgets[calling_widget_id] = {'workspace': w_choice_workspace,
                                           'model': w_choice_model,
                                           'output': w_output}

        w_box = widgets.VBox([w_choice_workspace, w_choice_model, w_button_download, w_output])
        display(w_box)

    def lauch_widget_simple_prediction(self,
                                       default_features_values,
                                       defaut_choice_model_name="log-reg-distance-angle",
                                       ):
        calling_widget_id = self.next_widget_id()
        self.launch_widget_download_model(defaut_choice_model_name=defaut_choice_model_name)

        w_features = WidgetGen.new_w_choice_features_values(default_values=default_features_values)
        w_button_predict = WidgetGen.new_w_button(button_name=W_PREDICT(), icon="microchip-ai")
        w_button_predict.on_click(functools.partial(self.predict, calling_widget_id=calling_widget_id))
        w_output_prediction = WidgetGen.new_w_output()

        self.widgets[calling_widget_id] = {'features_values': w_features,
                                           'output': w_output_prediction}

        w_box = widgets.VBox([w_features, w_button_predict, w_output_prediction])
        display(w_box)

    def lauch_widget_get_new_data(self, verbose=False, pred_calling_widget_id=None):
        calling_widget_id = self.next_widget_id()
        if pred_calling_widget_id is None:
            pred_calling_widget_id = calling_widget_id

        w_button_predict = WidgetGen.new_w_button(button_name=W_LOAD_DATA(), icon="circle-arrow-down")
        w_button_predict.on_click(functools.partial(self.get_new_data_for_prediction,
                                                    calling_widget_id=calling_widget_id))
        w_output_get_new_data = WidgetGen.new_w_output()

        self.widgets[calling_widget_id] = {'verbose': verbose,
                                           'output': w_output_get_new_data,
                                           'pred_calling_widget_id': pred_calling_widget_id}

        w_box = widgets.VBox([w_button_predict, w_output_get_new_data])
        display(w_box)

    def lauch_widget_prediction_on_new_data(self, defaut_choice_model_name="log-reg-distance-angle"):
        calling_widget_id = self.next_widget_id()
        self.launch_widget_download_model(defaut_choice_model_name=defaut_choice_model_name)
        self.lauch_widget_get_new_data(verbose=True, pred_calling_widget_id=calling_widget_id)

        w_button_predict = WidgetGen.new_w_button(button_name=W_PREDICT(), icon="microchip-ai")
        w_button_predict.on_click(functools.partial(self.predict, calling_widget_id=calling_widget_id))
        w_output_prediction = WidgetGen.new_w_output()

        self.widgets[calling_widget_id] = {'output': w_output_prediction}

        w_box = widgets.VBox([w_button_predict, w_output_prediction])
        display(w_box)

    def lauch_widget_reset_last_game_time(self):
        calling_widget_id = self.next_widget_id()

        w_button_reset = WidgetGen.new_w_button(button_name=W_RESET(), icon="microchip-ai")
        w_button_reset.on_click(functools.partial(self.reset_last_game_time, calling_widget_id=calling_widget_id))
        w_output_reset = WidgetGen.new_w_output()

        self.widgets[calling_widget_id] = {'output': w_output_reset}

        w_box = widgets.VBox([w_button_reset, w_output_reset])
        display(w_box)

    def launch_widget_log_langue(self):
        calling_widget_id = self.next_widget_id()

        w_choice_lang = WidgetGen.new_w_dropdown_log_language()
        w_button_change_lang = WidgetGen.new_w_button(button_name=W_CHANGE_LANG())
        w_button_change_lang.on_click(functools.partial(self.change_log_lang, calling_widget_id=calling_widget_id))
        w_output_log_lang = WidgetGen.new_w_output()

        self.widgets[calling_widget_id] = {'output': w_output_log_lang,
                                           'new_log_lang': w_choice_lang}

        w_box = widgets.VBox([w_choice_lang, w_button_change_lang, w_output_log_lang])
        display(w_box)

    def launch_widget_msg_langue(self):
        calling_widget_id = self.next_widget_id()

        w_choice_lang = WidgetGen.new_w_dropdown_msg_language()
        w_button_change_lang = WidgetGen.new_w_button(button_name=W_CHANGE_LANG())
        w_button_change_lang.on_click(functools.partial(self.change_msg_lang, calling_widget_id=calling_widget_id))
        w_output_log_lang = WidgetGen.new_w_output()

        self.widgets[calling_widget_id] = {'output': w_output_log_lang,
                                           'new_msg_lang': w_choice_lang}

        w_box = widgets.VBox([w_choice_lang, w_button_change_lang, w_output_log_lang])
        display(w_box)


    def logs(self):
        return self.client_serving.logs()
