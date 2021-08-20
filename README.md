# Crawl-the-weibo-user-name
爬虫采集微博用户名数据集

### 优势
支持崩溃恢复，爬取过程中可随时中断，下次执行时可无缝衔接

### 原理
从toscan_userid.txt读取userid进行爬取，爬取完后将此userid写入scaned_userid.txt文件，以避免重复爬取，且同时将用户名保存至username.txt，将通过该userid找到的新的userid存入toscan_userid_new.txt，当toscan_userid.txt的userid全部扫描完后，手动将toscan_userid_new.txt改名为toscan_userid.txt

### 运行
1. 在my_weibo_follow.py中self.headers填上自己的cookie，查看[如何获取cookie](https://github.com/dataabc/weibo-follow#%E5%A6%82%E4%BD%95%E8%8E%B7%E5%8F%96cookie)
2. 执行`python my_weibo_follow.py`
