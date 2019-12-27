from django.urls import path
from .views import login, super_register

app_name = 'interfaces'

urlpatterns = [
    path('app_login_API', login, name='login'),
]
