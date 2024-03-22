import argparse
import json
from typing import Callable
import urllib.request
import re
import os
import sys
import warnings

from pandas import HDFStore, DataFrame
from platformdirs import user_data_dir

from .src.get_paifu import get_paifu
from .src.i18n import localized_str, local_str
from .src.log_into_csv import log_into_csv
from .src.log_into_xlsx import log_into_xlsx
from .src.log_into_html import log_into_html
from .src.url_log import url_log, check_duplicate


url_reg = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"
avaiable_formats = ["xlsx", "html", "csv"]


def remove_old_paifu(paifu_str: str, formats: list[str], output: str) -> None:
    """
    Remove old paifu files.

    Args:
        paifu_str: str
            The name of the paifu file.
        formats: list
            The formats of the paifu file.
        output: str
            The output directory.

    Returns:
        None

    ---

    Examples:
        >>> remove_old_paifu("paifu", ["xlsx", "html", "csv"], "./")
        paifu.xlsx has been removed.
        paifu.html has been removed.
        paifu.csv has been removed.
    """

    for format in formats:
        if os.path.exists(f"{output}/{paifu_str}.{format}"):
            os.remove(f"{output}/{paifu_str}.{format}")
            print(f"{paifu_str}.{format} has been removed.")
    return None


def _get_lang(lang: str | None = None) -> local_str:
    """
    Get the localized string.

    If not given, use English.
    """

    if lang:
        _lang = lang
    else:
        _lang = "en"
    main_path = os.path.dirname(os.path.abspath(__file__))
    local_lang = localized_str(_lang, main_path)
    return local_lang


def _get_output(output: str = "./") -> str:
    """
    Get output directory from args.output.

    If not given, use current directory "./".
    """

    if output:
        _output = os.path.abspath(output)
    else:
        _output = os.path.abspath("./")
    return _output


def _get_urls(
    url: list[str] | None = None,
    local_lang: local_str = local_str("en", os.path.dirname(os.path.abspath(__file__))),
    output: str = os.path.abspath("./"),
    remake: bool = False,
) -> list[str]:
    """
    Get urls from input or url.

    If remake, get urls from url_log.h5
    Else if not given url, get urls from input.

    Note:
        `re.findall(url_reg, _url)` will return a list of urls that match the regular expression.
    """

    urls = []
    if remake:
        with HDFStore(f"{output}/{local_lang.paifu}/url_log.h5") as store:
            ############################################################
            # Special case: if "url" not in store, add it.
            # It will be deprecated in the future.
            if "url" not in store:
                store["url"] = DataFrame(columns=["url"])
                warnings.warn(
                    """The url_log.h5 you used is deprecated. 
                    You have to manually copy all urls and delete url_log.h5,
                    then run and paste the urls to the program. 
                    The new url_log.h5 will be automatically created.
                    """,
                    DeprecationWarning,
                )
            ############################################################
            urlstore = store["url"]["url"].values
            for _url in urlstore:
                if not re.match(url_reg, _url):
                    urls.append("https://" + _url)
                    continue
                urls.append(_url)
    elif not url:
        for _url in re.findall(url_reg, input(local_lang.hint_input)):
            urls.append(_url)
    else:
        for _url in url:
            urls.extend(re.findall(url_reg, _url))
    return urls


def _get_formats(format: list[str] | None = None) -> list:
    """
    Get formats from `args.format`.

    If not given, return ["csv"].
    """

    if format:
        formats = format
    else:
        formats = ["csv"]
    return formats


def _remake_log(
    local_lang: local_str, output: str, formats: list[str], all_formats: bool = False
) -> None:
    """
    Remake the log file from url_log.h5 (past logging log), and remove old paifu files.
    """

    paifu_str3 = local_lang.paifu + "/" + local_lang.sanma + local_lang.paifu
    paifu_str4 = local_lang.paifu + "/" + local_lang.yonma + local_lang.paifu
    try:
        if all_formats:
            remove_old_paifu(paifu_str3, avaiable_formats, output)
            remove_old_paifu(paifu_str4, avaiable_formats, output)
        else:
            remove_old_paifu(paifu_str3, formats, output)
            remove_old_paifu(paifu_str4, formats, output)
    except OSError:
        pass
    return None


def _get_log_func(formats: list[str], all_formats: bool = False) -> list[Callable]:
    """
    Parse the formats and return the corresponding log functions.

    If `all_formats`, return all log functions.
    """

    assert formats, "No format is given."

    if all_formats:
        log_formats = [
            log_into_xlsx,
            log_into_html,
            log_into_csv,
        ]
    else:
        log_formats = []
        if "xlsx" in formats:
            log_formats.append(log_into_xlsx)
        if "html" in formats:
            log_formats.append(log_into_html)
        if "csv" in formats:
            log_formats.append(log_into_csv)
    return log_formats


