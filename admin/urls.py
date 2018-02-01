from django.conf.urls import url
from .views import auto_update
app_name = 'admin'

urlpatterns = [
    url(r'get_config', auto_update.get_config),
    url(r'set_auto_update', auto_update.set_auto_update),
    # url(r'', auto_update.set_auto_update),  # for test

]