import pandas as pd
import os
from .local import local_str


def check_duplicate(url, local_str: local_str):
    if not os.path.isdir(f'./{local_str.paifu}/'):
        os.makedirs(f'./{local_str.paifu}/')
    store = pd.HDFStore(f'./{local_str.paifu}/url_log.h5')
    if 'url' not in store:
        store['url'] = pd.DataFrame({'url': ['']})
    duplicated = url in store['url']['url'].values
    store.close()
    return duplicated


def url_log(url, local_str: local_str):
    if not os.path.isdir(f'./{local_str.paifu}/'):
        os.makedirs(f'./{local_str.paifu}/')
    store = pd.HDFStore(f'./{local_str.paifu}/url_log.h5')
    if 'url' not in store:
        store['url'] = pd.DataFrame({'url': ['']})
    store['url'] = pd.DataFrame(
        {'url': url}, index=[len(store['url'])])
    store.close()
