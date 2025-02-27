from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='homepage'), 
    path('login/', views.login_view, name='login'),
    path('userregister/', views.userregister_view, name='userregister'),
]