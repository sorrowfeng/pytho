import urllib.request
import os

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111')
    response = urllib.request.urlopen(url)
    html = response.read()
    return html


def get_page(url):
    html = url_open(url).decode('utf-8')
    a = html.find('current-comment-page') + 23
    b = html.find(']', a)

    print(html[a:b])


def find_imgs(url):
    html = url_open(url).decode('utf-8')
    img_addrs = []

    a = html.find('img src=')
    while a != -1:
        b = html.find('.jpg', a, a+255)
        if b != -1:
            img_addrs.append(html[a+9:b+4])
        else:
            b = a + 9
        a = html.find('img src=', b)
    
    for each in img_addrs:
        print(each)

def save_imgs(folder, img_adds):
    for each in img_adds:
        filename = each.split('/')[-1]
        with open(filename, 'wb') as f:
            img = url_open(each)
            f.write(img)


def download_mm(folder = 'OOXX', pages = 10):
    os.mkdir(folder)
    os.chdir(folder)

    url = "http://jandan.net/ooxx"
    page_num = int(get_page(url))

    for i in range(pages):
        page_num -= i
        page_url = url + '/page'
        img_adds =  find_imgs(page_url)
        save_imgs(folder, img_adds)


if __name__ == '__main__':
    download_mm()