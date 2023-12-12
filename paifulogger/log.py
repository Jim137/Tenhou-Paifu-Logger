import argparse
from functools import partial
import urllib.request
import re
import os
import sys
from pandas import HDFStore, DataFrame

from paifulogger import __version__
from .src import *

url_reg = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"
avaiable_formats = ["xlsx", "html", "csv"]


def remove_old_paifu(paifu_str: str, formats, output):
    for format in formats:
        if os.path.exists(f"{output}/{paifu_str}.{format}"):
            os.remove(f"{output}/{paifu_str}.{format}")
    return None


def log(args):
    # get version and exit
    if args.version:
        print("Tenhou-Paifu-Logger", __version__)
        return None

    # get language
    if args.lang:
        lang = args.lang
    else:
        lang = "en"
    main_path = os.path.dirname(os.path.abspath(__file__))
    local_str = localized_str(lang, main_path)

    # get output directory
    if args.output:
        output = args.output
    else:
        output = os.path.abspath("./")

    # get urls
    urls = []
    if args.remake:
        store = HDFStore(f"{output}/{local_str.paifu}/url_log.h5")
        if "url" not in store:
            store["url"] = DataFrame(columns=["url"])
        urlstore = store["url"]["url"].values
        for url in urlstore:
            if not re.match(url_reg, url):
                urls.append("https://" + url)
                continue
            urls.append(url)
        store.close()
    elif not args.url:
        for url in re.findall(url_reg, input(local_str.hint_input)):
            urls.append(url)
    else:
        urls = args.url

    # get format
    if args.format:
        formats = args.format
    else:
        formats = ["xlsx"]

    # if remake, remove old files
    if args.remake:
        paifu_str3 = local_str.paifu + "/" + local_str.sanma + local_str.paifu
        paifu_str4 = local_str.paifu + "/" + local_str.yonma + local_str.paifu
        try:
            if args.all_formats:
                remove_old_paifu(paifu_str3, avaiable_formats, output)
                remove_old_paifu(paifu_str4, avaiable_formats, output)
            else:
                remove_old_paifu(paifu_str3, formats, output)
                remove_old_paifu(paifu_str4, formats, output)
        except OSError:
            pass

    # Parsing different formats log function
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

    # log
    for url in urls:
        if not re.match(url_reg, url):
            print(local_str.hint_url, url)
            continue
        if args.remake:
            pass
        elif check_duplicate(url, local_str, output) and not args.ignore_duplicated:
            print(local_str.hint_duplicate, url)
            continue
        try:
            paifu = get_paifu(url, local_str, output, args.mjai)
            for log_into_format in log_formats:
                log_into_format(paifu, local_str, output)
            if args.remake:
                pass
            else:
                url_log(url, local_str, output)
        except OSError:
            print(local_str.hint_url, url)
        except urllib.error.URLError:
            print(local_str.hint_url, url)
        except ValueError:
            print(local_str.hint_tw, url)


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
