import requests
from bs4 import BeautifulSoup


def get_rating(handle):
    handle = str(handle)
    url = 'http://codeforces.com/api/user.info?handles=' + handle
    results = BeautifulSoup(requests.get(url).text, 'html.parser').text
    print('我是10行--debug')
    results = eval(results)
    print('我是12行--debug')
    if results['status'] != 'OK':
        results['comment'] = 'handle: ' + handle + ' 不存在'
        return results
    info = results['result'][0]
    if 'rating' not in info.keys():
        info['rating'] = 0
    res = {'status': 'OK', 'rating': info['rating']}
    return res


def get_rating_change(handle):
    url = 'http://codeforces.com/api/user.rating?handle=' + str(handle)
    results = BeautifulSoup(requests.get(url).text, 'html.parser').text
    print('我是24行--debug')
    results = eval(results)
    print('我是26行--debug')
    if results['status'] != 'OK':
        raise Exception(results['comment'])
    return results['result']
