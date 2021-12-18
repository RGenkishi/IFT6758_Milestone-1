import importlib
import inspect

module_base = "ift6758.LANG."

LANG_LOG_SOURCE = 'LANG_LOG_FRA'

STRINGS_LOG = None


def launch_lang(lang_source):
    global LANG_LOG_SOURCE, STRINGS_LOG
    LANG_LOG_SOURCE = lang_source
    STRINGS_LOG = importlib.import_module(module_base + lang_source).STRINGS_LOG

def get_lang_log_source():
    return LANG_LOG_SOURCE


launch_lang(LANG_LOG_SOURCE)


def construct_string(*kwargs):
    return STRINGS_LOG[inspect.stack()[1][3]] % (kwargs)


def MISSING_KEY(key_Name):
    return construct_string(key_Name)


def LOGGER_INITIALIZED():
    return construct_string()


def SENDING_LOGS_TO_CLIENT():
    return construct_string()


def SENDING_RESPONSE_TO_CLIENT():
    return construct_string()


def REQUEST_RECEIVED():
    return construct_string(inspect.stack()[1][3])


def MODEL_LOADED_SUCCESSFULLY(model_name):
    return construct_string(model_name)


def MODEL_LOAD_ERROR(model_name):
    return construct_string(model_name)


def PREDICTION_SENT_TO_CLIENT():
    return construct_string()


def PREDICTION_ATTEMPT_ON_NONE_MODEL():
    return construct_string()


def LANG_CHANGED_SUCCESSFULLY(lang_name):
    return construct_string(lang_name)
