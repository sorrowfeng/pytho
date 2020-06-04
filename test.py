import requests

page_url = 'https://manhua.qpic.cn/manhua_detail/0/18_02_37_5b2a5f5c5ee4dc29161cb8786d04afdf_696.jpg/0'
filename = './test.jpg'

response = requests.get(page_url)
content = response.content
with open(filename, 'wb') as f:
    f.write(content)    # 写入图片信息