from django.urls import path
from . import views

urlpatterns = [
    path('create_project/<str:username>/', views.create_project, name='create_project'),
    path('get_project_list/', views.get_project_list, name='get_project_list'),
    path('get_project_detail/', views.get_project_detail, name='get_project_detail'),
    path('delete_project/<str:username>/', views.delete_project, name='delete_project'),
    path('rename_project/', views.rename_project, name='rename_project'),
    path('copy_project/<str:username>/', views.copy_project, name='copy_project'),
    path('search_project/<str:username>/', views.search_project, name='search_project'),
]