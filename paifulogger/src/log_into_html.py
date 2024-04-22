import io
import re

import pandas as pd

from .i18n import LocalStr
from .Paifu import Paifu


class PaifuHtml:
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
            self.replay = html_str.split("</body>")[1].split("</html>")[0]
        self.end = "</body></html>"
        pass

    def __repr__(self) -> str:
        return self.logged + self.new_log + self.end_table + self.replay + self.end

    def create_html(self, paifu_str, local_lang: LocalStr) -> None:
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
            <script>
                if (window.localStorage) {{
                    var p = document.querySelector('#persisted-text');
                    if (localStorage.text == null) {{
                        localStorage.text = p.value;
                    }} else {{
                        p.value = localStorage.text;
                    }}
                    p.addEventListener('keyup', function(){{ localStorage.text = p.value; }}, false);
                }}
            </script>
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
                        <th>{local_lang.r_change}</th>
                        <th>{local_lang.round_num}</th>
                        <th>{local_lang.win}</th>
                        <th>{local_lang.deal_in}</th>
                    </tr>
                </thead>
                <tbody>
        """

    def log_into_table(self, paifu: Paifu) -> None:
        self.new_log += f"""
                    <tr>
                        <td>{paifu.time}</td>
                        <td>{paifu.get_place(paifu.ban)}</td>
                        <td><a href="{paifu.url}">{paifu.url}</a></td>
                        <td><textarea id="persisted-text"></textarea></td>
                        <td>{paifu.r[paifu.ban]}</td>
                        <td>{paifu.rate_change:.03f}</td>
                        <td>{paifu.get_round_num()}</td>
                        <td>{paifu.get_win_num(paifu.ban)}</td>
                        <td>{paifu.get_deal_in_num(paifu.ban)}</td>
                    </tr>
        """

    def _retrieve(self, local_lang: LocalStr) -> tuple[int, float, float, float]:
        """
        Retrieve the data from the html table.
        """

        pseudo_html = (
            self.logged
            + self.new_log
            + """
                </tbody>
            </table>
        </body>
        </html>"""
        )
        wrapper = io.StringIO(pseudo_html)
        df = pd.read_html(wrapper)[0]
        logged_num = df.shape[0] - 1
        avg_plc = df[f"{local_lang.plc}"].mean()
        win_rate = df[f"{local_lang.win}"].sum() / df[f"{local_lang.round_num}"].sum()
        deal_in_rate = (
            df[f"{local_lang.deal_in}"].sum() / df[f"{local_lang.round_num}"].sum()
        )
        return logged_num, avg_plc, win_rate, deal_in_rate

    def end_of_table(self, local_lang: LocalStr) -> None:
        logged_num, avg_plc, win_rate, deal_in_rate = self._retrieve(local_lang)
        self.end_table += f"""
                </tbody>
            </table>
            <p>{local_lang.log_num} = {logged_num}</p>
            <p>{local_lang.avg_plc} = {avg_plc:.2}</p>
            <p>{local_lang.win_rate} = {win_rate:.3%}</p>
            <p>{local_lang.deal_in_rate} = {deal_in_rate:.3%}</p>
        """


def log_into_html(paifu: Paifu, local_lang: LocalStr, output: str):
    if paifu.player_num == 3:
        paifu_str = local_lang.sanma + local_lang.paifu
    else:
        paifu_str = local_lang.yonma + local_lang.paifu
    path = f"{output}/{local_lang.paifu}/{paifu_str}.html"
    try:
        with open(path, "r", encoding="utf-8") as f:
            html_str = f.read()
        html_c = PaifuHtml(html_str, paifu_str, local_lang)
    except FileNotFoundError:
        html_c = PaifuHtml("", paifu_str, local_lang)
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
