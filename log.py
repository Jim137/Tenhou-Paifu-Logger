import urllib.request
import argparse
import re
import os
from pandas import HDFStore, DataFrame
from src import *

url_reg = r'https://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d'


def log(args):

    # get language
    if args.lang:
        lang = args.lang
    else:
        lang = 'en'
    local_str = localized_str(lang)

    # get urls
    urls = []
    if args.remake:
        store = HDFStore(f'./{local_str.paifu}/url_log.h5')
        if 'url' not in store:
            store['url'] = DataFrame({'url': ['']})
        urls = store['url']['url'].values
        store.close()
    elif not args.url:
        urls.append(input(local_str.hint_input))
    else:
        urls = args.url

    # get format
    if args.format:
        format = args.format
    else:
        format = 'xlsx'

    # if remake, remove old files
    if args.remake:
        try:
            if args.all_formats:
                os.remove(f'./{local_str.paifu}/{local_str.paifu}.xlsx')
                os.remove(f'./{local_str.paifu}/{local_str.paifu}.html')
            else:
                os.remove(f'./{local_str.paifu}/{local_str.paifu}.{format}')
        except OSError:
            pass

    # log
    for url in urls:
        if not re.match(url_reg, url):
            print(local_str.hint_url, url)
            continue
        if args.remake:
            pass
        elif check_duplicate(url, local_str):
            print(local_str.hint_duplicate, url)
            continue
        try:
            paifu = get_paifu(url, local_str)
            if args.all_formats:
                log_into_html(paifu, local_str)
                log_into_xlsx(paifu, local_str)
            elif format == 'xlsx':
                log_into_xlsx(paifu, local_str)
            elif format == 'html':
                log_into_html(paifu, local_str)
            if args.remake:
                pass
            else:
                url_log(url, local_str)
        except urllib.error.URLError:
            print(local_str.hint_url, url)
        except ValueError:
            print(local_str.hint_tw, url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url",
                        nargs='*',
                        help="URL of the match.")
    parser.add_argument("-l",
                        "--lang",
                        type=str,
                        help="Language of the program and output files. Default is English. Available languages: English(en), 繁體中文(zh_tw).")
    parser.add_argument("-f",
                        "--format",
                        type=str,
                        help="Format of the output file. Default is xlsx. Available formats: xlsx, html.")
    parser.add_argument("-a",
                        "--all-formats",
                        action="store_true",
                        help="Output all formats.")
    parser.add_argument("-r",
                        "--remake",
                        action="store_true",
                        help="Remake the log file from url_log.h5 (past logging log). Use this when the program is updated, changing format or language of the log file, or the log file is missing. Note that this will overwrite the log file.")
    args = parser.parse_args()
    log(args)
