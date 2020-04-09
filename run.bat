start python manage.py runserver 0.0.0.0:80 --insecure
start python manage.py celery worker --loglevel=info
start celery -A logsystem beat -l info --pidfile= 
exit