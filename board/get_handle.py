# -*- coding:utf-8 -*-
import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse

def get_handle(handle):
    def ungzip(data):
        return gzip.decompress(data)

    def get_csrf(data):
        cer = re.compile('data-csrf=\'(.*?)\'>&nbsp;</span>', re.S)
        return cer.findall(data)[0]

    def getOpener(head):
        # deal with coookie
        cj = http.cookiejar.CookieJar()
        pro = urllib.request.HTTPCookieProcessor(cj)
        opener = urllib.request.build_opener(pro)
        header = []
        for key, value in head.items():
            elem = (key, value)
            header.append(elem)
        opener.addheaders = header
        return opener

    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'www.codeforces.com',
        'DNT': '1'
    }
    url = 'http://codeforces.com/profile/'+handle
    opener = getOpener(header)
    data = opener.open(url).read()
    data = ungzip(data)
    # csrf_token = get_csrf(data.decode())
    # print(data)
    temp = re.compile('%2Fprofile%2F(.*?)">', re.S)
    try:
        x = temp.findall(data.decode())[0]
    except IndexError:
        return ''
    # print(str(x))
    return str(x)
