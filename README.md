# Tenhou Paifu Logger

[<img src="https://img.shields.io/github/stars/Jim137/Tenhou-Paifu-Logger?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/) [<img src="https://img.shields.io/github/downloads/Jim137/Tenhou-Paifu-Logger/total?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/releases)

Logging tenhou paifu into excel or html file with some key information.

[Downloads](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest) | [中文說明](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_zh.md)

## Usage

1. Clone the repository or download the [latest release](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest).
   
   `git clone https://github.com/Jim137/Tenhou-Paifu-Logger.git`
   
2. Copy the paifu URL from tenhou.net to clipboard.
3. Open `runlog-user.bat`.
4. Once ![1675261153312](READMEs/image/README/1675261153312.png) appears, paste the paifu URL and press Enter.
5. After ![1675264143738](READMEs/image/README/1675264143738.png) appears, the paifu is successfully logged.
6. When ![1675261153312](READMEs/image/README/1675261153312.png) appears again, you can paste the next the URL.

## Features
* [x] Log paifu into excel or html file with some key information.
* [x] Distinguish Sanma(3p) and Yonma(4p) and log into separate sheets.
* [x] Skip duplicated paifu
* [x] Remake the paifu with URL already logged (-r, --remake). It will be useful when we updated the logging information in future.

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

## License

[MIT](LICENSE)
