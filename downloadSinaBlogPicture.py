import urllib.request, http.cookiejar, re, os


def downloadsinablogpic(url):
    """page = urllib.request.Request(url,headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2902.0 Safari/537.36'})
    html = str(urllib.request.urlopen(page, timeout=60).read())"""

    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2902.0 Safari/537.36'}
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    headers = []
    for key, value in header.items():
        element = (key, value)
        headers.append(element)
    opener.addheaders = headers
    html = opener.open(url, timeout=60).read().decode()

    img_re = re.compile(r'(?<=real_src =").+?"')
    img_list = img_re.findall(html)
    if len(img_list) < 1:
        print('There are no images on this page')
    else:
        print("Begin Download SinaBlog Pictures")
        downloadnum = 0
        if os.path.exists('tmp') is False:
            os.makedirs('tmp')
        for i in range(len(img_list)):
            print("img_list[%d]=%s" % (i, img_list[i]))
            try:
                urllib.request.urlretrieve(img_list[i], '.\\tmp\\' + '%s.jpg' % img_list[i][img_list[i].rfind('/') + 1:-1].replace('amp;', ''))
            except Exception as e:
                print(e)
                continue
            downloadnum += 1
            print("Download Success")
        if downloadnum == 0:
            print("There are errors occurred during downloading")
        elif downloadnum == 1:
            print("Total Download %d Picture" % downloadnum)
        else:
            print("Total Download %d Pictures" % downloadnum)


if __name__ == "__main__":
    url_sina = "http://blog.sina.com.cn/s/blog_6175bf700102wv6h.html"
    downloadsinablogpic(url_sina)
