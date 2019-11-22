from django.conf.urls import url
from django.urls import path
from .views import auto_update, superuser_views

app_name = 'superuser'

urlpatterns = [
    path('', superuser_views.modify),
    path('get_config', auto_update.get_config, name='get_config'),
    path('set_auto_update', auto_update.set_auto_update, name='set_auto_update'),
    url(r'finished', auto_update.finished),
    path('board/create', superuser_views.create_board),
    path('handle_controller', superuser_views.list_user, name='handle_controller'),
    path('handle_delete', superuser_views.delete_handle),
    path('download_excel', superuser_views.excel_export, name='excel_export'),
    path('modify_handle', superuser_views.edit_handle),
    path('jump_modify_board/<int:board_id>', superuser_views.jump_modify_board),
    path('modify_board_board', superuser_views.modify_board_board),
    path('delete_board', superuser_views.delete_board),
    path('manual_update/<int:only_board>', auto_update.manual_update, name='manual_update')
]
