import requests
from lxml import etree
import os

all_url = "http://www.xbiquge.la/xiaoshuodaquan/"

def list_dic(list1,list2):
    '''
    two lists merge a dict,a list as key,other list as value
    :param list1:key
    :param list2:value
    :return:dict
    '''
    dic = dict(map(lambda x,y:[x,y], list1,list2))
    return dic

class Spider:

    def __init__(self, word):
        self.word = word


    def start_requests(self):
        # 1. 请求网站拿到数据，抽取小说名创建文件夹，抽取小说链接
        # start_url = search_url + str(self.word)
        start_url = all_url
        print(start_url)
        response = requests.get(start_url)
        myhtml = etree.HTML(response.text)
        # print(myhtml)
        name_list = myhtml.xpath("//div[@class='novellist']/ul/li/a/text()")
        url_list = myhtml.xpath("//div[@class='novellist']/ul/li/a/@href")

        new_dic = list_dic(name_list, url_list)
        # print(new_dic)

        shu_name = self.word
        shu_url = new_dic.get(self.word)     
        

        if shu_url == None:
            print("没有找到此书")
            return
        else:
            if os.path.exists(shu_name) == False:
                os.mkdir(shu_name)
            self.requests_zhang(shu_name,shu_url)
       



    def requests_zhang(self,shu_name,shu_url):
        # 2. 请求小说拿到数据，抽取章名、文章链接
        response = requests.get(shu_url)
        #乱码 header显示编码格式是ISO-8859-1 内容的格式是utf-8 需要修改代码格式
        response.encoding='utf-8'
        # print(response.encoding) #没定义编码格式的时候，header显示的编码格式
        # print(response.apparent_encoding) #内容实际采用的编码格式
        # print(response.headers) #查看头标签内容
        html = etree.HTML(response.text)
        zhang_name_list = html.xpath('//div[@id="list"]/dl/dd/a/text()')
        zhang_url_list =html.xpath('//div[@id="list"]/dl/dd/a/@href')
        for zhang_name,zhang_url in zip(zhang_name_list,zhang_url_list):
            self.requests_data(zhang_name,zhang_url,shu_name)
            # print(zhang_name_list, zhang_url_list)


    def requests_data(self,zhang_name,zhang_url,shu_name):
        # 3. 请求文章拿到文章内容，创建文件保存到相应文件夹
        data_url = 'http://www.xbiquge.la'+zhang_url
        response = requests.get(data_url)
        response.encoding='utf-8'
        html = etree.HTML(response.text)
        content = "\n".join(html.xpath('//div[@id="content"]/text()'))
        # print(zhang_name)
        zhang_name = zhang_name[0:16].split('（')[0]
        
        file_name = shu_name + '\\' + shu_name + '.txt'
        print("正在下载："+zhang_name)
        with open(file_name,"a",encoding='utf-8') as f:
            f.write('\n\n'+str(zhang_name)+'\n\n\n')
            f.write(content)



if __name__ == '__main__':
    word = input('你想要下载什么?请输入:')
    spider = Spider(word)
    spider.start_requests()

