import os
import sys

sys.path.append(os.getcwd())

from paifulogger import __version__


def build_pyproject():
    if "dev" in __version__:
        print("Dev version, not building.")
        return None

    with open("requirements.txt", "r") as f:
        requirements = [f"{line.strip()}" for line in f.readlines()]

    pyproject = f"""[build-system]
requires      = ["setuptools>=61.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "PaifuLogger"
version = "{__version__}"
description = "Logging tenhou paifu into excel or html file with some key information."
readme = "README.md"
authors = [{{ name = "Jim137", email = "jim@mail.jim137.eu.org" }}]
license = {{ file = "LICENSE" }}
classifiers = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
keywords = ["mahjong", "review", "logger", "paifu", "tenhou", "haifu", "paipu", "riichi-mahjong"]
dependencies = {requirements}
requires-python = ">=3.10"

[project.urls]
Homepage = "https://github.com/Jim137/Tenhou-Paifu-Logger"

[project.scripts]
paifu = "paifulogger.__main__:main"
log = "paifulogger.log:main"
plog = "paifulogger.log:main"
plogger = "paifulogger.log:main"
paifulog = "paifulogger.log:main"
pdl = "paifulogger.paifu_dl:main"

[tool.setuptools.packages.find]
exclude = [
    "Paifu",
    "牌譜",
]

[tool.setuptools.package-data]
"paifulogger.localizations" = [
    "*.json",
]""".replace(
        "'", '"'
    )

    with open("pyproject.toml", "w") as f:
        f.write(pyproject)


if __name__ == "__main__":
    print(__version__)
    build_pyproject()
