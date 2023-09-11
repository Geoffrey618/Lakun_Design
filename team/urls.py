from django.urls import path
from . import views

urlpatterns = [
    path('add_team_member/<str:username>/', views.add_team_member, name='add_team_member'),
    path('delete_team_member/<str:username>/', views.delete_team_member, name='delete_team_member'),
    path('add_admin/<str:username>/', views.add_admin, name='add_admin'),
    path('delete_admin/<str:username>/', views.delete_admin, name='delete_admin'),
    path('get_team_list/<str:username>/', views.get_team_list, name='get_team_list'),
    path('get_user_list/<str:teamname>/', views.get_user_list, name='get_user_list'),
]