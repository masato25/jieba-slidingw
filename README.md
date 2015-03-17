Jieba with sliding windows
========
本程式主要base on https://github.com/fxsjy/jieba.<br>
"结巴"中文分词：做最好的 Python 中文分词组件<br>
"Jieba" (Chinese for "to stutter") Chinese text segmentation: built to be the best Python Chinese word segmentation module.<br>

About sliding windows
========
在 tags extraction 的funcation 新增一個funcation -> extract_tags_custom<br>
程式位置:[./jieba/analyse/__init__.py]<br>

sliding windows 例子(以下這三段字的文章):<br>
<br>
-----------------------------
我們都是輪班星人<br>
每天都在快樂爆肝的輪班星人<br>
輪班星人的酸甜苦辣
-----------------------------
<br>
在正常的斷字下:<br>
輪班 & 星人 會被抓成不同的tag<br>
<br>
透過sliding windows 的方式, 從單一已經擷取出來的片段關鍵字去往前或是往後合併字.<br>
如果在整體文章中合併之後出來的字詞都是同一個字的話.就將它視作為一個新字. [ex. 輪班星人]<br>
平常批次做tags extraction時新字會自動加入jieba現有字典, 但當程式停止運作時會消失.<br>
在執行tags extraction時使用者設定的detectedwdsavepath的參數代表著儲存的filename, <br>
它會幫你將斷字過程產生出來的結果寫入 -> result/newwd<br>
使用者需要另外寫code去產生custom_wrod.wd的字典 (可以參考. gen_wddict.rb)<br>

Require
=========
* 使用這個程式只需要安裝python 2.7 以上的版本.
* 如果想使用gen_wddict.rb , 就另外需要安裝ruby


如何使用
=========
可以程式執行 python jieba_cut_sample_fromfile.py<br>
* 它會在頁面中print出斷字的結果
* 你可以從 result/newwd/2015_03_01.wd 看到它寫出來的新字list


[注意]以下幾種結果不會認定為新字<br>
=========
* 已經存在jieba預設的字典中的字
* 全部都是英文的字
* 全部都是數字的字

*本程式主要依據https://github.com/fxsjy/jieba 做修改,實際上的文件請參照該git project