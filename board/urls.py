from django.conf.urls import url
from .views import board_rating
from .views import board_rating_change

app_name = 'board'

urlpatterns = [
    url(r'^$', board_rating),
    url(r'^([0-9]+)$', board_rating),
    url(r'^profile/([0-9a-zA-Z_]+)', board_rating_change),
]