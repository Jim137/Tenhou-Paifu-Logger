import urllib.request
import argparse
import re
import os
import sys
from pandas import HDFStore, DataFrame

from paifulogger import __version__
from .src import *

url_reg = r"https?://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d"


def remove_old_paifu(paifu_str: str, format, output):
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
        format = args.format
    else:
        format = "xlsx"

    # if remake, remove old files
    if args.remake:
        paifu_str3 = local_str.paifu + "/" + local_str.sanma + local_str.paifu
        paifu_str4 = local_str.paifu + "/" + local_str.yonma + local_str.paifu
        try:
            if args.all_formats:
                remove_old_paifu(paifu_str3, "html", output)
                remove_old_paifu(paifu_str3, "xlsx", output)
                remove_old_paifu(paifu_str3, "csv", output)
                remove_old_paifu(paifu_str4, "html", output)
                remove_old_paifu(paifu_str4, "xlsx", output)
                remove_old_paifu(paifu_str4, "csv", output)
            else:
                remove_old_paifu(paifu_str3, format, output)
                remove_old_paifu(paifu_str4, format, output)
        except OSError:
            pass

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
            if args.all_formats:
                log_into_html(paifu, local_str, output)
                log_into_xlsx(paifu, local_str, output)
                log_into_csv(paifu, local_str, output)
            elif format == "xlsx":
                log_into_xlsx(paifu, local_str, output)
            elif format == "html":
                log_into_html(paifu, local_str, output)
            elif format == "csv":
                log_into_csv(paifu, local_str, output)
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
        type=str,
        help="Format of the output file. Default is xlsx. Available formats: xlsx, html, csv.",
        choices=["xlsx", "html", "csv"],
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
