# Tenhou Paifu Logger

[![build](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/publish-to-test-pypi.yml/badge.svg)](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/publish-to-test-pypi.yml)
[![lint](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/test.yml/badge.svg)](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/test.yml)
[<img src="https://img.shields.io/pypi/v/PaifuLogger?style=plastic"> <img src="https://img.shields.io/pypi/wheel/PaifuLogger?style=plastic">](https://pypi.org/project/PaifuLogger/)
[![Downloads](https://static.pepy.tech/badge/Paifulogger)](https://pepy.tech/project/Paifulogger)
[<img src="https://img.shields.io/github/stars/Jim137/Tenhou-Paifu-Logger?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/)
[<img src="https://img.shields.io/github/downloads/Jim137/Tenhou-Paifu-Logger/total?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/releases)
![support-version](https://img.shields.io/pypi/pyversions/PaifuLogger?style=plastic)
![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgray?style=plastic)
![License](https://img.shields.io/github/license/Jim137/Tenhou-Paifu-Logger?style=plastic)

Logging tenhou paifu into excel, csv or html file with some key information.

![Generated by DALL·E](https://github.com/Jim137/Tenhou-Paifu-Logger/raw/master/READMEs/image/paifulogger.png)

If you like this project, please leave a star. It will be a great encouragement for me. And if you have any suggestions, please feel free to create an issue.

[Downloads](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest) | [繁體中文](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_zh_TW.md) | [简体中文](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_zh.md) | [日本語](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_ja.md)

## Requirements

* Python 3.10 or later

Since CLI-0.3.8, the project is only compatible with Python 3.10 or later.
For Python 3.9 or earlier users, please use [CLI-0.3.7.1](https://github.com/Jim137/Tenhou-Paifu-Logger/tree/CLI-0.3.7.1) which is the last version that supports Python 3.9 or earlier.
Or download from pypi with the following command.

```shell
pip install PaifuLogger==0.3.7.1
```

## Usage

### Command Line / Script

1. Download the project.

> a. Via GitHub.
>
>> i. Clone the repository or download the [latest release](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest).
>>
>> ```shell
>> git clone https://github.com/Jim137/Tenhou-Paifu-Logger.git
>> ```
>>
>> ii. Copy the paifu URL from tenhou.net to clipboard.
>>
>> iii. Run `runlog-user.bat` or `runlog-user.sh`.
>
> b. Via pypi.
>
>> i. Open terminal and install with pip command.
>>
>> ```shell
>> pip install PaifuLogger
>> ```
>>
>> ii. Copy the paifu URL from tenhou.net to clipboard. And run by
>>
>> ```shell
>> plog -l [language] -o [output directory] [paifu URLs]
>> ```
>>
>> ```shell
>> paifu plog -l [language] -o [output directory] [paifu URLs]
>> ```

2. Once `Please enter the URL of match:` appears, paste the URL and press Enter.\
Note: In the latest version, you can input multiple URLs at once, separated by whatever you like. If you are lazy, you can just paste w/o anything.
3. After `Match of {paifu name} has been recorded` appears, the paifu has been successfully logged.

### Inline

You can manually log the paifu by the following code.

```python
from paifulogger import get_log_func, get_paifu, localized_str, log_paifu

url = "Your paifu URL"
local_lang = localized_str("en") # Localization
log_formats = get_log_func(["csv", "html"]) # Log into csv and html file.
output = "./" # Output directory
mjai = False # Whether have output in mjai format

# Log the paifu into the file.
log_paifu(
    url,
    log_formats = log_formats,
    local_lang = local_lang,
    output = output,
    mjai = mjai
)
# Get Paifu object, which contains all the information of the paifu.
paifu = get_paifu(url, local_lang)
```

## Features

* [x] Support multiple URLs at once.
* [x] Log paifu into excel, csv or html file with some key information. (-f, --format)
* [x] Support logging to multiple formats at once. (e.g.: -f csv -f html; -a, --all-formats)
* [x] Distinguish Sanma(3p) and Yonma(4p) and log into separate sheets.
* [x] Skip duplicated paifu
* [x] Remake the paifu with URL already logged (-r, --remake). It will be useful when we updated the logging information in future.
* [x] Customized output directory (-o, --output)
* [x] Support mjai format paifu output (--mjai). *You have to run `git pull --recurse-submodules` first*.
* [x] Localization support (-l, --language)
  * [x] English: en
  * [x] Traditional Chinese: zh_tw
  * [x] Simplified Chinese: zh
  * [x] Japanese (ChatGPT): ja
* [x] Support config file. Placing `config.json` in the same directory as the execution enables local configuration. For global configuration, place it in the following directories:
  * Windows: `%localappdata%\Jim137\paifulogger\config.json`
  * macOS: `/Users/{UserName}/Library/Application Support/paifulogger/config.json`
  * Linux: `~/.local/share/paifulogger/config.json`
* [x] Support logging from Tenhou client(*.mjlog). (-c, --from-client DIR_TO_MJLOG)\
Note: Typically, the saved directory is `{Documents}/My Tenhou/log/` on Windows.
* [x] Match replay for html format. By clicking the match you want to review, the match replay will pop up accordingly.

## Information logged

* Game time
* Placing
* URL (for future use)
* Rate before the game
* The change of Rate: Note it assumes that the player has played more than 400 games.
* Number of wins
* Number of deal-ins

## Future features

* [ ] Agari analysis
* [ ] Support Majsoul paifu
* [ ] GUI

## Contribute

We welcome all kinds of contributions, including but not limited to bug reports, pull requests, feature requests, documentation improvements, localizations...etc.

See [CONTRIBUTING.md](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
