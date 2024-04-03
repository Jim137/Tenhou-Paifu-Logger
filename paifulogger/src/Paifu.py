import xml.etree.ElementTree as ET


class Paifu:
    def __init__(self, url: str, root: ET.Element):
        self.url = url
        self.ban = int(url[-1])
        self.root = root

        if gtype := root[1].get("type"):
            self.go_type = int(gtype)
        if owari := root[-1].get("owari"):
            self.owari = owari.split(",")
        if rate := root[2].get("rate"):
            self.r = rate.split(",")

        self.go_type_distinguish()

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

    def get_place(self, ban):
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
