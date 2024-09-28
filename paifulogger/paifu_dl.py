import argparse
import json
import os
import re
import sys
import urllib.error

from . import __version__, main_path
from .log import _get_lang
from .config import config_path
from .utils import get_paifu
from .i18n import LocalStr, localized_str

REG_URL = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"


def _get_urls(urls, local_lang: LocalStr = localized_str("en", main_path)) -> list[str]:
    """
    Get urls from input or args.url.

    If remake, get urls from url_log.h5
    Else if not given args.url, get urls from input.

    Parameters
    ----------
    urls: str | list[str] | None
        The url of the game log.
    local_lang: LocalStr
        The localized string.

    Returns
    -------
    list
        The list of urls.

    Note
    ----
        `re.findall(REG_URL, url)` will return a list of urls that match the regular expression.
    """

    check_urls = []

    if not urls:
        for url in re.findall(REG_URL, input(local_lang.hint_input)):
            check_urls.append(url)
    else:
        for url in urls:
            check_urls.extend(re.findall(REG_URL, url))
    return check_urls


def paifu_dl(
    urls: str | list[str] | None = None,
    *,
    local_lang: LocalStr = localized_str("en", main_path),
    output: str = "./",
    mjai: bool = False,
) -> int:
    """
    Download paifu from tenhou.net.

    Parameters
    ----------
    urls: str | list[str] | None
        The url of the game log.
    local_lang: LocalStr
        The localized string.
    output: str
        The output directory.
    mjai: bool
        Output MJAI format paifu.

    Returns
    -------
    int
        The return code.
    """

    if isinstance(urls, str):
        urls = [urls]

    check_urls = _get_urls(urls, local_lang)

    retcode = 0
    for url in check_urls:
        try:
            get_paifu(url, local_lang, output, mjai)
            print(f"paifu_dl: {url} has been downloaded.")
        except urllib.error.URLError:
            print(local_lang.hint_url, url)
            retcode = 1
        except OSError:
            print(local_lang.hint_url, url)
            retcode = 1
    return retcode


def pdl(args: argparse.Namespace) -> int:

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
    """
    Parse the arguments from the command line.

    Parameters
    ----------
    config_path: str | None
        The path of the config file.
    parser: argparse.ArgumentParser | None
        The parser.

    Returns
    -------
    argparse.Namespace
        The arguments.
    """
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
        action="version",
        help="""Show version of the program.
        If this is used, all other arguments will be ignored and the program will be closed.""",
        version=f"%(prog)s {__version__}",
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
