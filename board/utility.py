import requests
from bs4 import BeautifulSoup
import datetime, re


def get_rating(handle):
    handle = str(handle)
    url = 'http://codeforces.com/api/user.info?handles=' + handle
    results = BeautifulSoup(requests.get(url).text, 'html.parser').text
    results = eval(results)
    if results['status'] != 'OK':
        results['comment'] = 'handle: ' + handle + ' 不存在'
        return results
    info = results['result'][0]
    if 'rating' not in info.keys():
        info['rating'] = 0
    res = {'status': 'OK', 'rating': info['rating']}
    return res


def get_rating_change(cf_user, *days_ago):
    url = 'http://codeforces.com/api/user.rating?handle=' + cf_user.handle
    results = BeautifulSoup(requests.get(url).text, 'html.parser').text
    results = eval(results)
    if results['status'] != 'OK':
        raise Exception(results['comment'])
    res = {}
    now_rating = 0
    for info in results['result']:
        now_rating = info['newRating']
        update_time = datetime.datetime.fromtimestamp(info['ratingUpdateTimeSeconds'])
        for day in filter(lambda x: x if x not in res.keys() else None, days_ago):
            if (datetime.datetime.now() - update_time).days <= day:
                res[day] = info['oldRating']
    res['newRating'] = now_rating
    for day in filter(lambda x: x if x not in res.keys() else None, days_ago):
        res[day] = now_rating
    return res


def get_user_info(line):
    handle = re.findall(re.compile(r'[0-9a-zA-Z_]{3,24}'), line)
    realname = re.findall(re.compile(r'[\u4e00-\u9fa5]{2,3}'), line)
    if len(handle) == 0 or len(handle) > 1 or len(realname) > 1:
        return {'status': 'FAILED', 'comment': '无法识别'}
    if len(realname) == 0:
        realname.append('')
    res = get_rating(handle[0])
    res['realname'] = realname[0]
    res['handle'] = handle[0].lower()
    return res
