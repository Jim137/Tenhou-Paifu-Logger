import re
from datetime import datetime
import xml.etree.ElementTree as ET


class Paifu:
    def __init__(self, url: str, root: ET.Element):
        self.url = url
        self.time = datetime.strptime(re.findall(r"\d{10}", self.url)[0], "%Y%m%d%H")
        self.ban = int(url[-1])
        self.root = root

        if gtype := root[1].get("type"):
            self.go_type = int(gtype)
        if owari := root[-1].get("owari"):
            self.owari = owari.split(",")
        if rate := root[2].get("rate"):
            self.r = rate.split(",")

        self.go_type_distinguish()
        self._rounds()
        self.plc = self.get_place(self.ban)
        self.rate_change = self.get_rate_change()

    def go_type_distinguish(self):
        """
        Distinguish the type of the game. And set the go_str and player_num.

        ---

        Examples:
            三鳳南喰赤速 (go_type = 127) -> go_str = '三南喰赤速', player_num = 3

        """

        self.go_str = ""
        if self.go_type & 1:
            # PVP
            pass

        if self.go_type & 16:
            self.go_str += "三"
            self.player_num = 3
        else:
            self.go_str += "四"
            self.player_num = 4

        if self.go_type & 128:
            # 上
            pass

        if self.go_type & 32:
            # 特 or 鳳
            pass

        if self.go_type & 8:
            self.go_str += "南"
        else:
            self.go_str += "東"

        if self.go_type & 4:
            self.go_str += "喰"

        if not self.go_type & 2:
            self.go_str += "赤"

        if self.go_type & 64:
            self.go_str += "速"

    def _rounds(self):
        self.rounds = [[] for _ in range(self.get_round_num() + 1)]
        round_idx = -1
        for el in self.root:
            # Each element has tag: str, attrib: dict, text, tail attributes
            if el.tag == "INIT":
                round_idx += 1
            self.rounds[round_idx].append(el)

    def get_place(self, ban) -> int:
        """
        Return the placing and rate before match
        """
        o0, s0, o1, s1, o2, s2, o3, s3 = self.owari

        if self.player_num == 4:
            sp = [float(s0), float(s1), float(s2), float(s3)]
            placing = [1, 1, 1, 1]
            for i in range(4):
                for j in range(4):
                    if sp[i] < sp[j]:
                        placing[i] += 1
        else:
            sp = [float(s0), float(s1), float(s2)]
            placing = [1, 1, 1]
            for i in range(3):
                for j in range(3):
                    if sp[i] < sp[j]:
                        placing[i] += 1
        return placing[ban]

    def get_rate_change(self) -> float:
        """
        Return the rate change after match.

        Note: Since the rate change has a correction of number of played games. We assumed that player has played over 400 games,
        which the correction is fixed to 0.2.
        """

        if self.player_num == 4:
            dr_result = (30, 10, -10, -30)
            corr = (sum([float(r) for r in self.r]) / 4 - float(self.r[self.ban])) / 40
            return 0.2 * (dr_result[self.plc - 1] + corr)
        else:
            dr_result = (30, 0, -30, 0)
            corr = (sum([float(r) for r in self.r]) / 3 - float(self.r[self.ban])) / 40
            if self.plc == 4:
                assert False, "Sanma has no 4th place."
            return 0.2 * (dr_result[self.plc - 1] + corr)

    def get_round_num(self) -> int:
        """
        Return the total number of rounds
        """
        return len(self.root.findall("INIT"))

    def get_deal_in_num(self, ban) -> int:
        """
        Return the number of deal-in
        """
        agaris = self.root.findall("AGARI")
        count = 0
        for agari in agaris:
            if agari.get("fromWho") == str(ban) and agari.get("who") != str(ban):
                count += 1
        return count

    def get_win_num(self, ban) -> int:
        """
        Return the number of win
        """
        agaris = self.root.findall("AGARI")
        count = 0
        for agari in agaris:
            if agari.get("who") == str(ban):
                count += 1
        return count
