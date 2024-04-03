import gzip
import os
import urllib.request
import xml.etree.ElementTree as ET

from .i18n import LocalStr
from .Paifu import Paifu


HEADER = {
    "Host": "e.mjv.jp",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def url_request_handler(url: str):
    url = url.split("=")[1]
    url = "https://tenhou.net/0/log/?" + url[:-3]
    req = urllib.request.Request(url=url, headers=HEADER)
    opener = urllib.request.build_opener()
    response = opener.open(req)
    response = gzip.decompress(response.read()).decode("utf-8")
    return response


def get_paifu(url: str, local_lang: LocalStr, output: str, mjai: bool = False):
    response = url_request_handler(url)
    root = ET.fromstring(response)
    paifu = Paifu(url, root)
    path = f"{output}/{local_lang.paifu}/{paifu.go_str}/"
    if not os.path.isdir(path):
        os.makedirs(path)

    url = url.split("=")[1] + "=" + url.split("=")[2]
    with open(path + url + ".xml", "w") as t:
        t.write(response)

    # mjai format output
    if mjai:
        if paifu.player_num == 3:
            print(local_lang.sanma_mjai_error)
            return paifu

        try:
            from .mjlog2mjai.parse import load_mjlog, parse_mjlog_to_mjai
        except ImportError:
            print(local_lang.log2mjai_import_error)
            return paifu
        if not os.path.isdir(path + "/mjai/"):
            os.makedirs(path + "/mjai/")
        with open(path + "/mjai/" + url + ".mjson", "w", encoding="UTF-8") as f:
            f.write(parse_mjlog_to_mjai(load_mjlog(path + url + ".xml")))

    return paifu
