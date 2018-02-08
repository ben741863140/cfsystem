from django.conf.urls import url
from .views import auto_update, index
app_name = 'admin'

urlpatterns = [
    url(r'^$', index.index),
    url(r'get_config', auto_update.get_config),
    url(r'set_auto_update', auto_update.set_auto_update),
    url(r'del_cf_users', index.del_cf_users),
    url(r'list_add', index.list_add),
    url(r'list_override', index.list_override),


]