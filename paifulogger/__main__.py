import argparse
import sys

from paifulogger.log import main as plog_main
from paifulogger.paifu_dl import main as pdl_main


def main():
    parser = argparse.ArgumentParser(description="PaifuLogger CLI")
    subparsers = parser.add_subparsers(required=False, dest="command")

    plog_parser = subparsers.add_parser("plog", help="Paifu Logger. See 'paifulogger plog -h' for more info.")
    pdl_parser = subparsers.add_parser("pdl", help="Paifu Downloader. See 'paifulogger pdl -h' for more info.")

    options = sys.argv

    if "plog" in options:
        sys.exit(plog_main(plog_parser))
    elif "pdl" in options:
        sys.exit(pdl_main(pdl_parser))
    elif "-v" in options or "--version" in options:
        from .version import __version__
        print("Tenhou-Paifu-Logger", __version__)
        return 0
    else:
        parser.parse_args()
        sys.exit(parser.print_help())

if __name__ == "__main__":
    main()
