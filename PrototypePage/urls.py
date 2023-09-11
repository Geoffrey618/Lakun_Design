from django.urls import path
from . import views

urlpatterns = [
    path('create_page/', views.create_page, name='create_page'),
    path('edit_page/<int:page_id>/', views.edit_page, name='edit_page'),
    path('export_page/<int:page_id>/', views.export_page, name='export_page'),
    path('get_page_content/', views.get_page_content, name='get_page_content'),
]