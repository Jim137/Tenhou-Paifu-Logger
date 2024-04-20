class LocalStr:
    lang: str
    main_path: str

    hint_input: str
    paifu: str
    date: str
    plc: str
    remark: str
    preR: str
    avg_plc: str
    hint_record1: str
    hint_record2: str
    hint_url: str
    hint_tw: str
    excelE: int
    sanma: str
    yonma: str
    hint_duplicate: str
    sanma_mjai_error: str
    log2mjai_import_error: str
    r_change: str
    round_num: str
    win: str
    deal_in: str
    win_rate: str
    deal_in_rate: str
    log_num: str

    def __init__(self, lang: str = "en", main_path: str = "./") -> None: ...
    def load_data(self, data) -> None: ...
    def __setattr__(self, name, val) -> None: ...
    def __getattr__(self, name): ...

def localized_str(lang: str, main_path: str = ...) -> LocalStr: ...
