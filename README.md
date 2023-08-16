# Tenhou Paifu Logger

[<img src="https://img.shields.io/pypi/v/PaifuLogger?style=plastic"> <img src="https://img.shields.io/pypi/wheel/PaifuLogger?style=plastic">](https://pypi.org/project/PaifuLogger/) [<img src="https://img.shields.io/github/stars/Jim137/Tenhou-Paifu-Logger?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/) [<img src="https://img.shields.io/github/downloads/Jim137/Tenhou-Paifu-Logger/total?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/releases) ![GitHub](https://img.shields.io/github/license/Jim137/Tenhou-Paifu-Logger?style=plastic)

Logging tenhou paifu into excel or html file with some key information.

If you like this project, please leave a star. It will be a great encouragement for me. And if you have any suggestions, please feel free to create an issue.

[Downloads](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest) | [中文說明](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_zh.md) | [日本語](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_ja.md)

## Usage

1. Download the project.

  >a. Download from github.

  >>i. Clone the repository or download the [latest release](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest).

    git clone https://github.com/Jim137/Tenhou-Paifu-Logger.git

  >>ii. Copy the paifu URL from tenhou.net to clipboard.
  >>iii. Open `runlog-user.bat`.
    
  >b. Download from pypi.

  >>i. Open command line and type

    pip install PaifuLogger

  >>ii. Copy the paifu URL from tenhou.net to clipboard. And type

    log -l [language] -o [output directory] [paifu URLs]

2. Once ![1675261153312](https://github.com/Jim137/Tenhou-Paifu-Logger/raw/master/READMEs/image/README/1675261153312.png) appears, paste the paifu URL and press Enter.\
Note: In the latest version, you can input multiple URLs at once, separated by whatever you like. If you are lazy, you can just paste w/o anything.
3. After ![1675264143738](https://github.com/Jim137/Tenhou-Paifu-Logger/raw/master/READMEs/image/README/1675264143738.png) appears, the paifu is successfully logged.
4. When ![1675261153312](https://github.com/Jim137/Tenhou-Paifu-Logger/raw/master/READMEs/image/README/1675261153312.png) appears again, you can paste the next the URL.

## Features
* [x] Log paifu into excel or html file with some key information.
* [x] Distinguish Sanma(3p) and Yonma(4p) and log into separate sheets.
* [x] Skip duplicated paifu
* [x] Remake the paifu with URL already logged (-r, --remake). It will be useful when we updated the logging information in future.
* [x] Customized output directory (-o, --output)
* [x] Localization support (-l, --language)
  * [x] English: en
  * [x] Traditional Chinese: zh_tw
  * [x] Simplified Chinese: zh
  * [x] Japanese (ChatGPT): ja

## Information logged

* Game time
* Placing
* URL (for future use)
* Rate before the game

## Future features

* [ ] Add match replay for every round in html file
* [ ] The change of Rate
* [ ] Agari analysis
* [ ] Support Majsoul paifu
* [ ] GUI

## Contribute
We welcome all kinds of contributions, including but not limited to bug reports, pull requests, feature requests, documentation improvements, localizations...etc.

## License

[MIT](LICENSE)
