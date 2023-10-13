import json


class local_str:
    def __init__(self, lang: str = "en", main_path: str = "./"):
        self.lang = lang
        self.main_path = main_path
        pass

    def load_data(self, data):
        for key in data:
            self.__setattr__(key, data[key])

    def __setattr__(self, name, val):
        super().__setattr__(name, val)

    def __getattr__(self, name):
        "If the attribute is not loaded, return the value in English."

        with open(f"{self.main_path}/localizations/en.json") as f:
            data = json.load(f)
        return data[name]


def localized_str(lang: str, main_path: str) -> local_str:
    localized = local_str(lang, main_path)
    try:
        with open(f"{main_path}/localizations/{lang}.json", encoding="utf-8") as f:
            data = json.load(f)
            localized.load_data(data)
    except FileNotFoundError:
        with open(f"{main_path}/localizations/en.json") as f:
            data = json.load(f)
            localized.load_data(data)
    return localized
