import os
from dotenv import load_dotenv
import json
import configparser


def get_env_var(name: str):
    load_dotenv()
    return os.environ.get(name)


def get_config_var(name: str):
    with open('config.json') as f:
        data = json.load(f)
    return data[name]


def get_messages_var(lang, atr):
    config = configparser.ConfigParser()
    config.read('texts.INI', encoding='utf-8')
    try:
        return config.get(lang, atr)
    except Exception as err:
        print('Cause: {}'.format(err))
        return "ERR"
