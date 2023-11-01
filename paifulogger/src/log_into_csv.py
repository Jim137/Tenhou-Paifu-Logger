import csv
from datetime import datetime
import re
import os.path
import pandas as pd

from .get_place import get_place
from .Paifu import Paifu
from .i18n import local_str


def log_into_csv(paifu: Paifu, local_str: local_str, output: str):
    if paifu.player_num == 3:
        paifu_str = local_str.sanma + local_str.paifu
    else:
        paifu_str = local_str.yonma + local_str.paifu
    path = f"{output}/{local_str.paifu}/{paifu_str}.csv"
    if os.path.isfile(path):
        csvfile = open(path, "a+")
        writer = csv.writer(csvfile)
    else:
        csvfile = open(path, "w")
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "# id",
                local_str.date,
                local_str.plc,
                local_str.paifu,
                local_str.preR,
            ]
        )
    df = pd.read_csv(path, index_col=0)
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
        + local_str.hint_record1
        + re.findall(r"\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d", paifu.url)[0]
        + local_str.hint_record2
    )
    csvfile.close()
    return None
