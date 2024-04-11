import sys

if sys.version_info < (3, 10):
    raise ImportError("Python 3.10 or above is required for PaifuLogger.")
del sys

__version__ = "0.3.9.1"
