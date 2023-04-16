# 天鳳牌譜記錄器

快速記錄天鳳牌譜的工具。

[下載](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest) | [English](https://github.com/Jim137/Tenhou-Paifu-Logger/blob/master/README.md)
## 使用方法

1. Clone此專案或下載[最新版本](https://github.com/Jim137/Tenhou-Paifu-Logger/releases/latest)。
   
    `git clone https://github.com/Jim137/Tenhou-Paifu-Logger.git`
    
2. 首次使用時，右鍵編輯 `runlog-user.bat`，在set LANG=後加上語言代碼 `zh_tw`，保存後運行此檔案。
3. 複製天鳳牌譜至剪貼簿。
4. 在出現![1675260159266](image/README_zh/1675260159266.png)後，貼上天鳳牌譜並按下Enter。
5. 當出現![1675260331020](image/README_zh/1675260331020.png)後，則表示牌譜已經成功記錄。
6. 當再次出現![1675260159266](image/README_zh/1675260159266.png)，即可輸入下個牌譜。

## 功能
* [x] 將牌譜記錄到Excel檔案中。
* [x] 區分三麻和四麻，並分別記錄到不同的檔案中。

## 牌譜紀錄訊息

* 對局時間
* 順位
* 牌譜網址 (方便未來新增新功能時能快速套用過去牌譜)
* 對局前R值

## 預計新增功能

* [ ] 跳過已記錄的牌譜
* [ ] 對局R值變化
* [ ] 和銃分析
* [ ] 圖形使用者介面（GUI）
