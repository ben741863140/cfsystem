from django.conf.urls import url
from django.urls import path
from .views import auto_update, index
app_name = 'admin'

urlpatterns = [
    url(r'^$', index.index),
    path(r'get_config', auto_update.get_config, name='get_config'),
    path(r'set_auto_update', auto_update.set_auto_update, name='set_auto_update'),
    url(r'finished', auto_update.finished),
    url(r'del_cf_users', index.del_cf_users),
    url(r'list_add', index.list_add),
    url(r'list_override', index.list_override),


]