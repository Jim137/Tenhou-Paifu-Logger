import urllib.request
import argparse
import re
from src import *

url_reg = r'https://tenhou\.net/\d/\?log=\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d'


def log(args):
    if args.lang:
        lang = args.lang
    else:
        lang = 'en'
    local_str = localized_str(lang)

    urls = []
    if not args.url:
        urls.append(input(local_str.hint_input))
    else:
        urls = args.url

    if args.format:
        format = args.format
    else:
        format = 'xlsx'

    for url in urls:
        if not re.match(url_reg, url):
            print(local_str.hint_url, url)
            continue
        if check_duplicate(url, local_str):
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
    parser.add_argument("--all-formats",
                        action="store_true",
                        help="Output all formats.")
    args = parser.parse_args()
    log(args)
