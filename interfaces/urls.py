from django.urls import path
from .views import login, super_register, register, get_board_list, send_captcha, get_board, create_board, \
    add_board_item, update_api

app_name = 'interfaces'

urlpatterns = [
    path('app_login_API', login, name='login'),
    path('app_super_register_API', super_register, name='s_register'),
    path('app_register_API', register, name='register'),
    path('app_send_captcha_API', send_captcha, name='send_captcha'),
    path('app_get_board_list_API', get_board_list, name='get_board_list'),
    path('app_get_board_API', get_board, name='get_board'),
    path('app_create_board_API', create_board, name='create_board'),
    path('app_add_board_item_API', add_board_item, name='add_board_item'),
    path('app_update_API', update_api, name='update'),
]
