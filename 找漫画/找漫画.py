# -*- codeing: utf-8 -*-
'''
@File    :   找漫画.py
@Time    :   2020/05/25 19:04:33
@Author  :   sorrowfeng 
@Version :   1.0
@Contact :   1399600304@qq.com
@WebSite :   https://sorrowfeng.github.io
'''
# here put the import lib

import base64
import json
import os
import re
import socket
import threading
import time
import bs4
import requests
import random

from fake_useragent import UserAgent
from lxml import etree, html

# 将两个列表对应组和成一个新的字典
def list2dic(list1,list2):
    # lambda是匿名函数, 冒号前为参数, 后面为返回值, 即传入x, y, 返回[x,y]
    # map函数, 第一个参数为函数名, 后面为参数, 返回返回一个将 function 应用于 iterable 中每一项并输出其结果的迭代器。
    return dict(map(lambda x,y:[x,y], list1,list2)) 

# 搜索gase_url
base_url = "https://www.imanhuaw.com/statics/search.aspx?key="

# 配置user_agent大全
user_agent_list = [
    # Opera
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
 
    # IPhone
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPod
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPAD
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # Android
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # QQ浏览器 Android版本
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # Android Opera Mobile
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    # Android Pad Moto Xoom
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    # BlackBerry
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    # WebOS HP Touchpad
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    # Nokia N97
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    # Windows Phone Mango
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    # UC浏览器
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    # UCOpenwave
    "Openwave/ UCWEB7.0.2.37/28/999",
    # UC Opera
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
ua = UserAgent()

# ip池
proxies_list = [
    'http://42.3.51.114:80',
    'http://39.106.205.147:8085',
    'http://220.135.8.49:40297',
    'http://47.52.231.140:8080',
    'http://183.166.97.173:999',
    'http://117.59.224.64:80',
    'http://103.220.73.39:8080',
    'http://150.138.253.71:808',
    'http://118.25.35.202:9999',
    'http://221.2.155.35:8060',
    'http://119.254.94.93:8088',
]

# 随机代理与请求头
proxies = {'http': random.choice(proxies_list)}
headers = {"User-Agent": ua.random}



threads = []
# thread类
class myThread (threading.Thread):
    def __init__(self, page_filename, page_url):
        threading.Thread.__init__(self)
        self.page_filename = page_filename
        self.page_url = page_url
    def run(self):
        spider.save_image(self.page_filename, self.page_url) # 多线程保存图片





class Spider:
    word = ''   # 要下载的字段
    def __init__(self, word):
        self.word = word

    def start_requests(self):
        start_url = base_url + str(self.word)
        # print(start_url)
        response = requests.get(start_url, proxies=proxies, headers=headers)
        myhtml = etree.HTML(response.content.decode())
        # print(myhtml)
        # 所找到的所有漫画的漫画名与url
        comic_url_list = myhtml.xpath("//div[@class='mh-works-title clearfix']/h4/a/@href")     
        comic_name_list = myhtml.xpath("//div[@class='mh-works-title clearfix']/h4/a/text()") 
        
        # 为找到的所有url加上前缀
        add_str = 'https://www.imanhuaw.com'
        for i in range(len(comic_url_list)):
            comic_url_list[i] = add_str + comic_url_list[i]
        
        # 将漫画名与url组成一个字典
        name_url_dic = list2dic(comic_name_list, comic_url_list)

        if not name_url_dic:
            print('未找到此漫画')
            os.system('pause')
            return

        num = 0 # 序号
        find_dic = {} # 搜索找到的结果, 构成的字典  
        print('\n')
        for name in name_url_dic:
            num += 1
            find_dic[str(num)]=name    # 将找到的结果再放入一个字典内, 方便序号查找
            print(str(num) + '.  ' +  name)
        comic_num = input('\n你想下载的是(请输入序号):')
        print('\n\n')
        comic_name = find_dic[comic_num]  # 确定漫画名
        comic_url = name_url_dic.get(comic_name)  # 从字典中找到对应漫画的链接      
        print('正在为你下载:'+comic_name+'\n')
        self.word = comic_name # 改变word
        # print(self.word+comic_url)
        if os.path.exists(self.word) == False:   # 新建漫画目录
                os.mkdir(self.word)
        self.requests_chapter(comic_url)

    # 请求章节链接
    def requests_chapter(self, comic_url):
        response = requests.get(comic_url)
        response.encoding = 'utf-8'
        myhtml = etree.HTML(response.text)
        # print(myhtml)
        # 请求每章的名称与url
        chapter_name_list = myhtml.xpath("//div[@class='cy_plist']/ul/li/a/p/text()") 
        chapter_url_list = myhtml.xpath("//div[@class='cy_plist']/ul/li/a/@href")
        chapter_name_list.reverse() # 反序
        chapter_url_list.reverse()
        # chapter_name_url_dic = list2dic(chapter_name_list, chapter_url_list)
        # print(chapter_name_url_dic)

        for chapter_name, chapter_url in zip(chapter_name_list, chapter_url_list):      # 遍历所有章节     
            if os.path.exists(self.word + '/' + chapter_name) == False:
                os.mkdir(self.word + '/' + chapter_name)
            self.requests_img(chapter_name, chapter_url)
        
        print('下载完成')
        os.system('pause')
        return
            
    

    # 请求每章所有的图片
    def requests_img(self, chapter_name, chapter_url):
        page_url = 'https://www.imanhuaw.com' + chapter_url

        response = requests.get(page_url, headers=headers)
        myhtml = bs4.BeautifulSoup(response.content.decode(), 'lxml')   # 获取整个页面的html
        
        # 获取qTcms_S_m_murl_e的值, 该值就是加密后的本章节所有图片的链接
        find_qTcms_S_m_murl_e = re.compile(r'qTcms_S_m_murl_e="(.*?)"', re.S)
        qTcms_S_m_murl_e = re.findall(find_qTcms_S_m_murl_e, str(myhtml))[0]
        # print(qTcms_S_m_murl_e)

        # 解码qTcms_S_m_murl_e, 恢复原来的图片链接
        qTcms_S_m_murl = base64.b64decode(qTcms_S_m_murl_e).decode('utf-8')
        # print(qTcms_S_m_murl)

        # 将图片链接中的分隔符给去掉
        chapter_url_list = qTcms_S_m_murl.split('$qingtiandy$')
        # print(chapter_url)
        # print(chapter_name)
        i = 1
        for page_url in chapter_url_list:
            page_filename = self.word + '/' + chapter_name + '/' + chapter_name + '_' + str(i) + '.jpg'
            i += 1
            # self.save_image(page_filename, page_url)
            thread_num = myThread(page_filename, page_url) # 新建新线程对象
            # time.sleep(0.015)    # 加入延迟, 否则会漏章节
            thread_num.start()   # 开始线程
            threads.append(thread_num) # 添加线程到线程列表
            # time.sleep(0.015)    # 加入延迟, 否则会漏章节

        # 释放所有线程
        for t in threads:
            # time.sleep(0.01)
            t.join()


    # 保存图片
    def save_image(self, page_filename, page_url):
        response = requests.get(page_url)
        content = response.content
        with open(page_filename, 'wb') as f:
            f.write(content)    # 写入图片信息
        print('正在下载'+page_filename)




if __name__ == "__main__":
    word = input('请输入要下载的漫画:')
    spider = Spider(word)
    spider.start_requests()
