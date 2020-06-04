# -*- codeing: utf-8 -*-
'''
@File    :   douban.py
@Time    :   2020/05/13 18:29:30
@Author  :   sorrowfeng 
@Version :   1.0
@Contact :   1399600304@qq.com
@WebSite    :   https://sorrowfeng.github.io
'''

# here put the import lib
from bs4 import BeautifulSoup   # 网页解析, 获取数据
import re   # 正则表达式, 进行文字匹配
import urllib.request, urllib.error # 制定url, 获取网页数据
import xlwt # 进行excel操作
import sqlite3  # 进行SQLite操作


# 主函数
def main():
    baseurl = "https://movie.douban.com/top250?start="  #根路径
    #1. 爬取网页  与  2. 解析数据(逐一解析数据)
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影top250.xls"
    # dbpath = "movie.db"
    #3. 保存数据
    saveData(datalist, savepath)
    # saveDataDb(datalist, dbpath)



# 全局变量
# 电影详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')     # 创建正则规则对象
# 图片的规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S表示匹配包括换行符在内的所有字符
# 片名的规则
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 评分的规则
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数的规则
findRatingNum = re.compile(r'<span>(\d*)人评价</span>')
# 一句话评价的规则
findcomment = re.compile(r'<span class="inq">(.*?)</span>')
# 影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)



# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,10):   # 调用获取页面信息的函数十次
        url = baseurl + str(i*25)   
        html = askURL(url)  # 保存获取到的网页源码

        #2. 解析数据(逐一解析数据)
        soup = BeautifulSoup(html, "html.parser")   # 解析html对象, 用html.parser解析器
        for item in soup.find_all('div', class_="item"):     # 查找符合要求的字符串, 形成列表
            # print(item) # 测试: 查看电影item全部信息
            data = [] # 保存一部电影的全部信息
            item = str(item)    # 转成字符串

            link = re.findall(findLink, item)[0] # 通过正则查找指定字符串
            data.append(link)   # 添加链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc) # 添加图片

            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle) # 添加中文名
                otitle = titles[1].replace("/", "") # 把/替换掉
                data.append(otitle) # 添加外文名
            else:
                data.append(titles[0])
                data.append(' ')    #没有外文名, 留空(在列表中占一个位置)

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            ratingNum = re.findall(findRatingNum, item)[0]
            data.append(ratingNum)  # 添加评价人数

            comment = re.findall(findcomment, item)
            if len(comment) != 0:
                comment = comment[0].replace("。", "")
                data.append(comment)    # 添加一句话评论
            else:
                data.append(" ")    # 没有评论, 留空

            bd = re.findall(findBd, item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?", " ", bd)   # 替换<br/>
            data.append(bd.strip()) # 去掉前后的空格

            datalist.append(data)   # 把处理好的一部电影信息放入datalist

    # print(datalist)   # 测试获取到的一个item的数据
    return datalist # 返回数据



# 得到指定一个url的网页内容
def askURL(url):
    head = {    # 模拟浏览器头部信息
        "User-Agent" : "Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72"
    }
                # 用户代理, 表示告诉浏览器我们可以接受什么水平的内容
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
   
    return html



# 保存数据到xls
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("豆瓣电影250", cell_overwrite_ok=True)
    col = ("电影详情链接", "图片链接", "中文名", "外文名", "评分", "评价数", "一句话评价", "相关信息")  # 元组存放列标题
    for i in range(0, 8): 
        sheet.write(0, i, col[i])   # 写入列名
    for i in range(0, 250):
        print("第%d条"%(i+1))
        data = datalist[i]  # 写入250个item项目
        for j in range(0, 8):   
            sheet.write(i+1, j, data[j])    # 写入每个项目8个数据

    book.save(savepath)


# 保存数据到数据库
def saveDataDb(datalist, dbpath):
    initdb(dbpath)


# 初始化数据库
def init_db(dbpath):
    sql = '''
        create table movie250
        (
            id int primary key autoincrement,
            info_link text,
            info_img text,
            cname varchar,
            ename varchar,
            score numeric,
            rated numeric,
            instroduction text,
            info text
        )
    ''' # 创建数据表
    conn = sqlite3.connect(dbpath)  # 链接数据库

    cursor = conn.cursor()  # 获取游标
    cursor.execute(sql) # 执行sql语句

    conn.commit()   # 提交数据库操作
    conn.close()    # 关闭数据库连接


if __name__ == "__main__":
    main()
    print("爬取完成")

