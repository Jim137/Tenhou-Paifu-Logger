from .local_str import local_str
class zh_tw(local_str):
    def __init__(self):
        self.hint_input = '請輸入牌譜網址:'
        self.haifu = '牌譜'
        self.date = '日期'
        self.plc = '順位'
        self.remark = '備註'
        self.preR = '對局前R值'
        self.avg_plc = '平順'
        self.hint_record1 = '已將'
        self.hint_record2 = '牌譜記錄\n'
        self.hint_url = '請檢查牌譜網址是否正確\n'
        self.hint_tw = '請檢查網址後面&tw=(席次)是否附上\n'
        self.excelE = 11
