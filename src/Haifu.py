import xml.etree.ElementTree as ET


class Haifu():
    def __init__(self, url: str, root: ET.Element):
        self.url = url
        self.ban = int(url[-1])
        self.root = root

        self.go_type = int(root[1].get('type'))
        self.owari = root[-1].get('owari').split(',')
        self.r = root[2].get('rate').split(',')

        self.go_type_distinguish()

    def go_type_distinguish(self):
        self.go_str = ''
        if self.go_type & 1:
            # PVP
            pass

        if self.go_type & 16:
            self.go_str += '三'
            self.player_num = 3
        else:
            self.go_str += '四'
            self.player_num = 4

        if self.go_type & 128:
            # 上
            pass

        if self.go_type & 32:
            # 特 or 鳳
            pass

        if self.go_type & 8:
            self.go_str += '南'
        else:
            self.go_str += '東'

        if self.go_type & 4:
            self.go_str += '喰'

        if not self.go_type & 2:
            self.go_str += '赤'

        if self.go_type & 64:
            self.go_str += '速'
