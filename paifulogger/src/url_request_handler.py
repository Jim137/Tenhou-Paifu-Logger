import gzip
import urllib.request

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
