from datetime import datetime
from typing import cast
import re

import openpyxl as xl
from openpyxl.worksheet.worksheet import Worksheet

from .get_place import get_place
from .i18n import local_str
from .Paifu import Paifu


def log_into_xlsx(paifu: Paifu, local_lang: local_str, output: str):
    try:
        if paifu.player_num == 3:
            paifu_str = local_lang.sanma + local_lang.paifu
        else:
            paifu_str = local_lang.yonma + local_lang.paifu
        path = f"{output}/{local_lang.paifu}/{paifu_str}.xlsx"
        wb = xl.load_workbook(path)
        sheet = cast(Worksheet, wb.active)
        sheet.delete_rows(sheet.max_row)
    except FileNotFoundError:
        wb = xl.Workbook()
        sheet = cast(Worksheet, wb.active)
        sheet.append(
            [
                local_lang.date,
                local_lang.plc,
                local_lang.paifu,
                local_lang.remark,
                local_lang.preR,
            ]
        )
        sheet.column_dimensions["A"].width = 20
        sheet.column_dimensions["C"].width = 71
        sheet.column_dimensions["E"].width = local_lang.excelE
    sheet.append(
        [
            datetime.strptime(re.findall(r"\d{10}", paifu.url)[0], "%Y%m%d%H"),
            get_place(paifu, paifu.ban),
            paifu.url,
            "",
            float(paifu.r[paifu.ban]),
        ]
    )
    sheet["C" + str(sheet.max_row)].style = "Hyperlink"
    sheet.append([local_lang.avg_plc, "=average(B2:B" + str(sheet.max_row) + ")"])
    wb.save(path)
    print(
        "xlsx: "
        + local_lang.hint_record1
        + re.findall(r"\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d", paifu.url)[0]
        + local_lang.hint_record2
    )
    return None
