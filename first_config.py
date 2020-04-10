# -*- coding: utf-8 -*-

import re
text = ''
with open('./logsystem/settings.py', 'rb') as obj1:
    text = obj1.read()
    # print(text)
    host = input('请按以下格式输入系统ip以及域名,例子：\'8.8.8.8\', \'www.scaucf.top\',\n')
    mysql_ip = input('请按以下格式输入Mysql的ip,例子：127.0.0.1 \n')
    mysql_handle = input('请输入Mysql的账号\n')
    mysql_password = input('请输入Mysql的密码\n')
    # print(host)
    p_host = 'ALLOWED_HOSTS = \[.*?\]'
    host = 'ALLOWED_HOSTS = [' + host + ']'
    text = re.sub(p_host, host, text.decode('utf-8'))

    p_handle = '\'USER\': .*?,'
    mysql_handle = '\'USER\': \'' + mysql_handle + '\','
    text = re.sub(p_handle, mysql_handle, text)

    p_ip = '\'HOST\': .*?,'
    mysql_ip = '\'HOST\': \'' + mysql_ip + '\','
    text = re.sub(p_ip, mysql_ip, text)

    p_password = '\'PASSWORD\': .*?,'
    mysql_password = '\'PASSWORD\': \'' + mysql_password + '\','
    text = re.sub(p_password, mysql_password, text)

with open('./logsystem/settings.py', 'w') as obj:
    # print(text)
    obj.write(text)
    obj1.close()
    obj.close()
