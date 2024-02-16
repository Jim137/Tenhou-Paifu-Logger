import argparse
import urllib.request
import re
import os
import sys
from pandas import HDFStore, DataFrame

from .src import *

url_reg = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"
avaiable_formats = ["xlsx", "html", "csv"]


def remove_old_paifu(paifu_str: str, formats, output) -> None:
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
    """

    for format in formats:
        if os.path.exists(f"{output}/{paifu_str}.{format}"):
            os.remove(f"{output}/{paifu_str}.{format}")
            print(f"{paifu_str}.{format} has been removed.")
    return None


def _get_lang(args: argparse.Namespace):
    """
    Get the localized string.

    If not given, use English.
    """

    if args.lang:
        lang = args.lang
    else:
        lang = "en"
    main_path = os.path.dirname(os.path.abspath(__file__))
    local_lang = localized_str(lang, main_path)
    return local_lang


def _get_output(args: argparse.Namespace) -> str:
    """
    Get output directory from args.output.

    If not given, use current directory "./".
    """

    if args.output:
        output = args.output
    else:
        output = os.path.abspath("./")
    return output


def _get_urls(
    args: argparse.Namespace, local_lang: local_str, output: str
) -> list[str]:
    """
    Get urls from input or args.url.

    If remake, get urls from url_log.h5
    Else if not given args.url, get urls from input.

    Note:
        re.findall(url_reg, url) will return a list of urls that match the regular expression.
    """

    urls = []
    if args.remake:
        store = HDFStore(f"{output}/{local_lang.paifu}/url_log.h5")
        try:
            # Special case: if "url" not in store, add it.
            # It will be deprecated in the future.
            if "url" not in store:
                store["url"] = DataFrame(columns=["url"])
            
            urlstore = store["url"]["url"].values
            for url in urlstore:
                # Special case: if the url does not start with "https://", add it.
                # It will be deprecated in the future.
                if not re.match(url_reg, url):
                    urls.append("https://" + url)
                    continue

                urls.append(url)
        finally:
            store.close()
    elif not args.url:
        for url in re.findall(url_reg, input(local_lang.hint_input)):
            urls.append(url)
    else:
        for url in args.url:
            urls.extend(re.findall(url_reg, url))
    return urls


def _get_formats(args: argparse.Namespace) -> list:
    """
    Get formats from args.format.

    If not given, return ["xlsx"].
    """

    if args.format:
        formats = args.format
    else:
        formats = ["xlsx"]
    return formats


def _remake_log(
    args: argparse.Namespace, local_lang: local_str, output: str, formats: list[str]
) -> None:
    """
    Remake the log file from url_log.h5 (past logging log).
    """

    paifu_str3 = local_lang.paifu + "/" + local_lang.sanma + local_lang.paifu
    paifu_str4 = local_lang.paifu + "/" + local_lang.yonma + local_lang.paifu
    try:
        if args.all_formats:
            remove_old_paifu(paifu_str3, avaiable_formats, output)
            remove_old_paifu(paifu_str4, avaiable_formats, output)
        else:
            remove_old_paifu(paifu_str3, formats, output)
            remove_old_paifu(paifu_str4, formats, output)
    except OSError:
        pass
    return None


def _get_log_func(args: argparse.Namespace, formats: list[str]) -> list:
    """
    Parse the formats and return the corresponding log functions.

    If args.all_formats, return all log functions.
    """

    assert formats, "No format is given."

    if args.all_formats:
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


def _log(
    urls: list[str],
    local_lang: local_str,
    output: str,
    log_formats: list,
    remake: bool = False,
    ignore_duplicated: bool = False,
    mjai: bool = False,
):
    """
    Log the paifu files
    """

    for url in urls:
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
        except OSError:
            print(local_lang.hint_url, url)
        except urllib.error.URLError:
            print(local_lang.hint_url, url)
        except ValueError:
            print(local_lang.hint_tw, url)
    return None


def log(args: argparse.Namespace):
    """
    Parse the arguments and log the paifu files.
    """

    # get version and exit
    if args.version:
        try:
            from paifulogger import __version__
        except ImportError:
            from . import __version__
        print("Tenhou-Paifu-Logger", __version__)
        return None

    local_lang = _get_lang(args)
    output = _get_output(args)
    urls = _get_urls(args, local_lang, output)
    formats = _get_formats(args)

    # if remake, remove old files
    if args.remake:
        _remake_log(args, local_lang, output, formats)

    log_formats = _get_log_func(args, formats)
    _log(
        urls,
        local_lang,
        output,
        log_formats,
        args.remake,
        args.ignore_duplicated,
        args.mjai,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs="*", help="URL of the match.")
    parser.add_argument(
        "-l",
        "--lang",
        type=str,
        help="Language of the program and output files. Default is English. Available languages: English(en), 繁體中文(zh_tw), 简体中文(zh), 日本語(ja).",
    )
    parser.add_argument(
        "-f",
        "--format",
        action="append",
        type=str,
        help="Format of the output file. Default is xlsx. Available formats: xlsx, html, csv.",
        choices=avaiable_formats,
    )
    parser.add_argument(
        "-a", "--all-formats", action="store_true", help="Output all formats."
    )
    parser.add_argument(
        "-r",
        "--remake",
        action="store_true",
        help="Remake the log file from url_log.h5 (past logging log). Use this when the program is updated, changing format or language of the log file, or the log file is missing. Note that this will overwrite the log file.",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Output directory. Default is './'."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show version of the program. If this is used, all other arguments will be ignored and the program will be closed.",
    )
    parser.add_argument("--mjai", action="store_true", help="Output MJAI format paifu.")
    # Args for Debugging
    parser.add_argument(
        "--ignore-duplicated", action="store_true", help=argparse.SUPPRESS
    )
    args = parser.parse_args()
    log(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
