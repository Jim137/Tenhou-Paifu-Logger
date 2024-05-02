"""
URL Logger and Duplicate Checker

This module provides functionality to save URLs to a log file and check if a URL is duplicated in the log.

Log File:
    The module uses an HDF5 file format (url_log.h5) to store URLs. The log file is created automatically when
    you log the first URL.

Functions:
    - url_log(url, local_lang: LocalStr, output: str) -> None:
        Logs the given URL to the log file.

    - check_duplicate(url, local_lang: LocalStr, output: str) -> bool:
        Checks if the given URL already exists in the log file.

"""

import os

from pandas import HDFStore, DataFrame

from .i18n import LocalStr


def check_duplicate(url, local_lang: LocalStr, output: str) -> bool:
    """
    Check if the given URL is already in the log file.

    Parameters
    ----------
    url: str
        The URL to check.
    local_lang: LocalStr
        The language settings.
    output: str
        The output directory.

    Returns
    -------
    bool
        True if the URL is duplicated, False otherwise.
    """

    path = f"{output}/{local_lang.paifu}"
    if not os.path.isdir(path):
        os.makedirs(path)
    store = HDFStore(f"{path}/url_log.h5")
    if "url" not in store:
        store["url"] = DataFrame(columns=["url"])
    duplicated = url.split("//")[1] in store["url"]["url"].values
    store.close()
    return duplicated


def url_log(url, local_lang: LocalStr, output: str) -> None:
    """
    Logs the given URL to the log file.

    Parameters
    ----------
    url: str
        The URL to log.
    local_lang: LocalStr
        The language settings.
    output: str
        The output directory.
    """

    path = f"{output}/{local_lang.paifu}"
    if not os.path.isdir(path):
        os.makedirs(path)
    store = HDFStore(f"{path}/url_log.h5")
    if "url" not in store:
        store["url"] = DataFrame(columns=["url"])
    if url.split("//")[1] in store["url"]["url"].values:
        store.close()
        return None
    urls = store["url"]
    urls.loc[str(len(urls))] = url.split("//")[1]
    store["url"] = urls
    store.close()
    return None
