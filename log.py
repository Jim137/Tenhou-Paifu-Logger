import urllib.request
import argparse
from src import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
    if args.lang:
        lang = args.lang
    else:
        lang = 'en'
    if args.format:
        format = args.format
    else:
        format = 'xlsx'
    local_str = localized_str(lang)

    url = input(local_str.hint_input)
    try:
        paifu = get_paifu(url, local_str)
        if args.all_format:
            log_into_html(paifu, local_str)
            log_into_xlsx(paifu, local_str)
        elif format == 'xlsx':
            log_into_xlsx(paifu, local_str)
        elif format == 'html':
            log_into_html(paifu, local_str)
    except urllib.error.URLError:
        print(local_str.hint_url)
    except ValueError:
        print(local_str.hint_tw)
