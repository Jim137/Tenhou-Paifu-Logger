import urllib.request
import sys
from src import *


if __name__ == '__main__':
    if len(sys.argv) > 1:
        lang = sys.argv[1]
    else:
        lang = 'en'
    local_str = localized_str(lang)

    url = input(local_str.hint_input)
    try:
        paifu = get_paifu(url, local_str)
        log_into_xlsx(paifu, local_str)
    except urllib.error.URLError:
        print(local_str.hint_url)
    except ValueError:
        print(local_str.hint_tw)
