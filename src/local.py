import json
import os
import sys

bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


class local_str():
    def __init__(self):
        pass

    def load_data(self, data):
        for key in data:
            self.__setattr__(key, data[key])

    def __setattr__(self, name, val):
        super().__setattr__(name, val)

    def __getattr__(self, name):
        import json
        with open(os.path.abspath(os.path.join(bundle_dir, 'localizations\en.json'))) as f:
            data = json.load(f)
        return data[name]


def localized_str(lang: str):
    localized = local_str()
    try:
        with open(os.path.abspath(os.path.join(bundle_dir, f'localizations\{lang}.json')), encoding='utf-8') as f:
            data = json.load(f)
            localized.load_data(data)
    except FileNotFoundError:
        with open(os.path.abspath(os.path.join(bundle_dir, 'localizations\en.json'))) as f:
            data = json.load(f)
            localized.load_data(data)
    return localized
