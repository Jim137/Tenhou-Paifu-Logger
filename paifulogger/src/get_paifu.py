import gzip
import os
import urllib.request
from glob import glob
import xml.etree.ElementTree as ET

from .i18n import LocalStr, localized_str
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


def get_paifu(
    url: str,
    local_lang: LocalStr = localized_str("en"),
    output: str = "./",
    mjai: bool = False,
    no_output: bool = False,
) -> Paifu:
    response = url_request_handler(url)
    root = ET.fromstring(response)
    paifu = Paifu(url, root)

    if no_output:
        return paifu

    path = f"{output}/{local_lang.paifu}/{paifu.go_str}/"
    if not os.path.isdir(path):
        os.makedirs(path)

    with open(path + paifu.name + ".xml", "w") as t:
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


def get_paifu_from_local(
    url: str,
    go_str: str,
    local_lang: LocalStr = localized_str("en"),
    output: str = "./",
) -> Paifu | None:
    path = f"{output}/{local_lang.paifu}/{go_str}/"
    url = url.split("=")[1] + "=" + url.split("=")[2]
    try:
        with open(path + url + ".xml", "r") as t:
            response = t.read()
    except FileNotFoundError:
        print(f"Cannot find {path + url + '.xml'}")
        return None
    root = ET.fromstring(response)
    paifu = Paifu(url, root)
    return paifu


def get_paifu_from_client_log(
    path: str,
) -> list[Paifu] | None:
    if not os.path.isdir(path):
        print(f"Cannot find {path}")
        return None
    paifu_list = []
    for file in glob(f"{path}/*.mjlog"):
        url = "https://tenhou.net/0/?log=" + file.split("/")[-1][:-6]
        with gzip.open(file, "r") as f:
            file_content = f.read()
        root = ET.fromstring(file_content)
        paifu = Paifu(url, root)
        paifu_list.append(paifu)
    return paifu_list
