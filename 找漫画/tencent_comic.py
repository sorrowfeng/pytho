import requests
from lxml import etree
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os
'''
============================
python学习群：695185429
============================
'''
#打开腾讯动漫首页
url = 'https://ac.qq.com/'
#给网页发送请求
data = requests.get(url).text
#将网页信息转换成xpath可识别的类型
html = etree.HTML(data)
#提取到每个漫画的目录页地址
comic_list = html.xpath('//a[@class="in-rank-name"]/@href')
#print(comic_list)
#遍历提取到的信息
for comic in comic_list:
    #拼接成为漫画目录页的网址
    comic_url = url + str(comic)
    #从漫画目录页提取信息
    url_data = requests.get(comic_url).text
    #准备用xpath语法提取信息
    data_comic = etree.HTML(url_data)
    #提取漫画名--text（）为提取文本内容
    name_comic = data_comic.xpath("//h2[@class='works-intro-title ui-left']/strong/text()")
    #提取该漫画每一页的地址
    item_list = data_comic.xpath("//span[@class='works-chapter-item']/a/@href")
    # print(name_comic)
    # print(item_list)
    #以漫画名字为文件夹名创建文件夹
    os.makedirs('comic/' + str(name_comic))
    #将一本漫画的每一章地址遍历
    for item in item_list:
        #拼接每一章节的地址
        item_url = url + str(item)
        #print(item_url)
        #请求每一章节的信息
        page_mes = requests.get(item_url).text
        #准备使用xpath提取内容
        page_ming = etree.HTML(page_mes)
        #提取章节名
        page_name = page_ming.xpath('//span[@class="title-comicHeading"]/text()')
        #print(page_name)
        #再以章节名命名一个文件夹
        os.makedirs('comic/' + str(name_comic) + '/' + str(page_name))

        #以下为代码的主体部分

        #设置谷歌无界面浏览器
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        #webdriver位置
        path = r'/home/jmhao/chromedriver'
        #浏览器参数设置
        browser = webdriver.Chrome(executable_path=path, options=chrome_options)
        #开始请求第一个章节的网址
        browser.get(item_url)
        #设置延时,为后续做缓冲
        sleep(2)
        #browser.get_screenshot_as_file(str(page_name) + ".png")
        #尝试执行下列代码
        try:
            #设置自动下滑滚动条操作
            for i in range(1, 100):
                #滑动距离设置
                js = 'var q=document.getElementById("mainView").scrollTop = ' + str(i * 1000)
                #执行滑动选项
                browser.execute_script(js)
                #延时,使图片充分加载
                sleep(2)
            sleep(2)
            #将打开的界面截图保存,证明无界面浏览器确实打开了网页
            browser.get_screenshot_as_file(str(page_name) + ".png")
            #获取当前页面源码
            data = browser.page_source
            #在当前文件夹下创建html文件,并将网页源码写入
            fh = open("dongman.html", "w", encoding="utf-8")
            #写入操作
            fh.write(data)
            #关掉无界面浏览器
            fh.close()

            #下面的操作为打开保存的html文件,提取其中的图片信息,并保存到文件夹中

            #用beautifulsoup打开本地文件
            html_new = BeautifulSoup(open('dongman.html', encoding='utf-8'), features='html.parser')
            #提取html文件中的主体部分
            soup = html_new.find(id="mainView")
            #设置变量i,方便为保存的图片命名
            i = 0
            #提取出主体部分中的img标签（因为图片地址保存在img标签中）
            for items in soup.find_all("img"):
                #提取图片地址信息
                item = items.get("src")
                #请求图片地址
                comic_pic = requests.get(item).content
                #print(comic_pic)
                #尝试提取图片,若发生错误则跳过
                try:
                    #打开文件夹,将图片存入
                    with open('comic/' + str(name_comic) + '/' + str(page_name) + '/' + str(i + 1) + '.jpg', 'wb') as f:
                        #print('正在下载第 ', (i + 1), ' 张图片中')
                        print('正在下载' , str(name_comic) , '-' , str(page_name) , '- 第' , (i+1) , '张图片')
                        #写入操作
                        f.write(comic_pic)
                        #更改图片名,防止新下载的图片覆盖原图片
                        i += 1
                #若上述代码执行报错,则执行此部分代码
                except Exception as err:
                    #跳过错误代码
                    pass
        # 若上述代码执行报错（大概率是由于付费漫画）,则执行此部分代码
        except Exception as err:
            #跳过错误代码
            pass

