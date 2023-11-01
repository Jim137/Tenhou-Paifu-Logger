"""
URL Logger and Duplicate Checker

This module provides functionality to save URLs to a log file and check if a URL is duplicated in the log.

Log File:
    The module uses an HDF5 file format (url_log.h5) to store URLs. The log file is created automatically when
    you log the first URL.

Functions:
    - url_log(url, local_str: local_str, output: str) -> None:
        Logs the given URL to the log file.

    - check_duplicate(url, local_str: local_str, output: str) -> bool:
        Checks if the given URL already exists in the log file.

"""

from pandas import HDFStore, DataFrame
import os
from .i18n import local_str


def check_duplicate(url, local_str: local_str, output: str) -> bool:
    path = f"{output}/{local_str.paifu}"
    if not os.path.isdir(path):
        os.makedirs(path)
    store = HDFStore(f"{path}/url_log.h5")
    if "url" not in store:
        store["url"] = DataFrame(columns=["url"])
    duplicated = url.split("//")[1] in store["url"]["url"].values
    store.close()
    return duplicated


def url_log(url, local_str: local_str, output: str) -> None:
    path = f"{output}/{local_str.paifu}"
    if not os.path.isdir(path):
        os.makedirs(path)
    store = HDFStore(f"{path}/url_log.h5")
    if "url" not in store:
        store["url"] = DataFrame(columns=["url"])
    urls = store["url"]
    urls.loc[len(urls)] = url.split("//")[1]
    store["url"] = urls
    store.close()
