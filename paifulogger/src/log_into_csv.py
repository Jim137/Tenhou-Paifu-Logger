from datetime import datetime
import re

from .get_place import get_place
from .Paifu import Paifu
from .i18n import local_str

def log_into_csv(paifu: Paifu, local_str: local_str, output: str):
    try:
        if paifu.player_num == 3:
            paifu_str = local_str.sanma + local_str.paifu
        else:
            paifu_str = local_str.yonma + local_str.paifu
        path = f"{output}/{local_str.paifu}/{paifu_str}.csv"
    except FileNotFoundError:
        pass