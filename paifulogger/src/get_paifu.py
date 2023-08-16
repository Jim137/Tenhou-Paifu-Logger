import xml.etree.ElementTree as ET
import os

from .url_request_handler import url_request_handler
from .Paifu import Paifu
from .local import local_str


def get_paifu(url: str, local_str: local_str, output: str, mjai: bool = False):
    response = url_request_handler(url)
    root = ET.fromstring(response)
    paifu = Paifu(url, root)
    path = f'{output}/{local_str.paifu}/{paifu.go_str}/'
    if not os.path.isdir(path):
        os.makedirs(path)

    url = url.split('=')[1]+'='+url.split('=')[2]
    with open(path+url+'.xml', 'w') as t:
        t.write(response)
    
    # mjai format output
    if mjai:
        if paifu.player_num == 3:
            print(local_str.sanma_mjai_error)
            return paifu
        
        try:
            from .mjlog2mjai.parse import load_mjlog, parse_mjlog_to_mjai
        except ImportError:
            print(local_str.log2mjai_import_error)
            return paifu
        if not os.path.isdir(path+'/mjai/'):
            os.makedirs(path+'/mjai/')
        with open (path+'/mjai/'+url+'.mjson', 'w', encoding='UTF-8') as f:
            f.write(parse_mjlog_to_mjai(load_mjlog(path+url+'.xml')))

    return paifu
