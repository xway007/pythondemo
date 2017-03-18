# -*-coding:utf-8 -*-
import requests
import urllib.request
import os
import shutil
from datetime import datetime
import threading

urldict = {}
savedir = './output'
cninfourl = 'http://www.cninfo.com.cn/'


class DownloadData(threading.Thread):
    def __init__(self, url, filename):
        threading.Thread.__init__(self)
        self.url = url
        self.filename = filename

    def run(self):
        try:
            response = urllib.request.urlopen(self.url)
            with open(self.filename, 'wb') as file:
                file.write(response.read())
        except Exception as e:
            print(e)
        print(self.filename)


# 从巨潮资讯解析出pdf的真实下载地址
def getpdfurl():
    with open('stock.txt', 'rb') as f:
        for line in f.readlines():
            # stkcd = line.decode('utf-8')
            code = line[:6].decode('gbk')
            if not code.isdigit():
                continue
            totalpages = pageno = 1
            while pageno <= totalpages:
                # 年报/半年报/招股说明书
                indexurl = cninfourl + 'cninfo-new/fulltextSearch/full?searchkey=' + code + '+年报&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=%d' % pageno
                response = requests.get(indexurl)
                jsondatas = response.json()
                totalpages = jsondatas['totalpages']
                pageno += 1
                for jsondata in jsondatas['announcements']:
                    if jsondata['adjunctType'] != 'PDF':
                        continue
                    if all(outwords not in jsondata['announcementTitle'] for outwords in ['摘要', '公告', '指标']):
                        pdfurl = cninfourl + jsondata['adjunctUrl']
                        secname = jsondata['secName'].replace(' ', '').replace('*', '')
                        date = str(jsondata['adjunctUrl']).split('/')[1]
                        urldict.update({code + '-' + secname + '-' + date + '.pdf': pdfurl})


# 根据解析出的pdf地址下载到output，并重命名成有规律的文件
# 多线程, urlopen, urlretrieve
def savefiles():
    if os.path.exists(savedir):
        shutil.move(savedir, savedir + datetime.now().strftime('%Y%m%d%H%M%S'))
    os.mkdir(savedir + '/')

    for name in urldict:
        url = urldict[name]
        filename = savedir + '/' + name
        '''
        response = urllib.request.urlopen(url)
        with open(filename, 'wb') as file:
            file.write(response.read())
            '''
        # urllib.request.urlretrieve(url, filename)
        DownloadData(url, filename).start()


if __name__ == '__main__':
    getpdfurl()
    savefiles()
