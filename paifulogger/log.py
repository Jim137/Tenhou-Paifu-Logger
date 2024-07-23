import argparse
import json
import os
import re
import sys
import urllib.request
import warnings
from typing import Callable

from pandas import DataFrame, HDFStore

from . import __version__, main_path
from .src.config import config_path
from .src.get_paifu import get_paifu, get_paifu_from_client_log, save_mjai
from .src.i18n import LocalStr, localized_str
from .src.log_into_csv import log_into_csv
from .src.log_into_html import log_into_html
from .src.log_into_xlsx import log_into_xlsx
from .src.Paifu import Paifu
from .src.url_log import check_duplicate, url_log

REG_URL = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"
available_formats = ["xlsx", "html", "csv"]


def remove_old_paifu(paifu_str: str, formats: list[str], output: str) -> None:
    """
    Remove old paifu files.

    Parameters
    ----------
    paifu_str : str
        The name of the paifu file.
    formats : list
        The formats of the paifu file.
    output : str
        The output directory.

    Returns
    -------
    None

    Examples
    --------
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


def _get_lang(lang: str | None = None) -> LocalStr:
    """
    Get the localized string.

    If not given, use English.

    Parameters
    ----------
    lang : str
        The language of the program.

    Returns
    -------
    LocalStr
        The localized string.
    """

    return localized_str(lang, main_path) if lang else localized_str("en", main_path)


def _get_output(output: str = "./") -> str:
    """
    Get output directory from args.output.

    If not given, use current directory "./".

    Parameters
    ----------
    output : str
        The output directory.

    Returns
    -------
    str
        The absolute path of the output directory.
    """

    return os.path.abspath(output) if output else os.path.abspath("./")


def _get_urls(
    url: list[str] | None = None,
    local_lang: LocalStr = localized_str("en"),
    output: str = os.path.abspath("./"),
    remake: bool = False,
) -> list[str]:
    """
    Get urls from input or url.

    If remake, get urls from url_log.h5
    Else if not given url, get urls from input.

    Parameters
    ----------
    url : list[str]
        The urls of the paifu files.
    local_lang : LocalStr
        The localized string.
    output : str
        The output directory.
    remake : bool
        Remake the log file from url_log.h5.

    Returns
    -------
    list[str]
        The list of urls.

    Note
    ----
    `re.findall(REG_URL, _url)` will return a list of urls that match the regular expression.
    """

    urls = []
    if remake:
        with HDFStore(f"{output}/{local_lang.paifu}/url_log.h5") as store:
            # ===============================================================
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
            # ===============================================================
            urlstore = store["url"]["url"].values
            for _url in urlstore:
                if not re.match(REG_URL, _url):
                    urls.append("https://" + _url)
                    continue
                urls.append(_url)
    elif not url:
        for _url in re.findall(REG_URL, input(local_lang.hint_input)):
            urls.append(_url)
    else:
        for _url in url:
            urls.extend(re.findall(REG_URL, _url))
    return urls


def _get_formats(format: list[str] | None = None) -> list:
    """
    Get formats from `args.format`.

    If not given, return ["csv"].

    Parameters
    ----------
    format : list
        The formats of the output file.

    Returns
    -------
    list
        The formats of the output file.
    """

    return format if format else ["csv"]


def _remake_log(
    local_lang: LocalStr, output: str, formats: list[str], all_formats: bool = False
) -> None:
    """
    Remake the log file from url_log.h5 (past logging log), and remove old paifu files.

    Parameters
    ----------
    local_lang : LocalStr
        The localized string.
    output : str
        The output directory to remove.
    formats : list
        The formats of the output file.
    all_formats : bool
        Remove all formats.
    """

    paifu_str3 = local_lang.paifu + "/" + local_lang.sanma + local_lang.paifu
    paifu_str4 = local_lang.paifu + "/" + local_lang.yonma + local_lang.paifu
    try:
        if all_formats:
            remove_old_paifu(paifu_str3, available_formats, output)
        else:
            remove_old_paifu(paifu_str3, formats, output)
    except OSError:
        pass
    try:
        if all_formats:
            remove_old_paifu(paifu_str4, available_formats, output)
        else:
            remove_old_paifu(paifu_str4, formats, output)
    except OSError:
        pass
    return None


def get_log_func(formats: list[str], all_formats: bool = False) -> list[Callable]:
    """
    Parse the formats and return the corresponding log functions.

    If `all_formats`, return all log functions.

    Parameters
    ----------
    formats : list
        The formats of the output file.
    all_formats : bool
        Output all formats.

    Returns
    -------
    list
        The list of log functions.
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


