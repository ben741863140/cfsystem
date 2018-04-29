from django.urls import path
from .views import board_rating
from .views import board_rating_change

app_name = 'board'

urlpatterns = [
    path('', board_rating),
    path('<int:id>/', board_rating),
    path('profile/<int:handle>/', board_rating_change),
]
