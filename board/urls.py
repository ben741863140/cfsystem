from django.urls import path
from django.conf.urls import url
from .views import board_rating
from .views import board_rating_change

app_name = 'board'

urlpatterns = [
    path('', board_rating),
    path('<int:board_id>/', board_rating, name='board_view'),
    url(r'^profile/([0-9a-zA-Z_]+)', board_rating_change),
]
