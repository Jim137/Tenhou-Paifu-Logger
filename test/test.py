import argparse
import os
import sys
import unittest

sys.path.append(os.getcwd())

from paifulogger import log, paifu_dl


ATTR = [
    "url",
    "lang",
    "format",
    "all-formats",
    "remake",
    "output",
    "version",
    "mjai",
    "ignore-duplicated",
]


class Test(unittest.TestCase):
    def test_0(self):
        parser = argparse.ArgumentParser()
        args = parser.parse_args()

        for attr in ATTR:
            setattr(args, attr.replace("-", "_"), None)

        args.version = True

        self.assertEqual(log.log(args), 0)

    def test_1(self):
        parser = argparse.ArgumentParser()
        args = parser.parse_args()

        for attr in ATTR:
            setattr(args, attr.replace("-", "_"), None)

        args.url = [
            # yonma tests
            "https://tenhou.net/3/?log=2022052501gm-00c1-0000-f71e7910&tw=1",
            "https://tenhou.net/0/?log=2023051123gm-0001-0000-b3720f99&tw=2",
            "http://tenhou.net/0/?log=2023051216gm-0001-0000-5fd022cc&tw=1",
            # sanma tests
            "https://tenhou.net/0/?log=2023050200gm-0099-0000-50c65fbf&tw=2",
            "http://tenhou.net/0/?log=2023050419gm-0099-0000-b3111c7e&tw=0",
        ]
        args.all_formats = True
        args.ignore_duplicated = True
        args.output = "./test/"

        self.assertEqual(log.log(args), 0)

    def test_2(self):
        parser = argparse.ArgumentParser()
        args = parser.parse_args()

        for attr in ATTR:
            setattr(args, attr.replace("-", "_"), None)

        args.url = [
            # yonma tests
            "https://tenhou.net/3/?log=2022052501gm-00c1-0000-f71e7910&tw=1",
            "https://tenhou.net/0/?log=2023051123gm-0001-0000-b3720f99&tw=2",
            "http://tenhou.net/0/?log=2023051216gm-0001-0000-5fd022cc&tw=1",
            # sanma tests
            "https://tenhou.net/0/?log=2023050200gm-0099-0000-50c65fbf&tw=2",
            "http://tenhou.net/0/?log=2023050419gm-0099-0000-b3111c7e&tw=0",
        ]
        args.all_formats = True
        args.ignore_duplicated = True
        args.output = "./test/"
        args.lang = "zh_tw"

        self.assertEqual(log.log(args), 0)

    def test_3(self):
        urls = [
            # yonma tests
            "https://tenhou.net/3/?log=2022052501gm-00c1-0000-f71e7910&tw=1",
            "https://tenhou.net/0/?log=2023051123gm-0001-0000-b3720f99&tw=2",
            "http://tenhou.net/0/?log=2023051216gm-0001-0000-5fd022cc&tw=1",
            # sanma tests
            "https://tenhou.net/0/?log=2023050200gm-0099-0000-50c65fbf&tw=2",
            "http://tenhou.net/0/?log=2023050419gm-0099-0000-b3111c7e&tw=0",
        ]

        self.assertEqual(paifu_dl.paifu_dl(urls, output="./test/"), 0)

    def test_4(self):
        parser = argparse.ArgumentParser()
        args = parser.parse_args()

        for attr in ATTR:
            setattr(args, attr.replace("-", "_"), None)

        args.all_formats = True
        args.output = "./test/"
        args.remake = True

        self.assertEqual(log.log(args), 0)


if __name__ == "__main__":
    unittest.main()
