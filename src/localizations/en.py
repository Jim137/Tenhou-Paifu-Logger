from .local_str import local_str
class en(local_str):
    def __init__(self):
        self.hint_input = 'Please enter the URL of match:'
        self.haifu = 'Haifu'
        self.date = 'Date'
        self.plc = 'Placing'
        self.remark = 'Remark'
        self.preR = 'Rate before match'
        self.avg_plc = 'Average Placing'
        self.hint_record1 = 'Match of '
        self.hint_record2 = ' has been recorded.\n'
        self.hint_url = 'Please check the URL of match.\n'
        self.hint_tw = 'Please check the URL of match and whether &tw=(seat) is attached to the end of the URL.\n'
        self.excelE = 17
