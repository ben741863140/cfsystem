from django.conf.urls import url
from . import views

app_name = 'logreg'

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^reset_password/', views.reset_password, name='reset_password'),
    url(r'^modify_self/',views.modify_self, name='modify_self'),
]