import xml.etree.ElementTree as ET
import os
from .url_request_handler import url_request_handler
from .Haifu import Haifu
from .local import local_str


def get_haifu(url: str, local_str: local_str):
    response = url_request_handler(url)
    root = ET.fromstring(response)
    haifu = Haifu(url, root)
    if not os.path.isdir(f'./{local_str.haifu}/{haifu.go_str}/'):
        os.makedirs(f'./{local_str.haifu}/{haifu.go_str}/')

    with open(f'./{local_str.haifu}/{haifu.go_str}/'+url[26:]+'.xml', 'w') as t:
        t.write(response)
    return haifu
