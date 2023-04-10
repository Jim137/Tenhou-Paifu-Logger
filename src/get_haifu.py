import xml.etree.ElementTree as ET
from .url_request_handler import url_request_handler
from .Haifu import Haifu
from .local import local_str

def get_haifu(url: str, local_str: local_str):
    ban = int(url[-1])
    response = url_request_handler(url)
    root = ET.fromstring(response)
    haifu = Haifu(ban, root)
    with open(f'./{local_str.haifu}/{haifu.go_str}/'+url[26:]+'.xml', 'w') as t:
        t.write(response)
    return haifu