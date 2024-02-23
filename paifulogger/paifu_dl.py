import os
import re

from .src.i18n import local_str
from .src.get_paifu import get_paifu


url_reg = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"


def _get_urls(urls, local_lang: local_str) -> list[str]:
    """
    Get urls from input or args.url.

    If remake, get urls from url_log.h5
    Else if not given args.url, get urls from input.

    Note:
        `re.findall(url_reg, url)` will return a list of urls that match the regular expression.
    """

    check_urls = []

    if not urls:
        for url in re.findall(url_reg, input(local_lang.hint_input)):
            check_urls.append(url)
    else:
        for url in urls:
            check_urls.extend(re.findall(url_reg, url))
    return check_urls


def paifu_dl(
    urls: str | list[str] | None = None,
    local_lang: local_str = local_str("en", os.path.dirname(os.path.abspath(__file__))),
    output: str = "./",
    mjai: bool = False,
) -> None:
    """
    Download paifu from tenhou.net.

    Args:
        urls: str | list[str]
            The url of the game log.
        local_lang: local_str
            The localized string.
        output: str
            The output directory.
        mjai: bool
            If True, download MJAI format.
    """

    if isinstance(urls, str):
        urls = [urls]

    check_urls = _get_urls(urls, local_lang)

    for url in check_urls:
        try:
            get_paifu(url, local_lang, output, mjai)
            print(f"paifu_dl: {url} has been downloaded.")
        except Exception as e:
            print(e)
