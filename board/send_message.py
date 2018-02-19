# -*- coding:utf-8 -*-
import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse
from logreg.sender import use_sender, sender


def send_message(handle, content):
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

    url = 'http://codeforces.com/enter'
    opener = getOpener(header)
    data = opener.open(url).read()
    data = ungzip(data)
    csrf_token = get_csrf(data.decode())
    # print(data)
    use = str(sender(use_sender()))
    post_dict = {
        'csrf_token': csrf_token,
        'action': 'enter',
        'ftaa': 'g5a380v85956u33zgr',
        'bfaa': '7b5969570828ce4f737cbbc5c4b4a88f',
        'handle': use[:-1],
        'password': 'Aa123456',
        '_tta': '435'
    }
    # print(use)
    # print(handle)
    post_data = urllib.parse.urlencode(post_dict).encode()
    opener.open(url, post_data)
    url = 'http://codeforces.com/usertalk?other=' + str(handle)
    data = opener.open(url).read()
    data = ungzip(data)
    csrf_token = get_csrf(data.decode())
    post_dict = {
        'csrf_token': csrf_token,
        'action': 'sendMessage',
        'content': content,
        '_tta': '435'
    }
    post_data = urllib.parse.urlencode(post_dict).encode()
    opener.open(url, post_data)
    # print(data)
