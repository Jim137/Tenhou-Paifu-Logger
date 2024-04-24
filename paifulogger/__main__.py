import argparse
import sys

from paifulogger.log import main as plog_main
from paifulogger.paifu_dl import main as pdl_main
from paifulogger.version import __version__


def main():
    parser = argparse.ArgumentParser(description="PaifuLogger CLI", prog="PaifuLogger")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="""Show version of the program.
        If this is used, all other arguments will be ignored and the program will be closed.""",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(required=False, dest="command")

    plog_parser = subparsers.add_parser(
        "plog", help="Paifu Logger. See 'paifulogger plog -h' for more info."
    )
    pdl_parser = subparsers.add_parser(
        "pdl", help="Paifu Downloader. See 'paifulogger pdl -h' for more info."
    )

    options = sys.argv

    if "plog" in options:
        sys.exit(plog_main(plog_parser))
    elif "pdl" in options:
        sys.exit(pdl_main(pdl_parser))
    else:
        parser.parse_args()
        sys.exit(parser.print_help())


if __name__ == "__main__":
    main()
