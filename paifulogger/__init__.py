import os
import sys

if sys.version_info < (3, 10):
    raise ImportError("Python 3.10 or above is required for PaifuLogger.")
del sys

main_path = os.path.dirname(os.path.abspath(__file__))
del os

# import version first to avoid circular import
from .version import __version__
# ------------------------------

from .i18n import localized_str
from .log import config_path, get_log_func, log, log_paifu, log_parser, remove_old_paifu
from .paifu_dl import paifu_dl
from .utils import get_paifu, get_paifu_from_client_log, get_paifu_from_local


__all__ = [
    "__version__",
    "config_path",
    "get_log_func",
    "get_paifu",
    "get_paifu_from_client_log",
    "get_paifu_from_local",
    "localized_str",
    "log",
    "log_paifu",
    "log_parser",
    "main_path",
    "remove_old_paifu",
    "paifu_dl",
]
