import json
from .localizations.local_str import local_str


def localized_str(lang: str):
    localized = local_str()
    try:
        with open(f'./src/localizations/{lang}.json') as f:
            data = json.load(f)
            localized.load_data(data)
    except FileNotFoundError:
        with open('./src/localizations/en.json') as f:
            data = json.load(f)
            localized.load_data(data)
    return localized
