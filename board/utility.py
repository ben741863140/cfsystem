import requests
from bs4 import BeautifulSoup
from board.models import CFUser, RatingChange
import datetime


def get_rating(*handles):
    url = 'http://codeforces.com/api/user.info?handles='
    for handle in handles:
        url += str(handle) + ';'
    results = BeautifulSoup(requests.get(url).text, 'html.parser').text
    results = eval(results)
    res = {}
    if results['status'] != 'OK':
        raise Exception(results['comment'])
    for info in results['result']:
        res[info['handle'].lower()] = info['rating']
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


