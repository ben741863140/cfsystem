from django.conf.urls import url
from django.urls import path
from .views import auto_update, superuser_views
app_name = 'superuser'

urlpatterns = [
    url(r'^$', superuser_views.modify),
    path(r'get_config', auto_update.get_config, name='get_config'),
    path(r'set_auto_update', auto_update.set_auto_update, name='set_auto_update'),
    url(r'finished', auto_update.finished),
    url(r'del_cf_users', superuser_views.del_cf_users),
    url(r'list_add', superuser_views.list_add),
    url(r'list_override', superuser_views.list_override),
    url(r'board/create', superuser_views.create_board),


]