def log_paifu(
    *urls: list[str] | str,
    log_formats: list[Callable] = [log_into_csv],
    local_lang: local_str = local_str("en", os.path.dirname(os.path.abspath(__file__))),
    output: str = os.path.abspath("./"),
    remake: bool = False,
    ignore_duplicated: bool = False,
    mjai: bool = False,
) -> int:
    """
    Log paifu files.

    Args:
        urls: list[str]
            The urls of the paifu files.
        log_formats: list
            The list of log functions.
        local_lang: local_str
            The localized string.
        output: str
            The output directory.
        remake: bool
            Remake the log file from url_log.h5.
        ignore_duplicated: bool
            Ignore duplicated urls.
        mjai: bool
            Output MJAI format paifu.

    Returns:
        int
    """

    retCode = [0]
    _urls: list[str] = []
    for url in urls:
        if isinstance(url, list):
            _urls.extend(url)
        else:
            _urls.append(url)
    for url in _urls:
        if not re.match(url_reg, url):
            print(local_lang.hint_url, url)
            continue
        if remake:
            pass
        elif check_duplicate(url, local_lang, output) and not ignore_duplicated:
            print(local_lang.hint_duplicate, url)
            continue
        try:
            paifu = get_paifu(url, local_lang, output, mjai)
            for log_into_format in log_formats:
                log_into_format(paifu, local_lang, output)
            if remake:
                pass
            else:
                url_log(url, local_lang, output)
            retCode.append(0)
        except urllib.error.URLError:
            print(local_lang.hint_url, url)
            retCode.append(1)
        except OSError:
            print(local_lang.hint_url, url)
            retCode.append(1)
        except ValueError:
            print(local_lang.hint_tw, url)
            retCode.append(1)
    return max(retCode)


def log(args: argparse.Namespace) -> int:
    """
    Parse the arguments and log paifu files.
    """

    # get version and exit
    if args.version:
        try:
            from paifulogger import __version__
        except ImportError:
            from . import __version__
        print("Tenhou-Paifu-Logger", __version__)
        return 0

    local_lang = _get_lang(args.lang)
    output = _get_output(args.output)
    urls = _get_urls(args.url, local_lang, output, args.remake)
    formats = _get_formats(args.format)

    # if remake, remove old files
    if args.remake:
        _remake_log(local_lang, output, formats, args.all_formats)

    log_formats = _get_log_func(formats, args.all_formats)
    return log_paifu(
        urls,
        log_formats=log_formats,
        local_lang=local_lang,
        output=output,
        remake=args.remake,
        ignore_duplicated=args.ignore_duplicated,
        mjai=args.mjai,
    )


def log_parser(config_path: str | None = None) -> argparse.Namespace:
    """
    Parse the arguments from the command line.

    Args:
        config_path: str
            The path of the config file.

    Returns:
        argparse.Namespace
    """

    config = {}
    if config_path and os.path.exists(f"{config_path}/config.json"):
        with open(f"{config_path}/config.json", "r") as f:
            config = json.load(f)

    parser = argparse.ArgumentParser()
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
        "-f",
        "--format",
        action="append",
        type=str,
        help="Format of the output file. Default is csv. Available formats: xlsx, html, csv.",
        choices=avaiable_formats,
        default=config.get("format", None),
    )
    parser.add_argument(
        "-a",
        "--all-formats",
        action="store_true",
        help="Output all formats.",
        default=config.get("all_formats", False),
    )
    parser.add_argument(
        "-r",
        "--remake",
        action="store_true",
        help="""Remake the log file from url_log.h5 (past logging log). 
        Use this when the program is updated, changing format or language of the log file, or the log file is missing. 
        Note that this will overwrite the log file.""",
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
    # Args for Debugging
    parser.add_argument(
        "--ignore-duplicated",
        action="store_true",
        help=argparse.SUPPRESS,
        default=config.get("ignore_duplicated", False),
    )
    args = parser.parse_args()
    return args


def config_path() -> str | None:
    """
    Try to get the path of the config file from current directory or user_data_dir.
    """

    appname = "paifulogger"
    appauthor = "Jim137"
    user_data_dir(appname, appauthor)
    if os.path.exists(f"./config.json"):
        return "."
    elif os.path.exists(f"{user_data_dir(appname, appauthor)}/config.json"):
        return user_data_dir(appname, appauthor)
    else:
        return None


def main():
    args = log_parser(config_path())
    return log(args)


if __name__ == "__main__":
    sys.exit(main())
