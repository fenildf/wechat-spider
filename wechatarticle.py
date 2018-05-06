import time
import requests
import json
import re
import random
from selenium import webdriver

class WechatArticleUrl:

        def __init__(self,wechat_official_accounts,username,password):
            self.wechat_official_accounts = wechat_official_accounts
            self.article_url_list = []
            self.driver = webdriver.Firefox(executable_path='/Users/zl/Downloads/geckodriver')
            self.account_str = [username, password]
            self.cookies = {}
            self.token = ''
            self.header = {
                "HOST": "mp.weixin.qq.com",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
            }
            self.query = ''

        def __main__(self):
            self.login_wechat_official()
            self.get_token()
            self.get_url()

        def login_wechat_official(self):
            self.driver.get('https://mp.weixin.qq.com/')
            time.sleep(2)
            # ============登录，获取cookie
            self.driver.find_element_by_name('account').clear()
            self.driver.find_element_by_name('account').send_keys(self.account_str[0])
            self.driver.find_element_by_name('password').clear()
            self.driver.find_element_by_name('password').send_keys(self.account_str[1])
            # 在自动输完密码之后记得点一下记住我
            time.sleep(2)
            self.driver.find_element_by_xpath("./*//a[@class='btn_login']").click()
            # 拿手机扫二维码！
            time.sleep(10)
            self.driver.get('https://mp.weixin.qq.com/')
            cookie_items = self.driver.get_cookies()
            for cookie_item in cookie_items:
                self.cookies[cookie_item['name']] = cookie_item['value']

        def get_token(self):
            url = 'https://mp.weixin.qq.com'
            response = requests.get(url=url, cookies=self.cookies)
            self.token = re.findall(r'token=(\d+)', str(response.url))[0]

        def get_fakeid(self,query):
            query_id = {
                'action': 'search_biz',
                'token': self.token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'query': query,
                'begin': '0',
                'count': '5',
            }
            search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
            search_response = requests.get(search_url, cookies=self.cookies, headers=self.header, params=query_id)
            tmp_url = search_response.url  # 构造结果url
            # print(tmp_url)
            lists = search_response.json().get('list')[0]
            # print(lists)
            fakeid = lists.get('fakeid')
            return fakeid

        def get_url(self):
            for query in self.wechat_official_accounts:
                count = 0
                fakeid = self.get_fakeid(query)
                while True:
                    query_id_data = {
                        'token': self.token,
                        'lang': 'zh_CN',
                        'f': 'json',
                        'ajax': '1',
                        'random': random.random(),
                        'action': 'list_ex',
                        'begin': count,
                        'count': '10',
                        'query': self.query,
                        'fakeid': fakeid,
                        'type': '9'
                    }
                    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
                    appmsg_response = requests.get(appmsg_url, cookies=self.cookies, headers=self.header,params=query_id_data)
                    tmp_appmsg_url = appmsg_response.url
                    print(tmp_appmsg_url)
                    appmsg_response_json = json.loads(appmsg_response.content)
                    app_msg_cnt = appmsg_response_json['app_msg_cnt']
                    print(appmsg_response_json)
                    for msg_list in appmsg_response_json['app_msg_list']:
                        print(msg_list['link'])
                        self.article_url_list.append(msg_list['link'])

                    if app_msg_cnt <= 10 or app_msg_cnt - count <= 10:
                        break
                    else:
                        count += 10

                print(self.article_url_list)
                print(len(self.article_url_list))
                with open('article_url.txt', 'w') as file:
                    for url in self.article_url_list:
                        file.write(url)
                        file.write('\n')

if __name__ == '__main__':
    wechat_official_accounts = ['公众号微信号']
    username = '公众号账号'
    password = '公众号密码'
    wechat_official = WechatArticleUrl(wechat_official_accounts,username,password)
    wechat_official.__main__()
