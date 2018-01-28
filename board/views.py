from django.shortcuts import render
from board.models import CFUser, RatingChange
from board.update import update_rating, update_rating_change, load_cf_user


def board_view(request):
    class Info:
        rank = rating = oldRating = newRating = change = handle = 0
        name = ''

    select = 'ch1'
    if 'select' in request.GET.keys():
        select = request.GET['select']
    infos = []
    time = ''
    if select == 'ch1':
        for user in CFUser.objects.all():
            info = Info()
            info.rating = user.rating
            info.handle = user.handle
            infos.append(info)
        infos.sort(key=lambda x: x.rating, reverse=True)
    else:

        days_ago = int(select[2:])
        word = {'14': '两周', '30': '一月', '90': '三月', '180': '半年'}
        time = '近' + word[str(days_ago)]
        for user in RatingChange.objects.filter(days_ago=days_ago):
            info = Info()
            info.handle = user.cf_user.handle
            info.oldRating = user.oldRating
            info.newRating = user.newRating
            info.change = user.newRating - user.oldRating
            infos.append(info)
        infos.sort(key=lambda x: x.change, reverse=True)
    for info, rank in zip(infos, range(1, len(infos) + 1)):
        info.rank = rank
        if info.change > 0:
            info.change = '+' + str(info.change)
        else:
            info.change = str(info.change)
    return render(request, 'board/index.html',
                  {'is_ch1': select == 'ch1', 'rating': infos, 'Time': time})
