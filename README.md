# yomaobot
===
yomaobot is a telegram bot that replies images according to the keywords inputted by users.

### Building Dependency
---
* [Python](https://www.python.org/) >= 3
* [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](http://docs.python-requests.org/en/master/)
* [html5lib](https://github.com/html5lib/html5lib-python)
* [flask](http://flask.pocoo.org/)

You can simply install the libraries using pip:
```
$ pip install -r requirements.txt
```

### Special Requirement
---
* The proxy pass utility is used in this bot, so you can see an element named 'nginx port' and another named 'proxy port' in .conf file. For the proxy pass, you can use [nginx](http://nginx.org/) or [apache](https://httpd.apache.org/) to achieve.

### Feature
---
* Detect keywords and reply image.
* Keywords are as followed
  * cat, kitty, kitties, 貓, 咪, 喵
  * girl, sister, woman, women, 女, 姐, 姊, 妹

![Demo_cat](http://i.imgur.com/HVi5tw6.png "Demo_cat")
* It randomly select an image from the following site
  * https://www.ptt.cc/bbs/Beauty/index.html
  * https://www.ptt.cc/bbs/cat/index.html

### Author
---
Sean Chen <genius091612@gmail.com>

### License
---
GPLv3 or later