import io
import re
from datetime import datetime

import pandas as pd

from .i18n import LocalStr
from .Paifu import Paifu


class html:
    def __init__(self, html_str: str, paifu_str, local_lang: LocalStr):
        if html_str.split("</tbody>")[0] == "":
            self.logged = ""
            self.create_html(paifu_str, local_lang)
        else:
            self.logged = html_str.split("</tbody>")[0]
        self.new_log = ""
        self.end_table = ""
        if html_str.split("</body>")[0] == "":
            self.replay = ""
        elif len(html_str.split("</body>")) < 2:
            self.replay = ""
        else:
            self.replay = html_str.split("</body>")[1]
        self.end = "</body></html>"
        pass

    def __repr__(self) -> str:
        return self.logged + self.new_log + self.end_table + self.replay + self.end

    def create_html(self, paifu_str, local_lang: LocalStr):
        self.logged += f"""<!DOCTYPE html>
        <html lang={local_lang.lang}>
        <head>
            <meta charset="utf-8">
            <title>{paifu_str}</title>
            <style>
                table {{
                    border-collapse: collapse;
                }}
                table, th, td {{
                    border: 1px solid black;
                }}
                th, td {{
                    padding: 5px;
                }}
                th {{
                    text-align: left;
                }}
            </style>
        </head>
        <body>
            <table style="width:100%">
                <thead>
                    <tr>
                        <th>{local_lang.date}</th>
                        <th>{local_lang.plc}</th>
                        <th>{local_lang.paifu}</th>
                        <th>{local_lang.remark}</th>
                        <th>{local_lang.preR}</th>
                    </tr>
                </thead>
                <tbody>
        """

    def log_into_table(self, paifu: Paifu):
        time_str = datetime.strptime(re.findall(r"\d{10}", paifu.url)[0], "%Y%m%d%H")
        self.new_log += f"""
                    <tr>
                        <td>{time_str}</td>
                        <td>{paifu.get_place(paifu.ban)}</td>
                        <td><a href="{paifu.url}">{paifu.url}</a></td>
                        <td><textarea id="persisted-text"></textarea></td>
                        <td>{float(paifu.r[paifu.ban])}</td>
                    </tr>
        """

    def average_plc(self, local_lang: LocalStr):
        html_p = (
            self.logged
            + self.new_log
            + """
                    </tbody>
                </table>
            </body>
            </html>
        """
        )
        wrapper = io.StringIO(html_p)
        df = pd.read_html(wrapper)[0]
        avg_plc = df[f"{local_lang.plc}"].mean()
        return avg_plc

    def end_of_table(self, local_lang: LocalStr):
        self.end_table += (
            f"""
                </tbody>  
            </table>
            <p>{local_lang.avg_plc} = {self.average_plc(local_lang)}</p>
            """
            + """
            <script>
                if (window.localStorage) {
                    var p = document.querySelector('#persisted-text');
                    if (localStorage.text == null) {
                        localStorage.text = p.value;
                    } else {
                        p.value = localStorage.text;
                    }
                    p.addEventListener('keyup', function(){ localStorage.text = p.value; }, false);
                }
            </script>
        </body>
        """
        )


def log_into_html(paifu: Paifu, local_lang: LocalStr, output: str):
    if paifu.player_num == 3:
        paifu_str = local_lang.sanma + local_lang.paifu
    else:
        paifu_str = local_lang.yonma + local_lang.paifu
    path = f"{output}/{local_lang.paifu}/{paifu_str}.html"
    try:
        with open(path, "r", encoding="utf-8") as f:
            html_str = f.read()
        html_c = html(html_str, paifu_str, local_lang)
    except FileNotFoundError:
        html_c = html("", paifu_str, local_lang)
    html_c.log_into_table(paifu)
    html_c.end_of_table(local_lang)
    with open(path, "w", encoding="utf-8") as f:
        f.write(repr(html_c))
    print(
        "html: "
        + local_lang.hint_record1
        + re.findall(r"\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d", paifu.url)[0]
        + local_lang.hint_record2
    )
    return None
