import threading, time, datetime, re
from board.update import update_rating_change, update_rating
from board.models import CFUser


class UpdateSetting:
    def __init__(self, is_open=False, hour=0, minute=0):
        self.is_open = is_open
        self.hour = hour
        self.minute = minute

    def write_setting(self):
        open(r'auto_update.ini', 'w').close()
        file = open(r'auto_update.ini', 'a')
        if self.is_open:
            print('is_open: YES', file=file)
        else:
            print('is_open: NO', file=file)
        print('time: %02d:%02d' % (int(self.hour), int(self.minute)), file=file)
        file.close()

    def get_seconds(self):
        return self.hour * 3600 + self.minute * 60

    def load_setting(self):
        self.is_open = False
        try:
            content = open(r'auto_update.ini', 'r').readlines()
        except FileNotFoundError:
            return
        if len(content) < 2:
            return
        if re.findall(re.compile('yes', re.IGNORECASE), content[0]):
            self.is_open = True
        hour, minute = re.findall(re.compile(r'[0-9]{1,2}:[0-9]{1,2}'), content[1])[0].split(':')
        self.hour = int(hour)
        self.minute = int(minute)


class AutoUpdate(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self._keep_run = True
        self.update_setting = UpdateSetting()

    def stop(self):
        self._keep_run = False

    def run(self):
        while self._keep_run:
            if self.ready():
                self.update()
            time.sleep(10 * 60)

    def ready(self):
        diff = datetime.datetime.now() - get_farthest_update()
        if diff.days >= 1:
            return True
        if diff.seconds <= 60 * 30:
            return False
        self.update_setting.load_setting()
        diff = get_now_seconds() - self.update_setting.get_seconds()
        return 0 <= diff <= 15 * 60

    @staticmethod
    def update():
        print('开始更新数据库...')
        update_rating_change()
        update_rating()
        print('数据库更新完成')


def get_now_seconds():
    now = datetime.datetime.now()
    return now.hour * 3600 + now.minute * 60 + now.second


def get_farthest_update():
    _time = datetime.datetime.now()
    for user in CFUser.objects.all():
        _time = min(_time, user.last_update)
    return _time


def auto_update():
    if threading.active_count() == 1:  # 防止多次启动（似乎不用）
        AutoUpdate().start()
