import csv
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
        csvfile = open(path, "a+")
        writer = csv.writer(csvfile)
    except FileNotFoundError:
        csvfile = open(path, "w")
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                local_str.date,
                local_str.plc,
                local_str.paifu,
                local_str.remark,
                local_str.preR,
            ]
        )
    writer.writerow(
        [
            datetime.strptime(re.findall(r"\d{10}", paifu.url)[0], "%Y%m%d%H"),
            get_place(paifu, paifu.ban),
            paifu.url,
            "",
            float(paifu.r[paifu.ban]),
        ]
    )
    return None
