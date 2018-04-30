from django.urls import path
from .views import board_rating
from .views import board_rating_change

app_name = 'board'

urlpatterns = [
    path('', board_rating),
    path('<int:board_id>/', board_rating, name='board_view'),
    path('profile/<str:handle>/', board_rating_change, name='user_profile'),
]
