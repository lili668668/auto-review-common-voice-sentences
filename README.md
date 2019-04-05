# auto-review-common-voice-sentences
一個快速批量審核 common voice 上面句子的 script 工具

## 緣起

Mozilla 有一個 [Common Voice](https://voice.mozilla.org/) 專案，聽朋友說上面的句子，最近要經過好幾個人審核（[審核網頁](https://common-voice.github.io/sentence-collector/#/)），才能被使用。

帳號沒有條件限制，有空可以去申請個帳號審核。另外，本專案要有帳號，才能使用。

在幫忙審核大約一百筆後，我就放棄了，這一頁只能點3個讚，還沒有全選功能的網站，實在太浪費他人生命了。

秉持著信任句子提供者，所以我想讓所有句子都通過審核，這個想法，所以我寫了這個 Script。

## 注意：

- 因為寫的有點趕，所以這個 Script 可能有蟲，而且我文件跟相依套件還沒補全
- 如果你覺得審核網站上的句子，可能會有不是句子的文字出現(網址之類的)，就還是上網站上一個一個點比較好

## 工具

- 使用 Python3， 依賴 [requests](http://docs.python-requests.org)

## 使用方式

```bash
$ git clone https://github.com/lili668668/auto-review-common-voice-sentences

$ cd auto-review-common-voice-sentences

$ pip3 install requests

$ python3 main.py <username> "<authorization>" <review-number> # ex: python3 main.py lili668668 "Basic XXXOOO" 50
```

## authorization 在哪裡？
1. 用 Firefox 登入 Common Voice 審查網站
![](https://i.imgur.com/AlqRsmK.png)
2. 按下 F12 打開開發者工具，點選網路頁籤，篩選「XHR」
![](https://i.imgur.com/PXeaqIu.png)
3. 尋找請求 url 是「https://kinto.mozvoice.org/v1/buckets/App/collections/Sentences_Meta_zh-TW/records?approved=true&_sort=-last_modified」的那筆資料
![](https://i.imgur.com/xuyzrb8.png)
4. 請求標頭裡有 Authorization，複製內容，再貼上到 terminal
![](https://i.imgur.com/3C7sv93.png)

## 備註
- 其實可以用帳密取得 Authorization，比較人性一點，不過做的有點趕，之後再補上
- 這個現在只有審核台灣中文的句子，可以審核其他語言的句子，但我還沒做，之後補上
- `<review-number>` 可以填 all，就會直接幫你把所有句子審完 ex: python3 main.py lili668668 "Basic XXXOOO" all
- 他審核句子的方式是送 post 請求，post 請求裡帶要披次處理的 put 請求，一個句子是一個 put 請求，因為 put 請求有上限 25 筆，所以每 25 筆會發出去一次 post 請求
- 我沒有測過短時間大量請求會不會封鎖人，所以如果 Script 處理到一半失敗了，就換個 IP 重新開始試試看

