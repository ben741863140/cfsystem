@echo off
echo 请问是否为第一次启动，是请输入y，否则输入n
@set/p first=

if "%first%" == "y" (
python first_time_config.py
python manage.py makemigrations
python manage.py migrate
)

echo 请输入系统运行占用的端口号
@set/p port=
start python manage.py runserver 0.0.0.0:%port% --insecure
start python manage.py celery worker --loglevel=info
start celery -A logsystem beat -l info --pidfile= 
exit