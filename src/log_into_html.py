from datetime import datetime
import re
import pandas as pd
from .get_place import get_place
from .Paifu import Paifu
from .local import local_str


class html():
    def __init__(self, html_str: str, paifu_str, local_str: local_str):
        if html_str.split('</tbody>')[0] == '':
            self.logged = ''
            self.create_html(paifu_str, local_str)
        else:
            self.logged = html_str.split('</tbody>')[0]
        self.new_log = ''
        self.end_table = ''
        if html_str.split('</body>') [0] == '':
            self.replay = ''
        elif len(html_str.split('</body>')) < 2:
            self.replay = ''
        else:
            self.replay = html_str.split('</body>')[1]
        self.end = '</body></html>'
        pass

    def __repr__(self) -> str:
        return self.logged + self.new_log + self.end_table + self.replay + self.end

    def create_html(self, paifu_str, local_str: local_str):
        self.logged += f'''<!DOCTYPE html>
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
        '''

    def log_into_table(self, paifu: Paifu):
        time_str = datetime.strptime(re.findall(
            r'\d{10}', paifu.url)[0], "%Y%m%d%H")
        self.new_log += f'''
                    <tr>
                        <td>{time_str}</td>
                        <td>{get_place(paifu, paifu.ban)}</td>
                        <td><a href="{paifu.url}">{paifu.url}</a></td>
                        <td><textarea id="persisted-text"></textarea></td>
                        <td>{float(paifu.r[paifu.ban])}</td>
                    </tr>
        '''

    def average_plc(self, local_str: local_str):
        html_p = self.logged + self.new_log +'''
                </tbody>    
            </table>
        </body>
        </html>
        '''
        
        df = pd.read_html(html_p)[0]
        avg_plc = df[f'{local_str.plc}'].mean()
        return avg_plc


    def end_of_table(self, local_str: local_str):
        self.end_table += f'''
                </tbody>  
            </table>
            <p>{local_str.avg_plc} = {self.average_plc(local_str)}</p>
            '''+'''
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
        '''


def log_into_html(paifu: Paifu, local_str: local_str):
    if paifu.player_num == 3:
        paifu_str = local_str.sanma + local_str.paifu
    else:
        paifu_str = local_str.yonma + local_str.paifu
    try:
        with open(f'./{local_str.paifu}/{paifu_str}.html', 'r', encoding='utf-8') as f:
            html_str = f.read()
        html_c = html(html_str, paifu_str, local_str)
    except FileNotFoundError:
        html_c = html('', paifu_str, local_str)
    html_c.log_into_table(paifu)
    html_c.end_of_table(local_str)
    with open(f'./{local_str.paifu}/{paifu_str}.html', 'w', encoding='utf-8') as f:
        f.write(repr(html_c))
    print('html: '+local_str.hint_record1 +
          re.findall(r'\d{10}gm-\w{4}-\w{4}-\w{8}&tw=\d', paifu.url)[0]+local_str.hint_record2)
    return None
