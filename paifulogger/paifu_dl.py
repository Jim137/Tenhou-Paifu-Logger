import argparse
import json
import os
import re
import sys
import urllib.error

from . import main_path
from .log import _get_lang
from .src.config import config_path
from .src.i18n import localized_str, LocalStr
from .src.get_paifu import get_paifu


url_reg = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"


def _get_urls(urls, local_lang: LocalStr) -> list[str]:
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
    *,
    local_lang: LocalStr = localized_str("en"),
    output: str = "./",
    mjai: bool = False,
) -> int:
    """
    Download paifu from tenhou.net.

    Args:
        urls: str | list[str]
            The url of the game log.
        local_lang: LocalStr
            The localized string.
        output: str
            The output directory.
        mjai: bool
            If True, download MJAI format.
    """

    if isinstance(urls, str):
        urls = [urls]

    check_urls = _get_urls(urls, local_lang)

    retCode = 0
    for url in check_urls:
        try:
            get_paifu(url, local_lang, output, mjai)
            print(f"paifu_dl: {url} has been downloaded.")
        except urllib.error.URLError:
            print(local_lang.hint_url, url)
            retCode = 1
        except OSError:
            print(local_lang.hint_url, url)
            retCode = 1
    return retCode


def pdl(args: argparse.Namespace) -> int:
    if args.version:
        from .version import __version__

        print("Tenhou-Paifu-Logger", __version__)
        return 0

    local_lang = _get_lang(args.lang)

    return paifu_dl(
        args.url,
        local_lang=local_lang,
        output=args.output,
        mjai=args.mjai,
    )


def pdl_parser(
    config_path: str | None = None, parser: argparse.ArgumentParser | None = None
) -> argparse.Namespace:
    config = {}
    if config_path and os.path.exists(f"{config_path}/config.json"):
        with open(f"{config_path}/config.json", "r") as f:
            config = json.load(f)

    if parser is None:
        parser = argparse.ArgumentParser(description="Paifu Downloader")
    parser.add_argument("url", nargs="*", help="URL of the match.")
    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        help="""Language of the program and output files. Default is English. 
        Available languages: English(en), 繁體中文(zh_tw), 简体中文(zh), 日本語(ja).""",
        default=config.get("lang", None),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output directory. Default is './'.",
        default=config.get("output", None),
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show version of the program. If this is used, all other arguments will be ignored and the program will be closed.",
    )
    parser.add_argument(
        "--mjai",
        action="store_true",
        help="Output MJAI format paifu.",
        default=config.get("mjai", False),
    )

    args = parser.parse_args()
    if "pdl" in args.url:
        args.url.remove("pdl")
    return args


def main(plog_parser: argparse.ArgumentParser | None = None):
    args = pdl_parser(config_path(), plog_parser)
    sys.exit(pdl(args))
