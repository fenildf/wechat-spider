# 微信公众号推文永久链接爬虫

## 需求
获取某个或多个微信公众号的所有文章，并且文章的链接是永久链接。比如我之前想分析学校公众号的某一个长期栏目，就需要他所有相关推送的文章内容。但是有 100+ 的推送，总不可能一篇一篇文章的去保存它的链接对吧？因此要想办法自动获取到所有的链接，再通过打开链接得到文章内容。

## 原理
利用微信公众号后台素材管理－新建图文素材－超链接－查找文章（公众号）的接口。因此，我们要做的就是模拟这个请求。
1.Selenium ＋ Webdriver 登陆微信公众平台，获取公众号的Cookie
2.登陆之后获取 token 值，因为之后所有请求都需要带 token 这个参数
3.模拟搜索公众号，每个公众号有对应的 fakeid，我们要得到公众号的fakeid
4.模拟搜索公众号内的文章，self.query 这个值为搜索公众号文章的关键字，默认为空，可以修改为自己想要找的公众号文章标题对应的关键字。此时会返回一个JSON包，app_msg_list 中的 link就是我们要的链接。

## 前提
你要有一个自己的微信公众号（订阅号）
Python环境：Python3

## 方法
修改 wechat_official_accounts 为想要搜索公众号的微信号，支持多个微信号
修改 username 为自己订阅号的账号
修改 password 为自己订阅号的密码
修改 self.query 为自己想要搜索的公众号文章标题对应的关键字
修改 self.driver = webdriver.Firefox(executable_path='/Users/zl/Downloads/geckodriver') 为自己对应的geckodriver内核地址，也可以使用 Chrome 浏览器
