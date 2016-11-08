# -*-coding:utf-8-*-

import urllib.request, requests, re, platform, os
from bs4 import BeautifulSoup

url = 'http://chgyu1968.blog.163.com/blog/static/7449323201610871317333/'

response = urllib.request.urlopen(url)
content = response.read()
soup = BeautifulSoup(content.decode('gbk'), "html.parser")

"""content = requests.get(request).text
data = json.loads(content.decode('gbk'))
print(data)
count = 0
for dict in data['articles']:
    url = dict['imgsrc']
    count +=  1
    print(url)
    urllib.request.urlretrieve(url, url[url.rindex('.'):])
"""

# for jpgs in soup.findAll('key', values=re.compile(r'(?<=src=")\S+?jpg')):
for jpgs in soup.findAll(src=re.compile('.jpg')):
    print(jpgs['src'])
    if platform.system() != 'Windows':
        if os.path.exists('./tmp') is False:
            os.mkdir('./tmp')
        urllib.request.urlretrieve(jpgs['src'], './tmp/' + '%s.jpg' % jpgs['src'][-11:-4])
    else:
        if os.path.exists('.\\tmp') is False:
            os.mkdir('.\\tmp')
        urllib.request.urlretrieve(jpgs['src'], '.\\tmp\\' + '%s.jpg' % jpgs['src'][-11:-4])