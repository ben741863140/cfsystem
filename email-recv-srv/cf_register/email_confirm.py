# -*- coding:utf-8 -*-
import requests
import re


def email_confirm(email):
    html = requests.get('http://www.scaucf.top:14000/to/' + email)
    if html.status_code != 200:
        print(email + ' The page is failed')
        return
    # print(html.text)
    r = re.compile('To confirm your email please follow the link <a href=\\\\\"(.*?)\\\\\">', re.S)
    if not (len(r.findall(html.text)) != 0 and r.findall(html.text)[0] != ''):
        print(email + ' No confirm email')
        return
    url = r.findall(html.text)[0]
    requests.get(url)
    if html.status_code != 200:
        print(email + ' open failed')
        return


if __name__ == '__main__':
    for i in range(26, 151):
        email = 'scau_support' + str(i) + '@scaucf.top'
        email_confirm(email)