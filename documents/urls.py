from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('create_document/', views.create_document, name='create_document'),
    re_path('create_folder/', views.create_folder, name='create_folder'),
    re_path('get_dic/', views.get_dic, name='get_dic'),
    re_path('receive_message/', views.receive_message, name='receive_message'),
    re_path('edit_document/<int:documentid>/', views.edit_document, name='edit_document'),
    re_path('document_detail/', views.document_detail, name='document_detail'),
    re_path('save_document/<int:documentid>/', views.save_document, name='save_document'),
]