# 天凤牌谱记录器

[![build](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/publish-to-test-pypi.yml/badge.svg)](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/publish-to-test-pypi.yml)
[![lint](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/test.yml/badge.svg)](https://github.com/Jim137/Tenhou-Paifu-Logger/actions/workflows/test.yml)
[<img src="https://img.shields.io/pypi/v/PaifuLogger?style=plastic"> <img src="https://img.shields.io/pypi/wheel/PaifuLogger?style=plastic">](https://pypi.org/project/PaifuLogger/)
[![Downloads](https://static.pepy.tech/badge/Paifulogger)](https://pepy.tech/project/Paifulogger)
[<img src="https://img.shields.io/github/stars/Jim137/Tenhou-Paifu-Logger?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/)
[<img src="https://img.shields.io/github/downloads/Jim137/Tenhou-Paifu-Logger/total?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/releases)
![support-version](https://img.shields.io/pypi/pyversions/PaifuLogger?style=plastic)
![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgray?style=plastic)
![License](https://img.shields.io/github/license/Jim137/Tenhou-Paifu-Logger?style=plastic)

快速记录天凤牌谱的工具。

![由 DALL·E 生成](https://github.com/Jim137/Tenhou-Paifu-Logger/raw/master/READMEs/image/paifulogger.png)

如果你喜欢这个项目，请给我一颗 star，这将会是我很大的鼓励。如果你有任何建议，欢迎开issue来讨论。

[下载](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest) | [English](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/README.md) | [繁體中文](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_zh_TW.md) |[日本語](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_ja.md)

## 使用方法

1. 克隆此项目或下载[最新版本](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest)或使用pip下载。

    ```shell
    git clone https://github.com/Jim137/Tenhou-Paifu-Logger.git
    ```
    ```shell
    pip install PaifuLogger
    ```

2. 首次使用时，右键编辑 `runlog-user.bat` （Linux 用户则 `runlog-user.sh` ），在 set LANG= （export LANG=）后加上语言代码 `zh` ，保存后运行此文件。
  使用 pip 则运行以下命令。

    ```shell
    plog -l zh -o <输出目录> <多个牌谱网址>
    ```
    ```shell
    paifu plog -l zh -o <输出目录> <多个牌谱网址>
    ```

3. 复制天凤牌谱至剪贴板。
4. 在出现 `请输入牌谱网址:` 后，粘贴天凤牌谱并按下 Enter。\
   注意：在最新版本中，你可以一次输入多个牌谱网址，用任何你喜欢的符号隔开即可。如果你很懒，你也可以直接粘贴，不用加任何符号。
5. 当出现 `已将{牌谱}牌谱记录` 后，则表示牌谱已经成功记录。
6. 当再次出现 `请输入牌谱网址:`，即可输入下个牌谱。

## 功能

* [x] 支持一次输入多个牌谱网址。
* [x] 将牌谱记录到csv、Excel或html文件中。
* [x] 支持一次输出多个格式。（例：-f csv -f html; -a, --all-formats）
* [x] 区分三麻和四麻，并分别记录到不同的文件中。
* [x] 跳过已记录过的牌谱。
* [x] 重置已记录过的牌谱（-r, --remake）。当我们更新了牌谱记录的内容时，这个功能将会很有用。
* [x] 指定输出目录（-o, --output）
* [x] 支持mjai牌谱输出（--mjai）。*首次需要先执行 `git pull --recurse-submodules`*。
* [x] 本地化支持（-l, --language）
  * [x] 英文: en
  * [x] 繁体中文: zh_tw
  * [x] 简体中文: zh
  * [x] 日文 (ChatGPT): ja
* [x] 支持使用 config 文件设置。将 `config.json` 放置于相同使用环境下即可实现局域设置。若要实现全局设置，则将 `config.json` 放置于如下位置：
  * Windows: `%localappdata%\Jim137\paifulogger\config.json`
  * macOS: `/Users/{UserName}/Library/Application Support/paifulogger/config.json`
  * Linux: `~/.local/share/paifulogger/config.json`
* [x] 对局回放（仅限 html 牌谱）。

## 牌谱记录信息

* 对局时间
* 顺位
* 牌谱网址 (方便未来新增新功能时能快速套用过去牌谱)
* 对局前R值
* R值变化量

## 预计新增功能

* [ ] 和铳分析
* [ ] 雀魂牌谱支持
* [ ] 图形用户界面（GUI）

## 做出贡献

我们欢迎各种贡献，包括但不限于报告bug、PR、功能请求、文件改进、本地化...等。

参见[CONTRIBUTING.md](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/CONTRIBUTING.md)获取更多信息。

## 授权

[MIT](LICENSE)
