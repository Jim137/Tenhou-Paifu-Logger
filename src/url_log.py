from pandas import HDFStore, DataFrame
import os
from .local import local_str


def check_duplicate(url, local_str: local_str, output: str):
    path = f'{output}/{local_str.paifu}'
    if not os.path.isdir(path):
        os.makedirs(path)
    store = HDFStore(f'{path}/url_log.h5')
    if 'url' not in store:
        store['url'] = DataFrame(columns=['url'])
    duplicated = url.split('//')[1] in store['url']['url'].values
    store.close()
    return duplicated


def url_log(url, local_str: local_str, output: str):
    path = f'{output}/{local_str.paifu}'
    if not os.path.isdir(path):
        os.makedirs(path)
    store = HDFStore(f'{path}/url_log.h5')
    if 'url' not in store:
        store['url'] = DataFrame(columns=['url'])
    urls = store['url']
    urls.loc[len(urls)] = url.split('//')[1]
    store['url'] = urls
    store.close()
