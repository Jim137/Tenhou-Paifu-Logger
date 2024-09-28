from datetime import datetime
import xml.etree.ElementTree as ET

class Paifu:
    url: str
    name: str
    time: datetime
    ban: int
    root: ET.Element
    go_type: int
    owari: list[str]
    r: list[str]
    plc: int
    rate_change: list[str]
    go_str: str
    player_num: int
    rounds: list[list[ET.Element]]
    def __init__(self, url: str, root: ET.Element) -> None: ...
    def go_type_distinguish(self) -> None: ...
    def get_place(self, ban) -> int: ...
    def get_rate_change(self) -> float: ...
    def get_round_num(self) -> int: ...
    def get_deal_in_num(self, ban) -> int: ...
    def get_win_num(self, ban) -> int: ...
