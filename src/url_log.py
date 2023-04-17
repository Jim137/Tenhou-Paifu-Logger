import pandas as pd
from .local import local_str


def check_duplicate(url, local_str: local_str):
    store = pd.HDFStore(f'./{local_str.paifu}/url_hash_log.h5')
    if 'url_hash' not in store:
        store['url_hash'] = pd.DataFrame({'url': [], 'hash': []})
    duplicated = url in store['url_hash']['url'].values
    store.close()
    return duplicated


def url_log(url, local_str: local_str):
    store = pd.HDFStore(f'./{local_str.paifu}/url_hash_log.h5')
    if 'url_hash' not in store:
        store['url_hash'] = pd.DataFrame({'url': [], 'hash': []})
    store['url_hash'] = pd.DataFrame(
        {'url': url}, index=[len(store['url_hash'])])
    store.close()
