# -*- coding:utf-8 -*-
import requests
from lxml import etree


def register(username, email, password):
    headers = {
        "authority": "codeforces.com",
        "cache-control": "max-age=0",
        "origin": "https://codeforces.com",
        "upgrade-insecure-requests": "1",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "sec-fetch-user": "?1",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "referer": "https://codeforces.com/register",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookie": "JSESSIONID=787DF343C7D9008A73731C35FD035E52-n1; 39ce7=CF3UImrw; __utmc=71512449; __utmz=71512449.1579315239.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); evercookie_png=7l1qkls67n8b2aqpg9; evercookie_etag=7l1qkls67n8b2aqpg9; evercookie_cache=7l1qkls67n8b2aqpg9; 70a7c28f3de=7l1qkls67n8b2aqpg9; __utma=71512449.212828981.1579315239.1579319861.1579326406.3; __utmb=71512449.7.10.1579326406",
    }

    data = {
        "csrf_token": "8a225d637554f70085bdc7aeebe1f98f",
        "ftaa": "7l1qkls67n8b2aqpg9",
        "bfaa": "f3ea9361c7421f8ba7b676b9042e634a",
        "action": "register",
        "handle": username,
        "name": "0e09e58c",
        "age": "",
        "email": email,
        "password": password,
        "passwordConfirmation": password,
        "_tta": "95",
    }

    response = requests.post(
        "https://codeforces.com/register", headers=headers, data=data
    )
    html = etree.HTML(response.text)
    handle = html.xpath('//span[@class="error for__handle"]/text()')
    pwd = html.xpath('//span[@class="error for__password"]/text()')
    eml = html.xpath('//span[@class="error for__email"]/text()')

    # print(handle)
    #
    # print(pwd)
    #
    # print(eml)
    if (
        "Something went wrong. Please, try again later" in response.text
        or len(handle) > 0
        or len(pwd) > 0
        or len(eml) > 0
    ):
        print("验证有误")
    else:
        print("验证成功")
        response1 = requests.get(
            f"https://codeforces.com/register/afterRegistration?handle={username}",
            headers=headers,
        )
        if "Thank you for your interest in Codeforces" in response1.text:
            print("邮件发送成功")
        else:
            print("邮件发送失败")


if __name__ == "__main__":
    for i in range(143, 144):
        handle = 'scau_support' + str(i)
        email =  'scau_support' + str(i) + '@scaucf.top'
        register(handle, email, "scaucf")