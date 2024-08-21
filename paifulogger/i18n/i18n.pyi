class LocalStr:
    lang: str
    main_path: str

    # ==============================================
    # Additional fields defined in localization file
    excelE: int

    avg_plc: str
    date: str
    deal_in: str
    deal_in_rate: str
    hint_duplicate: str
    hint_input: str
    hint_record1: str
    hint_record2: str
    hint_tw: str
    hint_url: str
    log2mjai_import_error: str
    log_num: str
    paifu: str
    plc: str
    preR: str
    r_change: str
    remark: str
    round_num: str
    sanma: str
    sanma_mjai_error: str
    win: str
    win_rate: str
    yonma: str
    # ==============================================

    def __init__(self, lang: str = "en", main_path: str = "./") -> None: ...
    def load_data(self, data) -> None: ...
    def __setattr__(self, name, val) -> None: ...
    def __getattr__(self, name): ...

def localized_str(lang: str, main_path: str = ...) -> LocalStr: ...
