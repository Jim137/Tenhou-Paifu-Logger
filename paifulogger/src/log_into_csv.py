import csv
from datetime import datetime
import re
import os.path

import pandas as pd

from .get_place import get_place
from .i18n import local_str
from .Paifu import Paifu


def log_into_csv(paifu: Paifu, local_lang: local_str, output: str):
    if paifu.player_num == 3:
        paifu_str = local_lang.sanma + local_lang.paifu
    else:
        paifu_str = local_lang.yonma + local_lang.paifu
    path = f"{output}/{local_lang.paifu}/{paifu_str}.csv"
    if os.path.isfile(path):
        csvfile = open(path, "a+", encoding="utf-8")
        writer = csv.writer(csvfile)
    else:
        csvfile = open(path, "w", encoding="utf-8")
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "# id",
                local_lang.date,
                local_lang.plc,
                local_lang.paifu,
                local_lang.preR,
            ]
        )
    try:
        df = pd.read_csv(path, index_col=0, encoding="utf-8")
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=["id", "date", "plc", "paifu", "preR"])
    writer.writerow(
        [
            df.shape[0],
            datetime.strptime(re.findall(r"\d{10}", paifu.url)[0], "%Y%m%d%H"),
            get_place(paifu, paifu.ban),
            paifu.url,
            float(paifu.r[paifu.ban]),
        ]
    )
    print(
        "csv: "
        + local_lang.hint_record1
        + re.findall(r"\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d", paifu.url)[0]
        + local_lang.hint_record2
    )
    csvfile.close()
    return None
