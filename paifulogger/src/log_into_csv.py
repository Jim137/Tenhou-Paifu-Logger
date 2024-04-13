import csv
import re
import os.path
import pandas.errors
from pandas import read_csv, DataFrame
from datetime import datetime

from .i18n import LocalStr
from .Paifu import Paifu


def log_into_csv(paifu: Paifu, local_lang: LocalStr, output: str):
    if paifu.player_num == 3:
        paifu_str = local_lang.sanma + local_lang.paifu
    else:
        paifu_str = local_lang.yonma + local_lang.paifu
    path = f"{output}/{local_lang.paifu}/{paifu_str}.csv"
    if os.path.isfile(path):
        csvfile = open(path, "a+", encoding="utf-8")
        writer = csv.writer(csvfile)
    else:
        # Create a new csv file
        csvfile = open(path, "w", encoding="utf-8")
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "# id",
                local_lang.date,
                local_lang.plc,
                local_lang.paifu,
                local_lang.preR,
                local_lang.r_change,
                local_lang.round_num,
                local_lang.win,
                local_lang.deal_in,
            ]
        )
    try:
        try:
            # Read the csv file
            df = read_csv(path, index_col=0, encoding="utf-8")
        except pandas.errors.EmptyDataError:
            # If the csv file is empty, create a new DataFrame
            df = DataFrame(
                columns=[
                    "id",
                    "date",
                    "plc",
                    "paifu",
                    "preR",
                    "r_change",
                    "round_num",
                    "win",
                    "deal_in",
                ]
            )
        # Append new paifu data to the csv file
        writer.writerow(
            [
                df.shape[0],
                datetime.strptime(re.findall(r"\d{10}", paifu.url)[0], "%Y%m%d%H"),
                paifu.get_place(paifu.ban),
                paifu.url,
                float(paifu.r[paifu.ban]),
                paifu.rate_change,
                paifu.get_round_num(),
                paifu.get_win_num(paifu.ban),
                paifu.get_deal_in_num(paifu.ban),
            ]
        )
        print(
            "csv: "
            + local_lang.hint_record1
            + re.findall(r"\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d", paifu.url)[0]
            + local_lang.hint_record2
        )
    finally:
        csvfile.close()
    return None
