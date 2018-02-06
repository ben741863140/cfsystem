from django.conf.urls import url
from .views import board_upgrade
from .views import board_rating

app_name = 'board'

urlpatterns = [
    url(r'^$', board_rating),
    url(r'^([0-9]+)$', board_upgrade),
]