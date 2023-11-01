# 天鳳牌譜記錄器

[<img src="https://img.shields.io/pypi/v/PaifuLogger?style=plastic"> <img src="https://img.shields.io/pypi/wheel/PaifuLogger?style=plastic">](https://pypi.org/project/Tenhou-Paifu-Logger/) [<img src="https://img.shields.io/github/stars/Jim137/Tenhou-Paifu-Logger?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/) [<img src="https://img.shields.io/github/downloads/Jim137/Tenhou-Paifu-Logger/total?style=plastic">](https://github.com/Jim137/Tenhou-Paifu-Logger/releases) ![GitHub](https://img.shields.io/github/license/Jim137/Tenhou-Paifu-Logger?style=plastic)

快速記錄天鳳牌譜的工具。

如果你喜歡這個專案，請給我一顆star，這將會是我很大的鼓勵。如果你有任何建議，歡迎開issue來討論。

[下載](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest) | [English](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/README.md) | [日本語](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/READMEs/README_ja.md)
## 使用方法

1. Clone此專案或下載[最新版本](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest)或使用pip下載。
   
    `git clone https://github.com/Jim137/Tenhou-Paifu-Logger.git`

    `pip install PaifuLogger`
    
2. 首次使用時，右鍵編輯 `runlog-user.bat` (Linux用戶則 `runlog-user.sh` )，在set LANG= (export LANG=)後加上語言代碼 `zh_tw`，保存後運行此檔案。
  使用pip則運行以下命令。

    `log -l zh_tw -o <輸出目錄> (-r <多個牌譜網址>)`

3. 複製天鳳牌譜至剪貼簿。
4. 在出現![1675260159266](image/README_zh/1675260159266.png)後，貼上天鳳牌譜並按下Enter。\
注意：在最新版本中，你可以一次輸入多個牌譜網址，用任何你喜歡的符號隔開即可。如果你很懶，你也可以直接貼上，不用加任何符號。
5. 當出現![1675260331020](image/README_zh/1675260331020.png)後，則表示牌譜已經成功記錄。
6. 當再次出現![1675260159266](image/README_zh/1675260159266.png)，即可輸入下個牌譜。

## 功能
* [x] 將牌譜記錄到Excel或html檔案中。
* [x] 區分三麻和四麻，並分別記錄到不同的檔案中。
* [x] 跳過已記錄過的牌譜。
* [x] 重製已記錄過的牌譜（-r, --remake）。當我們更新了牌譜記錄的內容時，這個功能將會很有用。
* [x] 指定輸出目錄（-o, --output）
* [x] 支援mjai牌譜輸出（--mjai）。*首次需要先執行 `git pull --recurse-submodules`*。
* [x] 本地化支援（-l, --language）
  * [x] 英文: en
  * [x] 繁體中文: zh_tw
  * [x] 簡體中文: zh
  * [x] 日文 (ChatGPT): ja

## 牌譜紀錄訊息

* 對局時間
* 順位
* 牌譜網址 (方便未來新增新功能時能快速套用過去牌譜)
* 對局前R值

## 預計新增功能

* [ ] 每一本場的對局回放（html）
* [ ] 對局R值變化
* [ ] 和銃分析
* [ ] 雀魂牌譜支援
* [ ] 圖形使用者介面（GUI）

## 做出貢獻
我們歡迎各種貢獻，包括但不限於回報bug、PR、功能要求、文件改進、本地化...等。

參見[CONTRIBUTING.md](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/CONTRIBUTING.md)取得更多訊息。

## 授權
[MIT](LICENSE)