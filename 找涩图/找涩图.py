# -*- codeing: utf-8 -*-
'''
@File    :   find_img.py
@Time    :   2020/05/14 21:08:22
@Author  :   sorrowfeng 
@Version :   1.0
@Contact :   1399600304@qq.com
@WebSite :   https://sorrowfeng.github.io
'''

# here put the import lib
import os
import re
import urllib.request, urllib.error, urllib.parse
import urllib
# import _thread
import time
import socket
import json
import tkinter as tk
import threading    


# headers = {    
#     'accept':'image/webp,image/apng,*/*;q=0.8',
#     'accept-encoding':'gzip, deflate, br',
#     'accept-language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
#     'sec-fetch-dest':'image',
#     'sec-fetch-mode':'no-cors',
#     'sec-fetch-site':'cross-site',
#     'referer':'https://pixivic.com/popSearch',
#     'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72',
# }


# 保存图片到本地
def SaveImage(url, path):   # 传入的url是图片url地址
    request = urllib.request.Request(url)   # 模拟浏览器头部信息
    request.add_header('accept','image/webp,image/apng,*/*;q=0.8')
    request.add_header('accept-encoding','gzip, deflate, br')
    request.add_header('accept-language','zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6')
    request.add_header('sec-fetch-dest','image')
    request.add_header('sec-fetch-mode','no-cors')
    request.add_header('sec-fetch-site','cross-site')
    request.add_header('referer','https://pixivic.com/popSearch')
    request.add_header('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72')
    try:
        response = urllib.request.urlopen(request)  # 打开该url得到响应
        img = response.read()   # read读取出来
        f = open(path, 'wb')    # 以二进制写入的格式打开
        f.write(img)    # 写入
        f.close()       # 关闭
    except urllib.error.URLError as ue:  # 捕获urlerror
        if hasattr(ue, 'code'):  # 如果ue中包含'code'字段, 则打印出来
            print(ue.code)
        if hasattr(ue, "reason"):# 如果ue中包含'reason'字段, 则打印出来
            print(ue.reason)
    except IOError as ie:
        print(ie)

    return 




