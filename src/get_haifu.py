import xml.etree.ElementTree as ET
from .url_request_handler import url_request_handler
from .Haifu import Haifu


def get_haifu(url: str, local_haifu: str):
    ban = int(url[-1])
    t = open(f'./{local_haifu}/'+url[26:]+'.xml', 'w')
    response = url_request_handler(url)
    root = ET.fromstring(response)
    t.write(response)
    t.close()
    haifu = Haifu(ban, root)
    return haifu