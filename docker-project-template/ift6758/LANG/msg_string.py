import importlib
import inspect

module_base = "ift6758.LANG."

LANG_MSG_SOURCE = 'LANG_MSG_FRA'
LANG_MSG_SOURCE_ROLLBACK = 'LANG_MSG_ANG'

try:
    STRINGS_MSG = importlib.import_module(module_base + LANG_MSG_SOURCE).STRINGS_MSG
except:
    STRINGS_MSG = importlib.import_module(module_base + LANG_MSG_SOURCE_ROLLBACK).STRINGS_MSG
STRING_MSG_ROLLBACK = importlib.import_module(module_base + LANG_MSG_SOURCE_ROLLBACK).STRINGS_MSG


def launch_msg_lang(lang_source):
    global LANG_MSG_SOURCE, STRINGS_MSG
    LANG_MSG_SOURCE = lang_source
    STRINGS_MSG = importlib.import_module(module_base + lang_source).STRINGS_MSG


def get_lang_msg_source():
    return LANG_MSG_SOURCE


def construct_string(*kwargs):
    try:
        return STRINGS_MSG[inspect.stack()[1][3]].format(*kwargs)
    except:
        return STRING_MSG_ROLLBACK[inspect.stack()[1][3]].format(*kwargs)


def MSG_MISSING_KEY(key_name, example):
    return construct_string(key_name, inspect.stack()[1][3], example)


def MSG_MODEL_LOADED_SUCCESSFULLY(model_name):
    return construct_string(model_name)


def MSG_MODEL_LOAD_ERROR(model_name):
    return construct_string(model_name)


def MSG_PREDICTION_ATTEMPT_ON_NONE_MODEL():
    return construct_string()


def MSG_LOG_LANG_CHANGED_SUCCESSFULLY(lang_name):
    return construct_string(lang_name)


def MSG_LOG_LANG_CHANGE_ERROR(lang_name):
    return construct_string(lang_name)


def MSG_MSG_LANG_CHANGED_SUCCESSFULLY(lang_name):
    return construct_string(lang_name)


def MSG_MSG_LANG_CHANGE_ERROR(lang_name):
    return construct_string(lang_name)