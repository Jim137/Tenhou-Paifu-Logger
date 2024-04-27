import json

from .. import main_path


class LocalStr:
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


def localized_str(lang: str, main_path: str = main_path) -> LocalStr:
    """
    Get the localized string.

    Parameters
    ----------
    lang: str
        The language.
    main_path: str
        The main path.

    Returns
    -------
    LocalStr
        The localized string.
    """

    localized = LocalStr(lang, main_path)
    try:
        with open(f"{main_path}/localizations/{lang}.json", encoding="utf-8") as f:
            data = json.load(f)
            localized.load_data(data)
    except FileNotFoundError:
        print(f"Cannot find {lang}.json. Using English instead.")
        with open(f"{main_path}/localizations/en.json") as f:
            data = json.load(f)
            localized.load_data(data)
    return localized
