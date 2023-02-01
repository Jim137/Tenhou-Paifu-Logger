from .zh_tw import zh_tw
from .en import en


def localized_str(lang: str):
    if lang == 'zh_tw':
        local_str = zh_tw()
    elif lang == 'en':
        local_str = en()
    else:
        local_str = en()
    return local_str
