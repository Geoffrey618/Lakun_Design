from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('send_email/', views.send_email, name='send_email'),
    path('sms/', views.sms_view, name='sms_view'),
    path('find_password/<str:username>/', views.find_password, name='find_password'),
    path('form_team/<str:username>/', views.form_team, name='form_team'),
    path('info/<str:username>/', views.info, name='info'),
    path('change_info/<str:username>/', views.change_info, name='change_info'),
]