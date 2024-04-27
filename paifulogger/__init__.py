import os
import sys

if sys.version_info < (3, 10):
    raise ImportError("Python 3.10 or above is required for PaifuLogger.")
del sys

main_path = os.path.dirname(os.path.abspath(__file__))
del os

from .version import __version__

from .log import config_path, log, log_paifu, log_parser, remove_old_paifu
from .paifu_dl import paifu_dl
from .src.get_paifu import get_paifu
from .src.i18n import localized_str

__all__ = [
    "__version__",
    "config_path",
    "get_paifu",
    "localized_str",
    "log",
    "log_paifu",
    "log_parser",
    "main_path",
    "remove_old_paifu",
    "paifu_dl",
]
