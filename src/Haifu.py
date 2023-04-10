import xml.etree.ElementTree as ET

class Haifu():
    def __init__(self, ban: int, root: ET.Element):
        self.ban = ban
        self.owari = root[-1].get('owari').split(',')
        self.r = root[2].get('rate').split(',')