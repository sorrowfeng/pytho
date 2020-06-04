import urllib.request

url = 'https://www.whatismyip.com/'

proxy_support = urllib.request.ProxyHandler({'https': '123.110.219.104'})

opener = urllib.request.build_opener(proxy_support)
opener.add_headers = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111')]


urllib.request.install_opener(opener)

response = urllib.request.urlopen(url)
html = response.read().decode('utf-8')

print(html)
