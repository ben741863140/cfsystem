from django.conf.urls import url
from . import views

app_name = 'logreg'

urlpatterns = [
    url(r'^register/', views.register, name='register'),
]