class Crawler:
    __time_sleep = 0.1  # 延时时间
    __counter = 0       # 正在保存的第几个计数
    __start_amount = 0  # 开始页码
    __amount = 0        # 总页码
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72'}

    # 构造函数
    def __init__(self, t, word, app):    # word为想查找图片的名字字段
        self.__time_sleep = t
        if not os.path.exists("./" + word):     # 检测是否存在该word文件夹, 不存在则创建
            os.mkdir("./" + word)
        self.__counter = len(os.listdir('./' + word)) + 1   # 返回word路径下所有条目的信息, 并加一     

    # 获取后缀
    def get_suffix(self, name):     # name为保存图片时传入的网址
        m = re.search(r'\.[^\.]*$', name)   # \. 表示匹配.而不是任意字符
                                            # [^\.]*$ 表示匹配除了.之外的所有字符,0到n个并以其结尾
        if m.group(0) and len(m.group(0)) <= 5: # m.group(0)表示匹配到的第一个元素
            return m.group(0)   # 如果第一个元素存在, 并长度小于5, 则返回
        else:                   # 否则返回 '.jpeg'
            return '.jpeg'

    # 保存图片
    def save_image(self, rsp_data, word):
        for image_info in rsp_data['imageUrls']:
            try:    # 有可能发生异常的代码片段
                # 替换链接片段
                pps = image_info['original'].replace('https://i.pximg.net/','https://original.img.cheerfun.dev/')
                # print(pps) # 打印图片真实链接
                suffix = self.get_suffix(pps)
                # 保存图片
                # 开启一个新线程, 并传入执行的函数, 与对应参数, 参数为图片url与保存的文件名
                # _thread.start_new_thread(SaveImage, (pps, './' + word + '/' + str(self.__counter) + str(suffix)))
                threading.Thread(target=SaveImage, args=(pps, './' + word + '/' + word + "_" + str(self.__counter) + str(suffix))).start()
                
            except urllib.error.HTTPError as http_err:
                print(http_err) # 出现HTTPError打印其信息, 并继续往下执行
                continue
            except Exception as e:  # 出现其他错误, 休眠一秒, 打印其信息, 并继续往下执行
                time.sleep(1)
                print(e)
                print("出现未知错误, 放弃保存") 
                continue
            else:   # 没发生异常时执行的语句
                sum = len(os.listdir('./' + word))  # 查询当前word字段文件夹下的文件个数
                # print(f'第{str(self.__counter)}张涩图正在保存, 已有{str(sum)}张涩图') # Python3.6新引入的一种字符串格式化方法, 大括号{}标明被替换的字段
                # 文本框的打印输出
                app.t.insert('end', f'第{str(self.__counter)}张涩图正在保存, 已有{str(sum)}张涩图, 保存在{os.getcwd()}下的{word}文件夹\n')
                app.t.see(tk.END)   # 打印后自动翻滚到最后一行
                app.t.update()  # 更新
                self.__counter += 1 # 保存完一张后将counter计数加一
                time.sleep(self.__time_sleep)   # 并延时指定的秒数
        return
        
    
    # 获取图片
    def get_image(self, word=''):
        search = urllib.parse.quote(word) # 转义替换路径中的 / 
        pagenum = self.__start_amount   # 获取开始页码
        while pagenum <= self.__amount: # 当开始页码小于总页码时循环    
            url = 'https://api.pixivic.com/illustrations?keyword='+search+'&page='+str(pagenum)   # 写入url
            # print(url)  # 打印url
            try:
                req = urllib.request.Request(url=url, headers=self.headers)     # 用户代理, 告诉浏览器我们可以接受什么水平的信息
                page = urllib.request.urlopen(req)      # 接受打开url返回的信息
                rsp = page.read().decode('utf-8')       # 读取接受到的page信息并以utf-8格式保存到rsp中
            except UnicodeDecodeError as e: # 当在编码过程中发生与 Unicode 相关的错误
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e: # urlerror
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e: # 响应超时
                print(e)
                print("-----socket timout:", url)
            else:
                rsp_data = json.loads(rsp)   # 使用此conversion table将包含JSON文档的s（a str实例）解压缩为Python对象。
                temp = rsp_data['data']      # 将返回的data存入, 并在下方遍历传入save_image中, 再在data中提取出图片链接
                for ele in temp:    # 下载一页的图片
                    self.save_image(ele, word)  
                print("下载下一页")
                pagenum += 1
            finally:
                page.close() # 关闭
        print("下载结束")
        return


    def start(self, word, page_num, start_page):    # 开始
        self.__start_amount = start_page    # 开始页码
        self.__amount = page_num            # 总页码
        self.get_image(word)                # 获取图片





class Application(tk.Frame):
    theWord = ''
    def __init__(self, master=None):    # 构造函数
        super().__init__(master)
        master.title("找涩图")      # 标题名
        master.geometry("500x300")  # 父窗口大小
        self.pack()
        self.create_input_widget()  # 创建输入部件
        self.create_output_widget() # 创建输出部件
        

    def create_input_widget(self, master=None):     # 创建输入部件
        L1 = tk.Label(master, text="你要找谁的涩图?")  # 创建题头部件
        L1.pack()
        self.text_widget = tk.Entry(master, show=None, bd=5)  # 创建文本框部件
        self.text_widget.pack()
        b1 = tk.Button(master,text="开始找涩图",width=15,height=2,command=lambda:self.thread_it(self.start_find))   # 创建按钮, 按下执行start_find函数
        b1.pack()
        b2 = tk.Button(master,text="不找了, 退出",width=15,height=2,command=root.destroy) # 退出按钮
        b2.pack()

    def create_output_widget(self): # 创建输出部件
        self.t = tk.Text(width=400, height=100) # 文本框的大小
        self.t.pack()
        # t.insert('end', 'hello')

        
    def start_find(self):   # 开始查找函数
        self.theWord = self.text_widget.get() # 将文本框内字段传入
        self.crawler = Crawler(1.3, self.theWord, app) # 新建一个对象, 并初始化传入延时的时间, 以及想要查找的字段
        self.crawler.start(self.theWord, 10, 1) # 总页码10, 开始页码1

        

    # 打包进线程（耗时的操作）
    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args) 
        t.setDaemon(True)   # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()           # 启动
        # t.join()          # 阻塞--会卡死界面！





# 程序执行起点
if __name__ == "__main__":   
    root = tk.Tk()  # 创建Tk对象
    app = Application(master=root)  # 新建一个Application对象
    app.mainloop()  # 开始时间循环
