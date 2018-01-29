import threading, time, datetime, re
from board.update import update_rating_change, update_rating
from board.models import CFUser


class AutoUpdate(threading.Thread):

    def __init__(self, first_seconds):
        threading.Thread.__init__(self)
        self.first_seconds = first_seconds
        self.first = True
        self._keep_run = True

    def stop(self):
        self._keep_run = False

    def run(self):
        while self._keep_run:
            if self.first:
                self.first = False
                time.sleep(self.first_seconds)
            else:
                time.sleep(60 * 60 * 24)
            print('开始更新数据库...')
            update_rating()
            update_rating_change()


def auto_update():
    settings = get_settings()
    if settings['is_open'] and threading.active_count() == 1:
        now = datetime.datetime.now()
        now_time = (now.hour * 60 + now.minute) * 60
        set_time = (int(settings['hour']) * 60 + int(settings['minute'])) * 60
        if set_time < now_time:
            if len(CFUser.objects.all()) > 0:
                last_update = CFUser.objects.all()[0].last_update
                if last_update.day < now.day:
                    set_time = now_time
                else:
                    set_time += 60 * 60 * 24
            else:
                set_time += 60 * 60 * 24
        seconds = set_time - now_time
        left_hour = int(seconds / 3600)
        left_minute = int(seconds % 3600 / 60)
        if seconds:
            print('距离下次自动更新还有', left_hour, '小时', left_minute, '分钟')
        AutoUpdate(first_seconds=set_time - now_time).start()
    else:
        print('自动更新处于关闭状态')


def get_settings():
    settings = {'is_open': False}
    try:
        content = open(r'auto_update.ini', 'r').readlines()
    except FileNotFoundError:
        return settings
    if len(content) < 2:
        return settings
    if re.findall(re.compile('yes', re.IGNORECASE), content[0]):
        settings['is_open'] = True
    hour, minute = re.findall(re.compile(r'[0-9]{1,2}:[0-9]{1,2}'), content[1])[0].split(':')
    settings['hour'] = hour
    settings['minute'] = minute
    return settings