def log_paifu_from_local(
    paifus: list[Paifu],
    *,
    log_formats: list[Callable] = [log_into_csv],
    local_lang: LocalStr = localized_str("en", main_path),
    output: str = os.path.abspath("./"),
    ignore_duplicated: bool = False,
    mjai: bool = False,
):
    """
    Log paifu files from local.

    Parameters
    ----------
    paifus : list[Paifu]
        The list of paifu files.
    log_formats : list
        The log functions.
    local_lang : LocalStr
        The localized string.
    output : str
        The output directory.
    ignore_duplicated : bool
        Ignore duplicated urls.
    mjai : bool
        Output MJAI format paifu.

    Returns
    -------
    int
        The return code.
    """

    retcode = 0
    for paifu in paifus:
        try:
            if mjai:
                save_mjai(paifu, output, paifu.name, local_lang)
            if check_duplicate(paifu.url, local_lang, output) and not ignore_duplicated:
                print(local_lang.hint_duplicate, paifu.url)
                continue
            for log_into_format in log_formats:
                log_into_format(paifu, local_lang, output)
            url_log(paifu.url, local_lang, output)
        except OSError:
            print(local_lang.hint_url, paifu.url)
            retcode = 1
        except ValueError:
            print(local_lang.hint_tw, paifu.url)
            retcode = 1
        except KeyError:
            print(
                """Please remake the log file by `plog -f [format] -l [lang] -o [output] -r` first,
                  or `python -m paifulogger plog -f [format] -l [lang] -o [output] -r` manually."""
            )
            return 1
    return retcode


def log_paifu(
    *urls: list[str] | str,
    log_formats: list[Callable] = [log_into_csv],
    local_lang: LocalStr = localized_str("en", main_path),
    output: str = os.path.abspath("./"),
    remake: bool = False,
    ignore_duplicated: bool = False,
    mjai: bool = False,
) -> int:
    """
    Log paifu files.

    Parameters
    ----------
    urls : list
        The urls of the paifu files.
    log_formats : list
        The log functions.
    local_lang : LocalStr
        The localized string.
    output : str
        The output directory.
    remake : bool
        Remake the log file from url_log.h5.
    ignore_duplicated : bool
        Ignore duplicated urls.
    mjai : bool
        Output MJAI format paifu.

    Returns
    -------
    int
        The return code.
    """

    retcode = 0
    _urls: list[str] = []
    for url in urls:
        if isinstance(url, list):
            _urls.extend(url)
        else:
            _urls.append(url)
    for url in _urls:
        if not re.match(REG_URL, url):
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
        except urllib.error.URLError:
            print(local_lang.hint_url, url)
            retcode = 1
        except OSError:
            print(local_lang.hint_url, url)
            retcode = 1
        except ValueError:
            print(local_lang.hint_tw, url)
            retcode = 1
        except KeyError:
            print(
                """Please remake the log file by `plog -f [format] -l [lang] -o [output] -r`,
                  or `python -m paifulogger plog -f [format] -l [lang] -o [output] -r` manually."""
            )
            return 1
    return retcode


def log(args: argparse.Namespace) -> int:
    """
    Parse the arguments and log paifu files.

    Parameters
    ----------
    args : argparse.Namespace
        The arguments from the command line.

    Returns
    -------
    int
        The return code.
    """

    local_lang = _get_lang(args.lang)
    output = _get_output(args.output)
    formats = _get_formats(args.format)

    # if remake, remove old files
    if args.remake:
        _remake_log(local_lang, output, formats, args.all_formats)

    log_formats = get_log_func(formats, args.all_formats)

    if args.from_client:
        paifus = get_paifu_from_client_log(args.from_client)
        if not paifus:
            print("No paifu files found.")
            return 0
        print(f"Found {len(paifus)} paifu files.")
        return log_paifu_from_local(
            paifus,
            log_formats=log_formats,
            local_lang=local_lang,
            output=output,
            ignore_duplicated=args.ignore_duplicated,
            mjai=args.mjai,
        )

    urls = _get_urls(args.url, local_lang, output, args.remake)
    return log_paifu(
        urls,
        log_formats=log_formats,
        local_lang=local_lang,
        output=output,
        remake=args.remake,
        ignore_duplicated=args.ignore_duplicated,
        mjai=args.mjai,
    )


def log_parser(
    config_path: str | None = None, parser: argparse.ArgumentParser | None = None
) -> argparse.Namespace:
    """
    Parse the arguments from the command line.

    Parameters
    ----------
    config_path : str
        The path of the config file.
    parser : argparse.ArgumentParser
        The argument parser.

    Returns
    -------
    argparse.Namespace
        The arguments from the command line.
    """

    config = {}
    if config_path and os.path.exists(f"{config_path}/config.json"):
        with open(f"{config_path}/config.json", "r") as f:
            config = json.load(f)

    if parser is None:
        parser = argparse.ArgumentParser(description="Paifu Logger", prog="PaifuLogger")
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
        choices=available_formats,
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
    parser.add_argument(
        "-c",
        "--from-client",
        nargs="+",
        help="Log client saved paifu (*.mjlog) from given directory.",
        type=str,
    )
    # Args for Debugging
    parser.add_argument(
        "--ignore-duplicated",
        action="store_true",
        help=argparse.SUPPRESS,
        default=config.get("ignore_duplicated", False),
    )
    args = parser.parse_args()
    if "plog" in args.url:
        args.url.remove("plog")
    return args


def main(plog_parser: argparse.ArgumentParser | None = None):
    args = log_parser(config_path(), plog_parser)
    return log(args)


if __name__ == "__main__":
    sys.exit(main())
