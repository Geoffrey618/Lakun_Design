from django.urls import path
from . import views

urlpatterns = [
    path('get_message_list/<str:username>/', views.get_message_list, name='get_message_list'),
    path('mark_message_as_read/<str:messageid>/', views.mark_message_as_read, name='mark_message_as_read'),
    path('message_detail/<str:messageid>/', views.message_detail, name='message_detail'),
    path('delete_message/<str:messageid>/', views.delete_message, name='delete_message'),
    path('mark_all_unread_as_read/<str:username>/', views.mark_all_unread_as_read, name='mark_all_unread_as_read'),
    path('delete_all_messages_for_user/<str:username>/', views.delete_all_messages_for_user, name='delete_all_messages_for_user'),
    path('receive_chat_message/', views.receive_chat_message, name='receive_chat_message'),
    path('prompt_chat/', views.prompt_chat, name='prompt_chat'),
]