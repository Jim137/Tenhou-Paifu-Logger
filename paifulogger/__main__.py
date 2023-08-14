import argparse

from paifulogger import log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url",
                        nargs='*',
                        help="URL of the match.")
    parser.add_argument("-l",
                        "--lang",
                        type=str,
                        help="Language of the program and output files. Default is English. Available languages: English(en), 繁體中文(zh_tw), 简体中文(zh), 日本語(ja).")
    parser.add_argument("-f",
                        "--format",
                        type=str,
                        help="Format of the output file. Default is xlsx. Available formats: xlsx, html.",
                        choices=['xlsx', 'html'])
    parser.add_argument("-a",
                        "--all-formats",
                        action="store_true",
                        help="Output all formats.")
    parser.add_argument("-r",
                        "--remake",
                        action="store_true",
                        help="Remake the log file from url_log.h5 (past logging log). Use this when the program is updated, changing format or language of the log file, or the log file is missing. Note that this will overwrite the log file.")
    parser.add_argument("-o",
                        "--output",
                        type=str,
                        help="Output directory. Default is './'.")
    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="Show version of the program. If this is used, all other arguments will be ignored and the program will be closed.")
    # Args for Debugging
    parser.add_argument("--ignore-duplicated",
                        action="store_true",
                        help=argparse.SUPPRESS)
    args = parser.parse_args()
    log.log(args)


if __name__ == '__main__':
    main()
