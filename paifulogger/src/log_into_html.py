from datetime import datetime
import io
import re
from pandas import read_html
from .get_place import get_place
from .Paifu import Paifu
from .i18n import local_str


def create_html(html_str, paifu_str, local_str: local_str):
    html_str += f"""<!DOCTYPE html>
    <html lang={local_str.lang}>
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
                    <th>{local_str.date}</th>
                    <th>{local_str.plc}</th>
                    <th>{local_str.paifu}</th>
                    <th>{local_str.remark}</th>
                    <th>{local_str.preR}</th>
                </tr>
            </thead>
            <tbody>
    """
    return html_str


def log_into_table(html_str, paifu: Paifu, local_str: local_str):
    time_str = datetime.strptime(re.findall(r"\d{10}", paifu.url)[0], "%Y%m%d%H")
    html_str += f"""
                <tr>
                    <td>{time_str}</td>
                    <td>{get_place(paifu, paifu.ban)}</td>
                    <td><a href="{paifu.url}">{paifu.url}</a></td>
                    <td><textarea id="persisted-text"></textarea></td>
                    <td>{float(paifu.r[paifu.ban])}</td>
                </tr>
    """
    return html_str


def average_plc(html_str, local_str: local_str):
    html_p = (
        html_str
        + """
            </tbody>
        </table>
    </body>
    </html>
    """
    )
    wrapper = io.StringIO(html_p)
    df = read_html(wrapper)[0]
    avg_plc = df[f"{local_str.plc}"].mean()
    return avg_plc


def end_of_table(html_str, avg_plc, local_str: local_str):
    html_str += (
        f"""
            </tbody>
        </table>
        <p>{local_str.avg_plc} = {avg_plc}</p>
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
    </html>
    """
    )
    return html_str


def clear_end(html_str):
    html_str = html_str.split("</table>")[0]
    return html_str


def log_into_html(paifu: Paifu, local_str: local_str, output: str):
    if paifu.player_num == 3:
        paifu_str = local_str.sanma + local_str.paifu
    else:
        paifu_str = local_str.yonma + local_str.paifu
    path = f"{output}/{local_str.paifu}/{paifu_str}.html"
    try:
        with open(path, "r", encoding="utf-8") as f:
            html_str = f.read()
        html_str = clear_end(html_str)
    except FileNotFoundError:
        html_str = ""
        html_str = create_html(html_str, paifu_str, local_str)
    html_str = log_into_table(html_str, paifu, local_str)
    html_str = end_of_table(html_str, average_plc(html_str, local_str), local_str)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_str)
    print(
        "html: "
        + local_str.hint_record1
        + re.findall(r"\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d", paifu.url)[0]
        + local_str.hint_record2
    )
    return None
