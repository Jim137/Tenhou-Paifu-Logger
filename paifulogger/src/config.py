import os

from platformdirs import user_data_dir


def config_path() -> str | None:
    """
    Try to get the path of the config file from current directory or user_data_dir.

    Returns
    -------
    str | None
        The path of the config file.
    """

    appname = "paifulogger"
    appauthor = "Jim137"
    user_data_dir(appname, appauthor)
    if os.path.exists("./config.json"):
        return "."
    elif os.path.exists(f"{user_data_dir(appname, appauthor)}/config.json"):
        return user_data_dir(appname, appauthor)
    else:
        return None
