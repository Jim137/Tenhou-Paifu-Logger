import sys

if sys.version_info < (3, 10):
    raise ImportError("Python 3.10 or above is required for PaifuLogger.")
del sys

from .log import config_path, log, log_paifu, log_parser, remove_old_paifu
from .paifu_dl import paifu_dl

__version__ = "0.3.9.1"

__all__ = [
    "config_path",
    "log",
    "log_paifu",
    "log_parser",
    "remove_old_paifu",
    "paifu_dl",
    "__version__",
]
