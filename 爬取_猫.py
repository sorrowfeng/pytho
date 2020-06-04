import urllib.request

response = urllib.request.urlopen('http://placekitten.com/300/500')
cat_img = response.read()

with open('cat_300_500.jpg', 'wb') as file: 
    file.write(cat_img)


